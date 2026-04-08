#!/usr/bin/env python3
"""
交叉引用修复工具 - P0-4任务
修复剩余的114个交叉引用错误
"""

import re
import os
import glob
from pathlib import Path
from collections import defaultdict

class CrossRefFixer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.errors_fixed = 0
        self.files_checked = 0
        
        # 已知的文件映射关系 (旧路径 -> 新路径)
        self.file_mappings = {
            # Struct目录
            "Struct/03-relationships/03.02-csp-to-actor-encoding.md": "Struct/03-relationships/03.02-flink-to-process-calculus.md",
            
            # Knowledge目录
            "Knowledge/05-migrations/kafka-streams-to-flink-guide.md": "Knowledge/05-mapping-guides/migration-guides/05.2-kafka-streams-to-flink-migration.md",
            "Knowledge/kafka-streams-migration.md": "Knowledge/05-mapping-guides/migration-guides/05.2-kafka-streams-to-flink-migration.md",
            
            # Flink目录 - 旧路径映射
            "Flink/02-core-mechanisms/": "Flink/02-core/",
            "Flink/03-sql-table-api/": "Flink/03-api/03.02-table-sql-api/",
            "Flink/04-connectors/": "Flink/05-ecosystem/05.01-connectors/",
            "Flink/06-engineering/": "Flink/09-practices/09.03-performance-tuning/",
            "Flink/10-deployment/": "Flink/04-runtime/04.01-deployment/",
            "Flink/13-wasm/": "Flink/05-ecosystem/05.03-wasm-udf/",
            "Flink/12-ai-ml/": "Flink/06-ai-ml/",
        }
        
        # 已知的锚点修复映射
        self.anchor_mappings = {
            # 常见标题规范化映射
            "##-concept-definition": "##-1-概念定义-definitions",
            "##-property-derivation": "##-2-属性推导-properties",
            "##-relation-establishment": "##-3-关系建立-relations",
            "##-argumentation": "##-4-论证过程-argumentation",
            "##-proof": "##-5-形式证明--工程论证-proof--engineering-argument",
            "##-examples": "##-6-实例验证-examples",
            "##-visualization": "##-7-可视化-visualizations",
            "##-references": "##-8-引用参考-references",
        }
        
    def get_all_markdown_files(self):
        """获取所有Markdown文件"""
        md_files = []
        for pattern in ["Struct/**/*.md", "Knowledge/**/*.md", "Flink/**/*.md"]:
            md_files.extend(glob.glob(str(self.base_path / pattern), recursive=True))
        return [f for f in md_files if not f.endswith("_TEMPLATE.md")]
    
    def find_broken_refs(self, content, file_path):
        """查找损坏的引用"""
        issues = []
        
        # 匹配Markdown链接 [text](path#anchor)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for match in re.finditer(link_pattern, content):
            text, link = match.groups()
            if link.startswith("http") or link.startswith("#"):
                continue
                
            # 分离路径和锚点
            if "#" in link:
                path, anchor = link.split("#", 1)
            else:
                path, anchor = link, None
                
            # 检查文件是否存在
            if path:
                full_path = (Path(file_path).parent / path).resolve()
                if not full_path.exists():
                    issues.append({
                        'type': 'file',
                        'original': link,
                        'text': text,
                        'path': path,
                        'anchor': anchor,
                        'match': match.group(0)
                    })
                    
        return issues
    
    def fix_file_ref(self, path):
        """尝试修复文件引用"""
        # 直接映射
        if path in self.file_mappings:
            return self.file_mappings[path]
            
        # 目录前缀映射
        for old_prefix, new_prefix in self.file_mappings.items():
            if old_prefix.endswith("/") and path.startswith(old_prefix.replace("/", "")):
                return new_prefix + path[len(old_prefix.replace("/", "")):]
                
        # 尝试找到相似文件
        base_name = Path(path).name
        for md_file in self.get_all_markdown_files():
            if Path(md_file).name == base_name:
                # 计算相对路径
                return os.path.relpath(md_file, self.base_path).replace("\\", "/")
                
        return None
    
    def fix_anchor(self, anchor):
        """尝试修复锚点"""
        normalized = anchor.lower().replace(" ", "-")
        
        if normalized in self.anchor_mappings:
            return self.anchor_mappings[normalized]
            
        # 添加章节编号前缀的常见模式
        if not normalized.startswith("##-"):
            for pattern, replacement in self.anchor_mappings.items():
                if pattern.replace("##-", "") in normalized:
                    return replacement
                    
        return anchor
    
    def fix_file(self, file_path):
        """修复单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            issues = self.find_broken_refs(content, file_path)
            
            for issue in issues:
                if issue['type'] == 'file':
                    fixed_path = self.fix_file_ref(issue['path'])
                    if fixed_path:
                        fixed_anchor = self.fix_anchor(issue['anchor']) if issue['anchor'] else None
                        
                        if fixed_anchor:
                            new_link = f"[{issue['text']}]({fixed_path}#{fixed_anchor})"
                        else:
                            new_link = f"[{issue['text']}]({fixed_path})"
                            
                        content = content.replace(issue['match'], new_link)
                        self.errors_fixed += 1
                        print(f"  Fixed: {issue['match']} -> {new_link}")
                        
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            
        return False
    
    def run(self):
        """运行修复流程"""
        print("=" * 60)
        print("交叉引用修复工具 - P0-4任务")
        print("=" * 60)
        
        md_files = self.get_all_markdown_files()
        print(f"\n扫描文件数: {len(md_files)}")
        
        fixed_files = []
        for file_path in md_files:
            self.files_checked += 1
            if self.files_checked % 50 == 0:
                print(f"  已检查: {self.files_checked}/{len(md_files)}")
                
            if self.fix_file(file_path):
                fixed_files.append(file_path)
                
        print("\n" + "=" * 60)
        print("修复完成统计")
        print("=" * 60)
        print(f"检查文件数: {self.files_checked}")
        print(f"修复文件数: {len(fixed_files)}")
        print(f"修复错误数: {self.errors_fixed}")
        print(f"修复文件列表:")
        for f in fixed_files[:10]:  # 只显示前10个
            print(f"  - {os.path.basename(f)}")
        if len(fixed_files) > 10:
            print(f"  ... 还有 {len(fixed_files) - 10} 个文件")
            
        return self.errors_fixed

if __name__ == "__main__":
    import sys
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    fixer = CrossRefFixer(base_path)
    fixer.run()
