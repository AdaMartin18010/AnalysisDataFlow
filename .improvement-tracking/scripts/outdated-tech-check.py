#!/usr/bin/env python3
"""
outdated-tech-check.py - 技术版本过时检查

功能：检查文档中的技术版本是否过时，对比Flink最新版本
支持检测：Flink、Java、Scala、Python、Kafka、Kubernetes等
"""

import os
import sys
import re
import json
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError

# 配置
FLINK_VERSION_API = "https://api.github.com/repos/apache/flink/releases/latest"
KAFKA_VERSION_URL = "https://downloads.apache.org/kafka/"
SKIP_DIRECTORIES = ['.git', '.improvement-tracking', 'archive', '__pycache__']
REPORT_FILE = '../outdated-tech-report.md'

# 版本检测模式 - 扩展以支持更多技术栈
VERSION_PATTERNS = {
    'Flink': [
        r'Flink\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
        r'Apache\s+Flink\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
        r'flink-([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
    ],
    'Java': [
        r'Java\s+([0-9]+(?:\.[0-9]+)?)',
        r'JDK\s+([0-9]+(?:\.[0-9]+)?)',
        r'Java\s+SE\s+([0-9]+)',
    ],
    'Scala': [
        r'Scala\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
        r'scala-([0-9]+\.[0-9]+)',
    ],
    'Python': [
        r'Python\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
        r'pyflink\s+([0-9]+\.[0-9]+)',
    ],
    'Kafka': [
        r'Kafka\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
        r'kafka_([0-9]+\.[0-9]+)',
    ],
    'Kubernetes': [
        r'Kubernetes\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
        r'K8s\s+([0-9]+\.[0-9]+)',
        r'k8s\s+v?([0-9]+\.[0-9]+)',
    ],
    'Docker': [
        r'Docker\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
    ],
    'Maven': [
        r'Maven\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
    ],
    'Gradle': [
        r'Gradle\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
    ],
}

# 已知最新版本（硬编码作为后备，定期更新）
DEFAULT_LATEST_VERSIONS = {
    'Flink': '1.20.0',
    'Java': '21',
    'Scala': '2.13',
    'Python': '3.12',
    'Kafka': '3.8.0',
    'Kubernetes': '1.31',
    'Docker': '27.0',
    'Maven': '3.9.9',
    'Gradle': '8.10',
}


def fetch_flink_latest_version():
    """从GitHub API获取Flink最新版本"""
    try:
        req = Request(
            FLINK_VERSION_API,
            headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.v3+json'}
        )
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            tag_name = data.get('tag_name', '')
            # 移除 'release-' 前缀
            version = tag_name.replace('release-', '').replace('v', '')
            if version:
                print(f"   ✓ 从GitHub获取到Flink最新版本: {version}")
                return version
    except Exception as e:
        print(f"   ⚠ 无法获取Flink最新版本: {e}")
    
    return DEFAULT_LATEST_VERSIONS['Flink']


def parse_version(version_str):
    """解析版本字符串为元组，便于比较"""
    try:
        parts = version_str.split('.')
        return tuple(int(p) for p in parts[:3] if p.isdigit())
    except:
        return (0, 0, 0)


def compare_versions(v1, v2):
    """比较两个版本，返回-1, 0, 1"""
    p1, p2 = parse_version(v1), parse_version(v2)
    max_len = max(len(p1), len(p2))
    p1 = p1 + (0,) * (max_len - len(p1))
    p2 = p2 + (0,) * (max_len - len(p2))
    
    if p1 < p2:
        return -1
    elif p1 > p2:
        return 1
    return 0


def version_diff(v1, v2):
    """计算版本差距（主版本差 + 次版本差）"""
    p1, p2 = parse_version(v1), parse_version(v2)
    if len(p1) >= 2 and len(p2) >= 2:
        major_diff = abs(p1[0] - p2[0])
        minor_diff = abs(p1[1] - p2[1]) if major_diff == 0 else 0
        return major_diff, minor_diff
    return 0, 0


def get_version_status(doc_version, latest_version, tech_name):
    """判断版本状态"""
    if not doc_version or not latest_version:
        return 'unknown'
    
    comparison = compare_versions(doc_version, latest_version)
    
    if comparison >= 0:
        return 'current'
    
    major_diff, minor_diff = version_diff(doc_version, latest_version)
    
    # Flink特殊处理：主版本落后或次版本落后超过2
    if tech_name == 'Flink':
        if major_diff > 0 or minor_diff >= 3:
            return 'outdated'
        elif minor_diff >= 1:
            return 'warning'
    
    # 其他技术：主版本落后或次版本落后超过3
    if major_diff > 0 or minor_diff >= 3:
        return 'outdated'
    elif minor_diff >= 1:
        return 'warning'
    
    return 'current'


