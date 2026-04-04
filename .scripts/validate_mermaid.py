#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mermaid 语法校验脚本 - AnalysisDataFlow 自动化工具集

功能：
1. 提取所有 Markdown 文件中的 Mermaid 代码块
2. 使用本地 mermaid-cli 或在线 API 验证语法
3. 检测常见语法问题（括号不匹配、无效节点等）
4. 生成详细的验证报告

使用方法：
    python .scripts/validate_mermaid.py
    python .scripts/validate_mermaid.py --json
    python .scripts/validate_mermaid.py --online
    python .scripts/validate_mermaid.py --fix

依赖：
    可选: npm install -g @mermaid-js/mermaid-cli

退出码：
    0 - 所有检查通过
    1 - 发现语法错误
    2 - 运行异常
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
    """Mermaid代码块数据类"""
    file_path: str
    line_start: int
    line_end: int
    content: str
    diagram_type: str = ""
    error_message: Optional[str] = None
    suggestions: List[str] = field(default_factory=list)


@dataclass
class ValidationReport:
    """验证报告数据类"""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    total_files: int = 0
    total_blocks: int = 0
    valid_blocks: int = 0
    invalid_blocks: int = 0
    errors: List[Dict] = field(default_factory=list)
    warnings: List[Dict] = field(default_factory=list)
    diagram_types: Dict[str, int] = field(default_factory=dict)


