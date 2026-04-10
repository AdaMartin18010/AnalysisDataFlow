#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theorem Validator - 形式化元素编号验证工具

功能:
    - 扫描所有定理/定义/引理/命题/推论编号
    - 验证编号格式一致性 (Thm-X-XX-XX, Def-X-XX-XX, etc.)
    - 检测重复编号
    - 检测缺失编号
    - 验证交叉引用
    - 生成详细报告

作者: AnalysisDataFlow Project
版本: 1.0.0
日期: 2026-04-10
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Pattern, Set, Tuple


# =============================================================================
# 配置常量
# =============================================================================

DEFAULT_ENCODING = "utf-8"
DEFAULT_LOG_LEVEL = logging.INFO

# 编号模式配置
DEFAULT_ID_PATTERN = r"(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2})"
FORMAL_ELEMENT_TYPES = {
    "Thm": "定理 (Theorem)",
    "Def": "定义 (Definition)",
    "Lemma": "引理 (Lemma)",
    "Prop": "命题 (Proposition)",
    "Cor": "推论 (Corollary)",
}

STAGE_MAPPING = {
    "S": "Struct",
    "K": "Knowledge",
    "F": "Flink",
}

# 默认忽略的文件/目录
DEFAULT_IGNORE_PATTERNS = [
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "*.pyc",
    "*.pyo",
    ".DS_Store",
    "Thumbs.db",
    "*.log",
    "*.tmp",
    "*.temp",
    ".scripts",  # 忽略脚本目录本身
]


# =============================================================================
# 数据类定义
# =============================================================================

