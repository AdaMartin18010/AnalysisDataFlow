#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社区反馈聚合脚本 (Community Feedback Aggregator)

功能:
1. 读取和分析 GitHub Issues
2. 统计反馈类型分布
3. 生成月度/季度反馈报告
4. 提取高优先级任务
5. 生成贡献者统计
6. 更新 CONTRIBUTORS.md

作者: AnalysisDataFlow Community
版本: 1.0.0
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import argparse


# ============== 配置常量 ==============

DEFAULT_CONFIG = {
    "repo_owner": "AnalysisDataFlow",
    "repo_name": "AnalysisDataFlow",
    "github_api_url": "https://api.github.com",
    "output_dir": "reports/feedback",
    "contributors_file": "CONTRIBUTORS.md",
    "stats_file": ".stats/feedback-stats.json",
    "priority_labels": ["P0", "P1", "P2", "P3"],
    "category_labels": ["Struct", "Knowledge", "Flink"],
    "type_labels": ["bug", "enhancement", "documentation", "new-topic"],
    "status_labels": ["triage", "in-progress", "completed", "wontfix"],
}

# ============== 数据类定义 ==============

@dataclass
class FeedbackItem:
    """单个反馈项的数据结构"""
    number: int
    title: str
    body: str
    author: str
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime]
    state: str
    labels: List[str]
    feedback_type: str
    priority: str
    category: str
    url: str
    comments_count: int
    reactions_count: int


@dataclass
class FeedbackStats:
    """反馈统计数据结构"""
    total_issues: int
    open_issues: int
    closed_issues: int
    by_type: Dict[str, int]
    by_priority: Dict[str, int]
    by_category: Dict[str, int]
    by_status: Dict[str, int]
    by_author: Dict[str, int]
    monthly_trend: Dict[str, int]
    avg_resolution_days: float
    high_priority_open: List[FeedbackItem]


@dataclass
class Contributor:
    """贡献者数据结构"""
    username: str
    issues_opened: int
    issues_closed: int
    prs_opened: int
    prs_merged: int
    comments_made: int
    first_contribution: Optional[datetime]
    last_contribution: Optional[datetime]
    contributions_by_type: Dict[str, int]


# ============== GitHub API 交互 ==============

