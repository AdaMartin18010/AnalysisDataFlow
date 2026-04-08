#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档摘要生成器 - Document Summarizer for AnalysisDataFlow
基于本地规则分析生成结构化摘要，无需API Key

功能:
- 读取 Markdown 文档
- 生成结构化摘要 (遵循六段式)
- 提取关键术语和定义
- 生成 Mermaid 图建议
- 建议相关文档链接
"""

import os
import re
import sys
import json
import yaml
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from collections import Counter


@dataclass
class DocumentSummary:
    """文档摘要数据结构"""
    title: str
    filepath: str
    formal_level: str
    timestamp: str
    content_summary: str
    sections_status: Dict[str, Dict]
    definitions: List[Dict]
    theorems: List[Dict]
    key_terms: List[str]
    mermaid_blocks: List[str]
    references: List[str]
    suggestions: List[str]
    mermaid_suggestions: List[str]


class DocumentAnalyzer:
    """文档分析器"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.patterns = self._compile_patterns()
        self.logger = self._setup_logger()
    
    def _load_config(self, config_path: str = None) -> Dict:
        """加载配置文件"""
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__), 'config.yaml'
            )
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load config: {e}")
            return {}
    
    def _compile_patterns(self) -> Dict:
        """编译正则表达式模式"""
        patterns = self.config.get('patterns', {})
        compiled = {}
        for key, pattern in patterns.items():
            try:
                compiled[key] = re.compile(pattern, re.MULTILINE)
            except re.error:
                compiled[key] = None
        return compiled
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger('doc-summarizer')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def read_document(self, filepath: str) -> str:
        """读取文档内容"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Failed to read {filepath}: {e}")
            return ""
    
    def extract_title(self, content: str) -> str:
        """提取文档标题"""
        # 匹配 # 开头的标题
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return "Untitled"
    
    def extract_formal_level(self, content: str) -> str:
        """提取形式化等级"""
        # 匹配 > 所属阶段行中的形式化等级
        match = re.search(r'形式化等级:\s*(L[1-6](?:-[A-Z]+)?)', content)
        if match:
            return match.group(1)
        return "Unknown"
    
    def extract_sections(self, content: str) -> Dict[str, Dict]:
        """分析文档六段式结构"""
        sections = {}
        doc_structure = self.config.get('document_structure', {}).get('sections', [])
        
        for section in doc_structure:
            section_name = section['name']
            section_id = section['id']
            patterns = section.get('patterns', [])
            
            found = False
            content_preview = ""
            
            for pattern in patterns:
                # 查找章节
                regex = re.compile(
                    rf'{re.escape(pattern)}\s*\n(.*?)(?=^##\s|\Z)',
                    re.MULTILINE | re.DOTALL
                )
                match = regex.search(content)
                if match:
                    found = True
                    section_content = match.group(1).strip()
                    # 计算内容量 (字符数)
                    content_length = len(section_content)
                    # 取前200字符作为预览
                    content_preview = section_content[:200].replace('\n', ' ')
                    sections[section_id] = {
                        'name': section_name,
                        'found': True,
                        'content_length': content_length,
                        'preview': content_preview + ('...' if len(section_content) > 200 else '')
                    }
                    break
            
            if not found:
                sections[section_id] = {
                    'name': section_name,
                    'found': False,
                    'content_length': 0,
                    'preview': '[缺失]'
                }
        
        return sections
    
    def extract_definitions(self, content: str) -> List[Dict]:
        """提取定义 (Def-*)"""
        definitions = []
        pattern = r'\*\*(Def-[SKF]-\d{2}-\d{2})\*\*[:\s]+(.+?)(?=\n\n|\Z|\*\*Def-)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches[:20]:  # 最多20个
            def_id = match[0]
            def_text = match[1].strip().replace('\n', ' ')
            # 截取前150字符
            if len(def_text) > 150:
                def_text = def_text[:150] + '...'
            definitions.append({
                'id': def_id,
                'text': def_text
            })
        
        return definitions
    
    def extract_theorems(self, content: str) -> List[Dict]:
        """提取定理 (Thm-*)"""
        theorems = []
        pattern = r'\*\*(Thm-[SKF]-\d{2}-\d{2})\*\*[:\s]+(.+?)(?=\n\n|\Z|\*\*(?:Thm|Def|Lemma|Prop|Cor)-)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches[:20]:  # 最多20个
            thm_id = match[0]
            thm_text = match[1].strip().replace('\n', ' ')
            if len(thm_text) > 150:
                thm_text = thm_text[:150] + '...'
            theorems.append({
                'id': thm_id,
                'text': thm_text
            })
        
        return theorems
    
    def extract_lemmas(self, content: str) -> List[Dict]:
        """提取引理 (Lemma-*)"""
        lemmas = []
        pattern = r'\*\*(Lemma-[SKF]-\d{2}-\d{2})\*\*[:\s]+(.+?)(?=\n\n|\Z|\*\*(?:Thm|Def|Lemma|Prop|Cor)-)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches[:15]:
            lemmas.append({
                'id': match[0],
                'text': match[1].strip().replace('\n', ' ')[:150]
            })
        
        return lemmas
    
    def extract_mermaid_blocks(self, content: str) -> List[str]:
        """提取 Mermaid 图块"""
        pattern = r'```mermaid\s*\n([\s\S]*?)```'
        matches = re.findall(pattern, content)
        return matches
    
    def extract_references(self, content: str) -> List[str]:
        """提取引用"""
        pattern = r'\[\^(\d+)\]:\s*(.+?)(?=\n\[\^|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        return [f"[{ref_id}]: {text.strip()[:100]}" for ref_id, text in matches]
    
    def extract_key_terms(self, content: str) -> List[str]:
        """提取关键词"""
        # 提取加粗术语
        bold_terms = re.findall(r'\*\*([^*]+?)\*\*', content)
        # 提取代码术语
        code_terms = re.findall(r'`([^`]+)`', content)
        
        all_terms = bold_terms + code_terms
        
        # 过滤停用词和短词
        stopwords = set(['的', '是', '在', '和', '了', '与', '为', 'the', 'is', 'and', 'of'])
        filtered = [
            t for t in all_terms 
            if len(t) > 2 and t not in stopwords and not t.startswith('Thm-') 
            and not t.startswith('Def-') and not t.startswith('Lemma-')
        ]
        
        # 统计频率
        counter = Counter(filtered)
        # 返回最常见的10个
        return [term for term, _ in counter.most_common(10)]
    
    def generate_content_summary(self, content: str, sections: Dict) -> str:
        """生成内容摘要"""
        # 基于定义部分生成摘要
        definitions = self.extract_definitions(content)
        theorems = self.extract_theorems(content)
        
        summary_parts = []
        
        # 提取首段
        first_para = content.split('\n\n')[0] if content else ""
        if first_para.startswith('#'):
            first_para = ''
        
        if first_para:
            summary_parts.append(f"本文档探讨{first_para[:100]}...")
        
        if definitions:
            summary_parts.append(f"\n核心定义包括：{', '.join([d['id'] for d in definitions[:3]])}")
        
        if theorems:
            summary_parts.append(f"主要定理：{', '.join([t['id'] for t in theorems[:3]])}")
        
        # 统计章节完整性
        total_sections = len(sections)
        completed_sections = sum(1 for s in sections.values() if s['found'])
        
        summary_parts.append(
            f"\n文档结构完整性：{completed_sections}/{total_sections} 章节已完善"
        )
        
        return '\n'.join(summary_parts)
    
    def generate_suggestions(self, sections: Dict, definitions: List, 
                           theorems: List, mermaid_blocks: List) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        # 检查章节完整性
        for section_id, section_info in sections.items():
            if not section_info['found']:
                suggestions.append(f"⚠️ 缺失章节: {section_info['name']} ({section_id})")
            elif section_info['content_length'] < 100:
                suggestions.append(
                    f"⚡ 章节内容较短: {section_info['name']} "
                    f"({section_info['content_length']} 字符)，建议扩展"
                )
        
        # 检查定义数量
        if len(definitions) < 1:
            suggestions.append("⚠️ 建议添加至少一个形式化定义 (Def-*)")
        
        # 检查定理数量
        if len(theorems) < 1:
            suggestions.append("💡 可考虑添加定理或命题以增强严谨性")
        
        # 检查 Mermaid 图
        if len(mermaid_blocks) < 1:
            suggestions.append("📊 建议添加 Mermaid 可视化图以提升可读性")
        
        # 完整性检查
        completed = sum(1 for s in sections.values() if s['found'])
        if completed == len(sections):
            suggestions.append("✅ 所有必需章节已存在，文档结构完整")
        
        return suggestions
    
    def suggest_mermaid_diagrams(self, content: str, sections: Dict) -> List[str]:
        """生成 Mermaid 图建议"""
        suggestions = []
        
        # 检查内容特征并建议相应图表
        content_lower = content.lower()
        
        # 如果有定义和关系，建议概念图
        if sections.get('definitions', {}).get('found') and \
           sections.get('relations', {}).get('found'):
            suggestions.append("""
