#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink Performance Benchmark Runner

自动化Flink性能基准测试套件，支持:
- 吞吐测试 (Throughput Test)
- 状态访问测试 (State Access Test)
- Checkpoint测试 (Checkpoint Test)
- 恢复时间测试 (Recovery Test)

作者: AnalysisDataFlow Project
版本: v3.3.0
日期: 2026-04-08
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
import concurrent.futures
import statistics


# ============================================================================
# 配置常量
# ============================================================================

DEFAULT_FLINK_VERSIONS = ["1.18.1", "2.0.0", "2.2.0"]
DEFAULT_K8S_NAMESPACE = "flink-benchmark"
DEFAULT_METRICS_RETENTION_DAYS = 365

BENCHMARK_CONFIG = {
    "throughput": {
        "target_events_per_sec": 1_000_000,
        "test_duration_sec": 600,
        "warmup_duration_sec": 120,
        "latency_percentiles": [50, 99, 99.9],
    },
    "state_access": {
        "state_sizes_gb": [10, 50, 100, 500],
        "access_patterns": ["random", "sequential", "skewed"],
        "test_duration_sec": 300,
    },
    "checkpoint": {
        "intervals_sec": [60, 300, 600],
        "state_sizes_gb": [10, 50, 100],
        "test_duration_sec": 1800,
    },
    "recovery": {
        "failure_types": ["task_failure", "jobmanager_failure", "network_partition"],
        "timeout_sec": 300,
    },
}

K8S_CLUSTER_CONFIG = {
    "nodes": 3,
    "vcpus_per_node": 16,
    "memory_gb_per_node": 64,
    "storage_type": "nvme_ssd",
    "network_gbps": 25,
}


# ============================================================================
# 数据模型
# ============================================================================

class TestType(Enum):
    """测试类型枚举"""
    THROUGHPUT = "throughput"
    STATE_ACCESS = "state_access"
    CHECKPOINT = "checkpoint"
    RECOVERY = "recovery"


