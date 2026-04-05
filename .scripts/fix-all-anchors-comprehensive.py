#!/usr/bin/env python3
"""
全面锚点修复脚本 v3.0
====================
自动修复所有Markdown文档中的锚点问题
支持多种修复策略
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Set, Dict


def generate_anchor_github(header_text: str) -> str:
    """生成GitHub风格的锚点"""
    # 1. 转小写
    anchor = header_text.lower()
    # 2. 移除标点，但保留连字符和空格
    anchor = re.sub(r'[^\w\s-]', '', anchor)
    # 3. 空格替换为连字符
    anchor = anchor.replace(' ', '-')
    # 4. 合并多个连字符
    anchor = re.sub(r'-+', '-', anchor)
    # 5. 移除首尾连字符
    anchor = anchor.strip('-')
    return anchor


def extract_all_headers(content: str) -> Dict[str, str]:
    """提取所有标题和对应的锚点"""
    headers = {}
    
    # 匹配Markdown标题
    header_pattern = r'^(#{1,6})\s+(.+?)(?:\s+\{#[^}]+\})?$'
    for match in re.finditer(header_pattern, content, re.MULTILINE):
        level = len(match.group(1))
        header_text = match.group(2).strip()
        anchor = generate_anchor_github(header_text)
        if anchor:
            headers[anchor] = header_text
            # 也存储带连字符变化的版本
            headers[anchor.replace('--', '-')] = header_text
    
    return headers


def extract_all_anchors(content: str) -> Set[str]:
    """提取文档中所有可能的锚点"""
    anchors = set()
    headers = extract_all_headers(content)
    anchors.update(headers.keys())
    
    # 从自定义锚点提取
    anchor_pattern = r'<a\s+(?:name|id)=["\']([^"\']+)["\']'
    for match in re.finditer(anchor_pattern, content, re.IGNORECASE):
        anchors.add(match.group(1))
    
    # 从标题ID提取
    custom_id_pattern = r'\{#([^}]+)\}'
    for match in re.finditer(custom_id_pattern, content):
        custom_id = match.group(1).strip('#')
        anchors.add(custom_id)
    
    return anchors


def find_broken_anchor_links(content: str) -> List[Tuple[str, str, str]]:
    """找出所有失效的锚点链接 [text](#anchor)"""
    broken = []
    all_anchors = extract_all_anchors(content)
    headers = extract_all_headers(content)
    
    # 匹配锚点链接
    anchor_link_pattern = r'\[([^\]]+)\]\((#[^)]+)\)'
    
    for match in re.finditer(anchor_link_pattern, content):
        full_match = match.group(0)
        link_text = match.group(1)
        url = match.group(2)
        anchor = url[1:]  # 移除开头的#
        
        # 规范化锚点进行比较
        anchor_normalized = anchor.replace('--', '-').strip('-')
        
        # 检查锚点是否存在
        exists = False
        for existing in all_anchors:
            if existing == anchor or existing.replace('--', '-') == anchor_normalized:
                exists = True
                break
        
        if not exists:
            broken.append((full_match, link_text, anchor))
    
    return broken


def find_best_matching_anchor(target_anchor: str, all_anchors: Set[str]) -> str:
    """找到最匹配的锚点"""
    target_normalized = target_anchor.replace('--', '-').strip('-')
    
    # 策略1: 完全匹配
    for anchor in all_anchors:
        if anchor == target_anchor:
            return anchor
    
    # 策略2: 规范化后匹配
    for anchor in all_anchors:
        if anchor.replace('--', '-') == target_normalized:
            return anchor
    
    # 策略3: 包含关系
    for anchor in all_anchors:
        if target_normalized in anchor.replace('--', '-') or anchor.replace('--', '-') in target_normalized:
            if abs(len(target_normalized) - len(anchor.replace('--', '-'))) < 20:
                return anchor
    
    # 策略4: 相似度匹配
    best_match = None
    best_score = 0
    
    for anchor in all_anchors:
        # 计算共同子串长度
        anchor_norm = anchor.replace('--', '-')
        common = set(target_normalized) & set(anchor_norm)
        score = len(common)
        
        if score > best_score:
            best_score = score
            best_match = anchor
    
    if best_score > len(target_normalized) * 0.5:
        return best_match
    
    return None


def fix_link_in_content(content: str, broken_link: str, correct_anchor: str) -> str:
    """在内容中修复链接"""
    # 提取原链接的锚点
    match = re.search(r'\(#[^)]+\)', broken_link)
    if not match:
        return content
    
    old_url = match.group(0)
    new_url = f'(#{correct_anchor})'
    
    new_link = broken_link.replace(old_url, new_url)
    return content.replace(broken_link, new_link, 1)


def add_custom_anchor_to_header(content: str, anchor: str) -> str:
    """在合适的标题后添加自定义锚点"""
    # 找到包含类似文本的标题
    anchor_parts = anchor.replace('--', '-').split('-')
    
    header_pattern = r'^(#{1,6}\s+.+)$'
    for match in re.finditer(header_pattern, content, re.MULTILINE):
        header_line = match.group(1)
        header_text = re.sub(r'^#{1,6}\s+', '', header_line).strip()
        
        # 检查标题是否包含锚点关键词
        header_lower = header_text.lower()
        anchor_lower = anchor.lower()
        
        # 如果标题文本与锚点相似
        similarity = len(set(header_lower.split()) & set(anchor_lower.split('-')))
        if similarity > 0 and abs(len(header_text) - len(anchor)) < 50:
            # 添加自定义锚点
            if '{#' not in header_line:
                new_header = f"{header_line} {{#{anchor}}}"
                return content.replace(header_line, new_header, 1)
    
    return content


def fix_file_comprehensive(file_path: Path) -> Tuple[int, List[str]]:
    """全面修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return 0, [f"❌ 无法读取: {e}"]
    
    original_content = content
    all_anchors = extract_all_anchors(content)
    broken_links = find_broken_anchor_links(content)
    
    if not broken_links:
        return 0, []
    
    fixed_count = 0
    log = []
    
    for broken_link, link_text, anchor in broken_links:
        # 尝试找到最佳匹配的锚点
        best_match = find_best_matching_anchor(anchor, all_anchors)
        
        if best_match and best_match != anchor:
            # 方法1: 修复链接指向
            new_content = fix_link_in_content(content, broken_link, best_match)
            if new_content != content:
                content = new_content
                fixed_count += 1
                log.append(f"  ✅ 修复链接: [{link_text}](#{anchor}) → (#{best_match})")
                # 更新锚点集合
                all_anchors = extract_all_anchors(content)
                continue
        
        # 方法2: 添加自定义锚点
        new_content = add_custom_anchor_to_header(content, anchor)
        if new_content != content:
            content = new_content
            fixed_count += 1
            log.append(f"  ✅ 添加锚点: [{link_text}](#{anchor}) → 在标题添加{{#{anchor}}}")
            all_anchors = extract_all_anchors(content)
            continue
        
        # 无法修复
        log.append(f"  ⚠️  无法修复: [{link_text}](#{anchor})")
    
    if fixed_count > 0 and content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return fixed_count, log


def main():
    # 项目根目录
    root_dir = Path('.')
    
    # 查找所有Markdown文件
    md_files = list(root_dir.rglob('*.md'))
    md_files = [f for f in md_files if '.git' not in str(f) and '__pycache__' not in str(f)]
    
    print(f"🔍 扫描 {len(md_files)} 个Markdown文件...")
    print("=" * 70)
    
    total_fixed = 0
    total_files = 0
    report = ["# 全面锚点修复报告 v3.0", ""]
    
    for file_path in sorted(md_files):
        fixed, log = fix_file_comprehensive(file_path)
        
        if fixed > 0:
            total_fixed += fixed
            total_files += 1
            report.append(f"## {file_path}")
            report.append(f"✅ 修复 {fixed} 个问题")
            report.extend(log)
            report.append("")
            print(f"✅ {file_path}: 修复 {fixed} 个问题")
        elif log:
            # 有无法修复的问题
            report.append(f"## {file_path}")
            report.append(f"⚠️ 部分问题无法修复")
            report.extend(log)
            report.append("")
    
    report.append("=" * 70)
    report.append(f"## 总计")
    report.append(f"修复文件数: {total_files}")
    report.append(f"修复问题数: {total_fixed}")
    
    # 保存报告
    report_path = Path('COMPREHENSIVE-ANCHOR-FIX-REPORT.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print("=" * 70)
    print(f"✅ 修复完成！")
    print(f"📁 修复文件: {total_files} 个")
    print(f"🔧 修复问题: {total_fixed} 个")
    print(f"📄 报告: {report_path}")
    
    return total_fixed


if __name__ == '__main__':
    main()
