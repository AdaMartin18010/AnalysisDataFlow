#!/usr/bin/env python3
"""
AnalysisDataFlow 推导链 PDF 生成脚本
生成8个PDF文件和索引页面
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from fpdf import FPDF
    from pypdf import PdfReader, PdfWriter
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Run: pip install fpdf2 pypdf")
    sys.exit(1)

# Paths
PDF_OUTPUT_DIR = PROJECT_ROOT / "pdf"
REPORTS_DIR = PROJECT_ROOT / "reports"
STRUCT_DIR = PROJECT_ROOT / "Struct"
KNOWLEDGE_DIR = PROJECT_ROOT / "Knowledge"

PDF_OUTPUT_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Colors
BLUE = (31, 78, 121)
GOLD = (197, 164, 100)
GRAY = (64, 64, 64)

# Font paths
FONT_PATH = Path("C:/Windows/Fonts/simsun.ttc")


class SimplePDF(FPDF):
    """Simplified PDF generator"""
    
    def __init__(self, title=""):
        super().__init__()
        self.doc_title = title
        self.has_chinese_font = False
        self._setup_font()
        
    def _setup_font(self):
        """Setup Unicode font"""
        if FONT_PATH.exists():
            try:
                self.add_font('CN', '', str(FONT_PATH))
                self.add_font('CN', 'B', str(FONT_PATH))
                self.has_chinese_font = True
            except:
                pass
    
    def _font(self, style='', size=10):
        """Set font with fallback"""
        if self.has_chinese_font:
            self.set_font('CN', style, size)
        else:
            self.set_font('Arial', style, size)
    
    def header(self):
        if self.page_no() > 2:
            self._font('', 8)
            self.set_text_color(*GRAY)
            self.cell(0, 10, f"AnalysisDataFlow", 0, align='L')
            self.cell(0, 10, f"Page {self.page_no()}", 0, align='R')
            self.ln(12)
    
    def footer(self):
        if self.page_no() > 2:
            self.set_y(-15)
            self._font('', 8)
            self.set_text_color(*GRAY)
            self.cell(0, 10, f"- {self.page_no()} -", 0, align='C')


def clean_text(text: str) -> str:
    """Clean markdown text"""
    # Remove links
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove images
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', text)
    # Remove HTML
    text = re.sub(r'<[^>]+>', '', text)
    # Remove formatting
    text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Keep only safe chars
    text = re.sub(r'[^\w\s\-\(\)\[\]|,\.:\/]', ' ', text)
    return text.strip()[:500]  # Limit length


def generate_pdf(source: Path, output: Path, title: str, subtitle: str) -> Dict:
    """Generate PDF from markdown"""
    
    if not source.exists():
        return None
    
    content = source.read_text(encoding='utf-8')
    
    pdf = SimplePDF(title)
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # Cover
    pdf.add_page()
    pdf.set_fill_color(*BLUE)
    pdf.rect(0, 0, 210, 100, 'F')
    
    pdf.set_y(30)
    pdf._font('', 14)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'ANALYSISDATAFLOW', 0, align='C')
    pdf.ln(20)
    
    pdf._font('B', 20)
    pdf.cell(0, 12, title[:40], 0, align='C')
    pdf.ln(15)
    
    pdf._font('', 11)
    pdf.set_text_color(230, 230, 230)
    pdf.cell(0, 10, subtitle[:50], 0, align='C')
    
    pdf.set_y(140)
    pdf.set_text_color(*GRAY)
    pdf._font('', 10)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d')}", 0, align='C')
    
    # TOC placeholder
    pdf.add_page()
    pdf._font('B', 16)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 15, 'Contents', 0, align='C')
    pdf.ln(15)
    pdf._font('', 10)
    pdf.cell(0, 8, '(Document content follows)', 0, align='C')
    
    # Content
    pdf.add_page()
    lines = content.split('\n')
    code_buffer = []
    in_code = False
    
    for line in lines[:300]:  # Limit lines
        stripped = line.strip()
        
        if stripped.startswith('```'):
            in_code = not in_code
            if not in_code and code_buffer:
                pdf.set_font('Courier', '', 8)
                pdf.set_fill_color(240, 240, 240)
                for code in code_buffer[:20]:
                    safe = code[:90].encode('ascii', 'ignore').decode()
                    pdf.cell(0, 5, safe or ' ', 0, new_x="LMARGIN", new_y="NEXT", fill=True)
                code_buffer = []
                pdf.ln(2)
            continue
        
        if in_code:
            code_buffer.append(stripped)
            continue
        
        if stripped.startswith('```mermaid'):
            in_code = True
            continue
        
        # Headers
        if stripped.startswith('# '):
            pdf.ln(5)
            pdf._font('B', 14)
            pdf.set_text_color(*BLUE)
            text = clean_text(stripped[2:])[:60]
            pdf.cell(0, 10, text, 0, new_x="LMARGIN", new_y="NEXT")
            continue
        
        if stripped.startswith('## '):
            pdf.ln(3)
            pdf._font('B', 12)
            pdf.set_text_color(*BLUE)
            text = clean_text(stripped[3:])[:70]
            pdf.cell(0, 8, text, 0, new_x="LMARGIN", new_y="NEXT")
            continue
        
        if stripped.startswith('### '):
            pdf.ln(2)
            pdf._font('B', 10)
            pdf.set_text_color(*GRAY)
            text = clean_text(stripped[4:])[:80]
            pdf.cell(0, 6, text, 0, new_x="LMARGIN", new_y="NEXT")
            continue
        
        # Skip tables and complex elements
        if '|' in stripped:
            continue
        
        # Lists
        if stripped.startswith(('- ', '* ')):
            pdf._font('', 9)
            pdf.set_text_color(*GRAY)
            text = clean_text(stripped[2:])[:100]
            pdf.cell(5, 5, '', 0)
            pdf.cell(0, 5, f'- {text}', 0, new_x="LMARGIN", new_y="NEXT")
            continue
        
        # Numbered lists
        if re.match(r'^\d+\.', stripped):
            pdf._font('', 9)
            pdf.set_text_color(*GRAY)
            text = clean_text(stripped)[:100]
            pdf.cell(0, 5, text, 0, new_x="LMARGIN", new_y="NEXT")
            continue
        
        # Quotes
        if stripped.startswith('>'):
            pdf._font('', 9)
            pdf.set_text_color(100, 100, 100)
            text = clean_text(stripped[1:])[:100]
            pdf.cell(5, 5, '', 0)
            pdf.cell(0, 5, text, 0, new_x="LMARGIN", new_y="NEXT")
            continue
        
        # Paragraphs
        if stripped:
            pdf._font('', 9)
            pdf.set_text_color(*GRAY)
            text = clean_text(stripped)[:120]
            pdf.cell(0, 5, text, 0, new_x="LMARGIN", new_y="NEXT")
    
    pdf.output(str(output))
    
    # Stats
    size = output.stat().st_size
    reader = PdfReader(str(output))
    pages = len(reader.pages)
    
    return {'file': output.name, 'path': output, 'size': size, 'pages': pages}


def merge_pdfs(files: List[Path], output: Path, title: str, subtitle: str) -> Dict:
    """Merge PDFs with cover"""
    
    if not files:
        return None
    
    # Create cover
    cover_pdf = SimplePDF(title)
    cover_pdf.add_page()
    cover_pdf.set_fill_color(*BLUE)
    cover_pdf.rect(0, 0, 210, 100, 'F')
    cover_pdf.set_y(30)
    cover_pdf._font('', 14)
    cover_pdf.set_text_color(255, 255, 255)
    cover_pdf.cell(0, 10, 'ANALYSISDATAFLOW', 0, align='C')
    cover_pdf.ln(20)
    cover_pdf._font('B', 20)
    cover_pdf.cell(0, 12, title[:40], 0, align='C')
    cover_pdf.ln(15)
    cover_pdf._font('', 11)
    cover_pdf.set_text_color(230, 230, 230)
    cover_pdf.cell(0, 10, subtitle[:50], 0, align='C')
    
    temp_cover = PDF_OUTPUT_DIR / "_cover.pdf"
    cover_pdf.output(str(temp_cover))
    
    # Merge
    writer = PdfWriter()
    
    cover_reader = PdfReader(str(temp_cover))
    for page in cover_reader.pages:
        writer.add_page(page)
    
    for f in files:
        if f.exists():
            try:
                r = PdfReader(str(f))
                for page in r.pages:
                    writer.add_page(page)
            except:
                pass
    
    with open(output, 'wb') as f:
        writer.write(f)
    
    temp_cover.unlink(missing_ok=True)
    
    size = output.stat().st_size
    reader = PdfReader(str(output))
    pages = len(reader.pages)
    
    return {'file': output.name, 'path': output, 'size': size, 'pages': pages}


def generate_index(stats: List[Dict]):
    """Generate HTML index"""
    
    total_pages = sum(s['pages'] for s in stats)
    total_size = sum(s['size'] for s in stats)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AnalysisDataFlow PDF Index</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh; margin: 0; padding: 40px 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{ text-align: center; margin-bottom: 40px; }}
        h1 {{ color: #1f4e79; font-size: 2.5rem; margin-bottom: 10px; }}
        .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 40px; }}
        .stat-card {{ background: white; border-radius: 12px; padding: 25px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
        .stat-card .num {{ font-size: 2.5rem; font-weight: bold; color: #1f4e79; }}
        .stat-card .lbl {{ color: #666; margin-top: 5px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px; }}
        .card {{ background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
        .card h2 {{ color: #1f4e79; font-size: 1.3rem; margin-bottom: 10px; }}
        .meta {{ display: flex; gap: 15px; margin-bottom: 20px; font-size: 0.85rem; color: #666; }}
        .meta span {{ background: #f0f4f8; padding: 4px 12px; border-radius: 20px; }}
        .btn {{ display: inline-block; background: linear-gradient(135deg, #1f4e79, #3a7bd5); color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 500; }}
        footer {{ text-align: center; padding: 40px 0; color: #666; margin-top: 40px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>AnalysisDataFlow PDF Documents</h1>
            <p>Derivation Chain Documentation</p>
        </header>
        <div class="stats">
            <div class="stat-card"><div class="num">{len(stats)}</div><div class="lbl">PDFs</div></div>
            <div class="stat-card"><div class="num">{total_pages}</div><div class="lbl">Total Pages</div></div>
            <div class="stat-card"><div class="num">{total_size//1024} KB</div><div class="lbl">Total Size</div></div>
        </div>
        <div class="grid">
"""
    
    for s in stats:
        html += f"""
            <div class="card">
                <h2>{s['file'].replace('.pdf','')}</h2>
                <div class="meta"><span>{s['pages']} Pages</span><span>{s['size']//1024} KB</span></div>
                <a href="{s['file']}" class="btn" download>Download PDF</a>
            </div>
"""
    
    html += f"""
        </div>
        <footer>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | AnalysisDataFlow Project</footer>
    </div>
</body>
</html>
"""
    
    (PDF_OUTPUT_DIR / "index.html").write_text(html, encoding='utf-8')


