#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
断链分析工具
===========

分析 broken_links_full.json 文件，分类断链类型并生成修复建议。

功能:
    - 检测代码片段误报
    - 识别文件缺失链接
    - 按源文件分组统计
    - 生成真实断链列表

用法:
    python analyze_broken_links.py

输出:
    broken_links_real.json - 需要修复的真实断链列表
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict


def load_links(file_path: str = 'broken_links_full.json') -> List[Dict[str, Any]]:
    """加载断链数据文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def is_code_false_positive(url: str) -> bool:
    """
    检测URL是否为代码片段误报
    
    这些是在Markdown表格或代码块中的误解析链接。
    
    Args:
        url: 待检测的URL
        
    Returns:
        bool: 是否为误报
    """
    code_indicators = ['`', '\n', 'classOf', '=>', 'StateDeclaration', 
                       'StreamKey', '|', '<', '>']
    return any(indicator in url for indicator in code_indicators)


def is_file_link(url: str) -> bool:
    """
    判断URL是否为文件链接
    
    Args:
        url: 待检测的URL
        
    Returns:
        bool: 是否为文件链接
    """
    if url.startswith('./') or url.startswith('../'):
        return True
    if not url.startswith(('http', '#', 'mailto')) and '.md' in url.lower():
        return True
    return False


def categorize_links(links: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    将断链分类为不同类型
    
    Args:
        links: 原始断链列表
        
    Returns:
        Dict: 分类后的断链字典
    """
    categories = {
        'code_false_positives': [],
        'file_not_found': [],
        'possible_moves': []
    }
    
    for link in links:
        url = link['url']
        
        if is_code_false_positive(url):
            categories['code_false_positives'].append(link)
        elif is_file_link(url):
            categories['file_not_found'].append(link)
        else:
            categories['possible_moves'].append(link)
    
    return categories


def group_by_source(links: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    按源文件分组统计断链
    
    Args:
        links: 断链列表
        
    Returns:
        Dict: 按源文件分组的断链
    """
    by_source = defaultdict(list)
    for link in links:
        src = link['source']
        by_source[src].append(link)
    return dict(by_source)


def count_targets(links: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    统计常见断链目标
    
    Args:
        links: 断链列表
        
    Returns:
        Dict: 目标URL及其出现次数
    """
    target_counts = defaultdict(int)
    for link in links:
        target = link['url']
        target_counts[target] += 1
    return dict(target_counts)


def save_real_broken_links(links: List[Dict[str, Any]], 
                           output_file: str = 'broken_links_real.json') -> int:
    """
    保存真实需要修复的断链
    
    Args:
        links: 真实断链列表
        output_file: 输出文件路径
        
    Returns:
        int: 保存的链接数量
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(links, f, ensure_ascii=False, indent=2)
    return len(links)


def print_analysis_report(categories: Dict[str, List[Dict[str, Any]]],
                          by_source: Dict[str, List[Dict[str, Any]]],
                          target_counts: Dict[str, int]) -> None:
    """打印分析报告"""
    print('=== 断链分析统计 ===')
    print(f"代码片段误报（可忽略）: {len(categories['code_false_positives'])}")
    print(f"真实文件缺失: {len(categories['file_not_found'])}")
    print(f"其他: {len(categories['possible_moves'])}")
    print()
    
    print(f'=== 涉及 {len(by_source)} 个源文件的断链 ===')
    sorted_sources = sorted(by_source.items(), key=lambda x: -len(x[1]))[:20]
    for src, links in sorted_sources:
        print(f'{src}: {len(links)} 个断链')
    print()
    
    print('=== 常见的断链目标 ===')
    sorted_targets = sorted(target_counts.items(), key=lambda x: -x[1])[:20]
    for target, count in sorted_targets:
        print(f'{count}x: {target}')
    print()


def main() -> int:
    """主函数"""
    try:
        # 加载数据
        links = load_links()
        
        # 分类断链
        categories = categorize_links(links)
        
        # 按源文件分组
        by_source = group_by_source(categories['file_not_found'])
        
        # 统计目标
        target_counts = count_targets(categories['file_not_found'])
        
        # 打印报告
        print_analysis_report(categories, by_source, target_counts)
        
        # 保存真实断链
        count = save_real_broken_links(categories['file_not_found'])
        print(f'真实断链已保存到 broken_links_real.json ({count} 个)')
        
        return 0
        
    except FileNotFoundError:
        print("错误: 找不到 broken_links_full.json 文件")
        return 1
    except json.JSONDecodeError as e:
        print(f"错误: JSON解析失败 - {e}")
        return 1
    except Exception as e:
        print(f"错误: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