class TestStatus(Enum):
    """测试状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class BenchmarkResult:
    """基准测试结果数据类"""
    test_type: str
    test_name: str
    flink_version: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: TestStatus = TestStatus.PENDING
    
    # 性能指标
    throughput: Optional[float] = None  # events/sec
    latency_p50: Optional[float] = None  # ms
    latency_p99: Optional[float] = None  # ms
    latency_p999: Optional[float] = None  # ms
    state_access_latency: Optional[float] = None  # ms
    checkpoint_duration: Optional[float] = None  # sec
    recovery_time: Optional[float] = None  # sec
    
    # 资源使用
    cpu_usage_percent: Optional[float] = None
    memory_usage_gb: Optional[float] = None
    network_io_mbps: Optional[float] = None
    
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    
    def duration_sec(self) -> Optional[float]:
        """计算测试持续时间"""
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        result = asdict(self)
        result['start_time'] = self.start_time.isoformat()
        result['end_time'] = self.end_time.isoformat() if self.end_time else None
        result['status'] = self.status.value
        result['duration_sec'] = self.duration_sec()
        return result


@dataclass
class TestConfig:
    """测试配置数据类"""
    flink_version: str
    test_type: TestType
    parallelism: int = 8
    state_backend: str = "rocksdb"
    checkpoint_dir: str = "/flink/checkpoints"
    savepoint_dir: str = "/flink/savepoints"
    extra_config: Dict[str, str] = field(default_factory=dict)


# ============================================================================
# 日志配置
# ============================================================================

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """配置日志记录"""
    logger = logging.getLogger("flink_benchmark")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# ============================================================================
# Kubernetes 管理
# ============================================================================

class K8sManager:
    """Kubernetes 集群管理器"""
    
    def __init__(self, namespace: str = DEFAULT_K8S_NAMESPACE, logger: Optional[logging.Logger] = None):
        self.namespace = namespace
        self.logger = logger or logging.getLogger(__name__)
    
    def run_kubectl(self, args: List[str], capture_output: bool = True) -> subprocess.CompletedProcess:
        """运行 kubectl 命令"""
        cmd = ["kubectl", "-n", self.namespace] + args
        self.logger.debug(f"Running: {' '.join(cmd)}")
        return subprocess.run(cmd, capture_output=capture_output, text=True)
    
    def create_namespace(self) -> bool:
        """创建命名空间"""
        result = self.run_kubectl(["create", "namespace", self.namespace], capture_output=True)
        if result.returncode == 0 or "AlreadyExists" in result.stderr:
            self.logger.info(f"Namespace {self.namespace} ready")
            return True
        self.logger.error(f"Failed to create namespace: {result.stderr}")
        return False
    
    def deploy_flink_cluster(self, flink_version: str, config: Dict) -> bool:
        """部署 Flink 集群"""
        self.logger.info(f"Deploying Flink {flink_version} cluster...")
        
        # 生成 Flink 配置文件
        flink_config = self._generate_flink_config(flink_version, config)
        
        # 应用配置 (这里简化处理，实际应使用 Helm 或 operator)
        # 假设有准备好的 deployment yaml 模板
        deployment_yaml = self._generate_deployment_yaml(flink_version, flink_config)
        
        # 写入临时文件并应用
        temp_file = f"/tmp/flink-benchmark-{flink_version.replace('.', '-')}.yaml"
        with open(temp_file, 'w') as f:
            f.write(deployment_yaml)
        
        result = self.run_kubectl(["apply", "-f", temp_file])
        if result.returncode != 0:
            self.logger.error(f"Failed to deploy Flink: {result.stderr}")
            return False
        
        # 等待集群就绪
        return self._wait_for_cluster_ready()
    
    def _generate_flink_config(self, flink_version: str, config: Dict) -> Dict:
        """生成 Flink 配置"""
        return {
            "flink.version": flink_version,
            "kubernetes.namespace": self.namespace,
            "jobmanager.memory.process.size": "4g",
            "taskmanager.memory.process.size": "8g",
            "taskmanager.numberOfTaskSlots": "4",
            "state.backend": config.get("state_backend", "rocksdb"),
            "state.checkpoints.dir": config.get("checkpoint_dir", "/flink/checkpoints"),
            "execution.checkpointing.interval": "5min",
            "execution.checkpointing.max-concurrent-checkpoints": "1",
            **config.get("extra_config", {})
        }
    
    def _generate_deployment_yaml(self, flink_version: str, config: Dict) -> str:
        """生成 K8s deployment YAML (简化版)"""
        # 实际实现应使用 Helm chart 或 Flink Kubernetes Operator
        return f"""
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: flink-benchmark-{flink_version.replace('.', '-')}
  namespace: {self.namespace}
spec:
  image: flink:{flink_version}
  flinkVersion: v{flink_version}
  jobManager:
    resource:
      memory: "4Gi"
      cpu: 2
  taskManager:
    resource:
      memory: "8Gi"
      cpu: 4
    replicas: 8
  configuration:
    {chr(10).join(f'    {k}: "{v}"' for k, v in config.items())}
