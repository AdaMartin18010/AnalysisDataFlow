#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
六段式模板合规性审计脚本
检查Struct/目录下文档是否符合六段式模板规范
"""

import os
import re
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple


@dataclass
class SectionCheck:
    """单个章节的检查结果"""
    name: str
    required: bool
    found: bool
    line_number: int = -1
    content_length: int = 0
    issues: List[str] = field(default_factory=list)


@dataclass
class DocumentAuditResult:
    """单篇文档的审计结果"""
    file_path: str
    file_name: str
    total_sections: int = 0
    required_sections_found: int = 0
    sections: List[SectionCheck] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    is_compliant: bool = False
    has_title: bool = False
    has_metadata: bool = False


class SixSectionAuditor:
    """六段式模板合规性审计器"""
    
    # 必需的8个章节（标准命名）
    REQUIRED_SECTIONS = [
        ("概念定义", ["概念定义", "definitions", "definition", "1. 概念定义"]),
        ("属性推导", ["属性推导", "properties", "property", "2. 属性推导"]),
        ("关系建立", ["关系建立", "relations", "relation", "3. 关系建立", "关系建立"]),
        ("论证过程", ["论证过程", "argumentation", "4. 论证过程"]),
        ("形式证明", ["形式证明", "proof", "engineering argument", "5. 形式证明", "工程论证", "形式证明 / 工程论证"]),
        ("实例验证", ["实例验证", "examples", "example", "6. 实例验证"]),
        ("可视化", ["可视化", "visualizations", "visualization", "7. 可视化"]),
        ("引用参考", ["引用参考", "references", "reference", "8. 引用参考"]),
    ]
    
    # Markdown标题正则
    HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    
    def __init__(self, base_path: str = "Struct"):
        self.base_path = Path(base_path)
        self.results: List[DocumentAuditResult] = []
        
    def find_all_md_files(self) -> List[Path]:
        """查找所有Markdown文件"""
        md_files = []
        if self.base_path.exists():
            md_files = list(self.base_path.rglob("*.md"))
        return sorted(md_files)
    
    def extract_sections(self, content: str) -> List[Tuple[int, str, int]]:
        """提取文档中的所有章节标题
        返回: [(行号, 标题级别, 标题文本), ...]
        """
        sections = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            match = self.HEADING_PATTERN.match(line.strip())
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                sections.append((line_num, level, title))
        
        return sections
    
    def check_section_match(self, title: str, patterns: List[str]) -> bool:
        """检查标题是否匹配给定的模式列表"""
        title_lower = title.lower()
        for pattern in patterns:
            if pattern.lower() in title_lower:
                return True
        return False
    
    def get_section_content_length(self, content: str, section_start_line: int, 
                                    sections: List[Tuple[int, int, str]]) -> int:
        """获取章节内容长度（字符数）"""
        lines = content.split('\n')
        if section_start_line > len(lines):
            return 0
        
        # 找到下一个同级或更高级别的标题作为结束
        start_idx = section_start_line - 1
        section_level = None
        
        for line_num, level, title in sections:
            if line_num == section_start_line:
                section_level = level
                break
        
        if section_level is None:
            return 0
        
        # 找到章节结束位置
        end_idx = len(lines)
        for line_num, level, title in sections:
            if line_num > section_start_line and level <= section_level:
                end_idx = line_num - 1
                break
        
        content_lines = lines[start_idx+1:end_idx]
        content_text = '\n'.join(content_lines).strip()
        return len(content_text)
    
    def audit_document(self, file_path: Path) -> DocumentAuditResult:
        """审计单篇文档"""
        result = DocumentAuditResult(
            file_path=str(file_path),
            file_name=file_path.name
        )
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            result.issues.append(f"读取文件失败: {str(e)}")
            return result
        
        # 检查是否有标题（一级标题）
        lines = content.split('\n')
        if lines and lines[0].startswith('# '):
            result.has_title = True
        
        # 检查是否有元数据（通常在第一行或第二行，包含"所属阶段"等）
        first_few_lines = '\n'.join(lines[:10])
        if '所属阶段' in first_few_lines or '阶段' in first_few_lines or '前置依赖' in first_few_lines:
            result.has_metadata = True
        
        # 提取所有章节
        sections = self.extract_sections(content)
        result.total_sections = len(sections)
        
        # 检查必需章节
        found_required = set()
        section_checks = []
        
        for req_name, patterns in self.REQUIRED_SECTIONS:
            section_check = SectionCheck(
                name=req_name,
                required=True,
                found=False
            )
            
            for line_num, level, title in sections:
                if self.check_section_match(title, patterns):
                    section_check.found = True
                    section_check.line_number = line_num
                    section_check.content_length = self.get_section_content_length(
                        content, line_num, sections
                    )
                    found_required.add(req_name)
                    
                    # 检查内容是否为空
                    if section_check.content_length < 50:
                        section_check.issues.append(f"内容过短 ({section_check.content_length} 字符)")
                    break
            
            if not section_check.found:
                section_check.issues.append("章节缺失")
            
            section_checks.append(section_check)
        
        result.sections = section_checks
        result.required_sections_found = len(found_required)
        
        # 判断是否合规（所有必需章节都存在且有足够内容）
        all_sections_found = all(sc.found for sc in section_checks)
        all_sections_have_content = all(
            sc.content_length >= 50 for sc in section_checks if sc.found
        )
        
        result.is_compliant = all_sections_found and all_sections_have_content and result.has_title
        
        # 收集问题
        if not result.has_title:
            result.issues.append("缺少一级标题 (# 标题)")
        
        if not result.has_metadata:
            result.issues.append("缺少元数据（所属阶段、前置依赖等）")
        
        for sc in section_checks:
            if not sc.found:
                result.issues.append(f"缺少章节: {sc.name}")
            elif sc.content_length < 50:
                result.issues.append(f"章节内容过短: {sc.name} ({sc.content_length} 字符)")
        
        return result
    
    def run_audit(self) -> Dict:
        """执行完整审计"""
        md_files = self.find_all_md_files()
        
        print(f"找到 {len(md_files)} 篇Markdown文档")
        print("=" * 60)
        
        for i, file_path in enumerate(md_files, 1):
            print(f"[{i}/{len(md_files)}] 审计: {file_path}")
            result = self.audit_document(file_path)
            self.results.append(result)
        
        return self.generate_report()
    
    def generate_report(self) -> Dict:
        """生成审计报告"""
        total_docs = len(self.results)
        compliant_docs = [r for r in self.results if r.is_compliant]
        non_compliant_docs = [r for r in self.results if not r.is_compliant]
        
        compliance_rate = len(compliant_docs) / total_docs * 100 if total_docs > 0 else 0
        
        # 统计每个必需章节的缺失情况
        section_stats = {}
        for req_name, _ in self.REQUIRED_SECTIONS:
            missing_count = sum(
                1 for r in self.results 
                if any(sc.name == req_name and not sc.found for sc in r.sections)
            )
            section_stats[req_name] = {
                "missing_count": missing_count,
                "missing_rate": missing_count / total_docs * 100 if total_docs > 0 else 0
            }
        
        report = {
            "summary": {
                "total_documents": total_docs,
                "compliant_documents": len(compliant_docs),
                "non_compliant_documents": len(non_compliant_docs),
                "compliance_rate": round(compliance_rate, 2)
            },
            "section_statistics": section_stats,
            "compliant_documents": [
                {
                    "file": r.file_name,
                    "path": r.file_path,
                    "sections_found": r.required_sections_found
                }
                for r in compliant_docs
            ],
            "non_compliant_documents": [
                {
                    "file": r.file_name,
                    "path": r.file_path,
                    "sections_found": r.required_sections_found,
                    "issues": r.issues
                }
                for r in non_compliant_docs
            ],
            "detailed_results": [
                {
                    "file": r.file_name,
                    "path": r.file_path,
                    "is_compliant": r.is_compliant,
                    "has_title": r.has_title,
                    "has_metadata": r.has_metadata,
                    "total_sections": r.total_sections,
                    "required_sections_found": r.required_sections_found,
                    "sections": [
                        {
                            "name": sc.name,
                            "found": sc.found,
                            "line_number": sc.line_number,
                            "content_length": sc.content_length,
                            "issues": sc.issues
                        }
                        for sc in r.sections
                    ],
                    "issues": r.issues
                }
                for r in self.results
            ]
        }
        
        return report


def print_report(report: Dict):
    """打印格式化的审计报告"""
    summary = report["summary"]
    
    print("\n" + "=" * 80)
    print("六段式模板合规性审计报告")
    print("=" * 80)
    
    print("\n【审计摘要】")
    print(f"  总文档数: {summary['total_documents']}")
    print(f"  合规文档: {summary['compliant_documents']}")
    print(f"  不合规文档: {summary['non_compliant_documents']}")
    print(f"  合规率: {summary['compliance_rate']}%")
    
    print("\n【章节合规统计】")
    for section_name, stats in report["section_statistics"].items():
        status = "⚠️" if stats["missing_count"] > 0 else "✅"
        print(f"  {status} {section_name}: 缺失 {stats['missing_count']} 篇 ({stats['missing_rate']:.1f}%)")
    
    print("\n【合规文档列表】")
    if report["compliant_documents"]:
        for doc in report["compliant_documents"]:
            print(f"  ✅ {doc['file']}")
    else:
        print("  无")
    
    print("\n【不合规文档列表及问题】")
    if report["non_compliant_documents"]:
        for doc in report["non_compliant_documents"]:
            print(f"\n  ❌ {doc['file']}")
            print(f"     路径: {doc['path']}")
            print(f"     找到章节: {doc['sections_found']}/8")
            for issue in doc["issues"]:
                print(f"     - {issue}")
    else:
        print("  无")
    
    print("\n【修复建议】")
    non_compliant_count = len(report["non_compliant_documents"])
    if non_compliant_count > 0:
        print(f"1. 共有 {non_compliant_count} 篇文档需要修复")
        
        # 统计最常见的问题
        all_issues = []
        for doc in report["non_compliant_documents"]:
            all_issues.extend(doc["issues"])
        
        issue_counts = {}
        for issue in all_issues:
            # 简化问题分类
            if "缺少章节" in issue:
                key = "章节缺失"
            elif "内容过短" in issue:
                key = "内容过短"
            elif "缺少一级标题" in issue:
                key = "缺少标题"
            elif "缺少元数据" in issue:
                key = "缺少元数据"
            else:
                key = issue
            issue_counts[key] = issue_counts.get(key, 0) + 1
        
        print("2. 常见问题分类:")
        for issue, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
            print(f"   - {issue}: {count} 次")
        
        print("3. 优先级建议:")
        print("   P0: 修复章节缺失问题（影响合规性判断）")
        print("   P1: 补充元数据信息（所属阶段、前置依赖）")
        print("   P2: 扩充章节内容至50字符以上")
        print("   P3: 统一章节命名规范")
    else:
        print("所有文档均符合六段式模板规范！")
    
    print("\n" + "=" * 80)


def main():
    """主函数"""
    auditor = SixSectionAuditor("Struct")
    report = auditor.run_audit()
    
    # 打印报告
    print_report(report)
    
    # 保存详细报告到JSON
    output_file = "six_section_audit_report.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细报告已保存到: {output_file}")
    
    # 生成Markdown格式的修复任务清单
    generate_fix_task_list(report)


def generate_fix_task_list(report: Dict):
    """生成修复任务清单"""
    lines = [
        "# 六段式模板合规性修复任务清单\n",
        f"生成时间: 2026-04-09\n",
        f"总文档数: {report['summary']['total_documents']}\n",
        f"合规文档: {report['summary']['compliant_documents']}\n",
        f"不合规文档: {report['summary']['non_compliant_documents']}\n",
        f"合规率: {report['summary']['compliance_rate']}%\n",
        "\n## 不合规文档修复任务\n"
    ]
    
    for i, doc in enumerate(report["non_compliant_documents"], 1):
        lines.append(f"\n### {i}. {doc['file']}\n")
        lines.append(f"- **路径**: `{doc['path']}`\n")
        lines.append(f"- **当前章节数**: {doc['sections_found']}/8\n")
        lines.append(f"- **问题列表**:\n")
        for issue in doc["issues"]:
            lines.append(f"  - [ ] {issue}\n")
        lines.append(f"- **修复优先级**: {'P0' if doc['sections_found'] < 5 else 'P1'}\n")
    
    output_file = "six_section_fix_tasks.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"修复任务清单已保存到: {output_file}")


if __name__ == "__main__":
    main()
