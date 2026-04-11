#!/usr/bin/env python3
"""
概念关系图谱构建工具
功能：
- 解析所有文档提取概念
- 构建概念关系网络
- 导出Neo4j格式

作者: AnalysisDataFlow Toolchain Team
版本: 1.0.0
日期: 2026-04-11
"""

import re
import os
import json
import glob
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import argparse


@dataclass
class Concept:
    """概念节点"""
    id: str
    name: str
    name_zh: str
    name_en: str
    concept_type: str  # 'formal_element', 'pattern', 'technology', 'domain'
    source_file: str
    line_number: int
    definition: str
    related_concepts: List[str] = field(default_factory=list)
    properties: Dict = field(default_factory=dict)


@dataclass
class ConceptRelation:
    """概念关系边"""
    source: str
    target: str
    relation_type: str  # 'depends_on', 'implements', 'extends', 'references', 'similar_to'
    strength: float  # 0.0 - 1.0
    source_file: str
    evidence: str


class ConceptGraphBuilder:
    """概念关系图谱构建器"""
    
    # 概念提取模式
    CONCEPT_PATTERNS = {
        'formal_definition': [
            r'\*\*定义\s*\([^)]+\)\s*[:：]\s*([^*]+)',
            r'\*\*Definition\s*\([^)]+\)\s*:\s*([^*]+)',
        ],
        'formal_theorem': [
            r'\*\*定理\s*\([^)]+\)\s*[:：]\s*([^*]+)',
            r'\*\*Theorem\s*\([^)]+\)\s*:\s*([^*]+)',
        ],
        'concept_heading': [
            r'^#{2,4}\s+([^\(]+)(?:\([^)]*\))?\s*$',
        ],
    }
    
    # 关系关键词
    RELATION_KEYWORDS = {
        'depends_on': ['依赖', 'depends on', 'requires', '需要', '基于'],
        'implements': ['实现', 'implements', 'realizes', '实例化'],
        'extends': ['扩展', 'extends', '继承', 'inherits', 'generalizes'],
        'references': ['引用', 'references', 'see also', '参见', '详见'],
        'similar_to': ['类似', 'similar to', 'analogous to', '类似于', '等同于'],
        'contrasts_with': ['对比', 'vs', 'versus', 'compared to', '不同于'],
    }
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        self.concepts: Dict[str, Concept] = {}
        self.relations: List[ConceptRelation] = []
        self.concept_index: Dict[str, Set[str]] = defaultdict(set)  # 名称 -> 概念ID集合
        
    def scan_all_files(self) -> List[Path]:
        """扫描所有Markdown文件"""
        md_files = []
        patterns = [
            "Struct/**/*.md",
            "Knowledge/**/*.md",
            "Flink/**/*.md",
        ]
        
        for pattern in patterns:
            files = glob.glob(str(self.base_path / pattern), recursive=True)
            for f in files:
                path = Path(f).resolve()
                if not any(x in str(path) for x in ['TEMPLATE', '_TEMPLATE', '00-INDEX']):
                    md_files.append(path)
                    
        return sorted(set(md_files))
    
    def generate_concept_id(self, name: str, source_file: str) -> str:
        """生成概念唯一ID"""
        # 基于名称和文件路径生成哈希
        hash_input = f"{name}:{source_file}"
        hash_val = hash(hash_input) % 10000000
        return f"C{hash_val:07d}"
    
    def extract_concepts_from_file(self, file_path: Path) -> List[Concept]:
        """从文件中提取概念"""
        concepts = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            return concepts
            
        rel_path = str(file_path.relative_to(self.base_path))
        lines = content.split('\n')
        
        # 1. 提取形式化定义
        for line_num, line in enumerate(lines, 1):
            # 定义
            def_match = re.search(r'\*\*定义\s*\((Def-[SKF]-\d{2}-\d{2,3})\)\s*[:：]\s*\*\*([^*]+)\*\*', line)
            if def_match:
                def_id, def_name = def_match.groups()
                concept = Concept(
                    id=self.generate_concept_id(def_name, rel_path),
                    name=def_name,
                    name_zh=def_name,
                    name_en=def_name,
                    concept_type='formal_definition',
                    source_file=rel_path,
                    line_number=line_num,
                    definition=line.strip(),
                    properties={'formal_id': def_id}
                )
                concepts.append(concept)
                
            # 定理
            thm_match = re.search(r'\*\*定理\s*\((Thm-[SKF]-\d{2}-\d{2,3})\)\s*[:：]\s*\*\*([^*]+)\*\*', line)
            if thm_match:
                thm_id, thm_name = thm_match.groups()
                concept = Concept(
                    id=self.generate_concept_id(thm_name, rel_path),
                    name=thm_name,
                    name_zh=thm_name,
                    name_en=thm_name,
                    concept_type='formal_theorem',
                    source_file=rel_path,
                    line_number=line_num,
                    definition=line.strip(),
                    properties={'formal_id': thm_id}
                )
                concepts.append(concept)
                
        # 2. 提取章节标题作为概念
        for line_num, line in enumerate(lines, 1):
            # 二级或三级标题
            heading_match = re.match(r'^#{2,3}\s+([^#]+)$', line.strip())
            if heading_match:
                heading = heading_match.group(1).strip()
                # 跳过标准章节
                if any(h in heading for h in ['概念定义', '属性推导', '关系建立', '论证过程', '形式证明', '实例验证', '可视化', '引用参考']):
                    continue
                    
                concept = Concept(
                    id=self.generate_concept_id(heading, rel_path),
                    name=heading,
                    name_zh=heading,
                    name_en=heading,
                    concept_type='section_concept',
                    source_file=rel_path,
                    line_number=line_num,
                    definition=heading,
                    properties={'level': line.count('#')}
                )
                concepts.append(concept)
                
        return concepts
    
    def extract_relations(self, content: str, concepts: List[Concept], file_path: str) -> List[ConceptRelation]:
        """提取概念间关系"""
        relations = []
        lines = content.split('\n')
        
        # 构建概念名称到ID的映射
        name_to_id = {}
        for c in concepts:
            name_to_id[c.name] = c.id
            name_to_id[c.name.lower()] = c.id
            
        for line_num, line in enumerate(lines, 1):
            # 检查每种关系类型
            for rel_type, keywords in self.RELATION_KEYWORDS.items():
                for keyword in keywords:
                    if keyword in line:
                        # 尝试找到关系两边的概念
                        for c1 in concepts:
                            for c2 in concepts:
                                if c1.id != c2.id and c1.name in line and c2.name in line:
                                    # 检查相对位置
                                    pos1 = line.find(c1.name)
                                    pos2 = line.find(c2.name)
                                    pos_kw = line.find(keyword)
                                    
                                    # 简单的启发式：关键词在两者之间或之后
                                    if (pos1 < pos_kw < pos2) or (pos2 < pos_kw < pos1) or (pos_kw < pos1 and pos_kw < pos2):
                                        relation = ConceptRelation(
                                            source=c1.id if pos1 < pos2 else c2.id,
                                            target=c2.id if pos1 < pos2 else c1.id,
                                            relation_type=rel_type,
                                            strength=0.7,  # 默认强度
                                            source_file=file_path,
                                            evidence=line.strip()[:200]
                                        )
                                        relations.append(relation)
                                        
        return relations
    
    def infer_additional_relations(self) -> List[ConceptRelation]:
        """推断额外关系"""
        relations = []
        
        # 1. 同文件概念建立关系
        file_concepts = defaultdict(list)
        for concept in self.concepts.values():
            file_concepts[concept.source_file].append(concept)
            
        for file_path, concepts in file_concepts.items():
            # 按行号排序
            concepts.sort(key=lambda c: c.line_number)
            
            # 相邻概念建立弱关系
            for i in range(len(concepts) - 1):
                relations.append(ConceptRelation(
                    source=concepts[i].id,
                    target=concepts[i + 1].id,
                    relation_type='co_occurs_with',
                    strength=0.3,
                    source_file=file_path,
                    evidence='Same file co-occurrence'
                ))
                
        # 2. 同名概念建立等价关系
        name_groups = defaultdict(list)
        for concept in self.concepts.values():
            name_groups[concept.name].append(concept)
            
        for name, group in name_groups.items():
            if len(group) > 1:
                for i in range(len(group) - 1):
                    for j in range(i + 1, len(group)):
                        relations.append(ConceptRelation(
                            source=group[i].id,
                            target=group[j].id,
                            relation_type='equivalent_to',
                            strength=0.9,
                            source_file='inferred',
                            evidence=f'Same name: {name}'
                        ))
                        
        return relations
    
    def build_graph(self) -> Tuple[Dict[str, Concept], List[ConceptRelation]]:
        """构建完整图谱"""
        print("🌐 Concept Graph Builder")
        print("=" * 50)
        
        files = self.scan_all_files()
        print(f"\n📁 Found {len(files)} target files")
        
        # 1. 提取所有概念
        print("\n🔎 Extracting concepts...")
        all_concepts = []
        for i, file_path in enumerate(files, 1):
            if i % 50 == 0:
                print(f"   Progress: {i}/{len(files)} files")
            concepts = self.extract_concepts_from_file(file_path)
            all_concepts.extend(concepts)
            
        # 去重并构建概念字典
        for concept in all_concepts:
            if concept.id not in self.concepts:
                self.concepts[concept.id] = concept
                self.concept_index[concept.name].add(concept.id)
                
        print(f"   Extracted {len(self.concepts)} unique concepts")
        
        # 2. 提取关系
        print("\n🔗 Extracting relations...")
        all_relations = []
        for i, file_path in enumerate(files, 1):
            if i % 50 == 0:
                print(f"   Progress: {i}/{len(files)} files")
            try:
                content = file_path.read_text(encoding='utf-8')
                rel_path = str(file_path.relative_to(self.base_path))
                file_concepts = [c for c in all_concepts if c.source_file == rel_path]
                relations = self.extract_relations(content, file_concepts, rel_path)
                all_relations.extend(relations)
            except Exception:
                pass
                
        self.relations.extend(all_relations)
        print(f"   Extracted {len(self.relations)} explicit relations")
        
        # 3. 推断额外关系
        print("\n🧠 Inferring additional relations...")
        inferred = self.infer_additional_relations()
        self.relations.extend(inferred)
        print(f"   Inferred {len(inferred)} additional relations")
        
        return self.concepts, self.relations
    
    def export_to_neo4j(self, output_dir: str):
        """导出为Neo4j导入格式"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 1. 导出节点 (CSV)
        nodes_csv = output_path / 'concept_nodes.csv'
        with open(nodes_csv, 'w', encoding='utf-8') as f:
            f.write('id:ID,name,name_zh,name_en,type,source_file,line_number,definition\n')
            for concept in self.concepts.values():
                f.write(f'"{concept.id}","{concept.name}","{concept.name_zh}","{concept.name_en}",')
                f.write(f'"{concept.concept_type}","{concept.source_file}",{concept.line_number},')
                f.write(f'"{concept.definition[:200].replace(chr(34), chr(39))}"\n')
                
        # 2. 导出关系 (CSV)
        rels_csv = output_path / 'concept_relations.csv'
        with open(rels_csv, 'w', encoding='utf-8') as f:
            f.write(':START_ID,:END_ID,:TYPE,strength:float,source_file,evidence\n')
            for rel in self.relations:
                f.write(f'"{rel.source}","{rel.target}","{rel.relation_type}",')
                f.write(f'{rel.strength},"{rel.source_file}","{rel.evidence[:200]}"\n')
                
        # 3. 导出Cypher导入脚本
        cypher_file = output_path / 'import.cypher'
        with open(cypher_file, 'w', encoding='utf-8') as f:
            f.write("// Neo4j Concept Graph Import Script\n\n")
            f.write("// Create constraints\n")
            f.write("CREATE CONSTRAINT concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE;\n\n")
            f.write("// Load nodes\n")
            f.write("LOAD CSV WITH HEADERS FROM 'file:///concept_nodes.csv' AS row\n")
            f.write("CREATE (c:Concept {\n")
            f.write("  id: row.id,\n")
            f.write("  name: row.name,\n")
            f.write("  name_zh: row.name_zh,\n")
            f.write("  name_en: row.name_en,\n")
            f.write("  type: row.type,\n")
            f.write("  source_file: row.source_file,\n")
            f.write("  line_number: toInteger(row.line_number),\n")
            f.write("  definition: row.definition\n")
            f.write("});\n\n")
            f.write("// Load relations\n")
            f.write("LOAD CSV WITH HEADERS FROM 'file:///concept_relations.csv' AS row\n")
            f.write("MATCH (c1:Concept {id: row.START_ID})\n")
            f.write("MATCH (c2:Concept {id: row.END_ID})\n")
            f.write("CREATE (c1)-[r:RELATES {\n")
            f.write("  type: row.TYPE,\n")
            f.write("  strength: toFloat(row.strength),\n")
            f.write("  source_file: row.source_file,\n")
            f.write("  evidence: row.evidence\n")
            f.write("}]->(c2);\n")
            
        print(f"\n📁 Neo4j export saved to: {output_dir}")
        print(f"   - Nodes: {nodes_csv}")
        print(f"   - Relations: {rels_csv}")
        print(f"   - Cypher script: {cypher_file}")
        
    def export_to_json(self, output_path: str):
        """导出为JSON格式"""
        graph_data = {
            'nodes': [asdict(c) for c in self.concepts.values()],
            'edges': [asdict(r) for r in self.relations],
            'metadata': {
                'total_concepts': len(self.concepts),
                'total_relations': len(self.relations),
                'concept_types': list(set(c.concept_type for c in self.concepts.values())),
                'relation_types': list(set(r.relation_type for r in self.relations))
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
            
        print(f"\n📁 JSON export saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Concept Graph Builder')
    parser.add_argument('--base-path', default='.', help='项目根目录')
    parser.add_argument('--output-dir', default='knowledge-graph-export', help='输出目录')
    parser.add_argument('--format', choices=['neo4j', 'json', 'both'], default='both', help='导出格式')
    
    args = parser.parse_args()
    
    builder = ConceptGraphBuilder(args.base_path)
    concepts, relations = builder.build_graph()
    
    # 导出
    if args.format in ['neo4j', 'both']:
        builder.export_to_neo4j(args.output_dir)
        
    if args.format in ['json', 'both']:
        json_path = Path(args.output_dir) / 'concept_graph.json'
        builder.export_to_json(str(json_path))
        
    # 打印摘要
    print("\n" + "=" * 50)
    print("📊 BUILD SUMMARY")
    print("=" * 50)
    print(f"Total concepts:   {len(concepts)}")
    print(f"Total relations:  {len(relations)}")
    print(f"Concept types:    {len(set(c.concept_type for c in concepts.values()))}")
    print(f"Relation types:   {len(set(r.relation_type for r in relations))}")
    print("=" * 50)
    
    return 0


if __name__ == '__main__':
    exit(main())
