#!/usr/bin/env python3
"""
Document Summarizer for AnalysisDataFlow

This script automatically generates summaries for documents including:
- TL;DR one-sentence summary
- Key points extraction
- Multi-level summaries (full, section, paragraph)
- Code example descriptions

Usage:
    python doc-summarizer.py --file Struct/01.01-stream-processing.md
    python doc-summarizer.py --all --output-dir ./summaries
    python doc-summarizer.py --batch Struct/ Knowledge/
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
SOURCE_DIRS = ["Struct", "Knowledge", "Flink"]


@dataclass
class DocumentSummary:
    """Represents a document summary."""
    doc_path: str
    doc_title: str
    tldr: str  # One-sentence summary
    key_points: List[str]
    full_summary: str
    section_summaries: Dict[str, str]
    code_examples: List[Dict[str, str]]
    target_audience: str
    prerequisites: List[str]
    related_topics: List[str]
    generated_at: str
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_markdown(self) -> str:
        """Convert summary to markdown format."""
        md = f"""# Summary: {self.doc_title}

> **TL;DR**: {self.tldr}

## Key Points

"""
        for point in self.key_points:
            md += f"- {point}\n"
        
        md += f"""
## Full Summary

{self.full_summary}

## Target Audience

{self.target_audience}

## Prerequisites

