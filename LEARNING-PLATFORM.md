# 流计算学习平台

> 基于 AnalysisDataFlow 项目的在线学习平台 MVP
> 版本: v1.0 | 状态: 已完成 ✅

---

## 平台概述

流计算学习平台是一个面向 Apache Flink 和流处理技术的交互式在线学习系统。平台提供系统化的课程体系、交互式实验环境和实战编程挑战，帮助学习者从入门到精通掌握流计算核心技术。

### 平台特性

- 📚 **系统化课程**: 3门核心课程，13个课时，涵盖从基础到高级
- 🧪 **交互实验**: 3个可视化实验，动手理解核心机制
- 🏆 **编程挑战**: 3个实战挑战，检验学习成果
- 🎨 **现代UI**: 响应式设计，支持桌面和移动设备
- 🔗 **项目集成**: 直接引用 AnalysisDataFlow 项目文档

---

## 平台结构

```
learning-platform/
├── index.html                    # 主入口页面
├── LEARNING-PLATFORM.md          # 平台文档 (本文档)
├── courses/                      # 课程目录
│   ├── index.md                  # 课程目录索引
│   ├── course-01-flink-basics.html       # 课程1: Flink基础速成
│   ├── course-02-design-patterns.html    # 课程2: 流处理设计模式
│   └── course-03-advanced-topics.html    # 课程3: 高级主题与调优
├── labs/                         # 交互实验
│   ├── index.md                  # 实验目录索引
│   ├── lab-01-watermark.html     # 实验1: Watermark可视化
│   ├── lab-02-checkpoint.html    # 实验2: Checkpoint机制模拟
│   └── lab-03-backpressure.html  # 实验3: 背压检测实验
├── challenges/                   # 编程挑战
│   ├── index.md                  # 挑战目录索引
│   ├── challenge-01-wordcount.html       # 挑战1: WordCount实现
│   ├── challenge-02-window-agg.html      # 挑战2: 窗口聚合优化
│   └── challenge-03-state-mgmt.html      # 挑战3: 状态管理设计
└── assets/                       # 静态资源
```

---

## 课程目录

### 课程1: Flink基础速成 (5节课)

| 课节 | 标题 | 时长 | 关键概念 |
|------|------|------|----------|
| 1.1 | Flink简介与安装 | 30min | 架构概览、环境搭建 |
| 1.2 | DataStream API基础 | 40min | Source、Transformation、Sink |
| 1.3 | 第一个流处理应用 | 35min | WordCount、执行模式 |
| 1.4 | 时间与Watermark | 45min | Event Time、Processing Time |
| 1.5 | 基础窗口操作 | 40min | Tumbling、Sliding Window |

**文件路径**: `learning-platform/courses/course-01-flink-basics.html`

---

### 课程2: 流处理设计模式 (4节课)

| 课节 | 标题 | 时长 | 关键概念 |
|------|------|------|----------|
| 2.1 | 窗口高级特性 | 50min | Session Window、Custom Trigger |
| 2.2 | 状态管理基础 | 55min | Keyed State、Operator State |
| 2.3 | 复杂事件处理(CEP) | 60min | Pattern API、时间约束 |
| 2.4 | 连接器与集成 | 45min | Kafka、JDBC、File System |

**文件路径**: `learning-platform/courses/course-02-design-patterns.html`

---

### 课程3: 高级主题与调优 (4节课)

| 课节 | 标题 | 时长 | 关键概念 |
|------|------|------|----------|
| 3.1 | Checkpoint与容错 | 60min | Barrier、Exactly-Once |
| 3.2 | 背压与流量控制 | 50min | Credit-based Flow Control |
| 3.3 | 性能调优实践 | 55min | 并行度、状态后端选型 |
| 3.4 | 生产环境部署 | 45min | HA配置、监控告警 |

**文件路径**: `learning-platform/courses/course-03-advanced-topics.html`

---

## 交互实验

### 实验1: Watermark可视化

**难度**: 中级 | **时长**: 约30分钟

通过交互式图表理解 Watermark 的生成和传播机制：
- 事件时间与处理时间的关系
- Watermark 传播可视化
- 乱序数据处理演示
- 迟到事件处理

**技术实现**: HTML5 Canvas + JavaScript 动画

**文件路径**: `learning-platform/labs/lab-01-watermark.html`

---

### 实验2: Checkpoint机制模拟

**难度**: 高级 | **时长**: 约45分钟

模拟分布式 Checkpoint 过程：
- Barrier 注入和传播
- 对齐与非对齐 Checkpoint
- 状态快照过程
- 故障恢复模拟

