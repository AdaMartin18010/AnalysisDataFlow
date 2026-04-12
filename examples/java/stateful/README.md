# Flink Stateful 示例

## 项目简介

演示Flink三种核心状态类型：
- **ValueState**: 单值状态（计数器、累加器）
- **ListState**: 列表状态（最近N个元素）
- **MapState**: 映射状态（键值缓存）

## 应用场景

电商订单异常检测系统：
1. 统计用户下单次数 → ValueState
2. 记录用户累计消费 → ValueState  
3. 保存最近3笔订单 → ListState
4. 按商品统计购买次数 → MapState

## 快速开始

```bash
# 本地运行
mvn clean compile exec:java -Dexec.mainClass="com.example.flink.StatefulExample" -Plocal

# 打包
mvn clean package -Plocal
java -jar target/flink-stateful-1.0.0.jar
```

## 异常检测规则

| 规则 | 触发条件 | 使用状态 |
|-----|---------|---------|
| 高频下单 | 10分钟内≥5单 | ValueState(计数器) |
| 金额异常 | 累计消费>30000 | ValueState(累加器) |
| 重复购买 | 同一商品≥3次 | MapState |

## 输出示例

```
[状态更新] 用户=user_1, 订单数=1, 累计消费=5999, 最近订单=1
[状态更新] 用户=user_1, 订单数=2, 累计消费=7298, 最近订单=2
[状态更新] 用户=user_1, 订单数=3, 累计消费=12297, 最近订单=3
[状态更新] 用户=user_1, 订单数=4, 累计消费=15296, 最近订单=3
[状态更新] 用户=user_1, 订单数=5, 累计消费=36295, 最近订单=3

╔════════════════════════════════════════════════╗
║           ⚠️  异常购买行为告警                   ║
╠════════════════════════════════════════════════╣
║ 用户ID: user_1                                   ║
║ 告警原因: 短时间内高频下单(5次), 累计消费金额异常(36295元) ║
║ 订单总数: 5                                      ║
║ 累计消费: 36295                                  ║
║ 最近订单:                                        ║
║   - Order{user_1 buys watch for 2999}            ║
║   - Order{user_1 buys macbook for 12999}         ║
║   - Order{user_1 buys iphone for 5999}           ║
╚════════════════════════════════════════════════╝
```

## 状态后端配置

```java
// MemoryStateBackend - 开发测试
env.setStateBackend(new HashMapStateBackend()  // MemoryStateBackend已弃用，使用HashMapStateBackend
// ));

// FsStateBackend - 文件系统
env.setStateBackend(new FsStateBackend("file:///tmp/flink-state"));

// RocksDBStateBackend - 生产环境
env.setStateBackend(new EmbeddedRocksDBStateBackend());
```

## 状态TTL配置

```java

import org.apache.flink.streaming.api.windowing.time.Time;

StateTtlConfig ttlConfig = StateTtlConfig
    .newBuilder(Time.hours(24))
    .setUpdateType(StateTtlConfig.UpdateType.OnCreateAndWrite)
    .setStateVisibility(StateTtlConfig.StateVisibility.NeverReturnExpired)
    .build();
```
