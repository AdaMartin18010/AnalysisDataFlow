# 技术版本过时检查报告

> 生成时间: 2026-04-05 15:30:24

## 最新版本参考

| 技术 | 最新版本 | 状态 |
|------|----------|------|
| Docker | 27.0 | ⚠️ 默认值 |
| Flink | 1.20.0 | ⚠️ 默认值 |
| Gradle | 8.10 | ⚠️ 默认值 |
| Java | 21 | ⚠️ 默认值 |
| Kafka | 3.8.0 | ⚠️ 默认值 |
| Kubernetes | 1.31 | ⚠️ 默认值 |
| Maven | 3.9.9 | ⚠️ 默认值 |
| Python | 3.12 | ⚠️ 默认值 |
| Scala | 2.13 | ⚠️ 默认值 |


## 摘要

| 级别 | 数量 | 说明 |
|------|------|------|
| 🔴 严重过时 | 149 | 版本落后较多，建议立即更新 |
| 🟡 需要关注 | 96 | 版本略有落后，建议规划更新 |
| ✅ 当前版本 | 392 | 版本最新 |
| **总计** | **637** | - |

---

## 1. 严重过时的版本 🔴

以下文档中的技术版本**严重过时**，建议优先更新：

| 技术 | 文档版本 | 最新版本 | 文件路径 | 上下文 |
|------|----------|----------|----------|--------|
| Flink | 1.17 | 1.20.0 | `BEST-PRACTICES.md` | WatermarkInterval(200) }  // 步骤 6: Watermark 对齐配置（Flink 1.17... |
| Flink | 1.16 | 1.20.0 | `COMPATIBILITY-MATRIX.md` | 支持 \| 状态 \| 推荐场景 \| \|:---:\|:---:\|:---:\|:---:\|:---\| \| Flink 1.16... |
| Flink | 1.17 | 1.20.0 | `COMPATIBILITY-MATRIX.md` | nk 1.16 \| 2022-10 \| 2024-03 \| ⚠️ EOL \| 遗留系统维护 \| \| Flink 1.17... |
| Python | 3.7 | 3.12 | `COMPATIBILITY-MATRIX.md` | ```  ### 3.3 Python 版本要求 (PyFlink)  \| Flink 版本 \| Python 3.7 ... |
| Python | 3.8 | 3.12 | `COMPATIBILITY-MATRIX.md` | Python 版本要求 (PyFlink)  \| Flink 版本 \| Python 3.7 \| Python 3.8 ... |
| Python | 3.9 | 3.12 | `COMPATIBILITY-MATRIX.md` | (PyFlink)  \| Flink 版本 \| Python 3.7 \| Python 3.8 \| Python 3.9... |
| Kafka | 0.11 | 3.8.0 | `COMPATIBILITY-MATRIX.md` | \|  **说明:**  - `kafka-client` 版本需与 Flink 连接器版本匹配 - Kafka 0.11... |
| Kafka | 2.4 | 3.8.0 | `COMPATIBILITY-MATRIX.md` | 版本需与 Flink 连接器版本匹配 - Kafka 0.11+ 支持事务消息（精确一次语义） - Kafka 2.4+... |
| Kubernetes | 1.22 | 1.31 | `COMPATIBILITY-MATRIX.md` | . 生态组件兼容性  ### 5.1 Kubernetes 版本兼容性  \| Flink 版本 \| K8s 1.22 \|... |
| Kubernetes | 1.23 | 1.31 | `COMPATIBILITY-MATRIX.md` | ### 5.1 Kubernetes 版本兼容性  \| Flink 版本 \| K8s 1.22 \| K8s 1.23 \|... |
| Kubernetes | 1.24 | 1.31 | `COMPATIBILITY-MATRIX.md` | ernetes 版本兼容性  \| Flink 版本 \| K8s 1.22 \| K8s 1.23 \| K8s 1.24 \|... |
| Kubernetes | 1.25 | 1.31 | `COMPATIBILITY-MATRIX.md` | 容性  \| Flink 版本 \| K8s 1.22 \| K8s 1.23 \| K8s 1.24 \| K8s 1.25 \|... |
| Kubernetes | 1.26 | 1.31 | `COMPATIBILITY-MATRIX.md` | 版本 \| K8s 1.22 \| K8s 1.23 \| K8s 1.24 \| K8s 1.25 \| K8s 1.26 \| ... |
| Kubernetes | 1.27 | 1.31 | `COMPATIBILITY-MATRIX.md` | .22 \| K8s 1.23 \| K8s 1.24 \| K8s 1.25 \| K8s 1.26 \| K8s 1.27 \|... |
| Kubernetes | 1.28 | 1.31 | `COMPATIBILITY-MATRIX.md` | .23 \| K8s 1.24 \| K8s 1.25 \| K8s 1.26 \| K8s 1.27 \| K8s 1.28 \|... |
| Flink | 1.17 | 1.20.0 | `FAQ.md` | ## 5. 关于技术  ### Q17: Flink版本覆盖？  **A:**  当前文档覆盖 **Flink 1.17... |
| Flink | 1.17 | 1.20.0 | `GLOSSARY.md` | -  ## A  ### Adaptive Execution Engine (自适应执行引擎) [Flink 1.17... |
| Python | 3.8 | 3.12 | `PDF-EXPORT-GUIDE.md` | \| 工具 \| 用途 \| 安装命令 \| \|------\|------\|----------\| \| **Python 3.8... |
| Flink | 1.17 | 1.20.0 | `THEOREM-REGISTRY.md` | ture/Code/Release/Maintenance窗口 \| \| Def-F-08-52 \| Flink 1.17... |
| Flink | 1.17 | 1.20.0 | `TROUBLESHOOTING.md` | 初始版本，包含完整故障排查体系 \| Kimi Code \|  ---  *本手册基于Apache Flink 1.17+... |
| Flink | 1.16 | 1.20.0 | `Flink\3.9-state-backends-deep-comparison.md` | \| **形式化等级**: L4-L5 > **版本**: 2026.04 \| **适用版本**: Flink 1.16+... |
| Flink | 1.13 | 1.20.0 | `Flink\flink-cep-complete-tutorial.md` | cs-and-watermark.md) \| **形式化等级**: L3-L4 > **版本**: Flink 1.13... |
| Flink | 1.16 | 1.20.0 | `Flink\flink-state-backends-comparison.md` | \| **形式化等级**: L3-L4 > **版本**: 2026.04 \| **适用版本**: Flink 1.16+... |
| Flink | 1.17 | 1.20.0 | `Flink\00-meta\00-INDEX.md` | 最后更新**: 2026-04-05 - **文档总数**: 350+ 篇 - **覆盖版本**: Flink 1.17... |
| Docker | 20.10 | 27.0 | `Flink\00-meta\00-QUICK-START.md` | 分钟快速开始  ### 1.1 Docker Compose 一键启动  **系统要求：**  - Docker 20.... |
| Flink | 1.0 | 1.20.0 | `Flink\01-concepts\disaggregated-state-analysis.md` | gregatedStateBackend ```  **MemoryStateBackend** (Flink 1.0+... |
| Flink | 1.1 | 1.20.0 | `Flink\01-concepts\disaggregated-state-analysis.md` | 写入远程。适用于小状态(<100MB)、低延迟测试场景。  **FsStateBackend** (Flink 1.1+... |
| Flink | 1.2 | 1.20.0 | `Flink\01-concepts\disaggregated-state-analysis.md` | 系统。依赖 TaskManager 内存大小。  **RocksDBStateBackend** (Flink 1.2+... |
| Flink | 1.17 | 1.20.0 | `Flink\02-core\adaptive-execution-engine-v2.md` | 适应执行引擎 (Adaptive Execution Engine V2, AEE-V2)** 是 Flink 1.17... |
| Flink | 1.15 | 1.20.0 | `Flink\02-core\adaptive-execution-engine-v2.md` | 响应时间 \| \|------\|-----------\|---------\|---------\| \| Flink 1.15... |
| Flink | 1.16 | 1.20.0 | `Flink\02-core\adaptive-execution-engine-v2.md` | ---------\| \| Flink 1.15 \| 仅支持并行度调整 \| 手动 \| 分钟级 \| \| Flink 1.16... |
| Flink | 1.5 | 1.20.0 | `Flink\02-core\backpressure-and-flow-control.md` | mentation)](#4-论证过程-argumentation)     - [4.1 为什么 Flink 1.5 ... |
| Flink | 1.11 | 1.20.0 | `Flink\02-core\exactly-once-semantics-deep-dive.md` | } } ```### 6.3 非对齐Checkpoint配置```java // Flink 1.11+ 支持非... |
| Flink | 1.13 | 1.20.0 | `Flink\02-core\exactly-once-semantics-deep-dive.md` | nmentTimeout(Duration.ofSeconds(30));  // 或完全禁用对齐（Flink 1.13... |
| Flink | 1.17 | 1.20.0 | `Flink\02-core\flink-2.0-async-execution-model.md` | 同步执行<br/>Synchronous"]         ASYNC_V1["🟡 异步V1 (Flink 1.17+... |
| Flink | 1.17 | 1.20.0 | `Flink\02-core\multi-way-join-optimization.md` | │ │  Flink 1.17- |
| Flink | 1.13 | 1.20.0 | `Flink\02-core\state-backends-deep-comparison.md` | .size}, \quad \alpha \approx 0.3 $$  > ⚠️ **注意**: Flink 1.13... |
| Flink | 1.0 | 1.20.0 | `Flink\02-core\state-backends-deep-comparison.md` | --  ## 3. 关系建立 (Relations)  ### 3.1 状态后端演进关系  ``` Flink 1.0-... |
| Flink | 1.17 | 1.20.0 | `Flink\02-core\streaming-etl-best-practices.md` | nfig().setAutoWatermarkInterval(200L);  // 自适应调度器（Flink 1.17... |
| Flink | 1.17 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\built-in-functions-complete-list.md` | vs-2.0-comparison.md) \| **形式化等级**: L3 \| **版本兼容**: Flink 1.17... |
| Flink | 1.12 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\built-in-functions-complete-list.md` | 学函数 (Mathematical Functions) — 35个  > 🔢 **适用版本**: Flink 1.12... |
| Flink | 1.13 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\built-in-functions-complete-list.md` | 7.7 窗口函数 (Window Functions) — 18个  > 🪟 **适用版本**: Flink 1.13+... |
| Flink | 1.14 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\built-in-functions-complete-list.md` | 7.8 JSON函数 (JSON Functions) — 15个  > 🗂️ **适用版本**: Flink 1.14... |
| Flink | 1.13 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\flink-cep-complete-guide.md` | ions-deep-dive.md) \| **形式化等级**: L3-L5 > > **版本**: Flink 1.13... |
| Flink | 1.9 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\flink-sql-calcite-optimizer-deep-dive.md` | **Def-F-03-38 (Blink Planner架构)**: Blink Planner是Flink 1.9+引... |
| Flink | 1.8 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\flink-sql-calcite-optimizer-deep-dive.md` | nk Planner是Flink 1.9+引入的现代化优化器：  \| 组件 \| 旧Planner (Flink 1.8-... |
| Flink | 1.17 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\flink-sql-calcite-optimizer-deep-dive.md` | \| 标准符合度 \| SQL-92 \| SQL:2011 \| 现代SQL特性 \|  **迁移论证**：Flink 1.17... |
| Flink | 1.1 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\flink-sql-calcite-optimizer-deep-dive.md` | e Flink. "Table API & SQL - Calcite Integration." Flink 1.1 ... |
| Flink | 1.17 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\flink-sql-window-functions-deep-dive.md` | INTERVAL '1' HOUR,         -- 可选: 使用窗口TVF的延迟参数（Flink 1.17+） ... |
| Flink | 1.17 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\flink-table-sql-complete-guide.md` | ions-deep-dive.md) \| **形式化等级**: L3-L5 > > **版本**: Flink 1.17... |
| Flink | 1.13 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\flink-table-sql-complete-guide.md` | STRING,     event_time TIMESTAMP(3),      -- 计算列 (Flink 1.13... |
| Flink | 1.14 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\flink-table-sql-complete-guide.md` | M products GROUP BY category; ```  **Python UDAF (Flink 1.14... |
| Flink | 1.15 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\flink-table-sql-complete-guide.md` | TCH_RECOGNIZE: Flink 1.13+ - AFTER MATCH SKIP 子句: Flink 1.15... |
| Flink | 1.16 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\flink-table-sql-complete-guide.md` | - AFTER MATCH SKIP 子句: Flink 1.15+ - WITHIN 时间约束: Flink 1.16... |
| Flink | 1.9 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\query-optimization-analysis.md` | \| Transformation 链 \|  **Planner 类型演进**[^2]：  - **Flink 1.9 之... |
| Flink | 1.17 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\query-optimization-analysis.md` | ink 1.9-1.16**: 引入 Blink Planner，成为默认 Planner -**Flink 1.17... |
| Flink | 1.12 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\sql-functions-cheatsheet.md` | 记 \| 含义 \| 说明 \| \|------\|------\|------\| \| 🟢 \| 稳定版本 \| Flink 1.12... |
| Flink | 1.15 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\sql-functions-cheatsheet.md` | ----\| \| 🟢 \| 稳定版本 \| Flink 1.12+ 全支持 \| \| 🟡 \| 较新版本 \| Flink 1.15... |
| Flink | 1.17 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\sql-functions-cheatsheet.md` | 全支持 \| \| 🟡 \| 较新版本 \| Flink 1.15+ 引入 \| \| 🔵 \| 实验特性 \| Flink 1.17+... |
| Flink | 1.14 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\sql-functions-cheatsheet.md` | ) ```  ---  ## 10. 版本兼容性矩阵  \| 函数类别 \| Flink 1.12 \| Flink 1.14... |
| Flink | 1.16 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\sql-functions-cheatsheet.md` | # 10. 版本兼容性矩阵  \| 函数类别 \| Flink 1.12 \| Flink 1.14 \| Flink 1.16... |
| Python | 3.9 | 3.12 | `Flink\03-api\09-language-foundations\00-INDEX.md` | 2**适用版本: Flink 1.18+ / 2.0+ / 2.2+ \| Scala 3.x \| Python 3.9... |
| Flink | 1.14 | 1.20.0 | `Flink\03-api\09-language-foundations\01.02-typeinformation-derivation.md` | 型描述符)     - [Def-F-09-05: 宏派生 (Macro Derivation - Flink 1.14... |
| Flink | 1.9 | 1.20.0 | `Flink\03-api\09-language-foundations\01.02-typeinformation-derivation.md` | ph TB     subgraph "Flink Scala API 演进"         A[Flink 1.9-... |
| Flink | 1.15 | 1.20.0 | `Flink\03-api\09-language-foundations\01.02-typeinformation-derivation.md` | \|宏派生<br/>Scala 2.12\| B[TypeInformation]         C[Flink 1.15... |
| Python | 3.9 | 3.12 | `Flink\03-api\09-language-foundations\02.03-python-async-api.md` | \| **形式化等级**: L4-L5 > **版本**: Flink 2.2+ \| **语言**: Python 3.9... |
| Flink | 1.15 | 1.20.0 | `Flink\03-api\09-language-foundations\03.01-migration-guide.md` | link-scala-api-community.md) \| 形式化等级: L3-L4 \| 版本: Flink 1.15... |
| Flink | 1.16 | 1.20.0 | `Flink\03-api\09-language-foundations\03.01-migration-guide.md` | \| Flink 1.15 \| Flink 2.0 \| ⚠️ 需修改 \| ✅ 兼容 \| 中等 \| \| Flink 1.16... |
| Flink | 1.17 | 1.20.0 | `Flink\03-api\09-language-foundations\03.01-migration-guide.md` | \| Flink 1.16 \| Flink 2.0 \| ⚠️ 需修改 \| ✅ 兼容 \| 中等 \| \| Flink 1.17... |
| Flink | 1.14 | 1.20.0 | `Flink\03-api\09-language-foundations\03.01-migration-guide.md` | -------\|----------\|----------------\|----------\| \| Flink 1.14... |
| Flink | 1.14 | 1.20.0 | `Flink\03-api\09-language-foundations\06-risingwave-deep-dive.md` | + RocksDB      :2015, 2020     section 云原生转型     Flink 1.14 ... |
| Flink | 1.17 | 1.20.0 | `Flink\03-api\09-language-foundations\datastream-api-cheatsheet.md` | pi-complete-guide.md) > 形式化等级: L4 (API参考) > 适用版本: Flink 1.17... |
| Flink | 1.12 | 1.20.0 | `Flink\03-api\09-language-foundations\datastream-api-cheatsheet.md` | \| 无需Watermark \| 1.0+ \|  ```java // Java: 时间语义配置 (Flink 1.12+... |
| Flink | 1.13 | 1.20.0 | `Flink\03-api\09-language-foundations\datastream-api-cheatsheet.md` | 0.1                       // 抖动因子 ));  // 状态后端配置 (Flink 1.13... |
| Flink | 1.14 | 1.20.0 | `Flink\03-api\09-language-foundations\datastream-api-cheatsheet.md` | ///checkpoint/dir"); ```  ### 6.4 版本兼容性矩阵  \| 特性 \| Flink 1.14... |
| Flink | 1.15 | 1.20.0 | `Flink\03-api\09-language-foundations\datastream-api-cheatsheet.md` | \| 重要变更 \| 发布日期 \| \|------\|----------\|----------\| \| Flink 1.15 ... |
| Flink | 1.16 | 1.20.0 | `Flink\03-api\09-language-foundations\datastream-api-cheatsheet.md` | nk 1.15 \| 新Kafka Source/Sink API GA \| 2022-05 \| \| Flink 1.16... |
| Flink | 1.17 | 1.20.0 | `Flink\03-api\09-language-foundations\flink-datastream-api-complete-guide.md` | cs-formalization.md) \| **形式化等级**: L3-L4 > **版本**: Flink 1.17... |
| Flink | 1.12 | 1.20.0 | `Flink\03-api\09-language-foundations\flink-datastream-api-complete-guide.md` | ntTime()); ```**时间语义设置**:```java // 全局时间语义设置 (Flink 1.12... |
| Python | 3.9 | 3.12 | `Flink\03-api\09-language-foundations\flink-language-support-complete-guide.md` | dencies FROM flink:1.19.0-scala_2.12-java11  # 安装 Python 3.9... |
| Python | 3.9 | 3.12 | `Flink\03-api\09-language-foundations\pyflink-complete-guide.md` | \| **形式化等级**: L2-L3 \| **版本**: Flink 1.18+ / 2.0+ / Python 3.9... |
| Python | 1.20 | 3.12 | `Flink\03-api\09-language-foundations\pyflink-complete-guide.md` | .txt apache-flink ```  ``` # constraints.txt 示例 # PyFlink 1.... |
| Flink | 1.16 | 1.20.0 | `Flink\04-runtime\04.01-deployment\flink-deployment-ops-complete-guide.md` | -dive.md) \| **形式化等级**: L3-L4 > > **适用版本**: Apache Flink 1.16... |
| Flink | 1.17 | 1.20.0 | `Flink\04-runtime\04.01-deployment\multi-cloud-deployment-templates.md` | Description: Flink Version     Default: vvr-8.0.6-flink-1.17... |
| Flink | 1.16 | 1.20.0 | `Flink\04-runtime\04.01-deployment\serverless-flink-ga-guide.md` | al{B}$ \| GB-秒精确计费 \|  **核心特性矩阵**：  \| 特性 \| Preview (Flink 1.16... |
| Flink | 1.17 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\elasticsearch-connector-complete-guide.md` | 实例验证 (Examples)  ### 6.1 Maven 依赖配置  ```xml <!-- Flink 1.17+... |
| Flink | 1.17 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-24-connectors-guide.md` | ## 3.3 连接器版本兼容性矩阵  **Flink 版本与连接器版本对应**:  \| 连接器 \| Flink 1.17... |
| Flink | 1.12 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-24-connectors-guide.md` | # 4.4 CDC 连接器演进路径  **CDC 技术演进时间线**:  ``` CDC 1.x (Flink 1.12... |
| Flink | 1.15 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-24-connectors-guide.md` | bezium 嵌入模式 ├── 单表同步为主 └── Schema 变更需重启  CDC 2.x (Flink 1.15... |
| Kafka | 3.3 | 3.8.0 | `Flink\05-ecosystem\05.01-connectors\flink-24-connectors-guide.md` | │ │   • flink-connector-kafka 3.3.x (Kafka 3.x 原生)          ... |
| Kafka | 3.5 | 3.8.0 | `Flink\05-ecosystem\05.01-connectors\flink-24-connectors-guide.md` | **论证数据**:  **Kafka 3.x 连接器性能提升**:  ``` 测试环境: 10节点 Kafka 3.5 ... |
| Flink | 1.14 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-connectors-ecosystem-complete-guide.md` | ## 3.3 连接器版本兼容性矩阵  **Flink 版本与连接器版本对应**:  \| 连接器 \| Flink 1.14... |
| Flink | 1.15 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-connectors-ecosystem-complete-guide.md` | 容性矩阵  **Flink 版本与连接器版本对应**:  \| 连接器 \| Flink 1.14 \| Flink 1.15... |
| Flink | 1.16 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-connectors-ecosystem-complete-guide.md` | 版本与连接器版本对应**:  \| 连接器 \| Flink 1.14 \| Flink 1.15 \| Flink 1.16 ... |
| Flink | 1.17 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-connectors-ecosystem-complete-guide.md` | :  \| 连接器 \| Flink 1.14 \| Flink 1.15 \| Flink 1.16 \| Flink 1.17... |
| Flink | 1.17 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-delta-lake-integration.md` | use-architecture.md) \| **形式化等级**: L4-L5 \| **版本**: Flink 1.17... |
| Flink | 1.14 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-elasticsearch-connector-guide.md` | heckpoints();  // 4. 背压处理 // 启用 Buffer Debloating（Flink 1.14... |
| Flink | 1.17 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-iceberg-integration.md` | lake-integration.md) \| **形式化等级**: L4-L5 \| **版本**: Flink 1.17... |
| Flink | 1.16 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\jdbc-connector-complete-guide.md` | onOptions,     connectionOptions,     // 自定义异常处理 (Flink 1.16... |
| Flink | 1.14 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\kafka-integration-patterns.md` | itializer.OffsetsInitializer;  // 构建 Kafka Source（Flink 1.14... |
| Kafka | 2.4 | 3.8.0 | `Flink\05-ecosystem\05.01-connectors\kafka-integration-patterns.md` | Flink 的应对策略**：静态成员资格 (`group.instance.id`)、协作重平衡 (Kafka 2.4+... |
| Kafka | 0.11 | 3.8.0 | `Flink\05-ecosystem\05.01-connectors\kafka-integration-patterns.md` | 协调开销） \| 中等（事务协调开销） \| \| **外部依赖** \| 无需特殊支持 \| 需要事务支持（Kafka 0.11... |
| Kafka | 0.10 | 3.8.0 | `Flink\05-ecosystem\05.01-connectors\kafka-integration-patterns.md` | 版本支持的 Exactly-Once 策略有所差异。下表总结了各版本的能力矩阵：  \| 特性 \| Kafka 0.10 ... |
| Kafka | 1.0 | 3.8.0 | `Flink\05-ecosystem\05.01-connectors\kafka-integration-patterns.md` | 。下表总结了各版本的能力矩阵：  \| 特性 \| Kafka 0.10 \| Kafka 0.11 \| Kafka 1.0 ... |
| Kafka | 2.0 | 3.8.0 | `Flink\05-ecosystem\05.01-connectors\kafka-integration-patterns.md` | 矩阵：  \| 特性 \| Kafka 0.10 \| Kafka 0.11 \| Kafka 1.0 \| Kafka 2.0 ... |
| Kafka | 3.0 | 3.8.0 | `Flink\05-ecosystem\05.01-connectors\kafka-integration-patterns.md` | Kafka 0.11 \| Kafka 1.0 \| Kafka 2.0 \| Kafka 2.4+ \| Kafka 3.0+... |
| Kafka | 2.5 | 3.8.0 | `Flink\05-ecosystem\05.01-connectors\kafka-integration-patterns.md` | lients.consumer.CooperativeStickyAssignor" );  // Kafka 2.5+... |
| Flink | 1.17 | 1.20.0 | `Flink\05-ecosystem\05.02-lakehouse\flink-iceberg-integration.md` | eaming-lakehouse.md) \| **形式化等级**: L4-L5 \| **版本**: Flink 1.17... |
| Flink | 1.17 | 1.20.0 | `Flink\05-ecosystem\ecosystem\kafka-streams-migration.md` | > **Source**: Kafka Streams \| **Target**: Apache Flink 1.17+... |
| Flink | 1.2 | 1.20.0 | `Flink\07-rust-native\arroyo-update\01-arroyo-cloudflare-acquisition.md` | vs Flink 9.8k events/s    - 内存占用: Arroyo 180MB vs Flink 1.2G... |
| Flink | 0.5 | 1.20.0 | `Flink\07-rust-native\risingwave-comparison\02-nexmark-head-to-head.md` | ea RisingWave 0.9, 0.85, 0.95, 0.9, 0.95     area Flink 0.5,... |
| Kafka | 3.5 | 3.8.0 | `Flink\08-roadmap\08.01-flink-24\flink-2.4-tracking.md` | Paimon Preview \| Paimon GA + Delta 3.0 \| \| 消息队列 \| Kafka 3.5 ... |
| Flink | 1.17 | 1.20.0 | `Flink\08-roadmap\08.01-flink-24\flink-version-evolution-complete-guide.md` | .x 系列定义](#12-flink-1x-系列定义)       - [Def-F-08-52: Flink 1.17... |
| Flink | 1.17.0 | 1.20.0 | `Flink\08-roadmap\08.01-flink-24\flink-version-evolution-complete-guide.md` | 17 Release  **发布时间**: 2023年3月  **核心特性**:  ```yaml Flink 1.17... |
| Flink | 1.11 | 1.20.0 | `Flink\08-roadmap\08.01-flink-24\release-checklist-template.md` | 节奏合理性论证  基于Flink社区历史发布数据分析：  ``` 统计周期: 2020-2025 (Flink 1.11... |
| Flink | 1.16 | 1.20.0 | `Flink\09-practices\09.01-case-studies\case-iot-stream-processing.md` | 差 - **2022**: 引入边缘计算网关，本地预处理降低带宽压力 - **2023**: 引入 Flink 1.16... |
| Flink | 1.13 | 1.20.0 | `Flink\09-practices\09.01-case-studies\case-realtime-analytics.md` | park）+ 流处理（Storm）双轨运行，维护成本高，一致性难保证 - **2022**: 引入 Flink 1.13... |
| Flink | 1.17 | 1.20.0 | `Flink\09-practices\09.01-case-studies\case-realtime-analytics.md` | 1.13，构建第一代实时分析平台，解决了一致性问题，但吞吐瓶颈明显 - **2023**: 升级到 Flink 1.17... |
| Flink | 1.14 | 1.20.0 | `Flink\09-practices\09.03-performance-tuning\06.02-performance-optimization-complete.md` | y.floating-buffers-per-gate: 8  # 启用缓冲区Debloating（Flink 1.14... |
| Flink | 1.13 | 1.20.0 | `Flink\09-practices\09.03-performance-tuning\state-backend-selection.md` | *：受限于 `-Xmx`，建议单 TM 状态上限几十 MB。  **状态**：⚠️ **已弃用**。Flink 1.13... |
| Flink | 1.17 | 1.20.0 | `Flink\09-practices\09.03-performance-tuning\05-vs-competitors\flink-vs-spark-streaming.md` | uous Processing 成熟化 \| \| **批流统一** \| 强化 Batch 模式性能 (Flink 1.17... |
| Flink | 1.17 | 1.20.0 | `Flink\09-practices\09.04-security\security-hardening-guide.md` | Users,OU=Groups,DC=example,DC=com"; } ```  **方案B: Flink 1.17... |
| Flink | 1.16 | 1.20.0 | `Knowledge\3.10-flink-production-checklist.md` | \| **形式化等级**: L3-L4 > **版本**: 2026.04 \| **适用版本**: Flink 1.16+... |
| Flink | 1.16 | 1.20.0 | `Knowledge\production-deployment-checklist.md` | \| **形式化等级**: L3-L4 > **版本**: 2026.04 \| **适用版本**: Flink 1.16+... |
| Flink | 1.13 | 1.20.0 | `Knowledge\06-frontier\realtime-ai-streaming-2026.md` | ka 2.x \| 2011 \| 旧版协议、ZooKeeper依赖 \| 升级至KRaft模式 \| \| Flink 1.13... |
| Flink | 1.17 | 1.20.0 | `Knowledge\07-best-practices\07.02-performance-tuning-patterns.md` | e]] ) descriptor.enableStateCompression(true)  // Flink 1.17... |
| Flink | 1.12 | 1.20.0 | `Knowledge\09-anti-patterns\streaming-anti-patterns.md` | .getExecutionEnvironment  // 默认使用 Processing Time（Flink 1.12... |
| Flink | 1.11 | 1.20.0 | `Knowledge\98-exercises\exercise-03-checkpoint-analysis.md` | 3.8: 非对齐 Checkpoint 分析 (10分)  **难度**: L5  **背景**：Flink 1.11+... |
| Flink | 1.5 | 1.20.0 | `Knowledge\98-exercises\exercise-05-pattern-implementation.md` | 解释 Flink 反压 (Backpressure) 的产生原因和传播机制 (4分) 2. 对比 Flink 1.5 前... |
| Python | 3.9 | 3.12 | `Knowledge\98-exercises\README.md` | ) - Maven 3.8+ 或 Gradle 7+ - Docker (本地Flink集群) - Python 3.9... |
| Flink | 1.17 | 1.20.0 | `LEARNING-PATHS\certifications\custom-assessment.md` | ernel 2. 在线 IDE（如 CodeSandbox） 3. 自建评测系统  环境要求： - Flink 1.17... |
| Maven | 3.6 | 3.9.9 | `LEARNING-PATHS\certifications\custom-assessment.md` | ndbox） 3. 自建评测系统  环境要求： - Flink 1.17+ - JDK 11+ - Maven 3.6+... |
| Flink | 1.11 | 1.20.0 | `LEARNING-PATHS\certifications\ververica-certification.md` | TAIN_ON_CANCELLATION );  // Unaligned Checkpoint (Flink 1.11... |
| Flink | 1.12 | 1.20.0 | `reports\fictional-content-audit-20260405_143730.md` | Akka Classic \| 2025 Q2 \| Hold \| Pekko迁移 \| 200: \| Flink 1.12 ... |
| Flink | 1.14 | 1.20.0 | `Struct\07-tools\tla-for-flink.md` | 期checkpoint  ### 8.2 案例二：在恢复逻辑中发现Bug  **问题描述**：在分析Flink 1.14... |
| Python | 2.0 | 3.12 | `TECH-RADAR\00-INDEX.md` | TRIAL (试用) - 20项  有前景的技术，建议非核心场景试点  **语言与框架:**  - PyFlink 2.... |
| Flink | 1.0 | 1.20.0 | `TECH-RADAR\evolution-timeline.md` | : 基于Kafka的流处理         2014 : Apache Flink 1.0              :... |
| Flink | 1.3 | 1.20.0 | `TECH-RADAR\evolution-timeline.md` | ache Beam 孵化              : 统一编程模型         2017 : Flink 1.3 ... |
| Flink | 1.9 | 1.20.0 | `TECH-RADAR\evolution-timeline.md` | : 轻量级流处理      section 2019-2022         2019 : Flink 1.9 发布 ... |
| Flink | 1.14 | 1.20.0 | `TECH-RADAR\evolution-timeline.md` | 处理兴起              : K8s Operator出现         2021 : Flink 1.14... |
| Flink | 1.16 | 1.20.0 | `TECH-RADAR\evolution-timeline.md` | : 声明式资源管理         2022 : 流批一体成熟              : Flink 1.16发布 ... |
| Flink | 1.12 | 1.20.0 | `TECH-RADAR\evolution-timeline.md` | 用 \| \| Akka Classic \| 2025 Q2 \| Hold \| Pekko迁移 \| \| Flink 1.12... |
| Kafka | 2.6 | 3.8.0 | `TECH-RADAR\evolution-timeline.md` | fka诞生         2017 : Kafka Streams         2020 : Kafka 2.6 ... |
| Flink | 1.13 | 1.20.0 | `TECH-RADAR\risk-assessment.md` | # 9. 风险案例研究  ### 9.1 案例: 某金融公司Flink升级风险  **背景:** 从Flink 1.13... |
| Flink | 1.15 | 1.20.0 | `tutorials\01-environment-setup.md` | "my-flink-cluster" \   --EngineVersion "vvr-6.0.2-flink-1.15... |
| Flink | 1.10 | 1.20.0 | `tutorials\06-advanced-topics-script.md` | 械硬盘优化 - FLASH_SSD_OPTIMIZED：SSD优化  Managed Memory是Flink 1.10... |
| Flink | 1.11 | 1.20.0 | `tutorials\06-advanced-topics-script.md` | ：增加超时、检查网络/存储  【10:30-12:00】 Unaligned Checkpoint是Flink 1.11... |
| Flink | 1.14 | 1.20.0 | `tutorials\06-advanced-topics-script.md` | 6. 使用Broadcast State减少shuffle  Buffer Debloating是Flink 1.14引... |
| Flink | 1.11 | 1.20.0 | `tutorials\interactive\hands-on-labs\lab-05-checkpoint.md` | } } ```### 步骤 3: 增量 Checkpoint```java // Flink 1.11+ 增量 ... |


