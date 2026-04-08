#!/usr/bin/env python3
"""
交叉引用修复脚本 v2 - 全面修复
"""

import re
import os
import json
from pathlib import Path
from collections import defaultdict

def get_relative_path(from_file, to_file, base_path):
    """计算从 from_file 到 to_file 的相对路径"""
    try:
        from_path = Path(from_file).parent
        to_path = Path(to_file)
        
        # 计算相对路径
        rel = os.path.relpath(to_path, from_path).replace("\\", "/")
        return rel
    except Exception as e:
        return None

def fix_links_in_file(file_path, base_path, all_files):
    """修复单个文件中的链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes = []
        file_dir = os.path.dirname(file_path)
        
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
            
            # 如果路径已经存在，跳过
            if path_part.startswith("../") or path_part.startswith("./"):
                # 检查路径是否正确
                full = os.path.normpath(os.path.join(file_dir, path_part))
                if os.path.exists(full):
                    return match.group(0)
            
            # 尝试找到目标文件
            # 1. 直接尝试作为相对路径
            direct_path = os.path.normpath(os.path.join(file_dir, path_part))
            if os.path.exists(direct_path):
                return match.group(0)
            
            # 2. 从 base_path 尝试
            base_target = os.path.join(base_path, path_part)
            if os.path.exists(base_target):
                # 计算正确的相对路径
                new_path = get_relative_path(file_path, base_target, base_path)
                if new_path:
                    if anchor:
                        new_link = f"[{text}]({new_path}#{anchor})"
                    else:
                        new_link = f"[{text}]({new_path})"
                    fixes.append(f"  {path_part} -> {new_path}")
                    return new_link
            
            # 3. 尝试在 all_files 中查找相似文件名
            target_name = os.path.basename(path_part)
            for existing_file in all_files:
                if os.path.basename(existing_file) == target_name:
                    new_path = get_relative_path(file_path, existing_file, base_path)
                    if new_path:
                        if anchor:
                            new_link = f"[{text}]({new_path}#{anchor})"
                        else:
                            new_link = f"[{text}]({new_path})"
                        fixes.append(f"  {path_part} -> {new_path} (by name)")
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
    import glob
    
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    base_path = os.path.abspath(base_path)
    
    print("=" * 80)
    print("交叉引用修复脚本 v2")
    print("=" * 80)
    
    # 加载错误报告
    report_path = os.path.join(base_path, "cross-ref-report.json")
    if not os.path.exists(report_path):
        print(f"错误报告不存在: {report_path}")
        return
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    # 获取所有Markdown文件
    all_files = []
    for pattern in ["Struct/**/*.md", "Knowledge/**/*.md", "Flink/**/*.md"]:
        all_files.extend(glob.glob(os.path.join(base_path, pattern), recursive=True))
    all_files = [os.path.abspath(f) for f in all_files if not f.endswith("_TEMPLATE.md")]
    
    print(f"\n项目文件总数: {len(all_files)}")
    
    file_errors = report['errors']['file_not_found']
    anchor_errors = report['errors']['anchor_not_found']
    
    print(f"待修复错误:")
    print(f"  - 文件引用错误: {len(file_errors)}")
    print(f"  - 锚点引用错误: {len(anchor_errors)}")
    
    # 收集需要修复的文件
    files_to_fix = set()
    for err in file_errors:
        files_to_fix.add(err['source'])
    
    print(f"\n涉及文件数: {len(files_to_fix)}")
    
    # 修复每个文件
    total_fixes = 0
    fixed_files = []
    
    for i, file_path in enumerate(sorted(files_to_fix), 1):
        full_path = os.path.join(base_path, file_path.replace("\\", "/"))
        if os.path.exists(full_path):
            if i % 50 == 0:
                print(f"  已处理: {i}/{len(files_to_fix)}")
            count, fixes = fix_links_in_file(full_path, base_path, all_files)
            if count > 0:
                total_fixes += count
                fixed_files.append((file_path, count))
    
    print("\n" + "=" * 80)
    print("修复完成统计")
    print("=" * 80)
    print(f"修复文件数: {len(fixed_files)}")
    print(f"修复链接数: {total_fixes}")
    
    if fixed_files:
        print(f"\n修复文件列表 (Top 30):")
        for fp, cnt in sorted(fixed_files, key=lambda x: -x[1])[:30]:
            print(f"  {fp}: {cnt}处")

if __name__ == "__main__":
    main()
