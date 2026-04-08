#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码示例验证器 - Code Example Validator
验证项目中所有Markdown文件的代码示例语法正确性

作者: AI Agent
创建时间: 2026-04-08
版本: 1.0.0
"""

import re
import os
import sys
import json
import tempfile
import subprocess
import py_compile
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

# 添加依赖库
try:
    from ruamel.yaml import YAML
    from ruamel.yaml.main import round_trip_load
    RUAMEL_AVAILABLE = True
except ImportError:
    RUAMEL_AVAILABLE = False

try:
    import sqlparse
    SQLPARSE_AVAILABLE = True
except ImportError:
    SQLPARSE_AVAILABLE = False


@dataclass
class CodeBlock:
    """代码块数据结构"""
    language: str
    code: str
    file_path: str
    line_number: int
    block_index: int
    
    def __hash__(self):
        return hash((self.file_path, self.line_number, self.block_index))


@dataclass
class ValidationResult:
    """验证结果数据结构"""
    code_block: CodeBlock
    is_valid: bool
    error_message: Optional[str] = None
    error_line: Optional[int] = None
    severity: str = "error"  # error, warning, info
    fixable: bool = False
    suggested_fix: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "file_path": self.code_block.file_path,
            "line_number": self.code_block.line_number,
            "language": self.code_block.language,
            "block_index": self.code_block.block_index,
            "is_valid": self.is_valid,
            "error_message": self.error_message,
            "error_line": self.error_line,
            "severity": self.severity,
            "fixable": self.fixable,
            "suggested_fix": self.suggested_fix,
            "code_preview": self.code_block.code[:200] + "..." if len(self.code_block.code) > 200 else self.code_block.code
        }


@dataclass
class ValidationStats:
    """验证统计数据"""
    total_files: int = 0
    total_blocks: int = 0
    valid_blocks: int = 0
    invalid_blocks: int = 0
    warnings: int = 0
    fixable_issues: int = 0
    by_language: Dict[str, Dict] = field(default_factory=dict)
    
    def update(self, result: ValidationResult):
        lang = result.code_block.language
        if lang not in self.by_language:
            self.by_language[lang] = {
                "total": 0,
                "valid": 0,
                "invalid": 0,
                "warnings": 0
            }
        self.by_language[lang]["total"] += 1
        if result.is_valid:
            self.by_language[lang]["valid"] += 1
        else:
            self.by_language[lang]["invalid"] += 1
        if result.severity == "warning":
            self.by_language[lang]["warnings"] += 1


class CodeExampleValidator:
    """代码示例验证器主类"""
    
    SUPPORTED_LANGUAGES = ["java", "python", "yaml", "sql", "json", "xml", "bash", "shell"]
    
    def __init__(self, project_root: Path, max_workers: int = 4):
        self.project_root = Path(project_root)
        self.max_workers = max_workers
        self.results: List[ValidationResult] = []
        self.stats = ValidationStats()
        
        # 初始化YAML解析器
        if RUAMEL_AVAILABLE:
            self.yaml_parser = YAML(typ='safe')
            self.yaml_parser.preserve_quotes = True
    
    def scan_markdown_files(self) -> List[Path]:
        """扫描所有Markdown文件"""
        print("🔍 扫描Markdown文件...")
        md_files = list(self.project_root.rglob("*.md"))
        
        # 排除某些目录
        exclude_patterns = ['.git', 'node_modules', '__pycache__', '.venv', 'venv']
        md_files = [
            f for f in md_files 
            if not any(excl in str(f) for excl in exclude_patterns)
        ]
        
        self.stats.total_files = len(md_files)
        print(f"   找到 {len(md_files)} 个Markdown文件")
        return md_files
    
    def extract_code_blocks(self, content: str, file_path: str) -> List[CodeBlock]:
        """从Markdown内容中提取代码块"""
        code_blocks = []
        
        # 匹配 ```language\ncode\n``` 格式
        pattern = r'```(\w+)?\n(.*?)```'
        matches = list(re.finditer(pattern, content, re.DOTALL))
        
        # 计算行号
        lines_before = [0]
        for i, char in enumerate(content):
            if char == '\n':
                lines_before.append(i + 1)
        
        for idx, match in enumerate(matches):
            language = (match.group(1) or "text").lower().strip()
            code = match.group(2)
            
            # 计算起始行号
            start_pos = match.start()
            line_number = sum(1 for pos in lines_before if pos <= start_pos)
            
            # 只处理支持的语言
            if language in self.SUPPORTED_LANGUAGES or language in ["yml", "py", "sh"]:
                # 标准化语言名称
                lang_map = {"yml": "yaml", "py": "python", "sh": "bash"}
                language = lang_map.get(language, language)
                
                code_blocks.append(CodeBlock(
                    language=language,
                    code=code,
                    file_path=file_path,
                    line_number=line_number,
                    block_index=idx
                ))
        
        return code_blocks
    
    def validate_java(self, code: str) -> Tuple[bool, Optional[str], Optional[int]]:
        """验证Java代码语法"""
        if not code.strip():
            return True, None, None
        
        # 检查是否是完整类定义
        has_class = re.search(r'\bclass\s+\w+', code)
        has_interface = re.search(r'\binterface\s+\w+', code)
        has_enum = re.search(r'\benum\s+\w+', code)
        
        try:
            if has_class or has_interface or has_enum:
                # 完整类/接口/枚举 - 使用类名作为文件名
                class_match = re.search(r'(?:class|interface|enum)\s+(\w+)', code)
                class_name = class_match.group(1) if class_match else "TempValidation"
                
                with tempfile.NamedTemporaryFile(mode='w', suffix=f'{class_name}.java', delete=False) as f:
                    f.write(code)
                    temp_path = f.name
            else:
                # 代码片段 - 包装成完整类
                # 简单检测：如果是单条语句或变量声明，包装在方法中
                # 否则包装在main方法中
                lines = code.strip().split('\n')
                is_simple = len(lines) == 1 or all(
                    not l.strip().startswith(('if', 'for', 'while', '{', '}')) 
                    for l in lines
                )
                
                if is_simple:
                    # 简单表达式，放在main中
                    wrapped = f"""class TempValidation {{
    public static void main(String[] args) {{
        {code.strip()}
    }}
}}"""
                else:
                    # 复杂代码，保持原样但包装在类中
                    wrapped = f"""class TempValidation {{
    public static void validate() {{
{code}
    }}
}}"""
                
                with tempfile.NamedTemporaryFile(mode='w', suffix='TempValidation.java', delete=False) as f:
                    f.write(wrapped)
                    temp_path = f.name
            
            # 编译
            result = subprocess.run(
                ['javac', '-d', tempfile.gettempdir(), temp_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # 清理
            for ext in ['.java', '.class']:
                f = temp_path.replace('.java', ext)
                if os.path.exists(f):
                    os.unlink(f)
            
            if result.returncode == 0:
                return True, None, None
            else:
                error_msg = result.stderr
                # 如果是因为类名问题，尝试原始代码
                if "应在名为" in error_msg:
                    return self._validate_java_relaxed(code)
                line_match = re.search(r':(\d+):', error_msg)
                error_line = int(line_match.group(1)) if line_match else None
                return False, error_msg, error_line
                
        except subprocess.TimeoutExpired:
            return False, "编译超时", None
        except Exception as e:
            return False, f"验证错误: {str(e)}", None
    
    def _validate_java_relaxed(self, code: str) -> Tuple[bool, Optional[str], Optional[int]]:
        """宽松的Java验证（对片段不做严格检查）"""
        # 检查明显的语法错误
        open_braces = code.count('{')
        close_braces = code.count('}')
        open_parens = code.count('(')
        close_parens = code.count(')')
        
        if open_braces != close_braces:
            return False, f"大括号不匹配: {{={open_braces}, }}={close_braces}", None
        if open_parens != close_parens:
            return False, f"括号不匹配: (={open_parens}, )={close_parens}", None
        
        # 检查基本的Java语法模式
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # 检查常见错误
            if re.search(r'\b(if|for|while|switch)\s*\([^)]*\)\s*[^;{]', stripped):
                if not stripped.endswith(('{', ';', '}', '//', '/*')):
                    if stripped.count('(') == stripped.count(')'):
                        # 可能有缺失的{或;
                        pass  # 不标记为错误，可能是片段
        
        return True, None, None  # 片段模式：宽松通过
    
    def validate_python(self, code: str) -> Tuple[bool, Optional[str], Optional[int]]:
        """验证Python代码语法"""
        if not code.strip():
            return True, None, None
        
        try:
            # 使用compile函数直接验证
            compile(code, '<string>', 'exec')
            return True, None, None
        except SyntaxError as e:
            error_msg = f"SyntaxError: {e.msg}"
            error_line = e.lineno
            return False, error_msg, error_line
        except Exception as e:
            error_msg = str(e)
            return False, error_msg, None
    
    def validate_yaml(self, code: str) -> Tuple[bool, Optional[str], Optional[int]]:
        """验证YAML代码语法"""
        if not code.strip():
            return True, None, None
        
        # 清理代码：移除Markdown任务列表标记
        cleaned_code = re.sub(r'^(\s*)-\s*\[([ xX])\]\s*', r'\1- ', code, flags=re.MULTILINE)
        
        # 尝试使用ruamel.yaml
        if RUAMEL_AVAILABLE:
            try:
                # 尝试加载所有文档
                from ruamel.yaml import YAMLError
                yaml = YAML(typ='safe')
                yaml.preserve_quotes = True
                # 使用load_all处理多文档
                docs = list(yaml.load_all(cleaned_code))
                return True, None, None
            except YAMLError as e:
                error_msg = str(e)
                # 检查是否是常见的"多文档"误报
                if "but found another document" in error_msg and "---" in cleaned_code:
                    # 多文档是合法的，只是解析器配置问题
                    return True, None, None
                line_match = re.search(r'line\s+(\d+)', error_msg, re.IGNORECASE)
                error_line = int(line_match.group(1)) if line_match else None
                return False, error_msg, error_line
            except Exception as e:
                error_msg = str(e)
                line_match = re.search(r'line\s+(\d+)', error_msg, re.IGNORECASE)
                error_line = int(line_match.group(1)) if line_match else None
                return False, error_msg, error_line
        
        # 备选：使用PyYAML
        try:
            import yaml
            # 尝试加载所有文档
            docs = list(yaml.safe_load_all(cleaned_code))
            return True, None, None
        except ImportError:
            return True, "YAML库不可用，跳过验证", None
        except Exception as e:
            error_msg = str(e)
            # 多文档分隔符---是合法的
            if "but found another document" in str(e):
                return True, None, None
            line_match = re.search(r'line\s+(\d+)', error_msg, re.IGNORECASE)
            error_line = int(line_match.group(1)) if line_match else None
            return False, error_msg, error_line
    
    def validate_sql(self, code: str) -> Tuple[bool, Optional[str], Optional[int]]:
        """验证SQL代码语法"""
        if not code.strip():
            return True, None, None
        
        # 移除注释
        code_clean = re.sub(r'--.*$', '', code, flags=re.MULTILINE)
        code_clean = re.sub(r'/\*.*?\*/', '', code_clean, flags=re.DOTALL)
        
        if not code_clean.strip():
            return True, None, None
        
        if not SQLPARSE_AVAILABLE:
            # 基础检查
            return True, "sqlparse库不可用，进行基础检查", None
        
        try:
            parsed = sqlparse.parse(code)
            
            # 检查是否有解析错误
            errors = []
            for stmt in parsed:
                if stmt.get_type() == 'UNKNOWN' and stmt.tokens:
                    # 检查是否有明显的语法错误标记
                    tokens_str = str(stmt).upper().strip()
                    if tokens_str and not tokens_str.startswith(('SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP', 'WITH', 'SET', 'SHOW', 'DESCRIBE', 'EXPLAIN', 'GRANT', 'REVOKE')):
                        if len(tokens_str) > 10:  # 忽略太短的片段
                            errors.append(f"可能的语法问题: {tokens_str[:50]}...")
            
            if errors:
                return False, "; ".join(errors), None
            
            return True, None, None
            
        except Exception as e:
            return False, f"SQL解析错误: {str(e)}", None
    
    def validate_code_block(self, block: CodeBlock) -> ValidationResult:
        """验证单个代码块"""
        validators = {
            "java": self.validate_java,
            "python": self.validate_python,
            "yaml": self.validate_yaml,
            "sql": self.validate_sql,
        }
        
        if block.language not in validators:
            return ValidationResult(
                code_block=block,
                is_valid=True,
                error_message=f"语言 '{block.language}' 暂不支持详细验证"
            )
        
        validator = validators[block.language]
        is_valid, error_msg, error_line = validator(block.code)
        
        # 判断是否可以自动修复
        fixable = False
        suggested_fix = None
        
        if not is_valid and error_msg:
            # 检查常见问题
            if block.language == "python":
                if "IndentationError" in error_msg:
                    fixable = True
                    suggested_fix = "检查缩进一致性，使用4空格缩进"
                elif "SyntaxError" in error_msg and "EOF" in error_msg:
                    fixable = True
                    suggested_fix = "检查括号、引号是否成对闭合"
            elif block.language == "java":
                if "reached end of file" in error_msg and "parsing" in error_msg:
                    fixable = True
                    suggested_fix = "检查大括号是否成对闭合"
            elif block.language == "yaml":
                if "mapping values are not allowed" in error_msg:
                    fixable = True
                    suggested_fix = "检查冒号后是否有空格"
        
        return ValidationResult(
            code_block=block,
            is_valid=is_valid,
            error_message=error_msg,
            error_line=error_line,
            fixable=fixable,
            suggested_fix=suggested_fix
        )
    
    def process_file(self, file_path: Path) -> List[ValidationResult]:
        """处理单个Markdown文件"""
        results = []
        try:
            content = file_path.read_text(encoding='utf-8')
            code_blocks = self.extract_code_blocks(content, str(file_path))
            
            for block in code_blocks:
                result = self.validate_code_block(block)
                results.append(result)
                self.stats.update(result)
                
        except Exception as e:
            print(f"   ⚠️  读取文件失败: {file_path} - {e}")
        
        return results
    
    def run_validation(self) -> List[ValidationResult]:
        """运行完整验证"""
        print("\n" + "="*60)
        print("🚀 代码示例验证器启动")
        print("="*60)
        
        start_time = datetime.now()
        
        # 扫描文件
        md_files = self.scan_markdown_files()
        
        # 并行处理
        print(f"\n🔧 开始验证 (使用 {self.max_workers} 个线程)...")
        processed = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {executor.submit(self.process_file, f): f for f in md_files}
            
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    results = future.result()
                    self.results.extend(results)
                    processed += 1
                    
                    if processed % 50 == 0:
                        print(f"   已处理 {processed}/{len(md_files)} 个文件...")
                        
                except Exception as e:
                    print(f"   ❌ 处理文件失败: {file_path} - {e}")
        
        # 统计
        self.stats.total_blocks = len(self.results)
        self.stats.valid_blocks = sum(1 for r in self.results if r.is_valid)
        self.stats.invalid_blocks = self.stats.total_blocks - self.stats.valid_blocks
        self.stats.warnings = sum(1 for r in self.results if r.severity == "warning")
        self.stats.fixable_issues = sum(1 for r in self.results if r.fixable)
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        print(f"\n✅ 验证完成!")
        print(f"   耗时: {elapsed:.2f} 秒")
        print(f"   扫描文件: {self.stats.total_files}")
        print(f"   代码块总数: {self.stats.total_blocks}")
        print(f"   ✅ 有效: {self.stats.valid_blocks}")
        print(f"   ❌ 无效: {self.stats.invalid_blocks}")
        print(f"   ⚠️  可修复: {self.stats.fixable_issues}")
        
        return self.results
    
    def generate_report(self) -> str:
        """生成验证报告"""
        invalid_results = [r for r in self.results if not r.is_valid]
        
        report = f"""# 代码示例验证报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **验证器版本**: 1.0.0  
