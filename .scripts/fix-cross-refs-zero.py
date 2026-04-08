#!/usr/bin/env python3
"""
清零修复脚本
"""

import re
import os

# 最终清零修复
ZERO_FIXES = {
    # WASM 路径
    "../../../Flink/05-ecosystem/05.03-wasm-udf/09-wasm-udf-frameworks.md": "../../../Flink/05-ecosystem/05.03-wasm-udf/wasm-streaming.md",
    
    # 脚本路径
    "../../.scripts/flink-version-tracking/flink-release-tracker.py": "../../.scripts/flink-release-tracker.py",
    "../../.tasks/flink-release-tracker.md": "#",
    
    # Go模板语法 - 跳过
    "{{ .GrafanaURL }}": "#",
    "{{ .Annotations.RunbookURL }}": "#",
    "{{ .LogsURL }}": "#",
    
    # 旧目录 -> 新目录
    "../03-sql-table-api/": "../../03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md",
    "../../01-architecture/": "../../01-concepts/deployment-architectures.md",
    "../../09-language-foundations/": "../../03-api/09-language-foundations/flink-rust-native-api-guide.md",
    "../../COMPATIBILITY-MATRIX.md": "../../../COMPATIBILITY-MATRIX.md",
    "../04-connectors/": "../../05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md",
    "../12-ai-ml/": "../../06-ai-ml/flink-ai-agents-flip-531.md",
    "../02-core-mechanisms/": "../../02-core/checkpoint-mechanism-deep-dive.md",
    "../15-observability/": "../../04-runtime/04.03-observability/flink-observability-complete-guide.md",
    "../../Flink/01-architecture/": "../../01-concepts/deployment-architectures.md",
    "../14-graph/": "../../05-ecosystem/05.04-graph/flink-gelly-streaming-graph-processing.md",
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
            
            if link.startswith("http") or link.startswith("mailto:"):
                return match.group(0)
            
            if "#" in link:
                path_part, anchor = link.split("#", 1)
            else:
                path_part, anchor = link, None
            
            if path_part in fixes_map:
                new_path = fixes_map[path_part]
                if anchor and new_path != "#":
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
    print("清零修复")
    print("=" * 80)
    
    report_path = os.path.join(base_path, "cross-ref-report.json")
    if not os.path.exists(report_path):
        return
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    file_errors = report['errors']['file_not_found']
    
    files_to_fix = set()
    for err in file_errors:
        path = err['path']
        if path in ZERO_FIXES:
            files_to_fix.add(err['source'])
    
    print(f"待修复文件数: {len(files_to_fix)}")
    
    total_fixes = 0
    fixed_files = []
    
    for file_path in sorted(files_to_fix):
        full_path = os.path.join(base_path, file_path.replace("\\", "/"))
        if os.path.exists(full_path):
            count, fixes = fix_file(full_path, ZERO_FIXES)
            if count > 0:
                total_fixes += count
                fixed_files.append((file_path, count))
    
    print(f"\n修复完成")
    print(f"修复文件数: {len(fixed_files)}")
    print(f"修复链接数: {total_fixes}")

if __name__ == "__main__":
    main()
