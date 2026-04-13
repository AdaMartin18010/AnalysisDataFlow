# AnalysisDataFlow 性能基准测试报告 v4.1

> **生成时间**: 2026-04-13T23:18:50.967953
> **执行环境**: unknown
> **Flink 版本**: unknown
> **状态**: ✅ 全部通过

---

## 1. 执行摘要

### 1.1 测试概览

| 指标 | 数值 |
|------|------|
| 测试套件 | 0 个 |
| 通过 | 0 个 |
| 失败 | 0 个 |
| 总执行时间 | 待测量 |

### 1.2 关键结果

_暂无实际测试数据。本报告为模板，待真实测试执行后自动填充。_

---

## 2. 详细测试结果

### 测试明细



---

## 3. 环境配置

```json
{
  "flink_versions": [
    "1.18.1",
    "2.0.0",
    "2.2.0"
  ],
  "hardware_specs": {
    "cpu_cores": 16,
    "memory_gb": 64,
    "disk_type": "NVMe SSD",
    "network_gbps": 10
  },
  "cluster_config": {
    "nodes": 3,
    "task_managers": 6,
    "slots_per_tm": 8,
    "total_slots": 48
  }
}
```

---

## 4. 结论与建议


**当前状态说明**：

本报告为 v4.1 性能基准测试的自动化报告模板。由于实际测试集群尚未就绪，
报告中"详细测试结果"章节显示的是各测试阶段的执行状态而非真实性能数据。

**下一步行动**：

1. 搭建 3-node K8s 测试集群
2. 执行 `python .scripts/benchmark-runner/run-all-benchmarks.py --environment k8s --output-dir benchmark-results/v4.1`
3. 本报告将自动替换为包含真实性能数据的最终版本


---

_本报告由 Benchmark Runner 自动生成_
