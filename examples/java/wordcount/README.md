# Flink WordCount 示例

## 项目简介

这是一个完全可运行的 Apache Flink WordCount 示例项目，演示了流处理的基本概念：
- DataStream API
- 窗口操作
- 键控流（Keyed Stream）
- 状态计算

## 快速开始

### 前置要求

- JDK 11 或更高版本
- Apache Maven 3.6+
- (可选) Flink 集群 1.20+

### 本地运行

```bash
# 进入项目目录
cd examples/java/wordcount

# 编译并运行
mvn clean compile exec:java -Dexec.mainClass="com.example.flink.WordCount" -Plocal
```

### 打包为可执行JAR

```bash
# 打包
mvn clean package -Plocal

# 本地运行打包后的JAR
java -jar target/flink-wordcount-1.0.0.jar
```

### 从Socket读取数据

```bash
# 终端1：启动netcat
nc -lk 9999

# 终端2：运行WordCount
java -jar target/flink-wordcount-1.0.0.jar socket localhost 9999
```

### 提交到Flink集群

```bash
# 打包（不带依赖）
mvn clean package

# 提交到Flink集群
flink run target/flink-wordcount-1.0.0.jar
```

## 项目结构

```
wordcount/
├── pom.xml                    # Maven配置
├── README.md                  # 本文件
└── src/
    └── main/
        ├── java/com/example/flink/
        │   └── WordCount.java # 主程序
        └── resources/
            └── log4j2.properties
```

## 输出示例

```
=================================
WordCount程序已启动
=================================
(flink, 4)
(hello, 3)
(world, 2)
(is, 1)
(awesome, 1)
(stream, 1)
(processing, 1)
(with, 1)
(rocks, 1)
```

## 核心概念

1. **DataStream**: Flink流数据抽象
2. **FlatMap**: 一对多转换操作
3. **KeyBy**: 按key分区
4. **Window**: 时间窗口聚合
5. **Watermark**: 事件时间处理

## 自定义扩展

修改 `WordCount.java` 中的 `Tokenizer` 类来自定义分词逻辑：

```java
// 示例：只统计长度大于3的单词
if (word.length() > 3) {
    out.collect(new Tuple2<>(word, 1));
}
```

## 相关文档

- [Flink DataStream API](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/overview/)
- [Flink 窗口指南](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/windows/)
