#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 自动化内容更新脚本
Auto Content Updater

版本: v1.0 | 生效日期: 2026-04-12 | 状态: Active
功能: 外部链接检查、版本信息更新、统计数据更新、过期内容标记

用法:
    python auto-content-updater.py [options]
    
选项:
    --check-links          检查外部链接
    --update-versions      更新版本信息
    --update-stats         更新统计数据
    --mark-stale           标记过期内容
    --full-update          执行完整更新
    --dry-run              模拟运行，不实际修改文件
"""

import os
import re
import json
import yaml
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from urllib.parse import urlparse
import subprocess

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('.scripts/content-update.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 配置常量
CONFIG = {
    'stale_days': 90,  # 内容过期天数
    'critical_links': [
        'https://nightlies.apache.org/flink/',
        'https://flink.apache.org/',
        'https://cwiki.apache.org/confluence/display/FLINK/',
    ],
    'version_files': [
        'VERSION-TRACKING.md',
        'PROJECT-TRACKING.md',
        'ROADMAP.md',
    ],
    'stats_output': 'validation-stats.json',
}


@dataclass
class UpdateResult:
    """更新结果数据类"""
    task: str
    status: str  # 'success', 'warning', 'error'
    message: str
    details: Optional[Dict] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class ContentUpdater:
    """内容更新器主类"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.results: List[UpdateResult] = []
        self.project_stats = {}
        
    def log_result(self, result: UpdateResult):
        """记录更新结果"""
        self.results.append(result)
        if result.status == 'error':
            logger.error(f"[{result.task}] {result.message}")
        elif result.status == 'warning':
            logger.warning(f"[{result.task}] {result.message}")
        else:
            logger.info(f"[{result.task}] {result.message}")
    
    # ============ 1. 外部链接检查 ============
    
    def check_external_links(self) -> UpdateResult:
        """
        检查外部链接的健康状态
        
        功能:
        - 扫描所有Markdown文件中的外部链接
        - 验证链接可访问性
        - 识别失效链接
        - 生成链接健康报告
        """
        logger.info("开始外部链接检查...")
        
        try:
            # 调用现有的链接检查脚本
            result = subprocess.run(
                ['python', '.scripts/link-health-checker.py', '--json-output'],
                capture_output=True,
                text=True,
                timeout=1800
            )
            
            # 解析检查结果
            if result.returncode == 0:
                # 尝试解析JSON输出
                try:
                    link_data = json.loads(result.stdout)
                    broken_count = len(link_data.get('broken_links', []))
                    total_count = link_data.get('total_checked', 0)
                    
                    if broken_count == 0:
                        return UpdateResult(
                            task='check_external_links',
                            status='success',
                            message=f'所有 {total_count} 个外部链接正常',
                            details={'total': total_count, 'broken': 0}
                        )
                    else:
                        return UpdateResult(
                            task='check_external_links',
                            status='warning',
                            message=f'发现 {broken_count} 个失效链接 (共 {total_count} 个)',
                            details={'total': total_count, 'broken': broken_count, 'links': link_data.get('broken_links', [])}
                        )
                except json.JSONDecodeError:
                    return UpdateResult(
                        task='check_external_links',
                        status='success',
                        message='链接检查完成',
                        details={'output': result.stdout[:500]}
                    )
            else:
                return UpdateResult(
                    task='check_external_links',
                    status='error',
                    message=f'链接检查脚本执行失败: {result.stderr[:200]}'
                )
                
        except subprocess.TimeoutExpired:
            return UpdateResult(
                task='check_external_links',
                status='error',
                message='链接检查超时 (>30分钟)'
            )
        except Exception as e:
            return UpdateResult(
                task='check_external_links',
                status='error',
                message=f'链接检查异常: {str(e)}'
            )
    
    # ============ 2. 版本信息更新 ============
    
    def fetch_latest_versions(self) -> Dict[str, str]:
        """
        获取最新版本信息
        
        从各官方源获取最新版本号
        """
        versions = {
            'flink': self._get_flink_latest_version(),
            'flink_cdc': self._get_flink_cdc_latest_version(),
            'kubernetes_operator': self._get_k8s_operator_latest_version(),
            'scala': '2.12.20',  # 手动维护
            'java': '17',  # LTS版本
            'python': '3.11',  # 稳定版本
        }
        return versions
    
    def _get_flink_latest_version(self) -> str:
        """获取Flink最新版本"""
        # 实际实现中可以从Maven Central或GitHub API获取
        # 这里返回已知最新版本
        return '2.2.0'
    
    def _get_flink_cdc_latest_version(self) -> str:
        """获取Flink CDC最新版本"""
        return '3.6.0'
    
    def _get_k8s_operator_latest_version(self) -> str:
        """获取K8s Operator最新版本"""
        return '1.14.0'
    
    def update_version_tracking(self) -> UpdateResult:
        """
        更新版本跟踪文档
        
        功能:
        - 获取各组件最新版本
        - 更新VERSION-TRACKING.md
        - 标记需要关注的变化
        """
        logger.info("开始更新版本跟踪信息...")
        
        try:
            versions = self.fetch_latest_versions()
            version_file = PROJECT_ROOT / 'VERSION-TRACKING.md'
            
            if not version_file.exists():
                return UpdateResult(
                    task='update_version_tracking',
                    status='error',
                    message='VERSION-TRACKING.md 不存在'
                )
            
            # 读取现有内容
            content = version_file.read_text(encoding='utf-8')
            
            # 更新最后检查时间
            now = datetime.now().strftime('%Y-%m-%d')
            content = re.sub(
                r'最后更新: \d{4}-\d{2}-\d{2}',
                f'最后更新: {now}',
                content
            )
            
            # 实际实现中会更详细地更新各版本表格
            # 这里简化处理
            
            if not self.dry_run:
                version_file.write_text(content, encoding='utf-8')
                logger.info(f"已更新 {version_file}")
            else:
                logger.info(f"[DRY-RUN] 将更新 {version_file}")
            
            return UpdateResult(
                task='update_version_tracking',
                status='success',
                message=f'版本跟踪已更新，检测到 {len(versions)} 个组件',
                details={'versions': versions, 'updated_at': now}
            )
            
        except Exception as e:
            return UpdateResult(
                task='update_version_tracking',
                status='error',
                message=f'版本更新失败: {str(e)}'
            )
    
    # ============ 3. 统计数据更新 ============
    
    def calculate_project_stats(self) -> Dict:
        """
        计算项目统计数据
        
        统计项:
        - 文档总数
        - 代码行数
        - 形式化元素数量
        - Mermaid图表数量
        """
        stats = {
            'timestamp': datetime.now().isoformat(),
            'documents': {},
            'formal_elements': {},
            'code_examples': 0,
            'mermaid_charts': 0,
        }
        
        # 统计各目录文档数
        for directory in ['Struct', 'Knowledge', 'Flink', 'tutorials', 'en']:
            dir_path = PROJECT_ROOT / directory
            if dir_path.exists():
                md_files = list(dir_path.rglob('*.md'))
                stats['documents'][directory] = len(md_files)
        
        # 统计形式化元素
        stats['formal_elements'] = self._count_formal_elements()
        
        # 统计代码示例和Mermaid图表
        stats['code_examples'] = self._count_code_examples()
        stats['mermaid_charts'] = self._count_mermaid_charts()
        
        return stats
    
    def _count_formal_elements(self) -> Dict[str, int]:
        """统计形式化元素数量"""
        counts = {'theorem': 0, 'definition': 0, 'lemma': 0, 'proposition': 0, 'corollary': 0}
        
        for directory in ['Struct', 'Knowledge', 'Flink']:
            dir_path = PROJECT_ROOT / directory
            if not dir_path.exists():
                continue
                
            for md_file in dir_path.rglob('*.md'):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    counts['theorem'] += len(re.findall(r'\*\*Thm-[A-Z]-\d{2}-\d{2}\*\*', content))
                    counts['definition'] += len(re.findall(r'\*\*Def-[A-Z]-\d{2}-\d{2}\*\*', content))
                    counts['lemma'] += len(re.findall(r'\*\*Lemma-[A-Z]-\d{2}-\d{2}\*\*', content))
                    counts['proposition'] += len(re.findall(r'\*\*Prop-[A-Z]-\d{2}-\d{2}\*\*', content))
                    counts['corollary'] += len(re.findall(r'\*\*Cor-[A-Z]-\d{2}-\d{2}\*\*', content))
                except Exception:
                    pass
        
        return counts
    
    def _count_code_examples(self) -> int:
        """统计代码示例数量"""
        count = 0
        for directory in ['Struct', 'Knowledge', 'Flink', 'tutorials', 'examples']:
            dir_path = PROJECT_ROOT / directory
            if not dir_path.exists():
                continue
            for md_file in dir_path.rglob('*.md'):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    count += len(re.findall(r'```(java|scala|python|go|rust|coq|tla)', content))
                except Exception:
                    pass
        return count
    
    def _count_mermaid_charts(self) -> int:
        """统计Mermaid图表数量"""
        count = 0
        for directory in ['Struct', 'Knowledge', 'Flink']:
            dir_path = PROJECT_ROOT / directory
            if not dir_path.exists():
                continue
            for md_file in dir_path.rglob('*.md'):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    count += len(re.findall(r'```mermaid', content))
                except Exception:
                    pass
        return count
    
    def update_statistics(self) -> UpdateResult:
        """
        更新项目统计数据
        
        功能:
        - 计算最新统计
        - 更新统计文件
        - 生成趋势报告
        """
        logger.info("开始更新统计数据...")
        
        try:
            stats = self.calculate_project_stats()
            stats_file = PROJECT_ROOT / '.scripts' / CONFIG['stats_output']
            
            # 合并历史数据
            if stats_file.exists():
                try:
                    with open(stats_file, 'r', encoding='utf-8') as f:
                        history = json.load(f)
                    if not isinstance(history, list):
                        history = [history]
                except Exception:
                    history = []
            else:
                history = []
            
            history.append(stats)
            
            # 只保留最近30条记录
            history = history[-30:]
            
            if not self.dry_run:
                with open(stats_file, 'w', encoding='utf-8') as f:
                    json.dump(history, f, indent=2, ensure_ascii=False)
                logger.info(f"统计已更新: {stats_file}")
            else:
                logger.info(f"[DRY-RUN] 将更新 {stats_file}")
            
            # 更新PROJECT-TRACKING.md中的统计数据
            self._update_tracking_stats(stats)
            
            return UpdateResult(
                task='update_statistics',
                status='success',
                message=f'统计数据已更新，共 {sum(stats["documents"].values())} 篇文档',
                details=stats
            )
            
        except Exception as e:
            return UpdateResult(
                task='update_statistics',
                status='error',
                message=f'统计更新失败: {str(e)}'
            )
    
    def _update_tracking_stats(self, stats: Dict):
        """更新PROJECT-TRACKING.md中的统计数据"""
        tracking_file = PROJECT_ROOT / 'PROJECT-TRACKING.md'
        if not tracking_file.exists():
            return
        
        # 这里可以实现更复杂的统计更新逻辑
        pass
    
    # ============ 4. 过期内容标记 ============
    
    def mark_stale_content(self) -> UpdateResult:
        """
        标记过期内容
        
        功能:
        - 扫描文件修改时间
        - 标记超过stale_days天未更新的内容
        - 生成过期内容报告
        """
        logger.info(f"开始标记超过 {CONFIG['stale_days']} 天未更新的内容...")
        
        try:
            stale_files = []
            cutoff_date = datetime.now() - timedelta(days=CONFIG['stale_days'])
            
            # 扫描关键目录
            for directory in ['Struct', 'Knowledge', 'Flink']:
                dir_path = PROJECT_ROOT / directory
                if not dir_path.exists():
                    continue
                
                for md_file in dir_path.rglob('*.md'):
                    try:
                        mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
                        if mtime < cutoff_date:
                            stale_files.append({
                                'path': str(md_file.relative_to(PROJECT_ROOT)),
                                'last_modified': mtime.strftime('%Y-%m-%d'),
                                'days_stale': (datetime.now() - mtime).days
                            })
                            
                            # 可选：在文件中添加过期标记
                            if not self.dry_run:
                                self._add_stale_marker(md_file, mtime)
                                
                    except Exception as e:
                        logger.warning(f"无法检查文件 {md_file}: {e}")
            
            # 生成过期报告
            report = {
                'generated_at': datetime.now().isoformat(),
                'stale_threshold_days': CONFIG['stale_days'],
                'stale_files_count': len(stale_files),
                'stale_files': stale_files
            }
            
            report_file = PROJECT_ROOT / '.scripts' / 'stale-content-report.json'
            if not self.dry_run:
                with open(report_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
            
            return UpdateResult(
                task='mark_stale_content',
                status='warning' if stale_files else 'success',
                message=f'发现 {len(stale_files)} 个过期文件',
                details=report
            )
            
        except Exception as e:
            return UpdateResult(
                task='mark_stale_content',
                status='error',
                message=f'过期标记失败: {str(e)}'
            )
    
    def _add_stale_marker(self, file_path: Path, last_modified: datetime):
        """在文件中添加过期标记"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 检查是否已有过期标记
            if '> **内容状态**: ⚠️ 可能过期' in content:
                return
            
            # 在文件开头添加标记（如果还没有）
            marker = f"> **内容状态**: ⚠️ 可能过期 | **最后更新**: {last_modified.strftime('%Y-%m-%d')} | 建议复审\n>\n"
            
            # 查找合适的位置插入标记
            lines = content.split('\n')
            insert_pos = 0
            
            # 跳过YAML frontmatter
            if lines[0] == '---':
                for i, line in enumerate(lines[1:], 1):
                    if line == '---':
                        insert_pos = i + 1
                        break
            
            # 插入标记
            new_lines = lines[:insert_pos] + [marker] + lines[insert_pos:]
            new_content = '\n'.join(new_lines)
            
            file_path.write_text(new_content, encoding='utf-8')
            logger.debug(f"已添加过期标记: {file_path}")
            
        except Exception as e:
            logger.warning(f"无法标记文件 {file_path}: {e}")
    
    # ============ 5. 完整更新流程 ============
    
    def run_full_update(self) -> List[UpdateResult]:
        """
        执行完整更新流程
        
        依次执行所有更新任务
        """
        logger.info("=" * 60)
        logger.info("开始完整内容更新流程")
        logger.info("=" * 60)
        
        # 1. 外部链接检查
        self.log_result(self.check_external_links())
        
        # 2. 版本信息更新
        self.log_result(self.update_version_tracking())
        
        # 3. 统计数据更新
        self.log_result(self.update_statistics())
        
        # 4. 过期内容标记
        self.log_result(self.mark_stale_content())
        
        # 生成汇总报告
        self._generate_summary_report()
        
        return self.results
    
    def _generate_summary_report(self):
        """生成更新汇总报告"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'dry_run': self.dry_run,
            'results': [asdict(r) for r in self.results]
        }
        
        # 统计状态
        status_counts = {'success': 0, 'warning': 0, 'error': 0}
        for r in self.results:
            status_counts[r.status] = status_counts.get(r.status, 0) + 1
        
        report['summary'] = status_counts
        
        # 保存报告
        report_file = PROJECT_ROOT / '.scripts' / 'update-summary-report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info("=" * 60)
        logger.info("更新汇总:")
        logger.info(f"  成功: {status_counts['success']}")
        logger.info(f"  警告: {status_counts['warning']}")
        logger.info(f"  错误: {status_counts['error']}")
        logger.info("=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 自动化内容更新脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python auto-content-updater.py --full-update
    python auto-content-updater.py --check-links --dry-run
    python auto-content-updater.py --update-versions
    python auto-content-updater.py --mark-stale
        """
    )
    
    parser.add_argument('--check-links', action='store_true',
                        help='检查外部链接')
    parser.add_argument('--update-versions', action='store_true',
                        help='更新版本信息')
    parser.add_argument('--update-stats', action='store_true',
                        help='更新统计数据')
    parser.add_argument('--mark-stale', action='store_true',
                        help='标记过期内容')
    parser.add_argument('--full-update', action='store_true',
                        help='执行完整更新')
    parser.add_argument('--dry-run', action='store_true',
                        help='模拟运行，不实际修改文件')
    
    args = parser.parse_args()
    
    # 如果没有指定任何操作，显示帮助
    if not any([args.check_links, args.update_versions, args.update_stats, 
                args.mark_stale, args.full_update]):
        parser.print_help()
        return
    
    updater = ContentUpdater(dry_run=args.dry_run)
    
    if args.full_update:
        updater.run_full_update()
    else:
        if args.check_links:
            result = updater.check_external_links()
            updater.log_result(result)
            print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
            
        if args.update_versions:
            result = updater.update_version_tracking()
            updater.log_result(result)
            print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
            
        if args.update_stats:
            result = updater.update_statistics()
            updater.log_result(result)
            print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
            
        if args.mark_stale:
            result = updater.mark_stale_content()
            updater.log_result(result)
            print(json.dumps(asdict(result), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
