#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mermaid Diagram Validator
=========================

A production-grade tool for validating Mermaid diagram syntax in Markdown files.

Features:
    - Scans all .md files for Mermaid code blocks
    - Validates diagram syntax (flowchart, sequence, class, state, etc.)
    - Detects common errors (Chinese quotes, unclosed subgraphs, etc.)
    - Generates detailed validation reports
    - CI/CD integration support

Author: AnalysisDataFlow Project
Version: 1.0.0
License: MIT

Usage:
    python mermaid-validator.py [options] [path]

Examples:
    python mermaid-validator.py                    # Validate current directory
    python mermaid-validator.py ./docs             # Validate specific directory
    python mermaid-validator.py --json             # Output JSON report
    python mermaid-validator.py --fix              # Auto-fix minor issues
    python mermaid-validator.py --strict           # Strict mode (fail on warnings)
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict


# =============================================================================
# Constants and Configuration
# =============================================================================

VERSION = "1.0.0"
DEFAULT_ENCODING = "utf-8"
MERMAID_START_PATTERN = re.compile(r'^\s*```\s*mermaid\s*$', re.IGNORECASE)
MERMAID_END_PATTERN = re.compile(r'^\s*```\s*$')

# Chinese punctuation that should be avoided in Mermaid diagrams
CHINESE_PUNCTUATION = {
    '（': '(',  # Fullwidth left parenthesis
    '）': ')',  # Fullwidth right parenthesis
    '【': '[',  # Fullwidth left bracket
    '】': ']',  # Fullwidth right bracket
    '「': '"',  # Left corner bracket
    '」': '"',  # Right corner bracket
    '"': '"',  # Left double quote
    '"': '"',  # Right double quote
    ''': "'",  # Left single quote
    ''': "'",  # Right single quote
    '：': ':',  # Fullwidth colon
    '；': ';',  # Fullwidth semicolon
    '，': ',',  # Fullwidth comma
}

# Valid Mermaid diagram types
VALID_DIAGRAM_TYPES = {
    'flowchart', 'graph', 'sequenceDiagram', 'classDiagram',
    'stateDiagram', 'stateDiagram-v2', 'erDiagram', 'journey',
    'gantt', 'pie', 'requirementDiagram', 'gitgraph',
    'C4Context', 'C4Container', 'C4Component', 'C4Dynamic',
    'mindmap', 'timeline', 'quadrantChart', 'xychart-beta',
    'block-beta', 'packet-beta', 'kanban', 'architecture-beta'
}

# Valid arrow syntax patterns
VALID_ARROW_PATTERNS = [
    r'-->',     # Standard arrow
    r'---',     # Line without arrow
    r'--\|>',   # Arrow with bar
    r'--\)',    # Arrow with circle
    r'--\(\)',  # Arrow with double circle
    r'--x',     # Arrow with cross
    r'--o',     # Arrow with open circle
    r'==>',     # Thick arrow
    r'==',      # Thick line
    r'==\|>',   # Thick arrow with bar
    r'==\)',    # Thick arrow with circle
    r'==x',     # Thick arrow with cross
    r'==o',     # Thick arrow with open circle
    r'-\.->',   # Dotted arrow
    r'\.->',   # Dotted arrow alt
    r'-\.-',    # Dotted line
    r'\.\.-',  # Dotted line alt
    r'--\|',    # Bar without arrow
    r'==\|',    # Thick bar without arrow
    r'--',      # Simple line
]

ARROW_PATTERN = re.compile('|'.join(VALID_ARROW_PATTERNS))


# =============================================================================
# Enums and Data Classes
# =============================================================================

class ErrorSeverity(Enum):
    """Error severity levels."""
    ERROR = "error"       # Critical error, diagram won't render
    WARNING = "warning"   # Potential issue, may affect rendering
    INFO = "info"         # Style suggestion, best practice