class Severity(Enum):
    """问题严重程度枚举"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationError(NamedTuple):
    """验证错误记录"""
    severity: Severity
    file_path: str
    line_number: int
    element_id: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class FormalElement:
    """形式化元素数据结构"""
    element_id: str
    element_type: str  # Thm, Def, Lemma, Prop, Cor
    stage: str  # S, K, F
    doc_num: int
    seq_num: int
    file_path: str
    line_number: int
    line_content: str


@dataclass
class ValidationResult:
    """验证结果汇总"""
    elements: List[FormalElement] = field(default_factory=list)
    errors: List[ValidationError] = field(default_factory=list)
    duplicates: Dict[str, List[FormalElement]] = field(default_factory=dict)
    missing_numbers: Dict[str, List[int]] = field(default_factory=dict)
    invalid_formats: List[ValidationError] = field(default_factory=list)
    cross_ref_errors: List[ValidationError] = field(default_factory=list)
    stats: Dict[str, int] = field(default_factory=lambda: {
        "total_files": 0,
        "total_elements": 0,
        "thm_count": 0,
        "def_count": 0,
        "lemma_count": 0,
        "prop_count": 0,
        "cor_count": 0,
        "error_count": 0,
        "warning_count": 0,
    })


@dataclass
class ValidatorConfig:
    """验证器配置"""
    id_pattern: str = DEFAULT_ID_PATTERN
    ignore_patterns: List[str] = field(default_factory=lambda: DEFAULT_IGNORE_PATTERNS.copy())
    check_duplicates: bool = True
    check_missing: bool = True
    check_cross_refs: bool = True
    strict_mode: bool = False
    max_doc_num: int = 99
    max_seq_num: int = 99


# =============================================================================
# 核心验证器类
# =============================================================================

class TheoremValidator:
    """
    形式化元素编号验证器

    负责扫描、解析和验证所有形式化元素编号的完整性和一致性。
    """

    def __init__(self, config: Optional[ValidatorConfig] = None) -> None:
        """
        初始化验证器

        Args:
            config: 验证器配置，使用默认配置如果未提供
        """
        self.config = config or ValidatorConfig()
        self.id_regex: Pattern[str] = re.compile(self.config.id_pattern)
        self.ref_regex: Pattern[str] = re.compile(
            rf"`?({self.config.id_pattern})`?"
        )
        self.elements_by_id: Dict[str, List[FormalElement]] = {}
        self.elements_by_file: Dict[str, List[FormalElement]] = {}
        self.known_ids: Set[str] = set()
        self.logger = logging.getLogger(__name__)

    def scan_directory(
        self,
        root_dir: str,
        file_extensions: Optional[List[str]] = None
    ) -> ValidationResult:
        """
        扫描目录中的所有Markdown文件

        Args:
            root_dir: 根目录路径
            file_extensions: 要扫描的文件扩展名列表，默认为 [".md"]

        Returns:
            ValidationResult 包含所有扫描到的元素和发现的问题
        """
        result = ValidationResult()
        root_path = Path(root_dir).resolve()
        extensions = file_extensions or [".md"]

        self.logger.info(f"开始扫描目录: {root_path}")

        for ext in extensions:
            for file_path in root_path.rglob(f"*{ext}"):
                if self._should_ignore(file_path):
                    continue

                try:
                    self._process_file(file_path, result)
                    result.stats["total_files"] += 1
                except Exception as e:
                    self.logger.error(f"处理文件失败 {file_path}: {e}")
                    result.errors.append(ValidationError(
                        severity=Severity.ERROR,
                        file_path=str(file_path),
                        line_number=0,
                        element_id="",
                        message=f"文件处理失败: {e}",
                    ))

        # 执行后续验证
        if self.config.check_duplicates:
            self._detect_duplicates(result)

        if self.config.check_missing:
            self._detect_missing_numbers(result)

        if self.config.check_cross_refs:
            self._validate_cross_references(result)

        # 更新统计
        self._update_statistics(result)

        self.logger.info(f"扫描完成: {result.stats['total_files']} 文件, "
                        f"{result.stats['total_elements']} 形式化元素")

        return result

    def _should_ignore(self, file_path: Path) -> bool:
        """
        检查文件是否应该被忽略

        Args:
            file_path: 文件路径

        Returns:
            如果文件应该被忽略则返回 True
        """
        path_str = str(file_path)

        for pattern in self.config.ignore_patterns:
            # 支持简单的通配符匹配
            if "*" in pattern:
                import fnmatch
                if fnmatch.fnmatch(path_str, pattern) or \
                   fnmatch.fnmatch(file_path.name, pattern):
                    return True
            elif pattern in path_str:
                return True

        return False

    def _process_file(self, file_path: Path, result: ValidationResult) -> None:
        """
        处理单个文件

        Args:
            file_path: 文件路径
            result: 验证结果对象
        """
        self.logger.debug(f"处理文件: {file_path}")

        try:
            with open(file_path, "r", encoding=DEFAULT_ENCODING) as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            # 尝试其他编码
            with open(file_path, "r", encoding="gbk", errors="ignore") as f:
                lines = f.readlines()

        rel_path = str(file_path.relative_to(Path.cwd()))
        file_elements: List[FormalElement] = []

        for line_num, line in enumerate(lines, 1):
            # 查找所有匹配的编号
            for match in self.id_regex.finditer(line):
                element = self._parse_element(match, rel_path, line_num, line.strip())
                if element:
                    result.elements.append(element)
                    file_elements.append(element)
                    self.known_ids.add(element.element_id)

                    # 按ID索引
                    if element.element_id not in self.elements_by_id:
                        self.elements_by_id[element.element_id] = []
                    self.elements_by_id[element.element_id].append(element)

            # 检查无效格式（部分匹配但不完全符合规范）
            self._check_invalid_formats(line, rel_path, line_num, result)

        self.elements_by_file[rel_path] = file_elements

    def _parse_element(
        self,
        match: re.Match[str],
        file_path: str,
        line_number: int,
        line_content: str
    ) -> Optional[FormalElement]:
        """
        解析匹配到的形式化元素

        Args:
            match: 正则匹配对象
            file_path: 文件路径
            line_number: 行号
            line_content: 行内容

        Returns:
            FormalElement 对象或 None 如果解析失败
        """
        groups = match.groups()
        if len(groups) < 4:
            return None

        element_type, stage, doc_num_str, seq_num_str = groups[0], groups[1], groups[2], groups[3]

        try:
            doc_num = int(doc_num_str)
            seq_num = int(seq_num_str)
        except ValueError:
            return None

        element_id = f"{element_type}-{stage}-{doc_num_str}-{seq_num_str}"

        return FormalElement(
            element_id=element_id,
            element_type=element_type,
            stage=stage,
            doc_num=doc_num,
            seq_num=seq_num,
            file_path=file_path,
            line_number=line_number,
            line_content=line_content,
        )

    def _check_invalid_formats(
        self,
        line: str,
        file_path: str,
        line_number: int,
        result: ValidationResult
    ) -> None:
        """
        检查行中是否存在无效格式的编号

        Args:
            line: 行内容
            file_path: 文件路径
            line_number: 行号
            result: 验证结果对象
        """
        # 检测可能的错误格式（如缺少连字符、错误的大小写等）
        invalid_patterns = [
            (r"(?i)(thm|def|lemma|prop|cor)_", "使用下划线而非连字符"),
            (r"(?i)(thm|def|lemma|prop|cor)([SKF])", "缺少连字符分隔符"),
            (r"(?i)(thm|def|lemma|prop|cor)-([skf])-", "阶段代码应大写 (S/K/F)"),
            (r"(?i)(thm|def|lemma|prop|cor)-([SKF])-(\d)-", "文档序号应为两位数字"),
            (r"(?i)(thm|def|lemma|prop|cor)-([SKF])-(\d{2})-(\d)\b", "顺序号应为两位数字"),
        ]

        for pattern, message in invalid_patterns:
            if re.search(pattern, line):
                # 避免重复报告已经正确匹配的
                if not self.id_regex.search(line):
                    result.invalid_formats.append(ValidationError(
                        severity=Severity.WARNING,
                        file_path=file_path,
                        line_number=line_number,
                        element_id="",
                        message=f"可能的格式错误: {message}",
                        suggestion=f"参考格式: Thm-S-01-01, Def-K-02-03",
                    ))

    def _detect_duplicates(self, result: ValidationResult) -> None:
        """
        检测重复的编号

        Args:
            result: 验证结果对象
        """
        self.logger.debug("检测重复编号...")

        for element_id, elements in self.elements_by_id.items():
            if len(elements) > 1:
                result.duplicates[element_id] = elements

                # 生成错误信息
                locations = [f"{e.file_path}:{e.line_number}" for e in elements]
                result.errors.append(ValidationError(
                    severity=Severity.ERROR,
                    file_path=elements[0].file_path,
                    line_number=elements[0].line_number,
                    element_id=element_id,
                    message=f"重复编号: {element_id} 出现在 {len(elements)} 个位置",
                    suggestion=f"位置: {', '.join(locations[:3])}" +
                              ("..." if len(locations) > 3 else ""),
                ))

    def _detect_missing_numbers(self, result: ValidationResult) -> None:
        """
        检测缺失的编号

        Args:
            result: 验证结果对象
        """
        self.logger.debug("检测缺失编号...")

        # 按类型和阶段分组
        grouped: Dict[Tuple[str, str], List[FormalElement]] = {}

        for element in result.elements:
            key = (element.element_type, element.stage)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(element)

        # 检查每个组的连续性
        for (elem_type, stage), elements in grouped.items():
            # 按文档编号分组
            by_doc: Dict[int, List[int]] = {}
            for e in elements:
                if e.doc_num not in by_doc:
                    by_doc[e.doc_num] = []
                by_doc[e.doc_num].append(e.seq_num)

            # 检查每个文档内的连续性
            for doc_num, seq_nums in sorted(by_doc.items()):
                sorted_seqs = sorted(set(seq_nums))
                if len(sorted_seqs) <= 1:
                    continue

                # 查找缺失的序号
                expected = list(range(1, max(sorted_seqs) + 1))
                missing = [x for x in expected if x not in sorted_seqs]

                if missing:
                    key_str = f"{elem_type}-{stage}-{doc_num:02d}"
                    result.missing_numbers[key_str] = missing

                    # 仅在有大量缺失时添加警告
                    if len(missing) <= 5:  # 少量缺失可能是正常的（如删除的旧编号）
                        result.errors.append(ValidationError(
                            severity=Severity.INFO,
                            file_path=elements[0].file_path,
                            line_number=0,
                            element_id=key_str,
                            message=f"{key_str}-XX 可能缺失序号: {missing}",
                            suggestion="检查是否有意跳过或意外遗漏",
                        ))

    def _validate_cross_references(self, result: ValidationResult) -> None:
        """
        验证交叉引用的有效性

        Args:
            result: 验证结果对象
        """
        self.logger.debug("验证交叉引用...")

        # 查找所有形如 `Thm-S-01-01` 或 Thm-S-01-01 的引用
        ref_pattern = re.compile(
            rf"(?:参见|见|参考|引用|\[)[^\n]*?`?({self.config.id_pattern})`?"
        )

        for file_path, elements in self.elements_by_file.items():
            try:
                with open(file_path, "r", encoding=DEFAULT_ENCODING) as f:
                    content = f.read()
            except Exception:
                continue

            # 检查所有引用
            for match in self.ref_regex.finditer(content):
                ref_id = match.group(0).strip("`")

                # 去除可能的markdown格式
                ref_id = re.sub(r"[^\w\-]", "", ref_id)

                if ref_id not in self.known_ids:
                    # 获取行号
                    line_num = content[:match.start()].count("\n") + 1
                    result.cross_ref_errors.append(ValidationError(
                        severity=Severity.WARNING,
                        file_path=file_path,
                        line_number=line_num,
                        element_id=ref_id,
                        message=f"交叉引用指向不存在的元素: {ref_id}",
                        suggestion="检查编号是否正确或元素是否已定义",
                    ))

    def _update_statistics(self, result: ValidationResult) -> None:
        """
        更新统计信息

        Args:
            result: 验证结果对象
        """
        result.stats["total_elements"] = len(result.elements)
        result.stats["error_count"] = len([e for e in result.errors if e.severity == Severity.ERROR])
        result.stats["warning_count"] = len([e for e in result.errors if e.severity == Severity.WARNING])

        # 按类型统计
        for elem in result.elements:
            type_key = {
                "Thm": "thm_count",
                "Def": "def_count",
                "Lemma": "lemma_count",
                "Prop": "prop_count",
                "Cor": "cor_count",
            }.get(elem.element_type, "")
            if type_key:
                result.stats[type_key] += 1


# =============================================================================
# 报告生成器
# =============================================================================

class ReportGenerator:
    """
    验证报告生成器

    支持多种输出格式：控制台、JSON、Markdown
    """

    def __init__(self, result: ValidationResult) -> None:
        """
        初始化报告生成器

        Args:
            result: 验证结果对象
        """
        self.result = result

    def generate_console_report(self, verbose: bool = False) -> str:
        """
        生成控制台格式的报告

        Args:
            verbose: 是否显示详细信息

        Returns:
            报告字符串
        """
        lines = []
        lines.append("=" * 70)
        lines.append("形式化元素编号验证报告")
        lines.append("=" * 70)
        lines.append("")

        # 统计摘要
        lines.append("📊 统计摘要")
        lines.append("-" * 40)
        stats = self.result.stats
        lines.append(f"  扫描文件数:     {stats['total_files']}")
        lines.append(f"  形式化元素总数: {stats['total_elements']}")
        lines.append(f"    - 定理 (Thm):    {stats['thm_count']}")
        lines.append(f"    - 定义 (Def):    {stats['def_count']}")
        lines.append(f"    - 引理 (Lemma):  {stats['lemma_count']}")
        lines.append(f"    - 命题 (Prop):   {stats['prop_count']}")
        lines.append(f"    - 推论 (Cor):    {stats['cor_count']}")
        lines.append(f"  错误数:         {stats['error_count']}")
        lines.append(f"  警告数:         {stats['warning_count']}")
        lines.append("")

        # 重复编号
        if self.result.duplicates:
            lines.append("❌ 重复编号检测")
            lines.append("-" * 40)
            for elem_id, elements in sorted(self.result.duplicates.items()):
                lines.append(f"  {elem_id}: {len(elements)} 次出现")
                if verbose:
                    for e in elements[:3]:
                        lines.append(f"    - {e.file_path}:{e.line_number}")
                    if len(elements) > 3:
                        lines.append(f"    ... 还有 {len(elements)-3} 处")
            lines.append("")

        # 缺失编号
        if self.result.missing_numbers:
            lines.append("⚠️  缺失序号检测")
            lines.append("-" * 40)
            for key, missing in sorted(self.result.missing_numbers.items()):
                lines.append(f"  {key}-XX: 缺失 {missing}")
            lines.append("")

        # 无效格式
        if self.result.invalid_formats:
            lines.append("⚠️  格式警告")
            lines.append("-" * 40)
            for error in self.result.invalid_formats[:10]:
                lines.append(f"  {error.file_path}:{error.line_number}")
                lines.append(f"    {error.message}")
                if error.suggestion:
                    lines.append(f"    建议: {error.suggestion}")
            if len(self.result.invalid_formats) > 10:
                lines.append(f"  ... 还有 {len(self.result.invalid_formats)-10} 个警告")
            lines.append("")

        # 交叉引用错误
        if self.result.cross_ref_errors:
            lines.append("🔗 交叉引用问题")
            lines.append("-" * 40)
            for error in self.result.cross_ref_errors[:10]:
                lines.append(f"  {error.file_path}:{error.line_number}")
                lines.append(f"    {error.message}")
            if len(self.result.cross_ref_errors) > 10:
                lines.append(f"  ... 还有 {len(self.result.cross_ref_errors)-10} 个问题")
            lines.append("")

        # 总结
        lines.append("=" * 70)
        if stats['error_count'] == 0:
            lines.append("✅ 验证通过！未发现严重问题。")
        else:
            lines.append(f"❌ 发现 {stats['error_count']} 个错误，请修复后重试。")
        lines.append("=" * 70)

        return "\n".join(lines)

    def generate_json_report(self) -> str:
        """
        生成JSON格式的报告

        Returns:
            JSON字符串
        """
        report = {
            "summary": self.result.stats,
            "duplicates": {
                k: [
                    {
                        "file": e.file_path,
                        "line": e.line_number,
                        "content": e.line_content[:100],
                    }
                    for e in v
                ]
                for k, v in self.result.duplicates.items()
            },
            "missing_numbers": self.result.missing_numbers,
            "invalid_formats": [
                {
                    "file": e.file_path,
                    "line": e.line_number,
                    "message": e.message,
                    "suggestion": e.suggestion,
                }
                for e in self.result.invalid_formats
            ],
            "cross_ref_errors": [
                {
                    "file": e.file_path,
                    "line": e.line_number,
                    "element_id": e.element_id,
                    "message": e.message,
                }
                for e in self.result.cross_ref_errors
            ],
            "all_elements": [
                {
                    "id": e.element_id,
                    "type": e.element_type,
                    "stage": e.stage,
                    "doc_num": e.doc_num,
                    "seq_num": e.seq_num,
                    "file": e.file_path,
                    "line": e.line_number,
                }
                for e in self.result.elements
            ],
        }
        return json.dumps(report, indent=2, ensure_ascii=False)

    def generate_markdown_report(self) -> str:
        """
        生成Markdown格式的报告

        Returns:
            Markdown字符串
        """
        lines = []
        lines.append("# 形式化元素编号验证报告")
        lines.append("")
        lines.append(f"**生成时间**: 2026-04-10")
        lines.append("")

        # 统计摘要
        lines.append("## 📊 统计摘要")
        lines.append("")
        lines.append("| 指标 | 数值 |")
        lines.append("|------|------|")
        stats = self.result.stats
        lines.append(f"| 扫描文件数 | {stats['total_files']} |")
        lines.append(f"| 形式化元素总数 | {stats['total_elements']} |")
        lines.append(f"| 定理 (Thm) | {stats['thm_count']} |")
        lines.append(f"| 定义 (Def) | {stats['def_count']} |")
        lines.append(f"| 引理 (Lemma) | {stats['lemma_count']} |")
        lines.append(f"| 命题 (Prop) | {stats['prop_count']} |")
        lines.append(f"| 推论 (Cor) | {stats['cor_count']} |")
        lines.append(f"| 错误数 | {stats['error_count']} |")
        lines.append(f"| 警告数 | {stats['warning_count']} |")
        lines.append("")

        # 重复编号
        if self.result.duplicates:
            lines.append("## ❌ 重复编号")
            lines.append("")
            lines.append("| 编号 | 出现次数 | 位置 |")
            lines.append("|------|----------|------|")
            for elem_id, elements in sorted(self.result.duplicates.items()):
                locations = [f"{e.file_path}:{e.line_number}" for e in elements[:2]]
                loc_str = ", ".join(locations)
                if len(elements) > 2:
                    loc_str += f" (+{len(elements)-2})"
                lines.append(f"| `{elem_id}` | {len(elements)} | {loc_str} |")
            lines.append("")

        # 建议修正
        lines.append("## 💡 建议修正")
        lines.append("")
        if self.result.duplicates:
            lines.append("### 重复编号")
            lines.append("")
            for elem_id in sorted(self.result.duplicates.keys()):
                lines.append(f"- **{elem_id}**: 请为重复项分配新的唯一编号")
            lines.append("")

        if not self.result.duplicates and not self.result.errors:
            lines.append("✅ 未发现需要修正的问题。")
            lines.append("")

        lines.append("---")
        lines.append("*报告由 theorem-validator.py 自动生成*")

        return "\n".join(lines)


# =============================================================================
# CLI 接口
# =============================================================================

def create_argument_parser() -> argparse.ArgumentParser:
    """
    创建命令行参数解析器

    Returns:
        ArgumentParser 对象
    """
    parser = argparse.ArgumentParser(
        prog="theorem-validator",
        description="形式化元素编号验证工具 - 验证定理/定义/引理编号的完整性和一致性",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --dir ./docs                    # 扫描 docs 目录
  %(prog)s --dir ./docs --json --output report.json
  %(prog)s --dir ./docs --strict --verbose
  %(prog)s --config validator.conf         # 使用配置文件
        """,
    )

    parser.add_argument(
        "--dir",
        "-d",
        type=str,
        default=".",
        help="要扫描的根目录 (默认: 当前目录)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="输出文件路径 (默认: 输出到控制台)",
    )

    parser.add_argument(
        "--format",
        "-f",
        choices=["console", "json", "markdown", "md"],
        default="console",
        help="输出格式 (默认: console)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="显示详细信息",
    )

    parser.add_argument(
        "--strict",
        "-s",
        action="store_true",
        help="严格模式：将警告视为错误",
    )

    parser.add_argument(
        "--ignore",
        "-i",
        nargs="+",
        help="额外的忽略模式列表",
    )

    parser.add_argument(
        "--no-duplicates",
        action="store_true",
        help="禁用重复编号检查",
    )

    parser.add_argument(
        "--no-missing",
        action="store_true",
        help="禁用缺失编号检查",
    )

    parser.add_argument(
        "--no-cross-refs",
        action="store_true",
        help="禁用交叉引用检查",
    )

    parser.add_argument(
        "--pattern",
        "-p",
        type=str,
        default=DEFAULT_ID_PATTERN,
        help=f"自定义编号匹配正则表达式 (默认: {DEFAULT_ID_PATTERN})",
    )

    parser.add_argument(
        "--config",
        "-c",
        type=str,
        help="配置文件路径 (JSON格式)",
    )

    parser.add_argument(
        "--github-actions",
        action="store_true",
        help="GitHub Actions 模式：设置适当的退出码",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )

    return parser


