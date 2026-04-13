#!/usr/bin/env python3
"""
AnalysisDataFlow v4.1 Document Quality Audit Script (T1)
Scans Struct/, Knowledge/, Flink/ for documentation quality issues.
"""

import os
import re
import json
from collections import defaultdict, Counter
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path("e:/_src/AnalysisDataFlow")
TARGET_DIRS = [ROOT_DIR / d for d in ["Struct", "Knowledge", "Flink"]]
REPORT_PATH = ROOT_DIR / "DOCUMENT-QUALITY-AUDIT-v4.1.md"

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------
SECTION_PATTERNS = {
    "概念定义": re.compile(r'^\s*##\s+1\.\s*概念定义\s*\(?\s*Definitions\s*\)?', re.IGNORECASE | re.MULTILINE),
    "属性推导": re.compile(r'^\s*##\s+2\.\s*属性推导\s*\(?\s*Properties\s*\)?', re.IGNORECASE | re.MULTILINE),
    "关系建立": re.compile(r'^\s*##\s+3\.\s*关系建立\s*\(?\s*Relations\s*\)?', re.IGNORECASE | re.MULTILINE),
    "论证过程": re.compile(r'^\s*##\s+4\.\s*论证过程\s*\(?\s*Argumentation\s*\)?', re.IGNORECASE | re.MULTILINE),
    "形式证明": re.compile(r'^\s*##\s+5\.\s*(形式证明|工程论证)', re.IGNORECASE | re.MULTILINE),
    "实例验证": re.compile(r'^\s*##\s+6\.\s*实例验证\s*\(?\s*Examples\s*\)?', re.IGNORECASE | re.MULTILINE),
    "可视化":   re.compile(r'^\s*##\s+7\.\s*可视化\s*\(?\s*Visualizations\s*\)?', re.IGNORECASE | re.MULTILINE),
    "引用参考": re.compile(r'^\s*##\s+8\.\s*引用参考\s*\(?\s*References\s*\)?', re.IGNORECASE | re.MULTILINE),
}

THEOREM_RE = re.compile(
    r'\b(Thm|Lemma|Def|Prop|Cor)-([A-Z]+)-(\d+)-(\d+)\b',
    re.IGNORECASE
)

MERMAID_BLOCK_RE = re.compile(
    r'```\s*mermaid\s*\n(.*?)```',
    re.DOTALL | re.IGNORECASE
)

IMAGE_RE = re.compile(
    r'!\[(.*?)\]\((.*?)\)'
)

TABLE_LINE_RE = re.compile(r'^\s*\|.*\|\s*$')

# Files exempt from full 6-section template (index, readme, tracking, etc.)
EXEMPT_NAME_PATTERNS = [
    r'^00-INDEX\.md$',
    r'^README\.md$',
    r'^PROJECT-TRACKING\.md$',
    r'^THEOREM-REGISTRY\.md$',
    r'^00-.*\.md$',           # generic index files
    r'^.*-INDEX\.md$',
    r'^.*-report\.md$',
    r'^.*-changelog\.md$',
    r'^.*-template\.md$',
    r'^.*-roadmap\.md$',
]


def is_exempt(filename: str) -> bool:
    return any(re.search(p, filename, re.I) for p in EXEMPT_NAME_PATTERNS)


def gather_md_files() -> list[Path]:
    files = []
    for d in TARGET_DIRS:
        if d.exists():
            files.extend(d.rglob("*.md"))
    # sort for deterministic output
    files.sort()
    return files


def check_sections(content: str) -> dict:
    found = {}
    for name, pat in SECTION_PATTERNS.items():
        found[name] = bool(pat.search(content))
    return found


def check_theorems(content: str, filepath: Path) -> list[dict]:
    """Extract all theorem-like numbers."""
    matches = []
    for m in THEOREM_RE.finditer(content):
        matches.append({
            "type": m.group(1).capitalize(),
            "stage": m.group(2).upper(),
            "doc_num": int(m.group(3)),
            "seq_num": int(m.group(4)),
            "full": m.group(0),
            "pos": m.start(),
        })
    return matches


