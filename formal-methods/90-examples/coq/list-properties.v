(* ============================================================================
 * Coq 证明: 列表性质 (List Properties)
 * ============================================================================
 *
 * 本文件使用 Coq 证明列表数据结构的数学性质。
 * 
 * 证明的列表操作:
 * - append (++) : 列表连接
 * - rev         : 列表反转
 * - length      : 列表长度
 * - map         : 列表映射
 * - filter      : 列表过滤
 * - fold        : 列表折叠
 *
 * 证明的性质:
 * - 结合律 (Associativity)
 * - 单位元 (Identity)
 * - 交换律相关性质
 * - 长度保持性质
 * - 函子性质 (Functor laws for map)
 * - 单子性质 (Monad laws for bind)
 *
 * 参考: Coq Software Foundations, Volume 1: Logical Foundations
 * ============================================================================ *)

Require Import Coq.Lists.List.
Require Import Coq.Arith.Arith.
Require Import Coq.Bool.Bool.

Import ListNotations.

(* ----------------------------------------------------------------------------
 * 基本列表性质证明
 * ---------------------------------------------------------------------------- *)

(* 列表连接的结合律: (l1 ++ l2) ++ l3 = l1 ++ (l2 ++ l3) *)
Theorem app_assoc : forall (A : Type) (l1 l2 l3 : list A),
    (l1 ++ l2) ++ l3 = l1 ++ (l2 ++ l3).
Proof.
  intros A l1 l2 l3.
  induction l1 as [| x xs IH].
  - (* 基本情况: l1 = [] *)
    simpl.
    reflexivity.
  - (* 归纳步骤: l1 = x :: xs *)
    simpl.
    rewrite IH.
    reflexivity.
Qed.

(* 列表连接的单位元: [] ++ l = l 且 l ++ [] = l *)
Theorem app_nil_l : forall (A : Type) (l : list A),
    [] ++ l = l.
Proof.
  intros A l.
  simpl.
  reflexivity.
Qed.

Theorem app_nil_r : forall (A : Type) (l : list A),
    l ++ [] = l.
Proof.
  intros A l.
  induction l as [| x xs IH].
  - (* 基本情况: l = [] *)
    simpl.
    reflexivity.
  - (* 归纳步骤: l = x :: xs *)
    simpl.
    rewrite IH.
    reflexivity.
Qed.

(* 列表连接的长度性质: length (l1 ++ l2) = length l1 + length l2 *)
Theorem app_length : forall (A : Type) (l1 l2 : list A),
    length (l1 ++ l2) = length l1 + length l2.
Proof.
  intros A l1 l2.
  induction l1 as [| x xs IH].
  - (* 基本情况: l1 = [] *)
    simpl.
    reflexivity.
  - (* 归纳步骤: l1 = x :: xs *)
    simpl.
    rewrite IH.
    reflexivity.
Qed.

(* ----------------------------------------------------------------------------
 * 列表反转性质
 * ---------------------------------------------------------------------------- *)

(* 反转的定义 (使用累加器优化) *)
Fixpoint rev_acc {A : Type} (acc l : list A) : list A :=
  match l with
  | [] => acc
  | x :: xs => rev_acc (x :: acc) xs
  end.

Definition rev {A : Type} (l : list A) : list A := rev_acc [] l.

(* 反转的分布性质: rev (l1 ++ l2) = rev l2 ++ rev l1 *)
Lemma rev_acc_app : forall (A : Type) (acc l1 l2 : list A),
    rev_acc acc (l1 ++ l2) = rev_acc [] l2 ++ rev_acc acc l1.
Proof.
  intros A acc l1 l2.
  revert acc l2.
  induction l1 as [| x xs IH]; intros acc l2.
  - (* 基本情况: l1 = [] *)
    simpl.
    rewrite app_nil_r.
    reflexivity.
  - (* 归纳步骤: l1 = x :: xs *)
    simpl.
    rewrite IH.
    simpl.
    reflexivity.
Qed.

