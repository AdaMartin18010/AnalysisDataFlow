#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mermaid图表语法检查器 (Mermaid Syntax Checker)

功能：
- 提取所有Mermaid代码块
- 验证语法正确性
- 检查节点ID有效性
- 验证链接一致性
- 生成图表预览（可选）
- 支持flowchart, graph, sequenceDiagram, classDiagram等

作者: Automation Agent
版本: 1.0.0
"""

import re
import json
import argparse
import logging
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, Any
from enum import Enum
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DiagramType(Enum):
    """图表类型"""
    FLOWCHART = "flowchart"
    GRAPH = "graph"
    SEQUENCE = "sequenceDiagram"
    CLASS = "classDiagram"
    STATE = "stateDiagram"
    STATE_V2 = "stateDiagram-v2"
    ER = "erDiagram"
    GANTT = "gantt"
    PIE = "pie"
    JOURNEY = "journey"
    GIT = "gitGraph"
    MINDMAP = "mindmap"
    TIMELINE = "timeline"
    QUADRANT = "quadrantChart"
    UNKNOWN = "unknown"


class SyntaxErrorType(Enum):
    """语法错误类型"""
    INVALID_SYNTAX = "invalid_syntax"
    UNDEFINED_NODE = "undefined_node"
    DUPLICATE_NODE = "duplicate_node"
    INVALID_EDGE = "invalid_edge"
    INVALID_DIRECTION = "invalid_direction"
    INVALID_STATEMENT = "invalid_statement"
    MISSING_TERMINATOR = "missing_terminator"
    EMPTY_DIAGRAM = "empty_diagram"
    UNKNOWN_KEYWORD = "unknown_keyword"


@dataclass
class SyntaxError:
    """语法错误"""
    error_type: SyntaxErrorType
    line_number: int
    message: str
    suggestion: str = ""
    line_content: str = ""


@dataclass
class NodeInfo:
    """节点信息"""
    node_id: str
    node_type: str  # 节点类型：default, rounded, stadium, etc.
    label: str
    line_number: int
    is_defined: bool = True


@dataclass
class EdgeInfo:
    """边信息"""
    source: str
    target: str
    edge_type: str
    label: str
    line_number: int


@dataclass
class DiagramInfo:
    """图表信息"""
    diagram_type: DiagramType
    title: str = ""
    direction: str = ""
    nodes: List[NodeInfo] = field(default_factory=list)
    edges: List[EdgeInfo] = field(default_factory=list)
    errors: List[SyntaxError] = field(default_factory=list)


@dataclass
class MermaidBlock:
    """Mermaid代码块"""
    source_file: str
    line_start: int
    line_end: int
    content: str
    diagram_info: Optional[DiagramInfo] = None


@dataclass
class ValidationResult:
    """验证结果"""
    total_files: int = 0
    total_blocks: int = 0
    valid_blocks: int = 0
    error_blocks: int = 0
    warning_blocks: int = 0
    blocks: List[MermaidBlock] = field(default_factory=list)
    errors_by_type: Dict[str, int] = field(default_factory=lambda: defaultdict(int))


from collections import defaultdict


class MermaidSyntaxChecker:
    """Mermaid语法检查器"""
    
    # Mermaid代码块正则
    MERMAID_BLOCK_PATTERN = re.compile(
        r'```mermaid\s*\n(.*?)```',
        re.DOTALL | re.IGNORECASE
    )
    
    # 图表类型识别
    DIAGRAM_TYPE_PATTERNS = {
        DiagramType.FLOWCHART: re.compile(r'^\s*flowchart\s+', re.IGNORECASE),
        DiagramType.GRAPH: re.compile(r'^\s*graph\s+', re.IGNORECASE),
        DiagramType.SEQUENCE: re.compile(r'^\s*sequenceDiagram\s*', re.IGNORECASE),
        DiagramType.CLASS: re.compile(r'^\s*classDiagram\s*', re.IGNORECASE),
        DiagramType.STATE: re.compile(r'^\s*stateDiagram\s*(?!-v2)', re.IGNORECASE),
        DiagramType.STATE_V2: re.compile(r'^\s*stateDiagram-v2\s*', re.IGNORECASE),
        DiagramType.ER: re.compile(r'^\s*erDiagram\s*', re.IGNORECASE),
        DiagramType.GANTT: re.compile(r'^\s*gantt\s*', re.IGNORECASE),
        DiagramType.PIE: re.compile(r'^\s*pie\s*', re.IGNORECASE),
        DiagramType.JOURNEY: re.compile(r'^\s*journey\s*', re.IGNORECASE),
        DiagramType.GIT: re.compile(r'^\s*gitGraph\s*', re.IGNORECASE),
        DiagramType.MINDMAP: re.compile(r'^\s*mindmap\s*', re.IGNORECASE),
        DiagramType.TIMELINE: re.compile(r'^\s*timeline\s*', re.IGNORECASE),
        DiagramType.QUADRANT: re.compile(r'^\s*quadrantChart\s*', re.IGNORECASE),
    }
    
    # Flowchart/Graph 语法正则
    NODE_DEF_PATTERN = re.compile(
        r'([\w\s]+?)\s*\[\s*(.+?)\s*\]|'  # 矩形节点 [text]
        r'([\w\s]+?)\s*\(\s*(.+?)\s*\)|'  # 圆角节点 (text)
        r'([\w\s]+?)\s*\(\(\s*(.+?)\s*\)\)|'  # 圆形节点 ((text))
        r'([\w\s]+?)\s*\>\s*(.+?)\s*\]|'  # 不对称节点 >text]
        r'([\w\s]+?)\s*\{\s*(.+?)\s*\}|'  # 菱形节点 {text}
        r'([\w\s]+?)\s*\(\[\s*(.+?)\s*\]\)|'  # 体育场节点 ([text])
        r'([\w\s]+?)\s*\[\/\s*(.+?)\s*\/\]|'  # 子程序节点 [/text/]
        r'([\w\s]+?)\s*\[\\\s*(.+?)\s*\\\]',  # 平行四边形 [\text\]
        re.MULTILINE
    )
    
    # 简单节点定义（仅ID）
    SIMPLE_NODE_PATTERN = re.compile(r'^\s*([a-zA-Z][a-zA-Z0-9_]*)\s*$', re.MULTILINE)
    
    # 边定义
    EDGE_PATTERN = re.compile(
        r'([a-zA-Z][a-zA-Z0-9_]*)\s*'  # 源节点
        r'(--[\|>x]|==[\|>x]|[-.=]+|\-\.-|\-\-\-|\.[\|>x]|==[\|>x])\s*'  # 边类型
        r'(?:\|([^|]+)\|)?\s*'  # 可选标签
        r'([a-zA-Z][a-zA-Z0-9_]*)',  # 目标节点
        re.MULTILINE
    )
    
    # 方向定义
    DIRECTION_PATTERN = re.compile(r'^(?:flowchart|graph)\s+(TD|TB|BT|RL|LR)\s*$', re.MULTILINE)
    
    # 子图定义
    SUBGRAPH_PATTERN = re.compile(r'^\s*subgraph\s+(.+)$', re.MULTILINE | re.IGNORECASE)
    
    # 结束定义
    END_PATTERN = re.compile(r'^\s*end\s*$', re.MULTILINE | re.IGNORECASE)
    
    # 注释
    COMMENT_PATTERN = re.compile(r'%%.*$', re.MULTILINE)
    
    # 节点ID有效性
    VALID_NODE_ID_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]*$')
    
    # Sequence Diagram 参与者定义
    SEQ_PARTICIPANT_PATTERN = re.compile(
        r'^\s*(?:participant|actor)\s+(["\']?)([a-zA-Z][a-zA-Z0-9_\s]*)\1(?:\s+as\s+)?',
        re.MULTILINE | re.IGNORECASE
    )
    
    # Sequence Diagram 消息
    SEQ_MESSAGE_PATTERN = re.compile(
        r'^\s*([a-zA-Z][a-zA-Z0-9_]*)\s*(-?-{1,3}\>{0,2})\s*([a-zA-Z][a-zA-Z0-9_]*):',
        re.MULTILINE
    )
    
    # Class Diagram 类定义
    CLASS_DEF_PATTERN = re.compile(
        r'^\s*class\s+([a-zA-Z][a-zA-Z0-9_]*)',
        re.MULTILINE | re.IGNORECASE
    )
    
    def __init__(
        self,
        root_dir: Path,
        use_cli: bool = False,
        mmdc_path: Optional[str] = None,
        skip_patterns: Optional[List[str]] = None
    ):
        """
        初始化检查器
        
        Args:
            root_dir: 项目根目录
            use_cli: 是否使用Mermaid CLI进行验证
            mmdc_path: Mermaid CLI路径
            skip_patterns: 跳过的文件模式
        """
        self.root_dir = Path(root_dir).resolve()
        self.use_cli = use_cli
        self.mmdc_path = mmdc_path or "mmdc"
        self.skip_patterns = skip_patterns or [
            'node_modules', '.git', '__pycache__',
            '.venv', 'venv', 'archive'
        ]
        
    def _should_skip_file(self, file_path: Path) -> bool:
        """判断是否应该跳过文件"""
        path_str = str(file_path)
        return any(pattern in path_str for pattern in self.skip_patterns)
        
    def _detect_diagram_type(self, content: str) -> DiagramType:
        """检测图表类型"""
        for diagram_type, pattern in self.DIAGRAM_TYPE_PATTERNS.items():
            if pattern.search(content):
                return diagram_type
        return DiagramType.UNKNOWN
        
    def _extract_direction(self, content: str) -> str:
        """提取方向定义"""
        match = self.DIRECTION_PATTERN.search(content)
        if match:
            return match.group(1)
        return ""
        
    def _parse_flowchart(self, content: str) -> DiagramInfo:
        """解析Flowchart/Graph"""
        info = DiagramInfo(diagram_type=DiagramType.FLOWCHART)
        info.direction = self._extract_direction(content)
        
        # 移除注释
        clean_content = self.COMMENT_PATTERN.sub('', content)
        lines = clean_content.split('\n')
        
        defined_nodes: Set[str] = set()
        referenced_nodes: Set[str] = set()
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('%%'):
                continue
                
            # 跳过方向声明
            if self.DIRECTION_PATTERN.match(line):
                continue
                
            # 跳过子图声明
            if self.SUBGRAPH_PATTERN.match(line):
                continue
                
            # 跳过end
            if self.END_PATTERN.match(line):
                continue
                
            # 解析节点定义
            node_match = self._parse_node_def(line, line_num)
            if node_match:
                info.nodes.append(node_match)
                defined_nodes.add(node_match.node_id)
                continue
                
            # 解析边
            edge_match = self._parse_edge(line, line_num)
            if edge_match:
                info.edges.append(edge_match)
                referenced_nodes.add(edge_match.source)
                referenced_nodes.add(edge_match.target)
                
        # 检查未定义的节点
        for edge in info.edges:
            if edge.source not in defined_nodes:
                info.errors.append(SyntaxError(
                    error_type=SyntaxErrorType.UNDEFINED_NODE,
                    line_number=edge.line_number,
                    message=f"未定义的节点: '{edge.source}'",
                    suggestion=f"在使用前定义节点: {edge.source}[标签]"
                ))
            if edge.target not in defined_nodes:
                info.errors.append(SyntaxError(
                    error_type=SyntaxErrorType.UNDEFINED_NODE,
                    line_number=edge.line_number,
                    message=f"未定义的节点: '{edge.target}'",
                    suggestion=f"在使用前定义节点: {edge.target}[标签]"
                ))
                
        return info
        
    def _parse_node_def(self, line: str, line_num: int) -> Optional[NodeInfo]:
        """解析节点定义"""
        # 匹配各种节点形状
        patterns = [
            (r'^\s*([a-zA-Z][a-zA-Z0-9_]*)\s*\[\s*(.+?)\s*\]\s*$', 'rect'),  # [rect]
            (r'^\s*([a-zA-Z][a-zA-Z0-9_]*)\s*\(\s*(.+?)\s*\)\s*$', 'rounded'),  # (rounded)
            (r'^\s*([a-zA-Z][a-zA-Z0-9_]*)\s*\(\(\s*(.+?)\s*\)\)\s*$', 'circle'),  # ((circle))
            (r'^\s*([a-zA-Z][a-zA-Z0-9_]*)\s*\{\s*(.+?)\s*\}\s*$', 'diamond'),  # {diamond}
            (r'^\s*([a-zA-Z][a-zA-Z0-9_]*)\s*\(\[\s*(.+?)\s*\]\)\s*$', 'stadium'),  # ([stadium])
        ]
        
        for pattern, node_type in patterns:
            match = re.match(pattern, line, re.DOTALL)
            if match:
                node_id = match.group(1).strip()
                label = match.group(2).strip()
                return NodeInfo(
                    node_id=node_id,
                    node_type=node_type,
                    label=label,
                    line_number=line_num
                )
                
        # 简单节点定义（仅ID，无标签）
        simple_match = self.SIMPLE_NODE_PATTERN.match(line)
        if simple_match and not self.EDGE_PATTERN.search(line):
            node_id = simple_match.group(1)
            return NodeInfo(
                node_id=node_id,
                node_type='default',
                label=node_id,
                line_number=line_num
            )
            
        return None
        
    def _parse_edge(self, line: str, line_num: int) -> Optional[EdgeInfo]:
        """解析边定义"""
        match = self.EDGE_PATTERN.search(line)
        if match:
            return EdgeInfo(
                source=match.group(1),
                target=match.group(4),
                edge_type=match.group(2),
                label=match.group(3) or "",
                line_number=line_num
            )
        return None
        
    def _parse_sequence_diagram(self, content: str) -> DiagramInfo:
        """解析序列图"""
        info = DiagramInfo(diagram_type=DiagramType.SEQUENCE)
        
        # 移除注释
        clean_content = self.COMMENT_PATTERN.sub('', content)
        lines = clean_content.split('\n')
        
        participants: Set[str] = set()
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            # 解析参与者定义
            for match in self.SEQ_PARTICIPANT_PATTERN.finditer(line):
                participant = match.group(2).strip()
                participants.add(participant)
                info.nodes.append(NodeInfo(
                    node_id=participant,
                    node_type='actor',
                    label=participant,
                    line_number=line_num
                ))
                
            # 解析消息
            for match in self.SEQ_MESSAGE_PATTERN.finditer(line):
                source = match.group(1)
                target = match.group(3)
                
                # 检查参与者是否存在
                if source not in participants:
                    # 隐式参与者
                    participants.add(source)
                    info.nodes.append(NodeInfo(
                        node_id=source,
                        node_type='actor',
                        label=source,
                        line_number=line_num
                    ))
                    
                if target not in participants:
                    participants.add(target)
                    info.nodes.append(NodeInfo(
                        node_id=target,
                        node_type='actor',
                        label=target,
                        line_number=line_num
                    ))
                    
                info.edges.append(EdgeInfo(
                    source=source,
                    target=target,
                    edge_type=match.group(2),
                    label="",
                    line_number=line_num
                ))
                
        return info
        
    def _parse_class_diagram(self, content: str) -> DiagramInfo:
        """解析类图"""
        info = DiagramInfo(diagram_type=DiagramType.CLASS)
        
        clean_content = self.COMMENT_PATTERN.sub('', content)
        
        for match in self.CLASS_DEF_PATTERN.finditer(clean_content):
            class_name = match.group(1)
            line_num = clean_content[:match.start()].count('\n') + 1
            
            info.nodes.append(NodeInfo(
                node_id=class_name,
                node_type='class',
                label=class_name,
                line_number=line_num
            ))
            
        return info
        
    def _parse_diagram(self, content: str) -> DiagramInfo:
        """解析图表内容"""
        diagram_type = self._detect_diagram_type(content)
        
        if diagram_type in [DiagramType.FLOWCHART, DiagramType.GRAPH]:
            return self._parse_flowchart(content)
        elif diagram_type == DiagramType.SEQUENCE:
            return self._parse_sequence_diagram(content)
        elif diagram_type == DiagramType.CLASS:
            return self._parse_class_diagram(content)
        elif diagram_type == DiagramType.UNKNOWN:
            return DiagramInfo(
                diagram_type=DiagramType.UNKNOWN,
                errors=[SyntaxError(
                    error_type=SyntaxErrorType.UNKNOWN_KEYWORD,
                    line_number=1,
                    message="无法识别的图表类型",
                    suggestion="使用有效的图表类型: flowchart, graph, sequenceDiagram, classDiagram等"
                )]
            )
        else:
            # 其他类型暂时只检测类型，不深入解析
            return DiagramInfo(diagram_type=diagram_type)
            
    def _check_with_cli(self, content: str) -> List[SyntaxError]:
        """使用Mermaid CLI检查语法"""
        errors = []
        
        if not self.use_cli:
            return errors
            
        try:
            # 创建临时文件
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(
                mode='w', suffix='.mmd', delete=False
            ) as f:
                f.write(content)
                temp_path = f.name
                
            try:
                # 运行mmdc检查
                result = subprocess.run(
                    [self.mmdc_path, '-i', temp_path, '-o', '/dev/null'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode != 0:
                    # 解析错误输出
                    for line in result.stderr.split('\n'):
                        if 'error' in line.lower():
                            errors.append(SyntaxError(
                                error_type=SyntaxErrorType.INVALID_SYNTAX,
                                line_number=0,
                                message=line.strip(),
                                suggestion="检查Mermaid语法"
                            ))
            finally:
                os.unlink(temp_path)
                
        except Exception as e:
            logger.warning(f"CLI检查失败: {e}")
            
        return errors
        
    def check_block(self, content: str, file_path: str = "", line_offset: int = 0) -> MermaidBlock:
        """
        检查单个Mermaid代码块
        
        Args:
            content: Mermaid代码内容
            file_path: 源文件路径
            line_offset: 行号偏移
            
        Returns:
            Mermaid块信息
        """
        block = MermaidBlock(
            source_file=file_path,
            line_start=line_offset,
            line_end=line_offset + content.count('\n'),
            content=content
        )
        
        # 解析图表
        info = self._parse_diagram(content)
        
        # CLI检查
        if self.use_cli:
            cli_errors = self._check_with_cli(content)
            info.errors.extend(cli_errors)
            
        # 空图表检查
        if not info.nodes and not info.edges and not info.errors:
            info.errors.append(SyntaxError(
                error_type=SyntaxErrorType.EMPTY_DIAGRAM,
                line_number=1,
                message="图表内容为空",
                suggestion="添加节点和边定义"
            ))
            
        block.diagram_info = info
        return block
        
    def scan_file(self, file_path: Path) -> List[MermaidBlock]:
        """
        扫描文件中的所有Mermaid代码块
        
        Args:
            file_path: Markdown文件路径
            
        Returns:
            Mermaid块列表
        """
        blocks = []
        rel_path = str(file_path.relative_to(self.root_dir))
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.warning(f"无法读取文件 {file_path}: {e}")
            return blocks
            
        # 查找所有Mermaid代码块
        for match in self.MERMAID_BLOCK_PATTERN.finditer(content):
            mermaid_content = match.group(1).strip()
            line_num = content[:match.start()].count('\n') + 1
            
            block = self.check_block(mermaid_content, rel_path, line_num)
            blocks.append(block)
            
        return blocks
        
    def scan_directory(self, pattern: str = "**/*.md") -> ValidationResult:
        """
        扫描目录中的所有文件
        
        Args:
            pattern: 文件匹配模式
            
        Returns:
            验证结果
        """
        result = ValidationResult()
        
        md_files = list(self.root_dir.glob(pattern))
        result.total_files = len(md_files)
        
        logger.info(f"发现 {len(md_files)} 个Markdown文件")
        
        for file_path in md_files:
            if self._should_skip_file(file_path):
                continue
                
            blocks = self.scan_file(file_path)
            result.blocks.extend(blocks)
            
        result.total_blocks = len(result.blocks)
        
        # 统计
        for block in result.blocks:
            if block.diagram_info and block.diagram_info.errors:
                result.error_blocks += 1
                for error in block.diagram_info.errors:
                    result.errors_by_type[error.error_type.value] += 1
            else:
                result.valid_blocks += 1
                
        return result
        
    def generate_json_report(self, result: ValidationResult, output_path: Path) -> None:
        """生成JSON报告"""
        report_data = {
            'scan_time': datetime.now().isoformat(),
            'summary': {
                'total_files': result.total_files,
                'total_blocks': result.total_blocks,
                'valid_blocks': result.valid_blocks,
                'error_blocks': result.error_blocks,
                'validity_rate': round(
                    result.valid_blocks / result.total_blocks * 100, 2
                ) if result.total_blocks > 0 else 0,
                'errors_by_type': dict(result.errors_by_type)
            },
            'blocks': [
                {
                    'source_file': b.source_file,
                    'line_start': b.line_start,
                    'line_end': b.line_end,
                    'diagram_type': b.diagram_info.diagram_type.value if b.diagram_info else None,
                    'node_count': len(b.diagram_info.nodes) if b.diagram_info else 0,
                    'edge_count': len(b.diagram_info.edges) if b.diagram_info else 0,
                    'errors': [
                        {
                            'type': e.error_type.value,
                            'line': e.line_number,
                            'message': e.message,
                            'suggestion': e.suggestion
                        }
                        for e in (b.diagram_info.errors if b.diagram_info else [])
                    ]
                }
                for b in result.blocks
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
            
        logger.info(f"JSON报告已生成: {output_path}")
        
    def generate_markdown_report(self, result: ValidationResult, output_path: Path) -> None:
        """生成Markdown报告"""
        lines = [
            "# Mermaid语法检查报告",
            "",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 统计摘要",
            "",
            f"| 指标 | 数值 |",
            f"|------|------|",
            f"| 扫描文件数 | {result.total_files} |",
            f"| Mermaid块数 | {result.total_blocks} |",
            f"| 有效块 | {result.valid_blocks} |",
            f"| 错误块 | {result.error_blocks} |",
            f"| **有效率** | {round(result.valid_blocks / result.total_blocks * 100, 2) if result.total_blocks > 0 else 0}% |",
            "",
        ]
        
        # 错误类型统计
        if result.errors_by_type:
            lines.extend(["### 错误类型分布", ""])
            for error_type, count in sorted(result.errors_by_type.items(), key=lambda x: -x[1]):
                lines.append(f"- **{error_type}**: {count}")
            lines.append("")
            
        # 问题详情
        error_blocks = [b for b in result.blocks if b.diagram_info and b.diagram_info.errors]
        
        if error_blocks:
            lines.extend(["## 问题详情", ""])
            
            for block in error_blocks[:30]:  # 最多显示30个问题块
                lines.extend([
                    f"### {block.source_file}:{block.line_start}",
                    f"",
                    f"**图表类型**: {block.diagram_info.diagram_type.value if block.diagram_info else 'unknown'}",
                    f"",
                ])
                
                for error in block.diagram_info.errors:
                    lines.append(f"- ❌ **{error.error_type.value}** (行 {error.line_number}): {error.message}")
                    if error.suggestion:
                        lines.append(f"  - 💡 {error.suggestion}")
                lines.append("")
                
            if len(error_blocks) > 30:
                lines.append(f"*... 还有 {len(error_blocks) - 30} 个错误块*\n")
        else:
            lines.extend(["## 检查结果", "", "✅ 所有Mermaid图表语法正确！\n"])
            
        lines.extend([
            "",
            "---",
            "*由 mermaid-syntax-checker.py 自动生成*",
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
            
        logger.info(f"Markdown报告已生成: {output_path}")
        
    def generate_preview_html(
        self,
        result: ValidationResult,
        output_path: Path
    ) -> None:
        """生成HTML预览文件"""
        lines = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <title>Mermaid图表预览</title>',
            '    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>',
            '    <style>',
            '        body { font-family: Arial, sans-serif; margin: 20px; }',
            '        .block { border: 1px solid #ddd; margin: 20px 0; padding: 15px; border-radius: 5px; }',
            '        .block.error { border-color: #f44336; background: #ffebee; }',
            '        .block.valid { border-color: #4caf50; background: #e8f5e9; }',
            '        .mermaid { background: white; padding: 10px; }',
            '        .error-list { color: #f44336; }',
            '        h2 { margin-top: 0; }',
            '    </style>',
            '</head>',
            '<body>',
            f'    <h1>Mermaid图表预览 ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})</h1>',
        ]
        
        for block in result.blocks[:50]:  # 最多显示50个
            has_errors = block.diagram_info and block.diagram_info.errors
            css_class = 'error' if has_errors else 'valid'
            
            lines.extend([
                f'    <div class="block {css_class}">',
                f'        <h3>{block.source_file}:{block.line_start}</h3>',
            ])
            
            if has_errors:
                lines.append('        <div class="error-list"><ul>')
                for error in block.diagram_info.errors:
                    lines.append(f'            <li>{error.message}</li>')
                lines.append('        </ul></div>')
                
            lines.extend([
                '        <div class="mermaid">',
            ])
            
            # 转义HTML
            escaped_content = block.content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            lines.append(f'            {escaped_content}')
            
            lines.extend([
                '        </div>',
                '    </div>',
            ])
            
        lines.extend([
            '    <script>',
            '        mermaid.initialize({ startOnLoad: true });',
            '    </script>',
            '</body>',
            '</html>',
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
            
        logger.info(f"HTML预览已生成: {output_path}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='Mermaid图表语法检查器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                           # 检查当前目录
  %(prog)s -d ./docs                 # 检查指定目录
  %(prog)s --use-cli                 # 使用Mermaid CLI验证
  %(prog)s --preview                 # 生成HTML预览
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
        '--use-cli',
        action='store_true',
        help='使用Mermaid CLI进行验证'
    )
    
    parser.add_argument(
        '--mmdc-path',
        type=str,
        default='mmdc',
        help='Mermaid CLI路径 (默认: mmdc)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='./mermaid-check-reports',
        help='输出目录 (默认: ./mermaid-check-reports)'
    )
    
    parser.add_argument(
        '--preview',
        action='store_true',
        help='生成HTML预览文件'
    )
    
    args = parser.parse_args()
    
    # 创建检查器
    checker = MermaidSyntaxChecker(
        root_dir=Path(args.directory).resolve(),
        use_cli=args.use_cli,
        mmdc_path=args.mmdc_path
    )
    
    # 执行检查
    result = checker.scan_directory(args.pattern)
    
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成报告
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    json_path = output_dir / f"mermaid-check-{timestamp}.json"
    checker.generate_json_report(result, json_path)
    
    md_path = output_dir / f"mermaid-check-{timestamp}.md"
    checker.generate_markdown_report(result, md_path)
    
    # 生成预览
    if args.preview:
        html_path = output_dir / f"mermaid-preview-{timestamp}.html"
        checker.generate_preview_html(result, html_path)
        
    # 输出摘要
    print(f"\n{'='*60}")
    print("Mermaid语法检查完成")
    print(f"{'='*60}")
    print(f"扫描文件数: {result.total_files}")
    print(f"Mermaid块数: {result.total_blocks}")
    print(f"✓ 有效: {result.valid_blocks}")
    print(f"✗ 错误: {result.error_blocks}")
    print(f"有效率: {round(result.valid_blocks / result.total_blocks * 100, 2) if result.total_blocks > 0 else 0}%")
    print(f"{'='*60}")
    print(f"报告已保存至: {output_dir}")
    
    return 0 if result.error_blocks == 0 else 1


if __name__ == '__main__':
    exit(main())
