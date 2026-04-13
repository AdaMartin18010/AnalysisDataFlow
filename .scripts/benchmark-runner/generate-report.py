#!/usr/bin/env python3
"""
汇总基准测试结果并生成 Markdown + JSON 报告
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


REPORT_TEMPLATE = """# AnalysisDataFlow 性能基准测试报告 v4.1

> **生成时间**: {generated_at}
> **执行环境**: {environment}
> **Flink 版本**: {flink_version}
> **状态**: {status}

---

## 1. 执行摘要

### 1.1 测试概览

| 指标 | 数值 |
|------|------|
| 测试套件 | {total_tests} 个 |
| 通过 | {passed_tests} 个 |
| 失败 | {failed_tests} 个 |
| 总执行时间 | {total_duration} |

### 1.2 关键结果

{key_results}

---

## 2. 详细测试结果

{detailed_results}

---

## 3. 环境配置

```json
{environment_json}
```

---

## 4. 结论与建议

{conclusions}

---

*本报告由 Benchmark Runner 自动生成*
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 读取 orchestrator summary
    summary_file = results_dir / "orchestrator-summary.json"
    if summary_file.exists():
        with open(summary_file, "r", encoding="utf-8") as f:
            summary = json.load(f)
    else:
        summary = {
            "environment": "unknown",
            "flink_version": "unknown",
            "results": {},
        }

    # 读取已有基准数据作为参考
    baseline_file = Path("benchmark-data/all-benchmarks.json")
    baseline = {}
    if baseline_file.exists():
        with open(baseline_file, "r", encoding="utf-8") as f:
            baseline = json.load(f)

    results = summary.get("results", {})
    total = len(results)
    passed = sum(1 for v in results.values() if v.get("status") == "success")
    failed = total - passed

    key_results_md = "\n".join([
        f"- **{k}**: {v.get('status', 'unknown')}" for k, v in results.items()
    ]) if results else "_暂无实际测试数据。本报告为模板，待真实测试执行后自动填充。_"

    detailed_md = "### 测试明细\n\n"
    for stage_name, stage_result in results.items():
        status_emoji = "✅" if stage_result.get("status") == "success" else "❌"
        detailed_md += f"#### {status_emoji} {stage_name}\n\n"
        detailed_md += f"- 状态: {stage_result.get('status', 'unknown')}\n"
        if "error" in stage_result:
            detailed_md += f"- 错误: {stage_result['error']}\n"
        detailed_md += "\n"

    conclusions = """
**当前状态说明**：

本报告为 v4.1 性能基准测试的自动化报告模板。由于实际测试集群尚未就绪，
报告中"详细测试结果"章节显示的是各测试阶段的执行状态而非真实性能数据。

**下一步行动**：
1. 搭建 3-node K8s 测试集群
2. 执行 `python .scripts/benchmark-runner/run-all-benchmarks.py --environment k8s --output-dir benchmark-results/v4.1`
3. 本报告将自动替换为包含真实性能数据的最终版本
"""

    report = REPORT_TEMPLATE.format(
        generated_at=datetime.now().replace(tzinfo=None).isoformat(),
        environment=summary.get("environment", "unknown"),
        flink_version=summary.get("flink_version", "unknown"),
        status="✅ 全部通过" if failed == 0 else ("⚠️ 部分失败" if passed > 0 else "🔴 全部失败"),
        total_tests=total,
        passed_tests=passed,
        failed_tests=failed,
        total_duration="待测量",
        key_results=key_results_md,
        detailed_results=detailed_md,
        environment_json=json.dumps(baseline.get("environment", {}), indent=2, ensure_ascii=False),
        conclusions=conclusions,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    # 同时生成 JSON 版本
    json_report = {
        "report_version": "4.1.0",
        "generated_at": datetime.now().replace(tzinfo=None).isoformat(),
        "summary": summary,
        "baseline_reference": baseline.get("metadata", {}),
        "status": "template" if total == 0 else "preliminary",
    }
    with open(output_path.with_suffix(".json"), "w", encoding="utf-8") as f:
        json.dump(json_report, f, indent=2, ensure_ascii=False)

    print(f"✅ 报告已生成: {output_path}")


if __name__ == "__main__":
    main()
