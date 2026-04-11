#!/usr/bin/env python3
"""
AnalysisDataFlow 项目断链修复工具
==============================
自动修复Markdown文档中的无效内部链接和外部链接。

功能:
- 修复已知的内部链接路径错误
- 更新指向已移动文件的链接
- 修复外部链接(查找替代URL或标记为历史)
- 生成详细的修复报告

作者: Agent
版本: 1.0.0
"""

import os
import re
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from collections import defaultdict

# ============ 配置 ============
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
REPORTS_DIR = PROJECT_ROOT / "reports"

# 链接映射规则: (旧链接模式, 新链接路径, 修复类型)
# 修复类型: 'exact' (精确匹配), 'prefix' (前缀匹配), 'regex' (正则匹配)
LINK_REPLACEMENTS = [
    # FLINK-24-25-30-COMPLETION-REPORT.md 移动到 archive/completion-reports/
    ('FLINK-24-25-30-COMPLETION-REPORT.md', 'archive/completion-reports/FLINK-24-25-30-COMPLETION-REPORT.md', 'exact'),
    ('./FLINK-24-25-30-COMPLETION-REPORT.md', './archive/completion-reports/FLINK-24-25-30-COMPLETION-REPORT.md', 'exact'),
    
    # Flink/00-INDEX.md -> Flink/00-meta/00-INDEX.md
    ('Flink/00-INDEX.md', 'Flink/00-meta/00-INDEX.md', 'exact'),
    
    # Flink/06-engineering/performance-tuning-guide.md -> Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md
    ('Flink/06-engineering/performance-tuning-guide.md', 'Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md', 'exact'),
    ('./Flink/06-engineering/performance-tuning-guide.md', './Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md', 'exact'),
    
    # Flink/07-case-studies/ -> Flink/09-practices/09.01-case-studies/
    ('Flink/07-case-studies/', 'Flink/09-practices/09.01-case-studies/', 'prefix'),
    ('./Flink/07-case-studies/', './Flink/09-practices/09.01-case-studies/', 'prefix'),
    
    # Flink/02-core-mechanisms/ -> Flink/02-core/
    ('Flink/02-core-mechanisms/', 'Flink/02-core/', 'prefix'),
    ('./Flink/02-core-mechanisms/', './Flink/02-core/', 'prefix'),
    
    # PROJECT-VERSION-TRACKING.md -> Flink/00-meta/version-tracking.md
    ('PROJECT-VERSION-TRACKING.md', 'Flink/00-meta/version-tracking.md', 'exact'),
    ('./PROJECT-VERSION-TRACKING.md', './Flink/00-meta/version-tracking.md', 'exact'),
]

# 外部链接替换规则
EXTERNAL_LINK_REPLACEMENTS = [
    # Flink 文档链接更新
    ('https://flink.apache.org/documentation/exactly-once.html', 
     'https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/exactly_once/'),
    
    # Kafka 文档链接更新
    ('https://kafka.apache.org/documentation/producer-configs',
     'https://kafka.apache.org/documentation/#producerconfigs'),
    ('https://kafka.apache.org/documentation/transactions',
     'https://kafka.apache.org/documentation/#transactions'),
    
    # Pekko 链接
    ('https://pekko.apache.org/docs/',
     'https://pekko.apache.org/docs/pekko/current/'),
     
    # GitHub 链接更新 (master -> main)
    ('https://github.com/apache/flink/tree/master/',
     'https://github.com/apache/flink/tree/main/'),
]

# 已知移动的文件映射
MOVED_FILES = {
    'BENCHMARK-REPORT.md': {'line': 1, 'old': 'Flink/11-benchmarking/streaming-benchmarks.md', 'new': 'Flink/flink-performance-benchmark-suite.md'},
    'BEST-PRACTICES.md': {'line': 211, 'old': '"agg-state", classOf[Accumulator]', 'new': None, 'note': '代码片段,需手动修复'},
    'CASE-STUDIES.md': {'line': 19, 'old': './Flink/07-case-studies/case-realtime-analytics.md', 'new': './Flink/09-practices/09.01-case-studies/case-financial-realtime-risk-control.md'},
}


