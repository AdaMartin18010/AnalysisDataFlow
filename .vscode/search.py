#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 搜索工具

功能：
- 关键词搜索（支持模糊匹配）
- 定理编号搜索（如 Thm-S-17-01）
- 文档路径搜索
- 多条件组合搜索
- 结果高亮和相关性排序

用法：
    python search.py "checkpoint"
    python search.py "Thm-S-17-01"
    python search.py "checkpoint exactly-once" --operator AND
    python search.py "flink" --category Flink
    python search.py "theorem" --type theorem
    python search.py "watermark" --highlight
"""

import os
import re
import json
import math
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict
from difflib import SequenceMatcher


@dataclass
class SearchResult:
    """搜索结果条目"""
    doc_path: str
    title: str
    summary: str
    category: str
    score: float
    matched_keywords: List[str] = field(default_factory=list)
    formal_elements: List[Dict] = field(default_factory=list)
    highlights: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'doc_path': self.doc_path,
            'title': self.title,
            'summary': self.summary,
            'category': self.category,
            'score': round(self.score, 4),
            'matched_keywords': self.matched_keywords,
            'formal_elements': self.formal_elements,
            'highlights': self.highlights,
        }


class SearchEngine:
    """搜索引擎"""
    
    # 颜色代码（用于终端高亮）
    COLORS = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
    }
    
    # 形式化ID正则
    FORMAL_ID_PATTERN = re.compile(
        r'^(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2,3})$',
        re.IGNORECASE
    )
    
    def __init__(self, index_path: str = ".vscode/search-index.json"):
        self.index_path = Path(index_path)
        self.index_data: Dict[str, Any] = {}
        self.documents: Dict[str, Dict] = {}
        self.formal_elements: Dict[str, Dict] = {}
        self.inverted_index: Dict[str, Dict] = {}
        self.metadata: Dict[str, Any] = {}
        
        self._load_index()
    
    def _load_index(self):
        """加载索引文件"""
        if not self.index_path.exists():
            raise FileNotFoundError(f"索引文件不存在: {self.index_path}\n请先运行: python .vscode/build-search-index.py")
        
        with open(self.index_path, 'r', encoding='utf-8') as f:
            self.index_data = json.load(f)
        
        self.documents = self.index_data.get('documents', {})
        self.formal_elements = self.index_data.get('formal_elements', {})
        self.inverted_index = self.index_data.get('inverted_index', {})
        self.metadata = self.index_data.get('metadata', {})
    
    def _colorize(self, text: str, color: str) -> str:
        """给文本添加颜色"""
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['reset']}"
    
    def _highlight_text(self, text: str, keywords: List[str]) -> str:
        """高亮文本中的关键词"""
        if not keywords:
            return text
        
        # 转义特殊字符并构建正则
        escaped_keywords = [re.escape(kw) for kw in keywords]
        pattern = re.compile(
            '(' + '|'.join(escaped_keywords) + ')',
            re.IGNORECASE
        )
        
        # 替换并高亮
        def replace_match(m):
            return self._colorize(m.group(0), 'yellow')
        
        return pattern.sub(replace_match, text)
    
    def _calculate_similarity(self, s1: str, s2: str) -> float:
        """计算两个字符串的相似度"""
        return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()
    
    def _fuzzy_match(self, query: str, text: str) -> float:
        """模糊匹配得分"""
        query_lower = query.lower()
        text_lower = text.lower()
        
        # 完全匹配
        if query_lower == text_lower:
            return 1.0
        
        # 包含匹配
        if query_lower in text_lower:
            return 0.8
        
        # 开头匹配
        if text_lower.startswith(query_lower):
            return 0.7
        
        # 相似度匹配
        similarity = self._calculate_similarity(query, text)
        if similarity > 0.6:
            return similarity * 0.6
        
        # 词级别匹配
        query_words = set(query_lower.split())
        text_words = set(text_lower.split())
        if query_words and text_words:
            overlap = len(query_words & text_words)
            return (overlap / len(query_words)) * 0.5
        
        return 0.0
    
    def search_formal_id(self, formal_id: str) -> List[SearchResult]:
        """搜索形式化ID（如 Thm-S-17-01）"""
        results = []
        
        # 标准化ID
        formal_id_upper = formal_id.upper()
        
        # 精确查找
        if formal_id_upper in self.formal_elements:
            elem = self.formal_elements[formal_id_upper]
            doc_path = elem.get('location', '')
            if doc_path and doc_path in self.documents:
                doc = self.documents[doc_path]
                results.append(SearchResult(
                    doc_path=doc_path,
                    title=doc.get('title', ''),
                    summary=doc.get('summary', ''),
                    category=doc.get('category', ''),
                    score=1.0,
                    matched_keywords=[formal_id_upper],
                    formal_elements=[elem],
                    highlights=[f"找到 {formal_id_upper}: {elem.get('name', '')}"]
                ))
        
        # 模糊查找
        for elem_id, elem in self.formal_elements.items():
            if formal_id.upper() in elem_id.upper() or self._fuzzy_match(formal_id, elem_id) > 0.8:
                if not any(r.doc_path == elem.get('location', '') for r in results):
                    doc_path = elem.get('location', '')
                    if doc_path and doc_path in self.documents:
                        doc = self.documents[doc_path]
                        results.append(SearchResult(
                            doc_path=doc_path,
                            title=doc.get('title', ''),
                            summary=doc.get('summary', ''),
                            category=doc.get('category', ''),
                            score=0.9,
                            matched_keywords=[elem_id],
                            formal_elements=[elem],
                            highlights=[f"找到相似项 {elem_id}: {elem.get('name', '')}"]
                        ))
        
        return results
    
    def search_by_keyword(self, keyword: str, fuzzy: bool = True) -> List[Tuple[str, float]]:
        """通过关键词搜索文档"""
        matches = []
        keyword_lower = keyword.lower()
        
        # 精确匹配倒排索引
        if keyword_lower in self.inverted_index:
            idx_entry = self.inverted_index[keyword_lower]
            for doc_path in idx_entry.get('doc_paths', []):
                tf_score = idx_entry.get('tf_scores', {}).get(doc_path, 0)
                matches.append((doc_path, 0.5 + tf_score))
        
        if not fuzzy:
            return matches
        
        # 模糊匹配
        for idx_keyword, idx_entry in self.inverted_index.items():
            similarity = self._fuzzy_match(keyword, idx_keyword)
            if similarity > 0.6:
                for doc_path in idx_entry.get('doc_paths', []):
                    existing = next((m for m in matches if m[0] == doc_path), None)
                    if existing:
                        # 更新最高分
                        matches = [(p, max(s, similarity)) if p == doc_path else (p, s) 
                                  for p, s in matches]
                    else:
                        matches.append((doc_path, similarity * 0.5))
        
        return matches
    
    def search(
        self,
        query: str,
        category: Optional[str] = None,
        doc_type: Optional[str] = None,  # 文档类型过滤
        element_type: Optional[str] = None,  # 形式化元素类型过滤
        operator: str = 'OR',
        fuzzy: bool = True,
        limit: int = 20
    ) -> List[SearchResult]:
        """
        执行搜索
        
        Args:
            query: 搜索查询
            category: 按分类过滤 (Struct/Knowledge/Flink/Root)
            doc_type: 按文档类型过滤
            element_type: 按形式化元素类型过滤 (theorem/definition/lemma/proposition/corollary)
            operator: 多关键词操作符 (AND/OR)
            fuzzy: 是否启用模糊匹配
            limit: 返回结果数量限制
        """
        query = query.strip()
        if not query:
            return []
        
        # 检查是否是形式化ID搜索
        if self.FORMAL_ID_PATTERN.match(query) or '-' in query and any(
            prefix in query.upper() for prefix in ['THM-', 'DEF-', 'LEMMA-', 'PROP-', 'COR-']
        ):
            return self.search_formal_id(query)[:limit]
        
        # 分词
        keywords = [kw.strip() for kw in re.split(r'[\s,]+', query) if kw.strip()]
        if not keywords:
            return []
        
        # 收集所有匹配的文档
        doc_scores: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'score': 0,
            'matched_keywords': [],
            'formal_elements': [],
        })
        
        if operator.upper() == 'AND':
            # AND 操作：文档必须匹配所有关键词
            first_keyword = True
            valid_docs = set()
            
            for keyword in keywords:
                matches = self.search_by_keyword(keyword, fuzzy)
                keyword_docs = {doc_path for doc_path, _ in matches}
                
                if first_keyword:
                    valid_docs = keyword_docs
                    first_keyword = False
                else:
                    valid_docs &= keyword_docs
                
                for doc_path, score in matches:
                    if doc_path in valid_docs:
                        doc_scores[doc_path]['score'] += score
                        if keyword not in doc_scores[doc_path]['matched_keywords']:
                            doc_scores[doc_path]['matched_keywords'].append(keyword)
        else:
            # OR 操作：文档匹配任意关键词
            for keyword in keywords:
                matches = self.search_by_keyword(keyword, fuzzy)
                for doc_path, score in matches:
                    doc_scores[doc_path]['score'] += score
                    if keyword not in doc_scores[doc_path]['matched_keywords']:
                        doc_scores[doc_path]['matched_keywords'].append(keyword)
        
        # 应用过滤条件
        filtered_results = []
        for doc_path, data in doc_scores.items():
            if doc_path not in self.documents:
                continue
            
            doc = self.documents[doc_path]
            
            # 分类过滤
            if category and doc.get('category', '').lower() != category.lower():
                continue
            
            # 文档类型过滤
            if doc_type and doc.get('subcategory', '').lower() != doc_type.lower():
                continue
            
            # 形式化元素过滤
            formal_elems = []
            if element_type:
                for elem in doc.get('formal_elements', []):
                    if elem.get('element_type', '').lower() == element_type.lower():
                        formal_elems.append(elem)
                        data['score'] += 0.3  # 提升包含特定类型元素的文档得分
                if not formal_elems:
                    continue
            else:
                formal_elems = doc.get('formal_elements', [])
            
            # 标题匹配加分
            title_lower = doc.get('title', '').lower()
            for kw in data['matched_keywords']:
                if kw.lower() in title_lower:
                    data['score'] += 0.5
            
            # 关键词匹配加分
            doc_keywords = [k.lower() for k in doc.get('keywords', [])]
            for kw in data['matched_keywords']:
                if kw.lower() in doc_keywords:
                    data['score'] += 0.3
            
            # 生成高亮片段
            highlights = []
            summary = doc.get('summary', '')
            for kw in data['matched_keywords'][:3]:  # 最多3个关键词的高亮
                idx = summary.lower().find(kw.lower())
                if idx != -1:
                    start = max(0, idx - 40)
                    end = min(len(summary), idx + len(kw) + 40)
                    snippet = summary[start:end]
                    if start > 0:
                        snippet = '...' + snippet
                    if end < len(summary):
                        snippet = snippet + '...'
                    highlights.append(snippet)
            
            # 如果没有摘要匹配，使用标题
            if not highlights:
                highlights = [doc.get('title', '')]
            
            filtered_results.append(SearchResult(
                doc_path=doc_path,
                title=doc.get('title', ''),
                summary=doc.get('summary', ''),
                category=doc.get('category', ''),
                score=data['score'],
                matched_keywords=data['matched_keywords'],
                formal_elements=formal_elems[:5],  # 最多5个相关元素
                highlights=highlights[:2]  # 最多2个高亮片段
            ))
        
        # 按得分排序
        filtered_results.sort(key=lambda x: x.score, reverse=True)
        
        return filtered_results[:limit]
    
    def search_by_path(self, path_pattern: str) -> List[SearchResult]:
        """按文档路径搜索"""
        results = []
        pattern_lower = path_pattern.lower()
        
        for doc_path, doc in self.documents.items():
            if pattern_lower in doc_path.lower():
                score = 1.0 if pattern_lower == doc_path.lower() else 0.7
                results.append(SearchResult(
                    doc_path=doc_path,
                    title=doc.get('title', ''),
                    summary=doc.get('summary', ''),
                    category=doc.get('category', ''),
                    score=score,
                    matched_keywords=[path_pattern],
                    highlights=[f"路径匹配: {doc_path}"]
                ))
        
        return sorted(results, key=lambda x: x.score, reverse=True)
    
    def get_document(self, path: str) -> Optional[Dict]:
        """获取单个文档信息"""
        # 尝试精确匹配
        if path in self.documents:
            return self.documents[path]
        
        # 尝试模糊匹配
        for doc_path, doc in self.documents.items():
            if path.lower() in doc_path.lower():
                return doc
        
        return None
    
    def list_categories(self) -> Dict[str, int]:
        """列出所有分类及其文档数量"""
        return self.metadata.get('category_distribution', {})
    
    def list_formal_element_types(self) -> Dict[str, int]:
        """列出所有形式化元素类型及其数量"""
        return self.metadata.get('formal_element_types', {})
    
    def print_results(
        self,
        results: List[SearchResult],
        highlight: bool = True,
        show_formal: bool = False,
        format_type: str = 'table'
    ):
        """打印搜索结果"""
        if not results:
            print(self._colorize("未找到匹配结果", 'red'))
            return
        
        print(f"\n{self._colorize('═' * 70, 'cyan')}")
        print(f"{self._colorize(f' 找到 {len(results)} 个结果', 'bold')}")
        print(f"{self._colorize('═' * 70, 'cyan')}\n")
        
        for i, result in enumerate(results, 1):
            # 序号和得分
            score_str = f"{result.score:.2f}"
            print(f"{self._colorize(f'{i}.', 'bold')} {self._colorize(result.title, 'green')} "
                  f"[{self._colorize(score_str, 'yellow')}]")
            
            # 路径和分类
            path_str = f"   📄 {result.doc_path}"
            cat_str = f"[{result.category}]"
            print(f"{path_str} {self._colorize(cat_str, 'magenta')}")
            
            # 匹配关键词
            if result.matched_keywords:
                kw_str = ', '.join(result.matched_keywords[:5])
                print(f"   🔑 匹配: {self._colorize(kw_str, 'cyan')}")
            
            # 高亮片段
            if highlight and result.highlights:
                for hl in result.highlights[:1]:  # 只显示第一个高亮
                    highlighted = self._highlight_text(hl, result.matched_keywords)
                    print(f"   💡 {highlighted}")
            else:
                # 显示摘要
                summary = result.summary[:150] + '...' if len(result.summary) > 150 else result.summary
                print(f"   📝 {summary}")
            
            # 形式化元素
            if show_formal and result.formal_elements:
                print(f"   📐 相关形式化元素:")
                for elem in result.formal_elements[:3]:
                    elem_id = elem.get('id', '')
                    elem_name = elem.get('name', '')
                    elem_type = elem.get('element_type', '')
                    print(f"      - {self._colorize(elem_id, 'blue')} ({elem_type}): {elem_name}")
            
            print()
    
    def print_document_detail(self, path: str):
        """打印文档详细信息"""
        doc = self.get_document(path)
        if not doc:
            print(self._colorize(f"未找到文档: {path}", 'red'))
            return
        
        print(f"\n{self._colorize('═' * 70, 'cyan')}")
        print(f"{self._colorize(doc.get('title', 'Untitled'), 'bold green')}")
        print(f"{self._colorize('═' * 70, 'cyan')}\n")
        
        print(f"📄 路径: {doc.get('path', '')}")
        print(f"📁 分类: {doc.get('category', '')} / {doc.get('subcategory', '')}")
        print(f"📝 字数: {doc.get('word_count', 0)}")
        print(f"📅 修改: {doc.get('last_modified', '')}")
        
        # 关键词
        keywords = doc.get('keywords', [])
        if keywords:
            print(f"\n🔑 关键词: {', '.join(keywords[:15])}")
        
        # 摘要
        print(f"\n📋 摘要:\n{doc.get('summary', '')}")
        
        # 形式化元素
        formal_elems = doc.get('formal_elements', [])
        if formal_elems:
            print(f"\n📐 形式化元素 ({len(formal_elems)} 个):")
            by_type = defaultdict(list)
            for elem in formal_elems:
                by_type[elem.get('element_type', 'unknown')].append(elem)
            
            for elem_type, elems in sorted(by_type.items()):
                print(f"\n  [{elem_type.upper()}]:")
                for elem in elems:
                    print(f"    - {elem.get('id', '')}: {elem.get('name', '')}")
        
        # 文档结构
        headings = doc.get('headings', [])
        if headings:
            print(f"\n📑 文档结构:")
            for h in headings[:20]:  # 最多显示20个标题
                indent = "  " * (h.get('level', 1) - 1)
                print(f"{indent}{'#' * h.get('level', 1)} {h.get('text', '')}")
        
        print()


def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 搜索工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
搜索示例:
  # 基础关键词搜索
  python search.py "checkpoint"
  
  # 定理编号搜索
  python search.py "Thm-S-17-01"
  
  # 多关键词搜索（AND 模式）
  python search.py "checkpoint exactly-once" --operator AND
  
  # 按分类过滤
  python search.py "flink" --category Flink
  
  # 按形式化元素类型过滤
  python search.py "watermark" --type theorem
  
  # 显示更多详情
  python search.py "actor" --show-formal --highlight
  
  # 路径搜索
  python search.py "04-proofs" --path
  
  # 查看文档详情
  python search.py --doc "Struct/04-proofs/04.01-flink-checkpoint-correctness.md"
  
  # 列出统计信息
  python search.py --stats
        """
    )
    
    parser.add_argument('query', nargs='?', default='',
                        help='搜索查询')
    parser.add_argument('-c', '--category',
                        choices=['Struct', 'Knowledge', 'Flink', 'Root'],
                        help='按分类过滤')
    parser.add_argument('-t', '--type',
                        choices=['theorem', 'definition', 'lemma', 'proposition', 'corollary'],
                        help='按形式化元素类型过滤')
    parser.add_argument('-o', '--operator', default='OR',
                        choices=['AND', 'OR'],
                        help='多关键词操作符 (默认: OR)')
    parser.add_argument('-l', '--limit', type=int, default=20,
                        help='结果数量限制 (默认: 20)')
    parser.add_argument('--no-fuzzy', action='store_true',
                        help='禁用模糊匹配')
    parser.add_argument('--no-highlight', action='store_true',
                        help='禁用高亮显示')
    parser.add_argument('--show-formal', action='store_true',
                        help='显示相关形式化元素')
    parser.add_argument('--path', action='store_true',
                        help='按路径搜索模式')
    parser.add_argument('--doc',
                        help='查看指定文档的详细信息')
    parser.add_argument('--stats', action='store_true',
                        help='显示统计信息')
    parser.add_argument('--index', default='.vscode/search-index.json',
                        help='索引文件路径')
    parser.add_argument('--json', action='store_true',
                        help='以JSON格式输出结果')
    
    args = parser.parse_args()
    
    try:
        engine = SearchEngine(index_path=args.index)
    except FileNotFoundError as e:
        print(f"错误: {e}")
        return 1
    
    # 显示统计信息
    if args.stats:
        print("\n" + "=" * 50)
        print("📊 索引统计信息")
        print("=" * 50)
        print(f"文档总数: {engine.metadata.get('total_documents', 0)}")
        print(f"形式化元素: {engine.metadata.get('total_formal_elements', 0)}")
        print(f"索引条目: {engine.metadata.get('total_index_entries', 0)}")
        
        print("\n📁 分类分布:")
        for cat, count in sorted(engine.list_categories().items()):
            print(f"  - {cat}: {count}")
        
        print("\n📐 形式化元素类型:")
        for ftype, count in sorted(engine.list_formal_element_types().items()):
            print(f"  - {ftype}: {count}")
        
        return 0
    
    # 查看文档详情
    if args.doc:
        engine.print_document_detail(args.doc)
        return 0
    
    # 执行搜索
    if not args.query and not args.stats and not args.doc:
        parser.print_help()
        return 0
    
    if args.path:
        results = engine.search_by_path(args.query)
    else:
        results = engine.search(
            query=args.query,
            category=args.category,
            element_type=args.type,
            operator=args.operator,
            fuzzy=not args.no_fuzzy,
            limit=args.limit
        )
    
    # 输出结果
    if args.json:
        import json
        print(json.dumps([r.to_dict() for r in results], ensure_ascii=False, indent=2))
    else:
        engine.print_results(
            results,
            highlight=not args.no_highlight,
            show_formal=args.show_formal
        )
    
    return 0


if __name__ == '__main__':
    exit(main())
