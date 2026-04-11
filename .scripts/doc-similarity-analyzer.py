#!/usr/bin/env python3
"""
文档相似度分析工具
功能：
- 计算文档间相似度
- 检测重复内容
- 推荐相关文档

作者: AnalysisDataFlow Toolchain Team
版本: 1.0.0
日期: 2026-04-11
"""

import re
import os
import json
import glob
import math
import hashlib
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict, Counter
import argparse


@dataclass
class SimilarityResult:
    """相似度结果"""
    file1: str
    file2: str
    similarity: float  # 0.0 - 1.0
    common_terms: int
    method: str


@dataclass
class DuplicateBlock:
    """重复内容块"""
    file1: str
    file2: str
    start1: int
    start2: int
    length: int
    content_hash: str
    content_preview: str


class DocSimilarityAnalyzer:
    """文档相似度分析器"""
    
    # 停用词
    STOP_WORDS = {
        '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '之', '与', '及', '等', '或', '但', '而', '若', '为', '以', '于', '被', '将', '向', '从', '对', '关于',
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us'
    }
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        self.documents: Dict[str, Dict] = {}  # 文件路径 -> 文档信息
        self.similarity_matrix: Dict[Tuple[str, str], float] = {}
        self.duplicate_blocks: List[DuplicateBlock] = []
        
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
                if not any(x in str(path) for x in ['TEMPLATE', '_TEMPLATE', '00-INDEX']):
                    md_files.append(path)
                    
        return sorted(set(md_files))
    
    def tokenize(self, text: str) -> List[str]:
        """分词"""
        # 提取中文词汇
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,}', text)
        # 提取英文单词
        english_words = re.findall(r'[a-zA-Z]{3,}', text.lower())
        
        tokens = chinese_words + english_words
        # 过滤停用词
        tokens = [t for t in tokens if t not in self.STOP_WORDS]
        return tokens
    
    def compute_tf(self, tokens: List[str]) -> Dict[str, float]:
        """计算词频"""
        counter = Counter(tokens)
        total = len(tokens)
        return {term: count / total for term, count in counter.items()}
    
    def compute_idf(self, all_docs_tokens: List[List[str]]) -> Dict[str, float]:
        """计算逆文档频率"""
        N = len(all_docs_tokens)
        idf = {}
        
        # 统计包含每个词的文档数
        term_doc_count = defaultdict(int)
        for tokens in all_docs_tokens:
            unique_terms = set(tokens)
            for term in unique_terms:
                term_doc_count[term] += 1
                
        for term, doc_count in term_doc_count.items():
            idf[term] = math.log(N / (doc_count + 1)) + 1
            
        return idf
    
    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """计算余弦相似度"""
        # 获取所有维度
        all_terms = set(vec1.keys()) | set(vec2.keys())
        
        # 计算点积
        dot_product = sum(vec1.get(term, 0) * vec2.get(term, 0) for term in all_terms)
        
        # 计算模长
        norm1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        norm2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)
    
    def jaccard_similarity(self, set1: Set, set2: Set) -> float:
        """计算Jaccard相似度"""
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
    
    def find_duplicate_blocks(self, content1: str, content2: str, 
                               file1: str, file2: str, min_length: int = 50) -> List[DuplicateBlock]:
        """查找重复内容块"""
        duplicates = []
        
        # 按行分割
        lines1 = content1.split('\n')
        lines2 = content2.split('\n')
        
        # 使用滑动窗口查找重复
        window_sizes = [min_length, min_length * 2, min_length * 4]
        
        found_ranges = set()  # 避免重叠报告
        
        for window_size in window_sizes:
            for i in range(len(lines1) - window_size + 1):
                block1 = '\n'.join(lines1[i:i + window_size])
                hash1 = hashlib.md5(block1.encode()).hexdigest()
                
                # 在第二个文档中查找
                for j in range(len(lines2) - window_size + 1):
                    # 检查是否已报告
                    range_key = (min(i, j), max(i, j), window_size)
                    if range_key in found_ranges:
                        continue
                        
                    block2 = '\n'.join(lines2[j:j + window_size])
                    hash2 = hashlib.md5(block2.encode()).hexdigest()
                    
                    if hash1 == hash2 and len(block1.strip()) > 20:
                        duplicates.append(DuplicateBlock(
                            file1=file1,
                            file2=file2,
                            start1=i + 1,
                            start2=j + 1,
                            length=window_size,
                            content_hash=hash1[:8],
                            content_preview=block1[:200].replace('\n', ' ')
                        ))
                        found_ranges.add(range_key)
                        
        return duplicates
    
    def analyze_document(self, file_path: Path) -> Dict:
        """分析单个文档"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return None
            
        rel_path = str(file_path.relative_to(self.base_path))
        
        # 提取纯文本（移除Markdown标记）
        text = re.sub(r'```[\s\S]*?```', ' ', content)  # 代码块
        text = re.sub(r'`[^`]+`', ' ', text)  # 行内代码
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # 链接
        text = re.sub(r'[#*_]', ' ', text)  # Markdown标记
        
        tokens = self.tokenize(text)
        
        return {
            'path': rel_path,
            'content': content,
            'text': text,
            'tokens': tokens,
            'tf': self.compute_tf(tokens),
            'unique_terms': set(tokens),
            'term_count': len(tokens),
            'unique_count': len(set(tokens))
        }
    
    def run_analysis(self, threshold: float = 0.3, block_min_length: int = 3) -> Tuple[List[SimilarityResult], List[DuplicateBlock]]:
        """运行相似度分析"""
        print("📊 Document Similarity Analyzer")
        print("=" * 50)
        
        # 1. 扫描并分析所有文档
        print("\n📁 Scanning and analyzing documents...")
        files = self.scan_all_files()
        
        for i, file_path in enumerate(files, 1):
            if i % 100 == 0:
                print(f"   Progress: {i}/{len(files)} files")
                
            doc_info = self.analyze_document(file_path)
            if doc_info:
                self.documents[doc_info['path']] = doc_info
                
        print(f"   Analyzed {len(self.documents)} documents")
        
        # 2. 计算IDF
        print("\n🔢 Computing IDF...")
        all_tokens = [doc['tokens'] for doc in self.documents.values()]
        idf = self.compute_idf(all_tokens)
        
        # 3. 计算TF-IDF并比较相似度
        print("\n🔗 Computing similarities...")
        doc_paths = list(self.documents.keys())
        results = []
        
        # 计算TF-IDF向量
        for path in doc_paths:
            doc = self.documents[path]
            doc['tfidf'] = {term: tf * idf.get(term, 0) for term, tf in doc['tf'].items()}
            
        # 两两比较
        total_pairs = len(doc_paths) * (len(doc_paths) - 1) // 2
        processed = 0
        
        for i in range(len(doc_paths)):
            for j in range(i + 1, len(doc_paths)):
                path1, path2 = doc_paths[i], doc_paths[j]
                doc1, doc2 = self.documents[path1], self.documents[path2]
                
                # 余弦相似度
                cosine_sim = self.cosine_similarity(doc1['tfidf'], doc2['tfidf'])
                
                # Jaccard相似度
                jaccard_sim = self.jaccard_similarity(doc1['unique_terms'], doc2['unique_terms'])
                
                # 综合相似度
                combined_sim = 0.7 * cosine_sim + 0.3 * jaccard_sim
                
                if combined_sim >= threshold:
                    common = len(doc1['unique_terms'] & doc2['unique_terms'])
                    results.append(SimilarityResult(
                        file1=path1,
                        file2=path2,
                        similarity=combined_sim,
                        common_terms=common,
                        method='combined'
                    ))
                    
                processed += 1
                if processed % 1000 == 0:
                    print(f"   Progress: {processed}/{total_pairs} pairs ({100*processed//total_pairs}%)")
                    
        # 4. 检测重复块
        print("\n🔍 Detecting duplicate blocks...")
        duplicate_blocks = []
        
        # 只检查相似度高的文档对
        high_sim_pairs = [r for r in results if r.similarity > 0.5]
        for result in high_sim_pairs[:50]:  # 限制数量
            doc1 = self.documents[result.file1]
            doc2 = self.documents[result.file2]
            
            blocks = self.find_duplicate_blocks(
                doc1['content'], doc2['content'],
                result.file1, result.file2,
                min_length=block_min_length
            )
            duplicate_blocks.extend(blocks)
            
        self.duplicate_blocks = duplicate_blocks
        
        return sorted(results, key=lambda x: x.similarity, reverse=True), duplicate_blocks
    
    def find_related_docs(self, target_file: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """查找相关文档"""
        related = []
        
        for (file1, file2), sim in self.similarity_matrix.items():
            if file1 == target_file:
                related.append((file2, sim))
            elif file2 == target_file:
                related.append((file1, sim))
                
        return sorted(related, key=lambda x: x[1], reverse=True)[:top_k]
    
    def generate_report(self, output_path: str, results: List[SimilarityResult]):
        """生成分析报告"""
        # 统计
        similarity_buckets = {
            'very_high': len([r for r in results if r.similarity >= 0.8]),
            'high': len([r for r in results if 0.6 <= r.similarity < 0.8]),
            'medium': len([r for r in results if 0.4 <= r.similarity < 0.6]),
            'low': len([r for r in results if r.similarity < 0.4]),
        }
        
        report = {
            'version': '1.0.0',
            'tool': 'Document Similarity Analyzer',
            'statistics': {
                'total_documents': len(self.documents),
                'pairs_analyzed': len(results),
                'similarity_distribution': similarity_buckets,
                'duplicate_blocks_found': len(self.duplicate_blocks)
            },
            'high_similarity_pairs': [
                asdict(r) for r in results[:50]
            ],
            'duplicate_blocks': [
                asdict(b) for b in self.duplicate_blocks[:20]
            ],
            'recommendations': self._generate_recommendations(results)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        return report
    
    def _generate_recommendations(self, results: List[SimilarityResult]) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # 高相似度建议合并
        very_high = [r for r in results if r.similarity >= 0.8]
        if very_high:
            recommendations.append(f"发现 {len(very_high)} 对文档相似度超过80%，建议检查是否需要合并")
            
        # 重复块建议
        if self.duplicate_blocks:
            recommendations.append(f"发现 {len(self.duplicate_blocks)} 处重复内容块，建议提取为共享内容")
            
        # 孤立文档
        all_files = set(self.documents.keys())
        connected = set()
        for r in results:
            if r.similarity > 0.2:
                connected.add(r.file1)
                connected.add(r.file2)
        isolated = all_files - connected
        if isolated:
            recommendations.append(f"发现 {len(isolated)} 篇孤立文档（与其他文档相似度低），建议检查是否需要添加相关引用")
            
        return recommendations


def main():
    parser = argparse.ArgumentParser(description='Document Similarity Analyzer')
    parser.add_argument('--base-path', default='.', help='项目根目录')
    parser.add_argument('--output', default='doc-similarity-report.json', help='输出报告路径')
    parser.add_argument('--threshold', type=float, default=0.3, help='相似度阈值')
    parser.add_argument('--find-related', help='查找指定文档的相关文档')
    parser.add_argument('--top-k', type=int, default=5, help='返回相关文档数量')
    
    args = parser.parse_args()
    
    analyzer = DocSimilarityAnalyzer(args.base_path)
    results, duplicates = analyzer.run_analysis(threshold=args.threshold)
    
    # 生成报告
    report = analyzer.generate_report(args.output, results)
    
    # 查找相关文档
    if args.find_related:
        related = analyzer.find_related_docs(args.find_related, args.top_k)
        print(f"\n📚 Documents related to {args.find_related}:")
        for doc, sim in related:
            print(f"   {sim:.2%} - {doc}")
            
    # 打印摘要
    print("\n" + "=" * 50)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Documents analyzed:   {report['statistics']['total_documents']}")
    print(f"Similar pairs found:  {report['statistics']['pairs_analyzed']}")
    print(f"Duplicate blocks:     {report['statistics']['duplicate_blocks_found']}")
    print("\nSimilarity distribution:")
    for level, count in report['statistics']['similarity_distribution'].items():
        print(f"  {level:12s}: {count}")
    print("\nRecommendations:")
    for rec in report['recommendations']:
        print(f"  • {rec}")
    print("=" * 50)
    print(f"\n✅ Report saved to: {args.output}")
    
    return 0


if __name__ == '__main__':
    exit(main())
