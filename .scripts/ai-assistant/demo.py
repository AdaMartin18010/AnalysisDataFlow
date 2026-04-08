#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 辅助工具演示脚本
演示 AnalysisDataFlow AI Assistant 的核心功能
"""

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))


def import_from_file(module_name, file_path):
    """从文件动态导入模块"""
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def demo_summarizer():
    """演示文档摘要生成"""
    print("=" * 60)
    print("演示 1: 文档摘要生成器")
    print("=" * 60)
    
    # 导入并运行
    doc_summarizer = import_from_file('doc_summarizer', 
                                       os.path.join(script_dir, 'doc-summarizer.py'))
    analyzer = doc_summarizer.DocumentAnalyzer()
    
    # 使用 README.md 作为示例
    readme_path = os.path.join(
        os.path.dirname(os.path.dirname(script_dir)),
        'README.md'
    )
    
    if os.path.exists(readme_path):
        summary = analyzer.analyze(readme_path)
        print(f"\n📄 文档: {summary.title}")
        print(f"📊 关键词: {', '.join(summary.key_terms[:5])}")
        print(f"📐 形式化等级: {summary.formal_level}")
        print(f"\n💡 改进建议:")
        for sug in summary.suggestions[:3]:
            print(f"   - {sug}")
    else:
        print(f"示例文件不存在: {readme_path}")
    
    print()


def demo_translator():
    """演示自动翻译"""
    print("=" * 60)
    print("演示 2: 自动翻译助手")
    print("=" * 60)
    
    auto_translator = import_from_file('auto_translator',
                                        os.path.join(script_dir, 'auto-translator.py'))
    translator = auto_translator.AutoTranslator()
    
    sample_text = """
## 1. 概念定义

**Def-S-01-01** (流计算): 流计算是一种处理无边界数据流的计算模型。

## 2. 属性推导

流计算具有以下关键属性：
- 低延迟处理
- 高吞吐量
- 容错机制
"""
    
    print("\n📝 原文 (中文):")
    print(sample_text[:200] + "...")
    
    translated = translator.translate_document(sample_text, 'zh', 'en')
    
    print("\n🌐 译文 (英文):")
    print(translated[:200] + "...")
    print()


def demo_cross_ref():
    """演示交叉引用建议"""
    print("=" * 60)
    print("演示 3: 交叉引用建议器")
    print("=" * 60)
    
    cross_ref = import_from_file('cross_ref_suggester',
                                  os.path.join(script_dir, 'cross-ref-suggester.py'))
    suggester = cross_ref.CrossRefSuggester()
    
    # 模拟两个文档
    doc1_content = """
# Dataflow 模型

Dataflow 模型是一种流计算范式。
**Def-F-01-01**: Dataflow 定义...
关键词: 流计算、窗口、Watermark
"""
    
    doc2_content = """
# Flink DataStream

Flink 实现了 Dataflow 模型。
**Def-F-01-01**: Dataflow 定义...
关键词: 流计算、Checkpoint、Dataflow
"""
    
    # 创建临时文档
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        doc1_path = os.path.join(tmpdir, 'doc1.md')
        doc2_path = os.path.join(tmpdir, 'doc2.md')
        
        with open(doc1_path, 'w', encoding='utf-8') as f:
            f.write(doc1_content)
        with open(doc2_path, 'w', encoding='utf-8') as f:
            f.write(doc2_content)
        
        suggester.build_index(tmpdir)
        suggester.analyze_all()
        
        print(f"\n📚 索引文档数: {len(suggester.documents)}")
        print(f"🔗 建议链接数: {len(suggester.suggestions)}")
        
        if suggester.suggestions:
            print("\n📋 链接建议示例:")
            for sug in suggester.suggestions[:2]:
                print(f"   {os.path.basename(sug.source)} -> {os.path.basename(sug.target)}")
                print(f"   相似度: {sug.score:.2f}, 理由: {sug.reason}")
    
    print()


def main():
    """主函数"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "AnalysisDataFlow AI Assistant 演示" + " " * 14 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    try:
        demo_summarizer()
    except Exception as e:
        print(f"摘要演示出错: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        demo_translator()
    except Exception as e:
        print(f"翻译演示出错: {e}")
    
    try:
        demo_cross_ref()
    except Exception as e:
        print(f"交叉引用演示出错: {e}")
    
    print("=" * 60)
    print("演示完成!")
    print("=" * 60)
    print("\n更多用法请查看 README.md")


if __name__ == '__main__':
    main()
