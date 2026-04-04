#!/usr/bin/env python3
"""
问答机器人知识库构建器 - 自动生成FAQ和问答对
功能：
1. 从文档中提取问答对
2. 生成FAQ条目
3. 构建知识库索引
4. 提供问答匹配接口

用法：
    python qa-bot-knowledge-base.py --build --source Struct/ --output qa-kb/
    python qa-bot-knowledge-base.py --ask "什么是Checkpoint?"
    python qa-bot-knowledge-base.py --generate-faq --output FAQ-AI-GENERATED.md
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from difflib import SequenceMatcher

# 尝试导入可选依赖
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


@dataclass
class QAEntry:
    """问答条目"""
    question: str
    answer: str
    source_doc: str
    category: str
    tags: List[str]
    confidence: float = 1.0
    related_questions: List[str] = None
    
    def __post_init__(self):
        if self.related_questions is None:
            self.related_questions = []


@dataclass
class FAQSection:
    """FAQ章节"""
    title: str
    description: str
    entries: List[QAEntry]


class QuestionExtractor:
    """问题提取器"""
    
    # 常见问答模式
    QA_PATTERNS = [
        # 显式Q&A
        (r'(?:Q[:：]|问题[:：])\s*(.+?)\s*(?:A[:：]|答案[:：])\s*(.+?)(?=\n\s*(?:Q[:：]|问题[:：])|$)', 'explicit'),
        # FAQ格式
        (r'[-*]\s*\*\*(.+?)\*\*[:：]?\s*\n\s*(.+?)(?=\n\s*[-*]\s*\*\*|$)', 'faq'),
        # 什么是...
        (r'(?:^|\n)\s*###?\s*(什么是| how (?:is|are|does)|what (?:is|are))\s+(.+?)\s*\n\s*(.+?)(?=\n\s*###?\s*(?:什么是|how|what)|$)', 'definition'),
    ]
    
    # 常见技术问题模板
    QUESTION_TEMPLATES = [
        "什么是{concept}?",
        "{concept}的工作原理是什么?",
        "如何使用{concept}?",
        "{concept}和{alternative}有什么区别?",
        "{concept}的最佳实践是什么?",
        "什么时候应该使用{concept}?",
        "{concept}的优缺点是什么?",
        "如何排查{concept}相关问题?",
    ]
    
    def extract_from_document(self, content: str, doc_path: str) -> List[QAEntry]:
        """从文档中提取问答对"""
        entries = []
        
        for pattern, pattern_type in self.QA_PATTERNS:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                if pattern_type == 'explicit':
                    question, answer = match
                elif pattern_type == 'faq':
                    question, answer = match
                elif pattern_type == 'definition':
                    prefix, concept, answer = match
                    question = f"{prefix}{concept}"
                else:
                    continue
                
                # 清理文本
                question = self._clean_text(question)
                answer = self._clean_text(answer)
                
                if len(question) > 10 and len(answer) > 20:
                    entries.append(QAEntry(
                        question=question,
                        answer=answer[:500] + "..." if len(answer) > 500 else answer,
                        source_doc=doc_path,
                        category=self._categorize(question),
                        tags=self._extract_tags(question, answer)
                    ))
        
        return entries
    
    def generate_from_concepts(self, concepts: List[Dict], doc_path: str) -> List[QAEntry]:
        """从概念列表生成问答对"""
        entries = []
        
        for concept in concepts:
            name = concept.get('term', '')
            if not name or len(name) < 3:
                continue
            
            # 为每个概念生成基础问题
            for template in self.QUESTION_TEMPLATES[:3]:  # 只取前3个模板
                question = template.format(concept=name, alternative="其他方案")
                answer = f"{name} 是流计算领域的重要概念。详见 {doc_path}"
                
                entries.append(QAEntry(
                    question=question,
                    answer=answer,
                    source_doc=doc_path,
                    category="concept",
                    tags=[name.lower(), "generated"]
                ))
        
        return entries
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        text = re.sub(r'\*+', '', text)  # 移除Markdown强调
        text = re.sub(r'\n+', ' ', text)  # 合并换行
        text = re.sub(r'\s+', ' ', text)  # 合并空格
        return text.strip()
    
    def _categorize(self, question: str) -> str:
        """分类问题"""
        question_lower = question.lower()
        
        if any(kw in question_lower for kw in ['什么', 'what', '定义', 'definition']):
            return 'definition'
        elif any(kw in question_lower for kw in ['如何', 'how', '使用', 'use']):
            return 'howto'
        elif any(kw in question_lower for kw in ['区别', 'difference', '比较', 'vs']):
            return 'comparison'
        elif any(kw in question_lower for kw in ['为什么', 'why', '原理', 'work']):
            return 'concept'
        elif any(kw in question_lower for kw in ['问题', 'problem', '错误', 'error', '排查']):
            return 'troubleshooting'
        else:
            return 'general'
    
    def _extract_tags(self, question: str, answer: str) -> List[str]:
        """提取标签"""
        text = question + " " + answer
        tags = set()
        
        # 技术关键词
        keywords = [
            'flink', 'checkpoint', 'watermark', 'state', 'window',
            'streaming', 'batch', 'sql', 'table', 'api',
            'actor', 'csp', 'dataflow', 'parallelism', 'backpressure'
        ]
        
        for kw in keywords:
            if kw in text.lower():
                tags.add(kw)
        
        return list(tags)[:5]


class FAQGenerator:
    """FAQ生成器"""
    
    CATEGORIES = {
        'getting-started': '入门指南',
        'concepts': '核心概念',
        'configuration': '配置指南',
        'troubleshooting': '问题排查',
        'performance': '性能优化',
        'advanced': '高级主题'
    }
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.extractor = QuestionExtractor()
    
    def build_knowledge_base(self, source_dir: str, output_dir: str):
        """构建知识库"""
        print(f"正在构建知识库: {source_dir}")
        
        source_path = Path(source_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        all_entries: List[QAEntry] = []
        
        # 扫描所有Markdown文件
        for md_file in source_path.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                rel_path = str(md_file.relative_to(source_path))
                
                # 提取问答对
                entries = self.extractor.extract_from_document(content, rel_path)
                all_entries.extend(entries)
                
                print(f"  ✓ {rel_path}: {len(entries)} 个问答对")
                
            except Exception as e:
                print(f"  ✗ {md_file}: {e}")
        
        # 去重
        all_entries = self._deduplicate(all_entries)
        
        # 保存知识库
        self._save_knowledge_base(all_entries, output_path)
        
        print(f"\n知识库构建完成!")
        print(f"  - 总条目数: {len(all_entries)}")
    
    def _deduplicate(self, entries: List[QAEntry]) -> List[QAEntry]:
        """去重"""
        unique_entries = []
        seen_questions = set()
        
        for entry in entries:
            # 使用问题的前30个字符作为键
            key = entry.question[:30].lower()
            if key not in seen_questions:
                seen_questions.add(key)
                unique_entries.append(entry)
        
        return unique_entries
    
    def _save_knowledge_base(self, entries: List[QAEntry], output_path: Path):
        """保存知识库"""
        # 保存JSON格式
        kb_data = {
            'version': '1.0',
            'total_entries': len(entries),
            'categories': {},
            'entries': [asdict(e) for e in entries]
        }
        
        # 按分类统计
        for entry in entries:
            cat = entry.category
            if cat not in kb_data['categories']:
                kb_data['categories'][cat] = 0
            kb_data['categories'][cat] += 1
        
        with open(output_path / 'knowledge-base.json', 'w', encoding='utf-8') as f:
            json.dump(kb_data, f, ensure_ascii=False, indent=2)
        
        # 生成Markdown FAQ
        self._generate_markdown_faq(entries, output_path / 'FAQ-AI-GENERATED.md')
    
    def _generate_markdown_faq(self, entries: List[QAEntry], output_path: Path):
        """生成Markdown格式的FAQ"""
        # 按分类组织
        by_category: Dict[str, List[QAEntry]] = {}
        for entry in entries:
            cat = entry.category
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(entry)
        
        # 生成文档
        md_content = """# 自动生成的FAQ

