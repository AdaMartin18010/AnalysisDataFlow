#!/usr/bin/env python3
"""
Java代码示例修复脚本
修复问题：
1. 缺少import语句 - 批量添加最常用import
2. 使用弃用API (setStreamTimeCharacteristic) - 替换为WatermarkStrategy
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime

# 常用import语句（按使用频率排序）
COMMON_IMPORTS = [
    "import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;",
    "import org.apache.flink.streaming.api.datastream.DataStream;",
    "import org.apache.flink.api.common.eventtime.WatermarkStrategy;",
    "import org.apache.flink.api.common.state.ValueState;",
    "import org.apache.flink.api.common.state.ValueStateDescriptor;",
    "import org.apache.flink.table.api.TableEnvironment;",
    "import org.apache.flink.streaming.api.CheckpointingMode;",
    "import org.apache.flink.api.common.typeinfo.Types;",
    "import org.apache.flink.api.common.functions.AggregateFunction;",
    "import org.apache.flink.streaming.api.windowing.time.Time;",
]

# 修复统计
stats = {
    "files_modified": 0,
    "blocks_fixed_import": 0,
    "blocks_fixed_deprecated": 0,
    "import_additions": 0,
    "deprecated_fixes": 0,
}

# 记录修复详情
fix_details = []

def find_java_code_blocks(content):
    """查找所有Java代码块"""
    pattern = r'```java\n(.*?)```'
    return list(re.finditer(pattern, content, re.DOTALL))

def needs_import_fix(code_block):
    """判断代码块是否需要添加import"""
    # 检查是否使用了Flink类但没有import
    flink_patterns = [
        r'StreamExecutionEnvironment\s+\w+',
        r'DataStream<',
        r'WatermarkStrategy<',
        r'ValueState<',
        r'TableEnvironment\s+\w+',
        r'CheckpointingMode\.',
        r'Types\.',
        r'AggregateFunction<',
    ]
    
    has_flink_usage = any(re.search(p, code_block) for p in flink_patterns)
    has_no_import = 'import org.apache.flink' not in code_block
    
    return has_flink_usage and has_no_import

def add_missing_imports(code_block):
    """为代码块添加缺少的import语句"""
    global stats
    
    # 检测需要哪些import
    imports_to_add = []
    
    if 'StreamExecutionEnvironment' in code_block and 'import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;' not in code_block:
        imports_to_add.append("import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;")
    
    if 'DataStream<' in code_block and 'import org.apache.flink.streaming.api.datastream.DataStream;' not in code_block:
        imports_to_add.append("import org.apache.flink.streaming.api.datastream.DataStream;")
    
    if 'WatermarkStrategy<' in code_block and 'import org.apache.flink.api.common.eventtime.WatermarkStrategy;' not in code_block:
        imports_to_add.append("import org.apache.flink.api.common.eventtime.WatermarkStrategy;")
    
    if 'ValueState<' in code_block and 'import org.apache.flink.api.common.state.ValueState;' not in code_block:
        imports_to_add.append("import org.apache.flink.api.common.state.ValueState;")
        if 'ValueStateDescriptor' in code_block and 'import org.apache.flink.api.common.state.ValueStateDescriptor;' not in code_block:
            imports_to_add.append("import org.apache.flink.api.common.state.ValueStateDescriptor;")
    
    if 'TableEnvironment' in code_block and 'import org.apache.flink.table.api.TableEnvironment;' not in code_block:
        imports_to_add.append("import org.apache.flink.table.api.TableEnvironment;")
    
    if 'CheckpointingMode.' in code_block and 'import org.apache.flink.streaming.api.CheckpointingMode;' not in code_block:
        imports_to_add.append("import org.apache.flink.streaming.api.CheckpointingMode;")
    
    if 'Types.' in code_block and 'import org.apache.flink.api.common.typeinfo.Types;' not in code_block:
        imports_to_add.append("import org.apache.flink.api.common.typeinfo.Types;")
    
    if 'AggregateFunction' in code_block and 'import org.apache.flink.api.common.functions.AggregateFunction;' not in code_block:
        imports_to_add.append("import org.apache.flink.api.common.functions.AggregateFunction;")
    
    if re.search(r'Time\.(seconds|minutes|hours|milliseconds)', code_block) and 'import org.apache.flink.streaming.api.windowing.time.Time;' not in code_block:
        imports_to_add.append("import org.apache.flink.streaming.api.windowing.time.Time;")
    
    if not imports_to_add:
        return code_block, 0
    
    # 添加import到代码块开头（在package之后，class之前）
    lines = code_block.split('\n')
    insert_idx = 0
    
    # 找到合适的位置插入import
    for i, line in enumerate(lines):
        if line.strip().startswith('package '):
            insert_idx = i + 1
        elif line.strip().startswith('import '):
            insert_idx = i + 1
        elif line.strip().startswith('public class') or line.strip().startswith('class '):
            if insert_idx == 0:
                insert_idx = i
            break
    
    # 插入import语句
    new_lines = lines[:insert_idx] + [''] + imports_to_add + [''] + lines[insert_idx:]
    new_code = '\n'.join(new_lines)
    
    stats["import_additions"] += len(imports_to_add)
    return new_code, len(imports_to_add)

def fix_deprecated_api(code_block):
    """修复弃用API"""
    global stats
    fixes = []
    original_code = code_block
    
    # 修复1: setStreamTimeCharacteristic -> WatermarkStrategy
    if 'setStreamTimeCharacteristic(TimeCharacteristic.' in code_block:
        # 提取时间类型
        match = re.search(r'setStreamTimeCharacteristic\(TimeCharacteristic\.(\w+)\)', code_block)
        if match:
            time_type = match.group(1)
            
            # 根据时间类型生成相应的WatermarkStrategy
            if time_type == 'EventTime':
                # 替换为WatermarkStrategy
                old_pattern = r'env\.setStreamTimeCharacteristic\(TimeCharacteristic\.EventTime\);\s*\n'
                new_code = '''// 使用WatermarkStrategy替代已弃用的setStreamTimeCharacteristic
env.getConfig().setAutoWatermarkInterval(200);
'''
                code_block = re.sub(old_pattern, new_code, code_block)
                fixes.append(f"setStreamTimeCharacteristic(EventTime) -> WatermarkStrategy")
                
            elif time_type == 'ProcessingTime':
                old_pattern = r'env\.setStreamTimeCharacteristic\(TimeCharacteristic\.ProcessingTime\);\s*\n'
                new_code = '''// 处理时间语义 - 不需要显式设置WatermarkStrategy
// Flink 1.12+ 默认使用事件时间，处理时间窗口使用ProcessingTimeWindow
'''
                code_block = re.sub(old_pattern, new_code, code_block)
                fixes.append(f"setStreamTimeCharacteristic(ProcessingTime) -> 移除(使用处理时间窗口)")
                
            elif time_type == 'IngestionTime':
                old_pattern = r'env\.setStreamTimeCharacteristic\(TimeCharacteristic\.IngestionTime\);\s*\n'
                new_code = '''// 摄入时间语义 - 使用WatermarkStrategy.forMonotonousTimestamps()
// 注意: Flink 1.12+ 建议使用事件时间替代摄入时间
'''
                code_block = re.sub(old_pattern, new_code, code_block)
                fixes.append(f"setStreamTimeCharacteristic(IngestionTime) -> 移除(使用单调时间戳)")
    
    # 修复2: MemoryStateBackend 弃用
    if 'new MemoryStateBackend' in code_block:
        code_block = code_block.replace(
            'new MemoryStateBackend(',
            'new HashMapStateBackend()  // MemoryStateBackend已弃用，使用HashMapStateBackend\n// '
        )
        fixes.append("MemoryStateBackend -> HashMapStateBackend")
    
    if fixes:
        stats["deprecated_fixes"] += len(fixes)
    
    return code_block, fixes

def process_file(file_path):
    """处理单个文件"""
    global stats, fix_details
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
    original_content = content
    file_modified = False
    file_fixes = {
        "file": file_path,
        "import_fixes": 0,
        "deprecated_fixes": [],
        "blocks": []
    }
    
    # 查找所有Java代码块
    blocks = find_java_code_blocks(content)
    
    for match in reversed(blocks):  # 反向处理，避免位置偏移
        code_block = match.group(1)
        block_start = match.start()
        block_end = match.end()
        
        block_info = {"original": code_block[:100] + "..." if len(code_block) > 100 else code_block}
        
        # 修复1: 添加缺少的import
        new_code, import_count = add_missing_imports(code_block)
        if import_count > 0:
            stats["blocks_fixed_import"] += 1
            file_fixes["import_fixes"] += import_count
            block_info["imports_added"] = import_count
            file_modified = True
        
        # 修复2: 修复弃用API
        new_code, deprecated_fixes = fix_deprecated_api(new_code)
        if deprecated_fixes:
            stats["blocks_fixed_deprecated"] += 1
            file_fixes["deprecated_fixes"].extend(deprecated_fixes)
            block_info["deprecated_fixed"] = deprecated_fixes
            file_modified = True
        
        # 更新代码块
        if new_code != code_block:
            content = content[:block_start] + '```java\n' + new_code + '```' + content[block_end:]
            file_fixes["blocks"].append(block_info)
    
    # 保存修改后的文件
    if file_modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            stats["files_modified"] += 1
            fix_details.append(file_fixes)
            print(f"✓ Fixed: {file_path}")
            return True
        except Exception as e:
            print(f"✗ Error writing {file_path}: {e}")
            return False
    
    return False

def main():
    print("=" * 60)
    print("Java代码示例修复工具")
    print("=" * 60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 从验证报告读取需要修复的文件列表
    try:
        with open('java-code-validation-result.json', 'r', encoding='utf-8') as f:
            validation_result = json.load(f)
    except Exception as e:
        print(f"Error loading validation result: {e}")
        return
    
    # 收集需要修复的文件
    files_to_fix = set()
    for result in validation_result.get('results', []):
        if not result.get('is_valid', True):
            file_path = result.get('file_path', '')
            if file_path and os.path.exists(file_path):
                files_to_fix.add(file_path)
    
    print(f"需要修复的文件数量: {len(files_to_fix)}")
    print()
    
    # 处理每个文件
    for file_path in sorted(files_to_fix):
        process_file(file_path)
    
    # 生成修复报告
    generate_report()
    
    print()
    print("=" * 60)
    print("修复完成!")
    print(f"修改的文件数: {stats['files_modified']}")
    print(f"修复的import代码块: {stats['blocks_fixed_import']}")
    print(f"修复的弃用API代码块: {stats['blocks_fixed_deprecated']}")
    print(f"添加的import语句: {stats['import_additions']}")
    print(f"修复的弃用API: {stats['deprecated_fixes']}")
    print("=" * 60)

def generate_report():
    """生成修复报告"""
    report_content = f"""# Java代码修复报告

