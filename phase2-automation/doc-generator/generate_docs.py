#!/usr/bin/env python3
"""
Documentation Generator - Phase 2 Automation Tool
Generates documentation artifacts from source files.
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

class DocumentationGenerator:
    def __init__(self, input_dir, output_dir):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_index(self):
        """Generate index page from directory structure."""
        index = {
            'title': 'AnalysisDataFlow Documentation Index',
            'generated': datetime.now().isoformat(),
            'sections': []
        }
        
        for section_dir in ['Struct', 'Knowledge', 'Flink']:
            section_path = self.input_dir / section_dir
            if section_path.exists():
                files = list(section_path.rglob('*.md'))
                index['sections'].append({
                    'name': section_dir,
                    'file_count': len(files),
                    'files': [str(f.relative_to(self.input_dir)) for f in files[:20]]
                })
        
        output_file = self.output_dir / 'index.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        
        print(f"Generated index: {output_file}")
        return index
    
    def generate_stats(self):
        """Generate project statistics."""
        stats = {
            'generated': datetime.now().isoformat(),
            'files': {},
            'lines': {}
        }
        
        for ext in ['.md', '.java', '.py', '.v', '.tla']:
            files = list(self.input_dir.rglob(f'*{ext}'))
            stats['files'][ext] = len(files)
            
            total_lines = 0
            for f in files:
                try:
                    total_lines += len(f.read_text(encoding='utf-8').split('\n'))
                except:
                    pass
            stats['lines'][ext] = total_lines
        
        output_file = self.output_dir / 'stats.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"Generated stats: {output_file}")
        return stats

def main():
    parser = argparse.ArgumentParser(description='Documentation Generator')
    parser.add_argument('--input', '-i', default='.', help='Input directory')
    parser.add_argument('--output', '-o', default='generated-docs', help='Output directory')
    args = parser.parse_args()
    
    print(f"Generating documentation from {args.input} to {args.output}")
    
    generator = DocumentationGenerator(args.input, args.output)
    generator.generate_index()
    generator.generate_stats()
    
    print("\nDocumentation generation complete!")

if __name__ == '__main__':
    main()