class GitHubAPI:
    """GitHub API 封装类"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.base_url = DEFAULT_CONFIG["github_api_url"]
        self.owner = DEFAULT_CONFIG["repo_owner"]
        self.repo = DEFAULT_CONFIG["repo_name"]
    
    def _headers(self) -> Dict[str, str]:
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers
    
    def fetch_issues(self, state: str = "all", since: Optional[str] = None) -> List[Dict]:
        """获取 Issues 列表"""
        import urllib.request
        import urllib.error
        
        issues = []
        page = 1
        per_page = 100
        
        while True:
            url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues"
            params = f"?state={state}&per_page={per_page}&page={page}"
            if since:
                params += f"&since={since}"
            
            try:
                req = urllib.request.Request(url + params, headers=self._headers())
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = json.loads(response.read().decode())
                    if not data:
                        break
                    issues.extend(data)
                    page += 1
            except urllib.error.HTTPError as e:
                print(f"Error fetching issues: {e}")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                break
        
        return issues
    
    def fetch_issue_comments(self, issue_number: int) -> List[Dict]:
        """获取 Issue 的评论"""
        import urllib.request
        
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}/comments"
        
        try:
            req = urllib.request.Request(url, headers=self._headers())
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"Error fetching comments for issue #{issue_number}: {e}")
            return []


# ============== 反馈处理器 ==============

class FeedbackProcessor:
    """反馈数据处理核心类"""
    
    def __init__(self):
        self.type_mapping = {
            "bug": "错误报告",
            "enhancement": "功能建议",
            "documentation": "文档改进",
            "new-topic": "新主题请求",
        }
        self.priority_pattern = re.compile(r'\b(P0|P1|P2|P3)\b', re.IGNORECASE)
        self.category_pattern = re.compile(r'\b(Struct|Knowledge|Flink)\b', re.IGNORECASE)
    
    def parse_issue(self, issue_data: Dict) -> Optional[FeedbackItem]:
        """解析单个 Issue 数据"""
        if "pull_request" in issue_data:
            return None  # 跳过 PR
        
        labels = [label["name"] for label in issue_data.get("labels", [])]
        
        # 识别反馈类型
        feedback_type = "other"
        for label in labels:
            if label in self.type_mapping:
                feedback_type = label
                break
        
        # 识别优先级
        priority = "P3"  # 默认最低优先级
        for label in labels:
            match = self.priority_pattern.match(label)
            if match:
                priority = match.group(1).upper()
                break
        
        # 识别领域分类
        category = "other"
        for label in labels:
            match = self.category_pattern.match(label)
            if match:
                category = match.group(1)
                break
        
        # 解析时间
        created_at = datetime.fromisoformat(issue_data["created_at"].replace('Z', '+00:00'))
        updated_at = datetime.fromisoformat(issue_data["updated_at"].replace('Z', '+00:00'))
        closed_at = None
        if issue_data.get("closed_at"):
            closed_at = datetime.fromisoformat(issue_data["closed_at"].replace('Z', '+00:00'))
        
        return FeedbackItem(
            number=issue_data["number"],
            title=issue_data["title"],
            body=issue_data.get("body", ""),
            author=issue_data["user"]["login"],
            created_at=created_at,
            updated_at=updated_at,
            closed_at=closed_at,
            state=issue_data["state"],
            labels=labels,
            feedback_type=feedback_type,
            priority=priority,
            category=category,
            url=issue_data["html_url"],
            comments_count=issue_data.get("comments", 0),
            reactions_count=sum(
                issue_data.get("reactions", {}).get(k, 0) 
                for k in ["+1", "-1", "laugh", "confused", "heart", "hooray", "eyes", "rocket"]
            )
        )
    
    def calculate_stats(self, items: List[FeedbackItem]) -> FeedbackStats:
        """计算反馈统计"""
        total = len(items)
        open_items = [i for i in items if i.state == "open"]
        closed_items = [i for i in items if i.state == "closed"]
        
        # 按类型统计
        by_type = Counter(i.feedback_type for i in items)
        
        # 按优先级统计
        by_priority = Counter(i.priority for i in items)
        
        # 按领域统计
        by_category = Counter(i.category for i in items)
        
        # 按状态统计（基于标签）
        by_status = defaultdict(int)
        for item in items:
            has_status = False
            for status in DEFAULT_CONFIG["status_labels"]:
                if status in item.labels:
                    by_status[status] += 1
                    has_status = True
                    break
            if not has_status:
                by_status[item.state] += 1
        
        # 按作者统计
        by_author = Counter(i.author for i in items)
        
        # 月度趋势
        monthly_trend = defaultdict(int)
        for item in items:
            month_key = item.created_at.strftime("%Y-%m")
            monthly_trend[month_key] += 1
        
        # 平均解决时间
        resolution_times = []
        for item in closed_items:
            if item.closed_at:
                days = (item.closed_at - item.created_at).days
                resolution_times.append(days)
        avg_resolution = sum(resolution_times) / len(resolution_times) if resolution_times else 0
        
        # 高优先级未解决问题
        high_priority_open = [
            i for i in open_items 
            if i.priority in ["P0", "P1"]
        ]
        high_priority_open.sort(key=lambda x: (x.priority, x.created_at))
        
        return FeedbackStats(
            total_issues=total,
            open_issues=len(open_items),
            closed_issues=len(closed_items),
            by_type=dict(by_type),
            by_priority=dict(by_priority),
            by_category=dict(by_category),
            by_status=dict(by_status),
            by_author=dict(by_author),
            monthly_trend=dict(sorted(monthly_trend.items())),
            avg_resolution_days=avg_resolution,
            high_priority_open=high_priority_open[:20]  # 只保留前20个
        )


# ============== 报告生成器 ==============

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_monthly_report(self, stats: FeedbackStats, month: str) -> str:
        """生成月度报告"""
        report = f"""# 📊 社区反馈月度报告 - {month}

> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📈 总体概览

| 指标 | 数值 |
|------|------|
| 总 Issue 数 | {stats.total_issues} |
| 待处理 | {stats.open_issues} |
| 已解决 | {stats.closed_issues} |
| 平均解决时间 | {stats.avg_resolution_days:.1f} 天 |
| 解决率 | {stats.closed_issues / stats.total_issues * 100:.1f}% |

---

## 🏷️ 按类型分布

| 类型 | 数量 | 占比 |
|------|------|------|
"""
        for type_name, count in sorted(stats.by_type.items(), key=lambda x: -x[1]):
            pct = count / stats.total_issues * 100
            type_label = FeedbackProcessor().type_mapping.get(type_name, type_name)
            report += f"| {type_label} | {count} | {pct:.1f}% |\n"
        
        report += """
---

## 🎯 按优先级分布

| 优先级 | 数量 | 状态 |
|--------|------|------|
"""
        priority_colors = {"P0": "🔴", "P1": "🟠", "P2": "🟡", "P3": "🟢"}
        for p in ["P0", "P1", "P2", "P3"]:
            count = stats.by_priority.get(p, 0)
            report += f"| {priority_colors.get(p, '⚪')} {p} | {count} | {'需紧急处理' if p in ['P0', 'P1'] and count > 0 else '正常'} |\n"
        
        report += """
---

## 📚 按领域分布

| 领域 | 数量 | 占比 |
|------|------|------|
"""
        for cat, count in sorted(stats.by_category.items(), key=lambda x: -x[1]):
            pct = count / stats.total_issues * 100 if stats.total_issues > 0 else 0
            report += f"| {cat} | {count} | {pct:.1f}% |\n"
        
        report += """
---

## ⚡ 高优先级待处理任务

"""
        if stats.high_priority_open:
            report += "| Issue | 标题 | 优先级 | 创建时间 | 作者 |\n"
            report += "|-------|------|--------|----------|------|\n"
            for item in stats.high_priority_open:
                created_str = item.created_at.strftime("%Y-%m-%d")
                report += f"| #{item.number} | [{item.title[:40]}...]({item.url}) | {item.priority} | {created_str} | @{item.author} |\n"
        else:
            report += "✅ 当前没有高优先级待处理任务！\n"
        
        report += """
---

## 📊 月度趋势

```mermaid
xychart-beta
    title "反馈提交趋势"
    x-axis ["""
        
        months = list(stats.monthly_trend.keys())[-12:]  # 最近12个月
        report += ", ".join([f'"{m}"' for m in months])
        report += """]
    y-axis "Issue 数量"
    bar ["""
        
        counts = [stats.monthly_trend.get(m, 0) for m in months]
        report += ", ".join(map(str, counts))
        report += """]
```

---

## 👥 活跃贡献者

| 排名 | 用户名 | Issue 数 |
|------|--------|----------|
"""
        
        top_authors = sorted(stats.by_author.items(), key=lambda x: -x[1])[:10]
        for rank, (author, count) in enumerate(top_authors, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "🏅"
            report += f"| {medal} {rank} | @{author} | {count} |\n"
        
        report += f"""
---

## 📝 详细数据

完整数据已保存至: `{DEFAULT_CONFIG['stats_file']}`

---

*本报告由反馈聚合脚本自动生成*
"""
        
        return report
    
    def generate_contributors_list(self, contributors: List[Contributor]) -> str:
        """生成贡献者列表"""
        content = """# 🏆 项目贡献者

> 感谢所有为 AnalysisDataFlow 项目做出贡献的社区成员！

---

## 📋 统计说明

本列表自动统计以下贡献类型：
- 📝 提交 Issue（错误报告、功能建议、文档改进）
- 🔧 提交 Pull Request
- 💬 参与讨论和代码审查
- 📚 内容贡献和校对

---

## 🌟 核心贡献者

