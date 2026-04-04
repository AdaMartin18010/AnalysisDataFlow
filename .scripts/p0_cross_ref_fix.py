#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P0 交叉引用修复脚本 - 修复剩余错误
目标: 将错误数降至0
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

class P0CrossRefFixer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.fixes_applied = []
        self.stats = {'fixed': 0, 'skipped': 0, 'errors': 0}
        
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

    def fix_exercise_readme_links(self):
        """修复 Knowledge/98-exercises/README.md 中的重复链接问题"""
        filepath = "Knowledge/98-exercises/README.md"
        content = self.read_file(filepath)
        if not content:
            return
        
        # 修复重复的 .md00-INDEX.md 问题
        fixes = [
            ("../../Struct/00-INDEX.md00-INDEX.md", "../../Struct/00-INDEX.md"),
            ("../../Flink/00-INDEX.md00-INDEX.md", "../../Flink/00-INDEX.md"),
        ]
        
        modified = False
        for old, new in fixes:
            if old in content:
                content = content.replace(old, new)
                modified = True
                self.fixes_applied.append({'file': filepath, 'type': 'duplicate_link', 'old': old, 'new': new})
        
        if modified:
            if self.write_file(filepath, content):
                print(f"✓ 修复练习README链接: {filepath}")
                self.stats['fixed'] += 1

    def fix_wasi_component_links(self):
        """修复 WASI 组件模型文档中的链接"""
        filepath = "Flink/09-language-foundations/10-wasi-component-model.md"
        content = self.read_file(filepath)
        if not content:
            return
        
        # 修复前置依赖链接 - 文件不存在，改为指向存在的文件
        fixes = [
            ("[Flink/09-language-foundations/03-rust-native.md](./flink-rust-native-api-guide.md)",
             "[Flink Rust原生API](./flink-25-wasm-udf-ga.md)"),
        ]
        
        modified = False
        for old, new in fixes:
            if old in content:
                content = content.replace(old, new)
                modified = True
                self.fixes_applied.append({'file': filepath, 'type': 'broken_link', 'old': old, 'new': new})
        
        if modified:
            if self.write_file(filepath, content):
                print(f"✓ 修复WASI组件链接: {filepath}")
                self.stats['fixed'] += 1

    def fix_i18n_links(self):
        """修复 i18n 目录中的链接"""
        # i18n/en/README.md - 修复相对路径
        filepath = "i18n/en/README.md"
        content = self.read_file(filepath)
        if content:
            # 将 ../xxx 改为 ../../xxx 以正确指向根目录
            fixes = [
                ("](../Struct/", "](../../Struct/"),
                ("](../Knowledge/", "](../../Knowledge/"),
                ("](../Flink/", "](../../Flink/"),
                ("](../visuals/", "](../../visuals/"),
                ("](../knowledge-graph.html", "](../../knowledge-graph.html"),
                ("](../ROADMAP", "](../../ROADMAP"),
                ("](../E1-E4-ACCURACY-FIX", "](../../E1-E4-ACCURACY-FIX"),
                ("](../tutorials/", "](../../tutorials/"),
                ("](../PROJECT-VERSION-TRACKING", "](../../PROJECT-VERSION-TRACKING"),
                ("](../i18n/README.md", "](../../i18n/README.md"),
                ("](../LICENSE", "](../../LICENSE"),
                ("](../LICENSE-NOTICE", "](../../LICENSE-NOTICE"),
                ("](../THIRD-PARTY-NOTICES", "](../../THIRD-PARTY-NOTICES"),
            ]
            
            modified = False
            for old, new in fixes:
                if old in content:
                    content = content.replace(old, new)
                    modified = True
                    self.fixes_applied.append({'file': filepath, 'type': 'i18n_path', 'old': old, 'new': new})
            
            # 修复 demo.html 链接
            if "](demo.html)" in content:
                content = content.replace("](demo.html)", "](../../knowledge-graph.html)")
                modified = True
            
            if modified:
                if self.write_file(filepath, content):
                    print(f"✓ 修复i18n英文README链接: {filepath}")
                    self.stats['fixed'] += 1
        
        # i18n/i18n-architecture.md
        filepath = "i18n/i18n-architecture.md"
        content = self.read_file(filepath)
        if content:
            # 将不存在的英文文档链接改为中文文档
            fixes = [
                ("[GLOSSARY-EN.md](en/glossary/GLOSSARY-EN.md)", "[GLOSSARY.md](../GLOSSARY.md)"),
                ("[README-EN.md](en/docs/README-EN.md)", "[README.md](../README.md)"),
            ]
            
            modified = False
            for old, new in fixes:
                if old in content:
                    content = content.replace(old, new)
                    modified = True
                    self.fixes_applied.append({'file': filepath, 'type': 'i18n_missing', 'old': old, 'new': new})
            
            if modified:
                if self.write_file(filepath, content):
                    print(f"✓ 修复i18n架构文档链接: {filepath}")
                    self.stats['fixed'] += 1

    def fix_github_actions_links(self):
        """修复 GitHub Actions 链接 - 这些在GitHub上是有效的，但需要特殊处理"""
        # 这些链接在GitHub上有效，但在本地验证会失败
        # 将它们标记为外部链接或注释掉
        files_to_fix = [
            "LINK-HEALTH-AUTOMATION.md",
            "LINK-HEALTH-CHECK-COMPLETION-REPORT.md",
        ]
        
        for filepath in files_to_fix:
            content = self.read_file(filepath)
            if not content:
                continue
            
            # 将 ../../actions/workflows/ 改为 https://github.com/.../actions/workflows/
            # 使用绝对URL
            old_pattern = "[Actions](../../actions/workflows/"
            new_pattern = "[Actions](https://github.com/luyanfeng/AnalysisDataFlow/actions/workflows/"
            
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                # 同时修复 .yml) 结尾
                content = content.replace("link-health-check.yml)", "link-health-check.yml)")
                
                if self.write_file(filepath, content):
                    print(f"✓ 修复GitHub Actions链接: {filepath}")
                    self.stats['fixed'] += 1
                    self.fixes_applied.append({'file': filepath, 'type': 'github_actions', 'note': '改为绝对URL'})

    def fix_anchor_issues_in_docs(self):
        """修复文档中的锚点问题"""
        # 修复 BENCHMARK-REPORT.md 和 TROUBLESHOOTING-COMPLETE.md
        files_to_fix = [
            ("BENCHMARK-REPORT.md", "#5-形式证明--工程论证", "#5-形式证明--工程论证-proof--engineering-argument"),
            ("TROUBLESHOOTING-COMPLETE.md", "#5-形式证明--工程论证", "#5-形式证明--工程论证-proof--engineering-argument"),
        ]
        
        for filepath, wrong_anchor, correct_anchor in files_to_fix:
            content = self.read_file(filepath)
            if not content:
                continue
            
            if wrong_anchor in content:
                # 检查目标锚点是否存在
                if correct_anchor.lstrip('#') in content or f'id="{correct_anchor.lstrip("#")}"' in content:
                    content = content.replace(wrong_anchor, correct_anchor)
                    if self.write_file(filepath, content):
                        print(f"✓ 修复锚点: {filepath}")
                        self.stats['fixed'] += 1
                        self.fixes_applied.append({'file': filepath, 'type': 'anchor', 'old': wrong_anchor, 'new': correct_anchor})

    def fix_glossary_en_anchor(self):
        """修复 GLOSSARY-EN.md 中的缺失锚点"""
        filepath = "GLOSSARY-EN.md"
        content = self.read_file(filepath)
        if not content:
            return
        
        # 检查是否存在 J 部分的标题
        if "# J" not in content and "## J" not in content:
            # 在适当位置添加 J 部分（如果没有J开头的术语）
            # 或者移除到 J 的链接
            # 这里选择添加一个空的 J 部分
            lines = content.split('\n')
            new_lines = []
            added_j = False
            for i, line in enumerate(lines):
                new_lines.append(line)
                # 在 I 部分后添加 J 部分
                if line.startswith('# ') and ' I' in line and not added_j:
                    new_lines.append('')
                    new_lines.append('# J')
                    new_lines.append('')
                    new_lines.append('*No entries starting with J*')
                    new_lines.append('')
                    added_j = True
            
            if added_j:
                content = '\n'.join(new_lines)
                if self.write_file(filepath, content):
                    print(f"✓ 添加缺失的 J 部分: {filepath}")
                    self.stats['fixed'] += 1
                    self.fixes_applied.append({'file': filepath, 'type': 'add_section', 'section': 'J'})

    def create_missing_file(self, filepath, content):
        """创建缺失的文件"""
        full_path = self.base_dir / filepath
        try:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"创建文件 {filepath} 失败: {e}")
            return False

    def create_missing_rust_native_guide(self):
        """创建缺失的 Flink Rust 原生API指南文件"""
        filepath = "Flink/09-language-foundations/flink-rust-native-api-guide.md"
        if (self.base_dir / filepath).exists():
            return
        
        content = '''# Flink Rust 原生 API 开发指南

> 所属阶段: Flink/09-language-foundations | 前置依赖: [Flink WASM UDF GA](flink-25-wasm-udf-ga.md) | 形式化等级: L3

本文档介绍如何在 Flink 中使用 Rust 语言进行原生扩展开发。

## 1. 概述

Flink 通过 WASM (WebAssembly) 技术支持 Rust 语言的 UDF 开发。Rust 的高性能和内存安全特性使其成为流处理计算密集型任务的理想选择。

## 2. 环境准备

- Rust 编译器 (1.70+)
- wasm32-unknown-unknown target
- Flink 2.5+

## 3. 开发流程

参见 [Flink 2.5 WASM UDF GA 指南](flink-25-wasm-udf-ga.md) 获取详细开发步骤。

## 4. 参考文档

- [WASI Component Model](10-wasi-component-model.md)
- [Flink WASM Streaming](../../13-wasm/wasm-streaming.md)
'''
        
        if self.create_missing_file(filepath, content):
            print(f"✓ 创建缺失文件: {filepath}")
            self.stats['fixed'] += 1
            self.fixes_applied.append({'file': filepath, 'type': 'create_file'})

    def run_all_fixes(self):
        """运行所有修复"""
        print("="*70)
        print("P0 交叉引用修复 - 批量修复")
        print("="*70)
        
        self.fix_exercise_readme_links()
        self.fix_wasi_component_links()
        self.fix_i18n_links()
        self.fix_github_actions_links()
        self.fix_anchor_issues_in_docs()
        self.fix_glossary_en_anchor()
        self.create_missing_rust_native_guide()
        
        print("\n" + "="*70)
        print("修复完成统计")
        print("="*70)
        print(f"总修复数: {self.stats['fixed']}")
        
        if self.fixes_applied:
            print("\n修复详情:")
            for fix in self.fixes_applied:
                print(f"  - {fix['file']}: {fix.get('type', 'unknown')}")

def main():
    base_dir = Path(__file__).parent.parent
    fixer = P0CrossRefFixer(base_dir)
    fixer.run_all_fixes()
    print("\nP0 修复完成!")
    return 0

if __name__ == '__main__':
    exit(main())
