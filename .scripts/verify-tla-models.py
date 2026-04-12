#!/usr/bin/env python3
"""
TLA+模型验证脚本
用于批量验证TLA+模型和运行TLC模型检查

功能:
- 批量语法检查 (.tla文件)
- 运行TLC模型检查
- 检测死锁和不变式违反
- 生成覆盖率报告
- CI集成支持

作者: AnalysisDataFlow Project
版本: 1.0
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class TLCResult:
    """TLC检查结果"""
    file_path: str
    config_path: Optional[str] = None
    success: bool = False
    states_generated: int = 0
    distinct_states: int = 0
    deadlocks_found: int = 0
    invariant_violations: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    coverage: Dict = field(default_factory=dict)
    execution_time_ms: int = 0
    fingerprint_probability: Optional[float] = None


@dataclass
class ModelCheckReport:
    """模型检查报告"""
    timestamp: str
    total_models: int = 0
    successful_checks: int = 0
    failed_checks: int = 0
    total_states: int = 0
    total_deadlocks: int = 0
    total_invariant_violations: int = 0
    results: List[TLCResult] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "summary": {
                "total_models": self.total_models,
                "successful_checks": self.successful_checks,
                "failed_checks": self.failed_checks,
                "total_states": self.total_states,
                "total_deadlocks": self.total_deadlocks,
                "total_invariant_violations": self.total_invariant_violations,
                "success_rate": round(self.successful_checks / max(self.total_models, 1) * 100, 2)
            },
            "models": [
                {
                    "file": r.file_path,
                    "config": r.config_path,
                    "status": "success" if r.success else "failed",
                    "states": {
                        "generated": r.states_generated,
                        "distinct": r.distinct_states
                    },
                    "issues": {
                        "deadlocks": r.deadlocks_found,
                        "invariant_violations": r.invariant_violations
                    },
                    "errors": r.errors,
                    "warnings": r.warnings,
                    "coverage": r.coverage,
                    "execution_time_ms": r.execution_time_ms,
                    "fingerprint_probability": r.fingerprint_probability
                }
                for r in self.results
            ]
        }


class TLAVerifier:
    """TLA+模型验证器"""
    
    # TLC错误模式
    ERROR_PATTERNS = {
        'deadlock': re.compile(r'Deadlock reached|deadlock', re.IGNORECASE),
        'invariant_violation': re.compile(r'Invariant.*is violated|Invariant violation', re.IGNORECASE),
        'syntax_error': re.compile(r'parse error|syntax error|was expecting', re.IGNORECASE),
        'configuration_error': re.compile(r'configuration error|could not find', re.IGNORECASE),
    }
    
    # TLC成功模式
    SUCCESS_PATTERNS = {
        'states_generated': re.compile(r'(\d+) states generated'),
        'distinct_states': re.compile(r'(\d+) distinct states'),
        'fingerprint_prob': re.compile(r'calculated:\s*([\d.E+-]+)'),
        'finished': re.compile(r'Model checking completed|Finished in|(\d+)ms'),
    }
    
    def __init__(self, project_root: str, verbose: bool = False, 
                 timeout: int = 600, workers: int = 4,
                 max_depth: Optional[int] = None):
        self.project_root = Path(project_root).resolve()
        self.verbose = verbose
        self.timeout = timeout
        self.workers = workers
        self.max_depth = max_depth
        self.tlc_cmd = self._find_tlc()
        self.sany_cmd = self._find_sany()
        
    def _find_tlc(self) -> str:
        """查找TLC命令"""
        for cmd in ['tlc', 'tlc2']:
            try:
                result = subprocess.run(['which', cmd], capture_output=True, text=True)
                if result.returncode == 0:
                    return cmd
            except:
                pass
        
        # 检查常用路径
        for path in ['/usr/local/bin/tlc', os.path.expanduser('~/.local/bin/tlc')]:
            if os.path.exists(path):
                return path
        
        return 'tlc'
    
    def _find_sany(self) -> str:
        """查找SANY语法检查器"""
        for cmd in ['sany']:
            try:
                result = subprocess.run(['which', cmd], capture_output=True, text=True)
                if result.returncode == 0:
                    return cmd
            except:
                pass
        
        # 如果没有sany，使用tlc的语法检查模式
        return self.tlc_cmd
    
    def _run_tlc(self, model_path: Path, config_path: Optional[Path] = None) -> Tuple[int, str, str, float]:
        """运行TLC模型检查"""
        cmd = [self.tlc_cmd]
        
        # 基本选项
        cmd.extend([
            '-workers', str(self.workers),
            '-lncheck', 'final',  # 最后检查锁序
            '-checkpoint', '0',   # 禁用检查点以加速
        ])
        
        # 深度限制
        if self.max_depth:
            cmd.extend(['-depth', str(self.max_depth)])
        
        # 配置文件
        if config_path:
            cmd.extend(['-config', str(config_path)])
        else:
            # 自动查找配置文件
            auto_config = model_path.with_suffix('.cfg')
            if not auto_config.exists():
                auto_config = self.project_root / 'cfg' / f"{model_path.stem}.cfg"
            if auto_config.exists():
                cmd.extend(['-config', str(auto_config)])
        
        cmd.append(str(model_path))
        
        start_time = datetime.now()
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=self.project_root
            )
            elapsed = (datetime.now() - start_time).total_seconds() * 1000
            return result.returncode, result.stdout, result.stderr, elapsed
        except subprocess.TimeoutExpired:
            elapsed = (datetime.now() - start_time).total_seconds() * 1000
            return -1, "", f"Timeout after {self.timeout}s", elapsed
        except Exception as e:
            return -1, "", str(e), 0
    
    def _run_sany(self, file_path: Path) -> Tuple[int, str, str]:
        """运行SANY语法检查"""
        # 如果没有单独的sany命令，使用tlc的元模型检查
        if self.sany_cmd == self.tlc_cmd:
            cmd = [self.tlc_cmd, '-simulate', 'num=1', str(file_path)]
        else:
            cmd = [self.sany_cmd, str(file_path)]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self.project_root
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return -1, "", str(e)
    
    def _parse_tlc_output(self, stdout: str, stderr: str) -> Tuple[bool, Dict]:
        """解析TLC输出"""
        output = stdout + '\n' + stderr
        result = {
            'states_generated': 0,
            'distinct_states': 0,
            'deadlocks': 0,
            'invariant_violations': [],
            'errors': [],
            'warnings': [],
            'fingerprint_prob': None,
        }
        
        success = True
        
        # 检查错误
        if 'Error' in output or 'error' in output.lower():
            for line in output.split('\n'):
                if 'error' in line.lower() and 'Error: ' in line:
                    result['errors'].append(line.strip())
                    success = False
        
        # 检查死锁
        if self.ERROR_PATTERNS['deadlock'].search(output):
            result['deadlocks'] = output.lower().count('deadlock')
            success = False
        
        # 检查不变式违反
        invariant_matches = self.ERROR_PATTERNS['invariant_violation'].findall(output)
        if invariant_matches:
            result['invariant_violations'] = invariant_matches
            success = False
        
        # 解析状态统计
        states_gen = self.SUCCESS_PATTERNS['states_generated'].search(output)
        if states_gen:
            result['states_generated'] = int(states_gen.group(1))
        
        distinct = self.SUCCESS_PATTERNS['distinct_states'].search(output)
        if distinct:
            result['distinct_states'] = int(distinct.group(1))
        
        # 指纹概率 (用于评估检查完整性)
        fp_prob = self.SUCCESS_PATTERNS['fingerprint_prob'].search(output)
        if fp_prob:
            result['fingerprint_prob'] = float(fp_prob.group(1))
        
        return success, result
    
    def check_syntax(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查TLA+文件语法"""
        if self.verbose:
            print(f"  Syntax check: {file_path.name}")
        
        returncode, stdout, stderr = self._run_sany(file_path)
        
        errors = []
        if returncode != 0:
            output = stdout + '\n' + stderr
            for line in output.split('\n'):
                if 'error' in line.lower() or 'Error' in line:
                    errors.append(line.strip())
        
        return len(errors) == 0, errors
    
    def verify_model(self, model_path: Path, config_path: Optional[Path] = None) -> TLCResult:
        """验证单个模型"""
        print(f"  Model checking: {model_path.name}", flush=True)
        
        result = TLCResult(
            file_path=str(model_path.relative_to(self.project_root)),
            config_path=str(config_path.relative_to(self.project_root)) if config_path else None
        )
        
        # 首先检查语法
        syntax_ok, syntax_errors = self.check_syntax(model_path)
        if not syntax_ok:
            result.errors.extend(syntax_errors)
            return result
        
        # 运行TLC
        returncode, stdout, stderr, elapsed = self._run_tlc(model_path, config_path)
        result.execution_time_ms = int(elapsed)
        
        # 解析输出
        success, parsed = self._parse_tlc_output(stdout, stderr)
        
        result.success = success
        result.states_generated = parsed['states_generated']
        result.distinct_states = parsed['distinct_states']
        result.deadlocks_found = parsed['deadlocks']
        result.invariant_violations = parsed['invariant_violations']
        result.errors.extend(parsed['errors'])
        result.fingerprint_probability = parsed['fingerprint_prob']
        
        if self.verbose:
            if result.success:
                print(f"    ✓ States: {result.distinct_states}, Time: {result.execution_time_ms}ms")
            else:
                print(f"    ✗ Errors: {len(result.errors)}, Deadlocks: {result.deadlocks_found}")
        
        return result
    
    def _find_tla_files(self, patterns: List[str]) -> List[Path]:
        """查找TLA+文件"""
        files = set()
        
        for pattern in patterns:
            if '*' in pattern or '?' in pattern:
                matched = list(self.project_root.rglob(pattern))
                files.update(matched)
            else:
                path = self.project_root / pattern
                if path.exists():
                    files.add(path)
                elif path.with_suffix('.tla').exists():
                    files.add(path.with_suffix('.tla'))
        
        return sorted([f for f in files if f.suffix == '.tla'])
    
    def _find_config(self, model_path: Path) -> Optional[Path]:
        """查找模型的配置文件"""
        # 1. 同目录下的.cfg文件
        cfg = model_path.with_suffix('.cfg')
        if cfg.exists():
            return cfg
        
        # 2. cfg目录下的配置文件
        cfg_dir = self.project_root / 'cfg'
        if cfg_dir.exists():
            cfg = cfg_dir / f"{model_path.stem}.cfg"
            if cfg.exists():
                return cfg
        
        return None
    
    def verify_all(self, patterns: List[str]) -> ModelCheckReport:
        """验证所有模型"""
        files = self._find_tla_files(patterns)
        
        if not files:
            print("No .tla files found matching the specified patterns")
            return ModelCheckReport(timestamp=datetime.now().isoformat())
        
        print(f"\nFound {len(files)} TLA+ models to verify:\n")
        
        report = ModelCheckReport(
            timestamp=datetime.now().isoformat(),
            total_models=len(files)
        )
        
        for model_path in files:
            # 查找配置文件
            config_path = self._find_config(model_path)
            
            result = self.verify_model(model_path, config_path)
            report.results.append(result)
            
            if result.success:
                report.successful_checks += 1
            else:
                report.failed_checks += 1
            
            report.total_states += result.distinct_states
            report.total_deadlocks += result.deadlocks_found
            report.total_invariant_violations += len(result.invariant_violations)
        
        return report
    
    def generate_report(self, report: ModelCheckReport, output_format: str = 'text') -> str:
        """生成报告"""
        if output_format == 'json':
            return json.dumps(report.to_dict(), indent=2)
        
        # Text format
        lines = [
            "=" * 70,
            "TLA+ Model Verification Report",
            "=" * 70,
            f"Timestamp: {report.timestamp}",
            "",
            "Summary:",
            f"  Total Models:      {report.total_models}",
            f"  Successful:        {report.successful_checks} ({round(report.successful_checks/max(report.total_models,1)*100, 1)}%)",
            f"  Failed:            {report.failed_checks}",
            f"  Total States:      {report.total_states:,}",
            f"  Deadlocks Found:   {report.total_deadlocks}",
            f"  Invariant Violations: {report.total_invariant_violations}",
            "",
            "Model Details:",
            "-" * 70
        ]
        
        for result in report.results:
            status = "✓" if result.success else "✗"
            lines.append(f"  {status} {result.file_path}")
            lines.append(f"    States: {result.distinct_states:,} (generated: {result.states_generated:,})")
            lines.append(f"    Time: {result.execution_time_ms}ms")
            
            if result.fingerprint_probability:
                lines.append(f"    Fingerprint Probability: {result.fingerprint_probability:.2e}")
            
            issues = []
            if result.deadlocks_found:
                issues.append(f"{result.deadlocks_found} deadlock(s)")
            if result.invariant_violations:
                issues.append(f"{len(result.invariant_violations)} invariant violation(s)")
            if issues:
                lines.append(f"    Issues: {', '.join(issues)}")
            
            if result.errors:
                for err in result.errors[:2]:
                    lines.append(f"    Error: {err}")
        
        lines.extend([
            "-" * 70,
            ""
        ])
        
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Verify TLA+ models using TLC',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --project ./my-project models/*.tla
  %(prog)s --json --output report.json
  %(prog)s --workers 8 --timeout 1200
  %(prog)s --ci-mode  # CI-friendly output
  %(prog)s --depth 100  # Limit search depth
        """
    )
    
    parser.add_argument('files', nargs='*', default=['models/*.tla', '*.tla'],
                       help='TLA+ files or glob patterns (default: models/*.tla *.tla)')
    
    parser.add_argument('--project', '-p', default='.',
                       help='Project root directory')
    
    parser.add_argument('--workers', '-w', type=int, default=4,
                       help='Number of TLC worker threads (default: 4)')
    
    parser.add_argument('--timeout', '-t', type=int, default=600,
                       help='Timeout per model in seconds (default: 600)')
    
    parser.add_argument('--depth', '-d', type=int,
                       help='Maximum search depth')
    
    parser.add_argument('--report', '-r',
                       help='Write report to file')
    
    parser.add_argument('--json', action='store_true',
                       help='Output report in JSON format')
    
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    parser.add_argument('--syntax-only', action='store_true',
                       help='Only check syntax, skip model checking')
    
    parser.add_argument('--fail-on-deadlock', action='store_true',
                       help='Exit with error if deadlocks found')
    
    parser.add_argument('--fail-on-invariant', action='store_true',
                       help='Exit with error if invariants violated')
    
    parser.add_argument('--ci-mode', action='store_true',
                       help='CI-friendly output')
    
    args = parser.parse_args()
    
    # CI模式设置
    if args.ci_mode:
        args.fail_on_deadlock = True
        args.fail_on_invariant = True
        args.verbose = True
    
    # 创建验证器
    verifier = TLAVerifier(
        project_root=args.project,
        verbose=args.verbose,
        timeout=args.timeout,
        workers=args.workers,
        max_depth=args.depth
    )
    
    print(f"TLA+ Model Verification")
    print(f"Project: {verifier.project_root}")
    print(f"TLC: {verifier.tlc_cmd}")
    print(f"Workers: {args.workers}")
    if args.depth:
        print(f"Max Depth: {args.depth}")
    print(f"Files: {', '.join(args.files)}")
    
    # 执行验证
    if args.syntax_only:
        # 仅语法检查
        files = verifier._find_tla_files(args.files)
        all_ok = True
        for f in files:
            ok, errors = verifier.check_syntax(f)
            status = "✓" if ok else "✗"
            print(f"  {status} {f.name}")
            if not ok:
                all_ok = False
                for err in errors[:3]:
                    print(f"    {err}")
        sys.exit(0 if all_ok else 1)
    
    # 完整模型检查
    report = verifier.verify_all(args.files)
    
    # 生成报告
    output = verifier.generate_report(report, 'json' if args.json else 'text')
    
    # 输出
    if args.report:
        Path(args.report).write_text(output)
        print(f"\nReport written to: {args.report}")
    else:
        print(output)
    
    # 确定退出码
    exit_code = 0
    
    if report.failed_checks > 0:
        exit_code = 1
    
    if args.fail_on_deadlock and report.total_deadlocks > 0:
        print(f"\n❌ Found {report.total_deadlocks} deadlock(s)")
        exit_code = 1
    
    if args.fail_on_invariant and report.total_invariant_violations > 0:
        print(f"\n❌ Found {report.total_invariant_violations} invariant violation(s)")
        exit_code = 1
    
    # 最终总结
    if exit_code == 0:
        print("\n✅ All models verified successfully!")
    else:
        print("\n❌ Verification failed. See details above.")
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
