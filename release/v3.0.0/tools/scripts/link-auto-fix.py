#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
链接自动修复工具 v3.0

功能:
- 自动更新重定向链接（301/302）到新URL
- 标记无法自动修复的失效链接
- 支持批量处理和手动确认模式

作者: AnalysisDataFlow 项目
版本: 3.0.0
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

# 失效链接标记模板
BROKEN_LINK_MARKER = "<!-- BROKEN_LINK: {reason} -->"
BROKEN_LINK_SUFFIX = " ⚠️ *[链接失效: {reason}]*"


@dataclass
class LinkFix:
    """链接修复记录"""
    original_url: str
    new_url: str
    file_path: str
    line_number: int
    fix_type: str  # 'redirect', 'manual', 'marked'
    status: str = 'pending'  # 'pending', 'applied', 'failed'


class LinkAutoFixer:
    """链接自动修复器"""
    
    def __init__(self, base_path: Path, dry_run: bool = True):
        self.base_path = base_path
        self.dry_run = dry_run
        self.fixes: List[LinkFix] = []
        self.stats = {
            'redirects_fixed': 0,
            'broken_marked': 0,
            'failed': 0,
            'skipped': 0
        }
    
    def load_check_results(self, results_path: Path) -> Dict:
        """加载链接检查结果"""
        with open(results_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def find_markdown_files(self) -> List[Path]:
        """查找所有Markdown文件"""
        md_files = list(self.base_path.rglob('*.md'))
        # 排除隐藏目录
        md_files = [
            f for f in md_files 
            if not any(part.startswith('.') or part in ['node_modules', '__pycache__'] 
                      for part in f.parts)
        ]
        return md_files
    
    def find_link_in_file(self, file_path: Path, url: str, line_number: Optional[int] = None) -> List[Tuple[int, str, str]]:
        """
        在文件中查找链接，返回 (行号, 原行内容, 链接文本) 的列表
        """
        matches = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # Markdown链接正则
            md_pattern = re.compile(r'\[([^\]]+)\]\(([^\s\)]+)(?:\s+"[^"]*")?\)')
            
            for i, line in enumerate(lines, 1):
                if line_number and i != line_number:
                    continue
                
                for match in md_pattern.finditer(line):
                    link_text = match.group(1)
                    link_url = match.group(2)
                    
                    if link_url == url or url in link_url:
                        matches.append((i, line, link_text))
        
        except Exception as e:
            print(f"⚠️ 读取文件失败 {file_path}: {e}")
        
        return matches
    
    def fix_redirect_in_file(self, file_path: Path, original_url: str, 
                             new_url: str, line_number: Optional[int] = None) -> bool:
        """修复文件中的重定向链接"""
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # 转义特殊字符用于正则
            escaped_url = re.escape(original_url)
            
            # 替换链接URL（保持链接文本不变）
            # 匹配 [text](url) 或 [text](url "title")
            pattern = rf'(\[[^\]]+\]\(){escaped_url}((?:\s+"[^"]*")?\))'
            replacement = rf'\g<1>{new_url}\g<2>'
            
            new_content, count = re.subn(pattern, replacement, content)
            
            if count > 0:
                if not self.dry_run:
                    file_path.write_text(new_content, encoding='utf-8')
                    print(f"  ✅ 已修复: {file_path} (替换了 {count} 处)")
                else:
                    print(f"  [DRY-RUN] 将修复: {file_path} (可替换 {count} 处)")
                return True
            else:
                # 尝试简单字符串替换
                if original_url in content:
                    new_content = content.replace(original_url, new_url)
                    if new_content != content:
                        if not self.dry_run:
                            file_path.write_text(new_content, encoding='utf-8')
                            print(f"  ✅ 已修复(字符串替换): {file_path}")
                        else:
                            print(f"  [DRY-RUN] 将修复(字符串替换): {file_path}")
                        return True
            
            return False
            
        except Exception as e:
            print(f"  ❌ 修复失败 {file_path}: {e}")
            return False
    
    def mark_broken_link(self, file_path: Path, url: str, reason: str,
                         line_number: Optional[int] = None) -> bool:
        """标记失效链接"""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            modified = False
            
            for i, line in enumerate(lines):
                if line_number and i + 1 != line_number:
                    continue
                
                if url in line:
                    # 检查是否已经标记
                    if 'BROKEN_LINK' in line or '*[链接失效' in line:
                        continue
                    
                    # 在链接后添加失效标记
                    # 找到链接的结束位置
                    md_pattern = re.compile(r'(\[([^\]]+)\]\([^\)]+\))')
                    for match in md_pattern.finditer(line):
                        if url in match.group(1):
                            full_match = match.group(1)
                            link_text = match.group(2)
                            # 添加失效标记
                            marked = f"{full_match} ⚠️ *[链接失效: {reason}]*"
                            line = line.replace(full_match, marked, 1)
                            lines[i] = line
                            modified = True
                            break
            
            if modified:
                new_content = '\n'.join(lines)
                if not self.dry_run:
                    file_path.write_text(new_content, encoding='utf-8')
                    print(f"  ✅ 已标记失效链接: {file_path}")
                else:
                    print(f"  [DRY-RUN] 将标记失效链接: {file_path}")
                return True
            
            return False
            
        except Exception as e:
            print(f"  ❌ 标记失败 {file_path}: {e}")
            return False
    
    def fix_redirects(self, results_path: Path, confirm: bool = False) -> Dict:
        """自动修复重定向链接"""
        print("="*70)
        print("🔄 开始修复重定向链接")
        print("="*70)
        
        data = self.load_check_results(results_path)
        results = data.get('results', [])
        
        # 筛选重定向链接
        redirect_results = [
            r for r in results 
            if r.get('link_type') == 'redirect' and r.get('final_url')
        ]
        
        print(f"发现 {len(redirect_results)} 个重定向链接需要修复\n")
        
        if not redirect_results:
            print("✅ 没有需要修复的重定向链接")
            return self.stats
        
        # 按文件分组
        by_file: Dict[str, List[Dict]] = {}
        for result in redirect_results:
            file_path = result.get('source_file', '')
            if file_path not in by_file:
                by_file[file_path] = []
            by_file[file_path].append(result)
        
        for file_path_str, file_results in sorted(by_file.items()):
            file_path = self.base_path / file_path_str
            
            if not file_path.exists():
                print(f"⚠️ 文件不存在: {file_path}")
                continue
            
            print(f"\n📄 处理文件: {file_path_str}")
            
            for result in file_results:
                original_url = result['url']
                new_url = result.get('final_url') or result.get('redirect_url')
                line_number = result.get('line_number')
                
                if not new_url or original_url == new_url:
                    continue
                
                # 跳过某些域名
                if self._should_skip_domain(new_url):
                    print(f"  ⏭️  跳过域名: {original_url[:60]}...")
                    self.stats['skipped'] += 1
                    continue
                
                # 确认模式
                if confirm:
                    print(f"\n  原链接: {original_url[:80]}")
                    print(f"  新链接: {new_url[:80]}")
                    response = input("  是否修复? [Y/n/q]: ").strip().lower()
                    if response == 'q':
                        print("  已取消")
                        return self.stats
                    if response and response != 'y':
                        print("  已跳过")
                        self.stats['skipped'] += 1
                        continue
                
                # 执行修复
                success = self.fix_redirect_in_file(file_path, original_url, new_url, line_number)
                
                if success:
                    self.stats['redirects_fixed'] += 1
                    self.fixes.append(LinkFix(
                        original_url=original_url,
                        new_url=new_url,
                        file_path=str(file_path),
                        line_number=line_number or 0,
                        fix_type='redirect',
                        status='applied' if not self.dry_run else 'pending'
                    ))
                else:
                    self.stats['failed'] += 1
                    print(f"  ❌ 无法自动修复: {original_url[:60]}...")
        
        return self.stats
    
    def mark_broken_links(self, results_path: Path, confirm: bool = False) -> Dict:
        """标记失效链接"""
        print("\n" + "="*70)
        print("❌ 开始标记失效链接")
        print("="*70)
        
        data = self.load_check_results(results_path)
        results = data.get('results', [])
        
        # 筛选失效链接
        broken_results = [
            r for r in results 
            if r.get('link_type') == 'broken' and r.get('is_valid') == False
        ]
        
        print(f"发现 {len(broken_results)} 个失效链接需要标记\n")
        
        if not broken_results:
            print("✅ 没有需要标记的失效链接")
            return self.stats
        
        # 按文件分组
        by_file: Dict[str, List[Dict]] = {}
        for result in broken_results:
            file_path = result.get('source_file', '')
            if file_path not in by_file:
                by_file[file_path] = []
            by_file[file_path].append(result)
        
        for file_path_str, file_results in sorted(by_file.items()):
            file_path = self.base_path / file_path_str
            
            if not file_path.exists():
                print(f"⚠️ 文件不存在: {file_path}")
                continue
            
            print(f"\n📄 处理文件: {file_path_str}")
            
            for result in file_results:
                url = result['url']
                reason = result.get('error_message', '链接失效')
                line_number = result.get('line_number')
                
                # 确认模式
                if confirm:
                    print(f"\n  失效链接: {url[:80]}")
                    print(f"  原因: {reason}")
                    response = input("  是否标记? [Y/n/q]: ").strip().lower()
                    if response == 'q':
                        print("  已取消")
                        return self.stats
                    if response and response != 'y':
                        print("  已跳过")
                        self.stats['skipped'] += 1
                        continue
                
                # 执行标记
                success = self.mark_broken_link(file_path, url, reason, line_number)
                
                if success:
                    self.stats['broken_marked'] += 1
                    self.fixes.append(LinkFix(
                        original_url=url,
                        new_url='',
                        file_path=str(file_path),
                        line_number=line_number or 0,
                        fix_type='marked',
                        status='applied' if not self.dry_run else 'pending'
                    ))
                else:
                    # 可能是已经标记过或找不到
                    pass
        
        return self.stats
    
    def _should_skip_domain(self, url: str) -> bool:
        """检查是否应该跳过此域名的自动修复"""
        skip_domains = [
            'localhost',
            '127.0.0.1',
            'example.com',
            'your-domain.com',
        ]
        
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        for skip in skip_domains:
            if skip in domain:
                return True
        
        return False
    
    def list_redirects(self, results_path: Path):
        """列出所有重定向链接"""
        data = self.load_check_results(results_path)
        results = data.get('results', [])
        
        redirect_results = [
            r for r in results 
            if r.get('link_type') == 'redirect' and r.get('final_url')
        ]
        
        print("="*70)
        print(f"🔄 重定向链接列表 ({len(redirect_results)} 个)")
        print("="*70)
        
        if not redirect_results:
            print("没有发现重定向链接")
            return
        
        # 按文件分组
        by_file: Dict[str, List[Dict]] = {}
        for result in redirect_results:
            file_path = result.get('source_file', '')
            if file_path not in by_file:
                by_file[file_path] = []
            by_file[file_path].append(result)
        
        for file_path_str, file_results in sorted(by_file.items()):
            print(f"\n📄 {file_path_str}")
            for result in file_results:
                original = result['url']
                final = result.get('final_url', result.get('redirect_url', ''))
                print(f"  {original[:60]}...")
                print(f"  → {final[:60]}...")
    
    def list_broken(self, results_path: Path):
        """列出所有失效链接"""
        data = self.load_check_results(results_path)
        results = data.get('results', [])
        
        broken_results = [
            r for r in results 
            if r.get('link_type') == 'broken' and r.get('is_valid') == False
        ]
        
        print("="*70)
        print(f"❌ 失效链接列表 ({len(broken_results)} 个)")
        print("="*70)
        
        if not broken_results:
            print("没有发现失效链接")
            return
        
        # 按文件分组
        by_file: Dict[str, List[Dict]] = {}
        for result in broken_results:
            file_path = result.get('source_file', '')
            if file_path not in by_file:
                by_file[file_path] = []
            by_file[file_path].append(result)
        
        for file_path_str, file_results in sorted(by_file.items()):
            print(f"\n📄 {file_path_str}")
            for result in file_results:
                url = result['url']
                error = result.get('error_message', '未知错误')
                line = result.get('line_number', 0)
                print(f"  行 {line}: {url[:60]}...")
                print(f"     错误: {error}")
    
    def generate_fix_report(self, output_path: Path):
        """生成修复报告"""
        report_lines = []
        report_lines.append("# 链接自动修复报告\n")
        report_lines.append(f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_lines.append(f"**模式:** {'试运行' if self.dry_run else '实际执行'}\n")
        
        report_lines.append("## 统计摘要\n")
        report_lines.append(f"- 重定向修复: {self.stats['redirects_fixed']}")
        report_lines.append(f"- 失效链接标记: {self.stats['broken_marked']}")
        report_lines.append(f"- 失败: {self.stats['failed']}")
        report_lines.append(f"- 跳过: {self.stats['skipped']}")
        report_lines.append("")
        
        if self.fixes:
            report_lines.append("## 修复详情\n")
            report_lines.append("| 类型 | 文件 | 行号 | 原链接 | 新链接/操作 |")
            report_lines.append("|------|------|------|--------|-------------|")
            for fix in self.fixes:
                original_short = fix.original_url[:40] + "..." if len(fix.original_url) > 40 else fix.original_url
                new_short = fix.new_url[:40] + "..." if len(fix.new_url) > 40 else fix.new_url
                if fix.fix_type == 'marked':
                    new_short = "[已标记失效]"
                report_lines.append(f"| {fix.fix_type} | `{fix.file_path}` | {fix.line_number} | {original_short} | {new_short} |")
            report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        if not self.dry_run:
            output_path.write_text(report_content, encoding='utf-8')
            print(f"\n📄 修复报告已保存: {output_path}")
        
        return report_content


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='链接自动修复工具 v3.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 试运行（查看将要修复的内容，不实际修改）
  %(prog)s --dry-run
  
  # 自动修复所有重定向链接
  %(prog)s --fix-redirects
  
  # 标记所有失效链接
  %(prog)s --mark-broken
  
  # 修复并重定向和标记（完整自动修复）
  %(prog)s --fix-redirects --mark-broken
  
  # 交互式确认模式
  %(prog)s --fix-redirects --confirm
  
  # 仅列出重定向链接
  %(prog)s --list-redirects
  
  # 仅列出失效链接
  %(prog)s --list-broken
        """
    )
    
    parser.add_argument('--path', '-p', type=str, default='.',
                       help='项目基础路径 (默认: 当前目录)')
    parser.add_argument('--results', '-r', type=str, 
                       default='reports/link-health-results.json',
                       help='链接检查结果JSON文件路径')
    parser.add_argument('--fix-redirects', action='store_true',
                       help='修复重定向链接')
    parser.add_argument('--mark-broken', action='store_true',
                       help='标记失效链接')
    parser.add_argument('--list-redirects', action='store_true',
                       help='仅列出重定向链接')
    parser.add_argument('--list-broken', action='store_true',
                       help='仅列出失效链接')
    parser.add_argument('--dry-run', '-n', action='store_true',
                       help='试运行模式（不实际修改文件）')
    parser.add_argument('--confirm', '-c', action='store_true',
                       help='交互式确认模式')
    parser.add_argument('--report', type=str, default='reports/link-fix-report.md',
                       help='修复报告输出路径')
    
    args = parser.parse_args()
    
    base_path = Path(args.path).resolve()
    results_path = base_path / args.results
    
    if not results_path.exists():
        print(f"❌ 检查结果文件不存在: {results_path}")
        print("请先运行链接健康检查:")
        print("  python scripts/link-health-checker.py")
        return 1
    
    fixer = LinkAutoFixer(base_path, dry_run=args.dry_run)
    
    # 仅列出模式
    if args.list_redirects:
        fixer.list_redirects(results_path)
        return 0
    
    if args.list_broken:
        fixer.list_broken(results_path)
        return 0
    
    # 如果没有指定具体操作，显示帮助
    if not args.fix_redirects and not args.mark_broken:
        print("请指定操作：--fix-redirects、--mark-broken、--list-redirects 或 --list-broken")
        parser.print_help()
        return 1
    
    print("="*70)
    print("链接自动修复工具 v3.0")
    print("="*70)
    print(f"项目路径: {base_path}")
    print(f"检查结果: {results_path}")
    print(f"模式: {'试运行 (dry-run)' if args.dry_run else '实际执行'}")
    if args.confirm:
        print("交互确认: 启用")
    print("="*70)
    
    # 执行修复
    if args.fix_redirects:
        fixer.fix_redirects(results_path, confirm=args.confirm)
    
    if args.mark_broken:
        fixer.mark_broken_links(results_path, confirm=args.confirm)
    
    # 生成报告
    print("\n" + "="*70)
    print("修复统计")
    print("="*70)
    print(f"重定向修复: {fixer.stats['redirects_fixed']}")
    print(f"失效链接标记: {fixer.stats['broken_marked']}")
    print(f"失败: {fixer.stats['failed']}")
    print(f"跳过: {fixer.stats['skipped']}")
    print("="*70)
    
    fixer.generate_fix_report(base_path / args.report)
    
    if args.dry_run:
        print("\n⚠️  这是试运行模式，没有实际修改文件")
        print("要实际执行修复，请去掉 --dry-run 参数")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
