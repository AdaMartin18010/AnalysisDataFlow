---
title: "[EN] Unified Model Relationship Graph"
translation_status: "ai_translated"
source_file: "Struct/Unified-Model-Relationship-Graph.md"
source_version: "17194f9b"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.329610"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # 统一模型关系图谱 -->

<!-- TRANSLATE: > 所属阶段: Struct/ | 前置依赖: [01.01-unified-streaming-theory.md](./01-foundation/01.01-unified-streaming-theory.md), [03.03-expressiveness-hierarchy.md](./03-relationships/03.03-expressiveness-hierarchy.md), [03.04-bisimulation-equivalences.md](./03-relationships/03.04-bisimulation-equivalences.md) | 形式化等级: L4-L5 -->


<!-- TRANSLATE: ## 2. 属性推导 (Properties) -->

<!-- TRANSLATE: ### Prop-U-01: 表达能力单调性 -->

**命题**: 表达力层级 $\mathcal{E}$ 满足偏序的传递性：
$$M_1 \preceq_{exp} M_2 \land M_2 \preceq_{exp} M_3 \implies M_1 \preceq_{exp} M_3$$

<!-- TRANSLATE: **直观解释**: 编码关系可以传递组合，高层模型的完备编码能够继承低层模型的编码能力。 -->

<!-- TRANSLATE: ### Prop-U-02: 互模拟层次关系 -->

<!-- TRANSLATE: **命题**: 三种互模拟满足严格包含关系： -->
$$\sim \subsetneq \approx_w \subsetneq \approx_o$$

<!-- TRANSLATE: 即强互模拟蕴含弱互模拟，弱互模拟蕴含观测等价，但逆命题不成立。 -->

<!-- TRANSLATE: **证明概要**:  -->
- $\sim \subseteq \approx_w$: 强互模拟也是弱互模拟（取 $\tau$ 为恒等迁移）
- $\approx_w \subseteq \approx_o$: 弱互模拟保持外部迹
<!-- TRANSLATE: - 严格性通过反例证明：存在弱互模拟但不强互模拟的进程对 -->

<!-- TRANSLATE: ### Prop-U-03: 编码完备性的组合律 -->

**命题**: 若 $\llbracket \cdot \rrbracket_{12}: M_1 \to M_2$ 和 $\llbracket \cdot \rrbracket_{23}: M_2 \to M_3$ 均为完备编码，则复合编码 $\llbracket \cdot \rrbracket_{13} = \llbracket \cdot \rrbracket_{23} \circ \llbracket \cdot \rrbracket_{12}$ 也是完备的。


<!-- TRANSLATE: ## 4. 论证过程 (Argumentation) -->

<!-- TRANSLATE: ### 4.1 为什么Process Calculus位于表达力顶层 -->

<!-- TRANSLATE: Process Calculus（特别是π-calculus）能够表达动态通道创建和传递，这一特性使其成为表达力的"通用语言"： -->

<!-- TRANSLATE: 1. **动态拓扑**: π-calculus允许在运行时创建新通道并传递给其他进程，模拟动态变化的通信拓扑 -->
<!-- TRANSLATE: 2. **名称传递**: 通过名称传递(name passing)机制，可以实现Actor模型的动态地址传递 -->
<!-- TRANSLATE: 3. ** mobility**: π-calculus的 mobility 特性支持表达移动计算和动态重构 -->

<!-- TRANSLATE: ### 4.2 Dataflow作为中间层的合理性 -->

<!-- TRANSLATE: Dataflow模型选择性地限制了表达能力，换取了更好的可分析性： -->

<!-- TRANSLATE: - **有界状态**: Dataflow图的静态结构使得状态空间更易分析 -->
<!-- TRANSLATE: - **时间语义**: 显式的时间模型（事件时间、处理时间）使得时序性质可验证 -->
<!-- TRANSLATE: - **确定性**: 纯函数Dataflow图天然满足确定性，简化正确性论证 -->

<!-- TRANSLATE: 这种"表达能力换可分析性"的权衡是流处理系统设计的核心考量。 -->

<!-- TRANSLATE: ### 4.3 编码不完备性的工程意义 -->

