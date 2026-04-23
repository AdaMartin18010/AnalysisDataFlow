with open('Struct/06-frontier/ai-agent-streaming-formal-theory.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Content to insert before references
insertion = """### 7.6 AI Agent流式形式化理论推理树

**推理树：从底层定义到顶层定理的完整推导链**

```mermaid
graph BT
    subgraph 底层定义 [底层定义]
        D1[Def-S-AAS-02<br/>Agent认知状态机]
        D2[Def-S-AAS-03<br/>流式PTA循环]
        D3[Def-S-AAS-04<br/>Agent通信协议]
        D4[Def-S-AAS-05<br/>记忆与上下文系统]
    end

    subgraph 行为引理 [行为引理]
        L1[Lemma-S-AAS-01<br/>Agent状态迁移引理]
        L2[Lemma-S-AAS-02<br/>消息传递可靠性引理]
    end

    subgraph 中间命题 [中间命题]
        P1[Prop-S-AAS-01<br/>Agent响应时间下界]
        P2[Prop-S-AAS-02<br/>多Agent协作一致性]
    end

    subgraph 顶层定理 [顶层定理]
        T1[Thm-S-AAS-01<br/>单Agent流处理正确性]
        T2[Thm-S-AAS-02<br/>多Agent协作终止性]
        T3[Thm-S-AAS-03<br/>流式推理一致性]
    end

    D1 --> L1
    D2 --> L1
    D4 --> L1
    D3 --> L2
    D4 --> L2
    L1 --> P1
    L1 --> P2
    L2 --> P2
    P1 --> T1
    D2 --> T1
    D4 --> T1
    P2 --> T2
    T1 --> T2
    L2 --> T2
    L1 --> T3
    D2 --> T3
    D4 --> T3

    style D1 fill:#e1f5ff
    style D2 fill:#e1f5ff
    style D3 fill:#e1f5ff
    style D4 fill:#e1f5ff
    style L1 fill:#fff2cc
    style L2 fill:#fff2cc
    style P1 fill:#d5f5e3
    style P2 fill:#d5f5e3
    style T1 fill:#fadbd8
    style T2 fill:#fadbd8
    style T3 fill:#fadbd8
```

**说明**：此推理树展示了本文形式化理论的完整推导层次结构。底层定义（Def-S-AAS-02 至 Def-S-AAS-05）通过状态迁移引理和消息可靠性引理，支撑中间命题（响应时间下界与协作一致性），最终推导出三个顶层定理（单Agent正确性、多Agent终止性、流式推理一致性）。箭头方向表示理论依赖关系，颜色分层区分定义层（蓝）、引理层（黄）、命题层（绿）、定理层（红）。

---

### 7.7 概念关联矩阵

**概念关联矩阵：AI Agent与Actor模型、π-calculus、Session Types的严格映射**

```mermaid
graph TB
    subgraph Agent流计算 [Agent流计算 — 本文理论]
        A1[Agent认知状态机<br/>Def-S-AAS-02]
        A2[Agent通信协议<br/>Def-S-AAS-04]
        A3[流式PTA循环<br/>Def-S-AAS-03]
        A4[记忆与上下文系统<br/>Def-S-AAS-05]
    end

    subgraph Actor模型 [Actor模型 — Hewitt et al.]
        B1[Actor行为<br/>behavior = δ_w^perc ∘ δ_w^know ∘ δ_w^plan]
        B2[Actor邮箱<br/>mailbox ≈ 消息队列 Q_w]
        B3[Actor创建<br/>spawn ≈ Agent实例化 create_w]
        B4[异步消息<br/>send ≈ 通信协议 C]
    end

    subgraph π演算 [π-calculus — Milner]
        C1[通道名传递<br/>ch_ij — Agent间通道]
        C2[名字限制 νz<br/>私有通信通道]
        C3[并行组合 P|Q<br/>多Agent并发协作]
        C4[通信原语 ā⟨b⟩<br/>消息发送与接收]
    end

    subgraph 会话类型 [Session Types — Honda]
        D1[双端类型 !T.T / ?T.T<br/>请求-响应模式]
        D2[分支选择 &{l_i:P_i}<br/>协商协议分支]
        D3[递归类型 rec X.P<br/>多轮协商迭代]
        D4[线性通道保证<br/>因果序保持 Lemma-S-AAS-02]
    end

    A1 -.->|Φ: 行为映射| B1
    A2 -.->|Φ: 邮箱→队列| B2
    A3 -.->|Φ: 创建对应| B3
    A2 -.->|异步基础| B4
    A2 -.->|通道同构| C1
    A4 -.->|记忆隔离| C2
    A2 -.->|并行协作| C3
    A2 -.->|消息原语对应| C4
    A2 -.->|双端协议| D1
    A2 -.->|协商分支| D2
    A2 -.->|递归协商| D3
    A2 -.->|线性使用保证| D4
    B4 -.->|异步基础| A2
    C1 -.->|通道实例化| A2
    D1 -.->|类型安全| A2

    style A1 fill:#e1f5ff
    style A2 fill:#e1f5ff
    style A3 fill:#e1f5ff
    style A4 fill:#e1f5ff
    style B1 fill:#fff2cc
    style B2 fill:#fff2cc
    style B3 fill:#fff2cc
    style B4 fill:#fff2cc
    style C1 fill:#d5f5e3
    style C2 fill:#d5f5e3
    style C3 fill:#d5f5e3
    style C4 fill:#d5f5e3
    style D1 fill:#fadbd8
    style D2 fill:#fadbd8
    style D3 fill:#fadbd8
    style D4 fill:#fadbd8
```

**说明**：此概念关联矩阵展示了本文Agent流计算形式化理论与三大经典并发模型——Actor模型、π-calculus、Session Types——之间的严格映射关系。虚线箭头表示概念层面的对应与借鉴关系：Actor模型提供异步消息传递基础；π-calculus提供通道动态创建与进程组合的形式化框架；Session Types提供通信协议的类型安全保障。颜色分层区分Agent理论（蓝）、Actor模型（黄）、π-calculus（绿）、Session Types（红）。

---

"""

references = """## 8. 引用参考 (References)

[^1]: C. Hewitt, P. Bishop, and R. Steiger, "A Universal Modular Actor Formalism for Artificial Intelligence", IJCAI, 1973.
[^2]: R. Milner, "Communicating and Mobile Systems: the π-Calculus", Cambridge University Press, 1999.
[^3]: K. Honda, V. Vasconcelos, and M. Kubo, "Language Primitives and Type Discipline for Structured Communication-Based Programming", ESOP, 1998.
[^4]: G. A. Agha, "Actors: A Model of Concurrent Computation in Distributed Systems", MIT Press, 1986.
[^5]: T. Akidau et al., "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing", PVLDB, 8(12), 2015.
[^6]: L. Lamport, "Time, Clocks, and the Ordering of Events in a Distributed System", CACM, 21(7), 1978.
[^7]: R. S. Sutton and A. G. Barto, "Reinforcement Learning: An Introduction", 2nd ed., MIT Press, 2018.
[^8]: S. Russell and P. Norvig, "Artificial Intelligence: A Modern Approach", 4th ed., Pearson, 2020.

---
"""

# Find the split point: just before '## 8. 引用参考 (References)'
ref_idx = content.find('## 8. 引用参考 (References)')
if ref_idx == -1:
    raise ValueError("Could not find references section")

# Also find the start of appendix A
appendix_idx = content.find('## 附录A：符号表')
if appendix_idx == -1:
    raise ValueError("Could not find appendix A section")

# Build new content: everything before refs + insertion + references + everything from appendix on
new_content = content[:ref_idx] + insertion + references + content[appendix_idx:]

with open('Struct/06-frontier/ai-agent-streaming-formal-theory.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

import os
new_size = os.path.getsize('Struct/06-frontier/ai-agent-streaming-formal-theory.md')
old_size = len(content.encode('utf-8'))
print(f'Old file size: {old_size} bytes')
print(f'New file size: {new_size} bytes')
print(f'Added: {new_size - old_size} bytes')
print('Done')
