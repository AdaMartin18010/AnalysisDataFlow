#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow PDF 导出工具
PDF Export Tool for AnalysisDataFlow Project

功能:
- 单文档导出
- 批量目录导出
- 多文档合并导出
- Mermaid图表转换
- 自动生成目录和页眉页脚

依赖:
- pandoc
- xelatex (TeX Live 或 MiKTeX)
- mmdc (Mermaid CLI, 可选)
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import yaml

# =============================================================================
# 配置常量
# =============================================================================

SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_FILE = SCRIPT_DIR / "pdf-config.yaml"
TEMPLATE_FILE = SCRIPT_DIR / "pdf-template.tex"
OUTPUT_DIR = PROJECT_ROOT / "pdf-output"

DEFAULT_CONFIG = {
    "page": {"size": "a4", "margin": {"top": 25, "bottom": 25, "left": 30, "right": 25}},
    "fonts": {"main": "Latin Modern Roman", "chinese": {"main": "Source Han Serif SC"}},
    "table_of_contents": {"enabled": True, "depth": 3},
    "code_blocks": {"highlight_theme": "tango", "line_numbers": True},
    "mermaid": {"renderer": "mmdc", "output_format": "png", "dpi": 150},
}

# =============================================================================
# 工具函数
# =============================================================================

def log(message: str, level: str = "INFO"):
    """打印日志消息"""
    colors = {
        "INFO": "\033[94m",      # Blue
        "SUCCESS": "\033[92m",   # Green
        "WARNING": "\033[93m",   # Yellow
        "ERROR": "\033[91m",     # Red
        "RESET": "\033[0m"
    }
    color = colors.get(level, colors["INFO"])
    reset = colors["RESET"]
    print(f"{color}[{level}]{reset} {message}")


def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                log(f"已加载配置文件: {CONFIG_FILE}")
                return config
        except Exception as e:
            log(f"配置文件加载失败: {e}", "WARNING")
    log("使用默认配置", "WARNING")
    return DEFAULT_CONFIG


def check_dependencies() -> Dict[str, bool]:
    """检查依赖是否安装"""
    deps = {
        "pandoc": False,
        "xelatex": False,
        "mmdc": False,
    }
    
    # 检查 pandoc
    if shutil.which("pandoc"):
        deps["pandoc"] = True
        try:
            result = subprocess.run(["pandoc", "--version"], 
                                  capture_output=True, text=True, check=True)
            version = result.stdout.split('\n')[0]
            log(f"pandoc: {version}")
        except:
            pass
    else:
        log("未找到 pandoc，请先安装", "ERROR")
    
    # 检查 xelatex
    if shutil.which("xelatex"):
        deps["xelatex"] = True
        try:
            result = subprocess.run(["xelatex", "--version"], 
                                  capture_output=True, text=True, check=True)
            version = result.stdout.split('\n')[0]
            log(f"xelatex: {version}")
        except:
            pass
    else:
        log("未找到 xelatex，请先安装 TeX Live 或 MiKTeX", "ERROR")
    
    # 检查 mmdc (可选)
    if shutil.which("mmdc"):
        deps["mmdc"] = True
        log("mmdc (Mermaid CLI): 已安装")
    else:
        log("mmdc (Mermaid CLI): 未安装，Mermaid图表将被保留为代码块", "WARNING")
    
    return deps


def extract_mermaid_diagrams(content: str) -> tuple:
    """
    提取 Mermaid 图表
    返回: (处理后的内容, 图表列表)
    """
    mermaid_pattern = r'```mermaid\s*\n(.*?)```'
    diagrams = []
    
    def replace_mermaid(match):
        diagram_id = len(diagrams)
        diagram_code = match.group(1).strip()
        diagrams.append({
            'id': diagram_id,
            'code': diagram_code
        })
        # 返回占位符
        return f"MERMAID_DIAGRAM_PLACEHOLDER_{diagram_id}"
    
    processed_content = re.sub(mermaid_pattern, replace_mermaid, content, flags=re.DOTALL)
    return processed_content, diagrams


