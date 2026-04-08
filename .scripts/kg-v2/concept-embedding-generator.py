#!/usr/bin/env python3
"""
AnalysisDataFlow 知识图谱 v2.0 - 概念嵌入生成器
基于 Sentence-BERT 的语义嵌入生成与索引构建

功能:
1. 从 THEOREM-REGISTRY.md 和文档中提取概念
2. 使用 Sentence-BERT 生成语义嵌入
3. 构建 FAISS/Annoy 索引支持快速相似度搜索
4. 输出概念嵌入数据和索引文件

依赖:
    pip install sentence-transformers numpy scikit-learn h5py tqdm

Usage:
    python concept-embedding-generator.py
    python concept-embedding-generator.py --model all-MiniLM-L6-v2
    python concept-embedding-generator.py --output-dir ./embeddings
"""

import os
import re
import json
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime

import numpy as np
from tqdm import tqdm

# Optional imports with graceful fallback
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available, using fallback TF-IDF")

try:
    import h5py
    H5PY_AVAILABLE = True
except ImportError:
    H5PY_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


# ============================================
# Configuration
# ============================================

DEFAULT_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384  # For all-MiniLM-L6-v2
BATCH_SIZE = 32
PROJECT_ROOT = Path(__file__).parent.parent.parent


# ============================================
# Data Classes
# ============================================

@dataclass
class Concept:
    """知识图谱概念定义"""
    id: str
    label: str
    type: str  # theorem, definition, lemma, proposition, corollary, document
    stage: str  # Struct, Knowledge, Flink
    description: str
    embedding: Optional[np.ndarray] = None
    metadata: Dict = None
    
    def to_dict(self) -> Dict:
        """转换为字典（不含embedding）"""
        return {
            'id': self.id,
            'label': self.label,
            'type': self.type,
            'stage': self.stage,
            'description': self.description,
            'metadata': self.metadata or {}
        }


@dataclass
class SimilarConcept:
    """相似概念结果"""
    concept_id: str
    label: str
    similarity: float
    type: str


# ============================================
# Concept Extractor
# ============================================

