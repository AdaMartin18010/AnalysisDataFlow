# 自定义连接器开发 演进 特性跟踪

> 所属阶段: Flink/connectors/evolution | 前置依赖: [Connector Framework][^1] | 形式化等级: L3

## 1. 概念定义 (Definitions)

### Def-F-Conn-Custom-01: Connector Framework

连接器框架：
$$
\text{Framework} = \langle \text{SourceAPI}, \text{SinkAPI}, \text{TableAPI} \rangle
$$

### Def-F-Conn-Custom-02: SplitEnumerator

分片枚举器：
$$
\text{Enumerator} : \text{Discovery} \to \{\text{Split}_i\}
$$

## 2. 属性推导 (Properties)

### Prop-F-Conn-Custom-01: Extensibility

可扩展性：
$$
\forall \text{Source} : \text{Implements}(\text{Source}, \text{SourceInterface})
$$

## 3. 关系建立 (Relations)

### 连接器框架演进

| 版本 | 特性 | 状态 |
|------|------|------|
| 2.3 | FLIP-27 Source | GA |
| 2.4 | 新Sink API | GA |
| 2.5 | Table API增强 | GA |
| 3.0 | 统一框架 | 设计中 |

## 4. 论证过程 (Argumentation)

### 4.1 Source组件

| 组件 | 职责 |
|------|------|
| Split | 数据分片定义 |
| SplitEnumerator | 分片分配 |
| SourceReader | 数据读取 |
| SourceReaderContext | 运行时上下文 |

## 5. 形式证明 / 工程论证

### 5.1 自定义Source

```java
public class MySource implements Source<String, MySplit, MyCheckpoint> {

    @Override
    public SplitEnumerator<MySplit, MyCheckpoint> createEnumerator(
            SplitEnumeratorContext<MySplit> enumContext) {
        return new MySplitEnumerator(enumContext);
    }

    @Override
    public SourceReader<String, MySplit> createReader(
            SourceReaderContext readerContext) {
        return new MySourceReader(readerContext);
    }
}
```

## 6. 实例验证 (Examples)

### 6.1 Split实现

```java
public class MySplit implements SourceSplit {
    private final String splitId;
    private final long startOffset;
    private final long endOffset;

    @Override
    public String splitId() {
        return splitId;
    }
}
```

## 7. 可视化 (Visualizations)

```mermaid
graph TB
    A[Enumerator] --> B[分配Splits]
    B --> C[Reader 1]
    B --> D[Reader 2]
    C --> E[读取数据]
    D --> E
```

### 思维导图：自定义连接器开发全貌

以下思维导图以"自定义连接器开发"为中心，放射展开五大核心维度：

```mermaid
mindmap
  root((自定义连接器开发))
    Source开发
      Split设计
      Enumerator实现
      Reader开发
      事件时间处理
      Watermark生成
    Sink开发
      Writer实现
      Committer设计
      TwoPhaseCommit
      预写日志
    测试验证
      单元测试
      集成测试
      Exactly-Once测试
      兼容性测试
    文档发布
      API文档
      使用指南
      示例代码
      版本管理
    最佳实践
      错误处理
      指标暴露
      背压支持
      资源管理
```

### 多维关联树：组件→步骤→质量门禁

以下层次图展示连接器组件到开发步骤再到质量门禁的完整映射关系：

```mermaid
graph TB
    subgraph 连接器组件
        C1[Source API<br/>FLIP-27]
        C2[Sink API<br/>FLIP-143]
        C3[Table API<br/>统一接口]
    end

    subgraph 开发步骤
        D1[接口实现]
        D2[Split与事务设计]
        D3[序列化与配置]
        D4[容错与恢复]
    end

    subgraph 质量门禁
        Q1[单元测试通过]
        Q2[集成测试通过]
        Q3[Exactly-Once验证]
        Q4[兼容性测试通过]
    end

    C1 --> D1
    C1 --> D2
    C1 --> D4
    C2 --> D1
    C2 --> D2
    C2 --> D4
    C3 --> D1
    C3 --> D3
    D1 --> Q1
    D2 --> Q2
    D3 --> Q4
    D4 --> Q3
```

### 决策树：自定义连接器开发路径

以下决策树展示面对不同场景时应选择的自定义连接器开发路径：

```mermaid
flowchart TD
    Start([开始自定义连接器开发]) --> Q1{连接器类型?}
    Q1 -->|新Source| A1[采用新Source API<br/>FLIP-27]
    Q1 -->|新Sink| B1[采用新Sink API<br/>FLIP-143]
    Q1 -->|旧连接器升级| C1[设计兼容层]
    Q1 -->|社区贡献| D1[遵循社区规范]

    A1 --> A2[Split设计与实现]
    A2 --> A3[Enumerator分配策略]
    A3 --> A4[Reader并行读取]
    A4 --> End1[发布与文档]

    B1 --> B2{事务语义需求?}
    B2 -->|需要Exactly-Once| B3[TwoPhaseCommit实现]
    B2 -->|At-Least-Once| B4[预写日志模式]
    B3 --> End1
    B4 --> End1

    C1 --> C2[渐进迁移策略]
    C2 --> C3[向后兼容保证]
    C3 --> End1

    D1 --> D2[完整测试覆盖]
    D2 --> D3[贡献者指南对齐]
    D3 --> End1
```

## 8. 引用参考 (References)

[^1]: Flink Connector Development Documentation
[^2]: Apache Flink, "FLIP-27: Refactor Source Interface", 2020. https://cwiki.apache.org/confluence/display/FLINK/FLIP-27
[^3]: Apache Flink, "FLIP-143: Unified Sink API", 2021. https://cwiki.apache.org/confluence/display/FLINK/FLIP-143
[^4]: Apache Flink Documentation, "Custom Connector Development Guide", 2025. https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/sources/

---

## 跟踪信息

| 属性 | 值 |
|------|-----|
| 版本 | 2.4-3.0 |
| 当前状态 | 演进中 |

---

*文档版本: v1.0 | 创建日期: 2026-04-13*
