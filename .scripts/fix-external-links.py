#!/usr/bin/env python3
"""
外部链接自动修复工具
自动修复301重定向和替换失效链接为Archive.org备份

Author: AnalysisDataFlow Project
Version: 1.0.0
"""

import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from urllib.parse import quote


class ExternalLinkFixer:
    """外部链接修复器"""
    
    def __init__(self, root_dir: Path, dry_run: bool = True):
        """
        初始化修复器
        
        Args:
            root_dir: 项目根目录
            dry_run: 是否仅模拟运行（不实际修改文件）
        """
        self.root_dir = root_dir
        self.dry_run = dry_run
        self.changes: List[Dict] = []
        self.stats = {
            'files_scanned': 0,
            'files_modified': 0,
            'links_fixed': 0,
            'errors': 0
        }
    
    def get_archive_url(self, url: str) -> str:
        """获取Archive.org备份URL"""
        return f"https://web.archive.org/web/*/{url}"
    
    def fix_redirects_in_file(self, file_path: Path, redirect_map: Dict[str, str]) -> int:
        """
        修复文件中的重定向链接
        
        Args:
            file_path: 文件路径
            redirect_map: 旧URL -> 新URL 映射
            
        Returns:
            int: 修复的链接数
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            fixed_count = 0
            
            for old_url, new_url in redirect_map.items():
                # 转义特殊字符用于正则
                escaped_old = re.escape(old_url)
                
                # 匹配Markdown链接 [text](url)
                pattern = rf'\[([^\]]+)\]\({escaped_old}\)'
                matches = list(re.finditer(pattern, content))
                
                for match in matches:
                    link_text = match.group(1)
                    old_full = match.group(0)
                    new_full = f"[{link_text}]({new_url})"
                    content = content.replace(old_full, new_full)
                    fixed_count += 1
                    self.changes.append({
                        'file': str(file_path.relative_to(self.root_dir)),
                        'old_url': old_url,
                        'new_url': new_url,
                        'type': 'redirect',
                        'link_text': link_text
                    })
                
                # 匹配引用式链接定义 [ref]: url
                ref_pattern = rf'^(\[([^\]]+)\]:\s*){escaped_old}$'
                for match in re.finditer(ref_pattern, content, re.MULTILINE):
                    old_def = match.group(0)
                    ref = match.group(2)
                    new_def = f"[{ref}]: {new_url}"
                    content = content.replace(old_def, new_def)
                    fixed_count += 1
                    self.changes.append({
                        'file': str(file_path.relative_to(self.root_dir)),
                        'old_url': old_url,
                        'new_url': new_url,
                        'type': 'redirect_ref',
                        'ref': ref
                    })
                
                # 匹配裸URL <http://...>
                bare_pattern = rf'<{escaped_old}>'
                if re.search(bare_pattern, content):
                    content = re.sub(bare_pattern, f'<{new_url}>', content)
                    fixed_count += 1
                    self.changes.append({
                        'file': str(file_path.relative_to(self.root_dir)),
                        'old_url': old_url,
                        'new_url': new_url,
                        'type': 'bare_url'
                    })
            
            # 保存修改
            if content != original_content:
                self.stats['files_modified'] += 1
                if not self.dry_run:
                    file_path.write_text(content, encoding='utf-8')
                    print(f"  ✏️ 已更新: {file_path.relative_to(self.root_dir)}")
                else:
                    print(f"  📝 将更新: {file_path.relative_to(self.root_dir)}")
            
            return fixed_count
            
        except Exception as e:
            print(f"  ⚠️ 处理失败 {file_path}: {e}")
            self.stats['errors'] += 1
            return 0
    
    def mark_dead_links(self, file_path: Path, dead_links: List[Dict]) -> int:
        """
        标记文件中的失效链接
        
        Args:
            file_path: 文件路径
            dead_links: 失效链接列表，每项包含 url, error, archive_url
            
        Returns:
            int: 标记的链接数
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            marked_count = 0
            
            for link_info in dead_links:
                url = link_info['url']
                error = link_info.get('error', 'Unknown')
                archive_url = link_info.get('archive_url')
                
                escaped_url = re.escape(url)
                
                # 在链接后添加失效标记和Archive备份
                # 匹配Markdown链接 [text](url)
                pattern = rf'\[([^\]]+)\]\({escaped_url}\)'
                
                def replace_with_marker(match):
                    nonlocal marked_count
                    link_text = match.group(1)
                    marker = f"⚠️ **[已失效: {error}]**"
                    if archive_url:
                        marker += f" [Archive备份]({archive_url})"
                    marked_count += 1
                    return f"[{link_text}]({url}) {marker}"
                
                content = re.sub(pattern, replace_with_marker, content)
            
            # 保存修改
            if content != original_content:
                self.stats['files_modified'] += 1
                if not self.dry_run:
                    file_path.write_text(content, encoding='utf-8')
                    print(f"  ✏️ 已标记: {file_path.relative_to(self.root_dir)}")
                else:
                    print(f"  📝 将标记: {file_path.relative_to(self.root_dir)}")
            
            return marked_count
            
        except Exception as e:
            print(f"  ⚠️ 处理失败 {file_path}: {e}")
            self.stats['errors'] += 1
            return 0
    
    def fix_all_redirects(self, results_file: str = ".scripts/.link_check_results.json"):
        """
        修复所有301重定向链接
        
        Args:
            results_file: 检测结果JSON文件
        """
        results_path = self.root_dir / results_file
        if not results_path.exists():
            print(f"❌ 未找到检测结果文件: {results_file}")
            print("请先运行: python .scripts/external-link-checker.py")
            return
        
        with open(results_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 构建重定向映射
        redirect_map = {}
        for result in data.get('results', []):
            if result.get('redirect_url') and result.get('is_accessible'):
                old_url = result['url']
                new_url = result['redirect_url']
                redirect_map[old_url] = new_url
        
        if not redirect_map:
            print("✅ 未发现需要修复的重定向链接")
            return
        
        print(f"🔧 发现 {len(redirect_map)} 个重定向链接需要修复")
        
        # 扫描所有Markdown文件
        md_files = list(self.root_dir.rglob('*.md'))
        print(f"📄 扫描 {len(md_files)} 个文件...")
        
        for md_file in md_files:
            if '.git' in str(md_file):
                continue
            self.stats['files_scanned'] += 1
            fixed = self.fix_redirects_in_file(md_file, redirect_map)
            self.stats['links_fixed'] += fixed
        
        self.print_summary()
    
    def mark_all_dead_links(self, results_file: str = ".scripts/.link_check_results.json"):
        """
        标记所有失效链接
        
        Args:
            results_file: 检测结果JSON文件
        """
        results_path = self.root_dir / results_file
        if not results_path.exists():
            print(f"❌ 未找到检测结果文件: {results_file}")
            return
        
        with open(results_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 按文件分组失效链接
        dead_by_file: Dict[str, List[Dict]] = {}
        
        for result in data.get('results', []):
            if not result.get('is_accessible'):
                url = result['url']
                error = result.get('error_message', 'Unknown')
                archive_url = self.get_archive_url(url)
                
                for file_path in result.get('source_files', []):
                    if file_path not in dead_by_file:
                        dead_by_file[file_path] = []
                    dead_by_file[file_path].append({
                        'url': url,
                        'error': error,
                        'archive_url': archive_url
                    })
        
        if not dead_by_file:
            print("✅ 未发现失效链接")
            return
        
        print(f"🔍 发现 {sum(len(v) for v in dead_by_file.values())} 个失效链接分布在 {len(dead_by_file)} 个文件中")
        
        for file_path_str, dead_links in dead_by_file.items():
            file_path = self.root_dir / file_path_str
            if file_path.exists():
                self.stats['files_scanned'] += 1
                marked = self.mark_dead_links(file_path, dead_links)
                self.stats['links_fixed'] += marked
        
        self.print_summary()
    
    def generate_archive_report(self, results_file: str = ".scripts/.link_check_results.json",
                                output_file: str = "ARCHIVE-LINK-SUGGESTIONS.md"):
        """
        生成Archive.org备份建议报告
        
        Args:
            results_file: 检测结果JSON文件
            output_file: 输出报告文件名
        """
        results_path = self.root_dir / results_file
        if not results_path.exists():
            print(f"❌ 未找到检测结果文件: {results_file}")
            return
        
        with open(results_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        dead_links = [r for r in data.get('results', []) if not r.get('is_accessible')]
        
        lines = [
            "# Archive.org 备份链接建议",
            "",
            f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"> 失效链接数: {len(dead_links)}",
            "",
            "## 失效链接及Archive备份",
            "",
            "| 失效链接 | 错误信息 | Archive查询 | 源文件 |",
            "|----------|----------|-------------|--------|",
        ]
        
        for result in sorted(dead_links, key=lambda x: -x.get('priority', 0)):
            url = result['url']
            error = result.get('error_message', 'Unknown')[:30]
            archive_query = self.get_archive_url(url)
            files = ", ".join(result.get('source_files', [])[:2])[:40]
            lines.append(f"| [{url[:50]}...]({url}) | {error} | [查看备份]({archive_query}) | {files} |")
        
        lines.extend([
            "",
            "## 批量替换脚本",
            "",
            "可以使用以下Python脚本批量替换失效链接为Archive备份：",
            "",
            "```python",
            "import re",
            "",
            "# 定义替换映射",
            "replace_map = {",
        ])
        
        for result in dead_links[:20]:  # 只显示前20个
            url = result['url']
            archive = f"https://web.archive.org/web/20240000000000*/{url}"
            lines.append(f'    "{url}": "{archive}",')
        
        lines.extend([
            "}",
            "",
            "# 读取文件并替换",
            "with open('your-file.md', 'r', encoding='utf-8') as f:",
            "    content = f.read()",
            "",
            "for old, new in replace_map.items():",
            "    content = content.replace(old, new)",
            "",
            "with open('your-file.md', 'w', encoding='utf-8') as f:",
            "    f.write(content)",
            "```",
            "",
        ])
        
        report = "\n".join(lines)
        output_path = self.root_dir / output_file
        output_path.write_text(report, encoding='utf-8')
        print(f"📝 Archive建议报告已保存: {output_file}")
    
    def print_summary(self):
        """打印修复摘要"""
        mode_str = "【模拟模式】" if self.dry_run else "【实际执行】"
        print(f"\n{'='*60}")
        print(f"📊 修复摘要 {mode_str}")
        print(f"{'='*60}")
        print(f"📄 扫描文件: {self.stats['files_scanned']}")
        print(f"✏️ 修改文件: {self.stats['files_modified']}")
        print(f"🔗 修复链接: {self.stats['links_fixed']}")
        print(f"❌ 错误: {self.stats['errors']}")
        print(f"{'='*60}")
        
        if self.dry_run and self.stats['links_fixed'] > 0:
            print("💡 提示: 以上为模拟结果，实际执行请添加 --apply 参数")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='外部链接自动修复工具')
    parser.add_argument('--root', default='.', help='项目根目录')
    parser.add_argument('--mode', choices=['fix-redirects', 'mark-dead', 'archive-report', 'all'],
                        default='all', help='修复模式')
    parser.add_argument('--apply', action='store_true', help='实际执行修改（默认模拟运行）')
    parser.add_argument('--results', default='.scripts/.link_check_results.json',
                        help='检测结果JSON文件路径')
    args = parser.parse_args()
    
    root_dir = Path(args.root).resolve()
    fixer = ExternalLinkFixer(root_dir, dry_run=not args.apply)
    
    print(f"🔧 外部链接修复工具")
    print(f"📁 项目目录: {root_dir}")
    print(f"⚙️ 运行模式: {'实际执行' if args.apply else '模拟运行'}")
    print()
    
    if args.mode in ('fix-redirects', 'all'):
        print("🔄 模式1: 修复301重定向")
        fixer.fix_all_redirects(args.results)
        print()
    
    if args.mode in ('mark-dead', 'all'):
        print("🏷️ 模式2: 标记失效链接")
        fixer.mark_all_dead_links(args.results)
        print()
    
    if args.mode in ('archive-report', 'all'):
        print("📋 模式3: 生成Archive报告")
        fixer.generate_archive_report(args.results)
        print()
    
    print("✅ 修复工具执行完成")


if __name__ == '__main__':
    main()