class ErrorType(Enum):
    """Types of validation errors."""
    CHINESE_QUOTES = "chinese_quotes"
    UNCLOSED_SUBGRAPH = "unclosed_subgraph"
    INVALID_ARROW = "invalid_arrow"
    UNQUOTED_CHINESE_NODE = "unquoted_chinese_node"
    UNBALANCED_BRACKETS = "unbalanced_brackets"
    INVALID_DIRECTIVE = "invalid_directive"
    UNCLOSED_STRING = "unclosed_string"
    ORPHAN_END = "orphan_end"
    INVALID_NODE_ID = "invalid_node_id"
    UNKNOWN_DIAGRAM_TYPE = "unknown_diagram_type"
    UNCLOSED_CODE_BLOCK = "unclosed_code_block"


@dataclass
class ValidationError:
    """Represents a single validation error."""
    error_type: ErrorType
    severity: ErrorSeverity
    message: str
    line_number: int
    column: int
    suggestion: str
    context: str = ""  # Surrounding lines for context


@dataclass
class MermaidBlock:
    """Represents a Mermaid code block found in a file."""
    start_line: int
    end_line: int
    content: List[str]
    diagram_type: Optional[str] = None
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    infos: List[ValidationError] = field(default_factory=list)

    def all_issues(self) -> List[ValidationError]:
        """Return all issues sorted by line number."""
        all_issues = self.errors + self.warnings + self.infos
        return sorted(all_issues, key=lambda x: x.line_number)


@dataclass
class FileReport:
    """Validation report for a single file."""
    file_path: str
    blocks: List[MermaidBlock] = field(default_factory=list)
    parse_errors: List[str] = field(default_factory=list)

    def error_count(self) -> int:
        """Total number of errors across all blocks."""
        return sum(len(b.errors) for b in self.blocks)

    def warning_count(self) -> int:
        """Total number of warnings across all blocks."""
        return sum(len(b.warnings) for b in self.blocks)

    def info_count(self) -> int:
        """Total number of info messages across all blocks."""
        return sum(len(b.infos) for b in self.blocks)

    def has_issues(self) -> bool:
        """Check if file has any validation issues."""
        return self.error_count() > 0 or self.warning_count() > 0


@dataclass
class ValidationReport:
    """Overall validation report."""
    files: List[FileReport] = field(default_factory=list)
    scanned_files: int = 0
    skipped_files: int = 0

    def error_count(self) -> int:
        """Total errors across all files."""
        return sum(f.error_count() for f in self.files)

    def warning_count(self) -> int:
        """Total warnings across all files."""
        return sum(f.warning_count() for f in self.files)

    def info_count(self) -> int:
        """Total info messages across all files."""
        return sum(f.info_count() for f in self.files)

    def block_count(self) -> int:
        """Total Mermaid blocks found."""
        return sum(len(f.blocks) for f in self.files)

    def files_with_errors(self) -> List[FileReport]:
        """Get files that have validation errors."""
        return [f for f in self.files if f.error_count() > 0]

    def files_with_warnings(self) -> List[FileReport]:
        """Get files that have warnings (but no errors)."""
        return [f for f in self.files if f.error_count() == 0 and f.warning_count() > 0]


# =============================================================================
# Core Validator Class
# =============================================================================

