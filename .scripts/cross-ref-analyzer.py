#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版文档交叉引用分析器
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# 主题关键词映射
TOPIC_KEYWORDS = {
    "checkpoint": ["checkpoint", "快照", "容错", "fault tolerance", "barrier"],
    "watermark": ["watermark", "水位线", "时间语义", "event time"],
    "state": ["state", "状态", "state backend", "rocksdb"],
    "sql": ["sql", "table api", "查询优化", "calcite"],
    "ai": ["ai", "ml", "机器学习", "llm", "agent"],
    "security": ["security", "安全", "加密", "认证"],
    "performance": ["performance", "性能", "优化", "benchmark"],
    "deployment": ["deployment", "部署", "kubernetes", "k8s"],
    "theory": ["形式化", "formal", "theorem", "证明", "语义"],
    "actor": ["actor", "actor model", "akka"],
    "csp": ["csp", "communicating sequential"],
    "dataflow": ["dataflow", "流图", "operator"],
}

def extract_refs(content, current_path):
    """提取文档中的引用链接"""
    refs = []
    md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    for text, link in md_links:
        if link.endswith('.md') and not link.startswith('http'):
            # 简化的路径解析
            if link.startswith('./'):
                current_dir = os.path.dirname(current_path)
                ref_path = os.path.normpath(os.path.join(current_dir, link[2:]))
            elif link.startswith('../'):
                current_dir = os.path.dirname(current_path)
                ref_path = os.path.normpath(os.path.join(current_dir, link))
            else:
                ref_path = link
            refs.append(ref_path.replace('\\', '/'))
    return refs

def detect_topics(content):
    """检测文档主题"""
    content_lower = content.lower()
    topics = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        matches = sum(1 for k in keywords if k.lower() in content_lower)
        if matches >= 2:
            topics.append((topic, matches))
    return sorted(topics, key=lambda x: x[1], reverse=True)[:3]

