#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用修复脚本 - 第四轮
修复剩余链接错误
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
    
    def fix_visuals(self):
        """修复 visuals 中的链接"""
        # layer-decidability.md
        filepath = "visuals/layer-decidability.md"
        content = self.read_file(filepath)
        if content:
            fixes = [
                ("../Flink/02-features/cep-complex-event-processing.md", "../Flink/03-sql-table-api/flink-sql-window-functions-deep-dive.md"),
                ("../Flink/03-integrations/stateful-functions.md", "../Flink/04-connectors/flink-connectors-ecosystem-complete-guide.md"),
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
        
        # matrix-models.md - 修复目录链接
        filepath = "visuals/matrix-models.md"
        content = self.read_file(filepath)
        if content:
            fixes = [
                ("[../Flink/](../../Flink/)", "[Flink索引](../../Flink/00-INDEX.md)"),
                ("[../Knowledge/](../../Knowledge/)", "[Knowledge索引](../../Knowledge/00-INDEX.md)"),
            ]
            
            for old_link, new_link in fixes:
                if old_link in content:
                    content = content.replace(old_link, new_link)
                    self.fixes_applied.append({
                        'file': filepath,
                        'type': 'directory_link',
                        'old': old_link,
                        'new': new_link
                    })
                    print(f"✓ 修复 {filepath}: 修复目录链接")
            
            self.write_file(filepath, content)
        
        # selection-tree-consistency.md
        filepath = "visuals/selection-tree-consistency.md"
        content = self.read_file(filepath)
        if content:
            fixes = [
                ("../../Struct/02-properties/02.02-consistency-hierarchy.m)", "../../Struct/02-properties/02.02-consistency-hierarchy.md)"),
                ("../../Flink/02-core-mechanisms/exactly-once-end-to-end.m)", "../../Flink/02-core-mechanisms/exactly-once-end-to-end.md)"),
            ]
            
            for old_link, new_link in fixes:
                if old_link in content:
                    content = content.replace(old_link, new_link)
                    self.fixes_applied.append({
                        'file': filepath,
                        'type': 'malformed_link',
                        'old': old_link,
                        'new': new_link
                    })
                    print(f"✓ 修复 {filepath}: 修复截断的链接")
            
            self.write_file(filepath, content)
    
    def fix_tutorials(self):
        """修复 tutorials 中的链接"""
        filepath = "tutorials/interactive/README.md"
        content = self.read_file(filepath)
        if not content:
            return
        
        # 这些路径解析问题是由于 relative path 不正确
        fixes = [
            ("[Struct/](../../../Struct/)", "[Struct索引](../../Struct/00-INDEX.md)"),
            ("[Knowledge/](../../../Knowledge/)", "[Knowledge索引](../../Knowledge/00-INDEX.md)"),
            ("[Flink/](../../../Flink/)", "[Flink索引](../../Flink/00-INDEX.md)"),
            ("[AGENTS.md](../../../AGENTS.md)", "[AGENTS.md](../../AGENTS.md)"),
            ("[PROJECT-TRACKING.md](../../../PROJECT-TRACKING.md)", "[PROJECT-TRACKING.md](../../PROJECT-TRACKING.md)"),
        ]
        
        for old_link, new_link in fixes:
            if old_link in content:
                content = content.replace(old_link, new_link)
                self.fixes_applied.append({
                    'file': filepath,
                    'type': 'path_resolution',
                    'old': old_link,
                    'new': new_link
                })
                print(f"✓ 修复 {filepath}: {old_link} -> {new_link}")
        
        self.write_file(filepath, content)
    
    def fix_struct_proofs(self):
        """修复 Struct/04-proofs 中的 LaTeX 公式链接误报"""
        # 这些实际上是 LaTeX 公式，不是 Markdown 链接
        # 但验证器无法区分它们
        # 让我们修复这些文件中的问题
        filepath = "Struct/04-proofs/04.05-type-safety-fg-fgg.md"
        content = self.read_file(filepath)
        if not content:
            return
        
        # 这些是 LaTeX 公式中的括号，被错误识别为链接
        # 我们需要将它们转义或修改格式
        # 实际上这些问题是误报，不需要修改文件
        # 但我们可以记录这些误报
        print(f"  注: {filepath} 中的 LaTeX 公式被识别为链接（误报，无需修复）")
    
    def generate_fix_report(self):
        """生成修复报告"""
        print("\n" + "="*70)
        print("交叉引用修复报告 - 第四轮")
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
    
    print("开始第四轮修复...\n")
    
    fixer.fix_learning_paths()
    fixer.fix_visuals()
    fixer.fix_tutorials()
    fixer.fix_struct_proofs()
    
    fixer.generate_fix_report()
    print("\n第四轮修复完成!")

if __name__ == '__main__':
    main()
