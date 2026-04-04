#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 文档统计更新脚本

功能：
1. 文档统计 - 各目录文档数量、总文档数、总字节数、代码示例数量
2. 形式化元素统计 - 定理、定义、引理、命题、推论数量
3. 图表统计 - Mermaid图表、图片、表格数量
4. 交叉引用统计 - 内部链接、外部链接、锚点引用数量
5. 自动更新 - README.md、PROJECT-TRACKING.md、统计报告JSON
6. 输出格式 - Markdown表格、JSON机器可读、变更对比

作者: AnalysisDataFlow Automation
版本: 1.0.0
日期: 2026-04-04
"""

import os
import re
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field, asdict


@dataclass
class DirectoryStats:
    """目录统计信息"""
    name: str
    path: str
    file_count: int = 0
    size_bytes: int = 0
    lines: int = 0
    theorems: int = 0
    definitions: int = 0
    lemmas: int = 0
    propositions: int = 0
    corollaries: int = 0
    code_examples: int = 0
    mermaid_charts: int = 0
    images: int = 0
    tables: int = 0
    internal_links: int = 0
    external_links: int = 0
    anchor_refs: int = 0
    
    @property
    def size_kb(self) -> float:
        return round(self.size_bytes / 1024, 2)
    
    @property
    def size_mb(self) -> float:
        return round(self.size_bytes / (1024 * 1024), 2)
    
    @property
    def formal_elements_total(self) -> int:
        return self.theorems + self.definitions + self.lemmas + self.propositions + self.corollaries


@dataclass
class ProjectStats:
    """项目整体统计信息"""
    timestamp: str
    version: str = "1.0.0"
    total_docs: int = 0
    total_size_bytes: int = 0
    total_lines: int = 0
    theorems: int = 0
    definitions: int = 0
    lemmas: int = 0
    propositions: int = 0
    corollaries: int = 0
    code_examples: int = 0
    mermaid_charts: int = 0
    images: int = 0
    tables: int = 0
    internal_links: int = 0
    external_links: int = 0
    anchor_refs: int = 0
    directories: Dict[str, DirectoryStats] = field(default_factory=dict)
    
    @property
    def total_size_mb(self) -> float:
        return round(self.total_size_bytes / (1024 * 1024), 2)
    
    @property
    def formal_elements_total(self) -> int:
        return self.theorems + self.definitions + self.lemmas + self.propositions + self.corollaries


class DocumentAnalyzer:
    """文档分析器"""
    
    # 正则表达式模式
    PATTERNS = {
        # 形式化元素
        'theorem': re.compile(r'\*\*[\s]*定理\s*\(?\s*Thm[^\n]*\)?\s*\*\*|^##?#?\s*.*定理.*|Thm-[SKF]-\d+-\d+', re.MULTILINE | re.IGNORECASE),
        'definition': re.compile(r'\*\*[\s]*定义\s*\(?\s*Def[^\n]*\)?\s*\*\*|^##?#?\s*.*定义.*|Def-[SKF]-\d+-\d+', re.MULTILINE | re.IGNORECASE),
        'lemma': re.compile(r'\*\*[\s]*引理\s*\(?\s*Lemma[^\n]*\)?\s*\*\*|^##?#?\s*.*引理.*|Lemma-[SKF]-\d+-\d+', re.MULTILINE | re.IGNORECASE),
        'proposition': re.compile(r'\*\*[\s]*命题\s*\(?\s*Prop[^\n]*\)?\s*\*\*|^##?#?\s*.*命题.*|Prop-[SKF]-\d+-\d+', re.MULTILINE | re.IGNORECASE),
        'corollary': re.compile(r'\*\*[\s]*推论\s*\(?\s*Cor[^\n]*\)?\s*\*\*|^##?#?\s*.*推论.*|Cor-[SKF]-\d+-\d+', re.MULTILINE | re.IGNORECASE),
        
        # 代码示例
        'code_block': re.compile(r'```[\w]*\n[\s\S]*?```', re.MULTILINE),
        'inline_code': re.compile(r'`[^`]+`', re.MULTILINE),
        
        # 图表
        'mermaid': re.compile(r'```mermaid[\s\S]*?```', re.MULTILINE),
        'image': re.compile(r'!\[([^\]]*)\]\(([^)]+)\)', re.MULTILINE),
        'table': re.compile(r'\|[^\n]+\|\n\|[-:\s|]+\|\n(?:\|[^\n]+\|\n?)+', re.MULTILINE),
        
        # 链接
        'internal_link': re.compile(r'\[([^\]]+)\]\(([^:)]+\.md[^)]*)\)', re.MULTILINE),
        'external_link': re.compile(r'\[([^\]]+)\]\((https?://[^)]+)\)', re.MULTILINE),
        'anchor_ref': re.compile(r'\[([^\]]+)\]\([^)]*#[^)]+\)', re.MULTILINE),
        
        # 文档编号
        'formal_element_id': re.compile(r'(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d+-\d+', re.MULTILINE),
    }
    
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        
    def analyze_file(self, file_path: Path) -> Dict[str, int]:
        """分析单个文件"""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
        except Exception as e:
            print(f"警告: 无法读取文件 {file_path}: {e}")
            return {}
        
        stats = {
            'size_bytes': file_path.stat().st_size,
            'lines': len(lines),
            'theorems': 0,
            'definitions': 0,
            'lemmas': 0,
            'propositions': 0,
            'corollaries': 0,
            'code_examples': 0,
            'mermaid_charts': 0,
            'images': 0,
            'tables': 0,
            'internal_links': 0,
            'external_links': 0,
            'anchor_refs': 0,
        }
        
        # 统计形式化元素（使用编号模式更精确）
        formal_ids = self.PATTERNS['formal_element_id'].findall(content)
        for match in formal_ids:
            # findall返回的是元组或字符串，取决于捕获组
            if isinstance(match, tuple):
                elem_type = match[0]
            else:
                elem_type = match
            elem_type_lower = elem_type.lower()
            if elem_type_lower == 'thm':
                stats['theorems'] += 1
            elif elem_type_lower == 'def':
                stats['definitions'] += 1
            elif elem_type_lower == 'lemma':
                stats['lemmas'] += 1
            elif elem_type_lower == 'prop':
                stats['propositions'] += 1
            elif elem_type_lower == 'cor':
                stats['corollaries'] += 1
        
        # 如果没有编号的形式化元素，尝试标题模式
        if stats['theorems'] == 0:
            stats['theorems'] = len(self.PATTERNS['theorem'].findall(content))
        if stats['definitions'] == 0:
            stats['definitions'] = len(self.PATTERNS['definition'].findall(content))
        if stats['lemmas'] == 0:
            stats['lemmas'] = len(self.PATTERNS['lemma'].findall(content))
        if stats['propositions'] == 0:
            stats['propositions'] = len(self.PATTERNS['proposition'].findall(content))
        if stats['corollaries'] == 0:
            stats['corollaries'] = len(self.PATTERNS['corollary'].findall(content))
        
        # 代码示例
        code_blocks = len(self.PATTERNS['code_block'].findall(content))
        stats['code_examples'] = code_blocks
        
        # Mermaid图表
        stats['mermaid_charts'] = len(self.PATTERNS['mermaid'].findall(content))
        
        # 图片
        stats['images'] = len(self.PATTERNS['image'].findall(content))
        
        # 表格
        tables = self.PATTERNS['table'].findall(content)
        stats['tables'] = len(tables)
        
        # 链接统计
        stats['internal_links'] = len(self.PATTERNS['internal_link'].findall(content))
        stats['external_links'] = len(self.PATTERNS['external_link'].findall(content))
        stats['anchor_refs'] = len(self.PATTERNS['anchor_ref'].findall(content))
        
        return stats
    
    def analyze_directory(self, dir_name: str, dir_path: Path) -> DirectoryStats:
        """分析整个目录"""
        stats = DirectoryStats(name=dir_name, path=str(dir_path))
        
        if not dir_path.exists():
            print(f"警告: 目录不存在 {dir_path}")
            return stats
        
        md_files = list(dir_path.rglob('*.md'))
        stats.file_count = len(md_files)
        
        for md_file in md_files:
            file_stats = self.analyze_file(md_file)
            if file_stats:
                stats.size_bytes += file_stats['size_bytes']
                stats.lines += file_stats['lines']
                stats.theorems += file_stats['theorems']
                stats.definitions += file_stats['definitions']
                stats.lemmas += file_stats['lemmas']
                stats.propositions += file_stats['propositions']
                stats.corollaries += file_stats['corollaries']
                stats.code_examples += file_stats['code_examples']
                stats.mermaid_charts += file_stats['mermaid_charts']
                stats.images += file_stats['images']
                stats.tables += file_stats['tables']
                stats.internal_links += file_stats['internal_links']
                stats.external_links += file_stats['external_links']
                stats.anchor_refs += file_stats['anchor_refs']
        
        return stats


class StatsUpdater:
    """统计更新器"""
    
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.analyzer = DocumentAnalyzer(root_dir)
        self.stats_dir = root_dir / '.stats'
        self.stats_dir.mkdir(exist_ok=True)
        
    def collect_stats(self) -> ProjectStats:
        """收集所有统计信息"""
        timestamp = datetime.now().isoformat()
        project_stats = ProjectStats(timestamp=timestamp)
        
        # 定义要统计的目录
        directories = {
            'struct': self.root_dir / 'Struct',
            'knowledge': self.root_dir / 'Knowledge',
            'flink': self.root_dir / 'Flink',
            'visuals': self.root_dir / 'visuals',
            'tutorials': self.root_dir / 'tutorials',
            'learning_paths': self.root_dir / 'LEARNING-PATHS',
        }
        
        for dir_name, dir_path in directories.items():
            print(f"分析目录: {dir_name}...")
            dir_stats = self.analyzer.analyze_directory(dir_name, dir_path)
            project_stats.directories[dir_name] = dir_stats
            
            # 累加到总计
            project_stats.total_docs += dir_stats.file_count
            project_stats.total_size_bytes += dir_stats.size_bytes
            project_stats.total_lines += dir_stats.lines
            project_stats.theorems += dir_stats.theorems
            project_stats.definitions += dir_stats.definitions
            project_stats.lemmas += dir_stats.lemmas
            project_stats.propositions += dir_stats.propositions
            project_stats.corollaries += dir_stats.corollaries
            project_stats.code_examples += dir_stats.code_examples
            project_stats.mermaid_charts += dir_stats.mermaid_charts
            project_stats.images += dir_stats.images
            project_stats.tables += dir_stats.tables
            project_stats.internal_links += dir_stats.internal_links
            project_stats.external_links += dir_stats.external_links
            project_stats.anchor_refs += dir_stats.anchor_refs
        
        return project_stats
    
    def save_stats_json(self, stats: ProjectStats) -> None:
        """保存统计信息到JSON"""
        stats_file = self.stats_dir / 'project-stats.json'
        
        # 构建JSON结构
        data = {
            'timestamp': stats.timestamp,
            'version': stats.version,
            'summary': {
                'total_docs': stats.total_docs,
                'total_size_mb': stats.total_size_mb,
                'total_lines': stats.total_lines,
                'formal_elements': {
                    'theorems': stats.theorems,
                    'definitions': stats.definitions,
                    'lemmas': stats.lemmas,
                    'propositions': stats.propositions,
                    'corollaries': stats.corollaries,
                    'total': stats.formal_elements_total
                },
                'code_examples': stats.code_examples,
                'mermaid_charts': stats.mermaid_charts,
                'images': stats.images,
                'tables': stats.tables,
                'links': {
                    'internal': stats.internal_links,
                    'external': stats.external_links,
                    'anchors': stats.anchor_refs
                }
            },
            'directories': {}
        }
        
        for name, dir_stats in stats.directories.items():
            data['directories'][name] = {
                'path': str(dir_stats.path),
                'file_count': dir_stats.file_count,
                'size_kb': dir_stats.size_kb,
                'lines': dir_stats.lines,
                'formal_elements': {
                    'theorems': dir_stats.theorems,
                    'definitions': dir_stats.definitions,
                    'lemmas': dir_stats.lemmas,
                    'propositions': dir_stats.propositions,
                    'corollaries': dir_stats.corollaries,
                    'total': dir_stats.formal_elements_total
                },
                'code_examples': dir_stats.code_examples,
                'mermaid_charts': dir_stats.mermaid_charts,
                'images': dir_stats.images,
                'tables': dir_stats.tables,
                'links': {
                    'internal': dir_stats.internal_links,
                    'external': dir_stats.external_links,
                    'anchors': dir_stats.anchor_refs
                }
            }
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"统计JSON已保存: {stats_file}")
    
    def update_history(self, stats: ProjectStats) -> None:
        """更新历史记录"""
        history_file = self.stats_dir / 'stats-history.json'
        
        history = []
        if history_file.exists():
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except:
                history = []
        
        # 添加新记录
        history.append({
            'timestamp': stats.timestamp,
            'total_docs': stats.total_docs,
            'formal_elements': stats.formal_elements_total,
            'code_examples': stats.code_examples,
            'mermaid_charts': stats.mermaid_charts
        })
        
        # 只保留最近30条记录
        history = history[-30:]
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        
        print(f"历史记录已更新: {history_file}")
    
    def generate_markdown_report(self, stats: ProjectStats) -> str:
        """生成Markdown格式的统计报告"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        report = f"""# AnalysisDataFlow 项目统计报告