def main():
    root = Path(".")
    documents = {}
    ref_graph = defaultdict(set)
    reverse_graph = defaultdict(set)
    
    print("🔍 扫描文档...")
    
    # 扫描所有 md 文件
    for pattern in ["Struct/**/*.md", "Knowledge/**/*.md", "Flink/**/*.md"]:
        for md_file in root.glob(pattern):
            if md_file.name == "00-INDEX.md":
                continue
                
            rel_path = str(md_file.relative_to(root)).replace('\\', '/')
            try:
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                refs = extract_refs(content, rel_path)
                topics = detect_topics(content)
                
                # 提取标题
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else md_file.stem
                
                documents[rel_path] = {
                    'title': title[:80],
                    'refs': refs,
                    'topics': topics,
                    'size': len(content)
                }
                
                for ref in refs:
                    ref_graph[rel_path].add(ref)
                    reverse_graph[ref].add(rel_path)
            except Exception as e:
                print(f"  跳过 {rel_path}: {e}")
    
    print(f"✅ 扫描完成: {len(documents)} 篇文档")
    
    # 统计引用关系
    print("📊 分析引用关系...")
    for path in documents:
        documents[path]['outgoing'] = len(ref_graph[path])
        documents[path]['incoming'] = len(reverse_graph[path])
    
    # 找出孤立文档
    isolated = [(p, d) for p, d in documents.items() 
                if d.get('outgoing', 0) + d.get('incoming', 0) < 2]
    isolated.sort(key=lambda x: x[1].get('outgoing', 0) + x[1].get('incoming', 0))
    
    # 找出热点文档
    hub_scores = [(p, d, d.get('outgoing', 0) + d.get('incoming', 0) * 2) 
                  for p, d in documents.items()]
    hub_scores.sort(key=lambda x: x[2], reverse=True)
    
    # 生成目录映射推荐
    print("🗺️ 生成映射推荐...")
    recommendations = []
    
    # Struct -> Knowledge
    struct_docs = [(p, d) for p, d in documents.items() if p.startswith('Struct/')]
    knowledge_docs = [(p, d) for p, d in documents.items() if p.startswith('Knowledge/')]
    flink_docs = [(p, d) for p, d in documents.items() if p.startswith('Flink/')]
    
    for s_path, s_doc in struct_docs[:30]:
        for k_path, k_doc in knowledge_docs:
            # 主题匹配
            s_topics = set(t[0] for t in s_doc.get('topics', []))
            k_topics = set(t[0] for t in k_doc.get('topics', []))
            common = s_topics & k_topics
            if common:
                score = len(common) / max(len(s_topics), len(k_topics), 1)
                if score > 0.3:
                    recommendations.append({
                        'source': s_path,
                        'target': k_path,
                        'score': round(score, 3),
                        'reason': f"共同主题: {', '.join(common)}",
                        'type': 'Struct->Knowledge'
                    })
    
    for k_path, k_doc in knowledge_docs[:30]:
        for f_path, f_doc in flink_docs:
            k_topics = set(t[0] for t in k_doc.get('topics', []))
            f_topics = set(t[0] for t in f_doc.get('topics', []))
            common = k_topics & f_topics
            if common:
                score = len(common) / max(len(k_topics), len(f_topics), 1)
                if score > 0.4:
                    recommendations.append({
                        'source': k_path,
                        'target': f_path,
                        'score': round(score, 3),
                        'reason': f"共同主题: {', '.join(common)}",
                        'type': 'Knowledge->Flink'
                    })
    
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    # 生成报告
    report = {
        'generated_at': datetime.now().isoformat(),
        'summary': {
            'total_documents': len(documents),
            'total_references': sum(len(ref_graph[p]) for p in ref_graph),
            'isolated_documents': len(isolated),
            'recommendations': len(recommendations)
        },
        'isolated_documents': [
            {'path': p, 'title': d['title'], 'outgoing': d.get('outgoing', 0), 'incoming': d.get('incoming', 0)}
            for p, d in isolated[:25]
        ],
        'hub_documents': [
            {'path': p, 'title': d['title'], 'score': score, 'outgoing': d.get('outgoing', 0), 'incoming': d.get('incoming', 0)}
            for p, d, score in hub_scores[:25]
        ],
        'recommendations': recommendations[:50]
    }
    
    # 保存 JSON 报告
    with open('cross-ref-analysis-report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 生成 Markdown 报告
    md_lines = [
        "# 文档交叉引用分析报告",
        "",
        f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 📊 统计概览",
        "",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 文档总数 | {report['summary']['total_documents']} |",
        f"| 引用总数 | {report['summary']['total_references']} |",
        f"| 孤立文档数 | {report['summary']['isolated_documents']} |",
        f"| 推荐映射数 | {report['summary']['recommendations']} |",
        "",
        "## 📉 孤立文档（引用数<2）",
        "",
        "| 文档路径 | 标题 | 出链 | 入链 | 总计 |",
        "|----------|------|------|------|------|"
    ]
    
    for item in report['isolated_documents'][:20]:
        total = item['outgoing'] + item['incoming']
        md_lines.append(f"| {item['path']} | {item['title'][:50]} | {item['outgoing']} | {item['incoming']} | {total} |")
    
    md_lines.extend([
        "",
        "## 🔥 热点文档（Top 20）",
        "",
        "| 排名 | 文档路径 | 标题 | 总分 | 出链 | 入链 |",
        "|------|----------|------|------|------|------|"
    ])
    
    for i, item in enumerate(report['hub_documents'][:20], 1):
        md_lines.append(f"| {i} | {item['path']} | {item['title'][:40]} | {item['score']} | {item['outgoing']} | {item['incoming']} |")
    
    md_lines.extend([
        "",
        "## 🗺️ 目录间映射推荐（Top 25）",
        "",
        "| 类型 | 源文档 | 目标文档 | 分数 | 原因 |",
        "|------|--------|----------|------|------|"
    ])
    
    for item in report['recommendations'][:25]:
        md_lines.append(f"| {item['type']} | {item['source']} | {item['target']} | {item['score']} | {item['reason']} |")
    
    md_lines.append("")
    
    with open('cross-ref-analysis-report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
    
    print("\n✅ 报告生成完成!")
    print(f"  - JSON: cross-ref-analysis-report.json")
    print(f"  - Markdown: cross-ref-analysis-report.md")
    print(f"\n统计:")
    print(f"  - 孤立文档: {len(isolated)} 篇")
    print(f"  - 热点文档: {len(hub_scores)} 篇")
    print(f"  - 推荐映射: {len(recommendations)} 条")

if __name__ == "__main__":
    main()
