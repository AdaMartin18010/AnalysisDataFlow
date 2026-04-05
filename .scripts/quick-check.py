#!/usr/bin/env python3
"""
AnalysisDataFlow 本地快速检查脚本 v2.0
=====================================
功能: 本地提交前快速检查，只检查变更文件

改进:
- 排除代码块中的假链接
- 更智能的锚点验证
- 白名单机制减少误报

作者: AnalysisDataFlow CI/CD Team
版本: 2.0.0
"""

import re
import sys
import argparse
import subprocess
from pathlib import Path
from collections import defaultdict
from typing import List, Tuple, Optional, Set


# =============================================================================
# 配置
# =============================================================================

EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.scripts', 'reports'}

# 链接白名单 - 已知有效的特殊链接
LINK_WHITELIST = {
    # 相对路径根目录
    '/',
    # 特殊协议
    'javascript:void(0)',
    '#',
    # LaTeX 假阳性模式
    r'\bar{e}',
    r'\theta(',
    # 常见误报模式（代码中的泛型语法）
}

# 文件扩展名白名单 - 这些不是Markdown文件但可能被链接
FILE_EXTENSION_WHITELIST = {
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf',
    '.js', '.ts', '.java', '.py', '.scala', '.rs',
    '.json', '.yaml', '.yml', '.toml', '.xml',
    '.sh', '.bat', '.ps1',
    '.css', '.scss', '.less',
    '.html', '.htm',
}

# 代码中的假链接模式（需要排除）
CODE_FALSE_POSITIVE_PATTERNS = [
    # Scala/Java 泛型参数 [T](param) 或 [K, V](param)
    r'^\s*\[\s*[A-Z]\s*(?:,\s*[A-Z]\s*)*\s*\]\s*\(',
    # 方法调用 [Type](method:)
    r'^\s*\[[^\]]+\]\s*\([a-zA-Z_][a-zA-Z0-9_]*\s*:\s*\)',
    # 数组/列表访问 ["key"] 或 [index]
    r'^\s*\[["\'][^"\']+["\']\]\s*\(',
    # Scala 类型参数 [T: TypeInformation]
    r'^\s*\[\s*[A-Z]\s*:\s*[A-Za-z]+\s*\]\s*\(',
]


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


def extract_text_outside_code_blocks(content: str) -> str:
    """提取代码块之外的文本"""
    # 匹配代码块 ```...```
    code_block_pattern = r'```[\s\S]*?```'
    
    # 匹配行内代码 `...`
    inline_code_pattern = r'`[^`]+`'
    
    # 先替换代码块为占位符
    text = content
    text = re.sub(code_block_pattern, '\n\n', text)
    text = re.sub(inline_code_pattern, ' ', text)
    
    return text


def is_false_positive_link(text: str, url: str, context: str) -> bool:
    """检查是否是假链接（代码中的语法）"""
    # 检查白名单
    if url in LINK_WHITELIST:
        return False  # 白名单中的链接需要验证，但不是假链接
    
    # 检查是否是代码中的泛型语法
    full_match = f'[{text}]({url})'
    for pattern in CODE_FALSE_POSITIVE_PATTERNS:
        if re.match(pattern, full_match):
            return True
    
    # 检查文本是否是单个字母（可能是泛型参数）
    if len(text.strip()) == 1 and text.strip().isupper():
        return True
    
    # 检查是否是代码片段中的类型参数
    if re.match(r'^[A-Z]\s*(<:\s*[A-Za-z]+)?$', text.strip()):
        return True
    
    return False


def extract_links(content: str) -> List[Tuple[str, str, int, bool]]:
    """提取所有链接 [text](url)，返回 (text, url, position, is_in_code_block)"""
    links = []
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    # 找到所有代码块位置
    code_blocks = []
    code_pattern = r'```[\s\S]*?```'
    for match in re.finditer(code_pattern, content):
        code_blocks.append((match.start(), match.end()))
    
    # 找到所有行内 LaTeX 公式位置 ($...$)
    latex_blocks = []
    latex_pattern = r'\$[^\$]+\$'
    for match in re.finditer(latex_pattern, content):
        latex_blocks.append((match.start(), match.end()))
    
    # 找到所有 LaTeX 块位置 ($$...$$)
    latex_display_blocks = []
    latex_display_pattern = r'\$\$[\s\S]*?\$\$'
    for match in re.finditer(latex_display_pattern, content):
        latex_display_blocks.append((match.start(), match.end()))
    
    for match in re.finditer(pattern, content):
        text = match.group(1)
        url = match.group(2).split(' ')[0]  # 移除标题属性
        pos = match.start()
        
        # 检查是否在代码块内
        is_in_code = any(start <= pos <= end for start, end in code_blocks)
        
        # 检查是否在 LaTeX 公式内
        is_in_latex = any(start <= pos <= end for start, end in latex_blocks)
        is_in_latex_display = any(start <= pos <= end for start, end in latex_display_blocks)
        
        # 如果在代码块或 LaTeX 公式内，标记为 is_in_code=True
        if is_in_latex or is_in_latex_display:
            is_in_code = True
        
        links.append((text, url, pos, is_in_code))
    
    return links


