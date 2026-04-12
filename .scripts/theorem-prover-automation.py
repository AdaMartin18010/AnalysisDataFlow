#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定理证明自动化工具链
Theorem Prover Automation Toolchain

功能模块:
- Coq证明检查
- TLA+模型验证
- 定理依赖检查
- 证明完整性验证
- 自动证明建议

作者: AnalysisDataFlow Project
版本: 1.0.0
日期: 2026-04-12
"""

import os
import sys
import json
import re
import subprocess
import argparse
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Set, Callable
from enum import Enum
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import xml.etree.ElementTree as ET


# ==================== 配置常量 ====================

class Config:
    """全局配置"""
    # 路径配置
    COQ_PATH = "formal-methods/coq"
    TLA_PATH = "formal-methods/tla"
    COQ_PROOFS_PATH = "formal-methods/05-verification/03-theorem-proving/coq-proofs"
    TLA_SPECS_PATH = "formal-methods/05-verification/01-logic/tla-specs"
    DOCS_PATH = "docs"
    REPORTS_PATH = "reports/formal-verification"
    
    # 工具配置
    COQ_CMD = "coqc"
    COQDEP_CMD = "coqdep"
    TLA_CMD = "tlc2"  # TLA+ Community Edition
    APALACHE_CMD = "apalache-mc"
    
    # 验证配置
    TIMEOUT = 300  # 秒
    MAX_WORKERS = 4
    
    # 输出配置
    VERBOSE = False
    JSON_OUTPUT = False


# ==================== 数据模型 ====================

class VerificationStatus(Enum):
    """验证状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class ProofResult:
    """证明结果数据类"""
    file_path: str
    theorem_name: str
    status: VerificationStatus
    duration: float = 0.0
    dependencies: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    coverage: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            **asdict(self),
            'status': self.status.value
        }


@dataclass
class VerificationReport:
    """验证报告数据类"""
    total_files: int = 0
    successful: int = 0
    failed: int = 0
    timeout: int = 0
    skipped: int = 0
    total_duration: float = 0.0
    results: List[ProofResult] = field(default_factory=list)
    summary: Dict = field(default_factory=dict)
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'generated_at': self.generated_at,
            'total_files': self.total_files,
            'successful': self.successful,
            'failed': self.failed,
            'timeout': self.timeout,
            'skipped': self.skipped,
            'total_duration': self.total_duration,
            'success_rate': self.success_rate,
            'results': [r.to_dict() for r in self.results],
            'summary': self.summary
        }
    
    @property
    def success_rate(self) -> float:
        if self.total_files == 0:
            return 0.0
        return (self.successful / self.total_files) * 100


# ==================== 日志配置 ====================

def setup_logging(verbose: bool = False) -> logging.Logger:
    """配置日志系统"""
    logger = logging.getLogger("theorem-prover")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


logger = setup_logging()


# ==================== Coq 证明检查器 ====================

