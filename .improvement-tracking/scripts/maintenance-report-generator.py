#!/usr/bin/env python3
"""
maintenance-report-generator.py - 维护报告生成器

功能：生成综合维护报告
统计：待更新文档、待归档文档、质量分布、总体健康度
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

# 配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
REPORT_FILE = '../B2-maintenance-report.md'


def run_script(script_name):
    """运行其他脚本并返回结果摘要"""
    script_path = os.path.join(SCRIPT_DIR, script_name)
    
    if not os.path.exists(script_path):
        return {'error': f'脚本不存在: {script_name}'}
    
    try:
        # 运行脚本并捕获输出
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=300,  # 5分钟超时
            cwd=BASE_DIR
        )
        
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    except subprocess.TimeoutExpired:
        return {'error': '脚本执行超时'}
    except Exception as e:
        return {'error': str(e)}


def parse_script_output(output, script_type):
    """解析脚本输出，提取关键数据"""
    data = {}
    lines = output.split('\n')
    
    if script_type == 'orphaned':
        for line in lines:
            if '建议归档:' in line:
                try:
                    data['orphaned_count'] = int(re.search(r'(\d+)', line).group(1))
                except:
                    pass
            if '核心层需关注:' in line:
                try:
                    data['stale_core_count'] = int(re.search(r'(\d+)', line).group(1))
                except:
                    pass
    
    elif script_type == 'duplicate':
        for line in lines:
            if '完全重复:' in line:
                try:
                    data['exact_dups'] = int(re.search(r'(\d+)', line).group(1))
                except:
                    pass
            if '内容相似:' in line:
                try:
                    match = re.search(r'(\d+)\s*高', line)
                    if match:
                        data['high_similarity'] = int(match.group(1))
                except:
                    pass
    
    elif script_type == 'outdated':
        for line in lines:
            if '严重过时:' in line:
                try:
                    data['outdated_count'] = int(re.search(r'(\d+)', line).group(1))
                except:
                    pass
            if '需要关注:' in line:
                try:
                    data['warning_count'] = int(re.search(r'(\d+)', line).group(1))
                except:
                    pass
    
    elif script_type == 'quality':
        for line in lines:
            if 'D级(不及格' in line:
                try:
                    data['poor_count'] = int(re.search(r'(\d+)', line).group(1))
                except:
                    pass
            if '平均分:' in line:
                try:
                    data['avg_score'] = float(re.search(r'(\d+\.?\d*)', line).group(1))
                except:
                    pass
    
    return data


def count_documents():
    """统计文档数量"""
    counts = {
        'total_md': 0,
        'struct': 0,
        'knowledge': 0,
        'flink': 0,
        'root': 0
    }
    
    for root, dirs, files in os.walk(BASE_DIR):
        # 跳过特定目录
        dirs[:] = [d for d in dirs if d not in ['.git', '.improvement-tracking', 'archive', '__pycache__']]
        
        for filename in files:
            if filename.endswith('.md'):
                counts['total_md'] += 1
                
                rel_path = os.path.relpath(os.path.join(root, filename), BASE_DIR)
                parts = rel_path.split(os.sep)
                
                if len(parts) > 0:
                    top_dir = parts[0]
                    if top_dir == 'Struct':
                        counts['struct'] += 1
                    elif top_dir == 'Knowledge':
                        counts['knowledge'] += 1
                    elif top_dir == 'Flink':
                        counts['flink'] += 1
                    else:
                        counts['root'] += 1
    
    return counts


def count_formal_elements():
    """统计形式化元素数量"""
    elements = {
        'definitions': 0,
        'theorems': 0,
        'lemmas': 0,
        'propositions': 0,
        'corollaries': 0
    }
    
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in ['.git', '.improvement-tracking', 'archive', '__pycache__']]
        
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    elements['definitions'] += len(re.findall(r'Def-[A-Z]-\d{2}-\d{2}', content))
                    elements['theorems'] += len(re.findall(r'Thm-[A-Z]-\d{2}-\d{2}', content))
                    elements['lemmas'] += len(re.findall(r'Lemma-[A-Z]-\d{2}-\d{2}', content))
                    elements['propositions'] += len(re.findall(r'Prop-[A-Z]-\d{2}-\d{2}', content))
                    elements['corollaries'] += len(re.findall(r'Cor-[A-Z]-\d{2}-\d{2}', content))
                except:
                    pass
    
    return elements


def calculate_health_score(data):
    """计算整体健康分数"""
    score = 100
    
    # 根据问题数量扣分
    orphaned = data.get('orphaned', {}).get('orphaned_count', 0)
    outdated = data.get('outdated', {}).get('outdated_count', 0)
    poor_quality = data.get('quality', {}).get('poor_count', 0)
    duplicates = data.get('duplicate', {}).get('exact_dups', 0)
    
    # 扣分规则
    score -= min(orphaned * 2, 20)  # 每个孤儿文档扣2分，最多20分
    score -= min(outdated * 3, 30)  # 每个过时版本扣3分，最多30分
    score -= min(poor_quality * 2, 20)  # 每个低质量文档扣2分，最多20分
    score -= min(duplicates * 5, 15)  # 每组重复扣5分，最多15分
    
    return max(score, 0)


def generate_maintenance_report(data, doc_counts, formal_elements, timestamp):
    """生成综合维护报告"""
    
    health_score = calculate_health_score(data)
    
    # 健康度等级
    if health_score >= 80:
        health_grade = 'A'
        health_status = '🟢 优秀'
    elif health_score >= 60:
        health_grade = 'B'
        health_status = '🟡 良好'
    elif health_score >= 40:
        health_grade = 'C'
        health_status = '🟠 一般'
    else:
        health_grade = 'D'
        health_status = '🔴 需改进'
    
    report = f"""# B2 维护减负报告

