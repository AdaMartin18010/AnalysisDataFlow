#!/usr/bin/env python3
"""
Build Concept-Document-Code Triple Mapping Index
Scans all Markdown files to build a JSON index mapping:
  concepts -> documents -> code examples
"""

import os
import re
import json
from collections import defaultdict
from pathlib import Path

def extract_formal_elements(content, file_path):
    """Extract Def/Thm/Lemma/Prop/Cor definitions."""
    elements = []
    # Pattern: ### Def-X-XX-XX: Title
    pattern = re.compile(
        r'#{1,6}\s+(Def|Thm|Lemma|Prop|Cor)-([A-Z])-(\d+)-(\d+):\s*(.+?)$',
        re.MULTILINE
    )
    for match in pattern.finditer(content):
        elem_type = match.group(1)
        stage = match.group(2)
        doc_num = match.group(3)
        seq_num = match.group(4)
        title = match.group(5).strip()
        elements.append({
            'type': elem_type,
            'id': f"{elem_type}-{stage}-{doc_num}-{seq_num}",
            'title': title,
            'line': content[:match.start()].count('\n') + 1
        })
    return elements

def extract_code_examples(content, file_path):
    """Extract code blocks with language info."""
    examples = []
    pattern = re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL)
    for match in pattern.finditer(content):
        lang = match.group(1) or 'text'
        code = match.group(2).strip()
        # Only keep substantial code blocks (>10 lines)
        lines = code.split('\n')
        if len(lines) >= 10 and lang in ('java', 'python', 'sql', 'scala', 'go', 'rust', 'yaml', 'xml', 'json'):
            # Extract a summary (first non-empty, non-comment line)
            summary = ''
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('//') and not stripped.startswith('#') and not stripped.startswith('*'):
                    summary = stripped[:80]
                    break
            examples.append({
                'language': lang,
                'line_count': len(lines),
                'summary': summary,
                'line': content[:match.start()].count('\n') + 1
            })
    return examples

def extract_concept_mentions(content, concepts):
    """Find where concepts are mentioned in content."""
    mentions = defaultdict(list)
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        for concept in concepts:
            # Simple word boundary match
            if re.search(r'\b' + re.escape(concept) + r'\b', line, re.IGNORECASE):
                mentions[concept].append(i)
    return mentions

def build_mapping(base_path='.'):
    """Build the triple mapping index."""
    mapping = {
        'meta': {
            'version': '1.0',
            'generated': '2026-04-20',
            'total_files': 0,
            'total_concepts': 0,
            'total_code_examples': 0
        },
        'concepts': {},  # concept_id -> {title, type, documents[], code_examples[]}
        'documents': {},  # doc_path -> {title, concepts[], code_examples[], references[]}
        'code_examples': []  # {language, doc, line, summary}
    }
    
    # Collect all markdown files in core directories
    core_dirs = ['Struct', 'Knowledge', 'Flink']
    md_files = []
    for dir_name in core_dirs:
        dir_path = os.path.join(base_path, dir_name)
        if not os.path.exists(dir_path):
            continue
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if f.endswith('.md'):
                    md_files.append(os.path.join(root, f))
    
    # First pass: collect all formal elements (concepts)
    all_concepts = {}
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            rel_path = os.path.relpath(file_path, base_path).replace('\\', '/')
            elements = extract_formal_elements(content, rel_path)
            for elem in elements:
                all_concepts[elem['id']] = {
                    **elem,
                    'documents': [],
                    'code_examples': []
                }
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    # Second pass: build document entries and code examples
    total_code = 0
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            rel_path = os.path.relpath(file_path, base_path).replace('\\', '/')
            
            # Extract title
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else rel_path
            
            # Extract formal elements in this doc
            doc_elements = extract_formal_elements(content, rel_path)
            
            # Extract code examples
            code_examples = extract_code_examples(content, rel_path)
            total_code += len(code_examples)
            
            # Build document entry
            mapping['documents'][rel_path] = {
                'title': title,
                'concepts': [e['id'] for e in doc_elements],
                'code_example_count': len(code_examples),
                'code_examples': code_examples
            }
            
            # Add code examples to global list
            for ex in code_examples:
                mapping['code_examples'].append({
                    **ex,
                    'document': rel_path
                })
            
            # Link concepts to documents
            for elem in doc_elements:
                cid = elem['id']
                if cid in all_concepts:
                    all_concepts[cid]['documents'].append(rel_path)
                    all_concepts[cid]['code_examples'].extend([
                        {'language': ex['language'], 'summary': ex['summary'], 'document': rel_path}
                        for ex in code_examples
                    ])
                    
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    mapping['concepts'] = all_concepts
    mapping['meta']['total_files'] = len(md_files)
    mapping['meta']['total_concepts'] = len(all_concepts)
    mapping['meta']['total_code_examples'] = total_code
    
    return mapping

def save_mapping(mapping, output_path='KNOWLEDGE-GRAPH/data/concept-doc-code-mapping.json'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"Mapping saved to: {output_path}")
    print(f"  Files: {mapping['meta']['total_files']}")
    print(f"  Concepts: {mapping['meta']['total_concepts']}")
    print(f"  Code examples: {mapping['meta']['total_code_examples']}")

if __name__ == '__main__':
    mapping = build_mapping('.')
    save_mapping(mapping)
