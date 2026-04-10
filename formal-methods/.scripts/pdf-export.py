#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formal Methods PDF Export Tool
==============================

自动化将Markdown转换为PDF的专用工具，针对形式化方法文档优化。
支持数学公式、Mermaid图表、交叉引用和多种导出模式。

Author: AnalysisDataFlow Team
Version: 1.0.0
License: MIT

Dependencies:
    - pandoc >= 2.14
    - pdflatex / xelatex / lualatex
    - mermaid-cli (for diagram conversion)
    - PyYAML (for config parsing)

Usage:
    python pdf-export.py single input.md -o output.pdf
    python pdf-export.py batch "*.md" -o output_dir/
    python pdf-export.py merge file1.md file2.md -o combined.pdf
"""

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union


# =============================================================================
# Configuration and Data Classes
# =============================================================================

@dataclass
class ExportConfig:
    """PDF导出配置类"""
    # 基础配置
    template: str = "default"
    latex_engine: str = "xelatex"
    paper_size: str = "a4"
    margin: str = "2.5cm"
    
    # 字体配置
    main_font: str = "Latin Modern Roman"
    sans_font: str = "Latin Modern Sans"
    mono_font: str = "Latin Modern Mono"
    math_font: str = "Latin Modern Math"
    cjk_font: str = "Noto Serif CJK SC"
    
    # 内容配置
    toc: bool = True
    toc_depth: int = 3
    number_sections: bool = True
    
    # 公式配置
    math_engine: str = "mathjax"  # mathjax, katex, webtex
    
    # 图表配置
    mermaid_enabled: bool = True
    mermaid_theme: str = "default"
    figure_caption: bool = True
    
    # 代码配置
    code_highlight: str = "tango"
    code_font_size: str = "small"
    
    # 交叉引用
    cross_ref_enabled: bool = True
    
    # 分页配置
    chapter_newpage: bool = True
    
    # 元数据
    title: str = ""
    author: str = "AnalysisDataFlow"
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    version: str = "1.0"
    
    @classmethod
    def from_dict(cls, data: Dict) -> "ExportConfig":
        """从字典创建配置"""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    @classmethod
    def from_file(cls, path: Union[str, Path]) -> "ExportConfig":
        """从配置文件加载"""
        path = Path(path)
        if not path.exists():
            return cls()
        
        content = path.read_text(encoding='utf-8')
        
        if path.suffix == '.json':
            data = json.loads(content)
        elif path.suffix in ('.yaml', '.yml'):
            try:
                import yaml
                data = yaml.safe_load(content)
            except ImportError:
                logging.warning("PyYAML not installed, using default config")
                return cls()
        else:
            return cls()
        
        return cls.from_dict(data)


@dataclass
class ExportResult:
    """导出结果"""
    success: bool
    output_path: Optional[Path]
    message: str
    warnings: List[str] = field(default_factory=list)
    stats: Dict = field(default_factory=dict)


# =============================================================================
# Default LaTeX Templates
# =============================================================================

DEFAULT_LATEX_TEMPLATE = r'''
\documentclass[$if(fontsize)$$fontsize$,$endif$$if(lang)$$babel-lang$,$endif$$if(papersize)$$papersize$paper,$endif$$for(classoption)$$classoption$$sep$,$endfor$]{article}

% Encoding and fonts
\usepackage[UTF8]{ctex}
\usepackage{fontspec}
\setmainfont{$mainfont$}
\setsansfont{$sansfont$}
\setmonofont{$monofont$}

% Math support
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsthm}

% Page geometry
\usepackage[$for(geometry)$$geometry$$sep$,$endfor$]{geometry}

% Colors
\usepackage{xcolor}
\definecolor{linkblue}{RGB}{0,82,147}
\definecolor{citegreen}{RGB}{0,128,0}
\definecolor{urlred}{RGB}{128,0,0}

% Links
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=linkblue,
    citecolor=citegreen,
    urlcolor=urlred,
    bookmarks=true,
    bookmarksdepth=3
}

% Listings for code
\usepackage{listings}
\lstset{
    basicstyle=\ttfamily\small,
    breaklines=true,
    frame=single,
    numbers=left,
    numberstyle=\tiny\color{gray},
    keywordstyle=\color{blue},
    commentstyle=\color{green!60!black},
    stringstyle=\color{red}
}

% Graphics
\usepackage{graphicx}
\usepackage{float}

% Tables
\usepackage{longtable}
\usepackage{booktabs}

% Header/Footer
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\leftmark}
\fancyhead[R]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

% Theorem environments
\newtheorem{theorem}{定理}[section]
\newtheorem{lemma}[theorem]{引理}
\newtheorem{proposition}[theorem]{命题}
\newtheorem{corollary}[theorem]{推论}
\newtheorem{definition}[theorem]{定义}
\newtheorem{example}[theorem]{例}

% Custom commands
\newcommand{\TODO}[1]{\textcolor{red}{\textbf{TODO: #1}}}

$if(title)$
\title{$title$}
$endif$
$if(author)$
\author{$for(author)$$author$$sep$ \and $endfor$}
$endif$
$if(date)$
\date{$date$}
$endif$

\begin{document}

$if(title)$
\maketitle
$endif$

$if(abstract)$
\begin{abstract}
$abstract$
\end{abstract}
$endif$

$if(toc)$
\tableofcontents
\newpage
$endif$

$body$

\end{document}
'''

BOOK_LATEX_TEMPLATE = r'''
\documentclass[$if(fontsize)$$fontsize$,$endif$$if(lang)$$babel-lang$,$endif$$if(papersize)$$papersize$paper,$endif$]{book}

% Encoding and fonts
\usepackage[UTF8]{ctex}
\usepackage{fontspec}
\setmainfont{$mainfont$}
\setsansfont{$sansfont$}
\setmonofont{$monofont$}

% Math support
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsthm}

% Page geometry
\usepackage[$for(geometry)$$geometry$$sep$,$endfor$]{geometry}

% Colors
\usepackage{xcolor}
\definecolor{linkblue}{RGB}{0,82,147}
\definecolor{citegreen}{RGB}{0,128,0}

% Links
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=linkblue,
    citecolor=citegreen,
    bookmarks=true,
    bookmarksdepth=3
}

% Listings
\usepackage{listings}
\lstset{
    basicstyle=\ttfamily\small,
    breaklines=true,
    frame=single
}

\usepackage{graphicx}
\usepackage{longtable}
\usepackage{booktabs}

% Theorem environments
\newtheorem{theorem}{定理}[chapter]
\newtheorem{lemma}[theorem]{引理}
\newtheorem{definition}[theorem]{定义}

$if(title)$
\title{$title$}
$endif$
$if(author)$
\author{$for(author)$$author$$sep$ \and $endfor$}
$endif$

\begin{document}

\frontmatter
$if(title)$
\maketitle
$endif$

$if(toc)$
\tableofcontents
$endif$

\mainmatter
$body$

\backmatter
$if(bibliography)$
\bibliography{$for(bibliography)$$bibliography$$sep$,$endfor$}
$endif$

\end{document}
'''


# =============================================================================
# Mermaid Processor
# =============================================================================

class MermaidProcessor:
    """Mermaid图表处理器"""
    
    MERMAID_PATTERN = re.compile(r'```mermaid\s*\n(.*?)```', re.DOTALL)
    
    def __init__(self, temp_dir: Path, theme: str = "default"):
        self.temp_dir = temp_dir
        self.theme = theme
        self.diagram_count = 0
        self.cache: Dict[str, Path] = {}
    
    def check_mmdc(self) -> bool:
        """检查mermaid-cli是否可用"""
        return shutil.which("mmdc") is not None
    
    def convert_diagram(self, code: str, idx: int) -> Optional[Path]:
        """将Mermaid代码转换为SVG图片"""
        # 使用缓存
        code_hash = hash(code) & 0xFFFFFFFF
        if code_hash in self.cache:
            return self.cache[code_hash]
        
        input_file = self.temp_dir / f"diagram_{idx}.mmd"
        output_file = self.temp_dir / f"diagram_{idx}.svg"
        
        input_file.write_text(code, encoding='utf-8')
        
        cmd = [
            "mmdc",
            "-i", str(input_file),
            "-o", str(output_file),
            "-t", self.theme,
            "-b", "transparent"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0 and output_file.exists():
                self.cache[code_hash] = output_file
                return output_file
            else:
                logging.warning(f"Mermaid conversion failed: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            logging.warning(f"Mermaid conversion timeout for diagram {idx}")
            return None
        except Exception as e:
            logging.warning(f"Mermaid conversion error: {e}")
            return None
    
    def process_markdown(self, content: str) -> Tuple[str, List[str]]:
        """处理Markdown中的Mermaid图表，返回处理后的内容和警告列表"""
        warnings = []
        
        if not self.check_mmdc():
            warnings.append("mmdc (mermaid-cli) not found, diagrams will be left as code blocks")
            return content, warnings
        
        def replace_diagram(match) -> str:
            nonlocal self
            self.diagram_count += 1
            code = match.group(1).strip()
            
            output_path = self.convert_diagram(code, self.diagram_count)
            if output_path:
                return f"\n![Mermaid Diagram {self.diagram_count}]({output_path})\n"
            else:
                warnings.append(f"Failed to convert diagram {self.diagram_count}")
                return match.group(0)  # 保持原样
        
        processed = self.MERMAID_PATTERN.sub(replace_diagram, content)
        return processed, warnings


# =============================================================================
# Cross-Reference Processor
# =============================================================================

class CrossRefProcessor:
    """交叉引用处理器"""
    
    # 匹配各种引用格式
    REF_PATTERNS = {
        'theorem': re.compile(r'\[Thm-([A-Z])-(\d+)-(\d+)\]'),
        'lemma': re.compile(r'\[Lemma-([A-Z])-(\d+)-(\d+)\]'),
        'definition': re.compile(r'\[Def-([A-Z])-(\d+)-(\d+)\]'),
        'proposition': re.compile(r'\[Prop-([A-Z])-(\d+)-(\d+)\]'),
        'corollary': re.compile(r'\[Cor-([A-Z])-(\d+)-(\d+)\]'),
        'internal_link': re.compile(r'\[([^\]]+)\]\(#([^)]+)\)'),
        'file_link': re.compile(r'\[([^\]]+)\]\(([^)#]+)(?:#[^)]*)?\)'),
    }
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.ref_map: Dict[str, str] = {}
        self.warnings: List[str] = []
    
    def build_ref_map(self, files: List[Path]) -> None:
        """构建引用映射表"""
        for file_path in files:
            try:
                content = file_path.read_text(encoding='utf-8')
                # 提取所有定义和定理
                for match in self.REF_PATTERNS['definition'].finditer(content):
                    ref_id = f"Def-{match.group(1)}-{match.group(2)}-{match.group(3)}"
                    self.ref_map[ref_id] = str(file_path.relative_to(self.base_path))
            except Exception as e:
                self.warnings.append(f"Failed to process {file_path}: {e}")
    
    def process_content(self, content: str, current_file: Path) -> str:
        """处理内容中的交叉引用"""
        # 处理定理引用
        def replace_ref(match, ref_type: str) -> str:
            ref_id = f"{ref_type}-{match.group(1)}-{match.group(2)}-{match.group(3)}"
            label = f"{ref_type} {match.group(1)}.{match.group(2)}.{match.group(3)}"
            if ref_id in self.ref_map:
                return f"[{label}]({self.ref_map[ref_id]}#{ref_id})"
            return f"**{label}**"
        
        for ref_type, pattern in self.REF_PATTERNS.items():
            if ref_type in ['theorem', 'lemma', 'definition', 'proposition', 'corollary']:
                content = pattern.sub(
                    lambda m, rt=ref_type.capitalize(): replace_ref(m, rt),
                    content
                )
        
        return content


# =============================================================================
# Main Exporter Class
# =============================================================================

class PDFExporter:
    """PDF导出器主类"""
    
    def __init__(self, config: ExportConfig, temp_dir: Optional[Path] = None):
        self.config = config
        self.temp_dir = temp_dir or Path(tempfile.mkdtemp(prefix="pdf_export_"))
        self.mermaid_processor = MermaidProcessor(
            self.temp_dir,
            config.mermaid_theme
        )
        self.cross_ref_processor: Optional[CrossRefProcessor] = None
        self.logger = logging.getLogger(__name__)
    
    def cleanup(self) -> None:
        """清理临时文件"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def check_dependencies(self) -> Tuple[bool, List[str]]:
        """检查依赖是否满足"""
        missing = []
        
        # 检查 pandoc
        if not shutil.which("pandoc"):
            missing.append("pandoc (https://pandoc.org/installing.html)")
        
        # 检查 LaTeX 引擎
        if not shutil.which(self.config.latex_engine):
            missing.append(f"{self.config.latex_engine} (TeX Live or MiKTeX)")
        
        return len(missing) == 0, missing
    
    def prepare_markdown(self, input_path: Path, all_files: Optional[List[Path]] = None) -> Tuple[Path, List[str]]:
        """预处理Markdown文件"""
        content = input_path.read_text(encoding='utf-8')
        warnings = []
        
        # 处理Mermaid图表
        if self.config.mermaid_enabled:
            content, mermaid_warnings = self.mermaid_processor.process_markdown(content)
            warnings.extend(mermaid_warnings)
        
        # 处理交叉引用
        if self.config.cross_ref_enabled and all_files:
            if self.cross_ref_processor is None:
                self.cross_ref_processor = CrossRefProcessor(input_path.parent)
                self.cross_ref_processor.build_ref_map(all_files)
            content = self.cross_ref_processor.process_content(content, input_path)
            warnings.extend(self.cross_ref_processor.warnings)
        
        # 添加元数据头
        metadata = self._build_metadata()
        content = metadata + "\n\n" + content
        
        # 写入临时文件
        output_path = self.temp_dir / f"processed_{input_path.stem}.md"
        output_path.write_text(content, encoding='utf-8')
        
        return output_path, warnings
    
    def _build_metadata(self) -> str:
        """构建Pandoc元数据头"""
        lines = ["---"]
        if self.config.title:
            lines.append(f"title: {self.config.title}")
        if self.config.author:
            lines.append(f"author: {self.config.author}")
        if self.config.date:
            lines.append(f"date: {self.config.date}")
        lines.append(f"toc: {str(self.config.toc).lower()}")
        lines.append(f"toc-depth: {self.config.toc_depth}")
        lines.append(f"number-sections: {str(self.config.number_sections).lower()}")
        lines.append("---")
        return "\n".join(lines)
    
    def create_latex_template(self) -> Path:
        """创建LaTeX模板文件"""
        template_path = self.temp_dir / "template.tex"
        
        if self.config.template == "book":
            template_content = BOOK_LATEX_TEMPLATE
        else:
            template_content = DEFAULT_LATEX_TEMPLATE
        
        # 替换变量
        replacements = {
            '$mainfont$': self.config.main_font,
            '$sansfont$': self.config.sans_font,
            '$monofont$': self.config.mono_font,
            '$title$': self.config.title,
            '$author$': self.config.author,
            '$date$': self.config.date,
        }
        
        for key, value in replacements.items():
            template_content = template_content.replace(key, value)
        
        template_path.write_text(template_content, encoding='utf-8')
        return template_path
    
    def run_pandoc(self, input_path: Path, output_path: Path, template_path: Optional[Path] = None) -> ExportResult:
        """运行pandoc进行转换"""
        cmd = [
            "pandoc",
            str(input_path),
            "-o", str(output_path),
            "--pdf-engine", self.config.latex_engine,
            "-V", f"geometry:margin={self.config.margin}",
            "-V", f"papersize={self.config.paper_size}",
        ]
        
        # 添加模板
        if template_path and template_path.exists():
            cmd.extend(["--template", str(template_path)])
        
        # 添加目录选项
        if self.config.toc:
            cmd.append("--toc")
            cmd.extend(["--toc-depth", str(self.config.toc_depth)])
        
        # 添加章节编号
        if self.config.number_sections:
            cmd.append("--number-sections")
        
        # 添加数学支持
        if self.config.math_engine:
            cmd.extend(["--mathjax"])
        
        # 添加代码高亮
        if self.config.code_highlight:
            cmd.extend(["--highlight-style", self.config.code_highlight])
        
        # 添加其他过滤器
        cmd.extend([
            "-f", "markdown+tex_math_dollars+raw_tex+footnotes+implicit_figures",
            "-t", "pdf",
        ])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                return ExportResult(
                    success=True,
                    output_path=output_path,
                    message="Export successful",
                    stats={"command": " ".join(cmd)}
                )
            else:
                return ExportResult(
                    success=False,
                    output_path=None,
                    message=f"Pandoc failed: {result.stderr}",
                    warnings=[result.stderr]
                )
        except subprocess.TimeoutExpired:
            return ExportResult(
                success=False,
                output_path=None,
                message="Pandoc timed out after 5 minutes"
            )
        except Exception as e:
            return ExportResult(
                success=False,
                output_path=None,
                message=f"Error running pandoc: {e}"
            )
    
    def export_single(self, input_path: Path, output_path: Path) -> ExportResult:
        """导出单个文件"""
        self.logger.info(f"Exporting {input_path} to {output_path}")
        
        if not input_path.exists():
            return ExportResult(
                success=False,
                output_path=None,
                message=f"Input file not found: {input_path}"
            )
        
        # 检查依赖
        deps_ok, missing = self.check_dependencies()
        if not deps_ok:
            return ExportResult(
                success=False,
                output_path=None,
                message=f"Missing dependencies: {', '.join(missing)}"
            )
        
        # 预处理
        processed_path, warnings = self.prepare_markdown(input_path)
        
        # 创建模板
        template_path = self.create_latex_template()
        
        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 运行转换
        result = self.run_pandoc(processed_path, output_path, template_path)
        result.warnings.extend(warnings)
        
        return result
    
    def export_batch(self, input_pattern: str, output_dir: Path) -> List[ExportResult]:
        """批量导出"""
        import glob
        
        input_files = list(Path().glob(input_pattern))
        if not input_files:
            return [ExportResult(
                success=False,
                output_path=None,
                message=f"No files matching pattern: {input_pattern}"
            )]
        
        results = []
        for input_file in input_files:
            if input_file.suffix != '.md':
                continue
            output_file = output_dir / f"{input_file.stem}.pdf"
            result = self.export_single(input_file, output_file)
            results.append(result)
        
        return results
    
    def export_merge(self, input_files: List[Path], output_path: Path) -> ExportResult:
        """合并导出多个文件"""
        self.logger.info(f"Merging {len(input_files)} files to {output_path}")
        
        if not input_files:
            return ExportResult(
                success=False,
                output_path=None,
                message="No input files provided"
            )
        
        # 预处理所有文件
        processed_contents = []
        all_warnings = []
        
        for input_file in input_files:
            if not input_file.exists():
                all_warnings.append(f"File not found: {input_file}")
                continue
            
            processed_path, warnings = self.prepare_markdown(input_file, input_files)
            processed_contents.append(processed_path.read_text(encoding='utf-8'))
            all_warnings.extend(warnings)
            
            # 添加分页符（如果配置启用）
            if self.config.chapter_newpage:
                processed_contents.append("\\newpage\n")
        
        # 合并内容
        merged_content = "\n\n".join(processed_contents)
        merged_path = self.temp_dir / "merged.md"
        merged_path.write_text(merged_content, encoding='utf-8')
        
        # 创建模板并导出
        template_path = self.create_latex_template()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        result = self.run_pandoc(merged_path, output_path, template_path)
        result.warnings.extend(all_warnings)
        
        return result
    
    def export_volume(self, input_files: List[Path], output_dir: Path, 
                      files_per_volume: int = 10) -> List[ExportResult]:
        """分卷导出"""
        results = []
        
        for i in range(0, len(input_files), files_per_volume):
            volume_files = input_files[i:i + files_per_volume]
            volume_num = i // files_per_volume + 1
            output_path = output_dir / f"volume_{volume_num:02d}.pdf"
            
            self.config.title = f"{self.config.title} - Volume {volume_num}"
            result = self.export_merge(volume_files, output_path)
            results.append(result)
        
        return results


