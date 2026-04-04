#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成器 - 生成多种格式的链接检查报告

功能:
- 生成HTML报告 (美观的可视化界面)
- 生成Markdown报告 (适合GitHub/GitLab显示)
- 历史趋势分析
- 统计数据可视化

作者: AnalysisDataFlow 项目
版本: 1.0.0
"""

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import re


@dataclass
class TrendData:
    """趋势数据"""
    date: str
    total: int
    valid: int
    broken: int
    warnings: int


class ReportGenerator:
    """报告生成器"""

    def __init__(self, results_path: Path, history_dir: Optional[Path] = None):
        self.results_path = results_path
        self.history_dir = history_dir or Path("link-check-history")
        self.data = self._load_results()
        self.results = self.data.get('results', [])
        self.summary = self.data.get('summary', {})
        
    def _load_results(self) -> Dict:
        """加载检查结果"""
        with open(self.results_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _group_by_file(self) -> Dict[str, List[Dict]]:
        """按源文件分组结果"""
        grouped = defaultdict(list)
        for result in self.results:
            source_file = result.get('source_file', 'unknown')
            grouped[source_file].append(result)
        return dict(grouped)

    def _group_by_status(self) -> Dict[str, List[Dict]]:
        """按状态分组结果"""
        grouped = {
            'broken': [],
            'warning': [],
            'valid': [],
            'skipped': []
        }
        for result in self.results:
            if not result.get('is_valid'):
                grouped['broken'].append(result)
            elif result.get('error_message'):
                grouped['warning'].append(result)
            elif result.get('link_type') == 'skipped' or '排除' in result.get('error_message', ''):
                grouped['skipped'].append(result)
            else:
                grouped['valid'].append(result)
        return grouped

    def _group_by_domain(self) -> Dict[str, Dict[str, Any]]:
        """按域名统计"""
        domain_stats = defaultdict(lambda: {'total': 0, 'valid': 0, 'broken': 0})
        
        for result in self.results:
            url = result.get('url', '')
            if url.startswith(('http://', 'https://')):
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(url).netloc
                    domain_stats[domain]['total'] += 1
                    if result.get('is_valid'):
                        domain_stats[domain]['valid'] += 1
                    else:
                        domain_stats[domain]['broken'] += 1
                except:
                    pass
        
        return dict(domain_stats)

    def _calculate_trends(self, days: int = 30) -> List[TrendData]:
        """计算历史趋势"""
        trends = []
        
        if not self.history_dir.exists():
            return trends
        
        # 读取历史记录
        history_files = sorted(self.history_dir.glob('*.json'))
        
        for file_path in history_files[-days:]:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    summary = data.get('summary', {})
                    trends.append(TrendData(
                        date=file_path.stem,
                        total=summary.get('total_links', 0),
                        valid=summary.get('valid_links', 0),
                        broken=summary.get('broken_links', 0),
                        warnings=summary.get('warning_links', 0)
                    ))
            except:
                continue
        
        # 添加当前结果
        trends.append(TrendData(
            date=datetime.now().strftime('%Y-%m-%d'),
            total=self.summary.get('total_links', 0),
            valid=self.summary.get('valid_links', 0),
            broken=self.summary.get('broken_links', 0),
            warnings=self.summary.get('warning_links', 0)
        ))
        
        return trends

    def generate_html(self, output_path: Path) -> str:
        """生成HTML报告"""
        grouped = self._group_by_status()
        by_file = self._group_by_file()
        domain_stats = self._group_by_domain()
        trends = self._calculate_trends()
        
        # 计算统计数据
        total = self.summary.get('total_links', 0)
        valid = self.summary.get('valid_links', 0)
        broken = self.summary.get('broken_links', 0)
        warnings_count = self.summary.get('warning_links', 0)
        
        valid_pct = (valid / total * 100) if total > 0 else 0
        broken_pct = (broken / total * 100) if total > 0 else 0
        warning_pct = (warnings_count / total * 100) if total > 0 else 0
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>链接检查报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        :root {{
            --color-success: #28a745;
            --color-warning: #ffc107;
            --color-danger: #dc3545;
            --color-info: #17a2b8;
            --color-bg: #f8f9fa;
            --color-card: #ffffff;
            --color-text: #333333;
            --color-text-muted: #6c757d;
            --border-radius: 8px;
            --shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: var(--color-bg);
            color: var(--color-text);
            line-height: 1.6;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: var(--border-radius);
        }}
        
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .timestamp {{
            opacity: 0.9;
            font-size: 0.9em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: var(--color-card);
            padding: 20px;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            text-align: center;
        }}
        
        .stat-card.success {{
            border-top: 4px solid var(--color-success);
        }}
        
        .stat-card.warning {{
            border-top: 4px solid var(--color-warning);
        }}
        
        .stat-card.danger {{
            border-top: 4px solid var(--color-danger);
        }}
        
        .stat-card.info {{
            border-top: 4px solid var(--color-info);
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .stat-label {{
            color: var(--color-text-muted);
            font-size: 0.9em;
        }}
        
        .stat-percent {{
            font-size: 0.8em;
            opacity: 0.7;
        }}
        
        .section {{
            background: var(--color-card);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            margin-bottom: 30px;
            overflow: hidden;
        }}
        
        .section-header {{
            padding: 15px 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
            font-size: 1.2em;
            font-weight: 600;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .section-header .badge {{
            background: var(--color-danger);
            color: white;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 0.7em;
        }}
        
        .section-content {{
            padding: 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }}
        
        th {{
            background: #f8f9fa;
            font-weight: 600;
            position: sticky;
            top: 0;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.75em;
            font-weight: 600;
        }}
        
        .status-success {{
            background: #d4edda;
            color: #155724;
        }}
        
        .status-warning {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .status-danger {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .url-cell {{
            max-width: 400px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .file-cell {{
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .error-message {{
            color: var(--color-danger);
            font-size: 0.85em;
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .chart-container {{
            padding: 20px;
            height: 300px;
        }}
        
        .trend-chart {{
            display: flex;
            align-items: flex-end;
            justify-content: space-around;
            height: 100%;
            padding: 20px 0;
        }}
        
        .trend-bar {{
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
            margin: 0 5px;
        }}
        
        .bar-stack {{
            width: 100%;
            display: flex;
            flex-direction: column-reverse;
            border-radius: 4px;
            overflow: hidden;
            min-height: 10px;
        }}
        
        .bar-segment {{
            width: 100%;
            min-height: 2px;
        }}
        
        .bar-valid {{
            background: var(--color-success);
        }}
        
        .bar-broken {{
            background: var(--color-danger);
        }}
        
        .bar-warning {{
            background: var(--color-warning);
        }}
        
        .bar-label {{
            font-size: 0.7em;
            margin-top: 5px;
            transform: rotate(-45deg);
            white-space: nowrap;
        }}
        
        .domain-list {{
            max-height: 400px;
            overflow-y: auto;
        }}
        
        .filters {{
            padding: 15px 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .filters input {{
            padding: 8px 12px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 0.9em;
            width: 300px;
        }}
        
        footer {{
            text-align: center;
            padding: 20px;
            color: var(--color-text-muted);
            font-size: 0.85em;
        }}
        
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            table {{
                font-size: 0.85em;
            }}
            
            th, td {{
                padding: 8px 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔗 链接检查报告</h1>
            <div class="timestamp">生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</div>
            <div class="timestamp">检查文件数: {self.summary.get('total_files', 0)} | 总链接数: {total}</div>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card success">
                <div class="stat-label">有效链接</div>
                <div class="stat-value" style="color: var(--color-success);">{valid}</div>
                <div class="stat-percent">{valid_pct:.1f}%</div>
            </div>
            <div class="stat-card danger">
                <div class="stat-label">失效链接 ⚠️</div>
                <div class="stat-value" style="color: var(--color-danger);">{broken}</div>
                <div class="stat-percent">{broken_pct:.1f}%</div>
            </div>
            <div class="stat-card warning">
                <div class="stat-label">警告链接</div>
                <div class="stat-value" style="color: var(--color-warning);">{warnings_count}</div>
                <div class="stat-percent">{warning_pct:.1f}%</div>
            </div>
            <div class="stat-card info">
                <div class="stat-label">检查耗时</div>
                <div class="stat-value" style="color: var(--color-info); font-size: 1.8em;">{self.summary.get('check_duration', 0):.1f}s</div>
                <div class="stat-percent">完成于 {self.summary.get('completed_at', 'Unknown')[:19]}</div>
            </div>
        </div>
'''

        # 添加趋势图
        if trends:
            html += self._generate_trend_section(trends)

        # 添加失效链接详情
        if grouped['broken']:
            html += self._generate_broken_links_section(grouped['broken'])
        
        # 添加警告链接
        if grouped['warning']:
            html += self._generate_warning_links_section(grouped['warning'])
        
        # 添加域名统计
        if domain_stats:
            html += self._generate_domain_stats_section(domain_stats)
        
        # 添加按文件汇总
        html += self._generate_file_summary_section(by_file)

        html += '''
        <footer>
            <p>Generated by AnalysisDataFlow Link Checker v1.0.0</p>
        </footer>
    </div>
    
    <script>
        // 简单的表格过滤功能
        function filterTable(tableId, filterValue) {
            const table = document.getElementById(tableId);
            const rows = table.getElementsByTagName('tr');
            const lowerFilter = filterValue.toLowerCase();
            
            for (let i = 1; i < rows.length; i++) {
                const cells = rows[i].getElementsByTagName('td');
                let match = false;
                
                for (let j = 0; j < cells.length; j++) {
                    if (cells[j].textContent.toLowerCase().indexOf(lowerFilter) > -1) {
                        match = true;
                        break;
                    }
                }
                
                rows[i].style.display = match ? '' : 'none';
            }
        }
    </script>
</body>
</html>
'''
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return str(output_path)

    def _generate_trend_section(self, trends: List[TrendData]) -> str:
        """生成趋势图表部分"""
        max_val = max(t.total for t in trends) if trends else 1
        
        bars_html = ''
        for trend in trends:
            valid_height = (trend.valid / max_val * 100) if max_val > 0 else 0
            warning_height = (trend.warnings / max_val * 100) if max_val > 0 else 0
            broken_height = (trend.broken / max_val * 100) if max_val > 0 else 0
            
            bars_html += f'''
                <div class="trend-bar">
                    <div class="bar-stack" style="height: {valid_height + warning_height + broken_height}px;">
                        <div class="bar-segment bar-valid" style="height: {valid_height}px;"></div>
                        <div class="bar-segment bar-warning" style="height: {warning_height}px;"></div>
                        <div class="bar-segment bar-broken" style="height: {broken_height}px;"></div>
                    </div>
                    <div class="bar-label">{trend.date[-5:]}</div>
                </div>
            '''
        
        return f'''
        <div class="section">
            <div class="section-header">
                <span>📈 历史趋势 (最近30天)</span>
            </div>
            <div class="chart-container">
                <div class="trend-chart">
                    {bars_html}
                </div>
                <div style="text-align: center; margin-top: 10px;">
                    <span style="display: inline-block; margin: 0 10px;">
                        <span style="display: inline-block; width: 12px; height: 12px; background: var(--color-success); margin-right: 5px;"></span>有效
                    </span>
                    <span style="display: inline-block; margin: 0 10px;">
                        <span style="display: inline-block; width: 12px; height: 12px; background: var(--color-warning); margin-right: 5px;"></span>警告
                    </span>
                    <span style="display: inline-block; margin: 0 10px;">
                        <span style="display: inline-block; width: 12px; height: 12px; background: var(--color-danger); margin-right: 5px;"></span>失效
                    </span>
                </div>
            </div>
        </div>
        '''

    def _generate_broken_links_section(self, broken_links: List[Dict]) -> str:
        """生成失效链接详情部分"""
        rows = ''
        for link in broken_links:
            rows += f'''
                <tr>
                    <td class="url-cell" title="{link.get('url', '')}">{link.get('url', '')}</td>
                    <td class="file-cell" title="{link.get('source_file', '')}">{link.get('source_file', '')}</td>
                    <td>{link.get('line_number', 0)}</td>
                    <td><span class="status-badge status-danger">失效</span></td>
                    <td>{link.get('status_code', 'N/A')}</td>
                    <td class="error-message" title="{link.get('error_message', '')}">{link.get('error_message', '')}</td>
                </tr>
            '''
        
        return f'''
        <div class="section">
            <div class="section-header">
                <span>❌ 失效链接详情</span>
                <span class="badge">{len(broken_links)}</span>
            </div>
            <div class="filters">
                <input type="text" placeholder="🔍 过滤链接..." onkeyup="filterTable('broken-table', this.value)">
            </div>
            <div class="section-content">
                <table id="broken-table">
                    <thead>
                        <tr>
                            <th>URL</th>
                            <th>源文件</th>
                            <th>行号</th>
                            <th>状态</th>
                            <th>HTTP状态码</th>
                            <th>错误信息</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        </div>
        '''

    def _generate_warning_links_section(self, warning_links: List[Dict]) -> str:
        """生成警告链接部分"""
        rows = ''
        for link in warning_links[:50]:  # 限制显示数量
            rows += f'''
                <tr>
                    <td class="url-cell" title="{link.get('url', '')}">{link.get('url', '')}</td>
                    <td class="file-cell">{link.get('source_file', '')}</td>
                    <td>{link.get('line_number', 0)}</td>
                    <td><span class="status-badge status-warning">警告</span></td>
                    <td class="error-message">{link.get('error_message', '')}</td>
                </tr>
            '''
        
        if len(warning_links) > 50:
            rows += f'''
                <tr>
                    <td colspan="5" style="text-align: center; color: var(--color-text-muted);">
                        ... 还有 {len(warning_links) - 50} 个警告链接
                    </td>
                </tr>
            '''
        
        return f'''
        <div class="section">
            <div class="section-header">
                <span>⚠️ 警告链接</span>
                <span class="badge" style="background: var(--color-warning);">{len(warning_links)}</span>
            </div>
            <div class="section-content">
                <table>
                    <thead>
                        <tr>
                            <th>URL</th>
                            <th>源文件</th>
                            <th>行号</th>
                            <th>状态</th>
                            <th>警告信息</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        </div>
        '''

    def _generate_domain_stats_section(self, domain_stats: Dict[str, Dict]) -> str:
        """生成域名统计部分"""
        # 按总链接数排序
        sorted_domains = sorted(
            domain_stats.items(),
            key=lambda x: x[1]['total'],
            reverse=True
        )[:20]  # 只显示前20
        
        rows = ''
        for domain, stats in sorted_domains:
            valid_pct = (stats['valid'] / stats['total'] * 100) if stats['total'] > 0 else 0
            status_class = 'status-success' if stats['broken'] == 0 else 'status-danger'
            status_text = '正常' if stats['broken'] == 0 else f"{stats['broken']} 失效"
            
            rows += f'''
                <tr>
                    <td>{domain}</td>
                    <td>{stats['total']}</td>
                    <td>{stats['valid']}</td>
                    <td>{stats['broken']}</td>
                    <td>{valid_pct:.1f}%</td>
                    <td><span class="status-badge {status_class}">{status_text}</span></td>
                </tr>
            '''
        
        return f'''
        <div class="section">
            <div class="section-header">
                <span>🌐 域名统计 (Top 20)</span>
            </div>
            <div class="section-content domain-list">
                <table>
                    <thead>
                        <tr>
                            <th>域名</th>
                            <th>总链接</th>
                            <th>有效</th>
                            <th>失效</th>
                            <th>健康度</th>
                            <th>状态</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        </div>
        '''

    def _generate_file_summary_section(self, by_file: Dict[str, List[Dict]]) -> str:
        """生成文件汇总部分"""
        rows = ''
        for file_path, results in sorted(by_file.items()):
            total = len(results)
            broken = sum(1 for r in results if not r.get('is_valid'))
            valid = total - broken
            
            status = '✅ 正常' if broken == 0 else f'❌ {broken} 个失效'
            status_class = 'status-success' if broken == 0 else 'status-danger'
            
            rows += f'''
                <tr>
                    <td class="file-cell">{file_path}</td>
                    <td>{total}</td>
                    <td>{valid}</td>
                    <td>{broken}</td>
                    <td><span class="status-badge {status_class}">{status}</span></td>
                </tr>
            '''
        
        return f'''
        <div class="section">
            <div class="section-header">
                <span>📁 文件链接汇总</span>
            </div>
            <div class="section-content">
                <table>
                    <thead>
                        <tr>
                            <th>文件路径</th>
                            <th>总链接</th>
                            <th>有效</th>
                            <th>失效</th>
                            <th>状态</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        </div>
        '''

    def generate_markdown(self, output_path: Path) -> str:
        """生成Markdown报告"""
        grouped = self._group_by_status()
        total = self.summary.get('total_links', 0)
        valid = self.summary.get('valid_links', 0)
        broken = self.summary.get('broken_links', 0)
        warnings_count = self.summary.get('warning_links', 0)
        
        md = f'''# 🔗 链接检查报告

> 生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

## 📊 统计摘要

| 指标 | 数量 | 百分比 |
|------|------|--------|
| 检查文件数 | {self.summary.get('total_files', 0)} | - |
| 总链接数 | {total} | 100% |
| ✅ 有效链接 | {valid} | {(valid/total*100):.1f}% |
| ❌ 失效链接 | {broken} | {(broken/total*100):.1f}% |
| ⚠️ 警告链接 | {warnings_count} | {(warnings_count/total*100):.1f}% |
| 检查耗时 | {self.summary.get('check_duration', 0):.1f}s | - |

'''

        # 添加失效链接详情
        if grouped['broken']:
            md += '''## ❌ 失效链接详情

| URL | 源文件 | 行号 | 状态码 | 错误信息 |
|-----|--------|------|--------|----------|
'''
            for link in grouped['broken']:
                url = link.get('url', '')[:60] + '...' if len(link.get('url', '')) > 60 else link.get('url', '')
                file = link.get('source_file', '')[-40:] if len(link.get('source_file', '')) > 40 else link.get('source_file', '')
                md += f"| {url} | ...{file} | {link.get('line_number', 0)} | {link.get('status_code', 'N/A')} | {link.get('error_message', '')[:50]} |\n"
            
            md += '\n'
        
        # 添加警告链接
        if grouped['warning']:
            md += f'''## ⚠️ 警告链接 ({len(grouped['warning'])} 个)

<details>
<summary>点击查看详情</summary>

| URL | 源文件 | 行号 | 警告信息 |
|-----|--------|------|----------|
'''
            for link in grouped['warning'][:20]:  # 限制显示数量
                url = link.get('url', '')[:50] + '...' if len(link.get('url', '')) > 50 else link.get('url', '')
                md += f"| {url} | {link.get('source_file', '')} | {link.get('line_number', 0)} | {link.get('error_message', '')[:40]} |\n"
            
            if len(grouped['warning']) > 20:
                md += f"\n*... 还有 {len(grouped['warning']) - 20} 个警告链接*\n"
            
            md += '\n</details>\n\n'

        md += '''---

*Generated by AnalysisDataFlow Link Checker v1.0.0*
'''
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
        
        return str(output_path)

    def save_history(self):
        """保存当前结果到历史记录"""
        self.history_dir.mkdir(exist_ok=True)
        
        today = datetime.now().strftime('%Y-%m-%d')
        history_file = self.history_dir / f"{today}.json"
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        # 清理旧的历史记录 (保留90天)
        cutoff = datetime.now() - timedelta(days=90)
        for file_path in self.history_dir.glob('*.json'):
            try:
                file_date = datetime.strptime(file_path.stem, '%Y-%m-%d')
                if file_date < cutoff:
                    file_path.unlink()
            except:
                pass
        
        return str(history_file)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='生成链接检查报告',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--input', '-i', type=str, required=True,
                       help='输入JSON结果文件路径')
    parser.add_argument('--output-html', type=str,
                       help='输出HTML报告路径')
    parser.add_argument('--output-md', type=str,
                       help='输出Markdown报告路径')
    parser.add_argument('--save-history', action='store_true',
                       help='保存到历史记录')
    parser.add_argument('--history-dir', type=str, default='link-check-history',
                       help='历史记录目录')
    
    args = parser.parse_args()
    
    results_path = Path(args.input)
    if not results_path.exists():
        print(f"错误: 结果文件不存在: {results_path}")
        return 1
    
    history_dir = Path(args.history_dir) if args.history_dir else None
    generator = ReportGenerator(results_path, history_dir)
    
    # 保存历史记录
    if args.save_history:
        history_file = generator.save_history()
        print(f"历史记录已保存: {history_file}")
    
    # 生成HTML报告
    if args.output_html:
        html_path = generator.generate_html(Path(args.output_html))
        print(f"HTML报告已生成: {html_path}")
    
    # 生成Markdown报告
    if args.output_md:
        md_path = generator.generate_markdown(Path(args.output_md))
        print(f"Markdown报告已生成: {md_path}")
    
    # 如果没有指定输出，默认生成两种格式
    if not args.output_html and not args.output_md:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        html_path = generator.generate_html(Path(f'link-report-{timestamp}.html'))
        md_path = generator.generate_markdown(Path(f'link-report-{timestamp}.md'))
        print(f"默认报告已生成:")
        print(f"  HTML: {html_path}")
        print(f"  Markdown: {md_path}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
