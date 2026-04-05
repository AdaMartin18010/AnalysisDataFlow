#!/usr/bin/env python3
"""
quality-score-calculator.py - 文档质量分数计算器

功能：为每篇文档计算质量分数
基于：完整性、时效性、引用数量、结构规范性
"""

import os
import sys
import re
import json
from datetime import datetime, timedelta
from pathlib import Path

# 配置
DAYS_THRESHOLD = 90
SKIP_DIRECTORIES = ['.git', '.improvement-tracking', 'archive', '__pycache__', 
                    'node_modules', '.venv', 'venv']
REPORT_FILE = '../quality-score-report.md'
DETAILED_JSON = '../quality-scores.json'

# 权重配置
WEIGHTS = {
    'completeness': 0.35,    # 完整性
    'freshness': 0.25,       # 时效性
    'references': 0.20,      # 引用数量
    'structure': 0.20        # 结构规范性
}

# 评分标准
SCORE_THRESHOLDS = {
    'excellent': 85,    # 优秀
    'good': 70,         # 良好
    'pass': 50,         # 及格
    'poor': 0           # 差
}


def get_file_age_days(filepath):
    """获取文件最后修改时间（天数）"""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (24 * 3600)
    except:
        return 0


def parse_datetime(date_str):
    """解析日期字符串"""
    formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    return None


def analyze_structure(content):
    """分析文档结构规范性"""
    score = 0
    details = []
    
    # 检查标题层次（最多10分）
    h1_count = len(re.findall(r'^# ', content, re.MULTILINE))
    h2_count = len(re.findall(r'^## ', content, re.MULTILINE))
    h3_count = len(re.findall(r'^### ', content, re.MULTILINE))
    
    if h1_count == 1:
        score += 5
        details.append("✓ 有且仅有一个H1标题")
    elif h1_count == 0:
        details.append("✗ 缺少H1标题")
    else:
        score += 2
        details.append(f"△ 有{h1_count}个H1标题（建议1个）")
    
    if h2_count >= 2:
        score += 3
        details.append(f"✓ 有{h2_count}个H2标题")
    else:
        details.append("△ H2标题较少")
    
    if h3_count > 0:
        score += 2
    
    # 检查六段式结构（最多30分）
    sections = ['概念定义', '属性推导', '关系建立', '论证过程', 
                '形式证明', '实例验证', '可视化', '引用参考']
    section_scores = {
        '概念定义': 5, '属性推导': 4, '关系建立': 3, '论证过程': 4,
        '形式证明': 4, '实例验证': 3, '可视化': 4, '引用参考': 3
    }
    
    for section in sections:
        # 支持中英文标题
        patterns = [
            rf'^## \d+\.\s*{section}',
            rf'^## {section}',
            rf'^## \d+\.\s*{section.replace("定义", "Definitions?")}',
            rf'^## \d+\.\s*{section.replace("引用参考", "References?")}',
        ]
        found = False
        for pattern in patterns:
            if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                found = True
                break
        
        if found:
            score += section_scores.get(section, 2)
            details.append(f"✓ 包含'{section}'章节")
    
    # 检查Mermaid图（最多10分）
    mermaid_count = len(re.findall(r'```mermaid', content))
    if mermaid_count >= 1:
        score += min(mermaid_count * 5, 10)
        details.append(f"✓ 包含{mermaid_count}个Mermaid图")
    else:
        details.append("✗ 缺少Mermaid图")
    
    # 检查表格（最多5分）
    table_count = len(re.findall(r'\|.*\|.*\|', content))
    if table_count >= 3:  # 至少3行表格
        score += 5
        details.append("✓ 包含数据表格")
    
    # 检查代码块（最多5分）
    code_blocks = len(re.findall(r'```[a-zA-Z]*\n', content))
    if code_blocks > 0:
        score += min(code_blocks * 2, 5)
        details.append(f"✓ 包含{code_blocks}个代码块")
    
    return min(score, 50), details  # 结构分最高50


