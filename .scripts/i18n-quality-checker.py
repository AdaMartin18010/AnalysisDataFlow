#!/usr/bin/env python3
"""
Internationalization Quality Checker for AnalysisDataFlow

This script performs quality checks on translated documentation:
1. Terminology consistency validation
2. Link validity checking
3. Format consistency verification
4. Missing translation detection

Usage:
    python i18n-quality-checker.py --check-terms       # Validate terminology
    python i18n-quality-checker.py --check-links       # Validate links
    python i18n-quality-checker.py --check-format      # Validate format
    python i18n-quality-checker.py --check-all         # Run all checks
    python i18n-quality-checker.py --generate-report   # Generate full report
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
EN_DIR = PROJECT_ROOT / "en"
GLOSSARY_FILE = PROJECT_ROOT / "GLOSSARY-en.md"


@dataclass
class CheckResult:
    """Result of a quality check."""
    check_name: str
    passed: bool
    issues: List[str]
    warnings: List[str]
    stats: Dict
    
    def to_dict(self):
        return {
            "check_name": self.check_name,
            "passed": self.passed,
            "issues": self.issues,
            "warnings": self.warnings,
            "stats": self.stats
        }


class TerminologyChecker:
    """Checks terminology consistency."""
    
    def __init__(self):
        self.terms: Dict[str, str] = {}  # English -> Chinese
        self.load_glossary()
    
    def load_glossary(self):
        """Load terms from GLOSSARY-en.md."""
        if not GLOSSARY_FILE.exists():
            return
        
        content = GLOSSARY_FILE.read_text(encoding='utf-8')
        
        # Parse terms using regex
        pattern = r'###\s+(\S+)\s*\n.*?-\s*\*\*中文\*\*:\s*(\S+)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for en_term, cn_term in matches:
            self.terms[en_term.lower()] = cn_term
    
    def check_document(self, file_path: Path) -> CheckResult:
        """Check terminology in a document."""
        issues = []
        warnings = []
        
        if not file_path.exists():
            return CheckResult(
                check_name="Terminology",
                passed=False,
                issues=[f"File not found: {file_path}"],
                warnings=[],
                stats={}
            )
        
        content = file_path.read_text(encoding='utf-8')
        found_terms = set()
        
        # Check for undefined terms
        # Look for potential Chinese terms in English docs
        chinese_chars = re.findall(r'[\u4e00-\u9fff]+', content)
        if chinese_chars:
            warnings.append(f"Found {len(chinese_chars)} Chinese character sequences")
        
        # Check for consistent term usage
        for en_term in self.terms:
            if en_term.lower() in content.lower():
                found_terms.add(en_term)
        
        stats = {
            "total_terms_in_glossary": len(self.terms),
            "terms_found_in_doc": len(found_terms),
            "chinese_sequences": len(chinese_chars)
        }
        
        return CheckResult(
            check_name="Terminology",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            stats=stats
        )


class LinkChecker:
    """Checks link validity."""
    
    def __init__(self):
        self.broken_links: List[str] = []
    
    def extract_links(self, content: str) -> List[Tuple[str, str]]:
        """Extract markdown links from content."""
        # Pattern for [text](url)
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        return re.findall(pattern, content)
    
    def check_link(self, link: str, base_path: Path) -> bool:
        """Check if a link is valid."""
        # Skip external links
        if link.startswith('http://') or link.startswith('https://'):
            return True
        
        # Skip anchors-only links
        if link.startswith('#'):
            return True
        
        # Handle relative links
        if link.startswith('./') or link.startswith('../') or not link.startswith('/'):
            target = base_path.parent / link
            target = target.resolve()
            
            if target.exists():
                return True
            
            # Try with .md extension
            if not link.endswith('.md'):
                target = base_path.parent / (link + '.md')
                if target.exists():
                    return True
        
        return False
    
    def check_document(self, file_path: Path) -> CheckResult:
        """Check links in a document."""
        issues = []
        warnings = []
        
        if not file_path.exists():
            return CheckResult(
                check_name="Links",
                passed=False,
                issues=[f"File not found: {file_path}"],
                warnings=[],
                stats={}
            )
        
        content = file_path.read_text(encoding='utf-8')
        links = self.extract_links(content)
        
        valid_count = 0
        invalid_count = 0
        external_count = 0
        
        for text, url in links:
            if url.startswith('http://') or url.startswith('https://'):
                external_count += 1
                continue
            
            if self.check_link(url, file_path):
                valid_count += 1
            else:
                invalid_count += 1
                issues.append(f"Broken link: [{text}]({url})")
        
        stats = {
            "total_links": len(links),
            "valid_links": valid_count,
            "broken_links": invalid_count,
            "external_links": external_count
        }
        
        return CheckResult(
            check_name="Links",
            passed=invalid_count == 0,
            issues=issues,
            warnings=warnings,
            stats=stats
        )


class FormatChecker:
    """Checks document format consistency."""
    
    REQUIRED_SECTIONS = [
        "Definitions",
        "Properties",
        "Relations",
        "Argumentation",
        "Proof",
        "Examples",
        "Visualizations",
        "References"
    ]
    
    def check_document(self, file_path: Path) -> CheckResult:
        """Check document format."""
        issues = []
        warnings = []
        
        if not file_path.exists():
            return CheckResult(
                check_name="Format",
                passed=False,
                issues=[f"File not found: {file_path}"],
                warnings=[],
                stats={}
            )
        
        content = file_path.read_text(encoding='utf-8')
        
        # Check for H1 title
        if not re.search(r'^#\s+.+$', content, re.MULTILINE):
            issues.append("Missing H1 title")
        
        # Check for language badges
        if 'img.shields.io/badge' not in content:
            warnings.append("Missing language badges")
        
        # Check for required sections (relaxed for index files)
        found_sections = []
        for section in self.REQUIRED_SECTIONS:
            # Match ## 1. Section or ## Section
            patterns = [
                rf'^##\s+\d+\.\s*{section}',
                rf'^##\s*{section}'
            ]
            for pattern in patterns:
                if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                    found_sections.append(section)
                    break
        
        # Index files can have different structure
        is_index = 'INDEX' in file_path.name.upper()
        
        if not is_index and len(found_sections) < 4:
            warnings.append(f"Only {len(found_sections)}/8 standard sections found")
        
        # Check Mermaid diagrams
        mermaid_count = len(re.findall(r'```mermaid', content))
        
        # Check code blocks
        code_block_count = len(re.findall(r'```[a-z]*', content))
        
        stats = {
            "sections_found": len(found_sections),
            "mermaid_diagrams": mermaid_count,
            "code_blocks": code_block_count,
            "is_index": is_index
        }
        
        return CheckResult(
            check_name="Format",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            stats=stats
        )


class I18NQualityChecker:
    """Main quality checker orchestrating all checks."""
    
    def __init__(self):
        self.terminology_checker = TerminologyChecker()
        self.link_checker = LinkChecker()
        self.format_checker = FormatChecker()
    
    def check_all_documents(self) -> Dict[str, List[CheckResult]]:
        """Run all checks on all English documents."""
        results = {}
        
        if not EN_DIR.exists():
            return results
        
        for doc in EN_DIR.glob("*.md"):
            results[doc.name] = self.check_document(doc)
        
        return results
    
    def check_document(self, file_path: Path) -> List[CheckResult]:
        """Run all checks on a single document."""
        return [
            self.terminology_checker.check_document(file_path),
            self.link_checker.check_document(file_path),
            self.format_checker.check_document(file_path)
        ]
    
    def generate_report(self, results: Dict[str, List[CheckResult]]) -> str:
        """Generate a markdown report."""
        report = f"""# I18N Quality Check Report

> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

| Document | Terminology | Links | Format | Status |
|----------|-------------|-------|--------|--------|
"""
        
        total_issues = 0
        total_warnings = 0
        
        for doc_name, check_results in results.items():
            statuses = []
            for result in check_results:
                status = "✅" if result.passed else "❌"
                statuses.append(status)
                total_issues += len(result.issues)
                total_warnings += len(result.warnings)
            
            overall = "✅" if all(r.passed for r in check_results) else "❌"
            report += f"| {doc_name} | {statuses[0]} | {statuses[1]} | {statuses[2]} | {overall} |\n"
        
        report += f"""
## Statistics

- Total Documents Checked: {len(results)}
- Total Issues: {total_issues}
- Total Warnings: {total_warnings}

## Detailed Results

"""
        
        for doc_name, check_results in results.items():
            report += f"### {doc_name}\n\n"
            
            for result in check_results:
                report += f"**{result.check_name}**: {'✅ Passed' if result.passed else '❌ Failed'}\n\n"
                
                if result.stats:
                    report += "Stats:\n"
                    for key, value in result.stats.items():
                        report += f"- {key}: {value}\n"
                    report += "\n"
                
                if result.issues:
                    report += "Issues:\n"
                    for issue in result.issues:
                        report += f"- ❌ {issue}\n"
                    report += "\n"
                
                if result.warnings:
                    report += "Warnings:\n"
                    for warning in result.warnings:
                        report += f"- ⚠️ {warning}\n"
                    report += "\n"
            
            report += "---\n\n"
        
        return report
    
    def generate_json_report(self, results: Dict[str, List[CheckResult]]) -> str:
        """Generate a JSON report."""
        json_results = {}
        
        for doc_name, check_results in results.items():
            json_results[doc_name] = [r.to_dict() for r in check_results]
        
        return json.dumps(json_results, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="I18N Quality Checker for AnalysisDataFlow"
    )
    parser.add_argument(
        "--check-terms",
        action="store_true",
        help="Check terminology consistency"
    )
    parser.add_argument(
        "--check-links",
        action="store_true",
        help="Check link validity"
    )
    parser.add_argument(
        "--check-format",
        action="store_true",
        help="Check format consistency"
    )
    parser.add_argument(
        "--check-all",
        action="store_true",
        help="Run all checks"
    )
    parser.add_argument(
        "--document",
        type=str,
        help="Check specific document"
    )
    parser.add_argument(
        "--generate-report",
        action="store_true",
        help="Generate full report"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON format"
    )
    
    args = parser.parse_args()
    
    checker = I18NQualityChecker()
    
    if not any([args.check_terms, args.check_links, args.check_format, args.check_all, args.generate_report]):
        # Default to check-all if no specific check requested
        args.check_all = True
    
    if args.document:
        doc_path = Path(args.document)
        if not doc_path.is_absolute():
            doc_path = PROJECT_ROOT / doc_path
        
        print(f"Checking: {doc_path}")
        results = {doc_path.name: checker.check_document(doc_path)}
    else:
        print("Checking all English documents...")
        results = checker.check_all_documents()
    
    # Display results
    print("\n" + "=" * 60)
    print("Quality Check Results")
    print("=" * 60)
    
    for doc_name, check_results in results.items():
        print(f"\n📄 {doc_name}")
        for result in check_results:
            status = "✅" if result.passed else "❌"
            print(f"  {status} {result.check_name}: {len(result.issues)} issues, {len(result.warnings)} warnings")
            
            if result.issues and (args.check_all or args.generate_report):
                for issue in result.issues[:3]:  # Show first 3
                    print(f"     - {issue}")
                if len(result.issues) > 3:
                    print(f"     ... and {len(result.issues) - 3} more")
    
    # Generate report if requested
    if args.generate_report or args.check_all:
        report = checker.generate_report(results)
        report_file = PROJECT_ROOT / "i18n-quality-report.md"
        report_file.write_text(report, encoding='utf-8')
        print(f"\n📊 Report saved to: {report_file}")
        
        if args.json:
            json_report = checker.generate_json_report(results)
            json_file = PROJECT_ROOT / "i18n-quality-report.json"
            json_file.write_text(json_report, encoding='utf-8')
            print(f"📊 JSON report saved to: {json_file}")
    
    print("\n" + "=" * 60)
    print("Done!")


if __name__ == "__main__":
    main()
