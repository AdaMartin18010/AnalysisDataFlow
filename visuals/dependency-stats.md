# 定理依赖网络统计报告

> **生成时间**: 2026-04-10 21:36:38
> **统计范围**: 1812 个形式化元素

---

## 1. 总体统计

### 1.1 按类型分布

| 类型 | 数量 | 占比 |
|------|------|------|
| Thm (定理) | 333 | 18.4% |
| Def (定义) | 906 | 50.0% |
| Lemma (引理) | 307 | 16.9% |
| Prop (命题) | 250 | 13.8% |
| Cor (推论) | 16 | 0.9% |

### 1.2 按阶段分布

| 阶段 | 数量 | 占比 |
|------|------|------|
| Struct (S) | 303 | 16.7% |
| Knowledge (K) | 448 | 24.7% |
| Flink (F) | 1061 | 58.6% |

### 1.3 连接统计

- **总引用关系数**: 96
- **总被引用次数**: 96
- **平均出度**: 0.05 (每个元素平均依赖)
- **平均入度**: 0.05 (每个元素平均被引用)

---

## 2. 最常被引用的元素 TOP20

| 排名 | 元素ID | 名称 | 类型 | 被引用次数 | 所在阶段 |
|------|--------|------|------|-----------|----------|
| 1 | `Thm-S-20-01` | Watermark完全格定理 | Thm | 4 | Struct |
| 2 | `Thm-S-19-01` | Chandy-Lamport一致性定理 | Thm | 3 | Struct |
| 3 | `Thm-S-23-01` | Choreographic死锁自由定理 | Thm | 3 | Struct |
| 4 | `Thm-S-13-01` | Flink Dataflow Exactly-Once保持 | Thm | 2 | Struct |
| 5 | `Thm-S-17-01` | Flink Checkpoint一致性定理 | Thm | 2 | Struct |
| 6 | `Thm-F-12-16` | Feature Store物化视图正确性定理 | Thm | 2 | Flink |
| 7 | `Thm-F-07-32` | 智能制造IoT实时检测正确性定理 | Thm | 2 | Flink |
| 8 | `Thm-K-06-51` | 智能合约事件驱动执行正确性定理 | Thm | 2 | Knowledge |
| 9 | `Thm-S-04-01` | Dataflow确定性定理 | Thm | 1 | Struct |
| 10 | `Thm-S-05-01` | Go-CS-sync与CSP编码保持迹语义等价 | Thm | 1 | Struct |
| 11 | `Thm-S-07-01` | 流计算确定性定理 | Thm | 1 | Struct |
| 12 | `Thm-S-09-01` | Watermark单调性定理 | Thm | 1 | Struct |
| 13 | `Thm-S-12-01` | 受限Actor系统编码保持迹语义 | Thm | 1 | Struct |
| 14 | `Thm-S-14-01` | 表达能力严格层次定理 | Thm | 1 | Struct |
| 15 | `Thm-S-07-03` | Smart Casual Verification有效性 | Thm | 1 | Struct |
| 16 | `Thm-K-04-01` | 流数据库vs流引擎选择定理 | Thm | 1 | Knowledge |
| 17 | `Thm-F-02-36` | Schema演化兼容性定理 | Thm | 1 | Flink |
| 18 | `Thm-F-02-40` | 多路Join最优计划选择定理 | Thm | 1 | Flink |
| 19 | `Thm-F-02-45` | ForSt状态后端一致性定理 | Thm | 1 | Flink |
| 20 | `Thm-F-02-60` | 智能检查点最优性定理 | Thm | 1 | Flink |

---

## 3. 最复杂的依赖链

### 3.1 链 #1 (深度: 2)

```
→ Lemma-S-04-01: 算子局部确定性
  → Thm-S-04-01: Dataflow确定性定理
```

### 3.2 链 #2 (深度: 2)

```
→ Lemma-S-04-02: Watermark单调性
  → Thm-S-09-01: Watermark单调性定理
```

