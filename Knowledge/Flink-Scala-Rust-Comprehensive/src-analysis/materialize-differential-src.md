# Materialize Differential Dataflow 源码深度分析

> 所属阶段: Knowledge/Flink-Scala-Rust-Comprehensive | 前置依赖: [Timely Dataflow论文] | 形式化等级: L4

## 1. 项目结构

### 1.1 目录组织

Materialize 基于 Differential Dataflow 构建，核心依赖两个开源项目：Timely Dataflow 和 Differential Dataflow。

```
materialize/
├── src/
│   ├── adapter/           # SQL 适配层 (PostgreSQL协议)
│   ├── compute/           # 计算层 (Timely/Differential)
│   │   ├── src/
│   │   │   ├── compute_state.rs
│   │   │   ├── render/
│   │   │   └── logging/
│   │   └── client/
│   ├── storage/           # 存储层 (Persist)
│   └── persist/           # 持久化实现
└── misc/
    └── differential/      # Differential Dataflow 集成
```

### 1.2 Differential Dataflow 项目结构

```
differential-dataflow/
├── src/
│   ├── lib.rs
│   ├── input.rs
│   ├── collection.rs
│   ├── operators/
│   │   ├── arrange.rs
│   │   ├── join.rs
│   │   ├── reduce.rs
│   │   └── iterate.rs
│   ├── trace/
│   │   ├── cursor.rs
│   │   └── implementations/
│   │       ├── ord.rs
│   │       └── spine.rs
│   └── dataflow.rs
└── timely/
    └── src/
        ├── worker.rs
        ├── dataflow.rs
        └── scheduling.rs
```

---

## 2. 核心模块分析

### 2.1 Differential Dataflow 核心

**路径位置**: `differential-dataflow/src/`

**职责描述**: Differential Dataflow 提供基于差分计算的增量计算框架，核心抽象是 Collection 和 Arrangement。

**关键 trait/struct**:

```rust
// differential-dataflow/src/collection.rs
pub struct Collection<G: Scope, D, R: Semigroup> {
    pub inner: Stream<G, (D, G::Timestamp, R)>,
    pub phantom: PhantomData<(D, R)>,
}

// differential-dataflow/src/operators/arrange.rs
pub struct Arranged<G, T>
where
    G: Scope,
    T: TraceReader,
{
    pub stream: Stream<G, T::Batch>,
    pub trace: T::Trace,
}

// differential-dataflow/src/trace/implementations/spine.rs
pub struct Spine<K, V, T, R>
where
    T: Lattice + Ord,
    R: Semigroup,
{
    pub layers: Vec<Layer<K, V, T, R>>,
    pub merging: Vec<Option<MergeState<K, V, T, R>>>,
    pub since: Antichain<T>,
}
```

**源码分析 - Collection 差分语义**:

```rust
// differential-dataflow/src/collection.rs
impl<G: Scope, D: Data, R: Semigroup> Collection<G, D, R> {
    /// 合并两个 Collection
    pub fn concat(&self, other: &Self) -> Self {
        Collection {
            inner: self.inner.concat(&other.inner),
            phantom: PhantomData,
        }
    }

    /// 映射操作 (保持差分语义)
    pub fn map<D2, F>(&self, logic: F) -> Collection<G, D2, R>
    where
        D2: Data,
        F: Fn(D) -> D2 + 'static,
    {
        self.inner.map(move |(d, t, r)| (logic(d), t, r))
                  .as_collection()
    }

    /// 过滤操作
    pub fn filter<F>(&self, logic: F) -> Self
    where
        F: Fn(&D) -> bool + 'static,
    {
        self.inner.filter(move |(d, _t, _r)| logic(d))
                  .as_collection()
    }

    /// 聚合操作 (核心:产生 Arrangement)
    pub fn reduce<L, K, V2>(&self, logic: L) -> Collection<G, (K, V2), R>
    where
        K: Data,
        V2: Data,
        L: Fn(&K, &[(V, R)], &mut Vec<(V2, R)>) + 'static,
    {
        self.arrange_by_key()
            .reduce_named("Reduce", logic)
            .as_collection()
    }
}
```

### 2.2 Arrangement 实现

**路径位置**: `differential-dataflow/src/operators/arrange.rs`

**职责描述**: Arrangement 是 Differential Dataflow 的核心优化结构，类似于索引，支持高效的增量查询。

**源码分析 - ArrangeByKey**:

