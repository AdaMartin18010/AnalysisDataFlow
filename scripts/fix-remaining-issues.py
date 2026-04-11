#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复剩余的真实问题
"""

import os
import re
from pathlib import Path
from collections import defaultdict


class FixRemainingIssues:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.target_dirs = ['Struct', 'Knowledge', 'Flink']
        self.all_files = {}
        
    def scan_files(self):
        """扫描文件"""
        for dir_name in self.target_dirs:
            dir_path = self.root_dir / dir_name
            if dir_path.exists():
                for md_file in dir_path.rglob('*.md'):
                    rel_path = str(md_file.relative_to(self.root_dir)).replace('\\', '/')
                    self.all_files[rel_path] = md_file
                    self.all_files[rel_path.replace('.md', '')] = md_file
        
    def fix_common_patterns(self):
        """修复常见问题模式"""
        print("🔧 修复常见问题...")
        
        fixes = []
        
        # 常见修复模式
        patterns = [
            # Knowledge/case-studies 目录结构问题
            (r'Knowledge/case-studies/realtime-anti-fraud', 'Knowledge/case-studies/fraud-detection-production-case', '反欺诈案例路径修复'),
            (r'Knowledge/case-studies/realtime-game-analytics', 'Knowledge/case-studies/gaming-analytics-platform-case', '游戏分析案例路径修复'),
            (r'10-case-studies/ecommerce/', 'Knowledge/case-studies/', '电商案例路径修复'),
            (r'10-case-studies/iot/', 'Knowledge/case-studies/', 'IoT案例路径修复'),
            
            # Struct 目录结构问题
            (r'Struct/05-foundations/05\.03-streaming-dataflow-equivalence', 'Struct/01-foundation/01.04-dataflow-model-formalization', 'Dataflow等价性文档路径修复'),
            (r'Struct/Flink/', 'Flink/', 'Struct/Flink路径修复'),
            (r'Struct/Knowledge/', 'Knowledge/', 'Struct/Knowledge路径修复'),
            
            # Flink 目录结构问题
            (r'Flink/02-core-mechanisms/', 'Flink/02-core/', '核心机制目录修复'),
            (r'Flink/07-case-studies/', 'Flink/09-practices/09.01-case-studies/', '案例研究目录修复'),
            (r'Flink/06-engineering/', 'Flink/09-practices/09.03-performance-tuning/', '工程实践目录修复'),
            
            # 版本目录问题
            (r'flink-24/', 'Flink/08-roadmap/08.01-flink-24/', 'Flink 2.4路径修复'),
            (r'flink-25/', 'Flink/08-roadmap/08.02-flink-25/', 'Flink 2.5路径修复'),
            (r'flink-30/', 'Flink/08-roadmap/08.03-flink-30/', 'Flink 3.0路径修复'),
            
            # 元文档路径问题
            (r'\./GLOSSARY-EN\.md', './GLOSSARY.md', '英文词汇表路径修复'),
            (r'\./LEARNING-PATHS-DYNAMIC\.md', './LEARNING-PATHS/00-INDEX.md', '学习路径路径修复'),
        ]
        
        for rel_path, file_path in self.all_files.items():
            if not str(file_path).endswith('.md'):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                for old_pattern, new_pattern, description in patterns:
                    if old_pattern in content:
                        content = re.sub(old_pattern, new_pattern, content)
                        if content != original_content:
                            fixes.append({
                                'file': str(file_path),
                                'description': description,
                                'pattern': old_pattern
                            })
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                        
            except Exception as e:
                pass
        
        print(f"✅ 修复了 {len(fixes)} 处常见问题")
        return fixes
    
    def add_missing_anchors(self):
        """为缺失的锚点添加显式定义"""
        print("🔧 添加缺失锚点...")
        
        anchor_fixes = []
        
        # 常见缺失锚点映射
        anchor_mappings = {
            # 文件 -> 需要添加的锚点列表
            'Flink/00-FLINK-TECH-STACK-DEPENDENCY.md': [
                ('#关系-1-core--api-支撑关系', '## 关系 1: Core → API 支撑关系'),
                ('#关系-2-api--runtime-依赖关系', '## 关系 2: API → Runtime 依赖关系'),
                ('#61-core--api-依赖实例', '### 6.1 Core → API 依赖实例'),
            ],
            'Flink/02-core/checkpoint-mechanism-deep-dive.md': [
                ('#def-f-02-01-checkpoint-核心抽象', '## Def-F-02-01 (Checkpoint 核心抽象)'),
                ('#lemma-f-02-01-barrier-对齐保证状态一致性', '## Lemma-F-02-01 (Barrier 对齐保证状态一致性)'),
            ],
        }
        
        for file_rel, anchors in anchor_mappings.items():
            file_path = self.root_dir / file_rel
            if not file_path.exists():
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                for anchor_id, target_heading in anchors:
                    anchor_name = anchor_id.lstrip('#')
                    # 检查锚点是否已存在
                    if f'{{#{anchor_name}}}' not in content:
                        # 在目标标题后添加锚点
                        pattern = re.escape(target_heading)
                        replacement = f'{target_heading} {{{anchor_name}}}'
                        content = re.sub(pattern, replacement, content)
                        anchor_fixes.append({
                            'file': str(file_path),
                            'anchor': anchor_name
                        })
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                        
            except Exception as e:
                pass
        
        print(f"✅ 添加了 {len(anchor_fixes)} 个缺失锚点")
        return anchor_fixes
    
    def fix_relative_paths(self):
        """修复相对路径问题"""
        print("🔧 修复相对路径...")
        
        path_fixes = []
        
        for rel_path, file_path in self.all_files.items():
            if not str(file_path).endswith('.md'):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                file_dir = Path(file_path).parent
                
                # 查找所有相对路径链接
                link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')
                
                for match in link_pattern.finditer(original_content):
                    link_text = match.group(1)
                    link_path = match.group(2)
                    
                    # 跳过外部链接和绝对路径
                    if link_path.startswith(('http://', 'https://', '/', '#')):
                        continue
                    
                    # 解析目标路径
                    target = file_dir / link_path
                    
                    # 如果目标不存在，尝试修复
                    if not target.exists():
                        # 尝试添加.md
                        if not str(target).endswith('.md'):
                            target = Path(str(target) + '.md')
                        
                        if not target.exists():
                            # 查找可能的正确路径
                            target_name = Path(link_path).name
                            for known_path, known_file in self.all_files.items():
                                if known_path.endswith('/' + target_name) or known_path.endswith('/' + target_name + '.md'):
                                    # 计算新的相对路径
                                    try:
                                        new_rel = os.path.relpath(known_file, file_dir).replace('\\', '/')
                                        old_pattern = f']({link_path})'
                                        new_pattern = f']({new_rel})'
                                        content = content.replace(old_pattern, new_pattern, 1)
                                        path_fixes.append({
                                            'file': str(file_path),
                                            'old': link_path,
                                            'new': new_rel
                                        })
                                    except:
                                        pass
                                    break
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                        
            except Exception as e:
                pass
        
        print(f"✅ 修复了 {len(path_fixes)} 个路径问题")
        return path_fixes
    
    def run(self):
        """运行修复流程"""
        print("=" * 60)
        print("🔧 修复剩余问题")
        print("=" * 60)
        
        self.scan_files()
        
        fixes1 = self.fix_common_patterns()
        fixes2 = self.add_missing_anchors()
        fixes3 = self.fix_relative_paths()
        
        total_fixes = len(fixes1) + len(fixes2) + len(fixes3)
        
        print("=" * 60)
        print(f"✅ 共修复 {total_fixes} 个问题")
        print("=" * 60)
        
        return total_fixes


if __name__ == '__main__':
    fixer = FixRemainingIssues('.')
    fixer.run()
