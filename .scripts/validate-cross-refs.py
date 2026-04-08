#!/usr/bin/env python3
"""
交叉引用验证脚本 - 检测并报告所有交叉引用错误
排除代码块、LaTeX表达式等误报
"""

import re
import os
import glob
import json
from pathlib import Path
from collections import defaultdict

class CrossRefValidator:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.errors = {
            'file_not_found': [],
            'anchor_not_found': [],
            'case_mismatch': [],
            'other': []
        }
        self.stats = {
            'files_checked': 0,
            'links_checked': 0,
            'valid_links': 0,
            'ignored': 0
        }
        self.all_file_paths = set()
        self.file_anchors = {}
        
        # 忽略的链接模式（代码片段、LaTeX等）
        self.ignore_patterns = [
            r'^\\[a-zA-Z]+',  # LaTeX命令如 \bar, \theta
            r'^Duration\.',   # Java Duration类
            r'^"[^"]*"$',     # 纯字符串如 "first"
            r'^input:',        # 代码参数
            r'^asyncFunc:',    # 代码参数
            r'^maxRetries:',   # 代码参数
            r'^v_\d+',         # 数学下标
            r'^\w+:\s*\w+',    # 类型注解如 fa: F[A]
            r'^\w+,\s*classOf', # Scala代码
            r'^\w+,\s*Types\.', # Flink代码
            r'^[\n\s]*\w+\s*=', # 赋值语句
            r'^[\n\s]*"[^"]+",', # 字符串参数
            r'^\s*$',          # 空内容
            r'^[\n\s]*\\?\w+\s*\[', # 泛型代码
            r'\bclassOf\[',    # Scala classOf
            r'\bTypes\.',      # Flink Types
            r'^\d+$',          # 纯数字
            r'^\d+\.',         # 数字加. 如 1.second, 2, 100
            r'^\d+,',          # 数字加, 
            r'^op:',           # Scala操作符参数
            r'^_',             # Scala下划线
            r'^targetActor',   # Akka参数
            r'^onComplete',    # Akka参数
            r'^onFailure',     # Akka参数
            r'^println',       # Scala函数
            r'^[a-z]+[A-Z]',   # 驼峰命名代码
            r'^state\.',       # 代码
            r'^update',        # 函数名
            r'^operation',     # 代码
            r'^fallback',      # 代码
            r'^line:',         # 代码参数
            r'^out:',          # 代码参数
            r'^Collector',     # 类型
            r'^len$',          # 变量名
            r'^[A-Z]$',        # 单个大写字母类型参数
            r'^x\s*=>',        # lambda
        ]
        
        # 忽略的文本模式（在[]中的内容）
        self.ignore_text_patterns = [
            r'^\s*$',          # 空文本
            r'^[\n\s]+$',      # 只有空白
            r'^[\s\n]*input:', # 代码
            r'^[\s\n]*asyncFunc:',
            r'^[\s\n]*maxRetries:',
            r'^[\s\n]*\"[^\"]+\",\s*\n', # 多行字符串参数
            r'^Int$',          # 类型名
            r'^String$',       # 类型名
            r'^T$',            # 类型参数
            r'^Byte$',         # 类型名
            r'^Double$',       # 类型名
            r'^IO$',            # 类型名
            r'^Event$',         # 类型名
            r'^TimeWindow$',    # 类型名
            r'^GlobalWindow$',  # 类型名
            r'^User$',          # 类型名
            r'^A$',             # 类型参数
            r'^\(String, Int\)$', # 类型元组
            r'^IO,',            # 多个类型
            r'^[A-Z][a-z]+,',   # 驼峰类型列表
        ]
    
    def should_ignore_link(self, text, link):
        """判断是否应该忽略此链接"""
        # 检查链接模式
        for pattern in self.ignore_patterns:
            if re.match(pattern, link):
                return True, f"匹配模式: {pattern}"
        
        # 检查文本模式
        for pattern in self.ignore_text_patterns:
            if re.match(pattern, text):
                return True, f"文本匹配: {pattern}"
        
        # 如果链接包含换行符且看起来像代码
        if '\n' in link and ('classOf' in link or 'Types.' in link or '=' in link):
            return True, "多行代码片段"
        
        # 如果链接看起来像LaTeX
        if link.startswith('\\') and not link.startswith('\\/'):  # 排除 \/ 这种路径
            return True, "LaTeX表达式"
            
        return False, None
    
    def get_all_markdown_files(self):
        """获取所有Markdown文件"""
        md_files = []
        for pattern in ["Struct/**/*.md", "Knowledge/**/*.md", "Flink/**/*.md"]:
            md_files.extend(glob.glob(str(self.base_path / pattern), recursive=True))
        for f in md_files:
            rel_path = os.path.relpath(f, self.base_path).replace("\\", "/")
            self.all_file_paths.add(rel_path.lower())
        return [f for f in md_files if not f.endswith("_TEMPLATE.md")]
    
    def extract_anchors(self, content):
        """从内容中提取所有锚点"""
        anchors = set()
        header_pattern = r'^#{1,6}\s+(.+)$'
        for match in re.finditer(header_pattern, content, re.MULTILINE):
            title = match.group(1).strip()
            anchor = self.generate_anchor(title)
            anchors.add(anchor)
            anchors.add(anchor.lower())
        return anchors
    
    def generate_anchor(self, title):
        """根据标题生成GitHub风格的锚点"""
        anchor = re.sub(r'<[^>]+>', '', title)
        anchor = re.sub(r'[^\w\s-]', '', anchor)
        anchor = re.sub(r'\s+', '-', anchor.strip())
        return anchor.lower()
    
    def get_file_anchors(self, file_path):
        """获取文件的所有锚点（带缓存）"""
        if file_path not in self.file_anchors:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.file_anchors[file_path] = self.extract_anchors(content)
            except:
                self.file_anchors[file_path] = set()
        return self.file_anchors[file_path]
    
    def find_similar_path(self, path):
        """查找相似路径（大小写不匹配的情况）"""
        path_lower = path.lower()
        for existing_path in self.all_file_paths:
            if existing_path == path_lower:
                return True
        return False
    
    def validate_link(self, text, link, source_file, line_num):
        """验证单个链接"""
        self.stats['links_checked'] += 1
        
        # 跳过外部链接和纯锚点链接
        if link.startswith("http") or link.startswith("#") or link.startswith("mailto:"):
            self.stats['valid_links'] += 1
            return None
        
        # 检查是否应该忽略
        should_ignore, reason = self.should_ignore_link(text, link)
        if should_ignore:
            self.stats['ignored'] += 1
            return None
        
        # 分离路径和锚点
        if "#" in link:
            path, anchor = link.split("#", 1)
        else:
            path, anchor = link, None
        
        error_info = {
            'source': str(source_file),
            'link': link,
            'text': text[:100] if len(text) > 100 else text,  # 限制长度
            'path': path,
            'anchor': anchor,
            'line': line_num
        }
        
        # 如果是相对路径，计算完整路径
        if path:
            if path.startswith("/"):
                full_path = self.base_path / path.lstrip("/")
            else:
                source_dir = Path(source_file).parent
                try:
                    full_path = (source_dir / path).resolve()
                except:
                    # 跨驱动器错误，使用备用方法
                    full_path = Path(os.path.normpath(str(source_dir / path)))
            
            try:
                rel_path = os.path.relpath(full_path, self.base_path).replace("\\", "/")
            except:
                # 跨驱动器错误，跳过
                return None
            
            # 检查文件是否存在
            if not full_path.exists():
                # 检查是否是大小写问题
                is_case_issue = self.find_similar_path(rel_path)
                if is_case_issue:
                    error_info['type'] = 'case_mismatch'
                    self.errors['case_mismatch'].append(error_info)
                    return error_info
                else:
                    error_info['type'] = 'file_not_found'
                    self.errors['file_not_found'].append(error_info)
                    return error_info
            
            # 如果文件存在但锚点不为空，检查锚点
            if anchor and full_path.suffix == '.md':
                anchors = self.get_file_anchors(str(full_path))
                anchor_normalized = anchor.lower()
                if anchor_normalized not in anchors and anchor not in anchors:
                    error_info['type'] = 'anchor_not_found'
                    self.errors['anchor_not_found'].append(error_info)
                    return error_info
        elif anchor:
            # 纯锚点链接，检查源文件的锚点
            anchors = self.get_file_anchors(str(source_file))
            anchor_normalized = anchor.lower()
            if anchor_normalized not in anchors and anchor not in anchors:
                error_info['type'] = 'anchor_not_found'
                error_info['local'] = True
                self.errors['anchor_not_found'].append(error_info)
                return error_info
        
        self.stats['valid_links'] += 1
        return None
    
    def validate_file(self, file_path):
        """验证单个文件中的所有链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self.stats['files_checked'] += 1
            content = ''.join(lines)
            
            # 找到所有链接及其行号
            link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
            for line_num, line in enumerate(lines, 1):
                for match in re.finditer(link_pattern, line):
                    text, link = match.groups()
                    self.validate_link(text, link, file_path, line_num)
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    def run(self):
        """运行验证流程"""
        print("=" * 80)
        print("交叉引用验证工具 v2.0")
        print("=" * 80)
        
        md_files = self.get_all_markdown_files()
        print(f"\n扫描文件数: {len(md_files)}")
        
        for i, file_path in enumerate(md_files):
            if (i + 1) % 100 == 0:
                print(f"  已检查: {i + 1}/{len(md_files)}")
            self.validate_file(file_path)
        
        # 输出统计
        print("\n" + "=" * 80)
        print("验证结果统计")
        print("=" * 80)
        print(f"检查文件数: {self.stats['files_checked']}")
        print(f"检查链接数: {self.stats['links_checked']}")
        print(f"有效链接数: {self.stats['valid_links']}")
        print(f"忽略的链接: {self.stats['ignored']}")
        print(f"\n错误分布:")
        print(f"  - 文件引用错误: {len(self.errors['file_not_found'])}")
        print(f"  - 锚点引用错误: {len(self.errors['anchor_not_found'])}")
        print(f"  - 大小写不匹配: {len(self.errors['case_mismatch'])}")
        print(f"  - 其他错误: {len(self.errors['other'])}")
        total_errors = sum(len(v) for v in self.errors.values())
        print(f"  ====================")
        print(f"  总计错误: {total_errors}")
        
        # 输出详细错误报告
        if total_errors > 0:
            print("\n" + "=" * 80)
            print("详细错误报告")
            print("=" * 80)
            
            if self.errors['file_not_found']:
                print(f"\n📁 文件引用错误 (共{len(self.errors['file_not_found'])}个):")
                for i, err in enumerate(self.errors['file_not_found'][:30], 1):
                    print(f"  {i}. [{err['source']}:{err.get('line', '?')}]")
                    print(f"     文本: {err['text'][:50]}..." if len(err['text']) > 50 else f"     文本: {err['text']}")
                    print(f"     链接: {err['link']}")
                if len(self.errors['file_not_found']) > 30:
                    print(f"     ... 还有 {len(self.errors['file_not_found']) - 30} 个错误")
            
            if self.errors['anchor_not_found']:
                print(f"\n🔗 锚点引用错误 (共{len(self.errors['anchor_not_found'])}个):")
                for i, err in enumerate(self.errors['anchor_not_found'][:30], 1):
                    print(f"  {i}. [{err['source']}:{err.get('line', '?')}]")
                    print(f"     链接: {err['link']}")
                if len(self.errors['anchor_not_found']) > 30:
                    print(f"     ... 还有 {len(self.errors['anchor_not_found']) - 30} 个错误")
            
            if self.errors['case_mismatch']:
                print(f"\n📝 大小写不匹配错误 (共{len(self.errors['case_mismatch'])}个):")
                for i, err in enumerate(self.errors['case_mismatch'][:10], 1):
                    print(f"  {i}. [{err['source']}:{err.get('line', '?')}]")
                    print(f"     链接: {err['link']}")
        
        # 保存详细报告到JSON
        report = {
            'stats': self.stats,
            'errors': self.errors,
            'summary': {
                'total_files': len(md_files),
                'total_errors': total_errors,
                'file_errors': len(self.errors['file_not_found']),
                'anchor_errors': len(self.errors['anchor_not_found']),
                'case_errors': len(self.errors['case_mismatch'])
            }
        }
        
        report_path = self.base_path / 'cross-ref-report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n详细报告已保存到: {report_path}")
        
        return total_errors

if __name__ == "__main__":
    import sys
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    validator = CrossRefValidator(base_path)
    errors = validator.run()
    sys.exit(min(errors, 255))  # 返回错误数作为退出码（限制在255以内）
