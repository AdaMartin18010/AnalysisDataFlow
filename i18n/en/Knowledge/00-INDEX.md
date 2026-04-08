---
title: "[EN] 00 Index"
translation_status: "ai_translated"
source_file: "Knowledge/00-INDEX.md"
source_version: "4a363284"
translator: "AI"
reviewer: null
translated_at: "2026-04-08T15:15:06.331017"
reviewed_at: null
quality_score: null
terminology_verified: false
---


<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->

<!-- TRANSLATE: # Knowledge/ 知识结构导航索引 -->

<!-- TRANSLATE: > 所属阶段: Knowledge | 前置依赖: [../README.md](../README.md), [../QUICK-START.md](../QUICK-START.md) | 形式化等级: L3-L5 -->

<!-- TRANSLATE: ## 简介 -->

<!-- TRANSLATE: 本目录收录流计算领域的**知识结构、设计模式、业务建模、技术选型**等实践性文档。与 `Struct/` 的理论严格性不同，`Knowledge/` 聚焦于工程实践中的知识组织、模式提炼和经验总结。 -->

<!-- TRANSLATE: **核心定位**: -->

<!-- TRANSLATE: - 🗺️ 概念图谱: 流计算核心概念的系统性梳理 -->
<!-- TRANSLATE: - 🎨 设计模式: 可复用的流处理架构模式 -->
<!-- TRANSLATE: - 💼 业务场景: 行业典型应用与解决方案 -->
<!-- TRANSLATE: - ⚖️ 技术选型: 引擎、存储、架构的选择指南 -->
<!-- TRANSLATE: - 🔄 映射指南: 理论到实践、旧系统到新系统的迁移路径 -->
<!-- TRANSLATE: - 🚀 前沿探索: 实时AI、Serverless、Data Mesh等新兴方向 -->
<!-- TRANSLATE: - ✅ 最佳实践: 生产环境检查清单与调优指南 -->
<!-- TRANSLATE: - 📋 标准规范: 数据治理、安全合规规范 -->
<!-- TRANSLATE: - ⚠️ 反模式: 常见陷阱与规避策略 -->
<!-- TRANSLATE: - 📚 案例研究: 真实生产案例分析 -->


<!-- TRANSLATE: ## 01. 概念图谱 (Concept Atlas) -->

<!-- TRANSLATE: 流计算核心概念的系统性梳理与可视化。 -->

<!-- TRANSLATE: | 文档 | 描述 | 适用场景 | -->
<!-- TRANSLATE: |------|------|----------| -->
<!-- TRANSLATE: | [concurrency-paradigms-matrix.md](01-concept-atlas/concurrency-paradigms-matrix.md) | 并发范式对比矩阵: Actor vs CSP vs Dataflow vs Thread 的全维度对比 | 技术选型、架构设计、团队培训 | -->
<!-- TRANSLATE: | [data-streaming-landscape-2026-complete.md](01-concept-atlas/data-streaming-landscape-2026-complete.md) | 2026年流计算全景图: 引擎、数据库、生态系统的完整梳理 | 行业调研、技术战略、投资决策 | -->
<!-- TRANSLATE: | [streaming-models-mindmap.md](01-concept-atlas/streaming-models-mindmap.md) | 流计算模型思维导图: 从理论模型到工程实现的知识地图 | 学习路径规划、知识体系构建 | -->


<!-- TRANSLATE: ## 03. 业务场景 (Business Patterns) -->

<!-- TRANSLATE: 各行业流计算典型应用场景与解决方案。 -->

