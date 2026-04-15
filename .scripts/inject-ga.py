#!/usr/bin/env python3
"""Inject Google Analytics tag into an HTML file."""
import sys

ga_id = sys.argv[1]
html_path = sys.argv[2] if len(sys.argv) > 2 else 'knowledge-graph-site/index.html'

script = (
    "<!-- Google tag (gtag.js) -->"
    f"<script async src='https://www.googletagmanager.com/gtag/js?id={ga_id}'></script>"
    f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}"
    f"gtag('js',new Date());gtag('config','{ga_id}');</script>"
)

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('</head>', script + '</head>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Google Analytics ({ga_id}) injected into {html_path}")
