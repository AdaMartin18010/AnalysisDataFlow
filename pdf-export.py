#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow PDF 导出工具
============================

快速将 Markdown 文档导出为 PDF 格式。
支持单文件导出、批量导出和合并导出。

用法:
    python pdf-export.py single <input.md> [-o output.pdf]
    python pdf-export.py batch <directory> [-o output_dir/]
    python pdf-export.py merge <file1.md> <file2.md> ... [-o merged.pdf]
    python pdf-export.py check

依赖:
    - pandoc >= 2.14
    - xelatex (TeX Live 或 MiKTeX)

示例:
    # 导出单个文件
    python pdf-export.py single README.md
    python pdf-export.py single Struct/00-INDEX.md -o struct-index.pdf

    # 批量导出目录
    python pdf-export.py batch Struct/ -o pdf-output/struct/
    python pdf-export.py batch Knowledge/

    # 合并导出
    python pdf-export.py merge file1.md file2.md -o combined.pdf
    
    # 检查依赖
    python pdf-export.py check
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.absolute()
OUTPUT_DIR = PROJECT_ROOT / "pdf-output"

# 版本信息
VERSION = "1.1.0"


def check_dependencies() -> bool:
    """
    检查必需的依赖是否已安装
    
    Returns:
        bool: 所有依赖是否都已安装
    """
    deps = {
        "pandoc": shutil.which("pandoc"), 
        "xelatex": shutil.which("xelatex")
    }
    
    all_installed = all(deps.values())
    
    if not all_installed:
        print("❌ 缺少必需的依赖:")
        if not deps["pandoc"]:
            print("  - pandoc: https://pandoc.org/installing.html")
        if not deps["xelatex"]:
            print("  - xelatex: 安装 TeX Live (https://tug.org/texlive/) 或 MiKTeX")
        print("\n安装指南:")
        print("  Ubuntu/Debian: sudo apt-get install pandoc texlive-xetex")
        print("  macOS: brew install pandoc --cask mactex")
        print("  Windows: choco install pandoc miktex")
    else:
        print("✓ 所有依赖已安装")
        for name, path in deps.items():
            try:
                if name == "pandoc":
                    result = subprocess.run(
                        [path, "--version"], 
                        capture_output=True, 
                        text=True, 
                        timeout=10
                    )
                    version = result.stdout.split('\n')[0] if result.stdout else "未知版本"
                    print(f"  - {name}: {version}")
                else:
                    print(f"  - {name}: {path}")
            except (subprocess.TimeoutExpired, OSError) as e:
                print(f"  - {name}: {path} (获取版本失败: {e})")
    
    return all_installed


def get_latex_template() -> str:
    """
    获取基础 LaTeX 模板
    
    Returns:
        str: LaTeX 模板字符串
    """
    return r'''
\documentclass[11pt,a4paper]{article}
\usepackage[UTF8]{ctex}
\usepackage{fontspec}
\usepackage{geometry}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{listings}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{fancyhdr}

% 页面设置
\geometry{margin=2.5cm}

% 颜色定义
\definecolor{linkblue}{RGB}{0,82,147}
\hypersetup{
    colorlinks=true,
    linkcolor=linkblue,
    urlcolor=linkblue,
    bookmarks=true
}

% 代码高亮设置
\lstset{
    basicstyle=\ttfamily\small,
    breaklines=true,
    frame=single,
    numbers=left,
    numberstyle=\tiny\color{gray},
    showstringspaces=false,
    tabsize=2,
    captionpos=b
}

% 页眉页脚设置
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\leftmark}
\fancyhead[R]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

$if(title)$
\title{$title$}
$endif$
$if(author)$
\author{$author$}
$endif$
$if(date)$
\date{$date$}
$endif$

\begin{document}
$if(title)$
\maketitle
$endif$
$if(toc)$
\tableofcontents
\newpage
$endif$
$body$
\end{document}
'''


def parse_markdown_metadata(content: str) -> Tuple[str, str, str]:
    """
    解析 Markdown 文件中的元数据（标题、作者、日期）
    
    Args:
        content: Markdown 文件内容
    
    Returns:
        Tuple[str, str, str]: (标题, 作者, 日期)
    """
    title = ""
    author = ""
    date = datetime.now().strftime("%Y-%m-%d")
    
    # 尝试从 YAML front matter 提取元数据
    yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if yaml_match:
        yaml_content = yaml_match.group(1)
        title_match = re.search(r'^title:\s*(.+)$', yaml_content, re.MULTILINE)
        author_match = re.search(r'^author:\s*(.+)$', yaml_content, re.MULTILINE)
        date_match = re.search(r'^date:\s*(.+)$', yaml_content, re.MULTILINE)
        
        if title_match:
            title = title_match.group(1).strip('"\'')
        if author_match:
            author = author_match.group(1).strip('"\'')
        if date_match:
            date = date_match.group(1).strip('"\'')
    
    # 如果没有从 YAML 提取到标题，尝试从第一个 # 标题提取
    if not title:
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
    
    return title, author, date


