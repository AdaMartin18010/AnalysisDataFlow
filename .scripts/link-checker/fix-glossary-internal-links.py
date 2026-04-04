#!/usr/bin/env python3
"""
修复GLOSSARY.md内部的无效锚点链接
"""

import re
from pathlib import Path

def main():
    glossary_file = Path("E:\\_src\\AnalysisDataFlow\GLOSSARY.md")
    
    # 读取文件
    with open(glossary_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 定义映射：无效锚点 -> 有效锚点
    anchor_mapping = {
        '#流计算相关': '#1-基础术语',
        '#批处理相关': '#1-基础术语',
        '#实时处理相关': '#1-基础术语',
        '#进程演算术语': '#2-理论术语',
        '#形式化验证术语': '#2-理论术语',
        '#类型理论术语': '#2-理论术语',
        '#核心概念': '#3-flink术语',
        '#配置参数': '#3-flink术语',
        '#设计模式术语': '#4-工程术语',
        '#架构术语': '#4-工程术语',
        '#运维术语': '#4-工程术语',
        '#性能优化-术语': '#5-前沿术语',
        '#流批一体-术语': '#5-前沿术语',
        '#流数据库术语': '#5-前沿术语',
        '#云原生术语': '#5-前沿术语',
    }
    
    fixes = []
    
    for old_anchor, new_anchor in anchor_mapping.items():
        old_link = f"]({old_anchor})"
        new_link = f"]({new_anchor})"
        
        if old_link in content:
            content = content.replace(old_link, new_link)
            fixes.append({
                'old': old_anchor,
                'new': new_anchor
            })
    
    # 保存修复后的文件
    if content != original_content:
        with open(glossary_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"修复了 {len(fixes)} 个链接:")
        for fix in fixes:
            print(f"  {fix['old']} -> {fix['new']}")
    else:
        print("无需修复")
    
    return len(fixes)

if __name__ == "__main__":
    count = main()
    print(f"\n总计修复: {count} 个链接")
