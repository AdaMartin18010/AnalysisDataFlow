#!/usr/bin/env python3
"""
知识检索系统 (Knowledge Search Engine)
====================================
构建倒排索引，支持全文搜索和语义搜索，提供CLI和Web界面。

作者: Knowledge Graph Team
版本: 1.0.0
"""

import os
import re
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Any, Callable
from collections import defaultdict
import pickle
import hashlib

# 搜索库
try:
    from whoosh import index, scoring
    from whoosh.fields import Schema, TEXT, KEYWORD, ID, DATETIME, NUMERIC
    from whoosh.qparser import QueryParser, MultifieldParser
    from whoosh.query import Term, Or, And
    WHOOSH_AVAILABLE = True
except ImportError:
    WHOOSH_AVAILABLE = False

# BERT语义搜索
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    BERT_AVAILABLE = True
except ImportError:
    BERT_AVAILABLE = False
    np = None

# Web框架
try:
    from flask import Flask, request, jsonify, render_template_string
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """搜索结果数据结构"""
    doc_id: str
    title: str
    content_preview: str
    score: float
    highlights: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'doc_id': self.doc_id,
            'title': self.title,
            'content_preview': self.content_preview,
            'score': round(self.score, 4),
            'highlights': self.highlights,
            'metadata': self.metadata
        }


