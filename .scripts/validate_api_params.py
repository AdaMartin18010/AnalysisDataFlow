#!/usr/bin/env python3
"""
AnalysisDataFlow API参数验证工具
=================================
功能：扫描文档中的API参数，标记可能是虚构的参数

P1-9: 自动检查虚构API参数

作者: AnalysisDataFlow CI/CD Team
版本: 1.0.0
"""

import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime


# =============================================================================
# Flink官方API参数库
# =============================================================================

# Flink DataStream API配置参数
FLINK_DATASTREAM_PARAMS = {
    # 环境配置
    'setParallelism',
    'setMaxParallelism',
    'setAutoWatermarkInterval',
    'setBufferTimeout',
    'disableOperatorChaining',
    'enableCheckpointing',
    'getCheckpointConfig',
    'setStateBackend',
    'setRestartStrategy',
    
    # 时间特性
    'setStreamTimeCharacteristic',  # 已废弃但仍可能出现在文档中
    'getConfig',
    
    # Checkpoint配置
    'setCheckpointingMode',
    'setCheckpointInterval',
    'setCheckpointTimeout',
    'setMinPauseBetweenCheckpoints',
    'setMaxConcurrentCheckpoints',
    'enableExternalizedCheckpoints',
    'enableUnalignedCheckpoints',
    'setAlignmentTimeout',
    'setForceUnalignedCheckpoints',
    
    # State Backend配置
    'setStateBackend',
    'setMemoryStateBackend',
    'setFsStateBackend',
    'setRocksDBStateBackend',
    
    # Restart Strategy配置
    'setRestartStrategy',
    'fixedDelayRestart',
    'exponentialDelayRestart',
    'failureRateRestart',
    'noRestart',
}

# Flink Table API配置参数
FLINK_TABLE_PARAMS = {
    # 表配置
    'set',
    'get',
    'inBatchMode',
    'inStreamingMode',
    
    # 常见配置键
    'table.exec.mini-batch.enabled',
    'table.exec.mini-batch.allow-latency',
    'table.exec.mini-batch.size',
    'table.exec.state.ttl',
    'table.exec.source.idle-timeout',
    'table.optimizer.distinct-agg.split.enabled',
    'table.exec.spill-compression.enabled',
    'table.exec.spill-compression.block-size',
    'table.exec.resource.default-parallelism',
    
    # Planner配置
    'table.planner',
    'table.dml-sync',
}

# Flink SQL配置参数
FLINK_SQL_PARAMS = {
    # SET/RESET命令
    'SET',
    'RESET',
    
    # 常见SQL配置
    'pipeline.name',
    'parallelism.default',
    'taskmanager.memory.process.size',
    'jobmanager.memory.process.size',
    'state.backend',
    'state.checkpoints.dir',
    'execution.checkpointing.interval',
    'table.sql-dialect',
}

# Flink Connectors配置参数
FLINK_CONNECTOR_PARAMS = {
    # Kafka connector
    'properties.bootstrap.servers',
    'properties.group.id',
    'topic',
    'topics',
    'topic-pattern',
    'format',
    'scan.startup.mode',
    'scan.startup.specific-offsets',
    'scan.startup.timestamp-millis',
    'sink.partitioner',
    'sink.semantic',
    'sink.transactional-id-prefix',
    
    # JDBC connector
    'url',
    'table-name',
    'driver',
    'username',
    'password',
    'scan.fetch-size',
    'scan.partition.column',
    'scan.partition.num',
    'scan.partition.lower-bound',
    'scan.partition.upper-bound',
    'lookup.cache.max-rows',
    'lookup.cache.ttl',
    'lookup.max-retries',
    'sink.buffer-flush.max-rows',
    'sink.buffer-flush.interval',
    'sink.max-retries',
    
    # FileSystem connector
    'path',
    'format',
    'partition.default-name',
    'sink.shuffle-by-partition.enable',
    'sink.rolling-policy.file-size',
    'sink.rolling-policy.rollover-interval',
    'sink.rolling-policy.inactivity-interval',
    'sink.partition-commit.trigger',
    'sink.partition-commit.delay',
    'sink.partition-commit.policy.kind',
    'sink.partition-commit.success-file.name',
    'source.monitor-interval',
    'source.path.regex-pattern',
    
    # Elasticsearch connector
    'hosts',
    'index',
    'document-id.delimiter',
    'document-id.key-delimiter',
    'document-type',
    'username',
    'password',
    'failure-handler',
    'sink.flush-on-checkpoint',
    'sink.bulk-flush.max-actions',
    'sink.bulk-flush.max-size',
    'sink.bulk-flush.interval',
    'sink.bulk-flush.backoff.strategy',
    'sink.bulk-flush.backoff.max-retries',
    'sink.bulk-flush.backoff.delay',
    'connection.max-retry-timeout',
    'connection.path-prefix',
}

