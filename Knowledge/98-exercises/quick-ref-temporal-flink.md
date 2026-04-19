# Temporal + Flink 分层架构快速参考卡片

> **快速查阅**: Temporal与Flink整合的分层架构、典型场景与代码模板
>
> **完整文档**: [temporal-flink-layered-architecture.md](../06-frontier/temporal-flink-layered-architecture.md)

---

## 🏗️ 分层架构速查图

### 四层架构模型

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 4: 业务编排层 (Temporal)    ← 准可判定层                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  Saga模式   │  │ 人工审批     │  │ 跨服务事务协调           │  │
│  │  补偿事务    │  │ 外部信号     │  │ 长时间运行流程           │  │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘  │
│         │                │                      │               │
│         └────────────────┼──────────────────────┘               │
│                          │ Trigger Events                       │
│  判定性: 准可判定 (Quasi-Decidable)                              │
│  延迟: 秒/分钟/天级                                              │
├──────────────────────────┼──────────────────────────────────────┤
│  Layer 3: 流处理层 (Flink)         ← 半可判定层                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ 窗口聚合    │  │ CEP检测     │  │ 实时特征计算              │  │
│  │ 时间窗口    │  │ 复杂模式    │  │ 指标统计                  │  │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘  │
│         │                │                      │               │
│  判定性: 半可判定 (Semi-Decidable)                               │
│  延迟: 毫秒级 (事件级)                                           │
├──────────────────────────┼──────────────────────────────────────┤
│  Layer 2: 消息队列层 (Kafka/Pulsar)                              │
│  职责: 事件存储、顺序保证、流复用                                  │
├──────────────────────────┼──────────────────────────────────────┤
│  Layer 1: 数据源层                                               │
│  IoT传感器 │ 交易系统 │ 用户行为日志 │ 外部API                     │
└─────────────────────────────────────────────────────────────────┘
```

### 判定性谱系定位

```
判定性强度 ↑
           │
可判定层   │  批处理 (Flink Bounded Stream)
           │  顺序计算
           │
准可判定层 │  ●──────────────────────────────────────●
           │  │ Temporal Workflow (确定性状态机)     │
           │  │  • 事件历史重放                      │
           │  │  • Saga补偿序列                      │
           │  │  • 人工审批/外部事件等待             │
           │  ●──────────────────────────────────────●
           │
半可判定层 │  ●──────────────────────────────────────●
           │  │ Flink Stream Processing             │
           │  │  • CEP模式检测 (无限流)              │
           │  │  • 窗口聚合 (水印近似)               │
           │  │  • 高吞吐实时计算                    │
           │  ●──────────────────────────────────────●
           │
不可判定层 │  通用分布式共识 (FLP不可能性)
           │  LLM Agent涌现行为
           │
           └──────────────────────────────────────────────→ 复杂度
```

---

## 📊 典型场景匹配表

| 场景 | Flink职责 | Temporal职责 | 集成模式 |
|------|-----------|--------------|----------|
| **IoT设备维护** | 温度异常检测(窗口聚合) | 创建工单→工程师确认→完成维护 | 单向触发 |
| **金融风控** | 可疑交易模式检测(CEP) | 调查流程→人工审核→风险定级 | 单向触发 |
| **电商订单** | 实时库存检查 | 订单履约→支付→发货→签收 | 双向同步 |
| **设备告警** | 多传感器聚合判断 | 分级响应(CRITICAL/WARNING) | 单向触发 |
| **实时推荐** | 用户行为实时特征 | A/B测试实验编排 | 双向同步 |
| **异常检测** | ML模型实时推理 | 告警升级→专家介入 | 单向触发 |

### 场景详细配置速查

| 场景 | Flink配置 | Temporal配置 | 端到端延迟 |
|------|-----------|--------------|------------|
| **IoT维护** | 5分钟窗口 + 60秒Checkpoint | 24小时人工确认超时 | < 6分钟 |
| **实时风控** | 1分钟窗口 + 30秒Checkpoint | 1小时调查超时 | < 2分钟 |
| **订单处理** | 直接触发无窗口 | 7天履约超时 | < 1秒 |

---

## 💻 代码模板速查

### Flink Temporal Sink (Java)

```java
/**
 * Flink Temporal Sink - 事务性工作流触发器
 */
