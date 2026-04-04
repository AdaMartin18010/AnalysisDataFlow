#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用修复脚本 - 第三轮
修复更多链接错误
"""

import os
import re
from pathlib import Path

class CrossRefFixer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.fixes_applied = []
        
    def read_file(self, filepath):
        """读取文件内容"""
        full_path = self.base_dir / filepath
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"读取文件 {filepath} 失败: {e}")
            return None
    
    def write_file(self, filepath, content):
        """写入文件内容"""
        full_path = self.base_dir / filepath
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"写入文件 {filepath} 失败: {e}")
            return False
    
    def fix_toolchain_md(self):
        """修复 TOOLCHAIN.md 中的链接"""
        filepath = "TOOLCHAIN.md"
        content = self.read_file(filepath)
        if not content:
            return
        
        # 第313行的链接文本格式问题
        old_link = "[text](path/to/file.md)"
        new_link = "[text](Flink/00-INDEX.md)"
        
        if old_link in content:
            content = content.replace(old_link, new_link)
            if self.write_file(filepath, content):
                self.fixes_applied.append({
                    'file': filepath,
                    'type': 'placeholder_link',
                    'old': old_link,
                    'new': new_link
                })
                print(f"✓ 修复 {filepath}: {old_link} -> {new_link}")
    
    def fix_flink_00_index(self):
        """修复 Flink/00-INDEX.md 中的链接"""
        filepath = "Flink/00-INDEX.md"
        content = self.read_file(filepath)
        if not content:
            return
        
        fixes = [
            ("01-architecture/flink-24-performance-improvements.md", "06-engineering/flink-24-performance-improvements.md"),
            ("13-wasm/flink-25-wasm-udf-ga.md", "09-language-foundations/flink-25-wasm-udf-ga.md"),
        ]
        
        for old_link, new_link in fixes:
            if old_link in content:
                content = content.replace(old_link, new_link)
                self.fixes_applied.append({
                    'file': filepath,
                    'type': 'file_not_found',
                    'old': old_link,
                    'new': new_link
                })
                print(f"✓ 修复 {filepath}: {old_link} -> {new_link}")
        
        self.write_file(filepath, content)
    
    def fix_learning_paths(self):
        """修复 LEARNING-PATHS 中的链接"""
        filepath = "LEARNING-PATHS/data-engineer-path.md"
        content = self.read_file(filepath)
        if not content:
            return
        
        # 第71行链接有截断问题
        old_link = "[Flink/02-core-mechanisms/state-backend-selection.m](../Flink/02-core-mechanisms/state-backend-selection.md)"
        new_link = "[state-backend-selection.md](../Flink/06-engineering/state-backend-selection.md)"
        
        if old_link in content:
            content = content.replace(old_link, new_link)
            if self.write_file(filepath, content):
                self.fixes_applied.append({
                    'file': filepath,
                    'type': 'malformed_link',
                    'old': old_link,
                    'new': new_link
                })
                print(f"✓ 修复 {filepath}: 修复截断的链接")
    
    def fix_tech_radar(self):
        """修复 TECH-RADAR 中的链接"""
        # 修复 decision-tree.md
        filepath = "TECH-RADAR/decision-tree.md"
        content = self.read_file(filepath)
        if content:
            old_link = "[decision-helper.html](./visuals/decision-helper.html)"
            new_link = "[selection-tree-streaming.md](../visuals/selection-tree-streaming.md)"
            
            if old_link in content:
                content = content.replace(old_link, new_link)
                if self.write_file(filepath, content):
                    self.fixes_applied.append({
                        'file': filepath,
                        'type': 'file_not_found',
                        'old': old_link,
                        'new': new_link
                    })
                    print(f"✓ 修复 {filepath}: {old_link} -> {new_link}")
        
        # 修复 README.md
        filepath = "TECH-RADAR/README.md"
        content = self.read_file(filepath)
        if content:
            fixes = [
                ("../Flink/02-core-mechanisms/disaggregated-state-analysis.md", "../Flink/01-architecture/disaggregated-state-analysis.md"),
                ("../Flink/06-frontier/serverless-stream-processing-architecture.md", "../Knowledge/06-frontier/serverless-stream-processing-architecture.md"),
            ]
            
            for old_link, new_link in fixes:
                if old_link in content:
                    content = content.replace(old_link, new_link)
                    self.fixes_applied.append({
                        'file': filepath,
                        'type': 'file_not_found',
                        'old': old_link,
                        'new': new_link
                    })
                    print(f"✓ 修复 {filepath}: {old_link} -> {new_link}")
            
            self.write_file(filepath, content)
    
    def fix_visuals(self):
        """修复 visuals 中的链接"""
        fixes_map = {
            "visuals/index-visual.md": [
                ("Knowledge/06-frontier/streaming-graph-tgn.md", "Knowledge/06-frontier/streaming-graph-processing-tgn.md"),
            ],
            "visuals/layer-decidability.md": [
                ("../Knowledge/05-patterns/saga-pattern.md", "../Knowledge/02-design-patterns/pattern-async-io-enrichment.md"),
                ("../Knowledge/04-engineering/streaming-systems-design.md", "../Knowledge/04-technology-selection/engine-selection-guide.md"),
                ("../Knowledge/06-frontier/llm-agent-architecture.md", "../Knowledge/06-frontier/ai-agent-streaming-architecture.md"),
                ("../Flink/01-core/checkpoint-mechanism.md", "../Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md"),
                ("../Flink/01-core/watermark-mechanism.md", "../Flink/02-core-mechanisms/time-semantics-and-watermark.md"),
            ],
        }
        
        for filepath, fixes in fixes_map.items():
            content = self.read_file(filepath)
            if not content:
                continue
            
            for old_link, new_link in fixes:
                if old_link in content:
                    content = content.replace(old_link, new_link)
                    self.fixes_applied.append({
                        'file': filepath,
                        'type': 'file_not_found',
                        'old': old_link,
                        'new': new_link
                    })
                    print(f"✓ 修复 {filepath}: {old_link} -> {new_link}")
            
            self.write_file(filepath, content)
    
    def generate_fix_report(self):
        """生成修复报告"""
        print("\n" + "="*70)
        print("交叉引用修复报告 - 第三轮")
        print("="*70)
        print(f"\n总修复数: {len(self.fixes_applied)}")
        
        if self.fixes_applied:
            print("\n修复详情:")
            for fix in self.fixes_applied:
                print(f"  - {fix['file']}: {fix['old']} -> {fix['new']}")
        
        return self.fixes_applied

def main():
    base_dir = Path(__file__).parent.parent
    fixer = CrossRefFixer(base_dir)
    
    print("开始第三轮修复...\n")
    
    fixer.fix_toolchain_md()
    fixer.fix_flink_00_index()
    fixer.fix_learning_paths()
    fixer.fix_tech_radar()
    fixer.fix_visuals()
    
    fixer.generate_fix_report()
    print("\n第三轮修复完成!")

if __name__ == '__main__':
    main()