class ConceptExtractor:
    """从项目文档中提取概念"""
    
    # Regex patterns for extracting formal elements
    THEOREM_PATTERN = re.compile(
        r'\|\s*(Thm-[SKF]-\d{2}-\d{2,3})\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|',
        re.MULTILINE
    )
    DEFINITION_PATTERN = re.compile(
        r'\|\s*(Def-[SKF]-\d{2}-\d{2,3})\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|',
        re.MULTILINE
    )
    LEMMA_PATTERN = re.compile(
        r'\|\s*(Lemma-[SKF]-\d{2}-\d{2,3})\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|',
        re.MULTILINE
    )
    PROPOSITION_PATTERN = re.compile(
        r'\|\s*(Prop-[SKF]-\d{2}-\d{2,3})\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|',
        re.MULTILINE
    )
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.concepts: List[Concept] = []
        
    def extract_from_theorem_registry(self) -> List[Concept]:
        """从 THEOREM-REGISTRY.md 提取形式化元素"""
        registry_path = self.project_root / "THEOREM-REGISTRY.md"
        if not registry_path.exists():
            print(f"Warning: {registry_path} not found")
            return []
        
        content = registry_path.read_text(encoding='utf-8')
        concepts = []
        
        # Extract theorems
        for match in self.THEOREM_PATTERN.finditer(content):
            concept_id = match.group(1).strip()
            name = match.group(2).strip()
            location = match.group(3).strip()
            formality_level = match.group(4).strip()
            
            stage = self._parse_stage(concept_id)
            
            concepts.append(Concept(
                id=concept_id,
                label=name,
                type='theorem',
                stage=stage,
                description=f"{name} - {formality_level}",
                metadata={
                    'location': location,
                    'formality_level': formality_level
                }
            ))
        
        # Extract definitions
        for match in self.DEFINITION_PATTERN.finditer(content):
            concept_id = match.group(1).strip()
            name = match.group(2).strip()
            location = match.group(3).strip()
            formality_level = match.group(4).strip()
            
            stage = self._parse_stage(concept_id)
            
            concepts.append(Concept(
                id=concept_id,
                label=name,
                type='definition',
                stage=stage,
                description=f"{name} - {formality_level}",
                metadata={
                    'location': location,
                    'formality_level': formality_level
                }
            ))
        
        # Extract lemmas
        for match in self.LEMMA_PATTERN.finditer(content):
            concept_id = match.group(1).strip()
            name = match.group(2).strip()
            location = match.group(3).strip()
            formality_level = match.group(4).strip()
            
            stage = self._parse_stage(concept_id)
            
            concepts.append(Concept(
                id=concept_id,
                label=name,
                type='lemma',
                stage=stage,
                description=f"{name} - {formality_level}",
                metadata={
                    'location': location,
                    'formality_level': formality_level
                }
            ))
        
        # Extract propositions
        for match in self.PROPOSITION_PATTERN.finditer(content):
            concept_id = match.group(1).strip()
            name = match.group(2).strip()
            location = match.group(3).strip()
            formality_level = match.group(4).strip()
            
            stage = self._parse_stage(concept_id)
            
            concepts.append(Concept(
                id=concept_id,
                label=name,
                type='proposition',
                stage=stage,
                description=f"{name} - {formality_level}",
                metadata={
                    'location': location,
                    'formality_level': formality_level
                }
            ))
        
        print(f"Extracted {len(concepts)} formal elements from THEOREM-REGISTRY.md")
        return concepts
    
    def extract_from_graph_data(self) -> List[Concept]:
        """从 graph-data.json 提取文档节点"""
        graph_path = self.project_root / ".vscode" / "graph-data.json"
        if not graph_path.exists():
            print(f"Warning: {graph_path} not found")
            return []
        
        with open(graph_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        concepts = []
        for node in data.get('nodes', []):
            concept_id = node.get('id', '')
            label = node.get('label', concept_id)
            node_type = node.get('type', 'unknown')
            group = node.get('group', 'unknown')
            
            # Skip if already extracted from registry
            if any(c.id == concept_id for c in self.concepts):
                continue
            
            concepts.append(Concept(
                id=concept_id,
                label=label,
                type=node_type,
                stage=group,
                description=label,
                metadata=node.get('metadata', {})
            ))
        
        print(f"Extracted {len(concepts)} nodes from graph-data.json")
        return concepts
    
    def extract_all(self) -> List[Concept]:
        """提取所有概念"""
        self.concepts = []
        
        # Extract from theorem registry
        self.concepts.extend(self.extract_from_theorem_registry())
        
        # Extract from graph data
        self.concepts.extend(self.extract_from_graph_data())
        
        # Remove duplicates
        seen_ids = set()
        unique_concepts = []
        for c in self.concepts:
            if c.id not in seen_ids:
                seen_ids.add(c.id)
                unique_concepts.append(c)
        
        self.concepts = unique_concepts
        print(f"Total unique concepts: {len(self.concepts)}")
        return self.concepts
    
    def _parse_stage(self, concept_id: str) -> str:
        """从概念ID解析阶段"""
        if '-S-' in concept_id:
            return 'Struct'
        elif '-K-' in concept_id:
            return 'Knowledge'
        elif '-F-' in concept_id:
            return 'Flink'
        return 'Unknown'


# ============================================
# Embedding Generator
# ============================================

class EmbeddingGenerator:
    """使用Sentence-BERT生成语义嵌入"""
    
    def __init__(self, model_name: str = DEFAULT_MODEL, use_gpu: bool = False):
        self.model_name = model_name
        self.model = None
        self.use_gpu = use_gpu
        
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            print(f"Loading Sentence-BERT model: {model_name}")
            self.model = SentenceTransformer(model_name)
            if use_gpu:
                self.model = self.model.to('cuda')
            print(f"Model loaded. Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
        elif SKLEARN_AVAILABLE:
            print("Using TF-IDF fallback (Sentence-BERT not available)")
            self.vectorizer = TfidfVectorizer(max_features=EMBEDDING_DIM)
        else:
            raise RuntimeError("Neither sentence-transformers nor scikit-learn available")
    
    def generate_embeddings(self, concepts: List[Concept], batch_size: int = BATCH_SIZE) -> np.ndarray:
        """为概念列表生成嵌入"""
        texts = [f"{c.label}. {c.description}" for c in concepts]
        
        if self.model:
            # Use Sentence-BERT
            print("Generating embeddings with Sentence-BERT...")
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=True,
                convert_to_numpy=True
            )
        elif SKLEARN_AVAILABLE:
            # Use TF-IDF fallback
            print("Generating embeddings with TF-IDF...")
            embeddings = self.vectorizer.fit_transform(texts).toarray()
        else:
            raise RuntimeError("No embedding method available")
        
        # Normalize embeddings
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        return embeddings
    
    def compute_similarity_matrix(self, embeddings: np.ndarray) -> np.ndarray:
        """计算相似度矩阵"""
        return cosine_similarity(embeddings)
    
    def find_similar_concepts(
        self, 
        query_embedding: np.ndarray, 
        concept_embeddings: np.ndarray,
        concepts: List[Concept],
        top_k: int = 10
    ) -> List[SimilarConcept]:
        """找到最相似的概念"""
        similarities = cosine_similarity(
            query_embedding.reshape(1, -1),
            concept_embeddings
        )[0]
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            concept = concepts[idx]
            results.append(SimilarConcept(
                concept_id=concept.id,
                label=concept.label,
                similarity=float(similarities[idx]),
                type=concept.type
            ))
        
        return results


# ============================================
# Index Builder
# ============================================

class IndexBuilder:
    """构建快速相似度搜索索引"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_embeddings_hdf5(self, concepts: List[Concept], embeddings: np.ndarray):
        """保存嵌入到HDF5格式"""
        if not H5PY_AVAILABLE:
            print("h5py not available, skipping HDF5 save")
            return
        
        hdf5_path = self.output_dir / "concept-embeddings.h5"
        
        with h5py.File(hdf5_path, 'w') as f:
            # Save embeddings
            f.create_dataset('embeddings', data=embeddings, compression='gzip')
            
            # Save concept IDs
            concept_ids = [c.id.encode('utf-8') for c in concepts]
            f.create_dataset('concept_ids', data=concept_ids)
            
            # Save metadata
            metadata = json.dumps({
                'created_at': datetime.now().isoformat(),
                'num_concepts': len(concepts),
                'embedding_dim': embeddings.shape[1]
            })
            f.attrs['metadata'] = metadata
        
        print(f"Saved embeddings to {hdf5_path}")
    
    def save_embeddings_numpy(self, concepts: List[Concept], embeddings: np.ndarray):
        """保存嵌入到NumPy格式"""
        npy_path = self.output_dir / "concept-embeddings.npy"
        np.save(npy_path, embeddings)
        
        # Save concept IDs separately
        ids_path = self.output_dir / "concept-ids.json"
        with open(ids_path, 'w', encoding='utf-8') as f:
            json.dump([c.id for c in concepts], f, ensure_ascii=False, indent=2)
        
        print(f"Saved embeddings to {npy_path}")
    
    def save_concepts_json(self, concepts: List[Concept]):
        """保存概念元数据到JSON"""
        json_path = self.output_dir / "concept-embeddings.json"
        
        data = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'num_concepts': len(concepts),
                'version': '2.0'
            },
            'concepts': {c.id: c.to_dict() for c in concepts},
            'embeddings': {}  # Will be populated separately for web use
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Saved concept metadata to {json_path}")
    
    def build_annoy_index(self, embeddings: np.ndarray, concepts: List[Concept]):
        """构建Annoy索引"""
        try:
            from annoy import AnnoyIndex
            
            index = AnnoyIndex(embeddings.shape[1], 'angular')
            
            for i, embedding in enumerate(embeddings):
                index.add_item(i, embedding)
            
            index.build(10)  # 10 trees
            
            annoy_path = self.output_dir / "concept-index.ann"
            index.save(str(annoy_path))
            
            # Save mapping
            mapping_path = self.output_dir / "concept-index-mapping.json"
            with open(mapping_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'index_to_id': [c.id for c in concepts],
                    'id_to_index': {c.id: i for i, c in enumerate(concepts)}
                }, f)
            
            print(f"Saved Annoy index to {annoy_path}")
        except ImportError:
            print("annoy not available, skipping Annoy index build")
    
    def build_faiss_index(self, embeddings: np.ndarray):
        """构建FAISS索引"""
        try:
            import faiss
            
            # Create index
            index = faiss.IndexFlatIP(embeddings.shape[1])  # Inner product for cosine similarity
            
            # Add vectors
            index.add(embeddings.astype('float32'))
            
            # Save index
            faiss_path = self.output_dir / "concept-index.faiss"
            faiss.write_index(index, str(faiss_path))
            
            print(f"Saved FAISS index to {faiss_path}")
        except ImportError:
            print("faiss not available, skipping FAISS index build")
    
    def compute_similarity_pairs(self, concepts: List[Concept], embeddings: np.ndarray, threshold: float = 0.8):
        """计算高相似度概念对"""
        print("Computing similarity pairs...")
        
        similarity_matrix = cosine_similarity(embeddings)
        
        pairs = []
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                similarity = similarity_matrix[i, j]
                if similarity >= threshold:
                    pairs.append({
                        'source': concepts[i].id,
                        'target': concepts[j].id,
                        'similarity': float(similarity),
                        'type': 'implicit_similarity'
                    })
        
        pairs_path = self.output_dir / "similarity-pairs.json"
        with open(pairs_path, 'w', encoding='utf-8') as f:
            json.dump(pairs, f, ensure_ascii=False, indent=2)
        
        print(f"Found {len(pairs)} similar pairs (threshold={threshold})")
        print(f"Saved similarity pairs to {pairs_path}")
        
        return pairs


# ============================================
# Main Pipeline
# ============================================

def main():
    parser = argparse.ArgumentParser(description='Generate concept embeddings for Knowledge Graph v2.0')
    parser.add_argument('--model', default=DEFAULT_MODEL, help='Sentence-BERT model name')
    parser.add_argument('--output-dir', default='.scripts/kg-v2', help='Output directory')
    parser.add_argument('--similarity-threshold', type=float, default=0.8, help='Similarity threshold')
    parser.add_argument('--no-gpu', action='store_true', help='Disable GPU')
    parser.add_argument('--batch-size', type=int, default=BATCH_SIZE, help='Batch size')
    parser.add_argument('--project-root', type=Path, default=PROJECT_ROOT, help='Project root directory')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("AnalysisDataFlow 知识图谱 v2.0 - 概念嵌入生成器")
    print("=" * 60)
    print(f"Model: {args.model}")
    print(f"Output: {args.output_dir}")
    print(f"Project: {args.project_root}")
    print("=" * 60)
    
    # Step 1: Extract concepts
    print("\n[Step 1/4] Extracting concepts...")
    extractor = ConceptExtractor(args.project_root)
    concepts = extractor.extract_all()
    
    if not concepts:
        print("No concepts found!")
        return
    
    # Step 2: Generate embeddings
    print("\n[Step 2/4] Generating embeddings...")
    generator = EmbeddingGenerator(args.model, use_gpu=not args.no_gpu)
    embeddings = generator.generate_embeddings(concepts, batch_size=args.batch_size)
    
    # Attach embeddings to concepts
    for concept, embedding in zip(concepts, embeddings):
        concept.embedding = embedding
    
    print(f"Generated {embeddings.shape[0]} embeddings of dimension {embeddings.shape[1]}")
    
    # Step 3: Build indices
    print("\n[Step 3/4] Building indices...")
    output_dir = args.project_root / args.output_dir
    index_builder = IndexBuilder(output_dir)
    
    index_builder.save_embeddings_hdf5(concepts, embeddings)
    index_builder.save_embeddings_numpy(concepts, embeddings)
    index_builder.save_concepts_json(concepts)
    index_builder.build_annoy_index(embeddings, concepts)
    index_builder.build_faiss_index(embeddings)
    
    # Step 4: Compute similarity pairs
    print("\n[Step 4/4] Computing similarity pairs...")
    similar_pairs = index_builder.compute_similarity_pairs(
        concepts, embeddings, threshold=args.similarity_threshold
    )
    
    # Generate report
    print("\n" + "=" * 60)
    print("Generation Summary")
    print("=" * 60)
    print(f"Total concepts: {len(concepts)}")
    print(f"  - Theorems: {sum(1 for c in concepts if c.type == 'theorem')}")
    print(f"  - Definitions: {sum(1 for c in concepts if c.type == 'definition')}")
    print(f"  - Lemmas: {sum(1 for c in concepts if c.type == 'lemma')}")
    print(f"  - Propositions: {sum(1 for c in concepts if c.type == 'proposition')}")
    print(f"  - Documents: {sum(1 for c in concepts if c.type == 'document')}")
    print(f"\nEmbedding dimension: {embeddings.shape[1]}")
    print(f"Similar pairs found: {len(similar_pairs)}")
    print(f"\nOutput files:")
    print(f"  - {output_dir / 'concept-embeddings.json'}")
    print(f"  - {output_dir / 'concept-embeddings.npy'}")
    print(f"  - {output_dir / 'similarity-pairs.json'}")
    print("=" * 60)
    
    # Example search
    print("\n[Example] Top 5 similar concepts to first concept:")
    similar = generator.find_similar_concepts(
        embeddings[0], embeddings, concepts, top_k=5
    )
    for i, sim in enumerate(similar[1:], 1):  # Skip self
        print(f"  {i}. {sim.label} ({sim.type}) - {sim.similarity:.3f}")
    
    print("\n✅ Concept embedding generation complete!")


if __name__ == '__main__':
    main()
