import sys

with open('Struct/01-foundation/01.01-unified-streaming-theory.md', 'r', encoding='utf-8') as f:
    content = f.read()

old_73 = r"""```mermaid
graph BT
    %% 顶层：定理 (深绿色)
    T1[Thm-S-01-01<br/>统一流计算系统的组合性]
    T2[Thm-S-01-02<br/>表达能力层次判定]
    T3[Thm-S-01-03<br/>USTM算子层完备性]

    %% 上层：引理/性质 (浅绿色)
    L1[Lemma-S-01-01<br/>USTM 完备性]
    L2[Lemma-S-01-02<br/>层次严格包含]
    L3[Lemma-S-01-03<br/>确定性条件]
    P1[Prop-S-01-01<br/>算子组合结合性]
    P2[Prop-S-01-02<br/>算子组合封闭性]

    %% 中层：定义 (紫色/橙色)
    D1[Def-S-01-01<br/>USTM 元模型]
    D2[Def-S-01-02<br/>算子层 𝒪]
    D3[Def-S-01-03<br/>算子组合 ⊗]
    D4[Def-S-01-04<br/>算子语义 ⟦·⟧ₒₚ]
    D5[Def-S-01-05<br/>算子元数 arity]
    D6[Def-S-01-06<br/>状态依赖 stateful]
    D7[Def-S-01-07<br/>表达能力层次 ℒ]
    D8[Def-S-01-08<br/>Processor]
    D9[Def-S-01-09<br/>Channel]
    D10[Def-S-01-10<br/>TimeModel]
    D11[Def-S-01-11<br/>Consistency Model]
    D12[Def-S-01-12<br/>UCM]

    %% 底层：公理/基本假设 (黄色)
    A1[Church-Turing 论题]
    A2[可判定性层次]
    A3[进程代数理论]
    A4[函数复合结合律]

    %% 依赖边：T1
    T1 -->|"接口兼容"| D1
    T1 -->|"处理单元"| D8
    T1 -->|"通道连接"| D9
    T1 -->|"一致性"| D11
    T1 -->|"模型覆盖"| L1
    T1 -->|"算子封闭"| P2

    %% 依赖边：T2
    T2 -->|"层次结构"| D7
    T2 -->|"严格包含"| L2

    %% 依赖边：T3
    T3 -->|"算子集合"| D2
    T3 -->|"组合封闭"| P2
    T3 -->|"语义等价"| D4
    T3 -->|"元数约束"| D5
    T3 -->|"拓扑排序"| D8

    %% 依赖边：引理
    L1 -->|"元模型"| D1
    L1 -->|"UCM 特化"| D12

    L2 -->|"层次"| D7
    L2 -->|"计算完备"| A1
    L2 -->|"可判定性"| A2

    L3 -->|"纯函数"| D8
    L3 -->|"FIFO 语义"| D9
    L3 -->|"时序"| D10

    %% 依赖边：性质
    P1 -->|"语义解释"| D4
    P1 -->|"函数复合结合"| A4

    P2 -->|"元数封闭"| D5
    P2 -->|"语义封闭"| D4
    P2 -->|"状态封闭"| D6

    %% 依赖边：定义
    D1 -->|"层次"| D2
    D1 -->|"算子层"| D3
    D1 -->|"状态一致"| D11
    D1 -->|"并发模型"| D12

    D2 -->|"组合算子"| D3
    D2 -->|"语义函数"| D4
    D2 -->|"元数"| D5
    D2 -->|"状态判定"| D6

    D3 -->|"语义解释"| D4
    D3 -->|"元数约束"| D5

    D12 -->|"处理单元"| D8
    D12 -->|"通信"| D9
    D12 -->|"时间"| D10

    D7 -->|"计算极限"| A1
    D7 -->|"复杂度层次"| A2

    %% 样式定义
    classDef axiom fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef definition fill:#e1bee7,stroke:#6a1b9a,stroke-width:2px
    classDef operator fill:#ffe0b2,stroke:#e65100,stroke-width:2px
    classDef lemma fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    classDef property fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    classDef theorem fill:#a5d6a7,stroke:#1b5e20,stroke-width:3px

    class A1,A2,A3,A4 axiom
    class D1,D7,D8,D9,D10,D11,D12 definition
    class D2,D3,D4,D5,D6 operator
    class L1,L2,L3 lemma
    class P1,P2 property
    class T1,T2,T3 theorem
```"""