> 本FAQ由AI自动从项目文档中提取生成
> 生成时间: {timestamp}

## 目录

""".format(timestamp=self._get_timestamp())
        
        # 生成目录
        for category in sorted(by_category.keys()):
            md_content += f"- [{category}](#{category})\n"
        
        md_content += "\n---\n\n"
        
        # 生成各分类内容
        for category in sorted(by_category.keys()):
            md_content += f"## {category}\n\n"
            
            for i, entry in enumerate(by_category[category][:20], 1):  # 每类最多20个
                md_content += f"### Q{i}: {entry.question}\n\n"
                md_content += f"{entry.answer}\n\n"
                md_content += f"*来源: [{entry.source_doc}](../{entry.source_doc})*\n\n"
                if entry.tags:
                    md_content += f"*标签: {', '.join(entry.tags)}*\n\n"
                md_content += "---\n\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"  FAQ已保存到: {output_path}")
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def answer_question(self, question: str, knowledge_base_path: str) -> Optional[QAEntry]:
        """回答问题"""
        # 加载知识库
        kb_path = Path(knowledge_base_path) / 'knowledge-base.json'
        
        if not kb_path.exists():
            print(f"错误: 知识库不存在: {kb_path}")
            return None
        
        with open(kb_path, 'r', encoding='utf-8') as f:
            kb_data = json.load(f)
        
        entries = [QAEntry(**e) for e in kb_data['entries']]
        
        # 查找最佳匹配
        best_match = None
        best_score = 0.0
        
        for entry in entries:
            score = self._calculate_similarity(question, entry.question)
            if score > best_score:
                best_score = score
                best_match = entry
        
        if best_match and best_score > 0.3:
            best_match.confidence = best_score
            return best_match
        
        return None
    
    def _calculate_similarity(self, q1: str, q2: str) -> float:
        """计算问题相似度"""
        # 使用序列匹配
        return SequenceMatcher(None, q1.lower(), q2.lower()).ratio()
    
    def generate_enhanced_answer(self, question: str, context: str) -> str:
        """使用LLM生成增强答案"""
        if not HAS_OPENAI or not self.api_key:
            return context
        
        try:
            client = openai.OpenAI(api_key=self.api_key)
            
            prompt = f"""基于以下参考信息，回答用户问题。如果参考信息不足，请说明。