# =============================================================================
# CLI Interface
# =============================================================================

def create_parser() -> argparse.ArgumentParser:
    """创建命令行解析器"""
    parser = argparse.ArgumentParser(
        prog="pdf-export.py",
        description="Formal Methods PDF Export Tool - Convert Markdown to PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s single doc.md -o output.pdf
  %(prog)s batch "*.md" -o pdf_output/
  %(prog)s merge doc1.md doc2.md -o combined.pdf
  %(prog)s volume *.md -o volumes/ --files-per-volume 5
  %(prog)s single doc.md -c config.yaml -o output.pdf
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # 全局选项
    parser.add_argument("-c", "--config", type=Path, help="Configuration file (YAML/JSON)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    
    # Single command
    single_parser = subparsers.add_parser("single", help="Export single file")
    single_parser.add_argument("input", type=Path, help="Input Markdown file")
    single_parser.add_argument("-o", "--output", type=Path, required=True, help="Output PDF file")
    single_parser.add_argument("--template", choices=["default", "book"], default="default")
    single_parser.add_argument("--engine", default="xelatex", help="LaTeX engine")
    single_parser.add_argument("--title", help="Document title")
    
    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Batch export files")
    batch_parser.add_argument("pattern", help="File pattern (e.g., '*.md')")
    batch_parser.add_argument("-o", "--output-dir", type=Path, required=True, help="Output directory")
    batch_parser.add_argument("--no-mermaid", action="store_true", help="Disable Mermaid processing")
    
    # Merge command
    merge_parser = subparsers.add_parser("merge", help="Merge multiple files")
    merge_parser.add_argument("files", nargs="+", type=Path, help="Input Markdown files")
    merge_parser.add_argument("-o", "--output", type=Path, required=True, help="Output PDF file")
    merge_parser.add_argument("--no-page-break", action="store_true", help="Disable page breaks between files")
    
    # Volume command
    volume_parser = subparsers.add_parser("volume", help="Export in volumes")
    volume_parser.add_argument("files", nargs="+", type=Path, help="Input Markdown files")
    volume_parser.add_argument("-o", "--output-dir", type=Path, required=True, help="Output directory")
    volume_parser.add_argument("--files-per-volume", type=int, default=10, help="Files per volume")
    
    return parser


def setup_logging(verbose: bool) -> None:
    """设置日志"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )


def main() -> int:
    """主入口函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # 设置日志
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # 加载配置
    config = ExportConfig()
    if args.config:
        config = ExportConfig.from_file(args.config)
        logger.info(f"Loaded config from {args.config}")
    
    # 应用命令行覆盖
    if hasattr(args, 'template'):
        config.template = args.template
    if hasattr(args, 'engine'):
        config.latex_engine = args.engine
    if hasattr(args, 'title') and args.title:
        config.title = args.title
    if hasattr(args, 'no_mermaid') and args.no_mermaid:
        config.mermaid_enabled = False
    if hasattr(args, 'no_page_break') and args.no_page_break:
        config.chapter_newpage = False
    
    # 创建导出器
    exporter = PDFExporter(config)
    
    try:
        # 执行命令
        if args.command == "single":
            result = exporter.export_single(args.input, args.output)
            results = [result]
        
        elif args.command == "batch":
            results = exporter.export_batch(args.pattern, args.output_dir)
        
        elif args.command == "merge":
            result = exporter.export_merge(args.files, args.output)
            results = [result]
        
        elif args.command == "volume":
            results = exporter.export_volume(args.files, args.output_dir, args.files_per_volume)
        
        else:
            parser.print_help()
            return 1
        
        # 输出结果
        success_count = sum(1 for r in results if r.success)
        total_count = len(results)
        
        for i, result in enumerate(results):
            status = "✓" if result.success else "✗"
            output = result.output_path or "N/A"
            print(f"[{status}] {i+1}/{total_count}: {output}")
            if result.warnings:
                for warning in result.warnings:
                    print(f"    ⚠ {warning}")
            if not result.success:
                print(f"    ✗ Error: {result.message}")
        
        print(f"\nSummary: {success_count}/{total_count} files exported successfully")
        
        return 0 if success_count == total_count else 1
    
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1
    finally:
        exporter.cleanup()


if __name__ == "__main__":
    sys.exit(main())
