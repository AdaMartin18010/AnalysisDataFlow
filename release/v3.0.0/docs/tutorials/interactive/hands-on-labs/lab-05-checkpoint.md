# Lab 5: Checkpoint 与恢复

> 所属阶段: Flink/Hands-on | 前置依赖: [Lab 4](./lab-04-state-management.md) | 预计时间: 75分钟 | 形式化等级: L4

## 实验目标

- [x] 理解 Checkpoint 的工作原理
- [x] 掌握 Checkpoint 配置与调优
- [x] 学会从 Checkpoint/Savepoint 恢复作业
- [x] 理解 Exactly-Once 语义实现

## 前置知识

- Lab 4 的状态管理
- 分布式一致性基础
- Flink 状态后端

## Checkpoint 机制概览

```
Checkpoint = 一致性快照 = 所有算子状态 + 数据源偏移量
```

### Checkpoint 流程

1. **触发**: JobManager 协调器触发 Checkpoint
2. **同步阶段**: 算子执行快照（停止处理，记录状态）
3. **异步阶段**: 状态异步写入存储
4. **确认**: TaskManager 确认 Checkpoint 完成
5. **完成**: JobManager 通知所有算子 Checkpoint 完成

## 实验步骤

### 步骤 1: 配置 Checkpoint

```java
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.api.environment.CheckpointConfig;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;


public class CheckpointExample {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // 启用 Checkpoint，每10秒触发一次
        env.enableCheckpointing(10000);

        // Checkpoint 模式
        env.getCheckpointConfig().setCheckpointingMode(
            CheckpointingMode.EXACTLY_ONCE  // 或 AT_LEAST_ONCE
        );

        // Checkpoint 超时
        env.getCheckpointConfig().setCheckpointTimeout(60000);

        // 同时进行的 Checkpoint 数量
        env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);

        // 两个 Checkpoint 之间的最小间隔
        env.getCheckpointConfig().setMinPauseBetweenCheckpoints(5000);

        // 外部化 Checkpoint（作业取消后保留）
        env.getCheckpointConfig().setExternalizedCheckpointCleanup(
            CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION
        );

        // 允许失败的 Checkpoint 次数
        env.getCheckpointConfig().setTolerableCheckpointFailureNumber(3);

        // 配置状态后端
        env.setStateBackend(new RocksDBStateBackend("hdfs://namenode:8020/flink/checkpoints"));

        // ... 定义数据流处理逻辑

        env.execute("Checkpoint Example");
    }
}
```

### 步骤 2: 状态后端配置

```java
import org.apache.flink.contrib.streaming.state.RocksDBStateBackend;
import org.apache.flink.runtime.state.filesystem.FsStateBackend;
import org.apache.flink.runtime.state.memory.MemoryStateBackend;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;


public class StateBackendConfig {

    public static void configureStateBackend(StreamExecutionEnvironment env, String type) {
        switch (type) {
            case "memory":
                // 内存状态后端（仅测试）
                env.setStateBackend(new HashMapStateBackend()  // MemoryStateBackend已弃用，使用HashMapStateBackend
// 
                    5242880,  // 最大状态大小 5MB
                    true       // 异步快照
                ));
                break;

            case "filesystem":
                // 文件系统状态后端
                env.setStateBackend(new FsStateBackend(
                    "file:///tmp/flink-checkpoints",
                    true  // 异步快照
                ));
                break;

            case "rocksdb":
                // RocksDB 状态后端（推荐生产环境）
                env.setStateBackend(new RocksDBStateBackend(
                    "hdfs://namenode:8020/flink/checkpoints",
                    true  // 增量 Checkpoint
                ));

                // RocksDB 调优
                RocksDBStateBackend rocksDbBackend =
                    (RocksDBStateBackend) env.getStateBackend();
                break;
        }
    }
}
```

### 步骤 3: 增量 Checkpoint

```java
// Flink 1.11+ 增量 Checkpoint 配置
env.setStateBackend(new RocksDBStateBackend(
    checkpointPath,
    true  // 启用增量 Checkpoint
));

// 配置增量 Checkpoint 参数
env.getCheckpointConfig().setPreferCheckpointForRecovery(true);

// 清理旧的 Checkpoint
env.getCheckpointConfig().enableUnalignedCheckpoints();
```

### 步骤 4: 从 Checkpoint 恢复作业

```bash
# 列出可用的 Checkpoint
ls -la /tmp/flink-checkpoints/<job-id>/

# 从特定 Checkpoint 恢复
flink run -s /tmp/flink-checkpoints/<job-id>/chk-123 \
    -c com.example.MyJob \
    my-job.jar

# 从最新的 Checkpoint 恢复
flink run -s /tmp/flink-checkpoints/<job-id>/ \
    -c com.example.MyJob \
    my-job.jar
```

### 步骤 5: Savepoint 操作

