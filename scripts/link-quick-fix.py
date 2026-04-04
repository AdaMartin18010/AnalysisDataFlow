#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
链接快速修复工具 v3.0 - 用于手动紧急修复

功能:
- 快速修复指定文件中的特定链接
- 支持批量替换URL
- 支持查找和替换所有实例

作者: AnalysisDataFlow 项目
版本: 3.0.0
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional


class LinkQuickFixer:
    """链接快速修复器"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.changes_made = []
    
    def find_files_with_url(self, url: str) -> List[Tuple[Path, int, str]]:
        """
        查找包含指定URL的所有文件
        返回: [(文件路径, 行号, 行内容), ...]
        """
        results = []
        md_files = list(self.base_path.rglob('*.md'))
        
        # 排除隐藏目录
        md_files = [
            f for f in md_files 
            if not any(part.startswith('.') or part in ['node_modules', '__pycache__'] 
                      for part in f.parts)
        ]
        
        print(f"正在搜索 {len(md_files)} 个Markdown文件...")
        
        for file_path in md_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    if url in line:
                        # 检查是否在代码块中
                        # 简单检查：统计前面的 ``` 数量
                        prev_content = '\n'.join(lines[:i-1])
                        code_block_count = prev_content.count('```')
                        in_code_block = code_block_count % 2 == 1
                        
                        if not in_code_block:
                            results.append((file_path, i, line.strip()))
                        
            except Exception as e:
                print(f"⚠️ 读取文件失败 {file_path}: {e}")
        
        return results
    
    def replace_url_in_file(self, file_path: Path, old_url: str, new_url: str,
                           line_number: Optional[int] = None,
                           dry_run: bool = True) -> bool:
        """在文件中替换URL"""
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            if line_number:
                # 仅替换指定行
                lines = content.split('\n')
                if line_number > len(lines):
                    print(f"❌ 行号超出范围: {line_number}")
                    return False
                
                old_line = lines[line_number - 1]
                if old_url not in old_line:
                    print(f"⚠️ 第 {line_number} 行未找到URL: {old_url}")
                    return False
                
                new_line = old_line.replace(old_url, new_url)
                lines[line_number - 1] = new_line
                new_content = '\n'.join(lines)
                
                action = "将替换" if dry_run else "已替换"
                print(f"  {action}第 {line_number} 行:")
                print(f"    - {old_line.strip()[:80]}")
                print(f"    + {new_line.strip()[:80]}")
                
            else:
                # 替换所有实例
                new_content = content.replace(old_url, new_url)
                count = content.count(old_url)
                
                action = "将替换" if dry_run else "已替换"
                print(f"  {action} {count} 处实例")
            
            if new_content == original_content:
                print("⚠️ 内容未改变")
                return False
            
            if not dry_run:
                file_path.write_text(new_content, encoding='utf-8')
                print(f"  ✅ 文件已更新: {file_path}")
            else:
                print(f"  [DRY-RUN] 文件未修改: {file_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ 操作失败 {file_path}: {e}")
            return False
    
    def find_and_replace_all(self, old_url: str, new_url: str,
                            dry_run: bool = True) -> int:
        """查找并替换所有文件中的URL"""
        print("="*70)
        print("🔍 查找并替换所有实例")
        print("="*70)
        print(f"原URL: {old_url}")
        print(f"新URL: {new_url}")
        print("")
        
        matches = self.find_files_with_url(old_url)
        
        if not matches:
            print("❌ 未找到包含此URL的文件")
            return 0
        
        print(f"\n找到 {len(matches)} 个匹配:\n")
        
        for file_path, line_num, line_content in matches:
            rel_path = file_path.relative_to(self.base_path)
            print(f"  {rel_path}:{line_num}")
            print(f"    {line_content[:100]}...")
        
        print("")
        
        if dry_run:
            response = input("是否确认替换? [y/N]: ").strip().lower()
            if response != 'y':
                print("已取消")
                return 0
            dry_run = False
        
        # 执行替换
        fixed_count = 0
        processed_files = set()
        
        for file_path, line_num, _ in matches:
            if file_path in processed_files:
                continue
            
            success = self.replace_url_in_file(
                file_path, old_url, new_url,
                line_number=None,  # 替换所有实例
                dry_run=dry_run
            )
            
            if success:
                fixed_count += 1
                processed_files.add(file_path)
        
        print(f"\n✅ 成功更新 {fixed_count} 个文件")
        return fixed_count
    
    def fix_specific_link(self, file_path: Path, line_number: int,
                         new_url: str, dry_run: bool = True) -> bool:
        """修复特定文件特定行的链接"""
        print("="*70)
        print("🔧 修复特定链接")
        print("="*70)
        
        if not file_path.exists():
            print(f"❌ 文件不存在: {file_path}")
            return False
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            if line_number > len(lines):
                print(f"❌ 行号超出范围: {line_number}")
                return False
            
            line = lines[line_number - 1]
            print(f"\n文件: {file_path}")
            print(f"行 {line_number}: {line.strip()[:100]}")
            
            # 提取链接
            md_pattern = re.compile(r'\[([^\]]+)\]\(([^\s\)]+)')
            matches = list(md_pattern.finditer(line))
            
            if not matches:
                print("❌ 未找到Markdown链接")
                return False
            
            print(f"\n发现 {len(matches)} 个链接:")
            for i, match in enumerate(matches, 1):
                text = match.group(1)
                url = match.group(2)
                print(f"  {i}. [{text}]({url})")
            
            if len(matches) == 1:
                selected = 1
            else:
                selected = input("\n请选择要替换的链接编号 (1-N): ").strip()
                try:
                    selected = int(selected)
                    if selected < 1 or selected > len(matches):
                        print("❌ 无效的选择")
                        return False
                except ValueError:
                    print("❌ 无效的输入")
                    return False
            
            match = matches[selected - 1]
            old_url = match.group(2)
            link_text = match.group(1)
            
            print(f"\n替换链接:")
            print(f"  文本: {link_text}")
            print(f"  原URL: {old_url}")
            print(f"  新URL: {new_url}")
            
            if dry_run:
                response = input("\n是否确认? [y/N]: ").strip().lower()
                if response != 'y':
                    print("已取消")
                    return False
                dry_run = False
            
            # 执行替换
            success = self.replace_url_in_file(
                file_path, old_url, new_url,
                line_number=line_number,
                dry_run=dry_run
            )
            
            return success
            
        except Exception as e:
            print(f"❌ 操作失败: {e}")
            return False
    
    def interactive_fix(self):
        """交互式修复模式"""
        print("="*70)
        print("🛠️  交互式链接修复")
        print("="*70)
        print("")
        print("请选择操作:")
        print("  1. 查找并替换所有文件中的URL")
        print("  2. 修复特定文件特定行的链接")
        print("  3. 查找URL出现在哪些文件中")
        print("  q. 退出")
        print("")
        
        choice = input("请输入选项 (1/2/3/q): ").strip().lower()
        
        if choice == 'q':
            print("再见!")
            return
        
        elif choice == '1':
            old_url = input("请输入要替换的URL: ").strip()
            if not old_url:
                print("❌ URL不能为空")
                return
            
            new_url = input("请输入新的URL: ").strip()
            if not new_url:
                print("❌ 新URL不能为空")
                return
            
            self.find_and_replace_all(old_url, new_url, dry_run=True)
        
        elif choice == '2':
            file_str = input("请输入文件路径 (相对项目根目录): ").strip()
            if not file_str:
                print("❌ 文件路径不能为空")
                return
            
            file_path = self.base_path / file_str
            
            line_str = input("请输入行号: ").strip()
            try:
                line_number = int(line_str)
            except ValueError:
                print("❌ 无效的行号")
                return
            
            new_url = input("请输入新的URL: ").strip()
            if not new_url:
                print("❌ 新URL不能为空")
                return
            
            self.fix_specific_link(file_path, line_number, new_url, dry_run=True)
        
        elif choice == '3':
            url = input("请输入要查找的URL: ").strip()
            if not url:
                print("❌ URL不能为空")
                return
            
            matches = self.find_files_with_url(url)
            
            if not matches:
                print("❌ 未找到包含此URL的文件")
                return
            
            print(f"\n找到 {len(matches)} 个匹配:\n")
            for file_path, line_num, line_content in matches:
                rel_path = file_path.relative_to(self.base_path)
                print(f"  {rel_path}:{line_num}")
                print(f"    {line_content[:100]}...")
        
        else:
            print("❌ 无效的选项")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='链接快速修复工具 v3.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互式修复
  %(prog)s --interactive
  
  # 查找URL所在文件
  %(prog)s --find "https://example.com/old-url"
  
  # 替换所有文件中的URL（交互确认）
  %(prog)s --replace "https://old.com" "https://new.com"
  
  # 修复特定文件特定行的链接
  %(prog)s --file README.md --line 42 --new-url "https://new-url.com"
  
  # 使用完整路径
  %(prog)s --file Flink/01-architecture.md --line 156 \
           --new-url "https://nightlies.apache.org/flink/flink-docs-stable/"
        """
    )
    
    parser.add_argument('--path', '-p', type=str, default='.',
                       help='项目基础路径 (默认: 当前目录)')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='交互式修复模式')
    parser.add_argument('--find', '-f', type=str,
                       help='查找URL所在文件')
    parser.add_argument('--replace', '-r', nargs=2, metavar=('OLD_URL', 'NEW_URL'),
                       help='替换所有文件中的URL')
    parser.add_argument('--file', type=str,
                       help='要修复的文件路径')
    parser.add_argument('--line', '-l', type=int,
                       help='要修复的行号')
    parser.add_argument('--new-url', '-n', type=str,
                       help='新的URL')
    parser.add_argument('--yes', '-y', action='store_true',
                       help='自动确认（不提示）')
    
    args = parser.parse_args()
    
    base_path = Path(args.path).resolve()
    fixer = LinkQuickFixer(base_path)
    
    # 交互模式
    if args.interactive:
        fixer.interactive_fix()
        return 0
    
    # 查找模式
    if args.find:
        matches = fixer.find_files_with_url(args.find)
        
        if not matches:
            print(f"❌ 未找到包含此URL的文件: {args.find}")
            return 1
        
        print(f"\n找到 {len(matches)} 个匹配:\n")
        for file_path, line_num, line_content in matches:
            rel_path = file_path.relative_to(base_path)
            print(f"  {rel_path}:{line_num}")
            print(f"    {line_content[:100]}...")
        return 0
    
    # 替换模式
    if args.replace:
        old_url, new_url = args.replace
        fixer.find_and_replace_all(old_url, new_url, dry_run=not args.yes)
        return 0
    
    # 特定修复模式
    if args.file and args.line and args.new_url:
        file_path = base_path / args.file
        success = fixer.fix_specific_link(
            file_path, args.line, args.new_url,
            dry_run=not args.yes
        )
        return 0 if success else 1
    
    # 如果没有参数，显示帮助
    print("请指定操作或使用交互模式")
    parser.print_help()
    return 1


if __name__ == '__main__':
    sys.exit(main())
