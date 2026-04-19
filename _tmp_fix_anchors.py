import re, os
from pathlib import Path
from collections import defaultdict
import difflib

class AnchorFixer:
    def __init__(self, base_path):
        self.base_path = Path(base_path).resolve()
        self.anchor_cache = {}
        self.custom_anchors = {}
        self.heading_anchors = {}
        self.issues = []
        
    def extract_anchors(self, content):
        anchors = set()
        custom = set()
        headings = {}
        
        header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        for match in header_pattern.finditer(content):
            level, title = match.groups()
            
            custom_match = re.search(r'\{\s*#([^}\s]+)\s*\}', title)
            if custom_match:
                custom.add(custom_match.group(1))
                anchors.add(custom_match.group(1))
                heading_text = re.sub(r'\{\s*#([^}\s]+)\s*\}', '', title).strip()
            else:
                heading_text = title.strip()
            
            anchor = heading_text.strip().lower()
            anchor = re.sub(r'[^\w\s-]', '', anchor)
            anchor = re.sub(r'[-\s]+', '-', anchor)
            anchor = anchor.strip('-')
            if anchor:
                anchors.add(anchor)
                headings[anchor] = heading_text.strip()
        
        html_anchor_pattern = re.compile(r'<a\s+name=["\']([^"\']+)["\']', re.IGNORECASE)
        for match in html_anchor_pattern.finditer(content):
            anchors.add(match.group(1))
            custom.add(match.group(1))
        
        return anchors, custom, headings
    
    def find_best_match(self, broken_anchor, target_str):
        all_anchors = self.anchor_cache.get(target_str, set())
        custom = self.custom_anchors.get(target_str, set())
        headings = self.heading_anchors.get(target_str, {})
        
        if broken_anchor in all_anchors:
            return broken_anchor
        
        # Check if broken_anchor is a concatenation/double of a valid anchor
        for valid in sorted(all_anchors, key=len, reverse=True):
            if broken_anchor == valid + valid or broken_anchor == valid + '-' + valid:
                return valid
            if broken_anchor.startswith(valid + '-'):
                remainder = broken_anchor[len(valid)+1:]
                if remainder in all_anchors:
                    return valid
        
        # Check custom anchors first
        for ca in custom:
            if ca in broken_anchor or broken_anchor in ca:
                return ca
        
        # Try exact match after -- -> -
        fixed = broken_anchor.replace('--', '-')
        if fixed in all_anchors:
            return fixed
        
        # Remove leading hyphen (for emoji headings)
        if fixed.startswith('-'):
            no_leading = fixed.lstrip('-')
            if no_leading in all_anchors:
                return no_leading
        
        # Try fuzzy matching against headings
        best_match = None
        best_ratio = 0.0
        broken_clean = broken_anchor.replace('-', '')
        
        for h, title in headings.items():
            h_clean = h.replace('-', '')
            if broken_clean in h_clean or h_clean in broken_clean:
                ratio = difflib.SequenceMatcher(None, broken_anchor, h).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = h
        
        if best_match and best_ratio > 0.5:
            return best_match
        
        return None
    
    def scan(self):
        md_files = []
        for pattern in ['Struct/**/*.md', 'Knowledge/**/*.md', 'Flink/**/*.md', 'docs/**/*.md', '*.md']:
            md_files.extend(self.base_path.glob(pattern))
        md_files = list(set(md_files))
        
        for f in md_files:
            try:
                content = f.read_text(encoding='utf-8')
                anchors, custom, headings = self.extract_anchors(content)
                self.anchor_cache[str(f)] = anchors
                self.custom_anchors[str(f)] = custom
                self.heading_anchors[str(f)] = headings
            except:
                pass
        
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        
        for f in md_files:
            try:
                content = f.read_text(encoding='utf-8')
            except:
                continue
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                for m in link_pattern.finditer(line):
                    text, url = m.groups()
                    if url.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                        continue
                    if '#' not in url:
                        continue
                    path_part, anchor = url.split('#', 1)
                    if not path_part:
                        target = f
                    else:
                        if path_part.startswith('/'):
                            target = self.base_path / path_part.lstrip('/')
                        else:
                            target = f.parent / path_part
                        try:
                            target = target.resolve()
                        except:
                            continue
                    if not target.exists():
                        continue
                    target_str = str(target)
                    if target_str not in self.anchor_cache:
                        continue
                    if anchor not in self.anchor_cache[target_str]:
                        best = self.find_best_match(anchor, target_str)
                        if best:
                            self.issues.append({
                                'source': str(f),
                                'line': line_num,
                                'url': url,
                                'anchor': anchor,
                                'target': str(target),
                                'suggested': best,
                            })
        
        return self.issues
    
    def apply_fixes(self, dry_run=True):
        by_file = defaultdict(list)
        for issue in self.issues:
            by_file[issue['source']].append(issue)
        
        fixed_count = 0
        for file_path, issues in by_file.items():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            # Sort by URL length descending to avoid partial replacements
            issues_sorted = sorted(issues, key=lambda x: len(x['url']), reverse=True)
            
            for issue in issues_sorted:
                old_url = issue['url']
                new_url = old_url.replace('#' + issue['anchor'], '#' + issue['suggested'])
                if old_url in content:
                    if dry_run:
                        rel = str(Path(file_path).relative_to(self.base_path)).replace('\\', '/')
                        print(f"[DRY] {rel}:{issue['line']} {old_url} -> {new_url}")
                    else:
                        content = content.replace(old_url, new_url)
            
            if not dry_run and content != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += len(issues)
                rel = str(Path(file_path).relative_to(self.base_path)).replace('\\', '/')
                print(f"Fixed {len(issues)} anchors in {rel}")
        
        return fixed_count

fixer = AnchorFixer('.')
issues = fixer.scan()
print(f"\nFound {len(issues)} fixable broken anchors")
print("="*80)
fixed = fixer.apply_fixes(dry_run=False)
print(f"\nTotal fixed: {fixed}")
