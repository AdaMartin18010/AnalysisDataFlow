#!/usr/bin/env python3
"""
定理依赖关系分析器 (Theorem Dependency Analyzer)
===============================================
解析定理、引理、命题之间的依赖关系，检测循环依赖，识别关键路径。

作者: Knowledge Graph Team
版本: 1.0.0
"""

import os
import re
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Set, Tuple, Optional, Any, FrozenSet
from collections import defaultdict, deque

# 可选依赖
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    nx = None


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Theorem:
    """定理/引理/命题数据结构"""
    id: str
    formal_id: str  # 如 Thm-S-01-01
    name: str
    theorem_type: str  # theorem, lemma, proposition, corollary, definition
    source_file: str
    source_line: int
    statement: str
    proof: str = ""
    dependencies: Set[str] = field(default_factory=set)
    used_by: Set[str] = field(default_factory=set)
    proof_depth: int = -1  # 证明深度，-1表示未计算
    complexity_score: float = 0.0
    is_proven: bool = False
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'formal_id': self.formal_id,
            'name': self.name,
            'theorem_type': self.theorem_type,
            'source_file': self.source_file,
            'source_line': self.source_line,
            'statement': self.statement[:500],
            'dependencies': list(self.dependencies),
            'used_by': list(self.used_by),
            'proof_depth': self.proof_depth,
            'complexity_score': self.complexity_score,
            'is_proven': self.is_proven
        }


@dataclass
class DependencyEdge:
    """依赖边数据结构"""
    source: str
    target: str
    dependency_type: str  # direct, indirect, cyclic
    evidence: str = ""
    line_number: int = 0


