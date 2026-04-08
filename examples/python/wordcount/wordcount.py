#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink WordCount Python示例

功能：统计文本流中的单词频次

运行方式：
1. 本地运行: python wordcount.py
2. 指定输入: python wordcount.py --input data.txt
3. 集群提交: flink run -py wordcount.py

依赖安装：
    pip install -r requirements.txt

作者: AnalysisDataFlow Project
版本: 1.0.0
"""

import argparse
import logging
from typing import Iterable

from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.functions import FlatMapFunction, RuntimeContext
from pyflink.datastream.window import TumblingProcessingTimeWindows, Time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Tokenizer(FlatMapFunction):
    """
    分词器：将文本行拆分为单词
    
    输出格式: (word, 1)
    """
    
    def flat_map(self, value: str, collector):
        """
        将输入行分割为单词并输出(word, count)元组
        
        Args:
            value: 输入文本行
            collector: 结果收集器
        """
        # 转换为小写并按非单词字符分割
        words = value.lower().split()
        
        for word in words:
            # 去除标点符号
            clean_word = ''.join(char for char in word if char.isalnum())
            if clean_word:
                collector.collect((clean_word, 1))


def create_demo_data() -> list:
    """
    创建演示数据
    
    Returns:
        示例文本列表
    """
    return [
        "Hello Flink",
        "Hello World",
        "Flink is awesome",
        "Stream processing with Flink",
        "Hello Flink World",
        "Real-time analytics",
        "Flink rocks",
        "Hello again",
        "Apache Flink is great",
        "Stream processing made easy"
    ]


def run_wordcount(input_file: str = None):
    """
    运行WordCount程序
    
    Args:
        input_file: 可选的输入文件路径，不指定则使用演示数据
    """
    logger.info("=" * 50)
    logger.info("Flink WordCount Python Example")
    logger.info("=" * 50)
    
    # 创建执行环境
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(2)
    
    # 设置时间语义（处理时间）
    env.set_stream_time_characteristic(TimeCharacteristic.ProcessingTime)
    
    # 创建数据源
    if input_file:
        logger.info(f"从文件读取数据: {input_file}")
        # 从文件读取
        data_stream = env.read_text_file(input_file)
    else:
        logger.info("使用内置演示数据")
        logger.info("如需从文件读取，请使用: python wordcount.py --input your_file.txt")
        # 使用演示数据
        data = create_demo_data()
        data_stream = env.from_collection(data)
    
    # 数据流处理
    word_counts = (
        data_stream
        # 1. 分词
        .flat_map(
            Tokenizer(),
            output_type=Types.TUPLE([Types.STRING(), Types.INT()])
        )
        # 2. 按单词分组
        .key_by(lambda x: x[0])
        # 3. 5秒滚动窗口
        .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
        # 4. 求和
        .sum(1)
    )
    
    # 输出结果
    word_counts.print()
    
    # 执行
    logger.info("启动Flink作业...")
    env.execute("Flink WordCount Python")
    logger.info("作业执行完成")


def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(
        description='Flink WordCount Python Example',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python wordcount.py                    # 使用演示数据运行
  python wordcount.py --input data.txt   # 从文件读取数据
  flink run -py wordcount.py             # 提交到Flink集群
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        help='输入文件路径 (默认使用演示数据)'
    )
    
    parser.add_argument(
        '--parallelism', '-p',
        type=int,
        default=2,
        help='并行度 (默认: 2)'
    )
    
    args = parser.parse_args()
    
    try:
        run_wordcount(args.input)
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        raise


if __name__ == '__main__':
    main()