<!-- TRANSLATE: | 文档 | 描述 | 适用场景 | -->
<!-- TRANSLATE: |------|------|----------| -->
<!-- TRANSLATE: | [fintech-realtime-risk-control.md](03-business-patterns/fintech-realtime-risk-control.md) | 金融实时风控: 反欺诈、信用评估、交易监控 | 银行、支付、保险、证券 | -->
<!-- TRANSLATE: | [real-time-recommendation.md](03-business-patterns/real-time-recommendation.md) | 实时推荐系统: 个性化推荐、实时特征更新 | 电商、内容平台、社交媒体 | -->
<!-- TRANSLATE: | [iot-stream-processing.md](03-business-patterns/iot-stream-processing.md) | IoT流处理: 设备数据采集、边缘计算、实时监控 | 智能制造、车联网、能源管理 | -->
<!-- TRANSLATE: | [log-monitoring.md](03-business-patterns/log-monitoring.md) | 日志监控与告警: 集中采集、实时分析、智能告警 | 运维可观测、DevOps、SRE | -->
<!-- TRANSLATE: | [alibaba-double11-flink.md](03-business-patterns/alibaba-double11-flink.md) | 阿里双11实时计算: 超大规模流处理架构 | 大促活动、流量峰值、电商核心系统 | -->
<!-- TRANSLATE: | [netflix-streaming-pipeline.md](03-business-patterns/netflix-streaming-pipeline.md) | Netflix实时数据处理: 播放体验优化、内容推荐 | 视频流媒体、用户体验优化 | -->
<!-- TRANSLATE: | [uber-realtime-platform.md](03-business-patterns/uber-realtime-platform.md) | Uber实时平台: 供需匹配、动态定价、ETA计算 | 共享经济、出行服务、物流调度 | -->
<!-- TRANSLATE: | [spotify-music-recommendation.md](03-business-patterns/spotify-music-recommendation.md) | Spotify音乐推荐: 实时音乐推荐与发现 | 音乐平台、内容发现、个性化体验 | -->
<!-- TRANSLATE: | [stripe-payment-processing.md](03-business-patterns/stripe-payment-processing.md) | Stripe支付处理: 实时支付风控与对账 | 支付处理、金融科技、交易合规 | -->
<!-- TRANSLATE: | [gaming-analytics.md](03-business-patterns/gaming-analytics.md) | 游戏实时分析: 玩家行为、反作弊、运营决策 | 游戏行业、实时运营、玩家体验 | -->
<!-- TRANSLATE: | [airbnb-marketplace-dynamics.md](03-business-patterns/airbnb-marketplace-dynamics.md) | Airbnb市场动态: 供需平衡、定价策略、搜索排序 | 双边市场、平台经济、动态定价 | -->
<!-- TRANSLATE: | [data-mesh-streaming-architecture-2026.md](03-business-patterns/data-mesh-streaming-architecture-2026.md) | Data Mesh流式架构: 域驱动数据产品、自助服务 | 大型企业、数据平台、组织架构变革 | -->
<!-- TRANSLATE: | [streaming-data-product-economics.md](03-business-patterns/streaming-data-product-economics.md) | 流数据产品经济学: 成本模型、价值评估、ROI分析 | 数据产品管理、成本控制、价值度量 | -->


<!-- TRANSLATE: ## 05. 映射指南 (Mapping Guides) -->

<!-- TRANSLATE: 理论到代码、旧系统到新系统的迁移路径。 -->

<!-- TRANSLATE: | 文档 | 描述 | 适用场景 | -->
<!-- TRANSLATE: |------|------|----------| -->
<!-- TRANSLATE: | [struct-to-flink-mapping.md](05-mapping-guides/struct-to-flink-mapping.md) | Struct到Flink映射: 理论概念到Flink API的对应关系 | 理论学习后的工程实践、API选择 | -->
<!-- TRANSLATE: | [theory-to-code-patterns.md](05-mapping-guides/theory-to-code-patterns.md) | 理论到代码模式: 进程演算、类型理论到实现 | 学术研究转工程、形式化方法应用 | -->
<!-- TRANSLATE: | [migration-guides/05.1-spark-streaming-to-flink-migration.md](05-mapping-guides/migration-guides/05.1-spark-streaming-to-flink-migration.md) | Spark Streaming迁移到Flink: 代码转换、语义映射 | Spark用户迁移、技术栈统一 | -->
<!-- TRANSLATE: | [migration-guides/05.2-kafka-streams-to-flink-migration.md](05-mapping-guides/migration-guides/05.2-kafka-streams-to-flink-migration.md) | Kafka Streams迁移到Flink: DSL转换、状态迁移 | Kafka Streams扩展、复杂处理需求 | -->
<!-- TRANSLATE: | [migration-guides/05.3-storm-to-flink-migration.md](05-mapping-guides/migration-guides/05.3-storm-to-flink-migration.md) | Storm迁移到Flink: 拓扑转换、语义升级 | Storm系统现代化、Exactly-Once需求 | -->
<!-- TRANSLATE: | [migration-guides/05.4-flink-1x-to-2x-migration.md](05-mapping-guides/migration-guides/05.4-flink-1x-to-2x-migration.md) | Flink 1.x到2.x迁移: API变更、配置调整、兼容性 | Flink版本升级、新特性采用 | -->
<!-- TRANSLATE: | [migration-guides/05.5-batch-to-streaming-migration.md](05-mapping-guides/migration-guides/05.5-batch-to-streaming-migration.md) | 批处理迁移到流处理: 架构转型、思维模式转变 | Lambda架构简化、实时化改造 | -->
<!-- TRANSLATE: | [streaming-etl-tools-landscape-2026.md](05-mapping-guides/streaming-etl-tools-landscape-2026.md) | 2026年流式ETL工具全景: 工具对比与选型 | ETL现代化、数据集成项目 | -->
<!-- TRANSLATE: | [streaming-sql-engines-2026-comparison.md](05-mapping-guides/streaming-sql-engines-2026-comparison.md) | 2026年流式SQL引擎对比: Flink SQL、RisingWave等 | SQL优先团队、降低开发门槛 | -->
<!-- TRANSLATE: | [multi-agent-frameworks-2026-comparison.md](05-mapping-guides/multi-agent-frameworks-2026-comparison.md) | 2026年多Agent框架对比: AutoGen、LangGraph等 | AI Agent架构、多智能体系统 | -->


