#!/usr/bin/env python3
"""
Flink内容新鲜度元数据生成脚本
扫描Flink目录下的所有markdown文件并生成freshness-metadata.json
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class FreshnessMetadataGenerator:
    """内容新鲜度元数据生成器"""
    
    # 版本EOL日期
    EOL_VERSIONS = ['1.13', '1.14', '1.15', '1.16']
    
    # 当前主流版本
    CURRENT_VERSIONS = ['2.0', '2.1', '2.2', '2.3']
    
    # 文件路径到内容类型的映射规则
    CONTENT_TYPE_RULES = [
        (r'02-core', 'core'),
        (r'01-concepts', 'core'),
        (r'03-api.*-reference', 'reference'),
        (r'03-api.*-cheatsheet', 'reference'),
        (r'03-api', 'reference'),
        (r'06-ai-ml', 'frontier'),
        (r'07-rust-native', 'frontier'),
        (r'08-roadmap', 'frontier'),
        (r'09-practices', 'practice'),
        (r'04-runtime.*evolution', 'reference'),
        (r'04-runtime', 'core'),
        (r'05-ecosystem.*evolution', 'reference'),
        (r'05-ecosystem', 'practice'),
        (r'00-meta', 'reference'),
    ]
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.flink_dir = self.project_root / 'Flink'
        self.results = []
        
    def _detect_tech_version(self, content: str, file_path: str) -> str:
        """从技术内容中检测Flink版本"""
        # 按优先级检查版本
        version_patterns = [
            r'Flink[\s]*([2-3]\.\d+(?:\.\d+)?)',
            r'version[\s]*[:\-]?\s*([2-3]\.\d+)',
        ]
        
        found_versions = []
        for pattern in version_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                # 清理版本字符串
                version = match.strip()
                if re.match(r'^[2-3]\.\d', version):
                    found_versions.append(version)
        
        # 特殊路径检测
        path_lower = file_path.lower()
        if 'flink-2.3' in path_lower or '2.3' in path_lower:
            found_versions.append('2.3')
        elif 'flink-2.2' in path_lower or '2.2' in path_lower:
            found_versions.append('2.2')
        elif 'flink-2.0' in path_lower or '2.0' in path_lower:
            found_versions.append('2.0')
        elif 'flink-2.1' in path_lower or '2.1' in path_lower:
            found_versions.append('2.1')
        
        # 返回最新的版本
        if found_versions:
            return max(found_versions, key=lambda v: float(v[:3]))
        
        # AI/ML文档默认为2.3
        if '06-ai-ml' in file_path or 'ai-agent' in path_lower:
            return '2.3'
        
        # Rust原生默认为2.2
        if 'rust-native' in file_path or 'rust' in path_lower:
            return '2.2'
        
        # 默认为2.2
        return '2.2'
    
    def _count_references(self, content: str) -> int:
        """统计引用数量"""
        refs = re.findall(r'\[\^(\d+)\]', content)
        return len(set(refs))
    
    def _determine_content_type(self, file_path: str) -> str:
        """根据文件路径确定内容类型"""
        path_str = str(file_path).replace('\\', '/')
        
        for pattern, content_type in self.CONTENT_TYPE_RULES:
            if re.search(pattern, path_str, re.IGNORECASE):
                return content_type
        
        return 'reference'
    
    def _calculate_confidence(
        self, 
        mtime: datetime, 
        version: str, 
        ref_count: int,
        content_type: str
    ) -> Tuple[str, str]:
        """计算置信度等级和验证状态"""
        score = 0
        now = datetime.now()
        days_old = (now - mtime).days
        
        # 时间因子 (0-40分)
        if days_old < 30:
            score += 40
        elif days_old < 90:
            score += 30
        elif days_old < 180:
            score += 20
        else:
            score += 10
        
        # 版本因子 (0-30分)
        version_main = version[:3] if len(version) >= 3 else version
        if version_main in ['2.3', '2.2']:
            score += 30
        elif version_main in ['2.1', '2.0']:
            score += 25
        elif version_main.startswith('1.1') or version_main.startswith('1.2'):
            score += 15
        else:
            score += 10
        
        # 引用因子 (0-30分)
        if ref_count >= 10:
            score += 30
        elif ref_count >= 5:
            score += 20
        elif ref_count >= 2:
            score += 10
        
        # 内容类型调整
        if content_type == 'frontier':
            score -= 10
        elif content_type == 'core':
            score += 5
        
        # 映射到等级
        if score >= 70:
            level = 'high'
            status = 'validated'
        elif score >= 40:
            level = 'medium'
            status = 'pending'
        else:
            level = 'low'
            status = 'deprecated' if version_main in self.EOL_VERSIONS else 'pending'
        
        return level, status
    
    def _calculate_next_review(self, last_updated: str, confidence_level: str) -> str:
        """计算建议下次审查日期"""
        last = datetime.strptime(last_updated, '%Y-%m-%d')
        
        if confidence_level == 'high':
            delta = timedelta(days=180)
        elif confidence_level == 'medium':
            delta = timedelta(days=90)
        else:
            delta = timedelta(days=30)
        
        next_review = last + delta
        return next_review.strftime('%Y-%m-%d')
    
    def _analyze_file(self, file_path: Path) -> Optional[Dict]:
        """分析单个文件"""
        try:
            stat = file_path.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            relative_path = str(file_path.relative_to(self.project_root))
            tech_version = self._detect_tech_version(content, relative_path)
            ref_count = self._count_references(content)
            content_type = self._determine_content_type(relative_path)
            
            confidence_level, validation_status = self._calculate_confidence(
                mtime, tech_version, ref_count, content_type
            )
            
            last_updated = mtime.strftime('%Y-%m-%d')
            next_review = self._calculate_next_review(last_updated, confidence_level)
            
            return {
                'path': relative_path.replace('\\', '/'),
                'last_updated': last_updated,
                'tech_version': tech_version,
                'confidence_level': confidence_level,
                'content_type': content_type,
                'refs_count': ref_count,
                'validation_status': validation_status,
                'next_review': next_review,
                'freshness': {
                    'last_updated': last_updated,
                    'tech_version': tech_version,
                    'confidence_level': confidence_level,
                    'content_type': content_type,
                    'refs_count': ref_count,
                    'validation_status': validation_status,
                    'next_review': next_review
                }
            }
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None
    
    def scan_and_generate(self) -> Dict:
        """扫描并生成元数据"""
        print(f"Scanning {self.flink_dir} for markdown files...")
        
        markdown_files = list(self.flink_dir.rglob('*.md'))
        print(f"Found {len(markdown_files)} markdown files")
        
        files_metadata = []
        for i, file_path in enumerate(markdown_files, 1):
            metadata = self._analyze_file(file_path)
            if metadata:
                files_metadata.append(metadata)
            
            if i % 50 == 0:
                print(f"  Processed {i}/{len(markdown_files)} files...")
        
        # 生成汇总统计
        confidence_dist = {'high': 0, 'medium': 0, 'low': 0}
        type_dist = {}
        version_dist = {}
        
        for f in files_metadata:
            confidence_dist[f['confidence_level']] += 1
            t = f['content_type']
            type_dist[t] = type_dist.get(t, 0) + 1
            v = f['tech_version'][:3]
            version_dist[v] = version_dist.get(v, 0) + 1
        
        result = {
            'generated_at': datetime.now().isoformat(),
            'project': 'AnalysisDataFlow',
            'directory': 'Flink/',
            'total_files': len(files_metadata),
            'statistics': {
                'confidence_distribution': confidence_dist,
                'content_type_distribution': type_dist,
                'version_distribution': version_dist
            },
            'files': files_metadata
        }
        
        self.results = result
        return result
    
    def save_metadata(self, output_path: str):
        """保存元数据到JSON文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\nMetadata saved to: {output_path}")
    
    def generate_report(self, output_path: str):
        """生成执行报告"""
        stats = self.results['statistics']
        total = self.results['total_files']
        
        report_lines = [
            "# A1 - 内容新鲜度扫描执行报告",
            "",
            f"生成时间: {self.results['generated_at']}",
            f"扫描目录: {self.results['directory']}",
            f"总文件数: {total}",
            "",
            "## 执行摘要",
            "",
            "本次扫描分析了Flink目录下的所有markdown文档，基于以下维度评估内容新鲜度：",
            "- 文档最后修改时间",
            "- 技术版本相关性",
            "- 引用数量和质量",
            "- 内容类型分类",
            "",
            "## 置信度分布",
            "",
            "| 等级 | 数量 | 百分比 | 说明 |",
            "|------|------|--------|------|",
        ]
        
        for level in ['high', 'medium', 'low']:
            count = stats['confidence_distribution'][level]
            pct = count / total * 100 if total > 0 else 0
            desc = {
                'high': '内容可靠，可直接参考',
                'medium': '基本可靠，关键信息需验证',
                'low': '可能过时，必须验证后使用'
            }[level]
            report_lines.append(f"| {level} | {count} | {pct:.1f}% | {desc} |")
        
        report_lines.extend([
            "",
            "## 内容类型分布",
            "",
            "| 类型 | 数量 | 说明 |",
            "|------|------|------|",
        ])
        
        type_desc = {
            'core': '核心机制、架构设计',
            'reference': 'API参考、配置文档',
            'frontier': '前沿特性、实验功能',
            'practice': '实践指南、案例研究'
        }
        
        for t, count in sorted(stats['content_type_distribution'].items(), key=lambda x: -x[1]):
            desc = type_desc.get(t, '')
            report_lines.append(f"| {t} | {count} | {desc} |")
        
        report_lines.extend([
            "",
            "## 版本分布",
            "",
            "| 版本 | 数量 |",
            "|------|------|",
        ])
        
        for v, count in sorted(stats['version_distribution'].items(), key=lambda x: x[0]):
            report_lines.append(f"| {v} | {count} |")
        
        report_lines.extend([
            "",
            "## 低置信度文件列表（需优先审查）",
            "",
        ])
        
        low_conf_files = [f for f in self.results['files'] if f['confidence_level'] == 'low']
        for f in low_conf_files[:30]:
            report_lines.append(f"- `{f['path']}` (v{f['tech_version']}, refs: {f['refs_count']})")
        
        if len(low_conf_files) > 30:
            report_lines.append(f"\n... 还有 {len(low_conf_files) - 30} 个低置信度文件")
        
        report_lines.extend([
            "",
            "## 高置信度文件示例",
            "",
        ])
        
        high_conf_files = [f for f in self.results['files'] if f['confidence_level'] == 'high']
        for f in high_conf_files[:15]:
            report_lines.append(f"- `{f['path']}` (v{f['tech_version']}, refs: {f['refs_count']})")
        
        report_lines.extend([
            "",
            "## 生成的文件",
            "",
            "1. `freshness-metadata.json` - 完整元数据文件",
            "2. `freshness-template.md` - 新鲜度标记模板",
            "3. `content-freshness-system.md` - 系统设计文档",
            "4. `apply-freshness-tags.py` - 批量标记应用脚本",
            "",
            "## 后续操作",
            "",
            "1. 审查低置信度文件，更新过期内容",
            "2. 运行 `python apply-freshness-tags.py` 应用标记（试运行）",
            "3. 确认无误后运行 `python apply-freshness-tags.py --apply` 正式应用",
            "",
            "---",
            "",
            "*报告由内容新鲜度标记系统自动生成*"
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        print(f"Report saved to: {output_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate freshness metadata for Flink documentation'
    )
    parser.add_argument(
        '--project-root',
        default='..',
        help='Project root directory'
    )
    parser.add_argument(
        '--output',
        default='freshness-metadata.json',
        help='Output JSON file path'
    )
    parser.add_argument(
        '--report',
        default='A1-report.md',
        help='Output report file path'
    )
    
    args = parser.parse_args()
    
    generator = FreshnessMetadataGenerator(args.project_root)
    generator.scan_and_generate()
    generator.save_metadata(args.output)
    generator.generate_report(args.report)
    
    print("\nDone!")


if __name__ == '__main__':
    main()
