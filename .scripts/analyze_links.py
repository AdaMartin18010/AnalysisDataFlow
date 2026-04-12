#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析链接检测结果并生成修复计划"""

import json
import re
from datetime import datetime

def analyze_links():
    with open('.scripts/.link_health_results_v4.1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 分类统计
    not_found = []
    placeholder = []
    localhost = []
    connection_error = []
    timeout = []
    forbidden = []
    
    for result in data['results']:
        url = result['url']
        category = result['category']
        
        if category == 'not_found':
            not_found.append(result)
        elif category == 'connection_error':
            connection_error.append(result)
        elif category == 'timeout':
            timeout.append(result)
        elif category == 'forbidden':
            forbidden.append(result)
        
        # 检测占位符链接
        if 'your-org' in url or 'your-repo' in url:
            placeholder.append(result)
        
        # 检测localhost链接
        if 'localhost' in url or '127.0.0.1' in url:
            localhost.append(result)

    print(f'=== 链接问题统计 ===')
    print(f'404 Not Found: {len(not_found)}')
    print(f'Connection Error: {len(connection_error)}')
    print(f'Timeout: {len(timeout)}')
    print(f'Forbidden: {len(forbidden)}')
    print(f'Placeholder links (your-org/your-repo): {len(placeholder)}')
    print(f'Localhost links: {len(localhost)}')

    print('\n=== 404 Not Found Links ===')
    for r in not_found:
        print(f"  {r['url']}")
        print(f"    Files: {r['source_files'][:3]}")

    print('\n=== Connection Error Links ===')
    for r in connection_error:
        print(f"  {r['url']}")

    print('\n=== Placeholder Links ===')
    for r in placeholder:
        print(f"  {r['url']}")
        print(f"    Files: {r['source_files'][:3]}")
        
    print('\n=== Localhost Links ===')
    for r in localhost:
        print(f"  {r['url']}")

    # 保存详细结果
    analysis = {
        'analysis_time': datetime.now().isoformat(),
        'categories': {
            'not_found': not_found,
            'connection_error': connection_error,
            'timeout': timeout,
            'forbidden': forbidden,
            'placeholder': placeholder,
            'localhost': localhost
        },
        'counts': {
            'not_found': len(not_found),
            'connection_error': len(connection_error),
            'timeout': len(timeout),
            'forbidden': len(forbidden),
            'placeholder': len(placeholder),
            'localhost': len(localhost)
        }
    }
    
    with open('.scripts/link_analysis_result.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f'\n分析结果已保存到 .scripts/link_analysis_result.json')
    return analysis

if __name__ == '__main__':
    analyze_links()
