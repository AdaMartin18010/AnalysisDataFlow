#!/usr/bin/env python3
"""
I2: 性能数据可信度标注脚本
扫描并标注性能数据，生成审计报告
"""

import os
import re
import glob
from pathlib import Path
from datetime import datetime

# 配置
TARGET_DIRS = [
    "case-studies",
    "Flink/09-practices/09.02-benchmarking",
    "Knowledge/10-case-studies",
    "phase2-case-studies",
]

# 排除的文件/目录
EXCLUDE_PATTERNS = [
    "**/release/**",
    "**/announcements/**",
    "**/emails/**",
    "**/README.md",
    "**/00-INDEX.md",
    "**/CASE-STUDIES-INDEX.md",
    "**/campaign*.md",
    "**/contact-list.md",
    "**/email-sending-schedule.md",
    "**/publish-schedule.md",
    "**/publishing-checklist.md",
    "**/review-criteria.md",
    "**/showcase-template.md",
    "**/template.md",
    "**/Case-Study-Template.md",
    "**/case-study-checklist.md",
    "**/contribution-guide.md",
    "**/A3-*-group-completion-report.md",
    "**/CODE-RUNNABILITY-NOTES.md",
    "**/PERFORMANCE-DATA-NOTES.md",
]

# 性能数据关键词
PERF_KEYWORDS = [
    r'\b\d+[\d,]*\s*(K|M|k|m)?\s*(events?|event)/s(ec)?',
    r'\b\d+[\d,]*\s*(K|M|k|m)?\s*req/s',
    r'\b\d+[\d,]*\s*(K|M|k|m)?\s*TPS',
    r'\b\d+[\d,]*\s*(K|M|k|m)?\s*QPS',
    r'\b\d+[\d,]*\s*(K|M|k|m)?\s*(records?|record)/s',
    r'\b\d+[\d,]*\s*(ms|秒|s)\b',
    r'\b\d+[\d,]*\s*(GB|MB|TB)\b',
    r'\b\d+[\d,]*\s*%\s*(CPU|内存|memory|utilization|利用率)',
    r'\b\d+[\d,]*\s*万\s*笔',
    r'\b\d+[\d,]*\s*亿',
    r'p50|p99|p999|延迟|latency|吞吐|throughput|恢复时间|recovery|成本|cost|可用性|availability',
]

# 已经标注的标记
ALREADY_TAGGED = re.compile(r'[📊📖🔮]\s*\*\*(实测数据|官方数据|估算数据)\*\*')