> 报告生成时间: {timestamp}  
> 项目名称: AnalysisDataFlow  
> 健康度评分: {health_score}/100 ({health_grade}级 - {health_status})

---

## 执行摘要

本报告通过自动化脚本对项目文档库进行全面健康检查，识别需要维护的文档并提供改进建议。

### 整体健康度

```
健康度: {health_score}/100
[{('=' * int(health_score/5))}{(' ' * (20-int(health_score/5)))}] {health_status}
```

---

## 1. 文档资产统计

### 1.1 文档数量分布

| 目录 | 文档数量 | 占比 |
|------|----------|------|
| Struct/ (形式理论) | {doc_counts['struct']} | {doc_counts['struct']/max(doc_counts['total_md'],1)*100:.1f}% |
| Knowledge/ (知识结构) | {doc_counts['knowledge']} | {doc_counts['knowledge']/max(doc_counts['total_md'],1)*100:.1f}% |
| Flink/ (Flink专项) | {doc_counts['flink']} | {doc_counts['flink']/max(doc_counts['total_md'],1)*100:.1f}% |
| 根目录/其他 | {doc_counts['root']} | {doc_counts['root']/max(doc_counts['total_md'],1)*100:.1f}% |
| **总计** | **{doc_counts['total_md']}** | **100%** |

### 1.2 形式化元素统计

| 元素类型 | 数量 | 备注 |
|----------|------|------|
| 定义 (Def-*) | {formal_elements['definitions']} | 形式化定义 |
| 定理 (Thm-*) | {formal_elements['theorems']} | 形式化定理 |
| 引理 (Lemma-*) | {formal_elements['lemmas']} | 辅助引理 |
| 命题 (Prop-*) | {formal_elements['propositions']} | 重要命题 |
| 推论 (Cor-*) | {formal_elements['corollaries']} | 定理推论 |
| **总计** | **{sum(formal_elements.values())}** | - |

---

## 2. 维护问题汇总

### 2.1 孤儿文档

