#!/usr/bin/env python3
"""
AnalysisDataFlow 统一质量门禁脚本
=================================
功能: 整合所有质量检查，输出统一报告，设置失败阈值

检查项:
- 内部链接有效性
- 锚点存在性
- 交叉引用正确性
- 外部链接健康度（可选）
- 定理编号唯一性
- Markdown格式基础检查

作者: AnalysisDataFlow CI/CD Team
版本: 1.0.0
"""

import re
import sys
import json
import argparse
import asyncio
import aiohttp
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set


# =============================================================================
# 配置常量
# =============================================================================

EXCLUDE_PATTERNS = [
    r'localhost',
    r'127\.0\.0\.1',
    r'example\.com',
    r'your-domain\.com',
    r'\.local',
    r'\.internal',
    r'github\.com/[^/]+/[^/]+/edit/',
    r'github\.com/[^/]+/[^/]+/issues/new',
    r'docs\.google\.com',
    r'drive\.google\.com',
    r'linkedin\.com',
]

THEOREM_PATTERN = re.compile(r'(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d{2})-(\d{2,3})')

DEFAULT_TIMEOUT = 10
MAX_RETRIES = 2
CONCURRENT_LIMIT = 20


# =============================================================================
# 工具函数
# =============================================================================

def find_all_markdown_files(root_path: Path) -> List[Path]:
    """获取所有Markdown文件"""
    exclude_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.scripts', 'reports'}
    md_files = []
    for f in root_path.rglob('*.md'):
        if not any(part in exclude_dirs for part in f.parts):
            md_files.append(f)
    return md_files


def extract_links(content: str) -> List[Tuple[str, str, int]]:
    """提取所有链接 [text](url)"""
    links = []
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    for match in re.finditer(pattern, content):
        text = match.group(1)
        url = match.group(2).split(' ')[0]  # 移除标题
        links.append((text, url, match.start()))
    return links


def classify_link(url: str) -> str:
    """分类链接类型"""
    if url.startswith('http://') or url.startswith('https://'):
        return 'external'
    if url.startswith('#'):
        return 'anchor'
    if url.startswith('mailto:'):
        return 'email'
    return 'internal'


def should_skip_url(url: str) -> bool:
    """检查是否应该跳过此URL"""
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            return True
    return False


def validate_internal_link(url: str, source_file: Path, all_files: Set[Path]) -> Tuple[bool, Optional[str]]:
    """验证内部链接"""
    source_dir = source_file.parent
    
    # 移除锚点
    parts = url.split('#')
    url_without_anchor = parts[0]
    anchor = parts[1] if len(parts) > 1 else None
    
    if not url_without_anchor:
        return True, None
    
    # 解析路径
    if url_without_anchor.startswith('/'):
        target = Path('.') / url_without_anchor.lstrip('/')
    else:
        target = source_dir / url_without_anchor
    
    target = target.resolve()
    
    # 检查文件是否存在
    if not target.exists():
        target_with_md = Path(str(target) + '.md')
        if target_with_md.exists():
            return True, None
        
        target_index = target / 'index.md'
        if target_index.exists():
            return True, None
        
        return False, f"文件不存在: {target}"
    
    return True, None


def validate_anchor(content: str, anchor: str) -> bool:
    """验证锚点是否存在"""
    anchor = anchor.lower().replace(' ', '-')
    
    # 检查标题锚点
    header_pattern = r'^#{1,6}\s+(.+)$'
    for match in re.finditer(header_pattern, content, re.MULTILINE):
        header_text = match.group(1).strip()
        header_anchor = re.sub(r'[^\w\s-]', '', header_text).lower().replace(' ', '-')
        if header_anchor == anchor:
            return True
    
    # 检查自定义锚点
    anchor_pattern = r'<a\s+name=["\']([^"\']+)["\']'
    for match in re.finditer(anchor_pattern, content):
        if match.group(1) == anchor:
            return True
    
    return False


# =============================================================================
# 检查器类
# =============================================================================

