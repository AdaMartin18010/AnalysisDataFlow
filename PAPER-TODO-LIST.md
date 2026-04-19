# Paper TODO List - 学术前沿内容补充计划

> **创建日期**: 2026-04-12
> **状态**: ✅ 100% 完成 (2026-04-15) | 46/46 任务全部交付
> **关联文档**: [ACADEMIC-FRONTIER-GAP-ANALYSIS.md](./archive/academic-reports/ACADEMIC-FRONTIER-GAP-ANALYSIS.md)
> **适用范围**: AnalysisDataFlow项目 v3.9+

---

## 优先级说明

- **🔴 高优先级**: 项目急需补充的内容，缺失会导致知识库不完整
- **🟡 中优先级**: 建议补充的内容，可提升知识库深度
- **🟢 低优先级**: 可选补充的内容，作为未来扩展方向

---

## 🔴 高优先级

### 1. 特征存储系统 (Feature Store)

**背景**: 根据ACADEMIC-FRONTIER-GAP-ANALYSIS分析，项目完全缺乏特征存储相关内容，而这是实时ML的关键基础设施。

**待补充内容**:

| # | 任务项 | 参考论文 | 目标文档位置 |
|---|--------|----------|--------------|
| 1.1 | 特征存储的架构设计与形式化定义 | OpenMLDB (SIGMOD 2025), Feast | `Knowledge/feature-store-architecture.md` |
| 1.2 | 训练-推理一致性保证机制 | FEBench (VLDB 2023) | `Struct/consistency-training-inference.md` |
| 1.3 | 实时特征计算与流处理的集成 | OpenMLDB, PECJ (SIGMOD 2024) | `Knowledge/stream-feature-computation.md` |
| 1.4 | 特征血缘追踪与版本管理 | Tecton白皮书 | `Knowledge/feature-lineage-tracking.md` |
| 1.5 | 特征存储与Flink的集成实践 | 阿里巴巴实践 | `Flink/flink-feature-store-integration.md` |

**预期产出**: 5篇核心文档，填补项目在此领域的空白

---

### 2. 硬件加速流处理

**背景**: SIGMOD 2026预印论文"Accelerating Stream Processing Engines via Hardware Offloading"直接相关，需及时跟进。

**待补充内容**:

| # | 任务项 | 参考论文 | 目标文档位置 |
|---|--------|----------|--------------|
| 2.1 | 流处理硬件加速综述 | Hardware Offloading (SIGMOD 2026) | `Knowledge/hardware-accelerated-streaming.md` |
| 2.2 | FPGA在流处理中的应用 | Falcon (PVLDB 2025) | `Flink/flink-fpga-acceleration.md` |
| 2.3 | GPU加速流连接算法 | EDBT 2024 Benchmark | `Knowledge/gpu-stream-join.md` |
| 2.4 | DPU/SmartNIC在流处理中的角色 | OSDI 2025相关工作 | `Knowledge/dpu-stream-processing.md` |
| 2.5 | 硬件卸载决策的形式化模型 | ADAMANT (BTW 2025) | `Struct/hardware-offload-decision.md` |

**预期产出**: 5篇技术文档，建立硬件加速流处理的理论体系

---

### 3. 事务流处理形式化

**背景**: 根据VLDB Journal 2024综述，事务流处理是重要研究方向，项目缺乏相关形式化内容。

**待补充内容**:

| # | 任务项 | 参考论文 | 目标文档位置 |
|---|--------|----------|--------------|
| 3.1 | 事务语义与流语义的统一形式化 | Zhang et al. (VLDBJ 2024) | `Struct/transactional-stream-semantics.md` |
| 3.2 | ACID在流处理中的实现分析 | VLDB 2024综述 | `Knowledge/acid-in-stream-processing.md` |
| 3.3 | 有界陈旧性的形式化定义 | Skybridge (OSDI 2025) | `Struct/bounded-staleness.md` |
| 3.4 | 推测式排序与流处理 | SpecLog (OSDI 2025) | `Struct/speculative-stream-ordering.md` |

**预期产出**: 4篇形式化文档，完善事务流处理理论

---

### 4. 时序知识图谱流推理

**背景**: 时序知识图谱(TKG)推理是知识图谱与流处理的交叉热点，项目缺乏相关内容。

**待补充内容**:

| # | 任务项 | 参考论文 | 目标文档位置 |
|---|--------|----------|--------------|
| 4.1 | 时序知识图谱的流式更新机制 | StreamE (SIGIR 2025) | `Knowledge/tkg-stream-updates.md` |
| 4.2 | 时间感知的查询推理算法 | EVOREASONER (2025) | `Knowledge/temporal-kg-reasoning.md` |
| 4.3 | LLM与知识图谱结合的流式推理 | Follow the Path (2025) | `Knowledge/llm-kg-stream-reasoning.md` |
| 4.4 | TKG推理的在线学习理论 | INFER (ICLR 2025) | `Struct/online-tkg-learning.md` |

**预期产出**: 4篇文档，覆盖TKG流推理核心内容

---

## 🟡 中优先级

### 5. LLM4DB / AI4DB 集成

**背景**: LLM与数据库/流处理的集成是新兴热点，值得系统性分析。

**待补充内容**:

| # | 任务项 | 参考论文 | 目标文档位置 |
|---|--------|----------|--------------|
| 5.1 | LLM辅助流处理配置调优 | GPTuner (VLDB 2024), ZERO-TUNE (ICDE 2024) | `Knowledge/llm-stream-tuning.md` |
| 5.2 | LLM增强的查询重写与优化 | LLM-R2 (PVLDB 2025) | `Knowledge/llm-query-rewrite.md` |
| 5.3 | 数据库诊断系统的LLM应用 | D-Bot (VLDB 2024) | `Knowledge/llm-stream-diagnosis.md` |
| 5.4 | 学习型成本模型在流处理中的应用 | Heinrich et al. (PVLDB 2025) | `Struct/learned-cost-models-streaming.md` |
| 5.5 | 自动特征选择的流处理性能建模 | Agnihotri et al. (AIDB 2025) | `Knowledge/automated-feature-selection.md` |

**预期产出**: 5篇文档，建立LLM4Stream的知识体系

---

### 6. 窗口连接优化

**背景**: VLDB 2025论文揭示窗口连接重排序的重要性，需要补充相关理论。

**待补充内容**:

| # | 任务项 | 参考论文 | 目标文档位置 |
|---|--------|----------|--------------|
| 6.1 | 窗口连接的重排序理论 | Ziehn et al. (PVLDB 2025) | `Struct/window-join-reordering.md` |
| 6.2 | 窗口语义对代数性质的影响 | WJR算法论文 | `Struct/window-algebra-properties.md` |
| 6.3 | 乱序数据流的窗口连接优化 | PECJ (SIGMOD 2024) | `Knowledge/disordered-window-join.md` |
| 6.4 | 区间连接的并行化理论 | OpenMLDB相关工作 | `Struct/interval-join-parallelism.md` |

**预期产出**: 4篇文档，完善窗口操作理论

---

### 7. 近似查询处理 (AQP)

**背景**: AQP在流场景下有独特价值，项目缺乏系统性分析。

**待补充内容**:

| # | 任务项 | 参考论文 | 目标文档位置 |
|---|--------|----------|--------------|
| 7.1 | 流场景下AQP的形式化框架 | AQP Survey (SIGMOD 2017) | `Struct/aqp-streaming-formalization.md` |
| 7.2 | 采样、草图、直方图方法的统一理论 | Chaudhuri et al. | `Struct/unified-aqp-theory.md` |
| 7.3 | 误差边界保证机制 | ThalamusDB (PACMMOD 2024) | `Knowledge/aqp-error-bounds.md` |
| 7.4 | 流摘要的增量维护 | Data Triage框架 | `Knowledge/stream-summaries.md` |

**预期产出**: 4篇文档，建立流AQP理论基础

---

### 8. 可靠性与端到端保证

**背景**: 流处理可靠性是工业界关注重点，需要形式化分析。

**待补充内容**:

| # | 任务项 | 参考论文 | 目标文档位置 |
|---|--------|----------|--------------|
| 8.1 | 端到端可靠性的形式化定义 | Mayer et al. (VLDB 2025) | `Struct/end-to-end-reliability.md` |
| 8.2 | 可靠性保证的验证方法 | VLDB 2025论文 | `Knowledge/reliability-verification.md` |
| 8.3 | 与Exactly-Once语义的对比分析 | 对比研究 | `Knowledge/exactly-once-comparison.md` |

**预期产出**: 3篇文档，完善可靠性理论体系

---

## 🟢 低优先级

### 9. 强化学习在流处理中的应用

**背景**: RL在索引、查询优化等领域有应用，可作为扩展方向。

**待补充内容**:

