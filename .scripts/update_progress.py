#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进度自动更新脚本 - AnalysisDataFlow 自动化工具集

功能：
1. 自动扫描项目文档计算实际进度
2. 更新 PROJECT-TRACKING.md 中的进度条
3. 支持手动指定进度百分比
4. 生成进度更新报告

使用方法：
    python .scripts/update_progress.py
    python .scripts/update_progress.py --auto
    python .scripts/update_progress.py --struct 45 --knowledge 120 --flink 130
    python .scripts/update_progress.py --update-file

退出码：
    0 - 更新成功
    1 - 更新失败
    2 - 运行异常
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime


@dataclass
class ProgressData:
    """进度数据类"""
    struct_count: int = 0
    struct_total: int = 50  # 目标总数
    knowledge_count: int = 0
    knowledge_total: int = 140
    flink_count: int = 0
    flink_total: int = 170
    visual_count: int = 0
    visual_total: int = 25
    tutorial_count: int = 0
    tutorial_total: int = 30
    governance_count: int = 0
    governance_total: int = 100
    
    @property
    def total_count(self) -> int:
        return (self.struct_count + self.knowledge_count + self.flink_count + 
                self.visual_count + self.tutorial_count)
    
    @property
    def total_target(self) -> int:
        return (self.struct_total + self.knowledge_total + self.flink_total + 
                self.visual_total + self.tutorial_total)
    
    def get_percentage(self, category: str) -> float:
        """获取类别百分比"""
        mapping = {
            'struct': (self.struct_count, self.struct_total),
            'knowledge': (self.knowledge_count, self.knowledge_total),
            'flink': (self.flink_count, self.flink_total),
            'visual': (self.visual_count, self.visual_total),
            'tutorial': (self.tutorial_count, self.tutorial_total),
            'governance': (self.governance_count, self.governance_total),
        }
        count, total = mapping.get(category, (0, 1))
        return (count / total * 100) if total > 0 else 0
    
    def get_overall_percentage(self) -> float:
        """获取总体百分比"""
        return (self.total_count / self.total_target * 100) if self.total_target > 0 else 0