new_73 = r"""```mermaid
graph BT
    %% 顶层：定理 (深绿色)
    T1[Thm-S-01-01<br/>统一流计算系统的组合性]
    T2[Thm-S-01-02<br/>表达能力层次判定]
    T3[Thm-S-01-03<br/>USTM算子层完备性]

    %% 上层：引理/性质 (浅绿色)
    L1[Lemma-S-01-01<br/>USTM 完备性]
    L2[Lemma-S-01-02<br/>层次严格包含]
    L3[Lemma-S-01-03<br/>确定性条件]
    P1[Prop-S-01-01<br/>算子组合结合性]
    P2[Prop-S-01-02<br/>算子组合封闭性]

    %% 中层：定义 (紫色/橙色)
    D1[Def-S-01-01<br/>USTM 元模型]
    D2[Def-S-01-02<br/>表达能力层次 ℒ]
    D3[Def-S-01-03<br/>Processor]
    D4[Def-S-01-04<br/>Channel]
    D5[Def-S-01-05<br/>TimeModel]
    D6[Def-S-01-06<br/>Consistency Model]
    D7[Def-S-01-07<br/>UCM]
    D8[Def-S-01-08<br/>算子层 𝒪]
    D9[Def-S-01-09<br/>算子组合 ⊗]
    D10[Def-S-01-10<br/>算子语义 ⟦·⟧ₒₚ]
    D11[Def-S-01-11<br/>算子元数 arity]
    D12[Def-S-01-12<br/>状态依赖 stateful]

    %% 底层：公理/基本假设 (黄色)
    A1[Church-Turing 论题]
    A2[可判定性层次]
    A3[进程代数理论]
    A4[函数复合结合律]

    %% 依赖边：T1
    T1 -->|"接口兼容"| D1
    T1 -->|"处理单元"| D3
    T1 -->|"通道连接"| D4
    T1 -->|"一致性"| D6
    T1 -->|"模型覆盖"| L1
    T1 -->|"算子封闭"| P2

    %% 依赖边：T2
    T2 -->|"层次结构"| D2
    T2 -->|"严格包含"| L2

    %% 依赖边：T3
    T3 -->|"算子集合"| D8
    T3 -->|"组合封闭"| P2
    T3 -->|"语义等价"| D10
    T3 -->|"元数约束"| D11
    T3 -->|"拓扑排序"| D3

    %% 依赖边：引理
    L1 -->|"元模型"| D1
    L1 -->|"UCM 特化"| D7

    L2 -->|"层次"| D2
    L2 -->|"计算完备"| A1
    L2 -->|"可判定性"| A2

    L3 -->|"纯函数"| D3
    L3 -->|"FIFO 语义"| D4
    L3 -->|"时序"| D5

    %% 依赖边：性质
    P1 -->|"语义解释"| D10
    P1 -->|"函数复合结合"| A4

    P2 -->|"元数封闭"| D11
    P2 -->|"语义封闭"| D10
    P2 -->|"状态封闭"| D12

    %% 依赖边：定义
    D1 -->|"层次"| D2
    D1 -->|"算子层"| D8
    D1 -->|"状态一致"| D6
    D1 -->|"并发模型"| D7

    D8 -->|"组合算子"| D9
    D8 -->|"语义函数"| D10
    D8 -->|"元数"| D11
    D8 -->|"状态判定"| D12

    D9 -->|"语义解释"| D10
    D9 -->|"元数约束"| D11

    D7 -->|"处理单元"| D3
    D7 -->|"通信"| D4
    D7 -->|"时间"| D5

    D2 -->|"计算极限"| A1
    D2 -->|"复杂度层次"| A2

    %% 样式定义
    classDef axiom fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef definition fill:#e1bee7,stroke:#6a1b9a,stroke-width:2px
    classDef operator fill:#ffe0b2,stroke:#e65100,stroke-width:2px
    classDef lemma fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    classDef property fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    classDef theorem fill:#a5d6a7,stroke:#1b5e20,stroke-width:3px

    class A1,A2,A3,A4 axiom
    class D1,D2,D3,D4,D5,D6,D7 definition
    class D8,D9,D10,D11,D12 operator
    class L1,L2,L3 lemma
    class P1,P2 property
    class T1,T2,T3 theorem
```"""

if old_73 in content:
    content = content.replace(old_73, new_73)
    print('FIXED: Figure 7.3')
else:
    print('NOT FOUND: Figure 7.3 old block')

