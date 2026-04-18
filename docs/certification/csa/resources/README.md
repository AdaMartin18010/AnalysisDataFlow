# CSA 学习资源

> **初级认证学习资料汇总**

## 文档资源

### 必读文档

| 优先级 | 文档 | 说明 | 预计时间 |
|--------|------|------|----------|
| P0 | [5分钟快速开始](../../../../tutorials/00-5-MINUTE-QUICK-START.md) | 项目入门 | 10min |
| P0 | [环境搭建](../../../../tutorials/01-environment-setup.md) | 开发环境 | 30min |
| P0 | [第一个 Flink 作业](../../../../tutorials/02-first-flink-job.md) | Hello World | 45min |
| P1 | [流处理基础概念](../../../../tutorials/02-streaming-fundamentals-script.md) | 核心概念 | 60min |
| P1 | [流模型思维导图](../../../../Knowledge/01-concept-atlas/streaming-models-mindmap.md) | 概念图谱 | 30min |

### Flink 官方文档

- [Flink 1.18 文档](https://nightlies.apache.org/flink/flink-docs-release-1.18/)
- [DataStream API](https://nightlies.apache.org/flink/flink-docs-release-1.18/docs/dev/datastream/overview/)
- [窗口操作](https://nightlies.apache.org/flink/flink-docs-release-1.18/docs/dev/datastream/operators/windows/)
- [状态管理](https://nightlies.apache.org/flink/flink-docs-release-1.18/docs/dev/datastream/fault-tolerance/state/)

## 视频资源

### 推荐课程

| 课程 | 平台 | 时长 | 链接 |
|------|------|------|------|
| Flink 入门到实战 | B站 | 10h | [链接](https://www.bilibili.com) |
| Apache Flink 官方教程 | YouTube | 5h | [链接](https://youtube.com) |
| 流计算系统课程 | Coursera | 8h | [链接](https://coursera.org) |

## 代码示例

### 官方示例

```bash
# 下载 Flink 官方示例
git clone https://github.com/apache/flink.git
cd flink/flink-examples
```

### 本项目示例

- [Flink/01-getting-started/]
- [tutorials/interactive/coding-challenges/](../../../../tutorials/interactive/coding-challenges/)

## 练习题库

- [CSA 练习题库](../quizzes/README.md) - 300+ 题目
- [流处理基础测验](../../../../tutorials/interactive/quizzes/stream-processing-fundamentals.md)
- [Flink 专项测验](../../../../tutorials/interactive/quizzes/flink-specialized.md)

## 推荐书籍

### 必读

1. **《Streaming Systems》** - Tyler Akidau et al.
   - 第 1-4 章：流计算基础
   - 第 5-6 章：时间语义与窗口

2. **《Apache Flink实战》** - 崔星灿
   - 第 1-5 章：入门与基础

### 参考

1. **《Designing Data-Intensive Applications》** - Martin Kleppmann
   - 第 11 章：流处理

## 工具推荐

### 开发工具

| 工具 | 用途 | 推荐配置 |
|------|------|----------|
| IntelliJ IDEA | Java 开发 | 安装 Flink 插件 |
| VS Code | 轻量编辑 | Java 扩展包 |
| Maven | 构建工具 | 3.6+ |

### 调试工具

- Flink Web UI: 作业监控
- VisualVM: JVM 监控
- Kafka Tool: Kafka 管理

## 社区资源

- [Flink 中文社区](https://flink-learning.org.cn/)
- [Stack Overflow - Flink](https://stackoverflow.com/questions/tagged/apache-flink)
- [Flink 用户邮件列表](https://flink.apache.org/community.html#mailing-lists)

## 认证准备清单

### 考前检查

- [ ] 完成全部 8 个模块学习
- [ ] 完成 16 个实验任务
- [ ] 练习题库正确率 80%+
- [ ] 完成综合项目
- [ ] 完成 1 套模拟考试

### 知识掌握度自测

- [ ] 能解释 Event Time 与 Processing Time 区别
- [ ] 能选择合适的窗口类型
- [ ] 熟练使用 DataStream API
- [ ] 理解 Watermark 作用
- [ ] 能配置 Checkpoint
- [ ] 能部署 Standalone 集群

---

[返回课程大纲 →](../syllabus-csa.md)
