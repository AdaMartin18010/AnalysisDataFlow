#!/usr/bin/env python3
"""
执行吞吐测试并收集指标
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


def run_nexmark_benchmark(jobmanager_url: str, query: str, throughput_meps: float, output_dir: Path):
    """模拟执行 Nexmark 吞吐测试。实际环境中应调用 Flink SQL Gateway 或提交 JAR。"""
    print(f"▶️ 启动 Nexmark Q{query} 测试，目标吞吐: {throughput_meps}M eps")

    # 模拟测试运行时间
    duration_sec = 600
    start = time.time()

    # 模拟指标收集（实际应通过 REST API 轮询）
    results = {
        "test_name": f"nexmark-{query}",
        "target_throughput_meps": throughput_meps,
        "start_time": datetime.now().replace(tzinfo=None).isoformat(),
        "duration_seconds": duration_sec,
        "metrics": {
            "actual_throughput_meps": round(throughput_meps * 0.98, 2),
            "latency_p50_ms": 12,
            "latency_p99_ms": 48,
            "backpressure_detected": False,
        },
        "status": "success",
    }

    # 模拟耗时
    time.sleep(1)

    output_file = output_dir / f"throughput-{query}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ Q{query} 完成 | 实际吞吐: {results['metrics']['actual_throughput_meps']}M eps | 输出: {output_file}")
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", default="local")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--jobmanager-url", default="http://localhost:8081")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    queries = [
        ("0", 4.0),
        ("1", 3.5),
        ("5", 1.5),
        ("8", 1.2),
    ]

    all_results = []
    for query, target in queries:
        result = run_nexmark_benchmark(args.jobmanager_url, query, target, output_dir)
        all_results.append(result)

    summary = {
        "test_suite": "throughput",
        "environment": args.environment,
        "timestamp": datetime.now().replace(tzinfo=None).isoformat(),
        "results": all_results,
    }
    with open(output_dir / "throughput-summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"🏁 吞吐测试套件完成，汇总保存到 {output_dir / 'throughput-summary.json'}")


if __name__ == "__main__":
    main()
