#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Broken Link Fixer v4.2
修复 broken_links_real.json 中的失效内部链接
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

def main():
    with open('broken_links_real.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Index all non-release markdown files
    all_md = {}
    for fp in Path('.').rglob('*.md'):
        ps = str(fp).replace('\\', '/')
        if 'release/' in ps or 'node_modules/' in ps or '.git/' in ps:
            continue
        all_md[fp.name] = all_md.get(fp.name, []) + [ps]
        all_md[fp.stem] = all_md.get(fp.stem, []) + [ps]
    
    # Known directory renames
    dir_mappings = {
        'Flink/12-ai-ml/': 'Flink/06-ai-ml/',
        'Flink/06-engineering/': 'Flink/09-practices/09.03-performance-tuning/',
        'Flink/03-sql-table-api/': 'Flink/03-api/03.02-table-sql-api/',
        'Flink/02-core-mechanisms/': 'Flink/02-core/',
        'Flink/01-architecture/': 'Flink/01-concepts/',
        'Flink/13-security/': 'Flink/09-practices/09.04-security/',
    }
    
    def resolve_abs(source, url):
        """Resolve relative URL to absolute path from project root"""
        source_dir = Path(source).parent
        url_no_anchor = url.split('#')[0]
        if url.startswith('./') or url.startswith('../'):
            try:
                resolved = (source_dir / url_no_anchor).resolve()
                rel = resolved.relative_to(Path('.').resolve())
                return str(rel).replace('\\', '/')
            except:
                return None
        return url_no_anchor
    
    def compute_rel(source, target_abs):
        """Compute relative path from source to target"""
        source_dir = Path(source).parent
        target_path = Path(target_abs.replace('/', '\\'))
        try:
            rel = os.path.relpath(str(target_path), str(source_dir)).replace('\\', '/')
            return rel
        except:
            return target_abs
    
    def find_fix(source, url):
        url_no_anchor = url.split('#')[0]
        anchor = '#' + url.split('#', 1)[1] if '#' in url else ''
        abs_target = resolve_abs(source, url)
        
        # If target actually exists, it's a false positive (e.g., anchor issue)
        if abs_target and os.path.exists(abs_target):
            return None  # Don't fix
        
        # Try directory prefix mappings first
        for old_prefix, new_prefix in dir_mappings.items():
            if url.startswith(old_prefix):
                new_url = url.replace(old_prefix, new_prefix, 1)
                new_no_anchor = new_url.split('#')[0]
                if os.path.exists(new_no_anchor):
                    return new_url
                # Search in new prefix directory
                search_path = Path(new_prefix)
                target_name = Path(new_no_anchor).name
                if search_path.exists():
                    found = list(search_path.rglob(target_name))
                    if found:
                        rel = compute_rel(source, str(found[0]).replace('\\', '/'))
                        return rel + anchor
        
        # For non-prefixed relative links in Flink context
        if not url.startswith('Flink/') and not url.startswith('../') and not url.startswith('./'):
            for old_prefix, new_prefix in dir_mappings.items():
                old_local = old_prefix.replace('Flink/', '')
                if url.startswith(old_local):
                    new_local = new_prefix.replace('Flink/', '')
                    new_url = url.replace(old_local, new_local, 1)
                    new_no_anchor = new_url.split('#')[0]
                    candidate = 'Flink/' + new_no_anchor
                    if os.path.exists(candidate):
                        rel = compute_rel(source, candidate)
                        return rel + anchor
        
        # Try filename lookup
        target_name = Path(url_no_anchor).name
        if target_name in all_md:
            candidates = all_md[target_name]
            if len(candidates) == 1:
                best = candidates[0]
            else:
                # Score by path overlap
                best = None
                best_score = -1
                source_parts = set(Path(source).parts)
                for c in candidates:
                    c_parts = set(Path(c).parts)
                    score = len(source_parts & c_parts)
                    # Prefer Flink/ over release/ or i18n/
                    if 'i18n/' in c:
                        score -= 5
                    if score > best_score:
                        best_score = score
                        best = c
            rel = compute_rel(source, best)
            return rel + anchor
        
        # Try stem lookup for files without .md
        target_stem = Path(url_no_anchor).stem
        if target_stem in all_md and '.' not in target_name:
            candidates = all_md[target_stem]
            if len(candidates) == 1:
                best = candidates[0]
            else:
                best = candidates[0]  # simple fallback
            rel = compute_rel(source, best)
            return rel + anchor
        
        return None
    
    # Group by source file
    by_source = defaultdict(list)
    for item in data:
        src = item['source'].lstrip('.\\/')
        by_source[src].append(item)
    
    fixes_applied = []
    fixes_failed = []
    skipped_existing = []
    files_modified = set()
    
    for source, items in by_source.items():
        if not os.path.exists(source):
            continue
        
        try:
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        
        new_content = content
        modified = False
        
        for item in items:
            url = item['url']
            text = item['text']
            fix = find_fix(source, url)
            
            if fix is None:
                # Check if it's a false positive
                abs_target = resolve_abs(source, url)
                if abs_target and os.path.exists(abs_target):
                    skipped_existing.append(item)
                else:
                    fixes_failed.append(item)
                continue
            
            # Apply fix in content
            # Need to handle markdown link patterns carefully
            # Pattern: [text](url) or [text](url "title")
            old_pattern = re.escape(f'[{text}]({url})')
            new_link = f'[{text}]({fix})'
            
            if old_pattern in new_content:
                new_content = new_content.replace(f'[{text}]({url})', new_link)
                modified = True
                fixes_applied.append({
                    'source': source,
                    'text': text,
                    'old_url': url,
                    'new_url': fix,
                    'line': item.get('line', 0)
                })
            else:
                # Try regex-based replacement
                escaped_text = re.escape(text)
                escaped_url = re.escape(url)
                pattern = rf'\[{escaped_text}\]\({escaped_url}(?:\s+\"[^\"]*\")?\)'
                matches = list(re.finditer(pattern, new_content))
                if matches:
                    # Replace last occurrence to avoid offset issues
                    for m in reversed(matches):
                        start, end = m.span()
                        new_content = new_content[:start] + new_link + new_content[end:]
                    modified = True
                    fixes_applied.append({
                        'source': source,
                        'text': text,
                        'old_url': url,
                        'new_url': fix,
                        'line': item.get('line', 0)
                    })
                else:
                    fixes_failed.append(item)
        
        if modified:
            with open(source, 'w', encoding='utf-8') as f:
                f.write(new_content)
            files_modified.add(source)
    
    # Generate report
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report_lines = [
        '# 外部链接修复报告 v4.2',
        '',
        f'**生成时间**: {timestamp}',
        '',
        '## 修复统计',
        '',
        '| 指标 | 数值 |',
        '|------|------|',
        f'| 检测到的失效链接总数 | {len(data)} |',
        f'| 已修复链接 | {len(fixes_applied)} |',
        f'| 无法修复 (目标不存在) | {len(fixes_failed)} |',
        f'| 误报 (目标实际存在) | {len(skipped_existing)} |',
        f'| 修改的文件数 | {len(files_modified)} |',
        '',
        '## 修复详情 (前 100 条)',
        '',
    ]
    
    for fix in fixes_applied[:100]:
        report_lines.append(f"- `{fix['source']}` 第{fix['line']}行")
        report_lines.append(f"  - 旧: `[{fix['text']}]({fix['old_url']})`")
        report_lines.append(f"  - 新: `[{fix['text']}]({fix['new_url']})`")
        report_lines.append('')
    
    if len(fixes_applied) > 100:
        report_lines.append(f'... 还有 {len(fixes_applied) - 100} 条修复记录')
        report_lines.append('')
    
    report_lines.append('## 未修复链接示例 (前 50 条)')
    report_lines.append('')
    for fail in fixes_failed[:50]:
        report_lines.append(f"- `{fail['source']}`: `[{fail['text']}]({fail['url']})`")
    if len(fixes_failed) > 50:
        report_lines.append(f"- ... 还有 {len(fixes_failed) - 50} 条未修复")
    report_lines.append('')
    
    report_lines.append('## 修复规则说明')
    report_lines.append('')
    report_lines.append('1. **目录重映射**: Flink/12-ai-ml/ → Flink/06-ai-ml/ 等')
    report_lines.append('2. **文件名查找**: 通过全局文件名索引自动定位目标文档')
    report_lines.append('3. **相对路径保持**: 修复后的链接仍保持相对路径格式')
    report_lines.append('4. **误报过滤**: 对实际存在的目标文件（如 README.md）跳过修复')
    report_lines.append('')
    
    with open('EXTERNAL-LINK-FIX-REPORT-v4.2.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f'已修复: {len(fixes_applied)}')
    print(f'未修复: {len(fixes_failed)}')
    print(f'误报: {len(skipped_existing)}')
    print(f'修改文件: {len(files_modified)}')
    print('报告: EXTERNAL-LINK-FIX-REPORT-v4.2.md')

if __name__ == '__main__':
    main()
