#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档交叉引用智能推荐系统
功能：
1. 分析文档之间的引用关系
2. 识别孤立文档和引用密集文档
3. 基于内容相似度推荐引用
4. 基于主题相关性推荐引用
5. 生成推荐报告
"""

import os
import re
import json
import hashlib
from pathlib import Path
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from difflib import SequenceMatcher


@dataclass
class Document:
    """文档元数据"""
    path: str
    content: str = ""
    title: str = ""
    headings: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    outgoing_refs: List[str] = field(default_factory=list)
    incoming_refs: List[str] = field(default_factory=list)
    section: str = ""
    word_count: int = 0
    
    @property
    def filename(self) -> str:
        return os.path.basename(self.path)
    
    @property
    def dir_name(self) -> str:
        return os.path.dirname(self.path).split(os.sep)[0] if os.sep in self.path else ""


@dataclass
class ReferenceRecommendation:
    """引用推荐项"""
    source: str
    target: str
    score: float
    reason: str
    confidence: str  # high, medium, low


class CrossRefRecommender:
    """交叉引用推荐器"""
    
    # 主题关键词映射
    TOPIC_KEYWORDS = {
        "checkpoint": ["checkpoint", "快照", "容错", "fault tolerance", "barrier", "对齐"],
        "watermark": ["watermark", "水位线", "时间语义", "event time", "处理时间"],
        "state": ["state", "状态", "state backend", "rocksdb", "状态管理"],
        "sql": ["sql", "table api", "查询优化", "calcite", "物化视图"],
        "ai": ["ai", "ml", "机器学习", "llm", "agent", "向量搜索", "rag"],
        "security": ["security", "安全", "加密", "认证", "授权", "audit"],
        "performance": ["performance", "性能", "优化", "调优", "benchmark"],
        "deployment": ["deployment", "部署", "kubernetes", "k8s", "operator"],
        "theory": ["形式化", "formal", "theorem", "证明", "语义", "calculus"],
        "actor": ["actor", "actor model", "akka", "pekko", "actor 模型"],
        "csp": ["csp", "communicating sequential", "通道", "channel"],
        "dataflow": ["dataflow", "流图", "operator", "算子"],
    }
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.documents: Dict[str, Document] = {}
        self.ref_graph: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_graph: Dict[str, Set[str]] = defaultdict(set)
        
    def scan_documents(self) -> None:
        """扫描所有 Markdown 文档"""
        print("🔍 扫描文档中...")
        
        for pattern in ["Struct/**/*.md", "Knowledge/**/*.md", "Flink/**/*.md"]:
            for md_file in self.root_dir.glob(pattern):
                # 跳过索引文件本身
                if md_file.name == "00-INDEX.md":
                    continue
                    
                rel_path = str(md_file.relative_to(self.root_dir))
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                
                doc = self._parse_document(rel_path, content)
                self.documents[rel_path] = doc
                
        print(f"✅ 扫描完成: {len(self.documents)} 篇文档")
        
    def _parse_document(self, path: str, content: str) -> Document:
        """解析文档内容"""
        # 提取标题
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else path
        
        # 提取所有标题
        headings = re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE)
        
        # 提取关键词（从标题和概念定义部分）
        keywords = self._extract_keywords(content)
        
        # 提取引用链接
        outgoing_refs = self._extract_refs(content, path)
        
        # 确定所属章节
        section = path.split(os.sep)[0] if os.sep in path else "other"
        
        # 字数统计
        word_count = len(content.split())
        
        return Document(
            path=path,
            content=content[:5000],  # 只存储前5000字符用于分析
            title=title,
            headings=headings[:10],  # 只取前10个标题
            keywords=keywords,
            outgoing_refs=outgoing_refs,
            section=section,
            word_count=word_count
        )
    
    def _extract_keywords(self, content: str) -> List[str]:
        """提取关键词"""
        keywords = []
        
        # 从概念定义部分提取
        concept_matches = re.findall(r'[\*\-]\s*\*\*(.+?)\*\*[:：]', content)
        keywords.extend(concept_matches)
        
        # 从定理/定义编号提取
        theorem_matches = re.findall(r'(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d+-\d+', content)
        keywords.extend(theorem_matches)
        
        # 从代码块标签提取
        code_tags = re.findall(r'```(\w+)', content)
        keywords.extend(code_tags)
        
        # 从加粗文本提取
        bold_texts = re.findall(r'\*\*([^*]+)\*\*', content)
        keywords.extend([t for t in bold_texts if len(t) < 50])
        
        return list(set(keywords))[:30]  # 去重并限制数量
    
    def _extract_refs(self, content: str, current_path: str) -> List[str]:
        """提取文档中的引用链接"""
        refs = []
        
        # 匹配 Markdown 链接
        md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        
        for text, link in md_links:
            # 只处理相对路径的 md 文件
            if link.endswith('.md') and not link.startswith('http'):
                # 解析相对路径
                ref_path = self._resolve_ref_path(current_path, link)
                if ref_path and ref_path in self.documents:
                    refs.append(ref_path)
                    
        return refs
    
    def _resolve_ref_path(self, current_path: str, link: str) -> Optional[str]:
        """解析相对链接为绝对路径"""
        current_dir = os.path.dirname(current_path)
        
        if link.startswith('./'):
            ref_path = os.path.normpath(os.path.join(current_dir, link[2:]))
        elif link.startswith('../'):
            ref_path = os.path.normpath(os.path.join(current_dir, link))
        elif link.startswith('/'):
            ref_path = link[1:]
        else:
            ref_path = os.path.normpath(os.path.join(current_dir, link))
            
        # 统一路径分隔符
        ref_path = ref_path.replace('\\', '/')
        return ref_path
    
    def build_reference_graph(self) -> None:
        """构建引用关系图"""
        print("🔗 构建引用关系图...")
        
        for path, doc in self.documents.items():
            for ref in doc.outgoing_refs:
                self.ref_graph[path].add(ref)
                self.reverse_graph[ref].add(path)
                
        print(f"✅ 引用关系图构建完成: {len(self.ref_graph)} 个节点")
        
    def find_isolated_documents(self, threshold: int = 2) -> List[Document]:
        """查找孤立文档（引用数少于阈值）"""
        isolated = []
        
        for path, doc in self.documents.items():
            out_count = len(doc.outgoing_refs)
            in_count = len(self.reverse_graph.get(path, set()))
            total = out_count + in_count
            
            if total < threshold:
                isolated.append((doc, out_count, in_count))
                
        return sorted(isolated, key=lambda x: x[1] + x[2])
    
    def find_hub_documents(self, top_n: int = 20) -> List[Tuple[Document, int]]:
        """查找引用密集的热点文档"""
        hub_scores = []
        
        for path, doc in self.documents.items():
            out_count = len(doc.outgoing_refs)
            in_count = len(self.reverse_graph.get(path, set()))
            score = out_count + in_count * 2  # 被引用权重更高
            
            hub_scores.append((doc, score, out_count, in_count))
            
        return sorted(hub_scores, key=lambda x: x[1], reverse=True)[:top_n]
    
    def calculate_content_similarity(self, doc1: Document, doc2: Document) -> float:
        """计算两篇文档的内容相似度"""
        # 基于标题和关键词的 Jaccard 相似度
        set1 = set(doc1.keywords + doc1.headings[:5])
        set2 = set(doc2.keywords + doc2.headings[:5])
        
        if not set1 or not set2:
            return 0.0
            
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    def calculate_topic_similarity(self, doc1: Document, doc2: Document) -> Tuple[float, str]:
        """计算主题相似度并返回主题标签"""
        content1 = doc1.content.lower()
        content2 = doc2.content.lower()
        
        best_score = 0.0
        best_topic = ""
        
        for topic, keywords in self.TOPIC_KEYWORDS.items():
            matches1 = sum(1 for k in keywords if k.lower() in content1)
            matches2 = sum(1 for k in keywords if k.lower() in content2)
            
            if matches1 > 0 and matches2 > 0:
                # 两篇文档都包含该主题关键词
                score = min(matches1, matches2) / max(matches1, matches2) if max(matches1, matches2) > 0 else 0
                if score > best_score:
                    best_score = score
                    best_topic = topic
                    
        return best_score, best_topic
    
    def recommend_cross_refs(self, source_path: str, top_n: int = 10) -> List[ReferenceRecommendation]:
        """为指定文档推荐交叉引用"""
        if source_path not in self.documents:
            return []
            
        source = self.documents[source_path]
        existing_refs = set(source.outgoing_refs)
        recommendations = []
        
        for target_path, target in self.documents.items():
            if target_path == source_path or target_path in existing_refs:
                continue
                
            # 计算相似度
            content_sim = self.calculate_content_similarity(source, target)
            topic_sim, topic = self.calculate_topic_similarity(source, target)
            
            # 综合评分
            score = content_sim * 0.4 + topic_sim * 0.6
            
            if score > 0.1:  # 阈值过滤
                if score > 0.5:
                    confidence = "high"
                elif score > 0.3:
                    confidence = "medium"
                else:
                    confidence = "low"
                    
                reason = f"主题'{topic}'相关" if topic else "内容相似"
                recommendations.append(ReferenceRecommendation(
                    source=source_path,
                    target=target_path,
                    score=score,
                    reason=reason,
                    confidence=confidence
                ))
                
        return sorted(recommendations, key=lambda x: x.score, reverse=True)[:top_n]
    
    def recommend_directory_mapping(self) -> List[ReferenceRecommendation]:
        """推荐目录间的映射关系"""
        print("🗺️ 分析目录映射关系...")
        
        recommendations = []
        
        # Struct -> Knowledge 映射
        struct_docs = [d for p, d in self.documents.items() if p.startswith("Struct/")]
        knowledge_docs = [d for p, d in self.documents.items() if p.startswith("Knowledge/")]
        flink_docs = [d for p, d in self.documents.items() if p.startswith("Flink/")]
        
        # 为每个 Struct 文档推荐 Knowledge 文档
        for s_doc in struct_docs[:20]:  # 限制数量
            for k_doc in knowledge_docs:
                topic_sim, topic = self.calculate_topic_similarity(s_doc, k_doc)
                if topic_sim > 0.3:
                    recommendations.append(ReferenceRecommendation(
                        source=s_doc.path,
                        target=k_doc.path,
                        score=topic_sim,
                        reason=f"理论到实践映射: {topic}",
                        confidence="medium" if topic_sim > 0.5 else "low"
                    ))
                    
        # Knowledge -> Flink 映射
        for k_doc in knowledge_docs[:20]:
            for f_doc in flink_docs:
                topic_sim, topic = self.calculate_topic_similarity(k_doc, f_doc)
                if topic_sim > 0.4:
                    recommendations.append(ReferenceRecommendation(
                        source=k_doc.path,
                        target=f_doc.path,
                        score=topic_sim,
                        reason=f"知识到实现映射: {topic}",
                        confidence="high" if topic_sim > 0.6 else "medium"
                    ))
                    
        return sorted(recommendations, key=lambda x: x.score, reverse=True)[:50]
    
    def generate_mermaid_graph(self) -> str:
        """生成 Mermaid 引用关系图"""
        lines = ["```mermaid", "graph TB"]
        
        # 按目录分组
        sections = defaultdict(list)
        for path in self.documents:
            section = path.split('/')[0] if '/' in path else 'other'
            sections[section].append(path)
            
        # 添加子图
        colors = {"Struct": "#e1bee7", "Knowledge": "#c8e6c9", "Flink": "#bbdefb"}
        
        for section, docs in sections.items():
            if len(docs) > 20:
                docs = docs[:20]  # 限制数量
                
            lines.append(f"    subgraph {section}")
            for doc in docs:
                node_id = self._path_to_node_id(doc)
                label = os.path.basename(doc).replace('.md', '')
                lines.append(f"        {node_id}[{label}]")
            lines.append("    end")
            
        # 添加边（限制数量）
        edge_count = 0
        for source, targets in self.ref_graph.items():
            if edge_count >= 50:
                break
            for target in list(targets)[:3]:  # 每个文档最多3条边
                if edge_count >= 50:
                    break
                source_id = self._path_to_node_id(source)
                target_id = self._path_to_node_id(target)
                lines.append(f"    {source_id} --> {target_id}")
                edge_count += 1
                
        lines.append("```")
        return "\n".join(lines)
    
    def _path_to_node_id(self, path: str) -> str:
        """将路径转换为节点ID"""
        return "node_" + hashlib.md5(path.encode()).hexdigest()[:8]
    
    def generate_report(self) -> dict:
        """生成完整分析报告"""
        print("📊 生成分析报告中...")
        
        # 基础统计
        total_docs = len(self.documents)
        total_refs = sum(len(refs) for refs in self.ref_graph.values())
        
        # 孤立文档
        isolated = self.find_isolated_documents(threshold=2)
        
        # 热点文档
        hubs = self.find_hub_documents(top_n=20)
        
        # 目录间映射推荐
        dir_mappings = self.recommend_directory_mapping()
        
        # 为每个目录生成推荐
        per_dir_recommendations = {}
        for section in ["Struct/", "Knowledge/", "Flink/"]:
            section_docs = [p for p in self.documents if p.startswith(section)]
            recs = []
            for doc_path in section_docs[:10]:
                doc_recs = self.recommend_cross_refs(doc_path, top_n=5)
                if doc_recs:
                    recs.extend(doc_recs)
            per_dir_recommendations[section] = recs[:20]
        
        report = {
            "summary": {
                "total_documents": total_docs,
                "total_references": total_refs,
                "avg_refs_per_doc": round(total_refs / total_docs, 2) if total_docs > 0 else 0,
                "isolated_count": len(isolated),
                "recommendations_generated": sum(len(r) for r in per_dir_recommendations.values())
            },
            "isolated_documents": [
                {
                    "path": d.path,
                    "title": d.title,
                    "outgoing": out_count,
                    "incoming": in_count
                }
                for d, out_count, in_count in isolated[:20]
            ],
            "hub_documents": [
                {
                    "path": d.path,
                    "title": d.title,
                    "score": score,
                    "outgoing": out_count,
                    "incoming": in_count
                }
                for d, score, out_count, in_count in hubs
            ],
            "directory_mappings": [
                {
                    "source": r.source,
                    "target": r.target,
                    "score": round(r.score, 3),
                    "reason": r.reason,
                    "confidence": r.confidence
                }
                for r in dir_mappings[:30]
            ],
            "per_directory_recommendations": {
                k: [
                    {
                        "source": r.source,
                        "target": r.target,
                        "score": round(r.score, 3),
                        "reason": r.reason,
                        "confidence": r.confidence
                    }
                    for r in v
                ]
                for k, v in per_dir_recommendations.items()
            },
            "mermaid_graph": self.generate_mermaid_graph()
        }
        
        return report
    
    def save_report(self, output_path: str = "cross-ref-analysis-report.json") -> None:
        """保存报告到文件"""
        report = self.generate_report()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 报告已保存: {output_path}")
        
        # 同时生成 Markdown 报告
        md_path = output_path.replace('.json', '.md')
        self._save_markdown_report(report, md_path)
        
    def _save_markdown_report(self, report: dict, output_path: str) -> None:
        """生成 Markdown 格式的报告"""
        lines = [
            "# 文档交叉引用分析报告",
            "",
            f"生成时间: {os.popen('date').read().strip()}",
            "",
            "## 📊 统计概览",
            "",
            f"| 指标 | 数值 |",
            f"|------|------|",
            f"| 文档总数 | {report['summary']['total_documents']} |",
            f"| 引用总数 | {report['summary']['total_references']} |",
            f"| 平均每文档引用 | {report['summary']['avg_refs_per_doc']} |",
            f"| 孤立文档数 | {report['summary']['isolated_count']} |",
            f"| 生成推荐数 | {report['summary']['recommendations_generated']} |",
            "",
            "## 🔗 引用网络可视化",
            "",
            report['mermaid_graph'],
            "",
            "## 📉 孤立文档（引用数<2）",
            "",
            "| 文档路径 | 标题 | 出链 | 入链 |",
            "|----------|------|------|------|"
        ]
        
        for item in report['isolated_documents'][:15]:
            lines.append(f"| {item['path']} | {item['title'][:40]}... | {item['outgoing']} | {item['incoming']} |")
            
        lines.extend([
            "",
            "## 🔥 热点文档（Top 15）",
            "",
            "| 排名 | 文档路径 | 总分 | 出链 | 入链 |",
            "|------|----------|------|------|------|"
        ])
        
        for i, item in enumerate(report['hub_documents'][:15], 1):
            lines.append(f"| {i} | {item['path']} | {item['score']} | {item['outgoing']} | {item['incoming']} |")
            
        lines.extend([
            "",
            "## 🗺️ 目录间映射推荐（Top 15）",
            "",
            "| 源文档 | 目标文档 | 分数 | 原因 | 置信度 |",
            "|--------|----------|------|------|--------|"
        ])
        
        for item in report['directory_mappings'][:15]:
            lines.append(f"| {item['source']} | {item['target']} | {item['score']} | {item['reason']} | {item['confidence']} |")
            
        lines.append("")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
            
        print(f"✅ Markdown 报告已保存: {output_path}")


def main():
    """主函数"""
    print("=" * 60)
    print("📚 文档交叉引用智能推荐系统")
    print("=" * 60)
    
    recommender = CrossRefRecommender()
    
    # 扫描文档
    recommender.scan_documents()
    
    # 构建引用图
    recommender.build_reference_graph()
    
    # 生成并保存报告
    recommender.save_report("cross-ref-analysis-report.json")
    
    print("\n" + "=" * 60)
    print("✅ 分析完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
