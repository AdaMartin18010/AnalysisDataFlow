#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社区反馈可视化仪表板 (Community Feedback Dashboard)

功能:
- 生成 HTML 可视化仪表板
- 反馈趋势图表
- 处理效率分析
- 社区活跃度展示

作者: AnalysisDataFlow Community
版本: 1.0.0
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import argparse


class DashboardGenerator:
    """仪表板 HTML 生成器"""
    
    def __init__(self, stats_file: str = ".stats/feedback-stats.json"):
        self.stats_file = Path(stats_file)
        self.stats = self._load_stats()
    
    def _load_stats(self) -> Dict:
        """加载统计数据"""
        if self.stats_file.exists():
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def generate_html(self) -> str:
        """生成完整 HTML 仪表板"""
        stats = self.stats
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AnalysisDataFlow 社区反馈仪表板</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --primary-color: #2563eb;
            --secondary-color: #64748b;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --bg-color: #f1f5f9;
            --card-bg: #ffffff;
            --text-color: #1e293b;
            --border-color: #e2e8f0;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, var(--primary-color), #1d4ed8);
            color: white;
            padding: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        
        .header h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        
        .header .subtitle {{
            opacity: 0.9;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .stat-card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        .stat-card .icon {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .stat-card .value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: var(--primary-color);
        }}
        
        .stat-card .label {{
            color: var(--secondary-color);
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .stat-card .change {{
            font-size: 0.875rem;
            margin-top: 0.5rem;
        }}
        
        .stat-card .change.positive {{
            color: var(--success-color);
        }}
        
        .stat-card .change.negative {{
            color: var(--danger-color);
        }}
        
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .chart-card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}
        
        .chart-card h3 {{
            font-size: 1.125rem;
            margin-bottom: 1rem;
            color: var(--text-color);
        }}
        
        .chart-container {{
            position: relative;
            height: 300px;
        }}
        
        .priority-legend {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }}
        
        .priority-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
        }}
        
        .priority-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }}
        
        .priority-dot.p0 {{ background: var(--danger-color); }}
        .priority-dot.p1 {{ background: #f97316; }}
        .priority-dot.p2 {{ background: var(--warning-color); }}
        .priority-dot.p3 {{ background: var(--success-color); }}
        
        .table-container {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th, td {{
            text-align: left;
            padding: 0.75rem;
            border-bottom: 1px solid var(--border-color);
        }}
        
        th {{
            font-weight: 600;
            color: var(--secondary-color);
            font-size: 0.875rem;
            text-transform: uppercase;
        }}
        
        tr:hover {{
            background: var(--bg-color);
        }}
        
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        
        .badge-p0 {{ background: #fee2e2; color: #991b1b; }}
        .badge-p1 {{ background: #ffedd5; color: #9a3412; }}
        .badge-p2 {{ background: #fef3c7; color: #92400e; }}
        .badge-p3 {{ background: #d1fae5; color: #065f46; }}
        .badge-bug {{ background: #fee2e2; color: #991b1b; }}
        .badge-enhancement {{ background: #dbeafe; color: #1e40af; }}
        .badge-documentation {{ background: #e0e7ff; color: #3730a3; }}
        .badge-new-topic {{ background: #f3e8ff; color: #6b21a8; }}
        
        .footer {{
            text-align: center;
            padding: 2rem;
            color: var(--secondary-color);
            font-size: 0.875rem;
        }}
        
        @media (max-width: 768px) {{
            .chart-grid {{
                grid-template-columns: 1fr;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <h1>📊 社区反馈仪表板</h1>
        <p class="subtitle">AnalysisDataFlow 项目社区活动实时概览</p>
    </header>
    
    <main class="container">
        <!-- 关键指标卡片 -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="icon">📋</div>
                <div class="value">{stats.get('total_issues', 0)}</div>
                <div class="label">总反馈数</div>
                <div class="change positive">↑ 社区活跃</div>
            </div>
            <div class="stat-card">
                <div class="icon">📂</div>
                <div class="value">{stats.get('open_issues', 0)}</div>
                <div class="label">待处理</div>
                <div class="change">持续跟进中</div>
            </div>
            <div class="stat-card">
                <div class="icon">✅</div>
                <div class="value">{stats.get('closed_issues', 0)}</div>
                <div class="label">已解决</div>
                <div class="change positive">{stats.get('closed_issues', 0) / stats.get('total_issues', 1) * 100:.1f}% 解决率</div>
            </div>
            <div class="stat-card">
                <div class="icon">⏱️</div>
                <div class="value">{stats.get('avg_resolution_days', 0):.1f}</div>
                <div class="label">平均解决天数</div>
                <div class="change">目标: < 7 天</div>
            </div>
        </div>
        
        <!-- 图表区域 -->
        <div class="chart-grid">
            <div class="chart-card">
                <h3>📈 反馈趋势 (最近12个月)</h3>
                <div class="chart-container">
                    <canvas id="trendChart"></canvas>
                </div>
            </div>
            
            <div class="chart-card">
                <h3>🎯 优先级分布</h3>
                <div class="priority-legend">
                    <div class="priority-item">
                        <div class="priority-dot p0"></div>
                        <span>P0 关键</span>
                    </div>
                    <div class="priority-item">
                        <div class="priority-dot p1"></div>
                        <span>P1 重要</span>
                    </div>
                    <div class="priority-item">
                        <div class="priority-dot p2"></div>
                        <span>P2 一般</span>
                    </div>
                    <div class="priority-item">
                        <div class="priority-dot p3"></div>
                        <span>P3 建议</span>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="priorityChart"></canvas>
                </div>
            </div>
            
            <div class="chart-card">
                <h3>🏷️ 反馈类型分布</h3>
                <div class="chart-container">
                    <canvas id="typeChart"></canvas>
                </div>
            </div>
            
            <div class="chart-card">
                <h3>📚 领域分布</h3>
                <div class="chart-container">
                    <canvas id="categoryChart"></canvas>
                </div>
            </div>
        </div>
        
        <!-- 高优先级任务表 -->
        <div class="table-container">
            <h3>🔴 高优先级待处理任务</h3>
            <table>
                <thead>
                    <tr>
                        <th>优先级</th>
                        <th>标题</th>
                        <th>类型</th>
                        <th>领域</th>
                        <th>创建时间</th>
                    </tr>
                </thead>
                <tbody id="highPriorityTable">
                    <tr>
                        <td colspan="5" style="text-align: center; color: var(--secondary-color);">
                            暂无高优先级任务，太棒了！🎉
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </main>
    
    <footer class="footer">
        <p>最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>AnalysisDataFlow Community | 数据由反馈聚合脚本自动生成</p>
    </footer>
    
    <script>
        // 趋势图数据
        const trendCtx = document.getElementById('trendChart').getContext('2d');
        const monthlyTrend = {json.dumps(stats.get('monthly_trend', {{}}))};
        const months = Object.keys(monthlyTrend).slice(-12);
        const counts = Object.values(monthlyTrend).slice(-12);
        
        new Chart(trendCtx, {{
            type: 'line',
            data: {{
                labels: months,
                datasets: [{{
                    label: '新反馈数',
                    data: counts,
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    tension: 0.4,
                    fill: true
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{ stepSize: 1 }}
                    }}
                }}
            }}
        }});
        
        // 优先级分布图
        const priorityCtx = document.getElementById('priorityChart').getContext('2d');
        const priorityData = {json.dumps(stats.get('by_priority', {{}}))};
        
        new Chart(priorityCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['P0 关键', 'P1 重要', 'P2 一般', 'P3 建议'],
                datasets: [{{
                    data: [
                        priorityData['P0'] || 0,
                        priorityData['P1'] || 0,
                        priorityData['P2'] || 0,
                        priorityData['P3'] || 0
                    ],
                    backgroundColor: ['#ef4444', '#f97316', '#f59e0b', '#10b981']
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false
            }}
        }});
        
        // 类型分布图
        const typeCtx = document.getElementById('typeChart').getContext('2d');
        const typeData = {json.dumps(stats.get('by_type', {{}}))};
        
        new Chart(typeCtx, {{
            type: 'bar',
            data: {{
                labels: Object.keys(typeData).map(t => {{
                    const map = {{'bug': '错误报告', 'enhancement': '功能建议', 
                                   'documentation': '文档改进', 'new-topic': '新主题'}};
                    return map[t] || t;
                }}),
                datasets: [{{
                    label: '数量',
                    data: Object.values(typeData),
                    backgroundColor: ['#ef4444', '#3b82f6', '#6366f1', '#a855f7']
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});
        
        // 领域分布图
        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        const categoryData = {json.dumps(stats.get('by_category', {{}}))};
        
        new Chart(categoryCtx, {{
            type: 'pie',
            data: {{
                labels: Object.keys(categoryData),
                datasets: [{{
                    data: Object.values(categoryData),
                    backgroundColor: ['#0ea5e9', '#8b5cf6', '#ec4899', '#6b7280']
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false
            }}
        }});
    </script>
</body>
</html>"""
        
        return html
    
    def save(self, output_path: str = "reports/feedback/dashboard.html"):
        """保存仪表板文件"""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        html = self.generate_html()
        with open(output, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"仪表板已生成: {output.absolute()}")
        return output


class DashboardServer:
    """本地仪表板服务器"""
    
    def __init__(self, html_path: str, port: int = 8080):
        self.html_path = Path(html_path)
        self.port = port
    
    def start(self):
        """启动服务器"""
        html_content = self.html_path.read_text(encoding='utf-8')
        
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            
            def log_message(self, format, *args):
                pass  # 禁用日志输出
        
        server = HTTPServer(('localhost', self.port), Handler)
        url = f"http://localhost:{self.port}"
        
        print(f"\n🚀 仪表板服务器已启动!")
        print(f"   访问地址: {url}")
        print(f"   按 Ctrl+C 停止服务器\n")
        
        # 自动打开浏览器
        webbrowser.open(url)
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 服务器已停止")


def main():
    parser = argparse.ArgumentParser(description="社区反馈可视化仪表板")
    parser.add_argument("--generate", action="store_true", help="生成仪表板 HTML 文件")
    parser.add_argument("--serve", action="store_true", help="启动本地服务器")
    parser.add_argument("--port", type=int, default=8080, help="服务器端口 (默认: 8080)")
    parser.add_argument("--output", default="reports/feedback/dashboard.html", help="输出路径")
    parser.add_argument("--stats", default=".stats/feedback-stats.json", help="统计数据文件")
    
    args = parser.parse_args()
    
    # 如果没有指定操作，默认生成并启动
    if not args.generate and not args.serve:
        args.generate = True
        args.serve = True
    
    # 生成仪表板
    if args.generate:
        generator = DashboardGenerator(stats_file=args.stats)
        output_path = generator.save(args.output)
        
        if not args.serve:
            print(f"\n仪表板文件已生成，请用浏览器打开:")
            print(f"   file://{output_path.absolute()}")
    
    # 启动服务器
    if args.serve:
        html_path = args.output if Path(args.output).exists() else "reports/feedback/dashboard.html"
        server = DashboardServer(html_path, port=args.port)
        server.start()


if __name__ == "__main__":
    main()
