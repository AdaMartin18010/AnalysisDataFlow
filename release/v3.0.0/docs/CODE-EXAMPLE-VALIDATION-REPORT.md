> **状态**: 🔮 前瞻内容 | **风险等级**: 高 | **最后更新**: 2026-04
> 
> 此文档描述的内容处于早期规划阶段，可能与最终实现不符。请以 Apache Flink 官方发布为准。
# 代码示例验证报告

> **生成时间**: 2026-04-08 15:34:55
> **验证器版本**: 1.0.0
> **项目根目录**: .

## 📊 验证统计

| 指标 | 数值 |
|------|------|
| 扫描文件数 | 1079 |
| 代码块总数 | 5433 |
| ✅ 验证通过 | 4071 |
| ❌ 验证失败 | 1362 |
| ⚠️  警告数 | 0 |
| 🔧 可自动修复 | 20 |
| **通过率** | 74.93% |

### 按语言统计

| 语言 | 总数 | 有效 | 无效 | 通过率 |
|------|------|------|------|--------|
| bash | 798 | 798 | 0 | 100.00% |
| java | 1867 | 819 | 1048 | 43.87% |
| json | 139 | 139 | 0 | 100.00% |
| python | 456 | 408 | 48 | 89.47% |
| sql | 1092 | 910 | 182 | 83.33% |
| xml | 83 | 83 | 0 | 100.00% |
| yaml | 998 | 914 | 84 | 91.58% |

## 🚨 问题代码清单

共发现 **1362** 个有问题的代码示例：


### `.improvement-tracking\freshness-template.md`

**问题 #5** (第 129 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 3


### `100-PERCENT-COMPLETION-MASTER-PLAN.md`

**问题 #2** (第 75 行, 语言: python)

- **错误**: SyntaxError: invalid character '，' (U+FF0C)
- **错误行**: 4


### `BEST-PRACTICES.md`

**问题 #14** (第 680 行, 语言: yaml)

- **错误**: while scanning a simple key
  in "<unicode string>", line 28, column 3:
      ---
      ^ (line: 28)
could not find expected ':'
  in "<unicode string>", line 29, column 3:
      apiVersion: autoscali
- **错误行**: 28


### `CASE-STUDIES.md`

**问题 #3** (第 263 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgl8r28f6TempValidation.java:4: 错误: 找不到符号
WatermarkStrategy<Transaction> strategy = WatermarkStrategy
^
  符号:   类 WatermarkStrategy
  位置: 类 TempValidation
C:\Users\
- **错误行**: 4

**问题 #7** (第 487 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqwc8qgjvTempValidation.java:4: 错误: 找不到符号
MapStateDescriptor<String, Rule> ruleStateDescriptor =
^
  符号:   类 MapStateDescriptor
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 4

**问题 #9** (第 602 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx1t2faa9TempValidation.java:4: 错误: 找不到符号
DataStream<UserFeature> userFeatureStream = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 4

**问题 #12** (第 719 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsqhjkdaeTempValidation.java:4: 错误: 找不到符号
DataStream<Order> preAggregated = orderStream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #13** (第 789 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp452umv8uTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #14** (第 799 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7zusu_dnTempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend rocksDb = new RocksDBStateBackend("hdfs://checkpoints");
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempV
- **错误行**: 4

**问题 #16** (第 884 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm_jaemjeThresholdMonitorFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<SensorData> processed = env
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #22** (第 1131 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeh08w2bzAntiCheatProcessFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<PlayerAction> actionStream = env
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #28** (第 1419 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcawhow47TempValidation.java:4: 错误: 找不到符号
DataStream<LogEvent> parsedLogs = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpc
- **错误行**: 4


### `CONFIG-TEMPLATES\development\ide-config-guide.md`

