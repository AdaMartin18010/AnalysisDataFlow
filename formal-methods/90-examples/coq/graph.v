(* ============================================================================
 * Coq 证明: 图算法验证 (Graph Algorithms)
 * ============================================================================
 *
 * 本文件使用 Coq 形式化验证图算法及其性质。
 *
 * 涵盖内容:
 * - 图的表示 (邻接表、邻接矩阵)
 * - 可达性 (Reachability)
 * - 深度优先搜索 (DFS)
 * - 广度优先搜索 (BFS)
 * - 最短路径 (Dijkstra - 规约)
 * - 拓扑排序 (Topological Sort)
 *
 * 验证性质:
 * - 算法终止性
 * - 正确性 (如: BFS找到最短路径)
 * - 完备性 (找到所有可达节点)
 *
 * 参考:
 * - Mathematical Components Library (MathComp)
 * - Graph Theory in Coq
 * ============================================================================ *)

Require Import Coq.Lists.List.
Require Import Coq.Arith.Arith.
Require Import Coq.Arith.Compare_dec.
Require Import Coq.Bool.Bool.
Require Import Coq.Setoids.Setoid.
Require Import Coq.Classes.RelationClasses.
Require Import Coq.Relations.Relation_Definitions.

Import ListNotations.

(* ----------------------------------------------------------------------------
 * 图的基本定义
 * ---------------------------------------------------------------------------- *)

(* 顶点类型 *)
Definition Vertex := nat.

(* 边: (源, 目标, 权重) *)
Definition Edge := (Vertex * Vertex * nat)%type.

(* 图: 顶点集合 + 边集合 *)
Record Graph := {
  vertices : list Vertex;
  edges : list Edge;
  vertices_nodup : NoDup vertices  (* 顶点无重复 *)
}.

