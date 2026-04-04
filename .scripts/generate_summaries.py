#!/usr/bin/env python3
"""
AnalysisDataFlow 文档摘要自动生成器
Automatic Document Summary Generator

功能:
- 自动提取文档关键信息
- 生成结构化摘要
- 创建文档元数据
- 支持批量处理

用法:
    python generate_summaries.py [options]

输出:
    docs/summaries/*.json - 文档摘要
    docs/summary-index.json - 摘要索引

版本: 1.0.0
作者: AnalysisDataFlow Team
"""

import argparse
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib


PROJECT_ROOT = Path(__file__).parent.parent
SUMMARIES_DIR = PROJECT_ROOT / "docs" / "summaries"
SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
INDEX_OUTPUT = PROJECT_ROOT / "docs" / "summary-index.json"

SCAN_DIRS = ["Struct", "Knowledge", "Flink"]


@dataclass
class DocumentSummary:
    """文档摘要"""
    doc_id: str
    path: str
    title: str
    summary: str
    key_points: List[str]
    theorems: List[str]
    definitions: List[str]
    related_docs: List[str]
    reading_time: int  # minutes
    difficulty: str
    last_updated: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


class SummaryGenerator:
    """摘要生成器"""
    
    def __init__(self):
        self.summaries: List[DocumentSummary] = []
    
    def extract_first_paragraph(self, content: str) -> str:
        """提取第一段作为摘要"""
        # 跳过frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2]
        
        # 找到第一个非空段落
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        for para in paragraphs:
            # 跳过标题和代码块
            if para.startswith('#') or para.startswith('```'):
                continue
            # 返回前200字符
            return para[:300] + '...' if len(para) > 300 else para
        
        return ""
    
    def extract_key_points(self, content: str) -> List[str]:
        """提取关键点"""
        points = []
        
        # 提取列表项
        list_pattern = r'^[\s]*[-*]\s+(.+)$'
        for match in re.finditer(list_pattern, content, re.MULTILINE):
            point = match.group(1).strip()
            if len(point) > 20 and len(point) < 200:
                points.append(point)
            if len(points) >= 5:
                break
        
        return points[:5]
    
    def extract_theorems(self, content: str) -> List[str]:
        """提取定理引用"""
        theorem_pattern = r'`?(Thm-[SKF]-\d+-\d+)`?'
        theorems = list(set(re.findall(theorem_pattern, content)))
        return sorted(theorems)[:10]
    
    def extract_definitions(self, content: str) -> List[str]:
        """提取定义引用"""
        def_pattern = r'`?(Def-[SKF]-\d+-\d+)`?'
        definitions = list(set(re.findall(def_pattern, content)))
        return sorted(definitions)[:10]
    
    def extract_related_docs(self, content: str) -> List[str]:
        """提取相关文档链接"""
        related = []
        
        # 匹配Markdown链接
        link_pattern = r'\[([^\]]+)\]\(([^)]+\.md)\)'
        for match in re.finditer(link_pattern, content):
            title = match.group(1)
            path = match.group(2)
            related.append({"title": title, "path": path})
        
        return related[:5]
    
    def estimate_reading_time(self, content: str) -> int:
        """估算阅读时间"""
        # 中文字符 + 英文单词
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        english_words = len(re.findall(r'[a-zA-Z]+', content))
        total_words = chinese_chars + english_words
        
        # 假设阅读速度: 200字/分钟
        minutes = max(1, total_words // 200)
        return minutes
    
    def determine_difficulty(self, content: str, path: str) -> str:
        """确定文档难度"""
        # 根据路径和内容判断
        if "Struct/" in path:
            if "proofs/" in path.lower():
                return "Advanced"
            return "Intermediate"
        elif "Flink/" in path:
            if "core-mechanisms" in path.lower():
                return "Intermediate"
            return "Beginner"
        elif "Knowledge/" in path:
            if "design-patterns" in path.lower():
                return "Intermediate"
            return "Beginner"
        
        # 根据内容关键词
        if re.search(r'定理|证明|Theorem|Proof|Formal', content):
            return "Advanced"
        elif re.search(r'模式|Pattern|架构|Architecture', content):
            return "Intermediate"
        
        return "Beginner"
    
    def process_document(self, file_path: Path) -> Optional[DocumentSummary]:
        """处理单个文档"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 提取标题
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else file_path.stem
            
            rel_path = str(file_path.relative_to(PROJECT_ROOT))
            doc_id = hashlib.md5(rel_path.encode()).hexdigest()[:12]
            
            summary = DocumentSummary(
                doc_id=doc_id,
                path=rel_path,
                title=title,
                summary=self.extract_first_paragraph(content),
                key_points=self.extract_key_points(content),
                theorems=self.extract_theorems(content),
                definitions=self.extract_definitions(content),
                related_docs=self.extract_related_docs(content),
                reading_time=self.estimate_reading_time(content),
                difficulty=self.determine_difficulty(content, rel_path),
                last_updated=datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            )
            
            return summary
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
    
    def scan_and_process(self, limit: Optional[int] = None):
        """扫描并处理所有文档"""
        print("📄 Scanning documents...")
        
        doc_files = []
        for scan_dir in SCAN_DIRS:
            dir_path = PROJECT_ROOT / scan_dir
            if dir_path.exists():
                doc_files.extend(dir_path.rglob("*.md"))
        
        # 添加根目录文件
        doc_files.extend(PROJECT_ROOT.glob("*.md"))
        
        doc_files = sorted(set(doc_files))
        if limit:
            doc_files = doc_files[:limit]
        
        print(f"   Found {len(doc_files)} documents")
        
        for i, file_path in enumerate(doc_files, 1):
            summary = self.process_document(file_path)
            if summary:
                self.summaries.append(summary)
            if i % 50 == 0:
                print(f"   Processed {i}/{len(doc_files)}")
        
        print(f"✅ Generated {len(self.summaries)} summaries")
    
    def save_summaries(self):
        """保存摘要文件"""
        # 保存每个摘要
        for summary in self.summaries:
            output_file = SUMMARIES_DIR / f"{summary.doc_id}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(summary.to_dict(), f, ensure_ascii=False, indent=2)
        
        # 保存索引
        index = {
            "version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "total_summaries": len(self.summaries),
            "summaries": [
                {
                    "id": s.doc_id,
                    "path": s.path,
                    "title": s.title,
                    "difficulty": s.difficulty,
                    "reading_time": s.reading_time
                }
                for s in self.summaries
            ]
        }
        
        with open(INDEX_OUTPUT, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Summaries saved to {SUMMARIES_DIR}")
        print(f"💾 Index saved to {INDEX_OUTPUT}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate document summaries for AnalysisDataFlow',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--limit', '-l', type=int, help='Limit number of documents to process')
    parser.add_argument('--doc', '-d', help='Process specific document only')
    
    args = parser.parse_args()
    
    generator = SummaryGenerator()
    
    if args.doc:
        # 处理单个文档
        doc_path = PROJECT_ROOT / args.doc
        if doc_path.exists():
            summary = generator.process_document(doc_path)
            if summary:
                print(json.dumps(summary.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(f"Document not found: {args.doc}")
    else:
        # 批量处理
        generator.scan_and_process(limit=args.limit)
        generator.save_summaries()
        
        # 统计
        difficulties = {}
        total_reading_time = 0
        for s in generator.summaries:
            difficulties[s.difficulty] = difficulties.get(s.difficulty, 0) + 1
            total_reading_time += s.reading_time
        
        print(f"\n📊 Summary Statistics:")
        print(f"  Total documents: {len(generator.summaries)}")
        print(f"  Total reading time: {total_reading_time} minutes")
        print(f"  Difficulty distribution:")
        for diff, count in sorted(difficulties.items()):
            print(f"    {diff}: {count}")


if __name__ == '__main__':
    main()
