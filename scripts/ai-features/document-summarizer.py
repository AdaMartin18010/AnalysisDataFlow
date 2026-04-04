#!/usr/bin/env python3
"""
文档摘要生成器 - AI辅助文档分析工具
功能：
1. 使用LLM API生成文档摘要
2. 提取关键概念和定理
3. 支持翻译功能
4. 批量处理多篇文档

用法：
    python document-summarizer.py --input README.md
    python document-summarizer.py --input Struct/01-foundation/ --batch
    python document-summarizer.py --input README.md --translate --target-lang en
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib

# 尝试导入可选依赖
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


@dataclass
class DocumentSummary:
    """文档摘要数据结构"""
    title: str
    summary: str
    key_concepts: List[Dict[str, str]]
    theorems: List[Dict[str, str]]
    definitions: List[Dict[str, str]]
    word_count: int
    reading_time_minutes: int
    difficulty_score: int  # 1-10
    prerequisites: List[str]
    related_docs: List[str]


class DocumentSummarizer:
    """文档摘要生成器"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.cache_dir = Path(".cache/summaries")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_cache_path(self, file_path: str) -> Path:
        """获取缓存文件路径"""
        file_hash = hashlib.md5(file_path.encode()).hexdigest()
        return self.cache_dir / f"{file_hash}.json"
    
    def _load_cache(self, file_path: str) -> Optional[DocumentSummary]:
        """加载缓存的摘要"""
        cache_path = self._get_cache_path(file_path)
        if cache_path.exists():
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return DocumentSummary(**data)
        return None
    
    def _save_cache(self, file_path: str, summary: DocumentSummary):
        """保存摘要到缓存"""
        cache_path = self._get_cache_path(file_path)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(summary.__dict__, f, ensure_ascii=False, indent=2)
    
    def _extract_title(self, content: str) -> str:
        """提取文档标题"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return "Untitled"
    
    def _extract_theorems(self, content: str) -> List[Dict[str, str]]:
        """提取定理和定义"""
        theorems = []
        
        # 匹配定理格式: **Thm-S-01-01** 或 **定理**
        theorem_patterns = [
            (r'\*\*(Thm-[A-Z]-\d{2}-\d{2})\*\*[:：]\s*(.+?)(?=\n\n|\Z)', 'theorem'),
            (r'\*\*(Def-[A-Z]-\d{2}-\d{2})\*\*[:：]\s*(.+?)(?=\n\n|\Z)', 'definition'),
            (r'\*\*(Lemma-[A-Z]-\d{2}-\d{2})\*\*[:：]\s*(.+?)(?=\n\n|\Z)', 'lemma'),
            (r'\*\*(Prop-[A-Z]-\d{2}-\d{2})\*\*[:：]\s*(.+?)(?=\n\n|\Z)', 'proposition'),
        ]
        
        for pattern, kind in theorem_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                if isinstance(match, tuple):
                    ref, statement = match
                    theorems.append({
                        'reference': ref,
                        'type': kind,
                        'statement': statement.strip()[:200] + '...' if len(statement) > 200 else statement.strip()
                    })
        
        return theorems
    
    def _extract_key_concepts(self, content: str) -> List[Dict[str, str]]:
        """提取关键概念"""
        concepts = []
        
        # 匹配加粗术语
        bold_terms = re.findall(r'\*\*([^*]+?)\*\*', content)
        term_freq = {}
        for term in bold_terms:
            if len(term) > 2 and len(term) < 50:
                term_freq[term] = term_freq.get(term, 0) + 1
        
        # 选择高频术语
        top_terms = sorted(term_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        for term, freq in top_terms:
            concepts.append({
                'term': term,
                'frequency': freq,
                'category': self._categorize_term(term, content)
            })
        
        return concepts
    
    def _categorize_term(self, term: str, content: str) -> str:
        """对术语进行分类"""
        # 简单启发式分类
        if any(kw in term.lower() for kw in ['定理', 'theorem', 'lemma', 'corollary']):
            return 'theorem'
        elif any(kw in term.lower() for kw in ['定义', 'definition']):
            return 'definition'
        elif any(kw in term.lower() for kw in ['算法', 'algorithm']):
            return 'algorithm'
        elif any(kw in term.lower() for kw in ['模型', 'model']):
            return 'model'
        else:
            return 'concept'
    
    def _calculate_difficulty(self, content: str) -> int:
        """计算文档难度评分 (1-10)"""
        score = 5  # 基础分
        
        # 形式化元素越多越难
        formal_elements = len(re.findall(r'\*\*(Thm|Def|Lemma|Prop)-[A-Z]-\d{2}-\d{2}\*\*', content))
        score += min(formal_elements // 5, 3)
        
        # 数学公式越多越难
        math_formulas = len(re.findall(r'\$[^$]+\$', content))
        score += min(math_formulas // 10, 2)
        
        # 代码示例降低难度
        code_blocks = len(re.findall(r'```', content))
        score -= min(code_blocks // 4, 2)
        
        return max(1, min(10, score))
    
    def _extract_prerequisites(self, content: str) -> List[str]:
        """提取前置依赖"""
        prereqs = []
        
        # 查找前置依赖标记
        match = re.search(r'前置依赖[:：]\s*\[(.+?)\]', content)
        if match:
            deps = match.group(1).split(',')
            prereqs = [d.strip() for d in deps]
        
        return prereqs
    
    def _generate_summary_with_llm(self, content: str, max_length: int = 500) -> str:
        """使用LLM生成摘要"""
        if not HAS_OPENAI or not self.api_key:
            # 降级为启发式摘要
            return self._generate_heuristic_summary(content, max_length)
        
        try:
            client = openai.OpenAI(api_key=self.api_key)
            
            prompt = f"""请为以下技术文档生成简洁的摘要（200字以内）：

