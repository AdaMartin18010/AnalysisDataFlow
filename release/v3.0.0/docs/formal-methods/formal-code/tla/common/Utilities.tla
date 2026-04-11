------------------------------- MODULE Utilities -------------------------------
(******************************************************************************)
(* 通用工具模块                                                                *)
(*                                                                            *)
(* 提供集合操作、序列操作等辅助函数                                             *)
(*                                                                            *)
(* 使用方法: EXTENDS common.Utilities                                          *)
(*                                                                            *)
(* 所属阶段: Struct/ | 形式化等级: L5                                          *)
(******************************************************************************)

------------------------------------------------------------------------------
(* 导入基础模块 *)
EXTENDS Naturals, Sequences, FiniteSets

------------------------------------------------------------------------------
(*============================================================================*)
(* 集合操作辅助函数                                                            *)
(*============================================================================*)

(* 从非空集合中选择一个元素（确定性选择） *)
CHOOSE_ONE(S) == CHOOSE x \in S : TRUE

(* 集合的任意元素（用于存在性证明） *)
SOME_ELEMENT(S) == CHOOSE x \in S : TRUE

(* 判断集合是否为单元素集合 *)
IsSingleton(S) == \E x \in S : S = {x}

(* 获取单元素集合的唯一元素 *)
TheElement(S) == CHOOSE x \in S : S = {x}

(* 集合的幂集（有限集合的所有子集） *)
PowerSet(S) == { T \in SUBSET S : TRUE }