# 合并所有已知参数
ALL_KNOWN_PARAMS = (
    FLINK_DATASTREAM_PARAMS | 
    FLINK_TABLE_PARAMS | 
    FLINK_SQL_PARAMS | 
    FLINK_CONNECTOR_PARAMS
)


# =============================================================================
# 可疑模式检测
# =============================================================================

# 虚构参数的常见模式
SUSPICIOUS_PATTERNS = {
    # 占位符模式
    'placeholders': [
        r'your-\w+',
        r'my-\w+',
        r'xxx',
        r'example-\w+',
        r'test-\w+',
        r'dummy-\w+',
        r'placeholder-\w+',
    ],
    
    # 不完整的参数名
    'incomplete': [
        r'\w+\.\.+',  # 例如: table.exec...
        r'\w+<.*>',   # 包含泛型但未闭合
        r'\$\{\w+\}', # 变量占位
    ],
    
    # 过时的参数名模式
    'outdated': [
        r'flink\.contrib\.',  # contrib已移除
        r'storm\.compat\.',
        r'flink\.streaming\.connectors\.',  # 旧包名
    ],
    
    # 可能的拼写错误
    'possible_typos': [
        r'paralell',  # parallel的拼写错误
        r'chekpoint',  # checkpoint的拼写错误
        r'wartermark',  # watermark的拼写错误
        r'stat[e]?backend',  # state backend连写
        r'checkpiont',
    ]
}

# 上下文敏感的可疑模式
CONTEXT_SUSPICIOUS = {
    # 在配置上下文中出现的可疑值
    'config_value': [
        r'\d+[smhd]\d+',  # 时间单位格式错误，如 1h30（缺少单位）
        r'true|false',  # 布尔值通常没问题，但配合未知参数时需检查
    ],
    
    # 类名模式
    'class_name': [
        r'com\.example\.',  # 示例包名
        r'org\.mycompany\.',  # 示例包名
    ]
}


# =============================================================================
# 数据类定义
# =============================================================================

@dataclass
class APIParamUsage:
    """API参数使用记录"""
    param_name: str
    file_path: str
    line_number: int
    context: str
    param_type: str  # 'config_key', 'method_call', 'class_name', etc.
    is_known: bool
    is_suspicious: bool
    suspicion_reason: str = None


# =============================================================================
# 参数提取器
# =============================================================================