public class TemporalWorkflowSink
    extends TwoPhaseCommitSinkFunction<AlertEvent,
                                       TemporalTransaction,
                                       Void> {

    private transient TemporalClient temporalClient;

    @Override
    protected void invoke(TemporalTransaction transaction,
                          AlertEvent value,
                          Context context) {
        transaction.addPendingWorkflow(value);
    }

    @Override
    protected void commit(TemporalTransaction transaction) {
        for (AlertEvent alert : transaction.getPendingWorkflows()) {
            String workflowId = generateWorkflowId(alert);
            try {
                temporalClient.startWorkflow(
                    "DeviceMaintenanceWorkflow",
                    workflowId,
                    alert
                );
            } catch (WorkflowExecutionAlreadyStarted e) {
                // 幂等处理:已存在的Workflow忽略
                log.info("Workflow {} already exists, skipping", workflowId);
            }
        }
    }

    private String generateWorkflowId(AlertEvent alert) {
        // 幂等性保证:相同设备+时间窗口生成相同ID
        return String.format("maintenance-%s-%d",
            alert.getDeviceId(),
            alert.getWindowStart() / 3600000); // 小时级窗口
    }
}
```

### Temporal Workflow (Go)

```go
package maintenance

import (
    "time"
    "go.temporal.io/sdk/workflow"
)

// DeviceAlert 设备告警事件
type DeviceAlert struct {
    DeviceID    string
    SensorType  string
    AlertLevel  string // WARNING, CRITICAL
    Temperature float64
    Timestamp   time.Time
}

// DeviceMaintenanceWorkflow 设备维护工作流
func DeviceMaintenanceWorkflow(
    ctx workflow.Context,
    alert DeviceAlert
) (*MaintenanceResult, error) {
    logger := workflow.GetLogger(ctx)

    // 定义Activity选项
    ao := workflow.ActivityOptions{
        StartToCloseTimeout: 10 * time.Minute,
        RetryPolicy: &temporal.RetryPolicy{
            InitialInterval:    time.Second,
            BackoffCoefficient: 2.0,
            MaximumInterval:    time.Minute,
            MaximumAttempts:    3,
        },
    }
    ctx = workflow.WithActivityOptions(ctx, ao)

    // Step 1: 创建维护工单(幂等操作)
    var ticketID string
    err := workflow.ExecuteActivity(
        ctx, CreateMaintenanceTicket, alert
    ).Get(ctx, &ticketID)
    if err != nil {
        return nil, err
    }

    // Step 2: 根据告警级别分支处理
    if alert.AlertLevel == "CRITICAL" {
        // CRITICAL:立即通知,1小时等待确认
        err = workflow.ExecuteActivity(
            ctx, SendUrgentNotification, alert, ticketID
        ).Get(ctx, nil)

        selector := workflow.NewSelector(ctx)
        var ack EngineerAcknowledgment

        selector.AddReceive(
            workflow.GetSignalChannel(ctx, "EngineerAcknowledged"),
            func(c workflow.ReceiveChannel, more bool) {
                c.Receive(ctx, &ack)
            },
        )

        // 设置超时
        timer := workflow.NewTimer(ctx, time.Hour)
        selector.AddFuture(timer, func(f workflow.Future) {
            _ = workflow.ExecuteActivity(
                ctx, EscalateToManager, ticketID
            ).Get(ctx, nil)
        })

        selector.Select(ctx)
    } else {
        // WARNING:正常流程,24小时等待
        // ...
    }

    return result, nil
}
```

### IoT温度监控 Flink Job

```java
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.api.windowing.time.Time;


public class TemperatureMonitorJob {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // 配置Checkpoint
        env.enableCheckpointing(60000); // 60秒
        env.getCheckpointConfig().setCheckpointingMode(
            CheckpointingMode.EXACTLY_ONCE);

        // 数据源:MQTT/Kafka
        DataStream<SensorReading> readings = env
            .addSource(new FlinkKafkaConsumer<>(
                "sensor-readings",
                new SensorReadingDeserializationSchema(),
                kafkaProps))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<SensorReading>forBoundedOutOfOrderness(
                    Duration.ofSeconds(30))
                .withTimestampAssigner((event, ts) -> event.getTimestamp())
            );

        // 窗口聚合:设备ID分组,1小时滚动窗口
        DataStream<DeviceAlert> alerts = readings
            .keyBy(SensorReading::getDeviceId)
            .window(TumblingEventTimeWindows.of(Time.hours(1)))
            .aggregate(new AverageTemperatureAggregate())
            .filter(avg -> avg.getAverageTemp() > 80.0)
            .map(avg -> new DeviceAlert(
                avg.getDeviceId(),
                "TEMPERATURE",
                avg.getAverageTemp() > 90.0 ? "CRITICAL" : "WARNING",
                avg.getAverageTemp(),
                avg.getWindowStart()
            ));

        // 写入Temporal触发工作流
        alerts.addSink(new TemporalWorkflowSink(
            "temporal:7233",
            "iot-maintenance"
        ));

        env.execute("IoT Temperature Monitor");
    }
}
```

### Saga模式实现

```go
// MaintenanceSaga 维护Saga管理
type MaintenanceSaga struct {
    compensations []func() error
}

