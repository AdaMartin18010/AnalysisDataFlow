#!/usr/bin/env python3
"""
Flink内容新鲜度标记应用脚本
用于将新鲜度元数据批量应用到Markdown文档顶部
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

class FreshnessTagApplier:
    """内容新鲜度标记应用器"""
    
    def __init__(self, metadata_path: str, project_root: str):
        self.metadata_path = metadata_path
        self.project_root = Path(project_root)
        self.metadata = self._load_metadata()
        
    def _load_metadata(self) -> Dict:
        """加载元数据JSON文件"""
        with open(self.metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _generate_frontmatter(self, file_info: Dict) -> str:
        """生成YAML front matter"""
        freshness = file_info.get('freshness', {})
        
        frontmatter = """---
freshness:
  last_updated: "{last_updated}"
  tech_version: "{tech_version}"
  confidence_level: "{confidence_level}"
  content_type: "{content_type}"
  refs_count: {refs_count}
  validation_status: "{validation_status}"
  next_review: "{next_review}"
---

""".format(
            last_updated=freshness.get('last_updated', ''),
            tech_version=freshness.get('tech_version', ''),
            confidence_level=freshness.get('confidence_level', 'medium'),
            content_type=freshness.get('content_type', 'reference'),
            refs_count=freshness.get('refs_count', 0),
            validation_status=freshness.get('validation_status', 'pending'),
            next_review=freshness.get('next_review', '')
        )
        return frontmatter
    
    def _has_existing_frontmatter(self, content: str) -> bool:
        """检查是否已有YAML front matter"""
        return content.startswith('---\n') or content.startswith('---\r\n')
    
    def _has_freshness_tag(self, content: str) -> bool:
        """检查是否已有freshness标记"""
        return 'freshness:' in content[:500]
    
    def _remove_old_frontmatter(self, content: str) -> str:
        """移除旧的YAML front matter"""
        if not self._has_existing_frontmatter(content):
            return content
        
        # 找到第二个---
        match = re.search(r'^---\s*\n(.*?)---\s*\n', content, re.DOTALL)
        if match:
            return content[match.end():]
        return content
    
    def apply_tag_to_file(self, file_info: Dict, dry_run: bool = True) -> Dict:
        """
        为单个文件应用新鲜度标记
        
        Args:
            file_info: 文件元数据
            dry_run: 是否为试运行模式（不实际修改文件）
        
        Returns:
            操作结果字典
        """
        relative_path = file_info['path']
        file_path = self.project_root / relative_path
        
        result = {
            'path': relative_path,
            'status': 'skipped',
            'message': ''
        }
        
        if not file_path.exists():
            result['status'] = 'error'
            result['message'] = f'File not found: {file_path}'
            return result
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # 检查是否已有freshness标记
            if self._has_freshness_tag(original_content):
                result['status'] = 'skipped'
                result['message'] = 'Already has freshness tag'
                return result
            
            # 生成新的front matter
            new_frontmatter = self._generate_frontmatter(file_info)
            
            # 移除旧的front matter（如果有）
            content_without_frontmatter = self._remove_old_frontmatter(original_content)
            
            # 组合新内容
            new_content = new_frontmatter + content_without_frontmatter.lstrip()
            
            if not dry_run:
                # 备份原文件
                backup_path = str(file_path) + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # 写入新内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                result['status'] = 'success'
                result['message'] = 'Tag applied successfully'
            else:
                result['status'] = 'dry_run'
                result['message'] = 'Would apply tag (dry run)'
            
        except Exception as e:
            result['status'] = 'error'
            result['message'] = str(e)
        
        return result
    
    def apply_all_tags(self, dry_run: bool = True) -> List[Dict]:
        """
        为所有文件应用新鲜度标记
        
        Args:
            dry_run: 是否为试运行模式
        
        Returns:
            操作结果列表
        """
        results = []
        files = self.metadata.get('files', [])
        
        print(f"{'[DRY RUN] ' if dry_run else ''}Processing {len(files)} files...")
        
        for i, file_info in enumerate(files, 1):
            result = self.apply_tag_to_file(file_info, dry_run)
            results.append(result)
            
            if i % 50 == 0:
                print(f"  Processed {i}/{len(files)} files...")
        
        return results
    
    def generate_report(self, results: List[Dict]) -> str:
        """生成操作报告"""
        total = len(results)
        success = len([r for r in results if r['status'] == 'success'])
        dry_run_success = len([r for r in results if r['status'] == 'dry_run'])
        skipped = len([r for r in results if r['status'] == 'skipped'])
        errors = len([r for r in results if r['status'] == 'error'])
        
        report = f"""# 新鲜度标记应用报告

生成时间: {datetime.now().isoformat()}

## 执行摘要

| 指标 | 数量 |
|------|------|
| 总文件数 | {total} |
| 成功应用 | {success} |
| 试运行成功 | {dry_run_success} |
| 已跳过 | {skipped} |
| 错误 | {errors} |

## 状态分布

"""
        
        # 按状态分组
        status_groups = {}
        for r in results:
            status = r['status']
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(r)
        
        for status, items in status_groups.items():
            report += f"\n### {status.upper()} ({len(items)} 文件)\n\n"
            for item in items[:10]:  # 只显示前10个
                report += f"- `{item['path']}`: {item['message']}\n"
            if len(items) > 10:
                report += f"- ... 还有 {len(items) - 10} 个文件\n"
        
        return report


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Apply freshness tags to Flink markdown files'
    )
    parser.add_argument(
        '--metadata',
        default='freshness-metadata.json',
        help='Path to freshness metadata JSON file'
    )
    parser.add_argument(
        '--project-root',
        default='..',
        help='Project root directory'
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Actually apply tags (default is dry run)'
    )
    parser.add_argument(
        '--report',
        default='apply-report.md',
        help='Path to save operation report'
    )
    
    args = parser.parse_args()
    
    # 创建applier实例
    applier = FreshnessTagApplier(
        metadata_path=args.metadata,
        project_root=args.project_root
    )
    
    # 应用标签
    dry_run = not args.apply
    results = applier.apply_all_tags(dry_run=dry_run)
    
    # 生成报告
    report = applier.generate_report(results)
    
    # 保存报告
    with open(args.report, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nReport saved to: {args.report}")
    
    # 打印摘要
    success = len([r for r in results if r['status'] in ('success', 'dry_run')])
    print(f"Summary: {success}/{len(results)} files ready for tagging")


if __name__ == '__main__':
    main()
