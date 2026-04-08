#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动翻译助手 - Auto Translator for AnalysisDataFlow
基于规则的中英互译工具，无需API Key

功能:
- Markdown 文档翻译
- 保留代码块和公式
- 术语对照表支持
- 批量处理
"""

import os
import re
import sys
import yaml
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TranslationBlock:
    """翻译块数据结构"""
    content: str
    block_type: str  # 'text', 'code', 'math', 'special'
    translate: bool  # 是否需要翻译


class AutoTranslator:
    """自动翻译器"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.terminology = self._build_terminology()
        self.preserve_patterns = self._compile_preserve_patterns()
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
    
    def _build_terminology(self) -> Dict[str, str]:
        """构建术语对照表"""
        terminology = {}
        terms = self.config.get('translator', {}).get('terminology', [])
        for term in terms:
            zh = term.get('zh', '')
            en = term.get('en', '')
            if zh and en:
                terminology[zh] = en
                terminology[en] = zh
        return terminology
    
    def _compile_preserve_patterns(self) -> List[re.Pattern]:
        """编译保留模式（不翻译）"""
        patterns = []
        raw_patterns = self.config.get('translator', {}).get('preserve_patterns', [])
        for pattern in raw_patterns:
            try:
                patterns.append(re.compile(pattern, re.MULTILINE))
            except re.error:
                pass
        return patterns
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger('auto-translator')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def detect_language(self, text: str) -> str:
        """检测文本语言 (zh/en)"""
        # 简单启发式：检查中文字符比例
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        total_chars = len(text)
        
        if total_chars == 0:
            return 'unknown'
        
        ratio = chinese_chars / total_chars
        return 'zh' if ratio > 0.1 else 'en'
    
    def split_into_blocks(self, content: str) -> List[TranslationBlock]:
        """将内容分割为翻译块"""
        blocks = []
        
        # 定义块分隔模式
        patterns = [
            # 代码块
            (r'```[\s\S]*?```', 'code'),
            # 行内代码
            (r'`[^`]+`', 'code'),
            # 公式块
            (r'\$\$[\s\S]*?\$\$', 'math'),
            # 行内公式
            (r'\$[^$\n]+\$', 'math'),
            # HTML 标签
            (r'<[^>]+>', 'special'),
            # 链接
            (r'\[([^\]]+)\]\(([^)]+)\)', 'special'),
            # 图片
            (r'!\[([^\]]*)\]\(([^)]+)\)', 'special'),
            # 定理/定义编号
            (r'\*\*(?:Thm|Def|Lemma|Prop|Cor)-[SKF]-\d{2}-\d{2}\*\*', 'special'),
        ]
        
        # 使用占位符保护特殊块
        placeholders = {}
        placeholder_id = 0
        protected_content = content
        
        for pattern, block_type in patterns:
            def replace_with_placeholder(match):
                nonlocal placeholder_id
                key = f"__PLACEHOLDER_{placeholder_id:04d}__"
                placeholders[key] = TranslationBlock(
                    content=match.group(0),
                    block_type=block_type,
                    translate=False
                )
                placeholder_id += 1
                return key
            
            protected_content = re.sub(pattern, replace_with_placeholder, protected_content)
        
        # 分割文本块
        parts = re.split(r'(__PLACEHOLDER_\d{4}__)', protected_content)
        
        for part in parts:
            if part in placeholders:
                blocks.append(placeholders[part])
            elif part.strip():
                blocks.append(TranslationBlock(
                    content=part,
                    block_type='text',
                    translate=True
                ))
        
        return blocks
    
    def translate_text(self, text: str, source: str = 'zh', target: str = 'en') -> str:
        """翻译文本（基于规则）"""
        if source == target:
            return text
        
        result = text
        
        # 术语替换
        for src_term, tgt_term in self.terminology.items():
            if source == 'zh' and target == 'en':
                # 中文 -> 英文
                if src_term in result:
                    result = result.replace(src_term, tgt_term)
            else:
                # 英文 -> 中文
                if src_term in result:
                    result = result.replace(src_term, tgt_term)
        
        # 基于模式的翻译规则
        if source == 'zh' and target == 'en':
            result = self._apply_zh_to_en_rules(result)
        else:
            result = self._apply_en_to_zh_rules(result)
        
        return result
    
    def _apply_zh_to_en_rules(self, text: str) -> str:
        """应用中文到英文的翻译规则"""
        # 常见句式映射
        rules = [
            # 标题翻译
            (r'^#\s*概念定义', '# Concept Definitions'),
            (r'^#\s*属性推导', '# Property Derivation'),
            (r'^#\s*关系建立', '# Relationship Building'),
            (r'^#\s*论证过程', '# Argumentation Process'),
            (r'^#\s*形式证明', '# Formal Proof'),
            (r'^#\s*实例验证', '# Example Verification'),
            (r'^#\s*可视化', '# Visualizations'),
            (r'^#\s*引用参考', '# References'),
            
            # 常用词汇
            (r'定义\s*[:：]', 'Definition:'),
            (r'定理\s*[:：]', 'Theorem:'),
            (r'引理\s*[:：]', 'Lemma:'),
            (r'命题\s*[:：]', 'Proposition:'),
            (r'推论\s*[:：]', 'Corollary:'),
            (r'证明\s*[:：]', 'Proof:'),
            (r'示例\s*[:：]', 'Example:'),
            (r'注意\s*[:：]', 'Note:'),
            (r'警告\s*[:：]', 'Warning:'),
            
            # 常用短语
            (r'如\s*图\s*所\s*示', 'as shown in the figure'),
            (r'如\s*下\s*所\s*示', 'as shown below'),
            (r'以\s*下\s*是', 'the following is'),
            (r'我\s*们\s*定\s*义', 'we define'),
            (r'设\s*定', 'let'),
            (r'则\s*有', 'then'),
            (r'因\s*此', 'therefore'),
            (r'所\s*以', 'so'),
            (r'因\s*为', 'because'),
            (r'如\s*果', 'if'),
            (r'那\s*么', 'then'),
            (r'当\s*且\s*仅\s*当', 'if and only if'),
            
            # 文档头部信息
            (r'所\s*属\s*阶\s*段', 'Stage'),
            (r'前\s*置\s*依\s*赖', 'Prerequisites'),
            (r'形\s*式\s*化\s*等\s*级', 'Formalization Level'),
        ]
        
        for pattern, replacement in rules:
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE | re.UNICODE)
        
        return text
    
    def _apply_en_to_zh_rules(self, text: str) -> str:
        """应用英文到中文的翻译规则"""
        rules = [
            # 标题翻译
            (r'^#\s*Concept Definitions', '# 概念定义'),
            (r'^#\s*Property Derivation', '# 属性推导'),
            (r'^#\s*Relationship Building', '# 关系建立'),
            (r'^#\s*Argumentation Process', '# 论证过程'),
            (r'^#\s*Formal Proof', '# 形式证明'),
            (r'^#\s*Example Verification', '# 实例验证'),
            (r'^#\s*Visualizations', '# 可视化'),
            (r'^#\s*References', '# 引用参考'),
            
            # 常用词汇
            (r'\bDefinition:\s*', '定义：'),
            (r'\bTheorem:\s*', '定理：'),
            (r'\bLemma:\s*', '引理：'),
            (r'\bProposition:\s*', '命题：'),
            (r'\bCorollary:\s*', '推论：'),
            (r'\bProof:\s*', '证明：'),
            (r'\bExample:\s*', '示例：'),
            (r'\bNote:\s*', '注意：'),
            (r'\bWarning:\s*', '警告：'),
            
            # 常用短语
            (r'\bas shown in the figure\b', '如图所示'),
            (r'\bas shown below\b', '如下所示'),
            (r'\bthe following is\b', '以下是'),
            (r'\bwe define\b', '我们定义'),
            (r'\blet\b', '设'),
            (r'\bthen\b', '则有'),
            (r'\btherefore\b', '因此'),
            (r'\bso\b', '所以'),
            (r'\bbecause\b', '因为'),
            (r'\bif\b', '如果'),
            (r'\bif and only if\b', '当且仅当'),
            
            # 文档头部信息
            (r'\bStage\b', '所属阶段'),
            (r'\bPrerequisites\b', '前置依赖'),
            (r'\bFormalization Level\b', '形式化等级'),
        ]
        
        for pattern, replacement in rules:
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE | re.IGNORECASE)
        
        return text
    
    def translate_document(self, content: str, source: str = None, target: str = 'en') -> str:
        """翻译整个文档"""
        # 自动检测源语言
        if source is None:
            source = self.detect_language(content)
        
        if source == target:
            return content
        
        self.logger.info(f"Translating from {source} to {target}")
        
        # 分割为块
        blocks = self.split_into_blocks(content)
        
        # 翻译各块
        translated_blocks = []
        for block in blocks:
            if block.translate:
                translated = self.translate_text(block.content, source, target)
                translated_blocks.append(translated)
            else:
                translated_blocks.append(block.content)
        
        return ''.join(translated_blocks)
    
    def translate_file(self, input_path: str, output_path: str = None,
                      source: str = None, target: str = 'en') -> str:
        """翻译文件"""
        # 读取输入文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 翻译
        translated = self.translate_document(content, source, target)
        
        # 确定输出路径
        if output_path is None:
            input_path_obj = Path(input_path)
            suffix = '-en' if target == 'en' else '-zh'
            output_path = input_path_obj.parent / f"{input_path_obj.stem}{suffix}{input_path_obj.suffix}"
        
        # 保存
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated)
        
        self.logger.info(f"Translated saved to: {output_path}")
        return str(output_path)
    
    def batch_translate(self, directory: str, pattern: str = '*.md',
                       source: str = None, target: str = 'en') -> List[str]:
        """批量翻译"""
        translated_files = []
        
        for file_path in Path(directory).rglob(pattern):
            try:
                output_path = self.translate_file(str(file_path), source=source, target=target)
                translated_files.append(output_path)
            except Exception as e:
                self.logger.error(f"Error translating {file_path}: {e}")
        
        return translated_files


