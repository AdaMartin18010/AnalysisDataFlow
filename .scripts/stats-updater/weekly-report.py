#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周报生成器 (Weekly Report Generator)

功能:
    - 生成周报文档
    - 本周新增统计
    - 贡献者统计
    - 变更摘要
    - 趋势分析

作者: AnalysisDataFlow Project
版本: 1.0.0
"""

import json
import subprocess
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class WeeklyChange:
    """周变更数据"""
    docs_added: int
    docs_modified: int
    docs_deleted: int
    formal_elements_added: int
    code_examples_added: int
    lines_added: int
    lines_deleted: int


class WeeklyReportGenerator:
    """周报生成器"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化周报生成器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.root_dir = Path(self.config["project"]["root_dir"]).resolve()
        self.stats_dir = self.root_dir / ".stats"
        self.reports_dir = self.root_dir / self.config.get("output", {}).get("weekly_report_dir", "reports/weekly")
        
        # 确保报告目录存在
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # 计算本周日期范围
        self.today = datetime.now()
        self.week_start = self.today - timedelta(days=self.today.weekday())
        self.week_end = self.week_start + timedelta(days=6)
        
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "project": {"root_dir": "../.."},
                "output": {"weekly_report_dir": "reports/weekly"}
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
    
    def get_git_changes(self) -> Dict:
        """
        获取Git变更统计
        
        Returns:
            Dict: 变更统计信息
        """
        changes = {
            "commits": 0,
            "authors": set(),
            "files_changed": 0,
            "insertions": 0,
            "deletions": 0,
        }
        
        try:
            # 获取本周提交统计
            since = self.week_start.strftime("%Y-%m-%d")
            until = (self.week_end + timedelta(days=1)).strftime("%Y-%m-%d")
            
            # 获取提交数量
            result = subprocess.run(
                ["git", "log", "--oneline", f"--since={since}", f"--until={until}", "--format=%h|%an|%s"],
                cwd=self.root_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                commits = [line for line in result.stdout.strip().split('\n') if line]
                changes["commits"] = len(commits)
                
                # 提取作者
                for commit in commits:
                    parts = commit.split('|')
                    if len(parts) >= 2:
                        changes["authors"].add(parts[1])
                
                # 获取文件变更统计
                stat_result = subprocess.run(
                    ["git", "log", "--shortstat", f"--since={since}", f"--until={until}", "--format="],
                    cwd=self.root_dir,
                    capture_output=True,
                    text=True
                )
                
                if stat_result.returncode == 0:
                    # 解析统计信息
                    for line in stat_result.stdout.split('\n'):
                        # 匹配: 3 files changed, 50 insertions(+), 10 deletions(-)
                        match = re.search(r'(\d+) files? changed.*?([\d,]+) insertions?.*?([\d,]+) deletions?', line)
                        if match:
                            changes["files_changed"] += int(match.group(1))
                            changes["insertions"] += int(match.group(2).replace(',', ''))
                            changes["deletions"] += int(match.group(3).replace(',', ''))
            
        except Exception as e:
            print(f"⚠️  获取Git统计失败: {e}")
        
        changes["authors"] = list(changes["authors"])
        return changes
    
    def calculate_weekly_changes(self) -> WeeklyChange:
        """
        计算本周变更
        
        Returns:
            WeeklyChange: 周变更数据
        """
        history = self.load_history()
        current = self.load_stats()
        
        if not current or len(history) < 2:
            # 如果没有历史数据，返回零值
            return WeeklyChange(0, 0, 0, 0, 0, 0, 0)
        
        # 找到上周的数据点
        last_week = history[-2] if len(history) >= 2 else history[0]
        current_summary = current.get("summary", {})
        
        return WeeklyChange(
            docs_added=max(0, current_summary.get("total_docs", 0) - last_week.get("total_docs", 0)),
            docs_modified=0,  # 需要更复杂的逻辑计算
            docs_deleted=0,
            formal_elements_added=max(0, current_summary.get("formal_elements", {}).get("total", 0) - last_week.get("formal_elements", 0)),
            code_examples_added=max(0, current_summary.get("code_examples", 0) - last_week.get("code_examples", 0)),
            lines_added=0,  # 从Git统计获取
            lines_deleted=0
        )
    
    def generate_report(self) -> str:
        """
        生成周报
        
        Returns:
            str: 周报Markdown内容
        """
        stats = self.load_stats()
        history = self.load_history()
        git_changes = self.get_git_changes()
        weekly_changes = self.calculate_weekly_changes()
        
        if not stats:
            return "# 项目周报\n\n> ⚠️ 暂无统计数据"
        
        sections = [
            self._generate_header(),
            self._generate_summary(stats, weekly_changes, git_changes),
            self._generate_new_additions(stats, weekly_changes),
            self._generate_contributors(git_changes),
            self._generate_changes_summary(git_changes),
            self._generate_trend_analysis(history),
            self._generate_next_week_plan(),
            self._generate_footer(),
        ]
        
        return '\n\n---\n\n'.join(sections)
    
    def _generate_header(self) -> str:
        """生成周报头部"""
        week_num = self.today.isocalendar()[1]
        
        return f"""# 📊 AnalysisDataFlow 项目周报

> **报告周期**: {self.week_start.strftime('%Y年%m月%d日')} - {self.week_end.strftime('%Y年%m月%d日')}  
> **第{week_num}周** | **自动生成**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 目录

- [📈 本周概览](#本周概览)
- [🆕 新增内容](#新增内容)
- [👥 贡献者](#贡献者)
- [📝 变更摘要](#变更摘要)
- [📊 趋势分析](#趋势分析)
- [🎯 下周计划](#下周计划)

---"""
    
    def _generate_summary(self, stats: Dict, changes: WeeklyChange, git_changes: Dict) -> str:
        """生成概览部分"""
        summary = stats.get("summary", {})
        
        # 计算增长率
        docs_growth = changes.docs_added
        formal_growth = changes.formal_elements_added
        code_growth = changes.code_examples_added
        
        # 趋势指示器
        docs_trend = "📈" if docs_growth > 0 else "➡️" if docs_growth == 0 else "📉"
        formal_trend = "📈" if formal_growth > 0 else "➡️" if formal_growth == 0 else "📉"
        code_trend = "📈" if code_growth > 0 else "➡️" if code_growth == 0 else "📉"
        
        return f"""## 本周概览

### 核心指标

| 指标 | 当前值 | 本周变化 | 趋势 |
|------|--------|----------|------|
| 📚 文档总数 | {summary.get('total_docs', 0)} | {'+' if docs_growth >= 0 else ''}{docs_growth} | {docs_trend} |
| 🔬 形式化元素 | {summary.get('formal_elements', {}).get('total', 0):,} | {'+' if formal_growth >= 0 else ''}{formal_growth} | {formal_trend} |
| 💻 代码示例 | {summary.get('code_examples', 0):,} | {'+' if code_growth >= 0 else ''}{code_growth} | {code_trend} |
| 📈 Mermaid图表 | {summary.get('mermaid_charts', 0)} | - | ➡️ |

### Git活动

| 指标 | 数值 |
|------|------|
| 📝 提交次数 | {git_changes.get('commits', 0)} |
| 👥 活跃贡献者 | {len(git_changes.get('authors', []))} |
| 📁 变更文件 | {git_changes.get('files_changed', 0)} |
| ➕ 新增行数 | {git_changes.get('insertions', 0)} |
| ➖ 删除行数 | {git_changes.get('deletions', 0)} |
| 📊 净变更 | {git_changes.get('insertions', 0) - git_changes.get('deletions', 0):+d} |

### 项目健康度

```mermaid
graph TD
    A[本周项目健康度] --> B[文档增长: {'优秀' if docs_growth > 5 else '正常' if docs_growth >= 0 else '需关注'}]
    A --> C[形式化增长: {'优秀' if formal_growth > 20 else '正常' if formal_growth >= 0 else '需关注'}]
    A --> D[代码增长: {'优秀' if code_growth > 50 else '正常' if code_growth >= 0 else '需关注'}]
    A --> E[提交活跃: {'活跃' if git_changes.get('commits', 0) > 10 else '正常' if git_changes.get('commits', 0) > 0 else '静默'}]
    
    style A fill:#e3f2fd
    style B fill:#{'c8e6c9' if docs_growth > 5 else 'fff9c4' if docs_growth >= 0 else 'ffcdd2'}
    style C fill:#{'c8e6c9' if formal_growth > 20 else 'fff9c4' if formal_growth >= 0 else 'ffcdd2'}
    style D fill:#{'c8e6c9' if code_growth > 50 else 'fff9c4' if code_growth >= 0 else 'ffcdd2'}
    style E fill:#{'c8e6c9' if git_changes.get('commits', 0) > 10 else 'fff9c4' if git_changes.get('commits', 0) > 0 else 'ffcdd2'}
```"""
    
    def _generate_new_additions(self, stats: Dict, changes: WeeklyChange) -> str:
        """生成新增内容部分"""
        dirs = stats.get("directories", {})
        
        # 如果没有新增，显示当前状态
        if changes.docs_added == 0 and changes.formal_elements_added == 0:
            return f"""## 新增内容

> ℹ️ 本周无新增文档或形式化元素。

### 当前各目录状态

| 目录 | 文档数 | 形式化元素 | 代码示例 | 图表 |
|------|--------|------------|----------|------|
""" + '\n'.join([
            f"| {name.capitalize()}/ | {data.get('file_count', 0)} | {data.get('formal_elements', {}).get('total', 0)} | {data.get('code_examples', 0)} | {data.get('mermaid_charts', 0)} |"
            for name, data in sorted(dirs.items())
        ])
        
        return f"""## 新增内容

### 本周新增统计

| 类型 | 数量 | 占比 |
|------|------|------|
| 新增文档 | {changes.docs_added} | {self._calc_percentage(changes.docs_added, stats.get('summary', {}).get('total_docs', 1))}% |
| 新增形式化元素 | {changes.formal_elements_added} | {self._calc_percentage(changes.formal_elements_added, stats.get('summary', {}).get('formal_elements', {}).get('total', 1))}% |
| 新增代码示例 | {changes.code_examples_added} | {self._calc_percentage(changes.code_examples_added, stats.get('summary', {}).get('code_examples', 1))}% |

### 各目录新增分布

```mermaid
pie title 本周新增文档分布
""" + '\n'.join([
            f'    "{name.capitalize()}" : {data.get("file_count", 0)}'
            for name, data in sorted(dirs.items())
        ]) + """
```

### 新增内容详情

| 目录 | 当前文档 | 形式化元素 | 代码示例 |
|------|----------|------------|----------|
""" + '\n'.join([
            f"| {name.capitalize()}/ | {data.get('file_count', 0)} | {data.get('formal_elements', {}).get('total', 0)} | {data.get('code_examples', 0)} |"
            for name, data in sorted(dirs.items())
        ])
    
    def _calc_percentage(self, value: int, total: int) -> int:
        """计算百分比"""
        if total == 0:
            return 0
        return round((value / total) * 100)
    
    def _generate_contributors(self, git_changes: Dict) -> str:
        """生成贡献者部分"""
        authors = git_changes.get("authors", [])
        commits = git_changes.get("commits", 0)
        
        if not authors:
            return """## 贡献者

> ℹ️ 本周暂无Git提交记录或无法获取贡献者信息。

### 贡献统计

| 指标 | 数值 |
|------|------|
| 活跃贡献者 | 0 |
| 提交次数 | 0 |"""
        
        # 尝试获取每个作者的提交数
        author_commits = []
        try:
            since = self.week_start.strftime("%Y-%m-%d")
            until = (self.week_end + timedelta(days=1)).strftime("%Y-%m-%d")
            
            for author in authors:
                result = subprocess.run(
                    ["git", "log", "--oneline", f"--since={since}", f"--until={until}", 
                     "--author", author, "--format=%h"],
                    cwd=self.root_dir,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    commit_count = len([l for l in result.stdout.strip().split('\n') if l])
                    author_commits.append((author, commit_count))
            
            # 按提交数排序
            author_commits.sort(key=lambda x: x[1], reverse=True)
            
        except Exception:
            author_commits = [(author, 0) for author in authors]
        
        contributors_table = '\n'.join([
            f"| {i+1} | {name} | {count} | {'⭐' if i == 0 else '👍' if i == 1 else '💪'} |"
            for i, (name, count) in enumerate(author_commits[:5])  # 只显示前5
        ])
        
        return f"""## 贡献者

### 本周活跃贡献者 ({len(authors)}人)

| 排名 | 贡献者 | 提交数 | 徽章 |
|------|--------|--------|------|
{contributors_table}

### 贡献分布

```mermaid
graph LR
    subgraph 本周贡献
""" + '\n'.join([
            f'        A{i}[{name}<br/>{count}次]' 
            for i, (name, count) in enumerate(author_commits[:4])
        ]) + """
    end
```

### 累计贡献

- 本周提交总数: **{commits}** 次
- 活跃贡献者: **{len(authors)}** 人
- 人均提交: **{commits / len(authors) if authors else 0:.1f}** 次"""
    
    def _generate_changes_summary(self, git_changes: Dict) -> str:
        """生成变更摘要"""
        insertions = git_changes.get("insertions", 0)
        deletions = git_changes.get("deletions", 0)
        net_change = insertions - deletions
        files_changed = git_changes.get("files_changed", 0)
        
        # 变更类型分析（模拟）
        change_types = []
        if insertions > deletions * 2:
            change_types.append("以新增内容为主")
        elif deletions > insertions * 2:
            change_types.append("以删除/重构为主")
        else:
            change_types.append("增删平衡，优化迭代")
        
        if files_changed > 20:
            change_types.append("大规模变更")
        elif files_changed > 10:
            change_types.append("中等规模变更")
        else:
            change_types.append("小规模精细调整")
        
        return f"""## 变更摘要

### 代码变更统计

| 指标 | 数值 | 说明 |
|------|------|------|
| 变更文件 | {files_changed} | 涉及文件数量 |
| 新增行数 | +{insertions:,} | 新增代码/文档 |
| 删除行数 | -{deletions:,} | 删除代码/文档 |
| 净变更 | {net_change:+d} | 总体变化 |

### 变更类型分析

- **变更特征**: {', '.join(change_types)}
- **变更强度**: {'高' if files_changed > 20 else '中' if files_changed > 10 else '低'}
- **净增长**: {'正增长' if net_change > 0 else '负增长' if net_change < 0 else '持平'}

### 变更趋势图

```mermaid
xychart-beta
    title "本周变更趋势"
    x-axis [新增, 删除, 净变更]
    y-axis "行数"
    bar [{insertions}, {deletions}, {abs(net_change)}]
```"""
    
    def _generate_trend_analysis(self, history: List[Dict]) -> str:
        """生成趋势分析"""
        if len(history) < 2:
            return """## 趋势分析

> ℹ️ 历史数据不足，无法生成趋势分析。需要至少2周的数据。"""
        
        # 计算最近几周的趋势
        recent = history[-4:] if len(history) >= 4 else history
        
        # 计算平均增长率
        if len(recent) >= 2:
            docs_growth = ((recent[-1].get("total_docs", 0) - recent[0].get("total_docs", 0)) 
                          / max(recent[0].get("total_docs", 1), 1)) * 100
            formal_growth = ((recent[-1].get("formal_elements", 0) - recent[0].get("formal_elements", 0)) 
                            / max(recent[0].get("formal_elements", 1), 1)) * 100
        else:
            docs_growth = 0
            formal_growth = 0
        
        # 预测下周
        current_docs = recent[-1].get("total_docs", 0)
        current_formal = recent[-1].get("formal_elements", 0)
        
        predicted_docs = int(current_docs * (1 + docs_growth / 100 / len(recent)))
        predicted_formal = int(current_formal * (1 + formal_growth / 100 / len(recent)))
        
        return f"""## 趋势分析

### 近期趋势（最近{len(recent)}周）

| 指标 | 起始值 | 当前值 | 总增长 | 平均周增长 |
|------|--------|--------|--------|------------|
| 文档数 | {recent[0].get('total_docs', 0)} | {recent[-1].get('total_docs', 0)} | +{recent[-1].get('total_docs', 0) - recent[0].get('total_docs', 0)} | {docs_growth/len(recent):+.1f}% |
| 形式化元素 | {recent[0].get('formal_elements', 0)} | {recent[-1].get('formal_elements', 0)} | +{recent[-1].get('formal_elements', 0) - recent[0].get('formal_elements', 0)} | {formal_growth/len(recent):+.1f}% |

### 趋势预测

基于当前趋势，预测下周指标:

| 指标 | 当前值 | 预测值 | 预测变化 |
|------|--------|--------|----------|
| 文档数 | {current_docs} | {predicted_docs} | {predicted_docs - current_docs:+d} |
| 形式化元素 | {current_formal} | {predicted_formal} | {predicted_formal - current_formal:+d} |

### 历史走势

```mermaid
graph LR
""" + ' --> '.join([
            f'W{i}[{h.get("total_docs", 0)}篇]'
            for i, h in enumerate(recent)
        ]) + f"""
    W{len(recent)-1} --> W{len(recent)}[预测<br/>{predicted_docs}篇]
    
    style W{len(recent)} fill:#fff3e0
```

### 趋势评估

- **文档增长趋势**: {'上升📈' if docs_growth > 0 else '下降📉' if docs_growth < 0 else '稳定➡️'}
- **形式化深度**: {'加强' if formal_growth > docs_growth else '持平' if formal_growth == docs_growth else '放缓'}
- **整体健康度**: {'优秀⭐' if docs_growth > 5 and formal_growth > 10 else '良好👍' if docs_growth >= 0 else '需关注⚠️'}"""
    
    def _generate_next_week_plan(self) -> str:
        """生成下周计划"""
        return """## 下周计划

### 计划任务

| 优先级 | 任务 | 目标 | 负责人 |
|--------|------|------|--------|
| P0 | 内容审核 | 确保文档质量 | 核心团队 |
| P1 | 形式化完善 | 补充定理证明 | 形式化团队 |
| P2 | 代码示例 | 增加可运行示例 | 工程团队 |
| P3 | 可视化优化 | 完善Mermaid图表 | 文档团队 |

### 目标指标

| 指标 | 本周基线 | 下周目标 | 增长预期 |
|------|----------|----------|----------|
| 文档数 | 基准值 | +2~5篇 | 稳定增长 |
| 形式化元素 | 基准值 | +10~20个 | 持续完善 |
| 代码示例 | 基准值 | +20~50个 | 丰富实践 |

### 风险提醒

- [ ] 关注外部链接有效性
- [ ] 检查定理编号唯一性
- [ ] 验证Mermaid语法正确性
- [ ] 更新依赖版本信息

---

**注**: 下周计划为自动生成模板，实际计划请根据项目情况调整。"""
    
    def _generate_footer(self) -> str:
        """生成页脚"""
        return f"""---

## 报告说明

- 📊 本报告由 `weekly-report.py` 自动生成
- 📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 📁 报告位置: `{self.reports_dir}`
- 🔄 更新频率: 每周日自动生成

### 数据来源

- 统计数据: `.stats/project-stats.json`
- 历史数据: `.stats/stats-history.json`
- Git数据: `git log` 命令输出

---

*AnalysisDataFlow Weekly Report v1.0*"""
    
    def save_report(self, content: str):
        """
        保存周报
        
        Args:
            content: 周报内容
        """
        week_num = self.today.isocalendar()[1]
        filename = f"weekly-report-W{week_num:02d}-{self.today.strftime('%Y%m%d')}.md"
        report_path = self.reports_dir / filename
        
        # 同时保存为最新周报
        latest_path = self.reports_dir / "weekly-report-latest.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        with open(latest_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 周报已保存:")
        print(f"   - {report_path}")
        print(f"   - {latest_path}")


def main():
    """主函数"""
    import sys
    
    script_dir = Path(__file__).parent
    config_path = script_dir / "config.json"
    
    generator = WeeklyReportGenerator(str(config_path))
    
    print("🚀 正在生成周报...")
    
    report = generator.generate_report()
    generator.save_report(report)
    
    print("\n✅ 周报生成完成!")
    return 0


if __name__ == "__main__":
    exit(main())