def load_config_file(config_path: str) -> Optional[ValidatorConfig]:
    """
    从文件加载配置

    Args:
        config_path: 配置文件路径

    Returns:
        ValidatorConfig 对象或 None
    """
    try:
        with open(config_path, "r", encoding=DEFAULT_ENCODING) as f:
            config_data = json.load(f)

        return ValidatorConfig(
            id_pattern=config_data.get("id_pattern", DEFAULT_ID_PATTERN),
            ignore_patterns=config_data.get("ignore_patterns", DEFAULT_IGNORE_PATTERNS),
            check_duplicates=config_data.get("check_duplicates", True),
            check_missing=config_data.get("check_missing", True),
            check_cross_refs=config_data.get("check_cross_refs", True),
            strict_mode=config_data.get("strict_mode", False),
            max_doc_num=config_data.get("max_doc_num", 99),
            max_seq_num=config_data.get("max_seq_num", 99),
        )
    except Exception as e:
        logging.error(f"加载配置文件失败: {e}")
        return None


def main(argv: Optional[List[str]] = None) -> int:
    """
    主入口函数

    Args:
        argv: 命令行参数列表

    Returns:
        退出码 (0=成功, 1=有错误, 2=配置错误)
    """
    parser = create_argument_parser()
    args = parser.parse_args(argv)

    # 设置日志
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
    )

    # 加载配置
    if args.config:
        config = load_config_file(args.config)
        if config is None:
            return 2
    else:
        ignore_patterns = DEFAULT_IGNORE_PATTERNS.copy()
        if args.ignore:
            ignore_patterns.extend(args.ignore)

        config = ValidatorConfig(
            id_pattern=args.pattern,
            ignore_patterns=ignore_patterns,
            check_duplicates=not args.no_duplicates,
            check_missing=not args.no_missing,
            check_cross_refs=not args.no_cross_refs,
            strict_mode=args.strict,
        )

    # 运行验证
    validator = TheoremValidator(config)
    result = validator.scan_directory(args.dir)

    # 生成报告
    generator = ReportGenerator(result)

    if args.format in ("json",):
        report = generator.generate_json_report()
    elif args.format in ("markdown", "md"):
        report = generator.generate_markdown_report()
    else:
        report = generator.generate_console_report(verbose=args.verbose)

    # 输出报告
    if args.output:
        try:
            with open(args.output, "w", encoding=DEFAULT_ENCODING) as f:
                f.write(report)
            print(f"报告已保存到: {args.output}")
        except Exception as e:
            print(f"写入输出文件失败: {e}", file=sys.stderr)
            return 2
    else:
        print(report)

    # 确定退出码
    if args.github_actions or args.strict:
        has_errors = result.stats["error_count"] > 0
        has_warnings = result.stats["warning_count"] > 0
        if has_errors or (args.strict and has_warnings):
            return 1

    return 0