class MermaidValidator:
    """
    Main validator class for Mermaid diagrams.
    
    This class handles the parsing and validation of Mermaid code blocks
    found in Markdown files.
    """

    def __init__(self, strict: bool = False, check_chinese: bool = True):
        """
        Initialize the validator.
        
        Args:
            strict: If True, warnings are treated as errors
            check_chinese: If True, validate Chinese text formatting
        """
        self.strict = strict
        self.check_chinese = check_chinese
        self.errors: List[ValidationError] = []

    def validate_file(self, file_path: Path) -> FileReport:
        """
        Validate all Mermaid blocks in a single file.
        
        Args:
            file_path: Path to the Markdown file
            
        Returns:
            FileReport containing validation results
        """
        report = FileReport(str(file_path))
        
        try:
            content = file_path.read_text(encoding=DEFAULT_ENCODING)
            lines = content.split('\n')
        except Exception as e:
            report.parse_errors.append(f"Failed to read file: {e}")
            return report

        in_mermaid_block = False
        current_block_start = 0
        current_block_lines: List[str] = []

        for line_num, line in enumerate(lines, 1):
            if MERMAID_START_PATTERN.match(line):
                if in_mermaid_block:
                    # Nested mermaid block - report error
                    report.parse_errors.append(
                        f"Line {line_num}: Nested Mermaid block detected"
                    )
                in_mermaid_block = True
                current_block_start = line_num
                current_block_lines = []
            elif MERMAID_END_PATTERN.match(line) and in_mermaid_block:
                block = MermaidBlock(
                    start_line=current_block_start,
                    end_line=line_num,
                    content=current_block_lines.copy()
                )
                self._validate_block(block)
                report.blocks.append(block)
                in_mermaid_block = False
                current_block_lines = []
            elif in_mermaid_block:
                current_block_lines.append(line)

        # Check for unclosed block
        if in_mermaid_block:
            report.parse_errors.append(
                f"Line {current_block_start}: Unclosed Mermaid block "
                f"(started at line {current_block_start})"
            )

        return report

    def _validate_block(self, block: MermaidBlock) -> None:
        """
        Validate a single Mermaid block.
        
        Args:
            block: MermaidBlock to validate
        """
        if not block.content:
            block.errors.append(ValidationError(
                error_type=ErrorType.INVALID_DIRECTIVE,
                severity=ErrorSeverity.ERROR,
                message="Empty Mermaid block",
                line_number=block.start_line,
                column=0,
                suggestion="Add diagram content or remove empty block"
            ))
            return

        # Detect diagram type from first line
        first_line = block.content[0].strip() if block.content else ""
        block.diagram_type = self._detect_diagram_type(first_line)

        # Validate based on diagram type
        if block.diagram_type in {'flowchart', 'graph'}:
            self._validate_flowchart(block)
        elif block.diagram_type == 'sequenceDiagram':
            self._validate_sequence_diagram(block)
        elif block.diagram_type in {'classDiagram', 'erDiagram'}:
            self._validate_declaration_diagram(block)
        elif block.diagram_type and 'stateDiagram' in block.diagram_type:
            self._validate_state_diagram(block)
        else:
            # Generic validation for other diagram types
            self._validate_generic(block)

    def _detect_diagram_type(self, first_line: str) -> Optional[str]:
        """
        Detect the type of Mermaid diagram.
        
        Args:
            first_line: First line of the diagram content
            
        Returns:
            Diagram type string or None if unknown
        """
        # Handle direction suffix (e.g., "flowchart TD", "graph LR")
        words = first_line.split()
        if not words:
            return None

        base_type = words[0].lower()
        
        # Map legacy 'graph' to 'flowchart'
        if base_type == 'graph':
            return 'flowchart'
        
        # Handle stateDiagram-v2
        if base_type.startswith('statediagram'):
            return base_type
            
        return base_type if base_type in VALID_DIAGRAM_TYPES else None

    def _validate_flowchart(self, block: MermaidBlock) -> None:
        """Validate flowchart/graph specific syntax."""
        subgraph_stack: List[Tuple[str, int]] = []  # (name, line_number)
        
        for idx, line in enumerate(block.content):
            line_num = block.start_line + idx + 1
            stripped = line.strip()
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith('%%'):
                continue

            # Check for Chinese punctuation
            if self.check_chinese:
                self._check_chinese_punctuation(line, line_num, block)

            # Check subgraph
            if stripped.lower().startswith('subgraph'):
                subgraph_name = stripped[8:].strip()
                subgraph_stack.append((subgraph_name, line_num))
            elif stripped.lower() == 'end':
                if subgraph_stack:
                    subgraph_stack.pop()
                else:
                    block.errors.append(ValidationError(
                        error_type=ErrorType.ORPHAN_END,
                        severity=ErrorSeverity.ERROR,
                        message="'end' without matching 'subgraph'",
                        line_number=line_num,
                        column=line.find('end'),
                        suggestion="Remove orphan 'end' or add missing 'subgraph'"
                    ))

            # Check node definitions and arrows
            self._check_flowchart_line(line, line_num, block)

        # Check for unclosed subgraphs
        for subgraph_name, line_num in subgraph_stack:
            block.errors.append(ValidationError(
                error_type=ErrorType.UNCLOSED_SUBGRAPH,
                severity=ErrorSeverity.ERROR,
                message=f"Unclosed subgraph: '{subgraph_name}'",
                line_number=line_num,
                column=0,
                suggestion="Add 'end' to close the subgraph"
            ))

    def _check_flowchart_line(self, line: str, line_num: int, block: MermaidBlock) -> None:
        """Validate a single flowchart line."""
        stripped = line.strip()
        
        # Skip subgraph/end lines
        if stripped.lower().startswith('subgraph') or stripped.lower() == 'end':
            return

        # Check for arrow connections
        if '--' in line or '==' in line or '-.' in line:
            self._validate_arrow_syntax(line, line_num, block)

        # Check for unquoted Chinese text in node definitions
        self._check_unquoted_chinese(line, line_num, block)

        # Check bracket balance in node definitions
        self._check_bracket_balance(line, line_num, block)

    def _validate_arrow_syntax(self, line: str, line_num: int, block: MermaidBlock) -> None:
        """Validate arrow syntax in flowchart connections."""
        # Check for common arrow mistakes
        mistakes = [
            (r'--\s*>', '-->', "Remove space between '--' and '>'"),
            (r'==\s*>', '==>', "Remove space between '==' and '>'"),
            (r'-\.\s*>', '-.->', "Remove space between '.-' and '>'"),
            (r'-\s*-*>', '-->', "Remove space in arrow"),
        ]
        
        for pattern, correct, suggestion in mistakes:
            if re.search(pattern, line):
                block.errors.append(ValidationError(
                    error_type=ErrorType.INVALID_ARROW,
                    severity=ErrorSeverity.ERROR,
                    message=f"Invalid arrow syntax",
                    line_number=line_num,
                    column=line.find('--'),
                    suggestion=f"Use '{correct}' instead. {suggestion}"
                ))

    def _check_unquoted_chinese(self, line: str, line_num: int, block: MermaidBlock) -> None:
        """Check for unquoted Chinese text in node definitions."""
        # Pattern to match node definitions with brackets
        # Examples: A[中文], B(中文), C{中文}
        node_patterns = [
            r'\[([^\]]*[一-龥]+[^\]]*)\]',  # Square brackets
            r'\(([^\)]*[一-龥]+[^\)]*)\)',  # Parentheses
            r'\{([^\}]*[一-龥]+[^\}]*)\}',  # Curly braces
        ]
        
        for pattern in node_patterns:
            for match in re.finditer(pattern, line):
                content = match.group(1)
                # Check if content is NOT properly quoted
                if not re.match(r'^"[^"]*"$', content.strip()):
                    # Chinese text found without proper quotes
                    block.warnings.append(ValidationError(
                        error_type=ErrorType.UNQUOTED_CHINESE_NODE,
                        severity=ErrorSeverity.WARNING,
                        message=f"Chinese text in node should be quoted: '{content[:30]}...'" if len(content) > 30 else f"Chinese text in node should be quoted: '{content}'",
                        line_number=line_num,
                        column=match.start(),
                        suggestion=f'Use ["{content}"] with double quotes around Chinese text'
                    ))

    def _check_bracket_balance(self, line: str, line_num: int, block: MermaidBlock) -> None:
        """Check for balanced brackets in node definitions."""
        brackets = {'[': ']', '(': ')', '{': '}', '<': '>'}
        stack: List[Tuple[str, int]] = []
        
        for idx, char in enumerate(line):
            if char in brackets:
                stack.append((char, idx))
            elif char in brackets.values():
                if stack and brackets[stack[-1][0]] == char:
                    stack.pop()
                else:
                    block.errors.append(ValidationError(
                        error_type=ErrorType.UNBALANCED_BRACKETS,
                        severity=ErrorSeverity.ERROR,
                        message=f"Unbalanced bracket: unexpected '{char}'",
                        line_number=line_num,
                        column=idx,
                        suggestion=f"Add matching '{brackets.get(char, char)}' or remove extra '{char}'"
                    ))

    def _check_chinese_punctuation(self, line: str, line_num: int, block: MermaidBlock) -> None:
        """Check for Chinese punctuation that might cause parsing issues."""
        for idx, char in enumerate(line):
            if char in CHINESE_PUNCTUATION:
                replacement = CHINESE_PUNCTUATION[char]
                block.warnings.append(ValidationError(
                    error_type=ErrorType.CHINESE_QUOTES,
                    severity=ErrorSeverity.WARNING,
                    message=f"Chinese punctuation detected: '{char}'",
                    line_number=line_num,
                    column=idx,
                    suggestion=f"Replace with ASCII equivalent: '{replacement}'"
                ))

    def _validate_sequence_diagram(self, block: MermaidBlock) -> None:
        """Validate sequence diagram specific syntax."""
        for idx, line in enumerate(block.content):
            line_num = block.start_line + idx + 1
            stripped = line.strip()
            
            if not stripped or stripped.startswith('%%'):
                continue

            if self.check_chinese:
                self._check_chinese_punctuation(line, line_num, block)

            # Check for participant declarations
            if stripped.lower().startswith('participant') or stripped.lower().startswith('actor'):
                # Check for unquoted Chinese in participant names
                if re.search(r'[一-龥]', stripped):
                    if '"' not in stripped:
                        block.warnings.append(ValidationError(
                            error_type=ErrorType.UNQUOTED_CHINESE_NODE,
                            severity=ErrorSeverity.WARNING,
                            message="Participant with Chinese text should be quoted",
                            line_number=line_num,
                            column=0,
                            suggestion='Use: participant "中文名称" as alias'
                        ))

            # Check message arrows
            if '->>' in line or '-->>' in line or '->' in line or '-->' in line:
                # Valid sequence diagram arrows
                pass

    def _validate_declaration_diagram(self, block: MermaidBlock) -> None:
        """Validate class diagram or ER diagram syntax."""
        for idx, line in enumerate(block.content):
            line_num = block.start_line + idx + 1
            if self.check_chinese:
                self._check_chinese_punctuation(line, line_num, block)

    def _validate_state_diagram(self, block: MermaidBlock) -> None:
        """Validate state diagram specific syntax."""
        state_stack: List[Tuple[str, int]] = []
        
        for idx, line in enumerate(block.content):
            line_num = block.start_line + idx + 1
            stripped = line.strip()
            
            if not stripped or stripped.startswith('%%'):
                continue

            if self.check_chinese:
                self._check_chinese_punctuation(line, line_num, block)

            # Check for state blocks
            if stripped.lower().startswith('state'):
                # Check if it's a composite state definition
                if '{' in stripped:
                    state_name = stripped[5:stripped.find('{')].strip()
                    state_stack.append((state_name, line_num))
                elif stripped.endswith('{'):
                    state_stack.append((stripped, line_num))
            elif stripped == '}':
                if state_stack:
                    state_stack.pop()

        # Check for unclosed states
        for state_name, line_num in state_stack:
            block.errors.append(ValidationError(
                error_type=ErrorType.UNCLOSED_SUBGRAPH,
                severity=ErrorSeverity.ERROR,
                message=f"Unclosed state: '{state_name}'",
                line_number=line_num,
                column=0,
                suggestion="Add '}' to close the state"
            ))

    def _validate_generic(self, block: MermaidBlock) -> None:
        """Generic validation for unsupported diagram types."""
        if not block.diagram_type:
            block.warnings.append(ValidationError(
                error_type=ErrorType.UNKNOWN_DIAGRAM_TYPE,
                severity=ErrorSeverity.WARNING,
                message=f"Unknown or missing diagram type",
                line_number=block.start_line + 1,
                column=0,
                suggestion=f"Valid types: {', '.join(sorted(VALID_DIAGRAM_TYPES))}"
            ))

        for idx, line in enumerate(block.content):
            line_num = block.start_line + idx + 1
            if self.check_chinese:
                self._check_chinese_punctuation(line, line_num, block)