```bash
# 触发 Savepoint
flink savepoint <job-id> hdfs://namenode:8020/flink/savepoints

# 触发 Savepoint 并取消作业
flink stop --savepointPath hdfs://namenode:8020/flink/savepoints <job-id>

# 从 Savepoint 恢复
flink run -s hdfs://namenode:8020/flink/savepoints/savepoint-123 \
    -c com.example.MyJob \
    my-job.jar

# 从 Savepoint 恢复但跳过无法映射的状态
flink run -s hdfs://namenode:8020/flink/savepoints/savepoint-123 \
    --allowNonRestoredState \
    -c com.example.MyJob \
    my-job.jar
```

### 步骤 6: 程序中触发 Savepoint

```java
// 通过 REST API 触发 Savepoint
public class SavepointTrigger {

    public String triggerSavepoint(String jobManagerUrl, String jobId)
            throws Exception {

        String url = String.format("%s/jobs/%s/savepoints", jobManagerUrl, jobId);

        String json = "{"
            + "'cancel-job': false,"
            + "'target-directory': 'hdfs://namenode:8020/flink/savepoints'"
            + "}";

        // 发送 POST 请求
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(json))
            .build();

        HttpClient client = HttpClient.newHttpClient();
        HttpResponse<String> response = client.send(request,
            HttpResponse.BodyHandlers.ofString());

        return response.body();
    }
}
```

## 验证方法

### 检查清单

- [ ] Checkpoint 成功触发并保存
- [ ] 能够从 Checkpoint 恢复作业状态
- [ ] 增量 Checkpoint 减少存储占用
- [ ] 理解 Exactly-Once 保证机制
- [ ] 掌握 Savepoint 用于升级部署

### 监控 Checkpoint

通过 Flink Web UI (<http://localhost:8081>) 查看：

- Checkpoint 历史
- 每次 Checkpoint 的时长
- 状态大小
- 失败原因

### 测试恢复

```java

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

@Test
public void testCheckpointAndRestore() throws Exception {
    // 1. 启动作业
    StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
    env.enableCheckpointing(1000);
    // ... 配置作业
    JobClient jobClient = env.executeAsync();

    // 2. 等待一些数据处理后触发 Savepoint
    Thread.sleep(5000);
    String savepointPath = cluster.triggerSavepoint(
        jobClient.getJobID(),
        false
    ).get();

    // 3. 取消作业
    jobClient.cancel().get();

    // 4. 从 Savepoint 恢复
    StreamExecutionEnvironment newEnv =
        StreamExecutionEnvironment.getExecutionEnvironment();
    // ... 配置相同作业
    newEnv.setDefaultSavepointDirectory(savepointPath);
    JobClient restoredJob = newEnv.executeAsync();

    // 5. 验证状态恢复正确
    // ...
}
```

## 扩展练习

### 练习 1: 自定义 Checkpoint 监听器

```java
public class CheckpointMonitor implements CheckpointListener {

    private final MetricReporter reporter;

    @Override
    public void notifyCheckpointComplete(long checkpointId) {
        reporter.reportMetric("checkpoint.success", 1);
        System.out.println("Checkpoint " + checkpointId + " completed");
    }

    @Override
    public void notifyCheckpointAborted(long checkpointId) {
        reporter.reportMetric("checkpoint.failure", 1);
        System.err.println("Checkpoint " + checkpointId + " aborted");
    }
}

// 在算子中使用
public class MonitoredFunction extends RichFunction
    implements CheckpointListener {
    // ...
}
```

### 练习 2: 实现端到端 Exactly-Once

```java
// Kafka Source 的 Exactly-Once 配置
FlinkKafkaConsumer<String> kafkaSource = new FlinkKafkaConsumer<>(
    "topic",
    new SimpleStringSchema(),
    properties
);

// 启用 Checkpoint 提交 Offset
kafkaSource.setCommitOffsetsOnCheckpoints(true);

// Kafka Sink 的 Exactly-Once 配置
FlinkKafkaProducer<String> kafkaSink = new FlinkKafkaProducer<>(
    "output-topic",
    new SimpleStringSchema(),
    properties,
    FlinkKafkaProducer.Semantic.EXACTLY_ONCE  // 启用事务
);

// 事务超时配置（必须大于 Checkpoint 间隔）
properties.setProperty("transaction.timeout.ms", "900000");
```

## 故障排查

### Checkpoint 失败常见原因

| 问题 | 原因 | 解决 |
|------|------|------|
| Checkpoint 超时 | 状态过大，网络慢 | 增加超时时间，启用增量 Checkpoint |
| 状态过大 | 未清理过期状态 | 配置 State TTL |
| 反压导致 | 处理速度慢 | 优化算子性能，增加并行度 |
| 存储失败 | HDFS/S3 连接问题 | 检查存储连接，配置重试 |

### 性能调优

```java
// 大状态优化
env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);
env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30000);

// 异步快照
env.setStateBackend(new RocksDBStateBackend(path, true));

// 未对齐 Checkpoint（低延迟场景）
env.getCheckpointConfig().enableUnalignedCheckpoints();
env.getCheckpointConfig().setAlignmentTimeout(Duration.ofSeconds(30));
```

## 下一步

- [Lab 6: CEP模式匹配](./lab-06-cep.md)
- [Flink Playground 高级练习](../flink-playground/README.md)

## 引用参考
