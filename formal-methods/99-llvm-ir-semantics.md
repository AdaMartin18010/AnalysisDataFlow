# LLVM IR 的形式化语义

> **所属阶段**: Knowledge | **前置依赖**: [类型理论基础](01-foundations/05-type-theory.md), [编译器正确性](04-application-layer/06-compiler-verification/01-compiler-correctness.md) | **形式化等级**: L5

---

## 1. 概念定义 (Definitions)

### Def-K-99-14: LLVM IR (Intermediate Representation)

**LLVM IR**（Low Level Virtual Machine Intermediate Representation，低级虚拟机中间表示）是一种强类型的、低级的、通用的编译器中间表示语言。它为多种编程语言的编译器提供了一套统一的中间表示层，实现了"前端-优化器-后端"解耦的编译器架构。

形式化地，LLVM IR 可以定义为一个五元组：

$$\text{LLVM IR} := (T, V, I, F, M)$$

其中各组件定义如下：

| 组件 | 符号 | 描述 |
|------|------|------|
| **类型系统** | $T$ | LLVM IR 类型集合，包括基础类型、派生类型和聚合类型 |
| **值集合** | $V$ | SSA 形式的值集合，包括常量、变量和指令结果 |
| **指令集** | $I$ | LLVM IR 指令集合，包括运算、内存操作、控制流指令 |
| **函数集合** | $F$ | 模块中定义的函数集合，每个函数包含基本块和指令 |
| **元数据** | $M$ | 调试信息、优化提示等附加元数据 |

LLVM IR 具有以下核心特性：

1. **静态单赋值形式 (SSA)**：每个变量在程序中只被赋值一次
2. **无限虚拟寄存器**：可使用任意数量的虚拟寄存器，寄存器分配由后端优化器完成
3. **强类型系统**：所有值都有显式的类型标注
4. **三地址码风格**：大多数指令采用 `结果 = 操作 操作数1, 操作数2` 的形式
5. **平台无关性**：抽象了目标平台的硬件细节

LLVM IR 的表示层次包括：

- **内存表示 (In-Memory IR)**：编译器内部的数据结构（`llvm::Module`, `llvm::Function`, `llvm::BasicBlock`, `llvm::Instruction` 等 C++ 类）
- **位码表示 (Bitcode)**：高效的二进制序列化格式，用于存储和传输
- **文本表示 (Assembly)**：人类可读的文本格式，文件扩展名通常为 `.ll`

**LLVM IR 文本表示示例**：

```llvm
; 计算两个整数的最大值函数
define i32 @max(i32 %a, i32 %b) {
entry:
  %cmp = icmp sgt i32 %a, %b
  br i1 %cmp, label %then, label %else

then:
  ret i32 %a

else:
  ret i32 %b
}
```

**形式化类型系统**：

LLVM IR 的类型系统 $T$ 递归定义为：

$$
\begin{aligned}
t ::= & \; \texttt{void} \;|\; \texttt{i}n \; (n \in \{1, 8, 16, 32, 64, 128\}) \\
      |& \; \texttt{float} \;|\; \texttt{double} \;|\; \texttt{fp128} \\
      |& \; t^* \; \text{(指针类型)} \\
      |& \; [n \times t] \; \text{(数组类型)} \\
      |& \; \{t_1, t_2, \ldots, t_n\} \; \text{(结构体类型)} \\
      |& \; \texttt{label} \;|\; \texttt{metadata}
\end{aligned}
$$

---

### Def-K-99-15: SSA形式 (Static Single Assignment)

**SSA（Static Single Assignment，静态单赋值）** 是一种中间表示形式，要求程序中的每个变量在代码中只被赋值一次。这一形式化约束极大地简化了数据流分析，使得许多编译器优化能够更高效地实现。

**形式化定义**：

设程序 $P$ 包含变量集合 $Var$ 和赋值点集合 $Assign$，SSA 形式要求满足：

$$\forall v \in Var: |\{a \in Assign \mid \text{dest}(a) = v\}| \leq 1$$

其中 $\text{dest}(a)$ 返回赋值操作 $a$ 的目标变量。

**SSA的核心性质**：

1. **定义-使用清晰**：每个使用点（use）有唯一的定义点（def）
2. **数据流分析简化**：到达定义（reaching definition）分析可在 $O(n)$ 时间内完成
3. **优化友好**：常量传播、死代码消除、公共子表达式消除等优化在 SSA 上更为高效