class QualityChecker:
    """统一质量检查器"""
    
    def __init__(self, root_path: Path, fail_threshold: int = 5):
        self.root_path = root_path
        self.fail_threshold = fail_threshold
        self.results = {
            'checks': [],
            'summary': {
                'total_checks': 0,
                'passed': 0,
                'failed': 0,
                'warnings': 0,
                'broken_links': 0
            }
        }
        self.errors = []
        self.warnings = []
    
    def add_check(self, name: str, passed: bool, details: List[str] = None, error_count: int = 0):
        """添加检查结果"""
        self.results['checks'].append({
            'name': name,
            'passed': passed,
            'details': details or [],
            'error_count': error_count,
            'timestamp': datetime.now().isoformat()
        })
        self.results['summary']['total_checks'] += 1
        if passed:
            self.results['summary']['passed'] += 1
        else:
            self.results['summary']['failed'] += 1
    
    def check_internal_links(self, md_files: List[Path]) -> bool:
        """检查内部链接"""
        print("\n📄 检查内部链接...")
        all_files_set = set(md_files)
        broken_links = []
        total_links = 0
        
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                self.warnings.append(f"无法读取 {md_file}: {e}")
                continue
            
            links = extract_links(content)
            
            for text, url, _ in links:
                if classify_link(url) == 'internal':
                    total_links += 1
                    is_valid, error = validate_internal_link(url, md_file, all_files_set)
                    if not is_valid:
                        broken_links.append({
                            'source': str(md_file.relative_to(self.root_path)),
                            'text': text,
                            'url': url,
                            'error': error
                        })
        
        passed = len(broken_links) <= self.fail_threshold
        
        print(f"   总链接: {total_links}")
        print(f"   失效: {len(broken_links)}")
        
        details = [f"发现 {len(broken_links)} 个失效内部链接（阈值: {self.fail_threshold}）"]
        if broken_links:
            by_source = defaultdict(list)
            for link in broken_links:
                by_source[link['source']].append(link)
            
            for source, links in list(sorted(by_source.items()))[:5]:
                details.append(f"  📄 {source}")
                for link in links[:3]:
                    details.append(f"    - [{link['text']}]({link['url']}): {link['error']}")
        
        self.results['summary']['broken_links'] += len(broken_links)
        self.add_check('内部链接检查', passed, details, len(broken_links))
        
        if broken_links:
            self.errors.extend([f"{l['source']}: [{l['text']}]({l['url']})" for l in broken_links[:10]])
        
        return passed
    
    def check_anchors(self, md_files: List[Path]) -> bool:
        """检查锚点"""
        print("\n🔗 检查锚点...")
        broken_anchors = []
        total_anchors = 0
        
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue
            
            links = extract_links(content)
            
            for text, url, _ in links:
                if classify_link(url) == 'anchor' or '#' in url:
                    total_anchors += 1
                    anchor = url.split('#')[1] if '#' in url else url[1:]
                    if not validate_anchor(content, anchor):
                        broken_anchors.append({
                            'source': str(md_file.relative_to(self.root_path)),
                            'text': text,
                            'anchor': anchor
                        })
        
        passed = len(broken_anchors) <= self.fail_threshold
        
        print(f"   总锚点: {total_anchors}")
        print(f"   失效: {len(broken_anchors)}")
        
        details = [f"发现 {len(broken_anchors)} 个无效锚点（阈值: {self.fail_threshold}）"]
        self.add_check('锚点检查', passed, details, len(broken_anchors))
        
        return passed
    
    def check_cross_references(self, md_files: List[Path]) -> bool:
        """检查交叉引用"""
        print("\n📚 检查交叉引用...")
        all_files_set = set(str(f) for f in md_files)
        broken_refs = []
        
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue
            
            # 查找文档引用如 [文档](path/to/doc.md)
            ref_pattern = r'\[([^\]]+)\]\(([^)]+\.md[^)]*)\)'
            for match in re.finditer(ref_pattern, content):
                text = match.group(1)
                ref_path = match.group(2).split('#')[0]  # 移除锚点
                
                source_dir = md_file.parent
                if ref_path.startswith('/'):
                    target = self.root_path / ref_path.lstrip('/')
                else:
                    target = source_dir / ref_path
                
                target = target.resolve()
                if str(target) not in all_files_set and not target.exists():
                    broken_refs.append({
                        'source': str(md_file.relative_to(self.root_path)),
                        'text': text,
                        'ref': ref_path
                    })
        
        passed = len(broken_refs) <= self.fail_threshold
        
        print(f"   失效引用: {len(broken_refs)}")
        
        details = [f"发现 {len(broken_refs)} 个无效交叉引用（阈值: {self.fail_threshold}）"]
        self.add_check('交叉引用检查', passed, details, len(broken_refs))
        
        return passed
    
    def check_theorem_numbers(self, md_files: List[Path]) -> bool:
        """检查定理编号唯一性"""
        print("\n📐 检查定理编号...")
        all_theorems = defaultdict(list)
        
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue
            
            for match in THEOREM_PATTERN.finditer(content):
                theorem_id = f"{match.group(1)}-{match.group(2)}-{match.group(3)}-{match.group(4)}"
                all_theorems[theorem_id].append(str(md_file.relative_to(self.root_path)))
        
        duplicates = {k: v for k, v in all_theorems.items() if len(v) > 1}
        passed = len(duplicates) == 0
        
        print(f"   唯一定理: {len(all_theorems)}")
        print(f"   重复: {len(duplicates)}")
        
        details = [f"发现 {len(duplicates)} 个重复定理编号"]
        if duplicates:
            for tid, files in list(duplicates.items())[:5]:
                details.append(f"  {tid}: {', '.join(files)}")
        
        self.add_check('定理编号检查', passed, details, len(duplicates))
        
        return passed
    
    async def check_external_links(self, md_files: List[Path]) -> bool:
        """检查外部链接（异步）"""
        print("\n🌐 检查外部链接...")
        
        external_links = []
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue
            
            links = extract_links(content)
            for text, url, _ in links:
                if classify_link(url) == 'external' and not should_skip_url(url):
                    external_links.append({
                        'source': str(md_file.relative_to(self.root_path)),
                        'text': text,
                        'url': url
                    })
        
        if not external_links:
            print("   没有外部链接需要检查")
            self.add_check('外部链接检查', True, ['没有外部链接'], 0)
            return True
        
        # 去重
        unique_urls = list(set(link['url'] for link in external_links))
        print(f"   唯一URL: {len(unique_urls)}")
        
        # 并发检查
        broken = []
        semaphore = asyncio.Semaphore(CONCURRENT_LIMIT)
        
        async with aiohttp.ClientSession(
            headers={'User-Agent': 'AnalysisDataFlow-QualityChecker/1.0'}
        ) as session:
            async def check_single(url):
                async with semaphore:
                    try:
                        async with session.head(
                            url,
                            timeout=aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT),
                            allow_redirects=True,
                            ssl=False
                        ) as response:
                            if response.status >= 400:
                                return url, response.status
                            return url, None
                    except Exception as e:
                        return url, str(e)
            
            tasks = [check_single(url) for url in unique_urls]
            results = await asyncio.gather(*tasks)
        
        for url, error in results:
            if error is not None:
                broken.append({'url': url, 'error': error})
        
        passed = len(broken) <= self.fail_threshold
        
        print(f"   失效: {len(broken)}")
        
        details = [f"发现 {len(broken)} 个失效外部链接（阈值: {self.fail_threshold}）"]
        self.add_check('外部链接检查', passed, details, len(broken))
        
        return passed
    
    def generate_report(self, output_path: Path, json_path: Optional[Path] = None):
        """生成报告"""
        lines = [
            "# 🚪 质量门禁检查报告",
            "",
            f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"> **检查路径**: {self.root_path}",
            "",
            "## 📊 检查摘要",
            "",
            f"- **总检查项**: {self.results['summary']['total_checks']}",
            f"- **通过**: {self.results['summary']['passed']} ✅",
            f"- **失败**: {self.results['summary']['failed']} ❌",
            f"- **失效链接**: {self.results['summary']['broken_links']}",
            "",
        ]
        
        # 添加详细结果
        lines.extend(["## 📋 详细结果", ""])
        for check in self.results['checks']:
            status = "✅ 通过" if check['passed'] else "❌ 失败"
            lines.append(f"### {check['name']} - {status}")
            for detail in check['details']:
                lines.append(detail)
            lines.append("")
        
        # 错误汇总
        if self.errors:
            lines.extend([
                "## ❌ 错误汇总",
                "",
                "```",
            ])
            for error in self.errors[:50]:
                lines.append(error)
            if len(self.errors) > 50:
                lines.append(f"... 还有 {len(self.errors) - 50} 个错误")
            lines.extend(["```", ""])
        
        # 写入报告
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        # 写入JSON
        if json_path:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)


