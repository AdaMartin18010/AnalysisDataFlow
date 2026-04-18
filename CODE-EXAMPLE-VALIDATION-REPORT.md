# 代码示例验证报告

> **生成时间**: 2026-04-18 18:49:33
> **验证器版本**: 1.0.0
> **项目根目录**: .

## 📊 验证统计

| 指标 | 数值 |
|------|------|
| 扫描文件数 | 4032 |
| 代码块总数 | 14539 |
| ✅ 验证通过 | 10754 |
| ❌ 验证失败 | 3785 |
| ⚠️  警告数 | 0 |
| 🔧 可自动修复 | 50 |
| **通过率** | 73.97% |

### 按语言统计

| 语言 | 总数 | 有效 | 无效 | 通过率 |
|------|------|------|------|--------|
| bash | 2091 | 2091 | 0 | 100.00% |
| java | 5343 | 2244 | 3099 | 42.00% |
| json | 360 | 360 | 0 | 100.00% |
| python | 1483 | 1381 | 102 | 93.12% |
| shell | 1 | 1 | 0 | 100.00% |
| sql | 2522 | 2119 | 403 | 84.02% |
| xml | 180 | 180 | 0 | 100.00% |
| yaml | 2559 | 2378 | 181 | 92.93% |

## 🚨 问题代码清单

共发现 **3785** 个有问题的代码示例：


### `AI-STREAMING-RESEARCH-REPORT-2024-2025.md`

**问题 #14** (第 591 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfwnarr9uTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpfwnarr9uTemp
- **错误行**: 3


### `BEST-PRACTICES-COMPLETE.md`

**问题 #2** (第 29 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd3mi_zr6TempValidation.java:7: 错误: 非法的表达式开始
stream.map(...).startNewChain().filter(...);
           ^
C:\Users\luyan\AppData\Local\Temp\tmpd3mi_zr6TempValidation.j
- **错误行**: 7

**问题 #3** (第 45 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzyu7agvzTempValidation.java:4: 错误: 找不到符号
env.getConfig().setAutoWatermarkInterval(200);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4


### `CASE-STUDIES.md`

**问题 #3** (第 267 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0xkwxsvpTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp0xkwxsvpTempValidat
- **错误行**: 4

**问题 #7** (第 496 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdqxsr5b7TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.typeinfo.Types;
^
C:\Users\luyan\AppData\Local\Temp\tmpdqxsr5b7TempValidation.java:4
- **错误行**: 4

**问题 #9** (第 614 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplcklsebdTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmplck
- **错误行**: 3

**问题 #12** (第 735 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2osdzvy8TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp2osdzvy8TempValidat
- **错误行**: 4

**问题 #13** (第 809 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2eqq2j1_TempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #14** (第 819 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcwe8qb6kTempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend rocksDb = new RocksDBStateBackend("hdfs://checkpoints");
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempV
- **错误行**: 4

**问题 #16** (第 904 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptn_0d2c4ThresholdMonitorFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<SensorData> processed = env
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\
- **错误行**: 2

**问题 #22** (第 1155 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi__njgelAntiCheatProcessFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<PlayerAction> actionStream = env
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\App
- **错误行**: 2

**问题 #28** (第 1446 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcxu2pp1rTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpcxu
- **错误行**: 3


### `CI-CD-OPTIMIZATION-REPORT.md`

**问题 #4** (第 233 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    jobs:
    ^ (line: 2)
found duplicate key "jobs" with value "{}" (original value: "{}")
  in "<unicode string>", line 10, co
- **错误行**: 2


### `CODE-QUALITY-FINAL-REPORT.md`

**问题 #5** (第 291 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 1

**问题 #7** (第 311 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 1


### `CODE-VALIDATION-JAVA-REPORT.md`

**问题 #1** (第 197 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2m9gpkhdTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2m9gpkhdTemp
- **错误行**: 3

**问题 #2** (第 208 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmb0bm0ncTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.Table; // 用于 Table
        ^
C:\Users\luyan\AppData\Local\Temp\tmpmb0bm0ncTem
- **错误行**: 3


### `CODE-VALIDATION-PYTHON-REPORT.md`

**问题 #1** (第 32 行, 语言: python)

- **错误**: SyntaxError: '(' was never closed
- **错误行**: 14

**问题 #2** (第 62 行, 语言: python)

- **错误**: SyntaxError: invalid character '，' (U+FF0C)
- **错误行**: 4

**问题 #3** (第 82 行, 语言: python)

- **错误**: SyntaxError: unterminated triple-quoted string literal (detected at line 13)
- **错误行**: 10

**问题 #4** (第 107 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 13

**问题 #5** (第 136 行, 语言: python)

- **错误**: SyntaxError: 'await' outside async function
- **错误行**: 4

**问题 #6** (第 153 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 6

**问题 #7** (第 173 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 17

**问题 #8** (第 206 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 3

**问题 #9** (第 243 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 6

**问题 #10** (第 261 行, 语言: python)

- **错误**: SyntaxError: expected '('
- **错误行**: 10

**问题 #11** (第 287 行, 语言: python)

- **错误**: SyntaxError: '(' was never closed
- **错误行**: 11

**问题 #13** (第 341 行, 语言: python)

- **错误**: SyntaxError: '(' was never closed
- **错误行**: 14

**问题 #14** (第 367 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 2

**问题 #15** (第 396 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2

**问题 #16** (第 428 行, 语言: python)

- **错误**: SyntaxError: invalid character '✅' (U+2705)
- **错误行**: 4

**问题 #17** (第 457 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 2

**问题 #18** (第 478 行, 语言: python)

- **错误**: SyntaxError: 'async for' outside async function
- **错误行**: 8

**问题 #19** (第 506 行, 语言: python)

- **错误**: SyntaxError: '(' was never closed
- **错误行**: 11

**问题 #20** (第 534 行, 语言: python)

- **错误**: SyntaxError: invalid decimal literal
- **错误行**: 2

**问题 #21** (第 552 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 9

**问题 #24** (第 620 行, 语言: python)

- **错误**: SyntaxError: invalid decimal literal
- **错误行**: 2

**问题 #25** (第 637 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 7

**问题 #27** (第 685 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 5

**问题 #28** (第 710 行, 语言: python)

- **错误**: SyntaxError: unterminated triple-quoted string literal (detected at line 13)
- **错误行**: 9

**问题 #30** (第 761 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2

**问题 #31** (第 787 行, 语言: python)

- **错误**: SyntaxError: '[' was never closed
- **错误行**: 12

**问题 #32** (第 815 行, 语言: python)

- **错误**: SyntaxError: invalid character '⊥' (U+22A5)
- **错误行**: 3

**问题 #33** (第 844 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 17

**问题 #34** (第 876 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 13

**问题 #35** (第 907 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 19

**问题 #36** (第 942 行, 语言: python)

- **错误**: SyntaxError: invalid decimal literal
- **错误行**: 4

**问题 #37** (第 972 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 13

**问题 #38** (第 1000 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 2

**问题 #39** (第 1018 行, 语言: python)

- **错误**: SyntaxError: expected 'else' after 'if' expression
- **错误行**: 2

**问题 #40** (第 1040 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 5

**问题 #42** (第 1098 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2

**问题 #43** (第 1119 行, 语言: python)

- **错误**: SyntaxError: invalid character '⊕' (U+2295)
- **错误行**: 3

**问题 #44** (第 1136 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 1

**问题 #45** (第 1158 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 3

**问题 #46** (第 1178 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2

**问题 #47** (第 1198 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2

**问题 #48** (第 1224 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2


### `CONFIG-TEMPLATES\development\ide-config-guide.md`

**问题 #3** (第 81 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzblvxr07TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpzb
- **错误行**: 4


### `CONFIG-TEMPLATES\scenarios\scenario-comparison.md`

**问题 #8** (第 197 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg7rf0n05TempValidation.java:10: 错误: 非法字符: '#'

# 作业 2: 高吞吐

^
C:\Users\luyan\AppData\Local\Temp\tmpg7rf0n05TempValidation.java:10: 错误: 不是语句

# 作业 2: 高吞吐

  ^
C:\Users\

- **错误行**: 10


### `CONTRIBUTING-EN.md`

**问题 #23** (第 913 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp565onqcpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3


### `CONTRIBUTING.md`

**问题 #24** (第 991 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpun04ca_6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3


### `DEPLOYMENT-ARCHITECTURES.md`

**问题 #5** (第 218 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppyb61fw0TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmppy
- **错误行**: 4


### `FAQ.md`

**问题 #7** (第 436 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk2_azs2eTempValidation.java:4: 错误: 找不到符号
AIAgentConfig config = AIAgentConfig.builder()
^
  符号:   类 AIAgentConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #9** (第 502 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp88alz1tbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #11** (第 558 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmzome77wTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #13** (第 627 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpttoljd0wTempValidation.java:4: 错误: 找不到符号
SmartCheckpointMetrics metrics = checkpointConfig.getSmartMetrics();
^
  符号:   类 SmartCheckpointMetrics
  位置: 类 TempValida
- **错误行**: 4

**问题 #16** (第 772 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcu8oqvvlTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #17** (第 826 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpue4ylmzwGPUDetectionFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
StreamExecutionEnvironment env =
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 2

**问题 #24** (第 1053 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsimsa79kTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpsim
- **错误行**: 3

**问题 #25** (第 1089 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看已注册的 WASM UDF
SHOW FUNCTIONS WHERE TYPE = 'WA...; 可能的语法问题: -- 查看 UDF 详情
DESCRIBE FUNCTION STRING_LEN;...

**问题 #31** (第 1273 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp131mm_xoTempValidation.java:4: 错误: 找不到符号
env.setStateBackend(new RocksDBStateBackend("hdfs://checkpoints", true));
                        ^
  符号:   类 RocksDBState
- **错误行**: 4

**问题 #33** (第 1326 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmowtzmv9TempValidation.java:4: 错误: 找不到符号
GPUResource resource = new GPUResource(1, 16);
^
  符号:   类 GPUResource
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 4

**问题 #34** (第 1356 行, 语言: sql)

- **错误**: 可能的语法问题: -- 2.4: 流批一体基础
SET EXECUTION.MODE = 'STREAMING';...; 可能的语法问题: -- 2.5: 新增自适应模式
SET EXECUTION.MODE = 'ADAPTIVE';  ...

**问题 #37** (第 1460 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbn0lmkxgTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpbn0
- **错误行**: 3

**问题 #42** (第 1635 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpehi7mvfzTempValidation.java:5: 错误: 找不到符号
env.enableCheckpointing(5000);  // 每5秒，无论负载
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpe
- **错误行**: 5

**问题 #45** (第 1739 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphemyk7gyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #49** (第 1932 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbyvkj1n6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpbyv
- **错误行**: 3


### `FLINK-IOT-GAP-ANALYSIS.md`

**问题 #1** (第 44 行, 语言: sql)

- **错误**: 可能的语法问题: -- 设备时间作为事件时间，而非KAFKA摄入时间
WATERMARK FOR DEVICE_TIM...

**问题 #7** (第 198 行, 语言: sql)

- **错误**: 可能的语法问题: WATERMARK FOR DEVICE_TIME AS DEVICE_TIME - INTERVA...


### `Flink-IoT-Authority-Alignment\Phase-1-Architecture\01-flink-iot-foundation-and-architecture.md`

**问题 #9** (第 738 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 95, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^ (line: 95)
- **错误行**: 95
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #11** (第 1122 行, 语言: yaml)

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

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8dkcv3n0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8dk
- **错误行**: 3

**问题 #7** (第 417 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphb6d0pcqTempValidation.java:4: 错误: 找不到符号
WatermarkStrategy.<SensorEvent>forBoundedOutOfOrderness(
                   ^
  符号:   类 SensorEvent
  位置: 类 TempValidation
- **错误行**: 4

**问题 #8** (第 448 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpilrbj7kbTempValidation.java:4: 错误: 找不到符号
WatermarkStrategy.<SensorEvent>forBoundedOutOfOrderness(
                   ^
  符号:   类 SensorEvent
  位置: 类 TempValidation
- **错误行**: 4

**问题 #13** (第 574 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdbgq3yd9TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpdbgq3yd9TempValidat
- **错误行**: 4

**问题 #28** (第 1374 行, 语言: sql)

- **错误**: 可能的语法问题: -- AWS IAM角色配置（通过FLINK配置传递）
-- FLINK-CONF.YAML:
--...

**问题 #32** (第 1487 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...


### `Flink-IoT-Authority-Alignment\Phase-1-Architecture\PHASE-1-COMPLETION-REPORT.md`

**问题 #3** (第 141 行, 语言: sql)

- **错误**: 可能的语法问题: WATERMARK FOR DEVICE_TIME AS DEVICE_TIME - INTERVA...


### `Flink-IoT-Authority-Alignment\Phase-10-Telecom\22-flink-iot-telecom-self-healing.md`

**问题 #3** (第 415 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr6fuvp7hTempValidation.java:4: 错误: 找不到符号
DataSet<Vertex<String, Double>> rootCauseScores = faultGraph
^
  符号:   类 DataSet
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4


### `Flink-IoT-Authority-Alignment\Phase-13-Water-Management\25-flink-iot-smart-water-management.md`

**问题 #7** (第 529 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw0mffb_sTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpw0mffb_sTempValidatio
- **错误行**: 4


### `Flink-IoT-Authority-Alignment\Phase-2-Processing\04-flink-iot-hierarchical-downsampling.md`

**问题 #11** (第 495 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplvx9sfwlTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Flink-IoT-Authority-Alignment\Phase-2-Processing\05-flink-iot-alerting-and-monitoring.md`

**问题 #4** (第 248 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdo5kbgizTempValidation.java:5: 错误: 找不到符号
                watermarkStrategy.getCurrentWatermark();
                ^
  符号:   变量 watermarkStrategy
  位置: 类 TempValida
- **错误行**: 5

**问题 #6** (第 284 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq9uxdirfTempValidation.java:6: 错误: 不是语句
- numberOfFailedCheckpoints
^
C:\Users\luyan\AppData\Local\Temp\tmpq9uxdirfTempValidation.java:6: 错误: 需要';'
- numberOfFaile
- **错误行**: 6

**问题 #10** (第 357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpra__xd_vTempValidation.java:6: 错误: 不是语句
- watermarkLag
^
C:\Users\luyan\AppData\Local\Temp\tmpra__xd_vTempValidation.java:6: 错误: 需要';'
- watermarkLag

- **错误行**: 6


### `Flink-IoT-Authority-Alignment\Phase-3-Deployment\06-flink-iot-cloud-native-deployment.md`

**问题 #8** (第 366 行, 语言: sql)

- **错误**: 可能的语法问题: -- 内存存储与磁性存储分层
MEMORY_RETENTION := 24 HOURS   -- 热...

**问题 #33** (第 3264 行, 语言: yaml)

- **错误**: while parsing a flow node
expected the node content, but found '-'
  in "<unicode string>", line 4, column 3:
    {{- define "flink-iot.deployment" -}}
      ^ (line: 4)
- **错误行**: 4


### `Flink-IoT-Authority-Alignment\Phase-3-Deployment\07-flink-iot-performance-tuning.md`

**问题 #6** (第 482 行, 语言: sql)

- **错误**: 可能的语法问题: -- ========================================
-- FLI...; 可能的语法问题: -- 2. CHECKPOINT配置（生产环境推荐）
SET 'EXECUTION.CHECKPOI...; 可能的语法问题: -- 3. 状态后端配置
SET 'STATE.BACKEND' = 'ROCKSDB';...; 可能的语法问题: -- 4

**问题 #8** (第 599 行, 语言: sql)

- **错误**: 可能的语法问题: -- ========================================
-- ROC...; 可能的语法问题: -- 1. 内存调优参数
SET 'STATE.BACKEND.ROCKSDB.MEMORY.MAN...; 可能的语法问题: -- 2. WRITEBUFFER配置
SET 'STATE.BACKEND.ROCKSDB.WRI...; 可能的语法问题:


### `Flink-IoT-Authority-Alignment\Phase-4-Case-Study\08-flink-iot-complete-case-study.md`

**问题 #17** (第 1735 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 103, column 39:
     ...   jobmanager.memory.process.size: 2048m
                                         ^ (line: 103)
- **错误行**: 103
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #24** (第 2344 行, 语言: sql)

- **错误**: 可能的语法问题: -- 1. 使用 MINIBATCH 优化聚合性能
SET TABLE.EXEC.MINI-BATC...; 可能的语法问题: -- 2. 启用 LOCAL-GLOBAL 聚合
SET TABLE.OPTIMIZER.AGG-P...; 可能的语法问题: -- 3. 使用 ROCKSDB 状态后端
SET STATE.BACKEND = 'ROCKSDB...; 可能的语法问题:


### `Flink-IoT-Authority-Alignment\Phase-4-Case-Study\09-flink-iot-pattern-catalog.md`

**问题 #2** (第 91 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx_r7sqsbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpx_r
- **错误行**: 3

**问题 #3** (第 110 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqe5u1hkcTempValidation.java:4: 错误: 找不到符号
ExecutionEnvironment batchEnv = ExecutionEnvironment.getExecutionEnvironment();
^
  符号:   类 ExecutionEnvironment
  位置: 类 T
- **错误行**: 4

**问题 #4** (第 123 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvx59cqbxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpvx5
- **错误行**: 3

**问题 #5** (第 139 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmlq6v1akTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpmlq
- **错误行**: 3

**问题 #6** (第 185 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2x2gcj5nTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2x2
- **错误行**: 3

**问题 #7** (第 206 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplg568x_8TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmplg568x_8TempValidat
- **错误行**: 4

**问题 #8** (第 243 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4sj899baTempValidation.java:4: 错误: 找不到符号
Properties prodMqttProps = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #9** (第 264 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz29p31piTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpz29
- **错误行**: 3

**问题 #10** (第 285 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyn8kl01iTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpyn8kl01
- **错误行**: 3

**问题 #11** (第 308 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvghiom0dTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpvghiom0dTempValidat
- **错误行**: 4

**问题 #12** (第 352 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjgzeme5yTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpjgzeme5yTempValidat
- **错误行**: 4

**问题 #14** (第 453 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwjkribdlAverageAggregate.java:6: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<AvgTemperature> avgTemp = sensorStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 6

**问题 #15** (第 496 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp10htitk5TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp10h
- **错误行**: 3

**问题 #16** (第 520 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz1tsxfvsSessionProcessFunction.java:6: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<DeviceSession> sessions = sensorStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 6

**问题 #17** (第 578 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaeiie2hzTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpaeiie2hzTempValidat
- **错误行**: 4

**问题 #19** (第 636 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpidhd5rpnTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpidhd5rpnTempValidat
- **错误行**: 4

**问题 #20** (第 697 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprm1hpduaTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmprm1hpduaTempValidat
- **错误行**: 4

**问题 #21** (第 759 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5z7ca6puHeartbeatMonitor.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
Pattern<DeviceEvent, ?> offlinePattern = Pattern
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppDat
- **错误行**: 2

**问题 #22** (第 832 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpahmuj09gTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpahm
- **错误行**: 3

**问题 #24** (第 908 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwn9jz6zlTempValidation.java:10: 错误: 找不到符号
tableEnv.executeSql(createCatalog);
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpwn9
- **错误行**: 10

**问题 #25** (第 935 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgggzeavaTempValidation.java:4: 错误: 找不到符号
Map<String, String> hudiOptions = new HashMap<>();
^
  符号:   类 Map
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #26** (第 958 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphbpk5gugTempValidation.java:4: 错误: 找不到符号
PinotSinkFunction<GenericRow> pinotSink = new PinotSinkFunction<>(
^
  符号:   类 PinotSinkFunction
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #30** (第 1132 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpda1_wkvqTempValidation.java:5: 错误: 需要';'
appender.json.type = RollingFile
                                ^
C:\Users\luyan\AppData\Local\Temp\tmpda1_wkvqTempValida
- **错误行**: 5

**问题 #32** (第 1166 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3j1h_7htTracedFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
OpenTelemetry openTelemetry = OpenTelemetrySdk.builder()
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #43** (第 1486 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6gbjqjfyTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp6gbjqjfyTempV
- **错误行**: 4

**问题 #44** (第 1506 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplgsqir1uTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmplgsqir1uTempValidat
- **错误行**: 4


### `Flink-IoT-Authority-Alignment\Phase-7-Smart-Retail\case-smart-retail-complete.md`

**问题 #39** (第 6123 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv3uz0fylTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpv3uz0
- **错误行**: 3


### `Flink-IoT-Authority-Alignment\Phase-8-Wearables\case-wearables-health-complete.md`

**问题 #28** (第 2839 行, 语言: sql)

- **错误**: 可能的语法问题: AND AVG(GLUCOSE_MGDL) > 200;...

**问题 #41** (第 3838 行, 语言: sql)

- **错误**: 可能的语法问题: -- 3小时和6小时预测（类似逻辑，使用更长历史数据）
-- 此处省略类似代码......


### `Flink\00-FLINK-TECH-STACK-DEPENDENCY.md`

**问题 #8** (第 365 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi0hhs6iuTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #9** (第 390 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2ocjb6fmTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2ocjb6fmTemp
- **错误行**: 3

**问题 #11** (第 427 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpne0a09wnTempValidation.java:7: 错误: 找不到符号
FlinkKafkaConsumer<Event> source = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\User
- **错误行**: 7


### `Flink\00-meta\00-QUICK-START.md`

**问题 #10** (第 327 行, 语言: sql)

- **错误**: 可能的语法问题: -- 步骤 1:注册 MCP 工具
-- 注: 以下为未来可能的语法(概念设计),尚未正式实现
<!...; 可能的语法问题: -- 步骤 2:创建 AI AGENT(未来可能的语法,概念设计阶段)
<!-- 以下语法为概念设计...

**问题 #11** (第 378 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyjutacbgTempValidation.java:4: 错误: 找不到符号
Agent agent = Agent.builder()
^
  符号:   类 Agent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpyjutacbgTempVa
- **错误行**: 4

**问题 #17** (第 570 行, 语言: sql)
- **错误**: 可能的语法问题: USE CATALOG PAIMON_CATALOG;...

**问题 #18** (第 615 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph85nsyntTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #19** (第 638 行, 语言: sql)
- **错误**: 可能的语法问题: -- 配置自适应执行
SET EXECUTION.RUNTIME-MODE = ADAPTIVE;...

**问题 #22** (第 727 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqlxfamzjTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqlx
- **错误行**: 3

**问题 #25** (第 811 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl_9z12v9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpl_9z12v9Temp
- **错误行**: 3


### `Flink\01-concepts\datastream-v2-semantics.md`

**问题 #12** (第 336 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphy0ctuzlBadV1Function.java:1: 错误: 程序包org.apache.flink.streaming.api.functions不存在
import org.apache.flink.streaming.api.functions.ProcessFunction;

- **错误行**: 1

**问题 #16** (第 457 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp09x3_jmlAsyncAggregator.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
KafkaSource<Event> source = KafkaSource.<Event>builder()
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan
- **错误行**: 2

**问题 #17** (第 497 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_ql9wy5hDeduplicateFunction.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
RecordAttributes attrs = RecordAttributes.builder()
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 1


### `Flink\01-concepts\disaggregated-state-analysis.md`

**问题 #3** (第 365 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx2gwecfuTempValidation.java:3: 错误: 找不到符号
        DisaggregatedStateBackend stateBackend = new DisaggregatedStateBackend(
        ^
  符号:   类 DisaggregatedStateBack
- **错误行**: 3

**问题 #4** (第 394 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf4psp2thTempValidation.java:10: 错误: 需要';'
    .build()
            ^
1 个错误

- **错误行**: 10


### `Flink\01-concepts\flink-1.x-vs-2.0-comparison.md`

**问题 #7** (第 253 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqax_u7ghTempValidation.java:4: 错误: 找不到符号
CountState current = state.value();  // 阻塞调用
^
  符号:   类 CountState
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #8** (第 264 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdfrz204aTempValidation.java:4: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpdfrz204aTe
- **错误行**: 4

**问题 #13** (第 374 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7rrrhx_yTempValidation.java:3: 错误: 非法的表达式开始
public void processElement(Event event, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmp7rrrhx_yTempValidation.ja
- **错误行**: 3

**问题 #14** (第 385 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd4asmsphTempValidation.java:3: 错误: 非法的表达式开始
public void processElement(Event event, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpd4asmsphTempValidation.ja
- **错误行**: 3


### `Flink\01-concepts\flink-architecture-evolution-1x-to-2x.md`

**问题 #1** (第 250 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjdaok9t4TempValidation.java:4: 错误: 找不到符号
   state.getAsync(key)
                  ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpjdao
- **错误行**: 4


### `Flink\01-concepts\flink-system-architecture-deep-dive.md`

**问题 #13** (第 389 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo4s9nku_TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpo4
- **错误行**: 4

**问题 #14** (第 411 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5cp112caTempValidation.java:4: 错误: 非法的表达式开始
private void handleSubmitJob(SubmitJob submitJob) {
^
C:\Users\luyan\AppData\Local\Temp\tmp5cp112caTempValidation.java:
- **错误行**: 4

**问题 #15** (第 434 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpik1mwzslTempValidation.java:4: 错误: 非法的表达式开始
public void start() throws Exception {
^
C:\Users\luyan\AppData\Local\Temp\tmpik1mwzslTempValidation.java:25: 错误: 需要 cl
- **错误行**: 4

**问题 #16** (第 459 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpggy6cvyuTempValidation.java:4: 错误: 非法的表达式开始
private void deployTask(ExecutionVertex vertex, LogicalSlot slot) {
^
C:\Users\luyan\AppData\Local\Temp\tmpggy6cvyuTemp
- **错误行**: 4

**问题 #17** (第 479 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzp3l9qvpTempValidation.java:4: 错误: 非法的表达式开始
public void submitTask(TaskDeploymentDescriptor tdd) {
^
C:\Users\luyan\AppData\Local\Temp\tmpzp3l9qvpTempValidation.ja
- **错误行**: 4

**问题 #20** (第 568 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpew1vl1_fTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #24** (第 683 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnzslbtuoTempValidation.java:4: 错误: 非法的表达式开始
public void triggerCheckpoint(long timestamp) {
^
C:\Users\luyan\AppData\Local\Temp\tmpnzslbtuoTempValidation.java:30:
- **错误行**: 4

**问题 #35** (第 1222 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo3tkwfxlTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpo3t
- **错误行**: 3


### `Flink\02-core\adaptive-execution-engine-v2.md`

**问题 #11** (第 677 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4r5o6ii8SkewResistantAggregate.java:41: 错误: 需要 class、interface、enum 或 record
dataStream
^
1 个错误

- **错误行**: 41

**问题 #19** (第 1141 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu82ogom9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #20** (第 1187 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp1q57hz5TempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4


### `Flink\02-core\async-execution-model.md`

**问题 #7** (第 435 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt689xna3OrderedCallback.java:8: 错误: 未命名类 是预览功能，默认情况下禁用。
PriorityQueue<OrderedCallback> callbackQueue =
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 8

**问题 #9** (第 487 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2neai95lTempValidation.java:4: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp2neai95lTe
- **错误行**: 4

**问题 #10** (第 505 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4djj9108TempValidation.java:4: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp4djj9108Te
- **错误行**: 4

**问题 #15** (第 729 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi8gwpke6TempValidation.java:3: 错误: 非法的表达式开始
public void processElement(Event event, Context ctx, ResultFuture<Result> resultFuture) {
^
C:\Users\luyan\AppData\Loca
- **错误行**: 3

**问题 #16** (第 768 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpet5sgcgqTempValidation.java:3: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpet5sgcgqTe
- **错误行**: 3

**问题 #17** (第 782 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpspswnswgTempValidation.java:3: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpspswnswgTe
- **错误行**: 3

**问题 #24** (第 1179 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfk2lo55jAECCallbackProcessor.java:4: 错误: 找不到符号
    void onStateAccessComplete(Key key, long sequence, Result result) {
                               ^
  符号:   类 K
- **错误行**: 4


### `Flink\02-core\checkpoint-mechanism-deep-dive.md`

**问题 #1** (第 174 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2495t4h1StateBackend.java:3: 错误: 需要<标识符>
    createKeyedStateBackend(env, stateHandles): AbstractKeyedStateBackend<K>
                           ^
C:\Users\luyan\A
- **错误行**: 3

**问题 #5** (第 537 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzaug1qsgTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend = new EmbeddedRocksDBStateBackend(true);
^
  符号:   类 EmbeddedRocksDBStateBacken
- **错误行**: 4

**问题 #8** (第 704 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprs5j2s6dTempValidation.java:4: 错误: 非法的表达式开始
public boolean restoreSavepoint(
^
C:\Users\luyan\AppData\Local\Temp\tmprs5j2s6dTempValidation.java:76: 错误: 需要 class、in
- **错误行**: 4

**问题 #10** (第 881 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphqrwefbkTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #11** (第 915 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkjwjww1lTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #12** (第 942 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdftxzdslTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #13** (第 963 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo_866gzxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Flink\02-core\delta-join-production-guide.md`

**问题 #1** (第 59 行, 语言: sql)
- **错误**: 可能的语法问题: -- MYSQL CDC 源:忽略 DELETE 操作
'DEBEZIUM.SKIPPED.OPER...

**问题 #11** (第 699 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp484nn8umTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #22** (第 1278 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbjqxdvoiTempValidation.java:4: 错误: 找不到符号
if (errorRate > 0.05 || avgLatency > 1000) {
    ^
  符号:   变量 errorRate
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #23** (第 1289 行, 语言: sql)
- **错误**: 可能的语法问题: -- 步骤1: 禁用 DELTA JOIN 优化
SET TABLE.OPTIMIZER.DELTA...; 可能的语法问题: -- 步骤2: 增加 REGULAR JOIN 状态 TTL
SET TABLE.EXEC.STAT...; 可能的语法问题: -- 步骤3: 优化 CHECKPOINT 配置
SET EXECUTION.CHECKPOINTI...; 可能的语法问题:

**问题 #24** (第 1332 行, 语言: sql)
- **错误**: 可能的语法问题: 'DEBEZIUM.SKIPPED.OPERATIONS' = 'D',  -- 必须
'DEBEZ...

**问题 #25** (第 1339 行, 语言: sql)
- **错误**: 可能的语法问题: 'LOOKUP.ASYNC' = 'TRUE',
'LOOKUP.CACHE.MAX-ROWS' =...

**问题 #26** (第 1347 行, 语言: sql)
- **错误**: 可能的语法问题: 'LOOKUP.CACHE.MAX-ROWS' = '200000',
'LOOKUP.CACHE....


### `Flink\02-core\delta-join.md`

**问题 #3** (第 244 行, 语言: sql)
- **错误**: 可能的语法问题: -- FLINK SQL开启DELTA JOIN优化
SET TABLE.OPTIMIZER.MUL...

**问题 #4** (第 317 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpixpeny4eAsyncUserProfileLookup.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<UserEvent> userEvents = env.fromSource(
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luya
- **错误行**: 2

**问题 #9** (第 539 行, 语言: sql)
- **错误**: 可能的语法问题: -- 优化后:投影下推,仅查询必要字段
-- 外部查询变为:SELECT USER_ID, AGE,...


### `Flink\02-core\exactly-once-end-to-end.md`

**问题 #2** (第 98 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzy1mr8jsTempValidation.java:3: 错误: 找不到符号
        Properties properties = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 3

**问题 #6** (第 263 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0ardb83sTempValidation.java:3: 错误: 找不到符号
        Properties properties = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 3

**问题 #7** (第 281 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjdtptmshTempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #10** (第 357 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphy2lta7kTempValidation.java:3: 错误: 找不到符号
JdbcXaSinkFunction<Row> xaSink = new JdbcXaSinkFunction<>(
^
  符号:   类 JdbcXaSinkFunction
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #11** (第 398 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyk_ya63fTempValidation.java:4: 错误: 需要';'
protected void preCommit(String pendingFile) throws Exception {
                        ^
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #16** (第 556 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdjz69qw0TempValidation.java:3: 错误: 需要';'
KafkaSource<String> createKafkaSource(String bootstrapServers, String topic, String groupId) {

- **错误行**: 3

**问题 #17** (第 576 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm5zrwxq3TempValidation.java:3: 错误: 需要';'
KafkaSink<String> createKafkaSink(String bootstrapServers, String topic, String transactionalIdPrefix) {

- **错误行**: 3

**问题 #21** (第 772 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4jtyj5_5TempValidation.java:9: 错误: 非法的表达式开始
    protected abstract TXN beginTransaction() throws Exception;
    ^
C:\Users\luyan\AppData\Local\Temp\tmp4jtyj5_5Temp
- **错误行**: 9

**问题 #23** (第 842 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp38ho644jTempValidation.java:7: 错误: 需要';'
    public void snapshotState(FunctionSnapshotContext context) throws Exception {
                             ^
C:\Users\
- **错误行**: 7

**问题 #24** (第 876 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6kcki1r1TempValidation.java:7: 错误: 需要';'
    public void notifyCheckpointComplete(long checkpointId) throws Exception {
                                        ^
C
- **错误行**: 7

**问题 #28** (第 1140 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjriqopk2TempValidation.java:7: 错误: 需要';'
    public void initializeState(FunctionInitializationContext context) throws Exception {
                               ^
- **错误行**: 7


### `Flink\02-core\exactly-once-semantics-deep-dive.md`

**问题 #4** (第 241 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpen08ugceTempValidation.java:4: 错误: 找不到符号
properties.setProperty("enable.auto.commit", "false");
^
  符号:   变量 properties
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #5** (第 269 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbnb0c67vTempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #6** (第 285 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo_1k52mkTempValidation.java:4: 错误: 找不到符号
String transactionalIdPrefix = jobId + "-" + operatorId;
                               ^
  符号:   变量 jobId
  位置: 类 TempVal
- **错误行**: 4

**问题 #7** (第 310 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7i22n9c8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp7i22n9c
- **错误行**: 3

**问题 #8** (第 348 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq1p48524TempValidation.java:3: 错误: 找不到符号
        Properties consumerProps = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 3

**问题 #15** (第 919 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps686wn_wTempValidation.java:4: 错误: 找不到符号
env.getCheckpointConfig().enableUnalignedCheckpoints(true);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4

**问题 #21** (第 1227 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppqbdd5obTempValidation.java:6: 错误: 非法的表达式开始
    private void onCheckpointTimeout(long checkpointId) {
    ^
C:\Users\luyan\AppData\Local\Temp\tmppqbdd5obTempValida
- **错误行**: 6


### `Flink\02-core\flink-2.0-forst-state-backend.md`

**问题 #5** (第 370 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphvt8328aTempValidation.java:4: 错误: 找不到符号
StateDescriptor<V> descriptor = StateDescriptor
^
  符号:   类 StateDescriptor
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 4


### `Flink\02-core\flink-2.2-frontier-features.md`

**问题 #8** (第 709 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_6qjziq9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #9** (第 732 行, 语言: sql)
- **错误**: 可能的语法问题: -- 3. 创建嵌入模型(使用 ML_PREDICT)
<!-- 以下语法为概念设计,实际 FLIN...

**问题 #10** (第 835 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzkxeu411TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #11** (第 864 行, 语言: sql)
- **错误**: 可能的语法问题: -- 4. 查看物化表
SHOW MATERIALIZED TABLES;...

**问题 #13** (第 1038 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7dfar568TempValidation.java:8: 错误: 非法的表达式开始
import org.apache.flink.api.connector.source.SourceReaderContext;
^
C:\Users\luyan\AppData\Local\Temp\tmp7dfar568TempVa
- **错误行**: 8

**问题 #15** (第 1108 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6oj1z2doTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #16** (第 1125 行, 语言: sql)
- **错误**: 可能的语法问题: -- SQL CLIENT 配置
SET 'CLUSTER.SCHEDULING.STRATEGY'...


### `Flink\02-core\flink-state-management-complete-guide.md`

**问题 #6** (第 551 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_s3ktpigTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp_s3ktpi
- **错误行**: 3

**问题 #18** (第 1346 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjqgap0isTempValidation.java:9: 错误: 不是语句
taskmanager.memory.framework.heap.size: 512mb
                                 ^
C:\Users\luyan\AppData\Local\Temp\tmpjqgap
- **错误行**: 9

**问题 #19** (第 1360 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsnhatvtrTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDb = new EmbeddedRocksDBStateBackend(true);
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置:
- **错误行**: 4

**问题 #21** (第 1392 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwvl1o_l2TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.typeinfo.Types;
^
C:\Users\luyan\AppData\Local\Temp\tmpwvl1o_l2TempValidation.java:4
- **错误行**: 4

**问题 #22** (第 1415 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6lz_0ijwTempValidation.java:5: 错误: 找不到符号
for (String key : keys) {
                  ^
  符号:   变量 keys
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 5

**问题 #23** (第 1427 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8naagoe7TempValidation.java:4: 错误: 找不到符号
if (listSize > MAX_LIST_SIZE) {
    ^
  符号:   变量 listSize
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp8naa
- **错误行**: 4

**问题 #24** (第 1446 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprkklv3ajTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmprkklv3ajTempV
- **错误行**: 4

**问题 #25** (第 1465 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpai75krf6TempValidation.java:4: 错误: 找不到符号
env.getCheckpointConfig().enableUnalignedCheckpoints();
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #26** (第 1485 行, 语言: sql)
- **错误**: 可能的语法问题: -- 设置全局 STATE TTL
SET 'SQL.STATE-TTL' = '1 DAY';...

**问题 #27** (第 1516 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpglbpt6h2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpglbpt
- **错误行**: 3

**问题 #29** (第 1575 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2drrqcv3TempValidation.java:5: 错误: 需要';'
public void open(Configuration parameters) {
                ^
C:\Users\luyan\AppData\Local\Temp\tmp2drrqcv3TempValidation
- **错误行**: 5

**问题 #30** (第 1592 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5020uxchTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5020u
- **错误行**: 3

**问题 #31** (第 1614 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0b_kz1yuTempValidation.java:4: 错误: 非法的表达式开始
private transient long lastAccessTime;
^
C:\Users\luyan\AppData\Local\Temp\tmp0b_kz1yuTempValidation.java:25: 错误: 需要 cl
- **错误行**: 4

**问题 #32** (第 1652 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcc8eb30vTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpcc
- **错误行**: 4

**问题 #33** (第 1702 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcpleux20UserState.java:14: 错误: 需要 class、interface、enum 或 record
env.getConfig().registerTypeWithKryoSerializer(UserState.class, new CompatibleSerializer());
^
C:\U
- **错误行**: 14


### `Flink\02-core\flink-state-ttl-best-practices.md`

**问题 #4** (第 224 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp57yrzbqtTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.StateTtlConfig;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp57yrzbq
- **错误行**: 3

**问题 #5** (第 246 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7xdlvaw_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp7xdlv
- **错误行**: 3

**问题 #6** (第 269 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcd52cq8bTempValidation.java:4: 错误: 找不到符号
StateTtlConfig rocksdbCleanup = StateTtlConfig
^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 4

**问题 #8** (第 325 行, 语言: sql)
- **错误**: 可能的语法问题: -- 设置全局 STATE TTL
SET 'SQL.STATE-TTL' = '1 DAY';...

**问题 #9** (第 350 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0nh4xp62TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmp0nh4xp62TempValidatio
- **错误行**: 4

**问题 #10** (第 370 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphv9sxsp9TempValidation.java:7: 错误: 非法的表达式开始
public StateTtlConfig createAggregationTtlConfig() {
^
C:\Users\luyan\AppData\Local\Temp\tmphv9sxsp9TempValidation.java
- **错误行**: 7

**问题 #21** (第 891 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb95mj6wtTempValidation.java:5: 错误: 找不到符号
    (Gauge<Long>) () -> {
     ^
  符号:   类 Gauge
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpb95mj6wtTempV
- **错误行**: 5

**问题 #22** (第 908 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkii_su3gTempValidation.java:5: 错误: 需要';'
public void open(Configuration parameters) {
                ^
C:\Users\luyan\AppData\Local\Temp\tmpkii_su3gTempValidation
- **错误行**: 5

**问题 #24** (第 925 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdzgdbvcrTempValidation.java:3: 错误: 非法的表达式开始
        .cleanupIncrementally(
        ^
C:\Users\luyan\AppData\Local\Temp\tmpdzgdbvcrTempValidation.java:6: 错误: 需要';'

- **错误行**: 3

**问题 #25** (第 934 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq8pivj3bTempValidation.java:3: 错误: 找不到符号
        env.setStateBackend(new EmbeddedRocksDBStateBackend());
                                ^
  符号:   类 EmbeddedRocksD
- **错误行**: 3

**问题 #26** (第 953 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7x5rj69pTempValidation.java:3: 错误: 找不到符号
        DefaultConfigurableOptionsFactory factory = new DefaultConfigurableOptionsFactory();
        ^
  符号:   类 DefaultCo
- **错误行**: 3


### `Flink\02-core\forst-state-backend.md`

**问题 #6** (第 459 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqd_vrb4tTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpqd
- **错误行**: 4


### `Flink\02-core\multi-way-join-optimization.md`

**问题 #10** (第 354 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe0_e_3ylTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpe0_
- **错误行**: 3

**问题 #11** (第 389 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8av71z7rTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8av
- **错误行**: 3


### `Flink\02-core\network-stack-evolution.md`

**问题 #9** (第 526 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkocv49gbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Flink\02-core\smart-checkpointing-strategies.md`

**问题 #20** (第 1205 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6t9jojlsTempValidation.java:5: 错误: 非法字符: '#'
# ============================================================
^
C:\Users\luyan\AppData\Local\Temp\tmp6t9jojlsTempVali
- **错误行**: 5

**问题 #21** (第 1235 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpziwyjxjqTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #22** (第 1262 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph_t64jk7TempValidation.java:5: 错误: 非法字符: '#'
# ============================================================
^
C:\Users\luyan\AppData\Local\Temp\tmph_t64jk7TempVali
- **错误行**: 5

**问题 #23** (第 1291 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn8400wp3TempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend rocksDbBackend = new RocksDBStateBackend(
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempValidation
C:\Us
- **错误行**: 4

**问题 #24** (第 1316 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplgvdct56TempValidation.java:5: 错误: 非法字符: '#'
# ============================================================
^
C:\Users\luyan\AppData\Local\Temp\tmplgvdct56TempVali
- **错误行**: 5

**问题 #25** (第 1342 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp25u9ixtbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #26** (第 1375 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgu9_9dbkTempValidation.java:5: 错误: 非法字符: '#'
# ============================================================
^
C:\Users\luyan\AppData\Local\Temp\tmpgu9_9dbkTempVali
- **错误行**: 5

**问题 #27** (第 1401 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr3x4cwkrTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Flink\02-core\state-backend-evolution-analysis.md`

**问题 #2** (第 284 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmb9sr7wiTempValidation.java:5: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpmb
- **错误行**: 5

**问题 #3** (第 309 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbxvk9rb7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #5** (第 370 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpco5eu5g3TempValidation.java:4: 错误: 找不到符号
ForStStateBackend forstBackend = new ForStStateBackend();
^
  符号:   类 ForStStateBackend
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #7** (第 428 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyvvfx5hbEmbeddedRocksDBStateBackend.java:37: 错误: 非法的表达式开始
        );
        ^
1 个错误

- **错误行**: 37

**问题 #8** (第 481 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplyxzx41gForStStateBackend.java:46: 错误: 非法的表达式开始
        );
        ^
1 个错误

- **错误行**: 46


### `Flink\02-core\state-backends-deep-comparison.md`

**问题 #3** (第 543 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg0iymrsiTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #5** (第 580 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpood40hr6TempValidation.java:5: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 5

**问题 #6** (第 630 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoyemd1_5TempValidation.java:5: 错误: 找不到符号
ForStStateBackend forstBackend = new ForStStateBackend();
^
  符号:   类 ForStStateBackend
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 5


### `Flink\02-core\streaming-etl-best-practices.md`

**问题 #5** (第 513 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp51731n9qTempValidation.java:4: 错误: 找不到符号
MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
^
  符号:   类 MySqlSource
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #7** (第 555 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgobdoy8lTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.state.ValueState;
^
C:\Users\luyan\AppData\Local\Temp\tmpgobdoy8lTempValidation.java
- **错误行**: 4

**问题 #8** (第 590 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu7g3f7rjTempValidation.java:4: 错误: 找不到符号
JdbcInputFormat jdbcInput = JdbcInputFormat.buildJdbcInputFormat()
^
  符号:   类 JdbcInputFormat
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #11** (第 744 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzkyegfcfTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpzkyegfcfTempValidat
- **错误行**: 4

**问题 #12** (第 809 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6ikeqkp_TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmp6ikeqkp_TempValidatio
- **错误行**: 4

**问题 #14** (第 850 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpecljl_q7AsyncDatabaseRequest.java:43: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedEvent> enriched = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以启用 未命名
- **错误行**: 43

**问题 #15** (第 925 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgm4b898oTempValidation.java:18: 错误: 不是语句
"INSERT INTO table (id, value) VALUES (?, ?) " +
^
C:\Users\luyan\AppData\Local\Temp\tmpgm4b898oTempValidation.java:19: 错误
- **错误行**: 18

**问题 #17** (第 1001 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphdetwwumTempValidation.java:4: 错误: 找不到符号
StreamingFileSink<Record> sink = StreamingFileSink
^
  符号:   类 StreamingFileSink
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4

**问题 #22** (第 1173 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_s24rohtTempValidation.java:4: 错误: 找不到符号
AvroDeserializationSchema<Order> schema = AvroDeserializationSchema
^
  符号:   类 AvroDeserializationSchema
  位置: 类 TempVali
- **错误行**: 4

**问题 #25** (第 1302 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjng44pinTempValidation.java:4: 错误: 找不到符号
env.getConfig().setAutoWatermarkInterval(200L);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #26** (第 1327 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5n0wipzcTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5n0wi
- **错误行**: 3

**问题 #27** (第 1356 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps3afqi9nTempValidation.java:4: 错误: 找不到符号
SpecificAvroSerde<Order> serde = new SpecificAvroSerde<>();
^
  符号:   类 SpecificAvroSerde
  位置: 类 TempValidation
C:\Users\
- **错误行**: 4

**问题 #31** (第 1438 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2acc9c6gTempValidation.java:4: 错误: 找不到符号
OutputTag<FailedRecord> dlqTag = new OutputTag<FailedRecord>("dlq"){};
^
  符号:   类 OutputTag
  位置: 类 TempValidation
C:\Use
- **错误行**: 4


### `Flink\02-core\time-semantics-and-watermark.md`

**问题 #1** (第 300 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc7yh2_mlTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpc7yh2
- **错误行**: 3

**问题 #2** (第 310 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkbh5t8zmTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpkbh5t
- **错误行**: 3

**问题 #3** (第 320 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqeoz2p9eTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqeoz2
- **错误行**: 3

**问题 #6** (第 550 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzd11r8s8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpzd1
- **错误行**: 3

**问题 #7** (第 562 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcuqljnpaTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpcuq
- **错误行**: 3

**问题 #8** (第 578 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5i7ac68zTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5i7ac
- **错误行**: 3

**问题 #9** (第 589 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp39etr_z8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp39etr
- **错误行**: 3

**问题 #10** (第 600 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprbup_7vwTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmprbup_
- **错误行**: 3

**问题 #11** (第 614 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkdrcwb2gTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpkdr
- **错误行**: 3

**问题 #24** (第 1150 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc1u8ms2wWatermarkStrategy.java:19: 错误: 需要 class、interface、enum 或 record
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
^
1 个错误

- **错误行**: 19


### `Flink\03-api\03.02-table-sql-api\ansi-sql-2023-compliance-guide.md`

**问题 #1** (第 104 行, 语言: sql)
- **错误**: 可能的语法问题: MATCH_RECOGNIZE (
    PARTITION BY PARTITION_KEY  ...

**问题 #5** (第 371 行, 语言: sql)
- **错误**: 可能的语法问题: JSON_VALUE(JSON_FIELD, '$.PATH'
    RETURNING VARC...

**问题 #6** (第 392 行, 语言: sql)
- **错误**: 可能的语法问题: JSON_TABLE(
    JSON_DATA,
    '$.ITEMS[*]'
    CO...

**问题 #8** (第 501 行, 语言: sql)
- **错误**: 可能的语法问题: -- 执行结果示例
-- {"ORDER_ID":1001,"CUSTOMER":"ALICE","...

**问题 #13** (第 605 行, 语言: sql)
- **错误**: 可能的语法问题: -- 输出: 每5分钟累积一次,每小时重置
-- [00:00, 00:05), [00:00, 0...

**问题 #24** (第 1058 行, 语言: sql)
- **错误**: 可能的语法问题: -- ============================================
--...


### `Flink\03-api\03.02-table-sql-api\data-types-complete-reference.md`

**问题 #2** (第 107 行, 语言: sql)
- **错误**: 可能的语法问题: STRING          -- 无限制长度
STRING(100)     -- 限制最大长度...

**问题 #3** (第 123 行, 语言: sql)
- **错误**: 可能的语法问题: VARCHAR         -- 同STRING,无限制
VARCHAR(N)      -- ...

**问题 #4** (第 138 行, 语言: sql)
- **错误**: 可能的语法问题: CHAR(N)         -- 固定N字符...

**问题 #5** (第 164 行, 语言: sql)
- **错误**: 可能的语法问题: DECIMAL(10, 2)   -- 8位整数 + 2位小数,如12345678.90
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
- **错误**: 可能的语法问题: TIME                    -- TIME(0),无小数秒
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
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_e3n5vatTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.DataTypes;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp_e3n5vatTempValidat
- **错误行**: 3

**问题 #19** (第 586 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn1omlpzkTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpn1omlpzkTempV
- **错误行**: 3

**问题 #22** (第 691 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqfdx2xn_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqfdx2xn_Temp
- **错误行**: 3


### `Flink\03-api\03.02-table-sql-api\flink-cep-complete-guide.md`

**问题 #9** (第 316 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjomn2pfeLoginEvent.java:16: 错误: 未命名类 是预览功能，默认情况下禁用。
Pattern<LoginEvent, ?> pattern = Pattern
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 16

**问题 #10** (第 352 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqd86iq3lTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.cep.pattern.Pattern;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqd86iq3lTempValidat
- **错误行**: 3

**问题 #11** (第 387 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo18x020eTempValidation.java:4: 错误: 找不到符号
Pattern.<Event>begin("login").where(evt -> evt.type.equals("LOGIN"))
         ^
  符号:   类 Event
  位置: 类 TempValidation
C:\
- **错误行**: 4

**问题 #12** (第 424 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp079oj42hTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.pattern.conditions.IterativeCondition;
^
C:\Users\luyan\AppData\Local\Temp\tmp079oj42hTempV
- **错误行**: 3

**问题 #13** (第 475 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkzikd5ayTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.CEP;
^
C:\Users\luyan\AppData\Local\Temp\tmpkzikd5ayTempValidation.java:3: 错误: 不是语句
import
- **错误行**: 3

**问题 #18** (第 985 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdmrjfdt2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.cep.nfa.aftermatch.AfterMatchSkipStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 3

**问题 #19** (第 1008 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwdtzs27rTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwdtzs
- **错误行**: 3

**问题 #20** (第 1031 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6mkb5hg5TempValidation.java:5: 错误: 找不到符号
    MyEvent.class,
    ^
  符号:   类 MyEvent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp6mkb5hg5TempValidat
- **错误行**: 5

**问题 #21** (第 1047 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7unejzmhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp7unej
- **错误行**: 3

**问题 #26** (第 1254 行, 语言: sql)
- **错误**: 可能的语法问题: -- AFTER MATCH SKIP子句
AFTER MATCH SKIP PAST LAST R...


### `Flink\03-api\03.02-table-sql-api\flink-materialized-table-deep-dive.md`

**问题 #2** (第 114 行, 语言: sql)
- **错误**: 可能的语法问题: -- HASH分布(默认)
DISTRIBUTED BY HASH(USER_ID) INTO 16...


### `Flink\03-api\03.02-table-sql-api\flink-process-table-functions.md`

**问题 #9** (第 500 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpatkn27o4DeduplicationPTF.java:11: 错误: 需要 class、interface、enum 或 record
import org.apache.flink.api.common.typeinfo.Types;
^
1 个错误

- **错误行**: 11

**问题 #10** (第 562 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeaa_ji47TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpeaa_ji47Temp
- **错误行**: 3

**问题 #12** (第 708 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj9h7p_88MLInferencePTF.java:13: 错误: 需要 class、interface、enum 或 record
import org.apache.flink.api.common.state.ValueState;
^
C:\Users\luyan\AppData\Local\Temp\tmpj9
- **错误行**: 13


### `Flink\03-api\03.02-table-sql-api\flink-sql-calcite-optimizer-deep-dive.md`

**问题 #10** (第 652 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxqsd09e3TempValidation.java:4: 错误: 找不到符号
VolcanoPlanner planner = new VolcanoPlanner(
^
  符号:   类 VolcanoPlanner
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #14** (第 774 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp43kxicb1TempValidation.java:4: 错误: 非法的表达式开始
void optimizeGroup(Group group, Cost upperBound) {
^
C:\Users\luyan\AppData\Local\Temp\tmp43kxicb1TempValidation.java:4
- **错误行**: 4

**问题 #16** (第 827 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2864xvffTempValidation.java:4: 错误: 非法的表达式开始
public void onMatch(RelOptRuleCall call) {
^
C:\Users\luyan\AppData\Local\Temp\tmp2864xvffTempValidation.java:37: 错误: 需
- **错误行**: 4

**问题 #19** (第 906 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkzyx59fjTempValidation.java:4: 错误: 非法的表达式开始
public void onMatch(RelOptRuleCall call) {
^
C:\Users\luyan\AppData\Local\Temp\tmpkzyx59fjTempValidation.java:26: 错误: 需
- **错误行**: 4

**问题 #23** (第 1009 行, 语言: sql)
- **错误**: 可能的语法问题: -- 启用两阶段聚合
SET TABLE.OPTIMIZER.AGG-PHASE-STRATEGY ...; 可能的语法问题: -- 或自动选择
SET TABLE.OPTIMIZER.AGG-PHASE-STRATEGY = ...

**问题 #41** (第 1553 行, 语言: sql)
- **错误**: 可能的语法问题: -- 分析整张表
ANALYZE TABLE ORDERS COMPUTE STATISTICS;...; 可能的语法问题: -- 分析指定列
ANALYZE TABLE ORDERS COMPUTE STATISTICS F...; 可能的语法问题: -- 采样分析
ANALYZE TABLE BIG_TABLE COMPUTE STATISTICS...; 可能的语法问题:

**问题 #44** (第 1630 行, 语言: sql)
- **错误**: 可能的语法问题: # 伪代码示意，非完整可执行配置
-- 优化1: 添加统计信息
ANALYZE TABLE ORDE...; 可能的语法问题: ANALYZE TABLE PRODUCTS COMPUTE STATISTICS;...; 可能的语法问题: ANALYZE TABLE CATEGORIES COMPUTE STATISTICS;...; 可能的语法问题: -- 优化2: 启用CBO

**问题 #50** (第 1760 行, 语言: sql)
- **错误**: 可能的语法问题: -- 优化1: 启用DISTINCT拆分
SET TABLE.OPTIMIZER.DISTINCT-...; 可能的语法问题: -- 优化2: 启用MINI-BATCH
SET TABLE.EXEC.MINI-BATCH.ENA...; 可能的语法问题: -- 优化3: 启用LOCAL-GLOBAL聚合
SET TABLE.OPTIMIZER.LOCAL...; 可能的语法问题:

**问题 #66** (第 2514 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4ovjcs1dBatchPhysicalRel.java:31: 错误: 非法的表达式开始
        Transformation<RowData> leftInput = ...;
                                            ^
C:\Users\luyan\AppDat
- **错误行**: 31


### `Flink\03-api\03.02-table-sql-api\flink-sql-hints-optimization.md`

**问题 #12** (第 324 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo0sar9wgTempValidation.java:4: 错误: 找不到符号
tableEnv.createTemporaryFunction("ExtractJson", JsonPathFunction.class);
                                                ^
- **错误行**: 4

**问题 #13** (第 339 行, 语言: sql)
- **错误**: 可能的语法问题: -- 基础执行计划
EXPLAIN PLAN FOR
SELECT /*+ BROADCAST_HA...; 可能的语法问题: -- 详细执行计划(含优化器决策)
EXPLAIN ESTIMATED_COST, CHANGELO...


### `Flink\03-api\03.02-table-sql-api\flink-sql-window-functions-deep-dive.md`

**问题 #4** (第 338 行, 语言: sql)
- **错误**: 可能的语法问题: -- 优化后:仅存储中间状态
-- FLINK自动优化为:
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
- **错误**: 可能的语法问题: -- 输出示例(假设当前为11:00):
-- WINDOW_START        | WIND...

**问题 #13** (第 630 行, 语言: sql)
- **错误**: 可能的语法问题: -- 输出包含CHANGELOG(排名变化时产生撤回更新)
-- +I: 新增排名
-- -D: 旧...

**问题 #15** (第 703 行, 语言: sql)
- **错误**: 可能的语法问题: -- 配置允许延迟
SET 'TABLE.EXEC.EMIT.ALLOW-LATENESS' = '...; 可能的语法问题: -- 延迟数据侧输出(FLINK SQL暂不支持,需DATASTREAM API)
-- 或使用PR...


### `Flink\03-api\03.02-table-sql-api\flink-table-sql-complete-guide.md`

**问题 #7** (第 372 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfdeox_oyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpfdeox_oyTempV
- **错误行**: 3

**问题 #10** (第 446 行, 语言: sql)
- **错误**: 可能的语法问题: -- 切换数据库
USE ANALYTICS;...

**问题 #13** (第 501 行, 语言: sql)
- **错误**: 可能的语法问题: <!-- 以下语法为概念设计,实际 FLINK 版本尚未支持 -->
~~CREATE MODEL~...

**问题 #19** (第 584 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyav41tteTempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.from("orders")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpyav41
- **错误行**: 4

**问题 #24** (第 678 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprp1xxsksTempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.from("user_events")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #32** (第 814 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7ed1rqbcTempValidation.java:4: 错误: 找不到符号
Table topN = tableEnv.from("product_sales")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #39** (第 962 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwiemz8cuTempValidation.java:4: 错误: 找不到符号
Table windowed = tableEnv.from("user_events")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4

**问题 #44** (第 1071 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3nh9vm8vTempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.from("orders")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp3nh9v
- **错误行**: 4

**问题 #53** (第 1377 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp87gnve1_TempValidation.java:12: 错误: 非法的表达式开始
    .next("C").where(...)
                     ^
C:\Users\luyan\AppData\Local\Temp\tmp87gnve1_TempValidation.java:13:
- **错误行**: 12

**问题 #64** (第 1654 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplmo35h1oTempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql(
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #66** (第 1718 行, 语言: sql)

- **错误**: 可能的语法问题: -- 创建嵌入模型
<!-- 以下语法为概念设计,实际 FLINK 版本尚未支持 -->
~~CRE...; 可能的语法问题: -- 创建分类模型
~~CREATE MODEL SENTIMENT_CLASSIFIER~~ (未...

**问题 #76** (第 2076 行, 语言: sql)

- **错误**: 可能的语法问题: -- 1. 配置 STATE TTL
SET 'TABLE.EXEC.STATE.TTL' = '1...; 可能的语法问题: -- 3. 增量 CHECKPOINT
SET 'STATE.BACKEND.INCREMENTAL...; 可能的语法问题: -- 4. ROCKSDB 调优
SET 'STATE.BACKEND.ROCKSDB.PREDEF...

**问题 #77** (第 2094 行, 语言: sql)

- **错误**: 可能的语法问题: -- 1. 合理设置 WATERMARK 延迟
-- 过小: 丢数据
-- 过大: 延迟高
WATE...; 可能的语法问题: -- 3. 允许延迟数据
SET 'TABLE.EXEC.EMIT.ALLOW-LATENESS' ...


### `Flink\03-api\03.02-table-sql-api\flink-vector-search-rag.md`

**问题 #14** (第 613 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...; 可能的语法问题: -- ============================================
--...


### `Flink\03-api\03.02-table-sql-api\materialized-tables.md`

**问题 #11** (第 477 行, 语言: sql)

- **错误**: 可能的语法问题: -- 2. 查看所有物化表(FLINK 2.2+)
SHOW MATERIALIZED TABLES...; 可能的语法问题: -- 3. 查看特定物化表详细信息
DESCRIBE EXTENDED USER_ACTIVITY_...

**问题 #13** (第 547 行, 语言: sql)

- **错误**: 可能的语法问题: -- 手动验证推断的 FRESHNESS
DESCRIBE EXTENDED USER_STATS_...; 可能的语法问题: -- 预期输出: FRESHNESS = 1 MINUTE (基于 5S WATERMARK + 缓...

**问题 #17** (第 658 行, 语言: sql)

- **错误**: 可能的语法问题: -- 优势:
-- 1. 物化表 USER_PROFILES_MT 每小时刷新,存储预计算结果
--...

**问题 #18** (第 701 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6_bsohhzTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp6_bsohhzTempValidat
- **错误行**: 4

**问题 #19** (第 732 行, 语言: sql)

- **错误**: 可能的语法问题: -- FLINK 2.2+ 新增语法

-- 列出所有物化表
SHOW MATERIALIZED T...; 可能的语法问题: -- 列出指定数据库的物化表
SHOW MATERIALIZED TABLES FROM ANALY...; 可能的语法问题: -- 带过滤条件
SHOW MATERIALIZED TABLES LIKE 'USER%';...; 可能的语法问题: --

**问题 #26** (第 1005 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看所有物化表(FLINK 2.2+)
SHOW MATERIALIZED TABLES [F...


### `Flink\03-api\03.02-table-sql-api\model-ddl-and-ml-predict.md`

**问题 #1** (第 19 行, 语言: sql)

- **错误**: 可能的语法问题: <!-- CREATE MODEL 语法仍为概念设计,尚未在 FLINK 2.2 中支持 -->
~...

**问题 #10** (第 257 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsu4jys77TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpsu4jys77TempValidat
- **错误行**: 4

**问题 #13** (第 415 行, 语言: sql)

- **错误**: 可能的语法问题: -- 步骤 1: 创建 OPENAI 模型定义
<!-- 以下为概念设计 -->
~~CREATE ...

**问题 #14** (第 494 行, 语言: sql)

- **错误**: 可能的语法问题: -- 步骤 1: 创建嵌入模型(用于文档向量化)
~~CREATE MODEL TEXT_EMBED...; 可能的语法问题: -- 步骤 2: 创建 LLM 模型
~~CREATE MODEL QA_MODEL~~ (未来可能...

**问题 #16** (第 652 行, 语言: sql)

- **错误**: 可能的语法问题: ~~CREATE MODEL INTERNAL_CLASSIFIER~~ (未来可能的语法)
WIT...

**问题 #21** (第 817 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjb27rrxwTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.table.api.Table;
^
C:\Users\luyan\AppData\Local\Temp\tmpjb27rrxwTempValidation.java:4: 错误: 不是语句
- **错误行**: 4


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
ANALYZE TABLE ORDERS COMPUTE STATISTICS F...; 可能的语法问题: -- 采样分析(大数据表)
ANALYZE TABLE BIG_TABLE COMPUTE STAT...

**问题 #20** (第 698 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看表统计信息
SHOW CREATE TABLE ORDERS;...; 可能的语法问题: -- 通过 EXPLAIN 查看优化器使用的统计
EXPLAIN PLAN FOR SELECT *...

**问题 #22** (第 740 行, 语言: sql)

- **错误**: 可能的语法问题: -- 1. 设置合理的状态 TTL
SET TABLE.EXEC.STATE.TTL = '24 H...; 可能的语法问题: -- 2. 使用 ROCKSDB 状态后端(大状态)
SET STATE.BACKEND = 'RO...; 可能的语法问题: -- 3. 配置增量 CHECKPOINT
SET EXECUTION.CHECKPOINTING....


### `Flink\03-api\03.02-table-sql-api\sql-functions-cheatsheet.md`

**问题 #3** (第 798 行, 语言: sql)

- **错误**: 可能的语法问题: -- 数学
ABS(), ROUND(), CEIL(), FLOOR(), POWER(), SQ...


### `Flink\03-api\03.02-table-sql-api\sql-vs-datastream-comparison.md`

**问题 #3** (第 267 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb9sqyj1dTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.functions.AggregateFunction;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #5** (第 302 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmsrd8tqwTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpmsrd8tqwTempValidatio
- **错误行**: 4

**问题 #6** (第 324 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_m9yas13AsyncUserEnrichment.java:23: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedOrder> enriched = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以启用 未命名类
- **错误行**: 23

**问题 #7** (第 358 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx1kkac9yTempValidation.java:4: 错误: 找不到符号
tableEnv.createTemporaryView("orders", orderStream);
                                       ^
  符号:   变量 orderStream
  位置:
- **错误行**: 4


### `Flink\03-api\09-language-foundations\03-rust-native.md`

**问题 #7** (第 451 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe3wrtr4jTempValidation.java:4: 错误: 找不到符号
    stream,
    ^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpe3wrtr4jTempValidation.jav
- **错误行**: 4


### `Flink\03-api\09-language-foundations\04-streaming-lakehouse.md`

**问题 #19** (第 575 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_CATALOG;...

**问题 #21** (第 776 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...


### `Flink\03-api\09-language-foundations\06-risingwave-deep-dive.md`

**问题 #21** (第 1269 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbucxgqxzTempValidation.java:14: 错误: 找不到符号
MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
^
  符号:   类 MySqlSource
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 14

**问题 #24** (第 1352 行, 语言: sql)

- **错误**: 可能的语法问题: -- 7. 应用层查询示例(LLM RAG 调用)
-- SELECT * FROM RAG_RET...


### `Flink\03-api\09-language-foundations\07-rust-streaming-landscape.md`

**问题 #16** (第 876 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3lng74bnTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp3ln
- **错误行**: 3


### `Flink\03-api\09-language-foundations\08-flink-rust-connector-dev.md`

**问题 #36** (第 2075 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3kcr6zonRustKafkaSourceIntegrationTest.java:3: 错误: 需要 class、interface、enum 或 record
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
- **错误行**: 3


### `Flink\03-api\09-language-foundations\10-wasi-component-model.md`

**问题 #15** (第 789 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5z6dti2_WasiComponentOperator.java:77: 错误: 非法的表达式开始
                byte[] value = getRuntimeContext().getState(...).value();

- **错误行**: 77


### `Flink\03-api\09-language-foundations\datastream-api-cheatsheet.md`

**问题 #1** (第 38 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9i4liqdlTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9i4
- **错误行**: 3

**问题 #3** (第 83 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl8ghz138TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpl8g
- **错误行**: 3

**问题 #5** (第 128 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvm_obe13TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpvm_obe13TempValidat
- **错误行**: 4

**问题 #6** (第 152 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi88tym2qTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpi88
- **错误行**: 3

**问题 #7** (第 180 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3lzw9hi7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp3lz
- **错误行**: 3

**问题 #8** (第 226 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprj7ubw9oTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmprj7ubw9oTempValidat
- **错误行**: 4

**问题 #9** (第 261 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpass66bcfCountWithTimeout.java:1: 错误: 程序包org.apache.flink.streaming.api.functions不存在
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;

- **错误行**: 1

**问题 #10** (第 320 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8u__78xwTempValidation.java:4: 错误: 找不到符号
stream.print();                           // 输出到stdout
^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #11** (第 344 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4qjvp627TempValidation.java:4: 错误: 找不到符号
KafkaSink<String> sink = KafkaSink.<String>builder()
^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #12** (第 407 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplpfjuiycTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #13** (第 432 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsjyznwneTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpsjyznwneTempValidat
- **错误行**: 4

**问题 #14** (第 482 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4zgdf1zvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp4zgdf
- **错误行**: 3

**问题 #15** (第 514 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzcm5s4gqTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpzcm5s
- **错误行**: 3

**问题 #17** (第 632 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp877vfxq_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp877vf
- **错误行**: 3

**问题 #18** (第 652 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0coehta6TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp0coehta6TempValidat
- **错误行**: 4

**问题 #19** (第 725 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4_bz1y4wTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp4_bz1y4
- **错误行**: 3


### `Flink\03-api\09-language-foundations\flink-25-wasm-udf-ga.md`

**问题 #43** (第 2163 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpysy69tc0TempValidation.java:4: 错误: 找不到符号
WasmFunctionConfig optimalConfig = WasmFunctionConfig.builder()
^
  符号:   类 WasmFunctionConfig
  位置: 类 TempValidation
C:\U
- **错误行**: 4


### `Flink\03-api\09-language-foundations\flink-datastream-api-complete-guide.md`

**问题 #4** (第 184 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7z5fbp7wTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp7z5fbp7wTempValidat
- **错误行**: 4

**问题 #8** (第 284 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqn69k8jxTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpqn69k8jxTempValidat
- **错误行**: 4

**问题 #11** (第 406 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1z_r_2okTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1z_r_2okTempV
- **错误行**: 3

**问题 #14** (第 557 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgeyt3753TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpgey
- **错误行**: 3

**问题 #15** (第 578 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqw71tqrzTempValidation.java:8: 错误: 需要';'
public void onTimer(long timestamp, OnTimerContext ctx, Collector<Out> out) {
                   ^
C:\Users\luyan\AppData\
- **错误行**: 8

**问题 #17** (第 627 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv7giucn9CustomWatermarkGenerator.java:2: 错误: 需要 class、interface、enum 或 record
WatermarkStrategy.<Event>forMonotonousTimestamps()
^
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 2

**问题 #19** (第 675 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0_u77cl5TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp0_u
- **错误行**: 3

**问题 #21** (第 722 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp39aimn7hAsyncDatabaseRequest.java:51: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Result> asyncResult = AsyncDataStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 51

**问题 #23** (第 815 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo_3ed07eTempValidation.java:7: 错误: 找不到符号
timeout = 5_000;  // 5 seconds
^
  符号:   变量 timeout
  位置: 类 TempValidation
1 个错误

- **错误行**: 7

**问题 #28** (第 1031 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaf2dbmaxTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpaf2dbmaxTempValidat
- **错误行**: 4

**问题 #29** (第 1107 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmzjir83gTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpmzjir83gTempValidatio
- **错误行**: 4

**问题 #32** (第 1180 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqj4s1y9jTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpqj4s1y9jTempValidat
- **错误行**: 4

**问题 #33** (第 1260 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5wmzu87fTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.state.ValueState;
^
C:\Users\luyan\AppData\Local\Temp\tmp5wmzu87fTempValidation.java
- **错误行**: 4

**问题 #35** (第 1338 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo_9us0cmTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.state.ValueState;
^
C:\Users\luyan\AppData\Local\Temp\tmpo_9us0cmTempValidation.java
- **错误行**: 4

**问题 #36** (第 1361 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5jp2mbfhTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.state.ValueState;
^
C:\Users\luyan\AppData\Local\Temp\tmp5jp2mbfhTempValidation.java
- **错误行**: 4

**问题 #39** (第 1545 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp98kjl_o2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp98k
- **错误行**: 3

**问题 #41** (第 1599 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnk1ykme7TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpnk1ykme7TempValidat
- **错误行**: 4


### `Flink\03-api\09-language-foundations\flink-language-support-complete-guide.md`

**问题 #2** (第 196 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp58huo1toTempValidation.java:4: 错误: 需要';'
List<Integer> vs List<String> → 都是 List
                ^
C:\Users\luyan\AppData\Local\Temp\tmp58huo1toTempValidation.java
- **错误行**: 4

**问题 #6** (第 481 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp566_r7vrFlinkSpringConfig.java:3: 错误: 需要 class、interface、enum 或 record
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luy
- **错误行**: 3

**问题 #14** (第 1175 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppwzvac53JavaWithScalaUDF.java:27: 错误: 需要'{'
class ScalaMapFunction[T, R] extends RichMapFunction[T, R] {
                      ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 27


### `Flink\04-runtime\04.01-deployment\evolution\config-management.md`

**问题 #1** (第 48 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpix3xow1mTempValidation.java:3: 错误: 找不到符号
ConfigManager cm = ConfigManager.getInstance();
^
  符号:   类 ConfigManager
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 3


### `Flink\04-runtime\04.01-deployment\evolution\scheduling-evolution.md`

**问题 #2** (第 301 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9g153rruTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #3** (第 320 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeelt_a9kTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #4** (第 339 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpewnbkhg9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #5** (第 362 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpirpr9s10TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #6** (第 392 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwqqhs2czTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Flink\04-runtime\04.01-deployment\evolution\yarn-deploy.md`

**问题 #3** (第 58 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm8uklkp6TempValidation.java:3: 错误: 找不到符号
        env.getConfig().setAutoWatermarkInterval(200);
        ^
  符号:   变量 env
  位置: 类 TempValidation
1 个错误

- **错误行**: 3


### `Flink\04-runtime\04.01-deployment\flink-24-deployment-improvements.md`

**问题 #75** (第 2865 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    flink-conf-global.yaml: |
    ^ (line: 4)
found duplicate key "apiVersion" with value "flink.apache.org/v1beta1" (original v
- **错误行**: 4


### `Flink\04-runtime\04.01-deployment\flink-deployment-ops-complete-guide.md`

**问题 #16** (第 413 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 2:
     taskmanager.numberOfTaskSlots: 8
     ^ (line: 2)
found duplicate key "taskmanager.numberOfTaskSlots" with value "4" (origi
- **错误行**: 2

**问题 #17** (第 425 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    taskmanager.memory.network.min: 64mb
    ^ (line: 2)
found duplicate key "taskmanager.memory.network.min" with value "256mb"
- **错误行**: 2

**问题 #18** (第 437 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    execution.checkpointing.interval ...
    ^ (line: 2)
found duplicate key "execution.checkpointing.interval" with value "30s
- **错误行**: 2

**问题 #42** (第 1147 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplpb77fecTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmplpb
- **错误行**: 3


### `Flink\04-runtime\04.01-deployment\flink-k8s-operator-1.14-guide.md`

**问题 #7** (第 156 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxpme1q_7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpxpm
- **错误行**: 3

**问题 #29** (第 605 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkada24hoTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpkada24hoTempValidat
- **错误行**: 4

**问题 #44** (第 985 行, 语言: yaml)

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

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzsqv_0q7TempValidation.java:4: 错误: 找不到符号
while (running) {
       ^
  符号:   变量 running
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpzsqv_0q7TempVali
- **错误行**: 4


### `Flink\04-runtime\04.01-deployment\flink-serverless-architecture.md`

**问题 #6** (第 255 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0wgqbl52TempValidation.java:5: 错误: 需要';'
public Response handle(Request req) {
                      ^
C:\Users\luyan\AppData\Local\Temp\tmp0wgqbl52TempValidation.
- **错误行**: 5


### `Flink\04-runtime\04.01-deployment\multi-cloud-deployment-templates.md`

**问题 #10** (第 912 行, 语言: yaml)

- **错误**: could not determine a constructor for the tag '!Ref'
  in "<unicode string>", line 290, column 12:
        Value: !Ref FlinkApplication
               ^ (line: 290)
- **错误行**: 290

**问题 #21** (第 2453 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 23, column 52:
     ... aproc.logging.stackdriver.enable: 'true'
                                         ^ (line: 23)
- **错误行**: 23
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Flink\04-runtime\04.01-deployment\serverless-flink-ga-guide.md`

**问题 #10** (第 462 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    spec:
    ^ (line: 2)
found duplicate key "spec" with value "{}" (original value: "{}")
  in "<unicode string>", line 7, col
- **错误行**: 2

**问题 #11** (第 477 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend: hashmap  # 内存状态,重启丢失
    ^ (line: 2)
found duplicate key "state.backend" with value "forst" (original value:
- **错误行**: 2

**问题 #15** (第 775 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 98, column 22:
        resourceGroupName: "flink-serverless",
                         ^ (line: 98)
- **错误行**: 98
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Flink\04-runtime\04.03-observability\distributed-tracing.md`

**问题 #2** (第 88 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1sz6j9ihTempValidation.java:4: 错误: 不是语句
   traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
                  ^
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #8** (第 350 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxtrg0y_tTracingStreamOperator.java:2: 错误: 找不到符号
class TracingStreamOperator<OUT> extends AbstractStreamOperator<OUT> {
                                         ^

- **错误行**: 2


### `Flink\04-runtime\04.03-observability\evolution\alerting-evolution.md`

**问题 #2** (第 65 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkp4d95jdTempValidation.java:3: 错误: 找不到符号
        AlertManager.register(new AlertRule()
        ^
  符号:   变量 AlertManager
  位置: 类 TempValidation
C:\Users\luyan\AppD
- **错误行**: 3


### `Flink\04-runtime\04.03-observability\evolution\logging-evolution.md`

**问题 #2** (第 55 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkjj2i5bkTempValidation.java:3: 错误: 找不到符号
        LOG.info("Processing event",
        ^
  符号:   变量 LOG
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3


### `Flink\04-runtime\04.03-observability\evolution\metrics-evolution.md`

**问题 #2** (第 56 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzqjjm81kTempValidation.java:3: 错误: 找不到符号
        getRuntimeContext()
        ^
  符号:   方法 getRuntimeContext()
  位置: 类 TempValidation
1 个错误

- **错误行**: 3


### `Flink\04-runtime\04.03-observability\evolution\slo-evolution.md`

**问题 #2** (第 65 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7ac_r4z3TempValidation.java:3: 错误: 找不到符号
        double errorBudget = 1 - slo.getTarget();
                                 ^
  符号:   变量 slo
  位置: 类 TempValidation
- **错误行**: 3


### `Flink\04-runtime\04.03-observability\evolution\testing-evolution.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6gw3r8mgTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmp6g
- **错误行**: 4

**问题 #2** (第 74 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6_whhhixTempValidation.java:3: 错误: 找不到符号
        MiniCluster cluster = new MiniCluster(
        ^
  符号:   类 MiniCluster
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3


### `Flink\04-runtime\04.03-observability\evolution\tracing-evolution.md`

**问题 #2** (第 63 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz6jsviahTempValidation.java:3: 错误: 找不到符号
Span span = tracer.spanBuilder("process").startSpan();
^
  符号:   类 Span
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 3


### `Flink\04-runtime\04.03-observability\evolution\webui-evolution.md`

**问题 #1** (第 48 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpegx87cjwTempValidation.java:3: 错误: 非法的表达式开始
        GET /jobs/{jobid}/vertices
                  ^
C:\Users\luyan\AppData\Local\Temp\tmpegx87cjwTempValidation.java
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\04.04-cdc-debezium-integration.md`

**问题 #10** (第 581 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptpuyx2rsTempValidation.java:3: 错误: 非法的表达式开始
        import com.ververica.cdc.connectors.mysql.source.MySqlSource;
        ^
C:\Users\luyan\AppData\Local\Temp\tmptp
- **错误行**: 3

**问题 #15** (第 813 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查询数据湖(流读模式)
SET 'EXECUTION.RUNTIME-MODE' = 'STR...

**问题 #20** (第 1045 行, 语言: sql)

- **错误**: 可能的语法问题: -- MYSQL服务器配置(MY.CNF)
[MYSQLD]

# 必需:开启BINLOG

SERVE...

**问题 #24** (第 1143 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph9_3cjmbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmph9_3c
- **错误行**: 3

**问题 #25** (第 1171 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnj6r6jvjTempValidation.java:4: 错误: 找不到符号
MySqlSource<String> source = MySqlSource.<String>builder()
^
  符号:   类 MySqlSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4


### `Flink\05-ecosystem\05.01-connectors\cloudevents-integration-guide.md`

**问题 #7** (第 479 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6bzsbs0fSchemaRoutingFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<CloudEvent> events = env
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Local\
- **错误行**: 2

**问题 #9** (第 575 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphl09ugazTempValidation.java:3: 错误: 找不到符号
        LOG.info("Processing event",
        ^
  符号:   变量 LOG
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #10** (第 585 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjayhb22sTempValidation.java:3: 错误: 找不到符号
        meterRegistry.counter("events.processed",
        ^
  符号:   变量 meterRegistry
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 3

**问题 #15** (第 898 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9b7d98tyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9b7d98tyTemp
- **错误行**: 3

**问题 #20** (第 1429 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv9xycpgsAzureEventGridIntegration.java:3: 错误: 需要';'
import com.azure.core.models.CloudEvent as AzureCloudEvent;
                                       ^
1 个错误

- **错误行**: 3

**问题 #29** (第 2434 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpukklg1l7TempValidation.java:4: 错误: 找不到符号
if (aggregate.getVersion() % SNAPSHOT_INTERVAL == 0) {
    ^
  符号:   变量 aggregate
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #31** (第 2487 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl5c6y4h1TempValidation.java:5: 错误: 找不到符号
  ctx.timestamp() + sagaDefinition.getTimeoutMs()
  ^
  符号:   变量 ctx
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 5

**问题 #32** (第 2514 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_z97w88aTempValidation.java:4: 错误: 找不到符号
props.setProperty("batch.size", "16384");
^
  符号:   变量 props
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp_
- **错误行**: 4

**问题 #33** (第 2529 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpltwizhw9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpltwizhw
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\diskless-kafka-deep-dive.md`

**问题 #2** (第 106 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf0enencfTempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #3** (第 135 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8365uymvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #5** (第 233 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppuq3pj2qTempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\elasticsearch-connector-complete-guide.md`

**问题 #13** (第 172 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_th6ny8yTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp_th6ny8yTempValidat
- **错误行**: 4

**问题 #14** (第 189 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx2gj21z1TempValidation.java:4: 错误: 程序包ElasticsearchSink不存在
ElasticsearchSink.Builder<LogEvent> builder = new ElasticsearchSink.Builder<>(
                 ^
C:\Use
- **错误行**: 4

**问题 #16** (第 231 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkmqvdafgTempValidation.java:4: 错误: 找不到符号
builder.setFlushOnCheckpoint(true);
^
  符号:   变量 builder
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #20** (第 375 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7ytma1rzTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.http.auth.AuthScope;
^
C:\Users\luyan\AppData\Local\Temp\tmp7ytma1rzTempValidation.java:3: 错误: 不是语句
i
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\evolution\cdc-connector.md`

**问题 #1** (第 58 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvg47af7_TempValidation.java:3: 错误: 找不到符号
        MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
        ^
  符号:   类 MySqlSource
  位置: 类 TempValida
- **错误行**: 3

**问题 #2** (第 74 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp998nuw5uTempValidation.java:3: 错误: 找不到符号
stream.process(new ProcessFunction<String, Row>() {
                   ^
  符号:   类 ProcessFunction
  位置: 类 TempValidation

- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\evolution\cloud-connector.md`

**问题 #1** (第 56 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpio_6y6ymTempValidation.java:3: 错误: 找不到符号
        env.getConfig().setDefaultFileSystemScheme("s3://");
        ^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 3

**问题 #2** (第 68 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5neyb192TempValidation.java:3: 错误: 找不到符号
        FlinkKinesisConsumer<String> consumer = new FlinkKinesisConsumer<>(
        ^
  符号:   类 FlinkKinesisConsumer
  位置:
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\evolution\file-connector.md`

**问题 #1** (第 57 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp84nl0zpzTempValidation.java:3: 错误: 找不到符号
        FileSource<String> source = FileSource
        ^
  符号:   类 FileSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3

**问题 #2** (第 70 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpay993gahTempValidation.java:3: 错误: 找不到符号
        FileSink<GenericRecord> sink = FileSink
        ^
  符号:   类 FileSink
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\evolution\jdbc-connector.md`

**问题 #1** (第 56 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd3je_1tgTempValidation.java:3: 错误: 找不到符号
        JdbcSourceBuilder<Row> builder = JdbcSourceBuilder.<Row>builder()
        ^
  符号:   类 JdbcSourceBuilder
  位置: 类 Te
- **错误行**: 3

**问题 #2** (第 68 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp4bgv89mTempValidation.java:3: 错误: 找不到符号
JdbcSink.sink(
^
  符号:   变量 JdbcSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpp4bgv89mTempValidation.ja
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\evolution\kafka-connector.md`

**问题 #1** (第 55 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppmwlgtffTempValidation.java:3: 错误: 找不到符号
        KafkaSource<String> source = KafkaSource.<String>builder()
        ^
  符号:   类 KafkaSource
  位置: 类 TempValidation

- **错误行**: 3

**问题 #2** (第 69 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp49p9qq3pTempValidation.java:3: 错误: 找不到符号
        KafkaSink<String> sink = KafkaSink.<String>builder()
        ^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\evolution\lakehouse-connector.md`

**问题 #1** (第 60 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8depr9h6TempValidation.java:5: 错误: 找不到符号
    .withOverwritePartition(partition)
                            ^
  符号:   变量 partition
  位置: 类 TempValidation
C:\Users\
- **错误行**: 5


### `Flink\05-ecosystem\05.01-connectors\evolution\mq-connector.md`

**问题 #1** (第 57 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplgxfpbxeTempValidation.java:3: 错误: 找不到符号
        PulsarSource<String> source = PulsarSource.builder()
        ^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Us
- **错误行**: 3

**问题 #2** (第 72 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq4tqec9gTempValidation.java:3: 错误: 找不到符号
        RMQSink<String> sink = new RMQSink<>(
        ^
  符号:   类 RMQSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\evolution\nosql-connector.md`

**问题 #1** (第 58 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsyvtt2egTempValidation.java:3: 错误: 找不到符号
        HBaseSinkFunction<Row> sink = new HBaseSinkFunction<>(
        ^
  符号:   类 HBaseSinkFunction
  位置: 类 TempValidatio
- **错误行**: 3

**问题 #2** (第 71 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvfq3jqz2TempValidation.java:3: 错误: 找不到符号
        MongoDBSource<String> source = MongoDBSource.<String>builder()
        ^
  符号:   类 MongoDBSource
  位置: 类 TempValid
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\flink-24-connectors-guide.md`

**问题 #3** (第 151 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmycmw4mdTempValidation.java:3: 错误: 不是语句
        Kafka3Source<T> = ⟨BootstrapServers, TopicPattern, ConsumerProtocol,
                    ^
C:\Users\luyan\AppData\L
- **错误行**: 3

**问题 #13** (第 461 行, 语言: sql)

- **错误**: 可能的语法问题: -- 传统方式 (显式指定 JAR)
SET 'PIPELINE.JARS' = 'FILE:///...

**问题 #29** (第 1130 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkxsa259mTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpkxs
- **错误行**: 3

**问题 #30** (第 1157 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7ghpxd42TempValidation.java:4: 错误: 找不到符号
KafkaSink<String> sink = KafkaSink.<String>builder()
^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #35** (第 1323 行, 语言: sql)

- **错误**: 可能的语法问题: -- ICEBERG V2 流式增量读取
SET 'EXECUTION.RUNTIME-MODE' ...

**问题 #36** (第 1342 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG FLUSS_CATALOG;...

**问题 #39** (第 1486 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwmsdatloTempValidation.java:4: 错误: 找不到符号
TableResult result = tableEnv.executeSql(""
^
  符号:   类 TableResult
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #40** (第 1506 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7py00uo3TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp7py
- **错误行**: 3

**问题 #43** (第 1598 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 66, column 13:
          filter: id > 0
                ^ (line: 66)
- **错误行**: 66
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Flink\05-ecosystem\05.01-connectors\flink-cdc-3.6.0-guide.md`

**问题 #10** (第 421 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    transform:
    ^ (line: 2)
found duplicate key "transform" with value "[]" (original value: "[]")
  in "<unicode string>", l
- **错误行**: 2


### `Flink\05-ecosystem\05.01-connectors\flink-connectors-ecosystem-complete-guide.md`

**问题 #3** (第 154 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvahw4gvuSource.java:2: 错误: 找不到符号
    extends SourceReaderFactory<T, SplitT> {
            ^
  符号: 类 SourceReaderFactory
C:\Users\luyan\AppData\Local\Temp\tmpvahw4g
- **错误行**: 2

**问题 #4** (第 190 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf418bx0fSink.java:3: 错误: 找不到符号
    SinkWriter<InputT> createWriter(InitContext context);
                                    ^
  符号:   类 InitContext
  位置: 接口 Sink<
- **错误行**: 3

**问题 #22** (第 801 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6mc6owl6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp6mc
- **错误行**: 3

**问题 #23** (第 825 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsq_rf_6eTempValidation.java:4: 错误: 找不到符号
KafkaSink<String> sink = KafkaSink.<String>builder()
^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #25** (第 870 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo0ahpm44TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpo0a
- **错误行**: 3

**问题 #26** (第 895 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm3ramzx_TempValidation.java:4: 错误: 找不到符号
PulsarSink<String> sink = PulsarSink.builder()
^
  符号:   类 PulsarSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #28** (第 925 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfmzh_wigTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpfmz
- **错误行**: 3

**问题 #30** (第 974 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpze6vti1oTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpze6
- **错误行**: 3

**问题 #31** (第 1000 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphcrga99pTempValidation.java:4: 错误: 找不到符号
Properties producerConfig = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #33** (第 1037 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdqocj4rcTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpdqo
- **错误行**: 3

**问题 #35** (第 1080 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp929h46crTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp929
- **错误行**: 3

**问题 #36** (第 1133 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2j7s_tvqTempValidation.java:4: 错误: 找不到符号
FileSystem fs = FileSystem.get(new URI("s3://my-bucket/data"));
^
  符号:   类 FileSystem
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #37** (第 1153 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnrtf0f02TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnrt
- **错误行**: 3

**问题 #38** (第 1172 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7o_b0s4hTempValidation.java:4: 错误: 找不到符号
Schema schema = new Schema.Parser().parse(
^
  符号:   类 Schema
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #39** (第 1190 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppp5cucz_TempValidation.java:4: 错误: 找不到符号
final StreamingFileSink<Row> sink = StreamingFileSink
      ^
  符号:   类 StreamingFileSink
  位置: 类 TempValidation
C:\Users\
- **错误行**: 4

**问题 #40** (第 1211 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm9h096wjTempValidation.java:4: 错误: 找不到符号
FileSink<Row> sink = FileSink.forBulkFormat(
^
  符号:   类 FileSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #42** (第 1255 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp00m1cxpvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp00m
- **错误行**: 3

**问题 #43** (第 1279 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw7h8clfvTempValidation.java:4: 错误: 找不到符号
JdbcExactlyOnceSink<Row> sink = JdbcExactlyOnceSink.sink(
^
  符号:   类 JdbcExactlyOnceSink
  位置: 类 TempValidation
C:\Users\
- **错误行**: 4

**问题 #46** (第 1357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmakjffd_TempValidation.java:4: 错误: 找不到符号
ClusterBuilder clusterBuilder = new ClusterBuilder() {
^
  符号:   类 ClusterBuilder
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #48** (第 1397 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpttc5pq97TempValidation.java:4: 错误: 找不到符号
HBaseSourceFunction<Row> source = new HBaseSourceFunction<>(
^
  符号:   类 HBaseSourceFunction
  位置: 类 TempValidation
C:\Use
- **错误行**: 4

**问题 #50** (第 1439 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi4x_up19TempValidation.java:4: 错误: 找不到符号
List<HttpHost> httpHosts = Arrays.asList(
^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpi4x
- **错误行**: 4

**问题 #52** (第 1482 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkw15frczTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpkw1
- **错误行**: 3

**问题 #54** (第 1530 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_x_vgxpeTempValidation.java:4: 错误: 找不到符号
FlinkJedisPoolConfig conf = new FlinkJedisPoolConfig.Builder()
^
  符号:   类 FlinkJedisPoolConfig
  位置: 类 TempValidation
C:\
- **错误行**: 4

**问题 #56** (第 1582 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbotqhfs_TempValidation.java:4: 错误: 找不到符号
InfluxDBSink<String> sink = InfluxDBSink.builder()
^
  符号:   类 InfluxDBSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 4

**问题 #58** (第 1622 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp7l24cdfTempValidation.java:4: 错误: 找不到符号
CatalogLoader catalogLoader = CatalogLoader.hive(
^
  符号:   类 CatalogLoader
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 4

**问题 #59** (第 1639 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG ICEBERG_CATALOG;...

**问题 #60** (第 1675 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplyp6i9_6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmplyp
- **错误行**: 3

**问题 #64** (第 1752 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_CATALOG;...

**问题 #66** (第 1798 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1fzghl99TempValidation.java:4: 错误: 找不到符号
DeltaSink<Row> deltaSink = DeltaSink
^
  符号:   类 DeltaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp1fz
- **错误行**: 4

**问题 #68** (第 1828 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG FLUSS_CATALOG;...

**问题 #70** (第 1868 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_kbhrv7oTempValidation.java:4: 错误: 找不到符号
MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
^
  符号:   类 MySqlSource
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #79** (第 2329 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqjzclc2wTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqjzclc2
- **错误行**: 3

**问题 #80** (第 2348 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppzl0vej3TempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `Flink\05-ecosystem\05.01-connectors\flink-delta-lake-integration.md`

**问题 #11** (第 414 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5iwiq9joTempValidation.java:4: 错误: 非法的表达式开始
public void notifyCheckpointComplete(long checkpointId) {
^
C:\Users\luyan\AppData\Local\Temp\tmp5iwiq9joTempValidation
- **错误行**: 4

**问题 #16** (第 514 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm44tlg6eTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpm44
- **错误行**: 3

**问题 #17** (第 534 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2_vb2n__TempValidation.java:3: 错误: 找不到符号
        DeltaSource<RowData> streamingSource = DeltaSource
        ^
  符号:   类 DeltaSource
  位置: 类 TempValidation
C:\Users
- **错误行**: 3

**问题 #18** (第 550 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsfunp9vsTempValidation.java:3: 错误: 找不到符号
        DeltaSink<RowData> deltaSink = DeltaSink
        ^
  符号:   类 DeltaSink
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3

**问题 #19** (第 566 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc3d59wjqTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpc3d59wj
- **错误行**: 3

**问题 #21** (第 634 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3d5l8qonTempValidation.java:3: 错误: 找不到符号
        PostgresSource<String> pgSource = PostgresSource.<String>builder()
        ^
  符号:   类 PostgresSource
  位置: 类 Temp
- **错误行**: 3

**问题 #23** (第 673 行, 语言: sql)

- **错误**: 可能的语法问题: -- 流式查询
SET 'EXECUTION.RUNTIME-MODE' = 'STREAMING'...; 可能的语法问题: -- 批处理查询
SET 'EXECUTION.RUNTIME-MODE' = 'BATCH';...

**问题 #32** (第 832 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplwh3nhl6TempValidation.java:3: 错误: 找不到符号
        conf.set("delta.logRetentionDuration", "interval 30 days");
        ^
  符号:   变量 conf
  位置: 类 TempValidation
C:\Us
- **错误行**: 3


### `Flink\05-ecosystem\05.01-connectors\flink-elasticsearch-connector-guide.md`

**问题 #12** (第 322 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn5xzhzjuTempValidation.java:5: 错误: 不是语句
  "mappings": {
  ^
C:\Users\luyan\AppData\Local\Temp\tmpn5xzhzjuTempValidation.java:5: 错误: 需要';'
  "mappings": {

- **错误行**: 5

**问题 #17** (第 555 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1tbzd8j3TempValidation.java:40: 错误: 找不到符号
tableEnv.executeSql(createTableSQL);
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp1t
- **错误行**: 40

**问题 #19** (第 686 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd5v_o5r0TempValidation.java:4: 错误: 程序包ElasticsearchSink不存在
ElasticsearchSink.Builder<Event> builder =
                 ^
C:\Users\luyan\AppData\Local\Temp\tmpd5v_o
- **错误行**: 4

**问题 #24** (第 869 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3haf08dsTempValidation.java:4: 错误: 找不到符号
builder.setBulkFlushMaxActions(500);   // 从 1000 降低
^
  符号:   变量 builder
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #26** (第 903 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprq0wvzzqTempValidation.java:4: 错误: 找不到符号
String docId = event.getOrderId() + "_" + event.getTimestamp();
               ^
  符号:   变量 event
  位置: 类 TempValidation
C
- **错误行**: 4

**问题 #30** (第 975 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoep858bcTempValidation.java:4: 错误: 非法的表达式开始
public String sanitizeJson(Event event) {
^
C:\Users\luyan\AppData\Local\Temp\tmpoep858bcTempValidation.java:22: 错误: 需要
- **错误行**: 4

**问题 #32** (第 1056 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7ohbcntzTempValidation.java:4: 错误: 找不到符号
env.getConfig().enableObjectReuse();
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp7ohbcntz
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

**问题 #35** (第 1427 行, 语言: sql)

- **错误**: 可能的语法问题: -- 注意:分区演进是增量式的,历史数据保持原分区,新数据使用新分区策略...

**问题 #37** (第 1499 行, 语言: sql)

- **错误**: 可能的语法问题: -- 强制 COMPACTION(合并 DELETE 文件)
CALL ICEBERG_CATALO...

**问题 #43** (第 1751 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8o0kvq7hTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8o0kvq7
- **错误行**: 3

**问题 #45** (第 1801 行, 语言: sql)

- **错误**: 可能的语法问题: -- 重写数据文件(合并小文件)
CALL ICEBERG_CATALOG.SYSTEM.REWRI...; 可能的语法问题: -- 按分区压缩
CALL ICEBERG_CATALOG.SYSTEM.REWRITE_DATA_...

**问题 #47** (第 1863 行, 语言: sql)

- **错误**: 可能的语法问题: -- 手动触发过期
CALL ICEBERG_CATALOG.SYSTEM.EXPIRE_SNAPS...


### `Flink\05-ecosystem\05.01-connectors\flink-jdbc-connector-guide.md`

**问题 #14** (第 391 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqtf5j_wuTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.connector.jdbc.*;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqtf5j_wuTempValidation
- **错误行**: 3

**问题 #15** (第 436 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0l41xomyTempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql("""
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp0l41xomyTempVali
- **错误行**: 4

**问题 #17** (第 540 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6ndlxaxiTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp6ndlxax
- **错误行**: 3

**问题 #22** (第 690 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpys8jc1yhTempValidation.java:4: 错误: 找不到符号
config.setMaximumPoolSize(sinkParallelism + 5);
                          ^
  符号:   变量 sinkParallelism
  位置: 类 TempValidat
- **错误行**: 4

**问题 #24** (第 718 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj6o2nb7uTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpj6o
- **错误行**: 3

**问题 #26** (第 759 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppzacrfjyTempValidation.java:8: 错误: 需要';'
SET GLOBAL innodb_rollback_on_timeout = ON;
          ^
C:\Users\luyan\AppData\Local\Temp\tmppzacrfjyTempValidation.java:9
- **错误行**: 8

**问题 #29** (第 809 行, 语言: sql)

- **错误**: 可能的语法问题: -- MYSQL: 查看当前连接
SHOW PROCESSLIST;...; 可能的语法问题: -- 查看 XA 事务
XA RECOVER;...

**问题 #30** (第 845 行, 语言: sql)

- **错误**: 可能的语法问题: -- 启用二进制日志(CDC 必需)
SET GLOBAL BINLOG_FORMAT = 'ROW...; 可能的语法问题: -- 优化 INNODB
SET GLOBAL INNODB_BUFFER_POOL_SIZE = ...

**问题 #31** (第 858 行, 语言: sql)

- **错误**: 可能的语法问题: -- 优化写入性能
SET SYNCHRONOUS_COMMIT = OFF;...; 可能的语法问题: --  PREPARED TRANSACTIONS FOR XA
SET MAX_PREPARED_...


### `Flink\05-ecosystem\05.01-connectors\flink-mongodb-connector-guide.md`

**问题 #15** (第 357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplsegdbvvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmplse
- **错误行**: 3

**问题 #17** (第 406 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpws8z5qocTempValidation.java:4: 错误: 找不到符号
ReplaceOneModel<Document> replace = new ReplaceOneModel<>(
^
  符号:   类 ReplaceOneModel
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #25** (第 689 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppu31ft0kTempValidation.java:5: 错误: 找不到符号
tableEnv.executeSql("""
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmppu31ft0kTempVali
- **错误行**: 5

**问题 #33** (第 984 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp75zkrdqlTempValidation.java:4: 错误: 找不到符号
ReplaceOneModel<Document> replace = new ReplaceOneModel<>(
^
  符号:   类 ReplaceOneModel
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #35** (第 1021 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc3onj8ukTempValidation.java:4: 错误: 找不到符号
MongoClientSettings settings = MongoClientSettings.builder()
^
  符号:   类 MongoClientSettings
  位置: 类 TempValidation
C:\Use
- **错误行**: 4

**问题 #37** (第 1058 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp618v4os1MyClassCodec.java:23: 错误: 未命名类 是预览功能，默认情况下禁用。
CodecRegistry customCodecRegistry = CodecRegistries.fromCodecs(
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 23

**问题 #39** (第 1137 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv7df48e5TempValidation.java:4: 错误: 找不到符号
FindIterable<Document> iterable = collection
^
  符号:   类 FindIterable
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #40** (第 1159 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvidk8wnrTempValidation.java:4: 错误: 找不到符号
BulkWriteOptions options = new BulkWriteOptions()
^
  符号:   类 BulkWriteOptions
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #41** (第 1185 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwlnfxt0zTempValidation.java:4: 错误: 找不到符号
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

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpowegbmypTempValidation.java:4: 错误: 非法的表达式开始
.setProperty("useSSL", "false")
^
C:\Users\luyan\AppData\Local\Temp\tmpowegbmypTempValidation.java:14: 错误: 需要';'
.setPr
- **错误行**: 4

**问题 #17** (第 663 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8ltxqvjbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.connector.jdbc.source.JdbcSource;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8ltxqv
- **错误行**: 3

**问题 #18** (第 698 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7znplrx0TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.source.JdbcSource;
^
C:\Users\luyan\AppData\Local\Temp\tmp7znplrx0TempValidation
- **错误行**: 3

**问题 #19** (第 740 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjowlz6kkTempValidation.java:4: 错误: 找不到符号
JdbcSource<MyRecord> incrementalSource = JdbcSource.<MyRecord>builder()
^
  符号:   类 JdbcSource
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #20** (第 764 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp000hdp5jTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcSink;
^
C:\Users\luyan\AppData\Local\Temp\tmp000hdp5jTempValidation.java:3:
- **错误行**: 3

**问题 #21** (第 799 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5kbac7grTempValidation.java:29: 错误: 非法的表达式开始
);
^
1 个错误

- **错误行**: 29

**问题 #22** (第 831 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp14zcjsh3TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcExactlyOnceOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmp14zcjsh3TempValid
- **错误行**: 3

**问题 #23** (第 870 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpisrtl7k9TempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpis
- **错误行**: 4

**问题 #24** (第 892 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt81oa6txTempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpt8
- **错误行**: 4

**问题 #25** (第 911 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcdg872wjTempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpcd
- **错误行**: 4

**问题 #26** (第 931 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvjqaugh2TempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpvj
- **错误行**: 4

**问题 #27** (第 966 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpscvu4ny1TempValidation.java:4: 错误: 找不到符号
JdbcExecutionOptions executionOptions = JdbcExecutionOptions.builder()
^
  符号:   类 JdbcExecutionOptions
  位置: 类 TempValida
- **错误行**: 4

**问题 #29** (第 1026 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphp_qh02vTempValidation.java:10: 错误: 已在方法 main(String[])中定义了变量 url
String url = "jdbc:postgresql://localhost:5432/mydb" +
       ^
1 个错误

- **错误行**: 10

**问题 #30** (第 1056 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpblg063gdTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcExecutionOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmpblg063gdTempValidat
- **错误行**: 3

**问题 #31** (第 1104 行, 语言: sql)

- **错误**: 可能的语法问题: -- MYSQL: 查看当前连接
SHOW PROCESSLIST;...

**问题 #32** (第 1118 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy2z4v2auTempValidation.java:4: 错误: 找不到符号
HikariConfig config = new HikariConfig();
^
  符号:   类 HikariConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #33** (第 1149 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpavx98ehoTempValidation.java:9: 错误: 找不到符号
JdbcSource<MyRecord> source = JdbcSource.<MyRecord>builder()
^
  符号:   类 JdbcSource
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 9

**问题 #34** (第 1186 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfpgg4js2TempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);  // 1分钟,不要太短
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4


### `Flink\05-ecosystem\05.01-connectors\kafka-integration-patterns.md`

**问题 #1** (第 300 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpigss3wegTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #2** (第 328 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps6ulihr7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.connector.base.DeliveryGuarantee;
        ^
C:\Users\luyan\AppData\Local\Temp\tmps6ulih
- **错误行**: 3

**问题 #3** (第 350 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf6povct9TempValidation.java:4: 错误: 找不到符号
KafkaSource<UserEvent> source = KafkaSource.<UserEvent>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 4

**问题 #10** (第 721 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6rjq73y3TempValidation.java:4: 错误: 找不到符号
properties.setProperty(
^
  符号:   变量 properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp6rjq73y3TempVa
- **错误行**: 4


### `Flink\05-ecosystem\05.01-connectors\mongodb-connector-complete-guide.md`

**问题 #12** (第 725 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmple2sq806TempValidation.java:4: 错误: 找不到符号
MongoSink<Document> updateSink = MongoSink.<Document>builder()
^
  符号:   类 MongoSink
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4


### `Flink\05-ecosystem\05.01-connectors\pulsar-integration-guide.md`

**问题 #3** (第 205 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9l_zmkglTempValidation.java:4: 错误: 找不到符号
PulsarSource<String> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #4** (第 223 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0u7h1cunTempValidation.java:4: 错误: 找不到符号
PulsarSink<String> sink = PulsarSink.builder()
^
  符号:   类 PulsarSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #9** (第 366 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx0fxz9jbEnrichedStreamProcessing.java:18: 错误: 非法的表达式开始
            .setDeserializationSchema(...)
                                      ^
C:\Users\luyan\AppData\Lo
- **错误行**: 18

**问题 #10** (第 402 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5vtgb8_xTempValidation.java:4: 错误: 找不到符号
PulsarSource<String> optimizedSource = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #11** (第 440 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6iix6zz8SchemaEvolutionExample.java:24: 错误: 非法的表达式开始
        DataStream<EventV2> stream = env.fromSource(source, ...)

- **错误行**: 24


### `Flink\05-ecosystem\05.02-lakehouse\flink-iceberg-integration.md`

**问题 #29** (第 950 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG ICEBERG_CATALOG;...; 可能的语法问题: USE ECOMMERCE;...

**问题 #30** (第 1001 行, 语言: sql)

- **错误**: 可能的语法问题: -- 使用 UPSERT 模式处理 CDC 变更
SET 'EXECUTION.CHECKPOINT...

**问题 #31** (第 1062 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...

**问题 #36** (第 1477 行, 语言: sql)

- **错误**: 可能的语法问题: -- 在分支上写入数据(不影响主线)
SET 'ICEBERG.CATALOG.DEFAULT-BR...

**问题 #38** (第 1546 行, 语言: sql)

- **错误**: 可能的语法问题: -- 注意:分区演进是增量式的,历史数据保持原分区,新数据使用新分区策略...

**问题 #39** (第 1575 行, 语言: sql)

- **错误**: 可能的语法问题: -- 强制 COMPACTION(合并 DELETE 文件)
CALL ICEBERG_CATALO...

**问题 #46** (第 1875 行, 语言: sql)

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


### `Flink\05-ecosystem\05.02-lakehouse\streaming-lakehouse-architecture.md`

**问题 #25** (第 879 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG ICEBERG_CATALOG;...; 可能的语法问题: USE REALTIME_DW;...; 可能的语法问题: -- ============================================
--...

**问题 #26** (第 1040 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_CATALOG;...


### `Flink\05-ecosystem\05.02-lakehouse\streaming-lakehouse-deep-dive-2026.md`

**问题 #35** (第 1173 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_PROD;...; 可能的语法问题: USE ECOMMERCE;...; 可能的语法问题: -- ============================================
--...

**问题 #36** (第 1445 行, 语言: yaml)

- **错误**: while scanning a simple key
  in "<unicode string>", line 59, column 1:
    spark.sql.catalog.polaris=org.ap ...
    ^ (line: 59)
could not find expected ':'
  in "<unicode string>", line 60, column
- **错误行**: 59


### `Flink\05-ecosystem\05.03-wasm-udf\wasi-0.3-async-preview.md`

**问题 #26** (第 1197 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb9grv_07TempValidation.java:5: 错误: 需要';'
public void testCancellation() throws Exception {
                            ^
C:\Users\luyan\AppData\Local\Temp\tmpb9grv
- **错误行**: 5


### `Flink\05-ecosystem\05.04-graph\flink-gelly-streaming-graph-processing.md`

**问题 #3** (第 262 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8b0y9zi0TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp8b0y9zi0TempValidat
- **错误行**: 4

**问题 #4** (第 306 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2poc2n4mTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2po
- **错误行**: 3

**问题 #5** (第 345 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpemze3s14VertexState.java:14: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Edge<Long, Double>> edgeStream = ...;
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Lo
- **错误行**: 14

**问题 #6** (第 436 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphbwk8l75TempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend rocksDbBackend = new RocksDBStateBackend(
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempValidation
C:\Us
- **错误行**: 4


### `Flink\05-ecosystem\05.04-graph\flink-gelly.md`

**问题 #3** (第 166 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpde146qlrTempValidation.java:4: 错误: 找不到符号
Graph<Long, Double, Double> bipartiteGraph = Graph.fromDataSet(
^
  符号:   类 Graph
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #4** (第 197 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph02do_9zTempValidation.java:4: 错误: 非法的表达式开始
Graph<String, AccountInfo, Transaction> transactionGraph = ...;

- **错误行**: 4

**问题 #5** (第 218 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1l5juae_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1l5
- **错误行**: 3


### `Flink\05-ecosystem\ecosystem\kafka-streams-migration.md`

**问题 #2** (第 69 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqitco3w_TempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #3** (第 76 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz_448i2hTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #4** (第 101 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr5pfft_pTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpr5pfft_pTemp
- **错误行**: 3

**问题 #5** (第 126 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpldrrxiz0TempValidation.java:3: 错误: 找不到符号
        KStream<String, Integer> transformed = stream
        ^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3

**问题 #6** (第 136 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp8inxvwuTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpp8i
- **错误行**: 3

**问题 #7** (第 149 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplc2d1vzpTempValidation.java:3: 错误: 找不到符号
        Table transformed = tableEnv.from("input_table")
        ^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 3

**问题 #8** (第 165 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkxaz6ax6TempValidation.java:3: 错误: 找不到符号
        KTable<String, Long> counts = stream
        ^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 3

**问题 #9** (第 173 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpor9tgcubTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpor9tgcubTempValidat
- **错误行**: 4

**问题 #10** (第 214 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5370m9weTempValidation.java:3: 错误: 找不到符号
        KStream<String, String> joined = stream1.join(
        ^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 3

**问题 #11** (第 225 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpamue3y51TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpamu
- **错误行**: 3

**问题 #12** (第 240 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpni0n89rhTempValidation.java:3: 错误: 找不到符号
        Table joined = table1
        ^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpni0n89
- **错误行**: 3

**问题 #16** (第 330 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjg6rr801TempValidation.java:3: 错误: 找不到符号
        properties.put(StreamsConfig.NUM_STREAM_THREADS_CONFIG, 4);
                       ^
  符号:   变量 StreamsConfig
  位置
- **错误行**: 3

**问题 #17** (第 336 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbrpca9iwTempValidation.java:6: 错误: 非法的表达式开始
stream.map(...).setParallelism(2);
           ^
1 个错误

- **错误行**: 6

**问题 #18** (第 347 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp983yyr2TempValidation.java:3: 错误: 找不到符号
        properties.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG,
                       ^
  符号:   变量 StreamsConfig
  位置:
- **错误行**: 3

**问题 #19** (第 355 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkagl_3ftTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpkagl_3f
- **错误行**: 3

**问题 #20** (第 377 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0qg_t6o7TempValidation.java:4: 错误: 需要';'
public void testTopology() {
                        ^
C:\Users\luyan\AppData\Local\Temp\tmp0qg_t6o7TempValidation.java:8:
- **错误行**: 4

**问题 #21** (第 395 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpac2kcem0TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpac
- **错误行**: 4

**问题 #22** (第 422 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptiwmidtpTempValidation.java:4: 错误: 需要';'
public void testMigrationParity() {
                               ^
1 个错误

- **错误行**: 4


### `Flink\05-ecosystem\ecosystem\materialize-comparison.md`

**问题 #4** (第 110 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph65t_lp6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmph65
- **错误行**: 3

**问题 #5** (第 129 行, 语言: sql)

- **错误**: 可能的语法问题: -- AUTOMATIC MAINTENANCE, AUTOMATIC INDEXING...

**问题 #10** (第 314 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqc1lk22uTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqc1
- **错误行**: 3


### `Flink\05-ecosystem\ecosystem\pulsar-functions-integration.md`

**问题 #2** (第 73 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjp8m6_xkTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpjp8
- **错误行**: 3

**问题 #3** (第 100 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp85g6u751TempValidation.java:3: 错误: 找不到符号
        PulsarSink<String> sink = PulsarSink.builder()
        ^
  符号:   类 PulsarSink
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 3

**问题 #9** (第 236 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp65zjo0vtTempValidation.java:4: 错误: 找不到符号
Schema<OrderEvent> schema = Schema.AVRO(OrderEvent.class);
^
  符号:   类 Schema
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #10** (第 247 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpex0h3r2oTempValidation.java:4: 错误: 找不到符号
PulsarSource<OrderEvent> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #11** (第 264 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwszdlai7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwszdlai
- **错误行**: 3

**问题 #12** (第 281 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbvdsrqexTempValidation.java:4: 错误: 找不到符号
PulsarSource<String> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4


### `Flink\05-ecosystem\ecosystem\risingwave-integration-guide.md`

**问题 #2** (第 80 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1euruze9TempValidation.java:4: 错误: 找不到符号
JdbcSink.sink(
^
  符号:   变量 JdbcSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp1euruze9TempValidation.ja
- **错误行**: 4

**问题 #4** (第 124 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwcm9h81sTempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpwc
- **错误行**: 4

**问题 #8** (第 241 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqegmf8msTempValidation.java:4: 错误: 找不到符号
TwoPhaseCommitSinkFunction<Event, JdbcConnection, Void> exactlyOnceSink =
^
  符号:   类 TwoPhaseCommitSinkFunction
  位置: 类 T
- **错误行**: 4

**问题 #9** (第 278 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu8j2him8TempValidation.java:4: 错误: 找不到符号
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


### `Flink\05-ecosystem\flink-dynamic-iceberg-sink-guide.md`

**问题 #7** (第 954 行, 语言: yaml)

- **错误**: while scanning a simple key
  in "<unicode string>", line 3, column 1:
    -- 用于监控 Dynamic Iceberg Sink 作业健康度
    ^ (line: 3)
could not find expected ':'
  in "<unicode string>", line 4, column 1:

- **错误行**: 3


### `Flink\06-ai-ml\ai-agent-flink-deep-integration.md`

**问题 #7** (第 390 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprcdshz0nTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmprcdsh
- **错误行**: 3

**问题 #8** (第 409 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx8dnyrqoCustomerSupportAgent.java:350: 错误: 非法的表达式开始
            .addSource(new KafkaSource<Query>(...))
                                              ^
C:\Users\lu
- **错误行**: 350


### `Flink\06-ai-ml\ai-ml\evolution\a2a-protocol.md`

**问题 #1** (第 47 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo28goej2TempValidation.java:3: 错误: 找不到符号
        A2AMessage msg = A2AMessage.builder()
        ^
  符号:   类 A2AMessage
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 3

**问题 #2** (第 59 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxi8gkuucTempValidation.java:3: 错误: 找不到符号
        agent1.delegate(task, agent2);
                        ^
  符号:   变量 task
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 3


### `Flink\06-ai-ml\ai-ml\evolution\ai-agent-24.md`

**问题 #2** (第 49 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbrffi1ziTempValidation.java:3: 错误: 找不到符号
        Agent agent = Agent.newBuilder()
        ^
  符号:   类 Agent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 3

**问题 #3** (第 60 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpajueik_uTempValidation.java:4: 错误: 找不到符号
    .addSink(new ActionSink());
                 ^
  符号:   类 ActionSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4


### `Flink\06-ai-ml\ai-ml\evolution\ai-agent-25.md`

**问题 #1** (第 51 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnabc5ngsTempValidation.java:3: 错误: 找不到符号
        MultiAgentSystem system = MultiAgentSystem.builder()
        ^
  符号:   类 MultiAgentSystem
  位置: 类 TempValidation
C
- **错误行**: 3

**问题 #2** (第 62 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpktzalve5TempValidation.java:3: 错误: 找不到符号
system.coordinate(event, (detector, diagnoser) -> {
                  ^
  符号:   变量 event
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 3


### `Flink\06-ai-ml\ai-ml\evolution\ai-agent-30.md`

**问题 #3** (第 62 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplgd91vixTempValidation.java:4: 错误: 找不到符号
    .toSink(AlertSink.class);
            ^
  符号:   类 AlertSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4


### `Flink\06-ai-ml\ai-ml\evolution\feature-store.md`

**问题 #1** (第 46 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpah2yidjfTempValidation.java:3: 错误: 找不到符号
        FeatureVector fv = featureStore.getOnlineFeatures(entityId, features);
        ^
  符号:   类 FeatureVector
  位置: 类 T
- **错误行**: 3

**问题 #2** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph6_lqovnTempValidation.java:3: 错误: 找不到符号
stream.map(event -> {
^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmph6_lqovnTempValidati
- **错误行**: 3


### `Flink\06-ai-ml\ai-ml\evolution\llm-integration.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx2b5qicjTempValidation.java:3: 错误: 找不到符号
llmClient.completeStream(prompt, token -> {
                         ^
  符号:   变量 prompt
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 3

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0_3rssu7TempValidation.java:3: 错误: 找不到符号
        stream.map(new LLMMapFunction("gpt-4", promptTemplate));
                       ^
  符号:   类 LLMMapFunction
  位置: 类
- **错误行**: 3


### `Flink\06-ai-ml\ai-ml\evolution\ml-inference.md`

**问题 #1** (第 48 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1v6q9y1sTempValidation.java:3: 错误: 找不到符号
        SavedModelBundle model = SavedModelBundle.load("/path/to/model");
        ^
  符号:   类 SavedModelBundle
  位置: 类 Tem
- **错误行**: 3

**问题 #2** (第 57 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt8350qjvTempValidation.java:4: 错误: 找不到符号
    .setParallelism(gpuCount);
                    ^
  符号:   变量 gpuCount
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4


### `Flink\06-ai-ml\ai-ml\evolution\model-serving.md`

**问题 #2** (第 45 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg0lnyaanTempValidation.java:3: 错误: 找不到符号
        ModelRouter router = new ModelRouter()
        ^
  符号:   类 ModelRouter
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3

**问题 #3** (第 55 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7jqtmq5fTempValidation.java:3: 错误: 找不到符号
        ModelVersion version = registry.getLatest("fraud-detection");
        ^
  符号:   类 ModelVersion
  位置: 类 TempValidat
- **错误行**: 3


### `Flink\06-ai-ml\ai-ml\evolution\vector-search.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1d_ydlbhTempValidation.java:3: 错误: 找不到符号
        VectorIndex index = new HNSWIndex.Builder()
        ^
  符号:   类 VectorIndex
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 3

**问题 #2** (第 65 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl6okyhl3TempValidation.java:3: 错误: 找不到符号
        List<Vector> results = index.search(queryVector, 10);
        ^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 3


### `Flink\06-ai-ml\flink-22-data-ai-platform.md`

**问题 #2** (第 57 行, 语言: sql)

- **错误**: 可能的语法问题: -- 基本语法结构 (DEF-A-01-02A)
ML_PREDICT(
    MODEL_SPE...

**问题 #19** (第 1148 行, 语言: sql)

- **错误**: 可能的语法问题: -- 注册新模型版本
REGISTER MODEL 'RECOMMENDATION_MODEL@V3...; 可能的语法问题: -- 设置模型别名
SET MODEL ALIAS 'RECOMMENDATION_MODEL@ST...; 可能的语法问题: -- 全量发布:更新PRODUCTION别名
SET MODEL ALIAS 'RECOMMENDA...; 可能的语法问题:


### `Flink\06-ai-ml\flink-25-gpu-acceleration.md`

**问题 #7** (第 487 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprbskoat6TempValidation.java:5: 错误: 需要';'
public void testGPUSumAccuracy() {
                              ^
1 个错误

- **错误行**: 5


### `Flink\06-ai-ml\flink-agent-workflow-engine.md`

**问题 #10** (第 1118 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm5l0lr6mWorkflowBuilder.java:67: 错误: 未命名类 是预览功能，默认情况下禁用。
WorkflowDefinition workflow = WorkflowBuilder
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 67

**问题 #13** (第 1480 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa2vz_e_uTempValidation.java:4: 错误: 找不到符号
WorkflowDefinition riskWorkflow = WorkflowBuilder
^
  符号:   类 WorkflowDefinition
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4


### `Flink\06-ai-ml\flink-agents-flip-531.md`

**问题 #5** (第 464 行, 语言: sql)

- **错误**: 可能的语法问题: -- DEF-F-12-30: FLINK AGENT DDL 定义

-- 注: 以下为未来可能的...


### `Flink\06-ai-ml\flink-ai-agents-flip-531.md`

**问题 #6** (第 287 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy573w6ydBadAgent.java:1: 错误: 程序包org.apache.flink.api.common.state不存在
import org.apache.flink.api.common.state.ListState;
                                        ^

- **错误行**: 1

**问题 #7** (第 304 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph5gwbemwTempValidation.java:4: 错误: 找不到符号
String response = llmClient.completeSync(prompt);  // 阻塞！
                                         ^
  符号:   变量 prompt
  位
- **错误行**: 4

**问题 #8** (第 315 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6le_ktzaTempValidation.java:5: 错误: 找不到符号
    generateLLMRequest();  // 可能压垮服务！
    ^
  符号:   方法 generateLLMRequest()
  位置: 类 TempValidation
1 个错误

- **错误行**: 5

**问题 #11** (第 509 行, 语言: sql)

- **错误**: 可能的语法问题: -- 创建AGENT
-- 注: 以下为未来可能的语法(概念设计阶段)
<!-- 以下语法为概念设计...; 可能的语法问题: -- 注册SQL工具
-- 注: 以下为未来可能的语法(概念设计阶段)
<!-- 以下语法为概念设计...; 可能的语法问题: -- 注册外部工具
-- 注: 以下为未来可能的语法(概念设计阶段)
~~CREATE TOOL S...; 可能的语法问题:

**问题 #12** (第 577 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpznitsc90TempValidation.java:4: 错误: 找不到符号
Agent salesAgent = Agent.builder()
^
  符号:   类 Agent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpznitsc90T
- **错误行**: 4


### `Flink\06-ai-ml\flink-ai-ml-integration-complete-guide.md`

**问题 #5** (第 189 行, 语言: sql)
- **错误**: 可能的语法问题: -- DEF-F-12-104A: 相似度函数
COSINE_SIMILARITY(U, V) = ...

**问题 #6** (第 202 行, 语言: sql)
- **错误**: 可能的语法问题: -- 模型定义语法(DEF-F-12-105A)
<!-- 以下语法为概念设计,实际 FLINK 版...

**问题 #10** (第 375 行, 语言: sql)
- **错误**: 可能的语法问题: <!-- 以下语法为概念设计,实际 FLINK 版本尚未支持 -->
-- ~~CREATE AGE...; 可能的语法问题: -- DEF-F-12-110B: CREATE TOOL语法(未来可能的语法,概念设计阶段)
--...; 可能的语法问题: -- DEF-F-12-110C: AGENT工作流语法
<!-- 以下语法为概念设计,实际 FLI...

**问题 #14** (第 689 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5x26gidfBadAgent.java:1: 错误: 程序包org.apache.flink.api.common.state不存在
import org.apache.flink.api.common.state.ListState;
                                        ^

- **错误行**: 1

**问题 #15** (第 715 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgydg3zheTempValidation.java:4: 错误: 找不到符号
String response = llmClient.completeSync(prompt);  // 阻塞！吞吐量受限
                                         ^
  符号:   变量 promp
- **错误行**: 4

**问题 #16** (第 726 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi53dghqvTempValidation.java:5: 错误: 找不到符号
    generateLLMRequest();  // 可能压垮LLM服务！
    ^
  符号:   方法 generateLLMRequest()
  位置: 类 TempValidation
1 个错误

- **错误行**: 5

**问题 #21** (第 1345 行, 语言: sql)
- **错误**: 可能的语法问题: -- ============================================
--...; 可能的语法问题: -- 步骤2: 创建技术支持AGENT
-- 注: 以下为未来可能的语法(概念设计阶段)
~~CRE...; 可能的语法问题: -- 步骤3: 注册SQL工具 - 查询订单
-- 注: 以下为未来可能的语法(概念设计阶段)
<!...; 可能的语法问题:

**问题 #22** (第 1601 行, 语言: sql)
- **错误**: 可能的语法问题: -- 步骤3: 创建嵌入模型
<!-- 以下语法为概念设计,实际 FLINK 版本尚未支持 -->
...; 可能的语法问题: -- 步骤4: 创建LLM模型
~~CREATE MODEL RAG_GENERATOR~~ (未来...

**问题 #24** (第 2033 行, 语言: sql)

- **错误**: 可能的语法问题: -- 步骤4: 创建不同成本的模型定义
~~CREATE MODEL GPT35_ECONOMY~~...; 可能的语法问题: ~~CREATE MODEL GPT4_STANDARD~~ (未来可能的语法)
WITH (
  ...

**问题 #38** (第 3042 行, 语言: sql)

- **错误**: 可能的语法问题: -- 创建AGENT
-- 注: 以下为未来可能的语法(概念设计阶段)
<!-- 以下语法为概念设计...; 可能的语法问题: -- 创建模型
~~CREATE MODEL <NAME>~~ WITH ('PROVIDER' =...

**问题 #39** (第 3072 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5hzygh4yTempValidation.java:4: 错误: 找不到符号
Agent agent = Agent.builder()
^
  符号:   类 Agent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp5hzygh4yTempVa
- **错误行**: 4


### `Flink\06-ai-ml\flink-llm-integration.md`

**问题 #1** (第 35 行, 语言: sql)
- **错误**: 可能的语法问题: <!-- 以下语法为概念设计,实际 FLINK 版本尚未支持 -->
~~CREATE MODEL~...

**问题 #2** (第 56 行, 语言: sql)

- **错误**: 可能的语法问题: ML_PREDICT(
  MODEL_NAME,           -- 模型名称 (STRIN...

**问题 #6** (第 292 行, 语言: sql)

- **错误**: 可能的语法问题: -- DEF-F-12-41: MODEL DDL 实例

-- OPENAI GPT-4 模型
~...; 可能的语法问题: -- 文本嵌入模型
~~CREATE MODEL TEXT_EMBEDDING_3~~ (未来可能的...; 可能的语法问题: -- 兼容 OLLAMA 本地模型
~~CREATE MODEL LOCAL_LLAMA~~ (未来...

**问题 #9** (第 368 行, 语言: sql)

- **错误**: 可能的语法问题: -- 实时客服消息情感分析
~~CREATE MODEL SENTIMENT_ANALYZER~~ ...

**问题 #12** (第 435 行, 语言: sql)

- **错误**: 可能的语法问题: -- 实时多语言翻译
~~CREATE MODEL TRANSLATOR~~ (未来可能的语法)
W...

**问题 #16** (第 639 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpocgl8obuBatchLLMCaller.java:15: 错误: 未结束的字符文字
SET 'table.exec.async-lookup.buffer-capacity' = '100';
    ^
C:\Users\luyan\AppData\Local\Temp\tmpocgl8obuBatchLLMCall
- **错误行**: 15

**问题 #20** (第 732 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3ao74v6cPIIMaskingFunction.java:15: 错误: 需要 class、interface、enum 或 record
SELECT
^
C:\Users\luyan\AppData\Local\Temp\tmp3ao74v6cPIIMaskingFunction.java:18: 错误: 未结束的
- **错误行**: 15


### `Flink\06-ai-ml\flink-llm-realtime-inference-guide.md`

**问题 #6** (第 238 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf0bq5tqlTempValidation.java:4: 错误: 找不到符号
String response = llmClient.complete(prompt);  // 阻塞!
                                     ^
  符号:   变量 prompt
  位置: 类 Tem
- **错误行**: 4

**问题 #7** (第 244 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp703bp6ojTempValidation.java:4: 错误: 找不到符号
CompletableFuture<String> future = llmClient.completeAsync(prompt);
^
  符号:   类 CompletableFuture
  位置: 类 TempValidation
C
- **错误行**: 4

**问题 #8** (第 254 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfssc7ikyTempValidation.java:4: 错误: 非法的表达式开始
public void processElement(Request req) {
^
C:\Users\luyan\AppData\Local\Temp\tmpfssc7ikyTempValidation.java:9: 错误: 需要
- **错误行**: 4

**问题 #9** (第 261 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl95nk2b7TempValidation.java:4: 错误: 非法的表达式开始
private ListState<Message> conversationHistory;
^
C:\Users\luyan\AppData\Local\Temp\tmpl95nk2b7TempValidation.java:16:
- **错误行**: 4

**问题 #10** (第 277 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpme8_ujhiTempValidation.java:4: 错误: 找不到符号
String response = llmClient.complete(prompt);
                                     ^
  符号:   变量 prompt
  位置: 类 TempValidat
- **错误行**: 4

**问题 #11** (第 282 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfpt6f6cyTempValidation.java:4: 错误: 找不到符号
RetryPolicy<String> retryPolicy = RetryPolicy.<String>builder()
^
  符号:   类 RetryPolicy
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4


### `Flink\06-ai-ml\flink-llm-realtime-rag-architecture.md`

**问题 #6** (第 364 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp23vmhl8xRAGQueryService.java:67: 错误: 非法的表达式开始
            .map(new RichMapFunction<EnrichedQuery, LLMResponse>() {
            ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 67


### `Flink\06-ai-ml\flink-mcp-protocol-integration.md`

**问题 #8** (第 440 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps2cpvl7dTempValidation.java:4: 错误: 不是语句

1. 接收 MCP 调用请求 request = { name, arguments }
^
C:\Users\luyan\AppData\Local\Temp\tmps2cpvl7dTempValidation.java:4: 错误: 需要';

- **错误行**: 4

**问题 #15** (第 1156 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb421ccblMcpEnrichmentFunction.java:89: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedEvent> enrichedStream = rawStream
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\lu
- **错误行**: 89

**问题 #16** (第 1260 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8mtc_a3jMcpTableFunction.java:63: 错误: 未命名类 是预览功能，默认情况下禁用。
TableEnvironment tEnv = TableEnvironment.create(...);
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\
- **错误行**: 63

**问题 #27** (第 1820 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp03hp4yn2TempValidation.java:4: 错误: 找不到符号
String sql = "SELECT * FROM " + tableName + " WHERE id = " + userInput;
                                ^
  符号:   变量 table
- **错误行**: 4


### `Flink\06-ai-ml\flink-ml-architecture.md`

**问题 #3** (第 228 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe39rey8fTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Flink\06-ai-ml\flink-realtime-ml-inference.md`

**问题 #3** (第 298 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_dtpoh_wTempValidation.java:13: 错误: 非法的表达式开始
AsyncDataStream.unorderedWait(...);
                              ^
1 个错误

- **错误行**: 13

**问题 #5** (第 361 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxal5pqkaDriftDetectionFunction.java:11: 错误: 非法的表达式开始
        currentState.update(...);
                            ^
1 个错误

- **错误行**: 11

**问题 #7** (第 419 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4ntzsi0kTFServingAsyncFunction.java:54: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedEvent> scoredEvents = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以
- **错误行**: 54


### `Flink\06-ai-ml\flip-531-ai-agents-ga-guide.md`

**问题 #1** (第 92 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdpezfzdhTempValidation.java:4: 错误: 找不到符号
EmbeddingConfiguration embedConfig = EmbeddingConfiguration.builder()
^
  符号:   类 EmbeddingConfiguration
  位置: 类 TempValid
- **错误行**: 4

**问题 #4** (第 193 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcsyigysfTempValidation.java:4: 错误: 找不到符号
CompletableFuture<ToolResult> future = agent.executeToolAsync(
^
  符号:   类 CompletableFuture
  位置: 类 TempValidation
C:\Use
- **错误行**: 4


### `Flink\06-ai-ml\llm-streaming-inference-architecture.md`

**问题 #5** (第 369 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvy7uqsr_LLMInferenceAsyncFunction.java:92: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<String> prompts = ...;
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Loc
- **错误行**: 92


### `Flink\06-ai-ml\model-serving-streaming.md`

**问题 #3** (第 259 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgqf624zyTFServingAsyncFunction.java:47: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Prediction> predictions = featureStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 47


### `Flink\06-ai-ml\online-learning-algorithms.md`

**问题 #6** (第 495 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfd_0eqpyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.ml.classification.logisticregression;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpfd
- **错误行**: 3

**问题 #15** (第 960 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprrua6tggTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmprrua6tggTempValidatio
- **错误行**: 4


### `Flink\06-ai-ml\online-learning-production.md`

**问题 #3** (第 252 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwtt0x73uTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwtt
- **错误行**: 3


### `Flink\06-ai-ml\rag-streaming-architecture.md`

**问题 #3** (第 464 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9sz2xn2pStreamingRAGPipeline.java:85: 错误: 非法的表达式开始
                .setRecordSerializer(...)
                                     ^
C:\Users\luyan\AppData\Local\Te
- **错误行**: 85


### `Flink\06-ai-ml\realtime-feature-engineering-feature-store.md`

**问题 #11** (第 495 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeaj7uukzStreamFeatureJoin.java:15: 错误: 非法的表达式开始
            .addSource(new FlinkKafkaConsumer<>("clicks", ...));

- **错误行**: 15

**问题 #14** (第 714 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsvnvgygdRecommendationFeatureJob.java:15: 错误: 非法的表达式开始
            .addSource(new FlinkKafkaConsumer<>("user_events", ...));

- **错误行**: 15


### `Flink\06-ai-ml\realtime-feature-engineering-guide.md`

**问题 #2** (第 339 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjgd0o75aUserBehaviorAggregator.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<FeatureVector> features = events
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppDa
- **错误行**: 1

**问题 #3** (第 389 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpivhq2xyiSessionFeatureProcessFunction.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<SessionFeatures> sessionFeatures = events
^
  （请使用 --enable-preview 以启用 未命名类）
C:\U
- **错误行**: 1


### `Flink\06-ai-ml\streaming-rag-implementation-patterns.md`

**问题 #5** (第 798 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl7ubhb1yStreamingRAGJob.java:24: 错误: 非法的表达式开始
            new DebeziumSourceFunction<>(...)
                                         ^
C:\Users\luyan\AppData\Local
- **错误行**: 24


### `Flink\06-ai-ml\vector-database-integration.md`

**问题 #1** (第 26 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7_of7v0tVectorSink.java:2: 错误: 找不到符号
interface VectorSink<T> extends RichSinkFunction<T> {
                                ^
  符号: 类 RichSinkFunction
C:\Users\luya
- **错误行**: 2

**问题 #5** (第 266 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvjbsy294TempValidation.java:5: 错误: 找不到符号
List<VectorRecord> candidates = milvus.search(queryVector, topK=100);
^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 5

**问题 #8** (第 343 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprevfojjuTempValidation.java:4: 错误: 需要';'
CREATE TABLE vector_items (
            ^
C:\Users\luyan\AppData\Local\Temp\tmprevfojjuTempValidation.java:5: 错误: 需要')'或',
- **错误行**: 4

**问题 #11** (第 453 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgn1ajdmvMilvusLookupFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
TableResult result = tEnv.sqlQuery("""
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #13** (第 532 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp74w5191kTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp74w5191kTempValidat
- **错误行**: 4


### `Flink\07-roadmap\flink-23-formal-analysis.md`

**问题 #6** (第 627 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqmgdfor9StateBackend.java:6: 错误: 找不到符号
    <T> ValueState<T> getState(ValueStateDescriptor<T> descriptor);
                               ^
  符号:   类 ValueStateDes
- **错误行**: 6

**问题 #12** (第 1071 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    scheduler:
    ^ (line: 2)
found duplicate key "scheduler" with value "{}" (original value: "{}")
  in "<unicode string>", l
- **错误行**: 2

**问题 #17** (第 1576 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    jobmanager.scheduler: Adaptive
    ^ (line: 4)
found duplicate key "jobmanager.scheduler" with value "Adaptive" (original va
- **错误行**: 4


### `Flink\07-roadmap\flink-24-formal-prospects.md`

**问题 #16** (第 885 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6tfsy7fnTempValidation.java:3: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp6tfsy7fnTe
- **错误行**: 3


### `Flink\07-rust-native\ai-native-streaming\01-ai-native-architecture.md`

**问题 #8** (第 187 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprvi2as6yTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmprvi
- **错误行**: 3

**问题 #15** (第 403 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuffinfteTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpuff
- **错误行**: 3


### `Flink\07-rust-native\arroyo-update\01-arroyo-cloudflare-acquisition.md`

**问题 #26** (第 905 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp017s07q8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp017
- **错误行**: 3


### `Flink\07-rust-native\flash-engine\05-flink-compatibility.md`

**问题 #25** (第 551 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe3k0vetmTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpe3k
- **错误行**: 3


### `Flink\07-rust-native\heterogeneous-computing\01-gpu-udf-cuda.md`

**问题 #3** (第 356 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1uxinwgmSmallStateProcessor.java:1: 错误: 程序包org.apache.flink.streaming.api.functions不存在
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;

- **错误行**: 1


### `Flink\07-rust-native\heterogeneous-computing\04-unified-acceleration-api.md`

**问题 #10** (第 1140 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgygj7wmqUnifiedAccelExample.java:7: 错误: 非法的表达式开始
        TableEnvironment tEnv = TableEnvironment.create(...);

- **错误行**: 7


### `Flink\07-rust-native\iron-functions-complete-guide.md`

**问题 #17** (第 560 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxhcx6rz7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Te
- **错误行**: 3


### `Flink\07-rust-native\risingwave-comparison\01-risingwave-architecture.md`

**问题 #5** (第 350 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp3r3nyxdTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpp3r
- **错误行**: 3


### `Flink\07-rust-native\risingwave-comparison\02-nexmark-head-to-head.md`

**问题 #8** (第 416 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp41m7rdtyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp41m
- **错误行**: 3

**问题 #15** (第 609 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 3, column 12:
      resources:
               ^ (line: 3)
- **错误行**: 3
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Flink\07-rust-native\risingwave-comparison\03-migration-guide.md`

**问题 #9** (第 605 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfjuw8vo3NormalizeUdf.java:9: 错误: 需要 class、interface、enum 或 record
tableEnv.createTemporaryFunction("normalize", NormalizeUdf.class);
^
C:\Users\luyan\AppData\Local
- **错误行**: 9


### `Flink\07-rust-native\risingwave-comparison\04-hybrid-deployment.md`

**问题 #6** (第 499 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpabijz1hoTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpabi
- **错误行**: 3

**问题 #8** (第 561 行, 语言: sql)

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

**问题 #1** (第 44 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp14e4h2jnTempValidation.java:4: 错误: 找不到符号
VectorSpecies<Float> SPECIES = FloatVector.SPECIES_256;
^
  符号:   类 VectorSpecies
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #2** (第 136 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb6qigvgbTempValidation.java:4: 错误: 找不到符号
long address = unsafe.allocateMemory(size + 32);
                                     ^
  符号:   变量 size
  位置: 类 TempValida
- **错误行**: 4


### `Flink\07-rust-native\vectorized-udfs\01-vectorized-udf-intro.md`

**问题 #8** (第 985 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...


### `Flink\08-roadmap\08.01-flink-24\2026-q2-flink-tasks.md`

**问题 #13** (第 473 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0jmf2asrTempValidation.java:4: 错误: 找不到符号
for (KeyGroup kg : keyGroups) {
                   ^
  符号:   变量 keyGroups
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 4


### `Flink\08-roadmap\08.01-flink-24\community-dynamics-tracking.md`

**问题 #15** (第 424 行, 语言: yaml)

- **错误**: sequence entries are not allowed here
  in "<unicode string>", line 4, column 54:
     ... park to Flink: Lessons Learned" - 12K views
                                         ^ (line: 4)
- **错误行**: 4


### `Flink\08-roadmap\08.01-flink-24\flink-2.1-frontier-tracking.md`

**问题 #4** (第 412 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgsddha0bTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4


### `Flink\08-roadmap\08.01-flink-24\flink-2.3-2.4-roadmap.md`

**问题 #11** (第 314 行, 语言: yaml)

- **错误**: while parsing a block collection
  in "<unicode string>", line 9, column 7:
          - JOB_MANAGER_RPC_ADDRESS=jobmanager
          ^ (line: 9)
expected <block end>, but found '<scalar>'
  in "<unico
- **错误行**: 9


### `Flink\08-roadmap\08.01-flink-24\flink-2.4-tracking.md`

**问题 #12** (第 481 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_tfnrs8xTempValidation.java:6: 错误: 找不到符号
AgentCoordinator coordinator = new AgentCoordinator(env);  // [Flink 2.4 前瞻] 该API为规划特性,可能变动
^
  符号:   类 AgentCoordinator

- **错误行**: 6

**问题 #13** (第 522 行, 语言: sql)

- **错误**: 可能的语法问题: -- SQL API: 创建AI AGENT

-- 注册MCP工具(未来可能的语法,概念设计阶段)...; 可能的语法问题: -- 创建AGENT(未来可能的语法,概念设计阶段)
<!-- 以下语法为概念设计,实际 FLINK...; 可能的语法问题: -- 多AGENT协调查询(未来可能的语法,概念设计阶段)
~~CREATE AGENT_TEAM ...

**问题 #14** (第 566 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwnkp3iv0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #24** (第 981 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 2, column 4:
      S: Agent状态空间 (Memory + Context)
       ^ (line: 2)
- **错误行**: 2
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #28** (第 1126 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0lr8t64xAgent.java:15: 错误: 未命名类 是预览功能，默认情况下禁用。
AgentCoordinator coordinator = env.getAgentCoordinator();
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData
- **错误行**: 15

**问题 #34** (第 1398 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 2, column 7:
      V(t): 时变顶点集合
          ^ (line: 2)
- **错误行**: 2
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #35** (第 1422 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 18, column 5:
      支持: MATCH, WHERE, RETURN
        ^ (line: 18)
- **错误行**: 18
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #38** (第 1575 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpye9sh3hvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpye9sh
- **错误行**: 3

**问题 #43** (第 1769 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyyazxjkgTempValidation.java:4: 错误: 找不到符号
UnifiedSource<RowData> source = UnifiedSource.<RowData>builder()
^
  符号:   类 UnifiedSource
  位置: 类 TempValidation
C:\Users
- **错误行**: 4


### `Flink\08-roadmap\08.01-flink-24\flink-2.5-preview.md`

**问题 #1** (第 42 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 1, column 32:
    预计发布时间: 2026 Q3 (Feature Freeze: 2026-07, GA: 2026-09)
                                   ^ (line: 1)
- **错误行**: 1
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #3** (第 97 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 1, column 33:
    FLIP: FLIP-442 "Serverless Flink: Zero-to-Infinity Scaling"
                                    ^ (line: 1)
- **错误行**: 1
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #12** (第 432 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw88lrw2sTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #14** (第 515 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm81spxnkTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpm81spxnkTemp
- **错误行**: 3


### `Flink\08-roadmap\08.01-flink-24\flink-25-stream-batch-unification.md`

**问题 #15** (第 613 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphim9sgt9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #16** (第 656 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb1lwcathTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #19** (第 855 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1up4hzjnTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1up4hzjnTemp
- **错误行**: 3

**问题 #25** (第 1158 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv98n7rzhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #26** (第 1179 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpofo2thmuTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #29** (第 1247 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 5, column 31:
        配置: execution.runtime-mode: STREAMING
                                  ^ (line: 5)
- **错误行**: 5
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Flink\08-roadmap\08.01-flink-24\flink-30-architecture-redesign.md`

**问题 #3** (第 153 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdqksugjmExecutionMode.java:12: 错误: 不是语句
    if (stream.isUnbounded() && hints.latency < 100ms)
                                                   ^
C:\Users\luyan\
- **错误行**: 12

**问题 #5** (第 204 行, 语言: yaml)
- **错误**: while parsing a block collection
  in "<unicode string>", line 2, column 3:
      - HotData: L1 + L2 (95%+命中率,3.0目标)
      ^ (line: 2)
expected <block end>, but found '?'
  in "<unicode string>", line
- **错误行**: 2

**问题 #17** (第 566 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn0tf82w4TempValidation.java:3: 错误: 需要';'
ExecutionMode selectOptimalMode(DataCharacteristics data, QueryRequirements req) {
                               ^
C:\Use
- **错误行**: 3

**问题 #24** (第 773 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdw0yykebTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpdw
- **错误行**: 4


### `Flink\08-roadmap\08.01-flink-24\flink-version-evolution-complete-guide.md`

**问题 #12** (第 390 行, 语言: sql)
- **错误**: 可能的语法问题: -- 注册ML模型
<!-- 以下语法为概念设计,实际 FLINK 版本尚未支持 -->
~~CRE...

**问题 #30** (第 858 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4kmbzmhzTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp4kmbzmhzTempV
- **错误行**: 3

**问题 #31** (第 881 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp431a4_6hTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #32** (第 908 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8yvtjcx4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8yvtjcx4Temp
- **错误行**: 3


### `Flink\08-roadmap\08.02-flink-25\flink-25-features-preview.md`

**问题 #2** (第 38 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx1ja4nu7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpx1j
- **错误行**: 3

**问题 #7** (第 140 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl7vj0yazTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpl7v
- **错误行**: 3

**问题 #8** (第 160 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl6cnb_8xTempValidation.java:4: 错误: 找不到符号
InferenceConfig config = InferenceConfig.builder()
^
  符号:   类 InferenceConfig
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #14** (第 264 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp01177p2dTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp01177p2dTemp
- **错误行**: 3


### `Flink\08-roadmap\08.02-flink-25\flink-25-migration-guide.md`

**问题 #7** (第 135 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    execution.runtime-mode: adaptive ...
    ^ (line: 2)
found duplicate key "execution.runtime-mode" with value "streaming" (o
- **错误行**: 2

**问题 #8** (第 151 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprj2asz8wTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #9** (第 179 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpje8e8vedTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpje8e8vedTemp
- **错误行**: 3


### `Flink\08-roadmap\08.02-flink-25\flink-25-roadmap.md`

**问题 #1** (第 16 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 3, column 19:
      - Feature Freeze: 2026-07
                      ^ (line: 3)
- **错误行**: 3
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #2** (第 45 行, 语言: yaml)

- **错误**: while parsing a block collection
  in "<unicode string>", line 3, column 5:
        - 统一执行计划生成器
        ^ (line: 3)
expected <block end>, but found '?'
  in "<unicode string>", line 6, column 5:

- **错误行**: 3

**问题 #3** (第 80 行, 语言: yaml)

- **错误**: while parsing a block collection
  in "<unicode string>", line 3, column 5:
        - 无流量时资源释放至 0
        ^ (line: 3)
expected <block end>, but found '?'
  in "<unicode string>", line 6, column 5:

- **错误行**: 3

**问题 #4** (第 113 行, 语言: yaml)

- **错误**: while parsing a block collection
  in "<unicode string>", line 3, column 5:
        - 动态批处理
        ^ (line: 3)
expected <block end>, but found '?'
  in "<unicode string>", line 6, column 5:
        状
- **错误行**: 3


### `Flink\09-practices\09.01-case-studies\case-ecommerce-realtime-recommendation.md`

**问题 #19** (第 1847 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjnbb4v1yTempValidation.java:4: 错误: 非法的表达式开始
public UserProfile updateProfile(UserProfile current, BehaviorEvent event) {
^
C:\Users\luyan\AppData\Local\Temp\tmpjnb
- **错误行**: 4


### `Flink\09-practices\09.01-case-studies\case-financial-realtime-risk-control.md`

**问题 #6** (第 495 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph91p_jxsTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmph91
- **错误行**: 3

**问题 #7** (第 507 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzwam4fxdTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpzwam4
- **错误行**: 3

**问题 #10** (第 558 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfp53czcwTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpfp53czcwTempValidat
- **错误行**: 4

**问题 #11** (第 592 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbngmdlaaTempValidation.java:4: 错误: 找不到符号
LoadingCache<String, UserProfile> profileCache = Caffeine.newBuilder()
^
  符号:   类 LoadingCache
  位置: 类 TempValidation
C:\
- **错误行**: 4

**问题 #24** (第 1782 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnzabsg38TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnzabsg38Tem
- **错误行**: 3

**问题 #25** (第 1809 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwd_7pchfTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpwd_7pchfTempValidatio
- **错误行**: 4

**问题 #26** (第 1836 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptxpj4onxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmptxp
- **错误行**: 3

**问题 #29** (第 1895 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7jiq2fhlTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp7jiq2fhlTem
- **错误行**: 3

**问题 #30** (第 1913 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3eor5sq4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp3eo
- **错误行**: 3


### `Flink\09-practices\09.01-case-studies\case-gaming-realtime-analytics.md`

**问题 #8** (第 773 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppt6eug2eGamingAnalyticsJob.java:188: 错误: 需要'('或'['
                )
                ^
1 个错误

- **错误行**: 188


### `Flink\09-practices\09.01-case-studies\case-iot-stream-processing.md`

**问题 #3** (第 254 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphguxmhxzTempValidation.java:4: 错误: 找不到符号
    .<SensorEvent>forBoundedOutOfOrderness(Duration.ofSeconds(10))
      ^
  符号:   类 SensorEvent
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #5** (第 335 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyej9xi60TempValidation.java:4: 错误: 找不到符号
    .<SensorEvent>forBoundedOutOfOrderness(Duration.ofSeconds(10))
      ^
  符号:   类 SensorEvent
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #6** (第 362 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3biwi230TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp3biwi
- **错误行**: 3


### `Flink\09-practices\09.01-case-studies\case-realtime-analytics.md`

**问题 #11** (第 810 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbsvpdfvsTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpbs
- **错误行**: 4

**问题 #12** (第 852 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2p4onylkTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmp2p
- **错误行**: 4

**问题 #16** (第 1056 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn8ln60wvTempValidation.java:4: 错误: 非法的表达式开始
public int getPartition(String userId) {
^
C:\Users\luyan\AppData\Local\Temp\tmpn8ln60wvTempValidation.java:13: 错误: 需要
- **错误行**: 4

**问题 #17** (第 1089 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqo0jvpqkTempValidation.java:5: 错误: 需要';'
    .withIdleness(Duration.ofMinutes(1))  // 1分钟无数据视为空闲
                                        ^
1 个错误

- **错误行**: 5

**问题 #18** (第 1113 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfoaki4zaTempValidation.java:3: 错误: 非法的表达式开始
        .map(new ParseFunction())
        ^
C:\Users\luyan\AppData\Local\Temp\tmpfoaki4zaTempValidation.java:5: 错误: 需要'
- **错误行**: 3

**问题 #19** (第 1123 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqlw4_judTempValidation.java:3: 错误: 找不到符号
        StateTtlConfig ttlConfig = StateTtlConfig
        ^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 3

**问题 #20** (第 1136 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppmraj3y4TempValidation.java:4: 错误: 需要';'
public void snapshotState(FunctionSnapshotContext context) throws Exception {
                         ^
C:\Users\luyan\Ap
- **错误行**: 4


### `Flink\09-practices\09.01-case-studies\case-smart-grid-energy-management.md`

**问题 #7** (第 659 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpltqwupecTempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend rocksDbBackend = new RocksDBStateBackend(
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempValidation
C:\Us
- **错误行**: 4


### `Flink\09-practices\09.01-case-studies\case-smart-manufacturing-iot.md`

**问题 #5** (第 506 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdsn2___9TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpdsn2___9TempValidatio
- **错误行**: 4


### `Flink\09-practices\09.02-benchmarking\flink-24-25-benchmark-results.md`

**问题 #5** (第 384 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 7, column 3:
      RocksDB: 9.2.0
      ^ (line: 7)
found duplicate key "ForSt" with value "2.5.0-tiered (2.5)" (original value: "2.4.0-nativ
- **错误行**: 7


### `Flink\09-practices\09.02-benchmarking\performance-benchmark-suite.md`

**问题 #5** (第 475 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpobyyqthfTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpoby
- **错误行**: 3

**问题 #6** (第 489 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr77p7_o6TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpr77p7_o6TempValidat
- **错误行**: 4

**问题 #7** (第 524 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe_17c1rlTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpe_17c1rlTempValidat
- **错误行**: 4

**问题 #19** (第 1484 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 222


### `Flink\09-practices\09.02-benchmarking\performance-benchmarking-guide.md`

**问题 #6** (第 251 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptwgn83obTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmptwg
- **错误行**: 3

**问题 #7** (第 299 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0rkzgu6zTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp0rk
- **错误行**: 3

**问题 #9** (第 361 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2lpt26wjTempValidation.java:4: 错误: 找不到符号
MetricGroup metricGroup = getRuntimeContext()
^
  符号:   类 MetricGroup
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #18** (第 607 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4vignxboTempValidation.java:5: 错误: 非法的表达式开始
    .window(...)  // 第一阶段
            ^
C:\Users\luyan\AppData\Local\Temp\tmp4vignxboTempValidation.java:8: 错误: 非法的表达式开
- **错误行**: 5

**问题 #19** (第 619 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxci0gn8jTempValidation.java:4: 错误: 找不到符号
stream.map(event -> {
^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpxci0gn8jTempValidati
- **错误行**: 4


### `Flink\09-practices\09.02-benchmarking\streaming-benchmarks.md`

**问题 #4** (第 295 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqbquwyxhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Flink\09-practices\09.03-performance-tuning\05-vs-competitors\flink-vs-kafka-streams.md`

**问题 #10** (第 323 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp14r7jhmzTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp14r7j
- **错误行**: 3

**问题 #11** (第 349 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1qg16mnpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1qg
- **错误行**: 3

**问题 #12** (第 364 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpavhlv9caTempValidation.java:4: 错误: 找不到符号
WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ofSeconds(30))
                   ^
  符号:   类 Event
  位置: 类 Tem
- **错误行**: 4

**问题 #17** (第 528 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm8hvr162TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.typeinfo.Types;
^
C:\Users\luyan\AppData\Local\Temp\tmpm8hvr162TempValidation.java:4
- **错误行**: 4

**问题 #18** (第 581 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbnlkp6fpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpbnl
- **错误行**: 3

**问题 #24** (第 1004 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmwu1kt9pTempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #25** (第 1022 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnyrrm_e9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Flink\09-practices\09.03-performance-tuning\05-vs-competitors\flink-vs-risingwave-deep-dive.md`

**问题 #7** (第 319 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzxr7ejruTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpzxr
- **错误行**: 3


### `Flink\09-practices\09.03-performance-tuning\05-vs-competitors\linkedin-samza-deep-dive.md`

**问题 #8** (第 332 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpde7tif__WordCountTask.java:24: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Tuple2<String, Integer>> wordCounts =
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 24

**问题 #10** (第 415 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp13ot730zTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp13o
- **错误行**: 3

**问题 #11** (第 431 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfd5qo9pcTempValidation.java:8: 错误: 非法的表达式开始
public void processActivity(MemberEvent event, MessageCollector collector) {
^
C:\Users\luyan\AppData\Local\Temp\tmpfd5
- **错误行**: 8

**问题 #12** (第 448 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7mhnp7edTempValidation.java:3: 错误: 找不到符号
        Table memberProfile = tableEnv.fromDataStream(profileStream)
        ^
  符号:   类 Table
  位置: 类 TempValidation
C:\U
- **错误行**: 3


### `Flink\09-practices\09.03-performance-tuning\06.02-performance-optimization-complete.md`

**问题 #4** (第 451 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6d613i8tTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #7** (第 564 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjzq4j96zTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpjzq
- **错误行**: 3

**问题 #8** (第 607 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz7xmsnv8Order.java:2: 错误: 需要 class、interface、enum 或 record
env.getConfig().registerTypeWithKryoSerializer(
^
C:\Users\luyan\AppData\Local\Temp\tmpz7xmsnv8Order.jav
- **错误行**: 2

**问题 #11** (第 730 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc08g95udTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpc08
- **错误行**: 3

**问题 #12** (第 776 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看执行计划
EXPLAIN SELECT
    USER_ID,
    COUNT(*)...; 可能的语法问题: -- 使用EXPLAIN ESTIMATED_COST查看代价估算
EXPLAIN ESTIMATE...

**问题 #16** (第 904 行, 语言: sql)

- **错误**: 可能的语法问题: -- 动态分区裁剪
SET TABLE.OPTIMIZER.DYNAMIC-FILTERING.EN...

**问题 #22** (第 1141 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxxaa_qe_TempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<Event> kafkaSource = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #23** (第 1200 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu_6diixsAsyncUserLookup.java:41: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedEvent> enriched = AsyncDataStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 41

**问题 #25** (第 1297 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk9y7np42TempValidation.java:4: 错误: 找不到符号
HikariConfig config = new HikariConfig();
^
  符号:   类 HikariConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #27** (第 1377 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2i8ui181TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2i8
- **错误行**: 3

**问题 #29** (第 1437 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsv90c2_xFraudResultSink.java:36: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<FraudResult> results = AsyncDataStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 36

**问题 #31** (第 1522 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3rtliexqTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp3rtliexqTempValidat
- **错误行**: 4


### `Flink\09-practices\09.03-performance-tuning\flink-24-performance-improvements.md`

**问题 #7** (第 473 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsfi8z9btUserEvent.java:13: 错误: 未命名类 是预览功能，默认情况下禁用。
ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();
^
  （请使用 --enable-preview 以启用 未命名类）
C
- **错误行**: 13

**问题 #10** (第 550 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppfxwb7llTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.CheckpointingMode;
^
C:\Users\luyan\AppData\Local\Temp\tmppfxwb7llTempValidation.
- **错误行**: 4

**问题 #11** (第 585 行, 语言: sql)

- **错误**: 可能的语法问题: -- 启用向量化执行
SET TABLE.EXEC.MINI-BATCH.ENABLED = TRU...; 可能的语法问题: -- 启用自适应JOIN
SET TABLE.OPTIMIZER.ADAPTIVE-JOIN.ENA...; 可能的语法问题: -- 启用谓词下推
SET TABLE.OPTIMIZER.PREDICATE-PUSHDOWN.E...; 可能的语法问题:

**问题 #13** (第 630 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgcckdo3sTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpgcckdo3sTemp
- **错误行**: 3


### `Flink\09-practices\09.03-performance-tuning\flink-tco-cost-optimization-guide.md`

**问题 #5** (第 791 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6u5m6oz8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Flink\09-practices\09.03-performance-tuning\performance-tuning-guide.md`

**问题 #3** (第 297 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp31jnlukiTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp31j
- **错误行**: 3

**问题 #4** (第 318 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    execution.checkpointing.unaligne ...
    ^ (line: 2)
found duplicate key "execution.checkpointing.interval" with value "600
- **错误行**: 2

**问题 #6** (第 364 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpheseesyeTempValidation.java:3: 错误: 找不到符号
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        ^
  符号:   类 StreamE
- **错误行**: 3

**问题 #7** (第 377 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq9lo8fzrTempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4


### `Flink\09-practices\09.03-performance-tuning\state-backend-selection.md`

**问题 #1** (第 337 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7ivrcynqTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #2** (第 363 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4zq1hagqTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend backend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #3** (第 384 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa9nl7tl5TempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend backend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #5** (第 425 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3vnfcr8kTempValidation.java:3: 错误: 找不到符号
        conf.setString("taskmanager.memory.managed.size", "64mb");  // 过小！
        ^
  符号:   变量 conf
  位置: 类 TempValidatio
- **错误行**: 3

**问题 #6** (第 433 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpepu1er3aTempValidation.java:3: 错误: 找不到符号
        conf.setString("taskmanager.memory.managed.fraction", "0.4");
        ^
  符号:   变量 conf
  位置: 类 TempValidation
C:\
- **错误行**: 3


### `Flink\09-practices\09.03-performance-tuning\stream-processing-cost-optimization.md`

**问题 #4** (第 318 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp03tb5a8_TempValidation.java:6: 错误: 找不到符号
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
  in "<unicode string>", line 10, co
- **错误行**: 2

**问题 #19** (第 1118 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6pts5crcTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Flink\09-practices\09.03-performance-tuning\stream-processing-testing-strategies.md`

**问题 #3** (第 196 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxlx8aiaaTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #4** (第 234 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1w7ksnl9TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.typeinfo.Types;
^
C:\Users\luyan\AppData\Local\Temp\tmp1w7ksnl9TempValidation.java:4
- **错误行**: 4

**问题 #5** (第 268 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbdqevig7TempValidation.java:8: 错误: 需要';'
public void testEnrichmentOperatorWithMock() throws Exception {
                                          ^
C:\Users\luyan
- **错误行**: 8

**问题 #6** (第 305 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4r6k9x06TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmp4r
- **错误行**: 4

**问题 #7** (第 357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpku1ye_4gTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpku
- **错误行**: 4

**问题 #8** (第 401 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeq6bpasyTempValidation.java:4: 错误: 需要';'
public void testCheckpointRecovery() throws Exception {
                                  ^
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #9** (第 453 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphkguih56TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmphk
- **错误行**: 4

**问题 #11** (第 549 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp34wrzkoqTempValidation.java:4: 错误: 需要';'
public void testFailureRecovery() throws Exception {
                               ^
C:\Users\luyan\AppData\Local\Temp\tm
- **错误行**: 4

**问题 #13** (第 666 行, 语言: java)

- **错误**: 括号不匹配: (=80, )=84


### `Flink\09-practices\09.03-performance-tuning\troubleshooting-handbook.md`

**问题 #16** (第 476 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaat7zci7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpaat7zci7Tem
- **错误行**: 3

**问题 #26** (第 606 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsbtsx_caTempValidation.java:4: 错误: 找不到符号
    .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(30))
      ^
  符号:   类 Event
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4

**问题 #28** (第 622 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk6df6nljTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpk6d
- **错误行**: 3

**问题 #29** (第 640 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp04fy557mTempValidation.java:4: 错误: 找不到符号
WatermarkStrategy.<Event>forBoundedOutOfOrderness(
                   ^
  符号:   类 Event
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #32** (第 680 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcnle_sd1TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpcnle_sd1Tem
- **错误行**: 3

**问题 #37** (第 749 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    restart-strategy: fixed-delay
    ^ (line: 2)
found duplicate key "restart-strategy" with value "exponential-delay" (origina
- **错误行**: 2

**问题 #39** (第 773 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwhrn7q70TempValidation.java:5: 错误: 找不到符号
    externalService.call();
    ^
  符号:   变量 externalService
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpw
- **错误行**: 5


### `Flink\09-practices\09.04-deployment\flink-k8s-operator-migration-1.13-to-1.14.md`

**问题 #18** (第 557 行, 语言: yaml)

- **错误**: while scanning a block scalar
  in "<unicode string>", line 6, column 22:
        - Reconcile 成功率: > 99%
                         ^ (line: 6)
expected a comment or a line break, but found '9'
  in "<u
- **错误行**: 6


### `Flink\09-practices\09.04-deployment\flink-kubernetes-operator-1.14-guide.md`

**问题 #11** (第 299 行, 语言: yaml)

- **错误**: while scanning a simple key
  in "<unicode string>", line 9, column 1:
    {
    ^ (line: 9)
could not find expected ':'
  in "<unicode string>", line 10, column 3:
      "$schema": "<http://json-schem>
- **错误行**: 9

**问题 #22** (第 699 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    spec:
    ^ (line: 2)
found duplicate key "spec" with value "{}" (original value: "{}")
  in "<unicode string>", line 10, co
- **错误行**: 2

**问题 #35** (第 1674 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 24, column 1:
    apiVersion: kustomize.config.k8s ...
    ^ (line: 24)
found duplicate key "apiVersion" with value "flink.apache.org/v1beta
- **错误行**: 24


### `Flink\09-practices\09.04-security\flink-24-security-enhancements.md`

**问题 #13** (第 391 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzxlidiksTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpzxl
- **错误行**: 3


### `Flink\09-practices\09.04-security\flink-security-complete-guide.md`

**问题 #8** (第 503 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp53lfxe7bTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
^
C:\Users\luyan\AppData\Local\Temp\tmp53lfxe7bT
- **错误行**: 4


### `Flink\09-practices\09.04-security\security-hardening-guide.md`

**问题 #15** (第 546 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy3oiuyhgEncryptedRocksDBStateBackend.java:29: 错误: 非法的表达式开始
            super.createKeyedStateBackend(...),
                                          ^
C:\Users\luy
- **错误行**: 29

**问题 #16** (第 586 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    state.backend: rocksdb
    ^ (line: 4)
found duplicate key "s3.server-side-encryption" with value "aws:kms" (original value:
- **错误行**: 4

**问题 #18** (第 623 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplimtsfelTempValidation.java:4: 错误: 找不到符号
Properties kafkaProps = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #19** (第 644 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph9wz5p64TempValidation.java:10: 错误: 找不到符号
JDBCInputFormat jdbcInput = JDBCInputFormat.buildJDBCInputFormat()
^
  符号:   类 JDBCInputFormat
  位置: 类 TempValidation
C:\
- **错误行**: 10

**问题 #20** (第 665 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgcci0xoyTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.runtime.state.encryption.EncryptionOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmpgcci0xoyTemp
- **错误行**: 3

**问题 #26** (第 864 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp96zczvkbRowLevelSecurityFilter.java:24: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Event> securedStream = rawStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 24


### `Flink\09-practices\09.04-security\security\evolution\audit-evolution.md`

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpox5h9r7zTempValidation.java:3: 错误: 找不到符号
        auditLog.record(new AuditEvent()
        ^
  符号:   变量 auditLog
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 3


### `Flink\09-practices\09.04-security\security\evolution\auth-evolution.md`

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8uv10rk1TempValidation.java:3: 错误: 找不到符号
        OAuth2Client client = new OAuth2Client()
        ^
  符号:   类 OAuth2Client
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3


### `Flink\09-practices\09.04-security\security\evolution\authorization-evolution.md`

**问题 #2** (第 67 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiouc5cq8TempValidation.java:3: 错误: 找不到符号
if (authorizer.hasPermission(user, "jobs:cancel", jobId)) {
                             ^
  符号:   变量 user
  位置: 类 TempVal
- **错误行**: 3


### `Flink\09-practices\09.04-security\security\evolution\compliance-evolution.md`

**问题 #2** (第 69 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpydsy0attTempValidation.java:4: 错误: 此处不允许使用修饰符private
private String ssn;
               ^
C:\Users\luyan\AppData\Local\Temp\tmpydsy0attTempValidation.java:3: 错误: 找
- **错误行**: 4


### `Flink\09-practices\09.04-security\security\evolution\data-governance-evolution.md`

**问题 #1** (第 55 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzwjtre90TempValidation.java:3: 错误: 找不到符号
        LineageRecorder.record(new DataLineage()
        ^
  符号:   变量 LineageRecorder
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 3


### `Flink\09-practices\09.04-security\security\evolution\encryption-evolution.md`

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsgrai1j3TempValidation.java:3: 错误: 找不到符号
        KeyVault vault = KeyVault.create(config);
        ^
  符号:   类 KeyVault
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3


### `Flink\09-practices\09.04-security\security\evolution\key-management-evolution.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6jibtuzcTempValidation.java:3: 错误: 找不到符号
        Vault vault = Vault.builder()
        ^
  符号:   类 Vault
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 3


### `Flink\09-practices\09.04-security\security\evolution\lineage-evolution.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2p8sm5juTempValidation.java:3: 错误: 找不到符号
        LineageContext ctx = LineageContext.current();
        ^
  符号:   类 LineageContext
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3


### `Flink\09-practices\09.04-security\security\evolution\tee-evolution.md`

**问题 #1** (第 58 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3hzwdm51TempValidation.java:3: 错误: 找不到符号
        Enclave enclave = EnclaveLoader.load("enclave.so");
        ^
  符号:   类 Enclave
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3

**问题 #2** (第 67 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvrrztn5kTempValidation.java:4: 错误: 找不到符号
EnclaveResult result = teeExecutor.execute(() -> {
^
  符号:   类 EnclaveResult
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4


### `Flink\09-practices\09.04-security\spiffe-spire-integration-guide.md`

**问题 #14** (第 715 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvqlidlunTempValidation.java:4: 错误: 找不到符号
Properties kafkaProps = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #15** (第 750 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4qkxtz9gTempValidation.java:4: 错误: 找不到符号
RestClientBuilder builder = RestClient.builder(
^
  符号:   类 RestClientBuilder
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4


### `Flink\09-practices\09.04-security\streaming-security-best-practices.md`

**问题 #4** (第 209 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 9, column 1:
    ssl.keystore.location=/etc/kafka ...
    ^ (line: 9)
- **错误行**: 9

**问题 #8** (第 327 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf7k7au5zTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpf7k7au5
- **错误行**: 3


### `Flink\09-practices\09.05-edge\flink-edge-ai-optimization.md`

**问题 #8** (第 534 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw3v8knzjModelInferenceWithBroadcast.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<ModelUpdate> modelUpdates = env
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2


### `Flink\09-practices\09.05-edge\flink-edge-resource-optimization.md`

**问题 #2** (第 275 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpba28w270TempValidation.java:6: 错误: 找不到符号
env.setParallelism(optimalParallelism);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpba28w
- **错误行**: 6

**问题 #3** (第 287 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeerq3jh2TempValidation.java:5: 错误: 非法的表达式开始
    .filter(...)
            ^
C:\Users\luyan\AppData\Local\Temp\tmpeerq3jh2TempValidation.java:6: 错误: 非法的表达式开始
    .ma
- **错误行**: 5

**问题 #4** (第 305 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt3xtwrf7TempValidation.java:5: 错误: 找不到符号
    inputStream,
    ^
  符号:   变量 inputStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpt3xtwrf7TempVali
- **错误行**: 5


### `Flink\09-practices\09.05-edge\flink-edge-streaming-guide.md`

**问题 #3** (第 300 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4gd25vggTempValidation.java:8: 错误: 找不到符号
    .filter(nonNullFilter);
            ^
  符号:   变量 nonNullFilter
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 8

**问题 #4** (第 317 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_flbg1obTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp_flbg
- **错误行**: 3


### `Flink\09-practices\09.06-debugging\source-code-debugging.md`

**问题 #11** (第 535 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptogbf412TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #13** (第 605 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnaiwsv9nTempValidation.java:3: 错误: 找不到符号
        MiniClusterResourceConfiguration config =
        ^
  符号:   类 MiniClusterResourceConfiguration
  位置: 类 TempValidat
- **错误行**: 3

**问题 #14** (第 634 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz5szkpb6TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.typeinfo.Types;
^
C:\Users\luyan\AppData\Local\Temp\tmpz5szkpb6TempValidation.java:4
- **错误行**: 4

**问题 #28** (第 861 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeuu6h312TempValidation.java:4: 错误: 非法的表达式开始
public CompletableFuture<Acknowledge> submitJob(
^
C:\Users\luyan\AppData\Local\Temp\tmpeuu6h312TempValidation.java:24:
- **错误行**: 4

**问题 #29** (第 885 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsj9n5a9fTempValidation.java:4: 错误: 非法的表达式开始
public void startScheduling() {
^
C:\Users\luyan\AppData\Local\Temp\tmpsj9n5a9fTempValidation.java:19: 错误: 需要 class、int
- **错误行**: 4

**问题 #30** (第 904 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq3exq039TempValidation.java:4: 错误: 非法的表达式开始
public CompletableFuture<CompletedCheckpoint> triggerCheckpoint(
^
C:\Users\luyan\AppData\Local\Temp\tmpq3exq039TempVal
- **错误行**: 4

**问题 #31** (第 937 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr39uho87TempValidation.java:4: 错误: 非法的表达式开始
public void run() {
^
C:\Users\luyan\AppData\Local\Temp\tmpr39uho87TempValidation.java:18: 错误: 需要 class、interface、enum
- **错误行**: 4

**问题 #32** (第 955 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6kdzr6oxTempValidation.java:4: 错误: 非法的表达式开始
public boolean allocateSlot(
^
C:\Users\luyan\AppData\Local\Temp\tmp6kdzr6oxTempValidation.java:17: 错误: 需要 class、interf
- **错误行**: 4

**问题 #33** (第 972 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjkqpiox8TempValidation.java:4: 错误: 非法的表达式开始
public MemorySegment requestBuffer() throws IOException {
^
C:\Users\luyan\AppData\Local\Temp\tmpjkqpiox8TempValidation
- **错误行**: 4

**问题 #34** (第 988 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_3dvny4nTempValidation.java:4: 错误: 非法的表达式开始
public void processBarrier(
^
C:\Users\luyan\AppData\Local\Temp\tmp_3dvny4nTempValidation.java:17: 错误: 需要 class、interfa
- **错误行**: 4

**问题 #35** (第 1005 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa7r_5d1bTempValidation.java:4: 错误: 非法的表达式开始
public void run() {
^
C:\Users\luyan\AppData\Local\Temp\tmpa7r_5d1bTempValidation.java:16: 错误: 需要 class、interface、enum
- **错误行**: 4

**问题 #36** (第 1021 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpphpw47_vTempValidation.java:4: 错误: 非法的表达式开始
private void restoreState() throws Exception {
^
C:\Users\luyan\AppData\Local\Temp\tmpphpw47_vTempValidation.java:12: 错
- **错误行**: 4

**问题 #37** (第 1035 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpme84fbdpTempValidation.java:4: 错误: 非法的表达式开始
public void emit(T record) throws IOException {
^
C:\Users\luyan\AppData\Local\Temp\tmpme84fbdpTempValidation.java:11:
- **错误行**: 4

**问题 #38** (第 1046 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp40an_nk_TempValidation.java:4: 错误: 非法的表达式开始
public void notifyCreditAvailable(InputChannelID inputChannelId) {
^
C:\Users\luyan\AppData\Local\Temp\tmp40an_nk_TempV
- **错误行**: 4

**问题 #39** (第 1059 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv9dmbqpnTempValidation.java:4: 错误: 非法的表达式开始
public void checkAndWaitForBuffers() throws IOException {
^
C:\Users\luyan\AppData\Local\Temp\tmpv9dmbqpnTempValidation
- **错误行**: 4

**问题 #51** (第 1270 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqa97nrhwOptimizedMap.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<ComplexObject> stream = ...;
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 2

**问题 #54** (第 1328 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6ahvl0rtLeakyFunction.java:2: 错误: 非法的类型开始
public class LeakyFunction extends KeyedProcessFunction<...> {
                                                        ^

- **错误行**: 2

**问题 #57** (第 1386 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6pcexubpDeadlockInAsyncIO.java:2: 错误: 非法的类型开始
public class DeadlockInAsyncIO extends RichAsyncFunction<...> {

- **错误行**: 2


### `Flink\09-practices\09.07-performance\flink-performance-tuning-methodology.md`

**问题 #4** (第 283 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzw710c0uSaltedKeyPartitioner.java:25: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Event> salted = events
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 25


### `Flink\10-internals\checkpoint-source-analysis.md`

**问题 #9** (第 255 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgd2mp6dhTempValidation.java:4: 错误: 非法的表达式开始
private long checkpointIdCounter = 1;
^
C:\Users\luyan\AppData\Local\Temp\tmpgd2mp6dhTempValidation.java:11: 错误: 需要 cla
- **错误行**: 4

**问题 #10** (第 276 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplmhqdy85TempValidation.java:4: 错误: 非法的表达式开始
public void processBarrier(CheckpointBarrier receivedBarrier, int channelIndex) throws IOException {
^
C:\Users\luyan\A
- **错误行**: 4

**问题 #11** (第 318 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc5wqo5crTempValidation.java:4: 错误: 非法的表达式开始
public void processBarrier(CheckpointBarrier barrier, int channelIndex) {
^
C:\Users\luyan\AppData\Local\Temp\tmpc5wqo5
- **错误行**: 4

**问题 #12** (第 344 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjgjw0w6nTempValidation.java:4: 错误: 非法的表达式开始
public void snapshotState(FunctionSnapshotContext context) throws Exception {
^
C:\Users\luyan\AppData\Local\Temp\tmpjg
- **错误行**: 4

**问题 #13** (第 374 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp44qqs3nvTempValidation.java:4: 错误: 非法的表达式开始
public SnapshotResult<StateObject> snapshot(...) {
^
C:\Users\luyan\AppData\Local\Temp\tmp44qqs3nvTempValidation.java:4
- **错误行**: 4

**问题 #14** (第 396 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkcjl38loTempValidation.java:4: 错误: 非法的表达式开始
private ScheduledFuture<?> schedulerHandle;
^
C:\Users\luyan\AppData\Local\Temp\tmpkcjl38loTempValidation.java:20: 错误:
- **错误行**: 4

**问题 #16** (第 450 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvbj11k8wTempValidation.java:4: 错误: 非法的表达式开始
public CheckpointCoordinator(
^
C:\Users\luyan\AppData\Local\Temp\tmpvbj11k8wTempValidation.java:4: 错误: 方法声明无效; 需要返回类型

- **错误行**: 4

**问题 #19** (第 527 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp12ywm4hkTempValidation.java:6: 错误: 非法的表达式开始
public void triggerCheckpoint(long timestamp) {
^
C:\Users\luyan\AppData\Local\Temp\tmp12ywm4hkTempValidation.java:25:
- **错误行**: 6

**问题 #21** (第 621 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpztyfw2frScheduledTrigger.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
private void scheduleTriggerWithDelay(long delay) {
        ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #22** (第 642 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2xv8_qokTempValidation.java:3: 错误: 非法的表达式开始
public void triggerCheckpoint(long timestamp) throws CheckpointTriggerException {
^
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 3

**问题 #23** (第 681 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqt7lfn8yTempValidation.java:4: 错误: 非法的表达式开始
private void blockChannel(int channelIndex) throws IOException {
^
C:\Users\luyan\AppData\Local\Temp\tmpqt7lfn8yTempVal
- **错误行**: 4

**问题 #24** (第 716 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7zkzu9nnTempValidation.java:11: 错误: 非法的表达式开始
private void handleAlignmentTimeout() {
^
C:\Users\luyan\AppData\Local\Temp\tmp7zkzu9nnTempValidation.java:20: 错误: 需要
- **错误行**: 11

**问题 #26** (第 791 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdfyczk87TempValidation.java:4: 错误: 非法的表达式开始
public void snapshotState(StateSnapshotContext context) throws Exception {
^
C:\Users\luyan\AppData\Local\Temp\tmpdfycz
- **错误行**: 4

**问题 #28** (第 849 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwzk217yuTempValidation.java:4: 错误: 非法的表达式开始
public boolean restoreLatestCheckpointedStateToAll(
^
C:\Users\luyan\AppData\Local\Temp\tmpwzk217yuTempValidation.java:
- **错误行**: 4

**问题 #29** (第 878 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplvly9xf8TempValidation.java:4: 错误: 非法的表达式开始
public void assignStates() {
^
C:\Users\luyan\AppData\Local\Temp\tmplvly9xf8TempValidation.java:25: 错误: 需要 class、interf
- **错误行**: 4

**问题 #30** (第 911 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyriq_bzlIncrementalSnapshotStrategy.java:4: 错误: 非法的类型开始
    public SnapshotResult<StateObject> performIncrementalSnapshot(...) {

- **错误行**: 4

**问题 #32** (第 975 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw95xi1aaTempValidation.java:4: 错误: 非法的表达式开始
public void processBarrier(CheckpointBarrier barrier, int channelIndex) {
^
C:\Users\luyan\AppData\Local\Temp\tmpw95xi1
- **错误行**: 4

**问题 #33** (第 1002 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5nh6y1n7TempValidation.java:4: 错误: 非法的表达式开始
private boolean allBarriersReceived() {
^
C:\Users\luyan\AppData\Local\Temp\tmp5nh6y1n7TempValidation.java:14: 错误: 需要 c
- **错误行**: 4

**问题 #34** (第 1050 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0ruqa1caTempValidation.java:4: 错误: 非法的表达式开始
public void processBarrier(CheckpointBarrier barrier, int channelIndex) {
^
C:\Users\luyan\AppData\Local\Temp\tmp0ruqa1
- **错误行**: 4

**问题 #35** (第 1078 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw0_311vdTempValidation.java:4: 错误: 非法的表达式开始
public void readChannelState() {
^
C:\Users\luyan\AppData\Local\Temp\tmpw0_311vdTempValidation.java:17: 错误: 需要 class、in
- **错误行**: 4

**问题 #36** (第 1126 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxe7dorpnTempValidation.java:4: 错误: 非法的表达式开始
public void snapshotState(FunctionSnapshotContext context) throws Exception {
^
C:\Users\luyan\AppData\Local\Temp\tmpxe
- **错误行**: 4

**问题 #37** (第 1160 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphc6pjamoTempValidation.java:5: 错误: 非法的表达式开始
public void notifyCheckpointAborted(long checkpointId) {
^
C:\Users\luyan\AppData\Local\Temp\tmphc6pjamoTempValidation.
- **错误行**: 5

**问题 #38** (第 1186 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2an83gpoTempValidation.java:3: 错误: 非法的表达式开始
public void commit(Transaction txn) {
^
C:\Users\luyan\AppData\Local\Temp\tmp2an83gpoTempValidation.java:12: 错误: 需要 cla
- **错误行**: 3

**问题 #39** (第 1230 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk2l973ocIncrementalStateHandle.java:5: 错误: 找不到符号
    List<StreamStateHandle> sharedStateHandles;      // 共享状态(来自之前Checkpoint)
         ^
  符号:   类 StreamStateHandl
- **错误行**: 5

**问题 #40** (第 1267 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphk6jpzjzTempValidation.java:4: 错误: 非法的表达式开始
public void unregisterUnusedState(long lowestRetainCheckpoint) {
^
C:\Users\luyan\AppData\Local\Temp\tmphk6jpzjzTempVal
- **错误行**: 4

**问题 #41** (第 1296 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwm2dthj3TempValidation.java:6: 错误: 非法的表达式开始
public CompletableFuture<CompletedCheckpoint> triggerCheckpoint(long timestamp) {
^
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 6

**问题 #43** (第 1470 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd1lgl9yoTempValidation.java:7: 错误: 需要';'
public void processBarrier(CheckpointBarrier receivedBarrier, int channelIndex)
                          ^
C:\Users\luyan
- **错误行**: 7

**问题 #45** (第 1589 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpplgkmfb6TempValidation.java:7: 错误: 需要';'
public void snapshotState(StateSnapshotContext context) throws Exception {
                         ^
C:\Users\luyan\AppDa
- **错误行**: 7

**问题 #47** (第 1704 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmmxgwwziTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #49** (第 1805 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppunzk70pMemoryStateBackend.java:5: 错误: 非法的类型开始
    public <K> CheckpointableKeyedStateBackend<K> createKeyedStateBackend(...) {

- **错误行**: 5

**问题 #50** (第 1844 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpttd42dafRocksDBStateBackend.java:5: 错误: 非法的类型开始
    public <K> CheckpointableKeyedStateBackend<K> createKeyedStateBackend(...) {

- **错误行**: 5

**问题 #63** (第 2446 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_nbj65p9TempValidation.java:4: 错误: 不是语句
grep "checkpointId=12345" flink-*.log
^
C:\Users\luyan\AppData\Local\Temp\tmp_nbj65p9TempValidation.java:4: 错误: 需要';'
grep
- **错误行**: 4

**问题 #64** (第 2458 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp05cjy0vcTempValidation.java:4: 错误: 非法的表达式开始
public PendingCheckpoint(...) {
^
C:\Users\luyan\AppData\Local\Temp\tmp05cjy0vcTempValidation.java:4: 错误: 方法声明无效; 需要返回类
- **错误行**: 4

**问题 #65** (第 2475 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7v4y0br6TempValidation.java:4: 错误: 非法的表达式开始
private long alignmentStartNanos;
^
C:\Users\luyan\AppData\Local\Temp\tmp7v4y0br6TempValidation.java:6: 错误: 非法的类型开始
pub
- **错误行**: 4


### `Flink\10-internals\jobmanager-source-analysis.md`

**问题 #10** (第 153 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppk8yp126TempValidation.java:4: 错误: 非法的表达式开始
private void handleJobMasterError(Throwable cause) {
^
C:\Users\luyan\AppData\Local\Temp\tmppk8yp126TempValidation.java
- **错误行**: 4

**问题 #11** (第 172 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplel4pbseTempValidation.java:4: 错误: 找不到符号
for (JobVertex vertex : jobGraph.getVertices()) {
                        ^
  符号:   变量 jobGraph
  位置: 类 TempValidation
C:\
- **错误行**: 4

**问题 #13** (第 206 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8ocs9zwwTempValidation.java:4: 错误: 非法的表达式开始
public void processBarrier(CheckpointBarrier barrier, InputChannelInfo channelInfo) {
^
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #14** (第 227 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprfl9cqp0TempValidation.java:4: 错误: 不是语句
Phase 1 (Request):  JobMaster ──requestSlot──▶ ResourceManager
^
C:\Users\luyan\AppData\Local\Temp\tmprfl9cqp0TempValidatio
- **错误行**: 4

**问题 #19** (第 385 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp68fmvab7TempValidation.java:9: 错误: 非法的表达式开始
public void processBarrier(CheckpointBarrier barrier, InputChannelInfo channelInfo) {
^
C:\Users\luyan\AppData\Local\Te
- **错误行**: 9

**问题 #21** (第 443 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb_mhka18TempValidation.java:3: 错误: 非法的表达式开始
public static ExecutionGraph buildGraph(
^
C:\Users\luyan\AppData\Local\Temp\tmpb_mhka18TempValidation.java:18: 错误: 非法的
- **错误行**: 3

**问题 #26** (第 622 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsfn3sbslTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #27** (第 652 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1awoxwscTempValidation.java:5: 错误: 非法的表达式开始
public CompletableFuture<Acknowledge> submitJob(
^
C:\Users\luyan\AppData\Local\Temp\tmp1awoxwscTempValidation.java:73:
- **错误行**: 5

**问题 #29** (第 740 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbm0ms1kzTempValidation.java:4: 错误: 非法的表达式开始
public Collection<SlotExecutionVertexAssignment> allocateSlots(
^
C:\Users\luyan\AppData\Local\Temp\tmpbm0ms1kzTempVali
- **错误行**: 4

**问题 #30** (第 768 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3m6wd8trCheckpointCoordinator.java:2: 错误: 需要 class、interface、enum 或 record
env.enableCheckpointing(10000);
^
C:\Users\luyan\AppData\Local\Temp\tmp3m6wd8trCheckpoin
- **错误行**: 2

**问题 #32** (第 842 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6d6evstaTempValidation.java:6: 错误: 非法的表达式开始
public void heartbeatTimeout(ResourceID resourceID) {
^
C:\Users\luyan\AppData\Local\Temp\tmp6d6evstaTempValidation.jav
- **错误行**: 6

**问题 #44** (第 1280 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp22pya_daTempValidation.java:7: 错误: 需要';'
-Djobmanager.memory.process.size=1024m
                                     ^
C:\Users\luyan\AppData\Local\Temp\tmp22pya_d
- **错误行**: 7

**问题 #45** (第 1305 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp89yhodjfTempValidation.java:6: 错误: 需要';'
logger.jobmaster.name = org.apache.flink.runtime.jobmaster
                                                          ^
C:\
- **错误行**: 6

**问题 #46** (第 1335 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9cpx69y6JobMaster.java:102: 错误: 非法的表达式开始
                new SlotOffer(availableSlot.get().getAllocationId(), ...));

- **错误行**: 102


### `Flink\10-internals\memory-management-internals.md`

**问题 #9** (第 245 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvxnzgd0yLocalBufferPool.java:2: 错误: 找不到符号
class LocalBufferPool implements BufferPool {
                                 ^
  符号: 类 BufferPool
C:\Users\luyan\AppDat
- **错误行**: 2

**问题 #11** (第 359 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr5_xyw4tTempValidation.java:4: 错误: 非法的表达式开始
public static final int DEFAULT_PAGE_SIZE = 32768;  // 32KB
^
C:\Users\luyan\AppData\Local\Temp\tmpr5_xyw4tTempValidati
- **错误行**: 4

**问题 #14** (第 514 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphdhhp7udTempValidation.java:3: 错误: 找不到符号
if (currentNumberOfMemorySegments > numberOfRequiredMemorySegments) {
    ^
  符号:   变量 currentNumberOfMemorySegments
  位置:
- **错误行**: 3

**问题 #15** (第 530 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp77lo6buTempValidation.java:3: 错误: 非法的表达式开始
private MemorySegment requestMemorySegmentInternal() {
^
C:\Users\luyan\AppData\Local\Temp\tmpp77lo6buTempValidation.ja
- **错误行**: 3

**问题 #16** (第 552 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw1y_fbv4TempValidation.java:3: 错误: 非法的表达式开始
public int getInt(int index) {
^
C:\Users\luyan\AppData\Local\Temp\tmpw1y_fbv4TempValidation.java:12: 错误: 需要 class、inte
- **错误行**: 3

**问题 #17** (第 570 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpynlj6kw9TempValidation.java:3: 错误: 非法的表达式开始
public void free() {
^
C:\Users\luyan\AppData\Local\Temp\tmpynlj6kw9TempValidation.java:10: 错误: 需要 class、interface、enum
- **错误行**: 3

**问题 #22** (第 886 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_4kziauuTempValidation.java:4: 错误: 找不到符号
long address = MemoryUtils.allocateUnsafe(size);
                                          ^
  符号:   变量 size
  位置: 类 TempV
- **错误行**: 4

**问题 #23** (第 907 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp212owpovTempValidation.java:3: 错误: 找不到符号
        CompletableFuture<Buffer> future = new CompletableFuture<>();
        ^
  符号:   类 CompletableFuture
  位置: 类 TempVa
- **错误行**: 3

**问题 #24** (第 933 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptfkmz7hhTempValidation.java:3: 错误: 非法的表达式开始
public int getInt(int index) {
^
C:\Users\luyan\AppData\Local\Temp\tmptfkmz7hhTempValidation.java:12: 错误: 需要 class、inte
- **错误行**: 3

**问题 #25** (第 1015 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcfunjc54TempValidation.java:4: 错误: 需要';'
public Buffer retain() {
                    ^
C:\Users\luyan\AppData\Local\Temp\tmpcfunjc54TempValidation.java:10: 错误: 需要
- **错误行**: 4

**问题 #30** (第 1242 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<block mapping start>',)
  in "<unicode string>", line 9, column 1:
    taskmanager.memory.network.fract ...
    ^ (line: 9)
- **错误行**: 9

**问题 #32** (第 1305 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk98libbtTempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `Flink\10-internals\network-stack-internals.md`

**问题 #1** (第 49 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvcx_1lvcTempValidation.java:4: 错误: 不是语句
taskmanager.memory.network.min: 64mb
                          ^
C:\Users\luyan\AppData\Local\Temp\tmpvcx_1lvcTempValidatio
- **错误行**: 4

**问题 #9** (第 332 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv0tdfz2qTempValidation.java:4: 错误: 找不到符号
ResultPartitionWriter writer = new ResultPartition(
^
  符号:   类 ResultPartitionWriter
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 4


### `Flink\10-internals\scheduler-source-analysis.md`

**问题 #4** (第 239 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_kwmzkz6SchedulerBase.java:14: 错误: 非法的表达式开始
    protected void transitionToRunning() { ... }
                                           ^
C:\Users\luyan\AppData\Lo
- **错误行**: 14

**问题 #18** (第 663 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_ra2ry08TempValidation.java:3: 错误: 非法的表达式开始
private Locality computeLocality(SlotInfo slot, SlotProfile req) {
^
C:\Users\luyan\AppData\Local\Temp\tmp_ra2ry08TempV
- **错误行**: 3

**问题 #19** (第 686 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9nf6nc86FailoverStrategy.java:11: 错误: 非法的类型开始
    public Set<ExecutionVertexID> getTasksNeedingRestart(...) {

- **错误行**: 11

**问题 #23** (第 803 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6uv7aclhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #24** (第 827 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7yy_o84gTempValidation.java:4: 错误: 不是语句
jobmanager.scheduler: adaptive
          ^
C:\Users\luyan\AppData\Local\Temp\tmp7yy_o84gTempValidation.java:4: 错误: 需要';'
jo
- **错误行**: 4

**问题 #25** (第 841 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcc35ysepTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #26** (第 862 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdl1dgy94TempValidation.java:4: 错误: 不是语句
jobmanager.scheduler: speculative
          ^
C:\Users\luyan\AppData\Local\Temp\tmpdl1dgy94TempValidation.java:4: 错误: 需要';'
- **错误行**: 4

**问题 #27** (第 877 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp90wsrcyzTempValidation.java:4: 错误: 不是语句
slot.request.timeout: 300000  // 5分钟
            ^
C:\Users\luyan\AppData\Local\Temp\tmp90wsrcyzTempValidation.java:4: 错误:
- **错误行**: 4

**问题 #28** (第 889 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfm0zlb4rTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpfm0
- **错误行**: 3

**问题 #29** (第 910 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmdub6ssnTempValidation.java:4: 错误: 不是语句
jobmanager.execution.failover-strategy: region
                             ^
C:\Users\luyan\AppData\Local\Temp\tmpmdub6ssn
- **错误行**: 4

**问题 #30** (第 925 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm1xjlngfTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Flink\10-internals\serialization-internals.md`

**问题 #7** (第 202 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpviazepfbMyMap.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Tuple2<String, Integer>> stream = env.fromElements(
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\App
- **错误行**: 2

**问题 #10** (第 359 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpem5bn7wfTempValidation.java:7: 错误: 非法的表达式开始
private static <T> boolean isValidPojoClass(Class<T> clazz) {
^
C:\Users\luyan\AppData\Local\Temp\tmpem5bn7wfTempValida
- **错误行**: 7

**问题 #11** (第 421 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwzbgzg1bTempValidation.java:7: 错误: 非法的表达式开始
private static <X> TypeInformation<X> createTypeInfoFromInputs(
^
C:\Users\luyan\AppData\Local\Temp\tmpwzbgzg1bTempVali
- **错误行**: 7

**问题 #16** (第 686 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt2jjk1ffUserEvent.java:30: 错误: 未命名类 是预览功能，默认情况下禁用。
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
^
  （请使用 --enable-preview
- **错误行**: 30


### `Flink\10-internals\source-code-reading-guide.md`

**问题 #12** (第 392 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp91eo9zc2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #13** (第 416 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu27gmhwwTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpu2
- **错误行**: 4

**问题 #14** (第 433 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpppb8wj4sTempValidation.java:4: 错误: 非法的表达式开始
public <R> SingleOutputStreamOperator<R> flatMap(
^
C:\Users\luyan\AppData\Local\Temp\tmpppb8wj4sTempValidation.java:16
- **错误行**: 4

**问题 #15** (第 449 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpot56gfs2TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpot
- **错误行**: 4

**问题 #16** (第 476 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkx3b4iztTempValidation.java:4: 错误: 非法的表达式开始
public StreamGraph generate() {
^
C:\Users\luyan\AppData\Local\Temp\tmpkx3b4iztTempValidation.java:19: 错误: 需要 class、int
- **错误行**: 4

**问题 #17** (第 495 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiwen51y0TempValidation.java:4: 错误: 非法的表达式开始
public JobGraph createJobGraph(StreamGraph streamGraph) {
^
C:\Users\luyan\AppData\Local\Temp\tmpiwen51y0TempValidation
- **错误行**: 4

**问题 #18** (第 516 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbh3s_nelTempValidation.java:4: 错误: 非法的表达式开始
public static ExecutionGraph buildGraph(...)
^
C:\Users\luyan\AppData\Local\Temp\tmpbh3s_nelTempValidation.java:4: 错误:
- **错误行**: 4

**问题 #27** (第 772 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprgbj57llTempValidation.java:4: 错误: 需要';'
jobGraph.getJobID().toString().equals("your-job-id")
                                                    ^
1 个错误

- **错误行**: 4

**问题 #28** (第 779 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpayxrx_ifTempValidation.java:4: 错误: 不是语句
taskDeploymentDescriptor.getJobID().toString().equals("your-job-id") &&

- **错误行**: 4

**问题 #29** (第 789 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 5, column 1:
    logger.runtime.name = org.apache ...
    ^ (line: 5)
- **错误行**: 5


### `Flink\10-internals\state-backend-internals.md`

**问题 #11** (第 699 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa0iun0t2TempValidation.java:8: 错误: 非法的表达式开始
private void snapshotStateTable(
^
C:\Users\luyan\AppData\Local\Temp\tmpa0iun0t2TempValidation.java:48: 错误: 需要 class、in
- **错误行**: 8

**问题 #27** (第 2148 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppk_24db7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #29** (第 2220 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb_f8fv2qTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #31** (第 2309 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm4yjg53zTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpm4
- **错误行**: 4


### `Flink\10-internals\taskmanager-source-analysis.md`

**问题 #10** (第 171 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp3oyz6syTempValidation.java:4: 错误: 非法的表达式开始
public boolean add(T task) {
^
C:\Users\luyan\AppData\Local\Temp\tmpp3oyz6syTempValidation.java:15: 错误: 需要 class、interf
- **错误行**: 4

**问题 #11** (第 196 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprx6h_dbrTempValidation.java:4: 错误: 非法的表达式开始
public void run() {
^
C:\Users\luyan\AppData\Local\Temp\tmprx6h_dbrTempValidation.java:28: 错误: 需要 class、interface、enum
- **错误行**: 4

**问题 #13** (第 279 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdn_y3tzvTempValidation.java:4: 错误: 非法的表达式开始
private void registerSlotsWithResourceManager() {
^
C:\Users\luyan\AppData\Local\Temp\tmpdn_y3tzvTempValidation.java:17
- **错误行**: 4

**问题 #16** (第 357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc2unni72TempValidation.java:4: 错误: 非法的表达式开始
public boolean allocateSlot(int index, JobID jobId, AllocationID allocationId,
^
C:\Users\luyan\AppData\Local\Temp\tmpc
- **错误行**: 4

**问题 #17** (第 383 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3_1e4k8rTempValidation.java:4: 错误: 非法的表达式开始
public void createSlotSharingGroup(SlotSharingGroupId slotSharingGroupId,
^
C:\Users\luyan\AppData\Local\Temp\tmp3_1e4k
- **错误行**: 4

**问题 #19** (第 412 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzo9m8kg1TempValidation.java:4: 错误: 非法的表达式开始
public CompletableFuture<Acknowledge> submitTask(
^
C:\Users\luyan\AppData\Local\Temp\tmpzo9m8kg1TempValidation.java:31
- **错误行**: 4

**问题 #20** (第 445 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprozd71olTempValidation.java:4: 错误: 非法的表达式开始
private void restoreState() throws Exception {
^
C:\Users\luyan\AppData\Local\Temp\tmprozd71olTempValidation.java:28: 错
- **错误行**: 4

**问题 #24** (第 605 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvy36bmbxTempValidation.java:4: 错误: 非法的表达式开始
public void run() {
^
C:\Users\luyan\AppData\Local\Temp\tmpvy36bmbxTempValidation.java:17: 错误: 需要 class、interface、enum
- **错误行**: 4

**问题 #29** (第 850 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm14qo16eInputGateExample.java:30: 错误: 非法的表达式开始
                new PartitionRequestClientFactory(new NettyConnectionManager(...)),

- **错误行**: 30


### `Flink\10-internals\watermark-source-analysis.md`

**问题 #8** (第 249 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmls1bycfWatermarkStrategyWithIdleness.java:4: 错误: 需要 class、interface、enum 或 record
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
^
1 个错误

- **错误行**: 4

**问题 #14** (第 467 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2yc_cq5oWatermarkStrategy.java:15: 错误: 未命名类 是预览功能，默认情况下禁用。
private static final long WATERMARK_INTERVAL = 200L; // 毫秒
                     ^
  （请使用 --enable-previe
- **错误行**: 15

**问题 #16** (第 512 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpplkg1_icTempValidation.java:4: 错误: 非法的表达式开始
private void findAndOutputNewMinWatermarkAcrossAlignedChannels() throws Exception {
^
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #19** (第 604 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_47f337rWindowOperator.java:2: 错误: 非法的类型开始
public class WindowOperator<K, IN, OUT, W extends Window> extends AbstractUdfStreamOperator<OUT, ...> {

- **错误行**: 2

**问题 #23** (第 698 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9edwtvsaTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9ed
- **错误行**: 3

**问题 #27** (第 863 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd47n5wdvWatermarkStrategyWithAlignment.java:2: 错误: 需要 class、interface、enum 或 record
WatermarkStrategy
^
C:\Users\luyan\AppData\Local\Temp\tmpd47n5wdvWatermarkStrat
- **错误行**: 2

**问题 #29** (第 932 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu_q9ak0wTempValidation.java:4: 错误: 非法的表达式开始
public TriggerResult onElement(T element, long timestamp, TimeWindow window, TriggerContext ctx) {
^
C:\Users\luyan\App
- **错误行**: 4

**问题 #31** (第 982 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4ssj3ulxWindowOperator.java:2: 错误: 非法的类型开始
public class WindowOperator<K, IN, ACC, OUT, W extends Window> extends ... {

- **错误行**: 2

**问题 #36** (第 1148 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyx86l5k3TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpyx8
- **错误行**: 3

**问题 #37** (第 1164 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnwzjrkt8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnwz
- **错误行**: 3

**问题 #40** (第 1287 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbnznrqrhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpbnz
- **错误行**: 3

**问题 #41** (第 1310 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2_6kptnxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2_6
- **错误行**: 3

**问题 #42** (第 1344 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpup0pq81tTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpup0
- **错误行**: 3

**问题 #43** (第 1370 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmviyor10KeepLastNEvictor.java:42: 错误: 需要 class、interface、enum 或 record
stream
^
1 个错误

- **错误行**: 42

**问题 #44** (第 1422 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4z7dphnkTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #55** (第 2078 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpju5_9_gfTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpju
- **错误行**: 4

**问题 #58** (第 2166 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4yd_2f9sTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp4yd_2
- **错误行**: 3

**问题 #59** (第 2190 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcqicic1lTempValidation.java:4: 错误: 需要';'
log4j.logger.org.apache.flink.streaming.runtime.io.StatusWatermarkValve=DEBUG

- **错误行**: 4


### `Flink\3.9-state-backends-deep-comparison.md`

**问题 #21** (第 589 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend.rocksdb.memory.man ...
    ^ (line: 2)
found duplicate key "state.backend.rocksdb.memory.managed" with value
- **错误行**: 2

**问题 #22** (第 610 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend.rocksdb.compaction ...
    ^ (line: 2)
found duplicate key "state.backend.rocksdb.compaction.style" with valu
- **错误行**: 2


### `Flink\data-types-complete-reference.md`

**问题 #6** (第 261 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptp3uxrr9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.DataTypes;
        ^
C:\Users\luyan\AppData\Local\Temp\tmptp3uxrr9TempValidat
- **错误行**: 3


### `Flink\elasticsearch-connector-guide.md`

**问题 #4** (第 248 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplhcba_edTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.elasticsearch.sink.Elasticsearch7SinkBuilder;
^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #6** (第 325 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpldxm48swTempValidation.java:4: 错误: 找不到符号
ElasticsearchSink<Event> esSink = new Elasticsearch7SinkBuilder<Event>()
^
  符号:   类 ElasticsearchSink
  位置: 类 TempValidat
- **错误行**: 4


### `Flink\flink-feature-store-integration.md`

**问题 #4** (第 384 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc2zuju1nTempValidation.java:24: 错误: 找不到符号
tableEnv.executeSql(createTable);
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpc2zuj
- **错误行**: 24


### `Flink\flink-nexmark-benchmark-guide.md`

**问题 #2** (第 234 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb8x_yrobTempValidation.java:5: 错误: 找不到符号
Random random = new Random(SEED);
^
  符号:   类 Random
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpb8x_yrobT
- **错误行**: 5

**问题 #3** (第 242 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqdhvou_yTempValidation.java:5: 错误: 找不到符号
long eventTime = baseTime + (offsetSec * 1000);
                             ^
  符号:   变量 offsetSec
  位置: 类 TempValidation
- **错误行**: 5

**问题 #10** (第 381 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpha42nmr6TempValidation.java:4: 错误: 找不到符号
tableEnv.getConfig().getConfiguration()
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #12** (第 405 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6vejz556TempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #15** (第 459 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmjgx_fl5TempValidation.java:4: 错误: 需要';'
CREATE TABLE Person (
            ^
C:\Users\luyan\AppData\Local\Temp\tmpmjgx_fl5TempValidation.java:5: 错误: 需要')'或','

- **错误行**: 4

**问题 #16** (第 495 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplhupf9xiTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Flink\flink-state-backends-comparison.md`

**问题 #8** (第 487 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxxp_we75TempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #9** (第 514 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplam6yeyfTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #10** (第 563 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa84t4f4iTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #14** (第 719 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprjp5sh0xTempValidation.java:4: 错误: 找不到符号
config.set(RocksDBOptions.BLOCK_CACHE_SIZE, MemorySize.ofMebiBytes(256));
           ^
  符号:   变量 RocksDBOptions
  位置: 类 T
- **错误行**: 4

**问题 #16** (第 736 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdb7e9ajrTempValidation.java:3: 错误: 找不到符号
        config.set(CheckpointingOptions.INCREMENTAL_CHECKPOINTS, true);
                   ^
  符号:   变量 CheckpointingOptio
- **错误行**: 3

**问题 #18** (第 746 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6ugh51r5TempValidation.java:3: 错误: 找不到符号
        config.set(CheckpointingOptions.MAX_CONCURRENT_CHECKPOINTS, 1);
                   ^
  符号:   变量 CheckpointingOptio
- **错误行**: 3

**问题 #20** (第 759 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpticuin0vTempValidation.java:4: 错误: 找不到符号
config.set(CheckpointingOptions.LOCAL_RECOVERY, true);
           ^
  符号:   变量 CheckpointingOptions
  位置: 类 TempValidation
- **错误行**: 4


### `Flink\jdbc-connector-guide.md`

**问题 #4** (第 226 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7l6iyivvTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcConnectionOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmp7l6iyivvTempValida
- **错误行**: 3

**问题 #6** (第 295 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp34pxfmuaTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcInputFormat;
^
C:\Users\luyan\AppData\Local\Temp\tmp34pxfmuaTempValidation.j
- **错误行**: 3


### `Flink\mongodb-connector-guide.md`

**问题 #4** (第 246 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps7l77xzuTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.source.MongoSource;
^
C:\Users\luyan\AppData\Local\Temp\tmps7l77xzuTempValida
- **错误行**: 3

**问题 #5** (第 282 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjbydhesvTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.source.MongoSource;
^
C:\Users\luyan\AppData\Local\Temp\tmpjbydhesvTempValida
- **错误行**: 3

**问题 #6** (第 315 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmproaica0mTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.sink.MongoSink;
^
C:\Users\luyan\AppData\Local\Temp\tmproaica0mTempValidation
- **错误行**: 3


### `Flink\pulsar-functions-integration.md`

**问题 #8** (第 217 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmhbyo997TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpmhb
- **错误行**: 3


### `Flink\risingwave-integration-guide.md`

**问题 #6** (第 126 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprtnktulmTempValidation.java:4: 错误: 找不到符号
FlinkKafkaProducer<String> kafkaProducer = new FlinkKafkaProducer<>(
^
  符号:   类 FlinkKafkaProducer
  位置: 类 TempValidation
- **错误行**: 4

**问题 #9** (第 182 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzbtoqxkeTempValidation.java:4: 错误: 找不到符号
DebeziumSourceFunction<String> source = DebeziumSourceFunction.<String>builder()
^
  符号:   类 DebeziumSourceFunction
  位置:
- **错误行**: 4

**问题 #10** (第 193 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf3gql7i9TempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.sqlQuery(
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpf3gql7i9Te
- **错误行**: 4


### `Flink\state-backends-comparison.md`

**问题 #4** (第 240 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi_wbg9hwTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.runtime.state.hashmap.HashMapStateBackend;
^
C:\Users\luyan\AppData\Local\Temp\tmpi_wbg9hwTempV
- **错误行**: 3

**问题 #5** (第 273 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    state.backend: hashmap
    ^ (line: 4)
found duplicate key "state.backend" with value "rocksdb" (original value: "hashmap")

- **错误行**: 4

**问题 #6** (第 299 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplo6ec3dzTempValidation.java:4: 错误: 非法的表达式开始
public void monitorStateBackend(RuntimeContext ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmplo6ec3dzTempValidation.jav
- **错误行**: 4


### `INTEGRATED-GUIDE.md`

**问题 #3** (第 69 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpryc677jeTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `JAVA-CODE-FIX-REPORT.md`

**问题 #1** (第 46 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2emx1savTempValidation.java:5: 错误: 非法的表达式开始
DataStream<Event> stream = env.addSource(...);
                                         ^
1 个错误

- **错误行**: 5

**问题 #2** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1lmcm7r_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #3** (第 65 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq078pv22TempValidation.java:5: 错误: 非法的表达式开始
stream.assignTimestampsAndWatermarks(...);
                                     ^
1 个错误

- **错误行**: 5

**问题 #4** (第 73 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqub7ot9tTempValidation.java:4: 错误: 找不到符号
env.getConfig().setAutoWatermarkInterval(200);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4


### `KNOWLEDGE-GRAPH-DATA-GUIDE.md`

**问题 #12** (第 401 行, 语言: python)

- **错误**: SyntaxError: illegal target for annotation
- **错误行**: 1


### `Knowledge\01-concept-atlas\01.01-stream-processing-fundamentals.md`

**问题 #4** (第 600 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5895ydezTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp589
- **错误行**: 3

**问题 #5** (第 620 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5w2gte8vTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5w2
- **错误行**: 3


### `Knowledge\01-concept-atlas\01.02-time-semantics.md`

**问题 #7** (第 664 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8xufit83PeriodicWatermarkGenerator.java:28: 错误: 未命名类 是预览功能，默认情况下禁用。
WatermarkStrategy<MyEvent> customStrategy = WatermarkStrategy
^
  （请使用 --enable-preview 以启用 未命名
- **错误行**: 28

**问题 #9** (第 719 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9nd7si5vTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3


### `Knowledge\01-concept-atlas\01.03-window-concepts.md`

**问题 #2** (第 295 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5mnh9yalTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
        ^
C:\Users\luyan\Ap
- **错误行**: 3

**问题 #3** (第 317 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkza5a0okTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpkza
- **错误行**: 3

**问题 #4** (第 331 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6pdq9ct6TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp6pdq9ct6TempValidat
- **错误行**: 4

**问题 #6** (第 394 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppatksc63TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmppat
- **错误行**: 3

**问题 #7** (第 414 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1x0yo40kTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp1x0yo40kTempValidat
- **错误行**: 4


### `Knowledge\01-concept-atlas\01.04-state-management-concepts.md`

**问题 #4** (第 381 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp67tfrziyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp67tfr
- **错误行**: 3

**问题 #5** (第 400 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppkikvdbwTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4


### `Knowledge\01-concept-atlas\01.05-consistency-models.md`

**问题 #1** (第 229 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpupyb84y8TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.CheckpointingMode;
^
C:\Users\luyan\AppData\Local\Temp\tmpupyb84y8TempValidation.
- **错误行**: 4


### `Knowledge\01-concept-atlas\streaming-languages-landscape-2025.md`

**问题 #1** (第 339 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr079tl0vTempValidation.java:4: 错误: 找不到符号
ExecutorService executor = Executors.newFixedThreadPool(100);
^
  符号:   类 ExecutorService
  位置: 类 TempValidation
C:\Users\
- **错误行**: 4


### `Knowledge\02-design-patterns\02.01-stream-join-patterns.md`

**问题 #4** (第 747 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3hg5q9grCurrencyConversionTemporalJoin.java:93: 错误: 需要';'
        Table exchangeRatesTable = tableEnv.from("exchange_rates");
             ^
1 个错误

- **错误行**: 93


### `Knowledge\02-design-patterns\02.03-backpressure-handling-patterns.md`

**问题 #3** (第 280 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4b9vny15AdaptiveBuffer.java:16: 错误: 找不到符号
        } else if (ratio < 0.8 && currentLatency < targetLatency) {
                                                   ^

- **错误行**: 16


### `Knowledge\02-design-patterns\pattern-cep-complex-event.md`

**问题 #5** (第 470 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1cmmdq93TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.CEP;
^
C:\Users\luyan\AppData\Local\Temp\tmp1cmmdq93TempValidation.java:3: 错误: 不是语句
import
- **错误行**: 3

**问题 #6** (第 541 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpssj7b3i9TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpssj7b3i9TempValidat
- **错误行**: 4

**问题 #7** (第 600 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpst2ad7h3TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpst2ad7h3TempValidatio
- **错误行**: 4

**问题 #8** (第 635 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy6axib0eTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpy6axi
- **错误行**: 3

**问题 #9** (第 656 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplng8r26vTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmplng8r26vTempValidatio
- **错误行**: 4

**问题 #10** (第 683 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp29nm_npsTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp29nm_npsTempValidat
- **错误行**: 4

**问题 #12** (第 769 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp2cymb56TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpp2c
- **错误行**: 3

**问题 #13** (第 794 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphf36yzefTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmphf36y
- **错误行**: 3

**问题 #14** (第 810 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpobm9sdcoTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpobm9s
- **错误行**: 3

**问题 #15** (第 828 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3in931p_TempValidation.java:4: 错误: 找不到符号
Pattern<Event, ?> inefficient = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp3i
- **错误行**: 4


### `Knowledge\02-design-patterns\pattern-log-analysis.md`

**问题 #5** (第 453 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcozapuo3TempValidation.java:5: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpcozapuo3TempValidat
- **错误行**: 5

**问题 #6** (第 527 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjikwi9fkTraceAnalysisFunction.java:2: 错误: 需要 class、interface、enum 或 record
unifiedLogs
^
C:\Users\luyan\AppData\Local\Temp\tmpjikwi9fkTraceAnalysisFunction.java:10
- **错误行**: 2

**问题 #7** (第 596 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvsbg6qo2TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpvsbg6qo2TempValidat
- **错误行**: 4

**问题 #8** (第 648 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbuvc7sgzSlowRequestDetector.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<LatencyMetric> latencyMetrics = unifiedLogs
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luy
- **错误行**: 2


### `Knowledge\02-design-patterns\pattern-realtime-feature-engineering.md`

**问题 #4** (第 346 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp05a6zuaSessionAggregator.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Transaction> transactions = ...
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Loc
- **错误行**: 2


### `Knowledge\02-design-patterns\pattern-windowed-aggregation.md`

**问题 #3** (第 466 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl32mqtlxSumAggregate.java:1: 错误: 从发行版 9 开始, '_' 为关键字, 不能用作标识符
import org.apache.flink.streaming.api.scala._
                                            ^
C:\Users\
- **错误行**: 1

**问题 #4** (第 500 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9z10eu3dAverageAggregate.java:3: 错误: 从发行版 9 开始, '_' 为关键字, 不能用作标识符
  .keyBy(_.sensorId)
         ^
C:\Users\luyan\AppData\Local\Temp\tmp9z10eu3dAverageAggregate.jav
- **错误行**: 3

**问题 #10** (第 662 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkap2vyjjTopNFunction.java:1: 错误: 需要';'
import org.apache.flink.streaming.api.windowing.triggers.ContinuousTrigger

- **错误行**: 1

**问题 #11** (第 715 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp67844v1kTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp678
- **错误行**: 3


### `Knowledge\02-design-patterns\polyglot-streaming-patterns.md`

**问题 #9** (第 981 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc8o2zce_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Knowledge\03-business-patterns\data-mesh-streaming-architecture-2026.md`

**问题 #5** (第 409 行, 语言: yaml)

- **错误**: while scanning a block scalar
  in "<unicode string>", line 15, column 19:
        completeness: > 99.9%
                      ^ (line: 15)
expected a comment or a line break, but found '9'
  in "<uni
- **错误行**: 15


### `Knowledge\03-business-patterns\fintech-realtime-risk-control.md`

**问题 #6** (第 277 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppmey8_byTempValidation.java:4: 错误: 非法的表达式开始
public RiskDecision evaluate(Transaction txn) {
^
C:\Users\luyan\AppData\Local\Temp\tmppmey8_byTempValidation.java:28:
- **错误行**: 4


### `Knowledge\03-business-patterns\netflix-streaming-pipeline.md`

**问题 #12** (第 357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5tu45x_qTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5tu
- **错误行**: 3


### `Knowledge\03-business-patterns\uber-realtime-platform.md`

**问题 #27** (第 743 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm26jh5rbSurgePricingJob.java:15: 错误: 非法的表达式开始
        DataStream<DriverEvent> driverEvents = env.addSource(...);

- **错误行**: 15

**问题 #28** (第 881 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsolja5tpFraudDetectionJob.java:15: 错误: 非法的表达式开始
        DataStream<TripEvent> trips = env.addSource(...);
                                                    ^
C:\
- **错误行**: 15


### `Knowledge\04-technology-selection\engine-selection-guide.md`

**问题 #5** (第 675 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptb8zxdidTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmptb8zxdi
- **错误行**: 3


### `Knowledge\04-technology-selection\flink-vs-risingwave.md`

**问题 #8** (第 402 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq7mwg5tzTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpq7m
- **错误行**: 3

**问题 #10** (第 553 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4shbn98vTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmp4shbn98vTempValidatio
- **错误行**: 4


### `Knowledge\04-technology-selection\multidimensional-comparison-matrices.md`

**问题 #33** (第 1677 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpulkmoplbTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #34** (第 1705 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxp_4k3chTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #35** (第 1733 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvlpdhpu8TempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4


### `Knowledge\05-mapping-guides\migration-guides\05.1-spark-streaming-to-flink-migration.md`

**问题 #5** (第 166 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqsv1232kTempValidation.java:5: 错误: 找不到符号
env.getConfig().setAutoWatermarkInterval(200);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 5

**问题 #9** (第 245 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl_h6hpvmTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpl_
- **错误行**: 3

**问题 #11** (第 288 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8tiwoxicCountFunction.java:34: 错误: 需要 class、interface、enum 或 record
keyedStream.process(new CountFunction());
^
1 个错误

- **错误行**: 34

**问题 #13** (第 340 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpczggtsj_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpczg
- **错误行**: 3

**问题 #15** (第 363 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwl3zilihTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwl3zili
- **错误行**: 3

**问题 #19** (第 462 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps7x81blsTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmps7x
- **错误行**: 3

**问题 #20** (第 479 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbb3mbiheTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpbb3mb
- **错误行**: 3

**问题 #21** (第 494 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjd7w7oh2TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpjd7w7oh2TempValidat
- **错误行**: 4


### `Knowledge\05-mapping-guides\migration-guides\05.2-kafka-streams-to-flink-migration.md`

**问题 #5** (第 144 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpomj4qkaeTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpomj4qkaeTempV
- **错误行**: 3

**问题 #6** (第 167 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp48tqkzisTempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #7** (第 180 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb93zbetuTempValidation.java:3: 错误: 找不到符号
        KafkaSource<MyEvent> source = KafkaSource.<MyEvent>builder()
        ^
  符号:   类 KafkaSource
  位置: 类 TempValidatio
- **错误行**: 3

**问题 #8** (第 234 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvfglt9y4TempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #9** (第 255 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjtt1k83_TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpjt
- **错误行**: 4

**问题 #10** (第 308 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvwqt2fapTempValidation.java:3: 错误: 找不到符号
        KTable<String, Long> wordCounts = source
        ^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #11** (第 319 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3w11ei7vCountAggregate.java:6: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Tuple2<String, Long>> wordCounts = source
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 6

**问题 #12** (第 363 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg3_759nzTempValidation.java:3: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3

**问题 #13** (第 376 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuy9f1t9kTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpuy9f1t9kTempValidat
- **错误行**: 4

**问题 #21** (第 606 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmbxq7d8eTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpmbxq7d8eTempValidat
- **错误行**: 4


### `Knowledge\05-mapping-guides\migration-guides\05.3-storm-to-flink-migration.md`

**问题 #1** (第 84 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpecd8hr1sTempValidation.java:4: 错误: 找不到符号
Map<String, Object> state = new HashMap<>();
^
  符号:   类 Map
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpe
- **错误行**: 4

**问题 #2** (第 92 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeznel4jrTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpeznel4jrTem
- **错误行**: 3

**问题 #4** (第 131 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8cv9k8igTempValidation.java:5: 错误: 找不到符号
    .fieldsGrouping("split", new Fields("word"));
                                 ^
  符号:   类 Fields
  位置: 类 TempValidati
- **错误行**: 5

**问题 #8** (第 208 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpncw580mkTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.functions.AggregateFunction;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #9** (第 263 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjuq100trSentenceSpout.java:64: 错误: 未命名类 是预览功能，默认情况下禁用。
TopologyBuilder builder = new TopologyBuilder();
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\
- **错误行**: 64

**问题 #10** (第 339 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb12e91beWordCount.java:37: 错误: 未命名类 是预览功能，默认情况下禁用。
public static void main(String[] args) throws Exception {
              ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错
- **错误行**: 37

**问题 #12** (第 435 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdx7zx99pTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpdx7
- **错误行**: 3

**问题 #14** (第 481 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptyg90wiaTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.functions.AggregateFunction;
^
C:\Users\luyan\AppData\Local\Temp\tmptyg90wiaTempVali
- **错误行**: 4

**问题 #23** (第 727 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgpgtcc8gTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpgpg
- **错误行**: 3


### `Knowledge\05-mapping-guides\migration-guides\05.4-flink-1x-to-2x-migration.md`

**问题 #4** (第 144 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjzs6ave7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpjzs6ave7Tem
- **错误行**: 3

**问题 #5** (第 186 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph9zclujhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #6** (第 237 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend: rocksdb
    ^ (line: 2)
found duplicate key "state.backend" with value "rocksdb" (original value: "rocksdb")

- **错误行**: 2

**问题 #9** (第 350 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo8rjfahpTempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<String> consumer = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #10** (第 364 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo5bld_g4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpo5b
- **错误行**: 3

**问题 #11** (第 388 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp86mbqh5hTempValidation.java:4: 错误: 找不到符号
FlinkKafkaProducer<String> producer = new FlinkKafkaProducer<>(
^
  符号:   类 FlinkKafkaProducer
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #12** (第 402 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpley2e_9nTempValidation.java:4: 错误: 找不到符号
KafkaSink<String> sink = KafkaSink.<String>builder()
^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #13** (第 420 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpug7rdnijTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpug7rdnijTemp
- **错误行**: 3

**问题 #14** (第 441 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpce5kzw91TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpce5
- **错误行**: 3

**问题 #15** (第 463 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkjoq5f_9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpkjoq5
- **错误行**: 3

**问题 #16** (第 481 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5ggdl2bvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5ggdl
- **错误行**: 3


### `Knowledge\05-mapping-guides\migration-guides\05.5-batch-to-streaming-migration.md`

**问题 #2** (第 120 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp__kybbp4TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.functions.AggregateFunction;
^
C:\Users\luyan\AppData\Local\Temp\tmp__kybbp4TempVali
- **错误行**: 4

**问题 #5** (第 185 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsz834giqTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #6** (第 200 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7fxay_z3TempValidation.java:4: 错误: 找不到符号
List<Data> allData = readAllData();
^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp7fxay_z3T
- **错误行**: 4

**问题 #8** (第 234 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdbkkfuytTempValidation.java:4: 错误: 找不到符号
for (Record record : batchData) {
                     ^
  符号:   变量 batchData
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #9** (第 243 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_w9t5uunTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp_w9t5
- **错误行**: 3

**问题 #11** (第 317 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc3yiwkfqTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpc3yiwkfqTempValidat
- **错误行**: 4

**问题 #13** (第 359 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8fpxxom4TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp8fpxxom4TempValidat
- **错误行**: 4

**问题 #15** (第 407 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkyql3ji0TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpkyql3ji0TempValidat
- **错误行**: 4

**问题 #16** (第 432 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi3wygecsTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpi3wygecsTempValidat
- **错误行**: 4

**问题 #18** (第 469 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp652nt6uwDeduplicateFunction.java:39: 错误: 需要 class、interface、enum 或 record
stream.keyBy(e -> e.getUserId() + "_" + e.getEventType())
^
1 个错误

- **错误行**: 39

**问题 #20** (第 528 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmm9jzerqTopNFunction.java:37: 错误: 需要 class、interface、enum 或 record
stream.keyBy(ProductSale::getCategory)
^
1 个错误

- **错误行**: 37

**问题 #25** (第 671 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplgmw3ofaTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmplgmw3
- **错误行**: 3

**问题 #26** (第 689 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeqc7wjs3TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpeqc7w
- **错误行**: 3

**问题 #27** (第 714 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwtl70smaTempValidation.java:5: 错误: 找不到符号
    stream,
    ^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpwtl70smaTempValidation.jav
- **错误行**: 5


### `Knowledge\05-mapping-guides\streaming-etl-tools-landscape-2026.md`

**问题 #7** (第 664 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq5rzdwj2TempValidation.java:4: 错误: 找不到符号
Table orders = tEnv.fromDataStream(
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpq5rzdwj2
- **错误行**: 4


### `Knowledge\05-mapping-guides\streaming-sql-engines-2026-comparison.md`

**问题 #12** (第 847 行, 语言: sql)

- **错误**: 可能的语法问题: -- 4. 服务查询需直接查询SINK数据库
-- FLINK SQL本身不提供物化视图查询服务...


### `Knowledge\05-mapping-guides\struct-to-flink-mapping.md`

**问题 #1** (第 205 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb10sjk7uTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #2** (第 263 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp67_62zzxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp67_
- **错误行**: 3

**问题 #3** (第 310 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx5a0wvfkTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpx5a0wvf
- **错误行**: 3

**问题 #4** (第 361 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmp08fmusTempValidation.java:7: 错误: 找不到符号
env.setStateBackend(new HashMapStateBackend());
                        ^
  符号:   类 HashMapStateBackend
  位置: 类 TempValida
- **错误行**: 7

**问题 #5** (第 402 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3s8on9egTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp3s8on
- **错误行**: 3

**问题 #8** (第 513 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_75bk42jEventTypeInfo.java:23: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Tuple2<String, Integer>> keyedStream = stream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 23

**问题 #9** (第 711 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfhvbumt3TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #10** (第 777 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp79g0g7qxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp79g
- **错误行**: 3

**问题 #11** (第 824 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp64f1zbsxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp64f1zbs
- **错误行**: 3


### `Knowledge\05-migrations\kafka-streams-to-flink-guide.md`

**问题 #9** (第 470 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4wi6njauTempValidation.java:4: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #10** (第 486 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn910s9huTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpn910s9huTempValidat
- **错误行**: 4

**问题 #11** (第 532 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjspuen1iTempValidation.java:4: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #12** (第 549 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpym1sh5p_TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpym1sh5p_TempValidat
- **错误行**: 4

**问题 #13** (第 593 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxijljgooTempValidation.java:4: 错误: 找不到符号
KStream<String, Click> clicks = builder.stream("clicks");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #14** (第 605 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp87_q7knnTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp87_
- **错误行**: 3

**问题 #15** (第 618 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6if2kwi6TempValidation.java:4: 错误: 找不到符号
KTable<Windowed<String>, Long> slidingCounts = clicks
^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #16** (第 628 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgu9wcg_pTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpgu9
- **错误行**: 3

**问题 #17** (第 641 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxcsdxxerTempValidation.java:4: 错误: 找不到符号
KTable<Windowed<String>, Long> sessionCounts = clicks
^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #18** (第 651 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi1fstydfTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpi1f
- **错误行**: 3

**问题 #21** (第 759 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdog8c9mwTempValidation.java:3: 错误: 找不到符号
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "my-streams-app");
                  ^
  符号:   变量 StreamsConfig
  位
- **错误行**: 3

**问题 #22** (第 766 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_l_jhskpTempValidation.java:3: 错误: 找不到符号
        env.execute("my-streams-app");  // 作业名称
        ^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 3

**问题 #23** (第 786 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp49h1u51mTempValidation.java:3: 错误: 找不到符号
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092");
                  ^
  符号:   变量 StreamsConfig
  位置
- **错误行**: 3

**问题 #24** (第 794 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpszb0d59_TempValidation.java:3: 错误: 找不到符号
        KafkaSource<String> source = KafkaSource.<String>builder()
        ^
  符号:   类 KafkaSource
  位置: 类 TempValidation

- **错误行**: 3

**问题 #25** (第 814 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptzof50joTempValidation.java:3: 错误: 找不到符号
        props.put(StreamsConfig.STATE_DIR_CONFIG, "/var/lib/kafka-streams");
                  ^
  符号:   变量 StreamsConfig

- **错误行**: 3

**问题 #26** (第 821 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpar1nl8x7TempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4

**问题 #27** (第 835 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoplgn1l_TempValidation.java:4: 错误: 找不到符号
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, "exactly_once_v2");
          ^
  符号:   变量 StreamsConfig
  位置: 类 Temp
- **错误行**: 4

**问题 #28** (第 845 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm_nuaxqcTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpm_nuaxq
- **错误行**: 3

**问题 #29** (第 867 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgg49xxfxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpgg49xxfxTempV
- **错误行**: 3

**问题 #32** (第 956 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkchzhyxkTempValidation.java:4: 错误: 找不到符号
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, "exactly_once_v2");
          ^
  符号:   变量 StreamsConfig
  位置: 类 Temp
- **错误行**: 4

**问题 #34** (第 1028 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc4x26cplTempValidation.java:4: 错误: 找不到符号
KStream<String, Event> repartitioned = events
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #35** (第 1042 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzgj16apqTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpzgj16apqTempValidat
- **错误行**: 4

**问题 #37** (第 1120 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_itwejovDualWriteValidation.java:44: 错误: 非法的表达式开始
            .setRecordSerializer(...)
                                 ^
C:\Users\luyan\AppData\Local\Temp\tmp_it
- **错误行**: 44

**问题 #44** (第 1365 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt898mfqwTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpt89
- **错误行**: 3

**问题 #47** (第 1464 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwucex55eTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpwucex55eTempValidat
- **错误行**: 4

**问题 #48** (第 1492 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2w5iwyxoTempValidation.java:3: 错误: 找不到符号
        KafkaSource<String> source = KafkaSource.<String>builder()
        ^
  符号:   类 KafkaSource
  位置: 类 TempValidation

- **错误行**: 3


### `Knowledge\06-frontier\ai-agent-streaming-architecture.md`

**问题 #9** (第 822 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjhhy5j2qTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpjhh
- **错误行**: 3


### `Knowledge\06-frontier\audio-stream-processing.md`

**问题 #2** (第 96 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx_7x0u9aTempValidation.java:3: 错误: 找不到符号
        DataStream<AudioFrame> audioStream = env
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppD
- **错误行**: 3


### `Knowledge\06-frontier\cloud-edge-continuum.md`

**问题 #5** (第 451 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp698lqn2zAdaptivePlacement.java:4: 错误: 找不到符号
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


### `Knowledge\06-frontier\mcp-protocol-formal-specification.md`

**问题 #5** (第 916 行, 语言: yaml)

- **错误**: found undefined alias '.amazonaws.com:443'
  in "<unicode string>", line 16, column 11:
            - *.amazonaws.com:443
              ^ (line: 16)
- **错误行**: 16


### `Knowledge\06-frontier\multimodal-stream-processing.md`

**问题 #2** (第 119 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgjmuhp7aTempValidation.java:3: 错误: 找不到符号
        DataStream<TextEvent> textStream = env
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3


### `Knowledge\06-frontier\multimodal-streaming-architecture.md`

**问题 #13** (第 533 行, 语言: java)

- **错误**: 括号不匹配: (=40, )=43


### `Knowledge\06-frontier\real-time-rag-architecture.md`

**问题 #4** (第 299 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9qjrhzubEmbeddingAsyncFn.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.async不存在
import org.apache.flink.streaming.api.functions.async.AsyncFunction;

- **错误行**: 1

**问题 #5** (第 315 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjyn3ut1xVectorBulkSink.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.sink不存在
import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;

- **错误行**: 1


### `Knowledge\06-frontier\realtime-ai-streaming-2026.md`

**问题 #16** (第 592 行, 语言: java)

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

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjd5bpa3oTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpjd5bpa3oTempValidat
- **错误行**: 4


### `Knowledge\06-frontier\realtime-inference-optimization-formal.md`

**问题 #9** (第 1043 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcspgowm7TempValidation.java:13: 错误: 需要')'或','
        maxWaitTime = 100ms,
                         ^
C:\Users\luyan\AppData\Local\Temp\tmpcspgowm7TempValidation.j
- **错误行**: 13


### `Knowledge\06-frontier\realtime-ml-inference\06.04.01-ml-model-serving.md`

**问题 #3** (第 232 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk4ff8wizTritonAsyncInference.java:42: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Prediction> predictions = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以启用 未命名
- **错误行**: 42

**问题 #4** (第 286 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbknnz2enTempValidation.java:4: 错误: 找不到符号
MapStateDescriptor<String, String> modelVersionState =
^
  符号:   类 MapStateDescriptor
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 4


### `Knowledge\06-frontier\realtime-ml-inference\06.04.02-feature-store-streaming.md`

**问题 #4** (第 250 行, 语言: sql)

- **错误**: 可能的语法问题: HOP(EVENT_TIME, INTERVAL '1' MINUTE, INTERVAL '5' ...


### `Knowledge\06-frontier\risingwave-integration-guide.md`

**问题 #6** (第 482 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptwumi6b1TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmptw
- **错误行**: 4

**问题 #10** (第 602 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppxgu9nhtTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmppxgu9nhtTempValidat
- **错误行**: 4

**问题 #16** (第 818 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmxsiqpg0TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpmxsiqpg0TempValidat
- **错误行**: 4

**问题 #20** (第 963 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6zeuyu4aTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp6zeuyu4aTempValidat
- **错误行**: 4

**问题 #31** (第 1381 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 7, column 1:
    flink savepoint <job-id>
    ^ (line: 7)
- **错误行**: 7


### `Knowledge\06-frontier\rust-streaming-ecosystem.md`

**问题 #13** (第 755 行, 语言: sql)

- **错误**: 可能的语法问题: -- 返回: 10000.00 (严格串行化保证)

-- 即使在高并发写入下,也不会读到中间状态
...


### `Knowledge\06-frontier\serverless-streaming-formal-theory.md`

**问题 #1** (第 871 行, 语言: python)

- **错误**: SyntaxError: invalid character '→' (U+2192)
- **错误行**: 4


### `Knowledge\06-frontier\streaming-access-control.md`

**问题 #9** (第 670 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdb2b1kimLineageTracker.java:4: 错误: 找不到符号
    void track(DataRecord record, Operator op) {
               ^
  符号:   类 DataRecord
  位置: 类 LineageTracker
C:\Users\luy
- **错误行**: 4

**问题 #13** (第 777 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkfmktpkaLineageTrackingFunction.java:1: 错误: 程序包org.apache.flink.streaming.api.functions不存在
import org.apache.flink.streaming.api.functions.ProcessFunction;

- **错误行**: 1


### `Knowledge\06-frontier\streaming-database-ecosystem-comparison.md`

**问题 #6** (第 517 行, 语言: sql)

- **错误**: 可能的语法问题: -- 图遍历递归(有限支持)
   WITH RECURSIVE PATHS AS (...)...


### `Knowledge\06-frontier\streaming-graph-processing-tgn.md`

**问题 #7** (第 347 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpam696hvjTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.graph.streaming.*;
^
C:\Users\luyan\AppData\Local\Temp\tmpam696hvjTempValidation.java:3: 错误: 需要
- **错误行**: 3


### `Knowledge\06-frontier\streaming-lakehouse-formal-theory.md`

**问题 #3** (第 811 行, 语言: sql)

- **错误**: 可能的语法问题: -- 历史数据自动适配新分区方案
-- 无需重写数据,通过隐藏分区实现...

**问题 #7** (第 887 行, 语言: sql)

- **错误**: 可能的语法问题: -- 批处理模式:历史数据分析
SET 'EXECUTION.RUNTIME-MODE' = 'BA...; 可能的语法问题: -- 流处理模式:实时指标计算
SET 'EXECUTION.RUNTIME-MODE' = 'ST...


### `Knowledge\06-frontier\streaming-materialized-view-architecture.md`

**问题 #7** (第 369 行, 语言: sql)

- **错误**: 可能的语法问题: -- 自动增量更新
-- 当SALES表发生INSERT/UPDATE/DELETE时,物化视图自动...


### `Knowledge\06-frontier\streaming-security-compliance.md`

**问题 #5** (第 446 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe_wuskycTempValidation.java:3: 错误: 不是语句
KafkaServer {
^
C:\Users\luyan\AppData\Local\Temp\tmpe_wuskycTempValidation.java:3: 错误: 需要';'
KafkaServer {
           ^
C:
- **错误行**: 3


### `Knowledge\06-frontier\streaming-slo-definition.md`

**问题 #4** (第 297 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1_p9pdr3TempValidation.java:4: 错误: 找不到符号
Counter slo_violations_total = Counter.build()
^
  符号:   类 Counter
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4


### `Knowledge\06-frontier\temporal-flink-layered-architecture.md`

**问题 #9** (第 622 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptkmoinvqTemporalStateLookup.java:5: 错误: 未命名类 是预览功能，默认情况下禁用。
public WorkflowState getWorkflowState() {
       ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 5


### `Knowledge\06-frontier\video-stream-analytics.md`

**问题 #2** (第 97 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfu4256v3TempValidation.java:3: 错误: 找不到符号
        DataStream<VideoFrame> videoStream = env
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppD
- **错误行**: 3

**问题 #4** (第 150 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 5


### `Knowledge\06-frontier\wasm-dataflow-patterns.md`

**问题 #26** (第 1399 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpii93sjamWasmMapFunction.java:22: 错误: 非法的表达式开始
        byte[] state = getRuntimeContext().getState(...).value();

- **错误行**: 22

**问题 #50** (第 2356 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdbq3647cWasmScalarFunction.java:12: 错误: 需要';'
    private val runtime = new WasmUdfRuntime()
                                              ^
C:\Users\luyan\AppData
- **错误行**: 12


### `Knowledge\06-frontier\web3-blockchain-streaming-architecture.md`

**问题 #7** (第 374 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfok7f4c4TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpfok7f4c4TempValidatio
- **错误行**: 4

**问题 #8** (第 423 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaurkm446TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpaurkm446TempValidat
- **错误行**: 4

**问题 #9** (第 486 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph2mvj8apTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmph2mvj8apTempValidat
- **错误行**: 4


### `Knowledge\07-best-practices\07.01-flink-production-checklist.md`

**问题 #3** (第 223 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsnarqh9wTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000); // 1分钟间隔
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpsnar
- **错误行**: 4

**问题 #4** (第 249 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpemudxpa9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpemu
- **错误行**: 3

**问题 #7** (第 374 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqulx_3fsTempValidation.java:4: 错误: 非法的表达式开始
private static final Logger LOG = LoggerFactory.getLogger(MyFunction.class);
^
C:\Users\luyan\AppData\Local\Temp\tmpqul
- **错误行**: 4

**问题 #11** (第 562 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbctatk5bTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(10000);  // 10s 间隔
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpbc
- **错误行**: 4

**问题 #12** (第 573 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqx_376qhTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(300000);  // 5min 间隔
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4


### `Knowledge\07-best-practices\07.02-performance-tuning-patterns.md`

**问题 #9** (第 352 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvy1rkc7eTempValidation.java:10: 错误: 需要';'
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

**问题 #8** (第 347 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1u4uzspyTempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `Knowledge\07-best-practices\07.05-security-hardening-guide.md`

**问题 #3** (第 213 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    security.kerberos.login.keytab:  ...
    ^ (line: 4)
found duplicate key "security.kerberos.login.contexts" with value "Cli
- **错误行**: 4

**问题 #13** (第 532 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnvhx4ut0TempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `Knowledge\07-best-practices\07.07-testing-strategies-complete.md`

**问题 #4** (第 142 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpis8oysglTempValidation.java:5: 错误: 需要';'
public void badTest() {
                   ^
C:\Users\luyan\AppData\Local\Temp\tmpis8oysglTempValidation.java:12: 错误: 需要';
- **错误行**: 5

**问题 #6** (第 232 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9jzyuoxlTempValidation.java:5: 错误: 需要';'
public void flakyTest() {
                     ^
C:\Users\luyan\AppData\Local\Temp\tmp9jzyuoxlTempValidation.java:13: 错误:
- **错误行**: 5

**问题 #7** (第 259 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeb2i5orvStatefulCounterTest.java:34: 错误: 需要')'或','
        harness.setup(new HashMapStateBackend()  // MemoryStateBackend已弃用,使用HashMapStateBackend

- **错误行**: 34


### `Knowledge\08-standards\streaming-data-governance.md`

**问题 #6** (第 203 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8gp5okycTempValidation.java:5: 错误: 不是语句
  "type": "record",
  ^
C:\Users\luyan\AppData\Local\Temp\tmp8gp5okycTempValidation.java:5: 错误: 需要';'
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

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp87l8n4ukMaskPII.java:18: 错误: 需要 class、interface、enum 或 record
SELECT
^
C:\Users\luyan\AppData\Local\Temp\tmp87l8n4ukMaskPII.java:20: 错误: 未结束的字符文字
    MaskPII(email
- **错误行**: 18


### `Knowledge\08-standards\streaming-security-compliance.md`

**问题 #7** (第 491 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnnme2do0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnnme2do0Temp
- **错误行**: 3

**问题 #10** (第 603 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf1hf1ujbTempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpf1
- **错误行**: 4


### `Knowledge\10-case-studies\CODE-RUNNABILITY-NOTES.md`

**问题 #1** (第 28 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprexiuu0eTempValidation.java:5: 错误: 找不到符号
env.setParallelism(100);  // 原为100,可根据TaskManager数量调整
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 5

**问题 #2** (第 59 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp08rubu_yTempValidation.java:5: 错误: 找不到符号
options.setConnectionTimeout(10);  // 网络不稳定时可增大
^
  符号:   变量 options
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 5

**问题 #3** (第 87 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4jupj18zTempValidation.java:5: 错误: 非法的表达式开始
kieFileSystem.write("src/main/resources/rules/fraud-rules.drl", ...)

- **错误行**: 5


### `Knowledge\10-case-studies\ecommerce\10.2.3-big-promotion-realtime-dashboard.md`

**问题 #19** (第 1529 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 9, column 12:
      websocket: {
               ^ (line: 9)
- **错误行**: 9
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `Knowledge\10-case-studies\finance\10.1.1-realtime-anti-fraud-system.md`

**问题 #3** (第 328 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmtrshnxcRealtimeAntiFraudEngine.java:196: 错误: 未命名变量 是预览功能，默认情况下禁用。
                .whenComplete((_, error) -> {
                               ^
  （请使用 --enable-p
- **错误行**: 196


### `Knowledge\10-case-studies\finance\10.1.4-realtime-payment-risk-control.md`

**问题 #8** (第 1028 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc11nyc_eRealtimePaymentRiskControlEngine.java:254: 错误: 未命名变量 是预览功能，默认情况下禁用。
                .whenComplete((_, error) -> {
                               ^
  （请使用 -
- **错误行**: 254

**问题 #9** (第 1421 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwzr6c63bTempValidation.java:4: 错误: 需要';'
       .withIdleness(Duration.ofMinutes(1))
                                           ^
1 个错误

- **错误行**: 4

**问题 #10** (第 1437 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptlkx82e_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmptlk
- **错误行**: 3


### `Knowledge\10-case-studies\finance\10.1.5-realtime-risk-control-platform.md`

**问题 #18** (第 1304 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvczxdf79TempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend backend = new RocksDBStateBackend(checkpointPath, true);
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempV
- **错误行**: 4

**问题 #19** (第 1326 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp17a60v3uTempValidation.java:5: 错误: 找不到符号
    input,
    ^
  符号:   变量 input
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp17a60v3uTempValidation.java:
- **错误行**: 5

**问题 #21** (第 1388 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9e3ya6gxTempValidation.java:5: 错误: 需要';'
public String getKey(TransactionEvent event) {
                    ^
C:\Users\luyan\AppData\Local\Temp\tmp9e3ya6gxTempVali
- **错误行**: 5

**问题 #25** (第 1470 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzhtmiyomTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpzhtmiyomTem
- **错误行**: 3

**问题 #26** (第 1484 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc7mnjr0kTempValidation.java:7: 错误: 找不到符号
       log.error("Process failed for event: {}", event, e);
                                                 ^
  符号:   变量
- **错误行**: 7

**问题 #27** (第 1497 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl5_m_zqbTempValidation.java:4: 错误: 需要';'
   public void close() {
                    ^
1 个错误

- **错误行**: 4


### `Knowledge\10-case-studies\iot\10.3.1-smart-manufacturing.md`

**问题 #4** (第 359 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi2r7jde2TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpi2r7jde2TempValidatio
- **错误行**: 4


### `Knowledge\10-case-studies\iot\10.3.3-predictive-maintenance-manufacturing.md`

**问题 #5** (第 650 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo0t_f42cTimeSeriesFeatureExtractor.java:1: 错误: 程序包org.apache.flink.streaming.api.functions不存在
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
- **错误行**: 1


### `Knowledge\10-case-studies\iot\10.3.5-smart-manufacturing-iot.md`

**问题 #13** (第 1419 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmparcujv5fTempValidation.java:4: 错误: 找不到符号
OpcUaClient client = OpcUaClient.create(
^
  符号:   类 OpcUaClient
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #14** (第 1463 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqgga8g29TempValidation.java:4: 错误: 找不到符号
DefaultConfigurableOptionsFactory optionsFactory =
^
  符号:   类 DefaultConfigurableOptionsFactory
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #17** (第 1577 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphl6zq4sdTimestampNormalizer.java:21: 错误: 需要 class、interface、enum 或 record
sensorReading.setTimestamp(
^
1 个错误

- **错误行**: 21

**问题 #18** (第 1629 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb2mtbp8kTempValidation.java:4: 错误: 找不到符号
   producer.send(record);  // 错误
                 ^
  符号:   变量 record
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #19** (第 1641 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjpovx3yvTempValidation.java:4: 错误: 找不到符号
   HikariConfig config = new HikariConfig();
   ^
  符号:   类 HikariConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #20** (第 1650 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn_ndlj8nTempValidation.java:4: 错误: 找不到符号
   ByteBuffer directBuffer = ByteBuffer.allocateDirect(1024 * 1024);
   ^
  符号:   类 ByteBuffer
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #22** (第 1688 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr10sgfs9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpr10sg
- **错误行**: 3

**问题 #23** (第 1703 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjntnz5xhTempValidation.java:4: 错误: 找不到符号
   try (OrtSession session = createSession()) {
        ^
  符号:   类 OrtSession
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #24** (第 1712 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpel7r_imaTempValidation.java:4: 错误: 有 'catch', 但是没有 'try'
   catch (Exception e) {
   ^
1 个错误

- **错误行**: 4


### `Knowledge\98-exercises\exercise-02-flink-basics.md`

**问题 #2** (第 94 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9hdszlc8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9hd
- **错误行**: 3

**问题 #3** (第 170 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg89iept9WordCount.java:205: 错误: 需要 class、interface、enum 或 record
*/
^
1 个错误

- **错误行**: 205

**问题 #5** (第 439 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyqinsw21TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpyqins
- **错误行**: 3


### `Knowledge\98-exercises\exercise-03-checkpoint-analysis.md`

**问题 #1** (第 60 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpub5bkrbhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpub5bkrb
- **错误行**: 3

**问题 #5** (第 382 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpectc51ndUnalignedCheckpointConfig.java:30: 错误: 需要 class、interface、enum 或 record
env.getCheckpointConfig().enableUnalignedCheckpoints();
^
C:\Users\luyan\AppData\Lo
- **错误行**: 30


### `Knowledge\98-exercises\exercise-05-pattern-implementation.md`

**问题 #1** (第 60 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_k8sk7kuTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp_k8sk
- **错误行**: 3

**问题 #2** (第 155 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu29831gqOrderEvent.java:121: 错误: 需要 class、interface、enum 或 record
import org.apache.flink.cep.CEP;
^
C:\Users\luyan\AppData\Local\Temp\tmpu29831gqOrderEvent.java:1
- **错误行**: 121


### `Knowledge\98-exercises\quick-ref-security-compliance.md`

**问题 #8** (第 296 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp39jh5dc0TempValidation.java:18: 错误: 需要';'
""")
    ^
C:\Users\luyan\AppData\Local\Temp\tmp39jh5dc0TempValidation.java:29: 错误: 需要';'
""")
    ^
2 个错误

- **错误行**: 18


### `Knowledge\98-exercises\quick-ref-temporal-flink.md`

**问题 #8** (第 370 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy169lbvlTemporalStateLookup.java:3: 错误: 未命名类 是预览功能，默认情况下禁用。
public WorkflowState getWorkflowState() {
       ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 3


### `Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.01-flink-2x-architecture.md`

**问题 #3** (第 292 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbczlqqfwTempValidation.java:4: 错误: 找不到符号
   state.getAsync(key)
                  ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpbczl
- **错误行**: 4

**问题 #5** (第 329 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8bsmrtr1TempValidation.java:4: 错误: 找不到符号
if (backpressureRatio > 0.5 && latencyP99 > targetLatency) {
    ^
  符号:   变量 backpressureRatio
  位置: 类 TempValidation
C:\
- **错误行**: 4


### `Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.02-flink-runtime-deep-dive.md`

**问题 #15** (第 532 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp008aoasvTempValidation.java:8: 错误: 非法的表达式开始
public void notifyCreditAvailable() {
^
C:\Users\luyan\AppData\Local\Temp\tmp008aoasvTempValidation.java:30: 错误: 需要 cla
- **错误行**: 8

**问题 #17** (第 603 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqi70n5ytTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.03-flink-state-backends.md`

**问题 #9** (第 302 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7kg9i8_dTempValidation.java:4: 错误: 不是语句
state.backend.rocksdb.writebuffer.size: 64mb
                                 ^
C:\Users\luyan\AppData\Local\Temp\tmp7kg9i8
- **错误行**: 4

**问题 #10** (第 318 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph94oa249TempValidation.java:5: 错误: 不是语句
state.backend.rocksdb.memory.managed: true
                            ^
C:\Users\luyan\AppData\Local\Temp\tmph94oa249TempV
- **错误行**: 5

**问题 #16** (第 479 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmc0vr64yTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #18** (第 535 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph7sdgq8mTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend = new EmbeddedRocksDBStateBackend(true);  // true=增量 Checkpoint
^
  符号:   类 Emb
- **错误行**: 4

**问题 #20** (第 587 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdfx7rzv7TempValidation.java:4: 错误: 找不到符号
ForStStateBackendConfig forstConfig = ForStStateBackendConfig.builder()
^
  符号:   类 ForStStateBackendConfig
  位置: 类 TempVa
- **错误行**: 4


### `Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.04-flink-sql-table-api.md`

**问题 #6** (第 138 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpednklarbTempValidation.java:4: 错误: 找不到符号
env.setRuntimeMode(RuntimeExecutionMode.STREAMING);
                   ^
  符号:   变量 RuntimeExecutionMode
  位置: 类 TempValid
- **错误行**: 4

**问题 #8** (第 282 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmwg9da13TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.functions.AggregateFunction;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #9** (第 306 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppzrtks21TempValidation.java:4: 错误: 非法的表达式开始
Filter -> Scan  =>  Scan(with Filter)
                 ^
C:\Users\luyan\AppData\Local\Temp\tmppzrtks21TempValidation.ja
- **错误行**: 4

**问题 #10** (第 319 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6ih8g3heTempValidation.java:4: 错误: 需要';'
A JOIN B JOIN C  =>  选择代价最低的 Join 顺序
      ^
C:\Users\luyan\AppData\Local\Temp\tmp6ih8g3heTempValidation.java:4: 错误: 需要';'
- **错误行**: 4

**问题 #11** (第 346 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp15te909yMLPredictUDF.java:11: 错误: 需要 class、interface、enum 或 record
AsyncFunction 调用 REST API,延迟 10-100ms
^
1 个错误

- **错误行**: 11

**问题 #13** (第 427 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiyh44htpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.Table;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpiyh44htpTempValidation.
- **错误行**: 3

**问题 #15** (第 513 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8sgr516xTempValidation.java:4: 错误: 找不到符号
TableConfig config = tableEnv.getConfig();
^
  符号:   类 TableConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #17** (第 597 行, 语言: sql)

- **错误**: 可能的语法问题: -- 4. 模型性能监控
DESCRIBE MODEL METRICS FRAUD_DETECTIO...; 可能的语法问题: -- 显示: AVG_INFERENCE_LATENCY, THROUGHPUT, ERROR_RA...

**问题 #18** (第 673 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc9w99dt1TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpc9w
- **错误行**: 3

**问题 #19** (第 715 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbco0991cTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.05-flink-cloud-native.md`

**问题 #7** (第 290 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcgvhd_dkTempValidation.java:4: 错误: 找不到符号
if (backpressureRatio > scaleUpThreshold ||
    ^
  符号:   变量 backpressureRatio
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4


### `Knowledge\Flink-Scala-Rust-Comprehensive\03-scala-rust-interop\03.01-wasm-interop.md`

**问题 #8** (第 306 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe3vlirudTempValidation.java:4: 错误: 非法的表达式开始
public record Input(long id, byte[] payload) {}
^
C:\Users\luyan\AppData\Local\Temp\tmpe3vlirudTempValidation.java:7: 错
- **错误行**: 4


### `Knowledge\Flink-Scala-Rust-Comprehensive\04-rust-engines\04.02-risingwave-deep-dive.md`

**问题 #9** (第 487 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5kemblfhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5ke
- **错误行**: 3


### `Knowledge\Flink-Scala-Rust-Comprehensive\04-rust-engines\04.03-materialize-analysis.md`

**问题 #7** (第 280 行, 语言: sql)

- **错误**: 可能的语法问题: -- 强一致性保证:余额始终准确,不会出现负余额(假设有约束)...

**问题 #11** (第 424 行, 语言: sql)

- **错误**: 可能的语法问题: -- 支持递归 CTE
WITH RECURSIVE CHAIN AS (
    SELECT *...

**问题 #12** (第 446 行, 语言: sql)

- **错误**: 可能的语法问题: -- 不支持递归 CTE,需外部处理...

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

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7m0v_tjtTempValidation.java:3: 错误: 非法的表达式开始
public CompletableFuture<CompletedCheckpoint> triggerCheckpoint(
^
C:\Users\luyan\AppData\Local\Temp\tmp7m0v_tjtTempVal
- **错误行**: 3

**问题 #4** (第 180 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc6akq1l2TempValidation.java:3: 错误: 非法的表达式开始
public boolean receiveAcknowledgeMessage(
^
C:\Users\luyan\AppData\Local\Temp\tmpc6akq1l2TempValidation.java:69: 错误: 需要
- **错误行**: 3

**问题 #5** (第 258 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_eh1i2luPendingCheckpoint.java:56: 错误: 非法的表达式开始
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

**问题 #10** (第 807 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgo61uvswBlockingBackPressure.java:4: 错误: 非法的类型开始
    public void emitRecord(...) {
                           ^
C:\Users\luyan\AppData\Local\Temp\tmpgo61uvswBlocki
- **错误行**: 4


### `Knowledge\Flink-Scala-Rust-Comprehensive\src-analysis\flink-runtime-architecture.md`

**问题 #3** (第 74 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3cpxthv9TempValidation.java:3: 错误: 非法的表达式开始
private void startJobExecution() {
^
C:\Users\luyan\AppData\Local\Temp\tmp3cpxthv9TempValidation.java:27: 错误: 需要 class、
- **错误行**: 3

**问题 #4** (第 101 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2ree8vy2TempValidation.java:4: 错误: 需要';'
public void notifyAllocationFailure(
                                   ^
C:\Users\luyan\AppData\Local\Temp\tmp2ree8vy2Tem
- **错误行**: 4

**问题 #7** (第 181 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpknkvyce0TempValidation.java:4: 错误: 需要';'
public CompletableFuture<Acknowledge> requestSlot(
                                                 ^
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #8** (第 218 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_oppp6u7TempValidation.java:3: 错误: 非法的表达式开始
protected abstract CompletableFuture<WorkerType> requestNewWorker(
^
C:\Users\luyan\AppData\Local\Temp\tmp_oppp6u7TempV
- **错误行**: 3

**问题 #11** (第 311 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpypx40z4kTempValidation.java:4: 错误: 需要';'
public CompletableFuture<Acknowledge> submitJob(
                                               ^
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #12** (第 350 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpynpsw_ifTempValidation.java:3: 错误: 非法的表达式开始
private void onJobManagerRunnerComplete(
^
C:\Users\luyan\AppData\Local\Temp\tmpynpsw_ifTempValidation.java:33: 错误: 需要
- **错误行**: 3

**问题 #17** (第 528 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpezin6vmfTempValidation.java:3: 错误: 非法的表达式开始
public ExecutionGraph buildExecutionGraph(JobGraph jobGraph) {
^
C:\Users\luyan\AppData\Local\Temp\tmpezin6vmfTempValid
- **错误行**: 3

**问题 #18** (第 632 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpio0_hi5dPipelinedRegionScheduler.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
public SchedulerNG createScheduler(
       ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 1

**问题 #19** (第 718 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp309xnoy3JobManager.java:8: 错误: 找不到符号
    SchedulerNG scheduler;  // 可插拔调度器
    ^
  符号:   类 SchedulerNG
  位置: 类 JobMaster
C:\Users\luyan\AppData\Local\Temp\tmp309xn
- **错误行**: 8

**问题 #21** (第 785 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp9w5w0i0SlotPoolImpl.java:7: 错误: 找不到符号
    private void requestSlotsBatch(List<SlotRequest> requests) {
                                        ^
  符号:   类 SlotReq
- **错误行**: 7


### `Knowledge\Flink-Scala-Rust-Comprehensive\src-analysis\flink-taskmanager-deep-dive.md`

**问题 #3** (第 97 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppzyib81eTempValidation.java:4: 错误: 需要';'
public CompletableFuture<Acknowledge> submitTask(
                                                ^
C:\Users\luyan\AppData
- **错误行**: 4

**问题 #4** (第 177 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpexvuzva5TempValidation.java:4: 错误: 需要';'
public CompletableFuture<Acknowledge> freeSlot(
                                              ^
C:\Users\luyan\AppData\Loc
- **错误行**: 4


### `Knowledge\case-studies\ecommerce-realtime-recommendation-v2.md`

**问题 #2** (第 253 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkn6p6ubkTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpkn6p6ubkTempValidat
- **错误行**: 4

**问题 #3** (第 317 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaj0f4mtxAsyncModelInference.java:47: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Prediction> predictions = featureStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 47


### `Knowledge\case-studies\finance\realtime-anti-fraud-system-case.md`

**问题 #2** (第 198 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwwws7n2hTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpwwws7n2hTempValidat
- **错误行**: 4

**问题 #3** (第 265 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppk4vy96cTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmppk4vy96cTempValidat
- **错误行**: 4


### `Knowledge\case-studies\fraud-detection-production-case.md`

**问题 #2** (第 262 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcoj58tgmTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpcoj58tgmTempValidatio
- **错误行**: 4

**问题 #3** (第 371 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxmyzzebkGNNInferenceFunction.java:92: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<TransactionWithRisk> gnnScores = transactions
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 92


### `Knowledge\case-studies\gaming-analytics-platform-case.md`

**问题 #2** (第 281 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1xkp_qh_TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp1xkp_qh_TempValidat
- **错误行**: 4

**问题 #3** (第 410 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe8lsnqeeABTestAssignment.java:53: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<ABTestResult> abResults = eventsWithVariant
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 53


### `Knowledge\case-studies\gaming\realtime-game-analytics-case.md`

**问题 #2** (第 182 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpss7nuvp0TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpss7nuvp0TempValidat
- **错误行**: 4

**问题 #4** (第 333 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd2anepq_TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpd2anepq_TempValidatio
- **错误行**: 4


### `Knowledge\case-studies\iot-smart-grid-case-study.md`

**问题 #2** (第 268 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptp_d126jTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmptp_d126jTempValidat
- **错误行**: 4

**问题 #3** (第 352 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv30qdfvtTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpv30qdfvtTempValidat
- **错误行**: 4


### `Knowledge\cep-complete-tutorial.md`

**问题 #4** (第 229 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpskfflrg7TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.Pattern;
^
C:\Users\luyan\AppData\Local\Temp\tmpskfflrg7TempValidation.java:3: 错误: 不是语句
imp
- **错误行**: 3

**问题 #5** (第 285 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph6q1wanzTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmph6q1wanzTempValidatio
- **错误行**: 4

**问题 #6** (第 330 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph6h0_8pxTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmph6h0_8pxTempValidatio
- **错误行**: 4


### `Knowledge\exactly-once-comparison.md`

**问题 #3** (第 247 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkbstrvbqTempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #4** (第 263 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt6eq1h06TempValidation.java:3: 错误: 找不到符号
        props.put("transactional.id", "my-transactional-id");
        ^
  符号:   变量 props
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 3


### `Knowledge\feature-lineage-tracking.md`

**问题 #3** (第 291 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwbl3kzwbTempValidation.java:4: 错误: 找不到符号
env.getConfig().setJobListener(new OpenLineageJobListener());
                                   ^
  符号:   类 OpenLineageJo
- **错误行**: 4


### `Knowledge\kafka-streams-migration.md`

**问题 #6** (第 145 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy54j8p69TempValidation.java:3: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3

**问题 #7** (第 158 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4bh74smvTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp4bh74smvTempValidat
- **错误行**: 4

**问题 #8** (第 185 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_64j61z4TempValidation.java:3: 错误: 找不到符号
        KTable<Windowed<String>, Long> counts = orders
        ^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3


### `Knowledge\llm-query-rewrite.md`

**问题 #8** (第 279 行, 语言: python)

- **错误**: SyntaxError: unterminated triple-quoted f-string literal (detected at line 11)
- **错误行**: 9


### `Knowledge\llm-stream-diagnosis.md`

**问题 #3** (第 252 行, 语言: python)

- **错误**: SyntaxError: unterminated triple-quoted f-string literal (detected at line 16)
- **错误行**: 13


### `Knowledge\stream-feature-computation.md`

**问题 #3** (第 370 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0432qnblTempValidation.java:3: 错误: 找不到符号
Pattern<UserBehaviorEvent, ?> purchaseIntent = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 3

**问题 #4** (第 405 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl4306ei6TempValidation.java:3: 错误: 找不到符号
DataStream<PriceSensitiveFeature> priceSensitiveFeatures = behaviorStream
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:
- **错误行**: 3


### `Knowledge\temporal-kg-reasoning.md`

**问题 #3** (第 297 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprh8wevn3TempValidation.java:4: 错误: 找不到符号
DataStream<TemporalQuery> queries = env.addSource(new QuerySource());
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Use
- **错误行**: 4


### `Knowledge\timestamp-aware-caching.md`

**问题 #3** (第 186 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbj0b3sq0TempValidation.java:4: 错误: 找不到符号
RocksDBStateBackendConfig config = new RocksDBStateBackendConfig();
^
  符号:   类 RocksDBStateBackendConfig
  位置: 类 TempVali
- **错误行**: 4


### `LEARNING-PATHS\beginner-quick-start.md`

**问题 #3** (第 125 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpue7so85mTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpue7so85mTem
- **错误行**: 3

**问题 #5** (第 228 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl0r8_75tTempValidation.java:7: 错误: 非法的表达式开始
private transient Counter eventCounter;
^
C:\Users\luyan\AppData\Local\Temp\tmpl0r8_75tTempValidation.java:17: 错误: 需要 c
- **错误行**: 7

**问题 #6** (第 264 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpms3p_uzsTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `LEARNING-PATHS\beginner-with-foundation.md`

**问题 #4** (第 198 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwkwv2ze2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwkwv2ze
- **错误行**: 3


### `LEARNING-PATHS\certifications\custom-assessment.md`

**问题 #5** (第 178 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt3o2cgx3OrderTimeoutDetection.java:191: 错误: 需要 class、interface、enum 或 record
*/
^
1 个错误

- **错误行**: 191

**问题 #6** (第 374 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6h_9rpdzDynamicRiskControlEngine.java:336: 错误: 需要 class、interface、enum 或 record
*/
^
1 个错误

- **错误行**: 336


### `LEARNING-PATHS\certifications\ververica-certification.md`

**问题 #2** (第 69 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnhs1lvu3TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnhs
- **错误行**: 3

**问题 #4** (第 133 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd9z8ouj1TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpd9z8ouj
- **错误行**: 3

**问题 #5** (第 153 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpipc_gji5TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpipc_gji5Tem
- **错误行**: 3

**问题 #6** (第 182 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsanw773uTempValidation.java:4: 错误: 找不到符号
WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                   ^
  符号:   类 Event
  位置: 类 Temp
- **错误行**: 4


### `LEARNING-PATHS\expert-performance-tuning.md`

**问题 #2** (第 79 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9w5enniwTempValidation.java:6: 错误: 找不到符号
      .addSink(new SlowSink());  // 故意降低处理速度
                   ^
  符号:   类 SlowSink
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 6

**问题 #4** (第 142 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn9x6ffgwTempValidation.java:4: 错误: 找不到符号
   env.getConfig().setBufferTimeout(0);  // 零缓冲延迟
   ^
  符号:   变量 env
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #8** (第 251 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8dkbhxrrTempValidation.java:4: 错误: 找不到符号
env.getCheckpointConfig().enableUnalignedCheckpoints();
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #11** (第 294 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3qlehgrwTempValidation.java:4: 错误: 程序包ElasticsearchSink不存在
   ElasticsearchSink.Builder<LogEvent> builder =
                    ^
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4


### `LEARNING-PATHS\industry-finance-realtime.md`

**问题 #4** (第 223 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpugsz245uTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpugsz2
- **错误行**: 3


### `LEARNING-PATHS\industry-iot-data-processing.md`

**问题 #3** (第 147 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvca3bhjoTempValidation.java:7: 错误: 找不到符号
  .setDeserializer(new SensorDataDeserializer())
                       ^
  符号:   类 SensorDataDeserializer
  位置: 类 TempVal
- **错误行**: 7


### `LEARNING-PATHS\intermediate-datastream-expert.md`

**问题 #4** (第 227 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpik34p4haTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.state.ValueState;
^
C:\Users\luyan\AppData\Local\Temp\tmpik34p4haTempValidation.java
- **错误行**: 4


### `LEARNING-PATHS\intermediate-sql-expert.md`

**问题 #9** (第 281 行, 语言: sql)

- **错误**: 可能的语法问题: -- 1. 使用 MINI-BATCH 优化聚合
SET TABLE.EXEC.MINI-BATCH...; 可能的语法问题: -- 2. 使用 LOCAL-GLOBAL 优化
SET TABLE.OPTIMIZER.AGG-P...


### `LEARNING-PATHS\intermediate-state-management-expert.md`

**问题 #2** (第 79 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_uwf_0teTempValidation.java:4: 错误: 找不到符号
   env.setStateBackend(new HashMapStateBackend());
                           ^
  符号:   类 HashMapStateBackend
  位置: 类 Temp
- **错误行**: 4

**问题 #5** (第 270 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplkg29pf_TempValidation.java:4: 错误: 需要';'
   stream.keyBy(event -> event.getUserId() % 1000)
                                                  ^
1 个错误

- **错误行**: 4

**问题 #6** (第 278 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbx5_om_tTempValidation.java:4: 错误: 找不到符号
   DefaultConfigurableStateBackend stateBackend =
   ^
  符号:   类 DefaultConfigurableStateBackend
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #7** (第 289 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0otxowwdTempValidation.java:4: 错误: 找不到符号
     new FileSystemCheckpointStorage("hdfs:///checkpoints")
         ^
  符号:   类 FileSystemCheckpointStorage
  位置: 类 TempV
- **错误行**: 4

**问题 #8** (第 321 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb6yqdyeuTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpb6yqdyeuTem
- **错误行**: 3

**问题 #9** (第 338 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvjpug35oTempValidation.java:4: 错误: 非法的表达式开始
public void processBatch(List<Event> events) {
^
C:\Users\luyan\AppData\Local\Temp\tmpvjpug35oTempValidation.java:5: 错误
- **错误行**: 4


### `POSITIONING.md`

**问题 #5** (第 219 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx98d8xyhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpx98d8xy
- **错误行**: 3


### `PRACTICAL-EXAMPLES.md`

**问题 #2** (第 43 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3wp41cf3TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp3wp
- **错误行**: 3

**问题 #3** (第 59 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1lljh60zTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1ll
- **错误行**: 3

**问题 #4** (第 77 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr2a02yxmTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpr2a02
- **错误行**: 3


### `Struct\01-foundation\01.04-dataflow-model-formalization.md`

**问题 #1** (第 392 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdg7dbtr2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpdg7
- **错误行**: 3


### `Struct\02-properties\02.01-determinism-in-streaming.md`

**问题 #3** (第 497 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdd5o0s0rTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpdd5
- **错误行**: 3

**问题 #4** (第 533 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvmyjaa90TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpvmyjaa90TempValidat
- **错误行**: 4

**问题 #5** (第 556 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpktgfxndmTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpktg
- **错误行**: 3

**问题 #6** (第 574 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3g5736muTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp3g5736muTempValidat
- **错误行**: 4


### `Struct\02-properties\02.02-consistency-hierarchy.md`

**问题 #1** (第 656 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8_6itku5TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8_6
- **错误行**: 3

**问题 #3** (第 730 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf_exeyklHttpSink.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.sink不存在
import org.apache.flink.streaming.api.functions.sink.SinkFunction;

- **错误行**: 1

**问题 #4** (第 754 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkj7b__zyEagerKafkaSource.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.source不存在
import org.apache.flink.streaming.api.functions.source.SourceFunction;

- **错误行**: 1


### `Struct\02-properties\02.03-watermark-monotonicity.md`

**问题 #1** (第 315 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8740shfjTempValidation.java:4: 错误: 非法的表达式开始
public void onWatermark(Watermark wm, Context ctx, Collector<Out> out) {
^
C:\Users\luyan\AppData\Local\Temp\tmp8740shf
- **错误行**: 4


### `Struct\03-relationships\03.02-flink-to-process-calculus.md`

**问题 #1** (第 418 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp40f1agsiTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp40f
- **错误行**: 3

**问题 #3** (第 492 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyv2128vcTempValidation.java:4: 错误: 找不到符号
countState.update(countState.value() + 1);
                  ^
  符号:   变量 countState
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4


### `Struct\03-relationships\03.05-cross-model-mappings.md`

**问题 #6** (第 557 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9hyyymzjTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9hy
- **错误行**: 3


### `Struct\04-proofs\04.02-flink-exactly-once-correctness.md`

**问题 #5** (第 732 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmj4frqm9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpmj4
- **错误行**: 3

**问题 #6** (第 774 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp64ezfb9fTempValidation.java:4: 错误: 找不到符号
StreamingFileSink<Result> sink = StreamingFileSink
^
  符号:   类 StreamingFileSink
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4

**问题 #7** (第 797 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9t_i7z8uCounterSink.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.sink不存在
import org.apache.flink.streaming.api.functions.sink.SinkFunction;

- **错误行**: 1

**问题 #8** (第 825 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9yo69ld0EagerKafkaSource.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.source不存在
import org.apache.flink.streaming.api.functions.source.SourceFunction;

- **错误行**: 1


### `Struct\04-proofs\04.04-watermark-algebra-formal-proof.md`

**问题 #2** (第 781 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjdd_api4TempValidation.java:4: 错误: 找不到符号
Watermark currentOutput = mergeAllInputWatermarks();
^
  符号:   类 Watermark
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #5** (第 1131 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2hl6f96cTempValidation.java:3: 错误: 非法的表达式开始
public void onWatermark(Watermark wm, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmp2hl6f96cTempValidation.java
- **错误行**: 3

**问题 #6** (第 1209 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu6mzxn2gTempValidation.java:3: 错误: 非法的表达式开始
public void onWatermark(Watermark wm, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpu6mzxn2gTempValidation.java
- **错误行**: 3


### `Struct\04-proofs\04.07-deadlock-freedom-choreographic.md`

**问题 #1** (第 246 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl8epl5ueBuyTicket.java:2: 错误: 需要'{'
class BuyTicket@Buyer,Seller {
               ^
C:\Users\luyan\AppData\Local\Temp\tmpl8epl5ueBuyTicket.java:2: 错误: 需要 class、int
- **错误行**: 2

**问题 #9** (第 932 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8o45_yszRequestResponse.java:1: 错误: 需要'{'
class RequestResponse@Client,Server {
                     ^
C:\Users\luyan\AppData\Local\Temp\tmp8o45_yszRequestResponse
- **错误行**: 1

**问题 #10** (第 952 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp45i3q5zqClientRequestResponse.java:3: 错误: 找不到符号
        sendToServer(request);
        ^
  符号:   方法 sendToServer(String)
  位置: 类 ClientRequestResponse
C:\Users\luy
- **错误行**: 3

**问题 #11** (第 963 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyai1jezdServerRequestResponse.java:3: 错误: 找不到符号
        String request = receiveFromClient();
                         ^
  符号:   方法 receiveFromClient()
  位置: 类 Ser
- **错误行**: 3

**问题 #12** (第 987 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpohrtgeheAuction.java:1: 错误: 需要'{'
class Auction@Buyer,Seller,Arbiter {
             ^
C:\Users\luyan\AppData\Local\Temp\tmpohrtgeheAuction.java:1: 错误: 需要 class、int
- **错误行**: 1


### `Struct\05-comparative-analysis\05.04-concurrency-models-2025-comparison.md`

**问题 #7** (第 612 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq44tq5laTempValidation.java:4: 错误: 非法的表达式开始
void bad() {
^
C:\Users\luyan\AppData\Local\Temp\tmpq44tq5laTempValidation.java:4: 错误: 需要';'
void bad() {
        ^
C:\
- **错误行**: 4


### `Struct\06-frontier\06.02-choreographic-streaming-programming.md`

**问题 #8** (第 541 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpryrhf6htTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpryr
- **错误行**: 3

**问题 #14** (第 694 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9ji30sc_JoinOp.java:11: 错误: 不是语句
            select {
            ^
C:\Users\luyan\AppData\Local\Temp\tmp9ji30sc_JoinOp.java:11: 错误: 需要';'
            select {

- **错误行**: 11


### `Struct\06-frontier\calvin-deterministic-streaming.md`

**问题 #2** (第 680 行, 语言: sql)

- **错误**: 可能的语法问题: IF (SELECT BALANCE FROM ACCOUNTS WHERE ID = 1) > 1...; 可能的语法问题: ELSE
       UPDATE ACCOUNTS SET BALANCE = BALANCE ...

**问题 #5** (第 1165 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpus7re6n_TempValidation.java:3: 错误: 非法的表达式开始
        DataStream<Order> orders = ...;
                                   ^
1 个错误

- **错误行**: 3

**问题 #7** (第 1212 行, 语言: sql)

- **错误**: 可能的语法问题: -- T: 用户下单购买商品
BEGIN;...; 可能的语法问题: -- 如果库存充足，扣减库存并创建订单
  IF STOCK > 0 THEN
    UPDATE...; 可能的语法问题: -- 动态：如果库存降至 0，触发补货通知
    IF NEW_STOCK == 0 THEN
 ...; 可能的语法问题: ELSE
    ROLLBACK;...


### `Struct\06-frontier\complex-event-processing-formal-theory.md`

**问题 #13** (第 1119 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsbqc12ugTempValidation.java:3: 错误: 找不到符号
        Pattern<Event, ?> pattern = Pattern
        ^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 3


### `Struct\06-frontier\dbsp-theory-framework.md`

**问题 #8** (第 983 行, 语言: sql)

- **错误**: 可能的语法问题: -- 内部使用 DBSP 理论维护：
-- 1. 为 R.ID 和 S.RID 维护 ARRANGE...

**问题 #20** (第 1243 行, 语言: sql)

- **错误**: 可能的语法问题: -- DBSP 语义: 通过 LOOP 算子维护传递闭包的增量更新...


### `Struct\06-frontier\graph-streaming-formal-theory.md`

**问题 #21** (第 1641 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfa_7x1zcStreamingGraphEnvironment.java:27: 错误: 非法的表达式开始
            .getState(new ValueStateDescriptor<>("vertexValue", ...));

- **错误行**: 27


### `Struct\06-frontier\streaming-lakehouse-formal-theory.md`

**问题 #25** (第 1305 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph_glxxfrTempValidation.java:11: 错误: 找不到符号
    .setFileFormat(FileFormat.PARQUET)
                   ^
  符号:   变量 FileFormat
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 11


### `Struct\07-tools\model-checking-guided-testing.md`

**问题 #4** (第 213 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppca2ckkdTempValidation.java:4: 错误: 需要';'
public void testCheckpointCompletionRace() {
                                        ^
1 个错误

- **错误行**: 4


### `Struct\Model-Selection-Decision-Tree.md`

**问题 #6** (第 388 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqrhw33xzTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpqrhw33xzTempValidatio
- **错误行**: 4


### `Struct\Proof-Chains-Consistency-Hierarchy.md`

**问题 #2** (第 725 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvnh8g0szTempValidation.java:5: 错误: 找不到符号
    .<ClickEvent>forBoundedOutOfOrderness(Duration.ofMinutes(1))
      ^
  符号:   类 ClickEvent
  位置: 类 TempValidation
C:\Us
- **错误行**: 5

**问题 #3** (第 750 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkc5fnut9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpkc5fnut
- **错误行**: 3


### `Struct\Proof-Chains-Dataflow-Foundation.md`

**问题 #2** (第 611 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa_s6qbyfTempValidation.java:4: 错误: 找不到符号
StreamGraph streamGraph = env.getStreamGraph();
^
  符号:   类 StreamGraph
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #3** (第 636 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt9x53j4wTempValidation.java:4: 错误: 找不到符号
CheckpointCoordinator.triggerCheckpoint(timestamp);
                                        ^
  符号:   变量 timestamp
  位置: 类
- **错误行**: 4

**问题 #4** (第 648 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa2zt39l9TempValidation.java:9: 错误: 找不到符号
    .aggregate(aggregateFunction); // 状态算子结合律检查
               ^
  符号:   变量 aggregateFunction
  位置: 类 TempValidation
C:\Us
- **错误行**: 9

**问题 #5** (第 662 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3gg5mzfnPureMapFunction.java:17: 错误: 需要 class、interface、enum 或 record
stream.assignTimestampsAndWatermarks(
^
C:\Users\luyan\AppData\Local\Temp\tmp3gg5mzfnPureMapF
- **错误行**: 17

**问题 #6** (第 707 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprs80_2p7TempValidation.java:4: 错误: 需要';'
public void testDeterminism() {
                           ^
C:\Users\luyan\AppData\Local\Temp\tmprs80_2p7TempValidation.j
- **错误行**: 4


### `Struct\Proof-Chains-Flink-Complete.md`

**问题 #3** (第 452 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmj0tvkpcTempValidation.java:4: 错误: 找不到符号
    inputStream,
    ^
  符号:   变量 inputStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpmj0tvkpcTempVali
- **错误行**: 4


### `Struct\Proof-Chains-Flink-Implementation.md`

**问题 #24** (第 506 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0edqjr63TempValidation.java:4: 错误: 非法的表达式开始
public void triggerCheckpoint(long timestamp) {
^
C:\Users\luyan\AppData\Local\Temp\tmp0edqjr63TempValidation.java:15:
- **错误行**: 4

**问题 #25** (第 521 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphbh0gw91TempValidation.java:4: 错误: 非法的表达式开始
public final void snapshotState(StateSnapshotContext context) {
^
C:\Users\luyan\AppData\Local\Temp\tmphbh0gw91TempVali
- **错误行**: 4

**问题 #26** (第 535 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaivdgrtcTempValidation.java:4: 错误: 非法的表达式开始
private void processElement(StreamRecord<IN> element) {
^
C:\Users\luyan\AppData\Local\Temp\tmpaivdgrtcTempValidation.j
- **错误行**: 4

**问题 #27** (第 552 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4glt9d3bTempValidation.java:4: 错误: 非法的表达式开始
public void emitCompletedElement() {
^
C:\Users\luyan\AppData\Local\Temp\tmp4glt9d3bTempValidation.java:13: 错误: 需要 clas
- **错误行**: 4


### `Struct\Unified-Model-Relationship-Graph.md`

**问题 #5** (第 245 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9b4s_kdzTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9b4
- **错误行**: 3


### `Struct\bounded-staleness.md`

**问题 #4** (第 301 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplic47mw6TempValidation.java:4: 错误: 找不到符号
StateBackendConfig config = new RocksDBStateBackendConfig();
^
  符号:   类 StateBackendConfig
  位置: 类 TempValidation
C:\User
- **错误行**: 4


### `Struct\serverless-ml-inference.md`

**问题 #2** (第 142 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2


### `Struct\speculative-stream-ordering.md`

**问题 #4** (第 365 行, 语言: sql)

- **错误**: 可能的语法问题: -- 若某 USER_EVENTS 记录被撤销（如上游 CDC 事务回滚），
-- MATERIAL...


### `Struct\transactional-stream-semantics.md`

**问题 #2** (第 199 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptpqncdwaTempValidation.java:4: 错误: 非法的表达式开始
public void processElement(Order order, Context ctx, Collector<Result> out) {
^
C:\Users\luyan\AppData\Local\Temp\tmptp
- **错误行**: 4


### `TECH-RADAR\migration-recommendations.md`

**问题 #4** (第 121 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5m2jer29WordCountBolt.java:20: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Tuple2<String, Integer>> wordCounts =
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 20


### `TOOLCHAIN.md`

**问题 #17** (第 464 行, 语言: yaml)

- **错误**: could not determine a constructor for the tag 'tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format'
  in "<unicode string>", line 43, column 19:
              format: !!python/name:py
- **错误行**: 43


### `TROUBLESHOOTING.md`

**问题 #6** (第 193 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpffzk6mn4SyncFunction.java:22: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Result> result = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 22

**问题 #8** (第 269 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5apj9enfTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5ap
- **错误行**: 3

**问题 #10** (第 337 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcq2l85eqTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpcq2l85eqTempValidat
- **错误行**: 4

**问题 #16** (第 578 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpstwj8xv5TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpstw
- **错误行**: 3


### `USTM-F-Reconstruction\02-model-instantiation\02.00-model-instantiation-framework.md`

**问题 #11** (第 606 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq3kitatmTempValidation.java:6: 错误: 需要';'
  .process(new CountFunction())
                               ^
1 个错误

- **错误行**: 6


### `USTM-F-Reconstruction\02-model-instantiation\02.03-dataflow-in-ustm.md`

**问题 #3** (第 563 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4_c3j6zxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp4_c
- **错误行**: 3

**问题 #5** (第 605 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphn6206t6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmphn620
- **错误行**: 3


### `USTM-F-Reconstruction\02-model-instantiation\02.07-flink-in-ustm.md`

**问题 #1** (第 73 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph0r_st6dTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmph0r
- **错误行**: 3

**问题 #3** (第 398 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2uvwrfk4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2uvwr
- **错误行**: 3


### `USTM-F-Reconstruction\03-proof-chains\03.03-consistency-lattice-theorem.md`

**问题 #2** (第 605 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsuvk48ihTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpsuvk48i
- **错误行**: 3

**问题 #3** (第 621 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9i0ywh96TempValidation.java:4: 错误: 找不到符号
properties.put(ProducerConfig.ACKS_CONFIG, "all");  // 强一致性
               ^
  符号:   变量 ProducerConfig
  位置: 类 TempValidat
- **错误行**: 4


### `USTM-F-Reconstruction\03-proof-chains\03.06-exactly-once-semantics-proof.md`

**问题 #1** (第 545 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5g5dzbc4TempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<String> source = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\Use
- **错误行**: 4

**问题 #2** (第 565 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr6gy1i5_TempValidation.java:4: 错误: 需要';'
INSERT INTO results (id, value)
           ^
C:\Users\luyan\AppData\Local\Temp\tmpr6gy1i5_TempValidation.java:4: 错误: 需要';'
- **错误行**: 4


### `USTM-F-Reconstruction\04-encoding-verification\04.03-dataflow-csp-encoding.md`

**问题 #18** (第 534 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx55_kfktTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpx55_k
- **错误行**: 3

**问题 #20** (第 560 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq03d0yo0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpq03d0
- **错误行**: 3

**问题 #22** (第 594 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp83t28p04TempValidation.java:3: 错误: 找不到符号
stream.process(new ProcessFunction() {
                   ^
  符号:   类 ProcessFunction
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 3


### `USTM-F-Reconstruction\archive\original-struct\01-foundation\01.04-dataflow-model-formalization.md`

**问题 #1** (第 392 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1iac4l4eTempValidation.java:3: 错误: 找不到符号
        DataStream<String> text = env.socketTextStream("localhost", 9999);
        ^
  符号:   类 DataStream
  位置: 类 TempVali
- **错误行**: 3


### `USTM-F-Reconstruction\archive\original-struct\02-properties\02.01-determinism-in-streaming.md`

**问题 #3** (第 408 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1u_1vzjsTempValidation.java:3: 错误: 找不到符号
        DataStream<Event> events = env.addSource(kafkaSource);
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Us
- **错误行**: 3

**问题 #4** (第 440 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4pgb125hTempValidation.java:4: 错误: 找不到符号
DataStream<Event> events = env.addSource(ctx -> {
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #5** (第 460 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu6o2np_6TempValidation.java:6: 错误: 非法的表达式开始
        WatermarkStrategy.<Event>forBoundedOutOfOrderness(...)

- **错误行**: 6

**问题 #6** (第 475 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7lf414t5TempValidation.java:4: 错误: 找不到符号
DataStream<EnrichedEvent> enriched = events
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4


### `USTM-F-Reconstruction\archive\original-struct\02-properties\02.02-consistency-hierarchy.md`

**问题 #1** (第 656 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxgvb6gymTempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<String> source = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\Use
- **错误行**: 4

**问题 #3** (第 726 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdj1jk8rgHttpSink.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.sink不存在
import org.apache.flink.streaming.api.functions.sink.SinkFunction;

- **错误行**: 1

**问题 #4** (第 750 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz6pmfgl8EagerKafkaSource.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.source不存在
import org.apache.flink.streaming.api.functions.source.SourceFunction;

- **错误行**: 1


### `USTM-F-Reconstruction\archive\original-struct\02-properties\02.03-watermark-monotonicity.md`

**问题 #1** (第 315 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmxrzy7i1TempValidation.java:4: 错误: 非法的表达式开始
public void onWatermark(Watermark wm, Context ctx, Collector<Out> out) {
^
C:\Users\luyan\AppData\Local\Temp\tmpmxrzy7i
- **错误行**: 4


### `USTM-F-Reconstruction\archive\original-struct\03-relationships\03.02-flink-to-process-calculus.md`

**问题 #1** (第 418 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4zhc35j1TempValidation.java:3: 错误: 找不到符号
        DataStream<String> text = env.socketTextStream("localhost", 9999);
        ^
  符号:   类 DataStream
  位置: 类 TempVali
- **错误行**: 3

**问题 #3** (第 488 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppovrhe0mTempValidation.java:4: 错误: 找不到符号
countState.update(countState.value() + 1);
                  ^
  符号:   变量 countState
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4


### `USTM-F-Reconstruction\archive\original-struct\03-relationships\03.05-cross-model-mappings.md`

**问题 #6** (第 557 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7n59ikneTempValidation.java:3: 错误: 找不到符号
        DataStream<Result> result = stream
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 3


### `USTM-F-Reconstruction\archive\original-struct\04-proofs\04.02-flink-exactly-once-correctness.md`

**问题 #5** (第 732 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbxlpdy_qTempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<String> source = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\Use
- **错误行**: 4

**问题 #6** (第 770 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpksg487vmTempValidation.java:4: 错误: 找不到符号
StreamingFileSink<Result> sink = StreamingFileSink
^
  符号:   类 StreamingFileSink
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4

**问题 #7** (第 793 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp465mr4puCounterSink.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.sink不存在
import org.apache.flink.streaming.api.functions.sink.SinkFunction;

- **错误行**: 1

**问题 #8** (第 821 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0ciryr8dEagerKafkaSource.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.source不存在
import org.apache.flink.streaming.api.functions.source.SourceFunction;

- **错误行**: 1


### `USTM-F-Reconstruction\archive\original-struct\04-proofs\04.04-watermark-algebra-formal-proof.md`

**问题 #2** (第 788 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz_0ecm6aTempValidation.java:4: 错误: 找不到符号
Watermark currentOutput = mergeAllInputWatermarks();
^
  符号:   类 Watermark
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #5** (第 1138 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplyc8m1ftTempValidation.java:3: 错误: 非法的表达式开始
public void onWatermark(Watermark wm, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmplyc8m1ftTempValidation.java
- **错误行**: 3

**问题 #6** (第 1216 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvglb84d7TempValidation.java:3: 错误: 非法的表达式开始
public void onWatermark(Watermark wm, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpvglb84d7TempValidation.java
- **错误行**: 3


### `USTM-F-Reconstruction\archive\original-struct\04-proofs\04.07-deadlock-freedom-choreographic.md`

**问题 #1** (第 242 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf28tvg_zBuyTicket.java:2: 错误: 需要'{'
class BuyTicket@Buyer,Seller {
               ^
C:\Users\luyan\AppData\Local\Temp\tmpf28tvg_zBuyTicket.java:2: 错误: 需要 class、int
- **错误行**: 2

**问题 #9** (第 933 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpodqy4kisRequestResponse.java:1: 错误: 需要'{'
class RequestResponse@Client,Server {
                     ^
C:\Users\luyan\AppData\Local\Temp\tmpodqy4kisRequestResponse
- **错误行**: 1

**问题 #10** (第 953 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpem1ad_36ClientRequestResponse.java:3: 错误: 找不到符号
        sendToServer(request);
        ^
  符号:   方法 sendToServer(String)
  位置: 类 ClientRequestResponse
C:\Users\luy
- **错误行**: 3

**问题 #11** (第 964 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplhjyyw2eServerRequestResponse.java:3: 错误: 找不到符号
        String request = receiveFromClient();
                         ^
  符号:   方法 receiveFromClient()
  位置: 类 Ser
- **错误行**: 3

**问题 #12** (第 988 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp24fvvywsAuction.java:1: 错误: 需要'{'
class Auction@Buyer,Seller,Arbiter {
             ^
C:\Users\luyan\AppData\Local\Temp\tmp24fvvywsAuction.java:1: 错误: 需要 class、int
- **错误行**: 1


### `USTM-F-Reconstruction\archive\original-struct\06-frontier\06.02-choreographic-streaming-programming.md`

**问题 #8** (第 541 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4zn5s74eTempValidation.java:4: 错误: 找不到符号
DataStream<String> lines = env.socketTextStream("localhost", 9999);
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users
- **错误行**: 4

**问题 #14** (第 690 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvuw5039eJoinOp.java:11: 错误: 不是语句
            select {
            ^
C:\Users\luyan\AppData\Local\Temp\tmpvuw5039eJoinOp.java:11: 错误: 需要';'
            select {

- **错误行**: 11


### `USTM-F-Reconstruction\archive\original-struct\Model-Selection-Decision-Tree.md`

**问题 #6** (第 400 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2xmlazm9TempValidation.java:4: 错误: 找不到符号
Pattern<UserEvent, ?> pattern = Pattern.<UserEvent>begin("start")
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 4


### `USTM-F-Reconstruction\archive\original-struct\Unified-Model-Relationship-Graph.md`

**问题 #5** (第 254 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr6eggrerTempValidation.java:3: 错误: 找不到符号
        DataStream<Event> stream = env
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 3


### `USTM-F-Reconstruction\pdf\USTM-F-Combined.md`

**问题 #78** (第 8593 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgquzbpm3TempValidation.java:6: 错误: 需要';'
  .process(new CountFunction())
                               ^
1 个错误

- **错误行**: 6

**问题 #103** (第 10785 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpczkcsyw4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpczk
- **错误行**: 3

**问题 #105** (第 10827 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpehulsa5qTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpehuls
- **错误行**: 3

**问题 #121** (第 12617 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgpai1973TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpgpa
- **错误行**: 3

**问题 #123** (第 12942 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmxtfv459TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpmxtfv
- **错误行**: 3

**问题 #139** (第 15475 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpemgueexeTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpemgueex
- **错误行**: 3

**问题 #140** (第 15491 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsrdrr3gmTempValidation.java:4: 错误: 找不到符号
properties.put(ProducerConfig.ACKS_CONFIG, "all");  // 强一致性
               ^
  符号:   变量 ProducerConfig
  位置: 类 TempValidat
- **错误行**: 4

**问题 #152** (第 17393 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf70l7mj8TempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<String> source = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\Use
- **错误行**: 4

**问题 #153** (第 17413 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptvf_itoiTempValidation.java:4: 错误: 需要';'
INSERT INTO results (id, value)
           ^
C:\Users\luyan\AppData\Local\Temp\tmptvf_itoiTempValidation.java:4: 错误: 需要';'
- **错误行**: 4

**问题 #218** (第 20728 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7izpc202TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp7izpc
- **错误行**: 3

**问题 #220** (第 20754 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgmarh8tyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpgmarh
- **错误行**: 3

**问题 #222** (第 20788 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc17v8gy9TempValidation.java:3: 错误: 找不到符号
stream.process(new ProcessFunction() {
                   ^
  符号:   类 ProcessFunction
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 3


### `archive\completion-reports\LINK-HEALTH-REPORT.md`

**问题 #1** (第 48 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1ntfuqfgTempValidation.java:4: 错误: 需要';'
state.get(Transaction("first"))
                               ^
1 个错误

- **错误行**: 4


### `archive\completion-reports\TECHNICAL-AUDIT-REPORT.md`

**问题 #1** (第 43 行, 语言: yaml)

- **错误**: while scanning a simple key
  in "<unicode string>", line 8, column 1:
    <artifactId>flink-ai-agent</arti ...
    ^ (line: 8)
could not find expected ':'
  in "<unicode string>", line 9, column 1:

- **错误行**: 8


### `archive\completion-reports\TROUBLESHOOTING-COMPLETE.md`

**问题 #9** (第 554 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpay_nzmf4TempValidation.java:4: 错误: 找不到符号
env.getConfig().setBufferDebloatingEnabled(true);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #17** (第 764 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa7v9x6h5MonitoredFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
StateTtlConfig ttlConfig = StateTtlConfig
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Loca
- **错误行**: 2

**问题 #19** (第 827 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeb6h0k_lMyKryoConfig.java:13: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<MyEvent> stream = env
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Local\Temp\tmpeb6
- **错误行**: 13

**问题 #22** (第 903 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpohikc7drTempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4


### `archive\deprecated\00.md`

**问题 #4** (第 403 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmxxfap1jTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend backend = new EmbeddedRocksDBStateBackend(true);
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置:
- **错误行**: 4

**问题 #6** (第 453 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi9138ctnTempValidation.java:6: 错误: 找不到符号
      .aggregate(new CountAggregate());
                     ^
  符号:   类 CountAggregate
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 6


### `archive\off-topic-candidates\Flink-IoT-Authority-Alignment\Phase-1-Architecture\01-flink-iot-foundation-and-architecture.md`

**问题 #9** (第 738 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 95, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^ (line: 95)
- **错误行**: 95
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #11** (第 1122 行, 语言: yaml)

- **错误**: could not determine a constructor for the tag '!Ref'
  in "<unicode string>", line 296, column 12:
        Value: !Ref VPC
               ^ (line: 296)
- **错误行**: 296


### `archive\off-topic-candidates\Flink-IoT-Authority-Alignment\Phase-1-Architecture\03-flink-iot-time-semantics-and-disorder.md`

**问题 #1** (第 162 行, 语言: sql)

- **错误**: 可能的语法问题: -- STREAMKAP推荐的IOT WATERMARK配置
WATERMARK FOR DEVIC...

**问题 #6** (第 372 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwqun2r2fTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwqu
- **错误行**: 3

**问题 #7** (第 417 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwh3l_208TempValidation.java:4: 错误: 找不到符号
WatermarkStrategy.<SensorEvent>forBoundedOutOfOrderness(
                   ^
  符号:   类 SensorEvent
  位置: 类 TempValidation
- **错误行**: 4

**问题 #8** (第 448 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo56bfzmmTempValidation.java:4: 错误: 找不到符号
WatermarkStrategy.<SensorEvent>forBoundedOutOfOrderness(
                   ^
  符号:   类 SensorEvent
  位置: 类 TempValidation
- **错误行**: 4

**问题 #13** (第 574 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe29vvfhjTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpe29vvfhjTempValidat
- **错误行**: 4

**问题 #28** (第 1374 行, 语言: sql)

- **错误**: 可能的语法问题: -- AWS IAM角色配置（通过FLINK配置传递）
-- FLINK-CONF.YAML:
--...

**问题 #32** (第 1487 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...


### `archive\off-topic-candidates\Flink-IoT-Authority-Alignment\Phase-1-Architecture\PHASE-1-COMPLETION-REPORT.md`

**问题 #3** (第 141 行, 语言: sql)

- **错误**: 可能的语法问题: WATERMARK FOR DEVICE_TIME AS DEVICE_TIME - INTERVA...


### `archive\off-topic-candidates\Flink-IoT-Authority-Alignment\Phase-10-Telecom\22-flink-iot-telecom-self-healing.md`

**问题 #3** (第 415 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprep5b4j0TempValidation.java:4: 错误: 找不到符号
DataSet<Vertex<String, Double>> rootCauseScores = faultGraph
^
  符号:   类 DataSet
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4


### `archive\off-topic-candidates\Flink-IoT-Authority-Alignment\Phase-13-Water-Management\25-flink-iot-smart-water-management.md`

**问题 #7** (第 529 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp52nhj0z3TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmp52nhj0z3TempValidatio
- **错误行**: 4


### `archive\off-topic-candidates\Flink-IoT-Authority-Alignment\Phase-2-Processing\04-flink-iot-hierarchical-downsampling.md`

**问题 #11** (第 495 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc4bp9dgaTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `archive\off-topic-candidates\Flink-IoT-Authority-Alignment\Phase-2-Processing\05-flink-iot-alerting-and-monitoring.md`

**问题 #4** (第 248 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq6dt05xxTempValidation.java:5: 错误: 找不到符号
                watermarkStrategy.getCurrentWatermark();
                ^
  符号:   变量 watermarkStrategy
  位置: 类 TempValida
- **错误行**: 5

**问题 #6** (第 284 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4zh5q8_fTempValidation.java:6: 错误: 不是语句
- numberOfFailedCheckpoints
^
C:\Users\luyan\AppData\Local\Temp\tmp4zh5q8_fTempValidation.java:6: 错误: 需要';'
- numberOfFaile
- **错误行**: 6

**问题 #10** (第 357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp5epagcbTempValidation.java:6: 错误: 不是语句
- watermarkLag
^
C:\Users\luyan\AppData\Local\Temp\tmpp5epagcbTempValidation.java:6: 错误: 需要';'
- watermarkLag

- **错误行**: 6


### `archive\off-topic-candidates\Flink-IoT-Authority-Alignment\Phase-3-Deployment\06-flink-iot-cloud-native-deployment.md`

**问题 #8** (第 366 行, 语言: sql)

- **错误**: 可能的语法问题: -- 内存存储与磁性存储分层
MEMORY_RETENTION := 24 HOURS   -- 热...

**问题 #33** (第 3264 行, 语言: yaml)

- **错误**: while parsing a flow node
expected the node content, but found '-'
  in "<unicode string>", line 4, column 3:
    {{- define "flink-iot.deployment" -}}
      ^ (line: 4)
- **错误行**: 4


### `archive\off-topic-candidates\Flink-IoT-Authority-Alignment\Phase-3-Deployment\07-flink-iot-performance-tuning.md`

**问题 #6** (第 482 行, 语言: sql)

- **错误**: 可能的语法问题: -- ========================================
-- FLI...; 可能的语法问题: -- 2. CHECKPOINT配置（生产环境推荐）
SET 'EXECUTION.CHECKPOI...; 可能的语法问题: -- 3. 状态后端配置
SET 'STATE.BACKEND' = 'ROCKSDB';...; 可能的语法问题: -- 4

**问题 #8** (第 599 行, 语言: sql)

- **错误**: 可能的语法问题: -- ========================================
-- ROC...; 可能的语法问题: -- 1. 内存调优参数
SET 'STATE.BACKEND.ROCKSDB.MEMORY.MAN...; 可能的语法问题: -- 2. WRITEBUFFER配置
SET 'STATE.BACKEND.ROCKSDB.WRI...; 可能的语法问题:


### `archive\off-topic-candidates\Flink-IoT-Authority-Alignment\Phase-4-Case-Study\08-flink-iot-complete-case-study.md`

**问题 #17** (第 1735 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 103, column 39:
     ...   jobmanager.memory.process.size: 2048m
                                         ^ (line: 103)
- **错误行**: 103
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #24** (第 2344 行, 语言: sql)

- **错误**: 可能的语法问题: -- 1. 使用 MINIBATCH 优化聚合性能
SET TABLE.EXEC.MINI-BATC...; 可能的语法问题: -- 2. 启用 LOCAL-GLOBAL 聚合
SET TABLE.OPTIMIZER.AGG-P...; 可能的语法问题: -- 3. 使用 ROCKSDB 状态后端
SET STATE.BACKEND = 'ROCKSDB...; 可能的语法问题:


### `archive\off-topic-candidates\Flink-IoT-Authority-Alignment\Phase-4-Case-Study\09-flink-iot-pattern-catalog.md`

**问题 #2** (第 91 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5g5111avTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5g5
- **错误行**: 3

**问题 #3** (第 110 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpibyap7miTempValidation.java:4: 错误: 找不到符号
ExecutionEnvironment batchEnv = ExecutionEnvironment.getExecutionEnvironment();
^
  符号:   类 ExecutionEnvironment
  位置: 类 T
- **错误行**: 4

**问题 #4** (第 123 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprn5tbe7jTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmprn5
- **错误行**: 3

**问题 #5** (第 139 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpidptxgp7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpidp
- **错误行**: 3

**问题 #6** (第 185 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpop7s6uuxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpop7
- **错误行**: 3

**问题 #7** (第 206 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyxtnuwk9TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpyxtnuwk9TempValidat
- **错误行**: 4

**问题 #8** (第 243 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp17lrcggjTempValidation.java:4: 错误: 找不到符号
Properties prodMqttProps = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #9** (第 264 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdfa4r7exTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpdfa
- **错误行**: 3

**问题 #10** (第 285 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuft4vrseTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpuft4vrs
- **错误行**: 3

**问题 #11** (第 308 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt4wy07hdTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpt4wy07hdTempValidat
- **错误行**: 4

**问题 #12** (第 352 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi09rtofjTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpi09rtofjTempValidat
- **错误行**: 4

**问题 #14** (第 453 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1jb3z2ckAverageAggregate.java:6: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<AvgTemperature> avgTemp = sensorStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 6

**问题 #15** (第 496 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1i9w8rr1TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1i9
- **错误行**: 3

**问题 #16** (第 520 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4h1j772iSessionProcessFunction.java:6: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<DeviceSession> sessions = sensorStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 6

**问题 #17** (第 578 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq2uth_38TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpq2uth_38TempValidat
- **错误行**: 4

**问题 #19** (第 636 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe__mbswbTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpe__mbswbTempValidat
- **错误行**: 4

**问题 #20** (第 697 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzdrtmw4tTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpzdrtmw4tTempValidat
- **错误行**: 4

**问题 #21** (第 759 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpur0ps6_hHeartbeatMonitor.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
Pattern<DeviceEvent, ?> offlinePattern = Pattern
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppDat
- **错误行**: 2

**问题 #22** (第 832 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg6p6zum6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpg6p
- **错误行**: 3

**问题 #24** (第 908 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpayzlmaugTempValidation.java:10: 错误: 找不到符号
tableEnv.executeSql(createCatalog);
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpayz
- **错误行**: 10

**问题 #25** (第 935 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv6a47f3gTempValidation.java:4: 错误: 找不到符号
Map<String, String> hudiOptions = new HashMap<>();
^
  符号:   类 Map
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #26** (第 958 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnp5bp1vpTempValidation.java:4: 错误: 找不到符号
PinotSinkFunction<GenericRow> pinotSink = new PinotSinkFunction<>(
^
  符号:   类 PinotSinkFunction
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #30** (第 1132 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxhs8xyvoTempValidation.java:5: 错误: 需要';'
appender.json.type = RollingFile
                                ^
C:\Users\luyan\AppData\Local\Temp\tmpxhs8xyvoTempValida
- **错误行**: 5

**问题 #32** (第 1166 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkvz_rftaTracedFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
OpenTelemetry openTelemetry = OpenTelemetrySdk.builder()
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #43** (第 1486 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6o_7qqf0TempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp6o_7qqf0TempV
- **错误行**: 4

**问题 #44** (第 1506 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjddq4lr5TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpjddq4lr5TempValidat
- **错误行**: 4


### `archive\off-topic-candidates\Flink-IoT-Authority-Alignment\Phase-7-Smart-Retail\case-smart-retail-complete.md`

**问题 #39** (第 6123 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp13r8qtibTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp13r8q
- **错误行**: 3


### `archive\off-topic-candidates\Flink-IoT-Authority-Alignment\Phase-8-Wearables\case-wearables-health-complete.md`

**问题 #28** (第 2839 行, 语言: sql)

- **错误**: 可能的语法问题: AND AVG(GLUCOSE_MGDL) > 200;...

**问题 #41** (第 3838 行, 语言: sql)

- **错误**: 可能的语法问题: -- 3小时和6小时预测（类似逻辑，使用更长历史数据）
-- 此处省略类似代码......


### `archive\off-topic-candidates\formal-methods\wikipedia-concepts\17-two-phase-commit.md`

**问题 #14** (第 528 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg1jbu2cwTempValidation.java:4: 错误: 找不到符号
UserTransaction ut = getUserTransaction();
^
  符号:   类 UserTransaction
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 4


### `archive\off-topic-candidates\formal-methods\wikipedia-concepts\en\17-two-phase-commit.md`

**问题 #14** (第 544 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy0cgkk0bTempValidation.java:4: 错误: 找不到符号
UserTransaction ut = getUserTransaction();
^
  符号:   类 UserTransaction
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 4


### `docs\certification\csa\labs\lab-01-time-semantics.md`

**问题 #3** (第 89 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpky_m9t1oTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpky_m9t1oTempValidatio
- **错误行**: 4

**问题 #7** (第 199 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0e_asr5uTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmp0e_asr5uTempValidatio
- **错误行**: 4


### `docs\certification\csa\resources\capstone-project-csa.md`

**问题 #4** (第 153 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpayjva60_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpayj
- **错误行**: 3

**问题 #5** (第 185 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwoj_6cv3TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.functions.AggregateFunction;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #6** (第 220 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpind9hyvrTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpind9h
- **错误行**: 3

**问题 #8** (第 278 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsypkdgabTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpsypkd
- **错误行**: 3

**问题 #9** (第 310 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp11iva2i0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp11iva2i
- **错误行**: 3


### `docs\chatbot-integration.md`

**问题 #17** (第 683 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2pmoswwzTempValidation.java:3: 错误: 非法的表达式开始
        > env.enableCheckpointing(60000);  // 60 second interval
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2pmosww
- **错误行**: 3


### `docs\code-style-guide.md`

**问题 #6** (第 208 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<block mapping start>',)
  in "<unicode string>", line 7, column 1:
    version: "3.8"
    ^ (line: 7)
- **错误行**: 7


### `docs\contributing\writing-guide.md`

**问题 #9** (第 250 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5mit77aaTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #18** (第 397 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpviim0euqTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpvii
- **错误行**: 3

**问题 #22** (第 454 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplso69nbqTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmplso
- **错误行**: 3


### `docs\i18n\MKDOCS-I18N-CONFIG.md`

**问题 #1** (第 13 行, 语言: yaml)

- **错误**: could not determine a constructor for the tag 'tag:yaml.org,2002:python/name:material.extensions.emoji.twemoji'
  in "<unicode string>", line 72, column 20:
          emoji_index: !!python/name:materi
- **错误行**: 72


### `docs\i18n\en\04-QUICK-START.md`

**问题 #20** (第 757 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8ilao7foTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #21** (第 773 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 6, column 1:
    logger.flink.name = org.apache.flink
    ^ (line: 6)
- **错误行**: 6


### `docs\i18n\en\Flink\02-core\checkpoint-mechanism-deep-dive.md`

**问题 #1** (第 155 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvxod07ceStateBackend.java:3: 错误: 需要<标识符>
    createKeyedStateBackend(env, stateHandles): AbstractKeyedStateBackend<K>
                           ^
C:\Users\luyan\A
- **错误行**: 3

**问题 #5** (第 410 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph49ffas8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmph49ffas
- **错误行**: 3

**问题 #6** (第 428 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpooj9bl3mTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpooj9bl3
- **错误行**: 3

**问题 #7** (第 446 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_9nr1dqyTempValidation.java:4: 错误: 找不到符号
env.setStateBackend(new EmbeddedRocksDBStateBackend(true));  // incremental = true
                        ^
  符号:   类 Emb
- **错误行**: 4


### `docs\i18n\en\Knowledge\07-best-practices\07.01-flink-production-checklist.md`

**问题 #3** (第 223 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpju2ktcwlTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000); // 1 minute interval
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #4** (第 249 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi26et9t5TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpi26
- **错误行**: 3

**问题 #7** (第 374 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkiyp0aszTempValidation.java:4: 错误: 非法的表达式开始
private static final Logger LOG = LoggerFactory.getLogger(MyFunction.class);
^
C:\Users\luyan\AppData\Local\Temp\tmpkiy
- **错误行**: 4

**问题 #11** (第 562 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp28_di88bTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(10000);  // 10s interval
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #12** (第 573 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9rw4ydgkTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(300000);  // 5min interval
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `docs\i18n\en\OBSERVABILITY-GUIDE.md`

**问题 #6** (第 361 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyqivoy2cTempValidation.java:3: 错误: 找不到符号
        MDC.put("trace_id", TraceContext.getCurrentTraceId());
        ^
  符号:   变量 MDC
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3


### `docs\i18n\en\Struct\01-foundation\01.04-dataflow-model-formalization.md`

**问题 #1** (第 392 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxan5c1_mTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpxan
- **错误行**: 3


### `docs\i18n\en\Struct\02-properties\02.01-determinism-in-streaming.md`

**问题 #3** (第 497 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9jmkgvc1TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9jm
- **错误行**: 3

**问题 #4** (第 533 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxhs7jn6sTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpxhs7jn6sTempValidat
- **错误行**: 4

**问题 #5** (第 556 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvfs64iyoTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpvfs
- **错误行**: 3

**问题 #6** (第 574 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1rklb0ocTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp1rklb0ocTempValidat
- **错误行**: 4


### `docs\i18n\en\Struct\02-properties\02.02-consistency-hierarchy.md`

**问题 #1** (第 656 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp53yxvus8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp53y
- **错误行**: 3

**问题 #3** (第 730 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpixi9celsHttpSink.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.sink不存在
import org.apache.flink.streaming.api.functions.sink.SinkFunction;

- **错误行**: 1

**问题 #4** (第 754 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp433z05yxEagerKafkaSource.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.source不存在
import org.apache.flink.streaming.api.functions.source.SourceFunction;

- **错误行**: 1


### `docs\i18n\en\Struct\02-properties\02.03-watermark-monotonicity.md`

**问题 #1** (第 314 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxcl4kq_9TempValidation.java:4: 错误: 非法的表达式开始
public void onWatermark(Watermark wm, Context ctx, Collector<Out> out) {
^
C:\Users\luyan\AppData\Local\Temp\tmpxcl4kq_
- **错误行**: 4


### `docs\i18n\en\Struct\04-proofs\04.02-flink-exactly-once-correctness.md`

**问题 #5** (第 735 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp072jnc48TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp072
- **错误行**: 3

**问题 #6** (第 777 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqzjyyp0iTempValidation.java:4: 错误: 找不到符号
StreamingFileSink<Result> sink = StreamingFileSink
^
  符号:   类 StreamingFileSink
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4

**问题 #7** (第 800 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp402ydhcbCounterSink.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.sink不存在
import org.apache.flink.streaming.api.functions.sink.SinkFunction;

- **错误行**: 1

**问题 #8** (第 828 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpys_vcn5rEagerKafkaSource.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.source不存在
import org.apache.flink.streaming.api.functions.source.SourceFunction;

- **错误行**: 1


### `docs\i18n\en\TEMPLATE.md`

**问题 #3** (第 169 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvq0trh9jTempValidation.java:4: 错误: 找不到符号
StreamExecutionEnvironment env =
^
  符号:   类 StreamExecutionEnvironment
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4


### `docs\i18n\en\TROUBLESHOOTING.md`

**问题 #6** (第 197 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpelcp2o6zSyncFunction.java:22: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Result> result = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 22

**问题 #8** (第 273 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6cqyfiqwTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp6cq
- **错误行**: 3

**问题 #10** (第 341 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpboqajkioTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpboqajkioTempValidat
- **错误行**: 4

**问题 #16** (第 582 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj5qkvs5bTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpj5q
- **错误行**: 3


### `examples\docker\README.md`

**问题 #8** (第 139 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 3, column 37:
          jobmanager.memory.process.size: 512m
                                        ^ (line: 3)
- **错误行**: 3
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `examples\java\stateful\README.md`

**问题 #3** (第 62 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb4slgengTempValidation.java:4: 错误: 需要')'或','
env.setStateBackend(new HashMapStateBackend()  // MemoryStateBackend已弃用，使用HashMapStateBackend

- **错误行**: 4

**问题 #4** (第 76 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiq33zqeeTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpiq33z
- **错误行**: 3


### `examples\java\wordcount\README.md`

**问题 #7** (第 102 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsypmgy4kTempValidation.java:4: 错误: 找不到符号
if (word.length() > 3) {
    ^
  符号:   变量 word
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpsypmgy4kTempVal
- **错误行**: 4


### `formal-methods\01-foundations\05-type-theory.md`

**问题 #6** (第 533 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3dj_aoleTempValidation.java:3: 错误: 需要>或','
        <T extends Comparable<T>> T max(T a, T b)
           ^
C:\Users\luyan\AppData\Local\Temp\tmp3dj_aoleTempValidati
- **错误行**: 3


### `formal-methods\01-foundations\09-subtyping.md`

**问题 #3** (第 295 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnvr3reamComparable.java:5: 错误: 未命名类 是预览功能，默认情况下禁用。
<T extends Comparable<T>> T max(T a, T b)  // F-有界
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Lo
- **错误行**: 5

**问题 #8** (第 594 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5tc6o3jwAnimal.java:3: 错误: 非法的表达式开始
    void speak() { ... }
                   ^
C:\Users\luyan\AppData\Local\Temp\tmp5tc6o3jwAnimal.java:7: 错误: 非法的表达式开始
    void
- **错误行**: 3


### `formal-methods\03-model-taxonomy\06-practical-concurrency\01-practical-concurrency-formalization.md`

**问题 #5** (第 554 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprsyvk978ParallelMergeSort.java:48: 错误: 未命名类 是预览功能，默认情况下禁用。
ForkJoinPool pool = new ForkJoinPool();
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Local
- **错误行**: 48


### `formal-methods\04-application-layer\01-workflow\03-bpmn-semantics.md`

**问题 #11** (第 352 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0g5gt5tyEventBasedGateway.java:5: 错误: 找不到符号
    List<Event> waitingEvents;
         ^
  符号:   类 Event
  位置: 类 EventBasedGateway
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 5


### `formal-methods\04-application-layer\02-stream-processing\01-stream-formalization.md`

**问题 #4** (第 296 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2qpggkbvExactlyOnceOperator.java:3: 错误: 找不到符号
    void processElement(Element e) {
                        ^
  符号:   类 Element
  位置: 类 ExactlyOnceOperator
C:\Users
- **错误行**: 3


### `formal-methods\04-application-layer\02-stream-processing\03-window-semantics.md`

**问题 #2** (第 239 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphsa7m0k4TempValidation.java:4: 错误: 找不到符号
Window.into(FixedWindows.of(Duration.standardMinutes(1)))
^
  符号:   变量 Window
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4


### `formal-methods\04-application-layer\02-stream-processing\04-flink-formal-verification.md`

**问题 #1** (第 752 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaow3lvruTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpaow3lvruTempValidat
- **错误行**: 4

**问题 #3** (第 814 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5vy3b34rTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #4** (第 842 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6jw96_8uTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp6jw96
- **错误行**: 3


### `formal-methods\04-application-layer\02-stream-processing\04-flink-formalization.md`

**问题 #7** (第 375 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe5pi7wj_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpe5p
- **错误行**: 3

**问题 #9** (第 399 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqtnt1zp7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqtnt1zp
- **错误行**: 3

**问题 #11** (第 428 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph_xr8eg4TempValidation.java:12: 错误: 非法的表达式开始
WatermarkStrategy.<Event>forBoundedOutOfOrderness(...)
                                                  ^
1 个错误

- **错误行**: 12


### `formal-methods\04-application-layer\02-stream-processing\05-stream-joins.md`

**问题 #7** (第 318 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnbh8zqmmTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnbh
- **错误行**: 3

**问题 #9** (第 343 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbf44169cTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpbf44169cTempValidat
- **错误行**: 4

**问题 #13** (第 391 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx3qlk1vgTempValidation.java:4: 错误: 找不到符号
MapStateDescriptor<String, UserInfo> descriptor =
^
  符号:   类 MapStateDescriptor
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4


### `formal-methods\04-application-layer\04-blockchain-verification\02-consensus-protocols.md`

**问题 #8** (第 1031 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 6, column 1:
    timeout_propose = "3s"
    ^ (line: 6)
- **错误行**: 6


### `formal-methods\04-application-layer\10-kafka-formalization\01-kafka-semantics.md`

**问题 #26** (第 798 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdn5fnz1jTempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #27** (第 822 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptuaif48wTempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #28** (第 841 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr5cxjl1_TempValidation.java:3: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpr5
- **错误行**: 3

**问题 #29** (第 876 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm8l93qemTempValidation.java:3: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpm8
- **错误行**: 3

**问题 #30** (第 904 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_zujm4n5TempValidation.java:3: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp_z
- **错误行**: 3

**问题 #31** (第 930 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp31x09toxTempValidation.java:3: 错误: 找不到符号
Properties consumerProps = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 3

**问题 #32** (第 981 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8rpcwvx8TempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3


### `formal-methods\04-application-layer\11-mysql-formalization\01-mysql-innodb-semantics.md`

**问题 #5** (第 764 行, 语言: sql)

- **错误**: 可能的语法问题: -- READ COMMITTED: 返回3条记录 (幻读!)
-- REPEATABLE READ...

**问题 #9** (第 837 行, 语言: sql)

- **错误**: 可能的语法问题: -- 设置锁等待超时
SET SESSION INNODB_LOCK_WAIT_TIMEOUT = ...; 可能的语法问题: -- 等待50秒后:
-- ERROR 1205 (HY000): LOCK WAIT TIMEOU...

**问题 #10** (第 857 行, 语言: sql)

- **错误**: 可能的语法问题: -- 检查影响行数
-- 若 AFFECTED_ROWS = 1: 更新成功
-- 若 AFFECT...

**问题 #11** (第 887 行, 语言: sql)

- **错误**: 可能的语法问题: -- 应用程序代码 (伪代码)
-- 使用XA实现跨库事务

-- 第一阶段：准备
XA START...; 可能的语法问题: XA END 'TRX-001';...; 可能的语法问题: XA PREPARE 'TRX-001';  -- 准备阶段，记录REDO/UNDO...; 可能的语法问题: -- 协调器记录事务状态
-- 若所有参与者都PREPARE成功，则提交
--


### `formal-methods\05-verification\01-logic\06-permission-based-reasoning.md`

**问题 #8** (第 462 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp8291c9uTempValidation.java:7: 错误: 非法的表达式开始
void read_only(int x) {
^
C:\Users\luyan\AppData\Local\Temp\tmpp8291c9uTempValidation.java:7: 错误: 需要';'
void read_only(
- **错误行**: 7

**问题 #9** (第 493 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplohnogpvTempValidation.java:7: 错误: 非法的表达式开始
void parallel_sum(int[] a, int n) {
^
C:\Users\luyan\AppData\Local\Temp\tmplohnogpvTempValidation.java:7: 错误: 需要';'
voi
- **错误行**: 7

**问题 #13** (第 759 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0yzznr8qTreeNode.java:26: 错误: 不是语句
        parallel {
        ^
C:\Users\luyan\AppData\Local\Temp\tmp0yzznr8qTreeNode.java:26: 错误: 需要';'
        parallel {

- **错误行**: 26

**问题 #14** (第 797 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvvfl_q50TempValidation.java:11: 错误: 非法的表达式开始
void parallel_sort(int[] array, int n) {
^
C:\Users\luyan\AppData\Local\Temp\tmpvvfl_q50TempValidation.java:11: 错误: 需要
- **错误行**: 11

**问题 #16** (第 885 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3ermgfunLockFreeQueue.java:2: 错误: 找不到符号
    AtomicReference<Node<T>> head, tail;
    ^
  符号:   类 AtomicReference
  位置: 类 LockFreeQueue<T>
  其中, T是类型变量:
    T扩展已在类
- **错误行**: 2


### `formal-methods\05-verification\04-security\04-type-system-security.md`

**问题 #5** (第 449 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp28ztrivgTempValidation.java:5: 错误: 非法字符: '\u251c'
├── String
^
C:\Users\luyan\AppData\Local\Temp\tmp28ztrivgTempValidation.java:4: 错误: 不是语句
Object
^
C:\Users\luyan
- **错误行**: 5

**问题 #6** (第 461 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0okidsy1TempValidation.java:4: 错误: 找不到符号
List<String> strings = new ArrayList<>();
^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp0ok
- **错误行**: 4

**问题 #9** (第 499 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp02p_hao7TempValidation.java:4: 错误: 非法的表达式开始
void safeBufferJava() {
^
C:\Users\luyan\AppData\Local\Temp\tmp02p_hao7TempValidation.java:4: 错误: 需要';'
void safeBuffer
- **错误行**: 4


### `formal-methods\98-appendices\wikipedia-concepts\17-two-phase-commit.md`

**问题 #14** (第 528 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdavuiz19TempValidation.java:4: 错误: 找不到符号
UserTransaction ut = getUserTransaction();
^
  符号:   类 UserTransaction
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 4


### `formal-methods\98-appendices\wikipedia-concepts\en\17-two-phase-commit.md`

**问题 #14** (第 544 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3rngi983TempValidation.java:4: 错误: 找不到符号
UserTransaction ut = getUserTransaction();
^
  符号:   类 UserTransaction
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 4


### `formal-methods\COMPARISON-WORKFLOW-VS-STREAM.md`

**问题 #3** (第 219 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmperowttv0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpero
- **错误行**: 3


### `formal-methods\Flink\en\01-architecture-overview.md`

**问题 #1** (第 250 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuzqnh8v_TempValidation.java:4: 错误: 找不到符号
   state.getAsync(key)
                  ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpuzqn
- **错误行**: 4


### `formal-methods\Flink\en\03-checkpoint.md`

**问题 #1** (第 128 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp3mk3aogStateBackend.java:3: 错误: 需要<标识符>
    createKeyedStateBackend(env, stateHandles): AbstractKeyedStateBackend<K>
                           ^
C:\Users\luyan\A
- **错误行**: 3

**问题 #5** (第 577 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph6beq7q8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #6** (第 611 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuewl115_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #7** (第 638 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp211n4zcyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #8** (第 659 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcfhfia7aTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `formal-methods\Flink\en\04-state-backends.md`

**问题 #3** (第 493 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcwzplj_4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #5** (第 530 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwddh7hssTempValidation.java:5: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 5

**问题 #6** (第 580 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnrs3vxj3TempValidation.java:5: 错误: 找不到符号
ForStStateBackend forstBackend = new ForStStateBackend();
^
  符号:   类 ForStStateBackend
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 5


### `formal-methods\Flink\en\05-watermark.md`

**问题 #1** (第 256 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7bnmyg39TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp7bnmy
- **错误行**: 3

**问题 #2** (第 266 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6ofv5bbbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp6ofv5
- **错误行**: 3

**问题 #3** (第 276 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1fjbhs1aTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1fjbh
- **错误行**: 3

**问题 #4** (第 375 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqnz319gdTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqnz
- **错误行**: 3

**问题 #5** (第 387 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0se9a2paTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp0se
- **错误行**: 3

**问题 #6** (第 403 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwt6nz1t0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwt6nz
- **错误行**: 3

**问题 #7** (第 414 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7lju2hy8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp7lju2
- **错误行**: 3

**问题 #8** (第 425 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx57l0jmtTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpx57l0
- **错误行**: 3

**问题 #9** (第 439 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvu3gtjseTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpvu3
- **错误行**: 3


### `formal-methods\Flink\en\06-kafka-connector.md`

**问题 #7** (第 273 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwr0cvki6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwr0
- **错误行**: 3

**问题 #8** (第 296 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxl_reas7TempValidation.java:3: 错误: 找不到符号
        KafkaSink<String> sink = KafkaSink.<String>builder()
        ^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users
- **错误行**: 3

**问题 #9** (第 312 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpavsbb3oxTempValidation.java:3: 错误: 找不到符号
FlinkKafkaProducer<String> producer = new FlinkKafkaProducer<>(
^
  符号:   类 FlinkKafkaProducer
  位置: 类 TempValidation
C:\U
- **错误行**: 3


### `formal-methods\Flink\en\07-file-system.md`

**问题 #6** (第 261 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb2ctrdbwTempValidation.java:3: 错误: 找不到符号
        FileSink.forRowFormat(new Path("s3://bucket/output"), new SimpleStringEncoder())

- **错误行**: 3

**问题 #7** (第 307 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2_djugycTempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #8** (第 318 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt226_pkcTempValidation.java:5: 错误: 找不到符号
    new Path("s3://bucket/output"),
        ^
  符号:   类 Path
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpt
- **错误行**: 5

**问题 #9** (第 334 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcy7txidvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpcy7
- **错误行**: 3

**问题 #10** (第 357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphc2clt8yTempValidation.java:4: 错误: 找不到符号
FileSink<GenericRecord> sink = FileSink
^
  符号:   类 FileSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmph
- **错误行**: 4

**问题 #11** (第 382 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphhd686igTempValidation.java:4: 错误: 找不到符号
Schema evolvedSchema = new Schema.Parser().parse(
^
  符号:   类 Schema
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4


### `formal-methods\Flink\en\09-query-optimization.md`

**问题 #5** (第 238 行, 语言: sql)

- **错误**: 可能的语法问题: -- FULL ANALYSIS FOR CRITICAL TABLES
ANALYZE TABLE...; 可能的语法问题: -- COLUMN-SPECIFIC ANALYSIS
ANALYZE TABLE EVENTS C...; 可能的语法问题: -- SAMPLING FOR LARGE TABLES
ANALYZE TABLE BIG_TAB...

**问题 #6** (第 282 行, 语言: sql)

- **错误**: 可能的语法问题: -- ENABLE COST-BASED OPTIMIZATION
SET TABLE.OPTIMI...; 可能的语法问题: -- ENABLE ADVANCED REWRITES
SET TABLE.OPTIMIZER.DI...

**问题 #11** (第 370 行, 语言: sql)

- **错误**: 可能的语法问题: -- TWO-PHASE AGGREGATION FOR HIGH-CARDINALITY GROU...


### `formal-methods\Flink\en\11-standalone.md`

**问题 #10** (第 383 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 10, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^ (line: 10)
- **错误行**: 10
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `formal-methods\Flink\en\12-ml-pipeline.md`

**问题 #6** (第 359 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0n5p8bq3TempValidation.java:4: 错误: 找不到符号
OnlineLogisticRegression onlineLearner = new OnlineLogisticRegression()
^
  符号:   类 OnlineLogisticRegression
  位置: 类 TempV
- **错误行**: 4


### `formal-methods\Flink\en\13-gelly.md`

**问题 #1** (第 24 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnd_2phcgTempValidation.java:3: 错误: 不是语句
        Graph<K, VV, EV> = (DataSet<Vertex<K, VV>>, DataSet<Edge<K, EV>>)
             ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 3

**问题 #4** (第 253 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpstugcfvhTempValidation.java:4: 错误: 找不到符号
Graph<Long, Double, Double> graph = Graph.fromDataSet(
^
  符号:   类 Graph
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #5** (第 277 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmvm5ip_9PageRankComputeFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
Graph<Long, Double, Double> graph = Graph.fromDataSet(
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #6** (第 323 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr_29hlt0GatherNeighborIds.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
Graph<Long, Long, NullValue> ccGraph = graph
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #7** (第 356 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps3vee06uTempValidation.java:4: 错误: 找不到符号
Graph<Long, Double, Double> bipartiteGraph = Graph.fromDataSet(
^
  符号:   类 Graph
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #8** (第 379 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppcn_a68rTempValidation.java:4: 错误: 找不到符号
Graph<String, AccountInfo, Transaction> transactionGraph =
^
  符号:   类 Graph
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4


### `formal-methods\Knowledge\en\01-streaming-overview.md`

**问题 #4** (第 296 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6z41bs_vExactlyOnceOperator.java:3: 错误: 找不到符号
    void processElement(Element e) {
                        ^
  符号:   类 Element
  位置: 类 ExactlyOnceOperator
C:\Users
- **错误行**: 3


### `formal-methods\Knowledge\en\03-window-semantics.md`

**问题 #2** (第 239 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeljq22axTempValidation.java:4: 错误: 找不到符号
Window.into(FixedWindows.of(Duration.standardMinutes(1)))
^
  符号:   变量 Window
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4


### `formal-methods\Knowledge\en\04-time-semantics.md`

**问题 #7** (第 340 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpac9a_fikTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpac9
- **错误行**: 3

**问题 #9** (第 364 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqc5xe_c3TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqc5xe_c
- **错误行**: 3

**问题 #11** (第 393 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy5mdl6dxTempValidation.java:12: 错误: 非法的表达式开始
WatermarkStrategy.<Event>forBoundedOutOfOrderness(...)
                                                  ^
1 个错误

- **错误行**: 12


### `formal-methods\Knowledge\en\05-state-management.md`

**问题 #7** (第 318 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5j04kbocTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5j0
- **错误行**: 3

**问题 #9** (第 343 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnm9k8b6_TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpnm9k8b6_TempValidat
- **错误行**: 4

**问题 #13** (第 391 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpscw9ionzTempValidation.java:4: 错误: 找不到符号
MapStateDescriptor<String, UserInfo> descriptor =
^
  符号:   类 MapStateDescriptor
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4


### `formal-methods\Knowledge\en\07-exactly-once.md`

**问题 #6** (第 346 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiykco6fbTempValidation.java:4: 错误: 找不到符号
FlinkKafkaProducer<String> kafkaSink = new FlinkKafkaProducer<>(
^
  符号:   类 FlinkKafkaProducer
  位置: 类 TempValidation
C:\
- **错误行**: 4


### `formal-methods\Knowledge\en\10-performance-tuning.md`

**问题 #10** (第 440 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    taskmanager.memory.process.size: 4gb
    ^ (line: 4)
found duplicate key "taskmanager.memory.process.size" with value "32gb"
- **错误行**: 4


### `formal-methods\Knowledge\en\13-stream-joins.md`

**问题 #8** (第 396 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7fgl4burTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp7fg
- **错误行**: 3

**问题 #10** (第 421 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxxqnnng8TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpxxqnnng8TempValidat
- **错误行**: 4

**问题 #14** (第 474 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb_x0h7_xTempValidation.java:5: 错误: 需要';'
    new MapStateDescriptor<>("users", String.class, UserInfo.class)

- **错误行**: 5


### `formal-methods\Knowledge\en\15-schema-evolution.md`

**问题 #16** (第 520 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphgstios5TempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #17** (第 542 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2t5ivbtpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2t5ivbtpTempV
- **错误行**: 3

**问题 #18** (第 566 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn7gmawsiTempValidation.java:4: 错误: 找不到符号
Table orders = tableEnv.from("Orders");
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpn7gm
- **错误行**: 4


### `formal-methods\Knowledge\en\16-security.md`

**问题 #14** (第 566 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq7j847qeTempValidation.java:3: 错误: 找不到符号
        Configuration conf = new Configuration();
        ^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 3


### `formal-methods\Knowledge\en\17-cost-optimization.md`

**问题 #8** (第 401 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv7rtdas7TempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `formal-methods\分布式系统形式化建模理论与验证方法.md`

**问题 #31** (第 1137 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpezj3lkctTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpezj3lkctTem
- **错误行**: 3


### `i18n\en\Flink\00-FLINK-TECH-STACK-DEPENDENCY.md`

**问题 #8** (第 372 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj5yusrigTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #9** (第 397 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp39v2c26uTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp39v2c26uTemp
- **错误行**: 3

**问题 #11** (第 434 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpki2785ncTempValidation.java:7: 错误: 找不到符号
FlinkKafkaConsumer<Event> source = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\User
- **错误行**: 7


### `i18n\en\Flink\01-concepts\disaggregated-state-analysis.md`

**问题 #3** (第 372 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5ogvzxjzTempValidation.java:3: 错误: 找不到符号
        DisaggregatedStateBackend stateBackend = new DisaggregatedStateBackend(
        ^
  符号:   类 DisaggregatedStateBack
- **错误行**: 3

**问题 #4** (第 401 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb8aov1duTempValidation.java:10: 错误: 需要';'
    .build()
            ^
1 个错误

- **错误行**: 10


### `i18n\en\Flink\01-concepts\flink-1.x-vs-2.0-comparison.md`

**问题 #7** (第 260 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwsrq6k07TempValidation.java:4: 错误: 找不到符号
CountState current = state.value();  // blocking call
^
  符号:   类 CountState
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4

**问题 #8** (第 271 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfdj9ri4eTempValidation.java:4: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpfdj9ri4eTe
- **错误行**: 4

**问题 #13** (第 381 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp_3owpclTempValidation.java:3: 错误: 非法的表达式开始
public void processElement(Event event, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpp_3owpclTempValidation.ja
- **错误行**: 3

**问题 #14** (第 392 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu8d44v0lTempValidation.java:3: 错误: 非法的表达式开始
public void processElement(Event event, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpu8d44v0lTempValidation.ja
- **错误行**: 3


### `i18n\en\Flink\01-concepts\flink-architecture-evolution-1x-to-2x.md`

**问题 #1** (第 257 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp594k64_zTempValidation.java:4: 错误: 找不到符号
   state.getAsync(key)
                  ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp594k
- **错误行**: 4


### `i18n\en\Flink\02-core\checkpoint-mechanism-deep-dive.md`

**问题 #1** (第 188 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3u940ghhStateBackend.java:3: 错误: 需要<标识符>
    createKeyedStateBackend(env, stateHandles): AbstractKeyedStateBackend<K>
                           ^
C:\Users\luyan\A
- **错误行**: 3

**问题 #5** (第 551 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm3ehfyagTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend = new EmbeddedRocksDBStateBackend(true);
^
  符号:   类 EmbeddedRocksDBStateBacken
- **错误行**: 4

**问题 #8** (第 718 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt0vc4ucuTempValidation.java:4: 错误: 非法的表达式开始
public boolean restoreSavepoint(
^
C:\Users\luyan\AppData\Local\Temp\tmpt0vc4ucuTempValidation.java:76: 错误: 需要 class、in
- **错误行**: 4

**问题 #10** (第 895 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqnmzvfxbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #11** (第 929 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyyj275vmTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #12** (第 956 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk2d8xbb4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #13** (第 977 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfi7p2fqeTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #14** (第 1014 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj862dnstTempValidation.java:5: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend = new EmbeddedRocksDBStateBackend(true);
^
  符号:   类 EmbeddedRocksDBStateBacken
- **错误行**: 5

**问题 #20** (第 1282 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg2n8urhvTempValidation.java:3: 错误: 需要';'
        new EmbeddedRocksDBStateBackend(true)  // true enables incremental
                                             ^

- **错误行**: 3

**问题 #21** (第 1288 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl6c7zeb5TempValidation.java:3: 错误: 找不到符号
        DefaultConfigurableStateBackend backend = new EmbeddedRocksDBStateBackend(true);
        ^
  符号:   类 DefaultConfig
- **错误行**: 3

**问题 #22** (第 1297 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_ns0pf8rTempValidation.java:3: 错误: 找不到符号
        env.enableCheckpointing(60000);  // 1 minute, reduce frequency
        ^
  符号:   变量 env
  位置: 类 TempValidation
1 个
- **错误行**: 3

**问题 #23** (第 1303 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc6yeq0ysTempValidation.java:3: 错误: 找不到符号
        env.getCheckpointConfig().setPreferCheckpointForRecovery(true);
        ^
  符号:   变量 env
  位置: 类 TempValidation
1
- **错误行**: 3

**问题 #24** (第 1315 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp037vitouTempValidation.java:3: 错误: 找不到符号
        env.getCheckpointConfig().enableUnalignedCheckpoints();
        ^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 3

**问题 #25** (第 1326 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpta_gjfiiTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpta_gjfi
- **错误行**: 3


### `i18n\en\Flink\02-core\delta-join.md`

**问题 #3** (第 250 行, 语言: sql)

- **错误**: 可能的语法问题: -- ENABLE DELTA JOIN OPTIMIZATION IN FLINK SQL
SET...

**问题 #4** (第 323 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsbmxbgicAsyncUserProfileLookup.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<UserEvent> userEvents = env.fromSource(
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luya
- **错误行**: 2

**问题 #9** (第 545 行, 语言: sql)

- **错误**: 可能的语法问题: -- AFTER OPTIMIZATION: PROJECTION PUSHDOWN, ONLY Q...


### `i18n\en\Flink\02-core\exactly-once-semantics-deep-dive.md`

**问题 #4** (第 248 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjjzbl121TempValidation.java:4: 错误: 找不到符号
properties.setProperty("enable.auto.commit", "false");
^
  符号:   变量 properties
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #5** (第 276 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpewq6prrjTempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #6** (第 292 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz5igdv1kTempValidation.java:4: 错误: 找不到符号
String transactionalIdPrefix = jobId + "-" + operatorId;
                               ^
  符号:   变量 jobId
  位置: 类 TempVal
- **错误行**: 4

**问题 #7** (第 317 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp743ef50iTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp743ef50
- **错误行**: 3

**问题 #8** (第 355 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpetn3gbwzTempValidation.java:3: 错误: 找不到符号
        Properties consumerProps = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 3

**问题 #15** (第 926 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprm5aa8c5TempValidation.java:4: 错误: 找不到符号
env.getCheckpointConfig().enableUnalignedCheckpoints(true);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4

**问题 #21** (第 1234 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1lkc8103TempValidation.java:6: 错误: 非法的表达式开始
    private void onCheckpointTimeout(long checkpointId) {
    ^
C:\Users\luyan\AppData\Local\Temp\tmp1lkc8103TempValida
- **错误行**: 6


### `i18n\en\Flink\02-core\network-stack-evolution.md`

**问题 #9** (第 533 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpng7sudr6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `i18n\en\Flink\02-core\state-backend-evolution-analysis.md`

**问题 #2** (第 291 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr5h8ypkdTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #3** (第 315 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_3hit8erTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #5** (第 376 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprovc13geTempValidation.java:4: 错误: 找不到符号
ForStStateBackend forstBackend = new ForStStateBackend();
^
  符号:   类 ForStStateBackend
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #7** (第 434 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwp659pr6EmbeddedRocksDBStateBackend.java:37: 错误: 非法的表达式开始
        );
        ^
1 个错误

- **错误行**: 37

**问题 #8** (第 487 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1ig7qggcForStStateBackend.java:46: 错误: 非法的表达式开始
        );
        ^
1 个错误

- **错误行**: 46


### `i18n\en\Flink\02-core\time-semantics-and-watermark.md`

**问题 #1** (第 306 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwwy18aqoTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwwy18
- **错误行**: 3

**问题 #2** (第 316 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr154fbumTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpr154f
- **错误行**: 3

**问题 #3** (第 326 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprdn0thvbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmprdn0t
- **错误行**: 3

**问题 #6** (第 556 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjm6m8y1pTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpjm6
- **错误行**: 3

**问题 #7** (第 568 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwqo74jyaTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwqo
- **错误行**: 3

**问题 #8** (第 584 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzgnm966eTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpzgnm9
- **错误行**: 3

**问题 #9** (第 595 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr2a13se6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpr2a13
- **错误行**: 3

**问题 #10** (第 606 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxzawu73mTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpxzawu
- **错误行**: 3

**问题 #11** (第 620 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6gc6kzrpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp6gc
- **错误行**: 3


### `i18n\en\Flink\03-api\03.02-table-sql-api\flink-materialized-table-deep-dive.md`

**问题 #2** (第 121 行, 语言: sql)

- **错误**: 可能的语法问题: -- HASH DISTRIBUTION (DEFAULT)
DISTRIBUTED BY HASH...


### `i18n\en\Flink\03-api\03.02-table-sql-api\flink-sql-hints-optimization.md`

**问题 #12** (第 331 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9wvd0r3iTempValidation.java:4: 错误: 找不到符号
tableEnv.createTemporaryFunction("ExtractJson", JsonPathFunction.class);
                                                ^
- **错误行**: 4

**问题 #13** (第 346 行, 语言: sql)

- **错误**: 可能的语法问题: -- BASIC EXECUTION PLAN
EXPLAIN PLAN FOR
SELECT /*...; 可能的语法问题: -- DETAILED EXECUTION PLAN (WITH OPTIMIZER DECISIO...


### `i18n\en\Flink\03-api\03.02-table-sql-api\flink-table-sql-complete-guide.md`

**问题 #7** (第 379 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyh71pc8iTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpyh71pc8iTempV
- **错误行**: 3

**问题 #10** (第 453 行, 语言: sql)

- **错误**: 可能的语法问题: -- SWITCH DATABASE
USE ANALYTICS;...

**问题 #13** (第 508 行, 语言: sql)

- **错误**: 可能的语法问题: <!-- THE FOLLOWING SYNTAX IS CONCEPTUAL DESIGN; AC...

**问题 #19** (第 591 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq0ly4c9zTempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.from("orders")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpq0ly4
- **错误行**: 4

**问题 #24** (第 685 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6_e9tkvqTempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.from("user_events")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #32** (第 821 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdrjm0ye5TempValidation.java:4: 错误: 找不到符号
Table topN = tableEnv.from("product_sales")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #39** (第 969 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplv38z7uxTempValidation.java:4: 错误: 找不到符号
Table windowed = tableEnv.from("user_events")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4

**问题 #44** (第 1077 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2g0nqnanTempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.from("orders")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp2g0nq
- **错误行**: 4

**问题 #53** (第 1383 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp27qflaw6TempValidation.java:12: 错误: 非法的表达式开始
    .next("C").where(...)
                     ^
C:\Users\luyan\AppData\Local\Temp\tmp27qflaw6TempValidation.java:13:
- **错误行**: 12

**问题 #64** (第 1660 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe3cn5rsxTempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql(
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #66** (第 1724 行, 语言: sql)

- **错误**: 可能的语法问题: -- CREATE EMBEDDING MODEL
<!-- THE FOLLOWING SYNTA...; 可能的语法问题: -- CREATE CLASSIFICATION MODEL
~~CREATE MODEL SENT...

**问题 #76** (第 2082 行, 语言: sql)
- **错误**: 可能的语法问题: -- 1. CONFIGURE STATE TTL
SET 'TABLE.EXEC.STATE.TT...; 可能的语法问题: -- 3. INCREMENTAL CHECKPOINT
SET 'STATE.BACKEND.IN...; 可能的语法问题: -- 4. ROCKSDB TUNING
SET 'STATE.BACKEND.ROCKSDB.PR...

**问题 #77** (第 2100 行, 语言: sql)
- **错误**: 可能的语法问题: -- 1. REASONABLE WATERMARK DELAY
-- TOO SMALL: DAT...; 可能的语法问题: -- 3. ALLOW LATE DATA
SET 'TABLE.EXEC.EMIT.ALLOW-L...


### `i18n\en\Flink\03-api\03.02-table-sql-api\sql-vs-datastream-comparison.md`

**问题 #3** (第 274 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprf4e3wa1TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.functions.AggregateFunction;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #5** (第 309 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph48mnfw1TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmph48mnfw1TempValidatio
- **错误行**: 4

**问题 #6** (第 331 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaq4bnz69AsyncUserEnrichment.java:23: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedOrder> enriched = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以启用 未命名类
- **错误行**: 23

**问题 #7** (第 365 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx43jw17sTempValidation.java:4: 错误: 找不到符号
tableEnv.createTemporaryView("orders", orderStream);
                                       ^
  符号:   变量 orderStream
  位置:
- **错误行**: 4


### `i18n\en\Flink\03-api\09-language-foundations\03-rust-native.md`

**问题 #7** (第 458 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmo1q9s3gTempValidation.java:4: 错误: 找不到符号
    stream,
    ^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpmo1q9s3gTempValidation.jav
- **错误行**: 4


### `i18n\en\Flink\04-runtime\04.01-deployment\evolution\config-management.md`

**问题 #1** (第 55 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprsfpgyekTempValidation.java:3: 错误: 找不到符号
ConfigManager cm = ConfigManager.getInstance();
^
  符号:   类 ConfigManager
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 3


### `i18n\en\Flink\04-runtime\04.01-deployment\evolution\scheduling-evolution.md`

**问题 #2** (第 308 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbuoo_18dTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #3** (第 327 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr04vfe4qTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #4** (第 346 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp43o_jn6gTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #5** (第 369 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmporaqbiu8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #6** (第 399 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjyp9o16kTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `i18n\en\Flink\04-runtime\04.01-deployment\evolution\yarn-deploy.md`

**问题 #3** (第 65 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_b1frgb9TempValidation.java:3: 错误: 找不到符号
        env.getConfig().setAutoWatermarkInterval(200);
        ^
  符号:   变量 env
  位置: 类 TempValidation
1 个错误

- **错误行**: 3


### `i18n\en\Flink\04-runtime\04.01-deployment\flink-kubernetes-autoscaler-deep-dive.md`

**问题 #19** (第 478 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 12, column 78:
     ... ."Source: Kafka".max-parallelism: "12"
                                         ^ (line: 12)
- **错误行**: 12
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `i18n\en\Flink\04-runtime\04.01-deployment\flink-serverless-architecture.md`

**问题 #6** (第 262 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4qofj62xTempValidation.java:5: 错误: 需要';'
public Response handle(Request req) {
                      ^
C:\Users\luyan\AppData\Local\Temp\tmp4qofj62xTempValidation.
- **错误行**: 5


### `i18n\en\Flink\04-runtime\04.03-observability\evolution\alerting-evolution.md`

**问题 #2** (第 72 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw92y_ws7TempValidation.java:3: 错误: 找不到符号
        AlertManager.register(new AlertRule()
        ^
  符号:   变量 AlertManager
  位置: 类 TempValidation
C:\Users\luyan\AppD
- **错误行**: 3


### `i18n\en\Flink\04-runtime\04.03-observability\evolution\logging-evolution.md`

**问题 #2** (第 62 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1qks5vjoTempValidation.java:3: 错误: 找不到符号
        LOG.info("Processing event",
        ^
  符号:   变量 LOG
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3


### `i18n\en\Flink\04-runtime\04.03-observability\evolution\metrics-evolution.md`

**问题 #2** (第 63 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8g7ool2qTempValidation.java:3: 错误: 找不到符号
        getRuntimeContext()
        ^
  符号:   方法 getRuntimeContext()
  位置: 类 TempValidation
1 个错误

- **错误行**: 3


### `i18n\en\Flink\04-runtime\04.03-observability\evolution\slo-evolution.md`

**问题 #2** (第 72 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptff7jtv2TempValidation.java:3: 错误: 找不到符号
        double errorBudget = 1 - slo.getTarget();
                                 ^
  符号:   变量 slo
  位置: 类 TempValidation
- **错误行**: 3


### `i18n\en\Flink\04-runtime\04.03-observability\evolution\testing-evolution.md`

**问题 #1** (第 61 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp52s9ysejTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmp52
- **错误行**: 4

**问题 #2** (第 81 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgaw6oat4TempValidation.java:3: 错误: 找不到符号
        MiniCluster cluster = new MiniCluster(
        ^
  符号:   类 MiniCluster
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3


### `i18n\en\Flink\04-runtime\04.03-observability\evolution\tracing-evolution.md`

**问题 #2** (第 70 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp37qfyy0gTempValidation.java:3: 错误: 找不到符号
Span span = tracer.spanBuilder("process").startSpan();
^
  符号:   类 Span
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 3


### `i18n\en\Flink\04-runtime\04.03-observability\evolution\webui-evolution.md`

**问题 #1** (第 55 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp56ip8382TempValidation.java:3: 错误: 非法的表达式开始
        GET /jobs/{jobid}/vertices
                  ^
C:\Users\luyan\AppData\Local\Temp\tmp56ip8382TempValidation.java
- **错误行**: 3


### `i18n\en\Flink\05-ecosystem\05.01-connectors\diskless-kafka-deep-dive.md`

**问题 #2** (第 113 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc90kz1lhTempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #3** (第 142 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps28o9la2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #5** (第 240 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcylswv8cTempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3


### `i18n\en\Flink\05-ecosystem\05.01-connectors\evolution\cdc-connector.md`

**问题 #1** (第 65 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuqkisdueTempValidation.java:3: 错误: 找不到符号
        MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
        ^
  符号:   类 MySqlSource
  位置: 类 TempValida
- **错误行**: 3

**问题 #2** (第 81 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpghwh4yt6TempValidation.java:3: 错误: 找不到符号
stream.process(new ProcessFunction<String, Row>() {
                   ^
  符号:   类 ProcessFunction
  位置: 类 TempValidation

- **错误行**: 3


### `i18n\en\Flink\05-ecosystem\05.01-connectors\evolution\cloud-connector.md`

**问题 #1** (第 63 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2nxkyv3eTempValidation.java:3: 错误: 找不到符号
        env.getConfig().setDefaultFileSystemScheme("s3://");
        ^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 3

**问题 #2** (第 75 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5ou3w_u0TempValidation.java:3: 错误: 找不到符号
        FlinkKinesisConsumer<String> consumer = new FlinkKinesisConsumer<>(
        ^
  符号:   类 FlinkKinesisConsumer
  位置:
- **错误行**: 3


### `i18n\en\Flink\05-ecosystem\05.01-connectors\evolution\file-connector.md`

**问题 #1** (第 64 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxxwcxx8oTempValidation.java:3: 错误: 找不到符号
        FileSource<String> source = FileSource
        ^
  符号:   类 FileSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3

**问题 #2** (第 77 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsehqlm36TempValidation.java:3: 错误: 找不到符号
        FileSink<GenericRecord> sink = FileSink
        ^
  符号:   类 FileSink
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 3


### `i18n\en\Flink\05-ecosystem\05.01-connectors\evolution\jdbc-connector.md`

**问题 #1** (第 63 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkquiv0niTempValidation.java:3: 错误: 找不到符号
        JdbcSourceBuilder<Row> builder = JdbcSourceBuilder.<Row>builder()
        ^
  符号:   类 JdbcSourceBuilder
  位置: 类 Te
- **错误行**: 3

**问题 #2** (第 75 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc9vg5u8oTempValidation.java:3: 错误: 找不到符号
JdbcSink.sink(
^
  符号:   变量 JdbcSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpc9vg5u8oTempValidation.ja
- **错误行**: 3


### `i18n\en\Flink\05-ecosystem\05.01-connectors\evolution\kafka-connector.md`

**问题 #1** (第 62 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuu1cj8mcTempValidation.java:3: 错误: 找不到符号
        KafkaSource<String> source = KafkaSource.<String>builder()
        ^
  符号:   类 KafkaSource
  位置: 类 TempValidation

- **错误行**: 3

**问题 #2** (第 76 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5ryu1_mnTempValidation.java:3: 错误: 找不到符号
        KafkaSink<String> sink = KafkaSink.<String>builder()
        ^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users
- **错误行**: 3


### `i18n\en\Flink\05-ecosystem\05.01-connectors\evolution\lakehouse-connector.md`

**问题 #1** (第 67 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkcl62z6qTempValidation.java:5: 错误: 找不到符号
    .withOverwritePartition(partition)
                            ^
  符号:   变量 partition
  位置: 类 TempValidation
C:\Users\
- **错误行**: 5


### `i18n\en\Flink\05-ecosystem\05.01-connectors\evolution\mq-connector.md`

**问题 #1** (第 64 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfogwlsyaTempValidation.java:3: 错误: 找不到符号
        PulsarSource<String> source = PulsarSource.builder()
        ^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Us
- **错误行**: 3

**问题 #2** (第 79 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4kkph1tcTempValidation.java:3: 错误: 找不到符号
        RMQSink<String> sink = new RMQSink<>(
        ^
  符号:   类 RMQSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 3


### `i18n\en\Flink\05-ecosystem\05.01-connectors\evolution\nosql-connector.md`

**问题 #1** (第 65 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsf9dm6v6TempValidation.java:3: 错误: 找不到符号
        HBaseSinkFunction<Row> sink = new HBaseSinkFunction<>(
        ^
  符号:   类 HBaseSinkFunction
  位置: 类 TempValidatio
- **错误行**: 3

**问题 #2** (第 78 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp390ykgliTempValidation.java:3: 错误: 找不到符号
        MongoDBSource<String> source = MongoDBSource.<String>builder()
        ^
  符号:   类 MongoDBSource
  位置: 类 TempValid
- **错误行**: 3


### `i18n\en\Flink\05-ecosystem\05.01-connectors\pulsar-connector-guide.md`

**问题 #3** (第 212 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzbic_y19TempValidation.java:4: 错误: 找不到符号
PulsarSource<String> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #4** (第 230 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph0xcokypTempValidation.java:4: 错误: 找不到符号
PulsarSink<String> sink = PulsarSink.builder()
^
  符号:   类 PulsarSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #9** (第 373 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjr15ng42EnrichedStreamProcessing.java:18: 错误: 非法的表达式开始
            .setDeserializationSchema(...)
                                      ^
C:\Users\luyan\AppData\Lo
- **错误行**: 18

**问题 #10** (第 409 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5milup8zTempValidation.java:4: 错误: 找不到符号
PulsarSource<String> optimizedSource = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #11** (第 447 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv79fnln4SchemaEvolutionExample.java:24: 错误: 非法的表达式开始
        DataStream<EventV2> stream = env.fromSource(source, ...)

- **错误行**: 24


### `i18n\en\Flink\05-ecosystem\05.01-connectors\pulsar-integration-guide.md`

**问题 #3** (第 212 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkpd0b685TempValidation.java:4: 错误: 找不到符号
PulsarSource<String> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #4** (第 230 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7kulp5bdTempValidation.java:4: 错误: 找不到符号
PulsarSink<String> sink = PulsarSink.builder()
^
  符号:   类 PulsarSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #9** (第 373 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4usqadv_EnrichedStreamProcessing.java:18: 错误: 非法的表达式开始
            .setDeserializationSchema(...)
                                      ^
C:\Users\luyan\AppData\Lo
- **错误行**: 18

**问题 #10** (第 409 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp9qh0ds4TempValidation.java:4: 错误: 找不到符号
PulsarSource<String> optimizedSource = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #11** (第 447 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6vz0phasSchemaEvolutionExample.java:24: 错误: 非法的表达式开始
        DataStream<EventV2> stream = env.fromSource(source, ...)

- **错误行**: 24


### `i18n\en\Flink\05-ecosystem\05.04-graph\flink-gelly-streaming-graph-processing.md`

**问题 #3** (第 269 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplzxvu0zuTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmplzxvu0zuTempValidat
- **错误行**: 4

**问题 #4** (第 313 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj6w30cswTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpj6w
- **错误行**: 3

**问题 #5** (第 352 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4dujrherVertexState.java:14: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Edge<Long, Double>> edgeStream = ...;
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Lo
- **错误行**: 14

**问题 #6** (第 443 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoxnovtgtTempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend rocksDbBackend = new RocksDBStateBackend(
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempValidation
C:\Us
- **错误行**: 4


### `i18n\en\Flink\05-ecosystem\05.04-graph\flink-gelly.md`

**问题 #3** (第 173 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8vd8g445TempValidation.java:4: 错误: 找不到符号
Graph<Long, Double, Double> bipartiteGraph = Graph.fromDataSet(
^
  符号:   类 Graph
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #4** (第 204 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0_w7rhcjTempValidation.java:4: 错误: 非法的表达式开始
Graph<String, AccountInfo, Transaction> transactionGraph = ...;

- **错误行**: 4

**问题 #5** (第 225 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp04pk2ljfTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp04p
- **错误行**: 3


### `i18n\en\Flink\05-ecosystem\ecosystem\kafka-streams-migration.md`

**问题 #2** (第 76 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwcz7yoybTempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #3** (第 83 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsd3bz0avTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #4** (第 108 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr8xkpo4oTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpr8xkpo4oTemp
- **错误行**: 3

**问题 #5** (第 133 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplxhytmhnTempValidation.java:3: 错误: 找不到符号
        KStream<String, Integer> transformed = stream
        ^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3

**问题 #6** (第 143 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8rqy1iqpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8rq
- **错误行**: 3

**问题 #7** (第 156 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0u4z5dp2TempValidation.java:3: 错误: 找不到符号
        Table transformed = tableEnv.from("input_table")
        ^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 3

**问题 #8** (第 172 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4esgojc0TempValidation.java:3: 错误: 找不到符号
        KTable<String, Long> counts = stream
        ^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 3

**问题 #9** (第 180 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp91zopobtTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp91zopobtTempValidat
- **错误行**: 4

**问题 #10** (第 221 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0wr6efc8TempValidation.java:3: 错误: 找不到符号
        KStream<String, String> joined = stream1.join(
        ^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 3

**问题 #11** (第 232 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjr6czbicTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpjr6
- **错误行**: 3

**问题 #12** (第 247 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2gxfzr8cTempValidation.java:3: 错误: 找不到符号
        Table joined = table1
        ^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp2gxfzr
- **错误行**: 3

**问题 #16** (第 337 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0zlxajv0TempValidation.java:3: 错误: 找不到符号
        properties.put(StreamsConfig.NUM_STREAM_THREADS_CONFIG, 4);
                       ^
  符号:   变量 StreamsConfig
  位置
- **错误行**: 3

**问题 #17** (第 343 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvo80m370TempValidation.java:6: 错误: 非法的表达式开始
stream.map(...).setParallelism(2);
           ^
1 个错误

- **错误行**: 6

**问题 #18** (第 354 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp639cfzl_TempValidation.java:3: 错误: 找不到符号
        properties.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG,
                       ^
  符号:   变量 StreamsConfig
  位置:
- **错误行**: 3

**问题 #19** (第 362 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1ow4s0wsTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1ow4s0w
- **错误行**: 3

**问题 #20** (第 384 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprqhzepvsTempValidation.java:4: 错误: 需要';'
public void testTopology() {
                        ^
C:\Users\luyan\AppData\Local\Temp\tmprqhzepvsTempValidation.java:8:
- **错误行**: 4

**问题 #21** (第 402 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk39z62p9TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpk3
- **错误行**: 4

**问题 #22** (第 429 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxmdj6u7oTempValidation.java:4: 错误: 需要';'
public void testMigrationParity() {
                               ^
1 个错误

- **错误行**: 4


### `i18n\en\Flink\05-ecosystem\ecosystem\materialize-comparison.md`

**问题 #4** (第 117 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpntfs82pkTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpntf
- **错误行**: 3

**问题 #5** (第 136 行, 语言: sql)
- **错误**: 可能的语法问题: -- AUTOMATIC MAINTENANCE, AUTOMATIC INDEXING...

**问题 #10** (第 321 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpynf73yhvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpynf
- **错误行**: 3


### `i18n\en\Flink\05-ecosystem\ecosystem\pulsar-functions-integration.md`

**问题 #2** (第 80 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9jwkw7qmTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9jw
- **错误行**: 3

**问题 #3** (第 107 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpovyt6dryTempValidation.java:3: 错误: 找不到符号
        PulsarSink<String> sink = PulsarSink.builder()
        ^
  符号:   类 PulsarSink
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 3

**问题 #9** (第 243 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeejbzu_6TempValidation.java:4: 错误: 找不到符号
Schema<OrderEvent> schema = Schema.AVRO(OrderEvent.class);
^
  符号:   类 Schema
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #10** (第 254 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgob1nhl9TempValidation.java:4: 错误: 找不到符号
PulsarSource<OrderEvent> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #11** (第 271 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphbxtlx20TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmphbxtlx2
- **错误行**: 3

**问题 #12** (第 288 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwe1dq1epTempValidation.java:4: 错误: 找不到符号
PulsarSource<String> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4


### `i18n\en\Flink\05-ecosystem\ecosystem\risingwave-integration-guide.md`

**问题 #2** (第 87 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw51a285pTempValidation.java:4: 错误: 找不到符号
JdbcSink.sink(
^
  符号:   变量 JdbcSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpw51a285pTempValidation.ja
- **错误行**: 4

**问题 #4** (第 131 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp64r3p77oTempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp64
- **错误行**: 4

**问题 #8** (第 248 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy2349u57TempValidation.java:4: 错误: 找不到符号
TwoPhaseCommitSinkFunction<Event, JdbcConnection, Void> exactlyOnceSink =
^
  符号:   类 TwoPhaseCommitSinkFunction
  位置: 类 T
- **错误行**: 4

**问题 #9** (第 285 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdsx4mozeTempValidation.java:4: 错误: 找不到符号
JdbcExecutionOptions executionOptions = JdbcExecutionOptions.builder()
^
  符号:   类 JdbcExecutionOptions
  位置: 类 TempValida
- **错误行**: 4

**问题 #12** (第 363 行, 语言: sql)
- **错误**: 可能的语法问题: -- PROCESS IN FLINK
TABLE PROCESSED = TABLEENV.SQL...; 可能的语法问题: -- SINK TO RISINGWAVE
TABLEENV.EXECUTESQL(
    "CR...; 可能的语法问题: PROCESSED.EXECUTEINSERT("RISINGWAVE_SINK");...


### `i18n\en\Flink\06-ai-ml\ai-ml\evolution\a2a-protocol.md`

**问题 #1** (第 54 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjqbfskrjTempValidation.java:3: 错误: 找不到符号
        A2AMessage msg = A2AMessage.builder()
        ^
  符号:   类 A2AMessage
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 3

**问题 #2** (第 66 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp63zu31hnTempValidation.java:3: 错误: 找不到符号
        agent1.delegate(task, agent2);
                        ^
  符号:   变量 task
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 3


### `i18n\en\Flink\06-ai-ml\ai-ml\evolution\ai-agent-24.md`

**问题 #2** (第 56 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6x9nbes0TempValidation.java:3: 错误: 找不到符号
        Agent agent = Agent.newBuilder()
        ^
  符号:   类 Agent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 3

**问题 #3** (第 67 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmywitp9zTempValidation.java:4: 错误: 找不到符号
    .addSink(new ActionSink());
                 ^
  符号:   类 ActionSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4


### `i18n\en\Flink\06-ai-ml\ai-ml\evolution\ai-agent-25.md`

**问题 #1** (第 58 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzpenln7eTempValidation.java:3: 错误: 找不到符号
        MultiAgentSystem system = MultiAgentSystem.builder()
        ^
  符号:   类 MultiAgentSystem
  位置: 类 TempValidation
C
- **错误行**: 3

**问题 #2** (第 69 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsfx7hxmiTempValidation.java:3: 错误: 找不到符号
system.coordinate(event, (detector, diagnoser) -> {
                  ^
  符号:   变量 event
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 3


### `i18n\en\Flink\06-ai-ml\ai-ml\evolution\ai-agent-30.md`

**问题 #3** (第 69 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3xfzyuglTempValidation.java:4: 错误: 找不到符号
    .toSink(AlertSink.class);
            ^
  符号:   类 AlertSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4


### `i18n\en\Flink\06-ai-ml\ai-ml\evolution\feature-store.md`

**问题 #1** (第 53 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps2l_g0lkTempValidation.java:3: 错误: 找不到符号
        FeatureVector fv = featureStore.getOnlineFeatures(entityId, features);
        ^
  符号:   类 FeatureVector
  位置: 类 T
- **错误行**: 3

**问题 #2** (第 61 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6bs8ug4mTempValidation.java:3: 错误: 找不到符号
stream.map(event -> {
^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp6bs8ug4mTempValidati
- **错误行**: 3


### `i18n\en\Flink\06-ai-ml\ai-ml\evolution\llm-integration.md`

**问题 #1** (第 61 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2gsfr0uxTempValidation.java:3: 错误: 找不到符号
llmClient.completeStream(prompt, token -> {
                         ^
  符号:   变量 prompt
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 3

**问题 #2** (第 71 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwpccok2bTempValidation.java:3: 错误: 找不到符号
        stream.map(new LLMMapFunction("gpt-4", promptTemplate));
                       ^
  符号:   类 LLMMapFunction
  位置: 类
- **错误行**: 3


### `i18n\en\Flink\06-ai-ml\ai-ml\evolution\ml-inference.md`

**问题 #1** (第 55 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjvpw3807TempValidation.java:3: 错误: 找不到符号
        SavedModelBundle model = SavedModelBundle.load("/path/to/model");
        ^
  符号:   类 SavedModelBundle
  位置: 类 Tem
- **错误行**: 3

**问题 #2** (第 64 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5kyrwvctTempValidation.java:4: 错误: 找不到符号
    .setParallelism(gpuCount);
                    ^
  符号:   变量 gpuCount
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4


### `i18n\en\Flink\06-ai-ml\ai-ml\evolution\model-serving.md`

**问题 #2** (第 52 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuzwut7deTempValidation.java:3: 错误: 找不到符号
        ModelRouter router = new ModelRouter()
        ^
  符号:   类 ModelRouter
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3

**问题 #3** (第 62 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphexixo19TempValidation.java:3: 错误: 找不到符号
        ModelVersion version = registry.getLatest("fraud-detection");
        ^
  符号:   类 ModelVersion
  位置: 类 TempValidat
- **错误行**: 3


### `i18n\en\Flink\06-ai-ml\ai-ml\evolution\vector-search.md`

**问题 #1** (第 61 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzciaio6nTempValidation.java:3: 错误: 找不到符号
        VectorIndex index = new HNSWIndex.Builder()
        ^
  符号:   类 VectorIndex
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 3

**问题 #2** (第 72 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmwypmamzTempValidation.java:3: 错误: 找不到符号
        List<Vector> results = index.search(queryVector, 10);
        ^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 3


### `i18n\en\Flink\06-ai-ml\flink-ml-architecture.md`

**问题 #3** (第 235 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp11r49zeTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `i18n\en\Flink\06-ai-ml\model-serving-streaming.md`

**问题 #3** (第 266 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxa7vh195TFServingAsyncFunction.java:47: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Prediction> predictions = featureStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 47


### `i18n\en\Flink\06-ai-ml\realtime-feature-engineering-guide.md`

**问题 #2** (第 346 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc8bhruz0UserBehaviorAggregator.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<FeatureVector> features = events
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppDa
- **错误行**: 1

**问题 #3** (第 396 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpedo73cpjSessionFeatureProcessFunction.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<SessionFeatures> sessionFeatures = events
^
  （请使用 --enable-preview 以启用 未命名类）
C:\U
- **错误行**: 1


### `i18n\en\Flink\06-ai-ml\vector-database-integration.md`

**问题 #1** (第 33 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxkt1rb_tinterface.java:2: 错误: 找不到符号
interface VectorSink<T> extends RichSinkFunction<T> {
                                ^
  符号: 类 RichSinkFunction
C:\Users\luyan
- **错误行**: 2

**问题 #5** (第 273 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplzxcqubaTempValidation.java:5: 错误: 找不到符号
List<VectorRecord> candidates = milvus.search(queryVector, topK=100);
^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 5

**问题 #8** (第 350 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpax497h29TempValidation.java:4: 错误: 需要';'
CREATE TABLE vector_items (
            ^
C:\Users\luyan\AppData\Local\Temp\tmpax497h29TempValidation.java:5: 错误: 需要')'或',
- **错误行**: 4

**问题 #11** (第 460 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8wph3pqxMilvusLookupFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
TableResult result = tEnv.sqlQuery("""
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #13** (第 539 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppsece5xdTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmppsece5xdTempValidat
- **错误行**: 4


### `i18n\en\Flink\07-rust-native\risingwave-comparison\01-risingwave-architecture.md`

**问题 #5** (第 357 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxldalzevTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpxld
- **错误行**: 3


### `i18n\en\Flink\07-rust-native\risingwave-comparison\02-nexmark-head-to-head.md`

**问题 #8** (第 423 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgr6fhzjoTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpgr6
- **错误行**: 3

**问题 #15** (第 614 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 3, column 12:
      resources:
               ^ (line: 3)
- **错误行**: 3
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `i18n\en\Flink\07-rust-native\risingwave-comparison\04-risingwave-rust-udf-guide.md`

**问题 #17** (第 462 行, 语言: sql)
- **错误**: 可能的语法问题: -- RESULT:
-- KEY    | VALUE | IS_NUMERIC
-- -----...

**问题 #24** (第 740 行, 语言: sql)
- **错误**: 可能的语法问题: -- 2. GRADUALLY INCREASE COMPLEXITY
-- 3. USE EXPL...


### `i18n\en\Flink\07-rust-native\simd-optimization\03-jni-assembly-bridge.md`

**问题 #1** (第 51 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8t40b8oqTempValidation.java:4: 错误: 找不到符号
VectorSpecies<Float> SPECIES = FloatVector.SPECIES_256;
^
  符号:   类 VectorSpecies
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #2** (第 143 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5zzdmb85TempValidation.java:4: 错误: 找不到符号
long address = unsafe.allocateMemory(size + 32);
                                     ^
  符号:   变量 size
  位置: 类 TempValida
- **错误行**: 4


### `i18n\en\Flink\08-roadmap\08.01-flink-24\2026-q2-flink-tasks.md`

**问题 #13** (第 480 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph92y_ocuTempValidation.java:4: 错误: 找不到符号
for (KeyGroup kg : keyGroups) {
                   ^
  符号:   变量 keyGroups
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 4


### `i18n\en\Flink\08-roadmap\08.01-flink-24\community-dynamics-tracking.md`

**问题 #15** (第 431 行, 语言: yaml)
- **错误**: sequence entries are not allowed here
  in "<unicode string>", line 4, column 54:
     ... park to Flink: Lessons Learned" - 12K views
                                         ^ (line: 4)
- **错误行**: 4


### `i18n\en\Flink\08-roadmap\08.01-flink-24\flink-2.1-frontier-tracking.md`

**问题 #4** (第 419 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn1yjsy9dTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4


### `i18n\en\Flink\08-roadmap\08.01-flink-24\flink-2.3-2.4-roadmap.md`

**问题 #11** (第 321 行, 语言: yaml)
- **错误**: while parsing a block collection
  in "<unicode string>", line 9, column 7:
          - JOB_MANAGER_RPC_ADDRESS=jobmanager
          ^ (line: 9)
expected <block end>, but found '<scalar>'
  in "<unico
- **错误行**: 9


### `i18n\en\Flink\08-roadmap\08.01-flink-24\flink-2.5-preview.md`

**问题 #1** (第 49 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 1, column 43:
     ... Release: 2026 Q3 (Feature Freeze: 2026-07, GA: 2026-09)
                                         ^ (line: 1)
- **错误行**: 1
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #3** (第 104 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 1, column 33:
    FLIP: FLIP-442 "Serverless Flink: Zero-to-Infinity Scaling"
                                    ^ (line: 1)
- **错误行**: 1
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #12** (第 439 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiex03wepTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #14** (第 522 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj7ya4ocxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpj7ya4ocxTemp
- **错误行**: 3


### `i18n\en\Flink\08-roadmap\08.02-flink-25\flink-25-features-preview.md`

**问题 #2** (第 45 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo65oq6axTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpo65
- **错误行**: 3

**问题 #7** (第 147 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvivn47doTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpviv
- **错误行**: 3

**问题 #8** (第 167 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdhfjl3ydTempValidation.java:4: 错误: 找不到符号
InferenceConfig config = InferenceConfig.builder()
^
  符号:   类 InferenceConfig
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #14** (第 271 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp8ll61xpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpp8ll61xpTemp
- **错误行**: 3


### `i18n\en\Flink\08-roadmap\08.02-flink-25\flink-25-migration-guide.md`

**问题 #7** (第 142 行, 语言: yaml)
- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    execution.runtime-mode: adaptive ...
    ^ (line: 2)
found duplicate key "execution.runtime-mode" with value "streaming" (o
- **错误行**: 2

**问题 #8** (第 158 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmumdz6u6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #9** (第 186 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpubsdtnnoTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpubsdtnnoTemp
- **错误行**: 3


### `i18n\en\Flink\08-roadmap\08.02-flink-25\flink-25-roadmap.md`

**问题 #1** (第 23 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 3, column 19:
      - Feature Freeze: 2026-07
                      ^ (line: 3)
- **错误行**: 3
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #2** (第 52 行, 语言: yaml)
- **错误**: while parsing a block collection
  in "<unicode string>", line 3, column 5:
        - Unified execution plan generator
        ^ (line: 3)
expected <block end>, but found '?'
  in "<unicode string>",
- **错误行**: 3

**问题 #3** (第 87 行, 语言: yaml)
- **错误**: while parsing a block collection
  in "<unicode string>", line 3, column 5:
        - Release resources to 0 when no ...
        ^ (line: 3)
expected <block end>, but found '?'
  in "<unicode string>
- **错误行**: 3

**问题 #4** (第 120 行, 语言: yaml)
- **错误**: while parsing a block collection
  in "<unicode string>", line 3, column 5:
        - Dynamic batching
        ^ (line: 3)
expected <block end>, but found '?'
  in "<unicode string>", line 6, column 5
- **错误行**: 3


### `i18n\en\Flink\09-practices\09.01-case-studies\case-iot-stream-processing.md`

**问题 #3** (第 261 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps6ek7bg0TempValidation.java:4: 错误: 找不到符号
    .<SensorEvent>forBoundedOutOfOrderness(Duration.ofSeconds(10))
      ^
  符号:   类 SensorEvent
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #5** (第 342 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9h3hr1fhTempValidation.java:4: 错误: 找不到符号
    .<SensorEvent>forBoundedOutOfOrderness(Duration.ofSeconds(10))
      ^
  符号:   类 SensorEvent
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #6** (第 369 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0fb1wr6yTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp0fb1w
- **错误行**: 3


### `i18n\en\Flink\09-practices\09.02-benchmarking\performance-benchmarking-guide.md`

**问题 #6** (第 258 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkgctk74sTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpkgc
- **错误行**: 3

**问题 #7** (第 306 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnk1lo8nuTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnk1
- **错误行**: 3

**问题 #9** (第 368 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9ligx24eTempValidation.java:4: 错误: 找不到符号
MetricGroup metricGroup = getRuntimeContext()
^
  符号:   类 MetricGroup
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #18** (第 614 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6nys_ldbTempValidation.java:5: 错误: 非法的表达式开始
    .window(...)  // Phase 1
            ^
C:\Users\luyan\AppData\Local\Temp\tmp6nys_ldbTempValidation.java:8: 错误: 非法的表
- **错误行**: 5

**问题 #19** (第 626 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp20471_g1TempValidation.java:4: 错误: 找不到符号
stream.map(event -> {
^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp20471_g1TempValidati
- **错误行**: 4


### `i18n\en\Flink\09-practices\09.02-benchmarking\streaming-benchmarks.md`

**问题 #4** (第 302 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd3dxwfutTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `i18n\en\Flink\09-practices\09.03-performance-tuning\05-vs-competitors\flink-vs-risingwave-deep-dive.md`

**问题 #7** (第 326 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwkjbup8dTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwkj
- **错误行**: 3


### `i18n\en\Flink\09-practices\09.03-performance-tuning\05-vs-competitors\linkedin-samza-deep-dive.md`

**问题 #8** (第 339 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiew9n4seWordCountTask.java:24: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Tuple2<String, Integer>> wordCounts =
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 24

**问题 #10** (第 422 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo8gvsuaqTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpo8g
- **错误行**: 3

**问题 #11** (第 438 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1hgt8276TempValidation.java:8: 错误: 非法的表达式开始
public void processActivity(MemberEvent event, MessageCollector collector) {
^
C:\Users\luyan\AppData\Local\Temp\tmp1hg
- **错误行**: 8

**问题 #12** (第 455 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpblmxc4whTempValidation.java:3: 错误: 找不到符号
        Table memberProfile = tableEnv.fromDataStream(profileStream)
        ^
  符号:   类 Table
  位置: 类 TempValidation
C:\U
- **错误行**: 3


### `i18n\en\Flink\09-practices\09.03-performance-tuning\performance-tuning-guide.md`

**问题 #3** (第 304 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph9x_4ae2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmph9x
- **错误行**: 3

**问题 #4** (第 324 行, 语言: yaml)
- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    execution.checkpointing.unaligne ...
    ^ (line: 2)
found duplicate key "execution.checkpointing.interval" with value "600
- **错误行**: 2


### `i18n\en\Flink\09-practices\09.03-performance-tuning\state-backend-selection.md`

**问题 #1** (第 344 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9bhvxp00TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #2** (第 370 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3r3mcx6sTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend backend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #3** (第 391 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcvum23tcTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend backend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #5** (第 432 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3iocl4aeTempValidation.java:3: 错误: 找不到符号
        conf.setString("taskmanager.memory.managed.size", "64mb");  // Too small!
        ^
  符号:   变量 conf
  位置: 类 TempVa
- **错误行**: 3

**问题 #6** (第 440 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqoh031wzTempValidation.java:3: 错误: 找不到符号
        conf.setString("taskmanager.memory.managed.fraction", "0.4");
        ^
  符号:   变量 conf
  位置: 类 TempValidation
C:\
- **错误行**: 3


### `i18n\en\Flink\09-practices\09.04-security\security\evolution\audit-evolution.md`

**问题 #2** (第 71 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe8lg364_TempValidation.java:3: 错误: 找不到符号
        auditLog.record(new AuditEvent()
        ^
  符号:   变量 auditLog
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 3


### `i18n\en\Flink\09-practices\09.04-security\security\evolution\auth-evolution.md`

**问题 #2** (第 71 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps_kzxl_bTempValidation.java:3: 错误: 找不到符号
        OAuth2Client client = new OAuth2Client()
        ^
  符号:   类 OAuth2Client
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3


### `i18n\en\Flink\09-practices\09.04-security\security\evolution\authorization-evolution.md`

**问题 #2** (第 74 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_4dsjkrcTempValidation.java:3: 错误: 找不到符号
if (authorizer.hasPermission(user, "jobs:cancel", jobId)) {
                             ^
  符号:   变量 user
  位置: 类 TempVal
- **错误行**: 3


### `i18n\en\Flink\09-practices\09.04-security\security\evolution\compliance-evolution.md`

**问题 #2** (第 76 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg2u1ebbmTempValidation.java:4: 错误: 此处不允许使用修饰符private
private String ssn;
               ^
C:\Users\luyan\AppData\Local\Temp\tmpg2u1ebbmTempValidation.java:3: 错误: 找
- **错误行**: 4


### `i18n\en\Flink\09-practices\09.04-security\security\evolution\data-governance-evolution.md`

**问题 #1** (第 62 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4xe7q34wTempValidation.java:3: 错误: 找不到符号
        LineageRecorder.record(new DataLineage()
        ^
  符号:   变量 LineageRecorder
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 3


### `i18n\en\Flink\09-practices\09.04-security\security\evolution\encryption-evolution.md`

**问题 #2** (第 71 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxyx8_mnjTempValidation.java:3: 错误: 找不到符号
        KeyVault vault = KeyVault.create(config);
        ^
  符号:   类 KeyVault
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3


### `i18n\en\Flink\09-practices\09.04-security\security\evolution\key-management-evolution.md`

**问题 #1** (第 61 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpruib5c8lTempValidation.java:3: 错误: 找不到符号
        Vault vault = Vault.builder()
        ^
  符号:   类 Vault
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 3


### `i18n\en\Flink\09-practices\09.04-security\security\evolution\lineage-evolution.md`

**问题 #1** (第 61 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxhnigvl1TempValidation.java:3: 错误: 找不到符号
        LineageContext ctx = LineageContext.current();
        ^
  符号:   类 LineageContext
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3


### `i18n\en\Flink\09-practices\09.04-security\security\evolution\tee-evolution.md`

**问题 #1** (第 65 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_a081n0sTempValidation.java:3: 错误: 找不到符号
        Enclave enclave = EnclaveLoader.load("enclave.so");
        ^
  符号:   类 Enclave
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3

**问题 #2** (第 74 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4f_hmfwkTempValidation.java:4: 错误: 找不到符号
EnclaveResult result = teeExecutor.execute(() -> {
^
  符号:   类 EnclaveResult
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4


### `i18n\en\Flink\09-practices\09.04-security\streaming-security-best-practices.md`

**问题 #4** (第 216 行, 语言: yaml)
- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 9, column 1:
    ssl.keystore.location=/etc/kafka ...
    ^ (line: 9)
- **错误行**: 9

**问题 #8** (第 334 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps21991juTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmps21991j
- **错误行**: 3


### `i18n\en\Flink\09-practices\09.04-security\trusted-execution-flink.md`

**问题 #13** (第 491 行, 语言: python)
- **错误**: SyntaxError: unexpected indent
- **错误行**: 4

**问题 #14** (第 512 行, 语言: python)
- **错误**: SyntaxError: unexpected indent
- **错误行**: 1


### `i18n\en\Flink\09-practices\09.05-edge\flink-edge-ai-optimization.md`

**问题 #8** (第 542 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2x5djfi2ModelInferenceWithBroadcast.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<ModelUpdate> modelUpdates = env
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2


### `i18n\en\Flink\10-internals\source-code-reading-guide.md`

**问题 #12** (第 399 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7sipjuboTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #13** (第 423 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp69uqxfumTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmp69
- **错误行**: 4

**问题 #14** (第 440 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvlrw7fl3TempValidation.java:4: 错误: 非法的表达式开始
public <R> SingleOutputStreamOperator<R> flatMap(
^
C:\Users\luyan\AppData\Local\Temp\tmpvlrw7fl3TempValidation.java:16
- **错误行**: 4

**问题 #15** (第 456 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5it436j4TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmp5i
- **错误行**: 4

**问题 #16** (第 483 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcvs0pulkTempValidation.java:4: 错误: 非法的表达式开始
public StreamGraph generate() {
^
C:\Users\luyan\AppData\Local\Temp\tmpcvs0pulkTempValidation.java:19: 错误: 需要 class、int
- **错误行**: 4

**问题 #17** (第 502 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpboe0g4rcTempValidation.java:4: 错误: 非法的表达式开始
public JobGraph createJobGraph(StreamGraph streamGraph) {
^
C:\Users\luyan\AppData\Local\Temp\tmpboe0g4rcTempValidation
- **错误行**: 4

**问题 #18** (第 523 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl1pyfq1dTempValidation.java:4: 错误: 非法的表达式开始
public static ExecutionGraph buildGraph(...)
^
C:\Users\luyan\AppData\Local\Temp\tmpl1pyfq1dTempValidation.java:4: 错误:
- **错误行**: 4

**问题 #27** (第 779 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz43x7r7qTempValidation.java:4: 错误: 需要';'
jobGraph.getJobID().toString().equals("your-job-id")
                                                    ^
1 个错误

- **错误行**: 4

**问题 #28** (第 786 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppf62lk39TempValidation.java:4: 错误: 不是语句
taskDeploymentDescriptor.getJobID().toString().equals("your-job-id") &&

- **错误行**: 4

**问题 #29** (第 796 行, 语言: yaml)
- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 5, column 1:
    logger.runtime.name = org.apache ...
    ^ (line: 5)
- **错误行**: 5


### `i18n\en\Flink\3.9-state-backends-deep-comparison.md`

**问题 #13** (第 383 行, 语言: yaml)
- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend.rocksdb.memory.man ...
    ^ (line: 2)
found duplicate key "state.backend.rocksdb.memory.managed" with value
- **错误行**: 2

**问题 #14** (第 404 行, 语言: yaml)
- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend.rocksdb.compaction ...
    ^ (line: 2)
found duplicate key "state.backend.rocksdb.compaction.style" with valu
- **错误行**: 2


### `i18n\en\Flink\data-types-complete-reference.md`

**问题 #6** (第 268 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzm_yqb65TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.DataTypes;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpzm_yqb65TempValidat
- **错误行**: 3


### `i18n\en\Flink\elasticsearch-connector-guide.md`

**问题 #4** (第 255 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa4v9noltTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.elasticsearch.sink.Elasticsearch7SinkBuilder;
^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #6** (第 332 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp66ag2pbmTempValidation.java:4: 错误: 找不到符号
ElasticsearchSink<Event> esSink = new Elasticsearch7SinkBuilder<Event>()
^
  符号:   类 ElasticsearchSink
  位置: 类 TempValidat
- **错误行**: 4


### `i18n\en\Flink\flink-nexmark-benchmark-guide.md`

**问题 #2** (第 241 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmproywqay5TempValidation.java:5: 错误: 找不到符号
Random random = new Random(SEED);
^
  符号:   类 Random
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmproywqay5T
- **错误行**: 5

**问题 #3** (第 249 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi1n96at8TempValidation.java:5: 错误: 找不到符号
long eventTime = baseTime + (offsetSec * 1000);
                             ^
  符号:   变量 offsetSec
  位置: 类 TempValidation
- **错误行**: 5

**问题 #10** (第 388 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptzam7q9uTempValidation.java:4: 错误: 找不到符号
tableEnv.getConfig().getConfiguration()
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #12** (第 412 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphik02p9oTempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #15** (第 466 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp28jj7penTempValidation.java:4: 错误: 需要';'
CREATE TABLE Person (
            ^
C:\Users\luyan\AppData\Local\Temp\tmp28jj7penTempValidation.java:5: 错误: 需要')'或','

- **错误行**: 4

**问题 #16** (第 502 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo_67sz1qTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `i18n\en\Flink\flink-state-backends-comparison.md`

**问题 #3** (第 227 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_kr59cckTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #4** (第 254 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpljrjgpgwTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #5** (第 303 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpile3t08nTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #9** (第 459 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoeadazjbTempValidation.java:4: 错误: 找不到符号
config.set(RocksDBOptions.BLOCK_CACHE_SIZE, MemorySize.ofMebiBytes(256));
           ^
  符号:   变量 RocksDBOptions
  位置: 类 T
- **错误行**: 4

**问题 #11** (第 476 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp46uxt5okTempValidation.java:3: 错误: 找不到符号
        config.set(CheckpointingOptions.INCREMENTAL_CHECKPOINTS, true);
                   ^
  符号:   变量 CheckpointingOptio
- **错误行**: 3

**问题 #13** (第 486 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpflfe86q9TempValidation.java:3: 错误: 找不到符号
        config.set(CheckpointingOptions.MAX_CONCURRENT_CHECKPOINTS, 1);
                   ^
  符号:   变量 CheckpointingOptio
- **错误行**: 3

**问题 #15** (第 499 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi5b88f85TempValidation.java:4: 错误: 找不到符号
config.set(CheckpointingOptions.LOCAL_RECOVERY, true);
           ^
  符号:   变量 CheckpointingOptions
  位置: 类 TempValidation
- **错误行**: 4


### `i18n\en\Flink\jdbc-connector-guide.md`

**问题 #4** (第 233 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpphcjbdekTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcConnectionOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmpphcjbdekTempValida
- **错误行**: 3

**问题 #6** (第 302 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpobrczsqaTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcInputFormat;
^
C:\Users\luyan\AppData\Local\Temp\tmpobrczsqaTempValidation.j
- **错误行**: 3


### `i18n\en\Flink\mongodb-connector-guide.md`

**问题 #4** (第 253 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp08ji9s4vTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.source.MongoSource;
^
C:\Users\luyan\AppData\Local\Temp\tmp08ji9s4vTempValida
- **错误行**: 3

**问题 #5** (第 289 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdp2n30kdTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.source.MongoSource;
^
C:\Users\luyan\AppData\Local\Temp\tmpdp2n30kdTempValida
- **错误行**: 3

**问题 #6** (第 322 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpes20vy8vTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.sink.MongoSink;
^
C:\Users\luyan\AppData\Local\Temp\tmpes20vy8vTempValidation
- **错误行**: 3


### `i18n\en\Flink\pulsar-functions-integration.md`

**问题 #8** (第 224 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvrj5yo93TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpvrj
- **错误行**: 3


### `i18n\en\Flink\risingwave-integration-guide.md`

**问题 #6** (第 133 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptdrg54hjTempValidation.java:4: 错误: 找不到符号
FlinkKafkaProducer<String> kafkaProducer = new FlinkKafkaProducer<>(
^
  符号:   类 FlinkKafkaProducer
  位置: 类 TempValidation
- **错误行**: 4

**问题 #9** (第 189 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0bfaw_pvTempValidation.java:4: 错误: 找不到符号
DebeziumSourceFunction<String> source = DebeziumSourceFunction.<String>builder()
^
  符号:   类 DebeziumSourceFunction
  位置:
- **错误行**: 4

**问题 #10** (第 200 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8nj3gv9fTempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.sqlQuery(
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp8nj3gv9fTe
- **错误行**: 4


### `i18n\en\Flink\state-backends-comparison.md`

**问题 #2** (第 103 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsjpxix98TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.runtime.state.hashmap.HashMapStateBackend;
^
C:\Users\luyan\AppData\Local\Temp\tmpsjpxix98TempV
- **错误行**: 3

**问题 #3** (第 136 行, 语言: yaml)
- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    state.backend: hashmap
    ^ (line: 4)
found duplicate key "state.backend" with value "rocksdb" (original value: "hashmap")

- **错误行**: 4

**问题 #4** (第 162 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwmqwxvkuTempValidation.java:4: 错误: 非法的表达式开始
public void monitorStateBackend(RuntimeContext ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpwmqwxvkuTempValidation.jav
- **错误行**: 4


### `i18n\en\Knowledge\01-concept-atlas\01.01-stream-processing-fundamentals.md`

**问题 #4** (第 607 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkowif2boTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpkow
- **错误行**: 3

**问题 #5** (第 627 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppfi9t66_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmppfi
- **错误行**: 3


### `i18n\en\Knowledge\01-concept-atlas\01.03-window-concepts.md`

**问题 #2** (第 302 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvffatqmjTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
        ^
C:\Users\luyan\Ap
- **错误行**: 3

**问题 #3** (第 324 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfgbhpo3wTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpfgb
- **错误行**: 3

**问题 #4** (第 338 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpml2trltzTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpml2trltzTempValidat
- **错误行**: 4

**问题 #6** (第 401 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqbcp_k2pTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqbc
- **错误行**: 3

**问题 #7** (第 421 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvxsnvionTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpvxsnvionTempValidat
- **错误行**: 4


### `i18n\en\Knowledge\01-concept-atlas\01.04-state-management-concepts.md`

**问题 #4** (第 388 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp215cwdn_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp215cw
- **错误行**: 3

**问题 #5** (第 407 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm87srimxTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4


### `i18n\en\Knowledge\01-concept-atlas\01.05-consistency-models.md`

**问题 #1** (第 236 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplrel6j69TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.CheckpointingMode;
^
C:\Users\luyan\AppData\Local\Temp\tmplrel6j69TempValidation.
- **错误行**: 4


### `i18n\en\Knowledge\01-concept-atlas\streaming-languages-landscape-2025.md`

**问题 #1** (第 346 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0a8ys8pqTempValidation.java:4: 错误: 找不到符号
ExecutorService executor = Executors.newFixedThreadPool(100);
^
  符号:   类 ExecutorService
  位置: 类 TempValidation
C:\Users\
- **错误行**: 4


### `i18n\en\Knowledge\02-design-patterns\pattern-realtime-feature-engineering.md`

**问题 #4** (第 353 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2zt3ja7_SessionAggregator.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Transaction> transactions = ...
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Loc
- **错误行**: 2


### `i18n\en\Knowledge\03-business-patterns\data-mesh-streaming-architecture-2026.md`

**问题 #5** (第 416 行, 语言: yaml)
- **错误**: while scanning a block scalar
  in "<unicode string>", line 15, column 19:
        completeness: > 99.9%
                      ^ (line: 15)
expected a comment or a line break, but found '9'
  in "<uni
- **错误行**: 15


### `i18n\en\Knowledge\03-business-patterns\netflix-streaming-pipeline.md`

**问题 #12** (第 366 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3w3vocm_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp3w3
- **错误行**: 3


### `i18n\en\Knowledge\03-business-patterns\source-code-reading-guide.md`

**问题 #12** (第 399 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc0x54jknTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #13** (第 423 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpliga2xwwTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpli
- **错误行**: 4

**问题 #14** (第 440 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv0r73o45TempValidation.java:4: 错误: 非法的表达式开始
public <R> SingleOutputStreamOperator<R> flatMap(
^
C:\Users\luyan\AppData\Local\Temp\tmpv0r73o45TempValidation.java:16
- **错误行**: 4

**问题 #15** (第 456 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcnyozd0dTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpcn
- **错误行**: 4

**问题 #16** (第 483 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2f4wmr7_TempValidation.java:4: 错误: 非法的表达式开始
public StreamGraph generate() {
^
C:\Users\luyan\AppData\Local\Temp\tmp2f4wmr7_TempValidation.java:19: 错误: 需要 class、int
- **错误行**: 4

**问题 #17** (第 502 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwy_xtub8TempValidation.java:4: 错误: 非法的表达式开始
public JobGraph createJobGraph(StreamGraph streamGraph) {
^
C:\Users\luyan\AppData\Local\Temp\tmpwy_xtub8TempValidation
- **错误行**: 4

**问题 #18** (第 523 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxcf7uu1dTempValidation.java:4: 错误: 非法的表达式开始
public static ExecutionGraph buildGraph(...)
^
C:\Users\luyan\AppData\Local\Temp\tmpxcf7uu1dTempValidation.java:4: 错误:
- **错误行**: 4

**问题 #27** (第 779 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx525e1peTempValidation.java:4: 错误: 需要';'
jobGraph.getJobID().toString().equals("your-job-id")
                                                    ^
1 个错误

- **错误行**: 4

**问题 #28** (第 786 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1mtu2iixTempValidation.java:4: 错误: 不是语句
taskDeploymentDescriptor.getJobID().toString().equals("your-job-id") &&

- **错误行**: 4

**问题 #29** (第 796 行, 语言: yaml)
- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 5, column 1:
    logger.runtime.name = org.apache ...
    ^ (line: 5)
- **错误行**: 5


### `i18n\en\Knowledge\04-technology-selection\stream-processing-framework-selection.md`

**问题 #5** (第 682 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfbyv4k3mTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpfbyv4k3
- **错误行**: 3


### `i18n\en\Knowledge\05-mapping-guides\migration-guides\05.1-spark-streaming-to-flink-migration.md`

**问题 #5** (第 173 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4i05bb5vTempValidation.java:5: 错误: 找不到符号
env.getConfig().setAutoWatermarkInterval(200);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 5

**问题 #9** (第 252 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6hha5xu6TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmp6h
- **错误行**: 3

**问题 #11** (第 295 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgor2flotCountFunction.java:34: 错误: 需要 class、interface、enum 或 record
keyedStream.process(new CountFunction());
^
1 个错误

- **错误行**: 34

**问题 #13** (第 347 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp660_076qTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp660
- **错误行**: 3

**问题 #15** (第 370 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0hytetf4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp0hytetf
- **错误行**: 3

**问题 #19** (第 469 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf_1jnohcTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpf_1
- **错误行**: 3

**问题 #20** (第 486 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg2s7mafkTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpg2s7m
- **错误行**: 3

**问题 #21** (第 501 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppue2ogllTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmppue2ogllTempValidat
- **错误行**: 4


### `i18n\en\Knowledge\05-mapping-guides\migration-guides\05.2-kafka-streams-to-flink-migration.md`

**问题 #5** (第 151 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp079lg6g0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp079lg6g0TempV
- **错误行**: 3

**问题 #6** (第 174 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmty7q5iyTempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #7** (第 187 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpky9hfvm5TempValidation.java:3: 错误: 找不到符号
        KafkaSource<MyEvent> source = KafkaSource.<MyEvent>builder()
        ^
  符号:   类 KafkaSource
  位置: 类 TempValidatio
- **错误行**: 3

**问题 #8** (第 241 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr3henby2TempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #9** (第 262 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo8_3wlo4TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpo8
- **错误行**: 4

**问题 #10** (第 315 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp04_jwwdfTempValidation.java:3: 错误: 找不到符号
        KTable<String, Long> wordCounts = source
        ^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #11** (第 326 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsorjz51jCountAggregate.java:6: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Tuple2<String, Long>> wordCounts = source
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 6

**问题 #12** (第 370 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxrp999lxTempValidation.java:3: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3

**问题 #13** (第 383 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcudrm33_TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpcudrm33_TempValidat
- **错误行**: 4

**问题 #21** (第 613 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv389bvj6TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpv389bvj6TempValidat
- **错误行**: 4


### `i18n\en\Knowledge\05-mapping-guides\migration-guides\05.3-storm-to-flink-migration.md`

**问题 #1** (第 91 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz5waoneiTempValidation.java:4: 错误: 找不到符号
Map<String, Object> state = new HashMap<>();
^
  符号:   类 Map
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpz
- **错误行**: 4

**问题 #2** (第 99 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6jjtrr8cTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp6jjtrr8cTem
- **错误行**: 3

**问题 #4** (第 138 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp54ypol00TempValidation.java:5: 错误: 找不到符号
    .fieldsGrouping("split", new Fields("word"));
                                 ^
  符号:   类 Fields
  位置: 类 TempValidati
- **错误行**: 5

**问题 #8** (第 215 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp14qfyvofTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.functions.AggregateFunction;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #9** (第 270 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxg0efqq6SentenceSpout.java:64: 错误: 未命名类 是预览功能，默认情况下禁用。
TopologyBuilder builder = new TopologyBuilder();
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\
- **错误行**: 64

**问题 #10** (第 346 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4e3j_4tlWordCount.java:37: 错误: 未命名类 是预览功能，默认情况下禁用。
public static void main(String[] args) throws Exception {
              ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错
- **错误行**: 37

**问题 #12** (第 442 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdbmlovr0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpdbm
- **错误行**: 3

**问题 #14** (第 488 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl526s9oxTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.functions.AggregateFunction;
^
C:\Users\luyan\AppData\Local\Temp\tmpl526s9oxTempVali
- **错误行**: 4

**问题 #23** (第 734 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1ytlu7dmTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1yt
- **错误行**: 3


### `i18n\en\Knowledge\05-mapping-guides\migration-guides\05.4-flink-1x-to-2x-migration.md`

**问题 #4** (第 151 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxji80u2rTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpxji80u2rTem
- **错误行**: 3

**问题 #5** (第 193 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxjwm5pksTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #6** (第 244 行, 语言: yaml)
- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend: rocksdb
    ^ (line: 2)
found duplicate key "state.backend" with value "rocksdb" (original value: "rocksdb")

- **错误行**: 2

**问题 #9** (第 357 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3ubq3nccTempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<String> consumer = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #10** (第 371 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbjtft0c0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpbjt
- **错误行**: 3

**问题 #11** (第 395 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi9jtu317TempValidation.java:4: 错误: 找不到符号
FlinkKafkaProducer<String> producer = new FlinkKafkaProducer<>(
^
  符号:   类 FlinkKafkaProducer
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #12** (第 409 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1unud_dnTempValidation.java:4: 错误: 找不到符号
KafkaSink<String> sink = KafkaSink.<String>builder()
^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #13** (第 427 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwua9ztqmTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwua9ztqmTemp
- **错误行**: 3

**问题 #14** (第 448 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp29jdhctxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp29j
- **错误行**: 3

**问题 #15** (第 470 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8hgihmedTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8hgih
- **错误行**: 3

**问题 #16** (第 488 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprcutxxxkTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmprcutx
- **错误行**: 3


### `i18n\en\Knowledge\05-mapping-guides\migration-guides\05.5-batch-to-streaming-migration.md`

**问题 #2** (第 127 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_hw6192xTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.functions.AggregateFunction;
^
C:\Users\luyan\AppData\Local\Temp\tmp_hw6192xTempVali
- **错误行**: 4

**问题 #5** (第 192 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpibhpguwtTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #6** (第 207 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw2sz7cxwTempValidation.java:4: 错误: 找不到符号
List<Data> allData = readAllData();
^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpw2sz7cxwT
- **错误行**: 4

**问题 #8** (第 241 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpekbyghxiTempValidation.java:4: 错误: 找不到符号
for (Record record : batchData) {
                     ^
  符号:   变量 batchData
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #9** (第 250 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw4iuqx0yTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpw4iuq
- **错误行**: 3

**问题 #11** (第 324 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnemen1xaTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpnemen1xaTempValidat
- **错误行**: 4

**问题 #13** (第 366 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwuio4lerTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpwuio4lerTempValidat
- **错误行**: 4

**问题 #15** (第 414 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpurwo0venTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpurwo0venTempValidat
- **错误行**: 4

**问题 #16** (第 439 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy51n50f5TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpy51n50f5TempValidat
- **错误行**: 4

**问题 #18** (第 476 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmposec3vjrDeduplicateFunction.java:39: 错误: 需要 class、interface、enum 或 record
stream.keyBy(e -> e.getUserId() + "_" + e.getEventType())
^
1 个错误

- **错误行**: 39

**问题 #20** (第 535 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqijj9uxgTopNFunction.java:37: 错误: 需要 class、interface、enum 或 record
stream.keyBy(ProductSale::getCategory)
^
1 个错误

- **错误行**: 37

**问题 #25** (第 678 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppqxn_97kTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmppqxn_
- **错误行**: 3

**问题 #26** (第 696 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5u5p0xsxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5u5p0
- **错误行**: 3

**问题 #27** (第 721 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgajfumieTempValidation.java:5: 错误: 找不到符号
    stream,
    ^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpgajfumieTempValidation.jav
- **错误行**: 5


### `i18n\en\Knowledge\06-frontier\audio-stream-processing.md`

**问题 #2** (第 103 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp47k8md3tTempValidation.java:3: 错误: 找不到符号
        DataStream<AudioFrame> audioStream = env
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppD
- **错误行**: 3


### `i18n\en\Knowledge\06-frontier\multimodal-stream-processing.md`

**问题 #2** (第 126 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmz7qitruTempValidation.java:3: 错误: 找不到符号
        DataStream<TextEvent> textStream = env
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3


### `i18n\en\Knowledge\06-frontier\real-time-rag-architecture.md`

**问题 #4** (第 307 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkddozc9aEmbeddingAsyncFn.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.async不存在
import org.apache.flink.streaming.api.functions.async.AsyncFunction;

- **错误行**: 1

**问题 #5** (第 323 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo55l_6uvVectorBulkSink.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.sink不存在
import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;

- **错误行**: 1


### `i18n\en\Knowledge\06-frontier\realtime-data-mesh-practice.md`

**问题 #9** (第 354 行, 语言: sql)
- **错误**: 可能的语法问题: -- RESULT: F → E → B → [A, C]...


### `i18n\en\Knowledge\06-frontier\realtime-data-quality-validation.md`

**问题 #5** (第 271 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4k2srf6sTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp4k2srf6sTempValidat
- **错误行**: 4


### `i18n\en\Knowledge\06-frontier\realtime-ml-inference\06.04.01-ml-model-serving.md`

**问题 #3** (第 239 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvvlxqez9TritonAsyncInference.java:42: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Prediction> predictions = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以启用 未命名
- **错误行**: 42

**问题 #4** (第 293 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe2e53scjTempValidation.java:4: 错误: 找不到符号
MapStateDescriptor<String, String> modelVersionState =
^
  符号:   类 MapStateDescriptor
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 4


### `i18n\en\Knowledge\06-frontier\streaming-materialized-view-architecture.md`

**问题 #7** (第 376 行, 语言: sql)
- **错误**: 可能的语法问题: -- AUTOMATIC INCREMENTAL UPDATE
-- WHEN SALES TABL...


### `i18n\en\Knowledge\06-frontier\streaming-slo-definition.md`

**问题 #4** (第 305 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2j35n30wTempValidation.java:4: 错误: 找不到符号
Counter slo_violations_total = Counter.build()
^
  符号:   类 Counter
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4


### `i18n\en\Knowledge\06-frontier\video-stream-analytics.md`

**问题 #2** (第 104 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl9c15bm0TempValidation.java:3: 错误: 找不到符号
        DataStream<VideoFrame> videoStream = env
        ^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppD
- **错误行**: 3

**问题 #4** (第 157 行, 语言: python)
- **错误**: SyntaxError: invalid syntax
- **错误行**: 5


### `i18n\en\Knowledge\07-best-practices\07.02-performance-tuning-patterns.md`

**问题 #9** (第 359 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr913x9r1TempValidation.java:10: 错误: 需要';'
val descriptor = new ValueStateDescriptor[Array[Byte]](
                                                      ^
C:\Users\
- **错误行**: 10

**问题 #13** (第 473 行, 语言: yaml)
- **错误**: while constructing a mapping
  in "<unicode string>", line 5, column 1:
    taskmanager.memory.process.size: 4gb
    ^ (line: 5)
found duplicate key "taskmanager.memory.process.size" with value "32gb"
- **错误行**: 5


### `i18n\en\Knowledge\07-best-practices\07.05-security-hardening-guide.md`

**问题 #3** (第 220 行, 语言: yaml)
- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    security.kerberos.login.keytab:  ...
    ^ (line: 4)
found duplicate key "security.kerberos.login.contexts" with value "Cli
- **错误行**: 4

**问题 #13** (第 539 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2kddhjtjTempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `i18n\en\Knowledge\07-best-practices\flink-production-checklist.md`

**问题 #3** (第 230 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxpp9g19rTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000); // 1 minute interval
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #4** (第 256 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnuth9xesTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnut
- **错误行**: 3

**问题 #7** (第 381 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplqni373mTempValidation.java:4: 错误: 非法的表达式开始
private static final Logger LOG = LoggerFactory.getLogger(MyFunction.class);
^
C:\Users\luyan\AppData\Local\Temp\tmplqn
- **错误行**: 4

**问题 #11** (第 569 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuepf0r58TempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(10000);  // 10s interval
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #12** (第 580 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa9e5inpnTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(300000);  // 5min interval
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `i18n\en\Knowledge\08-standards\streaming-data-governance.md`

**问题 #6** (第 211 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpso8y_5d1TempValidation.java:5: 错误: 不是语句
  "type": "record",
  ^
C:\Users\luyan\AppData\Local\Temp\tmpso8y_5d1TempValidation.java:5: 错误: 需要';'
  "type": "record",

- **错误行**: 5

**问题 #9** (第 275 行, 语言: sql)
- **错误**: 可能的语法问题: -- LINEAGE OUTPUT:
-- FINAL_AMOUNT → DEPENDS ON: [...

**问题 #11** (第 328 行, 语言: sql)
- **错误**: 可能的语法问题: -- GRANT TABLE-LEVEL PERMISSIONS
GRANT SELECT ON T...

**问题 #12** (第 346 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy5u9sce7MaskPII.java:18: 错误: 需要 class、interface、enum 或 record
SELECT
^
C:\Users\luyan\AppData\Local\Temp\tmpy5u9sce7MaskPII.java:20: 错误: 未结束的字符文字
    MaskPII(email
- **错误行**: 18


### `i18n\en\Knowledge\10-case-studies\CODE-RUNNABILITY-NOTES.md`

**问题 #1** (第 35 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmv6jz7swTempValidation.java:5: 错误: 找不到符号
env.setParallelism(100);  // Originally 100, adjust based on TaskManager count
^
  符号:   变量 env
  位置: 类 TempValidation
C:\
- **错误行**: 5

**问题 #2** (第 66 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfeewa9h_TempValidation.java:5: 错误: 找不到符号
options.setConnectionTimeout(10);  // Increase when network is unstable
^
  符号:   变量 options
  位置: 类 TempValidation
C:\Use
- **错误行**: 5

**问题 #3** (第 94 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj0w080ylTempValidation.java:5: 错误: 非法的表达式开始
kieFileSystem.write("src/main/resources/rules/fraud-rules.drl", ...)

- **错误行**: 5


### `i18n\en\Knowledge\10-case-studies\iot\10.3.1-smart-manufacturing.md`

**问题 #4** (第 366 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw6lac54xTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpw6lac54xTempValidatio
- **错误行**: 4


### `i18n\en\Knowledge\98-exercises\exercise-02-flink-basics.md`

**问题 #2** (第 101 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpznfiefxcTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpznf
- **错误行**: 3

**问题 #3** (第 177 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj73678t9WordCount.java:206: 错误: 需要 class、interface、enum 或 record
*/
^
1 个错误

- **错误行**: 206

**问题 #5** (第 447 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpba78h3qkTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpba78h
- **错误行**: 3


### `i18n\en\Knowledge\98-exercises\exercise-03-checkpoint-analysis.md`

**问题 #1** (第 67 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2nmyvb68TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2nmyvb6
- **错误行**: 3

**问题 #5** (第 389 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprubuhctgexample.java:30: 错误: 需要 class、interface、enum 或 record
env.getCheckpointConfig().enableUnalignedCheckpoints();
^
C:\Users\luyan\AppData\Local\Temp\tmprubuhc
- **错误行**: 30


### `i18n\en\Knowledge\98-exercises\quick-ref-security-compliance.md`

**问题 #8** (第 305 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7m65mqx6TempValidation.java:18: 错误: 需要';'
""")
    ^
C:\Users\luyan\AppData\Local\Temp\tmp7m65mqx6TempValidation.java:29: 错误: 需要';'
""")
    ^
2 个错误

- **错误行**: 18


### `i18n\en\Knowledge\98-exercises\quick-ref-temporal-flink.md`

**问题 #8** (第 387 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplrqbah3tTemporalStateLookup.java:3: 错误: 未命名类 是预览功能，默认情况下禁用。
public WorkflowState getWorkflowState() {
       ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 3


### `i18n\en\Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.04-flink-sql-table-api.md`

**问题 #6** (第 145 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpslxgi4x1TempValidation.java:4: 错误: 找不到符号
env.setRuntimeMode(RuntimeExecutionMode.STREAMING);
                   ^
  符号:   变量 RuntimeExecutionMode
  位置: 类 TempValid
- **错误行**: 4

**问题 #8** (第 289 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprkdtphz8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.functions.AggregateFunction;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #9** (第 313 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpymod1copTempValidation.java:4: 错误: 非法的表达式开始
Filter -> Scan  =>  Scan(with Filter)
                 ^
C:\Users\luyan\AppData\Local\Temp\tmpymod1copTempValidation.ja
- **错误行**: 4

**问题 #10** (第 326 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6hq_gvwiTempValidation.java:4: 错误: 需要';'
A JOIN B JOIN C  =>  Select lowest-cost join order
      ^
C:\Users\luyan\AppData\Local\Temp\tmp6hq_gvwiTempValidation.jav
- **错误行**: 4

**问题 #11** (第 353 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7bij41qyMLPredictUDF.java:11: 错误: 需要 class、interface、enum 或 record
AsyncFunction calls REST API, latency 10-100ms
^
1 个错误

- **错误行**: 11

**问题 #13** (第 434 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvhsn1ntuTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.Table;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpvhsn1ntuTempValidation.
- **错误行**: 3

**问题 #15** (第 520 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa2otvdroTempValidation.java:4: 错误: 找不到符号
TableConfig config = tableEnv.getConfig();
^
  符号:   类 TableConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #17** (第 604 行, 语言: sql)
- **错误**: 可能的语法问题: -- 4. MODEL PERFORMANCE MONITORING
DESCRIBE MODEL ...; 可能的语法问题: -- DISPLAYS: AVG_INFERENCE_LATENCY, THROUGHPUT, ER...

**问题 #18** (第 680 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpymxf6r8zTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpymx
- **错误行**: 3

**问题 #19** (第 722 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsmavhkpcTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `i18n\en\Knowledge\Flink-Scala-Rust-Comprehensive\04-rust-engines\04.03-materialize-analysis.md`

**问题 #7** (第 287 行, 语言: sql)
- **错误**: 可能的语法问题: -- STRONG CONSISTENCY GUARANTEE: BALANCE IS ALWAYS...

**问题 #11** (第 431 行, 语言: sql)
- **错误**: 可能的语法问题: -- SUPPORTS RECURSIVE CTE
WITH RECURSIVE CHAIN AS ...

**问题 #12** (第 453 行, 语言: sql)
- **错误**: 可能的语法问题: -- RECURSIVE CTE NOT SUPPORTED, REQUIRES EXTERNAL ...

**问题 #14** (第 517 行, 语言: sql)
- **错误**: 可能的语法问题: -- SHOW MATERIALIZED VIEWS
SHOW MATERIALIZED VIEWS...; 可能的语法问题: -- SHOW SOURCES
SHOW SOURCES;...


### `i18n\en\Knowledge\case-studies\ecommerce-realtime-recommendation-v2.md`

**问题 #2** (第 260 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkytg_68yTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpkytg_68yTempValidat
- **错误行**: 4

**问题 #3** (第 324 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt23hce2_AsyncModelInference.java:47: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Prediction> predictions = featureStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 47


### `i18n\en\Knowledge\case-studies\ecommerce\realtime-recommendation-case.md`

**问题 #2** (第 260 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpotghqnxaTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpotghqnxaTempValidat
- **错误行**: 4

**问题 #3** (第 324 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1yx0ljpkAsyncModelInference.java:47: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Prediction> predictions = featureStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 47


### `i18n\en\Knowledge\case-studies\finance\realtime-anti-fraud-system-case.md`

**问题 #2** (第 205 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpios_ccveTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpios_ccveTempValidat
- **错误行**: 4

**问题 #3** (第 272 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpog2r0v_nTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpog2r0v_nTempValidat
- **错误行**: 4


### `i18n\en\Knowledge\case-studies\gaming\realtime-game-analytics-case.md`

**问题 #2** (第 189 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8x51qy45TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp8x51qy45TempValidat
- **错误行**: 4

**问题 #4** (第 340 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpegs96gweTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpegs96gweTempValidatio
- **错误行**: 4


### `i18n\en\Knowledge\case-studies\iot-smart-grid-case-study.md`

**问题 #2** (第 275 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdoeyn7htTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpdoeyn7htTempValidat
- **错误行**: 4

**问题 #3** (第 359 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplylmd5y4TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmplylmd5y4TempValidat
- **错误行**: 4


### `i18n\en\Knowledge\cep-complete-tutorial.md`

**问题 #4** (第 236 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo0evil0cTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.Pattern;
^
C:\Users\luyan\AppData\Local\Temp\tmpo0evil0cTempValidation.java:3: 错误: 不是语句
imp
- **错误行**: 3

**问题 #5** (第 292 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp10y0vrh3TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmp10y0vrh3TempValidatio
- **错误行**: 4

**问题 #6** (第 337 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx8k8i3fqTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpx8k8i3fqTempValidatio
- **错误行**: 4


### `i18n\en\Knowledge\kafka-streams-migration.md`

**问题 #3** (第 66 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpep02xpypTempValidation.java:3: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3

**问题 #4** (第 79 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps31zsuugTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmps31zsuugTempValidat
- **错误行**: 4

**问题 #5** (第 106 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1xrj8yoaTempValidation.java:3: 错误: 找不到符号
        KTable<Windowed<String>, Long> counts = orders
        ^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3


### `i18n\en\Struct\02-properties\02.02-consistency-hierarchy.md`

**问题 #1** (第 663 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8zffon4eTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8zf
- **错误行**: 3

**问题 #3** (第 737 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyvvp2hmbHttpSink.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.sink不存在
import org.apache.flink.streaming.api.functions.sink.SinkFunction;

- **错误行**: 1

**问题 #4** (第 761 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgk6gxydwEagerKafkaSource.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.source不存在
import org.apache.flink.streaming.api.functions.source.SourceFunction;

- **错误行**: 1


### `i18n\en\Struct\03-relationships\03.05-cross-model-mappings.md`

**问题 #6** (第 564 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbcq_moziTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpbcq
- **错误行**: 3


### `i18n\en\Struct\07-tools\model-checking-guided-testing.md`

**问题 #4** (第 220 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjo3c0un_TempValidation.java:4: 错误: 需要';'
public void testCheckpointCompletionRace() {
                                        ^
1 个错误

- **错误行**: 4


### `i18n\en\Struct\Proof-Chains-Flink-Implementation.md`

**问题 #24** (第 513 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi29v2gr7TempValidation.java:4: 错误: 非法的表达式开始
public void triggerCheckpoint(long timestamp) {
^
C:\Users\luyan\AppData\Local\Temp\tmpi29v2gr7TempValidation.java:15:
- **错误行**: 4

**问题 #25** (第 528 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoj_7xq41TempValidation.java:4: 错误: 非法的表达式开始
public final void snapshotState(StateSnapshotContext context) {
^
C:\Users\luyan\AppData\Local\Temp\tmpoj_7xq41TempVali
- **错误行**: 4

**问题 #26** (第 542 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3x0mi551TempValidation.java:4: 错误: 非法的表达式开始
private void processElement(StreamRecord<IN> element) {
^
C:\Users\luyan\AppData\Local\Temp\tmp3x0mi551TempValidation.j
- **错误行**: 4

**问题 #27** (第 559 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl0eg_w8wTempValidation.java:4: 错误: 非法的表达式开始
public void emitCompletedElement() {
^
C:\Users\luyan\AppData\Local\Temp\tmpl0eg_w8wTempValidation.java:13: 错误: 需要 clas
- **错误行**: 4


### `phase2-case-studies\aviation\11.32.1-baggage.md`

**问题 #8** (第 407 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph0xhlj_sTempValidation.java:3: 错误: 找不到符号
Pattern<BaggageEvent, ?> missedLoadingPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #9** (第 442 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp18uazzfwTempValidation.java:3: 错误: 找不到符号
Pattern<BaggageEvent, ?> misroutedPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 3


### `phase2-case-studies\construction\11.31.1-safety.md`

**问题 #7** (第 383 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvqq8h349TempValidation.java:3: 错误: 找不到符号
Pattern<ViolationEvent, ?> violationPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 3


### `phase2-case-studies\ecommerce\11.11.1-realtime-recommendation.md`

**问题 #2** (第 109 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgrulgq40UserInterestAggregateFunction.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<UserAction> actionStream = env
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 1


### `phase2-case-studies\energy\11.15.1-smart-grid.md`

**问题 #2** (第 111 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpze3x172nFaultDetectionFunction.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<PMUData> pmuStream = env
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 1


### `phase2-case-studies\energy\11.15.2-smart-grid-iot.md`

**问题 #18** (第 1307 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6gvtbkuhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp6gvtbku
- **错误行**: 3


### `phase2-case-studies\finance\11.13.1-risk-control.md`

**问题 #2** (第 112 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbzucy6b2FraudClusterDetectionFunction.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<ApplicationEvent> appStream = env
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 1

**问题 #4** (第 157 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfx1alf_kTempValidation.java:3: 错误: 找不到符号
Pattern<Transaction, ?> layeringPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 3


### `phase2-case-studies\finance\11.13.2-anti-fraud-system.md`

**问题 #5** (第 268 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyo9ln1brTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpyo9ln1brTempValidatio
- **错误行**: 4


### `phase2-case-studies\food\11.28.1-cold-chain.md`

**问题 #7** (第 359 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplho9dsfyTempValidation.java:3: 错误: 找不到符号
Pattern<SensorEvent, ?> doorOpenColdChainBreakPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 3


### `phase2-case-studies\gaming\11.12.1-player-behavior.md`

**问题 #2** (第 113 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprtz12qkeCheatDetectionFunction.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<PlayerAction> actionStream = env
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 1

**问题 #4** (第 190 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfw48comvTempValidation.java:3: 错误: 找不到符号
Pattern<PaymentEvent, ?> suspiciousPaymentPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppD
- **错误行**: 3


### `phase2-case-studies\healthcare\11.16.1-remote-patient.md`

**问题 #2** (第 106 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9jo8q7liVitalAnomalyFunction.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<VitalSign> vitalStream = env
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 1


### `phase2-case-studies\hospitality\11.38.1-hotel-management.md`

**问题 #4** (第 460 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfrdp9hlsTempValidation.java:86: 错误: 找不到符号
tableEnv.executeSql(pricingSql);
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
1 个错误

- **错误行**: 86


### `phase2-case-studies\logistics\11.19.1-fleet-management.md`

**问题 #2** (第 108 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj8risyvkDrivingBehaviorFunction.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<DrivingEvent> eventStream = env
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 1


### `phase2-case-studies\mining\11.27.1-mining-safety.md`

**问题 #6** (第 356 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1yvxdfwyTempValidation.java:3: 错误: 找不到符号
Pattern<SensorReading, ?> roofPressurePattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3


### `phase2-case-studies\pharma\11.30.1-pharma-tracking.md`

**问题 #6** (第 358 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgg3rpq3aTempValidation.java:3: 错误: 找不到符号
Pattern<SensorEvent, ?> coldChainBreakPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3


### `phase2-case-studies\public-safety\11.36.1-emergency-response.md`

**问题 #3** (第 299 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1utnh3djTempValidation.java:3: 错误: 找不到符号
Pattern<SensorReading, ?> floodRiskPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 3


### `phase2-case-studies\social-media\11.5.1-content-recommendation.md`

**问题 #8** (第 542 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeggbyl64InterestSequenceFunction.java:5: 错误: 找不到符号
class InterestSequenceFunction extends KeyedProcessFunction<String, UserAction, UserInterestSeq> {

- **错误行**: 5

**问题 #10** (第 860 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvo466y3uContentSafetyRules.java:49: 错误: 需要 class、interface、enum 或 record
CEP.pattern(contentStream, ContentSafetyRules.spamPattern)
^
C:\Users\luyan\AppData\Local\
- **错误行**: 49


### `phase2-case-studies\sports\11.24.1-sports-analytics.md`

**问题 #7** (第 397 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm2y5bs2nTempValidation.java:3: 错误: 找不到符号
Pattern<PlayerBiometricEvent, ?> fatigueRiskPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3


### `phase2-case-studies\supply-chain\11.4.1-supply-chain-inventory.md`

**问题 #8** (第 463 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvwoj80dxInventoryAggregationFunction.java:6: 错误: 找不到符号
    extends KeyedProcessFunction<String, InventoryChange, SkuInventory> {
            ^
  符号: 类 KeyedProcess
- **错误行**: 6

**问题 #12** (第 900 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqf5auivoTempValidation.java:7: 错误: 找不到符号
Pattern<SalesEvent, ?> salesAnomalyPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 7


### `phase2-case-studies\tourism\11.33.1-tourism-analytics.md`

**问题 #3** (第 274 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmd52mkkeTempValidation.java:3: 错误: 找不到符号
Pattern<TouristEvent, ?> suddenSurgePattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 3


### `phase2-case-studies\water\11.34.1-water-quality.md`

**问题 #6** (第 377 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdvwigmuhTempValidation.java:3: 错误: 找不到符号
Pattern<QualityControlledWaterReading, ?> pollutionSpreadPattern = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\U
- **错误行**: 3


### `reconstruction\phase3-visualization\04-comparison-matrices.md`

**问题 #5** (第 198 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5198ssrsTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5198ssr
- **错误行**: 3

**问题 #6** (第 210 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpptq2j5rtTempValidation.java:3: 错误: 找不到符号
        props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG,
                  ^
  符号:   变量 StreamsConfig
  位置: 类 TempVali
- **错误行**: 3


### `release\v3.0.0\docs\100-PERCENT-COMPLETION-MASTER-PLAN.md`

**问题 #2** (第 75 行, 语言: python)
- **错误**: SyntaxError: invalid character '，' (U+FF0C)
- **错误行**: 4


### `release\v3.0.0\docs\BEST-PRACTICES-COMPLETE.md`

**问题 #2** (第 29 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpef4cxv5gTempValidation.java:7: 错误: 非法的表达式开始
stream.map(...).startNewChain().filter(...);
           ^
C:\Users\luyan\AppData\Local\Temp\tmpef4cxv5gTempValidation.j
- **错误行**: 7

**问题 #3** (第 45 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps655a0h0TempValidation.java:4: 错误: 找不到符号
env.getConfig().setAutoWatermarkInterval(200);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4


### `release\v3.0.0\docs\CASE-STUDIES.md`

**问题 #3** (第 263 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl8tul9a7TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpl8tul9a7TempValidat
- **错误行**: 4

**问题 #7** (第 492 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyros6y3_TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.typeinfo.Types;
^
C:\Users\luyan\AppData\Local\Temp\tmpyros6y3_TempValidation.java:4
- **错误行**: 4

**问题 #9** (第 610 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmdq7r9_tTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpmdq
- **错误行**: 3

**问题 #12** (第 731 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9qow7if9TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp9qow7if9TempValidat
- **错误行**: 4

**问题 #13** (第 805 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp4jxssa7TempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #14** (第 815 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcglieqczTempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend rocksDb = new RocksDBStateBackend("hdfs://checkpoints");
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempV
- **错误行**: 4

**问题 #16** (第 900 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp20h64oarThresholdMonitorFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<SensorData> processed = env
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\
- **错误行**: 2

**问题 #22** (第 1151 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppk2xlbnbAntiCheatProcessFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<PlayerAction> actionStream = env
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\App
- **错误行**: 2

**问题 #28** (第 1442 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfihooeq3TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpfih
- **错误行**: 3


### `release\v3.0.0\docs\CONTRIBUTING-EN.md`

**问题 #23** (第 912 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbgb0r28tTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3


### `release\v3.0.0\docs\CONTRIBUTING.md`

**问题 #23** (第 886 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4zrhr2g2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3


### `release\v3.0.0\docs\DEPLOYMENT-ARCHITECTURES.md`

**问题 #5** (第 218 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp45errimgTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmp45
- **错误行**: 4


### `release\v3.0.0\docs\FAQ.md`

**问题 #7** (第 435 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphss2q3kkTempValidation.java:4: 错误: 找不到符号
AIAgentConfig config = AIAgentConfig.builder()
^
  符号:   类 AIAgentConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #9** (第 501 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_wu7dol1TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #11** (第 557 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7r3rbt82TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #13** (第 626 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7piflix0TempValidation.java:4: 错误: 找不到符号
SmartCheckpointMetrics metrics = checkpointConfig.getSmartMetrics();
^
  符号:   类 SmartCheckpointMetrics
  位置: 类 TempValida
- **错误行**: 4

**问题 #16** (第 771 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpki0404viTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #17** (第 825 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_o8jg_wyGPUDetectionFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
StreamExecutionEnvironment env =
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 2

**问题 #24** (第 1052 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxgntstu8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpxgn
- **错误行**: 3

**问题 #25** (第 1088 行, 语言: sql)
- **错误**: 可能的语法问题: -- 查看已注册的 WASM UDF
SHOW FUNCTIONS WHERE TYPE = 'WA...; 可能的语法问题: -- 查看 UDF 详情
DESCRIBE FUNCTION STRING_LEN;...

**问题 #31** (第 1272 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj2fxrvzuTempValidation.java:4: 错误: 找不到符号
env.setStateBackend(new RocksDBStateBackend("hdfs://checkpoints", true));
                        ^
  符号:   类 RocksDBState
- **错误行**: 4

**问题 #33** (第 1325 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4tsvc_bxTempValidation.java:4: 错误: 找不到符号
GPUResource resource = new GPUResource(1, 16);
^
  符号:   类 GPUResource
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 4

**问题 #34** (第 1355 行, 语言: sql)
- **错误**: 可能的语法问题: -- 2.4: 流批一体基础
SET EXECUTION.MODE = 'STREAMING';...; 可能的语法问题: -- 2.5: 新增自适应模式
SET EXECUTION.MODE = 'ADAPTIVE';  ...

**问题 #37** (第 1459 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphe98juuwTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmphe9
- **错误行**: 3

**问题 #42** (第 1634 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfgxkb3ywTempValidation.java:5: 错误: 找不到符号
env.enableCheckpointing(5000);  // 每5秒，无论负载
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpf
- **错误行**: 5

**问题 #45** (第 1738 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0eg4c6tiTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #49** (第 1931 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3u543d_vTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp3u5
- **错误行**: 3


### `release\v3.0.0\docs\FLINK-IOT-GAP-ANALYSIS.md`

**问题 #1** (第 44 行, 语言: sql)
- **错误**: 可能的语法问题: -- 设备时间作为事件时间，而非KAFKA摄入时间
WATERMARK FOR DEVICE_TIM...

**问题 #7** (第 198 行, 语言: sql)
- **错误**: 可能的语法问题: WATERMARK FOR DEVICE_TIME AS DEVICE_TIME - INTERVA...


### `release\v3.0.0\docs\Flink\00-FLINK-TECH-STACK-DEPENDENCY.md`

**问题 #8** (第 365 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmg9r4rz8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #9** (第 390 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxp9gtdauTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpxp9gtdauTemp
- **错误行**: 3

**问题 #11** (第 427 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpolqymdi4TempValidation.java:7: 错误: 找不到符号
FlinkKafkaConsumer<Event> source = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\User
- **错误行**: 7


### `release\v3.0.0\docs\Flink\00-meta\00-QUICK-START.md`

**问题 #10** (第 327 行, 语言: sql)
- **错误**: 可能的语法问题: -- 步骤 1：注册 MCP 工具
-- 注: 以下为未来可能的语法（概念设计），尚未正式实现
<!...; 可能的语法问题: -- 步骤 2：创建 AI AGENT（未来可能的语法，概念设计阶段）
<!-- 以下语法为概念设计...

**问题 #11** (第 378 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4f0dfsbqTempValidation.java:4: 错误: 找不到符号
Agent agent = Agent.builder()
^
  符号:   类 Agent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp4f0dfsbqTempVa
- **错误行**: 4

**问题 #17** (第 570 行, 语言: sql)
- **错误**: 可能的语法问题: USE CATALOG PAIMON_CATALOG;...

**问题 #18** (第 615 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwta3eq2dTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #19** (第 638 行, 语言: sql)
- **错误**: 可能的语法问题: -- 配置自适应执行
SET EXECUTION.RUNTIME-MODE = ADAPTIVE;...

**问题 #22** (第 727 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgmebu1huTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpgme
- **错误行**: 3

**问题 #25** (第 811 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgwaxajr2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpgwaxajr2Temp
- **错误行**: 3


### `release\v3.0.0\docs\Flink\01-concepts\datastream-v2-semantics.md`

**问题 #12** (第 336 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5_ys8awvBadV1Function.java:3: 错误: 程序包org.apache.flink.api.common.state不存在
import org.apache.flink.api.common.state.ValueState;

- **错误行**: 3

**问题 #16** (第 455 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmkhhoqlyAsyncAggregator.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
KafkaSource<Event> source = KafkaSource.<Event>builder()
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan
- **错误行**: 2

**问题 #17** (第 495 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaauoayb8DeduplicateFunction.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
RecordAttributes attrs = RecordAttributes.builder()
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 1


### `release\v3.0.0\docs\Flink\01-concepts\disaggregated-state-analysis.md`

**问题 #3** (第 365 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoanx6oajTempValidation.java:3: 错误: 找不到符号
        DisaggregatedStateBackend stateBackend = new DisaggregatedStateBackend(
        ^
  符号:   类 DisaggregatedStateBack
- **错误行**: 3

**问题 #4** (第 394 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplmjzhx1hTempValidation.java:10: 错误: 需要';'
    .build()
            ^
1 个错误

- **错误行**: 10


### `release\v3.0.0\docs\Flink\01-concepts\flink-1.x-vs-2.0-comparison.md`

**问题 #7** (第 253 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmxqdpv95TempValidation.java:4: 错误: 找不到符号
CountState current = state.value();  // 阻塞调用
^
  符号:   类 CountState
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #8** (第 264 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfj2kpipeTempValidation.java:4: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpfj2kpipeTe
- **错误行**: 4

**问题 #13** (第 374 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_teclijyTempValidation.java:3: 错误: 非法的表达式开始
public void processElement(Event event, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmp_teclijyTempValidation.ja
- **错误行**: 3

**问题 #14** (第 385 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_dsab3dhTempValidation.java:3: 错误: 非法的表达式开始
public void processElement(Event event, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmp_dsab3dhTempValidation.ja
- **错误行**: 3


### `release\v3.0.0\docs\Flink\01-concepts\flink-architecture-evolution-1x-to-2x.md`

**问题 #1** (第 250 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmtewvgj9TempValidation.java:4: 错误: 找不到符号
   state.getAsync(key)
                  ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpmtew
- **错误行**: 4


### `release\v3.0.0\docs\Flink\02-core\adaptive-execution-engine-v2.md`

**问题 #11** (第 673 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpocwgmpnpSkewResistantAggregate.java:41: 错误: 需要 class、interface、enum 或 record
dataStream
^
1 个错误

- **错误行**: 41

**问题 #19** (第 1137 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq51gq_u0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #20** (第 1183 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_du5zv9lTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4


### `release\v3.0.0\docs\Flink\02-core\async-execution-model.md`

**问题 #7** (第 435 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzrgr2xtrOrderedCallback.java:8: 错误: 未命名类 是预览功能，默认情况下禁用。
PriorityQueue<OrderedCallback> callbackQueue =
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 8

**问题 #9** (第 487 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpno7qfptoTempValidation.java:4: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpno7qfptoTe
- **错误行**: 4

**问题 #10** (第 505 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvnu_1b5jTempValidation.java:4: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpvnu_1b5jTe
- **错误行**: 4

**问题 #15** (第 729 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuy3fmb1rTempValidation.java:3: 错误: 非法的表达式开始
public void processElement(Event event, Context ctx, ResultFuture<Result> resultFuture) {
^
C:\Users\luyan\AppData\Loca
- **错误行**: 3

**问题 #16** (第 768 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4h952cu9TempValidation.java:3: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp4h952cu9Te
- **错误行**: 3

**问题 #17** (第 782 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfcpt8hmtTempValidation.java:3: 错误: 找不到符号
state.getAsync(key)
               ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpfcpt8hmtTe
- **错误行**: 3

**问题 #24** (第 1179 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp71gkllukAECCallbackProcessor.java:4: 错误: 找不到符号
    void onStateAccessComplete(Key key, long sequence, Result result) {
                               ^
  符号:   类 K
- **错误行**: 4


### `release\v3.0.0\docs\Flink\02-core\checkpoint-mechanism-deep-dive.md`

**问题 #1** (第 174 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcy_94eo8StateBackend.java:3: 错误: 需要<标识符>
    createKeyedStateBackend(env, stateHandles): AbstractKeyedStateBackend<K>
                           ^
C:\Users\luyan\A
- **错误行**: 3

**问题 #5** (第 537 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc4ujq5qyTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend = new EmbeddedRocksDBStateBackend(true);
^
  符号:   类 EmbeddedRocksDBStateBacken
- **错误行**: 4

**问题 #8** (第 704 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp13dnsn16TempValidation.java:4: 错误: 非法的表达式开始
public boolean restoreSavepoint(
^
C:\Users\luyan\AppData\Local\Temp\tmp13dnsn16TempValidation.java:76: 错误: 需要 class、in
- **错误行**: 4

**问题 #10** (第 881 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp42pjraovTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #11** (第 915 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi8ugjmsnTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #12** (第 942 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpohazg2tlTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #13** (第 963 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt4flaw_6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\Flink\02-core\delta-join-production-guide.md`

**问题 #1** (第 59 行, 语言: sql)
- **错误**: 可能的语法问题: -- MYSQL CDC 源：忽略 DELETE 操作
'DEBEZIUM.SKIPPED.OPER...

**问题 #11** (第 699 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnslroikjTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #22** (第 1278 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg1bat7abTempValidation.java:4: 错误: 找不到符号
if (errorRate > 0.05 || avgLatency > 1000) {
    ^
  符号:   变量 errorRate
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #23** (第 1289 行, 语言: sql)
- **错误**: 可能的语法问题: -- 步骤1: 禁用 DELTA JOIN 优化
SET TABLE.OPTIMIZER.DELTA...; 可能的语法问题: -- 步骤2: 增加 REGULAR JOIN 状态 TTL
SET TABLE.EXEC.STAT...; 可能的语法问题: -- 步骤3: 优化 CHECKPOINT 配置
SET EXECUTION.CHECKPOINTI...; 可能的语法问题:

**问题 #24** (第 1332 行, 语言: sql)
- **错误**: 可能的语法问题: 'DEBEZIUM.SKIPPED.OPERATIONS' = 'D',  -- 必须
'DEBEZ...

**问题 #25** (第 1339 行, 语言: sql)
- **错误**: 可能的语法问题: 'LOOKUP.ASYNC' = 'TRUE',
'LOOKUP.CACHE.MAX-ROWS' =...

**问题 #26** (第 1347 行, 语言: sql)
- **错误**: 可能的语法问题: 'LOOKUP.CACHE.MAX-ROWS' = '200000',
'LOOKUP.CACHE....


### `release\v3.0.0\docs\Flink\02-core\delta-join.md`

**问题 #3** (第 244 行, 语言: sql)
- **错误**: 可能的语法问题: -- FLINK SQL开启DELTA JOIN优化
SET TABLE.OPTIMIZER.MUL...

**问题 #4** (第 317 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplpen0ss2AsyncUserProfileLookup.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<UserEvent> userEvents = env.fromSource(
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luya
- **错误行**: 2

**问题 #9** (第 539 行, 语言: sql)
- **错误**: 可能的语法问题: -- 优化后：投影下推，仅查询必要字段
-- 外部查询变为：SELECT USER_ID, AGE,...


### `release\v3.0.0\docs\Flink\02-core\exactly-once-end-to-end.md`

**问题 #2** (第 140 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnmhvy57_TempValidation.java:3: 错误: 找不到符号
        Properties properties = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 3

**问题 #6** (第 305 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_6n6ozbaTempValidation.java:3: 错误: 找不到符号
        Properties properties = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 3

**问题 #7** (第 323 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4w2xyhx2TempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #10** (第 399 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf75h8t3eTempValidation.java:3: 错误: 找不到符号
JdbcXaSinkFunction<Row> xaSink = new JdbcXaSinkFunction<>(
^
  符号:   类 JdbcXaSinkFunction
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #11** (第 440 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph0tlngg1TempValidation.java:4: 错误: 需要';'
protected void preCommit(String pendingFile) throws Exception {
                        ^
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #16** (第 598 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr6ouc0qnTempValidation.java:3: 错误: 需要';'
KafkaSource<String> createKafkaSource(String bootstrapServers, String topic, String groupId) {

- **错误行**: 3

**问题 #17** (第 618 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpivh0ees6TempValidation.java:3: 错误: 需要';'
KafkaSink<String> createKafkaSink(String bootstrapServers, String topic, String transactionalIdPrefix) {

- **错误行**: 3

**问题 #21** (第 814 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp08bkbmwfTempValidation.java:9: 错误: 非法的表达式开始
    protected abstract TXN beginTransaction() throws Exception;
    ^
C:\Users\luyan\AppData\Local\Temp\tmp08bkbmwfTemp
- **错误行**: 9

**问题 #23** (第 884 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz572gzhtTempValidation.java:7: 错误: 需要';'
    public void snapshotState(FunctionSnapshotContext context) throws Exception {
                             ^
C:\Users\
- **错误行**: 7

**问题 #24** (第 918 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp6wp2e1bTempValidation.java:7: 错误: 需要';'
    public void notifyCheckpointComplete(long checkpointId) throws Exception {
                                        ^
C
- **错误行**: 7

**问题 #28** (第 1182 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7mi80oahTempValidation.java:7: 错误: 需要';'
    public void initializeState(FunctionInitializationContext context) throws Exception {
                               ^
- **错误行**: 7


### `release\v3.0.0\docs\Flink\02-core\exactly-once-semantics-deep-dive.md`

**问题 #4** (第 241 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8h84g2g6TempValidation.java:4: 错误: 找不到符号
properties.setProperty("enable.auto.commit", "false");
^
  符号:   变量 properties
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #5** (第 269 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8dxfaoyiTempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #6** (第 285 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvvlvevgaTempValidation.java:4: 错误: 找不到符号
String transactionalIdPrefix = jobId + "-" + operatorId;
                               ^
  符号:   变量 jobId
  位置: 类 TempVal
- **错误行**: 4

**问题 #7** (第 310 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplny7c950TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmplny7c95
- **错误行**: 3

**问题 #8** (第 348 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptunwk4_0TempValidation.java:3: 错误: 找不到符号
        Properties consumerProps = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 3

**问题 #15** (第 919 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1y5ojn_iTempValidation.java:4: 错误: 找不到符号
env.getCheckpointConfig().enableUnalignedCheckpoints(true);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4

**问题 #21** (第 1227 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprsp03swvTempValidation.java:6: 错误: 非法的表达式开始
    private void onCheckpointTimeout(long checkpointId) {
    ^
C:\Users\luyan\AppData\Local\Temp\tmprsp03swvTempValida
- **错误行**: 6


### `release\v3.0.0\docs\Flink\02-core\flink-2.0-forst-state-backend.md`

**问题 #5** (第 370 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqy51e_nzTempValidation.java:4: 错误: 找不到符号
StateDescriptor<V> descriptor = StateDescriptor
^
  符号:   类 StateDescriptor
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 4


### `release\v3.0.0\docs\Flink\02-core\flink-2.2-frontier-features.md`

**问题 #8** (第 709 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaanutpp5TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #9** (第 732 行, 语言: sql)
- **错误**: 可能的语法问题: -- 3. 创建嵌入模型（使用 ML_PREDICT）
<!-- 以下语法为概念设计，实际 FLIN...

**问题 #10** (第 834 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdbhbmmphTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #11** (第 863 行, 语言: sql)
- **错误**: 可能的语法问题: -- 4. 查看物化表
SHOW MATERIALIZED TABLES;...

**问题 #13** (第 1037 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprm8rnw64TempValidation.java:8: 错误: 非法的表达式开始
import org.apache.flink.api.connector.source.SourceReaderContext;
^
C:\Users\luyan\AppData\Local\Temp\tmprm8rnw64TempVa
- **错误行**: 8

**问题 #15** (第 1107 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpye2ggrjhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #16** (第 1124 行, 语言: sql)
- **错误**: 可能的语法问题: -- SQL CLIENT 配置
SET 'CLUSTER.SCHEDULING.STRATEGY'...


### `release\v3.0.0\docs\Flink\02-core\flink-state-management-complete-guide.md`

**问题 #6** (第 551 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8cf4_foxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8cf4_fo
- **错误行**: 3

**问题 #18** (第 1346 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1suo0torTempValidation.java:9: 错误: 不是语句
taskmanager.memory.framework.heap.size: 512mb
                                 ^
C:\Users\luyan\AppData\Local\Temp\tmp1suo0
- **错误行**: 9

**问题 #19** (第 1360 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgb6tfukiTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDb = new EmbeddedRocksDBStateBackend(true);
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置:
- **错误行**: 4

**问题 #21** (第 1392 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxe6q0845TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.typeinfo.Types;
^
C:\Users\luyan\AppData\Local\Temp\tmpxe6q0845TempValidation.java:4
- **错误行**: 4

**问题 #22** (第 1415 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw1s6i_lpTempValidation.java:5: 错误: 找不到符号
for (String key : keys) {
                  ^
  符号:   变量 keys
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 5

**问题 #23** (第 1427 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo0ewqm77TempValidation.java:4: 错误: 找不到符号
if (listSize > MAX_LIST_SIZE) {
    ^
  符号:   变量 listSize
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpo0ew
- **错误行**: 4

**问题 #24** (第 1446 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwf_cm7_aTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpwf_cm7_aTempV
- **错误行**: 4

**问题 #25** (第 1465 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1jq_1vk3TempValidation.java:4: 错误: 找不到符号
env.getCheckpointConfig().enableUnalignedCheckpoints();
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #26** (第 1485 行, 语言: sql)
- **错误**: 可能的语法问题: -- 设置全局 STATE TTL
SET 'SQL.STATE-TTL' = '1 DAY';...

**问题 #27** (第 1516 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpplto3s_4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpplto3
- **错误行**: 3

**问题 #29** (第 1575 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9a4sju8_TempValidation.java:5: 错误: 需要';'
public void open(Configuration parameters) {
                ^
C:\Users\luyan\AppData\Local\Temp\tmp9a4sju8_TempValidation
- **错误行**: 5

**问题 #30** (第 1592 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp09d4cnk4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp09d4c
- **错误行**: 3

**问题 #31** (第 1614 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprdvz3ez3TempValidation.java:4: 错误: 非法的表达式开始
private transient long lastAccessTime;
^
C:\Users\luyan\AppData\Local\Temp\tmprdvz3ez3TempValidation.java:25: 错误: 需要 cl
- **错误行**: 4

**问题 #32** (第 1652 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcw1960xeTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpcw
- **错误行**: 4

**问题 #33** (第 1702 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl89a_m85UserState.java:14: 错误: 需要 class、interface、enum 或 record
env.getConfig().registerTypeWithKryoSerializer(UserState.class, new CompatibleSerializer());
^
C:\U
- **错误行**: 14


### `release\v3.0.0\docs\Flink\02-core\flink-state-ttl-best-practices.md`

**问题 #4** (第 224 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyqmqzzh3TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.StateTtlConfig;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpyqmqzzh
- **错误行**: 3

**问题 #5** (第 246 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8391llkbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8391l
- **错误行**: 3

**问题 #6** (第 269 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcevaggrnTempValidation.java:4: 错误: 找不到符号
StateTtlConfig rocksdbCleanup = StateTtlConfig
^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 4

**问题 #8** (第 325 行, 语言: sql)
- **错误**: 可能的语法问题: -- 设置全局 STATE TTL
SET 'SQL.STATE-TTL' = '1 DAY';...

**问题 #9** (第 350 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpswod_vfdTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpswod_vfdTempValidatio
- **错误行**: 4

**问题 #10** (第 370 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_km_xcctTempValidation.java:7: 错误: 非法的表达式开始
public StateTtlConfig createAggregationTtlConfig() {
^
C:\Users\luyan\AppData\Local\Temp\tmp_km_xcctTempValidation.java
- **错误行**: 7

**问题 #21** (第 890 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe61qgf3vTempValidation.java:5: 错误: 找不到符号
    (Gauge<Long>) () -> {
     ^
  符号:   类 Gauge
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpe61qgf3vTempV
- **错误行**: 5

**问题 #22** (第 907 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8v6yvw_rTempValidation.java:5: 错误: 需要';'
public void open(Configuration parameters) {
                ^
C:\Users\luyan\AppData\Local\Temp\tmp8v6yvw_rTempValidation
- **错误行**: 5

**问题 #24** (第 924 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt4lc96i2TempValidation.java:3: 错误: 非法的表达式开始
        .cleanupIncrementally(
        ^
C:\Users\luyan\AppData\Local\Temp\tmpt4lc96i2TempValidation.java:6: 错误: 需要';'

- **错误行**: 3

**问题 #25** (第 933 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb0y1evbeTempValidation.java:3: 错误: 找不到符号
        env.setStateBackend(new EmbeddedRocksDBStateBackend());
                                ^
  符号:   类 EmbeddedRocksD
- **错误行**: 3

**问题 #26** (第 952 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoq01u8apTempValidation.java:3: 错误: 找不到符号
        DefaultConfigurableOptionsFactory factory = new DefaultConfigurableOptionsFactory();
        ^
  符号:   类 DefaultCo
- **错误行**: 3


### `release\v3.0.0\docs\Flink\02-core\forst-state-backend.md`

**问题 #6** (第 459 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg1kklseiTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpg1
- **错误行**: 4


### `release\v3.0.0\docs\Flink\02-core\multi-way-join-optimization.md`

**问题 #10** (第 354 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy4em_i49TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpy4e
- **错误行**: 3

**问题 #11** (第 389 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn0qs6mmzTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpn0q
- **错误行**: 3


### `release\v3.0.0\docs\Flink\02-core\network-stack-evolution.md`

**问题 #9** (第 526 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps6ghx86vTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\Flink\02-core\smart-checkpointing-strategies.md`

**问题 #20** (第 1204 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuebqsvp5TempValidation.java:5: 错误: 非法字符: '#'
# ============================================================
^
C:\Users\luyan\AppData\Local\Temp\tmpuebqsvp5TempVali
- **错误行**: 5

**问题 #21** (第 1234 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbxim1djdTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #22** (第 1261 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp1i9scwyTempValidation.java:5: 错误: 非法字符: '#'
# ============================================================
^
C:\Users\luyan\AppData\Local\Temp\tmpp1i9scwyTempVali
- **错误行**: 5

**问题 #23** (第 1290 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvu7_zhhcTempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend rocksDbBackend = new RocksDBStateBackend(
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempValidation
C:\Us
- **错误行**: 4

**问题 #24** (第 1315 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdc_4x3vqTempValidation.java:5: 错误: 非法字符: '#'
# ============================================================
^
C:\Users\luyan\AppData\Local\Temp\tmpdc_4x3vqTempVali
- **错误行**: 5

**问题 #25** (第 1341 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp822wj1ppTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #26** (第 1374 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3zj97t64TempValidation.java:5: 错误: 非法字符: '#'
# ============================================================
^
C:\Users\luyan\AppData\Local\Temp\tmp3zj97t64TempVali
- **错误行**: 5

**问题 #27** (第 1400 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptc7s2_w4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\Flink\02-core\state-backend-evolution-analysis.md`

**问题 #2** (第 284 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgxnwny0eTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #3** (第 309 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmnz_lv9cTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #5** (第 370 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdvounwwvTempValidation.java:4: 错误: 找不到符号
ForStStateBackend forstBackend = new ForStStateBackend();
^
  符号:   类 ForStStateBackend
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #7** (第 428 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpampft9gpEmbeddedRocksDBStateBackend.java:37: 错误: 非法的表达式开始
        );
        ^
1 个错误

- **错误行**: 37

**问题 #8** (第 481 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj1pcbqs7ForStStateBackend.java:46: 错误: 非法的表达式开始
        );
        ^
1 个错误

- **错误行**: 46


### `release\v3.0.0\docs\Flink\02-core\state-backends-deep-comparison.md`

**问题 #3** (第 543 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu03nevz_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #5** (第 580 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzng_cxj1TempValidation.java:5: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 5

**问题 #6** (第 630 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpupo7h0x9TempValidation.java:5: 错误: 找不到符号
ForStStateBackend forstBackend = new ForStStateBackend();
^
  符号:   类 ForStStateBackend
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 5


### `release\v3.0.0\docs\Flink\02-core\streaming-etl-best-practices.md`

**问题 #5** (第 513 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd_4otf9fTempValidation.java:4: 错误: 找不到符号
MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
^
  符号:   类 MySqlSource
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #7** (第 555 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqm2kmnbcTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.state.ValueState;
^
C:\Users\luyan\AppData\Local\Temp\tmpqm2kmnbcTempValidation.java
- **错误行**: 4

**问题 #8** (第 590 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4dkwzyleTempValidation.java:4: 错误: 找不到符号
JdbcInputFormat jdbcInput = JdbcInputFormat.buildJdbcInputFormat()
^
  符号:   类 JdbcInputFormat
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #11** (第 744 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6eykk961TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp6eykk961TempValidat
- **错误行**: 4

**问题 #12** (第 809 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphj8vrwktTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmphj8vrwktTempValidatio
- **错误行**: 4

**问题 #14** (第 850 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps8ev1h4zAsyncDatabaseRequest.java:43: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedEvent> enriched = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以启用 未命名
- **错误行**: 43

**问题 #15** (第 925 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqqd36ubbTempValidation.java:18: 错误: 不是语句
"INSERT INTO table (id, value) VALUES (?, ?) " +
^
C:\Users\luyan\AppData\Local\Temp\tmpqqd36ubbTempValidation.java:19: 错误
- **错误行**: 18

**问题 #17** (第 1001 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpma6bght0TempValidation.java:4: 错误: 找不到符号
StreamingFileSink<Record> sink = StreamingFileSink
^
  符号:   类 StreamingFileSink
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4

**问题 #22** (第 1173 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3axi4jgsTempValidation.java:4: 错误: 找不到符号
AvroDeserializationSchema<Order> schema = AvroDeserializationSchema
^
  符号:   类 AvroDeserializationSchema
  位置: 类 TempVali
- **错误行**: 4

**问题 #25** (第 1302 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcpq_yn1jTempValidation.java:4: 错误: 找不到符号
env.getConfig().setAutoWatermarkInterval(200L);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #26** (第 1327 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpov5osp3gTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpov5os
- **错误行**: 3

**问题 #27** (第 1356 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9r09asarTempValidation.java:4: 错误: 找不到符号
SpecificAvroSerde<Order> serde = new SpecificAvroSerde<>();
^
  符号:   类 SpecificAvroSerde
  位置: 类 TempValidation
C:\Users\
- **错误行**: 4

**问题 #31** (第 1438 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsdc1311_TempValidation.java:4: 错误: 找不到符号
OutputTag<FailedRecord> dlqTag = new OutputTag<FailedRecord>("dlq"){};
^
  符号:   类 OutputTag
  位置: 类 TempValidation
C:\Use
- **错误行**: 4


### `release\v3.0.0\docs\Flink\02-core\time-semantics-and-watermark.md`

**问题 #1** (第 300 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4p4dxo3vTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp4p4dx
- **错误行**: 3

**问题 #2** (第 310 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpegaj099sTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpegaj0
- **错误行**: 3

**问题 #3** (第 320 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe48fo2v2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpe48fo
- **错误行**: 3

**问题 #6** (第 550 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb8irj_heTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpb8i
- **错误行**: 3

**问题 #7** (第 562 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe4ukh4fdTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpe4u
- **错误行**: 3

**问题 #8** (第 578 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt9luq2yhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpt9luq
- **错误行**: 3

**问题 #9** (第 589 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprxkhu2_0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmprxkhu
- **错误行**: 3

**问题 #10** (第 600 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0lh241_dTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp0lh24
- **错误行**: 3

**问题 #11** (第 614 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphpxilh6vTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmphpx
- **错误行**: 3

**问题 #24** (第 1150 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf7tg8pb3WatermarkStrategy.java:19: 错误: 需要 class、interface、enum 或 record
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
^
1 个错误

- **错误行**: 19


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\ansi-sql-2023-compliance-guide.md`

**问题 #1** (第 105 行, 语言: sql)
- **错误**: 可能的语法问题: MATCH_RECOGNIZE (
    PARTITION BY PARTITION_KEY  ...

**问题 #5** (第 372 行, 语言: sql)
- **错误**: 可能的语法问题: JSON_VALUE(JSON_FIELD, '$.PATH'
    RETURNING VARC...

**问题 #6** (第 393 行, 语言: sql)
- **错误**: 可能的语法问题: JSON_TABLE(
    JSON_DATA,
    '$.ITEMS[*]'
    CO...

**问题 #8** (第 502 行, 语言: sql)
- **错误**: 可能的语法问题: -- 执行结果示例
-- {"ORDER_ID":1001,"CUSTOMER":"ALICE","...

**问题 #13** (第 606 行, 语言: sql)
- **错误**: 可能的语法问题: -- 输出: 每5分钟累积一次，每小时重置
-- [00:00, 00:05), [00:00, 0...

**问题 #24** (第 1058 行, 语言: sql)
- **错误**: 可能的语法问题: -- ============================================
--...


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\data-types-complete-reference.md`

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
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc68n3hbpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.DataTypes;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpc68n3hbpTempValidat
- **错误行**: 3

**问题 #19** (第 586 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpurnrmz0aTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpurnrmz0aTempV
- **错误行**: 3

**问题 #22** (第 691 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_wkg_13_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp_wkg_13_Temp
- **错误行**: 3


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\flink-cep-complete-guide.md`

**问题 #9** (第 316 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu6yhhd25LoginEvent.java:16: 错误: 未命名类 是预览功能，默认情况下禁用。
Pattern<LoginEvent, ?> pattern = Pattern
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 16

**问题 #10** (第 352 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8w_87e_bTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.cep.pattern.Pattern;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8w_87e_bTempValidat
- **错误行**: 3

**问题 #11** (第 387 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2rrk_5erTempValidation.java:4: 错误: 找不到符号
Pattern.<Event>begin("login").where(evt -> evt.type.equals("LOGIN"))
         ^
  符号:   类 Event
  位置: 类 TempValidation
C:\
- **错误行**: 4

**问题 #12** (第 424 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8uvfukagTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.pattern.conditions.IterativeCondition;
^
C:\Users\luyan\AppData\Local\Temp\tmp8uvfukagTempV
- **错误行**: 3

**问题 #13** (第 475 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzf867sc4TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.CEP;
^
C:\Users\luyan\AppData\Local\Temp\tmpzf867sc4TempValidation.java:3: 错误: 不是语句
import
- **错误行**: 3

**问题 #18** (第 982 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7v4bhb1cTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.cep.nfa.aftermatch.AfterMatchSkipStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 3

**问题 #19** (第 1005 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmperw0eyp6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmperw0e
- **错误行**: 3

**问题 #20** (第 1028 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy81vpqs2TempValidation.java:5: 错误: 找不到符号
    MyEvent.class,
    ^
  符号:   类 MyEvent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpy81vpqs2TempValidat
- **错误行**: 5

**问题 #21** (第 1044 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvbu_qdyzTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpvbu_q
- **错误行**: 3

**问题 #26** (第 1251 行, 语言: sql)
- **错误**: 可能的语法问题: -- AFTER MATCH SKIP子句
AFTER MATCH SKIP PAST LAST R...


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\flink-materialized-table-deep-dive.md`

**问题 #2** (第 113 行, 语言: sql)
- **错误**: 可能的语法问题: -- HASH分布（默认）
DISTRIBUTED BY HASH(USER_ID) INTO 16...


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\flink-process-table-functions.md`

**问题 #9** (第 500 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmfd_zo32DeduplicationPTF.java:11: 错误: 需要 class、interface、enum 或 record
import org.apache.flink.api.common.typeinfo.Types;
^
1 个错误

- **错误行**: 11

**问题 #10** (第 562 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaqx65f8aTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpaqx65f8aTemp
- **错误行**: 3

**问题 #12** (第 708 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmhy80hczMLInferencePTF.java:13: 错误: 需要 class、interface、enum 或 record
import org.apache.flink.api.common.state.ValueState;
^
C:\Users\luyan\AppData\Local\Temp\tmpmh
- **错误行**: 13


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\flink-python-udf.md`

**问题 #5** (第 277 行, 语言: python)
- **错误**: SyntaxError: invalid syntax
- **错误行**: 32

**问题 #10** (第 516 行, 语言: yaml)
- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 10, column 1:
    pandas==2.1.4
    ^ (line: 10)
- **错误行**: 10


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\flink-sql-calcite-optimizer-deep-dive.md`

**问题 #10** (第 652 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5vzq0lvwTempValidation.java:4: 错误: 找不到符号
VolcanoPlanner planner = new VolcanoPlanner(
^
  符号:   类 VolcanoPlanner
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #14** (第 774 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph5ygzt3pTempValidation.java:4: 错误: 非法的表达式开始
void optimizeGroup(Group group, Cost upperBound) {
^
C:\Users\luyan\AppData\Local\Temp\tmph5ygzt3pTempValidation.java:4
- **错误行**: 4

**问题 #16** (第 827 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaf_cq651TempValidation.java:4: 错误: 非法的表达式开始
public void onMatch(RelOptRuleCall call) {
^
C:\Users\luyan\AppData\Local\Temp\tmpaf_cq651TempValidation.java:37: 错误: 需
- **错误行**: 4

**问题 #19** (第 906 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa4wanw0pTempValidation.java:4: 错误: 非法的表达式开始
public void onMatch(RelOptRuleCall call) {
^
C:\Users\luyan\AppData\Local\Temp\tmpa4wanw0pTempValidation.java:26: 错误: 需
- **错误行**: 4

**问题 #23** (第 1009 行, 语言: sql)
- **错误**: 可能的语法问题: -- 启用两阶段聚合
SET TABLE.OPTIMIZER.AGG-PHASE-STRATEGY ...; 可能的语法问题: -- 或自动选择
SET TABLE.OPTIMIZER.AGG-PHASE-STRATEGY = ...

**问题 #41** (第 1553 行, 语言: sql)
- **错误**: 可能的语法问题: -- 分析整张表
ANALYZE TABLE ORDERS COMPUTE STATISTICS;...; 可能的语法问题: -- 分析指定列
ANALYZE TABLE ORDERS COMPUTE STATISTICS F...; 可能的语法问题: -- 采样分析
ANALYZE TABLE BIG_TABLE COMPUTE STATISTICS...; 可能的语法问题:

**问题 #44** (第 1630 行, 语言: sql)
- **错误**: 可能的语法问题: -- 优化1: 添加统计信息
ANALYZE TABLE ORDERS COMPUTE STATIS...; 可能的语法问题: ANALYZE TABLE PRODUCTS COMPUTE STATISTICS;...; 可能的语法问题: ANALYZE TABLE CATEGORIES COMPUTE STATISTICS;...; 可能的语法问题: -- 优化2: 启用CBO

**问题 #50** (第 1759 行, 语言: sql)
- **错误**: 可能的语法问题: -- 优化1: 启用DISTINCT拆分
SET TABLE.OPTIMIZER.DISTINCT-...; 可能的语法问题: -- 优化2: 启用MINI-BATCH
SET TABLE.EXEC.MINI-BATCH.ENA...; 可能的语法问题: -- 优化3: 启用LOCAL-GLOBAL聚合
SET TABLE.OPTIMIZER.LOCAL...; 可能的语法问题:

**问题 #66** (第 2513 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp768v0z8aBatchPhysicalRel.java:31: 错误: 非法的表达式开始
        Transformation<RowData> leftInput = ...;
                                            ^
C:\Users\luyan\AppDat
- **错误行**: 31


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\flink-sql-hints-optimization.md`

**问题 #12** (第 324 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgwtgiwrjTempValidation.java:4: 错误: 找不到符号
tableEnv.createTemporaryFunction("ExtractJson", JsonPathFunction.class);
                                                ^
- **错误行**: 4

**问题 #13** (第 339 行, 语言: sql)
- **错误**: 可能的语法问题: -- 基础执行计划
EXPLAIN PLAN FOR
SELECT /*+ BROADCAST_HA...; 可能的语法问题: -- 详细执行计划（含优化器决策）
EXPLAIN ESTIMATED_COST, CHANGELO...


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\flink-sql-window-functions-deep-dive.md`

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


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\flink-table-sql-complete-guide.md`

**问题 #7** (第 372 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwh0n3xrvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwh0n3xrvTempV
- **错误行**: 3

**问题 #10** (第 446 行, 语言: sql)
- **错误**: 可能的语法问题: -- 切换数据库
USE ANALYTICS;...

**问题 #13** (第 501 行, 语言: sql)
- **错误**: 可能的语法问题: <!-- 以下语法为概念设计，实际 FLINK 版本尚未支持 -->
~~CREATE MODEL~...

**问题 #19** (第 584 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr8oitxn_TempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.from("orders")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpr8oit
- **错误行**: 4

**问题 #24** (第 678 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp059aoj95TempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.from("user_events")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #32** (第 814 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3jexz8zrTempValidation.java:4: 错误: 找不到符号
Table topN = tableEnv.from("product_sales")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #39** (第 962 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphy9homv4TempValidation.java:4: 错误: 找不到符号
Table windowed = tableEnv.from("user_events")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4

**问题 #44** (第 1071 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkm_2wclsTempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.from("orders")
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpkm_2w
- **错误行**: 4

**问题 #53** (第 1377 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0s2g4gg_TempValidation.java:12: 错误: 非法的表达式开始
    .next("C").where(...)
                     ^
C:\Users\luyan\AppData\Local\Temp\tmp0s2g4gg_TempValidation.java:13:
- **错误行**: 12

**问题 #58** (第 1516 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 22

**问题 #64** (第 1654 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkbqiojl6TempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql(
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #66** (第 1718 行, 语言: sql)

- **错误**: 可能的语法问题: -- 创建嵌入模型
<!-- 以下语法为概念设计，实际 FLINK 版本尚未支持 -->
~~CRE...; 可能的语法问题: -- 创建分类模型
~~CREATE MODEL SENTIMENT_CLASSIFIER~~ (未...

**问题 #76** (第 2076 行, 语言: sql)

- **错误**: 可能的语法问题: -- 1. 配置 STATE TTL
SET 'TABLE.EXEC.STATE.TTL' = '1...; 可能的语法问题: -- 3. 增量 CHECKPOINT
SET 'STATE.BACKEND.INCREMENTAL...; 可能的语法问题: -- 4. ROCKSDB 调优
SET 'STATE.BACKEND.ROCKSDB.PREDEF...

**问题 #77** (第 2094 行, 语言: sql)

- **错误**: 可能的语法问题: -- 1. 合理设置 WATERMARK 延迟
-- 过小: 丢数据
-- 过大: 延迟高
WATE...; 可能的语法问题: -- 3. 允许延迟数据
SET 'TABLE.EXEC.EMIT.ALLOW-LATENESS' ...


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\flink-vector-search-rag.md`

**问题 #14** (第 594 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...; 可能的语法问题: -- ============================================
--...


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\materialized-tables.md`

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

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjfgv537_TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpjfgv537_TempValidat
- **错误行**: 4

**问题 #19** (第 732 行, 语言: sql)

- **错误**: 可能的语法问题: -- FLINK 2.2+ 新增语法

-- 列出所有物化表
SHOW MATERIALIZED T...; 可能的语法问题: -- 列出指定数据库的物化表
SHOW MATERIALIZED TABLES FROM ANALY...; 可能的语法问题: -- 带过滤条件
SHOW MATERIALIZED TABLES LIKE 'USER%';...; 可能的语法问题: --

**问题 #26** (第 1005 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看所有物化表（FLINK 2.2+）
SHOW MATERIALIZED TABLES [F...


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\model-ddl-and-ml-predict.md`

**问题 #1** (第 19 行, 语言: sql)

- **错误**: 可能的语法问题: <!-- 以下语法为概念设计，实际 FLINK 版本尚未支持 -->
~~CREATE MODEL~...

**问题 #10** (第 257 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3qsltedkTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp3qsltedkTempValidat
- **错误行**: 4

**问题 #13** (第 415 行, 语言: sql)

- **错误**: 可能的语法问题: -- 步骤 1: 创建 OPENAI 模型定义
<!-- 以下为概念设计 -->
~~CREATE ...

**问题 #14** (第 494 行, 语言: sql)

- **错误**: 可能的语法问题: -- 步骤 1: 创建嵌入模型（用于文档向量化）
~~CREATE MODEL TEXT_EMBED...; 可能的语法问题: -- 步骤 2: 创建 LLM 模型
~~CREATE MODEL QA_MODEL~~ (未来可能...

**问题 #16** (第 652 行, 语言: sql)

- **错误**: 可能的语法问题: ~~CREATE MODEL INTERNAL_CLASSIFIER~~ (未来可能的语法)
WIT...


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\query-optimization-analysis.md`

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


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\sql-functions-cheatsheet.md`

**问题 #3** (第 798 行, 语言: sql)

- **错误**: 可能的语法问题: -- 数学
ABS(), ROUND(), CEIL(), FLOOR(), POWER(), SQ...


### `release\v3.0.0\docs\Flink\03-api\03.02-table-sql-api\sql-vs-datastream-comparison.md`

**问题 #3** (第 267 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp42qmniy3TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.functions.AggregateFunction;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #5** (第 302 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqqqj21jjTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpqqqj21jjTempValidatio
- **错误行**: 4

**问题 #6** (第 324 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzjiz0bg2AsyncUserEnrichment.java:23: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedOrder> enriched = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以启用 未命名类
- **错误行**: 23

**问题 #7** (第 358 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbg2i6dk8TempValidation.java:4: 错误: 找不到符号
tableEnv.createTemporaryView("orders", orderStream);
                                       ^
  符号:   变量 orderStream
  位置:
- **错误行**: 4


### `release\v3.0.0\docs\Flink\03-api\09-language-foundations\02-python-api.md`

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


### `release\v3.0.0\docs\Flink\03-api\09-language-foundations\03-rust-native.md`

**问题 #7** (第 451 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyqkpc_jlTempValidation.java:4: 错误: 找不到符号
    stream,
    ^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpyqkpc_jlTempValidation.jav
- **错误行**: 4


### `release\v3.0.0\docs\Flink\03-api\09-language-foundations\04-streaming-lakehouse.md`

**问题 #19** (第 575 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_CATALOG;...

**问题 #21** (第 775 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...


### `release\v3.0.0\docs\Flink\03-api\09-language-foundations\06-risingwave-deep-dive.md`

**问题 #21** (第 1269 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprvsj38t0TempValidation.java:13: 错误: 找不到符号
MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
^
  符号:   类 MySqlSource
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 13

**问题 #24** (第 1351 行, 语言: sql)

- **错误**: 可能的语法问题: -- 7. 应用层查询示例（LLM RAG 调用）
-- SELECT * FROM RAG_RET...


### `release\v3.0.0\docs\Flink\03-api\09-language-foundations\07-rust-streaming-landscape.md`

**问题 #16** (第 876 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx5sesmomTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpx5s
- **错误行**: 3


### `release\v3.0.0\docs\Flink\03-api\09-language-foundations\08-flink-rust-connector-dev.md`

**问题 #36** (第 2075 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp56oi7j2iRustKafkaSourceIntegrationTest.java:3: 错误: 需要 class、interface、enum 或 record
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
- **错误行**: 3


### `release\v3.0.0\docs\Flink\03-api\09-language-foundations\10-wasi-component-model.md`

**问题 #15** (第 789 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_erl2q48WasiComponentOperator.java:77: 错误: 非法的表达式开始
                byte[] value = getRuntimeContext().getState(...).value();

- **错误行**: 77


### `release\v3.0.0\docs\Flink\03-api\09-language-foundations\datastream-api-cheatsheet.md`

**问题 #1** (第 38 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2b4zzt2qTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2b4
- **错误行**: 3

**问题 #3** (第 83 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp35f9ll4oTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp35f
- **错误行**: 3

**问题 #5** (第 128 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9pcbnlm_TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp9pcbnlm_TempValidat
- **错误行**: 4

**问题 #6** (第 152 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9m667ejpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9m6
- **错误行**: 3

**问题 #7** (第 180 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp401lrbfiTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp401
- **错误行**: 3

**问题 #8** (第 226 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6j5cu_6_TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp6j5cu_6_TempValidat
- **错误行**: 4

**问题 #9** (第 261 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1bmn_8s1CountWithTimeout.java:1: 错误: 程序包org.apache.flink.streaming.api.functions不存在
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;

- **错误行**: 1

**问题 #10** (第 320 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpghygxek_TempValidation.java:4: 错误: 找不到符号
stream.print();                           // 输出到stdout
^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #11** (第 344 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphki5_m91TempValidation.java:4: 错误: 找不到符号
KafkaSink<String> sink = KafkaSink.<String>builder()
^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #12** (第 407 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6n681nwkTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #13** (第 432 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsy6158h6TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpsy6158h6TempValidat
- **错误行**: 4

**问题 #14** (第 482 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe62kb75hTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpe62kb
- **错误行**: 3

**问题 #15** (第 514 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr2qgachhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpr2qga
- **错误行**: 3

**问题 #17** (第 632 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8wvb9algTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8wvb9
- **错误行**: 3

**问题 #18** (第 652 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpctu4644wTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpctu4644wTempValidat
- **错误行**: 4

**问题 #19** (第 725 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcvi4sfqyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpcvi4sfq
- **错误行**: 3


### `release\v3.0.0\docs\Flink\03-api\09-language-foundations\flink-25-wasm-udf-ga.md`

**问题 #43** (第 2163 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5o6qwhs0TempValidation.java:4: 错误: 找不到符号
WasmFunctionConfig optimalConfig = WasmFunctionConfig.builder()
^
  符号:   类 WasmFunctionConfig
  位置: 类 TempValidation
C:\U
- **错误行**: 4


### `release\v3.0.0\docs\Flink\03-api\09-language-foundations\flink-datastream-api-complete-guide.md`

**问题 #4** (第 184 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphff1d4ojTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmphff1d4ojTempValidat
- **错误行**: 4

**问题 #8** (第 284 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxehfdnlfTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpxehfdnlfTempValidat
- **错误行**: 4

**问题 #11** (第 406 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphi2u940sTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmphi2u940sTempV
- **错误行**: 3

**问题 #14** (第 555 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmt4kqz8qTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpmt4
- **错误行**: 3

**问题 #15** (第 576 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7g49si3eTempValidation.java:8: 错误: 需要';'
public void onTimer(long timestamp, OnTimerContext ctx, Collector<Out> out) {
                   ^
C:\Users\luyan\AppData\
- **错误行**: 8

**问题 #17** (第 625 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi8vxyswrCustomWatermarkGenerator.java:2: 错误: 需要 class、interface、enum 或 record
WatermarkStrategy.<Event>forMonotonousTimestamps()
^
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 2

**问题 #19** (第 673 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxyykhajzTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpxyy
- **错误行**: 3

**问题 #21** (第 720 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsezexak2AsyncDatabaseRequest.java:51: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Result> asyncResult = AsyncDataStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 51

**问题 #23** (第 813 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcnbb8p5oTempValidation.java:7: 错误: 找不到符号
timeout = 5_000;  // 5 seconds
^
  符号:   变量 timeout
  位置: 类 TempValidation
1 个错误

- **错误行**: 7

**问题 #28** (第 1029 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyopgwzpxTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpyopgwzpxTempValidat
- **错误行**: 4

**问题 #29** (第 1105 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3y8go_6hTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmp3y8go_6hTempValidatio
- **错误行**: 4

**问题 #32** (第 1178 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdfrsdn9wTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpdfrsdn9wTempValidat
- **错误行**: 4

**问题 #33** (第 1258 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqc_li1yzTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.state.ValueState;
^
C:\Users\luyan\AppData\Local\Temp\tmpqc_li1yzTempValidation.java
- **错误行**: 4

**问题 #35** (第 1336 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplm9ml3m6TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.state.ValueState;
^
C:\Users\luyan\AppData\Local\Temp\tmplm9ml3m6TempValidation.java
- **错误行**: 4

**问题 #36** (第 1359 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi18clw71TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.state.ValueState;
^
C:\Users\luyan\AppData\Local\Temp\tmpi18clw71TempValidation.java
- **错误行**: 4

**问题 #39** (第 1543 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbxvykg85TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpbxv
- **错误行**: 3

**问题 #41** (第 1597 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp73t4e0rwTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp73t4e0rwTempValidat
- **错误行**: 4


### `release\v3.0.0\docs\Flink\03-api\09-language-foundations\flink-language-support-complete-guide.md`

**问题 #2** (第 196 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy1tl793aTempValidation.java:4: 错误: 需要';'
List<Integer> vs List<String> → 都是 List
                ^
C:\Users\luyan\AppData\Local\Temp\tmpy1tl793aTempValidation.java
- **错误行**: 4

**问题 #6** (第 481 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk4__xr5uFlinkSpringConfig.java:3: 错误: 需要 class、interface、enum 或 record
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luy
- **错误行**: 3

**问题 #11** (第 872 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 3

**问题 #14** (第 1175 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqxj5c9uiJavaWithScalaUDF.java:27: 错误: 需要'{'
class ScalaMapFunction[T, R] extends RichMapFunction[T, R] {
                      ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 27


### `release\v3.0.0\docs\Flink\04-runtime\04.01-deployment\evolution\config-management.md`

**问题 #1** (第 48 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplt1b_aucTempValidation.java:3: 错误: 找不到符号
ConfigManager cm = ConfigManager.getInstance();
^
  符号:   类 ConfigManager
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 3


### `release\v3.0.0\docs\Flink\04-runtime\04.01-deployment\evolution\scheduling-evolution.md`

**问题 #2** (第 301 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkq6excqpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #3** (第 320 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4sj7rlu5TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #4** (第 339 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpngz7m14iTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #5** (第 362 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp82trs3huTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #6** (第 392 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplw4ez3phTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\Flink\04-runtime\04.01-deployment\evolution\yarn-deploy.md`

**问题 #3** (第 58 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpngr1lle5TempValidation.java:3: 错误: 找不到符号
        env.getConfig().setAutoWatermarkInterval(200);
        ^
  符号:   变量 env
  位置: 类 TempValidation
1 个错误

- **错误行**: 3


### `release\v3.0.0\docs\Flink\04-runtime\04.01-deployment\flink-24-deployment-improvements.md`

**问题 #75** (第 2866 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    flink-conf-global.yaml: |
    ^ (line: 4)
found duplicate key "apiVersion" with value "flink.apache.org/v1beta1" (original v
- **错误行**: 4


### `release\v3.0.0\docs\Flink\04-runtime\04.01-deployment\flink-deployment-ops-complete-guide.md`

**问题 #16** (第 413 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 2:
     taskmanager.numberOfTaskSlots: 8
     ^ (line: 2)
found duplicate key "taskmanager.numberOfTaskSlots" with value "4" (origi
- **错误行**: 2

**问题 #17** (第 425 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    taskmanager.memory.network.min: 64mb
    ^ (line: 2)
found duplicate key "taskmanager.memory.network.min" with value "256mb"
- **错误行**: 2

**问题 #18** (第 437 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    execution.checkpointing.interval ...
    ^ (line: 2)
found duplicate key "execution.checkpointing.interval" with value "30s
- **错误行**: 2

**问题 #42** (第 1147 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo_49xkw_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpo_4
- **错误行**: 3


### `release\v3.0.0\docs\Flink\04-runtime\04.01-deployment\flink-k8s-operator-1.14-guide.md`

**问题 #7** (第 156 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvx89bhclTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpvx8
- **错误行**: 3

**问题 #9** (第 195 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 2, column 17:
      deploymentName: string,      # FlinkDeployment 引用
                    ^ (line: 2)
- **错误行**: 2
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #29** (第 605 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwpsmi1csTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpwpsmi1csTempValidat
- **错误行**: 4

**问题 #44** (第 985 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 15, column 26:
            - blue: 90, green: 10, duration: 5m
                             ^ (line: 15)
- **错误行**: 15
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `release\v3.0.0\docs\Flink\04-runtime\04.01-deployment\flink-kubernetes-autoscaler-deep-dive.md`

**问题 #19** (第 471 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 12, column 78:
     ... ."Source: Kafka".max-parallelism: "12"
                                         ^ (line: 12)
- **错误行**: 12
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `release\v3.0.0\docs\Flink\04-runtime\04.01-deployment\flink-kubernetes-operator-deep-dive.md`

**问题 #6** (第 165 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqn3xyu58TempValidation.java:4: 错误: 找不到符号
while (running) {
       ^
  符号:   变量 running
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpqn3xyu58TempVali
- **错误行**: 4


### `release\v3.0.0\docs\Flink\04-runtime\04.01-deployment\flink-serverless-architecture.md`

**问题 #6** (第 255 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0atxd463TempValidation.java:5: 错误: 需要';'
public Response handle(Request req) {
                      ^
C:\Users\luyan\AppData\Local\Temp\tmp0atxd463TempValidation.
- **错误行**: 5


### `release\v3.0.0\docs\Flink\04-runtime\04.01-deployment\multi-cloud-deployment-templates.md`

**问题 #10** (第 912 行, 语言: yaml)

- **错误**: could not determine a constructor for the tag '!Ref'
  in "<unicode string>", line 290, column 12:
        Value: !Ref FlinkApplication
               ^ (line: 290)
- **错误行**: 290

**问题 #21** (第 2453 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 23, column 52:
     ... aproc.logging.stackdriver.enable: 'true'
                                         ^ (line: 23)
- **错误行**: 23
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `release\v3.0.0\docs\Flink\04-runtime\04.01-deployment\serverless-flink-ga-guide.md`

**问题 #10** (第 460 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    spec:
    ^ (line: 2)
found duplicate key "spec" with value "{}" (original value: "{}")
  in "<unicode string>", line 7, col
- **错误行**: 2

**问题 #11** (第 475 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend: hashmap  # 内存状态，重启丢失
    ^ (line: 2)
found duplicate key "state.backend" with value "forst" (original value:
- **错误行**: 2

**问题 #15** (第 773 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 98, column 22:
        resourceGroupName: "flink-serverless",
                         ^ (line: 98)
- **错误行**: 98
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `release\v3.0.0\docs\Flink\04-runtime\04.03-observability\distributed-tracing.md`

**问题 #2** (第 88 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9qda10rvTempValidation.java:4: 错误: 不是语句
   traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
                  ^
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #8** (第 350 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpib1v98npTracingStreamOperator.java:2: 错误: 找不到符号
class TracingStreamOperator<OUT> extends AbstractStreamOperator<OUT> {
                                         ^

- **错误行**: 2


### `release\v3.0.0\docs\Flink\04-runtime\04.03-observability\evolution\alerting-evolution.md`

**问题 #2** (第 65 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp039d_ok7TempValidation.java:3: 错误: 找不到符号
        AlertManager.register(new AlertRule()
        ^
  符号:   变量 AlertManager
  位置: 类 TempValidation
C:\Users\luyan\AppD
- **错误行**: 3


### `release\v3.0.0\docs\Flink\04-runtime\04.03-observability\evolution\logging-evolution.md`

**问题 #2** (第 55 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnagwqbvvTempValidation.java:3: 错误: 找不到符号
        LOG.info("Processing event",
        ^
  符号:   变量 LOG
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3


### `release\v3.0.0\docs\Flink\04-runtime\04.03-observability\evolution\metrics-evolution.md`

**问题 #2** (第 56 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi3okeuk5TempValidation.java:3: 错误: 找不到符号
        getRuntimeContext()
        ^
  符号:   方法 getRuntimeContext()
  位置: 类 TempValidation
1 个错误

- **错误行**: 3


### `release\v3.0.0\docs\Flink\04-runtime\04.03-observability\evolution\slo-evolution.md`

**问题 #2** (第 65 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwdomtwqgTempValidation.java:3: 错误: 找不到符号
        double errorBudget = 1 - slo.getTarget();
                                 ^
  符号:   变量 slo
  位置: 类 TempValidation
- **错误行**: 3


### `release\v3.0.0\docs\Flink\04-runtime\04.03-observability\evolution\testing-evolution.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq0le1uuwTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpq0
- **错误行**: 4

**问题 #2** (第 74 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2dy4wwunTempValidation.java:3: 错误: 找不到符号
        MiniCluster cluster = new MiniCluster(
        ^
  符号:   类 MiniCluster
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3


### `release\v3.0.0\docs\Flink\04-runtime\04.03-observability\evolution\tracing-evolution.md`

**问题 #2** (第 63 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1alui045TempValidation.java:3: 错误: 找不到符号
Span span = tracer.spanBuilder("process").startSpan();
^
  符号:   类 Span
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 3


### `release\v3.0.0\docs\Flink\04-runtime\04.03-observability\evolution\webui-evolution.md`

**问题 #1** (第 48 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvm6dg_z0TempValidation.java:3: 错误: 非法的表达式开始
        GET /jobs/{jobid}/vertices
                  ^
C:\Users\luyan\AppData\Local\Temp\tmpvm6dg_z0TempValidation.java
- **错误行**: 3


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\04.04-cdc-debezium-integration.md`

**问题 #10** (第 581 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9lvnpjygTempValidation.java:3: 错误: 非法的表达式开始
        import com.ververica.cdc.connectors.mysql.source.MySqlSource;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9l
- **错误行**: 3

**问题 #11** (第 615 行, 语言: sql)

- **错误**: 可能的语法问题: -- POSTGRESQL配置（POSTGRESQL.CONF）
WAL_LEVEL = LOGIC...

**问题 #15** (第 813 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查询数据湖（流读模式）
SET 'EXECUTION.RUNTIME-MODE' = 'STR...

**问题 #20** (第 1045 行, 语言: sql)

- **错误**: 可能的语法问题: -- MYSQL服务器配置（MY.CNF）
[MYSQLD]

# 必需：开启BINLOG

SERVE...

**问题 #21** (第 1080 行, 语言: sql)

- **错误**: 可能的语法问题: -- POSTGRESQL.CONF
WAL_LEVEL = LOGICAL
MAX_REPLICA...

**问题 #24** (第 1143 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt7q29uexTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpt7q29
- **错误行**: 3

**问题 #25** (第 1171 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn_92tfhoTempValidation.java:4: 错误: 找不到符号
MySqlSource<String> source = MySqlSource.<String>builder()
^
  符号:   类 MySqlSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\cloudevents-integration-guide.md`

**问题 #7** (第 479 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc_zyb473SchemaRoutingFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<CloudEvent> events = env
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Local\
- **错误行**: 2

**问题 #9** (第 575 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmwxt2zr4TempValidation.java:3: 错误: 找不到符号
        LOG.info("Processing event",
        ^
  符号:   变量 LOG
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #10** (第 585 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7wnk5596TempValidation.java:3: 错误: 找不到符号
        meterRegistry.counter("events.processed",
        ^
  符号:   变量 meterRegistry
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 3

**问题 #15** (第 896 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk1xasup6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpk1xasup6Temp
- **错误行**: 3

**问题 #20** (第 1427 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4zs4ct1uAzureEventGridIntegration.java:3: 错误: 需要';'
import com.azure.core.models.CloudEvent as AzureCloudEvent;
                                       ^
1 个错误

- **错误行**: 3

**问题 #29** (第 2432 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5stzjo49TempValidation.java:4: 错误: 找不到符号
if (aggregate.getVersion() % SNAPSHOT_INTERVAL == 0) {
    ^
  符号:   变量 aggregate
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #31** (第 2485 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwipai9u_TempValidation.java:5: 错误: 找不到符号
  ctx.timestamp() + sagaDefinition.getTimeoutMs()
  ^
  符号:   变量 ctx
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 5

**问题 #32** (第 2512 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5lz4ojpjTempValidation.java:4: 错误: 找不到符号
props.setProperty("batch.size", "16384");
^
  符号:   变量 props
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp5
- **错误行**: 4

**问题 #33** (第 2527 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_313ehryTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp_313ehr
- **错误行**: 3


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\diskless-kafka-deep-dive.md`

**问题 #2** (第 106 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjnijp045TempValidation.java:4: 错误: 找不到符号
KafkaSource<String> source = KafkaSource.<String>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #3** (第 135 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqx9djq84TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #5** (第 233 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpblvnei35TempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\elasticsearch-connector-complete-guide.md`

**问题 #13** (第 172 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpklkapaxoTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpklkapaxoTempValidat
- **错误行**: 4

**问题 #14** (第 189 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuk1fhi2aTempValidation.java:4: 错误: 程序包ElasticsearchSink不存在
ElasticsearchSink.Builder<LogEvent> builder = new ElasticsearchSink.Builder<>(
                 ^
C:\Use
- **错误行**: 4

**问题 #16** (第 231 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsu2s9kpmTempValidation.java:4: 错误: 找不到符号
builder.setFlushOnCheckpoint(true);
^
  符号:   变量 builder
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #20** (第 375 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm15n_sh_TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.http.auth.AuthScope;
^
C:\Users\luyan\AppData\Local\Temp\tmpm15n_sh_TempValidation.java:3: 错误: 不是语句
i
- **错误行**: 3


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\evolution\cdc-connector.md`

**问题 #1** (第 58 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1ne3now1TempValidation.java:3: 错误: 找不到符号
        MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
        ^
  符号:   类 MySqlSource
  位置: 类 TempValida
- **错误行**: 3

**问题 #2** (第 74 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqyq1c74nTempValidation.java:3: 错误: 找不到符号
stream.process(new ProcessFunction<String, Row>() {
                   ^
  符号:   类 ProcessFunction
  位置: 类 TempValidation

- **错误行**: 3


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\evolution\cloud-connector.md`

**问题 #1** (第 56 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp95fd5409TempValidation.java:3: 错误: 找不到符号
        env.getConfig().setDefaultFileSystemScheme("s3://");
        ^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 3

**问题 #2** (第 68 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo26znfe4TempValidation.java:3: 错误: 找不到符号
        FlinkKinesisConsumer<String> consumer = new FlinkKinesisConsumer<>(
        ^
  符号:   类 FlinkKinesisConsumer
  位置:
- **错误行**: 3


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\evolution\file-connector.md`

**问题 #1** (第 57 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjugcx0pvTempValidation.java:3: 错误: 找不到符号
        FileSource<String> source = FileSource
        ^
  符号:   类 FileSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3

**问题 #2** (第 70 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk2qp7q3hTempValidation.java:3: 错误: 找不到符号
        FileSink<GenericRecord> sink = FileSink
        ^
  符号:   类 FileSink
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 3


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\evolution\jdbc-connector.md`

**问题 #1** (第 56 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9230uxfgTempValidation.java:3: 错误: 找不到符号
        JdbcSourceBuilder<Row> builder = JdbcSourceBuilder.<Row>builder()
        ^
  符号:   类 JdbcSourceBuilder
  位置: 类 Te
- **错误行**: 3

**问题 #2** (第 68 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1jn6rarlTempValidation.java:3: 错误: 找不到符号
JdbcSink.sink(
^
  符号:   变量 JdbcSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp1jn6rarlTempValidation.ja
- **错误行**: 3


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\evolution\kafka-connector.md`

**问题 #1** (第 55 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgp7lru67TempValidation.java:3: 错误: 找不到符号
        KafkaSource<String> source = KafkaSource.<String>builder()
        ^
  符号:   类 KafkaSource
  位置: 类 TempValidation

- **错误行**: 3

**问题 #2** (第 69 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw0j405loTempValidation.java:3: 错误: 找不到符号
        KafkaSink<String> sink = KafkaSink.<String>builder()
        ^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users
- **错误行**: 3


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\evolution\lakehouse-connector.md`

**问题 #1** (第 60 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwhq8p99sTempValidation.java:5: 错误: 找不到符号
    .withOverwritePartition(partition)
                            ^
  符号:   变量 partition
  位置: 类 TempValidation
C:\Users\
- **错误行**: 5


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\evolution\mq-connector.md`

**问题 #1** (第 57 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp92fbyr1lTempValidation.java:3: 错误: 找不到符号
        PulsarSource<String> source = PulsarSource.builder()
        ^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Us
- **错误行**: 3

**问题 #2** (第 72 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmthtkyl7TempValidation.java:3: 错误: 找不到符号
        RMQSink<String> sink = new RMQSink<>(
        ^
  符号:   类 RMQSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 3


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\evolution\nosql-connector.md`

**问题 #1** (第 58 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7264zib3TempValidation.java:3: 错误: 找不到符号
        HBaseSinkFunction<Row> sink = new HBaseSinkFunction<>(
        ^
  符号:   类 HBaseSinkFunction
  位置: 类 TempValidatio
- **错误行**: 3

**问题 #2** (第 71 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw7d5w8faTempValidation.java:3: 错误: 找不到符号
        MongoDBSource<String> source = MongoDBSource.<String>builder()
        ^
  符号:   类 MongoDBSource
  位置: 类 TempValid
- **错误行**: 3


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\flink-24-connectors-guide.md`

**问题 #3** (第 152 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnbvk8tqdTempValidation.java:3: 错误: 不是语句
        Kafka3Source<T> = ⟨BootstrapServers, TopicPattern, ConsumerProtocol,
                    ^
C:\Users\luyan\AppData\L
- **错误行**: 3

**问题 #13** (第 462 行, 语言: sql)

- **错误**: 可能的语法问题: -- 传统方式 (显式指定 JAR)
SET 'PIPELINE.JARS' = 'FILE:///...

**问题 #29** (第 1131 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqcym450nTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqcy
- **错误行**: 3

**问题 #30** (第 1158 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfne_2i9xTempValidation.java:4: 错误: 找不到符号
KafkaSink<String> sink = KafkaSink.<String>builder()
^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #35** (第 1324 行, 语言: sql)

- **错误**: 可能的语法问题: -- ICEBERG V2 流式增量读取
SET 'EXECUTION.RUNTIME-MODE' ...

**问题 #36** (第 1343 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG FLUSS_CATALOG;...

**问题 #39** (第 1487 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg72rdaw2TempValidation.java:4: 错误: 找不到符号
TableResult result = tableEnv.executeSql(""
^
  符号:   类 TableResult
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #40** (第 1507 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprp0mkc75TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmprp0
- **错误行**: 3

**问题 #43** (第 1599 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 66, column 13:
          filter: id > 0
                ^ (line: 66)
- **错误行**: 66
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\flink-cdc-3.6.0-guide.md`

**问题 #10** (第 412 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    transform:
    ^ (line: 2)
found duplicate key "transform" with value "[]" (original value: "[]")
  in "<unicode string>", l
- **错误行**: 2


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\flink-connectors-ecosystem-complete-guide.md`

**问题 #3** (第 154 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdiizqwrdSource.java:2: 错误: 找不到符号
    extends SourceReaderFactory<T, SplitT> {
            ^
  符号: 类 SourceReaderFactory
C:\Users\luyan\AppData\Local\Temp\tmpdiizqw
- **错误行**: 2

**问题 #4** (第 190 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxrfarrbhSink.java:3: 错误: 找不到符号
    SinkWriter<InputT> createWriter(InitContext context);
                                    ^
  符号:   类 InitContext
  位置: 接口 Sink<
- **错误行**: 3

**问题 #22** (第 801 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1ofzuwozTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1of
- **错误行**: 3

**问题 #23** (第 825 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeo6mj5btTempValidation.java:4: 错误: 找不到符号
KafkaSink<String> sink = KafkaSink.<String>builder()
^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #25** (第 870 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg318otiiTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpg31
- **错误行**: 3

**问题 #26** (第 895 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpck72a5ujTempValidation.java:4: 错误: 找不到符号
PulsarSink<String> sink = PulsarSink.builder()
^
  符号:   类 PulsarSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #28** (第 925 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0nw75x4xTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp0nw
- **错误行**: 3

**问题 #30** (第 974 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpts6kr6rvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpts6
- **错误行**: 3

**问题 #31** (第 1000 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqr8wh8zvTempValidation.java:4: 错误: 找不到符号
Properties producerConfig = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #33** (第 1037 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy5vs80ztTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpy5v
- **错误行**: 3

**问题 #35** (第 1080 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppg8_ca11TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmppg8
- **错误行**: 3

**问题 #36** (第 1133 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi1es23xaTempValidation.java:4: 错误: 找不到符号
FileSystem fs = FileSystem.get(new URI("s3://my-bucket/data"));
^
  符号:   类 FileSystem
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #37** (第 1153 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_l2lri7iTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp_l2
- **错误行**: 3

**问题 #38** (第 1172 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpja25wd2sTempValidation.java:4: 错误: 找不到符号
Schema schema = new Schema.Parser().parse(
^
  符号:   类 Schema
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #39** (第 1190 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphw9adjhjTempValidation.java:4: 错误: 找不到符号
final StreamingFileSink<Row> sink = StreamingFileSink
      ^
  符号:   类 StreamingFileSink
  位置: 类 TempValidation
C:\Users\
- **错误行**: 4

**问题 #40** (第 1211 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5ptgsog9TempValidation.java:4: 错误: 找不到符号
FileSink<Row> sink = FileSink.forBulkFormat(
^
  符号:   类 FileSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #42** (第 1255 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi9akb2esTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpi9a
- **错误行**: 3

**问题 #43** (第 1279 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmwdmvj4gTempValidation.java:4: 错误: 找不到符号
JdbcExactlyOnceSink<Row> sink = JdbcExactlyOnceSink.sink(
^
  符号:   类 JdbcExactlyOnceSink
  位置: 类 TempValidation
C:\Users\
- **错误行**: 4

**问题 #46** (第 1357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwhaani_6TempValidation.java:4: 错误: 找不到符号
ClusterBuilder clusterBuilder = new ClusterBuilder() {
^
  符号:   类 ClusterBuilder
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #48** (第 1397 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfro_vak4TempValidation.java:4: 错误: 找不到符号
HBaseSourceFunction<Row> source = new HBaseSourceFunction<>(
^
  符号:   类 HBaseSourceFunction
  位置: 类 TempValidation
C:\Use
- **错误行**: 4

**问题 #50** (第 1439 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz917k5awTempValidation.java:4: 错误: 找不到符号
List<HttpHost> httpHosts = Arrays.asList(
^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpz91
- **错误行**: 4

**问题 #52** (第 1482 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4tm4ch5pTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp4tm
- **错误行**: 3

**问题 #54** (第 1530 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp7ayvf_0TempValidation.java:4: 错误: 找不到符号
FlinkJedisPoolConfig conf = new FlinkJedisPoolConfig.Builder()
^
  符号:   类 FlinkJedisPoolConfig
  位置: 类 TempValidation
C:\
- **错误行**: 4

**问题 #56** (第 1582 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp58kt5irqTempValidation.java:4: 错误: 找不到符号
InfluxDBSink<String> sink = InfluxDBSink.builder()
^
  符号:   类 InfluxDBSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 4

**问题 #58** (第 1622 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7yb2rfozTempValidation.java:4: 错误: 找不到符号
CatalogLoader catalogLoader = CatalogLoader.hive(
^
  符号:   类 CatalogLoader
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 4

**问题 #59** (第 1639 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG ICEBERG_CATALOG;...

**问题 #60** (第 1675 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpik16coy4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpik1
- **错误行**: 3

**问题 #64** (第 1752 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_CATALOG;...

**问题 #66** (第 1798 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphu51a7_iTempValidation.java:4: 错误: 找不到符号
DeltaSink<Row> deltaSink = DeltaSink
^
  符号:   类 DeltaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmphu5
- **错误行**: 4

**问题 #68** (第 1828 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG FLUSS_CATALOG;...

**问题 #70** (第 1868 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj6uvesdhTempValidation.java:4: 错误: 找不到符号
MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
^
  符号:   类 MySqlSource
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #79** (第 2329 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuep2r0hxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpuep2r0h
- **错误行**: 3

**问题 #80** (第 2348 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8gy3y68gTempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\flink-delta-lake-integration.md`

**问题 #11** (第 414 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvklsscw6TempValidation.java:4: 错误: 非法的表达式开始
public void notifyCheckpointComplete(long checkpointId) {
^
C:\Users\luyan\AppData\Local\Temp\tmpvklsscw6TempValidation
- **错误行**: 4

**问题 #16** (第 514 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpndqu7n2uTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpndq
- **错误行**: 3

**问题 #17** (第 534 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd9xvwqerTempValidation.java:3: 错误: 找不到符号
        DeltaSource<RowData> streamingSource = DeltaSource
        ^
  符号:   类 DeltaSource
  位置: 类 TempValidation
C:\Users
- **错误行**: 3

**问题 #18** (第 550 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8tpnbx_zTempValidation.java:3: 错误: 找不到符号
        DeltaSink<RowData> deltaSink = DeltaSink
        ^
  符号:   类 DeltaSink
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3

**问题 #19** (第 566 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1dt8tab4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1dt8tab
- **错误行**: 3

**问题 #21** (第 633 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5ye2qww0TempValidation.java:3: 错误: 找不到符号
        PostgresSource<String> pgSource = PostgresSource.<String>builder()
        ^
  符号:   类 PostgresSource
  位置: 类 Temp
- **错误行**: 3

**问题 #23** (第 672 行, 语言: sql)

- **错误**: 可能的语法问题: -- 流式查询
SET 'EXECUTION.RUNTIME-MODE' = 'STREAMING'...; 可能的语法问题: -- 批处理查询
SET 'EXECUTION.RUNTIME-MODE' = 'BATCH';...

**问题 #32** (第 831 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp934cyku6TempValidation.java:3: 错误: 找不到符号
        conf.set("delta.logRetentionDuration", "interval 30 days");
        ^
  符号:   变量 conf
  位置: 类 TempValidation
C:\Us
- **错误行**: 3


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\flink-elasticsearch-connector-guide.md`

**问题 #12** (第 322 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgac49yu1TempValidation.java:5: 错误: 不是语句
  "mappings": {
  ^
C:\Users\luyan\AppData\Local\Temp\tmpgac49yu1TempValidation.java:5: 错误: 需要';'
  "mappings": {

- **错误行**: 5

**问题 #17** (第 555 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpboizniftTempValidation.java:40: 错误: 找不到符号
tableEnv.executeSql(createTableSQL);
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpbo
- **错误行**: 40

**问题 #19** (第 686 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe_kedv5qTempValidation.java:4: 错误: 程序包ElasticsearchSink不存在
ElasticsearchSink.Builder<Event> builder =
                 ^
C:\Users\luyan\AppData\Local\Temp\tmpe_ked
- **错误行**: 4

**问题 #24** (第 869 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp47zmpuofTempValidation.java:4: 错误: 找不到符号
builder.setBulkFlushMaxActions(500);   // 从 1000 降低
^
  符号:   变量 builder
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #26** (第 903 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplkrufpzuTempValidation.java:4: 错误: 找不到符号
String docId = event.getOrderId() + "_" + event.getTimestamp();
               ^
  符号:   变量 event
  位置: 类 TempValidation
C
- **错误行**: 4

**问题 #30** (第 975 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqrkel8tjTempValidation.java:4: 错误: 非法的表达式开始
public String sanitizeJson(Event event) {
^
C:\Users\luyan\AppData\Local\Temp\tmpqrkel8tjTempValidation.java:22: 错误: 需要
- **错误行**: 4

**问题 #32** (第 1056 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptmgs3cvyTempValidation.java:4: 错误: 找不到符号
env.getConfig().enableObjectReuse();
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmptmgs3cvy
- **错误行**: 4


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\flink-iceberg-integration.md`

**问题 #27** (第 975 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG ICEBERG_CATALOG;...; 可能的语法问题: USE ECOMMERCE;...

**问题 #29** (第 1064 行, 语言: sql)

- **错误**: 可能的语法问题: -- 启用 UPSERT 模式写入 ICEBERG
SET 'EXECUTION.CHECKPOIN...

**问题 #30** (第 1101 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...

**问题 #35** (第 1488 行, 语言: sql)

- **错误**: 可能的语法问题: -- 注意：分区演进是增量式的，历史数据保持原分区，新数据使用新分区策略...

**问题 #37** (第 1560 行, 语言: sql)

- **错误**: 可能的语法问题: -- 强制 COMPACTION（合并 DELETE 文件）
CALL ICEBERG_CATALO...

**问题 #43** (第 1812 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc58ghyenTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpc58ghye
- **错误行**: 3

**问题 #45** (第 1862 行, 语言: sql)

- **错误**: 可能的语法问题: -- 重写数据文件（合并小文件）
CALL ICEBERG_CATALOG.SYSTEM.REWRI...; 可能的语法问题: -- 按分区压缩
CALL ICEBERG_CATALOG.SYSTEM.REWRITE_DATA_...

**问题 #47** (第 1922 行, 语言: sql)

- **错误**: 可能的语法问题: -- 手动触发过期
CALL ICEBERG_CATALOG.SYSTEM.EXPIRE_SNAPS...


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\flink-jdbc-connector-guide.md`

**问题 #14** (第 390 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxt0q75nyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.connector.jdbc.*;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpxt0q75nyTempValidation
- **错误行**: 3

**问题 #15** (第 435 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgj7x_y8pTempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql("""
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpgj7x_y8pTempVali
- **错误行**: 4

**问题 #17** (第 539 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_d2gx6ybTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp_d2gx6y
- **错误行**: 3

**问题 #22** (第 689 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwuw60kd6TempValidation.java:4: 错误: 找不到符号
config.setMaximumPoolSize(sinkParallelism + 5);
                          ^
  符号:   变量 sinkParallelism
  位置: 类 TempValidat
- **错误行**: 4

**问题 #24** (第 717 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6sve8r97TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp6sv
- **错误行**: 3

**问题 #26** (第 758 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa0y8lwjnTempValidation.java:8: 错误: 需要';'
SET GLOBAL innodb_rollback_on_timeout = ON;
          ^
C:\Users\luyan\AppData\Local\Temp\tmpa0y8lwjnTempValidation.java:9
- **错误行**: 8

**问题 #29** (第 808 行, 语言: sql)

- **错误**: 可能的语法问题: -- MYSQL: 查看当前连接
SHOW PROCESSLIST;...; 可能的语法问题: -- 查看 XA 事务
XA RECOVER;...

**问题 #30** (第 844 行, 语言: sql)

- **错误**: 可能的语法问题: -- 启用二进制日志（CDC 必需）
SET GLOBAL BINLOG_FORMAT = 'ROW...; 可能的语法问题: -- 优化 INNODB
SET GLOBAL INNODB_BUFFER_POOL_SIZE = ...

**问题 #31** (第 857 行, 语言: sql)

- **错误**: 可能的语法问题: -- 优化写入性能
SET SYNCHRONOUS_COMMIT = OFF;...; 可能的语法问题: --  PREPARED TRANSACTIONS FOR XA
SET MAX_PREPARED_...


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\flink-mongodb-connector-guide.md`

**问题 #15** (第 357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps4dtfprnTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmps4d
- **错误行**: 3

**问题 #17** (第 406 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp064ujkxxTempValidation.java:4: 错误: 找不到符号
ReplaceOneModel<Document> replace = new ReplaceOneModel<>(
^
  符号:   类 ReplaceOneModel
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #25** (第 689 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9j3fsbx7TempValidation.java:5: 错误: 找不到符号
tableEnv.executeSql("""
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp9j3fsbx7TempVali
- **错误行**: 5

**问题 #33** (第 983 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5y630wkhTempValidation.java:4: 错误: 找不到符号
ReplaceOneModel<Document> replace = new ReplaceOneModel<>(
^
  符号:   类 ReplaceOneModel
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #35** (第 1020 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg8n574wcTempValidation.java:4: 错误: 找不到符号
MongoClientSettings settings = MongoClientSettings.builder()
^
  符号:   类 MongoClientSettings
  位置: 类 TempValidation
C:\Use
- **错误行**: 4

**问题 #37** (第 1057 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxwceyqt2MyClassCodec.java:23: 错误: 未命名类 是预览功能，默认情况下禁用。
CodecRegistry customCodecRegistry = CodecRegistries.fromCodecs(
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 23

**问题 #39** (第 1136 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx_e_9mj5TempValidation.java:4: 错误: 找不到符号
FindIterable<Document> iterable = collection
^
  符号:   类 FindIterable
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #40** (第 1158 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmlyqcfpuTempValidation.java:4: 错误: 找不到符号
BulkWriteOptions options = new BulkWriteOptions()
^
  符号:   类 BulkWriteOptions
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #41** (第 1184 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9wn6oen8TempValidation.java:4: 错误: 找不到符号
MongoChangeStreamSource<ChangeEvent> source =
^
  符号:   类 MongoChangeStreamSource
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\flink-paimon-integration.md`

**问题 #13** (第 778 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_PROD;...

**问题 #14** (第 819 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...; 可能的语法问题: -- 模式2: 从最早快照开始消费
SET 'SCAN.MODE' = 'EARLIEST';...

**问题 #18** (第 1051 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...

**问题 #20** (第 1129 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看所有 TAG
SHOW TAGS FOR TABLE PAIMON_USERS;...


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\jdbc-connector-complete-guide.md`

**问题 #10** (第 393 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi84pwxj6TempValidation.java:4: 错误: 非法的表达式开始
.setProperty("useSSL", "false")
^
C:\Users\luyan\AppData\Local\Temp\tmpi84pwxj6TempValidation.java:14: 错误: 需要';'
.setPr
- **错误行**: 4

**问题 #17** (第 663 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw6bpywapTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.connector.jdbc.source.JdbcSource;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpw6bpyw
- **错误行**: 3

**问题 #18** (第 698 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfmlb7029TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.source.JdbcSource;
^
C:\Users\luyan\AppData\Local\Temp\tmpfmlb7029TempValidation
- **错误行**: 3

**问题 #19** (第 740 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp00p9niy0TempValidation.java:4: 错误: 找不到符号
JdbcSource<MyRecord> incrementalSource = JdbcSource.<MyRecord>builder()
^
  符号:   类 JdbcSource
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #20** (第 764 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx5eqvpfcTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcSink;
^
C:\Users\luyan\AppData\Local\Temp\tmpx5eqvpfcTempValidation.java:3:
- **错误行**: 3

**问题 #21** (第 799 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg34sbk68TempValidation.java:29: 错误: 非法的表达式开始
);
^
1 个错误

- **错误行**: 29

**问题 #22** (第 831 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp08ejqztbTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcExactlyOnceOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmp08ejqztbTempValid
- **错误行**: 3

**问题 #23** (第 870 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcpq4h17jTempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpcp
- **错误行**: 4

**问题 #24** (第 892 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpev729eb2TempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpev
- **错误行**: 4

**问题 #25** (第 911 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5s9um1_0TempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp5s
- **错误行**: 4

**问题 #26** (第 931 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_9zrscj9TempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp_9
- **错误行**: 4

**问题 #27** (第 966 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdtmkt20eTempValidation.java:4: 错误: 找不到符号
JdbcExecutionOptions executionOptions = JdbcExecutionOptions.builder()
^
  符号:   类 JdbcExecutionOptions
  位置: 类 TempValida
- **错误行**: 4

**问题 #29** (第 1026 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt3xajuffTempValidation.java:10: 错误: 已在方法 main(String[])中定义了变量 url
String url = "jdbc:postgresql://localhost:5432/mydb" +
       ^
1 个错误

- **错误行**: 10

**问题 #30** (第 1056 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpngwjws0bTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcExecutionOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmpngwjws0bTempValidat
- **错误行**: 3

**问题 #31** (第 1104 行, 语言: sql)

- **错误**: 可能的语法问题: -- MYSQL: 查看当前连接
SHOW PROCESSLIST;...

**问题 #32** (第 1118 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkdnv3zo2TempValidation.java:4: 错误: 找不到符号
HikariConfig config = new HikariConfig();
^
  符号:   类 HikariConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #33** (第 1149 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptkku5td3TempValidation.java:9: 错误: 找不到符号
JdbcSource<MyRecord> source = JdbcSource.<MyRecord>builder()
^
  符号:   类 JdbcSource
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 9

**问题 #34** (第 1186 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmparbfilweTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000);  // 1分钟，不要太短
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\kafka-integration-patterns.md`

**问题 #1** (第 300 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgmx5z7k5TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #2** (第 328 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcbdj_80lTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.connector.base.DeliveryGuarantee;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpcbdj_8
- **错误行**: 3

**问题 #3** (第 350 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsu4jjmh0TempValidation.java:4: 错误: 找不到符号
KafkaSource<UserEvent> source = KafkaSource.<UserEvent>builder()
^
  符号:   类 KafkaSource
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 4

**问题 #10** (第 721 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqoibckc6TempValidation.java:4: 错误: 找不到符号
properties.setProperty(
^
  符号:   变量 properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpqoibckc6TempVa
- **错误行**: 4


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\mongodb-connector-complete-guide.md`

**问题 #12** (第 723 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeafk6mjkTempValidation.java:4: 错误: 找不到符号
MongoSink<Document> updateSink = MongoSink.<Document>builder()
^
  符号:   类 MongoSink
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4


### `release\v3.0.0\docs\Flink\05-ecosystem\05.01-connectors\pulsar-integration-guide.md`

**问题 #3** (第 236 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz0gkkl6uTempValidation.java:4: 错误: 找不到符号
PulsarSource<String> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #4** (第 254 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc141xqeaTempValidation.java:4: 错误: 找不到符号
PulsarSink<String> sink = PulsarSink.builder()
^
  符号:   类 PulsarSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #9** (第 397 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe13w46cjEnrichedStreamProcessing.java:18: 错误: 非法的表达式开始
            .setDeserializationSchema(...)
                                      ^
C:\Users\luyan\AppData\Lo
- **错误行**: 18

**问题 #10** (第 433 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoe1_0l4lTempValidation.java:4: 错误: 找不到符号
PulsarSource<String> optimizedSource = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 4

**问题 #11** (第 471 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe7dpp6zqSchemaEvolutionExample.java:24: 错误: 非法的表达式开始
        DataStream<EventV2> stream = env.fromSource(source, ...)

- **错误行**: 24


### `release\v3.0.0\docs\Flink\05-ecosystem\05.02-lakehouse\flink-iceberg-integration.md`

**问题 #29** (第 950 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG ICEBERG_CATALOG;...; 可能的语法问题: USE ECOMMERCE;...

**问题 #30** (第 1001 行, 语言: sql)

- **错误**: 可能的语法问题: -- 使用 UPSERT 模式处理 CDC 变更
SET 'EXECUTION.CHECKPOINT...

**问题 #31** (第 1062 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...

**问题 #36** (第 1476 行, 语言: sql)

- **错误**: 可能的语法问题: -- 在分支上写入数据（不影响主线）
SET 'ICEBERG.CATALOG.DEFAULT-BR...

**问题 #38** (第 1545 行, 语言: sql)

- **错误**: 可能的语法问题: -- 注意：分区演进是增量式的，历史数据保持原分区，新数据使用新分区策略...

**问题 #39** (第 1574 行, 语言: sql)

- **错误**: 可能的语法问题: -- 强制 COMPACTION（合并 DELETE 文件）
CALL ICEBERG_CATALO...

**问题 #46** (第 1875 行, 语言: sql)

- **错误**: 可能的语法问题: -- 阶段 4: 数据一致性验证
-- 对比 HIVE 和 ICEBERG 表的记录数、SUM(AM...


### `release\v3.0.0\docs\Flink\05-ecosystem\05.02-lakehouse\flink-paimon-integration.md`

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

**问题 #31** (第 1560 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...


### `release\v3.0.0\docs\Flink\05-ecosystem\05.02-lakehouse\streaming-lakehouse-architecture.md`

**问题 #25** (第 879 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG ICEBERG_CATALOG;...; 可能的语法问题: USE REALTIME_DW;...; 可能的语法问题: -- ============================================
--...

**问题 #26** (第 1040 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_CATALOG;...


### `release\v3.0.0\docs\Flink\05-ecosystem\05.02-lakehouse\streaming-lakehouse-deep-dive-2026.md`

**问题 #35** (第 1173 行, 语言: sql)

- **错误**: 可能的语法问题: USE CATALOG PAIMON_PROD;...; 可能的语法问题: USE ECOMMERCE;...; 可能的语法问题: -- ============================================
--...

**问题 #36** (第 1445 行, 语言: yaml)

- **错误**: while scanning a simple key
  in "<unicode string>", line 59, column 1:
    spark.sql.catalog.polaris=org.ap ...
    ^ (line: 59)
could not find expected ':'
  in "<unicode string>", line 60, column
- **错误行**: 59


### `release\v3.0.0\docs\Flink\05-ecosystem\05.03-wasm-udf\wasi-0.3-async-preview.md`

**问题 #26** (第 1197 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsrjvli_9TempValidation.java:5: 错误: 需要';'
public void testCancellation() throws Exception {
                            ^
C:\Users\luyan\AppData\Local\Temp\tmpsrjvl
- **错误行**: 5


### `release\v3.0.0\docs\Flink\05-ecosystem\05.04-graph\flink-gelly-streaming-graph-processing.md`

**问题 #3** (第 262 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi7qzg8o2TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpi7qzg8o2TempValidat
- **错误行**: 4

**问题 #4** (第 306 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxg78ynbqTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpxg7
- **错误行**: 3

**问题 #5** (第 345 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr2oy2nywVertexState.java:14: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Edge<Long, Double>> edgeStream = ...;
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Lo
- **错误行**: 14

**问题 #6** (第 436 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmui6rxgcTempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend rocksDbBackend = new RocksDBStateBackend(
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempValidation
C:\Us
- **错误行**: 4


### `release\v3.0.0\docs\Flink\05-ecosystem\05.04-graph\flink-gelly.md`

**问题 #3** (第 166 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfqzl6bauTempValidation.java:4: 错误: 找不到符号
Graph<Long, Double, Double> bipartiteGraph = Graph.fromDataSet(
^
  符号:   类 Graph
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #4** (第 197 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxejmxdjeTempValidation.java:4: 错误: 非法的表达式开始
Graph<String, AccountInfo, Transaction> transactionGraph = ...;

- **错误行**: 4

**问题 #5** (第 218 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp4_bk6yyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpp4_
- **错误行**: 3


### `release\v3.0.0\docs\Flink\05-ecosystem\ecosystem\kafka-streams-migration.md`

**问题 #2** (第 69 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn3inobh7TempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #3** (第 76 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiqz8so_0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #4** (第 101 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps3_ge9i0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmps3_ge9i0Temp
- **错误行**: 3

**问题 #5** (第 126 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpep0krypwTempValidation.java:3: 错误: 找不到符号
        KStream<String, Integer> transformed = stream
        ^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3

**问题 #6** (第 136 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8az9w40wTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8az
- **错误行**: 3

**问题 #7** (第 149 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpijph7eunTempValidation.java:3: 错误: 找不到符号
        Table transformed = tableEnv.from("input_table")
        ^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 3

**问题 #8** (第 165 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptyh_k_hcTempValidation.java:3: 错误: 找不到符号
        KTable<String, Long> counts = stream
        ^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 3

**问题 #9** (第 173 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpid5pb8c_TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpid5pb8c_TempValidat
- **错误行**: 4

**问题 #10** (第 214 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9nsprmopTempValidation.java:3: 错误: 找不到符号
        KStream<String, String> joined = stream1.join(
        ^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 3

**问题 #11** (第 225 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpilj7b2lpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpilj
- **错误行**: 3

**问题 #12** (第 240 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0o725yu1TempValidation.java:3: 错误: 找不到符号
        Table joined = table1
        ^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp0o725y
- **错误行**: 3

**问题 #16** (第 328 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8i7epw6dTempValidation.java:3: 错误: 找不到符号
        properties.put(StreamsConfig.NUM_STREAM_THREADS_CONFIG, 4);
                       ^
  符号:   变量 StreamsConfig
  位置
- **错误行**: 3

**问题 #17** (第 334 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz7jdlmcnTempValidation.java:6: 错误: 非法的表达式开始
stream.map(...).setParallelism(2);
           ^
1 个错误

- **错误行**: 6

**问题 #18** (第 345 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx0gveuq2TempValidation.java:3: 错误: 找不到符号
        properties.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG,
                       ^
  符号:   变量 StreamsConfig
  位置:
- **错误行**: 3

**问题 #19** (第 353 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9zfcf_iuTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9zfcf_i
- **错误行**: 3

**问题 #20** (第 375 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprm_ak1qzTempValidation.java:4: 错误: 需要';'
public void testTopology() {
                        ^
C:\Users\luyan\AppData\Local\Temp\tmprm_ak1qzTempValidation.java:8:
- **错误行**: 4

**问题 #21** (第 393 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjuo5de_dTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpju
- **错误行**: 4

**问题 #22** (第 420 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp196vi9t4TempValidation.java:4: 错误: 需要';'
public void testMigrationParity() {
                               ^
1 个错误

- **错误行**: 4


### `release\v3.0.0\docs\Flink\05-ecosystem\ecosystem\materialize-comparison.md`

**问题 #4** (第 110 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi8qpsxftTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpi8q
- **错误行**: 3

**问题 #5** (第 129 行, 语言: sql)

- **错误**: 可能的语法问题: -- AUTOMATIC MAINTENANCE, AUTOMATIC INDEXING...

**问题 #10** (第 314 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1hwwap1cTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1hw
- **错误行**: 3


### `release\v3.0.0\docs\Flink\05-ecosystem\ecosystem\pulsar-functions-integration.md`

**问题 #2** (第 73 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpohpvxhjyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpohp
- **错误行**: 3

**问题 #3** (第 100 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2l3ebcn6TempValidation.java:3: 错误: 找不到符号
        PulsarSink<String> sink = PulsarSink.builder()
        ^
  符号:   类 PulsarSink
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 3

**问题 #9** (第 236 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbzfn13axTempValidation.java:4: 错误: 找不到符号
Schema<OrderEvent> schema = Schema.AVRO(OrderEvent.class);
^
  符号:   类 Schema
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #10** (第 247 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbo30xu41TempValidation.java:4: 错误: 找不到符号
PulsarSource<OrderEvent> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #11** (第 264 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptr0bb4wyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmptr0bb4w
- **错误行**: 3

**问题 #12** (第 281 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp54djudz5TempValidation.java:4: 错误: 找不到符号
PulsarSource<String> source = PulsarSource.builder()
^
  符号:   类 PulsarSource
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4


### `release\v3.0.0\docs\Flink\05-ecosystem\ecosystem\risingwave-integration-guide.md`

**问题 #2** (第 80 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjbqueipmTempValidation.java:4: 错误: 找不到符号
JdbcSink.sink(
^
  符号:   变量 JdbcSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpjbqueipmTempValidation.ja
- **错误行**: 4

**问题 #4** (第 124 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_a4h4mx9TempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp_a
- **错误行**: 4

**问题 #8** (第 241 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0rz3r7l_TempValidation.java:4: 错误: 找不到符号
TwoPhaseCommitSinkFunction<Event, JdbcConnection, Void> exactlyOnceSink =
^
  符号:   类 TwoPhaseCommitSinkFunction
  位置: 类 T
- **错误行**: 4

**问题 #9** (第 278 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1g3pdwprTempValidation.java:4: 错误: 找不到符号
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


### `release\v3.0.0\docs\Flink\06-ai-ml\ai-agent-flink-deep-integration.md`

**问题 #7** (第 390 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp09qywcdzTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp09qyw
- **错误行**: 3

**问题 #8** (第 409 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5dtxwrahCustomerSupportAgent.java:350: 错误: 非法的表达式开始
            .addSource(new KafkaSource<Query>(...))
                                              ^
C:\Users\lu
- **错误行**: 350

**问题 #9** (第 783 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 212


### `release\v3.0.0\docs\Flink\06-ai-ml\ai-ml\evolution\a2a-protocol.md`

**问题 #1** (第 47 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf2nir4szTempValidation.java:3: 错误: 找不到符号
        A2AMessage msg = A2AMessage.builder()
        ^
  符号:   类 A2AMessage
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 3

**问题 #2** (第 59 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiheg37rfTempValidation.java:3: 错误: 找不到符号
        agent1.delegate(task, agent2);
                        ^
  符号:   变量 task
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 3


### `release\v3.0.0\docs\Flink\06-ai-ml\ai-ml\evolution\ai-agent-24.md`

**问题 #2** (第 48 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprfte_op5TempValidation.java:3: 错误: 找不到符号
        Agent agent = Agent.newBuilder()
        ^
  符号:   类 Agent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 3

**问题 #3** (第 59 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfqwn43_pTempValidation.java:4: 错误: 找不到符号
    .addSink(new ActionSink());
                 ^
  符号:   类 ActionSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4


### `release\v3.0.0\docs\Flink\06-ai-ml\ai-ml\evolution\ai-agent-25.md`

**问题 #1** (第 50 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9ox6pe1_TempValidation.java:3: 错误: 找不到符号
        MultiAgentSystem system = MultiAgentSystem.builder()
        ^
  符号:   类 MultiAgentSystem
  位置: 类 TempValidation
C
- **错误行**: 3

**问题 #2** (第 61 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0p7qzojaTempValidation.java:3: 错误: 找不到符号
system.coordinate(event, (detector, diagnoser) -> {
                  ^
  符号:   变量 event
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 3


### `release\v3.0.0\docs\Flink\06-ai-ml\ai-ml\evolution\ai-agent-30.md`

**问题 #3** (第 61 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqftvpaxcTempValidation.java:4: 错误: 找不到符号
    .toSink(AlertSink.class);
            ^
  符号:   类 AlertSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4


### `release\v3.0.0\docs\Flink\06-ai-ml\ai-ml\evolution\feature-store.md`

**问题 #1** (第 46 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvbo0f2m2TempValidation.java:3: 错误: 找不到符号
        FeatureVector fv = featureStore.getOnlineFeatures(entityId, features);
        ^
  符号:   类 FeatureVector
  位置: 类 T
- **错误行**: 3

**问题 #2** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl6n5ewawTempValidation.java:3: 错误: 找不到符号
stream.map(event -> {
^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpl6n5ewawTempValidati
- **错误行**: 3


### `release\v3.0.0\docs\Flink\06-ai-ml\ai-ml\evolution\llm-integration.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl0jkn1_4TempValidation.java:3: 错误: 找不到符号
llmClient.completeStream(prompt, token -> {
                         ^
  符号:   变量 prompt
  位置: 类 TempValidation
C:\Users\l
- **错误行**: 3

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqekz6tojTempValidation.java:3: 错误: 找不到符号
        stream.map(new LLMMapFunction("gpt-4", promptTemplate));
                       ^
  符号:   类 LLMMapFunction
  位置: 类
- **错误行**: 3


### `release\v3.0.0\docs\Flink\06-ai-ml\ai-ml\evolution\ml-inference.md`

**问题 #1** (第 48 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0m1t2zjrTempValidation.java:3: 错误: 找不到符号
        SavedModelBundle model = SavedModelBundle.load("/path/to/model");
        ^
  符号:   类 SavedModelBundle
  位置: 类 Tem
- **错误行**: 3

**问题 #2** (第 57 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2l9m_p99TempValidation.java:4: 错误: 找不到符号
    .setParallelism(gpuCount);
                    ^
  符号:   变量 gpuCount
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4


### `release\v3.0.0\docs\Flink\06-ai-ml\ai-ml\evolution\model-serving.md`

**问题 #2** (第 45 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn3qljkleTempValidation.java:3: 错误: 找不到符号
        ModelRouter router = new ModelRouter()
        ^
  符号:   类 ModelRouter
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3

**问题 #3** (第 55 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp507_jccmTempValidation.java:3: 错误: 找不到符号
        ModelVersion version = registry.getLatest("fraud-detection");
        ^
  符号:   类 ModelVersion
  位置: 类 TempValidat
- **错误行**: 3


### `release\v3.0.0\docs\Flink\06-ai-ml\ai-ml\evolution\vector-search.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4js1um9yTempValidation.java:3: 错误: 找不到符号
        VectorIndex index = new HNSWIndex.Builder()
        ^
  符号:   类 VectorIndex
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 3

**问题 #2** (第 65 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiyqv88eeTempValidation.java:3: 错误: 找不到符号
        List<Vector> results = index.search(queryVector, 10);
        ^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 3


### `release\v3.0.0\docs\Flink\06-ai-ml\flink-25-gpu-acceleration.md`

**问题 #7** (第 483 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp95oosseeTempValidation.java:5: 错误: 需要';'
public void testGPUSumAccuracy() {
                              ^
1 个错误

- **错误行**: 5

**问题 #15** (第 1044 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 7, column 42:
     ... flink:2.5-gpu-cuda12  <!-- 前瞻性镜像: Flink 2.5规划中 -->
                                         ^ (line: 7)
- **错误行**: 7
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `release\v3.0.0\docs\Flink\06-ai-ml\flink-agent-workflow-engine.md`

**问题 #9** (第 1056 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqbzk3idaWorkflowBuilder.java:67: 错误: 未命名类 是预览功能，默认情况下禁用。
WorkflowDefinition workflow = WorkflowBuilder
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 67

**问题 #12** (第 1418 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9raqlqq8TempValidation.java:4: 错误: 找不到符号
WorkflowDefinition riskWorkflow = WorkflowBuilder
^
  符号:   类 WorkflowDefinition
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4


### `release\v3.0.0\docs\Flink\06-ai-ml\flink-agents-flip-531.md`

**问题 #5** (第 464 行, 语言: sql)

- **错误**: 可能的语法问题: -- DEF-F-12-30: FLINK AGENT DDL 定义

-- 注: 以下为未来可能的...


### `release\v3.0.0\docs\Flink\06-ai-ml\flink-ai-agents-flip-531.md`

**问题 #6** (第 292 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx5de08dxBadAgent.java:1: 错误: 程序包org.apache.flink.api.common.state不存在
import org.apache.flink.api.common.state.ListState;
                                        ^

- **错误行**: 1

**问题 #7** (第 309 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8i6ch5jyTempValidation.java:4: 错误: 找不到符号
String response = llmClient.completeSync(prompt);  // 阻塞！
                                         ^
  符号:   变量 prompt
  位
- **错误行**: 4

**问题 #8** (第 320 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpstijuppcTempValidation.java:5: 错误: 找不到符号
    generateLLMRequest();  // 可能压垮服务！
    ^
  符号:   方法 generateLLMRequest()
  位置: 类 TempValidation
1 个错误

- **错误行**: 5

**问题 #11** (第 514 行, 语言: sql)

- **错误**: 可能的语法问题: -- 创建AGENT
-- 注: 以下为未来可能的语法（概念设计阶段）
<!-- 以下语法为概念设计...; 可能的语法问题: -- 注册SQL工具
-- 注: 以下为未来可能的语法（概念设计阶段）
<!-- 以下语法为概念设计...; 可能的语法问题: -- 注册外部工具
-- 注: 以下为未来可能的语法（概念设计阶段）
~~CREATE TOOL S...; 可能的语法问题:

**问题 #12** (第 582 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl_9flojjTempValidation.java:4: 错误: 找不到符号
Agent salesAgent = Agent.builder()
^
  符号:   类 Agent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpl_9flojjT
- **错误行**: 4


### `release\v3.0.0\docs\Flink\06-ai-ml\flink-ai-ml-integration-complete-guide.md`

**问题 #5** (第 190 行, 语言: sql)
- **错误**: 可能的语法问题: -- DEF-F-12-104A: 相似度函数
COSINE_SIMILARITY(U, V) = ...

**问题 #6** (第 203 行, 语言: sql)
- **错误**: 可能的语法问题: -- 模型定义语法（DEF-F-12-105A）
<!-- 以下语法为概念设计，实际 FLINK 版...

**问题 #10** (第 374 行, 语言: sql)
- **错误**: 可能的语法问题: <!-- 以下语法为概念设计，实际 FLINK 版本尚未支持 -->
-- ~~CREATE AGE...; 可能的语法问题: -- DEF-F-12-110B: CREATE TOOL语法（未来可能的语法，概念设计阶段）
--...; 可能的语法问题: -- DEF-F-12-110C: AGENT工作流语法
<!-- 以下语法为概念设计，实际 FLI...

**问题 #14** (第 688 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpagz2mad1BadAgent.java:1: 错误: 程序包org.apache.flink.api.common.state不存在
import org.apache.flink.api.common.state.ListState;
                                        ^

- **错误行**: 1

**问题 #15** (第 714 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppza4lxu8TempValidation.java:4: 错误: 找不到符号
String response = llmClient.completeSync(prompt);  // 阻塞！吞吐量受限
                                         ^
  符号:   变量 promp
- **错误行**: 4

**问题 #16** (第 725 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmponnfm1_fTempValidation.java:5: 错误: 找不到符号
    generateLLMRequest();  // 可能压垮LLM服务！
    ^
  符号:   方法 generateLLMRequest()
  位置: 类 TempValidation
1 个错误

- **错误行**: 5

**问题 #21** (第 1344 行, 语言: sql)
- **错误**: 可能的语法问题: -- ============================================
--...; 可能的语法问题: -- 步骤2: 创建技术支持AGENT
-- 注: 以下为未来可能的语法（概念设计阶段）
~~CRE...; 可能的语法问题: -- 步骤3: 注册SQL工具 - 查询订单
-- 注: 以下为未来可能的语法（概念设计阶段）
<!...; 可能的语法问题:

**问题 #22** (第 1600 行, 语言: sql)
- **错误**: 可能的语法问题: -- 步骤3: 创建嵌入模型
<!-- 以下语法为概念设计，实际 FLINK 版本尚未支持 -->
...; 可能的语法问题: -- 步骤4: 创建LLM模型
~~CREATE MODEL RAG_GENERATOR~~ (未来...

**问题 #24** (第 2032 行, 语言: sql)

- **错误**: 可能的语法问题: -- 步骤4: 创建不同成本的模型定义
~~CREATE MODEL GPT35_ECONOMY~~...; 可能的语法问题: ~~CREATE MODEL GPT4_STANDARD~~ (未来可能的语法)
WITH (
  ...

**问题 #38** (第 3039 行, 语言: sql)

- **错误**: 可能的语法问题: -- 创建AGENT
-- 注: 以下为未来可能的语法（概念设计阶段）
<!-- 以下语法为概念设计...; 可能的语法问题: -- 创建模型
~~CREATE MODEL <NAME>~~ WITH ('PROVIDER' =...

**问题 #39** (第 3069 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8pnzfzyzTempValidation.java:4: 错误: 找不到符号
Agent agent = Agent.builder()
^
  符号:   类 Agent
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp8pnzfzyzTempVa
- **错误行**: 4


### `release\v3.0.0\docs\Flink\06-ai-ml\flink-llm-integration.md`

**问题 #1** (第 35 行, 语言: sql)
- **错误**: 可能的语法问题: <!-- 以下语法为概念设计，实际 FLINK 版本尚未支持 -->
~~CREATE MODEL~...

**问题 #2** (第 56 行, 语言: sql)

- **错误**: 可能的语法问题: ML_PREDICT(
  MODEL_NAME,           -- 模型名称 (STRIN...

**问题 #6** (第 292 行, 语言: sql)

- **错误**: 可能的语法问题: -- DEF-F-12-41: MODEL DDL 实例

-- OPENAI GPT-4 模型
~...; 可能的语法问题: -- 文本嵌入模型
~~CREATE MODEL TEXT_EMBEDDING_3~~ (未来可能的...; 可能的语法问题: -- 兼容 OLLAMA 本地模型
~~CREATE MODEL LOCAL_LLAMA~~ (未来...

**问题 #9** (第 368 行, 语言: sql)

- **错误**: 可能的语法问题: -- 实时客服消息情感分析
~~CREATE MODEL SENTIMENT_ANALYZER~~ ...

**问题 #12** (第 435 行, 语言: sql)

- **错误**: 可能的语法问题: -- 实时多语言翻译
~~CREATE MODEL TRANSLATOR~~ (未来可能的语法)
W...

**问题 #16** (第 638 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6p2lkpmrBatchLLMCaller.java:15: 错误: 未结束的字符文字
SET 'table.exec.async-lookup.buffer-capacity' = '100';
    ^
C:\Users\luyan\AppData\Local\Temp\tmp6p2lkpmrBatchLLMCall
- **错误行**: 15

**问题 #20** (第 731 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq50fh6b5PIIMaskingFunction.java:15: 错误: 需要 class、interface、enum 或 record
SELECT
^
C:\Users\luyan\AppData\Local\Temp\tmpq50fh6b5PIIMaskingFunction.java:18: 错误: 未结束的
- **错误行**: 15


### `release\v3.0.0\docs\Flink\06-ai-ml\flink-llm-realtime-inference-guide.md`

**问题 #6** (第 238 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaygz49z2TempValidation.java:4: 错误: 找不到符号
String response = llmClient.complete(prompt);  // 阻塞!
                                     ^
  符号:   变量 prompt
  位置: 类 Tem
- **错误行**: 4

**问题 #7** (第 244 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt9vmwgphTempValidation.java:4: 错误: 找不到符号
CompletableFuture<String> future = llmClient.completeAsync(prompt);
^
  符号:   类 CompletableFuture
  位置: 类 TempValidation
C
- **错误行**: 4

**问题 #8** (第 254 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdoh5yeu6TempValidation.java:4: 错误: 非法的表达式开始
public void processElement(Request req) {
^
C:\Users\luyan\AppData\Local\Temp\tmpdoh5yeu6TempValidation.java:9: 错误: 需要
- **错误行**: 4

**问题 #9** (第 261 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_v669s82TempValidation.java:4: 错误: 非法的表达式开始
private ListState<Message> conversationHistory;
^
C:\Users\luyan\AppData\Local\Temp\tmp_v669s82TempValidation.java:16:
- **错误行**: 4

**问题 #10** (第 277 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeh_12z0gTempValidation.java:4: 错误: 找不到符号
String response = llmClient.complete(prompt);
                                     ^
  符号:   变量 prompt
  位置: 类 TempValidat
- **错误行**: 4

**问题 #11** (第 282 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3ijhidk0TempValidation.java:4: 错误: 找不到符号
RetryPolicy<String> retryPolicy = RetryPolicy.<String>builder()
^
  符号:   类 RetryPolicy
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #14** (第 656 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 114

**问题 #20** (第 1128 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 10, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^ (line: 10)
- **错误行**: 10
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `release\v3.0.0\docs\Flink\06-ai-ml\flink-llm-realtime-rag-architecture.md`

**问题 #6** (第 364 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph_lp176qRAGQueryService.java:67: 错误: 非法的表达式开始
            .map(new RichMapFunction<EnrichedQuery, LLMResponse>() {
            ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 67


### `release\v3.0.0\docs\Flink\06-ai-ml\flink-mcp-protocol-integration.md`

**问题 #8** (第 438 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxwo9iu5bTempValidation.java:4: 错误: 不是语句

1. 接收 MCP 调用请求 request = { name, arguments }
^
C:\Users\luyan\AppData\Local\Temp\tmpxwo9iu5bTempValidation.java:4: 错误: 需要';

- **错误行**: 4

**问题 #15** (第 1154 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp53oxvbxfMcpEnrichmentFunction.java:89: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedEvent> enrichedStream = rawStream
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\lu
- **错误行**: 89

**问题 #16** (第 1258 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcfxpojybMcpTableFunction.java:63: 错误: 未命名类 是预览功能，默认情况下禁用。
TableEnvironment tEnv = TableEnvironment.create(...);
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\
- **错误行**: 63

**问题 #27** (第 1818 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprb9foo8zTempValidation.java:4: 错误: 找不到符号
String sql = "SELECT * FROM " + tableName + " WHERE id = " + userInput;
                                ^
  符号:   变量 table
- **错误行**: 4


### `release\v3.0.0\docs\Flink\06-ai-ml\flink-ml-architecture.md`

**问题 #3** (第 228 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprh_2vwuzTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\Flink\06-ai-ml\flink-realtime-ml-inference.md`

**问题 #3** (第 298 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5jqsjno9TempValidation.java:13: 错误: 非法的表达式开始
AsyncDataStream.unorderedWait(...);
                              ^
1 个错误

- **错误行**: 13

**问题 #5** (第 361 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphvvfdrwmDriftDetectionFunction.java:11: 错误: 非法的表达式开始
        currentState.update(...);
                            ^
1 个错误

- **错误行**: 11

**问题 #7** (第 419 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6x0hec6wTFServingAsyncFunction.java:54: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedEvent> scoredEvents = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以
- **错误行**: 54


### `release\v3.0.0\docs\Flink\06-ai-ml\flip-531-ai-agents-ga-guide.md`

**问题 #1** (第 92 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb4ky_5hiTempValidation.java:4: 错误: 找不到符号
EmbeddingConfiguration embedConfig = EmbeddingConfiguration.builder()
^
  符号:   类 EmbeddingConfiguration
  位置: 类 TempValid
- **错误行**: 4

**问题 #4** (第 193 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwypskydjTempValidation.java:4: 错误: 找不到符号
CompletableFuture<ToolResult> future = agent.executeToolAsync(
^
  符号:   类 CompletableFuture
  位置: 类 TempValidation
C:\Use
- **错误行**: 4


### `release\v3.0.0\docs\Flink\06-ai-ml\model-serving-streaming.md`

**问题 #3** (第 259 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppm3fa2q8TFServingAsyncFunction.java:47: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Prediction> predictions = featureStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 47


### `release\v3.0.0\docs\Flink\06-ai-ml\online-learning-algorithms.md`

**问题 #6** (第 495 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiqqi6siiTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.ml.classification.logisticregression;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpiq
- **错误行**: 3

**问题 #15** (第 960 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp27jhb_bjTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmp27jhb_bjTempValidatio
- **错误行**: 4


### `release\v3.0.0\docs\Flink\06-ai-ml\online-learning-production.md`

**问题 #3** (第 252 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpca85c2erTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpca8
- **错误行**: 3


### `release\v3.0.0\docs\Flink\06-ai-ml\rag-streaming-architecture.md`

**问题 #3** (第 464 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_ewn1_5rStreamingRAGPipeline.java:85: 错误: 非法的表达式开始
                .setRecordSerializer(...)
                                     ^
C:\Users\luyan\AppData\Local\Te
- **错误行**: 85


### `release\v3.0.0\docs\Flink\06-ai-ml\realtime-feature-engineering-feature-store.md`

**问题 #11** (第 495 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps6y61sw1StreamFeatureJoin.java:15: 错误: 非法的表达式开始
            .addSource(new FlinkKafkaConsumer<>("clicks", ...));

- **错误行**: 15

**问题 #14** (第 714 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgsmdi5prRecommendationFeatureJob.java:15: 错误: 非法的表达式开始
            .addSource(new FlinkKafkaConsumer<>("user_events", ...));

- **错误行**: 15


### `release\v3.0.0\docs\Flink\06-ai-ml\vector-database-integration.md`

**问题 #1** (第 26 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf51_rwj3VectorSink.java:2: 错误: 找不到符号
interface VectorSink<T> extends RichSinkFunction<T> {
                                ^
  符号: 类 RichSinkFunction
C:\Users\luya
- **错误行**: 2

**问题 #5** (第 266 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpru_cpblaTempValidation.java:5: 错误: 找不到符号
List<VectorRecord> candidates = milvus.search(queryVector, topK=100);
^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luy
- **错误行**: 5

**问题 #8** (第 343 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpolw6mdhaTempValidation.java:4: 错误: 需要';'
CREATE TABLE vector_items (
            ^
C:\Users\luyan\AppData\Local\Temp\tmpolw6mdhaTempValidation.java:5: 错误: 需要')'或',
- **错误行**: 4

**问题 #11** (第 453 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxbq3m1r5MilvusLookupFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
TableResult result = tEnv.sqlQuery("""
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #13** (第 532 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp25nya3s4TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp25nya3s4TempValidat
- **错误行**: 4


### `release\v3.0.0\docs\Flink\07-rust-native\ai-native-streaming\01-ai-native-architecture.md`

**问题 #8** (第 187 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnfbshgydTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnfb
- **错误行**: 3

**问题 #15** (第 403 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgciqt7qeTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpgci
- **错误行**: 3


### `release\v3.0.0\docs\Flink\07-rust-native\arroyo-update\01-arroyo-cloudflare-acquisition.md`

**问题 #16** (第 523 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 11, column 1:
    curl -X POST "<https://api.cloudf> ...
    ^ (line: 11)
- **错误行**: 11

**问题 #26** (第 905 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2gr7a7k3TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2gr
- **错误行**: 3


### `release\v3.0.0\docs\Flink\07-rust-native\flash-engine\05-flink-compatibility.md`

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

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp66t5fvz_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp66t
- **错误行**: 3


### `release\v3.0.0\docs\Flink\07-rust-native\flink-rust-ecosystem-trends-2026.md`

**问题 #6** (第 437 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 29, column 1:
    format = "parquet"
    ^ (line: 29)
- **错误行**: 29


### `release\v3.0.0\docs\Flink\07-rust-native\heterogeneous-computing\01-gpu-udf-cuda.md`

**问题 #3** (第 356 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmj3e0rrvSmallStateProcessor.java:1: 错误: 程序包org.apache.flink.streaming.api.functions不存在
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;

- **错误行**: 1


### `release\v3.0.0\docs\Flink\07-rust-native\heterogeneous-computing\04-unified-acceleration-api.md`

**问题 #10** (第 1140 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf678u6loUnifiedAccelExample.java:7: 错误: 非法的表达式开始
        TableEnvironment tEnv = TableEnvironment.create(...);

- **错误行**: 7


### `release\v3.0.0\docs\Flink\07-rust-native\iron-functions-complete-guide.md`

**问题 #17** (第 560 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcj1m31_tTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Te
- **错误行**: 3


### `release\v3.0.0\docs\Flink\07-rust-native\risingwave-comparison\01-risingwave-architecture.md`

**问题 #5** (第 350 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb441tdpoTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpb44
- **错误行**: 3


### `release\v3.0.0\docs\Flink\07-rust-native\risingwave-comparison\02-nexmark-head-to-head.md`

**问题 #8** (第 416 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvvzl__ceTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpvvz
- **错误行**: 3

**问题 #15** (第 609 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 3, column 12:
      resources:
               ^ (line: 3)
- **错误行**: 3
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `release\v3.0.0\docs\Flink\07-rust-native\risingwave-comparison\03-migration-guide.md`

**问题 #9** (第 605 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjh06ulfxNormalizeUdf.java:9: 错误: 需要 class、interface、enum 或 record
tableEnv.createTemporaryFunction("normalize", NormalizeUdf.class);
^
C:\Users\luyan\AppData\Local
- **错误行**: 9


### `release\v3.0.0\docs\Flink\07-rust-native\risingwave-comparison\04-hybrid-deployment.md`

**问题 #6** (第 499 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf3ht89p5TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpf3h
- **错误行**: 3

**问题 #8** (第 561 行, 语言: sql)

- **错误**: 可能的语法问题: -- TRINO 配置连接器
CATALOGS:
  RISINGWAVE:
    CONNECT...


### `release\v3.0.0\docs\Flink\07-rust-native\risingwave-comparison\04-risingwave-rust-udf-guide.md`

**问题 #17** (第 455 行, 语言: sql)

- **错误**: 可能的语法问题: -- 结果:
-- KEY    | VALUE | IS_NUMERIC
-- --------|...

**问题 #24** (第 743 行, 语言: sql)

- **错误**: 可能的语法问题: -- 2. 逐步增加复杂度
-- 3. 使用 EXPLAIN 查看执行计划
EXPLAIN SELE...


### `release\v3.0.0\docs\Flink\07-rust-native\risingwave-rust-udf-native-guide.md`

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


### `release\v3.0.0\docs\Flink\07-rust-native\simd-optimization\03-jni-assembly-bridge.md`

**问题 #1** (第 44 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7g2ey9aoTempValidation.java:4: 错误: 找不到符号
VectorSpecies<Float> SPECIES = FloatVector.SPECIES_256;
^
  符号:   类 VectorSpecies
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #2** (第 136 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvzzsomfvTempValidation.java:4: 错误: 找不到符号
long address = unsafe.allocateMemory(size + 32);
                                     ^
  符号:   变量 size
  位置: 类 TempValida
- **错误行**: 4


### `release\v3.0.0\docs\Flink\07-rust-native\vectorized-udfs\01-vectorized-udf-intro.md`

**问题 #5** (第 375 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 71

**问题 #8** (第 985 行, 语言: sql)

- **错误**: 可能的语法问题: -- ============================================
--...


### `release\v3.0.0\docs\Flink\08-roadmap\08.01-flink-24\2026-q2-flink-tasks.md`

**问题 #13** (第 473 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpydrp4nx4TempValidation.java:4: 错误: 找不到符号
for (KeyGroup kg : keyGroups) {
                   ^
  符号:   变量 keyGroups
  位置: 类 TempValidation
C:\Users\luyan\AppData\Lo
- **错误行**: 4


### `release\v3.0.0\docs\Flink\08-roadmap\08.01-flink-24\FLIP-TRACKING-SYSTEM.md`

**问题 #5** (第 392 行, 语言: yaml)

- **错误**: while parsing a block mapping
  in "<unicode string>", line 37, column 5:
        <!-- FLIP状态: Draft/Under Discuss ...
        ^ (line: 37)
expected <block end>, but found '-'
  in "<unicode string>"
- **错误行**: 37


### `release\v3.0.0\docs\Flink\08-roadmap\08.01-flink-24\community-dynamics-tracking.md`

**问题 #15** (第 423 行, 语言: yaml)

- **错误**: sequence entries are not allowed here
  in "<unicode string>", line 4, column 54:
     ... park to Flink: Lessons Learned" - 12K views
                                         ^ (line: 4)
- **错误行**: 4


### `release\v3.0.0\docs\Flink\08-roadmap\08.01-flink-24\flink-2.1-frontier-tracking.md`

**问题 #4** (第 410 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2veb_7q5TempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4


### `release\v3.0.0\docs\Flink\08-roadmap\08.01-flink-24\flink-2.3-2.4-roadmap.md`

**问题 #11** (第 313 行, 语言: yaml)

- **错误**: while parsing a block collection
  in "<unicode string>", line 9, column 7:
          - JOB_MANAGER_RPC_ADDRESS=jobmanager
          ^ (line: 9)
expected <block end>, but found '<scalar>'
  in "<unico
- **错误行**: 9


### `release\v3.0.0\docs\Flink\08-roadmap\08.01-flink-24\flink-2.4-tracking.md`

**问题 #12** (第 481 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjb9zp1elTempValidation.java:6: 错误: 找不到符号
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
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnzcub5r7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #24** (第 981 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 2, column 4:
      S: Agent状态空间 (Memory + Context)
       ^ (line: 2)
- **错误行**: 2
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #28** (第 1126 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpihdrj91oAgent.java:15: 错误: 未命名类 是预览功能，默认情况下禁用。
AgentCoordinator coordinator = env.getAgentCoordinator();
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData
- **错误行**: 15

**问题 #34** (第 1398 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 2, column 7:
      V(t): 时变顶点集合
          ^ (line: 2)
- **错误行**: 2
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #35** (第 1422 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 18, column 5:
      支持: MATCH, WHERE, RETURN
        ^ (line: 18)
- **错误行**: 18
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #38** (第 1575 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7mu1hdq_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp7mu1h
- **错误行**: 3

**问题 #43** (第 1769 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1nbs2cwyTempValidation.java:4: 错误: 找不到符号
UnifiedSource<RowData> source = UnifiedSource.<RowData>builder()
^
  符号:   类 UnifiedSource
  位置: 类 TempValidation
C:\Users
- **错误行**: 4


### `release\v3.0.0\docs\Flink\08-roadmap\08.01-flink-24\flink-2.5-preview.md`

**问题 #1** (第 42 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 1, column 32:
    预计发布时间: 2026 Q3 (Feature Freeze: 2026-07, GA: 2026-09)
                                   ^ (line: 1)
- **错误行**: 1
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #3** (第 97 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 1, column 33:
    FLIP: FLIP-442 "Serverless Flink: Zero-to-Infinity Scaling"
                                    ^ (line: 1)
- **错误行**: 1
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #12** (第 432 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp48dw1drbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #14** (第 515 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl0nb10qvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpl0nb10qvTemp
- **错误行**: 3


### `release\v3.0.0\docs\Flink\08-roadmap\08.01-flink-24\flink-25-stream-batch-unification.md`

**问题 #15** (第 612 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9maapae9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #16** (第 655 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx2ixj8grTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #19** (第 853 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph2kwdjbgTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmph2kwdjbgTemp
- **错误行**: 3

**问题 #25** (第 1156 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp40d537isTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #26** (第 1177 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptdkg6jzxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #29** (第 1245 行, 语言: yaml)
- **错误**: mapping values are not allowed here
  in "<unicode string>", line 5, column 31:
        配置: execution.runtime-mode: STREAMING
                                  ^ (line: 5)
- **错误行**: 5
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `release\v3.0.0\docs\Flink\08-roadmap\08.01-flink-24\flink-30-architecture-redesign.md`

**问题 #3** (第 153 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjtj0a40cExecutionMode.java:12: 错误: 不是语句
    if (stream.isUnbounded() && hints.latency < 100ms)
                                                   ^
C:\Users\luyan\
- **错误行**: 12

**问题 #5** (第 204 行, 语言: yaml)
- **错误**: while parsing a block collection
  in "<unicode string>", line 2, column 3:
      - HotData: L1 + L2 (95%+命中率，3.0目标)
      ^ (line: 2)
expected <block end>, but found '?'
  in "<unicode string>", line
- **错误行**: 2

**问题 #17** (第 566 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp18ze4r47TempValidation.java:3: 错误: 需要';'
ExecutionMode selectOptimalMode(DataCharacteristics data, QueryRequirements req) {
                               ^
C:\Use
- **错误行**: 3

**问题 #24** (第 773 行, 语言: java)
- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6kc5e5bvTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmp6k
- **错误行**: 4


### `release\v3.0.0\docs\Flink\08-roadmap\08.01-flink-24\flink-version-evolution-complete-guide.md`

**问题 #3** (第 137 行, 语言: yaml)
- **错误**: while parsing a block mapping
  in "<unicode string>", line 6, column 3:
      FLIP-217: "Incremental Checkpoin ...
      ^ (line: 6)
expected <block end>, but found '<block sequence start>'
  in "<u
- **错误行**: 6

**问题 #4** (第 173 行, 语言: yaml)
- **错误**: while parsing a block mapping
  in "<unicode string>", line 6, column 3:
      FLIP-265: "Adaptive Scheduler Im ...
      ^ (line: 6)
expected <block end>, but found '<block sequence start>'
  in "<u
- **错误行**: 6

**问题 #6** (第 209 行, 语言: yaml)
- **错误**: while parsing a block mapping
  in "<unicode string>", line 7, column 3:
      FLIP-311: "DataSet API Deprecati ...
      ^ (line: 7)
expected <block end>, but found '<block sequence start>'
  in "<u
- **错误行**: 7

**问题 #7** (第 245 行, 语言: yaml)
- **错误**: while parsing a block mapping
  in "<unicode string>", line 8, column 6:
         FLIP-392: "Disaggregated State S ...
         ^ (line: 8)
expected <block end>, but found '-'
  in "<unicode string>"
- **错误行**: 8

**问题 #8** (第 298 行, 语言: yaml)
- **错误**: while parsing a block mapping
  in "<unicode string>", line 6, column 3:
      FLIP-435: "Materialized Table"
      ^ (line: 6)
expected <block end>, but found '<block sequence start>'
  in "<unicode
- **错误行**: 6

**问题 #10** (第 341 行, 语言: yaml)
- **错误**: while parsing a block mapping
  in "<unicode string>", line 6, column 3:
      FLIP-471: "VECTOR_SEARCH Support ...
      ^ (line: 6)
expected <block end>, but found '<scalar>'
  in "<unicode string>
- **错误行**: 6

**问题 #12** (第 389 行, 语言: sql)
- **错误**: 可能的语法问题: -- 注册ML模型
<!-- 以下语法为概念设计，实际 FLINK 版本尚未支持 -->
~~CRE...

**问题 #13** (第 411 行, 语言: yaml)

- **错误**: while parsing a block mapping
  in "<unicode string>", line 6, column 3:
      FLIP-531: "Flink AI Agents" (MVP ...
      ^ (line: 6)
expected <block end>, but found '<scalar>'
  in "<unicode string>
- **错误行**: 6

**问题 #30** (第 857 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptqw7__p7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmptqw7__p7TempV
- **错误行**: 3

**问题 #31** (第 880 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq7adjjlxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #32** (第 907 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2lxbtcszTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2lxbtcszTemp
- **错误行**: 3


### `release\v3.0.0\docs\Flink\08-roadmap\08.02-flink-25\flink-25-features-preview.md`

**问题 #2** (第 37 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplh54bddjTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmplh5
- **错误行**: 3

**问题 #7** (第 139 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7_nxstpmTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp7_n
- **错误行**: 3

**问题 #8** (第 159 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwb0840woTempValidation.java:4: 错误: 找不到符号
InferenceConfig config = InferenceConfig.builder()
^
  符号:   类 InferenceConfig
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #14** (第 263 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnxdqqsptTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnxdqqsptTemp
- **错误行**: 3


### `release\v3.0.0\docs\Flink\08-roadmap\08.02-flink-25\flink-25-migration-guide.md`

**问题 #7** (第 134 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    execution.runtime-mode: adaptive ...
    ^ (line: 2)
found duplicate key "execution.runtime-mode" with value "streaming" (o
- **错误行**: 2

**问题 #8** (第 150 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpak0ddwtpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #9** (第 178 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3qcpihzaTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp3qcpihzaTemp
- **错误行**: 3


### `release\v3.0.0\docs\Flink\08-roadmap\08.02-flink-25\flink-25-roadmap.md`

**问题 #1** (第 15 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 3, column 19:
      - Feature Freeze: 2026-07
                      ^ (line: 3)
- **错误行**: 3
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #2** (第 44 行, 语言: yaml)

- **错误**: while parsing a block collection
  in "<unicode string>", line 3, column 5:
        - 统一执行计划生成器
        ^ (line: 3)
expected <block end>, but found '?'
  in "<unicode string>", line 6, column 5:

- **错误行**: 3

**问题 #3** (第 79 行, 语言: yaml)

- **错误**: while parsing a block collection
  in "<unicode string>", line 3, column 5:
        - 无流量时资源释放至 0
        ^ (line: 3)
expected <block end>, but found '?'
  in "<unicode string>", line 6, column 5:

- **错误行**: 3

**问题 #4** (第 112 行, 语言: yaml)

- **错误**: while parsing a block collection
  in "<unicode string>", line 3, column 5:
        - 动态批处理
        ^ (line: 3)
expected <block end>, but found '?'
  in "<unicode string>", line 6, column 5:
        状
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.01-case-studies\case-ecommerce-realtime-recommendation.md`

**问题 #19** (第 1846 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbzbrx7yjTempValidation.java:4: 错误: 非法的表达式开始
public UserProfile updateProfile(UserProfile current, BehaviorEvent event) {
^
C:\Users\luyan\AppData\Local\Temp\tmpbzb
- **错误行**: 4


### `release\v3.0.0\docs\Flink\09-practices\09.01-case-studies\case-financial-realtime-risk-control.md`

**问题 #6** (第 494 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeh8fbm9oTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpeh8
- **错误行**: 3

**问题 #7** (第 506 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9s9lo6x5TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9s9lo
- **错误行**: 3

**问题 #10** (第 557 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqipzhoc7TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpqipzhoc7TempValidat
- **错误行**: 4

**问题 #11** (第 591 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvfd4gpreTempValidation.java:4: 错误: 找不到符号
LoadingCache<String, UserProfile> profileCache = Caffeine.newBuilder()
^
  符号:   类 LoadingCache
  位置: 类 TempValidation
C:\
- **错误行**: 4

**问题 #24** (第 1779 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbe6e2a1uTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpbe6e2a1uTem
- **错误行**: 3

**问题 #25** (第 1806 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp16tcdg8aTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmp16tcdg8aTempValidatio
- **错误行**: 4

**问题 #26** (第 1833 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5l4fskjeTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5l4
- **错误行**: 3

**问题 #29** (第 1892 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphltjp511TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmphltjp511Tem
- **错误行**: 3

**问题 #30** (第 1910 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph6frwrhbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmph6f
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.01-case-studies\case-fraud-detection-advanced.md`

**问题 #8** (第 764 行, 语言: sql)

- **错误**: 可能的语法问题: -- REDIS 特征表结构
-- 用户实时统计特征
HSET USER:STATS:{USER_I...


### `release\v3.0.0\docs\Flink\09-practices\09.01-case-studies\case-gaming-realtime-analytics.md`

**问题 #8** (第 773 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqyka25qiGamingAnalyticsJob.java:188: 错误: 需要'('或'['
                )
                ^
1 个错误

- **错误行**: 188


### `release\v3.0.0\docs\Flink\09-practices\09.01-case-studies\case-iot-stream-processing.md`

**问题 #3** (第 253 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkjzvt5gdTempValidation.java:4: 错误: 找不到符号
    .<SensorEvent>forBoundedOutOfOrderness(Duration.ofSeconds(10))
      ^
  符号:   类 SensorEvent
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #5** (第 334 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3t2m5pnzTempValidation.java:4: 错误: 找不到符号
    .<SensorEvent>forBoundedOutOfOrderness(Duration.ofSeconds(10))
      ^
  符号:   类 SensorEvent
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #6** (第 361 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa1yzmccvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpa1yzm
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.01-case-studies\case-realtime-analytics.md`

**问题 #11** (第 809 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcvf9dq5wTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpcv
- **错误行**: 4

**问题 #12** (第 851 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpshkyl7wxTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpsh
- **错误行**: 4

**问题 #16** (第 1053 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbe9b6218TempValidation.java:4: 错误: 非法的表达式开始
public int getPartition(String userId) {
^
C:\Users\luyan\AppData\Local\Temp\tmpbe9b6218TempValidation.java:13: 错误: 需要
- **错误行**: 4

**问题 #17** (第 1086 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj_s61vdrTempValidation.java:5: 错误: 需要';'
    .withIdleness(Duration.ofMinutes(1))  // 1分钟无数据视为空闲
                                        ^
1 个错误

- **错误行**: 5

**问题 #18** (第 1110 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd77coz2nTempValidation.java:3: 错误: 非法的表达式开始
        .map(new ParseFunction())
        ^
C:\Users\luyan\AppData\Local\Temp\tmpd77coz2nTempValidation.java:5: 错误: 需要'
- **错误行**: 3

**问题 #19** (第 1120 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp31fj12lbTempValidation.java:3: 错误: 找不到符号
        StateTtlConfig ttlConfig = StateTtlConfig
        ^
  符号:   类 StateTtlConfig
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 3

**问题 #20** (第 1133 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyi9psfsaTempValidation.java:4: 错误: 需要';'
public void snapshotState(FunctionSnapshotContext context) throws Exception {
                         ^
C:\Users\luyan\Ap
- **错误行**: 4


### `release\v3.0.0\docs\Flink\09-practices\09.01-case-studies\case-smart-grid-energy-management.md`

**问题 #7** (第 659 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiiya284tTempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend rocksDbBackend = new RocksDBStateBackend(
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempValidation
C:\Us
- **错误行**: 4


### `release\v3.0.0\docs\Flink\09-practices\09.01-case-studies\case-smart-manufacturing-iot.md`

**问题 #5** (第 506 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn73ck5qyTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpn73ck5qyTempValidatio
- **错误行**: 4


### `release\v3.0.0\docs\Flink\09-practices\09.02-benchmarking\flink-24-25-benchmark-results.md`

**问题 #5** (第 383 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 7, column 3:
      RocksDB: 9.2.0
      ^ (line: 7)
found duplicate key "ForSt" with value "2.5.0-tiered (2.5)" (original value: "2.4.0-nativ
- **错误行**: 7


### `release\v3.0.0\docs\Flink\09-practices\09.02-benchmarking\performance-benchmark-suite.md`

**问题 #5** (第 475 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdashgb3oTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpdas
- **错误行**: 3

**问题 #6** (第 489 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpenlxevkrTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpenlxevkrTempValidat
- **错误行**: 4

**问题 #7** (第 524 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd3kf8b5mTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpd3kf8b5mTempValidat
- **错误行**: 4

**问题 #18** (第 1232 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 21

**问题 #19** (第 1481 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 82


### `release\v3.0.0\docs\Flink\09-practices\09.02-benchmarking\performance-benchmarking-guide.md`

**问题 #6** (第 251 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3_2evqbxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp3_2
- **错误行**: 3

**问题 #7** (第 299 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1r87nbueTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1r8
- **错误行**: 3

**问题 #9** (第 361 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmple3mqarwTempValidation.java:4: 错误: 找不到符号
MetricGroup metricGroup = getRuntimeContext()
^
  符号:   类 MetricGroup
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #18** (第 607 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt1if6cmuTempValidation.java:5: 错误: 非法的表达式开始
    .window(...)  // 第一阶段
            ^
C:\Users\luyan\AppData\Local\Temp\tmpt1if6cmuTempValidation.java:8: 错误: 非法的表达式开
- **错误行**: 5

**问题 #19** (第 619 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3hfo7tl3TempValidation.java:4: 错误: 找不到符号
stream.map(event -> {
^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp3hfo7tl3TempValidati
- **错误行**: 4


### `release\v3.0.0\docs\Flink\09-practices\09.02-benchmarking\streaming-benchmarks.md`

**问题 #4** (第 295 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp931fd50tTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #6** (第 361 行, 语言: yaml)

- **错误**: while scanning a simple key
  in "<unicode string>", line 15, column 1:
    rate(flink_taskmanager_job_task_ ...
    ^ (line: 15)
could not find expected ':'
  in "<unicode string>", line 17, column
- **错误行**: 15


### `release\v3.0.0\docs\Flink\09-practices\09.03-performance-tuning\05-vs-competitors\flink-vs-kafka-streams.md`

**问题 #10** (第 323 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq8xfemg6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpq8xfe
- **错误行**: 3

**问题 #11** (第 349 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp37248mreTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp372
- **错误行**: 3

**问题 #12** (第 364 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1zsf1h_3TempValidation.java:4: 错误: 找不到符号
WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ofSeconds(30))
                   ^
  符号:   类 Event
  位置: 类 Tem
- **错误行**: 4

**问题 #17** (第 528 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmufjudx6TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.typeinfo.Types;
^
C:\Users\luyan\AppData\Local\Temp\tmpmufjudx6TempValidation.java:4
- **错误行**: 4

**问题 #18** (第 581 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz6bdoehnTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpz6b
- **错误行**: 3

**问题 #24** (第 1004 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn2_m8cvlTempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #25** (第 1022 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbzjpfvl7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.03-performance-tuning\05-vs-competitors\flink-vs-risingwave-deep-dive.md`

**问题 #7** (第 319 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp23yzib9rTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp23y
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.03-performance-tuning\05-vs-competitors\linkedin-samza-deep-dive.md`

**问题 #8** (第 332 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc840edd1WordCountTask.java:24: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Tuple2<String, Integer>> wordCounts =
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 24

**问题 #10** (第 415 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmjjx4wjlTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpmjj
- **错误行**: 3

**问题 #11** (第 431 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp8hku44pTempValidation.java:8: 错误: 非法的表达式开始
public void processActivity(MemberEvent event, MessageCollector collector) {
^
C:\Users\luyan\AppData\Local\Temp\tmpp8h
- **错误行**: 8

**问题 #12** (第 448 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeztdu_anTempValidation.java:3: 错误: 找不到符号
        Table memberProfile = tableEnv.fromDataStream(profileStream)
        ^
  符号:   类 Table
  位置: 类 TempValidation
C:\U
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.03-performance-tuning\06.02-performance-optimization-complete.md`

**问题 #4** (第 450 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp7vu8gjsTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #7** (第 563 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkt1slfp2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpkt1
- **错误行**: 3

**问题 #8** (第 606 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp633bm9o_Order.java:2: 错误: 需要 class、interface、enum 或 record
env.getConfig().registerTypeWithKryoSerializer(
^
C:\Users\luyan\AppData\Local\Temp\tmp633bm9o_Order.jav
- **错误行**: 2

**问题 #11** (第 729 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpck2aj1ojTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpck2
- **错误行**: 3

**问题 #12** (第 775 行, 语言: sql)

- **错误**: 可能的语法问题: -- 查看执行计划
EXPLAIN SELECT
    USER_ID,
    COUNT(*)...; 可能的语法问题: -- 使用EXPLAIN ESTIMATED_COST查看代价估算
EXPLAIN ESTIMATE...

**问题 #16** (第 903 行, 语言: sql)

- **错误**: 可能的语法问题: -- 动态分区裁剪
SET TABLE.OPTIMIZER.DYNAMIC-FILTERING.EN...

**问题 #22** (第 1140 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsejx76xyTempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<Event> kafkaSource = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #23** (第 1199 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa61xdx2wAsyncUserLookup.java:41: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<EnrichedEvent> enriched = AsyncDataStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 41

**问题 #25** (第 1296 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwg7yitdlTempValidation.java:4: 错误: 找不到符号
HikariConfig config = new HikariConfig();
^
  符号:   类 HikariConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #27** (第 1376 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpir45wf3rTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpir4
- **错误行**: 3

**问题 #29** (第 1436 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp06iq7urzFraudResultSink.java:36: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<FraudResult> results = AsyncDataStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 36

**问题 #31** (第 1521 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8gwas7evTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp8gwas7evTempValidat
- **错误行**: 4


### `release\v3.0.0\docs\Flink\09-practices\09.03-performance-tuning\flink-24-performance-improvements.md`

**问题 #7** (第 474 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0gxhctmyUserEvent.java:13: 错误: 未命名类 是预览功能，默认情况下禁用。
ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();
^
  （请使用 --enable-preview 以启用 未命名类）
C
- **错误行**: 13

**问题 #10** (第 551 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbgifblm1TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.CheckpointingMode;
^
C:\Users\luyan\AppData\Local\Temp\tmpbgifblm1TempValidation.
- **错误行**: 4

**问题 #11** (第 586 行, 语言: sql)

- **错误**: 可能的语法问题: -- 启用向量化执行
SET TABLE.EXEC.MINI-BATCH.ENABLED = TRU...; 可能的语法问题: -- 启用自适应JOIN
SET TABLE.OPTIMIZER.ADAPTIVE-JOIN.ENA...; 可能的语法问题: -- 启用谓词下推
SET TABLE.OPTIMIZER.PREDICATE-PUSHDOWN.E...; 可能的语法问题:

**问题 #13** (第 631 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3temm77zTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp3temm77zTemp
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.03-performance-tuning\flink-tco-cost-optimization-guide.md`

**问题 #5** (第 791 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe8idsp7aTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.03-performance-tuning\performance-tuning-guide.md`

**问题 #3** (第 297 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp16wkixihTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp16w
- **错误行**: 3

**问题 #4** (第 318 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    execution.checkpointing.unaligne ...
    ^ (line: 2)
found duplicate key "execution.checkpointing.interval" with value "600
- **错误行**: 2


### `release\v3.0.0\docs\Flink\09-practices\09.03-performance-tuning\state-backend-selection.md`

**问题 #1** (第 337 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp81tgtjg_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #2** (第 363 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpskvswbomTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend backend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #3** (第 384 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi8gexw7rTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend backend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #5** (第 425 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpldzl3rrzTempValidation.java:3: 错误: 找不到符号
        conf.setString("taskmanager.memory.managed.size", "64mb");  // 过小！
        ^
  符号:   变量 conf
  位置: 类 TempValidatio
- **错误行**: 3

**问题 #6** (第 433 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpabawusrlTempValidation.java:3: 错误: 找不到符号
        conf.setString("taskmanager.memory.managed.fraction", "0.4");
        ^
  符号:   变量 conf
  位置: 类 TempValidation
C:\
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.03-performance-tuning\stream-processing-cost-optimization.md`

**问题 #4** (第 318 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjdeybpo7TempValidation.java:6: 错误: 找不到符号
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
  in "<unicode string>", line 10, co
- **错误行**: 2

**问题 #19** (第 1118 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpydtoi3poTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.03-performance-tuning\stream-processing-testing-strategies.md`

**问题 #3** (第 196 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjld_53k8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #4** (第 234 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd10qy6qjTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.typeinfo.Types;
^
C:\Users\luyan\AppData\Local\Temp\tmpd10qy6qjTempValidation.java:4
- **错误行**: 4

**问题 #5** (第 268 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5p26cionTempValidation.java:8: 错误: 需要';'
public void testEnrichmentOperatorWithMock() throws Exception {
                                          ^
C:\Users\luyan
- **错误行**: 8

**问题 #6** (第 305 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxaquuuvuTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpxa
- **错误行**: 4

**问题 #7** (第 357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbtrl9rc8TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpbt
- **错误行**: 4

**问题 #8** (第 401 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsipsbqh9TempValidation.java:4: 错误: 需要';'
public void testCheckpointRecovery() throws Exception {
                                  ^
C:\Users\luyan\AppData\Local\T
- **错误行**: 4

**问题 #9** (第 453 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp730so5vjTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmp73
- **错误行**: 4

**问题 #11** (第 549 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphwsmbftgTempValidation.java:4: 错误: 需要';'
public void testFailureRecovery() throws Exception {
                               ^
C:\Users\luyan\AppData\Local\Temp\tm
- **错误行**: 4

**问题 #13** (第 666 行, 语言: java)

- **错误**: 括号不匹配: (=79, )=83

**问题 #23** (第 1445 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmporzvf_k6StreamPerformanceBenchmark.java:6: 错误: 需要 class、interface、enum 或 record
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\
- **错误行**: 6


### `release\v3.0.0\docs\Flink\09-practices\09.03-performance-tuning\troubleshooting-handbook.md`

**问题 #16** (第 476 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2zi1no_9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp2zi1no_9Tem
- **错误行**: 3

**问题 #26** (第 606 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpma0k5qfuTempValidation.java:4: 错误: 找不到符号
    .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(30))
      ^
  符号:   类 Event
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4

**问题 #28** (第 622 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuk6_lctbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpuk6
- **错误行**: 3

**问题 #29** (第 640 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjsjxh875TempValidation.java:4: 错误: 找不到符号
WatermarkStrategy.<Event>forBoundedOutOfOrderness(
                   ^
  符号:   类 Event
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #32** (第 680 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0fi_gurhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp0fi_gurhTem
- **错误行**: 3

**问题 #37** (第 749 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    restart-strategy: fixed-delay
    ^ (line: 2)
found duplicate key "restart-strategy" with value "exponential-delay" (origina
- **错误行**: 2

**问题 #39** (第 773 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaoqh1n95TempValidation.java:5: 错误: 找不到符号
    externalService.call();
    ^
  符号:   变量 externalService
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpa
- **错误行**: 5


### `release\v3.0.0\docs\Flink\09-practices\09.04-deployment\flink-k8s-operator-migration-1.13-to-1.14.md`

**问题 #18** (第 556 行, 语言: yaml)

- **错误**: while scanning a block scalar
  in "<unicode string>", line 6, column 22:
        - Reconcile 成功率: > 99%
                         ^ (line: 6)
expected a comment or a line break, but found '9'
  in "<u
- **错误行**: 6

**问题 #22** (第 697 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 1


### `release\v3.0.0\docs\Flink\09-practices\09.04-deployment\flink-kubernetes-operator-1.14-guide.md`

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
      "$schema": "<http://json-schem>
- **错误行**: 9

**问题 #22** (第 699 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    spec:
    ^ (line: 2)
found duplicate key "spec" with value "{}" (original value: "{}")
  in "<unicode string>", line 10, co
- **错误行**: 2

**问题 #35** (第 1674 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 24, column 1:
    apiVersion: kustomize.config.k8s ...
    ^ (line: 24)
found duplicate key "apiVersion" with value "flink.apache.org/v1beta
- **错误行**: 24


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\flink-24-security-enhancements.md`

**问题 #5** (第 163 行, 语言: yaml)

- **错误**: while parsing a block mapping
  in "<unicode string>", line 2, column 1:
    security.oauth.enabled: true
    ^ (line: 2)
expected <block end>, but found '<scalar>'
  in "<unicode string>", line 3, co
- **错误行**: 2

**问题 #13** (第 392 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyl6acf30TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpyl6
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\flink-security-complete-guide.md`

**问题 #8** (第 503 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjudgq3cqTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
^
C:\Users\luyan\AppData\Local\Temp\tmpjudgq3cqT
- **错误行**: 4


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\security-hardening-guide.md`

**问题 #15** (第 545 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkpsef6z7EncryptedRocksDBStateBackend.java:29: 错误: 非法的表达式开始
            super.createKeyedStateBackend(...),
                                          ^
C:\Users\luy
- **错误行**: 29

**问题 #16** (第 585 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    state.backend: rocksdb
    ^ (line: 4)
found duplicate key "s3.server-side-encryption" with value "aws:kms" (original value:
- **错误行**: 4

**问题 #18** (第 622 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_qsfq4c5TempValidation.java:4: 错误: 找不到符号
Properties kafkaProps = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #19** (第 643 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9omg8zblTempValidation.java:10: 错误: 找不到符号
JDBCInputFormat jdbcInput = JDBCInputFormat.buildJDBCInputFormat()
^
  符号:   类 JDBCInputFormat
  位置: 类 TempValidation
C:\
- **错误行**: 10

**问题 #20** (第 664 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxdi49j53TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.runtime.state.encryption.EncryptionOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmpxdi49j53Temp
- **错误行**: 3

**问题 #26** (第 863 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7xczut4aRowLevelSecurityFilter.java:24: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Event> securedStream = rawStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 24


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\security\evolution\audit-evolution.md`

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprfeqb_m3TempValidation.java:3: 错误: 找不到符号
        auditLog.record(new AuditEvent()
        ^
  符号:   变量 auditLog
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\security\evolution\auth-evolution.md`

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaolcgcdlTempValidation.java:3: 错误: 找不到符号
        OAuth2Client client = new OAuth2Client()
        ^
  符号:   类 OAuth2Client
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\security\evolution\authorization-evolution.md`

**问题 #2** (第 67 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz78w1iclTempValidation.java:3: 错误: 找不到符号
if (authorizer.hasPermission(user, "jobs:cancel", jobId)) {
                             ^
  符号:   变量 user
  位置: 类 TempVal
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\security\evolution\compliance-evolution.md`

**问题 #2** (第 69 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbgnqbif1TempValidation.java:4: 错误: 此处不允许使用修饰符private
private String ssn;
               ^
C:\Users\luyan\AppData\Local\Temp\tmpbgnqbif1TempValidation.java:3: 错误: 找
- **错误行**: 4


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\security\evolution\data-governance-evolution.md`

**问题 #1** (第 55 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgt4at6vwTempValidation.java:3: 错误: 找不到符号
        LineageRecorder.record(new DataLineage()
        ^
  符号:   变量 LineageRecorder
  位置: 类 TempValidation
C:\Users\luya
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\security\evolution\encryption-evolution.md`

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv4bpnapkTempValidation.java:3: 错误: 找不到符号
        KeyVault vault = KeyVault.create(config);
        ^
  符号:   类 KeyVault
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\security\evolution\key-management-evolution.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3uq47io7TempValidation.java:3: 错误: 找不到符号
        Vault vault = Vault.builder()
        ^
  符号:   类 Vault
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\security\evolution\lineage-evolution.md`

**问题 #1** (第 54 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpliq2_4s2TempValidation.java:3: 错误: 找不到符号
        LineageContext ctx = LineageContext.current();
        ^
  符号:   类 LineageContext
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\security\evolution\tee-evolution.md`

**问题 #1** (第 57 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3z0rneifTempValidation.java:3: 错误: 找不到符号
        Enclave enclave = EnclaveLoader.load("enclave.so");
        ^
  符号:   类 Enclave
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 3

**问题 #2** (第 66 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyr7p034sTempValidation.java:4: 错误: 找不到符号
EnclaveResult result = teeExecutor.execute(() -> {
^
  符号:   类 EnclaveResult
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\spiffe-spire-integration-guide.md`

**问题 #14** (第 715 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp0y47_7nTempValidation.java:4: 错误: 找不到符号
Properties kafkaProps = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #15** (第 750 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9ckxynrmTempValidation.java:4: 错误: 找不到符号
RestClientBuilder builder = RestClient.builder(
^
  符号:   类 RestClientBuilder
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\streaming-security-best-practices.md`

**问题 #4** (第 208 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 9, column 1:
    ssl.keystore.location=/etc/kafka ...
    ^ (line: 9)
- **错误行**: 9

**问题 #8** (第 326 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx52gwb8cTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpx52gwb8
- **错误行**: 3


### `release\v3.0.0\docs\Flink\09-practices\09.04-security\trusted-execution-flink.md`

**问题 #13** (第 486 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 2

**问题 #14** (第 505 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 1


### `release\v3.0.0\docs\Flink\09-practices\09.05-edge\flink-edge-resource-optimization.md`

**问题 #2** (第 274 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnka9xfx_TempValidation.java:6: 错误: 找不到符号
env.setParallelism(optimalParallelism);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpnka9x
- **错误行**: 6

**问题 #3** (第 286 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe9aqcqqfTempValidation.java:5: 错误: 非法的表达式开始
    .filter(...)
            ^
C:\Users\luyan\AppData\Local\Temp\tmpe9aqcqqfTempValidation.java:6: 错误: 非法的表达式开始
    .ma
- **错误行**: 5

**问题 #4** (第 304 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppwis4hbzTempValidation.java:5: 错误: 找不到符号
    inputStream,
    ^
  符号:   变量 inputStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmppwis4hbzTempVali
- **错误行**: 5


### `release\v3.0.0\docs\Flink\09-practices\09.05-edge\flink-edge-streaming-guide.md`

**问题 #3** (第 300 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv7mx8h2hTempValidation.java:8: 错误: 找不到符号
    .filter(nonNullFilter);
            ^
  符号:   变量 nonNullFilter
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 8

**问题 #4** (第 317 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv4bg4iggTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpv4bg4
- **错误行**: 3


### `release\v3.0.0\docs\Flink\3.9-state-backends-deep-comparison.md`

**问题 #21** (第 589 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend.rocksdb.memory.man ...
    ^ (line: 2)
found duplicate key "state.backend.rocksdb.memory.managed" with value
- **错误行**: 2

**问题 #22** (第 610 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend.rocksdb.compaction ...
    ^ (line: 2)
found duplicate key "state.backend.rocksdb.compaction.style" with valu
- **错误行**: 2


### `release\v3.0.0\docs\Flink\data-types-complete-reference.md`

**问题 #6** (第 261 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjagmtrqaTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.DataTypes;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpjagmtrqaTempValidat
- **错误行**: 3


### `release\v3.0.0\docs\Flink\elasticsearch-connector-guide.md`

**问题 #4** (第 248 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp45qe7n76TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.elasticsearch.sink.Elasticsearch7SinkBuilder;
^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #6** (第 325 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc13pzrfxTempValidation.java:4: 错误: 找不到符号
ElasticsearchSink<Event> esSink = new Elasticsearch7SinkBuilder<Event>()
^
  符号:   类 ElasticsearchSink
  位置: 类 TempValidat
- **错误行**: 4


### `release\v3.0.0\docs\Flink\flink-nexmark-benchmark-guide.md`

**问题 #2** (第 234 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyjlgeevrTempValidation.java:5: 错误: 找不到符号
Random random = new Random(SEED);
^
  符号:   类 Random
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpyjlgeevrT
- **错误行**: 5

**问题 #3** (第 242 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmparek3x99TempValidation.java:5: 错误: 找不到符号
long eventTime = baseTime + (offsetSec * 1000);
                             ^
  符号:   变量 offsetSec
  位置: 类 TempValidation
- **错误行**: 5

**问题 #10** (第 381 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw8h9t6e0TempValidation.java:4: 错误: 找不到符号
tableEnv.getConfig().getConfiguration()
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #12** (第 405 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8_mqin_uTempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #15** (第 459 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzttn0e_jTempValidation.java:4: 错误: 需要';'
CREATE TABLE Person (
            ^
C:\Users\luyan\AppData\Local\Temp\tmpzttn0e_jTempValidation.java:5: 错误: 需要')'或','

- **错误行**: 4

**问题 #16** (第 495 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp77c90aaoTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\Flink\flink-state-backends-comparison.md`

**问题 #8** (第 487 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpria1sltbTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #9** (第 514 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyboo43lnTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #10** (第 563 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptw6bypucTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #14** (第 719 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp90ojghzmTempValidation.java:4: 错误: 找不到符号
config.set(RocksDBOptions.BLOCK_CACHE_SIZE, MemorySize.ofMebiBytes(256));
           ^
  符号:   变量 RocksDBOptions
  位置: 类 T
- **错误行**: 4

**问题 #16** (第 736 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkbd7zakwTempValidation.java:3: 错误: 找不到符号
        config.set(CheckpointingOptions.INCREMENTAL_CHECKPOINTS, true);
                   ^
  符号:   变量 CheckpointingOptio
- **错误行**: 3

**问题 #18** (第 746 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplen531kcTempValidation.java:3: 错误: 找不到符号
        config.set(CheckpointingOptions.MAX_CONCURRENT_CHECKPOINTS, 1);
                   ^
  符号:   变量 CheckpointingOptio
- **错误行**: 3

**问题 #20** (第 759 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpicuzxianTempValidation.java:4: 错误: 找不到符号
config.set(CheckpointingOptions.LOCAL_RECOVERY, true);
           ^
  符号:   变量 CheckpointingOptions
  位置: 类 TempValidation
- **错误行**: 4


### `release\v3.0.0\docs\Flink\jdbc-connector-guide.md`

**问题 #4** (第 226 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpau261c4jTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcConnectionOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmpau261c4jTempValida
- **错误行**: 3

**问题 #6** (第 295 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxzaxdzdfTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcInputFormat;
^
C:\Users\luyan\AppData\Local\Temp\tmpxzaxdzdfTempValidation.j
- **错误行**: 3


### `release\v3.0.0\docs\Flink\mongodb-connector-guide.md`

**问题 #4** (第 246 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpma_u2f21TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.source.MongoSource;
^
C:\Users\luyan\AppData\Local\Temp\tmpma_u2f21TempValida
- **错误行**: 3

**问题 #5** (第 282 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmrb1a3t1TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.source.MongoSource;
^
C:\Users\luyan\AppData\Local\Temp\tmpmrb1a3t1TempValida
- **错误行**: 3

**问题 #6** (第 315 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf_ruj4u5TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.sink.MongoSink;
^
C:\Users\luyan\AppData\Local\Temp\tmpf_ruj4u5TempValidation
- **错误行**: 3


### `release\v3.0.0\docs\Flink\pulsar-functions-integration.md`

**问题 #8** (第 217 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp62uu_wzjTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp62u
- **错误行**: 3


### `release\v3.0.0\docs\Flink\pyflink-deep-guide.md`

**问题 #9** (第 388 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2


### `release\v3.0.0\docs\Flink\risingwave-integration-guide.md`

**问题 #6** (第 126 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0epzwmatTempValidation.java:4: 错误: 找不到符号
FlinkKafkaProducer<String> kafkaProducer = new FlinkKafkaProducer<>(
^
  符号:   类 FlinkKafkaProducer
  位置: 类 TempValidation
- **错误行**: 4

**问题 #9** (第 182 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplszj_0v2TempValidation.java:4: 错误: 找不到符号
DebeziumSourceFunction<String> source = DebeziumSourceFunction.<String>builder()
^
  符号:   类 DebeziumSourceFunction
  位置:
- **错误行**: 4

**问题 #10** (第 193 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqd3ivzv9TempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.sqlQuery(
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpqd3ivzv9Te
- **错误行**: 4


### `release\v3.0.0\docs\Flink\state-backends-comparison.md`

**问题 #4** (第 240 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6u96pnhjTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.runtime.state.hashmap.HashMapStateBackend;
^
C:\Users\luyan\AppData\Local\Temp\tmp6u96pnhjTempV
- **错误行**: 3

**问题 #5** (第 273 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    state.backend: hashmap
    ^ (line: 4)
found duplicate key "state.backend" with value "rocksdb" (original value: "hashmap")

- **错误行**: 4

**问题 #6** (第 299 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0da2qi8tTempValidation.java:4: 错误: 非法的表达式开始
public void monitorStateBackend(RuntimeContext ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmp0da2qi8tTempValidation.jav
- **错误行**: 4


### `release\v3.0.0\docs\INTEGRATED-GUIDE.md`

**问题 #3** (第 58 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqsaj7fntTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\KNOWLEDGE-RELATIONSHIP-FINAL-100P-REPORT.md`

**问题 #5** (第 241 行, 语言: python)

- **错误**: SyntaxError: invalid character '✅' (U+2705)
- **错误行**: 4


### `release\v3.0.0\docs\KNOWLEDGE-RELATIONSHIP-RECONSTRUCTION-PLAN.md`

**问题 #5** (第 125 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 2


### `release\v3.0.0\docs\Knowledge\02-design-patterns\pattern-cep-complex-event.md`

**问题 #7** (第 331 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpakovl01nCEPState.java:4: 错误: 找不到符号
    List<NFAState> activeStates;
    ^
  符号:   类 List
  位置: 类 CEPState
C:\Users\luyan\AppData\Local\Temp\tmpakovl01nCEPState.jav
- **错误行**: 4

**问题 #10** (第 447 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb3dhp2xvTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.CEP;
^
C:\Users\luyan\AppData\Local\Temp\tmpb3dhp2xvTempValidation.java:3: 错误: 不是语句
import
- **错误行**: 3

**问题 #11** (第 518 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5f5x3gn1TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp5f5x3gn1TempValidat
- **错误行**: 4

**问题 #12** (第 575 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx4pq83rsTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpx4pq83rsTempValidatio
- **错误行**: 4

**问题 #13** (第 610 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfjra4bc9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpfjra4
- **错误行**: 3

**问题 #14** (第 629 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmlowj8slTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpmlowj8slTempValidatio
- **错误行**: 4

**问题 #15** (第 656 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe1ujplrwTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpe1ujplrwTempValidat
- **错误行**: 4

**问题 #17** (第 738 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp69pxjmyhTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp69p
- **错误行**: 3

**问题 #18** (第 763 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptw2_517pTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmptw2_5
- **错误行**: 3

**问题 #19** (第 779 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpivtp8143TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpivtp8
- **错误行**: 3

**问题 #20** (第 797 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw92h281oTempValidation.java:4: 错误: 找不到符号
Pattern<Event, ?> inefficient = Pattern
^
  符号:   类 Pattern
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpw9
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\02-design-patterns\pattern-log-analysis.md`

**问题 #5** (第 453 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu8xv5z4sTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpu8xv5z4sTempValidat
- **错误行**: 4

**问题 #6** (第 526 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeythi1dyTraceAnalysisFunction.java:2: 错误: 需要 class、interface、enum 或 record
unifiedLogs
^
C:\Users\luyan\AppData\Local\Temp\tmpeythi1dyTraceAnalysisFunction.java:10
- **错误行**: 2

**问题 #7** (第 595 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpez6ytpa2TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpez6ytpa2TempValidat
- **错误行**: 4

**问题 #8** (第 647 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbmuw30x4SlowRequestDetector.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<LatencyMetric> latencyMetrics = unifiedLogs
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luy
- **错误行**: 2


### `release\v3.0.0\docs\Knowledge\02-design-patterns\pattern-realtime-feature-engineering.md`

**问题 #4** (第 346 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu275d_xaSessionAggregator.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Transaction> transactions = ...
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Loc
- **错误行**: 2


### `release\v3.0.0\docs\Knowledge\02-design-patterns\pattern-windowed-aggregation.md`

**问题 #3** (第 466 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa5ep_eo9SumAggregate.java:1: 错误: 从发行版 9 开始, '_' 为关键字, 不能用作标识符
import org.apache.flink.streaming.api.scala._
                                            ^
C:\Users\
- **错误行**: 1

**问题 #4** (第 500 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpseeweg4fAverageAggregate.java:3: 错误: 从发行版 9 开始, '_' 为关键字, 不能用作标识符
  .keyBy(_.sensorId)
         ^
C:\Users\luyan\AppData\Local\Temp\tmpseeweg4fAverageAggregate.jav
- **错误行**: 3

**问题 #10** (第 662 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6zu63f55TopNFunction.java:1: 错误: 需要';'
import org.apache.flink.streaming.api.windowing.triggers.ContinuousTrigger

- **错误行**: 1

**问题 #11** (第 715 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj9qk5cy1TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpj9q
- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\03-business-patterns\data-mesh-streaming-architecture-2026.md`

**问题 #5** (第 372 行, 语言: yaml)

- **错误**: while scanning a block scalar
  in "<unicode string>", line 15, column 19:
        completeness: > 99.9%
                      ^ (line: 15)
expected a comment or a line break, but found '9'
  in "<uni
- **错误行**: 15


### `release\v3.0.0\docs\Knowledge\03-business-patterns\fintech-realtime-risk-control.md`

**问题 #6** (第 277 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmpvy_npoTempValidation.java:4: 错误: 非法的表达式开始
public RiskDecision evaluate(Transaction txn) {
^
C:\Users\luyan\AppData\Local\Temp\tmpmpvy_npoTempValidation.java:28:
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\03-business-patterns\netflix-streaming-pipeline.md`

**问题 #12** (第 357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnffwwolvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnff
- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\03-business-patterns\uber-realtime-platform.md`

**问题 #27** (第 743 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk3j8qc_nSurgePricingJob.java:15: 错误: 非法的表达式开始
        DataStream<DriverEvent> driverEvents = env.addSource(...);

- **错误行**: 15

**问题 #28** (第 881 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmputtc40k2FraudDetectionJob.java:15: 错误: 非法的表达式开始
        DataStream<TripEvent> trips = env.addSource(...);
                                                    ^
C:\
- **错误行**: 15


### `release\v3.0.0\docs\Knowledge\04-technology-selection\engine-selection-guide.md`

**问题 #5** (第 675 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdnp78iczTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpdnp78ic
- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\04-technology-selection\flink-vs-risingwave.md`

**问题 #8** (第 402 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa1e3rfj4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpa1e
- **错误行**: 3

**问题 #10** (第 553 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphduror60TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmphduror60TempValidatio
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\05-mapping-guides\migration-guides\05.1-spark-streaming-to-flink-migration.md`

**问题 #5** (第 166 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnef7_xorTempValidation.java:5: 错误: 找不到符号
env.getConfig().setAutoWatermarkInterval(200);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 5

**问题 #9** (第 245 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbx2g5y94TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpbx
- **错误行**: 3

**问题 #11** (第 288 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi5dfo2z0CountFunction.java:34: 错误: 需要 class、interface、enum 或 record
keyedStream.process(new CountFunction());
^
1 个错误

- **错误行**: 34

**问题 #13** (第 340 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpomqlyoo_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpomq
- **错误行**: 3

**问题 #15** (第 363 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy5pjdkz3TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpy5pjdkz
- **错误行**: 3

**问题 #19** (第 462 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppahnqdnbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmppah
- **错误行**: 3

**问题 #20** (第 479 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpibgsjoknTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpibgsj
- **错误行**: 3

**问题 #21** (第 494 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa8f8ikfsTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpa8f8ikfsTempValidat
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\05-mapping-guides\migration-guides\05.2-kafka-streams-to-flink-migration.md`

**问题 #5** (第 144 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5aw8143aTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5aw8143aTempV
- **错误行**: 3

**问题 #6** (第 167 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv9l3astpTempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #7** (第 180 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt2_liir0TempValidation.java:3: 错误: 找不到符号
        KafkaSource<MyEvent> source = KafkaSource.<MyEvent>builder()
        ^
  符号:   类 KafkaSource
  位置: 类 TempValidatio
- **错误行**: 3

**问题 #8** (第 234 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp316l7pm_TempValidation.java:3: 错误: 找不到符号
        StreamsBuilder builder = new StreamsBuilder();
        ^
  符号:   类 StreamsBuilder
  位置: 类 TempValidation
C:\Users\
- **错误行**: 3

**问题 #9** (第 255 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa1ktezazTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpa1
- **错误行**: 4

**问题 #10** (第 308 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4r44hvppTempValidation.java:3: 错误: 找不到符号
        KTable<String, Long> wordCounts = source
        ^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #11** (第 319 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo3nrc6meCountAggregate.java:6: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Tuple2<String, Long>> wordCounts = source
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 6

**问题 #12** (第 363 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6nq4mpsoTempValidation.java:3: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3

**问题 #13** (第 376 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpftivf0yaTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpftivf0yaTempValidat
- **错误行**: 4

**问题 #21** (第 606 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdpioxp92TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpdpioxp92TempValidat
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\05-mapping-guides\migration-guides\05.3-storm-to-flink-migration.md`

**问题 #1** (第 84 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp71qt5rzhTempValidation.java:4: 错误: 找不到符号
Map<String, Object> state = new HashMap<>();
^
  符号:   类 Map
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp7
- **错误行**: 4

**问题 #2** (第 92 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgx4fx_nwTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpgx4fx_nwTem
- **错误行**: 3

**问题 #4** (第 131 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp76uppzwaTempValidation.java:5: 错误: 找不到符号
    .fieldsGrouping("split", new Fields("word"));
                                 ^
  符号:   类 Fields
  位置: 类 TempValidati
- **错误行**: 5

**问题 #8** (第 208 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1vg10ev6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.functions.AggregateFunction;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #9** (第 263 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpay192jp8SentenceSpout.java:64: 错误: 未命名类 是预览功能，默认情况下禁用。
TopologyBuilder builder = new TopologyBuilder();
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\
- **错误行**: 64

**问题 #10** (第 339 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1iftxlz3WordCount.java:37: 错误: 未命名类 是预览功能，默认情况下禁用。
public static void main(String[] args) throws Exception {
              ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错
- **错误行**: 37

**问题 #12** (第 435 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqbpz9jk4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqbp
- **错误行**: 3

**问题 #14** (第 481 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp1k2808qTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.functions.AggregateFunction;
^
C:\Users\luyan\AppData\Local\Temp\tmpp1k2808qTempVali
- **错误行**: 4

**问题 #23** (第 727 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq9h5l9jyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpq9h
- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\05-mapping-guides\migration-guides\05.4-flink-1x-to-2x-migration.md`

**问题 #4** (第 144 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpii4wce67TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpii4wce67Tem
- **错误行**: 3

**问题 #5** (第 186 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn_38qsdjTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #6** (第 237 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend: rocksdb
    ^ (line: 2)
found duplicate key "state.backend" with value "rocksdb" (original value: "rocksdb")

- **错误行**: 2

**问题 #9** (第 350 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu_3lh00rTempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<String> consumer = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #10** (第 364 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp88q7x47aTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp88q
- **错误行**: 3

**问题 #11** (第 388 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqh8zkxbbTempValidation.java:4: 错误: 找不到符号
FlinkKafkaProducer<String> producer = new FlinkKafkaProducer<>(
^
  符号:   类 FlinkKafkaProducer
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #12** (第 402 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqt5i07xfTempValidation.java:4: 错误: 找不到符号
KafkaSink<String> sink = KafkaSink.<String>builder()
^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #13** (第 420 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnrfs965eTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnrfs965eTemp
- **错误行**: 3

**问题 #14** (第 441 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7ltlfdw6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp7lt
- **错误行**: 3

**问题 #15** (第 463 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfoy7bpafTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpfoy7b
- **错误行**: 3

**问题 #16** (第 481 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpadg12mcuTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpadg12
- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\05-mapping-guides\migration-guides\05.5-batch-to-streaming-migration.md`

**问题 #2** (第 120 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwzqt3h9yTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.api.common.functions.AggregateFunction;
^
C:\Users\luyan\AppData\Local\Temp\tmpwzqt3h9yTempVali
- **错误行**: 4

**问题 #5** (第 185 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9xbk0in2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #6** (第 200 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp55zpcujjTempValidation.java:4: 错误: 找不到符号
List<Data> allData = readAllData();
^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp55zpcujjT
- **错误行**: 4

**问题 #8** (第 234 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp12luu6u3TempValidation.java:4: 错误: 找不到符号
for (Record record : batchData) {
                     ^
  符号:   变量 batchData
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #9** (第 243 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0iic17qbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp0iic1
- **错误行**: 3

**问题 #11** (第 317 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7c6kni78TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp7c6kni78TempValidat
- **错误行**: 4

**问题 #13** (第 359 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj6y4raoiTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpj6y4raoiTempValidat
- **错误行**: 4

**问题 #15** (第 407 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk74p0l1bTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpk74p0l1bTempValidat
- **错误行**: 4

**问题 #16** (第 432 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzhjerfi0TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpzhjerfi0TempValidat
- **错误行**: 4

**问题 #18** (第 469 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp57puomtkDeduplicateFunction.java:39: 错误: 需要 class、interface、enum 或 record
stream.keyBy(e -> e.getUserId() + "_" + e.getEventType())
^
1 个错误

- **错误行**: 39

**问题 #20** (第 528 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz74gpiytTopNFunction.java:37: 错误: 需要 class、interface、enum 或 record
stream.keyBy(ProductSale::getCategory)
^
1 个错误

- **错误行**: 37

**问题 #25** (第 671 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_u5fkk5sTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp_u5fk
- **错误行**: 3

**问题 #26** (第 689 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpimd1i3_fTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpimd1i
- **错误行**: 3

**问题 #27** (第 714 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk3it1_8hTempValidation.java:5: 错误: 找不到符号
    stream,
    ^
  符号:   变量 stream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpk3it1_8hTempValidation.jav
- **错误行**: 5


### `release\v3.0.0\docs\Knowledge\05-mapping-guides\streaming-etl-tools-landscape-2026.md`

**问题 #7** (第 610 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp39we3cchTempValidation.java:4: 错误: 找不到符号
Table orders = tEnv.fromDataStream(
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp39we3cch
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\05-mapping-guides\streaming-sql-engines-2026-comparison.md`

**问题 #12** (第 788 行, 语言: sql)

- **错误**: 可能的语法问题: -- 4. 服务查询需直接查询SINK数据库
-- FLINK SQL本身不提供物化视图查询服务...


### `release\v3.0.0\docs\Knowledge\05-mapping-guides\struct-to-flink-mapping.md`

**问题 #1** (第 205 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk2spox2fTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #2** (第 263 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz0odv2hqTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpz0o
- **错误行**: 3

**问题 #3** (第 310 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbl58sh9zTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpbl58sh9
- **错误行**: 3

**问题 #4** (第 361 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl194c0liTempValidation.java:7: 错误: 找不到符号
env.setStateBackend(new HashMapStateBackend());
                        ^
  符号:   类 HashMapStateBackend
  位置: 类 TempValida
- **错误行**: 7

**问题 #5** (第 402 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3b1rv2woTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp3b1rv
- **错误行**: 3

**问题 #8** (第 513 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4qe0et4tEventTypeInfo.java:23: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Tuple2<String, Integer>> keyedStream = stream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 23

**问题 #9** (第 711 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8i9o2xxcTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #10** (第 777 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplf1ucqhlTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmplf1
- **错误行**: 3

**问题 #11** (第 824 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6gqb174mTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp6gqb174
- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\05-migrations\kafka-streams-to-flink-guide.md`

**问题 #9** (第 470 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi_lfmd82TempValidation.java:4: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #10** (第 486 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_ardv4uwTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp_ardv4uwTempValidat
- **错误行**: 4

**问题 #11** (第 532 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphpxliwm8TempValidation.java:4: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #12** (第 549 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo22odyohTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpo22odyohTempValidat
- **错误行**: 4

**问题 #13** (第 593 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpezh7fq06TempValidation.java:4: 错误: 找不到符号
KStream<String, Click> clicks = builder.stream("clicks");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4

**问题 #14** (第 605 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppi_yerw2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmppi_
- **错误行**: 3

**问题 #15** (第 618 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6d07tykrTempValidation.java:4: 错误: 找不到符号
KTable<Windowed<String>, Long> slidingCounts = clicks
^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #16** (第 628 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnlv7dz94TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnlv
- **错误行**: 3

**问题 #17** (第 641 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm5uq6srqTempValidation.java:4: 错误: 找不到符号
KTable<Windowed<String>, Long> sessionCounts = clicks
^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #18** (第 651 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpojtlry4sTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpojt
- **错误行**: 3

**问题 #21** (第 759 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3y7_fzygTempValidation.java:3: 错误: 找不到符号
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "my-streams-app");
                  ^
  符号:   变量 StreamsConfig
  位
- **错误行**: 3

**问题 #22** (第 766 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzh8kgxzgTempValidation.java:3: 错误: 找不到符号
        env.execute("my-streams-app");  // 作业名称
        ^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 3

**问题 #23** (第 786 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm9uw8snqTempValidation.java:3: 错误: 找不到符号
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092");
                  ^
  符号:   变量 StreamsConfig
  位置
- **错误行**: 3

**问题 #24** (第 794 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqt5j2txuTempValidation.java:3: 错误: 找不到符号
        KafkaSource<String> source = KafkaSource.<String>builder()
        ^
  符号:   类 KafkaSource
  位置: 类 TempValidation

- **错误行**: 3

**问题 #25** (第 814 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp461nq_loTempValidation.java:3: 错误: 找不到符号
        props.put(StreamsConfig.STATE_DIR_CONFIG, "/var/lib/kafka-streams");
                  ^
  符号:   变量 StreamsConfig

- **错误行**: 3

**问题 #26** (第 821 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo2ys65jcTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4

**问题 #27** (第 835 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1vmfi1nxTempValidation.java:4: 错误: 找不到符号
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, "exactly_once_v2");
          ^
  符号:   变量 StreamsConfig
  位置: 类 Temp
- **错误行**: 4

**问题 #28** (第 845 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqaypwjhnTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqaypwjh
- **错误行**: 3

**问题 #29** (第 867 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpms3fxm_fTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpms3fxm_fTempV
- **错误行**: 3

**问题 #32** (第 954 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm12ewc6uTempValidation.java:4: 错误: 找不到符号
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, "exactly_once_v2");
          ^
  符号:   变量 StreamsConfig
  位置: 类 Temp
- **错误行**: 4

**问题 #34** (第 1025 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw_zn1_61TempValidation.java:4: 错误: 找不到符号
KStream<String, Event> repartitioned = events
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #35** (第 1039 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7vjphzmpTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp7vjphzmpTempValidat
- **错误行**: 4

**问题 #37** (第 1117 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeba_m301DualWriteValidation.java:44: 错误: 非法的表达式开始
            .setRecordSerializer(...)
                                 ^
C:\Users\luyan\AppData\Local\Temp\tmpeba
- **错误行**: 44

**问题 #44** (第 1362 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6zkoc9goTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp6zk
- **错误行**: 3

**问题 #47** (第 1461 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa96hnmhnTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpa96hnmhnTempValidat
- **错误行**: 4

**问题 #48** (第 1489 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprvwuf85aTempValidation.java:3: 错误: 找不到符号
        KafkaSource<String> source = KafkaSource.<String>builder()
        ^
  符号:   类 KafkaSource
  位置: 类 TempValidation

- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\06-frontier\a2a-protocol-agent-communication.md`

**问题 #8** (第 355 行, 语言: python)

- **错误**: SyntaxError: 'async for' outside async function
- **错误行**: 8


### `release\v3.0.0\docs\Knowledge\06-frontier\ai-agent-streaming-architecture.md`

**问题 #9** (第 821 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbzpetgx7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpbzp
- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\06-frontier\cloud-edge-continuum.md`

**问题 #5** (第 451 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbdol93exAdaptivePlacement.java:4: 错误: 找不到符号
    Placement decide(Task task, SystemState state) {
                     ^
  符号:   类 Task
  位置: 类 AdaptivePlacement
C:
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\06-frontier\materialize-comparison-guide.md`

**问题 #7** (第 383 行, 语言: sql)

- **错误**: 可能的语法问题: -- 订阅实时变更
COPY (SUBSCRIBE TO MATERIALIZED_VIEW) TO...

**问题 #12** (第 676 行, 语言: sql)

- **错误**: 可能的语法问题: -- 订阅库存变更
COPY (SUBSCRIBE TO CURRENT_INVENTORY) TO...


### `release\v3.0.0\docs\Knowledge\06-frontier\mcp-protocol-agent-streaming.md`

**问题 #11** (第 449 行, 语言: python)

- **错误**: SyntaxError: 'await' outside function
- **错误行**: 41


### `release\v3.0.0\docs\Knowledge\06-frontier\multimodal-ai-streaming-architecture.md`

**问题 #3** (第 160 行, 语言: python)

- **错误**: SyntaxError: invalid decimal literal
- **错误行**: 2

**问题 #7** (第 303 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 57


### `release\v3.0.0\docs\Knowledge\06-frontier\multimodal-streaming-architecture.md`

**问题 #12** (第 391 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 118

**问题 #13** (第 533 行, 语言: java)

- **错误**: 括号不匹配: (=40, )=43

**问题 #14** (第 597 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 55


### `release\v3.0.0\docs\Knowledge\06-frontier\real-time-rag-architecture.md`

**问题 #4** (第 299 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpddmfny7nEmbeddingAsyncFn.java:2: 错误: 找不到符号
class EmbeddingAsyncFn extends AsyncFunction<Document, Vector> {
                               ^
  符号: 类 AsyncFunction

- **错误行**: 2

**问题 #5** (第 313 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp07a6e0wbVectorBulkSink.java:2: 错误: 找不到符号
class VectorBulkSink extends RichSinkFunction<Vector> {
                             ^
  符号: 类 RichSinkFunction
C:\Users\l
- **错误行**: 2


### `release\v3.0.0\docs\Knowledge\06-frontier\realtime-ai-streaming-2026.md`

**问题 #16** (第 588 行, 语言: java)

- **错误**: 括号不匹配: (=37, )=41


### `release\v3.0.0\docs\Knowledge\06-frontier\realtime-data-mesh-practice.md`

**问题 #9** (第 344 行, 语言: sql)

- **错误**: 可能的语法问题: -- 结果: F → E → B → [A, C]...


### `release\v3.0.0\docs\Knowledge\06-frontier\realtime-data-product-architecture.md`

**问题 #13** (第 403 行, 语言: yaml)

- **错误**: while scanning a block scalar
  in "<unicode string>", line 36, column 15:
          target: > 99.999%
                  ^ (line: 36)
expected a comment or a line break, but found '9'
  in "<unicode s
- **错误行**: 36


### `release\v3.0.0\docs\Knowledge\06-frontier\realtime-data-quality-validation.md`

**问题 #5** (第 263 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpol83n_v8TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpol83n_v8TempValidat
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\06-frontier\realtime-digital-twin-streaming.md`

**问题 #5** (第 257 行, 语言: python)

- **错误**: SyntaxError: invalid decimal literal
- **错误行**: 2

**问题 #6** (第 269 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 7


### `release\v3.0.0\docs\Knowledge\06-frontier\risingwave-integration-guide.md`

**问题 #6** (第 482 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphz_f71f3TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmphz
- **错误行**: 4

**问题 #10** (第 602 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppaqqrj7hTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmppaqqrj7hTempValidat
- **错误行**: 4

**问题 #16** (第 818 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2cub8xe5TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp2cub8xe5TempValidat
- **错误行**: 4

**问题 #20** (第 963 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppskutvuyTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmppskutvuyTempValidat
- **错误行**: 4

**问题 #31** (第 1381 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 7, column 1:
    flink savepoint <job-id>
    ^ (line: 7)
- **错误行**: 7


### `release\v3.0.0\docs\Knowledge\06-frontier\rust-streaming-ecosystem.md`

**问题 #13** (第 755 行, 语言: sql)

- **错误**: 可能的语法问题: -- 返回: 10000.00 (严格串行化保证)

-- 即使在高并发写入下，也不会读到中间状态
...


### `release\v3.0.0\docs\Knowledge\06-frontier\streaming-access-control.md`

**问题 #9** (第 670 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppiaytspeLineageTracker.java:4: 错误: 找不到符号
    void track(DataRecord record, Operator op) {
               ^
  符号:   类 DataRecord
  位置: 类 LineageTracker
C:\Users\luy
- **错误行**: 4

**问题 #13** (第 777 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph204lkzbLineageTrackingFunction.java:2: 错误: 找不到符号
class LineageTrackingFunction extends ProcessFunction<Record, Record> {
                                      ^

- **错误行**: 2


### `release\v3.0.0\docs\Knowledge\06-frontier\streaming-database-ecosystem-comparison.md`

**问题 #6** (第 517 行, 语言: sql)

- **错误**: 可能的语法问题: -- 图遍历递归（有限支持）
   WITH RECURSIVE PATHS AS (...)...


### `release\v3.0.0\docs\Knowledge\06-frontier\streaming-graph-processing-tgn.md`

**问题 #7** (第 347 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy0jv1jgfTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.graph.streaming.*;
^
C:\Users\luyan\AppData\Local\Temp\tmpy0jv1jgfTempValidation.java:3: 错误: 需要
- **错误行**: 3

**问题 #8** (第 399 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 65


### `release\v3.0.0\docs\Knowledge\06-frontier\streaming-materialized-view-architecture.md`

**问题 #7** (第 369 行, 语言: sql)

- **错误**: 可能的语法问题: -- 自动增量更新
-- 当SALES表发生INSERT/UPDATE/DELETE时，物化视图自动...


### `release\v3.0.0\docs\Knowledge\06-frontier\streaming-security-compliance.md`

**问题 #5** (第 446 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_hvsnwcgTempValidation.java:3: 错误: 不是语句
KafkaServer {
^
C:\Users\luyan\AppData\Local\Temp\tmp_hvsnwcgTempValidation.java:3: 错误: 需要';'
KafkaServer {
           ^
C:
- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\06-frontier\streaming-slo-definition.md`

**问题 #4** (第 297 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp19kz0iekTempValidation.java:4: 错误: 找不到符号
Counter slo_violations_total = Counter.build()
^
  符号:   类 Counter
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #7** (第 382 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 5


### `release\v3.0.0\docs\Knowledge\06-frontier\temporal-flink-layered-architecture.md`

**问题 #9** (第 621 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0udtt3w7TemporalStateLookup.java:5: 错误: 未命名类 是预览功能，默认情况下禁用。
public WorkflowState getWorkflowState() {
       ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 5


### `release\v3.0.0\docs\Knowledge\06-frontier\wasm-dataflow-patterns.md`

**问题 #26** (第 1398 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi89mkzi6WasmMapFunction.java:22: 错误: 非法的表达式开始
        byte[] state = getRuntimeContext().getState(...).value();

- **错误行**: 22

**问题 #50** (第 2355 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmuch4u2iWasmScalarFunction.java:12: 错误: 需要';'
    private val runtime = new WasmUdfRuntime()
                                              ^
C:\Users\luyan\AppData
- **错误行**: 12


### `release\v3.0.0\docs\Knowledge\06-frontier\web3-blockchain-streaming-architecture.md`

**问题 #7** (第 374 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqe3cgdweTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpqe3cgdweTempValidatio
- **错误行**: 4

**问题 #8** (第 423 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi0ui3k_0TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpi0ui3k_0TempValidat
- **错误行**: 4

**问题 #9** (第 486 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpezgmoukvTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpezgmoukvTempValidat
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\07-best-practices\07.01-flink-production-checklist.md`

**问题 #3** (第 223 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7knanxuiTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000); // 1分钟间隔
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp7kna
- **错误行**: 4

**问题 #4** (第 249 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp04kuf4qzTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp04k
- **错误行**: 3

**问题 #7** (第 374 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5j063rb4TempValidation.java:4: 错误: 非法的表达式开始
private static final Logger LOG = LoggerFactory.getLogger(MyFunction.class);
^
C:\Users\luyan\AppData\Local\Temp\tmp5j0
- **错误行**: 4

**问题 #11** (第 562 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo5lwhsnsTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(10000);  // 10s 间隔
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpo5
- **错误行**: 4

**问题 #12** (第 573 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt2l15qq0TempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(300000);  // 5min 间隔
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\07-best-practices\07.02-performance-tuning-patterns.md`

**问题 #9** (第 352 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwz08mtrvTempValidation.java:10: 错误: 需要';'
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


### `release\v3.0.0\docs\Knowledge\07-best-practices\07.04-cost-optimization-patterns.md`

**问题 #8** (第 347 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz4u2lh18TempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #9** (第 366 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 20


### `release\v3.0.0\docs\Knowledge\07-best-practices\07.05-security-hardening-guide.md`

**问题 #3** (第 213 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    security.kerberos.login.keytab:  ...
    ^ (line: 4)
found duplicate key "security.kerberos.login.contexts" with value "Cli
- **错误行**: 4

**问题 #13** (第 532 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpin7pjickTempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\07-best-practices\07.07-testing-strategies-complete.md`

**问题 #4** (第 142 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkc__hhsdTempValidation.java:5: 错误: 需要';'
public void badTest() {
                   ^
C:\Users\luyan\AppData\Local\Temp\tmpkc__hhsdTempValidation.java:12: 错误: 需要';
- **错误行**: 5

**问题 #6** (第 232 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeic2urq8TempValidation.java:5: 错误: 需要';'
public void flakyTest() {
                     ^
C:\Users\luyan\AppData\Local\Temp\tmpeic2urq8TempValidation.java:13: 错误:
- **错误行**: 5

**问题 #7** (第 259 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgradyv4mStatefulCounterTest.java:33: 错误: 需要')'或','
        harness.setup(new HashMapStateBackend()  // MemoryStateBackend已弃用，使用HashMapStateBackend

- **错误行**: 33


### `release\v3.0.0\docs\Knowledge\08-standards\streaming-data-governance.md`

**问题 #6** (第 203 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgm1brta3TempValidation.java:5: 错误: 不是语句
  "type": "record",
  ^
C:\Users\luyan\AppData\Local\Temp\tmpgm1brta3TempValidation.java:5: 错误: 需要';'
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

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe4y58ue6MaskPII.java:18: 错误: 需要 class、interface、enum 或 record
SELECT
^
C:\Users\luyan\AppData\Local\Temp\tmpe4y58ue6MaskPII.java:20: 错误: 未结束的字符文字
    MaskPII(email
- **错误行**: 18


### `release\v3.0.0\docs\Knowledge\08-standards\streaming-security-compliance.md`

**问题 #7** (第 491 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk4ogzpufTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpk4ogzpufTemp
- **错误行**: 3

**问题 #10** (第 603 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph6wxbt1wTempValidation.java:4: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmph6
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\10-case-studies\CODE-RUNNABILITY-NOTES.md`

**问题 #1** (第 28 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0abtmygmTempValidation.java:5: 错误: 找不到符号
env.setParallelism(100);  // 原为100，可根据TaskManager数量调整
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 5

**问题 #2** (第 59 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpthjtfgyzTempValidation.java:5: 错误: 找不到符号
options.setConnectionTimeout(10);  // 网络不稳定时可增大
^
  符号:   变量 options
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 5

**问题 #3** (第 87 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt5ty7w3_TempValidation.java:5: 错误: 非法的表达式开始
kieFileSystem.write("src/main/resources/rules/fraud-rules.drl", ...)

- **错误行**: 5


### `release\v3.0.0\docs\Knowledge\10-case-studies\ecommerce\10.2.3-big-promotion-realtime-dashboard.md`

**问题 #19** (第 1529 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 9, column 12:
      websocket: {
               ^ (line: 9)
- **错误行**: 9
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `release\v3.0.0\docs\Knowledge\10-case-studies\finance\10.1.1-realtime-anti-fraud-system.md`

**问题 #3** (第 328 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkf0_ambeRealtimeAntiFraudEngine.java:196: 错误: 未命名变量 是预览功能，默认情况下禁用。
                .whenComplete((_, error) -> {
                               ^
  （请使用 --enable-p
- **错误行**: 196


### `release\v3.0.0\docs\Knowledge\10-case-studies\finance\10.1.4-realtime-payment-risk-control.md`

**问题 #8** (第 1027 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp047y6c2uRealtimePaymentRiskControlEngine.java:254: 错误: 未命名变量 是预览功能，默认情况下禁用。
                .whenComplete((_, error) -> {
                               ^
  （请使用 -
- **错误行**: 254

**问题 #9** (第 1420 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp08q6q1emTempValidation.java:4: 错误: 需要';'
       .withIdleness(Duration.ofMinutes(1))
                                           ^
1 个错误

- **错误行**: 4

**问题 #10** (第 1436 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkslizlijTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpksl
- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\10-case-studies\finance\10.1.5-realtime-risk-control-platform.md`

**问题 #18** (第 1302 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmper9yaw9xTempValidation.java:4: 错误: 找不到符号
RocksDBStateBackend backend = new RocksDBStateBackend(checkpointPath, true);
^
  符号:   类 RocksDBStateBackend
  位置: 类 TempV
- **错误行**: 4

**问题 #19** (第 1324 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw9eztidcTempValidation.java:5: 错误: 找不到符号
    input,
    ^
  符号:   变量 input
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpw9eztidcTempValidation.java:
- **错误行**: 5

**问题 #21** (第 1386 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq2_hyxmrTempValidation.java:5: 错误: 需要';'
public String getKey(TransactionEvent event) {
                    ^
C:\Users\luyan\AppData\Local\Temp\tmpq2_hyxmrTempVali
- **错误行**: 5

**问题 #25** (第 1468 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8zvvf0odTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8zvvf0odTem
- **错误行**: 3

**问题 #26** (第 1481 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4u5fqrk7TempValidation.java:7: 错误: 找不到符号
       log.error("Process failed for event: {}", event, e);
                                                 ^
  符号:   变量
- **错误行**: 7

**问题 #27** (第 1494 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprjve10sgTempValidation.java:4: 错误: 需要';'
   public void close() {
                    ^
1 个错误

- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\10-case-studies\iot\10.3.1-smart-manufacturing.md`

**问题 #4** (第 359 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptjt2ef3eTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmptjt2ef3eTempValidatio
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\10-case-studies\iot\10.3.3-predictive-maintenance-manufacturing.md`

**问题 #5** (第 649 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdj77h7qjTimeSeriesFeatureExtractor.java:6: 错误: 程序包org.apache.flink.api.common.state不存在
import org.apache.flink.api.common.state.ValueState;

- **错误行**: 6


### `release\v3.0.0\docs\Knowledge\10-case-studies\iot\10.3.5-smart-manufacturing-iot.md`

**问题 #13** (第 1419 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp75obu6cbTempValidation.java:4: 错误: 找不到符号
OpcUaClient client = OpcUaClient.create(
^
  符号:   类 OpcUaClient
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #14** (第 1463 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi_ov4bflTempValidation.java:4: 错误: 找不到符号
DefaultConfigurableOptionsFactory optionsFactory =
^
  符号:   类 DefaultConfigurableOptionsFactory
  位置: 类 TempValidation
C:
- **错误行**: 4

**问题 #17** (第 1577 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphhb6bapbTimestampNormalizer.java:21: 错误: 需要 class、interface、enum 或 record
sensorReading.setTimestamp(
^
1 个错误

- **错误行**: 21

**问题 #18** (第 1629 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbbv34o7_TempValidation.java:4: 错误: 找不到符号
   producer.send(record);  // 错误
                 ^
  符号:   变量 record
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #19** (第 1641 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuex_h4g8TempValidation.java:4: 错误: 找不到符号
   HikariConfig config = new HikariConfig();
   ^
  符号:   类 HikariConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #20** (第 1650 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3ydmhz1wTempValidation.java:4: 错误: 找不到符号
   ByteBuffer directBuffer = ByteBuffer.allocateDirect(1024 * 1024);
   ^
  符号:   类 ByteBuffer
  位置: 类 TempValidation
C:\U
- **错误行**: 4

**问题 #22** (第 1688 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqhmj0yofTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqhmj0
- **错误行**: 3

**问题 #23** (第 1702 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeg140v22TempValidation.java:4: 错误: 找不到符号
   try (OrtSession session = createSession()) {
        ^
  符号:   类 OrtSession
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #24** (第 1711 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4lz4nyihTempValidation.java:4: 错误: 有 'catch', 但是没有 'try'
   catch (Exception e) {
   ^
1 个错误

- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\98-exercises\exercise-02-flink-basics.md`

**问题 #2** (第 94 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeub3colcTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpeub
- **错误行**: 3

**问题 #3** (第 170 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7nd_hiilWordCount.java:205: 错误: 需要 class、interface、enum 或 record
*/
^
1 个错误

- **错误行**: 205

**问题 #5** (第 439 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp87g8_tacTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp87g8_
- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\98-exercises\exercise-03-checkpoint-analysis.md`

**问题 #1** (第 60 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1katdemdTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1katdem
- **错误行**: 3

**问题 #5** (第 381 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyzghg856UnalignedCheckpointConfig.java:30: 错误: 需要 class、interface、enum 或 record
env.getCheckpointConfig().enableUnalignedCheckpoints();
^
C:\Users\luyan\AppData\Lo
- **错误行**: 30


### `release\v3.0.0\docs\Knowledge\98-exercises\exercise-05-pattern-implementation.md`

**问题 #1** (第 60 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5ymv5e14TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5ymv5
- **错误行**: 3

**问题 #2** (第 155 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprcaer_drOrderEvent.java:121: 错误: 需要 class、interface、enum 或 record
import org.apache.flink.cep.CEP;
^
C:\Users\luyan\AppData\Local\Temp\tmprcaer_drOrderEvent.java:1
- **错误行**: 121


### `release\v3.0.0\docs\Knowledge\98-exercises\quick-ref-security-compliance.md`

**问题 #8** (第 296 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplsc52o_mTempValidation.java:18: 错误: 需要';'
""")
    ^
C:\Users\luyan\AppData\Local\Temp\tmplsc52o_mTempValidation.java:29: 错误: 需要';'
""")
    ^
2 个错误

- **错误行**: 18


### `release\v3.0.0\docs\Knowledge\98-exercises\quick-ref-temporal-flink.md`

**问题 #8** (第 369 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphc7b3k46TemporalStateLookup.java:3: 错误: 未命名类 是预览功能，默认情况下禁用。
public WorkflowState getWorkflowState() {
       ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.01-flink-2x-architecture.md`

**问题 #3** (第 292 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq6mue93oTempValidation.java:4: 错误: 找不到符号
   state.getAsync(key)
                  ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpq6mu
- **错误行**: 4

**问题 #5** (第 329 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkm3juk2xTempValidation.java:4: 错误: 找不到符号
if (backpressureRatio > 0.5 && latencyP99 > targetLatency) {
    ^
  符号:   变量 backpressureRatio
  位置: 类 TempValidation
C:\
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.02-flink-runtime-deep-dive.md`

**问题 #15** (第 532 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpotxkablvTempValidation.java:8: 错误: 非法的表达式开始
public void notifyCreditAvailable() {
^
C:\Users\luyan\AppData\Local\Temp\tmpotxkablvTempValidation.java:30: 错误: 需要 cla
- **错误行**: 8

**问题 #17** (第 603 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqnwv34g4TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.03-flink-state-backends.md`

**问题 #9** (第 302 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8bleysyxTempValidation.java:4: 错误: 不是语句
state.backend.rocksdb.writebuffer.size: 64mb
                                 ^
C:\Users\luyan\AppData\Local\Temp\tmp8bleys
- **错误行**: 4

**问题 #10** (第 318 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8za9efu6TempValidation.java:5: 错误: 不是语句
state.backend.rocksdb.memory.managed: true
                            ^
C:\Users\luyan\AppData\Local\Temp\tmp8za9efu6TempV
- **错误行**: 5

**问题 #16** (第 479 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnrwdj03mTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #18** (第 535 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdw6yxvklTempValidation.java:4: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend = new EmbeddedRocksDBStateBackend(true);  // true=增量 Checkpoint
^
  符号:   类 Emb
- **错误行**: 4

**问题 #20** (第 587 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv82fz6cuTempValidation.java:4: 错误: 找不到符号
ForStStateBackendConfig forstConfig = ForStStateBackendConfig.builder()
^
  符号:   类 ForStStateBackendConfig
  位置: 类 TempVa
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.04-flink-sql-table-api.md`

**问题 #6** (第 138 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpexpjywwpTempValidation.java:4: 错误: 找不到符号
env.setRuntimeMode(RuntimeExecutionMode.STREAMING);
                   ^
  符号:   变量 RuntimeExecutionMode
  位置: 类 TempValid
- **错误行**: 4

**问题 #8** (第 282 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0k3mj77tTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.functions.AggregateFunction;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #9** (第 306 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiaea7go1TempValidation.java:4: 错误: 非法的表达式开始
Filter -> Scan  =>  Scan(with Filter)
                 ^
C:\Users\luyan\AppData\Local\Temp\tmpiaea7go1TempValidation.ja
- **错误行**: 4

**问题 #10** (第 319 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1rmixh5oTempValidation.java:4: 错误: 需要';'
A JOIN B JOIN C  =>  选择代价最低的 Join 顺序
      ^
C:\Users\luyan\AppData\Local\Temp\tmp1rmixh5oTempValidation.java:4: 错误: 需要';'
- **错误行**: 4

**问题 #11** (第 346 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_xnjkgtaMLPredictUDF.java:11: 错误: 需要 class、interface、enum 或 record
AsyncFunction 调用 REST API，延迟 10-100ms
^
C:\Users\luyan\AppData\Local\Temp\tmp_xnjkgtaMLPredictUD
- **错误行**: 11

**问题 #13** (第 427 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfc7zjsbqTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.Table;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpfc7zjsbqTempValidation.
- **错误行**: 3

**问题 #15** (第 513 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnh8vejy6TempValidation.java:4: 错误: 找不到符号
TableConfig config = tableEnv.getConfig();
^
  符号:   类 TableConfig
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4

**问题 #17** (第 597 行, 语言: sql)

- **错误**: 可能的语法问题: -- 4. 模型性能监控
DESCRIBE MODEL METRICS FRAUD_DETECTIO...; 可能的语法问题: -- 显示: AVG_INFERENCE_LATENCY, THROUGHPUT, ERROR_RA...

**问题 #18** (第 673 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp47657goaTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp476
- **错误行**: 3

**问题 #19** (第 715 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj062elsaTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\02-flink-system\02.05-flink-cloud-native.md`

**问题 #7** (第 290 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmvynqsf3TempValidation.java:4: 错误: 找不到符号
if (backpressureRatio > scaleUpThreshold ||
    ^
  符号:   变量 backpressureRatio
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\03-scala-rust-interop\03.01-wasm-interop.md`

**问题 #8** (第 305 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp40xornj1TempValidation.java:4: 错误: 非法的表达式开始
public record Input(long id, byte[] payload) {}
^
C:\Users\luyan\AppData\Local\Temp\tmp40xornj1TempValidation.java:7: 错
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\04-rust-engines\04.02-risingwave-deep-dive.md`

**问题 #9** (第 487 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7bfcgvdpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp7bf
- **错误行**: 3


### `release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\04-rust-engines\04.03-materialize-analysis.md`

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


### `release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\05-architecture-patterns\05.01-hybrid-architecture-patterns.md`

**问题 #5** (第 389 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 42, column 33:
                  output: STRUCT<ltv: DOUBLE, churn_risk: DOUBLE>
                                    ^ (line: 42)
- **错误行**: 42
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\src-analysis\flink-checkpoint-source.md`

**问题 #3** (第 91 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjirlrnthTempValidation.java:3: 错误: 非法的表达式开始
public CompletableFuture<CompletedCheckpoint> triggerCheckpoint(
^
C:\Users\luyan\AppData\Local\Temp\tmpjirlrnthTempVal
- **错误行**: 3

**问题 #4** (第 180 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpc3m2tp4qTempValidation.java:3: 错误: 非法的表达式开始
public boolean receiveAcknowledgeMessage(
^
C:\Users\luyan\AppData\Local\Temp\tmpc3m2tp4qTempValidation.java:69: 错误: 需要
- **错误行**: 3

**问题 #5** (第 258 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj4k8paccPendingCheckpoint.java:56: 错误: 非法的表达式开始
                        k -> new OperatorState(operatorId, ...));

- **错误行**: 56

**问题 #13** (第 794 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    execution.checkpointing.interval ...
    ^ (line: 4)
found duplicate key "execution.checkpointing.interval" with value "30s
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\src-analysis\flink-network-stack.md`

**问题 #10** (第 805 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp08bn6imuBlockingBackPressure.java:4: 错误: 非法的类型开始
    public void emitRecord(...) {
                           ^
C:\Users\luyan\AppData\Local\Temp\tmp08bn6imuBlocki
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\src-analysis\flink-runtime-architecture.md`

**问题 #3** (第 74 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf1x7r9tbTempValidation.java:3: 错误: 非法的表达式开始
private void startJobExecution() {
^
C:\Users\luyan\AppData\Local\Temp\tmpf1x7r9tbTempValidation.java:27: 错误: 需要 class、
- **错误行**: 3

**问题 #4** (第 101 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu9a0xa40TempValidation.java:4: 错误: 需要';'
public void notifyAllocationFailure(
                                   ^
C:\Users\luyan\AppData\Local\Temp\tmpu9a0xa40Tem
- **错误行**: 4

**问题 #7** (第 181 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwqm4b0_7TempValidation.java:4: 错误: 需要';'
public CompletableFuture<Acknowledge> requestSlot(
                                                 ^
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #8** (第 218 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo1qespdvTempValidation.java:3: 错误: 非法的表达式开始
protected abstract CompletableFuture<WorkerType> requestNewWorker(
^
C:\Users\luyan\AppData\Local\Temp\tmpo1qespdvTempV
- **错误行**: 3

**问题 #11** (第 311 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnc68wjm2TempValidation.java:4: 错误: 需要';'
public CompletableFuture<Acknowledge> submitJob(
                                               ^
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #12** (第 350 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzxx_nuskTempValidation.java:3: 错误: 非法的表达式开始
private void onJobManagerRunnerComplete(
^
C:\Users\luyan\AppData\Local\Temp\tmpzxx_nuskTempValidation.java:33: 错误: 需要
- **错误行**: 3

**问题 #17** (第 528 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_qba4so5TempValidation.java:3: 错误: 非法的表达式开始
public ExecutionGraph buildExecutionGraph(JobGraph jobGraph) {
^
C:\Users\luyan\AppData\Local\Temp\tmp_qba4so5TempValid
- **错误行**: 3

**问题 #18** (第 632 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjmc_mq7rPipelinedRegionScheduler.java:1: 错误: 未命名类 是预览功能，默认情况下禁用。
public SchedulerNG createScheduler(
       ^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 1

**问题 #19** (第 718 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzlijeg1yJobManager.java:8: 错误: 找不到符号
    SchedulerNG scheduler;  // 可插拔调度器
    ^
  符号:   类 SchedulerNG
  位置: 类 JobMaster
C:\Users\luyan\AppData\Local\Temp\tmpzlije
- **错误行**: 8

**问题 #21** (第 785 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnelk0dsnSlotPoolImpl.java:5: 错误: 找不到符号
    private void requestSlotsBatch(List<SlotRequest> requests) {
                                   ^
  符号:   类 List
  位置: 类
- **错误行**: 5


### `release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\src-analysis\flink-taskmanager-deep-dive.md`

**问题 #3** (第 97 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6gas5x1rTempValidation.java:4: 错误: 需要';'
public CompletableFuture<Acknowledge> submitTask(
                                                ^
C:\Users\luyan\AppData
- **错误行**: 4

**问题 #4** (第 177 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwvzh1vdbTempValidation.java:4: 错误: 需要';'
public CompletableFuture<Acknowledge> freeSlot(
                                              ^
C:\Users\luyan\AppData\Loc
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\case-studies\ecommerce-realtime-recommendation-v2.md`

**问题 #2** (第 253 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv_u4tq9bTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpv_u4tq9bTempValidat
- **错误行**: 4

**问题 #3** (第 317 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmtwt13lzAsyncModelInference.java:47: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Prediction> predictions = featureStream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 47


### `release\v3.0.0\docs\Knowledge\case-studies\finance\realtime-anti-fraud-system-case.md`

**问题 #2** (第 198 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph3kltf64TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmph3kltf64TempValidat
- **错误行**: 4

**问题 #3** (第 265 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp96vc7pkkTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp96vc7pkkTempValidat
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\case-studies\fraud-detection-production-case.md`

**问题 #2** (第 262 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr2oxkl09TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpr2oxkl09TempValidatio
- **错误行**: 4

**问题 #3** (第 371 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptwf201rxGNNInferenceFunction.java:92: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<TransactionWithRisk> gnnScores = transactions
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 92


### `release\v3.0.0\docs\Knowledge\case-studies\gaming-analytics-platform-case.md`

**问题 #2** (第 281 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi8h_vvkqTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpi8h_vvkqTempValidat
- **错误行**: 4

**问题 #3** (第 410 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaybiezr9ABTestAssignment.java:53: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<ABTestResult> abResults = eventsWithVariant
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 53


### `release\v3.0.0\docs\Knowledge\case-studies\gaming\realtime-game-analytics-case.md`

**问题 #2** (第 182 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf32_cyp3TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpf32_cyp3TempValidat
- **错误行**: 4

**问题 #4** (第 331 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy66f_cwfTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpy66f_cwfTempValidatio
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\case-studies\iot-smart-grid-case-study.md`

**问题 #2** (第 268 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfxlcccqjTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpfxlcccqjTempValidat
- **错误行**: 4

**问题 #3** (第 352 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphhvqb4ciTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmphhvqb4ciTempValidat
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\cep-complete-tutorial.md`

**问题 #4** (第 229 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4h4kbiyyTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.Pattern;
^
C:\Users\luyan\AppData\Local\Temp\tmp4h4kbiyyTempValidation.java:3: 错误: 不是语句
imp
- **错误行**: 3

**问题 #5** (第 285 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsd1yduwdTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpsd1yduwdTempValidatio
- **错误行**: 4

**问题 #6** (第 330 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjd64y73uTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpjd64y73uTempValidatio
- **错误行**: 4


### `release\v3.0.0\docs\Knowledge\kafka-streams-migration.md`

**问题 #6** (第 145 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqy0rpn51TempValidation.java:3: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3

**问题 #7** (第 158 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5zrs_jw8TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp5zrs_jw8TempValidat
- **错误行**: 4

**问题 #8** (第 185 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw9um9vr8TempValidation.java:3: 错误: 找不到符号
        KTable<Windowed<String>, Long> counts = orders
        ^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3


### `release\v3.0.0\docs\POSITIONING.md`

**问题 #5** (第 218 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_mmieq42TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp_mmieq4
- **错误行**: 3


### `release\v3.0.0\docs\PRACTICAL-EXAMPLES.md`

**问题 #2** (第 43 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcf86hgv2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpcf8
- **错误行**: 3

**问题 #3** (第 59 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprmfafleaTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmprmf
- **错误行**: 3

**问题 #4** (第 77 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp07kkdq56TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp07kkd
- **错误行**: 3


### `release\v3.0.0\docs\Struct\01-foundation\01.04-dataflow-model-formalization.md`

**问题 #1** (第 392 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgjzc_04gTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpgjz
- **错误行**: 3


### `release\v3.0.0\docs\Struct\01-foundation\01.07-session-types.md`

**问题 #6** (第 357 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2


### `release\v3.0.0\docs\Struct\02-properties\02.01-determinism-in-streaming.md`

**问题 #3** (第 497 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiowi9kcsTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpiow
- **错误行**: 3

**问题 #4** (第 533 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpglqreonvTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpglqreonvTempValidat
- **错误行**: 4

**问题 #5** (第 556 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkuspwp78TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpkus
- **错误行**: 3

**问题 #6** (第 574 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_929vs25TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp_929vs25TempValidat
- **错误行**: 4


### `release\v3.0.0\docs\Struct\02-properties\02.02-consistency-hierarchy.md`

**问题 #1** (第 656 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe72qzgydTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpe72
- **错误行**: 3

**问题 #3** (第 730 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgggtxr4nHttpSink.java:1: 错误: 找不到符号
class HttpSink implements SinkFunction<Record> {
                          ^
  符号: 类 SinkFunction
C:\Users\luyan\AppData\Local\T
- **错误行**: 1

**问题 #4** (第 752 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbmeeyxsuEagerKafkaSource.java:1: 错误: 找不到符号
class EagerKafkaSource implements SourceFunction<Record> {
                                  ^
  符号: 类 SourceFunction
C:
- **错误行**: 1


### `release\v3.0.0\docs\Struct\02-properties\02.03-watermark-monotonicity.md`

**问题 #1** (第 315 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpri4pvmphTempValidation.java:4: 错误: 非法的表达式开始
public void onWatermark(Watermark wm, Context ctx, Collector<Out> out) {
^
C:\Users\luyan\AppData\Local\Temp\tmpri4pvmp
- **错误行**: 4


### `release\v3.0.0\docs\Struct\03-relationships\03.02-flink-to-process-calculus.md`

**问题 #1** (第 418 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphmccw028TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmphmc
- **错误行**: 3

**问题 #3** (第 492 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7di8wocoTempValidation.java:4: 错误: 找不到符号
countState.update(countState.value() + 1);
                  ^
  符号:   变量 countState
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 4


### `release\v3.0.0\docs\Struct\03-relationships\03.05-cross-model-mappings.md`

**问题 #6** (第 557 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvipnxr23TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpvip
- **错误行**: 3


### `release\v3.0.0\docs\Struct\04-proofs\04.02-flink-exactly-once-correctness.md`

**问题 #5** (第 732 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnyeldxziTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnye
- **错误行**: 3

**问题 #6** (第 774 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkako849_TempValidation.java:4: 错误: 找不到符号
StreamingFileSink<Result> sink = StreamingFileSink
^
  符号:   类 StreamingFileSink
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4

**问题 #7** (第 797 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcj8s28bwCounterSink.java:2: 错误: 找不到符号
class CounterSink implements SinkFunction<Event> {
                             ^
  符号: 类 SinkFunction
C:\Users\luyan\AppData
- **错误行**: 2

**问题 #8** (第 823 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsq0ejy7uEagerKafkaSource.java:2: 错误: 找不到符号
class EagerKafkaSource implements SourceFunction<Record> {
                                  ^
  符号: 类 SourceFunction
C:
- **错误行**: 2


### `release\v3.0.0\docs\Struct\04-proofs\04.04-watermark-algebra-formal-proof.md`

**问题 #2** (第 781 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbcd579v6TempValidation.java:4: 错误: 找不到符号
Watermark currentOutput = mergeAllInputWatermarks();
^
  符号:   类 Watermark
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4

**问题 #5** (第 1131 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpom7hsxubTempValidation.java:3: 错误: 非法的表达式开始
public void onWatermark(Watermark wm, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpom7hsxubTempValidation.java
- **错误行**: 3

**问题 #6** (第 1209 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwhdnth8pTempValidation.java:3: 错误: 非法的表达式开始
public void onWatermark(Watermark wm, Context ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpwhdnth8pTempValidation.java
- **错误行**: 3


### `release\v3.0.0\docs\Struct\04-proofs\04.07-deadlock-freedom-choreographic.md`

**问题 #1** (第 246 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmperjqsrgkBuyTicket.java:2: 错误: 需要'{'
class BuyTicket@Buyer,Seller {
               ^
C:\Users\luyan\AppData\Local\Temp\tmperjqsrgkBuyTicket.java:2: 错误: 需要 class、int
- **错误行**: 2

**问题 #9** (第 932 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp97be7j4eRequestResponse.java:1: 错误: 需要'{'
class RequestResponse@Client,Server {
                     ^
C:\Users\luyan\AppData\Local\Temp\tmp97be7j4eRequestResponse
- **错误行**: 1

**问题 #10** (第 952 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcrjwtap3ClientRequestResponse.java:3: 错误: 找不到符号
        sendToServer(request);
        ^
  符号:   方法 sendToServer(String)
  位置: 类 ClientRequestResponse
C:\Users\luy
- **错误行**: 3

**问题 #11** (第 963 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp814aszipServerRequestResponse.java:3: 错误: 找不到符号
        String request = receiveFromClient();
                         ^
  符号:   方法 receiveFromClient()
  位置: 类 Ser
- **错误行**: 3

**问题 #12** (第 987 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8tuzej88Auction.java:1: 错误: 需要'{'
class Auction@Buyer,Seller,Arbiter {
             ^
C:\Users\luyan\AppData\Local\Temp\tmp8tuzej88Auction.java:1: 错误: 需要 class、int
- **错误行**: 1


### `release\v3.0.0\docs\Struct\06-frontier\06.02-choreographic-streaming-programming.md`

**问题 #8** (第 541 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6304tqixTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp630
- **错误行**: 3

**问题 #14** (第 694 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprhqjw6rsJoinOp.java:11: 错误: 不是语句
            select {
            ^
C:\Users\luyan\AppData\Local\Temp\tmprhqjw6rsJoinOp.java:11: 错误: 需要';'
            select {

- **错误行**: 11


### `release\v3.0.0\docs\Struct\Model-Selection-Decision-Tree.md`

**问题 #6** (第 388 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb0f231q3TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpb0f231q3TempValidatio
- **错误行**: 4


### `release\v3.0.0\docs\Struct\Proof-Chains-Consistency-Hierarchy.md`

**问题 #2** (第 725 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa387ojwvTempValidation.java:5: 错误: 找不到符号
    .<ClickEvent>forBoundedOutOfOrderness(Duration.ofMinutes(1))
      ^
  符号:   类 ClickEvent
  位置: 类 TempValidation
C:\Us
- **错误行**: 5

**问题 #3** (第 750 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprecvgqycTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmprecvgqy
- **错误行**: 3


### `release\v3.0.0\docs\Struct\Proof-Chains-Dataflow-Foundation.md`

**问题 #2** (第 611 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnizxxmg8TempValidation.java:4: 错误: 找不到符号
StreamGraph streamGraph = env.getStreamGraph();
^
  符号:   类 StreamGraph
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loca
- **错误行**: 4

**问题 #3** (第 636 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpugpnmtzwTempValidation.java:4: 错误: 找不到符号
CheckpointCoordinator.triggerCheckpoint(timestamp);
                                        ^
  符号:   变量 timestamp
  位置: 类
- **错误行**: 4

**问题 #4** (第 648 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp21e8ey5dTempValidation.java:9: 错误: 找不到符号
    .aggregate(aggregateFunction); // 状态算子结合律检查
               ^
  符号:   变量 aggregateFunction
  位置: 类 TempValidation
C:\Us
- **错误行**: 9

**问题 #5** (第 662 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcc4_qariPureMapFunction.java:17: 错误: 需要 class、interface、enum 或 record
stream.assignTimestampsAndWatermarks(
^
C:\Users\luyan\AppData\Local\Temp\tmpcc4_qariPureMapF
- **错误行**: 17

**问题 #6** (第 707 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpn890uoufTempValidation.java:4: 错误: 需要';'
public void testDeterminism() {
                           ^
C:\Users\luyan\AppData\Local\Temp\tmpn890uoufTempValidation.j
- **错误行**: 4


### `release\v3.0.0\docs\Struct\Proof-Chains-Flink-Complete.md`

**问题 #3** (第 452 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplzp1ivv2TempValidation.java:4: 错误: 找不到符号
    inputStream,
    ^
  符号:   变量 inputStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmplzp1ivv2TempVali
- **错误行**: 4


### `release\v3.0.0\docs\Struct\Proof-Chains-Flink-Implementation.md`

**问题 #24** (第 506 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptqgpn__uTempValidation.java:4: 错误: 非法的表达式开始
public void triggerCheckpoint(long timestamp) {
^
C:\Users\luyan\AppData\Local\Temp\tmptqgpn__uTempValidation.java:15:
- **错误行**: 4

**问题 #25** (第 521 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp56w_ktxxTempValidation.java:4: 错误: 非法的表达式开始
public final void snapshotState(StateSnapshotContext context) {
^
C:\Users\luyan\AppData\Local\Temp\tmp56w_ktxxTempVali
- **错误行**: 4

**问题 #26** (第 535 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplh804275TempValidation.java:4: 错误: 非法的表达式开始
private void processElement(StreamRecord<IN> element) {
^
C:\Users\luyan\AppData\Local\Temp\tmplh804275TempValidation.j
- **错误行**: 4

**问题 #27** (第 552 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpstxf_tvdTempValidation.java:4: 错误: 非法的表达式开始
public void emitCompletedElement() {
^
C:\Users\luyan\AppData\Local\Temp\tmpstxf_tvdTempValidation.java:13: 错误: 需要 clas
- **错误行**: 4


### `release\v3.0.0\docs\Struct\Unified-Model-Relationship-Graph.md`

**问题 #5** (第 245 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvxrcreynTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpvxr
- **错误行**: 3


### `release\v3.0.0\docs\TOOLCHAIN.md`

**问题 #17** (第 463 行, 语言: yaml)

- **错误**: could not determine a constructor for the tag 'tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format'
  in "<unicode string>", line 43, column 19:
              format: !!python/name:py
- **错误行**: 43


### `release\v3.0.0\docs\TROUBLESHOOTING.md`

**问题 #6** (第 192 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpukxp99enSyncFunction.java:22: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<Result> result = AsyncDataStream.unorderedWait(
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 22

**问题 #8** (第 268 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps5sbtbhyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmps5s
- **错误行**: 3

**问题 #10** (第 336 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7wx4l11jTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp7wx4l11jTempValidat
- **错误行**: 4

**问题 #16** (第 577 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg3qgt12yTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpg3q
- **错误行**: 3


### `release\v3.0.0\docs\docs\certification\csa\labs\lab-01-time-semantics.md`

**问题 #3** (第 89 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpam7gagrjTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpam7gagrjTempValidatio
- **错误行**: 4

**问题 #7** (第 199 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu0wfc39qTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpu0wfc39qTempValidatio
- **错误行**: 4


### `release\v3.0.0\docs\docs\certification\csa\resources\capstone-project-csa.md`

**问题 #4** (第 153 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplex0ddc2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmplex
- **错误行**: 3

**问题 #5** (第 185 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa33z4o6gTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.functions.AggregateFunction;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #6** (第 220 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmposgl9f3jTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmposgl9
- **错误行**: 3

**问题 #8** (第 278 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr1gu_b7wTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpr1gu_
- **错误行**: 3

**问题 #9** (第 310 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5egw2bv0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp5egw2bv
- **错误行**: 3


### `release\v3.0.0\docs\docs\chatbot-integration.md`

**问题 #5** (第 164 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 24

**问题 #17** (第 683 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpndtgh2o9TempValidation.java:3: 错误: 非法的表达式开始
        > env.enableCheckpointing(60000);  // 60 second interval
        ^
C:\Users\luyan\AppData\Local\Temp\tmpndtgh2o
- **错误行**: 3


### `release\v3.0.0\docs\docs\contributing\writing-guide.md`

**问题 #9** (第 250 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiswzix24TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #18** (第 397 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0kf95_qkTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp0kf
- **错误行**: 3

**问题 #22** (第 454 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprzos120fTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmprzo
- **错误行**: 3


### `release\v3.0.0\docs\docs\i18n\en\Flink\02-core\checkpoint-mechanism-deep-dive.md`

**问题 #1** (第 155 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoow2b_meStateBackend.java:3: 错误: 需要<标识符>
    createKeyedStateBackend(env, stateHandles): AbstractKeyedStateBackend<K>
                           ^
C:\Users\luyan\A
- **错误行**: 3

**问题 #5** (第 410 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk42tkq2_TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpk42tkq2
- **错误行**: 3

**问题 #6** (第 428 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprgyl5imsTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmprgyl5im
- **错误行**: 3

**问题 #7** (第 446 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp657omar7TempValidation.java:4: 错误: 找不到符号
env.setStateBackend(new EmbeddedRocksDBStateBackend(true));  // incremental = true
                        ^
  符号:   类 Emb
- **错误行**: 4


### `release\v3.0.0\docs\docs\i18n\en\Knowledge\07-best-practices\07.01-flink-production-checklist.md`

**问题 #3** (第 223 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaw1qs_4pTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(60000); // 1 minute interval
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #4** (第 249 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_gtbn114TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp_gt
- **错误行**: 3

**问题 #7** (第 374 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyt_ho4n8TempValidation.java:4: 错误: 非法的表达式开始
private static final Logger LOG = LoggerFactory.getLogger(MyFunction.class);
^
C:\Users\luyan\AppData\Local\Temp\tmpyt_
- **错误行**: 4

**问题 #11** (第 562 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppgmbujo_TempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(10000);  // 10s interval
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #12** (第 573 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9ajwxk8sTempValidation.java:4: 错误: 找不到符号
env.enableCheckpointing(300000);  // 5min interval
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `release\v3.0.0\docs\docs\i18n\en\Struct\01-foundation\01.04-dataflow-model-formalization.md`

**问题 #1** (第 392 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9i10f5aeTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9i1
- **错误行**: 3


### `release\v3.0.0\docs\docs\i18n\en\Struct\02-properties\02.01-determinism-in-streaming.md`

**问题 #3** (第 497 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpevbihgxsTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpevb
- **错误行**: 3

**问题 #4** (第 533 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy6ihcf6sTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpy6ihcf6sTempValidat
- **错误行**: 4

**问题 #5** (第 556 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpixq0nhs8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpixq
- **错误行**: 3

**问题 #6** (第 574 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkdjdx8loTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpkdjdx8loTempValidat
- **错误行**: 4


### `release\v3.0.0\docs\docs\i18n\en\Struct\02-properties\02.02-consistency-hierarchy.md`

**问题 #1** (第 656 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuexpayamTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpuex
- **错误行**: 3

**问题 #3** (第 730 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv0wew6tgHttpSink.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.sink不存在
import org.apache.flink.streaming.api.functions.sink.SinkFunction;

- **错误行**: 1

**问题 #4** (第 754 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptdl6d45aEagerKafkaSource.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.source不存在
import org.apache.flink.streaming.api.functions.source.SourceFunction;

- **错误行**: 1


### `release\v3.0.0\docs\docs\i18n\en\Struct\02-properties\02.03-watermark-monotonicity.md`

**问题 #1** (第 314 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjhd0ml6kTempValidation.java:4: 错误: 非法的表达式开始
public void onWatermark(Watermark wm, Context ctx, Collector<Out> out) {
^
C:\Users\luyan\AppData\Local\Temp\tmpjhd0ml6
- **错误行**: 4


### `release\v3.0.0\docs\docs\i18n\en\Struct\04-proofs\04.02-flink-exactly-once-correctness.md`

**问题 #5** (第 734 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp78qgre4jTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp78q
- **错误行**: 3

**问题 #6** (第 776 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppt7k4zz1TempValidation.java:4: 错误: 找不到符号
StreamingFileSink<Result> sink = StreamingFileSink
^
  符号:   类 StreamingFileSink
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4

**问题 #7** (第 799 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk_kq1ae_CounterSink.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.sink不存在
import org.apache.flink.streaming.api.functions.sink.SinkFunction;

- **错误行**: 1

**问题 #8** (第 827 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6pedbewrEagerKafkaSource.java:1: 错误: 程序包org.apache.flink.streaming.api.functions.source不存在
import org.apache.flink.streaming.api.functions.source.SourceFunction;

- **错误行**: 1


### `release\v3.0.0\docs\examples\docker\README.md`

**问题 #8** (第 139 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 3, column 37:
          jobmanager.memory.process.size: 512m
                                        ^ (line: 3)
- **错误行**: 3
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `release\v3.0.0\docs\examples\java\stateful\README.md`

**问题 #3** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpomuxm2yvTempValidation.java:4: 错误: 需要')'或','
env.setStateBackend(new HashMapStateBackend()  // MemoryStateBackend已弃用，使用HashMapStateBackend

- **错误行**: 4

**问题 #4** (第 78 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjqd72dfxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpjqd72
- **错误行**: 3


### `release\v3.0.0\docs\examples\java\wordcount\README.md`

**问题 #7** (第 103 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8qi9b5ezTempValidation.java:4: 错误: 找不到符号
if (word.length() > 3) {
    ^
  符号:   变量 word
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp8qi9b5ezTempVal
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\01-foundations\05-type-theory.md`

**问题 #6** (第 533 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxsa6bhswTempValidation.java:3: 错误: 需要>或','
        <T extends Comparable<T>> T max(T a, T b)
           ^
C:\Users\luyan\AppData\Local\Temp\tmpxsa6bhswTempValidati
- **错误行**: 3


### `release\v3.0.0\docs\formal-methods\01-foundations\09-subtyping.md`

**问题 #3** (第 295 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpodntm705Comparable.java:5: 错误: 未命名类 是预览功能，默认情况下禁用。
<T extends Comparable<T>> T max(T a, T b)  // F-有界
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Lo
- **错误行**: 5

**问题 #8** (第 594 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmfqyw5wuAnimal.java:3: 错误: 非法的表达式开始
    void speak() { ... }
                   ^
C:\Users\luyan\AppData\Local\Temp\tmpmfqyw5wuAnimal.java:7: 错误: 非法的表达式开始
    void
- **错误行**: 3


### `release\v3.0.0\docs\formal-methods\03-model-taxonomy\02-computation-models\dataflow-analysis-formal.md`

**问题 #7** (第 449 行, 语言: python)

- **错误**: SyntaxError: invalid character '⊥' (U+22A5)
- **错误行**: 3


### `release\v3.0.0\docs\formal-methods\03-model-taxonomy\06-practical-concurrency\01-practical-concurrency-formalization.md`

**问题 #5** (第 554 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu0adcsf7ParallelMergeSort.java:48: 错误: 未命名类 是预览功能，默认情况下禁用。
ForkJoinPool pool = new ForkJoinPool();
^
  （请使用 --enable-preview 以启用 未命名类）
C:\Users\luyan\AppData\Local
- **错误行**: 48


### `release\v3.0.0\docs\formal-methods\04-application-layer\01-workflow\03-bpmn-semantics.md`

**问题 #11** (第 352 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9frz_nxdEventBasedGateway.java:3: 错误: 找不到符号
    List<Event> waitingEvents;
    ^
  符号:   类 List
  位置: 类 EventBasedGateway
C:\Users\luyan\AppData\Local\Temp\tmp9frz
- **错误行**: 3


### `release\v3.0.0\docs\formal-methods\04-application-layer\02-stream-processing\01-stream-formalization.md`

**问题 #4** (第 296 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2cc9x7s7ExactlyOnceOperator.java:3: 错误: 找不到符号
    void processElement(Element e) {
                        ^
  符号:   类 Element
  位置: 类 ExactlyOnceOperator
C:\Users
- **错误行**: 3


### `release\v3.0.0\docs\formal-methods\04-application-layer\02-stream-processing\03-window-semantics.md`

**问题 #2** (第 239 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgk7a4pw5TempValidation.java:4: 错误: 找不到符号
Window.into(FixedWindows.of(Duration.standardMinutes(1)))
^
  符号:   变量 Window
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\04-application-layer\02-stream-processing\04-flink-formal-verification.md`

**问题 #1** (第 752 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbnhgxhaaTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpbnhgxhaaTempValidat
- **错误行**: 4

**问题 #3** (第 814 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi7j487rfTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.eventtime.WatermarkStrategy;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #4** (第 842 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0xj4guckTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp0xj4g
- **错误行**: 3


### `release\v3.0.0\docs\formal-methods\04-application-layer\02-stream-processing\04-flink-formalization.md`

**问题 #7** (第 375 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpidlpvt5tTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpidl
- **错误行**: 3

**问题 #9** (第 399 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpspl5eft1TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpspl5eft
- **错误行**: 3

**问题 #11** (第 428 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwmx1ii8wTempValidation.java:12: 错误: 非法的表达式开始
WatermarkStrategy.<Event>forBoundedOutOfOrderness(...)
                                                  ^
1 个错误

- **错误行**: 12


### `release\v3.0.0\docs\formal-methods\04-application-layer\02-stream-processing\05-stream-joins.md`

**问题 #7** (第 318 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfb9oh4yvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpfb9
- **错误行**: 3

**问题 #9** (第 343 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4vvytsdyTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp4vvytsdyTempValidat
- **错误行**: 4

**问题 #13** (第 391 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2dwn2sxgTempValidation.java:4: 错误: 找不到符号
MapStateDescriptor<String, UserInfo> descriptor =
^
  符号:   类 MapStateDescriptor
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\04-application-layer\04-blockchain-verification\02-consensus-protocols.md`

**问题 #8** (第 1031 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 6, column 1:
    timeout_propose = "3s"
    ^ (line: 6)
- **错误行**: 6


### `release\v3.0.0\docs\formal-methods\04-application-layer\10-kafka-formalization\01-kafka-semantics.md`

**问题 #26** (第 798 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyssjqik4TempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #27** (第 822 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmf8u67gaTempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #28** (第 841 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9687m7d1TempValidation.java:3: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp96
- **错误行**: 3

**问题 #29** (第 876 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3ek3wfliTempValidation.java:3: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp3e
- **错误行**: 3

**问题 #30** (第 904 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppt935888TempValidation.java:3: 错误: 找不到符号
Properties props = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmppt
- **错误行**: 3

**问题 #31** (第 930 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbq8myfevTempValidation.java:3: 错误: 找不到符号
Properties consumerProps = new Properties();
^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 3

**问题 #32** (第 981 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjvfzo6tbTempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\formal-methods\04-application-layer\11-mysql-formalization\01-mysql-innodb-semantics.md`

**问题 #5** (第 764 行, 语言: sql)

- **错误**: 可能的语法问题: -- READ COMMITTED: 返回3条记录 (幻读!)
-- REPEATABLE READ...

**问题 #9** (第 837 行, 语言: sql)

- **错误**: 可能的语法问题: -- 设置锁等待超时
SET SESSION INNODB_LOCK_WAIT_TIMEOUT = ...; 可能的语法问题: -- 等待50秒后:
-- ERROR 1205 (HY000): LOCK WAIT TIMEOU...

**问题 #10** (第 857 行, 语言: sql)

- **错误**: 可能的语法问题: -- 检查影响行数
-- 若 AFFECTED_ROWS = 1: 更新成功
-- 若 AFFECT...

**问题 #11** (第 887 行, 语言: sql)

- **错误**: 可能的语法问题: -- 应用程序代码 (伪代码)
-- 使用XA实现跨库事务

-- 第一阶段：准备
XA START...; 可能的语法问题: XA END 'TRX-001';...; 可能的语法问题: XA PREPARE 'TRX-001';  -- 准备阶段，记录REDO/UNDO...; 可能的语法问题: -- 协调器记录事务状态
-- 若所有参与者都PREPARE成功，则提交
--


### `release\v3.0.0\docs\formal-methods\05-verification\01-logic\06-permission-based-reasoning.md`

**问题 #8** (第 462 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcvk366emTempValidation.java:7: 错误: 非法的表达式开始
void read_only(int x) {
^
C:\Users\luyan\AppData\Local\Temp\tmpcvk366emTempValidation.java:7: 错误: 需要';'
void read_only(
- **错误行**: 7

**问题 #9** (第 493 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyeeub5a7TempValidation.java:7: 错误: 非法的表达式开始
void parallel_sum(int[] a, int n) {
^
C:\Users\luyan\AppData\Local\Temp\tmpyeeub5a7TempValidation.java:7: 错误: 需要';'
voi
- **错误行**: 7

**问题 #13** (第 759 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpir7f1ixvTreeNode.java:26: 错误: 不是语句
        parallel {
        ^
C:\Users\luyan\AppData\Local\Temp\tmpir7f1ixvTreeNode.java:26: 错误: 需要';'
        parallel {

- **错误行**: 26

**问题 #14** (第 797 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjwr6e3_aTempValidation.java:11: 错误: 非法的表达式开始
void parallel_sort(int[] array, int n) {
^
C:\Users\luyan\AppData\Local\Temp\tmpjwr6e3_aTempValidation.java:11: 错误: 需要
- **错误行**: 11

**问题 #16** (第 885 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0opucd0aLockFreeQueue.java:2: 错误: 找不到符号
    AtomicReference<Node<T>> head, tail;
    ^
  符号:   类 AtomicReference
  位置: 类 LockFreeQueue<T>
  其中, T是类型变量:
    T扩展已在类
- **错误行**: 2


### `release\v3.0.0\docs\formal-methods\05-verification\04-security\04-type-system-security.md`

**问题 #5** (第 449 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp9vaag29TempValidation.java:5: 错误: 非法字符: '\u251c'
├── String
^
C:\Users\luyan\AppData\Local\Temp\tmpp9vaag29TempValidation.java:4: 错误: 不是语句
Object
^
C:\Users\luyan
- **错误行**: 5

**问题 #6** (第 461 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg6mlg6moTempValidation.java:4: 错误: 找不到符号
List<String> strings = new ArrayList<>();
^
  符号:   类 List
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpg6m
- **错误行**: 4

**问题 #9** (第 499 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppvbbchsdTempValidation.java:4: 错误: 非法的表达式开始
void safeBufferJava() {
^
C:\Users\luyan\AppData\Local\Temp\tmppvbbchsdTempValidation.java:4: 错误: 需要';'
void safeBuffer
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\05-verification\05-quantum\02-quantum-separation-logic.md`

**问题 #4** (第 571 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 17

**问题 #5** (第 615 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 13

**问题 #6** (第 647 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 19


### `release\v3.0.0\docs\formal-methods\06-tools\industrial\aws-s3-formalization.md`

**问题 #6** (第 258 行, 语言: python)

- **错误**: SyntaxError: invalid decimal literal
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\08-ai-formal-methods\03-neural-network-verification.md`

**问题 #3** (第 230 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 13


### `release\v3.0.0\docs\formal-methods\08-ai-formal-methods\06-deepseek-prover-tutorial.md`

**问题 #3** (第 109 行, 语言: python)

- **错误**: SyntaxError: unexpected indent
- **错误行**: 2

**问题 #5** (第 211 行, 语言: python)

- **错误**: SyntaxError: expected 'else' after 'if' expression
- **错误行**: 2


### `release\v3.0.0\docs\formal-methods\08-ai-formal-methods\08-neuro-symbolic-ai.md`

**问题 #8** (第 522 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 5


### `release\v3.0.0\docs\formal-methods\98-appendices\09-mermaid-validation-report.md`

**问题 #15** (第 387 行, 语言: python)

- **错误**: SyntaxError: unterminated f-string literal (detected at line 38)
- **错误行**: 38


### `release\v3.0.0\docs\formal-methods\98-appendices\wikipedia-concepts\17-two-phase-commit.md`

**问题 #14** (第 528 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp717cs3a4TempValidation.java:4: 错误: 找不到符号
UserTransaction ut = getUserTransaction();
^
  符号:   类 UserTransaction
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\98-appendices\wikipedia-concepts\en\17-two-phase-commit.md`

**问题 #14** (第 544 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0igz7m78TempValidation.java:4: 错误: 找不到符号
UserTransaction ut = getUserTransaction();
^
  符号:   类 UserTransaction
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\99-probabilistic-programming.md`

**问题 #2** (第 411 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2

**问题 #3** (第 431 行, 语言: python)

- **错误**: SyntaxError: invalid character '⊕' (U+2295)
- **错误行**: 3

**问题 #4** (第 445 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 1

**问题 #5** (第 594 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 3

**问题 #6** (第 652 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2

**问题 #7** (第 701 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2


### `release\v3.0.0\docs\formal-methods\COMPARISON-WORKFLOW-VS-STREAM.md`

**问题 #3** (第 219 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphj14qsaiTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmphj1
- **错误行**: 3


### `release\v3.0.0\docs\formal-methods\Flink\en\01-architecture-overview.md`

**问题 #1** (第 250 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg4higj69TempValidation.java:4: 错误: 找不到符号
   state.getAsync(key)
                  ^
  符号:   变量 key
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpg4hi
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\Flink\en\03-checkpoint.md`

**问题 #1** (第 128 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv6jhyv6_StateBackend.java:3: 错误: 需要<标识符>
    createKeyedStateBackend(env, stateHandles): AbstractKeyedStateBackend<K>
                           ^
C:\Users\luyan\A
- **错误行**: 3

**问题 #5** (第 577 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp941hyk5hTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #6** (第 611 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmt_nnby2TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #7** (第 638 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi26s4azoTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #8** (第 659 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_f_a74bkTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `release\v3.0.0\docs\formal-methods\Flink\en\04-state-backends.md`

**问题 #3** (第 493 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa9bp186yTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #5** (第 530 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsjufa6z2TempValidation.java:5: 错误: 找不到符号
EmbeddedRocksDBStateBackend rocksDbBackend =
^
  符号:   类 EmbeddedRocksDBStateBackend
  位置: 类 TempValidation
C:\Users\luyan
- **错误行**: 5

**问题 #6** (第 580 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpu8dx0la6TempValidation.java:5: 错误: 找不到符号
ForStStateBackend forstBackend = new ForStStateBackend();
^
  符号:   类 ForStStateBackend
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 5


### `release\v3.0.0\docs\formal-methods\Flink\en\05-watermark.md`

**问题 #1** (第 256 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuymcl62lTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpuymcl
- **错误行**: 3

**问题 #2** (第 266 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeykmydc9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpeykmy
- **错误行**: 3

**问题 #3** (第 276 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi2orc05xTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpi2orc
- **错误行**: 3

**问题 #4** (第 375 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpdbrr744qTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpdbr
- **错误行**: 3

**问题 #5** (第 387 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppfrxuoz3TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmppfr
- **错误行**: 3

**问题 #6** (第 403 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8ykvu_dnTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8ykvu
- **错误行**: 3

**问题 #7** (第 414 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxkvv3egiTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpxkvv3
- **错误行**: 3

**问题 #8** (第 425 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl_husafyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpl_hus
- **错误行**: 3

**问题 #9** (第 439 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9cmrex3cTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9cm
- **错误行**: 3


### `release\v3.0.0\docs\formal-methods\Flink\en\06-kafka-connector.md`

**问题 #7** (第 273 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnxn_7h_dTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnxn
- **错误行**: 3

**问题 #8** (第 296 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqdxiyenhTempValidation.java:3: 错误: 找不到符号
        KafkaSink<String> sink = KafkaSink.<String>builder()
        ^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users
- **错误行**: 3

**问题 #9** (第 312 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt5o_qwk8TempValidation.java:3: 错误: 找不到符号
FlinkKafkaProducer<String> producer = new FlinkKafkaProducer<>(
^
  符号:   类 FlinkKafkaProducer
  位置: 类 TempValidation
C:\U
- **错误行**: 3


### `release\v3.0.0\docs\formal-methods\Flink\en\07-file-system.md`

**问题 #6** (第 261 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq24a100gTempValidation.java:3: 错误: 找不到符号
        FileSink.forRowFormat(new Path("s3://bucket/output"), new SimpleStringEncoder())

- **错误行**: 3

**问题 #7** (第 307 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph_vj94t_TempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4

**问题 #8** (第 318 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw57ew09sTempValidation.java:5: 错误: 找不到符号
    new Path("s3://bucket/output"),
        ^
  符号:   类 Path
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpw
- **错误行**: 5

**问题 #9** (第 334 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpstrae9b6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpstr
- **错误行**: 3

**问题 #10** (第 357 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmtmocvwjTempValidation.java:4: 错误: 找不到符号
FileSink<GenericRecord> sink = FileSink
^
  符号:   类 FileSink
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpm
- **错误行**: 4

**问题 #11** (第 382 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbk_xapy_TempValidation.java:4: 错误: 找不到符号
Schema evolvedSchema = new Schema.Parser().parse(
^
  符号:   类 Schema
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\Flink\en\09-query-optimization.md`

**问题 #5** (第 238 行, 语言: sql)

- **错误**: 可能的语法问题: -- FULL ANALYSIS FOR CRITICAL TABLES
ANALYZE TABLE...; 可能的语法问题: -- COLUMN-SPECIFIC ANALYSIS
ANALYZE TABLE EVENTS C...; 可能的语法问题: -- SAMPLING FOR LARGE TABLES
ANALYZE TABLE BIG_TAB...

**问题 #6** (第 282 行, 语言: sql)

- **错误**: 可能的语法问题: -- ENABLE COST-BASED OPTIMIZATION
SET TABLE.OPTIMI...; 可能的语法问题: -- ENABLE ADVANCED REWRITES
SET TABLE.OPTIMIZER.DI...

**问题 #11** (第 370 行, 语言: sql)

- **错误**: 可能的语法问题: -- TWO-PHASE AGGREGATION FOR HIGH-CARDINALITY GROU...


### `release\v3.0.0\docs\formal-methods\Flink\en\11-standalone.md`

**问题 #10** (第 383 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 10, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^ (line: 10)
- **错误行**: 10
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅


### `release\v3.0.0\docs\formal-methods\Flink\en\12-ml-pipeline.md`

**问题 #6** (第 358 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy2jifcf8TempValidation.java:4: 错误: 找不到符号
OnlineLogisticRegression onlineLearner = new OnlineLogisticRegression()
^
  符号:   类 OnlineLogisticRegression
  位置: 类 TempV
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\Flink\en\13-gelly.md`

**问题 #1** (第 24 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2ol4y1o6TempValidation.java:3: 错误: 不是语句
        Graph<K, VV, EV> = (DataSet<Vertex<K, VV>>, DataSet<Edge<K, EV>>)
             ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 3

**问题 #4** (第 253 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_vb5ju72TempValidation.java:4: 错误: 找不到符号
Graph<Long, Double, Double> graph = Graph.fromDataSet(
^
  符号:   类 Graph
  位置: 类 TempValidation
C:\Users\luyan\AppData\Loc
- **错误行**: 4

**问题 #5** (第 277 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt2dfk8vyPageRankComputeFunction.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
Graph<Long, Double, Double> graph = Graph.fromDataSet(
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #6** (第 323 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr84cxbvzGatherNeighborIds.java:2: 错误: 未命名类 是预览功能，默认情况下禁用。
Graph<Long, Long, NullValue> ccGraph = graph
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 2

**问题 #7** (第 356 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb2i_ev0kTempValidation.java:4: 错误: 找不到符号
Graph<Long, Double, Double> bipartiteGraph = Graph.fromDataSet(
^
  符号:   类 Graph
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 4

**问题 #8** (第 379 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6q_5aavlTempValidation.java:4: 错误: 找不到符号
Graph<String, AccountInfo, Transaction> transactionGraph =
^
  符号:   类 Graph
  位置: 类 TempValidation
C:\Users\luyan\AppData
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\Knowledge\en\01-streaming-overview.md`

**问题 #4** (第 296 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxwhgc07uExactlyOnceOperator.java:3: 错误: 找不到符号
    void processElement(Element e) {
                        ^
  符号:   类 Element
  位置: 类 ExactlyOnceOperator
C:\Users
- **错误行**: 3


### `release\v3.0.0\docs\formal-methods\Knowledge\en\03-window-semantics.md`

**问题 #2** (第 239 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprsdxg098TempValidation.java:4: 错误: 找不到符号
Window.into(FixedWindows.of(Duration.standardMinutes(1)))
^
  符号:   变量 Window
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\Knowledge\en\04-time-semantics.md`

**问题 #7** (第 340 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp364ls6haTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp364
- **错误行**: 3

**问题 #9** (第 364 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9nng25qiTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9nng25q
- **错误行**: 3

**问题 #11** (第 393 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmfhrnx4lTempValidation.java:12: 错误: 非法的表达式开始
WatermarkStrategy.<Event>forBoundedOutOfOrderness(...)
                                                  ^
1 个错误

- **错误行**: 12


### `release\v3.0.0\docs\formal-methods\Knowledge\en\05-state-management.md`

**问题 #7** (第 318 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxwj2go97TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpxwj
- **错误行**: 3

**问题 #9** (第 343 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_5_rpyp0TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp_5_rpyp0TempValidat
- **错误行**: 4

**问题 #13** (第 391 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2bwnl_ciTempValidation.java:4: 错误: 找不到符号
MapStateDescriptor<String, UserInfo> descriptor =
^
  符号:   类 MapStateDescriptor
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\Knowledge\en\07-exactly-once.md`

**问题 #6** (第 346 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpph67q_bgTempValidation.java:4: 错误: 找不到符号
FlinkKafkaProducer<String> kafkaSink = new FlinkKafkaProducer<>(
^
  符号:   类 FlinkKafkaProducer
  位置: 类 TempValidation
C:\
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\Knowledge\en\10-performance-tuning.md`

**问题 #10** (第 440 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    taskmanager.memory.process.size: 4gb
    ^ (line: 4)
found duplicate key "taskmanager.memory.process.size" with value "32gb"
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\Knowledge\en\13-stream-joins.md`

**问题 #8** (第 396 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmptcrcef7hTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmptcr
- **错误行**: 3

**问题 #10** (第 421 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcnphapssTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpcnphapssTempValidat
- **错误行**: 4

**问题 #14** (第 474 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpspy_nwh9TempValidation.java:5: 错误: 需要';'
    new MapStateDescriptor<>("users", String.class, UserInfo.class)

- **错误行**: 5


### `release\v3.0.0\docs\formal-methods\Knowledge\en\15-schema-evolution.md`

**问题 #16** (第 520 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4dudotliTempValidation.java:3: 错误: 找不到符号
        Properties props = new Properties();
        ^
  符号:   类 Properties
  位置: 类 TempValidation
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #17** (第 542 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_bfao9bnTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.typeinfo.Types;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp_bfao9bnTempV
- **错误行**: 3

**问题 #18** (第 566 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2j8d8zhwTempValidation.java:4: 错误: 找不到符号
Table orders = tableEnv.from("Orders");
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp2j8d
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\Knowledge\en\16-security.md`

**问题 #14** (第 564 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5r99grysTempValidation.java:3: 错误: 找不到符号
        Configuration conf = new Configuration();
        ^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\
- **错误行**: 3


### `release\v3.0.0\docs\formal-methods\Knowledge\en\17-cost-optimization.md`

**问题 #8** (第 401 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwz92r_f2TempValidation.java:4: 错误: 找不到符号
Configuration conf = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `release\v3.0.0\docs\formal-methods\分布式系统形式化建模理论与验证方法.md`

**问题 #31** (第 1137 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw2kro3u0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpw2kro3u0Tem
- **错误行**: 3


### `release\v3.0.0\docs\i18n\en\Flink\00-FLINK-TECH-STACK-DEPENDENCY.md`

**问题 #6** (第 234 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzoqholeyTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpzoq
- **错误行**: 3

**问题 #7** (第 250 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt8i9o5kjTempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.sqlQuery("SELECT COUNT(*) FROM events");
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\A
- **错误行**: 4

**问题 #8** (第 258 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd7ib2qteTempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<String> source = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C:\Use
- **错误行**: 4


### `release\v3.0.0\docs\i18n\en\Flink\3.9-state-backends-deep-comparison.md`

**问题 #13** (第 383 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend.rocksdb.memory.man ...
    ^ (line: 2)
found duplicate key "state.backend.rocksdb.memory.managed" with value
- **错误行**: 2

**问题 #14** (第 404 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 2, column 1:
    state.backend.rocksdb.compaction ...
    ^ (line: 2)
found duplicate key "state.backend.rocksdb.compaction.style" with valu
- **错误行**: 2


### `release\v3.0.0\docs\i18n\en\Flink\data-types-complete-reference.md`

**问题 #4** (第 140 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9pq3ggggTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.DataTypes;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9pq3ggggTempValidat
- **错误行**: 3


### `release\v3.0.0\docs\i18n\en\Flink\elasticsearch-connector-guide.md`

**问题 #2** (第 112 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkfa74lizTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.elasticsearch.sink.Elasticsearch7SinkBuilder;
^
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 3

**问题 #4** (第 189 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1609pjonTempValidation.java:4: 错误: 找不到符号
ElasticsearchSink<Event> esSink = new Elasticsearch7SinkBuilder<Event>()
^
  符号:   类 ElasticsearchSink
  位置: 类 TempValidat
- **错误行**: 4


### `release\v3.0.0\docs\i18n\en\Flink\flink-state-backends-comparison.md`

**问题 #3** (第 227 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx9e4nr8eTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #4** (第 254 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps6v447tvTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #5** (第 303 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk90pevhxTempValidation.java:4: 错误: 找不到符号
Configuration config = new Configuration();
^
  符号:   类 Configuration
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\
- **错误行**: 4

**问题 #9** (第 459 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq1ybzh33TempValidation.java:4: 错误: 找不到符号
config.set(RocksDBOptions.BLOCK_CACHE_SIZE, MemorySize.ofMebiBytes(256));
           ^
  符号:   变量 RocksDBOptions
  位置: 类 T
- **错误行**: 4

**问题 #11** (第 476 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp78i72pyfTempValidation.java:3: 错误: 找不到符号
        config.set(CheckpointingOptions.INCREMENTAL_CHECKPOINTS, true);
                   ^
  符号:   变量 CheckpointingOptio
- **错误行**: 3

**问题 #13** (第 486 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplhlwtjvxTempValidation.java:3: 错误: 找不到符号
        config.set(CheckpointingOptions.MAX_CONCURRENT_CHECKPOINTS, 1);
                   ^
  符号:   变量 CheckpointingOptio
- **错误行**: 3

**问题 #15** (第 499 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj9c7gbhlTempValidation.java:4: 错误: 找不到符号
config.set(CheckpointingOptions.LOCAL_RECOVERY, true);
           ^
  符号:   变量 CheckpointingOptions
  位置: 类 TempValidation
- **错误行**: 4


### `release\v3.0.0\docs\i18n\en\Flink\jdbc-connector-guide.md`

**问题 #2** (第 111 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm5bfsuvxTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcConnectionOptions;
^
C:\Users\luyan\AppData\Local\Temp\tmpm5bfsuvxTempValida
- **错误行**: 3

**问题 #4** (第 180 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7gqt5ce8TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.jdbc.JdbcInputFormat;
^
C:\Users\luyan\AppData\Local\Temp\tmp7gqt5ce8TempValidation.j
- **错误行**: 3


### `release\v3.0.0\docs\i18n\en\Flink\mongodb-connector-guide.md`

**问题 #2** (第 96 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5xhqhwmwTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.source.MongoSource;
^
C:\Users\luyan\AppData\Local\Temp\tmp5xhqhwmwTempValida
- **错误行**: 3

**问题 #3** (第 132 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp2rwvtolpTempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.source.MongoSource;
^
C:\Users\luyan\AppData\Local\Temp\tmp2rwvtolpTempValida
- **错误行**: 3

**问题 #4** (第 165 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp08l3ju1TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.connector.mongodb.sink.MongoSink;
^
C:\Users\luyan\AppData\Local\Temp\tmpp08l3ju1TempValidation
- **错误行**: 3


### `release\v3.0.0\docs\i18n\en\Flink\pulsar-functions-integration.md`

**问题 #4** (第 112 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpih5eu3fqTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpih5
- **错误行**: 3


### `release\v3.0.0\docs\i18n\en\Flink\pyflink-deep-guide.md`

**问题 #7** (第 265 行, 语言: python)

- **错误**: SyntaxError: invalid syntax
- **错误行**: 2


### `release\v3.0.0\docs\i18n\en\Flink\risingwave-integration-guide.md`

**问题 #3** (第 61 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaj1sic4tTempValidation.java:4: 错误: 找不到符号
FlinkKafkaProducer<String> kafkaProducer = new FlinkKafkaProducer<>(
^
  符号:   类 FlinkKafkaProducer
  位置: 类 TempValidation
- **错误行**: 4

**问题 #6** (第 117 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxjnnt8pzTempValidation.java:4: 错误: 找不到符号
DebeziumSourceFunction<String> source = DebeziumSourceFunction.<String>builder()
^
  符号:   类 DebeziumSourceFunction
  位置:
- **错误行**: 4

**问题 #7** (第 128 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkmmo20_zTempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.sqlQuery(
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpkmmo20_zTe
- **错误行**: 4


### `release\v3.0.0\docs\i18n\en\Flink\state-backends-comparison.md`

**问题 #2** (第 103 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6m93srp5TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.runtime.state.hashmap.HashMapStateBackend;
^
C:\Users\luyan\AppData\Local\Temp\tmp6m93srp5TempV
- **错误行**: 3

**问题 #3** (第 136 行, 语言: yaml)

- **错误**: while constructing a mapping
  in "<unicode string>", line 4, column 1:
    state.backend: hashmap
    ^ (line: 4)
found duplicate key "state.backend" with value "rocksdb" (original value: "hashmap")

- **错误行**: 4

**问题 #4** (第 162 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa4p1od2_TempValidation.java:4: 错误: 非法的表达式开始
public void monitorStateBackend(RuntimeContext ctx) {
^
C:\Users\luyan\AppData\Local\Temp\tmpa4p1od2_TempValidation.jav
- **错误行**: 4


### `release\v3.0.0\docs\i18n\en\Knowledge\cep-complete-tutorial.md`

**问题 #2** (第 99 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzl8efcp4TempValidation.java:3: 错误: 非法的表达式开始
import org.apache.flink.cep.Pattern;
^
C:\Users\luyan\AppData\Local\Temp\tmpzl8efcp4TempValidation.java:3: 错误: 不是语句
imp
- **错误行**: 3

**问题 #3** (第 155 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7ays6yiiTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmp7ays6yiiTempValidatio
- **错误行**: 4

**问题 #4** (第 200 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsej03w83TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpsej03w83TempValidatio
- **错误行**: 4


### `release\v3.0.0\docs\i18n\en\Knowledge\kafka-streams-migration.md`

**问题 #3** (第 66 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpz6btbzx6TempValidation.java:3: 错误: 找不到符号
KStream<String, Order> orders = builder.stream("orders");
^
  符号:   类 KStream
  位置: 类 TempValidation
C:\Users\luyan\AppDat
- **错误行**: 3

**问题 #4** (第 79 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpoj19x_t7TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpoj19x_t7TempValidat
- **错误行**: 4

**问题 #5** (第 106 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwbaxncw8TempValidation.java:3: 错误: 找不到符号
        KTable<Windowed<String>, Long> counts = orders
        ^
  符号:   类 KTable
  位置: 类 TempValidation
C:\Users\luyan\Ap
- **错误行**: 3


### `release\v3.0.0\docs\tutorials\01-environment-setup.md`

**问题 #5** (第 138 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 15, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^ (line: 15)
- **错误行**: 15
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #18** (第 658 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_lhjf8iaTempValidation.java:5: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmp_l
- **错误行**: 5


### `release\v3.0.0\docs\tutorials\02-first-flink-job.md`

**问题 #1** (第 66 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppdw_d6svTempValidation.java:5: 错误: 找不到符号
    .flatMap(tokenizer)  // 链内
             ^
  符号:   变量 tokenizer
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 5

**问题 #15** (第 797 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuyaz4xctTempValidation.java:4: 错误: 找不到符号
Set<String> stopWords = new HashSet<>(Arrays.asList("the", "a", "is", "of"));
^
  符号:   类 Set
  位置: 类 TempValidation
C:\Us
- **错误行**: 4

**问题 #17** (第 863 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmprjj_jn45TempValidation.java:5: 错误: 找不到符号
    .flatMap(new Tokenizer())
                 ^
  符号:   类 Tokenizer
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 5


### `release\v3.0.0\docs\tutorials\02-streaming-fundamentals-script.md`

**问题 #3** (第 75 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpth8xktqmTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpth8
- **错误行**: 3

**问题 #6** (第 162 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo6ejteb7TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #9** (第 258 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmponq8yozoTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmponq8yozoTempValidat
- **错误行**: 4

**问题 #12** (第 384 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcj9wditlTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpcj9
- **错误行**: 3


### `release\v3.0.0\docs\tutorials\04-design-patterns-script.md`

**问题 #10** (第 544 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy6_qp8puAsyncIOPattern.java:18: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 18

**问题 #12** (第 702 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_uz1evcoStateManagementPattern.java:25: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 25

**问题 #16** (第 1017 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpen2x40dvCheckpointPattern.java:82: 错误: 非法的表达式开始
            .addSource(new FlinkKafkaConsumer<>(...))
                                                ^
1 个错误

- **错误行**: 82


### `release\v3.0.0\docs\tutorials\05-production-deployment-script.md`

**问题 #4** (第 144 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 7, column 1:
    kubectl wait --for=condition=rea ...
    ^ (line: 7)
- **错误行**: 7


### `release\v3.0.0\docs\tutorials\06-advanced-topics-script.md`

**问题 #7** (第 310 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpm859ylv2StateTTLConfiguration.java:49: 错误: 非法的表达式开始
        DataStream<Event> stream = env.addSource(...);
                                                 ^
1 个错误
- **错误行**: 49

**问题 #13** (第 855 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphxf9de6kSkewHandling.java:16: 错误: 非法的表达式开始
        DataStream<Event> source = env.addSource(...);
                                                 ^
1 个错误

- **错误行**: 16

**问题 #17** (第 1231 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpion33nlpLargeStateOptimization.java:32: 错误: 非法的表达式开始
        DataStream<Event> source = env.addSource(...);
                                                 ^
1 个错
- **错误行**: 32


### `release\v3.0.0\docs\tutorials\interactive\coding-challenges\challenge-01-hot-items.md`

**问题 #5** (第 92 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpozg6hhegUserBehaviorSource.java:5: 错误: 非法的表达式开始
    private String[] users = {"user_001", "user_002", "user_003", ...};

- **错误行**: 5

**问题 #9** (第 296 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxgivrbjrTempValidation.java:4: 错误: 需要';'
public void testHotItems() throws Exception {
                        ^
C:\Users\luyan\AppData\Local\Temp\tmpxgivrbjrTempV
- **错误行**: 4

**问题 #11** (第 346 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpeuqg6zt0TempValidation.java:6: 错误: 非法的表达式开始
    .window(...)
            ^
C:\Users\luyan\AppData\Local\Temp\tmpeuqg6zt0TempValidation.java:7: 错误: 非法的表达式开始
    .ag
- **错误行**: 6

**问题 #12** (第 358 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpngygrgnaTempValidation.java:4: 错误: 找不到符号
windowedCounts.addSink(new RedisSink<>(
^
  符号:   变量 windowedCounts
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `release\v3.0.0\docs\tutorials\interactive\coding-challenges\challenge-03-order-timeout.md`

**问题 #3** (第 103 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp85wtk2d8TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp85w
- **错误行**: 3

**问题 #10** (第 663 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplg1ogyv7TempValidation.java:4: 错误: 需要';'
public void testOrderTimeout() throws Exception {
                            ^
C:\Users\luyan\AppData\Local\Temp\tmplg1og
- **错误行**: 4

**问题 #11** (第 727 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbn0_s2lbMultiLevelTimeout.java:3: 错误: 非法的类型开始
public class MultiLevelTimeout extends KeyedProcessFunction<...> {

- **错误行**: 3

**问题 #12** (第 770 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpckhs25rkOrderWithInventory.java:5: 错误: 非法的类型开始
public class OrderWithInventory extends KeyedProcessFunction<...> {

- **错误行**: 5


### `release\v3.0.0\docs\tutorials\interactive\coding-challenges\challenge-04-recommendation.md`

**问题 #4** (第 206 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvnf1acihCollaborativeFiltering.java:22: 错误: 非法的表达式开始
                ctx.getBroadcastState(...).immutableEntries()) {
                                      ^
C:\Us
- **错误行**: 22

**问题 #6** (第 376 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_5a2q4byRealtimeRecommendationJob.java:15: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 15

**问题 #8** (第 472 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpej65dtnsABTestSplit.java:4: 错误: 非法的类型开始
    public void processElement(UserProfile profile, Context ctx, ...) {

- **错误行**: 4


### `release\v3.0.0\docs\tutorials\interactive\coding-challenges\challenge-05-data-pipeline.md`

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr1w9r8xsCDCSourceConfig.java:21: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<String> cdcStream = env
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 21


### `release\v3.0.0\docs\tutorials\interactive\hands-on-labs\lab-01-first-flink-program.md`

**问题 #12** (第 267 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7elcssa4TempValidation.java:3: 错误: 找不到符号
if (word.length() >= 3) {
    ^
  符号:   变量 word
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp7elcssa4TempVa
- **错误行**: 3


### `release\v3.0.0\docs\tutorials\interactive\hands-on-labs\lab-02-event-time.md`

**问题 #4** (第 132 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_iwx7efbTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp_iw
- **错误行**: 3


### `release\v3.0.0\docs\tutorials\interactive\hands-on-labs\lab-03-window-aggregation.md`

**问题 #3** (第 146 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpo0b9hk1uSlidingWindowExample.java:19: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 19

**问题 #4** (第 203 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphczpkaxjSessionWindowExample.java:21: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 21

**问题 #6** (第 378 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpq66xws0lEnrichmentFunction.java:7: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<WindowStats> results = stream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 7

**问题 #7** (第 421 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6zs8dukxCountTrigger.java:58: 错误: 需要 class、interface、enum 或 record
stream.keyBy(...)
^
1 个错误

- **错误行**: 58

**问题 #8** (第 497 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg9jtfzfsWindowBenchmark.java:9: 错误: 非法的表达式开始
        stream.window(...)
                      ^
C:\Users\luyan\AppData\Local\Temp\tmpg9jtfzfsWindowBenchmark.java:1
- **错误行**: 9

**问题 #10** (第 566 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpivn_0nv0TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpivn
- **错误行**: 3


### `release\v3.0.0\docs\tutorials\interactive\hands-on-labs\lab-04-state-management.md`

**问题 #5** (第 275 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp090kckw2StatefulFunctionWithTTL.java:9: 错误: 非法的类型开始
public class StatefulFunctionWithTTL extends KeyedProcessFunction<...> {

- **错误行**: 9

**问题 #7** (第 375 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgmxqdeclTempValidation.java:4: 错误: 需要';'
public void testTemperatureAlert() throws Exception {
                                ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #9** (第 441 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzextmf_zTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpzextmf_zTem
- **错误行**: 3


### `release\v3.0.0\docs\tutorials\interactive\hands-on-labs\lab-05-checkpoint.md`

**问题 #3** (第 86 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb6wz51gfStateBackendConfig.java:14: 错误: 需要')'或','
                env.setStateBackend(new HashMapStateBackend()  // MemoryStateBackend已弃用，使用HashMapStateBackend

- **错误行**: 14

**问题 #4** (第 133 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8te5extaTempValidation.java:4: 错误: 找不到符号
env.setStateBackend(new RocksDBStateBackend(
                        ^
  符号:   类 RocksDBStateBackend
  位置: 类 TempValidatio
- **错误行**: 4

**问题 #8** (第 238 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwrm4l3csTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmpwr
- **错误行**: 4

**问题 #10** (第 303 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpaw76ou8aTempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<String> kafkaSource = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C
- **错误行**: 4

**问题 #11** (第 339 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgil1g2ezTempValidation.java:4: 错误: 找不到符号
env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4


### `release\v3.0.0\docs\tutorials\interactive\hands-on-labs\lab-06-cep.md`

**问题 #2** (第 36 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwegfpxv1BasicCEPExample.java:22: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 22

**问题 #3** (第 122 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1u8u4napTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmp1u8u4napTempValidatio
- **错误行**: 4

**问题 #4** (第 164 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfcnacdsxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpfcnac
- **错误行**: 3

**问题 #5** (第 196 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpayp0sw_kTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpayp0sw_kTempValidatio
- **错误行**: 4

**问题 #6** (第 241 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4nfx0e40TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmp4nfx0e40TempValidat
- **错误行**: 4

**问题 #7** (第 286 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpafs4sahdFraudDetectionCEP.java:14: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 14

**问题 #8** (第 362 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpajhg1rwzTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpajhg1rwzTempValidatio
- **错误行**: 4

**问题 #9** (第 395 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd6ryxcgtTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpd6ryx
- **错误行**: 3

**问题 #10** (第 421 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpldc8fu04TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpldc8fu04TempValidatio
- **错误行**: 4


### `release\v3.0.0\docs\tutorials\interactive\quizzes\comprehensive-test.md`

**问题 #1** (第 439 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp_z9jh0phTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmp_z9jh0phTempValidatio
- **错误行**: 4


### `release\v3.0.0\docs\whitepaper-streaming-2027.md`

**问题 #7** (第 442 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsf3w5makTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpsf3w5makTempValidat
- **错误行**: 4

**问题 #19** (第 966 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnlsdv8k0TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpnlsdv8k0TempValidatio
- **错误行**: 4

**问题 #21** (第 1076 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpit_m98xcSessionFeatureAggregate.java:1: 错误: 程序包org.apache.flink.api.common.functions不存在
import org.apache.flink.api.common.functions.AggregateFunction;

- **错误行**: 1


### `release\v3.0.0\docs\whitepapers\flink-enterprise-implementation-guide.md`

**问题 #3** (第 165 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqv9hqdsiTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpqv9hqds
- **错误行**: 3


### `release\v3.0.0\docs\whitepapers\realtime-ai-architecture-practice.md`

**问题 #10** (第 375 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzwilu9wwTensorFlowInference.java:33: 错误: 未命名类 是预览功能，默认情况下禁用。
Table result = tableEnv.sqlQuery(
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 33


### `reports\FICTIONAL-CONTENT-SUMMARY.md`

**问题 #1** (第 75 行, 语言: sql)

- **错误**: 可能的语法问题: ML_PREDICT(MODEL_ID, FEATURES);              -- SQ...; 可能的语法问题: VECTOR_SEARCH(VECTOR_COLUMN, QUERY_VECTOR);  -- SQ...


### `reports\fictional-content-audit-20260405_143730.md`

**问题 #30** (第 511 行, 语言: sql)

- **错误**: 可能的语法问题: 55: -- 形式 1: 基本调用

>>> 56: SELECT * FROM ML_PREDICT...

**问题 #53** (第 863 行, 语言: sql)

- **错误**: 可能的语法问题: 367: -- DEF-F-12-110A: CREATE AGENT语法（未来可能的语法，概念设计...

**问题 #168** (第 2684 行, 语言: yaml)

- **错误**: while scanning a block scalar
  in "<unicode string>", line 2, column 1:
    >>> 40: ai.agent.enabled: true   ...
    ^ (line: 2)
expected chomping or indentation indicators, but found '>'
  in "<uni
- **错误行**: 2

**问题 #174** (第 2776 行, 语言: yaml)

- **错误**: while scanning a block scalar
  in "<unicode string>", line 1, column 1:
    >>> 818: # flink-gpu-deployment.yaml
    ^ (line: 1)
expected chomping or indentation indicators, but found '>'
  in "<unic
- **错误行**: 1

**问题 #451** (第 7182 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 1, column 14:
    74: Flink 2.4:
                 ^ (line: 1)
- **错误行**: 1
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #583** (第 9257 行, 语言: sql)

- **错误**: 可能的语法问题: 1333: -- =========================================...


### `reports\theorem-uniqueness-report.md`

**问题 #184** (第 3454 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpmlnqhp6kUserBehaviorCounter.java:4: 错误: 进行语法分析时已到达文件结尾
public class UserBehaviorCounter extends KeyedProcessFunction<String, UserEvent, Metrics> {

- **错误行**: 4

**问题 #187** (第 3474 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwz9c365iUserBehaviorCounter.java:4: 错误: 进行语法分析时已到达文件结尾
public class UserBehaviorCounter extends KeyedProcessFunction<String, UserEvent, Metrics> {

- **错误行**: 4

**问题 #190** (第 3494 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnj89pmfwUserBehaviorCounter.java:4: 错误: 进行语法分析时已到达文件结尾
public class UserBehaviorCounter extends KeyedProcessFunction<String, UserEvent, Metrics> {

- **错误行**: 4

**问题 #357** (第 5169 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpskg_jcidAsyncWindowAggregateFunction.java:5: 错误: 进行语法分析时已到达文件结尾
public class AsyncWindowAggregateFunction extends KeyedProcessFunction<String, Event, WindowResult>
- **错误行**: 5

**问题 #361** (第 5204 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsc9b9iyvTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpsc9b9
- **错误行**: 3

**问题 #364** (第 5229 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqdz3xt14TempValidation.java:5: 错误: 需要';'
    .newBuilder(Time.days(7))
                             ^
1 个错误

- **错误行**: 5

**问题 #1673** (第 18584 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9sdslpysTempValidation.java:3: 错误: 未结束的注释
        /**
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9sdslpysTempValidation.java:8: 错误: 进行语法分析时已到达文件结尾
}
 ^
2 个错误

- **错误行**: 3

**问题 #6557** (第 68708 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvpx0zm5aEventBuffer.java:4: 错误: 进行语法分析时已到达文件结尾
public class EventBuffer extends KeyedProcessFunction<String, Event, List<Event>> {

- **错误行**: 4


### `tutorials\01-environment-setup.md`

**问题 #5** (第 138 行, 语言: yaml)

- **错误**: mapping values are not allowed here
  in "<unicode string>", line 15, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^ (line: 15)
- **错误行**: 15
- **建议**: 检查冒号后是否有空格
- **可自动修复**: ✅

**问题 #18** (第 659 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9cd98rokTempValidation.java:5: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmp9c
- **错误行**: 5


### `tutorials\02-first-flink-job.md`

**问题 #1** (第 66 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8sm4tqepTempValidation.java:5: 错误: 找不到符号
    .flatMap(tokenizer)  // 链内
             ^
  符号:   变量 tokenizer
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 5

**问题 #15** (第 797 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp90sh_65yTempValidation.java:4: 错误: 找不到符号
Set<String> stopWords = new HashSet<>(Arrays.asList("the", "a", "is", "of"));
^
  符号:   类 Set
  位置: 类 TempValidation
C:\Us
- **错误行**: 4

**问题 #17** (第 863 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp47qkjohaTempValidation.java:5: 错误: 找不到符号
    .flatMap(new Tokenizer())
                 ^
  符号:   类 Tokenizer
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 5


### `tutorials\02-streaming-fundamentals-script.md`

**问题 #3** (第 75 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnorjqcnxTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpnor
- **错误行**: 3

**问题 #6** (第 162 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpb1ys_4pjTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #9** (第 258 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa8tjdh24TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpa8tjdh24TempValidat
- **错误行**: 4

**问题 #12** (第 384 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwm9k_w92TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwm9
- **错误行**: 3


### `tutorials\04-design-patterns-script.md`

**问题 #10** (第 544 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf0vs8lgmAsyncIOPattern.java:18: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 18

**问题 #12** (第 702 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfv07b1qrStateManagementPattern.java:25: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 25

**问题 #16** (第 1017 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpg3vt0996CheckpointPattern.java:82: 错误: 非法的表达式开始
            .addSource(new FlinkKafkaConsumer<>(...))
                                                ^
1 个错误

- **错误行**: 82


### `tutorials\05-production-deployment-script.md`

**问题 #4** (第 144 行, 语言: yaml)

- **错误**: expected '<document start>', but found ('<scalar>',)
  in "<unicode string>", line 7, column 1:
    kubectl wait --for=condition=rea ...
    ^ (line: 7)
- **错误行**: 7


### `tutorials\06-advanced-topics-script.md`

**问题 #7** (第 310 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiw8jb6cdStateTTLConfiguration.java:49: 错误: 非法的表达式开始
        DataStream<Event> stream = env.addSource(...);
                                                 ^
1 个错误
- **错误行**: 49

**问题 #13** (第 855 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps76tnc3jSkewHandling.java:16: 错误: 非法的表达式开始
        DataStream<Event> source = env.addSource(...);
                                                 ^
1 个错误

- **错误行**: 16

**问题 #17** (第 1231 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphatcyob7LargeStateOptimization.java:32: 错误: 非法的表达式开始
        DataStream<Event> source = env.addSource(...);
                                                 ^
1 个错
- **错误行**: 32


### `tutorials\hands-on-labs\lab-07-flink-sql.md`

**问题 #5** (第 101 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpd1kelx5bTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.TableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpd1kelx5bTemp
- **错误行**: 3

**问题 #6** (第 123 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7b0ruv3dTempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql("""
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp7b0ruv3dTempVali
- **错误行**: 4

**问题 #7** (第 148 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr_03krizTempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql("""
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #8** (第 171 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpztiwignlTempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql("""
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpztiwignlTempVali
- **错误行**: 4

**问题 #9** (第 208 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpluz2zb2wTempValidation.java:4: 错误: 找不到符号
Table result = tableEnv.sqlQuery("SELECT * FROM user_events");
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4

**问题 #10** (第 227 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpi4x5ya17TempValidation.java:4: 错误: 找不到符号
Table userStats = tableEnv.sqlQuery("""
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpi4x5
- **错误行**: 4

**问题 #11** (第 260 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmph1ps3pfmTempValidation.java:4: 错误: 找不到符号
Table tumbleWindow = tableEnv.sqlQuery("""
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmph
- **错误行**: 4

**问题 #12** (第 293 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkdrkstmtTempValidation.java:4: 错误: 找不到符号
Table hopWindow = tableEnv.sqlQuery("""
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpkdrk
- **错误行**: 4

**问题 #13** (第 311 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv4bahh2_TempValidation.java:4: 错误: 找不到符号
Table sessionWindow = tableEnv.sqlQuery("""
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmp
- **错误行**: 4

**问题 #14** (第 330 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp56vt8tznTempValidation.java:4: 错误: 找不到符号
Table cumulateWindow = tableEnv.sqlQuery("""
^
  符号:   类 Table
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tm
- **错误行**: 4

**问题 #15** (第 350 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv4s_4t3mTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpv4s
- **错误行**: 3

**问题 #16** (第 384 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwvqx6s7cTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpwvq
- **错误行**: 3

**问题 #17** (第 406 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpp8snu428TempValidation.java:3: 错误: 非法的表达式开始
        import static org.apache.flink.table.api.Expressions.*;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpp8snu428
- **错误行**: 3

**问题 #19** (第 555 行, 语言: sql)

- **错误**: 可能的语法问题: -- 验证表结构
DESCRIBE USER_EVENTS;...

**问题 #26** (第 718 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpx38_pel5TempValidation.java:4: 错误: 找不到符号
tableEnv.getConfig().set("table.exec.source.idle-timeout", "10s");
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #27** (第 729 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp5l77rc9jTempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql("DROP TABLE IF EXISTS user_events");
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppDa
- **错误行**: 4

**问题 #28** (第 742 行, 语言: sql)

- **错误**: 可能的语法问题: -- 从最早偏移量开始
'SCAN.STARTUP.MODE' = 'EARLIEST-OFFSET...

**问题 #29** (第 756 行, 语言: sql)

- **错误**: 可能的语法问题: -- 启用 MINI-BATCH 优化
TABLEENV.GETCONFIG().SET("TABL...; 可能的语法问题: TABLEENV.GETCONFIG().SET("TABLE.EXEC.MINI-BATCH.AL...; 可能的语法问题: TABLEENV.GETCONFIG().SET("TABLE.EXEC.MINI-BATCH.SI...; 可能的语法问题:


### `tutorials\hands-on-labs\lab-08-connectors.md`

**问题 #7** (第 154 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxb3ije01TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpxb3
- **错误行**: 3

**问题 #8** (第 187 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy93zwhiqTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.connector.kafka.sink.KafkaSink;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpy93zwhiq
- **错误行**: 3

**问题 #9** (第 207 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp7k59fbrqTempValidation.java:4: 错误: 找不到符号
KafkaSink<Event> advancedSink = KafkaSink.<Event>builder()
^
  符号:   类 KafkaSink
  位置: 类 TempValidation
C:\Users\luyan\App
- **错误行**: 4

**问题 #10** (第 243 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpubusu576TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
        ^
C:\Users\luyan\AppData\Local\Te
- **错误行**: 3

**问题 #12** (第 322 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6ap58zt1TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.connector.jdbc.JdbcConnectionOptions;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp6a
- **错误行**: 3

**问题 #13** (第 365 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvcv_qj7pTempValidation.java:4: 错误: 找不到符号
JdbcExecutionOptions execOptions = JdbcExecutionOptions.builder()
^
  符号:   类 JdbcExecutionOptions
  位置: 类 TempValidation

- **错误行**: 4

**问题 #14** (第 400 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpyarj_r8oTempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql("""
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpyarj_r8oTempVali
- **错误行**: 4

**问题 #16** (第 454 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgza1oj_fElasticsearchConnectorDemo.java:19: 错误: 非法的表达式开始
        DataStream<Event> events = ...;
                                   ^
1 个错误

- **错误行**: 19

**问题 #17** (第 508 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpcwk5iv50TempValidation.java:5: 错误: 找不到符号
tableEnv.executeSql("""
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpcwk5iv50TempVali
- **错误行**: 5

**问题 #18** (第 562 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkc3krx8mTempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql("""
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpkc3krx8mTempVali
- **错误行**: 4

**问题 #19** (第 608 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpvd_vtp4cTempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql("""
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpvd_vtp4cTempVali
- **错误行**: 4

**问题 #20** (第 652 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpne0c73trTempValidation.java:4: 错误: 找不到符号
tableEnv.executeSql("""
^
  符号:   变量 tableEnv
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpne0c73trTempVali
- **错误行**: 4

**问题 #24** (第 792 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpv882wv6sAvroDeserializationSchema.java:1: 错误: 需要 class、interface、enum 或 record
<dependency>

^
1 个错误

- **错误行**: 1

**问题 #27** (第 899 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp20u2p9ezTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp20u2p
- **错误行**: 3

**问题 #29** (第 929 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpanjysgytTempValidation.java:4: 错误: 找不到符号
MySqlSource<String> mySqlSource = MySqlSource.<String>builder()
^
  符号:   类 MySqlSource
  位置: 类 TempValidation
C:\Users\lu
- **错误行**: 4

**问题 #30** (第 953 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpfplbz9itTempValidation.java:4: 错误: 非法的表达式开始
.setProperty("connections.max.idle.ms", "540000")
^
C:\Users\luyan\AppData\Local\Temp\tmpfplbz9itTempValidation.java:6:
- **错误行**: 4

**问题 #31** (第 969 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpgth48y_yTempValidation.java:4: 错误: 找不到符号
JdbcConnectionOptions.builder()
^
  符号:   变量 JdbcConnectionOptions
  位置: 类 TempValidation
1 个错误

- **错误行**: 4

**问题 #32** (第 988 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp29zs7gfmTempValidation.java:14: 错误: 需要';'
    })
      ^
1 个错误

- **错误行**: 14

**问题 #33** (第 1009 行, 语言: sql)

- **错误**: 可能的语法问题: -- 检查分区时间设置
'SINK.PARTITION-COMMIT.TRIGGER' = 'PRO...

**问题 #34** (第 1020 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf6ji7gi6TempValidation.java:10: 错误: 非法的表达式开始
.setProperty("lookup.async", "true")
^
C:\Users\luyan\AppData\Local\Temp\tmpf6ji7gi6TempValidation.java:11: 错误: 需要';'

- **错误行**: 10


### `tutorials\interactive\coding-challenges\challenge-01-hot-items.md`

**问题 #5** (第 94 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxb5rlnbyUserBehaviorSource.java:5: 错误: 非法的表达式开始
    private String[] users = {"user_001", "user_002", "user_003", ...};

- **错误行**: 5

**问题 #9** (第 298 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp94cheqteTempValidation.java:4: 错误: 需要';'
public void testHotItems() throws Exception {
                        ^
C:\Users\luyan\AppData\Local\Temp\tmp94cheqteTempV
- **错误行**: 4

**问题 #11** (第 348 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpxl_zesa_TempValidation.java:6: 错误: 非法的表达式开始
    .window(...)
            ^
C:\Users\luyan\AppData\Local\Temp\tmpxl_zesa_TempValidation.java:7: 错误: 非法的表达式开始
    .ag
- **错误行**: 6

**问题 #12** (第 360 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpf912km3xTempValidation.java:4: 错误: 找不到符号
windowedCounts.addSink(new RedisSink<>(
^
  符号:   变量 windowedCounts
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Te
- **错误行**: 4


### `tutorials\interactive\coding-challenges\challenge-03-order-timeout.md`

**问题 #3** (第 104 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpun07vftuTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpun0
- **错误行**: 3

**问题 #10** (第 664 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp37cjhdemTempValidation.java:4: 错误: 需要';'
public void testOrderTimeout() throws Exception {
                            ^
C:\Users\luyan\AppData\Local\Temp\tmp37cjh
- **错误行**: 4

**问题 #11** (第 728 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4iktf0m4MultiLevelTimeout.java:3: 错误: 非法的类型开始
public class MultiLevelTimeout extends KeyedProcessFunction<...> {

- **错误行**: 3

**问题 #12** (第 771 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpluwwjbe9OrderWithInventory.java:5: 错误: 非法的类型开始
public class OrderWithInventory extends KeyedProcessFunction<...> {

- **错误行**: 5


### `tutorials\interactive\coding-challenges\challenge-04-recommendation.md`

**问题 #4** (第 206 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpt4906taxCollaborativeFiltering.java:22: 错误: 非法的表达式开始
                ctx.getBroadcastState(...).immutableEntries()) {
                                      ^
C:\Us
- **错误行**: 22

**问题 #6** (第 376 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpl2c34na5RealtimeRecommendationJob.java:15: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 15

**问题 #8** (第 472 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6o25l9v3ABTestSplit.java:4: 错误: 非法的类型开始
    public void processElement(UserProfile profile, Context ctx, ...) {

- **错误行**: 4


### `tutorials\interactive\coding-challenges\challenge-05-data-pipeline.md`

**问题 #2** (第 64 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy1x0qvqxCDCSourceConfig.java:21: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<String> cdcStream = env
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 21


### `tutorials\interactive\hands-on-labs\lab-01-first-flink-program.md`

**问题 #12** (第 268 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpnj0f33wgTempValidation.java:3: 错误: 找不到符号
if (word.length() >= 3) {
    ^
  符号:   变量 word
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tmpnj0f33wgTempVa
- **错误行**: 3


### `tutorials\interactive\hands-on-labs\lab-02-event-time.md`

**问题 #4** (第 132 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpa8z16netTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpa8z
- **错误行**: 3


### `tutorials\interactive\hands-on-labs\lab-03-window-aggregation.md`

**问题 #3** (第 146 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps02owy4tSlidingWindowExample.java:19: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 19

**问题 #4** (第 203 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp0e00teauSessionWindowExample.java:21: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 21

**问题 #6** (第 378 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzeret_zmEnrichmentFunction.java:7: 错误: 未命名类 是预览功能，默认情况下禁用。
DataStream<WindowStats> results = stream
^
  （请使用 --enable-preview 以启用 未命名类）
1 个错误

- **错误行**: 7

**问题 #7** (第 421 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4x_zharrCountTrigger.java:58: 错误: 需要 class、interface、enum 或 record
stream.keyBy(...)
^
1 个错误

- **错误行**: 58

**问题 #8** (第 497 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3pfa5dxvWindowBenchmark.java:9: 错误: 非法的表达式开始
        stream.window(...)
                      ^
C:\Users\luyan\AppData\Local\Temp\tmp3pfa5dxvWindowBenchmark.java:1
- **错误行**: 9

**问题 #10** (第 566 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6v351_37TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.datastream.DataStream;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp6v3
- **错误行**: 3


### `tutorials\interactive\hands-on-labs\lab-04-state-management.md`

**问题 #5** (第 281 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqt9lc6m2StatefulFunctionWithTTL.java:9: 错误: 非法的类型开始
public class StatefulFunctionWithTTL extends KeyedProcessFunction<...> {

- **错误行**: 9

**问题 #7** (第 381 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp3p6jsfe1TempValidation.java:4: 错误: 需要';'
public void testTemperatureAlert() throws Exception {
                                ^
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #9** (第 447 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmphgfkkgq6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.api.common.state.ValueState;
        ^
C:\Users\luyan\AppData\Local\Temp\tmphgfkkgq6Tem
- **错误行**: 3


### `tutorials\interactive\hands-on-labs\lab-05-checkpoint.md`

**问题 #3** (第 86 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpj9_4wz5aStateBackendConfig.java:15: 错误: 需要')'或','
                env.setStateBackend(new HashMapStateBackend()  // MemoryStateBackend已弃用,使用HashMapStateBackend

- **错误行**: 15

**问题 #4** (第 134 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpayxf7679TempValidation.java:4: 错误: 找不到符号
env.setStateBackend(new RocksDBStateBackend(
                        ^
  符号:   类 RocksDBStateBackend
  位置: 类 TempValidatio
- **错误行**: 4

**问题 #8** (第 239 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8bbgai4rTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
^
C:\Users\luyan\AppData\Local\Temp\tmp8b
- **错误行**: 4

**问题 #10** (第 304 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4_9ianggTempValidation.java:4: 错误: 找不到符号
FlinkKafkaConsumer<String> kafkaSource = new FlinkKafkaConsumer<>(
^
  符号:   类 FlinkKafkaConsumer
  位置: 类 TempValidation
C
- **错误行**: 4

**问题 #11** (第 340 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpw9cgtgvlTempValidation.java:4: 错误: 找不到符号
env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\L
- **错误行**: 4


### `tutorials\interactive\hands-on-labs\lab-06-cep.md`

**问题 #2** (第 36 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpe0xkctliBasicCEPExample.java:22: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 22

**问题 #3** (第 122 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp4y8n0355TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmp4y8n0355TempValidatio
- **错误行**: 4

**问题 #4** (第 164 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp8cbz6sfdTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp8cbz6
- **错误行**: 3

**问题 #5** (第 196 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpqqw_tjamTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpqqw_tjamTempValidatio
- **错误行**: 4

**问题 #6** (第 241 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpwuvvat36TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmpwuvvat36TempValidat
- **错误行**: 4

**问题 #7** (第 286 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplv29axpnFraudDetectionCEP.java:14: 错误: 非法的表达式开始
            .assignTimestampsAndWatermarks(...);
                                           ^
1 个错误

- **错误行**: 14

**问题 #8** (第 362 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpuarb85v6TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpuarb85v6TempValidatio
- **错误行**: 4

**问题 #9** (第 395 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9k1z6v4mTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp9k1z6
- **错误行**: 3

**问题 #10** (第 421 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmps5j63h9kTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmps5j63h9kTempValidatio
- **错误行**: 4


### `tutorials\interactive\quizzes\comprehensive-test.md`

**问题 #1** (第 439 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpsnul6apqTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmpsnul6apqTempValidatio
- **错误行**: 4


### `visuals\cognitive-architecture-multidimensional-atlas.md`

**问题 #20** (第 1358 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp6_a37lgpTempValidation.java:4: 错误: 找不到符号
DataStream<SensorEvent> sensorStream = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp
- **错误行**: 4

**问题 #21** (第 1387 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp03pslnazTempValidation.java:4: 错误: 找不到符号
DataStream<UserAction> actionStream = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\
- **错误行**: 4

**问题 #22** (第 1418 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpr4kvu_13TempValidation.java:4: 错误: 找不到符号
DataStream<VideoFrame> videoStream = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\t
- **错误行**: 4

**问题 #23** (第 1446 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpbx2mjhmcTempValidation.java:4: 错误: 找不到符号
DataStream<CustomerQuery> queryStream = env
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Tem
- **错误行**: 4


### `visuals\layer-decidability.md`

**问题 #1** (第 120 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpiwggisk6TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.windowing.time.Time;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpiwggi
- **错误行**: 3


### `visuals\selection-tree-consistency.md`

**问题 #3** (第 181 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp9yhvi5auTempValidation.java:4: 错误: 找不到符号
env.disableCheckpointing();  // 禁用 Checkpoint
^
  符号:   变量 env
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\Temp\tm
- **错误行**: 4

**问题 #5** (第 227 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpzd8h_ttlTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmpzd8h_tt
- **错误行**: 3

**问题 #7** (第 288 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp1ah_r752TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.CheckpointingMode;
        ^
C:\Users\luyan\AppData\Local\Temp\tmp1ah_r75
- **错误行**: 3

**问题 #12** (第 441 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpkmvf2k5aTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #13** (第 461 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmp30bvupqpTempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3

**问题 #14** (第 486 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpy2paa8_9TempValidation.java:3: 错误: 非法的表达式开始
        import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
        ^
C:\Users\luyan\AppData\
- **错误行**: 3


### `whitepaper-streaming-2027.md`

**问题 #7** (第 443 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmplap2bl70TempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.datastream.DataStream;
^
C:\Users\luyan\AppData\Local\Temp\tmplap2bl70TempValidat
- **错误行**: 4

**问题 #19** (第 967 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmppyco_j5dTempValidation.java:4: 错误: 非法的表达式开始
import org.apache.flink.streaming.api.windowing.time.Time;
^
C:\Users\luyan\AppData\Local\Temp\tmppyco_j5dTempValidatio
- **错误行**: 4

**问题 #21** (第 1077 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpjpv37ehhSessionFeatureAggregate.java:1: 错误: 程序包org.apache.flink.api.common.functions不存在
import org.apache.flink.api.common.functions.AggregateFunction;

- **错误行**: 1


### `whitepapers\realtime-ai-architecture-practices.md`

**问题 #8** (第 307 行, 语言: java)

- **错误**: C:\Users\luyan\AppData\Local\Temp\tmpk6w2nrsdTempValidation.java:4: 错误: 找不到符号
DataStream<UserFeature> userFeatures = events
^
  符号:   类 DataStream
  位置: 类 TempValidation
C:\Users\luyan\AppData\Local\T
- **错误行**: 4


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
