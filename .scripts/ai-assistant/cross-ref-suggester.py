#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用建议器 - Cross Reference Suggester for AnalysisDataFlow
基于内容相似度分析建议文档链接，无需API Key

功能:
- 分析文档内容相似度
- 建议相关文档链接
- 构建文档关系图
- 发现孤立的文档
"""

import os
import re
import sys
import yaml
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import math


@dataclass
class Document:
    """文档数据结构"""
    filepath: str
    title: str = ""
    content: str = ""
    keywords: Set[str] = field(default_factory=set)
    definitions: List[str] = field(default_factory=list)
    theorems: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)


@dataclass
class LinkSuggestion:
    """链接建议数据结构"""
    source: str
    target: str
    score: float
    reason: str
    anchor_text: str = ""


class CrossRefSuggester:
    """交叉引用建议器"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.documents: Dict[str, Document] = {}
        self.keyword_index: Dict[str, Set[str]] = defaultdict(set)
        self.suggestions: List[LinkSuggestion] = []
        self.logger = self._setup_logger()
    
    def _load_config(self, config_path: str = None) -> Dict:
        """加载配置文件"""
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__), 'config.yaml'
            )
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load config: {e}")
            return {}
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger('cross-ref-suggester')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def extract_keywords(self, content: str) -> Set[str]:
        """提取关键词"""
        keywords = set()
        
        # 提取加粗文本
        bold = re.findall(r'\*\*([^*]{2,20})\*\*', content)
        keywords.update(bold)
        
        # 提取代码术语
        code = re.findall(r'`([^`]{2,20})`', content)
        keywords.update(code)
        
        # 提取定理/定义编号
        theorems = re.findall(r'(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d{2}-\d{2}', content)
        keywords.update(theorems)
        
        # 提取中文字词 (2-6字)
        chinese = re.findall(r'[\u4e00-\u9fff]{2,6}', content)
        
        # 停用词过滤
        stopwords = set([
            '的', '是', '在', '和', '了', '与', '为', '对', '有', '将',
            'the', 'is', 'are', 'and', 'of', 'to', 'in', 'for', 'with',
            'a', 'an', 'this', 'that', 'as', 'by', 'on', 'at', 'from'
        ])
        
        keywords.update([w for w in chinese if w not in stopwords])
        
        return keywords
    
    def parse_document(self, filepath: str) -> Document:
        """解析文档"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else Path(filepath).stem
        
        # 提取关键词
        keywords = self.extract_keywords(content)
        
        # 提取定义
        definitions = re.findall(r'\*\*(Def-[SKF]-\d{2}-\d{2})\*\*', content)
        
        # 提取定理
        theorems = re.findall(r'\*\*(Thm-[SKF]-\d{2}-\d{2})\*\*', content)
        theorems += re.findall(r'\*\*(Lemma-[SKF]-\d{2}-\d{2})\*\*', content)
        theorems += re.findall(r'\*\*(Prop-[SKF]-\d{2}-\d{2})\*\*', content)
        
        # 提取已有链接
        links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)
        link_targets = [link[1] for link in links]
        
        # 提取引用
        references = re.findall(r'\[\^(\d+)\]', content)
        
        return Document(
            filepath=filepath,
            title=title,
            content=content,
            keywords=keywords,
            definitions=definitions,
            theorems=theorems,
            references=references,
            links=link_targets
        )
    
    def build_index(self, directory: str, pattern: str = '*.md') -> None:
        """构建文档索引"""
        self.logger.info(f"Building index for {directory}")
        
        for filepath in Path(directory).rglob(pattern):
            try:
                doc = self.parse_document(str(filepath))
                self.documents[str(filepath)] = doc
                
                # 构建关键词倒排索引
                for keyword in doc.keywords:
                    self.keyword_index[keyword].add(str(filepath))
                
                self.logger.debug(f"Indexed: {filepath}")
            except Exception as e:
                self.logger.error(f"Error parsing {filepath}: {e}")
        
        self.logger.info(f"Indexed {len(self.documents)} documents")
    
    def calculate_similarity(self, doc1: Document, doc2: Document) -> float:
        """计算文档相似度 (Jaccard + TF-IDF 混合)"""
        # Jaccard 相似度
        keywords1 = doc1.keywords
        keywords2 = doc2.keywords
        
        if not keywords1 or not keywords2:
            return 0.0
        
        intersection = len(keywords1 & keywords2)
        union = len(keywords1 | keywords2)
        jaccard = intersection / union if union > 0 else 0.0
        
        # 定义/定理匹配加权
        def_overlap = set(doc1.definitions) & set(doc2.definitions)
        thm_overlap = set(doc1.theorems) & set(doc2.theorems)
        
        bonus = len(def_overlap) * 0.1 + len(thm_overlap) * 0.1
        
        return min(1.0, jaccard + bonus)
    
    def suggest_links(self, doc_path: str, top_k: int = 5) -> List[LinkSuggestion]:
        """为单个文档建议链接"""
        if doc_path not in self.documents:
            return []
        
        source_doc = self.documents[doc_path]
        suggestions = []
        
        for other_path, other_doc in self.documents.items():
            if other_path == doc_path:
                continue
            
            # 跳过已有链接
            if other_path in source_doc.links:
                continue
            
            # 计算相似度
            similarity = self.calculate_similarity(source_doc, other_doc)
            
            if similarity >= self.config.get('cross_ref', {}).get('similarity_threshold', 0.3):
                # 生成理由
                common_keywords = source_doc.keywords & other_doc.keywords
                reason = f"共同关键词: {', '.join(list(common_keywords)[:3])}"
                
                # 生成锚文本
                anchor_text = other_doc.title
                
                suggestions.append(LinkSuggestion(
                    source=doc_path,
                    target=other_path,
                    score=similarity,
                    reason=reason,
                    anchor_text=anchor_text
                ))
        
        # 排序并取 top_k
        suggestions.sort(key=lambda x: x.score, reverse=True)
        return suggestions[:top_k]
    
    def analyze_all(self) -> None:
        """分析所有文档并生成建议"""
        self.logger.info("Analyzing cross-references...")
        
        for doc_path in self.documents:
            doc_suggestions = self.suggest_links(doc_path)
            self.suggestions.extend(doc_suggestions)
        
        self.logger.info(f"Generated {len(self.suggestions)} suggestions")
    
    def find_orphaned_documents(self) -> List[str]:
        """发现孤立文档（没有链接也没有被链接）"""
        orphaned = []
        
        for doc_path, doc in self.documents.items():
            # 检查是否有出链
            has_outgoing = len(doc.links) > 0
            
            # 检查是否有入链
            has_incoming = any(
                doc_path in other.links 
                for other in self.documents.values()
            )
            
            if not has_outgoing and not has_incoming:
                orphaned.append(doc_path)
        
        return orphaned
    
    def find_missing_references(self, doc_path: str) -> List[Tuple[str, str]]:
        """查找文中提到但未引用的定义/定理"""
        if doc_path not in self.documents:
            return []
        
        doc = self.documents[doc_path]
        missing = []
        
        # 检查文档中提到的定义
        for keyword in doc.keywords:
            if keyword.startswith('Def-') or keyword.startswith('Thm-'):
                # 检查是否已有引用
                if keyword not in doc.content:
                    continue
                    
                # 检查是否已链接到包含该定义的文档
                found = False
                for other_path, other_doc in self.documents.items():
                    if other_path == doc_path:
                        continue
                    if keyword in other_doc.definitions or keyword in other_doc.theorems:
                        found = True
                        break
                
                if not found:
                    missing.append((keyword, "未找到来源文档"))
        
        return missing
    
    def generate_link_graph(self) -> Dict:
        """生成文档链接图 (用于 Mermaid)"""
        nodes = []
        edges = []
        
        # 生成节点
        for i, (doc_path, doc) in enumerate(self.documents.items()):
            node_id = f"doc{i}"
            nodes.append({
                'id': node_id,
                'label': doc.title[:30],
                'path': doc_path
            })
        
        # 生成边 (从已有链接)
        doc_to_id = {path: f"doc{i}" for i, path in enumerate(self.documents.keys())}
        
        for doc_path, doc in self.documents.items():
            source_id = doc_to_id.get(doc_path)
            for link in doc.links:
                # 解析相对路径
                target_path = os.path.normpath(
                    os.path.join(os.path.dirname(doc_path), link)
                )
                if target_path in doc_to_id:
                    target_id = doc_to_id[target_path]
                    edges.append({
                        'source': source_id,
                        'target': target_id
                    })
        
        return {'nodes': nodes, 'edges': edges}
    
    def generate_mermaid_graph(self) -> str:
        """生成 Mermaid 图代码"""
        graph = self.generate_link_graph()
        
        lines = ['```mermaid', 'graph TD']
        
        # 节点定义
        for node in graph['nodes']:
            lines.append(f'    {node["id"]}["{node["label"]}"]')
        
        lines.append('')
        
        # 边定义
        for edge in graph['edges']:
            lines.append(f'    {edge["source"]} --> {edge["target"]}')
        
        lines.append('```')
        
        return '\n'.join(lines)
    
    def generate_report(self, output_path: str = None) -> str:
        """生成报告"""
        lines = [
            "# 交叉引用分析报告",
            "",
            f"生成时间: {__import__('datetime').datetime.now().isoformat()}",
            f"文档总数: {len(self.documents)}",
            f"建议链接数: {len(self.suggestions)}",
            "",
            "---",
            "",
            "## 链接建议",
            "",
        ]
        
        # 按源文档分组
        by_source = defaultdict(list)
        for sug in self.suggestions:
            by_source[sug.source].append(sug)
        
        for source, suggestions in sorted(by_source.items()):
            source_doc = self.documents.get(source)
            title = source_doc.title if source_doc else Path(source).name
            
            lines.append(f"### {title}")
            lines.append(f"**文件**: `{source}`")
            lines.append("")
            lines.append("建议添加以下链接：")
            lines.append("")
            lines.append("| 目标文档 | 相似度 | 理由 | 建议链接 |")
            lines.append("|----------|--------|------|----------|")
            
            for sug in suggestions:
                target_doc = self.documents.get(sug.target)
                target_title = target_doc.title if target_doc else Path(sug.target).name
                rel_path = os.path.relpath(sug.target, os.path.dirname(source))
                link_code = f"[{sug.anchor_text}]({rel_path})"
                lines.append(
                    f"| {target_title} | {sug.score:.2f} | {sug.reason} | `{link_code}` |"
                )
            
            lines.append("")
        
        # 孤立文档
        lines.extend([
            "---",
            "",
            "## 孤立文档",
            "",
            "以下文档没有链接也没有被链接，建议检查：",
            "",
        ])
        
        orphaned = self.find_orphaned_documents()
        if orphaned:
            for path in orphaned:
                doc = self.documents.get(path)
                title = doc.title if doc else Path(path).name
                lines.append(f"- `{path}` ({title})")
        else:
            lines.append("✅ 未发现孤立文档")
        
        lines.append("")
        
        # 文档关系图
        lines.extend([
            "---",
            "",
            "## 文档关系图",
            "",
        ])
        lines.append(self.generate_mermaid_graph())
        lines.append("")
        
        report = '\n'.join(lines)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            self.logger.info(f"Report saved to: {output_path}")
        
        return report
    
    def export_suggestions_json(self, output_path: str) -> None:
        """导出建议为 JSON"""
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        data = {
            'documents': {
                path: {
                    'title': doc.title,
                    'keywords': list(doc.keywords),
                    'definitions': doc.definitions,
                    'theorems': doc.theorems,
                    'links': doc.links
                }
                for path, doc in self.documents.items()
            },
            'suggestions': [
                {
                    'source': sug.source,
                    'target': sug.target,
                    'score': sug.score,
                    'reason': sug.reason,
                    'anchor_text': sug.anchor_text
                }
                for sug in self.suggestions
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Suggestions exported to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='交叉引用建议器 - AnalysisDataFlow AI Assistant'
    )
    parser.add_argument(
        'directory',
        help='要分析的文档目录'
    )
    parser.add_argument(
        '-c', '--config',
        help='配置文件路径'
    )
    parser.add_argument(
        '-o', '--output',
        help='报告输出路径',
        default='cross-ref-report.md'
    )
    parser.add_argument(
        '--json',
        help='导出 JSON 格式的建议',
        default=None
    )
    parser.add_argument(
        '--pattern',
        help='文件匹配模式',
        default='*.md'
    )
    parser.add_argument(
        '--suggest-for',
        help='只为指定文档生成建议'
    )
    parser.add_argument(
        '--top-k',
        help='每个文档的建议数量',
        type=int,
        default=5
    )
    
    args = parser.parse_args()
    
    suggester = CrossRefSuggester(args.config)
    
    # 构建索引
    suggester.build_index(args.directory, args.pattern)
    
    if args.suggest_for:
        # 只为单个文档生成建议
        suggestions = suggester.suggest_links(args.suggest_for, args.top_k)
        print(f"Suggestions for {args.suggest_for}:")
        for sug in suggestions:
            print(f"  -> {sug.target} (score: {sug.score:.2f})")
            print(f"     Reason: {sug.reason}")
            print(f"     Link: [{sug.anchor_text}]({sug.target})")
    else:
        # 分析所有文档
        suggester.analyze_all()
        
        # 生成报告
        suggester.generate_report(args.output)
        
        # 导出 JSON (如果需要)
        if args.json:
            suggester.export_suggestions_json(args.json)


if __name__ == '__main__':
    main()
