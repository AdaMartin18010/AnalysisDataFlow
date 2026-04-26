# 文件系统连接器演进 特性跟踪

> 所属阶段: Flink/connectors/evolution | 前置依赖: [File Connectors][^1] | 形式化等级: L3

## 1. 概念定义 (Definitions)

### Def-F-Conn-File-01: File Source

文件源：
$$
\text{FileSource} : \text{Path} \to \text{Stream}
$$

### Def-F-Conn-File-02: File Sink

文件Sink：
$$
\text{FileSink} : \text{Stream} \xrightarrow{\text{batch}} \text{File}
$$

## 2. 属性推导 (Properties)

### Prop-F-Conn-File-01: Exactly-Once

Exactly-Once文件写入：
$$
\text{TwoPhaseCommit} + \text{Staging} \implies \text{Exactly-Once}
$$

## 3. 关系建立 (Relations)

### 文件连接器演进

| 版本 | 特性 | 状态 |
|------|------|------|
| 2.3 | StreamingFileSink | GA |
| 2.4 | FileSource FLIP-27 | GA |
| 2.5 | 格式增强 | GA |
| 3.0 | 统一文件API | 设计中 |

## 4. 论证过程 (Argumentation)

### 4.1 支持格式

| 格式 | Source | Sink | 压缩 |
|------|--------|------|------|
| CSV | ✅ | ✅ | ✅ |
| JSON | ✅ | ✅ | ✅ |
| Parquet | ✅ | ✅ | ✅ |
| ORC | ✅ | ✅ | ✅ |
| Avro | ✅ | ✅ | ✅ |

## 5. 形式证明 / 工程论证

### 5.1 FileSource

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
FileSource<String> source = FileSource
    .forRecordStreamFormat(
        new TextLineFormat(),
        new Path("hdfs:///input"))
    .setFileEnumeratorParallelism(10)
    .build();
```

## 6. 实例验证 (Examples)

### 6.1 Parquet Sink

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
FileSink<GenericRecord> sink = FileSink
    .forBulkFormat(
        new Path("hdfs:///output"),
        ParquetAvroWriters.forGenericRecord(schema))
    .withBucketAssigner(new DateTimeBucketAssigner<>())
    .withRollingPolicy(OnCheckpointRollingPolicy.build())
    .build();
```

## 7. 可视化 (Visualizations)

```mermaid
graph LR
    A[文件系统] --> B[File Source]
    B --> C[处理]
    C --> D[File Sink]
    D --> E[文件系统]
```

### 文件连接器演进思维导图

以下思维导图以"文件连接器演进"为中心，展示从本地文件到对象存储、格式支持与高级特性的全景。

```mermaid
mindmap
  root((文件连接器演进))
    本地文件
      TextFile
      CSV
      行格式
      简单读写
    HDFS集成
      Hadoop兼容
      NameNode
      数据本地性
      高可用
    对象存储
      S3
      OSS
      GCS
      Azure Blob
      分层存储
    格式支持
      Parquet
      Avro
      ORC
      JSON
      CSV
      Protobuf
    高级特性
      分区发现
      文件监控
      Exactly-Once
      压缩加密
```

### 存储系统到文件格式映射

以下层次图展示存储系统、文件格式与Flink读写能力之间的多维关联。

```mermaid
graph TB
    subgraph 存储系统
        A1[本地文件系统]
        A2[HDFS]
        A3[S3]
        A4[OSS]
        A5[GCS]
        A6[Azure Blob]
    end

    subgraph 文件格式
        B1[TextLine]
        B2[CSV]
        B3[JSON]
        B4[Parquet]
        B5[ORC]
        B6[Avro]
        B7[Protobuf]
    end

    subgraph Flink读写能力
        C1[流式读取<br/>FileSource]
        C2[批量写出<br/>FileSink]
        C3[分区发现<br/>Partition Discovery]
        C4[Exactly-Once<br/>两阶段提交]
    end

    A1 --> B1
    A1 --> B2
    A2 --> B4
    A2 --> B5
    A2 --> B6
    A3 --> B4
    A3 --> B6
    A4 --> B4
    A4 --> B3
    A5 --> B4
    A5 --> B7
    A6 --> B4
    A6 --> B3

    B1 --> C1
    B2 --> C1
    B3 --> C1
    B4 --> C1
    B4 --> C2
    B4 --> C3
    B4 --> C4
    B5 --> C1
    B5 --> C2
    B6 --> C1
    B6 --> C2
    B7 --> C1
```

### 文件连接器选型决策树

以下决策树指导在不同场景下选择合适的文件连接器与存储方案。

```mermaid
flowchart TD
    Start([开始选型]) --> Q1{数据规模与部署环境?}

    Q1 -->|本地开发/测试| A1[LocalFileSystem]
    A1 --> A2[TextLine / CSV]
    A2 --> A3[小数据量快速验证]

    Q1 -->|大数据存储/传统集群| B1[HDFS]
    B1 --> B2[Parquet / ORC]
    B2 --> B3[批量处理<br/>高吞吐列式存储]

    Q1 -->|云原生/弹性扩展| C1[S3 / OSS / GCS / Azure Blob]
    C1 --> C2{性能优化需求?}
    C2 -->|高吞吐分析| C3[Parquet + 对象存储优化]
    C2 -->|分层存储| C4[热温冷分层<br/>生命周期管理]

    Q1 -->|实时入湖/流批一体| D1[Streaming File Sink]
    D1 --> D2[分区提交<br/>Partition Commit]
    D2 --> D3[滚动策略 + 压缩]
    D3 --> D4[Exactly-Once 保证]
```

## 8. 引用参考 (References)

[^1]: Flink File Connector Documentation

---

## 跟踪信息

| 属性 | 值 |
|------|-----|
| 版本 | 2.4-3.0 |
| 当前状态 | 演进中 |

---

*文档版本: v1.0 | 创建日期: 2026-04-19*
