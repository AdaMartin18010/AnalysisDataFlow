#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update knowledge graph data for v4.3 - Add 12 new documents
"""

import json
import os
from datetime import datetime

BASE_DIR = r"e:\_src\AnalysisDataFlow"

# New documents metadata
NEW_DOCS = [
    {
        "path": "Struct/06-frontier/llm-guided-formal-proof-automation.md",
        "title": "LLM 辅助形式化证明自动化",
        "group": "Struct",
        "color": "#4A90D9",
        "formality_level": "L5-L6",
        "category": "06-frontier",
        "word_count": 5662,
        "tags": ["LLM", "Formal Verification", "TLA+", "Coq", "Lean 4", "Proof Automation"],
        "related_nodes": ["Struct_06-frontier_06.01-open-problems-streaming-verification"]
    },
    {
        "path": "formal-methods/06-tools/veil-framework-lean4.md",
        "title": "Veil Framework — 基于 Lean 4 的新一代迁移系统验证框架",
        "group": "FormalMethods",
        "color": "#8E44AD",
        "formality_level": "L5-L6",
        "category": "06-tools",
        "word_count": 5815,
        "tags": ["Veil", "Lean 4", "SMT", "Verification Conditions", "Distributed Systems"],
        "related_nodes": ["Struct_06-frontier_06.01-open-problems-streaming-verification"]
    },
    {
        "path": "Struct/01-foundation/minimal-session-types-theory.md",
        "title": "最小会话类型理论",
        "group": "Struct",
        "color": "#4A90D9",
        "formality_level": "L5-L6",
        "category": "01-foundation",
        "word_count": 5974,
        "tags": ["Session Types", "π-calculus", "Linear Logic", "Choreographic Programming"],
        "related_nodes": ["Struct_01-foundation_01.07-session-types", "Struct_01-foundation_01.02-process-calculus-primer"]
    },
    {
        "path": "Struct/06-frontier/dbsp-theory-framework.md",
        "title": "DBSP (Database Stream Processor) 理论框架",
        "group": "Struct",
        "color": "#4A90D9",
        "formality_level": "L5-L6",
        "category": "06-frontier",
        "word_count": 5922,
        "tags": ["DBSP", "Z-sets", "Incremental View Maintenance", "Differential Dataflow"],
        "related_nodes": ["Struct_01-foundation_01.04-dataflow-model-formalization", "Knowledge_06-frontier_streaming-lakehouse-iceberg-delta"]
    },
    {
        "path": "Knowledge/06-frontier/cd-raft-cross-domain-consensus.md",
        "title": "CD-Raft: 跨域场景下的Raft共识优化",
        "group": "Knowledge",
        "color": "#5CB85C",
        "formality_level": "L4-L5",
        "category": "06-frontier",
        "word_count": 3763,
        "tags": ["Raft", "Consensus", "Cross-Domain", "WAN", "Distributed Consensus"],
        "related_nodes": []
    },
    {
        "path": "Struct/06-frontier/calvin-deterministic-streaming.md",
        "title": "Calvin 确定性执行模型与流处理状态管理",
        "group": "Struct",
        "color": "#4A90D9",
        "formality_level": "L5-L6",
        "category": "06-frontier",
        "word_count": 5328,
        "tags": ["Calvin", "Deterministic Execution", "State Management", "FaunaDB", "2PC"],
        "related_nodes": ["Struct_01-foundation_01.04-dataflow-model-formalization"]
    },
    {
        "path": "Flink/05-ecosystem/flink-dynamic-iceberg-sink-guide.md",
        "title": "Flink Dynamic Iceberg Sink 完整指南",
        "group": "Flink",
        "color": "#F0AD4E",
        "formality_level": "L3-L4",
        "category": "05-ecosystem",
        "word_count": 4614,
        "tags": ["Iceberg", "Schema Evolution", "Data Lake", "Streaming ETL", "Table API"],
        "related_nodes": ["Flink_14-lakehouse_flink-iceberg-integration", "Knowledge_06-frontier_streaming-lakehouse-iceberg-delta"]
    },
    {
        "path": "formal-methods/08-ai-formal-methods/agent-behavior-contract-verification.md",
        "title": "AI Agent 行为契约验证方法",
        "group": "FormalMethods",
        "color": "#8E44AD",
        "formality_level": "L5-L6",
        "category": "08-ai-formal-methods",
        "word_count": 6294,
        "tags": ["AI Agent", "Behavior Contract", "MCP", "A2A", "Runtime Verification", "TLA+"],
        "related_nodes": ["Knowledge_06-frontier_a2a-protocol-agent-communication", "Struct_06-frontier_06.03-ai-agent-session-types"]
    },
    {
        "path": "Struct/01-foundation/streaming-database-formal-definition.md",
        "title": "Streaming Database 形式化定义与理论体系",
        "group": "Struct",
        "color": "#4A90D9",
        "formality_level": "L5-L6",
        "category": "01-foundation",
        "word_count": 5141,
        "tags": ["Streaming Database", "Materialized View", "DBSP", "RisingWave", "Arroyo"],
        "related_nodes": ["Knowledge_06-frontier_streaming-databases", "Knowledge_04-technology-selection_streaming-database-guide"]
    },
    {
        "path": "Knowledge/06-frontier/nist-caisi-agent-standards.md",
        "title": "NIST CAISI 标准化政策解读",
        "group": "Knowledge",
        "color": "#5CB85C",
        "formality_level": "L3-L4",
        "category": "06-frontier",
        "word_count": 3103,
        "tags": ["NIST", "CAISI", "AI Agent Standards", "MCP", "A2A", "Compliance"],
        "related_nodes": ["Knowledge_06-frontier_a2a-protocol-agent-communication"]
    },
    {
        "path": "Flink/05-ecosystem/05.01-connectors/fluss-integration.md",
        "title": "Apache Fluss (Incubating) - 为流分析而生的分布式存储",
        "group": "Flink",
        "color": "#F0AD4E",
        "formality_level": "L3",
        "category": "05-ecosystem",
        "word_count": 2633,
        "tags": ["Fluss", "Connector", "Stream Storage", "Distributed Storage"],
        "related_nodes": ["Flink_04-connectors_fluss-integration"]
    },
    {
        "path": "Flink/05-ecosystem/05.02-lakehouse/flink-paimon-integration.md",
        "title": "Apache Paimon 与 Flink 深度集成 - 流批统一的湖仓存储",
        "group": "Flink",
        "color": "#F0AD4E",
        "formality_level": "L4-L5",
        "category": "05-ecosystem",
        "word_count": 7309,
        "tags": ["Paimon", "Lakehouse", "Stream-Batch Unification", "LSM", "Connector"],
        "related_nodes": ["Flink_04-connectors_flink-paimon-integration", "Flink_14-lakehouse_flink-paimon-integration"]
    },
]


def make_node_id(doc):
    """Generate node id from path"""
    p = doc["path"]
    # Remove .md
    p = p.replace(".md", "")
    # Replace / with _, and . with -
    p = p.replace("/", "_").replace(".", "-")
    # Prefix with group
    return doc["group"] + "_" + p.split("_", 1)[1] if "_" in p else doc["group"] + "_" + p


def update_graph_data():
    """Update .vscode/graph-data.json"""
    path = os.path.join(BASE_DIR, ".vscode", "graph-data.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Build existing id set and path map
    existing_ids = {n["id"] for n in data["nodes"]}
    existing_paths = {n.get("metadata", {}).get("path", ""): n["id"] for n in data["nodes"]}

    new_nodes = []
    new_edges = []

    for doc in NEW_DOCS:
        # Generate node id
        parts = doc["path"].replace(".md", "").split("/")
        # id format: Group_category_filename
        category_part = parts[1] if len(parts) > 1 else ""
        filename = parts[-1]
        # Clean dots in category/filename
        category_part = category_part.replace(".", "-")
        filename = filename.replace(".", "-")
        node_id = f"{doc['group']}_{category_part}_{filename}"

        if node_id in existing_ids:
            print(f"Skipping duplicate node: {node_id}")
            continue

        node = {
            "id": node_id,
            "label": doc["title"],
            "type": "document",
            "group": doc["group"],
            "size": round(doc["word_count"] / 1000, 3),
            "color": doc["color"],
            "metadata": {
                "path": doc["path"],
                "formality_level": doc["formality_level"],
                "category": doc["category"],
                "word_count": doc["word_count"]
            }
        }
        new_nodes.append(node)

        # Create edges to related nodes
        for related in doc["related_nodes"]:
            if related in existing_ids:
                edge = {
                    "source": node_id,
                    "target": related,
                    "type": "citation",
                    "weight": 1
                }
                new_edges.append(edge)

        # Also create edges from predecessors if they exist in the graph
        # (predecessors are listed in related_nodes for simplicity in this script)

    # Add nodes and edges
    data["nodes"].extend(new_nodes)
    data["edges"].extend(new_edges)

    # Update stats
    stats = data.get("stats", {})
    stats["total_nodes"] = len(data["nodes"])
    stats["total_edges"] = len(data["edges"])
    stats["documents"] = stats.get("documents", 0) + len(new_nodes)
    stats["generated_at"] = datetime.now().isoformat()
    data["stats"] = stats

    # Write back
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated .vscode/graph-data.json: +{len(new_nodes)} nodes, +{len(new_edges)} edges")
    return new_nodes


def update_streaming_theory_graph():
    """Update KNOWLEDGE-GRAPH/data/streaming-theory-graph.json"""
    path = os.path.join(BASE_DIR, "KNOWLEDGE-GRAPH", "data", "streaming-theory-graph.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {n["id"] for n in data["nodes"]}

    additions = [
        {"id": "dbsp", "label": "DBSP理论框架", "type": "theory", "category": "foundation", "level": 5, "description": "基于Z-set的增量视图维护理论"},
        {"id": "calvin", "label": "Calvin确定性执行", "type": "protocol", "category": "consistency", "level": 5, "description": "确定性分布式事务协议"},
        {"id": "minimal-session-types", "label": "最小会话类型", "type": "formalism", "category": "foundation", "level": 5, "description": "仅含输入输出终止三构造子的会话类型"},
        {"id": "streaming-database", "label": "流数据库", "type": "concept", "category": "data-management", "level": 4, "description": "以物化视图为一等公民的流处理系统"},
    ]

    new_edges = [
        {"source": "dbsp", "target": "incremental-computation", "type": "enables", "label": "支持"},
        {"source": "dbsp", "target": "materialized-view", "type": "enables", "label": "支持"},
        {"source": "calvin", "target": "determinism", "type": "guarantees", "label": "保证"},
        {"source": "calvin", "target": "consistency", "type": "implies", "label": "蕴含"},
        {"source": "minimal-session-types", "target": "pi-calculus", "type": "extends", "label": "扩展"},
        {"source": "streaming-database", "target": "dataflow-model", "type": "based-on", "label": "基于"},
    ]

    added = 0
    for node in additions:
        if node["id"] not in existing_ids:
            data["nodes"].append(node)
            added += 1

    data["edges"].extend(new_edges)
    data["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated streaming-theory-graph.json: +{added} nodes, +{len(new_edges)} edges")


def update_flink_technology_graph():
    """Update KNOWLEDGE-GRAPH/data/flink-technology-graph.json"""
    path = os.path.join(BASE_DIR, "KNOWLEDGE-GRAPH", "data", "flink-technology-graph.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {n["id"] for n in data["nodes"]}

    additions = [
        {"id": "dynamic-iceberg-sink", "label": "Dynamic Iceberg Sink", "type": "connector", "category": "connector", "level": 4, "description": "动态Schema演化的Iceberg输出"},
        {"id": "fluss-connector", "label": "Fluss Connector", "type": "connector", "category": "connector", "level": 4, "description": "Fluss流存储连接器"},
        {"id": "paimon-connector", "label": "Paimon Connector", "type": "connector", "category": "connector", "level": 5, "description": "Paimon湖仓存储连接器"},
    ]

    new_edges = [
        {"source": "dynamic-iceberg-sink", "target": "filesystem-connector", "type": "extends", "label": "扩展"},
        {"source": "fluss-connector", "target": "kafka-connector", "type": "alternative", "label": "替代"},
        {"source": "paimon-connector", "target": "filesystem-connector", "type": "extends", "label": "扩展"},
        {"source": "paimon-connector", "target": "incremental-cp", "type": "uses", "label": "使用"},
    ]

    added = 0
    for node in additions:
        if node["id"] not in existing_ids:
            data["nodes"].append(node)
            added += 1

    data["edges"].extend(new_edges)
    data["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated flink-technology-graph.json: +{added} nodes, +{len(new_edges)} edges")


def update_concept_dependency_graph():
    """Update KNOWLEDGE-GRAPH/data/concept-dependency-graph.json"""
    path = os.path.join(BASE_DIR, "KNOWLEDGE-GRAPH", "data", "concept-dependency-graph.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {n["id"] for n in data["nodes"]}

    additions = [
        {"id": "llm-formal-proof", "label": "LLM辅助形式化证明", "type": "concept", "layer": 4, "importance": 7},
        {"id": "veil-framework", "label": "Veil验证框架", "type": "tool", "layer": 4, "importance": 7},
        {"id": "agent-contract", "label": "Agent行为契约", "type": "concept", "layer": 4, "importance": 8},
        {"id": "nist-caisi", "label": "NIST CAISI标准", "type": "standard", "layer": 3, "importance": 7},
        {"id": "cd-raft", "label": "CD-Raft跨域共识", "type": "concept", "layer": 4, "importance": 8},
    ]

    new_edges = [
        {"source": "llm-formal-proof", "target": "temporal-logic", "type": "requires", "weight": 2},
        {"source": "veil-framework", "target": "distributed-systems", "type": "applies-to", "weight": 2},
        {"source": "agent-contract", "target": "consistency-model", "type": "requires", "weight": 2},
        {"source": "nist-caisi", "target": "distributed-systems", "type": "governs", "weight": 2},
        {"source": "cd-raft", "target": "consistency-model", "type": "requires", "weight": 3},
    ]

    added = 0
    for node in additions:
        if node["id"] not in existing_ids:
            data["nodes"].append(node)
            added += 1

    data["edges"].extend(new_edges)
    data["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated concept-dependency-graph.json: +{added} nodes, +{len(new_edges)} edges")


def update_learning_path_graph():
    """Update KNOWLEDGE-GRAPH/data/learning-path-graph.json"""
    path = os.path.join(BASE_DIR, "KNOWLEDGE-GRAPH", "data", "learning-path-graph.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {n["id"] for n in data["nodes"]}

    additions = [
        {"id": "llm-formal-methods-learning", "label": "LLM形式化方法", "type": "topic", "stage": 9, "category": "advanced", "duration": "3天"},
        {"id": "streaming-database-learning", "label": "流数据库理论", "type": "topic", "stage": 9, "category": "advanced", "duration": "3天"},
        {"id": "lakehouse-integration-learning", "label": "湖仓集成实践", "type": "topic", "stage": 9, "category": "advanced", "duration": "3天"},
    ]

    new_edges = [
        {"source": "formal-methods", "target": "llm-formal-methods-learning", "type": "includes", "label": "包含"},
        {"source": "advanced-topics", "target": "streaming-database-learning", "type": "includes", "label": "包含"},
        {"source": "advanced-topics", "target": "lakehouse-integration-learning", "type": "includes", "label": "包含"},
    ]

    added = 0
    for node in additions:
        if node["id"] not in existing_ids:
            data["nodes"].append(node)
            added += 1

    data["edges"].extend(new_edges)
    data["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated learning-path-graph.json: +{added} nodes, +{len(new_edges)} edges")


def update_design_patterns_graph():
    """Update KNOWLEDGE-GRAPH/data/design-patterns-graph.json"""
    path = os.path.join(BASE_DIR, "KNOWLEDGE-GRAPH", "data", "design-patterns-graph.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {n["id"] for n in data["nodes"]}

    additions = [
        {"id": "dynamic-routing-pattern", "label": "动态路由模式", "type": "pattern", "category": "integration", "level": 4, "description": "动态消息路由到目标系统"},
        {"id": "schema-evolution-pattern", "label": "Schema演进模式", "type": "pattern", "category": "data", "level": 4, "description": "运行时Schema变更兼容"},
    ]

    new_edges = [
        {"source": "dynamic-routing-pattern", "target": "message-router", "type": "extends", "label": "扩展"},
        {"source": "schema-evolution-pattern", "target": "schema-registry", "type": "requires", "label": "需要"},
    ]

    added = 0
    for node in additions:
        if node["id"] not in existing_ids:
            data["nodes"].append(node)
            added += 1

    data["edges"].extend(new_edges)
    data["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated design-patterns-graph.json: +{added} nodes, +{len(new_edges)} edges")


def update_search_index():
    """Update .vscode/search-index.json with new documents"""
    path = os.path.join(BASE_DIR, ".vscode", "search-index.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = data.get("documents", {})
    inverted = data.get("inverted_index", {})
    metadata = data.get("metadata", {})

    for doc in NEW_DOCS:
        if doc["path"] in docs:
            print(f"Skipping existing search index entry: {doc['path']}")
            continue

        # Build summary from first 200 chars of file
        full_path = os.path.join(BASE_DIR, doc["path"])
        summary = ""
        try:
            with open(full_path, "r", encoding="utf-8") as fdoc:
                content = fdoc.read()
                # Extract abstract/summary section
                abstract_match = content.find("## 摘要")
                if abstract_match >= 0:
                    end = content.find("##", abstract_match + 1)
                    if end < 0:
                        end = len(content)
                    summary = content[abstract_match:end].replace("## 摘要", "").strip()[:300]
                else:
                    summary = content[:300]
        except Exception as e:
            summary = doc["title"]

        doc_entry = {
            "path": doc["path"],
            "title": doc["title"],
            "summary": summary,
            "category": doc["group"],
            "subcategory": doc["category"],
            "keywords": doc["tags"],
            "formal_elements": [],
            "headings": [],
            "content_hash": "",
            "last_modified": datetime.now().isoformat(),
            "word_count": doc["word_count"],
            "line_count": 0
        }
        docs[doc["path"]] = doc_entry

        # Update inverted index with keywords
        for tag in doc["tags"]:
            tag_lower = tag.lower()
            if tag_lower not in inverted:
                inverted[tag_lower] = {
                    "keyword": tag_lower,
                    "doc_paths": [],
                    "formal_ids": [],
                    "tf_scores": {}
                }
            inv = inverted[tag_lower]
            if doc["path"] not in inv["doc_paths"]:
                inv["doc_paths"].append(doc["path"])
            inv["tf_scores"][doc["path"]] = 0.8

    # Update metadata
    metadata["total_documents"] = len(docs)
    metadata["total_index_entries"] = len(inverted)
    cat_dist = metadata.get("category_distribution", {})
    for doc in NEW_DOCS:
        g = doc["group"]
        cat_dist[g] = cat_dist.get(g, 0) + 1
    metadata["category_distribution"] = cat_dist

    data["metadata"] = metadata
    data["documents"] = docs
    data["inverted_index"] = inverted

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated .vscode/search-index.json: +{len(NEW_DOCS)} documents")


if __name__ == "__main__":
    print("Starting v4.3 knowledge graph update...")
    new_nodes = update_graph_data()
    update_streaming_theory_graph()
    update_flink_technology_graph()
    update_concept_dependency_graph()
    update_learning_path_graph()
    update_design_patterns_graph()
    update_search_index()
    print("Done!")