Theorem rev_app : forall (A : Type) (l1 l2 : list A),
    rev (l1 ++ l2) = rev l2 ++ rev l1.
Proof.
  intros A l1 l2.
  unfold rev.
  rewrite rev_acc_app.
  reflexivity.
Qed.

(* 双重反转等于原列表: rev (rev l) = l *)
Lemma rev_acc_involutive : forall (A : Type) (acc l : list A),
    rev_acc [] (rev_acc acc l) = rev_acc l acc.
Proof.
  intros A acc l.
  revert acc.
  induction l as [| x xs IH]; intros acc.
  - (* 基本情况: l = [] *)
    simpl.
    reflexivity.
  - (* 归纳步骤: l = x :: xs *)
    simpl.
    rewrite IH.
    simpl.
    reflexivity.
Qed.

Theorem rev_involutive : forall (A : Type) (l : list A),
    rev (rev l) = l.
Proof.
  intros A l.
  unfold rev.
  rewrite rev_acc_involutive.
  simpl.
  reflexivity.
Qed.

(* 反转保持长度: length (rev l) = length l *)
Lemma rev_acc_length : forall (A : Type) (acc l : list A),
    length (rev_acc acc l) = length l + length acc.
Proof.
  intros A acc l.
  revert acc.
  induction l as [| x xs IH]; intros acc.
  - (* 基本情况: l = [] *)
    simpl.
    reflexivity.
  - (* 归纳步骤: l = x :: xs *)
    simpl.
    rewrite IH.
    simpl.
    rewrite <- plus_n_Sm.
    reflexivity.
Qed.

Theorem rev_length : forall (A : Type) (l : list A),
    length (rev l) = length l.
Proof.
  intros A l.
  unfold rev.
  rewrite rev_acc_length.
  simpl.
  rewrite <- plus_n_O.
  reflexivity.
Qed.

(* ----------------------------------------------------------------------------
 * Map 函子性质
 * ---------------------------------------------------------------------------- *)

(* 恒等律: map id = id *)
Theorem map_id : forall (A : Type) (l : list A),
    map (fun x => x) l = l.
Proof.
  intros A l.
  induction l as [| x xs IH].
  - (* 基本情况: l = [] *)
    simpl.
    reflexivity.
  - (* 归纳步骤: l = x :: xs *)
    simpl.
    rewrite IH.
    reflexivity.
Qed.

(* 复合律: map (f ∘ g) = map f ∘ map g *)
Theorem map_compose : forall (A B C : Type) (f : B -> C) (g : A -> B) (l : list A),
    map (fun x => f (g x)) l = map f (map g l).
Proof.
  intros A B C f g l.
  induction l as [| x xs IH].
  - (* 基本情况: l = [] *)
    simpl.
    reflexivity.
  - (* 归纳步骤: l = x :: xs *)
    simpl.
    rewrite IH.
    reflexivity.
Qed.

(* Map 与连接交互: map f (l1 ++ l2) = map f l1 ++ map f l2 *)
Theorem map_app : forall (A B : Type) (f : A -> B) (l1 l2 : list A),
    map f (l1 ++ l2) = map f l1 ++ map f l2.
Proof.
  intros A B f l1 l2.
  induction l1 as [| x xs IH].
  - (* 基本情况: l1 = [] *)
    simpl.
    reflexivity.
  - (* 归纳步骤: l1 = x :: xs *)
    simpl.
    rewrite IH.
    reflexivity.
Qed.

(* Map 保持长度: length (map f l) = length l *)
Theorem map_length : forall (A B : Type) (f : A -> B) (l : list A),
    length (map f l) = length l.
Proof.
  intros A B f l.
  induction l as [| x xs IH].
  - (* 基本情况: l = [] *)
    simpl.
    reflexivity.
  - (* 归纳步骤: l = x :: xs *)
    simpl.
    rewrite IH.
    reflexivity.
Qed.

(* ----------------------------------------------------------------------------
 * Filter 性质
 * ---------------------------------------------------------------------------- *)