class ProgressUpdater:
    """进度更新器"""
    
    # 进度条字符
    PROGRESS_CHAR = '█'
    EMPTY_CHAR = '░'
    PROGRESS_LENGTH = 20
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.tracking_file = self.root_dir / 'PROJECT-TRACKING.md'
        self.progress = ProgressData()
        
    def scan_project(self) -> None:
        """扫描项目统计实际进度"""
        print("正在扫描项目文档...")
        
        # 扫描各目录
        dirs = {
            'struct': self.root_dir / 'Struct',
            'knowledge': self.root_dir / 'Knowledge',
            'flink': self.root_dir / 'Flink',
            'visual': self.root_dir / 'visuals',
            'tutorial': self.root_dir / 'tutorials',
        }
        
        for category, dir_path in dirs.items():
            if dir_path.exists():
                md_files = list(dir_path.rglob('*.md'))
                count = len(md_files)
                setattr(self.progress, f'{category}_count', count)
                print(f"  {category}: {count} 个文档")
            else:
                print(f"  {category}: 目录不存在")
        
        # 根目录治理文档
        root_md_files = [f for f in self.root_dir.glob('*.md') 
                        if f.is_file() and not f.name.startswith('.')]
        self.progress.governance_count = len(root_md_files)
        print(f"  governance: {self.progress.governance_count} 个文档")
    
    def set_manual_progress(self, **kwargs) -> None:
        """设置手动进度"""
        for key, value in kwargs.items():
            if hasattr(self.progress, key):
                setattr(self.progress, key, value)
                print(f"  设置 {key} = {value}")
    
    def generate_progress_bar(self, percentage: float, length: int = None) -> str:
        """生成进度条"""
        if length is None:
            length = self.PROGRESS_LENGTH
        filled = int(length * percentage / 100)
        empty = length - filled
        return self.PROGRESS_CHAR * filled + self.EMPTY_CHAR * empty
    
    def format_progress_line(self, name: str, count: int, total: int) -> str:
        """格式化进度行"""
        percentage = (count / total * 100) if total > 0 else 0
        bar = self.generate_progress_bar(percentage)
        status = '✅' if percentage >= 100 else '🔄' if percentage >= 80 else '⏳'
        return f"├── {name}:   [{bar}] {percentage:.0f}% ({count}/{total} 完成) {status}"
    
    def update_tracking_file(self, dry_run: bool = False) -> bool:
        """更新跟踪文件"""
        if not self.tracking_file.exists():
            print(f"错误: {self.tracking_file} 不存在")
            return False
        
        try:
            content = self.tracking_file.read_text(encoding='utf-8')
            original_content = content
            
            # 更新总体进度
            overall_pct = self.progress.get_overall_percentage()
            overall_bar = self.generate_progress_bar(overall_pct)
            
            # 替换总体进度行
            content = re.sub(
                r'总体进度:.*?\n',
                f'总体进度: [{overall_bar}] {overall_pct:.0f}% ✅\n',
                content
            )
            
            # 替换各目录进度（支持多种格式）
            progress_patterns = [
                (r'(Struct/:)\s*\[.*?\]\s*[\d.]+%\s*\(\d+/\d+[^)]*\)',
                 self.format_progress_line('Struct/', self.progress.struct_count, self.progress.struct_total)),
                (r'(Knowledge/:)\s*\[.*?\]\s*[\d.]+%\s*\(\d+/\d+[^)]*\)',
                 self.format_progress_line('Knowledge/', self.progress.knowledge_count, self.progress.knowledge_total)),
                (r'(Flink/:)\s*\[.*?\]\s*[\d.]+%\s*\(\d+/\d+[^)]*\)',
                 self.format_progress_line('Flink/', self.progress.flink_count, self.progress.flink_total)),
                (r'(visuals/:)\s*\[.*?\]\s*[\d.]+%\s*\(\d+/\d+[^)]*\)',
                 self.format_progress_line('visuals/', self.progress.visual_count, self.progress.visual_total)),
                (r'(tutorials/:)\s*\[.*?\]\s*[\d.]+%\s*\(\d+/\d+[^)]*\)',
                 self.format_progress_line('tutorials/', self.progress.tutorial_count, self.progress.tutorial_total)),
            ]
            
            for pattern, replacement in progress_patterns:
                content = re.sub(pattern, replacement, content)
            
            # 更新统计表格
            content = self._update_stats_table(content)
            
            # 更新最后更新时间
            today = datetime.now().strftime('%Y-%m-%d')
            content = re.sub(
                r'\*\*最后更新\*\*: \d{4}-\d{2}-\d{2}',
                f'**最后更新**: {today}',
                content
            )
            
            if dry_run:
                print("\n[DRY RUN] 将要更新的内容:")
                # 显示差异
                original_lines = original_content.split('\n')[:30]
                new_lines = content.split('\n')[:30]
                for i, (old, new) in enumerate(zip(original_lines, new_lines)):
                    if old != new:
                        print(f"  行 {i+1}:")
                        print(f"    - {old}")
                        print(f"    + {new}")
                return True
            
            # 写入文件
            self.tracking_file.write_text(content, encoding='utf-8')
            print(f"✅ 已更新 {self.tracking_file}")
            return True
            
        except Exception as e:
            print(f"错误: 更新文件失败: {e}")
            return False
    
    def _update_stats_table(self, content: str) -> str:
        """更新统计表格"""
        # 简单的表格更新 - 替换文档数
        patterns = [
            (r'(\| Struct/ \|) \d+', f'\\1 {self.progress.struct_count}'),
            (r'(\| Knowledge/ \|) \d+', f'\\1 {self.progress.knowledge_count}'),
            (r'(\| Flink/ \|) \d+', f'\\1 {self.progress.flink_count}'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def print_summary(self) -> None:
        """打印进度摘要"""
        print("\n" + "=" * 60)
        print("项目进度摘要")
        print("=" * 60)
        
        categories = [
            ('Struct/', self.progress.struct_count, self.progress.struct_total),
            ('Knowledge/', self.progress.knowledge_count, self.progress.knowledge_total),
            ('Flink/', self.progress.flink_count, self.progress.flink_total),
            ('visuals/', self.progress.visual_count, self.progress.visual_total),
            ('tutorials/', self.progress.tutorial_count, self.progress.tutorial_total),
        ]
        
        for name, count, total in categories:
            percentage = (count / total * 100) if total > 0 else 0
            bar = self.generate_progress_bar(percentage)
            print(f"{name:12s} [{bar}] {percentage:5.1f}% ({count}/{total})")
        
        overall = self.progress.get_overall_percentage()
        overall_bar = self.generate_progress_bar(overall)
        print("-" * 60)
        print(f"{'总体':12s} [{overall_bar}] {overall:5.1f}%")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 进度自动更新工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python .scripts/update_progress.py --auto
  python .scripts/update_progress.py --struct 45 --knowledge 120
  python .scripts/update_progress.py --update-file
  python .scripts/update_progress.py --dry-run
        """
    )
    parser.add_argument('--auto', action='store_true', help='自动扫描项目并更新')
    parser.add_argument('--struct', type=int, help='设置 Struct 文档数')
    parser.add_argument('--knowledge', type=int, help='设置 Knowledge 文档数')
    parser.add_argument('--flink', type=int, help='设置 Flink 文档数')
    parser.add_argument('--visual', type=int, help='设置 visuals 文档数')
    parser.add_argument('--tutorial', type=int, help='设置 tutorials 文档数')
    parser.add_argument('--update-file', action='store_true', help='更新 PROJECT-TRACKING.md')
    parser.add_argument('--dry-run', action='store_true', help='预览更改但不写入')
    parser.add_argument('--summary', action='store_true', help='仅显示进度摘要')
    
    args = parser.parse_args()
    
    # 确定项目根目录
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    try:
        updater = ProgressUpdater(str(root_dir))
        
        # 如果指定了自动模式或手动数值
        if args.auto:
            updater.scan_project()
        elif any([args.struct, args.knowledge, args.flink, args.visual, args.tutorial]):
            updater.set_manual_progress(
                struct_count=args.struct or 0,
                knowledge_count=args.knowledge or 0,
                flink_count=args.flink or 0,
                visual_count=args.visual or 0,
                tutorial_count=args.tutorial or 0
            )
        else:
            # 默认扫描
            updater.scan_project()
        
        # 显示摘要
        updater.print_summary()
        
        # 如果需要更新文件
        if args.update_file or args.dry_run:
            success = updater.update_tracking_file(dry_run=args.dry_run)
            sys.exit(0 if success else 1)
        
        sys.exit(0)
    
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