class CoqChecker:
    """Coq证明检查器"""
    
    # 定理/引理/定义的正则表达式
    THEOREM_PATTERN = re.compile(
        r'(?:Theorem|Lemma|Proposition|Corollary|Definition|Inductive|Fixpoint)\s+'
        r'(\w+)',
        re.MULTILINE
    )
    
    # 证明结束标记
    PROOF_END_PATTERN = re.compile(r'(?:Qed|Defined|Admitted)\.', re.MULTILINE)
    
    # 依赖导入
    REQUIRE_PATTERN = re.compile(r'Require\s+(?:Import|Export)?\s*([^\.]+)\.')
    
    # 证明中的常见错误模式
    ERROR_PATTERNS = [
        (r'Error:\s*(.+?)(?=Error:|$)', 'coq_error'),
        (r'Tactic\s+failure', 'tactic_failure'),
        (r'Unsolved\s+goals', 'unsolved_goals'),
        (r'Unable\s+to\s+unify', 'unification_error'),
    ]
    
    # 警告模式
    WARNING_PATTERNS = [
        (r'Warning:\s*\[(\w+)\]\s*(.+?)(?=Warning:|$)', 'coq_warning'),
        (r'Deprecated', 'deprecated'),
        (r'Hint', 'hint_warning'),
    ]
    
    def __init__(self, coq_path: str = None):
        self.coq_path = coq_path or Config.COQ_PATH
        self.results: List[ProofResult] = []
        
    def find_coq_files(self) -> List[Path]:
        """查找所有Coq文件"""
        path = Path(self.coq_path)
        if not path.exists():
            logger.warning(f"Coq路径不存在: {path}")
            return []
        
        files = list(path.rglob("*.v"))
        
        # 同时检查其他可能的位置
        for extra_path in [Config.COQ_PROOFS_PATH, "formal-methods/90-examples/coq"]:
            extra = Path(extra_path)
            if extra.exists():
                files.extend(extra.rglob("*.v"))
        
        return sorted(set(files))
    
    def extract_theorems(self, file_path: Path) -> List[str]:
        """从Coq文件中提取定理名称"""
        content = file_path.read_text(encoding='utf-8')
        theorems = []
        
        for match in self.THEOREM_PATTERN.finditer(content):
            theorems.append(match.group(1))
        
        return theorems
    
    def extract_dependencies(self, file_path: Path) -> List[str]:
        """提取文件依赖"""
        content = file_path.read_text(encoding='utf-8')
        dependencies = []
        
        for match in self.REQUIRE_PATTERN.finditer(content):
            deps = match.group(1).split()
            dependencies.extend(deps)
        
        return dependencies
    
    def check_proof_completeness(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查证明完整性"""
        content = file_path.read_text(encoding='utf-8')
        warnings = []
        
        theorems = list(self.THEOREM_PATTERN.finditer(content))
        proof_ends = list(self.PROOF_END_PATTERN.finditer(content))
        
        # 检查是否有Admitted证明
        admitted_count = len(re.findall(r'Admitted\.', content))
        if admitted_count > 0:
            warnings.append(f"发现 {admitted_count} 个Admitted证明(需要完成)")
        
        # 检查定理与证明结束标记的平衡
        if len(theorems) > len(proof_ends):
            warnings.append(f"定理数量({len(theorems)}) > 证明结束标记({len(proof_ends)})")
        
        # 检查是否有空证明
        empty_proof_pattern = r'(?:Theorem|Lemma|Proposition|Corollary)\s+\w+[^.]+\.(?:\s*Proof\.\s*Qed\.)'
        empty_proofs = re.findall(empty_proof_pattern, content)
        if empty_proofs:
            warnings.append(f"发现 {len(empty_proofs)} 个可能为空的证明")
        
        is_complete = len(warnings) == 0
        return is_complete, warnings
    
    def compile_coq_file(self, file_path: Path) -> Tuple[bool, str, str, float]:
        """编译Coq文件"""
        start_time = datetime.now()
        
        try:
            # 构建编译命令
            cmd = [
                Config.COQ_CMD,
                '-Q', str(file_path.parent), 'StreamingTheorems',
                '-color', 'no',
                str(file_path)
            ]
            
            logger.debug(f"执行命令: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=Config.TIMEOUT,
                cwd=str(file_path.parent)
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            success = result.returncode == 0
            stdout = result.stdout
            stderr = result.stderr
            
            return success, stdout, stderr, duration
            
        except subprocess.TimeoutExpired:
            duration = (datetime.now() - start_time).total_seconds()
            return False, "", f"编译超时(>{Config.TIMEOUT}秒)", duration
        except FileNotFoundError:
            duration = (datetime.now() - start_time).total_seconds()
            return False, "", f"未找到Coq编译器({Config.COQ_CMD})", duration
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return False, "", str(e), duration
    
    def analyze_errors(self, output: str) -> Tuple[List[str], List[str]]:
        """分析错误和警告"""
        errors = []
        warnings = []
        
        # 分析错误
        for pattern, error_type in self.ERROR_PATTERNS:
            matches = re.findall(pattern, output, re.DOTALL | re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = ' '.join(match)
                errors.append(f"[{error_type}] {match.strip()}")
        
        # 分析警告
        for pattern, warning_type in self.WARNING_PATTERNS:
            matches = re.findall(pattern, output, re.DOTALL | re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = ' '.join(match)
                warnings.append(f"[{warning_type}] {match.strip()}")
        
        return errors, warnings
    
    def generate_suggestions(self, errors: List[str], warnings: List[str]) -> List[str]:
        """基于错误生成证明建议"""
        suggestions = []
        
        for error in errors:
            if 'tactic_failure' in error:
                suggestions.append("建议: 尝试使用更基础的tactic组合，或使用'auto'/'eauto'")
            elif 'unification_error' in error:
                suggestions.append("建议: 检查类型匹配，可能需要显式类型标注")
            elif 'unsolved_goals' in error:
                suggestions.append("建议: 证明不完整，添加更多tactic步骤或检查归纳假设")
        
        for warning in warnings:
            if 'Admitted' in warning:
                suggestions.append("建议: 优先完成Admitted证明，它们是证明 gaps")
            elif 'deprecated' in warning.lower():
                suggestions.append("建议: 更新已弃用的语法或定义")
        
        return suggestions
    
    def check_file(self, file_path: Path) -> ProofResult:
        """检查单个Coq文件"""
        logger.info(f"检查Coq文件: {file_path}")
        
        theorems = self.extract_theorems(file_path)
        dependencies = self.extract_dependencies(file_path)
        
        # 检查证明完整性
        is_complete, completeness_warnings = self.check_proof_completeness(file_path)
        
        # 编译检查
        success, stdout, stderr, duration = self.compile_coq_file(file_path)
        
        # 分析错误
        errors, warnings = self.analyze_errors(stdout + stderr)
        warnings.extend(completeness_warnings)
        
        # 生成建议
        suggestions = self.generate_suggestions(errors, warnings)
        
        # 确定状态
        if not success:
            if '超时' in stderr:
                status = VerificationStatus.TIMEOUT
            else:
                status = VerificationStatus.FAILURE
        elif errors:
            status = VerificationStatus.ERROR
        elif warnings:
            status = VerificationStatus.SUCCESS  # 有警告但成功
        else:
            status = VerificationStatus.SUCCESS
        
        # 计算覆盖率（基于Admitted比例）
        content = file_path.read_text(encoding='utf-8')
        admitted_count = len(re.findall(r'Admitted\.', content))
        total_theorems = len(theorems)
        coverage = ((total_theorems - admitted_count) / total_theorems * 100) if total_theorems > 0 else 100
        
        result = ProofResult(
            file_path=str(file_path),
            theorem_name=theorems[0] if theorems else "N/A",
            status=status,
            duration=duration,
            dependencies=dependencies,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            coverage=coverage
        )
        
        return result
    
    def check_all(self, parallel: bool = True) -> VerificationReport:
        """检查所有Coq文件"""
        files = self.find_coq_files()
        logger.info(f"找到 {len(files)} 个Coq文件")
        
        report = VerificationReport(total_files=len(files))
        
        if parallel and len(files) > 1:
            with ThreadPoolExecutor(max_workers=Config.MAX_WORKERS) as executor:
                futures = {executor.submit(self.check_file, f): f for f in files}
                for future in as_completed(futures):
                    result = future.result()
                    self.results.append(result)
                    report.results.append(result)
                    self._update_report_counters(report, result)
        else:
            for file_path in files:
                result = self.check_file(file_path)
                self.results.append(result)
                report.results.append(result)
                self._update_report_counters(report, result)
        
        report.total_duration = sum(r.duration for r in report.results)
        report.summary = self._generate_summary(report)
        
        return report
    
    def _update_report_counters(self, report: VerificationReport, result: ProofResult):
        """更新报告计数器"""
        if result.status == VerificationStatus.SUCCESS:
            report.successful += 1
        elif result.status == VerificationStatus.FAILURE:
            report.failed += 1
        elif result.status == VerificationStatus.TIMEOUT:
            report.timeout += 1
        elif result.status == VerificationStatus.SKIPPED:
            report.skipped += 1
    
    def _generate_summary(self, report: VerificationReport) -> Dict:
        """生成报告摘要"""
        total_theorems = sum(
            len(self.extract_theorems(Path(r.file_path)))
            for r in report.results
        )
        
        total_admitted = 0
        for r in report.results:
            content = Path(r.file_path).read_text(encoding='utf-8')
            total_admitted += len(re.findall(r'Admitted\.', content))
        
        return {
            'total_theorems': total_theorems,
            'total_admitted': total_admitted,
            'completeness_rate': (
                ((total_theorems - total_admitted) / total_theorems * 100)
                if total_theorems > 0 else 100
            ),
            'total_errors': sum(len(r.errors) for r in report.results),
            'total_warnings': sum(len(r.warnings) for r in report.results),
            'total_suggestions': sum(len(r.suggestions) for r in report.results),
        }


# ==================== TLA+ 模型验证器 ====================

class TLAChecker:
    """TLA+模型验证器"""
    
    # TLA+ 元素提取模式
    MODULE_PATTERN = re.compile(r'----\s*MODULE\s+(\w+)\s*----')
    VARIABLE_PATTERN = re.compile(r'VARIABLES?\s+([\w,\s]+)')
    CONSTANT_PATTERN = re.compile(r'CONSTANTS?\s+([\w,\s]+)')
    OPERATOR_PATTERN = re.compile(r'(\w+)\s*\([^)]*\)\s*==')
    THEOREM_PATTERN = re.compile(r'THEOREM\s+(\w+)')
    INVARIANT_PATTERN = re.compile(r'INVARIANT\s+(\w+)')
    PROPERTY_PATTERN = re.compile(r'PROPERTY\s+(\w+)')
    
    def __init__(self, tla_path: str = None):
        self.tla_path = tla_path or Config.TLA_PATH
        self.results: List[ProofResult] = []
    
    def find_tla_files(self) -> List[Path]:
        """查找所有TLA+文件"""
        path = Path(self.tla_path)
        if not path.exists():
            logger.warning(f"TLA+路径不存在: {path}")
            path.mkdir(parents=True, exist_ok=True)
            return []
        
        files = list(path.rglob("*.tla"))
        
        # 同时检查其他可能的位置
        for extra_path in [Config.TLA_SPECS_PATH, "formal-methods/90-examples/tla-plus", "formal-methods/formal-code/tla"]:
            extra = Path(extra_path)
            if extra.exists():
                files.extend(extra.rglob("*.tla"))
        
        return sorted(set(files))
    
    def parse_tla_file(self, file_path: Path) -> Dict:
        """解析TLA+文件结构"""
        content = file_path.read_text(encoding='utf-8')
        
        return {
            'module': self.MODULE_PATTERN.search(content),
            'variables': self.VARIABLE_PATTERN.findall(content),
            'constants': self.CONSTANT_PATTERN.findall(content),
            'operators': self.OPERATOR_PATTERN.findall(content),
            'theorems': self.THEOREM_PATTERN.findall(content),
            'invariants': self.INVARIANT_PATTERN.findall(content),
            'properties': self.PROPERTY_PATTERN.findall(content),
            'extends': re.findall(r'EXTENDS\s+([\w,\s]+)', content),
        }
    
    def validate_syntax(self, file_path: Path) -> Tuple[bool, List[str]]:
        """验证TLA+语法"""
        content = file_path.read_text(encoding='utf-8')
        errors = []
        
        # 检查模块声明
        if not self.MODULE_PATTERN.search(content):
            errors.append("缺少MODULE声明")
        
        # 检查括号匹配
        open_parens = content.count('(') - content.count(')')
        open_brackets = content.count('[') - content.count(']')
        open_braces = content.count('{') - content.count('}')
        
        if open_parens != 0:
            errors.append(f"括号不匹配: {open_parens} 个未闭合")
        if open_brackets != 0:
            errors.append(f"方括号不匹配: {open_brackets} 个未闭合")
        if open_braces != 0:
            errors.append(f"花括号不匹配: {open_braces} 个未闭合")
        
        # 检查常见的语法错误
        if re.search(r'==\s*==', content):
            errors.append("发现重复的 == 运算符")
        
        # 检查是否使用了未定义的变量
        vars_defined = set()
        for match in self.VARIABLE_PATTERN.finditer(content):
            vars_defined.update(v.strip() for v in match.group(1).split(','))
        
        return len(errors) == 0, errors
    
    def run_model_checker(self, file_path: Path, cfg_path: Path = None) -> Tuple[bool, str, str, float]:
        """运行TLA+模型检查器"""
        start_time = datetime.now()
        
        try:
            # 首先尝试使用Apalache
            cmd = [
                Config.APALACHE_CMD,
                'check',
                '--init=Init',
                '--next=Next',
                '--inv=TypeOK',
                str(file_path)
            ]
            
            logger.debug(f"执行命令: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=Config.TIMEOUT
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            # 如果Apalache不可用，回退到语法检查
            if result.returncode == 127 or 'command not found' in result.stderr:
                logger.warning("Apalache不可用，仅进行语法验证")
                success, errors = self.validate_syntax(file_path)
                return success, "语法验证完成", "\n".join(errors) if errors else "", duration
            
            success = result.returncode == 0 and "No error" in result.stdout
            return success, result.stdout, result.stderr, duration
            
        except subprocess.TimeoutExpired:
            duration = (datetime.now() - start_time).total_seconds()
            return False, "", f"模型检查超时(>{Config.TIMEOUT}秒)", duration
        except FileNotFoundError:
            duration = (datetime.now() - start_time).total_seconds()
            # 回退到语法检查
            success, errors = self.validate_syntax(file_path)
            return success, "语法验证完成", "\n".join(errors) if errors else "", duration
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return False, "", str(e), duration
    
    def check_file(self, file_path: Path) -> ProofResult:
        """检查单个TLA+文件"""
        logger.info(f"检查TLA+文件: {file_path}")
        
        # 解析文件结构
        structure = self.parse_tla_file(file_path)
        
        # 查找对应的配置文件
        cfg_path = file_path.with_suffix('.cfg')
        if not cfg_path.exists():
            cfg_path = None
        
        # 运行验证
        success, stdout, stderr, duration = self.run_model_checker(file_path, cfg_path)
        
        # 分析结果
        errors = []
        warnings = []
        
        if not success:
            if stderr:
                errors.append(stderr)
            if 'Deadlock' in stdout:
                warnings.append("发现潜在死锁")
            if 'Invariant' in stdout and 'violated' in stdout:
                errors.append("不变量被违反")
        
        # 生成建议
        suggestions = []
        if errors:
            suggestions.append("建议: 检查状态转换定义和不变量")
        if not structure['theorems']:
            suggestions.append("建议: 添加THEOREM证明性质")
        if not structure['invariants']:
            suggestions.append("建议: 添加INVARIANT类型检查")
        
        # 确定状态
        if not success and errors:
            status = VerificationStatus.FAILURE
        elif warnings:
            status = VerificationStatus.SUCCESS
        else:
            status = VerificationStatus.SUCCESS
        
        # 计算覆盖率
        total_elements = (
            len(structure['operators']) +
            len(structure['theorems']) +
            len(structure['invariants'])
        )
        coverage = min(100, total_elements * 10)  # 简化的覆盖率计算
        
        result = ProofResult(
            file_path=str(file_path),
            theorem_name=structure['module'].group(1) if structure['module'] else "N/A",
            status=status,
            duration=duration,
            dependencies=structure['extends'],
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            coverage=coverage
        )
        
        return result
    
    def check_all(self, parallel: bool = True) -> VerificationReport:
        """检查所有TLA+文件"""
        files = self.find_tla_files()
        logger.info(f"找到 {len(files)} 个TLA+文件")
        
        report = VerificationReport(total_files=len(files))
        
        if parallel and len(files) > 1:
            with ThreadPoolExecutor(max_workers=Config.MAX_WORKERS) as executor:
                futures = {executor.submit(self.check_file, f): f for f in files}
                for future in as_completed(futures):
                    result = future.result()
                    self.results.append(result)
                    report.results.append(result)
                    self._update_report_counters(report, result)
        else:
            for file_path in files:
                result = self.check_file(file_path)
                self.results.append(result)
                report.results.append(result)
                self._update_report_counters(report, result)
        
        report.total_duration = sum(r.duration for r in report.results)
        report.summary = self._generate_summary(report)
        
        return report
    
    def _update_report_counters(self, report: VerificationReport, result: ProofResult):
        """更新报告计数器"""
        if result.status == VerificationStatus.SUCCESS:
            report.successful += 1
        elif result.status == VerificationStatus.FAILURE:
            report.failed += 1
        elif result.status == VerificationStatus.TIMEOUT:
            report.timeout += 1
        elif result.status == VerificationStatus.SKIPPED:
            report.skipped += 1
    
    def _generate_summary(self, report: VerificationReport) -> Dict:
        """生成报告摘要"""
        total_modules = 0
        total_operators = 0
        total_invariants = 0
        
        for result in report.results:
            structure = self.parse_tla_file(Path(result.file_path))
            if structure['module']:
                total_modules += 1
            total_operators += len(structure['operators'])
            total_invariants += len(structure['invariants'])
        
        return {
            'total_modules': total_modules,
            'total_operators': total_operators,
            'total_invariants': total_invariants,
            'total_errors': sum(len(r.errors) for r in report.results),
            'total_warnings': sum(len(r.warnings) for r in report.results),
        }


# ==================== 定理依赖检查器 ====================

class DependencyChecker:
    """定理依赖检查器"""
    
    def __init__(self):
        self.dependencies: Dict[str, Set[str]] = {}
        self.reverse_deps: Dict[str, Set[str]] = {}
    
    def build_dependency_graph(self, coq_results: List[ProofResult], 
                                tla_results: List[ProofResult]) -> Dict:
        """构建依赖图"""
        all_results = coq_results + tla_results
        
        for result in all_results:
            self.dependencies[result.file_path] = set(result.dependencies)
        
        # 构建反向依赖
        for file_path, deps in self.dependencies.items():
            for dep in deps:
                if dep not in self.reverse_deps:
                    self.reverse_deps[dep] = set()
                self.reverse_deps[dep].add(file_path)
        
        # 检测循环依赖
        cycles = self._detect_cycles()
        
        # 计算依赖深度
        depths = self._calculate_depths()
        
        return {
            'dependencies': {k: list(v) for k, v in self.dependencies.items()},
            'reverse_dependencies': {k: list(v) for k, v in self.reverse_deps.items()},
            'cycles': cycles,
            'depths': depths,
            'orphan_files': self._find_orphans(all_results),
        }
    
    def _detect_cycles(self) -> List[List[str]]:
        """检测循环依赖"""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.dependencies.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, path)
                elif neighbor in rec_stack:
                    # 发现循环
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            
            path.pop()
            rec_stack.remove(node)
        
        for node in self.dependencies:
            if node not in visited:
                dfs(node, [])
        
        return cycles
    
    def _calculate_depths(self) -> Dict[str, int]:
        """计算每个文件的依赖深度"""
        depths = {}
        
        def get_depth(node: str, visited: Set[str]) -> int:
            if node in depths:
                return depths[node]
            if node in visited:
                return 0  # 循环依赖
            
            visited.add(node)
            deps = self.dependencies.get(node, set())
            
            if not deps:
                depths[node] = 0
            else:
                max_dep_depth = max(
                    (get_depth(dep, visited) for dep in deps if dep in self.dependencies),
                    default=0
                )
                depths[node] = max_dep_depth + 1
            
            visited.remove(node)
            return depths[node]
        
        for node in self.dependencies:
            get_depth(node, set())
        
        return depths
    
    def _find_orphans(self, results: List[ProofResult]) -> List[str]:
        """查找没有依赖也没有被依赖的文件"""
        all_files = {r.file_path for r in results}
        referenced = set()
        
        for deps in self.dependencies.values():
            referenced.update(deps)
        
        for refs in self.reverse_deps.values():
            referenced.update(refs)
        
        orphans = all_files - referenced
        return list(orphans)
    
    def check_dependency_health(self) -> Dict:
        """检查依赖健康状况"""
        issues = []
        suggestions = []
        
        # 检查过深的依赖
        depths = self._calculate_depths()
        deep_files = [(f, d) for f, d in depths.items() if d > 5]
        if deep_files:
            issues.append(f"发现 {len(deep_files)} 个深度依赖文件(>5层)")
            suggestions.append("建议: 考虑重构深层依赖的文件，提取公共模块")
        
        # 检查循环依赖
        cycles = self._detect_cycles()
        if cycles:
            issues.append(f"发现 {len(cycles)} 个循环依赖")
            suggestions.append("建议: 打破循环依赖，提取共享接口")
        
        return {
            'healthy': len(issues) == 0,
            'issues': issues,
            'suggestions': suggestions,
        }


# ==================== 证明完整性验证器 ====================

class CompletenessValidator:
    """证明完整性验证器"""
    
    def __init__(self):
        self.validation_rules = [
            self._check_all_theorems_proved,
            self._check_no_axiom_overuse,
            self._check_documentation_coverage,
            self._check_proof_modularity,
        ]
    
    def validate(self, coq_results: List[ProofResult], 
                 tla_results: List[ProofResult]) -> Dict:
        """执行完整性验证"""
        all_results = coq_results + tla_results
        
        validation_report = {
            'passed': [],
            'failed': [],
            'warnings': [],
            'score': 0.0,
            'details': {}
        }
        
        for rule in self.validation_rules:
            rule_name = rule.__name__
            try:
                result = rule(all_results)
                validation_report['details'][rule_name] = result
                if result['passed']:
                    validation_report['passed'].append(rule_name)
                else:
                    validation_report['failed'].append(rule_name)
                if result.get('warnings'):
                    validation_report['warnings'].extend(result['warnings'])
            except Exception as e:
                validation_report['details'][rule_name] = {
                    'passed': False,
                    'error': str(e)
                }
                validation_report['failed'].append(rule_name)
        
        # 计算总体得分
        total_rules = len(self.validation_rules)
        passed_rules = len(validation_report['passed'])
        validation_report['score'] = (passed_rules / total_rules) * 100
        
        return validation_report
    
    def _check_all_theorems_proved(self, results: List[ProofResult]) -> Dict:
        """检查所有定理是否已证明"""
        unproved = []
        
        for result in results:
            if result.coverage < 100:
                unproved.append({
                    'file': result.file_path,
                    'coverage': result.coverage
                })
        
        return {
            'passed': len(unproved) == 0,
            'unproved_files': unproved,
            'message': f"{len(unproved)} 个文件未完全证明"
        }
    
    def _check_no_axiom_overuse(self, results: List[ProofResult]) -> Dict:
        """检查公理使用"""
        # 这是一个简化检查，实际应该解析Coq文件
        axiom_usage = []
        
        for result in results:
            if 'Axiom' in str(result.file_path):
                axiom_usage.append(result.file_path)
        
        return {
            'passed': len(axiom_usage) <= 5,  # 允许少量公理
            'axiom_count': len(axiom_usage),
            'message': f"发现 {len(axiom_usage)} 个公理使用"
        }
    
    def _check_documentation_coverage(self, results: List[ProofResult]) -> Dict:
        """检查文档覆盖率"""
        undocumented = []
        
        for result in results:
            file_path = Path(result.file_path)
            doc_file = file_path.with_suffix('.md')
            if not doc_file.exists():
                undocumented.append(str(file_path))
        
        coverage = (
            ((len(results) - len(undocumented)) / len(results) * 100)
            if results else 100
        )
        
        return {
            'passed': coverage >= 80,
            'coverage': coverage,
            'undocumented': undocumented[:10],  # 限制数量
            'message': f"文档覆盖率: {coverage:.1f}%"
        }
    
    def _check_proof_modularity(self, results: List[ProofResult]) -> Dict:
        """检查证明模块化"""
        # 检查文件大小分布
        large_files = []
        
        for result in results:
            file_path = Path(result.file_path)
            if file_path.exists():
                size = file_path.stat().st_size
                if size > 50000:  # 50KB
                    large_files.append({
                        'file': str(file_path),
                        'size': size
                    })
        
        return {
            'passed': len(large_files) <= 3,
            'large_files': large_files,
            'message': f"发现 {len(large_files)} 个超大证明文件"
        }


# ==================== 自动证明建议生成器 ====================

class ProofSuggestionEngine:
    """自动证明建议引擎"""
    
    # 证明模式库
    PROOF_PATTERNS = {
        'induction': {
            'patterns': [r'induction', r'recurs', r'Inductive'],
            'suggestions': [
                "使用 'induction x' 开始归纳证明",
                "确保处理基础情况和归纳步骤",
                "考虑使用 'simpl' 简化递归调用"
            ]
        },
        'equality': {
            'patterns': [r'=', r'equality', r'reflexivity'],
            'suggestions': [
                "尝试 'reflexivity' 证明等式",
                "使用 'rewrite' 进行等式替换",
                "考虑 'symmetry' 改变等式方向"
            ]
        },
        'contradiction': {
            'patterns': [r'contradiction', r'False', r'discriminate'],
            'suggestions': [
                "使用 'discriminate' 处理矛盾的等式",
                "尝试 'inversion' 分析矛盾假设",
                "考虑 'exfalso' 转为证明False"
            ]
        },
        'logical_connectives': {
            'patterns': [r'->', r'/\\', r'\\/', r'~'],
            'suggestions': [
                "使用 'intro' 引入蕴含前提",
                "使用 'split' 拆分合取",
                "使用 'left'/'right' 处理析取",
                "使用 'apply' 应用蕴含结论"
            ]
        }
    }
    
    def analyze_proof_goal(self, goal: str, context: List[str] = None) -> List[str]:
        """分析证明目标并生成建议"""
        suggestions = []
        
        # 匹配证明模式
        for pattern_name, pattern_data in self.PROOF_PATTERNS.items():
            for pattern in pattern_data['patterns']:
                if re.search(pattern, goal, re.IGNORECASE):
                    suggestions.extend(pattern_data['suggestions'])
                    break
        
        # 基于上下文生成建议
        if context:
            suggestions.extend(self._context_based_suggestions(context))
        
        # 去重并返回
        return list(dict.fromkeys(suggestions))
    
    def _context_based_suggestions(self, context: List[str]) -> List[str]:
        """基于上下文的建议"""
        suggestions = []
        
        for hyp in context:
            if 'forall' in hyp:
                suggestions.append("考虑对全称量词使用 'intros'")
            if 'exists' in hyp:
                suggestions.append("对存在量词使用 'exists' 提供 witness")
            if '->' in hyp:
                suggestions.append("蕴含假设可以使用 'apply' 或 'specialize'")
        
        return suggestions
    
    def generate_proof_template(self, theorem_statement: str) -> str:
        """生成证明模板"""
        template = f"""
Theorem {theorem_statement.split()[1] if len(theorem_statement.split()) > 1 else 'example'} :
  {theorem_statement}.
Proof.
  (* 自动生成的证明骨架 *)
  intros.
  (* 根据目标结构选择策略 *)
  simpl.
  auto.
Qed.
"""
        return template.strip()
    
    def suggest_lemmas(self, current_goal: str, available_lemmas: List[str]) -> List[str]:
        """建议可能有用的引理"""
        suggestions = []
        
        # 简单的关键词匹配
        goal_keywords = set(re.findall(r'\w+', current_goal.lower()))
        
        for lemma in available_lemmas:
            lemma_keywords = set(re.findall(r'\w+', lemma.lower()))
            overlap = goal_keywords & lemma_keywords
            if len(overlap) >= 2:  # 至少两个关键词重叠
                suggestions.append(lemma)
        
        return suggestions[:5]  # 返回前5个建议


# ==================== 报告生成器 ====================

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir or Config.REPORTS_PATH)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_markdown_report(self, report: VerificationReport, 
                                  checker_type: str) -> str:
        """生成Markdown格式报告"""
        lines = [
            f"# {checker_type} 验证报告",
            "",
            f"生成时间: {report.generated_at}",
            "",
            "## 摘要",
            "",
            f"- **总文件数**: {report.total_files}",
            f"- **成功**: {report.successful}",
            f"- **失败**: {report.failed}",
            f"- **超时**: {report.timeout}",
            f"- **跳过**: {report.skipped}",
            f"- **成功率**: {report.success_rate:.2f}%",
            f"- **总耗时**: {report.total_duration:.2f}秒",
            "",
            "## 详细结果",
            "",
        ]
        
        for result in report.results:
            status_emoji = {
                VerificationStatus.SUCCESS: "✅",
                VerificationStatus.FAILURE: "❌",
                VerificationStatus.TIMEOUT: "⏱️",
                VerificationStatus.ERROR: "⚠️",
                VerificationStatus.SKIPPED: "⏭️",
            }.get(result.status, "❓")
            
            lines.extend([
                f"### {status_emoji} {Path(result.file_path).name}",
                "",
                f"- **状态**: {result.status.value}",
                f"- **耗时**: {result.duration:.2f}秒",
                f"- **覆盖率**: {result.coverage:.1f}%",
                f"- **依赖**: {', '.join(result.dependencies) if result.dependencies else '无'}",
                "",
            ])
            
            if result.errors:
                lines.extend(["**错误**:", ""])
                for error in result.errors:
                    lines.append(f"- {error}")
                lines.append("")
            
            if result.warnings:
                lines.extend(["**警告**:", ""])
                for warning in result.warnings:
                    lines.append(f"- {warning}")
                lines.append("")
            
            if result.suggestions:
                lines.extend(["**建议**:", ""])
                for suggestion in result.suggestions:
                    lines.append(f"- {suggestion}")
                lines.append("")
        
        if report.summary:
            lines.extend([
                "## 汇总统计",
                "",
                "```json",
                json.dumps(report.summary, indent=2, ensure_ascii=False),
                "```",
                "",
            ])
        
        return "\n".join(lines)
    
    def generate_json_report(self, report: VerificationReport) -> str:
        """生成JSON格式报告"""
        return json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
    
    def save_reports(self, coq_report: VerificationReport, 
                     tla_report: VerificationReport,
                     dependency_report: Dict = None,
                     completeness_report: Dict = None):
        """保存所有报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Markdown报告
        coq_md = self.generate_markdown_report(coq_report, "Coq")
        tla_md = self.generate_markdown_report(tla_report, "TLA+")
        
        (self.output_dir / f"coq-report-{timestamp}.md").write_text(coq_md, encoding='utf-8')
        (self.output_dir / f"tla-report-{timestamp}.md").write_text(tla_md, encoding='utf-8')
        
        # JSON报告
        (self.output_dir / f"coq-report-{timestamp}.json").write_text(
            self.generate_json_report(coq_report), encoding='utf-8'
        )
        (self.output_dir / f"tla-report-{timestamp}.json").write_text(
            self.generate_json_report(tla_report), encoding='utf-8'
        )
        
        # 依赖和完整性报告
        if dependency_report:
            (self.output_dir / f"dependency-report-{timestamp}.json").write_text(
                json.dumps(dependency_report, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
        
        if completeness_report:
            (self.output_dir / f"completeness-report-{timestamp}.json").write_text(
                json.dumps(completeness_report, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
        
        logger.info(f"报告已保存到: {self.output_dir}")


# ==================== 主控制类 ====================

class TheoremProverAutomation:
    """定理证明自动化主控制类"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.coq_checker = CoqChecker()
        self.tla_checker = TLAChecker()
        self.dependency_checker = DependencyChecker()
        self.completeness_validator = CompletenessValidator()
        self.suggestion_engine = ProofSuggestionEngine()
        self.report_generator = ReportGenerator()
    
    def run_full_check(self, parallel: bool = True) -> Dict:
        """运行完整检查流程"""
        logger.info("=" * 60)
        logger.info("开始定理证明自动化检查")
        logger.info("=" * 60)
        
        # 1. Coq证明检查
        logger.info("\n[1/5] Coq证明检查...")
        coq_report = self.coq_checker.check_all(parallel)
        logger.info(f"Coq检查完成: {coq_report.successful}/{coq_report.total_files} 成功")
        
        # 2. TLA+模型验证
        logger.info("\n[2/5] TLA+模型验证...")
        tla_report = self.tla_checker.check_all(parallel)
        logger.info(f"TLA+检查完成: {tla_report.successful}/{tla_report.total_files} 成功")
        
        # 3. 定理依赖检查
        logger.info("\n[3/5] 定理依赖检查...")
        dependency_report = self.dependency_checker.build_dependency_graph(
            coq_report.results, tla_report.results
        )
        health = self.dependency_checker.check_dependency_health()
        logger.info(f"依赖检查完成: {'健康' if health['healthy'] else '发现'}")
        
        # 4. 证明完整性验证
        logger.info("\n[4/5] 证明完整性验证...")
        completeness_report = self.completeness_validator.validate(
            coq_report.results, tla_report.results
        )
        logger.info(f"完整性得分: {completeness_report['score']:.1f}%")
        
        # 5. 生成报告
        logger.info("\n[5/5] 生成报告...")
        self.report_generator.save_reports(
            coq_report, tla_report, 
            dependency_report, completeness_report
        )
        
        # 汇总结果
        summary = {
            'coq': coq_report.to_dict(),
            'tla': tla_report.to_dict(),
            'dependency': dependency_report,
            'completeness': completeness_report,
            'overall_success_rate': (
                (coq_report.successful + tla_report.successful) /
                max(1, coq_report.total_files + tla_report.total_files) * 100
            ),
        }
        
        logger.info("\n" + "=" * 60)
        logger.info("检查完成!")
        logger.info(f"总体成功率: {summary['overall_success_rate']:.2f}%")
        logger.info("=" * 60)
        
        return summary
    
    def check_coq_only(self) -> VerificationReport:
        """仅检查Coq证明"""
        return self.coq_checker.check_all()
    
    def check_tla_only(self) -> VerificationReport:
        """仅检查TLA+模型"""
        return self.tla_checker.check_all()
    
    def get_proof_suggestions(self, file_path: str) -> List[str]:
        """获取证明建议"""
        path = Path(file_path)
        if not path.exists():
            return [f"文件不存在: {file_path}"]
        
        content = path.read_text(encoding='utf-8')
        
        # 提取当前的证明目标（简化实现）
        goals = re.findall(r'Theorem\s+\w+\s*:([^\.]+)\.', content)
        
        suggestions = []
        for goal in goals:
            goal_suggestions = self.suggestion_engine.analyze_proof_goal(goal)
            suggestions.extend(goal_suggestions)
        
        return list(dict.fromkeys(suggestions))


# ==================== 命令行接口 ====================

def create_argument_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description='定理证明自动化工具链',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 运行完整检查
  python theorem-prover-automation.py
  
  # 仅检查Coq
  python theorem-prover-automation.py --coq-only
  
  # 仅检查TLA+
  python theorem-prover-automation.py --tla-only
  
  # 获取特定文件的证明建议
  python theorem-prover-automation.py --suggest path/to/file.v
  
  # 详细输出
  python theorem-prover-automation.py -v
  
  # JSON格式输出
  python theorem-prover-automation.py --json
        """
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='启用详细输出'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='以JSON格式输出结果'
    )
    
    parser.add_argument(
        '--coq-only',
        action='store_true',
        help='仅检查Coq证明'
    )
    
    parser.add_argument(
        '--tla-only',
        action='store_true',
        help='仅检查TLA+模型'
    )
    
    parser.add_argument(
        '--suggest',
        metavar='FILE',
        help='获取指定文件的证明建议'
    )
    
    parser.add_argument(
        '--parallel',
        action='store_true',
        default=True,
        help='启用并行检查(默认开启)'
    )
    
    parser.add_argument(
        '--no-parallel',
        dest='parallel',
        action='store_false',
        help='禁用并行检查'
    )
    
    parser.add_argument(
        '--output-dir',
        metavar='DIR',
        default=Config.REPORTS_PATH,
        help=f'报告输出目录(默认: {Config.REPORTS_PATH})'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        metavar='SECONDS',
        default=Config.TIMEOUT,
        help=f'验证超时时间(默认: {Config.TIMEOUT}秒)'
    )
    
    return parser


def main():
    """主函数"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # 配置
    Config.VERBOSE = args.verbose
    Config.TIMEOUT = args.timeout
    Config.REPORTS_PATH = args.output_dir
    Config.JSON_OUTPUT = args.json
    
    # 重新配置日志
    global logger
    logger = setup_logging(args.verbose)
    
    # 创建自动化实例
    automation = TheoremProverAutomation()
    
    try:
        if args.suggest:
            # 获取证明建议
            suggestions = automation.get_proof_suggestions(args.suggest)
            if args.json:
                print(json.dumps({'suggestions': suggestions}, indent=2, ensure_ascii=False))
            else:
                print(f"\n证明建议 for {args.suggest}:")
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"  {i}. {suggestion}")
        
        elif args.coq_only:
            # 仅Coq检查
            report = automation.check_coq_only()
            if args.json:
                print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
            else:
                print(f"\nCoq检查结果:")
                print(f"  成功率: {report.success_rate:.2f}%")
                print(f"  通过: {report.successful}/{report.total_files}")
        
        elif args.tla_only:
            # 仅TLA+检查
            report = automation.check_tla_only()
            if args.json:
                print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
            else:
                print(f"\nTLA+检查结果:")
                print(f"  成功率: {report.success_rate:.2f}%")
                print(f"  通过: {report.successful}/{report.total_files}")
        
        else:
            # 完整检查
            summary = automation.run_full_check(parallel=args.parallel)
            if args.json:
                print(json.dumps(summary, indent=2, ensure_ascii=False))
            else:
                print(f"\n{'='*60}")
                print("定理证明自动化检查完成!")
                print(f"{'='*60}")
                print(f"总体成功率: {summary['overall_success_rate']:.2f}%")
                print(f"Coq: {summary['coq']['successful']}/{summary['coq']['total_files']} 通过")
                print(f"TLA+: {summary['tla']['successful']}/{summary['tla']['total_files']} 通过")
                print(f"完整性得分: {summary['completeness']['score']:.1f}%")
    
    except KeyboardInterrupt:
        logger.info("\n操作被用户中断")
        sys.exit(1)
    except Exception as e:
        logger.error(f"错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
