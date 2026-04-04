#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
链接检查器 - 递归扫描Markdown文件并检查链接有效性

功能:
- 递归扫描所有Markdown文件
- 检查外部链接可访问性 (HTTP/HTTPS)
- 检查内部链接有效性 (锚点、相对路径)
- 生成详细报告

作者: AnalysisDataFlow 项目
版本: 1.0.0
"""

import asyncio
import argparse
import json
import logging
import re
import sys
import time
import yaml
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from urllib.parse import urlparse, urljoin, unquote
from collections import defaultdict

import aiohttp
from aiohttp import ClientSession, ClientTimeout, ClientError

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('link-checker.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class LinkCheckResult:
    """链接检查结果数据类"""
    url: str
    source_file: str
    line_number: int
    link_type: str  # 'external', 'internal', 'anchor', 'email', 'file'
    status_code: Optional[int] = None
    is_valid: bool = False
    error_message: Optional[str] = None
    response_time: float = 0.0
    redirect_url: Optional[str] = None
    checked_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CheckSummary:
    """检查汇总数据类"""
    total_files: int = 0
    total_links: int = 0
    valid_links: int = 0
    broken_links: int = 0
    warning_links: int = 0
    skipped_links: int = 0
    check_duration: float = 0.0
    started_at: str = ""
    completed_at: str = ""


class LinkExtractor:
    """Markdown链接提取器"""
    
    # Markdown链接正则: [text](url) 或 [text](url "title")
    MARKDOWN_LINK_PATTERN = re.compile(
        r'\[([^\]]+)\]\(([^\s\)]+)(?:\s+"[^"]*")?\)'
    )
    
    # HTML链接正则: <a href="url">
    HTML_LINK_PATTERN = re.compile(
        r'<a[^>]+href=["\']([^"\'>]+)["\'][^>]*>',
        re.IGNORECASE
    )
    
    # 引用链接正则: [text][ref] 或 [text]
    REFERENCE_LINK_PATTERN = re.compile(
        r'\[([^\]]+)\](?:\[([^\]]*)\])?'
    )
    
    # 引用定义正则: [ref]: url
    REFERENCE_DEF_PATTERN = re.compile(
        r'^\[([^\]]+)\]:\s*(\S+)'
    )
    
    # 自动链接: <url>
    AUTO_LINK_PATTERN = re.compile(
        r'<([a-zA-Z][a-zA-Z0-9+.-]*:[^>]+)>'
    )

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.file_cache: Dict[Path, str] = {}

    def extract_links(self, file_path: Path) -> List[Tuple[str, int]]:
        """从Markdown文件中提取所有链接"""
        links = []
        
        try:
            content = self._read_file(file_path)
            lines = content.split('\n')
            
            # 收集引用定义
            references = {}
            for line_num, line in enumerate(lines, 1):
                ref_match = self.REFERENCE_DEF_PATTERN.match(line)
                if ref_match:
                    ref_name = ref_match.group(1)
                    ref_url = ref_match.group(2)
                    references[ref_name] = (ref_url, line_num)
            
            for line_num, line in enumerate(lines, 1):
                # 跳过代码块
                if line.strip().startswith('```'):
                    continue
                    
                # 提取Markdown链接
                for match in self.MARKDOWN_LINK_PATTERN.finditer(line):
                    url = match.group(2)
                    links.append((url, line_num))
                
                # 提取HTML链接
                for match in self.HTML_LINK_PATTERN.finditer(line):
                    url = match.group(1)
                    links.append((url, line_num))
                
                # 提取自动链接
                for match in self.AUTO_LINK_PATTERN.finditer(line):
                    url = match.group(1)
                    links.append((url, line_num))
                
                # 处理引用链接
                for match in self.REFERENCE_LINK_PATTERN.finditer(line):
                    ref_name = match.group(2) or match.group(1)
                    if ref_name in references:
                        url, _ = references[ref_name]
                        links.append((url, line_num))
                        
        except Exception as e:
            logger.error(f"提取链接时出错 {file_path}: {e}")
            
        return links

    def _read_file(self, file_path: Path) -> str:
        """读取文件内容（带缓存）"""
        if file_path not in self.file_cache:
            try:
                self.file_cache[file_path] = file_path.read_text(encoding='utf-8')
            except Exception as e:
                logger.error(f"读取文件失败 {file_path}: {e}")
                return ""
        return self.file_cache[file_path]


class LinkChecker:
    """链接检查器核心类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.extractor: Optional[LinkExtractor] = None
        self.session: Optional[ClientSession] = None
        self.results: List[LinkCheckResult] = []
        self.visited_urls: Set[str] = set()
        self.file_exists_cache: Dict[Path, bool] = {}
        self.anchor_cache: Dict[Path, Set[str]] = {}
        
        # 统计信息
        self.summary = CheckSummary()
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        timeout_config = self.config.get('timeout', {})
        timeout = ClientTimeout(
            total=timeout_config.get('total', 30),
            connect=timeout_config.get('connect', 10)
        )
        
        headers = {
            'User-Agent': self.config.get('user_agent', 
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
            ),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        
        connector = aiohttp.TCPConnector(
            limit=self.config.get('max_concurrent', 50),
            limit_per_host=self.config.get('max_per_host', 10),
            enable_cleanup_closed=True,
            force_close=True,
        )
        
        self.session = ClientSession(
            timeout=timeout,
            headers=headers,
            connector=connector
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()

    def _classify_link(self, url: str) -> str:
        """分类链接类型"""
        if url.startswith(('http://', 'https://')):
            return 'external'
        elif url.startswith('mailto:'):
            return 'email'
        elif url.startswith('#'):
            return 'anchor'
        elif url.startswith(('file://', '/', './', '../')):
            return 'file'
        else:
            return 'internal'

    def _is_excluded(self, url: str) -> bool:
        """检查URL是否在排除列表中"""
        exclude_patterns = self.config.get('exclude', [])
        for pattern in exclude_patterns:
            if re.search(pattern, url):
                return True
        return False

    async def check_external_link(self, url: str) -> LinkCheckResult:
        """检查外部链接"""
        result = LinkCheckResult(
            url=url,
            source_file="",
            line_number=0,
            link_type='external'
        )
        
        if self._is_excluded(url):
            result.error_message = "URL在排除列表中"
            result.is_valid = True  # 跳过视为有效
            return result
        
        retry_config = self.config.get('retry', {})
        max_retries = retry_config.get('max_retries', 3)
        retry_delay = retry_config.get('delay', 1)
        
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                
                async with self.session.get(
                    url, 
                    allow_redirects=True,
                    ssl=False  # 某些网站SSL证书可能有问题
                ) as response:
                    result.response_time = time.time() - start_time
                    result.status_code = response.status
                    
                    if response.history:
                        result.redirect_url = str(response.history[-1].url)
                    
                    # 2xx 状态码视为有效
                    if 200 <= response.status < 300:
                        result.is_valid = True
                        return result
                    
                    # 3xx 状态码视为警告
                    elif 300 <= response.status < 400:
                        result.is_valid = True
                        result.error_message = f"重定向警告: HTTP {response.status}"
                        return result
                    
                    # 4xx/5xx 状态码
                    else:
                        result.error_message = f"HTTP错误: {response.status}"
                        
            except asyncio.TimeoutError:
                result.error_message = f"请求超时 (尝试 {attempt + 1}/{max_retries})"
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (attempt + 1))
                    continue
                    
            except ClientError as e:
                result.error_message = f"客户端错误: {str(e)}"
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (attempt + 1))
                    continue
                    
            except Exception as e:
                result.error_message = f"未知错误: {str(e)}"
                break
        
        return result

    def check_internal_link(self, url: str, source_file: Path) -> LinkCheckResult:
        """检查内部链接"""
        result = LinkCheckResult(
            url=url,
            source_file=str(source_file),
            line_number=0,
            link_type='internal'
        )
        
        try:
            # 解析URL
            parsed = urlparse(url)
            
            # 处理锚点链接
            if '#' in url:
                base_url, anchor = url.split('#', 1)
            else:
                base_url, anchor = url, None
            
            # 解析目标文件路径
            if base_url.startswith('/'):
                # 绝对路径
                target_path = self.extractor.base_path / base_url.lstrip('/')
            elif base_url.startswith(('./', '../')) or not base_url.startswith(('http', 'mailto', 'file')):
                # 相对路径
                target_path = source_file.parent / base_url
                target_path = target_path.resolve()
            else:
                result.error_message = f"无法解析的内部链接: {url}"
                return result
            
            # 检查文件是否存在
            if target_path in self.file_exists_cache:
                file_exists = self.file_exists_cache[target_path]
            else:
                file_exists = target_path.exists()
                self.file_exists_cache[target_path] = file_exists
            
            if not file_exists:
                result.error_message = f"文件不存在: {target_path.relative_to(self.extractor.base_path)}"
                return result
            
            # 如果有锚点，检查锚点是否存在
            if anchor:
                if target_path not in self.anchor_cache:
                    self.anchor_cache[target_path] = self._extract_anchors(target_path)
                
                anchors = self.anchor_cache[target_path]
                decoded_anchor = unquote(anchor).lower().replace(' ', '-')
                
                if decoded_anchor not in anchors:
                    result.error_message = f"锚点不存在: #{anchor}"
                    result.is_valid = False
                    return result
            
            result.is_valid = True
            
        except Exception as e:
            result.error_message = f"检查内部链接时出错: {str(e)}"
        
        return result

    def _extract_anchors(self, file_path: Path) -> Set[str]:
        """从Markdown文件中提取所有锚点"""
        anchors = set()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 提取标题锚点
            header_pattern = re.compile(r'^#{1,6}\s+(.+)$', re.MULTILINE)
            for match in header_pattern.finditer(content):
                title = match.group(1).strip()
                # GitHub风格的锚点转换
                anchor = title.lower()
                anchor = re.sub(r'[^\w\s-]', '', anchor)
                anchor = re.sub(r'\s+', '-', anchor)
                anchors.add(anchor)
            
            # 提取HTML锚点
            html_anchor_pattern = re.compile(r'<a[^>]+name=["\']([^"\'>]+)["\'][^>]*>', re.IGNORECASE)
            for match in html_anchor_pattern.finditer(content):
                anchors.add(match.group(1).lower())
            
            # 提取id锚点
            id_pattern = re.compile(r'<[^>]+id=["\']([^"\'>]+)["\'][^>]*>', re.IGNORECASE)
            for match in id_pattern.finditer(content):
                anchors.add(match.group(1).lower())
                
        except Exception as e:
            logger.warning(f"提取锚点时出错 {file_path}: {e}")
        
        return anchors

    def check_file_link(self, url: str, source_file: Path) -> LinkCheckResult:
        """检查文件链接"""
        result = LinkCheckResult(
            url=url,
            source_file=str(source_file),
            line_number=0,
            link_type='file'
        )
        
        try:
            if url.startswith('file://'):
                file_path = Path(unquote(url[7:]))
            elif url.startswith('/'):
                file_path = self.extractor.base_path / url.lstrip('/')
            else:
                file_path = source_file.parent / url
                file_path = file_path.resolve()
            
            if file_path.exists():
                result.is_valid = True
            else:
                result.error_message = f"文件不存在: {file_path}"
                
        except Exception as e:
            result.error_message = f"检查文件链接时出错: {str(e)}"
        
        return result

    def check_email_link(self, url: str) -> LinkCheckResult:
        """检查邮件链接"""
        result = LinkCheckResult(
            url=url,
            source_file="",
            line_number=0,
            link_type='email'
        )
        
        # 简单验证邮件格式
        email_pattern = re.compile(r'^mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
        if email_pattern.match(url):
            result.is_valid = True
        else:
            result.error_message = "邮件格式无效"
        
        return result

    async def process_file(self, file_path: Path) -> List[LinkCheckResult]:
        """处理单个文件中的所有链接"""
        results = []
        links = self.extractor.extract_links(file_path)
        
        logger.info(f"检查文件: {file_path.relative_to(self.extractor.base_path)} ({len(links)} 个链接)")
        
        external_links = []
        for url, line_num in links:
            link_type = self._classify_link(url)
            
            if link_type == 'external':
                external_links.append((url, line_num))
            else:
                # 同步检查内部链接
                if link_type == 'internal':
                    result = self.check_internal_link(url, file_path)
                elif link_type == 'file':
                    result = self.check_file_link(url, file_path)
                elif link_type == 'email':
                    result = self.check_email_link(url)
                elif link_type == 'anchor':
                    result = self.check_internal_link(url, file_path)
                else:
                    continue
                
                result.source_file = str(file_path)
                result.line_number = line_num
                results.append(result)
        
        # 异步批量检查外部链接
        if external_links:
            semaphore = asyncio.Semaphore(self.config.get('max_concurrent', 50))
            
            async def check_with_limit(url, line_num):
                async with semaphore:
                    result = await self.check_external_link(url)
                    result.source_file = str(file_path)
                    result.line_number = line_num
                    return result
            
            external_results = await asyncio.gather(*[
                check_with_limit(url, line_num) 
                for url, line_num in external_links
            ])
            results.extend(external_results)
        
        return results

    async def run(self, base_path: Path, include_patterns: List[str] = None) -> Tuple[List[LinkCheckResult], CheckSummary]:
        """运行链接检查"""
        self.summary.started_at = datetime.now().isoformat()
        start_time = time.time()
        
        self.extractor = LinkExtractor(base_path)
        
        # 查找所有Markdown文件
        md_files = []
        for pattern in (include_patterns or ['**/*.md']):
            md_files.extend(base_path.glob(pattern))
        
        # 去重并保持顺序
        seen = set()
        md_files = [f for f in md_files if not (f in seen or seen.add(f))]
        
        self.summary.total_files = len(md_files)
        logger.info(f"找到 {len(md_files)} 个Markdown文件")
        
        # 并发处理所有文件
        all_results = []
        batch_size = self.config.get('file_batch_size', 10)
        
        for i in range(0, len(md_files), batch_size):
            batch = md_files[i:i + batch_size]
            batch_results = await asyncio.gather(*[
                self.process_file(f) for f in batch
            ])
            for results in batch_results:
                all_results.extend(results)
            
            logger.info(f"进度: {min(i + batch_size, len(md_files))}/{len(md_files)} 文件")
        
        self.results = all_results
        self.summary.total_links = len(all_results)
        
        # 统计结果
        for result in all_results:
            if result.is_valid and not result.error_message:
                self.summary.valid_links += 1
            elif result.is_valid and result.error_message:
                self.summary.warning_links += 1
            elif not result.is_valid:
                self.summary.broken_links += 1
        
        self.summary.check_duration = time.time() - start_time
        self.summary.completed_at = datetime.now().isoformat()
        
        logger.info(f"检查完成: {self.summary.total_links} 个链接, "
                   f"{self.summary.valid_links} 有效, "
                   f"{self.summary.warning_links} 警告, "
                   f"{self.summary.broken_links} 失效")
        
        return all_results, self.summary

    def save_results(self, output_path: Path):
        """保存检查结果到JSON文件"""
        data = {
            'summary': asdict(self.summary),
            'results': [asdict(r) for r in self.results]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"结果已保存到: {output_path}")


def load_config(config_path: Path) -> Dict[str, Any]:
    """加载配置文件"""
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    return {}


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Markdown链接检查器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --path ./docs
  %(prog)s --path ./docs --config config.yaml
  %(prog)s --path ./docs --output results.json
        """
    )
    
    parser.add_argument('--path', '-p', type=str, default='.',
                       help='要扫描的基础目录路径 (默认: 当前目录)')
    parser.add_argument('--config', '-c', type=str, default='config.yaml',
                       help='配置文件路径 (默认: config.yaml)')
    parser.add_argument('--output', '-o', type=str, default='link-check-results.json',
                       help='输出JSON文件路径 (默认: link-check-results.json)')
    parser.add_argument('--patterns', type=str, nargs='+', default=['**/*.md'],
                       help='包含的文件模式 (默认: **/*.md)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='启用详细日志输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    base_path = Path(args.path).resolve()
    config_path = Path(args.config)
    
    # 如果配置文件是相对路径，在脚本目录中查找
    if not config_path.is_absolute():
        script_dir = Path(__file__).parent
        config_path = script_dir / config_path
    
    config = load_config(config_path)
    
    logger.info(f"开始链接检查...")
    logger.info(f"基础路径: {base_path}")
    logger.info(f"配置文件: {config_path}")
    
    async with LinkChecker(config) as checker:
        results, summary = await checker.run(base_path, args.patterns)
        checker.save_results(Path(args.output))
    
    # 如果有失效链接，返回非零退出码
    if summary.broken_links > 0:
        logger.warning(f"发现 {summary.broken_links} 个失效链接!")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
