/-!
# CCS (Calculus of Communicating Systems) 形式化定义

本文件在Lean 4中形式化定义了Milner的CCS进程演算。

## 参考
- Milner, R. (1989). Communication and Concurrency.
- Milner, R. (1999). Communicating and Mobile Systems: the π-Calculus.
- Aceto et al. Reactive Systems: Modelling, Specification and Verification.
-/-

namespace CCS

/-! ## 1. 基本概念与类型定义 -/

/-- 通道名称 -/
def Channel : Type := String
deriving BEq, Hashable, Repr

/-- 常数名称 -/
def ConstName : Type := String
deriving BEq, Hashable, Repr

/-- 可见动作类型
- `input ch`: 输入动作 ch?
- `output ch`: 输出动作 ch!
-/
inductive VisibleAction : Type where
  | input (ch : Channel) : VisibleAction
  | output (ch : Channel) : VisibleAction
deriving BEq, Repr

/-- 动作类型
- `visible va`: 可见动作（输入/输出）
- `tau`: 内部动作 τ
-/
inductive Action : Type where
  | visible (va : VisibleAction) : Action
  | tau : Action
deriving BEq, Repr

/-- 动作的补运算
- input的补是output（同通道）
- output的补是input（同通道）
- tau没有补（返回自身）
-/
def complement : Action → Action
  | .visible (.input ch) => .visible (.output ch)
  | .visible (.output ch) => .visible (.input ch)
  | .tau => .tau

/-- 补动作性质：双重否定等于原动作 -/
lemma complement_involutive (a : Action) : complement (complement a) = a := by
  cases a with
  | visible va =>
    cases va with
    | input ch => rfl
    | output ch => rfl
  | tau => rfl

/-- 判断两个动作是否互补 -/
def areComplementary (a₁ a₂ : Action) : Bool :=
  complement a₁ = a₂

/-- 判断动作是否为可见动作 -/
def isVisible : Action → Bool
  | .visible _ => true
  | .tau => false

/-- 获取可见动作（如果是可见动作）-/
def getVisible? : Action → Option VisibleAction
  | .visible va => some va
  | .tau => none

/-! ## 2. 进程项定义 -/

/-- CCS进程项

CCS进程由以下构造子组成：
- `Nil`: 零进程（终止进程）
- `Prefix a P`: 前缀 - 执行动作a后变为P
- `Sum P Q`: 选择 - 非确定性选择P或Q
- `Par P Q`: 并行 - P和Q并行执行
- `Restrict S P`: 限制 - P在通道集合S上的限制
- `Relabel f P`: 重标号 - 用函数f重命名P的通道
- `Const K`: 常数（递归定义的引用）
-/
inductive Process : Type where
  | Nil : Process
  | Prefix (a : Action) (P : Process) : Process
  | Sum (P Q : Process) : Process
  | Par (P Q : Process) : Process
  | Restrict (channels : List Channel) (P : Process) : Process
  | Relabel (f : Channel → Channel) (P : Process) : Process
  | Const (name : ConstName) : Process
deriving BEq, Repr

/-! ## 3. 结构化操作语义 (SOS规则) -/

