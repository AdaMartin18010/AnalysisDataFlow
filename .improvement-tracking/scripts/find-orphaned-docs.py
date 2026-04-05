#!/usr/bin/env python3
"""
find-orphaned-docs.py - 发现孤儿文档

功能：找出90天未修改且不在核心层的文档，输出建议归档列表
"""

import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# 配置
DAYS_THRESHOLD = 90
CORE_DIRECTORIES = ['Struct', 'Knowledge', 'Flink']  # 核心层目录
SKIP_DIRECTORIES = ['.git', '.improvement-tracking', 'archive', '__pycache__', 'node_modules', '.venv', 'venv']
REPORT_FILE = '../orphaned-docs-report.md'


def get_file_age_days(filepath):
    """获取文件最后修改时间（天数）"""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (24 * 3600)
    except OSError:
        return 0


def get_file_mtime_str(filepath):
    """获取文件最后修改时间字符串"""
    try:
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    except OSError:
        return 'Unknown'


def should_check_file(filepath):
    """判断是否应该检查此文件"""
    filename = os.path.basename(filepath)
    
    # 只检查markdown文件
    if not filename.endswith('.md'):
        return False
    
    # 跳过特定文件
    skip_files = ['README.md', 'README-EN.md', 'AGENTS.md', 'CHANGELOG.md', 
                  'ROADMAP.md', 'PROJECT-TRACKING.md', 'LICENSE', '.gitignore']
    if filename in skip_files:
        return False
    
    return True


def is_in_core_layer(filepath):
    """检查文件是否在核心层目录中"""
    path_parts = Path(filepath).parts
    for core_dir in CORE_DIRECTORIES:
        if core_dir in path_parts:
            return True
    return False


def analyze_document(filepath):
    """分析单个文档"""
    age_days = get_file_age_days(filepath)
    is_core = is_in_core_layer(filepath)
    
    return {
        'path': filepath,
        'filename': os.path.basename(filepath),
        'age_days': age_days,
        'last_modified': get_file_mtime_str(filepath),
        'is_core': is_core,
        'is_orphaned': age_days > DAYS_THRESHOLD and not is_core
    }


def scan_directory(base_dir):
    """扫描目录中的所有markdown文件"""
    documents = []
    
    for root, dirs, files in os.walk(base_dir):
        # 跳过指定目录
        dirs[:] = [d for d in dirs if d not in SKIP_DIRECTORIES]
        
        for filename in files:
            filepath = os.path.join(root, filename)
            if should_check_file(filepath):
                doc_info = analyze_document(filepath)
                documents.append(doc_info)
    
    return documents


def categorize_documents(documents):
    """对文档进行分类"""
    orphaned = [d for d in documents if d['is_orphaned']]
    stale_core = [d for d in documents if d['age_days'] > DAYS_THRESHOLD and d['is_core']]
    recent = [d for d in documents if d['age_days'] <= DAYS_THRESHOLD]
    
    # 按年龄排序
    orphaned.sort(key=lambda x: x['age_days'], reverse=True)
    stale_core.sort(key=lambda x: x['age_days'], reverse=True)
    
    return {
        'orphaned': orphaned,
        'stale_core': stale_core,
        'recent': recent
    }


def generate_report(categorized, base_dir):
    """生成报告"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = f"""# 孤儿文档分析报告

> 生成时间: {timestamp}  
> 分析目录: `{base_dir}`  
> 时间阈值: {DAYS_THRESHOLD}天未修改

## 摘要

| 类别 | 数量 | 占比 |
|------|------|------|
| 🗑️ 建议归档（非核心层+超期） | {len(categorized['orphaned'])} | {len(categorized['orphaned'])/max(len(categorized['orphaned'])+len(categorized['stale_core'])+len(categorized['recent']),1)*100:.1f}% |
| ⚠️ 核心层需关注 | {len(categorized['stale_core'])} | {len(categorized['stale_core'])/max(len(categorized['orphaned'])+len(categorized['stale_core'])+len(categorized['recent']),1)*100:.1f}% |
| ✅ 近期活跃 | {len(categorized['recent'])} | {len(categorized['recent'])/max(len(categorized['orphaned'])+len(categorized['stale_core'])+len(categorized['recent']),1)*100:.1f}% |

---

## 1. 建议归档的文档

以下文档**超过{DAYS_THRESHOLD}天未修改**且**不在核心层**，建议归档处理：

| 序号 | 文件路径 | 最后修改 | 闲置天数 |
|------|----------|----------|----------|
"""
    
    for i, doc in enumerate(categorized['orphaned'], 1):
        rel_path = os.path.relpath(doc['path'], base_dir)
        report += f"| {i} | `{rel_path}` | {doc['last_modified']} | {doc['age_days']:.0f}天 |\n"
    
    if not categorized['orphaned']:
        report += "\n*未发现需要归档的文档*\n"
    
    report += f"""