**SSA构造算法——插值算法（Phi-Insertion Algorithm）**：

构造 SSA 的核心步骤包括：

1. **支配边界计算（Dominance Frontier）**：
   节点 $X$ 的支配边界 $DF(X)$ 是所有满足以下条件的节点 $Y$ 的集合：
   - $X$ 支配 $Y$ 的某个前驱节点
   - $X$ 不严格支配 $Y$

2. **PHI 节点插入**：
   对于每个变量 $v$ 在节点 $X$ 的定义，需要在 $DF(X)$ 中的所有节点插入 PHI 节点

3. **变量重命名**：
   为每个定义分配唯一的版本号，形成 $v_1, v_2, \ldots, v_n$ 系列

**SSA形式示例**：

```llvm
; 原始代码（非SSA）
; x = 5
; if (cond) x = x + 1
; y = x * 2

; SSA形式
entry:
  %x.1 = add i32 5, 0
  br i1 %cond, label %then, label %merge

then:
  %x.2 = add i32 %x.1, 1
  br label %merge

merge:
  %x.3 = phi i32 [%x.2, %then], [%x.1, %entry]
  %y = mul i32 %x.3, 2
```

**SSA形式的操作语义**：

给定环境 $\rho: Var \rightarrow Value$，SSA 指令的执行语义可定义为：

$$
\frac{\llbracket e \rrbracket_\rho = v}{\rho \vdash x = e \Downarrow \rho[x \mapsto v]}
$$

其中 $\llbracket e \rrbracket_\rho$ 表示在环境 $\rho$ 下表达式 $e$ 的求值。

---

### Def-K-99-16: 基本块 (Basic Block)

**基本块（Basic Block）** 是 LLVM IR 控制流图的基本单元，定义为一段最大长度的连续指令序列，具有以下形式化特征：

**形式化定义**：

基本块 $B$ 是一个指令序列 $(i_1, i_2, \ldots, i_n)$，满足：

1. **入口单一性**：控制流只能通过第一条指令进入 $B$
2. **出口单一性**：控制流只能通过最后一条指令离开 $B$
3. **内部连续性**：$i_1$ 到 $i_{n-1}$ 都是非控制流指令
4. **终结指令**：$i_n$ 必须是终结指令（terminator instruction）

**终结指令类型**：

| 指令 | 语法 | 语义 |
|------|------|------|
| `ret` | `ret <type> <value>` 或 `ret void` | 函数返回 |
| `br` | `br i1 <cond>, label <iftrue>, label <iffalse>` | 条件分支 |
| `br` | `br label <dest>` | 无条件跳转 |
| `switch` | `switch <intty> <value>, label <defaultdest> [<intty> <val>, label <dest>]*` | 多路分支 |
| `indirectbr` | `indirectbr <somety>* <address>, [label <dest1>, ...]` | 间接跳转 |
| `invoke` | `invoke <ty> <fn>(<args>) to label <normal> unwind label <exception>` | 异常处理调用 |
| `resume` | `resume <type> <value>` | 异常传播 |
| `unreachable` | `unreachable` | 不可达代码 |

**基本块的控制流图表示**：

基本块集合 $BB$ 构成有向图 $G = (BB, E)$，其中边 $(B_1, B_2) \in E$ 当且仅当控制流可以从 $B_1$ 转移到 $B_2$。

**基本块的形式化结构**：

$$
B := (\text{label}, P, I, T)
$$

其中：

- $\text{label}$：基本块的唯一标识符
- $P \subseteq BB$：前驱基本块集合
- $I = (i_1, \ldots, i_{n-1})$：非终结指令序列
- $T = i_n$：终结指令

**LLVM IR 基本块示例**：

```llvm
define i32 @gcd(i32 %a, i32 %b) {
entry:                          ; 基本块入口标签
  %cmp = icmp eq i32 %b, 0      ; 非终结指令
  br i1 %cmp, label %return, label %loop  ; 终结指令

loop:                           ; 另一个基本块
  %rem = srem i32 %a, %b
  %new_a = add i32 %b, 0
  %new_b = add i32 %rem, 0
  %cmp2 = icmp eq i32 %new_b, 0
  br i1 %cmp2, label %return, label %loop

return:                         ; 返回基本块
  %result = phi i32 [%a, %entry], [%new_a, %loop]
  ret i32 %result
}
```

---

### Def-K-99-17: 控制流图 (CFG)

