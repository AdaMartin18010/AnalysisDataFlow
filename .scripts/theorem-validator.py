#!/usr/bin/env python3
"""
Theorem Numbering System Validator
====================================
 Validates theorem/def/lemma/prop/cor numbering across all project documents.

 Features:
 - Detects duplicate numbers
 - Checks continuity
 - Validates format consistency
 - Generates detailed reports
 - CI/CD integration ready

 Version: 1.0.0
 Date: 2026-04-12
"""

import os
import re
import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Numbering pattern: {Type}-{Stage}-{DocNum}-{SeqNum}
# Types: Thm, Def, Lemma, Prop, Cor
# Stages: S (Struct), K (Knowledge), F (Flink), G (Go), R (Rust), A (AI), C (Cross)
NUMBERING_PATTERN = re.compile(
    r'\b(Thm|Def|Lemma|Prop|Cor)-([SFKGRACU])-(\d{2}(?:-\d{2})?)-(\d{2,3})\b',
    re.IGNORECASE
)

# Pattern to detect actual definitions (e.g., "**Def-S-01-01**" or "> Def-S-01-01" or "#### Def-S-01-01")
DEFINITION_PATTERN = re.compile(
    r'^(\*\*|>\s*|####\s*|#####\s*|#{1,6}\s*)?(Thm|Def|Lemma|Prop|Cor)-([SFKGRACU])-(\d{2}(?:-\d{2})?)-(\d{2,3})\b',
    re.IGNORECASE
)

# Alternative patterns found in the project
ALT_PATTERNS = [
    re.compile(r'\b(Thm|Def|Lemma|Prop|Cor)-([SFKGRAC])-(\d{2,3})-(\d{2,3})\b', re.IGNORECASE),
    re.compile(r'\b(Thm|Def|Lemma|Prop|Cor)-([SFKGRAC])-([A-Za-z]+)-(\d{2,3})\b', re.IGNORECASE),
]

# Element type names
TYPE_NAMES = {
    'Thm': 'Theorem',
    'Def': 'Definition', 
    'Lemma': 'Lemma',
    'Prop': 'Proposition',
    'Cor': 'Corollary'
}

STAGE_NAMES = {
    'S': 'Struct',
    'K': 'Knowledge', 
    'F': 'Flink',
    'G': 'Go',
    'R': 'Rust',
    'A': 'AI',
    'C': 'Cross',
    'U': 'Unified'
}

