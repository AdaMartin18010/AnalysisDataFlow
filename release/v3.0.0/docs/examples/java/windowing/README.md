# Flink Windowing 示例

## 项目简介

演示Flink三种核心窗口类型：

- **Tumbling Window** (滚动窗口): 固定大小，不重叠
- **Sliding Window** (滑动窗口): 固定大小，可重叠
- **Session Window** (会话窗口): 动态大小，由活动间隙决定

## 快速开始

### 本地运行

```bash
# 滚动窗口 (默认)
mvn clean compile exec:java -Dexec.mainClass="com.example.flink.WindowingExample" -Plocal

# 滑动窗口
mvn clean compile exec:java -Dexec.mainClass="com.example.flink.WindowingExample" -Plocal -Dexec.args="sliding"

# 会话窗口
mvn clean compile exec:java -Dexec.mainClass="com.example.flink.WindowingExample" -Plocal -Dexec.args="session"
```

### 打包运行

```bash
# 打包
mvn clean package -Plocal

# 运行不同窗口类型
java -jar target/flink-windowing-1.0.0.jar tumbling
java -jar target/flink-windowing-1.0.0.jar sliding
java -jar target/flink-windowing-1.0.0.jar session
```

## 窗口对比

| 窗口类型 | 特点 | 适用场景 |
|---------|------|---------|
| Tumbling | 固定大小，不重叠 | 定期统计、批量处理 |
| Sliding | 固定大小，可重叠 | 移动平均、趋势分析 |
| Session | 动态大小 | 用户行为分析、会话追踪 |

## 输出示例

### Tumbling Window

```
使用 TumblingWindow: 窗口大小=5秒
(sensor_1, 26.0)
(sensor_2, 30.5)
```

### Sliding Window

```
使用 SlidingWindow: 窗口大小=5秒, 滑动间隔=2秒
(sensor_1, 26.0)
(sensor_1, 26.67)
(sensor_2, 30.5)
```

### Session Window

```
使用 SessionWindow: 会话间隔=3秒
(sensor_1, 26.5)
(sensor_2, 30.17)
```