def main():
    print("=" * 60)
    print("AnalysisDataFlow PDF Generator")
    print("=" * 60)
    print()
    
    tasks = [
        ('Proof-Chains-Checkpoint.pdf', STRUCT_DIR / 'Proof-Chains-Checkpoint-Correctness.md',
         'Checkpoint Proof Chain', 'Fault Tolerance'),
        ('Proof-Chains-Exactly-Once.pdf', STRUCT_DIR / 'Proof-Chains-Exactly-Once-Correctness.md',
         'Exactly-Once Proof Chain', 'Consistency'),
        ('Proof-Chains-Encoding.pdf', STRUCT_DIR / 'Proof-Chains-Cross-Model-Encoding.md',
         'Encoding Proof Chain', 'Model Translation'),
        ('Foundation-Complete.pdf', STRUCT_DIR / 'Proof-Chains-Foundation-Complete.md',
         'Foundation Chains', 'Core Theory'),
        ('Properties-Complete.pdf', STRUCT_DIR / 'Proof-Chains-Properties-Complete.md',
         'Property Chains', 'Lemmas'),
        ('Flink-Complete.pdf', STRUCT_DIR / 'Proof-Chains-Flink-Complete.md',
         'Flink Proof Chain', 'Implementation'),
        ('Knowledge-Mapping.pdf', KNOWLEDGE_DIR / 'Knowledge-to-Flink-Mapping.md',
         'Knowledge Mapping', 'Bridge'),
    ]
    
    stats = []
    
    for name, src, title, sub in tasks:
        out = PDF_OUTPUT_DIR / name
        print(f"Generating {name}...")
        
        result = generate_pdf(src, out, title, sub)
        if result:
            stats.append(result)
            print(f"  OK: {result['pages']} pages, {result['size']//1024} KB")
        else:
            print(f"  Skipped")
    
    # Complete merge
    print()
    print("Generating Proof-Chains-Complete.pdf...")
    chain_files = [
        STRUCT_DIR / 'Proof-Chains-Foundation-Complete.md',
        STRUCT_DIR / 'Proof-Chains-Checkpoint-Correctness.md',
        STRUCT_DIR / 'Proof-Chains-Exactly-Once-Correctness.md',
        STRUCT_DIR / 'Proof-Chains-Cross-Model-Encoding.md',
    ]
    
    temps = []
    for i, f in enumerate(chain_files):
        if f.exists():
            t = PDF_OUTPUT_DIR / f"_t{i}.pdf"
            r = generate_pdf(f, t, f"Part {i+1}", "")
            if r:
                temps.append(t)
    
    if temps:
        complete = PDF_OUTPUT_DIR / "Proof-Chains-Complete.pdf"
        r = merge_pdfs(temps, complete, "Complete Proof Chains", "All Derivation Chains")
        if r:
            stats.append(r)
            print(f"  OK: {r['pages']} pages, {r['size']//1024} KB")
        for t in temps:
            t.unlink(missing_ok=True)
    
    # Index
    print()
    print("Generating index...")
    generate_index(stats)
    
    # Stats
    print()
    print("=" * 60)
    total_pages = sum(s['pages'] for s in stats)
    total_size = sum(s['size'] for s in stats)
    print(f"PDFs: {len(stats)} | Pages: {total_pages} | Size: {total_size//1024} KB")
    print()
    for s in stats:
        print(f"  {s['file']}: {s['pages']}p, {s['size']//1024}KB")
    
    # Log
    log = f"""PDF Generation Log
Time: {datetime.now().isoformat()}
Status: Success

Statistics:
- Total PDFs: {len(stats)}
- Total Pages: {total_pages}
- Total Size: {total_size//1024} KB

Files:
"""
    for s in stats:
        log += f"- {s['file']}: {s['pages']} pages, {s['size']//1024} KB\n"
    
    (REPORTS_DIR / "pdf-generation-log.txt").write_text(log, encoding='utf-8')
    
    return {'count': len(stats), 'pages': total_pages, 'size': total_size}


if __name__ == "__main__":
    main()
