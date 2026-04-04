#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用修复脚本 - 第五轮（最终轮）
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
        
        # 尝试找到并修复截断的链接
        # 原始链接文本: [Flink/02-core-mechanisms/state-backend-selection.m](../Flink/02-core-mechanisms/state-backend-selection.md)
        # 模式: .m](../ 应该是 .md](../
        if ".m](../" in content:
            content = content.replace(".m](../", ".md](..")
            if self.write_file(filepath, content):
                self.fixes_applied.append({
                    'file': filepath,
                    'type': 'malformed_link',
                    'description': '修复.m到.md的链接截断'
                })
                print(f"✓ 修复 {filepath}: 修复.m到.md的链接截断")
    
    def fix_visuals(self):
        """修复 visuals 中的链接"""
        # matrix-models.md - 修复相对路径
        filepath = "visuals/matrix-models.md"
        content = self.read_file(filepath)
        if content:
            # 使用正确的相对路径
            old1 = "[Flink索引](../../Flink/00-INDEX.md)"
            new1 = "[Flink索引](../Flink/00-INDEX.md)"
            old2 = "[Knowledge索引](../../Knowledge/00-INDEX.md)"
            new2 = "[Knowledge索引](../Knowledge/00-INDEX.md)"
            
            if old1 in content:
                content = content.replace(old1, new1)
            if old2 in content:
                content = content.replace(old2, new2)
            
            if self.write_file(filepath, content):
                self.fixes_applied.append({
                    'file': filepath,
                    'type': 'path_fix',
                    'description': '修复相对路径'
                })
                print(f"✓ 修复 {filepath}: 修复相对路径")
        
        # selection-tree-consistency.md
        filepath = "visuals/selection-tree-consistency.md"
        content = self.read_file(filepath)
        if content:
            if ".m)]" in content:
                content = content.replace(".m)]", ".md)]")
                if self.write_file(filepath, content):
                    self.fixes_applied.append({
                        'file': filepath,
                        'type': 'malformed_link',
                        'description': '修复.m到.md的链接截断'
                    })
                    print(f"✓ 修复 {filepath}: 修复.m到.md的链接截断")
    
    def fix_knowledge_files(self):
        """修复 Knowledge 文件中的截断链接"""
        # concurrency-paradigms-matrix.md
        filepath = "Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md"
        content = self.read_file(filepath)
        if content:
            # 修复截断的链接 [../Struct/05-comparative-analysis/05.01-go-vs-scal]
            if "05.01-go-vs-scal](../" in content:
                content = content.replace("05.01-go-vs-scal](..", "05.01-go-vs-scala-expressiveness](..")
                if self.write_file(filepath, content):
                    self.fixes_applied.append({
                        'file': filepath,
                        'type': 'malformed_link',
                        'description': '修复截断的链接'
                    })
                    print(f"✓ 修复 {filepath}: 修复截断的链接")
        
        # streaming-models-mindmap.md
        filepath = "Knowledge/01-concept-atlas/streaming-models-mindmap.md"
        content = self.read_file(filepath)
        if content:
            # 修复截断的链接 [../../Struct/01-foundation/01.01-process-calculi-o]
            if "01.01-process-calculi-o](../../" in content:
                content = content.replace("01.01-process-calculi-o](../..", "01.01-unified-streaming-theory](..")
                if self.write_file(filepath, content):
                    self.fixes_applied.append({
                        'file': filepath,
                        'type': 'malformed_link',
                        'description': '修复截断的链接和文件名'
                    })
                    print(f"✓ 修复 {filepath}: 修复截断的链接和文件名")
    
    def generate_fix_report(self):
        """生成修复报告"""
        print("\n" + "="*70)
        print("交叉引用修复报告 - 第五轮（最终轮）")
        print("="*70)
        print(f"\n总修复数: {len(self.fixes_applied)}")
        
        if self.fixes_applied:
            print("\n修复详情:")
            for fix in self.fixes_applied:
                print(f"  - {fix['file']}: {fix.get('description', fix.get('old', 'unknown'))}")
        
        return self.fixes_applied

def main():
    base_dir = Path(__file__).parent.parent
    fixer = CrossRefFixer(base_dir)
    
    print("开始第五轮修复（最终轮）...\n")
    
    fixer.fix_learning_paths()
    fixer.fix_visuals()
    fixer.fix_knowledge_files()
    
    fixer.generate_fix_report()
    print("\n第五轮修复完成!")

if __name__ == '__main__':
    main()
