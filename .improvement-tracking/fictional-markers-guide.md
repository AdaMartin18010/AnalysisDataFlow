# 虚构内容标记指南

> 本文档定义如何标记项目中的虚构 API、配置参数、Maven 依赖和发布时间线。
>
> 版本: v1.0 | 生成日期: 2026-04-05

---

## 1. 标记原则

### 1.1 核心原则

1. **诚实透明**: 明确标识非官方内容，避免误导读者
2. **最小侵入**: 标记应尽可能不破坏文档的可读性
3. **一致性**: 同类内容使用统一的标记方式
4. **可追溯**: 标记应指向官方来源或相关 FLIP

### 1.2 标记强度分级

| 级别 | 适用场景 | 标记方式 |
|------|----------|----------|
| 🟡 **提示** | 实验性功能、规划特性 | HTML 注释或行内注释 |
| 🟠 **警告** | 概念设计、提案阶段 | 警告框 + 删除线 |
| 🔴 **强烈警告** | 虚构依赖、不存在配置 | 警告框 + 删除线 + 说明 |

---

## 2. SQL 语法标记

### 2.1 CREATE AGENT / CREATE TOOL / CREATE WORKFLOW

**推荐标记方式** (HTML 注释):

```markdown
<!-- FICTIONAL: 以下语法为 FLIP-531 提案阶段的概念设计，尚未正式发布 -->
CREATE AGENT sales_assistant
WITH (
  'model' = 'gpt-4',
  'temperature' = '0.7'
);
```

**替代标记方式** (代码块注释):

```markdown
```sql
-- FICTIONAL: 概念设计阶段，尚未正式发布
CREATE AGENT sales_assistant;
```

```

### 2.2 CREATE MODEL

**推荐标记方式**:

```markdown
<!-- FICTIONAL: Model DDL 为概念设计，以 Apache Flink 官方文档为准 -->
CREATE MODEL sentiment_analyzer
WITH (
  'provider' = 'openai',
  'model' = 'text-embedding-3-small'
);
```

### 2.3 VECTOR_SEARCH

**推荐标记方式** (带状态说明):

```markdown
<!-- FICTIONAL: VECTOR_SEARCH 为规划功能（FLIP-540），尚未正式发布 -->
SELECT * FROM TABLE(VECTOR_SEARCH(
  index_name => 'docs',
  query_vector => embedding
));
```

### 2.4 ML_PREDICT

**推荐标记方式**:

```markdown
<!-- FICTIONAL: ML_PREDICT 为实验性功能，API 可能变动 -->
SELECT ML_PREDICT('model_name', features) AS prediction
FROM input_table;
```

---

## 3. 配置参数标记

### 3.1 ai.agent.enabled

**YAML 文件标记**:

```yaml
# FICTIONAL: 未来配置参数（概念），尚未正式实现
# ai.agent.enabled: true
```

**或** (如必须保留在配置中):

```yaml
ai.agent.enabled: true  # FICTIONAL: 概念设计，尚未正式实现
```

**Java 代码标记**:

```java
// FICTIONAL: ai.agent.enabled 为未来配置参数（概念），尚未正式实现
// env.getConfig().setBoolean("ai.agent.enabled", true);
```

### 3.2 serverless.enabled

```yaml
# FICTIONAL: Serverless 模式配置（规划中），可能变动
serverless.enabled: true
```

---

## 4. Maven 依赖标记

### 4.1 flink-ai-agent / flink-ai-agents

**推荐标记方式** (XML 注释):

```xml
<!--
  FICTIONAL: flink-ai-agents 为未来可能提供的模块（设计阶段）
  尚未在 Maven Central 正式发布
-->
<!--
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-ai-agents</artifactId>
    <version>2.4.0</version>
</dependency>
-->
```

**简化标记** (行内):

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-ai-agents</artifactId>  <!-- FICTIONAL: 尚未正式发布 -->
    <version>2.4.0</version>
</dependency>
```

### 4.2 flink-mcp-connector

```xml
<!-- FICTIONAL: MCP 连接器（规划中），尚未正式发布 -->
<!-- <artifactId>flink-mcp-connector</artifactId> -->
```

### 4.3 flink-serverless

```xml
<!-- FICTIONAL: Serverless 模块（规划中），尚未正式发布 -->
<!-- <artifactId>flink-serverless</artifactId> -->
```

---

## 5. 时间线标记

### 5.1 发布时间线

**表格中的标记**:

```markdown
| 版本 | 预计时间 | 备注 |
|------|----------|------|
| Flink 2.3 | 2026 Q2 | <!-- FICTIONAL: 预计时间，以官方为准 --> |
| Flink 2.4 | 2026 Q4 | <!-- FICTIONAL: 预计时间，以官方为准 --> |
```

**或** (使用删除线 + 警告):

```markdown
> ⚠️ **FICTIONAL**: 以下时间线为项目推测，实际发布时间请以 [Apache Flink 官方](https://flink.apache.org/) 为准。

| 版本 | 时间线 |
|------|--------|
| ~~2026 Q1~~ | ~~预计发布~~ |
```

---

## 6. 警告框模板

### 6.1 通用警告框

```markdown
> ⚠️ **FICTIONAL CONTENT**
>
> 本节包含虚构或概念性的 API 设计，尚未在 Apache Flink 官方实现。
> 请以 [Apache Flink 官方文档](https://nightlies.apache.org/flink/) 为准。
```

### 6.2 FLIP 相关警告框

```markdown
> 📝 **FLIP-531 提案阶段**
>
> `CREATE AGENT` 语法为 [FLIP-531](https://cwiki.apache.org/confluence/display/FLINK/FLIP-531) 提案的概念设计，
> 目前处于讨论阶段，尚未正式发布。API 可能在最终实现中发生变化。
```

### 6.3 Maven 依赖警告框

```markdown
> 🚫 **FICTIONAL DEPENDENCY**
>
> `flink-ai-agents` 依赖当前不存在于 Maven Central 或 Flink 官方仓库。
> 这仅为概念设计阶段的示例，实际使用时需要等待官方发布。
```

---

## 7. Markdown 格式参考

### 7.1 删除线

用于标记虚构或过时的内容:

```markdown
~~CREATE AGENT~~ (FICTIONAL: 概念设计)
~~ai.agent.enabled~~ (FICTIONAL: 不存在配置)
```

### 7.2 代码块注释

```markdown
```sql
-- FICTIONAL: 以下 SQL 为概念设计
CREATE MODEL example;
```

```

### 7.3 行内代码标记

```markdown
`CREATE AGENT` <!-- FICTIONAL: 概念设计 -->
```

---

## 8. 快速参考表

| 内容类型 | 推荐标记 | 替代方案 |
|----------|----------|----------|
| SQL 语法 | `<!-- FICTIONAL: ... -->` | 代码块内注释 |
| 配置参数 | `# FICTIONAL: ...` | 行尾注释 |
| Maven 依赖 | XML 注释包裹 | 行内注释 |
| 时间线 | HTML 注释 | 删除线 + 警告框 |

---

## 9. 验证清单

在添加虚构内容标记前，请确认:

- [ ] 已识别内容确实不在 Flink 官方文档中
- [ ] 已检查相关 FLIP 的状态（如适用）
- [ ] 已选择适当的标记强度级别
- [ ] 标记方式与文档风格一致
- [ ] 已提供指向官方来源的链接（如适用）

---

*本指南由自动化扫描工具生成，应根据 Flink 官方进展定期更新。*
