# Flink 目录重组计划

## 当前问题
- roadmap/: 100个文件 - 严重过载
- 14-rust-assembly-ecosystem/: 70个文件 - 需要拆分
- 分散目录: api-evolution/, ai-ml/, connectors/, deployment/等
- 重复分类: 05-operations/ 和 07-operations/ 都只有1个文件

## 新目录结构

```
Flink/
├── 00-meta/                          # 元信息
│   ├── 00-INDEX.md
│   ├── 00-QUICK-START.md
│   └── version-tracking.md
│
├── 01-concepts/                      # 架构概念
│   ├── 01.01-stream-processing-concepts.md
│   └── 01.02-deployment-architectures.md
│
├── 02-core/                          # 核心机制
│   ├── 02.01-checkpoint-mechanism/
│   ├── 02.02-state-management/
│   ├── 02.03-time-watermark/
│   └── 02.04-adaptive-execution/
│
├── 03-api/                           # API层
│   ├── 03.01-datastream-api/
│   ├── 03.02-table-sql-api/
│   └── 03.03-connector-api/
│
├── 04-runtime/                       # 运行时
│   ├── 04.01-deployment/
│   ├── 04.02-operations/
│   └── 04.03-observability/
│
├── 05-ecosystem/                     # 生态系统
│   ├── 05.01-connectors/
│   ├── 05.02-lakehouse/
│   └── 05.03-wasm-udf/
│
├── 06-ai-ml/                         # AI/ML集成
│   ├── 06.01-ml-inference/
│   ├── 06.02-feature-engineering/
│   └── 06.03-ai-agents/
│
├── 07-rust-native/                   # Rust生态
│   ├── 07.01-rust-engines/
│   ├── 07.02-wasm-integration/
│   └── 07.03-simd-optimization/
│
├── 08-roadmap/                       # 路线图
│   ├── 08.01-flink-24/
│   ├── 08.02-flink-25/
│   ├── 08.03-flink-30/
│   └── 08.04-feature-evolution/
│
├── 09-practices/                     # 工程实践
│   ├── 09.01-case-studies/
│   ├── 09.02-benchmarking/
│   ├── 09.03-performance-tuning/
│   └── 09.04-security/
│
└── 10-legacy/                        # 归档
    └── (旧版本、过时文档)
```

## 迁移映射

| 原目录 | 新目录 | 操作 |
|--------|--------|------|
| 00-INDEX.md | 00-meta/00-INDEX.md | 移动 |
| 00-QUICK-START.md | 00-meta/00-QUICK-START.md | 移动 |
| 01-architecture/ | 01-concepts/ | 重命名 |
| 02-core-mechanisms/ | 02-core/ | 重命名 |
| 03-sql-table-api/ | 03-api/03.02-table-sql-api/ | 移动+重命名 |
| api-evolution/ | 08-roadmap/08.04-feature-evolution/ | 合并 |
| 04-connectors/ | 05-ecosystem/05.01-connectors/ | 移动+合并 |
| connectors/ | 05-ecosystem/05.01-connectors/ | 合并 |
| 05-operations/ + 07-operations/ | 04-runtime/04.02-operations/ | 合并 |
| 06-engineering/ | 09-practices/09.03-performance-tuning/ | 合并 |
| 07-case-studies/ | 09-practices/09.01-case-studies/ | 移动 |
| 08-roadmap/ | 08-roadmap/08.01-flink-24/等 | 拆分 |
| roadmap/ | 08-roadmap/08.04-feature-evolution/ | 拆分+合并 |
| 09-language-foundations/ | 03-api/ | 拆分 |
| 10-deployment/ + deployment/ | 04-runtime/04.01-deployment/ | 合并 |
| 11-benchmarking/ | 09-practices/09.02-benchmarking/ | 移动 |
| 12-ai-ml/ + ai-ml/ | 06-ai-ml/ | 合并 |
| 13-security/ + security/ | 09-practices/09.04-security/ | 合并 |
| 13-wasm/ | 05-ecosystem/05.03-wasm-udf/ | 移动 |
| 14-lakehouse/ | 05-ecosystem/05.02-lakehouse/ | 移动 |
| 14-graph/ | 05-ecosystem/05.04-graph/ | 移动 |
| 14-rust-assembly-ecosystem/ | 07-rust-native/ | 重命名+重组 |
| 15-observability/ + observability/ | 04-runtime/04.03-observability/ | 合并 |
| ecosystem/ | 05-ecosystem/ | 合并 |
| flink-24/, flink-25/, flink-30/ | 08-roadmap/ | 整合 |
| version-tracking/ | 00-meta/ | 移动 |
