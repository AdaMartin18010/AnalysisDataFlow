#!/usr/bin/env python3
"""
Theorem System Visualization Generator
=======================================
Generates visualizations for theorem numbering system analysis.

Version: 1.0.0
Date: 2026-04-12
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import Counter

# Color palette for charts
COLORS = {
    'Thm': '#FF6B6B',      # Red
    'Def': '#4ECDC4',      # Teal
    'Lemma': '#45B7D1',    # Blue
    'Prop': '#96CEB4',     # Green
    'Cor': '#FFEAA7',      # Yellow
    'S': '#6C5CE7',        # Purple
    'K': '#FD79A8',        # Pink
    'F': '#00B894',        # Green
    'R': '#E17055',        # Orange
    'A': '#74B9FF'         # Light Blue
}

STAGE_NAMES = {
    'S': 'Struct',
    'K': 'Knowledge',
    'F': 'Flink',
    'R': 'Rust',
    'A': 'AI',
    'C': 'Cross',
    'U': 'Unified'
}

TYPE_NAMES = {
    'Thm': 'Theorem',
    'Def': 'Definition',
    'Lemma': 'Lemma',
    'Prop': 'Proposition',
    'Cor': 'Corollary'
}

def generate_mermaid_pie_chart(data: dict, title: str):
    """Generate a Mermaid pie chart."""
    mermaid = f"""```mermaid
pie title {title}
"""
    for label, value in sorted(data.items(), key=lambda x: x[1], reverse=True):
        display_label = STAGE_NAMES.get(label, TYPE_NAMES.get(label, label))
        mermaid += f"    \"{display_label}\" : {value}\n"
    mermaid += "```\n"
    return mermaid

def generate_mermaid_bar_chart(data: dict, title: str, x_label: str = "Category", y_label: str = "Count"):
    """Generate a Mermaid XY chart (bar chart)."""
    mermaid = f"""```mermaid
xychart-beta
    title "{title}"
    x-axis [{', '.join(f'"{k}"' for k in data.keys())}]
    y-axis "{y_label}" 0 --> {max(data.values()) * 1.2:.0f}
    bar [{', '.join(str(v) for v in data.values())}]
```
"""
    return mermaid

def generate_distribution_heatmap(by_doc: dict) -> str:
    """Generate a markdown table showing distribution heatmap."""
    # Group by stage
    stage_docs = {}
    for doc_key, count in by_doc.items():
        stage = doc_key.split('-')[0]
        if stage not in stage_docs:
            stage_docs[stage] = {}
        stage_docs[stage][doc_key] = count
    
    table = "| Stage | Document | Count | Heat |\n"
    table += "|-------|----------|-------|------|\n"
    
    for stage in sorted(stage_docs.keys()):
        docs = stage_docs[stage]
        max_count = max(docs.values())
        for doc_key in sorted(docs.keys()):
            count = docs[doc_key]
            # Generate heat bar
            heat_level = int((count / max_count) * 10)
            heat = "█" * heat_level + "░" * (10 - heat_level)
            table += f"| {STAGE_NAMES.get(stage, stage)} | {doc_key} | {count} | {heat} |\n"
    
    return table

def generate_sunburst_data(by_type: dict, by_stage: dict, elements: list) -> str:
    """Generate sunburst diagram data (as JSON for external rendering)."""
    # Group by stage and type
    hierarchy = {}
    for elem in elements:
        stage = elem.get('stage', 'Unknown')
        elem_type = elem.get('type', 'Unknown')
        if stage not in hierarchy:
            hierarchy[stage] = {}
        if elem_type not in hierarchy[stage]:
            hierarchy[stage][elem_type] = 0
        hierarchy[stage][elem_type] += 1
    
    sunburst_data = {
        "name": "Theorem System",
        "children": []
    }
    
    for stage, types in hierarchy.items():
        stage_node = {
            "name": STAGE_NAMES.get(stage, stage),
            "children": []
        }
        for elem_type, count in types.items():
            stage_node["children"].append({
                "name": TYPE_NAMES.get(elem_type, elem_type),
                "value": count
            })
        sunburst_data["children"].append(stage_node)
    
    return json.dumps(sunburst_data, indent=2)

