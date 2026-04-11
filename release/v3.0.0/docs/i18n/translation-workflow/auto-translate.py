#!/usr/bin/env python3
"""
AI辅助翻译工具 - 智能预翻译与术语替换

功能:
1. AI预翻译中文文档
2. 术语自动替换
3. 保持Markdown格式
4. 人工审校集成

作者: AnalysisDataFlow i18n Team
版本: 4.0-prep

使用:
    python auto-translate.py <source_file> [--model gpt-4o] [--review]
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class TranslationTask:
    """翻译任务"""
    source_file: str
    target_file: str
    priority: str
    word_count: int
    status: str = "pending"


class AutoTranslator:
    """AI辅助翻译器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.terminology: Dict = {}
        self.prohibited_terms: List[str] = []
        self.load_terminology()
    
    def load_terminology(self) -> None:
        """加载术语库"""
        # 加载核心术语
        core_terms_path = self.project_root / "i18n/terminology/core-terms.json"
        if core_terms_path.exists():
            with open(core_terms_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for term in data.get("terms", []):
                    self.terminology[term["term"]] = term
        
        # 加载Flink术语
        flink_terms_path = self.project_root / "i18n/terminology/flink-terms.json"
        if flink_terms_path.exists():
            with open(flink_terms_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for term in data.get("terms", []):
                    self.terminology[term["term"]] = term
        
        # 加载禁止翻译列表
        rules_path = self.project_root / "i18n/terminology/verification-rules.json"
        if rules_path.exists():
            with open(rules_path, 'r', encoding='utf-8') as f:
                rules = json.load(f)
                prohibited = rules.get("prohibited_translation", {}).get("categories", {})
                for category, config in prohibited.items():
                    if "terms" in config:
                        self.prohibited_terms.extend(config["terms"])
    
    def create_translation_prompt(self, content: str, file_path: str) -> str:
        """创建翻译提示词"""
        
        # 提取文件相关的关键术语
        relevant_terms = []
        for term_id, term_info in self.terminology.items():
            if term_info["term"] in content:
                relevant_terms.append({
                    "cn": term_info["term"],
                    "en": term_info["en"],
                    "definition": term_info.get("definition_en", "")
                })
        
        # 构建术语提示
        term_prompt = "\n".join([
            f"- {t['cn']} → {t['en']}: {t['definition']}"
            for t in relevant_terms[:20]  # 限制术语数量
        ])
        
        # 禁止翻译列表提示
        prohibited_prompt = "\n".join([f"- {t}" for t in self.prohibited_terms[:15]])
        
        prompt = f"""You are a professional technical translator specializing in stream processing, distributed systems, and formal methods. Translate the following Chinese technical document into English.

## Translation Guidelines

### Terminology Standards (CRITICAL - Must Follow)
The following terms must be translated EXACTLY as specified:
{term_prompt}

### Terms That MUST NOT Be Translated
Keep the following terms in their original form:
{prohibited_prompt}
- All class names (e.g., DataStream, ProcessFunction)
- All API method names (e.g., map, flatMap, keyBy)
- All configuration keys (e.g., execution.checkpointing.interval)
- All product names (e.g., Apache Flink, Apache Kafka)

### Style Guidelines
1. Use clear, professional technical English
2. Maintain the original Markdown formatting exactly
3. Preserve all code blocks, Mermaid diagrams, and mathematical formulas
4. Use present tense for technical descriptions
5. Keep sentences concise (under 25 words when possible)
6. Use active voice where appropriate
7. Ensure abbreviations are expanded on first use

### Document Structure
The document follows a standard 8-section structure:
1. Concept Definitions
2. Property Derivation
3. Relationship Establishment
4. Argumentation Process
5. Formal Proof / Engineering Argument
6. Example Verification
7. Visualizations
8. References

Maintain this structure in the translation.

### Source Document
File: {file_path}

---

{content}

---

Please provide the complete English translation, maintaining all formatting and structure."""
        
        return prompt
    
    def apply_term_replacements(self, content: str) -> str:
        """应用术语替换（后处理）"""
        
        # 创建术语替换映射
        replacements = {}
        for term_id, term_info in self.terminology.items():
            cn_term = term_info["term"]
            en_term = term_info["en"]
            
            # 简单的术语替换（实际应更智能，考虑上下文）
            replacements[cn_term] = en_term
        
        # 按术语长度降序排序，避免部分替换问题
        sorted_terms = sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True)
        
        # 在代码块和公式外进行替换
        result = []
        in_code_block = False
        in_math = False
        
        for line in content.split('\n'):
            # 检测代码块
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
            
            # 检测行内数学公式
            if not in_code_block:
                # 简单检测，实际应更精确
                pass
            
            # 在非代码区域进行替换
            if not in_code_block:
                for cn_term, en_term in sorted_terms:
                    # 使用单词边界避免部分匹配
                    pattern = r'(?<![\w])' + re.escape(cn_term) + r'(?![\w])'
                    line = re.sub(pattern, en_term, line)
            
            result.append(line)
        
        return '\n'.join(result)
    
    def generate_frontmatter(self, source_file: str, translator: str = "AI") -> str:
        """生成翻译文档的frontmatter"""
        
        frontmatter = f"""---
title: "[EN] {Path(source_file).stem.replace('-', ' ').title()}"
translation_status: "ai_translated"
source_file: "{source_file}"
source_version: "{self.compute_file_hash(source_file)[:8]}"
translator: "{translator}"
reviewer: null
translated_at: "{datetime.now().isoformat()}"
reviewed_at: null
quality_score: null
terminology_verified: false
---

"""
        return frontmatter
    
    def compute_file_hash(self, file_path: str) -> str:
        """计算文件哈希"""
        import hashlib
        
        full_path = self.project_root / file_path
        if not full_path.exists():
            return ""
        
        sha256 = hashlib.sha256()
        with open(full_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def translate_file(self, source_file: str, model: str = "gpt-4o", 
                       review: bool = False) -> Tuple[bool, str]:
        """
        翻译单个文件
        
        Args:
            source_file: 源文件路径
            model: AI模型名称
            review: 是否需要人工审校
            
        Returns:
            (success, message)
        """
        source_path = self.project_root / source_file
        
        if not source_path.exists():
            return False, f"源文件不存在: {source_file}"
        
        # 读取源文件
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 确定目标路径
        if source_file.startswith(("Struct/", "Knowledge/", "Flink/")):
            target_file = f"i18n/en/{source_file}"
        else:
            target_file = f"i18n/en/{Path(source_file).name}"
        
        target_path = self.project_root / target_file
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 生成翻译提示词
        prompt = self.create_translation_prompt(content, source_file)
        
        # 保存提示词到临时文件（供人工使用）
        prompt_file = self.project_root / "i18n/translation-workflow/temp" / f"{Path(source_file).stem}-prompt.txt"
        prompt_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"📝 翻译提示词已保存: {prompt_file}")
        
        # 这里可以集成实际的AI API调用
        # 目前生成模板供人工使用
        
        # 生成AI翻译模板
        translated_content = self.generate_ai_translation_template(content, source_file)
        
        # 写入目标文件
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        if review:
            print(f"⏳ 文件已标记为待审校: {target_file}")
        else:
            print(f"✅ 翻译完成: {target_file}")
        
        return True, target_file
    
    def generate_ai_translation_template(self, content: str, source_file: str) -> str:
        """生成AI翻译模板（实际使用时替换为真实AI调用）"""
        
        # 生成frontmatter
        frontmatter = self.generate_frontmatter(source_file)
        
        # 标记需要翻译的部分
        lines = content.split('\n')
        translated_lines = []
        
        in_code_block = False
        in_frontmatter = False
        
        for line in lines:
            # 跳过原始frontmatter
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    in_frontmatter = False
                    continue
            
            if in_frontmatter:
                continue
            
            # 保留代码块
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                translated_lines.append(line)
                continue
            
            if in_code_block:
                translated_lines.append(line)
                continue
            
            # 保留Mermaid图表
            if line.strip().startswith('```mermaid'):
                translated_lines.append(line)
                continue
            
            # 保留数学公式
            if line.strip().startswith('$$') or '$' in line:
                translated_lines.append(line)
                continue
            
            # 保留Markdown标记行
            if line.strip().startswith(('#', '|', '- ', '* ', '1. ', '> ', '[', '![')):
                # 这些行需要翻译但保留格式
                translated_lines.append(f"<!-- TRANSLATE: {line} -->")
                continue
            
            # 普通文本行
            if line.strip():
                translated_lines.append(f"<!-- TRANSLATE: {line} -->")
            else:
                translated_lines.append(line)
        
        translated_content = '\n'.join(translated_lines)
        
        # 组合最终内容
        result = frontmatter + "\n<!-- AI Translation Template - Replace <!-- TRANSLATE --> markers with actual translation -->\n\n" + translated_content
        
        return result
    
    def batch_translate(self, queue_file: str, model: str = "gpt-4o") -> None:
        """批量翻译队列中的文件"""
        
        queue_path = self.project_root / queue_file
        if not queue_path.exists():
            print(f"❌ 队列文件不存在: {queue_file}")
            return
        
        with open(queue_path, 'r', encoding='utf-8') as f:
            queue = json.load(f)
        
        tasks = queue.get("tasks", [])
        
        # 按优先级过滤
        priority_filter = ["P0", "P1"]  # 仅翻译P0和P1
        tasks_to_translate = [t for t in tasks if t["priority"] in priority_filter]
        
        print(f"📋 批量翻译任务: {len(tasks_to_translate)} 个文件 (P0/P1)")
        
        success_count = 0
        fail_count = 0
        
        for task in tasks_to_translate:
            print(f"\n🔄 翻译: {task['source_file']}")
            success, message = self.translate_file(task["source_file"], model, review=True)
            
            if success:
                success_count += 1
                task["status"] = "ai_translated"
                task["target_file"] = message
            else:
                fail_count += 1
                task["status"] = "failed"
                task["error"] = message
        
        # 更新队列
        with open(queue_path, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 批量翻译完成: {success_count} 成功, {fail_count} 失败")


def main():
    """主入口"""
    parser = argparse.ArgumentParser(description='AI辅助翻译工具')
    parser.add_argument('source', help='源文件路径或队列文件')
    parser.add_argument('--batch', action='store_true', help='批量模式')
    parser.add_argument('--model', default='gpt-4o', help='AI模型')
    parser.add_argument('--review', action='store_true', help='标记为待审校')
    parser.add_argument('--root', default='.', help='项目根目录')
    
    args = parser.parse_args()
    
    translator = AutoTranslator(args.root)
    
    if args.batch:
        translator.batch_translate(args.source, args.model)
    else:
        success, message = translator.translate_file(args.source, args.model, args.review)
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            sys.exit(1)


if __name__ == "__main__":
    main()
