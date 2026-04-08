#!/usr/bin/env python3
"""
知识图谱 v2.0 搜索索引生成器
生成Lunr.js兼容的搜索索引
"""

import json
import re
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "knowledge-graph-site" / "data"
REGISTRY_FILE = PROJECT_ROOT / "THEOREM-REGISTRY.md"

def extract_searchable_content():
    """从定理注册表和其他文档提取可搜索内容"""
    documents = []
    
    if REGISTRY_FILE.exists():
        content = REGISTRY_FILE.read_text(encoding='utf-8')
        
        # 提取标题作为文档
        headers = re.findall(r'^##+\s+(.+)$', content, re.MULTILINE)
        for i, header in enumerate(headers):
            doc = {
                "id": f"header_{i}",
                "title": header.strip(),
                "content": header.strip(),
                "category": "section",
                "url": f"#section-{i}"
            }
            documents.append(doc)
        
        # 提取定理/定义引用
        theorem_refs = re.findall(r'(Thm-[SKF]-\d{2}-\d{2,3})', content)
        definition_refs = re.findall(r'(Def-[SKF]-\d{2}-\d{2,3})', content)
        lemma_refs = re.findall(r'(Lemma-[SKF]-\d{2}-\d{2,3})', content)
        
        for i, ref in enumerate(set(theorem_refs + definition_refs + lemma_refs)):
            doc = {
                "id": f"ref_{i}",
                "title": ref,
                "content": f"形式化元素: {ref}",
                "category": "reference",
                "url": f"#{ref.lower()}"
            }
            documents.append(doc)
    
    # 添加预设搜索文档
    preset_docs = [
        {
            "id": "intro",
            "title": "知识图谱介绍",
            "content": "AnalysisDataFlow 知识图谱是一个交互式可视化工具，用于探索流计算理论、Flink实践和业务建模之间的关系。",
            "category": "guide",
            "url": "#intro"
        },
        {
            "id": "struct",
            "title": "Struct 形式理论",
            "content": "包含流计算的形式化定义、定理、证明和严格分析。涵盖进程演算、Dataflow模型、一致性理论等。",
            "category": "category",
            "url": "#struct"
        },
        {
            "id": "knowledge",
            "title": "Knowledge 知识结构",
            "content": "设计模式、业务建模、最佳实践和架构指南。帮助工程师将理论应用到实际项目中。",
            "category": "category",
            "url": "#knowledge"
        },
        {
            "id": "flink",
            "title": "Flink 专项",
            "content": "Apache Flink的架构、机制、API、部署和优化。包含核心机制、SQL/Table API、连接器等内容。",
            "category": "category",
            "url": "#flink"
        },
        {
            "id": "search_help",
            "title": "搜索帮助",
            "content": "使用搜索功能查找定理、定义、概念和文档。支持按类别过滤和语义搜索。",
            "category": "help",
            "url": "#search-help"
        },
        {
            "id": "checkpoint",
            "title": "Flink Checkpoint机制",
            "content": "Checkpoint是Flink的分布式快照机制，用于实现 exactly-once 语义和容错恢复。",
            "category": "concept",
            "url": "#checkpoint"
        },
        {
            "id": "watermark",
            "title": "Watermark水位线",
            "content": "Watermark是Flink处理乱序事件时间的关键机制，用于触发窗口计算和处理延迟数据。",
            "category": "concept",
            "url": "#watermark"
        },
        {
            "id": "backpressure",
            "title": "Backpressure背压",
            "content": "Backpressure是流处理系统的一种自我保护机制，当下游处理速度低于上游时自动降速。",
            "category": "concept",
            "url": "#backpressure"
        }
    ]
    
    documents.extend(preset_docs)
    
    return documents

def generate_lunr_index():
    """生成Lunr.js搜索索引"""
    documents = extract_searchable_content()
    
    # 构建索引结构
    index_data = {
        "version": "2.3.9",
        "fields": ["title", "content", "category"],
        "documents": documents,
        "index": {
            "version": "2.3.9",
            "fields": ["title", "content"],
            "ref": "id",
            "documentStore": {},
            "tokenStore": {},
            "corpusTokens": []
        }
    }
    
    # 简单倒排索引实现
    token_map = {}
    
    for doc in documents:
        # 提取所有词元
        text = f"{doc['title']} {doc['content']}".lower()
        tokens = re.findall(r'\b[\w\u4e00-\u9fff]+\b', text)
        
        for token in tokens:
            if len(token) > 1:
                if token not in token_map:
                    token_map[token] = []
                if doc["id"] not in token_map[token]:
                    token_map[token].append(doc["id"])
    
    index_data["index"]["tokenStore"] = token_map
    index_data["index"]["corpusTokens"] = list(token_map.keys())
    index_data["index"]["documentStore"] = {doc["id"]: doc for doc in documents}
    
    return index_data

def generate_suggestions():
    """生成搜索建议"""
    suggestions = [
        "Checkpoint机制",
        "Watermark水位线",
        "Backpressure背压",
        "Exactly-Once语义",
        "Dataflow模型",
        "Actor模型",
        "进程演算",
        "状态后端",
        "窗口计算",
        "时间语义",
        "Thm-S-01-01",
        "Def-K-02-01",
        "Flink SQL",
        "Table API"
    ]
    return suggestions

def main():
    """主函数"""
    print("🔍 开始生成搜索索引...")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 生成Lunr索引
    index_data = generate_lunr_index()
    index_file = OUTPUT_DIR / "search-index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    print(f"✅ 搜索索引已生成: {index_file}")
    
    # 生成搜索建议
    suggestions = generate_suggestions()
    suggestions_file = OUTPUT_DIR / "search-suggestions.json"
    with open(suggestions_file, 'w', encoding='utf-8') as f:
        json.dump(suggestions, f, ensure_ascii=False, indent=2)
    print(f"✅ 搜索建议已生成: {suggestions_file}")
    
    print(f"📊 索引文档数: {len(index_data['documents'])}")
    print(f"📊 词元数: {len(index_data['index']['corpusTokens'])}")
    
    print("\n🎉 搜索索引生成完成!")

if __name__ == "__main__":
    main()