**技术实现**: HTML5 Canvas + 实时动画

**文件路径**: `learning-platform/labs/lab-02-checkpoint.html`

---

### 实验3: 背压检测实验

**难度**: 高级 | **时长**: 约40分钟

可视化背压的传播和处理：
- 背压产生的原因
- Credit-based 流控制
- 缓冲区状态监控
- 背压解决策略

**技术实现**: HTML5 Canvas + 实时指标监控

**文件路径**: `learning-platform/labs/lab-03-backpressure.html`

---

## 编程挑战

### 挑战1: WordCount实现

**难度**: 初级 | **积分**: 100

实现流处理领域的 "Hello World" - 实时词频统计。

**要求**:
- 从 Socket 或 Kafka 读取文本数据
- 实时统计词频
- 每5秒输出一次结果
- 支持 Exactly-Once 语义

**文件路径**: `learning-platform/challenges/challenge-01-wordcount.html`

---

### 挑战2: 窗口聚合优化

**难度**: 中级 | **积分**: 200

优化复杂的窗口聚合操作，处理迟到数据和增量计算。

**要求**:
- 实现两阶段聚合解决数据倾斜
- 处理迟到数据到侧输出流
- 使用增量聚合优化性能
- 支持 Session Window 动态合并

**文件路径**: `learning-platform/challenges/challenge-02-window-agg.html`

---

### 挑战3: 状态管理设计

**难度**: 高级 | **积分**: 300

设计高效的状态管理方案，实现 Exactly-Once 语义。

**要求**:
- 使用 Keyed State 实现去重
- 设计 TTL 策略自动清理过期状态
- 处理大规模状态 (使用 RocksDB)
- 实现状态迁移和升级

**文件路径**: `learning-platform/challenges/challenge-03-state-mgmt.html`

---

## 学习路径

### 初级路径 (1-2周)

```
课程1 (全部5节) → 挑战1 → 实验1
```

**目标**: 掌握 Flink 基础，能够编写简单的流处理应用

---

### 中级路径 (2-3周)

```
课程2 (全部4节) → 挑战2 → 实验2
```

**目标**: 掌握流处理设计模式，处理复杂业务场景

---

### 高级路径 (3-4周)

```
课程3 (全部4节) → 挑战3 → 实验3
```

**目标**: 掌握生产环境调优和故障处理

---

## 访问方式

### 本地访问

```bash
# 进入学习平台目录
cd learning-platform

# 使用 Python 启动本地服务器
python -m http.server 8080

# 或使用 Node.js
npx serve .

# 浏览器访问
open http://localhost:8080
```

### 直接使用

直接在浏览器中打开 `learning-platform/index.html` 文件即可访问。

---

## 技术栈

- **前端**: HTML5, CSS3, JavaScript (原生)
- **可视化**: HTML5 Canvas API
- **图表**: Mermaid.js (流程图)
- **样式**: 自定义 CSS (无第三方框架依赖)
- **兼容性**: 现代浏览器 (Chrome, Firefox, Safari, Edge)

---

## 内容统计

| 类型 | 数量 | 说明 |
|------|------|------|
| 核心课程 | 3门 | 13课时，约16小时内容 |
| 交互实验 | 3个 | 约115分钟交互体验 |
| 编程挑战 | 3个 | 600积分奖励系统 |
| 代码示例 | 50+ | 完整的可运行代码 |
| 测试用例 | 15+ | 验证实现正确性 |

---

## 参考资料

平台内容引用自 AnalysisDataFlow 项目：

- [项目 README](./README.md)
- [Struct 形式理论目录](./Struct/)
- [Knowledge 知识结构目录](./Knowledge/)
- [Flink 技术文档目录](./Flink/)
- [快速入门指南](./QUICK-START.md)
- [最佳实践指南](./BEST-PRACTICES.md)

---

## 未来扩展计划

- [ ] 添加更多课程 (SQL API、Table API、机器学习集成)
- [ ] 在线代码编辑器集成 (类似 Jupyter Notebook)
- [ ] 用户进度跟踪和成就系统
- [ ] 社区讨论区
- [ ] 移动端 App
- [ ] 视频教程集成

---

## 贡献指南

欢迎提交 Issue 和 PR 来改进学习平台：

1. 报告课程内容错误
2. 建议新的实验或挑战
3. 改进 UI/UX 设计
4. 添加更多代码示例

---

## 许可证

本学习平台内容遵循与 AnalysisDataFlow 项目相同的开源许可证。

---

*流计算学习平台 v1.0 - 让流计算学习更简单*
