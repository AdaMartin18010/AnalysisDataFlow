#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码注释生成器 - Code Comment Generator for AnalysisDataFlow
基于规则分析生成代码注释，无需API Key

功能:
- 多语言代码注释生成
- 函数/类文档字符串生成
- 行内注释建议
- 支持 Python, Java, Scala, Rust, Go, JavaScript, TypeScript
"""

import os
import re
import sys
import yaml
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass
from enum import Enum


class Language(Enum):
    PYTHON = "python"
    JAVA = "java"
    SCALA = "scala"
    RUST = "rust"
    GO = "go"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"


@dataclass
class FunctionInfo:
    """函数信息"""
    name: str
    params: List[Tuple[str, str]]  # (name, type)
    return_type: str
    body: str
    docstring: str = ""


@dataclass
class ClassInfo:
    """类信息"""
    name: str
    attributes: List[Tuple[str, str]]
    methods: List[str]
    docstring: str = ""


class CodeCommentGenerator:
    """代码注释生成器"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        self.language_configs = self.config.get('code_comment', {}).get('languages', {})
    
    def _load_config(self, config_path: str = None) -> Dict:
        """加载配置文件"""
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__), 'config.yaml'
            )
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load config: {e}")
            return {}
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger('code-comment-generator')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def detect_language(self, file_path: str) -> Optional[Language]:
        """检测代码语言"""
        ext = Path(file_path).suffix.lower()
        
        mapping = {
            '.py': Language.PYTHON,
            '.java': Language.JAVA,
            '.scala': Language.SCALA,
            '.rs': Language.RUST,
            '.go': Language.GO,
            '.js': Language.JAVASCRIPT,
            '.ts': Language.TYPESCRIPT,
        }
        
        return mapping.get(ext)
    
    def parse_python_functions(self, content: str) -> List[FunctionInfo]:
        """解析 Python 函数"""
        functions = []
        
        # 匹配函数定义
        pattern = r'def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^:]+))?:\s*\n((?:\s+(?:"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|[^\n]*\n))*)'
        
        for match in re.finditer(pattern, content):
            name = match.group(1)
            params_str = match.group(2)
            return_type = match.group(3) or 'None'
            body = match.group(4)
            
            # 解析参数
            params = []
            for param in params_str.split(','):
                param = param.strip()
                if param and param != 'self' and param != 'cls':
                    if ':' in param:
                        p_name, p_type = param.split(':', 1)
                        params.append((p_name.strip(), p_type.strip()))
                    else:
                        params.append((param, 'Any'))
            
            # 检查已有 docstring
            docstring_match = re.search(r'^[\s]*("""|\'\'\')([\s\S]*?)\1', body)
            existing_docstring = docstring_match.group(2) if docstring_match else ""
            
            functions.append(FunctionInfo(
                name=name,
                params=params,
                return_type=return_type,
                body=body,
                docstring=existing_docstring
            ))
        
        return functions
    
    def parse_python_classes(self, content: str) -> List[ClassInfo]:
        """解析 Python 类"""
        classes = []
        
        pattern = r'class\s+(\w+)(?:\([^)]*\))?:\s*\n([\s\S]*?)(?=\nclass\s+|\Z)'
        
        for match in re.finditer(pattern, content):
            name = match.group(1)
            body = match.group(2)
            
            # 提取属性 (简单启发式)
            attributes = []
            for attr_match in re.finditer(r'self\.(\w+)\s*=\s*([^\n]+)', body):
                attr_name = attr_match.group(1)
                attr_value = attr_match.group(2)
                attributes.append((attr_name, type(attr_value).__name__))
            
            # 提取方法名
            methods = re.findall(r'def\s+(\w+)\s*\(', body)
            methods = [m for m in methods if m not in ['__init__']]
            
            # 检查已有 docstring
            docstring_match = re.search(r'^[\s]*("""|\'\'\')([\s\S]*?)\1', body)
            existing_docstring = docstring_match.group(2) if docstring_match else ""
            
            classes.append(ClassInfo(
                name=name,
                attributes=attributes,
                methods=methods,
                docstring=existing_docstring
            ))
        
        return classes
    
    def parse_java_functions(self, content: str) -> List[FunctionInfo]:
        """解析 Java 方法"""
        functions = []
        
        # 匹配方法定义
        pattern = r'(?:public|private|protected|static|\s)+[\w<>\[\]]+\s+(\w+)\s*\(([^)]*)\)\s*\{([\s\S]*?)\n\s*\}'
        
        for match in re.finditer(pattern, content):
            name = match.group(1)
            params_str = match.group(2)
            body = match.group(3)
            
            # 解析返回类型 (从前面提取)
            method_start = content[:match.start()].split('\n')[-1]
            return_type_match = re.search(r'(\w[\w<>\[\]]*)\s+' + name + r'\s*\(', method_start)
            return_type = return_type_match.group(1) if return_type_match else 'void'
            
            # 解析参数
            params = []
            for param in params_str.split(','):
                param = param.strip()
                if param:
                    parts = param.split()
                    if len(parts) >= 2:
                        params.append((parts[-1], ' '.join(parts[:-1])))
            
            functions.append(FunctionInfo(
                name=name,
                params=params,
                return_type=return_type,
                body=body
            ))
        
        return functions
    
    def generate_python_docstring(self, func: FunctionInfo) -> str:
        """生成 Python docstring"""
        lines = ['"""']
        
        # 功能描述
        lines.append(f"{func.name}")
        lines.append("")
        lines.append(f"功能: 实现{func.name}功能")
        lines.append("")
        
        # 参数
        if func.params:
            lines.append("参数:")
            for p_name, p_type in func.params:
                lines.append(f"    {p_name} ({p_type}): 参数描述")
            lines.append("")
        
        # 返回
        lines.append("返回:")
        lines.append(f"    {func.return_type}: 返回描述")
        lines.append("")
        
        # 示例
        lines.append("示例:")
        lines.append(f"    >>> {func.name}({', '.join([p[0] for p in func.params])})")
        lines.append("    结果")
        
        lines.append('"""')
        
        return '\n'.join(['    ' + line if line else '    ' for line in lines])
    
    def generate_python_class_docstring(self, cls: ClassInfo) -> str:
        """生成 Python 类 docstring"""
        lines = ['"""']
        
        lines.append(f"{cls.name}")
        lines.append("")
        lines.append(f"功能: {cls.name}类，实现相关功能")
        lines.append("")
        
        if cls.attributes:
            lines.append("属性:")
            for attr_name, attr_type in cls.attributes[:5]:  # 最多5个
                lines.append(f"    {attr_name}: {attr_type} - 属性描述")
            lines.append("")
        
        if cls.methods:
            lines.append("方法:")
            for method_name in cls.methods[:10]:  # 最多10个
                lines.append(f"    {method_name}(): 方法描述")
            lines.append("")
        
        lines.append("示例:")
        lines.append(f"    >>> obj = {cls.name}()")
        lines.append("    >>> obj.method()")
        
        lines.append('"""')
        
        return '\n'.join(['    ' + line if line else '    ' for line in lines])
    
    def generate_java_javadoc(self, func: FunctionInfo) -> str:
        """生成 Java Javadoc"""
        lines = ["/**"]
        
        lines.append(f" * {func.name}")
        lines.append(" * ")
        lines.append(f" * 功能: 实现{func.name}功能")
        lines.append(" * ")
        
        for p_name, p_type in func.params:
            lines.append(f" * @param {p_name} 参数描述 ({p_type})")
        
        lines.append(f" * @return 返回描述 ({func.return_type})")
        lines.append(" * ")
        lines.append(" * @example")
        lines.append(f" * {func.name}({', '.join([p[0] for p in func.params])});")
        
        lines.append(" */")
        
        return '\n'.join(lines)
    
    def generate_line_comments(self, content: str, language: Language) -> List[Tuple[int, str]]:
        """生成行内注释建议"""
        comments = []
        lines = content.split('\n')
        
        comment_patterns = {
            Language.PYTHON: '#',
            Language.JAVA: '//',
            Language.SCALA: '//',
            Language.RUST: '//',
            Language.GO: '//',
            Language.JAVASCRIPT: '//',
            Language.TYPESCRIPT: '//',
        }
        
        comment_prefix = comment_patterns.get(language, '//')
        
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # 跳过空行和已有注释
            if not line_stripped or line_stripped.startswith(comment_prefix):
                continue
            
            # 识别需要注释的模式
            comment = None
            
            # 复杂逻辑
            if re.search(r'if\s+.*and.*or', line_stripped):
                comment = f"{comment_prefix} 复合条件判断"
            elif re.search(r'for\s+.*in\s+range\(.*,.*,.*\)', line_stripped):
                comment = f"{comment_prefix} 带步长的循环"
            elif re.search(r'while\s+True', line_stripped):
                comment = f"{comment_prefix} 无限循环，需配合break使用"
            elif re.search(r'try\s*:', line_stripped) or re.search(r'try\s*\{', line_stripped):
                comment = f"{comment_prefix} 异常处理开始"
            elif '= []' in line_stripped or '= {}' in line_stripped or '= set()' in line_stripped:
                comment = f"{comment_prefix} 初始化空数据结构"
            elif re.search(r'\.get\(|\.pop\(|\.append\(|\.extend\(', line_stripped):
                comment = f"{comment_prefix} 数据结构操作"
            elif re.search(r'return\s+', line_stripped):
                comment = f"{comment_prefix} 返回结果"
            elif re.search(r'raise\s+\w+|throw\s+new', line_stripped):
                comment = f"{comment_prefix} 抛出异常"
            elif re.search(r'import\s+|from\s+.*import|#include|using\s+', line_stripped):
                comment = f"{comment_prefix} 导入依赖"
            
            if comment:
                comments.append((i, comment))
        
        return comments
    
    def process_python_file(self, content: str) -> str:
        """处理 Python 文件"""
        result = content
        
        # 处理函数
        functions = self.parse_python_functions(content)
        for func in functions:
            if not func.docstring:  # 没有现有 docstring
                docstring = self.generate_python_docstring(func)
                # 在函数定义后插入 docstring
                pattern = rf'(def\s+{func.name}\s*\([^)]*\)(?:\s*->\s*[^:]+)?:\s*\n)'
                replacement = rf'\1{docstring}\n'
                result = re.sub(pattern, replacement, result, count=1)
        
        # 处理类
        classes = self.parse_python_classes(content)
        for cls in classes:
            if not cls.docstring:
                docstring = self.generate_python_class_docstring(cls)
                pattern = rf'(class\s+{cls.name}(?:\([^)]*\))?:\s*\n)'
                replacement = rf'\1{docstring}\n'
                result = re.sub(pattern, replacement, result, count=1)
        
        return result
    
    def process_java_file(self, content: str) -> str:
        """处理 Java 文件"""
        result = content
        
        functions = self.parse_java_functions(content)
        for func in functions:
            javadoc = self.generate_java_javadoc(func)
            
            # 查找方法位置
            pattern = rf'((?:public|private|protected|static|\s)+[\w<>\[\]]+\s+{func.name}\s*\([^)]*\))'
            
            # 检查是否已有 Javadoc
            method_pos = result.find(f"{func.name}(")
            if method_pos > 0:
                before = result[max(0, method_pos-50):method_pos]
                if '/**' not in before:
                    replacement = f"{javadoc}\n    \\1"
                    result = re.sub(pattern, replacement, result, count=1)
        
        return result
    
    def process_file(self, file_path: str, inline_comments: bool = False) -> str:
        """处理文件并生成注释"""
        language = self.detect_language(file_path)
        if not language:
            self.logger.warning(f"Unsupported file type: {file_path}")
            return None
        
        self.logger.info(f"Processing {file_path} ({language.value})")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 根据语言处理
        if language == Language.PYTHON:
            result = self.process_python_file(content)
        elif language in [Language.JAVA, Language.SCALA]:
            result = self.process_java_file(content)
        else:
            # 其他语言：仅生成行内注释建议
            result = content
        
        # 添加行内注释建议
        if inline_comments:
            line_comments = self.generate_line_comments(content, language)
            lines = result.split('\n')
            # 从后往前插入，避免行号变化
            for line_num, comment in sorted(line_comments, reverse=True):
                if line_num <= len(lines):
                    indent = len(lines[line_num - 1]) - len(lines[line_num - 1].lstrip())
                    lines.insert(line_num, ' ' * indent + comment)
            result = '\n'.join(lines)
        
        return result
    
    def save_processed(self, file_path: str, content: str, suffix: str = '.commented') -> str:
        """保存处理后的文件"""
        path = Path(file_path)
        output_path = path.parent / f"{path.stem}{suffix}{path.suffix}"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"Saved to: {output_path}")
        return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description='代码注释生成器 - AnalysisDataFlow AI Assistant'
    )
    parser.add_argument(
        'input',
        help='输入文件或目录路径'
    )
    parser.add_argument(
        '-o', '--output',
        help='输出文件路径 (默认: 添加 .commented 后缀)'
    )
    parser.add_argument(
        '-c', '--config',
        help='配置文件路径'
    )
    parser.add_argument(
        '--inline',
        action='store_true',
        help='添加行内注释建议'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='批量处理目录'
    )
    parser.add_argument(
        '--extensions',
        help='文件扩展名列表 (逗号分隔)',
        default='py,java,scala,rs,go,js,ts'
    )
    parser.add_argument(
        '--stdout',
        action='store_true',
        help='输出到标准输出'
    )
    
    args = parser.parse_args()
    
    generator = CodeCommentGenerator(args.config)
    
    if args.batch or os.path.isdir(args.input):
        extensions = args.extensions.split(',')
        for ext in extensions:
            for file_path in Path(args.input).rglob(f'*.{ext}'):
                try:
                    result = generator.process_file(str(file_path), args.inline)
                    if result and not args.stdout:
                        generator.save_processed(str(file_path), result)
                    elif result and args.stdout:
                        print(f"=== {file_path} ===")
                        print(result)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    else:
        result = generator.process_file(args.input, args.inline)
        if result:
            if args.stdout:
                print(result)
            elif args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"Saved to: {args.output}")
            else:
                generator.save_processed(args.input, result)


if __name__ == '__main__':
    main()
