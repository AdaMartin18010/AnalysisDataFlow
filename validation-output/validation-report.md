# 定理依赖验证报告

> **生成时间**: 2026-04-11 21:18:05
> **验证工具**: Theorem Dependency Validator v1.0.0

## 摘要

- **扫描文件数**: 655
- **发现元素数**: 447
- **问题总数**: 642
  - 错误: 24
  - 警告: 563
  - 信息: 55

## 统计概览

### 按类型分布

| 类型 | 数量 | 占比 |
|------|------|------|
| Cor | 4 | 0.9% |
| Def | 244 | 54.6% |
| Lemma | 99 | 22.1% |
| Prop | 27 | 6.0% |
| Thm | 73 | 16.3% |

### 按阶段分布

| 阶段 | 数量 | 说明 |
|------|------|------|
| F | 212 | Flink - Flink专项 |
| K | 137 | Knowledge - 知识结构 |
| S | 98 | Struct - 形式理论 |

### 形式化等级分布

| 等级 | 数量 |
|------|------|
| L3 | 10 |
| L4 | 20 |
| L4-L5 | 6 |
| L5 | 5 |

### 依赖覆盖

- **有依赖的元素**: 333 / 447 (74.5%)
- **有被引用的元素**: 322 / 447
- **孤立元素**: 55
- **依赖关系总数**: 809

## 关键路径

依赖图中最长的依赖链:

Def-F-14-21 -> Def-F-14-22 -> Def-F-14-23 -> Def-F-14-24 -> Def-F-14-25 -> Thm-F-14-15 -> Thm-F-14-16 -> Thm-F-14-17 -> Thm-F-14-18 -> Def-F-14-05 -> Def-F-14-06 -> Def-F-14-07 -> Def-F-14-08 -> Def-F-14-09 -> Thm-F-14-04 -> Thm-F-14-05 -> Thm-F-14-06

## 问题详情

### 错误

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-04-01 -> Thm-S-04-02 -> Thm-S-07-01 -> Thm-S-04-01
- **元素**: Thm-S-04-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-04-02 -> Thm-S-07-01 -> Thm-S-04-02
- **元素**: Thm-S-04-02
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-04-01 -> Thm-S-04-02 -> Thm-S-04-01
- **元素**: Thm-S-04-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-04-02 -> Thm-S-04-02
- **元素**: Thm-S-04-02
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-04-01 -> Thm-S-04-01
- **元素**: Thm-S-04-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-S-04-01 -> Def-S-04-02 -> Def-S-04-03 -> Def-S-04-04 -> Def-S-04-01
- **元素**: Def-S-04-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-S-04-01 -> Def-S-04-02 -> Def-S-04-03 -> Def-S-04-01
- **元素**: Def-S-04-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-S-04-01 -> Def-S-04-02 -> Def-S-04-01
- **元素**: Def-S-04-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-S-04-01 -> Def-S-04-01
- **元素**: Def-S-04-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-18-01 -> Thm-S-18-01
- **元素**: Thm-S-18-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-S-16-02 -> Def-S-16-03 -> Def-S-16-04 -> Def-S-16-02
- **元素**: Def-S-16-02
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Lemma-S-13-03 -> Lemma-S-13-03
- **元素**: Lemma-S-13-03
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Lemma-S-04-02 -> Lemma-S-04-02
- **元素**: Lemma-S-04-02
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-S-03-01 -> Thm-S-03-01
- **元素**: Thm-S-03-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-K-06-01 -> Def-K-06-07 -> Lemma-K-06-01 -> Def-K-06-02 -> Def-K-06-03 -> Def-K-06-04 -> Def-K-06-05 -> Def-K-06-06 -> Thm-K-06-01
- **元素**: Thm-K-06-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-K-06-07 -> Lemma-K-06-01 -> Def-K-06-02 -> Def-K-06-03 -> Def-K-06-04 -> Def-K-06-05 -> Def-K-06-06 -> Def-K-06-07
- **元素**: Def-K-06-07
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-K-06-01 -> Def-K-06-07 -> Lemma-K-06-01 -> Def-K-06-02 -> Def-K-06-03 -> Def-K-06-04 -> Def-K-06-05 -> Thm-K-06-01
- **元素**: Thm-K-06-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-K-06-07 -> Lemma-K-06-01 -> Def-K-06-02 -> Def-K-06-03 -> Def-K-06-04 -> Def-K-06-05 -> Def-K-06-07
- **元素**: Def-K-06-07
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-K-05-11 -> Thm-K-05-05 -> Def-K-05-11
- **元素**: Def-K-05-11
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-K-05-01 -> Def-K-05-05 -> Thm-K-05-03 -> Def-K-05-07 -> Def-K-05-08 -> Thm-K-05-04 -> Def-K-05-10 -> Def-K-05-11 -> Thm-K-05-05 -> Thm-K-05-01
- **元素**: Thm-K-05-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-K-05-05 -> Thm-K-05-05
- **元素**: Thm-K-05-05
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Def-K-05-11 -> Def-K-05-11
- **元素**: Def-K-05-11
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-K-05-01 -> Def-K-05-05 -> Thm-K-05-03 -> Def-K-05-07 -> Def-K-05-08 -> Thm-K-05-04 -> Def-K-05-10 -> Def-K-05-11 -> Thm-K-05-01
- **元素**: Thm-K-05-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

#### CIRCULAR_DEPENDENCY

