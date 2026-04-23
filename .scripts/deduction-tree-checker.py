#!/usr/bin/env python3
"""
推理树覆盖率自动检测器
功能：
- 递归扫描核心目录 Markdown 文件
- 检测推理树（graph BT / flowchart BT）存在性与质量
- 检测其他思维表征（mindmap / quadrantChart / stateDiagram-v2）
- 分级评估 A/B/C/D
- 输出文本报告 + JSON 报告
- 支持 --fix-suggestions 自动生成建议

作者: AnalysisDataFlow Toolchain Team
版本: 1.0.0
日期: 2026-04-24
"""

import re
import os
import sys
import json
import glob
import argparse
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple
from collections import defaultdict


@dataclass
class DeductionTreeInfo:
    """单文档推理树检测信息"""
    file_path: str
    has_bt: bool = False
    bt_has_formal: bool = False
    has_mindmap: bool = False
    has_quadrant: bool = False
    has_state_diag: bool = False
    grade: str = "D"
    formal_elements_in_doc: List[str] = field(default_factory=list)
    bt_content: Optional[str] = None


@dataclass
class ReportSummary:
    """报告汇总"""
    total_files: int = 0
    files_with_bt: int = 0
    files_with_mindmap: int = 0
    files_with_quadrant: int = 0
    files_with_state_diag: int = 0
    grade_a: int = 0
    grade_b: int = 0
    grade_c: int = 0
    grade_d: int = 0
    coverage_rate: float = 0.0


