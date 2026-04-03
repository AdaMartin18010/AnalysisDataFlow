#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 搜索索引构建脚本

功能：
- 扫描所有 .md 文件
- 提取标题、摘要、关键词
- 提取定理/定义/引理编号
- 生成 JSON 格式的搜索索引和倒排索引

用法：
    python build-search-index.py
    python build-search-index.py --output custom-index.json
    python build-search-index.py --verbose
"""

import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
from collections import defaultdict
import argparse


@dataclass
class FormalElement:
    """形式化元素（定理/定义/引理/命题/推论）"""
    id: str                          # 编号，如 Thm-S-01-01
    name: str                        # 名称
    element_type: str                # 类型: theorem, definition, lemma, proposition, corollary
    stage: str                       # 阶段: S/K/F
    doc_number: str                  # 文档序号
    sequence: str                    # 顺序号
    formal_level: str                # 形式化等级 L1-L6
    location: str                    # 所在位置/文档路径
    status: str = "✅"               # 状态


@dataclass
class Document:
    """文档条目"""
    path: str                        # 相对路径
    title: str                       # 文档标题
    summary: str                     # 摘要/简介
    category: str                    # 分类: Struct/Knowledge/Flink/Root
    subcategory: str                 # 子分类
    keywords: List[str] = field(default_factory=list)
    formal_elements: List[FormalElement] = field(default_factory=list)
    headings: List[Dict[str, Any]] = field(default_factory=list)  # 文档内的标题结构
    content_hash: str = ""           # 内容哈希，用于增量更新
    last_modified: str = ""          # 最后修改时间
    word_count: int = 0              # 字数统计
    line_count: int = 0              # 行数统计


@dataclass
class InvertedIndex:
    """倒排索引条目"""
    keyword: str
    doc_paths: List[str] = field(default_factory=list)
    formal_ids: List[str] = field(default_factory=list)
    tf_scores: Dict[str, float] = field(default_factory=dict)  # 词频得分


class SearchIndexBuilder:
    """搜索索引构建器"""
    
    # 形式化元素编号正则表达式
    FORMAL_ID_PATTERNS = {
        'theorem': re.compile(r'(Thm-[SKF]-\d{2}-\d{2,3})'),
        'definition': re.compile(r'(Def-[SKF]-\d{2}-\d{2,3})'),
        'lemma': re.compile(r'(Lemma-[SKF]-\d{2}-\d{2,3})'),
        'proposition': re.compile(r'(Prop-[SKF]-\d{2}-\d{2,3})'),
        'corollary': re.compile(r'(Cor-[SKF]-\d{2}-\d{2,3})'),
    }
    
    # 文档类型映射
    CATEGORY_MAP = {
        'Struct': ['Struct/', 'struct/'],
        'Knowledge': ['Knowledge/', 'knowledge/'],
        'Flink': ['Flink/', 'flink/'],
        'Root': [],  # 根目录文档
    }
    
    # 停用词
    STOP_WORDS = {
        '的', '了', '和', '是', '在', '有', '我', '都', '个', '与', '也', '对',
        '为', '能', '很', '可以', '就', '不', '会', '要', '没有', '我们', '这',
        '上', '他', '而', '及', '与', '或', '但', '等', 'the', 'a', 'an', 'is',
        'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
        'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
        'shall', 'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in', 'for',
        'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'under', 'and', 'but',
        'or', 'yet', 'so', 'if', 'because', 'although', 'though', 'while', 'where',
        'when', 'that', 'which', 'who', 'whom', 'whose', 'what', 'whatever',
        'this', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'them', 'their', 'there', 'then', 'than', 'here', 'just', 'only', 'own',
        'same', 'such', 'what', 'which', 'who', 'whom', 'whose', 'why', 'how',
        'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
        'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
        'very', 's', 't', 'don', 'should', 'now', 'using', 'use', 'used', 'based',
        'via', 'within', 'among', 'across', 'without', 'against', 'towards',
    }
    
    def __init__(self, root_dir: str = ".", verbose: bool = False):
        self.root_dir = Path(root_dir)
        self.verbose = verbose
        self.documents: Dict[str, Document] = {}
        self.formal_elements: Dict[str, FormalElement] = {}
        self.inverted_index: Dict[str, InvertedIndex] = {}
        self.keywords_index: Dict[str, Set[str]] = defaultdict(set)
        
    def log(self, message: str):
        """输出日志"""
        if self.verbose:
            print(f"[INDEX] {message}")
    
    def get_category(self, rel_path: str) -> Tuple[str, str]:
        """根据路径获取分类和子分类"""
        path_lower = rel_path.lower()
        
        for category, prefixes in self.CATEGORY_MAP.items():
            if category == 'Root':
                if '/' not in rel_path and '\\' not in rel_path:
                    return 'Root', 'root'
                continue
            for prefix in prefixes:
                if prefix.lower() in path_lower:
                    # 获取子分类（目录名）
                    parts = rel_path.replace('\\', '/').split('/')
                    if len(parts) > 1:
                        subcategory = parts[1] if len(parts) > 1 else 'general'
                        return category, subcategory
                    return category, 'general'
        
        return 'Other', 'general'
    
    def extract_title(self, content: str) -> str:
        """提取文档标题"""
        # 匹配 # 标题
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return "Untitled"
    
    def extract_summary(self, content: str, max_length: int = 300) -> str:
        """提取文档摘要"""
        # 移除 front matter (如果有)
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        
        # 尝试提取引言或第一段
        lines = content.split('\n')
        summary_lines = []
        
        for line in lines:
            line = line.strip()
            # 跳过标题、空行、代码块标记
            if line.startswith('#') or not line or line.startswith('```'):
                continue
            # 跳过表格、图片等
            if line.startswith('|') or line.startswith('![') or line.startswith('['):
                continue
            summary_lines.append(line)
            if len(''.join(summary_lines)) >= max_length:
                break
        
        summary = ' '.join(summary_lines)
        if len(summary) > max_length:
            summary = summary[:max_length-3] + '...'
        
        return summary if summary else "No summary available"
    
    def extract_headings(self, content: str) -> List[Dict[str, Any]]:
        """提取文档标题结构"""
        headings = []
        for match in re.finditer(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE):
            level = len(match.group(1))
            text = match.group(2).strip()
            # 提取可能的ID
            anchor_match = re.search(r'\{#([^}]+)\}$', text)
            anchor = anchor_match.group(1) if anchor_match else None
            text = re.sub(r'\{#[^}]+\}$', '', text).strip()
            
            headings.append({
                'level': level,
                'text': text,
                'anchor': anchor or self._slugify(text)
            })
        return headings
    
    def _slugify(self, text: str) -> str:
        """将文本转换为URL友好的slug"""
        text = re.sub(r'[^\w\s-]', '', text.lower())
        text = re.sub(r'[-\s]+', '-', text)
        return text[:50]
    
    def extract_formal_elements(self, content: str, rel_path: str) -> List[FormalElement]:
        """提取形式化元素（定理/定义/引理等）"""
        elements = []
        
        # 从表格中提取
        table_pattern = re.compile(
            r'\|\s*(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2,3})\s*\|\s*([^|]+)\|',
            re.MULTILINE
        )
        
        for match in table_pattern.finditer(content):
            elem_type_abbr = match.group(1)
            stage = match.group(2)
            doc_num = match.group(3)
            seq = match.group(4)
            name = match.group(5).strip()
            
            type_map = {
                'Thm': 'theorem',
                'Def': 'definition', 
                'Lemma': 'lemma',
                'Prop': 'proposition',
                'Cor': 'corollary'
            }
            
            element = FormalElement(
                id=f"{elem_type_abbr}-{stage}-{doc_num}-{seq}",
                name=name,
                element_type=type_map.get(elem_type_abbr, 'unknown'),
                stage=stage,
                doc_number=doc_num,
                sequence=seq,
                formal_level="L4",  # 默认值
                location=rel_path
            )
            elements.append(element)
            self.formal_elements[element.id] = element
        
        # 从行内标记提取
        inline_patterns = [
            (r'`(Thm-[SKF]-\d{2}-\d{2,3})`', 'theorem'),
            (r'`(Def-[SKF]-\d{2}-\d{2,3})`', 'definition'),
            (r'`(Lemma-[SKF]-\d{2}-\d{2,3})`', 'lemma'),
            (r'`(Prop-[SKF]-\d{2}-\d{2,3})`', 'proposition'),
            (r'`(Cor-[SKF]-\d{2}-\d{2,3})`', 'corollary'),
        ]
        
        for pattern, elem_type in inline_patterns:
            for match in re.finditer(pattern, content):
                elem_id = match.group(1)
                if elem_id not in self.formal_elements:
                    parts = elem_id.split('-')
                    if len(parts) == 4:
                        element = FormalElement(
                            id=elem_id,
                            name=elem_id,
                            element_type=elem_type,
                            stage=parts[1],
                            doc_number=parts[2],
                            sequence=parts[3],
                            formal_level="L4",
                            location=rel_path
                        )
                        elements.append(element)
                        self.formal_elements[elem_id] = element
        
        return elements
    
    def extract_keywords(self, content: str, title: str) -> List[str]:
        """提取关键词"""
        keywords = set()
        
        # 从内容中提取英文技术词汇
        tech_words = re.findall(r'\b[A-Z][a-zA-Z]{2,}\b', content)
        for word in tech_words:
            if word.lower() not in self.STOP_WORDS and len(word) > 2:
                keywords.add(word)
        
        # 提取连字符连接的技术术语
        hyphen_terms = re.findall(r'\b[a-z]+(-[a-z]+)+\b', content.lower())
        for term in hyphen_terms:
            keywords.add(term)
        
        # 提取下划线连接的技术术语
        underscore_terms = re.findall(r'\b[a-z]+(_[a-z]+)+\b', content.lower())
        for term in underscore_terms:
            keywords.add(term)
        
        # 从标题中提取
        title_words = re.findall(r'\w+', title)
        for word in title_words:
            if len(word) > 2:
                keywords.add(word.lower())
                keywords.add(word.capitalize())
        
        # 常见技术关键词（预定义）
        predefined_keywords = [
            'Flink', 'Dataflow', 'Actor', 'CSP', 'CCS', 'Pi-Calculus',
            'Checkpoint', 'Watermark', 'Exactly-Once', 'Backpressure',
            'Streaming', 'Stream', 'Batch', 'Real-time', 'Latency',
            'Determinism', 'Consistency', 'Liveness', 'Safety',
            'Type Safety', 'Progress', 'Preservation', 'Coq', 'TLA+',
            'Chandy-Lamport', 'USTM', 'Petri', 'Session Types',
            'Choreographic', 'pDOT', 'DOT', 'FG', 'FGG',
            'Rust', 'Go', 'Scala', 'Java', 'Python', 'WASM',
            'Kafka', 'Pulsar', 'Iceberg', 'Delta Lake', 'Hudi',
            'RAG', 'Vector', 'AI', 'ML', 'GPU', 'TEE',
            'SQL', 'Table API', 'DataStream', 'Process Function',
        ]
        
        for kw in predefined_keywords:
            if kw.lower() in content.lower():
                keywords.add(kw)
        
        return sorted(list(keywords))
    
    def tokenize(self, text: str) -> List[str]:
        """分词"""
        # 简单分词：按非字母数字字符分割
        tokens = re.findall(r'[a-zA-Z0-9\u4e00-\u9fff]+', text.lower())
        return [t for t in tokens if t not in self.STOP_WORDS and len(t) > 1]
    
    def build_inverted_index(self) -> Dict[str, InvertedIndex]:
        """构建倒排索引"""
        index: Dict[str, Dict[str, Any]] = defaultdict(lambda: {'docs': set(), 'formal_ids': set(), 'tf': defaultdict(int)})
        
        for doc_path, doc in self.documents.items():
            # 索引文档内容
            text = f"{doc.title} {doc.summary} {' '.join(doc.keywords)}"
            tokens = self.tokenize(text)
            
            token_count = len(tokens)
            token_freq = defaultdict(int)
            for token in tokens:
                token_freq[token] += 1
            
            for token, freq in token_freq.items():
                index[token]['docs'].add(doc_path)
                index[token]['tf'][doc_path] = freq / token_count if token_count > 0 else 0
            
            # 索引标题词（高权重）
            title_tokens = self.tokenize(doc.title)
            for token in title_tokens:
                index[token]['docs'].add(doc_path)
                index[token]['tf'][doc_path] = index[token]['tf'].get(doc_path, 0) + 2.0
            
            # 索引形式化元素
            for elem in doc.formal_elements:
                # 索引元素ID的各个部分
                parts = elem.id.lower().split('-')
                for part in parts:
                    index[part]['docs'].add(doc_path)
                    index[part]['formal_ids'].add(elem.id)
                
                # 索引元素名称
                name_tokens = self.tokenize(elem.name)
                for token in name_tokens:
                    index[token]['docs'].add(doc_path)
                    index[token]['formal_ids'].add(elem.id)
        
        # 转换为InvertedIndex对象
        result = {}
        for keyword, data in index.items():
            result[keyword] = InvertedIndex(
                keyword=keyword,
                doc_paths=sorted(list(data['docs'])),
                formal_ids=sorted(list(data['formal_ids'])),
                tf_scores=dict(data['tf'])
            )
        
        return result
    
    def process_file(self, file_path: Path) -> Optional[Document]:
        """处理单个文件"""
        try:
            rel_path = str(file_path.relative_to(self.root_dir)).replace('\\', '/')
            
            # 跳过某些文件
            if any(skip in rel_path.lower() for skip in ['node_modules', '.git', '__pycache__']):
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 计算内容哈希
            content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()[:16]
            
            # 提取信息
            title = self.extract_title(content)
            summary = self.extract_summary(content)
            category, subcategory = self.get_category(rel_path)
            keywords = self.extract_keywords(content, title)
            headings = self.extract_headings(content)
            formal_elements = self.extract_formal_elements(content, rel_path)
            
            # 统计
            word_count = len(content.split())
            line_count = len(content.split('\n'))
            
            # 修改时间
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            
            doc = Document(
                path=rel_path,
                title=title,
                summary=summary,
                category=category,
                subcategory=subcategory,
                keywords=keywords,
                formal_elements=formal_elements,
                headings=headings,
                content_hash=content_hash,
                last_modified=mtime,
                word_count=word_count,
                line_count=line_count
            )
            
            self.log(f"Processed: {rel_path} ({len(formal_elements)} formal elements)")
            return doc
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
    
    def scan_directory(self) -> List[Path]:
        """扫描目录获取所有md文件"""
        md_files = []
        for pattern in ['**/*.md', '**/*.MD']:
            md_files.extend(self.root_dir.glob(pattern))
        return [f for f in md_files if not any(skip in str(f) for skip in ['node_modules', '.git', '__pycache__'])]
    
    def build(self) -> Dict[str, Any]:
        """构建完整索引"""
        print("=" * 60)
        print("AnalysisDataFlow 搜索索引构建")
        print("=" * 60)
        
        # 扫描文件
        print("\n📁 扫描文档...")
        md_files = self.scan_directory()
        print(f"   找到 {len(md_files)} 个 Markdown 文件")
        
        # 处理文件
        print("\n📄 处理文档...")
        for file_path in md_files:
            doc = self.process_file(file_path)
            if doc:
                self.documents[doc.path] = doc
        
        print(f"   成功处理 {len(self.documents)} 个文档")
        print(f"   提取 {len(self.formal_elements)} 个形式化元素")
        
        # 构建倒排索引
        print("\n🔍 构建倒排索引...")
        self.inverted_index = self.build_inverted_index()
        print(f"   生成 {len(self.inverted_index)} 个索引条目")
        
        # 生成统计
        category_counts = defaultdict(int)
        for doc in self.documents.values():
            category_counts[doc.category] += 1
        
        formal_type_counts = defaultdict(int)
        for elem in self.formal_elements.values():
            formal_type_counts[elem.element_type] += 1
        
        # 组装结果
        result = {
            'metadata': {
                'version': '1.0',
                'build_date': datetime.now().isoformat(),
                'total_documents': len(self.documents),
                'total_formal_elements': len(self.formal_elements),
                'total_index_entries': len(self.inverted_index),
                'category_distribution': dict(category_counts),
                'formal_element_types': dict(formal_type_counts),
            },
            'documents': {path: asdict(doc) for path, doc in self.documents.items()},
            'formal_elements': {elem_id: asdict(elem) for elem_id, elem in self.formal_elements.items()},
            'inverted_index': {kw: asdict(idx) for kw, idx in self.inverted_index.items()},
        }
        
        print("\n📊 统计信息:")
        print(f"   文档总数: {result['metadata']['total_documents']}")
        for cat, count in sorted(category_counts.items()):
            print(f"   - {cat}: {count}")
        print(f"   形式化元素: {result['metadata']['total_formal_elements']}")
        for ftype, count in sorted(formal_type_counts.items()):
            print(f"   - {ftype}: {count}")
        
        return result
    
    def save(self, output_path: str):
        """保存索引到文件"""
        result = self.build()
        
        output_file = self.root_dir / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        file_size = output_file.stat().st_size / 1024  # KB
        print(f"\n✅ 索引已保存: {output_file}")
        print(f"   文件大小: {file_size:.1f} KB")
        
        return result


def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 搜索索引构建工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python build-search-index.py
  python build-search-index.py --output .vscode/search-index.json
  python build-search-index.py --verbose
  python build-search-index.py --root /path/to/project
        """
    )
    parser.add_argument('-o', '--output', default='.vscode/search-index.json',
                        help='输出文件路径 (默认: .vscode/search-index.json)')
    parser.add_argument('-r', '--root', default='.',
                        help='项目根目录 (默认: 当前目录)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='显示详细日志')
    
    args = parser.parse_args()
    
    builder = SearchIndexBuilder(root_dir=args.root, verbose=args.verbose)
    builder.save(args.output)


if __name__ == '__main__':
    main()