**控制流图（Control Flow Graph, CFG）** 是表示程序控制流结构的有向图，是编译器分析和优化的核心数据结构。

**形式化定义**：

程序的控制流图是一个五元组：

$$\text{CFG} := (N, E, n_{entry}, n_{exit}, \Sigma)$$

其中：

- $N$：基本块（节点）集合
- $E \subseteq N \times N$：控制流边集合
- $n_{entry} \in N$：唯一的入口节点
- $n_{exit} \in N$：唯一的出口节点
- $\Sigma$：边上的标记（分支条件等）

**支配关系（Dominance Relation）**：

节点 $d$ 支配节点 $n$（记作 $d \text{ dom } n$），如果从 $n_{entry}$ 到 $n$ 的每条路径都经过 $d$：

$$d \text{ dom } n \iff \forall p \in \text{Paths}(n_{entry}, n): d \in p$$

**直接支配（Immediate Dominator）**：

$d$ 是 $n$ 的直接支配者（记作 $d = \text{idom}(n)$），如果：

- $d \text{ dom } n$ 且 $d \neq n$
- 不存在 $d'$ 满足 $d \text{ dom } d' \text{ dom } n$ 且 $d' \neq d, d' \neq n$

**支配树（Dominator Tree）**：

支配关系形成树结构，其中：

- 根节点是 $n_{entry}$
- $d$ 是 $n$ 的父节点当且仅当 $d = \text{idom}(n)$

**后支配（Post-Dominance）**：

节点 $p$ 后支配节点 $n$（记作 $p \text{ pdom } n$），如果从 $n$ 到 $n_{exit}$ 的每条路径都经过 $p$：

$$p \text{ pdom } n \iff \forall p' \in \text{Paths}(n, n_{exit}): p \in p'$$

**控制流图的性质**：

1. **可归约性（Reducibility）**：CFG 可归约当且仅当它可以被压缩为单个节点，且不会移除循环
2. **区间结构（Interval Structure）**：可归约 CFG 可以分解为嵌套区间
3. **循环结构（Loop Structure）**：自然循环由回边（back edge）及其支配区域确定

**循环的自然循环定义**：

给定回边 $(n \rightarrow h)$，其中 $h \text{ dom } n$，自然循环定义为：

$$\text{NaturalLoop}(n \rightarrow h) = \{h\} \cup \{m \mid \exists \text{ 路径 } p: m \leadsto n \text{ 不经过 } h\}$$

---

### Def-K-99-18: PHI节点 (PHI Node)

**PHI 节点** 是 SSA 形式的核心机制，用于合并在不同控制流路径上定义的变量版本，解决控制流汇合点（join point）处的值选择问题。

**形式化定义**：

PHI 节点是一个伪指令，形式为：

$$\phi(v_1: B_1, v_2: B_2, \ldots, v_n: B_n)$$

其中：

- $(v_i, B_i)$ 是值-基本块对
- $B_i$ 是当前基本块的前驱基本块
- 当控制流从 $B_i$ 进入时，PHI 节点选择值 $v_i$

**PHI 节点的形式化语义**：

设当前基本块为 $B$，其前驱集合为 $\text{Pred}(B)$，PHI 节点 $\phi_i$ 定义为：

$$\phi_i = \phi(v_{i,1}: B_1, v_{i,2}: B_2, \ldots, v_{i,k}: B_k)$$

其中 $\{B_1, \ldots, B_k\} = \text{Pred}(B)$。

执行语义为：

$$\llbracket \phi_i \rrbracket_{B_j} = v_{i,j} \quad \text{if 控制流从 } B_j \text{ 到达}$$

**PHI 节点的类型规则**：

1. **类型一致性**：所有 $v_{i,j}$ 必须具有相同的 LLVM IR 类型
2. **完整性**：对于每个前驱基本块 $B_j \in \text{Pred}(B)$，必须恰好有一个对应的值
3. **位置约束**：PHI 节点必须位于基本块的最开始，在任何非 PHI 指令之前

**PHI 节点的插入算法**：

```
算法: 最小PHI插入
输入: 变量v的定义点集合Defs(v)
输出: 需要插入PHI节点的位置

1. 计算DF+(Defs(v)): 定义点的迭代支配边界闭包
2. 对于每个节点n ∈ DF+(Defs(v)):
   在n处插入PHI节点: v = φ(v, v, ..., v)
3. 重命名变量，为每个定义和PHI节点分配唯一版本号
```