class DocumentIndexer:
    """文档索引器"""
    
    # 文档类型正则
    FORMAL_ID_PATTERN = re.compile(r'(Def|Thm|Lemma|Prop|Cor)-([SKF])-(\d+)-(\d+)')
    
    def __init__(self, index_dir: str, use_whoosh: bool = True):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.use_whoosh = use_whoosh and WHOOSH_AVAILABLE
        self.whoosh_index = None
        self.documents: Dict[str, Dict] = {}
        
        # 简单的内存索引（Whoosh不可用时）
        self.inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self.doc_term_freq: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        
        # BERT模型
        self.bert_model = None
        self.doc_embeddings: Dict[str, Any] = {}
        
        if self.use_whoosh:
            self._init_whoosh()
    
    def _init_whoosh(self):
        """初始化Whoosh索引"""
        if not WHOOSH_AVAILABLE:
            return
        
        schema = Schema(
            doc_id=ID(stored=True, unique=True),
            title=TEXT(stored=True, analyzer=scoring.BM25F.B()),
            content=TEXT(stored=True),
            content_clean=TEXT(stored=True),
            formal_ids=KEYWORD(stored=True, lowercase=True, commas=True),
            doc_type=KEYWORD(stored=True, lowercase=True),
            source_file=ID(stored=True),
            modified=DATETIME(stored=True),
            word_count=NUMERIC(stored=True),
            section_count=NUMERIC(stored=True)
        )
        
        if index.exists_in(str(self.index_dir)):
            self.whoosh_index = index.open_dir(str(self.index_dir))
            logger.info("已加载现有Whoosh索引")
        else:
            self.whoosh_index = index.create_in(str(self.index_dir), schema)
            logger.info("创建新的Whoosh索引")
    
    def load_bert_model(self, model_name: str = 'paraphrase-MiniLM-L3-v2'):
        """加载BERT模型用于语义搜索"""
        if not BERT_AVAILABLE:
            logger.warning("BERT不可用")
            return
        
        try:
            self.bert_model = SentenceTransformer(model_name)
            logger.info(f"BERT模型加载成功: {model_name}")
        except Exception as e:
            logger.error(f"BERT模型加载失败: {e}")
    
    def clean_content(self, content: str) -> str:
        """清理文档内容用于索引"""
        # 移除代码块
        content = re.sub(r'```[\s\S]*?```', ' ', content)
        # 移除行内代码
        content = re.sub(r'`[^`]+`', ' ', content)
        # 移除链接
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
        # 移除图片
        content = re.sub(r'!\[.*?\]\(.*?\)', ' ', content)
        # 移除URL
        content = re.sub(r'https?://\S+', ' ', content)
        # 规范化空白
        content = re.sub(r'\s+', ' ', content)
        return content.strip()
    
    def extract_formal_ids(self, content: str) -> List[str]:
        """提取形式化ID"""
        return [m.group(0) for m in self.FORMAL_ID_PATTERN.finditer(content)]
    
    def index_document(self, file_path: Path, base_path: Path) -> bool:
        """索引单个文档"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"无法读取文件 {file_path}: {e}")
            return False
        
        doc_id = str(file_path.relative_to(base_path))
        
        # 提取元数据
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem
        
        content_clean = self.clean_content(content)
        formal_ids = self.extract_formal_ids(content)
        
        # 确定文档类型
        doc_type = self._determine_doc_type(doc_id, content)
        
        # 统计信息
        word_count = len(content.split())
        section_count = len(re.findall(r'^#{2,4}\s+', content, re.MULTILINE))
        modified = datetime.fromtimestamp(file_path.stat().st_mtime)
        
        doc_data = {
            'doc_id': doc_id,
            'title': title,
            'content': content[:10000],  # 限制大小
            'content_clean': content_clean[:5000],
            'formal_ids': ','.join(formal_ids[:20]),
            'doc_type': doc_type,
            'source_file': doc_id,
            'modified': modified,
            'word_count': word_count,
            'section_count': section_count
        }
        
        self.documents[doc_id] = doc_data
        
        # Whoosh索引
        if self.use_whoosh and self.whoosh_index:
            writer = self.whoosh_index.writer()
            writer.update_document(**doc_data)
            writer.commit()
        
        # 内存索引
        self._update_inverted_index(doc_id, content_clean)
        
        # BERT嵌入
        if self.bert_model and BERT_AVAILABLE:
            try:
                embedding = self.bert_model.encode(f"{title}. {content_clean[:500]}")
                self.doc_embeddings[doc_id] = embedding
            except Exception as e:
                logger.warning(f"BERT嵌入失败 {doc_id}: {e}")
        
        return True
    
    def _determine_doc_type(self, doc_id: str, content: str) -> str:
        """确定文档类型"""
        if 'Struct/' in doc_id:
            return 'formal_theory'
        elif 'Knowledge/' in doc_id:
            return 'knowledge_guide'
        elif 'Flink/' in doc_id:
            return 'flink_reference'
        elif 'case' in doc_id.lower():
            return 'case_study'
        else:
            return 'general'
    
    def _update_inverted_index(self, doc_id: str, content: str):
        """更新倒排索引"""
        # 分词（简单实现）
        words = re.findall(r'\b[a-zA-Z]+\b|[\u4e00-\u9fff]', content.lower())
        
        for word in words:
            if len(word) > 1:
                self.inverted_index[word].add(doc_id)
                self.doc_term_freq[doc_id][word] += 1
    
    def index_directory(self, directory: Path, base_path: Path, pattern: str = "*.md"):
        """索引整个目录"""
        files = list(directory.rglob(pattern))
        logger.info(f"在 {directory} 中找到 {len(files)} 个文件")
        
        count = 0
        for file_path in files:
            if any(exclude in str(file_path) for exclude in ['README', 'CHANGELOG', 'INDEX']):
                continue
            
            if self.index_document(file_path, base_path):
                count += 1
                if count % 100 == 0:
                    logger.info(f"已索引 {count} 个文档")
        
        logger.info(f"索引完成: {count} 个文档")
        return count
    
    def save_index(self):
        """保存索引到磁盘"""
        index_data = {
            'documents': self.documents,
            'inverted_index': {k: list(v) for k, v in self.inverted_index.items()},
            'doc_term_freq': dict(self.doc_term_freq),
            'saved_at': datetime.now().isoformat()
        }
        
        # 保存JSON索引
        json_path = self.index_dir / 'search-index.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
        
        # 保存BERT嵌入
        if self.doc_embeddings:
            embeddings_path = self.index_dir / 'doc-embeddings.pkl'
            with open(embeddings_path, 'wb') as f:
                pickle.dump(self.doc_embeddings, f)
        
        logger.info(f"索引已保存到: {self.index_dir}")
    
    def load_index(self) -> bool:
        """从磁盘加载索引"""
        json_path = self.index_dir / 'search-index.json'
        if not json_path.exists():
            return False
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.documents = data.get('documents', {})
            self.inverted_index = defaultdict(set, {
                k: set(v) for k, v in data.get('inverted_index', {}).items()
            })
            self.doc_term_freq = defaultdict(
                lambda: defaultdict(int),
                {k: defaultdict(int, v) for k, v in data.get('doc_term_freq', {}).items()}
            )
            
            # 加载BERT嵌入
            embeddings_path = self.index_dir / 'doc-embeddings.pkl'
            if embeddings_path.exists():
                with open(embeddings_path, 'rb') as f:
                    self.doc_embeddings = pickle.load(f)
            
            logger.info(f"索引已加载: {len(self.documents)} 个文档")
            return True
            
        except Exception as e:
            logger.error(f"索引加载失败: {e}")
            return False


class SearchEngine:
    """搜索引擎"""
    
    def __init__(self, indexer: DocumentIndexer):
        self.indexer = indexer
    
    def search_fulltext(self, query: str, doc_type: Optional[str] = None, 
                        top_k: int = 10) -> List[SearchResult]:
        """全文搜索"""
        results = []
        
        if self.indexer.use_whoosh and self.indexer.whoosh_index:
            results = self._search_whoosh(query, doc_type, top_k)
        else:
            results = self._search_inverted_index(query, top_k)
        
        return results
    
    def _search_whoosh(self, query: str, doc_type: Optional[str], 
                       top_k: int) -> List[SearchResult]:
        """使用Whoosh搜索"""
        results = []
        
        try:
            with self.indexer.whoosh_index.searcher() as searcher:
                parser = MultifieldParser(
                    ['title', 'content_clean', 'formal_ids'],
                    schema=self.indexer.whoosh_index.schema
                )
                
                whoosh_query = parser.parse(query)
                
                # 添加类型过滤
                if doc_type:
                    whoosh_query = And([whoosh_query, Term('doc_type', doc_type)])
                
                hits = searcher.search(whoosh_query, limit=top_k * 2)
                
                for hit in hits[:top_k]:
                    result = SearchResult(
                        doc_id=hit['doc_id'],
                        title=hit['title'],
                        content_preview=hit.get('content', '')[:300],
                        score=hit.score,
                        highlights=hit.highlights('content_clean') or [],
                        metadata={
                            'doc_type': hit.get('doc_type', ''),
                            'word_count': hit.get('word_count', 0),
                            'formal_ids': hit.get('formal_ids', '').split(',')[:5]
                        }
                    )
                    results.append(result)
                    
        except Exception as e:
            logger.error(f"Whoosh搜索失败: {e}")
        
        return results
    
    def _search_inverted_index(self, query: str, top_k: int) -> List[SearchResult]:
        """使用倒排索引搜索"""
        # 分词
        query_words = re.findall(r'\b[a-zA-Z]+\b|[\u4e00-\u9fff]', query.lower())
        
        # 计算文档得分
        doc_scores: Dict[str, float] = defaultdict(float)
        
        for word in query_words:
            if word in self.indexer.inverted_index:
                for doc_id in self.indexer.inverted_index[word]:
                    # TF-IDF分数
                    tf = self.indexer.doc_term_freq[doc_id].get(word, 0)
                    idf = 1.0 / (1 + len(self.indexer.inverted_index[word]))
                    doc_scores[doc_id] += tf * idf
        
        # 排序并创建结果
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for doc_id, score in sorted_docs[:top_k]:
            doc = self.indexer.documents.get(doc_id, {})
            result = SearchResult(
                doc_id=doc_id,
                title=doc.get('title', ''),
                content_preview=doc.get('content_clean', '')[:300],
                score=score,
                metadata={
                    'doc_type': doc.get('doc_type', ''),
                    'word_count': doc.get('word_count', 0)
                }
            )
            results.append(result)
        
        return results
    
    def search_semantic(self, query: str, top_k: int = 10) -> List[SearchResult]:
        """语义搜索（使用BERT）"""
        if not BERT_AVAILABLE or self.indexer.bert_model is None:
            logger.warning("BERT不可用，回退到全文搜索")
            return self.search_fulltext(query, top_k=top_k)
        
        if not self.indexer.doc_embeddings:
            logger.warning("没有文档嵌入，回退到全文搜索")
            return self.search_fulltext(query, top_k=top_k)
        
        try:
            # 计算查询向量
            query_embedding = self.indexer.bert_model.encode(query)
            
            # 计算相似度
            doc_scores = []
            for doc_id, doc_embedding in self.indexer.doc_embeddings.items():
                if BERT_AVAILABLE and np is not None:
                    similarity = np.dot(query_embedding, doc_embedding) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
                    )
                    doc_scores.append((doc_id, float(similarity)))
            
            # 排序
            doc_scores.sort(key=lambda x: x[1], reverse=True)
            
            results = []
            for doc_id, score in doc_scores[:top_k]:
                doc = self.indexer.documents.get(doc_id, {})
                result = SearchResult(
                    doc_id=doc_id,
                    title=doc.get('title', ''),
                    content_preview=doc.get('content_clean', '')[:300],
                    score=score,
                    metadata={'search_type': 'semantic'}
                )
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"语义搜索失败: {e}")
            return self.search_fulltext(query, top_k=top_k)
    
    def search_hybrid(self, query: str, top_k: int = 10) -> List[SearchResult]:
        """混合搜索（全文 + 语义）"""
        # 获取全文搜索结果
        fulltext_results = self.search_fulltext(query, top_k=top_k)
        
        # 获取语义搜索结果
        semantic_results = self.search_semantic(query, top_k=top_k)
        
        # 合并结果
        merged: Dict[str, SearchResult] = {}
        
        for result in fulltext_results:
            merged[result.doc_id] = result
            merged[result.doc_id].score *= 0.5  # 权重
        
        for result in semantic_results:
            if result.doc_id in merged:
                merged[result.doc_id].score += result.score * 0.5
            else:
                result.score *= 0.5
                merged[result.doc_id] = result
        
        # 排序
        final_results = sorted(merged.values(), key=lambda x: x.score, reverse=True)
        return final_results[:top_k]
    
    def search_by_formal_id(self, formal_id: str) -> Optional[SearchResult]:
        """按形式化ID搜索"""
        # 在文档中查找包含该ID的文档
        for doc_id, doc in self.indexer.documents.items():
            if formal_id in doc.get('formal_ids', ''):
                return SearchResult(
                    doc_id=doc_id,
                    title=doc.get('title', ''),
                    content_preview=doc.get('content', '')[:300],
                    score=1.0,
                    metadata={'formal_ids': [formal_id]}
                )
        return None
    
    def generate_summary(self, query: str, results: List[SearchResult]) -> str:
        """生成搜索结果摘要"""
        if not results:
            return f"未找到与 '{query}' 相关的结果。"
        
        summary = f"找到 {len(results)} 个相关结果:\n\n"
        
        for i, result in enumerate(results[:5], 1):
            summary += f"{i}. {result.title}\n"
            summary += f"   路径: {result.doc_id}\n"
            summary += f"   相关度: {result.score:.2%}\n"
            if result.highlights:
                summary += f"   摘要: ...{result.highlights[0][:150]}...\n"
            summary += "\n"
        
        return summary


class CLISearch:
    """命令行搜索界面"""
    
    def __init__(self, search_engine: SearchEngine):
        self.search_engine = search_engine
    
    def run(self):
        """运行CLI交互"""
        print("\n" + "=" * 70)
        print("知识检索系统 (Knowledge Search Engine)")
        print("=" * 70)
        print("\n命令:")
        print("  /quit, /q    - 退出")
        print("  /help, /h    - 显示帮助")
        print("  /semantic, /s - 切换语义搜索")
        print("  /hybrid, /y   - 切换混合搜索")
        print("  /type <type>  - 按类型过滤 (formal_theory, knowledge_guide, flink_reference)")
        print("\n输入查询内容开始搜索...\n")
        
        search_mode = 'fulltext'
        doc_type = None
        
        while True:
            try:
                query = input("search> ").strip()
                
                if not query:
                    continue
                
                if query in ['/quit', '/q']:
                    print("再见!")
                    break
                
                if query in ['/help', '/h']:
                    self._show_help()
                    continue
                
                if query in ['/semantic', '/s']:
                    search_mode = 'semantic'
                    print("已切换到语义搜索模式")
                    continue
                
                if query in ['/hybrid', '/y']:
                    search_mode = 'hybrid'
                    print("已切换到混合搜索模式")
                    continue
                
                if query.startswith('/type '):
                    doc_type = query[6:].strip() or None
                    print(f"文档类型过滤: {doc_type or '无'}")
                    continue
                
                # 执行搜索
                print(f"\n正在搜索: '{query}' (模式: {search_mode})...\n")
                
                if search_mode == 'semantic':
                    results = self.search_engine.search_semantic(query)
                elif search_mode == 'hybrid':
                    results = self.search_engine.search_hybrid(query)
                else:
                    results = self.search_engine.search_fulltext(query, doc_type)
                
                # 显示结果
                self._display_results(results)
                
            except KeyboardInterrupt:
                print("\n再见!")
                break
            except Exception as e:
                print(f"错误: {e}")
    
    def _show_help(self):
        """显示帮助信息"""
        print("""