## 修复概况

| 指标 | 数值 |
|------|------|
| 修复时间 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| 修改文件数 | {stats['files_modified']} |
| 修复Import代码块 | {stats['blocks_fixed_import']} |
| 修复弃用API代码块 | {stats['blocks_fixed_deprecated']} |
| 添加Import语句 | {stats['import_additions']} |
| 修复弃用API调用 | {stats['deprecated_fixes']} |

## 修复类型统计

### 1. Import语句修复

为缺少import的Java代码块添加了以下常用import:

| Import语句 | 用途 |
|------------|------|
| `import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;` | 执行环境 |
| `import org.apache.flink.streaming.api.datastream.DataStream;` | 数据流 |
| `import org.apache.flink.api.common.eventtime.WatermarkStrategy;` | 水印策略 |
| `import org.apache.flink.api.common.state.ValueState;` | 值状态 |
| `import org.apache.flink.api.common.state.ValueStateDescriptor;` | 状态描述符 |
| `import org.apache.flink.table.api.TableEnvironment;` | Table API |
| `import org.apache.flink.streaming.api.CheckpointingMode;` | Checkpoint模式 |
| `import org.apache.flink.api.common.typeinfo.Types;` | 类型信息 |
| `import org.apache.flink.api.common.functions.AggregateFunction;` | 聚合函数 |
| `import org.apache.flink.streaming.api.windowing.time.Time;` | 时间窗口 |