def check_mermaid(content: str) -> list[dict]:
    blocks = []
    for m in MERMAID_BLOCK_RE.finditer(content):
        inner = m.group(1).strip()
        issues = []
        if not inner:
            issues.append("空块")
        else:
            first_line = inner.splitlines()[0].strip() if inner else ""
            # common diagram types
            valid_starts = [
                "graph", "flowchart", "sequenceDiagram", "classDiagram",
                "stateDiagram", "stateDiagram-v2", "erDiagram", "gantt",
                "pie", "journey", "gitGraph", "requirementDiagram",
                "mindmap", "timeline", "sankey", "xychart", "block",
                "---", "title:", "%%", "subgraph"
            ]
            if not any(first_line.lower().startswith(v.lower()) for v in valid_starts):
                issues.append(f"可疑首行: {first_line[:40]}")
        blocks.append({
            "raw": inner,
            "issues": issues,
        })
    return blocks


def check_images(content: str, filepath: Path) -> list[dict]:
    issues = []
    for m in IMAGE_RE.finditer(content):
        alt = m.group(1)
        src = m.group(2).strip()
        # skip web URLs and anchors
        if src.startswith(("http://", "https://", "#", "mailto:")):
            continue
        # resolve relative to markdown file dir
        if src.startswith("/"):
            resolved = ROOT_DIR / src.lstrip("/")
        else:
            resolved = filepath.parent / src
        resolved = resolved.resolve()
        if not resolved.exists():
            issues.append({
                "alt": alt,
                "src": src,
                "resolved": str(resolved.relative_to(ROOT_DIR)) if str(ROOT_DIR) in str(resolved) else str(resolved),
            })
    return issues


def check_tables(content: str) -> list[dict]:
    """Basic table format checks."""
    lines = content.splitlines()
    issues = []
    in_table = False
    table_lines = []
    table_start = 0

    for idx, line in enumerate(lines):
        if TABLE_LINE_RE.match(line):
            if not in_table:
                in_table = True
                table_lines = [line]
                table_start = idx + 1
            else:
                table_lines.append(line)
        else:
            if in_table and len(table_lines) >= 2:
                # analyze table
                col_counts = [ln.count("|") for ln in table_lines]
                if len(set(col_counts)) > 1:
                    issues.append({
                        "line_start": table_start,
                        "line_end": idx,
                        "reason": f"列数不一致 ({set(col_counts)})",
                    })
                # check for header separator (line with only |, -, :, spaces)
                has_sep = any(
                    re.match(r'^\s*\|[-:\s|]+\|\s*$', ln)
                    for ln in table_lines[1:]
                )
                if not has_sep and len(table_lines) > 1:
                    issues.append({
                        "line_start": table_start,
                        "line_end": idx,
                        "reason": "缺少表头分隔线",
                    })
            in_table = False
            table_lines = []

    # trailing table
    if in_table and len(table_lines) >= 2:
        col_counts = [ln.count("|") for ln in table_lines]
        if len(set(col_counts)) > 1:
            issues.append({
                "line_start": table_start,
                "line_end": len(lines),
                "reason": f"列数不一致 ({set(col_counts)})",
            })
        has_sep = any(
            re.match(r'^\s*\|[-:\s|]+\|\s*$', ln)
            for ln in table_lines[1:]
        )
        if not has_sep and len(table_lines) > 1:
            issues.append({
                "line_start": table_start,
                "line_end": len(lines),
                "reason": "缺少表头分隔线",
            })

    return issues


def analyze_theorem_numbers(all_theorems: list[dict]) -> dict:
    """Check for duplicates and gaps per (type, stage, doc_num).
    Deduplicate per file first to avoid counting in-document references as duplicates.
    """
    # Deduplicate per file to avoid TOC/body/reference double counting
    seen_per_file = set()
    deduped = []
    for t in all_theorems:
        fid = (t["file"], t["type"], t["stage"], t["doc_num"], t["seq_num"])
        if fid not in seen_per_file:
            seen_per_file.add(fid)
            deduped.append(t)

    # group by (type, stage, doc_num)
    groups = defaultdict(list)
    for t in deduped:
        key = (t["type"], t["stage"], t["doc_num"])
        groups[key].append(t["seq_num"])

    duplicates = []
    gaps = []

    for key, seqs in groups.items():
        seqs_sorted = sorted(seqs)
        # duplicates across files
        seen = set()
        for s in seqs_sorted:
            if s in seen:
                duplicates.append({
                    "key": key,
                    "seq": s,
                })
            seen.add(s)
        # gaps (only if max > 1)
        if seqs_sorted:
            max_seq = max(seqs_sorted)
            expected = set(range(1, max_seq + 1))
            missing = sorted(expected - set(seqs_sorted))
            if missing:
                gaps.append({
                    "key": key,
                    "missing": missing,
                    "max": max_seq,
                })

    return {
        "total_theorems": len(all_theorems),
        "deduped_theorems": len(deduped),
        "unique_keys": len(groups),
        "duplicates": duplicates,
        "gaps": gaps,
    }


