#!/usr/bin/env python3
"""
修复AnalysisDataFlow项目中的重复编号错误

主要问题：
1. 索引文档和模式文档中使用了 `**Thm-S-XX-XX**: 描述` 格式，被误认为定义
2. 需要将这类引用改为纯文本引用格式
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple

class DuplicateIDFixer:
    def __init__(self, validation_report_path: str):
        self.validation_report_path = validation_report_path
        self.issues = []
        self.fixed_count = 0
        self.fixes_log = []
        
        # 定义ID模式 - 匹配 **ID**: 或 **ID** 格式
        self.id_patterns = {
            'Thm': re.compile(r'\*\*?(Thm-[SFK]-\d{2}-\d{2})\*\*:?'),
            'Def': re.compile(r'\*\*?(Def-[SFK]-\d{2}-\d{2})\*\*:?'),
            'Lemma': re.compile(r'\*\*?(Lemma-[SFK]-\d{2}-\d{2})\*\*:?'),
            'Prop': re.compile(r'\*\*?(Prop-[SFK]-\d{2}-\d{2})\*\*:?'),
            'Cor': re.compile(r'\*\*?(Cor-[SFK]-\d{2}-\d{2})\*\*:?'),
        }
        
        # 表格行中的ID引用模式（如 | Thm-S-XX-XX | 描述 |）
        self.table_id_pattern = re.compile(
            r'^\|\s*\*\*?(Thm|Def|Lemma|Prop|Cor)-([SFK])-(\d{2})-(\d{2})\*\*?\s*\|'
        )
        
    def load_validation_report(self):
        """加载验证报告"""
        with open(self.validation_report_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.issues = [issue for issue in data.get('issues', []) 
                          if issue['code'] == 'DUPLICATE_ID']
        print(f"Loaded {len(self.issues)} DUPLICATE_ID issues")
        
    def group_issues_by_file(self) -> Dict[str, List[dict]]:
        """按文件分组问题"""
        issues_by_file = {}
        for issue in self.issues:
            file_path = issue['file_path']
            if file_path not in issues_by_file:
                issues_by_file[file_path] = []
            issues_by_file[file_path].append(issue)
        return issues_by_file
    
    def get_duplicate_ids_by_file(self, file_path: str) -> Set[str]:
        """获取特定文件中的重复ID集合"""
        duplicate_ids = set()
        for issue in self.issues:
            if issue['file_path'] == file_path:
                duplicate_ids.add(issue['element_id'])
        return duplicate_ids
    
    def fix_file(self, file_path: str, duplicate_ids: Set[str]) -> bool:
        """修复单个文件中的重复ID问题"""
        full_path = Path(file_path)
        if not full_path.exists():
            # 尝试从项目根目录查找
            full_path = Path(os.getcwd()) / file_path
            if not full_path.exists():
                print(f"  Warning: File not found: {file_path}")
                return False
        
        # 读取文件内容
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"  Error reading {file_path}: {e}")
            return False
        
        fixed = False
        new_lines = []
        changes = []
        
        for line_num, line in enumerate(lines, 1):
            original_line = line
            modified = False
            
            # 检查是否是表格行
            is_table_row = line.strip().startswith('|') and '|' in line[1:]
            
            for id_type, pattern in self.id_patterns.items():
                for match in pattern.finditer(line):
                    element_id = match.group(1)
                    if element_id in duplicate_ids:
                        # 根据上下文决定如何修复
                        if is_table_row:
                            # 表格中：保留ID但去掉加粗
                            line = line.replace(match.group(0), element_id)
                        else:
                            # 非表格中：转换为链接引用格式
                            line = line.replace(match.group(0), f"`{element_id}`")
                        modified = True
                        changes.append({
                            'line': line_num,
                            'original': match.group(0),
                            'fixed': element_id if is_table_row else f'`{element_id}`',
                            'element_id': element_id
                        })
            
            if modified:
                fixed = True
            new_lines.append(line)
        
        if fixed:
            # 写回文件
            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                self.fixes_log.append({
                    'file': file_path,
                    'changes': changes
                })
                self.fixed_count += len(changes)
                print(f"  Fixed {len(changes)} issues in {file_path}")
                return True
            except Exception as e:
                print(f"  Error writing {file_path}: {e}")
                return False
        
        return False
    
    def run(self):
        """执行修复"""
        print("=" * 60)
        print("Duplicate ID Fixer")
        print("=" * 60)
        
        # 加载验证报告
        self.load_validation_report()
        
        # 按文件分组
        issues_by_file = self.group_issues_by_file()
        print(f"Found {len(issues_by_file)} files with duplicate IDs")
        print()
        
        # 修复每个文件
        fixed_files = 0
        for file_path in sorted(issues_by_file.keys()):
            print(f"Processing: {file_path}")
            duplicate_ids = self.get_duplicate_ids_by_file(file_path)
            if self.fix_file(file_path, duplicate_ids):
                fixed_files += 1
        
        print()
        print("=" * 60)
        print(f"Summary: Fixed {self.fixed_count} issues in {fixed_files} files")
        print("=" * 60)
        
        return self.fixes_log
    
    def generate_report(self, output_path: str):
        """生成修复报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_issues_found': len(self.issues),
            'total_fixed': self.fixed_count,
            'files_fixed': len(self.fixes_log),
            'fixes': self.fixes_log
        }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 同时生成Markdown报告
        md_path = output_path.replace('.json', '.md')
        self._generate_markdown_report(md_path)
        
        print(f"\nReports generated:")
        print(f"  - {output_path}")
        print(f"  - {md_path}")
    
    def _generate_markdown_report(self, output_path: str):
        """生成Markdown格式的修复报告"""
        lines = [
            "# 重复ID修复报告",
            "",
            f"**修复时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**原始问题数**: {len(self.issues)}",
            f"**修复数量**: {self.fixed_count}",
            f"**涉及文件数**: {len(self.fixes_log)}",
            "",
            "## 修复策略",
            "",
            "1. 识别验证报告中标记为DUPLICATE_ID的问题",
            "2. 对于索引文档和模式文档中重复的元素声明：",
            "   - 表格中的元素引用：保留ID，移除加粗格式 `**ID**` → `ID`",
            "   - 正文中的元素引用：转换为代码格式 `**ID**` → `` `ID` ``",
            "3. 保留主文档（Proof-Chains）中的原始定义",
            "",
            "## 修复详情",
            ""
        ]
        
        for fix in self.fixes_log:
            lines.append(f"### {fix['file']}")
            lines.append("")
            lines.append("| 行号 | 原始内容 | 修复后 | 元素ID |")
            lines.append("|------|----------|--------|--------|")
            for change in fix['changes']:
                orig = change['original'].replace('|', '\\|')
                fixed = change['fixed'].replace('|', '\\|')
                lines.append(f"| {change['line']} | {orig} | {fixed} | {change['element_id']} |")
            lines.append("")
        
        lines.extend([
            "## 后续建议",
            "",
            "1. 重新运行验证脚本确认所有DUPLICATE_ID错误已修复",
            "2. 检查文档语义是否因格式变更而受影响",
            "3. 考虑在文档规范中明确区分元素定义和元素引用",
            ""
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))


def main():
    # 配置
    VALIDATION_REPORT = 'reports/validation-report-2026-04-11.json'
    FIX_REPORT_JSON = 'reports/fix-duplicate-ids-report.json'
    FIX_REPORT_MD = 'reports/fix-duplicate-ids-report.md'
    
    # 检查验证报告是否存在
    if not os.path.exists(VALIDATION_REPORT):
        print(f"Error: Validation report not found: {VALIDATION_REPORT}")
        return 1
    
    # 执行修复
    fixer = DuplicateIDFixer(VALIDATION_REPORT)
    fixer.run()
    
    # 生成报告
    fixer.generate_report(FIX_REPORT_JSON)
    
    return 0


if __name__ == '__main__':
    exit(main())
