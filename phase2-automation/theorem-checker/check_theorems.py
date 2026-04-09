#!/usr/bin/env python3
"""
Theorem Number Checker - Phase 2 Task 5-4
Validates theorem and definition numbering consistency.

Usage:
    python check_theorems.py [directory]

Checks:
- Theorem IDs follow format: {Type}-{Stage}-{Doc}-{Num}
- No duplicate theorem IDs
- Sequential numbering within documents
- References to undefined theorems
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Valid theorem types
THEOREM_TYPES = ['Thm', 'Def', 'Lemma', 'Prop', 'Cor', 'Axiom']
# Valid stages
STAGES = ['S', 'K', 'F']  # Struct, Knowledge, Flink

class TheoremChecker:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.theorems = defaultdict(list)  # theorem_id -> [locations]
        self.refs = defaultdict(list)  # theorem_id -> [reference locations]
        self.errors = []
        self.warnings = []
        
    def scan_files(self):
        """Scan all markdown files."""
        return list(self.root_dir.rglob("*.md"))
    
    def is_valid_theorem_id(self, theorem_id):
        """Check if theorem ID follows valid format."""
        pattern = r'^(Thm|Def|Lemma|Prop|Cor|Axiom)-[SKF]-\d{2}-\d{2}$'
        return re.match(pattern, theorem_id) is not None
    
    def extract_theorems(self, file_path):
        """Extract theorem definitions from file."""
        content = file_path.read_text(encoding='utf-8')
        theorems = []
        
        # Pattern for theorem definitions
        # Matches: **Thm-S-01-01** or ### Thm-S-01-01 或 Def-S-01-01:
        patterns = [
            r'\*\*(Thm|Def|Lemma|Prop|Cor|Axiom)-([SKF])-(\d{2})-(\d{2})\*\*',
            r'###?\s+(Thm|Def|Lemma|Prop|Cor|Axiom)-([SKF])-(\d{2})-(\d{2})',
            r'^(Thm|Def|Lemma|Prop|Cor|Axiom)-([SKF])-(\d{2})-(\d{2})\s*:',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                theorem_id = f"{match.group(1)}-{match.group(2)}-{match.group(3)}-{match.group(4)}"
                line_num = content[:match.start()].count('\n') + 1
                theorems.append({
                    'id': theorem_id,
                    'line': line_num,
                    'type': match.group(1),
                    'stage': match.group(2),
                    'doc': match.group(3),
                    'num': match.group(4),
                    'context': content[max(0, match.start()-50):match.end()+50]
                })
        
        return theorems
    
    def extract_refs(self, file_path):
        """Extract theorem references from file."""
        content = file_path.read_text(encoding='utf-8')
        refs = []
        
        # Pattern for theorem references (but not definitions)
        patterns = [
            r'(?:see|in|by|from|引用|根据|见)\s+(Thm|Def|Lemma|Prop|Cor|Axiom)-([SKF])-(\d{2})-(\d{2})',
            r'\[(Thm|Def|Lemma|Prop|Cor|Axiom)-([SKF])-(\d{2})-(\d{2})\](?!\s*:)',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                theorem_id = f"{match.group(1)}-{match.group(2)}-{match.group(3)}-{match.group(4)}"
                line_num = content[:match.start()].count('\n') + 1
                refs.append({
                    'id': theorem_id,
                    'line': line_num,
                    'context': content[max(0, match.start()-30):match.end()+30]
                })
        
        return refs
    
    def check_file(self, file_path):
        """Check a single file."""
        relative_path = file_path.relative_to(self.root_dir)
        
        # Extract theorems
        file_theorems = self.extract_theorems(file_path)
        for t in file_theorems:
            self.theorems[t['id']].append({
                'file': str(relative_path),
                'line': t['line'],
                'context': t['context']
            })
            
            # Validate format
            if not self.is_valid_theorem_id(t['id']):
                self.errors.append({
                    'type': 'invalid_format',
                    'theorem_id': t['id'],
                    'file': str(relative_path),
                    'line': t['line'],
                    'message': f'Invalid theorem ID format: {t["id"]}'
                })
        
        # Extract references
        file_refs = self.extract_refs(file_path)
        for r in file_refs:
            self.refs[r['id']].append({
                'file': str(relative_path),
                'line': r['line'],
                'context': r['context']
            })
    
    def check_duplicates(self):
        """Check for duplicate theorem IDs."""
        for theorem_id, locations in self.theorems.items():
            if len(locations) > 1:
                self.errors.append({
                    'type': 'duplicate',
                    'theorem_id': theorem_id,
                    'locations': locations,
                    'message': f'Theorem {theorem_id} defined {len(locations)} times'
                })
    
    def check_undefined_refs(self):
        """Check for references to undefined theorems."""
        for ref_id, locations in self.refs.items():
            if ref_id not in self.theorems:
                for loc in locations:
                    self.errors.append({
                        'type': 'undefined_reference',
                        'theorem_id': ref_id,
                        'file': loc['file'],
                        'line': loc['line'],
                        'message': f'Reference to undefined theorem: {ref_id}'
                    })
    
    def check_sequential(self):
        """Check sequential numbering within documents."""
        # Group by stage and doc
        doc_theorems = defaultdict(list)
        for theorem_id, locations in self.theorems.items():
            parts = theorem_id.split('-')
            if len(parts) == 4:
                key = f"{parts[1]}-{parts[2]}"  # Stage-Doc
                doc_theorems[key].append(int(parts[3]))
        
        for doc_key, nums in doc_theorems.items():
            nums.sort()
            for i in range(len(nums) - 1):
                if nums[i+1] - nums[i] > 1:
                    self.warnings.append({
                        'type': 'non_sequential',
                        'doc': doc_key,
                        'missing': list(range(nums[i] + 1, nums[i+1])),
                        'message': f'Non-sequential numbering in {doc_key}: missing {nums[i] + 1}'
                    })
    
    def generate_report(self):
        """Generate validation report."""
        return {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_theorems': len(self.theorems),
                'total_refs': sum(len(v) for v in self.refs.values()),
                'errors': len(self.errors),
                'warnings': len(self.warnings)
            },
            'theorems': dict(self.theorems),
            'errors': self.errors,
            'warnings': self.warnings
        }
    
    def print_report(self, report):
        """Print report to console."""
        print("\n" + "="*60)
        print("THEOREM NUMBER CHECKER REPORT")
        print("="*60)
        print(f"Total theorems found: {report['summary']['total_theorems']}")
        print(f"Total references: {report['summary']['total_refs']}")
        print(f"Errors: {report['summary']['errors']}")
        print(f"Warnings: {report['summary']['warnings']}")
        print("="*60)
        
        if self.errors:
            print("\n❌ ERRORS:")
            for err in self.errors[:10]:
                print(f"  [{err['type']}] {err['message']}")
                if 'file' in err:
                    print(f"    File: {err['file']}:{err.get('line', 'N/A')}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more errors")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warn in self.warnings[:5]:
                print(f"  [{warn['type']}] {warn['message']}")

def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"AnalysisDataFlow Theorem Number Checker")
    print(f"Scanning directory: {directory}\n")
    
    checker = TheoremChecker(directory)
    
    # Scan files
    files = checker.scan_files()
    print(f"Found {len(files)} markdown files")
    
    # Check each file
    for i, file_path in enumerate(files, 1):
        if i % 100 == 0:
            print(f"Processed {i}/{len(files)} files...")
        checker.check_file(file_path)
    
    # Run checks
    checker.check_duplicates()
    checker.check_undefined_refs()
    checker.check_sequential()
    
    # Generate report
    report = checker.generate_report()
    
    # Output
    checker.print_report(report)
    
    # Save report
    with open('theorem-check-report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\nReport saved to: theorem-check-report.json")
    
    # Exit with error code if errors found
    sys.exit(0 if not checker.errors else 1)

if __name__ == '__main__':
    main()