# =============================================================================
# Report Generators
# =============================================================================

class ReportGenerator:
    """Base class for report generators."""
    
    def generate(self, report: ValidationReport) -> str:
        """Generate report string from validation results."""
        raise NotImplementedError


class ConsoleReportGenerator(ReportGenerator):
    """Generate human-readable console output."""
    
    COLORS = {
        'error': '\033[91m',      # Red
        'warning': '\033[93m',    # Yellow
        'info': '\033[94m',       # Blue
        'reset': '\033[0m',       # Reset
        'bold': '\033[1m',        # Bold
        'green': '\033[92m',      # Green
    }

    def __init__(self, use_color: bool = True):
        self.use_color = use_color and sys.stdout.isatty()

    def _color(self, color: str, text: str) -> str:
        """Apply color to text if enabled."""
        if self.use_color:
            return f"{self.COLORS.get(color, '')}{text}{self.COLORS['reset']}"
        return text

    def generate(self, report: ValidationReport) -> str:
        """Generate console-formatted report."""
        lines = []
        
        # Header
        lines.append(self._color('bold', '=' * 70))
        lines.append(self._color('bold', '  MERMAID DIAGRAM VALIDATION REPORT'))
        lines.append(self._color('bold', '=' * 70))
        lines.append('')

        # Summary
        error_files = len(report.files_with_errors())
        warning_files = len(report.files_with_warnings())
        
        lines.append(self._color('bold', 'SUMMARY'))
        lines.append('-' * 40)
        lines.append(f"Files scanned:      {report.scanned_files}")
        lines.append(f"Files skipped:      {report.skipped_files}")
        lines.append(f"Mermaid blocks:     {report.block_count()}")
        lines.append('')
        
        # Color-coded issue counts
        error_str = self._color('error', f"{report.error_count()} errors") if report.error_count() > 0 else "0 errors"
        warning_str = self._color('warning', f"{report.warning_count()} warnings") if report.warning_count() > 0 else "0 warnings"
        info_str = self._color('info', f"{report.info_count()} info") if report.info_count() > 0 else "0 info"
        
        lines.append(f"Issues found:       {error_str}, {warning_str}, {info_str}")
        lines.append(f"Files with errors:  {error_files}")
        lines.append(f"Files with warnings:{warning_files}")
        lines.append('')

        # Error details
        if report.error_count() > 0:
            lines.append(self._color('error', self._color('bold', 'ERRORS')))
            lines.append(self._color('error', '-' * 40))
            
            for file_report in report.files_with_errors():
                lines.append(f"\n📄 {self._color('bold', file_report.file_path)}")
                
                for block in file_report.blocks:
                    if block.errors:
                        lines.append(f"  Block (lines {block.start_line}-{block.end_line})")
                        for error in block.errors:
                            lines.append(f"    ❌ {self._color('error', error.error_type.value)}")
                            lines.append(f"       Line {error.line_number}, Col {error.column}: {error.message}")
                            lines.append(f"       💡 {error.suggestion}")
            lines.append('')

        # Warning details
        if report.warning_count() > 0:
            lines.append(self._color('warning', self._color('bold', 'WARNINGS')))
            lines.append(self._color('warning', '-' * 40))
            
            for file_report in report.files_with_warnings() + report.files_with_errors():
                warnings_to_show = [b for b in file_report.blocks if b.warnings]
                if not warnings_to_show:
                    continue
                    
                lines.append(f"\n📄 {self._color('bold', file_report.file_path)}")
                
                for block in warnings_to_show:
                    lines.append(f"  Block (lines {block.start_line}-{block.end_line})")
                    for warning in block.warnings[:5]:  # Limit warnings per block
                        lines.append(f"    ⚠️  {self._color('warning', warning.error_type.value)}")
                        lines.append(f"       Line {warning.line_number}: {warning.message}")
                        lines.append(f"       💡 {warning.suggestion}")
                    if len(block.warnings) > 5:
                        lines.append(f"    ... and {len(block.warnings) - 5} more warnings")
            lines.append('')

        # Success message
        if report.error_count() == 0 and report.warning_count() == 0:
            lines.append(self._color('green', self._color('bold', '✅ All validations passed!')))
            lines.append('')

        # Footer
        lines.append(self._color('bold', '=' * 70))
        lines.append(f"Validation completed at {self._get_timestamp()}")
        lines.append(self._color('bold', '=' * 70))
        
        return '\n'.join(lines)

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class JSONReportGenerator(ReportGenerator):
    """Generate JSON format report for CI/CD integration."""
    
    def generate(self, report: ValidationReport) -> str:
        """Generate JSON-formatted report."""
        data = {
            'version': VERSION,
            'timestamp': self._get_timestamp(),
            'summary': {
                'scanned_files': report.scanned_files,
                'skipped_files': report.skipped_files,
                'total_blocks': report.block_count(),
                'total_errors': report.error_count(),
                'total_warnings': report.warning_count(),
                'total_info': report.info_count(),
                'files_with_errors': len(report.files_with_errors()),
                'files_with_warnings': len(report.files_with_warnings()),
            },
            'files': []
        }

        for file_report in report.files:
            file_data = {
                'path': file_report.file_path,
                'error_count': file_report.error_count(),
                'warning_count': file_report.warning_count(),
                'parse_errors': file_report.parse_errors,
                'blocks': []
            }

            for block in file_report.blocks:
                block_data = {
                    'start_line': block.start_line,
                    'end_line': block.end_line,
                    'diagram_type': block.diagram_type,
                    'errors': [
                        {
                            'type': e.error_type.value,
                            'severity': e.severity.value,
                            'message': e.message,
                            'line': e.line_number,
                            'column': e.column,
                            'suggestion': e.suggestion
                        }
                        for e in block.errors
                    ],
                    'warnings': [
                        {
                            'type': w.error_type.value,
                            'severity': w.severity.value,
                            'message': w.message,
                            'line': w.line_number,
                            'column': w.column,
                            'suggestion': w.suggestion
                        }
                        for w in block.warnings
                    ]
                }
                file_data['blocks'].append(block_data)

            data['files'].append(file_data)

        return json.dumps(data, indent=2, ensure_ascii=False)

    def _get_timestamp(self) -> str:
        """Get ISO format timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()


class MarkdownReportGenerator(ReportGenerator):
    """Generate Markdown format report for documentation."""
    
    def generate(self, report: ValidationReport) -> str:
        """Generate Markdown-formatted report."""
        lines = [
            '# Mermaid Validation Report',
            '',
            f'**Generated:** {self._get_timestamp()}',
            f'**Version:** {VERSION}',
            '',
            '## Summary',
            '',
            '| Metric | Count |',
            '|--------|-------|',
            f'| Files Scanned | {report.scanned_files} |',
            f'| Files Skipped | {report.skipped_files} |',
            f'| Mermaid Blocks | {report.block_count()} |',
            f'| Total Errors | {report.error_count()} |',
            f'| Total Warnings | {report.warning_count()} |',
            f'| Files with Errors | {len(report.files_with_errors())} |',
            '',
        ]

        if report.error_count() > 0:
            lines.extend(['## Errors', ''])
            
            for file_report in report.files_with_errors():
                lines.append(f'### {file_report.file_path}')
                lines.append('')
                
                for block in file_report.blocks:
                    if block.errors:
                        lines.append(f'**Block (lines {block.start_line}-{block.end_line})**')
                        lines.append('')
                        
                        for error in block.errors:
                            lines.append(f'- **{error.error_type.value}** (Line {error.line_number})')
                            lines.append(f'  - Message: {error.message}')
                            lines.append(f'  - Suggestion: {error.suggestion}')
                            lines.append('')

        if report.warning_count() > 0:
            lines.extend(['## Warnings', ''])
            
            for file_report in report.files:
                warnings = [b for b in file_report.blocks if b.warnings]
                if not warnings:
                    continue
                    
                lines.append(f'### {file_report.file_path}')
                lines.append('')
                
                for block in warnings:
                    for warning in block.warnings[:3]:
                        lines.append(f'- **{warning.error_type.value}** (Line {warning.line_number})')
                        lines.append(f'  - {warning.message}')
                        lines.append('')

        if report.error_count() == 0 and report.warning_count() == 0:
            lines.extend(['## Result', '', '✅ All validations passed!', ''])

        return '\n'.join(lines)

    def _get_timestamp(self) -> str:
        """Get formatted timestamp."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# =============================================================================
