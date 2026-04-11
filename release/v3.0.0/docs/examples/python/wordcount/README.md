# Flink WordCount Python示例

## 项目简介

使用PyFlink实现的WordCount示例，演示DataStream API的基本用法。

## 环境要求

- Python 3.8+
- Java 11+ (Flink依赖)
- Apache Flink 1.20+

## 快速开始

### 1. 安装依赖

```bash
cd examples/python/wordcount
pip install -r requirements.txt
```

### 2. 运行示例

```bash
# 使用演示数据运行
python wordcount.py

# 从文件读取数据
python wordcount.py --input data.txt

# 指定并行度
python wordcount.py --input data.txt --parallelism 4
```

### 3. 提交到Flink集群

```bash
# 使用flink run提交
flink run -py wordcount.py

# 指定Python虚拟环境
flink run -py wordcount.py -pyenv /path/to/venv
```

## 项目结构

```
wordcount/
├── wordcount.py      # 主程序
├── requirements.txt  # 依赖配置
├── README.md         # 本文件
└── test_wordcount.py # 单元测试
```

## 代码说明

### Tokenizer类

```python
class Tokenizer(FlatMapFunction):
    """自定义分词器"""
    def flat_map(self, value: str, collector):
        words = value.lower().split()
        for word in words:
            collector.collect((word, 1))
```

### 处理流程

1. `flat_map`: 分词转换
2. `key_by`: 按单词分组
3. `window`: 时间窗口
4. `sum`: 聚合求和

## 输出示例

```
2024-01-15 10:30:00 - INFO - Flink WordCount Python Example
2024-01-15 10:30:05 - INFO - 使用内置演示数据
('flink', 4)
('hello', 3)
('world', 2)
('is', 1)
('awesome', 1)
('stream', 1)
('processing', 1)
```

## 自定义扩展

### 修改分词逻辑

```python
def flat_map(self, value: str, collector):
    # 只保留长度>3的单词
    words = [w for w in value.lower().split() if len(w) > 3]
    for word in words:
        collector.collect((word, 1))
```

### 使用事件时间

```python
from pyflink.common.time import Instant
from pyflink.common.watermark_strategy import WatermarkStrategy

watermark_strategy = WatermarkStrategy.for_bounded_out_of_orderness(
    Duration.of_seconds(5)
)
stream.assign_timestamps_and_watermarks(watermark_strategy)
```

## 常见问题

### Q: 找不到Java?

```bash
# 设置JAVA_HOME
export JAVA_HOME=/path/to/java
# Windows
set JAVA_HOME=C:\Program Files\Java\jdk-11
```

### Q: pip安装失败?

```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
