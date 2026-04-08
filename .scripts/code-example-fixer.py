#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码示例修复器 - Code Example Fixer
自动修复Markdown中代码示例的常见问题

作者: AI Agent
创建时间: 2026-04-08
版本: 1.0.0
"""

import re
import os
import sys
import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Optional
from datetime import datetime
from difflib import unified_diff


@dataclass
class FixResult:
    """修复结果"""
    file_path: str
    block_index: int
    original_code: str
    fixed_code: str
    fixes_applied: List[str]
    success: bool


class CodeExampleFixer:
    """代码示例修复器"""
    
    def __init__(self, project_root: Path, dry_run: bool = True):
        self.project_root = Path(project_root)
        self.dry_run = dry_run
        self.fixes_applied: List[FixResult] = []
    
    def fix_python_indentation(self, code: str) -> Tuple[str, List[str]]:
        """修复Python缩进问题"""
        fixes = []
        lines = code.split('\n')
        
        # 检测缩进类型
        has_tabs = any('\t' in line for line in lines)
        has_spaces = any('    ' in line or '  ' in line for line in lines)
        
        if has_tabs and has_spaces:
            # 混用Tab和空格，统一为4空格
            new_lines = []
            for line in lines:
                # 将Tab替换为4空格
                fixed_line = line.replace('\t', '    ')
                new_lines.append(fixed_line)
            code = '\n'.join(new_lines)
            fixes.append("将Tab替换为4空格")
        elif has_tabs:
            # 只有Tab，替换为4空格
            code = code.replace('\t', '    ')
            fixes.append("将Tab替换为4空格")
        
        # 检测常见缩进问题：2空格缩进改为4空格
        lines = code.split('\n')
        has_2space = any(re.match(r'^  [^ ]', line) for line in lines if line.strip())
        has_4space = any(re.match(r'^    [^ ]', line) for line in lines if line.strip())
        
        if has_2space and not has_4space:
            # 可能是2空格缩进，扩大为4空格
            new_lines = []
            for line in lines:
                leading_spaces = len(line) - len(line.lstrip())
                if leading_spaces > 0:
                    new_indent = '    ' * (leading_spaces // 2) + '  ' * (leading_spaces % 2)
                    new_lines.append(new_indent + line.lstrip())
                else:
                    new_lines.append(line)
            code = '\n'.join(new_lines)
            fixes.append("将2空格缩进转换为4空格")
        
        return code, fixes
    
    def fix_common_python_issues(self, code: str) -> Tuple[str, List[str]]:
        """修复常见Python语法问题"""
        fixes = []
        original = code
        
        # 修复print语句 (Python 2 -> 3)
        # 简单匹配print后面直接跟空格和内容的
        code = re.sub(r'\bprint\s+([^(])', r'print(\1', code)
        if code != original:
            fixes.append("修复print语句语法")
            original = code
        
        # 修复缺少的冒号 (常见错误)
        # 在if/for/while/def/class后添加冒号
        patterns = [
            (r'^(\s*if\s+[^:]+)$', r'\1:'),
            (r'^(\s*elif\s+[^:]+)$', r'\1:'),
            (r'^(\s*else\s*)$', r'\1:'),
            (r'^(\s*for\s+[^:]+)$', r'\1:'),
            (r'^(\s*while\s+[^:]+)$', r'\1:'),
            (r'^(\s*def\s+[^:]+)$', r'\1:'),
            (r'^(\s*class\s+[^:]+)$', r'\1:'),
            (r'^(\s*try\s*)$', r'\1:'),
            (r'^(\s*except\s*[^:]+)$', r'\1:'),
            (r'^(\s*finally\s*)$', r'\1:'),
        ]
        
        lines = code.split('\n')
        new_lines = []
        for line in lines:
            new_line = line
            for pattern, replacement in patterns:
                new_line = re.sub(pattern, replacement, new_line)
            if new_line != line:
                fixes.append(f"添加缺失的冒号: {line.strip()[:30]}")
            new_lines.append(new_line)
        code = '\n'.join(new_lines)
        
        # 修复尾部空格
        code_lines = code.split('\n')
        stripped_lines = [line.rstrip() for line in code_lines]
        if stripped_lines != code_lines:
            fixes.append("移除尾部空格")
            code = '\n'.join(stripped_lines)
        
        # 确保文件末尾有且只有一个换行
        code = code.rstrip() + '\n'
        
        return code, fixes
    
    def fix_java_issues(self, code: str) -> Tuple[str, List[str]]:
        """修复Java代码问题"""
        fixes = []
        
        # 修复尾部空格
        lines = code.split('\n')
        stripped_lines = [line.rstrip() for line in lines]
        if stripped_lines != lines:
            fixes.append("移除尾部空格")
            code = '\n'.join(stripped_lines)
        
        # 修复常见语法问题
        # 检查并修复不完整语句（简化检查）
        open_braces = code.count('{')
        close_braces = code.count('}')
        if open_braces > close_braces:
            # 可能需要添加闭合大括号
            missing = open_braces - close_braces
            code = code.rstrip() + '\n' + '}\n' * missing
            fixes.append(f"添加 {missing} 个缺失的闭合大括号")
        
        # 确保文件末尾有换行
        code = code.rstrip() + '\n'
        
        return code, fixes
    
    def fix_yaml_issues(self, code: str) -> Tuple[str, List[str]]:
        """修复YAML问题"""
        fixes = []
        
        # 修复Tab缩进
        if '\t' in code:
            code = code.replace('\t', '  ')
            fixes.append("将Tab替换为2空格")
        
        # 修复尾部空格
        lines = code.split('\n')
        stripped_lines = [line.rstrip() for line in lines]
        if stripped_lines != lines:
            fixes.append("移除尾部空格")
            code = '\n'.join(stripped_lines)
        
        # 确保冒号后有空格
        lines = code.split('\n')
        new_lines = []
        for line in lines:
            # 匹配 key:value 但排除 key: value (已有空格) 和 URL
            new_line = re.sub(r'^(\s*[\w-]+):([^\s]|$)', r'\1: \2', line)
            if new_line != line:
                fixes.append(f"添加冒号后空格: {line.strip()[:30]}")
            new_lines.append(new_line)
        code = '\n'.join(new_lines)
        
        # 确保文件末尾有换行
        code = code.rstrip() + '\n'
        
        return code, fixes
    
    def fix_sql_issues(self, code: str) -> Tuple[str, List[str]]:
        """修复SQL问题"""
        fixes = []
        
        # 修复尾部空格
        lines = code.split('\n')
        stripped_lines = [line.rstrip() for line in lines]
        if stripped_lines != lines:
            fixes.append("移除尾部空格")
            code = '\n'.join(stripped_lines)
        
        # 统一关键字大写（可选）
        # keywords = ['SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'TABLE']
        # for kw in keywords:
        #     code = re.sub(r'\b' + kw + r'\b', kw, code, flags=re.IGNORECASE)
        
        # 确保文件末尾有换行
        code = code.rstrip() + '\n'
        
        return code, fixes
    
    def fix_generic_issues(self, code: str) -> Tuple[str, List[str]]:
        """修复通用问题（适用于所有语言）"""
        fixes = []
        
        # 移除尾部空格
        lines = code.split('\n')
        stripped_lines = [line.rstrip() for line in lines]
        if stripped_lines != lines:
            fixes.append("移除尾部空格")
        
        # 统一换行符为\n
        code = '\n'.join(stripped_lines)
        code = code.replace('\r\n', '\n').replace('\r', '\n')
        
        # 确保文件末尾有且只有一个换行
        code = code.rstrip() + '\n'
        
        # 移除空文件中的多余换行
        if code.strip() == '':
            code = ''
        
        return code, fixes
    
    def fix_code_block(self, language: str, code: str) -> Tuple[str, List[str]]:
        """根据语言修复代码块"""
        all_fixes = []
        
        # 通用修复
        code, fixes = self.fix_generic_issues(code)
        all_fixes.extend(fixes)
        
        # 语言特定修复
        if language in ['python', 'py']:
            code, fixes = self.fix_python_indentation(code)
            all_fixes.extend(fixes)
            code, fixes = self.fix_common_python_issues(code)
            all_fixes.extend(fixes)
        elif language in ['java']:
            code, fixes = self.fix_java_issues(code)
            all_fixes.extend(fixes)
        elif language in ['yaml', 'yml']:
            code, fixes = self.fix_yaml_issues(code)
            all_fixes.extend(fixes)
        elif language in ['sql']:
            code, fixes = self.fix_sql_issues(code)
            all_fixes.extend(fixes)
        
        return code, all_fixes
    
    def process_markdown_file(self, file_path: Path) -> List[FixResult]:
        """处理单个Markdown文件"""
        results = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # 匹配代码块
            pattern = r'```(\w+)?\n(.*?)```'
            
            def replace_code_block(match):
                language = (match.group(1) or "text").lower().strip()
                code = match.group(2)
                
                # 标准化语言名称
                lang_map = {"yml": "yaml", "py": "python", "sh": "bash"}
                language = lang_map.get(language, language)
                
                # 修复代码
                fixed_code, fixes = self.fix_code_block(language, code)
                
                if fixes and fixed_code != code:
                    result = FixResult(
                        file_path=str(file_path),
                        block_index=len(results),
                        original_code=code,
                        fixed_code=fixed_code,
                        fixes_applied=fixes,
                        success=True
                    )
                    results.append(result)
                    return f'```{match.group(1) or "text"}\n{fixed_code}```'
                
                return match.group(0)
            
            new_content = re.sub(pattern, replace_code_block, content, flags=re.DOTALL)
            
            # 保存修改
            if not self.dry_run and new_content != original_content:
                file_path.write_text(new_content, encoding='utf-8')
            
        except Exception as e:
            print(f"   ⚠️  处理文件失败: {file_path} - {e}")
        
        return results
    
    def run_fixer(self, validation_results: Optional[Path] = None):
        """运行修复器"""
        print("\n" + "="*60)
        print("🔧 代码示例修复器启动")
        if self.dry_run:
            print("   模式: 预览 (dry-run)")
        else:
            print("   模式: 实际修改")
        print("="*60)
        
        # 如果提供了验证结果，优先处理有问题的文件
        target_files = []
        if validation_results and validation_results.exists():
            with open(validation_results, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 提取有问题的文件路径
                problem_files = set()
                for item in data:
                    if not item.get('is_valid', True):
                        problem_files.add(item['file_path'])
                target_files = [Path(p) for p in problem_files]
                print(f"   从验证结果加载 {len(target_files)} 个有问题的文件")
        
        # 如果没有目标文件，处理所有Markdown文件
        if not target_files:
            target_files = list(self.project_root.rglob("*.md"))
            # 排除某些目录
            exclude_patterns = ['.git', 'node_modules', '__pycache__', '.venv', 'venv']
            target_files = [
                f for f in target_files 
                if not any(excl in str(f) for excl in exclude_patterns)
            ]
            print(f"   扫描到 {len(target_files)} 个Markdown文件")
        
        # 处理文件
        all_results = []
        for i, file_path in enumerate(target_files, 1):
            if i % 50 == 0:
                print(f"   已处理 {i}/{len(target_files)} 个文件...")
            
            results = self.process_markdown_file(file_path)
            all_results.extend(results)
        
        self.fixes_applied = all_results
        
        # 输出统计
        print(f"\n✅ 修复完成!")
        print(f"   处理文件: {len(target_files)}")
        print(f"   修复代码块: {len(all_results)}")
        
        if all_results:
            fix_counts = {}
            for r in all_results:
                for fix in r.fixes_applied:
                    fix_counts[fix] = fix_counts.get(fix, 0) + 1
            
            print("\n📊 修复类型统计:")
            for fix_type, count in sorted(fix_counts.items(), key=lambda x: -x[1])[:10]:
                print(f"   - {fix_type}: {count} 次")
        
        return all_results
    
    def generate_fix_report(self) -> str:
        """生成修复报告"""
        report = f"""# 代码示例修复报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **模式**: {'预览 (dry-run)' if self.dry_run else '实际修改'}  
