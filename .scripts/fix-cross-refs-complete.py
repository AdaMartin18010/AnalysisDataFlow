#!/usr/bin/env python3
"""
最终清零修复脚本
"""

import re
import os

# 剩余修复映射
REMAINING_FIXES = {
    # api-evolution 规划文档 -> 现有文档
    "api-evolution/datastream-24.md": "../08-roadmap/08.01-flink-24/flink-2.4-tracking.md",
    "api-evolution/datastream-25.md": "../08-roadmap/08.01-flink-24/flink-2.5-preview.md",
    "api-evolution/datastream-30.md": "../08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md",
    "api-evolution/sql-24.md": "../03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md",
    "api-evolution/sql-25.md": "../08-roadmap/08.01-flink-24/flink-2.5-preview.md",
    "api-evolution/sql-30.md": "../08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md",
    "api-evolution/window-api.md": "../03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md",
    "api-evolution/window-sql.md": "../03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md",
    "api-evolution/state-api.md": "../02-core/flink-state-management-complete-guide.md",
    "api-evolution/async-api.md": "../02-core/async-execution-model.md",
    "api-evolution/cep-evolution.md": "../03-api/03.02-table-sql-api/flink-cep-complete-guide.md",
    "api-evolution/agg-sql.md": "../03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md",
    "api-evolution/join-sql.md": "../02-core/multi-way-join-optimization.md",
    "api-evolution/udf-sql.md": "../03-api/03.02-table-sql-api/flink-python-udf.md",
    "api-evolution/materialized-view.md": "../03-api/03.02-table-sql-api/flink-materialized-table-deep-dive.md",
    
    # 根目录引用 -> 正确相对路径
    "../README-EN.md": "../../README-EN.md",
    "../GLOSSARY.md": "../../GLOSSARY.md",
    "../LEARNING-PATHS/00-INDEX.md": "../../LEARNING-PATHS/00-INDEX.md",
    "../PROJECT-TRACKING.md": "../../PROJECT-TRACKING.md",
    "../SEARCH-GUIDE.md": "../../SEARCH-GUIDE.md",
    "../THEOREM-REGISTRY.md": "../../THEOREM-REGISTRY.md",
    "../COMPLETION-CHECKLIST.md": "../../PROJECT-TRACKING.md",  # 映射到项目追踪
    "../knowledge-graph.html": "../../knowledge-graph.html",
    "../CONTRIBUTING.md": "../../CONTRIBUTING.md",
    
    # 脚本引用
    "../../.scripts/flink-release-tracker.py": "../../.scripts/flink-version-tracking/flink-release-tracker.py",
    
    # 架构文档引用 -> 现有文档
    "../../Flink/01-concepts/deployment-architectures.md": "../../../Flink/01-concepts/deployment-architectures.md",
    "../../Flink/05-ecosystem/05.03-wasm-udf/09-wasm-udf-frameworks.md": "../../../Flink/05-ecosystem/05.03-wasm-udf/09-wasm-udf-frameworks.md",
    
    # 代码片段误报修复
    "name": "#",  # 类型参数V的误报
}

def fix_file(file_path, fixes_map):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes = []
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        def replace_link(match):
            text = match.group(1)
            link = match.group(2)
            
            if link.startswith("http") or link.startswith("#") or link.startswith("mailto:"):
                return match.group(0)
            
            if "#" in link:
                path_part, anchor = link.split("#", 1)
            else:
                path_part, anchor = link, None
            
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
    print("最终清零修复")
    print("=" * 80)
    
    report_path = os.path.join(base_path, "cross-ref-report.json")
    if not os.path.exists(report_path):
        print(f"错误报告不存在")
        return
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    file_errors = report['errors']['file_not_found']
    
    files_to_fix = set()
    for err in file_errors:
        path = err['path']
        if path in REMAINING_FIXES:
            files_to_fix.add(err['source'])
    
    print(f"\n待修复文件数: {len(files_to_fix)}")
    
    total_fixes = 0
    fixed_files = []
    
    for file_path in sorted(files_to_fix):
        full_path = os.path.join(base_path, file_path.replace("\\", "/"))
        if os.path.exists(full_path):
            count, fixes = fix_file(full_path, REMAINING_FIXES)
            if count > 0:
                total_fixes += count
                fixed_files.append((file_path, count))
    
    print("\n" + "=" * 80)
    print("修复完成")
    print("=" * 80)
    print(f"修复文件数: {len(fixed_files)}")
    print(f"修复链接数: {total_fixes}")
    
    for fp, cnt in fixed_files:
        print(f"  {fp}: {cnt}处")

if __name__ == "__main__":
    main()
