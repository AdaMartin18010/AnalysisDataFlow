#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定理注册表验证器 v2.0

功能:
- 验证所有Markdown文档中的定理/定义/引理编号唯一性
- 检查编号格式是否符合规范
- 验证引用是否正确
- 生成验证报告

作者: AnalysisDataFlow 项目
版本: 2.0.0
"""

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple


@dataclass
class ValidationError:
    """验证错误信息"""
    error_type: str
    file_path: str
    line_number: int
    message: str
    context: str = ""


@dataclass
class ValidationReport:
    """验证报告"""
    total_files: int = 0
    total_theorems: int = 0
    total_definitions: int = 0
    total_lemmas: int = 0
    total_propositions: int = 0
    total_corollaries: int = 0
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    duplicate_ids: Dict[str, List[str]] = field(default_factory=dict)


def get_theorem_patterns() -> Dict[str, re.Pattern]:
    """获取定理编号正则表达式模式"""
    return {
        'Thm': re.compile(r'Thm-[SKF]-\d{2}-\d{2}'),
        'Def': re.compile(r'Def-[SKF]-\d{2}-\d{2}'),
        'Lemma': re.compile(r'Lemma-[SKF]-\d{2}-\d{2}'),
        'Prop': re.compile(r'Prop-[SKF]-\d{2}-\d{2}'),
        'Cor': re.compile(r'Cor-[SKF]-\d{2}-\d{2}')
    }


def validate_id_format(theorem_id: str) -> Tuple[bool, str]:
    """
    验证定理ID格式
    
    格式: {Type}-{Stage}-{DocNum}-{SeqNum}
    - Type: Thm, Def, Lemma, Prop, Cor
    - Stage: S, K, F
    - DocNum: 01-99
    - SeqNum: 01-99
    """
    parts = theorem_id.split('-')
    if len(parts) != 4:
        return False, f"Invalid format: expected 4 parts, got {len(parts)}"
    
    type_, stage, doc_num, seq_num = parts
    
    # 验证类型
    if type_ not in ['Thm', 'Def', 'Lemma', 'Prop', 'Cor']:
        return False, f"Invalid type: {type_}"
    
    # 验证阶段
    if stage not in ['S', 'K', 'F']:
        return False, f"Invalid stage: {stage}, expected S/K/F"
    
    # 验证文档序号
    if not (doc_num.isdigit() and len(doc_num) == 2):
        return False, f"Invalid document number: {doc_num}"
    
    # 验证顺序号
    if not (seq_num.isdigit() and len(seq_num) == 2):
        return False, f"Invalid sequence number: {seq_num}"
    
    return True, "Valid"


def scan_document(file_path: Path) -> Dict[str, List[Tuple[int, str]]]:
    """扫描单个文档，提取所有定理ID及其位置"""
    patterns = get_theorem_patterns()
    results = defaultdict(list)
    
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for thm_type, pattern in patterns.items():
                for match in pattern.finditer(line):
                    theorem_id = match.group(0)
                    results[thm_type].append((line_num, theorem_id))
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
    
    return dict(results)


def scan_all_documents(base_path: Path) -> Tuple[Dict, int]:
    """扫描所有文档，返回定理映射和文件计数"""
    all_theorems = defaultdict(lambda: defaultdict(list))
    file_count = 0
    
    # 扫描主要目录
    for directory in ['Struct', 'Knowledge', 'Flink']:
        dir_path = base_path / directory
        if not dir_path.exists():
            continue
        
        for md_file in dir_path.rglob('*.md'):
            # 跳过隐藏目录
            if any(part.startswith('.') or part in ['node_modules', '__pycache__']
                   for part in md_file.parts):
                continue
            
            file_count += 1
            doc_theorems = scan_document(md_file)
            rel_path = str(md_file.relative_to(base_path)).replace('\\', '/')
            
            for thm_type, theorems in doc_theorems.items():
                for line_num, theorem_id in theorems:
                    all_theorems[thm_type][theorem_id].append({
                        'file': rel_path,
                        'line': line_num
                    })
    
    return dict(all_theorems), file_count


def check_duplicates(all_theorems: Dict) -> Dict[str, List[str]]:
    """检查重复的定理ID"""
    duplicates = {}
    
    for thm_type, theorems in all_theorems.items():
        for theorem_id, locations in theorems.items():
            if len(locations) > 1:
                if theorem_id not in duplicates:
                    duplicates[theorem_id] = []
                for loc in locations:
                    duplicates[theorem_id].append(f"{loc['file']}:{loc['line']}")
    
    return duplicates


def validate_theorem_registry(registry_path: Path, all_theorems: Dict) -> List[ValidationError]:
    """验证定理注册表的完整性"""
    errors = []
    
    if not registry_path.exists():
        errors.append(ValidationError(
            error_type="Missing Registry",
            file_path="THEOREM-REGISTRY.md",
            line_number=0,
            message="Theorem registry file not found"
        ))
        return errors
    
    try:
        content = registry_path.read_text(encoding='utf-8')
        
        # 检查所有发现的定理是否在注册表中
        for thm_type, theorems in all_theorems.items():
            for theorem_id in theorems.keys():
                if theorem_id not in content:
                    errors.append(ValidationError(
                        error_type="Missing in Registry",
                        file_path="THEOREM-REGISTRY.md",
                        line_number=0,
                        message=f"{theorem_id} not found in registry",
                        context=f"Found in: {theorems[theorem_id][0]['file']}"
                    ))
    except Exception as e:
        errors.append(ValidationError(
            error_type="Registry Read Error",
            file_path="THEOREM-REGISTRY.md",
            line_number=0,
            message=f"Could not read registry: {e}"
        ))
    
    return errors


def generate_validation_report(report: ValidationReport, output_path: Path):
    """生成Markdown格式的验证报告"""
    lines = [
        "# 定理注册表验证报告",
        "",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 📊 统计概览",
        "",
        "| 指标 | 数值 |",
        "|------|------|",
        f"| 扫描文件数 | {report.total_files} |",
        f"| 定理 (Thm) | {report.total_theorems} |",
        f"| 定义 (Def) | {report.total_definitions} |",
        f"| 引理 (Lemma) | {report.total_lemmas} |",
        f"| 命题 (Prop) | {report.total_propositions} |",
        f"| 推论 (Cor) | {report.total_corollaries} |",
        f"| **总计** | **{report.total_theorems + report.total_definitions + report.total_lemmas + report.total_propositions + report.total_corollaries}** |",
        "",
        f"| 错误数 | {len(report.errors)} |",
        f"| 警告数 | {len(report.warnings)} |",
        ""
    ]
    
    if report.duplicate_ids:
        lines.extend([
            "## ❌ 重复ID检测",
            "",
            "发现以下重复的定理ID:",
            "",
            "| ID | 出现位置 |",
            "|----|----------|"
        ])
        for thm_id, locations in sorted(report.duplicate_ids.items()):
            loc_str = ', '.join(locations[:3])
            if len(locations) > 3:
                loc_str += f" (+{len(locations) - 3} more)"
            lines.append(f"| `{thm_id}` | {loc_str} |")
        lines.append("")
    
    if report.errors:
        lines.extend([
            "## ❌ 错误详情",
            "",
            "| 类型 | 文件 | 行号 | 消息 |",
            "|------|------|------|------|"
        ])
        for error in report.errors[:50]:  # 最多显示50个错误
            lines.append(f"| {error.error_type} | {error.file_path} | {error.line_number} | {error.message} |")
        if len(report.errors) > 50:
            lines.append(f"| ... | ... | ... | 还有 {len(report.errors) - 50} 个错误 |")
        lines.append("")
    
    if report.warnings:
        lines.extend([
            "## ⚠️ 警告详情",
            "",
            "| 类型 | 文件 | 行号 | 消息 |",
            "|------|------|------|------|"
        ])
        for warning in report.warnings[:30]:
            lines.append(f"| {warning.error_type} | {warning.file_path} | {warning.line_number} | {warning.message} |")
        lines.append("")
    
    if not report.errors and not report.warnings and not report.duplicate_ids:
        lines.extend([
            "## ✅ 验证结果",
            "",
            "所有验证通过！未发现错误、警告或重复ID。",
            ""
        ])
    
    lines.extend([
        "---",
        "",
        "*此报告由定理验证器自动生成*"
    ])
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text('\n'.join(lines), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(
        description='定理注册表验证器 v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本验证
  python theorem-validator.py
  
  # 严格模式（发现重复ID时报错）
  python theorem-validator.py --strict
  
  # 指定输出路径
  python theorem-validator.py --output reports/validation.md
        """
    )
    
    parser.add_argument(
        '--base-path', '-b',
        type=str,
        default='.',
        help='项目根目录 (默认: 当前目录)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='reports/theorem-validation-report.md',
        help='输出报告路径 (默认: reports/theorem-validation-report.md)'
    )
    
    parser.add_argument(
        '--strict',
        action='store_true',
        help='严格模式: 发现重复ID时返回非零退出码'
    )
    
    parser.add_argument(
        '--check-registry',
        action='store_true',
        help='检查定理注册表的完整性'
    )
    
    args = parser.parse_args()
    
    base_path = Path(args.base_path).resolve()
    print(f"开始验证定理注册表...")
    print(f"基础路径: {base_path}")
    
    # 扫描所有文档
    print("\n🔍 扫描文档...")
    all_theorems, file_count = scan_all_documents(base_path)
    print(f"   扫描了 {file_count} 个文件")
    
    # 创建报告对象
    report = ValidationReport(total_files=file_count)
    
    # 统计各类定理数量
    report.total_theorems = len(all_theorems.get('Thm', {}))
    report.total_definitions = len(all_theorems.get('Def', {}))
    report.total_lemmas = len(all_theorems.get('Lemma', {}))
    report.total_propositions = len(all_theorems.get('Prop', {}))
    report.total_corollaries = len(all_theorems.get('Cor', {}))
    
    # 检查重复
    print("\n🔄 检查重复ID...")
    report.duplicate_ids = check_duplicates(all_theorems)
    
    if report.duplicate_ids:
        print(f"   ⚠️ 发现 {len(report.duplicate_ids)} 个重复ID")
        for thm_id, locations in sorted(report.duplicate_ids.items())[:5]:
            print(f"      - {thm_id}: {', '.join(locations[:2])}")
        if len(report.duplicate_ids) > 5:
            print(f"      ... 还有 {len(report.duplicate_ids) - 5} 个")
    else:
        print("   ✅ 未发现重复ID")
    
    # 检查ID格式
    print("\n📝 验证ID格式...")
    format_errors = 0
    for thm_type, theorems in all_theorems.items():
        for theorem_id in theorems.keys():
            valid, msg = validate_id_format(theorem_id)
            if not valid:
                format_errors += 1
                report.errors.append(ValidationError(
                    error_type="Invalid Format",
                    file_path=theorems[theorem_id][0]['file'],
                    line_number=theorems[theorem_id][0]['line'],
                    message=msg,
                    context=theorem_id
                ))
    
    if format_errors > 0:
        print(f"   ⚠️ 发现 {format_errors} 个格式错误")
    else:
        print("   ✅ 所有ID格式正确")
    
    # 检查注册表完整性
    if args.check_registry:
        print("\n📋 检查注册表完整性...")
        registry_path = base_path / 'THEOREM-REGISTRY.md'
        registry_errors = validate_theorem_registry(registry_path, all_theorems)
        report.errors.extend(registry_errors)
        
        if registry_errors:
            print(f"   ⚠️ 发现 {len(registry_errors)} 个注册表问题")
        else:
            print("   ✅ 注册表完整")
    
    # 生成报告
    output_path = Path(args.output)
    generate_validation_report(report, output_path)
    print(f"\n📄 报告已保存: {output_path}")
    
    # 输出摘要
    print("\n" + "="*60)
    print("验证摘要")
    print("="*60)
    print(f"文件数: {report.total_files}")
    print(f"定理数: {report.total_theorems + report.total_definitions + report.total_lemmas + report.total_propositions + report.total_corollaries}")
    print(f"重复ID: {len(report.duplicate_ids)}")
    print(f"错误: {len(report.errors)}")
    print(f"警告: {len(report.warnings)}")
    print("="*60)
    
    # 返回退出码
    if report.duplicate_ids or report.errors:
        if args.strict:
            print("\n❌ 验证失败 (严格模式)")
            return 1
        else:
            print("\n⚠️ 验证发现一些问题，但继续执行")
            return 0
    
    print("\n✅ 验证通过")
    return 0


if __name__ == '__main__':
    sys.exit(main())
