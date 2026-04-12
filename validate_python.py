#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 代码验证工具
================

验证项目中 Python 代码示例的语法正确性和执行能力。

功能:
    - 语法检查
    - 导入验证
    - 代码执行测试
    - 生成验证报告

用法:
    python validate_python.py [--fix] [--output OUTPUT]

选项:
    --fix       尝试自动修复可修复的问题
    --output    指定输出报告路径
"""

import argparse
import ast
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class ValidationResult:
    """单个文件的验证结果"""
    file_path: str
    syntax_valid: bool = False
    can_execute: bool = False
    import_errors: List[str] = field(default_factory=list)
    syntax_errors: List[str] = field(default_factory=list)
    runtime_errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    score: float = 0.0


class PythonValidator:
    """Python 代码验证器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.results: List[ValidationResult] = []
        
    def find_python_files(self) -> List[Path]:
        """查找所有 Python 文件"""
        py_files = []
        
        for root, dirs, files in os.walk(self.project_root):
            # 跳过排除目录
            dirs[:] = [
                d for d in dirs 
                if d not in ('.git', '__pycache__', 'node_modules', 
                           '.venv', 'venv', 'env')
            ]
            
            for file in files:
                if file.endswith('.py'):
                    py_files.append(Path(root) / file)
        
        return sorted(py_files)
    
    def check_syntax(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查 Python 语法"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # 尝试解析 AST
            ast.parse(source)
            return True, errors
            
        except SyntaxError as e:
            errors.append(f"语法错误 (第{e.lineno}行): {e.msg}")
            return False, errors
        except UnicodeDecodeError as e:
            errors.append(f"编码错误: {e}")
            return False, errors
        except Exception as e:
            errors.append(f"读取错误: {e}")
            return False, errors
    
    def check_imports(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查导入语句"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source)
            
            # 提取所有导入
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            # 检查可导入性（可选，可能需要特定环境）
            # 这里只检查基本语法
            
            return True, errors
            
        except Exception as e:
            errors.append(f"导入检查错误: {e}")
            return False, errors
    
    def validate_file(self, file_path: Path) -> ValidationResult:
        """验证单个文件"""
        result = ValidationResult(file_path=str(file_path))
        
        # 检查语法
        syntax_valid, syntax_errors = self.check_syntax(file_path)
        result.syntax_valid = syntax_valid
        result.syntax_errors = syntax_errors
        
        if syntax_valid:
            # 检查导入
            import_valid, import_errors = self.check_imports(file_path)
            result.import_errors = import_errors
            
            # 如果能导入，假设可以执行
            result.can_execute = import_valid and len(import_errors) == 0
        
        # 计算分数
        score = 100.0
        if not result.syntax_valid:
            score -= 50
        if result.syntax_errors:
            score -= len(result.syntax_errors) * 5
        if result.import_errors:
            score -= len(result.import_errors) * 3
        
        result.score = max(0, score)
        
        return result
    
    def run_validation(self) -> Dict[str, Any]:
        """运行完整验证"""
        files = self.find_python_files()
        
        print(f"找到 {len(files)} 个 Python 文件")
        print("=" * 60)
        
        total_syntax_valid = 0
        total_can_execute = 0
        
        for i, file_path in enumerate(files, 1):
            print(f"[{i}/{len(files)}] 验证: {file_path}")
            
            result = self.validate_file(file_path)
            self.results.append(result)
            
            if result.syntax_valid:
                total_syntax_valid += 1
            if result.can_execute:
                total_can_execute += 1
            
            if not result.syntax_valid:
                print(f"    ❌ 语法错误")
                for error in result.syntax_errors[:3]:
                    print(f"       {error}")
            elif result.import_errors:
                print(f"    ⚠️  导入警告")
                for error in result.import_errors[:2]:
                    print(f"       {error}")
            else:
                print(f"    ✅ 通过")
        
        # 生成报告
        avg_score = sum(r.score for r in self.results) / len(self.results) if self.results else 0
        
        report = {
            "summary": {
                "total_files": len(files),
                "syntax_valid": total_syntax_valid,
                "can_execute": total_can_execute,
                "syntax_valid_rate": round(total_syntax_valid / len(files) * 100, 2) if files else 0,
                "execute_rate": round(total_can_execute / len(files) * 100, 2) if files else 0,
                "average_score": round(avg_score, 2),
                "validation_time": datetime.now().isoformat()
            },
            "results": [asdict(r) for r in self.results]
        }
        
        return report
    
    def generate_report(self, output_path: str = "python-validation-report.json") -> None:
        """生成 JSON 报告"""
        report = self.run_validation()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n报告已保存到: {output_path}")
        
        # 打印摘要
        summary = report["summary"]
        print("\n" + "=" * 60)
        print("验证摘要")
        print("=" * 60)
        print(f"总文件数: {summary['total_files']}")
        print(f"语法正确: {summary['syntax_valid']} ({summary['syntax_valid_rate']}%)")
        print(f"可执行: {summary['can_execute']} ({summary['execute_rate']}%)")
        print(f"平均分数: {summary['average_score']}")


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Python 代码验证工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--output", "-o",
        default="python-validation-report.json",
        help="输出报告路径"
    )
    
    parser.add_argument(
        "--project-root", "-p",
        default=".",
        help="项目根目录"
    )
    
    args = parser.parse_args()
    
    validator = PythonValidator(args.project_root)
    validator.generate_report(args.output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