class TheoremParser:
    """定理解析器"""
    
    # 正则表达式模式
    FORMAL_ID_PATTERN = re.compile(
        r'`(Thm|Lemma|Prop|Cor|Def)-([SKF])-(\d+)-(\d+)`[:：]?\s*([^\n]*)',
        re.IGNORECASE
    )
    
    PROOF_SECTION_PATTERN = re.compile(
        r'[#]+\s*5\.\s*(?:形式证明|Proof)[\s\S]*?(?=(?:[#]+\s*6\.|\Z))',
        re.IGNORECASE
    )
    
    # 依赖关键词模式
    DEPENDENCY_KEYWORDS = [
        (r'(?:根据|by|from|using)\s*[`:]?\s*(Thm|Lemma|Prop|Cor|Def)-([SKF])-(\d+)-(\d+)', 'direct'),
        (r'(?:应用|apply)\s*[`:]?\s*(Thm|Lemma|Prop|Cor|Def)-([SKF])-(\d+)-(\d+)', 'direct'),
        (r'(?:由|from)\s*[^，。]*?(?:可知|可得|推出)', 'contextual'),
        (r'(?:引理|lemma)\s+(\d+|[A-Z])', 'local_reference'),
    ]
    
    THEOREM_TYPE_MAP = {
        'Thm': 'theorem',
        'Lemma': 'lemma',
        'Prop': 'proposition',
        'Cor': 'corollary',
        'Def': 'definition'
    }
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.theorems: Dict[str, Theorem] = {}
        self.edges: List[DependencyEdge] = []
        self.file_contents: Dict[str, str] = {}
    
    def parse_file(self, file_path: Path) -> List[Theorem]:
        """解析单个文件中的定理"""
        theorems = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            self.file_contents[str(file_path)] = content
        except Exception as e:
            logger.error(f"无法读取文件 {file_path}: {e}")
            return theorems
        
        lines = content.split('\n')
        
        # 查找所有形式化ID
        for match in self.FORMAL_ID_PATTERN.finditer(content):
            formal_type = match.group(1)
            stage = match.group(2)
            doc_num = match.group(3)
            seq_num = match.group(4)
            name = match.group(5).strip()
            
            formal_id = f"{formal_type}-{stage}-{doc_num}-{seq_num}"
            theorem_type = self.THEOREM_TYPE_MAP.get(formal_type, 'unknown')
            
            line_num = content[:match.start()].count('\n') + 1
            
            # 提取声明和证明
            statement, proof = self._extract_statement_and_proof(content, match.end())
            
            theorem = Theorem(
                id=formal_id,
                formal_id=formal_id,
                name=name or formal_id,
                theorem_type=theorem_type,
                source_file=str(file_path.relative_to(self.base_path)),
                source_line=line_num,
                statement=statement,
                proof=proof
            )
            
            theorems.append(theorem)
            self.theorems[formal_id] = theorem
        
        return theorems
    
    def _extract_statement_and_proof(self, content: str, start_pos: int) -> Tuple[str, str]:
        """提取定理声明和证明"""
        remaining = content[start_pos:]
        
        # 找到下一个形式化元素或章节标题
        next_match = self.FORMAL_ID_PATTERN.search(remaining)
        next_section = re.search(r'\n[#]+\s*\d', remaining)
        
        end_pos = len(remaining)
        if next_match:
            end_pos = min(end_pos, next_match.start())
        if next_section:
            end_pos = min(end_pos, next_section.start())
        
        section = remaining[:end_pos]
        
        # 尝试分离声明和证明
        proof_match = self.PROOF_SECTION_PATTERN.search(content[start_pos:start_pos + end_pos + 1000])
        
        if proof_match:
            proof_start_rel = proof_match.start()
            statement = remaining[:proof_start_rel].strip()
            proof = proof_match.group(0).strip()
        else:
            statement = section.strip()
            proof = ""
        
        return statement[:1000], proof[:2000]
    
    def extract_dependencies(self):
        """提取所有定理的依赖关系"""
        for theorem_id, theorem in self.theorems.items():
            # 从证明文本中提取依赖
            if theorem.proof:
                self._extract_from_proof(theorem, theorem.proof)
            
            # 从声明文本中提取依赖
            self._extract_from_statement(theorem, theorem.statement)
        
        # 构建反向依赖（used_by）
        for theorem_id, theorem in self.theorems.items():
            for dep_id in theorem.dependencies:
                if dep_id in self.theorems:
                    self.theorems[dep_id].used_by.add(theorem_id)
        
        logger.info(f"提取了 {len(self.edges)} 个依赖关系")
    
    def _extract_from_proof(self, theorem: Theorem, proof_text: str):
        """从证明文本中提取依赖"""
        for pattern, dep_type in self.DEPENDENCY_KEYWORDS:
            for match in re.finditer(pattern, proof_text, re.IGNORECASE):
                if len(match.groups()) >= 4:
                    formal_type = match.group(1)
                    stage = match.group(2)
                    doc_num = match.group(3)
                    seq_num = match.group(4)
                    dep_id = f"{formal_type}-{stage}-{doc_num}-{seq_num}"
                else:
                    continue
                
                if dep_id != theorem.id and dep_id in self.theorems:
                    theorem.dependencies.add(dep_id)
                    self.edges.append(DependencyEdge(
                        source=theorem.id,
                        target=dep_id,
                        dependency_type=dep_type,
                        evidence=match.group(0)
                    ))
    
    def _extract_from_statement(self, theorem: Theorem, statement: str):
        """从声明文本中提取依赖"""
        # 查找声明中引用的其他定理
        for match in self.FORMAL_ID_PATTERN.finditer(statement):
            dep_id = f"{match.group(1)}-{match.group(2)}-{match.group(3)}-{match.group(4)}"
            if dep_id != theorem.id and dep_id in self.theorems:
                theorem.dependencies.add(dep_id)
                self.edges.append(DependencyEdge(
                    source=theorem.id,
                    target=dep_id,
                    dependency_type='statement_reference'
                ))
    
    def parse_directory(self, directory: str, pattern: str = "*.md") -> int:
        """解析目录中的所有文件"""
        dir_path = self.base_path / directory
        if not dir_path.exists():
            logger.warning(f"目录不存在: {dir_path}")
            return 0
        
        files = list(dir_path.rglob(pattern))
        logger.info(f"在 {directory} 中找到 {len(files)} 个文件")
        
        total = 0
        for file_path in files:
            theorems = self.parse_file(file_path)
            total += len(theorems)
        
        # 提取依赖关系
        self.extract_dependencies()
        
        logger.info(f"总共解析 {total} 个定理/引理/命题")
        return total


