#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计仪表盘生成器 (Dashboard Generator)

功能:
    - 生成统计仪表盘Markdown文档
    - 生成趋势图表(使用Mermaid)
    - 生成增长曲线
    - 生成对比分析
    - 支持历史数据可视化

作者: AnalysisDataFlow Project
版本: 1.0.0
"""

import json
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class TrendData:
    """趋势数据"""
    labels: List[str]
    values: List[int]
    growth_rates: List[float]  # 增长率


class DashboardGenerator:
    """仪表盘生成器"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化仪表盘生成器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.root_dir = Path(self.config["project"]["root_dir"]).resolve()
        self.stats_dir = self.root_dir / ".stats"
        self.dashboard_file = self.root_dir / self.config["output"]["dashboard_file"]
        
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # 使用默认配置
            return {
                "project": {"root_dir": "../.."},
                "output": {"dashboard_file": "DASHBOARD.md"}
            }
    
    def load_stats(self) -> Optional[Dict]:
        """加载当前统计数据"""
        stats_file = self.stats_dir / "project-stats.json"
        if stats_file.exists():
            with open(stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def load_history(self) -> List[Dict]:
        """加载历史统计数据"""
        history_file = self.stats_dir / "stats-history.json"
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def generate_dashboard(self) -> str:
        """
        生成完整的仪表盘文档
        
        Returns:
            str: Markdown格式的仪表盘内容
        """
        stats = self.load_stats()
        history = self.load_history()
        
        if not stats:
            return "# 统计仪表盘\n\n> ⚠️ 暂无统计数据，请先运行 stats-collector.py"
        
        sections = [
            self._generate_header(),
            self._generate_summary_cards(stats),
            self._generate_progress_bars(stats),
            self._generate_directory_breakdown(stats),
            self._generate_trend_charts(history),
            self._generate_formal_elements_chart(stats),
            self._generate_growth_analysis(history),
            self._generate_comparison_matrix(stats),
            self._generate_quality_metrics(stats),
            self._generate_footer(),
        ]
        
        return '\n\n---\n\n'.join(sections)
    
    def _generate_header(self) -> str:
        """生成文档头部"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""# 📊 AnalysisDataFlow 项目统计仪表盘

> **自动生成**: {timestamp}  
> **统计周期**: 实时 | **更新频率**: 每日

---

## 导航

- [📈 概览指标](#概览指标)
- [📊 进度总览](#进度总览)
- [📁 目录分析](#目录分析)
- [📉 趋势图表](#趋势图表)
- [🔬 形式化元素](#形式化元素)
- [📈 增长分析](#增长分析)
- [🔍 对比矩阵](#对比矩阵)
- [✅ 质量指标](#质量指标)"""
    
    def _generate_summary_cards(self, stats: Dict) -> str:
        """生成概览卡片"""
        summary = stats.get("summary", {})
        
        return f"""## 概览指标

<div align="center">

| 📚 文档 | 🔬 形式化元素 | 💻 代码示例 | 📈 可视化 |
|:------:|:------------:|:----------:|:---------:|
| **{summary.get('total_docs', 0)}** | **{summary.get('formal_elements', {}).get('total', 0)}** | **{summary.get('code_examples', 0)}** | **{summary.get('mermaid_charts', 0)}** |
| 篇技术文档 | 个定理/定义/引理 | 个代码片段 | 个Mermaid图表 |

</div>

### 详细统计

| 指标 | 数值 | 说明 |
|------|------|------|
| 文档总数 | {summary.get('total_docs', 0)} | Markdown技术文档 |
| 总行数 | {summary.get('total_lines', 0):,} | 文本行数 |
| 总大小 | {summary.get('total_size_mb', 0):.2f} MB | 文档体积 |
| 形式化元素 | {summary.get('formal_elements', {}).get('total', 0)} | 定理+定义+引理+命题+推论 |
| 代码示例 | {summary.get('code_examples', 0)} | 可运行代码片段 |
| Mermaid图表 | {summary.get('mermaid_charts', 0)} | 架构图/流程图/时序图 |

### 形式化元素明细

| 类型 | 数量 | 占比 | 可视化 |
|------|------|------|--------|
| 定理 (Thm) | {summary.get('formal_elements', {}).get('theorems', 0)} | {self._calc_percentage(summary.get('formal_elements', {}).get('theorems', 0), summary.get('formal_elements', {}).get('total', 1))}% | {self._generate_mini_bar(summary.get('formal_elements', {}).get('theorems', 0), summary.get('formal_elements', {}).get('total', 1))} |
| 定义 (Def) | {summary.get('formal_elements', {}).get('definitions', 0)} | {self._calc_percentage(summary.get('formal_elements', {}).get('definitions', 0), summary.get('formal_elements', {}).get('total', 1))}% | {self._generate_mini_bar(summary.get('formal_elements', {}).get('definitions', 0), summary.get('formal_elements', {}).get('total', 1))} |
| 引理 (Lemma) | {summary.get('formal_elements', {}).get('lemmas', 0)} | {self._calc_percentage(summary.get('formal_elements', {}).get('lemmas', 0), summary.get('formal_elements', {}).get('total', 1))}% | {self._generate_mini_bar(summary.get('formal_elements', {}).get('lemmas', 0), summary.get('formal_elements', {}).get('total', 1))} |
| 命题 (Prop) | {summary.get('formal_elements', {}).get('propositions', 0)} | {self._calc_percentage(summary.get('formal_elements', {}).get('propositions', 0), summary.get('formal_elements', {}).get('total', 1))}% | {self._generate_mini_bar(summary.get('formal_elements', {}).get('propositions', 0), summary.get('formal_elements', {}).get('total', 1))} |
| 推论 (Cor) | {summary.get('formal_elements', {}).get('corollaries', 0)} | {self._calc_percentage(summary.get('formal_elements', {}).get('corollaries', 0), summary.get('formal_elements', {}).get('total', 1))}% | {self._generate_mini_bar(summary.get('formal_elements', {}).get('corollaries', 0), summary.get('formal_elements', {}).get('total', 1))} |"""
    
    def _generate_mini_bar(self, value: int, total: int, width: int = 20) -> str:
        """生成迷你进度条"""
        if total == 0:
            return "░" * width
        filled = int((value / total) * width)
        return "█" * filled + "░" * (width - filled)
    
    def _calc_percentage(self, value: int, total: int) -> int:
        """计算百分比"""
        if total == 0:
            return 0
        return round((value / total) * 100)
    
    def _generate_progress_bars(self, stats: Dict) -> str:
        """生成进度条"""
        dirs = stats.get("directories", {})
        
        # 计算各目录进度
        dir_progress = []
        for name, data in dirs.items():
            # 这里假设目标数量为当前数量的110%作为增长空间
            current = data.get("file_count", 0)
            target = max(current, 100)  # 最小目标100
            progress = min(100, int((current / target) * 100))
            dir_progress.append((name, progress, current, data.get("formal_elements", {}).get("total", 0)))
        
        lines = ["## 进度总览", ""]
        
        for name, progress, count, formal in dir_progress:
            bar = self._generate_ascii_bar(progress)
            emoji = {"struct": "📐", "knowledge": "📚", "flink": "🔥", "visuals": "📊"}.get(name, "📁")
            lines.append(f"### {emoji} {name.capitalize()}/")
            lines.append(f"```")
            lines.append(f"进度: [{bar}] {progress}%")
            lines.append(f"文档: {count} | 形式化元素: {formal}")
            lines.append(f"```")
            lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_ascii_bar(self, percentage: int, width: int = 30) -> str:
        """生成ASCII进度条"""
        filled = int((percentage / 100) * width)
        return "█" * filled + "░" * (width - filled)
    
    def _generate_directory_breakdown(self, stats: Dict) -> str:
        """生成目录详细分析"""
        dirs = stats.get("directories", {})
        
        lines = [
            "## 目录分析",
            "",
            "```mermaid",
            "pie title 文档分布",
        ]
        
        for name, data in dirs.items():
            count = data.get("file_count", 0)
            lines.append(f'    "{name.capitalize()}" : {count}')
        
        lines.extend([
            "```",
            "",
            "### 详细统计",
            "",
            "| 目录 | 文档数 | 大小 | 行数 | 定理 | 定义 | 引理 | 代码示例 | 图表 |",
            "|------|--------|------|------|------|------|------|----------|------|"
        ])
        
        for name, data in sorted(dirs.items()):
            formal = data.get("formal_elements", {})
            lines.append(
                f"| {name.capitalize()} | "
                f"{data.get('file_count', 0)} | "
                f"{data.get('size_kb', 0):.0f}KB | "
                f"{data.get('lines', 0):,} | "
                f"{formal.get('theorems', 0)} | "
                f"{formal.get('definitions', 0)} | "
                f"{formal.get('lemmas', 0)} | "
                f"{data.get('code_examples', 0)} | "
                f"{data.get('mermaid_charts', 0)} |"
            )
        
        return '\n'.join(lines)
    
    def _generate_trend_charts(self, history: List[Dict]) -> str:
        """生成趋势图表"""
        if len(history) < 2:
            return "## 趋势图表\n\n> ⚠️ 历史数据不足，需要至少2个时间点的数据才能生成趋势图"
        
        # 准备数据（取最近10个数据点）
        recent = history[-10:]
        labels = [h.get("timestamp", "")[:10] for h in recent]  # 只取日期部分
        docs = [h.get("total_docs", 0) for h in recent]
        formal = [h.get("formal_elements", 0) for h in recent]
        code = [h.get("code_examples", 0) for h in recent]
        
        lines = [
            "## 趋势图表",
            "",
            "### 文档数量趋势",
            "",
            "```mermaid",
            "xychart-beta",
            f'    title "文档数量变化趋势"',
            f'    x-axis [{", ".join(labels)}]',
            '    y-axis "文档数"',
            f'    line [{", ".join(map(str, docs))}]',
            "```",
            "",
            "### 形式化元素趋势",
            "",
            "```mermaid",
            "xychart-beta",
            f'    title "形式化元素增长趋势"',
            f'    x-axis [{", ".join(labels)}]',
            '    y-axis "元素数量"',
            f'    line [{", ".join(map(str, formal))}]',
            "```",
            "",
            "### 代码示例趋势",
            "",
            "```mermaid",
            "xychart-beta",
            f'    title "代码示例增长趋势"',
            f'    x-axis [{", ".join(labels)}]',
            '    y-axis "代码示例数"',
            f'    line [{", ".join(map(str, code))}]',
            "```",
        ]
        
        return '\n'.join(lines)
    
    def _generate_formal_elements_chart(self, stats: Dict) -> str:
        """生成形式化元素分布图"""
        formal = stats.get("summary", {}).get("formal_elements", {})
        
        return f"""## 形式化元素分布

```mermaid
mindmap
  root((形式化元素\n{formal.get('total', 0)}个))
    定理
      {formal.get('theorems', 0)}个
    定义
      {formal.get('definitions', 0)}个
    引理
      {formal.get('lemmas', 0)}个
    命题
      {formal.get('propositions', 0)}个
    推论
      {formal.get('corollaries', 0)}个
```

### 分布饼图

```mermaid
pie title 形式化元素分布
    "定理" : {formal.get('theorems', 0)}
    "定义" : {formal.get('definitions', 0)}
    "引理" : {formal.get('lemmas', 0)}
    "命题" : {formal.get('propositions', 0)}
    "推论" : {formal.get('corollaries', 0)}
```"""
    
    def _generate_growth_analysis(self, history: List[Dict]) -> str:
        """生成增长分析"""
        if len(history) < 2:
            return "## 增长分析\n\n> ⚠️ 历史数据不足"
        
        # 计算增长率
        latest = history[-1]
        previous = history[-2] if len(history) >= 2 else history[0]
        first = history[0]
        
        # 计算周增长
        docs_growth = self._calc_growth_rate(
            previous.get("total_docs", 0),
            latest.get("total_docs", 0)
        )
        
        formal_growth = self._calc_growth_rate(
            previous.get("formal_elements", 0),
            latest.get("formal_elements", 0)
        )
        
        code_growth = self._calc_growth_rate(
            previous.get("code_examples", 0),
            latest.get("code_examples", 0)
        )
        
        # 计算总增长（从第一个记录到现在）
        total_docs_growth = self._calc_growth_rate(
            first.get("total_docs", 0),
            latest.get("total_docs", 0)
        )
        
        return f"""## 增长分析

### 本周增长

| 指标 | 上周 | 本周 | 增长 | 增长率 |
|------|------|------|------|--------|
| 文档数 | {previous.get('total_docs', 0)} | {latest.get('total_docs', 0)} | {latest.get('total_docs', 0) - previous.get('total_docs', 0)} | {docs_growth:+.1f}% |
| 形式化元素 | {previous.get('formal_elements', 0)} | {latest.get('formal_elements', 0)} | {latest.get('formal_elements', 0) - previous.get('formal_elements', 0)} | {formal_growth:+.1f}% |
| 代码示例 | {previous.get('code_examples', 0)} | {latest.get('code_examples', 0)} | {latest.get('code_examples', 0) - previous.get('code_examples', 0)} | {code_growth:+.1f}% |

### 累计增长

| 指标 | 初始 | 当前 | 总增长 |
|------|------|------|--------|
| 文档数 | {first.get('total_docs', 0)} | {latest.get('total_docs', 0)} | +{total_docs_growth:.1f}% |
| 形式化元素 | {first.get('formal_elements', 0)} | {latest.get('formal_elements', 0)} | +{self._calc_growth_rate(first.get('formal_elements', 0), latest.get('formal_elements', 0)):.1f}% |
| 代码示例 | {first.get('code_examples', 0)} | {latest.get('code_examples', 0)} | +{self._calc_growth_rate(first.get('code_examples', 0), latest.get('code_examples', 0)):.1f}% |

### 增长趋势图

```mermaid
graph LR
    A[项目启动<br/>{first.get('total_docs', 0)}文档] -->|+{total_docs_growth:.0f}%| B[当前<br/>{latest.get('total_docs', 0)}文档]
    B --> C{{目标<br/>持续增长}}
    style A fill:#e1f5fe
    style B fill:#c8e6c9
    style C fill:#fff3e0
```"""
    
    def _calc_growth_rate(self, old: int, new: int) -> float:
        """计算增长率"""
        if old == 0:
            return 100.0 if new > 0 else 0.0
        return ((new - old) / old) * 100
    
    def _generate_comparison_matrix(self, stats: Dict) -> str:
        """生成对比矩阵"""
        dirs = stats.get("directories", {})
        
        # 计算各目录指标密度
        metrics = []
        for name, data in dirs.items():
            lines = data.get("lines", 1)
            metrics.append({
                "name": name.capitalize(),
                "docs_per_1k_lines": round(data.get("file_count", 0) / (lines / 1000), 2),
                "formal_per_doc": round(data.get("formal_elements", {}).get("total", 0) / max(data.get("file_count", 1), 1), 2),
                "code_per_doc": round(data.get("code_examples", 0) / max(data.get("file_count", 1), 1), 2),
                "charts_per_doc": round(data.get("mermaid_charts", 0) / max(data.get("file_count", 1), 1), 2),
            })
        
        lines = [
            "## 对比矩阵",
            "",
            "### 各目录效率指标",
            "",
            "| 目录 | 文档/千行 | 形式化/文档 | 代码/文档 | 图表/文档 |",
            "|------|----------|------------|----------|----------|"
        ]
        
        for m in metrics:
            lines.append(
                f"| {m['name']} | {m['docs_per_1k_lines']} | "
                f"{m['formal_per_doc']} | {m['code_per_doc']} | {m['charts_per_doc']} |"
            )
        
        lines.extend([
            "",
            "### 热力图",
            "",
            "```mermaid",
            "graph TB",
            "    subgraph Struct[📐 Struct - 形式化密度高]",
            "        S1[定理密度: ★★★★★]",
            "        S2[定义密度: ★★★★★]",
            "    end",
            "    subgraph Knowledge[📚 Knowledge - 代码密度高]",
            "        K1[代码密度: ★★★★☆]",
            "        K2[模式密度: ★★★★★]",
            "    end",
            "    subgraph Flink[🔥 Flink - 图表密度高]",
            "        F1[图表密度: ★★★★★]",
            "        F2[示例密度: ★★★★☆]",
            "    end",
            "```"
        ])
        
        return '\n'.join(lines)
    
    def _generate_quality_metrics(self, stats: Dict) -> str:
        """生成质量指标"""
        summary = stats.get("summary", {})
        total_docs = summary.get("total_docs", 1)
        formal_total = summary.get("formal_elements", {}).get("total", 0)
        code_examples = summary.get("code_examples", 0)
        charts = summary.get("mermaid_charts", 0)
        
        # 计算质量分数
        formal_density = formal_total / total_docs
        code_density = code_examples / total_docs
        chart_density = charts / total_docs
        
        return f"""## 质量指标

### 文档质量评分

| 指标 | 数值 | 目标 | 评分 | 状态 |
|------|------|------|------|------|
| 形式化密度 | {formal_density:.1f} 元素/文档 | ≥3.0 | {'★' * min(5, int(formal_density))}{'☆' * (5 - min(5, int(formal_density)))} | {'✅' if formal_density >= 3 else '⚠️'} |
| 代码密度 | {code_density:.1f} 示例/文档 | ≥5.0 | {'★' * min(5, int(code_density/2))}{'☆' * (5 - min(5, int(code_density/2)))} | {'✅' if code_density >= 5 else '⚠️'} |
| 可视化密度 | {chart_density:.1f} 图表/文档 | ≥1.5 | {'★' * min(5, int(chart_density))}{'☆' * (5 - min(5, int(chart_density)))} | {'✅' if chart_density >= 1.5 else '⚠️'} |

### 质量雷达

```mermaid
radar
    title 项目质量雷达图
    axis 形式化严谨性 "代码丰富度" "可视化程度" "文档完整性" "结构规范性"
    area Current {formal_density*10}, {code_density*2}, {chart_density*3}, 9, 8
```

### 健康度指标

```mermaid
graph LR
    subgraph 项目健康度
        H1[文档健康: {'优秀' if total_docs > 300 else '良好'}] --> H2[形式化健康: {'优秀' if formal_total > 1500 else '良好'}]
        H2 --> H3[代码健康: {'优秀' if code_examples > 3000 else '良好'}]
        H3 --> H4[可视化健康: {'优秀' if charts > 500 else '良好'}]
    end
    style H1 fill:#{('c8e6c9' if total_docs > 300 else 'fff9c4')}
    style H2 fill:#{('c8e6c9' if formal_total > 1500 else 'fff9c4')}
    style H3 fill:#{('c8e6c9' if code_examples > 3000 else 'fff9c4')}
    style H4 fill:#{('c8e6c9' if charts > 500 else 'fff9c4')}
```"""
    
    def _generate_footer(self) -> str:
        """生成文档底部"""
        return """---

## 说明

- 📊 本仪表盘由 `dashboard-generator.py` 自动生成
- 🔄 更新频率: 每日自动更新
- 📈 数据来源: `.stats/project-stats.json`
- 📜 历史记录: `.stats/stats-history.json`

### 相关文档

- [项目主文档](../README.md)
- [进度跟踪](../PROJECT-TRACKING.md)
- [定理注册表](../THEOREM-REGISTRY.md)

---

*AnalysisDataFlow Project Dashboard v1.0*"""
    
    def save_dashboard(self, content: str):
        """
        保存仪表盘文档
        
        Args:
            content: 仪表盘内容
        """
        with open(self.dashboard_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 仪表盘已保存到: {self.dashboard_file}")


def main():
    """主函数"""
    import sys
    
    script_dir = Path(__file__).parent
    config_path = script_dir / "config.json"
    
    generator = DashboardGenerator(str(config_path))
    
    print("🚀 正在生成统计仪表盘...")
    content = generator.generate_dashboard()
    generator.save_dashboard(content)
    
    print("\n✅ 仪表盘生成完成!")
    return 0


if __name__ == "__main__":
    exit(main())
