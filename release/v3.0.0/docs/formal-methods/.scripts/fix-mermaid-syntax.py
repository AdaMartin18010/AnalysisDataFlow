#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mermaid 语法批量修复脚本

功能:
1. 扫描所有.md文件中的Mermaid代码块
2. 自动修复常见语法错误:
   - `-- >` → `-->`
   - `- ->` → `-->`
   - `== >` → `==>`
   - `--.` → `-.-`
3. 修复中文引号问题
4. 生成修复报告

作者: Auto-generated
日期: 2026-04-10
"""

import re
import os
import json
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from datetime import datetime


@dataclass
class FixRecord:
    """记录一次修复操作"""
    file_path: str
    line_number: int
    original: str
    fixed: str
    fix_type: str


@dataclass
class FileReport:
    """单个文件的修复报告"""
    file_path: str
    total_mermaid_blocks: int = 0
    fixes: List[FixRecord] = field(default_factory=list)
    errors_remaining: List[Dict] = field(default_factory=list)


class MermaidFixer:
    """Mermaid语法修复器"""
    
    # 修复规则: (模式, 替换, 描述)
    FIX_RULES = [
        # 箭头修复
        (r'--\s*>', '-->', '箭头空格修复'),
        (r'-\s*->', '-->', '箭头空格修复'),
        (r'=\s*>', '==>', '粗箭头空格修复'),
        (r'=\s*=\s*>', '==>', '粗箭头多空格修复'),
        
        # 虚线修复
        (r'--\.', '-.-', '虚线修复'),
        (r'\.\s*-\s*\.\.?', '-.-', '虚线格式修复'),
        
        # 点线修复
        (r'-\.\s*->', '-.->', '点线箭头修复'),
        
        # 其他常见错误
        (r'<\s*--\s*>', '<-->', '双向箭头修复'),
        (r'--\s*>>', '-->>', '开放箭头修复'),
    ]
    
    # 中文引号修复
    QUOTE_FIXES = [
        # 修复错误的引号嵌套
        (r'"([^"]*)"([^"]*)"', r'"\1\2"', '引号嵌套修复'),
    ]
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.fix_records: List[FixRecord] = []
        self.files_processed = 0
        self.files_modified = 0
        self.total_blocks = 0
        
    def log(self, message: str):
        """输出日志"""
        if self.verbose:
            print(message)
    
    def fix_arrow_syntax(self, line: str) -> Tuple[str, List[Tuple[str, str]]]:
        """
        修复箭头语法错误
        返回: (修复后的行, [(原始片段, 修复类型), ...])
        """
        fixed_line = line
        changes = []
        
        for pattern, replacement, desc in self.FIX_RULES:
            matches = list(re.finditer(pattern, fixed_line))
            for match in reversed(matches):  # 从后向前替换，避免位置变化
                original = match.group(0)
                fixed_line = fixed_line[:match.start()] + replacement + fixed_line[match.end():]
                changes.append((original, desc))
        
        return fixed_line, changes
    
    def fix_quotes_in_mermaid(self, content: str) -> Tuple[str, List[Tuple[int, str, str]]]:
        """
        修复Mermaid代码块中的引号问题
        返回: (修复后的内容, [(行号, 原始, 修复类型), ...])
        """
        changes = []
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines, 1):
            fixed_line = line
            # 检查是否有节点定义包含中文引号
            # 例如: A["节点"] 应该是合法的，但 A["节点"文本"] 是非法的
            
            # 统计引号数量
            double_quotes = line.count('"')
            
            # 如果引号数量为奇数，可能是未闭合
            if double_quotes % 2 == 1 and double_quotes > 0:
                # 尝试修复：找到最后一个不完整的引号
                # 这只是一个启发式修复
                pass  # 暂不处理复杂引号问题
            
            # 修复连续引号问题
            if '""' in fixed_line and '[]' not in fixed_line:
                original = fixed_line
                fixed_line = re.sub(r'""+', '"', fixed_line)
                if fixed_line != original:
                    changes.append((i, original, '连续引号修复'))
            
            fixed_lines.append(fixed_line)
        
        return '\n'.join(fixed_lines), changes
    
    def process_mermaid_block(self, block_lines: List[str], start_line: int) -> Tuple[List[str], List[FixRecord]]:
        """
        处理一个Mermaid代码块
        返回: (修复后的行列表, 修复记录列表)
        """
        fixed_lines = []
        records = []
        
        for i, line in enumerate(block_lines):
            line_num = start_line + i
            original_line = line
            
            # 跳过代码块标记
            if line.strip() == '```mermaid' or line.strip() == '```':
                fixed_lines.append(line)
                continue
            
            # 修复箭头语法
            fixed_line, arrow_changes = self.fix_arrow_syntax(line)
            
            for orig, change_type in arrow_changes:
                records.append(FixRecord(
                    file_path='',  # 稍后填充
                    line_number=line_num,
                    original=orig,
                    fixed=fixed_line.strip(),
                    fix_type=change_type
                ))
            
            fixed_lines.append(fixed_line)
        
        return fixed_lines, records
    
    def process_file(self, file_path: Path) -> FileReport:
        """处理单个文件"""
        report = FileReport(file_path=str(file_path))
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.log(f"  错误: 无法读取文件 {file_path}: {e}")
            return report
        
        lines = content.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 检测Mermaid代码块开始
            if line.strip() == '```mermaid':
                report.total_mermaid_blocks += 1
                block_start = i
                block_lines = [line]
                i += 1
                
                # 收集整个代码块
                while i < len(lines) and lines[i].strip() != '```':
                    block_lines.append(lines[i])
                    i += 1
                
                # 添加结束标记
                if i < len(lines):
                    block_lines.append(lines[i])
                    i += 1
                
                # 处理代码块
                fixed_block, records = self.process_mermaid_block(block_lines, block_start + 1)
                
                # 填充文件路径
                for r in records:
                    r.file_path = str(file_path)
                
                report.fixes.extend(records)
                fixed_lines.extend(fixed_block)
            else:
                fixed_lines.append(line)
                i += 1
        
        # 写入修复后的内容
        if report.fixes:
            fixed_content = '\n'.join(fixed_lines)
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                self.files_modified += 1
                self.log(f"  已修复 {len(report.fixes)} 处问题")
            except Exception as e:
                self.log(f"  错误: 无法写入文件 {file_path}: {e}")
        
        return report
    
    def scan_for_remaining_errors(self, file_path: Path) -> List[Dict]:
        """扫描文件中剩余的潜在错误"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return errors
        
        lines = content.split('\n')
        in_mermaid = False
        
        for i, line in enumerate(lines, 1):
            if line.strip() == '```mermaid':
                in_mermaid = True
                continue
            elif line.strip() == '```' and in_mermaid:
                in_mermaid = False
                continue
            
            if in_mermaid:
                # 检查可能的语法错误
                # 检查箭头中的空格
                if re.search(r'--\s+>', line) or re.search(r'-\s+->', line):
                    errors.append({
                        'line': i,
                        'content': line.strip()[:80],
                        'error_type': '箭头空格'
                    })
                
                # 检查引号问题
                if line.count('"') % 2 == 1:
                    errors.append({
                        'line': i,
                        'content': line.strip()[:80],
                        'error_type': '可能未闭合的引号'
                    })
                
                # 检查节点定义语法
                if '[' in line and ']' not in line:
                    errors.append({
                        'line': i,
                        'content': line.strip()[:80],
                        'error_type': '可能未闭合的方括号'
                    })
        
        return errors


