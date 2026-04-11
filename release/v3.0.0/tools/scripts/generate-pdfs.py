#!/usr/bin/env python3
"""
AnalysisDataFlow 白皮书 PDF 生成脚本
支持本地批量生成和GitHub Actions集成
"""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path
from datetime import datetime

# 白皮书配置
WHITEPAPERS = {
    "streaming-technology-trends-2026": {
        "title": "流计算技术趋势白皮书 2026",
        "english_title": "Streaming Technology Trends Whitepaper 2026",
        "subtitle": "技术趋势预测、市场分析、选型指南",
        "version": "v1.0",
        "date": "2026-04-08",
        "audience": "CTO、架构师、技术决策者",
        "pages": "40+",
        "size": "~37KB"
    },
    "flink-enterprise-implementation-guide": {
        "title": "Flink企业落地指南",
        "english_title": "Flink Enterprise Implementation Guide",
        "subtitle": "实施路线图、最佳实践、成功案例",
        "version": "v1.0",
        "date": "2026-04-08",
        "audience": "技术负责人、架构师、运维工程师",
        "pages": "60+",
        "size": "~39KB"
    },
    "realtime-ai-architecture-practice": {
        "title": "实时AI架构实践白皮书",
        "english_title": "Real-Time AI Architecture Practice Whitepaper",
        "subtitle": "AI+流计算架构、生产案例、技术实现",
        "version": "v1.0",
        "date": "2026-04-08",
        "audience": "AI工程师、架构师、技术决策者",
        "pages": "50+",
        "size": "~39KB"
    }
}


def check_dependencies():
    """检查必要的依赖是否安装"""
    deps = ["pandoc"]
    missing = []
    
    for dep in deps:
        result = subprocess.run(
            ["which", dep] if os.name != 'nt' else ["where", dep],
            capture_output=True
        )
        if result.returncode != 0:
            missing.append(dep)
    
    if missing:
        print(f"❌ 缺少依赖: {', '.join(missing)}")
        print("请安装:")
        print("  macOS: brew install pandoc")
        print("  Ubuntu: sudo apt-get install pandoc texlive-xetex")
        print("  Windows: choco install pandoc")
        return False
    
    return True