class DependencyAnalyzer:
    """依赖关系分析器"""
    
    def __init__(self, parser: TheoremParser):
        self.parser = parser
        self.graph = None
        if NETWORKX_AVAILABLE:
            self.graph = nx.DiGraph()
    
    def build_dependency_graph(self):
        """构建依赖图"""
        if not NETWORKX_AVAILABLE or self.graph is None:
            logger.warning("NetworkX不可用，跳过图构建")
            return
        
        # 添加节点
        for theorem_id, theorem in self.parser.theorems.items():
            self.graph.add_node(
                theorem_id,
                type=theorem.theorem_type,
                name=theorem.name,
                source_file=theorem.source_file,
                complexity=theorem.complexity_score
            )
        
        # 添加边
        for edge in self.parser.edges:
            if edge.source in self.parser.theorems and edge.target in self.parser.theorems:
                self.graph.add_edge(
                    edge.source,
                    edge.target,
                    type=edge.dependency_type
                )
        
        logger.info(f"依赖图构建完成: {self.graph.number_of_nodes()} 节点, {self.graph.number_of_edges()} 边")
    
    def detect_cycles(self) -> List[List[str]]:
        """检测循环依赖"""
        if not NETWORKX_AVAILABLE or self.graph is None:
            return []
        
        try:
            cycles = list(nx.simple_cycles(self.graph))
            if cycles:
                logger.warning(f"检测到 {len(cycles)} 个循环依赖!")
                for cycle in cycles[:5]:  # 只显示前5个
                    logger.warning(f"  循环: {' -> '.join(cycle)} -> {cycle[0]}")
            else:
                logger.info("未检测到循环依赖")
            return cycles
        except Exception as e:
            logger.error(f"循环检测失败: {e}")
            return []
    
    def compute_proof_depth(self):
        """计算每个定理的证明深度（最长依赖链长度）"""
        # 使用拓扑排序的思想计算深度
        in_degree = {t_id: 0 for t_id in self.parser.theorems}
        
        for theorem in self.parser.theorems.values():
            in_degree[theorem.id] = len(theorem.dependencies)
        
        # BFS计算深度
        queue = deque([t_id for t_id, degree in in_degree.items() if degree == 0])
        depth = {t_id: 0 for t_id in queue}
        
        for t_id in queue:
            self.parser.theorems[t_id].proof_depth = 0
        
        while queue:
            current = queue.popleft()
            current_depth = depth[current]
            
            # 更新后继节点
            theorem = self.parser.theorems.get(current)
            if theorem:
                for successor_id in theorem.used_by:
                    successor = self.parser.theorems.get(successor_id)
                    if successor:
                        new_depth = current_depth + 1
                        if successor.proof_depth < new_depth:
                            successor.proof_depth = new_depth
                            depth[successor_id] = new_depth
                        
                        in_degree[successor_id] -= 1
                        if in_degree[successor_id] == 0:
                            queue.append(successor_id)
        
        # 计算平均深度和最大深度
        depths = [t.proof_depth for t in self.parser.theorems.values() if t.proof_depth >= 0]
        if depths:
            logger.info(f"证明深度统计: 最大={max(depths)}, 平均={sum(depths)/len(depths):.2f}")
    
    def compute_complexity(self):
        """计算定理复杂度"""
        for theorem in self.parser.theorems.values():
            # 复杂度基于：依赖数量、证明长度、被引用次数
            dep_count = len(theorem.dependencies)
            proof_length = len(theorem.proof)
            usage_count = len(theorem.used_by)
            
            # 复杂度分数（可调整权重）
            complexity = (
                dep_count * 2.0 +
                (proof_length / 500) * 1.0 +
                usage_count * 1.5
            )
            
            theorem.complexity_score = round(complexity, 2)
    
    def find_critical_path(self, target_theorem: str) -> List[str]:
        """找到证明目标定理所需的关键路径"""
        if target_theorem not in self.parser.theorems:
            logger.error(f"定理不存在: {target_theorem}")
            return []
        
        # 使用BFS找到所有依赖
        visited = set()
        queue = deque([target_theorem])
        critical_set = set()
        
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            critical_set.add(current)
            
            theorem = self.parser.theorems.get(current)
            if theorem:
                for dep in theorem.dependencies:
                    if dep not in visited:
                        queue.append(dep)
        
        # 尝试找到最长路径作为关键路径
        critical_path = self._find_longest_path_in_subgraph(critical_set)
        
        return critical_path
    
    def _find_longest_path_in_subgraph(self, node_set: Set[str]) -> List[str]:
        """在子图中找到最长路径"""
        # 简化的最长路径算法
        longest_path = []
        
        # 从每个叶节点开始回溯
        leaves = [n for n in node_set if not any(e.source == n for e in self.parser.edges)]
        
        for leaf in leaves:
            path = self._backtrack_from_node(leaf, node_set)
            if len(path) > len(longest_path):
                longest_path = path
        
        return longest_path[::-1]  # 反转以获得从依赖到目标的顺序
    
    def _backtrack_from_node(self, node: str, valid_nodes: Set[str]) -> List[str]:
        """从节点回溯"""
        path = [node]
        current = node
        
        while True:
            # 找到指向当前节点的边
            predecessors = [
                e.source for e in self.parser.edges
                if e.target == current and e.source in valid_nodes
            ]
            
            if not predecessors:
                break
            
            # 选择证明深度最大的前驱
            best_pred = max(predecessors, key=lambda n: 
                self.parser.theorems.get(n, Theorem('', '', '', '', 0, '')).proof_depth
            )
            path.append(best_pred)
            current = best_pred
        
        return path
    
    def find_foundation_theorems(self) -> List[str]:
        """找到基础定理（不依赖其他定理的定理）"""
        foundations = [
            t_id for t_id, theorem in self.parser.theorems.items()
            if not theorem.dependencies
        ]
        return foundations
    
    def find_most_important(self, n: int = 20) -> List[Tuple[str, int]]:
        """找到最重要的定理（被引用次数最多）"""
        importance = [
            (t_id, len(theorem.used_by))
            for t_id, theorem in self.parser.theorems.items()
        ]
        return sorted(importance, key=lambda x: x[1], reverse=True)[:n]


