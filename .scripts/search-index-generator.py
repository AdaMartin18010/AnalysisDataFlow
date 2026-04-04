#!/usr/bin/env python3
"""
Search Index Generator for AnalysisDataFlow

This script generates search indices for the knowledge base including:
- Full-text search index (BM25/inverted index)
- Vector search index (embeddings for semantic search)
- Metadata index (document properties, tags, categories)
- Cross-reference index

Usage:
    python search-index-generator.py --output-dir ./search-index
    python search-index-generator.py --incremental --since 2026-04-01
    python search-index-generator.py --generate-vectors --model bge-large
"""

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
import pickle


# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
SOURCE_DIRS = ["Struct", "Knowledge", "Flink"]
EXCLUDE_PATTERNS = ["*.draft.md", "*.archived.md", "README.md", "00-INDEX.md"]


@dataclass
class DocumentChunk:
    """Represents a chunk of a document for indexing."""
    doc_id: str
    doc_path: str
    doc_title: str
    chunk_id: str
    content: str
    section: str
    chunk_type: str  # paragraph, code, theorem, definition, etc.
    position: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SearchIndexEntry:
    """Represents a search index entry."""
    id: str
    path: str
    title: str
    content: str
    summary: str
    sections: List[str]
    tags: List[str]
    category: str
    last_modified: str
    word_count: int
    theorem_count: int
    has_code: bool
    has_diagrams: bool
    
    def to_dict(self) -> Dict:
        return asdict(self)


class MarkdownParser:
    """Parser for Markdown documents."""
    
    @staticmethod
    def parse_document(filepath: Path) -> Dict[str, Any]:
        """Parse a Markdown document and extract structure."""
        content = filepath.read_text(encoding="utf-8")
        
        # Extract title
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else filepath.stem
        
        # Extract sections
        sections = re.findall(r'^#{2,3} (.+)$', content, re.MULTILINE)
        
        # Extract code blocks
        code_blocks = re.findall(r'```[\w]*\n(.*?)```', content, re.DOTALL)
        
        # Extract theorems/definitions
        theorems = re.findall(r'`(Thm|Def|Lemma|Prop)-[SFK]-\d+-\d+`', content)
        
        # Extract Mermaid diagrams
        diagrams = re.findall(r'```mermaid\n(.*?)```', content, re.DOTALL)
        
        # Extract summary/TL;DR if present
        summary = ""
        summary_match = re.search(r'> \*\*TL;DR\*\*:\s*(.+)', content)
        if summary_match:
            summary = summary_match.group(1)
        
        # Extract tags from metadata
        tags = []
        tags_match = re.search(r'tags:\s*\[(.*?)\]', content)
        if tags_match:
            tags = [t.strip() for t in tags_match.group(1).split(",")]
        
        return {
            "title": title,
            "content": content,
            "sections": sections,
            "code_blocks": code_blocks,
            "theorems": theorems,
            "diagrams": diagrams,
            "summary": summary,
            "tags": tags,
            "word_count": len(content.split()),
        }
    
    @staticmethod
    def chunk_document(filepath: Path, doc_id: str, chunk_size: int = 500) -> List[DocumentChunk]:
        """Split document into chunks for indexing."""
        content = filepath.read_text(encoding="utf-8")
        parsed = MarkdownParser.parse_document(filepath)
        
        chunks = []
        lines = content.split('\n')
        current_chunk = []
        current_section = "Introduction"
        chunk_index = 0
        position = 0
        
        for line in lines:
            # Track current section
            if line.startswith('## '):
                if current_chunk:
                    chunk_text = '\n'.join(current_chunk)
                    chunks.append(DocumentChunk(
                        doc_id=doc_id,
                        doc_path=str(filepath.relative_to(PROJECT_ROOT)),
                        doc_title=parsed["title"],
                        chunk_id=f"{doc_id}_chunk_{chunk_index}",
                        content=chunk_text,
                        section=current_section,
                        chunk_type="text",
                        position=position,
                    ))
                    chunk_index += 1
                    position += len(chunk_text)
                    current_chunk = []
                current_section = line[3:].strip()
            
            # Handle code blocks
            elif line.startswith('```'):
                if current_chunk:
                    chunk_text = '\n'.join(current_chunk)
                    chunks.append(DocumentChunk(
                        doc_id=doc_id,
                        doc_path=str(filepath.relative_to(PROJECT_ROOT)),
                        doc_title=parsed["title"],
                        chunk_id=f"{doc_id}_chunk_{chunk_index}",
                        content=chunk_text,
                        section=current_section,
                        chunk_type="text",
                        position=position,
                    ))
                    chunk_index += 1
                    position += len(chunk_text)
                    current_chunk = []
                
                # Extract code block
                code_lines = [line]
                line_idx = lines.index(line) + 1
                while line_idx < len(lines) and not lines[line_idx].startswith('```'):
                    code_lines.append(lines[line_idx])
                    line_idx += 1
                if line_idx < len(lines):
                    code_lines.append(lines[line_idx])
                
                code_text = '\n'.join(code_lines)
                chunks.append(DocumentChunk(
                    doc_id=doc_id,
                    doc_path=str(filepath.relative_to(PROJECT_ROOT)),
                    doc_title=parsed["title"],
                    chunk_id=f"{doc_id}_chunk_{chunk_index}",
                    content=code_text,
                    section=current_section,
                    chunk_type="code",
                    position=position,
                ))
                chunk_index += 1
                position += len(code_text)
            
            else:
                current_chunk.append(line)
                
                # Check chunk size
                if len('\n'.join(current_chunk)) >= chunk_size:
                    chunk_text = '\n'.join(current_chunk)
                    chunks.append(DocumentChunk(
                        doc_id=doc_id,
                        doc_path=str(filepath.relative_to(PROJECT_ROOT)),
                        doc_title=parsed["title"],
                        chunk_id=f"{doc_id}_chunk_{chunk_index}",
                        content=chunk_text,
                        section=current_section,
                        chunk_type="text",
                        position=position,
                    ))
                    chunk_index += 1
                    position += len(chunk_text)
                    current_chunk = []
        
        # Add remaining content
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunks.append(DocumentChunk(
                doc_id=doc_id,
                doc_path=str(filepath.relative_to(PROJECT_ROOT)),
                doc_title=parsed["title"],
                chunk_id=f"{doc_id}_chunk_{chunk_index}",
                content=chunk_text,
                section=current_section,
                chunk_type="text",
                position=position,
            ))
        
        return chunks


