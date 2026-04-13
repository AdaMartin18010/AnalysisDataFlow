# AnalysisDataFlow 性能基准测试执行方案 v4.1

> **状态**: 🔴 待执行 | **版本**: v4.1 | **制定日期**: 2026-04-13
> **目标**: 在实际集群上执行完整的 Flink 性能基准测试，生成真实性能数据报告

---

## 1. 执行摘要

### 1.1 测试目标

本方案定义了 AnalysisDataFlow 项目 v4.1 阶段的性能基准测试执行计划，旨在：

1. **验证理论指标**：将文档中的性能声明与实际测试数据对齐
2. **建立性能基线**：为后续版本演进提供可对比的历史数据
3. **发现性能瓶颈**：识别 Flink 在特定场景下的优化空间
4. **产出实战报告**：生成可用于社区分享的白皮书级性能报告

### 1.2 测试范围

| 测试类别 | 目标指标 | 优先级 |
|---------|---------|--------|
| 吞吐测试 (Throughput) | 1M+ events/sec | P0 |
| 状态访问测试 (State Access) | 100GB 状态稳定访问 | P0 |
| Checkpoint 测试 | < 1min @ 100GB 状态 | P0 |
| 恢复时间测试 (Recovery) | < 30s 故障恢复 | P0 |
| 背压测试 (Backpressure) | 识别临界点并量化 | P1 |
| Nexmark 基准 | Q0-Q12 完整覆盖 | P1 |

---

## 2. 环境要求

### 2.1 硬件规格

```
┌─────────────────────────────────────────────────────────────┐
│                    推荐测试集群配置                          │
├─────────────────┬───────────────────────────────────────────┤
│ 节点数量         │ 3 台物理机 / 虚拟机                        │
│ CPU             │ 每台 16 核 (推荐 Intel Xeon / AMD EPYC)    │
│ 内存            │ 每台 64GB DDR4/DDR5                       │
│ 磁盘            │ NVMe SSD 500GB+ (Checkpoint 专用)         │
│ 网络            │ 10Gbps 内网，延迟 < 0.1ms                 │
│ 操作系统        │ Ubuntu 22.04 LTS / CentOS 8               │
└─────────────────┴───────────────────────────────────────────┘
```

### 2.2 软件栈

| 组件 | 版本 | 用途 |
|------|------|------|
| Apache Flink | 2.0.0 | 被测系统 |
| Kubernetes | 1.29+ | 容器编排 |
| Kafka | 3.6+ | 数据源 |
| Prometheus | 2.50+ | 指标采集 |
| Grafana | 10.3+ | 可视化 |
| Nexmark Generator | 内置 | 数据生成 |

### 2.3 K8s 资源配置

```yaml
# 集群总资源
JobManager:  1 pod × 2 cores × 4GB
TaskManager: 6 pods × 4 cores × 8GB
Total Slots: 48
```

---

## 3. 测试数据集设计

### 3.1 Nexmark 基准数据

| Query | 描述 | 目标吞吐 | 关键指标 |
|-------|------|---------|---------|
| Q0 | Pass Through | 4M+ eps | 端到端延迟 |
| Q1 | Currency Conversion | 3.5M+ eps | 算子吞吐量 |
| Q2 | Selection | 3M+ eps | 过滤效率 |
| Q5 | Hot Items | 1.5M+ eps | 窗口聚合性能 |
| Q8 | Monitor New Users | 1.2M+ eps | 双流 Join |
| Q11 | Bidding Session | 800K+ eps | Session Window |

### 3.2 自定义工作负载

```json
{
  "workload_id": "custom-state-access-100gb",
  "description": "100GB 状态随机访问测试",
  "state_size_gb": 100,
  "keyspace_size": 10000000,
  "state_backend": ["rocksdb", "hashmap", "forst"],
  "operations_per_second": 500000,
  "read_ratio": 0.7,
  "write_ratio": 0.3
}
```

---

## 4. 测试执行步骤

### 4.1 吞吐测试 (T1)

**步骤**：

