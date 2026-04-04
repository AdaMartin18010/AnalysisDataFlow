#!/usr/bin/env python3
"""
锚点链接检查和修复脚本
扫描所有Markdown文件，查找并修复锚点链接错误
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict
from urllib.parse import unquote

class AnchorChecker:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.issues = []
        self.fixes = []
        self.files_data = {}  # 存储每个文件的标题和链接信息
        
    def slugify(self, text):
        """将标题转换为GitHub风格的锚点ID"""
        # 移除首尾空白
        text = text.strip()
        # 转换为小写
        text = text.lower()
        # 移除Markdown标记（如**粗体**、*斜体*等）
        text = re.sub(r'[*_`#]+', '', text)
        # 替换特殊字符为空格
        text = re.sub(r'[^\w\s-]', '', text)
        # 替换空格和多个连字符为单个连字符
        text = re.sub(r'[-\s]+', '-', text)
        # 移除首尾连字符
        text = text.strip('-')
        return text
    
    def extract_headings(self, content):
        """提取所有标题及其锚点"""
        headings = {}
        # 匹配Markdown标题: ## 标题内容
        pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        for match in pattern.finditer(content):
            level = len(match.group(1))
            title = match.group(2).strip()
            anchor = self.slugify(title)
            if anchor:
                headings[anchor] = {
                    'level': level,
                    'title': title,
                    'anchor': anchor
                }
        return headings
    
    def extract_anchor_links(self, content):
        """提取所有锚点链接 [text](#anchor) 或 [text](./file.md#anchor)"""
        links = []
        # 匹配锚点链接
        pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        for match in pattern.finditer(content):
            link_text = match.group(1)
            link_target = match.group(2)
            # 只处理锚点链接
            if '#' in link_target:
                parts = link_target.split('#', 1)
                file_path = parts[0]
                anchor = parts[1]
                links.append({
                    'text': link_text,
                    'target': link_target,
                    'file': file_path,
                    'anchor': anchor,
                    'pos': match.start()
                })
        return links
    
    def scan_file(self, file_path):
        """扫描单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return
        
        headings = self.extract_headings(content)
        links = self.extract_anchor_links(content)
        
        self.files_data[file_path] = {
            'headings': headings,
            'links': links,
            'content': content
        }
    
    def check_links(self):
        """检查所有链接的有效性"""
        for file_path, data in self.files_data.items():
            for link in data['links']:
                self.validate_link(file_path, link)
    
    def validate_link(self, source_file, link):
        """验证单个链接"""
        target_file = link['file']
        anchor = link['anchor']
        
        # URL解码锚点
        decoded_anchor = unquote(anchor)
        
        if not target_file:
            # 内部链接
            target_path = source_file
        else:
            # 外部文件链接
            target_path = (Path(source_file).parent / target_file).resolve()
            if str(target_path) not in self.files_data:
                # 尝试添加.md后缀
                target_path_md = str(target_path) + '.md'
                if target_path_md in self.files_data:
                    target_path = target_path_md
                else:
                    self.issues.append({
                        'type': 'file_not_found',
                        'source': source_file,
                        'target': target_file,
                        'anchor': anchor,
                        'link_text': link['text']
                    })
                    return
        
        # 检查锚点是否存在
        target_data = self.files_data.get(str(target_path))
        if not target_data:
            return
        
        headings = target_data['headings']
        
        # 检查锚点是否匹配
        if decoded_anchor.lower() not in [h.lower() for h in headings.keys()]:
            # 尝试找到匹配的锚点
            best_match = self.find_best_match(decoded_anchor, headings.keys())
            self.issues.append({
                'type': 'anchor_not_found',
                'source': source_file,
                'target': target_file or '(same file)',
                'anchor': anchor,
                'decoded_anchor': decoded_anchor,
                'link_text': link['text'],
                'suggested_fix': best_match
            })
    
    def find_best_match(self, anchor, available_headings):
        """找到最匹配的锚点"""
        anchor_lower = anchor.lower()
        
        for heading in available_headings:
            if heading.lower() == anchor_lower:
                return heading
        
        # 尝试忽略连字符/空格差异
        anchor_normalized = anchor_lower.replace('-', '').replace(' ', '')
        for heading in available_headings:
            heading_normalized = heading.lower().replace('-', '').replace(' ', '')
            if heading_normalized == anchor_normalized:
                return heading
        
        return None
    
    def fix_anchor_links(self):
        """修复锚点链接"""
        fixed_count = 0
        
        for issue in self.issues:
            if issue['type'] != 'anchor_not_found':
                continue
            
            if not issue.get('suggested_fix'):
                continue
            
            source_file = issue['source']
            wrong_anchor = issue['anchor']
            correct_anchor = issue['suggested_fix']
            
            if wrong_anchor == correct_anchor:
                continue
            
            # 修复文件
            if self.fix_file_anchor(source_file, wrong_anchor, correct_anchor):
                fixed_count += 1
                self.fixes.append({
                    'file': source_file,
                    'old': wrong_anchor,
                    'new': correct_anchor,
                    'context': issue['link_text']
                })
        
        return fixed_count
    
    def fix_file_anchor(self, file_path, old_anchor, new_anchor):
        """修复单个文件中的锚点"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换锚点链接 (需要小心处理，只替换链接中的锚点)
            # 模式: ](...#old_anchor) 或 ](...#old_anchor)
            old_pattern = f"](#{old_anchor})"
            new_pattern = f"](#{new_anchor})"
            
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            
            # 尝试URL解码后的匹配
            old_decoded = unquote(old_anchor)
            if old_decoded != old_anchor:
                old_pattern = f"](#{old_decoded})"
                if old_pattern in content:
                    content = content.replace(old_pattern, new_pattern)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    return True
            
            return False
        except Exception as e:
            print(f"Error fixing {file_path}: {e}")
            return False
    
    def run(self):
        """运行完整的检查和修复流程"""
        print("=" * 80)
        print("锚点链接检查工具")
        print("=" * 80)
        
        # 1. 扫描所有文件
        print("\n[1/4] 扫描所有Markdown文件...")
        md_files = list(self.root_dir.rglob('*.md'))
        print(f"发现 {len(md_files)} 个Markdown文件")
        
        for i, file_path in enumerate(md_files, 1):
            if i % 50 == 0:
                print(f"  进度: {i}/{len(md_files)}")
            self.scan_file(file_path)
        
        # 2. 检查链接
        print("\n[2/4] 检查锚点链接...")
        self.check_links()
        
        # 3. 报告问题
        print("\n[3/4] 问题报告:")
        anchor_issues = [i for i in self.issues if i['type'] == 'anchor_not_found']
        file_issues = [i for i in self.issues if i['type'] == 'file_not_found']
        
        print(f"  - 锚点不存在: {len(anchor_issues)} 个")
        print(f"  - 文件不存在: {len(file_issues)} 个")
        
        if anchor_issues:
            print("\n  锚点问题详情:")
            for issue in anchor_issues[:20]:  # 只显示前20个
                print(f"    {Path(issue['source']).name} -> #{issue['anchor']}")
                if issue.get('suggested_fix'):
                    print(f"      建议修复: #{issue['suggested_fix']}")
            if len(anchor_issues) > 20:
                print(f"    ... 还有 {len(anchor_issues) - 20} 个问题")
        
        # 4. 修复问题
        print("\n[4/4] 修复锚点链接...")
        fixed = self.fix_anchor_links()
        print(f"  修复了 {fixed} 个锚点链接")
        
        # 5. 汇总
        print("\n" + "=" * 80)
        print("修复完成!")
        print("=" * 80)
        
        if self.fixes:
            print("\n修复详情:")
            for fix in self.fixes:
                print(f"  {Path(fix['file']).name}: #{fix['old']} -> #{fix['new']}")
        
        return fixed


def main():
    root_dir = "E:\\_src\\AnalysisDataFlow"
    checker = AnchorChecker(root_dir)
    fixed_count = checker.run()
    return fixed_count


if __name__ == "__main__":
    count = main()
    print(f"\n总计修复: {count} 个锚点链接")
    sys.exit(0)
