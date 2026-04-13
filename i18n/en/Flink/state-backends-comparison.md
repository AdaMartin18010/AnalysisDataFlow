---
title: "[EN] State Backends Comparison"
translation_status: "ai_translated"
source_file: "Flink/state-backends-comparison.md"
source_version: "69f844ec"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.364953"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # Flink State Backends 深度对比 -->

<!-- TRANSLATE: > 所属阶段: Flink | 前置依赖: [checkpoint-mechanism-deep-dive.md](../../../Flink/02-core/checkpoint-mechanism-deep-dive.md) | 形式化等级: L4 -->


<!-- TRANSLATE: ## 2. 属性推导 (Properties) -->

<!-- TRANSLATE: ### Lemma-F-Backend-01: 状态大小边界 -->

<!-- TRANSLATE: **引理**: 各状态后端支持的最大状态规模： -->

<!-- TRANSLATE: | 状态后端 | 最大状态规模 | 限制因素 | -->
<!-- TRANSLATE: |---------|-------------|----------| -->
<!-- TRANSLATE: | HashMapStateBackend | 几十 MB ~ 几百 MB | JVM 堆大小，GC 压力 | -->
<!-- TRANSLATE: | RocksDBStateBackend | 几十 GB ~ 几百 GB | 磁盘空间，内存/磁盘比 | -->
<!-- TRANSLATE: | ForStStateBackend | 理论上无上限 | 远程存储容量 | -->

<!-- TRANSLATE: ### Lemma-F-Backend-02: 访问延迟层次 -->

<!-- TRANSLATE: **引理**: 状态访问延迟满足以下关系： -->

$$
<!-- TRANSLATE: L_{HashMap} \ll L_{RocksDB\_memory} < L_{RocksDB\_disk} \ll L_{ForSt\_remote} -->
$$

<!-- TRANSLATE: **近似数量级**： -->

<!-- TRANSLATE: | 后端 | 命中场景 | 延迟量级 | -->
<!-- TRANSLATE: |------|----------|----------| -->
<!-- TRANSLATE: | HashMap | 内存 | ~100 ns | -->
<!-- TRANSLATE: | RocksDB (MemTable) | 内存 | ~1 μs | -->
<!-- TRANSLATE: | RocksDB (SST L0) | SSD | ~100 μs | -->
<!-- TRANSLATE: | RocksDB (SST L3+) | SSD | ~1 ms | -->
<!-- TRANSLATE: | ForSt | 网络 | ~10 ms | -->

<!-- TRANSLATE: ### Prop-F-Backend-01: Checkpoint 规模关系 -->

<!-- TRANSLATE: **命题**: Checkpoint 大小与状态后端的关系： -->

$$
<!-- TRANSLATE: \text{Checkpoint}_{HashMap} = |S_{total}| -->
$$

$$
<!-- TRANSLATE: \text{Checkpoint}_{RocksDB\_full} = |S_{total}| -->
$$

$$
<!-- TRANSLATE: \text{Checkpoint}_{RocksDB\_incremental} = |\Delta S| \ll |S_{total}| -->
$$


<!-- TRANSLATE: ## 4. 论证过程 (Argumentation) -->

<!-- TRANSLATE: ### 4.1 状态后端选择决策树 -->

```
状态大小估计?
├── < 100MB
│   └── 是否要求极速访问?
│       ├── 是 → HashMapStateBackend
│       └── 否 → HashMapStateBackend (默认)
├── 100MB ~ 10GB
│   └── 是否有大窗口/大 Key State?
│       ├── 是 → RocksDBStateBackend (增量Checkpoint)
│       └── 否 → RocksDBStateBackend
└── > 10GB
    └── 是否需要存算分离?
        ├── 是 → ForStStateBackend (Flink 2.0+)
        └── 否 → RocksDBStateBackend (优化配置)
```

<!-- TRANSLATE: ### 4.2 性能调优策略对比 -->

<!-- TRANSLATE: | 优化目标 | HashMap | RocksDB | ForSt | -->
<!-- TRANSLATE: |---------|---------|---------|-------| -->
<!-- TRANSLATE: | 减少 GC | 减少状态大小 | 无需优化 | 无需优化 | -->
<!-- TRANSLATE: | 降低延迟 | 预分配内存 | 增大 Block Cache | 优化网络 | -->
<!-- TRANSLATE: | 提高吞吐 | 并行度 | 批量读写 | 异步 Pipeline | -->
<!-- TRANSLATE: | 减少 Checkpoint 时间 | 状态小 | 启用增量 | 无需 Checkpoint | -->


<!-- TRANSLATE: ## 6. 实例验证 (Examples) -->

<!-- TRANSLATE: ### 6.1 配置示例 -->