# =============================================================================
# 主程序
# =============================================================================

async def main():
    parser = argparse.ArgumentParser(description='AnalysisDataFlow 统一质量门禁')
    parser.add_argument('--path', '-p', default='.', help='检查路径')
    parser.add_argument('--check-internal', action='store_true', help='检查内部链接')
    parser.add_argument('--check-external', action='store_true', help='检查外部链接')
    parser.add_argument('--check-anchors', action='store_true', help='检查锚点')
    parser.add_argument('--check-refs', action='store_true', help='检查交叉引用')
    parser.add_argument('--check-theorems', action='store_true', help='检查定理编号')
    parser.add_argument('--fail-threshold', type=int, default=5, help='失败阈值')
    parser.add_argument('--output', '-o', default='reports/quality-gates-report.md', help='报告输出路径')
    parser.add_argument('--json', '-j', help='JSON输出路径')
    parser.add_argument('--all', action='store_true', help='执行所有检查')
    
    args = parser.parse_args()
    
    root_path = Path(args.path).resolve()
    
    # 如果没有指定任何检查，默认执行内部链接和锚点检查
    if not any([args.check_internal, args.check_external, args.check_anchors, 
                args.check_refs, args.check_theorems, args.all]):
        args.check_internal = True
        args.check_anchors = True
    
    if args.all:
        args.check_internal = True
        args.check_external = True
        args.check_anchors = True
        args.check_refs = True
        args.check_theorems = True
    
    print("=" * 70)
    print("🚪 AnalysisDataFlow 统一质量门禁")
    print("=" * 70)
    print(f"检查路径: {root_path}")
    print(f"失败阈值: {args.fail_threshold}")
    
    # 获取所有Markdown文件
    print("\n📁 扫描Markdown文件...")
    md_files = find_all_markdown_files(root_path)
    print(f"找到 {len(md_files)} 个Markdown文件")
    
    # 创建检查器
    checker = QualityChecker(root_path, args.fail_threshold)
    
    # 执行检查
    all_passed = True
    
    if args.check_internal:
        if not checker.check_internal_links(md_files):
            all_passed = False
    
    if args.check_anchors:
        if not checker.check_anchors(md_files):
            all_passed = False
    
    if args.check_refs:
        if not checker.check_cross_references(md_files):
            all_passed = False
    
    if args.check_theorems:
        if not checker.check_theorem_numbers(md_files):
            all_passed = False
    
    if args.check_external:
        if not await checker.check_external_links(md_files):
            all_passed = False
    
    # 生成报告
    output_path = Path(args.output)
    json_path = Path(args.json) if args.json else None
    checker.generate_report(output_path, json_path)
    
    print(f"\n📝 报告已生成: {output_path}")
    
    # 输出摘要
    print("\n" + "=" * 70)
    print("📊 检查摘要")
    print("=" * 70)
    print(f"总检查项: {checker.results['summary']['total_checks']}")
    print(f"通过: {checker.results['summary']['passed']} ✅")
    print(f"失败: {checker.results['summary']['failed']} ❌")
    print(f"失效链接: {checker.results['summary']['broken_links']}")
    print("=" * 70)
    
    if all_passed:
        print("\n✅ 所有检查通过！")
        sys.exit(0)
    else:
        print("\n❌ 部分检查未通过")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
