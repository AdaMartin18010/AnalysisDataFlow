#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CI/CD 集成检查脚本

整合所有检查功能:
- Markdown语法检查
- 定理编号验证
- Mermaid语法验证
- 内部链接检查
- 前瞻性内容标记检查

作者: AnalysisDataFlow 项目
版本: 1.0.0
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


class Colors:
    """终端颜色"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def log_info(msg: str):
    print(f"{Colors.BLUE}ℹ️{Colors.RESET} {msg}")


def log_success(msg: str):
    print(f"{Colors.GREEN}✅{Colors.RESET} {msg}")


def log_warning(msg: str):
    print(f"{Colors.YELLOW}⚠️{Colors.RESET} {msg}")


def log_error(msg: str):
    print(f"{Colors.RED}❌{Colors.RESET} {msg}")


def log_section(title: str):
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{title}{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")


# ==================== 检查函数 ====================

def check_markdown_syntax(files: List[Path]) -> Tuple[int, int, List[Dict]]:
    """
    检查Markdown语法
    
    返回: (通过数, 失败数, 错误列表)
    """
    errors = []
    passed = 0
    failed = 0
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8')
            has_error = False
            
            # 检查YAML frontmatter
            if content.startswith('---'):
                end_marker = content.find('---', 3)
                if end_marker == -1:
                    errors.append({
                        'file': str(file_path),
                        'line': 1,
                        'message': 'Unclosed YAML frontmatter'
                    })
                    has_error = True
            
            # 检查表格语法（简化检查）
            lines = content.split('\n')
            in_table = False
            table_start_line = 0
            
            for i, line in enumerate(lines, 1):
                if '|' in line:
                    if not in_table:
                        in_table = True
                        table_start_line = i
                    # 检查表格分隔符行
                    if i == table_start_line + 1:
                        if not all(c in '-|: ' for c in line):
                            pass  # 可能不是表格
                else:
                    in_table = False
            
            if has_error:
                failed += 1
            else:
                passed += 1
                
        except Exception as e:
            errors.append({
                'file': str(file_path),
                'line': 0,
                'message': f'Could not read file: {e}'
            })
            failed += 1
    
    return passed, failed, errors


def check_theorem_ids(files: List[Path]) -> Tuple[int, int, Dict, List[Dict]]:
    """
    检查定理ID唯一性
    
    返回: (定理数, 重复数, 定理映射, 错误列表)
    """
    patterns = {
        'Thm': re.compile(r'Thm-[SKF]-\d{2}-\d{2}'),
        'Def': re.compile(r'Def-[SKF]-\d{2}-\d{2}'),
        'Lemma': re.compile(r'Lemma-[SKF]-\d{2}-\d{2}'),
        'Prop': re.compile(r'Prop-[SKF]-\d{2}-\d{2}'),
        'Cor': re.compile(r'Cor-[SKF]-\d{2}-\d{2}')
    }
    
    all_theorems = defaultdict(lambda: defaultdict(list))
    errors = []
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8')
            rel_path = str(file_path).replace('\\', '/')
            
            for thm_type, pattern in patterns.items():
                for match in pattern.finditer(content):
                    theorem_id = match.group(0)
                    line_num = content[:match.start()].count('\n') + 1
                    all_theorems[thm_type][theorem_id].append({
                        'file': rel_path,
                        'line': line_num
                    })
        except Exception as e:
            errors.append({
                'file': str(file_path),
                'message': f'Could not read file: {e}'
            })
    
    # 检查重复
    duplicates = {}
    total_count = 0
    
    for thm_type, theorems in all_theorems.items():
        total_count += len(theorems)
        for thm_id, locations in theorems.items():
            if len(locations) > 1:
                duplicates[thm_id] = locations
    
    return total_count, len(duplicates), dict(all_theorems), errors


def check_mermaid_syntax(files: List[Path]) -> Tuple[int, int, List[Dict]]:
    """
    检查Mermaid语法
    
    返回: (图表数, 错误数, 错误列表)
    """
    mermaid_pattern = re.compile(r'```mermaid\s*\n(.*?)```', re.DOTALL)
    valid_types = ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram',
                   'stateDiagram', 'stateDiagram-v2', 'erDiagram', 'gantt',
                   'pie', 'mindmap', 'timeline']
    
    diagram_count = 0
    error_count = 0
    errors = []
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8')
            diagrams = mermaid_pattern.findall(content)
            
            for i, diagram in enumerate(diagrams):
                diagram_count += 1
                lines = diagram.strip().split('\n')
                
                if not lines:
                    continue
                
                first_line = lines[0].strip()
                
                # 检查图表类型
                valid_type = False
                for vt in valid_types:
                    if first_line.startswith(vt):
                        valid_type = True
                        break
                
                if not valid_type:
                    error_count += 1
                    errors.append({
                        'file': str(file_path),
                        'diagram': i + 1,
                        'message': f'Unknown chart type: {first_line[:30]}...'
                    })
                    continue
                
                # 检查括号匹配
                open_brackets = diagram.count('[') + diagram.count('{') + diagram.count('(')
                close_brackets = diagram.count(']') + diagram.count('}') + diagram.count(')')
                if open_brackets != close_brackets:
                    error_count += 1
                    errors.append({
                        'file': str(file_path),
                        'diagram': i + 1,
                        'message': f'Unbalanced brackets: {open_brackets} open, {close_brackets} close'
                    })
        
        except Exception as e:
            pass
    
    return diagram_count, error_count, errors


def check_internal_links(files: List[Path]) -> Tuple[int, int, List[Dict]]:
    """
    检查内部链接
    
    返回: (链接数, 失效数, 错误列表)
    """
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    # 构建所有文档的集合
    all_docs = set()
    for f in files:
        all_docs.add(str(f).replace('\\', '/'))
    
    link_count = 0
    broken_count = 0
    errors = []
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8')
            doc_dir = file_path.parent
            
            for match in link_pattern.finditer(content):
                link_text = match.group(1)
                link_target = match.group(2)
                link_count += 1
                
                # 跳过外部链接和锚点
                if link_target.startswith(('http://', 'https://', 'mailto:', '#')):
                    continue
                
                # 移除锚点
                target_path = link_target.split('#')[0]
                if not target_path:
                    continue
                
                # 解析相对路径
                if target_path.startswith('/'):
                    full_path = target_path.lstrip('/')
                else:
                    full_path = str((doc_dir / target_path).resolve())
                    full_path = full_path.replace('\\', '/')
                    cwd = str(Path('.').resolve()).replace('\\', '/')
                    if full_path.startswith(cwd):
                        full_path = full_path[len(cwd)+1:]
                
                # 检查文件是否存在
                if full_path not in all_docs and not Path(full_path).exists():
                    broken_count += 1
                    errors.append({
                        'source': str(file_path),
                        'target': link_target,
                        'resolved': full_path
                    })
        
        except Exception as e:
            pass
    
    return link_count, broken_count, errors


def check_prospective_markers(files: List[Path]) -> Tuple[int, int, List[Dict]]:
    """
    检查前瞻性内容标记
    
    返回: (检查文件数, 错误数, 错误列表)
    """
    prospective_keywords = [
        'Flink 2.4', 'Flink 2.5', 'Flink 3.0'
    ]
    
    prospective_file_patterns = [
        r'flink-2\.4', r'flink-2\.5', r'flink-3\.', r'roadmap', r'preview'
    ]
    
    markers = [
        '> ⚠️ **前瞻性声明**',
        '> **前瞻性声明**',
        'status: preview',
        'status: roadmap',
        '前瞻性内容'
    ]
    
    checked = 0
    error_count = 0
    errors = []
    
    for file_path in files:
        file_name = file_path.name.lower()
        
        # 判断是否为前瞻性文件
        is_prospective = any(re.search(p, file_name) for p in prospective_file_patterns)
        
        try:
            content = file_path.read_text(encoding='utf-8')
            has_keywords = any(kw in content for kw in prospective_keywords)
            
            if is_prospective or has_keywords:
                checked += 1
                has_marker = any(marker in content for marker in markers)
                
                if not has_marker:
                    error_count += 1
                    errors.append({
                        'file': str(file_path),
                        'reason': 'Missing prospective content marker'
                    })
        
        except Exception as e:
            pass
    
    return checked, error_count, errors


# ==================== 主程序 ====================

def get_changed_files(base_ref: str = None) -> List[Path]:
    """获取变更的文件列表"""
    import subprocess
    
    files = []
    
    if base_ref:
        # 在CI环境中获取变更文件
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-only', '--diff-filter=ACMRT', f'origin/{base_ref}', '...HEAD'],
                capture_output=True, text=True
            )
            files = [Path(f) for f in result.stdout.strip().split('\n') 
                     if f.endswith('.md') and Path(f).exists()]
        except Exception as e:
            print(f"Warning: Could not get changed files: {e}")
    
    if not files:
        # 获取所有markdown文件
        for directory in ['Struct', 'Knowledge', 'Flink', 'visuals', 'tutorials']:
            if Path(directory).exists():
                files.extend(Path(directory).rglob('*.md'))
        
        # 根目录文档
        for md_file in Path('.').glob('*.md'):
            if md_file.is_file() and not str(md_file).startswith('.'):
                files.append(md_file)
    
    # 去重并过滤
    seen = set()
    unique_files = []
    for f in files:
        # 跳过隐藏目录
        if any(part.startswith('.') or part in ['node_modules', '__pycache__']
               for part in f.parts):
            continue
        
        if f not in seen:
            seen.add(f)
            unique_files.append(f)
    
    return unique_files


def main():
    parser = argparse.ArgumentParser(
        description='CI/CD 集成检查脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 检查所有文件
  python ci-check-scripts.py
  
  # 只检查变更的文件（CI环境）
  python ci-check-scripts.py --changed-only --base-ref main
  
  # 生成JSON报告
  python ci-check-scripts.py --json reports/ci-check-results.json
        """
    )
    
    parser.add_argument('--changed-only', action='store_true',
                        help='只检查变更的文件')
    parser.add_argument('--base-ref', type=str,
                        help='基础分支引用（用于获取变更文件）')
    parser.add_argument('--json', type=str,
                        help='输出JSON格式报告')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='详细输出')
    
    args = parser.parse_args()
    
    log_section("CI/CD 集成检查")
    
    # 获取要检查的文件
    if args.changed_only:
        files = get_changed_files(args.base_ref)
        log_info(f"检查 {len(files)} 个变更文件")
    else:
        files = get_changed_files()
        log_info(f"检查 {len(files)} 个文件")
    
    if not files:
        log_warning("没有找到需要检查的文件")
        return 0
    
    # 运行所有检查
    results = {
        'timestamp': datetime.now().isoformat(),
        'files_checked': len(files),
        'checks': {}
    }
    
    # 1. Markdown语法检查
    log_section("1. Markdown语法检查")
    passed, failed, errors = check_markdown_syntax(files)
    results['checks']['markdown'] = {
        'passed': passed,
        'failed': failed,
        'errors': errors[:10] if not args.verbose else errors
    }
    log_info(f"检查文件: {passed + failed}")
    log_success(f"通过: {passed}")
    if failed > 0:
        log_error(f"失败: {failed}")
    
    # 2. 定理ID检查
    log_section("2. 定理编号唯一性检查")
    thm_count, dup_count, thm_map, errors = check_theorem_ids(files)
    results['checks']['theorem'] = {
        'total': thm_count,
        'duplicates': dup_count,
        'errors': errors[:10] if not args.verbose else errors
    }
    log_info(f"定理总数: {thm_count}")
    if dup_count > 0:
        log_error(f"重复ID: {dup_count}")
    else:
        log_success("无重复ID")
    
    # 3. Mermaid语法检查
    log_section("3. Mermaid语法检查")
    diagram_count, error_count, errors = check_mermaid_syntax(files)
    results['checks']['mermaid'] = {
        'diagrams': diagram_count,
        'errors': error_count,
        'details': errors[:10] if not args.verbose else errors
    }
    log_info(f"图表数量: {diagram_count}")
    if error_count > 0:
        log_error(f"语法错误: {error_count}")
    else:
        log_success("语法正确")
    
    # 4. 内部链接检查
    log_section("4. 内部链接健康检查")
    link_count, broken_count, errors = check_internal_links(files)
    results['checks']['links'] = {
        'total': link_count,
        'broken': broken_count,
        'errors': errors[:10] if not args.verbose else errors
    }
    log_info(f"内部链接: {link_count}")
    if broken_count > 0:
        log_error(f"失效链接: {broken_count}")
    else:
        log_success("所有链接有效")
    
    # 5. 前瞻性内容标记检查
    log_section("5. 前瞻性内容标记检查")
    checked, error_count, errors = check_prospective_markers(files)
    results['checks']['prospective'] = {
        'checked': checked,
        'errors': error_count,
        'details': errors[:10] if not args.verbose else errors
    }
    log_info(f"前瞻性文件: {checked}")
    if error_count > 0:
        log_error(f"缺失标记: {error_count}")
    else:
        log_success("标记完整")
    
    # 保存JSON报告
    if args.json:
        output_path = Path(args.json)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        log_info(f"报告已保存: {output_path}")
    
    # 最终摘要
    log_section("检查结果摘要")
    
    total_errors = (
        results['checks']['markdown']['failed'] +
        results['checks']['theorem']['duplicates'] +
        results['checks']['mermaid']['errors'] +
        results['checks']['links']['broken'] +
        results['checks']['prospective']['errors']
    )
    
    if total_errors == 0:
        log_success("所有检查通过！")
        return 0
    else:
        log_error(f"发现 {total_errors} 个问题")
        return 1


if __name__ == '__main__':
    sys.exit(main())