def render_mermaid_diagram(diagram: Dict, output_dir: Path, dpi: int = 150) -> Optional[Path]:
    """
    渲染单个 Mermaid 图表为图片
    """
    if not shutil.which("mmdc"):
        return None
    
    diagram_file = output_dir / f"mermaid_{diagram['id']}.mmd"
    output_file = output_dir / f"mermaid_{diagram['id']}.png"
    
    # 写入临时 mermaid 文件
    with open(diagram_file, "w", encoding="utf-8") as f:
        f.write(diagram['code'])
    
    try:
        cmd = [
            "mmdc",
            "-i", str(diagram_file),
            "-o", str(output_file),
            "-b", "white",
            "-s", "2"
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        
        if output_file.exists():
            log(f"  渲染图表 {diagram['id']}: {output_file.name}")
            return output_file
    except subprocess.CalledProcessError as e:
        log(f"  图表 {diagram['id']} 渲染失败: {e}", "WARNING")
    
    return None


def process_mermaid_diagrams(content: str, temp_dir: Path, dpi: int = 150) -> str:
    """
    处理内容中的所有 Mermaid 图表
    """
    processed_content, diagrams = extract_mermaid_diagrams(content)
    
    if not diagrams:
        return content
    
    log(f"发现 {len(diagrams)} 个 Mermaid 图表")
    
    for diagram in diagrams:
        image_path = render_mermaid_diagram(diagram, temp_dir, dpi)
        
        if image_path:
            # 替换为图片引用
            placeholder = f"MERMAID_DIAGRAM_PLACEHOLDER_{diagram['id']}"
            relative_path = image_path.name
            image_markdown = f"\n![Mermaid Diagram {diagram['id']}]({relative_path})\n"
            processed_content = processed_content.replace(placeholder, image_markdown)
        else:
            # 保留原始代码块
            placeholder = f"MERMAID_DIAGRAM_PLACEHOLDER_{diagram['id']}"
            original_code = f"```mermaid\n{diagram['code']}\n```"
            processed_content = processed_content.replace(placeholder, original_code)
    
    return processed_content


def preprocess_markdown(content: str, file_path: Path) -> str:
    """
    预处理 Markdown 内容
    - 修复相对路径
    - 处理定理/定义框
    """
    # 处理定理/定义框标记
    # Thm-xxx 标记转换为 LaTeX 环境
    theorem_pattern = r'(Thm-[A-Z]-\d{2}-\d{2})'
    content = re.sub(theorem_pattern, r'**\1**', content)
    
    # 修复相对链接为绝对路径
    # 这里简化处理，实际使用时可增强
    
    return content


def build_pandoc_args(config: Dict, template_path: Path, 
                      output_path: Path, with_toc: bool = True) -> List[str]:
    """
    构建 pandoc 命令参数
    """
    args = [
        "pandoc",
        "--pdf-engine=xelatex",
        "--template", str(template_path),
        "-o", str(output_path),
        "--highlight-style", config.get("code_blocks", {}).get("highlight_theme", "tango"),
        "--number-sections",
    ]
    
    # 目录设置
    if with_toc and config.get("table_of_contents", {}).get("enabled", True):
        args.append("--toc")
        depth = config.get("table_of_contents", {}).get("depth", 3)
        args.extend(["--toc-depth", str(depth)])
    
    # 页面设置
    margin = config.get("page", {}).get("margin", {})
    geometry = []
    if margin.get("top"):
        geometry.append(f"top={margin['top']}mm")
    if margin.get("bottom"):
        geometry.append(f"bottom={margin['bottom']}mm")
    if margin.get("left"):
        geometry.append(f"left={margin['left']}mm")
    if margin.get("right"):
        geometry.append(f"right={margin['right']}mm")
    
    if geometry:
        args.extend(["-V", f"geometry={','.join(geometry)}"])
    
    # LaTeX 额外选项
    args.extend([
        "-V", "colorlinks=true",
        "-V", "linkcolor=ADFPrimary",
    ])
    
    return args


# =============================================================================
# 导出功能
# =============================================================================

def export_single(input_file: Path, output_file: Optional[Path] = None,
                  config: Optional[Dict] = None, with_mermaid: bool = True) -> bool:
    """
    导出单个 Markdown 文件为 PDF
    
    Args:
        input_file: 输入 Markdown 文件路径
        output_file: 输出 PDF 文件路径（可选，默认自动生成）
        config: 配置字典（可选）
        with_mermaid: 是否处理 Mermaid 图表
    
    Returns:
        是否成功
    """
    if not input_file.exists():
        log(f"文件不存在: {input_file}", "ERROR")
        return False
    
    if config is None:
        config = load_config()
    
    # 自动确定输出路径
    if output_file is None:
        output_file = OUTPUT_DIR / f"{input_file.stem}.pdf"
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    log(f"导出: {input_file.name} -> {output_file.name}")
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # 读取并预处理内容
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 预处理
        content = preprocess_markdown(content, input_file)
        
        # 处理 Mermaid 图表
        if with_mermaid and shutil.which("mmdc"):
            content = process_mermaid_diagrams(content, temp_path, 
                config.get("mermaid", {}).get("dpi", 150))
        
        # 写入临时 markdown 文件
        temp_md = temp_path / "input.md"
        with open(temp_md, "w", encoding="utf-8") as f:
            f.write(content)
        
        # 复制图片到临时目录
        img_dir = input_file.parent / "images"
        if img_dir.exists():
            for img in img_dir.glob("*"):
                shutil.copy2(img, temp_path / img.name)
        
        # 构建并执行 pandoc 命令
        args = build_pandoc_args(config, TEMPLATE_FILE, output_file)
        args.append(str(temp_md))
        
        try:
            result = subprocess.run(args, capture_output=True, text=True, cwd=temp_dir)
            if result.returncode != 0:
                log(f"pandoc 错误:\n{result.stderr}", "ERROR")
                return False
            
            log(f"成功导出: {output_file}", "SUCCESS")
            return True
            
        except Exception as e:
            log(f"导出失败: {e}", "ERROR")
            return False


def export_batch(input_dir: Path, output_dir: Optional[Path] = None,
                 pattern: str = "*.md", config: Optional[Dict] = None,
                 preserve_structure: bool = True) -> List[Path]:
    """
    批量导出目录中的 Markdown 文件
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        pattern: 文件匹配模式
        config: 配置字典
        preserve_structure: 是否保留目录结构
    
    Returns:
        成功导出的文件列表
    """
    if not input_dir.exists():
        log(f"目录不存在: {input_dir}", "ERROR")
        return []
    
    if config is None:
        config = load_config()
    
    if output_dir is None:
        output_dir = OUTPUT_DIR / input_dir.name
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 查找所有匹配的文件
    md_files = list(input_dir.rglob(pattern))
    log(f"在 {input_dir} 中找到 {len(md_files)} 个 Markdown 文件")
    
    exported = []
    for i, md_file in enumerate(md_files, 1):
        if preserve_structure:
            relative = md_file.relative_to(input_dir)
            out_file = output_dir / relative.with_suffix(".pdf")
            out_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            out_file = output_dir / f"{md_file.stem}.pdf"
        
        log(f"[{i}/{len(md_files)}] 处理: {md_file.relative_to(input_dir)}")
        
        if export_single(md_file, out_file, config):
            exported.append(out_file)
    
    log(f"批量导出完成: {len(exported)}/{len(md_files)} 成功", "SUCCESS")
    return exported


def export_merge(input_files: List[Path], output_file: Path,
                 config: Optional[Dict] = None, 
                 page_break_between: bool = True) -> bool:
    """
    合并多个 Markdown 文件为一个 PDF
    
    Args:
        input_files: 输入文件列表
        output_file: 输出 PDF 文件
        config: 配置字典
        page_break_between: 文档间是否添加分页
    
    Returns:
        是否成功
    """
    if not input_files:
        log("没有输入文件", "ERROR")
        return False
    
    if config is None:
        config = load_config()
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    log(f"合并导出 {len(input_files)} 个文档 -> {output_file.name}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        merged_content = []
        
        for i, md_file in enumerate(input_files):
            if not md_file.exists():
                log(f"跳过不存在的文件: {md_file}", "WARNING")
                continue
            
            log(f"  [{i+1}/{len(input_files)}] 合并: {md_file.name}")
            
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 预处理
            content = preprocess_markdown(content, md_file)
            
            # 处理 Mermaid 图表
            if shutil.which("mmdc"):
                content = process_mermaid_diagrams(content, temp_path,
                    config.get("mermaid", {}).get("dpi", 150))
            
            # 添加文档标题
            doc_title = f"# {md_file.stem.replace('-', ' ').title()}\n\n"
            
            merged_content.append(doc_title + content)
            
            # 添加分页符
            if page_break_between and i < len(input_files) - 1:
                merged_content.append("\n\\newpage\n")
        
        # 写入合并后的文件
        merged_md = temp_path / "merged.md"
        with open(merged_md, "w", encoding="utf-8") as f:
            f.write("\n\n".join(merged_content))
        
        # 构建并执行 pandoc 命令
        args = build_pandoc_args(config, TEMPLATE_FILE, output_file)
        args.append(str(merged_md))
        
        try:
            result = subprocess.run(args, capture_output=True, text=True, cwd=temp_dir)
            if result.returncode != 0:
                log(f"pandoc 错误:\n{result.stderr}", "ERROR")
                return False
            
            log(f"成功导出合并文档: {output_file}", "SUCCESS")
            return True
            
        except Exception as e:
            log(f"导出失败: {e}", "ERROR")
            return False


def export_full_project(config: Optional[Dict] = None) -> bool:
    """
    导出完整项目为多个 PDF (按目录组织)
    
    Args:
        config: 配置字典
    
    Returns:
        是否成功
    """
    if config is None:
        config = load_config()
    
    log("=" * 60)
    log("开始导出完整项目")
    log("=" * 60)
    
    success_count = 0
    total_dirs = 0
    
    # 主要目录
    main_dirs = ["Struct", "Knowledge", "Flink"]
    
    for dir_name in main_dirs:
        dir_path = PROJECT_ROOT / dir_name
        if not dir_path.exists():
            log(f"目录不存在: {dir_path}", "WARNING")
            continue
        
        total_dirs += 1
        log(f"\n导出目录: {dir_name}")
        log("-" * 40)
        
        output_subdir = OUTPUT_DIR / dir_name
        exported = export_batch(dir_path, output_subdir, config=config)
        
        if exported:
            success_count += 1
            
            # 创建合并版本
            md_files = sorted(dir_path.rglob("*.md"))
            if md_files:
                merged_file = OUTPUT_DIR / f"{dir_name}-Complete.pdf"
                log(f"\n创建合并版本: {merged_file.name}")
                export_merge(md_files, merged_file, config)
    
    log("\n" + "=" * 60)
    log(f"完整项目导出完成: {success_count}/{total_dirs} 个主目录", "SUCCESS")
    log(f"输出目录: {OUTPUT_DIR}")
    log("=" * 60)
    
    return success_count == total_dirs


# =============================================================================
# 命令行接口
# =============================================================================

def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="AnalysisDataFlow PDF 导出工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 导出单个文件
  %(prog)s single README.md
  %(prog)s single Struct/00-INDEX.md -o output.pdf

  # 批量导出目录
  %(prog)s batch Struct/
  %(prog)s batch Knowledge/ -o ./my-pdfs/

  # 合并导出多个文件
  %(prog)s merge file1.md file2.md file3.md -o merged.pdf

  # 导出完整项目
  %(prog)s full

  # 检查依赖
  %(prog)s check
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # single 命令
    single_parser = subparsers.add_parser("single", help="导出单个 Markdown 文件")
    single_parser.add_argument("input", help="输入 Markdown 文件路径")
    single_parser.add_argument("-o", "--output", help="输出 PDF 文件路径")
    single_parser.add_argument("--no-mermaid", action="store_true",
                              help="不渲染 Mermaid 图表")
    
    # batch 命令
    batch_parser = subparsers.add_parser("batch", help="批量导出目录")
    batch_parser.add_argument("input", help="输入目录路径")
    batch_parser.add_argument("-o", "--output", help="输出目录路径")
    batch_parser.add_argument("-p", "--pattern", default="*.md",
                             help="文件匹配模式 (默认: *.md)")
    batch_parser.add_argument("--flat", action="store_true",
                             help="平铺输出，不保留目录结构")
    
    # merge 命令
    merge_parser = subparsers.add_parser("merge", help="合并多个文件导出")
    merge_parser.add_argument("inputs", nargs="+", help="输入 Markdown 文件路径")
    merge_parser.add_argument("-o", "--output", required=True, help="输出 PDF 文件路径")
    merge_parser.add_argument("--no-page-break", action="store_true",
                             help="文档间不添加分页")
    
    # full 命令
    full_parser = subparsers.add_parser("full", help="导出完整项目")
    
    # check 命令
    check_parser = subparsers.add_parser("check", help="检查依赖环境")
    
    return parser


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # check 命令
    if args.command == "check":
        log("检查依赖环境...")
        deps = check_dependencies()
        
        print("\n依赖状态:")
        print("-" * 40)
        for name, installed in deps.items():
            status = "✓ 已安装" if installed else "✗ 未安装"
            print(f"  {name:12} {status}")
        print("-" * 40)
        
        if not all(deps.values()):
            log("\n缺少必需依赖，请参考 PDF-EXPORT-GUIDE.md 安装", "WARNING")
            return 1
        return 0
    
    # 加载配置
    config = load_config()
    
    # 检查核心依赖
    deps = check_dependencies()
    if not deps["pandoc"] or not deps["xelatex"]:
        log("缺少必需依赖 (pandoc 或 xelatex)", "ERROR")
        log("请运行 'python export-to-pdf.py check' 检查环境", "INFO")
        return 1
    
    # single 命令
    if args.command == "single":
        input_file = Path(args.input)
        output_file = Path(args.output) if args.output else None
        success = export_single(input_file, output_file, config, 
                               with_mermaid=not args.no_mermaid)
        return 0 if success else 1
    
    # batch 命令
    elif args.command == "batch":
        input_dir = Path(args.input)
        output_dir = Path(args.output) if args.output else None
        exported = export_batch(input_dir, output_dir, args.pattern, config,
                               preserve_structure=not args.flat)
        return 0 if exported else 1
    
    # merge 命令
    elif args.command == "merge":
        input_files = [Path(f) for f in args.inputs]
        output_file = Path(args.output)
        success = export_merge(input_files, output_file, config,
                             page_break_between=not args.no_page_break)
        return 0 if success else 1
    
    # full 命令
    elif args.command == "full":
        success = export_full_project(config)
        return 0 if success else 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
