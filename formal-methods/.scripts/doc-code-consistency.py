#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Doc-Code Consistency Checker - 文档-代码一致性检查工具

功能:
    - 扫描文档中的形式化引用 (Def-*, Thm-*, Lemma-*, Prop-*, Cor-*)
    - 扫描 Lean 4 代码中的 theorem/def/lemma 实现
    - 检查文档与代码之间的一致性
    - 生成不一致报告 (JSON + Markdown)

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
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Pattern, Set, Tuple, NamedTuple
from datetime import datetime


# =============================================================================
# 配置常量
# =============================================================================

DEFAULT_ENCODING = "utf-8"
DEFAULT_LOG_LEVEL = logging.INFO

# 形式化编号模式: Thm-S-01-01, Def-K-02-03, etc.
FORMAL_ID_PATTERN = r"(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2})"

# Lean 代码中的定义模式
LEAN_THEOREM_PATTERN = r"\b(theorem|lemma|def|inductive|structure|class)\s+(\w+)"
LEAN_DOCSTRING_PATTERN = r"/-\s*\n?(.*?)\n?-/"
LEAN_LINE_COMMENT_PATTERN = r"--\s*(.*)"

# 默认路径配置
DEFAULT_DOC_DIRS = ["formal-methods"]
DEFAULT_LEAN_DIR = "formal-methods/formal-code/lean4"

# 忽略模式
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
    ".lake",
    "build",
]

# 形式化元素类型映射
FORMAL_ELEMENT_TYPES = {
    "Thm": "定理 (Theorem)",
    "Def": "定义 (Definition)",
    "Lemma": "引理 (Lemma)",
    "Prop": "命题 (Proposition)",
    "Cor": "推论 (Corollary)",
}


# =============================================================================
# 数据类定义
# =============================================================================

