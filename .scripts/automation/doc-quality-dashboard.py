#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档质量仪表板生成器 (Document Quality Dashboard)

功能：
- 聚合各工具的检查结果
- 生成HTML质量仪表板
- 计算质量评分
- 趋势分析（历史对比）
- 生成改进建议
- 集成：GitHub Actions报告

作者: Automation Agent
版本: 1.0.0
"""

import re
import json
import argparse
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, Any
from datetime import datetime, timedelta
from collections import defaultdict
import math

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class QualityMetric:
    """质量指标"""
    name: str
    score: float  # 0-100
    weight: float
    details: Dict[str, Any] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)


@dataclass
class FileQuality:
    """文件质量信息"""
    file_path: str
    overall_score: float
    metrics: List[QualityMetric]
    issues_count: int = 0
    warnings_count: int = 0
    last_modified: Optional[datetime] = None


@dataclass
class TrendData:
    """趋势数据"""
    timestamp: datetime
    overall_score: float
    total_issues: int
    valid_files: int
    total_files: int


@dataclass
class DashboardData:
    """仪表板数据"""
    generated_at: datetime
    overall_score: float
    total_files: int
    valid_files: int
    total_issues: int
    total_warnings: int
    metrics_summary: Dict[str, float]
    file_qualities: List[FileQuality]
    trends: List[TrendData]
    recommendations: List[str]


class QualityDashboardGenerator:
    """质量仪表板生成器"""
    
    # 权重配置
    DEFAULT_WEIGHTS = {
        'cross_ref': 0.25,      # 交叉引用完整性
        'template': 0.25,       # 模板合规性
        'formal_element': 0.20, # 形式化元素规范
        'mermaid': 0.15,        # Mermaid语法
        'readability': 0.15,    # 可读性
    }
    
    def __init__(
        self,
        root_dir: Path,
        reports_dir: Path,
        history_file: Optional[Path] = None,
        weights: Optional[Dict[str, float]] = None
    ):
        """
        初始化生成器
        
        Args:
            root_dir: 项目根目录
            reports_dir: 报告目录
            history_file: 历史数据文件
            weights: 指标权重配置
        """
        self.root_dir = Path(root_dir).resolve()
        self.reports_dir = Path(reports_dir).resolve()
        self.history_file = history_file or self.root_dir / '.quality-history.json'
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()
        
    def _load_report(self, report_name: str) -> Optional[Dict]:
        """加载报告文件"""
        # 查找最新的报告
        pattern = f"{report_name}-*.json"
        reports = sorted(self.reports_dir.glob(pattern))
        
        if reports:
            latest = reports[-1]
            try:
                with open(latest, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"加载报告失败 {latest}: {e}")
                
        return None
        
    def _calculate_cross_ref_score(self, report: Optional[Dict]) -> QualityMetric:
        """计算交叉引用分数"""
        if not report:
            return QualityMetric(
                name="交叉引用",
                score=0,
                weight=self.weights['cross_ref'],
                issues=["无法加载交叉引用报告"]
            )
            
        summary = report.get('summary', {})
        total = summary.get('total_links', 1)
        valid = summary.get('valid_links', 0)
        invalid = summary.get('invalid_links', 0)
        errors = summary.get('error_links', 0)
        
        score = max(0, (valid / total * 100) - (invalid + errors) * 5)
        
        issues = []
        if invalid > 0:
            issues.append(f"{invalid} 个无效链接")
        if errors > 0:
            issues.append(f"{errors} 个链接错误")
            
        return QualityMetric(
            name="交叉引用",
            score=min(100, score),
            weight=self.weights['cross_ref'],
            details=summary,
            issues=issues
        )
        
    def _calculate_template_score(self, report: Optional[Dict]) -> QualityMetric:
        """计算模板合规分数"""
        if not report:
            return QualityMetric(
                name="模板合规",
                score=0,
                weight=self.weights['template'],
                issues=["无法加载模板验证报告"]
            )
            
        summary = report.get('summary', {})
        total = summary.get('total_files', 1)
        valid = summary.get('valid_files', 0)
        errors = summary.get('total_errors', 0)
        warnings = summary.get('total_warnings', 0)
        avg_score = summary.get('average_score', 0)
        
        score = avg_score if avg_score else (valid / total * 100)
        
        issues = []
        if errors > 0:
            issues.append(f"{errors} 个错误")
        if warnings > 0:
            issues.append(f"{warnings} 个警告")
            
        return QualityMetric(
            name="模板合规",
            score=score,
            weight=self.weights['template'],
            details=summary,
            issues=issues
        )
        
    def _calculate_formal_element_score(self, report: Optional[Dict]) -> QualityMetric:
        """计算形式化元素分数"""
        if not report:
            return QualityMetric(
                name="形式化元素",
                score=0,
                weight=self.weights['formal_element'],
                issues=["无法加载形式化元素报告"]
            )
            
        statistics = report.get('statistics', {})
        conflicts = report.get('conflicts', [])
        
        total_elements = statistics.get('total_unique_elements', 0)
        
        # 基于冲突数量计算分数
        conflict_penalty = len(conflicts) * 5
        score = max(0, 100 - conflict_penalty)
        
        issues = []
        for conflict in conflicts[:5]:
            issues.append(conflict.get('message', '未知冲突'))
            
        return QualityMetric(
            name="形式化元素",
            score=score,
            weight=self.weights['formal_element'],
            details=statistics,
            issues=issues
        )
        
    def _calculate_mermaid_score(self, report: Optional[Dict]) -> QualityMetric:
        """计算Mermaid分数"""
        if not report:
            return QualityMetric(
                name="Mermaid图表",
                score=0,
                weight=self.weights['mermaid'],
                issues=["无法加载Mermaid检查报告"]
            )
            
        summary = report.get('summary', {})
        total = summary.get('total_blocks', 1)
        valid = summary.get('valid_blocks', 0)
        errors = summary.get('errors_by_type', {})
        
        score = valid / total * 100 if total > 0 else 0
        
        issues = []
        for error_type, count in errors.items():
            issues.append(f"{error_type}: {count}")
            
        return QualityMetric(
            name="Mermaid图表",
            score=score,
            weight=self.weights['mermaid'],
            details=summary,
            issues=issues
        )
        
    def _calculate_readability_score(self, file_path: Path) -> QualityMetric:
        """计算可读性分数（基于文件统计）"""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # 基本统计
            total_lines = len(lines)
            non_empty_lines = len([l for l in lines if l.strip()])
            
            # 计算平均行长度
            line_lengths = [len(l) for l in lines if l.strip()]
            avg_line_length = sum(line_lengths) / len(line_lengths) if line_lengths else 0
            
            # 长行数量
            long_lines = len([l for l in line_lengths if l > 120])
            
            # 计算分数
            score = 100
            
            # 空行比例检查
            if total_lines > 0:
                empty_ratio = (total_lines - non_empty_lines) / total_lines
                if empty_ratio > 0.3:
                    score -= 10
                    
            # 长行惩罚
            score -= long_lines * 2
            
            issues = []
            if long_lines > 0:
                issues.append(f"{long_lines} 行超过120字符")
                
            return QualityMetric(
                name="可读性",
                score=max(0, score),
                weight=self.weights['readability'],
                details={
                    'total_lines': total_lines,
                    'avg_line_length': round(avg_line_length, 1),
                    'long_lines': long_lines
                },
                issues=issues
            )
            
        except Exception as e:
            return QualityMetric(
                name="可读性",
                score=0,
                weight=self.weights['readability'],
                issues=[f"无法计算: {e}"]
            )
            
    def aggregate_data(self) -> DashboardData:
        """聚合所有数据"""
        logger.info("开始聚合质量数据...")
        
        # 加载各工具报告
        cross_ref_report = self._load_report('cross-ref-report')
        template_report = self._load_report('template-validation')
        formal_report = self._load_report('formal-elements')
        mermaid_report = self._load_report('mermaid-check')
        
        # 计算各项指标
        metrics_list = [
            self._calculate_cross_ref_score(cross_ref_report),
            self._calculate_template_score(template_report),
            self._calculate_formal_element_score(formal_report),
            self._calculate_mermaid_score(mermaid_report),
        ]
        
        # 获取文件列表
        md_files = list(self.root_dir.glob('**/*.md'))
        md_files = [f for f in md_files if '.git' not in str(f)]
        
        # 计算每个文件的质量
        file_qualities: List[FileQuality] = []
        
        for file_path in md_files[:100]:  # 限制处理文件数
            rel_path = str(file_path.relative_to(self.root_dir))
            
            # 文件特定指标
            readability = self._calculate_readability_score(file_path)
            
            file_metrics = metrics_list + [readability]
            
            # 计算加权分数
            total_weight = sum(m.weight for m in file_metrics)
            overall_score = sum(m.score * m.weight for m in file_metrics) / total_weight if total_weight > 0 else 0
            
            issues_count = sum(len(m.issues) for m in file_metrics)
            
            file_qualities.append(FileQuality(
                file_path=rel_path,
                overall_score=round(overall_score, 2),
                metrics=file_metrics,
                issues_count=issues_count
            ))
            
        # 计算总体分数
        total_weight = sum(m.weight for m in metrics_list)
        overall_score = sum(m.score * m.weight for m in metrics_list) / total_weight if total_weight > 0 else 0
        
        # 计算汇总
        total_files = len(md_files)
        valid_files = sum(1 for fq in file_qualities if fq.overall_score >= 80)
        total_issues = sum(fq.issues_count for fq in file_qualities)
        total_warnings = sum(len([m for m in fq.metrics if m.issues]) for fq in file_qualities)
        
        # 指标摘要
        metrics_summary = {m.name: round(m.score, 2) for m in metrics_list}
        
        # 加载趋势数据
        trends = self._load_trends()
        
        # 生成建议
        recommendations = self._generate_recommendations(metrics_list, file_qualities)
        
        return DashboardData(
            generated_at=datetime.now(),
            overall_score=round(overall_score, 2),
            total_files=total_files,
            valid_files=valid_files,
            total_issues=total_issues,
            total_warnings=total_warnings,
            metrics_summary=metrics_summary,
            file_qualities=sorted(file_qualities, key=lambda x: x.overall_score)[:50],
            trends=trends,
            recommendations=recommendations
        )
        
    def _load_trends(self) -> List[TrendData]:
        """加载历史趋势数据"""
        trends = []
        
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    
                for entry in history[-30:]:  # 最近30条
                    trends.append(TrendData(
                        timestamp=datetime.fromisoformat(entry['timestamp']),
                        overall_score=entry.get('overall_score', 0),
                        total_issues=entry.get('total_issues', 0),
                        valid_files=entry.get('valid_files', 0),
                        total_files=entry.get('total_files', 1)
                    ))
            except Exception as e:
                logger.warning(f"加载历史数据失败: {e}")
                
        return trends
        
    def _save_trend(self, data: DashboardData) -> None:
        """保存当前数据到历史记录"""
        history = []
        
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except:
                pass
                
        entry = {
            'timestamp': data.generated_at.isoformat(),
            'overall_score': data.overall_score,
            'total_issues': data.total_issues,
            'valid_files': data.valid_files,
            'total_files': data.total_files
        }
        
        history.append(entry)
        
        # 只保留最近90条
        history = history[-90:]
        
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存历史数据失败: {e}")
            
    def _generate_recommendations(
        self,
        metrics: List[QualityMetric],
        file_qualities: List[FileQuality]
    ) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于低分指标生成建议
        for metric in metrics:
            if metric.score < 60:
                recommendations.append(
                    f"🔴 **{metric.name}**需要立即改进 (得分: {metric.score:.1f})"
                )
            elif metric.score < 80:
                recommendations.append(
                    f"🟡 **{metric.name}**有提升空间 (得分: {metric.score:.1f})"
                )
                
        # 找出问题最多的文件
        problematic_files = sorted(
            file_qualities,
            key=lambda x: x.issues_count,
            reverse=True
        )[:5]
        
        if problematic_files and problematic_files[0].issues_count > 0:
            recommendations.append(
                f"📁 重点关注以下文件: {', '.join(f.file_path for f in problematic_files[:3])}"
            )
            
        # 通用建议
        if not any('交叉引用' in r for r in recommendations):
            recommendations.append("✅ 交叉引用维护良好，继续保持")
            
        if not any('模板' in r for r in recommendations):
            recommendations.append("✅ 模板合规性良好，继续保持")
            
        return recommendations
        
    def generate_html_dashboard(self, data: DashboardData, output_path: Path) -> None:
        """生成HTML仪表板"""
        # 趋势数据JSON
        trend_labels = [t.timestamp.strftime('%m-%d') for t in data.trends]
        trend_scores = [t.overall_score for t in data.trends]
        trend_issues = [t.total_issues for t in data.trends]
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文档质量仪表板</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --primary: #2196F3;
            --success: #4CAF50;
            --warning: #FF9800;
            --danger: #f44336;
            --bg: #f5f5f5;
            --card-bg: #ffffff;
            --text: #333333;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }}
        .header h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
        .header p {{ opacity: 0.9; }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}
        .score-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        .score-card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.2s;
        }}
        .score-card:hover {{ transform: translateY(-4px); }}
        .score-value {{
            font-size: 3rem;
            font-weight: bold;
            margin: 1rem 0;
        }}
        .score-excellent {{ color: var(--success); }}
        .score-good {{ color: var(--primary); }}
        .score-warning {{ color: var(--warning); }}
        .score-poor {{ color: var(--danger); }}
        .score-label {{ color: #666; font-size: 0.9rem; }}
        .section {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            font-size: 1.25rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--bg);
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }}
        .metric-item {{
            padding: 1rem;
            background: var(--bg);
            border-radius: 8px;
        }}
        .metric-name {{ font-size: 0.9rem; color: #666; }}
        .metric-value {{
            font-size: 1.5rem;
            font-weight: bold;
            margin-top: 0.5rem;
        }}
        .chart-container {{
            position: relative;
            height: 300px;
            margin: 1rem 0;
        }}
        .file-list {{
            max-height: 400px;
            overflow-y: auto;
        }}
        .file-item {{
            display: flex;
            align-items: center;
            padding: 0.75rem;
            border-bottom: 1px solid var(--bg);
        }}
        .file-item:last-child {{ border-bottom: none; }}
        .file-score {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 1rem;
            flex-shrink: 0;
        }}
        .file-path {{ flex: 1; font-size: 0.9rem; }}
        .file-issues {{ color: #666; font-size: 0.85rem; }}
        .recommendations {{
            list-style: none;
        }}
        .recommendations li {{
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            background: var(--bg);
            border-radius: 8px;
            border-left: 4px solid var(--primary);
        }}
        .status-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        .status-good {{ background: #e8f5e9; color: #2e7d32; }}
        .status-warning {{ background: #fff3e0; color: #ef6c00; }}
        .status-bad {{ background: #ffebee; color: #c62828; }}
        .footer {{
            text-align: center;
            padding: 2rem;
            color: #666;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 文档质量仪表板</h1>
        <p>生成时间: {data.generated_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="container">
        <!-- 总体评分 -->
        <div class="score-grid">
            <div class="score-card">
                <div class="score-label">总体质量评分</div>
                <div class="score-value {self._get_score_class(data.overall_score)}">
                    {data.overall_score:.1f}
                </div>
                <span class="status-badge {self._get_status_class(data.overall_score)}">
                    {self._get_status_text(data.overall_score)}
                </span>
            </div>
            <div class="score-card">
                <div class="score-label">文件总数</div>
                <div class="score-value score-good">{data.total_files}</div>
                <div class="file-issues">有效文件: {data.valid_files}</div>
            </div>
            <div class="score-card">
                <div class="score-label">问题总数</div>
                <div class="score-value {self._get_score_class(100 - min(100, data.total_issues))}">
                    {data.total_issues}
                </div>
                <div class="file-issues">警告: {data.total_warnings}</div>
            </div>
            <div class="score-card">
                <div class="score-label">合规率</div>
                <div class="score-value {self._get_score_class(data.valid_files / data.total_files * 100 if data.total_files > 0 else 0)}">
                    {data.valid_files / data.total_files * 100:.1f}%
                </div>
                <div class="file-issues">{data.valid_files}/{data.total_files} 文件</div>
            </div>
        </div>
        
        <!-- 指标详情 -->
        <div class="section">
            <h2>📈 质量指标详情</h2>
            <div class="metric-grid">
                {self._generate_metric_items(data.metrics_summary)}
            </div>
        </div>
        
        <!-- 趋势图表 -->
        <div class="section">
            <h2>📉 质量趋势</h2>
            <div class="chart-container">
                <canvas id="trendChart"></canvas>
            </div>
        </div>
        
        <!-- 文件质量排行 -->
        <div class="section">
            <h2>📁 文件质量排行（得分最低）</h2>
            <div class="file-list">
                {self._generate_file_list(data.file_qualities)}
            </div>
        </div>
        
        <!-- 改进建议 -->
        <div class="section">
            <h2>💡 改进建议</h2>
            <ul class="recommendations">
                {''.join(f'<li>{r}</li>' for r in data.recommendations)}
            </ul>
        </div>
    </div>
    
    <div class="footer">
        <p>由 doc-quality-dashboard.py 自动生成</p>
    </div>
    
    <script>
        // 趋势图表
        const ctx = document.getElementById('trendChart').getContext('2d');
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(trend_labels)},
                datasets: [{{
                    label: '总体评分',
                    data: {json.dumps(trend_scores)},
                    borderColor: '#2196F3',
                    backgroundColor: 'rgba(33, 150, 243, 0.1)',
                    tension: 0.4,
                    fill: true
                }}, {{
                    label: '问题数',
                    data: {json.dumps(trend_issues)},
                    borderColor: '#f44336',
                    backgroundColor: 'rgba(244, 67, 54, 0.1)',
                    tension: 0.4,
                    yAxisID: 'y1'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {{
                    mode: 'index',
                    intersect: false,
                }},
                scales: {{
                    y: {{
                        type: 'linear',
                        display: true,
                        position: 'left',
                        min: 0,
                        max: 100
                    }},
                    y1: {{
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: {{
                            drawOnChartArea: false,
                        }},
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>'''
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
            
        logger.info(f"HTML仪表板已生成: {output_path}")
        
    def _get_score_class(self, score: float) -> str:
        """获取分数对应的CSS类"""
        if score >= 90:
            return 'score-excellent'
        elif score >= 75:
            return 'score-good'
        elif score >= 60:
            return 'score-warning'
        else:
            return 'score-poor'
            
    def _get_status_class(self, score: float) -> str:
        """获取状态对应的CSS类"""
        if score >= 80:
            return 'status-good'
        elif score >= 60:
            return 'status-warning'
        else:
            return 'status-bad'
            
    def _get_status_text(self, score: float) -> str:
        """获取状态文本"""
        if score >= 90:
            return '优秀'
        elif score >= 75:
            return '良好'
        elif score >= 60:
            return '及格'
        else:
            return '需改进'
            
    def _generate_metric_items(self, metrics: Dict[str, float]) -> str:
        """生成指标项HTML"""
        items = []
        for name, score in metrics.items():
            score_class = self._get_score_class(score)
            items.append(f'''
                <div class="metric-item">
                    <div class="metric-name">{name}</div>
                    <div class="metric-value {score_class}">{score:.1f}</div>
                </div>
            ''')
        return ''.join(items)
        
    def _generate_file_list(self, files: List[FileQuality]) -> str:
        """生成文件列表HTML"""
        items = []
        for file in files[:20]:  # 最多显示20个
            score_class = self._get_score_class(file.overall_score)
            items.append(f'''
                <div class="file-item">
                    <div class="file-score {score_class}">{file.overall_score:.0f}</div>
                    <div class="file-path">{file.file_path}</div>
                    <div class="file-issues">{file.issues_count} 问题</div>
                </div>
            ''')
        return ''.join(items)
        
    def generate_github_actions_output(self, data: DashboardData, output_path: Path) -> None:
        """生成GitHub Actions输出"""
        lines = [
            "# 文档质量检查报告",
            "",
            f"**检查时间**: {data.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 质量评分",
            "",
            f"| 指标 | 得分 | 状态 |",
            f"|------|------|------|",
            f"| 总体评分 | {data.overall_score:.1f} | {self._get_status_text(data.overall_score)} |",
        ]
        
        for name, score in data.metrics_summary.items():
            lines.append(f"| {name} | {score:.1f} | {self._get_status_text(score)} |")
            
        lines.extend([
            "",
            "## 统计摘要",
            "",
            f"- **文件总数**: {data.total_files}",
            f"- **有效文件**: {data.valid_files} ({data.valid_files / data.total_files * 100:.1f}%)",
            f"- **问题总数**: {data.total_issues}",
            f"- **警告总数**: {data.total_warnings}",
            "",
            "## 改进建议",
            "",
        ])
        
        for rec in data.recommendations:
            lines.append(f"- {rec}")
            
        lines.extend([
            "",
            "---",
            "*由 doc-quality-dashboard.py 自动生成*",
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
            
        logger.info(f"GitHub Actions报告已生成: {output_path}")
        
        # 同时设置GitHub Actions输出变量
        github_output = Path(os.environ.get('GITHUB_OUTPUT', '/dev/null'))
        if github_output.exists():
            with open(github_output, 'a', encoding='utf-8') as f:
                f.write(f"quality_score={data.overall_score:.1f}\n")
                f.write(f"valid_files={data.valid_files}\n")
                f.write(f"total_files={data.total_files}\n")
                f.write(f"total_issues={data.total_issues}\n")
                
                # 判断质量是否通过
                passed = data.overall_score >= 60 and data.total_issues < 100
                f.write(f"quality_passed={'true' if passed else 'false'}\n")


import os


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='文档质量仪表板生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                           # 生成仪表板
  %(prog)s -d . -r ./reports         # 指定目录和报告位置
  %(prog)s --github-actions          # 生成GitHub Actions报告
        """
    )
    
    parser.add_argument(
        '-d', '--directory',
        type=str,
        default='.',
        help='项目根目录 (默认: 当前目录)'
    )
    
    parser.add_argument(
        '-r', '--reports-dir',
        type=str,
        default='./reports',
        help='报告目录 (默认: ./reports)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='./quality-dashboard.html',
        help='输出文件路径 (默认: ./quality-dashboard.html)'
    )
    
    parser.add_argument(
        '--github-actions',
        action='store_true',
        help='生成GitHub Actions报告格式'
    )
    
    parser.add_argument(
        '--save-history',
        action='store_true',
        default=True,
        help='保存历史数据用于趋势分析'
    )
    
    args = parser.parse_args()
    
    # 创建生成器
    generator = QualityDashboardGenerator(
        root_dir=Path(args.directory).resolve(),
        reports_dir=Path(args.reports_dir).resolve()
    )
    
    # 聚合数据
    data = generator.aggregate_data()
    
    # 保存历史
    if args.save_history:
        generator._save_trend(data)
        
    # 生成输出
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.github_actions:
        generator.generate_github_actions_output(data, output_path)
    else:
        generator.generate_html_dashboard(data, output_path)
        
    # 输出摘要
    print(f"\n{'='*60}")
    print("文档质量仪表板生成完成")
    print(f"{'='*60}")
    print(f"总体评分: {data.overall_score:.1f}/100 ({generator._get_status_text(data.overall_score)})")
    print(f"文件统计: {data.valid_files}/{data.total_files} 有效")
    print(f"问题统计: {data.total_issues} 问题, {data.total_warnings} 警告")
    print(f"{'='*60}")
    print(f"仪表板已保存至: {output_path}")
    
    # 返回退出码
    return 0 if data.overall_score >= 60 else 1


if __name__ == '__main__':
    exit(main())