- **消息**: 发现循环依赖: Thm-K-05-01 -> Def-K-05-05 -> Thm-K-05-03 -> Def-K-05-07 -> Def-K-05-08 -> Thm-K-05-04 -> Def-K-05-10 -> Thm-K-05-01
- **元素**: Thm-K-05-01
- **位置**: N/A:N/A
- **建议**: 请检查依赖关系，确保依赖图是无环的

### 警告

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-01-04
- **元素**: Thm-S-17-01
- **建议**: 请检查依赖声明或创建 Def-S-01-04

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-02-03
- **元素**: Thm-S-17-01
- **建议**: 请检查依赖声明或创建 Def-S-02-03

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-F-02-01
- **元素**: Def-F-02-91
- **建议**: 请检查依赖声明或创建 Thm-F-02-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-F-02-01
- **元素**: Lemma-F-02-70
- **建议**: 请检查依赖声明或创建 Thm-F-02-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-01
- **元素**: Def-S-12-01
- **建议**: 请检查依赖声明或创建 Thm-S-12-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-01
- **元素**: Def-S-12-02
- **建议**: 请检查依赖声明或创建 Thm-S-12-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-01
- **元素**: Def-S-12-03
- **建议**: 请检查依赖声明或创建 Thm-S-12-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-01
- **元素**: Def-S-13-01
- **建议**: 请检查依赖声明或创建 Thm-S-13-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-01
- **元素**: Def-S-13-02
- **建议**: 请检查依赖声明或创建 Thm-S-13-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-01
- **元素**: Def-S-13-03
- **建议**: 请检查依赖声明或创建 Thm-S-13-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-01
- **元素**: Def-S-13-04
- **建议**: 请检查依赖声明或创建 Thm-S-13-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-01
- **元素**: Def-S-14-03
- **建议**: 请检查依赖声明或创建 Thm-S-14-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-01
- **元素**: Def-S-15-02
- **建议**: 请检查依赖声明或创建 Thm-S-15-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-01
- **元素**: Def-S-15-03
- **建议**: 请检查依赖声明或创建 Thm-S-15-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-02
- **元素**: Def-S-15-03
- **建议**: 请检查依赖声明或创建 Thm-S-15-02

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-01
- **元素**: Def-S-15-04
- **建议**: 请检查依赖声明或创建 Thm-S-15-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-02
- **元素**: Def-S-15-04
- **建议**: 请检查依赖声明或创建 Thm-S-15-02

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-01
- **元素**: Def-S-16-02
- **建议**: 请检查依赖声明或创建 Thm-S-16-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-01
- **元素**: Def-S-16-03
- **建议**: 请检查依赖声明或创建 Thm-S-16-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-01
- **元素**: Def-S-16-04
- **建议**: 请检查依赖声明或创建 Thm-S-16-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-26-01
- **元素**: Def-S-16-08
- **建议**: 请检查依赖声明或创建 Thm-S-26-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-26-01
- **元素**: Def-S-16-09
- **建议**: 请检查依赖声明或创建 Thm-S-26-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-06
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Thm-S-12-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-03-05
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Def-S-03-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-07
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Thm-S-12-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-03-02
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Thm-S-03-02

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-08
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Thm-S-12-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-09
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Thm-S-12-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-03-04
- **元素**: Lemma-S-12-01
- **建议**: 请检查依赖声明或创建 Def-S-03-04

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-06
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Thm-S-12-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-03-05
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Def-S-03-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-07
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Thm-S-12-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-03-02
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Thm-S-03-02

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-08
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Thm-S-12-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-09
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Thm-S-12-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-03-04
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Def-S-03-04

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-10
- **元素**: Lemma-S-12-02
- **建议**: 请检查依赖声明或创建 Thm-S-12-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-06
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Thm-S-12-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-03-05
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Def-S-03-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-07
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Thm-S-12-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-03-02
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Thm-S-03-02

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-08
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Thm-S-12-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-09
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Thm-S-12-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-S-03-04
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Def-S-03-04

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-12-10
- **元素**: Lemma-S-12-03
- **建议**: 请检查依赖声明或创建 Thm-S-12-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-06
- **元素**: Lemma-S-13-01
- **建议**: 请检查依赖声明或创建 Thm-S-13-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-07
- **元素**: Lemma-S-13-01
- **建议**: 请检查依赖声明或创建 Thm-S-13-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-01
- **元素**: Lemma-S-13-01
- **建议**: 请检查依赖声明或创建 Thm-S-13-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-08
- **元素**: Lemma-S-13-01
- **建议**: 请检查依赖声明或创建 Thm-S-13-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-09
- **元素**: Lemma-S-13-01
- **建议**: 请检查依赖声明或创建 Thm-S-13-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-10
- **元素**: Lemma-S-13-01
- **建议**: 请检查依赖声明或创建 Thm-S-13-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-06
- **元素**: Lemma-S-13-02
- **建议**: 请检查依赖声明或创建 Thm-S-13-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-07
- **元素**: Lemma-S-13-02
- **建议**: 请检查依赖声明或创建 Thm-S-13-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-01
- **元素**: Lemma-S-13-02
- **建议**: 请检查依赖声明或创建 Thm-S-13-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-08
- **元素**: Lemma-S-13-02
- **建议**: 请检查依赖声明或创建 Thm-S-13-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-09
- **元素**: Lemma-S-13-02
- **建议**: 请检查依赖声明或创建 Thm-S-13-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-10
- **元素**: Lemma-S-13-02
- **建议**: 请检查依赖声明或创建 Thm-S-13-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-06
- **元素**: Lemma-S-13-03
- **建议**: 请检查依赖声明或创建 Thm-S-13-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-07
- **元素**: Lemma-S-13-03
- **建议**: 请检查依赖声明或创建 Thm-S-13-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-01
- **元素**: Lemma-S-13-03
- **建议**: 请检查依赖声明或创建 Thm-S-13-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-08
- **元素**: Lemma-S-13-03
- **建议**: 请检查依赖声明或创建 Thm-S-13-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-09
- **元素**: Lemma-S-13-03
- **建议**: 请检查依赖声明或创建 Thm-S-13-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-13-10
- **元素**: Lemma-S-13-03
- **建议**: 请检查依赖声明或创建 Thm-S-13-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-05
- **元素**: Lemma-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-06
- **元素**: Lemma-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-07
- **元素**: Lemma-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-08
- **元素**: Lemma-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-05
- **元素**: Lemma-S-14-02
- **建议**: 请检查依赖声明或创建 Thm-S-14-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-06
- **元素**: Lemma-S-14-02
- **建议**: 请检查依赖声明或创建 Thm-S-14-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-07
- **元素**: Lemma-S-14-02
- **建议**: 请检查依赖声明或创建 Thm-S-14-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-08
- **元素**: Lemma-S-14-02
- **建议**: 请检查依赖声明或创建 Thm-S-14-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-09
- **元素**: Lemma-S-14-02
- **建议**: 请检查依赖声明或创建 Thm-S-14-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-06
- **元素**: Lemma-S-15-01
- **建议**: 请检查依赖声明或创建 Thm-S-15-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-07
- **元素**: Lemma-S-15-01
- **建议**: 请检查依赖声明或创建 Thm-S-15-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-08
- **元素**: Lemma-S-15-01
- **建议**: 请检查依赖声明或创建 Thm-S-15-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-09
- **元素**: Lemma-S-15-01
- **建议**: 请检查依赖声明或创建 Thm-S-15-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-10
- **元素**: Lemma-S-15-01
- **建议**: 请检查依赖声明或创建 Thm-S-15-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-06
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Thm-S-15-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-07
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Thm-S-15-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-08
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Thm-S-15-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-09
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Thm-S-15-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-15-10
- **元素**: Lemma-S-15-02
- **建议**: 请检查依赖声明或创建 Thm-S-15-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-06
- **元素**: Lemma-S-16-01
- **建议**: 请检查依赖声明或创建 Thm-S-16-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-07
- **元素**: Lemma-S-16-01
- **建议**: 请检查依赖声明或创建 Thm-S-16-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-08
- **元素**: Lemma-S-16-01
- **建议**: 请检查依赖声明或创建 Thm-S-16-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-09
- **元素**: Lemma-S-16-01
- **建议**: 请检查依赖声明或创建 Thm-S-16-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-10
- **元素**: Lemma-S-16-01
- **建议**: 请检查依赖声明或创建 Thm-S-16-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-06
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Thm-S-16-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-07
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Thm-S-16-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-08
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Thm-S-16-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-09
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Thm-S-16-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-16-10
- **元素**: Lemma-S-16-02
- **建议**: 请检查依赖声明或创建 Thm-S-16-10

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-05
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-05

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-06
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-07
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-07

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-08
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-08

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-14-09
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-14-09

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Thm-S-08-03
- **元素**: Cor-S-14-01
- **建议**: 请检查依赖声明或创建 Thm-S-08-03

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Lemma-S-04-01
- **元素**: Lemma-S-04-02
- **建议**: 请检查依赖声明或创建 Lemma-S-04-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Prop-K-05-01
- **元素**: Thm-K-05-05
- **建议**: 请检查依赖声明或创建 Prop-K-05-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Prop-K-05-13
- **元素**: Thm-K-05-05
- **建议**: 请检查依赖声明或创建 Prop-K-05-13

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Prop-K-05-01
- **元素**: Def-K-05-10
- **建议**: 请检查依赖声明或创建 Prop-K-05-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Prop-K-05-13
- **元素**: Def-K-05-10
- **建议**: 请检查依赖声明或创建 Prop-K-05-13

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Prop-K-05-01
- **元素**: Def-K-05-11
- **建议**: 请检查依赖声明或创建 Prop-K-05-01

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Prop-K-05-13
- **元素**: Def-K-05-11
- **建议**: 请检查依赖声明或创建 Prop-K-05-13

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Def-F-15-06
- **元素**: Def-F-15-05
- **建议**: 请检查依赖声明或创建 Def-F-15-06