| 指标 | 数量 | 状态 |
|------|------|------|
| 建议归档（90天未修改+非核心层） | {data.get('orphaned', {}).get('orphaned_count', 'N/A')} | {'🔴 需要处理' if data.get('orphaned', {}).get('orphaned_count', 0) > 0 else '✅ 正常'} |
| 核心层需关注 | {data.get('orphaned', {}).get('stale_core_count', 'N/A')} | {'🟡 建议更新' if data.get('orphaned', {}).get('stale_core_count', 0) > 0 else '✅ 正常'} |

**详细报告**: [orphaned-docs-report.md](./orphaned-docs-report.md)

### 2.2 重复内容

| 指标 | 数量 | 状态 |
|------|------|------|
| 完全重复文档组 | {data.get('duplicate', {}).get('exact_dups', 'N/A')} | {'🔴 需要处理' if data.get('duplicate', {}).get('exact_dups', 0) > 0 else '✅ 正常'} |
| 高度相似内容 | {data.get('duplicate', {}).get('high_similarity', 'N/A')} | {'🟡 建议合并' if data.get('duplicate', {}).get('high_similarity', 0) > 0 else '✅ 正常'} |

**详细报告**: [duplicate-content-report.md](./duplicate-content-report.md)

### 2.3 版本过时

| 指标 | 数量 | 状态 |
|------|------|------|
| 严重过时的技术版本 | {data.get('outdated', {}).get('outdated_count', 'N/A')} | {'🔴 需要更新' if data.get('outdated', {}).get('outdated_count', 0) > 0 else '✅ 正常'} |
| 需要关注的技术版本 | {data.get('outdated', {}).get('warning_count', 'N/A')} | {'🟡 建议规划' if data.get('outdated', {}).get('warning_count', 0) > 0 else '✅ 正常'} |

**详细报告**: [outdated-tech-report.md](./outdated-tech-report.md)

### 2.4 质量分布

| 等级 | 数量 | 标准 |
|------|------|------|
| A级 (优秀 ≥85分) | {data.get('quality', {}).get('excellent_count', 'N/A')} | 质量优秀 |
| B级 (良好 70-84分) | {data.get('quality', {}).get('good_count', 'N/A')} | 质量良好 |
| C级 (及格 50-69分) | {data.get('quality', {}).get('pass_count', 'N/A')} | 需要改进 |
| D级 (不及格 <50分) | {data.get('quality', {}).get('poor_count', 'N/A')} | 急需改进 |
| **平均分** | **{data.get('quality', {}).get('avg_score', 'N/A'):.1f}** | - |

**详细报告**: [quality-score-report.md](./quality-score-report.md)

---

## 3. 问题热力图

```
维护问题热力图 (数量越多颜色越深)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

孤儿文档    [{'█' * min(data.get('orphaned', {}).get('orphaned_count', 0), 20)}{'░' * (20-min(data.get('orphaned', {}).get('orphaned_count', 0), 20))}] {data.get('orphaned', {}).get('orphaned_count', 0)}
版本过时    [{'█' * min(data.get('outdated', {}).get('outdated_count', 0), 20)}{'░' * (20-min(data.get('outdated', {}).get('outdated_count', 0), 20))}] {data.get('outdated', {}).get('outdated_count', 0)}
质量不及格  [{'█' * min(data.get('quality', {}).get('poor_count', 0), 20)}{'░' * (20-min(data.get('quality', {}).get('poor_count', 0), 20))}] {data.get('quality', {}).get('poor_count', 0)}
完全重复    [{'█' * min(data.get('duplicate', {}).get('exact_dups', 0), 20)}{'░' * (20-min(data.get('duplicate', {}).get('exact_dups', 0), 20))}] {data.get('duplicate', {}).get('exact_dups', 0)}

图例: ████ 严重问题  ░░░░ 轻微问题  .... 无问题
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 4. 维护行动清单

### 4.1 立即行动 (本周)

- [ ] 审查并归档 {data.get('orphaned', {}).get('orphaned_count', 0)} 个孤儿文档
- [ ] 处理 {data.get('duplicate', {}).get('exact_dups', 0)} 组完全重复的内容
- [ ] 更新 {data.get('outdated', {}).get('outdated_count', 0)} 处严重过时的技术版本

### 4.2 短期规划 (本月)

- [ ] 改进 {data.get('quality', {}).get('poor_count', 0)} 个质量不及格的文档
- [ ] 更新 {data.get('orphaned', {}).get('stale_core_count', 0)} 个核心层文档
- [ ] 审查并合并 {data.get('duplicate', {}).get('high_similarity', 0)} 对高度相似的内容

### 4.3 中期规划 (本季度)

- [ ] 建立文档更新SOP（标准操作流程）
- [ ] 设置自动化质量门禁
- [ ] 完善文档模板，减少重复内容产生
- [ ] 建立定期维护机制

---

## 5. 自动化脚本使用指南

所有脚本位于 `.improvement-tracking/scripts/` 目录下：

### 5.1 单独运行脚本

```bash
# 1. 发现孤儿文档
python .improvement-tracking/scripts/find-orphaned-docs.py