搜索帮助:
-----------
1. 全文搜索: 直接输入关键词，如 "checkpoint 容错"
2. 语义搜索: 使用 /semantic 后输入自然语言查询
3. 混合搜索: 使用 /hybrid 结合两种搜索方式
4. 类型过滤: 使用 /type formal_theory 只搜索形式理论文档

搜索技巧:
- 使用引号进行精确匹配: "exact phrase"
- 使用 AND/OR 进行布尔查询: "flink AND checkpoint"
- 按形式化ID搜索: Thm-S-01-01
        """)
    
    def _display_results(self, results: List[SearchResult]):
        """显示搜索结果"""
        if not results:
            print("未找到相关结果。")
            return
        
        print(f"找到 {len(results)} 个结果:\n")
        
        for i, result in enumerate(results, 1):
            print(f"[{i}] {result.title}")
            print(f"    路径: {result.doc_id}")
            print(f"    相关度: {result.score:.2%}")
            
            if result.metadata.get('formal_ids'):
                print(f"    形式化ID: {', '.join(result.metadata['formal_ids'][:3])}")
            
            preview = result.content_preview[:200].replace('\n', ' ')
            print(f"    {preview}...\n")


class WebSearch:
    """Web搜索界面（Flask）"""
    
    HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>知识检索系统</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
        .search-box { display: flex; gap: 10px; margin: 20px 0; }
        input[type="text"] { flex: 1; padding: 12px; font-size: 16px; border: 1px solid #ddd; border-radius: 4px; }
        select { padding: 12px; font-size: 16px; border: 1px solid #ddd; border-radius: 4px; }
        button { padding: 12px 24px; font-size: 16px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #45a049; }
        .stats { color: #666; font-size: 14px; margin: 10px 0; }
        .result { background: white; padding: 15px; margin: 10px 0; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .result-title { font-size: 18px; font-weight: bold; color: #1a0dab; margin-bottom: 5px; }
        .result-path { color: #006621; font-size: 14px; margin-bottom: 5px; }
        .result-preview { color: #545454; line-height: 1.5; }
        .result-meta { color: #999; font-size: 12px; margin-top: 8px; }
        .score { color: #ff6b6b; font-weight: bold; }
        .badge { display: inline-block; padding: 2px 8px; background: #e3f2fd; color: #1976d2; border-radius: 12px; font-size: 12px; margin-right: 5px; }
        .no-results { text-align: center; color: #666; padding: 40px; }
        .loading { text-align: center; color: #666; padding: 20px; }
    </style>
</head>
<body>
    <h1>🔍 知识检索系统</h1>
    
    <form action="/search" method="GET" class="search-box">
        <input type="text" name="q" value="{{ query }}" placeholder="输入搜索关键词..." required>
        <select name="mode">
            <option value="fulltext" {% if mode == 'fulltext' %}selected{% endif %}>全文搜索</option>
            <option value="semantic" {% if mode == 'semantic' %}selected{% endif %}>语义搜索</option>
            <option value="hybrid" {% if mode == 'hybrid' %}selected{% endif %}>混合搜索</option>
        </select>
        <select name="type">
            <option value="">所有类型</option>
            <option value="formal_theory" {% if doc_type == 'formal_theory' %}selected{% endif %}>形式理论</option>
            <option value="knowledge_guide" {% if doc_type == 'knowledge_guide' %}selected{% endif %}>知识指南</option>
            <option value="flink_reference" {% if doc_type == 'flink_reference' %}selected{% endif %}>Flink参考</option>
        </select>
        <button type="submit">搜索</button>
    </form>
    
    {% if results is not none %}
    <div class="stats">找到 {{ results|length }} 个结果</div>
    
    {% if results %}
        {% for result in results %}
        <div class="result">
            <div class="result-title">{{ result.title }}</div>
            <div class="result-path">{{ result.doc_id }}</div>
            <div class="result-preview">{{ result.content_preview[:300] }}...</div>
            <div class="result-meta">
                <span class="score">相关度: {{ "%.1f"|format(result.score * 100) }}%</span>
                {% if result.metadata.doc_type %}
                <span class="badge">{{ result.metadata.doc_type }}</span>
                {% endif %}
                {% if result.metadata.formal_ids %}
                <span class="badge">{{ result.metadata.formal_ids[0] }}</span>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    {% else %}
        <div class="no-results">未找到相关结果</div>
    {% endif %}
    {% endif %}
    
    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #999; font-size: 12px; text-align: center;">
        知识检索系统 v1.0 | 支持全文搜索、语义搜索、混合搜索
    </div>
</body>
</html>
    '''
    
    def __init__(self, search_engine: SearchEngine, host: str = '0.0.0.0', port: int = 5000):
        self.search_engine = search_engine
        self.host = host
        self.port = port
        self.app = Flask(__name__) if FLASK_AVAILABLE else None
        
        if self.app:
            self._setup_routes()
    
    def _setup_routes(self):
        """设置路由"""
        @self.app.route('/')
        def index():
            from flask import render_template_string
            return render_template_string(self.HTML_TEMPLATE, results=None, query='', mode='fulltext', doc_type='')
        
        @self.app.route('/search')
        def search():
            from flask import render_template_string, request
            
            query = request.args.get('q', '')
            mode = request.args.get('mode', 'fulltext')
            doc_type = request.args.get('type', '') or None
            
            if not query:
                return render_template_string(self.HTML_TEMPLATE, results=[], query='', mode=mode, doc_type=doc_type or '')
            
            # 执行搜索
            if mode == 'semantic':
                results = self.search_engine.search_semantic(query)
            elif mode == 'hybrid':
                results = self.search_engine.search_hybrid(query)
            else:
                results = self.search_engine.search_fulltext(query, doc_type)
            
            # 转换为字典
            result_dicts = [r.to_dict() for r in results]
            
            return render_template_string(
                self.HTML_TEMPLATE,
                results=result_dicts,
                query=query,
                mode=mode,
                doc_type=doc_type or ''
            )
        
        @self.app.route('/api/search')
        def api_search():
            from flask import request, jsonify
            
            query = request.args.get('q', '')
            mode = request.args.get('mode', 'fulltext')
            top_k = int(request.args.get('k', 10))
            
            if not query:
                return jsonify({'error': 'Empty query'}), 400
            
            if mode == 'semantic':
                results = self.search_engine.search_semantic(query, top_k)
            elif mode == 'hybrid':
                results = self.search_engine.search_hybrid(query, top_k)
            else:
                results = self.search_engine.search_fulltext(query, top_k=top_k)
            
            return jsonify({
                'query': query,
                'mode': mode,
                'count': len(results),
                'results': [r.to_dict() for r in results]
            })
    
    def run(self, debug: bool = False):
        """运行Web服务器"""
        if not FLASK_AVAILABLE:
            logger.error("Flask不可用，无法启动Web界面")
            return
        
        print(f"\n启动Web服务器...")
        print(f"访问地址: http://{self.host}:{self.port}")
        print(f"按Ctrl+C停止服务器\n")
        
        self.app.run(host=self.host, port=self.port, debug=debug)


class KnowledgeSearchSystem:
    """知识检索系统主类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_path = Path(config.get('base_path', '.'))
        self.index_dir = Path(config.get('index_dir', '.scripts/knowledge-graph/index'))
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        self.indexer = None
        self.search_engine = None
    
    def build_index(self):
        """构建索引"""
        logger.info("=" * 70)
        logger.info("构建知识检索索引")
        logger.info("=" * 70)
        
        use_whoosh = self.config.get('use_whoosh', True) and WHOOSH_AVAILABLE
        self.indexer = DocumentIndexer(str(self.index_dir), use_whoosh=use_whoosh)
        
        # 加载BERT模型（如果启用）
        if self.config.get('use_semantic', True):
            self.indexer.load_bert_model()
        
        # 索引目录
        directories = self.config.get('source_directories', ['Struct', 'Knowledge', 'Flink'])
        for directory in directories:
            dir_path = self.base_path / directory
            if dir_path.exists():
                self.indexer.index_directory(dir_path, self.base_path)
        
        # 保存索引
        self.indexer.save_index()
        
        logger.info("索引构建完成!")
    
    def load_index(self) -> bool:
        """加载索引"""
        use_whoosh = self.config.get('use_whoosh', True) and WHOOSH_AVAILABLE
        self.indexer = DocumentIndexer(str(self.index_dir), use_whoosh=use_whoosh)
        
        if self.indexer.load_index():
            # 加载BERT模型
            if self.config.get('use_semantic', True):
                self.indexer.load_bert_model()
            return True
        return False
    
    def run_cli(self):
        """运行CLI界面"""
        if self.search_engine is None:
            self.search_engine = SearchEngine(self.indexer)
        
        cli = CLISearch(self.search_engine)
        cli.run()
    
    def run_web(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """运行Web界面"""
        if self.search_engine is None:
            self.search_engine = SearchEngine(self.indexer)
        
        web = WebSearch(self.search_engine, host, port)
        web.run(debug=debug)


def load_config(config_path: str) -> Dict[str, Any]:
    """加载配置文件"""
    default_config = {
        'base_path': '.',
        'index_dir': '.scripts/knowledge-graph/index',
        'output_dir': '.scripts/knowledge-graph/output',
        'source_directories': ['Struct', 'Knowledge', 'Flink'],
        'use_whoosh': True,
        'use_semantic': True,
        'web_host': '0.0.0.0',
        'web_port': 5000
    }
    
    config_file = Path(config_path)
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            default_config.update(user_config)
        except Exception as e:
            logger.warning(f"配置文件加载失败: {e}")
    
    return default_config


def main():
    parser = argparse.ArgumentParser(
        description='知识检索系统 - 全文搜索和语义搜索'
    )
    parser.add_argument(
        '-c', '--config',
        default='.scripts/knowledge-graph/config.json',
        help='配置文件路径'
    )
    parser.add_argument(
        'command',
        choices=['index', 'cli', 'web'],
        help='命令: index=构建索引, cli=命令行界面, web=Web界面'
    )
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Web服务器主机地址'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Web服务器端口'
    )
    parser.add_argument(
        '--no-semantic',
        action='store_true',
        help='禁用语义搜索'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细日志'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    config = load_config(args.config)
    
    if args.no_semantic:
        config['use_semantic'] = False
    
    system = KnowledgeSearchSystem(config)
    
    if args.command == 'index':
        system.build_index()
    
    elif args.command == 'cli':
        if not system.load_index():
            print("索引不存在，请先运行 'index' 命令构建索引")
            return
        system.run_cli()
    
    elif args.command == 'web':
        if not system.load_index():
            print("索引不存在，请先运行 'index' 命令构建索引")
            return
        system.run_web(host=args.host, port=args.port)


if __name__ == '__main__':
    main()