class Severity(Enum):
    """问题严重程度枚举"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class DocReference:
    """文档中的形式化引用"""
    element_id: str          # 如: Thm-S-02-01
    element_type: str        # Thm, Def, Lemma, Prop, Cor
    stage: str               # S, K, F
    doc_num: int
    seq_num: int
    file_path: str
    line_number: int
    line_content: str
    context: str = ""        # 上下文（前后几行）


@dataclass
class LeanImplementation:
    """Lean 代码中的实现"""
    name: str                # 定义名称（如: progress, StrongBisimulation）
    kind: str                # theorem, lemma, def, inductive, structure, class
    file_path: str
    line_number: int
    line_content: str
    docstring: str = ""      # 文档字符串
    formal_refs: List[str] = field(default_factory=list)  # 引用的形式化编号


@dataclass
class ConsistencyMapping:
    """文档与代码的对应关系"""
    formal_id: str           # 形式化编号
    doc_refs: List[DocReference] = field(default_factory=list)
    lean_impls: List[LeanImplementation] = field(default_factory=list)
    status: str = ""         # matched, doc_only, code_only


@dataclass
class ConsistencyResult:
    """一致性检查结果"""
    # 扫描统计
    doc_files_scanned: int = 0
    lean_files_scanned: int = 0
    total_doc_refs: int = 0
    total_lean_defs: int = 0
    
    # 对应关系
    matched: List[ConsistencyMapping] = field(default_factory=list)
    doc_only: List[ConsistencyMapping] = field(default_factory=list)  # 文档有但代码无
    code_only: List[LeanImplementation] = field(default_factory=list)  # 代码有但文档未引用
    
    # 按类型统计
    stats: Dict[str, int] = field(default_factory=lambda: {
        "matched_count": 0,
        "doc_only_count": 0,
        "code_only_count": 0,
        "thm_matched": 0,
        "def_matched": 0,
        "lemma_matched": 0,
        "prop_matched": 0,
        "cor_matched": 0,
    })


@dataclass
class CheckerConfig:
    """检查器配置"""
    doc_dirs: List[str] = field(default_factory=lambda: DEFAULT_DOC_DIRS.copy())
    lean_dir: str = DEFAULT_LEAN_DIR
    ignore_patterns: List[str] = field(default_factory=lambda: DEFAULT_IGNORE_PATTERNS.copy())
    formal_id_pattern: str = FORMAL_ID_PATTERN
    lean_pattern: str = LEAN_THEOREM_PATTERN
    verbose: bool = False


# =============================================================================
# 核心检查器类
# =============================================================================

class DocCodeConsistencyChecker:
    """
    文档-代码一致性检查器
    
    负责扫描文档中的形式化引用和 Lean 代码中的实现，
    并检查两者之间的一致性。
    """
    
    def __init__(self, config: Optional[CheckerConfig] = None) -> None:
        """
        初始化检查器
        
        Args:
            config: 检查器配置
        """
        self.config = config or CheckerConfig()
        self.formal_id_regex: Pattern[str] = re.compile(self.config.formal_id_pattern)
        self.lean_def_regex: Pattern[str] = re.compile(self.config.lean_pattern)
        self.logger = logging.getLogger(__name__)
        
        # 存储扫描结果
        self.doc_refs: List[DocReference] = []
        self.lean_impls: List[LeanImplementation] = []
        
    def run_check(self) -> ConsistencyResult:
        """
        运行完整的一致性检查
        
        Returns:
            ConsistencyResult 包含所有检查结果
        """
        result = ConsistencyResult()
        
        # 1. 扫描文档
        self.logger.info("开始扫描文档...")
        self._scan_documents()
        result.doc_files_scanned = len(set(r.file_path for r in self.doc_refs))
        result.total_doc_refs = len(self.doc_refs)
        
        # 2. 扫描 Lean 代码
        self.logger.info("开始扫描 Lean 代码...")
        self._scan_lean_code()
        result.lean_files_scanned = len(set(i.file_path for i in self.lean_impls))
        result.total_lean_defs = len(self.lean_impls)
        
        # 3. 执行一致性检查
        self.logger.info("执行一致性检查...")
        self._check_consistency(result)
        
        # 4. 更新统计
        self._update_statistics(result)
        
        self.logger.info(
            f"检查完成: {result.doc_files_scanned} 文档文件, "
            f"{result.lean_files_scanned} Lean文件, "
            f"{result.stats['matched_count']} 已对应"
        )
        
        return result
    
    def _scan_documents(self) -> None:
        """扫描所有文档文件中的形式化引用"""
        for doc_dir in self.config.doc_dirs:
            root_path = Path(doc_dir).resolve()
            if not root_path.exists():
                self.logger.warning(f"文档目录不存在: {root_path}")
                continue
            
            for file_path in root_path.rglob("*.md"):
                if self._should_ignore(file_path):
                    continue
                self._process_doc_file(file_path)
    
    def _process_doc_file(self, file_path: Path) -> None:
        """
        处理单个文档文件
        
        Args:
            file_path: 文档文件路径
        """
        try:
            with open(file_path, "r", encoding=DEFAULT_ENCODING) as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="gbk", errors="ignore") as f:
                lines = f.readlines()
        except Exception as e:
            self.logger.error(f"无法读取文件 {file_path}: {e}")
            return
        
        rel_path = str(file_path.relative_to(Path.cwd()))
        
        for line_num, line in enumerate(lines, 1):
            for match in self.formal_id_regex.finditer(line):
                ref = self._parse_doc_reference(match, rel_path, line_num, line.strip())
                if ref:
                    # 添加上下文
                    context_start = max(0, line_num - 2)
                    context_end = min(len(lines), line_num + 2)
                    ref.context = "".join(lines[context_start:context_end])
                    self.doc_refs.append(ref)
    
    def _parse_doc_reference(
        self,
        match: re.Match[str],
        file_path: str,
        line_number: int,
        line_content: str
    ) -> Optional[DocReference]:
        """
        解析文档中的形式化引用
        
        Args:
            match: 正则匹配对象
            file_path: 文件路径
            line_number: 行号
            line_content: 行内容
            
        Returns:
            DocReference 对象或 None
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
        
        return DocReference(
            element_id=element_id,
            element_type=element_type,
            stage=stage,
            doc_num=doc_num,
            seq_num=seq_num,
            file_path=file_path,
            line_number=line_number,
            line_content=line_content[:200],  # 限制长度
        )
    
    def _scan_lean_code(self) -> None:
        """扫描所有 Lean 代码文件"""
        lean_path = Path(self.config.lean_dir).resolve()
        if not lean_path.exists():
            self.logger.warning(f"Lean 目录不存在: {lean_path}")
            return
        
        for file_path in lean_path.rglob("*.lean"):
            if self._should_ignore(file_path):
                continue
            self._process_lean_file(file_path)
    
    def _process_lean_file(self, file_path: Path) -> None:
        """
        处理单个 Lean 文件
        
        Args:
            file_path: Lean 文件路径
        """
        try:
            with open(file_path, "r", encoding=DEFAULT_ENCODING) as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            self.logger.error(f"无法读取文件 {file_path}: {e}")
            return
        
        rel_path = str(file_path.relative_to(Path.cwd()))
        
        # 提取文档字符串
        docstrings = self._extract_lean_docstrings(content)
        
        for line_num, line in enumerate(lines, 1):
            for match in self.lean_def_regex.finditer(line):
                kind, name = match.groups()
                
                # 查找附近的文档字符串
                docstring = self._find_nearby_docstring(docstrings, line_num)
                
                # 提取该行中的形式化引用
                formal_refs = self.formal_id_regex.findall(line)
                formal_ref_ids = [f"{g[0]}-{g[1]}-{g[2]}-{g[3]}" for g in formal_refs]
                
                impl = LeanImplementation(
                    name=name,
                    kind=kind,
                    file_path=rel_path,
                    line_number=line_num,
                    line_content=line.strip()[:200],
                    docstring=docstring[:500] if docstring else "",
                    formal_refs=formal_ref_ids,
                )
                self.lean_impls.append(impl)
    
    def _extract_lean_docstrings(self, content: str) -> List[Tuple[int, str]]:
        """
        提取 Lean 文件中的所有文档字符串及其位置
        
        Args:
            content: 文件内容
            
        Returns:
            列表，每个元素是 (行号, 文档字符串内容)
        """
        docstrings = []
        
        # 匹配 /- ... -/ 块注释
        for match in re.finditer(r'/-\s*\n?(.*?)-/', content, re.DOTALL):
            # 计算行号
            line_num = content[:match.start()].count('\n') + 1
            docstrings.append((line_num, match.group(1).strip()))
        
        # 匹配 /-- ... -/ 文档注释
        for match in re.finditer(r'/--\s*\n?(.*?)-/', content, re.DOTALL):
            line_num = content[:match.start()].count('\n') + 1
            docstrings.append((line_num, match.group(1).strip()))
        
        return docstrings
    
    def _find_nearby_docstring(self, docstrings: List[Tuple[int, str]], line_num: int) -> str:
        """
        查找距离指定行最近的文档字符串
        
        Args:
            docstrings: 文档字符串列表
            line_num: 目标行号
            
        Returns:
            最近的文档字符串或空字符串
        """
        best_match = ""
        best_distance = float('inf')
        
        for doc_line, doc_content in docstrings:
            distance = abs(doc_line - line_num)
            if distance < best_distance and distance <= 10:  # 最多10行距离
                best_distance = distance
                best_match = doc_content
        
        return best_match
    
    def _check_consistency(self, result: ConsistencyResult) -> None:
        """
        执行一致性检查
        
        Args:
            result: 结果对象
        """
        # 构建查找表
        doc_refs_by_id: Dict[str, List[DocReference]] = {}
        for ref in self.doc_refs:
            if ref.element_id not in doc_refs_by_id:
                doc_refs_by_id[ref.element_id] = []
            doc_refs_by_id[ref.element_id].append(ref)
        
        # 1. 检查文档中引用的形式化元素是否在代码中有对应
        for formal_id, refs in doc_refs_by_id.items():
            mapping = ConsistencyMapping(
                formal_id=formal_id,
                doc_refs=refs,
                status="doc_only"
            )
            
            # 查找代码中是否有实现（通过名称匹配或引用匹配）
            matching_impls = self._find_matching_implementations(formal_id, refs)
            
            if matching_impls:
                mapping.lean_impls = matching_impls
                mapping.status = "matched"
                result.matched.append(mapping)
            else:
                result.doc_only.append(mapping)
        
        # 2. 检查代码中是否有文档未引用的实现
        referenced_ids = set(doc_refs_by_id.keys())
        for impl in self.lean_impls:
            # 如果实现引用了形式化编号，则认为已匹配
            if impl.formal_refs:
                continue
            
            # 检查是否是重要的定理/定义（简单启发式：包含 theorem/lemma/def）
            if impl.kind in ('theorem', 'lemma', 'def'):
                # 检查是否已作为某个匹配的代码部分
                is_matched = any(
                    impl.name in [i.name for i in m.lean_impls]
                    for m in result.matched
                )
                if not is_matched:
                    result.code_only.append(impl)
    
    def _find_matching_implementations(
        self,
        formal_id: str,
        doc_refs: List[DocReference]
    ) -> List[LeanImplementation]:
        """
        查找与形式化编号匹配的 Lean 实现
        
        匹配策略：
        1. 代码中直接引用了该形式化编号
        2. 名称匹配（从文档上下文中提取可能的名称）
        
        Args:
            formal_id: 形式化编号
            doc_refs: 文档引用列表
            
        Returns:
            匹配的 Lean 实现列表
        """
        matches = []
        
        # 策略1: 代码直接引用了形式化编号
        for impl in self.lean_impls:
            if formal_id in impl.formal_refs:
                matches.append(impl)
        
        # 策略2: 从文档上下文中提取可能的名称进行匹配
        if not matches:
            # 从形式化编号提取元素类型和序号
            match = self.formal_id_regex.match(formal_id)
            if match:
                element_type = match.group(1)
                # 尝试匹配常见的命名模式
                for impl in self.lean_impls:
                    # 简单启发式：检查实现类型是否匹配
                    if element_type == "Thm" and impl.kind == "theorem":
                        # 可以添加更复杂的匹配逻辑
                        pass
                    elif element_type == "Lemma" and impl.kind == "lemma":
                        pass
                    elif element_type == "Def" and impl.kind in ("def", "inductive", "structure"):
                        pass
        
        return matches
    
    def _update_statistics(self, result: ConsistencyResult) -> None:
        """更新统计信息"""
        result.stats["matched_count"] = len(result.matched)
        result.stats["doc_only_count"] = len(result.doc_only)
        result.stats["code_only_count"] = len(result.code_only)
        
        # 按类型统计已匹配
        for mapping in result.matched:
            element_type = mapping.formal_id.split('-')[0]
            type_key = {
                "Thm": "thm_matched",
                "Def": "def_matched",
                "Lemma": "lemma_matched",
                "Prop": "prop_matched",
                "Cor": "cor_matched",
            }.get(element_type, "")
            if type_key:
                result.stats[type_key] += 1
    
    def _should_ignore(self, file_path: Path) -> bool:
        """
        检查文件是否应该被忽略
        
        Args:
            file_path: 文件路径
            
        Returns:
            如果应该忽略返回 True
        """
        path_str = str(file_path)
        
        for pattern in self.config.ignore_patterns:
            if "*" in pattern:
                import fnmatch
                if fnmatch.fnmatch(path_str, pattern) or \
                   fnmatch.fnmatch(file_path.name, pattern):
                    return True
            elif pattern in path_str:
                return True
        
        return False