用户问题: {question}

参考信息:
{context}

请提供简洁、准确的回答（300字以内）："""
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是流计算领域的技术专家。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"LLM调用失败: {e}", file=sys.stderr)
            return context


def print_qa_result(entry: QAEntry, query: str):
    """打印问答结果"""
    print(f"\n{'='*70}")
    print(f"❓ 问题: \"{query}\"")
    print(f"{'='*70}")
    
    if entry:
        print(f"\n💡 匹配问题: {entry.question}")
        print(f"   置信度: {entry.confidence:.2%}")
        print(f"\n📖 答案:\n{entry.answer}")
        print(f"\n📄 来源: {entry.source_doc}")
        if entry.tags:
            print(f"🏷️  标签: {', '.join(entry.tags)}")
    else:
        print("\n未找到匹配答案。请尝试其他表述。")
    
    print(f"{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description="问答机器人知识库构建器 - 自动生成FAQ",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --build --source . --output qa-kb/
  %(prog)s --ask "什么是Checkpoint?" --kb qa-kb/
  %(prog)s --interactive --kb qa-kb/
  %(prog)s --generate-faq --source Struct/ --output FAQ.md
        """
    )
    
    parser.add_argument('--source', '-s', default='.',
                       help='源文档目录')
    parser.add_argument('--output', '-o', default='qa-kb',
                       help='输出目录')
    parser.add_argument('--kb', '-k', default='qa-kb',
                       help='知识库目录')
    
    # 命令
    parser.add_argument('--build', action='store_true',
                       help='构建知识库')
    parser.add_argument('--ask', '-q',
                       help='提问')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='交互模式')
    parser.add_argument('--generate-faq', action='store_true',
                       help='生成FAQ文档')
    parser.add_argument('--enhance', '-e', action='store_true',
                       help='使用LLM增强答案')
    parser.add_argument('--api-key', help='OpenAI API密钥')
    
    args = parser.parse_args()
    
    # 初始化生成器
    generator = FAQGenerator(api_key=args.api_key)
    
    if args.build:
        # 构建知识库
        generator.build_knowledge_base(args.source, args.output)
    
    elif args.generate_faq:
        # 生成FAQ
        generator.build_knowledge_base(args.source, args.output)
    
    elif args.ask:
        # 回答问题
        entry = generator.answer_question(args.ask, args.kb)
        
        if entry and args.enhance:
            entry.answer = generator.generate_enhanced_answer(args.ask, entry.answer)
        
        print_qa_result(entry, args.ask)
    
    elif args.interactive:
        # 交互模式
        print("="*70)
        print("🤖 问答机器人 (输入 'quit' 退出)")
        print("="*70)
        
        while True:
            try:
                question = input("\n❓ 你的问题: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("再见!")
                    break
                
                if not question:
                    continue
                
                entry = generator.answer_question(question, args.kb)
                
                if entry and args.enhance:
                    entry.answer = generator.generate_enhanced_answer(question, entry.answer)
                
                print_qa_result(entry, question)
                
            except KeyboardInterrupt:
                print("\n再见!")
                break
            except Exception as e:
                print(f"错误: {e}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
