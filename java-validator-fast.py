#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Java代码验证器 - 快速版本
"""

import re
import os
import sys
import json
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

# Flink/Java 常见类的import映射
FLINK_IMPORTS = {
    'StreamExecutionEnvironment': 'org.apache.flink.streaming.api.environment.StreamExecutionEnvironment',
    'DataStream': 'org.apache.flink.streaming.api.datastream.DataStream',
    'SingleOutputStreamOperator': 'org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator',
    'ConnectedStreams': 'org.apache.flink.streaming.api.datastream.ConnectedStreams',
    'KeyedStream': 'org.apache.flink.streaming.api.datastream.KeyedStream',
    'WindowedStream': 'org.apache.flink.streaming.api.datastream.WindowedStream',
    'WatermarkStrategy': 'org.apache.flink.api.common.eventtime.WatermarkStrategy',
    'WatermarkGenerator': 'org.apache.flink.api.common.eventtime.WatermarkGenerator',
    'TimestampAssigner': 'org.apache.flink.api.common.eventtime.TimestampAssigner',
    'SerializableTimestampAssigner': 'org.apache.flink.api.common.eventtime.SerializableTimestampAssigner',
    'TimeWindow': 'org.apache.flink.streaming.api.windowing.windows.TimeWindow',
    'GlobalWindow': 'org.apache.flink.streaming.api.windowing.windows.GlobalWindow',
    'TumblingEventTimeWindows': 'org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows',
    'TumblingProcessingTimeWindows': 'org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows',
    'SlidingEventTimeWindows': 'org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows',
    'SlidingProcessingTimeWindows': 'org.apache.flink.streaming.api.windowing.assigners.SlidingProcessingTimeWindows',
    'EventTimeSessionWindows': 'org.apache.flink.streaming.api.windowing.assigners.EventTimeSessionWindows',
    'ProcessingTimeSessionWindows': 'org.apache.flink.streaming.api.windowing.assigners.ProcessingTimeSessionWindows',
    'Trigger': 'org.apache.flink.streaming.api.windowing.triggers.Trigger',
    'TriggerResult': 'org.apache.flink.streaming.api.windowing.triggers.TriggerResult',
    'Evictor': 'org.apache.flink.streaming.api.windowing.evictors.Evictor',
    'ValueState': 'org.apache.flink.api.common.state.ValueState',
    'ValueStateDescriptor': 'org.apache.flink.api.common.state.ValueStateDescriptor',
    'ListState': 'org.apache.flink.api.common.state.ListState',
    'ListStateDescriptor': 'org.apache.flink.api.common.state.ListStateDescriptor',
    'MapState': 'org.apache.flink.api.common.state.MapState',
    'MapStateDescriptor': 'org.apache.flink.api.common.state.MapStateDescriptor',
    'ReducingState': 'org.apache.flink.api.common.state.ReducingState',
    'ReducingStateDescriptor': 'org.apache.flink.api.common.state.ReducingStateDescriptor',
    'AggregatingState': 'org.apache.flink.api.common.state.AggregatingState',
    'AggregatingStateDescriptor': 'org.apache.flink.api.common.state.AggregatingStateDescriptor',
    'StateTtlConfig': 'org.apache.flink.api.common.state.StateTtlConfig',
    'CheckpointListener': 'org.apache.flink.streaming.api.checkpoint.CheckpointListener',
    'CheckpointedFunction': 'org.apache.flink.streaming.api.checkpoint.CheckpointedFunction',
    'ListCheckpointed': 'org.apache.flink.streaming.api.checkpoint.ListCheckpointed',
    'CheckpointingMode': 'org.apache.flink.streaming.api.CheckpointingMode',
    'MapFunction': 'org.apache.flink.api.common.functions.MapFunction',
    'FlatMapFunction': 'org.apache.flink.api.common.functions.FlatMapFunction',
    'FilterFunction': 'org.apache.flink.api.common.functions.FilterFunction',
    'ReduceFunction': 'org.apache.flink.api.common.functions.ReduceFunction',
    'FoldFunction': 'org.apache.flink.api.common.functions.FoldFunction',
    'AggregateFunction': 'org.apache.flink.api.common.functions.AggregateFunction',
    'RichMapFunction': 'org.apache.flink.api.common.functions.RichMapFunction',
    'RichFlatMapFunction': 'org.apache.flink.api.common.functions.RichFlatMapFunction',
    'RichFilterFunction': 'org.apache.flink.api.common.functions.RichFilterFunction',
    'RichReduceFunction': 'org.apache.flink.api.common.functions.RichReduceFunction',
    'RichFunction': 'org.apache.flink.api.common.functions.RichFunction',
    'RuntimeContext': 'org.apache.flink.api.common.functions.RuntimeContext',
    'ProcessFunction': 'org.apache.flink.streaming.api.functions.ProcessFunction',
    'KeyedProcessFunction': 'org.apache.flink.streaming.api.functions.KeyedProcessFunction',
    'CoProcessFunction': 'org.apache.flink.streaming.api.functions.co.CoProcessFunction',
    'KeyedCoProcessFunction': 'org.apache.flink.streaming.api.functions.co.KeyedCoProcessFunction',
    'ProcessAllWindowFunction': 'org.apache.flink.streaming.api.functions.windowing.ProcessAllWindowFunction',
    'ProcessWindowFunction': 'org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction',
    'BroadcastProcessFunction': 'org.apache.flink.streaming.api.functions.co.BroadcastProcessFunction',
    'KeyedBroadcastProcessFunction': 'org.apache.flink.streaming.api.functions.co.KeyedBroadcastProcessFunction',
    'SinkFunction': 'org.apache.flink.streaming.api.functions.sink.SinkFunction',
    'RichSinkFunction': 'org.apache.flink.streaming.api.functions.sink.RichSinkFunction',
    'SourceFunction': 'org.apache.flink.streaming.api.functions.source.SourceFunction',
    'RichSourceFunction': 'org.apache.flink.streaming.api.functions.source.RichSourceFunction',
    'ParallelSourceFunction': 'org.apache.flink.streaming.api.functions.source.ParallelSourceFunction',
    'OutputTag': 'org.apache.flink.util.OutputTag',
    'Collector': 'org.apache.flink.util.Collector',
    'TypeInformation': 'org.apache.flink.api.common.typeinfo.TypeInformation',
    'TypeHint': 'org.apache.flink.api.common.typeinfo.TypeHint',
    'Types': 'org.apache.flink.api.common.typeinfo.Types',
    'SerializerConfig': 'org.apache.flink.api.common.serialization.SerializerConfig',
    'Configuration': 'org.apache.flink.configuration.Configuration',
    'ExecutionConfig': 'org.apache.flink.api.common.ExecutionConfig',
    'TableEnvironment': 'org.apache.flink.table.api.TableEnvironment',
    'StreamTableEnvironment': 'org.apache.flink.table.api.StreamTableEnvironment',
    'Table': 'org.apache.flink.table.api.Table',
    'TableDescriptor': 'org.apache.flink.table.api.TableDescriptor',
    'Schema': 'org.apache.flink.table.api.Schema',
    'DataTypes': 'org.apache.flink.table.api.DataTypes',
    'Pattern': 'org.apache.flink.cep.Pattern',
    'CEP': 'org.apache.flink.cep.CEP',
    'PatternSelectFunction': 'org.apache.flink.cep.PatternSelectFunction',
    'PatternTimeoutFunction': 'org.apache.flink.cep.PatternTimeoutFunction',
    'Counter': 'org.apache.flink.metrics.Counter',
    'Gauge': 'org.apache.flink.metrics.Gauge',
    'Histogram': 'org.apache.flink.metrics.Histogram',
    'Meter': 'org.apache.flink.metrics.Meter',
    'MetricGroup': 'org.apache.flink.metrics.MetricGroup',
}


def detect_missing_imports(code):
    """检测代码中缺少import的类"""
    missing = []
    for class_name, import_path in FLINK_IMPORTS.items():
        pattern = r'\b' + class_name + r'\b'
        if re.search(pattern, code):
            import_pattern = r'import\s+' + import_path.replace('.', r'\.') + r'\s*;'
            if not re.search(import_pattern, code):
                wildcard_pattern = r'import\s+' + import_path.rsplit('.', 1)[0].replace('.', r'\.') + r'\.\*\s*;'
                if not re.search(wildcard_pattern, code):
                    missing.append((class_name, import_path))
    return missing


def add_missing_imports(code):
    """为代码添加缺失的import语句"""
    missing = detect_missing_imports(code)
    if not missing:
        return code
    
    imports = [f"import {import_path};" for class_name, import_path in missing]
    package_match = re.search(r'^package\s+[^;]+;', code, re.MULTILINE)
    
    if package_match:
        insert_pos = package_match.end()
        return code[:insert_pos] + '\n\n' + '\n'.join(imports) + code[insert_pos:]
    else:
        return '\n'.join(imports) + '\n\n' + code


def wrap_code_if_needed(code):
    """如果代码不是完整类，则包装成完整类"""
    has_class = re.search(r'\bclass\s+\w+', code)
    has_interface = re.search(r'\binterface\s+\w+', code)
    has_enum = re.search(r'\benum\s+\w+', code)
    
    if has_class or has_interface or has_enum:
        match = re.search(r'(?:class|interface|enum)\s+(\w+)', code)
        class_name = match.group(1) if match else "Unknown"
        return code, class_name
    
    code_with_imports = add_missing_imports(code)
    wrapped = f"""public class TempValidation {{
    {code_with_imports.replace(chr(10), chr(10) + '    ')}
}}"""
    return wrapped, "TempValidation"


def validate_java_code(code):
    """验证Java代码语法"""
    if not code.strip():
        return True, None, None, None, None
    
    missing_imports = detect_missing_imports(code)
    wrapped_code, class_name = wrap_code_if_needed(code)
    
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, f"{class_name}.java")
    
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(wrapped_code)
        
        result = subprocess.run(
            ['javac', '-d', temp_dir, temp_file],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        for ext in ['.java', '.class']:
            f = temp_file.replace('.java', ext)
            if os.path.exists(f):
                os.unlink(f)
        
        if result.returncode == 0:
            return True, None, None, None, None
        else:
            error_msg = result.stderr
            issue_type = "syntax_error"
            if "找不到符号" in error_msg or "cannot find symbol" in error_msg:
                issue_type = "missing_import"
            elif "已弃用" in error_msg or "deprecated" in error_msg.lower():
                issue_type = "deprecated_api"
            
            line_match = re.search(r':(\d+):', error_msg)
            error_line = int(line_match.group(1)) if line_match else None
            
            if issue_type == "missing_import" and missing_imports:
                fixed_code = add_missing_imports(code)
                is_fixed, fix_err, _, _, _ = validate_java_code(fixed_code)
                if is_fixed:
                    return False, error_msg, error_line, issue_type, fixed_code
            
            return False, error_msg, error_line, issue_type, None
            
    except subprocess.TimeoutExpired:
        return False, "编译超时", None, "timeout", None
    except Exception as e:
        return False, f"验证错误: {str(e)}", None, "error", None


def process_file(args):
    """处理单个文件"""
    file_path, content = args
    results = []
    
    pattern = r'```(\w+)?\n(.*?)```'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    lines_before = [0]
    for i, char in enumerate(content):
        if char == '\n':
            lines_before.append(i + 1)
    
    for idx, match in enumerate(matches):
        language = (match.group(1) or "text").lower().strip()
        code = match.group(2)
        
        if language != "java":
            continue
        
        start_pos = match.start()
        line_number = sum(1 for pos in lines_before if pos <= start_pos)
        
        is_valid, error_msg, error_line, issue_type, fixed_code = validate_java_code(code)
        
        results.append({
            'file_path': file_path,
            'line_number': line_number,
            'block_index': idx,
            'is_valid': is_valid and not error_msg,
            'error_message': error_msg,
            'error_line': error_line,
            'issue_type': issue_type,
            'fixable': fixed_code is not None,
            'suggested_fix': fixed_code,
            'code_preview': code[:300] + "..." if len(code) > 300 else code
        })
    
    return results


def main():
    print("=" * 60)
    print("Java代码示例验证器 - 快速版本")
    print("=" * 60)
    
    project_root = Path('.')
    print("\n🔍 扫描Markdown文件...")
    
    md_files = list(project_root.rglob("*.md"))
    exclude_patterns = ['.git', 'node_modules', '__pycache__', '.venv', 'venv', 'archive']
    md_files = [f for f in md_files if not any(excl in str(f) for excl in exclude_patterns)]
    
    print(f"   找到 {len(md_files)} 个Markdown文件")
    
    # 准备任务
    tasks = []
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8')
            if '```java' in content:
                tasks.append((str(md_file), content))
        except:
            pass
    
    print(f"   {len(tasks)} 个文件包含Java代码")
    
    # 处理所有文件
    print("\n🔧 验证Java代码块...")
    all_results = []
    
    # 使用进程池
    cpu_count = min(multiprocessing.cpu_count(), 8)
    print(f"   使用 {cpu_count} 个进程并行处理")
    
    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        futures = {executor.submit(process_file, task): task for task in tasks}
        completed = 0
        
        for future in as_completed(futures):
            completed += 1
            if completed % 50 == 0 or completed == len(tasks):
                print(f"   进度: {completed}/{len(tasks)} 文件")
            
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as e:
                print(f"   错误: {e}")
    
    print(f"\n✅ 验证完成! 共验证 {len(all_results)} 个Java代码块")
    
    # 统计
    valid = sum(1 for r in all_results if r['is_valid'])
    invalid = len(all_results) - valid
    fixable = sum(1 for r in all_results if r['fixable'])
    
    issue_types = {}
    for r in all_results:
        if r['issue_type']:
            issue_types[r['issue_type']] = issue_types.get(r['issue_type'], 0) + 1
    
    print(f"\n📊 统计结果:")
    print(f"   - 总数: {len(all_results)}")
    print(f"   - 通过: {valid}")
    print(f"   - 失败: {invalid}")
    print(f"   - 可修复: {fixable}")
    print(f"   - 通过率: {(valid/len(all_results)*100):.2f}%" if all_results else "   - 通过率: N/A")
    
    print(f"\n📋 问题类型分布:")
    for it, count in sorted(issue_types.items(), key=lambda x: -x[1]):
        print(f"   - {it}: {count}")
    
    # 保存报告
    report = {
        'timestamp': datetime.now().isoformat(),
        'stats': {
            'total_files': len(md_files),
            'files_with_java': len(tasks),
            'total_blocks': len(all_results),
            'valid': valid,
            'invalid': invalid,
            'fixable': fixable,
            'pass_rate': (valid / len(all_results) * 100) if all_results else 0,
            'issue_types': issue_types
        },
        'results': all_results
    }
    
    with open('java-code-validation-result.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📝 JSON报告已保存: java-code-validation-result.json")
    
    # 生成Markdown报告
    generate_markdown_report(report)
    
    return report


def generate_markdown_report(data):
    """生成Markdown报告"""
    stats = data['stats']
    results = data['results']
    
    lines = []
    lines.append("# Java代码示例验证报告")
    lines.append("")
    lines.append(f"> **生成时间**: {data['timestamp']}")
    lines.append(f"> **验证器版本**: 1.0.0 (快速版本)")
    lines.append("")
    
    lines.append("## 📊 验证统计")
    lines.append("")
    lines.append("| 指标 | 数值 |")
    lines.append("|------|------|")
    lines.append(f"| 扫描文件数 | {stats['total_files']} |")
    lines.append(f"| 含Java代码的文件数 | {stats['files_with_java']} |")
    lines.append(f"| Java代码块总数 | {stats['total_blocks']} |")
    lines.append(f"| ✅ 验证通过 | {stats['valid']} |")
    lines.append(f"| ❌ 验证失败 | {stats['invalid']} |")
    lines.append(f"| 🔧 可自动修复 | {stats['fixable']} |")
    lines.append(f"| **通过率** | {stats['pass_rate']:.2f}% |")
    lines.append("")
    
    if stats['issue_types']:
        lines.append("### 问题类型分布")
        lines.append("")
        lines.append("| 问题类型 | 数量 | 说明 |")
        lines.append("|----------|------|------|")
        descriptions = {
            'missing_import': '缺少import语句',
            'deprecated_api': '使用弃用API',
            'syntax_error': '语法错误',
            'missing_context': '缺少上下文',
            'timeout': '编译超时',
            'error': '其他错误'
        }
        for it, count in sorted(stats['issue_types'].items(), key=lambda x: -x[1]):
            desc = descriptions.get(it, it)
            lines.append(f"| {it} | {count} | {desc} |")
        lines.append("")
    
    # 失败的代码清单
    invalid_results = [r for r in results if not r['is_valid']]
    if invalid_results:
        lines.append("## 🚨 问题代码清单 (前50个)")
        lines.append("")
        lines.append(f"共发现 **{len(invalid_results)}** 个有问题的Java代码示例，显示前50个：")
        lines.append("")
        
        for r in invalid_results[:50]:
            lines.append(f"### `{r['file_path']}` (第 {r['line_number']} 行)")
            lines.append("")
            if r['issue_type']:
                lines.append(f"- **问题类型**: {r['issue_type']}")
            if r['error_message']:
                err = r['error_message'][:300] + "..." if len(r['error_message']) > 300 else r['error_message']
                lines.append(f"- **错误**: {err.replace(chr(10), ' ')}")
            if r['fixable']:
                lines.append(f"- **可修复**: ✅ 是")
            lines.append("")
            lines.append("**代码预览**:")
            lines.append("```java")
            lines.append(r['code_preview'])
            lines.append("```")
            lines.append("")
    
    # 修复的代码清单
    fixable_results = [r for r in results if r['fixable'] and r['suggested_fix']]
    if fixable_results:
        lines.append(f"## 🔧 修复的代码清单 (前30个)")
        lines.append("")
        lines.append(f"共修复 **{len(fixable_results)}** 个代码示例，显示前30个：")
        lines.append("")
        
        for r in fixable_results[:30]:
            lines.append(f"### `{r['file_path']}` (第 {r['line_number']} 行)")
            lines.append("")
            lines.append("**原始代码**:")
            lines.append("```java")
            lines.append(r['code_preview'])
            lines.append("```")
            lines.append("")
            lines.append("**修复后代码**:")
            lines.append("```java")
            fix = r['suggested_fix'][:400] + "..." if len(r['suggested_fix']) > 400 else r['suggested_fix']
            lines.append(fix)
            lines.append("```")
            lines.append("")
    
    # 需要人工审核的案例
    complex_results = [r for r in results if not r['is_valid'] and not r['fixable']]
    if complex_results:
        lines.append("## ⚠️ 需要人工审核的复杂案例 (前30个)")
        lines.append("")
        lines.append(f"共 **{len(complex_results)}** 个案例需要人工处理，显示前30个：")
        lines.append("")
        for r in complex_results[:30]:
            lines.append(f"- `{r['file_path']}` 第 {r['line_number']} 行: {r['issue_type'] or '未知问题'}")
        lines.append("")
    
    lines.append("## 💡 改进建议")
    lines.append("")
    lines.append("1. **添加import语句**: 对于缺少import的代码，建议添加必要的import语句")
    lines.append("2. **更新弃用API**: 对于使用弃用API的代码，建议迁移到新API")
    lines.append("3. **提供上下文**: 对于片段代码，建议添加必要的上下文注释")
    lines.append("4. **代码完整性**: 确保代码示例是完整的、可运行的")
    lines.append("")
    
    with open('CODE-VALIDATION-JAVA-REPORT.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"📝 Markdown报告已保存: CODE-VALIDATION-JAVA-REPORT.md")


if __name__ == '__main__':
    main()