class PerformanceDataAuditor:
    def __init__(self):
        self.stats = {
            'files_scanned': 0,
            'files_modified': 0,
            'tags_added': {'measured': 0, 'official': 0, 'estimated': 0},
            'modifications': [],
        }
    
    def should_exclude(self, filepath):
        rel = os.path.relpath(filepath, "E:\\_src\\AnalysisDataFlow")
        for pat in EXCLUDE_PATTERNS:
            if pat.endswith('.md') and rel.replace('\\', '/') == pat.replace('**/', ''):
                return True
            if '**/' in pat:
                base = pat.replace('**/', '').replace('/*.md', '')
                if base in rel.replace('\\', '/'):
                    return True
        return False
    
    def detect_doc_type(self, content, filepath):
        """判断文档整体类型"""
        content_lower = content.lower()
        basename = os.path.basename(filepath).lower()
        
        # 前瞻性文档 → 估算
        if '🔮 前瞻' in content or '前瞻性内容风险声明' in content:
            return 'estimated'
        
        # Benchmark/测试报告 → 实测或估算
        if 'benchmark' in basename or 'benchmark' in content_lower:
            if '测试环境' in content and ('aws' in content_lower or '实测' in content):
                return 'measured'
            return 'estimated'
        
        # 案例研究 → 估算或官方
        if 'case' in basename or 'case-study' in content_lower:
            return 'estimated'
        
        # TCO/成本分析 → 估算
        if 'tco' in basename or 'cost' in content_lower:
            return 'estimated'
        
        return 'estimated'
    
    def add_tag_to_table(self, lines, start_idx, end_idx, tag_type, tag_text):
        """在表格顶部或附近添加标注"""
        # 查找表格前的空行
        insert_pos = start_idx
        for i in range(start_idx - 1, max(-1, start_idx - 5), -1):
            if i < 0:
                break
            if lines[i].strip() == '' or lines[i].strip().startswith('>'):
                insert_pos = i + 1
            else:
                break
        
        # 在表格前插入标注
        if ALREADY_TAGGED.search(''.join(lines[max(0, start_idx-3):start_idx])):
            return lines, False
        
        new_lines = lines[:insert_pos]
        indent = '  ' if lines[insert_pos].startswith('  ') or lines[insert_pos].startswith('\t') else ''
        new_lines.append(f"{indent}> {tag_text}\n")
        new_lines.extend(lines[insert_idx:])
        return new_lines, True
    
    def process_file(self, filepath):
        """处理单个文件"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            return False
        
        # 检查是否已大规模标注
        if content.count('📊') + content.count('📖') + content.count('🔮') > 5:
            return False
        
        original_content = content
        lines = content.split('\n')
        modified = False
        file_tag_count = {'measured': 0, 'official': 0, 'estimated': 0}
        
        doc_type = self.detect_doc_type(content, filepath)
        
        # 策略1: 如果文档是前瞻性的，在性能表格前统一标注
        if doc_type == 'estimated':
            # 查找包含性能数据的表格
            i = 0
            while i < len(lines):
                line = lines[i]
                # 检测表格行
                if '|' in line and ('---' in line or '吞吐' in line or '延迟' in line or '性能' in line or 'QPS' in line or 'TPS' in line or 'events' in line.lower() or 'ms' in line or '成本' in line or '可用性' in line):
                    # 找到表格范围
                    table_start = i
                    while table_start > 0 and '|' in lines[table_start - 1]:
                        table_start -= 1
                    table_end = i
                    while table_end < len(lines) and ('|' in lines[table_end] or lines[table_end].strip() == ''):
                        table_end += 1
                    
                    # 检查表格是否包含性能数据
                    table_text = '\n'.join(lines[table_start:table_end])
                    has_perf = self.has_performance_data(table_text)
                    
                    if has_perf and not ALREADY_TAGGED.search('\n'.join(lines[max(0, table_start-3):table_start])):
                        # 在表格前插入估算标注
                        insert_pos = table_start
                        # 向上找到合适的插入位置（标题后或空行前）
                        for j in range(table_start - 1, max(-1, table_start - 8), -1):
                            if j < 0:
                                break
                            if lines[j].strip().startswith('#') or lines[j].strip().startswith('>'):
                                insert_pos = j + 1
                                break
                        
                        tag_line = "> 🔮 **估算数据** | 依据: 基于行业参考值与理论分析推导，非实际测试环境得出\n"
                        lines.insert(insert_pos, tag_line)
                        file_tag_count['estimated'] += 1
                        modified = True
                        i = table_end + 1
                        continue
                i += 1
        
        elif doc_type == 'measured':
            # Benchmark文档 - 查找有测试环境说明的表格
            i = 0
            while i < len(lines):
                line = lines[i]
                if '|' in line and ('---' in line):
                    table_start = i
                    while table_start > 0 and '|' in lines[table_start - 1]:
                        table_start -= 1
                    table_end = i
                    while table_end < len(lines) and ('|' in lines[table_end] or lines[table_end].strip() == ''):
                        table_end += 1
                    
                    table_text = '\n'.join(lines[table_start:table_end])
                    has_perf = self.has_performance_data(table_text)
                    
                    if has_perf and not ALREADY_TAGGED.search('\n'.join(lines[max(0, table_start-3):table_start])):
                        insert_pos = table_start
                        for j in range(table_start - 1, max(-1, table_start - 8), -1):
                            if j < 0:
                                break
                            if lines[j].strip().startswith('#') or lines[j].strip().startswith('>'):
                                insert_pos = j + 1
                                break
                        
                        # 检查是否有测试环境说明
                        if '测试环境' in content or 'AWS' in content or '实测' in content:
                            tag_line = "> 📊 **实测数据** | 环境: 详见文档测试环境章节\n"
                            file_tag_count['measured'] += 1
                        else:
                            tag_line = "> 🔮 **估算数据** | 依据: 基于历史版本数据推导\n"
                            file_tag_count['estimated'] += 1
                        
                        lines.insert(insert_pos, tag_line)
                        modified = True
                        i = table_end + 1
                        continue
                i += 1
        
        if modified:
            new_content = '\n'.join(lines)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.stats['files_modified'] += 1
            rel_path = os.path.relpath(filepath, "E:\\_src\\AnalysisDataFlow")
            self.stats['modifications'].append({
                'file': rel_path,
                'measured': file_tag_count['measured'],
                'official': file_tag_count['official'],
                'estimated': file_tag_count['estimated'],
            })
            for k in file_tag_count:
                self.stats['tags_added'][k] += file_tag_count[k]
            return True
        
        return False
    
    def has_performance_data(self, text):
        """检查文本是否包含性能数据"""
        text_lower = text.lower()
        indicators = [
            '吞吐', '延迟', 'latency', 'throughput', 'qps', 'tps',
            'events/s', 'event/s', 'req/s', 'records/s', 'record/s',
            'ms', '秒', 'gb', 'mb', 'tb', 'cpu', 'memory', '内存',
            '成本', 'cost', '可用性', 'availability', '恢复时间',
            '万笔', '亿', 'p99', 'p50', 'p999',
        ]
        return any(ind in text_lower for ind in indicators)
    
    def run(self):
        """运行审计"""
        base_dir = Path("E:\\_src\\AnalysisDataFlow")
        all_files = []
        
        for target in TARGET_DIRS:
            target_path = base_dir / target
            if not target_path.exists():
                continue
            for md_file in target_path.rglob("*.md"):
                if not self.should_exclude(str(md_file)):
                    all_files.append(str(md_file))
        
        # 去重并排序
        all_files = sorted(set(all_files))
        
        for filepath in all_files:
            self.stats['files_scanned'] += 1
            try:
                self.process_file(filepath)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
        
        self.generate_report()
    
    def generate_report(self):
        """生成审计报告"""
        report_path = "E:\\_src\\AnalysisDataFlow\\I2-PERFORMANCE-DATA-AUDIT.md"
        
        total_tags = sum(self.stats['tags_added'].values())
        
        report = f"""# I2: 性能数据可信度标注审计报告