def export_single(
    input_file: Path, 
    output_file: Optional[Path] = None,
    verbose: bool = False
) -> bool:
    """
    导出单个 Markdown 文件为 PDF
    
    Args:
        input_file: 输入 Markdown 文件路径
        output_file: 输出 PDF 文件路径（可选）
        verbose: 是否显示详细输出
    
    Returns:
        bool: 是否成功导出
    """
    # 验证输入文件
    if not input_file.exists():
        print(f"❌ 文件不存在: {input_file}")
        return False
    
    if not input_file.is_file():
        print(f"❌ 路径不是文件: {input_file}")
        return False
    
    # 自动确定输出路径
    if output_file is None:
        output_file = OUTPUT_DIR / f"{input_file.stem}.pdf"
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"📄 导出: {input_file.name} -> {output_file.name}")
    
    # 读取并解析 Markdown 内容
    try:
        md_content = input_file.read_text(encoding='utf-8')
        title, author, date = parse_markdown_metadata(md_content)
    except (IOError, UnicodeDecodeError) as e:
        print(f"⚠️  读取文件时出错: {e}")
        title, author, date = input_file.stem, "", datetime.now().strftime("%Y-%m-%d")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # 创建模板文件
        template_file = temp_path / "template.tex"
        template_file.write_text(get_latex_template(), encoding='utf-8')
        
        # 构建 pandoc 命令
        cmd = [
            "pandoc",
            str(input_file),
            "-o", str(output_file),
            "--pdf-engine=xelatex",
            "--template", str(template_file),
            "--toc",
            "--toc-depth=3",
            "--number-sections",
            "--highlight-style=tango",
            "-V", "geometry:margin=2.5cm",
            "-V", "colorlinks=true",
            "-V", "CJKmainfont=Noto Sans CJK SC"
        ]
        
        # 添加元数据变量
        if title:
            cmd.extend(["-V", f"title={title}"])
        if author:
            cmd.extend(["-V", f"author={author}"])
        if date:
            cmd.extend(["-V", f"date={date}"])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=temp_dir,
                timeout=300,  # 5分钟超时
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode == 0:
                print(f"✅ 成功导出: {output_file}")
                try:
                    file_size = output_file.stat().st_size / 1024
                    print(f"   文件大小: {file_size:.1f} KB")
                except OSError:
                    pass
                
                if verbose:
                    print(f"   标题: {title or '未提取'}")
                    print(f"   作者: {author or '未提取'}")
                
                return True
            else:
                print(f"❌ 导出失败:")
                print(f"   {result.stderr[:500] if result.stderr else '未知错误'}")
                
                # 清理失败的输出文件
                if output_file.exists():
                    output_file.unlink()
                
                return False
                
        except subprocess.TimeoutExpired:
            print(f"❌ 导出超时（超过5分钟）")
            return False
        except OSError as e:
            print(f"❌ 导出错误: {e}")
            return False


def export_batch(
    input_dir: Path, 
    output_dir: Optional[Path] = None,
    verbose: bool = False
) -> int:
    """
    批量导出目录中的所有 Markdown 文件
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录（可选）
        verbose: 是否显示详细输出
    
    Returns:
        int: 成功导出的文件数量
    """
    # 验证输入目录
    if not input_dir.exists():
        print(f"❌ 目录不存在: {input_dir}")
        return 0
    
    if not input_dir.is_dir():
        print(f"❌ 路径不是目录: {input_dir}")
        return 0
    
    if output_dir is None:
        output_dir = OUTPUT_DIR / input_dir.name
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 查找所有 Markdown 文件（排除隐藏目录和特定目录）
    exclude_dirs = {'.git', '.github', 'node_modules', '__pycache__', 
                    '.vscode', '.idea'}
    md_files = [
        f for f in input_dir.rglob("*.md")
        if not any(excluded in f.parts for excluded in exclude_dirs)
    ]
    
    if not md_files:
        print(f"⚠️  在 {input_dir} 中未找到 Markdown 文件")
        return 0
    
    print(f"\n📁 批量导出: {input_dir}")
    print(f"   找到 {len(md_files)} 个 Markdown 文件")
    print(f"   输出目录: {output_dir}\n")
    
    success_count = 0
    failed_files = []
    
    for i, md_file in enumerate(md_files, 1):
        # 保持目录结构
        try:
            relative_path = md_file.relative_to(input_dir)
        except ValueError:
            relative_path = Path(md_file.name)
        
        out_file = output_dir / relative_path.with_suffix(".pdf")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"[{i}/{len(md_files)}] ", end="")
        if export_single(md_file, out_file, verbose=verbose):
            success_count += 1
        else:
            failed_files.append(str(relative_path))
    
    # 打印总结
    print(f"\n{'='*50}")
    print(f"批量导出完成: {success_count}/{len(md_files)} 成功")
    
    if failed_files:
        print(f"\n失败的文件 ({len(failed_files)} 个):")
        for f in failed_files[:10]:  # 最多显示10个
            print(f"  - {f}")
        if len(failed_files) > 10:
            print(f"  ... 还有 {len(failed_files) - 10} 个")
    
    print(f"输出目录: {output_dir}")
    
    return success_count


