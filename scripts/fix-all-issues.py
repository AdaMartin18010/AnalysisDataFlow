#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面问题修复脚本
修复内容：
1. 重复定理ID
2. 断裂锚点引用
3. 断裂链接
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class ComprehensiveFixer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.target_dirs = ['Struct', 'Knowledge', 'Flink']
        
        # 统计
        self.fixed_duplicate_ids = 0
        self.fixed_broken_links = 0
        self.fixed_broken_anchors = 0
        
        # 记录已使用的ID
        self.used_ids = set()
        self.id_counter = defaultdict(int)
        
    def scan_all_files(self):
        """扫描所有目标目录中的Markdown文件"""
        files = []
        for dir_name in self.target_dirs:
            dir_path = self.root_dir / dir_name
            if dir_path.exists():
                files.extend(dir_path.rglob('*.md'))
        return files
    
    def fix_duplicate_theorem_ids(self, files):
        """修复重复的定理ID"""
        print("🔧 修复重复定理ID...")
        
        # 收集所有ID
        id_locations = defaultdict(list)
        id_pattern = re.compile(r'(Def|Thm|Lemma|Prop|Cor)-([SFK])-(\d+)-(\d+)')
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for match in id_pattern.finditer(content):
                        full_id = match.group(0)
                        id_locations[full_id].append((file_path, match.start()))
            except Exception as e:
                print(f"  ⚠️ 读取文件失败 {file_path}: {e}")
        
        # 修复重复ID
        for full_id, locations in id_locations.items():
            if len(locations) > 1:
                # 保留第一个，其余修复
                for i, (file_path, pos) in enumerate(locations[1:], 1):
                    match = id_pattern.search(full_id)
                    if match:
                        type_prefix, stage, doc_num, seq = match.groups()
                        new_seq = int(seq) + i
                        new_id = f"{type_prefix}-{stage}-{doc_num}-{new_seq:02d}"
                        
                        # 确保新ID不重复
                        while new_id in id_locations or new_id in self.used_ids:
                            new_seq += 1
                            new_id = f"{type_prefix}-{stage}-{doc_num}-{new_seq:02d}"
                        
                        self.used_ids.add(new_id)
                        
                        # 替换文件中的ID
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            new_content = content.replace(full_id, new_id, 1)
                            if new_content != content:
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(new_content)
                                self.fixed_duplicate_ids += 1
                                print(f"  ✅ {file_path.name}: {full_id} -> {new_id}")
                        except Exception as e:
                            print(f"  ⚠️ 修复失败 {file_path}: {e}")
        
        print(f"✅ 修复了 {self.fixed_duplicate_ids} 个重复ID")
    
    def fix_broken_anchors(self, files):
        """修复断裂的锚点引用"""
        print("🔧 修复断裂锚点...")
        
        # 收集所有有效的锚点
        file_anchors = defaultdict(set)
        anchor_pattern = re.compile(r'\{#[\w\-\_.]+\}')
        header_pattern = re.compile(r'^(#{1,6})\s+(.+?)(?:\s+\{#[\w\-\_.]+\})?$')
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        # 显式锚点
                        for match in anchor_pattern.finditer(line):
                            anchor = match.group(0)[2:-1]
                            file_anchors[file_path].add(anchor.lower())
                        
                        # 标题锚点
                        header_match = header_pattern.match(line)
                        if header_match:
                            text = header_match.group(2)
                            # 生成多种变体
                            anchor = self.generate_anchor(text)
                            if anchor:
                                file_anchors[file_path].add(anchor.lower())
            except Exception as e:
                print(f"  ⚠️ 读取文件失败 {file_path}: {e}")
        
        print(f"✅ 收集了 {sum(len(v) for v in file_anchors.values())} 个锚点")
        
        # 修复断裂锚点引用
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                for match in link_pattern.finditer(content):
                    link_text = match.group(1)
                    link_target = match.group(2)
                    
                    if '#' in link_target and not link_target.startswith('#'):
                        # 文件锚点链接
                        parts = link_target.split('#')
                        target_path = parts[0]
                        anchor = parts[1] if len(parts) > 1 else ''
                        
                        # 解析目标文件路径
                        target_file = self.resolve_link(file_path, target_path)
                        if target_file and anchor:
                            # 检查锚点是否存在
                            anchor_lower = anchor.lower()
                            valid_anchors = file_anchors.get(target_file, set())
                            
                            if anchor_lower not in valid_anchors:
                                # 尝试找到最接近的锚点
                                best_match = self.find_best_anchor_match(anchor_lower, valid_anchors)
                                if best_match:
                                    new_link = f"{target_path}#{best_match}"
                                    old_link = link_target
                                    content = content.replace(f']({old_link})', f']({new_link})', 1)
                                    self.fixed_broken_anchors += 1
                                    print(f"  ✅ {file_path.name}: {old_link} -> {new_link}")
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                        
            except Exception as e:
                print(f"  ⚠️ 修复失败 {file_path}: {e}")
        
        print(f"✅ 修复了 {self.fixed_broken_anchors} 个断裂锚点")
    
    def generate_anchor(self, text):
        """生成锚点"""
        import re
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'[_\*`]', '', text)
        anchor = text.strip().lower()
        anchor = re.sub(r'\s+', '-', anchor)
        anchor = re.sub(r'[^\w\-\_.]', '-', anchor)
        anchor = re.sub(r'-+', '-', anchor)
        anchor = anchor.strip('-')
        return anchor
    
    def resolve_link(self, source_file, link_path):
        """解析链接路径到实际文件"""
        if link_path.startswith('/'):
            target = self.root_dir / link_path[1:]
        else:
            target = source_file.parent / link_path
        
        target = target.resolve()
        if target.exists():
            return target
        # 尝试添加.md后缀
        target_md = Path(str(target) + '.md')
        if target_md.exists():
            return target_md
        return None
    
    def find_best_anchor_match(self, anchor, valid_anchors):
        """找到最接近的锚点匹配"""
        if anchor in valid_anchors:
            return anchor
        
        # 清理锚点
        clean_anchor = re.sub(r'[^\w\-]', '', anchor)
        
        for valid in valid_anchors:
            clean_valid = re.sub(r'[^\w\-]', '', valid)
            if clean_anchor == clean_valid:
                return valid
            if clean_anchor in clean_valid or clean_valid in clean_anchor:
                return valid
        
        return None
    
    def fix_broken_links(self, files):
        """修复断裂的文件链接"""
        print("🔧 修复断裂链接...")
        
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)#]+)\)')
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                for match in link_pattern.finditer(content):
                    link_text = match.group(1)
                    link_target = match.group(2)
                    
                    if link_target.startswith('http'):
                        continue
                    
                    if '#' in link_target:
                        link_target = link_target.split('#')[0]
                    
                    if not link_target:
                        continue
                    
                    target_file = self.resolve_link(file_path, link_target)
                    if not target_file:
                        # 尝试修复
                        fixed = self.try_fix_link(file_path, link_target, files)
                        if fixed:
                            content = content.replace(f']({link_target})', f']({fixed})', 1)
                            self.fixed_broken_links += 1
                            print(f"  ✅ {file_path.name}: {link_target} -> {fixed}")
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                        
            except Exception as e:
                print(f"  ⚠️ 修复失败 {file_path}: {e}")
        
        print(f"✅ 修复了 {self.fixed_broken_links} 个断裂链接")
    
    def try_fix_link(self, source_file, broken_link, all_files):
        """尝试修复断裂链接"""
        # 提取文件名
        link_name = Path(broken_link).name
        if not link_name:
            return None
        
        link_name_lower = link_name.lower()
        if link_name_lower.endswith('.md'):
            link_name_lower = link_name_lower[:-3]
        
        # 在所有文件中搜索
        for f in all_files:
            f_name = f.name.lower()
            if f_name.endswith('.md'):
                f_name = f_name[:-3]
            
            if f_name == link_name_lower or link_name_lower in f_name:
                # 计算相对路径
                try:
                    rel_path = os.path.relpath(f, source_file.parent)
                    return rel_path.replace('\\', '/')
                except:
                    return str(f).replace('\\', '/')
        
        return None
    
    def run(self):
        """运行所有修复"""
        print("=" * 60)
        print("🚀 开始全面问题修复")
        print("=" * 60)
        
        files = self.scan_all_files()
        print(f"📁 扫描到 {len(files)} 个Markdown文件")
        print()
        
        # 1. 修复重复ID
        self.fix_duplicate_theorem_ids(files)
        print()
        
        # 2. 修复断裂链接
        self.fix_broken_links(files)
        print()
        
        # 3. 修复断裂锚点
        self.fix_broken_anchors(files)
        print()
        
        # 汇总
        print("=" * 60)
        print("📊 修复汇总")
        print("=" * 60)
        print(f"  重复ID修复: {self.fixed_duplicate_ids}")
        print(f"  断裂链接修复: {self.fixed_broken_links}")
        print(f"  断裂锚点修复: {self.fixed_broken_anchors}")
        print(f"  总计修复: {self.fixed_duplicate_ids + self.fixed_broken_links + self.fixed_broken_anchors}")
        print()

if __name__ == '__main__':
    fixer = ComprehensiveFixer('.')
    fixer.run()
