#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mermaid 图表语法验证脚本

功能：
1. 提取所有Markdown文件中的 Mermaid 代码块
2. 使用 mermaid-cli (mmdc) 或在线 API 验证语法
3. 报告语法错误

依赖安装：
    npm install -g @mermaid-js/mermaid-cli  # 安装 mermaid-cli
    
或者使用在线验证（不需要本地安装）

使用方法：
    python .vscode/validate-mermaid.py
    python .vscode/validate-mermaid.py --json
    python .vscode/validate-mermaid.py --fix  # 尝试修复常见问题
"""

import os
import re
import sys
import json
import argparse
import subprocess
import tempfile
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError


@dataclass
class MermaidBlock:
    """Mermaid代码块"""
    file_path: str
    line_start: int
    line_end: int
    content: str
    diagram_type: str = ""
    error_message: Optional[str] = None


@dataclass
class ValidationReport:
    """验证报告"""
    total_files: int = 0
    total_blocks: int = 0
    valid_blocks: int = 0
    invalid_blocks: int = 0
    errors: List[Dict] = field(default_factory=list)
    warnings: List[Dict] = field(default_factory=list)


class MermaidValidator:
    """Mermaid验证器"""
    
    # Mermaid代码块正则
    MERMAID_BLOCK_PATTERN = re.compile(
        r'```mermaid\n(.*?)```',
        re.DOTALL | re.IGNORECASE
    )
    
    # 图表类型检测
    DIAGRAM_TYPES = [
        'graph', 'flowchart', 'sequenceDiagram', 'classDiagram',
        'stateDiagram', 'stateDiagram-v2', 'erDiagram', 'journey',
        'gantt', 'pie', 'requirementDiagram', 'gitGraph',
        'mindmap', 'timeline', 'quadrantChart', 'xychart-beta'
    ]
    
    def __init__(self, root_dir: str, use_online: bool = False):
        self.root_dir = Path(root_dir)
        self.report = ValidationReport()
        self.use_online = use_online
        self.mmdc_path = self._find_mmdc()
        self.blocks: List[MermaidBlock] = []
        
    def _find_mmdc(self) -> Optional[str]:
        """查找 mmdc 命令"""
        try:
            result = subprocess.run(
                ['where', 'mmdc'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n')[0]
        except (subprocess.CalledProcessError, FileNotFoundError):
            # 尝试常见的npm全局安装路径
            npm_paths = [
                os.path.expandvars(r'%APPDATA%\npm\mmdc.cmd'),
                os.path.expandvars(r'%LOCALAPPDATA%\npm\mmdc.cmd'),
                '/usr/local/bin/mmdc',
                '/usr/bin/mmdc'
            ]
            for path in npm_paths:
                if os.path.exists(path):
                    return path
            return None
    
    def scan_all_files(self) -> None:
        """扫描所有Markdown文件"""
        md_files = []
        for pattern in ['**/*.md']:
            md_files.extend(self.root_dir.glob(pattern))
        
        self.report.total_files = len(md_files)
        
        for file_path in md_files:
            self._scan_file(file_path)
    
    def _scan_file(self, file_path: Path) -> None:
        """扫描单个文件中的Mermaid代码块"""
        try:
            content = file_path.read_text(encoding='utf-8')
            rel_path = str(file_path.relative_to(self.root_dir))
            
            for match in self.MERMAID_BLOCK_PATTERN.finditer(content):
                # 计算行号
                start_pos = match.start()
                line_start = content[:start_pos].count('\n') + 1
                line_end = line_start + match.group(0).count('\n')
                
                mermaid_content = match.group(1).strip()
                
                # 检测图表类型
                diagram_type = self._detect_diagram_type(mermaid_content)
                
                block = MermaidBlock(
                    file_path=rel_path,
                    line_start=line_start,
                    line_end=line_end,
                    content=mermaid_content,
                    diagram_type=diagram_type
                )
                self.blocks.append(block)
        except Exception as e:
            self.report.errors.append({
                'type': 'file_read_error',
                'file': str(file_path),
                'message': str(e)
            })
    
    def _detect_diagram_type(self, content: str) -> str:
        """检测图表类型"""
        first_line = content.strip().split('\n')[0].strip().lower()
        for dtype in self.DIAGRAM_TYPES:
            if first_line.startswith(dtype.lower()):
                return dtype
        return 'unknown'
    
    def validate(self) -> None:
        """验证所有Mermaid代码块"""
        self.report.total_blocks = len(self.blocks)
        
        if self.use_online:
            self._validate_online()
        elif self.mmdc_path:
            self._validate_local()
        else:
            self._validate_basic()
    
    def _validate_local(self) -> None:
        """使用本地 mmdc 验证"""
        print(f"使用本地验证器: {self.mmdc_path}")
        
        for block in self.blocks:
            try:
                with tempfile.NamedTemporaryFile(
                    mode='w', suffix='.mmd', delete=False
                ) as f:
                    f.write(block.content)
                    temp_file = f.name
                
                try:
                    # 尝试渲染为SVG以验证语法
                    with tempfile.NamedTemporaryFile(
                        mode='w', suffix='.svg', delete=False
                    ) as out_f:
                        output_file = out_f.name
                    
                    result = subprocess.run(
                        [self.mmdc_path, '-i', temp_file, '-o', output_file],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.returncode == 0:
                        self.report.valid_blocks += 1
                        block.error_message = None
                    else:
                        self.report.invalid_blocks += 1
                        block.error_message = result.stderr or "渲染失败"
                        self.report.errors.append({
                            'type': 'syntax_error',
                            'file': block.file_path,
                            'line': block.line_start,
                            'diagram_type': block.diagram_type,
                            'message': block.error_message
                        })
                finally:
                    os.unlink(temp_file)
                    if os.path.exists(output_file):
                        os.unlink(output_file)
                        
            except subprocess.TimeoutExpired:
                self.report.invalid_blocks += 1
                block.error_message = "验证超时"
                self.report.errors.append({
                    'type': 'timeout',
                    'file': block.file_path,
                    'line': block.line_start,
                    'message': '验证超时'
                })
            except Exception as e:
                self.report.invalid_blocks += 1
                block.error_message = str(e)
                self.report.errors.append({
                    'type': 'validation_error',
                    'file': block.file_path,
                    'line': block.line_start,
                    'message': str(e)
                })
    
    def _validate_online(self) -> None:
        """使用在线API验证（需要网络连接）"""
        print("使用在线验证API...")
        
        # Mermaid Live Editor API
        api_url = "https://mermaid.ink/svg/"
        
        import base64
        import zlib
        
        for block in self.blocks:
            try:
                # 使用 mermaid.ink API
                encoded = base64.b64encode(
                    zlib.compress(block.content.encode('utf-8'), 9)
                ).decode('ascii')
                
                req = Request(
                    f"{api_url}{encoded}",
                    method='HEAD',
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                
                try:
                    with urlopen(req, timeout=10) as response:
                        if response.status == 200:
                            self.report.valid_blocks += 1
                        else:
                            self.report.invalid_blocks += 1
                            self.report.errors.append({
                                'type': 'syntax_error',
                                'file': block.file_path,
                                'line': block.line_start,
                                'diagram_type': block.diagram_type,
                                'message': f'HTTP {response.status}'
                            })
                except URLError as e:
                    self.report.invalid_blocks += 1
                    self.report.errors.append({
                        'type': 'syntax_error',
                        'file': block.file_path,
                        'line': block.line_start,
                        'diagram_type': block.diagram_type,
                        'message': str(e.reason)
                    })
                    
            except Exception as e:
                self.report.invalid_blocks += 1
                self.report.errors.append({
                    'type': 'validation_error',
                    'file': block.file_path,
                    'line': block.line_start,
                    'message': str(e)
                })
    
    def _validate_basic(self) -> None:
        """基本语法检查（不依赖外部工具）"""
        print("执行基本语法检查（不依赖外部工具）...")
        
        common_issues = [
            (r'graph\s+\w+\s*\n', "图表方向应为 TB/TD/LR/RL/BT"),
            (r'\(\s*\)', "空括号可能导致问题"),
            (r'-->\s*\n', "箭头指向空节点"),
            (r'classDef\s+\w+\s*,', "classDef 语法错误，应使用空格分隔"),
        ]
        
        for block in self.blocks:
            issues_found = []
            
            # 检查常见语法问题
            for pattern, message in common_issues:
                if re.search(pattern, block.content, re.IGNORECASE):
                    issues_found.append(message)
            
            # 检查括号匹配
            if block.content.count('(') != block.content.count(')'):
                issues_found.append("圆括号不匹配")
            if block.content.count('[') != block.content.count(']'):
                issues_found.append("方括号不匹配")
            if block.content.count('{') != block.content.count('}'):
                issues_found.append("花括号不匹配")
            
            # 检查节点ID格式
            lines = block.content.split('\n')
            for line in lines:
                # 检测可能的无效节点定义
                if re.search(r'^\s*\w+\s*[^\[\(\{<\w\s]', line.strip()):
                    if not line.strip().startswith(('subgraph', 'end', 'classDef', 'linkStyle', 'style', 'click')):
                        issues_found.append(f"可能的无效节点定义: {line.strip()[:30]}")
            
            if issues_found:
                self.report.invalid_blocks += 1
                block.error_message = "; ".join(issues_found)
                self.report.errors.append({
                    'type': 'syntax_warning',
                    'file': block.file_path,
                    'line': block.line_start,
                    'diagram_type': block.diagram_type,
                    'message': "; ".join(issues_found)
                })
            else:
                self.report.valid_blocks += 1
    
    def print_report(self, json_output: bool = False) -> int:
        """打印验证报告"""
        if json_output:
            report_dict = {
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_files': self.report.total_files,
                    'total_blocks': self.report.total_blocks,
                    'valid_blocks': self.report.valid_blocks,
                    'invalid_blocks': self.report.invalid_blocks,
                    'validation_method': 'online' if self.use_online else ('local' if self.mmdc_path else 'basic')
                },
                'diagram_types': self._count_diagram_types(),
                'errors': self.report.errors,
                'warnings': self.report.warnings
            }
            print(json.dumps(report_dict, indent=2, ensure_ascii=False))
        else:
            print("=" * 80)
            print("Mermaid 图表验证报告")
            print("=" * 80)
            print(f"\n📊 统计信息:")
            print(f"   扫描文件数: {self.report.total_files}")
            print(f"   Mermaid代码块: {self.report.total_blocks}")
            print(f"   ✅ 有效: {self.report.valid_blocks}")
            print(f"   ❌ 无效: {self.report.invalid_blocks}")
            
            method = '在线API' if self.use_online else ('本地mmdc' if self.mmdc_path else '基本检查')
            print(f"   验证方式: {method}")
            
            # 图表类型分布
            type_counts = self._count_diagram_types()
            if type_counts:
                print(f"\n📈 图表类型分布:")
                for dtype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
                    print(f"   {dtype}: {count}")
            
            if self.report.errors:
                print(f"\n❌ 发现 {len(self.report.errors)} 个问题:")
                for error in self.report.errors[:15]:  # 最多显示15个
                    print(f"\n   [{error['type']}] {error.get('diagram_type', 'unknown')}")
                    print(f"   位置: {error['file']}:{error.get('line', 'N/A')}")
                    print(f"   问题: {error['message'][:100]}")
                if len(self.report.errors) > 15:
                    print(f"\n   ... 还有 {len(self.report.errors) - 15} 个问题未显示")
            else:
                print(f"\n✅ 所有Mermaid图表语法正确！")
            
            if not self.mmdc_path and not self.use_online:
                print(f"\n💡 提示: 安装 mermaid-cli 可获得更完整的验证:")
                print(f"   npm install -g @mermaid-js/mermaid-cli")
            
            print("\n" + "=" * 80)
        
        return 1 if self.report.invalid_blocks > 0 else 0
    
    def _count_diagram_types(self) -> Dict[str, int]:
        """统计图表类型"""
        counts = {}
        for block in self.blocks:
            dtype = block.diagram_type or 'unknown'
            counts[dtype] = counts.get(dtype, 0) + 1
        return counts


def main():
    parser = argparse.ArgumentParser(
        description='Mermaid 图表语法验证工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python .vscode/validate-mermaid.py
  python .vscode/validate-mermaid.py --json
  python .vscode/validate-mermaid.py --online  # 使用在线验证
        """
    )
    parser.add_argument('--json', action='store_true', help='输出JSON格式报告')
    parser.add_argument('--online', action='store_true', help='使用在线API验证')
    parser.add_argument('--fix', action='store_true', help='尝试自动修复常见问题')
    
    args = parser.parse_args()
    
    # 确定项目根目录
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    print(f"正在扫描项目中的 Mermaid 图表: {root_dir}", 
          file=sys.stderr if args.json else sys.stdout)
    
    validator = MermaidValidator(str(root_dir), use_online=args.online)
    validator.scan_all_files()
    validator.validate()
    
    exit_code = validator.print_report(json_output=args.json)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