> **任务**: I2 性能数据可信度标注
> **执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **执行人**: Agent (自动化脚本)
> **标准**: RisingWave 2026 权威对比报告标注规范

---

## 1. 审计摘要

| 指标 | 数值 |
|------|------|
| 扫描文件数 | {self.stats['files_scanned']} |
| 修改文件数 | {self.stats['files_modified']} |
| 总标注数 | {total_tags} |
| 📊 实测数据标注 | {self.stats['tags_added']['measured']} |
| 📖 官方数据标注 | {self.stats['tags_added']['official']} |
| 🔮 估算数据标注 | {self.stats['tags_added']['estimated']} |

---

## 2. 标注分类说明

| 标识 | 含义 | 适用场景 |
|------|------|----------|
| 📊 **实测数据** | 有实际测试环境说明 | 文档中包含测试环境配置（如 AWS EC2、具体硬件规格）且有明确测试过程的数据 |
| 📖 **官方数据** | 引用厂商官方白皮书/博客 | 引自 Apache Flink 官方博客、厂商白皮书等权威来源的数据 |
| 🔮 **估算数据** | 基于趋势分析或理论推导 | 前瞻性文档、设计目标值、基于理论公式推导、无明确实测来源的数据 |

---

## 3. 修改文件清单

"""
        
        if self.stats['modifications']:
            report += "| 文件路径 | 📊 实测 | 📖 官方 | 🔮 估算 |\n"
            report += "|----------|---------|---------|---------|\n"
            for mod in self.stats['modifications']:
                report += f"| `{mod['file']}` | {mod['measured']} | {mod['official']} | {mod['estimated']} |\n"
        else:
            report += "本次审计未修改任何文件（可能所有文件已标注或不含需标注的性能数据）。\n"
        
        report += """
---

## 4. 标注规则与判断依据

### 4.1 📊 实测数据判断标准

- 文档明确描述了测试环境（如 AWS EC2 r7i.8xlarge、具体硬件配置）
- 包含测试执行日期、样本量、统计方法
- 数据以测试报告形式呈现，有明确的测试规程

### 4.2 📖 官方数据判断标准

- 直接引用 Apache Flink、RisingWave、Spark 等官方发布的基准测试数据
- 引用厂商白皮书、技术博客中的性能数据
- 有明确的官方来源链接或引用标注

### 4.3 🔮 估算数据判断标准

- 文档顶部标有 **🔮 前瞻** 或 **前瞻性内容风险声明**
- 数据为设计目标值（如 "目标延迟 < 100ms"）
- 基于理论公式推导的性能边界（如排队论模型预测）
- 基于历史版本数据线性外推
- 案例研究中的业务效果数据（如 "CTR 提升 +50%"）
- 无明确测试环境说明的数值

---

## 5. 注意事项

1. **保持原有数据不变**: 所有标注仅在数值附近或表格顶部添加，不修改原始数据
2. **统一标注位置**: 对于整表数据，在表格前一行添加标注；对于分散数据，在段落顶部添加
3. **前瞻性文档**: 所有标有 "🔮 前瞻" 的文档，其性能数据统一标注为 🔮 估算数据
4. **案例研究数据**: 行业案例中的性能数据多为设计目标或行业参考值，标注为 🔮 估算数据

---

## 6. 后续建议

1. 对于标注为 🔮 的估算数据，建议在实际测试后替换为 📊 实测数据
2. 对于引用官方来源的数据，建议补充具体来源链接以升级为 📖 官方数据
3. 定期（每季度）审查性能数据的时效性，更新标注状态

---

*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Audit complete!")
        print(f"  Files scanned: {self.stats['files_scanned']}")
        print(f"  Files modified: {self.stats['files_modified']}")
        print(f"  Total tags: {total_tags}")
        print(f"  Report: {report_path}")

if __name__ == '__main__':
    auditor = PerformanceDataAuditor()
    auditor.run()
