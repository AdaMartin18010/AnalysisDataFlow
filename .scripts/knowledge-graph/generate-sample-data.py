#!/usr/bin/env python3
"""
示例数据生成器
=============
生成示例知识图谱数据，用于测试和演示。
"""

import json
import random
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_concept_graph():
    """生成示例概念图谱"""
    concepts = {
        "Thm-S-01-01": {
            "name": "流计算基本定理",
            "category": "theorem",
            "source_file": "Struct/1.1-streaming-foundations.md",
            "definition": "流计算系统的基本理论性质...",
            "dependencies": ["Def-S-01-01", "Def-S-01-02"],
            "pagerank": 0.85,
            "in_degree": 2,
            "out_degree": 5
        },
        "Def-S-01-01": {
            "name": "Event Time定义",
            "category": "definition",
            "source_file": "Struct/1.1-streaming-foundations.md",
            "definition": "事件时间是指事件实际发生的时间...",
            "dependencies": [],
            "pagerank": 0.92,
            "in_degree": 0,
            "out_degree": 8
        },
        "Def-S-01-02": {
            "name": "Processing Time定义",
            "category": "definition",
            "source_file": "Struct/1.1-streaming-foundations.md",
            "definition": "处理时间是指事件被处理的时间...",
            "dependencies": [],
            "pagerank": 0.78,
            "in_degree": 0,
            "out_degree": 3
        },
        "Lemma-S-02-01": {
            "name": "Watermark单调性引理",
            "category": "lemma",
            "source_file": "Struct/1.2-watermark-theory.md",
            "definition": "Watermark在时间维度上是非递减的...",
            "dependencies": ["Def-S-01-01", "Thm-S-01-01"],
            "pagerank": 0.65,
            "in_degree": 2,
            "out_degree": 2
        },
        "Thm-S-02-01": {
            "name": "Exactly-Once定理",
            "category": "theorem",
            "source_file": "Struct/2.1-consistency-models.md",
            "definition": "在分布式流处理中实现exactly-once语义的充要条件...",
            "dependencies": ["Thm-S-01-01", "Lemma-S-02-01"],
            "pagerank": 0.88,
            "in_degree": 2,
            "out_degree": 6
        }
    }
    
    relations = [
        {"source": "Thm-S-01-01", "target": "Def-S-01-01", "type": "depends_on", "weight": 1.0},
        {"source": "Thm-S-01-01", "target": "Def-S-01-02", "type": "depends_on", "weight": 1.0},
        {"source": "Lemma-S-02-01", "target": "Def-S-01-01", "type": "depends_on", "weight": 1.0},
        {"source": "Lemma-S-02-01", "target": "Thm-S-01-01", "type": "depends_on", "weight": 0.8},
        {"source": "Thm-S-02-01", "target": "Thm-S-01-01", "type": "depends_on", "weight": 1.0},
        {"source": "Thm-S-02-01", "target": "Lemma-S-02-01", "type": "depends_on", "weight": 0.9}
    ]
    
    summary = {
        "generated_at": datetime.now().isoformat(),
        "statistics": {
            "total_concepts": len(concepts),
            "total_relations": len(relations),
            "by_category": {
                "theorem": 2,
                "definition": 2,
                "lemma": 1
            }
        },
        "concepts": concepts,
        "relations": relations
    }
    
    with open(OUTPUT_DIR / "concept-summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 生成概念图谱: {len(concepts)} 个概念, {len(relations)} 个关系")
    return summary


def generate_cypher_script():
    """生成示例Cypher脚本"""
    cypher = """// 概念图谱Cypher导入脚本
// 生成时间: {timestamp}

CREATE CONSTRAINT concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE;

CREATE (c_Def_S_01_01:Concept {{
    id: "Def-S-01-01",
    name: "Event Time定义",
    category: "definition",
    source_file: "Struct/1.1-streaming-foundations.md",
    definition: "事件时间是指事件实际发生的时间..."
}});

CREATE (c_Def_S_01_02:Concept {{
    id: "Def-S-01-02",
    name: "Processing Time定义",
    category: "definition",
    source_file: "Struct/1.1-streaming-foundations.md",
    definition: "处理时间是指事件被处理的时间..."
}});

CREATE (c_Thm_S_01_01:Concept {{
    id: "Thm-S-01-01",
    name: "流计算基本定理",
    category: "theorem",
    source_file: "Struct/1.1-streaming-foundations.md",
    definition: "流计算系统的基本理论性质..."
}});

CREATE (c_Def_S_01_01)-[:REFERENCES {{weight: 1.0}}]->(c_Thm_S_01_01);
CREATE (c_Def_S_01_02)-[:REFERENCES {{weight: 1.0}}]->(c_Thm_S_01_01);

CREATE INDEX concept_category IF NOT EXISTS FOR (c:Concept) ON (c.category);
""".format(timestamp=datetime.now().isoformat())
    
    with open(OUTPUT_DIR / "graph-data.cypher", "w", encoding="utf-8") as f:
        f.write(cypher)
    
    print("✓ 生成Cypher脚本")


