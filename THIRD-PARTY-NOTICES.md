# 第三方声明与引用致谢 (Third-Party Notices)

> **AnalysisDataFlow 项目 - 统一流计算理论模型与工程实践知识库**

本文档列出本项目引用的第三方内容、学术来源、代码示例及其许可证信息。

---

## 1. 第三方软件与工具

### 1.1 Apache Flink

- **项目**: Apache Flink
- **许可证**: Apache License 2.0
- **官网**: <https://flink.apache.org/>
- **说明**: 本项目包含大量关于 Apache Flink 的架构分析、机制解读和最佳实践
- **版权**: Copyright 2014-2026 The Apache Software Foundation

### 1.2 Apache Paimon

- **项目**: Apache Paimon (Incubating)
- **许可证**: Apache License 2.0
- **官网**: <https://paimon.apache.org/>
- **说明**: 流式湖仓存储格式相关文档引用

### 1.3 Debezium

- **项目**: Debezium
- **许可证**: Apache License 2.0
- **官网**: <https://debezium.io/>
- **说明**: CDC 连接器相关文档引用

### 1.4 Kubernetes

- **项目**: Kubernetes
- **许可证**: Apache License 2.0
- **官网**: <https://kubernetes.io/>
- **说明**: Flink on K8s 部署相关内容引用

---

## 2. 学术引用与论文

本项目在构建过程中参考了大量学术论文，以下是主要引用来源：

### 2.1 Dataflow 模型

```
Akidau, T., Bradshaw, R., Chambers, C., Chernyak, S., Fernández-Moctezuma, R. J.,
Lax, R., ... & Whittle, S. (2015).
The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and
Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing.
Proceedings of the VLDB Endowment, 8(12), 1792-1803.
```

### 2.2 分布式系统时间语义

```
Lamport, L. (1978).
Time, Clocks, and the Ordering of Events in a Distributed System.
Communications of the ACM, 21(7), 558-565.
```

### 2.3 Exactly-Once 语义

```
Carbone, P., Fóra, G., Ewen, S., Haridi, S., & Tzoumas, K. (2016).
Lightweight Asynchronous Snapshots for Distributed Dataflows.
arXiv preprint arXiv:1506.08603.
```

### 2.4 流计算容错

```
Akidau, T., Balikov, A., Bekiroğlu, K., Chernyak, S., Haberman, J., Lax, R.,
... & Nordstrom, P. (2013).
MillWheel: Fault-Tolerant Stream Processing at Internet Scale.
Proceedings of the VLDB Endowment, 6(11), 1033-1044.
```

### 2.5 进程演算基础

```
Milner, R. (1989).
Communication and Concurrency.
Prentice Hall.

Hoare, C. A. R. (1978).
Communicating Sequential Processes.
Communications of the ACM, 21(8), 666-677.
```

### 2.6 更多引用

每篇具体文档末尾的 **引用参考 (References)** 章节列出了该文档直接引用的学术来源。

---

## 3. 官方文档引用

本项目参考了以下官方文档：

| 来源 | 许可证/条款 | 链接 |
|------|-------------|------|
| Apache Flink 官方文档 | Apache License 2.0 | <https://nightlies.apache.org/flink/> |
| Apache Kafka 官方文档 | Apache License 2.0 | <https://kafka.apache.org/documentation/> |
| Apache Spark 官方文档 | Apache License 2.0 | <https://spark.apache.org/docs/> |
| RisingWave 官方文档 | Apache License 2.0 | <https://docs.risingwave.com/> |
| PostgreSQL 官方文档 | PostgreSQL License | <https://www.postgresql.org/docs/> |
| MySQL 官方文档 | GPL v2 / 商业许可 | <https://dev.mysql.com/doc/> |
| Temporal 官方文档 | MIT License | <https://docs.temporal.io/> |

---

## 4. 代码示例许可

### 4.1 Flink 代码示例

本项目中的 Flink 代码示例主要基于：

- **来源**: Apache Flink 官方示例
- **原许可证**: Apache License 2.0
- **使用方式**: 根据 Apache License 2.0 允许的使用范围进行修改和再发布
- **声明**: 部分示例代码改编自 Apache Flink 官方文档和示例

### 4.2 Java/Scala 代码

- 代码示例遵循 Apache License 2.0
- 可直接用于学习和非商业用途
- 商业使用请遵守 Apache License 2.0 的归属要求

### 4.3 SQL 示例

- SQL 代码片段属于通用技术表达
- 不受特定许可证约束
- 建议引用时注明来源

---

## 5. 图表与可视化

### 5.1 Mermaid 图表

- 本项目使用 Mermaid 语法创建图表
- Mermaid 为开源项目，MIT 许可证
- 项目图表内容为原创或基于公开资料重绘

### 5.2 架构图

- 所有架构图均为本项目原创
- 遵循 Apache License 2.0 许可
- 引用时请保留来源声明

---

## 6. 竞品对比与商标

### 6.1 提及的产品和商标

本文档中提及的产品名称和商标归各自所有者所有：

| 商标/产品 | 所有者 |
|-----------|--------|
| Apache Flink®, Flink® | The Apache Software Foundation |
| Apache Spark®, Spark® | The Apache Software Foundation |
| Apache Kafka®, Kafka® | The Apache Software Foundation |
| Kubernetes® | The Linux Foundation |
| Amazon Web Services™, AWS™ | Amazon.com, Inc. |
| Google Cloud Platform™, GCP™ | Google LLC |
| Microsoft Azure™ | Microsoft Corporation |
| RisingWave | RisingWave Labs |
| Materialize | Materialize, Inc. |
| Bytewax | Bytewax, Inc. |

### 6.2 声明

- 所有商标均为其各自所有者的财产
- 本项目对商标的使用符合合理使用原则
- 不暗示与商标所有者的关联或认可

---

## 7. 引用规范

### 7.1 学术引用

如果您在学术论文中引用了本项目，请同时引用本项目引用的原始来源：

```
本项目基于以下工作构建：[原始论文引用]
详细分析参见：AdaMartin18010, AnalysisDataFlow Project, 2026.
```

### 7.2 技术文档引用

```
本文档部分分析基于 AnalysisDataFlow 项目 (https://github.com/luyanfeng/AnalysisDataFlow)
原始概念来自 [原始来源]
```

---

## 8. 致谢

感谢以下项目和组织对开源社区的贡献，使本项目成为可能：

- **Apache Software Foundation** - Flink, Kafka, Spark 等优秀开源项目
- **Google** - Dataflow 模型和 MillWheel 论文
- **学术界** - 分布式系统领域的先驱研究者
- **开源社区** - 所有为流计算生态做出贡献的开发者

---

## 9. 更新记录

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2026-04-03 | v1.0 | 初始版本，整理主要第三方引用 |

---

## 10. 反馈与修正

如果您发现：

- 遗漏的引用声明
- 许可证信息错误
- 归属不当的内容

请通过以下方式反馈：

- **提交 Issue**: <https://github.com/luyanfeng/AnalysisDataFlow/issues>
- **联系作者**: 通过 GitHub 平台

---

**最后更新**: 2026-04-03
**文档版本**: v1.0
**许可证**: Apache License 2.0
