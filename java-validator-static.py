#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Java代码验证器 - 静态分析版本
使用正则表达式进行静态分析，避免编译超时
"""

import re
import json
from pathlib import Path
from datetime import datetime

FLINK_IMPORTS = {
    'StreamExecutionEnvironment': 'org.apache.flink.streaming.api.environment.StreamExecutionEnvironment',
    'DataStream': 'org.apache.flink.streaming.api.datastream.DataStream',
    'SingleOutputStreamOperator': 'org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator',
    'ConnectedStreams': 'org.apache.flink.streaming.api.datastream.ConnectedStreams',
    'KeyedStream': 'org.apache.flink.streaming.api.datastream.KeyedStream',
    'WindowedStream': 'org.apache.flink.streaming.api.datastream.WindowedStream',
    'WatermarkStrategy': 'org.apache.flink.api.common.eventtime.WatermarkStrategy',
    'TimestampAssigner': 'org.apache.flink.api.common.eventtime.TimestampAssigner',
    'SerializableTimestampAssigner': 'org.apache.flink.api.common.eventtime.SerializableTimestampAssigner',
    'TimeWindow': 'org.apache.flink.streaming.api.windowing.windows.TimeWindow',
    'TumblingEventTimeWindows': 'org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows',
    'SlidingEventTimeWindows': 'org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows',
    'EventTimeSessionWindows': 'org.apache.flink.streaming.api.windowing.assigners.EventTimeSessionWindows',
    'ValueState': 'org.apache.flink.api.common.state.ValueState',
    'ValueStateDescriptor': 'org.apache.flink.api.common.state.ValueStateDescriptor',
    'ListState': 'org.apache.flink.api.common.state.ListState',
    'ListStateDescriptor': 'org.apache.flink.api.common.state.ListStateDescriptor',
    'MapState': 'org.apache.flink.api.common.state.MapState',
    'MapStateDescriptor': 'org.apache.flink.api.common.state.MapStateDescriptor',
    'StateTtlConfig': 'org.apache.flink.api.common.state.StateTtlConfig',
    'CheckpointedFunction': 'org.apache.flink.streaming.api.checkpoint.CheckpointedFunction',
    'MapFunction': 'org.apache.flink.api.common.functions.MapFunction',
    'FlatMapFunction': 'org.apache.flink.api.common.functions.FlatMapFunction',
    'FilterFunction': 'org.apache.flink.api.common.functions.FilterFunction',
    'ReduceFunction': 'org.apache.flink.api.common.functions.ReduceFunction',
    'AggregateFunction': 'org.apache.flink.api.common.functions.AggregateFunction',
    'RichMapFunction': 'org.apache.flink.api.common.functions.RichMapFunction',
    'ProcessFunction': 'org.apache.flink.streaming.api.functions.ProcessFunction',
    'KeyedProcessFunction': 'org.apache.flink.streaming.api.functions.KeyedProcessFunction',
    'ProcessWindowFunction': 'org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction',
    'SinkFunction': 'org.apache.flink.streaming.api.functions.sink.SinkFunction',
    'SourceFunction': 'org.apache.flink.streaming.api.functions.source.SourceFunction',
    'OutputTag': 'org.apache.flink.util.OutputTag',
    'Collector': 'org.apache.flink.util.Collector',
    'TypeInformation': 'org.apache.flink.api.common.typeinfo.TypeInformation',
    'Types': 'org.apache.flink.api.common.typeinfo.Types',
    'Configuration': 'org.apache.flink.configuration.Configuration',
    'TableEnvironment': 'org.apache.flink.table.api.TableEnvironment',
    'StreamTableEnvironment': 'org.apache.flink.table.api.StreamTableEnvironment',
    'Table': 'org.apache.flink.table.api.Table',
    'DataTypes': 'org.apache.flink.table.api.DataTypes',
    'Pattern': 'org.apache.flink.cep.Pattern',
    'CEP': 'org.apache.flink.cep.CEP',
}

# 弃用API模式
DEPRECATED_PATTERNS = [
    (r'env\.setStreamTimeCharacteristic', 'setStreamTimeCharacteristic已弃用'),
    (r'\.fold\s*\(', 'fold操作已弃用，请使用AggregateFunction'),
    (r'ExecutionConfig\.setAutoWatermarkInterval', '请使用WatermarkStrategy.withIdleness()'),
]

# 常见语法问题
SYNTAX_PATTERNS = [
    (r'\{[^}]*$', '可能缺少闭合大括号'),
    (r'\([^)]*$', '可能缺少闭合括号'),
    (r'\{[^}]*\{[^}]*\}[^}]*$', '大括号可能不匹配'),
]


def detect_missing_imports(code):
    """检测缺少的import"""
    missing = []
    for class_name, import_path in FLINK_IMPORTS.items():
        if re.search(r'\b' + class_name + r'\b', code):
            if not re.search(r'import\s+' + import_path.replace('.', r'\.') + r'\s*;', code):
                if not re.search(r'import\s+' + import_path.rsplit('.', 1)[0].replace('.', r'\.') + r'\.\*\s*;', code):
                    missing.append((class_name, import_path))
    return missing


def detect_deprecated_apis(code):
    """检测弃用API"""
    found = []
    for pattern, msg in DEPRECATED_PATTERNS:
        if re.search(pattern, code):
            found.append((pattern, msg))
    return found


def detect_syntax_issues(code):
    """检测语法问题"""
    issues = []
    
    # 检查大括号匹配
    open_braces = code.count('{')
    close_braces = code.count('}')
    if open_braces != close_braces:
        issues.append(f'大括号不匹配: {{={open_braces}, }}={close_braces}')
    
    # 检查括号匹配
    open_parens = code.count('(')
    close_parens = code.count(')')
    if open_parens != close_parens:
        issues.append(f'括号不匹配: (={open_parens}, )={close_parens}')
    
    # 检查方括号匹配
    open_brackets = code.count('[')
    close_brackets = code.count(']')
    if open_brackets != close_brackets:
        issues.append(f'方括号不匹配: [={open_brackets}, ]={close_brackets}')
    
    return issues


def analyze_code(code, file_path, line_number):
    """分析代码块"""
    result = {
        'file': file_path,
        'line': line_number,
        'valid': True,
        'issues': [],
        'missing_imports': [],
        'deprecated_apis': [],
        'syntax_issues': [],
        'is_snippet': False,
        'preview': code[:200] + "..." if len(code) > 200 else code
    }
    
    # 跳过非代码内容
    if not code.strip() or code.strip().startswith('$') or code.strip().startswith('>'):
        result['valid'] = True
        result['is_snippet'] = True
        return result
    
    # 检测是否为代码片段
    has_class = bool(re.search(r'\bclass\s+\w+', code))
    has_interface = bool(re.search(r'\binterface\s+\w+', code))
    has_enum = bool(re.search(r'\benum\s+\w+', code))
    result['is_snippet'] = not (has_class or has_interface or has_enum)
    
    # 检测缺少的import
    result['missing_imports'] = detect_missing_imports(code)
    
    # 检测弃用API
    result['deprecated_apis'] = detect_deprecated_apis(code)
    
    # 检测语法问题
    result['syntax_issues'] = detect_syntax_issues(code)
    
    # 综合评估
    if result['syntax_issues']:
        result['valid'] = False
        result['issues'].append('语法问题: ' + '; '.join(result['syntax_issues']))
    
    if result['missing_imports']:
        result['issues'].append(f'缺少import: {len(result["missing_imports"])}个类')
    
    if result['deprecated_apis']:
        result['issues'].append(f'使用弃用API: {len(result["deprecated_apis"])}处')
    
    return result


def main():
    print("=" * 60)
    print("Java代码验证器 - 静态分析版本 (Q1-2)")
    print("=" * 60)
    
    # 收集所有Java代码块
    print("\n📄 扫描Markdown文件...")
    all_blocks = []
    
    for md_file in Path('.').rglob("*.md"):
        ps = str(md_file)
        if any(x in ps for x in ['.git', 'node_modules', '__pycache__', 'venv', '.venv', 'archive', 'release']):
            continue
        try:
            content = md_file.read_text(encoding='utf-8')
            if '```java' not in content:
                continue
            
            ms = list(re.finditer(r'```(\w+)?\n(.*?)```', content, re.DOTALL))
            
            lbs = [0]
            for idx, char in enumerate(content):
                if char == '\n':
                    lbs.append(idx + 1)
            
            for idx, m in enumerate(ms):
                lang = (m.group(1) or "text").lower().strip()
                if lang != "java":
                    continue
                code = m.group(2)
                sp = m.start()
                ln = sum(1 for p in lbs if p <= sp)
                all_blocks.append({'file': ps, 'line': ln, 'code': code})
        except:
            pass
    
    print(f"   找到 {len(all_blocks)} 个Java代码块")
    
    # 分析所有代码块
    print(f"\n🔧 分析Java代码块...")
    results = []
    
    for i, b in enumerate(all_blocks):
        if (i + 1) % 200 == 0:
            print(f"   进度: {i + 1}/{len(all_blocks)}")
        
        r = analyze_code(b['code'], b['file'], b['line'])
        results.append(r)
    
    print(f"\n✅ 分析完成!")
    
    # 统计
    valid = sum(1 for r in results if r['valid'] and not r['issues'])
    has_issues = sum(1 for r in results if r['issues'])
    snippets = sum(1 for r in results if r['is_snippet'])
    
    missing_import_count = sum(len(r['missing_imports']) for r in results)
    deprecated_count = sum(len(r['deprecated_apis']) for r in results)
    syntax_issue_count = sum(len(r['syntax_issues']) for r in results)
    
    print(f"\n📊 统计结果:")
    print(f"   - 总代码块数: {len(results)}")
    print(f"   - 无问题代码: {valid}")
    print(f"   - 有问题代码: {has_issues}")
    print(f"   - 代码片段: {snippets}")
    print(f"   - 缺少import: {missing_import_count}处")
    print(f"   - 弃用API: {deprecated_count}处")
    print(f"   - 语法问题: {syntax_issue_count}处")
    
    # 按问题类型分组
    files_with_missing_imports = [r for r in results if r['missing_imports']]
    files_with_deprecated = [r for r in results if r['deprecated_apis']]
    files_with_syntax = [r for r in results if r['syntax_issues']]
    
    print(f"\n📁 问题分布:")
    print(f"   - 缺少import的文件: {len(files_with_missing_imports)}")
    print(f"   - 使用弃用API的文件: {len(files_with_deprecated)}")
    print(f"   - 有语法问题的文件: {len(files_with_syntax)}")
    
    # 生成报告
    report = {
        'timestamp': datetime.now().isoformat(),
        'stats': {
            'total_blocks': len(results),
            'valid': valid,
            'has_issues': has_issues,
            'snippets': snippets,
            'missing_import_count': missing_import_count,
            'deprecated_count': deprecated_count,
            'syntax_issue_count': syntax_issue_count,
            'files_with_missing_imports': len(files_with_missing_imports),
            'files_with_deprecated': len(files_with_deprecated),
            'files_with_syntax': len(files_with_syntax),
        },
        'results': results
    }
    
    # 保存JSON
    with open('java-code-validation-result.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n📝 JSON报告: java-code-validation-result.json")
    
    # 生成Markdown报告
    md = []
    md.append("# Java代码示例验证报告 (Q1-2)")
    md.append("")
    md.append(f"> **生成时间**: {report['timestamp']}")
    md.append(f"> **任务**: Q1-2 Java代码示例验证")
    md.append(f"> **方法**: 静态分析 (正则表达式匹配)")
    md.append("")
    
    md.append("## 📊 验证统计")
    md.append("")
    md.append("| 指标 | 数值 |")
    md.append("|------|------|")
    md.append(f"| Java代码块总数 | {len(results)} |")
    md.append(f"| ✅ 无问题代码 | {valid} |")
    md.append(f"| ⚠️ 有问题代码 | {has_issues} |")
    md.append(f"| 📝 代码片段 | {snippets} |")
    md.append(f"| 🔗 缺少import | {missing_import_count} 处 |")
    md.append(f"| 📦 弃用API | {deprecated_count} 处 |")
    md.append(f"| 🔧 语法问题 | {syntax_issue_count} 处 |")
    md.append("")
    
    # 缺少import的文件
    if files_with_missing_imports:
        md.append("## 🔗 缺少Import的文件")
        md.append("")
        md.append(f"共 **{len(files_with_missing_imports)}** 个文件缺少import语句：")
        md.append("")
        for r in files_with_missing_imports[:100]:
            imports = ', '.join([c for c, _ in r['missing_imports'][:5]])
            if len(r['missing_imports']) > 5:
                imports += f" 等{len(r['missing_imports'])}个"
            md.append(f"- `{r['file']}` 第{r['line']}行: {imports}")
        if len(files_with_missing_imports) > 100:
            md.append(f"- ... 还有 {len(files_with_missing_imports) - 100} 个文件")
        md.append("")
    
    # 使用弃用API的文件
    if files_with_deprecated:
        md.append("## 📦 使用弃用API的文件")
        md.append("")
        md.append(f"共 **{len(files_with_deprecated)}** 个文件使用弃用API：")
        md.append("")
        for r in files_with_deprecated[:50]:
            apis = ', '.join([msg for _, msg in r['deprecated_apis']])
            md.append(f"- `{r['file']}` 第{r['line']}行: {apis}")
        if len(files_with_deprecated) > 50:
            md.append(f"- ... 还有 {len(files_with_deprecated) - 50} 个文件")
        md.append("")
    
    # 语法问题的文件
    if files_with_syntax:
        md.append("## 🔧 语法问题的文件")
        md.append("")
        md.append(f"共 **{len(files_with_syntax)}** 个文件有语法问题：")
        md.append("")
        for r in files_with_syntax[:50]:
            issues = '; '.join(r['syntax_issues'])
            md.append(f"- `{r['file']}` 第{r['line']}行: {issues}")
        if len(files_with_syntax) > 50:
            md.append(f"- ... 还有 {len(files_with_syntax) - 50} 个文件")
        md.append("")
    
    # 示例：修复建议
    if files_with_missing_imports:
        md.append("## 💡 修复示例")
        md.append("")
        md.append("### 添加Import示例")
        md.append("")
        r = files_with_missing_imports[0]
        md.append(f"**文件**: `{r['file']}` 第{r['line']}行")
        md.append("")
        md.append("**当前代码**:")
        md.append("```java")
        md.append(r['preview'][:300])
        md.append("```")
        md.append("")
        md.append("**建议添加的import**:")
        md.append("```java")
        for cn, ip in r['missing_imports'][:10]:
            md.append(f"import {ip}; // 用于 {cn}")
        md.append("```")
        md.append("")
    
    # 改进建议
    md.append("## 📋 改进建议")
    md.append("")
    md.append("### 1. 添加缺失的Import语句")
    md.append(f"- 共有 {len(files_with_missing_imports)} 个代码块缺少必要的import语句")
    md.append("- 常见需要添加的import包括Flink核心类、状态管理类、时间语义类等")
    md.append("")
    md.append("### 2. 更新弃用API")
    md.append(f"- 共有 {len(files_with_deprecated)} 个代码块使用弃用API")
    md.append("- 主要弃用API：")
    md.append("  - `setStreamTimeCharacteristic()` → 使用WatermarkStrategy")
    md.append("  - `fold()` → 使用AggregateFunction")
    md.append("")
    md.append("### 3. 修复语法问题")
    md.append(f"- 共有 {len(files_with_syntax)} 个代码块存在语法问题")
    md.append("- 常见问题：大括号不匹配、括号不匹配等")
    md.append("")
    md.append("### 4. 代码片段上下文")
    md.append(f"- 共有 {snippets} 个代码片段需要添加上下文注释")
    md.append("- 建议为片段代码添加必要的说明和完整示例链接")
    md.append("")
    
    with open('CODE-VALIDATION-JAVA-REPORT.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    
    print(f"📝 Markdown报告: CODE-VALIDATION-JAVA-REPORT.md")
    print("\n" + "=" * 60)
    print("完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