文档内容（前3000字符）：
{content[:3000]}

要求：
1. 概括核心主题和主要内容
2. 突出关键技术点
3. 说明文档的实用价值
4. 使用中文回答

摘要："""
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的技术文档分析助手。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"LLM API调用失败: {e}", file=sys.stderr)
            return self._generate_heuristic_summary(content, max_length)
    
    def _generate_heuristic_summary(self, content: str, max_length: int = 500) -> str:
        """启发式生成摘要"""
        lines = content.split('\n')
        
        # 收集关键句
        summary_sentences = []
        
        for line in lines[:50]:  # 只看前50行
            line = line.strip()
            # 跳过标题和空行
            if not line or line.startswith('#') or line.startswith('```'):
                continue
            # 选择包含关键信息的句子
            if any(kw in line for kw in ['是', '定义', '理论', '模型', '本文']):
                if len(line) > 20 and len(line) < 200:
                    summary_sentences.append(line)
            if len(summary_sentences) >= 3:
                break
        
        summary = ' '.join(summary_sentences)
        return summary[:max_length] if len(summary) > max_length else summary
    
    def summarize(self, file_path: str, use_cache: bool = True, use_llm: bool = True) -> DocumentSummary:
        """生成文档摘要"""
        # 检查缓存
        if use_cache:
            cached = self._load_cache(file_path)
            if cached:
                print(f"  [缓存] 使用缓存摘要: {file_path}")
                return cached
        
        # 读取文档
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"  [分析] 正在分析: {file_path}")
        
        # 提取信息
        title = self._extract_title(content)
        theorems = self._extract_theorems(content)
        concepts = self._extract_key_concepts(content)
        difficulty = self._calculate_difficulty(content)
        prereqs = self._extract_prerequisites(content)
        
        # 生成摘要
        if use_llm:
            summary_text = self._generate_summary_with_llm(content)
        else:
            summary_text = self._generate_heuristic_summary(content)
        
        # 统计信息
        word_count = len(content)
        reading_time = max(1, word_count // 800)  # 假设800字/分钟
        
        # 提取相关文档
        related = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)
        related_docs = [r[1] for r in related[:10]]
        
        summary = DocumentSummary(
            title=title,
            summary=summary_text,
            key_concepts=concepts[:10],
            theorems=theorems[:10],
            definitions=[t for t in theorems if t.get('type') == 'definition'][:10],
            word_count=word_count,
            reading_time_minutes=reading_time,
            difficulty_score=difficulty,
            prerequisites=prereqs,
            related_docs=related_docs
        )
        
        # 保存缓存
        if use_cache:
            self._save_cache(file_path, summary)
        
        return summary
    
    def generate_index(self, directory: str, output: str = "index-summary.json"):
        """为目录生成摘要索引"""
        path = Path(directory)
        summaries = {}
        
        print(f"正在扫描目录: {directory}")
        
        for md_file in path.rglob("*.md"):
            rel_path = str(md_file.relative_to(Path.cwd()))
            try:
                summary = self.summarize(str(md_file))
                summaries[rel_path] = summary.__dict__
                print(f"  ✓ {rel_path}")
            except Exception as e:
                print(f"  ✗ {rel_path}: {e}")
        
        # 保存索引
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(summaries, f, ensure_ascii=False, indent=2)
        
        print(f"\n索引已保存到: {output}")
        print(f"总计: {len(summaries)} 篇文档")
    
    def print_summary(self, summary: DocumentSummary):
        """打印摘要信息"""
        print(f"\n{'='*60}")
        print(f"📄 文档: {summary.title}")
        print(f"{'='*60}")
        print(f"\n📝 摘要:")
        print(f"   {summary.summary}")
        print(f"\n📊 统计:")
        print(f"   - 字数: {summary.word_count:,}")
        print(f"   - 阅读时间: {summary.reading_time_minutes} 分钟")
        print(f"   - 难度评分: {summary.difficulty_score}/10")
        print(f"\n🔑 关键概念 ({len(summary.key_concepts)}个):")
        for concept in summary.key_concepts[:5]:
            print(f"   • {concept['term']} ({concept['category']}, 出现{concept['frequency']}次)")
        print(f"\n📐 定理/定义 ({len(summary.theorems)}个):")
        for theorem in summary.theorems[:5]:
            print(f"   • {theorem['reference']}: {theorem['statement'][:60]}...")
        if summary.prerequisites:
            print(f"\n🔗 前置依赖:")
            for prereq in summary.prerequisites:
                print(f"   • {prereq}")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="文档摘要生成器 - 分析技术文档并生成结构化摘要",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --input README.md                    # 单文档摘要
  %(prog)s --input Struct/ --batch             # 批量处理
  %(prog)s --input README.md --format json     # JSON输出
  %(prog)s --index Struct/ --output index.json # 生成索引
        """
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入文件或目录路径')
    parser.add_argument('--batch', '-b', action='store_true', help='批量处理目录')
    parser.add_argument('--index', action='store_true', help='生成索引文件')
    parser.add_argument('--output', '-o', default='summary.json', help='输出文件路径')
    parser.add_argument('--format', '-f', choices=['text', 'json', 'markdown'], 
                       default='text', help='输出格式')
    parser.add_argument('--no-cache', action='store_true', help='禁用缓存')
    parser.add_argument('--no-llm', action='store_true', help='不使用LLM API')
    parser.add_argument('--api-key', help='OpenAI API密钥')
    parser.add_argument('--model', default='gpt-4', help='LLM模型名称')
    
    args = parser.parse_args()
    
    # 初始化摘要器
    summarizer = DocumentSummarizer(
        api_key=args.api_key,
        model=args.model
    )
    
    if args.index:
        # 生成索引
        summarizer.generate_index(args.input, args.output)
    
    elif args.batch or Path(args.input).is_dir():
        # 批量处理
        path = Path(args.input)
        results = []
        
        print(f"批量处理目录: {args.input}\n")
        
        for md_file in path.rglob("*.md"):
            try:
                summary = summarizer.summarize(
                    str(md_file), 
                    use_cache=not args.no_cache,
                    use_llm=not args.no_llm
                )
                results.append((str(md_file), summary))
                
                if args.format == 'text':
                    summarizer.print_summary(summary)
                    
            except Exception as e:
                print(f"错误处理 {md_file}: {e}", file=sys.stderr)
        
        if args.format == 'json':
            output = {path: summary.__dict__ for path, summary in results}
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print(f"\n结果已保存到: {args.output}")
    
    else:
        # 单文件处理
        summary = summarizer.summarize(
            args.input,
            use_cache=not args.no_cache,
            use_llm=not args.no_llm
        )
        
        if args.format == 'text':
            summarizer.print_summary(summary)
        elif args.format == 'json':
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(summary.__dict__, f, ensure_ascii=False, indent=2)
            print(f"摘要已保存到: {args.output}")
        elif args.format == 'markdown':
            md_content = f"""# {summary.title} - 文档摘要

## 概述

{summary.summary}

## 文档统计

| 指标 | 值 |
|------|-----|
| 字数 | {summary.word_count:,} |
| 阅读时间 | {summary.reading_time_minutes} 分钟 |
| 难度评分 | {summary.difficulty_score}/10 |

## 关键概念

"""
            for concept in summary.key_concepts:
                md_content += f"- **{concept['term']}** ({concept['category']})\n"
            
            md_content += "\n## 定理与定义\n\n"
            for theorem in summary.theorems[:10]:
                md_content += f"- **{theorem['reference']}** ({theorem['type']}): {theorem['statement'][:100]}...\n"
            
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"Markdown摘要已保存到: {args.output}")


if __name__ == "__main__":
    main()