**问题 #3** (第 81 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpscscarimTempValidation.java:4: 错误: 非法的表达式开始
public static void main(String[] args) throws Exception {
^
C:\Users\luyan\AppData\Local\Temp\tmpscscarimTempValidation
- **错误行**: 4


### `CONFIG-TEMPLATES\production\ha-security-guide.md`

**问题 #2** (第 50 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 9, column 1:
    server.1=zookeeper-0:2888:3888
    ^ (line: 9)
- **错误行**: 9


### `CONFIG-TEMPLATES\scenarios\scenario-comparison.md`

**问题 #8** (第 197 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 9, column 1:
    env.getConfig().setExecutionBuff ...
    ^ (line: 9)
- **错误行**: 9


### `CONTRIBUTING.md`

**问题 #23** (第 857 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv25o9fihTempValidation.java:5: 错误: 找不到符号
WatermarkStrategy<Event> strategy = WatermarkStrategy
^
  符号:   类 WatermarkStrategy
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 5


### `DEPLOYMENT-ARCHITECTURES.md`

**问题 #5** (第 196 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsvg89j1fTempValidation.java:5: 错误: 需要';'
public void testPipeline() {
                        ^
1 个错误

- **错误行**: 5


### `FAQ.md`

**问题 #7** (第 388 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqz7umah3TempValidation.java:4: 错误: 找不到符号
AIAgentConfig config = AIAgentConfig.builder()
^
  符号:   类 AIAgentConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #9** (第 454 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyuhqqxi9TempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #11** (第 505 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9p594qhaTempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env =
        ^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3

**问题 #13** (第 571 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo7qqdbkvTempValidation.java:4: 错误: 找不到符号
SmartCheckpointMetrics metrics = checkpointConfig.getSmartMetrics();
^
  符号:   类 SmartCheckpointMetrics
  位置: 类 TempValida
- **错误行**: 4

**问题 #16** (第 712 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9b5519nnTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #17** (第 762 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps0ue23h8GPUDetectionFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
StreamExecutionEnvironment env =
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #24** (第 980 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1xdp6pulTempValidation.java:4: 错误: 非法的表达式开始
StreamTableEnvironment tableEnv = ...;
                                  ^
C:\Users\luyan\AppData\Local\Temp\tmp1xdp6pu
- **错误行**: 4

**问题 #25** (第 1012 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看已注册的 WASM UDF
SHOW FUNCTIONS WHERE TYPE = 'WA...; 可能的语法问题: -- 查看 UDF 详情
DESCRIBE FUNCTION STRING_LEN;...

**问题 #31** (第 1196 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt0pj08z2TempValidation.java:4: 错误: 找不到符号
env.setStateBackend(new RocksDBStateBackend("hdfs://checkpoints", true));
                        ^
  符号:   类 RocksDBState
- **错误行**: 4

**问题 #33** (第 1249 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplb8vdhkkTempValidation.java:4: 错误: 找不到符号
GPUResource resource = new GPUResource(1, 16);
^
  符号:   类 GPUResource
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 4

**问题 #34** (第 1279 行, 语言: sql)

- **错误**: 可能的语法问题: -- 2.4: 流批一体基础
SET EXECUTION.MODE = 'STREAMING';...; 可能的语法问题: -- 2.5: 新增自适应模式
SET EXECUTION.MODE = 'ADAPTIVE';  ...

**问题 #37** (第 1381 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg0roig2oTempValidation.java:5: 错误: 找不到符号
DataStream<Row> result = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpg0roig2oTe
- **错误行**: 5

**问题 #42** (第 1545 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb2b25bcjTempValidation.java:5: 错误: 找不到符号
env.enableCheckpointing(5000);  // 每5秒，无论负载
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpb
- **错误行**: 5

**问题 #45** (第 1643 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpik74gcyiTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #49** (第 1826 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_sqycwcnTempValidation.java:4: 错误: 找不到符号
AIAgentConfig config = AIAgentConfig.builder()
^
  符号:   类 AIAgentConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4


### `FLINK-IOT-GAP-ANALYSIS.md`

**问题 #1** (第 44 行, 语言: sql)

- **错误**: 可能的语法问题: -- 设备时间作为事件时间，而非KAFKA摄入时间
WATERMARK FOR DEVICE_TIM...

**问题 #7** (第 198 行, 语言: sql)

- **错误**: 可能的语法问题: WATERMARK FOR DEVICE_TIME AS DEVICE_TIME - INTERVA...


### `Flink-IoT-Authority-Alignment\Phase-1-Architecture\01-flink-iot-foundation-and-architecture.md`

**问题 #9** (第 685 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 95, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^ (line: 95)
- **错误行**: 95
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #11** (第 1069 行, 语言: yaml)

- **错误**: could not determine a constructor for the tag '!Ref'
  in "<unicode string>", line 296, column 12:
        Value: !Ref VPC
               ^ (line: 296)
- **错误行**: 296


### `Flink-IoT-Authority-Alignment\Phase-1-Architecture\03-flink-iot-time-semantics-and-disorder.md`

**问题 #1** (第 162 行, 语言: sql)

- **错误**: 可能的语法问题: -- STREAMKAP推荐的IOT WATERMARK配置
WATERMARK FOR DEVIC...

**问题 #6** (第 372 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6_y45q9fTempValidation.java:3: 错误: 找不到符号
        WatermarkStrategy<SensorEvent> strategy = WatermarkStrategy
        ^
  符号:   类 WatermarkStrategy
  位置: 类 TempVali
- **错误行**: 3

**问题 #7** (第 413 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3l5z2mhmTempValidation.java:4: 错误: 找不到符号
WatermarkStrategy.<SensorEvent>forBoundedOutOfOrderness(
                   ^
  符号:   类 SensorEvent
  位置: 类 TempValidation
- **错误行**: 4

**问题 #8** (第 444 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp67d1gboyTempValidation.java:4: 错误: 找不到符号
WatermarkStrategy.<SensorEvent>forBoundedOutOfOrderness(
                   ^
  符号:   类 SensorEvent
  位置: 类 TempValidation
- **错误行**: 4

**问题 #13** (第 570 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp42bf6zblTempValidation.java:4: 错误: 找不到符号
OutputTag<SensorEvent> lateDataTag = new OutputTag<SensorEvent>("late-data"){};
^
  符号:   类 OutputTag
  位置: 类 TempValidati
- **错误行**: 4

**问题 #28** (第 1342 行, 语言: sql)

- **错误**: 可能的语法问题: -- AWS IAM角色配置（通过FLINK配置传递）
-- FLINK-CONF.YAML:
--...

**问题 #32** (第 1452 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...


### `Flink-IoT-Authority-Alignment\Phase-1-Architecture\PHASE-1-COMPLETION-REPORT.md`

**问题 #3** (第 141 行, 语言: sql)

- **错误**: 可能的语法问题: WATERMARK FOR DEVICE_TIME AS DEVICE_TIME - INTERVA...


### `Flink-IoT-Authority-Alignment\Phase-10-Telecom\22-flink-iot-telecom-self-healing.md`

**问题 #3** (第 415 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptw65ebnwTempValidation.java:4: 错误: 找不到符号
DataSet<Vertex<String, Double>> rootCauseScores = faultGraph
^
  符号:   类 DataSet
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4


### `Flink-IoT-Authority-Alignment\Phase-13-Water-Management\25-flink-iot-smart-water-management.md`

**问题 #7** (第 529 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmrr11xq9TempValidation.java:4: 错误: 找不到符号
Pattern<WaterEvent, ?> leakPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4


### `Flink-IoT-Authority-Alignment\Phase-13-Water-Management\case-smart-water-complete.md`

**问题 #9** (第 1992 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 1

**问题 #11** (第 2076 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 30

**问题 #13** (第 2267 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 65


### `Flink-IoT-Authority-Alignment\Phase-2-Processing\04-flink-iot-hierarchical-downsampling.md`

**问题 #11** (第 452 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqyikz9ipTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
^
  符号:   类 StreamExecutionEnvironm
- **错误行**: 4


### `Flink-IoT-Authority-Alignment\Phase-2-Processing\05-flink-iot-alerting-and-monitoring.md`

**问题 #4** (第 196 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp503app12TempValidation.java:5: 错误: 找不到符号
                watermarkStrategy.getCurrentWatermark();
                ^
  符号:   变量 watermarkStrategy
  位置: 类 TempValida
- **错误行**: 5

**问题 #6** (第 232 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv0zgr8qwTempValidation.java:6: 错误: 不是语句
- numberOfFailedCheckpoints
^
C:\Users\luyan\AppData\Local\Temp\tmpv0zgr8qwTempValidation.java:6: 错误: 需要';'
- numberOfFaile
- **错误行**: 6

**问题 #10** (第 305 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2r6awtw8TempValidation.java:6: 错误: 不是语句
- watermarkLag
^
C:\Users\luyan\AppData\Local\Temp\tmp2r6awtw8TempValidation.java:6: 错误: 需要';'
- watermarkLag

- **错误行**: 6


### `Flink-IoT-Authority-Alignment\Phase-3-Deployment\06-flink-iot-cloud-native-deployment.md`

**问题 #8** (第 297 行, 语言: sql)

- **错误**: 可能的语法问题: -- 内存存储与磁性存储分层
MEMORY_RETENTION := 24 HOURS   -- 热...

**问题 #33** (第 3195 行, 语言: yaml)

- **错误**: while parsing a flow node
expected the node content, but found '-'
  in "<unicode string>", line 4, column 3:
    {{- define "flink-iot.deployment" -}}
      ^ (line: 4)
- **错误行**: 4


### `Flink-IoT-Authority-Alignment\Phase-3-Deployment\07-flink-iot-performance-tuning.md`

**问题 #6** (第 419 行, 语言: sql)

- **错误**: 可能的语法问题: -- ========================================
-- FLI...; 可能的语法问题: -- 2. CHECKPOINT配置（生产环境推荐）
SET 'EXECUTION.CHECKPOI...; 可能的语法问题: -- 3. 状态后端配置
SET 'STATE.BACKEND' = 'ROCKSDB';...; 可能的语法问题: -- 4

**问题 #8** (第 536 行, 语言: sql)

- **错误**: 可能的语法问题: -- ========================================
-- ROC...; 可能的语法问题: -- 1. 内存调优参数
SET 'STATE.BACKEND.ROCKSDB.MEMORY.MAN...; 可能的语法问题: -- 2. WRITEBUFFER配置
SET 'STATE.BACKEND.ROCKSDB.WRI...; 可能的语法问题:


### `Flink-IoT-Authority-Alignment\Phase-4-Case-Study\08-flink-iot-complete-case-study.md`

**问题 #17** (第 1649 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 103, column 39:
     ...   jobmanager.memory.process.size: 2048m
                                         ^ (line: 103)
- **错误行**: 103
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #24** (第 2258 行, 语言: sql)

- **错误**: 可能的语法问题: -- 1. 使用 MINIBATCH 优化聚合性能
SET TABLE.EXEC.MINI-BATC...; 可能的语法问题: -- 2. 启用 LOCAL-GLOBAL 聚合
SET TABLE.OPTIMIZER.AGG-P...; 可能的语法问题: -- 3. 使用 ROCKSDB 状态后端
SET STATE.BACKEND = 'ROCKSDB...; 可能的语法问题:


### `Flink-IoT-Authority-Alignment\Phase-4-Case-Study\09-flink-iot-pattern-catalog.md`

**问题 #2** (第 35 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwccqm5vrTempValidation.java:4: 错误: 找不到符号
DataStream<SensorData> filtered = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpw
- **错误行**: 4

**问题 #3** (第 50 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxl3d8j6sTempValidation.java:4: 错误: 找不到符号
ExecutionEnvironment batchEnv = ExecutionEnvironment.getExecutionEnvironment();
^
  符号:   类 ExecutionEnvironment
  位置: 类 T
- **错误行**: 4

**问题 #4** (第 63 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcjlm9z4fTempValidation.java:4: 错误: 找不到符号
DataStream<HourlyStats> realtimeStats = streamEnv
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #5** (第 75 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbmu_7b53TempValidation.java:4: 错误: 找不到符号
DataStream<SensorData> allData = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpbm
- **错误行**: 4

**问题 #6** (第 117 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5wwb30tbTempValidation.java:3: 错误: 找不到符号
        Properties mqttProps = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppD
- **错误行**: 3

**问题 #7** (第 135 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg9fsjhrfTempValidation.java:4: 错误: 找不到符号
List<String> topics = Arrays.asList(
^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpg9fsjhrf
- **错误行**: 4

**问题 #8** (第 169 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeetnh_tkTempValidation.java:4: 错误: 找不到符号
Properties prodMqttProps = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #9** (第 190 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptu7ctmehTempValidation.java:3: 错误: 找不到符号
        KafkaSource<SensorReading> kafkaSource = KafkaSource.<SensorReading>builder()
        ^
  符号:   类 KafkaSource
  位置
- **错误行**: 3

**问题 #10** (第 208 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk5ec6ns7TempValidation.java:3: 错误: 找不到符号
        KafkaSource<SensorReading> exactlyOnceSource = KafkaSource.<SensorReading>builder()
        ^
  符号:   类 KafkaSourc
- **错误行**: 3

**问题 #11** (第 228 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd0a9rg5vTempValidation.java:4: 错误: 找不到符号
DataStream<SensorReading> partitionedStream = kafkaStream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4

**问题 #12** (第 266 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmibxv9wnTempValidation.java:4: 错误: 找不到符号
DataStream<DeviceConfig> deviceConfigs = sensorStream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4

**问题 #14** (第 363 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpud2f2eskAverageAggregate.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<AvgTemperature> avgTemp = sensorStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 1

**问题 #15** (第 401 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7cbxoxroTempValidation.java:4: 错误: 找不到符号
DataStream<MovingAverage> movingAvg = sensorStream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 4

**问题 #16** (第 421 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp049z66fjSessionProcessFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<DeviceSession> sessions = sensorStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #17** (第 475 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp519bymxiTempValidation.java:4: 错误: 找不到符号
DataStream<EnrichedReading> enriched = tempStream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #19** (第 529 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg8zwtl83TempValidation.java:4: 错误: 找不到符号
DataStream<EnrichedEvent> enriched = eventStream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #20** (第 586 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3eqc9ohrTempValidation.java:4: 错误: 找不到符号
Pattern<SensorReading, ?> tempAnomalyPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #21** (第 644 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb1cdb2_eHeartbeatMonitor.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
Pattern<DeviceEvent, ?> offlinePattern = Pattern
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #22** (第 712 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw4gwh1vwTempValidation.java:4: 错误: 找不到符号
InfluxDBConfig influxConfig = InfluxDBConfig.builder()
^
  符号:   类 InfluxDBConfig
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #24** (第 785 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgc9vzt02TempValidation.java:10: 错误: 找不到符号
tableEnv.executeSql(createCatalog);
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpgc9
- **错误行**: 10

**问题 #25** (第 812 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3ot3qd_eTempValidation.java:4: 错误: 找不到符号
Map<String, String> hudiOptions = new HashMap<>();
^
  符号:   类 Map
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #26** (第 835 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx8hq_fqfTempValidation.java:4: 错误: 找不到符号
PinotSinkFunction<GenericRow> pinotSink = new PinotSinkFunction<>(
^
  符号:   类 PinotSinkFunction
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #30** (第 1009 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyy_gaqcsTempValidation.java:5: 错误: 需要';'
appender.json.type = RollingFile
                                ^
C:\Users\luyan\AppData\Local\Temp\tmpyy_gaqcsTempValida
- **错误行**: 5

**问题 #32** (第 1043 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9hbij6ikTracedFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
OpenTelemetry openTelemetry = OpenTelemetrySdk.builder()
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #43** (第 1363 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc8zmu74rTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpc8zmu74rTempV
- **错误行**: 4

**问题 #44** (第 1383 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd32nd5o6TempValidation.java:4: 错误: 找不到符号
DataStream<AggregatedResult> phase1 = dataStream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4


### `Flink-IoT-Authority-Alignment\Phase-7-Smart-Retail\case-smart-retail-complete.md`

**问题 #17** (第 3675 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 56

**问题 #18** (第 3929 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 30

**问题 #19** (第 4173 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 35

**问题 #20** (第 4377 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 38

**问题 #39** (第 6123 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeuwxl8h7TempValidation.java:4: 错误: 找不到符号
StateTtlConfig ttlConfig = StateTtlConfig
^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4


### `Flink-IoT-Authority-Alignment\Phase-8-Wearables\case-wearables-health-complete.md`

**问题 #28** (第 2808 行, 语言: sql)

- **错误**: 可能的语法问题: AND AVG(GLUCOSE_MGDL) > 200;...

**问题 #41** (第 3807 行, 语言: sql)

- **错误**: 可能的语法问题: -- 3小时和6小时预测（类似逻辑，使用更长历史数据）
-- 此处省略类似代码......

**问题 #54** (第 4863 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 32

**问题 #55** (第 5202 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 34

**问题 #56** (第 5432 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 34

**问题 #57** (第 5725 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 44

**问题 #58** (第 6037 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 40


### `Flink\00-FLINK-TECH-STACK-DEPENDENCY.md`

**问题 #8** (第 365 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjllu5xv4TempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #9** (第 386 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfi2itswaTempValidation.java:4: 错误: 找不到符号
TableEnvironment tableEnv = TableEnvironment.create(
^
  符号:   类 TableEnvironment
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #11** (第 420 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb6rj06v_TempValidation.java:7: 错误: 找不到符号
FlinkKafkaConsumer<Event> source = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\User
- **错误行**: 7


### `Flink\00-meta\00-QUICK-START.md`

**问题 #10** (第 323 行, 语言: sql)

- **错误**: 可能的语法问题: -- 步骤 1：注册 MCP 工具
-- 注: 以下为未来可能的语法（概念设计），尚未正式实现
<!...; 可能的语法问题: -- 步骤 2：创建 AI AGENT（未来可能的语法，概念设计阶段）
<!-- 以下语法为概念设计...

**问题 #11** (第 374 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnio5etiiTempValidation.java:4: 错误: 找不到符号
Agent agent = Agent.builder()
^
  符号:   类 Agent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpnio5etiiTempVa
- **错误行**: 4

**问题 #17** (第 566 行, 语言: sql)
- **错误**: 可能的语法问题: USE CATALOG PAIMON_CATALOG;...

**问题 #18** (第 611 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq3ma6tvyTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #19** (第 631 行, 语言: sql)
- **错误**: 可能的语法问题: -- 配置自适应执行
SET EXECUTION.RUNTIME-MODE = ADAPTIVE;...

**问题 #22** (第 720 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpysavvzn8TempValidation.java:4: 错误: 非法的表达式开始
DataStream<Transaction> transactions = ...;
                                       ^
1 个错误

- **错误行**: 4

**问题 #25** (第 801 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc4zqqu4tTempValidation.java:4: 错误: 找不到符号
TableEnvironment tEnv = TableEnvironment.create(
^
  符号:   类 TableEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4


### `Flink\01-concepts\datastream-v2-semantics.md`

**问题 #12** (第 332 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6pl18exaBadV1Function.java:2: 错误: 找不到符号
class BadV1Function extends ProcessFunction<Event, Result> {
                            ^
  符号: 类 ProcessFunction
C:\Users
- **错误行**: 2

**问题 #16** (第 446 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2a0h5uahAsyncAggregator.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
KafkaSource<Event> source = KafkaSource.<Event>builder()
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan
- **错误行**: 2

**问题 #17** (第 486 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqnns1plyDeduplicateFunction.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
RecordAttributes attrs = RecordAttributes.builder()
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 1


### `Flink\01-concepts\disaggregated-state-analysis.md`

**问题 #3** (第 365 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwdmlckteTempValidation.java:3: 错误: 找不到符号
        DisaggregatedStateBackend stateBackend = new DisaggregatedStateBackend(
        ^
  符号:   类 DisaggregatedStateBack
- **错误行**: 3

**问题 #4** (第 394 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiwp29sq6TempValidation.java:10: 错误: 需要';'
    .build()
            ^
1 个错误

- **错误行**: 10


### `Flink\01-concepts\flink-1.x-vs-2.0-comparison.md`

**问题 #7** (第 249 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdqe2gx4cTempValidation.java:4: 错误: 找不到符号
CountState current = state.value();  // 阻塞调用
^
  符号:   类 CountState
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #8** (第 260 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp011y10_6TempValidation.java:4: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp011y10_6Te
- **错误行**: 4

**问题 #13** (第 370 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo3qrdh2qTempValidation.java:3: 错误: 非法的表达式开始
public void processElement(Event event, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpo3qrdh2qTempValidation.ja
- **错误行**: 3

**问题 #14** (第 381 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl0poja0vTempValidation.java:3: 错误: 非法的表达式开始
public void processElement(Event event, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpl0poja0vTempValidation.ja
- **错误行**: 3


### `Flink\01-concepts\flink-architecture-evolution-1x-to-2x.md`

**问题 #1** (第 250 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6__sxkjrTempValidation.java:4: 错误: 找不到符号
   state.getAsync(key)
                  ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp6__s
- **错误行**: 4


### `Flink\02-core\adaptive-execution-engine-v2.md`

**问题 #11** (第 673 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx0p5ryj7SkewResistantAggregate.java:41: 错误: 需要 class、interface、enum 或 record
dataStream
^
1 个错误

- **错误行**: 41

**问题 #19** (第 1137 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptakw_azjTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #20** (第 1180 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz25oyt_vTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4


### `Flink\02-core\async-execution-model.md`

**问题 #7** (第 434 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7o5mek2hOrderedCallback.java:8: 错误: 未命名类 是预览功能，默认情况下禁用。
PriorityQueue<OrderedCallback> callbackQueue =
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 8

**问题 #9** (第 486 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdyenbuucTempValidation.java:4: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpdyenbuucTe
- **错误行**: 4

**问题 #10** (第 504 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_zsyovqfTempValidation.java:4: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp_zsyovqfTe
- **错误行**: 4

**问题 #15** (第 721 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph_wyj_34TempValidation.java:3: 错误: 非法的表达式开始
public void processElement(Event event, Context ctx, ResultFuture<Result> resultFuture) {
^
C:\Users\luyan\AppData\Loca
- **错误行**: 3

**问题 #16** (第 760 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcqzq69k3TempValidation.java:3: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpcqzq69k3Te
- **错误行**: 3

**问题 #17** (第 774 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpolnaor7yTempValidation.java:3: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpolnaor7yTe
- **错误行**: 3

**问题 #24** (第 1171 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu5w_fflgAECCallbackProcessor.java:4: 错误: 找不到符号
    void onStateAccessComplete(Key key, long sequence, Result result) {
                               ^
  符号:   类 K
- **错误行**: 4


### `Flink\02-core\checkpoint-mechanism-deep-dive.md`

**问题 #1** (第 179 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpedb4g5b9StateBackend.java:3: 错误: 需要<标识符>
    createKeyedStateBackend(env, stateHandles): AbstractKeyedStateBackend<K>
                           ^
C:\Users\luyan\A
- **错误行**: 3

**问题 #5** (第 542 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp54d2nrtiTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend = new EmbeddedRocksDBStateBackend(true);
^
  符号:   类 EmbeddedRocksDBStateBacken
- **错误行**: 4

**问题 #8** (第 709 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptm9dyvjyTempValidation.java:4: 错误: 非法的表达式开始
public boolean restoreSavepoint(
^
C:\Users\luyan\AppData\Local\Temp\tmptm9dyvjyTempValidation.java:76: 错误: 需要 class、in
- **错误行**: 4

**问题 #10** (第 886 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphnt8tk73TempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        ^
  符号:   类 StreamE
- **错误行**: 3

**问题 #11** (第 916 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkspqlzksTempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        ^
  符号:   类 StreamE
- **错误行**: 3

**问题 #12** (第 940 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprgdmuld5TempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        ^
  符号:   类 StreamE
- **错误行**: 3

**问题 #13** (第 958 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnqpvlpivTempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        ^
  符号:   类 StreamE
- **错误行**: 3


### `Flink\02-core\delta-join-production-guide.md`

**问题 #1** (第 53 行, 语言: sql)
- **错误**: 可能的语法问题: -- MYSQL CDC 源：忽略 DELETE 操作
'DEBEZIUM.SKIPPED.OPER...

**问题 #11** (第 693 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcp6lj0t8TempValidation.java:7: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 7

**问题 #22** (第 1268 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprdf9niqkTempValidation.java:4: 错误: 找不到符号
if (errorRate > 0.05 || avgLatency > 1000) {
    ^
  符号:   变量 errorRate
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #23** (第 1279 行, 语言: sql)
- **错误**: 可能的语法问题: -- 步骤1: 禁用 DELTA JOIN 优化
SET TABLE.OPTIMIZER.DELTA...; 可能的语法问题: -- 步骤2: 增加 REGULAR JOIN 状态 TTL
SET TABLE.EXEC.STAT...; 可能的语法问题: -- 步骤3: 优化 CHECKPOINT 配置
SET EXECUTION.CHECKPOINTI...; 可能的语法问题:

**问题 #24** (第 1322 行, 语言: sql)
- **错误**: 可能的语法问题: 'DEBEZIUM.SKIPPED.OPERATIONS' = 'D',  -- 必须
'DEBEZ...

**问题 #25** (第 1329 行, 语言: sql)
- **错误**: 可能的语法问题: 'LOOKUP.ASYNC' = 'TRUE',
'LOOKUP.CACHE.MAX-ROWS' =...

**问题 #26** (第 1337 行, 语言: sql)
- **错误**: 可能的语法问题: 'LOOKUP.CACHE.MAX-ROWS' = '200000',
'LOOKUP.CACHE....


### `Flink\02-core\delta-join.md`

**问题 #3** (第 244 行, 语言: sql)
- **错误**: 可能的语法问题: -- FLINK SQL开启DELTA JOIN优化
SET TABLE.OPTIMIZER.MUL...

**问题 #4** (第 317 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpme35vpvsAsyncUserProfileLookup.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<UserEvent> userEvents = env.fromSource(
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luya
- **错误行**: 2

**问题 #9** (第 535 行, 语言: sql)
- **错误**: 可能的语法问题: -- 优化后：投影下推，仅查询必要字段
-- 外部查询变为：SELECT USER_ID, AGE,...


### `Flink\02-core\exactly-once-end-to-end.md`

**问题 #2** (第 139 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr4f06jltTempValidation.java:3: 错误: 找不到符号
        Properties properties = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 3

**问题 #6** (第 304 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy1cdq01yTempValidation.java:3: 错误: 找不到符号
        Properties properties = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 3

**问题 #7** (第 322 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3r3mgrjdTempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #10** (第 398 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplowg4pltTempValidation.java:3: 错误: 找不到符号
JdbcXaSinkFunction<Row> xaSink = new JdbcXaSinkFunction<>(
^
  符号:   类 JdbcXaSinkFunction
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #11** (第 439 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8xht7tt3TempValidation.java:4: 错误: 需要';'
protected void preCommit(String pendingFile) throws Exception {
                        ^
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #16** (第 597 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoezf9nt_TempValidation.java:3: 错误: 需要';'
KafkaSource<String> createKafkaSource(String bootstrapServers, String topic, String groupId) {

- **错误行**: 3

**问题 #17** (第 617 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa9n3gqsdTempValidation.java:3: 错误: 需要';'
KafkaSink<String> createKafkaSink(String bootstrapServers, String topic, String transactionalIdPrefix) {

- **错误行**: 3

**问题 #21** (第 808 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkmi2u840TempValidation.java:9: 错误: 非法的表达式开始
    protected abstract TXN beginTransaction() throws Exception;
    ^
C:\Users\luyan\AppData\Local\Temp\tmpkmi2u840Temp
- **错误行**: 9

**问题 #23** (第 878 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphmt92sexTempValidation.java:7: 错误: 需要';'
    public void snapshotState(FunctionSnapshotContext context) throws Exception {
                             ^
C:\Users\
- **错误行**: 7

**问题 #24** (第 912 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuramykejTempValidation.java:7: 错误: 需要';'
    public void notifyCheckpointComplete(long checkpointId) throws Exception {
                                        ^
C
- **错误行**: 7

**问题 #28** (第 1176 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8wjkn0izTempValidation.java:7: 错误: 需要';'
    public void initializeState(FunctionInitializationContext context) throws Exception {
                               ^
- **错误行**: 7


### `Flink\02-core\exactly-once-semantics-deep-dive.md`

**问题 #4** (第 239 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy8ncwk77TempValidation.java:4: 错误: 找不到符号
properties.setProperty("enable.auto.commit", "false");
^
  符号:   变量 properties
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #5** (第 267 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpygcfm638TempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #6** (第 283 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6w28yzprTempValidation.java:4: 错误: 找不到符号
String transactionalIdPrefix = jobId + "-" + operatorId;
                               ^
  符号:   变量 jobId
  位置: 类 TempVal
- **错误行**: 4

**问题 #7** (第 308 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1f8gqlteTempValidation.java:3: 错误: 找不到符号
        env.enableCheckpointing(60000); // 60秒
        ^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 3

**问题 #8** (第 343 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeo5z1wrkTempValidation.java:3: 错误: 找不到符号
        Properties consumerProps = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 3

**问题 #15** (第 898 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpazysr2_8TempValidation.java:4: 错误: 找不到符号
env.getCheckpointConfig().enableUnalignedCheckpoints(true);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4

**问题 #21** (第 1206 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaaa_ihycTempValidation.java:6: 错误: 非法的表达式开始
    private void onCheckpointTimeout(long checkpointId) {
    ^
C:\Users\luyan\AppData\Local\Temp\tmpaaa_ihycTempValida
- **错误行**: 6


### `Flink\02-core\flink-2.0-forst-state-backend.md`

**问题 #5** (第 368 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6ouc75p6TempValidation.java:4: 错误: 找不到符号
StateDescriptor<V> descriptor = StateDescriptor
^
  符号:   类 StateDescriptor
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 4


### `Flink\02-core\flink-2.2-frontier-features.md`

**问题 #8** (第 709 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdir8soenTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
^
  符号:   类 StreamExecutionEnvironm
- **错误行**: 4

**问题 #9** (第 728 行, 语言: sql)
- **错误**: 可能的语法问题: -- 3. 创建嵌入模型（使用 ML_PREDICT）
<!-- 以下语法为概念设计，实际 FLIN...

**问题 #10** (第 830 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptxe0rit8TempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
^
  符号:   类 StreamExecutionEnvironm
- **错误行**: 4

**问题 #11** (第 855 行, 语言: sql)
- **错误**: 可能的语法问题: -- 4. 查看物化表
SHOW MATERIALIZED TABLES;...

**问题 #13** (第 1029 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjetvs91pTempValidation.java:8: 错误: 非法的表达式开始
import org.apache.flink.api.connector.source.SourceReaderContext;
^
C:\Users\luyan\AppData\Local\Temp\tmpjetvs91pTempVa
- **错误行**: 8

**问题 #15** (第 1096 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuexs36t2TempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
^
  符号:   类 StreamExecutionEnvironm
- **错误行**: 4

**问题 #16** (第 1110 行, 语言: sql)
- **错误**: 可能的语法问题: -- SQL CLIENT 配置
SET 'CLUSTER.SCHEDULING.STRATEGY'...


### `Flink\02-core\flink-state-management-complete-guide.md`

**问题 #6** (第 484 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr2qi6ddtTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);  // 60秒间隔
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpr2q
- **错误行**: 4

**问题 #18** (第 1261 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzttjk8zzTempValidation.java:9: 错误: 不是语句
taskmanager.memory.framework.heap.size: 512mb
                                 ^
C:\Users\luyan\AppData\Local\Temp\tmpzttjk
- **错误行**: 9

**问题 #19** (第 1275 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv90im6tiTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDb = new EmbeddedRocksDBStateBackend(true);
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置:
- **错误行**: 4

**问题 #21** (第 1307 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuhitnm41TempValidation.java:4: 错误: 找不到符号
ValueStateDescriptor<Long> descriptor = new ValueStateDescriptor<>(
^
  符号:   类 ValueStateDescriptor
  位置: 类 TempValidatio
- **错误行**: 4

**问题 #22** (第 1327 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmple2f0sanTempValidation.java:5: 错误: 找不到符号
for (String key : keys) {
                  ^
  符号:   变量 keys
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 5

**问题 #23** (第 1339 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbn5d3x8zTempValidation.java:4: 错误: 找不到符号
if (listSize > MAX_LIST_SIZE) {
    ^
  符号:   变量 listSize
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpbn5d
- **错误行**: 4

**问题 #24** (第 1358 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprj1i0nyzTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmprj1i0nyzTempV
- **错误行**: 4

**问题 #25** (第 1377 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8s9p46nzTempValidation.java:4: 错误: 找不到符号
env.getCheckpointConfig().enableUnalignedCheckpoints();
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #26** (第 1397 行, 语言: sql)
- **错误**: 可能的语法问题: -- 设置全局 STATE TTL
SET 'SQL.STATE-TTL' = '1 DAY';...

**问题 #27** (第 1428 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0z5_2mmuTempValidation.java:4: 错误: 找不到符号
Time windowSize = Time.hours(1);
^
  符号:   类 Time
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp0z5_2mmuTemp
- **错误行**: 4

**问题 #29** (第 1484 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph9x32_erTempValidation.java:5: 错误: 需要';'
public void open(Configuration parameters) {
                ^
C:\Users\luyan\AppData\Local\Temp\tmph9x32_erTempValidation
- **错误行**: 5

**问题 #30** (第 1501 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptca5s7jwTempValidation.java:4: 错误: 找不到符号
StateTtlConfig ttlConfig = StateTtlConfig
^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #31** (第 1520 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd2ik2_axTempValidation.java:4: 错误: 非法的表达式开始
private transient long lastAccessTime;
^
C:\Users\luyan\AppData\Local\Temp\tmpd2ik2_axTempValidation.java:25: 错误: 需要 cl
- **错误行**: 4

**问题 #32** (第 1558 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_tsw0y5_TempValidation.java:7: 错误: 非法的表达式开始
public static void configureChangelogBackend(StreamExecutionEnvironment env) {
^
C:\Users\luyan\AppData\Local\Temp\tmp_
- **错误行**: 7

**问题 #33** (第 1605 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplw1ydx3fUserState.java:14: 错误: 需要 class、interface、enum 或 record
env.getConfig().registerTypeWithKryoSerializer(UserState.class, new CompatibleSerializer());
^
C:\U
- **错误行**: 14


### `Flink\02-core\flink-state-ttl-best-practices.md`

**问题 #4** (第 224 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppm3_6_kfTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.StateTtlConfig;
        ^
C:\Users\luyan\AppData\Local\Temp\tmppm3_6_k
- **错误行**: 3

**问题 #5** (第 243 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbce3gh40TempValidation.java:4: 错误: 找不到符号
StateTtlConfig incrementalCleanup = StateTtlConfig
^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #6** (第 263 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy6m0724gTempValidation.java:4: 错误: 找不到符号
StateTtlConfig rocksdbCleanup = StateTtlConfig
^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 4

**问题 #8** (第 319 行, 语言: sql)
- **错误**: 可能的语法问题: -- 设置全局 STATE TTL
SET 'SQL.STATE-TTL' = '1 DAY';...

**问题 #9** (第 344 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpveptwa6kTempValidation.java:7: 错误: 非法的表达式开始
public StateTtlConfig createSessionTtlConfig() {
^
C:\Users\luyan\AppData\Local\Temp\tmpveptwa6kTempValidation.java:17:
- **错误行**: 7

**问题 #10** (第 361 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpots5ila9TempValidation.java:7: 错误: 非法的表达式开始
public StateTtlConfig createAggregationTtlConfig() {
^
C:\Users\luyan\AppData\Local\Temp\tmpots5ila9TempValidation.java
- **错误行**: 7

**问题 #21** (第 863 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcmxpwlu9TempValidation.java:5: 错误: 找不到符号
    (Gauge<Long>) () -> {
     ^
  符号:   类 Gauge
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpcmxpwlu9TempV
- **错误行**: 5

**问题 #22** (第 880 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyncxhox3TempValidation.java:5: 错误: 需要';'
public void open(Configuration parameters) {
                ^
C:\Users\luyan\AppData\Local\Temp\tmpyncxhox3TempValidation
- **错误行**: 5

**问题 #24** (第 897 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptjz1fe1dTempValidation.java:3: 错误: 非法的表达式开始
        .cleanupIncrementally(
        ^
C:\Users\luyan\AppData\Local\Temp\tmptjz1fe1dTempValidation.java:6: 错误: 需要';'

- **错误行**: 3

**问题 #25** (第 906 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1l0pgjk2TempValidation.java:3: 错误: 找不到符号
        env.setStateBackend(new EmbeddedRocksDBStateBackend());
                                ^
  符号:   类 EmbeddedRocksD
- **错误行**: 3

**问题 #26** (第 925 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqvwhyz4lTempValidation.java:3: 错误: 找不到符号
        DefaultConfigurableOptionsFactory factory = new DefaultConfigurableOptionsFactory();
        ^
  符号:   类 DefaultCo
- **错误行**: 3


### `Flink\02-core\forst-state-backend.md`

**问题 #6** (第 456 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdgzyeo7sTempValidation.java:3: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 3


### `Flink\02-core\multi-way-join-optimization.md`

**问题 #10** (第 354 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpknxpky29TempValidation.java:4: 错误: 找不到符号
DataStream<Result> result = orders
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpknxp
- **错误行**: 4

**问题 #11** (第 385 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7ficfdi8TempValidation.java:4: 错误: 找不到符号
DataStream<UnifiedResult> result =
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp7fic
- **错误行**: 4


### `Flink\02-core\network-stack-evolution.md`

**问题 #9** (第 526 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqh1bv3wrTempValidation.java:8: 错误: 不是语句
taskmanager.network.memory.buffer-debloat.enabled: true
                                 ^
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 8


### `Flink\02-core\smart-checkpointing-strategies.md`

**问题 #20** (第 1201 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpimpq1_0vTempValidation.java:5: 错误: 非法字符: '#'
# ============================================================
^
C:\Users\luyan\AppData\Local\Temp\tmpimpq1_0vTempVali
- **错误行**: 5

**问题 #21** (第 1231 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg9zyzp6mTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
^
  符号:   类 StreamExecutionEnvironm
- **错误行**: 4

**问题 #22** (第 1255 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgepq9ps6TempValidation.java:5: 错误: 非法字符: '#'
# ============================================================
^
C:\Users\luyan\AppData\Local\Temp\tmpgepq9ps6TempVali
- **错误行**: 5

**问题 #23** (第 1284 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1y717_u0TempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend rocksDbBackend = new RocksDBStateBackend(
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempValidation
C:\Us
- **错误行**: 4

**问题 #24** (第 1309 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe3207wbcTempValidation.java:5: 错误: 非法字符: '#'
# ============================================================
^
C:\Users\luyan\AppData\Local\Temp\tmpe3207wbcTempVali
- **错误行**: 5

**问题 #25** (第 1335 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiqj4qep4TempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
^
  符号:   类 StreamExecutionEnvironm
- **错误行**: 4

**问题 #26** (第 1365 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_yguerhlTempValidation.java:5: 错误: 非法字符: '#'
# ============================================================
^
C:\Users\luyan\AppData\Local\Temp\tmp_yguerhlTempVali
- **错误行**: 5

**问题 #27** (第 1391 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwhuj8cvxTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
^
  符号:   类 StreamExecutionEnvironm
- **错误行**: 4


### `Flink\02-core\state-backend-evolution-analysis.md`

**问题 #2** (第 277 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp80gop6t5TempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #3** (第 298 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_sp_8lswTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #5** (第 356 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvav33976TempValidation.java:4: 错误: 找不到符号
ForStStateBackend forstBackend = new ForStStateBackend();
^
  符号:   类 ForStStateBackend
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #7** (第 414 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2emybr70EmbeddedRocksDBStateBackend.java:37: 错误: 非法的表达式开始
        );
        ^
1 个错误

- **错误行**: 37

**问题 #8** (第 467 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp84v5097fForStStateBackend.java:46: 错误: 非法的表达式开始
        );
        ^
1 个错误

- **错误行**: 46


### `Flink\02-core\state-backends-deep-comparison.md`

**问题 #3** (第 529 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnn2vbj_vTempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env =
        ^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3

**问题 #5** (第 562 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgw2kmmhvTempValidation.java:5: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 5

**问题 #6** (第 612 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph32zgoo4TempValidation.java:5: 错误: 找不到符号
ForStStateBackend forstBackend = new ForStStateBackend();
^
  符号:   类 ForStStateBackend
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 5


### `Flink\02-core\streaming-etl-best-practices.md`

**问题 #5** (第 513 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw9zhkwe6TempValidation.java:4: 错误: 找不到符号
MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
^
  符号:   类 MySqlSource
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #7** (第 555 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuntfckfcTempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<Event> source = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\User
- **错误行**: 4

**问题 #8** (第 587 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm4c3_w__TempValidation.java:4: 错误: 找不到符号
JdbcInputFormat jdbcInput = JdbcInputFormat.buildJdbcInputFormat()
^
  符号:   类 JdbcInputFormat
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #11** (第 735 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_tb6o1uuTempValidation.java:4: 错误: 找不到符号
DataStream<Result> result = stream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp_tb6
- **错误行**: 4

**问题 #12** (第 795 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3svyqko5TempValidation.java:10: 错误: 找不到符号
    .process(new ProcessJoinFunction<Order, Payment, EnrichedOrder>() {
                 ^
  符号:   类 ProcessJoinFunction

- **错误行**: 10

**问题 #14** (第 833 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi21tltv7AsyncDatabaseRequest.java:40: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedEvent> enriched = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以启用 未命名
- **错误行**: 40

**问题 #15** (第 905 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnt2jkxjxTempValidation.java:18: 错误: 不是语句
"INSERT INTO table (id, value) VALUES (?, ?) " +
^
C:\Users\luyan\AppData\Local\Temp\tmpnt2jkxjxTempValidation.java:19: 错误
- **错误行**: 18

**问题 #17** (第 981 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1l0u20ieTempValidation.java:4: 错误: 找不到符号
StreamingFileSink<Record> sink = StreamingFileSink
^
  符号:   类 StreamingFileSink
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4

**问题 #22** (第 1153 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl0pzv0y2TempValidation.java:4: 错误: 找不到符号
AvroDeserializationSchema<Order> schema = AvroDeserializationSchema
^
  符号:   类 AvroDeserializationSchema
  位置: 类 TempVali
- **错误行**: 4

**问题 #25** (第 1282 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprcm34447TempValidation.java:4: 错误: 找不到符号
env.getConfig().setAutoWatermarkInterval(200L);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #26** (第 1307 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuowxhnduTempValidation.java:3: 错误: 找不到符号
        StateTtlConfig ttlConfig = StateTtlConfig
        ^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 3

**问题 #27** (第 1333 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw0w6nyssTempValidation.java:4: 错误: 找不到符号
SpecificAvroSerde<Order> serde = new SpecificAvroSerde<>();
^
  符号:   类 SpecificAvroSerde
  位置: 类 TempValidation
C:\Users\
- **错误行**: 4

**问题 #31** (第 1415 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoeg69eobTempValidation.java:4: 错误: 找不到符号
OutputTag<FailedRecord> dlqTag = new OutputTag<FailedRecord>("dlq"){};
^
  符号:   类 OutputTag
  位置: 类 TempValidation
C:\Use
- **错误行**: 4


### `Flink\02-core\time-semantics-and-watermark.md`

**问题 #1** (第 284 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpybxxkl5hTempValidation.java:3: 错误: 非法的表达式开始
        .window(TumblingEventTimeWindows.of(Time.minutes(1)))
        ^
C:\Users\luyan\AppData\Local\Temp\tmpybxxkl5hTe
- **错误行**: 3

**问题 #2** (第 291 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdt_7l1mgTempValidation.java:3: 错误: 非法的表达式开始
        .window(TumblingEventTimeWindows.of(Time.minutes(1)))
        ^
C:\Users\luyan\AppData\Local\Temp\tmpdt_7l1mgTe
- **错误行**: 3

**问题 #3** (第 298 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5ezi8mvrTempValidation.java:4: 错误: 非法的表达式开始
.window(TumblingEventTimeWindows.of(Time.minutes(1)))
^
C:\Users\luyan\AppData\Local\Temp\tmp5ezi8mvrTempValidation.jav
- **错误行**: 4

**问题 #6** (第 522 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp18krz7yhTempValidation.java:3: 错误: 找不到符号
        DataStream<Event> stream = env.fromSource(kafkaSource,
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Us
- **错误行**: 3

**问题 #7** (第 531 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphv00pd_gTempValidation.java:3: 错误: 找不到符号
        DataStream<Transaction> stream = env.fromSource(kafkaSource,
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
- **错误行**: 3

**问题 #8** (第 544 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcjf22y8xTempValidation.java:5: 错误: 找不到符号
    .aggregate(new CountAggregate());
                   ^
  符号:   类 CountAggregate
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 5

**问题 #9** (第 552 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4vc335j8TempValidation.java:5: 错误: 找不到符号
    .aggregate(new AverageAggregate());
                   ^
  符号:   类 AverageAggregate
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 5

**问题 #10** (第 560 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqbz386fzTempValidation.java:6: 错误: 找不到符号
    .aggregate(new SessionAggregate());
                   ^
  符号:   类 SessionAggregate
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 6

**问题 #11** (第 571 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf3z6gc3cTempValidation.java:3: 错误: 找不到符号
        OutputTag<Event> lateDataTag = new OutputTag<Event>("late-data"){};
        ^
  符号:   类 OutputTag
  位置: 类 TempVali
- **错误行**: 3


### `Flink\03-api\03.02-table-sql-api\ansi-sql-2023-compliance-guide.md`

**问题 #1** (第 102 行, 语言: sql)
- **错误**: 可能的语法问题: MATCH_RECOGNIZE (
    PARTITION BY PARTITION_KEY  ...

**问题 #5** (第 369 行, 语言: sql)
- **错误**: 可能的语法问题: JSON_VALUE(JSON_FIELD, '$.PATH'
    RETURNING VARC...

**问题 #6** (第 390 行, 语言: sql)
- **错误**: 可能的语法问题: JSON_TABLE(
    JSON_DATA,
    '$.ITEMS[*]'
    CO...

**问题 #8** (第 499 行, 语言: sql)
- **错误**: 可能的语法问题: -- 执行结果示例
-- {"ORDER_ID":1001,"CUSTOMER":"ALICE","...

**问题 #13** (第 603 行, 语言: sql)
- **错误**: 可能的语法问题: -- 输出: 每5分钟累积一次，每小时重置
-- [00:00, 00:05), [00:00, 0...

**问题 #24** (第 1055 行, 语言: sql)
- **错误**: 可能的语法问题: -- ============================================
--...


### `Flink\03-api\03.02-table-sql-api\data-types-complete-reference.md`

**问题 #2** (第 107 行, 语言: sql)
- **错误**: 可能的语法问题: STRING          -- 无限制长度
STRING(100)     -- 限制最大长度...

**问题 #3** (第 123 行, 语言: sql)
- **错误**: 可能的语法问题: VARCHAR         -- 同STRING，无限制
VARCHAR(N)      -- ...

**问题 #4** (第 138 行, 语言: sql)
- **错误**: 可能的语法问题: CHAR(N)         -- 固定N字符...

**问题 #5** (第 164 行, 语言: sql)
- **错误**: 可能的语法问题: DECIMAL(10, 2)   -- 8位整数 + 2位小数，如12345678.90
DECIM...

**问题 #6** (第 187 行, 语言: sql)
- **错误**: 可能的语法问题: BOOLEAN    -- TRUE / FALSE / NULL...

**问题 #7** (第 217 行, 语言: sql)
- **错误**: 可能的语法问题: -- 声明
ARRAY<INT>
ARRAY<STRING>
ARRAY<ROW<ID INT, N...

**问题 #8** (第 242 行, 语言: sql)
- **错误**: 可能的语法问题: -- 声明
MAP<STRING, INT>
MAP<STRING, ROW<...>>

-- 构...

**问题 #9** (第 264 行, 语言: sql)
- **错误**: 可能的语法问题: -- 声明
ROW<ID INT, NAME STRING, AGE INT>

-- 构造
ROW...

**问题 #10** (第 298 行, 语言: sql)
- **错误**: 可能的语法问题: DATE
DATE '2024-01-15'...

**问题 #11** (第 317 行, 语言: sql)
- **错误**: 可能的语法问题: TIME                    -- TIME(0)，无小数秒
TIME(3)   ...

**问题 #12** (第 337 行, 语言: sql)
- **错误**: 可能的语法问题: TIMESTAMP               -- TIMESTAMP(6)
TIMESTAMP(...

**问题 #13** (第 356 行, 语言: sql)
- **错误**: 可能的语法问题: TIMESTAMP_LTZ(3)
TO_TIMESTAMP_LTZ(EPOCHMILLIS, 3)...

**问题 #14** (第 379 行, 语言: sql)
- **错误**: 可能的语法问题: -- 年月间隔
INTERVAL YEAR TO MONTH
INTERVAL '2-6' YEAR...

**问题 #15** (第 431 行, 语言: sql)
- **错误**: 可能的语法问题: CAST(EXPRESSION AS TYPE)
EXPRESSION::TYPE        -...

**问题 #16** (第 438 行, 语言: sql)
- **错误**: 可能的语法问题: -- 数值转换
CAST('123' AS INT)
CAST(123 AS STRING)
CAS...

**问题 #17** (第 535 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxt1c6juyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.DataTypes;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpxt1c6juyTempValidat
- **错误行**: 3

**问题 #19** (第 583 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2fyz3a54TempValidation.java:4: 错误: 找不到符号
DataType dataType = DataTypes.INT();
^
  符号:   类 DataType
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp2fyz
- **错误行**: 4

**问题 #22** (第 685 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe6ggfoyxTempValidation.java:3: 错误: 非法的表达式开始
        TableEnvironment tEnv = TableEnvironment.create(...);
                                                        ^
- **错误行**: 3


### `Flink\03-api\03.02-table-sql-api\flink-cep-complete-guide.md`

**问题 #9** (第 316 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn_m3oletLoginEvent.java:16: 错误: 未命名类 是预览功能，默认情况下禁用。
Pattern<LoginEvent, ?> pattern = Pattern
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 16

**问题 #10** (第 352 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphvqxvf8uTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.cep.pattern.Pattern;
        ^
C:\Users\luyan\AppData\Local\Temp\tmphvqxvf8uTempValidat
- **错误行**: 3

**问题 #11** (第 387 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuabweeoeTempValidation.java:4: 错误: 找不到符号
Pattern.<Event>begin("login").where(evt -> evt.type.equals("LOGIN"))
         ^
  符号:   类 Event
  位置: 类 TempValidation
C:\
- **错误行**: 4

**问题 #12** (第 424 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoikl1679TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.pattern.conditions.IterativeCondition;
^
C:\Users\luyan\AppData\Local\Temp\tmpoikl1679TempV
- **错误行**: 3

**问题 #13** (第 475 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv69emq4pTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.CEP;
^
C:\Users\luyan\AppData\Local\Temp\tmpv69emq4pTempValidation.java:3: 错误: 不是语句
import
- **错误行**: 3

**问题 #18** (第 964 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpstn4mixaTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.cep.nfa.aftermatch.AfterMatchSkipStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 3

**问题 #19** (第 987 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp65zpszpsTempValidation.java:6: 错误: 非法的表达式开始
    .where(...)
           ^
1 个错误

- **错误行**: 6

**问题 #20** (第 1007 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp378igr6_TempValidation.java:5: 错误: 找不到符号
    MyEvent.class,
    ^
  符号:   类 MyEvent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp378igr6_TempValidat
- **错误行**: 5

**问题 #21** (第 1023 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp46d46itbTempValidation.java:4: 错误: 找不到符号
Pattern.<Event>begin("start")
         ^
  符号:   类 Event
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp46d46
- **错误行**: 4

**问题 #26** (第 1227 行, 语言: sql)
- **错误**: 可能的语法问题: -- AFTER MATCH SKIP子句
AFTER MATCH SKIP PAST LAST R...


### `Flink\03-api\03.02-table-sql-api\flink-materialized-table-deep-dive.md`

**问题 #2** (第 113 行, 语言: sql)
- **错误**: 可能的语法问题: -- HASH分布（默认）
DISTRIBUTED BY HASH(USER_ID) INTO 16...


### `Flink\03-api\03.02-table-sql-api\flink-process-table-functions.md`

**问题 #10** (第 559 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjfg94o8cTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpjfg94o8cTemp
- **错误行**: 3


### `Flink\03-api\03.02-table-sql-api\flink-python-udf.md`

**问题 #5** (第 277 行, 语言: python)
- **错误**: SyntaxError: invalid syntax
- **错误行**: 32

**问题 #10** (第 516 行, 语言: yaml)
- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 10, column 1:
    pandas==2.1.4
    ^ (line: 10)
- **错误行**: 10


### `Flink\03-api\03.02-table-sql-api\flink-sql-calcite-optimizer-deep-dive.md`

**问题 #10** (第 652 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps17ko8cfTempValidation.java:4: 错误: 找不到符号
VolcanoPlanner planner = new VolcanoPlanner(
^
  符号:   类 VolcanoPlanner
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #14** (第 774 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6me4l3y_TempValidation.java:4: 错误: 非法的表达式开始
void optimizeGroup(Group group, Cost upperBound) {
^
C:\Users\luyan\AppData\Local\Temp\tmp6me4l3y_TempValidation.java:4
- **错误行**: 4

**问题 #16** (第 827 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv8uafej8TempValidation.java:4: 错误: 非法的表达式开始
public void onMatch(RelOptRuleCall call) {
^
C:\Users\luyan\AppData\Local\Temp\tmpv8uafej8TempValidation.java:37: 错误: 需
- **错误行**: 4

**问题 #19** (第 906 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb73wnwqxTempValidation.java:4: 错误: 非法的表达式开始
public void onMatch(RelOptRuleCall call) {
^
C:\Users\luyan\AppData\Local\Temp\tmpb73wnwqxTempValidation.java:26: 错误: 需
- **错误行**: 4

**问题 #23** (第 1009 行, 语言: sql)
- **错误**: 可能的语法问题: -- 启用两阶段聚合
SET TABLE.OPTIMIZER.AGG-PHASE-STRATEGY ...; 可能的语法问题: -- 或自动选择
SET TABLE.OPTIMIZER.AGG-PHASE-STRATEGY = ...

**问题 #41** (第 1551 行, 语言: sql)
- **错误**: 可能的语法问题: -- 分析整张表
ANALYZE TABLE ORDERS COMPUTE STATISTICS;...; 可能的语法问题: -- 分析指定列
ANALYZE TABLE ORDERS COMPUTE STATISTICS F...; 可能的语法问题: -- 采样分析
ANALYZE TABLE BIG_TABLE COMPUTE STATISTICS...; 可能的语法问题:

**问题 #44** (第 1628 行, 语言: sql)
- **错误**: 可能的语法问题: -- 优化1: 添加统计信息
ANALYZE TABLE ORDERS COMPUTE STATIS...; 可能的语法问题: ANALYZE TABLE PRODUCTS COMPUTE STATISTICS;...; 可能的语法问题: ANALYZE TABLE CATEGORIES COMPUTE STATISTICS;...; 可能的语法问题: -- 优化2: 启用CBO

**问题 #50** (第 1757 行, 语言: sql)
- **错误**: 可能的语法问题: -- 优化1: 启用DISTINCT拆分
SET TABLE.OPTIMIZER.DISTINCT-...; 可能的语法问题: -- 优化2: 启用MINI-BATCH
SET TABLE.EXEC.MINI-BATCH.ENA...; 可能的语法问题: -- 优化3: 启用LOCAL-GLOBAL聚合
SET TABLE.OPTIMIZER.LOCAL...; 可能的语法问题:

**问题 #66** (第 2511 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_60_xzvvBatchPhysicalRel.java:31: 错误: 非法的表达式开始
        Transformation<RowData> leftInput = ...;
                                            ^
C:\Users\luyan\AppDat
- **错误行**: 31


### `Flink\03-api\03.02-table-sql-api\flink-sql-hints-optimization.md`

**问题 #12** (第 324 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgnzufg99TempValidation.java:4: 错误: 找不到符号
tableEnv.createTemporaryFunction("ExtractJson", JsonPathFunction.class);
                                                ^
- **错误行**: 4

**问题 #13** (第 339 行, 语言: sql)
- **错误**: 可能的语法问题: -- 基础执行计划
EXPLAIN PLAN FOR
SELECT /*+ BROADCAST_HA...; 可能的语法问题: -- 详细执行计划（含优化器决策）
EXPLAIN ESTIMATED_COST, CHANGELO...


### `Flink\03-api\03.02-table-sql-api\flink-sql-window-functions-deep-dive.md`

**问题 #4** (第 338 行, 语言: sql)
- **错误**: 可能的语法问题: -- 优化后：仅存储中间状态
-- FLINK自动优化为：
-- VALUESTATE<SUMACC...

**问题 #6** (第 366 行, 语言: sql)
- **错误**: 可能的语法问题: -- 或自动识别
SET 'TABLE.OPTIMIZER.AGG-PHASE-STRATEGY' ...

**问题 #8** (第 426 行, 语言: sql)
- **错误**: 可能的语法问题: -- 输出示例:
-- CATEGORY | WINDOW_START        | WINDO...

**问题 #9** (第 465 行, 语言: sql)
- **错误**: 可能的语法问题: -- 关键洞察:
-- - 每个事件同时贡献给5个窗口
-- - 状态开销是TUMBLE的5倍
--...

**问题 #10** (第 500 行, 语言: sql)
- **错误**: 可能的语法问题: -- 输出示例:
-- USER_ID | SESSION_START       | SESSIO...

**问题 #11** (第 538 行, 语言: sql)
- **错误**: 可能的语法问题: -- 输出示例（假设当前为11:00）:
-- WINDOW_START        | WIND...

**问题 #13** (第 630 行, 语言: sql)
- **错误**: 可能的语法问题: -- 输出包含CHANGELOG（排名变化时产生撤回更新）
-- +I: 新增排名
-- -D: 旧...

**问题 #15** (第 703 行, 语言: sql)
- **错误**: 可能的语法问题: -- 配置允许延迟
SET 'TABLE.EXEC.EMIT.ALLOW-LATENESS' = '...; 可能的语法问题: -- 延迟数据侧输出（FLINK SQL暂不支持，需DATASTREAM API）
-- 或使用PR...


### `Flink\03-api\03.02-table-sql-api\flink-table-sql-complete-guide.md`

**问题 #7** (第 372 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpswbrjuh8TempValidation.java:4: 错误: 找不到符号
TableDescriptor sourceDescriptor = TableDescriptor.forConnector("kafka")
^
  符号:   类 TableDescriptor
  位置: 类 TempValidatio
- **错误行**: 4

**问题 #10** (第 443 行, 语言: sql)
- **错误**: 可能的语法问题: -- 切换数据库
USE ANALYTICS;...

**问题 #13** (第 498 行, 语言: sql)
- **错误**: 可能的语法问题: <!-- 以下语法为概念设计，实际 FLINK 版本尚未支持 -->
~~CREATE MODEL~...

**问题 #19** (第 581 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptrn_hyf3TempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.from("orders")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmptrn_h
- **错误行**: 4

**问题 #24** (第 675 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu4twn1__TempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.from("user_events")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #32** (第 811 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptk8dl7waTempValidation.java:4: 错误: 找不到符号
Table topN = tableEnv.from("product_sales")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #39** (第 959 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcvju5tp0TempValidation.java:4: 错误: 找不到符号
Table windowed = tableEnv.from("user_events")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4

**问题 #44** (第 1068 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj71l_l0kTempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.from("orders")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpj71l_
- **错误行**: 4

**问题 #53** (第 1371 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa_atotjvTempValidation.java:12: 错误: 非法的表达式开始
    .next("C").where(...)
                     ^
C:\Users\luyan\AppData\Local\Temp\tmpa_atotjvTempValidation.java:13:
- **错误行**: 12

**问题 #58** (第 1507 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 22

**问题 #64** (第 1645 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdmvyrrcwTempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql(
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #66** (第 1709 行, 语言: sql)

- **错误**: 可能的语法问题: -- 创建嵌入模型
<!-- 以下语法为概念设计，实际 FLINK 版本尚未支持 -->
~~CRE...; 可能的语法问题: -- 创建分类模型
~~CREATE MODEL SENTIMENT_CLASSIFIER~~ (未...

**问题 #76** (第 2067 行, 语言: sql)

- **错误**: 可能的语法问题: -- 1. 配置 STATE TTL
SET 'TABLE.EXEC.STATE.TTL' = '1...; 可能的语法问题: -- 3. 增量 CHECKPOINT
SET 'STATE.BACKEND.INCREMENTAL...; 可能的语法问题: -- 4. ROCKSDB 调优
SET 'STATE.BACKEND.ROCKSDB.PREDEF...

**问题 #77** (第 2085 行, 语言: sql)

- **错误**: 可能的语法问题: -- 1. 合理设置 WATERMARK 延迟
-- 过小: 丢数据
-- 过大: 延迟高
WATE...; 可能的语法问题: -- 3. 允许延迟数据
SET 'TABLE.EXEC.EMIT.ALLOW-LATENESS' ...


### `Flink\03-api\03.02-table-sql-api\flink-vector-search-rag.md`

**问题 #14** (第 589 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...; 可能的语法问题: -- ============================================
--...


### `Flink\03-api\03.02-table-sql-api\materialized-tables.md`

**问题 #11** (第 477 行, 语言: sql)

- **错误**: 可能的语法问题: -- 2. 查看所有物化表（FLINK 2.2+）
SHOW MATERIALIZED TABLES...; 可能的语法问题: -- 3. 查看特定物化表详细信息
DESCRIBE EXTENDED USER_ACTIVITY_...

**问题 #13** (第 547 行, 语言: sql)

- **错误**: 可能的语法问题: -- 手动验证推断的 FRESHNESS
DESCRIBE EXTENDED USER_STATS_...; 可能的语法问题: -- 预期输出: FRESHNESS = 1 MINUTE (基于 5S WATERMARK + 缓...

**问题 #17** (第 658 行, 语言: sql)

- **错误**: 可能的语法问题: -- 优势：
-- 1. 物化表 USER_PROFILES_MT 每小时刷新，存储预计算结果
--...

**问题 #18** (第 701 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm8fkj7qjTempValidation.java:4: 错误: 找不到符号
StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);
^
  符号:   类 StreamTableEnvironment
  位置: 类 TempValid
- **错误行**: 4

**问题 #19** (第 728 行, 语言: sql)

- **错误**: 可能的语法问题: -- FLINK 2.2+ 新增语法

-- 列出所有物化表
SHOW MATERIALIZED T...; 可能的语法问题: -- 列出指定数据库的物化表
SHOW MATERIALIZED TABLES FROM ANALY...; 可能的语法问题: -- 带过滤条件
SHOW MATERIALIZED TABLES LIKE 'USER%';...; 可能的语法问题: --

**问题 #26** (第 1001 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看所有物化表（FLINK 2.2+）
SHOW MATERIALIZED TABLES [F...


### `Flink\03-api\03.02-table-sql-api\model-ddl-and-ml-predict.md`

**问题 #1** (第 15 行, 语言: sql)

- **错误**: 可能的语法问题: <!-- 以下语法为概念设计，实际 FLINK 版本尚未支持 -->
~~CREATE MODEL~...

**问题 #10** (第 253 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz29s61myTempValidation.java:8: 错误: 非法的类型开始
    .process(new KeyedProcessFunction<..., Row, Row>() {
                                      ^
C:\Users\luyan\AppData\
- **错误行**: 8

**问题 #13** (第 408 行, 语言: sql)

- **错误**: 可能的语法问题: -- 步骤 1: 创建 OPENAI 模型定义
<!-- 以下为概念设计 -->
~~CREATE ...

**问题 #14** (第 487 行, 语言: sql)

- **错误**: 可能的语法问题: -- 步骤 1: 创建嵌入模型（用于文档向量化）
~~CREATE MODEL TEXT_EMBED...; 可能的语法问题: -- 步骤 2: 创建 LLM 模型
~~CREATE MODEL QA_MODEL~~ (未来可能...

**问题 #16** (第 642 行, 语言: sql)

- **错误**: 可能的语法问题: ~~CREATE MODEL INTERNAL_CLASSIFIER~~ (未来可能的语法)
WIT...


### `Flink\03-api\03.02-table-sql-api\query-optimization-analysis.md`

**问题 #11** (第 443 行, 语言: sql)

- **错误**: 可能的语法问题: -- 方法 2: TABLE CONFIG
SET TABLE.OPTIMIZER.JOIN.BRO...

**问题 #17** (第 621 行, 语言: sql)

- **错误**: 可能的语法问题: -- 方式 1: SQL 级别
SET TABLE.EXEC.STATE.TTL = '1 HOUR...; 可能的语法问题: -- 方式 2: TABLE API
TABLE RESULT = TABLEENV
    .SQ...

**问题 #18** (第 663 行, 语言: sql)

- **错误**: 可能的语法问题: -- 启用 CBO JOIN 重排序
SET TABLE.OPTIMIZER.JOIN-REORDE...; 可能的语法问题: -- 启用 DISTINCT 聚合拆分
SET TABLE.OPTIMIZER.DISTINCT-A...; 可能的语法问题: -- 设置广播 JOIN 阈值
SET TABLE.OPTIMIZER.JOIN.BROADCAST...; 可能的语法问题:

**问题 #19** (第 685 行, 语言: sql)

- **错误**: 可能的语法问题: -- 分析整张表
ANALYZE TABLE ORDERS COMPUTE STATISTICS;...; 可能的语法问题: -- 分析指定列
ANALYZE TABLE ORDERS COMPUTE STATISTICS F...; 可能的语法问题: -- 采样分析（大数据表）
ANALYZE TABLE BIG_TABLE COMPUTE STAT...

**问题 #20** (第 698 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看表统计信息
SHOW CREATE TABLE ORDERS;...; 可能的语法问题: -- 通过 EXPLAIN 查看优化器使用的统计
EXPLAIN PLAN FOR SELECT *...

**问题 #22** (第 740 行, 语言: sql)

- **错误**: 可能的语法问题: -- 1. 设置合理的状态 TTL
SET TABLE.EXEC.STATE.TTL = '24 H...; 可能的语法问题: -- 2. 使用 ROCKSDB 状态后端（大状态）
SET STATE.BACKEND = 'RO...; 可能的语法问题: -- 3. 配置增量 CHECKPOINT
SET EXECUTION.CHECKPOINTING....


### `Flink\03-api\03.02-table-sql-api\sql-functions-cheatsheet.md`

**问题 #3** (第 798 行, 语言: sql)

- **错误**: 可能的语法问题: -- 数学
ABS(), ROUND(), CEIL(), FLOOR(), POWER(), SQ...


### `Flink\03-api\03.02-table-sql-api\sql-vs-datastream-comparison.md`

**问题 #3** (第 267 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2nf5cuzrTempValidation.java:10: 错误: 找不到符号
    .aggregate(new OrderAggregateFunction())
                   ^
  符号:   类 OrderAggregateFunction
  位置: 类 TempValidation
- **错误行**: 10

**问题 #5** (第 298 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq6k5izceTempValidation.java:3: 错误: 找不到符号
orders
^
  符号:   变量 orders
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpq6k5izceTempValidation.java:4: 错误:
- **错误行**: 3

**问题 #6** (第 317 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0dl3xhwiAsyncUserEnrichment.java:20: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedOrder> enriched = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以启用 未命名类
- **错误行**: 20

**问题 #7** (第 348 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi9580lgeTempValidation.java:4: 错误: 找不到符号
tableEnv.createTemporaryView("orders", orderStream);
                                       ^
  符号:   变量 orderStream
  位置:
- **错误行**: 4


### `Flink\03-api\09-language-foundations\02-python-api.md`

**问题 #14** (第 401 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 8, column 1:
    scikit-learn==1.3.0
    ^ (line: 8)
- **错误行**: 8

**问题 #26** (第 1020 行, 语言: python)

- **错误**: SyntaxError: 'await' outside async function
- **错误行**: 4

**问题 #27** (第 1035 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 6

**问题 #32** (第 1324 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 17


### `Flink\03-api\09-language-foundations\03-rust-native.md`

**问题 #7** (第 451 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6_2e2fi3TempValidation.java:4: 错误: 找不到符号
    stream,
    ^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp6_2e2fi3TempValidation.jav
- **错误行**: 4


### `Flink\03-api\09-language-foundations\04-streaming-lakehouse.md`

**问题 #19** (第 575 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_CATALOG;...

**问题 #21** (第 770 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...


### `Flink\03-api\09-language-foundations\06-risingwave-deep-dive.md`

**问题 #21** (第 1265 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn_1n5cb_TempValidation.java:13: 错误: 找不到符号
MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
^
  符号:   类 MySqlSource
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 13

**问题 #24** (第 1347 行, 语言: sql)

- **错误**: 可能的语法问题: -- 7. 应用层查询示例（LLM RAG 调用）
-- SELECT * FROM RAG_RET...


### `Flink\03-api\09-language-foundations\07-rust-streaming-landscape.md`

**问题 #16** (第 876 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn15lmrhfTempValidation.java:4: 错误: 找不到符号
DataStream<Transaction> transactions = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4


### `Flink\03-api\09-language-foundations\10-wasi-component-model.md`

**问题 #15** (第 786 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpszo9jrsdWasiComponentOperator.java:77: 错误: 非法的表达式开始
                byte[] value = getRuntimeContext().getState(...).value();

- **错误行**: 77


### `Flink\03-api\09-language-foundations\datastream-api-cheatsheet.md`

**问题 #1** (第 38 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps0ow1nl3TempValidation.java:4: 错误: 找不到符号
DataStream<Integer> numbers = env.fromElements(1, 2, 3, 4, 5);
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 4

**问题 #3** (第 80 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp25nmal3tTempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #5** (第 122 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1q4ilanbTempValidation.java:4: 错误: 找不到符号
DataStream<Integer> mapped = stream.map(x -> x * 2);
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 4

**问题 #6** (第 143 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxueusn8xTempValidation.java:4: 错误: 找不到符号
KeyedStream<Event, String> keyed = stream
^
  符号:   类 KeyedStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #7** (第 168 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_fgqhikqTempValidation.java:6: 错误: 找不到符号
DataStream<Result> tumbling = keyed
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp_fg
- **错误行**: 6

**问题 #8** (第 209 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgcyka195TempValidation.java:4: 错误: 找不到符号
DataStream<Result> joined = stream1
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpgcy
- **错误行**: 4

**问题 #9** (第 240 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp220xqugtCountWithTimeout.java:2: 错误: 找不到符号
class CountWithTimeout extends KeyedProcessFunction<String, Event, Result> {
                               ^
  符号: 类 Ke
- **错误行**: 2

**问题 #10** (第 292 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfi0ut_g2TempValidation.java:4: 错误: 找不到符号
stream.print();                           // 输出到stdout
^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #11** (第 316 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjbwvb3toTempValidation.java:4: 错误: 找不到符号
KafkaSink<String> sink = KafkaSink.<String>builder()
^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #12** (第 379 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt2iuk2m2TempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #13** (第 400 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgcu5z8_hTempValidation.java:6: 错误: 找不到符号
WatermarkStrategy.<Event>forMonotonousTimestamps()
                   ^
  符号:   类 Event
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 6

**问题 #14** (第 447 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5t8ztsu3TempValidation.java:6: 错误: 非法的表达式开始
.window(TumblingEventTimeWindows.of(Time.minutes(5)))
^
C:\Users\luyan\AppData\Local\Temp\tmp5t8ztsu3TempValidation.jav
- **错误行**: 6

**问题 #15** (第 476 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl1ndo1n9TempValidation.java:11: 错误: 找不到符号
    .aggregate(new MyAggregate());
                   ^
  符号:   类 MyAggregate
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 11

**问题 #17** (第 586 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq1w1exebTempValidation.java:4: 错误: 找不到符号
StateTtlConfig ttlConfig = StateTtlConfig
^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #18** (第 603 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcpfoye3sTempValidation.java:4: 错误: 找不到符号
MapStateDescriptor<String, Rule> ruleStateDescriptor =
^
  符号:   类 MapStateDescriptor
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 4

**问题 #19** (第 672 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfs38r8xdTempValidation.java:6: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpfs38r8xdTempV
- **错误行**: 6


### `Flink\03-api\09-language-foundations\flink-25-wasm-udf-ga.md`

**问题 #43** (第 2156 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu_7i3p4bTempValidation.java:4: 错误: 找不到符号
WasmFunctionConfig optimalConfig = WasmFunctionConfig.builder()
^
  符号:   类 WasmFunctionConfig
  位置: 类 TempValidation
C:\U
- **错误行**: 4


### `Flink\03-api\09-language-foundations\flink-datastream-api-complete-guide.md`

**问题 #4** (第 176 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpby7nki6fTempValidation.java:4: 错误: 找不到符号
DataStream<String> ids = events.map(new MapFunction<Event, String>() {
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Us
- **错误行**: 4

**问题 #8** (第 272 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpekgmv6pzTempValidation.java:4: 错误: 找不到符号
KeyedStream<Event, String> keyed = events.keyBy(Event::getUserId);
^
  符号:   类 KeyedStream
  位置: 类 TempValidation
C:\Users
- **错误行**: 4

**问题 #11** (第 390 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt49u6l3jTempValidation.java:4: 错误: 找不到符号
StateTtlConfig ttlConfig = StateTtlConfig
^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #14** (第 530 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmploevplwzTempValidation.java:4: 错误: 找不到符号
DataStream<Event> withTimestamps = stream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #15** (第 547 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplv3ofqjrTempValidation.java:8: 错误: 需要';'
public void onTimer(long timestamp, OnTimerContext ctx, Collector<Out> out) {
                   ^
C:\Users\luyan\AppData\
- **错误行**: 8

**问题 #17** (第 596 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5y8m_giwCustomWatermarkGenerator.java:2: 错误: 需要 class、interface、enum 或 record
WatermarkStrategy.<Event>forMonotonousTimestamps()
^
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 2

**问题 #19** (第 644 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpffpfz8xtTempValidation.java:9: 错误: 找不到符号
    .aggregate(new MyAggregate());
                   ^
  符号:   类 MyAggregate
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 9

**问题 #21** (第 687 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3m5tvhmwAsyncDatabaseRequest.java:48: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Result> asyncResult = AsyncDataStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 48

**问题 #23** (第 777 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7umwtmcnTempValidation.java:7: 错误: 找不到符号
timeout = 5_000;  // 5 seconds
^
  符号:   变量 timeout
  位置: 类 TempValidation
1 个错误

- **错误行**: 7

**问题 #28** (第 986 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq19bb3t0TempValidation.java:4: 错误: 找不到符号
Pattern<Transaction, ?> fraudPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #29** (第 1058 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6ydfwcx9TempValidation.java:4: 错误: 找不到符号
Pattern<Transaction, ?> complexPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #32** (第 1128 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2e_wfn9cTempValidation.java:4: 错误: 找不到符号
MapStateDescriptor<String, Rule> ruleStateDescriptor =
^
  符号:   类 MapStateDescriptor
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 4

**问题 #33** (第 1202 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdrpi5fozTempValidation.java:4: 错误: 不是语句
KeyedBroadcastProcessFunction<String, Event, Rule, Result> {
                             ^
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #35** (第 1277 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpttj87cb5TempValidation.java:12: 错误: 需要';'
public void open(Configuration parameters) {
                ^
C:\Users\luyan\AppData\Local\Temp\tmpttj87cb5TempValidatio
- **错误行**: 12

**问题 #36** (第 1296 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdgqitm0pTempValidation.java:10: 错误: 非法的表达式开始
byte[] keySerialized = ...;  // 序列化查询键
                       ^
1 个错误

- **错误行**: 10

**问题 #39** (第 1477 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8r8d3l28TempValidation.java:4: 错误: 找不到符号
StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);
^
  符号:   类 StreamTableEnvironment
  位置: 类 TempValid
- **错误行**: 4

**问题 #41** (第 1526 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjcbm96g9TempValidation.java:4: 错误: 找不到符号
DataStream<Event> salted = events
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpjcbm9
- **错误行**: 4


### `Flink\03-api\09-language-foundations\flink-language-support-complete-guide.md`

**问题 #2** (第 196 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpknqfxtyzTempValidation.java:4: 错误: 需要';'
List<Integer> vs List<String> → 都是 List
                ^
C:\Users\luyan\AppData\Local\Temp\tmpknqfxtyzTempValidation.java
- **错误行**: 4

**问题 #11** (第 860 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 3

**问题 #14** (第 1163 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyz7ilfa0JavaWithScalaUDF.java:23: 错误: 需要'{'
class ScalaMapFunction[T, R] extends RichMapFunction[T, R] {
                      ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 23


### `Flink\04-runtime\04.01-deployment\evolution\config-management.md`

**问题 #1** (第 48 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6prs25hnTempValidation.java:3: 错误: 找不到符号
ConfigManager cm = ConfigManager.getInstance();
^
  符号:   类 ConfigManager
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 3


### `Flink\04-runtime\04.01-deployment\evolution\scheduling-evolution.md`

**问题 #2** (第 284 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2dlgx4uwTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #3** (第 300 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg30ulagcTempValidation.java:8: 错误: 不是语句
scheduler-mode: legacy
         ^
C:\Users\luyan\AppData\Local\Temp\tmpg30ulagcTempValidation.java:8: 错误: 需要';'
scheduler-m
- **错误行**: 8

**问题 #4** (第 316 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphs78ym1pTempValidation.java:14: 错误: 不是语句
scheduler-mode: reactive
         ^
C:\Users\luyan\AppData\Local\Temp\tmphs78ym1pTempValidation.java:14: 错误: 需要';'
schedul
- **错误行**: 14

**问题 #5** (第 336 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptkxb_f49TempValidation.java:11: 错误: 不是语句
scheduler-mode: adaptive
         ^
C:\Users\luyan\AppData\Local\Temp\tmptkxb_f49TempValidation.java:11: 错误: 需要';'
schedul
- **错误行**: 11

**问题 #6** (第 363 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2yzntr4fTempValidation.java:14: 错误: 不是语句
scheduler-mode: adaptive-v2
         ^
C:\Users\luyan\AppData\Local\Temp\tmp2yzntr4fTempValidation.java:14: 错误: 需要';'
sche
- **错误行**: 14


### `Flink\04-runtime\04.01-deployment\evolution\yarn-deploy.md`

**问题 #3** (第 58 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy7r1m230TempValidation.java:3: 错误: 找不到符号
        env.getConfig().setAutoWatermarkInterval(200);
        ^
  符号:   变量 env
  位置: 类 TempValidation
1 个错误

- **错误行**: 3


### `Flink\04-runtime\04.01-deployment\flink-24-deployment-improvements.md`

**问题 #75** (第 2862 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    flink-conf-global.yaml: |
    ^ (line: 4)
found duplicate key "apiVersion" with value "flink.apache.org/v1beta1" (original v
- **错误行**: 4


### `Flink\04-runtime\04.01-deployment\flink-deployment-ops-complete-guide.md`

**问题 #16** (第 409 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 2:
     taskmanager.numberOfTaskSlots: 8
     ^ (line: 2)
found duplicate key "taskmanager.numberOfTaskSlots" with value "4" (origi
- **错误行**: 2

**问题 #17** (第 421 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    taskmanager.memory.network.min: 64mb
    ^ (line: 2)
found duplicate key "taskmanager.memory.network.min" with value "256mb"
- **错误行**: 2

**问题 #18** (第 433 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    execution.checkpointing.interval ...
    ^ (line: 2)
found duplicate key "execution.checkpointing.interval" with value "30s
- **错误行**: 2

**问题 #42** (第 1143 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf_qoendrTempValidation.java:4: 错误: 找不到符号
DataStream<Event> stream = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpf_qoendr
- **错误行**: 4


### `Flink\04-runtime\04.01-deployment\flink-k8s-operator-1.14-guide.md`

**问题 #7** (第 152 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd19fc6c_TempValidation.java:4: 错误: 找不到符号
DataStream<Event> stream = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpd19fc6c_
- **错误行**: 4

**问题 #9** (第 188 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 2, column 17:
      deploymentName: string,      # FlinkDeployment 引用
                    ^ (line: 2)
- **错误行**: 2
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #29** (第 598 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp44y6dkxoTempValidation.java:4: 错误: 需要';'
DataStream<Result> process(DataStream<Event> input) {
                          ^
C:\Users\luyan\AppData\Local\Temp\tmp44y
- **错误行**: 4

**问题 #44** (第 971 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 15, column 26:
            - blue: 90, green: 10, duration: 5m
                             ^ (line: 15)
- **错误行**: 15
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Flink\04-runtime\04.01-deployment\flink-kubernetes-autoscaler-deep-dive.md`

**问题 #19** (第 471 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 12, column 78:
     ... ."Source: Kafka".max-parallelism: "12"
                                         ^ (line: 12)
- **错误行**: 12
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Flink\04-runtime\04.01-deployment\flink-kubernetes-operator-deep-dive.md`

**问题 #6** (第 165 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfde2r69fTempValidation.java:4: 错误: 找不到符号
while (running) {
       ^
  符号:   变量 running
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpfde2r69fTempVali
- **错误行**: 4


### `Flink\04-runtime\04.01-deployment\flink-serverless-architecture.md`

**问题 #6** (第 255 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppqf1na3cTempValidation.java:5: 错误: 需要';'
public Response handle(Request req) {
                      ^
C:\Users\luyan\AppData\Local\Temp\tmppqf1na3cTempValidation.
- **错误行**: 5


### `Flink\04-runtime\04.01-deployment\multi-cloud-deployment-templates.md`

**问题 #10** (第 908 行, 语言: yaml)

- **错误**: could not determine a constructor for the tag '!Ref'
  in "<unicode string>", line 290, column 12:
        Value: !Ref FlinkApplication
               ^ (line: 290)
- **错误行**: 290

**问题 #21** (第 2449 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 23, column 52:
     ... aproc.logging.stackdriver.enable: 'true'
                                         ^ (line: 23)
- **错误行**: 23
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Flink\04-runtime\04.01-deployment\serverless-flink-ga-guide.md`

**问题 #10** (第 460 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    spec:
    ^ (line: 2)
found duplicate key "spec" with value "{}" (original value: "{}")
  in "<unicode string>", line 7, co
- **错误行**: 2

**问题 #11** (第 475 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend: hashmap  # 内存状态，重启丢失
    ^ (line: 2)
found duplicate key "state.backend" with value "forst" (original value:
- **错误行**: 2

**问题 #15** (第 772 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 98, column 22:
        resourceGroupName: "flink-serverless",
                         ^ (line: 98)
- **错误行**: 98
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Flink\04-runtime\04.03-observability\distributed-tracing.md`

**问题 #2** (第 88 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkezckuctTempValidation.java:4: 错误: 不是语句
   traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
                  ^
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #8** (第 343 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp77ebjkqgTracingStreamOperator.java:2: 错误: 找不到符号
class TracingStreamOperator<OUT> extends AbstractStreamOperator<OUT> {
                                         ^

- **错误行**: 2


### `Flink\04-runtime\04.03-observability\evolution\alerting-evolution.md`

**问题 #2** (第 65 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqpv4guj5TempValidation.java:3: 错误: 找不到符号
        AlertManager.register(new AlertRule()
        ^
  符号:   变量 AlertManager
  位置: 类 TempValidation
C:\Users\luyan\AppD
- **错误行**: 3


### `Flink\04-runtime\04.03-observability\evolution\logging-evolution.md`

**问题 #2** (第 55 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb2zbl9znTempValidation.java:3: 错误: 找不到符号
        LOG.info("Processing event",
        ^
  符号:   变量 LOG
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3


### `Flink\04-runtime\04.03-observability\evolution\metrics-evolution.md`

**问题 #2** (第 56 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwygjxsijTempValidation.java:3: 错误: 找不到符号
        getRuntimeContext()
        ^
  符号:   方法 getRuntimeContext()
  位置: 类 TempValidation
1 个错误

- **错误行**: 3


### `Flink\04-runtime\04.03-observability\evolution\slo-evolution.md`

**问题 #2** (第 65 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy9y18sj4TempValidation.java:3: 错误: 找不到符号
        double errorBudget = 1 - slo.getTarget();
                                 ^
  符号:   变量 slo
  位置: 类 TempValidation
- **错误行**: 3


### `Flink\04-runtime\04.03-observability\evolution\testing-evolution.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_r3rwwtvTempValidation.java:4: 错误: 需要';'
public void testPipeline() throws Exception {
                        ^
C:\Users\luyan\AppData\Local\Temp\tmp_r3rwwtvTempV
- **错误行**: 4

**问题 #2** (第 70 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx08uy_qiTempValidation.java:3: 错误: 找不到符号
        MiniCluster cluster = new MiniCluster(
        ^
  符号:   类 MiniCluster
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3


### `Flink\04-runtime\04.03-observability\evolution\tracing-evolution.md`

**问题 #2** (第 63 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1mxne40tTempValidation.java:3: 错误: 找不到符号
Span span = tracer.spanBuilder("process").startSpan();
^
  符号:   类 Span
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 3


### `Flink\04-runtime\04.03-observability\evolution\webui-evolution.md`

**问题 #1** (第 48 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbq2xla0_TempValidation.java:3: 错误: 非法的表达式开始
        GET /jobs/{jobid}/vertices
                  ^
C:\Users\luyan\AppData\Local\Temp\tmpbq2xla0_TempValidation.java
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\04.04-cdc-debezium-integration.md`

**问题 #10** (第 581 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf_7c4v07TempValidation.java:3: 错误: 非法的表达式开始
        import com.ververica.cdc.connectors.mysql.source.MySqlSource;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpf_
- **错误行**: 3

**问题 #11** (第 615 行, 语言: sql)

- **错误**: 可能的语法问题: -- POSTGRESQL配置（POSTGRESQL.CONF）
WAL_LEVEL = LOGIC...

**问题 #15** (第 810 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查询数据湖（流读模式）
SET 'EXECUTION.RUNTIME-MODE' = 'STR...

**问题 #20** (第 1042 行, 语言: sql)

- **错误**: 可能的语法问题: -- MYSQL服务器配置（MY.CNF）
[MYSQLD]

# 必需：开启BINLOG

SERVE...

**问题 #21** (第 1077 行, 语言: sql)

- **错误**: 可能的语法问题: -- POSTGRESQL.CONF
WAL_LEVEL = LOGICAL
MAX_REPLICA...

**问题 #24** (第 1140 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpetbv97o1TempValidation.java:4: 错误: 找不到符号
env.setRestartStrategy(RestartStrategies.exponentialDelayRestart(
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #25** (第 1165 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpim6uum3fTempValidation.java:4: 错误: 找不到符号
MySqlSource<String> source = MySqlSource.<String>builder()
^
  符号:   类 MySqlSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4


### `Flink\05-ecosystem\05.01-connectors\cloudevents-integration-guide.md`

**问题 #7** (第 479 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpur4vph72SchemaRoutingFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<CloudEvent> events = env
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #9** (第 571 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps3ixn4tkTempValidation.java:3: 错误: 找不到符号
        LOG.info("Processing event",
        ^
  符号:   变量 LOG
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #10** (第 581 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpin4sfxq5TempValidation.java:3: 错误: 找不到符号
        meterRegistry.counter("events.processed",
        ^
  符号:   变量 meterRegistry
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 3

**问题 #15** (第 889 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg7gerglwTempValidation.java:4: 错误: 找不到符号
TableEnvironment tableEnv = TableEnvironment.create(EnvironmentSettings.inStreamingMode());
^
  符号:   类 TableEnvironment

- **错误行**: 4

**问题 #20** (第 1414 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb6jur0hsAzureEventGridIntegration.java:3: 错误: 需要';'
import com.azure.core.models.CloudEvent as AzureCloudEvent;
                                       ^
1 个错误

- **错误行**: 3

**问题 #29** (第 2407 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6s0r6xtvTempValidation.java:4: 错误: 找不到符号
if (aggregate.getVersion() % SNAPSHOT_INTERVAL == 0) {
    ^
  符号:   变量 aggregate
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #31** (第 2460 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpadaha6qiTempValidation.java:5: 错误: 找不到符号
  ctx.timestamp() + sagaDefinition.getTimeoutMs()
  ^
  符号:   变量 ctx
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 5

**问题 #32** (第 2487 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc9t4zvvjTempValidation.java:4: 错误: 找不到符号
props.setProperty("batch.size", "16384");
^
  符号:   变量 props
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpc
- **错误行**: 4

**问题 #33** (第 2502 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv48ygh2vTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpv48ygh2vTempV
- **错误行**: 4


### `Flink\05-ecosystem\05.01-connectors\diskless-kafka-deep-dive.md`

**问题 #2** (第 106 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwayryx7lTempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #3** (第 135 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvo3df2eeTempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env =
        ^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3

**问题 #5** (第 229 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1pn6jwh7TempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\elasticsearch-connector-complete-guide.md`

**问题 #13** (第 172 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp71d_m5dvTempValidation.java:4: 错误: 非法的表达式开始
DataStream<LogEvent> stream = ...;
                              ^
1 个错误

- **错误行**: 4

**问题 #14** (第 186 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnu7t4foyTempValidation.java:4: 错误: 程序包ElasticsearchSink不存在
ElasticsearchSink.Builder<LogEvent> builder = new ElasticsearchSink.Builder<>(
                 ^
C:\Use
- **错误行**: 4

**问题 #16** (第 228 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8s7iora7TempValidation.java:4: 错误: 找不到符号
builder.setFlushOnCheckpoint(true);
^
  符号:   变量 builder
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #20** (第 372 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd2ahwew7TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.http.auth.AuthScope;
^
C:\Users\luyan\AppData\Local\Temp\tmpd2ahwew7TempValidation.java:3: 错误: 不是语句
i
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\evolution\cdc-connector.md`

**问题 #1** (第 58 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy91d6mwgTempValidation.java:3: 错误: 找不到符号
        MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
        ^
  符号:   类 MySqlSource
  位置: 类 TempValida
- **错误行**: 3

**问题 #2** (第 74 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi4sw_nvkTempValidation.java:3: 错误: 找不到符号
stream.process(new ProcessFunction<String, Row>() {
                   ^
  符号:   类 ProcessFunction
  位置: 类 TempValidation

- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\evolution\cloud-connector.md`

**问题 #1** (第 56 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4mx7ngknTempValidation.java:3: 错误: 找不到符号
        env.getConfig().setDefaultFileSystemScheme("s3://");
        ^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 3

**问题 #2** (第 68 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp09ojs4noTempValidation.java:3: 错误: 找不到符号
        FlinkKinesisConsumer<String> consumer = new FlinkKinesisConsumer<>(
        ^
  符号:   类 FlinkKinesisConsumer
  位置:
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\evolution\file-connector.md`

**问题 #1** (第 57 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzop9qhl_TempValidation.java:3: 错误: 找不到符号
        FileSource<String> source = FileSource
        ^
  符号:   类 FileSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3

**问题 #2** (第 70 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuvao_6wpTempValidation.java:3: 错误: 找不到符号
        FileSink<GenericRecord> sink = FileSink
        ^
  符号:   类 FileSink
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\evolution\jdbc-connector.md`

**问题 #1** (第 56 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpklrp999gTempValidation.java:3: 错误: 找不到符号
        JdbcSourceBuilder<Row> builder = JdbcSourceBuilder.<Row>builder()
        ^
  符号:   类 JdbcSourceBuilder
  位置: 类 Te
- **错误行**: 3

**问题 #2** (第 68 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzoo9hwwgTempValidation.java:3: 错误: 找不到符号
JdbcSink.sink(
^
  符号:   变量 JdbcSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpzoo9hwwgTempValidation.ja
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\evolution\kafka-connector.md`

**问题 #1** (第 55 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_ti__yneTempValidation.java:3: 错误: 找不到符号
        KafkaSource<String> source = KafkaSource.<String>builder()
        ^
  符号:   类 KafkaSource
  位置: 类 TempValidation

- **错误行**: 3

**问题 #2** (第 69 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvm_qtgzhTempValidation.java:3: 错误: 找不到符号
        KafkaSink<String> sink = KafkaSink.<String>builder()
        ^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\evolution\lakehouse-connector.md`

**问题 #1** (第 56 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb1pk45thTempValidation.java:5: 错误: 找不到符号
    .withOverwritePartition(partition)
                            ^
  符号:   变量 partition
  位置: 类 TempValidation
C:\Users\
- **错误行**: 5


### `Flink\05-ecosystem\05.01-connectors\evolution\mq-connector.md`

**问题 #1** (第 57 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfayb_q41TempValidation.java:3: 错误: 找不到符号
        PulsarSource<String> source = PulsarSource.builder()
        ^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Us
- **错误行**: 3

**问题 #2** (第 72 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj867_3g9TempValidation.java:3: 错误: 找不到符号
        RMQSink<String> sink = new RMQSink<>(
        ^
  符号:   类 RMQSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\evolution\nosql-connector.md`

**问题 #1** (第 58 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeb8_0lt4TempValidation.java:3: 错误: 找不到符号
        HBaseSinkFunction<Row> sink = new HBaseSinkFunction<>(
        ^
  符号:   类 HBaseSinkFunction
  位置: 类 TempValidatio
- **错误行**: 3

**问题 #2** (第 71 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpii3y1peyTempValidation.java:3: 错误: 找不到符号
        MongoDBSource<String> source = MongoDBSource.<String>builder()
        ^
  符号:   类 MongoDBSource
  位置: 类 TempValid
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\flink-24-connectors-guide.md`

**问题 #3** (第 149 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplx2wb5_4TempValidation.java:3: 错误: 不是语句
        Kafka3Source<T> = ⟨BootstrapServers, TopicPattern, ConsumerProtocol,
                    ^
C:\Users\luyan\AppData\L
- **错误行**: 3

**问题 #13** (第 459 行, 语言: sql)

- **错误**: 可能的语法问题: -- 传统方式 (显式指定 JAR)
SET 'PIPELINE.JARS' = 'FILE:///...

**问题 #29** (第 1128 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppehf6h_0TempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #30** (第 1152 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaeyr_qrsTempValidation.java:4: 错误: 找不到符号
KafkaSink<String> sink = KafkaSink.<String>builder()
^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #35** (第 1318 行, 语言: sql)

- **错误**: 可能的语法问题: -- ICEBERG V2 流式增量读取
SET 'EXECUTION.RUNTIME-MODE' ...

**问题 #36** (第 1337 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG FLUSS_CATALOG;...

**问题 #39** (第 1481 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo95qmizwTempValidation.java:4: 错误: 找不到符号
TableResult result = tableEnv.executeSql(""
^
  符号:   类 TableResult
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #40** (第 1501 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx581tlusTempValidation.java:4: 错误: 找不到符号
Properties consumerConfig = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #43** (第 1590 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 66, column 13:
          filter: id > 0
                ^ (line: 66)
- **错误行**: 66
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Flink\05-ecosystem\05.01-connectors\flink-cdc-3.6.0-guide.md`

**问题 #10** (第 412 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    transform:
    ^ (line: 2)
found duplicate key "transform" with value "[]" (original value: "[]")
  in "<unicode string>",
- **错误行**: 2


### `Flink\05-ecosystem\05.01-connectors\flink-connectors-ecosystem-complete-guide.md`

**问题 #3** (第 154 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmhbpjd7lSource.java:2: 错误: 找不到符号
    extends SourceReaderFactory<T, SplitT> {
            ^
  符号: 类 SourceReaderFactory
C:\Users\luyan\AppData\Local\Temp\tmpmhbpjd
- **错误行**: 2

**问题 #4** (第 190 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn4wb986nSink.java:3: 错误: 找不到符号
    SinkWriter<InputT> createWriter(InitContext context);
                                    ^
  符号:   类 InitContext
  位置: 接口 Sink<
- **错误行**: 3

**问题 #22** (第 801 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpit6to6pdTempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #23** (第 822 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1_a_b9y9TempValidation.java:4: 错误: 找不到符号
KafkaSink<String> sink = KafkaSink.<String>builder()
^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #25** (第 867 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpubroahchTempValidation.java:4: 错误: 找不到符号
PulsarSource<String> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #26** (第 889 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpebxxsocjTempValidation.java:4: 错误: 找不到符号
PulsarSink<String> sink = PulsarSink.builder()
^
  符号:   类 PulsarSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #28** (第 919 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpua3t9zjxTempValidation.java:4: 错误: 找不到符号
RMQConnectionConfig connectionConfig = new RMQConnectionConfig.Builder()
^
  符号:   类 RMQConnectionConfig
  位置: 类 TempValid
- **错误行**: 4

**问题 #30** (第 965 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpovp2uts4TempValidation.java:4: 错误: 找不到符号
Properties consumerConfig = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #31** (第 988 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg_plooyjTempValidation.java:4: 错误: 找不到符号
Properties producerConfig = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #33** (第 1025 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv1vyz41uTempValidation.java:4: 错误: 找不到符号
DeserializationSchema<String> deserializer = new SimpleStringSchema();
^
  符号:   类 DeserializationSchema
  位置: 类 TempValid
- **错误行**: 4

**问题 #35** (第 1065 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqs3gvs2pTempValidation.java:4: 错误: 找不到符号
MQTTSource<String> source = MQTTSource.<String>builder()
^
  符号:   类 MQTTSource
  位置: 类 TempValidation
C:\Users\luyan\AppD
- **错误行**: 4

**问题 #36** (第 1115 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_9ixj62gTempValidation.java:4: 错误: 找不到符号
FileSystem fs = FileSystem.get(new URI("s3://my-bucket/data"));
^
  符号:   类 FileSystem
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #37** (第 1135 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxuj6xcziTempValidation.java:4: 错误: 找不到符号
FileSource<Row> source = FileSource.forRecordStreamFormat(
^
  符号:   类 FileSource
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #38** (第 1151 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgtfmbv4vTempValidation.java:4: 错误: 找不到符号
Schema schema = new Schema.Parser().parse(
^
  符号:   类 Schema
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #39** (第 1169 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphv3ksictTempValidation.java:4: 错误: 找不到符号
final StreamingFileSink<Row> sink = StreamingFileSink
      ^
  符号:   类 StreamingFileSink
  位置: 类 TempValidation
C:\Users\
- **错误行**: 4

**问题 #40** (第 1190 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpimwat4wtTempValidation.java:4: 错误: 找不到符号
FileSink<Row> sink = FileSink.forBulkFormat(
^
  符号:   类 FileSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #42** (第 1234 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppc2alp2yTempValidation.java:4: 错误: 找不到符号
JdbcSource<Row> source = JdbcSource.<Row>builder()
^
  符号:   类 JdbcSource
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 4

**问题 #43** (第 1255 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6wtqchhuTempValidation.java:4: 错误: 找不到符号
JdbcExactlyOnceSink<Row> sink = JdbcExactlyOnceSink.sink(
^
  符号:   类 JdbcExactlyOnceSink
  位置: 类 TempValidation
C:\Users\
- **错误行**: 4

**问题 #46** (第 1333 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpebkcx7p_TempValidation.java:4: 错误: 找不到符号
ClusterBuilder clusterBuilder = new ClusterBuilder() {
^
  符号:   类 ClusterBuilder
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #48** (第 1373 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq90vynpbTempValidation.java:4: 错误: 找不到符号
HBaseSourceFunction<Row> source = new HBaseSourceFunction<>(
^
  符号:   类 HBaseSourceFunction
  位置: 类 TempValidation
C:\Use
- **错误行**: 4

**问题 #50** (第 1415 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqfxfkvkqTempValidation.java:4: 错误: 找不到符号
List<HttpHost> httpHosts = Arrays.asList(
^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpqfx
- **错误行**: 4

**问题 #52** (第 1458 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjsrcw3d3TempValidation.java:4: 错误: 找不到符号
MongoSource<String> source = MongoSource.<String>builder()
^
  符号:   类 MongoSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #54** (第 1503 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmyh3qgnpTempValidation.java:4: 错误: 找不到符号
FlinkJedisPoolConfig conf = new FlinkJedisPoolConfig.Builder()
^
  符号:   类 FlinkJedisPoolConfig
  位置: 类 TempValidation
C:\
- **错误行**: 4

**问题 #56** (第 1555 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv3rw821iTempValidation.java:4: 错误: 找不到符号
InfluxDBSink<String> sink = InfluxDBSink.builder()
^
  符号:   类 InfluxDBSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 4

**问题 #58** (第 1595 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp127ukvkpTempValidation.java:4: 错误: 找不到符号
CatalogLoader catalogLoader = CatalogLoader.hive(
^
  符号:   类 CatalogLoader
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 4

**问题 #59** (第 1612 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG ICEBERG_CATALOG;...

**问题 #60** (第 1648 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp65mzufauTempValidation.java:4: 错误: 找不到符号
Table table = catalog.loadTable(TableIdentifier.of("db", "user_events"));
^
  符号:   类 Table
  位置: 类 TempValidation
C:\User
- **错误行**: 4

**问题 #64** (第 1722 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_CATALOG;...

**问题 #66** (第 1768 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjtc0b1j5TempValidation.java:4: 错误: 找不到符号
DeltaSink<Row> deltaSink = DeltaSink
^
  符号:   类 DeltaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpjtc
- **错误行**: 4

**问题 #68** (第 1798 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG FLUSS_CATALOG;...

**问题 #70** (第 1838 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqh8hvxg6TempValidation.java:4: 错误: 找不到符号
MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
^
  符号:   类 MySqlSource
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #79** (第 2299 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl6zoub8wTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000, CheckpointingMode.EXACTLY_ONCE);
                               ^
  符号:   变量 CheckpointingM
- **错误行**: 4

**问题 #80** (第 2315 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj4c8q13nTempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `Flink\05-ecosystem\05.01-connectors\flink-delta-lake-integration.md`

**问题 #11** (第 414 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5vgi684xTempValidation.java:4: 错误: 非法的表达式开始
public void notifyCheckpointComplete(long checkpointId) {
^
C:\Users\luyan\AppData\Local\Temp\tmp5vgi684xTempValidation
- **错误行**: 4

**问题 #16** (第 514 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplr9pl5ueTempValidation.java:3: 错误: 找不到符号
        DeltaSource<RowData> deltaSource = DeltaSource
        ^
  符号:   类 DeltaSource
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 3

**问题 #17** (第 531 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp56duqeilTempValidation.java:3: 错误: 找不到符号
        DeltaSource<RowData> streamingSource = DeltaSource
        ^
  符号:   类 DeltaSource
  位置: 类 TempValidation
C:\Users
- **错误行**: 3

**问题 #18** (第 547 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6ws4wtruTempValidation.java:3: 错误: 找不到符号
        DeltaSink<RowData> deltaSink = DeltaSink
        ^
  符号:   类 DeltaSink
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3

**问题 #19** (第 563 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcbay5g9nTempValidation.java:3: 错误: 找不到符号
        env.enableCheckpointing(60000);
        ^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 3

**问题 #21** (第 623 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0elb6i0bTempValidation.java:3: 错误: 找不到符号
        PostgresSource<String> pgSource = PostgresSource.<String>builder()
        ^
  符号:   类 PostgresSource
  位置: 类 Temp
- **错误行**: 3

**问题 #23** (第 662 行, 语言: sql)

- **错误**: 可能的语法问题: -- 流式查询
SET 'EXECUTION.RUNTIME-MODE' = 'STREAMING'...; 可能的语法问题: -- 批处理查询
SET 'EXECUTION.RUNTIME-MODE' = 'BATCH';...

**问题 #32** (第 821 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgjuuqru9TempValidation.java:3: 错误: 找不到符号
        conf.set("delta.logRetentionDuration", "interval 30 days");
        ^
  符号:   变量 conf
  位置: 类 TempValidation
C:\Us
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\flink-elasticsearch-connector-guide.md`

**问题 #12** (第 322 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjv2phklpTempValidation.java:5: 错误: 不是语句
  "mappings": {
  ^
C:\Users\luyan\AppData\Local\Temp\tmpjv2phklpTempValidation.java:5: 错误: 需要';'
  "mappings": {

- **错误行**: 5

**问题 #17** (第 551 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1qchi17pTempValidation.java:40: 错误: 找不到符号
tableEnv.executeSql(createTableSQL);
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp1q
- **错误行**: 40

**问题 #19** (第 682 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3a16p2q3TempValidation.java:4: 错误: 程序包ElasticsearchSink不存在
ElasticsearchSink.Builder<Event> builder =
                 ^
C:\Users\luyan\AppData\Local\Temp\tmp3a16p
- **错误行**: 4

**问题 #24** (第 865 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphvclba3nTempValidation.java:4: 错误: 找不到符号
builder.setBulkFlushMaxActions(500);   // 从 1000 降低
^
  符号:   变量 builder
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #26** (第 899 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_jcn3fzvTempValidation.java:4: 错误: 找不到符号
String docId = event.getOrderId() + "_" + event.getTimestamp();
               ^
  符号:   变量 event
  位置: 类 TempValidation
C
- **错误行**: 4

**问题 #30** (第 971 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsd94o8p_TempValidation.java:4: 错误: 非法的表达式开始
public String sanitizeJson(Event event) {
^
C:\Users\luyan\AppData\Local\Temp\tmpsd94o8p_TempValidation.java:22: 错误: 需要
- **错误行**: 4

**问题 #32** (第 1052 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkog00asrTempValidation.java:4: 错误: 找不到符号
env.getConfig().enableObjectReuse();
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpkog00asr
- **错误行**: 4


### `Flink\05-ecosystem\05.01-connectors\flink-iceberg-integration.md`

**问题 #27** (第 913 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG ICEBERG_CATALOG;...; 可能的语法问题: USE ECOMMERCE;...

**问题 #29** (第 1002 行, 语言: sql)

- **错误**: 可能的语法问题: -- 启用 UPSERT 模式写入 ICEBERG
SET 'EXECUTION.CHECKPOIN...

**问题 #30** (第 1039 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...

**问题 #35** (第 1413 行, 语言: sql)

- **错误**: 可能的语法问题: -- 注意：分区演进是增量式的，历史数据保持原分区，新数据使用新分区策略...

**问题 #37** (第 1485 行, 语言: sql)

- **错误**: 可能的语法问题: -- 强制 COMPACTION（合并 DELETE 文件）
CALL ICEBERG_CATALO...

**问题 #43** (第 1737 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbmrcn4wdTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);  // 60s
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpbmrcn
- **错误行**: 4

**问题 #45** (第 1784 行, 语言: sql)

- **错误**: 可能的语法问题: -- 重写数据文件（合并小文件）
CALL ICEBERG_CATALOG.SYSTEM.REWRI...; 可能的语法问题: -- 按分区压缩
CALL ICEBERG_CATALOG.SYSTEM.REWRITE_DATA_...

**问题 #47** (第 1844 行, 语言: sql)

- **错误**: 可能的语法问题: -- 手动触发过期
CALL ICEBERG_CATALOG.SYSTEM.EXPIRE_SNAPS...


### `Flink\05-ecosystem\05.01-connectors\flink-jdbc-connector-guide.md`

**问题 #14** (第 390 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgpq7v1xtTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.connector.jdbc.*;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpgpq7v1xtTempValidation
- **错误行**: 3

**问题 #15** (第 432 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3mwbgbk2TempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql("""
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp3mwbgbk2TempVali
- **错误行**: 4

**问题 #17** (第 536 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpttaguq3nTempValidation.java:4: 错误: 找不到符号
JdbcExactlyOnceSink<Order> xaSink = JdbcExactlyOnceSink
^
  符号:   类 JdbcExactlyOnceSink
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #22** (第 683 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8_0b8rowTempValidation.java:4: 错误: 找不到符号
config.setMaximumPoolSize(sinkParallelism + 5);
                          ^
  符号:   变量 sinkParallelism
  位置: 类 TempValidat
- **错误行**: 4

**问题 #24** (第 711 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphd522izmTempValidation.java:18: 错误: 需要';'
SET GLOBAL innodb_lock_wait_timeout = 50;
          ^
C:\Users\luyan\AppData\Local\Temp\tmphd522izmTempValidation.java:19
- **错误行**: 18

**问题 #26** (第 749 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb9bglsb7TempValidation.java:8: 错误: 需要';'
SET GLOBAL innodb_rollback_on_timeout = ON;
          ^
C:\Users\luyan\AppData\Local\Temp\tmpb9bglsb7TempValidation.java:9
- **错误行**: 8

**问题 #29** (第 799 行, 语言: sql)

- **错误**: 可能的语法问题: -- MYSQL: 查看当前连接
SHOW PROCESSLIST;...; 可能的语法问题: -- 查看 XA 事务
XA RECOVER;...

**问题 #30** (第 835 行, 语言: sql)

- **错误**: 可能的语法问题: -- 启用二进制日志（CDC 必需）
SET GLOBAL BINLOG_FORMAT = 'ROW...; 可能的语法问题: -- 优化 INNODB
SET GLOBAL INNODB_BUFFER_POOL_SIZE = ...

**问题 #31** (第 848 行, 语言: sql)

- **错误**: 可能的语法问题: -- 优化写入性能
SET SYNCHRONOUS_COMMIT = OFF;...; 可能的语法问题: --  PREPARED TRANSACTIONS FOR XA
SET MAX_PREPARED_...


### `Flink\05-ecosystem\05.01-connectors\flink-mongodb-connector-guide.md`

**问题 #15** (第 357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvsa11zokTempValidation.java:4: 错误: 找不到符号
DataStream<ChangeEvent> events = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpvs
- **错误行**: 4

**问题 #17** (第 403 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbrasu5irTempValidation.java:4: 错误: 找不到符号
ReplaceOneModel<Document> replace = new ReplaceOneModel<>(
^
  符号:   类 ReplaceOneModel
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #25** (第 674 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_w_mtptuTempValidation.java:5: 错误: 找不到符号
tableEnv.executeSql("""
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp_w_mtptuTempVali
- **错误行**: 5

**问题 #33** (第 962 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpidde4wbmTempValidation.java:4: 错误: 找不到符号
ReplaceOneModel<Document> replace = new ReplaceOneModel<>(
^
  符号:   类 ReplaceOneModel
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #35** (第 999 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyehv0ixtTempValidation.java:4: 错误: 找不到符号
MongoClientSettings settings = MongoClientSettings.builder()
^
  符号:   类 MongoClientSettings
  位置: 类 TempValidation
C:\Use
- **错误行**: 4

**问题 #37** (第 1036 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2s7amygxMyClassCodec.java:23: 错误: 未命名类 是预览功能，默认情况下禁用。
CodecRegistry customCodecRegistry = CodecRegistries.fromCodecs(
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 23

**问题 #39** (第 1115 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplmnyvke1TempValidation.java:4: 错误: 找不到符号
FindIterable<Document> iterable = collection
^
  符号:   类 FindIterable
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #40** (第 1137 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk5cr2ipeTempValidation.java:4: 错误: 找不到符号
BulkWriteOptions options = new BulkWriteOptions()
^
  符号:   类 BulkWriteOptions
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #41** (第 1163 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp74k8qcyrTempValidation.java:4: 错误: 找不到符号
MongoChangeStreamSource<ChangeEvent> source =
^
  符号:   类 MongoChangeStreamSource
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4


### `Flink\05-ecosystem\05.01-connectors\flink-paimon-integration.md`

**问题 #13** (第 726 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_PROD;...

**问题 #14** (第 767 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...; 可能的语法问题: -- 模式2: 从最早快照开始消费
SET 'SCAN.MODE' = 'EARLIEST';...

**问题 #18** (第 999 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...

**问题 #20** (第 1077 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看所有 TAG
SHOW TAGS FOR TABLE PAIMON_USERS;...


### `Flink\05-ecosystem\05.01-connectors\jdbc-connector-complete-guide.md`

**问题 #10** (第 393 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa10g25p5TempValidation.java:4: 错误: 非法的表达式开始
.setProperty("useSSL", "false")
^
C:\Users\luyan\AppData\Local\Temp\tmpa10g25p5TempValidation.java:14: 错误: 需要';'
.setPr
- **错误行**: 4

**问题 #17** (第 663 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplrg2pxxoTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.connector.jdbc.source.JdbcSource;
        ^
C:\Users\luyan\AppData\Local\Temp\tmplrg2px
- **错误行**: 3

**问题 #18** (第 695 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzqcdyc_sTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.source.JdbcSource;
^
C:\Users\luyan\AppData\Local\Temp\tmpzqcdyc_sTempValidation
- **错误行**: 3

**问题 #19** (第 734 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvt4bh5ksTempValidation.java:4: 错误: 找不到符号
JdbcSource<MyRecord> incrementalSource = JdbcSource.<MyRecord>builder()
^
  符号:   类 JdbcSource
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #20** (第 758 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbsloppdpTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcSink;
^
C:\Users\luyan\AppData\Local\Temp\tmpbsloppdpTempValidation.java:3:
- **错误行**: 3

**问题 #21** (第 793 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb5oclqp7TempValidation.java:29: 错误: 非法的表达式开始
);
^
1 个错误

- **错误行**: 29

**问题 #22** (第 825 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnltefdp9TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcExactlyOnceOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmpnltefdp9TempValid
- **错误行**: 3

**问题 #23** (第 864 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_5zio2ckTempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp_5
- **错误行**: 4

**问题 #24** (第 886 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpou3bkct4TempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpou
- **错误行**: 4

**问题 #25** (第 905 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_080sfa6TempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp_0
- **错误行**: 4

**问题 #26** (第 925 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvrsxfhtwTempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpvr
- **错误行**: 4

**问题 #27** (第 960 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps95sgc6bTempValidation.java:4: 错误: 找不到符号
JdbcExecutionOptions executionOptions = JdbcExecutionOptions.builder()
^
  符号:   类 JdbcExecutionOptions
  位置: 类 TempValida
- **错误行**: 4

**问题 #29** (第 1020 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_owejy0sTempValidation.java:10: 错误: 已在方法 main(String[])中定义了变量 url
String url = "jdbc:postgresql://localhost:5432/mydb" +
       ^
1 个错误

- **错误行**: 10

**问题 #30** (第 1050 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8s9y7obfTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcExecutionOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmp8s9y7obfTempValidat
- **错误行**: 3

**问题 #31** (第 1098 行, 语言: sql)

- **错误**: 可能的语法问题: -- MYSQL: 查看当前连接
SHOW PROCESSLIST;...

**问题 #32** (第 1112 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3o38skj7TempValidation.java:4: 错误: 找不到符号
HikariConfig config = new HikariConfig();
^
  符号:   类 HikariConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #33** (第 1143 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiw6rk5xcTempValidation.java:9: 错误: 找不到符号
JdbcSource<MyRecord> source = JdbcSource.<MyRecord>builder()
^
  符号:   类 JdbcSource
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 9

**问题 #34** (第 1180 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmqd5lndsTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);  // 1分钟，不要太短
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4


### `Flink\05-ecosystem\05.01-connectors\kafka-integration-patterns.md`

**问题 #1** (第 300 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzces7vc9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #2** (第 325 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd9am47hvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.connector.base.DeliveryGuarantee;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpd9am47
- **错误行**: 3

**问题 #3** (第 347 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbdp8z1eeTempValidation.java:4: 错误: 找不到符号
KafkaSource<UserEvent> source = KafkaSource.<UserEvent>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 4

**问题 #10** (第 712 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3p7ip6jxTempValidation.java:4: 错误: 找不到符号
properties.setProperty(
^
  符号:   变量 properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp3p7ip6jxTempVa
- **错误行**: 4


### `Flink\05-ecosystem\05.01-connectors\mongodb-connector-complete-guide.md`

**问题 #12** (第 715 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw5jpakihTempValidation.java:4: 错误: 找不到符号
MongoSink<Document> updateSink = MongoSink.<Document>builder()
^
  符号:   类 MongoSink
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4


### `Flink\05-ecosystem\05.01-connectors\pulsar-integration-guide.md`

**问题 #3** (第 205 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp944v2yp4TempValidation.java:4: 错误: 找不到符号
PulsarSource<String> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #4** (第 223 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn1rqgy75TempValidation.java:4: 错误: 找不到符号
PulsarSink<String> sink = PulsarSink.builder()
^
  符号:   类 PulsarSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #9** (第 361 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy5iqams6EnrichedStreamProcessing.java:13: 错误: 非法的表达式开始
            .setDeserializationSchema(...)
                                      ^
C:\Users\luyan\AppData\Lo
- **错误行**: 13

**问题 #10** (第 392 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8bp0iktgTempValidation.java:4: 错误: 找不到符号
PulsarSource<String> optimizedSource = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #11** (第 430 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3x6d2hl5SchemaEvolutionExample.java:21: 错误: 非法的表达式开始
        DataStream<EventV2> stream = env.fromSource(source, ...)

- **错误行**: 21


### `Flink\05-ecosystem\05.02-lakehouse\flink-iceberg-integration.md`

**问题 #29** (第 950 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG ICEBERG_CATALOG;...; 可能的语法问题: USE ECOMMERCE;...

**问题 #30** (第 1001 行, 语言: sql)

- **错误**: 可能的语法问题: -- 使用 UPSERT 模式处理 CDC 变更
SET 'EXECUTION.CHECKPOINT...

**问题 #31** (第 1062 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...

**问题 #36** (第 1464 行, 语言: sql)

- **错误**: 可能的语法问题: -- 在分支上写入数据（不影响主线）
SET 'ICEBERG.CATALOG.DEFAULT-BR...

**问题 #38** (第 1533 行, 语言: sql)

- **错误**: 可能的语法问题: -- 注意：分区演进是增量式的，历史数据保持原分区，新数据使用新分区策略...

**问题 #39** (第 1562 行, 语言: sql)

- **错误**: 可能的语法问题: -- 强制 COMPACTION（合并 DELETE 文件）
CALL ICEBERG_CATALO...

**问题 #46** (第 1860 行, 语言: sql)

- **错误**: 可能的语法问题: -- 阶段 4: 数据一致性验证
-- 对比 HIVE 和 ICEBERG 表的记录数、SUM(AM...


### `Flink\05-ecosystem\05.02-lakehouse\flink-paimon-integration.md`

**问题 #14** (第 747 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_PROD;...

**问题 #15** (第 786 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...; 可能的语法问题: -- 模式2: 从最早快照开始消费
SET 'SCAN.MODE' = 'EARLIEST';...

**问题 #16** (第 828 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...

**问题 #23** (第 1167 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看所有 TAG
SHOW TAGS FOR TABLE PAIMON_USERS;...

**问题 #24** (第 1205 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...

**问题 #31** (第 1551 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...


### `Flink\05-ecosystem\05.02-lakehouse\streaming-lakehouse-architecture.md`

**问题 #25** (第 879 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG ICEBERG_CATALOG;...; 可能的语法问题: USE REALTIME_DW;...; 可能的语法问题: -- ============================================
--...

**问题 #26** (第 1040 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_CATALOG;...


### `Flink\05-ecosystem\05.02-lakehouse\streaming-lakehouse-deep-dive-2026.md`

**问题 #35** (第 1169 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_PROD;...; 可能的语法问题: USE ECOMMERCE;...; 可能的语法问题: -- ============================================
--...

**问题 #36** (第 1441 行, 语言: yaml)

- **错误**: while scanning a simple key
  in "<unicode string>", line 59, column 1:
    spark.sql.catalog.polaris=org.ap ...
    ^ (line: 59)
could not find expected ':'
  in "<unicode string>", line 60, column
- **错误行**: 59


### `Flink\05-ecosystem\05.03-wasm-udf\wasi-0.3-async-preview.md`

**问题 #26** (第 1193 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp57725dl8TempValidation.java:5: 错误: 需要';'
public void testCancellation() throws Exception {
                            ^
C:\Users\luyan\AppData\Local\Temp\tmp57725
- **错误行**: 5


### `Flink\05-ecosystem\05.04-graph\flink-gelly-streaming-graph-processing.md`

**问题 #3** (第 262 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp39m6jxchTempValidation.java:4: 错误: 找不到符号
DataStream<Edge<Long, Double>> tweetEdges = tweets
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 4

**问题 #4** (第 302 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpymkk20a0TempValidation.java:4: 错误: 找不到符号
DataStream<Edge<String, TransactionInfo>> txEdges = transactions
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #5** (第 337 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpshgcbt1kVertexState.java:10: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Edge<Long, Double>> edgeStream = ...;
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Lo
- **错误行**: 10

**问题 #6** (第 424 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdwc99ldyTempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend rocksDbBackend = new RocksDBStateBackend(
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempValidation
C:\Us
- **错误行**: 4


### `Flink\05-ecosystem\05.04-graph\flink-gelly.md`

**问题 #3** (第 166 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyfbyo7n3TempValidation.java:4: 错误: 找不到符号
Graph<Long, Double, Double> bipartiteGraph = Graph.fromDataSet(
^
  符号:   类 Graph
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #4** (第 197 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmnh0b2avTempValidation.java:4: 错误: 非法的表达式开始
Graph<String, AccountInfo, Transaction> transactionGraph = ...;

- **错误行**: 4

**问题 #5** (第 218 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph22szvw6TempValidation.java:4: 错误: 找不到符号
DataStream<Graph<String, AccountInfo, Transaction>> timeSliceGraphs =
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Use
- **错误行**: 4


### `Flink\05-ecosystem\ecosystem\kafka-streams-migration.md`

**问题 #2** (第 69 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyowihs02TempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #3** (第 76 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqhcq_3l0TempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env =
        ^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3

**问题 #4** (第 97 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9ey6bdodTempValidation.java:3: 错误: 找不到符号
        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);
        ^
  符号:   类 StreamTableEnvironment

- **错误行**: 3

**问题 #5** (第 119 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphgf2p0dcTempValidation.java:3: 错误: 找不到符号
        KStream<String, Integer> transformed = stream
        ^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3

**问题 #6** (第 129 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0pdzc6u9TempValidation.java:3: 错误: 找不到符号
        DataStream<Tuple2<String, Integer>> transformed = stream
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\
- **错误行**: 3

**问题 #7** (第 139 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjf5stfaoTempValidation.java:3: 错误: 找不到符号
        Table transformed = tableEnv.from("input_table")
        ^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 3

**问题 #8** (第 155 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcxy4rm2rTempValidation.java:3: 错误: 找不到符号
        KTable<String, Long> counts = stream
        ^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 3

**问题 #9** (第 163 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5zhxvaxpTempValidation.java:3: 错误: 找不到符号
DataStream<Tuple2<String, Long>> counts = stream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 3

**问题 #10** (第 198 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpih3dv7a_TempValidation.java:3: 错误: 找不到符号
        KStream<String, String> joined = stream1.join(
        ^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 3

**问题 #11** (第 209 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6rxmiwj7TempValidation.java:3: 错误: 找不到符号
        DataStream<String> joined = stream1
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 3

**问题 #12** (第 220 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9iiyng2_TempValidation.java:3: 错误: 找不到符号
        Table joined = table1
        ^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp9iiyng
- **错误行**: 3

**问题 #16** (第 308 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgsmsl3_2TempValidation.java:3: 错误: 找不到符号
        properties.put(StreamsConfig.NUM_STREAM_THREADS_CONFIG, 4);
                       ^
  符号:   变量 StreamsConfig
  位置
- **错误行**: 3

**问题 #17** (第 314 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnccaqjg_TempValidation.java:6: 错误: 非法的表达式开始
stream.map(...).setParallelism(2);
           ^
1 个错误

- **错误行**: 6

**问题 #18** (第 325 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjscymf5pTempValidation.java:3: 错误: 找不到符号
        properties.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG,
                       ^
  符号:   变量 StreamsConfig
  位置:
- **错误行**: 3

**问题 #19** (第 333 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnug4e9w3TempValidation.java:3: 错误: 找不到符号
        env.enableCheckpointing(100);  // 100ms
        ^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 3

**问题 #20** (第 352 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpitakh9mvTempValidation.java:4: 错误: 需要';'
public void testTopology() {
                        ^
C:\Users\luyan\AppData\Local\Temp\tmpitakh9mvTempValidation.java:8:
- **错误行**: 4

**问题 #21** (第 370 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbppl8s60TempValidation.java:4: 错误: 需要';'
public void testPipeline() throws Exception {
                        ^
C:\Users\luyan\AppData\Local\Temp\tmpbppl8s60TempV
- **错误行**: 4

**问题 #22** (第 392 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7t94talhTempValidation.java:4: 错误: 需要';'
public void testMigrationParity() {
                               ^
1 个错误

- **错误行**: 4


### `Flink\05-ecosystem\ecosystem\materialize-comparison.md`

**问题 #4** (第 110 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnyr6j9f0TempValidation.java:4: 错误: 找不到符号
DataStream<Event> stream = env.addSource(kafkaSource);
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #5** (第 125 行, 语言: sql)

- **错误**: 可能的语法问题: -- AUTOMATIC MAINTENANCE, AUTOMATIC INDEXING...

**问题 #10** (第 310 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp096386vcTempValidation.java:4: 错误: 找不到符号
DataStream<Result> result = stream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp0963
- **错误行**: 4


### `Flink\05-ecosystem\ecosystem\pulsar-functions-integration.md`

**问题 #2** (第 73 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzewqhm0uTempValidation.java:7: 错误: 找不到符号
PulsarSource<String> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 7

**问题 #3** (第 97 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp941qjwubTempValidation.java:3: 错误: 找不到符号
        PulsarSink<String> sink = PulsarSink.builder()
        ^
  符号:   类 PulsarSink
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 3

**问题 #9** (第 233 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjwe66odnTempValidation.java:4: 错误: 找不到符号
Schema<OrderEvent> schema = Schema.AVRO(OrderEvent.class);
^
  符号:   类 Schema
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #10** (第 244 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsim5o7xgTempValidation.java:4: 错误: 找不到符号
PulsarSource<OrderEvent> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #11** (第 261 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmio9prmkTempValidation.java:3: 错误: 找不到符号
        env.enableCheckpointing(5000);
        ^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 3

**问题 #12** (第 275 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8r41d6jpTempValidation.java:4: 错误: 找不到符号
PulsarSource<String> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4


### `Flink\05-ecosystem\ecosystem\risingwave-integration-guide.md`

**问题 #2** (第 80 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp48m_ldzmTempValidation.java:4: 错误: 找不到符号
JdbcSink.sink(
^
  符号:   变量 JdbcSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp48m_ldzmTempValidation.ja
- **错误行**: 4

**问题 #4** (第 124 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3v035ngtTempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp3v
- **错误行**: 4

**问题 #8** (第 241 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuyj7gvqkTempValidation.java:4: 错误: 找不到符号
TwoPhaseCommitSinkFunction<Event, JdbcConnection, Void> exactlyOnceSink =
^
  符号:   类 TwoPhaseCommitSinkFunction
  位置: 类 T
- **错误行**: 4

**问题 #9** (第 278 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpno0y8dwvTempValidation.java:4: 错误: 找不到符号
JdbcExecutionOptions executionOptions = JdbcExecutionOptions.builder()
^
  符号:   类 JdbcExecutionOptions
  位置: 类 TempValida
- **错误行**: 4

**问题 #12** (第 356 行, 语言: sql)

- **错误**: 可能的语法问题: -- PROCESS IN FLINK
TABLE PROCESSED = TABLEENV.SQL...; 可能的语法问题: -- SINK TO RISINGWAVE
TABLEENV.EXECUTESQL(
    "CR...; 可能的语法问题: PROCESSED.EXECUTEINSERT("RISINGWAVE_SINK");...


### `Flink\06-ai-ml\ai-agent-flink-deep-integration.md`

**问题 #7** (第 385 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpouzszfe7TempValidation.java:4: 错误: 找不到符号
Pattern<AgentEvent, ?> complexDecision = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #8** (第 401 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmper9d_ksbCustomerSupportAgent.java:342: 错误: 非法的表达式开始
            .addSource(new KafkaSource<Query>(...))
                                              ^
C:\Users\lu
- **错误行**: 342

**问题 #9** (第 767 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 212


### `Flink\06-ai-ml\ai-ml\evolution\a2a-protocol.md`

**问题 #1** (第 47 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg2lcoi4dTempValidation.java:3: 错误: 找不到符号
        A2AMessage msg = A2AMessage.builder()
        ^
  符号:   类 A2AMessage
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 3

**问题 #2** (第 59 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph1d5hgudTempValidation.java:3: 错误: 找不到符号
        agent1.delegate(task, agent2);
                        ^
  符号:   变量 task
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 3


### `Flink\06-ai-ml\ai-ml\evolution\ai-agent-24.md`

**问题 #2** (第 45 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4gq422uaTempValidation.java:3: 错误: 找不到符号
        Agent agent = Agent.newBuilder()
        ^
  符号:   类 Agent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 3

**问题 #3** (第 56 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7c3k_lmcTempValidation.java:4: 错误: 找不到符号
    .addSink(new ActionSink());
                 ^
  符号:   类 ActionSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4


### `Flink\06-ai-ml\ai-ml\evolution\ai-agent-25.md`

**问题 #1** (第 47 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpknb5kw4aTempValidation.java:3: 错误: 找不到符号
        MultiAgentSystem system = MultiAgentSystem.builder()
        ^
  符号:   类 MultiAgentSystem
  位置: 类 TempValidation
C
- **错误行**: 3

**问题 #2** (第 58 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphmr3f07wTempValidation.java:3: 错误: 找不到符号
system.coordinate(event, (detector, diagnoser) -> {
                  ^
  符号:   变量 event
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 3


### `Flink\06-ai-ml\ai-ml\evolution\ai-agent-30.md`

**问题 #3** (第 58 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp30bxdglmTempValidation.java:4: 错误: 找不到符号
    .toSink(AlertSink.class);
            ^
  符号:   类 AlertSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4


### `Flink\06-ai-ml\ai-ml\evolution\feature-store.md`

**问题 #1** (第 46 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg5onhoyrTempValidation.java:3: 错误: 找不到符号
        FeatureVector fv = featureStore.getOnlineFeatures(entityId, features);
        ^
  符号:   类 FeatureVector
  位置: 类 T
- **错误行**: 3

**问题 #2** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_0pe92ssTempValidation.java:3: 错误: 找不到符号
stream.map(event -> {
^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp_0pe92ssTempValidati
- **错误行**: 3


### `Flink\06-ai-ml\ai-ml\evolution\llm-integration.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg6w502gvTempValidation.java:3: 错误: 找不到符号
llmClient.completeStream(prompt, token -> {
                         ^
  符号:   变量 prompt
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 3

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvnjo3eyyTempValidation.java:3: 错误: 找不到符号
        stream.map(new LLMMapFunction("gpt-4", promptTemplate));
                       ^
  符号:   类 LLMMapFunction
  位置: 类
- **错误行**: 3


### `Flink\06-ai-ml\ai-ml\evolution\ml-inference.md`

**问题 #1** (第 48 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9s8_bnqsTempValidation.java:3: 错误: 找不到符号
        SavedModelBundle model = SavedModelBundle.load("/path/to/model");
        ^
  符号:   类 SavedModelBundle
  位置: 类 Tem
- **错误行**: 3

**问题 #2** (第 57 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsc44hm0oTempValidation.java:4: 错误: 找不到符号
    .setParallelism(gpuCount);
                    ^
  符号:   变量 gpuCount
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4


### `Flink\06-ai-ml\ai-ml\evolution\model-serving.md`

**问题 #2** (第 45 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd_nc586aTempValidation.java:3: 错误: 找不到符号
        ModelRouter router = new ModelRouter()
        ^
  符号:   类 ModelRouter
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3

**问题 #3** (第 55 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa82pkutjTempValidation.java:3: 错误: 找不到符号
        ModelVersion version = registry.getLatest("fraud-detection");
        ^
  符号:   类 ModelVersion
  位置: 类 TempValidat
- **错误行**: 3


### `Flink\06-ai-ml\ai-ml\evolution\vector-search.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3yrb9zi9TempValidation.java:3: 错误: 找不到符号
        VectorIndex index = new HNSWIndex.Builder()
        ^
  符号:   类 VectorIndex
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 3

**问题 #2** (第 65 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpizv87ojhTempValidation.java:3: 错误: 找不到符号
        List<Vector> results = index.search(queryVector, 10);
        ^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 3


### `Flink\06-ai-ml\flink-25-gpu-acceleration.md`

**问题 #7** (第 479 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp772e1neTempValidation.java:5: 错误: 需要';'
public void testGPUSumAccuracy() {
                              ^
1 个错误

- **错误行**: 5

**问题 #15** (第 1040 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 7, column 42:
     ... flink:2.5-gpu-cuda12  <!-- 前瞻性镜像: Flink 2.5规划中 -->
                                         ^ (line: 7)
- **错误行**: 7
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Flink\06-ai-ml\flink-agent-workflow-engine.md`

**问题 #9** (第 1046 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp62n6bor3WorkflowBuilder.java:67: 错误: 未命名类 是预览功能，默认情况下禁用。
WorkflowDefinition workflow = WorkflowBuilder
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 67

**问题 #12** (第 1408 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1o3gh70kTempValidation.java:4: 错误: 找不到符号
WorkflowDefinition riskWorkflow = WorkflowBuilder
^
  符号:   类 WorkflowDefinition
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4


### `Flink\06-ai-ml\flink-agents-flip-531.md`

**问题 #5** (第 460 行, 语言: sql)

- **错误**: 可能的语法问题: -- DEF-F-12-30: FLINK AGENT DDL 定义

-- 注: 以下为未来可能的...


### `Flink\06-ai-ml\flink-ai-agents-flip-531.md`

**问题 #6** (第 285 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp482feo7bBadAgent.java:3: 错误: 找不到符号
    ListState<Message> allHistory;  // 永不清理！
    ^
  符号:   类 ListState
  位置: 类 BadAgent
C:\Users\luyan\AppData\Local\Temp\tmp482
- **错误行**: 3

**问题 #7** (第 300 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3iru663oTempValidation.java:4: 错误: 找不到符号
String response = llmClient.completeSync(prompt);  // 阻塞！
                                         ^
  符号:   变量 prompt
  位
- **错误行**: 4

**问题 #8** (第 311 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz1lwl2viTempValidation.java:5: 错误: 找不到符号
    generateLLMRequest();  // 可能压垮服务！
    ^
  符号:   方法 generateLLMRequest()
  位置: 类 TempValidation
1 个错误

- **错误行**: 5

**问题 #11** (第 505 行, 语言: sql)

- **错误**: 可能的语法问题: -- 创建AGENT
-- 注: 以下为未来可能的语法（概念设计阶段）
<!-- 以下语法为概念设计...; 可能的语法问题: -- 注册SQL工具
-- 注: 以下为未来可能的语法（概念设计阶段）
<!-- 以下语法为概念设计...; 可能的语法问题: -- 注册外部工具
-- 注: 以下为未来可能的语法（概念设计阶段）
~~CREATE TOOL S...; 可能的语法问题:

**问题 #12** (第 573 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpham79w4zTempValidation.java:4: 错误: 找不到符号
Agent salesAgent = Agent.builder()
^
  符号:   类 Agent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpham79w4zT
- **错误行**: 4


### `Flink\06-ai-ml\flink-ai-ml-integration-complete-guide.md`

**问题 #5** (第 183 行, 语言: sql)
- **错误**: 可能的语法问题: -- DEF-F-12-104A: 相似度函数
COSINE_SIMILARITY(U, V) = ...

**问题 #6** (第 196 行, 语言: sql)
- **错误**: 可能的语法问题: -- 模型定义语法（DEF-F-12-105A）
<!-- 以下语法为概念设计，实际 FLINK 版...

**问题 #10** (第 367 行, 语言: sql)
- **错误**: 可能的语法问题: <!-- 以下语法为概念设计，实际 FLINK 版本尚未支持 -->
-- ~~CREATE AGE...; 可能的语法问题: -- DEF-F-12-110B: CREATE TOOL语法（未来可能的语法，概念设计阶段）
--...; 可能的语法问题: -- DEF-F-12-110C: AGENT工作流语法
<!-- 以下语法为概念设计，实际 FLI...

**问题 #14** (第 681 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2dhwohafBadAgent.java:3: 错误: 找不到符号
    ListState<Message> allHistory;  // 永不清理！
    ^
  符号:   类 ListState
  位置: 类 BadAgent
C:\Users\luyan\AppData\Local\Temp\tmp2dh
- **错误行**: 3

**问题 #15** (第 705 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnjh0kbsvTempValidation.java:4: 错误: 找不到符号
String response = llmClient.completeSync(prompt);  // 阻塞！吞吐量受限
                                         ^
  符号:   变量 promp
- **错误行**: 4

**问题 #16** (第 716 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprylur9x4TempValidation.java:5: 错误: 找不到符号
    generateLLMRequest();  // 可能压垮LLM服务！
    ^
  符号:   方法 generateLLMRequest()
  位置: 类 TempValidation
1 个错误

- **错误行**: 5

**问题 #21** (第 1335 行, 语言: sql)
- **错误**: 可能的语法问题: -- ============================================
--...; 可能的语法问题: -- 步骤2: 创建技术支持AGENT
-- 注: 以下为未来可能的语法（概念设计阶段）
~~CRE...; 可能的语法问题: -- 步骤3: 注册SQL工具 - 查询订单
-- 注: 以下为未来可能的语法（概念设计阶段）
<!...; 可能的语法问题:

**问题 #22** (第 1591 行, 语言: sql)
- **错误**: 可能的语法问题: -- 步骤3: 创建嵌入模型
<!-- 以下语法为概念设计，实际 FLINK 版本尚未支持 -->
...; 可能的语法问题: -- 步骤4: 创建LLM模型
~~CREATE MODEL RAG_GENERATOR~~ (未来...

**问题 #24** (第 2019 行, 语言: sql)

- **错误**: 可能的语法问题: -- 步骤4: 创建不同成本的模型定义
~~CREATE MODEL GPT35_ECONOMY~~...; 可能的语法问题: ~~CREATE MODEL GPT4_STANDARD~~ (未来可能的语法)
WITH (
  ...

**问题 #38** (第 3023 行, 语言: sql)

- **错误**: 可能的语法问题: -- 创建AGENT
-- 注: 以下为未来可能的语法（概念设计阶段）
<!-- 以下语法为概念设计...; 可能的语法问题: -- 创建模型
~~CREATE MODEL <NAME>~~ WITH ('PROVIDER' =...

**问题 #39** (第 3053 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsbfjkj14TempValidation.java:4: 错误: 找不到符号
Agent agent = Agent.builder()
^
  符号:   类 Agent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpsbfjkj14TempVa
- **错误行**: 4


### `Flink\06-ai-ml\flink-llm-integration.md`

**问题 #1** (第 31 行, 语言: sql)
- **错误**: 可能的语法问题: <!-- 以下语法为概念设计，实际 FLINK 版本尚未支持 -->
~~CREATE MODEL~...

**问题 #2** (第 52 行, 语言: sql)

- **错误**: 可能的语法问题: ML_PREDICT(
  MODEL_NAME,           -- 模型名称 (STRIN...

**问题 #6** (第 288 行, 语言: sql)

- **错误**: 可能的语法问题: -- DEF-F-12-41: MODEL DDL 实例

-- OPENAI GPT-4 模型
~...; 可能的语法问题: -- 文本嵌入模型
~~CREATE MODEL TEXT_EMBEDDING_3~~ (未来可能的...; 可能的语法问题: -- 兼容 OLLAMA 本地模型
~~CREATE MODEL LOCAL_LLAMA~~ (未来...

**问题 #9** (第 364 行, 语言: sql)

- **错误**: 可能的语法问题: -- 实时客服消息情感分析
~~CREATE MODEL SENTIMENT_ANALYZER~~ ...

**问题 #12** (第 431 行, 语言: sql)

- **错误**: 可能的语法问题: -- 实时多语言翻译
~~CREATE MODEL TRANSLATOR~~ (未来可能的语法)
W...

**问题 #16** (第 631 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppc9rdq_lBatchLLMCaller.java:15: 错误: 未结束的字符文字
SET 'table.exec.async-lookup.buffer-capacity' = '100';
    ^
C:\Users\luyan\AppData\Local\Temp\tmppc9rdq_lBatchLLMCall
- **错误行**: 15

**问题 #20** (第 724 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6tpb7gh7PIIMaskingFunction.java:15: 错误: 需要 class、interface、enum 或 record
SELECT
^
C:\Users\luyan\AppData\Local\Temp\tmp6tpb7gh7PIIMaskingFunction.java:18: 错误: 未结束的
- **错误行**: 15


### `Flink\06-ai-ml\flink-llm-realtime-inference-guide.md`

**问题 #6** (第 238 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4lu3vr1bTempValidation.java:4: 错误: 找不到符号
String response = llmClient.complete(prompt);  // 阻塞!
                                     ^
  符号:   变量 prompt
  位置: 类 Tem
- **错误行**: 4

**问题 #7** (第 244 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeaxc1anaTempValidation.java:4: 错误: 找不到符号
CompletableFuture<String> future = llmClient.completeAsync(prompt);
^
  符号:   类 CompletableFuture
  位置: 类 TempValidation
C
- **错误行**: 4

**问题 #8** (第 254 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9n18qq6cTempValidation.java:4: 错误: 非法的表达式开始
public void processElement(Request req) {
^
C:\Users\luyan\AppData\Local\Temp\tmp9n18qq6cTempValidation.java:9: 错误: 需要
- **错误行**: 4

**问题 #9** (第 261 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1ft3vxagTempValidation.java:4: 错误: 非法的表达式开始
private ListState<Message> conversationHistory;
^
C:\Users\luyan\AppData\Local\Temp\tmp1ft3vxagTempValidation.java:16:
- **错误行**: 4

**问题 #10** (第 277 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaiw2jeadTempValidation.java:4: 错误: 找不到符号
String response = llmClient.complete(prompt);
                                     ^
  符号:   变量 prompt
  位置: 类 TempValidat
- **错误行**: 4

**问题 #11** (第 282 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvbq_z0e2TempValidation.java:4: 错误: 找不到符号
RetryPolicy<String> retryPolicy = RetryPolicy.<String>builder()
^
  符号:   类 RetryPolicy
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #14** (第 648 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 114

**问题 #20** (第 1116 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 10, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^ (line: 10)
- **错误行**: 10
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Flink\06-ai-ml\flink-llm-realtime-rag-architecture.md`

**问题 #6** (第 364 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzzpioucoRAGQueryService.java:63: 错误: 非法的表达式开始
            .map(new RichMapFunction<EnrichedQuery, LLMResponse>() {
            ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 63


### `Flink\06-ai-ml\flink-mcp-protocol-integration.md`

**问题 #8** (第 433 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8ul1dpnfTempValidation.java:4: 错误: 不是语句

1. 接收 MCP 调用请求 request = { name, arguments }
^
C:\Users\luyan\AppData\Local\Temp\tmp8ul1dpnfTempValidation.java:4: 错误: 需要';

- **错误行**: 4

**问题 #15** (第 1146 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps3m43o48McpEnrichmentFunction.java:86: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedEvent> enrichedStream = rawStream
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\lu
- **错误行**: 86

**问题 #16** (第 1247 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8of0gug3McpTableFunction.java:60: 错误: 未命名类 是预览功能，默认情况下禁用。
TableEnvironment tEnv = TableEnvironment.create(...);
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\
- **错误行**: 60

**问题 #27** (第 1804 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd_kfknhgTempValidation.java:4: 错误: 找不到符号
String sql = "SELECT * FROM " + tableName + " WHERE id = " + userInput;
                                ^
  符号:   变量 table
- **错误行**: 4


### `Flink\06-ai-ml\flink-ml-architecture.md`

**问题 #3** (第 228 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvjnlzfy7TempValidation.java:4: 错误: 非法的表达式开始
StreamExecutionEnvironment env = ...;
                                 ^
C:\Users\luyan\AppData\Local\Temp\tmpvjnlzfy7T
- **错误行**: 4


### `Flink\06-ai-ml\flink-realtime-ml-inference.md`

**问题 #3** (第 298 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbusgaif_TempValidation.java:13: 错误: 非法的表达式开始
AsyncDataStream.unorderedWait(...);
                              ^
1 个错误

- **错误行**: 13

**问题 #5** (第 361 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbenn88gxDriftDetectionFunction.java:8: 错误: 非法的表达式开始
        currentState.update(...);
                            ^
1 个错误

- **错误行**: 8

**问题 #7** (第 416 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7mjn8i5xTFServingAsyncFunction.java:51: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedEvent> scoredEvents = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以
- **错误行**: 51


### `Flink\06-ai-ml\flip-531-ai-agents-ga-guide.md`

**问题 #1** (第 88 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4xd8ksa4TempValidation.java:4: 错误: 找不到符号
EmbeddingConfiguration embedConfig = EmbeddingConfiguration.builder()
^
  符号:   类 EmbeddingConfiguration
  位置: 类 TempValid
- **错误行**: 4

**问题 #4** (第 189 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvkix2gwvTempValidation.java:4: 错误: 找不到符号
CompletableFuture<ToolResult> future = agent.executeToolAsync(
^
  符号:   类 CompletableFuture
  位置: 类 TempValidation
C:\Use
- **错误行**: 4


### `Flink\06-ai-ml\model-serving-streaming.md`

**问题 #3** (第 259 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcd87gf1hTFServingAsyncFunction.java:43: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Prediction> predictions = featureStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 43


### `Flink\06-ai-ml\online-learning-algorithms.md`

**问题 #6** (第 491 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphsw8t5skTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.ml.classification.logisticregression;
        ^
C:\Users\luyan\AppData\Local\Temp\tmphs
- **错误行**: 3

**问题 #15** (第 944 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa1ihg98lTempValidation.java:4: 错误: 找不到符号
Pattern<Metric, ?> driftPattern = Pattern.<Metric>begin("start")
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4


### `Flink\06-ai-ml\online-learning-production.md`

**问题 #3** (第 252 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeko8lbfwTempValidation.java:3: 错误: 找不到符号
        DataStream<Sample> trainingSamples = featureStream
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3


### `Flink\06-ai-ml\rag-streaming-architecture.md`

**问题 #3** (第 464 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdptvxb7pStreamingRAGPipeline.java:85: 错误: 非法的表达式开始
                .setRecordSerializer(...)
                                     ^
C:\Users\luyan\AppData\Local\Te
- **错误行**: 85


### `Flink\06-ai-ml\realtime-feature-engineering-feature-store.md`

**问题 #11** (第 489 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3m_bdh9_StreamFeatureJoin.java:10: 错误: 非法的表达式开始
            .addSource(new FlinkKafkaConsumer<>("clicks", ...));

- **错误行**: 10

**问题 #14** (第 699 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0_yrf6alRecommendationFeatureJob.java:10: 错误: 非法的表达式开始
            .addSource(new FlinkKafkaConsumer<>("user_events", ...));

- **错误行**: 10


### `Flink\06-ai-ml\vector-database-integration.md`

**问题 #1** (第 26 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz959hkjnVectorSink.java:2: 错误: 找不到符号
interface VectorSink<T> extends RichSinkFunction<T> {
                                ^
  符号: 类 RichSinkFunction
C:\Users\luya
- **错误行**: 2

**问题 #5** (第 266 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2zgk7qwkTempValidation.java:5: 错误: 找不到符号
List<VectorRecord> candidates = milvus.search(queryVector, topK=100);
^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 5

**问题 #8** (第 343 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjteikwemTempValidation.java:4: 错误: 需要';'
CREATE TABLE vector_items (
            ^
C:\Users\luyan\AppData\Local\Temp\tmpjteikwemTempValidation.java:5: 错误: 需要')'或',
- **错误行**: 4

**问题 #11** (第 450 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr_y_9he4MilvusLookupFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
TableResult result = tEnv.sqlQuery("""
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #13** (第 529 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfb4alzjqTempValidation.java:4: 错误: 找不到符号
DataStream<Recommendation> recommendations =
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `Flink\07-rust-native\ai-native-streaming\01-ai-native-architecture.md`

**问题 #8** (第 183 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpraygnlgjTempValidation.java:4: 错误: 找不到符号
OnlineLogisticRegression olr = new OnlineLogisticRegression()
^
  符号:   类 OnlineLogisticRegression
  位置: 类 TempValidation

- **错误行**: 4

**问题 #15** (第 396 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy6eloixrTempValidation.java:4: 错误: 找不到符号
DataStream<Feature> features = stream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpy
- **错误行**: 4


### `Flink\07-rust-native\arroyo-update\01-arroyo-cloudflare-acquisition.md`

**问题 #16** (第 523 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 11, column 1:
    curl -X POST "<[链接不完整 - 需手动修复]> ...
    ^ (line: 11)
- **错误行**: 11

**问题 #26** (第 905 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0jr2egqhTempValidation.java:3: 错误: 找不到符号
        DataStream<Event> stream = env
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 3


### `Flink\07-rust-native\flash-engine\05-flink-compatibility.md`

**问题 #23** (第 485 行, 语言: sql)

- **错误**: 可能的语法问题: 迁移步骤:

1. 在 FLASH 平台创建作业
2. 复用原 SQL 代码（无需修改）
3. 配置 ...

**问题 #24** (第 527 行, 语言: sql)

- **错误**: 可能的语法问题: 迁移注意事项:
- SESSION WINDOW 原生支持度 ~70%
- 部分逻辑可能回退到 JA...

**问题 #25** (第 549 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt6webgztTempValidation.java:11: 错误: 非法字符: '\uff08'
方案 A（推荐）: 重构为 SQL/Table API
    ^
C:\Users\luyan\AppData\Local\Temp\tmpt6webgztTempValidation.java:11: 错误: 此处不允许
- **错误行**: 11


### `Flink\07-rust-native\flink-rust-ecosystem-trends-2026.md`

**问题 #6** (第 434 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 29, column 1:
    format = "parquet"
    ^ (line: 29)
- **错误行**: 29


### `Flink\07-rust-native\heterogeneous-computing\01-gpu-udf-cuda.md`

**问题 #3** (第 356 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpau9e8b3jSmallStateProcessor.java:2: 错误: 找不到符号
class SmallStateProcessor extends KeyedProcessFunction<String, Event, Result> {
                                  ^

- **错误行**: 2


### `Flink\07-rust-native\heterogeneous-computing\04-unified-acceleration-api.md`

**问题 #10** (第 1140 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzt1we63uUnifiedAccelExample.java:4: 错误: 非法的表达式开始
        TableEnvironment tEnv = TableEnvironment.create(...);

- **错误行**: 4


### `Flink\07-rust-native\iron-functions-complete-guide.md`

**问题 #17** (第 556 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpigwql34iTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Te
- **错误行**: 3


### `Flink\07-rust-native\risingwave-comparison\01-risingwave-architecture.md`

**问题 #5** (第 350 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbmfr5djbTempValidation.java:4: 错误: 找不到符号
DataStream<Event> events = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpbmfr5djb
- **错误行**: 4


### `Flink\07-rust-native\risingwave-comparison\02-nexmark-head-to-head.md`

**问题 #8** (第 416 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3jk5axysTempValidation.java:17: 错误: 非法的表达式开始
q5.addSink(new RedisSink<>(...));
                           ^
1 个错误

- **错误行**: 17

**问题 #15** (第 605 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 3, column 12:
      resources:
               ^ (line: 3)
- **错误行**: 3
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Flink\07-rust-native\risingwave-comparison\03-migration-guide.md`

**问题 #9** (第 605 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6ykbil23NormalizeUdf.java:9: 错误: 需要 class、interface、enum 或 record
tableEnv.createTemporaryFunction("normalize", NormalizeUdf.class);
^
C:\Users\luyan\AppData\Local
- **错误行**: 9


### `Flink\07-rust-native\risingwave-comparison\04-hybrid-deployment.md`

**问题 #6** (第 499 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2ww42ux_TempValidation.java:12: 错误: 非法的表达式开始
DataStream<Order> orders = ...;
                           ^
C:\Users\luyan\AppData\Local\Temp\tmp2ww42ux_TempValidati
- **错误行**: 12

**问题 #8** (第 558 行, 语言: sql)

- **错误**: 可能的语法问题: -- TRINO 配置连接器
CATALOGS:
  RISINGWAVE:
    CONNECT...


### `Flink\07-rust-native\risingwave-comparison\04-risingwave-rust-udf-guide.md`

**问题 #17** (第 455 行, 语言: sql)

- **错误**: 可能的语法问题: -- 结果:
-- KEY    | VALUE | IS_NUMERIC
-- --------|...

**问题 #24** (第 743 行, 语言: sql)

- **错误**: 可能的语法问题: -- 2. 逐步增加复杂度
-- 3. 使用 EXPLAIN 查看执行计划
EXPLAIN SELE...


### `Flink\07-rust-native\risingwave-rust-udf-native-guide.md`

**问题 #8** (第 410 行, 语言: sql)

- **错误**: 可能的语法问题: -- 结果: 1, 2, 3, 4, 5...

**问题 #9** (第 427 行, 语言: sql)

- **错误**: 可能的语法问题: -- 结果:
-- PART    | IDX
-- --------|-----
-- APPLE...

**问题 #23** (第 1025 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看 UDF 执行统计
EXPLAIN ANALYZE SELECT MY_UDF(COLUM...; 可能的语法问题: -- 启用详细日志
SET UDF_LOG_LEVEL = 'DEBUG';...


### `Flink\07-rust-native\simd-optimization\03-jni-assembly-bridge.md`

**问题 #1** (第 40 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp15kda3vpTempValidation.java:4: 错误: 找不到符号
VectorSpecies<Float> SPECIES = FloatVector.SPECIES_256;
^
  符号:   类 VectorSpecies
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #2** (第 132 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps1mi8s07TempValidation.java:4: 错误: 找不到符号
long address = unsafe.allocateMemory(size + 32);
                                     ^
  符号:   变量 size
  位置: 类 TempValida
- **错误行**: 4


### `Flink\07-rust-native\vectorized-udfs\01-vectorized-udf-intro.md`

**问题 #5** (第 375 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 71

**问题 #8** (第 985 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...


### `Flink\08-roadmap\08.01-flink-24\2026-q2-flink-tasks.md`

**问题 #13** (第 470 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl3magdvqTempValidation.java:4: 错误: 找不到符号
for (KeyGroup kg : keyGroups) {
                   ^
  符号:   变量 keyGroups
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 4


### `Flink\08-roadmap\08.01-flink-24\FLIP-TRACKING-SYSTEM.md`

**问题 #5** (第 389 行, 语言: yaml)

- **错误**: while parsing a block mapping
  in "<unicode string>", line 37, column 5:
        <!-- FLIP状态: Draft/Under Discuss ...
        ^ (line: 37)
expected <block end>, but found '-'
  in "<unicode string>"
- **错误行**: 37


### `Flink\08-roadmap\08.01-flink-24\community-dynamics-tracking.md`

**问题 #15** (第 420 行, 语言: yaml)

- **错误**: sequence entries are not allowed here
  in "<unicode string>", line 4, column 54:
     ... park to Flink: Lessons Learned" - 12K views
                                         ^ (line: 4)
- **错误行**: 4


### `Flink\08-roadmap\08.01-flink-24\flink-2.1-frontier-tracking.md`

**问题 #4** (第 403 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyxmw2z9uTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4


### `Flink\08-roadmap\08.01-flink-24\flink-2.3-2.4-roadmap.md`

**问题 #11** (第 310 行, 语言: yaml)

- **错误**: while parsing a block collection
  in "<unicode string>", line 9, column 7:
          - JOB_MANAGER_RPC_ADDRESS=jobmanager
          ^ (line: 9)
expected <block end>, but found '<scalar>'
  in "<unico
- **错误行**: 9


### `Flink\08-roadmap\08.01-flink-24\flink-2.4-tracking.md`

**问题 #12** (第 481 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpptz9ngb5TempValidation.java:6: 错误: 找不到符号
AgentCoordinator coordinator = new AgentCoordinator(env);  // [Flink 2.4 前瞻] 该API为规划特性，可能变动
^
  符号:   类 AgentCoordinator

- **错误行**: 6

**问题 #13** (第 522 行, 语言: sql)

- **错误**: 可能的语法问题: -- SQL API: 创建AI AGENT

-- 注册MCP工具（未来可能的语法，概念设计阶段）...; 可能的语法问题: -- 创建AGENT（未来可能的语法，概念设计阶段）
<!-- 以下语法为概念设计，实际 FLINK...; 可能的语法问题: -- 多AGENT协调查询（未来可能的语法，概念设计阶段）
~~CREATE AGENT_TEAM ...

**问题 #14** (第 566 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvolhatjqTempValidation.java:21: 错误: 非法的表达式开始
    .fromSource(kafkaSource, WatermarkStrategy.forBoundedOutOfOrderness(...), "Kafka")

- **错误行**: 21


### `Flink\08-roadmap\08.01-flink-24\flink-2.5-preview.md`

**问题 #1** (第 39 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 1, column 32:
    预计发布时间: 2026 Q3 (Feature Freeze: 2026-07, GA: 2026-09)
                                   ^ (line: 1)
- **错误行**: 1
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #3** (第 94 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 1, column 33:
    FLIP: FLIP-442 "Serverless Flink: Zero-to-Infinity Scaling"
                                    ^ (line: 1)
- **错误行**: 1
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #12** (第 429 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpol17qtbmTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
^
  符号:   类 StreamExecutionEnvironm
- **错误行**: 4

**问题 #14** (第 508 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt2grqiz5TempValidation.java:4: 错误: 找不到符号
TableEnvironment tEnv = TableEnvironment.create(EnvironmentSettings.inStreamingMode());
^
  符号:   类 TableEnvironment
  位置:
- **错误行**: 4


### `Flink\08-roadmap\08.01-flink-24\flink-25-stream-batch-unification.md`

**问题 #15** (第 609 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp__hmoba6TempValidation.java:8: 错误: 非法的类型开始
env.getConfig().set("execution.runtime-mode", "ADAPTIVE");  <!-- 前瞻性API: Flink 2.5规划中 -->

- **错误行**: 8

**问题 #16** (第 648 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf5ab3fybTempValidation.java:9: 错误: 非法的类型开始
env.getConfig().set("execution.runtime-mode", "MIXED");  <!-- 前瞻性API: Flink 2.5规划中 -->

- **错误行**: 9

**问题 #19** (第 837 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9rcv2jg6TempValidation.java:4: 错误: 找不到符号
TableEnvironment tEnv = TableEnvironment.create(
^
  符号:   类 TableEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #25** (第 1137 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp278awx91TempValidation.java:9: 错误: 非法的类型开始
env.getConfig().set("execution.runtime-mode", "BATCH");  <!-- 前瞻性配置: Flink 2.5规划中 -->

- **错误行**: 9

**问题 #26** (第 1155 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfxvucsrcTempValidation.java:18: 错误: 非法的类型开始
env.getConfig().set("execution.runtime-mode", "BATCH");  <!-- 前瞻性配置: Flink 2.5规划中 -->

- **错误行**: 18

**问题 #29** (第 1219 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 5, column 31:
        配置: execution.runtime-mode: STREAMING
                                  ^ (line: 5)
- **错误行**: 5
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Flink\08-roadmap\08.01-flink-24\flink-30-architecture-redesign.md`

**问题 #3** (第 150 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3g386r0mExecutionMode.java:9: 错误: 不是语句
    if (stream.isUnbounded() && hints.latency < 100ms)
                                                   ^
C:\Users\luyan\A
- **错误行**: 9

**问题 #5** (第 198 行, 语言: yaml)

- **错误**: while parsing a block collection
  in "<unicode string>", line 2, column 3:
      - HotData: L1 + L2 (95%+命中率，3.0目标)
      ^ (line: 2)
expected <block end>, but found '?'
  in "<unicode string>", line
- **错误行**: 2

**问题 #17** (第 560 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4l8brb50TempValidation.java:3: 错误: 需要';'
ExecutionMode selectOptimalMode(DataCharacteristics data, QueryRequirements req) {
                               ^
C:\Use
- **错误行**: 3

**问题 #24** (第 767 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpssu0bb78TempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
^
  符号:   类 StreamExecutionEnvironm
- **错误行**: 4


### `Flink\08-roadmap\08.01-flink-24\flink-version-evolution-complete-guide.md`

**问题 #3** (第 129 行, 语言: yaml)

- **错误**: while parsing a block mapping
  in "<unicode string>", line 6, column 3:
      FLIP-217: "Incremental Checkpoin ...
      ^ (line: 6)
expected <block end>, but found '<block sequence start>'
  in "<u
- **错误行**: 6

**问题 #4** (第 165 行, 语言: yaml)

- **错误**: while parsing a block mapping
  in "<unicode string>", line 6, column 3:
      FLIP-265: "Adaptive Scheduler Im ...
      ^ (line: 6)
expected <block end>, but found '<block sequence start>'
  in "<u
- **错误行**: 6

**问题 #6** (第 201 行, 语言: yaml)

- **错误**: while parsing a block mapping
  in "<unicode string>", line 7, column 3:
      FLIP-311: "DataSet API Deprecati ...
      ^ (line: 7)
expected <block end>, but found '<block sequence start>'
  in "<u
- **错误行**: 7

**问题 #7** (第 237 行, 语言: yaml)

- **错误**: while parsing a block mapping
  in "<unicode string>", line 8, column 6:
         FLIP-392: "Disaggregated State S ...
         ^ (line: 8)
expected <block end>, but found '-'
  in "<unicode string>"
- **错误行**: 8

**问题 #8** (第 290 行, 语言: yaml)

- **错误**: while parsing a block mapping
  in "<unicode string>", line 6, column 3:
      FLIP-435: "Materialized Table"
      ^ (line: 6)
expected <block end>, but found '<block sequence start>'
  in "<unicode
- **错误行**: 6

**问题 #10** (第 333 行, 语言: yaml)

- **错误**: while parsing a block mapping
  in "<unicode string>", line 6, column 3:
      FLIP-471: "VECTOR_SEARCH Support ...
      ^ (line: 6)
expected <block end>, but found '<scalar>'
  in "<unicode string>
- **错误行**: 6

**问题 #12** (第 381 行, 语言: sql)

- **错误**: 可能的语法问题: -- 注册ML模型
<!-- 以下语法为概念设计，实际 FLINK 版本尚未支持 -->
~~CRE...

**问题 #13** (第 403 行, 语言: yaml)

- **错误**: while parsing a block mapping
  in "<unicode string>", line 6, column 3:
      FLIP-531: "Flink AI Agents" (MVP ...
      ^ (line: 6)
expected <block end>, but found '<scalar>'
  in "<unicode string>
- **错误行**: 6

**问题 #30** (第 849 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc13o2yktTempValidation.java:4: 错误: 找不到符号
ExecutionEnvironment env =
^
  符号:   类 ExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpc1
- **错误行**: 4

**问题 #31** (第 869 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdtx4e181TempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #32** (第 891 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi6e6ymwwTempValidation.java:4: 错误: 找不到符号
EnvironmentSettings settings = EnvironmentSettings
^
  符号:   类 EnvironmentSettings
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4


### `Flink\08-roadmap\08.02-flink-25\flink-25-features-preview.md`

**问题 #2** (第 34 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiu61pbf7TempValidation.java:11: 错误: 非法的表达式开始
DataStream<Event> stream = env.fromSource(kafkaSource, ...);
                                                       ^

- **错误行**: 11

**问题 #7** (第 131 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0neya_2oTempValidation.java:4: 错误: 找不到符号
ModelInferenceConfig config = ModelInferenceConfig.builder()
^
  符号:   类 ModelInferenceConfig
  位置: 类 TempValidation
C:\Us
- **错误行**: 4

**问题 #8** (第 148 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2s31l5ydTempValidation.java:4: 错误: 找不到符号
InferenceConfig config = InferenceConfig.builder()
^
  符号:   类 InferenceConfig
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #14** (第 252 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpls_u9m89TempValidation.java:4: 错误: 非法的表达式开始
TableEnvironment tEnv = TableEnvironment.create(...);
                                                ^
1 个错误

- **错误行**: 4


### `Flink\08-roadmap\08.02-flink-25\flink-25-migration-guide.md`

**问题 #7** (第 129 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    execution.runtime-mode: adaptive ...
    ^ (line: 2)
found duplicate key "execution.runtime-mode" with value "streaming" (o
- **错误行**: 2

**问题 #8** (第 145 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnvc0q_wnTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #9** (第 168 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpolihwfssTempValidation.java:4: 错误: 找不到符号
TableEnvironment tEnv = TableEnvironment.create(settings);
^
  符号:   类 TableEnvironment
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4


### `Flink\08-roadmap\08.02-flink-25\flink-25-roadmap.md`

**问题 #1** (第 12 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 3, column 19:
      - Feature Freeze: 2026-07
                      ^ (line: 3)
- **错误行**: 3
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #2** (第 41 行, 语言: yaml)

- **错误**: while parsing a block collection
  in "<unicode string>", line 3, column 5:
        - 统一执行计划生成器
        ^ (line: 3)
expected <block end>, but found '?'
  in "<unicode string>", line 6, column 5:

- **错误行**: 3

**问题 #3** (第 76 行, 语言: yaml)

- **错误**: while parsing a block collection
  in "<unicode string>", line 3, column 5:
        - 无流量时资源释放至 0
        ^ (line: 3)
expected <block end>, but found '?'
  in "<unicode string>", line 6, column 5:

- **错误行**: 3

**问题 #4** (第 109 行, 语言: yaml)

- **错误**: while parsing a block collection
  in "<unicode string>", line 3, column 5:
        - 动态批处理
        ^ (line: 3)
expected <block end>, but found '?'
  in "<unicode string>", line 6, column 5:
        状
- **错误行**: 3


### `Flink\09-practices\09.01-case-studies\case-ecommerce-realtime-recommendation.md`

**问题 #19** (第 1835 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf7bvvdt9TempValidation.java:4: 错误: 非法的表达式开始
public UserProfile updateProfile(UserProfile current, BehaviorEvent event) {
^
C:\Users\luyan\AppData\Local\Temp\tmpf7b
- **错误行**: 4


### `Flink\09-practices\09.01-case-studies\case-financial-realtime-risk-control.md`

**问题 #6** (第 491 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3sg_x6naTempValidation.java:4: 错误: 找不到符号
DataStream<Transaction> partitioned = transactions
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 4

**问题 #7** (第 500 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj837asabTempValidation.java:3: 错误: 找不到符号
        StateTtlConfig ttlConfig = StateTtlConfig
        ^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 3

**问题 #10** (第 548 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy6eja1i6TempValidation.java:4: 错误: 找不到符号
AsyncFunction<EnrichedTransaction, ScoredTransaction> asyncFunction =
^
  符号:   类 AsyncFunction
  位置: 类 TempValidation
C:\
- **错误行**: 4

**问题 #11** (第 578 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjhq8zw12TempValidation.java:4: 错误: 找不到符号
LoadingCache<String, UserProfile> profileCache = Caffeine.newBuilder()
^
  符号:   类 LoadingCache
  位置: 类 TempValidation
C:\
- **错误行**: 4

**问题 #24** (第 1758 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo3s4bas5TempValidation.java:4: 错误: 找不到符号
StateTtlConfig ttlConfig = StateTtlConfig
^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #25** (第 1780 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1og5opg_TempValidation.java:4: 错误: 找不到符号
Pattern<Transaction, ?> pattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #26** (第 1804 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3a272uh7TempValidation.java:4: 错误: 找不到符号
DataStream<Result> result = AsyncDataStream.unorderedWait(
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #29** (第 1859 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptas1rc45TempValidation.java:4: 错误: 找不到符号
ValueState<OnlineFeatures> onlineFeatures;
^
  符号:   类 ValueState
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #30** (第 1874 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgrd555gcTempValidation.java:4: 错误: 找不到符号
DataStream<ScoredTransaction> shadowScored = AsyncDataStream.unorderedWait(
^
  符号:   类 DataStream
  位置: 类 TempValidation

- **错误行**: 4


### `Flink\09-practices\09.01-case-studies\case-fraud-detection-advanced.md`

**问题 #8** (第 743 行, 语言: sql)

- **错误**: 可能的语法问题: -- REDIS 特征表结构
-- 用户实时统计特征
HSET USER:STATS:{USER_I...


### `Flink\09-practices\09.01-case-studies\case-gaming-realtime-analytics.md`

**问题 #8** (第 770 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqjga5vh4GamingAnalyticsJob.java:184: 错误: 需要'('或'['
                )
                ^
1 个错误

- **错误行**: 184


### `Flink\09-practices\09.01-case-studies\case-iot-stream-processing.md`

**问题 #3** (第 240 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp60la3afdTempValidation.java:4: 错误: 找不到符号
    .<SensorEvent>forBoundedOutOfOrderness(Duration.ofSeconds(10))
      ^
  符号:   类 SensorEvent
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #5** (第 321 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqbjf0f4jTempValidation.java:4: 错误: 找不到符号
    .<SensorEvent>forBoundedOutOfOrderness(Duration.ofSeconds(10))
      ^
  符号:   类 SensorEvent
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #6** (第 348 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0rqvbblmTempValidation.java:3: 错误: 找不到符号
        StateTtlConfig ttlConfig = StateTtlConfig
        ^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 3


### `Flink\09-practices\09.01-case-studies\case-realtime-analytics.md`

**问题 #11** (第 800 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8wotaoszTempValidation.java:3: 错误: 非法的表达式开始
private static void configureStateBackend(StreamExecutionEnvironment env) {
^
C:\Users\luyan\AppData\Local\Temp\tmp8wot
- **错误行**: 3

**问题 #12** (第 839 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn8ui1wl3TempValidation.java:3: 错误: 非法的表达式开始
private static void configureCheckpoint(StreamExecutionEnvironment env) {
^
C:\Users\luyan\AppData\Local\Temp\tmpn8ui1w
- **错误行**: 3

**问题 #16** (第 1034 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprstn_0tfTempValidation.java:4: 错误: 非法的表达式开始
public int getPartition(String userId) {
^
C:\Users\luyan\AppData\Local\Temp\tmprstn_0tfTempValidation.java:13: 错误: 需要
- **错误行**: 4

**问题 #17** (第 1067 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoaymoif7TempValidation.java:5: 错误: 需要';'
    .withIdleness(Duration.ofMinutes(1))  // 1分钟无数据视为空闲
                                        ^
1 个错误

- **错误行**: 5

**问题 #18** (第 1091 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps8eqltpfTempValidation.java:3: 错误: 非法的表达式开始
        .map(new ParseFunction())
        ^
C:\Users\luyan\AppData\Local\Temp\tmps8eqltpfTempValidation.java:5: 错误: 需要'
- **错误行**: 3

**问题 #19** (第 1101 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx7pnqnd2TempValidation.java:3: 错误: 找不到符号
        StateTtlConfig ttlConfig = StateTtlConfig
        ^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 3

**问题 #20** (第 1114 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfj2uxn18TempValidation.java:4: 错误: 需要';'
public void snapshotState(FunctionSnapshotContext context) throws Exception {
                         ^
C:\Users\luyan\Ap
- **错误行**: 4


### `Flink\09-practices\09.01-case-studies\case-smart-grid-energy-management.md`

**问题 #7** (第 659 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmputbdv0yjTempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend rocksDbBackend = new RocksDBStateBackend(
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempValidation
C:\Us
- **错误行**: 4


### `Flink\09-practices\09.01-case-studies\case-smart-manufacturing-iot.md`

**问题 #5** (第 506 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgxnq9albTempValidation.java:11: 错误: 找不到符号
    .where(new SimpleCondition<SensorEvent>() {
               ^
  符号:   类 SimpleCondition
  位置: 类 TempValidation
C:\User
- **错误行**: 11


### `Flink\09-practices\09.02-benchmarking\flink-24-25-benchmark-results.md`

**问题 #5** (第 380 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 7, column 3:
      RocksDB: 9.2.0
      ^ (line: 7)
found duplicate key "ForSt" with value "2.5.0-tiered (2.5)" (original value: "2.4.0-nativ
- **错误行**: 7


### `Flink\09-practices\09.02-benchmarking\performance-benchmark-suite.md`

**问题 #5** (第 475 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprop5xhddTempValidation.java:4: 错误: 找不到符号
DataStream<Bid> bids = env.addSource(new NexmarkSource("Bid"));
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #6** (第 486 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg4ubsfwkTempValidation.java:4: 错误: 找不到符号
DataStream<Auction> auctions = env.addSource(new NexmarkSource("Auction"));
^
  符号:   类 DataStream
  位置: 类 TempValidation

- **错误行**: 4

**问题 #7** (第 515 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9wbq4vntTempValidation.java:4: 错误: 找不到符号
DataStream<Person> persons = env.addSource(new NexmarkSource("Person"));
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\
- **错误行**: 4

**问题 #18** (第 1201 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 21

**问题 #19** (第 1450 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 82


### `Flink\09-practices\09.02-benchmarking\performance-benchmarking-guide.md`

**问题 #6** (第 251 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfq1rilkoTempValidation.java:4: 错误: 找不到符号
DataStream<String> source = env.addSource(new WordSource())
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #7** (第 296 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt75hxh8oTempValidation.java:4: 错误: 找不到符号
DataStream<Event> events = env.addSource(new KafkaSource<>())
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4

**问题 #9** (第 354 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppw2w4xlnTempValidation.java:4: 错误: 找不到符号
MetricGroup metricGroup = getRuntimeContext()
^
  符号:   类 MetricGroup
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #18** (第 600 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_e5v2y1xTempValidation.java:5: 错误: 非法的表达式开始
    .window(...)  // 第一阶段
            ^
C:\Users\luyan\AppData\Local\Temp\tmp_e5v2y1xTempValidation.java:8: 错误: 非法的表达式开
- **错误行**: 5

**问题 #19** (第 612 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5uce76tpTempValidation.java:4: 错误: 找不到符号
stream.map(event -> {
^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp5uce76tpTempValidati
- **错误行**: 4


### `Flink\09-practices\09.02-benchmarking\streaming-benchmarks.md`

**问题 #4** (第 295 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp33hdsl2gTempValidation.java:6: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 6

**问题 #6** (第 358 行, 语言: yaml)

- **错误**: while scanning a simple key
  in "<unicode string>", line 15, column 1:
    rate(flink_taskmanager_job_task_ ...
    ^ (line: 15)
could not find expected ':'
  in "<unicode string>", line 17, column
- **错误行**: 15


### `Flink\09-practices\09.03-performance-tuning\05-vs-competitors\flink-vs-kafka-streams.md`

**问题 #10** (第 323 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdsg3bfoqTempValidation.java:4: 错误: 找不到符号
Pattern<Transaction, ?> fraudPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #11** (第 346 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp53m5x6hzTempValidation.java:4: 错误: 非法的表达式开始
DataStream<Event1> kafka = env.fromSource(kafkaSource, ...);
                                                       ^
C
- **错误行**: 4

**问题 #12** (第 358 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb085bwlhTempValidation.java:4: 错误: 找不到符号
WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ofSeconds(30))
                   ^
  符号:   类 Event
  位置: 类 Tem
- **错误行**: 4

**问题 #17** (第 522 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxezvqfq_TempValidation.java:23: 错误: 需要';'
public Integer getInventory(@PathVariable String productId) {
                           ^
C:\Users\luyan\AppData\Local\T
- **错误行**: 23

**问题 #18** (第 572 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdqw3j3blTempValidation.java:4: 错误: 找不到符号
DataStream<Transaction> transactions = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #24** (第 991 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc_y3bm4mTempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #25** (第 1009 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpagosfwm5TempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        ^
  符号:   类 StreamE
- **错误行**: 3


### `Flink\09-practices\09.03-performance-tuning\05-vs-competitors\flink-vs-risingwave-deep-dive.md`

**问题 #7** (第 319 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv18n4_axTempValidation.java:4: 错误: 找不到符号
DataStream<CleanedOrder> cleanedOrders = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `Flink\09-practices\09.03-performance-tuning\05-vs-competitors\linkedin-samza-deep-dive.md`

**问题 #8** (第 332 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqsud0lgyWordCountTask.java:18: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Tuple2<String, Integer>> wordCounts =
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 18

**问题 #10** (第 409 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0b2pt3vqTempValidation.java:3: 错误: 找不到符号
        DataStream<MemberActivity> activityStream = events
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #11** (第 421 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplymr8v4dTempValidation.java:8: 错误: 非法的表达式开始
public void processActivity(MemberEvent event, MessageCollector collector) {
^
C:\Users\luyan\AppData\Local\Temp\tmplym
- **错误行**: 8

**问题 #12** (第 438 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6com9o1dTempValidation.java:3: 错误: 找不到符号
        Table memberProfile = tableEnv.fromDataStream(profileStream)
        ^
  符号:   类 Table
  位置: 类 TempValidation
C:\U
- **错误行**: 3


### `Flink\09-practices\09.03-performance-tuning\06.02-performance-optimization-complete.md`

**问题 #4** (第 447 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxfnuomd6TempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #7** (第 552 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7a6jl6miTempValidation.java:4: 错误: 找不到符号
env.disableOperatorChaining();  // 全局禁用（调试用）
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #8** (第 591 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6sxxgegxOrder.java:2: 错误: 需要 class、interface、enum 或 record
env.getConfig().registerTypeWithKryoSerializer(
^
C:\Users\luyan\AppData\Local\Temp\tmp6sxxgegxOrder.jav
- **错误行**: 2

**问题 #11** (第 708 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjj6olsdpTempValidation.java:4: 错误: 找不到符号
env.setParallelism(8);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpjj6olsdpTempValidation
- **错误行**: 4

**问题 #12** (第 750 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看执行计划
EXPLAIN SELECT
    USER_ID,
    COUNT(*)...; 可能的语法问题: -- 使用EXPLAIN ESTIMATED_COST查看代价估算
EXPLAIN ESTIMATE...

**问题 #16** (第 878 行, 语言: sql)

- **错误**: 可能的语法问题: -- 动态分区裁剪
SET TABLE.OPTIMIZER.DYNAMIC-FILTERING.EN...

**问题 #22** (第 1115 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoiiadfudTempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<Event> kafkaSource = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #23** (第 1174 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp05xhuaklAsyncUserLookup.java:38: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedEvent> enriched = AsyncDataStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 38

**问题 #25** (第 1268 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmsumrgvbTempValidation.java:4: 错误: 找不到符号
HikariConfig config = new HikariConfig();
^
  符号:   类 HikariConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #27** (第 1348 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpajjxn5ksTempValidation.java:4: 错误: 找不到符号
DataStream<Order> orders = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpajjxn5ks
- **错误行**: 4

**问题 #29** (第 1404 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpapvg1lv3FraudResultSink.java:33: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<FraudResult> results = AsyncDataStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 33

**问题 #31** (第 1486 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf93po_htTempValidation.java:4: 错误: 找不到符号
DataStream<DeviceMetrics> metrics = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tm
- **错误行**: 4


### `Flink\09-practices\09.03-performance-tuning\flink-24-performance-improvements.md`

**问题 #7** (第 471 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphpvhn4nwUserEvent.java:13: 错误: 未命名类 是预览功能，默认情况下禁用。
ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();
^
  （请使用 --enable-preview 以启用 未命名类）
C
- **错误行**: 13

**问题 #10** (第 548 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp27w18ae1TempValidation.java:4: 错误: 找不到符号
ForStStateBackend forStBackend = new ForStStateBackend();  // [Flink 2.4 前瞻] 该API为规划特性，可能变动
^
  符号:   类 ForStStateBackend

- **错误行**: 4

**问题 #11** (第 580 行, 语言: sql)

- **错误**: 可能的语法问题: -- 启用向量化执行
SET TABLE.EXEC.MINI-BATCH.ENABLED = TRU...; 可能的语法问题: -- 启用自适应JOIN
SET TABLE.OPTIMIZER.ADAPTIVE-JOIN.ENA...; 可能的语法问题: -- 启用谓词下推
SET TABLE.OPTIMIZER.PREDICATE-PUSHDOWN.E...; 可能的语法问题:

**问题 #13** (第 625 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptijcsz5bTempValidation.java:4: 错误: 找不到符号
TableEnvironment tableEnv = TableEnvironment.create(settings);
^
  符号:   类 TableEnvironment
  位置: 类 TempValidation
C:\User
- **错误行**: 4


### `Flink\09-practices\09.03-performance-tuning\flink-tco-cost-optimization-guide.md`

**问题 #5** (第 791 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8jmh8jzpTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4


### `Flink\09-practices\09.03-performance-tuning\performance-tuning-guide.md`

**问题 #3** (第 297 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphnflt5fzTempValidation.java:4: 错误: 找不到符号
DataStream<Order> orders = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmphnflt5fz
- **错误行**: 4

**问题 #4** (第 314 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    execution.checkpointing.unaligne ...
    ^ (line: 2)
found duplicate key "execution.checkpointing.interval" with value "600
- **错误行**: 2


### `Flink\09-practices\09.03-performance-tuning\state-backend-selection.md`

**问题 #1** (第 337 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmi_k7fn8TempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env =
        ^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3

**问题 #2** (第 359 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf9ijp5x3TempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend backend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #3** (第 380 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj_cvgm9bTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend backend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #5** (第 421 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps8zph9huTempValidation.java:3: 错误: 找不到符号
        conf.setString("taskmanager.memory.managed.size", "64mb");  // 过小！
        ^
  符号:   变量 conf
  位置: 类 TempValidatio
- **错误行**: 3

**问题 #6** (第 429 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaj7i7jmkTempValidation.java:3: 错误: 找不到符号
        conf.setString("taskmanager.memory.managed.fraction", "0.4");
        ^
  符号:   变量 conf
  位置: 类 TempValidation
C:\
- **错误行**: 3


### `Flink\09-practices\09.03-performance-tuning\stream-processing-cost-optimization.md`

**问题 #4** (第 318 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwf0c658vTempValidation.java:6: 错误: 找不到符号
    triggerEmergencyCheckpoint();
    ^
  符号:   方法 triggerEmergencyCheckpoint()
  位置: 类 TempValidation
C:\Users\luyan\AppD
- **错误行**: 6

**问题 #12** (第 852 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    spec:
    ^ (line: 2)
found duplicate key "spec" with value "{}" (original value: "{}")
  in "<unicode string>", line 10, c
- **错误行**: 2

**问题 #19** (第 1118 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb2u4ut2tTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4


### `Flink\09-practices\09.03-performance-tuning\stream-processing-testing-strategies.md`

**问题 #3** (第 196 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwm1m_8xkTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #4** (第 231 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkpjd4kvtTempValidation.java:4: 错误: 需要';'
public void testStatefulOperator() throws Exception {
                                ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #5** (第 262 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb0530dkvTempValidation.java:8: 错误: 需要';'
public void testEnrichmentOperatorWithMock() throws Exception {
                                          ^
C:\Users\luyan
- **错误行**: 8

**问题 #6** (第 299 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdpv0e6xuTempValidation.java:4: 错误: 需要';'
public void testKafkaSourceIntegration() throws Exception {
                                      ^
C:\Users\luyan\AppData
- **错误行**: 4

**问题 #7** (第 347 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpddpgjroeTempValidation.java:4: 错误: 需要';'
public void testRocksDBStateBackend() throws Exception {
                                   ^
C:\Users\luyan\AppData\Local
- **错误行**: 4

**问题 #8** (第 388 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6mro890gTempValidation.java:4: 错误: 需要';'
public void testCheckpointRecovery() throws Exception {
                                  ^
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #9** (第 440 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc5v6sej3TempValidation.java:4: 错误: 需要';'
public void testEndToEndPipeline() throws Exception {
                                ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #11** (第 533 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxoojf8tvTempValidation.java:4: 错误: 需要';'
public void testFailureRecovery() throws Exception {
                               ^
C:\Users\luyan\AppData\Local\Temp\tm
- **错误行**: 4

**问题 #13** (第 646 行, 语言: java)

- **错误**: 括号不匹配: (=79, )=83


### `Flink\09-practices\09.03-performance-tuning\troubleshooting-handbook.md`

**问题 #16** (第 476 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpauky1r_4TempValidation.java:5: 错误: 非法的表达式开始
private static final List<Object> cache = new ArrayList<>();
^
C:\Users\luyan\AppData\Local\Temp\tmpauky1r_4TempValidat
- **错误行**: 5

**问题 #26** (第 603 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpegexr5giTempValidation.java:4: 错误: 找不到符号
    .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(30))
      ^
  符号:   类 Event
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4

**问题 #28** (第 619 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3rejiqw0TempValidation.java:5: 错误: 非法的表达式开始
DataStream<Event> stream1 = ...
                            ^
C:\Users\luyan\AppData\Local\Temp\tmp3rejiqw0TempValidati
- **错误行**: 5

**问题 #29** (第 634 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1_wlgfybTempValidation.java:4: 错误: 找不到符号
WatermarkStrategy.<Event>forBoundedOutOfOrderness(
                   ^
  符号:   类 Event
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #32** (第 674 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkzr3rdc0TempValidation.java:9: 错误: 非法的表达式开始
new ValueStateDescriptor<>("newName", ...); // 名称变更会导致状态找不到
                                      ^
1 个错误

- **错误行**: 9

**问题 #37** (第 739 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    restart-strategy: fixed-delay
    ^ (line: 2)
found duplicate key "restart-strategy" with value "exponential-delay" (origina
- **错误行**: 2

**问题 #39** (第 763 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvg5b9bf6TempValidation.java:5: 错误: 找不到符号
    externalService.call();
    ^
  符号:   变量 externalService
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpv
- **错误行**: 5


### `Flink\09-practices\09.04-deployment\flink-k8s-operator-migration-1.13-to-1.14.md`

**问题 #18** (第 544 行, 语言: yaml)

- **错误**: while scanning a block scalar
  in "<unicode string>", line 6, column 22:
        - Reconcile 成功率: > 99%
                         ^ (line: 6)
expected a comment or a line break, but found '9'
  in "<u
- **错误行**: 6

**问题 #22** (第 684 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 1


### `Flink\09-practices\09.04-deployment\flink-kubernetes-operator-1.14-guide.md`

**问题 #2** (第 73 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 2, column 7:
      name: string,                    # 配 ...
          ^ (line: 2)
- **错误行**: 2
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #11** (第 299 行, 语言: yaml)

- **错误**: while scanning a simple key
  in "<unicode string>", line 9, column 1:
    {
    ^ (line: 9)
could not find expected ':'
  in "<unicode string>", line 10, column 3:
      "$schema": "<[链接不完整 - 需手动修复]>
- **错误行**: 9

**问题 #22** (第 699 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    spec:
    ^ (line: 2)
found duplicate key "spec" with value "{}" (original value: "{}")
  in "<unicode string>", line 10, c
- **错误行**: 2

**问题 #35** (第 1674 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 24, column 1:
    apiVersion: kustomize.config.k8s ...
    ^ (line: 24)
found duplicate key "apiVersion" with value "flink.apache.org/v1beta
- **错误行**: 24


### `Flink\09-practices\09.04-security\flink-24-security-enhancements.md`

**问题 #5** (第 160 行, 语言: yaml)

- **错误**: while parsing a block mapping
  in "<unicode string>", line 2, column 1:
    security.oauth.enabled: true
    ^ (line: 2)
expected <block end>, but found '<scalar>'
  in "<unicode string>", line 3, co
- **错误行**: 2

**问题 #13** (第 389 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpavpg4z1lTempValidation.java:4: 错误: 找不到符号
DataMaskingConfig maskingConfig = DataMaskingConfig.builder()  // [Flink 2.4 前瞻] 该API为规划特性，可能变动
^
  符号:   类 DataMaskingCon
- **错误行**: 4


### `Flink\09-practices\09.04-security\flink-security-complete-guide.md`

**问题 #8** (第 503 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfnyvpqeuTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
^
C:\Users\luyan\AppData\Local\Temp\tmpfnyvpqeuT
- **错误行**: 4


### `Flink\09-practices\09.04-security\security-hardening-guide.md`

**问题 #15** (第 542 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdfmknoq_EncryptedRocksDBStateBackend.java:29: 错误: 非法的表达式开始
            super.createKeyedStateBackend(...),
                                          ^
C:\Users\luy
- **错误行**: 29

**问题 #16** (第 582 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    state.backend: rocksdb
    ^ (line: 4)
found duplicate key "s3.server-side-encryption" with value "aws:kms" (original value:
- **错误行**: 4

**问题 #18** (第 619 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjqhk4k60TempValidation.java:4: 错误: 找不到符号
Properties kafkaProps = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #19** (第 640 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_1pma7m8TempValidation.java:10: 错误: 找不到符号
JDBCInputFormat jdbcInput = JDBCInputFormat.buildJDBCInputFormat()
^
  符号:   类 JDBCInputFormat
  位置: 类 TempValidation
C:\
- **错误行**: 10

**问题 #20** (第 661 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxdn5hlwhTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.runtime.state.encryption.EncryptionOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmpxdn5hlwhTemp
- **错误行**: 3

**问题 #26** (第 857 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0qtz7fzwRowLevelSecurityFilter.java:21: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Event> securedStream = rawStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 21


### `Flink\09-practices\09.04-security\security\evolution\audit-evolution.md`

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyqpf4gmpTempValidation.java:3: 错误: 找不到符号
        auditLog.record(new AuditEvent()
        ^
  符号:   变量 auditLog
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 3


### `Flink\09-practices\09.04-security\security\evolution\auth-evolution.md`

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpepemayrrTempValidation.java:3: 错误: 找不到符号
        OAuth2Client client = new OAuth2Client()
        ^
  符号:   类 OAuth2Client
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3


### `Flink\09-practices\09.04-security\security\evolution\authorization-evolution.md`

**问题 #2** (第 67 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp82wbtzdtTempValidation.java:3: 错误: 找不到符号
if (authorizer.hasPermission(user, "jobs:cancel", jobId)) {
                             ^
  符号:   变量 user
  位置: 类 TempVal
- **错误行**: 3


### `Flink\09-practices\09.04-security\security\evolution\compliance-evolution.md`

**问题 #2** (第 69 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplcg7ovclTempValidation.java:4: 错误: 此处不允许使用修饰符private
private String ssn;
               ^
C:\Users\luyan\AppData\Local\Temp\tmplcg7ovclTempValidation.java:3: 错误: 找
- **错误行**: 4


### `Flink\09-practices\09.04-security\security\evolution\data-governance-evolution.md`

**问题 #1** (第 55 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvn7_fmpcTempValidation.java:3: 错误: 找不到符号
        LineageRecorder.record(new DataLineage()
        ^
  符号:   变量 LineageRecorder
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 3


### `Flink\09-practices\09.04-security\security\evolution\encryption-evolution.md`

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg9q19ojwTempValidation.java:3: 错误: 找不到符号
        KeyVault vault = KeyVault.create(config);
        ^
  符号:   类 KeyVault
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3


### `Flink\09-practices\09.04-security\security\evolution\key-management-evolution.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdfhwpr4hTempValidation.java:3: 错误: 找不到符号
        Vault vault = Vault.builder()
        ^
  符号:   类 Vault
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 3


### `Flink\09-practices\09.04-security\security\evolution\lineage-evolution.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplfgyo1oxTempValidation.java:3: 错误: 找不到符号
        LineageContext ctx = LineageContext.current();
        ^
  符号:   类 LineageContext
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3


### `Flink\09-practices\09.04-security\security\evolution\tee-evolution.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1583f8pcTempValidation.java:3: 错误: 找不到符号
        Enclave enclave = EnclaveLoader.load("enclave.so");
        ^
  符号:   类 Enclave
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3

**问题 #2** (第 63 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp38im17z7TempValidation.java:4: 错误: 找不到符号
EnclaveResult result = teeExecutor.execute(() -> {
^
  符号:   类 EnclaveResult
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4


### `Flink\09-practices\09.04-security\spiffe-spire-integration-guide.md`

**问题 #14** (第 715 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe1jdoj8pTempValidation.java:4: 错误: 找不到符号
Properties kafkaProps = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #15** (第 750 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe1vbp1d3TempValidation.java:4: 错误: 找不到符号
RestClientBuilder builder = RestClient.builder(
^
  符号:   类 RestClientBuilder
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4


### `Flink\09-practices\09.04-security\streaming-security-best-practices.md`

**问题 #4** (第 205 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 9, column 1:
    ssl.keystore.location=/etc/kafka ...
    ^ (line: 9)
- **错误行**: 9

**问题 #8** (第 323 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4ani_mhuTempValidation.java:4: 错误: 找不到符号
CheckpointConfig checkpointConfig = env.getCheckpointConfig();
^
  符号:   类 CheckpointConfig
  位置: 类 TempValidation
C:\User
- **错误行**: 4


### `Flink\09-practices\09.04-security\trusted-execution-flink.md`

**问题 #13** (第 482 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 2

**问题 #14** (第 500 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 1


### `Flink\09-practices\09.05-edge\flink-edge-resource-optimization.md`

**问题 #2** (第 271 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8zqigiebTempValidation.java:6: 错误: 找不到符号
env.setParallelism(optimalParallelism);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp8zqig
- **错误行**: 6

**问题 #3** (第 283 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbm9eyfbuTempValidation.java:5: 错误: 非法的表达式开始
    .filter(...)
            ^
C:\Users\luyan\AppData\Local\Temp\tmpbm9eyfbuTempValidation.java:6: 错误: 非法的表达式开始
    .ma
- **错误行**: 5

**问题 #4** (第 301 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaj9qhvugTempValidation.java:5: 错误: 找不到符号
    inputStream,
    ^
  符号:   变量 inputStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpaj9qhvugTempVali
- **错误行**: 5


### `Flink\09-practices\09.05-edge\flink-edge-streaming-guide.md`

**问题 #3** (第 300 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8y6rmscwTempValidation.java:8: 错误: 找不到符号
    .filter(nonNullFilter);
            ^
  符号:   变量 nonNullFilter
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 8

**问题 #4** (第 317 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp273ngqfxTempValidation.java:4: 错误: 非法的表达式开始
.window(TumblingEventTimeWindows.of(Time.minutes(5)))
^
C:\Users\luyan\AppData\Local\Temp\tmp273ngqfxTempValidation.jav
- **错误行**: 4


### `Flink\3.9-state-backends-deep-comparison.md`

**问题 #21** (第 580 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend.rocksdb.memory.man ...
    ^ (line: 2)
found duplicate key "state.backend.rocksdb.memory.managed" with value
- **错误行**: 2

**问题 #22** (第 601 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend.rocksdb.compaction ...
    ^ (line: 2)
found duplicate key "state.backend.rocksdb.compaction.style" with valu
- **错误行**: 2


### `Flink\data-types-complete-reference.md`

**问题 #6** (第 261 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0e0g02e8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.DataTypes;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp0e0g02e8TempValidat
- **错误行**: 3


### `Flink\elasticsearch-connector-guide.md`

**问题 #4** (第 248 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp278feldlTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.elasticsearch.sink.Elasticsearch7SinkBuilder;
^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #6** (第 325 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3nde9oxqTempValidation.java:4: 错误: 找不到符号
ElasticsearchSink<Event> esSink = new Elasticsearch7SinkBuilder<Event>()
^
  符号:   类 ElasticsearchSink
  位置: 类 TempValidat
- **错误行**: 4


### `Flink\flink-nexmark-benchmark-guide.md`

**问题 #2** (第 227 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgzh0o87gTempValidation.java:5: 错误: 找不到符号
Random random = new Random(SEED);
^
  符号:   类 Random
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpgzh0o87gT
- **错误行**: 5

**问题 #3** (第 235 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0e3eyzolTempValidation.java:5: 错误: 找不到符号
long eventTime = baseTime + (offsetSec * 1000);
                             ^
  符号:   变量 offsetSec
  位置: 类 TempValidation
- **错误行**: 5

**问题 #10** (第 371 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp21933oyrTempValidation.java:4: 错误: 找不到符号
tableEnv.getConfig().getConfiguration()
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #12** (第 395 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjz8cz09aTempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #15** (第 449 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc2f7nehsTempValidation.java:4: 错误: 需要';'
CREATE TABLE Person (
            ^
C:\Users\luyan\AppData\Local\Temp\tmpc2f7nehsTempValidation.java:5: 错误: 需要')'或','

- **错误行**: 4

**问题 #16** (第 485 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzqn2nzqxTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4


### `Flink\flink-state-backends-comparison.md`

**问题 #8** (第 487 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzul_w358TempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #9** (第 514 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp78rqs9idTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #10** (第 563 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw_sctbrbTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #14** (第 719 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx85a4l7eTempValidation.java:4: 错误: 找不到符号
config.set(RocksDBOptions.BLOCK_CACHE_SIZE, MemorySize.ofMebiBytes(256));
           ^
  符号:   变量 RocksDBOptions
  位置: 类 T
- **错误行**: 4

**问题 #16** (第 736 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp78683wuxTempValidation.java:3: 错误: 找不到符号
        config.set(CheckpointingOptions.INCREMENTAL_CHECKPOINTS, true);
                   ^
  符号:   变量 CheckpointingOptio
- **错误行**: 3

**问题 #18** (第 746 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzufkf3pnTempValidation.java:3: 错误: 找不到符号
        config.set(CheckpointingOptions.MAX_CONCURRENT_CHECKPOINTS, 1);
                   ^
  符号:   变量 CheckpointingOptio
- **错误行**: 3

**问题 #20** (第 759 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9qi8br97TempValidation.java:4: 错误: 找不到符号
config.set(CheckpointingOptions.LOCAL_RECOVERY, true);
           ^
  符号:   变量 CheckpointingOptions
  位置: 类 TempValidation
- **错误行**: 4


### `Flink\jdbc-connector-guide.md`

**问题 #4** (第 226 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeade7y6bTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcConnectionOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmpeade7y6bTempValida
- **错误行**: 3

**问题 #6** (第 292 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvqetoniyTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcInputFormat;
^
C:\Users\luyan\AppData\Local\Temp\tmpvqetoniyTempValidation.j
- **错误行**: 3


### `Flink\mongodb-connector-guide.md`

**问题 #4** (第 246 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8n7k17lgTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.source.MongoSource;
^
C:\Users\luyan\AppData\Local\Temp\tmp8n7k17lgTempValida
- **错误行**: 3

**问题 #5** (第 282 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp52d_g99dTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.source.MongoSource;
^
C:\Users\luyan\AppData\Local\Temp\tmp52d_g99dTempValida
- **错误行**: 3

**问题 #6** (第 315 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbmzrpzrfTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.sink.MongoSink;
^
C:\Users\luyan\AppData\Local\Temp\tmpbmzrpzrfTempValidation
- **错误行**: 3


### `Flink\pulsar-functions-integration.md`

**问题 #8** (第 217 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8g4guixuTempValidation.java:25: 错误: 非法的表达式开始
stats.addSink(new JdbcSink(...));
                           ^
1 个错误

- **错误行**: 25


### `Flink\pyflink-deep-guide.md`

**问题 #9** (第 388 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2


### `Flink\risingwave-integration-guide.md`

**问题 #6** (第 126 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprhnzw404TempValidation.java:4: 错误: 找不到符号
FlinkKafkaProducer<String> kafkaProducer = new FlinkKafkaProducer<>(
^
  符号:   类 FlinkKafkaProducer
  位置: 类 TempValidation
- **错误行**: 4

**问题 #9** (第 182 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp92t50pceTempValidation.java:4: 错误: 找不到符号
DebeziumSourceFunction<String> source = DebeziumSourceFunction.<String>builder()
^
  符号:   类 DebeziumSourceFunction
  位置:
- **错误行**: 4

**问题 #10** (第 193 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe30wjdabTempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.sqlQuery(
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpe30wjdabTe
- **错误行**: 4


### `Flink\state-backends-comparison.md`

**问题 #4** (第 240 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl3j6rifsTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.runtime.state.hashmap.HashMapStateBackend;
^
C:\Users\luyan\AppData\Local\Temp\tmpl3j6rifsTempV
- **错误行**: 3

**问题 #5** (第 273 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    state.backend: hashmap
    ^ (line: 4)
found duplicate key "state.backend" with value "rocksdb" (original value: "hashmap")

- **错误行**: 4

**问题 #6** (第 299 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpks30m5lrTempValidation.java:4: 错误: 非法的表达式开始
public void monitorStateBackend(RuntimeContext ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpks30m5lrTempValidation.jav
- **错误行**: 4


### `Knowledge\02-design-patterns\pattern-cep-complex-event.md`

**问题 #7** (第 331 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphmvyh3gsCEPState.java:4: 错误: 找不到符号
    List<NFAState> activeStates;
    ^
  符号:   类 List
  位置: 类 CEPState
C:\Users\luyan\AppData\Local\Temp\tmphmvyh3gsCEPState.jav
- **错误行**: 4

**问题 #10** (第 447 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptyalndchTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.CEP;
^
C:\Users\luyan\AppData\Local\Temp\tmptyalndchTempValidation.java:3: 错误: 不是语句
import
- **错误行**: 3

**问题 #11** (第 514 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph75cl12uTempValidation.java:4: 错误: 找不到符号
Pattern<SensorEvent, ?> failurePattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #12** (第 567 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpovpa7gsqTempValidation.java:4: 错误: 找不到符号
Pattern<LoginEvent, ?> bruteForcePattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 4

**问题 #13** (第 599 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplfi5aoshTempValidation.java:4: 错误: 找不到符号
Pattern<Event, ?> greedyPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #14** (第 615 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxl0wwrwvTempValidation.java:4: 错误: 找不到符号
Pattern<AlarmEvent, ?> shutdownPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #15** (第 639 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvgx4nj6gTempValidation.java:4: 错误: 找不到符号
OutputTag<String> timeoutTag = new OutputTag<String>("timeout"){};
^
  符号:   类 OutputTag
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 4

**问题 #17** (第 718 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyf7by9fcTempValidation.java:4: 错误: 找不到符号
Pattern<Event, ?> unoptimized = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpyf
- **错误行**: 4

**问题 #18** (第 740 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppo9yyx3gTempValidation.java:4: 错误: 非法的表达式开始
.within(Time.seconds(5))   // 太紧张
^
C:\Users\luyan\AppData\Local\Temp\tmppo9yyx3gTempValidation.java:10: 错误: 需要';'
.wit
- **错误行**: 4

**问题 #19** (第 753 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4p38upreTempValidation.java:4: 错误: 找不到符号
env.setStateBackend(new EmbeddedRocksDBStateBackend(true));
                        ^
  符号:   类 EmbeddedRocksDBStateBacken
- **错误行**: 4

**问题 #20** (第 768 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvc32qbp0TempValidation.java:4: 错误: 找不到符号
Pattern<Event, ?> inefficient = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpvc
- **错误行**: 4


### `Knowledge\02-design-patterns\pattern-log-analysis.md`

**问题 #5** (第 453 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbo2sdvtrTempValidation.java:61: 错误: 未命名变量 是预览功能，默认情况下禁用。
            .withTimestampAssigner((log, _) -> log.getTimestamp())

- **错误行**: 61

**问题 #6** (第 523 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkwqqe9_zTraceAnalysisFunction.java:2: 错误: 需要 class、interface、enum 或 record
unifiedLogs
^
1 个错误

- **错误行**: 2

**问题 #7** (第 589 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbg45p82xTempValidation.java:4: 错误: 找不到符号
DataStream<Alert> errorAlerts = unifiedLogs
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #8** (第 637 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphn4zy3plSlowRequestDetector.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<LatencyMetric> latencyMetrics = unifiedLogs
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2


### `Knowledge\02-design-patterns\pattern-realtime-feature-engineering.md`

**问题 #4** (第 346 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdz9j0vjbSessionAggregator.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Transaction> transactions = ...
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Loc
- **错误行**: 2


### `Knowledge\02-design-patterns\pattern-windowed-aggregation.md`

**问题 #3** (第 466 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyag3cfnmSumAggregate.java:1: 错误: 从发行版 9 开始, '_' 为关键字, 不能用作标识符
import org.apache.flink.streaming.api.scala._
                                            ^
C:\Users\
- **错误行**: 1

**问题 #4** (第 496 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp163pur3uAverageAggregate.java:3: 错误: 从发行版 9 开始, '_' 为关键字, 不能用作标识符
  .keyBy(_.sensorId)
         ^
C:\Users\luyan\AppData\Local\Temp\tmp163pur3uAverageAggregate.jav
- **错误行**: 3

**问题 #10** (第 654 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqeq804u8TopNFunction.java:1: 错误: 需要';'
import org.apache.flink.streaming.api.windowing.triggers.ContinuousTrigger

- **错误行**: 1

**问题 #11** (第 704 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw7ow7hnsTempValidation.java:16: 错误: 未命名变量 是预览功能，默认情况下禁用。
      .withTimestampAssigner((pv, _) -> pv.timestamp)
                                  ^
  （请使用 --enable-
- **错误行**: 16


### `Knowledge\03-business-patterns\data-mesh-streaming-architecture-2026.md`

**问题 #5** (第 372 行, 语言: yaml)

- **错误**: while scanning a block scalar
  in "<unicode string>", line 15, column 19:
        completeness: > 99.9%
                      ^ (line: 15)
expected a comment or a line break, but found '9'
  in "<uni
- **错误行**: 15


### `Knowledge\03-business-patterns\fintech-realtime-risk-control.md`

**问题 #6** (第 277 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdzteombzTempValidation.java:4: 错误: 非法的表达式开始
public RiskDecision evaluate(Transaction txn) {
^
C:\Users\luyan\AppData\Local\Temp\tmpdzteombzTempValidation.java:28:
- **错误行**: 4


### `Knowledge\03-business-patterns\netflix-streaming-pipeline.md`

**问题 #12** (第 357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpckxol6kpTempValidation.java:4: 错误: 找不到符号
DataStream<PlayEvent> plays = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpckxol
- **错误行**: 4


### `Knowledge\03-business-patterns\uber-realtime-platform.md`

**问题 #27** (第 736 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfe5ril48SurgePricingJob.java:9: 错误: 非法的表达式开始
        DataStream<DriverEvent> driverEvents = env.addSource(...);

- **错误行**: 9

**问题 #28** (第 868 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp71i56ylfFraudDetectionJob.java:8: 错误: 非法的表达式开始
        DataStream<TripEvent> trips = env.addSource(...);
                                                    ^
C:\U
- **错误行**: 8


### `Knowledge\04-technology-selection\engine-selection-guide.md`

**问题 #5** (第 675 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzzaye1f4TempValidation.java:4: 错误: 找不到符号
env.setBufferTimeout(5);  // 5ms 缓冲区超时
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpzzaye1
- **错误行**: 4


### `Knowledge\04-technology-selection\flink-vs-risingwave.md`

**问题 #8** (第 402 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1yghn4hrTempValidation.java:4: 错误: 非法的表达式开始
DataStream<Event> stream = env.addSource(...);
                                         ^
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #10** (第 550 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwf3jdaaeTempValidation.java:4: 错误: 找不到符号
env.setBufferTimeout(0);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpwf3jdaaeTempValidati
- **错误行**: 4


### `Knowledge\05-mapping-guides\migration-guides\05.1-spark-streaming-to-flink-migration.md`

**问题 #5** (第 166 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpooj4zzrfTempValidation.java:4: 错误: 找不到符号
env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);
                                ^
  符号:   变量 TimeCharacteri
- **错误行**: 4

**问题 #9** (第 244 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyfp0c6xtTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpyf
- **错误行**: 3

**问题 #11** (第 284 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqettdfnnCountFunction.java:29: 错误: 需要 class、interface、enum 或 record
keyedStream.process(new CountFunction());
^
1 个错误

- **错误行**: 29

**问题 #13** (第 331 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy91c7ubpTempValidation.java:3: 错误: 找不到符号
        DataStream<Tuple2<String, Integer>> windowedCounts = keyedStream
        ^
  符号:   类 DataStream
  位置: 类 TempValida
- **错误行**: 3

**问题 #15** (第 350 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjes2udd0TempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000); // 60秒间隔
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpjes2
- **错误行**: 4

**问题 #19** (第 446 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2r5d3xxiTempValidation.java:9: 错误: 非法的类型开始
    .process(new KeyedBroadcastProcessFunction() {...});
                                                  ^
1 个错误

- **错误行**: 9

**问题 #20** (第 460 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_3yi1i7tTempValidation.java:4: 错误: 找不到符号
env.setRestartStrategy(RestartStrategies.fixedDelayRestart(3, Time.seconds(10)));
^
  符号:   变量 env
  位置: 类 TempValidation

- **错误行**: 4

**问题 #21** (第 472 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7sz131b3TempValidation.java:4: 错误: 找不到符号
OutputTag<String> lateDataTag = new OutputTag<String>("late-data"){};
^
  符号:   类 OutputTag
  位置: 类 TempValidation
C:\User
- **错误行**: 4


### `Knowledge\05-mapping-guides\migration-guides\05.2-kafka-streams-to-flink-migration.md`

**问题 #5** (第 144 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0nlycm73TempValidation.java:4: 错误: 找不到符号
ReadOnlyKeyValueStore<String, Long> store =
^
  符号:   类 ReadOnlyKeyValueStore
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #6** (第 164 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz10c_h63TempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #7** (第 177 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp01iyozt0TempValidation.java:3: 错误: 找不到符号
        KafkaSource<MyEvent> source = KafkaSource.<MyEvent>builder()
        ^
  符号:   类 KafkaSource
  位置: 类 TempValidatio
- **错误行**: 3

**问题 #8** (第 231 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgpxydm3aTempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #9** (第 252 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfkexlzobTempValidation.java:3: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 3

**问题 #10** (第 301 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg1zcit3eTempValidation.java:3: 错误: 找不到符号
        KTable<String, Long> wordCounts = source
        ^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #11** (第 312 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2n80nsltCountAggregate.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Tuple2<String, Long>> wordCounts = source
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 1

**问题 #12** (第 351 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp92e144p0TempValidation.java:3: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3

**问题 #13** (第 364 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdm01_h9zTempValidation.java:4: 错误: 找不到符号
DataStream<Customer> customerStream = env.fromSource(
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4

**问题 #21** (第 583 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4bp8d4hoTempValidation.java:3: 错误: 非法的表达式开始
DataStream<Event> stream = ...;
                           ^
1 个错误

- **错误行**: 3


### `Knowledge\05-mapping-guides\migration-guides\05.3-storm-to-flink-migration.md`

**问题 #1** (第 84 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph4qurwloTempValidation.java:4: 错误: 找不到符号
Map<String, Object> state = new HashMap<>();
^
  符号:   类 Map
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmph
- **错误行**: 4

**问题 #2** (第 92 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg1sp5jttTempValidation.java:4: 错误: 找不到符号
ValueStateDescriptor<Long> descriptor = new ValueStateDescriptor<>("count", Types.LONG);
^
  符号:   类 ValueStateDescriptor

- **错误行**: 4

**问题 #4** (第 126 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk2dejvecTempValidation.java:5: 错误: 找不到符号
    .fieldsGrouping("split", new Fields("word"));
                                 ^
  符号:   类 Fields
  位置: 类 TempValidati
- **错误行**: 5

**问题 #8** (第 203 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzhnouhsfTempValidation.java:4: 错误: 非法的表达式开始
stream.keyBy(...)
             ^
C:\Users\luyan\AppData\Local\Temp\tmpzhnouhsfTempValidation.java:6: 错误: 非法的类型开始
    .a
- **错误行**: 4

**问题 #9** (第 254 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaor_a1zhSentenceSpout.java:64: 错误: 未命名类 是预览功能，默认情况下禁用。
TopologyBuilder builder = new TopologyBuilder();
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\
- **错误行**: 64

**问题 #10** (第 330 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa2dmew96WordCount.java:33: 错误: 未命名类 是预览功能，默认情况下禁用。
public static void main(String[] args) throws Exception {
              ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错
- **错误行**: 33

**问题 #12** (第 422 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbtnufi3dTempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #14** (第 464 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7oc_v16fTempValidation.java:5: 错误: 找不到符号
    .aggregate(new AggregateFunction<Value, Accumulator, Result>() {
                   ^
  符号:   类 AggregateFunction
  位置
- **错误行**: 5

**问题 #23** (第 701 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptu7l5_waTempValidation.java:8: 错误: 找不到符号
DataStream<Query> queries = env.addSource(new QuerySource());
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 8


### `Knowledge\05-mapping-guides\migration-guides\05.4-flink-1x-to-2x-migration.md`

**问题 #4** (第 144 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfn6vi3a4TempValidation.java:4: 错误: 找不到符号
ValueStateDescriptor<Long> descriptor = new ValueStateDescriptor<>(
^
  符号:   类 ValueStateDescriptor
  位置: 类 TempValidatio
- **错误行**: 4

**问题 #5** (第 181 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl2d6zngnTempValidation.java:23: 错误: 非法的表达式开始
counts.sinkTo(FileSink.forRowFormat(...).build());
                                    ^
C:\Users\luyan\AppData\Local\
- **错误行**: 23

**问题 #6** (第 228 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend: rocksdb
    ^ (line: 2)
found duplicate key "state.backend" with value "rocksdb" (original value: "rocksdb")

- **错误行**: 2

**问题 #9** (第 341 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvh368ca0TempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<String> consumer = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #10** (第 355 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1g46xmmzTempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #11** (第 376 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpawi90begTempValidation.java:4: 错误: 找不到符号
FlinkKafkaProducer<String> producer = new FlinkKafkaProducer<>(
^
  符号:   类 FlinkKafkaProducer
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #12** (第 390 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp80gmrfj4TempValidation.java:4: 错误: 找不到符号
KafkaSink<String> sink = KafkaSink.<String>builder()
^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #13** (第 408 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp67hb70nkTempValidation.java:4: 错误: 找不到符号
EnvironmentSettings settings = EnvironmentSettings
^
  符号:   类 EnvironmentSettings
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #14** (第 426 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppadg5ofkTempValidation.java:4: 错误: 找不到符号
EnvironmentSettings settings = EnvironmentSettings
^
  符号:   类 EnvironmentSettings
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #15** (第 444 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbdasod86TempValidation.java:3: 错误: 找不到符号
        ValueStateDescriptor<Long> descriptor = new ValueStateDescriptor<>("count", Long.class);
        ^
  符号:   类 Value
- **错误行**: 3

**问题 #16** (第 459 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb3751pitTempValidation.java:3: 错误: 找不到符号
        ValueStateDescriptor<Long> descriptor = new ValueStateDescriptor<>("count", Long.class);
        ^
  符号:   类 Value
- **错误行**: 3


### `Knowledge\05-mapping-guides\migration-guides\05.5-batch-to-streaming-migration.md`

**问题 #2** (第 120 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkdyaywzwTempValidation.java:7: 错误: 找不到符号
    .aggregate(new AggregateFunction<Order, OrderAcc, OrderResult>() {
                   ^
  符号:   类 AggregateFunction

- **错误行**: 7

**问题 #5** (第 182 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsy4o0beqTempValidation.java:3: 错误: 找不到符号
        WatermarkStrategy<Event> strategy = WatermarkStrategy
        ^
  符号:   类 WatermarkStrategy
  位置: 类 TempValidation
- **错误行**: 3

**问题 #6** (第 194 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps37b9em3TempValidation.java:4: 错误: 找不到符号
List<Data> allData = readAllData();
^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmps37b9em3T
- **错误行**: 4

**问题 #8** (第 225 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv9bbst08TempValidation.java:4: 错误: 找不到符号
for (Record record : batchData) {
                     ^
  符号:   变量 batchData
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #9** (第 234 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf1_vgwx_TempValidation.java:10: 错误: 找不到符号
.process(new TimeWindowFunction());
             ^
  符号:   类 TimeWindowFunction
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 10

**问题 #11** (第 305 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7km7d282TempValidation.java:4: 错误: 找不到符号
DataStream<Row> stream = env.fromSource(
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4

**问题 #13** (第 344 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpodfu8mv4TempValidation.java:3: 错误: 非法的表达式开始
DataStream<Sale> sales = ...;
                         ^
1 个错误

- **错误行**: 3

**问题 #15** (第 387 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoo1dzsfvTempValidation.java:4: 错误: 非法的表达式开始
DataStream<Order> orders = ...;
                           ^
C:\Users\luyan\AppData\Local\Temp\tmpoo1dzsfvTempValidatio
- **错误行**: 4

**问题 #16** (第 408 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1y0ksdr_TempValidation.java:4: 错误: 找不到符号
MapStateDescriptor<String, Customer> descriptor =
^
  符号:   类 MapStateDescriptor
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4

**问题 #18** (第 442 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5hzbjyc4DeduplicateFunction.java:33: 错误: 需要 class、interface、enum 或 record
stream.keyBy(e -> e.getUserId() + "_" + e.getEventType())
^
1 个错误

- **错误行**: 33

**问题 #20** (第 495 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3k795ifcTopNFunction.java:34: 错误: 需要 class、interface、enum 或 record
stream.keyBy(ProductSale::getCategory)
^
1 个错误

- **错误行**: 34

**问题 #25** (第 635 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7qsltlkpTempValidation.java:4: 错误: 非法的表达式开始
stream.keyBy(...)  // 分区键
             ^
1 个错误

- **错误行**: 4

**问题 #26** (第 650 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_6b6v79nTempValidation.java:13: 错误: 非法的表达式开始
.aggregate(...);
           ^
1 个错误

- **错误行**: 13

**问题 #27** (第 672 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplktcr6ngTempValidation.java:5: 错误: 找不到符号
    stream,
    ^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmplktcr6ngTempValidation.jav
- **错误行**: 5


### `Knowledge\05-mapping-guides\streaming-etl-tools-landscape-2026.md`

**问题 #7** (第 607 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp813zn4teTempValidation.java:4: 错误: 找不到符号
Table orders = tEnv.fromDataStream(
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp813zn4te
- **错误行**: 4


### `Knowledge\05-mapping-guides\streaming-sql-engines-2026-comparison.md`

**问题 #12** (第 788 行, 语言: sql)

- **错误**: 可能的语法问题: -- 4. 服务查询需直接查询SINK数据库
-- FLINK SQL本身不提供物化视图查询服务...


### `Knowledge\05-mapping-guides\struct-to-flink-mapping.md`

**问题 #1** (第 205 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz71nyzhhTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
^
  符号:   类 StreamExecutionEnvironm
- **错误行**: 4

**问题 #2** (第 258 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmjhri5w6TempValidation.java:6: 错误: 找不到符号
WatermarkStrategy<Event> strategy = WatermarkStrategy
^
  符号:   类 WatermarkStrategy
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 6

**问题 #3** (第 301 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx3vwbb4iTempValidation.java:6: 错误: 找不到符号
env.enableCheckpointing(60000);  // Checkpoint 周期
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 6

**问题 #4** (第 349 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsoge4gfwTempValidation.java:7: 错误: 找不到符号
env.setStateBackend(new HashMapStateBackend());
                        ^
  符号:   类 HashMapStateBackend
  位置: 类 TempValida
- **错误行**: 7

**问题 #5** (第 390 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6biojtzaTempValidation.java:7: 错误: 找不到符号
FlinkKafkaConsumer<Event> source = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\User
- **错误行**: 7

**问题 #8** (第 498 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuocg40b_EventTypeInfo.java:20: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Tuple2<String, Integer>> keyedStream = stream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 20

**问题 #9** (第 693 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp11smfhbcTempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env =
        ^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3

**问题 #10** (第 753 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcavvlyeyTempValidation.java:4: 错误: 找不到符号
WatermarkStrategy<Event> strategy = WatermarkStrategy
^
  符号:   类 WatermarkStrategy
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 4

**问题 #11** (第 795 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw89kk900TempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpw89kk900TempV
- **错误行**: 4


### `Knowledge\05-migrations\kafka-streams-to-flink-guide.md`

**问题 #9** (第 462 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk0_ghplmTempValidation.java:4: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #10** (第 478 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptdcbchh8TempValidation.java:4: 错误: 找不到符号
DataStream<Order> orders = env.fromSource(
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #11** (第 520 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6r5bduzkTempValidation.java:4: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #12** (第 537 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx8q5z9uqTempValidation.java:4: 错误: 找不到符号
DataStream<Customer> customerStream = env.fromSource(
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4

**问题 #13** (第 578 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdygtieoiTempValidation.java:4: 错误: 找不到符号
KStream<String, Click> clicks = builder.stream("clicks");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #14** (第 590 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj91q2wpdTempValidation.java:3: 错误: 找不到符号
        DataStream<Tuple2<String, Long>> clickCounts = clicks
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Use
- **错误行**: 3

**问题 #15** (第 599 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi6rkrzx6TempValidation.java:4: 错误: 找不到符号
KTable<Windowed<String>, Long> slidingCounts = clicks
^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #16** (第 609 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp61igvtesTempValidation.java:3: 错误: 找不到符号
        DataStream<Tuple2<String, Long>> slidingCounts = clicks
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\U
- **错误行**: 3

**问题 #17** (第 618 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplzsrvxr3TempValidation.java:4: 错误: 找不到符号
KTable<Windowed<String>, Long> sessionCounts = clicks
^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #18** (第 628 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2kv_a0chTempValidation.java:3: 错误: 找不到符号
        DataStream<Tuple2<String, Long>> sessionCounts = clicks
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\U
- **错误行**: 3

**问题 #21** (第 727 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqr_wf8trTempValidation.java:3: 错误: 找不到符号
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "my-streams-app");
                  ^
  符号:   变量 StreamsConfig
  位
- **错误行**: 3

**问题 #22** (第 734 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpznoba0edTempValidation.java:3: 错误: 找不到符号
        env.execute("my-streams-app");  // 作业名称
        ^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 3

**问题 #23** (第 754 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpus9u7dukTempValidation.java:3: 错误: 找不到符号
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092");
                  ^
  符号:   变量 StreamsConfig
  位置
- **错误行**: 3

**问题 #24** (第 762 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppof1ohmbTempValidation.java:3: 错误: 找不到符号
        KafkaSource<String> source = KafkaSource.<String>builder()
        ^
  符号:   类 KafkaSource
  位置: 类 TempValidation

- **错误行**: 3

**问题 #25** (第 782 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1ktl8_3_TempValidation.java:3: 错误: 找不到符号
        props.put(StreamsConfig.STATE_DIR_CONFIG, "/var/lib/kafka-streams");
                  ^
  符号:   变量 StreamsConfig

- **错误行**: 3

**问题 #26** (第 789 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgf9ojcqjTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4

**问题 #27** (第 803 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9f24qo9pTempValidation.java:4: 错误: 找不到符号
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, "exactly_once_v2");
          ^
  符号:   变量 StreamsConfig
  位置: 类 Temp
- **错误行**: 4

**问题 #28** (第 813 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa752sk3rTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpa752sk3rTempV
- **错误行**: 4

**问题 #29** (第 832 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp71bimvegTempValidation.java:4: 错误: 找不到符号
KafkaStreams streams = new KafkaStreams(builder.build(), props);
^
  符号:   类 KafkaStreams
  位置: 类 TempValidation
C:\Users\
- **错误行**: 4

**问题 #32** (第 912 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8oe941t2TempValidation.java:4: 错误: 找不到符号
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, "exactly_once_v2");
          ^
  符号:   变量 StreamsConfig
  位置: 类 Temp
- **错误行**: 4

**问题 #34** (第 979 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxfeyfgw5TempValidation.java:4: 错误: 找不到符号
KStream<String, Event> repartitioned = events
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #35** (第 993 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6j7l_0dlTempValidation.java:4: 错误: 找不到符号
DataStream<Event> repartitioned = events
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4

**问题 #37** (第 1068 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2rx8ozbhDualWriteValidation.java:40: 错误: 非法的表达式开始
            .setRecordSerializer(...)
                                 ^
C:\Users\luyan\AppData\Local\Temp\tmp2rx
- **错误行**: 40

**问题 #44** (第 1309 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpndhbyaqdTempValidation.java:10: 错误: 非法的表达式开始
DataStream<Event> stream = env.fromSource(...)
                                          ^
C:\Users\luyan\AppData\Loca
- **错误行**: 10

**问题 #47** (第 1401 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcdmf2v58TempValidation.java:3: 错误: 非法的表达式开始
DataStream<Event> stream = ...;
                           ^
1 个错误

- **错误行**: 3

**问题 #48** (第 1426 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7mchx_j3TempValidation.java:3: 错误: 找不到符号
        KafkaSource<String> source = KafkaSource.<String>builder()
        ^
  符号:   类 KafkaSource
  位置: 类 TempValidation

- **错误行**: 3


### `Knowledge\06-frontier\a2a-protocol-agent-communication.md`

**问题 #8** (第 352 行, 语言: python)

- **错误**: SyntaxError: 'async for' outside async function
- **错误行**: 8


### `Knowledge\06-frontier\ai-agent-streaming-architecture.md`

**问题 #9** (第 818 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwhr8o14uTempValidation.java:4: 错误: 找不到符号
DataStream<Context> enrichedContext = userMessages
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 4


### `Knowledge\06-frontier\cloud-edge-continuum.md`

**问题 #5** (第 451 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd5tam670AdaptivePlacement.java:4: 错误: 找不到符号
    Placement decide(Task task, SystemState state) {
                     ^
  符号:   类 Task
  位置: 类 AdaptivePlacement
C:
- **错误行**: 4


### `Knowledge\06-frontier\materialize-comparison-guide.md`

**问题 #7** (第 383 行, 语言: sql)

- **错误**: 可能的语法问题: -- 订阅实时变更
COPY (SUBSCRIBE TO MATERIALIZED_VIEW) TO...

**问题 #12** (第 676 行, 语言: sql)

- **错误**: 可能的语法问题: -- 订阅库存变更
COPY (SUBSCRIBE TO CURRENT_INVENTORY) TO...


### `Knowledge\06-frontier\mcp-protocol-agent-streaming.md`

**问题 #11** (第 446 行, 语言: python)

- **错误**: SyntaxError: 'await' outside function
- **错误行**: 41


### `Knowledge\06-frontier\multimodal-ai-streaming-architecture.md`

**问题 #3** (第 160 行, 语言: python)

- **错误**: SyntaxError: invalid decimal literal
- **错误行**: 2

**问题 #7** (第 303 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 57


### `Knowledge\06-frontier\multimodal-streaming-architecture.md`

**问题 #12** (第 391 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 118

**问题 #13** (第 533 行, 语言: java)

- **错误**: 括号不匹配: (=40, )=43

**问题 #14** (第 593 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 55


### `Knowledge\06-frontier\real-time-rag-architecture.md`

**问题 #4** (第 299 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaew8nwtqEmbeddingAsyncFn.java:2: 错误: 找不到符号
class EmbeddingAsyncFn extends AsyncFunction<Document, Vector> {
                               ^
  符号: 类 AsyncFunction

- **错误行**: 2

**问题 #5** (第 313 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5jkb_g37VectorBulkSink.java:2: 错误: 找不到符号
class VectorBulkSink extends RichSinkFunction<Vector> {
                             ^
  符号: 类 RichSinkFunction
C:\Users\l
- **错误行**: 2


### `Knowledge\06-frontier\realtime-ai-streaming-2026.md`

**问题 #16** (第 588 行, 语言: java)

- **错误**: 括号不匹配: (=37, )=41


### `Knowledge\06-frontier\realtime-data-mesh-practice.md`

**问题 #9** (第 344 行, 语言: sql)

- **错误**: 可能的语法问题: -- 结果: F → E → B → [A, C]...


### `Knowledge\06-frontier\realtime-data-product-architecture.md`

**问题 #13** (第 403 行, 语言: yaml)

- **错误**: while scanning a block scalar
  in "<unicode string>", line 36, column 15:
          target: > 99.999%
                  ^ (line: 36)
expected a comment or a line break, but found '9'
  in "<unicode s
- **错误行**: 36


### `Knowledge\06-frontier\realtime-data-quality-validation.md`

**问题 #5** (第 263 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps9xcmwe8TempValidation.java:4: 错误: 找不到符号
DataStream<Event> validatedStream = source
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4


### `Knowledge\06-frontier\realtime-digital-twin-streaming.md`

**问题 #5** (第 257 行, 语言: python)

- **错误**: SyntaxError: invalid decimal literal
- **错误行**: 2

**问题 #6** (第 269 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 7


### `Knowledge\06-frontier\risingwave-integration-guide.md`

**问题 #6** (第 482 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppdch1j2bTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
^
  符号:   类 StreamExecutionEnvironm
- **错误行**: 4

**问题 #10** (第 597 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdvbb4145TempValidation.java:4: 错误: 找不到符号
DataStream<OrderStats> statsStream = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4

**问题 #16** (第 809 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5xujv_fhTempValidation.java:4: 错误: 非法的表达式开始
DataStream<Order> orders = env.addSource(...);
                                         ^
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #20** (第 950 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnx4a1_ugTempValidation.java:4: 错误: 非法的表达式开始
DataStream<UserEvent> events = env.addSource(...);
                                             ^
1 个错误

- **错误行**: 4

**问题 #31** (第 1365 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 7, column 1:
    flink savepoint <job-id>
    ^ (line: 7)
- **错误行**: 7


### `Knowledge\06-frontier\rust-streaming-ecosystem.md`

**问题 #13** (第 755 行, 语言: sql)

- **错误**: 可能的语法问题: -- 返回: 10000.00 (严格串行化保证)

-- 即使在高并发写入下，也不会读到中间状态
...


### `Knowledge\06-frontier\streaming-access-control.md`

**问题 #9** (第 670 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4sb1okiyLineageTracker.java:4: 错误: 找不到符号
    void track(DataRecord record, Operator op) {
               ^
  符号:   类 DataRecord
  位置: 类 LineageTracker
C:\Users\luy
- **错误行**: 4

**问题 #13** (第 777 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy5hqvssbLineageTrackingFunction.java:2: 错误: 找不到符号
class LineageTrackingFunction extends ProcessFunction<Record, Record> {
                                      ^

- **错误行**: 2


### `Knowledge\06-frontier\streaming-database-ecosystem-comparison.md`

**问题 #6** (第 516 行, 语言: sql)

- **错误**: 可能的语法问题: -- 图遍历递归（有限支持）
   WITH RECURSIVE PATHS AS (...)...


### `Knowledge\06-frontier\streaming-graph-processing-tgn.md`

**问题 #7** (第 347 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqi9rd075TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.graph.streaming.*;
^
C:\Users\luyan\AppData\Local\Temp\tmpqi9rd075TempValidation.java:3: 错误: 需要
- **错误行**: 3

**问题 #8** (第 396 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 65


### `Knowledge\06-frontier\streaming-materialized-view-architecture.md`

**问题 #7** (第 369 行, 语言: sql)

- **错误**: 可能的语法问题: -- 自动增量更新
-- 当SALES表发生INSERT/UPDATE/DELETE时，物化视图自动...


### `Knowledge\06-frontier\streaming-security-compliance.md`

**问题 #5** (第 446 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwdajqszaTempValidation.java:3: 错误: 不是语句
KafkaServer {
^
C:\Users\luyan\AppData\Local\Temp\tmpwdajqszaTempValidation.java:3: 错误: 需要';'
KafkaServer {
           ^
C:
- **错误行**: 3


### `Knowledge\06-frontier\streaming-slo-definition.md`

**问题 #4** (第 297 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6o0raf5qTempValidation.java:4: 错误: 找不到符号
Counter slo_violations_total = Counter.build()
^
  符号:   类 Counter
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #7** (第 382 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 5


### `Knowledge\06-frontier\temporal-flink-layered-architecture.md`

**问题 #9** (第 618 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6b4xxtqqTemporalStateLookup.java:5: 错误: 未命名类 是预览功能，默认情况下禁用。
public WorkflowState getWorkflowState() {
       ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 5


### `Knowledge\06-frontier\wasm-dataflow-patterns.md`

**问题 #26** (第 1395 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnii3in_0WasmMapFunction.java:22: 错误: 非法的表达式开始
        byte[] state = getRuntimeContext().getState(...).value();

- **错误行**: 22

**问题 #50** (第 2352 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpskwuzvxyWasmScalarFunction.java:12: 错误: 需要';'
    private val runtime = new WasmUdfRuntime()
                                              ^
C:\Users\luyan\AppData
- **错误行**: 12


### `Knowledge\06-frontier\web3-blockchain-streaming-architecture.md`

**问题 #7** (第 374 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp564ya0xuTempValidation.java:4: 错误: 找不到符号
Pattern<DeFiEvent, ?> flashLoanAttackPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #8** (第 420 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8lxgb4dbTempValidation.java:4: 错误: 找不到符号
ValueStateDescriptor<RiskProfile> riskStateDesc =
^
  符号:   类 ValueStateDescriptor
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #9** (第 478 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnvptrd1yTempValidation.java:4: 错误: 找不到符号
DataStream<NFTMetrics> floorPriceStream = nftEventStream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppD
- **错误行**: 4


### `Knowledge\07-best-practices\07.01-flink-production-checklist.md`

**问题 #3** (第 223 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd8y0ovc9TempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000); // 1分钟间隔
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpd8y0
- **错误行**: 4

**问题 #4** (第 249 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzglb2kzgTempValidation.java:4: 错误: 找不到符号
DataStream<Event> withWatermark = stream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4

**问题 #7** (第 370 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp904fdf0jTempValidation.java:4: 错误: 非法的表达式开始
private static final Logger LOG = LoggerFactory.getLogger(MyFunction.class);
^
C:\Users\luyan\AppData\Local\Temp\tmp904
- **错误行**: 4

**问题 #11** (第 558 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmposebvu5yTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(10000);  // 10s 间隔
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpos
- **错误行**: 4

**问题 #12** (第 569 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgeb75jmjTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(300000);  // 5min 间隔
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4


### `Knowledge\07-best-practices\07.02-performance-tuning-patterns.md`

**问题 #9** (第 352 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy_tsd5ljTempValidation.java:10: 错误: 需要';'
val descriptor = new ValueStateDescriptor[Array[Byte]](
                                                      ^
C:\Users\
- **错误行**: 10

**问题 #13** (第 466 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 5, column 1:
    taskmanager.memory.process.size: 4gb
    ^ (line: 5)
found duplicate key "taskmanager.memory.process.size" with value "32gb"
- **错误行**: 5


### `Knowledge\07-best-practices\07.04-cost-optimization-patterns.md`

**问题 #5** (第 213 行, 语言: yaml)

- **错误**: while scanning a simple key
  in "<unicode string>", line 31, column 3:
      ---
      ^ (line: 31)
could not find expected ':'
  in "<unicode string>", line 32, column 3:
      apiVersion: autoscali
- **错误行**: 31

**问题 #8** (第 346 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt3x2jtvyTempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #9** (第 365 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 20


### `Knowledge\07-best-practices\07.05-security-hardening-guide.md`

**问题 #3** (第 213 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    security.kerberos.login.keytab:  ...
    ^ (line: 4)
found duplicate key "security.kerberos.login.contexts" with value "Cli
- **错误行**: 4

**问题 #13** (第 529 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprs2ko1tmTempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `Knowledge\07-best-practices\07.07-testing-strategies-complete.md`

**问题 #4** (第 142 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp91regl8vTempValidation.java:5: 错误: 需要';'
public void badTest() {
                   ^
C:\Users\luyan\AppData\Local\Temp\tmp91regl8vTempValidation.java:12: 错误: 需要';
- **错误行**: 5

**问题 #6** (第 232 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxsrn507nTempValidation.java:5: 错误: 需要';'
public void flakyTest() {
                     ^
C:\Users\luyan\AppData\Local\Temp\tmpxsrn507nTempValidation.java:13: 错误:
- **错误行**: 5


### `Knowledge\08-standards\streaming-data-governance.md`

**问题 #6** (第 203 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1osj071iTempValidation.java:5: 错误: 不是语句
  "type": "record",
  ^
C:\Users\luyan\AppData\Local\Temp\tmp1osj071iTempValidation.java:5: 错误: 需要';'
  "type": "record",

- **错误行**: 5

**问题 #9** (第 267 行, 语言: sql)

- **错误**: 可能的语法问题: -- 血缘输出:
-- FINAL_AMOUNT → 依赖: [ORDERS.AMOUNT]
-- ...

**问题 #11** (第 320 行, 语言: sql)

- **错误**: 可能的语法问题: -- 授权表级权限
GRANT SELECT ON TABLE USER_EVENTS TO ROL...

**问题 #12** (第 338 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6aat6do_MaskPII.java:18: 错误: 需要 class、interface、enum 或 record
SELECT
^
C:\Users\luyan\AppData\Local\Temp\tmp6aat6do_MaskPII.java:20: 错误: 未结束的字符文字
    MaskPII(email
- **错误行**: 18


### `Knowledge\08-standards\streaming-security-compliance.md`

**问题 #7** (第 491 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd5n51mceTempValidation.java:4: 错误: 找不到符号
TableEnvironment tEnv = TableEnvironment.create(EnvironmentSettings.inStreamingMode());
^
  符号:   类 TableEnvironment
  位置:
- **错误行**: 4

**问题 #10** (第 600 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqo_zr7z5TempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpqo
- **错误行**: 4


### `Knowledge\10-case-studies\ecommerce\10.2.3-big-promotion-realtime-dashboard.md`

**问题 #19** (第 1526 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 9, column 12:
      websocket: {
               ^ (line: 9)
- **错误行**: 9
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Knowledge\10-case-studies\finance\10.1.1-realtime-anti-fraud-system.md`

**问题 #3** (第 328 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwgdzy96pRealtimeAntiFraudEngine.java:189: 错误: 未命名变量 是预览功能，默认情况下禁用。
                .whenComplete((_, error) -> {
                               ^
  （请使用 --enable-p
- **错误行**: 189


### `Knowledge\10-case-studies\finance\10.1.4-realtime-payment-risk-control.md`

**问题 #8** (第 1010 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_g2o5t8zRealtimePaymentRiskControlEngine.java:250: 错误: 未命名变量 是预览功能，默认情况下禁用。
                .whenComplete((_, error) -> {
                               ^
  （请使用 -
- **错误行**: 250

**问题 #9** (第 1399 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw_eun47kTempValidation.java:4: 错误: 需要';'
       .withIdleness(Duration.ofMinutes(1))
                                           ^
1 个错误

- **错误行**: 4

**问题 #10** (第 1414 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1ojhu3qiTempValidation.java:4: 错误: 找不到符号
   DataStream<ModelUpdate> modelUpdates = env.addSource(new ModelUpdateSource());
   ^
  符号:   类 DataStream
  位置: 类 TempVa
- **错误行**: 4


### `Knowledge\10-case-studies\iot\10.3.1-smart-manufacturing.md`

**问题 #4** (第 347 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy3o6oznvTempValidation.java:4: 错误: 找不到符号
Pattern<SensorData, ?> vibrationPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4


### `Knowledge\10-case-studies\iot\10.3.3-predictive-maintenance-manufacturing.md`

**问题 #5** (第 635 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg6ak8v6jTimeSeriesFeatureExtractor.java:5: 错误: 找不到符号
class TimeSeriesFeatureExtractor extends KeyedProcessFunction<String, SensorReading, FeatureVector> {

- **错误行**: 5


### `Knowledge\98-exercises\exercise-02-flink-basics.md`

**问题 #2** (第 94 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6dv3m9pzTempValidation.java:3: 错误: 找不到符号
        DataStream<Event> stream = env
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 3

**问题 #3** (第 166 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfey0g3w_WordCount.java:87: 错误: 需要 class、interface、enum 或 record
*/
^
1 个错误

- **错误行**: 87

**问题 #5** (第 317 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpixw0lp3bTempValidation.java:7: 错误: 找不到符号
    .addSink(new MySink());
                 ^
  符号:   类 MySink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 7


### `Knowledge\98-exercises\exercise-03-checkpoint-analysis.md`

**问题 #1** (第 60 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyli7gj9iTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);  // 1分钟
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpyli7g
- **错误行**: 4

**问题 #5** (第 304 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx90tp022UnalignedCheckpointConfig.java:59: 错误: 需要 class、interface、enum 或 record
*/
^
1 个错误

- **错误行**: 59


### `Knowledge\98-exercises\exercise-05-pattern-implementation.md`

**问题 #1** (第 60 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu4b0nkhiTempValidation.java:4: 错误: 找不到符号
Pattern<LoginEvent, ?> pattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpu
- **错误行**: 4


### `Knowledge\98-exercises\quick-ref-security-compliance.md`

**问题 #8** (第 296 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmperbkd_egTempValidation.java:18: 错误: 需要';'
""")
    ^
C:\Users\luyan\AppData\Local\Temp\tmperbkd_egTempValidation.java:29: 错误: 需要';'
""")
    ^
2 个错误

- **错误行**: 18


### `Knowledge\98-exercises\quick-ref-temporal-flink.md`

**问题 #8** (第 363 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpskza9ipzTemporalStateLookup.java:3: 错误: 未命名类 是预览功能，默认情况下禁用。
public WorkflowState getWorkflowState() {
       ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 3


### `Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.01-flink-2x-architecture.md`

**问题 #3** (第 292 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8gya6lycTempValidation.java:4: 错误: 找不到符号
   state.getAsync(key)
                  ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp8gya
- **错误行**: 4

**问题 #5** (第 326 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwx8sboa3TempValidation.java:4: 错误: 找不到符号
if (backpressureRatio > 0.5 && latencyP99 > targetLatency) {
    ^
  符号:   变量 backpressureRatio
  位置: 类 TempValidation
C:\
- **错误行**: 4


### `Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.02-flink-runtime-deep-dive.md`

**问题 #15** (第 532 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp80tyhwj3TempValidation.java:8: 错误: 非法的表达式开始
public void notifyCreditAvailable() {
^
C:\Users\luyan\AppData\Local\Temp\tmp80tyhwj3TempValidation.java:30: 错误: 需要 cla
- **错误行**: 8

**问题 #17** (第 603 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv5r6clzvTempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env =
        ^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3


### `Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.03-flink-state-backends.md`

**问题 #9** (第 302 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmduokr5zTempValidation.java:4: 错误: 不是语句
state.backend.rocksdb.writebuffer.size: 64mb
                                 ^
C:\Users\luyan\AppData\Local\Temp\tmpmduokr
- **错误行**: 4

**问题 #10** (第 318 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6qwhjac_TempValidation.java:5: 错误: 不是语句
state.backend.rocksdb.memory.managed: true
                            ^
C:\Users\luyan\AppData\Local\Temp\tmp6qwhjac_TempV
- **错误行**: 5

**问题 #16** (第 479 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgd8pjv2dTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #18** (第 532 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbanvbr1tTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend = new EmbeddedRocksDBStateBackend(true);  // true=增量 Checkpoint
^
  符号:   类 Emb
- **错误行**: 4

**问题 #20** (第 584 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpghxd4chkTempValidation.java:4: 错误: 找不到符号
ForStStateBackendConfig forstConfig = ForStStateBackendConfig.builder()
^
  符号:   类 ForStStateBackendConfig
  位置: 类 TempVa
- **错误行**: 4


### `Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.04-flink-sql-table-api.md`

**问题 #6** (第 138 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3zmrqjjoTempValidation.java:4: 错误: 找不到符号
env.setRuntimeMode(RuntimeExecutionMode.STREAMING);
                   ^
  符号:   变量 RuntimeExecutionMode
  位置: 类 TempValid
- **错误行**: 4

**问题 #8** (第 282 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc6q8w85oTempValidation.java:7: 错误: 非法的类型开始
    .aggregate(new AggregateFunction<...>() { ... })
                                     ^
C:\Users\luyan\AppData\Local
- **错误行**: 7

**问题 #9** (第 302 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8xj55j9uTempValidation.java:4: 错误: 非法的表达式开始
Filter -> Scan  =>  Scan(with Filter)
                 ^
C:\Users\luyan\AppData\Local\Temp\tmp8xj55j9uTempValidation.ja
- **错误行**: 4

**问题 #10** (第 315 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaz9zum8tTempValidation.java:4: 错误: 需要';'
A JOIN B JOIN C  =>  选择代价最低的 Join 顺序
      ^
C:\Users\luyan\AppData\Local\Temp\tmpaz9zum8tTempValidation.java:4: 错误: 需要';'
- **错误行**: 4

**问题 #11** (第 342 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpskigjw_hMLPredictUDF.java:11: 错误: 需要 class、interface、enum 或 record
AsyncFunction 调用 REST API，延迟 10-100ms
^
C:\Users\luyan\AppData\Local\Temp\tmpskigjw_hMLPredictUD
- **错误行**: 11

**问题 #13** (第 423 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2h7itf4sTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.Table;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2h7itf4sTempValidation.
- **错误行**: 3

**问题 #15** (第 505 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqu_z1zr3TempValidation.java:4: 错误: 找不到符号
TableConfig config = tableEnv.getConfig();
^
  符号:   类 TableConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #17** (第 589 行, 语言: sql)

- **错误**: 可能的语法问题: -- 4. 模型性能监控
DESCRIBE MODEL METRICS FRAUD_DETECTIO...; 可能的语法问题: -- 显示: AVG_INFERENCE_LATENCY, THROUGHPUT, ERROR_RA...

**问题 #18** (第 665 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5ov3vbiiTempValidation.java:6: 错误: 找不到符号
DataStream<Event> stream = env.addSource(new KafkaSource<>());
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 6

**问题 #19** (第 703 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpynadssjsTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4


### `Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.05-flink-cloud-native.md`

**问题 #7** (第 290 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcgqvp3osTempValidation.java:4: 错误: 找不到符号
if (backpressureRatio > scaleUpThreshold ||
    ^
  符号:   变量 backpressureRatio
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4


### `Knowledge\Flink-Scala-Rust-Comprehensive\03-scala-rust-interop\03.01-wasm-interop.md`

**问题 #8** (第 302 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn2s7p395TempValidation.java:4: 错误: 非法的表达式开始
public record Input(long id, byte[] payload) {}
^
C:\Users\luyan\AppData\Local\Temp\tmpn2s7p395TempValidation.java:7: 错
- **错误行**: 4


### `Knowledge\Flink-Scala-Rust-Comprehensive\04-rust-engines\04.02-risingwave-deep-dive.md`

**问题 #9** (第 487 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpilh360t9TempValidation.java:4: 错误: 找不到符号
DataStream<Event> events = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpilh360t9
- **错误行**: 4


### `Knowledge\Flink-Scala-Rust-Comprehensive\04-rust-engines\04.03-materialize-analysis.md`

**问题 #7** (第 280 行, 语言: sql)

- **错误**: 可能的语法问题: -- 强一致性保证：余额始终准确，不会出现负余额（假设有约束）...

**问题 #11** (第 424 行, 语言: sql)

- **错误**: 可能的语法问题: -- 支持递归 CTE
WITH RECURSIVE CHAIN AS (
    SELECT *...

**问题 #12** (第 446 行, 语言: sql)

- **错误**: 可能的语法问题: -- 不支持递归 CTE，需外部处理...

**问题 #14** (第 510 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看物化视图状态
SHOW MATERIALIZED VIEWS;...; 可能的语法问题: -- 查看源表状态
SHOW SOURCES;...


### `Knowledge\Flink-Scala-Rust-Comprehensive\05-architecture-patterns\05.01-hybrid-architecture-patterns.md`

**问题 #5** (第 389 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 42, column 33:
                  output: STRUCT<ltv: DOUBLE, churn_risk: DOUBLE>
                                    ^ (line: 42)
- **错误行**: 42
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Knowledge\Flink-Scala-Rust-Comprehensive\src-analysis\flink-checkpoint-source.md`

**问题 #3** (第 91 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5zb9g31eTempValidation.java:3: 错误: 非法的表达式开始
public CompletableFuture<CompletedCheckpoint> triggerCheckpoint(
^
C:\Users\luyan\AppData\Local\Temp\tmp5zb9g31eTempVal
- **错误行**: 3

**问题 #4** (第 180 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8ztjxosjTempValidation.java:3: 错误: 非法的表达式开始
public boolean receiveAcknowledgeMessage(
^
C:\Users\luyan\AppData\Local\Temp\tmp8ztjxosjTempValidation.java:69: 错误: 需要
- **错误行**: 3

**问题 #5** (第 258 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgen1gf3wPendingCheckpoint.java:56: 错误: 非法的表达式开始
                        k -> new OperatorState(operatorId, ...));

- **错误行**: 56

**问题 #13** (第 794 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    execution.checkpointing.interval ...
    ^ (line: 4)
found duplicate key "execution.checkpointing.interval" with value "30s
- **错误行**: 4


### `Knowledge\Flink-Scala-Rust-Comprehensive\src-analysis\flink-network-stack.md`

**问题 #10** (第 805 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1507jg1cBlockingBackPressure.java:4: 错误: 非法的类型开始
    public void emitRecord(...) {
                           ^
C:\Users\luyan\AppData\Local\Temp\tmp1507jg1cBlocki
- **错误行**: 4


### `Knowledge\Flink-Scala-Rust-Comprehensive\src-analysis\flink-runtime-architecture.md`

**问题 #3** (第 74 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw8i8gbjdTempValidation.java:3: 错误: 非法的表达式开始
private void startJobExecution() {
^
C:\Users\luyan\AppData\Local\Temp\tmpw8i8gbjdTempValidation.java:27: 错误: 需要 class、
- **错误行**: 3

**问题 #4** (第 101 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj8t817sbTempValidation.java:4: 错误: 需要';'
public void notifyAllocationFailure(
                                   ^
C:\Users\luyan\AppData\Local\Temp\tmpj8t817sbTem
- **错误行**: 4

**问题 #7** (第 181 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg5fq18jvTempValidation.java:4: 错误: 需要';'
public CompletableFuture<Acknowledge> requestSlot(
                                                 ^
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #8** (第 218 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4i_utjp_TempValidation.java:3: 错误: 非法的表达式开始
protected abstract CompletableFuture<WorkerType> requestNewWorker(
^
C:\Users\luyan\AppData\Local\Temp\tmp4i_utjp_TempV
- **错误行**: 3

**问题 #11** (第 311 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv142ioh4TempValidation.java:4: 错误: 需要';'
public CompletableFuture<Acknowledge> submitJob(
                                               ^
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #12** (第 350 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphrjobvleTempValidation.java:3: 错误: 非法的表达式开始
private void onJobManagerRunnerComplete(
^
C:\Users\luyan\AppData\Local\Temp\tmphrjobvleTempValidation.java:33: 错误: 需要
- **错误行**: 3

**问题 #17** (第 528 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm12v3pj_TempValidation.java:3: 错误: 非法的表达式开始
public ExecutionGraph buildExecutionGraph(JobGraph jobGraph) {
^
C:\Users\luyan\AppData\Local\Temp\tmpm12v3pj_TempValid
- **错误行**: 3

**问题 #18** (第 632 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiat94_bqPipelinedRegionScheduler.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
public SchedulerNG createScheduler(
       ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 1

**问题 #19** (第 718 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjii501xlJobManager.java:8: 错误: 找不到符号
    SchedulerNG scheduler;  // 可插拔调度器
    ^
  符号:   类 SchedulerNG
  位置: 类 JobMaster
C:\Users\luyan\AppData\Local\Temp\tmpjii50
- **错误行**: 8

**问题 #21** (第 785 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps9pxndh8SlotPoolImpl.java:5: 错误: 找不到符号
    private void requestSlotsBatch(List<SlotRequest> requests) {
                                   ^
  符号:   类 List
  位置: 类
- **错误行**: 5


### `Knowledge\Flink-Scala-Rust-Comprehensive\src-analysis\flink-taskmanager-deep-dive.md`

**问题 #3** (第 97 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2oxncmzhTempValidation.java:4: 错误: 需要';'
public CompletableFuture<Acknowledge> submitTask(
                                                ^
C:\Users\luyan\AppData
- **错误行**: 4

**问题 #4** (第 177 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0wtow__7TempValidation.java:4: 错误: 需要';'
public CompletableFuture<Acknowledge> freeSlot(
                                              ^
C:\Users\luyan\AppData\Loc
- **错误行**: 4


### `Knowledge\cep-complete-tutorial.md`

**问题 #4** (第 229 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqvlc_759TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.Pattern;
^
C:\Users\luyan\AppData\Local\Temp\tmpqvlc_759TempValidation.java:3: 错误: 不是语句
imp
- **错误行**: 3

**问题 #5** (第 281 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoyik4dqiTempValidation.java:4: 错误: 找不到符号
Pattern<LoginEvent, ?> suspiciousLogin = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #6** (第 323 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdyw9_c50TempValidation.java:4: 错误: 找不到符号
Pattern<SensorReading, ?> overheatingPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4


### `Knowledge\kafka-streams-migration.md`

**问题 #6** (第 145 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2u11tjj4TempValidation.java:3: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3

**问题 #7** (第 158 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2ogvje7oTempValidation.java:4: 错误: 非法的表达式开始
DataStream<Order> orders = env.fromKafka("orders", ...);
                                                   ^
C:\Users\
- **错误行**: 4

**问题 #8** (第 182 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfslsr_b1TempValidation.java:3: 错误: 找不到符号
        KTable<Windowed<String>, Long> counts = orders
        ^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3


### `LEARNING-PATHS\beginner-quick-start.md`

**问题 #3** (第 125 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7vfh84u3TempValidation.java:4: 错误: 找不到符号
env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);
                                ^
  符号:   变量 TimeCharacteri
- **错误行**: 4

**问题 #5** (第 216 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkg4qb_2tTempValidation.java:7: 错误: 非法的表达式开始
private transient Counter eventCounter;
^
C:\Users\luyan\AppData\Local\Temp\tmpkg4qb_2tTempValidation.java:17: 错误: 需要 c
- **错误行**: 7

**问题 #6** (第 252 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpohunwgl7TempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4


### `LEARNING-PATHS\beginner-with-foundation.md`

**问题 #4** (第 197 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz1cr29_cTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpz1cr29_cTempV
- **错误行**: 4


### `LEARNING-PATHS\certifications\custom-assessment.md`

**问题 #5** (第 152 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0dk7s086OrderTimeoutDetection.java:132: 错误: 需要 class、interface、enum 或 record
*/
^
1 个错误

- **错误行**: 132

**问题 #6** (第 289 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps9p6zovzDynamicRiskControlEngine.java:222: 错误: 需要 class、interface、enum 或 record
*/
^
1 个错误

- **错误行**: 222


### `LEARNING-PATHS\certifications\ververica-certification.md`

**问题 #2** (第 69 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfgr0g515TempValidation.java:4: 错误: 找不到符号
DataStream<Integer> stream = env.fromElements(1, 2, 3, 4, 5);
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4

**问题 #4** (第 129 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5d74ttn3TempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp5d74ttn3TempV
- **错误行**: 4

**问题 #5** (第 146 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi30ffa6uTempValidation.java:20: 错误: 非法的表达式开始
    new MapStateDescriptor<>("rules", Types.STRING, Types.ROW(...));

- **错误行**: 20

**问题 #6** (第 170 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0yx4hhs0TempValidation.java:4: 错误: 找不到符号
WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                   ^
  符号:   类 Event
  位置: 类 Temp
- **错误行**: 4


### `LEARNING-PATHS\expert-performance-tuning.md`

**问题 #2** (第 79 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprck8r_vhTempValidation.java:6: 错误: 找不到符号
      .addSink(new SlowSink());  // 故意降低处理速度
                   ^
  符号:   类 SlowSink
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 6

**问题 #4** (第 142 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvwlvv0fxTempValidation.java:4: 错误: 找不到符号
   env.getConfig().setBufferTimeout(0);  // 零缓冲延迟
   ^
  符号:   变量 env
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #8** (第 251 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjs81akbjTempValidation.java:4: 错误: 找不到符号
env.getCheckpointConfig().enableUnalignedCheckpoints();
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #11** (第 294 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3ujmet0lTempValidation.java:4: 错误: 程序包ElasticsearchSink不存在
   ElasticsearchSink.Builder<LogEvent> builder =
                    ^
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4


### `LEARNING-PATHS\industry-ecommerce-recommendation.md`

**问题 #7** (第 306 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 2


### `LEARNING-PATHS\industry-finance-realtime.md`

**问题 #4** (第 222 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdy747mcdTempValidation.java:4: 错误: 找不到符号
   Pattern<Transaction, ?> fraudPattern = Pattern.<Transaction>begin("start")
   ^
  符号:   类 Pattern
  位置: 类 TempValidatio
- **错误行**: 4


### `LEARNING-PATHS\industry-iot-data-processing.md`

**问题 #3** (第 147 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp581j6m_TempValidation.java:7: 错误: 找不到符号
  .setDeserializer(new SensorDataDeserializer())
                       ^
  符号:   类 SensorDataDeserializer
  位置: 类 TempVal
- **错误行**: 7


### `LEARNING-PATHS\intermediate-datastream-expert.md`

**问题 #4** (第 226 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg11l57blTempValidation.java:4: 错误: 非法的表达式开始
public void processElement(List<Element> elements, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpg11l57blTempVa
- **错误行**: 4


### `LEARNING-PATHS\intermediate-sql-expert.md`

**问题 #9** (第 281 行, 语言: sql)

- **错误**: 可能的语法问题: -- 1. 使用 MINI-BATCH 优化聚合
SET TABLE.EXEC.MINI-BATCH...; 可能的语法问题: -- 2. 使用 LOCAL-GLOBAL 优化
SET TABLE.OPTIMIZER.AGG-P...


### `LEARNING-PATHS\intermediate-state-management-expert.md`

**问题 #2** (第 79 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcictbfezTempValidation.java:4: 错误: 找不到符号
   env.setStateBackend(new HashMapStateBackend());
                           ^
  符号:   类 HashMapStateBackend
  位置: 类 Temp
- **错误行**: 4

**问题 #5** (第 262 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdv4bvwszTempValidation.java:4: 错误: 需要';'
   stream.keyBy(event -> event.getUserId() % 1000)
                                                  ^
1 个错误

- **错误行**: 4

**问题 #6** (第 269 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu3audq7iTempValidation.java:4: 错误: 找不到符号
   DefaultConfigurableStateBackend stateBackend =
   ^
  符号:   类 DefaultConfigurableStateBackend
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #7** (第 280 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfrt0zce8TempValidation.java:4: 错误: 找不到符号
     new FileSystemCheckpointStorage("hdfs:///checkpoints")
         ^
  符号:   类 FileSystemCheckpointStorage
  位置: 类 TempV
- **错误行**: 4

**问题 #8** (第 311 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp79leth_wTempValidation.java:5: 错误: 找不到符号
ValueState<List<LargeObject>> largeListState;
^
  符号:   类 ValueState
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 5

**问题 #9** (第 325 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp30o03oxkTempValidation.java:4: 错误: 非法的表达式开始
public void processBatch(List<Event> events) {
^
C:\Users\luyan\AppData\Local\Temp\tmp30o03oxkTempValidation.java:5: 错误
- **错误行**: 4


### `POSITIONING.md`

**问题 #5** (第 215 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_2ddzpazTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp_2ddzpazTempV
- **错误行**: 4


### `POST-100-PERCENT-ROADMAP-v4.1.md`

**问题 #2** (第 94 行, 语言: python)

- **错误**: SyntaxError: invalid character '（' (U+FF08)
- **错误行**: 5


### `Struct\01-foundation\01.04-dataflow-model-formalization.md`

**问题 #1** (第 392 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvi620ri7TempValidation.java:3: 错误: 找不到符号
        DataStream<String> text = env.socketTextStream("localhost", 9999);
        ^
  符号:   类 DataStream
  位置: 类 TempVali
- **错误行**: 3


### `Struct\01-foundation\01.07-session-types.md`

**问题 #6** (第 357 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2


### `Struct\02-properties\02.01-determinism-in-streaming.md`

**问题 #3** (第 408 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplreniml5TempValidation.java:3: 错误: 找不到符号
        DataStream<Event> events = env.addSource(kafkaSource);
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Us
- **错误行**: 3

**问题 #4** (第 440 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5nlo1kl6TempValidation.java:4: 错误: 找不到符号
DataStream<Event> events = env.addSource(ctx -> {
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #5** (第 460 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvxjk5906TempValidation.java:6: 错误: 非法的表达式开始
        WatermarkStrategy.<Event>forBoundedOutOfOrderness(...)

- **错误行**: 6

**问题 #6** (第 475 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpav7gjkxlTempValidation.java:4: 错误: 找不到符号
DataStream<EnrichedEvent> enriched = events
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4


### `Struct\02-properties\02.02-consistency-hierarchy.md`

**问题 #1** (第 656 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpykxd67ozTempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<String> source = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\Use
- **错误行**: 4

**问题 #3** (第 726 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphkpik5t3HttpSink.java:1: 错误: 找不到符号
class HttpSink implements SinkFunction<Record> {
                          ^
  符号: 类 SinkFunction
C:\Users\luyan\AppData\Local\T
- **错误行**: 1

**问题 #4** (第 748 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvf0trge1EagerKafkaSource.java:1: 错误: 找不到符号
class EagerKafkaSource implements SourceFunction<Record> {
                                  ^
  符号: 类 SourceFunction
C:
- **错误行**: 1


### `Struct\02-properties\02.03-watermark-monotonicity.md`

**问题 #1** (第 315 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2ejv2a43TempValidation.java:4: 错误: 非法的表达式开始
public void onWatermark(Watermark wm, Context ctx, Collector<Out> out) {
^
C:\Users\luyan\AppData\Local\Temp\tmp2ejv2a4
- **错误行**: 4


### `Struct\03-relationships\03.02-flink-to-process-calculus.md`

**问题 #1** (第 418 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9ap1ww_6TempValidation.java:3: 错误: 找不到符号
        DataStream<String> text = env.socketTextStream("localhost", 9999);
        ^
  符号:   类 DataStream
  位置: 类 TempVali
- **错误行**: 3

**问题 #3** (第 488 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpek8qdxyoTempValidation.java:4: 错误: 找不到符号
countState.update(countState.value() + 1);
                  ^
  符号:   变量 countState
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4


### `Struct\03-relationships\03.05-cross-model-mappings.md`

**问题 #6** (第 557 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptcsqsiv6TempValidation.java:3: 错误: 找不到符号
        DataStream<Result> result = stream
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 3


### `Struct\04-proofs\04.02-flink-exactly-once-correctness.md`

**问题 #5** (第 732 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6dpzjvbqTempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<String> source = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\Use
- **错误行**: 4

**问题 #6** (第 770 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5ypcm36mTempValidation.java:4: 错误: 找不到符号
StreamingFileSink<Result> sink = StreamingFileSink
^
  符号:   类 StreamingFileSink
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4

**问题 #7** (第 793 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr82ipk9eCounterSink.java:2: 错误: 找不到符号
class CounterSink implements SinkFunction<Event> {
                             ^
  符号: 类 SinkFunction
C:\Users\luyan\AppData
- **错误行**: 2

**问题 #8** (第 819 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpol9fvbz9EagerKafkaSource.java:2: 错误: 找不到符号
class EagerKafkaSource implements SourceFunction<Record> {
                                  ^
  符号: 类 SourceFunction
C:
- **错误行**: 2


### `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md`

**问题 #2** (第 781 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_qvusea9TempValidation.java:4: 错误: 找不到符号
Watermark currentOutput = mergeAllInputWatermarks();
^
  符号:   类 Watermark
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #5** (第 1131 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm_e5lzltTempValidation.java:3: 错误: 非法的表达式开始
public void onWatermark(Watermark wm, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpm_e5lzltTempValidation.java
- **错误行**: 3

**问题 #6** (第 1209 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7hddx593TempValidation.java:3: 错误: 非法的表达式开始
public void onWatermark(Watermark wm, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmp7hddx593TempValidation.java
- **错误行**: 3


### `Struct\04-proofs\04.07-deadlock-freedom-choreographic.md`

**问题 #1** (第 246 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8v2f9uigBuyTicket.java:2: 错误: 需要'{'
class BuyTicket@Buyer,Seller {
               ^
C:\Users\luyan\AppData\Local\Temp\tmp8v2f9uigBuyTicket.java:2: 错误: 需要 class、int
- **错误行**: 2

**问题 #9** (第 932 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpshp3ln2eRequestResponse.java:1: 错误: 需要'{'
class RequestResponse@Client,Server {
                     ^
C:\Users\luyan\AppData\Local\Temp\tmpshp3ln2eRequestResponse
- **错误行**: 1

**问题 #10** (第 952 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplglkuy2_ClientRequestResponse.java:3: 错误: 找不到符号
        sendToServer(request);
        ^
  符号:   方法 sendToServer(String)
  位置: 类 ClientRequestResponse
C:\Users\luy
- **错误行**: 3

**问题 #11** (第 963 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw74q1782ServerRequestResponse.java:3: 错误: 找不到符号
        String request = receiveFromClient();
                         ^
  符号:   方法 receiveFromClient()
  位置: 类 Ser
- **错误行**: 3

**问题 #12** (第 987 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqo0wi_e2Auction.java:1: 错误: 需要'{'
class Auction@Buyer,Seller,Arbiter {
             ^
C:\Users\luyan\AppData\Local\Temp\tmpqo0wi_e2Auction.java:1: 错误: 需要 class、int
- **错误行**: 1


### `Struct\06-frontier\06.02-choreographic-streaming-programming.md`

**问题 #8** (第 541 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdh192q5uTempValidation.java:4: 错误: 找不到符号
DataStream<String> lines = env.socketTextStream("localhost", 9999);
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users
- **错误行**: 4

**问题 #14** (第 690 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2fwvqfu_JoinOp.java:11: 错误: 不是语句
            select {
            ^
C:\Users\luyan\AppData\Local\Temp\tmp2fwvqfu_JoinOp.java:11: 错误: 需要';'
            select {

- **错误行**: 11


### `Struct\Model-Selection-Decision-Tree.md`

**问题 #6** (第 388 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1pe76i2tTempValidation.java:4: 错误: 找不到符号
Pattern<UserEvent, ?> pattern = Pattern.<UserEvent>begin("start")
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 4


### `Struct\Unified-Model-Relationship-Graph.md`

**问题 #5** (第 245 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpic4vaqr9TempValidation.java:3: 错误: 找不到符号
        DataStream<Event> stream = env
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 3


### `TECH-RADAR\migration-recommendations.md`

**问题 #4** (第 121 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7yzpkqv5WordCountBolt.java:14: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Tuple2<String, Integer>> wordCounts =
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 14


### `TOOLCHAIN.md`

**问题 #17** (第 460 行, 语言: yaml)

- **错误**: could not determine a constructor for the tag 'tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format'
  in "<unicode string>", line 43, column 19:
              format: !!python/name:py
- **错误行**: 43


### `TROUBLESHOOTING.md`

**问题 #6** (第 189 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5yehp86lSyncFunction.java:19: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Result> result = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 19

**问题 #8** (第 262 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqi39ddotTempValidation.java:4: 错误: 找不到符号
env.setBufferTimeout(100); // 减少Buffer等待时间
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpqi
- **错误行**: 4

**问题 #10** (第 326 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4pzb_82zTempValidation.java:4: 错误: 找不到符号
DataStream<LocalAgg> localAgg = source
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #16** (第 556 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplcr_218jTempValidation.java:4: 错误: 找不到符号
WatermarkStrategy<Event> strategy = WatermarkStrategy
^
  符号:   类 WatermarkStrategy
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 4


### `archive\completion-reports\LINK-HEALTH-REPORT.md`

**问题 #1** (第 48 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc0urvl29TempValidation.java:4: 错误: 需要';'
state.get(Transaction("first"))
                               ^
1 个错误

- **错误行**: 4


### `archive\completion-reports\TECHNICAL-AUDIT-REPORT.md`

**问题 #1** (第 38 行, 语言: yaml)

- **错误**: while scanning a simple key
  in "<unicode string>", line 8, column 1:
    <artifactId>flink-ai-agent</arti ...
    ^ (line: 8)
could not find expected ':'
  in "<unicode string>", line 9, column 1:

- **错误行**: 8


### `archive\completion-reports\TROUBLESHOOTING-COMPLETE.md`

**问题 #9** (第 554 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprvjx03wmTempValidation.java:4: 错误: 找不到符号
env.getConfig().setBufferDebloatingEnabled(true);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #17** (第 764 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppm_1gw9aMonitoredFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
StateTtlConfig ttlConfig = StateTtlConfig
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Loca
- **错误行**: 2

**问题 #19** (第 827 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2ldnl6u3MyKryoConfig.java:13: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<MyEvent> stream = env
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Local\Temp\tmp2ld
- **错误行**: 13

**问题 #22** (第 903 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqpj2xkbsTempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4


### `archive\deprecated\00.md`

**问题 #4** (第 399 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_6xnrlmlTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend backend = new EmbeddedRocksDBStateBackend(true);
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置:
- **错误行**: 4

**问题 #6** (第 449 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0dr6k89kTempValidation.java:6: 错误: 找不到符号
      .aggregate(new CountAggregate());
                     ^
  符号:   类 CountAggregate
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 6


### `archive\deprecated\LEARNING-PATHS-DYNAMIC.md`

**问题 #3** (第 146 行, 语言: python)

- **错误**: SyntaxError: illegal target for annotation
- **错误行**: 2

**问题 #5** (第 199 行, 语言: python)

- **错误**: SyntaxError: invalid character '×' (U+00D7)
- **错误行**: 1


### `docs\certification\csa\labs\lab-01-time-semantics.md`

**问题 #3** (第 76 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_37z8qroTempValidation.java:4: 错误: 找不到符号
    .map(new MapFunction<String, Tuple2<String, Integer>>() {
             ^
  符号:   类 MapFunction
  位置: 类 TempValidation

- **错误行**: 4

**问题 #7** (第 154 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd2txh60eTempValidation.java:9: 错误: 找不到符号
        new BoundedOutOfOrdernessTimestampExtractor<
            ^
  符号:   类 BoundedOutOfOrdernessTimestampExtractor
  位置:
- **错误行**: 9


### `docs\certification\csa\resources\capstone-project-csa.md`

**问题 #4** (第 153 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp45z3hpvTempValidation.java:3: 错误: 找不到符号
        DataStream<OrderEvent> orderStream = env
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppD
- **错误行**: 3

**问题 #5** (第 182 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzrpak76zTempValidation.java:6: 错误: 找不到符号
    .aggregate(new GmvAggregateFunction())
                   ^
  符号:   类 GmvAggregateFunction
  位置: 类 TempValidation
C:\U
- **错误行**: 6

**问题 #6** (第 213 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxedw1ph8TempValidation.java:9: 错误: 找不到符号
    .addSink(categorySink);
             ^
  符号:   变量 categorySink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 9

**问题 #8** (第 265 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvaa4z3oyTempValidation.java:7: 错误: 找不到符号
    .addSink(redisSink);
             ^
  符号:   变量 redisSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpv
- **错误行**: 7

**问题 #9** (第 294 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmf2ietofTempValidation.java:3: 错误: 找不到符号
        env.enableCheckpointing(30000);
        ^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 3


### `docs\chatbot-integration.md`

**问题 #5** (第 160 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 24

**问题 #17** (第 679 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoqc_dnkhTempValidation.java:3: 错误: 非法的表达式开始
        > env.enableCheckpointing(60000);  // 60 second interval
        ^
C:\Users\luyan\AppData\Local\Temp\tmpoqc_dnk
- **错误行**: 3


### `docs\contributing\writing-guide.md`

**问题 #9** (第 250 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbkrtfssdTempValidation.java:3: 错误: 找不到符号
        WatermarkStrategy<Event> strategy = WatermarkStrategy
        ^
  符号:   类 WatermarkStrategy
  位置: 类 TempValidation
- **错误行**: 3

**问题 #18** (第 394 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphc57ghsaTempValidation.java:4: 错误: 找不到符号
DataStream<Event> stream = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmphc57ghsa
- **错误行**: 4

**问题 #22** (第 445 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_oq367naTempValidation.java:4: 错误: 找不到符号
DataStream<String> result = stream.map(x -> x.toString());
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4


### `i18n\en\Flink\3.9-state-backends-deep-comparison.md`

**问题 #13** (第 378 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend.rocksdb.memory.man ...
    ^ (line: 2)
found duplicate key "state.backend.rocksdb.memory.managed" with value
- **错误行**: 2

**问题 #14** (第 399 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend.rocksdb.compaction ...
    ^ (line: 2)
found duplicate key "state.backend.rocksdb.compaction.style" with valu
- **错误行**: 2


### `i18n\en\Flink\data-types-complete-reference.md`

**问题 #4** (第 140 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplhyifmzcTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.DataTypes;
        ^
C:\Users\luyan\AppData\Local\Temp\tmplhyifmzcTempValidat
- **错误行**: 3


### `i18n\en\Flink\elasticsearch-connector-guide.md`

**问题 #2** (第 112 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1x9ciigxTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.elasticsearch.sink.Elasticsearch7SinkBuilder;
^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #4** (第 189 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn7qpkvk5TempValidation.java:4: 错误: 找不到符号
ElasticsearchSink<Event> esSink = new Elasticsearch7SinkBuilder<Event>()
^
  符号:   类 ElasticsearchSink
  位置: 类 TempValidat
- **错误行**: 4


### `i18n\en\Flink\flink-state-backends-comparison.md`

**问题 #3** (第 227 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpij21g1ofTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #4** (第 254 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkcupqxgyTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #5** (第 303 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2wa5rp6oTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #9** (第 459 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoomtz6uyTempValidation.java:4: 错误: 找不到符号
config.set(RocksDBOptions.BLOCK_CACHE_SIZE, MemorySize.ofMebiBytes(256));
           ^
  符号:   变量 RocksDBOptions
  位置: 类 T
- **错误行**: 4

**问题 #11** (第 476 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1ogexk2iTempValidation.java:3: 错误: 找不到符号
        config.set(CheckpointingOptions.INCREMENTAL_CHECKPOINTS, true);
                   ^
  符号:   变量 CheckpointingOptio
- **错误行**: 3

**问题 #13** (第 486 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplzyzyz38TempValidation.java:3: 错误: 找不到符号
        config.set(CheckpointingOptions.MAX_CONCURRENT_CHECKPOINTS, 1);
                   ^
  符号:   变量 CheckpointingOptio
- **错误行**: 3

**问题 #15** (第 499 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5hc8kp_nTempValidation.java:4: 错误: 找不到符号
config.set(CheckpointingOptions.LOCAL_RECOVERY, true);
           ^
  符号:   变量 CheckpointingOptions
  位置: 类 TempValidation
- **错误行**: 4


### `i18n\en\Flink\jdbc-connector-guide.md`

**问题 #2** (第 111 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpspl8_4bnTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcConnectionOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmpspl8_4bnTempValida
- **错误行**: 3

**问题 #4** (第 177 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6_lervtzTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcInputFormat;
^
C:\Users\luyan\AppData\Local\Temp\tmp6_lervtzTempValidation.j
- **错误行**: 3


### `i18n\en\Flink\mongodb-connector-guide.md`

**问题 #2** (第 96 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpca816f13TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.source.MongoSource;
^
C:\Users\luyan\AppData\Local\Temp\tmpca816f13TempValida
- **错误行**: 3

**问题 #3** (第 132 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnsnvj3zjTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.source.MongoSource;
^
C:\Users\luyan\AppData\Local\Temp\tmpnsnvj3zjTempValida
- **错误行**: 3

**问题 #4** (第 165 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxdklkx9yTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.sink.MongoSink;
^
C:\Users\luyan\AppData\Local\Temp\tmpxdklkx9yTempValidation
- **错误行**: 3


### `i18n\en\Flink\pulsar-functions-integration.md`

**问题 #4** (第 112 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoxmv33ypTempValidation.java:25: 错误: 非法的表达式开始
stats.addSink(new JdbcSink(...));
                           ^
1 个错误

- **错误行**: 25


### `i18n\en\Flink\pyflink-deep-guide.md`

**问题 #7** (第 265 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2


### `i18n\en\Flink\risingwave-integration-guide.md`

**问题 #3** (第 61 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmoov14oaTempValidation.java:4: 错误: 找不到符号
FlinkKafkaProducer<String> kafkaProducer = new FlinkKafkaProducer<>(
^
  符号:   类 FlinkKafkaProducer
  位置: 类 TempValidation
- **错误行**: 4

**问题 #6** (第 117 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3wsrtaznTempValidation.java:4: 错误: 找不到符号
DebeziumSourceFunction<String> source = DebeziumSourceFunction.<String>builder()
^
  符号:   类 DebeziumSourceFunction
  位置:
- **错误行**: 4

**问题 #7** (第 128 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpidposc0jTempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.sqlQuery(
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpidposc0jTe
- **错误行**: 4


### `i18n\en\Flink\state-backends-comparison.md`

**问题 #2** (第 103 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf_zu5_mqTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.runtime.state.hashmap.HashMapStateBackend;
^
C:\Users\luyan\AppData\Local\Temp\tmpf_zu5_mqTempV
- **错误行**: 3

**问题 #3** (第 136 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    state.backend: hashmap
    ^ (line: 4)
found duplicate key "state.backend" with value "rocksdb" (original value: "hashmap")

- **错误行**: 4

**问题 #4** (第 162 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq2m85yolTempValidation.java:4: 错误: 非法的表达式开始
public void monitorStateBackend(RuntimeContext ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpq2m85yolTempValidation.jav
- **错误行**: 4


### `i18n\en\Knowledge\cep-complete-tutorial.md`

**问题 #2** (第 99 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpumv0dsysTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.Pattern;
^
C:\Users\luyan\AppData\Local\Temp\tmpumv0dsysTempValidation.java:3: 错误: 不是语句
imp
- **错误行**: 3

**问题 #3** (第 151 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp64ux84iTempValidation.java:4: 错误: 找不到符号
Pattern<LoginEvent, ?> suspiciousLogin = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #4** (第 193 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp1e7sskoTempValidation.java:4: 错误: 找不到符号
Pattern<SensorReading, ?> overheatingPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4


### `i18n\en\Knowledge\kafka-streams-migration.md`

**问题 #3** (第 66 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9pw60ni0TempValidation.java:3: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3

**问题 #4** (第 79 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfl3ndbkfTempValidation.java:4: 错误: 非法的表达式开始
DataStream<Order> orders = env.fromKafka("orders", ...);
                                                   ^
C:\Users\
- **错误行**: 4

**问题 #5** (第 103 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw3aatyuxTempValidation.java:3: 错误: 找不到符号
        KTable<Windowed<String>, Long> counts = orders
        ^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3


### `reports\FICTIONAL-CONTENT-SUMMARY.md`

**问题 #1** (第 75 行, 语言: sql)

- **错误**: 可能的语法问题: ML_PREDICT(MODEL_ID, FEATURES);              -- SQ...; 可能的语法问题: VECTOR_SEARCH(VECTOR_COLUMN, QUERY_VECTOR);  -- SQ...


### `reports\fictional-content-audit-20260405_143730.md`

**问题 #30** (第 510 行, 语言: sql)

- **错误**: 可能的语法问题: 55: -- 形式 1: 基本调用

>>> 56: SELECT * FROM ML_PREDICT...

**问题 #53** (第 860 行, 语言: sql)

- **错误**: 可能的语法问题: 367: -- DEF-F-12-110A: CREATE AGENT语法（未来可能的语法，概念设计...

**问题 #168** (第 2678 行, 语言: yaml)

- **错误**: while scanning a block scalar
  in "<unicode string>", line 2, column 1:
    >>> 40: ai.agent.enabled: true   ...
    ^ (line: 2)
expected chomping or indentation indicators, but found '>'
  in "<uni
- **错误行**: 2

**问题 #174** (第 2770 行, 语言: yaml)

- **错误**: while scanning a block scalar
  in "<unicode string>", line 1, column 1:
    >>> 818: # flink-gpu-deployment.yaml
    ^ (line: 1)
expected chomping or indentation indicators, but found '>'
  in "<unic
- **错误行**: 1

**问题 #451** (第 7164 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 1, column 14:
    74: Flink 2.4:
                 ^ (line: 1)
- **错误行**: 1
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #583** (第 9233 行, 语言: sql)

- **错误**: 可能的语法问题: 1333: -- =========================================...


### `tutorials\01-environment-setup.md`

**问题 #5** (第 138 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 15, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^ (line: 15)
- **错误行**: 15
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #18** (第 658 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj3zgosumTempValidation.java:4: 错误: 非法的表达式开始
public class $NAME$ {
^
C:\Users\luyan\AppData\Local\Temp\tmpj3zgosumTempValidation.java:10: 错误: 需要';'
        env.exec
- **错误行**: 4


### `tutorials\02-first-flink-job.md`

**问题 #1** (第 66 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpanfw27qyTempValidation.java:5: 错误: 找不到符号
    .flatMap(tokenizer)  // 链内
             ^
  符号:   变量 tokenizer
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 5

**问题 #15** (第 791 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk6mus8wrTempValidation.java:4: 错误: 找不到符号
Set<String> stopWords = new HashSet<>(Arrays.asList("the", "a", "is", "of"));
^
  符号:   类 Set
  位置: 类 TempValidation
C:\Us
- **错误行**: 4

**问题 #17** (第 854 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx4mlneoiTempValidation.java:5: 错误: 找不到符号
    .flatMap(new Tokenizer())
                 ^
  符号:   类 Tokenizer
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 5


### `tutorials\02-streaming-fundamentals-script.md`

**问题 #3** (第 75 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7ncnh_foTempValidation.java:4: 错误: 找不到符号
Dataset<Row> batch = spark.read().parquet("/data/logs");
^
  符号:   类 Dataset
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4

**问题 #6** (第 158 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp27134r4_TempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #9** (第 251 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl53c5bsvTempValidation.java:6: 错误: 找不到符号
WatermarkStrategy.<MyEvent>forMonotonousTimestamps()
                   ^
  符号:   类 MyEvent
  位置: 类 TempValidation
C:\User
- **错误行**: 6

**问题 #12** (第 374 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzo99ri64TempValidation.java:9: 错误: 找不到符号
    .aggregate(new CountAggregate());
                   ^
  符号:   类 CountAggregate
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 9


### `tutorials\04-design-patterns-script.md`

**问题 #10** (第 525 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgem_bs_9AsyncIOPattern.java:14: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 14

**问题 #12** (第 679 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplgqi51e1StateManagementPattern.java:17: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 17

**问题 #16** (第 980 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4senuhxxCheckpointPattern.java:76: 错误: 非法的表达式开始
            .addSource(new FlinkKafkaConsumer<>(...))
                                                ^
1 个错误

- **错误行**: 76


### `tutorials\05-production-deployment-script.md`

**问题 #4** (第 144 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 7, column 1:
    kubectl wait --for=condition=rea ...
    ^ (line: 7)
- **错误行**: 7


### `tutorials\06-advanced-topics-script.md`

**问题 #7** (第 308 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv6y2rib0StateTTLConfiguration.java:42: 错误: 非法的表达式开始
        DataStream<Event> stream = env.addSource(...);
                                                 ^
1 个错误
- **错误行**: 42

**问题 #13** (第 835 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2pw9ej8eSkewHandling.java:9: 错误: 非法的表达式开始
        DataStream<Event> source = env.addSource(...);
                                                 ^
1 个错误

- **错误行**: 9

**问题 #17** (第 1199 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5nnl9luyLargeStateOptimization.java:25: 错误: 非法的表达式开始
        DataStream<Event> source = env.addSource(...);
                                                 ^
1 个错
- **错误行**: 25


### `tutorials\interactive\coding-challenges\challenge-01-hot-items.md`

**问题 #5** (第 92 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb6ruwwl5UserBehaviorSource.java:5: 错误: 非法的表达式开始
    private String[] users = {"user_001", "user_002", "user_003", ...};

- **错误行**: 5

**问题 #9** (第 285 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb6vrfofbTempValidation.java:4: 错误: 需要';'
public void testHotItems() throws Exception {
                        ^
C:\Users\luyan\AppData\Local\Temp\tmpb6vrfofbTempV
- **错误行**: 4

**问题 #11** (第 335 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2vtocjxgTempValidation.java:6: 错误: 非法的表达式开始
    .window(...)
            ^
C:\Users\luyan\AppData\Local\Temp\tmp2vtocjxgTempValidation.java:7: 错误: 非法的表达式开始
    .ag
- **错误行**: 6

**问题 #12** (第 347 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnk9nhno1TempValidation.java:4: 错误: 找不到符号
windowedCounts.addSink(new RedisSink<>(
^
  符号:   变量 windowedCounts
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `tutorials\interactive\coding-challenges\challenge-03-order-timeout.md`

**问题 #6** (第 352 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpplqzhve6TempValidation.java:4: 错误: 需要';'
public void testOrderTimeout() throws Exception {
                            ^
C:\Users\luyan\AppData\Local\Temp\tmpplqzh
- **错误行**: 4

**问题 #7** (第 416 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7mf165lgMultiLevelTimeout.java:3: 错误: 非法的类型开始
public class MultiLevelTimeout extends KeyedProcessFunction<...> {

- **错误行**: 3

**问题 #8** (第 459 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk0t3xajiOrderWithInventory.java:2: 错误: 非法的类型开始
public class OrderWithInventory extends KeyedProcessFunction<...> {

- **错误行**: 2


### `tutorials\interactive\coding-challenges\challenge-04-recommendation.md`

**问题 #4** (第 198 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkj_kpc8qCollaborativeFiltering.java:22: 错误: 非法的表达式开始
                ctx.getBroadcastState(...).immutableEntries()) {
                                      ^
C:\Us
- **错误行**: 22

**问题 #6** (第 364 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2pwnwj5jRealtimeRecommendationJob.java:11: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 11

**问题 #8** (第 456 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmputda3w_6ABTestSplit.java:4: 错误: 非法的类型开始
    public void processElement(UserProfile profile, Context ctx, ...) {

- **错误行**: 4


### `tutorials\interactive\coding-challenges\challenge-05-data-pipeline.md`

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1ojwx3y4CDCSourceConfig.java:18: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<String> cdcStream = env
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 18


### `tutorials\interactive\hands-on-labs\lab-01-first-flink-program.md`

**问题 #12** (第 267 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpja1hxiq3TempValidation.java:3: 错误: 找不到符号
if (word.length() >= 3) {
    ^
  符号:   变量 word
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpja1hxiq3TempVa
- **错误行**: 3


### `tutorials\interactive\hands-on-labs\lab-02-event-time.md`

**问题 #4** (第 132 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpke_kczmiTempValidation.java:4: 错误: 非法的表达式开始
private static final OutputTag<SensorReading> lateDataTag =
^
C:\Users\luyan\AppData\Local\Temp\tmpke_kczmiTempValidati
- **错误行**: 4


### `tutorials\interactive\hands-on-labs\lab-03-window-aggregation.md`

**问题 #3** (第 146 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp49iqhxjhSlidingWindowExample.java:14: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 14

**问题 #4** (第 198 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo9oag32nSessionWindowExample.java:17: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 17

**问题 #6** (第 369 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptfku65wbEnrichmentFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<WindowStats> results = stream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #7** (第 407 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4e2ltq8wCountTrigger.java:55: 错误: 需要 class、interface、enum 或 record
stream.keyBy(...)
^
1 个错误

- **错误行**: 55

**问题 #8** (第 480 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyqzbrwj3WindowBenchmark.java:6: 错误: 非法的表达式开始
        stream.window(...)
                      ^
C:\Users\luyan\AppData\Local\Temp\tmpyqzbrwj3WindowBenchmark.java:1
- **错误行**: 6

**问题 #10** (第 542 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpze0e31zeTempValidation.java:4: 错误: 非法的表达式开始
DataStream<WindowResult> mainResults = ...;
                                       ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4


### `tutorials\interactive\hands-on-labs\lab-04-state-management.md`

**问题 #5** (第 271 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptsqbynfmStatefulFunctionWithTTL.java:4: 错误: 非法的类型开始
public class StatefulFunctionWithTTL extends KeyedProcessFunction<...> {

- **错误行**: 4

**问题 #7** (第 366 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppt0rd4jzTempValidation.java:4: 错误: 需要';'
public void testTemperatureAlert() throws Exception {
                                ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #9** (第 428 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpasdpgl2sTempValidation.java:4: 错误: 找不到符号
ValueStateDescriptor<Long> descriptor =
^
  符号:   类 ValueStateDescriptor
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4


### `tutorials\interactive\hands-on-labs\lab-05-checkpoint.md`

**问题 #4** (第 126 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt99m2229TempValidation.java:4: 错误: 找不到符号
env.setStateBackend(new RocksDBStateBackend(
                        ^
  符号:   类 RocksDBStateBackend
  位置: 类 TempValidatio
- **错误行**: 4

**问题 #8** (第 231 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptkebdvxcTempValidation.java:4: 错误: 需要';'
public void testCheckpointAndRestore() throws Exception {
                                    ^
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #10** (第 293 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmbpcm72xTempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<String> kafkaSource = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C
- **错误行**: 4

**问题 #11** (第 329 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv_acso45TempValidation.java:4: 错误: 找不到符号
env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4


### `tutorials\interactive\hands-on-labs\lab-06-cep.md`

**问题 #2** (第 36 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppx17ok91BasicCEPExample.java:18: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 18

**问题 #3** (第 118 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyntxl133TempValidation.java:4: 错误: 找不到符号
Pattern<LoginEvent, ?> loginFailPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #4** (第 157 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpehju69v_TempValidation.java:4: 错误: 找不到符号
Pattern<Event, ?> strictPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #5** (第 186 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsw9c9cegTempValidation.java:4: 错误: 找不到符号
Pattern<StockPrice, ?> risingPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #6** (第 228 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3quxicljTempValidation.java:4: 错误: 找不到符号
OutputTag<TimeoutEvent> timeoutTag = new OutputTag<TimeoutEvent>("timeout"){};
^
  符号:   类 OutputTag
  位置: 类 TempValidatio
- **错误行**: 4

**问题 #7** (第 269 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxtpuumthFraudDetectionCEP.java:9: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 9

**问题 #8** (第 340 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6kvsti4xTempValidation.java:4: 错误: 需要';'
public void testLoginFailurePattern() throws Exception {
                                   ^
C:\Users\luyan\AppData\Local
- **错误行**: 4

**问题 #9** (第 370 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz702j72hTempValidation.java:4: 错误: 找不到符号
Pattern<UserAction, ?> cartAbandonmentPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 4

**问题 #10** (第 393 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb7uukuqmTempValidation.java:4: 错误: 找不到符号
Pattern<SensorReading, ?> failurePattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 4


### `tutorials\interactive\quizzes\comprehensive-test.md`

**问题 #1** (第 439 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppjw_xwg9TempValidation.java:3: 错误: 找不到符号
Pattern<LoginEvent, ?> pattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpp
- **错误行**: 3


### `v5.0\RELEASE-NOTES-v5.0.md`

**问题 #2** (第 162 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 10


### `visuals\layer-decidability.md`

**问题 #1** (第 120 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu5wzi0qgTempValidation.java:6: 错误: 找不到符号
      .aggregate(new CountAggregate());
                     ^
  符号:   类 CountAggregate
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 6


### `visuals\selection-tree-consistency.md`

**问题 #3** (第 181 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsiml9z2wTempValidation.java:4: 错误: 找不到符号
env.disableCheckpointing();  // 禁用 Checkpoint
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tm
- **错误行**: 4

**问题 #5** (第 227 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp22lzkwndTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp22lzkwndTempV
- **错误行**: 4

**问题 #7** (第 285 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqrmfar77TempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpqrmfar77TempV
- **错误行**: 4

**问题 #12** (第 435 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphm0ypme5TempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env =
        ^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3

**问题 #13** (第 452 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz5q2xpb1TempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env =
        ^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3

**问题 #14** (第 473 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd550vevzTempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env =
        ^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3


### `whitepaper-streaming-2027.md`

**问题 #7** (第 439 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgjw4m330TempValidation.java:4: 错误: 找不到符号
DataStream<FeatureVector> realTimeFeatures = events
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #19** (第 959 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkb9jcqlfTempValidation.java:5: 错误: 找不到符号
Pattern<EnrichedTransaction, ?> geoPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 5

**问题 #21** (第 1066 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfvz8t07eSessionFeatureAggregate.java:2: 错误: 找不到符号
class SessionFeatureAggregate implements AggregateFunction<UserEvent, SessionAccumulator, SessionFeature> {

- **错误行**: 2


### `whitepapers\flink-enterprise-implementation-guide.md`

**问题 #3** (第 162 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp87r8q5qkTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000); // 1分钟间隔
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp87r8
- **错误行**: 4


### `whitepapers\realtime-ai-architecture-practice.md`

**问题 #10** (第 369 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpleijd77wTensorFlowInference.java:33: 错误: 未命名类 是预览功能，默认情况下禁用。
Table result = tableEnv.sqlQuery(
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 33


## 🔧 修复建议

### 常见问题及修复方法

#### Python

1. **缩进错误 (IndentationError)**
   - 使用统一的4空格缩进
   - 不要混用Tab和空格
   - 运行 `.scripts/code-example-fixer.py` 自动修复

2. **语法错误 (SyntaxError)**
   - 检查括号、引号是否成对
   - 检查冒号是否正确使用
   - 确保代码片段完整性

#### Java

1. **缺少分号**
   - 每个语句结尾添加分号
   - 检查导入语句完整性

2. **括号不匹配**
   - 检查大括号 `{}`、小括号 `()`、方括号 `[]` 是否成对

#### YAML

1. **缩进问题**
   - 使用2空格缩进
   - 冒号后必须有空格

2. **特殊字符**
   - 字符串包含特殊字符时使用引号包裹

#### SQL

1. **关键字错误**
   - 检查SQL关键字拼写
   - 确保表名、列名正确

## 📁 输出文件

验证结果已保存为JSON格式，可用于进一步处理：

- `validation-results.json` - 完整验证结果
- `invalid-blocks.json` - 仅包含无效代码块

## 🚀 下一步操作

运行自动修复工具：

```bash
python .scripts/code-example-fixer.py
```

这将自动修复以下问题：

- 缩进不一致
- 尾部空格
- 简单的括号匹配问题
- 代码格式化

---
_报告由代码示例验证器自动生成_
