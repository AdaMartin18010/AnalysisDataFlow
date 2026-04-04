#!/usr/bin/env python3
"""
锚点链接检查和修复脚本 v2
扫描所有Markdown文件，查找并修复锚点链接错误
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict
from urllib.parse import unquote, quote

class AnchorChecker:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.issues = []
        self.fixes = []
        self.files_data = {}
        self.verbose = True
        
    def slugify(self, text):
        """将标题转换为GitHub风格的锚点ID"""
        text = text.strip()
        text = text.lower()
        text = re.sub(r'[*_`#]+', '', text)
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        text = text.strip('-')
        return text
    
    def github_anchor(self, text):
        """GitHub风格的锚点生成"""
        # GitHub的锚点生成规则
        anchor = text.strip().lower()
        # 移除HTML标签
        anchor = re.sub(r'<[^>]+>', '', anchor)
        # 移除Markdown标记
        anchor = re.sub(r'[*_`#\[\]]+', '', anchor)
        # 替换空格为连字符
        anchor = re.sub(r'\s+', '-', anchor)
        # 移除特殊字符，但保留连字符
        anchor = re.sub(r'[^\w\u4e00-\u9fff\-]', '', anchor)
        # 移除首尾连字符
        anchor = anchor.strip('-')
        return anchor
    
    def extract_headings(self, content):
        """提取所有标题及其锚点"""
        headings = {}
        pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        for match in pattern.finditer(content):
            level = len(match.group(1))
            title = match.group(2).strip()
            # 生成多种可能的锚点格式
            anchor_github = self.github_anchor(title)
            anchor_slug = self.slugify(title)
            
            headings[anchor_github.lower()] = {
                'level': level,
                'title': title,
                'anchor_github': anchor_github,
                'anchor_slug': anchor_slug
            }
            # 也添加slug版本
            if anchor_slug.lower() != anchor_github.lower():
                headings[anchor_slug.lower()] = {
                    'level': level,
                    'title': title,
                    'anchor_github': anchor_github,
                    'anchor_slug': anchor_slug
                }
        return headings
    
    def extract_anchor_links(self, content, file_path):
        """提取所有锚点链接"""
        links = []
        pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        for match in pattern.finditer(content):
            link_text = match.group(1)
            link_target = match.group(2)
            
            # 跳过图片和外部链接
            if link_target.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                continue
                
            if '#' in link_target:
                parts = link_target.split('#', 1)
                file_path_part = parts[0]
                anchor = parts[1]
                links.append({
                    'text': link_text,
                    'target': link_target,
                    'file': file_path_part,
                    'anchor': anchor,
                    'full_match': match.group(0),
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
        links = self.extract_anchor_links(content, file_path)
        
        self.files_data[str(file_path)] = {
            'headings': headings,
            'links': links,
            'content': content,
            'path': file_path
        }
    
    def check_links(self):
        """检查所有链接的有效性"""
        for file_path, data in self.files_data.items():
            for link in data['links']:
                self.validate_link(file_path, link)
    
    def normalize_anchor(self, anchor):
        """规范化锚点用于比较"""
        # URL解码
        decoded = unquote(anchor)
        # 转小写
        decoded = decoded.lower()
        # 替换空格为连字符
        decoded = decoded.replace(' ', '-')
        # 移除多余连字符
        decoded = re.sub(r'-+', '-', decoded)
        decoded = decoded.strip('-')
        return decoded
    
    def validate_link(self, source_file, link):
        """验证单个链接"""
        target_file = link['file']
        anchor = link['anchor']
        
        # 规范化锚点
        normalized_anchor = self.normalize_anchor(anchor)
        
        if not target_file:
            # 内部链接
            target_path = source_file
        else:
            # 解析目标文件路径
            source_dir = Path(source_file).parent
            target_path = source_dir / target_file
            
            # 尝试不同扩展名
            possible_paths = [
                str(target_path),
                str(target_path) + '.md',
                str(target_path.with_suffix('.md'))
            ]
            
            found = False
            for p in possible_paths:
                abs_p = str(Path(p).resolve())
                if abs_p in self.files_data:
                    target_path = abs_p
                    found = True
                    break
            
            if not found:
                self.issues.append({
                    'type': 'file_not_found',
                    'source': source_file,
                    'target': target_file,
                    'anchor': anchor,
                    'link_text': link['text'],
                    'full_match': link['full_match']
                })
                return
        
        # 检查锚点
        target_data = self.files_data.get(str(target_path))
        if not target_data:
            return
        
        headings = target_data['headings']
        
        # 检查各种可能的匹配
        found_match = None
        for heading_key in headings.keys():
            if heading_key == normalized_anchor:
                found_match = heading_key
                break
            # 检查原始锚点（不规范化）
            if heading_key == anchor.lower():
                found_match = heading_key
                break
        
        if not found_match:
            # 尝试模糊匹配
            best_match = self.find_best_match(normalized_anchor, list(headings.keys()))
            self.issues.append({
                'type': 'anchor_not_found',
                'source': source_file,
                'target': target_file or '(same file)',
                'anchor': anchor,
                'normalized_anchor': normalized_anchor,
                'link_text': link['text'],
                'full_match': link['full_match'],
                'suggested_fix': best_match,
                'available_headings': list(headings.keys())[:5]  # 前5个可用标题
            })
    
    def find_best_match(self, anchor, available_headings):
        """找到最匹配的锚点"""
        anchor_clean = anchor.replace('-', '').replace('_', '')
        
        # 首先尝试完全匹配（忽略大小写）
        for heading in available_headings:
            if heading.lower() == anchor.lower():
                return heading
        
        # 尝试清理后的匹配
        for heading in available_headings:
            heading_clean = heading.replace('-', '').replace('_', '')
            if heading_clean.lower() == anchor_clean.lower():
                return heading
        
        # 尝试部分匹配
        for heading in available_headings:
            if anchor_clean in heading.replace('-', '').replace('_', '').lower():
                return heading
            if heading.replace('-', '').replace('_', '').lower() in anchor_clean:
                return heading
        
        return None
    
    def fix_anchor_links(self):
        """修复锚点链接"""
        fixed_count = 0
        files_modified = set()
        
        # 按文件分组问题
        file_issues = defaultdict(list)
        for issue in self.issues:
            if issue['type'] == 'anchor_not_found' and issue.get('suggested_fix'):
                file_issues[issue['source']].append(issue)
        
        for source_file, issues in file_issues.items():
            if self.fix_file_anchors(source_file, issues):
                fixed_count += len(issues)
                files_modified.add(source_file)
        
        return fixed_count, len(files_modified)
    
    def fix_file_anchors(self, file_path, issues):
        """修复单个文件中的多个锚点"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            for issue in issues:
                wrong_anchor = issue['anchor']
                correct_anchor = issue['suggested_fix']
                
                if wrong_anchor == correct_anchor:
                    continue
                
                # 构建替换模式
                # 需要小心处理，只替换链接中的锚点
                patterns = [
                    (f"](#{wrong_anchor})", f"](#{correct_anchor})"),
                    (f"](#{unquote(wrong_anchor)})", f"](#{correct_anchor})"),
                ]
                
                for old, new in patterns:
                    if old in content:
                        content = content.replace(old, new)
                        self.fixes.append({
                            'file': file_path,
                            'old': wrong_anchor,
                            'new': correct_anchor,
                            'context': issue['link_text'][:50]
                        })
                        break
            
            if content != original_content:
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
        print("锚点链接检查工具 v2")
        print("=" * 80)
        
        # 1. 扫描所有文件
        print("\n[1/4] 扫描所有Markdown文件...")
        md_files = list(self.root_dir.rglob('*.md'))
        print(f"发现 {len(md_files)} 个Markdown文件")
        
        for i, file_path in enumerate(md_files, 1):
            if i % 100 == 0:
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
            print("\n  锚点问题详情 (前30个):")
            for issue in anchor_issues[:30]:
                source_name = Path(issue['source']).name
                print(f"    {source_name} -> #{issue['anchor']}")
                if issue.get('suggested_fix'):
                    print(f"      建议: #{issue['suggested_fix']}")
                if self.verbose and issue.get('available_headings'):
                    print(f"      可用: {issue['available_headings']}")
            if len(anchor_issues) > 30:
                print(f"    ... 还有 {len(anchor_issues) - 30} 个问题")
        
        # 4. 修复问题
        print("\n[4/4] 修复锚点链接...")
        fixed, files_modified = self.fix_anchor_links()
        print(f"  修复了 {fixed} 个锚点链接 (涉及 {files_modified} 个文件)")
        
        # 5. 汇总
        print("\n" + "=" * 80)
        print("检查完成!")
        print("=" * 80)
        
        if self.fixes:
            print("\n修复详情 (前20个):")
            for fix in self.fixes[:20]:
                print(f"  {Path(fix['file']).name}:")
                print(f"    #{fix['old']} -> #{fix['new']}")
        
        return fixed, len(anchor_issues)


def main():
    root_dir = "E:\\_src\\AnalysisDataFlow"
    checker = AnchorChecker(root_dir)
    fixed_count, total_issues = checker.run()
    print(f"\n总计: 发现 {total_issues} 个问题, 修复了 {fixed_count} 个锚点链接")
    return fixed_count


if __name__ == "__main__":
    count = main()
    sys.exit(0)