#### MISSING_DEPENDENCY

- **消息**: 依赖的元素不存在: Lemma-F-15-01
- **元素**: Def-F-15-14
- **建议**: 请检查依赖声明或创建 Lemma-F-15-01

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-16-08
- **元素**: Thm-S-16-08
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-14-08
- **元素**: Thm-S-14-08
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-13-06
- **元素**: Thm-S-13-06
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-15-06
- **元素**: Thm-S-15-06
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-12-06
- **元素**: Thm-S-12-06
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-15-09
- **元素**: Thm-S-15-09
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-16-06
- **元素**: Thm-S-16-06
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-13-08
- **元素**: Thm-S-13-08
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-12-08
- **元素**: Thm-S-12-08
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-12-07
- **元素**: Thm-S-12-07
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-14-07
- **元素**: Thm-S-14-07
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-15-07
- **元素**: Thm-S-15-07
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Def-S-03-05
- **元素**: Def-S-03-05
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-14-05
- **元素**: Thm-S-14-05
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-16-07
- **元素**: Thm-S-16-07
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-14-09
- **元素**: Thm-S-14-09
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-12-09
- **元素**: Thm-S-12-09
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-16-10
- **元素**: Thm-S-16-10
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-12-10
- **元素**: Thm-S-12-10
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-15-10
- **元素**: Thm-S-15-10
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-15-08
- **元素**: Thm-S-15-08
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-14-06
- **元素**: Thm-S-14-06
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-13-09
- **元素**: Thm-S-13-09
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-16-09
- **元素**: Thm-S-16-09
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Def-S-03-04
- **元素**: Def-S-03-04
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-13-10
- **元素**: Thm-S-13-10
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Prop-K-05-13
- **元素**: Prop-K-05-13
- **建议**: 请检查文档是否被删除或编号是否变更

