#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink 特性支持矩阵生成器
========================
自动从文档提取特性信息，生成特性支持矩阵可视化表格。

功能：
1. 从文档自动提取特性定义
2. 生成特性支持矩阵 (Markdown/HTML/CSV)
3. 支持多版本对比
4. 生成可视化图表 (Mermaid/ASCII)
5. 特性趋势分析

用法：
    python feature-matrix-generator.py --versions 2.4 2.5 3.0
    python feature-matrix-generator.py --extract-from Flink/02-core-mechanisms/
    python feature-matrix-generator.py --output-format all

作者: Agent
日期: 2026-04-04
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict
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

# 特性状态映射
STATUS_SYMBOLS = {
    "supported": "✅",
    "preview": "🚧",
    "deprecated": "⚠️",
    "not_supported": "❌",
    "planned": "🔜",
    "unknown": "❓",
}

STATUS_COLORS = {
    "supported": "#28a745",
    "preview": "#ffc107",
    "deprecated": "#fd7e14",
    "not_supported": "#dc3545",
    "planned": "#6c757d",
}


# =============================================================================
# 特性提取器
# =============================================================================

class FeatureExtractor:
    """从文档中提取特性信息"""
    
    # 特性模式定义
    PATTERNS = {
        "definitions": {
            "regex": r'###\s+(Def-[A-Z]-\d{2}-\d{2}):\s*(.+?)(?=\n###|\n##|$)',
            "type": "definition"
        },
        "theorems": {
            "regex": r'####?\s+(Thm-[A-Z]-\d{2}-\d{2}):\s*(.+?)(?=\n####?|\n###|$)',
            "type": "theorem"
        },
        "lemmas": {
            "regex": r'####?\s+(Lemma-[A-Z]-\d{2}-\d{2}):\s*(.+?)(?=\n####?|\n###|$)',
            "type": "lemma"
        },
        "propositions": {
            "regex": r'####?\s+(Prop-[A-Z]-\d{2}-\d{2}):\s*(.+?)(?=\n####?|\n###|$)',
            "type": "proposition"
        },
        "flips": {
            "regex": r'FLIP-(\d+):\s*[\"\']?([^\"\'\n]+)[\"\']?',
            "type": "flip"
        },
        "features": {
            "regex": r'[-*]\s*(.+?):\s*(.+?)(?=\n[-*]|\n##|$)',
            "type": "feature"
        },
    }
    
    def __init__(self, base_path: Path = PROJECT_ROOT):
        self.base_path = base_path
        self.extracted_features = defaultdict(list)
    
    def extract_from_file(self, file_path: Path) -> Dict[str, List[Dict]]:
        """从单个文件提取特性"""
        if not file_path.exists():
            return {}
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        features = defaultdict(list)
        
        for category, pattern in self.PATTERNS.items():
            matches = re.findall(pattern["regex"], content, re.DOTALL)
            for match in matches:
                if isinstance(match, tuple):
                    feature_id = match[0]
                    feature_desc = match[1].strip().split('\n')[0]  # 只取第一行
                else:
                    feature_id = match
                    feature_desc = ""
                
                features[category].append({
                    "id": feature_id,
                    "description": feature_desc,
                    "type": pattern["type"],
                    "source": str(file_path.relative_to(self.base_path)),
                })
        
        return dict(features)
    
    def extract_from_directory(self, dir_path: Path, recursive: bool = True) -> Dict[str, List[Dict]]:
        """从目录提取特性"""
        all_features = defaultdict(list)
        
        if recursive:
            md_files = list(dir_path.rglob("*.md"))
        else:
            md_files = list(dir_path.glob("*.md"))
        
        for file_path in md_files:
            features = self.extract_from_file(file_path)
            for category, items in features.items():
                all_features[category].extend(items)
        
        return dict(all_features)
    
    def extract_version_features(self, config: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """从版本文档中提取特性信息"""
        version_features = {}
        
        doc_paths = config.get("document_paths", {})
        tracking_docs = doc_paths.get("tracking", {})
        
        for version, doc_path in tracking_docs.items():
            full_path = self.base_path / doc_path
            if full_path.exists():
                features = self.extract_from_file(full_path)
                version_features[version] = {
                    "source": str(doc_path),
                    "features": features,
                    "extracted_at": datetime.now().isoformat(),
                }
        
        return version_features


# =============================================================================
# 矩阵生成器
# =============================================================================

class FeatureMatrixGenerator:
    """特性矩阵生成器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.feature_matrix = config.get("feature_matrix", {})
        self.categories = config.get("feature_categories", [])
    
    def get_feature_status(self, version: str, feature_id: str) -> str:
        """获取特性的支持状态"""
        version_features = self.feature_matrix.get("version_features", {})
        features = version_features.get(version, {})
        return features.get(feature_id, "unknown")
    
    def get_status_symbol(self, status: str) -> str:
        """获取状态符号"""
        return STATUS_SYMBOLS.get(status, "❓")
    
    def generate_markdown_matrix(self, versions: List[str], 
                                  category_filter: Optional[List[str]] = None) -> str:
        """
        生成 Markdown 格式的特性矩阵
        
        Args:
            versions: 要包含的版本列表
            category_filter: 可选的类别过滤
            
        Returns:
            Markdown 表格字符串
        """
        lines = [
            "# Flink 特性支持矩阵\n",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            "---\n",
        ]
        
        for category in self.categories:
            cat_id = category.get("id", "")
            cat_name = category.get("name", "")
            
            if category_filter and cat_id not in category_filter:
                continue
            
            lines.append(f"## {cat_name}\n")
            
            features = category.get("features", [])
            if not features:
                continue
            
            # 表头
            header = ["特性", "描述"] + [f"**{v}**" for v in versions]
            lines.append("| " + " | ".join(header) + " |")
            lines.append("|" + "---|" * (len(versions) + 2))
            
            # 特性行
            for feature in features:
                feature_id = feature.get("id", "")
                feature_name = feature.get("name", "")
                feature_desc = feature.get("description", "")
                
                row = [feature_name, feature_desc]
                
                for version in versions:
                    status = self.get_feature_status(version, feature_id)
                    symbol = self.get_status_symbol(status)
                    row.append(symbol)
                
                lines.append("| " + " | ".join(row) + " |")
            
            lines.append("")  # 空行分隔
        
        # 添加图例
        lines.extend([
            "## 图例\n",
            "| 符号 | 状态 | 说明 |",
            "|------|------|------|",
        ])
        
        status_defs = self.feature_matrix.get("support_status", [])
        for status_def in status_defs:
            symbol = status_def.get("symbol", "")
            label = status_def.get("label", "")
            value = status_def.get("value", "")
            lines.append(f"| {symbol} | {label} | {value} |")
        
        return "\n".join(lines)
    
    def generate_html_matrix(self, versions: List[str],
                              category_filter: Optional[List[str]] = None) -> str:
        """生成 HTML 格式的特性矩阵"""
        markdown_content = self.generate_markdown_matrix(versions, category_filter)
        
        # 转换 Markdown 到 HTML
        html_content = self._markdown_to_html(markdown_content)
        
        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flink 特性支持矩阵</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 
                         'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1400px;
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
            font-size: 14px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: 600;
            position: sticky;
            top: 0;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e8f4f8;
        }}
        .version-header {{
            background-color: #e6522c !important;
            color: white;
            text-align: center;
        }}
        .status-supported {{ color: #28a745; font-weight: bold; }}
        .status-preview {{ color: #ffc107; font-weight: bold; }}
        .status-deprecated {{ color: #fd7e14; }}
        .status-not-supported {{ color: #dc3545; }}
        .status-planned {{ color: #6c757d; }}
        .legend {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
{html_content}
    </div>
</body>
</html>"""
        
        return html_template
    
    def generate_csv_matrix(self, versions: List[str],
                            category_filter: Optional[List[str]] = None) -> str:
        """生成 CSV 格式的特性矩阵"""
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 写入标题
        writer.writerow(["Flink 特性支持矩阵"])
        writer.writerow([f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
        writer.writerow([])
        
        for category in self.categories:
            cat_id = category.get("id", "")
            cat_name = category.get("name", "")
            
            if category_filter and cat_id not in category_filter:
                continue
            
            writer.writerow([cat_name])
            writer.writerow(["特性", "描述"] + versions)
            
            features = category.get("features", [])
            for feature in features:
                feature_name = feature.get("name", "")
                feature_desc = feature.get("description", "")
                
                row = [feature_name, feature_desc]
                for version in versions:
                    status = self.get_feature_status(version, feature.get("id", ""))
                    row.append(status)
                
                writer.writerow(row)
            
            writer.writerow([])  # 空行分隔
        
        return output.getvalue()
    
    def generate_json_matrix(self, versions: List[str]) -> str:
        """生成 JSON 格式的特性矩阵"""
        data = {
            "meta": {
                "generated_at": datetime.now().isoformat(),
                "versions": versions,
            },
            "categories": [],
        }
        
        for category in self.categories:
            cat_data = {
                "id": category.get("id", ""),
                "name": category.get("name", ""),
                "features": [],
            }
            
            for feature in category.get("features", []):
                feature_data = {
                    "id": feature.get("id", ""),
                    "name": feature.get("name", ""),
                    "description": feature.get("description", ""),
                    "support": {},
                }
                
                for version in versions:
                    status = self.get_feature_status(version, feature.get("id", ""))
                    feature_data["support"][version] = {
                        "status": status,
                        "symbol": self.get_status_symbol(status),
                    }
                
                cat_data["features"].append(feature_data)
            
            data["categories"].append(cat_data)
        
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def generate_mermaid_diagram(self, versions: List[str]) -> str:
        """生成 Mermaid 格式的特性演进图"""
        lines = [
            "```mermaid",
            "%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#e6522c', 'edgeLabelBackground':'#fff'}}}%%",
            "graph LR",
        ]
        
        # 添加版本节点
        for i, version in enumerate(versions):
            node_id = f"V{version.replace('.', '_')}"
            lines.append(f"    {node_id}[Flink {version}]")
            
            if i > 0:
                prev_id = f"V{versions[i-1].replace('.', '_')}"
                lines.append(f"    {prev_id} --> {node_id}")
        
        lines.append("    ")
        
        # 为每个重要特性添加子图
        key_features = [
            ("ai_agent", "AI Agent", ["2.3", "2.4", "2.5", "3.0"]),
            ("serverless", "Serverless", ["2.4", "2.5", "3.0"]),
            ("unified_execution", "统一执行层", ["3.0"]),
        ]
        
        for feature_id, feature_name, supported_versions in key_features:
            lines.append(f"    subgraph {feature_name}")
            
            prev_node = None
            for version in versions:
                if version in supported_versions:
                    status = self.get_feature_status(version, feature_id)
                    symbol = self.get_status_symbol(status)
                    node_id = f"{feature_id}_{version.replace('.', '_')}"
                    lines.append(f"        {node_id}[{symbol}]")
                    
                    if prev_node:
                        lines.append(f"        {prev_node} --> {node_id}")
                    prev_node = node_id
            
            lines.append("    end")
            lines.append("    ")
        
        lines.append("```")
        
        return "\n".join(lines)
    
    def generate_ascii_heatmap(self, versions: List[str]) -> str:
        """生成 ASCII 热力图"""
        lines = [
            "",
            "特性支持热力图 (🔥 = 支持 / 🟡 = 预览 / ❄️ = 不支持)",
            "=" * 70,
            "",
        ]
        
        # 收集所有特性
        all_features = []
        for category in self.categories:
            cat_name = category.get("name", "")
            for feature in category.get("features", []):
                all_features.append((cat_name, feature))
        
        # 计算最大名称长度
        max_name_len = max(len(f[1].get("name", "")) for f in all_features) if all_features else 20
        
        # 标题行
        header = "特性".ljust(max_name_len) + " | " + " | ".join(f"{v:>6}" for v in versions)
        lines.append(header)
        lines.append("-" * len(header))
        
        # 当前类别
        current_cat = None
        
        for cat_name, feature in all_features:
            # 类别分隔
            if cat_name != current_cat:
                lines.append(f"\n[{cat_name}]")
                current_cat = cat_name
            
            feature_name = feature.get("name", "")[:max_name_len].ljust(max_name_len)
            row = [feature_name]
            
            for version in versions:
                status = self.get_feature_status(version, feature.get("id", ""))
                if status == "supported":
                    cell = "🔥🔥"
                elif status == "preview":
                    cell = "🟡🟡"
                elif status == "planned":
                    cell = "🔜 "
                else:
                    cell = "❄️❄️"
                row.append(cell.rjust(6))
            
            lines.append(" | ".join(row))
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def _markdown_to_html(self, markdown: str) -> str:
        """简单的 Markdown 到 HTML 转换"""
        html = markdown
        
        # 转义
        html = html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        # 标题
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        
        # 粗体
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        
        # 表格
        lines = html.split('\n')
        result = []
        in_table = False
        header_row = False
        
        for line in lines:
            if line.startswith('|') and '|' in line[1:]:
                if not in_table:
                    result.append('<table>')
                    in_table = True
                    header_row = True
                
                cells = [c.strip() for c in line.split('|')[1:-1]]
                
                # 跳过分隔行
                if all(c.replace('-', '').replace(' ', '') == '' for c in cells):
                    continue
                
                # 版本列添加特殊样式
                if header_row and cells and cells[0] == "特性":
                    row = '<tr>'
                    for i, cell in enumerate(cells):
                        if i >= 2:  # 版本列
                            row += f'<th class="version-header">{cell}</th>'
                        else:
                            row += f'<th>{cell}</th>'
                    row += '</tr>'
                    result.append(row)
                    header_row = False
                else:
                    row = '<tr>'
                    for i, cell in enumerate(cells):
                        if i >= 2:  # 状态列
                            status_class = self._get_status_class(cell)
                            row += f'<td class="{status_class}">{cell}</td>'
                        else:
                            row += f'<td>{cell}</td>'
                    row += '</tr>'
                    result.append(row)
            else:
                if in_table:
                    result.append('</table>')
                    in_table = False
                result.append(line)
        
        if in_table:
            result.append('</table>')
        
        html = '\n'.join(result)
        
        # 段落
        paragraphs = html.split('\n\n')
        processed = []
        for p in paragraphs:
            p = p.strip()
            if p and not p.startswith('<') and not p.endswith('>'):
                p = f'<p>{p}</p>'
            processed.append(p)
        
        return '\n\n'.join(processed)
    
    def _get_status_class(self, cell: str) -> str:
        """根据状态符号获取 CSS 类"""
        symbol_to_status = {
            "✅": "status-supported",
            "🚧": "status-preview",
            "⚠️": "status-deprecated",
            "❌": "status-not-supported",
            "🔜": "status-planned",
        }
        for symbol, status in symbol_to_status.items():
            if symbol in cell:
                return status
        return ""


# =============================================================================
# 命令行接口
# =============================================================================

def create_argument_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="feature-matrix-generator.py",
        description="Flink 特性支持矩阵生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成 Markdown 矩阵
  python feature-matrix-generator.py --versions 2.4 2.5 3.0
  
  # 生成所有格式
  python feature-matrix-generator.py --versions 2.4 2.5 3.0 --format all
  
  # 生成特定类别的矩阵
  python feature-matrix-generator.py --versions 2.4 2.5 --category ai_ml cloud_native
  
  # 生成 Mermaid 图
  python feature-matrix-generator.py --versions 2.4 2.5 3.0 --mermaid
        """
    )
    
    parser.add_argument(
        "--versions",
        nargs="+",
        default=["2.4", "2.5", "3.0"],
        help="要包含的版本列表"
    )
    
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="配置文件路径"
    )
    
    parser.add_argument(
        "--format",
        choices=["markdown", "html", "csv", "json", "all"],
        default="markdown",
        help="输出格式"
    )
    
    parser.add_argument(
        "--category",
        nargs="+",
        help="只包含指定类别的特性"
    )
    
    parser.add_argument(
        "--mermaid",
        action="store_true",
        help="生成 Mermaid 演进图"
    )
    
    parser.add_argument(
        "--heatmap",
        action="store_true",
        help="生成 ASCII 热力图"
    )
    
    parser.add_argument(
        "--output",
        type=Path,
        help="输出文件路径"
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="输出目录 (用于 all 格式)"
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
        
        generator = FeatureMatrixGenerator(config)
        
        outputs = {}
        
        # 生成各种格式的输出
        if args.format in ["markdown", "all"]:
            outputs["md"] = generator.generate_markdown_matrix(args.versions, args.category)
        
        if args.format in ["html", "all"]:
            outputs["html"] = generator.generate_html_matrix(args.versions, args.category)
        
        if args.format in ["csv", "all"]:
            outputs["csv"] = generator.generate_csv_matrix(args.versions, args.category)
        
        if args.format in ["json", "all"]:
            outputs["json"] = generator.generate_json_matrix(args.versions)
        
        if args.mermaid or args.format == "all":
            outputs["mermaid"] = generator.generate_mermaid_diagram(args.versions)
        
        if args.heatmap or args.format == "all":
            outputs["heatmap"] = generator.generate_ascii_heatmap(args.versions)
        
        # 输出结果
        if args.format == "all" and args.output_dir:
            # 输出到目录
            args.output_dir.mkdir(parents=True, exist_ok=True)
            for ext, content in outputs.items():
                output_path = args.output_dir / f"feature-matrix.{ext}"
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"已保存: {output_path}")
        elif args.output:
            # 输出到单个文件
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(list(outputs.values())[0])
            print(f"已保存: {args.output}")
        else:
            # 输出到 stdout
            for ext, content in outputs.items():
                if len(outputs) > 1:
                    print(f"\n{'='*60}")
                    print(f"格式: {ext}")
                    print(f"{'='*60}\n")
                print(content)
        
        return 0
        
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