```rust
// differential-dataflow/src/operators/arrange.rs
impl<G: Scope, K: Data+Hashable, V: Data, R: Semigroup>
    ArrangeByKey<G, K, V, R> for Collection<G, (K, V), R>
{
    fn arrange_by_key(
        &self,
    ) -> Arranged<G, TraceAgent<OrdValSpine<K, V, G::Timestamp, R>>>
    {
        // 配置 Trace 容量
        let mut trace = OrdValSpine::new();
        let mut buffer = Vec::new();

        self.inner.unary_frontier(Pipeline, "ArrangeByKey", move |cap, info| {
            move |input, output| {
                // 处理输入更新
                input.for_each(|time, data| {
                    data.swap(&mut buffer);

                    // 按 key 排序并分组
                    buffer.sort_by(|((k1, _), _, _), ((k2, _), _, _)| k1.cmp(k2));

                    // 构建 Batch
                    let batch = OrdValBatch::from_data(
                        buffer.drain(..).map(|((k, v), t, r)| (k, v, t, r))
                    );

                    // 插入 Trace
                    trace.insert(batch);

                    // 输出 Batch 到下游
                    output.session(&time).give(batch);
                });

                // 推进 Frontier
                trace.advance_by(input.frontier().frontier());
            }
        })
        .arrange(trace)
    }
}
```

**Arrangement 结构图**:

```mermaid
graph TB
    subgraph "Arrangement 内部结构"
        Layer0["Layer 0<br/>(最新数据)"]
        Layer1["Layer 1"]
        Layer2["Layer 2"]
        LayerN["Layer N<br/>(历史数据)"]

        Layer0 --> Layer1
        Layer1 --> Layer2
        Layer2 --> LayerN
    end

    subgraph "每层内部"
        Batch["Batch (有序数据块)"]
        Keys["Keys (有序键列表)"]
        Diffs["Deltas (时间差分)"]

        Batch --> Keys
        Batch --> Diffs
    end
```

### 2.3 时间处理与进度追踪

**路径位置**: `timely-dataflow/src/progress/`

**职责描述**: Timely Dataflow 的核心创新是显式时间戳和进度追踪，支持迭代和循环数据流。

**关键 trait/struct**:

```rust
// timely-dataflow/src/progress/timestamp.rs
pub trait Timestamp: Clone+Ord+Debug+Send+Any {
    type Summary: PathSummary<Self>;
    fn minimum() -> Self;
}

// timely-dataflow/src/progress/frontier.rs
pub struct Antichain<T> {
    elements: Vec<T>,
}

impl<T: PartialOrder> Antichain<T> {
    /// 插入元素,保持反链性质
    pub fn insert(&mut self, element: T) -> bool {
        if self.elements.iter().any(|e| e.less_equal(&element)) {
            return false;
        }
        self.elements.retain(|e| !element.less_equal(e));
        self.elements.push(element);
        true
    }

    /// 检查时间戳是否在后继集合中
    pub fn less_equal(&self, time: &T) -> bool {
        self.elements.iter().any(|e| e.less_equal(time))
    }
}
```

**源码分析 - Frontier 更新**:

```rust
// timely-dataflow/src/progress/frontier.rs
impl<T: Timestamp> MutableAntichain<T> {
    /// 更新 Frontier
    pub fn update_iter<I>(&mut self, updates: I) -> ChangeBatch<T>
    where
        I: IntoIterator<Item = (T, i64)>,
    {
        let mut changes = ChangeBatch::new();

        for (time, delta) in updates {
            let old_frontier = self.frontier().to_vec();

            // 更新计数
            if delta > 0 {
                self.occurances.insert(time.clone(), delta as usize);
            } else {
                self.occurances.remove(&time);
            }

            // 计算新 Frontier
            let new_frontier = self.rebuild_frontier();

            // 记录变化
            for t in old_frontier.iter() {
                if !new_frontier.less_equal(t) {
                    changes.update(t.clone(), -1);
                }
            }
            for t in new_frontier.iter() {
                if !old_frontier.less_equal(t) {
                    changes.update(t.clone(), 1);
                }
            }
        }

        changes
    }
}
```

### 2.4 增量计算优化

**路径位置**: `differential-dataflow/src/operators/join.rs`

**职责描述**: Join 是流处理的核心算子，Differential Dataflow 通过 Arrangement 共享实现高效的增量 Join。

**源码分析 - Delta Join**:

```rust
// differential-dataflow/src/operators/join.rs
impl<G, K, V1, V2, R1, R2> JoinCore<G, K, V2, R2> for Arranged<G, K, V1, R1>
where
    G: Scope,
    K: Data,
    V1: Data,
    V2: Data,
    R1: Semigroup,
    R2: Semigroup,
{
    fn join_core<V3, R3, F>(&self, other: &Arranged<G, K, V2, R2>, logic: F)
        -> Collection<G, (K, V3), R3>
    where
        V3: Data,
        R3: Semigroup,
        F: Fn(&K, &V1, &V2, &mut Vec<(V3, R3)>) + 'static,
    {
        // 获取两个 Arrangement 的 Trace
        let trace1 = self.trace.clone();
        let trace2 = other.trace.clone();

        self.stream.binary_frontier(
            &other.stream,
            Pipeline,
            Pipeline,
            "Join",
            move |capability, info| {
                let mut trace1_cursor = trace1.cursor();
                let mut trace2_cursor = trace2.cursor();

                move |input1, input2, output| {
                    // 处理左侧输入的增量更新
                    input1.for_each(|time, data| {
                        let mut session = output.session(&time);
                        for (key, val1, diff1) in data.iter() {
                            // 在右侧 Arrangement 中查找匹配
                            trace2_cursor.seek_key(key);
                            while trace2_cursor.key_valid() &&
                                  trace2_cursor.key() == key {
                                let val2 = trace2_cursor.val();
                                let diff2 = trace2_cursor.diff();

                                // 应用 Join 逻辑
                                let mut results = Vec::new();
                                logic(key, val1, val2, &mut results);

                                for (result, diff3) in results {
                                    let combined_diff =
                                        diff1.multiply(diff2).multiply(&diff3);
                                    session.give((
                                        (key.clone(), result),
                                        time.clone(),
                                        combined_diff,
                                    ));
                                }

                                trace2_cursor.step_val();
                            }
                        }
                    });

                    // 对称处理右侧输入...
                }
            }
        )
    }
}
```

**增量 Join 示意图**:

```mermaid
graph LR
    subgraph "输入 1 (增量)"
        Delta1["ΔA: +{k1, v1}"]
    end

    subgraph "Arrangement B (索引)"
        B1["k1 -> [v2, v3]"]
        B2["k2 -> [v4]"]
    end

    subgraph "输出 (增量)"
        Out1["+{k1, (v1,v2)}"]
        Out2["+{k1, (v1,v3)}"]
    end

    Delta1 --> Join["Join Operator"]
    B1 --> Join
    Join --> Out1
    Join --> Out2
```

### 2.5 强一致性保证机制

**路径位置**: `materialize/src/persist/src/`

**职责描述**: Materialize 的 Persist 层提供严格序列化 (Strict Serializability) 保证。

**关键 trait/struct**:

```rust
// src/persist/src/indexed/mod.rs
pub struct Indexed<K, V, T, D> {
    /// 写入缓冲区
    log: Vec<(K, V, T, D)>,
    /// 已索引数据
    traces: HashMap<Id, TraceArrangement<K, V, T, D>>,
    /// 已持久化 Frontier
    since: Antichain<T>,
    /// 上界时间戳
    upper: Antichain<T>,
}

// src/persist/src/s3.rs
pub struct S3Blob {
    client: S3Client,
    bucket: String,
    key_prefix: String,
}
```

**源码分析 - 事务性写入**:

```rust
// src/persist/src/indexed/mod.rs
impl<K, V, T, D> Indexed<K, V, T, D> {
    /// 原子性写入批次
    pub async fn write_batch(
        &mut self,
        batch: Vec<(K, V, T, D)>,
    ) -> Result<Upper<T>, Error> {
        // 1. 分配新的 Upper
        let new_upper = self.advance_upper();

        // 2. 验证所有时间戳小于 new_upper
        for (_, _, ts, _) in &batch {
            if !self.upper.less_equal(ts) {
                return Err(Error::InvalidTimestamp);
            }
        }

        // 3. 写入 WAL (Write-Ahead Log)
        let wal_entry = WalEntry::Batch {
            data: batch.clone(),
            upper: new_upper.clone(),
        };
        self.blob.write_wal(wal_entry).await?;

        // 4. 更新内存索引
        self.log.extend(batch);

        // 5. 触发异步 Compaction
        if self.log.len() > self.compaction_threshold {
            self.trigger_compaction().await?;
        }

        Ok(Upper(new_upper))
    }

    /// 获取一致性快照
    pub async fn snapshot(
        &self,
        as_of: Antichain<T>,
    ) -> Result<Snapshot<K, V, T, D>, Error> {
        // 验证 as_of 是有效的
        if !self.since.less_equal(&as_of) {
            return Err(Error::SnapshotBeforeSince);
        }

        // 合并所有相关 Trace
        let mut cursor = Cursor::new();
        for trace in self.traces.values() {
            trace.cursor().seek(&as_of);
            while cursor.valid() {
                // 收集数据
            }
        }

        Ok(Snapshot { cursor, as_of })
    }
}
```