#### REGISTRY_ORPHAN

- **消息**: 注册表中有但未在文档中找到: Thm-S-13-07
- **元素**: Thm-S-13-07
- **建议**: 请检查文档是否被删除或编号是否变更

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-206
- **元素**: Def-K-10-206
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-14-05
- **元素**: Thm-F-14-05
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-10-201
- **元素**: Thm-K-10-201
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-233
- **元素**: Def-F-07-233
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-03
- **元素**: Def-F-07-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-13-03
- **元素**: Def-S-13-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-201
- **元素**: Def-K-10-201
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-31
- **元素**: Lemma-F-07-31
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-07
- **元素**: Def-K-06-07
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-190
- **元素**: Def-K-06-190
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-03-03
- **元素**: Def-K-03-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-232
- **元素**: Lemma-F-07-232
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-35
- **元素**: Def-F-07-35
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-03
- **元素**: Def-F-14-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-252
- **元素**: Lemma-F-07-252
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-18-01
- **元素**: Lemma-S-18-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-245
- **元素**: Def-F-07-245
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-10-233
- **元素**: Thm-K-10-233
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-211
- **元素**: Def-F-07-211
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-08-02
- **元素**: Def-S-08-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-05-07
- **元素**: Def-K-05-07
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-02
- **元素**: Def-F-14-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-12
- **元素**: Lemma-F-07-12
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-15-13
- **元素**: Def-F-15-13
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-14-01
- **元素**: Lemma-S-14-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-74
- **元素**: Def-F-07-74
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-18-02
- **元素**: Lemma-S-18-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-03-22
- **元素**: Def-F-03-22
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-07-12
- **元素**: Thm-F-07-12
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-25
- **元素**: Def-F-14-25
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-07-241
- **元素**: Prop-F-07-241
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-14-22
- **元素**: Prop-F-14-22
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-212
- **元素**: Def-K-10-212
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-16-03
- **元素**: Def-S-16-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-13-01
- **元素**: Def-S-13-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-06-115
- **元素**: Thm-K-06-115
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-03-01
- **元素**: Def-K-03-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-15-08
- **元素**: Def-F-15-08
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-02-14
- **元素**: Def-S-02-14
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-K-06-126
- **元素**: Prop-K-06-126
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-202
- **元素**: Def-K-10-202
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-07-232
- **元素**: Prop-F-07-232
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-S-18-01
- **元素**: Thm-S-18-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-12-02
- **元素**: Def-S-12-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-72
- **元素**: Lemma-F-07-72
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-10-34
- **元素**: Def-F-10-34
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-75
- **元素**: Def-F-07-75
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-15-02
- **元素**: Def-S-15-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-225
- **元素**: Def-F-07-225
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-31
- **元素**: Def-F-07-31
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-172
- **元素**: Def-K-06-172
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-261
- **元素**: Def-F-07-261
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-07-211
- **元素**: Prop-F-07-211
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-01
- **元素**: Def-F-14-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-02-75
- **元素**: Def-F-02-75
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-175
- **元素**: Def-K-06-175
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-10-231
- **元素**: Lemma-K-10-231
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-05-02
- **元素**: Def-F-05-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-234
- **元素**: Def-F-07-234
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-15-12
- **元素**: Def-F-15-12
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-170
- **元素**: Def-K-06-170
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-14-01
- **元素**: Def-S-14-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-10
- **元素**: Def-F-07-10
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-06-02
- **元素**: Thm-K-06-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-262
- **元素**: Def-F-07-262
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-02-12
- **元素**: Lemma-S-02-12
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-07-231
- **元素**: Prop-F-07-231
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-02-54
- **元素**: Def-F-02-54
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-02-91
- **元素**: Def-F-02-91
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-01
- **元素**: Lemma-F-07-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-17-01
- **元素**: Def-S-17-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-205
- **元素**: Def-K-10-205
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-01
- **元素**: Lemma-K-06-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-02-77
- **元素**: Def-F-02-77
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-10-222
- **元素**: Thm-K-10-222
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-06-01
- **元素**: Prop-F-06-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-15-07
- **元素**: Def-F-15-07
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-K-06-127
- **元素**: Prop-K-06-127
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-117
- **元素**: Lemma-K-06-117
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-S-19-01
- **元素**: Thm-S-19-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-02-50
- **元素**: Def-F-02-50
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-10-02
- **元素**: Def-S-10-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-06-30
- **元素**: Thm-F-06-30
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-02-01
- **元素**: Def-K-02-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-54
- **元素**: Def-F-07-54
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-07
- **元素**: Def-F-14-07
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-05
- **元素**: Lemma-K-06-05
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-06-125
- **元素**: Thm-K-06-125
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-06-40
- **元素**: Thm-K-06-40
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-02-13
- **元素**: Lemma-S-02-13
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-10-32
- **元素**: Def-F-10-32
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-14-21
- **元素**: Thm-F-14-21
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-224
- **元素**: Def-K-10-224
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-16-02
- **元素**: Lemma-S-16-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-02-16
- **元素**: Def-S-02-16
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-51
- **元素**: Def-F-07-51
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-11
- **元素**: Def-F-07-11
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-31
- **元素**: Def-F-14-31
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-83
- **元素**: Def-K-06-83
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-10-212
- **元素**: Lemma-K-10-212
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-12-02
- **元素**: Lemma-S-12-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-07-71
- **元素**: Thm-F-07-71
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-05-01
- **元素**: Prop-F-05-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-07-50
- **元素**: Thm-F-07-50
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-07-10
- **元素**: Thm-F-07-10
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-16-02
- **元素**: Def-S-16-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-02-14
- **元素**: Lemma-S-02-14
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-04-03
- **元素**: Def-S-04-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-254
- **元素**: Def-F-07-254
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-14-22
- **元素**: Thm-F-14-22
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-12-01
- **元素**: Def-S-12-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-221
- **元素**: Lemma-F-07-221
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-10-221
- **元素**: Thm-K-10-221
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-07-52
- **元素**: Thm-F-07-52
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-14-02
- **元素**: Lemma-S-14-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-235
- **元素**: Def-K-10-235
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-14-03
- **元素**: Def-S-14-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-03-20
- **元素**: Def-F-03-20
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-04-01
- **元素**: Def-K-04-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-02-40
- **元素**: Thm-F-02-40
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-03-07
- **元素**: Prop-F-03-07
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-07-11
- **元素**: Thm-F-07-11
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-02-05
- **元素**: Lemma-K-02-05
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-15-02
- **元素**: Lemma-S-15-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-263
- **元素**: Def-F-07-263
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-234
- **元素**: Def-K-10-234
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-241
- **元素**: Lemma-F-07-241
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-02-41
- **元素**: Prop-F-02-41
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-73
- **元素**: Def-F-07-73
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-253
- **元素**: Def-F-07-253
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-03-01
- **元素**: Lemma-S-03-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-02-40
- **元素**: Prop-F-02-40
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-22
- **元素**: Def-F-14-22
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-10-16
- **元素**: Prop-F-10-16
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-30
- **元素**: Lemma-F-07-30
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-15-11
- **元素**: Def-F-15-11
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-S-17-01
- **元素**: Thm-S-17-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-15-01
- **元素**: Def-S-15-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-09-01
- **元素**: Thm-F-09-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Cor-S-02-06
- **元素**: Cor-S-02-06
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-10-17
- **元素**: Prop-F-10-17
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-243
- **元素**: Lemma-F-07-243
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-80
- **元素**: Def-K-06-80
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-02-13
- **元素**: Def-S-02-13
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-10-01
- **元素**: Def-S-10-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-223
- **元素**: Lemma-F-07-223
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-06
- **元素**: Def-F-14-06
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-243
- **元素**: Def-F-07-243
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-09-02
- **元素**: Def-S-09-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-06-31
- **元素**: Def-F-06-31
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-191
- **元素**: Def-K-06-191
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-52
- **元素**: Lemma-K-06-52
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-73
- **元素**: Def-K-06-73
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-08-04
- **元素**: Def-S-08-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-K-06-40
- **元素**: Prop-K-06-40
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-05-03
- **元素**: Thm-K-05-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-02-53
- **元素**: Def-F-02-53
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-18-03
- **元素**: Def-S-18-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-07-01
- **元素**: Def-S-07-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-255
- **元素**: Def-F-07-255
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-252
- **元素**: Def-F-07-252
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-06-32
- **元素**: Def-F-06-32
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-23
- **元素**: Def-F-14-23
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-03-15
- **元素**: Thm-F-03-15
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-35
- **元素**: Def-F-14-35
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-32
- **元素**: Def-F-14-32
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-04-02
- **元素**: Def-K-04-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-02-74
- **元素**: Def-F-02-74
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-41
- **元素**: Lemma-K-06-41
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-251
- **元素**: Lemma-F-07-251
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-71
- **元素**: Def-K-06-71
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-32
- **元素**: Def-F-07-32
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-232
- **元素**: Def-K-10-232
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-21
- **元素**: Def-F-14-21
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-18-03
- **元素**: Lemma-S-18-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-04-04
- **元素**: Def-S-04-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-05
- **元素**: Def-K-06-05
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-51
- **元素**: Lemma-F-07-51
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-265
- **元素**: Def-F-07-265
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-02-52
- **元素**: Def-F-02-52
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-72
- **元素**: Def-K-06-72
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-04-04
- **元素**: Def-K-04-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-174
- **元素**: Def-K-06-174
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-125
- **元素**: Lemma-K-06-125
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-10-231
- **元素**: Thm-K-10-231
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-221
- **元素**: Def-F-07-221
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-236
- **元素**: Def-K-10-236
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-02-42
- **元素**: Prop-F-02-42
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-07-251
- **元素**: Prop-F-07-251
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-07-01
- **元素**: Thm-K-07-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-04
- **元素**: Lemma-K-06-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-84
- **元素**: Def-K-06-84
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-10-223
- **元素**: Thm-K-10-223
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-262
- **元素**: Lemma-F-07-262
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-05-03
- **元素**: Def-F-05-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-213
- **元素**: Def-F-07-213
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-06-34
- **元素**: Def-F-06-34
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-231
- **元素**: Lemma-F-07-231
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-16-01
- **元素**: Lemma-S-16-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-12
- **元素**: Def-F-07-12
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-02-15
- **元素**: Def-S-02-15
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-10-221
- **元素**: Lemma-K-10-221
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-03-02
- **元素**: Def-K-03-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-14-11
- **元素**: Lemma-F-14-11
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-14-17
- **元素**: Thm-F-14-17
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-71
- **元素**: Def-F-07-71
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-212
- **元素**: Lemma-F-07-212
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-02-04
- **元素**: Def-K-02-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-S-04-02
- **元素**: Thm-S-04-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-04-03
- **元素**: Def-K-04-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-72
- **元素**: Def-F-07-72
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-221
- **元素**: Def-K-10-221
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-115
- **元素**: Lemma-K-06-115
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-10-232
- **元素**: Thm-K-10-232
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-233
- **元素**: Def-K-10-233
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-05-11
- **元素**: Def-K-05-11
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-193
- **元素**: Def-K-06-193
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-214
- **元素**: Def-F-07-214
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-S-04-01
- **元素**: Thm-S-04-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-03-08
- **元素**: Lemma-F-03-08
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-14-16
- **元素**: Thm-F-14-16
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-10-32
- **元素**: Thm-F-10-32
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-232
- **元素**: Def-F-07-232
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-02-23
- **元素**: Lemma-F-02-23
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-08-01
- **元素**: Def-S-08-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-33
- **元素**: Def-F-07-33
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-05-05
- **元素**: Thm-K-05-05
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-02-01
- **元素**: Lemma-F-02-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-18-04
- **元素**: Lemma-S-18-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-13-02
- **元素**: Lemma-S-13-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-15-14
- **元素**: Def-F-15-14
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-238
- **元素**: Def-K-10-238
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-05-01
- **元素**: Def-F-05-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-14-03
- **元素**: Lemma-F-14-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-33
- **元素**: Def-F-14-33
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-06
- **元素**: Lemma-K-06-06
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-07-32
- **元素**: Thm-F-07-32
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-04-02
- **元素**: Def-S-04-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-02-03
- **元素**: Def-K-02-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-02-04
- **元素**: Lemma-K-02-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-07-30
- **元素**: Thm-F-07-30
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-237
- **元素**: Def-K-10-237
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-10-211
- **元素**: Thm-K-10-211
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-02-41
- **元素**: Lemma-F-02-41
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-07-71
- **元素**: Prop-F-07-71
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-01
- **元素**: Def-K-06-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-173
- **元素**: Def-K-06-173
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-04-05
- **元素**: Def-S-04-05
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-06
- **元素**: Def-K-06-06
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-03-04
- **元素**: Def-K-03-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-73
- **元素**: Lemma-F-07-73
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-50
- **元素**: Lemma-F-07-50
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-16-01
- **元素**: Def-S-16-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-03-07
- **元素**: Lemma-F-03-07
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-51
- **元素**: Lemma-K-06-51
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-06-32
- **元素**: Thm-F-06-32
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-224
- **元素**: Def-F-07-224
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-S-08-01
- **元素**: Prop-S-08-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-10-212
- **元素**: Thm-K-10-212
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-14-21
- **元素**: Prop-F-14-21
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-244
- **元素**: Def-F-07-244
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-02-02
- **元素**: Lemma-F-02-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-06-30
- **元素**: Def-F-06-30
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-253
- **元素**: Lemma-F-07-253
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-17-02
- **元素**: Def-S-17-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-34
- **元素**: Def-F-07-34
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-S-07-01
- **元素**: Thm-S-07-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-06-01
- **元素**: Thm-K-06-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-06-03
- **元素**: Lemma-F-06-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-214
- **元素**: Def-K-10-214
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-02
- **元素**: Lemma-K-06-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-10-31
- **元素**: Def-F-10-31
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-06-33
- **元素**: Def-F-06-33
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-05
- **元素**: Def-F-14-05
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-S-02-08
- **元素**: Thm-S-02-08
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-02-45
- **元素**: Thm-F-02-45
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-20-01
- **元素**: Lemma-S-20-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-50
- **元素**: Def-F-07-50
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-225
- **元素**: Def-K-10-225
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-05-10
- **元素**: Def-K-05-10
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-03-01
- **元素**: Def-S-03-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-55
- **元素**: Def-F-07-55
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-222
- **元素**: Lemma-F-07-222
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-S-09-01
- **元素**: Thm-S-09-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-53
- **元素**: Lemma-F-07-53
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-05-02
- **元素**: Def-K-05-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-261
- **元素**: Lemma-F-07-261
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-223
- **元素**: Def-K-10-223
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-07-221
- **元素**: Prop-F-07-221
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-06-35
- **元素**: Def-F-06-35
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-18-05
- **元素**: Def-S-18-05
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-02-47
- **元素**: Thm-F-02-47
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Cor-S-14-01
- **元素**: Cor-S-14-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-235
- **元素**: Def-F-07-235
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Cor-S-02-04
- **元素**: Cor-S-02-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-213
- **元素**: Lemma-F-07-213
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-19-02
- **元素**: Def-S-19-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-15-05
- **元素**: Def-F-15-05
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-52
- **元素**: Lemma-F-07-52
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-24
- **元素**: Def-F-14-24
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-S-08-02
- **元素**: Thm-S-08-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-06-50
- **元素**: Thm-K-06-50
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-13-02
- **元素**: Def-S-13-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-01
- **元素**: Def-F-07-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-50
- **元素**: Lemma-K-06-50
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-06-03
- **元素**: Thm-K-06-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-10-35
- **元素**: Def-F-10-35
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-01-03
- **元素**: Def-K-01-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-14-01
- **元素**: Thm-F-14-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-14-02
- **元素**: Lemma-F-14-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-171
- **元素**: Def-K-06-171
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-20-04
- **元素**: Def-S-20-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-14-02
- **元素**: Def-S-14-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-06-127
- **元素**: Thm-K-06-127
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-09-01
- **元素**: Lemma-S-09-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-242
- **元素**: Lemma-F-07-242
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-34
- **元素**: Def-F-14-34
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-01-01
- **元素**: Def-K-01-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-01-04
- **元素**: Def-K-01-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-12-03
- **元素**: Lemma-S-12-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-07-31
- **元素**: Thm-F-07-31
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-215
- **元素**: Def-K-10-215
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-223
- **元素**: Def-F-07-223
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-71
- **元素**: Lemma-F-07-71
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-05-04
- **元素**: Def-K-05-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-10-232
- **元素**: Lemma-K-10-232
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-02-52
- **元素**: Thm-F-02-52
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-211
- **元素**: Lemma-F-07-211
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-14-18
- **元素**: Thm-F-14-18
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-10-202
- **元素**: Lemma-K-10-202
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-06-117
- **元素**: Thm-K-06-117
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-14-01
- **元素**: Lemma-F-14-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-242
- **元素**: Def-F-07-242
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-03-01
- **元素**: Lemma-F-03-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-116
- **元素**: Lemma-K-06-116
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-02-51
- **元素**: Def-F-02-51
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-03-21
- **元素**: Def-F-03-21
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-15-01
- **元素**: Lemma-S-15-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-09
- **元素**: Def-F-14-09
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-02-50
- **元素**: Thm-F-02-50
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-10-202
- **元素**: Thm-K-10-202
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-04
- **元素**: Def-K-06-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-17-03
- **元素**: Def-S-17-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-14-04
- **元素**: Thm-F-14-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-05-01
- **元素**: Def-K-05-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-10-222
- **元素**: Lemma-K-10-222
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-231
- **元素**: Def-K-10-231
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-241
- **元素**: Def-F-07-241
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-02
- **元素**: Lemma-F-07-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-264
- **元素**: Def-F-07-264
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-16-04
- **元素**: Def-S-16-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-222
- **元素**: Def-F-07-222
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-02
- **元素**: Def-K-06-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-12-03
- **元素**: Def-S-12-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-13-01
- **元素**: Lemma-S-13-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-05-03
- **元素**: Def-K-05-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-03-02
- **元素**: Thm-K-03-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-S-03-01
- **元素**: Thm-S-03-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-02-06
- **元素**: Lemma-K-02-06
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-204
- **元素**: Def-K-10-204
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-10-201
- **元素**: Lemma-K-10-201
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-05-04
- **元素**: Thm-K-05-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-52
- **元素**: Def-F-07-52
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-10-33
- **元素**: Def-F-10-33
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-10
- **元素**: Lemma-F-07-10
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-212
- **元素**: Def-F-07-212
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-07-51
- **元素**: Thm-F-07-51
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-01-02
- **元素**: Def-K-01-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-05-08
- **元素**: Def-K-05-08
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-195
- **元素**: Def-K-06-195
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-04-02
- **元素**: Lemma-S-04-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-30
- **元素**: Def-F-07-30
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-70
- **元素**: Def-K-06-70
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-05-01
- **元素**: Thm-K-05-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-32
- **元素**: Lemma-F-07-32
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-K-02-03
- **元素**: Prop-K-02-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-02-61
- **元素**: Def-F-02-61
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-10-30
- **元素**: Thm-F-10-30
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-02-70
- **元素**: Def-F-02-70
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-K-06-41
- **元素**: Prop-K-06-41
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-06-116
- **元素**: Thm-K-06-116
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-07-01
- **元素**: Prop-F-07-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-211
- **元素**: Def-K-10-211
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-02
- **元素**: Def-F-07-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-203
- **元素**: Def-K-10-203
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-15-04
- **元素**: Def-S-15-04
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-03
- **元素**: Def-K-06-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-10-31
- **元素**: Thm-F-10-31
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-06-51
- **元素**: Thm-K-06-51
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-14-06
- **元素**: Thm-F-14-06
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-05-05
- **元素**: Def-K-05-05
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-82
- **元素**: Def-K-06-82
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-10-213
- **元素**: Thm-K-10-213
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-263
- **元素**: Lemma-F-07-263
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-14-01
- **元素**: Prop-F-14-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-K-06-126
- **元素**: Thm-K-06-126
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-14-08
- **元素**: Def-F-14-08
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-53
- **元素**: Def-F-07-53
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-03
- **元素**: Lemma-K-06-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-06-40
- **元素**: Lemma-K-06-40
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-04-01
- **元素**: Def-S-04-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-14-23
- **元素**: Thm-F-14-23
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-14-15
- **元素**: Thm-F-14-15
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-02-63
- **元素**: Def-F-02-63
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-231
- **元素**: Def-F-07-231
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-07-11
- **元素**: Lemma-F-07-11
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-194
- **元素**: Def-K-06-194
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-02-40
- **元素**: Lemma-F-02-40
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-06-01
- **元素**: Lemma-F-06-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-07-261
- **元素**: Prop-F-07-261
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-251
- **元素**: Def-F-07-251
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-14-12
- **元素**: Lemma-F-14-12
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-S-12-01
- **元素**: Lemma-S-12-01
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-15-03
- **元素**: Def-S-15-03
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-F-07-215
- **元素**: Def-F-07-215
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-213
- **元素**: Def-K-10-213
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-06-02
- **元素**: Lemma-F-06-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-02-02
- **元素**: Def-K-02-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-14-13
- **元素**: Lemma-F-14-13
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Thm-F-06-31
- **元素**: Thm-F-06-31
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Prop-F-10-15
- **元素**: Prop-F-10-15
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-F-02-70
- **元素**: Lemma-F-02-70
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-10-222
- **元素**: Def-K-10-222
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Cor-S-02-05
- **元素**: Cor-S-02-05
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-S-18-02
- **元素**: Def-S-18-02
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Lemma-K-10-211
- **元素**: Lemma-K-10-211
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-192
- **元素**: Def-K-06-192
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