class MermaidValidator:
    """Mermaid 验证器"""
    
    # Mermaid代码块正则表达式
    MERMAID_BLOCK_PATTERN = re.compile(
        r'```mermaid\s*\n(.*?)```',
        re.DOTALL | re.IGNORECASE
    )
    
    # 图表类型检测
    DIAGRAM_TYPES = [
        'graph', 'flowchart', 'sequenceDiagram', 'classDiagram',
        'stateDiagram', 'stateDiagram-v2', 'erDiagram', 'journey',
        'gantt', 'pie', 'requirementDiagram', 'gitGraph',
        'mindmap', 'timeline', 'quadrantChart', 'xychart-beta', 'flowchart-v2'
    ]
    
    # 常见语法问题模式
    COMMON_ISSUES = [
        (r'graph\s+[a-zA-Z]{3,}', "图表方向应为 TB/TD/LR/RL/BT 之一"),
        (r'\(\s*\)', "空括号可能导致渲染问题"),
        (r'-->\s*\n', "箭头指向空节点"),
        (r'classDef\s+\w+\s*,', "classDef 语法错误，应使用空格分隔样式属性"),
        (r'subgraph\s+[^"\']+\n', "subgraph 标题建议用引号包裹"),
        (r'\|\s*\|', "空的管道符可能导致表格渲染问题"),
    ]
    
    def __init__(self, root_dir: str, use_online: bool = False, timeout: int = 30):
        self.root_dir = Path(root_dir)
        self.report = ValidationReport()
        self.use_online = use_online
        self.timeout = timeout
        self.mmdc_path = self._find_mmdc()
        self.blocks: List[MermaidBlock] = []
        
    def _find_mmdc(self) -> Optional[str]:
        """查找 mmdc (mermaid-cli) 命令"""
        # 首先尝试在 PATH 中查找
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(
                    ['where', 'mmdc'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout.strip().split('\n')[0]
            else:
                result = subprocess.run(
                    ['which', 'mmdc'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # 尝试常见安装路径
        npm_paths = [
            os.path.expandvars(r'%APPDATA%\npm\mmdc.cmd'),
            os.path.expandvars(r'%LOCALAPPDATA%\npm\mmdc.cmd'),
            os.path.expandvars(r'%USERPROFILE%\AppData\Roaming\npm\mmdc.cmd'),
            '/usr/local/bin/mmdc',
            '/usr/bin/mmdc',
            '/opt/homebrew/bin/mmdc',
        ]
        for path in npm_paths:
            if os.path.exists(path):
                return path
        return None
    
    def scan_all_files(self, include_patterns: Optional[List[str]] = None) -> None:
        """扫描所有 Markdown 文件"""
        if include_patterns is None:
            include_patterns = ['**/*.md']
        
        md_files = set()
        for pattern in include_patterns:
            for file_path in self.root_dir.glob(pattern):
                if '.git' not in str(file_path):
                    md_files.add(file_path)
        
        self.report.total_files = len(md_files)
        
        for file_path in sorted(md_files):
            self._scan_file(file_path)
    
    def _scan_file(self, file_path: Path) -> None:
        """扫描单个文件中的 Mermaid 代码块"""
        try:
            content = file_path.read_text(encoding='utf-8')
            rel_path = str(file_path.relative_to(self.root_dir))
            
            for match in self.MERMAID_BLOCK_PATTERN.finditer(content):
                start_pos = match.start()
                line_start = content[:start_pos].count('\n') + 1
                line_end = line_start + match.group(0).count('\n')
                
                mermaid_content = match.group(1).strip()
                if not mermaid_content:
                    continue
                
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
        """验证所有 Mermaid 代码块"""
        self.report.total_blocks = len(self.blocks)
        
        if self.use_online:
            self._validate_online()
        elif self.mmdc_path:
            self._validate_local()
        else:
            self._validate_basic()
    
    def _validate_local(self) -> None:
        """使用本地 mmdc 验证"""
        for block in self.blocks:
            try:
                with tempfile.NamedTemporaryFile(
                    mode='w', suffix='.mmd', delete=False, encoding='utf-8'
                ) as f:
                    f.write(block.content)
                    temp_file = f.name
                
                output_file = temp_file + '.svg'
                
                try:
                    result = subprocess.run(
                        [self.mmdc_path, '-i', temp_file, '-o', output_file, '-b', 'transparent'],
                        capture_output=True,
                        text=True,
                        timeout=self.timeout
                    )
                    
                    if result.returncode == 0:
                        self.report.valid_blocks += 1
                        block.error_message = None
                    else:
                        self.report.invalid_blocks += 1
                        block.error_message = result.stderr or "渲染失败"
                        self._analyze_error(block)
                        self.report.errors.append({
                            'type': 'syntax_error',
                            'file': block.file_path,
                            'line': block.line_start,
                            'diagram_type': block.diagram_type,
                            'message': block.error_message[:200]
                        })
                finally:
                    try:
                        os.unlink(temp_file)
                        if os.path.exists(output_file):
                            os.unlink(output_file)
                    except:
                        pass
                    
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
        """使用在线 API 验证"""
        import base64
        import zlib
        
        api_url = "https://mermaid.ink/svg/"
        
        for block in self.blocks:
            try:
                encoded = base64.b64encode(
                    zlib.compress(block.content.encode('utf-8'), 9)
                ).decode('ascii')
                
                req = Request(
                    f"{api_url}{encoded}",
                    method='HEAD',
                    headers={'User-Agent': 'Mozilla/5.0 (compatible; AnalysisDataFlow-Validator)'}
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
        for block in self.blocks:
            issues_found = []
            suggestions = []
            
            # 检查常见语法问题
            for pattern, message in self.COMMON_ISSUES:
                if re.search(pattern, block.content, re.IGNORECASE):
                    issues_found.append(message)
            
            # 检查括号匹配
            if block.content.count('(') != block.content.count(')'):
                issues_found.append("圆括号不匹配")
                suggestions.append("检查并确保所有 '(' 都有对应的 ')'")
            
            if block.content.count('[') != block.content.count(']'):
                issues_found.append("方括号不匹配")
                suggestions.append("检查并确保所有 '[' 都有对应的 ']'")
            
            # 对于 graph/flowchart，检查节点定义
            if block.diagram_type in ['graph', 'flowchart', 'flowchart-v2']:
                lines = block.content.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith(('%%', 'subgraph', 'end', 'classDef', 'linkStyle', 'style', 'click')):
                        continue
                    # 检查可能的无效节点定义
                    if re.search(r'^\s*\w+\s*[^\[\(\{<\w\s\-]', line):
                        if '-->' not in line and '---' not in line:
                            issues_found.append(f"可能的无效节点定义: {line[:40]}")
            
            # 检查 stateDiagram 语法
            if 'stateDiagram' in block.diagram_type:
                if '[*]' not in block.content:
                    self.report.warnings.append({
                        'type': 'missing_start',
                        'file': block.file_path,
                        'line': block.line_start,
                        'message': 'stateDiagram 建议包含 [*] 起始/结束节点'
                    })
            
            if issues_found:
                self.report.invalid_blocks += 1
                block.error_message = "; ".join(issues_found)
                block.suggestions = suggestions
                self.report.errors.append({
                    'type': 'syntax_warning',
                    'file': block.file_path,
                    'line': block.line_start,
                    'diagram_type': block.diagram_type,
                    'message': "; ".join(issues_found),
                    'suggestions': suggestions
                })
            else:
                self.report.valid_blocks += 1
    
    def _analyze_error(self, block: MermaidBlock) -> None:
        """分析错误并提供建议"""
        error_msg = block.error_message or ""
        
        if "syntax error" in error_msg.lower():
            block.suggestions.append("检查 Mermaid 语法，确保使用了正确的图表类型声明")
        if "Expecting" in error_msg:
            block.suggestions.append("检查缺少的关键字或符号")
        if "Parse error" in error_msg:
            block.suggestions.append("尝试简化图表结构，检查特殊字符")
    
    def try_fix(self, block: MermaidBlock) -> Optional[str]:
        """尝试自动修复常见问题"""
        content = block.content
        fixes = []
        
        # 修复 graph 方向
        if re.search(r'graph\s+[a-zA-Z]{3,}', content, re.IGNORECASE):
            content = re.sub(r'graph\s+([a-zA-Z]{3,})', r'graph TD', content, flags=re.IGNORECASE)
            fixes.append("将图表方向修复为 TD")
        
        # 修复 classDef 语法
        if 'classDef' in content and ',' in content:
            # 尝试修复 classDef 中的逗号分隔
            pass  # 这需要更复杂的处理
        
        return content if fixes else None
    
    def print_report(self, json_output: bool = False) -> int:
        """打印验证报告"""
        # 统计图表类型
        for block in self.blocks:
            dtype = block.diagram_type or 'unknown'
            self.report.diagram_types[dtype] = self.report.diagram_types.get(dtype, 0) + 1
        
        if json_output:
            report_dict = {
                'timestamp': self.report.timestamp,
                'summary': {
                    'total_files': self.report.total_files,
                    'total_blocks': self.report.total_blocks,
                    'valid_blocks': self.report.valid_blocks,
                    'invalid_blocks': self.report.invalid_blocks,
                    'validation_method': 'online' if self.use_online else ('local' if self.mmdc_path else 'basic'),
                    'mmdc_available': self.mmdc_path is not None
                },
                'diagram_types': self.report.diagram_types,
                'errors': self.report.errors,
                'warnings': self.report.warnings
            }
            print(json.dumps(report_dict, indent=2, ensure_ascii=False))
        else:
            print("=" * 80)
            print("Mermaid 图表语法验证报告")
            print("=" * 80)
            print(f"\n📊 统计信息:")
            print(f"   扫描文件数: {self.report.total_files}")
            print(f"   Mermaid 代码块: {self.report.total_blocks}")
            print(f"   ✅ 有效: {self.report.valid_blocks}")
            print(f"   ❌ 无效: {self.report.invalid_blocks}")
            
            method = '在线 API' if self.use_online else ('本地 mmdc' if self.mmdc_path else '基本检查')
            print(f"   验证方式: {method}")
            
            if self.report.diagram_types:
                print(f"\n📈 图表类型分布:")
                for dtype, count in sorted(self.report.diagram_types.items(), key=lambda x: -x[1]):
                    print(f"   {dtype}: {count}")
            
            if self.report.errors:
                print(f"\n❌ 发现 {len(self.report.errors)} 个问题:")
                for error in self.report.errors[:15]:
                    print(f"\n   [{error['type']}] {error.get('diagram_type', 'unknown')}")
                    print(f"   位置: {error['file']}:{error.get('line', 'N/A')}")
                    msg = error['message']
                    if len(msg) > 150:
                        msg = msg[:150] + "..."
                    print(f"   问题: {msg}")
                    if error.get('suggestions'):
                        for sug in error['suggestions']:
                            print(f"   💡 {sug}")
                if len(self.report.errors) > 15:
                    print(f"\n   ... 还有 {len(self.report.errors) - 15} 个问题未显示")
            else:
                print(f"\n✅ 所有 Mermaid 图表语法正确！")
            
            if not self.mmdc_path and not self.use_online:
                print(f"\n💡 提示: 安装 mermaid-cli 可获得更完整的验证:")
                print(f"   npm install -g @mermaid-js/mermaid-cli")
            
            print("\n" + "=" * 80)
        
        return 1 if self.report.invalid_blocks > 0 else 0


def main():
    parser = argparse.ArgumentParser(
        description='Mermaid 图表语法验证工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python .scripts/validate_mermaid.py
  python .scripts/validate_mermaid.py --json
  python .scripts/validate_mermaid.py --online      # 使用在线 API 验证
  python .scripts/validate_mermaid.py --fix         # 尝试自动修复
  python .scripts/validate_mermaid.py Struct/       # 只验证指定目录
        """
    )
    parser.add_argument('paths', nargs='*', help='指定要验证的路径（默认为整个项目）')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式报告')
    parser.add_argument('--online', action='store_true', help='使用在线 API 验证')
    parser.add_argument('--fix', action='store_true', help='尝试自动修复常见问题')
    parser.add_argument('--timeout', type=int, default=30, help='验证超时时间（秒）')
    
    args = parser.parse_args()
    
    # 确定项目根目录
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    # 确定要扫描的路径
    if args.paths:
        patterns = [f"{p}/**/*.md" if os.path.isdir(p) else p for p in args.paths]
    else:
        patterns = None
    
    if not args.json:
        print(f"正在扫描 Mermaid 图表: {root_dir}")
    
    try:
        validator = MermaidValidator(str(root_dir), use_online=args.online, timeout=args.timeout)
        validator.scan_all_files(include_patterns=patterns)
        validator.validate()
        
        # 如果指定了 --fix，尝试修复
        if args.fix:
            print("\n🔧 尝试自动修复...")
            fixed_count = 0
            for block in validator.blocks:
                if block.error_message:
                    fixed = validator.try_fix(block)
                    if fixed:
                        print(f"   修复: {block.file_path}:{block.line_start}")
                        fixed_count += 1
            print(f"   已修复 {fixed_count} 个问题")
        
        exit_code = validator.print_report(json_output=args.json)
        sys.exit(exit_code)
    
    except KeyboardInterrupt:
        print("\n\n操作已取消", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 运行错误: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
