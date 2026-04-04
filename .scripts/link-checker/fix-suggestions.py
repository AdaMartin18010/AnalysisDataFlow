#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复建议工具 - 自动分析失效链接并提供修复建议

功能:
- Wayback Machine 查询
- 替代链接建议
- 自动生成修复脚本
- 批量修复支持

作者: AnalysisDataFlow 项目
版本: 1.0.0
"""

import argparse
import asyncio
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urlparse, quote

import aiohttp


@dataclass
class FixSuggestion:
    """修复建议数据类"""
    original_url: str
    source_file: str
    line_number: int
    suggestion_type: str  # 'wayback', 'redirect', 'manual', 'remove'
    suggested_url: Optional[str] = None
    confidence: float = 0.0  # 0-1
    description: str = ""
    auto_fixable: bool = False


class WaybackMachineClient:
    """Wayback Machine API 客户端"""
    
    BASE_URL = "https://archive.org/wayback/available"
    CDX_URL = "https://web.archive.org/cdx/search/cdx"
    
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.cache: Dict[str, Optional[str]] = {}
    
    async def get_snapshot(self, url: str, timestamp: Optional[str] = None) -> Optional[str]:
        """获取最近的网页快照"""
        if url in self.cache:
            return self.cache[url]
        
        try:
            params = {'url': url}
            if timestamp:
                params['timestamp'] = timestamp
            
            async with self.session.get(self.BASE_URL, params=params, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    archived = data.get('archived_snapshots', {}).get('closest', {})
                    
                    if archived and archived.get('available'):
                        snapshot_url = archived.get('url')
                        self.cache[url] = snapshot_url
                        return snapshot_url
                        
        except Exception as e:
            print(f"Wayback查询失败 {url}: {e}")
        
        self.cache[url] = None
        return None
    
    async def get_all_snapshots(self, url: str, limit: int = 5) -> List[Dict]:
        """获取多个历史快照"""
        snapshots = []
        
        try:
            params = {
                'url': url,
                'output': 'json',
                'limit': limit
            }
            
            async with self.session.get(self.CDX_URL, params=params, timeout=15) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if len(data) > 1:  # 第一行是表头
                        headers = data[0]
                        for row in data[1:]:
                            snapshot = dict(zip(headers, row))
                            snapshots.append({
                                'timestamp': snapshot.get('timestamp'),
                                'original': snapshot.get('original'),
                                'mimetype': snapshot.get('mimetype'),
                                'statuscode': snapshot.get('statuscode'),
                                'digest': snapshot.get('digest'),
                                'url': f"https://web.archive.org/web/{snapshot.get('timestamp')}/{snapshot.get('original')}"
                            })
                            
        except Exception as e:
            print(f"CDX查询失败 {url}: {e}")
        
        return snapshots


class RedirectDetector:
    """重定向检测器"""
    
    # 常见域名变更映射
    DOMAIN_MAPPINGS = {
        'http://': 'https://',
        'www.github.com': 'github.com',
        'www.gitlab.com': 'gitlab.com',
        'docs.python.org/2/': 'docs.python.org/3/',
        'stackoverflow.com': 'stackoverflow.com',
    }
    
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
    
    async def check_redirect(self, url: str) -> Optional[str]:
        """检查URL是否永久重定向到新地址"""
        try:
            async with self.session.head(url, allow_redirects=False, timeout=10) as resp:
                if resp.status in (301, 308):  # 永久重定向
                    location = resp.headers.get('Location')
                    return location
                    
                # 尝试GET请求
                if resp.status in (302, 307):
                    async with self.session.get(url, allow_redirects=True, timeout=10) as get_resp:
                        final_url = str(get_resp.url)
                        if final_url != url:
                            return final_url
                            
        except Exception:
            pass
        
        return None
    
    def suggest_domain_fix(self, url: str) -> Optional[str]:
        """基于常见模式建议域名修复"""
        # http -> https
        if url.startswith('http://') and not url.startswith('http://localhost'):
            https_url = 'https://' + url[7:]
            return https_url
        
        # 移除 www 前缀 (某些网站)
        if '://www.' in url:
            for www_domain, non_www in self.DOMAIN_MAPPINGS.items():
                if www_domain in url and www_domain != non_www:
                    return url.replace(www_domain, non_www)
        
        return None


class AlternativeFinder:
    """替代链接查找器"""
    
    # 文档替代源
    DOC_ALTERNATIVES = {
        'docs.oracle.com/javase/7': 'docs.oracle.com/javase/8',
        'docs.python.org/2': 'docs.python.org/3',
        'flink.apache.org/docs/1.': 'flink.apache.org/docs/stable',
        'spark.apache.org/docs/1.': 'spark.apache.org/docs/latest',
        'hadoop.apache.org/docs/r1': 'hadoop.apache.org/docs/stable',
    }
    
    # 学术论文替代源
    PAPER_ALTERNATIVES = {
        'dl.acm.org': ['arxiv.org', 'sci-hub.se'],
        'ieeexplore.ieee.org': ['arxiv.org'],
        'springer.com': ['sci-hub.se'],
    }
    
    def find_doc_alternative(self, url: str) -> Optional[str]:
        """查找文档的替代链接"""
        for old, new in self.DOC_ALTERNATIVES.items():
            if old in url:
                return url.replace(old, new)
        return None
    
    def find_paper_alternative(self, url: str) -> List[str]:
        """查找学术论文的替代链接"""
        alternatives = []
        
        # 提取DOI或论文标题
        doi_match = re.search(r'10\.\d{4,}/[^\s"<>]+', url)
        if doi_match:
            doi = doi_match.group(0)
            alternatives.append(f"https://doi.org/{doi}")
            alternatives.append(f"https://sci-hub.se/{doi}")
        
        # 检查域名替代
        for domain, alts in self.PAPER_ALTERNATIVES.items():
            if domain in url:
                for alt in alts:
                    alternatives.append(f"https://{alt}")
        
        return alternatives


class FixSuggestionEngine:
    """修复建议引擎"""

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.wayback: Optional[WaybackMachineClient] = None
        self.redirect: Optional[RedirectDetector] = None
        self.alternative: Optional[AlternativeFinder] = None

    async def __aenter__(self):
        """异步上下文管理器入口"""
        timeout = aiohttp.ClientTimeout(total=30)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AnalysisDataFlow-LinkChecker/1.0.0'
        }
        self.session = aiohttp.ClientSession(timeout=timeout, headers=headers)
        self.wayback = WaybackMachineClient(self.session)
        self.redirect = RedirectDetector(self.session)
        self.alternative = AlternativeFinder()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()

    async def analyze_broken_link(self, result: Dict) -> List[FixSuggestion]:
        """分析单个失效链接并生成修复建议"""
        suggestions = []
        url = result.get('url', '')
        source_file = result.get('source_file', '')
        line_number = result.get('line_number', 0)
        error = result.get('error_message', '')
        
        # 1. 检查是否是重定向
        redirect_url = await self.redirect.check_redirect(url)
        if redirect_url:
            suggestions.append(FixSuggestion(
                original_url=url,
                source_file=source_file,
                line_number=line_number,
                suggestion_type='redirect',
                suggested_url=redirect_url,
                confidence=0.9,
                description=f"URL永久重定向到: {redirect_url}",
                auto_fixable=True
            ))
        
        # 2. 检查域名修复
        domain_fix = self.redirect.suggest_domain_fix(url)
        if domain_fix and domain_fix != url:
            suggestions.append(FixSuggestion(
                original_url=url,
                source_file=source_file,
                line_number=line_number,
                suggestion_type='domain_fix',
                suggested_url=domain_fix,
                confidence=0.7,
                description=f"建议升级到HTTPS: {domain_fix}",
                auto_fixable=True
            ))
        
        # 3. Wayback Machine 快照
        if url.startswith('http'):
            snapshot = await self.wayback.get_snapshot(url)
            if snapshot:
                suggestions.append(FixSuggestion(
                    original_url=url,
                    source_file=source_file,
                    line_number=line_number,
                    suggestion_type='wayback',
                    suggested_url=snapshot,
                    confidence=0.8,
                    description=f"Wayback Machine 存档快照",
                    auto_fixable=False  # 需要人工确认
                ))
        
        # 4. 文档替代
        doc_alt = self.alternative.find_doc_alternative(url)
        if doc_alt:
            suggestions.append(FixSuggestion(
                original_url=url,
                source_file=source_file,
                line_number=line_number,
                suggestion_type='doc_update',
                suggested_url=doc_alt,
                confidence=0.75,
                description="文档版本已更新",
                auto_fixable=True
            ))
        
        # 5. 学术论文替代
        if any(x in url for x in ['acm.org', 'ieee.org', 'springer.com']):
            paper_alts = self.alternative.find_paper_alternative(url)
            for alt in paper_alts:
                suggestions.append(FixSuggestion(
                    original_url=url,
                    source_file=source_file,
                    line_number=line_number,
                    suggestion_type='paper_alt',
                    suggested_url=alt,
                    confidence=0.5,
                    description="学术论文替代源 (请验证可访问性)",
                    auto_fixable=False
                ))
        
        # 6. 如果没有任何建议，提供手动修复选项
        if not suggestions:
            suggestions.append(FixSuggestion(
                original_url=url,
                source_file=source_file,
                line_number=line_number,
                suggestion_type='manual',
                suggested_url=None,
                confidence=0.0,
                description=f"需要手动修复: {error}",
                auto_fixable=False
            ))
        
        return suggestions

    async def process_results(self, results: List[Dict]) -> List[FixSuggestion]:
        """处理所有失效链接"""
        all_suggestions = []
        
        # 只处理失效链接
        broken_links = [r for r in results if not r.get('is_valid')]
        
        print(f"分析 {len(broken_links)} 个失效链接...")
        
        # 并发处理
        tasks = [self.analyze_broken_link(result) for result in broken_links]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_suggestions.extend(result)
            else:
                print(f"处理链接时出错: {result}")
        
        return all_suggestions


def generate_fix_script(suggestions: List[FixSuggestion], output_path: Path):
    """生成自动修复脚本"""
    # 筛选可自动修复的建议
    auto_fixable = [s for s in suggestions if s.auto_fixable and s.suggested_url]
    
    script_lines = [
        "#!/usr/bin/env python3",
        "# -*- coding: utf-8 -*",
        "# 自动生成的链接修复脚本",
        "# 生成时间: {}".format(time.strftime('%Y-%m-%d %H:%M:%S')),
        "",
        "import re",
        "from pathlib import Path",
        "",
        "# 修复规则",
        "fixes = [",
    ]
    
    # 按文件分组
    by_file: Dict[str, List[FixSuggestion]] = {}
    for s in auto_fixable:
        if s.source_file not in by_file:
            by_file[s.source_file] = []
        by_file[s.source_file].append(s)
    
    for file_path, fixes in by_file.items():
        for fix in fixes:
            script_lines.append(f"    # {file_path}:{fix.line_number}")
            script_lines.append(f"    ('{file_path}', r'{fix.original_url}', '{fix.suggested_url}'),")
    
    script_lines.extend([
        "]",
        "",
        "def apply_fixes():",
        "    for file_path, old_url, new_url in fixes:",
        "        path = Path(file_path)",
        "        if not path.exists():",
        "            print(f'文件不存在: {file_path}')",
        "            continue",
        "        ",
        "        content = path.read_text(encoding='utf-8')",
        "        # 使用正则确保精确匹配",
        "        pattern = re.escape(old_url)",
        "        if re.search(pattern, content):",
        "            new_content = re.sub(pattern, new_url, content)",
        "            path.write_text(new_content, encoding='utf-8')",
        "            print(f'✓ 修复: {file_path}')",
        "            print(f'  {old_url} -> {new_url}')",
        "        else:",
        "            print(f'✗ 未找到: {file_path} - {old_url}')",
        "",
        'if __name__ == "__main__":',
        "    apply_fixes()",
        "",
    ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(script_lines))
    
    print(f"修复脚本已生成: {output_path}")
    print(f"包含 {len(auto_fixable)} 个自动修复规则")


def generate_markdown_report(suggestions: List[FixSuggestion], output_path: Path):
    """生成Markdown修复建议报告"""
    # 按类型分组
    by_type: Dict[str, List[FixSuggestion]] = {
        'redirect': [],
        'wayback': [],
        'doc_update': [],
        'domain_fix': [],
        'manual': [],
        'other': []
    }
    
    for s in suggestions:
        if s.suggestion_type in by_type:
            by_type[s.suggestion_type].append(s)
        else:
            by_type['other'].append(s)
    
    md_lines = [
        "# 🔧 链接修复建议报告",
        "",
        f"> 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"> 总建议数: {len(suggestions)}",
        "",
        "## 📊 建议分类统计",
        "",
        "| 类型 | 数量 | 可自动修复 |",
        "|------|------|------------|",
    ]
    
    for type_name, items in by_type.items():
        auto_count = sum(1 for s in items if s.auto_fixable)
        type_label = {
            'redirect': '🔀 重定向',
            'wayback': '📚 Wayback存档',
            'doc_update': '📖 文档更新',
            'domain_fix': '🔒 HTTPS升级',
            'manual': '✋ 手动修复',
            'other': '📦 其他'
        }.get(type_name, type_name)
        md_lines.append(f"| {type_label} | {len(items)} | {auto_count} |")
    
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    
    # 可自动修复的建议
    auto_fixable = [s for s in suggestions if s.auto_fixable]
    if auto_fixable:
        md_lines.extend([
            "## ✅ 可自动修复",
            "",
            "运行以下命令应用自动修复:",
            "",
            "```bash",
            "python auto-fix-links.py",
            "```",
            "",
            "| 原URL | 建议URL | 文件 | 行号 |",
            "|-------|---------|------|------|",
        ])
        
        for s in auto_fixable[:50]:  # 限制显示数量
            orig = s.original_url[:50] + '...' if len(s.original_url) > 50 else s.original_url
            sugg = s.suggested_url[:50] + '...' if len(s.suggested_url) > 50 else s.suggested_url
            md_lines.append(f"| {orig} | {sugg} | {s.source_file} | {s.line_number} |")
        
        if len(auto_fixable) > 50:
            md_lines.append(f"\n*... 还有 {len(auto_fixable) - 50} 个可自动修复的链接*\n")
        
        md_lines.append("")
    
    # 需要手动检查的建议
    manual_check = [s for s in suggestions if not s.auto_fixable]
    if manual_check:
        md_lines.extend([
            "## ✋ 需要手动检查",
            "",
            "| 原URL | 建议 | 文件 | 行号 | 置信度 |",
            "|-------|------|------|------|--------|",
        ])
        
        for s in manual_check[:50]:
            orig = s.original_url[:40] + '...' if len(s.original_url) > 40 else s.original_url
            sugg = (s.suggested_url[:40] + '...') if s.suggested_url and len(s.suggested_url) > 40 else (s.suggested_url or '-')
            confidence = f"{s.confidence*100:.0f}%"
            md_lines.append(f"| {orig} | {sugg} | {s.source_file} | {s.line_number} | {confidence} |")
        
        if len(manual_check) > 50:
            md_lines.append(f"\n*... 还有 {len(manual_check) - 50} 个需要手动检查的链接*\n")
        
        md_lines.append("")
    
    # Wayback存档建议
    wayback_suggestions = by_type.get('wayback', [])
    if wayback_suggestions:
        md_lines.extend([
            "## 📚 Wayback Machine 存档",
            "",
            "以下链接在 Wayback Machine 中有存档，请验证内容后决定是否替换:",
            "",
            "| 原URL | 存档URL | 文件 | 行号 |",
            "|-------|---------|------|------|",
        ])
        
        for s in wayback_suggestions[:30]:
            orig = s.original_url[:40] + '...' if len(s.original_url) > 40 else s.original_url
            sugg = s.suggested_url[:60] + '...' if len(s.suggested_url) > 60 else s.suggested_url
            md_lines.append(f"| {orig} | [{sugg}]({s.suggested_url}) | {s.source_file} | {s.line_number} |")
        
        md_lines.append("")
    
    md_lines.extend([
        "---",
        "",
        "*由 AnalysisDataFlow Fix Suggestions Tool 生成*",
    ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
    
    print(f"Markdown报告已生成: {output_path}")


def generate_json_report(suggestions: List[FixSuggestion], output_path: Path):
    """生成JSON格式的修复建议"""
    data = {
        'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_suggestions': len(suggestions),
        'auto_fixable_count': sum(1 for s in suggestions if s.auto_fixable),
        'suggestions': [
            {
                'original_url': s.original_url,
                'source_file': s.source_file,
                'line_number': s.line_number,
                'suggestion_type': s.suggestion_type,
                'suggested_url': s.suggested_url,
                'confidence': s.confidence,
                'description': s.description,
                'auto_fixable': s.auto_fixable
            }
            for s in suggestions
        ]
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"JSON报告已生成: {output_path}")


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='链接修复建议工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --input link-check-results.json
  %(prog)s --input link-check-results.json --generate-script
  %(prog)s --input link-check-results.json --output-md fix-suggestions.md
        """
    )
    
    parser.add_argument('--input', '-i', type=str, required=True,
                       help='输入的链接检查结果JSON文件')
    parser.add_argument('--output-md', type=str,
                       help='输出Markdown报告路径')
    parser.add_argument('--output-json', type=str,
                       help='输出JSON报告路径')
    parser.add_argument('--generate-script', action='store_true',
                       help='生成Python修复脚本')
    parser.add_argument('--script-path', type=str, default='auto-fix-links.py',
                       help='修复脚本输出路径 (默认: auto-fix-links.py)')
    parser.add_argument('--confidence', type=float, default=0.5,
                       help='置信度阈值 (默认: 0.5)')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        return 1
    
    # 加载结果
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = data.get('results', [])
    
    print(f"加载了 {len(results)} 个检查结果")
    
    # 分析并提供建议
    async with FixSuggestionEngine() as engine:
        suggestions = await engine.process_results(results)
    
    # 按置信度过滤
    suggestions = [s for s in suggestions if s.confidence >= args.confidence]
    
    print(f"\n生成了 {len(suggestions)} 个修复建议")
    print(f"  - 可自动修复: {sum(1 for s in suggestions if s.auto_fixable)}")
    print(f"  - 需要手动检查: {sum(1 for s in suggestions if not s.auto_fixable)}")
    
    # 生成报告
    if args.output_md:
        generate_markdown_report(suggestions, Path(args.output_md))
    
    if args.output_json:
        generate_json_report(suggestions, Path(args.output_json))
    
    if args.generate_script:
        generate_fix_script(suggestions, Path(args.script_path))
    
    # 如果没有指定输出，默认生成所有格式
    if not any([args.output_md, args.output_json, args.generate_script]):
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        generate_markdown_report(suggestions, Path(f'fix-suggestions-{timestamp}.md'))
        generate_json_report(suggestions, Path(f'fix-suggestions-{timestamp}.json'))
        generate_fix_script(suggestions, Path('auto-fix-links.py'))
    
    return 0


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