def analyze_completeness(content, filepath):
    """分析文档完整性"""
    score = 0
    details = []
    
    # 字数检查（最多20分）
    text_only = re.sub(r'```[\s\S]*?```', '', content)  # 移除代码块
    text_only = re.sub(r'\[.*?\]\(.*?\)', '', text_only)  # 移除链接
    text_only = re.sub(r'[#*|`\-\n]', '', text_only)  # 移除Markdown标记
    word_count = len(text_only.split())
    
    if word_count >= 2000:
        score += 20
        details.append(f"✓ 内容丰富（{word_count}字）")
    elif word_count >= 1000:
        score += 15
        details.append(f"△ 内容较丰富（{word_count}字）")
    elif word_count >= 500:
        score += 10
        details.append(f"△ 内容一般（{word_count}字）")
    else:
        score += 5
        details.append(f"✗ 内容较少（{word_count}字）")
    
    # 定义/定理数量（最多15分）
    def_count = len(re.findall(r'Def-[A-Z]-\d{2}-\d{2}', content))
    thm_count = len(re.findall(r'Thm-[A-Z]-\d{2}-\d{2}', content))
    lemma_count = len(re.findall(r'Lemma-[A-Z]-\d{2}-\d{2}', content))
    
    formal_count = def_count + thm_count + lemma_count
    if formal_count >= 5:
        score += 15
        details.append(f"✓ 形式化元素丰富（{def_count}定义/{thm_count}定理/{lemma_count}引理）")
    elif formal_count >= 2:
        score += 10
        details.append(f"△ 形式化元素适中（{def_count}定义/{thm_count}定理/{lemma_count}引理）")
    elif formal_count > 0:
        score += 5
        details.append(f"△ 形式化元素较少（{def_count}定义/{thm_count}定理/{lemma_count}引理）")
    else:
        details.append("✗ 缺少形式化元素编号")
    
    # 示例数量（最多10分）
    example_count = len(re.findall(r'## \d+\.\s*实例验证', content, re.MULTILINE))
    example_count += len(re.findall(r'### .*[Ee]xample', content))
    if example_count > 0:
        score += min(example_count * 5, 10)
        details.append(f"✓ 包含{example_count}个示例章节")
    else:
        details.append("△ 缺少示例章节")
    
    # 前置依赖检查（最多5分）
    if re.search(r'前置依赖[:：]', content) or re.search(r'dependencies[:：]', content, re.IGNORECASE):
        score += 5
        details.append("✓ 包含前置依赖说明")
    
    return min(score, 50), details  # 完整性最高50


def analyze_freshness(filepath, content):
    """分析文档时效性"""
    score = 0
    details = []
    
    # 文件修改时间
    try:
        mtime = os.path.getmtime(filepath)
        age_days = (time.time() - mtime) / (24 * 3600)
    except:
        age_days = 0
    
    if age_days <= 30:
        score += 30
        details.append(f"✓ 近期更新（{age_days:.0f}天前）")
    elif age_days <= 90:
        score += 25
        details.append(f"△ 近期更新（{age_days:.0f}天前）")
    elif age_days <= 180:
        score += 15
        details.append(f"△ 更新较久（{age_days:.0f}天前）")
    elif age_days <= 365:
        score += 10
        details.append(f"✗ 更新很久（{age_days:.0f}天前）")
    else:
        score += 5
        details.append(f"✗ 长期未更新（{age_days:.0f}天前）")
    
    # 检查文档内日期
    date_patterns = [
        r'更新日期[:：]\s*(\d{4}-\d{2}-\d{2})',
        r'最后更新[:：]\s*(\d{4}-\d{2}-\d{2})',
        r'\d{4}-\d{2}-\d{2}'  # 通用日期格式
    ]
    
    doc_dates = []
    for pattern in date_patterns:
        matches = re.findall(pattern, content)
        doc_dates.extend(matches)
    
    if doc_dates:
        # 找到最新的日期
        latest_date = max(doc_dates)
        details.append(f"✓ 文档内标注日期: {latest_date}")
    
    # 版本声明（如Flink版本）
    version_match = re.search(r'Flink\s+([0-9]+\.[0-9]+)', content)
    if version_match:
        details.append(f"✓ 指定Flink版本: {version_match.group(1)}")
    
    return min(score, 40), details  # 时效性最高40