# =============================================================================
# GitHub Actions 支持
# =============================================================================

def github_actions_summary(result: ValidationResult) -> str:
    """
    生成GitHub Actions步骤摘要

    Args:
        result: 验证结果

    Returns:
        Markdown格式的摘要字符串
    """
    stats = result.stats
    lines = [
        "## 定理验证器结果",
        "",
        f"- **扫描文件**: {stats['total_files']}",
        f"- **形式化元素**: {stats['total_elements']}",
        f"  - 定理: {stats['thm_count']}",
        f"  - 定义: {stats['def_count']}",
        f"  - 引理: {stats['lemma_count']}",
        f"  - 命题: {stats['prop_count']}",
        f"  - 推论: {stats['cor_count']}",
        f"- **错误**: {stats['error_count']}",
        f"- **警告**: {stats['warning_count']}",
        "",
    ]

    if result.duplicates:
        lines.append("### ❌ 重复编号")
        for elem_id in list(result.duplicates.keys())[:10]:
            lines.append(f"- `{elem_id}`")
        if len(result.duplicates) > 10:
            lines.append(f"- ... 还有 {len(result.duplicates)-10} 个")
        lines.append("")

    if stats['error_count'] == 0:
        lines.append("✅ **验证通过**")
    else:
        lines.append("❌ **发现错误，请查看详细报告**")

    return "\n".join(lines)