class DependencyExporter:
    """依赖关系导出器"""
    
    def __init__(self, parser: TheoremParser, analyzer: DependencyAnalyzer):
        self.parser = parser
        self.analyzer = analyzer
    
    def export_json(self, output_path: str):
        """导出为JSON格式"""
        data = {
            'generated_at': datetime.now().isoformat(),
            'statistics': {
                'total_theorems': len(self.parser.theorems),
                'total_dependencies': len(self.parser.edges),
                'by_type': {}
            },
            'theorems': {},
            'edges': [],
            'cycles': [],
            'foundations': [],
            'critical_paths': {}
        }
        
        # 按类型统计
        for theorem in self.parser.theorems.values():
            t_type = theorem.theorem_type
            data['statistics']['by_type'][t_type] = \
                data['statistics']['by_type'].get(t_type, 0) + 1
        
        # 导出定理
        for theorem_id, theorem in self.parser.theorems.items():
            data['theorems'][theorem_id] = theorem.to_dict()
        
        # 导出边
        for edge in self.parser.edges:
            data['edges'].append({
                'source': edge.source,
                'target': edge.target,
                'type': edge.dependency_type,
                'evidence': edge.evidence[:100]
            })
        
        # 导出循环依赖
        cycles = self.analyzer.detect_cycles()
        data['cycles'] = [list(cycle) for cycle in cycles[:20]]
        
        # 导出头信息
        data['foundations'] = self.analyzer.find_foundation_theorems()
        
        # 导出关键路径（针对最重要的10个定理）
        important = self.analyzer.find_most_important(10)
        for theorem_id, _ in important:
            path = self.analyzer.find_critical_path(theorem_id)
            data['critical_paths'][theorem_id] = path
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"依赖关系JSON已导出到: {output_path}")
    
    def export_critical_path_txt(self, output_path: str):
        """导出关键路径文本报告"""
        lines = [
            "=" * 70,
            "定理依赖关系关键路径分析报告",
            f"生成时间: {datetime.now().isoformat()}",
            "=" * 70,
            ""
        ]
        
        # 1. 基础定理
        foundations = self.analyzer.find_foundation_theorems()
        lines.extend([
            f"【基础定理】共 {len(foundations)} 个（不依赖其他定理）",
            "-" * 70
        ])
        for t_id in foundations[:30]:
            theorem = self.parser.theorems.get(t_id)
            if theorem:
                lines.append(f"  • {t_id}: {theorem.name}")
        if len(foundations) > 30:
            lines.append(f"  ... 还有 {len(foundations) - 30} 个")
        lines.append("")
        
        # 2. 最重要的定理
        lines.extend([
            "【最重要定理】（被引用次数最多）",
            "-" * 70
        ])
        important = self.analyzer.find_most_important(20)
        for rank, (t_id, count) in enumerate(important, 1):
            theorem = self.parser.theorems.get(t_id)
            if theorem:
                lines.append(f"  {rank}. {t_id}: 被引用 {count} 次")
                lines.append(f"     {theorem.name}")
        lines.append("")
        
        # 3. 证明深度最大的定理
        lines.extend([
            "【证明深度最大】（依赖链最长）",
            "-" * 70
        ])
        by_depth = sorted(
            [(t_id, t.proof_depth) for t_id, t in self.parser.theorems.items()],
            key=lambda x: x[1],
            reverse=True
        )[:20]
        for rank, (t_id, depth) in enumerate(by_depth, 1):
            if depth >= 0:
                theorem = self.parser.theorems.get(t_id)
                if theorem:
                    lines.append(f"  {rank}. {t_id}: 深度 {depth}")
        lines.append("")
        
        # 4. 关键路径示例
        lines.extend([
            "【关键路径示例】（证明某定理所需的最少依赖链）",
            "-" * 70
        ])
        for theorem_id, _ in important[:5]:
            path = self.analyzer.find_critical_path(theorem_id)
            if path:
                lines.append(f"\n  证明 {theorem_id} 的关键路径:")
                for i, node in enumerate(path):
                    indent = "    " + "  " * i
                    lines.append(f"{indent}└─> {node}")
        lines.append("")
        
        # 5. 循环依赖警告
        cycles = self.analyzer.detect_cycles()
        if cycles:
            lines.extend([
                "【⚠️ 循环依赖警告】",
                "-" * 70
            ])
            for i, cycle in enumerate(cycles[:10], 1):
                lines.append(f"  {i}. {' -> '.join(cycle)} -> {cycle[0]}")
        else:
            lines.extend([
                "【✅ 循环依赖检查】",
                "-" * 70,
                "  未发现循环依赖"
            ])
        
        lines.extend([
            "",
            "=" * 70,
            "报告结束",
            "=" * 70
        ])
        
        Path(output_path).write_text('\n'.join(lines), encoding='utf-8')
        logger.info(f"关键路径报告已导出到: {output_path}")