def export_merge(
    input_files: List[Path], 
    output_file: Path,
    add_page_breaks: bool = True,
    verbose: bool = False
) -> bool:
    """
    合并多个 Markdown 文件为一个 PDF
    
    Args:
        input_files: 输入文件列表
        output_file: 输出 PDF 文件路径
        add_page_breaks: 是否在文档间添加分页符
        verbose: 是否显示详细输出
    
    Returns:
        bool: 是否成功导出
    """
    if not input_files:
        print("❌ 未提供输入文件")
        return False
    
    # 验证所有输入文件
    valid_files = []
    for f in input_files:
        if f.exists() and f.is_file():
            valid_files.append(f)
        else:
            print(f"⚠️  跳过不存在的文件: {f}")
    
    if not valid_files:
        print("❌ 没有有效的输入文件")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📚 合并导出 {len(valid_files)} 个文件 -> {output_file.name}\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # 合并文件内容
        merged_content = []
        for i, md_file in enumerate(valid_files, 1):
            print(f"  [{i}/{len(valid_files)}] 添加: {md_file.name}")
            
            try:
                content = md_file.read_text(encoding='utf-8')
            except (IOError, UnicodeDecodeError) as e:
                print(f"      ⚠️  读取失败: {e}")
                continue
            
            # 添加文档标题（如果不是以标题开头）
            if not content.strip().startswith('#'):
                content = f"# {md_file.stem.replace('-', ' ').title()}\n\n{content}"
            
            merged_content.append(content)
            
            # 添加分页符（除了最后一个文件）
            if add_page_breaks and i < len(valid_files):
                merged_content.append("\n\n\\newpage\n\n")
        
        if not merged_content:
            print("❌ 没有可合并的内容")
            return False
        
        # 写入合并后的文件
        merged_file = temp_path / "merged.md"
        try:
            merged_file.write_text("\n".join(merged_content), encoding='utf-8')
        except IOError as e:
            print(f"❌ 写入合并文件失败: {e}")
            return False
        
        # 导出合并后的文件
        return export_single(merged_file, output_file, verbose=verbose)


def main() -> int:
    """主函数 - 命令行入口"""
    parser = argparse.ArgumentParser(
        description="AnalysisDataFlow PDF 导出工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 导出单个文件
  python pdf-export.py single README.md
  python pdf-export.py single Struct/00-INDEX.md -o struct-index.pdf

  # 批量导出目录
  python pdf-export.py batch Struct/ -o pdf-output/struct/
  python pdf-export.py batch Knowledge/

  # 合并多个文件
  python pdf-export.py merge file1.md file2.md file3.md -o combined.pdf
  
  # 合并时不添加分页符
  python pdf-export.py merge file1.md file2.md -o combined.pdf --no-page-breaks

  # 检查依赖
  python pdf-export.py check

  # 显示详细输出
  python pdf-export.py single README.md -v
        """
    )
    
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="显示详细输出"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # single 命令
    single_parser = subparsers.add_parser("single", help="导出单个文件")
    single_parser.add_argument("input", type=Path, help="输入 Markdown 文件")
    single_parser.add_argument("-o", "--output", type=Path, help="输出 PDF 文件")
    
    # batch 命令
    batch_parser = subparsers.add_parser("batch", help="批量导出目录")
    batch_parser.add_argument("input", type=Path, help="输入目录")
    batch_parser.add_argument("-o", "--output", type=Path, help="输出目录")
    
    # merge 命令
    merge_parser = subparsers.add_parser("merge", help="合并导出多个文件")
    merge_parser.add_argument("files", nargs="+", type=Path, help="输入文件列表")
    merge_parser.add_argument(
        "-o", "--output", type=Path, required=True, help="输出 PDF 文件"
    )
    merge_parser.add_argument(
        "--no-page-breaks", 
        action="store_true", 
        help="不在文档间添加分页符"
    )
    
    # check 命令
    subparsers.add_parser("check", help="检查依赖环境")
    
    # 版本信息
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # 检查依赖命令
    if args.command == "check":
        return 0 if check_dependencies() else 1
    
    # 检查核心依赖
    if not shutil.which("pandoc") or not shutil.which("xelatex"):
        print("❌ 缺少必需依赖 (pandoc 或 xelatex)")
        print("请运行: python pdf-export.py check")
        return 1
    
    # 执行命令
    verbose = getattr(args, 'verbose', False)
    
    try:
        if args.command == "single":
            success = export_single(args.input, args.output, verbose=verbose)
            return 0 if success else 1
        
        elif args.command == "batch":
            count = export_batch(args.input, args.output, verbose=verbose)
            return 0 if count > 0 else 1
        
        elif args.command == "merge":
            add_page_breaks = not args.no_page_breaks
            success = export_merge(
                args.files, args.output, add_page_breaks, verbose=verbose
            )
            return 0 if success else 1
        
        else:
            parser.print_help()
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⚠️  操作被用户中断")
        return 130
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