#### NOT_IN_REGISTRY

- **消息**: 文档中有但未在注册表中登记: Def-K-06-81
- **元素**: Def-K-06-81
- **建议**: 请更新THEOREM-REGISTRY.md添加此元素

### 信息

- 孤立元素: Thm-S-02-08 - (CALM定理 — Consistency As Logical Monotonicity):
- 孤立元素: Lemma-S-18-01 - （Source 可重放引理），可重放 Source 保证故障恢复后从最后一个成功 Checkpoint $C_n$ 的偏移量重放。因此所有在 $C_n$ 之后到达的记录都会被重新处理。不存在记录被永久
- 孤立元素: Lemma-S-18-02 - ，Sink 不会重新提交 $T_n$（或即使重新提交，幂等 commit 保证无重复效果）
- 孤立元素: Lemma-S-20-01 - （结合律），有限集合的最小上界可通过成对合并计算：
- 孤立元素: Thm-K-03-02 - 给定Netflix业务负载特征，Keystone平台满足：
- 孤立元素: Def-K-06-190 - [边缘流处理]: 边缘流处理是指在数据源产生地或其邻近的计算节点上，对连续到达的数据流进行实时处理、过滤、聚合和推理的计算范式。形式上，边缘流处理系统可建模为六元组：
- 孤立元素: Def-K-06-195 - [边缘运维自动化]: 边缘运维复杂度随节点数 $N$ 呈亚线性增长：
- 孤立元素: Thm-K-06-40 - (实时多模态的必要性定理): 在以下应用场景中，多模态处理的延迟约束是刚性需求：
- 孤立元素: Prop-K-06-41 - (异步推理模式): 为避免模型推理阻塞数据流，采用AsyncFunction模式：
- 孤立元素: Thm-K-06-03 - (一致性模型蕴含关系). 设：
- 孤立元素: Def-K-06-01 - (RisingWave 系统架构). RisingWave 是一个分布式流处理数据库系统，其架构可形式化定义为五元组：
- 孤立元素: Thm-K-06-115 - (视图选择NP完全性). 给定查询工作负载 $\mathcal{Q}$ 和物化视图候选集 $\mathcal{C}$，在满足存储约束 $S_{budget}$ 的前提下最大化查询性能提升的视图选择问题
- 孤立元素: Thm-K-07-01 - 对于流处理作业 $J$，测试套件 $S$ 达到完全覆盖当且仅当：
- 孤立元素: Thm-K-10-223 - (CEP检测完备性): 对于给定的CEP模式集合 $\mathcal{P}$，Flink CEP引擎能够检测所有满足模式约束的事件序列。
- 孤立元素: Thm-K-10-213 - (负荷预测准确性): 基于LSTM的短期负荷预测模型在典型场景下 MAPE < 3%。
- 孤立元素: Thm-F-02-40 - (中间结果爆炸定理): 对于 $n$ 路Join，若各流记录独立到达且匹配概率为 $p$，第 $k$ 层中间流的期望大小为：
- 孤立元素: Def-F-02-54 - (MultiJoin支持矩阵):
- 孤立元素: Lemma-F-02-01 - 的工程实现：尽管 DAG 中不同分支进度不同，但每个节点本地的 Watermark 序列都保持单调不减。
- 孤立元素: Thm-F-07-71 - (实时性价值定理): 设问题发生时刻为 $t_0$，发现时刻为 $t_d$，修复时刻为 $t_f$，则损失函数满足：
- 孤立元素: Def-F-07-01 - (实时推荐系统 Real-time Recommendation System): 实时推荐系统是一个五元组 $\mathcal{R} = (\mathcal{U}, \mathcal{I}, \ma
- ... 还有 35 个信息项

---

*报告由 Theorem Dependency Validator 自动生成*