**PHI 节点的直观理解**：

PHI 节点可以看作是控制流的选择器。当多个控制流路径汇合时，PHI 节点根据"从哪个路径来"选择相应的值。

```llvm
; 示例：if-else结构
entry:
  %x.0 = add i32 1, 0
  %cond = icmp sgt i32 %n, 0
  br i1 %cond, label %then, label %else

then:
  %x.1 = add i32 %x.0, 10
  br label %merge

else:
  %x.2 = sub i32 %x.0, 5
  br label %merge

merge:
  %x.3 = phi i32 [%x.1, %then], [%x.2, %else]
  ; 如果来自then块，选择%x.1
  ; 如果来自else块，选择%x.2
  ret i32 %x.3
```

---

### Def-K-99-19: 内存模型 (Memory Model)

**LLVM IR 内存模型** 定义了内存访问操作（load/store）的语义，包括内存位置、对齐要求、易变性以及并发访问行为。

**形式化定义**：

内存模型 $Mem$ 是一个三元组：

$$Mem := (Addr, Val, \text{State})$$

其中：

- $Addr$：内存地址空间（通常是 $[0, 2^{64})$ 或 $[0, 2^{32})$）
- $Val$：可存储的值集合
- $\text{State}: Addr \rightharpoonup Val$：部分映射，表示当前内存状态

**内存访问指令**：

| 指令 | 语法 | 操作语义 |
|------|------|----------|
| `alloca` | `%ptr = alloca <type>, align <n>` | 在栈上分配空间，返回指针 |
| `load` | `%val = load <type>, <type>* %ptr, align <n>` | 从内存读取值 |
| `store` | `store <type> %val, <type>* %ptr, align <n>` | 向内存写入值 |
| `getelementptr` | `%ptr = getelementptr <type>, <type>* %base, <idx>...` | 计算元素地址 |

**内存模型特性**：

1. **类型双关（Type-Based Alias Analysis, TBAA）**：
   LLVM 利用类型信息优化内存别名分析。基于类型的别名规则（TBAA）假设不同类型的指针不别名：

   $$\text{type}(p_1) \neq \text{type}(p_2) \Rightarrow \neg \text{alias}(p_1, p_2)$$

2. **对齐要求（Alignment）**：
   内存访问可以指定对齐要求，对齐的访问可能比未对齐的访问更高效：

   $$\text{aligned}(addr, n) \iff addr \mod n = 0$$

3. **易变性（Volatility）**：
   `volatile` 关键字禁止对内存访问进行某些优化：
   - 易变 load 不能被删除或合并
   - 易变 store 不能被删除或移动

4. **原子性（Atomicity）**：
   LLVM IR 支持原子内存操作，用于并发编程：

   ```llvm
   %val = load atomic i32, i32* %ptr unordered, align 4
   store atomic i32 %val, i32* %ptr release, align 4
   %old = cmpxchg i32* %ptr, i32 %cmp, i32 %new seq_cst seq_cst
   ```

**内存序（Memory Ordering）**：

| 排序级别 | C++ 等价 | 语义 |
|----------|----------|------|
| `unordered` | 无 | 最弱排序，允许任意重排 |
| `monotonic` | `memory_order_relaxed` | 保证原子性，无顺序保证 |
| `acquire` | `memory_order_acquire` | 读-获取：之后的读写不能重排到之前 |
| `release` | `memory_order_release` | 写-释放：之前的读写不能重排到之后 |
| `acq_rel` | `memory_order_acq_rel` | 读-修改-写操作：acquire + release |
| `seq_cst` | `memory_order_seq_cst` | 顺序一致性：全序关系 |

**地址计算——GetElementPtr (GEP)**：

GEP 指令的形式化语义：

$$\text{GEP}(base, idx_1, idx_2, \ldots, idx_n) = base + \sum_{i=1}^{n} idx_i \times \text{sizeof}(\text{type}_i)$$

其中 $\text{type}_i$ 是经过前 $i-1$ 个索引后的元素类型。

---

### Def-K-99-20: 未定义行为 (Undefined Behavior)

**未定义行为（Undefined Behavior, UB）** 是指程序中某些操作的语义在语言规范中未定义，编译器可以对这些操作做出任意假设以进行优化。

**形式化定义**：

设程序状态空间为 $\Sigma$，操作 $op$ 在状态 $\sigma \in \Sigma$ 下具有未定义行为，记作：

