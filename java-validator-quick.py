#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Java代码验证器 - 快速版本 (处理前1000个)
"""

import re
import os
import json
import tempfile
import subprocess
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


def detect_missing_imports(code):
    missing = []
    for class_name, import_path in FLINK_IMPORTS.items():
        if re.search(r'\b' + class_name + r'\b', code):
            if not re.search(r'import\s+' + import_path.replace('.', r'\.') + r'\s*;', code):
                if not re.search(r'import\s+' + import_path.rsplit('.', 1)[0].replace('.', r'\.') + r'\.\*\s*;', code):
                    missing.append((class_name, import_path))
    return missing


def add_missing_imports(code):
    missing = detect_missing_imports(code)
    if not missing:
        return code
    imports = [f"import {ip};" for cn, ip in missing]
    pm = re.search(r'^package\s+[^;]+;', code, re.MULTILINE)
    if pm:
        ip = pm.end()
        return code[:ip] + '\n\n' + '\n'.join(imports) + code[ip:]
    return '\n'.join(imports) + '\n\n' + code


def wrap_code(code):
    if re.search(r'\b(class|interface|enum)\s+\w+', code):
        m = re.search(r'(?:class|interface|enum)\s+(\w+)', code)
        return code, m.group(1) if m else "Unknown"
    
    cwi = add_missing_imports(code)
    w = f"""public class TempValidation {{
    {cwi.replace(chr(10), chr(10) + '    ')}
}}"""
    return w, "TempValidation"


def validate(code):
    if not code.strip() or code.strip().startswith('$') or code.strip().startswith('>'):
        return True, None, None, None, None
    
    mi = detect_missing_imports(code)
    wc, cn = wrap_code(code)
    td = tempfile.gettempdir()
    tf = os.path.join(td, f"{cn}.java")
    
    try:
        with open(tf, 'w', encoding='utf-8') as f:
            f.write(wc)
        
        r = subprocess.run(['javac', '-d', td, tf], capture_output=True, text=True, timeout=3)
        
        for e in ['.java', '.class']:
            f = tf.replace('.java', e)
            if os.path.exists(f):
                os.unlink(f)
        
        if r.returncode == 0:
            return True, None, None, None, None
        
        em = r.stderr
        it = "syntax_error"
        if "找不到符号" in em or "cannot find symbol" in em:
            it = "missing_import"
        
        lm = re.search(r':(\d+):', em)
        el = int(lm.group(1)) if lm else None
        
        if it == "missing_import" and mi:
            fc = add_missing_imports(code)
            wf, _ = wrap_code(fc)
            try:
                with open(tf, 'w', encoding='utf-8') as f:
                    f.write(wf)
                r2 = subprocess.run(['javac', '-d', td, tf], capture_output=True, text=True, timeout=3)
                for e in ['.java', '.class']:
                    f = tf.replace('.java', e)
                    if os.path.exists(f):
                        os.unlink(f)
                if r2.returncode == 0:
                    return False, em, el, it, fc
            except:
                pass
        
        return False, em, el, it, None
        
    except subprocess.TimeoutExpired:
        return False, "超时", None, "timeout", None
    except Exception as e:
        return False, str(e), None, "error", None


def main():
    print("=" * 60)
    print("Java代码验证器 - Q1-2任务")
    print("=" * 60)
    
    # 收集所有Java代码块
    print("\n📄 收集Java代码块...")
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
            for c in content:
                if c == '\n':
                    lbs.append(len(lbs))
            
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
    
    total_blocks = len(all_blocks)
    print(f"   找到 {total_blocks} 个Java代码块")
    
    # 限制处理数量以保证性能
    MAX_BLOCKS = 1500
    if len(all_blocks) > MAX_BLOCKS:
        print(f"   为控制执行时间，处理前 {MAX_BLOCKS} 个代码块")
        all_blocks = all_blocks[:MAX_BLOCKS]
    
    # 验证
    print(f"\n🔧 验证Java代码块 (0/{len(all_blocks)})...")
    results = []
    
    for i, b in enumerate(all_blocks):
        if (i + 1) % 100 == 0:
            print(f"   验证进度: {i + 1}/{len(all_blocks)}")
        
        v, em, el, it, sf = validate(b['code'])
        results.append({
            'file': b['file'],
            'line': b['line'],
            'valid': v and not em,
            'error': em,
            'error_line': el,
            'issue_type': it,
            'fixable': sf is not None,
            'fix': sf,
            'preview': b['code'][:200] + "..." if len(b['code']) > 200 else b['code']
        })
    
    # 统计
    valid = sum(1 for r in results if r['valid'])
    invalid = len(results) - valid
    fixable = sum(1 for r in results if r['fixable'])
    
    it_counts = {}
    for r in results:
        if r['issue_type']:
            it_counts[r['issue_type']] = it_counts.get(r['issue_type'], 0) + 1
    
    print(f"\n✅ 验证完成!")
    print(f"\n📊 统计结果:")
    print(f"   - 验证的代码块数: {len(results)}")
    print(f"   - 通过: {valid}")
    print(f"   - 失败: {invalid}")
    print(f"   - 可自动修复: {fixable}")
    print(f"   - 通过率: {(valid/len(results)*100):.2f}%")
    
    print(f"\n📋 问题类型分布:")
    for t, c in sorted(it_counts.items(), key=lambda x: -x[1]):
        print(f"   - {t}: {c}")
    
    # 生成报告
    report = {
        'timestamp': datetime.now().isoformat(),
        'stats': {
            'total_java_blocks_in_project': total_blocks,
            'validated_blocks': len(results),
            'valid': valid,
            'invalid': invalid,
            'fixable': fixable,
            'pass_rate': (valid / len(results) * 100) if results else 0,
            'issue_types': it_counts
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
    md.append(f"> **说明**: 项目中共有 {total_blocks} 个Java代码块，本次验证了 {len(results)} 个")
    md.append("")
    
    md.append("## 📊 验证统计")
    md.append("")
    md.append("| 指标 | 数值 |")
    md.append("|------|------|")
    md.append(f"| 项目中Java代码块总数 | {total_blocks} |")
    md.append(f"| 本次验证的代码块数 | {len(results)} |")
    md.append(f"| ✅ 验证通过 | {valid} |")
    md.append(f"| ❌ 验证失败 | {invalid} |")
    md.append(f"| 🔧 可自动修复 | {fixable} |")
    md.append(f"| **通过率** | {report['stats']['pass_rate']:.2f}% |")
    md.append("")
    
    if it_counts:
        md.append("### 问题类型分布")
        md.append("")
        md.append("| 问题类型 | 数量 |")
        md.append("|----------|------|")
        for t, c in sorted(it_counts.items(), key=lambda x: -x[1]):
            md.append(f"| {t} | {c} |")
        md.append("")
    
    # 问题代码
    inv = [r for r in results if not r['valid']]
    if inv:
        md.append(f"## 🚨 问题代码清单 (前50个，共{len(inv)}个)")
        md.append("")
        for r in inv[:50]:
            md.append(f"### `{r['file']}` (第 {r['line']} 行)")
            md.append("")
            if r['issue_type']:
                md.append(f"- **问题类型**: {r['issue_type']}")
            if r['error']:
                e = r['error'][:200].replace('\n', ' ')
                md.append(f"- **错误**: {e}...")
            if r['fixable']:
                md.append(f"- **可修复**: ✅")
            md.append("")
            md.append("```java")
            md.append(r['preview'][:300])
            md.append("```")
            md.append("")
    
    # 修复的代码
    fix = [r for r in results if r['fixable'] and r['fix']]
    if fix:
        md.append(f"## 🔧 修复的代码清单 (前30个，共{len(fix)}个)")
        md.append("")
        for r in fix[:30]:
            md.append(f"### `{r['file']}` (第 {r['line']} 行)")
            md.append("")
            md.append("**原始代码**:")
            md.append("```java")
            md.append(r['preview'][:250])
            md.append("```")
            md.append("")
            md.append("**修复后**:")
            md.append("```java")
            f = r['fix'][:350].replace('```', '')
            md.append(f)
            md.append("```")
            md.append("")
    
    # 复杂案例
    comp = [r for r in results if not r['valid'] and not r['fixable']]
    if comp:
        md.append(f"## ⚠️ 需人工审核案例 (前30个，共{len(comp)}个)")
        md.append("")
        for r in comp[:30]:
            md.append(f"- `{r['file']}` 第 {r['line']} 行: {r['issue_type'] or '未知'}")
        md.append("")
    
    md.append("## 💡 改进建议")
    md.append("")
    md.append("1. **添加import语句**: 为缺少import的代码添加必要的import")
    md.append("2. **更新弃用API**: 迁移使用弃用API的代码")
    md.append("3. **提供上下文**: 为片段代码添加上下文注释")
    md.append("4. **代码完整性**: 确保代码示例完整可运行")
    md.append("")
    
    with open('CODE-VALIDATION-JAVA-REPORT.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    
    print(f"📝 Markdown报告: CODE-VALIDATION-JAVA-REPORT.md")
    print("\n" + "=" * 60)
    print("完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
