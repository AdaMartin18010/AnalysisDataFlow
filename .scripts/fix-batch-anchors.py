#!/usr/bin/env python3
"""
批量锚点修复脚本 - 全面修复剩余55个问题
"""

import re
from pathlib import Path

def fix_file(filepath, fixes):
    """应用修复到文件"""
    path = Path(filepath)
    if not path.exists():
        return 0
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    count = 0
    for old, new in fixes:
        if old in content:
            content = content.replace(old, new)
            count += 1
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return count
    return 0

def add_anchor_to_header(filepath, header_pattern, anchor_text):
    """在标题后添加自定义锚点"""
    path = Path(filepath)
    if not path.exists():
        return 0
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    # 匹配标题行（确保标题后面没有已有锚点）
    pattern = r'^(#{1,6}\s+' + re.escape(header_pattern) + r')$'
    replacement = r'\1 {' + anchor_text + '}'
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return 1
    return 0

def main():
    total_fixed = 0
    
    # ========== 1. 根目录报告文件 ==========
    print("=== 修复根目录报告文件 ===")
    root_fixes = {
        ".vscode/README.md": [
            ("[📄 PDF 导出功能](#-pdf-导出功能)", "[📄 PDF 导出功能](#pdf-导出功能)"),
        ],
        "CASE-STUDIES.md": [
            ("[🆕 新增详细案例（Knowledge/10-case-studies/）](#-新增详细案例knowledge10-case-studies)", 
             "[🆕 新增详细案例（Knowledge/10-case-studies/）](#新增详细案例)"),
        ],
        # CROSS-REF-VALIDATION-REPORT-v2.md - 这些链接指向不存在的索引文件，需要修改或删除
        # DASHBOARD.md - 相对路径问题
        # 等等...
    }
    
    for filepath, fixes in root_fixes.items():
        fixed = fix_file(filepath, fixes)
        if fixed > 0:
            print(f"✅ {filepath}: 修复 {fixed} 个问题")
            total_fixed += fixed
    
    # ========== 2. Struct/01-foundation ==========
    print("\n=== 修复 Struct/01-foundation ===")
    
    # 01.04-dataflow-model-formalization.md - 重复锚点问题
    fixed = fix_file("Struct/01-foundation/01.04-dataflow-model-formalization.md", [
        # 修复目录中的重复锚点链接
        ('[关系 1: Dataflow Model `⊃` Kahn 进程网络 (KPN) {#关系-1-dataflow-model--kahn-进程网络-kpn} {#关系-1-dataflow-model--kahn-进程网络-kpn-关系-1-dataflow-model--kahn-进程网络-kpn}](#关系-1-dataflow-model--kahn-进程网络-kpn-关系-1-dataflow-model--kahn-进程网络-kpn-关系-1-dataflow-model--kahn-进程网络-kpn-关系-1-dataflow-model--kahn-进程网络-kpn)',
         '[关系 1: Dataflow Model `⊃` Kahn 进程网络 (KPN)](#关系-1-dataflow-model--kahn-进程网络-kpn)'),
        ('[关系 2: 同步数据流 (SDF) `⊂` 动态数据流 (DDF) `≈` Dataflow Model {#关系-2-同步数据流-sdf--动态数据流-ddf--dataflow-model} {#关系-2-同步数据流-sdf--动态数据流-ddf--dataflow-model-关系-2-同步数据流-sdf--动态数据流-ddf--dataflow-model}](#关系-2-同步数据流-sdf--动态数据流-ddf--dataflow-model-关系-2-同步数据流-sdf--动态数据流-ddf--dataflow-model-关系-2-同步数据流-sdf--动态数据流-ddf--dataflow-model-关系-2-同步数据流-sdf--动态数据流-ddf--dataflow-model)',
         '[关系 2: 同步数据流 (SDF) `⊂` 动态数据流 (DDF) `≈` Dataflow Model](#关系-2-同步数据流-sdf--动态数据流-ddf--dataflow-model)'),
        ('[关系 3: Dataflow 理论模型 `↦` Flink Runtime 实现 {#关系-3-dataflow-理论模型--flink-runtime-实现} {#关系-3-dataflow-理论模型--flink-runtime-实现-关系-3-dataflow-理论模型--flink-runtime-实现}](#关系-3-dataflow-理论模型--flink-runtime-实现-关系-3-dataflow-理论模型--flink-runtime-实现-关系-3-dataflow-理论模型--flink-runtime-实现-关系-3-dataflow-理论模型--flink-runtime-实现)',
         '[关系 3: Dataflow 理论模型 `↦` Flink Runtime 实现](#关系-3-dataflow-理论模型--flink-runtime-实现)'),
        ('[5. 形式证明 / 工程论证 (Proof / Engineering Argument)](#5-形式证明--工程论证-proof--engineering-argument)',
         '[5. 形式证明 / 工程论证 (Proof / Engineering Argument)](#5-形式证明--工程论证)'),
    ])
    if fixed > 0:
        print(f"✅ 01.04-dataflow-model-formalization.md: 修复 {fixed} 个问题")
        total_fixed += fixed
    
    # 添加缺失的锚点
    fixed = add_anchor_to_header("Struct/01-foundation/01.04-dataflow-model-formalization.md", 
                                  "5. 形式证明 / 工程论证 (Proof / Engineering Argument)", 
                                  "{#5-形式证明--工程论证}")
    if fixed > 0:
        print(f"✅ 01.04-dataflow-model-formalization.md: 添加锚点")
        total_fixed += fixed
    
    # 01.05-csp-formalization.md
    fixed = add_anchor_to_header("Struct/01-foundation/01.05-csp-formalization.md", 
                                  "基础情形 ($Q = 0$)", 
                                  "{#基础情形-q--0}")
    if fixed > 0:
        print(f"✅ 01.05-csp-formalization.md: 添加锚点 基础情形")
        total_fixed += fixed
    
    fixed = add_anchor_to_header("Struct/01-foundation/01.05-csp-formalization.md", 
                                  "6. 实例验证 (Examples \\& Verification)", 
                                  "{#6-实例验证-examples--verification}")
    if fixed > 0:
        print(f"✅ 01.05-csp-formalization.md: 添加锚点 6.")
        total_fixed += fixed
    
    # 01.06-petri-net-formalization.md
    fixed = fix_file("Struct/01-foundation/01.06-petri-net-formalization.md", [
        ("[Petri 网形式化 (Petri Net Formalization)](#petri-网形式化)", 
         "[Petri 网形式化 (Petri Net Formalization)](#petri-网形式化-petri-net-formalization)"),
        ("[图 1-1: Petri 网结构示例](#图-1-petri-网结构示例)", 
         "[图 1-1: Petri 网结构示例](#图-1-1-petri-网结构示例)"),
        ("[6. 实例验证 (Examples \\& Verification)](#6-实例验证)", 
         "[6. 实例验证 (Examples \\& Verification)](#6-实例验证-examples--verification)"),
    ])
    if fixed > 0:
        print(f"✅ 01.06-petri-net-formalization.md: 修复 {fixed} 个问题")
        total_fixed += fixed
    
    # 添加缺失锚点
    fixed = add_anchor_to_header("Struct/01-foundation/01.06-petri-net-formalization.md", 
                                  "Petri 网形式化 (Petri Net Formalization)", 
                                  "{#petri-网形式化-petri-net-formalization}")
    if fixed > 0:
        print(f"✅ 01.06-petri-net-formalization.md: 添加标题锚点")
        total_fixed += fixed
    
    # 01.07-session-types.md
    fixed = add_anchor_to_header("Struct/01-foundation/01.07-session-types.md", 
                                  "5. 形式证明 / 工程论证 (Proof)", 
                                  "{#5-形式证明--工程论证-proof}")
    if fixed > 0:
        print(f"✅ 01.07-session-types.md: 添加锚点")
        total_fixed += fixed
    
    print(f"\n🔧 本批次总计修复: {total_fixed} 个问题")

if __name__ == '__main__':
    main()
