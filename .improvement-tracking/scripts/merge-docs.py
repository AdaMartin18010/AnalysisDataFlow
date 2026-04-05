#!/usr/bin/env python3
"""
文档合并辅助脚本

功能：
1. 分析重复文件内容相似度
2. 生成合并建议
3. 执行安全合并（备份、合并、验证）
4. 更新内部链接引用
5. 生成合并报告

使用方法：
    python merge-docs.py --analyze              # 仅分析重复内容
    python merge-docs.py --plan --group DUP-001 # 生成特定组合并计划
    python merge-docs.py --execute --group DUP-001 --dry-run  # 模拟执行合并
    python merge-docs.py --execute --group DUP-001             # 实际执行合并
    python merge-docs.py --update-links --file path/to/file.md # 更新文件中的链接
"""

import argparse
import json
import hashlib
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from difflib import SequenceMatcher

# 项目根目录
PROJECT_ROOT = Path("e:/_src/AnalysisDataFlow")
ANALYSIS_FILE = PROJECT_ROOT / ".improvement-tracking/duplicate-content-analysis.json"
BACKUP_DIR = PROJECT_ROOT / ".improvement-tracking/backups"


class DocumentAnalyzer:
    """文档分析器"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.analysis_data = None
        
    def load_analysis(self) -> dict:
        """加载重复内容分析数据"""
        with open(ANALYSIS_FILE, 'r', encoding='utf-8') as f:
            self.analysis_data = json.load(f)
        return self.analysis_data
    
    def calculate_similarity(self, file1: Path, file2: Path) -> float:
        """计算两个文件的相似度 (0-1)"""
        try:
            content1 = self._read_file(file1)
            content2 = self._read_file(file2)
            
            # 使用SequenceMatcher计算相似度
            similarity = SequenceMatcher(None, content1, content2).ratio()
            return round(similarity, 2)
        except Exception as e:
            print(f"计算相似度时出错: {e}")
            return 0.0
    
    def _read_file(self, filepath: Path) -> str:
        """读取文件内容"""
        full_path = self.project_root / filepath
        if not full_path.exists():
            return ""
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    def extract_headings(self, filepath: Path) -> List[str]:
        """提取文档中的所有标题"""
        content = self._read_file(filepath)
        # 匹配 Markdown 标题
        headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        return headings
    
    def extract_definitions(self, filepath: Path) -> List[dict]:
        """提取文档中的所有定义"""
        content = self._read_file(filepath)
        definitions = []
        
        # 匹配 Def-* 格式的定义
        pattern = r'###\s+(Def-[A-Z]-\d+[\d-]*):\s*(.+?)\n\n(.+?)(?=###|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            definitions.append({
                'id': match[0],
                'name': match[1].strip(),
                'content': match[2].strip()[:200] + '...' if len(match[2]) > 200 else match[2].strip()
            })
        
        return definitions
    
    def extract_code_blocks(self, filepath: Path) -> List[dict]:
        """提取文档中的所有代码块"""
        content = self._read_file(filepath)
        code_blocks = []
        
        # 匹配代码块
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for lang, code in matches:
            code_blocks.append({
                'language': lang or 'text',
                'content': code.strip()[:100] + '...' if len(code) > 100 else code.strip(),
                'hash': hashlib.md5(code.encode()).hexdigest()[:8]
            })
        
        return code_blocks
    
    def compare_documents(self, file1: Path, file2: Path) -> dict:
        """详细比较两个文档"""
        result = {
            'file1': str(file1),
            'file2': str(file2),
            'similarity_score': self.calculate_similarity(file1, file2),
            'headings_file1': self.extract_headings(file1),
            'headings_file2': self.extract_headings(file2),
            'common_headings': [],
            'unique_to_file1': [],
            'unique_to_file2': [],
            'definitions_file1': len(self.extract_definitions(file1)),
            'definitions_file2': len(self.extract_definitions(file2)),
            'code_blocks_file1': len(self.extract_code_blocks(file1)),
            'code_blocks_file2': len(self.extract_code_blocks(file2)),
        }
        
        set1 = set(result['headings_file1'])
        set2 = set(result['headings_file2'])
        
        result['common_headings'] = list(set1 & set2)
        result['unique_to_file1'] = list(set1 - set2)
        result['unique_to_file2'] = list(set2 - set1)
        
        return result


class MergePlanner:
    """合并计划生成器"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.analyzer = DocumentAnalyzer(project_root)
        
    def generate_merge_plan(self, group_id: str) -> dict:
        """为特定重复组生成详细合并计划"""
        analysis = self.analyzer.load_analysis()
        
        group = None
        for g in analysis.get('duplicate_groups', []):
            if g['id'] == group_id:
                group = g
                break
        
        if not group:
            raise ValueError(f"未找到重复组: {group_id}")
        
        plan = {
            'group_id': group_id,
            'topic': group['topic'],
            'generated_at': datetime.now().isoformat(),
            'primary_file': group['primary_file'],
            'files_to_merge': [],
            'detailed_comparison': [],
            'merge_steps': [],
            'risks': [],
            'estimated_time_minutes': 0
        }
        
        primary_path = Path(group['primary_file'])
        
        # 详细比较每个从文档与主文档
        for file_info in group['files']:
            file_path = Path(file_info['path'])
            if file_path == primary_path:
                continue
            
            comparison = self.analyzer.compare_documents(primary_path, file_path)
            plan['detailed_comparison'].append(comparison)
            
            # 识别独特内容
            unique_content = {
                'file': str(file_path),
                'unique_headings': comparison['unique_to_file2'],
                'unique_definitions': [],
                'unique_code_examples': []
            }
            plan['files_to_merge'].append(unique_content)
        
        # 生成合并步骤
        plan['merge_steps'] = self._generate_steps(group, plan['files_to_merge'])
        
        # 识别风险
        plan['risks'] = self._identify_risks(group, plan['detailed_comparison'])
        
        # 估算时间
        plan['estimated_time_minutes'] = self._estimate_time(group, plan)
        
        return plan
    
    def _generate_steps(self, group: dict, files_to_merge: List[dict]) -> List[dict]:
        """生成合并步骤"""
        steps = []
        
        # 步骤1: 备份
        steps.append({
            'order': 1,
            'action': 'backup',
            'description': '备份所有涉及文件',
            'commands': [
                f"mkdir -p {BACKUP_DIR}/{group['id']}",
                f"cp {{file}} {BACKUP_DIR}/{group['id']}/"
            ]
        })
        
        # 步骤2: 整合内容
        steps.append({
            'order': 2,
            'action': 'merge_content',
            'description': f"整合内容到主文档: {group['primary_file']}",
            'details': '将每个从文档的独特内容章节插入到主文档适当位置'
        })
        
        # 步骤3: 更新定义编号
        steps.append({
            'order': 3,
            'action': 'normalize_definitions',
            'description': '统一定义编号格式',
            'details': '确保所有 Def-* 编号符合项目规范且不冲突'
        })
        
        # 步骤4: 更新链接
        steps.append({
            'order': 4,
            'action': 'update_links',
            'description': '更新所有指向被删除文件的链接',
            'details': '扫描整个项目，更新相对链接指向新的主文档'
        })
        
        # 步骤5: 删除重复文件
        steps.append({
            'order': 5,
            'action': 'delete_duplicates',
            'description': '删除已合并的重复文件',
            'files_to_delete': [f['path'] for f in group['files'] if f['path'] != group['primary_file']]
        })
        
        # 步骤6: 验证
        steps.append({
            'order': 6,
            'action': 'verify',
            'description': '验证合并结果',
            'checks': [
                '主文档可正常打开',
                '所有内部链接有效',
                'Mermaid 图可渲染',
                '六段式结构完整'
            ]
        })
        
        return steps
    
    def _identify_risks(self, group: dict, comparisons: List[dict]) -> List[dict]:
        """识别合并风险"""
        risks = []
        
        # 检查相似度
        for comp in comparisons:
            if comp['similarity_score'] > 0.9:
                risks.append({
                    'level': 'high',
                    'type': 'high_similarity',
                    'description': f"{comp['file2']} 与主文档相似度高达 {comp['similarity_score']}，可能内容几乎相同",
                    'mitigation': '仔细检查是否有独特内容需要保留'
                })
        
        # 检查定义冲突
        total_defs = sum(c['definitions_file1'] + c['definitions_file2'] for c in comparisons)
        if total_defs > 20:
            risks.append({
                'level': 'medium',
                'type': 'many_definitions',
                'description': f'涉及 {total_defs} 个定义，编号冲突风险较高',
                'mitigation': '使用定理注册表验证所有编号唯一性'
            })
        
        return risks
    
    def _estimate_time(self, group: dict, plan: dict) -> int:
        """估算合并所需时间（分钟）"""
        base_time = 30  # 基础时间
        
        # 根据文件数量
        file_count = len(group['files'])
        base_time += file_count * 15
        
        # 根据风险等级
        for risk in plan['risks']:
            if risk['level'] == 'high':
                base_time += 30
            elif risk['level'] == 'medium':
                base_time += 15
        
        return base_time


