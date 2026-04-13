#!/usr/bin/env python3
"""
生成基准测试工作负载配置和 Flink 作业提交参数
"""

import argparse
import json
from pathlib import Path


WORKLOAD_SPECS = {
    "nexmark-q0": {
        "type": "nexmark",
        "query": "q0",
        "description": "简单透传查询",
        "target_throughput_meps": 4.0,
        "duration_minutes": 10,
    },
    "nexmark-q5": {
        "type": "nexmark",
        "query": "q5",
        "description": "Hot Items 窗口聚合",
        "target_throughput_meps": 1.5,
        "duration_minutes": 15,
    },
    "state-access-100gb": {
        "type": "custom",
        "description": "100GB 状态随机访问测试",
        "state_size_gb": 100,
        "keyspace_size": 10_000_000,
        "operations_per_second": 500_000,
        "read_ratio": 0.7,
        "write_ratio": 0.3,
        "duration_minutes": 20,
    },
    "checkpoint-stress": {
        "type": "custom",
        "description": "Checkpoint 压力测试",
        "state_size_gb": 100,
        "checkpoint_interval_ms": 60_000,
        "duration_minutes": 30,
    },
    "recovery-failure": {
        "type": "custom",
        "description": "故障恢复测试",
        "state_size_gb": 50,
        "inject_failure_at_minute": 10,
        "duration_minutes": 20,
    },
}


def generate_nexmark_job_config(query: str, throughput_meps: float) -> dict:
    return {
        "job_name": f"nexmark-{query}-benchmark",
        "jar_path": "benchmark-data/flink-sql-gateway.jar",
        "parallelism": 48,
        "config": {
            "execution.checkpointing.interval": "60s",
            "execution.checkpointing.min-pause-between-checkpoints": "30s",
            "state.backend": "rocksdb",
            "state.backend.incremental": "true",
            "table.exec.source.default-phase": "CONTINUOUS_UNBOUNDED",
        },
        "nexmark_config": {
            "nexmark.workload.queries": query,
            "nexmark.workload.events.num": -1,
            "nexmark.workload.events.per.second": int(throughput_meps * 1_000_000),
        },
    }


def generate_stateful_job_config(workload_id: str, spec: dict) -> dict:
    return {
        "job_name": f"{workload_id}-benchmark",
        "jar_path": "benchmark-data/stateful-benchmark.jar",
        "parallelism": 48,
        "config": {
            "execution.checkpointing.interval": f"{spec.get('checkpoint_interval_ms', 60000)}ms",
            "state.backend": "rocksdb",
            "state.backend.incremental": "true",
            "taskmanager.memory.managed.fraction": "0.5",
        },
        "workload_config": {
            "keyspace.size": spec.get("keyspace_size", 1_000_000),
            "ops.per.second": spec.get("operations_per_second", 100_000),
            "read.ratio": spec.get("read_ratio", 0.5),
            "write.ratio": spec.get("write_ratio", 0.5),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--flink-version", default="2.0.0")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "flink_version": args.flink_version,
        "workloads": [],
    }

    for workload_id, spec in WORKLOAD_SPECS.items():
        if spec["type"] == "nexmark":
            job_config = generate_nexmark_job_config(
                spec["query"], spec["target_throughput_meps"]
            )
        else:
            job_config = generate_stateful_job_config(workload_id, spec)

        workload_file = output_dir / f"{workload_id}.json"
        with open(workload_file, "w", encoding="utf-8") as f:
            json.dump(job_config, f, indent=2, ensure_ascii=False)

        manifest["workloads"].append({
            "id": workload_id,
            "file": str(workload_file),
            "description": spec["description"],
            "duration_minutes": spec["duration_minutes"],
        })

    manifest_file = output_dir / "workload-manifest.json"
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"✅ 已生成 {len(manifest['workloads'])} 个工作负载配置到 {output_dir}")


if __name__ == "__main__":
    main()