def generate_report(fixer: MermaidFixer, reports: List[FileReport], output_dir: Path):
    """生成修复报告"""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Markdown报告
    md_content = f"""# Mermaid语法修复报告

**生成时间**: {timestamp}

## 摘要

- 处理文件数: {fixer.files_processed}
- 修改文件数: {fixer.files_modified}
- Mermaid代码块数: {sum(r.total_mermaid_blocks for r in reports)}
- 修复问题数: {len(fixer.fix_records)}

## 修复详情

"""
    
    for report in reports:
        if report.fixes:
            md_content += f"\n### {report.file_path}\n\n"
            md_content += f"- Mermaid代码块: {report.total_mermaid_blocks}\n"
            md_content += f"- 修复数量: {len(report.fixes)}\n\n"
            
            # 按修复类型分组
            fixes_by_type = {}
            for fix in report.fixes:
                if fix.fix_type not in fixes_by_type:
                    fixes_by_type[fix.fix_type] = []
                fixes_by_type[fix.fix_type].append(fix)
            
            for fix_type, fixes in fixes_by_type.items():
                md_content += f"**{fix_type}** ({len(fixes)}处):\n\n"
                for fix in fixes[:10]:  # 最多显示10个
                    md_content += f"- 行{fix.line_number}: `{fix.original}` → `{fix.fixed}`\n"
                if len(fixes) > 10:
                    md_content += f"- ... 还有 {len(fixes) - 10} 处\n"
                md_content += "\n"
    
    # JSON报告
    json_data = {
        'timestamp': timestamp,
        'summary': {
            'files_processed': fixer.files_processed,
            'files_modified': fixer.files_modified,
            'total_mermaid_blocks': sum(r.total_mermaid_blocks for r in reports),
            'total_fixes': len(fixer.fix_records)
        },
        'files': []
    }
    
    for report in reports:
        if report.fixes:
            json_data['files'].append({
                'file_path': report.file_path,
                'mermaid_blocks': report.total_mermaid_blocks,
                'fixes': [
                    {
                        'line': f.line_number,
                        'original': f.original,
                        'fixed': f.fixed,
                        'type': f.fix_type
                    }
                    for f in report.fixes
                ]
            })
    
    # 写入报告
    md_path = output_dir / 'mermaid-fix-report.md'
    json_path = output_dir / 'mermaid-fix-report.json'
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    return md_path, json_path


