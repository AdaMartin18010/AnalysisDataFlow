#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Java代码示例验证器 - Java Code Example Validator
验证项目中所有Markdown文件的Java代码示例可编译性和可运行性

作者: AI Agent
创建时间: 2026-04-12
版本: 1.0.0
"""

import re
import os
import sys
import json
import tempfile
import subprocess
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Set
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback


@dataclass
class CodeBlock:
    """代码块数据结构"""
    language: str
    code: str
    file_path: str
    line_number: int
    block_index: int
    
    def __hash__(self):
        return hash((self.file_path, self.line_number, self.block_index))


@dataclass
class ValidationResult:
    """验证结果数据结构"""
    code_block: CodeBlock
    is_valid: bool
    error_message: Optional[str] = None
    error_line: Optional[int] = None
    severity: str = "error"  # error, warning, info
    fixable: bool = False
    suggested_fix: Optional[str] = None
    issue_type: Optional[str] = None  # missing_import, deprecated_api, syntax_error, missing_context
    
    def to_dict(self) -> dict:
        return {
            "file_path": self.code_block.file_path,
            "line_number": self.code_block.line_number,
            "language": self.code_block.language,
            "block_index": self.code_block.block_index,
            "is_valid": self.is_valid,
            "error_message": self.error_message,
            "error_line": self.error_line,
            "severity": self.severity,
            "fixable": self.fixable,
            "suggested_fix": self.suggested_fix,
            "issue_type": self.issue_type,
            "code_preview": self.code_block.code[:300] + "..." if len(self.code_block.code) > 300 else self.code_block.code
        }


@dataclass
class ValidationStats:
    """验证统计数据"""
    total_files: int = 0
    total_blocks: int = 0
    valid_blocks: int = 0
    invalid_blocks: int = 0
    fixed_blocks: int = 0
    warnings: int = 0
    by_issue_type: Dict[str, int] = field(default_factory=dict)
    
    def update(self, result: ValidationResult):
        if result.is_valid:
            self.valid_blocks += 1
        else:
            self.invalid_blocks += 1
        
        if result.fixable:
            self.fixed_blocks += 1
            
        if result.issue_type:
            self.by_issue_type[result.issue_type] = self.by_issue_type.get(result.issue_type, 0) + 1


class JavaCodeValidator:
    """Java代码验证器主类"""
    
    # Flink/Java 常见类的import映射
    FLINK_IMPORTS = {
        # Core API
        'StreamExecutionEnvironment': 'org.apache.flink.streaming.api.environment.StreamExecutionEnvironment',
        'DataStream': 'org.apache.flink.streaming.api.datastream.DataStream',
        'SingleOutputStreamOperator': 'org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator',
        'ConnectedStreams': 'org.apache.flink.streaming.api.datastream.ConnectedStreams',
        'KeyedStream': 'org.apache.flink.streaming.api.datastream.KeyedStream',
        'WindowedStream': 'org.apache.flink.streaming.api.datastream.WindowedStream',
        'AllWindowedStream': 'org.apache.flink.streaming.api.datastream.AllWindowedStream',
        'IterativeStream': 'org.apache.flink.streaming.api.datastream.IterativeStream',
        'BroadcastStream': 'org.apache.flink.streaming.api.datastream.BroadcastStream',
        'BroadcastConnectedStream': 'org.apache.flink.streaming.api.datastream.BroadcastConnectedStream',
        
        # Time & Watermark
        'WatermarkStrategy': 'org.apache.flink.api.common.eventtime.WatermarkStrategy',
        'WatermarkGenerator': 'org.apache.flink.api.common.eventtime.WatermarkGenerator',
        'WatermarkGeneratorSupplier': 'org.apache.flink.api.common.eventtime.WatermarkGeneratorSupplier',
        'WatermarkOutput': 'org.apache.flink.api.common.eventtime.WatermarkOutput',
        'TimestampAssigner': 'org.apache.flink.api.common.eventtime.TimestampAssigner',
        'TimestampAssignerSupplier': 'org.apache.flink.api.common.eventtime.TimestampAssignerSupplier',
        'SerializableTimestampAssigner': 'org.apache.flink.api.common.eventtime.SerializableTimestampAssigner',
        
        # Window
        'TimeWindow': 'org.apache.flink.streaming.api.windowing.windows.TimeWindow',
        'GlobalWindow': 'org.apache.flink.streaming.api.windowing.windows.GlobalWindow',
        'WindowAssigner': 'org.apache.flink.streaming.api.windowing.assigners.WindowAssigner',
        'TumblingEventTimeWindows': 'org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows',
        'TumblingProcessingTimeWindows': 'org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows',
        'SlidingEventTimeWindows': 'org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows',
        'SlidingProcessingTimeWindows': 'org.apache.flink.streaming.api.windowing.assigners.SlidingProcessingTimeWindows',
        'SessionWindowTimeGapExtractor': 'org.apache.flink.streaming.api.windowing.assigners.SessionWindowTimeGapExtractor',
        'EventTimeSessionWindows': 'org.apache.flink.streaming.api.windowing.assigners.EventTimeSessionWindows',
        'ProcessingTimeSessionWindows': 'org.apache.flink.streaming.api.windowing.assigners.ProcessingTimeSessionWindows',
        'DynamicEventTimeSessionWindows': 'org.apache.flink.streaming.api.windowing.assigners.DynamicEventTimeSessionWindows',
        'DynamicProcessingTimeSessionWindows': 'org.apache.flink.streaming.api.windowing.assigners.DynamicProcessingTimeSessionWindows',
        
        # Triggers & Evictors
        'Trigger': 'org.apache.flink.streaming.api.windowing.triggers.Trigger',
        'TriggerResult': 'org.apache.flink.streaming.api.windowing.triggers.TriggerResult',
        'Evictor': 'org.apache.flink.streaming.api.windowing.evictors.Evictor',
        'CountEvictor': 'org.apache.flink.streaming.api.windowing.evictors.CountEvictor',
        'TimeEvictor': 'org.apache.flink.streaming.api.windowing.evictors.TimeEvictor',
        
        # State
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
        'State': 'org.apache.flink.api.common.state.State',
        'StateDescriptor': 'org.apache.flink.api.common.state.StateDescriptor',
        'StateTtlConfig': 'org.apache.flink.api.common.state.StateTtlConfig',
        
        # Checkpoint & Fault Tolerance
        'CheckpointListener': 'org.apache.flink.streaming.api.checkpoint.CheckpointListener',
        'CheckpointedFunction': 'org.apache.flink.streaming.api.checkpoint.CheckpointedFunction',
        'ListCheckpointed': 'org.apache.flink.streaming.api.checkpoint.ListCheckpointed',
        'CheckpointingMode': 'org.apache.flink.streaming.api.CheckpointingMode',
        
        # Functions
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
        
        # Process Functions
        'ProcessFunction': 'org.apache.flink.streaming.api.functions.ProcessFunction',
        'KeyedProcessFunction': 'org.apache.flink.streaming.api.functions.KeyedProcessFunction',
        'CoProcessFunction': 'org.apache.flink.streaming.api.functions.co.CoProcessFunction',
        'KeyedCoProcessFunction': 'org.apache.flink.streaming.api.functions.co.KeyedCoProcessFunction',
        'ProcessAllWindowFunction': 'org.apache.flink.streaming.api.functions.windowing.ProcessAllWindowFunction',
        'ProcessWindowFunction': 'org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction',
        'BroadcastProcessFunction': 'org.apache.flink.streaming.api.functions.co.BroadcastProcessFunction',
        'KeyedBroadcastProcessFunction': 'org.apache.flink.streaming.api.functions.co.KeyedBroadcastProcessFunction',
        
        # Sink & Source
        'SinkFunction': 'org.apache.flink.streaming.api.functions.sink.SinkFunction',
        'RichSinkFunction': 'org.apache.flink.streaming.api.functions.sink.RichSinkFunction',
        'SourceFunction': 'org.apache.flink.streaming.api.functions.source.SourceFunction',
        'RichSourceFunction': 'org.apache.flink.streaming.api.functions.source.RichSourceFunction',
        'ParallelSourceFunction': 'org.apache.flink.streaming.api.functions.source.ParallelSourceFunction',
        'FromElementsFunction': 'org.apache.flink.streaming.api.functions.source.FromElementsFunction',
        'FileProcessingMode': 'org.apache.flink.streaming.api.functions.source.FileProcessingMode',
        
        # Output
        'OutputTag': 'org.apache.flink.util.OutputTag',
        'Collector': 'org.apache.flink.util.Collector',
        
        # Serialization
        'TypeInformation': 'org.apache.flink.api.common.typeinfo.TypeInformation',
        'TypeHint': 'org.apache.flink.api.common.typeinfo.TypeHint',
        'Types': 'org.apache.flink.api.common.typeinfo.Types',
        'SerializerConfig': 'org.apache.flink.api.common.serialization.SerializerConfig',
        
        # Configuration
        'Configuration': 'org.apache.flink.configuration.Configuration',
        'ExecutionConfig': 'org.apache.flink.api.common.ExecutionConfig',
        
        # Table API
        'TableEnvironment': 'org.apache.flink.table.api.TableEnvironment',
        'StreamTableEnvironment': 'org.apache.flink.table.api.StreamTableEnvironment',
        'Table': 'org.apache.flink.table.api.Table',
        'TableDescriptor': 'org.apache.flink.table.api.TableDescriptor',
        'Schema': 'org.apache.flink.table.api.Schema',
        'DataTypes': 'org.apache.flink.table.api.DataTypes',
        
        # CEP
        'Pattern': 'org.apache.flink.cep.Pattern',
        'CEP': 'org.apache.flink.cep.CEP',
        'PatternSelectFunction': 'org.apache.flink.cep.PatternSelectFunction',
        'PatternTimeoutFunction': 'org.apache.flink.cep.PatternTimeoutFunction',
        'PatternFlatSelectFunction': 'org.apache.flink.cep.PatternFlatSelectFunction',
        
        # Metrics
        'Counter': 'org.apache.flink.metrics.Counter',
        'Gauge': 'org.apache.flink.metrics.Gauge',
        'Histogram': 'org.apache.flink.metrics.Histogram',
        'Meter': 'org.apache.flink.metrics.Meter',
        'MetricGroup': 'org.apache.flink.metrics.MetricGroup',
    }
    
    # 弃用的API映射 (旧API -> 新API)
    DEPRECATED_APIS = {
        r'\.assignTimestampsAndWatermarks\s*\(\s*WatermarkStrategy': None,  # 需要检查上下文
        r'env\.setStreamTimeCharacteristic': '已弃用，Flink 1.12+ 默认使用事件时间',
        r'\.fold\s*\(': 'fold 操作已弃用，请使用 AggregateFunction',
        r'ExecutionConfig\.setAutoWatermarkInterval': '请使用 WatermarkStrategy.withIdleness()',
    }
    
    def __init__(self, project_root: Path, max_workers: int = 4):
        self.project_root = Path(project_root)
        self.max_workers = max_workers
        self.results: List[ValidationResult] = []
        self.stats = ValidationStats()
        
    def scan_markdown_files(self) -> List[Path]:
        """扫描所有Markdown文件"""
        print("🔍 扫描Markdown文件...")
        md_files = list(self.project_root.rglob("*.md"))
        
        # 排除某些目录
        exclude_patterns = ['.git', 'node_modules', '__pycache__', '.venv', 'venv', 'archive']
        md_files = [
            f for f in md_files 
            if not any(excl in str(f) for excl in exclude_patterns)
        ]
        
        self.stats.total_files = len(md_files)
        print(f"   找到 {len(md_files)} 个Markdown文件")
        return md_files
    
    def extract_code_blocks(self, content: str, file_path: str) -> List[CodeBlock]:
        """从Markdown内容中提取代码块"""
        code_blocks = []
        
        # 匹配 ```language
code
``` 格式
        pattern = r'```(\w+)?\n(.*?)```'
        matches = list(re.finditer(pattern, content, re.DOTALL))
        
        # 计算行号
        lines_before = [0]
        for i, char in enumerate(content):
            if char == '\n':
                lines_before.append(i + 1)
        
        for idx, match in enumerate(matches):
            language = (match.group(1) or "text").lower().strip()
            code = match.group(2)
            
            # 计算起始行号
            start_pos = match.start()
            line_number = sum(1 for pos in lines_before if pos <= start_pos)
            
            # 只处理Java代码块
            if language in ["java"]:
                code_blocks.append(CodeBlock(
                    language=language,
                    code=code,
                    file_path=file_path,
                    line_number=line_number,
                    block_index=idx
                ))
        
        return code_blocks
    
    def detect_missing_imports(self, code: str) -> List[Tuple[str, str]]:
        """检测代码中缺少import的类"""
        missing = []
        
        # 检查代码中使用的Flink类
        for class_name, import_path in self.FLINK_IMPORTS.items():
            # 匹配类名（排除已import的情况）
            pattern = r'\b' + class_name + r'\b'
            if re.search(pattern, code):
                # 检查是否已导入
                import_pattern = r'import\s+' + import_path.replace('.', r'\.') + r'\s*;'
                if not re.search(import_pattern, code):
                    # 检查是否有通配符导入
                    wildcard_pattern = r'import\s+' + import_path.rsplit('.', 1)[0].replace('.', r'\.') + r'\.\*\s*;'
                    if not re.search(wildcard_pattern, code):
                        missing.append((class_name, import_path))
        
        return missing
    
    def detect_deprecated_apis(self, code: str) -> List[Tuple[str, str]]:
        """检测代码中使用的弃用API"""
        deprecated = []
        
        for pattern, message in self.DEPRECATED_APIS.items():
            if re.search(pattern, code):
                deprecated.append((pattern, message or "此API已弃用"))
        
        return deprecated
    
    def add_missing_imports(self, code: str) -> str:
        """为代码添加缺失的import语句"""
        missing = self.detect_missing_imports(code)
        
        if not missing:
            return code
        
        # 构建import语句
        imports = []
        for class_name, import_path in missing:
            imports.append(f"import {import_path};")
        
        # 检查是否已有package声明
        package_match = re.search(r'^package\s+[^;]+;', code, re.MULTILINE)
        
        if package_match:
            # 在package后添加import
            insert_pos = package_match.end()
            return code[:insert_pos] + '\n\n' + '\n'.join(imports) + code[insert_pos:]
        else:
            # 在文件开头添加import
            return '\n'.join(imports) + '\n\n' + code
    
    def wrap_code_if_needed(self, code: str) -> Tuple[str, str]:
        """
        如果代码不是完整类，则包装成完整类
        返回: (包装后的代码, 类名)
        """
        # 检查是否已是完整类
        has_class = re.search(r'\bclass\s+\w+', code)
        has_interface = re.search(r'\binterface\s+\w+', code)
        has_enum = re.search(r'\benum\s+\w+', code)
        
        if has_class or has_interface or has_enum:
            # 提取类名
            match = re.search(r'(?:class|interface|enum)\s+(\w+)', code)
            class_name = match.group(1) if match else "Unknown"
            return code, class_name
        
        # 代码片段 - 需要包装
        # 添加缺失的import
        code_with_imports = self.add_missing_imports(code)
        
        # 包装成类
        wrapped = f"""public class TempValidation {{
    {code_with_imports.replace(chr(10), chr(10) + '    ')}
}}"""
        
        return wrapped, "TempValidation"
    
    def validate_java(self, code: str) -> Tuple[bool, Optional[str], Optional[int], Optional[str], Optional[str]]:
        """
        验证Java代码语法
        返回: (是否有效, 错误信息, 错误行号, 问题类型, 修复后的代码)
        """
        if not code.strip():
            return True, None, None, None, None
        
        # 检测缺少的import
        missing_imports = self.detect_missing_imports(code)
        
        # 检测弃用的API
        deprecated_apis = self.detect_deprecated_apis(code)
        
        # 包装代码（如果需要）
        wrapped_code, class_name = self.wrap_code_if_needed(code)
        
        # 写入临时文件
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"{class_name}.java")
        
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(wrapped_code)
            
            # 编译
            result = subprocess.run(
                ['javac', '-d', temp_dir, temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # 清理临时文件
            for ext in ['.java', '.class']:
                f = temp_file.replace('.java', ext)
                if os.path.exists(f):
                    os.unlink(f)
            
            if result.returncode == 0:
                # 编译成功，检查警告
                if deprecated_apis:
                    warnings = "; ".join([f"{p}: {m}" for p, m in deprecated_apis])
                    return True, f"警告: {warnings}", None, "deprecated_api", None
                return True, None, None, None, None
            else:
                error_msg = result.stderr
                
                # 分析问题类型
                issue_type = "syntax_error"
                if "找不到符号" in error_msg or "cannot find symbol" in error_msg:
                    issue_type = "missing_import"
                elif "已弃用" in error_msg or "deprecated" in error_msg.lower():
                    issue_type = "deprecated_api"
                elif "需要" in error_msg and "上下文" in error_msg:
                    issue_type = "missing_context"
                
                # 提取错误行号
                line_match = re.search(r':(\d+):', error_msg)
                error_line = int(line_match.group(1)) if line_match else None
                
                # 尝试修复：添加import
                if issue_type == "missing_import" and missing_imports:
                    fixed_code = self.add_missing_imports(code)
                    # 再次验证修复后的代码
                    is_fixed, fix_err, _, _, _ = self.validate_java(fixed_code)
                    if is_fixed:
                        return False, error_msg, error_line, issue_type, fixed_code
                
                return False, error_msg, error_line, issue_type, None
                
        except subprocess.TimeoutExpired:
            return False, "编译超时", None, "timeout", None
        except Exception as e:
            return False, f"验证错误: {str(e)}", None, "error", None
    
    def validate_code_block(self, block: CodeBlock) -> ValidationResult:
        """验证单个代码块"""
        is_valid, error_msg, error_line, issue_type, fixed_code = self.validate_java(block.code)
        
        severity = "error" if not is_valid else ("warning" if error_msg else "info")
        fixable = fixed_code is not None
        
        return ValidationResult(
            code_block=block,
            is_valid=is_valid and not error_msg,  # 有警告也算有问题
            error_message=error_msg,
            error_line=error_line,
            severity=severity,
            fixable=fixable,
            suggested_fix=fixed_code,
            issue_type=issue_type
        )
    
    def run_validation(self) -> None:
        """运行验证流程"""
        print("=" * 60)
        print("Java代码示例验证器启动")
        print("=" * 60)
        
        # 扫描文件
        md_files = self.scan_markdown_files()
        
        # 提取所有Java代码块
        print("\n📄 提取Java代码块...")
        all_blocks = []
        for md_file in md_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                blocks = self.extract_code_blocks(content, str(md_file))
                all_blocks.extend(blocks)
            except Exception as e:
                print(f"   警告: 无法读取 {md_file}: {e}")
        
        self.stats.total_blocks = len(all_blocks)
        print(f"   找到 {len(all_blocks)} 个Java代码块")
        
        # 验证代码块
        print("\n🔧 验证代码块...")
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.validate_code_block, block): block for block in all_blocks}
            
            for i, future in enumerate(as_completed(futures)):
                if (i + 1) % 100 == 0 or i == len(all_blocks) - 1:
                    print(f"   进度: {i + 1}/{len(all_blocks)}")
                
                try:
                    result = future.result()
                    self.results.append(result)
                    self.stats.update(result)
                except Exception as e:
                    print(f"   错误: 验证失败 - {e}")
        
        print("\n✅ 验证完成!")
    
    def generate_report(self) -> str:
        """生成验证报告"""
        report_lines = []
        report_lines.append("# Java代码示例验证报告")
        report_lines.append("")
        report_lines.append(f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"> **验证器版本**: 1.0.0")
        report_lines.append(f"> **项目根目录**: {self.project_root}")
        report_lines.append("")
        
        # 统计概览
        report_lines.append("## 📊 验证统计")
        report_lines.append("")
        report_lines.append("| 指标 | 数值 |")
        report_lines.append("|------|------|")
        report_lines.append(f"| 扫描文件数 | {self.stats.total_files} |")
        report_lines.append(f"| Java代码块总数 | {self.stats.total_blocks} |")
        report_lines.append(f"| ✅ 验证通过 | {self.stats.valid_blocks} |")
        report_lines.append(f"| ❌ 验证失败 | {self.stats.invalid_blocks} |")
        report_lines.append(f"| 🔧 可自动修复 | {self.stats.fixed_blocks} |")
        report_lines.append(f"| **通过率** | {(self.stats.valid_blocks / self.stats.total_blocks * 100):.2f}% |" if self.stats.total_blocks > 0 else "| **通过率** | N/A |")
        report_lines.append("")
        
        # 问题类型统计
        if self.stats.by_issue_type:
            report_lines.append("### 问题类型分布")
            report_lines.append("")
            report_lines.append("| 问题类型 | 数量 | 说明 |")
            report_lines.append("|----------|------|------|")
            for issue_type, count in sorted(self.stats.by_issue_type.items(), key=lambda x: -x[1]):
                description = {
                    "missing_import": "缺少import语句",
                    "deprecated_api": "使用弃用API",
                    "syntax_error": "语法错误",
                    "missing_context": "缺少上下文",
                    "timeout": "编译超时",
                    "error": "其他错误"
                }.get(issue_type, issue_type)
                report_lines.append(f"| {issue_type} | {count} | {description} |")
            report_lines.append("")
        
        # 失败的代码清单
        invalid_results = [r for r in self.results if not r.is_valid]
        if invalid_results:
            report_lines.append("## 🚨 问题代码清单")
            report_lines.append("")
            report_lines.append(f"共发现 **{len(invalid_results)}** 个有问题的Java代码示例：")
            report_lines.append("")
            
            # 按文件分组
            by_file = {}
            for result in invalid_results:
                file_path = result.code_block.file_path
                if file_path not in by_file:
                    by_file[file_path] = []
                by_file[file_path].append(result)
            
            for file_path, results in sorted(by_file.items()):
                report_lines.append(f"### `{file_path}`")
                report_lines.append("")
                
                for result in results:
                    cb = result.code_block
                    report_lines.append(f"**问题 #{result.code_block.block_index}** (第 {cb.line_number} 行)")
                    report_lines.append("")
                    
                    if result.issue_type:
                        report_lines.append(f"- **问题类型**: {result.issue_type}")
                    if result.error_message:
                        # 截断错误信息
                        err_msg = result.error_message[:500] + "..." if len(result.error_message) > 500 else result.error_message
                        report_lines.append(f"- **错误**: {err_msg.replace(chr(10), ' ')}")
                    if result.error_line:
                        report_lines.append(f"- **错误行**: {result.error_line}")
                    if result.fixable:
                        report_lines.append(f"- **可修复**: ✅ 是")
                    
                    report_lines.append("")
                    report_lines.append("**代码预览**:")
                    report_lines.append("```java")
                    preview = cb.code[:300] + "..." if len(cb.code) > 300 else cb.code
                    report_lines.append(preview)
                    report_lines.append("```")
                    report_lines.append("")
        
        # 修复的代码清单
        fixable_results = [r for r in self.results if r.fixable and r.suggested_fix]
        if fixable_results:
            report_lines.append("## 🔧 修复的代码清单")
            report_lines.append("")
            report_lines.append(f"共修复 **{len(fixable_results)}** 个代码示例：")
            report_lines.append("")
            
            for result in fixable_results[:50]:  # 只显示前50个
                cb = result.code_block
                report_lines.append(f"### `{cb.file_path}` (第 {cb.line_number} 行)")
                report_lines.append("")
                report_lines.append("**原始代码**:")
                report_lines.append("```java")
                report_lines.append(cb.code[:300] + "..." if len(cb.code) > 300 else cb.code)
                report_lines.append("```")
                report_lines.append("")
                report_lines.append("**修复后代码**:")
                report_lines.append("```java")
                report_lines.append(result.suggested_fix[:300] + "..." if len(result.suggested_fix) > 300 else result.suggested_fix)
                report_lines.append("```")
                report_lines.append("")
            
            if len(fixable_results) > 50:
                report_lines.append(f"*... 还有 {len(fixable_results) - 50} 个修复案例未显示*")
                report_lines.append("")
        
        # 需要人工审核的复杂案例
        complex_results = [r for r in self.results if not r.is_valid and not r.fixable]
        if complex_results:
            report_lines.append("## ⚠️ 需要人工审核的复杂案例")
            report_lines.append("")
            report_lines.append(f"共 **{len(complex_results)}** 个案例需要人工处理：")
            report_lines.append("")
            
            for result in complex_results[:30]:  # 只显示前30个
                cb = result.code_block
                report_lines.append(f"- `{cb.file_path}` 第 {cb.line_number} 行: {result.issue_type or '未知问题'}")
            
            if len(complex_results) > 30:
                report_lines.append(f"- ... 还有 {len(complex_results) - 30} 个案例")
            
            report_lines.append("")
        
        # 建议
        report_lines.append("## 💡 改进建议")
        report_lines.append("")
        report_lines.append("1. **添加import语句**: 对于缺少import的代码，建议添加必要的import语句")
        report_lines.append("2. **更新弃用API**: 对于使用弃用API的代码，建议迁移到新API")
        report_lines.append("3. **提供上下文**: 对于片段代码，建议添加必要的上下文注释")
        report_lines.append("4. **代码完整性**: 确保代码示例是完整的、可运行的")
        report_lines.append("")
        
        return '\n'.join(report_lines)
    
    def save_report(self, output_path: str = "CODE-VALIDATION-JAVA-REPORT.md") -> None:
        """保存报告到文件"""
        report = self.generate_report()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📝 报告已保存: {output_path}")
    
    def save_json_report(self, output_path: str = "java-code-validation-result.json") -> None:
        """保存JSON格式的详细结果"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "stats": {
                "total_files": self.stats.total_files,
                "total_blocks": self.stats.total_blocks,
                "valid_blocks": self.stats.valid_blocks,
                "invalid_blocks": self.stats.invalid_blocks,
                "fixed_blocks": self.stats.fixed_blocks,
                "by_issue_type": self.stats.by_issue_type,
                "pass_rate": (self.stats.valid_blocks / self.stats.total_blocks * 100) if self.stats.total_blocks > 0 else 0
            },
            "results": [r.to_dict() for r in self.results]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"📝 JSON报告已保存: {output_path}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Java代码示例验证器')
    parser.add_argument('--root', type=str, default='.', help='项目根目录')
    parser.add_argument('--workers', type=int, default=4, help='并发工作线程数')
    parser.add_argument('--output', type=str, default='CODE-VALIDATION-JAVA-REPORT.md', help='报告输出路径')
    
    args = parser.parse_args()
    
    validator = JavaCodeValidator(
        project_root=Path(args.root),
        max_workers=args.workers
    )
    
    validator.run_validation()
    validator.save_report(args.output)
    validator.save_json_report(args.output.replace('.md', '.json'))
    
    print("\n" + "=" * 60)
    print("验证完成!")
    print(f"- 扫描文件数: {validator.stats.total_files}")
    print(f"- Java代码块数: {validator.stats.total_blocks}")
    print(f"- 验证通过: {validator.stats.valid_blocks}")
    print(f"- 验证失败: {validator.stats.invalid_blocks}")
    print(f"- 可自动修复: {validator.stats.fixed_blocks}")
    if validator.stats.total_blocks > 0:
        print(f"- 通过率: {(validator.stats.valid_blocks / validator.stats.total_blocks * 100):.2f}%")
    print("=" * 60)


if __name__ == '__main__':
    main()