### 建议操作

```bash
# 创建归档目录
mkdir -p archive/$(date +%Y-%m)

# 移动孤儿文档（请根据实际情况调整路径）
"""
    
    for doc in categorized['orphaned'][:5]:  # 只显示前5个作为示例
        rel_path = os.path.relpath(doc['path'], base_dir)
        report += f"# mv {rel_path} archive/$(date +%Y-%m)/\n"
    
    if len(categorized['orphaned']) > 5:
        report += f"# ... 还有 {len(categorized['orphaned']) - 5} 个文件\n"
    
    report += f"""```

---

## 2. 核心层需关注的文档

以下**核心层文档**超过{DAYS_THRESHOLD}天未修改，建议安排更新：

| 序号 | 文件路径 | 最后修改 | 闲置天数 |
|------|----------|----------|----------|
"""
    
    for i, doc in enumerate(categorized['stale_core'][:20], 1):  # 只显示前20个
        rel_path = os.path.relpath(doc['path'], base_dir)
        report += f"| {i} | `{rel_path}` | {doc['last_modified']} | {doc['age_days']:.0f}天 |\n"
    
    if len(categorized['stale_core']) > 20:
        report += f"\n*... 还有 {len(categorized['stale_core']) - 20} 个文档*\n"
    
    if not categorized['stale_core']:
        report += "\n*所有核心层文档都在维护周期内*\n"
    
    report += f"""

---

## 3. 目录活跃度分布

"""
    
    # 按目录统计
    dir_stats = {}
    for doc in categorized['orphaned'] + categorized['stale_core'] + categorized['recent']:
        rel_path = os.path.relpath(doc['path'], base_dir)
        top_dir = rel_path.split(os.sep)[0] if os.sep in rel_path else 'root'
        
        if top_dir not in dir_stats:
            dir_stats[top_dir] = {'total': 0, 'orphaned': 0, 'stale': 0}
        dir_stats[top_dir]['total'] += 1
        if doc['is_orphaned']:
            dir_stats[top_dir]['orphaned'] += 1
        elif doc['age_days'] > DAYS_THRESHOLD:
            dir_stats[top_dir]['stale'] += 1
    
    report += "| 目录 | 总文档数 | 建议归档 | 需关注 | 健康度 |\n"
    report += "|------|----------|----------|--------|--------|\n"
    
    for dir_name, stats in sorted(dir_stats.items()):
        health = "✅" if stats['orphaned'] == 0 and stats['stale'] == 0 else "⚠️" if stats['orphaned'] == 0 else "🗑️"
        report += f"| {dir_name} | {stats['total']} | {stats['orphaned']} | {stats['stale']} | {health} |\n"
    
    report += """

---

## 4. 自动化建议

可以设置定时任务定期执行此脚本：

```bash
# 添加到 crontab（每月1日执行）
0 0 1 * * cd /path/to/project && python .improvement-tracking/scripts/find-orphaned-docs.py
```

"""
    
    return report


def main():
    """主函数"""
    # 确定项目根目录（脚本所在位置的父级的父级）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(script_dir))
    
    print("=" * 60)
    print("🔍 孤儿文档分析工具")
    print("=" * 60)
    print(f"扫描目录: {base_dir}")
    print(f"时间阈值: {DAYS_THRESHOLD}天")
    print("-" * 60)
    
    # 扫描文档
    print("\n📂 扫描文档中...")
    documents = scan_directory(base_dir)
    print(f"   找到 {len(documents)} 个 Markdown 文件")
    
    # 分类
    print("\n📊 分析文档状态...")
    categorized = categorize_documents(documents)
    
    orphaned_count = len(categorized['orphaned'])
    stale_core_count = len(categorized['stale_core'])
    
    print(f"   🗑️  建议归档: {orphaned_count} 个")
    print(f"   ⚠️  核心层需关注: {stale_core_count} 个")
    print(f"   ✅ 近期活跃: {len(categorized['recent'])} 个")
    
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
    if orphaned_count > 0:
        print(f"⚠️  发现 {orphaned_count} 个文档建议归档")
        print("   查看详细报告了解详情")
    else:
        print("✅ 没有发现需要归档的孤儿文档")
    
    if stale_core_count > 0:
        print(f"⚠️  发现 {stale_core_count} 个核心层文档需要关注")
    else:
        print("✅ 所有核心层文档都在维护周期内")
    
    print("\n💡 提示: 归档前请确认文档内容是否还有参考价值")
    print("=" * 60)
    
    return orphaned_count


if __name__ == '__main__':
    sys.exit(main())