---

## 3. 数据流分析

### 3.1 查询渲染 Pipeline

```mermaid
graph TB
    subgraph "SQL Adapter"
        SQL["SQL Query"]
        Parser["Parser"]
        Planner["Query Planner"]
        MIR["MIR (中间表示)"]
    end

    subgraph "Compute Layer"
        Render["Render (MIR -> Dataflow)"]
        Timely["Timely Dataflow"]
        Differential["Differential Operators"]
    end

    subgraph "Storage Layer"
        Persist["Persist"]
        S3["S3 / Blob Storage"]
    end

    SQL --> Parser
    Parser --> Planner
    Planner --> MIR
    MIR --> Render
    Render --> Timely
    Timely --> Differential
    Differential --> Persist
    Persist --> S3
```

### 3.2 物化视图维护流程

```rust
// src/compute/src/render/mod.rs
pub fn render_mir_plan(
    scope: &mut G,
    plan: Plan,
    sources: &SourceConnector,
) -> Collection<G, Row, Diff> {
    match plan {
        Plan::Constant { rows } => {
            // 常量数据
            scope.new_collection_from(rows).1
        }
        Plan::Get { id } => {
            // 获取源或索引
            sources.get(&id).expect("source not found")
        }
        Plan::Project { input, outputs } => {
            // 投影
            let input_collection = render_mir_plan(scope, *input, sources);
            input_collection.map(move |row| {
                Row::pack(outputs.iter().map(|i| row[*i]))
            })
        }
        Plan::Join { inputs, plan } => {
            // Join
            let input1 = render_mir_plan(scope, inputs.into_iter().next().unwrap(), sources);
            let input2 = render_mir_plan(scope, inputs.into_iter().next().unwrap(), sources);

            // 创建 Arrangements
            let arranged1 = input1.arrange_by_key();
            let arranged2 = input2.arrange_by_key();

            // 增量 Join
            arranged1.join_core(&arranged2, |k, v1, v2, output| {
                output.push((Row::pack(k.iter().chain(v1.iter()).chain(v2.iter())), 1));
            })
        }
        Plan::Reduce { input, key, aggregates } => {
            // 聚合
            let input_collection = render_mir_plan(scope, *input, sources);

            input_collection
                .map(move |row| (Row::pack(key.iter().map(|i| row[*i])), row))
                .arrange_by_key()
                .reduce(move |_key, source, target| {
                    // 计算聚合值
                    let mut accumulators: Vec<_> = aggregates.iter()
                        .map(|agg| agg.create_accumulator())
                        .collect();

                    for (row, diff) in source {
                        for (i, agg) in aggregates.iter().enumerate() {
                            accumulators[i].update(row, *diff);
                        }
                    }

                    // 输出聚合结果
                    let result = Row::pack(accumulators.iter().map(|a| a.finish()));
                    target.push((result, 1));
                })
                .as_collection()
        }
        _ => unimplemented!(),
    }
}
```

---

## 4. 关键算法

### 4.1 差分数据流核心算法

**伪代码**:

```
Algorithm: Differential Dataflow Update

Input: Update (data, time, diff)
Output: Propagated changes through dataflow graph

1. For each operator in topological order:
   a. Collect input updates at current time

   b. If operator is stateless (map, filter):
      - Apply function to each element
      - Emit output updates with same time and diff

   c. If operator is stateful (reduce, join):
      - Update internal trace with new updates
      - Compute output differences
      - For Join: look up matching keys in other input's trace
      - For Reduce: recompute aggregates for affected keys
      - Emit delta updates

   d. Advance frontier if all inputs have progressed

2. Repeat until no more updates at current time

3. Propagate to next timestamp in partial order
```

**Rust 实现** (differential-dataflow/src/operators/reduce.rs):