class SearchIndexGenerator:
    """Generates search indices for the knowledge base."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.parser = MarkdownParser()
        
        # Stop words for BM25
        self.stop_words = set([
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "must", "shall",
            "can", "need", "dare", "ought", "used", "to", "of", "in",
            "for", "on", "with", "at", "by", "from", "as", "into",
            "through", "during", "before", "after", "above", "below",
            "between", "under", "again", "further", "then", "once",
            "here", "there", "when", "where", "why", "how", "all",
            "each", "few", "more", "most", "other", "some", "such",
            "no", "nor", "not", "only", "own", "same", "so", "than",
            "too", "very", "just", "and", "but", "if", "or", "because",
            "until", "while", "this", "that", "these", "those",
        ])
    
    def _should_exclude(self, filepath: Path) -> bool:
        """Check if file should be excluded from indexing."""
        for pattern in EXCLUDE_PATTERNS:
            if filepath.match(pattern):
                return True
        return False
    
    def _get_all_documents(self) -> List[Path]:
        """Get all documents to index."""
        documents = []
        
        for source_dir in SOURCE_DIRS:
            source_path = PROJECT_ROOT / source_dir
            if source_path.exists():
                for pattern in ["**/*.md"]:
                    for file in source_path.glob(pattern):
                        if not self._should_exclude(file):
                            documents.append(file)
        
        # Also include root level documentation
        for file in PROJECT_ROOT.glob("*.md"):
            if not self._should_exclude(file):
                documents.append(file)
        
        return sorted(documents)
    
    def _compute_doc_id(self, filepath: Path) -> str:
        """Compute a unique document ID."""
        rel_path = filepath.relative_to(PROJECT_ROOT)
        return hashlib.md5(str(rel_path).encode()).hexdigest()[:12]
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        # Convert to lowercase and extract words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        # Filter stop words
        return [w for w in words if w not in self.stop_words and len(w) > 2]
    
    def generate_fulltext_index(self) -> Dict:
        """Generate inverted index for full-text search."""
        print("Generating full-text index...")
        
        documents = self._get_all_documents()
        
        # Document metadata
        doc_metadata = {}
        
        # Inverted index: term -> {doc_id: frequency}
        inverted_index = {}
        
        # Document frequency: term -> number of documents containing term
        doc_frequency = {}
        
        total_docs = len(documents)
        
        for i, doc_path in enumerate(documents):
            if i % 50 == 0:
                print(f"  Processing {i}/{total_docs} documents...")
            
            doc_id = self._compute_doc_id(doc_path)
            parsed = self.parser.parse_document(doc_path)
            
            # Store metadata
            doc_metadata[doc_id] = {
                "path": str(doc_path.relative_to(PROJECT_ROOT)),
                "title": parsed["title"],
                "summary": parsed["summary"],
                "sections": parsed["sections"][:10],  # Limit sections
                "tags": parsed["tags"],
                "word_count": parsed["word_count"],
                "theorem_count": len(parsed["theorems"]),
                "has_code": len(parsed["code_blocks"]) > 0,
                "has_diagrams": len(parsed["diagrams"]) > 0,
            }
            
            # Tokenize content
            tokens = self._tokenize(parsed["content"])
            
            # Count term frequencies in this document
            term_freq = {}
            for token in tokens:
                term_freq[token] = term_freq.get(token, 0) + 1
            
            # Update inverted index
            for term, freq in term_freq.items():
                if term not in inverted_index:
                    inverted_index[term] = {}
                    doc_frequency[term] = 0
                inverted_index[term][doc_id] = freq
                doc_frequency[term] += 1
        
        print(f"Full-text index complete: {len(inverted_index)} terms, {len(doc_metadata)} documents")
        
        return {
            "metadata": doc_metadata,
            "inverted_index": inverted_index,
            "doc_frequency": doc_frequency,
            "total_docs": total_docs,
            "generated_at": datetime.now().isoformat(),
        }
    
    def generate_chunk_index(self) -> Dict:
        """Generate chunked index for more precise search."""
        print("Generating chunk index...")
        
        documents = self._get_all_documents()
        chunks = []
        
        for i, doc_path in enumerate(documents):
            if i % 50 == 0:
                print(f"  Processing {i}/{len(documents)} documents...")
            
            doc_id = self._compute_doc_id(doc_path)
            doc_chunks = self.parser.chunk_document(doc_path, doc_id)
            chunks.extend([c.to_dict() for c in doc_chunks])
        
        print(f"Chunk index complete: {len(chunks)} chunks")
        
        return {
            "chunks": chunks,
            "generated_at": datetime.now().isoformat(),
        }
    
    def generate_metadata_index(self) -> Dict:
        """Generate metadata-only index."""
        print("Generating metadata index...")
        
        documents = self._get_all_documents()
        entries = []
        
        for doc_path in documents:
            doc_id = self._compute_doc_id(doc_path)
            parsed = self.parser.parse_document(doc_path)
            
            entry = SearchIndexEntry(
                id=doc_id,
                path=str(doc_path.relative_to(PROJECT_ROOT)),
                title=parsed["title"],
                content=parsed["content"][:500] + "..." if len(parsed["content"]) > 500 else parsed["content"],
                summary=parsed["summary"],
                sections=parsed["sections"][:10],
                tags=parsed["tags"],
                category=doc_path.parent.name,
                last_modified=datetime.fromtimestamp(doc_path.stat().st_mtime).isoformat(),
                word_count=parsed["word_count"],
                theorem_count=len(parsed["theorems"]),
                has_code=len(parsed["code_blocks"]) > 0,
                has_diagrams=len(parsed["diagrams"]) > 0,
            )
            entries.append(entry.to_dict())
        
        print(f"Metadata index complete: {len(entries)} entries")
        
        return {
            "entries": entries,
            "generated_at": datetime.now().isoformat(),
        }
    
    def generate_crossref_index(self) -> Dict:
        """Generate cross-reference index."""
        print("Generating cross-reference index...")
        
        documents = self._get_all_documents()
        
        # Theorem references
        theorem_refs = {}
        
        # Document references
        doc_refs = {}
        
        for doc_path in documents:
            doc_id = self._compute_doc_id(doc_path)
            content = doc_path.read_text(encoding="utf-8")
            rel_path = str(doc_path.relative_to(PROJECT_ROOT))
            
            # Find theorem references
            theorems = re.findall(r'`(Thm|Def|Lemma|Prop|Cor)-[SFK]-(\d+)-(\d+)`', content)
            for t in theorems:
                ref_id = f"{t[0]}-{t[1]}-{t[2]}-{t[3]}"
                if ref_id not in theorem_refs:
                    theorem_refs[ref_id] = []
                theorem_refs[ref_id].append(rel_path)
            
            # Find document links
            links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)
            doc_refs[rel_path] = [link[1] for link in links]
        
        print(f"Cross-reference index complete: {len(theorem_refs)} theorems, {len(doc_refs)} documents")
        
        return {
            "theorem_references": theorem_refs,
            "document_references": doc_refs,
            "generated_at": datetime.now().isoformat(),
        }
    
    def generate_all_indices(self, incremental: bool = False, since: Optional[str] = None):
        """Generate all search indices."""
        print(f"Generating search indices to {self.output_dir}")
        print("=" * 60)
        
        # Full-text index
        fulltext_index = self.generate_fulltext_index()
        with open(self.output_dir / "fulltext-index.json", "w", encoding="utf-8") as f:
            json.dump(fulltext_index, f, indent=2, ensure_ascii=False)
        print(f"Saved: fulltext-index.json")
        
        # Chunk index
        chunk_index = self.generate_chunk_index()
        with open(self.output_dir / "chunk-index.json", "w", encoding="utf-8") as f:
            json.dump(chunk_index, f, indent=2, ensure_ascii=False)
        print(f"Saved: chunk-index.json")
        
        # Metadata index
        metadata_index = self.generate_metadata_index()
        with open(self.output_dir / "metadata-index.json", "w", encoding="utf-8") as f:
            json.dump(metadata_index, f, indent=2, ensure_ascii=False)
        print(f"Saved: metadata-index.json")
        
        # Cross-reference index
        crossref_index = self.generate_crossref_index()
        with open(self.output_dir / "crossref-index.json", "w", encoding="utf-8") as f:
            json.dump(crossref_index, f, indent=2, ensure_ascii=False)
        print(f"Saved: crossref-index.json")
        
        # Generate manifest
        manifest = {
            "generated_at": datetime.now().isoformat(),
            "version": "1.0",
            "indices": {
                "fulltext": {
                    "file": "fulltext-index.json",
                    "format": "inverted-index",
                    "doc_count": fulltext_index["total_docs"],
                    "term_count": len(fulltext_index["inverted_index"]),
                },
                "chunks": {
                    "file": "chunk-index.json",
                    "format": "document-chunks",
                    "chunk_count": len(chunk_index["chunks"]),
                },
                "metadata": {
                    "file": "metadata-index.json",
                    "format": "document-metadata",
                    "entry_count": len(metadata_index["entries"]),
                },
                "crossref": {
                    "file": "crossref-index.json",
                    "format": "reference-graph",
                    "theorem_count": len(crossref_index["theorem_references"]),
                },
            },
        }
        
        with open(self.output_dir / "manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"Saved: manifest.json")
        
        print("=" * 60)
        print("Index generation complete!")
        
        return manifest


def main():
    parser = argparse.ArgumentParser(
        description="Search Index Generator for AnalysisDataFlow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate all indices
    python search-index-generator.py --output-dir ./search-index
    
    # Generate indices incrementally
    python search-index-generator.py --incremental --since 2026-04-01
    
    # Generate only specific index
    python search-index-generator.py --output-dir ./search-index --type metadata
        """
    )
    
    parser.add_argument("--output-dir", default="./search-index",
                       help="Output directory for indices (default: ./search-index)")
    parser.add_argument("--incremental", action="store_true",
                       help="Only process changed documents")
    parser.add_argument("--since", help="Only process documents modified since date (YYYY-MM-DD)")
    parser.add_argument("--type", choices=["fulltext", "chunks", "metadata", "crossref", "all"],
                       default="all", help="Type of index to generate (default: all)")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    generator = SearchIndexGenerator(output_dir)
    
    if args.type == "all":
        generator.generate_all_indices(incremental=args.incremental, since=args.since)
    else:
        print(f"Generating {args.type} index only...")
        if args.type == "fulltext":
            index = generator.generate_fulltext_index()
            with open(output_dir / "fulltext-index.json", "w", encoding="utf-8") as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
        elif args.type == "chunks":
            index = generator.generate_chunk_index()
            with open(output_dir / "chunk-index.json", "w", encoding="utf-8") as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
        elif args.type == "metadata":
            index = generator.generate_metadata_index()
            with open(output_dir / "metadata-index.json", "w", encoding="utf-8") as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
        elif args.type == "crossref":
            index = generator.generate_crossref_index()
            with open(output_dir / "crossref-index.json", "w", encoding="utf-8") as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
        print(f"Saved: {args.type}-index.json")


if __name__ == "__main__":
    main()
