#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户反馈分析脚本
功能：自动分类反馈、提取关键词、生成趋势报告、优先级排序

使用方式：
    python feedback-analyzer.py --input issues.json --output report.html
    python feedback-analyzer.py --repo owner/repo --days 30

作者: AnalysisDataFlow Team
版本: 1.0.0
"""

import json
import re
import argparse
import datetime
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Any
import math

# 关键词库
KEYWORDS = {
    "bug": ["错误", "bug", "失效", "broken", "error", "不工作", "崩溃"],
    "feature": ["建议", "功能", "feature", "enhancement", "希望", "需要", "缺少"],
    "documentation": ["文档", "说明", "doc", "不清楚", "看不懂", "示例"],
    "performance": ["慢", "卡顿", "性能", "加载", "优化", "速度"],
    "usability": ["难用", "体验", "界面", "导航", "找不到", "困惑"],
}

# 情感词库
SENTIMENT_WORDS = {
    "positive": ["好", "优秀", "满意", "喜欢", " helpful", "good", "great", "excellent", "love", "perfect"],
    "negative": ["差", "糟糕", "失望", "难用", "bad", "terrible", "disappointed", "confusing", "poor", "worst"],
    "urgent": ["紧急", "严重", "立即", "urgent", "critical", "severe", "important", "asap"],
}

class FeedbackAnalyzer:
    """反馈分析器主类"""
    
    def __init__(self):
        self.feedbacks: List[Dict] = []
        self.analysis_results: Dict = {}
        
    def load_from_json(self, filepath: str) -> None:
        """从 JSON 文件加载反馈数据"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                self.feedbacks = data
            elif isinstance(data, dict) and 'issues' in data:
                self.feedbacks = data['issues']
            else:
                self.feedbacks = [data]
        print(f"✅ 已加载 {len(self.feedbacks)} 条反馈")
        
    def load_from_github_issues(self, repo: str, token: str = None, days: int = 30) -> None:
        """从 GitHub API 加载 Issues（模拟实现）"""
        # 实际使用时需要安装 requests 库并调用 GitHub API
        print(f"📡 从 GitHub 仓库 {repo} 获取最近 {days} 天的反馈...")
        # 这里简化处理，实际应该调用 GitHub API
        print("⚠️  模拟模式：请通过 --input 参数提供 JSON 文件")
        
    def classify_feedback(self, feedback: Dict) -> str:
        """自动分类单条反馈"""
        title = feedback.get('title', '').lower()
        body = feedback.get('body', '').lower()
        content = title + ' ' + body
        
        scores = {}
        for category, keywords in KEYWORDS.items():
            score = sum(1 for kw in keywords if kw.lower() in content)
            scores[category] = score
            
        # 检查标签
        labels = feedback.get('labels', [])
        label_names = [l.get('name', '').lower() if isinstance(l, dict) else l.lower() for l in labels]
        
        if 'bug' in label_names:
            return 'bug'
        elif 'enhancement' in label_names or 'feature' in label_names:
            return 'feature'
        elif 'documentation' in label_names or 'doc' in label_names:
            return 'documentation'
            
        # 根据关键词得分分类
        if scores:
            max_category = max(scores, key=scores.get)
            if scores[max_category] > 0:
                return max_category
                
        return 'other'
        
    def extract_keywords(self, feedback: Dict, top_n: int = 10) -> List[Tuple[str, int]]:
        """提取反馈中的关键词"""
        title = feedback.get('title', '')
        body = feedback.get('body', '')
        content = title + ' ' + body
        
        # 简单的中文分词（基于常见词汇）
        # 实际使用时可接入 jieba 等专业分词库
        words = re.findall(r'[\u4e00-\u9fa5]{2,}|[a-zA-Z]+', content.lower())
        
        # 过滤停用词
        stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', 'the', 'is', 'a', 'an', 'and', 'or'}
        filtered_words = [w for w in words if w not in stopwords and len(w) > 1]
        
        word_counts = Counter(filtered_words)
        return word_counts.most_common(top_n)
        
    def analyze_sentiment(self, feedback: Dict) -> Dict:
        """分析反馈情感倾向"""
        content = (feedback.get('title', '') + ' ' + feedback.get('body', '')).lower()
        
        sentiment = {
            'positive': 0,
            'negative': 0,
            'urgent': 0,
            'overall': 'neutral'
        }
        
        for word in SENTIMENT_WORDS['positive']:
            sentiment['positive'] += content.count(word.lower())
        for word in SENTIMENT_WORDS['negative']:
            sentiment['negative'] += content.count(word.lower())
        for word in SENTIMENT_WORDS['urgent']:
            sentiment['urgent'] += content.count(word.lower())
            
        # 判断整体情感
        if sentiment['positive'] > sentiment['negative']:
            sentiment['overall'] = 'positive'
        elif sentiment['negative'] > sentiment['positive']:
            sentiment['overall'] = 'negative'
            
        # 检测紧急程度
        sentiment['is_urgent'] = sentiment['urgent'] > 0
        
        return sentiment
        
    def calculate_priority(self, feedback: Dict) -> int:
        """计算反馈优先级分数 (0-100)"""
        score = 50  # 基础分
        
        # 情感分析加分
        sentiment = self.analyze_sentiment(feedback)
        if sentiment['is_urgent']:
            score += 30
        if sentiment['overall'] == 'negative':
            score += 10
            
        # 互动数据加分
        reactions = feedback.get('reactions', {})
        if isinstance(reactions, dict):
            thumbs_up = reactions.get('+1', 0) + reactions.get('thumbs_up', 0)
            score += min(thumbs_up * 2, 20)  # 最多加 20 分
            
        # 评论数量加分
        comments = feedback.get('comments', 0)
        score += min(comments * 3, 15)
        
        # 标签调整
        labels = feedback.get('labels', [])
        label_names = [l.get('name', '').lower() if isinstance(l, dict) else l.lower() for l in labels]
        if 'priority/p0' in label_names:
            score = 100
        elif 'priority/p1' in label_names:
            score = max(score, 80)
        elif 'bug' in label_names:
            score += 10
            
        # 时间衰减（越新的反馈优先级略高）
        created_at = feedback.get('created_at', '')
        if created_at:
            try:
                created_date = datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                days_old = (datetime.datetime.now(datetime.timezone.utc) - created_date).days
                score -= min(days_old, 10)  # 最多减 10 分
            except:
                pass
                
        return max(0, min(100, score))
        
    def analyze_all(self) -> Dict:
        """分析所有反馈"""
        print("🔍 开始分析反馈数据...")
        
        # 分类统计
        category_counts = defaultdict(int)
        sentiment_counts = defaultdict(int)
        keyword_counter = Counter()
        priority_scores = []
        daily_counts = defaultdict(int)
        
        detailed_results = []
        
        for feedback in self.feedbacks:
            # 分类
            category = self.classify_feedback(feedback)
            category_counts[category] += 1
            feedback['auto_category'] = category
            
            # 情感分析
            sentiment = self.analyze_sentiment(feedback)
            sentiment_counts[sentiment['overall']] += 1
            feedback['sentiment'] = sentiment
            
            # 关键词
            keywords = self.extract_keywords(feedback, top_n=5)
            for kw, count in keywords:
                keyword_counter[kw] += count
            feedback['keywords'] = keywords
            
            # 优先级
            priority = self.calculate_priority(feedback)
            priority_scores.append(priority)
            feedback['priority_score'] = priority
            
            # 日期统计
            created_at = feedback.get('created_at', '')
            if created_at:
                try:
                    date = created_at[:10]  # YYYY-MM-DD
                    daily_counts[date] += 1
                except:
                    pass
                    
            detailed_results.append(feedback)
            
        self.analysis_results = {
            'summary': {
                'total': len(self.feedbacks),
                'categories': dict(category_counts),
                'sentiments': dict(sentiment_counts),
                'avg_priority': sum(priority_scores) / len(priority_scores) if priority_scores else 0,
                'high_priority_count': sum(1 for p in priority_scores if p >= 70),
            },
            'top_keywords': keyword_counter.most_common(20),
            'daily_trend': dict(sorted(daily_counts.items())),
            'feedbacks': sorted(detailed_results, key=lambda x: x['priority_score'], reverse=True)
        }
        
        print("✅ 分析完成")
        return self.analysis_results
        
    def generate_text_report(self) -> str:
        """生成文本报告"""
        if not self.analysis_results:
            self.analyze_all()
            
        r = self.analysis_results
        s = r['summary']
        
        report = f"""
{'='*60}
           用户反馈分析报告
{'='*60}
生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 总体统计
{'-'*40}
总反馈数: {s['total']}
平均优先级: {s['avg_priority']:.1f}/100
高优先级反馈: {s['high_priority_count']} 条

📁 分类分布
{'-'*40}
"""
        for cat, count in s['categories'].items():
            percentage = count / s['total'] * 100
            report += f"  {cat:15s}: {count:3d} ({percentage:5.1f}%)\n"
            
        report += f"""
😊 情感分布
{'-'*40}
"""
        for sent, count in s['sentiments'].items():
            percentage = count / s['total'] * 100
            report += f"  {sent:10s}: {count:3d} ({percentage:5.1f}%)\n"
            
        report += f"""
🔥 热门关键词 TOP 10
{'-'*40}
"""
        for kw, count in r['top_keywords'][:10]:
            report += f"  {kw:15s}: {count:3d}\n"
            
        report += f"""
⚠️  高优先级反馈 TOP 5
{'-'*40}
"""
        high_priority = [f for f in r['feedbacks'] if f['priority_score'] >= 70][:5]
        for i, f in enumerate(high_priority, 1):
            title = f.get('title', '无标题')[:40]
            report += f"  {i}. [{f['priority_score']:02d}] {title}\n"
            
        report += f"""
{'='*60}
                 报告结束
{'='*60}
"""
        return report
        
    def generate_html_report(self, output_path: str) -> None:
        """生成 HTML 报告"""
        if not self.analysis_results:
            self.analyze_all()
            
        r = self.analysis_results
        s = r['summary']
        
        # 生成分类图表数据
        category_data = json.dumps([{'name': k, 'value': v} for k, v in s['categories'].items()])
        sentiment_data = json.dumps([{'name': k, 'value': v} for k, v in s['sentiments'].items()])
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>用户反馈分析报告</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
        .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stat-card h3 {{ color: #666; font-size: 0.9em; margin-bottom: 10px; }}
        .stat-card .value {{ font-size: 2em; font-weight: bold; color: #333; }}
        .chart-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; margin-bottom: 20px; }}
        .chart-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .chart-card h3 {{ margin-bottom: 15px; color: #333; }}
        .feedback-list {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .feedback-list h3 {{ margin-bottom: 15px; color: #333; }}
        .feedback-item {{ padding: 15px; border-bottom: 1px solid #eee; }}
        .feedback-item:last-child {{ border-bottom: none; }}
        .priority-badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.8em; margin-right: 10px; }}
        .priority-high {{ background: #ffebee; color: #c62828; }}
        .priority-medium {{ background: #fff3e0; color: #ef6c00; }}
        .priority-low {{ background: #e8f5e9; color: #2e7d32; }}
        .category-tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.75em; background: #e3f2fd; color: #1565c0; margin-right: 5px; }}
        .keywords {{ margin-top: 8px; font-size: 0.85em; color: #666; }}
        .keyword-tag {{ display: inline-block; padding: 2px 6px; background: #f5f5f5; border-radius: 3px; margin-right: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 用户反馈分析报告</h1>
            <p>生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>总反馈数</h3>
                <div class="value">{s['total']}</div>
            </div>
            <div class="stat-card">
                <h3>平均优先级</h3>
                <div class="value">{s['avg_priority']:.1f}</div>
            </div>
            <div class="stat-card">
                <h3>高优先级反馈</h3>
                <div class="value">{s['high_priority_count']}</div>
            </div>
            <div class="stat-card">
                <h3>正面情感占比</h3>
                <div class="value">{s['sentiments'].get('positive', 0) / s['total'] * 100:.1f}%</div>
            </div>
        </div>
        
        <div class="chart-grid">
            <div class="chart-card">
                <h3>📁 反馈分类分布</h3>
                <canvas id="categoryChart"></canvas>
            </div>
            <div class="chart-card">
                <h3>😊 情感分布</h3>
                <canvas id="sentimentChart"></canvas>
            </div>
        </div>
        
        <div class="feedback-list">
            <h3>⚠️ 高优先级反馈（Top 10）</h3>
"""
        
        # 添加高优先级反馈列表
        high_priority = [f for f in r['feedbacks'] if f['priority_score'] >= 50][:10]
        for f in high_priority:
            priority_class = 'priority-high' if f['priority_score'] >= 70 else 'priority-medium' if f['priority_score'] >= 50 else 'priority-low'
            keywords_html = ''.join([f'<span class="keyword-tag">{kw}</span>' for kw, _ in f.get('keywords', [])[:5]])
            html += f"""
            <div class="feedback-item">
                <span class="priority-badge {priority_class}">{f['priority_score']}分</span>
                <span class="category-tag">{f.get('auto_category', 'other')}</span>
                <strong>{f.get('title', '无标题')}</strong>
                <div class="keywords">关键词: {keywords_html}</div>
            </div>
"""
        
        html += f"""
        </div>
    </div>
    
    <script>
        // 分类饼图
        new Chart(document.getElementById('categoryChart'), {{
            type: 'doughnut',
            data: {{
                labels: {list(s['categories'].keys())},
                datasets: [{{
                    data: {list(s['categories'].values())},
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
                }}]
            }}
        }});
        
        // 情感饼图
        new Chart(document.getElementById('sentimentChart'), {{
            type: 'pie',
            data: {{
                labels: {list(s['sentiments'].keys())},
                datasets: [{{
                    data: {list(s['sentiments'].values())},
                    backgroundColor: ['#4CAF50', '#FFC107', '#F44336']
                }}]
            }}
        }});
    </script>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ HTML 报告已保存: {output_path}")
        
    def export_to_json(self, output_path: str) -> None:
        """导出分析结果为 JSON"""
        if not self.analysis_results:
            self.analyze_all()
            
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON 数据已导出: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='用户反馈分析工具')
    parser.add_argument('--input', '-i', help='输入 JSON 文件路径')
    parser.add_argument('--output', '-o', help='输出报告路径')
    parser.add_argument('--format', '-f', choices=['text', 'html', 'json'], default='text', help='输出格式')
    parser.add_argument('--repo', '-r', help='GitHub 仓库 (owner/repo)')
    parser.add_argument('--days', '-d', type=int, default=30, help='分析最近 N 天的反馈')
    
    args = parser.parse_args()
    
    analyzer = FeedbackAnalyzer()
    
    # 加载数据
    if args.input:
        analyzer.load_from_json(args.input)
    elif args.repo:
        analyzer.load_from_github_issues(args.repo, days=args.days)
    else:
        print("❌ 请提供 --input 或 --repo 参数")
        parser.print_help()
        return
        
    # 执行分析
    analyzer.analyze_all()
    
    # 生成报告
    if args.format == 'text':
        report = analyzer.generate_text_report()
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ 报告已保存: {args.output}")
        else:
            print(report)
    elif args.format == 'html':
        output_path = args.output or 'feedback-report.html'
        analyzer.generate_html_report(output_path)
    elif args.format == 'json':
        output_path = args.output or 'feedback-analysis.json'
        analyzer.export_to_json(output_path)


if __name__ == '__main__':
    main()