"""
        if self.prerequisites:
            for prereq in self.prerequisites:
                md += f"- {prereq}\n"
        else:
            md += "None\n"
        
        md += "\n## Related Topics\n\n"
        if self.related_topics:
            for topic in self.related_topics:
                md += f"- {topic}\n"
        else:
            md += "None\n"
        
        if self.code_examples:
            md += "\n## Code Examples\n\n"
            for example in self.code_examples:
                md += f"**{example['title']}**: {example['description']}\n\n"
        
        if self.section_summaries:
            md += "\n## Section Summaries\n\n"
            for section, summary in self.section_summaries.items():
                md += f"### {section}\n\n{summary}\n\n"
        
        md += f"\n---\n*Generated at: {self.generated_at}*\n"
        
        return md


class DocumentParser:
    """Parser for extracting document structure and content."""
    
    def parse(self, filepath: Path) -> Dict[str, Any]:
        """Parse a Markdown document."""
        content = filepath.read_text(encoding="utf-8")
        
        # Extract title
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else filepath.stem
        
        # Extract sections with content
        sections = self._extract_sections(content)
        
        # Extract code examples
        code_examples = self._extract_code_examples(content)
        
        # Extract theorems/definitions
        formal_elements = self._extract_formal_elements(content)
        
        # Extract existing TL;DR if present
        tldr = self._extract_tldr(content)
        
        # Extract key information from first paragraph
        intro = self._extract_intro(content)
        
        return {
            "title": title,
            "content": content,
            "sections": sections,
            "code_examples": code_examples,
            "formal_elements": formal_elements,
            "existing_tldr": tldr,
            "introduction": intro,
        }
    
    def _extract_sections(self, content: str) -> Dict[str, str]:
        """Extract sections with their content."""
        sections = {}
        
        # Match level 2 and 3 headings
        pattern = r'^(#{2,3}) (.+)\n(.*?)(?=\n#{1,3} |$)'
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        
        for level, title, section_content in matches:
            sections[title.strip()] = section_content.strip()
        
        return sections
    
    def _extract_code_examples(self, content: str) -> List[Dict[str, str]]:
        """Extract code examples with their context."""
        examples = []
        
        # Find code blocks with preceding context
        pattern = r'(?:^|\n)([^\n]*(?:example|configuration|code|实现|配置)[^\n]*)\n```(\w*)\n(.*?)```'
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        
        for context, lang, code in matches[:5]:  # Limit to 5 examples
            examples.append({
                "context": context.strip(),
                "language": lang or "text",
                "code": code[:200] + "..." if len(code) > 200 else code,
            })
        
        return examples
    
    def _extract_formal_elements(self, content: str) -> Dict[str, List[str]]:
        """Extract formal elements (theorems, definitions, etc.)."""
        elements = {
            "theorems": re.findall(r'`(Thm-[SFK]-\d+-\d+)`', content),
            "definitions": re.findall(r'`(Def-[SFK]-\d+-\d+)`', content),
            "lemmas": re.findall(r'`(Lemma-[SFK]-\d+-\d+)`', content),
            "propositions": re.findall(r'`(Prop-[SFK]-\d+-\d+)`', content),
        }
        return elements
    
    def _extract_tldr(self, content: str) -> Optional[str]:
        """Extract existing TL;DR."""
        # Match TL;DR in various formats
        patterns = [
            r'> \*\*TL;DR\*\*[:：]\s*(.+?)(?:\n\n|\Z)',
            r'## TL;DR\s*\n(.+?)(?:\n##|\Z)',
            r'\*\*TL;DR\*\*[:：]\s*(.+?)(?:\n\n|\Z)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_intro(self, content: str) -> str:
        """Extract introduction paragraph."""
        # Get text after title and before first heading
        pattern = r'^# .+\n+(.*?)(?=\n## |\Z)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        
        if match:
            intro = match.group(1).strip()
            # Clean up markdown
            intro = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', intro)  # Remove links
            intro = re.sub(r'>\s*', '', intro)  # Remove blockquote markers
            return intro[:500]  # Limit length
        
        return ""


class Summarizer:
    """Generates summaries for documents."""
    
    def __init__(self):
        self.parser = DocumentParser()
        
        # Keywords for determining document type
        self.type_keywords = {
            "theoretical": ["theorem", "proof", "formal", "definition", "lemma", "process calculus", "形式化", "定理", "证明"],
            "practical": ["configuration", "deployment", "implementation", "example", "配置", "部署", "实现"],
            "design_pattern": ["pattern", "anti-pattern", "best practice", "模式", "反模式", "最佳实践"],
            "comparison": ["vs", "comparison", "contrast", "compare", "对比", "比较"],
            "tutorial": ["tutorial", "guide", "quick start", "教程", "指南", "入门"],
        }
    
    def _determine_document_type(self, content: str) -> str:
        """Determine the type of document based on content."""
        content_lower = content.lower()
        
        scores = {}
        for doc_type, keywords in self.type_keywords.items():
            score = sum(1 for kw in keywords if kw.lower() in content_lower)
            scores[doc_type] = score
        
        return max(scores, key=scores.get) if scores else "general"
    
    def _generate_tldr(self, parsed: Dict) -> str:
        """Generate one-sentence TL;DR summary."""
        title = parsed["title"]
        intro = parsed["introduction"]
        doc_type = self._determine_document_type(parsed["content"])
        
        # Use existing TL;DR if available
        if parsed["existing_tldr"]:
            return parsed["existing_tldr"]
        
        # Generate based on document type
        templates = {
            "theoretical": f"This document presents the formal theoretical foundations of {title}, including rigorous definitions and proofs essential for understanding stream computing semantics.",
            "practical": f"This document provides practical guidance on {title}, covering configuration, implementation patterns, and production deployment considerations.",
            "design_pattern": f"This document describes the {title} design pattern, including when to apply it, implementation strategies, and common pitfalls to avoid.",
            "comparison": f"This document provides a comprehensive comparison of {title}, analyzing trade-offs across multiple dimensions to support technology selection decisions.",
            "tutorial": f"This document is a step-by-step tutorial on {title}, designed to help readers quickly get started with practical examples.",
            "general": f"This document covers {title}, providing theoretical foundations, practical guidance, and best practices for stream computing.",
        }
        
        return templates.get(doc_type, templates["general"])
    
    def _generate_key_points(self, parsed: Dict) -> List[str]:
        """Extract key points from document."""
        key_points = []
        
        # Extract from section headings
        sections = parsed["sections"]
        
        # Get main sections (usually first 4-5)
        main_sections = list(sections.keys())[:5]
        
        for section in main_sections:
            # Clean up section title
            clean_title = re.sub(r'^\d+\.\s*', '', section)  # Remove numbering
            
            # Determine if it's a key point
            if any(keyword in clean_title.lower() for keyword in [
                "definition", "theorem", "proof", "conclusion", "summary",
                "核心", "关键", "重要", "定义", "定理", "结论"
            ]):
                key_points.append(clean_title)
        
        # Add formal elements as key points
        formal = parsed["formal_elements"]
        if formal["theorems"]:
            key_points.append(f"Key theorems: {', '.join(formal['theorems'][:3])}")
        if formal["definitions"]:
            key_points.append(f"Core definitions: {', '.join(formal['definitions'][:3])}")
        
        # Add code examples
        if parsed["code_examples"]:
            key_points.append(f"Includes {len(parsed['code_examples'])} practical code examples")
        
        # Ensure we have at least 3 key points
        if len(key_points) < 3:
            for section in main_sections[:3]:
                clean_title = re.sub(r'^\d+\.\s*', '', section)
                if clean_title not in key_points:
                    key_points.append(clean_title)
                if len(key_points) >= 5:
                    break
        
        return key_points[:5]  # Limit to 5 key points
    
    def _generate_full_summary(self, parsed: Dict) -> str:
        """Generate a full paragraph summary."""
        title = parsed["title"]
        intro = parsed["introduction"]
        sections = parsed["sections"]
        doc_type = self._determine_document_type(parsed["content"])
        
        # Build summary from available information
        parts = []
        
        # Start with introduction if available
        if intro and len(intro) > 50:
            parts.append(intro[:300])
        
        # Add section overview
        section_names = list(sections.keys())[:4]
        if section_names:
            section_list = ", ".join([re.sub(r'^\d+\.\s*', '', s) for s in section_names])
            parts.append(f"The document covers: {section_list}.")
        
        # Add formal elements info
        formal = parsed["formal_elements"]
        if formal["theorems"] or formal["definitions"]:
            element_desc = []
            if formal["theorems"]:
                element_desc.append(f"{len(formal['theorems'])} theorem(s)")
            if formal["definitions"]:
                element_desc.append(f"{len(formal['definitions'])} definition(s)")
            parts.append(f"It includes {', '.join(element_desc)}.")
        
        # Add code info
        if parsed["code_examples"]:
            parts.append(f"Practical code examples are provided to illustrate key concepts.")
        
        summary = " ".join(parts)
        
        # Ensure minimum length
        if len(summary) < 100:
            summary = f"This document on {title} provides comprehensive coverage of the topic, including theoretical foundations and practical implementation guidance for stream computing applications."
        
        return summary
    
    def _generate_section_summaries(self, parsed: Dict) -> Dict[str, str]:
        """Generate summaries for major sections."""
        section_summaries = {}
        sections = parsed["sections"]
        
        # Only summarize main sections
        for section_name, content in list(sections.items())[:3]:
            # Skip very short sections
            if len(content) < 100:
                continue
            
            # Extract first paragraph
            first_para = content.split('\n\n')[0].strip()
            
            # Clean up
            first_para = re.sub(r'```.*?```', '[code example]', first_para, flags=re.DOTALL)
            first_para = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', first_para)
            
            if len(first_para) > 50:
                clean_name = re.sub(r'^\d+\.\s*', '', section_name)
                section_summaries[clean_name] = first_para[:300]
        
        return section_summaries
    
    def _generate_code_descriptions(self, parsed: Dict) -> List[Dict[str, str]]:
        """Generate descriptions for code examples."""
        examples = []
        
        for i, example in enumerate(parsed["code_examples"][:3]):
            context = example["context"]
            
            # Generate description based on context and code
            if "configuration" in context.lower() or "配置" in context:
                description = f"Configuration example showing how to set up {context.lower()}"
            elif "example" in context.lower() or "示例" in context:
                description = f"Practical implementation example: {context}"
            else:
                description = f"Code demonstration: {context}"
            
            examples.append({
                "title": f"Example {i+1}",
                "description": description,
                "language": example["language"],
            })
        
        return examples
    
    def _determine_target_audience(self, parsed: Dict) -> str:
        """Determine the target audience."""
        content = parsed["content"].lower()
        doc_type = self._determine_document_type(content)
        
        audiences = {
            "theoretical": "Researchers and advanced practitioners interested in formal methods and theoretical foundations",
            "practical": "Engineers and developers implementing stream processing applications",
            "design_pattern": "Architects and senior developers designing stream processing systems",
            "comparison": "Technical decision-makers evaluating technology options",
            "tutorial": "Beginners and developers new to stream processing",
            "general": "Stream computing practitioners at all levels",
        }
        
        return audiences.get(doc_type, audiences["general"])
    
    def _extract_prerequisites(self, parsed: Dict) -> List[str]:
        """Extract prerequisite knowledge."""
        prereqs = []
        content = parsed["content"]
        
        # Look for prerequisite sections
        prereq_match = re.search(
            r'(?:##?\s*(?:Prerequisites|前置条件|前置知识).*?\n)(.*?)(?=\n##?\s|$)',
            content, re.IGNORECASE | re.DOTALL
        )
        
        if prereq_match:
            prereq_text = prereq_match.group(1)
            # Extract list items
            items = re.findall(r'[-*]\s*(.+)', prereq_text)
            prereqs = [item.strip() for item in items[:5]]
        
        # If no explicit prerequisites, infer from formal elements
        if not prereqs:
            formal = parsed["formal_elements"]
            if formal["definitions"]:
                prereqs.append("Familiarity with basic stream computing concepts")
            if formal["theorems"]:
                prereqs.append("Understanding of formal proof techniques")
        
        return prereqs
    
    def _extract_related_topics(self, parsed: Dict) -> List[str]:
        """Extract related topics from links and references."""
        topics = []
        content = parsed["content"]
        
        # Extract internal links
        links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)
        
        for text, link in links[:8]:
            # Clean up link text
            clean_text = text.strip()
            if clean_text and clean_text not in topics:
                topics.append(clean_text)
        
        return topics
    
    def summarize(self, filepath: Path) -> DocumentSummary:
        """Generate a complete summary for a document."""
        parsed = self.parser.parse(filepath)
        
        return DocumentSummary(
            doc_path=str(filepath.relative_to(PROJECT_ROOT)),
            doc_title=parsed["title"],
            tldr=self._generate_tldr(parsed),
            key_points=self._generate_key_points(parsed),
            full_summary=self._generate_full_summary(parsed),
            section_summaries=self._generate_section_summaries(parsed),
            code_examples=self._generate_code_descriptions(parsed),
            target_audience=self._determine_target_audience(parsed),
            prerequisites=self._extract_prerequisites(parsed),
            related_topics=self._extract_related_topics(parsed),
            generated_at=datetime.now().isoformat(),
        )


class BatchSummarizer:
    """Handles batch summarization."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.summarizer = Summarizer()
    
    def _get_documents(self, paths: List[str]) -> List[Path]:
        """Get all documents from given paths."""
        documents = []
        
        for path_str in paths:
            path = PROJECT_ROOT / path_str
            if path.is_file() and path.suffix == ".md":
                documents.append(path)
            elif path.is_dir():
                for file in path.glob("**/*.md"):
                    # Skip index and README files
                    if file.name not in ["00-INDEX.md", "README.md"]:
                        documents.append(file)
        
        return sorted(documents)
    
    def summarize_all(self, source_dirs: List[str] = None) -> Dict:
        """Summarize all documents in source directories."""
        if source_dirs is None:
            source_dirs = SOURCE_DIRS
        
        documents = self._get_documents(source_dirs)
        
        print(f"Summarizing {len(documents)} documents...")
        
        summaries = {}
        
        for i, doc_path in enumerate(documents):
            if i % 20 == 0:
                print(f"  Processed {i}/{len(documents)} documents...")
            
            try:
                summary = self.summarizer.summarize(doc_path)
                summaries[summary.doc_path] = summary.to_dict()
                
                # Save individual summary
                summary_file = self.output_dir / f"{doc_path.stem}-summary.md"
                with open(summary_file, "w", encoding="utf-8") as f:
                    f.write(summary.to_markdown())
                
            except Exception as e:
                print(f"  Error summarizing {doc_path}: {e}")
        
        # Save combined index
        index_file = self.output_dir / "summaries-index.json"
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "total_documents": len(summaries),
                "summaries": summaries,
            }, f, indent=2, ensure_ascii=False)
        
        print(f"Summaries saved to {self.output_dir}")
        print(f"Total: {len(summaries)} documents summarized")
        
        return summaries