<!-- TRANSLATE: ## 07. 最佳实践 (Best Practices) -->

<!-- TRANSLATE: 生产环境检查清单、调优指南与运维策略。 -->

<!-- TRANSLATE: | 文档 | 描述 | 适用场景 | -->
<!-- TRANSLATE: |------|------|----------| -->
<!-- TRANSLATE: | [07.01-flink-production-checklist.md](07-best-practices/07.01-flink-production-checklist.md) | Flink生产检查清单: 上线前的完整检查项 | 生产上线、运维审计、合规检查 | -->
<!-- TRANSLATE: | [07.02-performance-tuning-patterns.md](07-best-practices/07.02-performance-tuning-patterns.md) | 性能调优模式: 背压优化、序列化优化、并行度调优 | 性能优化、瓶颈排查 | -->
<!-- TRANSLATE: | [07.03-troubleshooting-guide.md](07-best-practices/07.03-troubleshooting-guide.md) | 故障排查指南: 常见问题诊断与解决 | 线上故障、紧急修复 | -->
<!-- TRANSLATE: | [07.04-cost-optimization-patterns.md](07-best-practices/07.04-cost-optimization-patterns.md) | 成本优化模式: 资源利用率、存储成本、计算优化 | FinOps、降本增效 | -->
<!-- TRANSLATE: | [07.05-security-hardening-guide.md](07-best-practices/07.05-security-hardening-guide.md) | 安全加固指南: 认证、授权、加密、审计 | 安全合规、生产加固 | -->
<!-- TRANSLATE: | [07.06-high-availability-patterns.md](07-best-practices/07.06-high-availability-patterns.md) | 高可用模式: 故障转移、多活架构、灾备 | 关键业务、SLA保障 | -->
<!-- TRANSLATE: | [07.07-testing-strategies-complete.md](07-best-practices/07.07-testing-strategies-complete.md) | 测试策略完整指南: 单元、集成、端到端测试 | 质量保障、CI/CD | -->


<!-- TRANSLATE: ## 09. 反模式 (Anti-Patterns) -->

<!-- TRANSLATE: 流处理常见陷阱、错误实践与规避策略。 -->

