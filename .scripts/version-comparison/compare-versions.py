#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink 版本对比工具
================
比较 Flink 2.4、2.5、3.0 等版本的特性差异，生成对比表格和报告。

功能：
1. 多版本特性对比分析
2. 生成 Markdown/HTML 对比表格
3. 版本评分与推荐
4. 迁移复杂度评估

用法：
    python compare-versions.py --versions 2.4 2.5 3.0 --format markdown
    python compare-versions.py --config config.yaml --output ./reports

作者: Agent
日期: 2026-04-04
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


# =============================================================================
# 常量定义
# =============================================================================

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DEFAULT_CONFIG_PATH = SCRIPT_DIR / "config.yaml"

# 特性状态符号映射
STATUS_SYMBOLS = {
    "supported": "✅",
    "preview": "🚧",
    "deprecated": "⚠️",
    "not_supported": "❌",
    "planned": "🔜",
}

# 版本生命周期状态
LIFECYCLE_STATUS = {
    "active": "🔥 活跃开发",
    "stable": "✅ 稳定维护",
    "maintenance": "⚠️ 维护模式",
    "eol": "❌ 终止支持",
    "preview": "🚧 预览/开发",
    "planning": "📋 规划中",
}


# =============================================================================
# 配置加载
# =============================================================================

def load_config(config_path: Path) -> Dict[str, Any]:
    """
    加载 YAML 配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
        
    Raises:
        FileNotFoundError: 配置文件不存在
        yaml.YAMLError: YAML解析错误
    """
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    return config


# =============================================================================
# 版本数据模型
# =============================================================================

class VersionInfo:
    """版本信息数据类"""
    
    def __init__(self, version: str, config: Dict[str, Any]):
        self.version = version
        self.release_date = config.get("release_date", "TBD")
        self.status = config.get("status", "未知")
        self.lifecycle = config.get("lifecycle", "unknown")
        self.description = config.get("description", "")
        self.highlights = config.get("highlights", [])
        self.changes = config.get("changes_from_2_3", {}) if version == "2.4" else \
                       config.get("changes_from_2_4", {}) if version == "2.5" else \
                       config.get("changes_from_2_5", {})
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "version": self.version,
            "release_date": self.release_date,
            "status": self.status,
            "lifecycle": self.lifecycle,
            "description": self.description,
            "highlights": self.highlights,
            "changes": self.changes,
        }