### 1.1 按技术统计

| 技术 | 过时次数 | 涉及的旧版本 |
|------|----------|--------------|
| Docker | 1 | 20.10 |
| Flink | 116 | 0.5, 1.0, 1.1, 1.10, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17, 1.17.0, 1.2, 1.3, 1.5, 1.8, 1.9 |
| Kafka | 13 | 0.10, 0.11, 1.0, 2.0, 2.4, 2.5, 2.6, 3.0, 3.3, 3.5 |
| Kubernetes | 7 | 1.22, 1.23, 1.24, 1.25, 1.26, 1.27, 1.28 |
| Maven | 1 | 3.6 |
| Python | 11 | 1.20, 2.0, 3.7, 3.8, 3.9 |


---

## 2. 需要关注的版本 🟡

以下文档中的技术版本**略有落后**，建议规划更新：

| 技术 | 文档版本 | 最新版本 | 文件路径 |
|------|----------|----------|----------|
| Flink | 1.18 | 1.20.0 | `BENCHMARK-REPORT.md` |
| Flink | 1.18 | 1.20.0 | `COMPATIBILITY-MATRIX.md` |
| Flink | 1.19 | 1.20.0 | `COMPATIBILITY-MATRIX.md` |
| Scala | 2.11 | 2.13 | `COMPATIBILITY-MATRIX.md` |
| Scala | 2.12 | 2.13 | `COMPATIBILITY-MATRIX.md` |
| Python | 3.10 | 3.12 | `COMPATIBILITY-MATRIX.md` |
| Python | 3.11 | 3.12 | `COMPATIBILITY-MATRIX.md` |
| Kubernetes | 1.29 | 1.31 | `COMPATIBILITY-MATRIX.md` |
| Kubernetes | 1.30 | 1.31 | `COMPATIBILITY-MATRIX.md` |
| Flink | 1.18 | 1.20.0 | `HISTORY.md` |
| Flink | 1.18 | 1.20.0 | `OBSERVABILITY-GUIDE.md` |
| Flink | 1.18 | 1.20.0 | `THEOREM-REGISTRY.md` |
| Flink | 1.19 | 1.20.0 | `THEOREM-REGISTRY.md` |
| Flink | 1.18 | 1.20.0 | `Flink\flink-pyflink-deep-dive.md` |
| Flink | 1.19 | 1.20.0 | `Flink\02-core\backpressure-and-flow-control.md` |
| Flink | 1.18 | 1.20.0 | `Flink\02-core\multi-way-join-optimization.md` |
| Flink | 1.18 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\ansi-sql-2023-compliance-guide.md` |
| Flink | 1.19 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\flink-process-table-functions.md` |
| Flink | 1.18 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\flink-table-sql-complete-guide.md` |
| Flink | 1.18 | 1.20.0 | `Flink\03-api\03.02-table-sql-api\sql-functions-cheatsheet.md` |
| Flink | 1.18 | 1.20.0 | `Flink\03-api\09-language-foundations\00-INDEX.md` |
| Scala | 2.12 | 2.13 | `Flink\03-api\09-language-foundations\01.02-typeinformation-derivation.md` |
| Scala | 2.12 | 2.13 | `Flink\03-api\09-language-foundations\02.01-java-api-from-scala.md` |
| Scala | 2.11 | 2.13 | `Flink\03-api\09-language-foundations\02.02-flink-scala-api-community.md` |
| Flink | 1.18 | 1.20.0 | `Flink\03-api\09-language-foundations\03-rust-native.md` |
| Flink | 1.18 | 1.20.0 | `Flink\03-api\09-language-foundations\03.01-migration-guide.md` |
| Flink | 1.19 | 1.20.0 | `Flink\03-api\09-language-foundations\03.01-migration-guide.md` |
| Flink | 1.18 | 1.20.0 | `Flink\03-api\09-language-foundations\04-streaming-lakehouse.md` |
| Flink | 1.18 | 1.20.0 | `Flink\03-api\09-language-foundations\06-risingwave-deep-dive.md` |
| Scala | 2.12 | 2.13 | `Flink\03-api\09-language-foundations\08-flink-rust-connector-dev.md` |
| Flink | 1.18 | 1.20.0 | `Flink\03-api\09-language-foundations\datastream-api-cheatsheet.md` |
| Scala | 2.12 | 2.13 | `Flink\03-api\09-language-foundations\flink-datastream-api-complete-guide.md` |
| Flink | 1.19 | 1.20.0 | `Flink\03-api\09-language-foundations\flink-language-support-complete-guide.md` |
| Flink | 1.18 | 1.20.0 | `Flink\03-api\09-language-foundations\pyflink-complete-guide.md` |
| Flink | 1.18 | 1.20.0 | `Flink\04-runtime\04.01-deployment\flink-deployment-ops-complete-guide.md` |
| Flink | 1.18.0 | 1.20.0 | `Flink\04-runtime\04.01-deployment\flink-deployment-ops-complete-guide.md` |
| Flink | 1.18 | 1.20.0 | `Flink\04-runtime\04.01-deployment\flink-kubernetes-autoscaler-deep-dive.md` |
| Flink | 1.18 | 1.20.0 | `Flink\04-runtime\04.01-deployment\multi-cloud-deployment-templates.md` |
| Flink | 1.19 | 1.20.0 | `Flink\04-runtime\04.01-deployment\multi-cloud-deployment-templates.md` |
| Flink | 1.18 | 1.20.0 | `Flink\04-runtime\04.03-observability\distributed-tracing.md` |
| Kafka | 3.7 | 3.8.0 | `Flink\05-ecosystem\05.01-connectors\diskless-kafka-cloud-native.md` |
| Flink | 1.18 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-24-connectors-guide.md` |
| Flink | 1.19 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-24-connectors-guide.md` |
| Flink | 1.18 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-connectors-ecosystem-complete-guide.md` |
| Flink | 1.19 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-connectors-ecosystem-complete-guide.md` |
| Flink | 1.18 | 1.20.0 | `Flink\05-ecosystem\05.01-connectors\flink-paimon-integration.md` |
| Flink | 1.18 | 1.20.0 | `Flink\05-ecosystem\05.02-lakehouse\flink-paimon-integration.md` |
| Flink | 1.18 | 1.20.0 | `Flink\05-ecosystem\05.02-lakehouse\streaming-lakehouse-architecture.md` |
| Flink | 1.18 | 1.20.0 | `Flink\06-ai-ml\flink-mcp-protocol-integration.md` |
| Flink | 1.18 | 1.20.0 | `Flink\07-rust-native\flink-rust-ecosystem-trends-2026.md` |
| Flink | 1.19 | 1.20.0 | `Flink\07-rust-native\flash-engine\01-flash-architecture.md` |
| Flink | 1.19 | 1.20.0 | `Flink\07-rust-native\flash-engine\04-nexmark-benchmark-analysis.md` |
| Flink | 1.18 | 1.20.0 | `Flink\08-roadmap\08.01-flink-24\flink-2.1-frontier-tracking.md` |
| Flink | 1.18 | 1.20.0 | `Flink\08-roadmap\08.01-flink-24\flink-2.4-tracking.md` |
| Scala | 2.12 | 2.13 | `Flink\08-roadmap\08.01-flink-24\flink-version-comparison-matrix.md` |
| Flink | 1.18 | 1.20.0 | `Flink\08-roadmap\08.01-flink-24\flink-version-evolution-complete-guide.md` |
| Flink | 1.19 | 1.20.0 | `Flink\08-roadmap\08.01-flink-24\flink-version-evolution-complete-guide.md` |
| Flink | 1.18.0 | 1.20.0 | `Flink\08-roadmap\08.01-flink-24\flink-version-evolution-complete-guide.md` |
| Flink | 1.19.0 | 1.20.0 | `Flink\08-roadmap\08.01-flink-24\flink-version-evolution-complete-guide.md` |
| Scala | 2.12 | 2.13 | `Flink\08-roadmap\08.01-flink-24\flink-version-evolution-complete-guide.md` |
| Flink | 1.18.0 | 1.20.0 | `Flink\08-roadmap\08.01-flink-24\release-checklist-template.md` |
| Flink | 1.18 | 1.20.0 | `Flink\09-practices\09.01-case-studies\case-iot-stream-processing.md` |
| Flink | 1.18 | 1.20.0 | `Flink\09-practices\09.01-case-studies\case-realtime-analytics.md` |
| Kafka | 3.7 | 3.8.0 | `Flink\09-practices\09.02-benchmarking\flink-24-25-benchmark-results.md` |
| Flink | 1.18 | 1.20.0 | `Flink\09-practices\09.02-benchmarking\performance-benchmark-suite.md` |
| Flink | 1.18 | 1.20.0 | `Flink\09-practices\09.04-security\security-hardening-guide.md` |
| Flink | 1.18 | 1.20.0 | `Knowledge\04-technology-selection\engine-selection-guide.md` |
| Flink | 1.18 | 1.20.0 | `Knowledge\04-technology-selection\flink-vs-risingwave.md` |
| Flink | 1.18 | 1.20.0 | `Knowledge\05-mapping-guides\migration-guides\05.4-flink-1x-to-2x-migration.md` |
| Flink | 1.18 | 1.20.0 | `Knowledge\06-frontier\materialize-comparison-guide.md` |
| Flink | 1.18 | 1.20.0 | `Knowledge\06-frontier\risingwave-integration-guide.md` |
| Flink | 1.18 | 1.20.0 | `Knowledge\06-frontier\streaming-materialized-view-architecture.md` |
| Kafka | 3.6 | 3.8.0 | `Knowledge\10-case-studies\social-media\10.4.2-realtime-recommendation-content.md` |
| Flink | 1.18 | 1.20.0 | `Knowledge\98-exercises\exercise-02-flink-basics.md` |
| Maven | 3.8 | 3.9.9 | `Knowledge\98-exercises\exercise-02-flink-basics.md` |
| Flink | 1.18 | 1.20.0 | `Knowledge\98-exercises\quick-ref-flink-vs-risingwave.md` |
| Maven | 3.8 | 3.9.9 | `Knowledge\98-exercises\README.md` |
| Scala | 2.11 | 2.13 | `reports\fictional-content-audit-20260405_143730.md` |
| Scala | 2.11 | 2.13 | `TECH-RADAR\00-INDEX.md` |
| Kafka | 3.7 | 3.8.0 | `TECH-RADAR\00-INDEX.md` |
| Kubernetes | 1.29 | 1.31 | `TECH-RADAR\00-INDEX.md` |
| Flink | 1.18 | 1.20.0 | `TECH-RADAR\evolution-timeline.md` |
| Scala | 2.11 | 2.13 | `TECH-RADAR\evolution-timeline.md` |
| Kafka | 3.7 | 3.8.0 | `TECH-RADAR\evolution-timeline.md` |
| Flink | 1.18 | 1.20.0 | `TECH-RADAR\migration-recommendations.md` |
| Scala | 2.11 | 2.13 | `TECH-RADAR\migration-recommendations.md` |
| Scala | 2.12 | 2.13 | `TECH-RADAR\migration-recommendations.md` |
| Scala | 2.12 | 2.13 | `TECH-RADAR\README.md` |
| Scala | 2.11 | 2.13 | `TECH-RADAR\README.md` |
| Kafka | 3.7 | 3.8.0 | `TECH-RADAR\risk-assessment.md` |
| Flink | 1.18 | 1.20.0 | `tutorials\00-5-MINUTE-QUICK-START.md` |
| Flink | 1.18.0 | 1.20.0 | `tutorials\00-5-MINUTE-QUICK-START.md` |
| Flink | 1.18 | 1.20.0 | `tutorials\01-environment-setup.md` |
| Flink | 1.18.1 | 1.20.0 | `tutorials\01-environment-setup.md` |
| Scala | 2.12 | 2.13 | `tutorials\03-flink-quickstart-script.md` |
| Maven | 3.8 | 3.9.9 | `tutorials\03-flink-quickstart-script.md` |


---

## 3. 当前版本统计 ✅

以下文档使用了最新的技术版本：

| 技术 | 文档中使用次数 | 版本 |
|------|----------------|------|
| Flink | 320 | 2.3 |
| Java | 55 | 11 |
| Kafka | 2 | 3.8.0 |
| Kubernetes | 1 | 1.31 |
| Python | 2 | 3.12 |
| Scala | 12 | 2.13 |


---

## 4. 更新建议

### 4.1 Flink专项更新建议

根据最新Flink版本 1.20.0，建议关注以下更新：

1. **检查API变更**: 从旧版本升级到新版本时，检查是否有废弃的API
2. **更新依赖版本**: 更新pom.xml或build.gradle中的Flink依赖
3. **验证配置参数**: 检查是否有新增或废弃的配置参数
4. **测试兼容性**: 在升级生产环境前进行充分测试

### 4.2 通用更新策略

1. **优先级**: 优先更新标记为"严重过时"的文档
2. **批量更新**: 同一技术的多个文档可以批量更新
3. **验证流程**: 更新后应进行以下检查：
   - 代码示例是否能正常运行
   - 配置参数是否仍然有效
   - 链接是否仍然可访问

### 4.3 自动化更新脚本示例

```bash
# 批量替换Flink版本号（请谨慎使用）
find . -name "*.md" -exec sed -i 's/Flink 1\.16/Flink 1.20/g' {} \;
find . -name "*.md" -exec sed -i 's/flink-1\.16/flink-1.20/g' {} \;

# 建议先进行干运行（dry-run）查看哪些文件会被修改
grep -r "Flink 1\.16" --include="*.md" .
```

### 4.4 版本跟踪清单

- [ ] 更新所有标记为"严重过时"的Flink版本
- [ ] 更新Java版本参考（建议升级到Java 17或21）
- [ ] 检查Scala版本兼容性
- [ ] 验证Kafka客户端版本
- [ ] 更新Kubernetes部署示例

---

## 5. 附录：版本获取方式

| 技术 | 版本查询方式 |
|------|--------------|
| Flink | GitHub Releases: <https://github.com/apache/flink/releases> |
| Java | Oracle/OpenJDK官网或SDK管理工具 |
| Kafka | Apache Kafka下载页 |
| Kubernetes | Kubernetes官方文档 |
| Python | Python官网或pyenv |

> **注意**: 本报告基于自动检测生成，建议人工复核后再进行更新操作。
