#!/usr/bin/env python3
"""
概念关系图谱构建器 (Concept Map Builder)
======================================
从所有文档中提取概念定义，构建概念关系图谱，生成多种格式输出。

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
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict
import xml.etree.ElementTree as ET
from xml.dom import minidom

# 可选依赖
networkx_available = False
nltk_available = False

try:
    import networkx as nx
    networkx_available = True
except ImportError:
    pass

try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    nltk_available = True
except ImportError:
    pass


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Concept:
    """概念定义数据结构"""
    id: str
    name: str
    category: str  # definition, theorem, lemma, proposition, corollary
    source_file: str
    source_line: int
    definition: str
    formal_id: Optional[str] = None  # 如 Def-S-01-01
    dependencies: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    synonyms: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConceptRelation:
    """概念关系数据结构"""
    source: str
    target: str
    relation_type: str  # depends_on, references, equivalent, extends, implements
    weight: float = 1.0
    evidence: str = ""
    source_file: str = ""


class ConceptExtractor:
    """概念提取器 - 从Markdown文档中提取概念定义"""
    
    # 正则表达式模式
    FORMAL_ID_PATTERN = re.compile(r'(Def|Thm|Lemma|Prop|Cor)-([SKF])-(\d+)-(\d+)')
    
    # 定义关键词模式
    DEFINITION_PATTERNS = [
        re.compile(r'[#]+\s*\d+\.\s*概念定义.*\n+((?:[^#]|\n)*)', re.IGNORECASE),
        re.compile(r'\*\*定义[：:]\s*([^\n]+)\*\*', re.IGNORECASE),
        re.compile(r'`(Def-[SKF]-\d+-\d+)`[:：]\s*([^\n]+)'),
    ]
    
    # 定理/引理/命题模式
    THEOREM_PATTERNS = [
        re.compile(r'`(Thm-[SKF]-\d+-\d+)`[:：]\s*([^\n]+)'),
        re.compile(r'`(Lemma-[SKF]-\d+-\d+)`[:：]\s*([^\n]+)'),
        re.compile(r'`(Prop-[SKF]-\d+-\d+)`[:：]\s*([^\n]+)'),
        re.compile(r'`(Cor-[SKF]-\d+-\d+)`[:：]\s*([^\n]+)'),
    ]
    
    # 依赖关系模式
    DEPENDENCY_PATTERNS = [
        re.compile(r'(?:依赖|depends?\s+on|使用|using)\s*[`:]\s*(Def|Thm|Lemma|Prop|Cor)-([SKF])-(\d+)-(\d+)', re.IGNORECASE),
        re.compile(r'(?:根据|by|from)\s*[`:]\s*(Def|Thm|Lemma|Prop|Cor)-([SKF])-(\d+)-(\d+)', re.IGNORECASE),
    ]
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.concepts: Dict[str, Concept] = {}
        self.relations: List[ConceptRelation] = []
        self.stop_words: Set[str] = set()
        
        if nltk_available:
            try:
                self.stop_words = set(stopwords.words('english'))
                self.stop_words.update(set(stopwords.words('chinese')))
            except:
                pass
    
    def extract_from_file(self, file_path: Path) -> List[Concept]:
        """从单个文件中提取概念"""
        concepts = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
        except Exception as e:
            logger.error(f"无法读取文件 {file_path}: {e}")
            return concepts
        
        # 提取定义
        for match in self.FORMAL_ID_PATTERN.finditer(content):
            formal_id = match.group(0)
            line_num = content[:match.start()].count('\n') + 1
            
            # 获取定义文本（接下来的几行）
            definition_lines = []
            for i in range(line_num, min(line_num + 10, len(lines))):
                line = lines[i].strip()
                if line and not line.startswith('#') and not line.startswith('`'):
                    definition_lines.append(line)
                if len(definition_lines) >= 3:
                    break
            
            definition = ' '.join(definition_lines)[:500] if definition_lines else ""
            
            # 确定类别
            category_map = {
                'Def': 'definition',
                'Thm': 'theorem',
                'Lemma': 'lemma',
                'Prop': 'proposition',
                'Cor': 'corollary'
            }
            category = category_map.get(match.group(1), 'unknown')
            
            concept = Concept(
                id=formal_id,
                name=formal_id,  # 将在后续处理中提取更友好的名称
                category=category,
                source_file=str(file_path.relative_to(self.base_path)),
                source_line=line_num,
                definition=definition,
                formal_id=formal_id
            )
            
            concepts.append(concept)
            self.concepts[formal_id] = concept
        
        # 提取依赖关系
        for concept in concepts:
            for pattern in self.DEPENDENCY_PATTERNS:
                for match in pattern.finditer(content):
                    dep_id = f"{match.group(1)}-{match.group(2)}-{match.group(3)}-{match.group(4)}"
                    if dep_id != concept.id and dep_id in self.concepts:
                        concept.dependencies.append(dep_id)
                        self.relations.append(ConceptRelation(
                            source=concept.id,
                            target=dep_id,
                            relation_type='depends_on',
                            source_file=str(file_path.relative_to(self.base_path))
                        ))
        
        return concepts
    
    def extract_from_directory(self, directory: str, pattern: str = "*.md") -> int:
        """从目录中提取所有概念"""
        dir_path = self.base_path / directory
        if not dir_path.exists():
            logger.warning(f"目录不存在: {dir_path}")
            return 0
        
        files = list(dir_path.rglob(pattern))
        logger.info(f"在 {directory} 中找到 {len(files)} 个文件")
        
        total_concepts = 0
        for file_path in files:
            concepts = self.extract_from_file(file_path)
            total_concepts += len(concepts)
        
        # 提取交叉引用关系
        self._extract_cross_references()
        
        logger.info(f"总共提取 {total_concepts} 个概念，{len(self.relations)} 个关系")
        return total_concepts
    
    def _extract_cross_references(self):
        """提取文档间的交叉引用关系"""
        # 基于定义文本中的ID引用
        for concept_id, concept in self.concepts.items():
            for other_id in self.concepts:
                if other_id != concept_id and other_id in concept.definition:
                    if other_id not in concept.dependencies:
                        concept.references.append(other_id)
                        self.relations.append(ConceptRelation(
                            source=concept_id,
                            target=other_id,
                            relation_type='references',
                            evidence="definition_text"
                        ))


class GraphBuilder:
    """图谱构建器 - 构建NetworkX图并计算指标"""
    
    def __init__(self, extractor: ConceptExtractor):
        self.extractor = extractor
        self.graph = None
        if networkx_available:
            self.graph = nx.DiGraph()
    
    def build_graph(self) -> Optional[Any]:
        """构建NetworkX有向图"""
        if not networkx_available or self.graph is None:
            logger.warning("NetworkX不可用，跳过图构建")
            return None
        
        # 添加节点
        for concept_id, concept in self.extractor.concepts.items():
            self.graph.add_node(
                concept_id,
                name=concept.name,
                category=concept.category,
                source_file=concept.source_file,
                definition=concept.definition[:200]
            )
        
        # 添加边
        for relation in self.extractor.relations:
            if relation.source in self.extractor.concepts and \
               relation.target in self.extractor.concepts:
                self.graph.add_edge(
                    relation.source,
                    relation.target,
                    relation_type=relation.relation_type,
                    weight=relation.weight
                )
        
        logger.info(f"图构建完成: {self.graph.number_of_nodes()} 节点, {self.graph.number_of_edges()} 边")
        return self.graph
    
    def compute_centrality(self) -> Dict[str, Dict[str, float]]:
        """计算中心性指标"""
        if not networkx_available or self.graph is None:
            return {}
        
        centrality = {}
        
        # 度中心性
        try:
            in_degree = nx.in_degree_centrality(self.graph)
            out_degree = nx.out_degree_centrality(self.graph)
            for node in self.graph.nodes():
                centrality[node] = {
                    'in_degree': in_degree.get(node, 0),
                    'out_degree': out_degree.get(node, 0)
                }
        except Exception as e:
            logger.warning(f"度中心性计算失败: {e}")
        
        # 介数中心性
        try:
            betweenness = nx.betweenness_centrality(self.graph)
            for node, value in betweenness.items():
                centrality[node]['betweenness'] = value
        except Exception as e:
            logger.warning(f"介数中心性计算失败: {e}")
        
        # PageRank
        try:
            pagerank = nx.pagerank(self.graph)
            for node, value in pagerank.items():
                centrality[node]['pagerank'] = value
        except Exception as e:
            logger.warning(f"PageRank计算失败: {e}")
        
        # 将中心性指标添加到节点属性
        for node, metrics in centrality.items():
            for key, value in metrics.items():
                self.graph.nodes[node][key] = value
        
        return centrality
    
    def get_top_concepts(self, metric: str = 'pagerank', n: int = 20) -> List[Tuple[str, float]]:
        """获取最重要的概念"""
        if not networkx_available or self.graph is None:
            return []
        
        values = []
        for node in self.graph.nodes():
            if metric in self.graph.nodes[node]:
                values.append((node, self.graph.nodes[node][metric]))
        
        return sorted(values, key=lambda x: x[1], reverse=True)[:n]


class CypherExporter:
    """Neo4j Cypher导出器"""
    
    def __init__(self, extractor: ConceptExtractor):
        self.extractor = extractor
    
    def export(self, output_path: str):
        """导出为Cypher语句"""
        lines = [
            "// 概念图谱Cypher导入脚本",
            f"// 生成时间: {datetime.now().isoformat()}",
            "",
            "// 清除现有数据（可选）",
            "// MATCH (n:Concept) DETACH DELETE n;",
            "",
            "// 创建约束",
            "CREATE CONSTRAINT concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE;",
            "",
            "// 创建概念节点"
        ]
        
        # 创建节点
        for concept_id, concept in self.extractor.concepts.items():
            # 转义引号
            name = concept.name.replace('"', '\\"').replace("'", "\\'")
            definition = concept.definition[:300].replace('"', '\\"').replace("'", "\\'")
            
            lines.append(f'''
CREATE (c_{concept_id.replace('-', '_')}:Concept {{
    id: "{concept_id}",
    name: "{name}",
    category: "{concept.category}",
    source_file: "{concept.source_file}",
    source_line: {concept.source_line},
    definition: "{definition}..."
}});''')
        
        lines.append("")
        lines.append("// 创建关系")
        
        # 创建关系
        for relation in self.extractor.relations:
            if relation.source in self.extractor.concepts and \
               relation.target in self.extractor.concepts:
                source_var = f"c_{relation.source.replace('-', '_')}"
                target_var = f"c_{relation.target.replace('-', '_')}"
                
                lines.append(f'''
MATCH ({source_var}:Concept {{id: "{relation.source}"}})
MATCH ({target_var}:Concept {{id: "{relation.target}"}})
CREATE ({source_var})-[:{relation.relation_type.upper()} {{
    weight: {relation.weight},
    evidence: "{relation.evidence}"
}}]->({target_var});''')
        
        lines.append("")
        lines.append("// 创建索引")
        lines.append("CREATE INDEX concept_category IF NOT EXISTS FOR (c:Concept) ON (c.category);")
        lines.append("CREATE INDEX concept_source IF NOT EXISTS FOR (c:Concept) ON (c.source_file);")
        
        # 写入文件
        Path(output_path).write_text('\n'.join(lines), encoding='utf-8')
        logger.info(f"Cypher脚本已导出到: {output_path}")


class GexfExporter:
    """GEXF格式导出器（Gephi兼容）"""
    
    def __init__(self, extractor: ConceptExtractor, graph: Any = None):
        self.extractor = extractor
        self.graph = graph
    
    def export(self, output_path: str):
        """导出为GEXF格式"""
        # 创建XML根元素
        root = ET.Element("gexf")
        root.set("xmlns", "http://www.gexf.net/1.3")
        root.set("version", "1.3")
        
        # 元数据
        meta = ET.SubElement(root, "meta")
        meta.set("lastmodifieddate", datetime.now().strftime("%Y-%m-%d"))
        creator = ET.SubElement(meta, "creator")
        creator.text = "Concept Map Builder"
        description = ET.SubElement(meta, "description")
        description.text = "Knowledge Graph Concept Map"
        
        # 图定义
        graph_elem = ET.SubElement(root, "graph")
        graph_elem.set("defaultedgetype", "directed")
        graph_elem.set("mode", "static")
        
        # 属性定义
        attributes = ET.SubElement(graph_elem, "attributes")
        attributes.set("class", "node")
        attributes.set("mode", "static")
        
        attr_defs = [
            ("category", "string", "Category"),
            ("source_file", "string", "Source File"),
            ("definition", "string", "Definition"),
            ("in_degree", "float", "In-Degree Centrality"),
            ("out_degree", "float", "Out-Degree Centrality"),
            ("pagerank", "float", "PageRank"),
        ]
        
        for i, (id_, type_, title) in enumerate(attr_defs):
            attr = ET.SubElement(attributes, "attribute")
            attr.set("id", str(i))
            attr.set("title", title)
            attr.set("type", type_)
        
        # 节点
        nodes_elem = ET.SubElement(graph_elem, "nodes")
        for concept_id, concept in self.extractor.concepts.items():
            node = ET.SubElement(nodes_elem, "node")
            node.set("id", concept_id)
            node.set("label", concept.name or concept_id)
            
            # 添加属性
            attvalues = ET.SubElement(node, "attvalues")
            
            attvalue = ET.SubElement(attvalues, "attvalue")
            attvalue.set("for", "0")
            attvalue.set("value", concept.category)
            
            attvalue = ET.SubElement(attvalues, "attvalue")
            attvalue.set("for", "1")
            attvalue.set("value", concept.source_file)
            
            attvalue = ET.SubElement(attvalues, "attvalue")
            attvalue.set("for", "2")
            attvalue.set("value", concept.definition[:200])
            
            # 添加中心性指标（如果有）
            if self.graph and networkx_available and concept_id in self.graph.nodes:
                node_data = self.graph.nodes[concept_id]
                for i, key in enumerate(['in_degree', 'out_degree', 'pagerank'], start=3):
                    if key in node_data:
                        attvalue = ET.SubElement(attvalues, "attvalue")
                        attvalue.set("for", str(i))
                        attvalue.set("value", str(node_data[key]))
        
        # 边
        edges_elem = ET.SubElement(graph_elem, "edges")
        edge_id = 0
        for relation in self.extractor.relations:
            if relation.source in self.extractor.concepts and \
               relation.target in self.extractor.concepts:
                edge = ET.SubElement(edges_elem, "edge")
                edge.set("id", str(edge_id))
                edge.set("source", relation.source)
                edge.set("target", relation.target)
                edge.set("label", relation.relation_type)
                edge.set("weight", str(relation.weight))
                edge_id += 1
        
        # 格式化并写入
        xml_str = ET.tostring(root, encoding='unicode')
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
        
        # 移除空白行
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        pretty_xml = '\n'.join(lines)
        
        Path(output_path).write_text(pretty_xml, encoding='utf-8')
        logger.info(f"GEXF文件已导出到: {output_path}")


class ConceptMapBuilder:
    """概念图谱构建器主类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_path = Path(config.get('base_path', '.'))
        self.output_dir = Path(config.get('output_dir', '.scripts/knowledge-graph/output'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.extractor = ConceptExtractor(self.base_path)
        self.graph_builder = None
        self.graph = None
    
    def run(self):
        """执行完整的构建流程"""
        logger.info("=" * 60)
        logger.info("概念图谱构建器启动")
        logger.info("=" * 60)
        
        # 1. 从各目录提取概念
        directories = self.config.get('source_directories', ['Struct', 'Knowledge', 'Flink'])
        for directory in directories:
            self.extractor.extract_from_directory(directory)
        
        # 2. 构建图
        self.graph_builder = GraphBuilder(self.extractor)
        self.graph = self.graph_builder.build_graph()
        
        # 3. 计算中心性指标
        if self.graph and networkx_available:
            centrality = self.graph_builder.compute_centrality()
            top_concepts = self.graph_builder.get_top_concepts('pagerank', 20)
            
            logger.info("\nTop 20 核心概念 (按PageRank):")
            for i, (concept_id, score) in enumerate(top_concepts, 1):
                concept = self.extractor.concepts.get(concept_id)
                logger.info(f"  {i}. {concept_id} ({concept.category if concept else 'unknown'}): {score:.4f}")
        
        # 4. 导出Cypher
        cypher_exporter = CypherExporter(self.extractor)
        cypher_path = self.output_dir / "graph-data.cypher"
        cypher_exporter.export(str(cypher_path))
        
        # 5. 导出GEXF
        gexf_exporter = GexfExporter(self.extractor, self.graph)
        gexf_path = self.output_dir / "graph.gexf"
        gexf_exporter.export(str(gexf_path))
        
        # 6. 导出JSON摘要
        summary_path = self.output_dir / "concept-summary.json"
        self._export_summary(summary_path)
        
        logger.info("=" * 60)
        logger.info("概念图谱构建完成!")
        logger.info(f"输出目录: {self.output_dir}")
        logger.info(f"  - Cypher脚本: {cypher_path}")
        logger.info(f"  - GEXF文件: {gexf_path}")
        logger.info(f"  - 摘要JSON: {summary_path}")
        logger.info("=" * 60)
    
    def _export_summary(self, output_path: Path):
        """导出摘要信息"""
        summary = {
            'generated_at': datetime.now().isoformat(),
            'statistics': {
                'total_concepts': len(self.extractor.concepts),
                'total_relations': len(self.extractor.relations),
                'by_category': {}
            },
            'concepts': {},
            'relations': []
        }
        
        # 按类别统计
        for concept in self.extractor.concepts.values():
            category = concept.category
            summary['statistics']['by_category'][category] = \
                summary['statistics']['by_category'].get(category, 0) + 1
        
        # 导出概念（限制字段）
        for concept_id, concept in self.extractor.concepts.items():
            summary['concepts'][concept_id] = {
                'name': concept.name,
                'category': concept.category,
                'source_file': concept.source_file,
                'definition': concept.definition[:200],
                'dependencies': concept.dependencies[:10],
                'references': concept.references[:10]
            }
            
            # 添加中心性指标
            if self.graph and networkx_available and concept_id in self.graph.nodes:
                node_data = self.graph.nodes[concept_id]
                for key in ['in_degree', 'out_degree', 'betweenness', 'pagerank']:
                    if key in node_data:
                        summary['concepts'][concept_id][key] = node_data[key]
        
        # 导出关系
        for relation in self.extractor.relations[:1000]:  # 限制数量
            summary['relations'].append({
                'source': relation.source,
                'target': relation.target,
                'type': relation.relation_type,
                'weight': relation.weight
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)


def load_config(config_path: str) -> Dict[str, Any]:
    """加载配置文件"""
    default_config = {
        'base_path': '.',
        'output_dir': '.scripts/knowledge-graph/output',
        'source_directories': ['Struct', 'Knowledge', 'Flink'],
        'max_file_size_mb': 10,
        'include_patterns': ['*.md'],
        'exclude_patterns': ['README*', 'CHANGELOG*', 'ARCHIVE*']
    }
    
    config_file = Path(config_path)
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            default_config.update(user_config)
            logger.info(f"已加载配置文件: {config_path}")
        except Exception as e:
            logger.warning(f"配置文件加载失败: {e}，使用默认配置")
    else:
        logger.info("未找到配置文件，使用默认配置")
    
    return default_config


def main():
    parser = argparse.ArgumentParser(
        description='概念关系图谱构建器 - 从文档提取概念并构建知识图谱'
    )
    parser.add_argument(
        '-c', '--config',
        default='.scripts/knowledge-graph/config.json',
        help='配置文件路径'
    )
    parser.add_argument(
        '-o', '--output',
        help='输出目录（覆盖配置文件中的设置）'
    )
    parser.add_argument(
        '--export-only',
        choices=['cypher', 'gexf', 'json', 'all'],
        default='all',
        help='仅导出指定格式'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细日志'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 加载配置
    config = load_config(args.config)
    if args.output:
        config['output_dir'] = args.output
    
    # 运行构建器
    builder = ConceptMapBuilder(config)
    builder.run()


if __name__ == '__main__':
    main()
