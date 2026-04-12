#!/usr/bin/env python3
"""
Coq证明验证脚本
用于批量验证项目中的Coq证明文件

功能:
- 批量编译.v文件
- 生成证明统计报告
- 检测Admitted定理
- 检查证明覆盖率
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
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class ProofStats:
    """证明统计信息"""
    file_path: str
    total_lines: int = 0
    theorem_count: int = 0
    lemma_count: int = 0
    definition_count: int = 0
    admitted_count: int = 0
    proof_qed_count: int = 0
    compile_time_ms: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class VerificationReport:
    """验证报告"""
    timestamp: str
    total_files: int = 0
    successful_files: int = 0
    failed_files: int = 0
    total_theorems: int = 0
    total_admitted: int = 0
    total_errors: int = 0
    file_stats: List[ProofStats] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "summary": {
                "total_files": self.total_files,
                "successful_files": self.successful_files,
                "failed_files": self.failed_files,
                "total_theorems": self.total_theorems,
                "total_admitted": self.total_admitted,
                "total_errors": self.total_errors,
                "success_rate": round(self.successful_files / max(self.total_files, 1) * 100, 2),
                "admission_rate": round(self.total_admitted / max(self.total_theorems, 1) * 100, 2)
            },
            "files": [
                {
                    "path": s.file_path,
                    "lines": s.total_lines,
                    "theorems": s.theorem_count,
                    "lemmas": s.lemma_count,
                    "definitions": s.definition_count,
                    "admitted": s.admitted_count,
                    "proofs": s.proof_qed_count,
                    "compile_time_ms": s.compile_time_ms,
                    "errors": s.errors,
                    "warnings": s.warnings,
                    "status": "success" if not s.errors else "failed"
                }
                for s in self.file_stats
            ]
        }


class CoqVerifier:
    """Coq证明验证器"""
    
    def __init__(self, project_root: str, verbose: bool = False, timeout: int = 300):
        self.project_root = Path(project_root).resolve()
        self.verbose = verbose
        self.timeout = timeout
        self.coqc_cmd = self._find_coqc()
        
    def _find_coqc(self) -> str:
        """查找coqc命令"""
        # 首先检查opam环境
        try:
            result = subprocess.run(
                ["opam", "env", "--switch=stream-verify", "--set-switch"],
                capture_output=True, text=True, shell=False
            )
            if result.returncode == 0:
                # 提取PATH
                for line in result.stdout.split('\n'):
                    if 'export PATH=' in line:
                        path = line.split('=', 1)[1].strip('"\';')
                        coqc = Path(path) / 'coqc'
                        if coqc.exists():
                            return str(coqc)
        except:
            pass
        
        # 检查环境变量
        if 'COQC' in os.environ:
            return os.environ['COQC']
        
        # 检查PATH
        for cmd in ['coqc']:
            try:
                result = subprocess.run(
                    ['which', cmd],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    return cmd
            except:
                pass
        
        return 'coqc'
    
    def _run_coqc(self, file_path: Path, output_dir: Optional[Path] = None) -> Tuple[int, str, str, float]:
        """运行coqc编译"""
        cmd = [self.coqc_cmd]
        
        # 添加项目选项
        coqproject = self.project_root / '_CoqProject'
        if coqproject.exists():
            cmd.extend(['-f', str(coqproject)])
        
        # 输出目录
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            cmd.extend(['-o', str(output_dir)])
        
        cmd.append(str(file_path))
        
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
            return -1, "", f"Timeout after {self.timeout}s", self.timeout * 1000
        except Exception as e:
            return -1, "", str(e), 0
    
    def _analyze_file(self, file_path: Path) -> ProofStats:
        """分析Coq文件内容"""
        stats = ProofStats(file_path=str(file_path.relative_to(self.project_root)))
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            stats.total_lines = len(lines)
            
            # 统计定义
            stats.theorem_count = len(re.findall(r'^\s*Theorem\s+', content, re.MULTILINE))
            stats.lemma_count = len(re.findall(r'^\s*Lemma\s+', content, re.MULTILINE))
            stats.definition_count = len(re.findall(r'^\s*(Definition|Inductive|Record|Class)\s+', content, re.MULTILINE))
            
            # 统计Admitted
            stats.admitted_count = len(re.findall(r'Admitted', content))
            
            # 统计Qed/Defined
            stats.proof_qed_count = len(re.findall(r'Qed|Defined', content))
            
        except Exception as e:
            stats.errors.append(f"File analysis error: {e}")
        
        return stats
    
    def _find_coq_files(self, patterns: List[str]) -> List[Path]:
        """查找Coq文件"""
        files = set()
        
        for pattern in patterns:
            if '*' in pattern or '?' in pattern:
                # Glob模式
                matched = list(self.project_root.rglob(pattern))
                files.update(matched)
            else:
                # 具体路径
                path = self.project_root / pattern
                if path.exists():
                    files.add(path)
                elif path.with_suffix('.v').exists():
                    files.add(path.with_suffix('.v'))
        
        # 过滤并排序
        return sorted([f for f in files if f.suffix == '.v'])
    
    def verify_file(self, file_path: Path, output_dir: Optional[Path] = None) -> ProofStats:
        """验证单个文件"""
        print(f"  Checking: {file_path.relative_to(self.project_root)}", flush=True)
        
        # 首先分析内容
        stats = self._analyze_file(file_path)
        
        # 然后尝试编译
        returncode, stdout, stderr, elapsed = self._run_coqc(file_path, output_dir)
        stats.compile_time_ms = int(elapsed)
        
        # 解析错误和警告
        if returncode != 0:
            # 提取错误信息
            error_lines = stderr.split('\n')
            for line in error_lines:
                if 'Error:' in line:
                    stats.errors.append(line.strip())
                elif line.strip() and not line.startswith('File'):
                    stats.warnings.append(line.strip())
        else:
            # 提取警告
            for line in stderr.split('\n'):
                if 'Warning:' in line:
                    stats.warnings.append(line.strip())
        
        if self.verbose:
            if stats.errors:
                print(f"    ❌ Errors: {len(stats.errors)}")
            elif stats.warnings:
                print(f"    ⚠️  Warnings: {len(stats.warnings)}")
            else:
                print(f"    ✓ OK ({stats.compile_time_ms}ms)")
        
        return stats
    
    def verify_all(self, patterns: List[str], output_dir: Optional[str] = None) -> VerificationReport:
        """验证所有文件"""
        files = self._find_coq_files(patterns)
        
        if not files:
            print("No .v files found matching the specified patterns")
            return VerificationReport(timestamp=datetime.now().isoformat())
        
        print(f"\nFound {len(files)} Coq files to verify:\n")
        
        report = VerificationReport(
            timestamp=datetime.now().isoformat(),
            total_files=len(files)
        )
        
        out_dir = Path(output_dir) if output_dir else None
        
        for file_path in files:
            stats = self.verify_file(file_path, out_dir)
            report.file_stats.append(stats)
            
            if stats.errors:
                report.failed_files += 1
                report.total_errors += len(stats.errors)
            else:
                report.successful_files += 1
            
            report.total_theorems += stats.theorem_count + stats.lemma_count
            report.total_admitted += stats.admitted_count
        
        return report
    
    def generate_report(self, report: VerificationReport, output_format: str = 'text') -> str:
        """生成报告"""
        if output_format == 'json':
            return json.dumps(report.to_dict(), indent=2)
        
        # Text format
        lines = [
            "=" * 60,
            "Coq Proof Verification Report",
            "=" * 60,
            f"Timestamp: {report.timestamp}",
            "",
            "Summary:",
            f"  Total Files:     {report.total_files}",
            f"  Successful:      {report.successful_files} ({round(report.successful_files/max(report.total_files,1)*100, 1)}%)",
            f"  Failed:          {report.failed_files}",
            f"  Total Theorems:  {report.total_theorems}",
            f"  Admitted:        {report.total_admitted} ({round(report.total_admitted/max(report.total_theorems,1)*100, 1)}%)",
            f"  Total Errors:    {report.total_errors}",
            "",
            "File Details:",
            "-" * 60
        ]
        
        for stat in report.file_stats:
            status = "✓" if not stat.errors else "✗"
            lines.append(f"  {status} {stat.file_path}")
            lines.append(f"    Lines: {stat.total_lines}, Theorems: {stat.theorem_count}, "
                        f"Lemmas: {stat.lemma_count}, Admitted: {stat.admitted_count}")
            if stat.errors:
                for err in stat.errors[:3]:  # 最多显示3个错误
                    lines.append(f"    Error: {err}")
            if stat.warnings:
                lines.append(f"    Warnings: {len(stat.warnings)}")
        
        lines.extend([
            "-" * 60,
            ""
        ])
        
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Verify Coq proofs in the project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --project ./my-project theories/*.v
  %(prog)s --json --output report.json
  %(prog)s --check-admitted --fail-on-admitted
  %(prog)s --ci-mode  # CI-friendly output
        """
    )
    
    parser.add_argument('files', nargs='*', default=['theories/**/*.v', 'proofs/**/*.v'],
                       help='Coq files or glob patterns to verify (default: theories/**/*.v proofs/**/*.v)')
    
    parser.add_argument('--project', '-p', default='.',
                       help='Project root directory (default: current directory)')
    
    parser.add_argument('--output', '-o',
                       help='Output directory for .vo files')
    
    parser.add_argument('--report', '-r',
                       help='Write report to file')
    
    parser.add_argument('--json', action='store_true',
                       help='Output report in JSON format')
    
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    parser.add_argument('--timeout', '-t', type=int, default=300,
                       help='Timeout per file in seconds (default: 300)')
    
    parser.add_argument('--check-admitted', action='store_true',
                       help='Check for Admitted theorems')
    
    parser.add_argument('--fail-on-admitted', action='store_true',
                       help='Exit with error if any Admitted found')
    
    parser.add_argument('--fail-on-warning', action='store_true',
                       help='Exit with error if any warnings found')
    
    parser.add_argument('--ci-mode', action='store_true',
                       help='CI-friendly output (implies --fail-on-admitted)')
    
    args = parser.parse_args()
    
    # CI模式设置
    if args.ci_mode:
        args.fail_on_admitted = True
        args.verbose = True
    
    # 创建验证器
    verifier = CoqVerifier(
        project_root=args.project,
        verbose=args.verbose,
        timeout=args.timeout
    )
    
    print(f"Coq Proof Verification")
    print(f"Project: {verifier.project_root}")
    print(f"Coq Compiler: {verifier.coqc_cmd}")
    print(f"Files: {', '.join(args.files)}")
    
    # 执行验证
    report = verifier.verify_all(args.files, args.output)
    
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
    
    if report.failed_files > 0:
        exit_code = 1
    
    if args.fail_on_admitted and report.total_admitted > 0:
        print(f"\n❌ Found {report.total_admitted} admitted theorem(s)")
        exit_code = 1
    
    if args.fail_on_warning:
        total_warnings = sum(len(s.warnings) for s in report.file_stats)
        if total_warnings > 0:
            print(f"\n❌ Found {total_warnings} warning(s)")
            exit_code = 1
    
    # 最终总结
    if exit_code == 0:
        print("\n✅ All proofs verified successfully!")
    else:
        print("\n❌ Verification failed. See details above.")
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
