#!/usr/bin/env python3
"""
AnalysisDataFlow 本地快速检查脚本
=================================
功能: 本地提交前快速检查，只检查变更文件

特点:
- 快速（<30秒）
- 只检查变更文件
- 适合预提交钩子使用

作者: AnalysisDataFlow CI/CD Team
版本: 1.0.0
"""

import re
import sys
import argparse
import subprocess
from pathlib import Path
from collections import defaultdict
from typing import List, Tuple, Optional


# =============================================================================
# 配置
# =============================================================================

EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.scripts', 'reports'}


# =============================================================================
# 工具函数
# =============================================================================

def get_changed_files() -> List[Path]:
    """获取Git变更的文件列表"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True,
            text=True,
            check=True
        )
        files = [Path(f) for f in result.stdout.strip().split('\n') if f.endswith('.md')]
        return [f for f in files if f.exists()]
    except subprocess.CalledProcessError:
        return []


def get_untracked_files() -> List[Path]:
    """获取未跟踪的文件列表"""
    try:
        result = subprocess.run(
            ['git', 'ls-files', '--others', '--exclude-standard'],
            capture_output=True,
            text=True,
            check=True
        )
        files = [Path(f) for f in result.stdout.strip().split('\n') if f.endswith('.md')]
        return [f for f in files if f.exists()]
    except subprocess.CalledProcessError:
        return []


def find_all_markdown_files() -> List[Path]:
    """获取所有Markdown文件（用于验证目标）"""
    md_files = []
    for f in Path('.').rglob('*.md'):
        if not any(part in EXCLUDE_DIRS for part in f.parts):
            md_files.append(f)
    return md_files


def extract_links(content: str) -> List[Tuple[str, str, int]]:
    """提取所有链接 [text](url)"""
    links = []
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    for match in re.finditer(pattern, content):
        text = match.group(1)
        url = match.group(2).split(' ')[0]
        links.append((text, url, match.start()))
    return links


def classify_link(url: str) -> str:
    """分类链接类型"""
    if url.startswith('http://') or url.startswith('https://'):
        return 'external'
    if url.startswith('#'):
        return 'anchor'
    if url.startswith('mailto:'):
        return 'email'
    return 'internal'


def validate_internal_link(url: str, source_file: Path, all_files: set) -> Tuple[bool, Optional[str]]:
    """验证内部链接"""
    source_dir = source_file.parent
    
    url_without_anchor = url.split('#')[0]
    if not url_without_anchor:
        return True, None
    
    if url_without_anchor.startswith('/'):
        target = Path('.') / url_without_anchor.lstrip('/')
    else:
        target = source_dir / url_without_anchor
    
    target = target.resolve()
    target_str = str(target).replace('\\', '/')
    
    # 检查各种可能的路径
    if target_str in all_files:
        return True, None
    
    target_with_md = Path(str(target) + '.md')
    if str(target_with_md).replace('\\', '/') in all_files:
        return True, None
    
    target_index = target / 'index.md'
    if str(target_index).replace('\\', '/') in all_files:
        return True, None
    
    if target.exists():
        return True, None
    
    return False, f"文件不存在: {target}"


# =============================================================================
# 快速检查器
# =============================================================================

class QuickChecker:
    """快速检查器"""
    
    def __init__(self, fail_on_error: bool = True):
        self.fail_on_error = fail_on_error
        self.issues = []
        self.warnings = []
    
    def check_files(self, files: List[Path], all_files: List[Path]) -> bool:
        """检查指定文件"""
        all_files_set = set(str(f).replace('\\', '/') for f in all_files)
        
        total_issues = 0
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                self.warnings.append(f"无法读取 {file_path}: {e}")
                continue
            
            links = extract_links(content)
            
            for text, url, pos in links:
                link_type = classify_link(url)
                
                if link_type == 'internal':
                    is_valid, error = validate_internal_link(url, file_path, all_files_set)
                    if not is_valid:
                        self.issues.append({
                            'file': str(file_path),
                            'type': '内部链接',
                            'text': text,
                            'url': url,
                            'error': error
                        })
                        total_issues += 1
                
                elif link_type == 'anchor':
                    anchor = url[1:] if url.startswith('#') else url.split('#')[1]
                    if not self._validate_anchor(content, anchor):
                        self.issues.append({
                            'file': str(file_path),
                            'type': '锚点',
                            'text': text,
                            'url': url,
                            'error': f"锚点不存在: {anchor}"
                        })
                        total_issues += 1
        
        return total_issues == 0 or not self.fail_on_error
    
    def _validate_anchor(self, content: str, anchor: str) -> bool:
        """验证锚点"""
        anchor = anchor.lower().replace(' ', '-')
        
        # 检查标题
        header_pattern = r'^#{1,6}\s+(.+)$'
        for match in re.finditer(header_pattern, content, re.MULTILINE):
            header_text = match.group(1).strip()
            header_anchor = re.sub(r'[^\w\s-]', '', header_text).lower().replace(' ', '-')
            if header_anchor == anchor:
                return True
        
        # 检查自定义锚点
        anchor_pattern = r'<a\s+name=["\']([^"\']+)["\']'
        for match in re.finditer(anchor_pattern, content):
            if match.group(1) == anchor:
                return True
        
        return False
    
    def print_report(self):
        """打印检查报告"""
        print("\n" + "=" * 70)
        print("📋 快速检查结果")
        print("=" * 70)
        
        if not self.issues:
            print("\n✅ 没有发现任何问题！")
            return
        
        print(f"\n⚠️  发现 {len(self.issues)} 个问题：\n")
        
        # 按文件分组
        by_file = defaultdict(list)
        for issue in self.issues:
            by_file[issue['file']].append(issue)
        
        for file_path, issues in sorted(by_file.items()):
            print(f"📄 {file_path}")
            for issue in issues:
                print(f"   [{issue['type']}] [{issue['text']}]({issue['url']})")
                print(f"   → {issue['error']}")
            print()
        
        print("=" * 70)
    
    def generate_report(self, output_path: Path):
        """生成报告文件"""
        lines = [
            "# PR快速检查报告",
            "",
            f"发现问题数: {len(self.issues)}",
            "",
            "## 问题详情",
            "",
        ]
        
        for issue in self.issues:
            lines.append(f"- **{issue['file']}**")
            lines.append(f"  - 类型: {issue['type']}")
            lines.append(f"  - 链接: [{issue['text']}]({issue['url']})")
            lines.append(f"  - 错误: {issue['error']}")
            lines.append("")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))


# =============================================================================
# 主程序
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='AnalysisDataFlow 快速检查')
    parser.add_argument('--files', help='逗号分隔的文件列表（用于CI/CD）')
    parser.add_argument('--staged-only', action='store_true', help='只检查暂存区文件')
    parser.add_argument('--all', action='store_true', help='检查所有文件')
    parser.add_argument('--fail-on-error', action='store_true', help='发现问题时返回非零退出码')
    parser.add_argument('--output', '-o', help='报告输出路径')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("⚡ AnalysisDataFlow 快速检查")
    print("=" * 70)
    
    # 确定要检查的文件
    if args.files:
        # CI/CD模式
        files = [Path(f.strip()) for f in args.files.split(',') if f.strip().endswith('.md')]
        files = [f for f in files if f.exists()]
    elif args.all:
        files = find_all_markdown_files()
    else:
        # 本地模式：检查暂存区和未跟踪的文件
        files = get_changed_files()
        if not args.staged_only:
            files.extend(get_untracked_files())
        files = list(set(files))  # 去重
    
    if not files:
        print("\n📭 没有需要检查的Markdown文件")
        sys.exit(0)
    
    print(f"\n📁 检查 {len(files)} 个文件:")
    for f in files[:10]:
        print(f"   - {f}")
    if len(files) > 10:
        print(f"   ... 还有 {len(files) - 10} 个")
    
    # 获取所有文件用于验证
    all_files = find_all_markdown_files()
    
    # 执行检查
    checker = QuickChecker(fail_on_error=args.fail_on_error)
    passed = checker.check_files(files, all_files)
    
    # 打印报告
    checker.print_report()
    
    # 生成报告文件
    if args.output:
        checker.generate_report(Path(args.output))
    
    if passed and not checker.issues:
        print("\n✅ 检查通过！")
        sys.exit(0)
    elif not checker.issues:
        print("\n⚠️  检查完成，但有问题被忽略")
        sys.exit(0)
    else:
        print("\n❌ 检查发现问题")
        sys.exit(1)


if __name__ == '__main__':
    main()
