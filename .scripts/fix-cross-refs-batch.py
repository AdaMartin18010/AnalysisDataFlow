#!/usr/bin/env python3
"""
批量修复交叉引用错误
"""

import re
import os
import json
from pathlib import Path
from collections import defaultdict

# 定义路径映射 (旧路径 -> 新路径)
PATH_MAPPINGS = {
    # Struct 目录
    "Struct/00-INDEX.md": "../Struct/00-INDEX.md",
    "Struct/01-foundation/01.01-process-calculus-fundamentals.md": "../01-foundation/01.01-process-calculus-fundamentals.md",
    "Struct/01-foundation/01.02-csp-formalization.md": "../01-foundation/01.02-csp-formalization.md",
    "Struct/01-foundation/01.03-actor-model-formalization.md": "../01-foundation/01.03-actor-model-formalization.md",
    "Struct/01-foundation/01.04-dataflow-model-formalization.md": "../01-foundation/01.04-dataflow-model-formalization.md",
    "Struct/02-properties/02.01-determinism-analysis.md": "../02-properties/02.01-determinism-analysis.md",
    "Struct/02-properties/02.02-consistency-hierarchy.md": "../02-properties/02.02-consistency-hierarchy.md",
    "Struct/03-relationships/03.01-flink-to-actor-encoding.md": "../03-relationships/03.01-flink-to-actor-encoding.md",
    
    # Flink 核心目录 - 旧路径映射
    "Flink/02-core-mechanisms/time-semantics-and-watermark.md": "Flink/02-core/time-semantics-and-watermark.md",
    "Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md": "Flink/02-core/checkpoint-mechanism-deep-dive.md",
    
    # Flink API
    "Flink/03-api-patterns/flink-cep-deep-dive.md": "Flink/03-api/03.02-table-sql-api/flink-cep-complete-guide.md",
    "Flink/03-sql-table-api/flink-table-sql-complete-guide.md": "Flink/03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md",
    "Flink/03-internals/flink-sql-overview.md": "Flink/03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md",
    
    # Flink 案例
    "Flink/07-case-studies/case-financial-realtime-risk-control.md": "Flink/09-practices/09.01-case-studies/case-financial-realtime-risk-control.md",
    "Flink/07-case-studies/case-iot-stream-processing.md": "Flink/09-practices/09.01-case-studies/case-iot-stream-processing.md",
    "Flink/07-case-studies/case-realtime-analytics.md": "Flink/09-practices/09.01-case-studies/case-realtime-analytics.md",
    
    # Flink 工程
    "Flink/06-engineering/state-backend-selection.md": "Flink/09-practices/09.03-performance-tuning/state-backend-selection.md",
    
    # Flink 对比
    "Flink/05-vs-competitors/flink-vs-spark-streaming.md": "Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-kafka-streams.md",
    "Flink/05-vs-competitors/flink-vs-kafka-streams.md": "Flink/09-practices/09.03-performance-tuning/05-vs-competitors/flink-vs-kafka-streams.md",
    
    # Flink 其他
    "Flink/04-ai-integration/flink-ml-integration.md": "Flink/06-ai-ml/flink-ai-agents-flip-531.md",
    "Flink/04-state-checkpoint/exactly-once-semantics.md": "Flink/02-core/exactly-once-end-to-end.md",
    "Flink/03-flink-state-management.md": "Flink/02-core/flink-state-management-complete-guide.md",
    
    # 根目录文件
    "GLOSSARY-EN.md": "GLOSSARY.md",
    "LEARNING-PATHS-DYNAMIC.md": "LEARNING-PATHS/00-INDEX.md",
    ".scripts/learning-path-recommender.py": "learning-path-recommender.js",
}