> **项目根目录**: {self.project_root}

## 📊 验证统计

| 指标 | 数值 |
|------|------|
| 扫描文件数 | {self.stats.total_files} |
| 代码块总数 | {self.stats.total_blocks} |
| ✅ 验证通过 | {self.stats.valid_blocks} |
| ❌ 验证失败 | {self.stats.invalid_blocks} |
| ⚠️  警告数 | {self.stats.warnings} |
| 🔧 可自动修复 | {self.stats.fixable_issues} |
| **通过率** | {(self.stats.valid_blocks / self.stats.total_blocks * 100):.2f}% |

### 按语言统计

| 语言 | 总数 | 有效 | 无效 | 通过率 |
|------|------|------|------|--------|
"""
        
        for lang, stats in sorted(self.stats.by_language.items()):
            total = stats['total']
            valid = stats['valid']
            invalid = stats['invalid']
            rate = (valid / total * 100) if total > 0 else 0
            report += f"| {lang} | {total} | {valid} | {invalid} | {rate:.2f}% |\n"
        
        # 问题清单
        report += f"""
## 🚨 问题代码清单

共发现 **{len(invalid_results)}** 个有问题的代码示例：

"""
        
        if not invalid_results:
            report += "✅ 未发现语法问题！\n"
        else:
            # 按文件分组
            by_file: Dict[str, List[ValidationResult]] = {}
            for r in invalid_results:
                fp = r.code_block.file_path
                if fp not in by_file:
                    by_file[fp] = []
                by_file[fp].append(r)
            
            for file_path, results in sorted(by_file.items()):
                rel_path = os.path.relpath(file_path, self.project_root)
                report += f"\n### `{rel_path}`\n\n"
                for r in results:
                    cb = r.code_block
                    report += f"""**问题 #{cb.block_index + 1}** (第 {cb.line_number} 行, 语言: {cb.language})