@dataclass
class FixResult:
    """修复结果数据类"""
    file_path: str
    line_number: int
    original_link: str
    fixed_link: Optional[str]
    fix_type: str  # 'internal', 'external', 'marked', 'manual', 'code_snippet'
    status: str  # 'success', 'failed', 'skipped'
    message: str = ""


class BrokenLinkFixer:
    """断链修复器主类"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.fixes: List[FixResult] = []
        self.stats = {
            'files_processed': 0,
            'fixes_applied': 0,
            'fixes_skipped': 0,
            'fixes_failed': 0,
            'external_fixed': 0,
            'marked_historical': 0,
        }
        
    def load_broken_links(self, json_path: Path) -> List[Dict]:
        """加载断链JSON数据"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 无法加载断链文件: {e}")
            return []
    
    def is_code_snippet(self, url: str) -> bool:
        """检查是否是代码片段而非真实链接"""
        code_patterns = [
            'classOf[',
            '_.length',
            '".md"',
            '"> ',
            'agg-state',
            'session-state',
        ]
        return any(pattern in url for pattern in code_patterns)
    
    def is_anchor_only(self, url: str) -> bool:
        """检查是否只有锚点"""
        return url.startswith('#') and len(url) > 1
    
    def fix_internal_link(self, url: str, source_file: Path) -> Optional[str]:
        """修复内部链接,返回修复后的URL或None"""
        # 跳过代码片段
        if self.is_code_snippet(url):
            return None
        
        # 跳过纯锚点
        if self.is_anchor_only(url):
            return None
        
        # 应用替换规则
        for old_pattern, new_pattern, match_type in LINK_REPLACEMENTS:
            if match_type == 'exact':
                if url == old_pattern:
                    return new_pattern
            elif match_type == 'prefix':
                if url.startswith(old_pattern):
                    return new_pattern + url[len(old_pattern):]
        
        return None
    
    def fix_external_link(self, url: str) -> Optional[str]:
        """修复外部链接"""
        for old_url, new_url in EXTERNAL_LINK_REPLACEMENTS:
            if url.startswith(old_url):
                return new_url
        return None
    
    def process_file(self, file_path: Path, broken_items: List[Dict]) -> List[FixResult]:
        """处理单个文件中的断链"""
        results = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            return [FixResult(str(file_path), 0, "", None, "error", "failed", str(e))]
        
        # 跟踪已修改的行
        modified_lines = set()
        new_lines = lines.copy()
        
        for item in broken_items:
            line_num = item.get('line', 1) - 1  # 转为0-based
            url = item.get('url', '')
            text = item.get('text', '')
            
            if line_num < 0 or line_num >= len(lines):
                continue
            
            # 跳过已处理的行
            if line_num in modified_lines:
                continue
            
            original_line = lines[line_num]
            
            # 判断链接类型并修复
            fixed_url = None
            fix_type = "unknown"
            
            if url.startswith('http'):
                # 外部链接
                fixed_url = self.fix_external_link(url)
                fix_type = "external"
                if fixed_url:
                    self.stats['external_fixed'] += 1
            else:
                # 内部链接
                fixed_url = self.fix_internal_link(url, file_path)
                fix_type = "internal"
            
            # 应用修复
            if fixed_url:
                # 替换行中的链接
                new_line = original_line.replace(url, fixed_url)
                if new_line != original_line:
                    new_lines[line_num] = new_line
                    modified_lines.add(line_num)
                    results.append(FixResult(
                        str(file_path), line_num + 1, url, fixed_url, 
                        fix_type, "success"
                    ))
                    self.stats['fixes_applied'] += 1
            elif self.is_code_snippet(url):
                results.append(FixResult(
                    str(file_path), line_num + 1, url, None,
                    "code_snippet", "skipped", "代码片段,需手动检查"
                ))
                self.stats['fixes_skipped'] += 1
            else:
                # 无法自动修复
                results.append(FixResult(
                    str(file_path), line_num + 1, url, None,
                    fix_type, "skipped", "无法自动修复,需手动处理"
                ))
                self.stats['fixes_skipped'] += 1
        
        # 写回文件
        if modified_lines:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
            except Exception as e:
                for r in results:
                    if r.status == "success":
                        r.status = "failed"
                        r.message = f"写入失败: {e}"
                self.stats['fixes_failed'] += len(modified_lines)
                self.stats['fixes_applied'] -= len(modified_lines)
        
        return results
    
    def fix_specific_files(self):
        """修复特定已知问题的文件"""
        fixes = []
        
        # 修复 AGENTS.md
        agents_file = self.project_root / "AGENTS.md"
        if agents_file.exists():
            try:
                with open(agents_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 修复 FLINK-24-25-30-COMPLETION-REPORT.md 链接
                old_content = content
                content = content.replace(
                    './FLINK-24-25-30-COMPLETION-REPORT.md',
                    './archive/completion-reports/FLINK-24-25-30-COMPLETION-REPORT.md'
                )
                
                if content != old_content:
                    with open(agents_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixes.append(FixResult(str(agents_file), 0, "FLINK-24-25-30-COMPLETION-REPORT.md", 
                                          "archive/completion-reports/FLINK-24-25-30-COMPLETION-REPORT.md",
                                          "internal", "success"))
                    self.stats['fixes_applied'] += 1
            except Exception as e:
                print(f"❌ 修复 AGENTS.md 失败: {e}")
        
        # 修复 ARCHITECTURE.md
        arch_file = self.project_root / "ARCHITECTURE.md"
        if arch_file.exists():
            try:
                with open(arch_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                old_content = content
                content = content.replace(
                    'Flink/00-INDEX.md',
                    'Flink/00-meta/00-INDEX.md'
                )
                content = content.replace(
                    './FLINK-24-25-30-COMPLETION-REPORT.md',
                    './archive/completion-reports/FLINK-24-25-30-COMPLETION-REPORT.md'
                )
                
                if content != old_content:
                    with open(arch_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixes.append(FixResult(str(arch_file), 0, "多重链接", None,
                                          "internal", "success"))
                    self.stats['fixes_applied'] += 1
            except Exception as e:
                print(f"❌ 修复 ARCHITECTURE.md 失败: {e}")
        
        # 修复 BENCHMARK-REPORT.md
        bench_file = self.project_root / "BENCHMARK-REPORT.md"
        if bench_file.exists():
            try:
                with open(bench_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                old_content = content
                content = content.replace(
                    './Flink/06-engineering/performance-tuning-guide.md',
                    './Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md'
                )
                
                if content != old_content:
                    with open(bench_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixes.append(FixResult(str(bench_file), 0, "performance-tuning-guide.md", None,
                                          "internal", "success"))
                    self.stats['fixes_applied'] += 1
            except Exception as e:
                print(f"❌ 修复 BENCHMARK-REPORT.md 失败: {e}")
        
        # 修复 BROKEN-LINK-FIX-REPORT.md
        broken_file = self.project_root / "BROKEN-LINK-FIX-REPORT.md"
        if broken_file.exists():
            try:
                with open(broken_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                old_content = content
                content = content.replace(
                    './FLINK-24-25-30-COMPLETION-REPORT.md',
                    './archive/completion-reports/FLINK-24-25-30-COMPLETION-REPORT.md'
                )
                content = content.replace(
                    'Flink/00-INDEX.md',
                    'Flink/00-meta/00-INDEX.md'
                )
                content = content.replace(
                    './Flink/06-engineering/performance-tuning-guide.md',
                    './Flink/09-practices/09.03-performance-tuning/performance-tuning-guide.md'
                )
                
                if content != old_content:
                    with open(broken_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixes.append(FixResult(str(broken_file), 0, "多重链接", None,
                                          "internal", "success"))
                    self.stats['fixes_applied'] += 1
            except Exception as e:
                print(f"❌ 修复 BROKEN-LINK-FIX-REPORT.md 失败: {e}")
        
        # 修复 CASE-STUDIES.md
        case_file = self.project_root / "CASE-STUDIES.md"
        if case_file.exists():
            try:
                with open(case_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                old_content = content
                content = content.replace(
                    './Flink/07-case-studies/case-realtime-analytics.md',
                    './Flink/09-practices/09.01-case-studies/case-financial-realtime-risk-control.md'
                )
                
                if content != old_content:
                    with open(case_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixes.append(FixResult(str(case_file), 0, "case-realtime-analytics.md", 
                                          "case-financial-realtime-risk-control.md",
                                          "internal", "success"))
                    self.stats['fixes_applied'] += 1
            except Exception as e:
                print(f"❌ 修复 CASE-STUDIES.md 失败: {e}")
        
        # 修复 CHANGELOG.md
        changelog_file = self.project_root / "CHANGELOG.md"
        if changelog_file.exists():
            try:
                with open(changelog_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                old_content = content
                content = content.replace(
                    'FLINK-24-25-30-COMPLETION-REPORT.md',
                    'archive/completion-reports/FLINK-24-25-30-COMPLETION-REPORT.md'
                )
                
                if content != old_content:
                    with open(changelog_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixes.append(FixResult(str(changelog_file), 0, "FLINK-24-25-30-COMPLETION-REPORT.md", 
                                          "archive/completion-reports/FLINK-24-25-30-COMPLETION-REPORT.md",
                                          "internal", "success"))
                    self.stats['fixes_applied'] += 1
            except Exception as e:
                print(f"❌ 修复 CHANGELOG.md 失败: {e}")
        
        return fixes
    
    def run(self, broken_links_json: Optional[Path] = None):
        """运行修复流程"""
        print("=" * 60)
        print("AnalysisDataFlow 断链修复工具")
        print("=" * 60)
        
        # 1. 修复特定已知文件
        print("\n📋 阶段1: 修复已知问题文件...")
        specific_fixes = self.fix_specific_files()
        print(f"   ✅ 已修复 {len(specific_fixes)} 个文件")
        
        # 2. 加载断链数据并处理
        if broken_links_json and broken_links_json.exists():
            print("\n📋 阶段2: 处理断链JSON数据...")
            broken_links = self.load_broken_links(broken_links_json)
            
            # 按文件分组
            by_file = defaultdict(list)
            for item in broken_links:
                source = item.get('source', '')
                if source.startswith('.\\'):
                    source = source[2:]
                by_file[source].append(item)
            
            print(f"   发现 {len(by_file)} 个文件需要处理")
            
            # 处理每个文件
            for file_path_str, items in by_file.items():
                file_path = self.project_root / file_path_str
                if file_path.exists():
                    results = self.process_file(file_path, items)
                    self.fixes.extend(results)
                    self.stats['files_processed'] += 1
                else:
                    # 尝试其他路径格式
                    alt_path = self.project_root / file_path_str.replace('\\', '/')
                    if alt_path.exists():
                        results = self.process_file(alt_path, items)
                        self.fixes.extend(results)
                        self.stats['files_processed'] += 1
        
        # 3. 生成报告
        print("\n📋 阶段3: 生成修复报告...")
        self.generate_reports()
        
        # 4. 输出统计
        print("\n" + "=" * 60)
        print("修复统计")
        print("=" * 60)
        print(f"   处理文件数: {self.stats['files_processed']}")
        print(f"   成功修复: {self.stats['fixes_applied']}")
        print(f"   外部链接修复: {self.stats['external_fixed']}")
        print(f"   跳过(需手动): {self.stats['fixes_skipped']}")
        print(f"   失败: {self.stats['fixes_failed']}")
        print("=" * 60)
        
        return self.stats
    
    def generate_reports(self):
        """生成修复报告"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Markdown 报告
        report_path = REPORTS_DIR / "fix-broken-links-report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 断链修复报告\n\n")
            f.write(f"**生成时间**: {timestamp}\n\n")
            f.write("## 修复统计\n\n")
            f.write("| 指标 | 数量 |\n")
            f.write("|------|------|\n")
            f.write(f"| 处理文件数 | {self.stats['files_processed']} |\n")
            f.write(f"| 成功修复 | {self.stats['fixes_applied']} |\n")
            f.write(f"| 外部链接修复 | {self.stats['external_fixed']} |\n")
            f.write(f"| 跳过(需手动) | {self.stats['fixes_skipped']} |\n")
            f.write(f"| 失败 | {self.stats['fixes_failed']} |\n")
            
            f.write("\n## 修复详情\n\n")
            f.write("### 成功修复的内部链接\n\n")
            f.write("| 文件 | 行号 | 原链接 | 修复后链接 |\n")
            f.write("|------|------|--------|------------|\n")
            
            internal_fixes = [f for f in self.fixes if f.fix_type == 'internal' and f.status == 'success']
            for fix in internal_fixes[:100]:  # 限制显示数量
                f.write(f"| {fix.file_path} | {fix.line_number} | `{fix.original_link[:50]}...` | `{fix.fixed_link[:50]}...` |\n")
            
            if len(internal_fixes) > 100:
                f.write(f"\n... 还有 {len(internal_fixes) - 100} 个修复未显示\n")
            
            f.write("\n### 成功修复的外部链接\n\n")
            f.write("| 文件 | 行号 | 原链接 | 修复后链接 |\n")
            f.write("|------|------|--------|------------|\n")
            
            external_fixes = [f for f in self.fixes if f.fix_type == 'external' and f.status == 'success']
            for fix in external_fixes:
                f.write(f"| {fix.file_path} | {fix.line_number} | `{fix.original_link[:50]}...` | `{fix.fixed_link[:50]}...` |\n")
            
            f.write("\n### 需手动修复的链接\n\n")
            f.write("| 文件 | 行号 | 链接 | 原因 |\n")
            f.write("|------|------|------|------|\n")
            
            manual_fixes = [f for f in self.fixes if f.status == 'skipped']
            for fix in manual_fixes[:50]:  # 限制显示数量
                f.write(f"| {fix.file_path} | {fix.line_number} | `{fix.original_link[:50]}` | {fix.message} |\n")
            
            if len(manual_fixes) > 50:
                f.write(f"\n... 还有 {len(manual_fixes) - 50} 个需手动修复\n")
        
        print(f"   ✅ 报告已生成: {report_path}")
        
        # JSON 报告
        json_report_path = REPORTS_DIR / "fix-broken-links-report.json"
        with open(json_report_path, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': timestamp,
                'stats': self.stats,
                'fixes': [asdict(fix) for fix in self.fixes]
            }, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ JSON报告已生成: {json_report_path}")
        
        # TODO清单
        todo_path = PROJECT_ROOT / "BROKEN-LINKS-TODO.md"
        with open(todo_path, 'w', encoding='utf-8') as f:
            f.write("# 断链修复待办清单\n\n")
            f.write(f"**生成时间**: {timestamp}\n\n")
            f.write("## 需要手动修复的链接\n\n")
            
            manual_fixes = [f for f in self.fixes if f.status == 'skipped']
            by_file = defaultdict(list)
            for fix in manual_fixes:
                by_file[fix.file_path].append(fix)
            
            for file_path, fixes in sorted(by_file.items()):
                f.write(f"\n### {file_path}\n\n")
                for fix in fixes:
                    f.write(f"- [ ] 第 {fix.line_number} 行: `{fix.original_link[:80]}`\n")
                    f.write(f"  - 原因: {fix.message}\n")
        
        print(f"   ✅ 待办清单已生成: {todo_path}")


def main():
    """主函数"""
    fixer = BrokenLinkFixer(PROJECT_ROOT)
    
    # 检查是否有断链JSON文件
    broken_links_json = PROJECT_ROOT / "broken_links_full.json"
    if not broken_links_json.exists():
        broken_links_json = PROJECT_ROOT / "broken_links_real.json"
    
    stats = fixer.run(broken_links_json if broken_links_json.exists() else None)
    
    return 0 if stats['fixes_failed'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