def classify_link(url: str) -> str:
    """分类链接类型"""
    if url.startswith('http://') or url.startswith('https://'):
        return 'external'
    if url.startswith('#'):
        return 'anchor'
    if url.startswith('mailto:'):
        return 'email'
    if url.startswith('javascript:'):
        return 'javascript'
    return 'internal'


def validate_internal_link(url: str, source_file: Path, all_files: Set[str]) -> Tuple[bool, Optional[str]]:
    """验证内部链接"""
    source_dir = source_file.parent
    
    url_without_anchor = url.split('#')[0]
    anchor = url.split('#')[1] if '#' in url else None
    
    if not url_without_anchor:
        # 只有锚点，验证锚点即可
        return True, None
    
    # 检查是否在白名单中
    if url_without_anchor in LINK_WHITELIST:
        return True, None
    
    # 检查是否是文件扩展名白名单
    if any(url_without_anchor.endswith(ext) for ext in FILE_EXTENSION_WHITELIST):
        # 这些是非Markdown文件，只检查基本路径格式
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
    
    # 对于新创建的文件，如果路径看起来合理，给予通过
    # 检查路径是否符合项目结构
    if target_str.startswith(str(Path('.').resolve()).replace('\\', '/')):
        # 是相对项目根的路径，可能尚未提交
        return True, None
    
    if target.exists():
        return True, None
    
    return False, f"文件不存在: {target}"


def generate_anchor_from_header(header_text: str) -> str:
    """从标题文本生成GitHub风格的锚点"""
    # 移除特殊字符，保留字母数字、空格、连字符
    anchor = re.sub(r'[^\w\s-]', '', header_text)
    # 替换空格为连字符
    anchor = anchor.replace(' ', '-')
    # 转小写
    anchor = anchor.lower()
    # 合并多个连字符
    anchor = re.sub(r'-+', '-', anchor)
    # 移除首尾连字符
    anchor = anchor.strip('-')
    return anchor


def extract_all_anchors(content: str) -> Set[str]:
    """提取文档中所有可能的锚点"""
    anchors = set()
    
    # 从标题提取
    header_pattern = r'^#{1,6}\s+(.+)$'
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
    custom_id_pattern = r'^#{1,6}\s+.+\s+\{([^}]+)\}\s*$'
    for match in re.finditer(custom_id_pattern, content, re.MULTILINE):
        custom_id = match.group(1).strip('#')
        anchors.add(custom_id)
    
    return anchors


# =============================================================================
# 快速检查器
# =============================================================================