# =============================================================================
# 报告生成器
# =============================================================================

class ReportGenerator:
    """
    一致性检查报告生成器
    
    支持 JSON 和 Markdown 格式输出。
    """
    
    def __init__(self, result: ConsistencyResult) -> None:
        """
        初始化报告生成器
        
        Args:
            result: 检查结果
        """
        self.result = result
        self.timestamp = datetime.now().isoformat()
    
    def generate_json_report(self) -> str:
        """
        生成 JSON 格式报告
        
        Returns:
            JSON 字符串
        """
        def serialize_mapping(m: ConsistencyMapping) -> dict:
            return {
                "formal_id": m.formal_id,
                "status": m.status,
                "doc_refs": [
                    {
                        "file": r.file_path,
                        "line": r.line_number,
                        "content": r.line_content,
                    }
                    for r in m.doc_refs
                ],
                "lean_impls": [
                    {
                        "name": i.name,
                        "kind": i.kind,
                        "file": i.file_path,
                        "line": i.line_number,
                    }
                    for i in m.lean_impls
                ],
            }
        
        def serialize_impl(i: LeanImplementation) -> dict:
            return {
                "name": i.name,
                "kind": i.kind,
                "file": i.file_path,
                "line": i.line_number,
                "line_content": i.line_content,
                "formal_refs": i.formal_refs,
            }
        
        report = {
            "metadata": {
                "generated_at": self.timestamp,
                "tool_version": "1.0.0",
            },
            "summary": {
                "doc_files_scanned": self.result.doc_files_scanned,
                "lean_files_scanned": self.result.lean_files_scanned,
                "total_doc_refs": self.result.total_doc_refs,
                "total_lean_defs": self.result.total_lean_defs,
            },
            "statistics": self.result.stats,
            "matched": [serialize_mapping(m) for m in self.result.matched],
            "doc_only": [serialize_mapping(m) for m in self.result.doc_only],
            "code_only": [serialize_impl(i) for i in self.result.code_only],
        }
        
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    def generate_markdown_report(self) -> str:
        """
        生成 Markdown 格式报告
        
        Returns:
            Markdown 字符串
        """
        lines = []
        lines.append("# 文档-代码一致性检查报告")
        lines.append("")
        lines.append(f"**生成时间**: {self.timestamp}")
        lines.append("")
        
        # 摘要
        lines.append("## 📊 检查摘要")
        lines.append("")
        lines.append("| 指标 | 数值 |")
        lines.append("|------|------|")
        lines.append(f"| 扫描文档文件数 | {self.result.doc_files_scanned} |")
        lines.append(f"| 扫描 Lean 文件数 | {self.result.lean_files_scanned} |")
        lines.append(f"| 文档形式化引用数 | {self.result.total_doc_refs} |")
        lines.append(f"| Lean 定义/定理数 | {self.result.total_lean_defs} |")
        lines.append("")
        
        # 一致性统计
        lines.append("## ✅ 一致性统计")
        lines.append("")
        lines.append("| 类别 | 数量 | 占比 |")
        lines.append("|------|------|------|")
        total = self.result.total_doc_refs or 1
        matched = self.result.stats["matched_count"]
        doc_only = self.result.stats["doc_only_count"]
        code_only = self.result.stats["code_only_count"]
        lines.append(f"| 已对应 (文档↔代码) | {matched} | {matched/total*100:.1f}% |")
        lines.append(f"| 仅文档引用 | {doc_only} | {doc_only/total*100:.1f}% |")
        lines.append(f"| 仅代码实现 | {code_only} | - |")
        lines.append("")
        
        # 按类型统计
        lines.append("### 按类型统计")
        lines.append("")
        lines.append("| 类型 | 已对应数量 |")
        lines.append("|------|------------|")
        lines.append(f"| 定理 (Thm) | {self.result.stats['thm_matched']} |")
        lines.append(f"| 定义 (Def) | {self.result.stats['def_matched']} |")
        lines.append(f"| 引理 (Lemma) | {self.result.stats['lemma_matched']} |")
        lines.append(f"| 命题 (Prop) | {self.result.stats['prop_matched']} |")
        lines.append(f"| 推论 (Cor) | {self.result.stats['cor_matched']} |")
        lines.append("")
        
        # 已对应列表
        if self.result.matched:
            lines.append("## 🟢 已对应列表 (文档↔代码)")
            lines.append("")
            lines.append("| 形式化编号 | 文档位置 | 代码位置 |")
            lines.append("|------------|----------|----------|")
            for mapping in sorted(self.result.matched, key=lambda x: x.formal_id):
                doc_locs = [f"{r.file_path}:{r.line_number}" for r in mapping.doc_refs[:1]]
                code_locs = [f"{i.file_path}:{i.line_number}" for i in mapping.lean_impls[:1]]
                lines.append(f"| `{mapping.formal_id}` | {', '.join(doc_locs)} | {', '.join(code_locs)} |")
            lines.append("")
        
        # 文档缺失代码列表
        if self.result.doc_only:
            lines.append("## 🟡 文档有引用但代码缺失")
            lines.append("")
            lines.append("以下形式化元素在文档中有引用，但在 Lean 代码中未找到对应实现：")
            lines.append("")
            lines.append("| 形式化编号 | 文档位置 | 上下文 |")
            lines.append("|------------|----------|--------|")
            for mapping in sorted(self.result.doc_only, key=lambda x: x.formal_id)[:50]:  # 限制显示数量
                doc_locs = [f"{r.file_path}:{r.line_number}" for r in mapping.doc_refs[:1]]
                context = mapping.doc_refs[0].line_content[:60] if mapping.doc_refs else ""
                lines.append(f"| `{mapping.formal_id}` | {', '.join(doc_locs)} | {context}... |")
            if len(self.result.doc_only) > 50:
                lines.append(f"| ... | ... | 还有 {len(self.result.doc_only) - 50} 项 |")
            lines.append("")
        
        # 代码缺失文档列表
        if self.result.code_only:
            lines.append("## 🔵 代码有实现但文档未引用")
            lines.append("")
            lines.append("以下 Lean 实现在代码中存在，但文档中未引用对应的形式化编号：")
            lines.append("")
            lines.append("| 名称 | 类型 | 文件位置 |")
            lines.append("|------|------|----------|")
            # 按文件分组
            by_file: Dict[str, List[LeanImplementation]] = {}
            for impl in self.result.code_only:
                if impl.file_path not in by_file:
                    by_file[impl.file_path] = []
                by_file[impl.file_path].append(impl)
            
            for file_path in sorted(by_file.keys()):
                impls = by_file[file_path][:5]  # 每文件最多显示5个
                for impl in impls:
                    lines.append(f"| `{impl.name}` | {impl.kind} | {impl.file_path}:{impl.line_number} |")
                if len(by_file[file_path]) > 5:
                    lines.append(f"| ... | ... | 还有 {len(by_file[file_path]) - 5} 项 |")
            lines.append("")
        
        # 建议
        lines.append("## 💡 改进建议")
        lines.append("")
        if self.result.doc_only:
            lines.append(f"1. **补充代码实现**: 为 {len(self.result.doc_only)} 个文档引用的形式化元素创建 Lean 实现")
            lines.append("")
        if self.result.code_only:
            lines.append(f"2. **补充文档引用**: 为 {len(self.result.code_only)} 个代码实现添加文档中的形式化编号引用")
            lines.append("")
        if not self.result.doc_only and not self.result.code_only:
            lines.append("✅ 文档与代码完全一致！")
            lines.append("")
        
        lines.append("---")
        lines.append("*报告由 doc-code-consistency.py 自动生成*")
        
        return "\n".join(lines)
    
    def generate_console_report(self) -> str:
        """
        生成控制台格式报告
        
        Returns:
            控制台格式字符串
        """
        lines = []
        lines.append("=" * 70)
        lines.append("文档-代码一致性检查报告")
        lines.append("=" * 70)
        lines.append("")
        
        # 摘要
        lines.append("📊 检查摘要")
        lines.append("-" * 40)
        lines.append(f"  扫描文档文件数: {self.result.doc_files_scanned}")
        lines.append(f"  扫描 Lean 文件数: {self.result.lean_files_scanned}")
        lines.append(f"  文档形式化引用数: {self.result.total_doc_refs}")
        lines.append(f"  Lean 定义/定理数: {self.result.total_lean_defs}")
        lines.append("")
        
        # 一致性统计
        lines.append("✅ 一致性统计")
        lines.append("-" * 40)
        stats = self.result.stats
        lines.append(f"  已对应: {stats['matched_count']}")
        lines.append(f"  仅文档: {stats['doc_only_count']}")
        lines.append(f"  仅代码: {stats['code_only_count']}")
        lines.append("")
        
        # 类型统计
        lines.append("📋 按类型统计 (已对应)")
        lines.append("-" * 40)
        lines.append(f"  定理 (Thm):   {stats['thm_matched']}")
        lines.append(f"  定义 (Def):   {stats['def_matched']}")
        lines.append(f"  引理 (Lemma): {stats['lemma_matched']}")
        lines.append(f"  命题 (Prop):  {stats['prop_matched']}")
        lines.append(f"  推论 (Cor):   {stats['cor_matched']}")
        lines.append("")
        
        # 样本展示
        if self.result.matched:
            lines.append("🟢 已对应样本 (前5项)")
            lines.append("-" * 40)
            for mapping in sorted(self.result.matched, key=lambda x: x.formal_id)[:5]:
                lines.append(f"  {mapping.formal_id}")
            lines.append("")
        
        if self.result.doc_only:
            lines.append(f"🟡 文档有但代码缺失 (前5项, 共{len(self.result.doc_only)}项)")
            lines.append("-" * 40)
            for mapping in sorted(self.result.doc_only, key=lambda x: x.formal_id)[:5]:
                lines.append(f"  {mapping.formal_id}")
            lines.append("")
        
        if self.result.code_only:
            lines.append(f"🔵 代码有但文档未引用 (前5项, 共{len(self.result.code_only)}项)")
            lines.append("-" * 40)
            for impl in self.result.code_only[:5]:
                lines.append(f"  {impl.name} ({impl.kind}) in {impl.file_path}:{impl.line_number}")
            lines.append("")
        
        # 总结
        lines.append("=" * 70)
        coverage = 0
        if self.result.total_doc_refs > 0:
            coverage = stats['matched_count'] / self.result.total_doc_refs * 100
        if coverage >= 90:
            lines.append(f"✅ 一致性良好: {coverage:.1f}% 的形式化元素已对应")
        elif coverage >= 50:
            lines.append(f"⚠️  一致性中等: {coverage:.1f}% 的形式化元素已对应")
        else:
            lines.append(f"❌ 一致性较差: {coverage:.1f}% 的形式化元素已对应")
        lines.append("=" * 70)
        
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
        prog="doc-code-consistency",
        description="文档-代码一致性检查工具 - 检查 Markdown 文档中的形式化引用与 Lean 4 代码实现的一致性",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                                  # 使用默认配置运行
  %(prog)s --doc-dir ./docs --lean-dir ./lean  # 指定目录
  %(prog)s --json --output report.json      # 输出 JSON 报告
  %(prog)s --md --output report.md          # 输出 Markdown 报告
  %(prog)s --verbose                        # 显示详细信息
        """,
    )
    
    parser.add_argument(
        "--doc-dir",
        "-d",
        action="append",
        help="要扫描的文档目录 (可多次指定，默认: formal-methods)",
    )
    
    parser.add_argument(
        "--lean-dir",
        "-l",
        type=str,
        default=DEFAULT_LEAN_DIR,
        help=f"Lean 代码目录 (默认: {DEFAULT_LEAN_DIR})",
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
        "--ignore",
        "-i",
        nargs="+",
        help="额外的忽略模式列表",
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )
    
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """
    主入口函数
    
    Args:
        argv: 命令行参数列表
        
    Returns:
        退出码 (0=成功)
    """
    parser = create_argument_parser()
    args = parser.parse_args(argv)
    
    # 设置日志
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
    )
    
    # 构建配置
    doc_dirs = args.doc_dir if args.doc_dir else DEFAULT_DOC_DIRS
    
    ignore_patterns = DEFAULT_IGNORE_PATTERNS.copy()
    if args.ignore:
        ignore_patterns.extend(args.ignore)
    
    config = CheckerConfig(
        doc_dirs=doc_dirs,
        lean_dir=args.lean_dir,
        ignore_patterns=ignore_patterns,
        verbose=args.verbose,
    )
    
    # 运行检查
    checker = DocCodeConsistencyChecker(config)
    result = checker.run_check()
    
    # 生成报告
    generator = ReportGenerator(result)
    
    if args.format in ("json",):
        report = generator.generate_json_report()
    elif args.format in ("markdown", "md"):
        report = generator.generate_markdown_report()
    else:
        report = generator.generate_console_report()
    
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
    
    return 0


# =============================================================================
# 入口点
# =============================================================================

if __name__ == "__main__":
    sys.exit(main())