### 3.3 链 #3 (深度: 2)

```
→ Lemma-S-05-02: CSP同步并行下迹前缀保持性
  → Thm-S-05-01: Go-CS-sync与CSP编码保持迹语义等价
```

### 3.4 链 #4 (深度: 2)

```
→ Lemma-S-07-02: Watermark单调性蕴含触发确定性
  → Thm-S-07-01: 流计算确定性定理
```

### 3.5 链 #5 (深度: 2)

```
→ Lemma-S-12-01: MAILBOX FIFO不变式
  → Thm-S-12-01: 受限Actor系统编码保持迹语义
```

### 3.6 链 #6 (深度: 2)

```
→ Lemma-S-13-01: 算子编码保持局部确定性
  → Thm-S-13-01: Flink Dataflow Exactly-Once保持
```

### 3.7 链 #7 (深度: 2)

```
→ Lemma-S-13-02: 屏障对齐保证快照一致性
  → Thm-S-13-01: Flink Dataflow Exactly-Once保持
```

### 3.8 链 #8 (深度: 2)

```
→ Lemma-S-07-07: 完备性边界
  → Thm-S-07-03: Smart Casual Verification有效性
```

### 3.9 链 #9 (深度: 2)

```
→ Lemma-S-17-01: Barrier传播不变式
  → Thm-S-17-01: Flink Checkpoint一致性定理
```

### 3.10 链 #10 (深度: 2)

```
→ Lemma-S-17-02: 状态一致性引理
  → Thm-S-17-01: Flink Checkpoint一致性定理
```

---

## 4. 孤立元素分析

检测到 **1632** 个孤立元素（无依赖且未被引用）：