class MergeExecutor:
    """合并执行器"""
    
    def __init__(self, project_root: Path, dry_run: bool = False):
        self.project_root = project_root
        self.dry_run = dry_run
        self.analyzer = DocumentAnalyzer(project_root)
        
    def backup_files(self, group_id: str, files: List[str]) -> Path:
        """备份文件"""
        backup_path = BACKUP_DIR / group_id / datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if self.dry_run:
            print(f"[DRY-RUN] 将创建备份目录: {backup_path}")
            return backup_path
        
        backup_path.mkdir(parents=True, exist_ok=True)
        
        for file_path in files:
            src = self.project_root / file_path
            if src.exists():
                dst = backup_path / Path(file_path).name
                shutil.copy2(src, dst)
                print(f"已备份: {file_path} -> {dst}")
        
        return backup_path
    
    def merge_content(self, primary_file: str, secondary_files: List[str]) -> str:
        """合并内容（返回合并后的内容）"""
        primary_path = self.project_root / primary_file
        primary_content = self.analyzer._read_file(primary_path)
        
        merged_content = primary_content
        
        for sec_file in secondary_files:
            sec_path = self.project_root / sec_file
            if not sec_path.exists():
                continue
            
            sec_content = self.analyzer._read_file(sec_path)
            
            # 提取独特章节
            unique_sections = self._extract_unique_sections(primary_content, sec_content)
            
            # 将独特章节添加到主文档
            for section in unique_sections:
                merged_content = self._insert_section(merged_content, section)
        
        return merged_content
    
    def _extract_unique_sections(self, primary: str, secondary: str) -> List[str]:
        """提取从文档中与主文档不同的章节"""
        # 简化实现：按二级标题分割，比较每个章节
        secondary_sections = re.split(r'\n## ', secondary)
        primary_sections = re.split(r'\n## ', primary)
        primary_set = set(s.strip()[:100] for s in primary_sections)
        
        unique = []
        for sec in secondary_sections:
            sec_preview = sec.strip()[:100]
            if sec_preview and sec_preview not in primary_set:
                unique.append('## ' + sec if not sec.startswith('##') else sec)
        
        return unique
    
    def _insert_section(self, content: str, section: str) -> str:
        """将章节插入到内容适当位置"""
        # 简化实现：添加到文档末尾的 "## 引用参考" 之前
        ref_match = re.search(r'\n## \d*\.?\s*引用参考', content)
        if ref_match:
            pos = ref_match.start()
            return content[:pos] + '\n' + section + '\n' + content[pos:]
        else:
            return content + '\n' + section
    
    def update_links_in_file(self, filepath: Path, old_refs: List[str], new_ref: str) -> int:
        """更新文件中的链接引用"""
        content = self.analyzer._read_file(filepath)
        original_content = content
        
        for old_ref in old_refs:
            # 匹配相对链接 [text](./old_ref) 或 [text](../old_ref)
            pattern = r'\[([^\]]+)\]\([^)]*' + re.escape(old_ref) + r'[^)]*\)'
            replacement = r'[\1](' + new_ref + r')'
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            if not self.dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            return 1
        return 0
    
    def scan_and_update_links(self, old_refs: List[str], new_ref: str) -> dict:
        """扫描整个项目并更新链接"""
        stats = {
            'files_scanned': 0,
            'files_updated': 0,
            'total_replacements': 0
        }
        
        for pattern in ['Flink/**/*.md', 'Knowledge/**/*.md', 'Struct/**/*.md']:
            for md_file in self.project_root.glob(pattern):
                stats['files_scanned'] += 1
                
                if self.update_links_in_file(md_file, old_refs, new_ref):
                    stats['files_updated'] += 1
                    stats['total_replacements'] += len(old_refs)
                    print(f"{'[DRY-RUN] ' if self.dry_run else ''}更新链接: {md_file}")
        
        return stats
    
    def delete_file(self, filepath: str) -> bool:
        """删除文件"""
        full_path = self.project_root / filepath
        
        if self.dry_run:
            print(f"[DRY-RUN] 将删除文件: {filepath}")
            return True
        
        if full_path.exists():
            full_path.unlink()
            print(f"已删除: {filepath}")
            return True
        return False
    
    def execute_merge(self, group_id: str) -> dict:
        """执行完整合并流程"""
        analysis = self.analyzer.load_analysis()
        
        group = None
        for g in analysis.get('duplicate_groups', []):
            if g['id'] == group_id:
                group = g
                break
        
        if not group:
            raise ValueError(f"未找到重复组: {group_id}")
        
        result = {
            'group_id': group_id,
            'success': True,
            'steps_executed': [],
            'errors': []
        }
        
        try:
            # 1. 备份
            files_to_backup = [f['path'] for f in group['files']]
            backup_path = self.backup_files(group_id, files_to_backup)
            result['steps_executed'].append({'step': 'backup', 'backup_path': str(backup_path)})
            
            # 2. 合并内容
            primary = group['primary_file']
            secondary = [f['path'] for f in group['files'] if f['path'] != primary]
            merged_content = self.merge_content(primary, secondary)
            
            if not self.dry_run:
                with open(self.project_root / primary, 'w', encoding='utf-8') as f:
                    f.write(merged_content)
            result['steps_executed'].append({'step': 'merge_content', 'primary': primary})
            
            # 3. 更新链接
            old_refs = [f['path'] for f in group['files'] if f['path'] != primary]
            link_stats = self.scan_and_update_links(old_refs, primary)
            result['steps_executed'].append({'step': 'update_links', 'stats': link_stats})
            
            # 4. 删除重复文件
            deleted = []
            for f in group['files']:
                if f['path'] != primary:
                    if self.delete_file(f['path']):
                        deleted.append(f['path'])
            result['steps_executed'].append({'step': 'delete_duplicates', 'deleted': deleted})
            
        except Exception as e:
            result['success'] = False
            result['errors'].append(str(e))
        
        return result