<!-- TRANSLATE: | 文档 | 描述 | 适用场景 | -->
<!-- TRANSLATE: |------|------|----------| -->
<!-- TRANSLATE: | [README.md](09-anti-patterns/README.md) | 反模式总览与索引 | 反模式入门、快速浏览 | -->
<!-- TRANSLATE: | [anti-pattern-checklist.md](09-anti-patterns/anti-pattern-checklist.md) | 反模式检查清单: 代码审查、设计评审 | 代码审查、设计评审 | -->
<!-- TRANSLATE: | [anti-pattern-01-global-state-abuse.md](09-anti-patterns/anti-pattern-01-global-state-abuse.md) | 反模式01: 全局状态滥用 | 状态设计、并发安全 | -->
<!-- TRANSLATE: | [anti-pattern-02-watermark-misconfiguration.md](09-anti-patterns/anti-pattern-02-watermark-misconfiguration.md) | 反模式02: Watermark配置错误 | 时间处理、延迟数据 | -->
<!-- TRANSLATE: | [anti-pattern-03-checkpoint-interval-misconfig.md](09-anti-patterns/anti-pattern-03-checkpoint-interval-misconfig.md) | 反模式03: Checkpoint间隔配置不当 | 容错设计、性能优化 | -->
<!-- TRANSLATE: | [anti-pattern-04-hot-key-skew.md](09-anti-patterns/anti-pattern-04-hot-key-skew.md) | 反模式04: 热点Key倾斜 | 数据分布、负载均衡 | -->
<!-- TRANSLATE: | [anti-pattern-05-blocking-io-processfunction.md](09-anti-patterns/anti-pattern-05-blocking-io-processfunction.md) | 反模式05: ProcessFunction中的阻塞IO | 异步设计、性能优化 | -->
<!-- TRANSLATE: | [anti-pattern-06-serialization-overhead.md](09-anti-patterns/anti-pattern-06-serialization-overhead.md) | 反模式06: 序列化开销过大 | 性能优化、序列化选择 | -->
<!-- TRANSLATE: | [anti-pattern-07-window-state-explosion.md](09-anti-patterns/anti-pattern-07-window-state-explosion.md) | 反模式07: 窗口状态爆炸 | 状态管理、内存优化 | -->
<!-- TRANSLATE: | [anti-pattern-08-ignoring-backpressure.md](09-anti-patterns/anti-pattern-08-ignoring-backpressure.md) | 反模式08: 忽视背压信号 | 流控设计、稳定性保障 | -->
<!-- TRANSLATE: | [anti-pattern-09-multi-stream-join-misalignment.md](09-anti-patterns/anti-pattern-09-multi-stream-join-misalignment.md) | 反模式09: 多流Join错位 | Join设计、时间对齐 | -->
<!-- TRANSLATE: | [anti-pattern-10-resource-estimation-oom.md](09-anti-patterns/anti-pattern-10-resource-estimation-oom.md) | 反模式10: 资源估算不足导致OOM | 容量规划、资源管理 | -->
<!-- TRANSLATE: | [streaming-anti-patterns.md](09-anti-patterns/streaming-anti-patterns.md) | 流处理反模式综合指南 | 反模式系统学习 | -->


<!-- TRANSLATE: ## 98. 练习与速查 (Exercises & Quick Ref) -->

<!-- TRANSLATE: 学习练习与快速参考手册。 -->

<!-- TRANSLATE: ### 练习文档 -->

<!-- TRANSLATE: | 文档 | 描述 | 适用场景 | -->
<!-- TRANSLATE: |------|------|----------| -->
<!-- TRANSLATE: | [README.md](98-exercises/README.md) | 练习目录说明与使用指南 | 学习计划、练习导航 | -->
<!-- TRANSLATE: | [exercise-01-process-calculus.md](98-exercises/exercise-01-process-calculus.md) | 练习01: 进程演算实践 | 理论基础巩固 | -->
<!-- TRANSLATE: | [exercise-02-flink-basics.md](98-exercises/exercise-02-flink-basics.md) | 练习02: Flink基础编程 | Flink入门实践 | -->
<!-- TRANSLATE: | [exercise-03-checkpoint-analysis.md](98-exercises/exercise-03-checkpoint-analysis.md) | 练习03: Checkpoint分析 | 容错机制理解 | -->
<!-- TRANSLATE: | [exercise-04-consistency-models.md](98-exercises/exercise-04-consistency-models.md) | 练习04: 一致性模型 | 分布式一致性 | -->
<!-- TRANSLATE: | [exercise-05-pattern-implementation.md](98-exercises/exercise-05-pattern-implementation.md) | 练习05: 设计模式实现 | 模式应用实践 | -->
<!-- TRANSLATE: | [exercise-06-tla-practice.md](98-exercises/exercise-06-tla-practice.md) | 练习06: TLA+形式化验证 | 形式化方法入门 | -->

<!-- TRANSLATE: ### 速查手册 -->

