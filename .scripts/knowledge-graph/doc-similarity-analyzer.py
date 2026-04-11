#!/usr/bin/env python3
"""
文档相似度分析器 (Document Similarity Analyzer)
=============================================
使用TF-IDF和BERT嵌入计算文档相似度，检测重复内容，推荐相关文档。

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
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Set, Tuple, Optional, Any, Callable
from collections import defaultdict
import heapq

# 机器学习库
SKLEARN_AVAILABLE = False
BERT_AVAILABLE = False

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
SKLEARN_AVAILABLE = True

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    BERT_AVAILABLE = True
except ImportError:
    np = None
    pass


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Document:
    """文档数据结构"""
    id: str
    path: str
    title: str
    content: str
    cleaned_content: str = ""
    word_count: int = 0
    section_count: int = 0
    embeddings: Optional[Any] = None
    tfidf_vector: Optional[Any] = None
    cluster_id: int = -1
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'path': self.path,
            'title': self.title,
            'word_count': self.word_count,
            'section_count': self.section_count,
            'cluster_id': self.cluster_id
        }


class TextPreprocessor:
    """文本预处理器"""
    
    # 停用词（中英文）
    STOP_WORDS = set([
        # 中文停用词
        '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也',
        '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那',
        '这个', '那个', '这里', '那里', '这样', '那样', '如何', '什么', '为什么', '怎么', '如果',
        # 英文停用词
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
        'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
        'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their'
    ])
    
    # Markdown语法模式
    MARKDOWN_PATTERNS = [
        (r'!\[.*?\]\(.*?\)', ''),  # 图片
        (r'\[([^\]]+)\]\([^)]+\)', r'\1'),  # 链接（保留文本）
        (r'`{3}[\s\S]*?`{3}', ''),  # 代码块
        (r'`([^`]+)`', r'\1'),  # 行内代码
        (r'#+\s*', ''),  # 标题标记
        (r'\*\*?|__?', ''),  # 粗体/斜体标记
        (r'\|', ' '),  # 表格分隔符
        (r'[-*]\s+', ' '),  # 列表标记
        (r'>\s*', ' '),  # 引用
    ]
    
    def __init__(self):
        pass
    
    def clean_markdown(self, text: str) -> str:
        """清理Markdown语法"""
        cleaned = text
        for pattern, replacement in self.MARKDOWN_PATTERNS:
            cleaned = re.sub(pattern, replacement, cleaned)
        return cleaned
    
    def remove_stopwords(self, text: str) -> str:
        """移除停用词"""
        words = re.findall(r'\b\w+\b|[\u4e00-\u9fff]', text.lower())
        filtered = [w for w in words if w not in self.STOP_WORDS and len(w) > 1]
        return ' '.join(filtered)
    
    def preprocess(self, text: str) -> str:
        """完整预处理流程"""
        # 清理Markdown
        cleaned = self.clean_markdown(text)
        # 移除URL
        cleaned = re.sub(r'https?://\S+', '', cleaned)
        # 移除停用词
        cleaned = self.remove_stopwords(cleaned)
        return cleaned


class DocumentLoader:
    """文档加载器"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.preprocessor = TextPreprocessor()
        self.documents: Dict[str, Document] = {}
    
    def load_file(self, file_path: Path) -> Optional[Document]:
        """加载单个文档"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"无法读取文件 {file_path}: {e}")
            return None
        
        # 提取标题
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem
        
        # 统计信息
        word_count = len(content.split())
        section_count = len(re.findall(r'^#{2,4}\s+', content, re.MULTILINE))
        
        # 预处理
        cleaned = self.preprocessor.preprocess(content)
        
        doc_id = str(file_path.relative_to(self.base_path))
        
        return Document(
            id=doc_id,
            path=str(file_path),
            title=title,
            content=content,
            cleaned_content=cleaned,
            word_count=word_count,
            section_count=section_count
        )
    
    def load_directory(self, directory: str, pattern: str = "*.md") -> int:
        """加载目录中的所有文档"""
        dir_path = self.base_path / directory
        if not dir_path.exists():
            logger.warning(f"目录不存在: {dir_path}")
            return 0
        
        files = list(dir_path.rglob(pattern))
        logger.info(f"在 {directory} 中找到 {len(files)} 个文件")
        
        count = 0
        for file_path in files:
            # 排除特定文件
            if any(exclude in str(file_path) for exclude in ['README', 'CHANGELOG', 'INDEX']):
                continue
            
            doc = self.load_file(file_path)
            if doc:
                self.documents[doc.id] = doc
                count += 1
        
        logger.info(f"成功加载 {count} 个文档")
        return count


class SimilarityCalculator:
    """相似度计算器"""
    
    def __init__(self, documents: Dict[str, Document]):
        self.documents = documents
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self.bert_embeddings = None
        self.bert_model = None
        
        if BERT_AVAILABLE:
            try:
                # 使用轻量级模型
                self.bert_model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
                logger.info("BERT模型加载成功")
            except Exception as e:
                logger.warning(f"BERT模型加载失败: {e}")
                self.bert_model = None
    
    def compute_tfidf(self) -> Any:
        """计算TF-IDF向量"""
        if not SKLEARN_AVAILABLE:
            logger.error("scikit-learn不可用")
            return None
        
        texts = [doc.cleaned_content for doc in self.documents.values()]
        doc_ids = list(self.documents.keys())
        
        # 创建TF-IDF向量化器
        vectorizer = TfidfVectorizer(
            max_features=5000,
            min_df=2,
            max_df=0.8,
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        
        try:
            self.tfidf_matrix = vectorizer.fit_transform(texts)
            
            # 将向量保存到文档
            for i, doc_id in enumerate(doc_ids):
                self.documents[doc_id].tfidf_vector = self.tfidf_matrix[i]
            
            logger.info(f"TF-IDF矩阵: {self.tfidf_matrix.shape}")
            return self.tfidf_matrix
            
        except Exception as e:
            logger.error(f"TF-IDF计算失败: {e}")
            return None
    
    def compute_bert_embeddings(self) -> Optional[Any]:
        """计算BERT嵌入"""
        if not BERT_AVAILABLE or self.bert_model is None:
            logger.warning("BERT不可用，跳过嵌入计算")
            return None
        
        texts = []
        doc_ids = []
        
        for doc_id, doc in self.documents.items():
            # 使用标题和前500字
            text = f"{doc.title}. {doc.cleaned_content[:500]}"
            texts.append(text)
            doc_ids.append(doc_id)
        
        try:
            logger.info("正在计算BERT嵌入...")
            self.bert_embeddings = self.bert_model.encode(
                texts,
                show_progress_bar=True,
                batch_size=32
            )
            
            # 保存到文档
            for i, doc_id in enumerate(doc_ids):
                self.documents[doc_id].embeddings = self.bert_embeddings[i]
            
            logger.info(f"BERT嵌入矩阵: {self.bert_embeddings.shape}")
            return self.bert_embeddings
            
        except Exception as e:
            logger.error(f"BERT嵌入计算失败: {e}")
            return None
    
    def compute_similarity_matrix(self, method: str = 'tfidf') -> Optional[Any]:
        """计算相似度矩阵"""
        if method == 'tfidf' and self.tfidf_matrix is not None:
            logger.info("使用TF-IDF计算相似度...")
            self.similarity_matrix = cosine_similarity(self.tfidf_matrix)
        elif method == 'bert' and self.bert_embeddings is not None:
            logger.info("使用BERT嵌入计算相似度...")
            self.similarity_matrix = cosine_similarity(self.bert_embeddings)
        else:
            logger.error(f"无法计算相似度: {method} 不可用")
            return None
        
        logger.info(f"相似度矩阵: {self.similarity_matrix.shape}")
        return self.similarity_matrix
    
    def find_similar_pairs(self, threshold: float = 0.7, top_k: int = 100) -> List[Tuple[str, str, float]]:
        """找到相似的文档对"""
        if self.similarity_matrix is None:
            return []
        
        doc_ids = list(self.documents.keys())
        similar_pairs = []
        
        for i in range(len(doc_ids)):
            for j in range(i + 1, len(doc_ids)):
                sim = self.similarity_matrix[i][j]
                if sim >= threshold:
                    similar_pairs.append((doc_ids[i], doc_ids[j], float(sim)))
        
        # 排序并返回前K个
        similar_pairs.sort(key=lambda x: x[2], reverse=True)
        return similar_pairs[:top_k]
    
    def find_duplicates(self, threshold: float = 0.85) -> List[Tuple[str, str, float]]:
        """找到可能的重复文档"""
        return self.find_similar_pairs(threshold=threshold, top_k=50)
    
    def get_related_documents(self, doc_id: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """获取与指定文档最相关的文档"""
        if doc_id not in self.documents:
            return []
        
        doc_ids = list(self.documents.keys())
        if doc_id in doc_ids:
            idx = doc_ids.index(doc_id)
            similarities = self.similarity_matrix[idx]
            
            # 获取最相似的（排除自己）
            related = []
            for i, sim in enumerate(similarities):
                if i != idx:
                    related.append((doc_ids[i], float(sim)))
            
            related.sort(key=lambda x: x[1], reverse=True)
            return related[:top_k]
        
        return []


class DocumentClusterer:
    """文档聚类器"""
    
    def __init__(self, documents: Dict[str, Document], similarity_matrix: Any):
        self.documents = documents
        self.similarity_matrix = similarity_matrix
        self.clusters: Dict[int, List[str]] = defaultdict(list)
    
    def cluster_kmeans(self, n_clusters: int = 10) -> Dict[int, List[str]]:
        """使用K-Means聚类"""
        if not SKLEARN_AVAILABLE or self.similarity_matrix is None:
            return {}
        
        doc_ids = list(self.documents.keys())
        
        try:
            # 使用相似度矩阵进行聚类
            # 将相似度转换为距离
            distance_matrix = 1 - self.similarity_matrix
            
            # K-Means聚类
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            labels = kmeans.fit_predict(distance_matrix)
            
            # 分配聚类
            self.clusters = defaultdict(list)
            for i, doc_id in enumerate(doc_ids):
                cluster_id = int(labels[i])
                self.clusters[cluster_id].append(doc_id)
                self.documents[doc_id].cluster_id = cluster_id
            
            logger.info(f"K-Means聚类完成: {n_clusters} 个聚类")
            return dict(self.clusters)
            
        except Exception as e:
            logger.error(f"K-Means聚类失败: {e}")
            return {}
    
    def cluster_hierarchical(self, n_clusters: int = 10) -> Dict[int, List[str]]:
        """使用层次聚类"""
        if not SKLEARN_AVAILABLE or self.similarity_matrix is None:
            return {}
        
        doc_ids = list(self.documents.keys())
        
        try:
            # 层次聚类
            clustering = AgglomerativeClustering(
                n_clusters=n_clusters,
                affinity='precomputed',
                linkage='average'
            )
            
            distance_matrix = 1 - self.similarity_matrix
            labels = clustering.fit_predict(distance_matrix)
            
            self.clusters = defaultdict(list)
            for i, doc_id in enumerate(doc_ids):
                cluster_id = int(labels[i])
                self.clusters[cluster_id].append(doc_id)
                self.documents[doc_id].cluster_id = cluster_id
            
            logger.info(f"层次聚类完成: {n_clusters} 个聚类")
            return dict(self.clusters)
            
        except Exception as e:
            logger.error(f"层次聚类失败: {e}")
            return {}
    
    def analyze_clusters(self) -> Dict[int, Dict]:
        """分析每个聚类的特征"""
        analysis = {}
        
        for cluster_id, doc_ids in self.clusters.items():
            titles = [self.documents[did].title for did in doc_ids]
            word_counts = [self.documents[did].word_count for did in doc_ids]
            
            # 提取关键词（简单实现：统计标题中的词频）
            title_text = ' '.join(titles).lower()
            words = re.findall(r'\b[a-z]+\b|[\u4e00-\u9fff]+', title_text)
            word_freq = defaultdict(int)
            for w in words:
                if len(w) > 2:
                    word_freq[w] += 1
            
            top_keywords = heapq.nlargest(5, word_freq.items(), key=lambda x: x[1])
            
            analysis[cluster_id] = {
                'size': len(doc_ids),
                'avg_word_count': sum(word_counts) / len(word_counts) if word_counts else 0,
                'titles': titles[:5],
                'keywords': [kw[0] for kw in top_keywords]
            }
        
        return analysis


class GapAnalyzer:
    """内容缺口分析器"""
    
    def __init__(self, documents: Dict[str, Document]):
        self.documents = documents
    
    def analyze_topic_coverage(self) -> Dict[str, Any]:
        """分析主题覆盖情况"""
        # 预定义的主题
        topics = {
            '理论基础': ['定理', '引理', '定义', '证明', '形式化', 'model', 'theory', 'formal'],
            'Flink技术': ['Flink', 'checkpoint', 'watermark', 'state', 'window', '流计算'],
            '系统设计': ['架构', '设计模式', '实现', 'architecture', 'design', 'implementation'],
            '性能优化': ['性能', '优化', 'benchmark', 'throughput', 'latency', 'optimization'],
            '生产实践': ['部署', '运维', '监控', 'deployment', 'production', 'operations'],
            '案例研究': ['案例', '应用', 'case study', 'example', 'application']
        }
        
        coverage = {}
        for topic, keywords in topics.items():
            matched_docs = []
            for doc_id, doc in self.documents.items():
                text = f"{doc.title} {doc.cleaned_content[:1000]}".lower()
                score = sum(1 for kw in keywords if kw.lower() in text)
                if score > 0:
                    matched_docs.append((doc_id, score))
            
            matched_docs.sort(key=lambda x: x[1], reverse=True)
            coverage[topic] = {
                'document_count': len(matched_docs),
                'coverage_ratio': len(matched_docs) / len(self.documents),
                'top_documents': [d[0] for d in matched_docs[:5]],
                'keywords_matched': len(matched_docs) > 0
            }
        
        return coverage
    
    def identify_gaps(self) -> List[Dict]:
        """识别内容缺口"""
        coverage = self.analyze_topic_coverage()
        
        gaps = []
        for topic, data in coverage.items():
            if data['document_count'] < 3:
                gaps.append({
                    'topic': topic,
                    'current_documents': data['document_count'],
                    'suggested_action': '建议增加相关文档',
                    'priority': 'high' if data['document_count'] == 0 else 'medium'
                })
        
        return sorted(gaps, key=lambda x: x['current_documents'])


class SimilarityExporter:
    """相似度结果导出器"""
    
    def __init__(self, calculator: SimilarityCalculator, clusterer: DocumentClusterer):
        self.calculator = calculator
        self.clusterer = clusterer
    
    def export_similarity_matrix(self, output_path: str):
        """导出相似度矩阵"""
        if self.calculator.similarity_matrix is None:
            return
        
        doc_ids = list(self.calculator.documents.keys())
        matrix_size = len(doc_ids)
        
        # 只导出上三角矩阵以节省空间
        matrix_data = {
            'documents': doc_ids,
            'matrix': [],
            'shape': [matrix_size, matrix_size]
        }
        
        # 转换为稀疏格式
        for i in range(matrix_size):
            for j in range(i + 1, matrix_size):
                sim = float(self.calculator.similarity_matrix[i][j])
                if sim > 0.3:  # 只保存有意义的相似度
                    matrix_data['matrix'].append({
                        'i': i,
                        'j': j,
                        'sim': round(sim, 4)
                    })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(matrix_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"相似度矩阵已导出到: {output_path}")
    
    def export_clusters(self, output_path: str):
        """导出聚类结果"""
        clusters_data = {
            'generated_at': datetime.now().isoformat(),
            'total_clusters': len(self.clusterer.clusters),
            'clusters': {}
        }
        
        # 获取聚类分析
        analysis = self.clusterer.analyze_clusters()
        
        for cluster_id, doc_ids in self.clusterer.clusters.items():
            clusters_data['clusters'][str(cluster_id)] = {
                'documents': doc_ids,
                'size': len(doc_ids),
                'keywords': analysis.get(cluster_id, {}).get('keywords', []),
                'sample_titles': analysis.get(cluster_id, {}).get('titles', [])[:3]
            }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(clusters_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"聚类结果已导出到: {output_path}")
    
    def export_recommendations(self, output_path: str):
        """导出文档推荐"""
        recommendations = {
            'generated_at': datetime.now().isoformat(),
            'recommendations': {}
        }
        
        # 为每个文档生成推荐
        for doc_id in self.calculator.documents:
            related = self.calculator.get_related_documents(doc_id, top_k=5)
            if related:
                recommendations['recommendations'][doc_id] = [
                    {'document': rid, 'similarity': round(sim, 4)}
                    for rid, sim in related
                ]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(recommendations, f, ensure_ascii=False, indent=2)
        
        logger.info(f"推荐结果已导出到: {output_path}")


class DocSimilarityAnalyzer:
    """文档相似度分析器主类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_path = Path(config.get('base_path', '.'))
        self.output_dir = Path(config.get('output_dir', '.scripts/knowledge-graph/output'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.loader = DocumentLoader(self.base_path)
        self.calculator = None
        self.clusterer = None
        self.gap_analyzer = None
    
    def run(self):
        """执行完整分析流程"""
        logger.info("=" * 70)
        logger.info("文档相似度分析器启动")
        logger.info("=" * 70)
        
        # 1. 加载文档
        directories = self.config.get('source_directories', ['Struct', 'Knowledge', 'Flink'])
        for directory in directories:
            self.loader.load_directory(directory)
        
        if len(self.loader.documents) < 2:
            logger.error("文档数量不足，无法进行分析")
            return
        
        # 2. 计算相似度
        self.calculator = SimilarityCalculator(self.loader.documents)
        self.calculator.compute_tfidf()
        self.calculator.compute_bert_embeddings()
        
        # 选择计算方法
        method = self.config.get('similarity_method', 'tfidf')
        self.calculator.compute_similarity_matrix(method=method)
        
        # 3. 检测重复
        duplicates = self.calculator.find_duplicates(threshold=0.85)
        if duplicates:
            logger.warning(f"检测到 {len(duplicates)} 对可能重复的文档:")
            for doc1, doc2, sim in duplicates[:10]:
                logger.warning(f"  [{sim:.2%}] {doc1} <-> {doc2}")
        
        # 4. 聚类
        self.clusterer = DocumentClusterer(
            self.loader.documents,
            self.calculator.similarity_matrix
        )
        n_clusters = min(self.config.get('n_clusters', 10), len(self.loader.documents))
        self.clusterer.cluster_hierarchical(n_clusters=n_clusters)
        
        # 5. 分析内容缺口
        self.gap_analyzer = GapAnalyzer(self.loader.documents)
        gaps = self.gap_analyzer.identify_gaps()
        
        logger.info("\n识别到的内容缺口:")
        for gap in gaps[:5]:
            logger.info(f"  - {gap['topic']}: {gap['current_documents']} 篇文档 (优先级: {gap['priority']})")
        
        # 6. 导出结果
        exporter = SimilarityExporter(self.calculator, self.clusterer)
        
        exporter.export_similarity_matrix(
            str(self.output_dir / 'similarity-matrix.json')
        )
        exporter.export_clusters(
            str(self.output_dir / 'doc-clusters.json')
        )
        exporter.export_recommendations(
            str(self.output_dir / 'doc-recommendations.json')
        )
        
        # 导出缺口分析
        gap_path = self.output_dir / 'content-gaps.json'
        with open(gap_path, 'w', encoding='utf-8') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'coverage': self.gap_analyzer.analyze_topic_coverage(),
                'gaps': gaps
            }, f, ensure_ascii=False, indent=2)
        
        logger.info("=" * 70)
        logger.info("分析完成!")
        logger.info(f"输出文件:")
        logger.info(f"  - 相似度矩阵: {self.output_dir / 'similarity-matrix.json'}")
        logger.info(f"  - 聚类结果: {self.output_dir / 'doc-clusters.json'}")
        logger.info(f"  - 推荐结果: {self.output_dir / 'doc-recommendations.json'}")
        logger.info(f"  - 缺口分析: {gap_path}")
        logger.info("=" * 70)


def load_config(config_path: str) -> Dict[str, Any]:
    """加载配置文件"""
    default_config = {
        'base_path': '.',
        'output_dir': '.scripts/knowledge-graph/output',
        'source_directories': ['Struct', 'Knowledge', 'Flink'],
        'similarity_method': 'tfidf',
        'n_clusters': 10,
        'duplicate_threshold': 0.85,
        'similarity_threshold': 0.7
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
        description='文档相似度分析器 - 计算文档相似度并生成推荐'
    )
    parser.add_argument(
        '-c', '--config',
        default='.scripts/knowledge-graph/config.json',
        help='配置文件路径'
    )
    parser.add_argument(
        '-o', '--output',
        help='输出目录'
    )
    parser.add_argument(
        '--method',
        choices=['tfidf', 'bert'],
        help='相似度计算方法'
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
    if args.output:
        config['output_dir'] = args.output
    if args.method:
        config['similarity_method'] = args.method
    
    analyzer = DocSimilarityAnalyzer(config)
    analyzer.run()


if __name__ == '__main__':
    main()
