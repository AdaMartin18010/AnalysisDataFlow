#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
形式化元素自动编号工具 (Formal Element Tracker)

功能：
- 扫描所有文档中的形式化元素
- 检测编号冲突和重复
- 自动建议新编号
- 生成全局形式化元素索引
- 检查编号连续性
- 可更新 THEOREM-REGISTRY.md

作者: Automation Agent
版本: 1.0.0
"""

import re
import json
import argparse
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Set, Optional, Tuple, Any
from collections import defaultdict
from datetime import datetime
from enum import Enum

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ElementType(Enum):
    """形式化元素类型"""
    DEFINITION = "Def"
    THEOREM = "Thm"
    LEMMA = "Lemma"
    PROPOSITION = "Prop"
    COROLLARY = "Cor"


class Stage(Enum):
    """阶段"""
    STRUCT = "S"
    KNOWLEDGE = "K"
    FLINK = "F"


@dataclass
class FormalElement:
    """形式化元素数据类"""
    element_type: str
    stage: str
    doc_num: str
    seq_num: str
    full_id: str
    file_path: str
    line_number: int
    context: str
    title: str = ""
    description: str = ""
    dependencies: List[str] = field(default_factory=list)
    
    def __hash__(self):
        return hash(self.full_id)
        
    def __eq__(self, other):
        if isinstance(other, FormalElement):
            return self.full_id == other.full_id
        return False


@dataclass
class ConflictInfo:
    """冲突信息"""
    element_id: str
    elements: List[FormalElement]
    conflict_type: str  # duplicate, gap, format_error
    message: str


@dataclass
class TrackingResult:
    """追踪结果"""
    elements: Dict[str, List[FormalElement]] = field(default_factory=lambda: defaultdict(list))
    conflicts: List[ConflictInfo] = field(default_factory=list)
    statistics: Dict[str, Any] = field(default_factory=dict)
    suggestions: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))


class FormalElementTracker:
    """形式化元素追踪器"""
    
    # 形式化元素编号正则
    FORMAL_PATTERN = re.compile(
        r'`(Def|Thm|Theorem|Lemma|Prop|Proposition|Cor|Corollary)'  # 类型
        r'[-\s]*'  # 分隔符
        r'([SKF])'  # 阶段
        r'[-\s]*'  # 分隔符
        r'(\d+)'  # 文档序号
        r'[-\s]*'  # 分隔符
        r'(\d+)`',  # 顺序号
        re.IGNORECASE
    )
    
    # 非标准格式检测
    NON_STANDARD_PATTERN = re.compile(
        r'(Def|Thm|Theorem|Lemma|Prop|Proposition|Cor|Corollary)'
        r'\s*[-–—]\s*'
        r'([^`\n]+)',
        re.IGNORECASE
    )
    
    # 标题提取
    TITLE_PATTERNS = [
        re.compile(r'(?:定义|定理|引理|命题|推论)\s*[:：]\s*(.+?)(?:\n|$)', re.IGNORECASE),
        re.compile(r'`[^`]+`\s*[:：]\s*(.+?)(?:\n|$)'),
        re.compile(r'#{3,}\s+(.+?)(?:\n|$)'),
    ]
    
    # 依赖关系检测
    DEPENDENCY_PATTERNS = [
        re.compile(r'(?:依赖|depends?\s*on|see|refer\s*to)\s*`(Thm|Def|Lemma|Prop|Cor)-[^`]+`', re.IGNORECASE),
        re.compile(r'(?:由|根据|基于)\s*`(Thm|Def|Lemma|Prop|Cor)-[^`]+`'),
    ]
    
    # 类型映射
    TYPE_MAPPING = {
        'Theorem': 'Thm',
        'Proposition': 'Prop',
        'Corollary': 'Cor',
    }
    
    # 阶段映射
    STAGE_MAPPING = {
        'Struct': 'S',
        'Knowledge': 'K',
        'Flink': 'F',
    }
    
    def __init__(
        self,
        root_dir: Path,
        registry_file: Optional[Path] = None,
        skip_patterns: Optional[List[str]] = None
    ):
        """
        初始化追踪器
        
        Args:
            root_dir: 项目根目录
            registry_file: 定理注册表文件路径
            skip_patterns: 跳过的文件模式
        """
        self.root_dir = Path(root_dir).resolve()
        self.registry_file = registry_file
        self.skip_patterns = skip_patterns or [
            'node_modules', '.git', '__pycache__',
            '.venv', 'venv', 'archive'
        ]
        self.element_counter: Dict[str, int] = defaultdict(int)
        
    def _should_skip_file(self, file_path: Path) -> bool:
        """判断是否应该跳过文件"""
        path_str = str(file_path)
        return any(pattern in path_str for pattern in self.skip_patterns)
        
    def _extract_title(self, content: str, element_pos: int) -> str:
        """从元素位置提取标题"""
        # 获取元素所在行及其后几行
        lines = content[:element_pos].split('\n')
        after_lines = content[element_pos:].split('\n')
        
        context = '\n'.join(lines[-3:] + after_lines[:3])
        
        for pattern in self.TITLE_PATTERNS:
            match = pattern.search(context)
            if match:
                title = match.group(1).strip()
                # 限制长度
                if len(title) > 100:
                    title = title[:97] + "..."
                return title
                
        return ""
        
    def _extract_dependencies(self, content: str, element_pos: int) -> List[str]:
        """提取依赖关系"""
        deps = []
        after_content = content[element_pos:element_pos + 2000]
        
        for pattern in self.DEPENDENCY_PATTERNS:
            for match in pattern.finditer(after_content):
                dep = match.group(0)
                # 提取ID
                id_match = re.search(r'(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d+-\d+', dep)
                if id_match:
                    deps.append(id_match.group(0))
                    
        return list(set(deps))
        
    def scan_file(self, file_path: Path) -> List[FormalElement]:
        """
        扫描单个文件中的形式化元素
        
        Args:
            file_path: Markdown文件路径
            
        Returns:
            形式化元素列表
        """
        elements = []
        rel_path = str(file_path.relative_to(self.root_dir))
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.warning(f"无法读取文件 {file_path}: {e}")
            return elements
            
        # 提取标准格式的形式化元素
        for match in self.FORMAL_PATTERN.finditer(content):
            element_type = match.group(1)
            stage = match.group(2).upper()
            doc_num = match.group(3)
            seq_num = match.group(4)
            
            # 标准化类型
            element_type = self.TYPE_MAPPING.get(element_type, element_type)
            
            # 确保序号是两位数
            doc_num = f"{int(doc_num):02d}"
            seq_num = f"{int(seq_num):02d}"
            
            full_id = f"{element_type}-{stage}-{doc_num}-{seq_num}"
            
            # 计算行号
            line_number = content[:match.start()].count('\n') + 1
            
            # 提取上下文
            context_start = max(0, match.start() - 50)
            context_end = min(len(content), match.end() + 50)
            context = content[context_start:context_end].strip()
            
            # 提取标题
            title = self._extract_title(content, match.start())
            
            # 提取依赖
            deps = self._extract_dependencies(content, match.start())
            
            elements.append(FormalElement(
                element_type=element_type,
                stage=stage,
                doc_num=doc_num,
                seq_num=seq_num,
                full_id=full_id,
                file_path=rel_path,
                line_number=line_number,
                context=context,
                title=title,
                dependencies=deps
            ))
            
        # 检测非标准格式
        for match in self.NON_STANDARD_PATTERN.finditer(content):
            element_type = match.group(1)
            content_after = match.group(2).strip()
            
            # 检查是否已经是标准格式
            if self.FORMAL_PATTERN.search(match.group(0)):
                continue
                
            line_number = content[:match.start()].count('\n') + 1
            
            logger.debug(
                f"发现非标准格式: {file_path}:{line_number} - {match.group(0)[:50]}"
            )
            
        return elements
        
    def scan_directory(
        self,
        pattern: str = "**/*.md",
        stages: Optional[List[str]] = None
    ) -> TrackingResult:
        """
        扫描目录中的所有文件
        
        Args:
            pattern: 文件匹配模式
            stages: 只扫描指定阶段（S/K/F）
            
        Returns:
            追踪结果
        """
        result = TrackingResult()
        
        md_files = list(self.root_dir.glob(pattern))
        logger.info(f"发现 {len(md_files)} 个Markdown文件")
        
        for file_path in md_files:
            if self._should_skip_file(file_path):
                continue
                
            # 如果指定了阶段，检查文件路径
            if stages:
                rel_path = str(file_path.relative_to(self.root_dir))
                if not any(f"/{s}/" in rel_path or rel_path.startswith(f"{s}/") 
                          for s in ['Struct', 'Knowledge', 'Flink']):
                    continue
                    
            elements = self.scan_file(file_path)
            
            for elem in elements:
                result.elements[elem.full_id].append(elem)
                
        # 分析冲突
        result.conflicts = self._analyze_conflicts(result.elements)
        
        # 生成统计
        result.statistics = self._generate_statistics(result.elements)
        
        # 生成建议
        result.suggestions = self._generate_suggestions(result)
        
        return result
        
    def _analyze_conflicts(
        self,
        elements: Dict[str, List[FormalElement]]
    ) -> List[ConflictInfo]:
        """分析冲突"""
        conflicts = []
        
        for elem_id, elems in elements.items():
            # 检测重复
            if len(elems) > 1:
                file_paths = [e.file_path for e in elems]
                conflicts.append(ConflictInfo(
                    element_id=elem_id,
                    elements=elems,
                    conflict_type="duplicate",
                    message=f"元素 '{elem_id}' 在 {len(elems)} 个位置重复定义: {', '.join(set(file_paths))}"
                ))
                
        # 检查编号连续性
        stage_type_groups: Dict[Tuple[str, str], List[int]] = defaultdict(list)
        
        for elem_id, elems in elements.items():
            if elems:
                elem = elems[0]
                key = (elem.stage, elem.element_type)
                seq_num = int(elem.seq_num)
                stage_type_groups[key].append(seq_num)
                
        for (stage, elem_type), seq_nums in stage_type_groups.items():
            seq_nums = sorted(set(seq_nums))
            expected = list(range(1, max(seq_nums) + 1))
            
            missing = set(expected) - set(seq_nums)
            for m in sorted(missing):
                suggested_id = f"{elem_type}-{stage}-XX-{m:02d}"
                conflicts.append(ConflictInfo(
                    element_id=suggested_id,
                    elements=[],
                    conflict_type="gap",
                    message=f"{elem_type}-{stage} 序列中缺少编号 {m:02d}"
                ))
                
        return conflicts
        
    def _generate_statistics(
        self,
        elements: Dict[str, List[FormalElement]]
    ) -> Dict[str, Any]:
        """生成统计信息"""
        stats = {
            'total_unique_elements': len(elements),
            'total_definitions': 0,
            'total_theorems': 0,
            'total_lemmas': 0,
            'total_propositions': 0,
            'total_corollaries': 0,
            'by_stage': defaultdict(lambda: defaultdict(int)),
            'by_file': defaultdict(int),
        }
        
        for elem_id, elems in elements.items():
            if elems:
                elem = elems[0]
                stats['by_stage'][elem.stage][elem.element_type] += 1
                stats['by_file'][elem.file_path] += 1
                
                if elem.element_type == 'Def':
                    stats['total_definitions'] += 1
                elif elem.element_type == 'Thm':
                    stats['total_theorems'] += 1
                elif elem.element_type == 'Lemma':
                    stats['total_lemmas'] += 1
                elif elem.element_type == 'Prop':
                    stats['total_propositions'] += 1
                elif elem.element_type == 'Cor':
                    stats['total_corollaries'] += 1
                    
        # 转换defaultdict为普通dict
        stats['by_stage'] = dict(stats['by_stage'])
        stats['by_file'] = dict(stats['by_file'])
        
        return stats
        
    def _generate_suggestions(self, result: TrackingResult) -> Dict[str, List[str]]:
        """生成建议"""
        suggestions = defaultdict(list)
        
        # 为每个阶段/类型建议新编号
        stage_doc_counters: Dict[Tuple[str, str], Set[int]] = defaultdict(set)
        
        for elem_id, elems in result.elements.items():
            if elems:
                elem = elems[0]
                key = (elem.stage, elem.doc_num)
                stage_doc_counters[key].add(int(elem.seq_num))
                
        # 为每个文件建议下一个可用编号
        file_elements: Dict[str, List[FormalElement]] = defaultdict(list)
        for elem_id, elems in result.elements.items():
            for elem in elems:
                file_elements[elem.file_path].append(elem)
                
        for file_path, elems in file_elements.items():
            # 按类型分组
            type_groups: Dict[str, List[int]] = defaultdict(list)
            for elem in elems:
                type_groups[elem.element_type].append(int(elem.seq_num))
                
            for elem_type, seq_nums in type_groups.items():
                if seq_nums:
                    next_num = max(seq_nums) + 1
                    elem = elems[0]
                    suggested_id = f"{elem_type}-{elem.stage}-{elem.doc_num}-{next_num:02d}"
                    suggestions[file_path].append(
                        f"下一个可用的 {elem_type} 编号: `{suggested_id}`"
                    )
                    
        # 为冲突提供建议
        for conflict in result.conflicts:
            if conflict.conflict_type == "duplicate":
                for elem in conflict.elements[1:]:
                    suggestions[elem.file_path].append(
                        f"请修改重复的编号 '{conflict.element_id}'"
                    )
                    
        return dict(suggestions)
        
    def suggest_new_id(
        self,
        element_type: str,
        stage: str,
        doc_num: str,
        result: TrackingResult
    ) -> str:
        """
        建议新的形式化元素ID
        
        Args:
            element_type: 元素类型 (Def/Thm/Lemma/Prop/Cor)
            stage: 阶段 (S/K/F)
            doc_num: 文档序号
            result: 追踪结果
            
        Returns:
            建议的完整ID
        """
        # 找出该文档中该类型的最大序号
        max_seq = 0
        for elem_id, elems in result.elements.items():
            for elem in elems:
                if (elem.element_type == element_type and 
                    elem.stage == stage and 
                    elem.doc_num == doc_num):
                    max_seq = max(max_seq, int(elem.seq_num))
                    
        next_seq = max_seq + 1
        return f"{element_type}-{stage}-{doc_num}-{next_seq:02d}"
        
    def generate_json_database(
        self,
        result: TrackingResult,
        output_path: Path
    ) -> None:
        """生成JSON格式数据库"""
        db_data = {
            'generated_at': datetime.now().isoformat(),
            'statistics': result.statistics,
            'elements': {},
            'conflicts': [
                {
                    'element_id': c.element_id,
                    'type': c.conflict_type,
                    'message': c.message,
                    'locations': [
                        {
                            'file': e.file_path,
                            'line': e.line_number,
                            'context': e.context
                        }
                        for e in c.elements
                    ]
                }
                for c in result.conflicts
            ],
            'suggestions': result.suggestions
        }
        
        # 合并重复元素
        for elem_id, elems in result.elements.items():
            if elems:
                primary = elems[0]
                db_data['elements'][elem_id] = {
                    'type': primary.element_type,
                    'stage': primary.stage,
                    'doc_num': primary.doc_num,
                    'seq_num': primary.seq_num,
                    'title': primary.title,
                    'description': primary.description,
                    'dependencies': primary.dependencies,
                    'locations': [
                        {
                            'file': e.file_path,
                            'line': e.line_number,
                            'context': e.context
                        }
                        for e in elems
                    ]
                }
                
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(db_data, f, ensure_ascii=False, indent=2)
            
        logger.info(f"JSON数据库已生成: {output_path}")
        
    def update_registry(
        self,
        result: TrackingResult,
        registry_path: Path,
        backup: bool = True
    ) -> None:
        """
        更新定理注册表
        
        Args:
            result: 追踪结果
            registry_path: 注册表文件路径
            backup: 是否备份原文件
        """
        if not registry_path.exists():
            logger.warning(f"注册表文件不存在: {registry_path}")
            return
            
        # 备份
        if backup:
            backup_path = registry_path.with_suffix('.md.bak')
            backup_path.write_text(registry_path.read_text(encoding='utf-8'), encoding='utf-8')
            logger.info(f"已备份原注册表: {backup_path}")
            
        # 读取现有内容
        content = registry_path.read_text(encoding='utf-8')
        
        # 构建更新部分
        update_sections = []
        
        for stage in ['S', 'K', 'F']:
            stage_name = {'S': 'Struct', 'K': 'Knowledge', 'F': 'Flink'}.get(stage, stage)
            stage_elems = [
                (eid, elems) for eid, elems in result.elements.items()
                if elems and elems[0].stage == stage
            ]
            
            if stage_elems:
                update_sections.append(f"\n### {stage_name} Stage 更新 ({datetime.now().strftime('%Y-%m-%d')})\n")
                
                for elem_id, elems in sorted(stage_elems):
                    elem = elems[0]
                    update_sections.append(
                        f"- `{elem.full_id}`: {elem.title or '未命名'} "
                        f"([{elem.file_path}]({elem.file_path}))"
                    )
                    
        # 查找插入位置（通常在文件末尾或特定标记处）
        insert_marker = "<!-- AUTO-UPDATE-SECTION -->"
        
        if insert_marker in content:
            # 在标记后插入
            parts = content.split(insert_marker, 1)
            new_content = parts[0] + insert_marker + '\n' + '\n'.join(update_sections) + '\n' + parts[1]
        else:
            # 在文件末尾添加
            new_content = content + '\n\n## 自动更新记录\n\n' + '\n'.join(update_sections)
            
        registry_path.write_text(new_content, encoding='utf-8')
        logger.info(f"注册表已更新: {registry_path}")
        
    def generate_markdown_report(
        self,
        result: TrackingResult,
        output_path: Path
    ) -> None:
        """生成Markdown报告"""
        lines = [
            "# 形式化元素追踪报告",
            "",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 统计摘要",
            "",
            f"- **唯一元素总数**: {result.statistics.get('total_unique_elements', 0)}",
            f"- **定义 (Def)**: {result.statistics.get('total_definitions', 0)}",
            f"- **定理 (Thm)**: {result.statistics.get('total_theorems', 0)}",
            f"- **引理 (Lemma)**: {result.statistics.get('total_lemmas', 0)}",
            f"- **命题 (Prop)**: {result.statistics.get('total_propositions', 0)}",
            f"- **推论 (Cor)**: {result.statistics.get('total_corollaries', 0)}",
            "",
        ]
        
        # 按阶段统计
        by_stage = result.statistics.get('by_stage', {})
        if by_stage:
            lines.extend(["## 按阶段统计", ""])
            for stage, types in sorted(by_stage.items()):
                stage_name = {'S': 'Struct', 'K': 'Knowledge', 'F': 'Flink'}.get(stage, stage)
                lines.append(f"### {stage_name} ({stage})")
                for elem_type, count in sorted(types.items()):
                    lines.append(f"- {elem_type}: {count}")
                lines.append("")
                
        # 冲突列表
        if result.conflicts:
            lines.extend(["## 冲突与问题", ""])
            
            duplicates = [c for c in result.conflicts if c.conflict_type == "duplicate"]
            gaps = [c for c in result.conflicts if c.conflict_type == "gap"]
            
            if duplicates:
                lines.extend(["### 重复定义", ""])
                for conflict in duplicates:
                    lines.append(f"**{conflict.element_id}**")
                    for elem in conflict.elements:
                        lines.append(f"- {elem.file_path}:{elem.line_number}")
                    lines.append("")
                    
            if gaps:
                lines.extend(["### 编号缺失", ""])
                for conflict in gaps:
                    lines.append(f"- {conflict.message}")
                lines.append("")
        else:
            lines.extend(["## 冲突检查", "", "✅ 未发现编号冲突或重复\n"])
            
        # 建议
        if result.suggestions:
            lines.extend(["## 编号建议", ""])
            for file_path, suggestions in list(result.suggestions.items())[:20]:
                lines.append(f"### {file_path}")
                for suggestion in suggestions:
                    lines.append(f"- {suggestion}")
                lines.append("")
                
        # 元素索引（前100个）
        lines.extend(["## 元素索引", ""])
        sorted_elements = sorted(result.elements.items())[:100]
        for elem_id, elems in sorted_elements:
            elem = elems[0]
            lines.append(
                f"- `{elem.full_id}`: {elem.title or '未命名'} "
                f"([{elem.file_path}:{elem.line_number}]({elem.file_path}))"
            )
            
        lines.extend([
            "",
            "---",
            "*由 formal-element-tracker.py 自动生成*",
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
            
        logger.info(f"Markdown报告已生成: {output_path}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='形式化元素自动编号工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                           # 扫描当前目录
  %(prog)s -d ./Struct               # 扫描指定目录
  %(prog)s --update-registry         # 更新定理注册表
  %(prog)s --suggest Def S 01        # 建议新编号
        """
    )
    
    parser.add_argument(
        '-d', '--directory',
        type=str,
        default='.',
        help='目标目录 (默认: 当前目录)'
    )
    
    parser.add_argument(
        '-p', '--pattern',
        type=str,
        default='**/*.md',
        help='文件匹配模式 (默认: **/*.md)'
    )
    
    parser.add_argument(
        '--stages',
        nargs='+',
        choices=['S', 'K', 'F'],
        help='只扫描指定阶段'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='./formal-element-reports',
        help='输出目录 (默认: ./formal-element-reports)'
    )
    
    parser.add_argument(
        '--update-registry',
        action='store_true',
        help='更新 THEOREM-REGISTRY.md'
    )
    
    parser.add_argument(
        '--registry-path',
        type=str,
        default='THEOREM-REGISTRY.md',
        help='定理注册表路径 (默认: THEOREM-REGISTRY.md)'
    )
    
    parser.add_argument(
        '--suggest',
        nargs=3,
        metavar=('TYPE', 'STAGE', 'DOC_NUM'),
        help='建议新编号 (示例: Def S 01)'
    )
    
    args = parser.parse_args()
    
    # 创建追踪器
    root_dir = Path(args.directory).resolve()
    tracker = FormalElementTracker(
        root_dir=root_dir,
        registry_file=root_dir / args.registry_path
    )
    
    # 执行扫描
    result = tracker.scan_directory(args.pattern, args.stages)
    
    # 建议模式
    if args.suggest:
        element_type, stage, doc_num = args.suggest
        suggested_id = tracker.suggest_new_id(element_type, stage, doc_num, result)
        print(f"\n建议的新编号: `{suggested_id}`\n")
        return 0
        
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成报告
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    json_path = output_dir / f"formal-elements-{timestamp}.json"
    tracker.generate_json_database(result, json_path)
    
    md_path = output_dir / f"formal-elements-{timestamp}.md"
    tracker.generate_markdown_report(result, md_path)
    
    # 更新注册表
    if args.update_registry:
        registry_path = root_dir / args.registry_path
        if registry_path.exists():
            tracker.update_registry(result, registry_path)
        else:
            logger.warning(f"注册表文件不存在: {registry_path}")
            
    # 输出摘要
    print(f"\n{'='*60}")
    print("形式化元素追踪完成")
    print(f"{'='*60}")
    print(f"唯一元素数: {result.statistics.get('total_unique_elements', 0)}")
    print(f"定义 (Def): {result.statistics.get('total_definitions', 0)}")
    print(f"定理 (Thm): {result.statistics.get('total_theorems', 0)}")
    print(f"引理 (Lemma): {result.statistics.get('total_lemmas', 0)}")
    print(f"命题 (Prop): {result.statistics.get('total_propositions', 0)}")
    print(f"推论 (Cor): {result.statistics.get('total_corollaries', 0)}")
    print(f"冲突数: {len(result.conflicts)}")
    print(f"{'='*60}")
    print(f"报告已保存至: {output_dir}")
    
    return 0 if not result.conflicts else 1


if __name__ == '__main__':
    exit(main())