def analyze_references(content):
    """分析引用数量和质量"""
    score = 0
    details = []
    
    # 引用标记检查（最多20分）
    ref_markers = re.findall(r'\[\^\d+\]', content)
    unique_refs = set(ref_markers)
    ref_count = len(unique_refs)
    
    if ref_count >= 10:
        score += 20
        details.append(f"✓ 引用丰富（{ref_count}个）")
    elif ref_count >= 5:
        score += 15
        details.append(f"△ 引用适中（{ref_count}个）")
    elif ref_count >= 2:
        score += 10
        details.append(f"△ 引用较少（{ref_count}个）")
    else:
        details.append(f"✗ 引用不足（{ref_count}个）")
    
    # 引用章节检查（最多10分）
    ref_section = re.search(r'## \d+\.\s*引用参考[\s\S]*?(?=^## |\Z)', content, re.MULTILINE)
    if ref_section:
        ref_entries = len(re.findall(r'^\[\^\d+\]:', ref_section.group(), re.MULTILINE))
        if ref_entries >= ref_count * 0.8:  # 引用定义与引用标记匹配
            score += 10
            details.append(f"✓ 引用章节完整（{ref_entries}条定义）")
        else:
            score += 5
            details.append(f"△ 引用章节不完整（{ref_entries}/{ref_count}）")
    else:
        if ref_count > 0:
            details.append("✗ 缺少引用参考章节")
        
    # 外部链接检查（最多10分）
    external_links = re.findall(r'\[.*?\]\((https?://[^)]+)\)', content)
    if len(external_links) >= 5:
        score += 10
        details.append(f"✓ 外部链接丰富（{len(external_links)}个）")
    elif len(external_links) > 0:
        score += 5
        details.append(f"△ 外部链接较少（{len(external_links)}个）")
    else:
        details.append("✗ 缺少外部链接")
    
    return min(score, 40), details  # 引用分最高40