> **生成时间**: {date_str}  
> **统计版本**: v{stats.version}  
> **文档总数**: {stats.total_docs}篇  
> **项目大小**: {stats.total_size_mb} MB

---

## 📊 总体统计

### 文档规模

| 指标 | 数值 |
|------|------|
| 总文档数 | {stats.total_docs} 篇 |
| 总行数 | {stats.total_lines:,} 行 |
| 总大小 | {stats.total_size_mb} MB ({stats.total_size_bytes:,} 字节) |
| 代码示例 | {stats.code_examples} 个 |

### 形式化元素统计

| 类型 | 数量 | 占比 |
|------|------|------|
| 定理 (Thm) | {stats.theorems} | {self._calc_percent(stats.theorems, stats.formal_elements_total)}% |
| 定义 (Def) | {stats.definitions} | {self._calc_percent(stats.definitions, stats.formal_elements_total)}% |
| 引理 (Lemma) | {stats.lemmas} | {self._calc_percent(stats.lemmas, stats.formal_elements_total)}% |
| 命题 (Prop) | {stats.propositions} | {self._calc_percent(stats.propositions, stats.formal_elements_total)}% |
| 推论 (Cor) | {stats.corollaries} | {self._calc_percent(stats.corollaries, stats.formal_elements_total)}% |
| **总计** | **{stats.formal_elements_total}** | **100%** |