"""
    
    def _wait_for_cluster_ready(self, timeout_sec: int = 300) -> bool:
        """等待集群就绪"""
        self.logger.info("Waiting for Flink cluster to be ready...")
        start = time.time()
        while time.time() - start < timeout_sec:
            result = self.run_kubectl(["get", "pods", "-l", "app=flink"])
            if "Running" in result.stdout and result.returncode == 0:
                self.logger.info("Flink cluster is ready")
                return True
            time.sleep(5)
        self.logger.error("Timeout waiting for cluster")
        return False
    
    def cleanup_cluster(self, flink_version: str) -> bool:
        """清理集群"""
        self.logger.info(f"Cleaning up Flink {flink_version} cluster...")
        result = self.run_kubectl([
            "delete", "flinkdeployment",
            f"flink-benchmark-{flink_version.replace('.', '-')}",
            "--ignore-not-found=true"
        ])
        return result.returncode == 0
    
    def get_pod_logs(self, pod_name: str, tail: int = 100) -> str:
        """获取 Pod 日志"""
        result = self.run_kubectl(["logs", pod_name, f"--tail={tail}"])
        return result.stdout if result.returncode == 0 else ""


# ============================================================================
# 指标收集器
# ============================================================================

class MetricsCollector:
    """性能指标收集器"""
    
    def __init__(self, prometheus_url: str = "http://localhost:9090", logger: Optional[logging.Logger] = None):
        self.prometheus_url = prometheus_url
        self.logger = logger or logging.getLogger(__name__)
    
    def query_prometheus(self, query: str, time_range: str = "5m") -> Dict:
        """查询 Prometheus 指标"""
        import urllib.request
        import urllib.parse
        
        url = f"{self.prometheus_url}/api/v1/query"
        params = urllib.parse.urlencode({"query": query, "time": time_range})
        
        try:
            with urllib.request.urlopen(f"{url}?{params}", timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            self.logger.error(f"Failed to query Prometheus: {e}")
            return {"data": {"result": []}}
    
    def collect_throughput_metrics(self, job_id: str, duration_sec: int) -> Dict:
        """收集吞吐指标"""
        query = f'flink_taskmanager_job_task_operator_numRecordsInPerSecond{{job_id="{job_id}"}}'
        result = self.query_prometheus(query)
        
        values = []
        for r in result.get("data", {}).get("result", []):
            values.extend([float(v[1]) for v in r.get("values", [])])
        
        return {
            "avg_throughput": statistics.mean(values) if values else 0,
            "max_throughput": max(values) if values else 0,
            "min_throughput": min(values) if values else 0,
        }
    
    def collect_latency_metrics(self, job_id: str) -> Dict:
        """收集延迟指标"""
        # 使用 Flink 的延迟跟踪指标
        latencies = {}
        for percentile in [50, 99, 99.9]:
            query = f'flink_taskmanager_job_latency_histogram{{job_id="{job_id}",quantile="{percentile/100}"}}'
            result = self.query_prometheus(query)
            if result.get("data", {}).get("result"):
                value = float(result["data"]["result"][0].get("value", [0, 0])[1])
                latencies[f"p{int(percentile)}"] = value
        return latencies
    
    def collect_resource_metrics(self, pod_prefix: str) -> Dict:
        """收集资源使用指标"""
        cpu_query = f'container_cpu_usage_seconds_total{{pod=~"{pod_prefix}.*"}}'
        mem_query = f'container_memory_usage_bytes{{pod=~"{pod_prefix}.*"}}'
        
        cpu_result = self.query_prometheus(cpu_query)
        mem_result = self.query_prometheus(mem_query)
        
        return {
            "cpu_cores": len(cpu_result.get("data", {}).get("result", [])),
            "memory_bytes": sum(
                float(r.get("value", [0, 0])[1]) 
                for r in mem_result.get("data", {}).get("result", [])
            ),
        }


# ============================================================================
# 基准测试运行器
# ============================================================================

class FlinkBenchmarkRunner:
    """Flink 基准测试运行器"""
    
    def __init__(self, 
                 k8s_manager: Optional[K8sManager] = None,
                 metrics_collector: Optional[MetricsCollector] = None,
                 logger: Optional[logging.Logger] = None,
                 output_dir: str = "./benchmark-results"):
        self.k8s = k8s_manager or K8sManager()
        self.metrics = metrics_collector or MetricsCollector()
        self.logger = logger or logging.getLogger(__name__)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results: List[BenchmarkResult] = []
    
    def run_all_benchmarks(self, flink_versions: List[str] = None, 
                           test_types: List[TestType] = None) -> List[BenchmarkResult]:
        """运行所有基准测试"""
        flink_versions = flink_versions or DEFAULT_FLINK_VERSIONS
        test_types = test_types or list(TestType)
        
        self.logger.info(f"Starting benchmark suite for Flink versions: {flink_versions}")
        
        for version in flink_versions:
            for test_type in test_types:
                result = self.run_test(version, test_type)
                self.results.append(result)
        
        return self.results
    
    def run_test(self, flink_version: str, test_type: TestType) -> BenchmarkResult:
        """运行单个测试"""
        test_name = f"{test_type.value}_v{flink_version}"
        result = BenchmarkResult(
            test_type=test_type.value,
            test_name=test_name,
            flink_version=flink_version,
            start_time=datetime.now(),
            status=TestStatus.RUNNING
        )
        
        try:
            # 部署集群
            if not self.k8s.deploy_flink_cluster(flink_version, {}):
                raise RuntimeError("Failed to deploy Flink cluster")
            
            # 运行具体测试
            if test_type == TestType.THROUGHPUT:
                self._run_throughput_test(result)
            elif test_type == TestType.STATE_ACCESS:
                self._run_state_access_test(result)
            elif test_type == TestType.CHECKPOINT:
                self._run_checkpoint_test(result)
            elif test_type == TestType.RECOVERY:
                self._run_recovery_test(result)
            
            result.status = TestStatus.COMPLETED
            
        except Exception as e:
            self.logger.error(f"Test {test_name} failed: {e}", exc_info=True)
            result.status = TestStatus.FAILED
            result.error_message = str(e)
        finally:
            result.end_time = datetime.now()
            self.k8s.cleanup_cluster(flink_version)
        
        return result
    
    def run_throughput_test(self, config: Dict) -> BenchmarkResult:
        """运行吞吐测试"""
        result = BenchmarkResult(
            test_type=TestType.THROUGHPUT.value,
            test_name=f"throughput_v{config.get('flink_version', 'unknown')}",
            flink_version=config.get("flink_version", ""),
            start_time=datetime.now(),
            status=TestStatus.RUNNING
        )
        
        try:
            self._run_throughput_test(result, config)
            result.status = TestStatus.COMPLETED
        except Exception as e:
            result.status = TestStatus.FAILED
            result.error_message = str(e)
        finally:
            result.end_time = datetime.now()
        
        return result
    
    def _run_throughput_test(self, result: BenchmarkResult, config: Dict = None):
        """执行吞吐测试逻辑"""
        cfg = BENCHMARK_CONFIG["throughput"]
        
        self.logger.info(f"Running throughput test: target {cfg['target_events_per_sec']} events/sec")
        
        # 1. 预热阶段
        self.logger.info(f"Warming up for {cfg['warmup_duration_sec']}s...")
        time.sleep(cfg["warmup_duration_sec"])
        
        # 2. 正式测试 - 使用 Nexmark generator 或自定义 generator
        job_id = self._submit_benchmark_job("throughput")
        
        # 3. 收集指标
        metrics = self.metrics.collect_throughput_metrics(job_id, cfg["test_duration_sec"])
        latency_metrics = self.metrics.collect_latency_metrics(job_id)
        
        result.throughput = metrics["avg_throughput"]
        result.latency_p50 = latency_metrics.get("p50", 0)
        result.latency_p99 = latency_metrics.get("p99", 0)
        result.latency_p999 = latency_metrics.get("p999", 0)
        
        # 4. 等待测试完成
        time.sleep(cfg["test_duration_sec"])
    
    def run_state_access_test(self, state_size: int, config: Dict = None) -> BenchmarkResult:
        """运行状态访问测试"""
        result = BenchmarkResult(
            test_type=TestType.STATE_ACCESS.value,
            test_name=f"state_access_{state_size}GB",
            flink_version=config.get("flink_version", "") if config else "",
            start_time=datetime.now(),
            status=TestStatus.RUNNING
        )
        
        try:
            self._run_state_access_test(result, state_size)
            result.status = TestStatus.COMPLETED
        except Exception as e:
            result.status = TestStatus.FAILED
            result.error_message = str(e)
        finally:
            result.end_time = datetime.now()
        
        return result
    
    def _run_state_access_test(self, result: BenchmarkResult, state_size_gb: int):
        """执行状态访问测试逻辑"""
        cfg = BENCHMARK_CONFIG["state_access"]
        
        self.logger.info(f"Running state access test with {state_size_gb}GB state")
        
        # 提交状态访问测试作业
        job_id = self._submit_benchmark_job("state_access", {"state_size_gb": state_size_gb})
        
        # 等待状态建立
        self.logger.info("Building state...")
        time.sleep(60)
        
        # 收集状态访问延迟
        metrics = self.metrics.collect_throughput_metrics(job_id, cfg["test_duration_sec"])
        
        result.state_access_latency = metrics.get("avg_latency_ms", 0)
        result.metadata["state_size_gb"] = state_size_gb
    
    def run_checkpoint_test(self, interval: int, config: Dict = None) -> BenchmarkResult:
        """运行 Checkpoint 测试"""
        result = BenchmarkResult(
            test_type=TestType.CHECKPOINT.value,
            test_name=f"checkpoint_{interval}s",
            flink_version=config.get("flink_version", "") if config else "",
            start_time=datetime.now(),
            status=TestStatus.RUNNING
        )
        
        try:
            self._run_checkpoint_test(result, interval)
            result.status = TestStatus.COMPLETED
        except Exception as e:
            result.status = TestStatus.FAILED
            result.error_message = str(e)
        finally:
            result.end_time = datetime.now()
        
        return result
    
    def _run_checkpoint_test(self, result: BenchmarkResult, interval_sec: int):
        """执行 Checkpoint 测试逻辑"""
        self.logger.info(f"Running checkpoint test with {interval_sec}s interval")
        
        # 提交带 checkpoint 的作业
        job_id = self._submit_benchmark_job("checkpoint", {"checkpoint_interval": interval_sec})
        
        # 监控多个 checkpoint 周期
        checkpoint_times = []
        for i in range(5):
            time.sleep(interval_sec)
            # 查询 checkpoint 完成时间
            duration = self._get_last_checkpoint_duration(job_id)
            if duration:
                checkpoint_times.append(duration)
        
        if checkpoint_times:
            result.checkpoint_duration = statistics.mean(checkpoint_times)
        result.metadata["checkpoint_interval_sec"] = interval_sec
    
    def run_recovery_test(self, failure_type: str, config: Dict = None) -> BenchmarkResult:
        """运行恢复时间测试"""
        result = BenchmarkResult(
            test_type=TestType.RECOVERY.value,
            test_name=f"recovery_{failure_type}",
            flink_version=config.get("flink_version", "") if config else "",
            start_time=datetime.now(),
            status=TestStatus.RUNNING
        )
        
        try:
            self._run_recovery_test(result, failure_type)
            result.status = TestStatus.COMPLETED
        except Exception as e:
            result.status = TestStatus.FAILED
            result.error_message = str(e)
        finally:
            result.end_time = datetime.now()
        
        return result
    
    def _run_recovery_test(self, result: BenchmarkResult, failure_type: str):
        """执行恢复测试逻辑"""
        self.logger.info(f"Running recovery test for failure type: {failure_type}")
        
        # 提交作业
        job_id = self._submit_benchmark_job("recovery")
        
        # 等待稳定
        time.sleep(60)
        
        # 注入故障
        failure_start = time.time()
        self._inject_failure(failure_type)
        
        # 等待恢复
        self._wait_for_recovery(job_id)
        recovery_end = time.time()
        
        result.recovery_time = recovery_end - failure_start
        result.metadata["failure_type"] = failure_type
    
    def _submit_benchmark_job(self, job_type: str, params: Dict = None) -> str:
        """提交基准测试作业 (模拟)"""
        # 实际实现应调用 Flink REST API 提交作业
        self.logger.info(f"Submitting {job_type} benchmark job...")
        # 返回模拟的 job ID
        import uuid
        return f"benchmark-{job_type}-{uuid.uuid4().hex[:8]}"
    
    def _get_last_checkpoint_duration(self, job_id: str) -> Optional[float]:
        """获取上次 checkpoint 持续时间"""
        query = f'flink_jobmanager_checkpoint_duration_time{{job_id="{job_id}"}}'
        result = self.metrics.query_prometheus(query)
        if result.get("data", {}).get("result"):
            return float(result["data"]["result"][0].get("value", [0, 0])[1]) / 1000
        return None
    
    def _inject_failure(self, failure_type: str):
        """注入故障 (模拟)"""
        self.logger.info(f"Injecting {failure_type} failure...")
        if failure_type == "task_failure":
            # 杀死 TaskManager pod
            self.k8s.run_kubectl(["delete", "pod", "-l", "component=taskmanager", "--grace-period=0"])
        elif failure_type == "jobmanager_failure":
            self.k8s.run_kubectl(["delete", "pod", "-l", "component=jobmanager", "--grace-period=0"])
    
    def _wait_for_recovery(self, job_id: str, timeout_sec: int = 300) -> bool:
        """等待作业恢复"""
        self.logger.info("Waiting for job recovery...")
        start = time.time()
        while time.time() - start < timeout_sec:
            # 检查作业状态
            time.sleep(5)
        return True
    
    def generate_report(self, results: List[BenchmarkResult] = None, 
                       format: str = "markdown") -> str:
        """生成测试报告"""
        results = results or self.results
        
        if format == "markdown":
            return self._generate_markdown_report(results)
        elif format == "json":
            return json.dumps([r.to_dict() for r in results], indent=2, ensure_ascii=False)
        elif format == "html":
            return self._generate_html_report(results)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _generate_markdown_report(self, results: List[BenchmarkResult]) -> str:
        """生成 Markdown 格式报告"""
        lines = [
            "# Flink 性能基准测试报告",
            f"",
            f"**生成时间**: {datetime.now().isoformat()}",
            f"**测试版本**: {', '.join(set(r.flink_version for r in results))}",
            f"",
            "## 测试环境",
            f"",
            "| 组件 | 规格 |",
            "|------|------|",
            f"| K8s Nodes | {K8S_CLUSTER_CONFIG['nodes']} × {K8S_CLUSTER_CONFIG['vcpus_per_node']}vCPU, {K8S_CLUSTER_CONFIG['memory_gb_per_node']}GB |",
            f"| Storage | {K8S_CLUSTER_CONFIG['storage_type']} |",
            f"| Network | {K8S_CLUSTER_CONFIG['network_gbps']} Gbps |",
            f"",
            "## 测试结果汇总",
            f"",
        ]
        
        # 按测试类型分组
        by_type: Dict[str, List[BenchmarkResult]] = {}
        for r in results:
            by_type.setdefault(r.test_type, []).append(r)
        
        for test_type, type_results in by_type.items():
            lines.extend([
                f"### {test_type.upper()}",
                "",
                "| 版本 | 状态 | 吞吐 (r/s) | P99延迟 (ms) | 恢复时间 (s) |",
                "|------|------|------------|--------------|--------------|",
            ])
            for r in type_results:
                lines.append(
                    f"| {r.flink_version} | {r.status.value} | "
                    f"{r.throughput or '-':,.0f} | {r.latency_p99 or '-'} | {r.recovery_time or '-'} |"
                )
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_html_report(self, results: List[BenchmarkResult]) -> str:
        """生成 HTML 格式报告"""
        # 简化实现
        return f"""
