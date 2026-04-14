#!/usr/bin/env python3
"""
翻译进度报告生成器

功能:
1. 扫描多语言文档目录
2. 统计翻译覆盖率
3. 生成Markdown和JSON进度报告

作者: AnalysisDataFlow i18n Team
版本: 1.1.0
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class ReportGenerator:
    """翻译进度报告生成器"""

    # 中文源目录
    SOURCE_DIRS = ["Struct", "Knowledge", "Flink"]
    ROOT_SOURCE_FILES = ["README.md", "QUICK-START.md", "ARCHITECTURE.md"]

    # 翻译目录配置
    TRANSLATION_DIRS = {
        "i18n/en": "AI Translation Workspace",
        "docs/i18n/en": "Documentation Site Source",
    }

    # 输出路径
    REPORT_DIR = "i18n/translation-workflow/reports"
    MD_REPORT = f"{REPORT_DIR}/i18n-progress-report.md"
    JSON_REPORT = f"{REPORT_DIR}/i18n-progress-report.json"

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.report_dir = self.project_root / self.REPORT_DIR
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def count_source_docs(self) -> Dict[str, int]:
        """统计中文源文档数量"""
        counts = {"root": 0, "categories": {}}

        for source_dir in self.SOURCE_DIRS:
            dir_path = self.project_root / source_dir
            category_count = 0
            if dir_path.exists():
                for md_file in dir_path.rglob("*.md"):
                    if any(x in str(md_file) for x in [".archived", ".draft", "archive/"]):
                        continue
                    category_count += 1
            counts["categories"][source_dir] = category_count

        for root_file in self.ROOT_SOURCE_FILES:
            file_path = self.project_root / root_file
            if file_path.exists():
                counts["root"] += 1

        counts["total"] = sum(counts["categories"].values()) + counts["root"]
        return counts

    def count_translation_docs(self, trans_dir: str) -> Dict[str, int]:
        """统计指定翻译目录的文档数量"""
        trans_path = self.project_root / trans_dir
        counts = {"total": 0, "categories": {}}

        if not trans_path.exists():
            return counts

        for md_file in trans_path.rglob("*.md"):
            if any(x in str(md_file) for x in [".archived", ".draft", "archive/"]):
                continue
            counts["total"] += 1

            # 尝试分类（基于路径中包含的目录名）
            rel_path = md_file.relative_to(trans_path)
            category = "root"
            for part in rel_path.parts[:-1]:
                if part in self.SOURCE_DIRS:
                    category = part
                    break
            counts["categories"][category] = counts["categories"].get(category, 0) + 1

        return counts

    def generate(self) -> Dict:
        """生成完整报告"""
        source_counts = self.count_source_docs()

        report = {
            "generated_at": datetime.now().isoformat(),
            "source_language": "zh",
            "source_documents": source_counts,
            "translations": {},
            "summary": {
                "total_english_docs": 0,
                "estimated_coverage_percent": 0.0,
            },
        }

        total_en = 0
        for trans_dir, label in self.TRANSLATION_DIRS.items():
            trans_counts = self.count_translation_docs(trans_dir)
            report["translations"][trans_dir] = {
                "label": label,
                "counts": trans_counts,
            }
            total_en += trans_counts["total"]

        # 估算整体英文覆盖率（避免重复计算，取总数，但注意可能有重叠）
        # 保守估计：使用总数 / 中文源文档总数
        source_total = source_counts["total"]
        coverage = round((total_en / source_total) * 100, 2) if source_total > 0 else 0.0

        report["summary"]["total_english_docs"] = total_en
        report["summary"]["estimated_coverage_percent"] = min(coverage, 100.0)

        # 生成JSON报告
        with open(self.project_root / self.JSON_REPORT, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        # 生成Markdown报告
        md_lines = [
            "# I18n Translation Progress Report",
            "",
            f"**Generated**: {report['generated_at']}",
            "",
            "## Summary",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Chinese Source Docs | {source_total} |",
            f"| English Translated Docs (all dirs) | {total_en} |",
            f"| Estimated Coverage | {coverage}% |",
            "",
            "## Source Documents",
            "",
            f"| Category | Count |",
            f"|----------|-------|",
        ]
        for cat, count in source_counts["categories"].items():
            md_lines.append(f"| {cat}/ | {count} |")
        md_lines.append(f"| Root Files | {source_counts['root']} |")
        md_lines.append("")

        md_lines.extend([
            "## Translation Directories",
            "",
            f"| Directory | Label | Total Docs |",
            f"|-----------|-------|------------|",
        ])
        for trans_dir, data in report["translations"].items():
            md_lines.append(
                f"| {trans_dir} | {data['label']} | {data['counts']['total']} |"
            )
        md_lines.append("")

        md_lines.extend([
            "## Notes",
            "",
            "- Coverage is estimated based on total English docs across all translation directories divided by total Chinese source docs.",
            "- Some documents may exist in multiple English directories (e.g., `i18n/en/` and `docs/i18n/en/`), so coverage may be slightly overstated.",
            "- Core formal proof documents (`Struct/04-proofs/`) are currently not recommended for pure AI translation.",
        ])

        with open(self.project_root / self.MD_REPORT, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))

        print(f"Report generated:")
        print(f"  JSON: {self.JSON_REPORT}")
        print(f"  Markdown: {self.MD_REPORT}")
        print(f"  Source docs: {source_total}")
        print(f"  EN docs: {total_en}")
        print(f"  Coverage: {coverage}%")

        return report


if __name__ == "__main__":
    generator = ReportGenerator()
    generator.generate()
