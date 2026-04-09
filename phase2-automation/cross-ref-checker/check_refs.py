#!/usr/bin/env python3
"""
Cross-Reference Checker - Phase 2 Task 5-3
Checks cross-references between markdown documents.

Usage:
    python check_refs.py [directory]

Features:
- Checks internal document links
- Validates theorem/definition references
- Reports broken cross-references
- Generates detailed report
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class CrossRefChecker:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.defined_refs = {}  # ref_id -> file_path
        self.used_refs = defaultdict(list)  # ref_id -> [usage_locations]
        self.broken_refs = []
        self.warnings = []
        
    def scan_files(self):
        """Scan all markdown files."""
        return list(self.root_dir.rglob("*.md"))
    
    def extract_defined_refs(self, file_path):
        """Extract references defined in a file."""
        content = file_path.read_text(encoding='utf-8')
        refs = []
        
        # Pattern for theorem/definition/lemma definitions
        # Matches: **Def-S-01-01** or ### Def-S-01-01
        patterns = [
            r'\*\*(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d{2}-\d{2}\*\*',
            r'###?\s+(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d{2}-\d{2}',
            r'\[\^(\d+)\]:',  # Footnotes
            r'\{#([a-zA-Z0-9-_]+)\}',  # HTML anchors
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                ref_id = match.group(0)
                # Clean up the ref_id
                ref_id = re.sub(r'[*#\[\]\{\}]', '', ref_id)
                refs.append({
                    'id': ref_id,
                    'line': content[:match.start()].count('\n') + 1,
                    'context': content[max(0, match.start()-50):match.end()+50]
                })
        
        return refs
    
    def extract_used_refs(self, file_path):
        """Extract references used in a file."""
        content = file_path.read_text(encoding='utf-8')
        refs = []
        
        # Pattern for referencing theorems/definitions
        # Matches: see Thm-S-01-01 or [Def-S-01-01]
        patterns = [
            r'(?:see|in|by|from)\s+(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d{2}-\d{2}',
            r'\[(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d{2}-\d{2}\]',
            r'\[\^(\d+)\]',  # Footnote references
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                ref_id = match.group(0)
                # Clean up
                ref_id = re.sub(r'\[|\]', '', ref_id)
                ref_id = re.sub(r'(?:see|in|by|from)\s+', '', ref_id, flags=re.IGNORECASE)
                refs.append({
                    'id': ref_id,
                    'line': content[:match.start()].count('\n') + 1,
                    'context': content[max(0, match.start()-30):match.end()+30]
                })
        
        return refs
    
    def check_file_refs(self, file_path):
        """Check references in a single file."""
        relative_path = file_path.relative_to(self.root_dir)
        
        # Extract definitions
        defined = self.extract_defined_refs(file_path)
        for ref in defined:
            ref_id = ref['id']
            if ref_id in self.defined_refs:
                self.warnings.append({
                    'type': 'duplicate_definition',
                    'ref_id': ref_id,
                    'file': str(relative_path),
                    'line': ref['line'],
                    'previous_file': self.defined_refs[ref_id],
                    'message': f'Duplicate definition of {ref_id}'
                })
            else:
                self.defined_refs[ref_id] = str(relative_path)
        
        # Extract usages
        used = self.extract_used_refs(file_path)
        for ref in used:
            ref_id = ref['id']
            self.used_refs[ref_id].append({
                'file': str(relative_path),
                'line': ref['line'],
                'context': ref['context']
            })
    
    def validate_refs(self):
        """Validate all references."""
        for ref_id, usages in self.used_refs.items():
            if ref_id not in self.defined_refs:
                for usage in usages:
                    self.broken_refs.append({
                        'ref_id': ref_id,
                        'file': usage['file'],
                        'line': usage['line'],
                        'context': usage['context'],
                        'error': f'Reference {ref_id} not found'
                    })
    
    def generate_report(self):
        """Generate validation report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_files_scanned': 0,
                'total_defined_refs': len(self.defined_refs),
                'total_used_refs': len(self.used_refs),
                'broken_refs': len(self.broken_refs),
                'warnings': len(self.warnings),
                'success_rate': 0.0
            },
            'defined_refs': self.defined_refs,
            'broken_refs': self.broken_refs,
            'warnings': self.warnings
        }
        
        # Calculate success rate
        total_refs = len(self.used_refs)
        if total_refs > 0:
            valid_refs = total_refs - len(self.broken_refs)
            report['summary']['success_rate'] = (valid_refs / total_refs) * 100
        
        return report
    
    def save_report(self, report, output_file='cross-ref-report.json'):
        """Save report to file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Report saved to: {output_file}")
    
    def print_summary(self, report):
        """Print summary to console."""
        print("\n" + "="*60)
        print("CROSS-REFERENCE CHECK SUMMARY")
        print("="*60)
        print(f"Defined references: {report['summary']['total_defined_refs']}")
        print(f"Used references: {report['summary']['total_used_refs']}")
        print(f"Broken references: {report['summary']['broken_refs']}")
        print(f"Warnings: {report['summary']['warnings']}")
        print(f"Success rate: {report['summary']['success_rate']:.2f}%")
        print("="*60)
        
        if self.broken_refs:
            print("\nBroken References:")
            for ref in self.broken_refs[:10]:
                print(f"  [{ref['ref_id']}] in {ref['file']}:{ref['line']}")
            if len(self.broken_refs) > 10:
                print(f"  ... and {len(self.broken_refs) - 10} more")
        
        if self.warnings:
            print("\nWarnings:")
            for warn in self.warnings[:5]:
                print(f"  {warn['message']}")

def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"AnalysisDataFlow Cross-Reference Checker")
    print(f"Scanning directory: {directory}\n")
    
    checker = CrossRefChecker(directory)
    
    # Scan all files
    files = checker.scan_files()
    print(f"Found {len(files)} markdown files")
    
    # Check each file
    for i, file_path in enumerate(files, 1):
        if i % 100 == 0:
            print(f"Processed {i}/{len(files)} files...")
        checker.check_file_refs(file_path)
    
    # Validate
    checker.validate_refs()
    
    # Generate report
    report = checker.generate_report()
    report['summary']['total_files_scanned'] = len(files)
    
    # Output
    checker.print_summary(report)
    checker.save_report(report)
    
    # Exit with error code if broken refs found
    sys.exit(0 if not checker.broken_refs else 1)

if __name__ == '__main__':
    main()