> **项目根目录**: {self.project_root}

## 📊 修复统计

| 指标 | 数值 |
|------|------|
| 修复的代码块 | {len(self.fixes_applied)} |

## 🔧 修复详情

"""
        
        if not self.fixes_applied:
            report += "✅ 未发现需要修复的问题\n"
        else:
            # 按文件分组
            by_file: dict = {}
            for r in self.fixes_applied:
                fp = r.file_path
                if fp not in by_file:
                    by_file[fp] = []
                by_file[fp].append(r)
            
            for file_path, results in sorted(by_file.items()):
                rel_path = os.path.relpath(file_path, self.project_root)
                report += f"\n### `{rel_path}`\n\n"
                for r in results:
                    report += f"**代码块 #{r.block_index + 1}**\n"
                    report += f"- **修复类型**: {', '.join(r.fixes_applied)}\n"
                    
                    # 显示差异
                    if r.original_code != r.fixed_code:
                        diff = list(unified_diff(
                            r.original_code.splitlines(keepends=True),
                            r.fixed_code.splitlines(keepends=True),
                            fromfile='original',
                            tofile='fixed',
                            lineterm=''
                        ))
                        if diff:
                            report += "- **差异**:\n```diff\n"
                            report += ''.join(diff[:20])  # 限制显示行数
                            if len(diff) > 20:
                                report += "...\n"
                            report += "```\n"
                    report += "\n"
        
        if self.dry_run:
            report += """
