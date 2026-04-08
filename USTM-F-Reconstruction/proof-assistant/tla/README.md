# USTM-F TLA+ 形式化验证

## 项目概述

本项目包含Flink核心协议的TLA+形式化规约和模型检验，是USTM-F（统一流理论模型-形式化）项目的重要组成部分。

## 目录结构

```
tla/
├── README.md                      # 本文件
├── models/                        # 模型检验配置文件
│   ├── CheckpointMC.tla          # CheckpointCoordinator模型实例
│   ├── CheckpointMC.cfg          # CheckpointCoordinator TLC配置
│   ├── ExactlyOnceMC.tla         # ExactlyOnce模型实例
│   └── ExactlyOnceMC.cfg         # ExactlyOnce TLC配置
├── protocols/                     # 协议规约
│   ├── CheckpointCoordinator.tla # 检查点协调协议
│   ├── ExactlyOnce.tla           # 两阶段提交/精确一次语义
│   ├── WatermarkProgress.tla     # Watermark进展性
│   └── StateConsistency.tla      # 状态一致性
└── utils/
    └── USTMUtils.tla             # 通用工具定义
```

## 协议规约说明

### 1. CheckpointCoordinator.tla
**检查点协调协议** - 基于Chandy-Lamport算法的Flink分布式快照机制

- **核心变量**: coordinatorState, taskStates, triggerChannel, ackChannel
- **关键属性**:
  - `CheckpointEventuallyCompletes`: 检查点最终完成
  - `CompletedCheckpointsHaveAllAcks`: 完成的检查点收到所有确认
  - `GlobalConsistency`: 全局一致性快照
  - `MutualExclusion`: 检查点互斥执行

### 2. ExactlyOnce.tla
**两阶段提交协议** - 实现端到端精确一次处理语义

- **核心变量**: coordState, participantState, voteChannel, decisionChannel
- **关键属性**:
  - `Atomicity`: 事务原子性
  - `MutualExclusion`: 提交/中止互斥
  - `ExactlyOnce`: 精确一次输出
  - `EventuallyDecides`: 事务最终决策

### 3. WatermarkProgress.tla
**Watermark进展性** - 事件时间处理的时间语义保证

- **核心变量**: sourceWatermarks, taskOutputWatermarks, globalWatermark
- **关键属性**:
  - `GlobalMonotonicity`: Watermark单调不减
  - `WatermarkProgress`: Watermark最终推进
  - `EventTimeIntegrity`: 事件时间完整性
  - `CorrectEventProcessing`: 正确的事件处理

### 4. StateConsistency.tla
**状态一致性** - 有状态算子的状态访问保证

- **核心变量**: currentState, stateVersions, checkpointSnapshots
- **关键属性**:
  - `ReadYourWrites`: 写前读一致性
  - `MonotonicReads`: 单调读
  - `WriteAtomicity`: 写入原子性
  - `RecoveryConsistency`: 恢复一致性

## 使用说明

### 环境要求
- [TLA+ Toolbox](https://lamport.azurewebsites.net/tla/toolbox.html) 或
- [TLC Model Checker](https://github.com/tlaplus/tlaplus) 命令行工具

### 运行模型检验

#### 使用TLA+ Toolbox
1. 打开TLA+ Toolbox
2. 导入项目根目录
3. 打开 `models/CheckpointMC.tla` 或 `models/ExactlyOnceMC.tla`
4. 创建新的Model，加载对应的 `.cfg` 配置文件
5. 运行TLC模型检验器

#### 使用命令行TLC
```bash
# 检验CheckpointCoordinator
cd proof-assistant/tla/models
tlc CheckpointMC.tla -config CheckpointMC.cfg

# 检验ExactlyOnce
tlc ExactlyOnceMC.tla -config ExactlyOnceMC.cfg
```

### 模型检验参数说明
- `Tasks`: 任务节点集合（模型实例中限制为3个）
- `MaxCheckpointId`: 最大检查点ID（通常设为2）
- `TimeoutPeriod`: 超时周期（控制状态空间）
- `Participants`: 2PC参与者集合
- `Transactions`: 事务ID集合

## 验证结果

### CheckpointCoordinator验证
| 属性 | 类型 | 结果 |
|------|------|------|
| TypeInvariant | 不变式 | ✅ 通过 |
| MC_Completeness | 活性 | ✅ 通过 |
| MC_NoDeadlock | 无死锁 | ✅ 通过 |
| CheckpointMonotonicity | 单调性 | ✅ 通过 |
| AckConsistency | 一致性 | ✅ 通过 |

### ExactlyOnce验证
| 属性 | 类型 | 结果 |
|------|------|------|
| TypeInvariant | 不变式 | ✅ 通过 |
| MC_Atomicity | 原子性 | ✅ 通过 |
| MC_EventuallyCommits | 活性 | ✅ 通过 |
| MutualExclusion | 互斥性 | ✅ 通过 |

## 形式化属性说明

### 安全属性 (Safety)
- **TypeInvariant**: 所有变量保持正确类型
- **AckConsistency**: 确认的一致性
- **MutualExclusion**: 互斥性保证
- **Atomicity**: 事务原子性

### 活性属性 (Liveness)
- **CheckpointEventuallyCompletes**: 检查点最终完成
- **EventuallyDecides**: 事务最终决策
- **EventualRecovery**: 最终恢复
- **WatermarkProgress**: Watermark进展

## 参考资料

- Leslie Lamport, "Specifying Systems", 2002
- Chandy & Lamport, "Distributed Snapshots", ACM TCS, 1985
- Flink Documentation: Checkpointing & Exactly-Once Semantics
- USTM-F Reconstruction Project Documentation

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-04-08 | 初始版本，4个核心协议规约 |
| 2.0.0 | 2026-04-08 | 完善Checkpoint和ExactlyOnce规约 |

---

**USTM-F Formal Verification Team**  
*Unified Streaming Theory Model - Formal Verification*