"""
        
        # 按贡献度排序
        sorted_contributors = sorted(
            contributors, 
            key=lambda c: (c.issues_opened + c.prs_merged + c.comments_made), 
            reverse=True
        )
        
        tiers = {
            "🏆 铂金贡献者": [],
            "🥇 金牌贡献者": [],
            "🥈 银牌贡献者": [],
            "🥉 铜牌贡献者": [],
            "👏 热心贡献者": []
        }
        
        for c in sorted_contributors:
            score = c.issues_opened + c.prs_merged * 2 + c.comments_made
            if score >= 50:
                tiers["🏆 铂金贡献者"].append(c)
            elif score >= 20:
                tiers["🥇 金牌贡献者"].append(c)
            elif score >= 10:
                tiers["🥈 银牌贡献者"].append(c)
            elif score >= 5:
                tiers["🥉 铜牌贡献者"].append(c)
            else:
                tiers["👏 热心贡献者"].append(c)
        
        for tier_name, tier_contributors in tiers.items():
            if tier_contributors:
                content += f"### {tier_name}\n\n"
                content += "| 用户名 | Issue | PR | 评论 | 首次贡献 |\n"
                content += "|--------|-------|-----|------|----------|\n"
                for c in tier_contributors[:20]:  # 每级最多显示20人
                    first = c.first_contribution.strftime("%Y-%m") if c.first_contribution else "-"
                    content += f"| [@{c.username}](https://github.com/{c.username}) | {c.issues_opened} | {c.prs_merged} | {c.comments_made} | {first} |\n"
                content += "\n"
        
        content += f"""---

## 📊 贡献统计摘要

- **总贡献者数**: {len(contributors)}
- **总 Issue 数**: {sum(c.issues_opened for c in contributors)}
- **总 PR 数**: {sum(c.prs_merged for c in contributors)}

---

## 🙏 致谢

特别感谢以下社区成员对项目的长期支持和贡献：

"""
        
        # 列出长期贡献者（有首次和最近贡献记录的）
        long_term = [c for c in contributors if c.first_contribution and c.last_contribution]
        if long_term:
            long_term.sort(key=lambda c: (c.last_contribution - c.first_contribution).days, reverse=True)
            for c in long_term[:10]:
                days = (c.last_contribution - c.first_contribution).days
                content += f"- [@{c.username}](https://github.com/{c.username}) - 持续贡献 {days} 天\n"
        
        content += f"""
---

*本列表由反馈聚合脚本自动更新于 {datetime.now().strftime("%Y-%m-%d")}*