```java
import org.apache.flink.runtime.state.hashmap.HashMapStateBackend;
import org.apache.flink.runtime.state.rocksdb.EmbeddedRocksDBStateBackend;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// ========== HashMapStateBackend ==========
// 适合：小状态，低延迟场景
env.setStateBackend(new HashMapStateBackend());
env.getCheckpointConfig().setCheckpointStorage("hdfs://namenode:8020/flink/checkpoints");

// ========== RocksDB State Backend ==========
// 适合：大状态，大窗口场景
EmbeddedRocksDBStateBackend rocksDbBackend = new EmbeddedRocksDBStateBackend(true); // 增量
env.setStateBackend(rocksDbBackend);
env.getCheckpointConfig().setCheckpointStorage("hdfs://namenode:8020/flink/checkpoints");

// RocksDB 高级配置
DefaultConfigurableStateBackend configurableBackend =
    new EmbeddedRocksDBStateBackend(true);
configurableBackend.setPredefinedOptions(PredefinedOptions.FLASH_SSD_OPTIMIZED);
env.setStateBackend(configurableBackend);

// ========== ForSt State Backend (Flink 2.0+) ==========
// 适合：超大规模状态，存算分离
ForStStateBackend forstBackend = new ForStStateBackend();
forstBackend.setRemoteStorageUri("s3://flink-state-bucket/");
env.setStateBackend(forstBackend);
```

<!-- TRANSLATE: ### 6.2 配置文件示例 -->

```yaml
# flink-conf.yaml

# --- HashMapStateBackend 配置 ---
state.backend: hashmap
state.checkpoint-storage: filesystem
state.checkpoints.dir: hdfs://namenode:8020/flink/checkpoints

# --- RocksDBStateBackend 配置 ---
state.backend: rocksdb
state.backend.incremental: true
state.backend.rocksdb.memory.fixed-per-slot: 256mb
state.backend.rocksdb.predefined-options: FLASH_SSD_OPTIMIZED

# RocksDB 调优参数
state.backend.rocksdb.threads.threads-number: 4
state.backend.rocksdb.timer-service.factory: ROCKSDB

# --- ForSt State Backend 配置 (Flink 2.0+) ---
state.backend: forst
state.backend.forst.remote.uri: s3://my-flink-state/
state.backend.forst.local.dir: /tmp/flink-forst
```

<!-- TRANSLATE: ### 6.3 状态监控代码 -->

```java
// 获取状态后端指标
public void monitorStateBackend(RuntimeContext ctx) {
    // 状态大小
    long stateSize = ctx.getStateSize();

    // 对于 RocksDB，获取详细指标
    if (stateBackend instanceof RocksDBStateBackend) {
        // SST 文件数量
        int sstFileCount = getMetric("rocksdb.num-files-at-level0")
                         + getMetric("rocksdb.num-files-at-level1")
                         + getMetric("rocksdb.num-files-at-level2");

        // Block Cache 命中率
        double cacheHitRate = getMetric("rocksdb.block.cache.hit.rate");

        // 写入放大
        double writeAmplification = getMetric("rocksdb.write.amplification");

        // 输出日志
        LOG.info("RocksDB Metrics - SST Files: {}, Cache Hit: {:.2f}%, Write Amp: {:.2f}",
            sstFileCount, cacheHitRate * 100, writeAmplification);
    }
}
```

<!-- TRANSLATE: ### 6.4 状态迁移脚本 -->

```python
#!/usr/bin/env python3
"""状态后端迁移检查脚本"""

import json

def analyze_state_usage(checkpoint_path):
    """分析 Checkpoint 状态大小，推荐状态后端"""

    # 模拟读取 Checkpoint 元数据
    checkpoint_meta = {
        "state_size_bytes": 536870912,  # 512 MB
        "state_files": 150,
        "max_key_state_size": 10485760,  # 10 MB
        "checkpoint_duration_ms": 30000
    }

    size_mb = checkpoint_meta["state_size_bytes"] / (1024 * 1024)

    recommendation = {
        "current_size_mb": size_mb,
        "recommendation": None,
        "reasoning": []
    }

    if size_mb < 100:
        recommendation["recommendation"] = "HashMapStateBackend"
        recommendation["reasoning"].append("状态小于 100MB，适合内存存储")
        recommendation["reasoning"].append("可获得最低访问延迟")
    elif size_mb < 5120:  # 5GB
        recommendation["recommendation"] = "RocksDBStateBackend (Incremental)"
        recommendation["reasoning"].append("状态较大，需要磁盘存储")
        recommendation["reasoning"].append("启用增量 Checkpoint 减少网络传输")
        recommendation["reasoning"].append("适合大窗口聚合场景")
    else:
        recommendation["recommendation"] = "ForStStateBackend (Flink 2.0+)"
        recommendation["reasoning"].append("状态超过 5GB，考虑存算分离")
        recommendation["reasoning"].append("避免本地磁盘瓶颈")
        recommendation["reasoning"].append("支持超大规模状态")

    # 额外建议
    if checkpoint_meta["checkpoint_duration_ms"] > 60000:
        recommendation["reasoning"].append(
            "⚠️ Checkpoint 时间过长，考虑启用增量 Checkpoint 或优化状态访问模式"
        )

    return recommendation

if __name__ == "__main__":
    result = analyze_state_usage("hdfs://checkpoints/job-123")
    print(json.dumps(result, indent=2, ensure_ascii=False))
```


<!-- TRANSLATE: ## 8. 引用参考 (References) -->