def generate_cover_page(paper_id: str, config: dict, output_dir: Path) -> Path:
    """生成封面页LaTeX文件"""
    
    latex_content = f"""% 自动生成的封面 - {paper_id}
\\documentclass[12pt,a4paper]{{article}}
\\usepackage[UTF8]{{ctex}}
\\usepackage{{geometry}}
\\usepackage{{xcolor}}
\\usepackage{{graphicx}}
\\usepackage{{tikz}}
\\usepackage{{fontspec}}

\\geometry{{margin=0cm}}
\\pagestyle{{empty}}

% 定义颜色
\\definecolor{{primaryblue}}{{RGB}}{{31,78,121}}
\\definecolor{{accentgold}}{{RGB}}{{197,164,100}}
\\definecolor{{lightgray}}{{RGB}}{{245,245,245}}
\\definecolor{{darkgray}}{{RGB}}{{64,64,64}}

\\begin{{document}}

\\begin{{tikzpicture}}[remember picture,overlay]
  % 顶部主色块
  \\fill[primaryblue] (current page.north west) rectangle ([yshift=-10cm]current page.north east);
  
  % 金色装饰线
  \\draw[accentgold, line width=3pt] ([yshift=-10cm,xshift=2cm]current page.north west) -- ([yshift=-10cm,xshift=-2cm]current page.north east);
  
  % 灰色底部
  \\fill[lightgray] ([yshift=-10cm]current page.north west) rectangle (current page.south east);
  
  % 底部装饰
  \\fill[primaryblue!10] ([yshift=4cm]current page.south west) rectangle (current page.south east);
\\end{{tikzpicture}}

\\vspace*{{3cm}}

\\begin{{center}}
  {{\\fontsize{{14}}{{16}}\\selectfont\\color{{white}} AnalysisDataFlow Project}}
  
  \\vspace{{1cm}}
  
  {{\\fontsize{{32}}{{40}}\\selectfont\\bfseries\\color{{white}} WHITEPAPER}}
  
  \\vspace{{4cm}}
  
  {{\\fontsize{{30}}{{38}}\\selectfont\\bfseries\\color{{primaryblue}} {config['title']}}}
  
  \\vspace{{0.8cm}}
  
  {{\\fontsize{{16}}{{20}}\\selectfont\\color{{darkgray}} {config['english_title']}}}
  
  \\vspace{{0.5cm}}
  
  {{\\fontsize{{13}}{{16}}\\selectfont\\color{{gray}} {config['subtitle']}}}
  
  \\vfill
  
  \\begin{{tikzpicture}}
    \\draw[accentgold, line width=1.5pt] (-4,0) -- (4,0);
  \\end{{tikzpicture}}
  
  \\vspace{{0.8cm}}
  
  {{\\fontsize{{12}}{{15}}\\selectfont\\color{{darkgray}} \\textbf{{版本}}: {config['version']}}}
  
  \\vspace{{0.3cm}}
  
  {{\\fontsize{{12}}{{15}}\\selectfont\\color{{darkgray}} \\textbf{{发布日期}}: {config['date']}}}
  
  \\vspace{{0.3cm}}
  
  {{\\fontsize{{11}}{{13}}\\selectfont\\color{{gray}} \\textbf{{目标读者}}: {config['audience']}}}
  
  \\vspace{{1.5cm}}
  
  {{\\fontsize{{10}}{{12}}\\selectfont\\color{{gray}} https://github.com/AnalysisDataFlow}}
\\end{{center}}

\\end{{document}}
"""
    
    cover_path = output_dir / f"{paper_id}-cover.tex"
    cover_path.write_text(latex_content, encoding='utf-8')
    return cover_path


def preprocess_markdown(paper_id: str, config: dict, input_path: Path, output_path: Path):
    """预处理Markdown文件，添加LaTeX frontmatter"""
    
    # 读取原始内容
    content = input_path.read_text(encoding='utf-8')
    
    # 移除第一个H1标题（使用封面替代）
    lines = content.split('\n')
    filtered_lines = []
    skip_next = False
    
    for line in lines:
        if line.startswith('# ') and not skip_next:
            skip_next = True
            continue
        if skip_next and line.strip() == '---':
            skip_next = False
            continue
        filtered_lines.append(line)
    
    filtered_content = '\n'.join(filtered_lines)
    
    # 构建frontmatter
    frontmatter = f"""---
title: "{config['title']}"
subtitle: "{config['subtitle']}"
author: AnalysisDataFlow Project Team
date: \\today
geometry: margin=2.5cm
papersize: a4
fontsize: 11pt
linestretch: 1.3
header-includes:
  - \\usepackage[UTF8]{{ctex}}
  - \\usepackage{{fancyhdr}}
  - \\usepackage{{titlesec}}
  - \\usepackage{{graphicx}}
  - \\usepackage{{xcolor}}
  - \\usepackage{{booktabs}}
  - \\usepackage{{longtable}}
  - \\usepackage{{array}}
  - \\usepackage{{float}}
  - \\usepackage{{caption}}
  - \\usepackage{{hyperref}}
  - \\usepackage{{listings}}
  - \\usepackage{{tikz}}
  - \\usepackage{{setspace}}
  - \\pagestyle{{fancy}}
  - \\fancyhf{{}}
  - \\fancyhead[L]{{\\small\\leftmark}}
  - \\fancyhead[R]{{\\small AnalysisDataFlow Whitepaper}}
  - \\fancyfoot[C]{{\\thepage}}
  - \\renewcommand{{\\headrulewidth}}{{0.4pt}}
  - \\renewcommand{{\\footrulewidth}}{{0.4pt}}
  - \\definecolor{{primaryblue}}{{RGB}}{{31,78,121}}
  - \\definecolor{{accentgold}}{{RGB}}{{197,164,100}}
  - \\titleformat{{\\section}}{{\\Large\\bfseries\\color{{primaryblue}}}}{{\\thesection}}{{1em}}{{}}
  - \\titleformat{{\\subsection}}{{\\large\\bfseries\\color{{primaryblue!80}}}}{{\\thesubsection}}{{1em}}{{}}
  - \\lstset{{basicstyle=\\small\\ttfamily,frame=single,breaklines=true}}
---

"""
    
    # 合并内容
    final_content = frontmatter + filtered_content
    
    output_path.write_text(final_content, encoding='utf-8')
    return output_path


