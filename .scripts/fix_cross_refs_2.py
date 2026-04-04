#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用修复脚本 - 第二轮
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
    
    def fix_readme_md(self):
        """修复 README.md 中的链接"""
        filepath = "README.md"
        content = self.read_file(filepath)
        if not content:
            return
        
        fixes = [
            ("Flink/12-ai-ml/flink-ai-agents-ga.md", "Flink/12-ai-ml/flip-531-ai-agents-ga-guide.md"),
            ("Flink/10-deployment/serverless-flink-complete-guide.md", "Flink/10-deployment/serverless-flink-ga-guide.md"),
            ("Flink/01-architecture/flink-2.3-roadmap.md", "Flink/08-roadmap/flink-2.3-2.4-roadmap.md"),
            ("Flink/12-ai-ml/tgn-temporal-graph-networks.md", "Flink/14-graph/flink-gelly-streaming-graph-processing.md"),
            ("Flink/12-ai-ml/multimodal-streaming-processing.md", "Knowledge/06-frontier/multimodal-streaming-architecture.md"),
            ("Struct/06-frontier/smart-casual-verification.md", "Struct/07-tools/smart-casual-verification.md"),
            ("Flink/05-vs-competitors/flink-vs-risingwave-modern-streaming.md", "Knowledge/04-technology-selection/flink-vs-risingwave.md"),
            ("Knowledge/07-architecture-patterns/temporal-flink-layered-architecture.md", "Knowledge/06-frontier/temporal-flink-layered-architecture.md"),
            ("Flink/06-engineering/serverless-streaming-cost-optimization.md", "Flink/10-deployment/serverless-flink-ga-guide.md"),
            ("Flink/13-security/streaming-data-security-compliance.md", "Knowledge/08-standards/streaming-security-compliance.md"),
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
    
    def fix_best_practices_md(self):
        """修复 BEST-PRACTICES.md 中的错误链接"""
        filepath = "BEST-PRACTICES.md"
        content = self.read_file(filepath)
        if not content:
            return
        
        # 修复拼接在一起的文件路径
        old_link = "Knowledge/07-best-practices/07.01-flink-production-checklist.md07.02-performance-tuning-patterns.md"
        new_link = "Knowledge/07-best-practices/07.02-performance-tuning-patterns.md"
        
        if old_link in content:
            content = content.replace(old_link, new_link)
            if self.write_file(filepath, content):
                self.fixes_applied.append({
                    'file': filepath,
                    'type': 'malformed_link',
                    'old': old_link,
                    'new': new_link
                })
                print(f"✓ 修复 {filepath}: 错误的拼接链接")
    
    def fix_architecture_md(self):
        """修复 ARCHITECTURE.md 中的示例链接"""
        filepath = "ARCHITECTURE.md"
        content = self.read_file(filepath)
        if not content:
            return
        
        # 第828-829行的示例链接应该使用占位符或指向实际存在的文件
        fixes = [
            ("[相关文档1](path/to/doc1.md)", "[相关文档1](Struct/00-INDEX.md)"),
            ("[相关文档2](path/to/doc2.md)", "[相关文档2](Flink/00-INDEX.md)"),
        ]
        
        for old_link, new_link in fixes:
            if old_link in content:
                content = content.replace(old_link, new_link)
                self.fixes_applied.append({
                    'file': filepath,
                    'type': 'placeholder_link',
                    'old': old_link,
                    'new': new_link
                })
                print(f"✓ 修复 {filepath}: {old_link} -> {new_link}")
        
        self.write_file(filepath, content)
    
    def fix_statistics_report_md(self):
        """修复 STATISTICS-REPORT.md 中的示例链接"""
        filepath = "STATISTICS-REPORT.md"
        content = self.read_file(filepath)
        if not content:
            return
        
        # 第292行的示例链接
        old_link = "[](../path)"
        new_link = "[](PROJECT-TRACKING.md)"
        
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
    
    def fix_toolchain_md(self):
        """修复 TOOLCHAIN.md 中的示例链接"""
        filepath = "TOOLCHAIN.md"
        content = self.read_file(filepath)
        if not content:
            return
        
        # 第313行的示例链接
        old_link = "[text](./path/to/file.md)"
        new_link = "[text](./Flink/00-INDEX.md)"
        
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
    
    def generate_fix_report(self):
        """生成修复报告"""
        print("\n" + "="*70)
        print("交叉引用修复报告 - 第二轮")
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
    
    print("开始第二轮修复...\n")
    
    fixer.fix_readme_md()
    fixer.fix_best_practices_md()
    fixer.fix_architecture_md()
    fixer.fix_statistics_report_md()
    fixer.fix_toolchain_md()
    
    fixer.generate_fix_report()
    print("\n第二轮修复完成!")

if __name__ == '__main__':
    main()