### 图表与可视化

| 类型 | 数量 |
|------|------|
| Mermaid图表 | {stats.mermaid_charts} 个 |
| 图片 | {stats.images} 个 |
| 表格 | {stats.tables} 个 |

### 交叉引用

| 类型 | 数量 |
|------|------|
| 内部链接 | {stats.internal_links} 个 |
| 外部链接 | {stats.external_links} 个 |
| 锚点引用 | {stats.anchor_refs} 个 |
| **链接总计** | **{stats.internal_links + stats.external_links + stats.anchor_refs}** 个 |

---

## 📁 各目录详细统计

"""
        
        # 各目录表格
        report += "| 目录 | 文档数 | 大小 | 行数 | 定理 | 定义 | 代码示例 | Mermaid |\n"
        report += "|------|--------|------|------|------|------|----------|---------|\n"
        
        for name, dir_stats in stats.directories.items():
            report += f"| {name}/ | {dir_stats.file_count} | {dir_stats.size_kb} KB | {dir_stats.lines:,} | "
            report += f"{dir_stats.theorems} | {dir_stats.definitions} | {dir_stats.code_examples} | {dir_stats.mermaid_charts} |\n"
        
        report += f"\n---\n\n## 📈 形式化元素分布\n\n```\n"
        
        # 生成ASCII图表
        max_val = max(stats.theorems, stats.definitions, stats.lemmas, 
                     stats.propositions, stats.corollaries, 1)
        
        elements = [
            ('定理', stats.theorems),
            ('定义', stats.definitions),
            ('引理', stats.lemmas),
            ('命题', stats.propositions),
            ('推论', stats.corollaries)
        ]
        
        for name, value in elements:
            bar_len = int((value / max_val) * 30)
            bar = '█' * bar_len
            report += f"{name:4} |{bar:<30}| {value}\n"
        
        report += "```\n\n---\n\n*报告由 update-stats.py 自动生成*\n"
        
        return report
    
    def _calc_percent(self, value: int, total: int) -> str:
        """计算百分比"""
        if total == 0:
            return "0.0"
        return f"{(value / total * 100):.1f}"
    
    def save_markdown_report(self, stats: ProjectStats) -> None:
        """保存Markdown报告"""
        report_file = self.stats_dir / 'STATISTICS-REPORT-GENERATED.md'
        report = self.generate_markdown_report(stats)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Markdown报告已保存: {report_file}")
    
    def update_readme(self, stats: ProjectStats) -> None:
        """更新README.md中的统计信息"""
        readme_file = self.root_dir / 'README.md'
        if not readme_file.exists():
            print(f"警告: README.md 不存在")
            return
        
        try:
            content = readme_file.read_text(encoding='utf-8')
            
            # 更新总文档数统计行
            old_pattern = r'\*\*总计: \d+ 篇技术文档.*?\*\*'
            new_text = f"**总计: {stats.total_docs} 篇技术文档 | {stats.formal_elements_total:,}+ 形式化元素 | {stats.mermaid_charts}+ Mermaid图表 | {stats.code_examples}+ 代码示例 | {stats.total_size_mb:.1f}+ MB**"
            content = re.sub(old_pattern, new_text, content)
            
            # 更新各目录文档数量
            for name, dir_stats in stats.directories.items():
                if name == 'struct':
                    pattern = r'(\| \*\*Struct/\*\* .*?\| )\d+文档'
                    content = re.sub(pattern, rf'\g<1>{dir_stats.file_count}文档', content)
                elif name == 'knowledge':
                    pattern = r'(\| \*\*Knowledge/\*\* .*?\| )\d+文档'
                    content = re.sub(pattern, rf'\g<1>{dir_stats.file_count}文档', content)
                elif name == 'flink':
                    pattern = r'(\| \*\*Flink/\*\* .*?\| )\d+文档'
                    content = re.sub(pattern, rf'\g<1>{dir_stats.file_count}文档', content)
            
            # 更新项目状态行
            old_status = r'\*\*总文档数\*\*: \d+ .*?\*\*大小\*\*: .*? MB'
            new_status = f"**总文档数**: {stats.total_docs} | **定理注册表版本**: v2.9 | **最后更新**: {datetime.now().strftime('%Y-%m-%d')} | **状态**: 持续演进 🚀 | **大小**: {stats.total_size_mb:.2f} MB"
            content = re.sub(old_status, new_status, content)
            
            # 更新形式化元素统计表
            content = self._update_formal_elements_table(content, stats)
            
            # 更新各目录进度表
            content = self._update_directory_progress(content, stats)
            
            readme_file.write_text(content, encoding='utf-8')
            print(f"README.md 已更新")
            
        except Exception as e:
            print(f"更新 README.md 时出错: {e}")
    
    def _update_formal_elements_table(self, content: str, stats: ProjectStats) -> str:
        """更新README中的形式化元素统计表"""
        # 匹配表格行并更新
        patterns = [
            (r'(\| 定理 \(Thm\) \| )\d+[,\d]*', stats.theorems),
            (r'(\| 定义 \(Def\) \| )\d+[,\d]*', stats.definitions),
            (r'(\| 引理 \(Lemma\) \| )\d+[,\d]*', stats.lemmas),
            (r'(\| 命题 \(Prop\) \| )\d+[,\d]*', stats.propositions),
            (r'(\| 推论 \(Cor\) \| )\d+[,\d]*', stats.corollaries),
        ]
        
        for pattern, value in patterns:
            content = re.sub(pattern, rf'\g<1>{value:,}', content)
        
        # 更新总计行
        total_pattern = r'(\| \*\*总计\*\* \| \*\*)\d+[,\d]*'
        content = re.sub(total_pattern, rf'\g<1>{stats.formal_elements_total:,}', content)
        
        return content
    
    def _update_directory_progress(self, content: str, stats: ProjectStats) -> str:
        """更新README中的目录进度表"""
        for name, dir_stats in stats.directories.items():
            dir_name = name.capitalize() if name != 'flink' else 'Flink'
            # 匹配形如: | Struct/ | [████] 100% | 43文档, 380定理, 835定义 |
            pattern = rf'(\| {re.escape(dir_name)}/ \| \[.*?\] \d+% \| )\d+文档'
            content = re.sub(pattern, rf'\g<1>{dir_stats.file_count}文档', content)
        
        return content
    
    def update_project_tracking(self, stats: ProjectStats) -> None:
        """更新PROJECT-TRACKING.md中的统计信息"""
        tracking_file = self.root_dir / 'PROJECT-TRACKING.md'
        if not tracking_file.exists():
            print(f"警告: PROJECT-TRACKING.md 不存在")
            return
        
        try:
            content = tracking_file.read_text(encoding='utf-8')
            date_str = datetime.now().strftime('%Y-%m-%d')
            
            # 更新头部统计行
            old_header = r'> \*\*最后更新\*\*: \d{4}-\d{2}-\d{2} .*?\*\*\d+篇文档.*?\| \d+\.\d+ MB\*\*'
            new_header = f'> **最后更新**: {date_str} | **总体进度**: **100%** | **状态**: 🎉 **项目完成** v3.2 | **{stats.total_docs}篇文档, {stats.formal_elements_total:,}形式化元素 | {stats.total_size_mb:.2f} MB**'
            content = re.sub(old_header, new_header, content)
            
            # 更新项目统计表
            for name, dir_stats in stats.directories.items():
                dir_cap = name.capitalize() if name != 'flink' else 'Flink'
                pattern = rf'(\| {re.escape(dir_cap)}/ \| )\d+( \| .*? \| )'
                content = re.sub(pattern, rf'\g<1>{dir_stats.file_count}\g<2>', content)
            
            # 更新总计行
            total_pattern = r'(\| \*\*总计\*\* \| \*\*)\d+(\*\* \| \*\*).*?(\*\* \| )'
            content = re.sub(total_pattern, rf'\g<1>{stats.total_docs}\g<2>{stats.total_size_mb:.2f}MB\g<3>', content)
            
            # 更新形式化指标表
            formal_patterns = [
                (r'(\| \*\*定理 \(Thm\)\*\* \| )\d+', stats.theorems),
                (r'(\| \*\*定义 \(Def\)\*\* \| )\d+', stats.definitions),
                (r'(\| \*\*引理 \(Lemma\)\*\* \| )\d+', stats.lemmas),
                (r'(\| \*\*命题 \(Prop\)\*\* \| )\d+', stats.propositions),
                (r'(\| \*\*推论 \(Cor\)\*\* \| )\d+', stats.corollaries),
            ]
            
            for pattern, value in formal_patterns:
                content = re.sub(pattern, rf'\g<1>{value:,}', content)
            
            # 更新总计
            total_formal_pattern = r'(\| \*\*总计\*\* \| \*\*)\d+(,\d+)*'
            content = re.sub(total_formal_pattern, rf'\g<1>{stats.formal_elements_total:,}', content)
            
            # 更新工程指标
            content = re.sub(r'(\*\*Mermaid 图表\*\*: )\d+', rf'\g<1>{stats.mermaid_charts}', content)
            content = re.sub(r'(\*\*代码示例\*\*: )\d+,\d+', rf'\g<1>{stats.code_examples:,}', content)
            content = re.sub(r'(\*\*交叉引用\*\*: )\d+,\d+', rf'\g<1>{stats.internal_links:,}', content)
            content = re.sub(r'(\*\*外部引用\*\*: )\d+', rf'\g<1>{stats.external_links}', content)
            
            tracking_file.write_text(content, encoding='utf-8')
            print(f"PROJECT-TRACKING.md 已更新")
            
        except Exception as e:
            print(f"更新 PROJECT-TRACKING.md 时出错: {e}")
    
    def generate_comparison(self, current: ProjectStats) -> str:
        """生成与上次统计的对比"""
        history_file = self.stats_dir / 'stats-history.json'
        
        if not history_file.exists():
            return "无历史数据可供对比"
        
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            if len(history) < 2:
                return "历史数据不足，无法对比"
            
            previous = history[-2]  # 上一次记录
            
            comparison = f"""