def extract_versions_from_file(filepath):
    """从文件中提取版本信息"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return []
    
    findings = []
    
    for tech_name, patterns in VERSION_PATTERNS.items():
        found_versions = set()
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                version = match.group(1)
                if version and version not in found_versions:
                    found_versions.add(version)
                    # 找到上下文
                    start = max(0, match.start() - 50)
                    end = min(len(content), match.end() + 50)
                    context = content[start:end].replace('\n', ' ')
                    findings.append({
                        'tech': tech_name,
                        'version': version,
                        'context': context.strip(),
                        'position': match.start()
                    })
    
    return findings


def scan_documents(base_dir):
    """扫描所有markdown文档"""
    documents = []
    
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRECTORIES]
        
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                versions = extract_versions_from_file(filepath)
                if versions:
                    documents.append({
                        'path': filepath,
                        'filename': filename,
                        'findings': versions
                    })
    
    return documents


def analyze_outdated_docs(documents, latest_versions):
    """分析过时的文档"""
    results = []
    
    for doc in documents:
        doc_results = {
            'path': doc['path'],
            'filename': doc['filename'],
            'findings': []
        }
        
        for finding in doc['findings']:
            tech = finding['tech']
            version = finding['version']
            latest = latest_versions.get(tech)
            
            if latest:
                status = get_version_status(version, latest, tech)
                finding['latest'] = latest
                finding['status'] = status
                finding['severity'] = {
                    'outdated': 'high',
                    'warning': 'medium',
                    'current': 'low',
                    'unknown': 'low'
                }.get(status, 'low')
                doc_results['findings'].append(finding)
        
        if doc_results['findings']:
            results.append(doc_results)
    
    return results


def categorize_findings(results):
    """分类整理发现"""
    outdated = []
    warning = []
    current = []
    
    for doc in results:
        for finding in doc['findings']:
            item = {
                'path': doc['path'],
                'filename': doc['filename'],
                **finding
            }
            
            if finding['status'] == 'outdated':
                outdated.append(item)
            elif finding['status'] == 'warning':
                warning.append(item)
            else:
                current.append(item)
    
    return {
        'outdated': outdated,
        'warning': warning,
        'current': current
    }


def generate_report(categorized, latest_versions, base_dir):
    """生成报告"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    outdated_count = len(categorized['outdated'])
    warning_count = len(categorized['warning'])
    current_count = len(categorized['current'])
    total_count = outdated_count + warning_count + current_count
    
    report = f"""# 技术版本过时检查报告

> 生成时间: {timestamp}

## 最新版本参考

| 技术 | 最新版本 | 状态 |
|------|----------|------|
"""
    
    for tech, version in sorted(latest_versions.items()):
        report += f"| {tech} | {version} | {'✅ 已获取' if version != DEFAULT_LATEST_VERSIONS.get(tech) else '⚠️ 默认值'} |\n"
    
    report += f"""

## 摘要

| 级别 | 数量 | 说明 |
|------|------|------|
| 🔴 严重过时 | {outdated_count} | 版本落后较多，建议立即更新 |
| 🟡 需要关注 | {warning_count} | 版本略有落后，建议规划更新 |
| ✅ 当前版本 | {current_count} | 版本最新 |
| **总计** | **{total_count}** | - |

---

## 1. 严重过时的版本 🔴

以下文档中的技术版本**严重过时**，建议优先更新：

| 技术 | 文档版本 | 最新版本 | 文件路径 | 上下文 |
|------|----------|----------|----------|--------|
"""
    
    for item in categorized['outdated']:
        rel_path = os.path.relpath(item['path'], base_dir)
        context = item['context'][:60] + '...' if len(item['context']) > 60 else item['context']
        context = context.replace('|', '\\|')
        report += f"| {item['tech']} | {item['version']} | {item['latest']} | `{rel_path}` | {context} |\n"
    
    if not categorized['outdated']:
        report += "\n✅ 未发现严重过时的版本\n"
    
    report += f"""

### 1.1 按技术统计

"""
    
    # 按技术统计
    tech_stats = {}
    for item in categorized['outdated']:
        tech = item['tech']
        if tech not in tech_stats:
            tech_stats[tech] = {'count': 0, 'versions': set()}
        tech_stats[tech]['count'] += 1
        tech_stats[tech]['versions'].add(item['version'])
    
    report += "| 技术 | 过时次数 | 涉及的旧版本 |\n"
    report += "|------|----------|--------------|\n"
    for tech, stats in sorted(tech_stats.items()):
        versions_str = ', '.join(sorted(stats['versions']))
        report += f"| {tech} | {stats['count']} | {versions_str} |\n"
    
    report += f"""

---

## 2. 需要关注的版本 🟡

以下文档中的技术版本**略有落后**，建议规划更新：

| 技术 | 文档版本 | 最新版本 | 文件路径 |
|------|----------|----------|----------|
"""
    
    for item in categorized['warning']:
        rel_path = os.path.relpath(item['path'], base_dir)
        report += f"| {item['tech']} | {item['version']} | {item['latest']} | `{rel_path}` |\n"
    
    if not categorized['warning']:
        report += "\n✅ 没有发现需要关注的版本\n"
    
    report += f"""

---

## 3. 当前版本统计 ✅

以下文档使用了最新的技术版本：

| 技术 | 文档中使用次数 | 版本 |
|------|----------------|------|
"""
    
    current_stats = {}
    for item in categorized['current']:
        tech = item['tech']
        if tech not in current_stats:
            current_stats[tech] = {'count': 0, 'version': item['version']}
        current_stats[tech]['count'] += 1
    
    for tech, stats in sorted(current_stats.items()):
        report += f"| {tech} | {stats['count']} | {stats['version']} |\n"
    
    if not categorized['current']:
        report += "\n- 没有使用当前版本的记录\n"
    
    report += f"""

---

## 4. 更新建议

### 4.1 Flink专项更新建议

根据最新Flink版本 {latest_versions.get('Flink', 'N/A')}，建议关注以下更新：

1. **检查API变更**: 从旧版本升级到新版本时，检查是否有废弃的API
2. **更新依赖版本**: 更新pom.xml或build.gradle中的Flink依赖
3. **验证配置参数**: 检查是否有新增或废弃的配置参数
4. **测试兼容性**: 在升级生产环境前进行充分测试

### 4.2 通用更新策略

1. **优先级**: 优先更新标记为"严重过时"的文档
2. **批量更新**: 同一技术的多个文档可以批量更新
3. **验证流程**: 更新后应进行以下检查：
   - 代码示例是否能正常运行
   - 配置参数是否仍然有效
   - 链接是否仍然可访问

### 4.3 自动化更新脚本示例

```bash
# 批量替换Flink版本号（请谨慎使用）
find . -name "*.md" -exec sed -i 's/Flink 1\.16/Flink 1.20/g' {{}} \\;
find . -name "*.md" -exec sed -i 's/flink-1\.16/flink-1.20/g' {{}} \\;

# 建议先进行干运行（dry-run）查看哪些文件会被修改
grep -r "Flink 1\\.16" --include="*.md" .
```

### 4.4 版本跟踪清单

- [ ] 更新所有标记为"严重过时"的Flink版本
- [ ] 更新Java版本参考（建议升级到Java 17或21）
- [ ] 检查Scala版本兼容性
- [ ] 验证Kafka客户端版本
- [ ] 更新Kubernetes部署示例

---

## 5. 附录：版本获取方式

| 技术 | 版本查询方式 |
|------|--------------|
| Flink | GitHub Releases: https://github.com/apache/flink/releases |
| Java | Oracle/OpenJDK官网或SDK管理工具 |
| Kafka | Apache Kafka下载页 |
| Kubernetes | Kubernetes官方文档 |
| Python | Python官网或pyenv |

> **注意**: 本报告基于自动检测生成，建议人工复核后再进行更新操作。

"""
    
    return report