func (s *MaintenanceSaga) addCompensation(fn func() error) {
    s.compensations = append(s.compensations, fn)
}

func (s *MaintenanceSaga) compensate(ctx workflow.Context) error {
    // 逆向执行补偿
    for i := len(s.compensations) - 1; i >= 0; i-- {
        if err := s.compensations[i](); err != nil {
            workflow.GetLogger(ctx).Error(
                "Compensation failed",
                "Index", i,
                "Error", err
            )
        }
    }
    return nil
}

func DeviceMaintenanceWorkflowWithSaga(
    ctx workflow.Context,
    alert DeviceAlert
) error {
    saga := &MaintenanceSaga{}

    // Step 1: 预留备件
    var reservationID string
    err := workflow.ExecuteActivity(
        ctx, ReserveSparePart, alert.DeviceID
    ).Get(ctx, &reservationID)
    if err != nil {
        return err
    }
    saga.addCompensation(func() error {
        return workflow.ExecuteActivity(
            ctx, ReleaseSparePart, reservationID
        ).Get(ctx, nil)
    })

    // Step 2: 停用设备
    err = workflow.ExecuteActivity(
        ctx, DisableDevice, alert.DeviceID
    ).Get(ctx, nil)
    if err != nil {
        saga.compensate(ctx)
        return err
    }
    saga.addCompensation(func() error {
        return workflow.ExecuteActivity(
            ctx, EnableDevice, alert.DeviceID
        ).Get(ctx, nil)
    })

    // Step 3: 执行维护
    // ...

    return nil
}
```

---

## 🔄 状态同步策略

### 模式1: 单向流（Flink → Temporal）

```
Flink                    Kafka                    Temporal
  │                       │                         │
  │── Detect Anomaly ────►│                         │
  │                       │─── Trigger Workflow ───►│
  │                       │                         │── Start Workflow
  │                       │                         │── Process
  │                       │◄── Status Update ───────┤
  │◄── Update State ──────│                         │
```

**适用场景**: Flink检测异常，Temporal处理后续流程

### 模式2: 双向同步（Flink ↔ Temporal）

```java
// Temporal Query Handler
@QueryMethod
public WorkflowState getWorkflowState() {
    return new WorkflowState(
        this.currentStatus,
        this.processedEvents.size(),
        this.pendingActivities
    );
}

// Flink AsyncFunction
public class TemporalStateLookup extends AsyncFunction<AlertEvent, EnrichedAlert> {
    @Override
    public void asyncInvoke(AlertEvent event, ResultFuture<EnrichedAlert> resultFuture) {
        CompletableFuture<WorkflowState> stateFuture = client.queryWorkflow(
            event.getDeviceId(),
            "getWorkflowState",
            WorkflowState.class
        );

        stateFuture.thenAccept(state -> {
            resultFuture.complete(Collections.singletonList(
                new EnrichedAlert(event, state)
            ));
        });
    }
}
```

**适用场景**: 需要状态反馈的复杂场景

---

## ⚖️ 错误处理对比

| 错误类型 | Flink处理方式 | Temporal处理方式 |
|----------|---------------|------------------|
| **瞬时故障** | 自动重试（Task重启） | Activity自动重试（指数退避） |
| **状态丢失** | 从Checkpoint恢复 | 从Event History重放 |
| **外部API失败** | 需Sink端处理 | Saga补偿事务 |
| **逻辑错误** | 需代码修复后重启 | Workflow版本升级 + 补丁 |
| **超时** | 窗口超时触发 | Workflow/Activity超时配置 |

---

## 📚 延伸阅读

| 文档 | 内容 |
|------|------|
| [temporal-flink-layered-architecture.md](../06-frontier/temporal-flink-layered-architecture.md) | 完整架构指南 |
| [streaming-slo-definition.md](../06-frontier/streaming-slo-definition.md) | 流处理SLO定义 |
| [realtime-data-mesh-practice.md](../06-frontier/realtime-data-mesh-practice.md) | 实时数据网格实践 |

---

*快速参考卡片 v1.0 | 最后更新: 2026-04-03*

---

*文档版本: v1.0 | 创建日期: 2026-04-15*
