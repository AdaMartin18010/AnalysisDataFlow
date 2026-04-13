#!/usr/bin/env python3
"""
从 Flink REST API 和 Prometheus 收集性能指标
"""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError


def fetch_flink_overview(jobmanager_url: str) -> dict:
    try:
        with urlopen(f"{jobmanager_url}/overview", timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except URLError as e:
        print(f"⚠️ 无法连接 Flink JobManager: {e}")
        return {}


def fetch_flink_job_metrics(jobmanager_url: str, job_id: str) -> dict:
    metrics = {}
    endpoints = {
        "overview": f"/jobs/{job_id}",
        "vertices": f"/jobs/{job_id}/vertices",
        "exceptions": f"/jobs/{job_id}/exceptions",
    }
    for key, endpoint in endpoints.items():
        try:
            with urlopen(f"{jobmanager_url}{endpoint}", timeout=10) as resp:
                metrics[key] = json.loads(resp.read().decode("utf-8"))
        except URLError as e:
            metrics[key] = {"error": str(e)}
    return metrics


def fetch_prometheus_query(prometheus_url: str, query: str) -> dict:
    try:
        url = f"{prometheus_url}/api/v1/query?query={query.replace(' ', '%20')}"
        with urlopen(url, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except URLError as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", default="local")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--jobmanager-url", default="http://localhost:8081")
    parser.add_argument("--prometheus-url", default="http://localhost:9090")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().replace(tzinfo=None).isoformat()
    snapshot = {
        "timestamp": timestamp,
        "environment": args.environment,
        "flink_overview": fetch_flink_overview(args.jobmanager_url),
    }

    # 如果存在活跃作业，收集作业级指标
    overview = snapshot["flink_overview"]
    if overview and "jobs-running" in overview:
        # 简化：只收集第一个运行中作业的指标
        # 实际环境中应遍历所有作业
        pass

    # Prometheus 关键查询
    prometheus_queries = {
        "task_cpu_usage": 'flink_taskmanager_Status_JVM_CPU_Load',
        "task_memory_heap_used": 'flink_taskmanager_Status_JVM_Memory_Heap_Used',
        "task_memory_heap_max": 'flink_taskmanager_Status_JVM_Memory_Heap_Max',
        "checkpoint_duration": 'flink_jobmanager_checkpointDurationTime',
        "numRecordsInPerSecond": 'flink_taskmanager_job_task_operator_numRecordsInPerSecond',
    }

    snapshot["prometheus"] = {}
    for metric_name, query in prometheus_queries.items():
        result = fetch_prometheus_query(args.prometheus_url, query)
        snapshot["prometheus"][metric_name] = result
        time.sleep(0.2)  # 避免过载

    output_file = output_dir / f"metrics-{datetime.now().replace(tzinfo=None).strftime('%Y%m%d-%H%M%S')}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

    print(f"✅ 指标快照已保存到 {output_file}")


if __name__ == "__main__":
    main()