# 相对路径修正 (从源目录到目标的正确相对路径)
RELATIVE_PATH_FIXES = {
    # Knowledge -> Flink
    ("Knowledge", "Flink/02-core/"): "../../Flink/02-core/",
    ("Knowledge", "Flink/01-concepts/"): "../../Flink/01-concepts/",
    ("Knowledge", "Flink/03-api/"): "../../Flink/03-api/",
    ("Knowledge", "Flink/04-runtime/"): "../../Flink/04-runtime/",
    ("Knowledge", "Flink/05-ecosystem/"): "../../Flink/05-ecosystem/",
    ("Knowledge", "Flink/06-ai-ml/"): "../../Flink/06-ai-ml/",
    ("Knowledge", "Flink/07-rust-native/"): "../../Flink/07-rust-native/",
    ("Knowledge", "Flink/08-roadmap/"): "../../Flink/08-roadmap/",
    ("Knowledge", "Flink/09-practices/"): "../../Flink/09-practices/",
    ("Knowledge", "Struct/"): "../Struct/",
    ("Knowledge", "GLOSSARY"): "../GLOSSARY.md",
    
    # Knowledge/XX-YYYY -> Flink
    ("Knowledge/02-design-patterns", "Flink/02-core/"): "../../Flink/02-core/",
    ("Knowledge/02-design-patterns", "Flink/03-api/"): "../../Flink/03-api/",
    ("Knowledge/02-design-patterns", "Flink/09-practices/"): "../../Flink/09-practices/",
    ("Knowledge/03-business-patterns", "Flink/02-core/"): "../../Flink/02-core/",
    ("Knowledge/03-business-patterns", "Flink/09-practices/"): "../../Flink/09-practices/",
    ("Knowledge/04-technology-selection", "Flink/02-core/"): "../../Flink/02-core/",
    ("Knowledge/06-frontier", "Flink/02-core/"): "../../Flink/02-core/",
    ("Knowledge/98-exercises", "Flink/02-core/"): "../../Flink/02-core/",
    
    # Struct -> Flink
    ("Struct", "Flink/02-core/"): "../Flink/02-core/",
    ("Struct/07-tools", "Flink/02-core/"): "../../Flink/02-core/",
    
    # Flink -> Flink (内部引用)
    ("Flink/00-meta", "Flink/02-core/"): "../02-core/",
    ("Flink/03-api", "Flink/02-core/"): "../../02-core/",
    ("Flink/04-runtime", "Flink/02-core/"): "../../02-core/",
    ("Flink/flink-pyflink-deep-dive.md", "Flink/02-core/"): "./02-core/",
}

def find_best_match(path, source_dir):
    """根据源文件位置找到正确的相对路径"""
    
    # 直接映射
    if path in PATH_MAPPINGS:
        return PATH_MAPPINGS[path]
    
    # 尝试相对路径修正
    for (src_prefix, dst_prefix), replacement in RELATIVE_PATH_FIXES.items():
        if source_dir.startswith(src_prefix) and path.startswith(dst_prefix):
            return path.replace(dst_prefix, replacement, 1)
    
    return None

def fix_links_in_file(file_path, base_path):
    """修复单个文件中的链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        source_dir = os.path.dirname(file_path).replace("\\", "/")
        fixes = []
        
        # 匹配Markdown链接
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        def replace_link(match):
            text = match.group(1)
            link = match.group(2)
            
            # 跳过外部链接和锚点链接
            if link.startswith("http") or link.startswith("#") or link.startswith("mailto:"):
                return match.group(0)
            
            # 分离路径和锚点
            if "#" in link:
                path_part, anchor = link.split("#", 1)
            else:
                path_part, anchor = link, None
            
            # 尝试找到修正
            new_path = find_best_match(path_part, source_dir)
            
            if new_path and new_path != path_part:
                if anchor:
                    new_link = f"[{text}]({new_path}#{anchor})"
                else:
                    new_link = f"[{text}]({new_path})"
                fixes.append(f"  {path_part} -> {new_path}")
                return new_link
            
            return match.group(0)
        
        new_content = re.sub(link_pattern, replace_link, content)
        
        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return len(fixes), fixes
        
        return 0, []
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0, []

def main():
    import sys
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print("=" * 80)
    print("批量修复交叉引用错误")
    print("=" * 80)
    
    # 加载错误报告
    report_path = os.path.join(base_path, "cross-ref-report.json")
    if not os.path.exists(report_path):
        print(f"错误报告不存在: {report_path}")
        return
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    file_errors = [i for i in report.get('issues', []) if i.get('issue_type') == 'broken_link']
    anchor_errors = [i for i in report.get('issues', []) if i.get('issue_type') == 'broken_anchor']
    
    print(f"\n待修复错误:")
    print(f"  - 文件引用错误: {len(file_errors)}")
    print(f"  - 锚点引用错误: {len(anchor_errors)}")
    
    # 收集需要修复的文件
    files_to_fix = set()
    for err in file_errors:
        files_to_fix.add(err['file_path'])
    for err in anchor_errors:
        files_to_fix.add(err['file_path'])
    
    print(f"\n涉及文件数: {len(files_to_fix)}")
    
    # 修复每个文件
    total_fixes = 0
    fixed_files = []
    
    for file_path in sorted(files_to_fix):
        full_path = os.path.join(base_path, file_path.replace("\\", "/"))
        if os.path.exists(full_path):
            count, fixes = fix_links_in_file(full_path, base_path)
            if count > 0:
                total_fixes += count
                fixed_files.append((file_path, count))
                print(f"\n修复: {file_path} ({count}处)")
                for fix in fixes[:5]:  # 只显示前5个
                    print(fix)
                if len(fixes) > 5:
                    print(f"  ... 还有 {len(fixes) - 5} 处")
    
    print("\n" + "=" * 80)
    print("修复完成统计")
    print("=" * 80)
    print(f"修复文件数: {len(fixed_files)}")
    print(f"修复链接数: {total_fixes}")
    print(f"\n修复文件列表 (Top 20):")
    for fp, cnt in sorted(fixed_files, key=lambda x: -x[1])[:20]:
        print(f"  {fp}: {cnt}处")

if __name__ == "__main__":
    main()
