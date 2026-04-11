#!/usr/bin/env python3
"""
AnalysisDataFlow Entity Extractor
Automatically extract entities and relationships from markdown documents
"""

import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class Entity:
    """Represents a knowledge entity"""
    id: str
    label: str
    type: str
    category: str
    description: str = ""
    source_file: str = ""
    line_number: int = 0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Relation:
    """Represents a relationship between entities"""
    source: str
    target: str
    type: str
    label: str = ""
    weight: float = 1.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class MarkdownEntityExtractor:
    """Extract entities from markdown files"""
    
    # Patterns for entity extraction
    PATTERNS = {
        # Formal elements (Thm-*, Def-*, Lemma-*, Prop-*, Cor-*)
        "theorem": re.compile(r'`?(Thm-[A-Z]-\d{2}-\d{2})`?[^\n]*[定理|Theorem][^\n]*[:：]\s*([^\n]+)', re.IGNORECASE),
        "definition": re.compile(r'`?(Def-[A-Z]-\d{2}-\d{2})`?[^\n]*[定义|Definition][^\n]*[:：]\s*([^\n]+)', re.IGNORECASE),
        "lemma": re.compile(r'`?(Lemma-[A-Z]-\d{2}-\d{2})`?[^\n]*[引理|Lemma][^\n]*[:：]\s*([^\n]+)', re.IGNORECASE),
        "proposition": re.compile(r'`?(Prop-[A-Z]-\d{2}-\d{2})`?[^\n]*[命题|Proposition][^\n]*[:：]\s*([^\n]+)', re.IGNORECASE),
        "corollary": re.compile(r'`?(Cor-[A-Z]-\d{2}-\d{2})`?[^\n]*[推论|Corollary][^\n]*[:：]\s*([^\n]+)', re.IGNORECASE),
        
        # Section headers as concepts
        "section": re.compile(r'^##+\s+(.+)$', re.MULTILINE),
        
        # Key concepts (bold or emphasized terms)
        "concept": re.compile(r'\*\*([^*]+)\*\*|__([^_]+)__'),
        
        # Links to other documents
        "doc_link": re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)'),
        
        # Code references
        "code_ref": re.compile(r'`([A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)+)`'),
        
        # Flink-specific patterns
        "flink_class": re.compile(r'`?(\w+Function|(\w+)Sink|(\w+)Source|(\w+)Descriptor)`?'),
        "flink_config": re.compile(r'`?([a-z-]+\.(checkpoint|state|restart|execution)[a-z-]*)`?'),
    }
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.entities: Dict[str, Entity] = {}
        self.relations: List[Relation] = []
        self.document_links: Dict[str, Set[str]] = defaultdict(set)
    
    def extract_from_file(self, file_path: Path) -> Tuple[List[Entity], List[Relation]]:
        """Extract entities from a single markdown file"""
        entities = []
        relations = []
        
        content = file_path.read_text(encoding="utf-8")
        rel_path = str(file_path.relative_to(self.base_dir))
        
        # Extract formal elements
        for entity_type, pattern in self.PATTERNS.items():
            if entity_type in ["theorem", "definition", "lemma", "proposition", "corollary"]:
                for match in pattern.finditer(content):
                    entity_id = match.group(1)
                    label = match.group(2).strip()
                    
                    # Get context (description)
                    line_start = content.rfind('\n', 0, match.start()) + 1
                    line_end = content.find('\n', match.end())
                    description = content[line_end:line_end+200].strip()
                    description = description.split('\n')[0][:150]
                    
                    entity = Entity(
                        id=entity_id,
                        label=label,
                        type=entity_type,
                        category="formal",
                        description=description,
                        source_file=rel_path,
                        line_number=content[:match.start()].count('\n') + 1
                    )
                    entities.append(entity)
                    self.entities[entity_id] = entity
                    
                    # Create relation from document to entity
                    doc_id = self._doc_path_to_id(rel_path)
                    relations.append(Relation(
                        source=doc_id,
                        target=entity_id,
                        type="contains",
                        label="包含"
                    ))
            
            elif entity_type == "section":
                # Extract major sections as concepts
                for i, match in enumerate(pattern.finditer(content)):
                    if i >= 10:  # Limit to first 10 sections
                        break
                    label = match.group(1).strip()
                    entity_id = f"{rel_path}#{label.replace(' ', '-').lower()[:30]}"
                    
                    entity = Entity(
                        id=entity_id,
                        label=label,
                        type="section",
                        category="structure",
                        source_file=rel_path,
                        line_number=content[:match.start()].count('\n') + 1
                    )
                    entities.append(entity)
            
            elif entity_type == "doc_link":
                # Extract document links
                for match in pattern.finditer(content):
                    target_doc = match.group(2)
                    self.document_links[rel_path].add(target_doc)
                    
                    source_id = self._doc_path_to_id(rel_path)
                    target_id = self._doc_path_to_id(target_doc)
                    
                    relations.append(Relation(
                        source=source_id,
                        target=target_id,
                        type="references",
                        label="引用",
                        weight=1.0
                    ))
        
        return entities, relations
    
    def _doc_path_to_id(self, path: str) -> str:
        """Convert document path to entity ID"""
        return path.replace('/', '_').replace('.md', '').replace('\\', '_')
    
    def extract_from_directory(self, dir_path: Path, pattern: str = "*.md") -> Dict[str, Any]:
        """Extract entities from all markdown files in directory"""
        dir_path = self.base_dir / dir_path
        all_entities = []
        all_relations = []
        
        for md_file in dir_path.rglob(pattern):
            if md_file.name == "00-INDEX.md":
                continue
            
            entities, relations = self.extract_from_file(md_file)
            all_entities.extend(entities)
            all_relations.extend(relations)
        
        # Create document entities
        doc_entities = []
        for md_file in dir_path.rglob(pattern):
            if md_file.name == "00-INDEX.md":
                continue
            
            rel_path = str(md_file.relative_to(self.base_dir))
            content = md_file.read_text(encoding="utf-8")
            
            # Extract title
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else md_file.stem
            
            # Count formal elements
            formal_count = len(re.findall(r'`?(Thm|Def|Lemma|Prop|Cor)-[A-Z]-\d{2}-\d{2}`?', content))
            
            doc_id = self._doc_path_to_id(rel_path)
            entity = Entity(
                id=doc_id,
                label=title,
                type="document",
                category=dir_path.name.lower(),
                description=f"Document with {formal_count} formal elements",
                source_file=rel_path,
                metadata={
                    "word_count": len(content.split()),
                    "formal_elements": formal_count
                }
            )
            doc_entities.append(entity)
        
        all_entities.extend(doc_entities)
        
        return {
            "entities": [asdict(e) for e in all_entities],
            "relations": [asdict(r) for r in all_relations],
            "stats": {
                "total_documents": len(doc_entities),
                "total_entities": len(all_entities),
                "total_relations": len(all_relations),
                "formal_elements": len([e for e in all_entities if e.type in 
                    ["theorem", "definition", "lemma", "proposition", "corollary"]])
            }
        }
    
    def build_dependency_graph(self) -> Dict[str, Any]:
        """Build concept dependency graph from extracted entities"""
        # Define core concepts and their dependencies
        concept_hierarchy = {
            "流计算基础": {
                "layer": 0,
                "depends_on": [],
                "description": "流计算的基本概念"
            },
            "时间语义": {
                "layer": 1,
                "depends_on": ["流计算基础"],
                "description": "事件时间、处理时间"
            },
            "窗口机制": {
                "layer": 1,
                "depends_on": ["流计算基础"],
                "description": "窗口类型和操作"
            },
            "Watermark": {
                "layer": 2,
                "depends_on": ["时间语义", "窗口机制"],
                "description": "乱序事件处理"
            },
            "一致性语义": {
                "layer": 1,
                "depends_on": ["流计算基础"],
                "description": "Exactly-Once等语义"
            },
            "状态管理": {
                "layer": 2,
                "depends_on": ["一致性语义"],
                "description": "有状态计算"
            },
            "Checkpoint": {
                "layer": 3,
                "depends_on": ["状态管理"],
                "description": "容错机制"
            },
            "Flink基础": {
                "layer": 2,
                "depends_on": ["流计算基础", "时间语义"],
                "description": "Flink核心概念"
            },
            "DataStream API": {
                "layer": 3,
                "depends_on": ["Flink基础"],
                "description": "流处理API"
            },
            "状态后端": {
                "layer": 3,
                "depends_on": ["状态管理", "Flink基础"],
                "description": "状态存储实现"
            }
        }
        
        nodes = []
        edges = []
        
        for concept_id, info in concept_hierarchy.items():
            node_id = concept_id.lower().replace(" ", "-")
            nodes.append({
                "id": node_id,
                "label": concept_id,
                "type": "concept",
                "category": "foundation" if info["layer"] < 2 else "advanced",
                "layer": info["layer"],
                "description": info["description"]
            })
            
            for dep in info["depends_on"]:
                dep_id = dep.lower().replace(" ", "-")
                edges.append({
                    "source": dep_id,
                    "target": node_id,
                    "type": "prerequisite",
                    "label": "前置"
                })
        
        return {
            "name": "自动提取概念依赖图",
            "description": "从文档自动提取的概念依赖关系",
            "nodes": nodes,
            "edges": edges,
            "categories": {
                "foundation": {"label": "基础", "color": "#3498DB"},
                "advanced": {"label": "进阶", "color": "#E74C3C"}
            },
            "relationTypes": {
                "prerequisite": {"label": "前置", "color": "#E74C3C", "style": "solid"}
            }
        }


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description="Extract entities from markdown documents")
    parser.add_argument("--base-dir", default=".", help="Base directory for documents")
    parser.add_argument("--output", "-o", default="extracted-entities.json", help="Output file")
    parser.add_argument("--build-deps", action="store_true", help="Build dependency graph")
    parser.add_argument("dirs", nargs="+", help="Directories to scan")
    
    args = parser.parse_args()
    
    base_dir = Path(args.base_dir)
    extractor = MarkdownEntityExtractor(base_dir)
    
    all_results = {
        "entities": [],
        "relations": [],
        "by_directory": {}
    }
    
    for dir_name in args.dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"Scanning {dir_path}...")
            result = extractor.extract_from_directory(Path(dir_name))
            all_results["by_directory"][dir_name] = result
            all_results["entities"].extend(result["entities"])
            all_results["relations"].extend(result["relations"])
            print(f"  Found {result['stats']['total_entities']} entities, "
                  f"{result['stats']['total_relations']} relations")
    
    # Add dependency graph if requested
    if args.build_deps:
        all_results["dependency_graph"] = extractor.build_dependency_graph()
    
    # Write output
    output_path = Path(args.output)
    output_path.write_text(json.dumps(all_results, indent=2, ensure_ascii=False), 
                           encoding="utf-8")
    print(f"\nOutput written to: {output_path}")
    
    # Print summary
    total_entities = len(all_results["entities"])
    total_relations = len(all_results["relations"])
    print(f"\nTotal: {total_entities} entities, {total_relations} relations")


if __name__ == "__main__":
    main()