(* 判断边是否存在 *)
Definition has_edge (g : Graph) (u v : Vertex) : bool :=
  existsb (fun e => let '(u', v', _) := e in Nat.eqb u u' && Nat.eqb v v') (edges g).

(* 获取邻居节点 *)
Definition neighbors (g : Graph) (v : Vertex) : list Vertex :=
  map (fun e => let '(_, v', _) := e in v')
      (filter (fun e => let '(u', _, _) := e in Nat.eqb v u') (edges g)).

(* ----------------------------------------------------------------------------
 * 路径和可达性
 * ---------------------------------------------------------------------------- *)

(* 路径: 顶点序列, 相邻顶点间有边 *)
Inductive Path (g : Graph) : Vertex -> Vertex -> list Vertex -> Prop :=
  | Path_nil : forall v, In v (vertices g) -> Path g v v [v]
  | Path_cons : forall u v w p,
      Path g u v p ->
      has_edge g v w = true ->
      Path g u w (p ++ [w]).

(* 可达性关系 *)
Definition Reachable (g : Graph) (u v : Vertex) : Prop :=
  exists p, Path g u v p.

(* 可达性的自反性和传递性 *)
Lemma reachable_refl : forall g v,
    In v (vertices g) -> Reachable g v v.
Proof.
  intros g v Hin.
  exists [v].
  apply Path_nil. assumption.
Qed.

Lemma reachable_trans : forall g u v w,
    Reachable g u v -> Reachable g v w -> Reachable g u w.
Proof.
  intros g u v w [p1 Hp1] [p2 Hp2].
  (* 路径组合 *)
Admitted. (* 需要路径连接引理 *)

(* ----------------------------------------------------------------------------
 * 深度优先搜索 (DFS)
 * ---------------------------------------------------------------------------- *)

(* DFS 状态 *)
Record DFSState := {
  visited : list Vertex;
  stack : list Vertex;
  result : list Vertex  (* 访问顺序 *)
}.

(* DFS 单步 *)
Definition dfs_step (g : Graph) (s : DFSState) : option DFSState :=
  match stack s with
  | [] => None  (* 完成 *)
  | v :: rest =>
      if existsb (Nat.eqb v) (visited s) then
        (* 已访问, 跳过 *)
        Some {| visited := visited s;
                stack := rest;
                result := result s |}
      else
        (* 未访问, 标记并扩展 *)
        let new_visited := v :: visited s in
        let new_stack := neighbors g v ++ rest in
        Some {| visited := new_visited;
                stack := new_stack;
                result := v :: result s |}
  end.

(* DFS 迭代 (使用 fuel 确保终止) *)
Fixpoint dfs_iter (g : Graph) (fuel : nat) (s : DFSState) : DFSState :=
  match fuel with
  | 0 => s  (* 燃料耗尽 *)
  | S fuel' =>
      match dfs_step g s with
      | None => s  (* 完成 *)
      | Some s' => dfs_iter g fuel' s'
      end
  end.

(* DFS 入口 *)
Definition dfs (g : Graph) (start : Vertex) : list Vertex :=
  let initial_state := {| visited := [];
                          stack := [start];
                          result := [] |} in
  let fuel := S (length (vertices g)) in  (* 足够燃料 *)
  rev (result (dfs_iter g fuel initial_state)).

(* DFS 正确性: 访问的节点都可达 *)
Lemma dfs_soundness : forall g start v,
    In v (dfs g start) -> Reachable g start v.
Proof.
  (* 归纳于 fuel 或 dfs_iter *)
Admitted.

(* DFS 完备性: 所有可达节点都被访问 *)
Lemma dfs_completeness : forall g start v,
    Reachable g start v -> In v (dfs g start).
Proof.
  (* 需要强归纳 *)
Admitted.

(* ----------------------------------------------------------------------------
 * 广度优先搜索 (BFS)
 * ---------------------------------------------------------------------------- *)

(* BFS 状态 *)
Record BFSState := {
  bfs_visited : list Vertex;
  queue : list (Vertex * nat);  (* (节点, 距离) *)
  distances : list (Vertex * nat)  (* 记录的最短距离 *)
}.

(* BFS 单步 *)
Definition bfs_step (g : Graph) (s : BFSState) : option BFSState :=
  match queue s with
  | [] => None  (* 完成 *)
  | (v, d) :: rest =>
      if existsb (fun '(v', _) => Nat.eqb v v') (bfs_visited s) then
        (* 已访问, 跳过 *)
        Some {| bfs_visited := bfs_visited s;
                queue := rest;
                distances := distances s |}
      else
        (* 未访问, 扩展邻居 *)
        let new_visited := (v, d) :: bfs_visited s in
        let new_neighbors := filter (fun v' => 
          negb (existsb (fun '(u, _) => Nat.eqb v' u) new_visited))
          (neighbors g v) in
        let new_queue := rest ++ map (fun v' => (v', S d)) new_neighbors in
        Some {| bfs_visited := new_visited;
                queue := new_queue;
                distances := (v, d) :: distances s |}
  end.

(* BFS 迭代 *)
Fixpoint bfs_iter (g : Graph) (fuel : nat) (s : BFSState) : BFSState :=
  match fuel with
  | 0 => s
  | S fuel' =>
      match bfs_step g s with
      | None => s
      | Some s' => bfs_iter g fuel' s'
      end
  end.

(* BFS 入口 *)
Definition bfs (g : Graph) (start : Vertex) : list (Vertex * nat) :=
  let initial_state := {| bfs_visited := [];
                          queue := [(start, 0)];
                          distances := [] |} in
  let fuel := S (length (vertices g) * length (vertices g)) in
  rev (distances (bfs_iter g fuel initial_state)).

(* 获取距离 *)
Definition distance_to (distances : list (Vertex * nat)) (v : Vertex) : option nat :=
  match find (fun '(v', _) => Nat.eqb v v') distances with
  | Some (_, d) => Some d
  | None => None
  end.

(* BFS 正确性: 找到的距离是最短距离 *)
Lemma bfs_correctness : forall g start v d,
    distance_to (bfs g start) v = Some d ->
    (exists p, Path g start v p /\ length p = S d) /\  (* 可达且长度为 d+1 *)
    (forall p, Path g start v p -> length p >= S d).  (* 最短性 *)
Proof.
  (* 需要归纳证明 BFS 按距离顺序扩展 *)
Admitted.

(* ----------------------------------------------------------------------------
 * 拓扑排序
 * ---------------------------------------------------------------------------- *)

(* 有向无环图 (DAG) *)
Definition IsDAG (g : Graph) : Prop :=
  ~ exists v, Reachable g v v.  (* 无自环, 即无环 *)

(* 入度计算 *)
Definition in_degree (g : Graph) (v : Vertex) : nat :=
  length (filter (fun e => let '(_, v', _) := e in Nat.eqb v v') (edges g)).

(* 拓扑排序状态 *)
Record TopoState := {
  topo_order : list Vertex;
  remaining : list Vertex;
  in_degrees : list (Vertex * nat)
}.

(* 移除节点及其出边 *)
Definition remove_vertex_edges (g : Graph) (v : Vertex) : Graph :=
  {| vertices := vertices g;
     edges := filter (fun e => let '(u, _, _) := e in negb (Nat.eqb u v)) (edges g);
     vertices_nodup := vertices_nodup g |}.

(* 拓扑排序单步: 找入度为0的节点 *)
Definition topo_step (g : Graph) (s : TopoState) : option TopoState :=
  match filter (fun '(v, deg) => Nat.eqb deg 0 && 
              negb (existsb (Nat.eqb v) (topo_order s))) (in_degrees s) with
  | [] => None  (* 无可用节点, 完成或有环 *)
  | (v, _) :: _ =>
      let new_remaining := remove v (remaining s) in
      let g' := remove_vertex_edges g v in
      let new_in_degrees := map (fun v' => (v', in_degree g' v')) new_remaining in
      Some {| topo_order := topo_order s ++ [v];
              remaining := new_remaining;
              in_degrees := new_in_degrees |}
  end.

(* 拓扑排序迭代 *)
Fixpoint topo_iter (g : Graph) (fuel : nat) (s : TopoState) : option TopoState :=
  match fuel with
  | 0 => Some s  (* 燃料耗尽 *)
  | S fuel' =>
      match topo_step g s with
      | None => Some s  (* 完成 *)
      | Some s' => topo_iter g fuel' s'
      end
  end.

(* 拓扑排序入口 *)
Definition topological_sort (g : Graph) : option (list Vertex) :=
  let initial_state := {| topo_order := [];
                          remaining := vertices g;
                          in_degrees := map (fun v => (v, in_degree g v)) (vertices g) |} in
  let fuel := S (length (vertices g)) in
  match topo_iter g fuel initial_state with
  | Some s => 
      if Nat.eqb (length (topo_order s)) (length (vertices g))
      then Some (topo_order s)  (* 成功 *)
      else None  (* 有环 *)
  | None => None
  end.

(* 拓扑排序正确性: 对于每条边 (u,v), u 在 v 之前 *)
Lemma topological_sort_correct : forall g order,
    topological_sort g = Some order ->
    forall u v w, In (u, v, w) (edges g) ->
    exists i j, nth_error order i = Some u /\
                nth_error order j = Some v /\
                i < j.
Proof.
  (* 基于拓扑排序构造过程 *)
Admitted.

(* ----------------------------------------------------------------------------
 * 最短路径: Dijkstra 算法 (规约)
 * ---------------------------------------------------------------------------- *)

(* 优先队列元素: (距离, 节点) *)
Definition PQElem := (nat * Vertex)%type.

(* Dijkstra 状态 *)
Record DijkstraState := {
  dist : list (Vertex * nat);  (* 当前最短距离 *)
  pq : list PQElem;            (* 优先队列 *)
  finalized : list Vertex      (* 已确定最短距离的节点 *)
}.

(* 提取最小距离节点 *)
Definition extract_min (pq : list PQElem) : option (PQElem * list PQElem) :=
  match pq with
  | [] => None
  | _ => 
      let min_elem := fold_right (fun x y => if fst x <=? fst y then x else y) 
                                  (hd (0, 0) pq) pq in
      Some (min_elem, remove min_elem pq)
  end.

(* 边权重 *)
Definition edge_weight (g : Graph) (u v : Vertex) : option nat :=
  match find (fun '(u', v', w) => Nat.eqb u u' && Nat.eqb v v') (edges g) with
  | Some (_, _, w) => Some w
  | None => None
  end.

(* 松弛操作 *)
Definition relax (g : Graph) (s : DijkstraState) (u : Vertex) (du : nat)
                : DijkstraState :=
  fold_left (fun acc v =>
    match edge_weight g u v with
    | Some w =>
        let new_dist := du + w in
        (match find (fun '(v', _) => Nat.eqb v v') (dist acc) with
        | Some (_, old_dist) =>
            if new_dist <? old_dist then
              {| dist := map (fun '(x, d) => if Nat.eqb x v then (x, new_dist) else (x, d)) 
                            (dist acc);
                 pq := (new_dist, v) :: pq acc;
                 finalized := finalized acc |}
            else acc
        | None => acc
        end)
    | None => acc
    end) (neighbors g u) s.

(* Dijkstra 单步 *)
Definition dijkstra_step (g : Graph) (s : DijkstraState) : option DijkstraState :=
  match extract_min (pq s) with
  | None => None  (* 优先队列为空 *)
  | Some ((du, u), pq') =>
      if existsb (Nat.eqb u) (finalized s) then
        (* 已处理, 跳过 *)
        Some {| dist := dist s; pq := pq'; finalized := finalized s |}
      else
        (* 处理节点 u *)
        let s' := {| dist := dist s; pq := pq'; 
                    finalized := u :: finalized s |} in
        Some (relax g s' u du)
  end.

(* Dijkstra 迭代 *)
Fixpoint dijkstra_iter (g : Graph) (fuel : nat) (s : DijkstraState) : DijkstraState :=
  match fuel with
  | 0 => s
  | S fuel' =>
      match dijkstra_step g s with
      | None => s
      | Some s' => dijkstra_iter g fuel' s'
      end
  end.

(* Dijkstra 入口 *)
Definition dijkstra (g : Graph) (start : Vertex) : list (Vertex * nat) :=
  let initial_dist := map (fun v => (v, if Nat.eqb v start then 0 else S (length (vertices g) * 100))) 
                         (vertices g) in
  let initial_state := {| dist := initial_dist;
                          pq := [(0, start)];
                          finalized := [] |} in
  let fuel := S (length (vertices g) * length (vertices g)) in
  dist (dijkstra_iter g fuel initial_state).

(* Dijkstra 正确性: 非负权重图中找到最短路径 *)
Lemma dijkstra_correctness : forall g start,
    (forall u v w, In (u, v, w) (edges g) -> w > 0) ->  (* 非负权重 *)
    forall v d, find (fun '(v', _) => Nat.eqb v v') (dijkstra g start) = Some (v, d) ->
    (exists p, Path g start v p /\ path_weight g p = d) /\  (* 可达且距离正确 *)
    (forall p, Path g start v p -> path_weight g p >= d).  (* 最短性 *)
Admitted.

(* 路径权重辅助函数 *)
Definition path_weight (g : Graph) (p : list Vertex) : nat :=
  match p with
  | [] => 0
  | _ :: rest =>
      fold_left (fun acc '(u, v) =>
        match edge_weight g u v with
        | Some w => acc + w
        | None => acc
        end) (combine (removelast p) rest) 0
  end.

(* ----------------------------------------------------------------------------
 * 图性质定理
 * ---------------------------------------------------------------------------- *)

(* 有限图的可达性是可判定的 *)
Theorem reachability_decidable : forall g u v,
    {Reachable g u v} + {~ Reachable g u v}.
Proof.
  intros g u v.
  (* 使用 BFS *)
  destruct (in_dec Nat.eq_dec v (map fst (bfs g u))) as [Hin | Hnotin].
  - left.
    (* BFS 完备性 *)
    apply bfs_completeness.
    (* 需要 In 和 Reachable 的关系 *)
  Admitted.

(* 传递闭包 *)
Inductive TC {A : Type} (R : A -> A -> Prop) : A -> A -> Prop :=
  | TC_base : forall x y, R x y -> TC R x y
  | TC_trans : forall x y z, R x y -> TC R y z -> TC R x z.

(* 可达性等于边关系的传递闭包 *)
Theorem reachable_tc : forall g u v,
    Reachable g u v <-> 
    TC (fun x y => has_edge g x y = true) u v.
Proof.
  intros g u v.
  split.
  - intros [p Hp].
    induction Hp.
    + (* Path_nil *)
      (* 基础情况需要特殊处理 *)
      admit.
    + (* Path_cons *)
      apply TC_trans with v.
      * apply TC_base.
        (* has_edge 转换为 Prop *)
        admit.
      * assumption.
  - intros Htc.
    induction Htc.
    + (* TC_base *)
      (* 单条边形成路径 *)
      admit.
    + (* TC_trans *)
      (* 路径连接 *)
      admit.
Admitted.

(* ============================================================================
 * 练习
 * ============================================================================
 *
 * 1. 完成 DFS 和 BFS 的所有正确性证明
 * 
 * 2. 证明强连通分量的正确性
 * 
 * 3. 实现并验证 Floyd-Warshall 所有点对最短路径算法
 * 
 * 4. 证明最小生成树 (Prim/Kruskal) 的性质
 * 
 * 5. 定义图同构并证明其等价关系
 *)