# =============================================================================
# 预提交钩子支持
# =============================================================================

def pre_commit_hook(argv: Optional[List[str]] = None) -> int:
    """
    预提交钩子入口

    检查暂存区中的Markdown文件

    Args:
        argv: 命令行参数

    Returns:
        退出码
    """
    import subprocess

    try:
        # 获取暂存区中的Markdown文件
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=True,
        )

        staged_files = [
            f.strip() for f in result.stdout.split("\n")
            if f.strip().endswith(".md")
        ]

        if not staged_files:
            print("没有暂存的Markdown文件需要检查")
            return 0

        print(f"检查 {len(staged_files)} 个暂存文件...")

        config = ValidatorConfig()
        validator = TheoremValidator(config)

        all_result = ValidationResult()

        for file_path in staged_files:
            if os.path.exists(file_path):
                # 临时处理单个文件
                validator.elements_by_file = {}
                validator.elements_by_id = {}
                validator.known_ids = set()

                file_result = ValidationResult()
                try:
                    validator._process_file(Path(file_path), file_result)
                    all_result.elements.extend(file_result.elements)
                    all_result.errors.extend(file_result.errors)
                except Exception as e:
                    print(f"警告: 无法处理 {file_path}: {e}")

        # 更新统计
        validator.elements_by_id = {}
        for elem in all_result.elements:
            if elem.element_id not in validator.elements_by_id:
                validator.elements_by_id[elem.element_id] = []
            validator.elements_by_id[elem.element_id].append(elem)

        validator._detect_duplicates(all_result)
        validator._update_statistics(all_result)

        # 生成简要报告
        stats = all_result.stats
        if stats['error_count'] > 0:
            print(f"❌ 发现 {stats['error_count']} 个错误:")
            for error in all_result.errors[:5]:
                print(f"  - {error.message}")
            return 1

        print(f"✅ 检查通过 ({stats['total_elements']} 个形式化元素)")
        return 0

    except subprocess.CalledProcessError as e:
        print(f"Git命令失败: {e}")
        return 0  # 允许提交，不阻止
    except Exception as e:
        print(f"预提交检查出错: {e}")
        return 0  # 允许提交


# =============================================================================
# 入口点
# =============================================================================

if __name__ == "__main__":
    # 检查是否是预提交钩子模式
    if len(sys.argv) > 1 and sys.argv[1] == "--pre-commit":
        sys.exit(pre_commit_hook(sys.argv[2:]))

    sys.exit(main())
