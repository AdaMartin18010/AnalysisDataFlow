#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对核心 API 文档中的 Java 示例进行深度修复：
补充缺失的 import 和最小上下文，使其可编译。

只处理已经带有伪代码标注、且结构简单可自动包装的代码块。
"""

import re
import os

PSEUDO_COMMENT = "// [伪代码片段 - 不可直接运行] 仅展示核心逻辑"

CORE_DIRS = [
    "Flink/03-api/",
    "Flink/04-runtime/",
    "Flink/02-core/",
]

COMMON_IMPORTS = {
    "StreamExecutionEnvironment": "import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;",
    "StreamTableEnvironment": "import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;",
    "TableEnvironment": "import org.apache.flink.table.api.TableEnvironment;",
    "Table": "import org.apache.flink.table.api.Table;",
    "DataStream": "import org.apache.flink.streaming.api.datastream.DataStream;",
    "DataTypes": "import org.apache.flink.table.api.DataTypes;",
    "WatermarkStrategy": "import org.apache.flink.api.common.eventtime.WatermarkStrategy;",
    "Time": "import org.apache.flink.streaming.api.windowing.time.Time;",
    "Duration": "import java.time.Duration;",
    "Properties": "import java.util.Properties;",
    "Configuration": "import org.apache.flink.configuration.Configuration;",
    "CheckpointingMode": "import org.apache.flink.streaming.api.CheckpointingMode;",
    "TumblingEventTimeWindows": "import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;",
    "SlidingEventTimeWindows": "import org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows;",
    "EventTimeSessionWindows": "import org.apache.flink.streaming.api.windowing.assigners.EventTimeSessionWindows;",
    "CountTrigger": "import org.apache.flink.streaming.api.windowing.triggers.CountTrigger;",
    "CountEvictor": "import org.apache.flink.streaming.api.windowing.evictors.CountEvictor;",
    "StateTtlConfig": "import org.apache.flink.api.common.state.StateTtlConfig;",
    "EmbeddedRocksDBStateBackend": "import org.apache.flink.contrib.streaming.state.EmbeddedRocksDBStateBackend;",
    "HashMapStateBackend": "import org.apache.flink.runtime.state.hashmap.HashMapStateBackend;",
    "OutputTag": "import org.apache.flink.util.OutputTag;",
    "Pattern": "import org.apache.flink.cep.Pattern;",
    "CEP": "import org.apache.flink.cep.CEP;",
    "KafkaSource": "import org.apache.flink.connector.kafka.source.KafkaSource;",
    "KafkaSink": "import org.apache.flink.connector.kafka.sink.KafkaSink;",
    "FlinkKafkaConsumer": "import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;",
    "FlinkKafkaProducer": "import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;",
    "SimpleStringSchema": "import org.apache.flink.api.common.serialization.SimpleStringSchema;",
    "KafkaRecordSerializationSchema": "import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;",
    "DeliveryGuarantee": "import org.apache.flink.connector.kafka.sink.DeliveryGuarantee;",
}


def can_auto_wrap(code_text):
    """判断代码块是否适合自动包装为可运行类"""
    lines = code_text.split("\n")

    # 移除标注行
    lines = [l for l in lines if PSEUDO_COMMENT not in l]

    # 不能包含类/接口定义
    for line in lines:
        if re.search(r"\b(class|interface|enum)\s+\w+", line):
            return False

    # 不能包含 @Override 开头的方法（这些通常是 ProcessFunction 内部的方法）
    override_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("@Override"):
            override_idx = i
            break
    if override_idx is not None:
        # 检查后面是否跟着方法定义
        for i in range(override_idx + 1, min(len(lines), override_idx + 3)):
            if re.search(r"\b(public|private|protected)\s+\w+\s+\w+\s*\(", lines[i]):
                return False

    # 不能包含只是 HTTP API 路径或配置项列表的代码
    non_comment_lines = [l for l in lines if l.strip() and not l.strip().startswith("//")]
    if not non_comment_lines:
        return False

    # 检查是否有明显的 API 调用
    has_api_call = False
    for line in non_comment_lines:
        stripped = line.strip()
        if (
            stripped.startswith("env.")
            or stripped.startswith("stream.")
            or stripped.startswith("tableEnv.")
            or "DataStream<" in stripped
            or "Table " in stripped
            or "Properties " in stripped
            or "env.getConfig()" in stripped
            or "env.enableCheckpointing" in stripped
            or "env.setStateBackend" in stripped
            or "env.setParallelism" in stripped
            or "KafkaSink" in stripped
            or "KafkaSource" in stripped
            or "FlinkKafkaConsumer" in stripped
            or "FlinkKafkaProducer" in stripped
            or "StateTtlConfig" in stripped
            or "WatermarkStrategy" in stripped
        ):
            has_api_call = True
            break

    if not has_api_call:
        return False

    # 不能有未闭合的括号（简单的检查）
    open_parens = code_text.count("(")
    close_parens = code_text.count(")")
    if open_parens != close_parens:
        return False

    open_braces = code_text.count("{")
    close_braces = code_text.count("}")
    if open_braces != close_braces:
        # 如果只有一个未闭合的匿名内部类，可能还是可包装的
        if open_braces - close_braces > 1:
            return False

    return True


def wrap_codeblock(code_text):
    """将代码块包装为最小可运行类"""
    lines = code_text.split("\n")

    # 移除标注行和空的前导行
    while lines and (not lines[0].strip() or PSEUDO_COMMENT in lines[0]):
        lines.pop(0)

    # 提取 import
    imports = set()
    body_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import "):
            imports.add(stripped)
        else:
            body_lines.append(line)

    body_text = "\n".join(body_lines)

    # 推断需要的 import
    needed = set(imports)
    for symbol, imp in COMMON_IMPORTS.items():
        if symbol in body_text and imp not in needed:
            needed.add(imp)

    # 如果使用了 $() 语法（Table API），需要添加静态导入
    if '$(' in body_text and "import static org.apache.flink.table.api.Expressions.$;" not in needed:
        needed.add("import static org.apache.flink.table.api.Expressions.$;")
    if "lit(" in body_text and "import static org.apache.flink.table.api.Expressions.lit;" not in needed:
        needed.add("import static org.apache.flink.table.api.Expressions.lit;")
    if "currentTimestamp()" in body_text and "import static org.apache.flink.table.api.Expressions.currentTimestamp;" not in needed:
        needed.add("import static org.apache.flink.table.api.Expressions.currentTimestamp;")

    # 推断需要的环境变量
    needs_env = "env" in body_text and "StreamExecutionEnvironment" not in body_text
    needs_table_env = "tableEnv" in body_text and "StreamTableEnvironment" not in body_text

    # 如果 needs_table_env 为 True，则一定需要 env
    if needs_table_env:
        needs_env = True

    # 构建输出
    result_lines = []

    # 添加 import
    for imp in sorted(needed):
        result_lines.append(imp)

    if needed:
        result_lines.append("")

    result_lines.append("public class Example {")
    result_lines.append("    public static void main(String[] args) throws Exception {")

    # 添加环境变量初始化
    if needs_env and needs_table_env:
        result_lines.append("        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();")
        result_lines.append("        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);")
    elif needs_env:
        result_lines.append("        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();")
    elif needs_table_env:
        result_lines.append("        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();")
        result_lines.append("        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);")

    # 添加主体代码
    for line in body_lines:
        stripped = line.strip()
        if not stripped:
            result_lines.append("")
        elif stripped.startswith("//"):
            result_lines.append("        " + line)
        else:
            result_lines.append("        " + line)

    result_lines.append("    }")
    result_lines.append("}")

    return "\n".join(result_lines)


def process_file(filepath):
    """处理单个文件，返回修改的代码块数"""
    if not os.path.exists(filepath):
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 找到所有 java 代码块
    pattern = r"(```java\n)(.*?)(```)"

    modified = False
    count = 0

    def replacer(match):
        nonlocal modified, count
        prefix = match.group(1)
        code = match.group(2)
        suffix = match.group(3)

        if PSEUDO_COMMENT not in code:
            return match.group(0)

        if not can_auto_wrap(code):
            return match.group(0)

        new_code = wrap_codeblock(code)
        if new_code:
            modified = True
            count += 1
            return prefix + new_code + "\n" + suffix

        return match.group(0)

    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    return count


def main():
    # 收集核心目录中的所有 markdown 文件
    files = []
    for core_dir in CORE_DIRS:
        if not os.path.exists(core_dir):
            continue
        for root, dirs, filenames in os.walk(core_dir):
            for f in filenames:
                if f.endswith(".md"):
                    files.append(os.path.join(root, f))

    print(f"扫描 {len(files)} 个核心目录文件...")

    total_wrapped = 0
    modified_files = []

    for filepath in files:
        count = process_file(filepath)
        if count > 0:
            total_wrapped += count
            modified_files.append((filepath, count))

    print(f"\n包装完成:")
    print(f"  修改文件数: {len(modified_files)}")
    print(f"  包装代码块数: {total_wrapped}")

    for filepath, count in modified_files:
        print(f"  {filepath}: {count} 个")


if __name__ == "__main__":
    main()
