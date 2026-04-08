#!/usr/bin/env python3
"""
交叉引用最终修复脚本
处理剩余的特定错误
"""

import re
import os

# 特定修复映射
SPECIFIC_FIXES = {
    # 缺失文件映射
    "../GLOSSARY-EN.md": "../GLOSSARY.md",
    "../LEARNING-PATHS-DYNAMIC.md": "../LEARNING-PATHS/00-INDEX.md",
    "../.scripts/learning-path-recommender.py": "../learning-path-recommender.js",
    
    # 拼写错误
    "02-core/checkpoint-mechanisms-deep-dive.md": "../02-core/checkpoint-mechanism-deep-dive.md",
    "checkpoint-mechanisms-deep-dive.md": "./checkpoint-mechanism-deep-dive.md",
    
    # 旧目录映射到新目录
    "../../Flink/02-core-mechanisms/": "../../Flink/02-core/",
    "../../Flink/07-case-studies/": "../../Flink/09-practices/09.01-case-studies/",
    "Flink/02-core-mechanisms": "../../Flink/02-core",
    "Flink/07-case-studies/": "../../Flink/09-practices/09.01-case-studies/",
    
    # 其他旧路径
    "../../00.md": "../../Flink/00-meta/00-INDEX.md",
    "../../../Flink/03-api/09-language-foundations/01.03-typeinformation-derivation.md": "../../../Flink/03-api/09-language-foundations/01.02-typeinformation-derivation.md",
    "../../../Flink/01-architecture/": "../../../Flink/01-concepts/",
    "../flink-architecture-overview.md": "../../Flink/01-concepts/deployment-architectures.md",
    "../wasm-runtime-fundamentals.md": "../../Flink/05-ecosystem/05.03-wasm-udf/wasm-runtime-fundamentals.md",
    "../路径/文件.md": "#",  # 占位符链接
    "../../../Flink/04-runtime/flink-rpc-internals.md": "../../../Flink/04-runtime/04.03-observability/flink-rpc-internals.md",
}

def fix_file(file_path, fixes_map):
    """修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes = []
        
        # 匹配Markdown链接
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        def replace_link(match):
            text = match.group(1)
            link = match.group(2)
            
            # 跳过外部链接
            if link.startswith("http") or link.startswith("#") or link.startswith("mailto:"):
                return match.group(0)
            
            # 分离路径和锚点
            if "#" in link:
                path_part, anchor = link.split("#", 1)
            else:
                path_part, anchor = link, None
            
            # 检查是否需要修复
            if path_part in fixes_map:
                new_path = fixes_map[path_part]
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
        print(f"Error: {file_path}: {e}")
        return 0, []

def main():
    import sys
    import json
    
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print("=" * 80)
    print("交叉引用最终修复")
    print("=" * 80)
    
    # 加载错误报告
    report_path = os.path.join(base_path, "cross-ref-report.json")
    if not os.path.exists(report_path):
        print(f"错误报告不存在")
        return
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    file_errors = report['errors']['file_not_found']
    
    # 收集需要修复的文件
    files_to_fix = set()
    for err in file_errors:
        path = err['path']
        if path in SPECIFIC_FIXES:
            files_to_fix.add(err['source'])
    
    print(f"\n特定修复条目: {len(SPECIFIC_FIXES)}")
    print(f"涉及文件数: {len(files_to_fix)}")
    
    # 修复每个文件
    total_fixes = 0
    fixed_files = []
    
    for file_path in sorted(files_to_fix):
        full_path = os.path.join(base_path, file_path.replace("\\", "/"))
        if os.path.exists(full_path):
            count, fixes = fix_file(full_path, SPECIFIC_FIXES)
            if count > 0:
                total_fixes += count
                fixed_files.append((file_path, count, fixes))
    
    print("\n" + "=" * 80)
    print("修复完成")
    print("=" * 80)
    print(f"修复文件数: {len(fixed_files)}")
    print(f"修复链接数: {total_fixes}")
    
    for fp, cnt, fixes in fixed_files:
        print(f"\n{fp}: {cnt}处")
        for fix in fixes:
            print(f"  {fix}")

if __name__ == "__main__":
    main()