def generate_pdf(paper_id: str, config: dict, whitepapers_dir: Path, output_dir: Path, use_docker: bool = False) -> Path:
    """生成单个PDF文件"""
    
    print(f"\n📄 正在生成: {config['title']}")
    
    input_path = whitepapers_dir / f"{paper_id}.md"
    output_path = output_dir / f"{paper_id}.pdf"
    
    if not input_path.exists():
        print(f"❌ 未找到输入文件: {input_path}")
        return None
    
    # 创建临时目录
    temp_dir = output_dir / "temp"
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # 预处理Markdown
        preprocessed_path = temp_dir / f"{paper_id}-preprocessed.md"
        preprocess_markdown(paper_id, config, input_path, preprocessed_path)
        
        # 生成封面
        cover_path = generate_cover_page(paper_id, config, temp_dir)
        
        # 编译封面
        print("  🎨 生成封面...")
        result = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-output-directory", str(temp_dir), str(cover_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"  ⚠️  封面编译警告 (非致命)")
        
        # 使用pandoc转换
        print("  📝 转换Markdown...")
        pandoc_cmd = [
            "pandoc",
            str(preprocessed_path),
            "--pdf-engine=xelatex",
            f"--output={output_path}",
            "--toc",
            "--toc-depth=3",
            "--number-sections",
            "--listings",
            "--highlight-style=tango",
            "-V", "geometry:margin=2.5cm",
            "-V", "colorlinks=true",
            "-V", "linkcolor=blue",
            "-V", "urlcolor=blue"
        ]
        
        result = subprocess.run(pandoc_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"  ❌ 生成失败:\n{result.stderr}")
            return None
        
        # 合并封面和正文 (使用pdfunite或pypdf)
        cover_pdf = temp_dir / f"{paper_id}-cover.pdf"
        if cover_pdf.exists():
            print("  📎 合并封面...")
            try:
                from pypdf import PdfMerger, PdfReader
                
                merger = PdfMerger()
                if cover_pdf.exists():
                    merger.append(str(cover_pdf))
                merger.append(str(output_path))
                
                final_output = output_dir / f"{paper_id}.pdf"
                merger.write(str(final_output))
                merger.close()
                
                print(f"  ✅ 完成: {final_output}")
                return final_output
            except ImportError:
                print(f"  ⚠️  未安装pypdf，封面未合并")
                print(f"  ✅ 完成: {output_path}")
                return output_path
        else:
            print(f"  ✅ 完成: {output_path}")
            return output_path
            
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return None