class APIParamExtractor:
    """API参数提取器"""
    
    def __init__(self):
        self.findings: List[APIParamUsage] = []
    
    def extract_from_code_block(self, content: str, file_path: str) -> List[APIParamUsage]:
        """从代码块中提取参数"""
        findings = []
        
        # 提取配置键（xxx.yyy.zzz模式）
        config_pattern = r'["\']([a-z][a-z0-9]*(?:\.[a-z][a-z0-9-]*)+)["\']'
        
        # 提取方法调用（xxx.yyy()模式）
        method_pattern = r'\.([a-z][a-zA-Z0-9]*)\s*\('
        
        # 提取类名引用
        class_pattern = r'([a-zA-Z][a-zA-Z0-9]*(?:\.[a-zA-Z][a-zA-Z0-9]*)+)\.'
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # 配置键
            for match in re.finditer(config_pattern, line):
                param = match.group(1)
                is_known = self._is_known_param(param)
                is_suspicious, reason = self._check_suspicious(param, line)
                
                findings.append(APIParamUsage(
                    param_name=param,
                    file_path=file_path,
                    line_number=line_num,
                    context=line.strip(),
                    param_type='config_key',
                    is_known=is_known,
                    is_suspicious=is_suspicious,
                    suspicion_reason=reason
                ))
            
            # 方法调用
            for match in re.finditer(method_pattern, line):
                method = match.group(1)
                is_known = method in ALL_KNOWN_PARAMS
                is_suspicious, reason = self._check_suspicious(method, line)
                
                findings.append(APIParamUsage(
                    param_name=method,
                    file_path=file_path,
                    line_number=line_num,
                    context=line.strip(),
                    param_type='method_call',
                    is_known=is_known,
                    is_suspicious=is_suspicious,
                    suspicion_reason=reason
                ))
        
        return findings
    
    def extract_from_tables(self, content: str, file_path: str) -> List[APIParamUsage]:
        """从Markdown表格中提取参数"""
        findings = []
        
        # 匹配表格中的代码格式参数名
        table_cell_pattern = r'\|\s*`([^`]+)`\s*\|'
        
        lines = content.split('\n')
        in_table = False
        table_start = 0
        
        for line_num, line in enumerate(lines, 1):
            if '|' in line:
                if not in_table:
                    in_table = True
                    table_start = line_num
                
                for match in re.finditer(table_cell_pattern, line):
                    param = match.group(1)
                    # 只关注看起来像配置键的内容
                    if '.' in param or param in ALL_KNOWN_PARAMS:
                        is_known = self._is_known_param(param)
                        is_suspicious, reason = self._check_suspicious(param, line)
                        
                        findings.append(APIParamUsage(
                            param_name=param,
                            file_path=file_path,
                            line_number=line_num,
                            context=line.strip(),
                            param_type='table_entry',
                            is_known=is_known,
                            is_suspicious=is_suspicious,
                            suspicion_reason=reason
                        ))
            else:
                in_table = False
        
        return findings
    
    def extract_from_inline_code(self, content: str, file_path: str) -> List[APIParamUsage]:
        """从行内代码中提取参数"""
        findings = []
        
        # 行内代码模式
        inline_pattern = r'`([^`]+)`'
        
        lines = content.split('\n')
        code_block_depth = 0
        
        for line_num, line in enumerate(lines, 1):
            # 跳过代码块
            if line.strip().startswith('```'):
                code_block_depth = 1 - code_block_depth
                continue
            
            if code_block_depth > 0:
                continue
            
            for match in re.finditer(inline_pattern, line):
                param = match.group(1)
                
                # 只处理看起来像参数的内容
                if self._looks_like_param(param):
                    is_known = self._is_known_param(param)
                    is_suspicious, reason = self._check_suspicious(param, line)
                    
                    findings.append(APIParamUsage(
                        param_name=param,
                        file_path=file_path,
                        line_number=line_num,
                        context=line.strip(),
                        param_type='inline_code',
                        is_known=is_known,
                        is_suspicious=is_suspicious,
                        suspicion_reason=reason
                    ))
        
        return findings
    
    def _is_known_param(self, param: str) -> bool:
        """检查参数是否在已知列表中"""
        if param in ALL_KNOWN_PARAMS:
            return True
        
        # 检查前缀匹配
        for known in ALL_KNOWN_PARAMS:
            if param.startswith(known + '.') or known.startswith(param + '.'):
                return True
        
        return False
    
    def _check_suspicious(self, param: str, context: str) -> Tuple[bool, str]:
        """检查参数是否可疑"""
        param_lower = param.lower()
        context_lower = context.lower()
        
        # 检查占位符模式
        for pattern in SUSPICIOUS_PATTERNS['placeholders']:
            if re.search(pattern, param_lower):
                return True, f"疑似占位符模式: {pattern}"
        
        # 检查不完整模式
        for pattern in SUSPICIOUS_PATTERNS['incomplete']:
            if re.search(pattern, param):
                return True, "参数名不完整"
        
        # 检查过时模式
        for pattern in SUSPICIOUS_PATTERNS['outdated']:
            if re.search(pattern, param_lower):
                return True, "使用过时的包名或前缀"
        
        # 检查可能的拼写错误
        for pattern in SUSPICIOUS_PATTERNS['possible_typos']:
            if re.search(pattern, param_lower):
                return True, f"可能的拼写错误: {pattern}"
        
        return False, None
    
    def _looks_like_param(self, text: str) -> bool:
        """判断文本是否看起来像参数"""
        # 包含点号的可能是配置键
        if '.' in text and text.replace('.', '').replace('-', '').isalnum():
            return True
        
        # 已知参数
        if text in ALL_KNOWN_PARAMS:
            return True
        
        # camelCase方法名
        if re.match(r'^[a-z]+([A-Z][a-z0-9]*)+$', text):
            return True
        
        return False
    
    def process_file(self, file_path: Path) -> List[APIParamUsage]:
        """处理单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"   ⚠️  无法读取 {file_path}: {e}")
            return []
        
        findings = []
        
        # 从代码块提取
        findings.extend(self.extract_from_code_block(content, str(file_path)))
        
        # 从表格提取
        findings.extend(self.extract_from_tables(content, str(file_path)))
        
        # 从行内代码提取
        findings.extend(self.extract_from_inline_code(content, str(file_path)))
        
        return findings


# =============================================================================
# 报告生成
# =============================================================================

def generate_validation_report(
    findings: List[APIParamUsage],
    output_path: Path,
    json_path: Optional[Path] = None
):
    """生成验证报告"""
    
    # 分类统计
    known_params = [f for f in findings if f.is_known]
    unknown_params = [f for f in findings if not f.is_known]
    suspicious_params = [f for f in findings if f.is_suspicious]
    
    # 按文件分组
    by_file = defaultdict(list)
    for f in findings:
        by_file[f.file_path].append(f)
    
    lines = [
        "# 🔍 API参数验证报告",
        "",
        f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"> **扫描参数**: {len(findings)} 个",
        "",
        "## 📊 统计摘要",
        "",
        f"| 类别 | 数量 | 状态 |",
        f"|------|------|------|",
        f"| ✅ 已知参数 | {len(known_params)} | 确认有效 |",
        f"| ⚠️  未知参数 | {len(unknown_params)} | 需要验证 |",
        f"| ❌ 可疑参数 | {len(suspicious_params)} | **需要修正** |",
        "",
    ]
    
    # 可疑参数详情
    if suspicious_params:
        lines.extend([
            "## ❌ 可疑参数详情（需修正）",
            "",
            "以下参数被标记为可疑，请检查是否正确：",
            "",
        ])
        
        for finding in suspicious_params:
            lines.extend([
                f"### {finding.param_name}",
                "",
                f"- **文件**: `{finding.file_path}` (第{finding.line_number}行)",
                f"- **类型**: {finding.param_type}",
                f"- **可疑原因**: {finding.suspicion_reason}",
                f"- **上下文**: `{finding.context[:100]}{'...' if len(finding.context) > 100 else ''}`",
                "",
            ])
        
        lines.extend([
            "### 修复建议",
            "",
            "1. **确认参数拼写**: 检查是否有拼写错误",
            "2. **验证参数存在**: 查阅Flink官方文档确认参数是否存在",
            "3. **更新参数库**: 如果是新参数，请更新 `.scripts/validate_api_params.py` 中的已知参数列表",
            "4. **使用占位符**: 如果是示例参数，请使用明显的占位符格式如 `your-param-name`",
            "",
        ])
    
    # 未知参数列表
    if unknown_params and len(unknown_params) <= 50:
        lines.extend([
            "## ⚠️ 未知参数列表（需验证）",
            "",
            "以下参数不在已知参数库中，请验证其有效性：",
            "",
            "| 参数名 | 文件 | 行号 | 类型 |",
            "|--------|------|------|------|",
        ])
        
        for finding in unknown_params[:50]:  # 限制数量
            lines.append(
                f"| `{finding.param_name}` | {finding.file_path} | {finding.line_number} | {finding.param_type} |"
            )
        
        lines.append("")
    
    # 按文件汇总
    lines.extend([
        "## 📁 按文件汇总",
        "",
    ])
    
    for file_path, file_findings in sorted(by_file.items()):
        suspicious_count = sum(1 for f in file_findings if f.is_suspicious)
        unknown_count = sum(1 for f in file_findings if not f.is_known)
        
        lines.extend([
            f"### {file_path}",
            "",
            f"- 总参数: {len(file_findings)}",
        ])
        
        if suspicious_count:
            lines.append(f"- ❌ 可疑: {suspicious_count}")
        if unknown_count:
            lines.append(f"- ⚠️  未知: {unknown_count}")
        
        lines.append("")
    
    # 已知参数库版本
    lines.extend([
        "## 📚 已知参数库",
        "",
        f"当前参数库包含: **{len(ALL_KNOWN_PARAMS)}** 个已知参数",
        "",
        "### 覆盖范围",
        "",
        f"- DataStream API: {len(FLINK_DATASTREAM_PARAMS)} 个",
        f"- Table API: {len(FLINK_TABLE_PARAMS)} 个",
        f"- SQL: {len(FLINK_SQL_PARAMS)} 个",
        f"- Connectors: {len(FLINK_CONNECTOR_PARAMS)} 个",
        "",
        "### 更新参数库",
        "",
        "```bash",
        "# 发现新的有效参数后，添加到 .scripts/validate_api_params.py",
        "# 相应类别的参数集合中",
        "```",
        "",
    ])
    
    # 写入报告
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    # 生成JSON报告
    if json_path:
        json_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'version': '1.0'
            },
            'summary': {
                'total_params': len(findings),
                'known_params': len(known_params),
                'unknown_params': len(unknown_params),
                'suspicious_params': len(suspicious_params)
            },
            'suspicious_params': [
                {
                    'param_name': f.param_name,
                    'file': f.file_path,
                    'line': f.line_number,
                    'type': f.param_type,
                    'reason': f.suspicion_reason,
                    'context': f.context
                }
                for f in suspicious_params
            ],
            'unknown_params': [
                {
                    'param_name': f.param_name,
                    'file': f.file_path,
                    'line': f.line_number,
                    'type': f.param_type
                }
                for f in unknown_params
            ]
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)


# =============================================================================
# 主程序
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow API参数验证工具'
    )
    parser.add_argument(
        '--path', '-p',
        default='.',
        help='要检查的根目录路径'
    )
    parser.add_argument(
        '--output', '-o',
        default='reports/api-validation-report.md',
        help='报告输出路径'
    )
    parser.add_argument(
        '--json', '-j',
        default='reports/api-validation-results.json',
        help='JSON结果输出路径'
    )
    parser.add_argument(
        '--focus',
        choices=['suspicious', 'unknown', 'all'],
        default='all',
        help='关注重点: suspicious=仅可疑, unknown=未知参数, all=全部'
    )
    
    args = parser.parse_args()
    
    root_path = Path(args.path).resolve()
    output_path = Path(args.output)
    json_path = Path(args.json)
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("AnalysisDataFlow API参数验证工具")
    print("=" * 70)
    print(f"检查路径: {root_path}")
    print(f"输出报告: {output_path}")
    print("=" * 70)
    
    # 收集Markdown文件
    print("\n📁 扫描Markdown文件...")
    md_files = list(root_path.rglob('*.md'))
    md_files = [
        f for f in md_files 
        if not any(part.startswith('.') for part in f.parts)
    ]
    print(f"   找到 {len(md_files)} 个Markdown文件")
    
    # 提取参数
    print("\n🔍 提取API参数...")
    extractor = APIParamExtractor()
    all_findings = []
    
    for i, md_file in enumerate(md_files, 1):
        findings = extractor.process_file(md_file)
        all_findings.extend(findings)
        
        if i % 50 == 0 or i == len(md_files):
            print(f"   进度: {i}/{len(md_files)} 文件")
    
    print(f"\n📊 提取结果:")
    print(f"   总参数: {len(all_findings)}")
    print(f"   已知参数: {sum(1 for f in all_findings if f.is_known)}")
    print(f"   未知参数: {sum(1 for f in all_findings if not f.is_known)}")
    print(f"   可疑参数: {sum(1 for f in all_findings if f.is_suspicious)}")
    
    # 生成报告
    print("\n📝 生成报告...")
    generate_validation_report(all_findings, output_path, json_path)
    print(f"   Markdown报告: {output_path}")
    print(f"   JSON报告: {json_path}")
    
    print("\n" + "=" * 70)
    print("验证完成!")
    print("=" * 70)
    
    # 返回退出码
    suspicious_count = sum(1 for f in all_findings if f.is_suspicious)
    
    if suspicious_count > 0:
        print(f"⚠️  发现 {suspicious_count} 个可疑参数")
        return 1
    else:
        print("✅ 未发现可疑参数")
        return 0


if __name__ == '__main__':
    exit(main())