old_76 = r"""```mermaid
graph BT
    %% 顶层：定理 (深绿色)
    T3[Thm-S-01-03<br/>USTM算子层完备性]

    %% 上层：性质 (浅绿色)
    P1[Prop-S-01-01<br/>算子组合结合性]
    P2[Prop-S-01-02<br/>算子组合封闭性]

    %% 中层：算子层定义 (橙色)
    D8[Def-S-01-08<br/>算子层 𝒪]
    D9[Def-S-01-09<br/>算子组合 ⊗]
    D10[Def-S-01-10<br/>算子语义 ⟦·⟧ₒₚ]
    D11[Def-S-01-11<br/>算子元数 arity]
    D12[Def-S-01-12<br/>状态依赖 stateful]

    %% 下层：基础定义 (紫色)
    D3[Def-S-01-08<br/>Processor]
    D4[Def-S-01-09<br/>Channel]

    %% 底层：数学公理 (黄色)
    A4[函数复合结合律]

    %% 依赖边
    T3 -->|"DAG分解"| D8
    T3 -->|"组合封闭"| P2
    T3 -->|"语义等价"| D10
    T3 -->|"拓扑排序"| D3

    P1 -->|"语义解释"| D10
    P1 -->|"函数复合结合"| A4

    P2 -->|"元数封闭"| D11
    P2 -->|"语义封闭"| D10
    P2 -->|"状态封闭"| D12

    D8 -->|"deploy映射"| D3
    D8 -->|"topology映射"| D4
    D9 -->|"诱导通道"| D4
    D10 -->|"状态语义"| D3
    D12 -->|"状态模型"| D3

    %% 样式
    classDef definition fill:#e1bee7,stroke:#6a1b9a,stroke-width:2px
    classDef operator fill:#ffe0b2,stroke:#e65100,stroke-width:2px
    classDef property fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    classDef theorem fill:#a5d6a7,stroke:#1b5e20,stroke-width:3px
    classDef axiom fill:#fff9c4,stroke:#f57f17,stroke-width:2px

    class D3,D4 definition
    class D8,D9,D10,D11,D12 operator
    class P1,P2 property
    class T3 theorem
    class A4 axiom
```"""

new_76 = r"""```mermaid
graph BT
    %% 顶层：定理 (深绿色)
    T3[Thm-S-01-03<br/>USTM算子层完备性]

    %% 上层：性质 (浅绿色)
    P1[Prop-S-01-01<br/>算子组合结合性]
    P2[Prop-S-01-02<br/>算子组合封闭性]

    %% 中层：算子层定义 (橙色)
    D8[Def-S-01-08<br/>算子层 𝒪]
    D9[Def-S-01-09<br/>算子组合 ⊗]
    D10[Def-S-01-10<br/>算子语义 ⟦·⟧ₒₚ]
    D11[Def-S-01-11<br/>算子元数 arity]
    D12[Def-S-01-12<br/>状态依赖 stateful]

    %% 下层：基础定义 (紫色)
    D3[Def-S-01-03<br/>Processor]
    D4[Def-S-01-04<br/>Channel]

    %% 底层：数学公理 (黄色)
    A4[函数复合结合律]

    %% 依赖边
    T3 -->|"DAG分解"| D8
    T3 -->|"组合封闭"| P2
    T3 -->|"语义等价"| D10
    T3 -->|"拓扑排序"| D3

    P1 -->|"语义解释"| D10
    P1 -->|"函数复合结合"| A4

    P2 -->|"元数封闭"| D11
    P2 -->|"语义封闭"| D10
    P2 -->|"状态封闭"| D12

    D8 -->|"deploy映射"| D3
    D8 -->|"topology映射"| D4
    D9 -->|"诱导通道"| D4
    D10 -->|"状态语义"| D3
    D12 -->|"状态模型"| D3

    %% 样式
    classDef definition fill:#e1bee7,stroke:#6a1b9a,stroke-width:2px
    classDef operator fill:#ffe0b2,stroke:#e65100,stroke-width:2px
    classDef property fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    classDef theorem fill:#a5d6a7,stroke:#1b5e20,stroke-width:3px
    classDef axiom fill:#fff9c4,stroke:#f57f17,stroke-width:2px

    class D3,D4 definition
    class D8,D9,D10,D11,D12 operator
    class P1,P2 property
    class T3 theorem
    class A4 axiom
```"""

if old_76 in content:
    content = content.replace(old_76, new_76)
    print('FIXED: Figure 7.6')
else:
    print('NOT FOUND: Figure 7.6 old block')

with open('Struct/01-foundation/01.01-unified-streaming-theory.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done.')
