# Mermaid语法修复报告

**生成时间**: 2026-04-10 20:14:38

## 摘要

- 处理文件数: 6
- 修改文件数: 6
- Mermaid代码块数: 25
- 修复问题数: 0

## 修复详情


### formal-methods\99-probabilistic-programming.md

- Mermaid代码块: 4
- 修复数量: 18

**箭头空格修复** (18处):

- 行853: `-->` → `PCHL -->|扩展概率选择| PPHL`
- 行853: `-->` → `PCHL -->|扩展概率选择| PPHL`
- 行854: `-->` → `PPHL -->|增加推导能力| EXT`
- 行854: `-->` → `PPHL -->|增加推导能力| EXT`
- 行923: `-->` → `A1 -->|路径聚合| B1`
- 行923: `-->` → `A1 -->|路径聚合| B1`
- 行924: `-->` → `A2 -->|采样解释| B2`
- 行924: `-->` → `A2 -->|采样解释| B2`
- 行925: `-->` → `B1 -->|分布解释| C1`
- 行925: `-->` → `B1 -->|分布解释| C1`
- ... 还有 8 处


### formal-methods\99-homotopy-type-theory.md

- Mermaid代码块: 4
- 修复数量: 118

**箭头空格修复** (106处):

- 行842: `-->` → `Contr --> Prop`
- 行842: `-->` → `Contr --> Prop`
- 行843: `-->` → `Prop --> Set`
- 行843: `-->` → `Prop --> Set`
- 行844: `-->` → `Set --> Groupoid`
- 行844: `-->` → `Set --> Groupoid`
- 行845: `-->` → `Groupoid --> Infinite`
- 行845: `-->` → `Groupoid --> Infinite`
- 行847: `-->` → `Unit --> Contr`
- 行847: `-->` → `Unit --> Contr`
- ... 还有 96 处

**双向箭头修复** (12处):

- 行967: `<-->` → `TT_Type <-->|解释| Top_Space`
- 行968: `<-->` → `TT_Type <-->|实现| Inf_Obj`
- 行970: `<-->` → `TT_Elem <-->|解释| Top_Point`
- 行971: `<-->` → `TT_Elem <-->|实现| Inf_0Cell`
- 行973: `<-->` → `TT_Path <-->|解释| Top_Path`
- 行974: `<-->` → `TT_Path <-->|实现| Inf_1Cell`
- 行976: `<-->` → `TT_Path2 <-->|解释| Top_Hom`
- 行977: `<-->` → `TT_Path2 <-->|实现| Inf_2Cell`
- 行979: `<-->` → `TT_Trans <-->|解释| Top_Lift`
- 行980: `<-->` → `TT_Trans <-->|实现| Inf_Funct`
- ... 还有 2 处


### formal-methods\99-game-semantics.md

- Mermaid代码块: 4
- 修复数量: 32

**箭头空格修复** (30处):

- 行943: `-->` → `C1 -->|"τ 响应"| B1`
- 行943: `-->` → `C1 -->|"τ 响应"| B1`
- 行944: `-->` → `B1 -->|"σ 提出"| A1`
- 行944: `-->` → `B1 -->|"σ 提出"| A1`
- 行945: `-->` → `A1 -->|"O 行动"| A2`
- 行945: `-->` → `A1 -->|"O 行动"| A2`
- 行946: `-->` → `A2 -->|"σ 回答"| B2`
- 行946: `-->` → `A2 -->|"σ 回答"| B2`
- 行947: `-->` → `B2 -->|"τ 回答"| C2`
- 行947: `-->` → `B2 -->|"τ 回答"| C2`
- ... 还有 20 处

**点线箭头修复** (2处):

- 行1009: `-.->` → `DS1 -.->|"不完全抽象问题"| DS3`
- 行1010: `-.->` → `GS1 -.->|"解决完全抽象"| GS2`


### formal-methods\99-kubernetes-scheduler.md

- Mermaid代码块: 3
- 修复数量: 118

**箭头空格修复** (118处):

- 行1166: `-->` → `A[Pod 创建] --> B{准入控制}`
- 行1166: `-->` → `A[Pod 创建] --> B{准入控制}`
- 行1167: `-->` → `B -->|通过| C[添加到调度队列]`
- 行1167: `-->` → `B -->|通过| C[添加到调度队列]`
- 行1168: `-->` → `B -->|拒绝| D[返回错误]`
- 行1168: `-->` → `B -->|拒绝| D[返回错误]`
- 行1170: `-->` → `C --> E[从队列取出 Pod]`
- 行1170: `-->` → `C --> E[从队列取出 Pod]`
- 行1171: `-->` → `E --> F[获取集群状态快照]`
- 行1171: `-->` → `E --> F[获取集群状态快照]`
- ... 还有 108 处


### formal-methods\99-raft-consensus.md

- Mermaid代码块: 3
- 修复数量: 65

**箭头空格修复** (64处):

- 行1715: `-->` → `[*] --> Follower: 初始化`
- 行1715: `-->` → `[*] --> Follower: 初始化`
- 行1717: `-->` → `Follower --> Candidate: 选举超时`
- 行1717: `-->` → `Follower --> Candidate: 选举超时`
- 行1718: `-->` → `Candidate --> Leader: 获得多数票`
- 行1718: `-->` → `Candidate --> Leader: 获得多数票`
- 行1719: `-->` → `Candidate --> Follower: 发现更高任期`
- 行1719: `-->` → `Candidate --> Follower: 发现更高任期`
- 行1720: `-->` → `Candidate --> Candidate: 选举超时（新任期）`
- 行1720: `-->` → `Candidate --> Candidate: 选举超时（新任期）`
- ... 还有 54 处

**开放箭头修复** (1处):

- 行1856: `-->>` → `L-->>C: 响应成功`


### formal-methods\99-llvm-ir-semantics.md

- Mermaid代码块: 7
- 修复数量: 89

**箭头空格修复** (86处):

- 行2018: `-->` → `Entry -->|cond = true| Then[then<br/>ret i32 %a]`
- 行2018: `-->` → `Entry -->|cond = true| Then[then<br/>ret i32 %a]`
- 行2019: `-->` → `Entry -->|cond = false| Else[else<br/>ret i32 %b]`
- 行2019: `-->` → `Entry -->|cond = false| Else[else<br/>ret i32 %b]`
- 行2032: `-->` → `E[entry<br/>%cmp = icmp sle i32 %n, 1] -->|n <= 1| R[return<br/>ret i32 1]`
- 行2032: `-->` → `E[entry<br/>%cmp = icmp sle i32 %n, 1] -->|n <= 1| R[return<br/>ret i32 1]`
- 行2033: `-->` → `E -->|n > 1| LP[loop.preheader]`
- 行2033: `-->` → `E -->|n > 1| LP[loop.preheader]`
- 行2034: `-->` → `LP --> L[loop<br/>%i = phi [2, LP], [%i.next, L]<br/>%result = phi [1, LP], [%mul, L]]`
- 行2034: `-->` → `LP --> L[loop<br/>%i = phi [2, LP], [%i.next, L]<br/>%result = phi [1, LP], [%mul, L]]`
- ... 还有 76 处

**点线箭头修复** (3处):

- 行2147: `-.->` → `C -.->|依赖| K`
- 行2148: `-.->` → `G -.->|依赖| L`
- 行2149: `-.->` → `G -.->|依赖| M`
