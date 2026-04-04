#!/usr/bin/env python3
"""
================================================================================
AnalysisDataFlow 自动统计更新脚本
================================================================================
描述: 自动统计项目文档数量并更新相关文件
功能:
  - 扫描各目录文档数量
  - 统计形式化元素（定理、定义等）
  - 更新 PROJECT-TRACKING.md
  - 更新 README.md
  - 生成统计报告

使用方法:
  python update-stats.py [选项]

选项:
  --check-only        仅检查，不更新文件
  --update-tracking   更新 PROJECT-TRACKING.md
  --update-readme     更新 README.md
  --format FORMAT     输出格式: text|json|markdown
  --output FILE       输出文件路径
  --verbose           显示详细信息

示例:
  # 仅显示当前统计
  python update-stats.py --check-only

  # 更新所有统计文件
  python update-stats.py --update-tracking --update-readme

  # 生成JSON统计报告
  python update-stats.py --format json --output stats.json
================================================================================
"""

import argparse
import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


class ProjectStats:
    """项目统计类"""
    
    # 形式化元素编号模式
    THEOREM_PATTERN = re.compile(r'(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d{2})-(\d{2})')
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.stats = {
            'Struct': {
                'files': 0,
                'theorems': 0,
                'definitions': 0,
                'lemmas': 0,
                'propositions': 0,
                'corollaries': 0
            },
            'Knowledge': {
                'files': 0,
                'theorems': 0,
                'definitions': 0,
                'patterns': 0,
                'scenarios': 0
            },
            'Flink': {
                'files': 0,
                'theorems': 0,
                'definitions': 0,
                'mechanisms': 0
            },
            'total': {
                'files': 0,
                'theorems': 0,
                'definitions': 0,
                'formal_elements': 0
            },
            'timestamp': datetime.now().isoformat()
        }
        self.changes_detected = False
    
    def log(self, message: str):
        """打印日志（仅在verbose模式）"""
        if self.verbose:
            print(message)
    
    def scan_directory(self, dir_name: str) -> List[Path]:
        """扫描目录中的Markdown文件"""
        dir_path = Path(dir_name)
        if not dir_path.exists():
            self.log(f"目录不存在: {dir_name}")
            return []
        
        md_files = [
            f for f in dir_path.rglob('*.md')
            if not any(p.startswith('.') for p in f.parts)
        ]
        
        self.log(f"{dir_name}: 发现 {len(md_files)} 个Markdown文件")
        return md_files
    
    def count_formal_elements(self, content: str, stage: str) -> Dict[str, int]:
        """统计内容中的形式化元素"""
        elements = {
            'theorems': 0,
            'definitions': 0,
            'lemmas': 0,
            'propositions': 0,
            'corollaries': 0
        }
        
        for match in self.THEOREM_PATTERN.finditer(content):
            elem_type = match.group(1)
            elem_stage = match.group(2)
            
            # 只统计对应阶段的元素
            stage_map = {'S': 'Struct', 'K': 'Knowledge', 'F': 'Flink'}
            if elem_stage != stage[0].upper():
                continue
            
            if elem_type == 'Thm':
                elements['theorems'] += 1
            elif elem_type == 'Def':
                elements['definitions'] += 1
            elif elem_type == 'Lemma':
                elements['lemmas'] += 1
            elif elem_type == 'Prop':
                elements['propositions'] += 1
            elif elem_type == 'Cor':
                elements['corollaries'] += 1
        
        return elements
    
    def gather_stats(self) -> Dict:
        """收集项目统计信息"""
        print("=" * 70)
        print("📊 正在收集项目统计信息...")
        print("=" * 70)
        
        for dir_name in ['Struct', 'Knowledge', 'Flink']:
            md_files = self.scan_directory(dir_name)
            self.stats[dir_name]['files'] = len(md_files)
            self.stats['total']['files'] += len(md_files)
            
            # 统计形式化元素
            for md_file in md_files:
                try:
                    content = md_file.read_text(encoding='utf-8')
                    elements = self.count_formal_elements(
                        content, 
                        dir_name[0].upper()
                    )
                    
                    for key, value in elements.items():
                        if key in self.stats[dir_name]:
                            self.stats[dir_name][key] += value
                        if key in ['theorems', 'definitions']:
                            self.stats['total'][key] += value
                            
                except Exception as e:
                    self.log(f"⚠️  无法读取 {md_file}: {e}")
        
        # 计算总形式化元素
        self.stats['total']['formal_elements'] = (
            self.stats['total']['theorems'] + 
            self.stats['total']['definitions']
        )
        
        return self.stats
    
    def print_stats(self):
        """打印统计信息"""
        print("\n" + "=" * 70)
        print("📈 项目统计报告")
        print("=" * 70)
        
        for dir_name in ['Struct', 'Knowledge', 'Flink']:
            dir_stats = self.stats[dir_name]
            print(f"\n📁 {dir_name}/")
            print(f"  文档数: {dir_stats['files']}")
            
            if 'theorems' in dir_stats and dir_stats['theorems'] > 0:
                print(f"  定理: {dir_stats['theorems']}")
            if 'definitions' in dir_stats and dir_stats['definitions'] > 0:
                print(f"  定义: {dir_stats['definitions']}")
            if 'lemmas' in dir_stats and dir_stats['lemmas'] > 0:
                print(f"  引理: {dir_stats['lemmas']}")
            if 'propositions' in dir_stats and dir_stats['propositions'] > 0:
                print(f"  命题: {dir_stats['propositions']}")
            if 'corollaries' in dir_stats and dir_stats['corollaries'] > 0:
                print(f"  推论: {dir_stats['corollaries']}")
        
        print("\n📊 总计")
        print(f"  总文档数: {self.stats['total']['files']}")
        print(f"  总定理数: {self.stats['total']['theorems']}")
        print(f"  总定义数: {self.stats['total']['definitions']}")
        print(f"  形式化元素总数: {self.stats['total']['formal_elements']}")
        print("=" * 70)
    
    def update_project_tracking(self) -> bool:
        """更新 PROJECT-TRACKING.md 文件"""
        tracking_path = Path('PROJECT-TRACKING.md')
        
        if not tracking_path.exists():
            print(f"⚠️  {tracking_path} 不存在，跳过更新")
            return False
        
        try:
            content = tracking_path.read_text(encoding='utf-8')
            original_content = content
            
            # 更新各目录文档数
            for dir_name in ['Struct', 'Knowledge', 'Flink']:
                count = self.stats[dir_name]['files']
                
                # 更新形如 "Struct/: [████] 100% (43文档" 的格式
                pattern = rf'({dir_name}/.*?\[.*?)\d+(%.*?\()\d+(文档)'
                replacement = rf'\g<1>{count // 10 * 10}\g<2>{count}\g<3>'
                content = re.sub(pattern, replacement, content)
                
                # 简化更新：只更新数字部分
                pattern2 = rf'({dir_name}/.*?\[.*?\].*?\d+%.*?\()\d+(文档)'
                content = re.sub(pattern2, rf'\g<1>{count}\g<2>', content)
            
            # 更新时间戳
            now = datetime.now().strftime('%Y-%m-%d')
            content = re.sub(
                r'(最后更新[：:]?\s*)\d{4}-\d{2}-\d{2',
                rf'\g<1>{now}',
                content
            )
            
            # 检查是否有变化
            if content != original_content:
                tracking_path.write_text(content, encoding='utf-8')
                print(f"✅ 已更新 {tracking_path}")
                self.changes_detected = True
                return True
            else:
                print(f"ℹ️  {tracking_path} 无需更新")
                return False
                
        except Exception as e:
            print(f"❌ 更新 {tracking_path} 失败: {e}")
            return False
    
    def update_readme(self) -> bool:
        """更新 README.md 文件"""
        readme_path = Path('README.md')
        
        if not readme_path.exists():
            print(f"⚠️  {readme_path} 不存在，跳过更新")
            return False
        
        try:
            content = readme_path.read_text(encoding='utf-8')
            original_content = content
            
            # 更新统计信息
            total_files = self.stats['total']['files']
            total_theorems = self.stats['total']['theorems']
            
            # 更新总计行
            content = re.sub(
                r'\*\*总计[:：]?\s*\d+\s*篇.*?\d+.*?形式化元素\*\*',
                f'**总计: {total_files} 篇技术文档 | {self.stats["total"]["formal_elements"]} 形式化元素**',
                content
            )
            
            # 更新各阶段统计
            for dir_name in ['Struct', 'Knowledge', 'Flink']:
                count = self.stats[dir_name]['files']
                theorems = self.stats[dir_name].get('theorems', 0)
                definitions = self.stats[dir_name].get('definitions', 0)
                
                # 更新表格中的统计信息
                pattern = rf'(\| \*\*{dir_name}/\*\* \| .*?\|.*?\| )\d+文档.*?( \|)'
                if dir_name == 'Struct':
                    replacement = rf'\g<1>{count}文档, {theorems}定理, {definitions}定义\g<2>'
                else:
                    replacement = rf'\g<1>{count}文档\g<2>'
                content = re.sub(pattern, replacement, content)
            
            # 检查是否有变化
            if content != original_content:
                readme_path.write_text(content, encoding='utf-8')
                print(f"✅ 已更新 {readme_path}")
                self.changes_detected = True
                return True
            else:
                print(f"ℹ️  {readme_path} 无需更新")
                return False
                
        except Exception as e:
            print(f"❌ 更新 {readme_path} 失败: {e}")
            return False
    
    def generate_json_report(self) -> str:
        """生成JSON格式报告"""
        return json.dumps(self.stats, indent=2, ensure_ascii=False)
    
    def generate_markdown_report(self) -> str:
        """生成Markdown格式报告"""
        report = f"""# 项目统计报告

**生成时间:** {self.stats['timestamp']}

## 目录统计

| 目录 | 文档数 | 定理 | 定义 | 其他 |
|------|--------|------|------|------|
"""
        
        for dir_name in ['Struct', 'Knowledge', 'Flink']:
            s = self.stats[dir_name]
            others = []
            if s.get('lemmas', 0) > 0:
                others.append(f"{s['lemmas']}引理")
            if s.get('propositions', 0) > 0:
                others.append(f"{s['propositions']}命题")
            if s.get('corollaries', 0) > 0:
                others.append(f"{s['corollaries']}推论")
            
            others_str = ', '.join(others) if others else '-'
            
            report += f"| {dir_name} | {s['files']} | {s.get('theorems', 0)} | {s.get('definitions', 0)} | {others_str} |\n"
        
        report += f"""
## 总计

- **总文档数:** {self.stats['total']['files']}
- **总定理数:** {self.stats['total']['theorems']}
- **总定义数:** {self.stats['total']['definitions']}
- **形式化元素总数:** {self.stats['total']['formal_elements']}

---
*由自动统计脚本生成*
"""
        return report