def generate_download_page(output_dir: Path, generated_pdfs: list):
    """生成HTML下载页面"""
    
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>白皮书下载 - AnalysisDataFlow</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      min-height: 100vh;
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 40px 20px;
    }
    header {
      text-align: center;
      margin-bottom: 60px;
    }
    header h1 {
      font-size: 2.5rem;
      color: #1f4e79;
      margin-bottom: 10px;
    }
    header p {
      font-size: 1.1rem;
      color: #666;
    }
    .papers-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
      gap: 30px;
      margin-bottom: 60px;
    }
    .paper-card {
      background: white;
      border-radius: 12px;
      padding: 30px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      transition: transform 0.3s, box-shadow 0.3s;
    }
    .paper-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    .paper-icon {
      width: 60px;
      height: 60px;
      background: linear-gradient(135deg, #1f4e79, #3a7bd5);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 20px;
    }
    .paper-icon svg {
      width: 32px;
      height: 32px;
      fill: white;
    }
    .paper-card h2 {
      font-size: 1.3rem;
      color: #1f4e79;
      margin-bottom: 10px;
    }
    .paper-card .subtitle {
      font-size: 0.9rem;
      color: #888;
      margin-bottom: 15px;
    }
    .paper-meta {
      display: flex;
      gap: 15px;
      margin-bottom: 20px;
      font-size: 0.85rem;
      color: #666;
      flex-wrap: wrap;
    }
    .paper-meta span {
      background: #f0f4f8;
      padding: 4px 12px;
      border-radius: 20px;
    }
    .download-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: linear-gradient(135deg, #1f4e79, #3a7bd5);
      color: white;
      padding: 12px 24px;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 500;
      transition: opacity 0.3s;
    }
    .download-btn:hover {
      opacity: 0.9;
    }
    .download-btn svg {
      width: 20px;
      height: 20px;
    }
    .features {
      background: white;
      border-radius: 12px;
      padding: 40px;
      margin-bottom: 40px;
    }
    .features h3 {
      font-size: 1.5rem;
      color: #1f4e79;
      margin-bottom: 20px;
    }
    .features ul {
      list-style: none;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 15px;
    }
    .features li {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .features li::before {
      content: "✓";
      display: flex;
      align-items: center;
      justify-content: center;
      width: 24px;
      height: 24px;
      background: #4caf50;
      color: white;
      border-radius: 50%;
      font-size: 0.8rem;
    }
    .timestamp {
      text-align: center;
      color: #888;
      font-size: 0.9rem;
      margin-top: 20px;
    }
    footer {
      text-align: center;
      padding: 40px 0;
      color: #666;
    }
    footer a {
      color: #1f4e79;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>📄 AnalysisDataFlow 白皮书</h1>
      <p>流计算领域权威技术参考文档 - 专业PDF格式下载</p>
    </header>
    
    <div class="papers-grid">
"""
    
    # 添加PDF卡片
    for paper_id, config in WHITEPAPERS.items():
        pdf_exists = any(paper_id in str(p) for p in generated_pdfs)
        button_attrs = 'href="{}" download'.format(f"{paper_id}.pdf") if pdf_exists else 'href="#" style="background:#ccc;pointer-events:none"'
        button_text = "下载 PDF" if pdf_exists else "生成中..."
        
        icons = {
            "streaming-technology-trends-2026": "M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z",
            "flink-enterprise-implementation-guide": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z",
            "realtime-ai-architecture-practice": "M12 2l-5.5 9h11z\"/><circle cx=\"17.5\" cy=\"17.5\" r=\"4.5\"/><path d=\"M3 13.5h8v8H3z"
        }
        
        tags = {
            "streaming-technology-trends-2026": ["📊 市场分析", "🔮 趋势预测"],
            "flink-enterprise-implementation-guide": ["🏗️ 实施路线图", "💼 企业案例"],
            "realtime-ai-architecture-practice": ["🤖 AI架构", "⚡ 实时推理"]
        }
        
        html_content += f"""
      <div class="paper-card">
        <div class="paper-icon">
          <svg viewBox="0 0 24 24"><path d="{icons.get(paper_id, '')}"/></svg>
        </div>
        <h2>{config['title']}</h2>
        <p class="subtitle">{config['english_title']}</p>
        <div class="paper-meta">
          <span>📄 {config['pages']} 页</span>
          {''.join(f'<span>{tag}</span>' for tag in tags.get(paper_id, []))}
        </div>
        <a {button_attrs} class="download-btn">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
          {button_text}
        </a>
      </div>
"""
    
    html_content += f"""
    </div>
    
    <div class="features">
      <h3>📋 PDF文档特性</h3>
      <ul>
        <li>专业学术排版（ACM/IEEE格式）</li>
        <li>自动生成目录导航</li>
        <li>页眉页脚标识</li>
        <li>图表公式正确渲染</li>
        <li>可打印高质量输出</li>
        <li>支持全文检索</li>
      </ul>
    </div>
    
    <div class="timestamp">
      <p>最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <footer>
      <p>© 2026 AnalysisDataFlow Project | 
         <a href="https://github.com/AnalysisDataFlow">GitHub</a> | 
         <a href="../">返回主页</a>
      </p>
    </footer>
  </div>
</body>
</html>
"""
    
    download_page_path = output_dir / "index.html"
    download_page_path.write_text(html_content, encoding='utf-8')
    print(f"\n🌐 下载页面已生成: {download_page_path}")
    return download_page_path


def generate_metadata(output_dir: Path):
    """生成metadata.json文件"""
    
    metadata = {
        "export_date": datetime.now().isoformat(),
        "version": "1.0",
        "papers": [
            {
                "id": paper_id,
                "filename": f"{paper_id}.pdf",
                **config
            }
            for paper_id, config in WHITEPAPERS.items()
        ]
    }
    
    metadata_path = output_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"📋 元数据已生成: {metadata_path}")


def main():
    parser = argparse.ArgumentParser(
        description="AnalysisDataFlow 白皮书 PDF 生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                          # 生成所有白皮书
  %(prog)s -p streaming-technology-trends-2026    # 生成指定白皮书
  %(prog)s -o ./output              # 指定输出目录
        """
    )
    
    parser.add_argument(
        "-p", "--paper",
        choices=list(WHITEPAPERS.keys()),
        help="指定要生成的白皮书ID"
    )
    parser.add_argument(
        "-o", "--output",
        default="whitepapers/pdf",
        help="输出目录 (默认: whitepapers/pdf)"
    )
    parser.add_argument(
        "--docker",
        action="store_true",
        help="使用Docker运行pandoc"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="检查依赖并退出"
    )
    
    args = parser.parse_args()
    
    # 检查依赖
    if not check_dependencies() or args.check:
        sys.exit(1 if not args.check else 0)
    
    # 确定路径
    script_dir = Path(__file__).parent.parent
    whitepapers_dir = script_dir / "whitepapers"
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 确定要生成的白皮书
    if args.paper:
        papers_to_generate = {args.paper: WHITEPAPERS[args.paper]}
    else:
        papers_to_generate = WHITEPAPERS
    
    print("=" * 60)
    print("AnalysisDataFlow 白皮书 PDF 生成器")
    print("=" * 60)
    
    # 生成PDF
    generated_pdfs = []
    for paper_id, config in papers_to_generate.items():
        pdf_path = generate_pdf(
            paper_id, config,
            whitepapers_dir, output_dir,
            use_docker=args.docker
        )
        if pdf_path:
            generated_pdfs.append(pdf_path)
    
    # 生成下载页面和元数据
    generate_download_page(output_dir, generated_pdfs)
    generate_metadata(output_dir)
    
    # 输出结果
    print("\n" + "=" * 60)
    print(f"✅ 生成完成! 共 {len(generated_pdfs)}/{len(papers_to_generate)} 个PDF")
    print("=" * 60)
    print(f"\n输出目录: {output_dir.absolute()}")
    print("\n生成的文件:")
    for pdf in generated_pdfs:
        size = pdf.stat().st_size / 1024
        print(f"  📄 {pdf.name} ({size:.1f} KB)")
    print(f"\n🌐 下载页面: {output_dir / 'index.html'}")


if __name__ == "__main__":
    main()
