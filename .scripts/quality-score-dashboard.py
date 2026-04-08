#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quality Score Dashboard - v4.1
生成交互式质量仪表板HTML

作者: Q1-4 Quality Audit Task
日期: 2026-04-08
"""

import json
import os
from pathlib import Path
from datetime import datetime


class QualityDashboardGenerator:
    """质量仪表板生成器"""
    
    def __init__(self, audit_data_path: str):
        self.audit_data_path = Path(audit_data_path)
        self.report = None
        self.details = None
        
    def load_data(self):
        """加载审计数据"""
        report_path = self.audit_data_path / 'audit-report-v4.1.json'
        details_path = self.audit_data_path / 'audit-details-v4.1.json'
        
        if report_path.exists():
            with open(report_path, 'r', encoding='utf-8') as f:
                self.report = json.load(f)
        
        if details_path.exists():
            with open(details_path, 'r', encoding='utf-8') as f:
                self.details = json.load(f)
    
    def generate_html(self) -> str:
        """生成HTML仪表板"""
        if not self.report:
            return "<html><body><h1>无可用数据</h1></body></html>"
        
        summary = self.report.get('summary', {})
        score_dist = self.report.get('score_distribution', {})
        doc_breakdown = self.report.get('document_breakdown', {})
        theorem_cont = self.report.get('theorem_continuity', {})
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文档质量审计仪表板 v4.1</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --primary: #2563eb;
            --success: #16a34a;
            --warning: #ca8a04;
            --danger: #dc2626;
            --info: #0891b2;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
            color: white;
            padding: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        
        .header .subtitle {{
            opacity: 0.9;
            font-size: 0.95rem;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border: 1px solid var(--border);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .card-title {{
            font-size: 0.875rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}
        
        .card-value {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }}
        
        .card-delta {{
            font-size: 0.875rem;
            color: var(--text-muted);
        }}
        
        .card-value.excellent {{ color: var(--success); }}
        .card-value.good {{ color: var(--info); }}
        .card-value.warning {{ color: var(--warning); }}
        .card-value.danger {{ color: var(--danger); }}
        
        .section {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border: 1px solid var(--border);
        }}
        
        .section-title {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--border);
        }}
        
        .chart-container {{
            position: relative;
            height: 300px;
            margin: 1rem 0;
        }}
        
        .chart-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 1.5rem;
        }}
        
        .progress-bar {{
            background: var(--border);
            border-radius: 9999px;
            height: 8px;
            overflow: hidden;
            margin-top: 0.5rem;
        }}
        
        .progress-fill {{
            height: 100%;
            border-radius: 9999px;
            transition: width 0.5s ease;
        }}
        
        .progress-fill.excellent {{ background: var(--success); }}
        .progress-fill.good {{ background: var(--info); }}
        .progress-fill.warning {{ background: var(--warning); }}
        .progress-fill.danger {{ background: var(--danger); }}
        
        .metric-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--border);
        }}
        
        .metric-row:last-child {{
            border-bottom: none;
        }}
        
        .badge {{
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        
        .badge-success {{ background: #dcfce7; color: #166534; }}
        .badge-warning {{ background: #fef9c3; color: #854d0e; }}
        .badge-danger {{ background: #fee2e2; color: #991b1b; }}
        .badge-info {{ background: #cffafe; color: #155e75; }}
        
        .score-dimension {{
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem;
            background: var(--bg);
            border-radius: 8px;
            margin-bottom: 0.75rem;
        }}
        
        .dimension-icon {{
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }}
        
        .dimension-info {{
            flex: 1;
        }}
        
        .dimension-name {{
            font-weight: 600;
            margin-bottom: 0.25rem;
        }}
        
        .dimension-weight {{
            font-size: 0.75rem;
            color: var(--text-muted);
        }}
        
        .dimension-score {{
            font-size: 1.5rem;
            font-weight: 700;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.875rem;
        }}
        
        th, td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        
        th {{
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }}
        
        tr:hover {{
            background: var(--bg);
        }}
        
        .footer {{
            text-align: center;
            padding: 2rem;
            color: var(--text-muted);
            font-size: 0.875rem;
        }}
        
        @media (max-width: 768px) {{
            .chart-row {{
                grid-template-columns: 1fr;
            }}
            
            .card-value {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 文档质量审计仪表板 v4.1</h1>
        <div class="subtitle">分析 {self.report.get('total_documents', 0)} 篇文档 · 生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
    </div>
    
    <div class="container">
        <!-- 核心指标卡片 -->
        <div class="grid">
            <div class="card">
                <div class="card-title">平均质量分数</div>
                <div class="card-value {self._get_score_class(summary.get('average_score', 0))}">{summary.get('average_score', 0)}</div>
                <div class="card-delta">满分 100 分</div>
            </div>
            
            <div class="card">
                <div class="card-title">文档总数</div>
                <div class="card-value good">{self.report.get('total_documents', 0)}</div>
                <div class="card-delta">已全面审计</div>
            </div>
            
            <div class="card">
                <div class="card-title">发现问题总数</div>
                <div class="card-value {self._get_issue_class(summary.get('total_issues', 0))}">{summary.get('total_issues', 0)}</div>
                <div class="card-delta">严重: {summary.get('critical_issues', 0)} | 高: {summary.get('high_issues', 0)}</div>
            </div>
            
            <div class="card">
                <div class="card-title">定理/定义总数</div>
                <div class="card-value info">{summary.get('total_theorems', 0) + summary.get('total_definitions', 0)}</div>
                <div class="card-delta">定理: {summary.get('total_theorems', 0)} | 定义: {summary.get('total_definitions', 0)}</div>
            </div>
        </div>
        
        <!-- 评分维度详情 -->
        <div class="section">
            <h2 class="section-title">📐 评分维度权重</h2>
            <div class="score-dimension">
                <div class="dimension-icon" style="background: #dbeafe;">📝</div>
                <div class="dimension-info">
                    <div class="dimension-name">六段式结构</div>
                    <div class="dimension-weight">权重 25% - 概念定义、属性推导、关系建立、论证过程、形式证明、实例验证</div>
                </div>
                <div class="dimension-score">25%</div>
            </div>
            <div class="score-dimension">
                <div class="dimension-icon" style="background: #dcfce7;">🔢</div>
                <div class="dimension-info">
                    <div class="dimension-name">形式化元素</div>
                    <div class="dimension-weight">权重 25% - 定理(Thm)、引理(Lemma)、定义(Def)、命题(Prop)、推论(Cor)</div>
                </div>
                <div class="dimension-score">25%</div>
            </div>
            <div class="score-dimension">
                <div class="dimension-icon" style="background: #fef9c3;">📈</div>
                <div class="dimension-info">
                    <div class="dimension-name">可视化图表</div>
                    <div class="dimension-weight">权重 15% - Mermaid流程图、状态图、类图、甘特图等</div>
                </div>
                <div class="dimension-score">15%</div>
            </div>
            <div class="score-dimension">
                <div class="dimension-icon" style="background: #fce7f3;">📚</div>
                <div class="dimension-info">
                    <div class="dimension-name">引用完整性</div>
                    <div class="dimension-weight">权重 15% - 外部引用、交叉引用、参考文献</div>
                </div>
                <div class="dimension-score">15%</div>
            </div>
            <div class="score-dimension">
                <div class="dimension-icon" style="background: #f3e8ff;">💻</div>
                <div class="dimension-info">
                    <div class="dimension-name">代码示例</div>
                    <div class="dimension-weight">权重 20% - 代码块、内联代码、配置示例</div>
                </div>
                <div class="dimension-score">20%</div>
            </div>
        </div>
        
        <!-- 图表区域 -->
        <div class="chart-row">
            <div class="section">
                <h2 class="section-title">📊 质量分数分布</h2>
                <div class="chart-container">
                    <canvas id="scoreDistChart"></canvas>
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">🎯 问题严重性分布</h2>
                <div class="chart-container">
                    <canvas id="issueChart"></canvas>
                </div>
            </div>
        </div>
        
        <!-- 文档类型分析 -->
        <div class="section">
            <h2 class="section-title">📁 文档类型分析</h2>
            <table>
                <thead>
                    <tr>
                        <th>类型</th>
                        <th>文档数量</th>
                        <th>平均分数</th>
                        <th>问题总数</th>
                        <th>质量评级</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_breakdown_rows(doc_breakdown)}
                </tbody>
            </table>
        </div>
        
        <!-- 定理连续性 -->
        <div class="section">
            <h2 class="section-title">🔗 定理编号连续性检查</h2>
            <div class="metric-row">
                <span>定理总数</span>
                <span class="badge badge-info">{theorem_cont.get('theorem_count', 0)}</span>
            </div>
            <div class="metric-row">
                <span>断号数量</span>
                <span class="badge {'badge-danger' if theorem_cont.get('gap_count', 0) > 0 else 'badge-success'}">{theorem_cont.get('gap_count', 0)}</span>
            </div>
            {self._generate_gap_list(theorem_cont.get('gaps_found', []))}
        </div>
        
        <!-- 资源统计 -->
        <div class="section">
            <h2 class="section-title">📦 资源统计</h2>
            <div class="grid" style="margin-bottom: 0;">
                <div class="card">
                    <div class="card-title">Mermaid 图表</div>
                    <div class="card-value good">{summary.get('total_mermaid_charts', 0)}</div>
                </div>
                <div class="card">
                    <div class="card-title">代码块</div>
                    <div class="card-value info">{summary.get('total_code_blocks', 0)}</div>
                </div>
                <div class="card">
                    <div class="card-title">表格</div>
                    <div class="card-value warning">{summary.get('total_tables', 0)}</div>
                </div>
            </div>
        </div>
        
        <!-- 顶部问题 -->
        <div class="section">
            <h2 class="section-title">⚠️ 重点问题 (前20个)</h2>
            {self._generate_top_issues()}
        </div>
    </div>
    
    <div class="footer">
        <p>由 Document Quality Auditor v4.1 生成 · AnalysisDataFlow Project</p>
        <p>审计时间: {self.report.get('audit_date', datetime.now().isoformat())}</p>
    </div>
    
    <script>
        // 分数分布图表
        const scoreCtx = document.getElementById('scoreDistChart').getContext('2d');
        new Chart(scoreCtx, {{
            type: 'doughnut',
            data: {{
                labels: {list(score_dist.keys())},
                datasets: [{{
                    data: {list(score_dist.values())},
                    backgroundColor: [
                        '#16a34a',  // excellent
                        '#0891b2',  // good
                        '#ca8a04',  // acceptable
                        '#ea580c',  // needs_improvement
                        '#dc2626'   // poor
                    ],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'right'
                    }}
                }}
            }}
        }});
        
        // 问题分布图表
        const issueCtx = document.getElementById('issueChart').getContext('2d');
        new Chart(issueCtx, {{
            type: 'bar',
            data: {{
                labels: ['严重', '高', '中', '低'],
                datasets: [{{
                    label: '问题数量',
                    data: [
                        {summary.get('critical_issues', 0)},
                        {summary.get('high_issues', 0)},
                        {summary.get('medium_issues', 0)},
                        {summary.get('low_issues', 0)}
                    ],
                    backgroundColor: [
                        '#dc2626',
                        '#ea580c',
                        '#ca8a04',
                        '#0891b2'
                    ],
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
'''
        return html
    
    def _get_score_class(self, score: float) -> str:
        """获取分数对应的CSS类"""
        if score >= 90:
            return 'excellent'
        elif score >= 80:
            return 'good'
        elif score >= 70:
            return 'warning'
        else:
            return 'danger'
    
    def _get_issue_class(self, count: int) -> str:
        """获取问题数量对应的CSS类"""
        if count == 0:
            return 'excellent'
        elif count < 50:
            return 'warning'
        else:
            return 'danger'
    
    def _generate_breakdown_rows(self, breakdown: dict) -> str:
        """生成文档类型分析行"""
        rows = []
        type_names = {
            'Struct': '📐 形式理论',
            'Knowledge': '📚 知识结构',
            'Flink': '⚡ Flink专项',
            'Root': '📄 根文档'
        }
        
        for doc_type, info in breakdown.items():
            score = info.get('avg_score', 0)
            score_class = self._get_score_class(score)
            rating = 'A+' if score >= 90 else 'A' if score >= 80 else 'B' if score >= 70 else 'C' if score >= 60 else 'D'
            
            rows.append(f'''
                <tr>
                    <td>{type_names.get(doc_type, doc_type)}</td>
                    <td>{info.get('count', 0)}</td>
                    <td><span class="badge badge-{score_class}">{score}</span></td>
                    <td>{info.get('total_issues', 0)}</td>
                    <td><span class="badge badge-{score_class}">{rating}</span></td>
                </tr>
            ''')
        
        return '\n'.join(rows) if rows else '<tr><td colspan="5">无数据</td></tr>'
    
    def _generate_gap_list(self, gaps: list) -> str:
        """生成断号列表"""
        if not gaps:
            return '<div class="metric-row"><span>✅ 无断号</span></div>'
        
        html = '<div style="margin-top: 1rem;"><strong>断号列表:</strong><div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem;">'
        for gap in gaps[:20]:  # 只显示前20个
            html += f'<span class="badge badge-warning">{gap}</span>'
        if len(gaps) > 20:
            html += f'<span class="badge">...还有 {len(gaps) - 20} 个</span>'
        html += '</div></div>'
        return html
    
    def _generate_top_issues(self) -> str:
        """生成顶部问题列表"""
        if not self.details:
            return '<p>无详细数据</p>'
        
        # 收集所有问题
        all_issues = []
        for doc in self.details[:50]:  # 限制处理文档数
            for issue in doc.get('issues', [])[:5]:  # 每篇文档最多5个问题
                all_issues.append({
                    'file': doc.get('relative_path', 'unknown'),
                    'category': issue.get('category', ''),
                    'severity': issue.get('severity', ''),
                    'message': issue.get('message', '')
                })
        
        if not all_issues:
            return '<p>✅ 未发现质量问题</p>'
        
        # 按严重性排序
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        all_issues.sort(key=lambda x: severity_order.get(x['severity'], 4))
        
        html = '<table><thead><tr><th>文件</th><th>类别</th><th>级别</th><th>问题</th></tr></thead><tbody>'
        
        for issue in all_issues[:20]:
            severity_class = {
                'critical': 'badge-danger',
                'high': 'badge-warning',
                'medium': 'badge-info',
                'low': 'badge-success'
            }.get(issue['severity'], 'badge-info')
            
            html += f'''
                <tr>
                    <td>{issue['file'][:50]}</td>
                    <td>{issue['category']}</td>
                    <td><span class="badge {severity_class}">{issue['severity']}</span></td>
                    <td>{issue['message'][:80]}</td>
                </tr>
            '''
        
        html += '</tbody></table>'
        return html
    
    def save_dashboard(self, output_path: str):
        """保存仪表板"""
        self.load_data()
        html = self.generate_html()
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ 质量仪表板已生成: {output_file}")


def main():
    """主函数"""
    project_root = Path(__file__).parent.parent
    audit_data_path = project_root / '.scripts' / 'audit-results'
    output_path = project_root / '.scripts' / 'quality-dashboard-v4.1.html'
    
    generator = QualityDashboardGenerator(str(audit_data_path))
    generator.save_dashboard(str(output_path))


if __name__ == '__main__':
    main()