(* 非空子集集合 *)
NonEmptySubsets(S) == { T \in SUBSET S : T # {} }

(* 集合的最大元素（假设集合元素为自然数且非空） *)
Max(S) == CHOOSE x \in S : \A y \in S : x >= y

(* 集合的最小元素（假设集合元素为自然数且非空） *)
Min(S) == CHOOSE x \in S : \A y \in S : x <= y

(* 两个集合的笛卡尔积 *)
CartesianProduct(S, T) == { <<x, y>> : x \in S, y \in T }

(* 集合元素个数（基数） *)
Cardinaltiy(S) == 
  IF S = {} THEN 0
  ELSE 1 + Cardinaltiy({ x \in S : x # CHOOSE_ONE(S) })

------------------------------------------------------------------------------
(*============================================================================*)
(* 序列操作辅助函数                                                            *)
(*============================================================================*)

(* 序列是否为空 *)
IsEmpty(seq) == seq = << >>

(* 序列长度（别名，与 Len 相同） *)
Length(seq) == Len(seq)

(* 获取序列的最后一个元素 *)
Last(seq) == seq[Len(seq)]

(* 获取序列除最后一个元素外的所有元素 *)
AllButLast(seq) == [ i \in 1..(Len(seq)-1) |-> seq[i] ]

(* 序列的前缀判断：seq1 是 seq2 的前缀 *)
IsPrefix(seq1, seq2) ==
  /\ Len(seq1) <= Len(seq2)
  /\ \A i \in 1..Len(seq1) : seq1[i] = seq2[i]

(* 序列追加单个元素（与 Append 相同，提供语义清晰的别名） *)
Add(seq, elem) == Append(seq, elem)

(* 序列合并：将 seq2 追加到 seq1 后 *)
Concat(seq1, seq2) == seq1 \o seq2

(* 反转序列 *)
Reverse(seq) ==
  [ i \in 1..Len(seq) |-> seq[Len(seq) - i + 1] ]

(* 获取序列中某个元素的所有索引位置 *)
IndexesOf(seq, elem) ==
  { i \in 1..Len(seq) : seq[i] = elem }

(* 序列是否包含某个元素 *)
Contains(seq, elem) ==
  \E i \in 1..Len(seq) : seq[i] = elem

(* 统计元素在序列中出现次数 *)
Count(seq, elem) ==
  Cardinaltiy({ i \in 1..Len(seq) : seq[i] = elem })

(* 序列去重（保留首次出现的顺序） *)
Unique(seq) ==
  LET RemoveDuplicates(i) ==
    IF i > Len(seq) THEN << >>
    ELSE IF Contains(RemoveDuplicates(i+1), seq[i]) 
         THEN RemoveDuplicates(i+1)
         ELSE << seq[i] >> \o RemoveDuplicates(i+1)
  IN RemoveDuplicates(1)

(* 序列映射：对序列每个元素应用函数 f *)
Map(seq, f(_)) ==
  [ i \in 1..Len(seq) |-> f(seq[i]) ]

(* 序列过滤：保留满足条件的元素 *)
Filter(seq, P(_)) ==
  LET FilterHelper(i) ==
    IF i > Len(seq) THEN << >>
    ELSE IF P(seq[i]) THEN << seq[i] >> \o FilterHelper(i+1)
         ELSE FilterHelper(i+1)
  IN FilterHelper(1)

(* 序列折叠/归约：左折叠 *)
FoldLeft(seq, base, f(_, _)) ==
  LET FoldHelper(i, acc) ==
    IF i > Len(seq) THEN acc
    ELSE FoldHelper(i+1, f(acc, seq[i]))
  IN FoldHelper(1, base)

------------------------------------------------------------------------------
(*============================================================================*)
(* 函数/记录操作辅助函数                                                       *)
(*============================================================================*)

(* 函数定义域（Domain 的别名） *)
Domain(f) == DOMAIN f

(* 函数值域 *)
Range(f) == { f[x] : x \in DOMAIN f }

(* 函数限制：将函数限制在子域上 *)
Restrict(f, subDomain) ==
  [ x \in subDomain |-> f[x] ]

(* 函数更新：更新函数在特定点的值 *)
Update(f, x, v) ==
  [ y \in DOMAIN f |-> IF y = x THEN v ELSE f[y] ]

(* 函数合并：优先使用 f2 的值 *)
Merge(f1, f2) ==
  [ x \in (DOMAIN f1) \union (DOMAIN f2) |->
      IF x \in DOMAIN f2 THEN f2[x] ELSE f1[x] ]

(* 记录更新语法糖（使用 EXCEPT 的替代写法） *)
UpdateRecord(rec, field, value) ==
  [ rec EXCEPT ![field] = value ]

------------------------------------------------------------------------------
(*============================================================================*)
(* 数学辅助函数                                                                *)
(*============================================================================*)

(* 最大值函数 *)
Max2(a, b) == IF a >= b THEN a ELSE b

(* 最小值函数 *)
Min2(a, b) == IF a <= b THEN a ELSE b

(* 区间 [a, b] 的自然数集合 *)
Interval(a, b) == { n \in Nat : a <= n /\ n <= b }

(* 向上取整除法 *)
CeilDiv(a, b) == (a + b - 1) \div b

(* 整数绝对值 *)
Abs(x) == IF x >= 0 THEN x ELSE -x

(* 判断是否为偶数 *)
IsEven(n) == n % 2 = 0

(* 判断是否为奇数 *)
IsOdd(n) == n % 2 = 1

------------------------------------------------------------------------------
(*============================================================================*)
(* 类型检查辅助函数                                                            *)
(*============================================================================*)

(* 判断值是否为序列 *)
IsSequence(v) ==
  /\ v \in Seq(ANY)  \* Seq 要求元素来自某个集合

(* 判断值是否为自然数 *)
IsNatural(v) == v \in Nat

(* 判断值是否为函数 *)
IsFunction(v) ==
  v = [ x \in DOMAIN v |-> v[x] ]

(* 空值的占位符定义 *)
ANY == {}

------------------------------------------------------------------------------
(*============================================================================*)
(* 分布式系统常用工具                                                          *)
(*============================================================================*)

(* 多数派大小：对于 N 个节点，多数派至少为 Floor(N/2) + 1 *)
MajoritySize(N) == (N \div 2) + 1

(* 判断一个集合是否构成多数派（相对于全集） *)
IsMajority(subset, universe) ==
  /\ subset \subseteq universe
  /\ Cardinaltiy(subset) >= MajoritySize(Cardinaltiy(universe))

(* 节点状态转换函数 *)
StateTransition(currentState, validNextStates, nextState) ==
  /\ nextState \in validNextStates
  /\ currentState # nextState

(* 单调递增检查 *)
IsMonotonicIncreasing(seq) ==
  \A i, j \in 1..Len(seq) : i < j => seq[i] <= seq[j]

(* 严格递增检查 *)
IsStrictlyIncreasing(seq) ==
  \A i, j \in 1..Len(seq) : i < j => seq[i] < seq[j]

(* 版本向量比较（用于向量时钟） *)
VersionVectorLeq(vv1, vv2, nodes) ==
  \A n \in nodes : vv1[n] <= vv2[n]

VersionVectorLess(vv1, vv2, nodes) ==
  /\ VersionVectorLeq(vv1, vv2, nodes)
  /\ \E n \in nodes : vv1[n] < vv2[n]

------------------------------------------------------------------------------
(*============================================================================*)
(* 模块结束                                                                    *)
(*============================================================================*)

================================================================================