class TheoremDependencyAnalyzer:
    """定理依赖关系分析器主类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_path = Path(config.get('base_path', '.'))
        self.output_dir = Path(config.get('output_dir', '.scripts/knowledge-graph/output'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.parser = TheoremParser(self.base_path)
        self.analyzer = None
    
    def run(self):
        """执行完整分析流程"""
        logger.info("=" * 70)
        logger.info("定理依赖关系分析器启动")
        logger.info("=" * 70)
        
        # 1. 解析文件
        directories = self.config.get('source_directories', ['Struct', 'Knowledge', 'Flink'])
        for directory in directories:
            self.parser.parse_directory(directory)
        
        # 2. 构建分析器
        self.analyzer = DependencyAnalyzer(self.parser)
        self.analyzer.build_dependency_graph()
        
        # 3. 计算指标
        self.analyzer.compute_complexity()
        self.analyzer.compute_proof_depth()
        
        # 4. 检测循环依赖
        cycles = self.analyzer.detect_cycles()
        
        # 5. 导出结果
        exporter = DependencyExporter(self.parser, self.analyzer)
        
        json_path = self.output_dir / "theorem-dependencies.json"
        exporter.export_json(str(json_path))
        
        txt_path = self.output_dir / "critical-path.txt"
        exporter.export_critical_path_txt(str(txt_path))
        
        # 6. 统计输出
        foundations = self.analyzer.find_foundation_theorems()
        important = self.analyzer.find_most_important(10)
        
        logger.info("=" * 70)
        logger.info("分析完成!")
        logger.info(f"  - 总定理数: {len(self.parser.theorems)}")
        logger.info(f"  - 总依赖数: {len(self.parser.edges)}")
        logger.info(f"  - 基础定理: {len(foundations)}")
        logger.info(f"  - 循环依赖: {len(cycles)}")
        logger.info("")
        logger.info("最重要的5个定理:")
        for i, (t_id, count) in enumerate(important[:5], 1):
            logger.info(f"  {i}. {t_id} (被引用 {count} 次)")
        logger.info("")
        logger.info(f"输出文件:")
        logger.info(f"  - JSON: {json_path}")
        logger.info(f"  - 报告: {txt_path}")
        logger.info("=" * 70)


def load_config(config_path: str) -> Dict[str, Any]:
    """加载配置文件"""
    default_config = {
        'base_path': '.',
        'output_dir': '.scripts/knowledge-graph/output',
        'source_directories': ['Struct', 'Knowledge', 'Flink']
    }
    
    config_file = Path(config_path)
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            default_config.update(user_config)
        except Exception as e:
            logger.warning(f"配置文件加载失败: {e}")
    
    return default_config


def main():
    parser = argparse.ArgumentParser(
        description='定理依赖关系分析器 - 分析定理、引理、命题之间的依赖关系'
    )
    parser.add_argument(
        '-c', '--config',
        default='.scripts/knowledge-graph/config.json',
        help='配置文件路径'
    )
    parser.add_argument(
        '-o', '--output',
        help='输出目录'
    )
    parser.add_argument(
        '-t', '--theorem',
        help='分析特定定理的关键路径'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细日志'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    config = load_config(args.config)
    if args.output:
        config['output_dir'] = args.output
    
    analyzer = TheoremDependencyAnalyzer(config)
    analyzer.run()
    
    # 如果指定了特定定理，打印其关键路径
    if args.theorem:
        path = analyzer.analyzer.find_critical_path(args.theorem)
        print(f"\n{args.theorem} 的关键路径:")
        for node in path:
            print(f"  -> {node}")


if __name__ == '__main__':
    main()