```rust
/// Reduce 操作的核心实现
pub fn reduce_implementation<K, V1, V2, T, R1, R2>(
    source: &Collection<(K, V1), T, R1>,
    logic: impl Fn(&K, &[(V1, R1)], &mut Vec<(V2, R2)>),
) -> Collection<(K, V2), T, R2>
where
    K: Data+Hash,
    V1: Data,
    V2: Data,
    T: Lattice+Ord,
    R1: Semigroup,
    R2: Semigroup,
{
    source.arrange_by_key().reduce_named("Reduce", logic)
}

/// Trace 上的增量 Reduce
impl<K, V, T, R> TraceReader for Spine<K, V, T, R> {
    fn reduce<L, V2, R2>(&self, logic: L) -> Collection<(K, V2), T, R2>
    where
        L: Fn(&K, &[(V, R)], &mut Vec<(V2, R2)>),
    {
        // 遍历所有键
        let mut cursor = self.cursor();
        while cursor.key_valid() {
            let key = cursor.key();

            // 收集该键的所有 (value, diff) 对
            let mut values = Vec::new();
            while cursor.val_valid() {
                let val = cursor.val();
                let diffs = cursor.diffs();
                for (time, diff) in diffs {
                    values.push((val.clone(), diff.clone()));
                }
                cursor.step_val();
            }

            // 应用 Reduce 逻辑
            let mut output = Vec::new();
            logic(key, &values, &mut output);

            // 输出结果
            for (v2, r2) in output {
                emit((key.clone(), v2), r2);
            }

            cursor.step_key();
        }
    }
}
```

### 4.2 Spine 合并策略

```rust
// differential-dataflow/src/trace/implementations/spine.rs
impl<K, V, T, R> Spine<K, V, T, R> {
    /// 插入新的 Batch,触发层级合并
    pub fn insert(&mut self, batch: Batch<K, V, T, R>) {
        // 找到合适的层级
        let mut level = 0;
        let mut batch = Some(batch);

        while let Some(b) = batch.take() {
            if level >= self.layers.len() {
                self.layers.push(Layer::new());
                self.merging.push(None);
            }

            if self.merging[level].is_none() {
                // 该层级空闲,直接插入
                self.merging[level] = Some(MergeState::Single(b));
            } else {
                // 需要合并
                let existing = self.merging[level].take().unwrap();
                batch = Some(self.merge_batches(existing, b, level));
            }

            level += 1;
        }
    }

    /// 合并两个 Batch
    fn merge_batches(
        &mut self,
        left: MergeState<K, V, T, R>,
        right: Batch<K, V, T, R>,
        level: usize,
    ) -> Batch<K, V, T, R> {
        // 使用归并排序合并两个有序 Batch
        let mut result = Batch::new();

        let (iter1, iter2) = (left.iter(), right.iter());

        // 归并两个迭代器
        let merged = MergeIterator::new(iter1, iter2);

        for ((k, v, t), r) in merged {
            // 合并相同键的差分
            if result.last().map(|(k2, _, _)| k2 == k).unwrap_or(false) {
                result.merge_last((k, v, t), r);
            } else {
                result.push((k, v, t), r);
            }
        }

        result
    }
}
```

---

## 5. 与 Flink 对比

| 维度 | Materialize (Differential) | Apache Flink |
|------|---------------------------|--------------|
| **计算模型** | 差分数据流 (Differential Dataflow) | Dataflow (Chandy-Lamport) |
| **时间语义** | 显式偏序时间戳 (Lattice) | 事件时间 + Watermark |
| **状态管理** | Arrangement (索引化) | Keyed State (RocksDB) |
| **增量计算** | 原生支持 (Diff 传播) | 需手动实现 |
| **一致性** | 严格序列化 (Strict Serializable) | Exactly-Once |
| **迭代计算** | 原生支持 (循环数据流) | 需外部迭代 |
| **共享状态** | Arrangement 跨查询共享 | 状态隔离 |
| **SQL支持** | 原生 (PostgreSQL) | Flink SQL |

### 5.1 状态管理对比

```mermaid
graph TB
    subgraph "Materialize State Management"
        MV1["Materialized View 1"]
        MV2["Materialized View 2"]
        Arr1["Arrangement A (共享)"]
        Arr2["Arrangement B"]

        MV1 --> Arr1
        MV2 --> Arr1
        MV2 --> Arr2
    end

    subgraph "Flink State Management"
        Job1["Job 1"]
        Job2["Job 2"]
        State1["RocksDB State 1 (隔离)"]
        State2["RocksDB State 2 (隔离)"]

        Job1 --> State1
        Job2 --> State2
    end
```

### 5.2 架构设计决策对比

| 决策点 | Materialize | Flink |
|--------|-------------|-------|
| 为何选择 Differential | 学术原型，严格一致性 | 工业成熟，吞吐优先 |
| 状态共享 | Arrangement 自动共享 | 手动优化 |
| 时间模型 | 偏序时间戳 | 全序事件时间 |
| 部署模式 | 云原生 SaaS | 自托管/云服务 |
| 适用场景 | 强一致性 OLAP | 高吞吐 ETL |

---

## 6. 引用参考
