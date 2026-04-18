# 流处理反模式检测清单 (Anti-pattern Detection Checklist)

> **所属阶段**: Knowledge/09-anti-patterns | **形式化等级**: L3 | **用途**: 代码审查、生产巡检、故障排查
>
> 本清单提供系统化的反模式检测方法，覆盖代码审查、配置审计、运行时监控三个阶段。

---

## 目录

- [流处理反模式检测清单 (Anti-pattern Detection Checklist)](#流处理反模式检测清单-anti-pattern-detection-checklist)
  - [目录](#目录)
  - [1. 检测阶段概述](#1-检测阶段概述)
  - [2. 代码审查清单](#2-代码审查清单)
    - [2.1 状态管理类 (AP-01, AP-07)](#21-状态管理类-ap-01-ap-07)
    - [2.2 I/O 处理类 (AP-05)](#22-io-处理类-ap-05)
    - [2.3 序列化类 (AP-06)](#23-序列化类-ap-06)
  - [3. 配置审计清单](#3-配置审计清单)
    - [3.1 Watermark 配置 (AP-02)](#31-watermark-配置-ap-02)
    - [3.2 Checkpoint 配置 (AP-03)](#32-checkpoint-配置-ap-03)
    - [3.3 内存配置 (AP-10)](#33-内存配置-ap-10)
  - [4. 运行时监控清单](#4-运行时监控清单)
    - [4.1 数据倾斜监控 (AP-04)](#41-数据倾斜监控-ap-04)
    - [4.2 背压监控 (AP-08)](#42-背压监控-ap-08)
    - [4.3 内存与 GC 监控 (AP-10)](#43-内存与-gc-监控-ap-10)
  - [5. 故障排查速查表](#5-故障排查速查表)
    - [5.1 症状 → 反模式映射](#51-症状-反模式映射)
    - [5.2 紧急处理流程](#52-紧急处理流程)
  - [6. 工具推荐](#6-工具推荐)
    - [6.1 静态检查工具](#61-静态检查工具)
    - [6.2 运行时监控工具](#62-运行时监控工具)
    - [6.3 诊断脚本](#63-诊断脚本)
  - [7. 总结](#7-总结)
    - [7.1 检测优先级](#71-检测优先级)
    - [7.2 团队协作流程](#72-团队协作流程)

---

## 1. 检测阶段概述

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         反模式检测生命周期                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   开发阶段                    测试阶段                    生产阶段       │
│   ───────────                ───────────                ───────────     │
│        │                           │                          │         │
│        ▼                           ▼                          ▼         │
│   ┌─────────┐               ┌─────────┐                 ┌─────────┐    │
│   │代码审查 │──────────────►│性能测试 │────────────────►│监控告警 │    │
│   │Checklist│               │Checklist│                 │Checklist│    │
│   └─────────┘               └─────────┘                 └─────────┘    │
│        │                           │                          │         │
│        ▼                           ▼                          ▼         │
│   发现问题                   发现性能瓶颈                发现线上问题    │
│        │                           │                          │         │
│        └───────────────────────────┴──────────────────────────┘         │
│                                    │                                    │
│                                    ▼                                    │
│                            ┌─────────────┐                              │
│                            │  修复验证   │                              │
│                            └─────────────┘                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 代码审查清单

### 2.1 状态管理类 (AP-01, AP-07)

| 检查项 | 危险信号 | 正确做法 |
|--------|----------|----------|
| **全局状态** | 使用 `static` 变量或 `object` 单例存储状态 | 使用 `getRuntimeContext.getState()` |
| **状态类型** | 使用 `ListState` 存储大量原始事件 | 使用 `ValueState` 存储累加器 |
| **窗口函数** | `ProcessWindowFunction` 直接处理 `Iterable` | 配合 `AggregateFunction` 预聚合 |
| **状态清理** | 无 TTL 配置的状态 | 配置 `StateTtlConfig` |

```scala
// ❌ 危险代码检查点
class DangerCheck {

  // 检查点 1: 静态变量
  static Map<String, Counter> globalMap = ... // ❌ AP-01

  // 检查点 2: 原始事件累积
  class BadWindowFn extends ProcessWindowFunction[Event, Result, String, TimeWindow] {
    override def process(key: String, ctx: Context, elements: Iterable[Event], out: Collector[Result]) = {
      // elements 可能包含百万条事件 ❌ AP-07
    }
  }

  // 检查点 3: 无 TTL 状态
  val state = getRuntimeContext.getState(descriptor) // 缺少 TTL 配置 ❌
}
```

### 2.2 I/O 处理类 (AP-05)

| 检查项 | 危险信号 | 正确做法 |
|--------|----------|----------|
| **数据库访问** | 使用 `JdbcTemplate.query()` 等同步 API | 使用 `AsyncFunction` + 异步客户端 |
| **HTTP 调用** | 使用 `HttpClient.execute()` | 使用 `AsyncHttpClient` 或 Vert.x |
| **Redis 访问** | 使用 `Jedis.get()` | 使用 `Lettuce` 异步 API |
| **RPC 调用** | 使用同步 gRPC stub | 使用异步 gRPC stub |

```scala
// ❌ 危险代码模式
class IoCheck {

  // 检查点 1: JDBC 同步查询
  def queryDb(id: String): Result = {
    val stmt = conn.prepareStatement("SELECT ...") // ❌ AP-05
    stmt.executeQuery() // 阻塞！
  }

  // 检查点 2: HTTP 同步调用
  def callApi(url: String): Response = {
    httpClient.execute(new HttpGet(url)) // 阻塞！❌ AP-05
  }

  // 检查点 3: Redis 同步访问
  def getCache(key: String): String = {
    jedis.get(key) // 阻塞网络 I/O ❌ AP-05
  }
}
```

### 2.3 序列化类 (AP-06)

| 检查项 | 危险信号 | 正确做法 |
|--------|----------|----------|
| **类型注册** | 自定义 case class 未注册 Kryo | `env.getConfig.registerKryoType(classOf[X])` |
| **POJO 规范** | 缺少无参构造器或 getter/setter | 添加 `@BeanProperty` 和无参构造器 |
| **序列化器** | 复杂类型使用默认序列化 | 实现自定义 `Serializer[T]` |

```scala
// ❌ 危险代码
class SerializationCheck {

  // 检查点 1: 未注册类型
  case class MyEvent(a: String, b: Int) // 未注册 ❌ AP-06

  // 检查点 2: 非 POJO 结构
  class InvalidPojo(val field: String) { // 缺少无参构造器 ❌
    // 缺少 getter/setter
  }
}
```

---

## 3. 配置审计清单

### 3.1 Watermark 配置 (AP-02)

| 配置项 | 检查规则 | 建议值 |
|--------|----------|--------|
| `forBoundedOutOfOrderness` | 延迟是否与数据源乱序程度匹配 | p99 乱序延迟 + 20% 余量 |
| `withIdleness` | 多流场景是否配置 | 空闲超时 = 2-5 分钟 |
| `allowedLateness` | 窗口是否允许额外延迟 | 根据业务容忍度设置 |

```yaml
# 配置检查模板
watermark:
  bounded_out_of_orderness:
    value: 10s  # 检查: 是否基于实际测量？
    measured_p99: 8s  # 应有测量依据
  idleness:
    enabled: true  # 多流场景必须
    timeout: 2m
  allowed_lateness:
    value: 5m  # 检查: 是否需要捕获迟到数据？
```

### 3.2 Checkpoint 配置 (AP-03)

| 配置项 | 检查规则 | 建议值 |
|--------|----------|--------|
| `checkpointInterval` | 是否满足 RTO/5 < interval < RTO/2 | 基于 RTO 计算 |
| `checkpointTimeout` | 是否大于典型 Checkpoint 持续时间 × 2 | 30s - 10min |
| `minPauseBetweenCheckpoints` | 是否大于 Checkpoint 持续时间 | 5s - 1min |
| `incrementalCheckpoints` | 大状态（>1GB）是否启用 | 必须启用 |

```yaml
# 配置检查模板
checkpoint:
  interval: 60s  # 检查: RTO / 5 < 60s < RTO / 2 ?
  timeout: 300s
  min_pause: 30s  # 检查: > checkpoint_duration ?
  incremental: true  # 检查: 状态 > 1GB ?

  # 计算验证
  sla:
    rto: 300s  # 恢复时间目标
    calculated_max: 150s  # RTO/2
    calculated_min: 60s   # RTO/5
    current: 60s  # 应在范围内 ✓
```

### 3.3 内存配置 (AP-10)

| 配置项 | 检查规则 | 建议值 |
|--------|----------|--------|
| `managedMemory` | 是否 > 预估状态大小 / 并行度 × 1.5 | 基于状态估算 |
| `networkMemory` | 是否满足 min(并行度×64MB, 1GB) | 256MB - 1GB |
| `jvmHeap` | 是否 > max(托管内存×0.5, 2GB) | 2GB - 8GB |

```yaml
# 配置检查模板
memory:
  estimated_state_gb: 50
  parallelism: 10

  calculated:
    managed_per_tm: 7.5gb  # 50/10 * 1.5
    required_total: 12gb   # (7.5 + 2 + 0.5) * 1.2

  configured:
    managed: 8gb  # 检查: >= 7.5gb ?
    total: 12gb   # 检查: >= 12gb ?
```

---

## 4. 运行时监控清单

### 4.1 数据倾斜监控 (AP-04)

| 指标 | 告警规则 | 检查方法 |
|------|----------|----------|
| `recordsInPerSecond` | 各 subtask 差值 > 5 倍 | Flink Web UI |
| `backPressuredTimeMsPerSecond` | 集中在少数 subtask | Flink Web UI |
| `stateSize` | 各 subtask 差值 > 10 倍 | Checkpoint 统计 |

```bash
# 倾斜检测脚本(基于 Flink REST API)
curl -s "http://flink:8081/jobs/${JOB_ID}/vertices/${VERTEX_ID}/subtasks/metrics?get=recordsInPerSecond" | \
  jq '.[].value' | \
  awk '{sum+=$1; max=$1>max?$1:max; min=$1<min||min==0?$1:min} END {print "Skew ratio:", max/min}'
# 输出 > 5 表示存在倾斜
```

### 4.2 背压监控 (AP-08)

| 指标 | 告警规则 | 处理建议 |
|------|----------|----------|
| `backPressuredTimeMsPerSecond` | > 200ms/s | 扩容或优化 |
| `outputQueueLength` | 持续增长 | 检查下游瓶颈 |
| `checkpointDuration` | 持续增长 | 状态过大或背压 |

```yaml
# Prometheus 告警规则
groups:
  - name: flink_backpressure
    rules:
      - alert: FlinkHighBackpressure
        expr: flink_taskmanager_job_task_backPressuredTimeMsPerSecond > 200
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Flink task backpressure high"

      - alert: FlinkCheckpointTimeout
        expr: flink_jobmanager_checkpoint_duration_time > 600000
        for: 1m
        labels:
          severity: critical
```

### 4.3 内存与 GC 监控 (AP-10)

| 指标 | 告警规则 | 处理建议 |
|------|----------|----------|
| `heapMemoryUsage` | > 85% | 增加堆内存 |
| `gcCollectionTime` | > 10% | 优化序列化或减少状态 |
| `managedMemoryUsage` | > 90% | 增加托管内存 |

---

## 5. 故障排查速查表

### 5.1 症状 → 反模式映射

| 症状 | 可能反模式 | 快速检查 |
|------|------------|----------|
| 吞吐量突然下降 | AP-05, AP-08 | 检查是否有阻塞 I/O，查看背压 |
| OOM 频繁 | AP-07, AP-10 | 检查窗口状态大小，内存配置 |
| Checkpoint 超时 | AP-03, AP-07, AP-10 | 检查间隔配置，状态大小 |
| 结果不一致 | AP-02, AP-09 | 检查 Watermark 配置，多流 Join |
| 故障恢复慢 | AP-03 | 检查 Checkpoint 间隔 |
| CPU 低但延迟高 | AP-05 | 检查是否有阻塞 I/O |
| 某些 subtask 特别慢 | AP-04 | 检查数据倾斜 |

### 5.2 紧急处理流程

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         故障紧急处理流程                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  【发现故障】                                                           │
│       │                                                                 │
│       ▼                                                                 │
│  【判断严重程度】                                                       │
│       │                                                                 │
│       ├──► 作业失败 ──► 【检查点恢复】 ──► 成功 ──► 【根因分析】        │
│       │                      │                    │                     │
│       │                      ▼                    ▼                     │
│       │                   无检查点             修复反模式               │
│       │                      │                    │                     │
│       │                      ▼                    ▼                     │
│       │                   【数据回放】        【回归测试】              │
│       │                      │                                          │
│       │                      ▼                                          │
│       │                   【通知业务方】                                 │
│       │                                                                 │
│       └──► 性能下降 ──► 【查看指标】                                    │
│                              │                                          │
│                              ▼                                          │
│                      【定位瓶颈算子】                                   │
│                              │                                          │
│                              ▼                                          │
│                      【应用对应解决方案】                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 6. 工具推荐

### 6.1 静态检查工具

| 工具 | 用途 | 集成方式 |
|------|------|----------|
| **Checkstyle** | 代码规范检查 | Maven/Gradle 插件 |
| **SpotBugs** | 潜在 Bug 检测 | CI/CD 集成 |
| **自定义 AST 检查** | Flink 特定反模式 | 预提交钩子 |

### 6.2 运行时监控工具

| 工具 | 用途 | 数据源 |
|------|------|--------|
| **Flink Web UI** | 背压、延迟、吞吐量可视化 | Flink REST API |
| **Prometheus + Grafana** | 指标收集与告警 | Flink Metrics Reporter |
| **Jaeger/Zipkin** | 分布式追踪 | OpenTelemetry |

### 6.3 诊断脚本

```bash
#!/bin/bash
# Flink 作业健康检查脚本

JOB_ID=$1
FLINK_URL=${2:-"http://localhost:8081"}

echo "=== Flink Job Health Check ==="
echo "Job ID: $JOB_ID"

# 1. 检查背压
echo -e "\n[1/5] Checking backpressure..."
BACKPRESSURE=$(curl -s "$FLINK_URL/jobs/$JOB_ID/vertices" | jq '.vertices[] | select(.metrics.backPressuredTimeMsPerSecond > 200) | .name')
if [ -n "$BACKPRESSURE" ]; then
  echo "⚠️  High backpressure detected in:"
  echo "$BACKPRESSURE"
else
  echo "✓ Backpressure normal"
fi

# 2. 检查 Checkpoint
echo -e "\n[2/5] Checking checkpoints..."
CHECKPOINT_STATS=$(curl -s "$FLINK_URL/jobs/$JOB_ID/checkpoints")
FAILED=$(echo $CHECKPOINT_STATS | jq '.counts.failed')
if [ "$FAILED" -gt 0 ]; then
  echo "⚠️  $FAILED failed checkpoints detected"
else
  echo "✓ Checkpoints healthy"
fi

# 3. 检查数据倾斜
echo -e "\n[3/5] Checking data skew..."
# 实现类似上述的倾斜检测逻辑

echo -e "\n=== Check Complete ==="
```

---

## 7. 总结

### 7.1 检测优先级

| 优先级 | 反模式 | 检测时机 | 检测成本 |
|--------|--------|----------|----------|
| P0 | AP-08, AP-10 | 实时监控 | 低 |
| P1 | AP-02, AP-03, AP-04, AP-05, AP-07, AP-09 | 代码审查 + 运行时 | 中 |
| P2 | AP-01, AP-06 | 代码审查 | 低 |

### 7.2 团队协作流程

```
开发人员 ──► 代码审查清单 ──► 提交前自检
    │
    ▼
代码审查员 ──► 重点检查 AP-01, AP-05, AP-06
    │
    ▼
测试工程师 ──► 性能测试 ──► 检查 AP-02, AP-03, AP-04
    │
    ▼
运维工程师 ──► 生产监控 ──► 检查 AP-08, AP-10
```

---

*文档版本: v1.0 | 更新日期: 2026-04-03 | 状态: 已完成*
