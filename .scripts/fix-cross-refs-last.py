#!/usr/bin/env python3
"""
最终修复脚本 - 处理剩余的缺失引用
对于缺失的规划文档，指向路线图或标记为#
"""

import re
import os

# 最终修复映射
FINAL_FIXES = {
    # 缺失的规划文档 -> 路线图文档
    "flink-24/flink-24-adaptive-execution-v2.md": "../08-roadmap/08.01-flink-24/flink-2.4-tracking.md",
    "flink-24/flink-24-ansi-sql-2023.md": "../08-roadmap/08.01-flink-24/flink-2.4-tracking.md",
    "flink-24/flink-24-new-connectors.md": "../08-roadmap/08.01-flink-24/flink-2.4-tracking.md",
    "flink-24/flink-24-observability-enhancements.md": "../08-roadmap/08.01-flink-24/flink-2.4-tracking.md",
    "flink-24/flink-24-smart-checkpointing.md": "../08-roadmap/08.01-flink-24/flink-2.4-tracking.md",
    "flink-24/flink-24-serverless-ga.md": "../08-roadmap/08.01-flink-24/flink-2.4-tracking.md",
    "flink-24/flink-24-ai-agents-ga.md": "../06-ai-ml/flink-ai-agents-flip-531.md",
    
    "flink-25/flink-25-stream-batch-unified.md": "../08-roadmap/08.01-flink-24/flink-25-stream-batch-unification.md",
    "flink-25/flink-25-ai-ml-production.md": "../06-ai-ml/flink-ai-agents-flip-531.md",
    "flink-25/flink-25-serverless-v2.md": "../08-roadmap/08.01-flink-24/flink-2.5-preview.md",
    "flink-25/flink-25-storage-backends.md": "../02-core/state-backends-deep-comparison.md",
    "flink-25/flink-25-performance.md": "../09-practices/09.03-performance-tuning/flink-24-performance-improvements.md",
    "flink-25/flink-25-observability.md": "../04-runtime/04.03-observability/distributed-tracing.md",
    "flink-25/flink-25-deployment.md": "../04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md",
    "flink-25/flink-25-new-connectors.md": "../08-roadmap/08.01-flink-24/flink-2.5-preview.md",
    
    "flink-30/flink-30-architecture-changes.md": "../08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md",
    "flink-30/flink-30-api-redesign.md": "../08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md",
    "flink-30/flink-30-cloud-native.md": "../08-roadmap/08.01-flink-24/flink-30-architecture-redesign.md",
    "flink-30/flink-30-state-management.md": "../02-core/state-backends-deep-comparison.md",
    "flink-30/flink-30-ai-native.md": "../06-ai-ml/flink-ai-agents-flip-531.md",
    "flink-30/flink-30-performance.md": "../09-practices/09.03-performance-tuning/flink-24-performance-improvements.md",
    "flink-30/flink-30-security.md": "../09-practices/09.04-security/flink-security-complete-guide.md",
    "flink-30/flink-30-connectors.md": "../05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md",
    "flink-30/flink-30-observability.md": "../04-runtime/04.03-observability/distributed-tracing.md",
    "flink-30/flink-30-sql-standard.md": "../03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md",
    
    # 缺失的架构文档 -> 现有文档
    "../../../Flink/04-runtime/04.03-observability/flink-rpc-internals.md": "../../../Flink/04-runtime/04.03-observability/distributed-tracing.md",
    "../../Flink/05-ecosystem/05.03-wasm-udf/wasm-runtime-fundamentals.md": "../../Flink/05-ecosystem/05.03-wasm-udf/09-wasm-udf-frameworks.md",
    "./flink-ycsb-benchmark-guide.md": "./flink-nexmark-benchmark-guide.md",
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
    print("最终修复 - 处理规划文档引用")
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
        if path in FINAL_FIXES:
            files_to_fix.add(err['source'])
    
    print(f"\n待修复文件数: {len(files_to_fix)}")
    
    # 修复每个文件
    total_fixes = 0
    fixed_files = []
    
    for file_path in sorted(files_to_fix):
        full_path = os.path.join(base_path, file_path.replace("\\", "/"))
        if os.path.exists(full_path):
            count, fixes = fix_file(full_path, FINAL_FIXES)
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

if __name__ == "__main__":
    main()
