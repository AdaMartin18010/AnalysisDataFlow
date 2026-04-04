#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目健康检查仪表盘 - AnalysisDataFlow 自动化工具集

功能：
1. 综合检查所有健康指标（文档、链接、定理、Mermaid等）
2. 生成仪表盘数据（JSON格式）
3. 支持趋势分析和历史对比
4. 提供可执行的改进建议

使用方法：
    python .scripts/health_check_dashboard.py
    python .scripts/health_check_dashboard.py --json
    python .scripts/health_check_dashboard.py --save
    python .scripts/health_check_dashboard.py --trend

退出码：
    0 - 健康状态良好
    1 - 发现需要关注的问题
    2 - 运行异常
"""

import os
import re
import sys
import json
import argparse
import subprocess
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict


@dataclass
class HealthMetric:
    """健康指标数据类"""
    name: str
    status: str  # healthy, warning, critical
    score: float  # 0-100
    value: any
    threshold: any
    message: str
    details: Dict = field(default_factory=dict)


@dataclass
class HealthReport:
    """健康报告数据类"""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    overall_score: float = 0.0
    overall_status: str = "unknown"  # healthy, warning, critical
    metrics: List[HealthMetric] = field(default_factory=list)
    issues: List[Dict] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    trends: Dict = field(default_factory=dict)


class HealthDashboard:
    """健康检查仪表盘"""
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.report = HealthReport()
        self.history_file = self.root_dir / '.stats' / 'health_history.json'
        self.markdown_files: List[Path] = []
        
    def collect_files(self) -> None:
        """收集所有 Markdown 文件"""
        for pattern in ['**/*.md']:
            for file_path in self.root_dir.glob(pattern):
                if '.git' not in str(file_path):
                    self.markdown_files.append(file_path)
    
    def check_document_coverage(self) -> HealthMetric:
        """检查文档覆盖率"""
        required_docs = [
            'README.md', 'AGENTS.md', 'PROJECT-TRACKING.md',
            'THEOREM-REGISTRY.md', 'STATISTICS-REPORT.md',
            'CHANGELOG.md', 'ROADMAP.md'
        ]
        
        found = []
        missing = []
        
        for doc in required_docs:
            if (self.root_dir / doc).exists():
                found.append(doc)
            else:
                missing.append(doc)
        
        score = len(found) / len(required_docs) * 100
        
        if missing:
            status = 'warning' if score >= 80 else 'critical'
            message = f"缺少 {len(missing)} 个核心文档"
        else:
            status = 'healthy'
            message = "所有核心文档已就位"
        
        return HealthMetric(
            name='document_coverage',
            status=status,
            score=score,
            value={'found': found, 'missing': missing},
            threshold={'required': required_docs},
            message=message,
            details={'found_count': len(found), 'missing_count': len(missing)}
        )
    
    def check_theorem_registry_sync(self) -> HealthMetric:
        """检查定理注册表同步状态"""
        registry_path = self.root_dir / 'THEOREM-REGISTRY.md'
        
        if not registry_path.exists():
            return HealthMetric(
                name='theorem_registry_sync',
                status='critical',
                score=0,
                value={'error': 'registry_not_found'},
                threshold={'max_desync': 0},
                message='THEOREM-REGISTRY.md 不存在'
            )
        
        try:
            # 扫描文档中的定理
            doc_theorems = set()
            registry_theorems = set()
            
            theorem_pattern = re.compile(
                r'\*\*(Thm|Lemma|Def|Prop|Cor)-([SFK])-(\d{1,2})-(\d{1,3}[a-zA-Z]?)\*\*',
                re.IGNORECASE
            )
            
            for file_path in self.markdown_files:
                if file_path.name == 'THEOREM-REGISTRY.md':
                    content = file_path.read_text(encoding='utf-8')
                    for match in theorem_pattern.finditer(content):
                        registry_theorems.add(match.group(0))
                elif any(str(file_path).startswith(str(self.root_dir / d)) for d in ['Struct', 'Knowledge', 'Flink']):
                    content = file_path.read_text(encoding='utf-8')
                    for match in theorem_pattern.finditer(content):
                        doc_theorems.add(match.group(0))
            
            only_in_docs = doc_theorems - registry_theorems
            only_in_registry = registry_theorems - doc_theorems
            
            total = len(doc_theorems | registry_theorems)
            synced = len(doc_theorems & registry_theorems)
            
            score = (synced / total * 100) if total > 0 else 100
            
            if only_in_docs or only_in_registry:
                status = 'warning' if score >= 95 else 'critical'
                message = f"同步率 {score:.1f}%: {len(only_in_docs)} 个未注册, {len(only_in_registry)} 个已删除"
            else:
                status = 'healthy'
                message = "定理注册表与文档完全同步"
            
            return HealthMetric(
                name='theorem_registry_sync',
                status=status,
                score=score,
                value={
                    'doc_count': len(doc_theorems),
                    'registry_count': len(registry_theorems),
                    'synced': synced,
                    'only_in_docs': list(only_in_docs)[:10],
                    'only_in_registry': list(only_in_registry)[:10]
                },
                threshold={'min_sync_rate': 95},
                message=message
            )
        
        except Exception as e:
            return HealthMetric(
                name='theorem_registry_sync',
                status='critical',
                score=0,
                value={'error': str(e)},
                threshold={'min_sync_rate': 95},
                message=f'检查失败: {e}'
            )
    
    def check_link_health(self) -> HealthMetric:
        """检查链接健康状态"""
        # 运行交叉引用验证脚本
        try:
            result = subprocess.run(
                [sys.executable, str(self.root_dir / '.scripts' / 'validate_cross_refs.py')],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # 解析结果
            report_path = self.root_dir / '.stats' / 'cross_ref_report.json'
            if report_path.exists():
                with open(report_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                total_errors = data.get('summary', {}).get('total_errors', 0)
                total_links = data.get('summary', {}).get('total_links', 1)
                
                error_rate = total_errors / total_links if total_links > 0 else 0
                score = max(0, 100 - error_rate * 100)
                
                if total_errors == 0:
                    status = 'healthy'
                    message = '所有链接有效'
                elif total_errors < 10:
                    status = 'warning'
                    message = f'发现 {total_errors} 个无效链接'
                else:
                    status = 'critical'
                    message = f'发现 {total_errors} 个无效链接，需要修复'
                
                return HealthMetric(
                    name='link_health',
                    status=status,
                    score=score,
                    value={'errors': total_errors, 'total': total_links},
                    threshold={'max_errors': 10},
                    message=message
                )
        
        except Exception as e:
            pass
        
        # 如果脚本运行失败，进行基本检查
        return self._basic_link_check()
    
    def _basic_link_check(self) -> HealthMetric:
        """基本链接检查"""
        link_pattern = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
        broken_links = 0
        total_links = 0
        
        md_files_set = {str(f.relative_to(self.root_dir)).replace('\\', '/') for f in self.markdown_files}
        
        for file_path in self.markdown_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                for match in link_pattern.finditer(content):
                    link_url = match.group(2)
                    
                    # 跳过外部链接
                    if link_url.startswith(('http://', 'https://', 'mailto:')):
                        continue
                    
                    total_links += 1
                    
                    # 检查内部链接
                    if not link_url.startswith('#'):
                        rel_path = str(file_path.relative_to(self.root_dir)).replace('\\', '/')
                        source_dir = os.path.dirname(rel_path)
                        
                        if link_url.startswith('/'):
                            target = link_url[1:]
                        else:
                            target = os.path.normpath(os.path.join(source_dir, link_url)).replace('\\', '/')
                        
                        if target not in md_files_set and target + '.md' not in md_files_set:
                            broken_links += 1
            
            except Exception:
                pass
        
        score = max(0, 100 - broken_links / max(total_links, 1) * 100)
        
        if broken_links == 0:
            status = 'healthy'
            message = '所有内部链接有效'
        elif broken_links < 20:
            status = 'warning'
            message = f'发现 {broken_links} 个潜在无效链接'
        else:
            status = 'critical'
            message = f'发现 {broken_links} 个潜在无效链接'
        
        return HealthMetric(
            name='link_health',
            status=status,
            score=score,
            value={'errors': broken_links, 'total': total_links},
            threshold={'max_errors': 20},
            message=message
        )
    
    def check_mermaid_health(self) -> HealthMetric:
        """检查 Mermaid 图表健康状态"""
        mermaid_pattern = re.compile(r'```mermaid\s*\n(.*?)```', re.DOTALL | re.IGNORECASE)
        
        total_charts = 0
        potential_issues = 0
        
        for file_path in self.markdown_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                for match in mermaid_pattern.finditer(content):
                    total_charts += 1
                    chart_content = match.group(1)
                    
                    # 基本语法检查
                    if chart_content.count('(') != chart_content.count(')'):
                        potential_issues += 1
                    elif chart_content.count('[') != chart_content.count(']'):
                        potential_issues += 1
            
            except Exception:
                pass
        
        score = max(0, 100 - potential_issues / max(total_charts, 1) * 100)
        
        if potential_issues == 0:
            status = 'healthy'
            message = f'所有 {total_charts} 个 Mermaid 图表语法正常'
        else:
            status = 'warning'
            message = f'发现 {potential_issues}/{total_charts} 个图表可能有语法问题'
        
        return HealthMetric(
            name='mermaid_health',
            status=status,
            score=score,
            value={'total': total_charts, 'issues': potential_issues},
            threshold={'max_issues': total_charts * 0.05},
            message=message
        )
    
    def check_document_freshness(self) -> HealthMetric:
        """检查文档新鲜度"""
        now = datetime.now()
        outdated_docs = []
        total_age_days = 0
        
        for file_path in self.markdown_files:
            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                age_days = (now - mtime).days
                total_age_days += age_days
                
                # 如果文件超过 180 天未更新，标记为可能过时
                if age_days > 180:
                    outdated_docs.append({
                        'file': str(file_path.relative_to(self.root_dir)),
                        'age_days': age_days
                    })
            
            except Exception:
                pass
        
        avg_age = total_age_days / max(len(self.markdown_files), 1)
        
        # 计算分数（越新越好）
        score = max(0, 100 - avg_age / 3)  # 300天降到0分
        
        if len(outdated_docs) < 10:
            status = 'healthy'
            message = f'文档平均更新于 {avg_age:.0f} 天前'
        elif len(outdated_docs) < 50:
            status = 'warning'
            message = f'{len(outdated_docs)} 个文档超过 180 天未更新'
        else:
            status = 'warning'
            message = f'{len(outdated_docs)} 个文档需要审查更新'
        
        return HealthMetric(
            name='document_freshness',
            status=status,
            score=score,
            value={'avg_age_days': avg_age, 'outdated_count': len(outdated_docs)},
            threshold={'max_outdated': 10},
            message=message
        )
    
    def check_progress_alignment(self) -> HealthMetric:
        """检查进度跟踪对齐"""
        tracking_path = self.root_dir / 'PROJECT-TRACKING.md'
        
        if not tracking_path.exists():
            return HealthMetric(
                name='progress_alignment',
                status='warning',
                score=50,
                value={'error': 'tracking_file_not_found'},
                threshold={'required': True},
                message='PROJECT-TRACKING.md 不存在'
            )
        
        try:
            content = tracking_path.read_text(encoding='utf-8')
            
            # 检查是否包含进度信息
            has_progress = '100%' in content or '总体进度' in content
            has_recent_update = datetime.now().strftime('%Y-%m') in content
            
            score = 100 if has_progress and has_recent_update else 70
            status = 'healthy' if score == 100 else 'warning'
            message = '进度跟踪文档已更新' if score == 100 else '进度跟踪可能需要更新'
            
            return HealthMetric(
                name='progress_alignment',
                status=status,
                score=score,
                value={'has_progress': has_progress, 'has_recent_update': has_recent_update},
                threshold={'required': True},
                message=message
            )
        
        except Exception as e:
            return HealthMetric(
                name='progress_alignment',
                status='warning',
                score=0,
                value={'error': str(e)},
                threshold={'required': True},
                message=f'读取失败: {e}'
            )
    
    def calculate_overall_health(self) -> None:
        """计算整体健康状态"""
        if not self.report.metrics:
            return
        
        scores = [m.score for m in self.report.metrics]
        self.report.overall_score = sum(scores) / len(scores)
        
        # 根据分数确定状态
        if self.report.overall_score >= 90:
            self.report.overall_status = 'healthy'
        elif self.report.overall_score >= 70:
            self.report.overall_status = 'warning'
        else:
            self.report.overall_status = 'critical'
        
        # 生成建议
        for metric in self.report.metrics:
            if metric.status != 'healthy':
                if metric.name == 'link_health':
                    self.report.recommendations.append(
                        "运行 `make validate-crossrefs` 或 `python .scripts/validate_cross_refs.py` 修复链接问题"
                    )
                elif metric.name == 'theorem_registry_sync':
                    self.report.recommendations.append(
                        "运行 `python .scripts/validate_theorem_numbers.py` 检查定理编号同步"
                    )
                elif metric.name == 'mermaid_health':
                    self.report.recommendations.append(
                        "运行 `make validate-mermaid` 检查并修复 Mermaid 语法"
                    )
                elif metric.name == 'document_freshness':
                    self.report.recommendations.append(
                        "审查并更新长时间未修改的文档"
                    )
    
    def load_history(self) -> List[Dict]:
        """加载历史数据"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_history(self) -> None:
        """保存历史数据"""
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        
        history = self.load_history()
        history.append({
            'timestamp': self.report.timestamp,
            'score': self.report.overall_score,
            'status': self.report.overall_status
        })
        
        # 只保留最近 30 条记录
        history = history[-30:]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
    
    def analyze_trends(self) -> Dict:
        """分析趋势"""
        history = self.load_history()
        
        if len(history) < 2:
            return {'message': '数据不足，无法分析趋势'}
        
        scores = [h['score'] for h in history]
        trend = 'improving' if scores[-1] > scores[0] else 'declining' if scores[-1] < scores[0] else 'stable'
        
        return {
            'trend': trend,
            'change': scores[-1] - scores[0],
            'avg_score': sum(scores) / len(scores),
            'data_points': len(history)
        }
    
    def run_all_checks(self) -> None:
        """运行所有检查"""
        print("🔍 正在运行健康检查...")
        
        self.collect_files()
        print(f"   已收集 {len(self.markdown_files)} 个文件")
        
        checks = [
            ('文档覆盖率', self.check_document_coverage),
            ('定理注册表同步', self.check_theorem_registry_sync),
            ('链接健康', self.check_link_health),
            ('Mermaid 图表', self.check_mermaid_health),
            ('文档新鲜度', self.check_document_freshness),
            ('进度跟踪对齐', self.check_progress_alignment),
        ]
        
        for name, check_func in checks:
            print(f"   检查: {name}...", end=' ')
            metric = check_func()
            self.report.metrics.append(metric)
            status_icon = '✅' if metric.status == 'healthy' else '⚠️' if metric.status == 'warning' else '❌'
            print(f"{status_icon} {metric.score:.1f}分")
        
        self.calculate_overall_health()
        self.report.trends = self.analyze_trends()
    
    def print_report(self, json_output: bool = False) -> int:
        """打印报告"""
        if json_output:
            report_dict = {
                'timestamp': self.report.timestamp,
                'overall': {
                    'score': round(self.report.overall_score, 2),
                    'status': self.report.overall_status
                },
                'metrics': [asdict(m) for m in self.report.metrics],
                'recommendations': self.report.recommendations,
                'trends': self.report.trends
            }
            print(json.dumps(report_dict, indent=2, ensure_ascii=False))
        else:
            status_icons = {
                'healthy': '✅',
                'warning': '⚠️',
                'critical': '❌',
                'unknown': '❓'
            }
            
            print("\n" + "=" * 70)
            print("AnalysisDataFlow 项目健康检查仪表盘")
            print("=" * 70)
            
            icon = status_icons.get(self.report.overall_status, '❓')
            print(f"\n{icon} 整体健康状态: {self.report.overall_status.upper()}")
            print(f"   综合得分: {self.report.overall_score:.1f}/100")
            
            print("\n📊 各项健康指标:")
            print("-" * 70)
            for metric in self.report.metrics:
                icon = status_icons.get(metric.status, '❓')
                print(f"   {icon} {metric.name:25s} {metric.score:5.1f}分  {metric.message}")
            
            if self.report.trends:
                print("\n📈 趋势分析:")
                trend_msg = self.report.trends.get('message', '')
                if trend_msg:
                    print(f"   {trend_msg}")
                else:
                    trend_icon = '📈' if self.report.trends.get('trend') == 'improving' else '📉' if self.report.trends.get('trend') == 'declining' else '➡️'
                    print(f"   {trend_icon} 趋势: {self.report.trends.get('trend', 'unknown')}")
                    print(f"   平均得分: {self.report.trends.get('avg_score', 0):.1f}")
            
            if self.report.recommendations:
                print("\n💡 改进建议:")
                for i, rec in enumerate(self.report.recommendations, 1):
                    print(f"   {i}. {rec}")
            
            print("\n" + "=" * 70)
        
        return 0 if self.report.overall_status == 'healthy' else 1


def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 项目健康检查仪表盘',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python .scripts/health_check_dashboard.py
  python .scripts/health_check_dashboard.py --json
  python .scripts/health_check_dashboard.py --save
  python .scripts/health_check_dashboard.py --trend
        """
    )
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--save', action='store_true', help='保存到历史记录')
    parser.add_argument('--trend', action='store_true', help='显示趋势分析')
    
    args = parser.parse_args()
    
    # 确定项目根目录
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    try:
        dashboard = HealthDashboard(str(root_dir))
        dashboard.run_all_checks()
        
        if args.save:
            dashboard.save_history()
            print("\n💾 已保存到历史记录")
        
        exit_code = dashboard.print_report(json_output=args.json)
        sys.exit(exit_code)
    
    except KeyboardInterrupt:
        print("\n\n操作已取消", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 运行错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