def main():
    """主函数"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(script_dir))
    
    print("=" * 60)
    print("🔍 技术版本过时检查工具")
    print("=" * 60)
    print(f"扫描目录: {base_dir}")
    print("-" * 60)
    
    # 获取最新版本
    print("\n📡 获取最新版本信息...")
    latest_versions = DEFAULT_LATEST_VERSIONS.copy()
    
    # 尝试获取Flink最新版本
    flink_version = fetch_flink_latest_version()
    if flink_version:
        latest_versions['Flink'] = flink_version
    
    print(f"\n   使用版本参考:")
    for tech, version in sorted(latest_versions.items()):
        status = "✓" if version != DEFAULT_LATEST_VERSIONS.get(tech) else "默认"
        print(f"   - {tech}: {version} ({status})")
    
    # 扫描文档
    print("\n📂 扫描文档中的版本信息...")
    documents = scan_documents(base_dir)
    print(f"   找到 {len(documents)} 个包含版本信息的文档")
    
    # 分析过时版本
    print("\n📊 分析版本状态...")
    results = analyze_outdated_docs(documents, latest_versions)
    
    # 分类整理
    categorized = categorize_findings(results)
    
    outdated_count = len(categorized['outdated'])
    warning_count = len(categorized['warning'])
    
    print(f"   🔴 严重过时: {outdated_count} 处")
    print(f"   🟡 需要关注: {warning_count} 处")
    print(f"   ✅ 当前版本: {len(categorized['current'])} 处")
    
    # 生成报告
    print("\n📝 生成报告...")
    report = generate_report(categorized, latest_versions, base_dir)
    
    report_path = os.path.join(script_dir, REPORT_FILE)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"   报告已保存: {report_path}")
    
    # 输出摘要
    print("\n" + "=" * 60)
    print("📋 执行摘要")
    print("=" * 60)
    
    if outdated_count == 0 and warning_count == 0:
        print("✅ 所有技术版本都是最新的")
    else:
        if outdated_count > 0:
            print(f"🔴 发现 {outdated_count} 处严重过时的版本，建议优先更新")
        if warning_count > 0:
            print(f"🟡 发现 {warning_count} 处需要关注的版本，建议规划更新")
    
    print("\n💡 提示: 版本信息可能存在误报，建议人工复核")
    print("=" * 60)
    
    return outdated_count + warning_count


if __name__ == '__main__':
    sys.exit(main())