def generate_html_dashboard(report_data: dict, output_path: str):
    """Generate an HTML dashboard with all visualizations."""
    stats = report_data.get('summary', {})
    by_type = stats.get('by_type', {})
    by_stage = stats.get('by_stage', {})
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>定理体系可视化仪表板</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5rem;
            background: linear-gradient(45deg, #00f260, #0575e6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
            background: rgba(255,255,255,0.08);
        }}
        .stat-value {{
            font-size: 3rem;
            font-weight: bold;
            color: #00f260;
        }}
        .stat-label {{
            font-size: 0.9rem;
            color: #888;
            margin-top: 5px;
        }}
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .chart-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .chart-title {{
            font-size: 1.2rem;
            margin-bottom: 15px;
            color: #fff;
        }}
        .issue-list {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .issue-item {{
            padding: 10px;
            margin: 5px 0;
            border-radius: 8px;
            background: rgba(255,100,100,0.1);
            border-left: 3px solid #ff6464;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            margin-top: 30px;
            font-size: 0.8rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔬 定理编号体系可视化仪表板</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{stats.get('total_definitions', 0):,}</div>
                <div class="stat-label">总定义数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats.get('total_references', 0):,}</div>
                <div class="stat-label">总引用数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats.get('files_scanned', 0)}</div>
                <div class="stat-label">扫描文件数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats.get('duplicates', 0)}</div>
                <div class="stat-label">重复编号</div>
            </div>
        </div>
        
        <div class="chart-grid">
            <div class="chart-card">
                <div class="chart-title">📊 按类型分布</div>
                <canvas id="typeChart"></canvas>
            </div>
            <div class="chart-card">
                <div class="chart-title">🗂️ 按阶段分布</div>
                <canvas id="stageChart"></canvas>
            </div>
        </div>
        
        <div class="issue-list">
            <div class="chart-title">⚠️ 问题汇总</div>
            <div class="issue-item">
                <strong>重复编号:</strong> {stats.get('duplicates', 0)} 个ID在多个位置定义
            </div>
            <div class="issue-item">
                <strong>未注册元素:</strong> {stats.get('orphaned', 0)} 个定义未在注册表中
            </div>
            <div class="issue-item">
                <strong>编号间隙:</strong> 检测到连续性缺口
            </div>
        </div>
        
        <div class="timestamp">
            生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
    
    <script>
        // Type distribution chart
        new Chart(document.getElementById('typeChart'), {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps([TYPE_NAMES.get(k, k) for k in by_type.keys()])},
                datasets: [{{
                    data: {json.dumps(list(by_type.values()))},
                    backgroundColor: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{ color: '#fff' }}
                    }}
                }}
            }}
        }});
        
        // Stage distribution chart
        new Chart(document.getElementById('stageChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps([STAGE_NAMES.get(k, k) for k in by_stage.keys()])},
                datasets: [{{
                    label: '元素数量',
                    data: {json.dumps(list(by_stage.values()))},
                    backgroundColor: ['#6C5CE7', '#FD79A8', '#00B894', '#E17055', '#74B9FF']
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{ color: '#888' }},
                        grid: {{ color: 'rgba(255,255,255,0.1)' }}
                    }},
                    x: {{
                        ticks: {{ color: '#888' }},
                        grid: {{ display: false }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML dashboard generated: {output_path}")

def main():
    """Main entry point."""
    root_dir = Path(".")
    report_path = root_dir / ".scripts" / "theorem-validation-report.json"
    
    if not report_path.exists():
        print(f"Error: Report not found at {report_path}")
        return
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    stats = report.get('summary', {})
    by_type = stats.get('by_type', {})
    by_stage = stats.get('by_stage', {})
    by_doc = stats.get('by_doc', {})
    
    # Generate markdown visualization report
    viz_report = f"""# 定理体系可视化报告

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. 总体统计

| 指标 | 数值 |
|------|------|
| 总定义数 | {stats.get('total_definitions', 0):,} |
| 总引用数 | {stats.get('total_references', 0):,} |
| 扫描文件数 | {stats.get('files_scanned', 0)} |
| 重复编号 | {stats.get('duplicates', 0)} |
| 未注册元素 | {stats.get('orphaned', 0)} |

## 2. 按类型分布

{generate_mermaid_pie_chart(by_type, "元素类型分布")}

## 3. 按阶段分布

{generate_mermaid_pie_chart(by_stage, "元素阶段分布")}

## 4. 按文档分布热力图

{generate_distribution_heatmap(by_doc)}

## 5. 问题分析

### 5.1 重复编号
检测到 **{stats.get('duplicates', 0)}** 个重复ID。这些可能是：
- 合法的跨文档引用
- 需要修复的重复定义

### 5.2 未注册元素
检测到 **{stats.get('orphaned', 0)}** 个在文档中定义但未在THEOREM-REGISTRY.md中注册的元素。

## 6. 改进建议

1. **规范化编号体系**: 确保每个定义有唯一的全局ID
2. **更新注册表**: 将未注册元素添加到THEOREM-REGISTRY.md
3. **CI/CD集成**: 使用theorem-validator.py在提交前自动检查

---

*此报告由 theorem-validator.py 自动生成*
"""
    
    # Save markdown report
    viz_path = root_dir / "THEOREM-SYSTEM-VISUALIZATION.md"
    with open(viz_path, 'w', encoding='utf-8') as f:
        f.write(viz_report)
    print(f"Markdown report generated: {viz_path}")
    
    # Generate HTML dashboard
    html_path = root_dir / ".scripts" / "theorem-dashboard.html"
    generate_html_dashboard(report, html_path)
    
    # Generate sunburst data
    sunburst_path = root_dir / ".scripts" / "theorem-sunburst-data.json"
    sunburst_data = generate_sunburst_data(by_type, by_stage, report.get('elements', []))
    with open(sunburst_path, 'w', encoding='utf-8') as f:
        f.write(sunburst_data)
    print(f"Sunburst data generated: {sunburst_path}")

if __name__ == '__main__':
    main()
