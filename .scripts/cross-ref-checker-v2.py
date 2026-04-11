#!/usr/bin/env python3
"""
交叉引用自动检查工具 v2.0
功能：
- 扫描所有Markdown文件
- 检查内部链接有效性
- 检查锚点引用正确性
- 生成错误报告

作者: AnalysisDataFlow Toolchain Team
版本: 2.0.0
日期: 2026-04-11
"""

import re
import os
import json
import glob
import hashlib
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import argparse


@dataclass
class CrossRefIssue:
    """交叉引用问题记录"""
    file_path: str
    line_number: int
    issue_type: str  # 'broken_link', 'broken_anchor', 'circular_ref', 'orphaned_file'
    source_link: str
    target_path: str
    anchor: Optional[str]
    severity: str  # 'error', 'warning', 'info'
    suggestion: str


@dataclass
class CheckStats:
    """检查统计"""
    total_files: int
    total_links: int
    broken_links: int
    broken_anchors: int
    circular_refs: int
    orphaned_files: int
    errors: int
    warnings: int
    duration_ms: int


class CrossRefCheckerV2:
    """交叉引用检查器 v2"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        self.issues: List[CrossRefIssue] = []
        self.files_checked = 0
        self.links_checked = 0
        self.file_cache: Dict[str, Path] = {}  # 相对路径 -> 绝对路径
        self.anchor_cache: Dict[str, Set[str]] = {}  # 文件路径 -> 锚点集合
        self.link_graph: Dict[str, Set[str]] = {}  # 文件依赖图
        
    def scan_all_files(self) -> List[Path]:
        """扫描所有Markdown文件"""
        md_files = []
        patterns = [
            "Struct/**/*.md",
            "Knowledge/**/*.md", 
            "Flink/**/*.md",
            "docs/**/*.md",
            "*.md"
        ]
        
        for pattern in patterns:
            files = glob.glob(str(self.base_path / pattern), recursive=True)
            for f in files:
                path = Path(f).resolve()
                if not any(part.startswith('.') for part in path.parts):
                    md_files.append(path)
                    rel_path = str(path.relative_to(self.base_path))
                    self.file_cache[rel_path] = path
                    self.file_cache[rel_path.lower()] = path  # 大小写不敏感缓存
                    
        return list(set(md_files))
    
    def extract_anchors(self, content: str) -> Set[str]:
        """提取文档中的所有锚点"""
        anchors = set()
        
        # 匹配标题锚点
        header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        for match in header_pattern.finditer(content):
            level, title = match.groups()
            # GitHub风格的锚点生成
            anchor = title.strip().lower()
            anchor = re.sub(r'[^\w\s-]', '', anchor)  # 移除非字母数字
            anchor = re.sub(r'[-\s]+', '-', anchor)  # 空格和连字符转为单个连字符
            anchor = anchor.strip('-')
            if anchor:
                anchors.add(anchor)
                
        # 匹配HTML锚点
        html_anchor_pattern = re.compile(r'<a\s+name=["\']([^"\']+)["\']', re.IGNORECASE)
        for match in html_anchor_pattern.finditer(content):
            anchors.add(match.group(1))
            
        return anchors
    
    def build_anchor_cache(self, files: List[Path]):
        """构建锚点缓存"""
        for file_path in files:
            try:
                content = file_path.read_text(encoding='utf-8')
                anchors = self.extract_anchors(content)
                self.anchor_cache[str(file_path)] = anchors
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")
    
    def parse_markdown_links(self, content: str) -> List[Tuple[int, str, str]]:
        """
        解析Markdown链接
        返回: [(行号, 链接文本, 链接目标), ...]
        """
        links = []
        lines = content.split('\n')
        
        # 匹配 [text](url) 格式
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        
        for line_num, line in enumerate(lines, 1):
            for match in link_pattern.finditer(line):
                text, url = match.groups()
                links.append((line_num, text, url))
                
        return links
    
    def resolve_link(self, source_file: Path, link_target: str) -> Tuple[Optional[Path], Optional[str]]:
        """
        解析链接目标
        返回: (目标文件路径, 锚点)
        """
        if '#' in link_target:
            path_part, anchor = link_target.split('#', 1)
        else:
            path_part, anchor = link_target, None
            
        if not path_part:
            # 纯锚点链接，指向同一文件
            return source_file, anchor
            
        # 处理URL协议
        if path_part.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            return None, None  # 外部链接，不检查
            
        # 解析相对路径
        if path_part.startswith('/'):
            # 绝对路径（相对于项目根）
            target = self.base_path / path_part.lstrip('/')
        else:
            # 相对路径
            target = source_file.parent / path_part
            
        try:
            resolved = target.resolve()
            if resolved.exists() and resolved.suffix == '.md':
                return resolved, anchor
        except Exception:
            pass
            
        return None, anchor
    
    def check_circular_reference(self, source: Path, target: Path, 
                                  visited: Set[str] = None) -> bool:
        """检查是否存在循环引用"""
        if visited is None:
            visited = set()
            
        source_str = str(source)
        target_str = str(target)
        
        if target_str in visited:
            return True
            
        visited.add(source_str)
        
        # 递归检查目标文件的链接
        if target_str in self.link_graph:
            for next_target in self.link_graph[target_str]:
                if self.check_circular_reference(target, Path(next_target), visited.copy()):
                    return True
                    
        return False
    
    def check_file(self, file_path: Path) -> List[CrossRefIssue]:
        """检查单个文件"""
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return [CrossRefIssue(
                file_path=str(file_path.relative_to(self.base_path)),
                line_number=0,
                issue_type='read_error',
                source_link='',
                target_path='',
                anchor=None,
                severity='error',
                suggestion=f'无法读取文件: {e}'
            )]
            
        links = self.parse_markdown_links(content)
        file_issues = []
        file_links = set()
        
        for line_num, text, url in links:
            self.links_checked += 1
            
            # 跳过外部链接
            if url.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                continue
                
            target_path, anchor = self.resolve_link(file_path, url)
            
            if target_path is None and not url.startswith('#'):
                # 链接指向的文件不存在
                file_issues.append(CrossRefIssue(
                    file_path=str(file_path.relative_to(self.base_path)),
                    line_number=line_num,
                    issue_type='broken_link',
                    source_link=url,
                    target_path=url.split('#')[0],
                    anchor=anchor,
                    severity='error',
                    suggestion=f'文件不存在: {url.split("#")[0]}'
                ))
            elif target_path is not None:
                file_links.add(str(target_path))
                
                # 检查锚点
                if anchor:
                    file_anchors = self.anchor_cache.get(str(target_path), set())
                    if anchor not in file_anchors:
                        # 尝试小写匹配
                        if anchor.lower() not in {a.lower() for a in file_anchors}:
                            file_issues.append(CrossRefIssue(
                                file_path=str(file_path.relative_to(self.base_path)),
                                line_number=line_num,
                                issue_type='broken_anchor',
                                source_link=url,
                                target_path=str(target_path.relative_to(self.base_path)),
                                anchor=anchor,
                                severity='warning',
                                suggestion=f'锚点不存在: #{anchor}'
                            ))
                            
        # 更新链接图
        self.link_graph[str(file_path)] = file_links
        
        return file_issues
    
    def find_orphaned_files(self, all_files: List[Path]) -> List[CrossRefIssue]:
        """查找孤立文件（没有被引用的文件）"""
        issues = []
        referenced = set()
        
        for source, targets in self.link_graph.items():
            referenced.update(targets)
            
        for file_path in all_files:
            file_str = str(file_path)
            rel_path = str(file_path.relative_to(self.base_path))
            
            # 跳过特定文件
            if any(x in rel_path for x in ['README', 'INDEX', 'TEMPLATE', '_sidebar']):
                continue
                
            if file_str not in referenced and file_str not in self.link_graph:
                issues.append(CrossRefIssue(
                    file_path=rel_path,
                    line_number=0,
                    issue_type='orphaned_file',
                    source_link='',
                    target_path='',
                    anchor=None,
                    severity='info',
                    suggestion='该文件没有被其他文档引用'
                ))
                
        return issues
    
    def run_check(self) -> Tuple[List[CrossRefIssue], CheckStats]:
        """运行完整检查"""
        import time
        start_time = time.time()
        
        print("🔍 Cross-Reference Checker v2.0")
        print("=" * 50)
        
        # 1. 扫描所有文件
        print("\n📁 Scanning Markdown files...")
        all_files = self.scan_all_files()
        print(f"   Found {len(all_files)} Markdown files")
        
        # 2. 构建锚点缓存
        print("\n📋 Building anchor cache...")
        self.build_anchor_cache(all_files)
        print(f"   Cached anchors for {len(self.anchor_cache)} files")
        
        # 3. 检查每个文件
        print("\n🔎 Checking cross-references...")
        all_issues = []
        for i, file_path in enumerate(all_files, 1):
            self.files_checked += 1
            if i % 50 == 0:
                print(f"   Progress: {i}/{len(all_files)} files")
            issues = self.check_file(file_path)
            all_issues.extend(issues)
            
        # 4. 检查循环引用
        print("\n🔄 Checking for circular references...")
        checked_pairs = set()
        for source, targets in self.link_graph.items():
            for target in targets:
                pair = (source, target)
                if pair in checked_pairs:
                    continue
                checked_pairs.add(pair)
                
                if self.check_circular_reference(Path(source), Path(target)):
                    all_issues.append(CrossRefIssue(
                        file_path=str(Path(source).relative_to(self.base_path)),
                        line_number=0,
                        issue_type='circular_ref',
                        source_link='',
                        target_path=str(Path(target).relative_to(self.base_path)),
                        anchor=None,
                        severity='warning',
                        suggestion='检测到循环引用'
                    ))
                    
        # 5. 查找孤立文件
        print("\n📎 Checking for orphaned files...")
        orphaned = self.find_orphaned_files(all_files)
        all_issues.extend(orphaned)
        
        duration = int((time.time() - start_time) * 1000)
        
        # 统计
        stats = CheckStats(
            total_files=self.files_checked,
            total_links=self.links_checked,
            broken_links=len([i for i in all_issues if i.issue_type == 'broken_link']),
            broken_anchors=len([i for i in all_issues if i.issue_type == 'broken_anchor']),
            circular_refs=len([i for i in all_issues if i.issue_type == 'circular_ref']),
            orphaned_files=len([i for i in all_issues if i.issue_type == 'orphaned_file']),
            errors=len([i for i in all_issues if i.severity == 'error']),
            warnings=len([i for i in all_issues if i.severity == 'warning']),
            duration_ms=duration
        )
        
        self.issues = all_issues
        return all_issues, stats
    
    def generate_report(self, output_path: str, stats: CheckStats):
        """生成JSON格式的检查报告"""
        report = {
            'version': '2.0.0',
            'timestamp': str(Path().stat().st_mtime),
            'base_path': str(self.base_path),
            'stats': asdict(stats),
            'issues': [asdict(issue) for issue in self.issues],
            'summary': {
                'total_issues': len(self.issues),
                'by_type': defaultdict(int),
                'by_severity': defaultdict(int),
                'by_directory': defaultdict(int)
            }
        }
        
        for issue in self.issues:
            report['summary']['by_type'][issue.issue_type] += 1
            report['summary']['by_severity'][issue.severity] += 1
            dir_name = issue.file_path.split('/')[0] if '/' in issue.file_path else 'root'
            report['summary']['by_directory'][dir_name] += 1
            
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        return report


def main():
    parser = argparse.ArgumentParser(description='Cross-Reference Checker v2.0')
    parser.add_argument('--base-path', default='.', help='项目根目录')
    parser.add_argument('--output', default='cross-ref-report-v2.json', help='输出报告路径')
    parser.add_argument('--format', choices=['json', 'md'], default='json', help='输出格式')
    parser.add_argument('--fail-on-error', action='store_true', help='发现错误时返回非零退出码')
    
    args = parser.parse_args()
    
    checker = CrossRefCheckerV2(args.base_path)
    issues, stats = checker.run_check()
    
    # 生成报告
    report = checker.generate_report(args.output, stats)
    
    # 打印摘要
    print("\n" + "=" * 50)
    print("📊 CHECK SUMMARY")
    print("=" * 50)
    print(f"Files scanned:      {stats.total_files}")
    print(f"Links checked:      {stats.total_links}")
    print(f"Broken links:       {stats.broken_links}")
    print(f"Broken anchors:     {stats.broken_anchors}")
    print(f"Circular refs:      {stats.circular_refs}")
    print(f"Orphaned files:     {stats.orphaned_files}")
    print(f"Total errors:       {stats.errors}")
    print(f"Total warnings:     {stats.warnings}")
    print(f"Duration:           {stats.duration_ms}ms")
    print("=" * 50)
    print(f"\n✅ Report saved to: {args.output}")
    
    # 返回退出码
    if args.fail_on_error and stats.errors > 0:
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
