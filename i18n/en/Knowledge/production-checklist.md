---
title: "[EN] Production Checklist"
translation_status: "ai_translated"
source_file: "Knowledge/production-checklist.md"
source_version: "d5ecfbb9"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.338699"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # Flink 生产环境检查清单 -->

<!-- TRANSLATE: > 所属阶段: Knowledge | 前置依赖: [Flink/02-core/checkpoint-mechanism-deep-dive.md](../Flink/02-core/checkpoint-mechanism-deep-dive.md) | 形式化等级: L3 -->


<!-- TRANSLATE: ## 2. 属性推导 (Properties) -->

<!-- TRANSLATE: ### Lemma-K-Prod-01: 配置正确性蕴含稳定性 -->

<!-- TRANSLATE: **引理**: 若所有 P0 级别配置检查通过，则作业在故障场景下可在 RTO 内恢复。 -->

<!-- TRANSLATE: **推导**： -->

<!-- TRANSLATE: 1. **Checkpoint 配置正确** → 状态可恢复 -->
   - 间隔 $\leq$ RTO/2，确保丢失数据窗口在容忍范围内
   - 超时 $\geq$ 典型持续时间 × 2，避免误报失败

<!-- TRANSLATE: 2. **状态后端配置正确** → 状态可持久化 -->
<!-- TRANSLATE:    - RocksDB 增量 Checkpoint → 减少网络和存储压力 -->
<!-- TRANSLATE:    - 本地恢复启用 → 减少恢复时间 -->

<!-- TRANSLATE: 3. **资源配置正确** → 运行时可预测 -->
   - 托管内存 $\geq$ 预估状态 × 1.5 → 避免 OOM
<!-- TRANSLATE:    - 网络缓冲区充足 → 避免背压级联 -->

<!-- TRANSLATE: ### Lemma-K-Prod-02: 监控完备性 -->

<!-- TRANSLATE: **引理**: 完备的监控覆盖可检测 95% 以上的潜在故障。 -->

<!-- TRANSLATE: **监控三支柱**： -->

<!-- TRANSLATE: | 支柱 | 关键指标 | 检测能力 | -->
<!-- TRANSLATE: |------|----------|----------| -->
<!-- TRANSLATE: | 指标 (Metrics) | Checkpoint 时间/大小/失败率 | 性能退化、资源瓶颈 | -->
<!-- TRANSLATE: | 日志 (Logging) | 异常堆栈、业务错误 | 逻辑错误、外部故障 | -->
<!-- TRANSLATE: | 追踪 (Tracing) | 端到端延迟、调用链 | 延迟来源、依赖故障 | -->


<!-- TRANSLATE: ## 4. 论证过程 (Argumentation) -->

<!-- TRANSLATE: ### 4.1 检查优先级论证 -->

<!-- TRANSLATE: **P0 - 阻塞性（必须修复）**： -->

<!-- TRANSLATE: - 数据丢失风险 -->
<!-- TRANSLATE: - 系统崩溃风险 -->
<!-- TRANSLATE: - 安全漏洞 -->

<!-- TRANSLATE: **P1 - 严重（必须计划修复）**： -->

<!-- TRANSLATE: - 性能显著下降 -->
<!-- TRANSLATE: - 恢复时间过长 -->
<!-- TRANSLATE: - 监控盲区 -->

<!-- TRANSLATE: **P2 - 建议（优化改进）**： -->

<!-- TRANSLATE: - 配置优化空间 -->
<!-- TRANSLATE: - 可观测性增强 -->
<!-- TRANSLATE: - 成本优化 -->

<!-- TRANSLATE: ### 4.2 检查频率论证 -->