def generate_theorem_dependencies():
    """生成示例定理依赖数据"""
    data = {
        "generated_at": datetime.now().isoformat(),
        "statistics": {
            "total_theorems": 15,
            "total_dependencies": 28,
            "by_type": {
                "theorem": 8,
                "lemma": 4,
                "proposition": 2,
                "definition": 10
            }
        },
        "theorems": {
            "Thm-S-01-01": {
                "id": "Thm-S-01-01",
                "formal_id": "Thm-S-01-01",
                "name": "流计算基本定理",
                "theorem_type": "theorem",
                "source_file": "Struct/1.1-streaming-foundations.md",
                "statement": "对于任何流计算系统...",
                "dependencies": ["Def-S-01-01", "Def-S-01-02"],
                "used_by": ["Thm-S-02-01", "Lemma-S-02-01"],
                "proof_depth": 1,
                "complexity_score": 8.5
            },
            "Def-S-01-01": {
                "id": "Def-S-01-01",
                "formal_id": "Def-S-01-01",
                "name": "Event Time定义",
                "theorem_type": "definition",
                "source_file": "Struct/1.1-streaming-foundations.md",
                "statement": "事件时间是指...",
                "dependencies": [],
                "used_by": ["Thm-S-01-01", "Lemma-S-02-01"],
                "proof_depth": 0,
                "complexity_score": 3.0
            }
        },
        "edges": [
            {"source": "Thm-S-01-01", "target": "Def-S-01-01", "type": "direct"},
            {"source": "Thm-S-01-01", "target": "Def-S-01-02", "type": "direct"}
        ],
        "cycles": [],
        "foundations": ["Def-S-01-01", "Def-S-01-02", "Def-S-02-01"],
        "critical_paths": {
            "Thm-S-02-01": ["Def-S-01-01", "Thm-S-01-01", "Lemma-S-02-01", "Thm-S-02-01"]
        }
    }
    
    with open(OUTPUT_DIR / "theorem-dependencies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 生成关键路径报告
    report = """======================================================================
定理依赖关系关键路径分析报告
生成时间: {timestamp}
======================================================================

【基础定理】共 3 个（不依赖其他定理）
----------------------------------------------------------------------
  • Def-S-01-01: Event Time定义
  • Def-S-01-02: Processing Time定义
  • Def-S-02-01: Watermark定义

【最重要定理】（被引用次数最多）
----------------------------------------------------------------------
  1. Def-S-01-01: 被引用 8 次
     Event Time定义
  2. Thm-S-01-01: 被引用 5 次
     流计算基本定理
  3. Def-S-01-02: 被引用 3 次
     Processing Time定义

【证明深度最大】（依赖链最长）
----------------------------------------------------------------------
  1. Thm-S-05-01: 深度 5
  2. Thm-S-04-01: 深度 4
  3. Thm-S-03-01: 深度 3

【关键路径示例】（证明某定理所需的最少依赖链）
----------------------------------------------------------------------

  证明 Thm-S-02-01 的关键路径:
    └─> Def-S-01-01
      └─> Thm-S-01-01
        └─> Lemma-S-02-01
          └─> Thm-S-02-01

【✅ 循环依赖检查】
----------------------------------------------------------------------
  未发现循环依赖

======================================================================
报告结束
======================================================================
""".format(timestamp=datetime.now().isoformat())
    
    with open(OUTPUT_DIR / "critical-path.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"✓ 生成定理依赖数据: {data['statistics']['total_theorems']} 个定理")


def generate_similarity_matrix():
    """生成示例相似度矩阵"""
    documents = [
        "Struct/1.1-streaming-foundations.md",
        "Struct/1.2-watermark-theory.md",
        "Struct/2.1-consistency-models.md",
        "Knowledge/flink-checkpoint-guide.md",
        "Knowledge/kafka-streams-comparison.md",
        "Flink/checkpoint-configuration.md"
    ]
    
    # 生成稀疏相似度矩阵
    matrix_data = {
        "documents": documents,
        "matrix": [],
        "shape": [len(documents), len(documents)]
    }
    
    # 添加一些相似度值
    similarities = [
        {"i": 0, "j": 2, "sim": 0.75},
        {"i": 0, "j": 3, "sim": 0.68},
        {"i": 1, "j": 2, "sim": 0.82},
        {"i": 3, "j": 5, "sim": 0.91},  # 高相似度 - checkpoint相关
        {"i": 2, "j": 3, "sim": 0.65}
    ]
    
    matrix_data["matrix"] = similarities
    
    with open(OUTPUT_DIR / "similarity-matrix.json", "w", encoding="utf-8") as f:
        json.dump(matrix_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 生成相似度矩阵: {len(documents)} 个文档")


def generate_clusters():
    """生成示例聚类结果"""
    clusters = {
        "generated_at": datetime.now().isoformat(),
        "total_clusters": 4,
        "clusters": {
            "0": {
                "documents": [
                    "Struct/1.1-streaming-foundations.md",
                    "Struct/1.2-watermark-theory.md"
                ],
                "size": 2,
                "keywords": ["streaming", "event time", "watermark"],
                "sample_titles": ["流计算基础理论", "Watermark理论"]
            },
            "1": {
                "documents": [
                    "Flink/checkpoint-configuration.md",
                    "Knowledge/flink-checkpoint-guide.md"
                ],
                "size": 2,
                "keywords": ["flink", "checkpoint", "fault tolerance"],
                "sample_titles": ["Flink Checkpoint配置", "Checkpoint指南"]
            },
            "2": {
                "documents": [
                    "Knowledge/kafka-streams-comparison.md"
                ],
                "size": 1,
                "keywords": ["kafka", "comparison", "streams"],
                "sample_titles": ["Kafka Streams对比分析"]
            },
            "3": {
                "documents": [
                    "Struct/2.1-consistency-models.md"
                ],
                "size": 1,
                "keywords": ["consistency", "exactly-once", "models"],
                "sample_titles": ["一致性模型"]
            }
        }
    }
    
    with open(OUTPUT_DIR / "doc-clusters.json", "w", encoding="utf-8") as f:
        json.dump(clusters, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 生成聚类结果: {clusters['total_clusters']} 个聚类")


def generate_content_gaps():
    """生成示例内容缺口分析"""
    gaps = {
        "generated_at": datetime.now().isoformat(),
        "coverage": {
            "理论基础": {
                "document_count": 5,
                "coverage_ratio": 0.83,
                "top_documents": ["Struct/1.1-streaming-foundations.md"],
                "keywords_matched": True
            },
            "Flink技术": {
                "document_count": 3,
                "coverage_ratio": 0.50,
                "top_documents": ["Flink/checkpoint-configuration.md"],
                "keywords_matched": True
            },
            "生产实践": {
                "document_count": 0,
                "coverage_ratio": 0.0,
                "top_documents": [],
                "keywords_matched": False
            }
        },
        "gaps": [
            {
                "topic": "生产实践",
                "current_documents": 0,
                "suggested_action": "建议增加相关文档",
                "priority": "high"
            },
            {
                "topic": "性能优化",
                "current_documents": 1,
                "suggested_action": "建议增加相关文档",
                "priority": "medium"
            }
        ]
    }
    
    with open(OUTPUT_DIR / "content-gaps.json", "w", encoding="utf-8") as f:
        json.dump(gaps, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 生成内容缺口分析: {len(gaps['gaps'])} 个缺口")


def generate_search_index():
    """生成示例搜索索引"""
    index_data = {
        "documents": {
            "Struct/1.1-streaming-foundations.md": {
                "doc_id": "Struct/1.1-streaming-foundations.md",
                "title": "流计算基础理论",
                "word_count": 2500,
                "section_count": 8,
                "doc_type": "formal_theory",
                "formal_ids": "Def-S-01-01,Def-S-01-02,Thm-S-01-01"
            },
            "Flink/checkpoint-configuration.md": {
                "doc_id": "Flink/checkpoint-configuration.md",
                "title": "Flink Checkpoint配置指南",
                "word_count": 1800,
                "section_count": 6,
                "doc_type": "flink_reference",
                "formal_ids": ""
            }
        },
        "inverted_index": {
            "checkpoint": ["Flink/checkpoint-configuration.md"],
            "streaming": ["Struct/1.1-streaming-foundations.md"],
            "event": ["Struct/1.1-streaming-foundations.md"],
            "time": ["Struct/1.1-streaming-foundations.md"],
            "flink": ["Flink/checkpoint-configuration.md"]
        },
        "saved_at": datetime.now().isoformat()
    }
    
    # 创建index目录
    index_dir = Path("index")
    index_dir.mkdir(exist_ok=True)
    
    with open(index_dir / "search-index.json", "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 生成搜索索引: {len(index_data['documents'])} 个文档")


def main():
    """生成所有示例数据"""
    print("=" * 60)
    print("知识图谱示例数据生成器")
    print("=" * 60)
    print()
    
    generate_concept_graph()
    generate_cypher_script()
    generate_theorem_dependencies()
    generate_similarity_matrix()
    generate_clusters()
    generate_content_gaps()
    generate_search_index()
    
    print()
    print("=" * 60)
    print("示例数据生成完成!")
    print(f"输出目录: {OUTPUT_DIR.absolute()}")
    print("=" * 60)
    print()
    print("生成的文件:")
    for file in sorted(OUTPUT_DIR.iterdir()):
        if file.is_file():
            print(f"  - {file.name}")
    for file in sorted(Path("index").iterdir()):
        if file.is_file():
            print(f"  - index/{file.name}")


if __name__ == "__main__":
    main()