<!-- TRANSLATE: | 文档 | 描述 | 适用场景 | -->
<!-- TRANSLATE: |------|------|----------| -->
<!-- TRANSLATE: | [quick-ref-streaming-anti-patterns.md](98-exercises/quick-ref-streaming-anti-patterns.md) | 流处理反模式速查 | 快速参考、代码审查 | -->
<!-- TRANSLATE: | [quick-ref-flink-vs-risingwave.md](98-exercises/quick-ref-flink-vs-risingwave.md) | Flink vs RisingWave速查 | 技术选型快速对比 | -->
<!-- TRANSLATE: | [quick-ref-security-compliance.md](98-exercises/quick-ref-security-compliance.md) | 安全合规速查 | 安全检查、合规审计 | -->
<!-- TRANSLATE: | [quick-ref-a2a-protocol.md](98-exercises/quick-ref-a2a-protocol.md) | A2A协议速查 | Agent开发参考 | -->
<!-- TRANSLATE: | [quick-ref-temporal-flink.md](98-exercises/quick-ref-temporal-flink.md) | Temporal+Flink速查 | 工作流开发参考 | -->


<!-- TRANSLATE: ## 导航链接 -->

<!-- TRANSLATE: ### 项目索引 -->

<!-- TRANSLATE: | 目标 | 路径 | -->
<!-- TRANSLATE: |------|------| -->
<!-- TRANSLATE: | 🏠 项目根目录 | [../README.md](../README.md) | -->
<!-- TRANSLATE: | 🚀 快速开始 | [../QUICK-START.md](../QUICK-START.md) | -->
<!-- TRANSLATE: | 📊 项目跟踪 | [../PROJECT-TRACKING.md](../PROJECT-TRACKING.md) | -->
<!-- TRANSLATE: | 🔧 定理注册表 | [../THEOREM-REGISTRY.md](../THEOREM-REGISTRY.md) | -->
<!-- TRANSLATE: | 🗺️ 路线图 | [../ROADMAP.md](../ROADMAP.md) | -->
<!-- TRANSLATE: | 📖 英文README | [../README-EN.md](../README-EN.md) | -->
<!-- TRANSLATE: | 🚀 英文快速开始 | [../QUICK-START-EN.md](../QUICK-START-EN.md) | -->

<!-- TRANSLATE: ### 姐妹目录索引 -->

<!-- TRANSLATE: | 目录 | 索引 | 描述 | -->
<!-- TRANSLATE: |------|------|------| -->
<!-- TRANSLATE: | Struct/ | [../Struct/00-INDEX.md](../Struct/00-INDEX.md) | 形式理论与严格证明 | -->
<!-- TRANSLATE: | Flink/ | [../Flink/00-INDEX.md](../Struct/00-INDEX.md) | Flink专项技术与实现 | -->

<!-- TRANSLATE: ### 其他重要文档 -->

<!-- TRANSLATE: | 文档 | 描述 | -->
<!-- TRANSLATE: |------|------| -->
<!-- TRANSLATE: | [../ARCHITECTURE.md](../ARCHITECTURE.md) | 项目架构总览 | -->
<!-- TRANSLATE: | [../BEST-PRACTICES.md](../BEST-PRACTICES.md) | 项目级最佳实践 | -->
<!-- TRANSLATE: | [../TROUBLESHOOTING.md](../TROUBLESHOOTING.md) | 故障排查指南 | -->
<!-- TRANSLATE: | [../GLOSSARY.md](../GLOSSARY.md) | 术语表(中文) | -->
<!-- TRANSLATE: | [../GLOSSARY-EN.md](../GLOSSARY.md) | 术语表(英文) | -->
<!-- TRANSLATE: | [../REFERENCES.md](../REFERENCES.md) | 参考文献 | -->


<!-- TRANSLATE: ## 使用建议 -->

<!-- TRANSLATE: ### 🎯 按角色选择 -->

<!-- TRANSLATE: - **架构师**: 01-concept-atlas → 04-technology-selection → 06-frontier -->
<!-- TRANSLATE: - **开发工程师**: 02-design-patterns → 07-best-practices → 09-anti-patterns -->
<!-- TRANSLATE: - **数据工程师**: 03-business-patterns → 05-mapping-guides → 10-case-studies -->
<!-- TRANSLATE: - **运维工程师**: 07-best-practices → 09-anti-patterns → 08-standards -->
<!-- TRANSLATE: - **学习者**: 98-exercises → 01-concept-atlas → 02-design-patterns -->

<!-- TRANSLATE: ### 🔄 典型学习路径 -->

<!-- TRANSLATE: 1. **入门路径**: 概念图谱 → 设计模式 → 练习 → 案例研究 -->
<!-- TRANSLATE: 2. **进阶路径**: 业务场景 → 技术选型 → 最佳实践 → 前沿探索 -->
<!-- TRANSLATE: 3. **专家路径**: 前沿探索 → 映射指南 → 反模式 → 标准规范 -->