## 📊 变更对比

| 指标 | 上次统计 | 本次统计 | 变更 |
|------|----------|----------|------|
| 文档总数 | {previous.get('total_docs', 0)} | {current.total_docs} | {current.total_docs - previous.get('total_docs', 0):+d} |
| 形式化元素 | {previous.get('formal_elements', 0):,} | {current.formal_elements_total:,} | {current.formal_elements_total - previous.get('formal_elements', 0):+d} |
| 代码示例 | {previous.get('code_examples', 0):,} | {current.code_examples:,} | {current.code_examples - previous.get('code_examples', 0):+d} |
| Mermaid图表 | {previous.get('mermaid_charts', 0)} | {current.mermaid_charts} | {current.mermaid_charts - previous.get('mermaid_charts', 0):+d} |
"""
            return comparison
            
        except Exception as e:
            return f"生成对比时出错: {e}"
    
    def run(self) -> None:
        """运行完整的统计更新流程"""
        print("=" * 60)
        print("AnalysisDataFlow 文档统计更新")
        print("=" * 60)
        print()
        
        # 1. 收集统计
        print("📊 正在收集统计信息...")
        stats = self.collect_stats()
        print()
        
        # 2. 保存JSON
        print("💾 保存统计JSON...")
        self.save_stats_json(stats)
        print()
        
        # 3. 更新历史
        print("📈 更新历史记录...")
        self.update_history(stats)
        print()
        
        # 4. 生成Markdown报告
        print("📝 生成Markdown报告...")
        self.save_markdown_report(stats)
        print()
        
        # 5. 更新README
        print("📄 更新 README.md...")
        self.update_readme(stats)
        print()
        
        # 6. 更新PROJECT-TRACKING
        print("📋 更新 PROJECT-TRACKING.md...")
        self.update_project_tracking(stats)
        print()
        
        # 7. 打印摘要
        print("=" * 60)
        print("统计摘要")
        print("=" * 60)
        print(f"总文档数: {stats.total_docs}")
        print(f"总大小: {stats.total_size_mb:.2f} MB")
        print(f"总行数: {stats.total_lines:,}")
        print(f"形式化元素: {stats.formal_elements_total:,}")
        print(f"  - 定理: {stats.theorems}")
        print(f"  - 定义: {stats.definitions}")
        print(f"  - 引理: {stats.lemmas}")
        print(f"  - 命题: {stats.propositions}")
        print(f"  - 推论: {stats.corollaries}")
        print(f"代码示例: {stats.code_examples}")
        print(f"Mermaid图表: {stats.mermaid_charts}")
        print(f"图片: {stats.images}")
        print(f"表格: {stats.tables}")
        print(f"内部链接: {stats.internal_links}")
        print(f"外部链接: {stats.external_links}")
        print()
        print("各目录统计:")
        for name, dir_stats in stats.directories.items():
            print(f"  {name}/: {dir_stats.file_count}文档, {dir_stats.formal_elements_total}形式化元素")
        print()
        
        # 8. 打印对比
        comparison = self.generate_comparison(stats)
        print(comparison)
        
        print("=" * 60)
        print("✅ 统计更新完成!")
        print("=" * 60)


def main():
    """主函数"""
    # 确定项目根目录
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    # 创建并运行更新器
    updater = StatsUpdater(root_dir)
    updater.run()


if __name__ == '__main__':
    main()