/-- 转移关系：P -[a]-> Q 表示P通过动作a转移到Q -/
inductive Transition : Process → Action → Process → Prop where
  /-- Act: 前缀规则 -/
  | Act {a P} : Transition (Process.Prefix a P) a P

  /-- SumL: 选择左规则 -/
  | SumL {P Q a P'} :
    Transition P a P' →
    Transition (Process.Sum P Q) a P'

  /-- SumR: 选择右规则 -/
  | SumR {P Q a Q'} :
    Transition Q a Q' →
    Transition (Process.Sum P Q) a Q'

  /-- ParL: 并行左规则 -/
  | ParL {P Q a P'} :
    Transition P a P' →
    Transition (Process.Par P Q) a (Process.Par P' Q)

  /-- ParR: 并行右规则 -/
  | ParR {P Q a Q'} :
    Transition Q a Q' →
    Transition (Process.Par P Q) a (Process.Par P Q')

  /-- Comm: 通信规则 -/
  | Comm {P Q P' Q' a} :
    Transition P a P' →
    Transition Q (complement a) Q' →
    a ≠ .tau →
    Transition (Process.Par P Q) .tau (Process.Par P' Q')

  /-- Res: 限制规则 -/
  | Res {P a P' S} :
    Transition P a P' →
    (∀ ch, a = .visible (.input ch) ∨ a = .visible (.output ch) → ch ∉ S) →
    Transition (Process.Restrict S P) a (Process.Restrict S P')

  /-- Rel: 重标号规则 -/
  | Rel {P a P' f} :
    Transition P a P' →
    Transition (Process.Relabel f P) (relabelAction f a) (Process.Relabel f P')
  where
    relabelAction (f : Channel → Channel) : Action → Action
      | .visible (.input ch) => .visible (.input (f ch))
      | .visible (.output ch) => .visible (.output (f ch))
      | .tau => .tau

infix:50 " -[ " => fun P a => Transition P a

/-! ## 4. 强互模拟 (Strong Bisimulation) -/

/-- 强互模拟关系

关系R是强互模拟，当且仅当：
- 如果 (P, Q) ∈ R 且 P -[a]-> P'，则存在 Q' 使得 Q -[a]-> Q' 且 (P', Q') ∈ R
- 如果 (P, Q) ∈ R 且 Q -[a]-> Q'，则存在 P' 使得 P -[a]-> P' 且 (P', Q') ∈ R
-/
def IsStrongBisimulation (R : Process → Process → Prop) : Prop :=
  ∀ P Q, R P Q →
    (∀ a P', Transition P a P' → ∃ Q', Transition Q a Q' ∧ R P' Q') ∧
    (∀ a Q', Transition Q a Q' → ∃ P', Transition P a P' ∧ R P' Q')

/-- 强互模拟等价关系（强互模拟的最大不动点）-/
def StronglyBisimilar (P Q : Process) : Prop :=
  ∃ R, IsStrongBisimulation R ∧ R P Q

infix:60 " ~ " => StronglyBisimilar

/-- 强互模拟是对称关系 -/
lemma strongBisim_symmetric {P Q : Process} : P ~ Q → Q ~ P := by
  intro h
  rcases h with ⟨R, hR, hPQ⟩
  use fun x y => R y x
  constructor
  · -- 证明逆关系也是强互模拟
    intro P' Q' hQP
    have h_sym := hR Q' P' hQP
    exact ⟨h_sym.right, h_sym.left⟩
  · -- 证明 Q R P
    exact hPQ

/-- 强互模拟是自反关系 -/
lemma strongBisim_reflexive (P : Process) : P ~ P := by
  use Eq
  constructor
  · -- 证明相等关系是强互模拟
    intro P' Q' h_eq
    rw [h_eq]
    constructor
    · intro a P' h_trans
      use P'
      constructor
      · exact h_trans
      · rfl
    · intro a Q' h_trans
      use Q'
      constructor
      · exact h_trans
      · rfl
  · -- 证明 P = P
    rfl

/-! ## 5. 弱互模拟 (Weak Bisimulation) -/

/-- 弱转移闭包

弱转移允许在执行可见动作前后执行任意数量的τ动作：
- P =τ=> Q 表示P可以通过0个或多个τ转移到Q
- P =a=> Q 表示P可以通过0个或多个τ，然后a，然后0个或多个τ转移到Q
-/
inductive WeakTransition : Process → Action → Process → Prop where
  | TauRefl {P} : WeakTransition P .tau P
  | TauStep {P P' Q} :
    Transition P .tau P' →
    WeakTransition P' .tau Q →
    WeakTransition P .tau Q
  | VisibleStep {P P' Q a} :
    Transition P a P' →
    a ≠ .tau →
    WeakTransition P' .tau Q →
    WeakTransition P a Q

/-- 弱互模拟关系 -/
def IsWeakBisimulation (R : Process → Process → Prop) : Prop :=
  ∀ P Q, R P Q →
    (∀ a P', Transition P a P' →
      if a = .tau then
        ∃ Q', WeakTransition Q .tau Q' ∧ R P' Q'
      else
        ∃ Q', WeakTransition Q a Q' ∧ R P' Q') ∧
    (∀ a Q', Transition Q a Q' →
      if a = .tau then
        ∃ P', WeakTransition P .tau P' ∧ R P' Q'
      else
        ∃ P', WeakTransition P a P' ∧ R P' Q')

/-- 弱互模拟等价关系 -/
def WeaklyBisimilar (P Q : Process) : Prop :=
  ∃ R, IsWeakBisimulation R ∧ R P Q

infix:60 " ≈ " => WeaklyBisimilar

/-- 强互模拟蕴含弱互模拟 -/
lemma strong_implies_weak {P Q : Process} : P ~ Q → P ≈ Q := by
  intro h
  rcases h with ⟨R, hR, hPQ⟩
  use R
  constructor
  · -- 证明强互模拟也是弱互模拟
    intro P' Q' hR'
    have h_strong := hR P' Q' hR'
    constructor
    · intro a P'' h_trans
      cases h_eq : a with
      | tau =>
        have ⟨Q', hQ, hR''⟩ := h_strong.left .tau P'' h_trans
        use Q'
        constructor
        · apply WeakTransition.TauStep hQ
          apply WeakTransition.TauRefl
        · exact hR''
      | visible va =>
        have ⟨Q', hQ, hR''⟩ := h_strong.left a P'' h_trans
        use Q'
        constructor
        · apply WeakTransition.VisibleStep hQ (by simp [h_eq]) WeakTransition.TauRefl
        · exact hR''
    · intro a Q'' h_trans
      cases h_eq : a with
      | tau =>
        have ⟨P', hP, hR''⟩ := h_strong.right .tau Q'' h_trans
        use P'
        constructor
        · apply WeakTransition.TauStep hP
          apply WeakTransition.TauRefl
        · exact hR''
      | visible va =>
        have ⟨P', hP, hR''⟩ := h_strong.right a Q'' h_trans
        use P'
        constructor
        · apply WeakTransition.VisibleStep hP (by simp [h_eq]) WeakTransition.TauRefl
        · exact hR''
  · exact hPQ

/-! ## 6. 示例进程 -/

section Examples

/-- 缓冲区进程（单槽）
    Buffer = in?.out!.Buffer -/
def Buffer : Process :=
  Process.Prefix (.visible (.input "in"))
    (Process.Prefix (.visible (.output "out")
      (Process.Const "Buffer")))

/-- 发送者进程
    Sender = send!.Sender -/
def Sender : Process :=
  Process.Prefix (.visible (.output "send")
    (Process.Const "Sender"))

/-- 接收者进程
    Receiver = recv?.Receiver -/
def Receiver : Process :=
  Process.Prefix (.visible (.input "recv")
    (Process.Const "Receiver"))

/-- 简单通信系统：发送者和接收者并行
    System = Sender | Receiver -/
def CommunicationSystem : Process :=
  Process.Par Sender Receiver

/-- 计数器进程
    Counter(n) = if n>0 then (inc?.Counter(n+1) + dec?.Counter(n-1)) else inc?.Counter(1) -/
def CounterSpec (n : Nat) : Process :=
  match n with
  | 0 => Process.Prefix (.visible (.input "inc")) (CounterSpec 1)
  | n+1 => Process.Sum
    (Process.Prefix (.visible (.input "inc")) (CounterSpec (n+2)))
    (Process.Prefix (.visible (.input "dec")) (CounterSpec n))

/-- 带限制通道的通信系统
    PrivateSystem = (Sender | Receiver) \\ {send, recv} -/
def PrivateSystem : Process :=
  Process.Restrict ["send", "recv"] CommunicationSystem

/-- 交替进程：交替执行a和b
    Alternator = a?.b!.Alternator -/
def Alternator : Process :=
  Process.Prefix (.visible (.input "a"))
    (Process.Prefix (.visible (.output "b")
      (Process.Const "Alternator")))

/-- 死锁进程（无转移）-/
def Deadlock : Process := Process.Nil

/-- 活锁示例：只执行内部τ动作
    Divergent = τ.Divergent -/
def Divergent : Process :=
  Process.Prefix .tau (Process.Const "Divergent")

end Examples

/-! ## 7. 辅助定义与引理 -/

/-- 进程的自由通道集合（近似定义）-/
def freeChannels : Process → List Channel
  | .Nil => []
  | .Prefix (.visible (.input ch)) P => ch :: freeChannels P
  | .Prefix (.visible (.output ch)) P => ch :: freeChannels P
  | .Prefix .tau P => freeChannels P
  | .Sum P Q => freeChannels P ++ freeChannels Q
  | .Par P Q => freeChannels P ++ freeChannels Q
  | .Restrict S P => (freeChannels P).filter (fun ch => ch ∉ S)
  | .Relabel f P => (freeChannels P).map f
  | .Const _ => []  -- 常数的自由通道需要环境定义

/-- 零进程的不可转移性 -/
lemma Nil_no_transition : ∀ a P, ¬Transition Process.Nil a P := by
  intro a P h
  cases h

/-- 前缀进程的确定性 -/
lemma Prefix_deterministic {a P Q R} :
  Transition (Process.Prefix a P) a Q →
  Transition (Process.Prefix a P) a R →
  Q = R := by
  intro h1 h2
  cases h1
  cases h2
  rfl

/-- 互模拟的并集仍是互模拟 -/
lemma bisimulation_union {R₁ R₂ : Process → Process → Prop}
  (h₁ : IsStrongBisimulation R₁)
  (h₂ : IsStrongBisimulation R₂) :
  IsStrongBisimulation (fun P Q => R₁ P Q ∨ R₂ P Q) := by
  intro P Q h_union
  cases h_union with
  | inl hR₁ =>
    have h := h₁ P Q hR₁
    constructor
    · intro a P' h_trans
      have ⟨Q', hQ, hR'⟩ := h.left a P' h_trans
      use Q'
      constructor
      · exact hQ
      · left; exact hR'
    · intro a Q' h_trans
      have ⟨P', hP, hR'⟩ := h.right a Q' h_trans
      use P'
      constructor
      · exact hP
      · left; exact hR'
  | inr hR₂ =>
    have h := h₂ P Q hR₂
    constructor
    · intro a P' h_trans
      have ⟨Q', hQ, hR'⟩ := h.left a P' h_trans
      use Q'
      constructor
      · exact hQ
      · right; exact hR'
    · intro a Q' h_trans
      have ⟨P', hP, hR'⟩ := h.right a Q' h_trans
      use P'
      constructor
      · exact hP
      · right; exact hR'

end CCS