# 2. 检测重复内容
python .improvement-tracking/scripts/detect-duplicate-content.py

# 3. 检查过时版本
python .improvement-tracking/scripts/outdated-tech-check.py

# 4. 计算质量分数
python .improvement-tracking/scripts/quality-score-calculator.py

# 5. 生成综合报告（运行所有脚本并汇总）
python .improvement-tracking/scripts/maintenance-report-generator.py
```

### 5.2 设置定时任务

```bash
# 每月1日运行完整检查（Linux/Mac）
0 0 1 * * cd /path/to/project && python .improvement-tracking/scripts/maintenance-report-generator.py

# Windows任务计划程序
# 每月执行: python .improvement-tracking\scripts\maintenance-report-generator.py
```

### 5.3 集成到Git工作流

```bash
# 在 .git/hooks/pre-commit 中添加:
#!/bin/bash
echo "运行文档质量检查..."
python .improvement-tracking/scripts/quality-score-calculator.py
# 如果有D级文档，阻止提交（可选）
if grep -q "D级文档" .improvement-tracking/quality-score-report.md; then
    echo "警告: 存在质量不及格的文档"
    # exit 1  # 取消注释以阻止提交
fi
```

---

## 6. 附录

### 6.1 报告文件清单

| 报告文件 | 说明 |
|----------|------|
| [orphaned-docs-report.md](./orphaned-docs-report.md) | 孤儿文档分析报告 |
| [duplicate-content-report.md](./duplicate-content-report.md) | 重复内容检测报告 |
| [outdated-tech-report.md](./outdated-tech-report.md) | 技术版本过时报告 |
| [quality-score-report.md](./quality-score-report.md) | 文档质量分数报告 |
| [quality-scores.json](./quality-scores.json) | 质量分数详细数据（JSON） |

### 6.2 健康度计算方式

```
健康度 = 100 - 扣分项

扣分规则:
- 孤儿文档: 每个扣2分，最多20分
- 版本过时: 每个扣3分，最多30分
- 质量不及格: 每个扣2分，最多20分
- 完全重复: 每组扣5分，最多15分

