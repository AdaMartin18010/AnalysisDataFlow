#!/usr/bin/env python3
"""
知识检索系统
功能：
- 全文搜索索引
- 概念快速定位
- 智能推荐

作者: AnalysisDataFlow Toolchain Team
版本: 1.0.0
日期: 2026-04-11
"""

import re
import os
import json
import glob
import math
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict, Counter
import argparse


@dataclass
class SearchResult:
    """搜索结果"""
    file_path: str
    title: str
    score: float
    highlights: List[str]
    matched_terms: List[str]


@dataclass
class SearchIndex:
    """搜索索引"""
    term_freq: Dict[str, Dict[str, int]]  # term -> {doc_id -> freq}
    doc_freq: Dict[str, int]  # term -> 文档频率
    doc_lengths: Dict[str, int]  # doc_id -> 文档长度
    doc_titles: Dict[str, str]  # doc_id -> 标题
    doc_snippets: Dict[str, str]  # doc_id -> 摘要
    avg_doc_length: float
    total_docs: int


class KnowledgeSearchSystem:
    """知识检索系统"""
    
    # BM25参数
    K1 = 1.5
    B = 0.75
    
    # 停用词
    STOP_WORDS = {
        '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '之', '与', '及', '等', '或', '但', '而', '若', '为', '以', '于', '被', '将', '向', '从', '对', '关于',
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what'
    }
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        self.index: SearchIndex = None
        self.concept_index: Dict[str, List[Dict]] = defaultdict(list)
        self.formal_element_index: Dict[str, Dict] = {}
        
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
                if not any(x in str(path) for x in ['TEMPLATE', '_TEMPLATE']):
                    md_files.append(path)
                    
        return sorted(set(md_files))
    
    def tokenize(self, text: str) -> List[str]:
        """分词"""
        # 中文词汇
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,}', text)
        # 英文单词
        english_words = re.findall(r'[a-zA-Z]{3,}', text.lower())
        # 数字
        numbers = re.findall(r'\d+', text)
        
        tokens = chinese_words + english_words + numbers
        tokens = [t for t in tokens if t not in self.STOP_WORDS and len(t) > 1]
        return tokens
    
    def extract_title(self, content: str) -> str:
        """提取文档标题"""
        lines = content.split('\n')
        for line in lines[:20]:
            if line.startswith('# ') and not line.startswith('## '):
                return line.lstrip('# ').strip()
        return "Untitled"
    
    def extract_snippet(self, content: str, max_length: int = 200) -> str:
        """提取文档摘要"""
        # 移除Markdown标记
        text = re.sub(r'```[\s\S]*?```', ' ', content)
        text = re.sub(r'`[^`]+`', ' ', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'[#*_>]', ' ', text)
        text = ' '.join(text.split())
        
        return text[:max_length] + ('...' if len(text) > max_length else '')
    
    def build_index(self) -> SearchIndex:
        """构建搜索索引"""
        print("🔍 Building search index...")
        
        files = self.scan_all_files()
        
        term_freq = defaultdict(lambda: defaultdict(int))
        doc_freq = defaultdict(int)
        doc_lengths = {}
        doc_titles = {}
        doc_snippets = {}
        
        for i, file_path in enumerate(files, 1):
            if i % 100 == 0:
                print(f"   Progress: {i}/{len(files)} files")
                
            try:
                content = file_path.read_text(encoding='utf-8')
            except Exception:
                continue
                
            rel_path = str(file_path.relative_to(self.base_path))
            
            # 提取内容
            text = re.sub(r'```[\s\S]*?```', ' ', content)
            text = re.sub(r'`[^`]+`', ' ', text)
            
            tokens = self.tokenize(text)
            doc_lengths[rel_path] = len(tokens)
            doc_titles[rel_path] = self.extract_title(content)
            doc_snippets[rel_path] = self.extract_snippet(content)
            
            # 统计词频
            unique_terms = set()
            for token in tokens:
                term_freq[token][rel_path] += 1
                unique_terms.add(token)
                
            # 文档频率
            for term in unique_terms:
                doc_freq[term] += 1
                
            # 索引形式化元素
            self._index_formal_elements(content, rel_path)
            
        avg_length = sum(doc_lengths.values()) / len(doc_lengths) if doc_lengths else 0
        
        self.index = SearchIndex(
            term_freq=dict(term_freq),
            doc_freq=dict(doc_freq),
            doc_lengths=doc_lengths,
            doc_titles=doc_titles,
            doc_snippets=doc_snippets,
            avg_doc_length=avg_length,
            total_docs=len(files)
        )
        
        print(f"   Indexed {self.index.total_docs} documents")
        print(f"   {len(self.index.term_freq)} unique terms")
        
        return self.index
    
    def _index_formal_elements(self, content: str, file_path: str):
        """索引形式化元素"""
        # 定理、定义、引理等
        patterns = [
            (r'\*\*定义\s*\((Def-[SKF]-\d{2}-\d{2,3})\)\s*[:：]\s*\*\*([^*]+)\*\*', 'definition'),
            (r'\*\*定理\s*\((Thm-[SKF]-\d{2}-\d{2,3})\)\s*[:：]\s*\*\*([^*]+)\*\*', 'theorem'),
            (r'\*\*引理\s*\((Lemma-[SKF]-\d{2}-\d{2,3})\)\s*[:：]\s*\*\*([^*]+)\*\*', 'lemma'),
            (r'\*\*命题\s*\((Prop-[SKF]-\d{2}-\d{2,3})\)\s*[:：]\s*\*\*([^*]+)\*\*', 'proposition'),
        ]
        
        for pattern, elem_type in patterns:
            for match in re.finditer(pattern, content):
                elem_id = match.group(1)
                elem_name = match.group(2)
                
                self.formal_element_index[elem_id] = {
                    'id': elem_id,
                    'name': elem_name,
                    'type': elem_type,
                    'file': file_path
                }
                
                # 添加到概念索引
                self.concept_index[elem_name].append({
                    'type': elem_type,
                    'id': elem_id,
                    'file': file_path
                })
    
    def bm25_score(self, term: str, doc_id: str) -> float:
        """计算BM25分数"""
        if doc_id not in self.index.term_freq.get(term, {}):
            return 0.0
            
        tf = self.index.term_freq[term][doc_id]
        df = self.index.doc_freq.get(term, 0)
        doc_len = self.index.doc_lengths.get(doc_id, 0)
        avg_len = self.index.avg_doc_length
        N = self.index.total_docs
        
        # IDF
        idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
        
        # TF normalization
        tf_norm = tf * (self.K1 + 1) / (tf + self.K1 * (1 - self.B + self.B * doc_len / avg_len))
        
        return idf * tf_norm
    
    def search(self, query: str, top_k: int = 10) -> List[SearchResult]:
        """执行搜索"""
        if not self.index:
            self.build_index()
            
        query_terms = self.tokenize(query)
        if not query_terms:
            return []
            
        scores = defaultdict(float)
        matched_terms = defaultdict(set)
        
        for term in query_terms:
            for doc_id in self.index.term_freq.get(term, {}):
                score = self.bm25_score(term, doc_id)
                scores[doc_id] += score
                matched_terms[doc_id].add(term)
                
        # 排序并获取top-k
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        for doc_id, score in ranked:
            # 提取高亮片段
            highlights = self._extract_highlights(doc_id, matched_terms[doc_id])
            
            results.append(SearchResult(
                file_path=doc_id,
                title=self.index.doc_titles.get(doc_id, 'Untitled'),
                score=score,
                highlights=highlights,
                matched_terms=list(matched_terms[doc_id])
            ))
            
        return results
    
    def _extract_highlights(self, doc_id: str, terms: Set[str], num_highlights: int = 3) -> List[str]:
        """提取高亮片段"""
        file_path = self.base_path / doc_id
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            return []
            
        # 移除代码块
        content = re.sub(r'```[\s\S]*?```', ' ', content)
        
        lines = content.split('\n')
        highlights = []
        
        for line in lines:
            if any(term.lower() in line.lower() for term in terms):
                # 高亮匹配词
                highlighted = line
                for term in sorted(terms, key=len, reverse=True):
                    highlighted = re.sub(
                        f'({re.escape(term)})',
                        r'**\1**',
                        highlighted,
                        flags=re.IGNORECASE
                    )
                if len(highlighted.strip()) > 20:
                    highlights.append(highlighted.strip())
                    if len(highlights) >= num_highlights:
                        break
                        
        return highlights
    
    def search_concept(self, concept_name: str) -> List[Dict]:
        """搜索概念"""
        results = []
        
        # 精确匹配
        if concept_name in self.concept_index:
            results.extend(self.concept_index[concept_name])
            
        # 模糊匹配
        for name, items in self.concept_index.items():
            if concept_name.lower() in name.lower() or name.lower() in concept_name.lower():
                if name != concept_name:
                    results.extend(items)
                    
        return results
    
    def search_formal_element(self, element_id: str) -> Optional[Dict]:
        """搜索形式化元素"""
        return self.formal_element_index.get(element_id)
    
    def suggest_related(self, doc_id: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """推荐相关文档"""
        if not self.index or doc_id not in self.index.doc_lengths:
            return []
            
        # 获取文档的特征词
        doc_terms = {}
        for term, docs in self.index.term_freq.items():
            if doc_id in docs:
                doc_terms[term] = docs[doc_id]
                
        # 计算与其他文档的相似度
        similarities = {}
        for other_id in self.index.doc_lengths:
            if other_id == doc_id:
                continue
                
            # 计算共同词
            common_terms = set(doc_terms.keys()) & set(self.index.term_freq.keys())
            if not common_terms:
                continue
                
            # 简单相似度：共同词加权和
            sim = sum(doc_terms.get(t, 0) * self.index.term_freq[t].get(other_id, 0) 
                     for t in common_terms)
            
            if sim > 0:
                similarities[other_id] = sim
                
        return sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k]
    
    def save_index(self, output_path: str):
        """保存索引到文件"""
        if not self.index:
            self.build_index()
            
        index_data = {
            'term_freq': self.index.term_freq,
            'doc_freq': self.index.doc_freq,
            'doc_lengths': self.index.doc_lengths,
            'doc_titles': self.index.doc_titles,
            'doc_snippets': self.index.doc_snippets,
            'avg_doc_length': self.index.avg_doc_length,
            'total_docs': self.index.total_docs,
            'concept_index': dict(self.concept_index),
            'formal_elements': self.formal_element_index
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
            
        print(f"\n💾 Index saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Knowledge Search System')
    parser.add_argument('--base-path', default='.', help='项目根目录')
    parser.add_argument('--build-index', action='store_true', help='构建索引')
    parser.add_argument('--index-file', default='search-index.json', help='索引文件路径')
    parser.add_argument('--query', help='搜索查询')
    parser.add_argument('--search-concept', help='搜索概念')
    parser.add_argument('--search-element', help='搜索形式化元素ID')
    parser.add_argument('--suggest-related', help='推荐相关文档')
    parser.add_argument('--top-k', type=int, default=10, help='返回结果数量')
    parser.add_argument('--interactive', action='store_true', help='交互模式')
    
    args = parser.parse_args()
    
    search_system = KnowledgeSearchSystem(args.base_path)
    
    # 构建或加载索引
    if args.build_index or not Path(args.index_file).exists():
        search_system.build_index()
        search_system.save_index(args.index_file)
    else:
        print(f"Loading index from {args.index_file}...")
        with open(args.index_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        search_system.index = SearchIndex(
            term_freq=data['term_freq'],
            doc_freq=data['doc_freq'],
            doc_lengths=data['doc_lengths'],
            doc_titles=data['doc_titles'],
            doc_snippets=data['doc_snippets'],
            avg_doc_length=data['avg_doc_length'],
            total_docs=data['total_docs']
        )
        search_system.concept_index = defaultdict(list, data.get('concept_index', {}))
        search_system.formal_element_index = data.get('formal_elements', {})
        print("Index loaded.")
    
    # 执行搜索
    if args.query:
        print(f"\n🔍 Searching for: {args.query}")
        results = search_system.search(args.query, args.top_k)
        
        print(f"\nFound {len(results)} results:\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r.title}")
            print(f"   File: {r.file_path}")
            print(f"   Score: {r.score:.2f}")
            print(f"   Matched: {', '.join(r.matched_terms)}")
            if r.highlights:
                print(f"   Highlights:")
                for h in r.highlights[:2]:
                    print(f"     - {h[:150]}...")
            print()
            
    if args.search_concept:
        print(f"\n📚 Searching concept: {args.search_concept}")
        results = search_system.search_concept(args.search_concept)
        
        print(f"\nFound {len(results)} concept instances:\n")
        for r in results[:args.top_k]:
            print(f"  • [{r['type']}] {r.get('id', '')} in {r['file']}")
            
    if args.search_element:
        print(f"\n📐 Searching element: {args.search_element}")
        result = search_system.search_formal_element(args.search_element)
        
        if result:
            print(f"\nFound:")
            print(f"  ID: {result['id']}")
            print(f"  Name: {result['name']}")
            print(f"  Type: {result['type']}")
            print(f"  File: {result['file']}")
        else:
            print("  Not found")
            
    if args.suggest_related:
        print(f"\n📎 Suggesting related to: {args.suggest_related}")
        related = search_system.suggest_related(args.suggest_related, args.top_k)
        
        print(f"\nRelated documents:\n")
        for doc_id, score in related:
            title = search_system.index.doc_titles.get(doc_id, 'Untitled')
            print(f"  • {title} ({doc_id}) - Score: {score:.2f}")
            
    # 交互模式
    if args.interactive:
        print("\n" + "=" * 50)
        print("🤖 Interactive Search Mode")
        print("=" * 50)
        print("Commands:")
        print("  /q <query>     - Search")
        print("  /c <concept>   - Search concept")
        print("  /e <element>   - Search formal element")
        print("  /r <doc>       - Suggest related")
        print("  /quit          - Exit")
        print("=" * 50)
        
        while True:
            try:
                cmd = input("\n> ").strip()
                if not cmd:
                    continue
                    
                if cmd.startswith('/q '):
                    query = cmd[3:]
                    results = search_system.search(query, 5)
                    print(f"\nResults for '{query}':")
                    for r in results:
                        print(f"  • {r.title} ({r.score:.2f})")
                        
                elif cmd.startswith('/c '):
                    concept = cmd[3:]
                    results = search_system.search_concept(concept)
                    print(f"\nConcept '{concept}':")
                    for r in results[:5]:
                        print(f"  • [{r['type']}] {r.get('id', '')}")
                        
                elif cmd.startswith('/e '):
                    elem = cmd[3:]
                    result = search_system.search_formal_element(elem)
                    print(f"\nElement '{elem}':")
                    if result:
                        print(f"  Name: {result['name']}")
                        print(f"  File: {result['file']}")
                    else:
                        print("  Not found")
                        
                elif cmd.startswith('/r '):
                    doc = cmd[3:]
                    related = search_system.suggest_related(doc, 5)
                    print(f"\nRelated to '{doc}':")
                    for d, s in related:
                        print(f"  • {d} ({s:.2f})")
                        
                elif cmd == '/quit':
                    break
                    
                else:
                    # 默认搜索
                    results = search_system.search(cmd, 5)
                    print(f"\nResults for '{cmd}':")
                    for r in results:
                        print(f"  • {r.title}")
                        
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
                
        print("\nGoodbye!")
    
    return 0


if __name__ == '__main__':
    exit(main())
