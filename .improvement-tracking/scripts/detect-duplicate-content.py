#!/usr/bin/env python3
"""
detect-duplicate-content.py - 重复内容检测

功能：检测内容重复或高度相似的文档，使用文本相似度算法
使用Jaccard相似度，纯Python标准库实现
"""

import os
import sys
import re
import hashlib
from collections import defaultdict
from datetime import datetime

# 配置
SIMILARITY_THRESHOLD = 0.7  # 相似度阈值（70%以上视为重复）
PARTIAL_THRESHOLD = 0.4     # 部分相似阈值（40%以上需要关注）
SKIP_DIRECTORIES = ['.git', '.improvement-tracking', 'archive', '__pycache__', 
                    'node_modules', '.venv', 'venv']
REPORT_FILE = '../duplicate-content-report.md'


def normalize_text(text):
    """标准化文本：去除代码块、链接、标点，转为小写"""
    # 移除代码块
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`[^`]*`', '', text)
    
    # 移除Markdown链接
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    
    # 移除URL
    text = re.sub(r'https?://\S+', '', text)
    
    # 移除标点符号和数字
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', '', text)
    
    # 转为小写，去除多余空格
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def get_shingles(text, k=5):
    """将文本切分为k-gram（shingles）"""
    words = text.split()
    if len(words) < k:
        return set(words)
    return set(tuple(words[i:i+k]) for i in range(len(words) - k + 1))


def jaccard_similarity(set1, set2):
    """计算Jaccard相似度"""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0


def get_file_hash(filepath):
    """获取文件内容哈希"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            return hashlib.md5(content.encode()).hexdigest()
    except:
        return None


def extract_sections(text):
    """提取文档章节结构"""
    sections = []
    lines = text.split('\n')
    current_section = []
    
    for line in lines:
        if line.startswith('#'):
            if current_section:
                sections.append('\n'.join(current_section))
                current_section = []
        current_section.append(line)
    
    if current_section:
        sections.append('\n'.join(current_section))
    
    return sections


def analyze_file(filepath):
    """分析单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return None
    
    normalized = normalize_text(content)
    shingles = get_shingles(normalized)
    sections = extract_sections(content)
    
    # 提取标题
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.basename(filepath)
    
    # 提取定义数量
    def_count = len(re.findall(r'Def-[A-Z]-\d{2}-\d{2}', content))
    thm_count = len(re.findall(r'Thm-[A-Z]-\d{2}-\d{2}', content))
    
    return {
        'path': filepath,
        'filename': os.path.basename(filepath),
        'title': title,
        'content': content,
        'normalized': normalized,
        'shingles': shingles,
        'word_count': len(normalized.split()),
        'sections': sections,
        'section_count': len(sections),
        'def_count': def_count,
        'thm_count': thm_count,
        'hash': get_file_hash(filepath)
    }


def scan_documents(base_dir):
    """扫描所有markdown文档"""
    documents = []
    
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRECTORIES]
        
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                doc_info = analyze_file(filepath)
                if doc_info and doc_info['word_count'] > 50:  # 忽略太短的文件
                    documents.append(doc_info)
    
    return documents


def find_exact_duplicates(documents):
    """查找完全相同的文件"""
    hash_groups = defaultdict(list)
    
    for doc in documents:
        hash_groups[doc['hash']].append(doc)
    
    duplicates = []
    for file_hash, docs in hash_groups.items():
        if len(docs) > 1:
            duplicates.append({
                'type': 'exact',
                'hash': file_hash,
                'documents': docs
            })
    
    return duplicates


def find_similar_documents(documents, threshold=SIMILARITY_THRESHOLD):
    """查找相似文档"""
    similar_pairs = []
    n = len(documents)
    
    print(f"\n   正在比较 {n} 个文档的相似度...")
    
    for i in range(n):
        for j in range(i + 1, n):
            doc1, doc2 = documents[i], documents[j]
            
            # 跳过字数差异过大的
            ratio = doc1['word_count'] / max(doc2['word_count'], 1)
            if ratio < 0.5 or ratio > 2.0:
                continue
            
            similarity = jaccard_similarity(doc1['shingles'], doc2['shingles'])
            
            if similarity >= threshold:
                similar_pairs.append({
                    'type': 'similar',
                    'doc1': doc1,
                    'doc2': doc2,
                    'similarity': similarity
                })
        
        if (i + 1) % 50 == 0 or i == n - 1:
            print(f"   进度: {i + 1}/{n} ({(i+1)/n*100:.1f}%)")
    
    # 按相似度排序
    similar_pairs.sort(key=lambda x: x['similarity'], reverse=True)
    return similar_pairs


def find_title_duplicates(documents):
    """查找标题重复"""
    title_groups = defaultdict(list)
    
    for doc in documents:
        # 标准化标题进行比较
        title_key = doc['title'].lower().strip()
        title_key = re.sub(r'[^\w]', '', title_key)
        title_groups[title_key].append(doc)
    
    duplicates = []
    for title, docs in title_groups.items():
        if len(docs) > 1 and len(title) > 5:  # 标题长度大于5才考虑
            duplicates.append({
                'type': 'title_duplicate',
                'title': docs[0]['title'],
                'documents': docs
            })
    
    return duplicates


def categorize_duplicates(exact_dups, similar_pairs, title_dups):
    """分类整理重复内容"""
    # 按相似度分组
    high_similarity = [p for p in similar_pairs if p['similarity'] >= 0.8]
    medium_similarity = [p for p in similar_pairs if 0.6 <= p['similarity'] < 0.8]
    low_similarity = [p for p in similar_pairs if PARTIAL_THRESHOLD <= p['similarity'] < 0.6]
    
    return {
        'exact': exact_dups,
        'high_similarity': high_similarity,
        'medium_similarity': medium_similarity,
        'low_similarity': low_similarity,
        'title_duplicate': title_dups
    }


def generate_report(categorized, base_dir):
    """生成报告"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    total_issues = (len(categorized['exact']) + 
                   len(categorized['high_similarity']) + 
                   len(categorized['medium_similarity']) +
                   len(categorized['low_similarity']) +
                   len(categorized['title_duplicate']))
    
    report = f"""# 重复内容检测报告

> 生成时间: {timestamp}  
> 相似度阈值: {SIMILARITY_THRESHOLD*100:.0f}%

## 摘要

| 类别 | 数量 | 严重程度 |
|------|------|----------|
| 🚨 完全相同 | {len(categorized['exact'])} | 高 |
| 🔴 高度相似 (≥80%) | {len(categorized['high_similarity'])} | 高 |
| 🟡 中度相似 (60-80%) | {len(categorized['medium_similarity'])} | 中 |
| 🟢 部分相似 (40-60%) | {len(categorized['low_similarity'])} | 低 |
| 📝 标题重复 | {len(categorized['title_duplicate'])} | 中 |
| **总计** | **{total_issues}** | - |

---

## 1. 完全相同的文档

以下文件内容完全相同，建议保留一个，删除或归档其他副本：

"""
    
    for i, group in enumerate(categorized['exact'], 1):
        report += f"### 1.{i} 哈希: {group['hash'][:8]}...\n\n"
        report += "| 文件路径 | 大小 |\n"
        report += "|----------|------|\n"
        for doc in group['documents']:
            rel_path = os.path.relpath(doc['path'], base_dir)
            size = os.path.getsize(doc['path'])
            report += f"| `{rel_path}` | {size} bytes |\n"
        report += "\n**建议操作**: 保留最新版本，归档或删除其他副本\n\n"
    
    if not categorized['exact']:
        report += "✅ 未发现完全相同的文档\n\n"
    
    report += """---

## 2. 高度相似的文档 (≥80%)

以下内容高度相似，可能是重复内容或应该合并：

"""
    
    for i, pair in enumerate(categorized['high_similarity'], 1):
        doc1, doc2 = pair['doc1'], pair['doc2']
        rel_path1 = os.path.relpath(doc1['path'], base_dir)
        rel_path2 = os.path.relpath(doc2['path'], base_dir)
        
        report += f"### 2.{i} 相似度: {pair['similarity']*100:.1f}%\n\n"
        report += f"- **文档A**: `{rel_path1}`\n"
        report += f"  - 标题: {doc1['title'][:60]}...\n"
        report += f"  - 字数: {doc1['word_count']}\n"
        report += f"  - 定义数: {doc1['def_count']}, 定理数: {doc1['thm_count']}\n\n"
        report += f"- **文档B**: `{rel_path2}`\n"
        report += f"  - 标题: {doc2['title'][:60]}...\n"
        report += f"  - 字数: {doc2['word_count']}\n"
        report += f"  - 定义数: {doc2['def_count']}, 定理数: {doc2['thm_count']}\n\n"
        
        report += "**建议操作**: 检查是否可以合并为一篇文档\n\n"
    
    if not categorized['high_similarity']:
        report += "✅ 未发现高度相似的文档\n\n"
    
    report += """---

## 3. 中度相似的文档 (60-80%)

以下内容中度相似，可能包含重复章节：

| 相似度 | 文档A | 文档B |
|--------|-------|-------|
"""
    
    for pair in categorized['medium_similarity'][:20]:  # 只显示前20个
        doc1, doc2 = pair['doc1'], pair['doc2']
        rel_path1 = os.path.relpath(doc1['path'], base_dir)
        rel_path2 = os.path.relpath(doc2['path'], base_dir)
        report += f"| {pair['similarity']*100:.1f}% | `{rel_path1}` | `{rel_path2}` |\n"
    
    if len(categorized['medium_similarity']) > 20:
        report += f"\n*... 还有 {len(categorized['medium_similarity']) - 20} 对文档*\n"
    
    if not categorized['medium_similarity']:
        report += "✅ 未发现中度相似的文档\n"
    
    report += """

---

## 4. 标题重复的文档

以下文档标题相同或非常相似：

"""
    
    for i, group in enumerate(categorized['title_duplicate'], 1):
        report += f"### 4.{i} 标题: {group['title']}\n\n"
        for doc in group['documents']:
            rel_path = os.path.relpath(doc['path'], base_dir)
            report += f"- `{rel_path}`\n"
        report += "\n"
    
    if not categorized['title_duplicate']:
        report += "✅ 未发现标题重复的文档\n"
    
    report += """---

## 5. 建议的合并策略

### 5.1 短期行动

1. **处理完全重复的文档**: 立即删除或归档
2. **处理标题重复**: 重命名以区分内容
3. **审查高度相似文档**: 决定是否合并

### 5.2 长期改进

1. **建立文档模板**: 减少重复内容产生
2. **内容引用机制**: 使用链接代替复制
3. **定期检测**: 每月运行此脚本

### 5.3 合并脚本示例

```bash
# 示例：合并两个高度相似的文档
cat doc1.md > merged.md
echo "" >> merged.md
echo "<!-- 以下内容来自 doc2.md -->" >> merged.md
cat doc2.md >> merged.md
```

"""
    
    return report


def main():
    """主函数"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(script_dir))
    
    print("=" * 60)
    print("🔍 重复内容检测工具")
    print("=" * 60)
    print(f"扫描目录: {base_dir}")
    print(f"相似度阈值: {SIMILARITY_THRESHOLD*100:.0f}%")
    print("-" * 60)
    
    # 扫描文档
    print("\n📂 扫描文档中...")
    documents = scan_documents(base_dir)
    print(f"   找到 {len(documents)} 个有效 Markdown 文件")
    
    if len(documents) < 2:
        print("   文档数量不足，无法检测相似性")
        return 0
    
    # 查找完全重复
    print("\n🔄 检查完全重复...")
    exact_dups = find_exact_duplicates(documents)
    print(f"   发现 {len(exact_dups)} 组完全重复的文档")
    
    # 查找相似文档
    print("\n📊 计算文档相似度...")
    similar_pairs = find_similar_documents(documents)
    print(f"   发现 {len(similar_pairs)} 对相似文档")
    
    # 查找标题重复
    print("\n📝 检查标题重复...")
    title_dups = find_title_duplicates(documents)
    print(f"   发现 {len(title_dups)} 组标题重复")
    
    # 分类整理
    categorized = categorize_duplicates(exact_dups, similar_pairs, title_dups)
    
    # 生成报告
    print("\n📝 生成报告...")
    report = generate_report(categorized, base_dir)
    
    report_path = os.path.join(script_dir, REPORT_FILE)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"   报告已保存: {report_path}")
    
    # 输出摘要
    print("\n" + "=" * 60)
    print("📋 执行摘要")
    print("=" * 60)
    
    total_issues = (len(exact_dups) + len(similar_pairs) + len(title_dups))
    
    if total_issues == 0:
        print("✅ 未发现重复或相似内容")
    else:
        print(f"⚠️  发现 {total_issues} 个问题:")
        if exact_dups:
            print(f"   - 完全重复: {len(exact_dups)} 组")
        if similar_pairs:
            high = len(categorized['high_similarity'])
            med = len(categorized['medium_similarity'])
            low = len(categorized['low_similarity'])
            print(f"   - 内容相似: {high} 高 / {med} 中 / {low} 低")
        if title_dups:
            print(f"   - 标题重复: {len(title_dups)} 组")
    
    print("\n💡 提示: 建议优先处理完全重复和高度相似的内容")
    print("=" * 60)
    
    return total_issues


if __name__ == '__main__':
    sys.exit(main())