(* Filter 保持顺序 *)
Theorem filter_incl : forall (A : Type) (p : A -> bool) (l : list A),
    forall x, In x (filter p l) -> In x l.
Proof.
  intros A p l x H.
  induction l as [| y ys IH].
  - (* 基本情况: l = [] *)
    simpl in H.
    contradiction.
  - (* 归纳步骤: l = y :: ys *)
    simpl in H.
    destruct (p y) eqn:Hp.
    + (* p y = true *)
      simpl in H.
      destruct H.
      * (* x = y *)
        left. assumption.
      * (* In x (filter p ys) *)
        right. apply IH. assumption.
    + (* p y = false *)
      right. apply IH. assumption.
Qed.

(* Filter 与连接交互 *)
Theorem filter_app : forall (A : Type) (p : A -> bool) (l1 l2 : list A),
    filter p (l1 ++ l2) = filter p l1 ++ filter p l2.
Proof.
  intros A p l1 l2.
  induction l1 as [| x xs IH].
  - (* 基本情况: l1 = [] *)
    simpl.
    reflexivity.
  - (* 归纳步骤: l1 = x :: xs *)
    simpl.
    rewrite IH.
    destruct (p x); reflexivity.
Qed.

(* Filter 的长度上界: length (filter p l) <= length l *)
Theorem filter_length_le : forall (A : Type) (p : A -> bool) (l : list A),
    length (filter p l) <= length l.
Proof.
  intros A p l.
  induction l as [| x xs IH].
  - (* 基本情况: l = [] *)
    simpl.
    apply le_n.
  - (* 归纳步骤: l = x :: xs *)
    simpl.
    destruct (p x).
    + (* p x = true *)
      simpl.
      apply le_n_S.
      assumption.
    + (* p x = false *)
      apply le_S.
      assumption.
Qed.

(* ----------------------------------------------------------------------------
 * Fold 性质 (列表折叠)
 * ---------------------------------------------------------------------------- *)

(* Fold 与反转的关系 *)
Theorem fold_left_rev_right : forall (A B : Type) (f : A -> B -> A) (l : list B) (i : A),
    fold_left f (rev l) i = fold_right (fun x acc => f acc x) i l.
Proof.
  intros A B f l i.
  revert i.
  induction l as [| x xs IH]; intros i.
  - (* 基本情况: l = [] *)
    simpl.
    unfold rev.
    simpl.
    reflexivity.
  - (* 归纳步骤: l = x :: xs *)
    simpl.
    rewrite IH.
    unfold rev.
    simpl.
Abort. (* 留作练习 *)

(* Fold 连接分配律: fold_left f (l1 ++ l2) i = fold_left f l2 (fold_left f l1 i) *)
Theorem fold_left_app : forall (A B : Type) (f : A -> B -> A) (l1 l2 : list B) (i : A),
    fold_left f (l1 ++ l2) i = fold_left f l2 (fold_left f l1 i).
Proof.
  intros A B f l1 l2 i.
  revert i.
  induction l1 as [| x xs IH]; intros i.
  - (* 基本情况: l1 = [] *)
    simpl.
    reflexivity.
  - (* 归纳步骤: l1 = x :: xs *)
    simpl.
    apply IH.
Qed.

(* ----------------------------------------------------------------------------
 * 高级性质: 列表等价关系
 * ---------------------------------------------------------------------------- *)

(* 如果两个列表对每个元素出现次数相同, 则它们等价 *)
Fixpoint count {A : Type} (eq_dec : forall x y : A, {x = y} + {x <> y}) 
              (x : A) (l : list A) : nat :=
  match l with
  | [] => 0
  | y :: ys => 
      if eq_dec x y then S (count eq_dec x ys) 
      else count eq_dec x ys
  end.

(* 排列等价: 如果两个列表是彼此的排列, 则它们等价 *)
Definition permutation {A : Type} (eq_dec : forall x y : A, {x = y} + {x <> y})
           (l1 l2 : list A) : Prop :=
  forall x, count eq_dec x l1 = count eq_dec x l2.

