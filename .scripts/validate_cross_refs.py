#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用验证脚本
扫描所有Markdown文件，检查内部链接、锚点链接、定理引用的有效性
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
        self.anchors = defaultdict(set)  # 文件 -> 锚点集合
        self.theorems = defaultdict(set)  # 文件 -> 定理集合
        self.links = []  # 所有链接
        self.errors = []
        self.warnings = []
        
    def collect_files(self):
        """收集所有Markdown文件"""
        for md_file in self.base_dir.rglob('*.md'):
            if '.git' in str(md_file):
                continue
            rel_path = md_file.relative_to(self.base_dir)
            self.md_files.append(rel_path)
            self.file_set.add(str(rel_path).replace('\\', '/'))
            
        print(f"找到 {len(self.md_files)} 个Markdown文件")
        
    def extract_anchors(self, content, file_path):
        """提取文件中的所有锚点"""
        # 标题锚点
        header_pattern = r'^#{1,6}\s+(.+)$'
        for match in re.finditer(header_pattern, content, re.MULTILINE):
            title = match.group(1).strip()
            # 转换为GitHub风格的锚点
            anchor = self._slugify(title)
            self.anchors[str(file_path)].add(anchor)
            
        # HTML锚点 <a name="...">
        html_anchor_pattern = r'<a\s+name=["\']([^"\']+)["\']'
        for match in re.finditer(html_anchor_pattern, content):
            self.anchors[str(file_path)].add(match.group(1))
            
        # 自定义锚点 {#id}
        custom_anchor_pattern = r'\{#([^}]+)\}'
        for match in re.finditer(custom_anchor_pattern, content):
            self.anchors[str(file_path)].add(match.group(1))
    
    def _slugify(self, text):
        """将标题转换为GitHub风格的锚点"""
        # 移除markdown标记
        text = re.sub(r'\*\*', '', text)
        text = re.sub(r'`', '', text)
        # 转换为小写
        text = text.lower()
        # 替换空格和特殊字符为连字符
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s]+', '-', text)
        # 移除首尾连字符
        text = text.strip('-')
        return text
    
    def extract_theorems(self, content, file_path):
        """提取文件中定义的定理"""
        # 定理定义模式: **Thm-X-XX-XX** 或 [Thm-X-XX-XX]
        theorem_patterns = [
            r'\*\*(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d+)-(\d+)\*\*',
            r'\[(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d+)-(\d+)\]',
            r'\*\*(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d+)-(\d+)[:\.]',
        ]
        for pattern in theorem_patterns:
            for match in re.finditer(pattern, content):
                theorem_id = f"{match.group(1)}-{match.group(2)}-{match.group(3)}-{match.group(4)}"
                self.theorems[str(file_path)].add(theorem_id)
    
    def extract_links(self, content, file_path):
        """提取文件中的所有链接"""
        # Markdown链接: [text](url)
        link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
        for match in re.finditer(link_pattern, content):
            link_text = match.group(1)
            link_url = match.group(2)
            
            # 忽略外部链接
            if link_url.startswith('http://') or link_url.startswith('https://'):
                continue
                
            self.links.append({
                'source': str(file_path),
                'text': link_text,
                'url': link_url,
                'line': content[:match.start()].count('\n') + 1
            })
    
    def validate_links(self):
        """验证所有链接的有效性"""
        for link in self.links:
            url = link['url']
            source = link['source']
            
            # 解析链接
            if '#' in url:
                file_part, anchor = url.split('#', 1)
            else:
                file_part, anchor = url, None
            
            # 处理空文件部分（同一文件内的锚点）
            if file_part == '':
                file_part = source
            
            # 处理相对路径
            if file_part:
                # 如果已经是相对路径格式
                if not file_part.startswith('./') and not file_part.startswith('../'):
                    # 检查是否是绝对路径从根目录
                    if not file_part.startswith('/'):
                        # 计算相对于源文件的完整路径
                        source_dir = Path(source).parent
                        target_path = source_dir / file_part
                        # 规范化路径
                        try:
                            target_path = target_path.resolve().relative_to(self.base_dir.resolve())
                        except:
                            pass
                        file_key = str(target_path).replace('\\', '/')
                    else:
                        file_key = file_part[1:]  # 移除开头的/
                else:
                    # 解析相对路径
                    source_dir = Path(source).parent
                    target_path = source_dir / file_part
                    try:
                        target_path = target_path.resolve().relative_to(self.base_dir.resolve())
                    except:
                        pass
                    file_key = str(target_path).replace('\\', '/')
            else:
                file_key = source
            
            # 验证文件是否存在
            if file_key not in self.file_set:
                # 尝试多种路径变体
                found = False
                for variant in [file_key, file_key + '.md', file_key.lstrip('./')]:
                    if variant in self.file_set:
                        found = True
                        file_key = variant
                        break
                
                if not found:
                    self.errors.append({
                        'type': 'file_not_found',
                        'source': source,
                        'url': url,
                        'text': link['text'],
                        'line': link['line'],
                        'resolved': file_key
                    })
                    continue
            
            # 验证锚点是否存在
            if anchor:
                # 转换锚点为标准化形式
                anchor_slug = self._slugify(anchor.replace('-', ' '))
                file_anchors = self.anchors.get(file_key, set())
                
                # 检查锚点（包括带-和不带-的变体）
                if anchor not in file_anchors and anchor_slug not in file_anchors:
                    # 尝试部分匹配
                    found = False
                    for fa in file_anchors:
                        if anchor in fa or fa in anchor or anchor_slug in fa:
                            found = True
                            break
                    
                    if not found:
                        self.errors.append({
                            'type': 'anchor_not_found',
                            'source': source,
                            'url': url,
                            'text': link['text'],
                            'line': link['line'],
                            'file': file_key,
                            'anchor': anchor
                        })
    
    def validate_theorem_refs(self, content, file_path):
        """验证定理引用"""
        # 查找定理引用（不检查是否是定义位置）
        ref_patterns = [
            r'参见\s*\*\*(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d+)-(\d+)\*\*',
            r'见\s*\*\*(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d+)-(\d+)\*\*',
            r'参考\s*\*\*(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d+)-(\d+)\*\*',
            r'由\s*\*\*(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d+)-(\d+)\*\*',
            r'\[(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d+)-(\d+)\]',
        ]
        
        all_theorems = set()
        for theorems in self.theorems.values():
            all_theorems.update(theorems)
        
        for pattern in ref_patterns:
            for match in re.finditer(pattern, content):
                theorem_id = f"{match.group(1)}-{match.group(2)}-{match.group(3)}-{match.group(4)}"
                if theorem_id not in all_theorems:
                    self.warnings.append({
                        'type': 'theorem_not_found',
                        'source': str(file_path),
                        'theorem': theorem_id,
                        'line': content[:match.start()].count('\n') + 1
                    })
    
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
                self.validate_theorem_refs(content, file_str)
            except Exception as e:
                print(f"扫描文件 {md_file} 时出错: {e}")
                
        print(f"提取到 {len(self.links)} 个内部链接")
        print(f"提取到 {sum(len(a) for a in self.anchors.values())} 个锚点")
        print(f"提取到 {sum(len(t) for t in self.theorems.values())} 个定理")
    
    def generate_report(self):
        """生成验证报告"""
        print("\n" + "="*60)
        print("交叉引用验证报告")
        print("="*60)
        print(f"\n验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"扫描文件数: {len(self.md_files)}")
        print(f"提取链接数: {len(self.links)}")
        print(f"\n错误数: {len(self.errors)}")
        print(f"警告数: {len(self.warnings)}")
        
        # 按类型分类错误
        file_errors = [e for e in self.errors if e['type'] == 'file_not_found']
        anchor_errors = [e for e in self.errors if e['type'] == 'anchor_not_found']
        theorem_warnings = [w for w in self.warnings if w['type'] == 'theorem_not_found']
        
        print(f"\n  - 文件不存在: {len(file_errors)}")
        print(f"  - 锚点不存在: {len(anchor_errors)}")
        print(f"  - 定理未找到: {len(theorem_warnings)}")
        
        # 保存详细报告
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_files': len(self.md_files),
                'total_links': len(self.links),
                'total_errors': len(self.errors),
                'total_warnings': len(self.warnings),
                'file_errors': len(file_errors),
                'anchor_errors': len(anchor_errors),
                'theorem_warnings': len(theorem_warnings)
            },
            'errors': self.errors,
            'warnings': self.warnings,
            'all_files': sorted(list(self.file_set)),
            'all_theorems': {k: sorted(list(v)) for k, v in self.theorems.items()},
            'all_anchors': {k: sorted(list(v)) for k, v in self.anchors.items()}
        }
        
        report_path = self.base_dir / '.stats/cross_ref_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n详细报告已保存到: {report_path}")
        
        # 输出前20个错误详情
        if self.errors:
            print("\n" + "-"*60)
            print("错误详情 (前20个):")
            print("-"*60)
            for i, err in enumerate(self.errors[:20], 1):
                print(f"\n{i}. [{err['type']}] 在 {err['source']}:{err['line']}")
                print(f"   链接: [{err['text']}]({err['url']})")
                if err['type'] == 'file_not_found':
                    print(f"   解析路径: {err.get('resolved', 'N/A')}")
                else:
                    print(f"   文件: {err.get('file', 'N/A')}, 锚点: {err.get('anchor', 'N/A')}")
        
        return report

def main():
    base_dir = Path(__file__).parent.parent
    validator = CrossRefValidator(base_dir)
    
    validator.collect_files()
    validator.scan_all_files()
    validator.validate_links()
    report = validator.generate_report()
    
    # 如果有错误，返回非零退出码
    if report['summary']['total_errors'] > 0:
        return 1
    return 0

if __name__ == '__main__':
    exit(main())