想要加入贡献者列表？请参考我们的 [贡献指南](../CONTRIBUTING.md)！
"""
        
        return content
    
    def save_report(self, filename: str, content: str):
        """保存报告文件"""
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"报告已保存: {filepath}")
        return filepath
    
    def save_json(self, filename: str, data: Any):
        """保存 JSON 数据"""
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        print(f"数据已保存: {filepath}")
        return filepath


# ============== 主程序 ==============

def main():
    parser = argparse.ArgumentParser(
        description="社区反馈聚合工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 生成月度报告
  python feedback-aggregator.py --monthly
  
  # 更新贡献者列表
  python feedback-aggregator.py --update-contributors
  
  # 提取高优先级任务
  python feedback-aggregator.py --extract-p0-p1
  
  # 完整分析
  python feedback-aggregator.py --full-analysis
        """
    )
    
    parser.add_argument("--monthly", action="store_true", help="生成月度报告")
    parser.add_argument("--update-contributors", action="store_true", help="更新贡献者列表")
    parser.add_argument("--extract-p0-p1", action="store_true", help="提取高优先级任务")
    parser.add_argument("--full-analysis", action="store_true", help="执行完整分析")
    parser.add_argument("--output-dir", default=DEFAULT_CONFIG["output_dir"], help="输出目录")
    parser.add_argument("--token", help="GitHub API Token")
    parser.add_argument("--since", help="起始日期 (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    # 如果没有指定任何操作，默认执行完整分析
    if not any([args.monthly, args.update_contributors, args.extract_p0_p1]):
        args.full_analysis = True
    
    print("=" * 60)
    print("🔧 社区反馈聚合工具 v1.0.0")
    print("=" * 60)
    
    # 初始化组件
    github = GitHubAPI(token=args.token)
    processor = FeedbackProcessor()
    reporter = ReportGenerator(args.output_dir)
    
    # 获取数据
    print("\n📥 正在获取 Issue 数据...")
    since = args.since if args.since else (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    try:
        issues_data = github.fetch_issues(state="all", since=since)
        print(f"✅ 获取到 {len(issues_data)} 个 Issue")
    except Exception as e:
        print(f"⚠️ 无法连接 GitHub API: {e}")
        print("   将使用本地缓存数据（如果可用）")
        issues_data = []
    
    # 解析 Issue
    print("\n🔍 正在解析 Issue 数据...")
    feedback_items = []
    for data in issues_data:
        item = processor.parse_issue(data)
        if item:
            feedback_items.append(item)
    print(f"✅ 解析成功 {len(feedback_items)} 个反馈项")
    
    # 计算统计
    print("\n📊 正在计算统计数据...")
    stats = processor.calculate_stats(feedback_items)
    
    # 执行请求的操作
    if args.full_analysis or args.monthly:
        print("\n📝 正在生成月度报告...")
        current_month = datetime.now().strftime("%Y-%m")
        report = reporter.generate_monthly_report(stats, current_month)
        reporter.save_report(f"monthly-report-{current_month}.md", report)
    
    if args.full_analysis or args.extract_p0_p1:
        print("\n⚡ 正在提取高优先级任务...")
        if stats.high_priority_open:
            tasks = "# 🔴 高优先级待处理任务\n\n"
            tasks += "| 优先级 | Issue | 标题 | 领域 | 创建时间 |\n"
            tasks += "|--------|-------|------|------|----------|\n"
            for item in stats.high_priority_open:
                created = item.created_at.strftime("%Y-%m-%d")
                tasks += f"| {item.priority} | #{item.number} | [{item.title[:50]}...]({item.url}) | {item.category} | {created} |\n"
            reporter.save_report("high-priority-tasks.md", tasks)
        else:
            print("   ✅ 当前没有高优先级待处理任务")
    
    if args.full_analysis or args.update_contributors:
        print("\n👥 正在更新贡献者列表...")
        # 构建简单的贡献者列表（基于 Issue 作者）
        contributors = []
        for author, count in stats.by_author.items():
            contributors.append(Contributor(
                username=author,
                issues_opened=count,
                issues_closed=0,
                prs_opened=0,
                prs_merged=0,
                comments_made=0,
                first_contribution=None,
                last_contribution=None,
                contributions_by_type={}
            ))
        
        contributors_content = reporter.generate_contributors_list(contributors)
        with open(DEFAULT_CONFIG["contributors_file"], 'w', encoding='utf-8') as f:
            f.write(contributors_content)
        print(f"   ✅ 已更新 {DEFAULT_CONFIG['contributors_file']}")
    
    # 保存统计数据
    print("\n💾 正在保存统计数据...")
    stats_dict = {
        "generated_at": datetime.now().isoformat(),
        "total_issues": stats.total_issues,
        "open_issues": stats.open_issues,
        "closed_issues": stats.closed_issues,
        "by_type": stats.by_type,
        "by_priority": stats.by_priority,
        "by_category": stats.by_category,
        "by_status": stats.by_status,
        "by_author": stats.by_author,
        "monthly_trend": stats.monthly_trend,
        "avg_resolution_days": stats.avg_resolution_days,
    }
    reporter.save_json("feedback-stats.json", stats_dict)
    
    # 保存详细反馈数据
    feedback_dicts = [asdict(item) for item in feedback_items]
    reporter.save_json("feedback-details.json", feedback_dicts)
    
    print("\n" + "=" * 60)
    print("✅ 处理完成!")
    print(f"   📁 报告目录: {args.output_dir}")
    print(f"   📊 总计 Issue: {stats.total_issues}")
    print(f"   📂 待处理: {stats.open_issues}")
    print(f"   ✅ 已解决: {stats.closed_issues}")
    print("=" * 60)


if __name__ == "__main__":
    main()