| 元素ID | 名称 | 类型 |
|--------|------|------|
| `Thm-S-01-01` | USTM组合性定理 | Thm |
| `Thm-S-01-02` | 表达能力层次判定 | Thm |
| `Thm-S-02-01` | 动态通道演算严格包含静态通道演算 | Thm |
| `Thm-S-03-01` | Actor邮箱串行处理下的局部确定性 | Thm |
| `Thm-S-03-02` | 监督树活性定理 | Thm |
| `Thm-S-06-01` | 第一人称Choreographic死锁自由 | Thm |
| `Thm-S-01-03` | 会话类型安全性 (Type Safety) | Thm |
| `Thm-S-01-04` | 会话类型无死锁性 (Deadlock Freedom) | Thm |
| `Thm-S-01-05` | 协议合规性 (Protocol Compliance) | Thm |
| `Thm-S-08-01` | Exactly-Once必要条件 | Thm |
| `Thm-S-08-02` | 端到端Exactly-Once正确性 | Thm |
| `Thm-S-08-03` | 统一一致性格 | Thm |
| `Thm-S-10-01` | Actor安全/活性组合性 | Thm |
| `Thm-S-11-01` | 类型安全(Progress + Preservation) | Thm |
| `Thm-S-02-08` | CALM定理 (Consistency As Logical | Thm |
| `Thm-S-02-09` | 同态计算正确性定理 | Thm |
| `Thm-S-02-10` | 流式差分隐私组合性 | Thm |
| `Thm-S-15-01` | 互模拟同余定理 | Thm |
| `Thm-S-16-01` | 跨层映射组合定理 | Thm |
| `Thm-S-06-02` | 1CP的EPP完备性 | Thm |
| `Thm-S-06-03` | 1CP与Census-Polymorphic互编码 | Thm |
| `Thm-S-18-01` | Flink Exactly-Once正确性定理 | Thm |
| `Thm-S-18-02` | 幂等Sink等价性定理 | Thm |
| `Thm-S-21-01` | FG/FGG类型安全定理 | Thm |
| `Thm-S-22-01` | DOT子类型完备性定理 | Thm |
| `Thm-S-24-01` | Go与Scala图灵完备等价 | Thm |
| `Thm-S-07-04` | CCF共识安全性质 | Thm |
| `Thm-S-07-05` | Trace验证搜索优化 | Thm |
| `Thm-K-05-01` | 核心映射语义保持性定理 | Thm |
| `Thm-K-03-02` | Keystone平台SLA满足性 | Thm |
| `Thm-K-03-03` | 双11实时计算SLA满足性 | Thm |
| `Thm-K-02-02` | 日志关联完整性条件 | Thm |
| `Thm-K-06-01` | Rust所有权系统内存安全定理 | Thm |
| `Thm-K-06-02` | Rust借用检查器正确性定理 | Thm |
| `Thm-K-06-03` | Send/Sync边界线程安全定理 | Thm |
| `Thm-K-06-04` | 异步流处理无数据竞争定理 | Thm |
| `Thm-K-07-01` | GPU TEE机密性定理 | Thm |
| `Thm-K-07-02` | GPU TEE完整性定理 | Thm |
| `Thm-K-07-03` | GPU TEE远程证明正确性定理 | Thm |
| `Thm-K-07-04` | GPU流计算安全执行定理 | Thm |
| `Thm-K-08-01` | Lakehouse时间旅行一致性定理 | Thm |
| `Thm-K-08-02` | 流批一体ACID隔离性定理 | Thm |
| `Thm-K-08-03` | 元数据层一致性保证定理 | Thm |
| `Thm-K-08-04` | 增量处理正确性定理 | Thm |
| `Thm-K-09-01` | RAG检索正确性定理 | Thm |
| `Thm-K-09-02` | RAG流式生成一致性定理 | Thm |
| `Thm-K-09-03` | 向量索引实时更新一致性定理 | Thm |
| `Thm-K-09-04` | RAG端到端正确性定理 | Thm |
| `Thm-F-02-01` | ForSt Checkpoint一致性定理 | Thm |
| `Thm-F-02-02` | LazyRestore正确性定理 | Thm |
| ... | 还有 1582 个 | ... |

---

## 5. 循环依赖检测

✅ **未检测到循环依赖**，依赖图是无环的（DAG）。

---

## 6. 主题分布

- **一般** (general): 1571 个元素
- **类型系统** (types): 81 个元素
- **并发理论** (concurrency): 70 个元素
- **验证方法** (verification): 68 个元素
- **Lambda演算** (lambda): 22 个元素

---

## 7. 关键洞察

1. **网络规模**: 共有 1812 个形式化元素，96 条依赖边
2. **核心枢纽**: 被引用最多的是 `Thm-S-20-01`，有 4 个引用
3. **证明复杂度**: 最长依赖链深度为 2
4. **网络密度**: 平均每个元素依赖 0.05 个其他元素
5. **引用比例**: 平均每个元素被引用 0.05 次
6. **孤立比例**: 1632 / 1812 = 90.1% 的元素是孤立的

---

## 8. 可视化文件列表

生成的可视化文件：

| 文件 | 说明 |
|------|------|
| `visuals/interactive-dependency.html` | 交互式D3.js可视化 |
| `visuals/lambda-deps.mmd` | Lambda演算主题依赖图 (Mermaid) |
| `visuals/types-deps.mmd` | 类型系统主题依赖图 (Mermaid) |
| `visuals/concurrency-deps.mmd` | 并发理论主题依赖图 (Mermaid) |
| `visuals/verification-deps.mmd` | 验证方法主题依赖图 (Mermaid) |
| `visuals/s-stage-deps.mmd` | Struct阶段依赖图 (Mermaid) |
| `visuals/k-stage-deps.mmd` | Knowledge阶段依赖图 (Mermaid) |
| `visuals/f-stage-deps.mmd` | Flink阶段依赖图 (Mermaid) |
| `visuals/dependency-stats.md` | 本统计报告 |

---

*报告由 theorem-dependency-graph.py 自动生成*