<!-- TRANSLATE: 并非所有模型间编码都是完备的，这种不完备性具有重要的工程意义： -->

<!-- TRANSLATE: | 源模型 | 目标模型 | 编码限制 | 工程影响 | -->
<!-- TRANSLATE: |--------|----------|----------|----------| -->
<!-- TRANSLATE: | Actor (动态地址) | CSP | 不完备 | CSP验证工具无法直接验证动态拓扑系统 | -->
<!-- TRANSLATE: | Flink | π-calculus | 部分 | 形式验证需抽象某些运行时特性 | -->
<!-- TRANSLATE: | 带Flink SQL的Dataflow | 纯Dataflow | 不完备 | SQL优化器的某些转换需额外正确性保证 | -->


<!-- TRANSLATE: ## 6. 实例验证 (Examples) -->

<!-- TRANSLATE: ### 6.1 模型编码实例: Actor到π-calculus -->

<!-- TRANSLATE: **源模型 (Actor)**: -->
```
Actor A:
  receive msg:
    if msg == "ping":
      send "pong" to sender
```

<!-- TRANSLATE: **目标编码 (π-calculus)**: -->
```
[[A]] = νa.(A⟨a⟩ | !a(x).(x == "ping").sender̄⟨"pong"⟩)
```

<!-- TRANSLATE: **编码说明**: -->
- Actor地址 $A$ 编码为 π-calculus 通道名 $a$
- 邮箱编码为带复制的输入守卫 $!a(x)$
- 消息发送编码为输出前缀 $\bar{sender}\langle"pong"\rangle$

<!-- TRANSLATE: ### 6.2 Flink算子编码实例 -->

<!-- TRANSLATE: **Flink DataStream**: -->
```java
DataStream<Event> stream = env
  .addSource(new KafkaSource<>())
  .map(e -> e.transform())
  .keyBy(e -> e.getKey())
  .window(TumblingEventTimeWindows.of(Time.minutes(5)))
  .aggregate(new MyAggregate());
```

<!-- TRANSLATE: **π-calculus编码框架**: -->
```
[[Source]] = νout.(KafkaConsumer | out̄⟨msg⟩.[[Source]])
[[Map]] = νin,out.(!in(x).out̄⟨f(x)⟩ | [[Map']])
[[Window]] = νin,out.(Buffer | Timer | Aggregator)
```

<!-- TRANSLATE: **验证**: 此编码保持数据流语义，但抽象了Flink的分布式执行细节。 -->


<!-- TRANSLATE: ## 8. 引用参考 (References) -->

<!-- TRANSLATE: [^1]: R. Milner, "Communicating and Mobile Systems: The π-calculus", Cambridge University Press, 1999. -->
<!-- TRANSLATE: [^2]: C.A.R. Hoare, "Communicating Sequential Processes", Prentice Hall, 1985. -->
<!-- TRANSLATE: [^3]: G. Agha, "Actors: A Model of Concurrent Computation in Distributed Systems", MIT Press, 1986. -->
<!-- TRANSLATE: [^4]: T. Akidau et al., "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing", PVLDB, 8(12), 2015. -->
<!-- TRANSLATE: [^5]: J.L. Peterson, "Petri Net Theory and the Modeling of Systems", Prentice Hall, 1981. -->
<!-- TRANSLATE: [^6]: R. Milner, "A Calculus of Communicating Systems", LNCS 92, Springer, 1980. -->
<!-- TRANSLATE: [^7]: D. Sangiorgi, "Introduction to Bisimulation and Coinduction", Cambridge University Press, 2011. -->
<!-- TRANSLATE: [^8]: Apache Flink Documentation, "DataStream API", 2025. https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/overview/ -->
<!-- TRANSLATE: [^9]: M. Papazoglou et al., "The Expressiveness of CSP with Priority", CONCUR 2000. -->
<!-- TRANSLATE: [^10]: F. Arbab, "Reo: A Channel-based Coordination Model for Component Composition", Mathematical Structures in Computer Science, 14(3), 2004. -->


<!-- TRANSLATE: *本文档遵循 [AGENTS.md](../AGENTS.md) 六段式模板规范 | 更新时间: 2026-04-06* -->
