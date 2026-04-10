```mermaid
graph TB
  subgraph types[类型理论 谱系]
    L0_Def_F_01_01[类型构造器层级]:::root
    L0_Def_F_01_02[System Fω 类型]:::root
    L0_Def_F_01_04[高阶类型实例]:::root
    L0_Def_F_01_05[依赖函数类型 ($\Pi$-类型)]:::root
    L0_Def_F_01_06[依赖对类型 ($\Sigma$-类型)]:::root
    L0_Def_F_01_07[归纳类型定义]:::root
    L0_Def_F_01_08[共归纳类型]:::root
    L0_Def_F_01_09[LF 类型层级]:::root
    L1_Def_F_05_40[多通道会话类型]:::derived
    L1_Def_F_05_15[共归纳类型]:::derived
    L1_Def_F_07_06[Hindley-Milner 类型系统]:::derived
    L1_Def_F_07_23[多态类型方案]:::derived
    L1_Def_F_09_02[子类型上下文]:::derived
    L1_Def_F_09_21[有界多态系统 (System F<:)]:::derived
    L2_Def_F_05_13[高阶类型实例]:::applied
    L0_Def_F_01_08 --> L2_Def_F_05_13
    L1_Def_F_05_15 --> L2_Def_F_05_13
  end
  classDef root fill:#e1f5fe,stroke:#01579b,stroke-width:2px
  classDef derived fill:#fff3e0,stroke:#e65100,stroke-width:1px
  classDef applied fill:#f3e5f5,stroke:#4a148c,stroke-width:1px
```
