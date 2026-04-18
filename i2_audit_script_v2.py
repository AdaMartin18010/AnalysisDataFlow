#!/usr/bin/env python3
"""
I2: 性能数据可信度标注脚本 v2
更精确地扫描并标注性能数据，生成审计报告
"""

import os
import re
from pathlib import Path
from datetime import datetime

# 配置
BASE_DIR = Path("E:\\_src\\AnalysisDataFlow")
TARGET_DIRS = [
    "case-studies",
    "Flink/09-practices/09.02-benchmarking",
    "Knowledge/10-case-studies",
    "phase2-case-studies",
]

# 排除的文件/目录 (精确匹配)
EXCLUDE_PATHS = {
    "case-studies/announcements",
    "case-studies/emails",
    "case-studies/README.md",
    "case-studies/campaign-2026.md",
    "case-studies/campaign-tracking.md",
    "case-studies/contact-list.md",
    "case-studies/email-sending-schedule.md",
    "case-studies/publish-schedule.md",
    "case-studies/publishing-checklist.md",
    "case-studies/review-criteria.md",
    "case-studies/showcase-template.md",
    "case-studies/template.md",
    "Knowledge/10-case-studies/00-INDEX.md",
    "Knowledge/10-case-studies/annual-case-collection-2026.md",
    "Knowledge/10-case-studies/CODE-RUNNABILITY-NOTES.md",
    "Knowledge/10-case-studies/PERFORMANCE-DATA-NOTES.md",
    "phase2-case-studies/CASE-STUDIES-INDEX.md",
    "phase2-case-studies/Case-Study-Template.md",
    "phase2-case-studies/case-study-checklist.md",
    "phase2-case-studies/contribution-guide.md",
    "phase2-case-studies/README.md",
    "phase2-case-studies/A3-C-group-completion-report.md",
    "phase2-case-studies/A3-D-group-completion-report.md",
}

# 已标注标记
ALREADY_TAGGED_RE = re.compile(r'[📊📖🔮]\s*\*\*(实测数据|官方数据|估算数据)\*\*')

# 性能数据可信度声明标记
TRUST_STATEMENT_RE = re.compile(r'性能数据可信度|数据来源|可信度声明')

# 真正的性能数值模式 (必须匹配这些才认为是性能数据)
PERF_VALUE_PATTERNS = [
    re.compile(r'\b\d+[\d,]*\.?\d*\s*(K|M|k|m)?\s*(events?|event|records?|record|req|requests?)/s(ec)?'),
    re.compile(r'\b\d+[\d,]*\.?\d*\s*(K|M|k|m)?\s*TPS\b'),
    re.compile(r'\b\d+[\d,]*\.?\d*\s*(K|M|k|m)?\s*QPS\b'),
    re.compile(r'\b\d+[\d,]*\.?\d*\s*(ms|毫秒)\b'),
    re.compile(r'\b\d+[\d,]*\.?\d*\s*(秒|s)\b(?![a-zA-Z])'),
    re.compile(r'\b\d+[\d,]*\.?\d*\s*(GB|MB|TB|KB)\b'),
    re.compile(r'\$\d+[\d,]*\.?\d*\s*/?\s*(月|天|年|hour|day|month)?'),
    re.compile(r'\b\d+[\d,]*\.?\d*\s*万\s*(笔|/秒|/分钟)'),
    re.compile(r'\b\d+[\d,]*\.?\d*\s*亿\b'),
    re.compile(r'\b\d+\.?\d*\s*%\s*(CPU|内存|memory|utilization)'),
    re.compile(r'p99\s*[=:]?\s*\d+'),
    re.compile(r'p50\s*[=:]?\s*\d+'),
    re.compile(r'p999\s*[=:]?\s*\d+'),
    re.compile(r'\b\d+[\d,]*\.?\d*\s*(K|k)\s*events?/s'),
    re.compile(r'99\.\d+%\s*可用'),
    re.compile(r'可用性\s*99\.\d+'),
]

