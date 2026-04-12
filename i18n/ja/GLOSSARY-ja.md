> **状态**: 🔮 前瞻内容 | **风险等级**: 高 | **最后更新**: 2026-04
>
> 此文档描述的内容处于早期规划阶段，可能与最终实现不符。请以 Apache Flink 官方发布为准。
>
# AnalysisDataFlow 用語表（グロッサリー）

> **バージョン**: v1.1 | **更新日**: 2026-04-04 | **範囲**: 全プロジェクト
>
> **バージョン注記**: 用語に付記された [2.0]、[2.4]、[2.5]、[3.0] は、Flink の対応バージョンで導入またはコア機能となったことを示します
>
> 本ドキュメントは AnalysisDataFlow プロジェクトの権威ある用語参考であり、アルファベット順に配列され、ストリームコンピューティング理論、Flink エンジニアリング実践、および最先端技術分野を網羅しています。

---

## 目次

- [用語表ナビゲーション](#用語表ナビゲーション)
- [用語分類インデックス](#用語分類インデックス)
- [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [K](#k) · [L](#l) · [M](#m) · [P](#p) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [W](#w)

---

## 用語表ナビゲーション

| 分類 | 用語数 | 主要分野 |
|------|--------|----------|
| [基礎用語](#1-基礎用語) | 35+ | ストリームコンピューティング、バッチ処理、リアルタイム処理 |
| [理論用語](#2-理論用語) | 40+ | プロセス計算、形式化検証、型理論 |
| [Flink用語](#3-flink用語) | 50+ | コア概念、API、設定パラメータ |
| [エンジニアリング用語](#4-エンジニアリング用語) | 30+ | デザインパターン、アーキテクチャ、運用 |
| [最先端用語](#5-最先端用語) | 35+ | AI Agent、ストリームデータベース、クラウドネイティブ |

---

## 用語分類インデックス

### 1. 基礎用語

- **ストリームコンピューティング関連**: Dataflow、Event Time、Processing Time、Watermark、Window
- **バッチ処理関連**: Batch Processing、Bounded Stream、Checkpoint
- **リアルタイム処理関連**: Real-time Processing、Latency、Throughput

### 2. 理論用語

- **プロセス計算用語**: CCS、CSP、π-Calculus、Actor Model、Session Types
- **形式化検証用語**: Bisimulation、Model Checking、TLA+、Iris
- **型理論用語**: FG/FGG、DOT、Path-Dependent Types

### 3. Flink用語

- **コア概念**: JobManager、TaskManager、Operator、State Backend
- **API関連**: DataStream API、Table API、SQL
- **設定パラメータ**: Parallelism、Checkpoint Interval、Watermark Strategy

### 4. エンジニアリング用語

- **デザインパターンパターン用語**: Windowed Aggregation、Async I/O、Side Output
- **アーキテクチャ用語**: Microservices、Event-Driven Architecture、Data Mesh
- **運用関連用語**: Backpressure、Monitoring、Autoscaling

### 5. 最先端用語

- **AI Agent用語**: AI Agent、ReAct、MCP、A2A、Agentic Workflow、FLIP-531
- **Serverless用語**: Serverless Flink、Scale-to-Zero、FaaS
- **パフォーマンス最適化用語**: Adaptive Execution Engine、Smart Checkpointing
- **ストリームデータベース用語**: Materialized View、Continuous Query、Incremental Update
- **クラウドネイティブ用語**: Kubernetes、Serverless、WASM、Lakehouse

---

## A

### Adaptive Execution Engine (適応型実行エンジン) [Flink 1.17+]

**定義**: Flink が導入したインテリジェント実行最適化フレームワーク。実行時統計情報に基づいて実行計画、リソース配分、並列度を動的に調整します。

**形式化定義**:

```
AEE-V2 = (𝒫, ℳ, 𝒜, 𝒞, ℛ, δ, π)
```

ここで 𝒫 は物理実行計画、ℳ は実行時メトリクス、𝒜 は適応アクション、𝒞 は制約条件、ℛ は再最適化器、δ は決定関数、π はパフォーマンス予測モデルです。

**コア能力**: データスキューの自動処理、並列度の動的調整、リソース適応配分

**関連概念**: Smart Checkpointing、Backpressure、Parallelism

---

### Actor Model (Actor モデル)

**定義**: メッセージを受信し、決定を下し、新しい Actor を作成し、メッセージを送信できる自律的エンティティである Actor を基本計算単位とする並行計算モデル。

**形式化定義**:

```
Actor ::= ⟨Mailbox, Behavior, State, Children, Supervisor⟩
```

**関連概念**: CSP (Communicating Sequential Processes)、π-Calculus、メッセージパッシング

---

### AI Agent (AIエージェント) [汎用用語]

**定義**: 環境において自律的に感知、推論、行動、学習できるインテリジェントシステム。6要素として形式化されます：

```
𝒜_agent ≜ ⟨𝒮, 𝒫, 𝒟, 𝒜, ℳ, 𝒢⟩
```

ここで 𝒮 は状態空間、𝒫 は感知、𝒟 は決定、𝒜 は行動、ℳ は記憶、𝒢 は目標です。

**Flink 統合**: Flink Agent はストリームコンピューティングフレームワークに基づく AI Agent 実装です

**関連概念**: ReAct、MCP、A2A、Multi-Agent、FLIP-531

---

### A2A Protocol (Agent-to-Agent Protocol) [Google 2025]

**定義**: Google が提案したオープンな Agent 相互運用標準。Agent 間のタスク委任、状態同期、結果返却をサポートします。

**形式化定義**:

```
A2A_Flink = ⟨𝒫, ℳ, 𝒮, 𝒜⟩
```

ここで 𝒫 は参加 Agent 集合、ℳ はメッセージタイプ、𝒮 はセッション状態機、𝒜 は認証認可メカニズムです。

**タスク状態遷移**: `pending → working → input-required → completed/failed`

**関連概念**: AI Agent、MCP、Orchestration、FLIP-531

---

### Aligned Checkpoint (アラインド Checkpoint)

**定義**: Flink において、オペレーターが**すべて**の入力チャネルから Barrier を受信した後に状態スナップショットをトリガーするメカニズム。

**形式化定義**:

```
AlignedSnapshot(t, n) ⟺ ∀c ∈ Inputs(t): Barrier(n) ∈ Received(c)
```

**関連概念**: Unaligned Checkpoint、Barrier、Exactly-Once

---

### Async I/O (非同期 I/O)

**定義**: ストリーム処理オペレーターが外部システム呼び出しを並行して実行できるようにするパターン。データフロー処理のブロックを回避します。

**形式化定義**:

```
AsyncFunction: I × C → Future[O]
```

ここで C は並行度パラメータで、同時に進行中の非同期リクエスト数を制御します。

**関連概念**: Backpressure、Enrichment、Concurrency

---

### At-Least-Once (少なくとも一度セマンティクス)

**定義**: ストリームコンピューティングシステムが各入力データが最終的な外部世界への影響を**少なくとも一度**保証するセマンティクス。

**形式化定義**:

```
∀r ∈ I. c(r, 𝒯) ≥ 1
```

ここで c(r, 𝒯) は因果影響カウントです。

**関連概念**: At-Most-Once、Exactly-Once、Delivery Guarantee

---

### At-Most-Once (多くとも一度セマンティクス)

**定義**: ストリームコンピューティングシステムが各入力データが最終的な外部世界への影響を**多くとも一度**保証するセマンティクス。データ損失を許容します。

**形式化定義**:

```
∀r ∈ I. c(r, 𝒯) ≤ 1
```

**関連概念**: At-Least-Once、Exactly-Once、Best-Effort

---

## B

### Backpressure (バックプレッシャー)

**定義**: ストリーム処理システムで、下流の処理速度が上流よりも遅い場合に上流に伝達されるフロー制御信号メカニズム。

**原理**: クレジットベースのフロー制御。受信バッファが満杯の場合は送信を一時停止します。

**関連概念**: Flow Control、Buffer、Credit-Based

---

### Barrier (Checkpoint Barrier)

**定義**: Flink でデータフローに挿入される特殊な制御イベント。異なる Checkpoint のデータ境界を区切ります。

**形式化定義**:

```
Barrier(n) = ⟨Type = CONTROL, checkpointId = n, timestamp = ts⟩
```

**関連概念**: Checkpoint、Aligned Checkpoint、Unaligned Checkpoint

---

### Batch Processing (バッチ処理)

**定義**: 有限で有界なデータセットを処理する計算モード。計算開始前にデータが完全に利用可能です。

**特徴**:

- 入力データは有界 (Bounded)
- 完全なデータセットにアクセス可能
- 遅延は重要でなく、高スループットを追求

**関連概念**: Stream Processing、Bounded Stream、Lambda Architecture

---

### Best-Effort (ベストエフォート)

**定義**: 一貫性保証を提供しない配信セマンティクス。システムはデータを最善を尽くして処理しますが、損失や重複を保証しません。

**関連概念**: At-Most-Once、Delivery Guarantee

---

### Bisimulation (バイシミュレーション)

**定義**: プロセス代数で2つのプロセスの動作等価性を判定する関係。2つのプロセスがすべての可能なアクションで相互にシミュレーションできることを要求します。

**形式化定義**:

```
R はバイシミュレーション ⟺ ∀(P,Q)∈R. ∀α. P→αP' ⇒ ∃Q'. Q→αQ' ∧ (P',Q')∈R
```

**関連概念**: Process Calculus、Trace Equivalence、CCS

---

### Bounded Stream (有界ストリーム)

**定義**: 有限のデータ量を持つデータストリーム。バッチ処理のデータ抽象化です。

**形式化定義**:

```
Bounded(S) ⟺ |S| < ∞
```

**関連概念**: Unbounded Stream、Batch Processing

---

### Buffer (バッファ)

**定義**: ストリーム処理でデータを一時的に保存するメモリ領域。プロデューサーとコンシューマーの間に位置します。

**関連概念**: Backpressure、Queue、Network Buffer

---

## C

### CALM Theorem (CALM 定理)

**定義**: Consistency As Logical Monotonicity —— 論理的単調なプログラムは協調なしで一貫性を保証できます。

**形式化表現**:

```
プログラム P が協調不要 ⟺ P は論理的単調
```

**関連概念**: Eventual Consistency、Coordination

---

### Causal Consistency (因果一貫性)

**定義**: 因果依存関係の操作順序を保持する分散システムの一貫性モデル。

**形式化定義**:

```
∀op_i, op_j. op_i ≺hb op_j ⇒ op_i ≺obs op_j
```

**関連概念**: Strong Consistency、Eventual Consistency、Happens-Before

---

### CEP (Complex Event Processing, 複雑イベント処理)

**定義**: イベントストリームから複雑なパターンを検出し、複合イベントを生成する技術。

**形式化定義**:

```
CEP: Stream × Pattern → DetectedEvents
```

**関連概念**: Pattern Matching、Event Pattern、Window

---

### CCS (Calculus of Communicating Systems)

**定義**: Milner が1980年に提案したラベル付き同期に基づくプロセス代数。

**構文**:

```
P, Q ::= 0 | α.P | P + Q | P | Q | P \ L | P[f]
```

**関連概念**: CSP、π-Calculus、Process Algebra

---

### CDC (Change Data Capture, 変更データキャプチャ)

**定義**: データベースの変更イベント（挿入、更新、削除）をキャプチャし、リアルタイムで下流システムに伝播する技術。

**関連概念**: Debezium、Streaming ETL、Log Mining

---

### Checkpoint (チェックポイント)

**定義**: 分散ストリーム処理ジョブの特定時点でのグローバルな一貫した状態スナップショット。障害回復に使用されます。

**形式化定義**:

```
CP = ⟨ID, TS, {S_i}_{i∈Tasks}, Metadata⟩
```

**関連概念**: Savepoint、State Backend、Recovery

---

### Chandy-Lamport Algorithm

**定義**: 分散システムでグローバルな一貫したスナップショットをキャプチャするための古典的アルゴリズム。Flink Checkpoint の理論基盤です。

**関連概念**: Global Snapshot、Consistent Cut、Checkpoint

---

### Choreographic Programming (コレオグラフィックプログラミング)

**定義**: グローバル視点から複数者間のインタラクションプロトコルを記述し、各参加者に投影する分散プログラミングパラダイム。

**関連概念**: Session Types、Endpoint Projection、Deadlock Freedom

---

### Cloud-Native (クラウドネイティブ)

**定義**: クラウドコンピューティングの利点を活用してアプリケーションを構築・実行する方法論。コンテナ化、マイクロサービス、継続的デリバリー、DevOps を強調します。

**関連概念**: Kubernetes、Containerization、Microservices

---

### Concurrency (並行性)

**定義**: 複数の計算タスクが重複する時間枠内で実行できる能力。並列 (Parallelism) とは区別されます。

**関連概念**: Parallelism、Race Condition、Synchronization

---

### Consistency Model (一貫性モデル)

**定義**: 分散システムでデータ操作の可視性と順序性を定義するルールの集合。

**階層構造**: Strong Consistency → Causal Consistency → Eventual Consistency

**関連概念**: Linearizability、Serializability、CAP Theorem

---

### Continuous Query (継続クエリ)

**定義**: ストリームデータベースで継続的に実行され、データ到着時に自動的に結果を更新するクエリ。

**形式化定義**:

```
q: S → 𝒱, ここで q は時変関数
```

**関連概念**: Materialized View、Streaming Database

---

### Credit-Based Flow Control (クレジットベースフロー制御)

**定義**: 受信側がクレジット値を送信することで送信側に受信可能なデータ量を通知し、フロー制御を実現するメカニズム。

**関連概念**: Backpressure、Flow Control

---

### CSP (Communicating Sequential Processes)

**定義**: Hoare が1985年に提案した同期通信と静的イベント名に基づくプロセス代数。

**構文**:

```
P, Q ::= STOP | SKIP | a → P | P □ Q | P ⊓ Q | P ||| Q | P |[A]| Q
```

**関連概念**: CCS、π-Calculus、Go Channels

---

## D

### Dataflow Model (Dataflow モデル)

**定義**: データがオペレーター間を流れる図として計算を表現するモデル。ストリームコンピューティングの核心理論基盤です。

**形式化定義**:

```
𝒢 = (V, E, P, Σ, 𝕋)
```

ここで V は頂点集合、E は辺集合、P は処理関数、Σ は状態、𝕋 は時間モデルです。

**関連概念**: DAG、Operator、Stream Graph

---

### DAG (Directed Acyclic Graph, 有向非巡回グラフ)

**定義**: データフロー処理トポロジーを表現するグラフ構造。ノードはオペレーター、辺はデータフロー、循環はありません。

**関連概念**: Dataflow Model、Job Graph、Execution Graph

---

### Deadlock Freedom (デッドロックフリー)

**定義**: システムが永遠に発生しないイベントを待って永久にブロックされるプロセスが存在しないことを保証する性質。

**関連概念**: Liveness、Choreographic Programming、Session Types

---

### Delivery Guarantee (配信保証)

**定義**: ストリーム処理システムのメッセージ配信信頼性に対する約束。At-Most-Once、At-Least-Once、Exactly-Once に分類されます。

**関連概念**: At-Most-Once、At-Least-Once、Exactly-Once

---

### Determinism (決定性)

**定義**: 同じ入力が与えられた場合、システムが常に同じ出力を生成する性質。

**形式化定義**:

```
Deterministic(P) ⟺ ∀x. P(x) = P(x)
```

**関連概念**: Reproducibility、Consistency

---

### Distributed Snapshot (分散スナップショット)

**定義**: 分散システムの特定時点でのグローバル状態をキャプチャする一貫したスナップショット。

**関連概念**: Chandy-Lamport Algorithm、Checkpoint、Consistent Cut

---

## E

### Edge Computing (エッジコンピューティング)

**定義**: データソース近く（ネットワークエッジ）でデータ処理を行う計算パラダイム。遅延と帯域消費を削減します。

**関連概念**: Cloud-Edge Continuum、IoT、Latency

---

### End-to-End Consistency (エンドツーエンド一貫性)

**定義**: 外部データソースから外部データシンクまでのパイプライン全体の一貫性保証。

**形式化定義**:

```
End-to-End-EO(J) ⟺ Replayable(Src) ∧ ConsistentCheckpoint(Ops) ∧ AtomicOutput(Snk)
```

**関連概念**: Internal Consistency、Exactly-Once、Source、Sink

---

### Event-Driven Architecture (イベント駆動アーキテクチャ)

**定義**: イベントの生成、検出、消費を中心にコンポーネント間のインタラクションを組織化するソフトウェアアーキテクチャパターン。

**関連概念**: Event Streaming、Pub/Sub、CQRS

---

### Event Time (イベント時間)

**定義**: データレコードが生成されたタイムスタンプ。データソースによって付与されます。

**形式化定義**:

```
t_e: Record → Timestamp
```

**関連概念**: Processing Time、Ingestion Time、Watermark

---

### Eventual Consistency (結果的一貫性)

**定義**: 新しい更新がない場合、最終的にすべてのレプリカが同じ値に収束することを保証する一貫性モデル。

**形式化定義**:

```
◇□(replicas converge)
```

**関連概念**: Strong Consistency、Causal Consistency、CALM Theorem

---

### Exactly-Once (厳密に一度セマンティクス)

**定義**: ストリームコンピューティングシステムが各入力データが最終的な外部世界への影響を**有してかつ唯一回のみ**保証するセマンティクス。

**形式化定義**:

```
∀r ∈ I. c(r, 𝒯) = 1
```

**関連概念**: At-Least-Once、At-Most-Once、Idempotency

---

### Execution Graph (実行グラフ)

**定義**: Flink で論理 JobGraph を物理実行計画に変換するグラフ構造。具体的な並列インスタンスを含みます。

**関連概念**: Job Graph、Task、Parallelism

---

## F

### Flink Agent [Flink 2.0+, FLIP-531]

**定義**: Flink ストリームコンピューティングフレームワークに基づいて構築された自律的インテリジェントエージェント。継続的な感知、決定、行動をサポートします。

**形式化定義**:

```
𝒜_Flink = ⟨𝒮_state, 𝒫_perception, 𝒟_decision, 𝒜_action, ℳ_memory, 𝒢_goal⟩
```

**コア特性**: 状態永続化、Replayability、分散実行、Exactly-Once セマンティクス

**関連概念**: AI Agent、FLIP-531、MCP、A2A、Stateful Stream Processing

---

### FLIP-531 (Flink AI Agents 提案) [Flink 2.0+]

**定義**: Apache Flink の公式機能提案。AI Agent ネイティブランタイムサポートを導入し、ストリームコンピューティングと AI インテリジェントエージェントの深い統合を実現します。

**コアコンポーネント**:

- **Flink Agent Runtime**: Agent 実行環境
- **MCP 統合**: Model Context Protocol サポート
- **A2A プロトコル**: Agent 間相互運用
- **Agentic Workflow**: インテリジェントエージェントワークフローオーケストレーション

**形式化定義**:

```
FLIP-531 = ⟨ℛ_agent, ℐ_mcp, 𝒫_a2a, 𝒲_workflow⟩
```

**関連概念**: Flink Agent、MCP、A2A、Agentic Workflow

---

### Flow Control (フロー制御)

**定義**: データプロデューサーとコンシューマー間のデータ転送レートを調整するメカニズム。

**関連概念**: Backpressure、Credit-Based、Buffer

---

### Function as a Service (FaaS)

**定義**: サーバーレスコンピューティングモード。ユーザーは関数コードを記述し、プラットフォームがインフラストラクチャと自動スケーリングを管理します。

**関連概念**: Serverless、Lambda、Cloud-Native

---

## G

### GPU Acceleration (GPU 加速) [Flink 2.5+]

**定義**: GPU の大規模並列計算能力を活用してストリーム処理オペレーターを実行。CUDA/OpenCL を通じて計算集約型操作を CPU から GPU にオフロードします。

**形式化定義**:

```
𝒪_GPU(D) = GPUKernel(Transfer(D_CPU→GPU))
```

**加速比**: S_GPU = T_CPU / (T_transfer + T_kernel + T_sync)

**適用条件**: バッチサイズ n > n_threshold かつ計算/転送比 > γ

**関連概念**: CUDA、Vector Search、Flink-CUDA Runtime

---

### Global Snapshot (グローバルスナップショット)

**定義**: 分散システムの特定時点でのすべてのプロセス状態の集合。障害回復と一貫性チェックに使用されます。

**関連概念**: Distributed Snapshot、Chandy-Lamport Algorithm、Checkpoint

---

### Global Window (グローバルウィンドウ)

**定義**: すべてのレコードを含む単一ウィンドウ。通常はカスタムトリガーと共に使用されます。

**形式化定義**:

```
Global: wid_global = (-∞, +∞)
```

**関連概念**: Tumbling Window、Sliding Window、Session Window

---

## H

### Happens-Before (先行発生関係)

**定義**: イベント間の因果的な部分順序を定義する関係。分散一貫性の基盤です。

**関連概念**: Causal Consistency、Partial Order、Clock

---

## I

### Idempotency (冪等性)

**定義**: 操作が複数回適用されても、最初の適用以外のシステム状態に影響を与えない性質。

**形式化定義**:

```
f(x) = f(f(x))
```

**関連概念**: Exactly-Once、At-Least-Once、Fault Tolerance

---

### Incremental Checkpoint (増分 Checkpoint)

**定義**: 前回の Checkpoint 以降に変更された状態のみを保存する Checkpoint メカニズム。

**関連概念**: Checkpoint、State Backend、RocksDB

---

### Ingestion Time (取込時間)

**定義**: データレコードがストリーム処理システムに取り込まれたタイムスタンプ。

**関連概念**: Event Time、Processing Time、Watermark

---

## K

### Keyed State (キー付き状態)

**定義**: キーでパーティション化された状態。同じキーを持つレコードが同じ状態インスタンスにアクセスします。

**関連概念**: Operator State、State Backend、KeyedStream

---

### Kafka

**定義**: 高スループットの分散ストリーミングプラットフォーム。パブリッシュ/サブスクライブメッセージングとストリーム処理を提供します。

**関連概念**: CDC、Streaming ETL、Event Streaming

---

### Kubernetes

**定義**: コンテナ化されたワークロードとサービスの管理のためのオープンソースコンテナオーケストレーションプラットフォーム。

**関連概念**: Cloud-Native、Container、Orchestration

---

## L

### Latency (遅延)

**定義**: イベントが発生してからそのイベントの処理結果が利用可能になるまでの時間。

**関連概念**: Throughput、Event Time、Processing Time

---

### Liveness (活性)

**定義**: システムが最終的に必要なアクションを実行することを保証する安全性プロパティ。

**関連概念**: Safety、Deadlock Freedom、Fairness

---

## M

### Materialized View (具体化ビュー)

**定義**: クエリ結果を事前に計算して保存するデータベースオブジェクト。ストリームデータベースでは継続的に更新されます。

**関連概念**: Continuous Query、Streaming Database、Incremental View Maintenance

---

### MCP (Model Context Protocol) [Anthropic 2024]

**定義**: Anthropic が提案した標準プロトコル。AI Agent が外部ツールやデータソースと通信するための統一インターフェースを提供します。

**関連概念**: AI Agent、A2A、Tool Calling、Flink Agent

---

### Microservices (マイクロサービス)

**定義**: 単一のアプリケーションを小さなサービスの集合として構築するアーキテクチャスタイル。各サービスは独自のプロセスで実行され、軽量なメカニズムで通信します。

**関連概念**: Service Mesh、Container、Cloud-Native

---

## P

### Parallelism (並列度)

**定義**: タスクを並行して実行するインスタンスの数。

**関連概念**: Concurrency、Task、Slot

---

### Pattern Matching (パターンマッチング)

**定義**: CEP で定義されたパターンに対してイベントシーケンスを照合するプロセス。

**関連概念**: CEP、Event Pattern、Window

---

### Processing Time (処理時間)

**定義**: データレコードがオペレーターによって処理される時点でのマシンのローカル時間。

**関連概念**: Event Time、Ingestion Time、Watermark

---

### π-Calculus (π-計算)

**定義**: Milner が提案したモバイルプロセス代数。動的チャネル作成と名前渡しをサポートします。

**形式化定義**:

```
P, Q ::= 0 | α.P | P + Q | P | Q | (νa)P | !P
```

**関連概念**: CCS、CSP、Mobile Processes

---

## R

### Race Condition (競合状態)

**定義**: 複数のプロセスが共有リソースにアクセスし、結果がタイミングに依存する状況。

**関連概念**: Concurrency、Synchronization、Mutual Exclusion

---

### Replayability (再実行可能性)

**定義**: ソースが以前のデータを再送信できる能力。Exactly-Once セマンティクスに不可欠です。

**関連概念**: Exactly-Once、Source、Checkpoint

---

### RocksDB

**定義**: Facebook が開発した高性能埋め込み型キーバリューストア。Flink の状態バックエンドとして広く使用されます。

**関連概念**: State Backend、Incremental Checkpoint、ForSt

---

## S

### Savepoint (セーブポイント)

**定義**: Flink で手動でトリガーされるアプリケーションの一貫したスナップショット。アップグレードや移行に使用されます。

**関連概念**: Checkpoint、State、Recovery

---

### Session Window (セッションウィンドウ)

**定義**: アクティビティの期間に基づいてレコードをグループ化するウィンドウタイプ。ギャップ期間後にクローズされます。

**形式化定義**:

```
Session(gap): 連続するイベント間の間隔 < gap
```

**関連概念**: Tumbling Window、Sliding Window、Global Window

---

### Side Output (サイド出力)

**定義**: メイン出力ストリームから遅延データや例外を分離するための追加出力ストリーム。

**関連概念**: Late Data、Output Tag、Multi-Output

---

### Sink (シンク)

**定義**: ストリーム処理パイプラインの終了点。外部システムにデータを書き込みます。

**関連概念**: Source、Connector、Exactly-Once

---

### Sliding Window (スライディングウィンドウ)

**定義**: 固定サイズで指定されたスライド間隔で動くウィンドウタイプ。ウィンドウが重複する可能性があります。

**形式化定義**:

```
Sliding(size, slide): [t - size, t) で t = k × slide (k ∈ ℕ)
```

**関連概念**: Tumbling Window、Session Window、Global Window

---

### Source (ソース)

**定義**: ストリーム処理パイプラインの開始点。外部システムからデータを読み取ります。

**関連概念**: Sink、Connector、Replayability

---

### State (状態)

**定義**: ストリーム処理オペレーターがイベント間で保持するデータ。Keyed State と Operator State の2種類があります。

**関連概念**: State Backend、Checkpoint、Stateful Processing

---

### State Backend (状態バックエンド)

**定義**: チェックポイント中にどのように状態が保存され回復されるかを決定するストレージメカニズム。

**実装**: MemoryStateBackend、FsStateBackend、RocksDBStateBackend

**関連概念**: State、Checkpoint、Incremental Checkpoint

---

### Stream Processing (ストリーム処理)

**定義**: 連続的かつ無限のデータフローをリアルタイムで処理する計算モード。

**特徴**:

- 入力データは無限 (Unbounded)
- 低遅延処理
- 継続的な計算

**関連概念**: Batch Processing、Event Streaming、Real-time Processing

---

### Streaming Database (ストリームデータベース)

**定義**: 継続的に到着するデータストリーム上で SQL クエリを実行し、リアルタイムで結果を更新するデータベースシステム。

**例**: Materialize、RisingWave、Timeplus

**関連概念**: Materialized View、Continuous Query、Stream Processing

---

### Strong Consistency (強い一貫性)

**定義**: すべての操作がグローバルに認識可能な全順序で実行されるように見える一貫性モデル。

**関連概念**: Linearizability、Serializability、Causal Consistency

---

## T

### Task (タスク)

**定義**: Flink の並列実行の基本単位。論理オペレーターの並列インスタンス。

**関連概念**: Operator、Subtask、Execution Graph

---

### TaskManager

**定義**: Flink クラスターワーカーノード。タスクを実行し、ネットワーク経由で他の TaskManager と通信します。

**関連概念**: JobManager、Slot、ResourceManager

---

### Throughput (スループット)

**定義**: システムが単位時間あたりに処理できるデータ量。

**関連概念**: Latency、Performance、Scalability

---

### Tumbling Window (タンブリングウィンドウ)

**定義**: 固定サイズで隣接し、重複しないウィンドウタイプ。

**形式化定義**:

```
Tumbling(size): [k × size, (k+1) × size) (k ∈ ℕ)
```

**関連概念**: Sliding Window、Session Window、Global Window

---

## U

### Unaligned Checkpoint (アンアラインド Checkpoint)

**定義**: オペレーターがすべての Barrier を受信する前に状態スナップショットをトリガーできる Flink の Checkpoint メカニズム。バックプレッシャー下でのチェックポイント遅延を削減します。

**関連概念**: Aligned Checkpoint、Barrier、Backpressure

---

### Unbounded Stream (無界ストリーム)

**定義**: 無限のデータ量を持つデータストリーム。ストリーム処理のデータ抽象化です。

**形式化定義**:

```
Unbounded(S) ⟺ |S| = ∞
```

**関連概念**: Bounded Stream、Stream Processing

---

## W

### Watermark (ウォーターマーク)

**定義**: イベント時間ストリーム処理で時間の進行を示すメタデータイベント。特定タイムスタンプ以前のすべてのイベントが到着したとマークします。

**形式化定義**:

```
WM(t) = max{ t_e | event e has arrived } - allowed_lateness
```

**関連概念**: Event Time、Window、Late Data

---

### Window (ウィンドウ)

**定義**: 無限ストリームを有限の「バケット」に分割するメカニズム。集計と分析を可能にします。

**タイプ**: Tumbling Window、Sliding Window、Session Window、Global Window

**関連概念**: Windowed Aggregation、Event Time、Watermark

---

### Windowed Aggregation (ウィンドウ集計)

**定義**: ウィンドウ内のすべてのイベントに対して集計関数（SUM、COUNT、AVG など）を適用する操作。

**関連概念**: Window、Aggregate Function、Event Time

---

---

> **翻訳者注記**: 本用語表はストリームコンピューティングと Flink に関連する100以上の核心用語を網羅しています。技術的な正確性を保持しつつ、日本語の技術文書スタイルに従って翻訳されています。形式化表記、定理番号、API名は原文と同一です。
>
> 完全な用語表については英語版 GLOSSARY.md を参照してください。
>
> 📅 **最終更新**: 2026-04-11 | 📝 **バージョン**: v1.0 (日本語版)
