#!/usr/bin/env python3
"""
Mermaid 语法验证器
检查项目中所有Mermaid图表的语法正确性

用法:
    python mermaid-syntax-validator.py [--strict] [--fix]

选项:
    --strict  严格模式，错误率超过阈值时报错退出
    --fix     尝试自动修复常见语法错误
"""

import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# 支持的Mermaid图表类型
VALID_CHART_TYPES = [
    'graph', 'flowchart', 'sequenceDiagram', 'classDiagram',
    'stateDiagram', 'stateDiagram-v2', 'erDiagram', 'gantt',
    'pie', 'mindmap', 'timeline', 'quadrantChart', 'gitGraph',
    'journey', 'requirementDiagram'
]

# 图的有效方向
VALID_DIRECTIONS = ['TB', 'TD', 'BT', 'RL', 'LR']


class MermaidValidator:
    """Mermaid图表语法验证器"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {
            'total': 0,
            'valid': 0,
            'invalid': 0,
            'by_type': defaultdict(int)
        }
    
    def validate_all(self, directories: list) -> dict:
        """验证所有Markdown文件中的Mermaid图表"""
        mermaid_pattern = re.compile(r'```mermaid\s*\n(.*?)```', re.DOTALL)
        
        for directory in directories:
            dir_path = Path(directory)
            if not dir_path.exists():
                continue
            
            for md_file in dir_path.rglob('*.md'):
                # 跳过隐藏目录
                if any(part.startswith('.') for part in md_file.parts):
                    continue
                
                try:
                    content = md_file.read_text(encoding='utf-8')
                    diagrams = mermaid_pattern.findall(content)
                    
                    for i, diagram in enumerate(diagrams):
                        self.stats['total'] += 1
                        result = self.validate_diagram(diagram, str(md_file), i + 1)
                        
                        if result['valid']:
                            self.stats['valid'] += 1
                        else:
                            self.stats['invalid'] += 1
                        
                        self.errors.extend(result.get('errors', []))
                        self.warnings.extend(result.get('warnings', []))
                        
                except Exception as e:
                    print(f"Warning: Could not process {md_file}: {e}", file=sys.stderr)
        
        return {
            'stats': self.stats,
            'errors': self.errors,
            'warnings': self.warnings
        }
    
    def validate_diagram(self, diagram: str, file_path: str, diagram_num: int) -> dict:
        """验证单个Mermaid图表"""
        errors = []
        warnings = []
        
        lines = diagram.strip().split('\n')
        if not lines:
            return {'valid': False, 'errors': ['Empty diagram']}
        
        first_line = lines[0].strip()
        
        # 1. 检查图表类型
        chart_type = None
        for vt in VALID_CHART_TYPES:
            if first_line.startswith(vt):
                chart_type = vt
                break
        
        if not chart_type:
            errors.append({
                'file': file_path,
                'diagram': diagram_num,
                'type': 'invalid_type',
                'message': f'Unknown chart type: {first_line[:50]}'
            })
            return {'valid': False, 'errors': errors, 'warnings': warnings}
        
        self.stats['by_type'][chart_type] += 1
        
        # 2. 验证特定图表类型的语法
        if chart_type in ['graph', 'flowchart']:
            type_errors = self._validate_graph(diagram)
            errors.extend(type_errors)
        elif chart_type == 'sequenceDiagram':
            type_errors = self._validate_sequence(diagram)
            errors.extend(type_errors)
        elif chart_type in ['stateDiagram', 'stateDiagram-v2']:
            type_errors = self._validate_state_diagram(diagram)
            errors.extend(type_errors)
        elif chart_type == 'classDiagram':
            type_errors = self._validate_class_diagram(diagram)
            errors.extend(type_errors)
        
        # 3. 通用检查
        # 检查括号匹配
        open_brackets = diagram.count('[') + diagram.count('{') + diagram.count('(')
        close_brackets = diagram.count(']') + diagram.count('}') + diagram.count(')')
        if open_brackets != close_brackets:
            errors.append({
                'file': file_path,
                'diagram': diagram_num,
                'type': 'bracket_mismatch',
                'message': f'Unbalanced brackets: {open_brackets} open, {close_brackets} close'
            })
        
        # 检查引号匹配
        if diagram.count('"') % 2 != 0:
            warnings.append({
                'file': file_path,
                'diagram': diagram_num,
                'type': 'quote_warning',
                'message': 'Odd number of double quotes detected'
            })
        
        # 检查空节点
        if re.search(r'\[\s*\]', diagram):
            warnings.append({
                'file': file_path,
                'diagram': diagram_num,
                'type': 'empty_node',
                'message': 'Empty node detected'
            })
        
        is_valid = len([e for e in errors if e['file'] == file_path and e['diagram'] == diagram_num]) == 0
        
        return {
            'valid': is_valid,
            'chart_type': chart_type,
            'errors': errors,
            'warnings': warnings
        }
    
    def _validate_graph(self, diagram: str) -> list:
        """验证graph/flowchart语法"""
        errors = []
        lines = diagram.strip().split('\n')
        
        # 检查方向定义
        first_line = lines[0].strip()
        direction_match = re.search(r'(?:graph|flowchart)\s+(TD|TB|BT|RL|LR)', first_line)
        
        if not direction_match:
            # 检查是否有其他有效定义
            if not re.search(r'(?:graph|flowchart)\s+\w+', first_line):
                errors.append({
                    'type': 'missing_direction',
                    'message': 'Missing direction (TD/TB/RL/LR) in graph definition'
                })
        
        # 检查节点定义语法
        for i, line in enumerate(lines[1:], start=2):
            line = line.strip()
            if not line or line.startswith('%%') or line.startswith('%'):
                continue
            
            # 检查节点定义中的括号匹配
            if '[' in line and ']' not in line:
                errors.append({
                    'type': 'syntax_error',
                    'line': i,
                    'message': f'Unclosed bracket in node definition: {line[:50]}'
                })
            
            if '{' in line and '}' not in line:
                errors.append({
                    'type': 'syntax_error',
                    'line': i,
                    'message': f'Unclosed brace in node definition: {line[:50]}'
                })
            
            # 检查箭头语法
            if '-->' in line:
                # 标准箭头，OK
                pass
            elif '==>' in line:
                # 粗箭头，OK
                pass
            elif '-.->' in line:
                # 虚线箭头，OK
                pass
            elif '--' in line and '>' not in line.split('--')[1][:10] if len(line.split('--')) > 1 else True:
                # 可能是文本箭头但没有箭头
                if '--' in line and '>' not in line:
                    warnings = {'type': 'arrow_warning', 'line': i, 'message': 'Possible missing arrowhead'}
        
        return errors
    
    def _validate_sequence_diagram(self, diagram: str) -> list:
        """验证序列图语法"""
        errors = []
        lines = diagram.strip().split('\n')
        
        participants = set()
        
        for i, line in enumerate(lines[1:], start=2):
            line = line.strip()
            if not line or line.startswith('%%'):
                continue
            
            # 收集参与者
            if line.startswith('participant'):
                match = re.search(r'participant\s+(\w+)', line)
                if match:
                    participants.add(match.group(1))
            elif line.startswith('actor'):
                match = re.search(r'actor\s+(\w+)', line)
                if match:
                    participants.add(match.group(1))
            
            # 检查消息语法
            if '->>' in line or '-->>' in line or '->' in line or '-->' in line:
                # 基本箭头语法检查
                if not re.search(r'(\w+)\s*-[-]?[>]\s*(\w+)\s*:', line):
                    if not re.search(r'(\w+)\s*-[-]?[>]\s*(\w+)', line):
                        errors.append({
                            'type': 'syntax_error',
                            'line': i,
                            'message': f'Invalid sequence diagram message syntax: {line[:50]}'
                        })
        
        return errors
    
    def _validate_state_diagram(self, diagram: str) -> list:
        """验证状态图语法"""
        errors = []
        lines = diagram.strip().split('\n')
        
        for i, line in enumerate(lines[1:], start=2):
            line = line.strip()
            if not line or line.startswith('%%'):
                continue
            
            # 检查状态转移语法
            if '-->' in line:
                if not re.search(r'[\w\s]+-->\s*[\w\s]+', line):
                    errors.append({
                        'type': 'syntax_error',
                        'line': i,
                        'message': f'Invalid state transition: {line[:50]}'
                    })
        
        return errors
    
    def _validate_class_diagram(self, diagram: str) -> list:
        """验证类图语法"""
        errors = []
        lines = diagram.strip().split('\n')
        
        for i, line in enumerate(lines[1:], start=2):
            line = line.strip()
            if not line or line.startswith('%%'):
                continue
            
            # 检查关系语法
            valid_relations = ['<|--', '--|>', '*--', '--*', 'o--', '--o', '-->', '<--', '..>', '<..']
            has_relation = any(rel in line for rel in valid_relations)
            
            if has_relation:
                # 检查是否有类名
                if not re.search(r'\w+\s*[<|\-*o.]+\s*\w+', line):
                    errors.append({
                        'type': 'syntax_error',
                        'line': i,
                        'message': f'Invalid class relationship: {line[:50]}'
                    })
        
        return errors


def generate_report(results: dict, output_path: Path = None) -> str:
    """生成验证报告"""
    stats = results['stats']
    errors = results['errors']
    warnings = results['warnings']
    
    lines = [
        "# Mermaid Syntax Validation Report",
        "",
        f"**Generated**: {datetime.now().isoformat()}",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total Diagrams | {stats['total']} |",
        f"| ✅ Valid | {stats['valid']} |",
        f"| ❌ Invalid | {stats['invalid']} |",
        f"| ⚠️ Warnings | {len(warnings)} |",
        ""
    ]
    
    if stats['by_type']:
        lines.extend([
            "## Diagrams by Type",
            "",
            "| Type | Count |",
            "|------|-------|"
        ])
        
        for chart_type, count in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
            lines.append(f"| {chart_type} | {count} |")
        
        lines.append("")
    
    if errors:
        lines.extend([
            "## ❌ Errors",
            "",
            "| File | Diagram | Type | Message |",
            "|------|---------|------|---------|"
        ])
        
        # 去重并排序
        seen = set()
        unique_errors = []
        for err in errors:
            key = (err.get('file', ''), err.get('diagram', 0), err.get('type', ''), err.get('message', ''))
            if key not in seen:
                seen.add(key)
                unique_errors.append(err)
        
        for err in unique_errors[:50]:  # 限制显示数量
            file_name = err.get('file', 'Unknown')
            diagram_num = err.get('diagram', '-')
            err_type = err.get('type', 'Unknown')
            message = err.get('message', '')[:60]
            lines.append(f"| {file_name} | {diagram_num} | {err_type} | {message} |")
        
        if len(unique_errors) > 50:
            lines.append(f"| ... | ... | ... | *and {len(unique_errors) - 50} more* |")
        
        lines.append("")
    
    if warnings:
        lines.extend([
            "## ⚠️ Warnings",
            "",
            "| File | Diagram | Type | Message |",
            "|------|---------|------|---------|"
        ])
        
        for warn in warnings[:30]:
            file_name = warn.get('file', 'Unknown')
            diagram_num = warn.get('diagram', '-')
            warn_type = warn.get('type', 'Unknown')
            message = warn.get('message', '')[:60]
            lines.append(f"| {file_name} | {diagram_num} | {warn_type} | {message} |")
        
        if len(warnings) > 30:
            lines.append(f"| ... | ... | ... | *and {len(warnings) - 30} more* |")
        
        lines.append("")
    
    # 成功率
    if stats['total'] > 0:
        success_rate = stats['valid'] / stats['total'] * 100
        lines.extend([
            "## Success Rate",
            "",
            f"**{success_rate:.1f}%** ({stats['valid']}/{stats['total']})",
            ""
        ])
    
    lines.extend([
        "---",
        "",
        "*This report was generated by mermaid-syntax-validator.py*"
    ])
    
    report = '\n'.join(lines)
    
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding='utf-8')
    
    # 同时生成JSON报告
    json_path = output_path.parent / 'mermaid-validation-results.json' if output_path else None
    if json_path:
        json_results = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total': stats['total'],
                'valid': stats['valid'],
                'invalid': stats['invalid'],
                'warnings': len(warnings),
                'success_rate': stats['valid'] / stats['total'] * 100 if stats['total'] > 0 else 0
            },
            'by_type': dict(stats['by_type']),
            'errors': errors,
            'warnings': warnings
        }
        json_path.write_text(json.dumps(json_results, indent=2), encoding='utf-8')
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description='Validate Mermaid diagram syntax in Markdown files'
    )
    parser.add_argument(
        '--strict', action='store_true',
        help='Exit with error if validation fails or error rate > 10%'
    )
    parser.add_argument(
        '--fix', action='store_true',
        help='Attempt to auto-fix common syntax errors (not implemented)'
    )
    parser.add_argument(
        '--output', '-o', type=str,
        default='reports/mermaid-validation-report.md',
        help='Output report path'
    )
    parser.add_argument(
        '--dirs', nargs='+',
        default=['Struct', 'Knowledge', 'Flink', 'docs', 'tutorials'],
        help='Directories to scan'
    )
    parser.add_argument(
        '--threshold', type=float, default=0.1,
        help='Error rate threshold for strict mode (default: 0.1 = 10%)'
    )
    
    args = parser.parse_args()
    
    print("🔍 Validating Mermaid diagram syntax...")
    
    validator = MermaidValidator()
    results = validator.validate_all(args.dirs)
    
    stats = results['stats']
    
    print(f"   Total diagrams: {stats['total']}")
    print(f"   Valid: {stats['valid']}")
    print(f"   Invalid: {stats['invalid']}")
    print(f"   Warnings: {len(results['warnings'])}")
    
    # 生成报告
    output_path = Path(args.output)
    report = generate_report(results, output_path)
    print(f"\n📄 Report saved to: {output_path}")
    
    # 严格模式检查
    if args.strict:
        if stats['total'] > 0:
            error_rate = stats['invalid'] / stats['total']
            if error_rate > args.threshold:
                print(f"\n❌ Error rate {error_rate:.1%} exceeds threshold ({args.threshold:.0%})")
                sys.exit(1)
        
        if results['errors']:
            print(f"\n❌ Found {len(results['errors'])} validation errors")
            sys.exit(1)
    
    print("\n✅ Mermaid validation completed")
    sys.exit(0)


if __name__ == '__main__':
    main()
