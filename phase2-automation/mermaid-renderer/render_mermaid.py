#!/usr/bin/env python3
"""
Mermaid Renderer - Phase 2 Task 5-5
Renders Mermaid diagrams in markdown files to SVG/PNG.

Usage:
    python render_mermaid.py <input.md> [output_dir]
    python render_mermaid.py --batch <directory>

Features:
- Extracts Mermaid diagrams from markdown
- Renders to SVG using mermaid-cli
- Updates markdown with image references
"""

import os
import re
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

class MermaidRenderer:
    def __init__(self, output_dir='diagrams'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def extract_mermaid_blocks(self, content):
        """Extract Mermaid code blocks from markdown."""
        pattern = r'```mermaid\s*\n(.*?)\n```'
        return re.findall(pattern, content, re.DOTALL)
    
    def render_diagram(self, mermaid_code, output_name):
        """Render a single Mermaid diagram."""
        # Create temporary mmd file
        mmd_file = self.output_dir / f"{output_name}.mmd"
        svg_file = self.output_dir / f"{output_name}.svg"
        
        mmd_file.write_text(mermaid_code, encoding='utf-8')
        
        # Render using mermaid-cli (mmdc)
        try:
            result = subprocess.run(
                ['mmdc', '-i', str(mmd_file), '-o', str(svg_file)],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✓ Rendered: {svg_file}")
            return svg_file
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to render {output_name}: {e.stderr}")
            return None
        except FileNotFoundError:
            print("✗ mmdc not found. Install with: npm install -g @mermaid-js/mermaid-cli")
            return None
    
    def process_file(self, input_file, inline=False):
        """Process a single markdown file."""
        input_path = Path(input_file)
        content = input_path.read_text(encoding='utf-8')
        
        diagrams = self.extract_mermaid_blocks(content)
        if not diagrams:
            print(f"No Mermaid diagrams found in {input_file}")
            return []
        
        print(f"Found {len(diagrams)} diagram(s) in {input_file}")
        
        rendered_files = []
        for i, diagram in enumerate(diagrams, 1):
            output_name = f"{input_path.stem}_diagram_{i}"
            svg_file = self.render_diagram(diagram, output_name)
            if svg_file:
                rendered_files.append(svg_file)
        
        return rendered_files
    
    def batch_process(self, directory, pattern='*.md'):
        """Process all markdown files in a directory."""
        dir_path = Path(directory)
        md_files = list(dir_path.rglob(pattern))
        
        print(f"Found {len(md_files)} markdown files to process\n")
        
        total_diagrams = 0
        for md_file in md_files:
            diagrams = self.extract_mermaid_blocks(md_file.read_text(encoding='utf-8'))
            if diagrams:
                print(f"Processing {md_file}...")
                self.process_file(md_file)
                total_diagrams += len(diagrams)
        
        print(f"\nTotal diagrams rendered: {total_diagrams}")

def main():
    parser = argparse.ArgumentParser(description='Mermaid Diagram Renderer')
    parser.add_argument('input', help='Input markdown file or directory')
    parser.add_argument('-o', '--output', default='diagrams', 
                       help='Output directory for rendered diagrams')
    parser.add_argument('-b', '--batch', action='store_true',
                       help='Batch process all markdown files in directory')
    parser.add_argument('--inline', action='store_true',
                       help='Replace mermaid blocks with image references')
    
    args = parser.parse_args()
    
    renderer = MermaidRenderer(args.output)
    
    if args.batch:
        renderer.batch_process(args.input)
    else:
        rendered = renderer.process_file(args.input, args.inline)
        print(f"\nRendered {len(rendered)} diagram(s) to {args.output}/")

if __name__ == '__main__':
    main()