# CLI and Main Entry Point
# =============================================================================

def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog='mermaid-validator',
        description='Validate Mermaid diagram syntax in Markdown files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Validate current directory
  %(prog)s ./docs                   # Validate specific directory
  %(prog)s --json -o report.json    # Output JSON report to file
  %(prog)s --strict                 # Fail on warnings (CI mode)
  %(prog)s --no-chinese-check       # Skip Chinese punctuation validation
  %(prog)s --exclude node_modules   # Exclude specific directories

Exit Codes:
  0  - Validation successful (no errors)
  1  - Validation failed (errors found)
  2  - Invalid arguments or runtime error
        """
    )

    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to directory or file to validate (default: current directory)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: stdout)'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format (for CI/CD integration)'
    )

    parser.add_argument(
        '--markdown',
        action='store_true',
        help='Output in Markdown format'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors (strict mode)'
    )

    parser.add_argument(
        '--no-chinese-check',
        action='store_true',
        help='Disable Chinese punctuation validation'
    )

    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )

    parser.add_argument(
        '--exclude',
        action='append',
        default=[],
        help='Directory names to exclude (can be used multiple times)'
    )

    parser.add_argument(
        '--max-file-size',
        type=int,
        default=10,
        help='Maximum file size in MB to process (default: 10)'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {VERSION}'
    )

    return parser


def find_markdown_files(
    path: Path,
    exclude_dirs: Set[str],
    max_file_size_mb: int
) -> Tuple[List[Path], List[Path]]:
    """
    Find all Markdown files in the given path.
    
    Args:
        path: Starting path (file or directory)
        exclude_dirs: Set of directory names to exclude
        max_file_size_mb: Maximum file size in MB
        
    Returns:
        Tuple of (found_files, skipped_files)
    """
    found_files: List[Path] = []
    skipped_files: List[Path] = []
    max_bytes = max_file_size_mb * 1024 * 1024

    if path.is_file():
        if path.suffix.lower() in {'.md', '.markdown'}:
            if path.stat().st_size <= max_bytes:
                found_files.append(path)
            else:
                skipped_files.append(path)
        return found_files, skipped_files

    for root, dirs, files in os.walk(path):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for filename in files:
            if filename.lower().endswith(('.md', '.markdown')):
                file_path = Path(root) / filename
                try:
                    if file_path.stat().st_size <= max_bytes:
                        found_files.append(file_path)
                    else:
                        skipped_files.append(file_path)
                except OSError:
                    skipped_files.append(file_path)

    return found_files, skipped_files


def main() -> int:
    """
    Main entry point.
    
    Returns:
        Exit code (0 = success, 1 = validation errors, 2 = runtime error)
    """
    parser = create_argument_parser()
    args = parser.parse_args()

    try:
        target_path = Path(args.path)
        
        if not target_path.exists():
            print(f"Error: Path not found: {target_path}", file=sys.stderr)
            return 2

        # Setup validator
        validator = MermaidValidator(
            strict=args.strict,
            check_chinese=not args.no_chinese_check
        )

        # Find files
        exclude_dirs = set(args.exclude) | {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}
        markdown_files, skipped_files = find_markdown_files(
            target_path,
            exclude_dirs,
            args.max_file_size
        )

        if not markdown_files:
            print("No Markdown files found.", file=sys.stderr)
            return 0

        # Validate all files
        report = ValidationReport(
            scanned_files=len(markdown_files),
            skipped_files=len(skipped_files)
        )

        for file_path in markdown_files:
            file_report = validator.validate_file(file_path)
            report.files.append(file_report)

        # Generate report
        if args.json:
            generator: ReportGenerator = JSONReportGenerator()
        elif args.markdown:
            generator = MarkdownReportGenerator()
        else:
            generator = ConsoleReportGenerator(use_color=not args.no_color)

        output = generator.generate(report)

        # Output results
        if args.output:
            with open(args.output, 'w', encoding=DEFAULT_ENCODING) as f:
                f.write(output)
            print(f"Report written to: {args.output}")
        else:
            print(output)

        # Determine exit code
        if report.error_count() > 0:
            return 1
        if args.strict and report.warning_count() > 0:
            return 1
        return 0

    except KeyboardInterrupt:
        print("\nValidation interrupted by user.", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
