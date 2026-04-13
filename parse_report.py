import re, json

with open('CODE-EXAMPLE-VALIDATION-REPORT.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

entries = []
current_file = None
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith('### `'):
        current_file = line.strip()[5:-1]
        i += 1
        continue
    
    m = re.match(r'\*\*块索引 #(\d+)\*\* \(第 (\d+) 行, 语言: (\w+)\)', line)
    if m:
        block_idx = m.group(1)
        line_num = int(m.group(2))
        lang = m.group(3)
        
        i += 1
        error_lines = []
        type_line = ''
        code_snippet = []
        
        while i < len(lines):
            l = lines[i]
            if re.match(r'\*\*块索引 #\d+\*\*', l) or l.startswith('### `'):
                break
            if l.startswith('- **错误**:'):
                err = l[10:].rstrip()
                i += 1
                while i < len(lines):
                    nl = lines[i]
                    if nl.startswith('- **'):
                        break
                    err += '\n' + nl.rstrip()
                    i += 1
                error_lines.append(err)
                continue
            elif l.startswith('- **类型**:'):
                type_line = l[10:].rstrip()
            elif l.strip().startswith('```' + lang):
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    cl = lines[i]
                    if cl.startswith('  '):
                        cl = cl[2:]
                    code_snippet.append(cl)
                    i += 1
            i += 1
        
        entries.append({
            'file': current_file,
            'block_idx': block_idx,
            'line_num': line_num,
            'lang': lang,
            'error': '\n'.join(error_lines),
            'type': type_line,
            'code': ''.join(code_snippet)
        })
        continue
    i += 1

with open('temp_entries3.json', 'w', encoding='utf-8') as f:
    json.dump(entries[:150], f, ensure_ascii=False, indent=2)

print('Saved %d entries' % len(entries[:150]))
for idx in range(min(10, len(entries))):
    print('%d: %s | len=%d' % (idx+1, entries[idx]['file'], len(entries[idx]['code'])))