$$\text{UB}_{op}(\sigma) \iff \nexists \sigma' \in \Sigma: \sigma \xrightarrow{op} \sigma'$$

即不存在定义良好的后继状态。

**LLVM IR 中的未定义行为分类**：

| 类别 | 示例 | 优化利用 |
|------|------|----------|
| **算术 UB** | 有符号整数溢出、除零 | 假设不发生以优化算术 |
| **内存 UB** | 空指针解引用、越界访问 | 假设指针有效以优化内存操作 |
| **控制流 UB** | 返回无值、unreachable 后的代码 | 删除不可达代码 |
| **并发 UB** | 数据竞争 | 假设无竞争以优化同步 |

**LLVM IR 中的未定义值（Undefined Value）**：

`undef` 是一个特殊的值，表示"任意值"，编译器可以选择对它最有利的值：

```llvm
; undef 可以用于优化
%mask = and i32 %x, undef  ; 可以优化为 %mask = 0
```

`undef` 的形式化语义：

$$\llbracket \text{undef} \rrbracket = \{v \mid v \in \text{Type}_{\text{range}}\}$$

即 `undef` 表示该类型的所有可能值。

**未定义行为的编译器利用**：

1. **优化基础**：编译器假设 UB 不发生，可以推导更强的不变量
2. **值范围推断**：假设无溢出，可以推断整数的精确范围
3. **死代码消除**：UB 之后的代码可以删除

**示例：UB 导致的意外优化**：

```c
// 原始 C 代码
int foo(int x) {
    if (x > x + 1)  // 有符号溢出是 UB
        return 1;
    return 0;
}

// 优化后的 LLVM IR（假设无溢出）
define i32 @foo(i32 %x) {
  ret i32 0  ; 条件恒为假，被优化掉
}
```

**Poison Value（毒值）**：

LLVM 引入 `poison` 值表示"已触发 UB 但尚未传播"的状态：

- 某些操作产生 poison（如溢出）
- poison 传播：大多数操作接受 poison 输入会产生 poison 输出
- 与 `undef` 不同：poison 会触发 UB 当用于某些上下文（如分支条件）

**形式化语义**：

$$
\llbracket \text{poison} \rrbracket = \bot \quad (\text{部分计算})
$$

$$
\text{inst}(\ldots, \text{poison}, \ldots) = \text{poison} \quad (\text{大多数指令})
$$

$$\text{br } \text{poison} = \text{UB} \quad (\text{分支条件})
$$


---

## 2. 属性推导 (Properties)

### Lemma-K-99-08: SSA的支配性质

**引理（SSA支配性质）**：在 SSA 形式的程序中，变量 $v$ 的定义点 $d_v$ 支配 $v$ 的所有使用点 $u_v$：

$$\forall v \in Var: \forall u \in \text{Uses}(v): d_v \text{ dom } u$$

**证明**：

假设存在使用点 $u$ 不被 $d_v$ 支配。根据支配定义，存在一条从入口到 $u$ 的路径不经过 $d_v$。

在 SSA 形式中，变量的值由其定义点的求值结果决定。如果存在到达 $u$ 的路径不经过 $d_v$，则在该路径上 $v$ 未被定义，导致 $v$ 在 $u$ 处无定义值可用。

这与 SSA 的不变式矛盾（SSA 要求每个使用都有定义），因此假设不成立，$d_v$ 必须支配所有使用点。

**推论**：

1. **支配树性质**：变量的定义-使用链形成支配树的子树
2. **支配边界与PHI节点**：PHI 节点只插入在定义点的支配边界处
3. **优化安全性**：基于支配信息的优化（如代码提升）在 SSA 上更安全

**应用——全局值编号（GVN）**：

SSA 支配性质使得全局值编号可以在线性时间内完成：

```
算法: 支配树遍历GVN
输入: SSA形式的CFG
输出: 每个值的唯一编号

1. 构建支配树
2. 按支配树先序遍历每个基本块
3. 对于每个指令:
   a. 如果其操作数和操作组合已在当前作用域中出现
      则该指令与前一个等价，可被替换
   b. 否则，分配新编号并加入作用域
4. 退出基本块时，恢复作用域状态
```

---

### Lemma-K-99-09: PHI节点的合流性质

**引理（PHI节点合流性质）**：在 SSA 形式中，PHI 节点的参数版本集合恰好是各前驱基本块出口处活跃变量的定义版本集合。

