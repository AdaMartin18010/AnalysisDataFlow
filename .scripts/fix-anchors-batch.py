#!/usr/bin/env python3
"""
批量修复锚点问题脚本
====================
自动修复Markdown文档中的锚点不一致问题
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Set


def generate_anchor_from_header(header_text: str) -> str:
    """从标题文本生成GitHub风格的锚点"""
    # 1. 转小写
    anchor = header_text.lower()
    # 2. 移除标点（保留连字符、空格、下划线）
    anchor = re.sub(r'[^\w\s-]', '', anchor)
    # 3. 空格替换为连字符
    anchor = anchor.replace(' ', '-')
    # 4. 合并多个连字符
    anchor = re.sub(r'-+', '-', anchor)
    # 5. 移除首尾连字符
    anchor = anchor.strip('-')
    return anchor


def extract_all_anchors(content: str) -> Set[str]:
    """提取文档中所有可能的锚点"""
    anchors = set()
    
    # 从标题提取
    header_pattern = r'^#{1,6}\s+(.+?)(?:\s*\{#[^}]+\})?$'
    for match in re.finditer(header_pattern, content, re.MULTILINE):
        header_text = match.group(1).strip()
        anchor = generate_anchor_from_header(header_text)
        if anchor:
            anchors.add(anchor)
    
    # 从自定义锚点提取
    anchor_pattern = r'<a\s+(?:name|id)=["\']([^"\']+)["\']'
    for match in re.finditer(anchor_pattern, content, re.IGNORECASE):
        anchors.add(match.group(1))
    
    # 从标题ID提取（如 ### Title {#custom-id}）
    custom_id_pattern = r'^#{1,6}\s+.+\s+\{#([^}]+)\}\s*$'
    for match in re.finditer(custom_id_pattern, content, re.MULTILINE):
        custom_id = match.group(1).strip('#')
        anchors.add(custom_id)
    
    return anchors


def find_broken_anchors(content: str, file_path: Path) -> List[Tuple[str, str, str]]:
    """找出所有失效的锚点链接"""
    broken = []
    all_anchors = extract_all_anchors(content)
    
    # 匹配锚点链接
    anchor_link_pattern = r'\[([^\]]+)\]\(#[^)]+\)'
    
    for match in re.finditer(anchor_link_pattern, content):
        full_match = match.group(0)
        link_text = match.group(1)
        
        # 提取锚点
        url_match = re.search(r'\(#[^)]+\)', full_match)
        if not url_match:
            continue
            
        url = url_match.group(0)[2:-1]  # 移除( # )
        anchor = url.split('#')[-1] if '#' in url else url[1:] if url.startswith('#') else url
        
        # 检查锚点是否存在
        if anchor and anchor not in all_anchors:
            # 尝试找到匹配的标题
            broken.append((full_match, link_text, anchor))
    
    return broken


def fix_anchor_link(content: str, broken_link: str, link_text: str, anchor: str, all_anchors: Set[str]) -> str:
    """修复单个锚点链接"""
    # 尝试找到最匹配的锚点
    # 策略1: 忽略大小写和标点，找到相似锚点
    anchor_normalized = anchor.lower().replace('-', '').replace('_', '')
    
    for existing_anchor in all_anchors:
        existing_normalized = existing_anchor.lower().replace('-', '').replace('_', '')
        if anchor_normalized == existing_normalized:
            # 完全匹配（忽略格式）
            new_link = broken_link.replace(f'(#{anchor})', f'(#{existing_anchor})')
            return content.replace(broken_link, new_link, 1)
    
    # 策略2: 查找包含关系的锚点
    for existing_anchor in all_anchors:
        if anchor in existing_anchor or existing_anchor in anchor:
            if abs(len(anchor) - len(existing_anchor)) < 20:  # 长度相近
                new_link = broken_link.replace(f'(#{anchor})', f'(#{existing_anchor})')
                return content.replace(broken_link, new_link, 1)
    
    # 策略3: 生成新的自定义锚点
    # 找到对应的标题并添加自定义锚点
    header_pattern = r'^(#{1,6}\s+.+)$'
    for match in re.finditer(header_pattern, content, re.MULTILINE):
        header_line = match.group(1)
        header_text = re.sub(r'^#{1,6}\s+', '', header_line)
        
        # 如果链接文本与标题相似
        if link_text.lower() in header_text.lower() or header_text.lower() in link_text.lower():
            # 添加自定义锚点
            new_header = f"{header_line} {{#{anchor}}}"
            content = content.replace(header_line, new_header, 1)
            return content
    
    return content


def fix_file(file_path: Path) -> Tuple[int, List[str]]:
    """修复单个文件的所有锚点问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return 0, [f"无法读取: {e}"]
    
    original_content = content
    all_anchors = extract_all_anchors(content)
    broken_links = find_broken_anchors(content, file_path)
    
    if not broken_links:
        return 0, []
    
    fixed_count = 0
    log = []
    
    for broken_link, link_text, anchor in broken_links:
        new_content = fix_anchor_link(content, broken_link, link_text, anchor, all_anchors)
        if new_content != content:
            content = new_content
            fixed_count += 1
            log.append(f"  修复: [{link_text}](#{anchor})")
            # 更新锚点集合
            all_anchors = extract_all_anchors(content)
    
    if fixed_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return fixed_count, log


