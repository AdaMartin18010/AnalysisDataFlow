# CDC连接器演进 特性跟踪

> 所属阶段: Flink/connectors/evolution | 前置依赖: [CDC Connector][^1] | 形式化等级: L3

## 1. 概念定义 (Definitions)

### Def-F-Conn-CDC-01: Change Data Capture
变更数据捕获：
$$
\text{CDC} : \text{DB Changes} \to \text{Stream}<\text{ChangeEvent}>
$$

### Def-F-Conn-CDC-02: Change Event
变更事件：
$$
\text{ChangeEvent} = \langle \text{Op}, \text{Before}, \text{After}, \text{Source} \rangle
$$

## 2. 属性推导 (Properties)

### Prop-F-Conn-CDC-01: Consistency Guarantee
一致性保证：
$$
\text{CDC} \implies \text{ExactlyOnce} \land \text{Ordering}
$$

## 3. 关系建立 (Relations)

### CDC演进

| 版本 | 特性 | 状态 |
|------|------|------|
| 2.3 | Debezium集成 | GA |
| 2.4 | 原生CDC | GA |
| 2.5 | 多源CDC | GA |
| 3.0 | 统一CDC框架 | 设计中 |

## 4. 论证过程 (Argumentation)

### 4.1 支持的数据库

| 数据库 | 捕获模式 | 状态 |
|--------|----------|------|
| MySQL | Binlog | GA |
| PostgreSQL | WAL | GA |
| Oracle | LogMiner | GA |
| MongoDB | Oplog | GA |
| SQL Server | CDC表 | Beta |

## 5. 形式证明 / 工程论证

### 5.1 MySQL CDC Source

```java
MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
    .hostname("mysql")
    .port(3306)
    .databaseList("inventory")
    .tableList("inventory.products")
    .username("flink")
    .password("flinkpwd")
    .deserializer(new JsonDebeziumDeserializationSchema())
    .build();
```

## 6. 实例验证 (Examples)

### 6.1 处理CDC事件

```java
stream.process(new ProcessFunction<String, Row>() {
    @Override
    public void processElement(String event, Context ctx, Collector<Row> out) {
        JsonObject json = JsonParser.parseString(event).getAsJsonObject();
        String op = json.get("op").getAsString();
        
        switch (op) {
            case "c": // CREATE
            case "r": // READ (snapshot)
                out.collect(parseAfter(json));
                break;
            case "u": // UPDATE
                out.collect(parseAfter(json));
                break;
            case "d": // DELETE
                out.collect(parseBefore(json));
                break;
        }
    }
});
```

## 7. 可视化 (Visualizations)

```mermaid
graph LR
    A[Database] --> B[CDC Capture]
    B --> C[Change Stream]
    C --> D[Flink处理]
    D --> E[Target]
```

## 8. 引用参考 (References)

[^1]: Flink CDC Connector Documentation

---

## 跟踪信息

| 属性 | 值 |
|------|-----|
| 版本 | 2.4-3.0 |
| 当前状态 | 演进中 |