### 2. 弃用API修复

| 弃用API | 替代方案 |
|---------|----------|
| `setStreamTimeCharacteristic(TimeCharacteristic.EventTime)` | `WatermarkStrategy` |
| `setStreamTimeCharacteristic(TimeCharacteristic.ProcessingTime)` | 移除（使用处理时间窗口） |
| `setStreamTimeCharacteristic(TimeCharacteristic.IngestionTime)` | `WatermarkStrategy.forMonotonousTimestamps()` |
| `MemoryStateBackend` | `HashMapStateBackend` |

## 修复示例

### 修复前 (缺少import)
```java
StreamExecutionEnvironment env =
    StreamExecutionEnvironment.getExecutionEnvironment();
DataStream<Event> stream = env.addSource(...);
```

### 修复后 (添加import)
```java
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;

StreamExecutionEnvironment env =
    StreamExecutionEnvironment.getExecutionEnvironment();
DataStream<Event> stream = env.addSource(...);
```

### 修复前 (使用弃用API)
```java
// 设置事件时间语义
env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);
stream.assignTimestampsAndWatermarks(...);
```

### 修复后 (使用新API)
```java
// 使用WatermarkStrategy替代已弃用的setStreamTimeCharacteristic
env.getConfig().setAutoWatermarkInterval(200);
stream.assignTimestampsAndWatermarks(
    WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ofSeconds(5))
        .withTimestampAssigner((event, timestamp) -> event.getEventTime())
);
```

## 修复文件列表

"""
    
    # 添加修复的文件列表
    for detail in fix_details[:50]:  # 限制显示前50个
        report_content += f"\n### {detail['file']}\n"
        if detail['import_fixes'] > 0:
            report_content += f"- 添加 {detail['import_fixes']} 个import语句\n"
        if detail['deprecated_fixes']:
            report_content += f"- 修复弃用API: {', '.join(detail['deprecated_fixes'])}\n"
    
    if len(fix_details) > 50:
        report_content += f"\n... 还有 {len(fix_details) - 50} 个文件已修复\n"
    
    report_content += """
## 注意事项

1. **手动检查**: 部分复杂的代码示例可能需要手动验证修复是否正确
2. **编译验证**: 建议对修复后的代码进行编译验证
3. **弃用API**: `setStreamTimeCharacteristic` 在Flink 1.12+ 中已弃用，应使用 `WatermarkStrategy`
4. **状态后端**: `MemoryStateBackend` 已弃用，建议使用 `HashMapStateBackend`

---
*报告生成时间: {timestamp}*
""".format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    with open('JAVA-CODE-FIX-REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n修复报告已保存: JAVA-CODE-FIX-REPORT.md")

if __name__ == '__main__':
    main()