def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 统计更新工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python update-stats.py --check-only
  python update-stats.py --update-tracking --update-readme
  python update-stats.py --format json --output stats.json
        """
    )
    
    parser.add_argument(
        '--check-only',
        action='store_true',
        help='仅检查，不更新文件'
    )
    parser.add_argument(
        '--update-tracking',
        action='store_true',
        help='更新 PROJECT-TRACKING.md'
    )
    parser.add_argument(
        '--update-readme',
        action='store_true',
        help='更新 README.md'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'markdown'],
        default='text',
        help='输出格式（默认text）'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='输出文件路径'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细信息'
    )
    
    args = parser.parse_args()
    
    # 创建统计器
    stats = ProjectStats(verbose=args.verbose)
    
    # 收集统计信息
    stats.gather_stats()
    
    # 打印统计
    stats.print_stats()
    
    # 生成输出
    output = None
    if args.format == 'json':
        output = stats.generate_json_report()
        print("\n" + output)
    elif args.format == 'markdown':
        output = stats.generate_markdown_report()
        print("\n" + output)
    
    # 保存到文件
    if args.output and output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"\n报告已保存到: {args.output}")
    
    # 更新文件
    if not args.check_only:
        if args.update_tracking:
            stats.update_project_tracking()
        
        if args.update_readme:
            stats.update_readme()
        
        if not args.update_tracking and not args.update_readme:
            print("\nℹ️  使用 --update-tracking 和/或 --update-readme 来更新文件")
    
    # 返回退出码
    return 0 if not stats.changes_detected else 1


if __name__ == '__main__':
    sys.exit(main())
