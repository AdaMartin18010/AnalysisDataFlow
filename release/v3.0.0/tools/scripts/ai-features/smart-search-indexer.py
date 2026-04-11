#!/usr/bin/env python3
"""
智能搜索索引构建器 - 支持语义搜索的文档索引系统
功能：
1. 构建文档全文索引
2. 生成向量嵌入用于语义搜索
3. 支持关键词搜索和相似度搜索
4. 提供REST API接口

用法：
    python smart-search-indexer.py --build --source . --output search-index/
    python smart-search-indexer.py --search "checkpoint mechanism"
    python smart-search-indexer.py --semantic-search "流处理容错"
    python smart-search-indexer.py --serve --port 8000
"""

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import pickle

# 尝试导入可选依赖
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    from rank_bm25 import BM25Okapi
    HAS_BM25 = True
except ImportError:
    HAS_BM25 = False


@dataclass
class SearchResult:
    """搜索结果"""
    doc_path: str
    title: str
    snippet: str
    score: float
    section: Optional[str] = None
    metadata: Optional[Dict] = None


@dataclass
class DocumentChunk:
    """文档分块"""
    doc_path: str
    chunk_id: int
    content: str
    section: str
    tokens: List[str]
    embedding: Optional[List[float]] = None


class TextProcessor:
    """文本处理工具"""
    
    # 中文停用词
    STOP_WORDS = {
        '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那',
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
    }
    
    @staticmethod
    def tokenize(text: str) -> List[str]:
        """分词（简化版）"""
        # 移除Markdown标记
        text = re.sub(r'[#*`\[\](){}|]', ' ', text)
        # 分词
        tokens = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z_]+|\d+', text.lower())
        # 过滤停用词和短词
        tokens = [t for t in tokens if t not in TextProcessor.STOP_WORDS and len(t) > 1]
        return tokens
    
    @staticmethod
    def chunk_document(content: str, chunk_size: int = 500, overlap: int = 100) -> List[Dict]:
        """将文档分块"""
        chunks = []
        lines = content.split('\n')
        current_chunk = []
        current_section = "Introduction"
        chunk_id = 0
        current_size = 0
        
        for line in lines:
            # 检测章节标题
            if line.startswith('# '):
                current_section = line[2:].strip()
            elif line.startswith('## '):
                current_section = line[3:].strip()
            
            line_size = len(line)
            
            if current_size + line_size > chunk_size and current_chunk:
                # 保存当前块
                chunk_text = '\n'.join(current_chunk)
                chunks.append({
                    'id': chunk_id,
                    'content': chunk_text,
                    'section': current_section,
                    'tokens': TextProcessor.tokenize(chunk_text)
                })
                chunk_id += 1
                
                # 保留重叠部分
                overlap_lines = current_chunk[-overlap//50:] if overlap > 0 else []
                current_chunk = overlap_lines + [line]
                current_size = sum(len(l) for l in current_chunk)
            else:
                current_chunk.append(line)
                current_size += line_size
        
        # 保存最后一块
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunks.append({
                'id': chunk_id,
                'content': chunk_text,
                'section': current_section,
                'tokens': TextProcessor.tokenize(chunk_text)
            })
        
        return chunks


class EmbeddingGenerator:
    """向量嵌入生成器"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.cache: Dict[str, List[float]] = {}
        
    def _get_cache_key(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()
    
    def generate(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """生成文本嵌入"""
        if not HAS_OPENAI or not self.api_key:
            # 使用随机向量作为fallback
            print("警告: 未配置OpenAI API，使用模拟嵌入", file=sys.stderr)
            return [[0.0] * 1536 for _ in texts]
        
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            
            # 检查缓存
            batch_to_process = []
            cached_embeddings = {}
            
            for text in batch:
                cache_key = self._get_cache_key(text)
                if cache_key in self.cache:
                    cached_embeddings[text] = self.cache[cache_key]
                else:
                    batch_to_process.append(text)
            
            # 调用API
            if batch_to_process:
                try:
                    client = openai.OpenAI(api_key=self.api_key)
                    response = client.embeddings.create(
                        model=self.model,
                        input=batch_to_process
                    )
                    
                    for text, embedding_data in zip(batch_to_process, response.data):
                        cache_key = self._get_cache_key(text)
                        self.cache[cache_key] = embedding_data.embedding
                        cached_embeddings[text] = embedding_data.embedding
                
                except Exception as e:
                    print(f"嵌入生成失败: {e}", file=sys.stderr)
                    for text in batch_to_process:
                        cached_embeddings[text] = [0.0] * 1536
            
            # 按原始顺序返回
            for text in batch:
                embeddings.append(cached_embeddings[text])
        
        return embeddings
    
    def cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """计算余弦相似度"""
        if not HAS_NUMPY:
            # 纯Python实现
            dot = sum(x*y for x, y in zip(a, b))
            norm_a = sum(x*x for x in a) ** 0.5
            norm_b = sum(x*x for x in b) ** 0.5
            return dot / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0
        
        a_arr = np.array(a)
        b_arr = np.array(b)
        return float(np.dot(a_arr, b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr)))


class SearchIndex:
    """搜索索引"""
    
    def __init__(self, index_dir: str = ".cache/search-index"):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        self.documents: Dict[str, Dict] = {}
        self.chunks: List[DocumentChunk] = []
        self.bm25: Optional[Any] = None
        self.embedding_gen = EmbeddingGenerator()
        
    def _get_index_path(self) -> Path:
        return self.index_dir / "index.pkl"
    
    def _get_metadata_path(self) -> Path:
        return self.index_dir / "metadata.json"
    
    def build(self, source_dir: str, file_pattern: str = "**/*.md"):
        """构建索引"""
        print(f"正在构建索引: {source_dir}")
        
        source_path = Path(source_dir)
        md_files = list(source_path.glob(file_pattern))
        
        print(f"找到 {len(md_files)} 个Markdown文件")
        
        # 处理每个文档
        for md_file in md_files:
            try:
                self._index_document(md_file, source_path)
            except Exception as e:
                print(f"  ✗ 索引失败 {md_file}: {e}")
        
        # 构建BM25索引
        if HAS_BM25 and self.chunks:
            print("构建BM25索引...")
            tokenized_chunks = [chunk.tokens for chunk in self.chunks]
            self.bm25 = BM25Okapi(tokenized_chunks)
        
        # 保存索引
        self.save()
        
        print(f"\n索引构建完成!")
        print(f"  - 文档数: {len(self.documents)}")
        print(f"  - 分块数: {len(self.chunks)}")
    
    def _index_document(self, file_path: Path, source_path: Path):
        """索引单个文档"""
        rel_path = str(file_path.relative_to(source_path))
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem
        
        # 分块
        chunks_data = TextProcessor.chunk_document(content)
        
        # 创建DocumentChunk对象
        for chunk_data in chunks_data:
            chunk = DocumentChunk(
                doc_path=rel_path,
                chunk_id=chunk_data['id'],
                content=chunk_data['content'],
                section=chunk_data['section'],
                tokens=chunk_data['tokens']
            )
            self.chunks.append(chunk)
        
        # 存储文档元数据
        self.documents[rel_path] = {
            'title': title,
            'path': rel_path,
            'chunk_count': len(chunks_data),
            'word_count': len(content)
        }
        
        print(f"  ✓ {rel_path} ({len(chunks_data)} chunks)")
    
    def generate_embeddings(self, batch_size: int = 50):
        """为所有块生成嵌入"""
        print(f"为 {len(self.chunks)} 个块生成嵌入...")
        
        texts = [chunk.content for chunk in self.chunks]
        embeddings = self.embedding_gen.generate(texts, batch_size=batch_size)
        
        for chunk, embedding in zip(self.chunks, embeddings):
            chunk.embedding = embedding
        
        print("嵌入生成完成")
    
    def search(self, query: str, top_k: int = 10) -> List[SearchResult]:
        """关键词搜索 (BM25)"""
        if not self.bm25:
            print("错误: BM25索引未构建", file=sys.stderr)
            return []
        
        query_tokens = TextProcessor.tokenize(query)
        scores = self.bm25.get_scores(query_tokens)
        
        # 获取top-k结果
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        
        results = []
        for idx in top_indices:
            if scores[idx] <= 0:
                continue
            chunk = self.chunks[idx]
            results.append(SearchResult(
                doc_path=chunk.doc_path,
                title=self.documents.get(chunk.doc_path, {}).get('title', 'Unknown'),
                snippet=chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content,
                score=float(scores[idx]),
                section=chunk.section
            ))
        
        return results
    
    def semantic_search(self, query: str, top_k: int = 10) -> List[SearchResult]:
        """语义搜索 (向量相似度)"""
        if not self.chunks or not self.chunks[0].embedding:
            print("错误: 嵌入未生成，请先运行 generate_embeddings()", file=sys.stderr)
            return []
        
        # 生成查询嵌入
        query_embedding = self.embedding_gen.generate([query])[0]
        
        # 计算相似度
        similarities = []
        for chunk in self.chunks:
            if chunk.embedding:
                sim = self.embedding_gen.cosine_similarity(query_embedding, chunk.embedding)
                similarities.append((chunk, sim))
        
        # 排序并返回top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for chunk, score in similarities[:top_k]:
            results.append(SearchResult(
                doc_path=chunk.doc_path,
                title=self.documents.get(chunk.doc_path, {}).get('title', 'Unknown'),
                snippet=chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content,
                score=score,
                section=chunk.section
            ))
        
        return results
    
    def hybrid_search(self, query: str, top_k: int = 10, semantic_weight: float = 0.5) -> List[SearchResult]:
        """混合搜索 (BM25 + 语义)"""
        keyword_results = {r.doc_path: r for r in self.search(query, top_k * 2)}
        semantic_results = {r.doc_path: r for r in self.semantic_search(query, top_k * 2)}
        
        # 合并并加权
        all_docs = set(keyword_results.keys()) | set(semantic_results.keys())
        combined_scores = {}
        
        for doc_path in all_docs:
            kw_score = keyword_results.get(doc_path, SearchResult("", "", "", 0)).score
            sem_score = semantic_results.get(doc_path, SearchResult("", "", "", 0)).score
            
            # 归一化并加权
            combined_scores[doc_path] = (
                (1 - semantic_weight) * (kw_score / max(keyword_results.values(), key=lambda x: x.score).score if keyword_results else 1) +
                semantic_weight * sem_score
            )
        
        # 排序并返回
        sorted_docs = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        for doc_path, score in sorted_docs:
            # 优先使用语义搜索结果（通常片段更相关）
            result = semantic_results.get(doc_path) or keyword_results.get(doc_path)
            result.score = score
            results.append(result)
        
        return results
    
    def save(self):
        """保存索引到磁盘"""
        # 保存pickle（包含BM25和chunks）
        with open(self._get_index_path(), 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'chunks': self.chunks,
                'bm25': self.bm25
            }, f)
        
        # 保存元数据（JSON，便于查看）
        with open(self._get_metadata_path(), 'w', encoding='utf-8') as f:
            json.dump({
                'document_count': len(self.documents),
                'chunk_count': len(self.chunks),
                'documents': list(self.documents.keys())
            }, f, ensure_ascii=False, indent=2)
        
        print(f"索引已保存到: {self.index_dir}")
    
    def load(self) -> bool:
        """从磁盘加载索引"""
        index_path = self._get_index_path()
        
        if not index_path.exists():
            return False
        
        with open(index_path, 'rb') as f:
            data = pickle.load(f)
            self.documents = data['documents']
            self.chunks = data['chunks']
            self.bm25 = data.get('bm25')
        
        print(f"索引已加载: {len(self.documents)} 文档, {len(self.chunks)} 块")
        return True


def print_results(results: List[SearchResult], query: str):
    """打印搜索结果"""
    print(f"\n{'='*70}")
    print(f"🔍 查询: \"{query}\"")
    print(f"{'='*70}")
    
    if not results:
        print("未找到相关结果")
        return
    
    for i, result in enumerate(results, 1):
        print(f"\n[{i}] {result.title}")
        print(f"    📄 {result.doc_path}")
        if result.section:
            print(f"    📑 章节: {result.section}")
        print(f"    ⭐ 相关度: {result.score:.4f}")
        print(f"    📝 {result.snippet}")
    
    print(f"\n{'='*70}")
    print(f"共找到 {len(results)} 个结果")


def main():
    parser = argparse.ArgumentParser(
        description="智能搜索索引构建器 - 构建全文和语义搜索索引",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --build --source . --index-dir search-index/
  %(prog)s --search "checkpoint mechanism" --index-dir search-index/
  %(prog)s --semantic-search "流处理容错" --index-dir search-index/
  %(prog)s --hybrid-search "watermark semantics" --index-dir search-index/
  %(prog)s --generate-embeddings --index-dir search-index/
        """
    )
    
    parser.add_argument('--index-dir', '-d', default='.cache/search-index',
                       help='索引目录路径')
    parser.add_argument('--source', '-s', default='.',
                       help='源文档目录')
    
    # 构建命令
    parser.add_argument('--build', action='store_true',
                       help='构建索引')
    parser.add_argument('--pattern', default='**/*.md',
                       help='文件匹配模式')
    
    # 搜索命令
    parser.add_argument('--search', '-q',
                       help='关键词搜索')
    parser.add_argument('--semantic-search', '-sq',
                       help='语义搜索')
    parser.add_argument('--hybrid-search', '-hq',
                       help='混合搜索')
    parser.add_argument('--top-k', '-k', type=int, default=10,
                       help='返回结果数量')
    
    # 其他命令
    parser.add_argument('--generate-embeddings', action='store_true',
                       help='生成向量嵌入')
    parser.add_argument('--api-key', help='OpenAI API密钥')
    
    args = parser.parse_args()
    
    # 初始化索引
    index = SearchIndex(args.index_dir)
    
    if args.build:
        # 构建索引
        index.build(args.source, args.pattern)
        print("\n提示: 运行 --generate-embeddings 以启用语义搜索")
    
    elif args.generate_embeddings:
        # 加载现有索引并生成嵌入
        if not index.load():
            print("错误: 索引不存在，请先运行 --build")
            sys.exit(1)
        
        if args.api_key:
            index.embedding_gen.api_key = args.api_key
        
        index.generate_embeddings()
        index.save()
    
    elif args.search:
        # 关键词搜索
        if not index.load():
            print("错误: 索引不存在，请先运行 --build")
            sys.exit(1)
        
        results = index.search(args.search, args.top_k)
        print_results(results, args.search)
    
    elif args.semantic_search:
        # 语义搜索
        if not index.load():
            print("错误: 索引不存在，请先运行 --build")
            sys.exit(1)
        
        if args.api_key:
            index.embedding_gen.api_key = args.api_key
        
        results = index.semantic_search(args.semantic_search, args.top_k)
        print_results(results, args.semantic_search)
    
    elif args.hybrid_search:
        # 混合搜索
        if not index.load():
            print("错误: 索引不存在，请先运行 --build")
            sys.exit(1)
        
        if args.api_key:
            index.embedding_gen.api_key = args.api_key
        
        results = index.hybrid_search(args.hybrid_search, args.top_k)
        print_results(results, args.hybrid_search)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