class FeatureMatrix:
    """特性矩阵数据类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.categories = config.get("feature_categories", [])
        self.status_defs = config.get("feature_matrix", {}).get("support_status", [])
        self.version_features = config.get("feature_matrix", {}).get("version_features", {})
    
    def get_feature_status(self, version: str, feature_id: str) -> str:
        """获取指定版本和特性的支持状态"""
        features = self.version_features.get(version, {})
        return features.get(feature_id, "not_supported")
    
    def get_status_symbol(self, status: str) -> str:
        """获取状态符号"""
        for s in self.status_defs:
            if s["value"] == status:
                return s["symbol"]
        return "❓"


# =============================================================================
# 对比生成器
# =============================================================================

class VersionComparator:
    """版本对比生成器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.versions_config = config.get("versions", {})
        self.feature_matrix = FeatureMatrix(config)
        self.comparison_config = config.get("version_comparison", {})
    
    def get_version_info(self, version: str) -> VersionInfo:
        """获取版本信息"""
        if version not in self.versions_config:
            raise ValueError(f"未找到版本配置: {version}")
        return VersionInfo(version, self.versions_config[version])
    
    def generate_overview_table(self, versions: List[str]) -> str:
        """
        生成版本概览对比表 (Markdown格式)
        
        Args:
            versions: 要对比的版本列表
            
        Returns:
            Markdown 表格字符串
        """
        lines = [
            "## 版本概览对比\n",
            "| 特性 | " + " | ".join(f"**{v}**" for v in versions) + " |",
            "|" + "---|" * (len(versions) + 1),
        ]
        
        # 发布日期
        row = ["**发布日期**"]
        for v in versions:
            info = self.get_version_info(v)
            row.append(info.release_date)
        lines.append("| " + " | ".join(row) + " |")
        
        # 状态
        row = ["**状态**"]
        for v in versions:
            info = self.get_version_info(v)
            row.append(info.status)
        lines.append("| " + " | ".join(row) + " |")
        
        # 生命周期
        row = ["**生命周期**"]
        for v in versions:
            info = self.get_version_info(v)
            status = LIFECYCLE_STATUS.get(info.lifecycle, info.lifecycle)
            row.append(status)
        lines.append("| " + " | ".join(row) + " |")
        
        # 主要描述
        row = ["**定位**"]
        for v in versions:
            info = self.get_version_info(v)
            row.append(info.description)
        lines.append("| " + " | ".join(row) + " |")
        
        return "\n".join(lines)
    
    def generate_feature_matrix_table(self, versions: List[str]) -> str:
        """
        生成特性支持矩阵表 (Markdown格式)
        
        Args:
            versions: 要对比的版本列表
            
        Returns:
            Markdown 表格字符串
        """
        lines = [
            "## 特性支持矩阵\n",
        ]
        
        for category in self.feature_matrix.categories:
            lines.append(f"### {category['name']}\n")
            
            # 表头
            header = ["特性", "描述"] + [f"**{v}**" for v in versions]
            lines.append("| " + " | ".join(header) + " |")
            lines.append("|" + "---|" * (len(versions) + 2))
            
            # 特性行
            for feature in category.get("features", []):
                feature_id = feature["id"]
                row = [
                    feature["name"],
                    feature["description"],
                ]
                
                for v in versions:
                    status = self.feature_matrix.get_feature_status(v, feature_id)
                    symbol = self.feature_matrix.get_status_symbol(status)
                    row.append(symbol)
                
                lines.append("| " + " | ".join(row) + " |")
            
            lines.append("")  # 空行分隔
        
        # 图例
        lines.append("### 图例\n")
        lines.append("| 符号 | 含义 |")
        lines.append("|---|---|")
        for s in self.feature_matrix.status_defs:
            lines.append(f"| {s['symbol']} | {s['label']} |")
        
        return "\n".join(lines)
    
    def generate_highlights_section(self, versions: List[str]) -> str:
        """
        生成版本亮点对比
        
        Args:
            versions: 要对比的版本列表
            
        Returns:
            Markdown 字符串
        """
        lines = ["## 版本亮点对比\n"]
        
        for v in versions:
            info = self.get_version_info(v)
            lines.append(f"### Flink {v}\n")
            lines.append(f"**发布时间**: {info.release_date}\n")
            lines.append(f"**版本定位**: {info.description}\n")
            lines.append("**核心亮点**:")
            for highlight in info.highlights:
                lines.append(f"- {highlight}")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_changes_section(self, versions: List[str]) -> str:
        """
        生成版本变更详情
        
        Args:
            versions: 要对比的版本列表
            
        Returns:
            Markdown 字符串
        """
        lines = ["## 版本变更详情\n"]
        
        for v in versions:
            info = self.get_version_info(v)
            if not info.changes:
                continue
            
            lines.append(f"### Flink {v} 主要变更\n")
            
            # 新增特性
            added = info.changes.get("added", [])
            if added:
                lines.append("**✨ 新增特性**:")
                for item in added:
                    lines.append(f"- {item}")
                lines.append("")
            
            # 功能增强
            enhanced = info.changes.get("enhanced", [])
            if enhanced:
                lines.append("**📝 功能增强**:")
                for item in enhanced:
                    lines.append(f"- {item}")
                lines.append("")
            
            # 弃用功能
            deprecated = info.changes.get("deprecated", [])
            if deprecated:
                lines.append("**⚠️ 已弃用**:")
                for item in deprecated:
                    lines.append(f"- {item}")
                lines.append("")
            
            # 破坏性变更
            breaking = info.changes.get("breaking_changes", [])
            if breaking:
                lines.append("**❌ 破坏性变更**:")
                for item in breaking:
                    lines.append(f"- {item}")
                lines.append("")
        
        return "\n".join(lines)
    
    def generate_score_card(self, versions: List[str]) -> str:
        """
        生成版本评分卡
        
        Args:
            versions: 要对比的版本列表
            
        Returns:
            Markdown 字符串
        """
        scoring = self.comparison_config.get("scoring", {})
        
        lines = [
            "## 版本评分对比\n",
            "评分维度 (1-5分):\n",
            "| 维度 | " + " | ".join(f"**{v}**" for v in versions) + " |",
            "|" + "---|" * (len(versions) + 1),
        ]
        
        dimensions = [
            ("稳定性", "stability"),
            ("新特性丰富度", "new_features"),
            ("性能优化", "performance"),
            ("迁移容易度", "migration_ease"),
        ]
        
        for label, key in dimensions:
            scores = scoring.get(key, {})
            row = [f"**{label}**"]
            for v in versions:
                score = scores.get(v, "N/A")
                # 转换为星级显示
                if isinstance(score, (int, float)):
                    stars = "⭐" * int(score) + ("½" if score % 1 >= 0.5 else "")
                    row.append(f"{score} {stars}")
                else:
                    row.append(str(score))
            lines.append("| " + " | ".join(row) + " |")
        
        # 计算综合得分
        lines.append("|" + "---|" * (len(versions) + 1))
        row = ["**综合评分**"]
        for v in versions:
            total = 0
            count = 0
            for _, key in dimensions:
                scores = scoring.get(key, {})
                if v in scores:
                    total += scores[v]
                    count += 1
            if count > 0:
                avg = total / count
                row.append(f"**{avg:.1f}**")
            else:
                row.append("N/A")
        lines.append("| " + " | ".join(row) + " |")
        
        return "\n".join(lines)
    
    def generate_recommendation(self, versions: List[str]) -> str:
        """
        生成版本选择建议
        
        Args:
            versions: 要对比的版本列表
            
        Returns:
            Markdown 字符串
        """
        lines = [
            "## 版本选择建议\n",
            "基于不同场景的版本推荐:\n",
        ]
        
        recommendations = [
            ("生产环境 (稳定性优先)", "推荐使用 Flink 2.5，作为LTS长期支持版本，提供最稳定的企业级支持。"),
            ("云原生部署", "Flink 2.4+ 提供 Serverless 支持，2.5 GA 更成熟。"),
            ("AI/ML集成", "需要 AI Agent 功能选择 2.4+，需要 GPU 加速选择 2.5+。"),
            ("前瞻性项目", "Flink 3.0 提供最新架构，适合愿意承担一定迁移成本的项目。"),
        ]
        
        for title, content in recommendations:
            lines.append(f"### {title}")
            lines.append(f"{content}\n")
        
        return "\n".join(lines)
    
    def generate_markdown_report(self, versions: List[str]) -> str:
        """
        生成完整的 Markdown 对比报告
        
        Args:
            versions: 要对比的版本列表
            
        Returns:
            完整 Markdown 报告
        """
        report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        lines = [
            f"# Flink 版本对比报告: {' vs '.join(versions)}",
            "",
            f"> 生成时间: {report_date}",
            f"> 对比版本: {', '.join(versions)}",
            "",
            "---",
            "",
        ]
        
        # 1. 版本概览
        lines.append(self.generate_overview_table(versions))
        lines.append("\n---\n")
        
        # 2. 版本亮点
        lines.append(self.generate_highlights_section(versions))
        lines.append("\n---\n")
        
        # 3. 特性矩阵
        lines.append(self.generate_feature_matrix_table(versions))
        lines.append("\n---\n")
        
        # 4. 变更详情
        lines.append(self.generate_changes_section(versions))
        lines.append("\n---\n")
        
        # 5. 评分对比
        lines.append(self.generate_score_card(versions))
        lines.append("\n---\n")
        
        # 6. 选择建议
        lines.append(self.generate_recommendation(versions))
        
        # 7. Mermaid 架构演进图
        lines.extend([
            "\n---\n",
            "## 版本演进架构图\n",
            "```mermaid",
            "graph LR",
        ])
        
        for i, v in enumerate(versions):
            if i < len(versions) - 1:
                lines.append(f"    V{v.replace('.', '_')}[Flink {v}] --> V{versions[i+1].replace('.', '_')}[Flink {versions[i+1]}]")
        
        lines.extend([
            "```",
            "",
        ])
        
        return "\n".join(lines)
    
    def generate_html_report(self, versions: List[str]) -> str:
        """
        生成 HTML 格式的对比报告
        
        Args:
            versions: 要对比的版本列表
            
        Returns:
            HTML 字符串
        """
        markdown_content = self.generate_markdown_report(versions)
        
        # 基础 HTML 模板
        html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flink 版本对比报告</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        * {{
            box-sizing: border-box;
        }}
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
        h3 {{
            color: #555;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: 600;
            color: #333;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #f0f0f0;
        }}
        .version-header {{
            background-color: #e6522c;
            color: white;
            font-weight: bold;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
        }}
        blockquote {{
            border-left: 4px solid #e6522c;
            margin: 0;
            padding-left: 16px;
            color: #666;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 30px 0;
        }}
        .mermaid {{
            text-align: center;
            margin: 20px 0;
        }}
        .status-supported {{
            color: #28a745;
            font-weight: bold;
        }}
        .status-preview {{
            color: #ffc107;
            font-weight: bold;
        }}
        .status-deprecated {{
            color: #fd7e14;
        }}
        .status-not-supported {{
            color: #dc3545;
        }}
    </style>
