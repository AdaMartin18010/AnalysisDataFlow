> **状态**: 🔮 前瞻内容 | **风险等级**: 高 | **最后更新**: 2026-04
> 
> 此文档描述的内容处于早期规划阶段，可能与最终实现不符。请以 Apache Flink 官方发布为准。
# AnalysisDataFlow 技術アーキテクチャドキュメント

> **バージョン**: v1.0 | **更新日**: 2026-04-03 | **ステータス**: 本番環境
>
> 本ドキュメントは AnalysisDataFlow プロジェクトの全体技術アーキテクチャを記述し、ディレクトリ構造、ドキュメント生成フロー、検証システム、ストレージアーキテクチャ、および拡張メカニズムを含みます。

---

## 目次

- [AnalysisDataFlow 技術アーキテクチャドキュメント](#analysisdataflow-技術アーキテクチャドキュメント)
  - [1. プロジェクト全体アーキテクチャ](#1-プロジェクト全体アーキテクチャ)
    - [1.1 4層アーキテクチャ概要](#11-4層アーキテクチャ概要)
    - [1.2 各層の責任とインターフェース](#12-各層の責任とインターフェース)
    - [1.3 データフローと依存関係](#13-データフローと依存関係)
  - [2. ドキュメント生成アーキテクチャ](#2-ドキュメント生成アーキテクチャ)
    - [2.1 Markdown 処理フロー](#21-markdown-処理フロー)
    - [2.2 Mermaid 図表レンダリング](#22-mermaid-図表レンダリング)
  - [3. 検証システムアーキテクチャ](#3-検証システムアーキテクチャ)
    - [3.1 検証スクリプトアーキテクチャ](#31-検証スクリプトアーキテクチャ)
    - [3.2 CI/CD フロー](#32-cicd-フロー)
    - [3.3 品質ゲート](#33-品質ゲート)
  - [4. ストレージアーキテクチャ](#4-ストレージアーキテクチャ)
    - [4.1 ファイル組織構造](#41-ファイル組織構造)
    - [4.2 インデックスシステム](#42-インデックスシステム)
    - [4.3 バージョン管理](#43-バージョン管理)
  - [5. 拡張アーキテクチャ](#5-拡張アーキテクチャ)
    - [5.1 新規ドキュメント追加](#51-新規ドキュメント追加)
    - [5.2 新規可視化追加](#52-新規可視化追加)
  - [付録](#付録)
    - [A. 用語表](#a-用語表)
    - [B. ディレクトリマッピング表](#b-ディレクトリマッピング表)
    - [C. 関連ドキュメント](#c-関連ドキュメント)

---

## 1. プロジェクト全体アーキテクチャ

### 1.1 4層アーキテクチャ概要

AnalysisDataFlow は**4層アーキテクチャ設計**を採用し、形式化理論からエンジニアリング実践までの完全な知識体系を実現します：

```mermaid
graph TB
    subgraph "Layer 1: 形式理論層 Struct/"
        S1[基礎理論<br/>01-foundation]
        S2[性質導出<br/>02-properties]
        S3[関係構築<br/>03-relationships]
        S4[形式証明<br/>04-proofs]
        S5[対比分析<br/>05-comparative]
        S6[最先端探索<br/>06-frontier]
    end

    subgraph "Layer 2: 知識アプリケーション層 Knowledge/"
        K1[概念アトラス<br/>01-concept-atlas]
        K2[デザインパターン<br/>02-design-patterns]
        K3[ビジネスシナリオ<br/>03-business-patterns]
        K4[技術選定<br/>04-technology-selection]
        K5[マッピングガイド<br/>05-mapping-guides]
        K6[最先端技術<br/>06-frontier]
        K7[ベストプラクティス<br/>07-best-practices]
        K8[アンチパターン<br/>09-anti-patterns]
    end

    subgraph "Layer 3: エンジニアリング実装層 Flink/"
        F1[アーキテクチャ設計<br/>01-architecture]
        F2[コアメカニズム<br/>02-core-mechanisms]
        F3[SQL/API<br/>03-sql-table-api]
        F4[コネクター<br/>04-connectors]
        F5[競合対比<br/>05-vs-competitors]
        F6[エンジニアリング実践<br/>06-engineering]
        F7[ケーススタディ<br/>07-case-studies]
        F8[AI/ML<br/>12-ai-ml]
        F9[セキュリティコンプライアンス<br/>13-security]
        F10[可観測性<br/>15-observability]
    end

    subgraph "Layer 4: 可視化ナビゲーション層 visuals/"
        V1[決定木<br/>decision-trees]
        V2[対比マトリックス<br/>comparison-matrices]
        V3[マインドマップ<br/>mind-maps]
        V4[ナレッジグラフ<br/>knowledge-graphs]
        V5[アーキテクチャ図集<br/>architecture-diagrams]
    end

    S6 --> K6
    S4 --> K5
    S1 --> K2
    K2 --> F2
    K3 --> F7
    K4 --> F5
    K6 --> F8

    F7 --> V5
    K4 --> V1
    F5 --> V2
    K1 --> V3
    S3 --> V4
```

### 1.2 各層の責任とインターフェース

#### Layer 1: Struct/ - 形式理論基盤層

| 属性 | 説明 |
|------|------|
| **ポジショニング** | 数学的定義、定理証明、厳密な論証 |
| **コンテンツ特徴** | 形式化言語、公理システム、証明構築 |
| **ドキュメント数** | 43 篇 |
| **コア成果物** | 188 定理、399 定義、158 補題 |

**内部インターフェース仕様**：

```
入力: 学術文献、形式化仕様
出力: Def-* (定義), Thm-* (定理), Lemma-* (補題), Prop-* (命題)
契約: 各定義は唯一の番号を持ち、各定理は完全な証明を持つ必要がある
```

**サブディレクトリ責任**：

- `01-foundation/`: USTM、プロセス計算、Actor、Dataflow 基礎理論
- `02-properties/`: 決定性、一貫性、Watermark 単調性などの性質
- `03-relationships/`: クロスモデルエンコーディング、表現能力階層
- `04-proofs/`: Checkpoint、Exactly-Once 正確性証明
- `05-comparative/`: Go vs Scala 表現力対比
- `06-frontier/`: 未解決問題、Choreographic プログラミング、AI Agent 形式化

#### Layer 2: Knowledge/ - 知識アプリケーション層

| 属性 | 説明 |
|------|------|
| **ポジショニング** | デザインパターン、ビジネスシナリオ、技術選定 |
| **コンテンツ特徴** | エンジニアリング実践、パターンカタログ、決定フレームワーク |
| **ドキュメント数** | 110 篇 |
| **コア成果物** | 45 デザインパターン、15 ビジネスシナリオ |

**内部インターフェース仕様**：

```
入力: Struct/ 形式化定義、業界ケース、エンジニアリング経験
出力: デザインパターンカタログ、技術選定ガイド、ビジネスシナリオ分析
契約: 各パターンは形式化基盤に関連付けられ、各選定は決定マトリックスを持つ必要がある
```

**サブディレクトリ責任**：

- `01-concept-atlas/`: 並行パラダイムマトリックス、概念マップ
- `02-design-patterns/`: イベント時間処理、状態計算、ウィンドウ集計などのパターン
- `03-business-patterns/`: Uber/Netflix/Alibaba などの実ケース
- `04-technology-selection/`: エンジン選定、ストレージ選定、ストリームデータベースガイド
- `05-mapping-guides/`: 理論からコードへのマッピング、移行ガイド
- `06-frontier/`: A2A プロトコル、MCP、リアルタイム RAG、ストリームデータベースエコシステム
- `09-anti-patterns/`: 10 大アンチパターン識別と回避戦略

#### Layer 3: Flink/ - エンジニアリング実装層

| 属性 | 説明 |
|------|------|
| **ポジショニング** | Flink 専門技術、アーキテクチャメカニズム、エンジニアリング実践 |
| **コンテンツ特徴** | ソース分析、設定例、パフォーマンスチューニング |
| **ドキュメント数** | 117 篇 |
| **コア成果物** | 107 Flink 関連定理、コアメカニズム完全カバー |

**内部インターフェース仕様**：

```
入力: Knowledge/ デザインパターン、Flink 公式ドキュメント、ソース分析
出力: アーキテクチャドキュメント、メカニズム詳細、ケーススタディ、ロードマップ
契約: 各メカニズムはソース参照を持ち、各ケースは生産検証を持つ必要がある
```

**サブディレクトリ責任**：

- `01-architecture/`: アーキテクチャ進化、分離状態分析
- `02-core-mechanisms/`: Checkpoint、Exactly-Once、Watermark、Delta Join
- `03-sql-table-api/`: SQL 最適化、Model DDL、Vector Search
- `04-connectors/`: Kafka、CDC、Iceberg、Paimon 統合
- `05-vs-competitors/`: Spark、RisingWave との対比
- `06-engineering/`: パフォーマンスチューニング、コスト最適化、テスト戦略
- `07-case-studies/`: 金融リスク管理、IoT、推薦システムなどのケース
- `12-ai-ml/`: Flink ML、オンライン学習、AI Agents
- `13-security/`: TEE、GPU 信頼性計算
- `15-observability/`: OpenTelemetry、SLO、可観測性

#### Layer 4: visuals/ - 可視化ナビゲーション層

| 属性 | 説明 |
|------|------|
| **ポジショニング** | 決定木、対比マトリックス、マインドマップ、ナレッジグラフ |
| **コンテンツ特徴** | 可視化ナビゲーション、クイック決定、知識概要 |
| **ドキュメント数** | 20 篇 |
| **コア成果物** | 5 種類の可視化、700+ Mermaid 図表 |

**内部インターフェース仕様**：

```
入力: 全プロジェクトドキュメント、定理依存関係、技術選定ロジック
出力: 決定木、対比マトリックス、マインドマップ、ナレッジグラフ
契約: 各可視化はソースドキュメントにナビゲートでき、各決定は条件分岐を持つ必要がある
```

**サブディレクトリ責任**：

- `decision-trees/`: 技術選定決定木、パラダイム選択決定木
- `comparison-matrices/`: エンジン対比マトリックス、モデル対比マトリックス
- `mind-maps/`: 知識マインドマップ、完全なナレッジグラフ
- `knowledge-graphs/`: 概念関係グラフ、定理依存グラフ
- `architecture-diagrams/`: システムアーキテクチャ図、階層アーキテクチャ図

### 1.3 データフローと依存関係

```mermaid
flowchart TB
    subgraph "知識生産フロー"
        direction TB
        A[学術文献<br/>公式ドキュメント] --> B[形式化定義<br/>Struct/]
        B --> C[性質導出<br/>定理証明]
        C --> D[デザインパターン<br/>Knowledge/]
        D --> E[エンジニアリング実装<br/>Flink/]
        E --> F[ケース検証<br/>生産実践]
        F -.->|フィードバック| B
    end

    subgraph "クロス層依存ネットワーク"
        direction LR
        S[Struct] -.->|理論基盤| K[Knowledge]
        K -.->|アプリケーション指導| F[Flink]
        F -.->|実装検証| S
        V[visuals] -.->|可視化ナビゲーション| S
        V -.->|可視化ナビゲーション| K
        V -.->|可視化ナビゲーション| F
    end

    subgraph "参照関係例"
        direction TB
        Def[Def-S-01-01<br/>USTM定義] --> Pattern[イベント時間処理パターン]
        Pattern --> Impl[Flink Watermark実装]
        Impl --> Case[Netflixケース]
        Case -.->|検証| Def
    end
```

**依存ルール**：

1. **単方向依存原則**: Struct → Knowledge → Flink、循環依存を回避
2. **フィードバック検証メカニズム**: Flink エンジニアリング実践が Struct 理論を検証
3. **可視化ナビゲーション**: visuals/ はナビゲーション層として、すべての層を参照可能

---

## 2. ドキュメント生成アーキテクチャ

### 2.1 Markdown 処理フロー

```mermaid
flowchart TD
    A[オリジナルコンテンツ入力] --> B{コンテンツタイプ判定}

    B -->|形式化理論| C[Structプロセッサ]
    B -->|デザインパターン| D[Knowledgeプロセッサ]
    B -->|Flink技術| E[Flinkプロセッサ]
    B -->|可視化| F[visualsプロセッサ]

    C --> G[6セクションテンプレートレンダリング]
    D --> G
    E --> G
    F --> H[可視化テンプレートレンダリング]

    G --> I[定理番号割り当て]
    G --> J[参照解析]
    G --> K[Mermaid図表埋め込み]

    H --> L[決定木生成]
    H --> M[対比マトリックス生成]
    H --> N[マインドマップ生成]

    I --> O[ドキュメント出力]
    J --> O
    K --> O
    L --> O
    M --> O
    N --> O

    O --> P[クロスリファレンスインデックス]
    O --> Q[定理登録表更新]
    O --> R[インデックスファイル更新]
```

**処理段階の説明**：

| 段階 | 機能 | 出力 |
|------|------|------|
| **コンテンツ解析** | ドキュメントタイプ識別、メタデータ抽出 | ドキュメントオブジェクトツリー |
| **テンプレートレンダリング** | 6セクションテンプレートまたは可視化テンプレートを適用 | 構造化 Markdown |
| **番号割り当て** | 定理/定義/補題番号を割り当て | グローバルに唯一の識別子 |
| **参照解析** | 内部/外部参照を解析 | リンクマッピング表 |
| **図表埋め込み** | Mermaid 図表を生成 | 可視化コードブロック |
| **インデックス更新** | 登録表とインデックスを更新 | THEOREM-REGISTRY.md |

### 2.2 Mermaid 図表レンダリング

**図表タイプと使用シナリオ**：

```mermaid
graph LR
    subgraph "図表タイプマトリックス"
        A[graph TB/TD] -->|階層構造<br/>マッピング関係| B[アーキテクチャ図<br/>依存図]
        C[flowchart TD] -->|決定木<br/>フローチャート| D[選定決定<br/>実行フロー]
        E[stateDiagram-v2] -->|状態遷移<br/>実行ツリー| F[状態機械<br/>実行パス]
        G[gantt] -->|ロードマップ<br/>タイムライン| H[バージョン計画<br/>マイルストーン]
        I[classDiagram] -->|タイプ構造<br/>モデル定義| J[クラス階層<br/>型システム]
        K[erDiagram] -->|データ関係<br/>エンティティ関連| L[ERモデル<br/>関係マッピング]
    end
```

**図表レンダリング仕様**：

```markdown
## 7. 可視化 (Visualizations)

### 7.1 階層構造図

以下の図表は XXX の階層構造を示しています：

```mermaid
graph TB
    A[トップ層] --> B[ミドル層1]
    A --> C[ミドル層2]
    B --> D[ボトム層1]
    B --> E[ボトム層2]
    C --> F[ボトム層3]
```

### 7.2 決定フロー図

以下の決定木は XXX の選択に役立ちます：

```mermaid
flowchart TD
    Start[開始] --> Q1{条件1?}
    Q1 -->|はい| A[案A]
    Q1 -->|いいえ| B[案B]
```
```

**レンダリングルール**：
1. 各図表の前にはテキスト説明が必要
2. 図表には明確なタイプ選択理由が必要
3. 複雑な図表には凡例説明が必要
4. 図表のセマンティクスはテキスト説明と一致する必要がある

---

## 3. 検証システムアーキテクチャ

### 3.1 検証スクリプトアーキテクチャ

```mermaid
graph TB
    subgraph "検証パイプライン"
        A[コードコミット] --> B[Pre-commit Hook]
        B --> C[ドキュメント構造検証]
        C --> D[コンテンツ品質検証]
        D --> E[クロスリファレンス検証]
        E --> F[Mermaid構文検証]
        F --> G[リンク有効性検証]

        G -->|通過| H[検証成功]
        G -->|失敗| I[エラーレポート]
        I --> J[修正フィードバック]
        J --> B
    end

    subgraph "検証コンポーネント"
        V1[StructureValidator<br/>6セクションチェック]
        V2[TheoremValidator<br/>番号唯一性]
        V3[ReferenceValidator<br/>参照完全性]
        V4[MermaidValidator<br/>構文チェック]
        V5[LinkValidator<br/>リンク到達性]
        V6[ContentValidator<br/>コンテンツ仕様]
    end

    C --> V1
    C --> V2
    D --> V6
    E --> V3
    F --> V4
    G --> V5
```

**検証コンポーネント詳細説明**：

| 検証コンポーネント | 責任 | 検証ルール |
|-------------------|------|------------|
| **StructureValidator** | 6セクションチェック | 8 つのセクションを含み、順序が正しい必要がある |
| **TheoremValidator** | 定理番号唯一性 | グローバル番号が競合せず、形式が正しい必要がある |
| **ReferenceValidator** | 参照完全性 | 内部リンクが有効で、外部リンクがアクセス可能である必要がある |
| **MermaidValidator** | Mermaid 構文チェック | 図表構文が正しく、レンダリング可能である必要がある |
| **LinkValidator** | リンク有効性 | HTTP 200 応答で、デッドリンクがない必要がある |
| **ContentValidator** | コンテンツ仕様 | 用語が一貫し、形式が統一されている必要がある |

### 3.2 CI/CD フロー

```mermaid
flowchart TB
    subgraph "GitHub Actions ワークフロー"
        A[Push/PR] --> B[ワークフロートリガー]

        B --> C[validate.yml]
        B --> D[update-stats.yml]
        B --> E[check-links.yml]

        C --> C1[構造検証]
        C --> C2[定理番号チェック]
        C --> C3[コンテンツ品質チェック]

        D --> D1[ドキュメント数統計]
        D --> D2[定理数統計]
        D --> D3[ダッシュボード更新]

        E --> E1[リンク到達性]
        E --> E2[外部参照検証]

        C1 & C2 & C3 --> F{すべて通過?}
        F -->|はい| G[ビルド成功]
        F -->|いいえ| H[ビルド失敗]

        G --> I[GitHub Pages へのデプロイ]
        H --> J[エラーレポート生成]
    end
```

**ワークフロー設定**（`.github/workflows/`）：

| ワークフローファイル | トリガー条件 | 責任 |
|---------------------|--------------|------|
| `validate.yml` | Push, PR | ドキュメント構造、定理番号、コンテンツ品質検証 |
| `update-stats.yml` | Push to main | 統計更新、ダッシュボード更新 |
| `check-links.yml` | 毎日定時 | 外部リンク有効性チェック |

### 3.3 品質ゲート

```mermaid
flowchart TD
    subgraph "品質ゲートチェックポイント"
        direction TB

        Q1[ゲート1: 6セクションチェック] -->|必須包含| Q1a[概念定義]
        Q1 -->|必須包含| Q1b[性質導出]
        Q1 -->|必須包含| Q1c[関係構築]
        Q1 -->|必須包含| Q1d[論証過程]
        Q1 -->|必須包含| Q1e[形式証明]
        Q1 -->|必須包含| Q1f[実例検証]
        Q1 -->|必須包含| Q1g[可視化]
        Q1 -->|必須包含| Q1h[引用参考]

        Q2[ゲート2: 番号仕様] --> Q2a[形式: Thm-S-XX-XX]
        Q2 --> Q2b[グローバル唯一性]
        Q2 --> Q2c[連続番号]

        Q3[ゲート3: 可視化要件] --> Q3a[少なくとも1つのMermaid図]
        Q3 --> Q3b[図表前に説明テキスト]
        Q3 --> Q3c[構文が正しい]

        Q4[ゲート4: 参照仕様] --> Q4a[外部参照が検証可能]
        Q4 --> Q4b[内部リンクが有効]
        Q4 --> Q4c[参照形式が統一]

        Q5[ゲート5: 用語一貫性] --> Q5a[用語表と一致]
        Q5 --> Q5b[省略形仕様]
        Q5 --> Q5c[日英対照]
    end
```

---

## 4. ストレージアーキテクチャ

### 4.1 ファイル組織構造

```mermaid
graph TB
    subgraph "プロジェクトルートディレクトリ"
        Root[AnalysisDataFlow/]

        Root --> Config[設定ファイル]
        Root --> Core[コアディレクトリ]
        Root --> Meta[メタデータ]
        Root --> CI[CI/CD]
    end

    subgraph "設定ファイル"
        Config --> README[README.md<br/>プロジェクト概要]
        Config --> AGENTS[AGENTS.md<br/>Agent仕様]
        Config --> ARCH[ARCHITECTURE.md<br/>アーキテクチャドキュメント]
        Config --> License[LICENSE<br/>ライセンス]
    end

    subgraph "コアディレクトリ"
        Core --> Struct[Struct/<br/>43ドキュメント]
        Core --> Knowledge[Knowledge/<br/>110ドキュメント]
        Core --> Flink[Flink/<br/>117ドキュメント]
        Core --> Visuals[visuals/<br/>20ドキュメント]
    end

    subgraph "メタデータ"
        Meta --> Tracking[PROJECT-TRACKING.md<br/>進捗ダッシュボード]
        Meta --> Version[PROJECT-VERSION-TRACKING.md<br/>バージョン追跡]
        Meta --> Registry[THEOREM-REGISTRY.md<br/>定理登録表]
        Meta --> Reports[FINAL-*.md<br/>完了レポート]
    end

    subgraph "CI/CD"
        CI --> Workflows[.github/workflows/<br/>ワークフロー定義]
        CI --> Scripts[scripts/<br/>検証スクリプト]
    end
```

**ファイル命名規約**：

```
{層号}.{番号}-{トピックキーワード}.md

例:
- 01.01-unified-streaming-theory.md    (Struct/01-foundation/)
- 02-design-patterns-overview.md        (Knowledge/02-design-patterns/)
- checkpoint-mechanism-deep-dive.md     (Flink/02-core-mechanisms/)
```

### 4.2 インデックスシステム

```mermaid
erDiagram
    DOCUMENT ||--o{ THEOREM : contains
    DOCUMENT ||--o{ DEFINITION : contains
    DOCUMENT ||--o{ LEMMA : contains
    DOCUMENT ||--o{ REFERENCE : cites

    DOCUMENT {
        string path PK
        string title
        string category
        string stage
        int formalization_level
        int theorem_count
        int definition_count
    }

    THEOREM {
        string id PK
        string document FK
        string statement
        string proof
        string type
    }

    DEFINITION {
        string id PK
        string document FK
        string term
        string definition_text
    }

    REFERENCE {
        string id PK
        string source_document FK
        string target_document FK
        string reference_type
    }
```

**インデックスファイル体系**：

| インデックスファイル | 責任 | 更新頻度 |
|---------------------|------|----------|
| `THEOREM-REGISTRY.md` | 全プロジェクトの定理/定義/補題登録表 | 各新規ドキュメント |
| `PROJECT-TRACKING.md` | 進捗ダッシュボード、タスクステータス | 各イテレーション |
| `PROJECT-VERSION-TRACKING.md` | バージョン履歴、変更ログ | 各バージョン |
| `Struct/00-INDEX.md` | Struct ディレクトリインデックス | 各新規ドキュメントバッチ |
| `Knowledge/00-INDEX.md` | Knowledge ディレクトリインデックス | 各新規ドキュメントバッチ |
| `Flink/00-INDEX.md` | Flink ディレクトリインデックス | 各新規ドキュメントバッチ |
| `visuals/index-visual.md` | 可視化ナビゲーションインデックス | 新規可視化時 |

### 4.3 バージョン管理

```mermaid
gantt
    title バージョンリリースロードマップ
    dateFormat YYYY-MM-DD

    section v1.x
    v1.0 基盤アーキテクチャ       :done, v1_0, 2025-01-01, 30d
    v1.5 コンテンツ拡張       :done, v1_5, after v1_0, 45d

    section v2.x
    v2.0 完全な理論       :done, v2_0, after v1_5, 60d
    v2.5 Flink深化      :done, v2_5, after v2_0, 45d
    v2.8 最先端技術       :done, v2_8, after v2_5, 30d

    section v3.x
    v3.0 最終完了       :active, v3_0, after v2_8, 30d
    v3.x メンテナンス更新       :milestone, v3_m, after v3_0, 90d
```

**バージョン管理戦略**：

| バージョン番号 | 意味 | 更新内容 |
|----------------|------|----------|
| **Major** (X.0) | 重大なアーキテクチャ変更 | ディレクトリ構造調整、番号体系変更 |
| **Minor** (x.X) | 機能拡張 | 新規ドキュメントバッチ、新規トピックカバー |
| **Patch** (x.x.X) | 修正最適化 | エラー修正、リンク更新、形式最適化 |

---

## 5. 拡張アーキテクチャ

### 5.1 新規ドキュメント追加

```mermaid
flowchart TD
    subgraph "新規ドキュメント追加フロー"
        A[ドキュメントタイプ決定] --> B{ディレクトリ選択}

        B -->|形式化理論| C[Struct/]
        B -->|デザインパターン| D[Knowledge/]
        B -->|Flink技術| E[Flink/]
        B -->|可視化| F[visuals/]

        C --> G[サブディレクトリ選択<br/>01-08]
        D --> H[サブディレクトリ選択<br/>01-09]
        E --> I[サブディレクトリ選択<br/>01-15]
        F --> J[サブディレクトリ選択<br/>decision-trees等]

        G & H & I & J --> K[番号割り当て]
        K --> L[ファイル作成<br/>{層号}.{番号}-{トピック}.md]
        L --> M[6セクションテンプレート適用]
        M --> N[定理番号割り当て]
        N --> O[コンテンツ作成]
        O --> P[Mermaid図追加]
        P --> Q[検証とコミット]
    end
```

### 5.2 新規可視化追加

```mermaid
flowchart LR
    subgraph "可視化タイプ選択"
        A[可視化ニーズ] --> B{コンテンツタイプ?}

        B -->|決定ロジック| C[決定木
        decision-trees/]
        B -->|対比分析| D[対比マトリックス
        comparison-matrices/]
        B -->|知識構造| E[マインドマップ
        mind-maps/]
        B -->|関係ネットワーク| F[ナレッジグラフ
        knowledge-graphs/]
        B -->|システムアーキテクチャ| G[アーキテクチャ図集
        architecture-diagrams/]
    end

    subgraph "可視化作成フロー"
        C & D & E & F & G --> H[Markdownファイル作成]
        H --> I[Mermaidタイプ選択]
        I --> J[図表コード作成]
        J --> K[ナビゲーションリンク追加]
        K --> L[visualsインデックス更新]
    end
```

---

## 付録

### A. 用語表

| 用語 | 英語 | 説明 |
|------|------|------|
| 6セクションテンプレート | Six-Section Template | ドキュメント標準構造テンプレート |
| USTM | Unified Streaming Theory Model | 統一ストリームコンピューティング理論モデル |
| Def-* | Definition | 形式化定義番号接頭辞 |
| Thm-* | Theorem | 定理番号接頭辞 |
| Lemma-* | Lemma | 補題番号接頭辞 |
| Prop-* | Proposition | 命題番号接頭辞 |
| Cor-* | Corollary | 推論番号接頭辞 |

### B. ディレクトリマッピング表

| ディレクトリコード | 完全パス | 用途 |
|-------------------|----------|------|
| S | Struct/ | 形式理論 |
| K | Knowledge/ | 知識アプリケーション |
| F | Flink/ | エンジニアリング実装 |
| V | visuals/ | 可視化ナビゲーション |

### C. 関連ドキュメント

- [AGENTS.md](../../AGENTS.md) - Agent ワークコンテキスト仕様
- [PROJECT-TRACKING.md](../../PROJECT-TRACKING.md) - プロジェクト進捗追跡
- [THEOREM-REGISTRY.md](../../THEOREM-REGISTRY.md) - 定理登録表
- [README.md](../../README.md) - プロジェクト概要

---

*本ドキュメントは AnalysisDataFlow アーキテクチャグループによってメンテナンスされ、最終更新: 2026-04-03*

---

> **翻訳者注記**: 本ドキュメントは日本の技術文書スタイルに従って翻訳されています。アーキテクチャの専門用語、システムコンポーネント名、設定パラメータは原文と同一です。最終更新: 2026-04-11