def calculate_quality_score(filepath):
    """计算单篇文档的质量分数"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return None
    
    # 分析各个维度
    structure_score, structure_details = analyze_structure(content)
    completeness_score, completeness_details = analyze_completeness(content, filepath)
    freshness_score, freshness_details = analyze_freshness(filepath, content)
    references_score, references_details = analyze_references(content)
    
    # 计算总分（各项按权重加权）
    total_score = (
        structure_score * WEIGHTS['structure'] * 2 +  # structure_score满分50，需要调整
        completeness_score * WEIGHTS['completeness'] * 2 +  # completeness_score满分50
        freshness_score * WEIGHTS['freshness'] * 2.5 +  # freshness_score满分40
        references_score * WEIGHTS['references'] * 2.5  # references_score满分40
    )
    
    # 归一化到100分制
    total_score = min(round(total_score), 100)
    
    # 确定等级
    if total_score >= SCORE_THRESHOLDS['excellent']:
        grade = 'A'
        status = 'excellent'
    elif total_score >= SCORE_THRESHOLDS['good']:
        grade = 'B'
        status = 'good'
    elif total_score >= SCORE_THRESHOLDS['pass']:
        grade = 'C'
        status = 'pass'
    else:
        grade = 'D'
        status = 'poor'
    
    return {
        'path': filepath,
        'filename': os.path.basename(filepath),
        'scores': {
            'structure': structure_score,
            'completeness': completeness_score,
            'freshness': freshness_score,
            'references': references_score,
            'total': total_score
        },
        'grade': grade,
        'status': status,
        'details': {
            'structure': structure_details,
            'completeness': completeness_details,
            'freshness': freshness_details,
            'references': references_details
        },
        'word_count': len(re.sub(r'[#*|`\-\n]', '', re.sub(r'```[\s\S]*?```', '', content)).split()),
        'def_count': len(re.findall(r'Def-[A-Z]-\d{2}-\d{2}', content)),
        'thm_count': len(re.findall(r'Thm-[A-Z]-\d{2}-\d{2}', content)),
        'ref_count': len(set(re.findall(r'\[\^\d+\]', content)))
    }


def scan_documents(base_dir):
    """扫描所有markdown文档"""
    documents = []
    
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRECTORIES]
        
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                score_info = calculate_quality_score(filepath)
                if score_info:
                    documents.append(score_info)
    
    return documents


def generate_report(documents, base_dir):
    """生成质量报告"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 排序
    documents.sort(key=lambda x: x['scores']['total'], reverse=True)
    
    # 统计
    total_docs = len(documents)
    excellent = len([d for d in documents if d['status'] == 'excellent'])
    good = len([d for d in documents if d['status'] == 'good'])
    passed = len([d for d in documents if d['status'] == 'pass'])
    poor = len([d for d in documents if d['status'] == 'poor'])
    
    avg_score = sum(d['scores']['total'] for d in documents) / max(total_docs, 1)
    
    report = f"""# 文档质量分数报告

> 生成时间: {timestamp}

## 总体统计

| 指标 | 数值 |
|------|------|
| 分析文档总数 | {total_docs} |
| 平均质量分数 | {avg_score:.1f}/100 |
| A级文档（优秀 ≥85分） | {excellent} ({excellent/max(total_docs,1)*100:.1f}%) |
| B级文档（良好 70-84分） | {good} ({good/max(total_docs,1)*100:.1f}%) |
| C级文档（及格 50-69分） | {passed} ({passed/max(total_docs,1)*100:.1f}%) |
| D级文档（不及格 <50分） | {poor} ({poor/max(total_docs,1)*100:.1f}%) |

---

## 质量分布

```
优秀 [{'█' * int(excellent/max(total_docs,1)*20)}{' ' * (20-int(excellent/max(total_docs,1)*20))}] {excellent/max(total_docs,1)*100:.1f}%
良好 [{'█' * int(good/max(total_docs,1)*20)}{' ' * (20-int(good/max(total_docs,1)*20))}] {good/max(total_docs,1)*100:.1f}%
及格 [{'█' * int(passed/max(total_docs,1)*20)}{' ' * (20-int(passed/max(total_docs,1)*20))}] {passed/max(total_docs,1)*100:.1f}%
不及格 [{'█' * int(poor/max(total_docs,1)*20)}{' ' * (20-int(poor/max(total_docs,1)*20))}] {poor/max(total_docs,1)*100:.1f}%
```

---

## 评分维度说明

| 维度 | 权重 | 满分 | 评估要点 |
|------|------|------|----------|
| 完整性 | {WEIGHTS['completeness']*100:.0f}% | 50 | 字数、定义/定理数、示例数 |
| 时效性 | {WEIGHTS['freshness']*100:.0f}% | 40 | 最后修改时间 |
| 引用质量 | {WEIGHTS['references']*100:.0f}% | 40 | 引用标记数、外部链接数 |
| 结构规范 | {WEIGHTS['structure']*100:.0f}% | 50 | 六段式结构、Mermaid图、表格 |

---

## 高分文档（优秀）

| 排名 | 文件名 | 总分 | 完整 | 时效 | 引用 | 结构 | 定义 | 定理 |
|------|--------|------|------|------|------|------|------|------|
"""
    
    top_docs = [d for d in documents if d['status'] == 'excellent'][:20]
    for i, doc in enumerate(top_docs, 1):
        rel_path = os.path.relpath(doc['path'], base_dir)
        s = doc['scores']
        report += f"| {i} | `{doc['filename'][:30]}` | **{s['total']}** | {s['completeness']} | {s['freshness']} | {s['references']} | {s['structure']} | {doc['def_count']} | {doc['thm_count']} |\n"
    
    report += f"""

---

## 需要改进的文档（不及格）

| 排名 | 文件名 | 总分 | 完整 | 时效 | 引用 | 结构 | 主要问题 |
|------|--------|------|------|------|------|------|----------|
"""
    
    poor_docs = [d for d in documents if d['status'] == 'poor'][:20]
    for i, doc in enumerate(poor_docs, 1):
        rel_path = os.path.relpath(doc['path'], base_dir)
        s = doc['scores']
        # 找出最低分项
        min_dim = min([('完整', s['completeness']), ('时效', s['freshness']), 
                       ('引用', s['references']), ('结构', s['structure'])], key=lambda x: x[1])
        report += f"| {i} | `{doc['filename'][:30]}` | **{s['total']}** | {s['completeness']} | {s['freshness']} | {s['references']} | {s['structure']} | {min_dim[0]}不足 |\n"
    
    if not poor_docs:
        report += "| - | - | - | - | - | - | - | 无不及格文档 |\n"
    
    report += f"""

---

## 各目录平均分

"""
    
    # 按目录统计
    dir_scores = {}
    for doc in documents:
        rel_path = os.path.relpath(doc['path'], base_dir)
        top_dir = rel_path.split(os.sep)[0] if os.sep in rel_path else 'root'
        
        if top_dir not in dir_scores:
            dir_scores[top_dir] = []
        dir_scores[top_dir].append(doc['scores']['total'])
    
    report += "| 目录 | 文档数 | 平均分 | 最高分 | 最低分 | 健康度 |\n"
    report += "|------|--------|--------|--------|--------|--------|\n"
    
    for dir_name, scores in sorted(dir_scores.items()):
        avg = sum(scores) / len(scores)
        max_s = max(scores)
        min_s = min(scores)
        health = "✅" if avg >= 70 else "⚠️" if avg >= 50 else "🔴"
        report += f"| {dir_name} | {len(scores)} | {avg:.1f} | {max_s} | {min_s} | {health} |\n"
    
    report += f"""

---

## 改进建议

### 高优先级（D级文档）

针对质量分数低于50分的文档，建议：

1. **补充形式化元素**: 添加定义(Def-)、定理(Thm-)、引理(Lemma-)编号
2. **完善六段式结构**: 确保包含概念定义、属性推导、关系建立、论证过程、实例验证、引用参考
3. **添加可视化**: 至少包含一个Mermaid图表
4. **补充引用**: 添加外部参考链接和引用标记

### 中优先级（C级文档）

1. **增加内容深度**: 扩写字数，添加更多示例
2. **更新时效性**: 更新文档中的版本信息和日期
3. **完善引用**: 补充更多外部参考

### 维护建议

```bash
# 设置质量门禁：禁止提交质量分低于50的文档
# 可以在git pre-commit hook中添加：
python .improvement-tracking/scripts/quality-score-calculator.py
# 检查是否有新的D级文档
```

---

## 详细数据

完整评分数据已保存到: `{DETAILED_JSON}`

可以导入到其他工具进行进一步分析。

"""
    
    return report