等级划分:
- A级(优秀): 80-100分
- B级(良好): 60-79分
- C级(一般): 40-59分
- D级(需改进): 0-39分
```

### 6.3 维护建议

1. **定期执行**: 建议每月运行一次完整检查
2. **优先级排序**: 优先处理健康度影响大的问题
3. **持续改进**: 将维护纳入日常开发流程
4. **团队协作**: 分配维护任务到具体责任人

---

> 本报告由 `maintenance-report-generator.py` 自动生成  
> 如需调整检查规则或报告格式，请修改对应脚本

"""
    
    return report


def main():
    """主函数"""
    global re
    import re
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print("=" * 70)
    print("📋 维护减负报告生成器")
    print("=" * 70)
    print(f"项目目录: {BASE_DIR}")
    print(f"开始时间: {timestamp}")
    print("-" * 70)
    
    # 统计文档数量
    print("\n📊 统计文档资产...")
    doc_counts = count_documents()
    print(f"   Markdown文档: {doc_counts['total_md']}")
    print(f"   - Struct/: {doc_counts['struct']}")
    print(f"   - Knowledge/: {doc_counts['knowledge']}")
    print(f"   - Flink/: {doc_counts['flink']}")
    
    # 统计形式化元素
    print("\n📐 统计形式化元素...")
    formal_elements = count_formal_elements()
    total_elements = sum(formal_elements.values())
    print(f"   总计: {total_elements} 个形式化元素")
    print(f"   - 定义: {formal_elements['definitions']}")
    print(f"   - 定理: {formal_elements['theorems']}")
    print(f"   - 引理: {formal_elements['lemmas']}")
    
    # 收集数据
    data = {}
    
    # 运行各个脚本（如果存在）
    scripts = [
        ('find-orphaned-docs.py', 'orphaned'),
        ('detect-duplicate-content.py', 'duplicate'),
        ('outdated-tech-check.py', 'outdated'),
        ('quality-score-calculator.py', 'quality')
    ]
    
    for script_name, data_key in scripts:
        script_path = os.path.join(SCRIPT_DIR, script_name)
        if os.path.exists(script_path):
            print(f"\n🔍 运行 {script_name}...")
            result = run_script(script_name)
            
            if 'error' in result:
                print(f"   ⚠ 运行失败: {result['error']}")
                data[data_key] = {}
            else:
                print(f"   ✓ 运行完成 (返回码: {result['returncode']})")
                # 解析输出
                parsed = parse_script_output(result['stdout'], data_key)
                data[data_key] = parsed
                
                # 打印关键指标
                for key, value in parsed.items():
                    print(f"   - {key}: {value}")
        else:
            print(f"\n⚠ 脚本不存在: {script_name}")
            data[data_key] = {}
    
    # 生成综合报告
    print("\n📝 生成综合维护报告...")
    report = generate_maintenance_report(data, doc_counts, formal_elements, timestamp)
    
    report_path = os.path.join(SCRIPT_DIR, REPORT_FILE)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"   报告已保存: {report_path}")
    
    # 输出摘要
    print("\n" + "=" * 70)
    print("📋 维护报告摘要")
    print("=" * 70)
    
    health_score = calculate_health_score(data)
    health_status = "🟢 优秀" if health_score >= 80 else "🟡 良好" if health_score >= 60 else "🟠 一般" if health_score >= 40 else "🔴 需改进"
    
    print(f"\n整体健康度: {health_score}/100 {health_status}")
    print(f"\n发现问题汇总:")
    
    total_issues = 0
    
    orphaned_count = data.get('orphaned', {}).get('orphaned_count', 0)
    if orphaned_count > 0:
        print(f"   🔴 孤儿文档: {orphaned_count} 个建议归档")
        total_issues += orphaned_count
    
    outdated_count = data.get('outdated', {}).get('outdated_count', 0)
    if outdated_count > 0:
        print(f"   🔴 版本过时: {outdated_count} 处需要更新")
        total_issues += outdated_count
    
    poor_count = data.get('quality', {}).get('poor_count', 0)
    if poor_count > 0:
        print(f"   🟠 质量不及格: {poor_count} 个文档待改进")
        total_issues += poor_count
    
    exact_dups = data.get('duplicate', {}).get('exact_dups', 0)
    if exact_dups > 0:
        print(f"   🔴 完全重复: {exact_dups} 组需要处理")
        total_issues += exact_dups
    
    if total_issues == 0:
        print("   ✅ 未发现需要处理的问题")
    else:
        print(f"\n   总计: {total_issues} 个问题需要关注")
    
    print(f"\n📄 详细报告: {REPORT_FILE}")
    print("=" * 70)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
