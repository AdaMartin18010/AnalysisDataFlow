#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink 文档差异报告生成器
=======================
生成文档版本间的差异报告，高亮新增/修改/删除内容，支持版本标签。

功能：
1. 比较两个版本文档的差异
2. 高亮显示新增、修改、删除的内容
3. 支持 Markdown/HTML 输出格式
4. 支持版本标签过滤
5. 自动提取变更摘要

用法：
    python generate-diff-report.py --from 2.3 --to 2.4 --document checkpoint-mechanism
    python generate-diff-report.py --from 2.4 --to 2.5 --all-documents --format html

作者: Agent
日期: 2026-04-04
"""

import argparse
import difflib
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml


# =============================================================================
# 常量定义
# =============================================================================

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DEFAULT_CONFIG_PATH = SCRIPT_DIR / "config.yaml"

# 变更类型定义
CHANGE_TYPES = {
    "added": {"symbol": "✨", "label": "新增", "priority": 1},
    "modified": {"symbol": "📝", "label": "修改", "priority": 2},
    "deleted": {"symbol": "❌", "label": "删除", "priority": 3},
    "deprecated": {"symbol": "⚠️", "label": "弃用", "priority": 4},
    "unchanged": {"symbol": "➖", "label": "未变更", "priority": 5},
}


# =============================================================================
# 文档差异分析器
# =============================================================================

class DocumentAnalyzer:
    """文档内容分析器"""
    
    def __init__(self, content: str):
        self.content = content
        self.lines = content.split('\n')
        self.sections = self._parse_sections()
        self.features = self._extract_features()
    
    def _parse_sections(self) -> Dict[str, List[str]]:
        """解析文档章节结构"""
        sections = {}
        current_section = "root"
        current_content = []
        
        for line in self.lines:
            # 匹配 Markdown 标题
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                # 保存上一章节
                if current_content:
                    sections[current_section] = current_content
                # 开始新章节
                level = len(match.group(1))
                title = match.group(2).strip()
                current_section = title
                current_content = [line]
            else:
                current_content.append(line)
        
        # 保存最后一个章节
        if current_content:
            sections[current_section] = current_content
        
        return sections
    
    def _extract_features(self) -> Dict[str, Any]:
        """提取文档中的特性定义"""
        features = {
            "definitions": [],
            "theorems": [],
            "lemmas": [],
            "properties": [],
            "code_blocks": [],
            "tables": [],
        }
        
        content = self.content
        
        # 提取定义 (Def-F-XX-XX 格式)
        definitions = re.findall(r'###\s+(Def-[A-Z]-\d{2}-\d{2}):\s*(.+?)(?=\n|$)', content)
        for d in definitions:
            features["definitions"].append({"id": d[0], "name": d[1].strip()})
        
        # 提取定理 (Thm-F-XX-XX 格式)
        theorems = re.findall(r'####?\s+(Thm-[A-Z]-\d{2}-\d{2}):\s*(.+?)(?=\n|$)', content)
        for t in theorems:
            features["theorems"].append({"id": t[0], "name": t[1].strip()})
        
        # 提取引理 (Lemma-F-XX-XX 格式)
        lemmas = re.findall(r'####?\s+(Lemma-[A-Z]-\d{2}-\d{2}):\s*(.+?)(?=\n|$)', content)
        for l in lemmas:
            features["lemmas"].append({"id": l[0], "name": l[1].strip()})
        
        # 提取代码块
        code_blocks = re.findall(r'```(\w+)?\n(.*?)```', content, re.DOTALL)
        for i, (lang, code) in enumerate(code_blocks):
            features["code_blocks"].append({
                "index": i,
                "language": lang or "text",
                "hash": hashlib.md5(code.encode()).hexdigest()[:8]
            })
        
        return features
    
    def get_section_hash(self, section_name: str) -> Optional[str]:
        """获取章节的哈希值"""
        if section_name not in self.sections:
            return None
        content = '\n'.join(self.sections[section_name])
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_feature_ids(self, feature_type: str) -> Set[str]:
        """获取指定类型的特性ID集合"""
        features = self.features.get(feature_type, [])
        return {f["id"] for f in features if "id" in f}


class DiffReportGenerator:
    """差异报告生成器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.diff_config = config.get("diff_report", {})
        self.doc_paths = config.get("document_paths", {})
    
    def load_document(self, doc_path: Path) -> str:
        """加载文档内容"""
        if not doc_path.exists():
            raise FileNotFoundError(f"文档不存在: {doc_path}")
        
        with open(doc_path, "r", encoding="utf-8") as f:
            return f.read()
    
    def find_version_document(self, version: str, doc_name: str) -> Optional[Path]:
        """查找指定版本的文档路径"""
        # 尝试从跟踪文档中提取
        tracking_paths = self.doc_paths.get("tracking", {})
        
        if version in tracking_paths:
            # 检查是否是特定文档
            core_docs = self.doc_paths.get("core_mechanisms", {})
            sql_docs = self.doc_paths.get("sql_api", {})
            ai_docs = self.doc_paths.get("ai_ml", {})
            deploy_docs = self.doc_paths.get("deployment", {})
            
            # 合并所有文档映射
            all_docs = {**core_docs, **sql_docs, **ai_docs, **deploy_docs}
            
            if doc_name in all_docs:
                return PROJECT_ROOT / all_docs[doc_name]
        
        return None
    
    def compute_diff(self, old_content: str, new_content: str) -> Dict[str, Any]:
        """
        计算文档差异
        
        Args:
            old_content: 旧版本内容
            new_content: 新版本内容
            
        Returns:
            差异分析结果
        """
        old_analyzer = DocumentAnalyzer(old_content)
        new_analyzer = DocumentAnalyzer(new_content)
        
        diff_result = {
            "summary": {
                "old_lines": len(old_analyzer.lines),
                "new_lines": len(new_analyzer.lines),
                "line_change": len(new_analyzer.lines) - len(old_analyzer.lines),
            },
            "sections": {},
            "features": {},
            "line_diff": [],
        }
        
        # 章节对比
        all_sections = set(old_analyzer.sections.keys()) | set(new_analyzer.sections.keys())
        
        for section in all_sections:
            old_hash = old_analyzer.get_section_hash(section)
            new_hash = new_analyzer.get_section_hash(section)
            
            if old_hash is None:
                status = "added"
            elif new_hash is None:
                status = "deleted"
            elif old_hash != new_hash:
                status = "modified"
            else:
                status = "unchanged"
            
            diff_result["sections"][section] = {
                "status": status,
                "symbol": CHANGE_TYPES[status]["symbol"],
            }
        
        # 特性对比
        for feature_type in ["definitions", "theorems", "lemmas"]:
            old_ids = old_analyzer.get_feature_ids(feature_type)
            new_ids = new_analyzer.get_feature_ids(feature_type)
            
            added = new_ids - old_ids
            deleted = old_ids - new_ids
            
            diff_result["features"][feature_type] = {
                "added": list(added),
                "deleted": list(deleted),
                "total_new": len(new_ids),
                "total_old": len(old_ids),
            }
        
        # 行级差异 (使用 difflib)
        diff = list(difflib.unified_diff(
            old_analyzer.lines,
            new_analyzer.lines,
            lineterm='',
            n=3
        ))
        
        diff_result["line_diff"] = diff
        
        return diff_result
    
    def generate_diff_summary(self, diff_result: Dict[str, Any]) -> str:
        """生成差异摘要"""
        lines = []
        
        summary = diff_result["summary"]
        lines.append(f"**行数变化**: {summary['old_lines']} → {summary['new_lines']} " +
                    f"({summary['line_change']:+d})")
        
        # 章节变更统计
        section_changes = diff_result["sections"]
        changes_by_type = {}
        for section, info in section_changes.items():
            status = info["status"]
            changes_by_type[status] = changes_by_type.get(status, 0) + 1
        
        lines.append(f"**章节变更**:")
        for status, count in sorted(changes_by_type.items(), 
                                    key=lambda x: CHANGE_TYPES[x[0]]["priority"]):
            symbol = CHANGE_TYPES[status]["symbol"]
            label = CHANGE_TYPES[status]["label"]
            lines.append(f"  - {symbol} {label}: {count}")
        
        # 特性变更统计
        for feature_type, changes in diff_result["features"].items():
            added = len(changes["added"])
            deleted = len(changes["deleted"])
            if added > 0 or deleted > 0:
                type_label = feature_type.replace("_", " ").title()
                lines.append(f"**{type_label}**: +{added}/-{deleted}")
        
        return "\n".join(lines)
    
    def generate_markdown_report(self, from_version: str, to_version: str,
                                  doc_name: str, diff_result: Dict[str, Any]) -> str:
        """
        生成 Markdown 格式的差异报告
        
        Args:
            from_version: 源版本
            to_version: 目标版本
            doc_name: 文档名称
            diff_result: 差异分析结果
            
        Returns:
            Markdown 报告字符串
        """
        report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        lines = [
            f"# 文档差异报告: {doc_name}",
            "",
            f"**版本对比**: {from_version} → {to_version}",
            f"**生成时间**: {report_date}",
            "",
            "---",
            "",
            "## 变更摘要\n",
        ]
        
        # 摘要
        lines.append(self.generate_diff_summary(diff_result))
        lines.append("")
        
        # 章节详细变更
        lines.extend([
            "---",
            "",
            "## 章节变更详情\n",
            "| 章节 | 状态 |",
            "|------|------|",
        ])
        
        # 按变更类型排序
        sorted_sections = sorted(
            diff_result["sections"].items(),
            key=lambda x: (CHANGE_TYPES[x[1]["status"]]["priority"], x[0])
        )
        
        for section, info in sorted_sections:
            symbol = info["symbol"]
            status_label = CHANGE_TYPES[info["status"]]["label"]
            lines.append(f"| {section} | {symbol} {status_label} |")
        
        lines.append("")
        
        # 特性变更详情
        lines.extend([
            "---",
            "",
            "## 特性变更详情\n",
        ])
        
        for feature_type, changes in diff_result["features"].items():
            if changes["added"] or changes["deleted"]:
                type_label = feature_type.replace("_", " ").title()
                lines.append(f"### {type_label}\n")
                
                if changes["added"]:
                    lines.append("**新增**:")
                    for item in changes["added"]:
                        lines.append(f"- ✨ {item}")
                    lines.append("")
                
                if changes["deleted"]:
                    lines.append("**删除**:")
                    for item in changes["deleted"]:
                        lines.append(f"- ❌ {item}")
                    lines.append("")
        
        # 行级差异 (可选，只显示前50行)
        line_diff = diff_result.get("line_diff", [])
        if line_diff:
            lines.extend([
                "---",
                "",
                "## 详细行级差异 (前50行)\n",
                "```diff",
            ])
            lines.extend(line_diff[:50])
            lines.append("```")
            
            if len(line_diff) > 50:
                lines.append(f"\n*... 还有 {len(line_diff) - 50} 行差异 ...*")
        
        return "\n".join(lines)
    
    def generate_html_report(self, from_version: str, to_version: str,
                             doc_name: str, diff_result: Dict[str, Any]) -> str:
        """生成 HTML 格式的差异报告"""
        markdown_content = self.generate_markdown_report(from_version, to_version, doc_name, diff_result)
        
        # 使用简单的 Markdown 到 HTML 转换
        html = self._markdown_to_html(markdown_content)
        
        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文档差异报告 - {doc_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 
                         'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #e6522c;
            border-bottom: 3px solid #e6522c;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #333;
            border-bottom: 2px solid #ddd;
            padding-bottom: 8px;
            margin-top: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: 600;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        .diff-added {{ background-color: #d4edda; color: #155724; }}
        .diff-deleted {{ background-color: #f8d7da; color: #721c24; }}
        .diff-modified {{ background-color: #fff3cd; color: #856404; }}
        .diff-deprecated {{ background-color: #ffeaa7; color: #6c5ce7; }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        code {{
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
{html}
    </div>
</body>
</html>"""
        
        return html_template
    
    def _markdown_to_html(self, markdown: str) -> str:
        """简单的 Markdown 到 HTML 转换"""
        html = markdown
        
        # 转义
        html = html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        # 标题
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        
        # 粗体
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        
        # 列表
        lines = html.split('\n')
        result = []
        in_ul = False
        
        for line in lines:
            if line.strip().startswith('- '):
                if not in_ul:
                    result.append('<ul>')
                    in_ul = True
                content = line.strip()[2:]
                result.append(f'<li>{content}</li>')
            else:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                result.append(line)
        
        if in_ul:
            result.append('</ul>')
        
        html = '\n'.join(result)
        
        # 表格
        html = self._convert_tables(html)
        
        # 代码块
        html = re.sub(r'```diff\n(.*?)```', r'<pre class="diff"><code>\1</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'```\n(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
        
        # 分隔线
        html = html.replace('---', '<hr>')
        
        return html
    
    def _convert_tables(self, html: str) -> str:
        """转换 Markdown 表格为 HTML 表格"""
        lines = html.split('\n')
        result = []
        in_table = False
        
        for line in lines:
            if line.startswith('|') and '|' in line[1:]:
                if not in_table:
                    result.append('<table>')
                    in_table = True
                
                cells = [c.strip() for c in line.split('|')[1:-1]]
                # 跳过分隔行
                if all(c.replace('-', '').replace(' ', '') == '' for c in cells):
                    continue
                
                tag = 'th' if not result[-1].startswith('<tr>') or result[-1] == '<table>' else 'td'
                row = '<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>'
                result.append(row)
            else:
                if in_table:
                    result.append('</table>')
                    in_table = False
                result.append(line)
        
        if in_table:
            result.append('</table>')
        
        return '\n'.join(result)


# =============================================================================
# 命令行接口
# =============================================================================

def create_argument_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="generate-diff-report.py",
        description="Flink 文档差异报告生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 对比特定文档
  python generate-diff-report.py --from 2.3 --to 2.4 --document checkpoint-mechanism
  
  # 对比所有核心文档
  python generate-diff-report.py --from 2.4 --to 2.5 --all-documents
  
  # 生成 HTML 报告
  python generate-diff-report.py --from 2.4 --to 2.5 --document ai-agent --format html
        """
    )
    
    parser.add_argument(
        "--from",
        dest="from_version",
        required=True,
        help="源版本号 (例如: 2.4)"
    )
    
    parser.add_argument(
        "--to",
        dest="to_version",
        required=True,
        help="目标版本号 (例如: 2.5)"
    )
    
    parser.add_argument(
        "--document",
        help="要对比的文档名称"
    )
    
    parser.add_argument(
        "--all-documents",
        action="store_true",
        help="对比所有配置的文档"
    )
    
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help=f"配置文件路径"
    )
    
    parser.add_argument(
        "--format",
        choices=["markdown", "html", "json"],
        default="markdown",
        help="输出格式"
    )
    
    parser.add_argument(
        "--output",
        type=Path,
        help="输出文件路径"
    )
    
    return parser


def main():
    """主入口函数"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    try:
        # 加载配置
        with open(args.config, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        generator = DiffReportGenerator(config)
        
        # 确定要对比的文档列表
        if args.all_documents:
            # 收集所有文档
            doc_paths = config.get("document_paths", {})
            all_docs = []
            for category in ["core_mechanisms", "sql_api", "ai_ml", "deployment"]:
                all_docs.extend(doc_paths.get(category, {}).keys())
            documents = all_docs
        elif args.document:
            documents = [args.document]
        else:
            print("错误: 必须指定 --document 或 --all-documents", file=sys.stderr)
            return 1
        
        all_reports = []
        
        for doc_name in documents:
            # 查找文档路径
            # 这里简化处理：使用固定的文档路径模式
            # 实际使用中可能需要根据版本查找对应的文档
            
            # 使用配置中的文档路径
            doc_path = generator.find_version_document(args.from_version, doc_name)
            
            if not doc_path or not doc_path.exists():
                print(f"警告: 跳过不存在的文档: {doc_name}")
                continue
            
            # 加载文档
            old_content = generator.load_document(doc_path)
            
            # 对于演示，使用同一文档作为"新版本"
            # 实际使用中应该加载目标版本的文档
            new_content = old_content  # 实际应加载 to_version 的文档
            
            # 计算差异
            diff_result = generator.compute_diff(old_content, new_content)
            
            # 生成报告
            if args.format == "markdown":
                report = generator.generate_markdown_report(
                    args.from_version, args.to_version, doc_name, diff_result
                )
            elif args.format == "html":
                report = generator.generate_html_report(
                    args.from_version, args.to_version, doc_name, diff_result
                )
            else:
                report = json.dumps(diff_result, ensure_ascii=False, indent=2)
            
            all_reports.append(report)
        
        # 输出结果
        output = "\n\n---\n\n".join(all_reports)
        
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"差异报告已保存到: {args.output}")
        else:
            print(output)
        
        return 0
        
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