形式化地，设 PHI 节点定义变量 $v$ 在基本块 $B$：

$$v = \phi(v_1: B_1, v_2: B_2, \ldots, v_k: B_k)$$

则对于每个 $i \in [1, k]$：

$$v_i = \text{LiveDef}(B_i, v)$$

其中 $\text{LiveDef}(B_i, v)$ 表示在 $B_i$ 出口处 $v$ 的最新定义版本。

**证明**：

根据 SSA 构造算法（Cytron 等人的算法）：

1. **PHI 插入**：PHI 节点仅插入在支配边界节点，这些节点恰好是多个定义汇合的控制流汇合点
2. **变量重命名**：重命名阶段跟踪每个变量在控制流路径上的当前版本
3. **参数选择**：对于每个前驱 $B_i$，PHI 节点选择 $B_i$ 中该变量的最新定义（栈顶）

因此，PHI 参数精确反映了各前驱路径上的定义版本。

**应用——SSA 解构**：

当从 SSA 形式转换回可执行代码时（SSA 解构），需要消除 PHI 节点：

```
算法: 传统SSA解构
输入: SSA形式的CFG（含PHI节点）
输出: 非SSA形式的可执行代码

1. 对于每个PHI节点 v = φ(v₁:B₁, v₂:B₂, ..., vₖ:Bₖ):
   a. 为v分配物理寄存器/内存位置
   b. 在每个前驱Bᵢ的末尾插入拷贝: v = vᵢ
2. 删除所有PHI节点
3. 进行寄存器分配
```

**并行拷贝问题**：

当多个 PHI 节点在同一个基本块时，它们的输入拷贝必须并行执行：

```llvm
; 原始PHI节点
merge:
  %x = phi i32 [%a1, %B1], [%a2, %B2]
  %y = phi i32 [%b1, %B1], [%b2, %B2]

; 如果在B1末尾插入顺序拷贝（错误！）
B1:
  ; ...
  %x = %a1    ; 这会覆盖%a1，如果%y依赖于原始的%x
  %y = %b1
```

正确的处理需要**并行拷贝**或引入临时变量。

---

### Lemma-K-99-10: 类型安全性

**引理（LLVM IR 类型安全性）**：良类型的（well-typed）LLVM IR 程序满足以下类型安全性：

1. **进展（Progress）**：每个良类型的非值表达式要么是一个值，要么可以进一步求值
2. **保持（Preservation）**：如果表达式 $e$ 具有类型 $\tau$ 且 $e \rightarrow e'$，则 $e'$ 也具有类型 $\tau$

**形式化表述**：

**进展**：

$$\vdash e : \tau \Rightarrow e \in Value \;\lor\; \exists e': e \rightarrow e'$$

**保持**：

$$\vdash e : \tau \land e \rightarrow e' \Rightarrow \vdash e' : \tau$$

**LLVM IR 的类型规则**：

**常量类型规则**：

$$
\frac{n \in \mathbb{Z} \land -2^{w-1} \leq n < 2^{w-1}}{\vdash n : \texttt{i}w}
$$

**二元运算类型规则**：

$$
\frac{\vdash e_1 : \tau \quad \vdash e_2 : \tau \quad \tau \in \{\texttt{i}w, \texttt{float}, \texttt{double}\}}{\vdash e_1 \oplus e_2 : \tau}
$$

**加载指令类型规则**：

$$
\frac{\vdash p : \tau*}{\vdash \texttt{load } p : \tau}
$$

**PHI 节点类型规则**：

$$
\frac{\forall i: \vdash v_i : \tau}{\vdash \phi(v_1:B_1, v_2:B_2, \ldots) : \tau}
$$

**类型安全性与优化**：

类型安全性保证了优化变换的合法性：

- 类型正确的变换保持程序的良类型性
- 类型信息指导 TBAA（基于类型的别名分析）
- 类型推导支持更激进的优化

---

### Prop-K-99-03: SSA的等价变换保持语义

**命题（SSA等价变换语义保持）**：在 SSA 形式上执行的规范优化变换保持程序的观察语义（observational semantics）。

**形式化表述**：

设变换 $T$ 将程序 $P$ 转换为 $P'$，$T$ 是语义保持的当且仅当：

$$P \approx_{obs} P'$$

即对于所有输入 $in$ 和观察 $obs$：