<!-- TRANSLATE: | 检查类型 | 频率 | 负责人 | -->
<!-- TRANSLATE: |----------|------|--------| -->
<!-- TRANSLATE: | 上线前检查 | 每次发布前 | 开发人员 | -->
<!-- TRANSLATE: | 定期检查 | 每周 | SRE | -->
<!-- TRANSLATE: | 深度审计 | 每季度 | 架构师 | -->
<!-- TRANSLATE: | 紧急检查 | 故障后 | 值班人员 | -->


<!-- TRANSLATE: ## 6. 实例验证 (Examples) -->

<!-- TRANSLATE: ### 6.1 完整上线检查清单 -->

```yaml
# Flink 生产检查清单
job_name: "user-behavior-analytics"
version: "1.0.0"
check_date: "2026-04-04"

# ========== P0 阻塞性检查 ==========
p0_checks:
  checkpoint:
    - item: "Checkpoint 已启用"
      status: PASS
      value: "state.checkpoint-storage: filesystem"

    - item: "Checkpoint 间隔合理"
      status: PASS
      value: "execution.checkpointing.interval: 300s"

    - item: "状态后端配置"
      status: PASS
      value: "state.backend: rocksdb"

  resources:
    - item: "并行度设置"
      status: PASS
      value: "parallelism.default: 12"

    - item: "内存配置"
      status: PASS
      value: "taskmanager.memory.process.size: 8gb"

  security:
    - item: "认证启用"
      status: PASS
      value: "security.ssl.internal.enabled: true"

# ========== P1 严重性检查 ==========
p1_checks:
  monitoring:
    - item: "指标上报配置"
      status: PASS
      value: "metrics.reporters: prometheus"

    - item: "日志级别"
      status: PASS
      value: "log4j.rootLogger: INFO"

  watermark:
    - item: "Watermark 策略"
      status: PASS
      value: "forBoundedOutOfOrderness(Duration.ofSeconds(30))"

# ========== P2 建议性检查 ==========
p2_checks:
  optimization:
    - item: "对象重用"
      status: WARN
      value: "pipeline.object-reuse: false (建议启用)"

    - item: "异步快照"
      status: PASS
      value: "state.backend.incremental: true"
```

<!-- TRANSLATE: ### 6.2 自动化检查脚本 -->