def run_audit():
    md_files = gather_md_files()
    total_files = len(md_files)

    # Accumulators
    non_compliant_docs = []
    all_theorems = []
    mermaid_stats = {"total_blocks": 0, "empty_or_bad": 0, "files_with_blocks": 0}
    image_issues = []
    table_issues = []
    exempt_count = 0
    checked_count = 0

    # Per-directory stats
    dir_stats = defaultdict(lambda: {"files": 0, "issues": 0})

    print(f"Scanning {total_files} markdown files...")

    for fp in md_files:
        rel = fp.relative_to(ROOT_DIR)
        dir_key = str(rel).split(os.sep)[0]
        dir_stats[dir_key]["files"] += 1

        try:
            content = fp.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  ERROR reading {rel}: {e}")
            continue

        filename = fp.name
        exempt = is_exempt(filename)
        if exempt:
            exempt_count += 1

        # 1. Sections
        sections = check_sections(content)
        missing = [k for k, v in sections.items() if not v]
        if not exempt and len(missing) >= 3:
            non_compliant_docs.append({
                "file": str(rel),
                "missing": missing,
                "missing_count": len(missing),
            })
            dir_stats[dir_key]["issues"] += 1

        if not exempt:
            checked_count += 1

        # 2. Theorems
        theorems = check_theorems(content, fp)
        for t in theorems:
            t["file"] = str(rel)
        all_theorems.extend(theorems)

        # 3. Mermaid
        mermaids = check_mermaid(content)
        if mermaids:
            mermaid_stats["files_with_blocks"] += 1
            mermaid_stats["total_blocks"] += len(mermaids)
            bad = sum(1 for b in mermaids if b["issues"])
            mermaid_stats["empty_or_bad"] += bad
            if bad:
                dir_stats[dir_key]["issues"] += 1

        # 4. Images
        imgs = check_images(content, fp)
        for img in imgs:
            image_issues.append({
                "file": str(rel),
                **img,
            })
            dir_stats[dir_key]["issues"] += 1

        # 5. Tables
        tbls = check_tables(content)
        for t in tbls:
            table_issues.append({
                "file": str(rel),
                **t,
            })
            dir_stats[dir_key]["issues"] += 1

    theorem_analysis = analyze_theorem_numbers(all_theorems)

    # Build report
    report_lines = []
    now = datetime.now().isoformat()

    report_lines.append(f"# AnalysisDataFlow v4.1 文档质量审计报告 (T1)")
    report_lines.append("")
    report_lines.append(f"> **生成时间**: {now}")
    report_lines.append(f"> **扫描范围**: Struct/, Knowledge/, Flink/")
    report_lines.append(f"> **扫描文件总数**: {total_files} 篇 Markdown")
    report_lines.append(f"> **审计模式**: 只读扫描 (正则+脚本)")
    report_lines.append("")

    # ------------------------------------------------------------------
    # 执行摘要
    # ------------------------------------------------------------------
    report_lines.append("## 1. 执行摘要")
    report_lines.append("")

    p0_count = len(non_compliant_docs) + len(image_issues)
    p1_count = len(theorem_analysis["duplicates"]) + len(theorem_analysis["gaps"])
    p2_count = mermaid_stats["empty_or_bad"] + len(table_issues)

    report_lines.append(f"- **六段式结构不合规文档**: {len(non_compliant_docs)} 篇 (缺少 ≥3 个核心章节)")
    report_lines.append(f"- **定理/定义原始出现次数**: {theorem_analysis['total_theorems']} 个")
    report_lines.append(f"- **定理编号重复**: {len(theorem_analysis['duplicates'])} 处")
    report_lines.append(f"- **定理编号断号**: {len(theorem_analysis['gaps'])} 处")
    report_lines.append(f"- **Mermaid 代码块**: {mermaid_stats['total_blocks']} 个 (问题块: {mermaid_stats['empty_or_bad']} 个)")
    report_lines.append(f"- **缺失图片引用**: {len(image_issues)} 处")
    report_lines.append(f"- **表格格式问题**: {len(table_issues)} 处")
    report_lines.append(f"- **P0 问题总数**: {p0_count}")
    report_lines.append(f"- **P1 问题总数**: {p1_count}")
    report_lines.append(f"- **P2 问题总数**: {p2_count}")
    report_lines.append("")

    # ------------------------------------------------------------------
    # 各检查项统计
    # ------------------------------------------------------------------
    report_lines.append("## 2. 各检查项详细统计")
    report_lines.append("")

    report_lines.append("### 2.1 六段式结构合规性")
    report_lines.append("")
    report_lines.append(f"- 需检查文档数 (非豁免): {checked_count}")
    report_lines.append(f"- 豁免文档数 (INDEX/README/报告等): {exempt_count}")
    report_lines.append(f"- **缺少 ≥3 核心章节**: {len(non_compliant_docs)} 篇")
    report_lines.append("")
    if non_compliant_docs:
        report_lines.append("| 文件路径 | 缺失章节数 | 缺失章节 |")
        report_lines.append("|---------|-----------|---------|")
        for item in sorted(non_compliant_docs, key=lambda x: x["missing_count"], reverse=True)[:50]:
            missing_str = ", ".join(item["missing"])
            report_lines.append(f"| {item['file']} | {item['missing_count']} | {missing_str} |")
        if len(non_compliant_docs) > 50:
            report_lines.append(f"| ... 还有 {len(non_compliant_docs)-50} 篇未列出 | | |")
        report_lines.append("")

    report_lines.append("### 2.2 定理编号连续性")
    report_lines.append("")
    report_lines.append(f"- 扫描到的定理/引理/定义/命题/推论总数: **{theorem_analysis['total_theorems']}**")
    report_lines.append(f"- 唯一 (Type-Stage-Doc) 组合数: **{theorem_analysis['unique_keys']}**")
    report_lines.append(f"- **重复编号**: {len(theorem_analysis['duplicates'])} 处")
    report_lines.append(f"- **断号 (gap)**: {len(theorem_analysis['gaps'])} 处")
    report_lines.append("")

    if theorem_analysis["duplicates"]:
        report_lines.append("#### 重复编号详情 (前 30)")
        report_lines.append("")
        report_lines.append("| 编号类型 | Stage | Doc | Seq |")
        report_lines.append("|---------|-------|-----|-----|")
        for dup in theorem_analysis["duplicates"][:30]:
            t, s, d = dup["key"]
            report_lines.append(f"| {t} | {s} | {d} | {dup['seq']} |")
        report_lines.append("")

    if theorem_analysis["gaps"]:
        report_lines.append("#### 断号详情 (前 30)")
        report_lines.append("")
        report_lines.append("| 编号类型 | Stage | Doc | 缺失序号 | 当前最大序号 |")
        report_lines.append("|---------|-------|-----|---------|------------|")
        for gap in theorem_analysis["gaps"][:30]:
            t, s, d = gap["key"]
            missing_str = ", ".join(str(x) for x in gap["missing"])
            report_lines.append(f"| {t} | {s} | {d} | {missing_str} | {gap['max']} |")
        report_lines.append("")

    report_lines.append("### 2.3 Mermaid 语法检查")
    report_lines.append("")
    report_lines.append(f"- 包含 Mermaid 块的文件数: {mermaid_stats['files_with_blocks']}")
    report_lines.append(f"- Mermaid 代码块总数: {mermaid_stats['total_blocks']}")
    report_lines.append(f"- 空块或可疑语法块: {mermaid_stats['empty_or_bad']}")
    report_lines.append("")

    report_lines.append("### 2.4 图片存在性检查")
    report_lines.append("")
    report_lines.append(f"- 缺失图片引用总数: {len(image_issues)}")
    if image_issues:
        report_lines.append("")
        report_lines.append("| 文件路径 | 引用路径 | Alt 文本 |")
        report_lines.append("|---------|---------|---------|")
        for img in image_issues[:50]:
            report_lines.append(f"| {img['file']} | `{img['src']}` | {img['alt'] or '-'} |")
        if len(image_issues) > 50:
            report_lines.append(f"| ... 还有 {len(image_issues)-50} 处未列出 | | |")
    report_lines.append("")

    report_lines.append("### 2.5 表格格式检查")
    report_lines.append("")
    report_lines.append(f"- 表格格式问题总数: {len(table_issues)}")
    if table_issues:
        report_lines.append("")
        report_lines.append("| 文件路径 | 起始行 | 问题描述 |")
        report_lines.append("|---------|--------|---------|")
        for t in table_issues[:50]:
            report_lines.append(f"| {t['file']} | {t['line_start']} | {t['reason']} |")
        if len(table_issues) > 50:
            report_lines.append(f"| ... 还有 {len(table_issues)-50} 处未列出 | | |")
    report_lines.append("")

    # ------------------------------------------------------------------
    # 问题清单 (P0/P1/P2)
    # ------------------------------------------------------------------
    report_lines.append("## 3. 问题清单 (按优先级分类)")
    report_lines.append("")

    report_lines.append("### P0 — 结构性/引用缺失")
    report_lines.append("")
    report_lines.append(f"- **六段式缺失 ≥3 章节**: {len(non_compliant_docs)} 篇文档")
    report_lines.append(f"- **缺失图片引用**: {len(image_issues)} 处")
    report_lines.append("")
    report_lines.append("> 修复建议: 对非豁免核心文档补齐缺失章节；修复或删除无效图片引用。")
    report_lines.append("")

    report_lines.append("### P1 — 编号一致性问题")
    report_lines.append("")
    report_lines.append(f"- **定理/引理/定义编号重复**: {len(theorem_analysis['duplicates'])} 处")
    report_lines.append(f"- **定理/引理/定义编号断号**: {len(theorem_analysis['gaps'])} 处")
    report_lines.append("")
    report_lines.append("> 修复建议: 使用统一脚本重排编号，或更新 THEOREM-REGISTRY.md 确保注册表与文档一致。")
    report_lines.append("")

    report_lines.append("### P2 — 格式与可视化问题")
    report_lines.append("")
    report_lines.append(f"- **Mermaid 空块/可疑语法**: {mermaid_stats['empty_or_bad']} 个")
    report_lines.append(f"- **表格格式异常**: {len(table_issues)} 处")
    report_lines.append("")
    report_lines.append("> 修复建议: 补充 Mermaid 图内容或修正图表类型声明；检查表格分隔线与列对齐。")
    report_lines.append("")

    # ------------------------------------------------------------------
    # 目录级分布
    # ------------------------------------------------------------------
    report_lines.append("## 4. 问题分布 (按目录)")
    report_lines.append("")
    report_lines.append("| 目录 | 扫描文件数 | 问题数 |")
    report_lines.append("|------|-----------|--------|")
    for dkey in ["Struct", "Knowledge", "Flink"]:
        st = dir_stats[dkey]
        report_lines.append(f"| {dkey}/ | {st['files']} | {st['issues']} |")
    report_lines.append("")

    # ------------------------------------------------------------------
    # 修复建议汇总
    # ------------------------------------------------------------------
    report_lines.append("## 5. 修复建议")
    report_lines.append("")
    report_lines.append("1. **批量修复图片引用**: 对缺失图片优先使用相对路径补全，或替换为有效资源。")
    report_lines.append("2. **结构合规性脚本化**: 将六段式检查集成到 `code-quality-check.yml`，对新增 PR 自动拦截。")
    report_lines.append("3. **定理编号自动化**: 在 CI 中增加定理编号扫描步骤，检测重复与断号。")
    report_lines.append("4. **Mermaid 预渲染校验**: 在 CI 中调用 `mmdc` 或 npx mermaid-cli 对 Mermaid 块做静态语法检查。")
    report_lines.append("5. **表格 lint 工具**: 引入 markdown-table-formatter 或类似工具自动修复对齐问题。")
    report_lines.append("")

    # ------------------------------------------------------------------
    # 附录: 方法说明
    # ------------------------------------------------------------------
    report_lines.append("## 附录: 审计方法说明")
    report_lines.append("")
    report_lines.append("- **六段式检查**: 使用正则匹配 `## 1. 概念定义` ~ `## 8. 引用参考` 等 8 个核心章节标题。INDEX/README/报告类文件按命名规则豁免。")
    report_lines.append("- **定理编号**: 正则 `\\b(Thm|Lemma|Def|Prop|Cor)-([A-Z]+)-(\\d+)-(\\d+)\\b`，按 (Type, Stage, DocNum) 分组检查重复与 1..N 连续性。")
    report_lines.append("- **Mermaid 检查**: 提取 ` ```mermaid ` 块，标记空块及首行非标准声明的块。")
    report_lines.append("- **图片检查**: 匹配 `![alt](src)`，跳过 HTTP 链接，对相对路径做文件存在性校验。")
    report_lines.append("- **表格检查**: 扫描 `|` 行，检查列数一致性及是否存在 `|---|---|` 风格的分隔线。")
    report_lines.append("")

    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Report written to {REPORT_PATH}")
    print("Audit complete.")


if __name__ == "__main__":
    run_audit()