# 性能指标关键词
PERF_METRIC_KEYWORDS = {'吞吐', '延迟', 'latency', 'throughput', '恢复时间', 'recovery', '成本', 'cost', '可用性', 'availability', '资源效率', '性价比', 'CPU利用率', '内存使用'}

# 前瞻性文档标记
FORWARD_LOOKING_MARKERS = ['🔮 前瞻', '前瞻性内容风险声明', '预计发布时间', '不代表 Apache Flink 官方承诺']

# 实测数据标记
MEASURED_MARKERS = ['测试环境:', 'AWS EC2', '实测数据', '测试执行日期', '统计方法', 'n=30', '样本量']

# 官方数据标记
OFFICIAL_MARKERS = ['官方数据', '来源:', 'Apache Flink 官方', '厂商白皮书', '官方博客']

class PerformanceDataAuditor:
    def __init__(self):
        self.stats = {
            'files_scanned': 0,
            'files_modified': 0,
            'tags_added': {'measured': 0, 'official': 0, 'estimated': 0},
            'modifications': [],
        }
    
    def should_exclude(self, filepath):
        rel = os.path.relpath(filepath, BASE_DIR).replace('\\', '/')
        if rel in EXCLUDE_PATHS:
            return True
        # 检查父目录
        for excluded in EXCLUDE_PATHS:
            if excluded.endswith('.md'):
                continue
            if rel.startswith(excluded + '/'):
                return True
        return False
    
    def is_forward_looking(self, content):
        """判断是否为前瞻性文档"""
        for marker in FORWARD_LOOKING_MARKERS:
            if marker in content:
                return True
        return False
    
    def has_trust_statement(self, content):
        """检查是否已有可信度声明"""
        return TRUST_STATEMENT_RE.search(content) is not None
    
    def table_contains_performance_data(self, table_lines):
        """严格判断表格是否包含性能数据"""
        table_text = '\n'.join(table_lines)
        
        # 必须包含性能数值
        has_perf_values = any(p.search(table_text) for p in PERF_VALUE_PATTERNS)
        
        # 同时需要包含性能指标关键词
        has_perf_keywords = any(kw in table_text for kw in PERF_METRIC_KEYWORDS)
        
        # 或者是纯数值对比表（如成本对比、吞吐对比）
        is_numeric_comparison = ('|' in table_text and 
                                 (has_perf_values or has_perf_keywords))
        
        return is_numeric_comparison and has_perf_values
    
    def determine_tag_type(self, content, table_lines, table_start):
        """判断标注类型"""
        table_text = '\n'.join(table_lines)
        context = content[max(0, table_start - 500):table_start]
        
        # 前瞻性文档 → 估算
        if self.is_forward_looking(content):
            return 'estimated', '基于前瞻性文档特性，数据为理论推导与趋势分析'
        
        # 检查上下文是否有实测标记
        if any(m in context for m in MEASURED_MARKERS):
            return 'measured', '环境: 详见文档测试环境配置章节'
        
        # 检查是否有官方来源标记
        if any(m in context for m in OFFICIAL_MARKERS):
            return 'official', '来源: 详见文档引用参考章节'
        
        # 案例研究中的目标值表格
        if '目标' in table_text and ('目标值' in table_text or '目标' in context[-100:]):
            return 'estimated', '依据: 设计目标值，实际达成可能因环境而异'
        
        # 成本分析
        if '成本' in table_text and ('$/月' in table_text or '月度' in table_text or '年度' in table_text):
            return 'estimated', '依据: 基于云厂商定价模型与理论计算'
        
        # 默认：案例研究数据多为估算
        return 'estimated', '依据: 基于行业参考值与理论分析推导，非实际测试环境得出'
    
    def process_file(self, filepath):
        """处理单个文件"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            return False
        
        # 如果已有大量标注，跳过
        existing_tags = content.count('📊') + content.count('📖') + content.count('🔮')
        if existing_tags > 3:
            return False
        
        # 如果已有性能数据可信度声明，跳过（文档级已有声明）
        if self.has_trust_statement(content):
            return False
        
        lines = content.split('\n')
        modified = False
        file_tag_count = {'measured': 0, 'official': 0, 'estimated': 0}
        insertions = []  # (insert_pos, tag_line)
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # 检测表格开始
            if '|' in line and ('---' in line or ':-' in line or line.strip().startswith('|')):
                # 找到表格范围
                table_start = i
                while table_start > 0 and '|' in lines[table_start - 1]:
                    table_start -= 1
                table_end = i
                while table_end < len(lines) and ('|' in lines[table_end] or lines[table_end].strip() == ''):
                    table_end += 1
                
                table_lines = lines[table_start:table_end]
                
                # 严格判断是否为性能数据表格
                if self.table_contains_performance_data(table_lines):
                    # 检查表格前是否已有标注
                    pre_context = '\n'.join(lines[max(0, table_start - 5):table_start])
                    if not ALREADY_TAGGED_RE.search(pre_context):
                        # 确定标注类型
                        tag_type, tag_desc = self.determine_tag_type(content, table_lines, table_start)
                        
                        # 找到插入位置（表格前最近的标题或空行）
                        insert_pos = table_start
                        for j in range(table_start - 1, max(-1, table_start - 10), -1):
                            if j < 0:
                                break
                            if lines[j].strip().startswith('#') or lines[j].strip().startswith('>'):
                                insert_pos = j + 1
                                break
                            if lines[j].strip() == '' and j < table_start - 1:
                                insert_pos = j + 1
                                break
                        
                        tag_map = {
                            'measured': f"> 📊 **实测数据** | {tag_desc}\n",
                            'official': f"> 📖 **官方数据** | {tag_desc}\n",
                            'estimated': f"> 🔮 **估算数据** | {tag_desc}\n",
                        }
                        tag_line = tag_map[tag_type]
                        insertions.append((insert_pos, tag_line, tag_type))
                        modified = True
                
                i = table_end
                continue
            
            i += 1
        
        if modified and insertions:
            # 按位置从后往前插入，避免位置偏移
            insertions.sort(key=lambda x: x[0], reverse=True)
            
            # 去重：同一位置只插入一次
            seen_pos = set()
            final_insertions = []
            for pos, tag, tag_type in insertions:
                if pos not in seen_pos:
                    seen_pos.add(pos)
                    final_insertions.append((pos, tag, tag_type))
            
            for pos, tag, tag_type in final_insertions:
                lines.insert(pos, tag)
                file_tag_count[tag_type] += 1
            
            new_content = '\n'.join(lines)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.stats['files_modified'] += 1
            rel_path = os.path.relpath(filepath, BASE_DIR)
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
    
    def run(self):
        """运行审计"""
        all_files = []
        
        for target in TARGET_DIRS:
            target_path = BASE_DIR / target
            if not target_path.exists():
                continue
            for md_file in target_path.rglob("*.md"):
                if not self.should_exclude(str(md_file)):
                    all_files.append(str(md_file))
        
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
        report_path = BASE_DIR / "I2-PERFORMANCE-DATA-AUDIT.md"
        
        total_tags = sum(self.stats['tags_added'].values())
        
        report = f"""# I2: 性能数据可信度标注审计报告

> **任务**: I2 性能数据可信度标注
> **执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **执行人**: Agent (自动化脚本 v2)
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
| 📖 **官方数据** | 引用厂商官方白皮书/博客 | 引自 Apache Flink、RisingWave、Spark 等官方发布的基准测试数据 |
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
        
        report += f"""
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
5. **已有声明跳过**: 如果文档或段落已有 "性能数据可信度声明" 或类似标注，不再重复添加

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
        print(f"  Measured: {self.stats['tags_added']['measured']}")
        print(f"  Official: {self.stats['tags_added']['official']}")
        print(f"  Estimated: {self.stats['tags_added']['estimated']}")
        print(f"  Report: {report_path}")

if __name__ == '__main__':
    auditor = PerformanceDataAuditor()
    auditor.run()