def main():
    parser = argparse.ArgumentParser(description='文档合并辅助工具')
    parser.add_argument('--analyze', action='store_true', help='分析重复内容')
    parser.add_argument('--plan', action='store_true', help='生成合并计划')
    parser.add_argument('--execute', action='store_true', help='执行合并')
    parser.add_argument('--group', type=str, help='指定重复组ID (如: DUP-001)')
    parser.add_argument('--dry-run', action='store_true', help='模拟执行，不实际修改')
    parser.add_argument('--update-links', action='store_true', help='更新链接')
    parser.add_argument('--file', type=str, help='指定文件路径')
    parser.add_argument('--old-refs', nargs='+', help='旧引用路径列表')
    parser.add_argument('--new-ref', type=str, help='新引用路径')
    parser.add_argument('--compare', nargs=2, metavar=('FILE1', 'FILE2'), help='比较两个文件')
    
    args = parser.parse_args()
    
    analyzer = DocumentAnalyzer(PROJECT_ROOT)
    planner = MergePlanner(PROJECT_ROOT)
    executor = MergeExecutor(PROJECT_ROOT, dry_run=args.dry_run)
    
    if args.analyze:
        print("=" * 60)
        print("重复内容分析报告")
        print("=" * 60)
        
        analysis = analyzer.load_analysis()
        summary = analysis.get('summary', {})
        
        print(f"\n扫描统计:")
        print(f"  - 重复组数量: {summary.get('total_duplicate_groups', 0)}")
        print(f"  - 涉及文件总数: {summary.get('total_duplicate_files', 0)}")
        print(f"  - 待删除文件: {summary.get('files_to_delete', 0)}")
        print(f"  - 预计工作量: {summary.get('total_estimated_effort_hours', 0)} 小时")
        
        print(f"\n优先级分布:")
        prio_dist = summary.get('priority_distribution', {})
        for p, c in sorted(prio_dist.items()):
            print(f"  - {p}: {c} 组")
        
        print(f"\n重复组列表:")
        for group in analysis.get('duplicate_groups', []):
            print(f"\n  [{group['id']}] {group['topic']}")
            print(f"    优先级: {group['priority']} | 相似度: {group['similarity_score']}")
            print(f"    主文档: {group['primary_file']}")
            print(f"    涉及文件: {len(group['files'])} 个")
    
    elif args.plan:
        if not args.group:
            print("错误: --plan 需要配合 --group 指定重复组ID")
            sys.exit(1)
        
        print(f"\n正在生成合并计划: {args.group}")
        print("=" * 60)
        
        try:
            plan = planner.generate_merge_plan(args.group)
            
            print(f"\n主题: {plan['topic']}")
            print(f"主文档: {plan['primary_file']}")
            print(f"预计时间: {plan['estimated_time_minutes']} 分钟")
            
            print(f"\n合并步骤:")
            for step in plan['merge_steps']:
                print(f"  {step['order']}. [{step['action']}] {step['description']}")
            
            if plan['risks']:
                print(f"\n风险提示:")
                for risk in plan['risks']:
                    print(f"  [{risk['level'].upper()}] {risk['description']}")
                    print(f"    缓解措施: {risk['mitigation']}")
            
            # 保存计划到文件
            plan_file = PROJECT_ROOT / f".improvement-tracking/merge-plan-{args.group}.json"
            with open(plan_file, 'w', encoding='utf-8') as f:
                json.dump(plan, f, indent=2, ensure_ascii=False)
            print(f"\n计划已保存到: {plan_file}")
            
        except ValueError as e:
            print(f"错误: {e}")
            sys.exit(1)
    
    elif args.execute:
        if not args.group:
            print("错误: --execute 需要配合 --group 指定重复组ID")
            sys.exit(1)
        
        mode = "[模拟执行]" if args.dry_run else "[实际执行]"
        print(f"\n{mode} 执行合并: {args.group}")
        print("=" * 60)
        
        result = executor.execute_merge(args.group)
        
        print(f"\n执行结果:")
        print(f"  成功: {result['success']}")
        print(f"  执行步骤: {len(result['steps_executed'])}")
        
        if result['errors']:
            print(f"\n错误:")
            for err in result['errors']:
                print(f"  - {err}")
        
        # 保存结果
        result_file = PROJECT_ROOT / f".improvement-tracking/merge-result-{args.group}.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n结果已保存到: {result_file}")
    
    elif args.update_links:
        if not args.old_refs or not args.new_ref:
            print("错误: --update-links 需要 --old-refs 和 --new-ref")
            sys.exit(1)
        
        print(f"\n更新链接引用:")
        print(f"  旧引用: {args.old_refs}")
        print(f"  新引用: {args.new_ref}")
        
        stats = executor.scan_and_update_links(args.old_refs, args.new_ref)
        
        print(f"\n统计:")
        print(f"  扫描文件: {stats['files_scanned']}")
        print(f"  更新文件: {stats['files_updated']}")
        print(f"  替换次数: {stats['total_replacements']}")
    
    elif args.compare:
        file1, file2 = args.compare
        print(f"\n比较文件:")
        print(f"  文件1: {file1}")
        print(f"  文件2: {file2}")
        print("=" * 60)
        
        result = analyzer.compare_documents(file1, file2)
        
        print(f"\n相似度: {result['similarity_score']}")
        print(f"\n共同标题 ({len(result['common_headings'])}):")
        for h in result['common_headings'][:10]:
            print(f"  - {h}")
        if len(result['common_headings']) > 10:
            print(f"  ... 还有 {len(result['common_headings']) - 10} 个")
        
        print(f"\n文件1独特标题 ({len(result['unique_to_file1'])}):")
        for h in result['unique_to_file1'][:5]:
            print(f"  - {h}")
        
        print(f"\n文件2独特标题 ({len(result['unique_to_file2'])}):")
        for h in result['unique_to_file2'][:5]:
            print(f"  - {h}")
        
        print(f"\n定义数量: 文件1={result['definitions_file1']}, 文件2={result['definitions_file2']}")
        print(f"代码块数量: 文件1={result['code_blocks_file1']}, 文件2={result['code_blocks_file2']}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
