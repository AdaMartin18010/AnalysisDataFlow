import re, os
from pathlib import Path
from collections import defaultdict

class Checker:
    def __init__(self, base_path):
        self.base_path = Path(base_path).resolve()
        self.anchor_cache = {}
        self.issues = []
        
    def extract_anchors(self, content):
        anchors = set()
        header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        for match in header_pattern.finditer(content):
            level, title = match.groups()
            anchor = title.strip().lower()
            anchor = re.sub(r'[^\w\s-]', '', anchor)
            anchor = re.sub(r'[-\s]+', '-', anchor)
            anchor = anchor.strip('-')
            if anchor:
                anchors.add(anchor)
        html_anchor_pattern = re.compile(r'<a\s+name=["\']([^"\']+)["\']', re.IGNORECASE)
        for match in html_anchor_pattern.finditer(content):
            anchors.add(match.group(1))
        custom_anchor_pattern = re.compile(r'\{\s*#([^}\s]+)\s*\}')
        for match in custom_anchor_pattern.finditer(content):
            anchors.add(match.group(1))
        return anchors
    
    def get_headings(self, content):
        headings = {}
        header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        for match in header_pattern.finditer(content):
            level, title = match.groups()
            anchor = title.strip().lower()
            anchor = re.sub(r'[^\w\s-]', '', anchor)
            anchor = re.sub(r'[-\s]+', '-', anchor)
            anchor = anchor.strip('-')
            if anchor:
                headings[anchor] = title.strip()
        return headings
    
    def scan(self):
        md_files = []
        for pattern in ['Struct/**/*.md', 'Knowledge/**/*.md', 'Flink/**/*.md', 'docs/**/*.md', '*.md']:
            md_files.extend(self.base_path.glob(pattern))
        md_files = list(set(md_files))
        
        for f in md_files:
            try:
                content = f.read_text(encoding='utf-8')
                self.anchor_cache[str(f)] = self.extract_anchors(content)
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
                        headings = self.get_headings(target.read_text(encoding='utf-8'))
                        self.issues.append({
                            'source': str(f.relative_to(self.base_path)).replace('\\', '/'),
                            'line': line_num,
                            'url': url,
                            'anchor': anchor,
                            'target': str(target.relative_to(self.base_path)).replace('\\', '/'),
                            'target_headings': headings
                        })
        
        print(f'Total broken anchors: {len(self.issues)}')
        
        by_anchor = defaultdict(list)
        for issue in self.issues:
            by_anchor[issue['anchor']].append(issue)
        
        for anchor, issues in sorted(by_anchor.items(), key=lambda x: -len(x[1]))[:50]:
            print(f'\n{anchor} ({len(issues)} occurrences)')
            for issue in issues[:3]:
                print(f'  {issue["source"]}:{issue["line"]} -> {issue["target"]}')
                closest = None
                closest_dist = 999
                for h, title in issue['target_headings'].items():
                    a_clean = anchor.replace('-', '')
                    h_clean = h.replace('-', '')
                    if a_clean in h_clean or h_clean in a_clean:
                        if abs(len(h) - len(anchor)) < closest_dist:
                            closest_dist = abs(len(h) - len(anchor))
                            closest = (h, title)
                if closest:
                    print(f'    Suggested: {closest[0]} ({closest[1]})')

checker = Checker('.')
checker.scan()