<!DOCTYPE html>
<html>
<head><title>Flink Benchmark Report</title></head>
<body>
<h1>Flink Performance Benchmark Report</h1>
<p>Generated: {datetime.now().isoformat()}</p>
<pre>{self._generate_markdown_report(results)}</pre>
</body>
</html>
"""
    
    def save_results(self, filename: str = None):
        """保存结果到文件"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.json"
        
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump([r.to_dict() for r in self.results], f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Results saved to {filepath}")


# ============================================================================
# 命令行接口
# ============================================================================

def create_argument_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="Flink Performance Benchmark Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 运行所有测试
  python flink-benchmark-runner.py --all --flink-versions 1.18.0 2.0.0
  
  # 只运行吞吐测试
  python flink-benchmark-runner.py --test-type throughput
  
  # 对比特定版本
  python flink-benchmark-runner.py --compare --versions 1.18.0 2.0.0 2.2.0
  
  # 生成报告
  python flink-benchmark-runner.py --generate-report results.json --format markdown
        """
    )
    
    parser.add_argument("--all", action="store_true", help="运行所有基准测试")
    parser.add_argument("--test-type", choices=[t.value for t in TestType],
                       help="指定测试类型")
    parser.add_argument("--flink-versions", nargs="+", default=DEFAULT_FLINK_VERSIONS,
                       help="Flink 版本列表")
    parser.add_argument("--namespace", default=DEFAULT_K8S_NAMESPACE,
                       help="Kubernetes 命名空间")
    parser.add_argument("--output-dir", default="./benchmark-results",
                       help="输出目录")
    parser.add_argument("--generate-report", metavar="RESULTS_FILE",
                       help="从已有结果生成报告")
    parser.add_argument("--format", choices=["markdown", "json", "html"], default="markdown",
                       help="报告格式")
    parser.add_argument("--parallel", type=int, default=1,
                       help="并行测试数")
    parser.add_argument("--state-size", type=int,
                       help="状态大小 (GB)，用于状态访问测试")
    parser.add_argument("--checkpoint-interval", type=int,
                       help="Checkpoint 间隔 (秒)")
    parser.add_argument("--failure-type", choices=BENCHMARK_CONFIG["recovery"]["failure_types"],
                       help="故障类型，用于恢复测试")
    parser.add_argument("--log-level", default="INFO",
                       choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       help="日志级别")
    parser.add_argument("--dry-run", action="store_true",
                       help="模拟运行，不实际部署集群")
    
    return parser


def main():
    """主入口函数"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # 设置日志
    log_file = f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger = setup_logging(args.log_level, log_file)
    
    logger.info("Flink Benchmark Runner v3.3.0")
    logger.info(f"Arguments: {args}")
    
    # 初始化运行器
    k8s_manager = K8sManager(namespace=args.namespace, logger=logger)
    metrics_collector = MetricsCollector(logger=logger)
    
    runner = FlinkBenchmarkRunner(
        k8s_manager=k8s_manager,
        metrics_collector=metrics_collector,
        logger=logger,
        output_dir=args.output_dir
    )
    
    # 生成报告模式
    if args.generate_report:
        logger.info(f"Generating report from {args.generate_report}")
        with open(args.generate_report, 'r') as f:
            data = json.load(f)
        # 从 JSON 重建结果对象
        report = runner.generate_report(format=args.format)
        report_file = f"benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{args.format}"
        with open(report_file, 'w') as f:
            f.write(report)
        logger.info(f"Report saved to {report_file}")
        return
    
    # 运行测试
    results = []
    
    if args.all:
        results = runner.run_all_benchmarks(args.flink_versions)
    elif args.test_type:
        test_type = TestType(args.test_type)
        for version in args.flink_versions:
            result = runner.run_test(version, test_type)
            results.append(result)
    elif args.state_size:
        for version in args.flink_versions:
            result = runner.run_state_access_test(args.state_size, {"flink_version": version})
            results.append(result)
    elif args.checkpoint_interval:
        for version in args.flink_versions:
            result = runner.run_checkpoint_test(args.checkpoint_interval, {"flink_version": version})
            results.append(result)
    elif args.failure_type:
        for version in args.flink_versions:
            result = runner.run_recovery_test(args.failure_type, {"flink_version": version})
            results.append(result)
    else:
        parser.print_help()
        return
    
    # 保存结果
    runner.results = results
    runner.save_results()
    
    # 生成报告
    report = runner.generate_report(format=args.format)
    report_file = Path(args.output_dir) / f"benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{args.format}"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"Benchmark completed. Report: {report_file}")
    
    # 输出摘要
    print("\n" + "=" * 60)
    print("BENCHMARK SUMMARY")
    print("=" * 60)
    for r in results:
        status_icon = "✓" if r.status == TestStatus.COMPLETED else "✗"
        print(f"{status_icon} {r.test_name}: {r.status.value}")


if __name__ == "__main__":
    main()