</head>
<body>
    <div class="container">
{content}
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default'
        }});
    </script>
</body>
</html>"""
        
        # 简单的 Markdown 到 HTML 转换
        html_content = self._markdown_to_html(markdown_content)
        
        return html_template.format(content=html_content)
    
    def _markdown_to_html(self, markdown: str) -> str:
        """简单的 Markdown 到 HTML 转换"""
        html = markdown
        
        # 转义 HTML 特殊字符
        html = html.replace("&", "&amp;")
        html = html.replace("<", "&lt;")
        html = html.replace(">", "&gt;")
        
        # 标题
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        
        # 粗体和斜体
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        
        # 代码
        html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
        
        # 分隔线
        html = html.replace("---", "<hr>")
        
        # 引用块
        html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
        
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
        
        # 表格 (简单处理)
        lines = html.split('\n')
        result = []
        in_table = False
        
        for line in lines:
            if line.startswith('|') and '|' in line[1:]:
                if not in_table:
                    result.append('<table>')
                    in_table = True
                
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if all(c.replace('-', '').replace(' ', '') == '' for c in cells):
                    # 分隔行，跳过
                    continue
                
                tag = 'th' if result[-1] == '<table>' else 'td'
                row = '<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>'
                result.append(row)
            else:
                if in_table:
                    result.append('</table>')
                    in_table = False
                result.append(line)
        
        if in_table:
            result.append('</table>')
        
        html = '\n'.join(result)
        
        # Mermaid 图表
        html = html.replace('```mermaid', '<div class="mermaid">')
        html = html.replace('```', '</div>')
        
        # 段落
        paragraphs = html.split('\n\n')
        processed = []
        for p in paragraphs:
            p = p.strip()
            if p and not p.startswith('<') and not p.endswith('>'):
                p = f'<p>{p}</p>'
            processed.append(p)
        html = '\n\n'.join(processed)
        
        return html


# =============================================================================
# 命令行接口
# =============================================================================

def create_argument_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="compare-versions.py",
        description="Flink 版本对比工具 - 生成版本特性对比报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 对比默认版本 (2.4 vs 2.5 vs 3.0) 生成 Markdown 报告
  python compare-versions.py
  
  # 对比指定版本
  python compare-versions.py --versions 2.4 2.5
  
  # 生成 HTML 报告
  python compare-versions.py --format html --output report.html
  
  # 指定配置文件
  python compare-versions.py --config my-config.yaml
        """
    )
    
    parser.add_argument(
        "--versions",
        nargs="+",
        default=["2.4", "2.5", "3.0"],
        help="要对比的版本列表 (默认: 2.4 2.5 3.0)"
    )
    
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help=f"配置文件路径 (默认: {DEFAULT_CONFIG_PATH})"
    )
    
    parser.add_argument(
        "--format",
        choices=["markdown", "html", "json"],
        default="markdown",
        help="输出格式 (默认: markdown)"
    )
    
    parser.add_argument(
        "--output",
        type=Path,
        help="输出文件路径 (默认: 输出到stdout)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="启用详细日志输出"
    )
    
    return parser


def main():
    """主入口函数"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    try:
        # 加载配置
        config = load_config(args.config)
        
        # 创建对比器
        comparator = VersionComparator(config)
        
        # 验证版本
        for v in args.versions:
            comparator.get_version_info(v)  # 会抛出异常如果版本不存在
        
        if args.verbose:
            print(f"正在对比版本: {', '.join(args.versions)}", file=sys.stderr)
            print(f"输出格式: {args.format}", file=sys.stderr)
        
        # 生成报告
        if args.format == "markdown":
            output = comparator.generate_markdown_report(args.versions)
        elif args.format == "html":
            output = comparator.generate_html_report(args.versions)
        elif args.format == "json":
            # JSON 输出版本信息
            data = {
                "versions": [comparator.get_version_info(v).to_dict() for v in args.versions],
                "generated_at": datetime.now().isoformat(),
            }
            output = json.dumps(data, ensure_ascii=False, indent=2)
        else:
            raise ValueError(f"不支持的格式: {args.format}")
        
        # 输出结果
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"报告已保存到: {args.output}")
        else:
            print(output)
        
        return 0
        
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