1. 部署 Flink 集群 (K8s)
2. 提交 Nexmark Q0 作业，从 100K eps 开始逐步加压
3. 记录每个压力级别的吞吐和延迟
4. 找到稳定运行的最大吞吐（背压出现前）
5. 重复 Q1, Q5, Q8

**通过标准**：

- Q0 稳定吞吐 ≥ 4M eps
- P99 延迟 < 100ms

### 4.2 状态访问测试 (T2)

**步骤**：

1. 部署 Stateful 作业（KeyedProcessFunction）
2. 逐步注入状态至 100GB
3. 持续进行读写操作，记录状态访问延迟
4. 切换 State Backend（RocksDB / HashMap / ForSt）对比

**通过标准**：

- P99 状态访问延迟 < 10ms (HashMap) / < 50ms (RocksDB)
- 无 OOM 或状态丢失

### 4.3 Checkpoint 测试 (T3)

**步骤**：

1. 运行 100GB 状态作业
2. 配置 Checkpoint 间隔：30s, 60s, 120s
3. 记录每次 Checkpoint 的时长、大小、对齐时间
4. 测试增量 Checkpoint 效果

**通过标准**：

- Checkpoint 完成时间 < 60s
- Checkpoint 失败率 < 0.1%
- 对齐时间 < 5s

### 4.4 恢复时间测试 (T4)

**步骤**：

1. 运行稳定作业并积累 100GB 状态
2. 手动 kill 一个 TaskManager
3. 记录从故障发生到作业恢复运行的时间
4. 测试 JobManager HA 切换时间

**通过标准**：

- TaskManager 故障恢复 < 30s
- JobManager 故障切换 < 60s
- 数据不丢失（Exactly-Once）

### 4.5 背压测试 (T5)

**步骤**：

1. 部署有状态聚合作业
2. 以 200% 于处理能力的数据速率注入
3. 观察背压传播路径和延迟增长曲线
4. 记录系统崩溃临界点

---

## 5. 自动化脚本体系

所有测试脚本位于 `.scripts/benchmark-runner/`：

| 脚本 | 功能 |
|------|------|
| `generate-workload.py` | 生成测试数据和 Flink 作业配置 |
| `run-throughput-test.py` | 执行吞吐测试并收集指标 |
| `run-checkpoint-test.py` | 执行 Checkpoint 测试 |
| `run-recovery-test.py` | 执行故障注入与恢复测试 |
| `collect-metrics.py` | 从 Prometheus/Flink REST API 收集指标 |
| `generate-report.py` | 汇总生成 Markdown + JSON 报告 |

**一键执行**：

```bash
python .scripts/benchmark-runner/run-all-benchmarks.py \
  --environment k8s \
  --output-dir benchmark-results/v4.1
```

---

## 6. 风险与回退方案

| 风险 | 影响 | 回退方案 |
|------|------|---------|
| 云资源预算不足 | 无法搭建目标集群 | 使用 Docker Compose 单节点测试，按比例推算 |
| K8s 环境不稳定 | 测试中断 | 切换到 bare metal Flink 部署 |
| 测试数据生成瓶颈 | 无法达到目标吞吐 | 使用预生成数据集，绕过 Kafka 瓶颈 |
| 指标采集失败 | 数据缺失 | 启用 Flink 本地 metrics reporter 作为备份 |

---

## 7. 交付物清单

- [ ] `BENCHMARK-RESULT-v4.1.md` — 完整性能报告
- [ ] `benchmark-results/v4.1/*.json` — 原始测试数据
- [ ] `benchmark-data/grafana-dashboard.json` — 可视化 Dashboard
- [ ] 性能对比白皮书 (可选)

---

## 8. 执行时间表

| 阶段 | 内容 | 工时 | 负责人 |
|------|------|------|--------|
|  Week 1 | 环境搭建 + 脚本验证 | 16h | benchmark-team |
|  Week 2 | T1-T3 执行 | 24h | benchmark-team |
|  Week 3 | T4-T5 执行 + 数据整理 | 20h | benchmark-team |
|  Week 4 | 报告撰写 + Review | 12h | benchmark-team |

**总计预算**: $500 (云资源) + 72h 工时

---

*AnalysisDataFlow Performance Benchmark v4.1*