| # | 任务项 | 参考论文 | 目标文档位置 |
|---|--------|----------|--------------|
| 9.1 | 强化学习在流查询优化中的应用 | RankPQO相关 | `Knowledge/rl-query-optimization.md` |
| 9.2 | 轨迹数据索引的RL方法 | BT-Tree (SIGMOD 2025) | `Knowledge/rl-trajectory-indexing.md` |
| 9.3 | TKG推理的RL方法 | ARLIE (TKDE 2026) | `Knowledge/rl-tkg-reasoning.md` |

**预期产出**: 3篇文档，探索RL与流处理的结合

---

### 10. 多模态流数据处理

**背景**: 视频流、多模态数据是新兴应用场景。

**待补充内容**:

| # | 任务项 | 参考论文 | 目标文档位置 |
|---|--------|----------|--------------|
| 10.1 | 视频流复杂事件处理 | DEBS 2025论文 | `Knowledge/video-stream-cep.md` |
| 10.2 | 多模态数据的近似查询 | ThalamusDB | `Knowledge/multimodal-stream-aqp.md` |
| 10.3 | 零样本视频查询 | SketchQL | `Knowledge/zero-shot-video-query.md` |

**预期产出**: 3篇文档，覆盖多模态流处理

---

### 11. 无服务器与流推理

**背景**: Serverless架构下的ML推理是新兴方向。

**待补充内容**:

| # | 任务项 | 参考论文 | 目标文档位置 |
|---|--------|----------|--------------|
| 11.1 | 无服务器LLM推理的形式化 | ServerlessLLM (OSDI 2024) | `Struct/serverless-ml-inference.md` |
| 11.2 | 流式推理的资源调度 | BlitzScale (OSDI 2025) | `Knowledge/stream-inference-scheduling.md` |
| 11.3 | 弹性序列并行与流处理 | LoongServe (SOSP 2024) | `Knowledge/elastic-sequence-parallelism.md` |

**预期产出**: 3篇文档，探索serverless与流处理的结合

---

### 12. 分布式缓存与状态管理

**背景**: 状态管理是流处理核心，可参考分布式缓存最新研究。

**待补充内容**:

| # | 任务项 | 参考论文 | 目标文档位置 |
|---|--------|----------|--------------|
| 12.1 | 有界陈旧性缓存的形式化 | Skybridge (OSDI 2025) | `Struct/bounded-staleness-cache.md` |
| 12.2 | 状态预取的形式化模型 | Keyed Prefetching (2025) | `Struct/state-prefetching.md` |
| 12.3 | 时间感知缓存替换 | 相关工作 | `Knowledge/timestamp-aware-caching.md` |

**预期产出**: 3篇文档，优化状态管理理论

---

## 执行计划

### Phase 1 (2026-Q2): 高优先级任务

```
4月: 任务1.1-1.3 (特征存储基础)
5月: 任务2.1-2.3 (硬件加速基础)
6月: 任务3.1-3.3 (事务流处理形式化)
```

### Phase 2 (2026-Q3): 高优先级收尾 + 中优先级启动

```
7月: 任务1.4-1.5, 4.1-4.2
8月: 任务2.4-2.5, 5.1-5.2
9月: 任务3.4, 4.3-4.4, 5.3-5.5
```

### Phase 3 (2026-Q4): 中优先级完成

```
10月: 任务6.1-6.4 (窗口连接)
11月: 任务7.1-7.4 (AQP)
12月: 任务8.1-8.3 (可靠性)
```

### Phase 4 (2027-Q1+): 低优先级扩展

```
按需执行: 任务9-12
```

---

## 资源需求

| 资源类型 | 数量 | 说明 |
|----------|------|------|
| 论文获取 | ~30篇 | 优先获取高优先级任务相关论文 |
| 算力资源 | GPU小时 | 用于复现硬件加速相关实验 |
| 专家咨询 | 2-3人 | 特征存储、硬件加速领域专家 |

---

## 关联文档更新

完成上述任务后，需要更新以下项目文档：

- [x] `PROJECT-TRACKING.md` - 更新进度百分比
- [x] `INDEX.md` - 添加新文档索引
- [x] `README.md` - 更新项目范围描述
- [x] `THEOREM-REGISTRY.md` - 注册新定理/定义
- [x] `ARCHITECTURE.md` - 更新架构图

---

## 备注

1. **论文获取**: 部分论文可能需要通过学术网络或预印本获取
2. **动态调整**: 根据VLDB/SIGMOD 2025正式论文列表调整补充内容
3. **质量优先**: 宁可少而精，不可多而杂
4. **形式化要求**: 所有Struct/目录下的文档必须遵循六段式模板

---

*最后更新: 2026-04-15*
*维护者: AnalysisDataFlow项目团队*
