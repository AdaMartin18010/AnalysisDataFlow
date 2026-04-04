#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用验证脚本 v2
更准确地识别链接问题
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class CrossRefValidator:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.md_files = []
        self.file_set = set()
        self.dir_set = set()
        self.non_md_files = set()  # 非md文件（如LICENSE）
        self.anchors = defaultdict(set)
        self.theorems = defaultdict(set)
        self.links = []
        self.errors = []
        self.warnings = []
        self.fixes = []  # 记录可自动修复的问题
        
    def collect_files(self):
        """收集所有文件"""
        for item in self.base_dir.rglob('*'):
            if '.git' in item.parts:
                continue
            if item.is_file():
                rel_path = item.relative_to(self.base_dir)
                path_str = str(rel_path).replace('\\', '/')
                if item.suffix == '.md':
                    self.md_files.append(rel_path)
                    self.file_set.add(path_str)
                else:
                    self.non_md_files.add(path_str)
            elif item.is_dir():
                rel_path = item.relative_to(self.base_dir)
                self.dir_set.add(str(rel_path).replace('\\', '/'))
                
        print(f"找到 {len(self.md_files)} 个Markdown文件")
        print(f"找到 {len(self.non_md_files)} 个其他文件")
        print(f"找到 {len(self.dir_set)} 个目录")
        
    def extract_anchors(self, content, file_path):
        """提取文件中的所有锚点"""
        # 标题锚点
        header_pattern = r'^#{1,6}\s+(.+?)(?:\s*\{#([^}]+)\})?$'
        for match in re.finditer(header_pattern, content, re.MULTILINE):
            title = match.group(1).strip()
            custom_anchor = match.group(2)
            
            if custom_anchor:
                self.anchors[file_path].add(custom_anchor)
            
            # 转换为GitHub风格的锚点
            anchor = self._slugify(title)
            if anchor:
                self.anchors[file_path].add(anchor)
            
            # 也添加原始标题作为锚点（处理中文锚点）
            title_clean = re.sub(r'<[^>]+>', '', title)  # 移除HTML标签
            if title_clean:
                self.anchors[file_path].add(title_clean)
            
        # HTML锚点 <a name="...">
        html_anchor_pattern = r'<a\s+name=["\']([^"\']+)["\']'
        for match in re.finditer(html_anchor_pattern, content):
            self.anchors[file_path].add(match.group(1))
    
    def _slugify(self, text):
        """将标题转换为GitHub风格的锚点"""
        # 移除markdown标记
        text = re.sub(r'\*\*', '', text)
        text = re.sub(r'`', '', text)
        text = re.sub(r'<[^>]+>', '', text)  # 移除HTML标签
        # 转换为小写（仅ASCII字符）
        text = text.lower()
        # 替换空格和特殊字符为连字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', text)  # 保留中文字符
        text = re.sub(r'[\s]+', '-', text)
        # 移除首尾连字符
        text = text.strip('-')
        return text
    
    def extract_theorems(self, content, file_path):
        """提取文件中定义的定理"""
        # 定理定义模式: **Thm-X-XX-XX** 或 [Thm-X-XX-XX]
        theorem_patterns = [
            r'^\s*[-\*]\s*\*\*(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d+)-(\d+)\*\*',
            r'\*\*(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d+)-(\d+)[:\.]',
            r'\*\*.*?(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d+)-(\d+).*?\*\*',
        ]
        for pattern in theorem_patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                theorem_id = f"{match.group(1)}-{match.group(2)}-{match.group(3)}-{match.group(4)}"
                self.theorems[file_path].add(theorem_id)
    
    def _get_code_ranges(self, content):
        """返回代码块和行内代码的 (start, end) 范围列表"""
        ranges = []
        # 处理 fenced code blocks (```)
        fence_pattern = r'^```.*?$'
        in_code = False
        code_start = 0
        for match in re.finditer(fence_pattern, content, re.MULTILINE):
            if not in_code:
                code_start = match.start()
                in_code = True
            else:
                ranges.append((code_start, match.end()))
                in_code = False
        # 处理行内代码 (`...`)
        inline_pattern = r'`[^`]*`'
        for match in re.finditer(inline_pattern, content):
            start, end = match.start(), match.end()
            # 检查是否在 fenced code block 内
            if any(rs <= start and end <= re for rs, re in ranges):
                continue
            ranges.append((start, end))
        # 处理 LaTeX 数学块 ($$...$$)
        latex_block_pattern = r'\$\$[\s\S]*?\$\$'
        for match in re.finditer(latex_block_pattern, content):
            ranges.append((match.start(), match.end()))
        # 处理行内 LaTeX ($...$) - 但要注意排除货币符号
        inline_latex_pattern = r'(?<!\$)\$[^$\n]+?\$(?!\$)'
        for match in re.finditer(inline_latex_pattern, content):
            ranges.append((match.start(), match.end()))
        return ranges

    def extract_links(self, content, file_path):
        """提取文件中的所有链接"""
        # Markdown链接: [text](url) - 改进匹配以处理多行
        link_pattern = r'\[([^\]]*?)\]\(([^)]+)\)'
        code_ranges = self._get_code_ranges(content)
        for match in re.finditer(link_pattern, content):
            # 跳过代码块/行内代码中的链接
            if any(rs <= match.start() and match.end() <= re for rs, re in code_ranges):
                continue

            link_text = match.group(1)
            link_url = match.group(2)

            # 过滤掉代码片段中的伪链接
            if '\n' in link_text and 'classOf' in link_url:
                continue
            if 'classOf' in link_url or 'Duration.of' in link_url:
                continue
            if link_url.startswith('#'):
                # 纯锚点链接，检查锚点
                self.links.append({
                    'source': file_path,
                    'text': link_text,
                    'url': link_url,
                    'line': content[:match.start()].count('\n') + 1,
                    'type': 'anchor_only'
                })
                continue
            
            # 忽略外部链接
            if link_url.startswith('http://') or link_url.startswith('https://'):
                continue
                
            self.links.append({
                'source': file_path,
                'text': link_text,
                'url': link_url,
                'line': content[:match.start()].count('\n') + 1,
                'type': 'internal'
            })
    
    def resolve_link(self, url, source_file):
        """解析链接为目标文件路径"""
        if '#' in url:
            file_part, anchor = url.split('#', 1)
        else:
            file_part, anchor = url, None
        
        # 空文件部分表示同一文件内的锚点
        if file_part == '':
            return source_file, anchor, True
        
        # 处理相对路径
        source_dir = Path(source_file).parent
        target_path = source_dir / file_part
        
        # 规范化路径
        try:
            target_path = target_path.resolve().relative_to(self.base_dir.resolve())
        except:
            pass
        
        target_str = str(target_path).replace('\\', '/')
        
        # 检查是否为目录链接
        if target_str in self.dir_set or target_str.rstrip('/') in self.dir_set:
            return target_str, anchor, True
        
        # 检查文件是否存在（包括.md扩展名变体）
        for variant in [target_str, target_str + '.md', target_str.lstrip('./')]:
            if variant in self.file_set:
                return variant, anchor, True
            if variant.rstrip('/') in self.file_set:
                return variant.rstrip('/'), anchor, True
        
        # 检查非md文件（如LICENSE）
        for variant in [target_str, target_str.lstrip('./')]:
            if variant in self.non_md_files:
                return variant, anchor, True
        
        return target_str, anchor, False
    
    def validate_links(self):
        """验证所有链接的有效性"""
        for link in self.links:
            url = link['url']
            source = link['source']
            link_type = link.get('type', 'internal')
            
            # 纯锚点链接
            if link_type == 'anchor_only':
                anchor = url[1:]  # 移除#
                file_anchors = self.anchors.get(source, set())
                anchor_slug = self._slugify(anchor)
                
                found = False
                for fa in file_anchors:
                    if anchor.lower() in fa.lower() or anchor_slug in fa or fa in anchor:
                        found = True
                        break
                
                if not found:
                    self.errors.append({
                        'type': 'anchor_not_found',
                        'source': source,
                        'url': url,
                        'text': link['text'],
                        'line': link['line'],
                        'file': source,
                        'anchor': anchor,
                        'suggestion': self._find_similar_anchor(source, anchor)
                    })
                continue
            
            # 内部链接
            target_file, anchor, exists = self.resolve_link(url, source)
            
            if not exists:
                self.errors.append({
                    'type': 'file_not_found',
                    'source': source,
                    'url': url,
                    'text': link['text'],
                    'line': link['line'],
                    'resolved': target_file,
                    'suggestion': self._find_similar_file(target_file)
                })
                continue
            
            # 验证锚点
            if anchor:
                file_anchors = self.anchors.get(target_file, set())
                anchor_slug = self._slugify(anchor)
                
                found = False
                for fa in file_anchors:
                    if anchor.lower() in fa.lower() or anchor_slug in fa.lower() or fa.lower() in anchor.lower():
                        found = True
                        break
                
                if not found:
                    self.errors.append({
                        'type': 'anchor_not_found',
                        'source': source,
                        'url': url,
                        'text': link['text'],
                        'line': link['line'],
                        'file': target_file,
                        'anchor': anchor,
                        'suggestion': self._find_similar_anchor(target_file, anchor)
                    })
    
    def _find_similar_file(self, target):
        """查找相似的文件"""
        target_lower = target.lower().replace('.md', '')
        candidates = []
        for f in self.file_set:
            f_lower = f.lower().replace('.md', '')
            if target_lower in f_lower or f_lower in target_lower:
                candidates.append(f)
        return candidates[:3] if candidates else None
    
    def _find_similar_anchor(self, file, anchor):
        """查找相似的锚点"""
        anchor_slug = self._slugify(anchor)
        file_anchors = self.anchors.get(file, set())
        candidates = []
        for fa in file_anchors:
            if anchor_slug in fa or fa in anchor_slug:
                candidates.append(fa)
        return candidates[:3] if candidates else None
    
    def scan_all_files(self):
        """扫描所有文件"""
        print("开始扫描文件...")
        for md_file in self.md_files:
            try:
                full_path = self.base_dir / md_file
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                file_str = str(md_file).replace('\\', '/')
                self.extract_anchors(content, file_str)
                self.extract_theorems(content, file_str)
                self.extract_links(content, file_str)
            except Exception as e:
                print(f"扫描文件 {md_file} 时出错: {e}")
                
        print(f"提取到 {len(self.links)} 个内部链接")
        print(f"提取到 {sum(len(a) for a in self.anchors.values())} 个锚点")
        print(f"提取到 {sum(len(t) for t in self.theorems.values())} 个定理定义")
    
    def identify_fixable_errors(self):
        """识别可以自动修复的错误"""
        for err in self.errors:
            if err['type'] == 'file_not_found':
                # 检查是否是大小写问题
                if err.get('suggestion'):
                    self.fixes.append({
                        'type': 'case_mismatch',
                        'error': err,
                        'fix': err['suggestion'][0]
                    })
            elif err['type'] == 'anchor_not_found':
                if err.get('suggestion'):
                    self.fixes.append({
                        'type': 'anchor_typo',
                        'error': err,
                        'fix': err['suggestion'][0]
                    })
    
    def generate_report(self):
        """生成验证报告"""
        self.identify_fixable_errors()
        
        print("\n" + "="*70)
        print("交叉引用完整性验证报告")
        print("="*70)
        print(f"\n验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"扫描文件数: {len(self.md_files)}")
        print(f"提取链接数: {len(self.links)}")
        
        # 按类型分类错误
        file_errors = [e for e in self.errors if e['type'] == 'file_not_found']
        anchor_errors = [e for e in self.errors if e['type'] == 'anchor_not_found']
        
        print(f"\n错误统计:")
        print(f"  - 文件不存在错误: {len(file_errors)}")
        print(f"  - 锚点不存在错误: {len(anchor_errors)}")
        print(f"  - 可自动修复: {len(self.fixes)}")
        
        # 按源文件分组错误
        errors_by_source = defaultdict(list)
        for err in self.errors:
            errors_by_source[err['source']].append(err)
        
        print(f"\n涉及文件数: {len(errors_by_source)}")
        
        # 保存详细报告
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_files': len(self.md_files),
                'total_links': len(self.links),
                'total_errors': len(self.errors),
                'file_errors': len(file_errors),
                'anchor_errors': len(anchor_errors),
                'fixable': len(self.fixes),
                'files_with_errors': len(errors_by_source)
            },
            'errors_by_category': {
                'file_not_found': file_errors,
                'anchor_not_found': anchor_errors
            },
            'errors_by_source': {k: v for k, v in errors_by_source.items()},
            'suggested_fixes': self.fixes,
            'all_files': sorted(list(self.file_set)),
            'all_dirs': sorted(list(self.dir_set))
        }
        
        os.makedirs('.stats', exist_ok=True)
        report_path = self.base_dir / '.stats/cross_ref_report_v2.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n详细报告已保存到: {report_path}")
        
        # 输出关键错误详情
        if file_errors:
            print("\n" + "-"*70)
            print("文件不存在错误 (前15个):")
            print("-"*70)
            for i, err in enumerate(file_errors[:15], 1):
                print(f"\n{i}. {err['source']}:{err['line']}")
                print(f"   链接: [{err['text'][:50]}]({err['url']})")
                print(f"   解析路径: {err['resolved']}")
                if err.get('suggestion'):
                    print(f"   建议: 可能是 {err['suggestion'][0]}")
        
        if anchor_errors:
            print("\n" + "-"*70)
            print("锚点不存在错误 (前10个):")
            print("-"*70)
            for i, err in enumerate(anchor_errors[:10], 1):
                print(f"\n{i}. {err['source']}:{err['line']}")
                print(f"   链接: [{err['text']}]({err['url']})")
                print(f"   锚点: #{err['anchor']}")
                if err.get('suggestion'):
                    print(f"   建议: 可能是 #{err['suggestion'][0]}")
        
        return report

def main():
    base_dir = Path(__file__).parent.parent
    validator = CrossRefValidator(base_dir)
    
    validator.collect_files()
    validator.scan_all_files()
    validator.validate_links()
    report = validator.generate_report()
    
    return 0

if __name__ == '__main__':
    exit(main())
