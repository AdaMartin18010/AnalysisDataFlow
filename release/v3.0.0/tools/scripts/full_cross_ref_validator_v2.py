#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全量交叉引用验证脚本 v2
改进版本：更准确地识别代码块、处理锚点格式
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from urllib.parse import urlparse, unquote


class CrossRefValidator:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.target_dirs = ['Struct', 'Knowledge', 'Flink']
        
        # 统计信息
        self.total_links = 0
        self.valid_links = 0
        self.ignored_links = 0
        self.broken_links = []
        
        # 文件和锚点索引
        self.all_files = set()
        self.file_anchors = defaultdict(set)  # 文件 -> 锚点集合
        
        # 链接模式匹配 [text](path) 或 [text](path#anchor)
        # 改进：要求链接文本不为空且至少包含一个非空白字符
        self.link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        # 锚点模式匹配 {#anchor} 或 ## Header {#anchor}
        self.anchor_pattern = re.compile(r'\{#[\w\-\_\.]+\}')
        # 标题模式 - 支持显式锚点
        self.header_pattern = re.compile(r'^(#{1,6})\s+(.+?)(?:\s+\{#([\w\-\_\.]+)\})?$')
        
        # 代码块标记
        self.code_fence_pattern = re.compile(r'^```')
        
    def scan_all_files(self):
        """扫描所有目标目录中的Markdown文件"""
        print("🔍 正在扫描所有Markdown文件...")
        
        for dir_name in self.target_dirs:
            dir_path = self.root_dir / dir_name
            if dir_path.exists():
                for md_file in dir_path.rglob('*.md'):
                    self.all_files.add(md_file)
                    self.extract_anchors(md_file)
                    
        print(f"✅ 扫描完成: 共 {len(self.all_files)} 个Markdown文件")
        
    def extract_anchors(self, file_path):
        """从文件中提取所有锚点"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                for line in lines:
                    # 匹配标题锚点 ## Header {#anchor}
                    header_match = self.header_pattern.match(line)
                    if header_match:
                        level, text, explicit_anchor = header_match.groups()
                        if explicit_anchor:
                            self.file_anchors[file_path].add(explicit_anchor.lower())
                        else:
                            # 从标题文本生成隐式锚点
                            implicit_anchor = self.generate_anchor_from_text(text)
                            if implicit_anchor:
                                self.file_anchors[file_path].add(implicit_anchor.lower())
                    
                    # 匹配显式锚点定义 {#anchor}
                    for match in self.anchor_pattern.finditer(line):
                        anchor = match.group(0)[2:-1]  # 去掉 {# 和 }
                        self.file_anchors[file_path].add(anchor.lower())
                        
        except Exception as e:
            print(f"⚠️  读取文件失败 {file_path}: {e}")
            
    def generate_anchor_from_text(self, text):
        """从标题文本生成GitHub风格的锚点"""
        # 移除markdown标记
        text = re.sub(r'<[^>]+>', '', text)  # HTML标签
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # 链接
        text = re.sub(r'[_\*`]', '', text)  # 格式标记
        
        # 移除开头的数字和点 (如 "1. " 或 "4.1 ")
        text = re.sub(r'^\d+(\.\d+)*\s*', '', text)
        
        # 转换为小写，替换空格为连字符
        anchor = text.strip().lower()
        anchor = re.sub(r'\s+', '-', anchor)
        anchor = re.sub(r'[^\w\-\_\.]', '-', anchor)  # 非字母数字字符替换为连字符
        anchor = re.sub(r'-+', '-', anchor)  # 多个连字符合并
        anchor = anchor.strip('-')
        
        return anchor if anchor else None
        
    def normalize_anchor(self, anchor):
        """规范化锚点，处理不同的格式变体"""
        anchor = anchor.lower().strip()
        
        # 变体1: "1-概念定义-definitions" -> "概念定义-definitions"
        # 变体2: "1.-概念定义-definitions" -> "概念定义-definitions"
        # 变体3: 保持原样
        
        variants = [anchor]
        
        # 移除前导数字前缀（如 "1-" 或 "1.-" 或 "4.1-"）
        no_number = re.sub(r'^(\d+(?:\.\d+)*)[-\.\s]*', '', anchor)
        if no_number and no_number != anchor:
            variants.append(no_number)
            
        # 将 "1-" 变为 "1.-"
        with_dot = re.sub(r'^(\d+(?:\.\d+)*)-', r'\1.-', anchor)
        if with_dot != anchor:
            variants.append(with_dot)
            
        # 将 "1.-" 变为 "1-"
        without_dot = re.sub(r'^(\d+(?:\.\d)*)\.\-', r'\1-', anchor)
        if without_dot != anchor:
            variants.append(without_dot)
            
        return variants
        
    def is_likely_code_content(self, line_content, link_text, link_target):
        """判断一个链接是否可能是代码中的泛型语法"""
        # 如果链接文本是大写的单个字母（如 T, K, V, S, R）或常见的泛型参数名
        if re.match(r'^[A-Z]$', link_text):
            # 检查周围是否有代码特征
            if any(indicator in line_content for indicator in [
                'def ', 'class ', 'val ', 'var ', 'type ', '<', '>',
                ']', '[', '(', ')', '=>', '::', 'new ', 'extends'
            ]):
                return True
                
        # 如果链接目标是代码片段（包含特殊字符）
        if re.search(r'[<>\(\)\[\]\{\}\|=>]', link_target):
            return True
            
        # 如果链接文本是类型参数格式（如 [A, B], [T], [K, V]）
        if re.match(r'^[A-Z]+(,[\s]*[A-Z]+)*$', link_text):
            return True
            
        return False
        
    def validate_all_links(self):
        """验证所有文件中的链接"""
        print("🔗 正在验证交叉引用...")
        
        for file_path in sorted(self.all_files):
            self.validate_file_links(file_path)
            
        print(f"✅ 验证完成: 共 {self.total_links} 个引用")
        
    def validate_file_links(self, file_path):
        """验证单个文件中的所有链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                in_code_block = False
                for line_num, line in enumerate(lines, 1):
                    # 检测代码块边界
                    if self.code_fence_pattern.match(line):
                        in_code_block = not in_code_block
                        continue
                        
                    # 跳过代码块中的内容
                    if in_code_block:
                        continue
                        
                    for match in self.link_pattern.finditer(line):
                        link_text, link_target = match.groups()
                        self.validate_link(file_path, line_num, link_text, link_target, line)
                        
        except Exception as e:
            print(f"⚠️  读取文件失败 {file_path}: {e}")
            
    def validate_link(self, source_file, line_num, link_text, link_target, line_content):
        """验证单个链接"""
        self.total_links += 1
        
        # 跳过外部链接
        if link_target.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            self.ignored_links += 1
            return
            
        # 跳过可能是代码泛型语法的链接
        if self.is_likely_code_content(line_content, link_text, link_target):
            self.ignored_links += 1
            return
            
        # 纯锚点链接（同一文件内）
        if link_target.startswith('#'):
            anchor = link_target[1:]
            self.check_anchor(source_file, source_file, line_num, link_text, anchor, line_content)
            return
            
        # 解析链接
        if '#' in link_target:
            file_part, anchor = link_target.split('#', 1)
        else:
            file_part, anchor = link_target, None
            
        # 处理相对路径
        if file_part:
            # 解析路径
            if file_part.startswith('/'):
                # 绝对路径（相对于项目根目录）
                target_file = self.root_dir / file_part.lstrip('/')
            else:
                # 相对路径
                target_file = source_file.parent / file_part
                
            # 规范化路径
            try:
                target_file = target_file.resolve()
            except:
                target_file = target_file.absolute()
                
            # 检查文件是否存在
            if not target_file.exists():
                self.broken_links.append({
                    'type': 'file_not_found',
                    'source': str(source_file.relative_to(self.root_dir)),
                    'line': line_num,
                    'link_text': link_text,
                    'target': link_target,
                    'resolved_path': str(target_file.relative_to(self.root_dir)) if self.root_dir in target_file.parents else str(target_file),
                    'line_content': line_content.strip()[:100]
                })
                return
                
            # 如果有锚点，检查锚点
            if anchor:
                self.check_anchor(source_file, target_file, line_num, link_text, anchor, line_content)
            else:
                self.valid_links += 1
        else:
            # 只有锚点的情况
            if anchor:
                self.check_anchor(source_file, source_file, line_num, link_text, anchor, line_content)
                
    def check_anchor(self, source_file, target_file, line_num, link_text, anchor, line_content):
        """检查锚点是否存在"""
        anchor_variants = self.normalize_anchor(anchor)
        
        if target_file in self.file_anchors:
            file_anchors = self.file_anchors[target_file]
            for variant in anchor_variants:
                if variant in file_anchors:
                    self.valid_links += 1
                    return
                    
        # 锚点不存在
        self.broken_links.append({
            'type': 'anchor_not_found',
            'source': str(source_file.relative_to(self.root_dir)),
            'line': line_num,
            'link_text': link_text,
            'target': f"#{anchor}",
            'target_file': str(target_file.relative_to(self.root_dir)),
            'available_anchors': sorted(self.file_anchors.get(target_file, set()))[:10],
            'line_content': line_content.strip()[:100]
        })
        
    def generate_report(self):
        """生成验证报告"""
        timestamp = datetime.now().isoformat()
        
        # 统计
        file_not_found = [b for b in self.broken_links if b['type'] == 'file_not_found']
        anchor_not_found = [b for b in self.broken_links if b['type'] == 'anchor_not_found']
        
        report = {
            'timestamp': timestamp,
            'summary': {
                'total_files': len(self.all_files),
                'total_links': self.total_links,
                'valid_links': self.valid_links,
                'ignored_links': self.ignored_links,
                'broken_links': len(self.broken_links),
                'file_not_found': len(file_not_found),
                'anchor_not_found': len(anchor_not_found),
                'validity_rate': round((self.valid_links / (self.total_links - self.ignored_links) * 100), 2) if (self.total_links - self.ignored_links) > 0 else 0
            },
            'broken_links': {
                'file_not_found': file_not_found,
                'anchor_not_found': anchor_not_found
            },
            'file_statistics': self.generate_file_statistics()
        }
        
        return report
        
    def generate_file_statistics(self):
        """生成每个文件的链接统计"""
        stats = defaultdict(lambda: {'total': 0, 'valid': 0, 'broken': 0})
        
        # 统计所有文件的链接数
        for link in self.broken_links:
            source = link['source']
            stats[source]['total'] += 1
            stats[source]['broken'] += 1
            
        # 转换为列表
        result = []
        for file_path, counts in sorted(stats.items(), key=lambda x: -x[1]['broken']):
            result.append({
                'file': file_path,
                'broken_count': counts['broken']
            })
            
        return result
        
    def save_reports(self, report):
        """保存报告到文件"""
        # JSON报告
        json_path = self.root_dir / 'cross-ref-validation-report-v2.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        # Markdown报告
        md_path = self.root_dir / 'cross-ref-validation-report-v2.md'
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_markdown_report(report))
            
        print(f"\n📄 报告已保存:")
        print(f"   - JSON: {json_path}")
        print(f"   - Markdown: {md_path}")
        
    def generate_markdown_report(self, report):
        """生成Markdown格式的报告"""
        s = report['summary']
        
        md = f"""# 全量交叉引用验证报告 v2

> 生成时间: {report['timestamp']}
> 验证范围: Struct/ Knowledge/ Flink/ 目录下的所有Markdown文件
> 验证版本: v2（改进版，过滤代码块和泛型语法）

## 📊 统计概览

| 指标 | 数值 |
|------|------|
| **扫描文件数** | {s['total_files']} |
| **总引用数** | {s['total_links']:,} |
| **有效引用** | {s['valid_links']:,} |
| **已忽略** (外部链接/代码) | {s['ignored_links']:,} |
| **断裂引用** | {s['broken_links']:,} |
| **文件不存在** | {s['file_not_found']:,} |
| **锚点不存在** | {s['anchor_not_found']:,} |
| **有效引用率** | {s['validity_rate']}% |

## 🔴 断裂引用详情

### 1. 文件不存在错误 ({s['file_not_found']} 个)

"""
        
        if report['broken_links']['file_not_found']:
            md += "| 源文件 | 行号 | 链接文本 | 目标路径 | 代码片段 |\n"
            md += "|--------|------|----------|----------|----------|\n"
            for item in report['broken_links']['file_not_found']:
                md += f"| `{item['source']}` | {item['line']} | {item['link_text'][:30]} | `{item['resolved_path'][:40]}` | `{item['line_content'][:40]}` |\n"
        else:
            md += "✅ 未发现文件不存在错误\n"
            
        md += f"\n### 2. 锚点不存在错误 ({s['anchor_not_found']} 个)\n\n"
        
        if report['broken_links']['anchor_not_found']:
            md += "| 源文件 | 行号 | 链接文本 | 目标文件 | 缺失锚点 | 可用锚点示例 |\n"
            md += "|--------|------|----------|----------|----------|--------------|\n"
            for item in report['broken_links']['anchor_not_found']:
                available = ', '.join(item['available_anchors'][:5]) if item['available_anchors'] else 'N/A'
                md += f"| `{item['source']}` | {item['line']} | {item['link_text'][:20]} | `{item['target_file'][:30]}` | `{item['target']}` | {available} |\n"
        else:
            md += "✅ 未发现锚点不存在错误\n"
            
        md += f"""
## 📁 问题文件Top 20

以下文件包含最多的断裂引用：

"""
        
        if report['file_statistics']:
            md += "| 排名 | 文件路径 | 断裂引用数 |\n"
            md += "|------|----------|------------|\n"
            for i, item in enumerate(report['file_statistics'][:20], 1):
                md += f"| {i} | `{item['file']}` | {item['broken_count']} |\n"
        else:
            md += "✅ 所有文件均无断裂引用\n"
            
        md += """
## 🔧 修复建议

### 文件不存在错误
1. 检查链接路径是否正确
2. 确认目标文件是否被移动或重命名
3. 使用相对路径时，确保路径相对于当前文件位置正确

### 锚点不存在错误
1. 检查锚点标识符是否拼写正确
2. 确认目标标题是否包含显式锚点定义 `{#anchor}`
3. 如果是隐式锚点，确保与GitHub生成的锚点格式一致（小写，空格替换为连字符）
4. 注意数字前缀的处理：`#1-概念定义` 与 `#概念定义` 是不同的锚点

## 📋 验证规则说明

- **代码块过滤**: 代码块（```...```）中的内容被忽略
- **泛型语法过滤**: 代码中的泛型参数如 `[T]`、`[String]` 等被忽略
- **外部链接**: `http://` 和 `https://` 开头的链接被忽略
- **锚点匹配**: 支持多种锚点格式变体（带/不带数字前缀）
- **大小写不敏感**: 锚点检查不区分大小写
"""
        
        return md
        
    def run(self):
        """运行完整的验证流程"""
        print("=" * 60)
        print("🔍 全量交叉引用验证 v2")
        print("=" * 60)
        
        # 1. 扫描所有文件
        self.scan_all_files()
        
        # 2. 验证所有链接
        self.validate_all_links()
        
        # 3. 生成报告
        report = self.generate_report()
        
        # 4. 保存报告
        self.save_reports(report)
        
        # 5. 打印摘要
        print("\n" + "=" * 60)
        print("📊 验证摘要")
        print("=" * 60)
        s = report['summary']
        print(f"  扫描文件数: {s['total_files']}")
        print(f"  总引用数: {s['total_links']:,}")
        print(f"  已忽略: {s['ignored_links']:,}")
        print(f"  有效引用: {s['valid_links']:,}")
        print(f"  断裂引用: {s['broken_links']:,}")
        print(f"  有效引用率: {s['validity_rate']}%")
        
        if s['broken_links'] > 0:
            print(f"\n⚠️  发现 {s['broken_links']} 个断裂引用，请查看详细报告")
            return False
        else:
            print("\n✅ 所有交叉引用均有效！")
            return True


if __name__ == '__main__':
    import sys
    
    # 获取项目根目录
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    validator = CrossRefValidator(root_dir)
    success = validator.run()
    
    sys.exit(0 if success else 1)
