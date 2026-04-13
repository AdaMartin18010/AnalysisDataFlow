# 学生学习路径

> **难度级别**: 初级 | **预计时长**: 4-6周 | **目标受众**: 计算机专业学生、转行者

---

## 路径概览

### 学习目标

- 建立流处理的基础概念框架
- 掌握Flink的基本使用
- 具备入门级项目开发能力

### 前置知识要求

- 基础编程能力(Java/Python)
- 了解基本的数据结构
- 对大数据技术有兴趣

### 完成标准

能够独立运行Flink程序，理解基本概念，完成入门级项目

---

## 阶段划分

### 阶段1: 入门阶段

**时间安排**: 第1周

**学习主题**:

- 什么是流处理？为什么需要它？
- 流处理与批处理的对比
- Flink简介
- 开发环境搭建

**推荐文档**:

- [Knowledge/01-concept-atlas/streaming-models-mindmap.md](../Knowledge/01-concept-atlas/streaming-models-mindmap.md)
- [Knowledge/98-exercises/exercise-02-flink-basics.md](../Knowledge/98-exercises/exercise-02-flink-basics.md)
- [Flink/01-architecture/deployment-architectures.md](../Flink/01-concepts/deployment-architectures.md)

**实践任务**:

1. 安装Java和Flink
2. 运行官方WordCount示例
3. 理解代码结构

---

### 阶段2: 基础概念

**时间安排**: 第2-3周

**学习主题**:

- DataStream API基础
- 时间语义（Event Time vs Processing Time）
- Window类型（滚动、滑动、会话）
- 基本转换操作（map, filter, keyBy, reduce）

**推荐文档**:

- [Flink/02-core/time-semantics-and-watermark.md](../Flink/02-core/time-semantics-and-watermark.md)
- [Knowledge/02-design-patterns/pattern-event-time-processing.md](../Knowledge/02-design-patterns/pattern-event-time-processing.md)
- [Knowledge/02-design-patterns/pattern-windowed-aggregation.md](../Knowledge/02-design-patterns/pattern-windowed-aggregation.md)
- [Knowledge/98-exercises/exercise-02-flink-basics.md](../Knowledge/98-exercises/exercise-02-flink-basics.md)

**实践任务**:

1. 实现自定义转换函数
2. 使用不同时间语义处理数据
3. 尝试各种Window类型

---

### 阶段3: 实践入门

**时间安排**: 第4-5周

**学习主题**:

- 有状态计算入门
- Flink SQL基础
- 简单的数据源和输出
- 调试技巧

**推荐文档**:

- [Flink/03-sql-table-api/sql-vs-datastream-comparison.md](../Flink/03-api/03.02-table-sql-api/sql-vs-datastream-comparison.md)
- [Knowledge/02-design-patterns/pattern-stateful-computation.md](../Knowledge/02-design-patterns/pattern-stateful-computation.md)
- [Knowledge/98-exercises/exercise-02-flink-basics.md](../Knowledge/98-exercises/exercise-02-flink-basics.md)

**实践任务**:

1. 实现WordCount（有状态版本）
2. 用Flink SQL查询数据
3. 连接Kafka读写数据

---

### 阶段4: 项目实战

**时间安排**: 第6周

**学习主题**:

- 综合项目开发
- 代码组织
- 问题排查
- 学习资源整理

**推荐文档**:

- [Flink/07-case-studies/case-realtime-analytics.md](../Flink/09-practices/09.01-case-studies/case-realtime-analytics.md)
- [Knowledge/98-exercises/README.md](../Knowledge/98-exercises/README.md)
- [Knowledge/09-anti-patterns/anti-pattern-checklist.md](../Knowledge/09-anti-patterns/anti-pattern-checklist.md)

**实践任务**:

1. 完成一个端到端项目
2. 整理学习笔记
3. 规划后续学习方向

---

## 学习资源索引

### 概念入门 (Knowledge/)

| 文档 | 主题 | 难度 | 预计时间 |
|------|------|------|----------|
| `01-concept-atlas/streaming-models-mindmap.md` | 流处理模型思维导图 | L2 | 2h |
| `02-design-patterns/pattern-event-time-processing.md` | 事件时间处理 | L3 | 3h |
| `02-design-patterns/pattern-windowed-aggregation.md` | 窗口聚合 | L2 | 2h |

### 练习 (Knowledge/98-exercises/)

| 文档 | 主题 | 难度 | 预计时间 |
|------|------|------|----------|
| `exercise-02-flink-basics.md` | Flink基础练习 | L2 | 4h |
| `exercise-03-checkpoint-analysis.md` | Checkpoint分析 | L3 | 3h |

### Flink基础 (Flink/)

| 文档 | 主题 | 难度 | 预计时间 |
|------|------|------|----------|
| `01-architecture/deployment-architectures.md` | 部署架构 | L2 | 2h |
| `02-core-mechanisms/time-semantics-and-watermark.md` | 时间语义 | L3 | 3h |
| `03-sql-table-api/sql-vs-datastream-comparison.md` | SQL vs DataStream | L2 | 2h |

---

## 实践项目

### 项目1: WordCount流处理程序

**项目描述**: 实现经典的WordCount，但处理实时数据流

**技术要求**:

- 从Socket或文件读取数据
- 实时统计词频
- 支持Window聚合
- 输出结果到控制台或文件

**学习要点**:

- DataStream API基础
- KeyBy和聚合操作
- Window使用

**产出物**:

- 可运行的代码
- 代码注释说明

---

### 项目2: 简单的实时数据统计

**项目描述**: 模拟实时数据，进行多维度统计

**技术要求**:

- 生成模拟数据流
- 按不同维度分组统计
- 计算实时指标（平均值、最大值等）
- 结果可视化（可选）

**学习要点**:

- 自定义数据源
- 复杂聚合
- 多流处理

**产出物**:

- 完整代码
- 运行截图
- 简要设计说明

---

### 项目3: 端到端的流处理项目

**项目描述**: 综合应用所学知识完成一个完整项目

**建议主题**:

- 实时天气数据分析
- 股票数据实时监控
- 网站访问日志分析
- 游戏实时排行榜

**技术要求**:

- 数据源接入
- 数据处理逻辑
- 结果输出
- 基本错误处理

**产出物**:

- 项目代码
- README文档
- 演示视频或截图

---

## 自测检查点

- [ ] **检查点1**: 理解流处理和批处理的区别
- [ ] **检查点2**: 能够独立运行Flink程序
- [ ] **检查点3**: 能够解释基本的流处理概念（Time, Window, State）
- [ ] **检查点4**: 能够使用DataStream API实现基本功能
- [ ] **检查点5**: 能够使用Flink SQL进行查询
- [ ] **检查点6**: 完成至少一个综合项目

---

## 学习建议

### 时间安排建议

- 每天至少1-2小时学习时间
- 理论学习和实践结合（1:2比例）
- 每周末做一个小项目巩固

### 常见问题

1. **环境搭建失败**: 检查Java版本，参考官方文档
2. **概念理解困难**: 结合图形和示例，多查资料
3. **代码报错**: 善用搜索引擎，查看官方示例

### 进阶方向

完成本路径后，可以选择：

- 数据工程师路径（深入工程实践）
- 后端开发路径（与业务系统结合）
- 研究员路径（深入学习理论）

---

## 延伸阅读

- Apache Flink官方教程: <https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/>
- 《Streaming Systems》入门章节
- Flink官方示例代码: <https://github.com/apache/flink/tree/master/flink-examples>

---

*此学习路径为AnalysisDataFlow项目预定义路径*