class TheoremValidator:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.elements = []  # All found definitions
        self.references = []  # All found references
        self.issues = []    # All detected issues
        self.stats = defaultdict(int)
        self.duplicates = defaultdict(list)
        self.by_file = defaultdict(list)
        self.by_type_stage = defaultdict(list)
        self.orphaned = []  # Elements not in registry
        
    def scan_document(self, filepath: Path) -> Tuple[List[Dict], List[Dict]]:
        """Scan a single document for theorem/def/lemma/prop/cor.
        
        Returns:
            Tuple of (definitions, references)
        """
        definitions = []
        references = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
            for line_num, line in enumerate(lines, 1):
                # Skip code blocks
                if line.strip().startswith('```'):
                    continue
                    
                # Check for definitions (bold, blockquote, or heading)
                def_match = DEFINITION_PATTERN.search(line)
                is_definition = def_match is not None
                    
                matches = NUMBERING_PATTERN.findall(line)
                for match in matches:
                    elem_type, stage, doc_num, seq_num = match
                    element = {
                        'type': elem_type.capitalize(),
                        'stage': stage.upper(),
                        'doc_num': doc_num,
                        'seq_num': seq_num,
                        'line': line_num,
                        'content': line.strip()[:100],
                        'file': str(filepath.relative_to(self.root_dir)),
                        'full_id': f"{elem_type.capitalize()}-{stage.upper()}-{doc_num}-{seq_num}"
                    }
                    
                    # Determine if this is a definition or reference
                    # A definition is typically:
                    # - In a heading (### Def-X-XX-XX)
                    # - Bold (**Def-X-XX-XX**)
                    # - In a table row starting with the element
                    # - In a blockquote (> Def-X-XX-XX)
                    line_stripped = line.strip()
                    is_def = (
                        line_stripped.startswith('#') or  # Heading
                        line_stripped.startswith('>') or   # Blockquote
                        '**' + element['full_id'] + '**' in line or  # Bold
                        ('|' in line and line.strip().startswith('|') and element['full_id'] in line.split('|')[1] if len(line.split('|')) > 1 else False)  # Table first column
                    )
                    
                    if is_def:
                        element['is_definition'] = True
                        definitions.append(element)
                    else:
                        element['is_definition'] = False
                        references.append(element)
                    
        except Exception as e:
            print(f"{Colors.WARNING}Warning: Could not read {filepath}: {e}{Colors.ENDC}")
            
        return definitions, references
    
    def scan_all_documents(self, directories: List[str] = None):
        """Scan all markdown documents in specified directories."""
        if directories is None:
            directories = ['Struct', 'Knowledge', 'Flink']
            
        print(f"{Colors.HEADER}Scanning documents...{Colors.ENDC}")
        
        all_defs = []
        all_refs = []
        
        for directory in directories:
            dir_path = self.root_dir / directory
            if not dir_path.exists():
                print(f"{Colors.WARNING}Directory not found: {directory}{Colors.ENDC}")
                continue
                
            for md_file in dir_path.rglob('*.md'):
                definitions, references = self.scan_document(md_file)
                all_defs.extend(definitions)
                all_refs.extend(references)
                
                for elem in definitions + references:
                    self.by_file[elem['file']].append(elem)
                    key = (elem['type'], elem['stage'], elem['doc_num'])
                    self.by_type_stage[key].append(elem)
                    
        # Use definitions as primary elements for validation
        self.elements = all_defs
        self.references = all_refs
        
        print(f"{Colors.OKGREEN}Found {len(all_defs)} definitions and {len(all_refs)} references across {len(self.by_file)} files{Colors.ENDC}")
        
    def check_duplicates(self):
        """Check for duplicate numbering."""
        print(f"{Colors.HEADER}Checking for duplicates...{Colors.ENDC}")
        
        seen = defaultdict(list)
        for elem in self.elements:
            seen[elem['full_id']].append(elem)
            
        for elem_id, occurrences in seen.items():
            if len(occurrences) > 1:
                self.duplicates[elem_id] = occurrences
                self.issues.append({
                    'type': 'duplicate',
                    'element_id': elem_id,
                    'count': len(occurrences),
                    'locations': [(e['file'], e['line']) for e in occurrences]
                })
                
        if self.duplicates:
            print(f"{Colors.FAIL}Found {len(self.duplicates)} duplicate IDs{Colors.ENDC}")
        else:
            print(f"{Colors.OKGREEN}No duplicates found{Colors.ENDC}")
            
    def check_continuity(self):
        """Check numbering continuity within each document."""
        print(f"{Colors.HEADER}Checking continuity...{Colors.ENDC}")
        
        # Group by stage, doc_num, and type
        by_group = defaultdict(list)
        for elem in self.elements:
            key = (elem['stage'], elem['doc_num'], elem['type'])
            by_group[key].append(int(elem['seq_num']))
            
        gaps_found = 0
        for key, seq_nums in by_group.items():
            seq_nums = sorted(set(seq_nums))
            if len(seq_nums) < 2:
                continue
                
            for i in range(1, len(seq_nums)):
                if seq_nums[i] - seq_nums[i-1] > 1:
                    gaps_found += 1
                    self.issues.append({
                        'type': 'gap',
                        'stage': key[0],
                        'doc_num': key[1],
                        'elem_type': key[2],
                        'expected': seq_nums[i-1] + 1,
                        'found': seq_nums[i]
                    })
                    
        if gaps_found:
            print(f"{Colors.WARNING}Found {gaps_found} numbering gaps{Colors.ENDC}")
        else:
            print(f"{Colors.OKGREEN}No continuity issues found{Colors.ENDC}")
            
    def check_format_consistency(self):
        """Check for format inconsistencies."""
        print(f"{Colors.HEADER}Checking format consistency...{Colors.ENDC}")
        
        format_issues = 0
        for elem in self.elements:
            # Check if seq_num has leading zeros
            if elem['seq_num'] != elem['seq_num'].zfill(2 if len(elem['seq_num']) <= 2 else 3):
                format_issues += 1
                self.issues.append({
                    'type': 'format',
                    'element_id': elem['full_id'],
                    'file': elem['file'],
                    'line': elem['line'],
                    'message': 'Inconsistent number padding'
                })
                
        if format_issues:
            print(f"{Colors.WARNING}Found {format_issues} format issues{Colors.ENDC}")
        else:
            print(f"{Colors.OKGREEN}No format issues found{Colors.ENDC}")
            
    def compare_with_registry(self, registry_path: str = "THEOREM-REGISTRY.md"):
        """Compare found elements with THEOREM-REGISTRY.md."""
        print(f"{Colors.HEADER}Comparing with registry...{Colors.ENDC}")
        
        registry_file = self.root_dir / registry_path
        if not registry_file.exists():
            print(f"{Colors.WARNING}Registry not found at {registry_path}{Colors.ENDC}")
            return
            
        try:
            with open(registry_file, 'r', encoding='utf-8') as f:
                registry_content = f.read()
                
            registry_pattern = re.compile(r'\b(Thm|Def|Lemma|Prop|Cor)-([SFKGRACU])-(\d{2}(?:-\d{2})?)-(\d{2,3})\b')
            registry_ids = set(m[0] for m in registry_pattern.findall(registry_content))
            found_ids = set(e['full_id'] for e in self.elements)
            
            # Elements in docs but not in registry
            not_in_registry = found_ids - registry_ids
            for elem_id in not_in_registry:
                elem = next(e for e in self.elements if e['full_id'] == elem_id)
                self.orphaned.append(elem)
                self.issues.append({
                    'type': 'orphan',
                    'element_id': elem_id,
                    'file': elem['file'],
                    'line': elem['line'],
                    'message': 'Not found in THEOREM-REGISTRY.md'
                })
                
            # Elements in registry but not found in docs
            not_in_docs = registry_ids - found_ids
            for elem_id in not_in_docs:
                self.issues.append({
                    'type': 'missing_in_docs',
                    'element_id': elem_id,
                    'message': 'In registry but not found in documents'
                })
                
            print(f"{Colors.OKBLUE}Registry comparison:{Colors.ENDC}")
            print(f"  - In docs, not registry: {len(not_in_registry)}")
            print(f"  - In registry, not docs: {len(not_in_docs)}")
            
        except Exception as e:
            print(f"{Colors.FAIL}Error reading registry: {e}{Colors.ENDC}")
            
    def generate_statistics(self) -> Dict:
        """Generate comprehensive statistics."""
        stats = {
            'total_definitions': len(self.elements),
            'total_references': len(self.references),
            'by_type': dict(Counter(e['type'] for e in self.elements)),
            'by_stage': dict(Counter(e['stage'] for e in self.elements)),
            'by_doc': {f"{k[0]}-{k[1]}": v for k, v in Counter((e['stage'], e['doc_num']) for e in self.elements).items()},
            'files_scanned': len(self.by_file),
            'duplicates': len(self.duplicates),
            'orphaned': len(self.orphaned),
            'total_issues': len(self.issues)
        }
        
        # Calculate per-stage breakdown
        stats['stage_breakdown'] = {}
        for stage in STAGE_NAMES.keys():
            stage_elems = [e for e in self.elements if e['stage'] == stage]
            if stage_elems:
                stats['stage_breakdown'][stage] = {
                    'total': len(stage_elems),
                    'by_type': dict(Counter(e['type'] for e in stage_elems)),
                    'files': len(set(e['file'] for e in stage_elems))
                }
                
        return stats
        
    def generate_report(self, output_path: str = "theorem-validation-report.json"):
        """Generate validation report."""
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': self.generate_statistics(),
            'issues': self.issues,
            'duplicates': {k: [
                {'file': e['file'], 'line': e['line'], 'content': e['content']}
                for e in v
            ] for k, v in self.duplicates.items()},
            'orphaned': self.orphaned
        }
        
        output_file = self.root_dir / output_path
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"{Colors.OKGREEN}Report saved to {output_file}{Colors.ENDC}")
        return report
        
    def print_summary(self):
        """Print summary to console."""
        stats = self.generate_statistics()
        
        print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}VALIDATION SUMMARY{Colors.ENDC}")
        print(f"{Colors.BOLD}{'='*60}{Colors.ENDC}")
        
        print(f"\n{Colors.HEADER}Total Definitions Found:{Colors.ENDC} {stats['total_definitions']}")
        print(f"{Colors.HEADER}Total References Found:{Colors.ENDC} {stats['total_references']}")
        print(f"{Colors.HEADER}Files Scanned:{Colors.ENDC} {stats['files_scanned']}")
        
        print(f"\n{Colors.HEADER}By Type:{Colors.ENDC}")
        for elem_type, count in sorted(stats['by_type'].items()):
            print(f"  {TYPE_NAMES.get(elem_type, elem_type)}: {count}")
            
        print(f"\n{Colors.HEADER}By Stage:{Colors.ENDC}")
        for stage, count in sorted(stats['by_stage'].items()):
            print(f"  {STAGE_NAMES.get(stage, stage)}: {count}")
            
        print(f"\n{Colors.HEADER}Issues Found:{Colors.ENDC}")
        issue_types = Counter(i['type'] for i in self.issues)
        for issue_type, count in sorted(issue_types.items()):
            color = Colors.FAIL if issue_type in ['duplicate', 'format'] else Colors.WARNING
            print(f"  {color}{issue_type}: {count}{Colors.ENDC}")
            
        if not self.issues:
            print(f"  {Colors.OKGREEN}No issues found!{Colors.ENDC}")
        else:
            print(f"  {Colors.BOLD}Total: {len(self.issues)} issues{Colors.ENDC}")
            
        print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}")
        
    def run_all_checks(self):
        """Run all validation checks."""
        self.scan_all_documents()
        self.check_duplicates()
        self.check_continuity()
        self.check_format_consistency()
        self.compare_with_registry()
        self.print_summary()
        return self.generate_statistics()

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate theorem/def/lemma/prop/cor numbering across project documents'
    )
    parser.add_argument(
        '--root', '-r',
        default='.',
        help='Root directory of the project (default: current directory)'
    )
    parser.add_argument(
        '--output', '-o',
        default='theorem-validation-report.json',
        help='Output report path (default: theorem-validation-report.json)'
    )
    parser.add_argument(
        '--dirs', '-d',
        nargs='+',
        default=['Struct', 'Knowledge', 'Flink'],
        help='Directories to scan (default: Struct Knowledge Flink)'
    )
    parser.add_argument(
        '--ci',
        action='store_true',
        help='Exit with error code if issues found (for CI/CD)'
    )
    parser.add_argument(
        '--no-registry-check',
        action='store_true',
        help='Skip registry comparison'
    )
    
    args = parser.parse_args()
    
    validator = TheoremValidator(args.root)
    validator.scan_all_documents(args.dirs)
    validator.check_duplicates()
    validator.check_continuity()
    validator.check_format_consistency()
    
    if not args.no_registry_check:
        validator.compare_with_registry()
        
    validator.print_summary()
    report = validator.generate_report(args.output)
    
    # CI/CD exit code
    if args.ci and report['summary']['total_issues'] > 0:
        print(f"{Colors.FAIL}Validation failed with {report['summary']['total_issues']} issues{Colors.ENDC}")
        sys.exit(1)
        
    sys.exit(0)

if __name__ == '__main__':
    main()