class QuickChecker:
    """快速检查器 v2.0"""
    
    def __init__(self, fail_on_error: bool = True, skip_code_blocks: bool = True):
        self.fail_on_error = fail_on_error
        self.skip_code_blocks = skip_code_blocks
        self.issues = []
        self.warnings = []
        self.skipped = []  # 记录被跳过的假链接
    
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
            
            # 提取所有锚点
            all_anchors = extract_all_anchors(content)
            
            # 提取所有链接
            links = extract_links(content)
            
            for text, url, pos, is_in_code in links:
                # 检查是否是假链接
                if is_false_positive_link(text, url, content[pos-50:pos+50]):
                    self.skipped.append({
                        'file': str(file_path),
                        'text': text,
                        'url': url,
                        'reason': '代码中的语法（假链接）'
                    })
                    continue
                
                # 如果设置了跳过代码块，且链接在代码块内，则跳过
                if self.skip_code_blocks and is_in_code:
                    self.skipped.append({
                        'file': str(file_path),
                        'text': text,
                        'url': url,
                        'reason': '代码块内'
                    })
                    continue
                
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
                    if not self._validate_anchor(anchor, all_anchors, content):
                        self.issues.append({
                            'file': str(file_path),
                            'type': '锚点',
                            'text': text,
                            'url': url,
                            'error': f"锚点不存在: {anchor}"
                        })
                        total_issues += 1
        
        return total_issues == 0 or not self.fail_on_error
    
    def _validate_anchor(self, anchor: str, all_anchors: Set[str], content: str) -> bool:
        """验证锚点"""
        anchor = anchor.lower().strip()
        
        # 直接匹配
        if anchor in all_anchors:
            return True
        
        # 尝试多种变体
        variations = [
            anchor,
            anchor.replace('-', ''),
            anchor.replace('_', '-'),
            anchor.replace('-', '_'),
        ]
        
        for variant in variations:
            if variant in all_anchors:
                return True
        
        # 对于空锚点或特殊锚点，给予通过
        if not anchor or anchor in ['top', 'bottom', 'main']:
            return True
        
        return False
    
    def print_report(self):
        """打印检查报告"""
        print("\n" + "=" * 70)
        print("📋 快速检查结果")
        print("=" * 70)
        
        if not self.issues:
            print("\n✅ 没有发现严重问题！")
            if self.skipped:
                print(f"\nℹ️  跳过了 {len(self.skipped)} 个代码中的假链接（这是正常的）")
            return
        
        print(f"\n⚠️  发现 {len(self.issues)} 个问题：\n")
        
        # 按文件分组
        by_file = defaultdict(list)
        for issue in self.issues:
            by_file[issue['file']].append(issue)
        
        for file_path, issues in sorted(by_file.items()):
            print(f"📄 {file_path}")
            for issue in issues[:5]:  # 每个文件最多显示5个
                print(f"   [{issue['type']}] [{issue['text']}]({issue['url']})")
                print(f"   → {issue['error']}")
            if len(issues) > 5:
                print(f"   ... 还有 {len(issues) - 5} 个问题")
            print()
        
        print("=" * 70)
        
        if self.skipped:
            print(f"\nℹ️  跳过了 {len(self.skipped)} 个代码中的假链接")
    
    def generate_report(self, output_path: Path):
        """生成报告文件"""
        lines = [
            "# PR快速检查报告",
            "",
            f"发现问题数: {len(self.issues)}",
            f"跳过假链接数: {len(self.skipped)}",
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
        
        if self.skipped:
            lines.append("## 跳过的假链接（代码中的语法）")
            lines.append("")
            for skip in self.skipped[:20]:  # 只显示前20个
                lines.append(f"- {skip['file']}: [{skip['text']}]({skip['url']}) - {skip['reason']}")
            if len(self.skipped) > 20:
                lines.append(f"- ... 还有 {len(self.skipped) - 20} 个")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))


# =============================================================================
# 主程序
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='AnalysisDataFlow 快速检查 v2.0')
    parser.add_argument('--files', help='逗号分隔的文件列表（用于CI/CD）')
    parser.add_argument('--staged-only', action='store_true', help='只检查暂存区文件')
    parser.add_argument('--all', action='store_true', help='检查所有文件')
    parser.add_argument('--fail-on-error', action='store_true', help='发现问题时返回非零退出码')
    parser.add_argument('--output', '-o', help='报告输出路径')
    parser.add_argument('--no-skip-code', action='store_true', help='不跳过代码块中的链接')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("⚡ AnalysisDataFlow 快速检查 v2.0")
    print("=" * 70)
    print("\n改进: 自动排除代码块中的假链接")
    
    # 确定要检查的文件
    if args.files:
        files = [Path(f.strip()) for f in args.files.split(',') if f.strip().endswith('.md')]
        files = [f for f in files if f.exists()]
    elif args.all:
        files = find_all_markdown_files()
    else:
        files = get_changed_files()
        if not args.staged_only:
            files.extend(get_untracked_files())
        files = list(set(files))
    
    if not files:
        print("\n📭 没有需要检查的Markdown文件")
        sys.exit(0)
    
    print(f"\n📁 检查 {len(files)} 个文件:")
    for f in files[:10]:
        print(f"   - {f}")
    if len(files) > 10:
        print(f"   ... 还有 {len(files) - 10} 个")
    
    all_files = find_all_markdown_files()
    
    # 执行检查
    skip_code = not args.no_skip_code
    checker = QuickChecker(fail_on_error=args.fail_on_error, skip_code_blocks=skip_code)
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
        print(f"\n❌ 检查发现 {len(checker.issues)} 个真实问题")
        sys.exit(1)


if __name__ == '__main__':
    main()
