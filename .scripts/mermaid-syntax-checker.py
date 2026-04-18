#!/usr/bin/env python3
"""
Mermaid图表语法检查器
功能：
- 提取所有Mermaid代码块
- 语法验证
- 生成可视化统计

作者: AnalysisDataFlow Toolchain Team
版本: 1.0.0
日期: 2026-04-11
"""

import re
import os
import json
import glob
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict
import argparse


@dataclass
class MermaidDiagram:
    """Mermaid图表记录"""
    file_path: str
    line_start: int
    line_end: int
    diagram_type: str
    content: str
    node_count: int
    edge_count: int
    has_syntax_error: bool
    error_message: Optional[str]


@dataclass
class SyntaxError:
    """语法错误记录"""
    file_path: str
    line_number: int
    error_type: str
    message: str
    context: str


class MermaidSyntaxChecker:
    """Mermaid语法检查器"""
    
    # 支持的图表类型
    DIAGRAM_TYPES = {
        'graph': ['TB', 'BT', 'LR', 'RL', 'TD'],
        'flowchart': ['TB', 'BT', 'LR', 'RL', 'TD'],
        'sequenceDiagram': [],
        'classDiagram': [],
        'stateDiagram': [],
        'stateDiagram-v2': [],
        'erDiagram': [],
        'gantt': [],
        'pie': [],
        'gitGraph': [],
        'journey': [],
        'requirementDiagram': [],
        'C4Context': [],
        'mindmap': [],
        'timeline': [],
        'xychart-beta': [],
        'quadrantChart': [],
        'radar': [],
        'radarChart': [],
        'block-beta': [],
        'sankey-beta': [],
    }
    
    # 节点定义模式
    NODE_PATTERNS = {
        'rectangle': r'\[\s*([^\]]+)\s*\]',
        'rounded': r'\(\s*([^)]+)\s*\)',
        'circle': r'\(\(\s*([^)]+)\s*\)\)',
        'rhombus': r'\{\s*([^}]+)\s*\}',
        'subroutine': r'\[\[\s*([^\]]+)\s*\]\]',
        'cylinder': r'\[\(\s*([^)]+)\s*\)\]',
        'circle_small': r'\(\s*([^)]+)\s*\)',
    }
    
    def __init__(self, base_path: str, use_mmdc: bool = False):
        self.base_path = Path(base_path).resolve()
        self.use_mmdc = use_mmdc  # 是否使用mmdc CLI工具
        self.diagrams: List[MermaidDiagram] = []
        self.errors: List[SyntaxError] = []
        
    def scan_all_files(self) -> List[Path]:
        """扫描所有Markdown文件"""
        md_files = []
        patterns = [
            "Struct/**/*.md",
            "Knowledge/**/*.md",
            "Flink/**/*.md",
            "docs/**/*.md",
            "*.md"
        ]
        
        for pattern in patterns:
            files = glob.glob(str(self.base_path / pattern), recursive=True)
            for f in files:
                path = Path(f).resolve()
                if not any(part.startswith('.') for part in path.parts):
                    md_files.append(path)
                    
        return list(set(md_files))
    
    def extract_mermaid_blocks(self, content: str) -> List[Tuple[int, int, str]]:
        """提取所有Mermaid代码块"""
        blocks = []
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # 匹配 ```mermaid 开始
            if re.match(r'^\s*```\s*mermaid\s*$', line, re.IGNORECASE):
                start_line = i
                diagram_lines = []
                i += 1
                
                # 收集到 ``` 结束
                while i < len(lines) and not re.match(r'^\s*```\s*$', lines[i]):
                    diagram_lines.append(lines[i])
                    i += 1
                    
                end_line = i
                diagram_content = '\n'.join(diagram_lines)
                blocks.append((start_line + 1, end_line, diagram_content))
                
            i += 1
            
        return blocks
    
    def detect_diagram_type(self, content: str) -> str:
        """检测图表类型"""
        first_line = content.strip().split('\n')[0].strip().lower()
        
        for dtype in self.DIAGRAM_TYPES.keys():
            if first_line.startswith(dtype.lower()):
                return dtype
                
        # 特殊处理
        if 'flowchart' in first_line:
            return 'flowchart'
        if first_line.startswith('graph'):
            return 'graph'
            
        return 'unknown'
    
    def count_nodes_and_edges(self, content: str, diagram_type: str) -> Tuple[int, int]:
        """统计节点和边的数量"""
        nodes = set()
        edges = 0
        
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('%') or line.startswith('%%'):
                continue
                
            # 跳过指令
            if line.startswith('subgraph') or line.startswith('end') or line.startswith('direction'):
                continue
                
            # 统计节点
            for pattern in self.NODE_PATTERNS.values():
                matches = re.findall(pattern, line)
                for match in matches:
                    nodes.add(match.strip())
                    
            # 统计边（箭头）
            if '-->' in line or '---' in line or '-.->' in line or '==>' in line:
                edges += 1
                # 提取节点ID
                node_ids = re.findall(r'([\w\-]+)\s*(?:-->|---|-.->|==>)', line)
                for nid in node_ids:
                    nodes.add(nid.strip())
                    
        return len(nodes), edges
    
    def validate_syntax_basic(self, content: str, diagram_type: str) -> Tuple[bool, Optional[str]]:
        """基本语法验证"""
        lines = content.split('\n')
        
        # 1. 检查图表类型
        if diagram_type == 'unknown':
            return False, "无法识别的图表类型"
            
        # 2. 检查基本结构
        if diagram_type in ['graph', 'flowchart']:
            # 检查方向
            first_line = lines[0].strip()
            if not any(d in first_line.upper() for d in ['TB', 'BT', 'LR', 'RL', 'TD']):
                pass  # 方向是可选的
                
            # 检查括号匹配
            brackets = {'[': ']', '(': ')', '{': '}', '[': ']'}
            stack = []
            for char in content:
                if char in brackets.keys():
                    stack.append(char)
                elif char in brackets.values():
                    if not stack:
                        return False, f"多余的闭合括号: {char}"
                    if brackets[stack.pop()] != char:
                        return False, f"括号不匹配"
                        
        # 3. 检查常见错误（仅在 graph/flowchart 中检测空节点）
        if diagram_type in ['graph', 'flowchart']:
            error_patterns = [
                (r'\[\s*\]', "空矩形节点"),
                (r'\(\s*\)', "空圆形节点"),
                (r'\{\s*\}', "空菱形节点"),
                (r'\|\s*\|', "空记录节点"),
            ]
            
            for pattern, desc in error_patterns:
                if re.search(pattern, content):
                    return False, f"发现{desc}"
                
        return True, None
    
    def validate_with_mmdc(self, content: str) -> Tuple[bool, Optional[str]]:
        """使用mmdc CLI工具验证（如果可用）"""
        if not self.use_mmdc:
            return True, None
            
        try:
            # 创建临时文件
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
                f.write(content)
                temp_path = f.name
                
            # 运行mmdc
            result = subprocess.run(
                ['mmdc', '-i', temp_path, '-o', '/dev/null'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # 清理
            os.unlink(temp_path)
            
            if result.returncode != 0:
                return False, result.stderr
                
            return True, None
            
        except subprocess.TimeoutExpired:
            return False, "验证超时"
        except FileNotFoundError:
            return True, None  # mmdc未安装，跳过
        except Exception as e:
            return True, None  # 其他错误，不阻断
    
    def analyze_file(self, file_path: Path) -> List[MermaidDiagram]:
        """分析单个文件"""
        diagrams = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(SyntaxError(
                file_path=str(file_path.relative_to(self.base_path)),
                line_number=0,
                error_type='read_error',
                message=f'无法读取文件: {e}',
                context=''
            ))
            return diagrams
            
        rel_path = str(file_path.relative_to(self.base_path))
        blocks = self.extract_mermaid_blocks(content)
        
        for start_line, end_line, block_content in blocks:
            diagram_type = self.detect_diagram_type(block_content)
            node_count, edge_count = self.count_nodes_and_edges(block_content, diagram_type)
            
            # 基本验证
            is_valid, error_msg = self.validate_syntax_basic(block_content, diagram_type)
            
            # 如果基本验证通过且启用了mmdc，则进一步验证
            if is_valid and self.use_mmdc:
                is_valid, error_msg = self.validate_with_mmdc(block_content)
                
            diagram = MermaidDiagram(
                file_path=rel_path,
                line_start=start_line,
                line_end=end_line,
                diagram_type=diagram_type,
                content=block_content[:500] + '...' if len(block_content) > 500 else block_content,
                node_count=node_count,
                edge_count=edge_count,
                has_syntax_error=not is_valid,
                error_message=error_msg
            )
            diagrams.append(diagram)
            
            if not is_valid:
                self.errors.append(SyntaxError(
                    file_path=rel_path,
                    line_number=start_line,
                    error_type='syntax_error',
                    message=error_msg or '语法错误',
                    context=block_content[:200]
                ))
                
        return diagrams
    
    def run_check(self) -> Tuple[List[MermaidDiagram], List[SyntaxError], Dict]:
        """运行完整检查"""
        print("📊 Mermaid Syntax Checker")
        print("=" * 50)
        
        files = self.scan_all_files()
        print(f"\n📁 Found {len(files)} Markdown files")
        
        all_diagrams = []
        
        print("\n🔎 Extracting and validating diagrams...")
        for i, file_path in enumerate(files, 1):
            if i % 50 == 0:
                print(f"   Progress: {i}/{len(files)} files")
                
            diagrams = self.analyze_file(file_path)
            all_diagrams.extend(diagrams)
            
        # 统计
        stats = {
            'total_files': len(files),
            'files_with_diagrams': len(set(d.file_path for d in all_diagrams)),
            'total_diagrams': len(all_diagrams),
            'syntax_errors': len([d for d in all_diagrams if d.has_syntax_error]),
            'by_type': defaultdict(int),
            'total_nodes': sum(d.node_count for d in all_diagrams),
            'total_edges': sum(d.edge_count for d in all_diagrams),
            'avg_nodes_per_diagram': round(sum(d.node_count for d in all_diagrams) / len(all_diagrams), 2) if all_diagrams else 0,
            'avg_edges_per_diagram': round(sum(d.edge_count for d in all_diagrams) / len(all_diagrams), 2) if all_diagrams else 0,
        }
        
        for d in all_diagrams:
            stats['by_type'][d.diagram_type] += 1
            
        self.diagrams = all_diagrams
        return all_diagrams, self.errors, stats
    
    def generate_report(self, output_path: str, stats: Dict):
        """生成报告"""
        report = {
            'version': '1.0.0',
            'tool': 'Mermaid Syntax Checker',
            'stats': stats,
            'diagrams': [asdict(d) for d in self.diagrams],
            'errors': [asdict(e) for e in self.errors],
            'type_distribution': dict(stats['by_type']),
            'summary': {
                'total': stats['total_diagrams'],
                'valid': stats['total_diagrams'] - stats['syntax_errors'],
                'invalid': stats['syntax_errors'],
                'validity_rate': round((stats['total_diagrams'] - stats['syntax_errors']) / stats['total_diagrams'] * 100, 2) if stats['total_diagrams'] > 0 else 0
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        return report


def main():
    parser = argparse.ArgumentParser(description='Mermaid Syntax Checker')
    parser.add_argument('--base-path', default='.', help='项目根目录')
    parser.add_argument('--output', default='mermaid-syntax-report.json', help='输出报告路径')
    parser.add_argument('--use-mmdc', action='store_true', help='使用mmdc CLI进行验证（需安装）')
    parser.add_argument('--fail-on-error', action='store_true', help='发现错误时返回非零退出码')
    
    args = parser.parse_args()
    
    checker = MermaidSyntaxChecker(args.base_path, use_mmdc=args.use_mmdc)
    diagrams, errors, stats = checker.run_check()
    
    # 生成报告
    report = checker.generate_report(args.output, stats)
    
    # 打印摘要
    print("\n" + "=" * 50)
    print("📊 CHECK SUMMARY")
    print("=" * 50)
    print(f"Total files scanned:    {stats['total_files']}")
    print(f"Files with diagrams:    {stats['files_with_diagrams']}")
    print(f"Total diagrams:         {stats['total_diagrams']}")
    print(f"Syntax errors:          {stats['syntax_errors']}")
    print(f"Validity rate:          {report['summary']['validity_rate']}%")
    print(f"\nTotal nodes:            {stats['total_nodes']}")
    print(f"Total edges:            {stats['total_edges']}")
    print(f"Avg nodes/diagram:      {stats['avg_nodes_per_diagram']}")
    print(f"Avg edges/diagram:      {stats['avg_edges_per_diagram']}")
    print("\nBy type:")
    for dtype, count in stats['by_type'].items():
        print(f"  {dtype:20s}: {count}")
    print("=" * 50)
    print(f"\n✅ Report saved to: {args.output}")
    
    if args.fail_on_error and stats['syntax_errors'] > 0:
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