```python
#!/usr/bin/env python3
"""Flink 生产检查脚本"""

import json
import sys
from typing import Dict, List, Tuple

class FlinkProductionChecker:
    def __init__(self, config: Dict):
        self.config = config
        self.results = []

    def check_checkpoint(self) -> List[Tuple[str, str, str]]:
        """检查 Checkpoint 配置"""
        checks = []

        # P0: Checkpoint 必须启用
        checkpointing = self.config.get('execution.checkpointing.enabled', True)
        checks.append(('P0', 'Checkpoint 已启用', 'PASS' if checkpointing else 'FAIL'))

        # P0: 间隔必须设置
        interval = self.config.get('execution.checkpointing.interval')
        if interval and interval <= 300000:  # 5分钟
            checks.append(('P0', 'Checkpoint 间隔 ≤ 5分钟', 'PASS'))
        else:
            checks.append(('P0', 'Checkpoint 间隔 ≤ 5分钟', 'FAIL'))

        # P1: 超时设置
        timeout = self.config.get('execution.checkpointing.timeout')
        if timeout and timeout >= 600000:  # 10分钟
            checks.append(('P1', 'Checkpoint 超时 ≥ 10分钟', 'PASS'))
        else:
            checks.append(('P1', 'Checkpoint 超时 ≥ 10分钟', 'WARN'))

        return checks

    def check_state_backend(self) -> List[Tuple[str, str, str]]:
        """检查状态后端配置"""
        checks = []

        backend = self.config.get('state.backend')
        if backend == 'rocksdb':
            checks.append(('P0', '状态后端使用 RocksDB', 'PASS'))

            # 检查增量 Checkpoint
            incremental = self.config.get('state.backend.incremental', False)
            checks.append(('P2', 'RocksDB 增量 Checkpoint',
                          'PASS' if incremental else 'WARN'))
        else:
            checks.append(('P0', '状态后端使用 RocksDB', 'WARN'))

        return checks

    def check_resources(self) -> List[Tuple[str, str, str]]:
        """检查资源配置"""
        checks = []

        tm_memory = self.config.get('taskmanager.memory.process.size', '1gb')
        # 解析内存大小
        memory_gb = self._parse_memory(tm_memory)
        if memory_gb >= 4:
            checks.append(('P0', 'TaskManager 内存 ≥ 4GB', 'PASS'))
        else:
            checks.append(('P0', 'TaskManager 内存 ≥ 4GB', 'FAIL'))

        parallelism = self.config.get('parallelism.default', 1)
        if parallelism >= 1:
            checks.append(('P1', '并行度已设置', 'PASS'))
        else:
            checks.append(('P1', '并行度已设置', 'FAIL'))

        return checks

    def _parse_memory(self, memory_str: str) -> float:
        """解析内存字符串为 GB"""
        value = float(memory_str[:-2])
        unit = memory_str[-2:].lower()
        if unit == 'gb':
            return value
        elif unit == 'mb':
            return value / 1024
        elif unit == 'tb':
            return value * 1024
        return value

    def run_all_checks(self) -> Dict:
        """运行所有检查"""
        all_checks = []
        all_checks.extend(self.check_checkpoint())
        all_checks.extend(self.check_state_backend())
        all_checks.extend(self.check_resources())

        # 统计结果
        p0_pass = sum(1 for p, _, r in all_checks if p == 'P0' and r == 'PASS')
        p0_total = sum(1 for p, _, _ in all_checks if p == 'P0')

        return {
            'checks': all_checks,
            'summary': {
                'p0_pass_rate': f"{p0_pass}/{p0_total}",
                'production_ready': p0_pass == p0_total
            }
        }

if __name__ == '__main__':
    # 示例配置
    config = {
        'execution.checkpointing.enabled': True,
        'execution.checkpointing.interval': 300000,
        'execution.checkpointing.timeout': 600000,
        'state.backend': 'rocksdb',
        'state.backend.incremental': True,
        'taskmanager.memory.process.size': '8gb',
        'parallelism.default': 12
    }

    checker = FlinkProductionChecker(config)
    result = checker.run_all_checks()

    print(json.dumps(result, indent=2))

    if not result['summary']['production_ready']:
        sys.exit(1)
```

<!-- TRANSLATE: ### 6.3 配置模板库 -->

```properties
# ===== 生产环境推荐配置 =====

# --- Checkpoint 配置 ---
execution.checkpointing.interval: 300s
execution.checkpointing.timeout: 600s
execution.checkpointing.min-pause: 300s
execution.checkpointing.max-concurrent-checkpoints: 1
execution.checkpointing.externalized-checkpoint-retention: RETAIN_ON_CANCELLATION

# --- 状态后端配置 ---
state.backend: rocksdb
state.backend.incremental: true
state.backend.rocksdb.memory.fixed-per-slot: 256mb
state.backend.rocksdb.predefined-options: FLASH_SSD_OPTIMIZED

# --- 内存配置 ---
taskmanager.memory.process.size: 8gb
taskmanager.memory.flink.size: 6gb
taskmanager.memory.managed.size: 2gb

# --- 网络配置 ---
taskmanager.memory.network.max: 256mb
taskmanager.numberOfTaskSlots: 4

# --- 高可用配置 ---
high-availability: zookeeper
high-availability.storageDir: hdfs:///flink/ha
high-availability.zookeeper.quorum: zk1:2181,zk2:2181,zk3:2181

# --- 监控配置 ---
metrics.reporters: prometheus
metrics.reporter.prometheus.port: 9249
metrics.reporter.prometheus.filter.includes: "*checkpoint*,*records*,*latency*"
```


<!-- TRANSLATE: ## 8. 引用参考 (References) -->

