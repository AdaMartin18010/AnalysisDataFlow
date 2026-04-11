#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用自动检查器 (Cross-Reference Validator)

功能：
- 扫描所有Markdown文件中的链接
- 验证内部链接有效性（文件存在、锚点存在）
- 验证外部链接可访问性（HTTP 200）
- 生成详细的错误报告
- 支持增量检查（只检查变更文件）

作者: Automation Agent
版本: 1.0.0
"""

import re
import json
import hashlib
import asyncio
import aiohttp
import argparse
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Set, Optional, Tuple, Any
from datetime import datetime
from urllib.parse import urlparse, urljoin
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LinkType(Enum):
    """链接类型枚举"""
    INTERNAL_FILE = "internal_file"      # 内部文件链接 [text](path/to/file.md)
    INTERNAL_ANCHOR = "internal_anchor"  # 内部锚点链接 [text](path/to/file.md#anchor)
    EXTERNAL_URL = "external_url"        # 外部URL链接 [text](https://...)
    REFERENCE = "reference"              # 引用链接 [^n]


class LinkStatus(Enum):
    """链接状态枚举"""
    VALID = "valid"
    INVALID = "invalid"
    WARNING = "warning"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class LinkInfo:
    """链接信息数据类"""
    source_file: str
    link_text: str
    link_target: str
    link_type: LinkType
    line_number: int
    column_number: int
    status: LinkStatus = LinkStatus.VALID
    message: str = ""
    http_status: Optional[int] = None
    response_time_ms: Optional[float] = None


@dataclass
class ValidationResult:
    """验证结果数据类"""
    total_files: int = 0
    total_links: int = 0
    valid_links: int = 0
    invalid_links: int = 0
    warning_links: int = 0
    error_links: int = 0
    skipped_links: int = 0
    links: List[LinkInfo] = field(default_factory=list)
    scan_time: str = ""
    duration_seconds: float = 0.0


class CrossRefValidator:
    """交叉引用验证器主类"""
    
    # Markdown链接正则表达式
    MD_LINK_PATTERN = re.compile(
        r'\[([^\]]+)\]\(([^)]+)\)',
        re.MULTILINE
    )
    
    # 引用链接正则 [^n]
    REF_PATTERN = re.compile(
        r'\[\^(\d+)\]',
        re.MULTILINE
    )
    
    # 锚点定义正则 [^n]: ...
    REF_DEF_PATTERN = re.compile(
        r'^\[\^(\d+)\]:\s*(.+)$',
        re.MULTILINE
    )
    
    # HTML锚点ID模式
    ANCHOR_PATTERN = re.compile(
        r'<a[^>]*id=["\']([^"\']+)["\'][^>]*>',
        re.IGNORECASE
    )
    
    # 标题锚点模式
    HEADING_PATTERN = re.compile(
        r'^(#{1,6})\s+(.+)$',
        re.MULTILINE
    )
    
    def __init__(
        self,
        root_dir: Path,
        cache_file: Optional[Path] = None,
        timeout: int = 30,
        max_concurrent: int = 10,
        skip_external: bool = False,
        skip_patterns: Optional[List[str]] = None
    ):
        """
        初始化验证器
        
        Args:
            root_dir: 项目根目录
            cache_file: 缓存文件路径
            timeout: HTTP请求超时时间（秒）
            max_concurrent: 最大并发请求数
            skip_external: 是否跳过外部链接检查
            skip_patterns: 跳过的文件模式列表
        """
        self.root_dir = Path(root_dir).resolve()
        self.cache_file = cache_file or self.root_dir / ".link_cache.json"
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self.skip_external = skip_external
        self.skip_patterns = skip_patterns or [
            "node_modules", ".git", "__pycache__", 
            ".venv", "venv", "archive"
        ]
        self.cache: Dict[str, Any] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        
    def _load_cache(self) -> None:
        """加载缓存"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
                logger.info(f"已加载缓存: {self.cache_file}")
            except Exception as e:
                logger.warning(f"加载缓存失败: {e}")
                self.cache = {}
                
    def _save_cache(self) -> None:
        """保存缓存"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
            logger.info(f"缓存已保存: {self.cache_file}")
        except Exception as e:
            logger.error(f"保存缓存失败: {e}")
            
    def _get_file_hash(self, file_path: Path) -> str:
        """计算文件哈希值"""
        content = file_path.read_bytes()
        return hashlib.md5(content).hexdigest()
        
    def _should_check_file(self, file_path: Path, changed_files: Optional[Set[str]] = None) -> bool:
        """判断是否需要检查文件"""
        if changed_files is not None:
            rel_path = str(file_path.relative_to(self.root_dir))
            return rel_path in changed_files
        return True
        
    def _is_external_url(self, url: str) -> bool:
        """判断是否为外部URL"""
        parsed = urlparse(url)
        return bool(parsed.scheme and parsed.netloc)
        
    def _extract_anchors(self, content: str) -> Set[str]:
        """从Markdown内容中提取所有锚点"""
        anchors = set()
        
        # HTML锚点
        for match in self.ANCHOR_PATTERN.finditer(content):
            anchors.add(match.group(1))
            
        # 标题锚点（转换为GitHub风格的slug）
        for match in self.HEADING_PATTERN.finditer(content):
            heading_text = match.group(2).strip()
            # 转换为小写，移除标点，空格替换为-
            anchor = re.sub(r'[^\w\s-]', '', heading_text.lower())
            anchor = re.sub(r'[-\s]+', '-', anchor).strip('-')
            if anchor:
                anchors.add(anchor)
                
        return anchors
        
    def _extract_references(self, content: str) -> Dict[str, str]:
        """提取引用定义"""
        refs = {}
        for match in self.REF_DEF_PATTERN.finditer(content):
            ref_id = match.group(1)
            ref_content = match.group(2).strip()
            refs[ref_id] = ref_content
        return refs
        
    def _parse_link(self, link_target: str) -> Tuple[str, Optional[str]]:
        """
        解析链接为目标文件和锚点
        
        Returns:
            (文件路径, 锚点或None)
        """
        if '#' in link_target:
            parts = link_target.split('#', 1)
            return parts[0], parts[1] if parts[1] else None
        return link_target, None
        
    def scan_file(self, file_path: Path) -> List[LinkInfo]:
        """
        扫描单个Markdown文件中的所有链接
        
        Args:
            file_path: Markdown文件路径
            
        Returns:
            链接信息列表
        """
        links = []
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # 扫描Markdown链接
        for match in self.MD_LINK_PATTERN.finditer(content):
            link_text = match.group(1)
            link_target = match.group(2)
            
            # 计算行号和列号
            pos = match.start()
            line_num = content[:pos].count('\n') + 1
            line_start = content.rfind('\n', 0, pos) + 1
            col_num = pos - line_start + 1
            
            # 确定链接类型
            if self._is_external_url(link_target):
                link_type = LinkType.EXTERNAL_URL
            elif '#' in link_target and not link_target.startswith('#'):
                link_type = LinkType.INTERNAL_ANCHOR
            else:
                link_type = LinkType.INTERNAL_FILE
                
            links.append(LinkInfo(
                source_file=str(file_path.relative_to(self.root_dir)),
                link_text=link_text,
                link_target=link_target,
                link_type=link_type,
                line_number=line_num,
                column_number=col_num
            ))
            
        # 扫描引用链接
        for match in self.REF_PATTERN.finditer(content):
            ref_id = match.group(1)
            pos = match.start()
            line_num = content[:pos].count('\n') + 1
            line_start = content.rfind('\n', 0, pos) + 1
            col_num = pos - line_start + 1
            
            links.append(LinkInfo(
                source_file=str(file_path.relative_to(self.root_dir)),
                link_text=f"[^{ref_id}]",
                link_target=ref_id,
                link_type=LinkType.REFERENCE,
                line_number=line_num,
                column_number=col_num
            ))
            
        return links
        
    def validate_internal_link(self, link: LinkInfo) -> LinkInfo:
        """验证内部链接"""
        source_file = self.root_dir / link.source_file
        file_path, anchor = self._parse_link(link.link_target)
        
        # 处理相对路径
        if not file_path:
            # 只有锚点，指向当前文件
            target_file = source_file
        elif file_path.startswith('/'):
            target_file = self.root_dir / file_path.lstrip('/')
        else:
            target_file = source_file.parent / file_path
            
        # 检查文件是否存在
        if not target_file.exists():
            link.status = LinkStatus.INVALID
            link.message = f"目标文件不存在: {target_file.relative_to(self.root_dir)}"
            return link
            
        # 检查锚点是否存在
        if anchor:
            try:
                content = target_file.read_text(encoding='utf-8')
                anchors = self._extract_anchors(content)
                
                if anchor not in anchors:
                    link.status = LinkStatus.WARNING
                    link.message = f"锚点不存在: #{anchor}"
                else:
                    link.status = LinkStatus.VALID
                    link.message = "链接有效"
            except Exception as e:
                link.status = LinkStatus.ERROR
                link.message = f"读取文件失败: {e}"
        else:
            link.status = LinkStatus.VALID
            link.message = "文件存在"
            
        return link
        
    async def validate_external_link(self, link: LinkInfo) -> LinkInfo:
        """验证外部链接"""
        if self.skip_external:
            link.status = LinkStatus.SKIPPED
            link.message = "外部链接检查已跳过"
            return link
            
        url = link.link_target
        cache_key = f"ext:{url}"
        
        # 检查缓存
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            link.status = LinkStatus(cached['status'])
            link.message = cached['message']
            link.http_status = cached.get('http_status')
            return link
            
        try:
            if not self.session:
                timeout = aiohttp.ClientTimeout(total=self.timeout)
                self.session = aiohttp.ClientSession(timeout=timeout)
                
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
            }
            
            start_time = asyncio.get_event_loop().time()
            async with self.session.head(url, headers=headers, allow_redirects=True) as response:
                duration = (asyncio.get_event_loop().time() - start_time) * 1000
                link.response_time_ms = round(duration, 2)
                link.http_status = response.status
                
                if response.status == 200:
                    link.status = LinkStatus.VALID
                    link.message = "链接可访问"
                elif response.status in [301, 302, 307, 308]:
                    link.status = LinkStatus.WARNING
                    link.message = f"重定向: {response.status}"
                elif response.status == 429:
                    link.status = LinkStatus.WARNING
                    link.message = "请求过多 (429)，请稍后重试"
                elif response.status >= 500:
                    link.status = LinkStatus.WARNING
                    link.message = f"服务器错误: {response.status}"
                else:
                    link.status = LinkStatus.INVALID
                    link.message = f"HTTP {response.status}"
                    
        except asyncio.TimeoutError:
            link.status = LinkStatus.WARNING
            link.message = f"请求超时 (>{self.timeout}s)"
        except Exception as e:
            link.status = LinkStatus.ERROR
            link.message = f"请求失败: {str(e)[:100]}"
            
        # 更新缓存
        self.cache[cache_key] = {
            'status': link.status.value,
            'message': link.message,
            'http_status': link.http_status,
            'checked_at': datetime.now().isoformat()
        }
        
        return link
        
    def validate_reference(self, link: LinkInfo, all_refs: Dict[str, Dict[str, str]]) -> LinkInfo:
        """验证引用链接"""
        source_file = link.source_file
        ref_id = link.link_target
        
        if source_file in all_refs and ref_id in all_refs[source_file]:
            link.status = LinkStatus.VALID
            link.message = "引用定义存在"
        else:
            link.status = LinkStatus.INVALID
            link.message = f"引用 [^{ref_id}] 未定义"
            
        return link
        
    async def run(
        self,
        file_pattern: str = "**/*.md",
        changed_files: Optional[Set[str]] = None
    ) -> ValidationResult:
        """
        运行验证
        
        Args:
            file_pattern: 文件匹配模式
            changed_files: 变更文件集合（增量检查）
            
        Returns:
            验证结果
        """
        start_time = datetime.now()
        self._load_cache()
        
        result = ValidationResult()
        result.scan_time = start_time.isoformat()
        
        # 收集所有Markdown文件
        md_files = list(self.root_dir.glob(file_pattern))
        md_files = [
            f for f in md_files 
            if not any(p in str(f) for p in self.skip_patterns)
        ]
        
        result.total_files = len(md_files)
        logger.info(f"发现 {len(md_files)} 个Markdown文件")
        
        # 预加载所有引用定义
        all_refs: Dict[str, Dict[str, str]] = {}
        for file_path in md_files:
            rel_path = str(file_path.relative_to(self.root_dir))
            content = file_path.read_text(encoding='utf-8')
            all_refs[rel_path] = self._extract_references(content)
            
        # 验证内部链接
        internal_links: List[LinkInfo] = []
        external_links: List[LinkInfo] = []
        reference_links: List[LinkInfo] = []
        
        for file_path in md_files:
            if not self._should_check_file(file_path, changed_files):
                continue
                
            links = self.scan_file(file_path)
            
            for link in links:
                if link.link_type in [LinkType.INTERNAL_FILE, LinkType.INTERNAL_ANCHOR]:
                    internal_links.append(link)
                elif link.link_type == LinkType.EXTERNAL_URL:
                    external_links.append(link)
                elif link.link_type == LinkType.REFERENCE:
                    reference_links.append(link)
                    
        logger.info(f"发现 {len(internal_links)} 个内部链接, {len(external_links)} 个外部链接, {len(reference_links)} 个引用")
        
        # 验证内部链接
        for link in internal_links:
            validated = self.validate_internal_link(link)
            result.links.append(validated)
            
        # 验证引用链接
        for link in reference_links:
            validated = self.validate_reference(link, all_refs)
            result.links.append(validated)
            
        # 异步验证外部链接
        if external_links and not self.skip_external:
            semaphore = asyncio.Semaphore(self.max_concurrent)
            
            async def validate_with_limit(link: LinkInfo) -> LinkInfo:
                async with semaphore:
                    return await self.validate_external_link(link)
                    
            external_results = await asyncio.gather(*[
                validate_with_limit(link) for link in external_links
            ])
            result.links.extend(external_results)
            
            # 关闭session
            if self.session:
                await self.session.close()
                self.session = None
                
        # 统计结果
        for link in result.links:
            result.total_links += 1
            if link.status == LinkStatus.VALID:
                result.valid_links += 1
            elif link.status == LinkStatus.INVALID:
                result.invalid_links += 1
            elif link.status == LinkStatus.WARNING:
                result.warning_links += 1
            elif link.status == LinkStatus.ERROR:
                result.error_links += 1
            elif link.status == LinkStatus.SKIPPED:
                result.skipped_links += 1
                
        # 计算耗时
        result.duration_seconds = (datetime.now() - start_time).total_seconds()
        
        # 保存缓存
        self._save_cache()
        
        return result
        
    def generate_json_report(self, result: ValidationResult, output_path: Path) -> None:
        """生成JSON格式报告"""
        report_data = {
            'scan_time': result.scan_time,
            'duration_seconds': result.duration_seconds,
            'summary': {
                'total_files': result.total_files,
                'total_links': result.total_links,
                'valid_links': result.valid_links,
                'invalid_links': result.invalid_links,
                'warning_links': result.warning_links,
                'error_links': result.error_links,
                'skipped_links': result.skipped_links,
                'validity_rate': round(
                    result.valid_links / result.total_links * 100, 2
                ) if result.total_links > 0 else 0
            },
            'links': [
                {
                    'source_file': link.source_file,
                    'link_text': link.link_text,
                    'link_target': link.link_target,
                    'link_type': link.link_type.value,
                    'line_number': link.line_number,
                    'column_number': link.column_number,
                    'status': link.status.value,
                    'message': link.message,
                    'http_status': link.http_status,
                    'response_time_ms': link.response_time_ms
                }
                for link in result.links
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
            
        logger.info(f"JSON报告已生成: {output_path}")
        
    def generate_markdown_summary(self, result: ValidationResult, output_path: Path) -> None:
        """生成Markdown格式摘要"""
        lines = [
            "# 交叉引用验证报告",
            "",
            f"> **扫描时间**: {result.scan_time}",
            f"> **扫描耗时**: {result.duration_seconds:.2f} 秒",
            "",
            "## 统计摘要",
            "",
            "| 指标 | 数值 |",
            "|------|------|",
            f"| 扫描文件数 | {result.total_files} |",
            f"| 总链接数 | {result.total_links} |",
            f"| ✓ 有效链接 | {result.valid_links} |",
            f"| ✗ 无效链接 | {result.invalid_links} |",
            f"| ⚠ 警告链接 | {result.warning_links} |",
            f"| ✕ 错误链接 | {result.error_links} |",
            f"| ○ 跳过链接 | {result.skipped_links} |",
            f"| **有效率** | {round(result.valid_links / result.total_links * 100, 2) if result.total_links > 0 else 0}% |",
            "",
            "## 问题详情",
            "",
        ]
        
        # 按状态分组
        invalid_links = [l for l in result.links if l.status == LinkStatus.INVALID]
        warning_links = [l for l in result.links if l.status == LinkStatus.WARNING]
        error_links = [l for l in result.links if l.status == LinkStatus.ERROR]
        
        if invalid_links:
            lines.extend([
                "### 无效链接",
                "",
            ])
            for link in invalid_links[:50]:  # 最多显示50条
                lines.append(
                    f"- `{link.source_file}:{link.line_number}` | "
                    f"[{link.link_text}]({link.link_target}) | {link.message}"
                )
            if len(invalid_links) > 50:
                lines.append(f"\n... 还有 {len(invalid_links) - 50} 条无效链接")
            lines.append("")
            
        if warning_links:
            lines.extend([
                "### 警告链接",
                "",
            ])
            for link in warning_links[:30]:
                lines.append(
                    f"- `{link.source_file}:{link.line_number}` | "
                    f"[{link.link_text}]({link.link_target}) | {link.message}"
                )
            if len(warning_links) > 30:
                lines.append(f"\n... 还有 {len(warning_links) - 30} 条警告")
            lines.append("")
            
        if error_links:
            lines.extend([
                "### 错误链接",
                "",
            ])
            for link in error_links[:20]:
                lines.append(
                    f"- `{link.source_file}:{link.line_number}` | "
                    f"[{link.link_text}]({link.link_target}) | {link.message}"
                )
            lines.append("")
            
        if not any([invalid_links, warning_links, error_links]):
            lines.append("✅ 所有链接均有效！\n")
            
        lines.extend([
            "",
            "---",
            "*由 cross-ref-validator.py 自动生成*",
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
            
        logger.info(f"Markdown摘要已生成: {output_path}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='交叉引用自动检查器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                          # 检查所有Markdown文件
  %(prog)s --incremental file1.md   # 只检查指定文件
  %(prog)s --skip-external          # 跳过外部链接检查
  %(prog)s --output-dir ./reports   # 指定输出目录
        """
    )
    
    parser.add_argument(
        '--root-dir',
        type=str,
        default='.',
        help='项目根目录 (默认: 当前目录)'
    )
    
    parser.add_argument(
        '--file-pattern',
        type=str,
        default='**/*.md',
        help='文件匹配模式 (默认: **/*.md)'
    )
    
    parser.add_argument(
        '--incremental',
        nargs='+',
        help='增量检查：只检查指定的文件列表'
    )
    
    parser.add_argument(
        '--skip-external',
        action='store_true',
        help='跳过外部链接检查'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='外部链接超时时间（秒）(默认: 30)'
    )
    
    parser.add_argument(
        '--max-concurrent',
        type=int,
        default=10,
        help='最大并发请求数 (默认: 10)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./cross-ref-reports',
        help='输出目录 (默认: ./cross-ref-reports)'
    )
    
    args = parser.parse_args()
    
    # 解析变更文件
    changed_files = None
    if args.incremental:
        changed_files = set(args.incremental)
        logger.info(f"增量模式：只检查 {len(changed_files)} 个文件")
        
    # 创建验证器
    validator = CrossRefValidator(
        root_dir=Path(args.root_dir),
        timeout=args.timeout,
        max_concurrent=args.max_concurrent,
        skip_external=args.skip_external
    )
    
    # 运行验证
    result = asyncio.run(validator.run(
        file_pattern=args.file_pattern,
        changed_files=changed_files
    ))
    
    # 创建输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成报告
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    json_path = output_dir / f"cross-ref-report-{timestamp}.json"
    validator.generate_json_report(result, json_path)
    
    md_path = output_dir / f"cross-ref-summary-{timestamp}.md"
    validator.generate_markdown_summary(result, md_path)
    
    # 输出摘要
    print(f"\n{'='*60}")
    print("交叉引用验证完成")
    print(f"{'='*60}")
    print(f"扫描文件数: {result.total_files}")
    print(f"总链接数: {result.total_links}")
    print(f"✓ 有效: {result.valid_links}")
    print(f"✗ 无效: {result.invalid_links}")
    print(f"⚠ 警告: {result.warning_links}")
    print(f"✕ 错误: {result.error_links}")
    print(f"○ 跳过: {result.skipped_links}")
    print(f"耗时: {result.duration_seconds:.2f} 秒")
    print(f"{'='*60}")
    print(f"报告已保存至: {output_dir}")
    
    # 返回退出码
    return 1 if result.invalid_links > 0 or result.error_links > 0 else 0


if __name__ == '__main__':
    exit(main())
