#!/usr/bin/env python3
"""
Link Checker Tool - Phase 2 Task 5-1
Automatically checks for broken links in markdown documents.

Usage:
    python link_checker.py [directory]

Features:
- Checks internal document links
- Checks external HTTP/HTTPS links
- Reports broken links with line numbers
- Generates detailed report
"""

import os
import re
import sys
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse
import json
from datetime import datetime

class LinkChecker:
    def __init__(self, root_dir, max_workers=10, timeout=10):
        self.root_dir = Path(root_dir)
        self.max_workers = max_workers
        self.timeout = timeout
        self.broken_links = []
        self.checked_links = 0
        self.total_links = 0
        
    def extract_links(self, file_path):
        """Extract all links from a markdown file."""
        links = []
        content = file_path.read_text(encoding='utf-8')
        
        # Pattern for markdown links: [text](url)
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            text, url = match.groups()
            line_num = content[:match.start()].count('\n') + 1
            links.append({
                'text': text,
                'url': url,
                'line': line_num,
                'file': str(file_path.relative_to(self.root_dir))
            })
        
        return links
    
    def check_internal_link(self, link, source_file):
        """Check if internal link is valid."""
        url = link['url']
        
        # Handle anchors
        if '#' in url:
            url = url.split('#')[0]
        
        # Skip empty URLs
        if not url:
            return None
        
        # Resolve relative path
        source_dir = self.root_dir / Path(source_file).parent
        target_path = (source_dir / url).resolve()
        
        # Check if file exists
        if not target_path.exists():
            return {
                'type': 'internal',
                'status': 'broken',
                'url': url,
                'file': link['file'],
                'line': link['line'],
                'error': f'File not found: {target_path}'
            }
        
        return {
            'type': 'internal',
            'status': 'ok',
            'url': url,
            'file': link['file'],
            'line': link['line']
        }
    
    def check_external_link(self, link):
        """Check if external link is valid."""
        url = link['url']
        
        try:
            headers = {
                'User-Agent': 'AnalysisDataFlow-LinkChecker/1.0'
            }
            response = requests.head(
                url, 
                headers=headers, 
                timeout=self.timeout,
                allow_redirects=True
            )
            
            # Some servers don't support HEAD, try GET
            if response.status_code == 405:
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    stream=True
                )
                response.close()
            
            if response.status_code >= 400:
                return {
                    'type': 'external',
                    'status': 'broken',
                    'url': url,
                    'file': link['file'],
                    'line': link['line'],
                    'error': f'HTTP {response.status_code}'
                }
            
            return {
                'type': 'external',
                'status': 'ok',
                'url': url,
                'file': link['file'],
                'line': link['line'],
                'http_status': response.status_code
            }
            
        except requests.exceptions.Timeout:
            return {
                'type': 'external',
                'status': 'timeout',
                'url': url,
                'file': link['file'],
                'line': link['line'],
                'error': 'Request timeout'
            }
        except Exception as e:
            return {
                'type': 'external',
                'status': 'error',
                'url': url,
                'file': link['file'],
                'line': link['line'],
                'error': str(e)
            }
    
    def check_link(self, link):
        """Check a single link."""
        url = link['url']
        
        # Skip certain URLs
        if url.startswith('mailto:'):
            return None
        if url.startswith('#'):  # Internal anchor
            return None
        
        # Check if internal or external
        if url.startswith('http://') or url.startswith('https://'):
            return self.check_external_link(link)
        else:
            return self.check_internal_link(link, link['file'])
    
    def scan_directory(self):
        """Scan all markdown files in directory."""
        markdown_files = list(self.root_dir.rglob('*.md'))
        all_links = []
        
        print(f"Scanning {len(markdown_files)} markdown files...")
        
        for file_path in markdown_files:
            links = self.extract_links(file_path)
            all_links.extend(links)
        
        self.total_links = len(all_links)
        print(f"Found {self.total_links} links to check")
        
        return all_links
    
    def check_all_links(self, all_links):
        """Check all links in parallel."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.check_link, link): link 
                      for link in all_links}
            
            for future in as_completed(futures):
                self.checked_links += 1
                result = future.result()
                
                if result and result['status'] != 'ok':
                    self.broken_links.append(result)
                
                # Progress report
                if self.checked_links % 100 == 0:
                    print(f"Checked {self.checked_links}/{self.total_links} links...")
    
    def generate_report(self):
        """Generate detailed report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_files': len(list(self.root_dir.rglob('*.md'))),
                'total_links': self.total_links,
                'checked_links': self.checked_links,
                'broken_links': len(self.broken_links),
                'success_rate': f"{((self.total_links - len(self.broken_links)) / self.total_links * 100):.2f}%" if self.total_links > 0 else "N/A"
            },
            'broken_links': self.broken_links
        }
        
        return report
    
    def save_report(self, report, output_file='link-check-report.json'):
        """Save report to file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\nReport saved to: {output_file}")
    
    def print_summary(self, report):
        """Print summary to console."""
        print("\n" + "="*60)
        print("LINK CHECK SUMMARY")
        print("="*60)
        print(f"Total files scanned: {report['summary']['total_files']}")
        print(f"Total links found: {report['summary']['total_links']}")
        print(f"Links checked: {report['summary']['checked_links']}")
        print(f"Broken links: {report['summary']['broken_links']}")
        print(f"Success rate: {report['summary']['success_rate']}")
        print("="*60)
        
        if self.broken_links:
            print("\nBroken Links:")
            for link in self.broken_links[:10]:  # Show first 10
                print(f"  [{link['type']}] {link['file']}:{link['line']}")
                print(f"    URL: {link['url']}")
                print(f"    Error: {link['error']}")
            
            if len(self.broken_links) > 10:
                print(f"  ... and {len(self.broken_links) - 10} more")


def main():
    # Get directory from command line or use current directory
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = '.'
    
    print(f"AnalysisDataFlow Link Checker")
    print(f"Scanning directory: {directory}\n")
    
    # Create checker and run
    checker = LinkChecker(directory)
    all_links = checker.scan_directory()
    checker.check_all_links(all_links)
    report = checker.generate_report()
    checker.print_summary(report)
    checker.save_report(report)
    
    # Exit with error code if broken links found
    sys.exit(0 if not checker.broken_links else 1)


if __name__ == '__main__':
    main()