def main():
    parser = argparse.ArgumentParser(
        description='自动翻译助手 - AnalysisDataFlow AI Assistant'
    )
    parser.add_argument(
        'input',
        help='输入文件或目录路径'
    )
    parser.add_argument(
        '-o', '--output',
        help='输出文件路径'
    )
    parser.add_argument(
        '-s', '--source',
        help='源语言 (zh/en/auto)',
        default='auto'
    )
    parser.add_argument(
        '-t', '--target',
        help='目标语言 (zh/en)',
        default='en'
    )
    parser.add_argument(
        '-c', '--config',
        help='配置文件路径'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='批量处理目录'
    )
    parser.add_argument(
        '--pattern',
        help='文件匹配模式 (批量处理时)',
        default='*.md'
    )
    parser.add_argument(
        '--stdout',
        action='store_true',
        help='输出到标准输出'
    )
    
    args = parser.parse_args()
    
    translator = AutoTranslator(args.config)
    
    source = None if args.source == 'auto' else args.source
    
    if args.batch or os.path.isdir(args.input):
        translated = translator.batch_translate(
            args.input, args.pattern, source, args.target
        )
        print(f"Translated {len(translated)} files:")
        for f in translated:
            print(f"  - {f}")
    else:
        if args.stdout:
            with open(args.input, 'r', encoding='utf-8') as f:
                content = f.read()
            translated = translator.translate_document(content, source, args.target)
            print(translated)
        else:
            translator.translate_file(args.input, args.output, source, args.target)


if __name__ == '__main__':
    main()