$$\text{obs}(\llbracket P \rrbracket(in)) = \text{obs}(\llbracket P' \rrbracket(in))$$

**常见SSA优化及其语义保持性**：

| 优化 | 描述 | 语义保持条件 |
|------|------|--------------|
| **常量传播** | 用常量值替换变量 | 被替换变量确实具有该常量值 |
| **死代码消除** | 删除无副作用的未使用指令 | 不影响观察行为 |
| **全局值编号** | 消除冗余计算 | 替换值在支配关系下等价 |
| **强度削弱** | 用廉价操作替代昂贵操作 | 数值等价 |
| **循环不变量外提** | 将循环内不变计算移出循环 | 保证每次迭代值相同 |
| **函数内联** | 用函数体替换调用点 | 保持调用约定 |

**证明框架——模拟关系**：

要证明优化 $T$ 的语义保持性，可以构造源程序 $P$ 和目标程序 $P'$ 状态之间的模拟关系 $R$：

1. **初始状态相关**：$\sigma_0 \mathrel{R} \sigma'_0$
2. **步骤保持**：$\sigma \mathrel{R} \sigma' \land \sigma \rightarrow \sigma_1 \Rightarrow \exists \sigma'_1: \sigma' \rightarrow^* \sigma'_1 \land \sigma_1 \mathrel{R} \sigma'_1$
3. **终止状态相关**：终止状态的观察等价

**示例：常量传播的语义保持性证明**：

```llvm
; 优化前
entry:
  %x = add i32 5, 0
  %y = mul i32 %x, 2
  ret i32 %y

; 优化后（常量传播）
entry:
  %x = add i32 5, 0
  %y = mul i32 5, 2   ; %x 被替换为 5
  ret i32 %y
```

证明：在 `%y` 的定义点，根据 SSA 性质，`%x` 的定义唯一且值为 5。因此替换保持语义。

---

## 3. 关系建立 (Relations)

### 与抽象语法树(AST)的关系

**LLVM IR 与 AST 的映射关系** 描述了从高级语言表示到低级中间表示的转换过程。

**结构映射**：

| AST 结构 | LLVM IR 表示 | 说明 |
|----------|--------------|------|
| 函数声明/定义 | `declare` / `define` | 直接对应 |
| 复合语句 | 基本块序列 | 控制流扁平化 |
| 表达式 | SSA 指令序列 | 引入临时变量 |
| 局部变量 | `alloca` + `load`/`store` 或纯 SSA 值 | 取决于 mem2reg 优化 |
| 控制结构 | 条件/无条件分支 | 结构化为 CFG |

**从 AST 到 LLVM IR 的转换示例**：

```c
// C 语言源代码
int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; i++) {
        result = result * i;
    }
    return result;
}
```

```llvm
; 对应的 LLVM IR（SSA 形式）
define i32 @factorial(i32 %n) {
entry:
  %cmp = icmp slt i32 %n, 2
  br i1 %cmp, label %return, label %loop.preheader

loop.preheader:
  br label %loop

loop:
  %i = phi i32 [ 2, %loop.preheader ], [ %i.next, %loop ]
  %result = phi i32 [ 1, %loop.preheader ], [ %result.next, %loop ]
  %result.next = mul i32 %result, %i
  %i.next = add i32 %i, 1
  %cmp.loop = icmp sle i32 %i.next, %n
  br i1 %cmp.loop, label %loop, label %return

return:
  %result.final = phi i32 [ 1, %entry ], [ %result.next, %loop ]
  ret i32 %result.final
}
```

**转换关键步骤**：

1. **控制流扁平化**：将嵌套结构转换为基本块和分支
2. **变量提升**：将可变局部变量转换为 SSA 形式
3. **类型降级**：将高级类型映射到 LLVM IR 类型
4. **运行时支持**：插入异常处理、栈展开等支持代码

---

### 与机器码的关系

**LLVM IR 与机器码的映射** 描述了从平台无关中间表示到目标平台指令的转换。

**抽象层次对比**：

| 特性 | LLVM IR | 机器码 (x86-64) |
|------|---------|-----------------|
| **寄存器** | 无限虚拟寄存器 (`%name`) | 有限物理寄存器 (`%rax`, `%rbx`, ...) |
| **类型** | 显式类型系统 | 隐式（操作数大小决定） |
| **控制流** | 基本块和标签 | 指令地址和跳转偏移 |
| **内存** | 抽象内存模型 | 物理地址空间 |
| **调用约定** | 抽象 | 平台特定（System V AMD64 ABI, Windows x64 等） |

**从 LLVM IR 到机器码的编译阶段**：

```
LLVM IR
   ↓
SelectionDAG (有向无环图)
   ↓
机器指令选择 (Instruction Selection)
   ↓
机器SSA (Machine SSA)
   ↓
寄存器分配 (Register Allocation)
   ↓
机器代码 (Machine Code)
   ↓
汇编/二进制输出
```

**寄存器分配问题**：

将无限虚拟寄存器映射到有限物理寄存器是一个图着色问题：

- **干扰图（Interference Graph）**：节点是虚拟寄存器，边表示同时活跃的寄存器
- **图着色**：为图着色使得相邻节点颜色不同（每种颜色代表一个物理寄存器）
- **溢出（Spilling）**：当颜色不足时，将值存入内存（栈）

---

### 与C语言语义的关系

**LLVM IR 作为 C 语言的编译目标**，其语义与 C 语言有紧密联系但存在重要差异。

**语义对应关系**：

| C 语言概念 | LLVM IR 表示 | 差异说明 |
|------------|--------------|----------|
| 变量 | SSA 值或 `alloca` | C 变量可变，LLVM 倡导不可变 SSA 值 |
| 指针 | `i8*` 或具体类型指针 | LLVM 指针类型更严格 |
| 数组 | `[n x type]` | LLVM 数组大小是类型的一部分 |
| 结构体 | `{type1, type2, ...}` | 需要显式布局和对齐 |
| 控制流 | 分支指令 | 无结构化控制流（无循环语句） |
| 函数调用 | `call` 指令 | 支持尾调用优化标记 |

**未定义行为的差异**：

```c
// C 代码
int f(int* p) {
    int x = *p;     // 如果 p 为 NULL，UB
    if (p == NULL)  // 这个检查在优化后可能失效！
        return 0;
    return x;
}
```

```llvm
; 优化后的 LLVM IR
define i32 @f(i32* %p) {
  %x = load i32, i32* %p      ; 编译器假设 p 非 NULL
  ret i32 %x                  ; NULL 检查被删除
}
```

**C 标准 vs LLVM IR UB**：

- **C 标准 UB**：源语言级别的未定义行为
- **LLVM IR UB**：中间表示级别的优化假设
- **编译器优化**：将 C UB 转化为 LLVM IR UB 以进行激进优化

**内存模型的关系**：

- **C 内存模型**：相对抽象，依赖实现定义的行为
- **LLVM 内存模型**：更具体，定义了 TBAA、原子操作等
- **编译器桥梁**：Clang 将 C 内存操作映射到 LLVM IR，同时保留足够的语义信息

---

### 与Vellvm项目的关系

**Vellvm（Verified LLVM）** 是一个在 Coq 证明助手中对 LLVM IR 进行形式化建模和验证的研究项目，旨在提高编译器优化的可靠性。

**Vellvm 项目概述**：

| 属性 | 内容 |
|------|------|
| **首次发表** | POPL 2012 [^4] |
| **扩展版本** | ICFP 2021 [^5] |
| **实现语言** | Coq |
| **目标** | 证明 LLVM 优化的正确性 |
| **状态** | 活跃研究项目 |

**Vellvm 的形式化框架**：

Vellvm 提供了 LLVM IR 的深嵌入（deep embedding）形式化：

1. **语法形式化**：在 Coq 中定义 LLVM IR 的抽象语法
2. **操作语义**：定义小步操作语义
3. **类型系统**：形式化 LLVM IR 的类型规则
4. **验证优化**：证明具体优化的语义保持性

**Vellvm 语义层次**：

```
层次3: 优化后的 LLVM IR（SSA 形式）
   ↓ 验证变换的正确性
层次2: LLVM IR 内存模型（含 load/store）
   ↓ 验证内存操作的正确性
层次1: LLVM IR 核心语义（纯 SSA）
   ↓ 验证基本指令的语义
层次0: 抽象机器模型
```

**Vellvm 验证的优化示例**：

- **常量传播**：证明替换保持语义
- **死代码消除**：证明删除无副作用的代码保持观察语义
- **内存到寄存器提升（mem2reg）**：证明将内存操作转换为 SSA 值保持语义

**Vellvm 的意义**：

1. **填补形式化空白**：LLVM 本身缺乏完整的形式化语义
2. **验证基础设施**：为 LLVM 优化验证提供基础框架
3. **错误发现**：在形式化过程中发现 LLVM 的实现缺陷