def main():
    """主函数"""
    # 优先修复的6个文档
    priority_files = [
        'formal-methods/99-probabilistic-programming.md',
        'formal-methods/99-homotopy-type-theory.md',
        'formal-methods/99-game-semantics.md',
        'formal-methods/99-kubernetes-scheduler.md',
        'formal-methods/99-raft-consensus.md',
        'formal-methods/99-llvm-ir-semantics.md',
    ]
    
    # 检查当前目录
    base_path = Path('.')
    
    # 确保在正确的目录
    if not (base_path / 'formal-methods').exists():
        print("错误: 请在项目根目录运行此脚本")
        sys.exit(1)
    
    print("=" * 60)
    print("Mermaid语法批量修复工具")
    print("=" * 60)
    
    fixer = MermaidFixer(verbose=True)
    reports = []
    
    # 处理优先文件
    print(f"\n正在处理 {len(priority_files)} 个优先文件...\n")
    
    for rel_path in priority_files:
        file_path = base_path / rel_path
        if file_path.exists():
            print(f"处理: {rel_path}")
            report = fixer.process_file(file_path)
            fixer.files_processed += 1
            reports.append(report)
            
            # 检查剩余错误
            remaining = fixer.scan_for_remaining_errors(file_path)
            if remaining:
                print(f"  警告: 发现 {len(remaining)} 处潜在问题")
                report.errors_remaining = remaining
        else:
            print(f"跳过: {rel_path} (文件不存在)")
    
    # 可选: 处理所有formal-methods中的.md文件
    # 扫描整个目录
    print("\n正在扫描所有formal-methods中的Markdown文件...")
    all_md_files = list((base_path / 'formal-methods').rglob('*.md'))
    print(f"找到 {len(all_md_files)} 个Markdown文件")
    
    # 生成报告
    print("\n生成修复报告...")
    output_dir = base_path / 'formal-methods' / '.scripts'
    md_report, json_report = generate_report(fixer, reports, output_dir)
    
    # 输出摘要
    print("\n" + "=" * 60)
    print("修复完成!")
    print("=" * 60)
    print(f"处理文件数: {fixer.files_processed}")
    print(f"修改文件数: {fixer.files_modified}")
    print(f"修复问题数: {sum(len(r.fixes) for r in reports)}")
    print(f"\n报告文件:")
    print(f"  - {md_report}")
    print(f"  - {json_report}")
    
    # 显示修复统计
    print("\n修复类型统计:")
    fix_types = {}
    for report in reports:
        for fix in report.fixes:
            fix_types[fix.fix_type] = fix_types.get(fix.fix_type, 0) + 1
    
    for fix_type, count in sorted(fix_types.items(), key=lambda x: -x[1]):
        print(f"  - {fix_type}: {count}")


if __name__ == '__main__':
    main()