### 建议 1: 概念层次图 (graph TD)
展示核心概念之间的层次关系：

```mermaid
graph TD
    A[核心概念] --> B[子概念1]
    A --> C[子概念2]
    B --> D[属性A]
    C --> E[属性B]
    style A fill:#f96,stroke:#333
```
""")
        
        # 如果有证明过程，建议流程图
        if sections.get('proof', {}).get('found'):
            suggestions.append("""
### 建议 2: 证明流程图 (flowchart TD)
展示定理证明的逻辑流程：

```mermaid
flowchart TD
    Start([开始]) --> Premise[前提条件]
    Premise --> Step1[推导步骤1]
    Step1 --> Step2[推导步骤2]
    Step2 --> Conclusion[结论]
    Conclusion --> End([结束])
```
""")
        
        # 如果有关系建立，建议对比矩阵
        if sections.get('relations', {}).get('found'):
            suggestions.append("""
### 建议 3: 模型对比矩阵
使用表格形式对比不同模型：

```markdown
| 特性 | 模型A | 模型B | 模型C |
|------|-------|-------|-------|
| 特性1 | ✓ | ✓ | ✗ |
| 特性2 | ✗ | ✓ | ✓ |
```
""")
        
        return suggestions
    
    def analyze(self, filepath: str) -> DocumentSummary:
        """分析文档并生成摘要"""
        self.logger.info(f"Analyzing: {filepath}")
        
        content = self.read_document(filepath)
        if not content:
            raise ValueError(f"Could not read document: {filepath}")
        
        # 提取各元素
        title = self.extract_title(content)
        formal_level = self.extract_formal_level(content)
        sections = self.extract_sections(content)
        definitions = self.extract_definitions(content)
        theorems = self.extract_theorems(content)
        lemmas = self.extract_lemmas(content)
        mermaid_blocks = self.extract_mermaid_blocks(content)
        references = self.extract_references(content)
        key_terms = self.extract_key_terms(content)
        
        # 合并定理和引理
        all_theorems = theorems + lemmas
        
        # 生成内容摘要
        content_summary = self.generate_content_summary(content, sections)
        
        # 生成建议
        suggestions = self.generate_suggestions(
            sections, definitions, all_theorems, mermaid_blocks
        )
        
        # 生成 Mermaid 建议
        mermaid_suggestions = self.suggest_mermaid_diagrams(content, sections)
        
        return DocumentSummary(
            title=title,
            filepath=filepath,
            formal_level=formal_level,
            timestamp=datetime.now().isoformat(),
            content_summary=content_summary,
            sections_status=sections,
            definitions=definitions,
            theorems=all_theorems,
            key_terms=key_terms,
            mermaid_blocks=mermaid_blocks,
            references=references,
            suggestions=suggestions,
            mermaid_suggestions=mermaid_suggestions
        )
    
    def generate_markdown_summary(self, summary: DocumentSummary) -> str:
        """生成 Markdown 格式摘要"""
        templates = self.config.get('summarizer', {}).get('templates', {})
        
        # 生成章节表格
        section_rows = []
        for section_id, info in summary.sections_status.items():
            status = "✅" if info['found'] else "❌"
            section_rows.append(
                f"| {info['name']} | {status} | {info['content_length']} 字符 |"
            )
        section_table = '\n'.join(section_rows)
        
        # 格式化定义列表
        def_list = '\n'.join([
            f"- **{d['id']}**: {d['text']}"
            for d in summary.definitions
        ]) if summary.definitions else "无"
        
        # 格式化定理列表
        thm_list = '\n'.join([
            f"- **{t['id']}**: {t['text']}"
            for t in summary.theorems
        ]) if summary.theorems else "无"
        
        # 格式化建议
        suggestions_text = '\n'.join([
            f"- {s}" for s in summary.suggestions
        ])
        
        # 格式化 Mermaid 建议
        mermaid_text = '\n'.join(summary.mermaid_suggestions)
        
        # 组装摘要
        output = f"""# 文档摘要: {summary.title}

