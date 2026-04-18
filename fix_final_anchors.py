#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

def github_anchor(text):
    text = text.lower()
    text = re.sub(r'\s', '-', text)
    text = re.sub(r'[^a-z0-9_\-\u4e00-\u9fff]', '', text)
    return text

explicit_re = re.compile(r'\s*\{#[^}]+\}\s*$')

# Files with remaining duplicated explicit anchors
files = [
    'Struct\\06-frontier\\06.03-ai-agent-session-types.md',
    'Struct\\03-relationships\\03.04-bisimulation-equivalences.md',
    'Struct\\05-comparative-analysis\\05.02-expressiveness-vs-decidability.md',
    'Struct\\06-frontier\\06.02-choreographic-streaming-programming.md',
    'Struct\\04-proofs\\04.04-watermark-algebra-formal-proof.md',
]

replacements = {}
for fp in files:
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        new_lines = []
        modified = False
        for line in lines:
            m = re.match(r'^(#{1,6})\s+(.*)$', line)
            if m:
                title = m.group(2).rstrip('\n')
                match = explicit_re.search(title)
                if match:
                    explicit = match.group(0).strip()[2:-1]
                    clean_title = title[:match.start()]
                    # Check if explicit anchor contains repetition
                    parts = explicit.split('-')
                    # Simple heuristic: if the explicit anchor is very long and contains repeated segments
                    half = len(explicit) // 2
                    if half > 10 and explicit[:half] in explicit[half:]:
                        # It's a duplication
                        new_lines.append(m.group(1) + ' ' + clean_title + '\n')
                        old_anchor = github_anchor(title)
                        new_anchor = github_anchor(clean_title)
                        replacements[old_anchor] = new_anchor
                        modified = True
                        continue
            new_lines.append(line)
        if modified:
            with open(fp, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f'Fixed headings in {fp}')
    except Exception as e:
        print(f'Error with {fp}: {e}')

# Also fix the heading in 06.02 that has multiple explicit anchors
fp = 'Struct\\06-frontier\\06.02-choreographic-streaming-programming.md'
try:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    # Fix heading with multiple explicit anchors
    content = content.replace(
        '关系 1: Choreographic ⊃ 传统数据流 {#关系-1-choreographic-传统数据流} {#关系-1-choreographic--传统数据流}',
        '关系 1: Choreographic ⊃ 传统数据流'
    )
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Fixed multiple explicit anchors in {fp}')
except Exception as e:
    print(f'Error with {fp}: {e}')

# Apply replacements globally
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        try:
            with open(fp, 'r', encoding='utf-8') as file:
                content = file.read()
            original = content
            for old, new in replacements.items():
                content = content.replace('#' + old, '#' + new)
            if content != original:
                with open(fp, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f'Replaced anchors in {fp}')
        except Exception as e:
            pass

print("Done.")