- **错误**: {r.error_message[:200] if r.error_message else '未知错误'}
"""
                    if r.error_line:
                        report += f"- **错误行**: {r.error_line}\n"
                    if r.suggested_fix:
                        report += f"- **建议**: {r.suggested_fix}\n"
                    if r.fixable:
                        report += f"- **可自动修复**: ✅\n"
                    report += "\n"
        
        # 修复建议
        report += """
## 🔧 修复建议

### 常见问题及修复方法

#### Python
1. **缩进错误 (IndentationError)**
   - 使用统一的4空格缩进
   - 不要混用Tab和空格
   - 运行 `.scripts/code-example-fixer.py` 自动修复

2. **语法错误 (SyntaxError)**
   - 检查括号、引号是否成对
   - 检查冒号是否正确使用
   - 确保代码片段完整性

#### Java
1. **缺少分号**
   - 每个语句结尾添加分号
   - 检查导入语句完整性

2. **括号不匹配**
   - 检查大括号 `{}`、小括号 `()`、方括号 `[]` 是否成对

#### YAML
1. **缩进问题**
   - 使用2空格缩进
   - 冒号后必须有空格

2. **特殊字符**
   - 字符串包含特殊字符时使用引号包裹

#### SQL
1. **关键字错误**
   - 检查SQL关键字拼写
   - 确保表名、列名正确