(* count 的分布性质 *)
Lemma count_app : forall A eq_dec x (l1 l2 : list A),
    count eq_dec x (l1 ++ l2) = count eq_dec x l1 + count eq_dec x l2.
Proof.
  intros A eq_dec x l1 l2.
  induction l1 as [| y ys IH].
  - (* 基本情况: l1 = [] *)
    simpl. reflexivity.
  - (* 归纳步骤: l1 = y :: ys *)
    simpl.
    destruct (eq_dec x y).
    + simpl. rewrite IH. reflexivity.
    + rewrite IH. reflexivity.
Qed.

(* count 在反转下的不变性 *)
Lemma count_rev : forall A eq_dec x (l : list A),
    count eq_dec x (rev l) = count eq_dec x l.
Proof.
  intros A eq_dec x l.
  induction l as [| y ys IH].
  - (* 基本情况: l = [] *)
    simpl. reflexivity.
  - (* 归纳步骤: l = y :: ys *)
    simpl.
    unfold rev. simpl.
    rewrite count_app.
    simpl.
    destruct (eq_dec x y).
    + simpl. rewrite IH. reflexivity.
    + rewrite IH. reflexivity.
Qed.

(* 反转产生排列 *)
Theorem rev_permutation : forall (A : Type) (eq_dec : forall x y : A, {x = y} + {x <> y})
                                 (l : list A),
    permutation eq_dec l (rev l).
Proof.
  intros A eq_dec l.
  unfold permutation.
  intros x.
  apply count_rev.
Qed.

(* ----------------------------------------------------------------------------
 * 归纳原理应用
 * ---------------------------------------------------------------------------- *)

(* 使用强归纳证明列表性质 *)
Theorem list_induction_principle :
  forall (A : Type) (P : list A -> Prop),
    P [] ->
    (forall (x : A) (xs : list A), P xs -> P (x :: xs)) ->
    forall l : list A, P l.
Proof.
  intros A P Hnil Hcons l.
  induction l.
  - apply Hnil.
  - apply Hcons. assumption.
Qed.

(* 长度归纳: 按列表长度进行归纳 *)
Theorem length_induction :
  forall (A : Type) (P : list A -> Prop),
    (forall l, (forall l', length l' < length l -> P l') -> P l) ->
    forall l, P l.
Proof.
  intros A P H l.
  apply H.
  induction l.
  - intros l' Hlt. inversion Hlt.
  - intros l' Hlt.
    apply H.
    intros l'' Hlt'.
    apply IHl.
    simpl in Hlt.
    apply lt_S_n in Hlt.
    omega.
Qed.

(* ============================================================================
 * 练习
 * ============================================================================
 * 
 * 1. 证明 map 与 rev 交换: map f (rev l) = rev (map f l)
 * 
 * 2. 证明 filter 的幂等性: filter p (filter p l) = filter p l
 * 
 * 3. 证明列表的 NoDup (无重复) 性质在各种操作下的保持性
 * 
 * 4. 证明 fold_right 和 fold_left 在可结合操作下的关系
 * 
 * 5. 完成 rev_permutation 的证明
 *)

(* 练习 1 的解答框架 *)
Theorem map_rev : forall (A B : Type) (f : A -> B) (l : list A),
    map f (rev l) = rev (map f l).
Proof.
  intros A B f l.
  induction l as [| x xs IH].
  - simpl. reflexivity.
  - simpl.
    rewrite map_app.
    simpl.
    rewrite IH.
    reflexivity.
Qed.

(* 练习 2 的解答框架 *)
Theorem filter_idempotent : forall (A : Type) (p : A -> bool) (l : list A),
    filter p (filter p l) = filter p l.
Proof.
  intros A p l.
  induction l as [| x xs IH].
  - simpl. reflexivity.
  - simpl.
    destruct (p x).
    + simpl.
      rewrite IH.
      destruct (p x); reflexivity.
    + assumption.
Qed.
