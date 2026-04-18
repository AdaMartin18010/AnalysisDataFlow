#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复已包装代码块中缺失的 import
"""

import re
import os

CORE_DIRS = ['Flink/03-api', 'Flink/04-runtime', 'Flink/02-core']

IMPORT_MAP = {
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
    "Tumble": "import org.apache.flink.table.api.Tumble;",
    "JoinHint": "import org.apache.flink.table.api.JoinHint;",
    "Schema": "import org.apache.flink.table.api.Schema;",
    "TableDescriptor": "import org.apache.flink.table.api.TableDescriptor;",
    "PartitionBy": "import org.apache.flink.table.api.PartitionBy;",
}

STATIC_IMPORTS = {
    "$(": "import static org.apache.flink.table.api.Expressions.$;",
    "lit(": "import static org.apache.flink.table.api.Expressions.lit;",
    "currentTimestamp()": "import static org.apache.flink.table.api.Expressions.currentTimestamp;",
    "rowNumber()": "import static org.apache.flink.table.api.Expressions.rowNumber;",
}


def fix_imports_in_block(code):
    """修复单个代码块中的缺失 import"""
    lines = code.split("\n")
    
    existing_imports = set()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import "):
            existing_imports.add(stripped)
    
    missing = []
    for symbol, imp in IMPORT_MAP.items():
        if symbol in code and imp not in existing_imports:
            missing.append(imp)
    
    for symbol, imp in STATIC_IMPORTS.items():
        if symbol in code and imp not in existing_imports:
            missing.append(imp)
    
    if not missing:
        return code
    
    # Find insertion point: after the last import, before the class declaration
    insert_idx = 0
    last_import_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("import "):
            last_import_idx = i
    
    if last_import_idx >= 0:
        insert_idx = last_import_idx + 1
    
    # Insert missing imports
    for imp in sorted(missing):
        lines.insert(insert_idx, imp)
        insert_idx += 1
    
    return "\n".join(lines)


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = False
    pattern = r"(```java\n)(.*?)(```)"
    
    def replacer(match):
        nonlocal modified
        prefix = match.group(1)
        code = match.group(2)
        suffix = match.group(3)
        
        if "public class Example" not in code:
            return match.group(0)
        
        new_code = fix_imports_in_block(code)
        if new_code != code:
            modified = True
            return prefix + new_code + "\n" + suffix
        
        return match.group(0)
    
    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
    
    return modified


def main():
    fixed_files = []
    for core_dir in CORE_DIRS:
        if not os.path.exists(core_dir):
            continue
        for root, dirs, files in os.walk(core_dir):
            for f in files:
                if not f.endswith(".md"):
                    continue
                filepath = os.path.join(root, f)
                if process_file(filepath):
                    fixed_files.append(filepath)
    
    print(f"修复了 {len(fixed_files)} 个文件中的缺失 import")


if __name__ == "__main__":
    main()