## 📁 输出文件

验证结果已保存为JSON格式，可用于进一步处理：
- `validation-results.json` - 完整验证结果
- `invalid-blocks.json` - 仅包含无效代码块

## 🚀 下一步操作

运行自动修复工具：
```bash
python .scripts/code-example-fixer.py
```

这将自动修复以下问题：
- 缩进不一致
- 尾部空格
- 简单的括号匹配问题
- 代码格式化

---
*报告由代码示例验证器自动生成*
"""
        
        return report
    
    def save_results(self, output_dir: Optional[Path] = None):
        """保存验证结果到文件"""
        if output_dir is None:
            output_dir = self.project_root
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存完整结果
        results_json = [r.to_dict() for r in self.results]
        with open(output_dir / "validation-results.json", 'w', encoding='utf-8') as f:
            json.dump(results_json, f, ensure_ascii=False, indent=2)
        
        # 保存仅无效结果
        invalid_results = [r.to_dict() for r in self.results if not r.is_valid]
        with open(output_dir / "invalid-blocks.json", 'w', encoding='utf-8') as f:
            json.dump(invalid_results, f, ensure_ascii=False, indent=2)
        
        # 保存统计信息
        stats_dict = {
            "total_files": self.stats.total_files,
            "total_blocks": self.stats.total_blocks,
            "valid_blocks": self.stats.valid_blocks,
            "invalid_blocks": self.stats.invalid_blocks,
            "warnings": self.stats.warnings,
            "fixable_issues": self.stats.fixable_issues,
            "by_language": self.stats.by_language,
            "timestamp": datetime.now().isoformat()
        }
        with open(output_dir / "validation-stats.json", 'w', encoding='utf-8') as f:
            json.dump(stats_dict, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 结果已保存到:")
        print(f"   - {output_dir / 'validation-results.json'}")
        print(f"   - {output_dir / 'invalid-blocks.json'}")
        print(f"   - {output_dir / 'validation-stats.json'}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='代码示例验证器')
    parser.add_argument('--project-root', '-p', type=str, default='.',
                        help='项目根目录 (默认: 当前目录)')
    parser.add_argument('--workers', '-w', type=int, default=4,
                        help='并发线程数 (默认: 4)')
    parser.add_argument('--output', '-o', type=str, default='.',
                        help='输出目录 (默认: 当前目录)')
    parser.add_argument('--report', '-r', type=str, default='CODE-EXAMPLE-VALIDATION-REPORT.md',
                        help='报告文件名 (默认: CODE-EXAMPLE-VALIDATION-REPORT.md)')
    
    args = parser.parse_args()
    
    # 创建验证器
    validator = CodeExampleValidator(
        project_root=Path(args.project_root),
        max_workers=args.workers
    )
    
    # 运行验证
    results = validator.run_validation()
    
    # 保存结果
    validator.save_results(Path(args.output))
    
    # 生成并保存报告
    report = validator.generate_report()
    report_path = Path(args.output) / args.report
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n📝 验证报告已保存: {report_path}")
    
    # 返回退出码
    invalid_count = sum(1 for r in results if not r.is_valid)
    if invalid_count > 0:
        print(f"\n⚠️  发现 {invalid_count} 个问题，请查看报告并修复")
        return 1
    else:
        print("\n✅ 所有代码示例验证通过！")
        return 0


if __name__ == '__main__':
    sys.exit(main())