## 🚀 下一步操作

当前为预览模式，要实际应用修复，请运行：

```bash
python .scripts/code-example-fixer.py --apply
```

## ⚠️ 注意事项

1. 修复前建议备份项目
2. 修复后请重新运行验证器确认问题已解决
3. 某些复杂问题仍需手动修复

"""
        
        report += """
---
*报告由代码示例修复器自动生成*
"""
        
        return report
    
    def save_fixes_log(self, output_path: Path):
        """保存修复日志"""
        fixes_data = [
            {
                "file_path": r.file_path,
                "block_index": r.block_index,
                "fixes_applied": r.fixes_applied,
                "original_code": r.original_code,
                "fixed_code": r.fixed_code
            }
            for r in self.fixes_applied
        ]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(fixes_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 修复日志已保存: {output_path}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='代码示例修复器')
    parser.add_argument('--project-root', '-p', type=str, default='.',
                        help='项目根目录 (默认: 当前目录)')
    parser.add_argument('--validation-results', '-v', type=str,
                        default='validation-results.json',
                        help='验证结果JSON文件路径')
    parser.add_argument('--apply', '-a', action='store_true',
                        help='实际应用修复 (默认只预览)')
    parser.add_argument('--report', '-r', type=str, default='CODE-EXAMPLE-FIX-REPORT.md',
                        help='报告文件名')
    
    args = parser.parse_args()
    
    # 创建修复器
    fixer = CodeExampleFixer(
        project_root=Path(args.project_root),
        dry_run=not args.apply
    )
    
    # 运行修复
    validation_path = Path(args.validation_results)
    if not validation_path.is_absolute():
        validation_path = Path(args.project_root) / validation_path
    
    results = fixer.run_fixer(validation_path if validation_path.exists() else None)
    
    # 生成并保存报告
    report = fixer.generate_fix_report()
    report_path = Path(args.project_root) / args.report
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n📝 修复报告已保存: {report_path}")
    
    # 保存修复日志
    if results:
        log_path = Path(args.project_root) / 'fixes-applied.json'
        fixer.save_fixes_log(log_path)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