def main():
    # 需要修复的文件列表
    files_to_fix = [
        "Flink/04-connectors/flink-delta-lake-integration.md",
        "Flink/04-connectors/kafka-integration-patterns.md",
        "Flink/09-language-foundations/01.02-typeinformation-derivation.md",
        "Flink/09-language-foundations/02.02-flink-scala-api-community.md",
        "Flink/09-language-foundations/flink-25-wasm-udf-ga.md",
        "Flink/10-deployment/kubernetes-deployment-production-guide.md",
        "Flink/12-ai-ml/online-learning-algorithms.md",
        "Flink/13-wasm/wasi-0.3-async-preview.md",
        "Knowledge/03-business-patterns/iot-stream-processing.md",
        "Knowledge/03-business-patterns/log-monitoring.md",
        "Knowledge/03-business-patterns/netflix-streaming-pipeline.md",
        "Knowledge/03-business-patterns/real-time-recommendation.md",
        "Knowledge/03-business-patterns/spotify-music-recommendation.md",
        "Knowledge/03-business-patterns/stripe-payment-processing.md",
        "Knowledge/03-business-patterns/uber-realtime-platform.md",
        "Knowledge/04-technology-selection/paradigm-selection-guide.md",
        "Knowledge/05-mapping-guides/theory-to-code-patterns.md",
        "Knowledge/06-frontier/streaming-database-ecosystem-comparison.md",
        "Knowledge/06-frontier/streaming-databases.md",
        "Knowledge/06-frontier/wasm-dataflow-patterns.md",
        "Struct/01-foundation/01.04-dataflow-model-formalization.md",
        "Struct/06-frontier/06.02-choreographic-streaming-programming.md",
        "TROUBLESHOOTING-COMPLETE.md",
        "docs/i18n/en/ARCHITECTURE.md",
    ]
    
    total_fixed = 0
    report = ["# 锚点修复报告", ""]
    
    for file_str in files_to_fix:
        file_path = Path(file_str)
        if not file_path.exists():
            report.append(f"## {file_str}")
            report.append(f"❌ 文件不存在")
            report.append("")
            continue
        
        fixed, log = fix_file(file_path)
        
        report.append(f"## {file_str}")
        if fixed > 0:
            report.append(f"✅ 修复 {fixed} 个问题")
            report.extend(log)
            total_fixed += fixed
        else:
            report.append("ℹ️ 无需修复或修复失败")
        report.append("")
    
    report.append(f"## 总计")
    report.append(f"修复问题数: {total_fixed}")
    
    # 保存报告
    with open("P0-FINAL-FIX-REPORT.md", 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"✅ 修复完成，共修复 {total_fixed} 个问题")
    print(f"📄 报告已保存到 P0-FINAL-FIX-REPORT.md")
    
    return total_fixed


if __name__ == '__main__':
    main()