def main():
    parser = argparse.ArgumentParser(
        description="Document Summarizer for AnalysisDataFlow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Summarize a single document
    python doc-summarizer.py --file Struct/01.01-stream-processing.md
    
    # Summarize all documents
    python doc-summarizer.py --all --output-dir ./summaries
    
    # Summarize specific directories
    python doc-summarizer.py --batch Struct/ Knowledge/
        """
    )
    
    parser.add_argument("--file", help="Single document to summarize")
    parser.add_argument("--all", action="store_true", help="Summarize all documents")
    parser.add_argument("--batch", nargs="+", help="Batch summarize directories")
    parser.add_argument("--output-dir", default="./summaries",
                       help="Output directory for summaries (default: ./summaries)")
    parser.add_argument("--format", choices=["markdown", "json", "both"], default="both",
                       help="Output format (default: both)")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    
    if args.file:
        # Single document
        doc_path = PROJECT_ROOT / args.file
        if not doc_path.exists():
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        
        summarizer = Summarizer()
        summary = summarizer.summarize(doc_path)
        
        if args.format in ["markdown", "both"]:
            print(summary.to_markdown())
        
        if args.format in ["json", "both"]:
            print(json.dumps(summary.to_dict(), indent=2, ensure_ascii=False))
    
    elif args.all or args.batch:
        # Batch processing
        batch_summarizer = BatchSummarizer(output_dir)
        
        if args.all:
            batch_summarizer.summarize_all()
        else:
            batch_summarizer.summarize_all(args.batch)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