> 生成时间: {summary.timestamp}
> 原文档: `{summary.filepath}`
> 形式化等级: {summary.formal_level}

---

## 内容概要

{summary.content_summary}

---

## 结构分析

| 章节 | 状态 | 内容量 |
|------|------|--------|
{section_table}

---

## 关键元素

### 定义 ({len(summary.definitions)})

{def_list}

### 定理/引理 ({len(summary.theorems)})

{thm_list}

### 关键词

{', '.join([f'`{t}`' for t in summary.key_terms])}

---

## 改进建议

{suggestions_text}

---

## 建议的可视化

{mermaid_text if mermaid_text else "已存在 Mermaid 图，无需额外建议。"}

---

## 引用统计

共发现 {len(summary.references)} 个引用。

"""
        
        return output
    
    def save_summary(self, summary: DocumentSummary, output_dir: str = None):
        """保存摘要到文件"""
        if output_dir is None:
            output_dir = self.config.get('output', {}).get('save_directory', 
                        '.scripts/ai-assistant/output')
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成文件名
        base_name = Path(summary.filepath).stem
        output_path = os.path.join(output_dir, f"{base_name}.summary.md")
        
        # 生成并保存 Markdown
        markdown = self.generate_markdown_summary(summary)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        self.logger.info(f"Summary saved to: {output_path}")
        
        # 同时保存 JSON
        json_path = os.path.join(output_dir, f"{base_name}.summary.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(summary), f, ensure_ascii=False, indent=2)
        
        return output_path


def main():
    parser = argparse.ArgumentParser(
        description='文档摘要生成器 - AnalysisDataFlow AI Assistant'
    )
    parser.add_argument(
        'input',
        help='输入文件或目录路径'
    )
    parser.add_argument(
        '-o', '--output',
        help='输出目录',
        default=None
    )
    parser.add_argument(
        '-c', '--config',
        help='配置文件路径',
        default=None
    )
    parser.add_argument(
        '--stdout',
        action='store_true',
        help='输出到标准输出'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='批量处理目录中的所有 .md 文件'
    )
    
    args = parser.parse_args()
    
    analyzer = DocumentAnalyzer(args.config)
    
    if args.batch or os.path.isdir(args.input):
        # 批量处理
        target_dir = args.input if os.path.isdir(args.input) else os.path.dirname(args.input)
        md_files = list(Path(target_dir).glob('**/*.md'))
        
        print(f"Found {len(md_files)} markdown files to process")
        
        for md_file in md_files:
            try:
                summary = analyzer.analyze(str(md_file))
                if args.stdout:
                    print(analyzer.generate_markdown_summary(summary))
                else:
                    analyzer.save_summary(summary, args.output)
            except Exception as e:
                print(f"Error processing {md_file}: {e}")
    else:
        # 单个文件处理
        summary = analyzer.analyze(args.input)
        if args.stdout:
            print(analyzer.generate_markdown_summary(summary))
        else:
            analyzer.save_summary(summary, args.output)


if __name__ == '__main__':
    main()