def main():
    """主函数"""
    global time
    import time
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(script_dir))
    
    print("=" * 60)
    print("📊 文档质量分数计算器")
    print("=" * 60)
    print(f"扫描目录: {base_dir}")
    print("-" * 60)
    
    # 扫描文档
    print("\n📂 扫描文档中...")
    documents = scan_documents(base_dir)
    print(f"   分析了 {len(documents)} 个 Markdown 文件")
    
    if not documents:
        print("   没有找到可分析的文档")
        return 0
    
    # 统计
    excellent = len([d for d in documents if d['status'] == 'excellent'])
    good = len([d for d in documents if d['status'] == 'good'])
    passed = len([d for d in documents if d['status'] == 'pass'])
    poor = len([d for d in documents if d['status'] == 'poor'])
    avg_score = sum(d['scores']['total'] for d in documents) / len(documents)
    
    print(f"\n📊 质量分布:")
    print(f"   A级(优秀≥85): {excellent} 个")
    print(f"   B级(良好70-84): {good} 个")
    print(f"   C级(及格50-69): {passed} 个")
    print(f"   D级(不及格<50): {poor} 个")
    print(f"   平均分: {avg_score:.1f}")
    
    # 生成报告
    print("\n📝 生成报告...")
    report = generate_report(documents, base_dir)
    
    report_path = os.path.join(script_dir, REPORT_FILE)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"   Markdown报告: {report_path}")
    
    # 保存JSON数据
    json_path = os.path.join(script_dir, DETAILED_JSON)
    # 移除details以减小文件大小
    json_data = [{k: v for k, v in d.items() if k != 'details'} for d in documents]
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"   JSON数据: {json_path}")
    
    # 输出摘要
    print("\n" + "=" * 60)
    print("📋 执行摘要")
    print("=" * 60)
    
    if poor == 0:
        print("✅ 所有文档质量都在及格线以上")
    else:
        print(f"⚠️  发现 {poor} 个质量不及格的文档需要改进")
    
    if excellent > 0:
        print(f"🌟 有 {excellent} 个文档达到优秀水平")
    
    print(f"\n💡 平均分 {avg_score:.1f}，{'高于' if avg_score >= 70 else '低于'}良好标准")
    print("=" * 60)
    
    return poor  # 返回不及格文档数


if __name__ == '__main__':
    sys.exit(main())
