#!/usr/bin/env python3
"""
AnalysisDataFlow Benchmark Orchestrator v4.1
一键执行全部性能基准测试并生成综合报告

用法:
    python run-all-benchmarks.py --environment k8s --output-dir benchmark-results/v4.1
"""

import argparse
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("benchmark-orchestrator")


class BenchmarkOrchestrator:
    def __init__(self, environment: str, output_dir: str, flink_version: str = "2.0.0"):
        self.environment = environment
        self.output_dir = Path(output_dir)
        self.flink_version = flink_version
        self.script_dir = Path(__file__).parent.resolve()
        self.start_time = None
        self.results = {}

    def run(self):
        self.start_time = datetime.now().replace(tzinfo=None)
        logger.info(f"🚀 启动基准测试套件 | 环境={self.environment} | Flink={self.flink_version}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        stages = [
            ("generate-workload", self._generate_workload),
            ("throughput-test", self._run_throughput),
            ("checkpoint-test", self._run_checkpoint),
            ("recovery-test", self._run_recovery),
            ("collect-metrics", self._collect_metrics),
            ("generate-report", self._generate_report),
        ]

        for stage_name, stage_func in stages:
            logger.info(f"▶️ 开始阶段: {stage_name}")
            try:
                stage_func()
                logger.info(f"✅ 阶段完成: {stage_name}")
            except Exception as e:
                logger.error(f"❌ 阶段失败: {stage_name} | 错误={e}")
                self.results[stage_name] = {"status": "failed", "error": str(e)}

        self._save_summary()
        logger.info(f"🏁 基准测试完成 | 输出目录={self.output_dir}")

    def _generate_workload(self):
        cmd = [
            sys.executable,
            str(self.script_dir / "generate-workload.py"),
            "--output-dir", str(self.output_dir / "workloads"),
            "--flink-version", self.flink_version,
        ]
        subprocess.run(cmd, check=True)
        self.results["generate-workload"] = {"status": "success"}

    def _run_throughput(self):
        cmd = [
            sys.executable,
            str(self.script_dir / "run-throughput-test.py"),
            "--environment", self.environment,
            "--output-dir", str(self.output_dir / "throughput"),
        ]
        subprocess.run(cmd, check=True)
        self.results["throughput-test"] = {"status": "success"}

    def _run_checkpoint(self):
        cmd = [
            sys.executable,
            str(self.script_dir / "run-checkpoint-test.py"),
            "--environment", self.environment,
            "--output-dir", str(self.output_dir / "checkpoint"),
        ]
        subprocess.run(cmd, check=True)
        self.results["checkpoint-test"] = {"status": "success"}

    def _run_recovery(self):
        cmd = [
            sys.executable,
            str(self.script_dir / "run-recovery-test.py"),
            "--environment", self.environment,
            "--output-dir", str(self.output_dir / "recovery"),
        ]
        subprocess.run(cmd, check=True)
        self.results["recovery-test"] = {"status": "success"}

    def _collect_metrics(self):
        cmd = [
            sys.executable,
            str(self.script_dir / "collect-metrics.py"),
            "--environment", self.environment,
            "--output-dir", str(self.output_dir / "metrics"),
        ]
        subprocess.run(cmd, check=True)
        self.results["collect-metrics"] = {"status": "success"}

    def _generate_report(self):
        cmd = [
            sys.executable,
            str(self.script_dir / "generate-report.py"),
            "--results-dir", str(self.output_dir),
            "--output", str(self.output_dir / "BENCHMARK-RESULT-v4.1.md"),
        ]
        subprocess.run(cmd, check=True)
        self.results["generate-report"] = {"status": "success"}

    def _save_summary(self):
        summary = {
            "orchestrator_version": "4.1.0",
            "environment": self.environment,
            "flink_version": self.flink_version,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": datetime.now().replace(tzinfo=None).isoformat(),
            "results": self.results,
        }
        with open(self.output_dir / "orchestrator-summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="AnalysisDataFlow Benchmark Orchestrator v4.1")
    parser.add_argument("--environment", required=True, choices=["k8s", "docker", "local"],
                        help="测试环境类型")
    parser.add_argument("--output-dir", required=True, help="测试结果输出目录")
    parser.add_argument("--flink-version", default="2.0.0", help="Flink 版本")
    args = parser.parse_args()

    orchestrator = BenchmarkOrchestrator(
        environment=args.environment,
        output_dir=args.output_dir,
        flink_version=args.flink_version,
    )
    orchestrator.run()


if __name__ == "__main__":
    main()