class DeductionTreeChecker:
    """推理树覆盖率检查器"""

    # 核心扫描目录
    SCAN_PATTERNS = [
        "Struct/**/*.md",
        "Knowledge/**/*.md",
        "Flink/**/*.md",
    ]

    # 排除模式（路径中包含这些字符串的文件跳过）
    SKIP_PATTERNS = [
        'en/', 'archive/', '.scripts/', '.github/', '.vscode/',
        'i18n/', 'docs/', 'COMMUNITY/', 'CONFIG-TEMPLATES/',
        'LEARNING-PATHS/', 'TECH-RADAR/', 'examples/',
        'formal-methods/', 'formal-proofs/', 'benchmark-data/',
        'benchmark-results/', 'case-studies/', 'docker/',
        'advisory-board/', '00-meta/', '98-exercises/',
        '_in-progress', 'deprecated',
    ]

    # 形式化元素编号模式（在推理树中查找）
    FORMAL_IN_BT_PATTERNS = [
        re.compile(r'Def-[SKF]-\d{2,}-\d{2,}'),
        re.compile(r'Lemma-[SKF]-\d{2,}-\d{2,}'),
        re.compile(r'Thm-[SKF]-\d{2,}-\d{2,}'),
        re.compile(r'Prop-[SKF]-\d{2,}-\d{2,}'),
        re.compile(r'Cor-[SKF]-\d{2,}-\d{2,}'),
    ]

    # 在文档中查找形式化元素（用于生成建议）
    FORMAL_IN_DOC_PATTERNS = [
        re.compile(r'(Def-[SKF]-\d{2,}-\d{2,})'),
        re.compile(r'(Lemma-[SKF]-\d{2,}-\d{2,})'),
        re.compile(r'(Thm-[SKF]-\d{2,}-\d{2,})'),
        re.compile(r'(Prop-[SKF]-\d{2,}-\d{2,})'),
        re.compile(r'(Cor-[SKF]-\d{2,}-\d{2,})'),
    ]

    # Mermaid 块开始/结束标记
    MERMAID_START_RE = re.compile(r'^\s*```\s*mermaid\s*$', re.IGNORECASE)
    MERMAID_END_RE = re.compile(r'^\s*```\s*$')

    # 推理树类型检测
    BT_START_RE = re.compile(r'^\s*(graph|flowchart)\s+BT\b', re.IGNORECASE)

    # 其他思维表征检测
    MINDMAP_START_RE = re.compile(r'^\s*mindmap\b', re.IGNORECASE)
    QUADRANT_START_RE = re.compile(r'^\s*quadrantChart\b', re.IGNORECASE)
    STATE_DIAG_START_RE = re.compile(r'^\s*stateDiagram-v2\b', re.IGNORECASE)

    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        self.results: List[DeductionTreeInfo] = []
        self.summary = ReportSummary()
        self.fix_suggestions: Dict[str, str] = {}

    def scan_files(self) -> List[Path]:
        """扫描目标 Markdown 文件"""
        md_files = []
        for pattern in self.SCAN_PATTERNS:
            files = glob.glob(str(self.base_path / pattern), recursive=True)
            for f in files:
                path = Path(f).resolve()
                path_str = str(path).replace('\\', '/')
                # 应用排除规则
                if any(skip in path_str for skip in self.SKIP_PATTERNS):
                    continue
                md_files.append(path)
        # 去重并排序
        unique = list(set(md_files))
        unique.sort(key=lambda p: str(p))
        return unique

    def extract_mermaid_blocks(self, content: str) -> List[Tuple[int, int, str]]:
        """提取所有 Mermaid 代码块，返回 (start_line, end_line, block_content)"""
        blocks = []
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            if self.MERMAID_START_RE.match(lines[i]):
                start_line = i
                block_lines = []
                i += 1
                while i < len(lines) and not self.MERMAID_END_RE.match(lines[i]):
                    block_lines.append(lines[i])
                    i += 1
                end_line = i
                block_content = '\n'.join(block_lines)
                blocks.append((start_line, end_line, block_content))
            i += 1
        return blocks

    def analyze_file(self, file_path: Path, content: str) -> DeductionTreeInfo:
        """分析单个文件的推理树情况"""
        rel_path = str(file_path.relative_to(self.base_path)).replace('\\', '/')
        info = DeductionTreeInfo(file_path=rel_path)

        # 提取所有 Mermaid 块
        mermaid_blocks = self.extract_mermaid_blocks(content)

        for start, end, block in mermaid_blocks:
            first_line = block.strip().split('\n')[0].strip() if block.strip() else ''

            # 检测推理树 (graph BT / flowchart BT)
            if self.BT_START_RE.match(first_line):
                info.has_bt = True
                info.bt_content = block
                # 检查是否包含形式化编号
                for pat in self.FORMAL_IN_BT_PATTERNS:
                    if pat.search(block):
                        info.bt_has_formal = True
                        break
                continue

            # 检测其他思维表征
            if self.MINDMAP_START_RE.match(first_line):
                info.has_mindmap = True
                continue
            if self.QUADRANT_START_RE.match(first_line):
                info.has_quadrant = True
                continue
            if self.STATE_DIAG_START_RE.match(first_line):
                info.has_state_diag = True
                continue

        # 在文档中搜索形式化元素（用于 --fix-suggestions）
        formal_set = set()
        for pat in self.FORMAL_IN_DOC_PATTERNS:
            for m in pat.finditer(content):
                formal_set.add(m.group(1))
        info.formal_elements_in_doc = sorted(formal_set)

        # 分级评估
        if info.has_bt:
            if info.bt_has_formal:
                if info.has_mindmap or info.has_quadrant or info.has_state_diag:
                    info.grade = "A"
                else:
                    info.grade = "B"
            else:
                info.grade = "C"
        else:
            info.grade = "D"

        return info

    def generate_fix_suggestion(self, info: DeductionTreeInfo) -> str:
        """为 D 级文档生成推理树建议"""
        elements = info.formal_elements_in_doc
        rel_path = info.file_path

        lines = []
        lines.append(f"# 建议：为 {rel_path} 添加推理树")
        lines.append("")
        lines.append("```mermaid")
        lines.append("flowchart BT")
        lines.append("    direction BT")
        lines.append("")

        if not elements:
            lines.append("    %% 本文档未检测到形式化编号")
            lines.append("    %% 建议先补充 Def-/Lemma-/Thm-/Prop- 编号")
            lines.append("    DOC[\"本文档\"] --> GOAL[\"推理目标\"]")
        else:
            # 按类型分组
            defs = [e for e in elements if e.startswith('Def-')]
            lemmas = [e for e in elements if e.startswith('Lemma-')]
            props = [e for e in elements if e.startswith('Prop-')]
            thms = [e for e in elements if e.startswith('Thm-')]
            cors = [e for e in elements if e.startswith('Cor-')]

            node_map = {}
            node_id = 0

            def add_nodes(items, prefix):
                nonlocal node_id
                result = []
                for item in items:
                    nid = f"{prefix}{node_id}"
                    node_id += 1
                    node_map[item] = nid
                    label = item.replace('-', '_')
                    result.append((nid, label, item))
                return result

            def_nodes = add_nodes(defs, "D")
            lemma_nodes = add_nodes(lemmas, "L")
            prop_nodes = add_nodes(props, "P")
            thm_nodes = add_nodes(thms, "T")
            cor_nodes = add_nodes(cors, "C")

            # 输出节点定义
            for nid, label, full in def_nodes:
                lines.append(f'    {nid}["{full}"]')
            for nid, label, full in lemma_nodes:
                lines.append(f'    {nid}["{full}"]')
            for nid, label, full in prop_nodes:
                lines.append(f'    {nid}["{full}"]')
            for nid, label, full in thm_nodes:
                lines.append(f'    {nid}["{full}"]')
            for nid, label, full in cor_nodes:
                lines.append(f'    {nid}["{full}"]')

            lines.append("")
            lines.append("    %% 建议的推导关系（请根据实际逻辑调整）")

            # 简单的默认关系：定义 -> 引理 -> 命题 -> 定理 -> 推论
            all_groups = [def_nodes, lemma_nodes, prop_nodes, thm_nodes, cor_nodes]
            for i in range(len(all_groups) - 1):
                current = all_groups[i]
                nxt = all_groups[i + 1]
                if current and nxt:
                    # 将当前组的所有节点连接到下一组的第一个节点作为示例
                    for nid, _, _ in current:
                        lines.append(f"    {nxt[0][0]} --> {nid}")

            if thm_nodes and not cor_nodes and not prop_nodes and not lemma_nodes:
                # 只有定义和定理的情况
                for nid, _, _ in def_nodes[:-1]:
                    lines.append(f"    {thm_nodes[0][0]} --> {nid}")

        lines.append("```")
        lines.append("")
        lines.append("<!-- 提示：请根据文档实际逻辑关系调整节点和边 -->")
        return '\n'.join(lines)

    def run(self, fix_suggestions: bool = False) -> None:
        """执行检查"""
        files = self.scan_files()
        self.summary.total_files = len(files)

        for fp in files:
            try:
                content = fp.read_text(encoding='utf-8')
            except Exception as e:
                print(f"  ⚠️  无法读取文件: {fp} ({e})")
                continue

            info = self.analyze_file(fp, content)
            self.results.append(info)

            # 汇总统计
            if info.has_bt:
                self.summary.files_with_bt += 1
            if info.has_mindmap:
                self.summary.files_with_mindmap += 1
            if info.has_quadrant:
                self.summary.files_with_quadrant += 1
            if info.has_state_diag:
                self.summary.files_with_state_diag += 1

            if info.grade == "A":
                self.summary.grade_a += 1
            elif info.grade == "B":
                self.summary.grade_b += 1
            elif info.grade == "C":
                self.summary.grade_c += 1
            else:
                self.summary.grade_d += 1

            if fix_suggestions and info.grade == "D":
                self.fix_suggestions[info.file_path] = self.generate_fix_suggestion(info)

        # 覆盖率 = 有推理树的文件 / 总文件
        if self.summary.total_files > 0:
            self.summary.coverage_rate = (
                self.summary.files_with_bt / self.summary.total_files * 100
            )

    def print_report(self) -> None:
        """打印文本报告"""
        s = self.summary

        print("=" * 50)
        print("📊 DEDUCTION TREE COVERAGE REPORT")
        print("=" * 50)
        print(f"Files scanned:      {s.total_files}")
        print(f"Files with BT:      {s.files_with_bt}")
        print(f"Files with mindmap: {s.files_with_mindmap}")
        print(f"Files with QC:      {s.files_with_quadrant}")
        print(f"Files with state:   {s.files_with_state_diag}")
        print()
        print(f"Grade A (rich):     {s.grade_a} ✅")
        print(f"Grade B (basic):    {s.grade_b} ⚠️")
        print(f"Grade C (weak):     {s.grade_c} ❌")
        print(f"Grade D (missing):  {s.grade_d} ❌")
        print()
        print(f"Coverage rate:      {s.coverage_rate:.1f}%")
        print("=" * 50)

        # D 级列表（缺少推理树）
        d_list = [r for r in self.results if r.grade == "D"]
        print()
        print("=" * 50)
        print("📋 MISSING DEDUCTION TREE LIST (Top 20)")
        print("=" * 50)
        if d_list:
            for r in d_list[:20]:
                print(f"  - {r.file_path}")
            if len(d_list) > 20:
                print(f"  ... and {len(d_list) - 20} more")
        else:
            print("  (None)")

        # C 级列表（推理树但无形式化元素）
        c_list = [r for r in self.results if r.grade == "C"]
        print()
        print("=" * 50)
        print("📋 MISSING FORMAL ELEMENTS IN BT")
        print("=" * 50)
        if c_list:
            for r in c_list:
                print(f"  - {r.file_path}")
        else:
            print("  (None)")

    def write_json_report(self, output_path: str) -> None:
        """输出 JSON 报告"""
        report = {
            "summary": asdict(self.summary),
            "details": [
                {
                    "file_path": r.file_path,
                    "grade": r.grade,
                    "has_bt": r.has_bt,
                    "bt_has_formal": r.bt_has_formal,
                    "has_mindmap": r.has_mindmap,
                    "has_quadrant": r.has_quadrant,
                    "has_state_diag": r.has_state_diag,
                    "formal_elements_count": len(r.formal_elements_in_doc),
                }
                for r in self.results
            ],
        }

        if self.fix_suggestions:
            report["fix_suggestions"] = self.fix_suggestions

        out_path = Path(output_path)
        try:
            out_path.write_text(
                json.dumps(report, ensure_ascii=False, indent=2),
                encoding='utf-8',
            )
            print(f"\n📄 JSON report written to: {out_path}")
        except Exception as e:
            print(f"\n❌ Failed to write JSON report: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="推理树覆盖率自动检测器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--base-path",
        default=".",
        help="项目根目录（默认当前目录）",
    )
    parser.add_argument(
        "--json-output",
        default="deduction-tree-report.json",
        help="JSON 报告输出路径（默认 deduction-tree-report.json）",
    )
    parser.add_argument(
        "--fix-suggestions",
        action="store_true",
        help="为 D 级文档输出建议的推理树结构",
    )

    args = parser.parse_args()

    checker = DeductionTreeChecker(args.base_path)
    checker.run(fix_suggestions=args.fix_suggestions)
    checker.print_report()
    checker.write_json_report(args.json_output)

    # 如果有 fix-suggestions，追加打印前几个
    if args.fix_suggestions and checker.fix_suggestions:
        print()
        print("=" * 50)
        print("🔧 FIX SUGGESTIONS (Top 5)")
        print("=" * 50)
        for idx, (path, suggestion) in enumerate(checker.fix_suggestions.items()):
            if idx >= 5:
                print(f"\n... and {len(checker.fix_suggestions) - 5} more suggestions")
                break
            print(f"\n--- {path} ---")
            print(suggestion)

    # 返回码：D级文件数 > 0 时返回 1（用于 CI）
    if checker.summary.grade_d > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
