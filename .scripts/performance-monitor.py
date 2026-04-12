#!/usr/bin/env python3
"""
性能监控脚本 - AnalysisDataFlow 项目质量监控
功能:
  1. 文档数量统计
  2. 代码示例统计
  3. 链接健康检查
  4. 构建时间监控
  5. 质量评分计算

作者: AnalysisDataFlow 监控体系
版本: 1.0.0
"""

import os
import re
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple, Any

# ============ 配置 ============
CONFIG = {
    "project_name": "AnalysisDataFlow",
    "version": "1.0.0",
    "directories": {
        "struct": "Struct",
        "knowledge": "Knowledge", 
        "flink": "Flink",
        "tutorials": "tutorials",
        "visuals": "visuals",
        "en": "en"
    },
    "thresholds": {
        "doc_count_min": 800,
        "code_examples_min": 4000,
        "link_health_min": 95.0,
        "quality_score_min": 85.0,
        "build_time_max": 300  # 秒
    },
    "patterns": {
        "code_block": re.compile(r'```[\w]*\n(.*?)```', re.DOTALL),
        "external_link": re.compile(r'\[([^\]]+)\]\((https?://[^\s\)]+)\)'),
        "internal_link": re.compile(r'\[([^\]]+)\]\(([^)]+)\)'),
        "mermaid": re.compile(r'```mermaid\n(.*?)```', re.DOTALL),
        "theorem": re.compile(r'\b(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2})\b'),
        "heading": re.compile(r'^#{1,6}\s+(.+)$', re.MULTILINE)
    }
}


class PerformanceMonitor:
    """性能监控主类"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.metrics = {}
        self.start_time = time.time()
        self.errors = []
        
    def run_all_checks(self) -> Dict[str, Any]:
        """运行所有监控检查"""
        print("=" * 60)
        print("AnalysisDataFlow 性能监控系统")
        print(f"开始时间: {datetime.now().isoformat()}")
        print("=" * 60)
        
        # 1. 文档统计
        print("\n📊 正在统计文档数量...")
        self.metrics["documents"] = self._count_documents()
        
        # 2. 代码示例统计
        print("\n💻 正在统计代码示例...")
        self.metrics["code_examples"] = self._count_code_examples()
        
        # 3. 链接健康检查
        print("\n🔗 正在检查链接健康...")
        self.metrics["link_health"] = self._check_link_health()
        
        # 4. 形式化元素统计
        print("\n📐 正在统计形式化元素...")
        self.metrics["formal_elements"] = self._count_formal_elements()
        
        # 5. 可视化统计
        print("\n📈 正在统计可视化图表...")
        self.metrics["visualizations"] = self._count_visualizations()
        
        # 6. 质量评分计算
        print("\n⭐ 正在计算质量评分...")
        self.metrics["quality_score"] = self._calculate_quality_score()
        
        # 7. 构建时间监控
        self.metrics["build_time"] = time.time() - self.start_time
        
        # 8. 阈值检查
        print("\n🚨 正在检查阈值...")
        self.metrics["alerts"] = self._check_thresholds()
        
        # 生成报告
        print("\n📝 正在生成报告...")
        self._generate_reports()
        
        return self.metrics
    
    def _count_documents(self) -> Dict[str, Any]:
        """统计文档数量"""
        stats = {
            "total": 0,
            "by_directory": {},
            "by_type": defaultdict(int),
            "total_lines": 0,
            "total_size_bytes": 0
        }
        
        for key, directory in CONFIG["directories"].items():
            dir_path = self.base_path / directory
            if not dir_path.exists():
                continue
                
            md_files = list(dir_path.rglob("*.md"))
            count = len(md_files)
            lines = 0
            size = 0
            
            for f in md_files:
                try:
                    content = f.read_text(encoding='utf-8')
                    lines += len(content.splitlines())
                    size += f.stat().st_size
                except Exception as e:
                    self.errors.append(f"Error reading {f}: {e}")
            
            stats["by_directory"][key] = {
                "count": count,
                "lines": lines,
                "size_bytes": size
            }
            stats["total"] += count
            stats["total_lines"] += lines
            stats["total_size_bytes"] += size
        
        # 统计根目录文档
        root_docs = [f for f in self.base_path.glob("*.md") if f.is_file()]
        stats["by_directory"]["root"] = {
            "count": len(root_docs),
            "lines": 0,
            "size_bytes": 0
        }
        for f in root_docs:
            try:
                content = f.read_text(encoding='utf-8')
                stats["by_directory"]["root"]["lines"] += len(content.splitlines())
                stats["by_directory"]["root"]["size_bytes"] += f.stat().st_size
            except:
                pass
        stats["total"] += len(root_docs)
        
        return stats
    
    def _count_code_examples(self) -> Dict[str, Any]:
        """统计代码示例"""
        stats = {
            "total_blocks": 0,
            "by_language": defaultdict(int),
            "total_lines": 0,
            "files_with_code": 0
        }
        
        pattern = CONFIG["patterns"]["code_block"]
        
        for key, directory in CONFIG["directories"].items():
            dir_path = self.base_path / directory
            if not dir_path.exists():
                continue
            
            for md_file in dir_path.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    has_code = False
                    
                    # 查找代码块
                    for match in pattern.finditer(content):
                        stats["total_blocks"] += 1
                        code = match.group(1)
                        lines = len(code.splitlines())
                        stats["total_lines"] += lines
                        has_code = True
                        
                        # 检测语言
                        block_start = content[:match.start()].rfind('```')
                        if block_start >= 0:
                            lang_line = content[block_start:match.start()].strip()
                            lang = lang_line.replace('```', '').strip() or 'text'
                            stats["by_language"][lang] += 1
                    
                    if has_code:
                        stats["files_with_code"] += 1
                        
                except Exception as e:
                    self.errors.append(f"Error analyzing code in {md_file}: {e}")
        
        return dict(stats)
    
    def _check_link_health(self) -> Dict[str, Any]:
        """检查链接健康"""
        stats = {
            "total_links": 0,
            "valid_links": 0,
            "broken_links": 0,
            "external_links": 0,
            "internal_links": 0,
            "health_rate": 100.0,
            "errors": []
        }
        
        internal_pattern = CONFIG["patterns"]["internal_link"]
        all_docs = set()
        
        # 收集所有文档
        for key, directory in CONFIG["directories"].items():
            dir_path = self.base_path / directory
            if not dir_path.exists():
                continue
            for md_file in dir_path.rglob("*.md"):
                all_docs.add(str(md_file.relative_to(self.base_path)).replace('\\', '/'))
        
        # 检查链接
        for key, directory in CONFIG["directories"].items():
            dir_path = self.base_path / directory
            if not dir_path.exists():
                continue
            
            for md_file in dir_path.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    doc_dir = md_file.parent.relative_to(self.base_path)
                    rel_path = str(md_file.relative_to(self.base_path)).replace('\\', '/')
                    
                    for match in internal_pattern.finditer(content):
                        link_target = match.group(2)
                        stats["total_links"] += 1
                        
                        # 外部链接
                        if link_target.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                            stats["external_links"] += 1
                            stats["valid_links"] += 1  # 跳过外部链接验证
                            continue
                        
                        # 内部链接
                        stats["internal_links"] += 1
                        
                        # 处理锚点
                        if link_target.startswith('#'):
                            stats["valid_links"] += 1
                            continue
                        
                        # 分离路径和锚点
                        target_parts = link_target.split('#')
                        target_path = target_parts[0]
                        
                        if not target_path:
                            stats["valid_links"] += 1
                            continue
                        
                        # 解析目标路径
                        if target_path.startswith('/'):
                            full_path = target_path.lstrip('/')
                        else:
                            target = Path(doc_dir) / target_path
                            full_path = str(target).replace('\\', '/')
                        
                        # 检查文件是否存在
                        if full_path in all_docs or (self.base_path / full_path).exists():
                            stats["valid_links"] += 1
                        else:
                            stats["broken_links"] += 1
                            stats["errors"].append({
                                "file": rel_path,
                                "target": link_target
                            })
                            
                except Exception as e:
                    self.errors.append(f"Error checking links in {md_file}: {e}")
        
        # 计算健康率
        if stats["total_links"] > 0:
            stats["health_rate"] = round(
                (stats["valid_links"] / stats["total_links"]) * 100, 2
            )
        
        return stats
    
    def _count_formal_elements(self) -> Dict[str, Any]:
        """统计形式化元素"""
        stats = {
            "total": 0,
            "by_type": defaultdict(int),
            "by_category": defaultdict(int)
        }
        
        pattern = CONFIG["patterns"]["theorem"]
        
        for key, directory in CONFIG["directories"].items():
            dir_path = self.base_path / directory
            if not dir_path.exists():
                continue
            
            for md_file in dir_path.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    
                    for match in pattern.finditer(content):
                        elem_type = match.group(1)  # Thm, Def, etc.
                        category = match.group(2)    # S, K, F
                        
                        stats["total"] += 1
                        stats["by_type"][elem_type] += 1
                        stats["by_category"][category] += 1
                        
                except Exception as e:
                    self.errors.append(f"Error counting formal elements in {md_file}: {e}")
        
        return dict(stats)
    
    def _count_visualizations(self) -> Dict[str, Any]:
        """统计可视化图表"""
        stats = {
            "total_mermaid": 0,
            "total_images": 0,
            "files_with_visuals": 0
        }
        
        mermaid_pattern = CONFIG["patterns"]["mermaid"]
        image_pattern = re.compile(r'!\[([^\]]*)\]\(([^\)]+)\)')
        
        for key, directory in CONFIG["directories"].items():
            dir_path = self.base_path / directory
            if not dir_path.exists():
                continue
            
            for md_file in dir_path.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    has_visual = False
                    
                    # 统计 Mermaid 图表
                    mermaid_count = len(mermaid_pattern.findall(content))
                    stats["total_mermaid"] += mermaid_count
                    if mermaid_count > 0:
                        has_visual = True
                    
                    # 统计图片
                    image_count = len(image_pattern.findall(content))
                    stats["total_images"] += image_count
                    if image_count > 0:
                        has_visual = True
                    
                    if has_visual:
                        stats["files_with_visuals"] += 1
                        
                except Exception as e:
                    self.errors.append(f"Error counting visuals in {md_file}: {e}")
        
        return stats
    
    def _calculate_quality_score(self) -> Dict[str, Any]:
        """计算质量评分"""
        scores = {
            "completeness": 0,      # 完整性
            "consistency": 0,       # 一致性
            "coverage": 0,          # 覆盖率
            "maintainability": 0,   # 可维护性
            "overall": 0
        }
        
        # 完整性评分 (基于文档结构)
        doc_data = self.metrics.get("documents", {})
        total_docs = doc_data.get("total", 0)
        expected_docs = CONFIG["thresholds"]["doc_count_min"]
        scores["completeness"] = min(100, round((total_docs / expected_docs) * 100, 2))
        
        # 一致性评分 (基于链接健康)
        link_data = self.metrics.get("link_health", {})
        health_rate = link_data.get("health_rate", 100)
        scores["consistency"] = health_rate
        
        # 覆盖率评分 (基于代码示例)
        code_data = self.metrics.get("code_examples", {})
        code_count = code_data.get("total_blocks", 0)
        expected_code = CONFIG["thresholds"]["code_examples_min"]
        scores["coverage"] = min(100, round((code_count / expected_code) * 100, 2))
        
        # 可维护性评分 (基于形式化元素)
        formal_data = self.metrics.get("formal_elements", {})
        formal_count = formal_data.get("total", 0)
        # 假设 8000 个形式化元素为满分
        scores["maintainability"] = min(100, round((formal_count / 8000) * 100, 2))
        
        # 总体评分 (加权平均)
        scores["overall"] = round(
            scores["completeness"] * 0.25 +
            scores["consistency"] * 0.25 +
            scores["coverage"] * 0.25 +
            scores["maintainability"] * 0.25,
            2
        )
        
        return scores
    
    def _check_thresholds(self) -> List[Dict[str, Any]]:
        """检查阈值并生成告警"""
        alerts = []
        
        # 检查文档数量
        doc_count = self.metrics["documents"].get("total", 0)
        if doc_count < CONFIG["thresholds"]["doc_count_min"]:
            alerts.append({
                "severity": "warning",
                "metric": "document_count",
                "message": f"文档数量 ({doc_count}) 低于阈值 ({CONFIG['thresholds']['doc_count_min']})",
                "value": doc_count,
                "threshold": CONFIG["thresholds"]["doc_count_min"]
            })
        
        # 检查链接健康
        health_rate = self.metrics["link_health"].get("health_rate", 100)
        if health_rate < CONFIG["thresholds"]["link_health_min"]:
            alerts.append({
                "severity": "critical",
                "metric": "link_health",
                "message": f"链接健康率 ({health_rate}%) 低于阈值 ({CONFIG['thresholds']['link_health_min']}%)",
                "value": health_rate,
                "threshold": CONFIG["thresholds"]["link_health_min"]
            })
        
        # 检查质量评分
        quality = self.metrics["quality_score"].get("overall", 100)
        if quality < CONFIG["thresholds"]["quality_score_min"]:
            alerts.append({
                "severity": "warning",
                "metric": "quality_score",
                "message": f"质量评分 ({quality}) 低于阈值 ({CONFIG['thresholds']['quality_score_min']})",
                "value": quality,
                "threshold": CONFIG["thresholds"]["quality_score_min"]
            })
        
        # 检查构建时间
        build_time = self.metrics.get("build_time", 0)
        if build_time > CONFIG["thresholds"]["build_time_max"]:
            alerts.append({
                "severity": "info",
                "metric": "build_time",
                "message": f"构建时间 ({build_time:.1f}s) 超过阈值 ({CONFIG['thresholds']['build_time_max']}s)",
                "value": build_time,
                "threshold": CONFIG["thresholds"]["build_time_max"]
            })
        
        return alerts
    
    def _generate_reports(self):
        """生成监控报告"""
        timestamp = datetime.now()
        
        # 1. JSON 报告
        report_data = {
            "generated_at": timestamp.isoformat(),
            "project": CONFIG["project_name"],
            "monitor_version": CONFIG["version"],
            "metrics": self.metrics,
            "errors": self.errors[:50]  # 限制错误数量
        }
        
        # 确保目录存在
        monitoring_dir = self.base_path / "monitoring"
        monitoring_dir.mkdir(exist_ok=True)
        
        json_path = monitoring_dir / "performance-report.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        # 2. Markdown 报告
        md_lines = [
            "# 📊 性能监控报告",
            "",
            f"**生成时间**: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**监控版本**: {CONFIG['version']}",
            f"**构建耗时**: {self.metrics['build_time']:.2f} 秒",
            "",
            "---",
            "",
            "## 📈 关键指标",
            ""
        ]
        
        # 文档统计
        doc_data = self.metrics["documents"]
        md_lines.extend([
            "### 文档统计",
            "",
            f"- **总文档数**: {doc_data['total']}",
            f"- **总行数**: {doc_data['total_lines']:,}",
            f"- **总大小**: {doc_data['total_size_bytes'] / 1024 / 1024:.2f} MB",
            "",
            "| 目录 | 文档数 | 行数 | 大小 |",
            "|------|--------|------|------|"
        ])
        
        for dir_name, dir_stats in doc_data["by_directory"].items():
            size_mb = dir_stats["size_bytes"] / 1024 / 1024
            md_lines.append(
                f"| {dir_name} | {dir_stats['count']} | {dir_stats['lines']:,} | {size_mb:.2f} MB |"
            )
        
        md_lines.append("")
        
        # 代码示例
        code_data = self.metrics["code_examples"]
        md_lines.extend([
            "### 代码示例统计",
            "",
            f"- **代码块总数**: {code_data['total_blocks']}",
            f"- **代码总行数**: {code_data['total_lines']:,}",
            f"- **包含代码的文件**: {code_data['files_with_code']}",
            "",
            "| 语言 | 代码块数 |",
            "|------|----------|"
        ])
        
        for lang, count in sorted(code_data.get("by_language", {}).items(), 
                                   key=lambda x: x[1], reverse=True)[:10]:
            md_lines.append(f"| {lang} | {count} |")
        
        md_lines.append("")
        
        # 链接健康
        link_data = self.metrics["link_health"]
        md_lines.extend([
            "### 链接健康",
            "",
            f"- **总链接数**: {link_data['total_links']}",
            f"- **有效链接**: {link_data['valid_links']}",
            f"- **失效链接**: {link_data['broken_links']}",
            f"- **外部链接**: {link_data['external_links']}",
            f"- **内部链接**: {link_data['internal_links']}",
            f"- **健康率**: {link_data['health_rate']}%",
            ""
        ])
        
        if link_data["broken_links"] > 0:
            md_lines.extend([
                "#### ⚠️ 失效链接 (前10个)",
                "",
                "| 文件 | 目标 |",
                "|------|------|"
            ])
            for error in link_data["errors"][:10]:
                md_lines.append(f"| {error['file']} | `{error['target']}` |")
            md_lines.append("")
        
        # 形式化元素
        formal_data = self.metrics["formal_elements"]
        md_lines.extend([
            "### 形式化元素",
            "",
            f"- **总数**: {formal_data['total']}",
            "",
            "| 类型 | 数量 |",
            "|------|------|"
        ])
        
        type_names = {
            "Thm": "定理", "Def": "定义", "Lemma": "引理",
            "Prop": "命题", "Cor": "推论"
        }
        for elem_type, count in sorted(formal_data.get("by_type", {}).items(),
                                       key=lambda x: x[1], reverse=True):
            name = type_names.get(elem_type, elem_type)
            md_lines.append(f"| {name} ({elem_type}) | {count} |")
        
        md_lines.append("")
        
        # 可视化
        visual_data = self.metrics["visualizations"]
        md_lines.extend([
            "### 可视化统计",
            "",
            f"- **Mermaid 图表**: {visual_data['total_mermaid']}",
            f"- **图片**: {visual_data['total_images']}",
            f"- **含可视化文件**: {visual_data['files_with_visuals']}",
            ""
        ])
        
        # 质量评分
        quality_data = self.metrics["quality_score"]
        md_lines.extend([
            "### 质量评分",
            "",
            f"- **总体评分**: {quality_data['overall']}/100",
            f"- **完整性**: {quality_data['completeness']}/100",
            f"- **一致性**: {quality_data['consistency']}/100",
            f"- **覆盖率**: {quality_data['coverage']}/100",
            f"- **可维护性**: {quality_data['maintainability']}/100",
            ""
        ])
        
        # 告警
        alerts = self.metrics["alerts"]
        if alerts:
            md_lines.extend([
                "## 🚨 告警",
                ""
            ])
            
            severity_icons = {
                "critical": "🔴",
                "warning": "🟡",
                "info": "🔵"
            }
            
            for alert in alerts:
                icon = severity_icons.get(alert["severity"], "⚪")
                md_lines.append(
                    f"- {icon} **{alert['severity'].upper()}**: {alert['message']}"
                )
            
            md_lines.append("")
        else:
            md_lines.extend([
                "## ✅ 状态",
                "",
                "所有指标均在阈值范围内。",
                ""
            ])
        
        # 保存 Markdown 报告
        md_path = monitoring_dir / "performance-report.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_lines))
        
        # 3. 控制台输出摘要
        print("\n" + "=" * 60)
        print("监控摘要")
        print("=" * 60)
        print(f"文档总数: {doc_data['total']}")
        print(f"代码示例: {code_data['total_blocks']} 个块, {code_data['total_lines']:,} 行")
        print(f"链接健康: {link_data['health_rate']}% ({link_data['broken_links']} 失效)")
        print(f"形式化元素: {formal_data['total']}")
        print(f"质量评分: {quality_data['overall']}/100")
        print(f"告警数量: {len(alerts)}")
        print(f"构建耗时: {self.metrics['build_time']:.2f} 秒")
        print("=" * 60)
        print(f"\n报告已保存:")
        print(f"  - JSON: {json_path}")
        print(f"  - Markdown: {md_path}")


def update_metrics_history(metrics: Dict[str, Any], base_path: Path):
    """更新历史趋势数据"""
    history_path = base_path / "monitoring" / "metrics-history.json"
    
    # 读取现有历史
    history = {"records": []}
    if history_path.exists():
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            pass
    
    # 添加新记录
    record = {
        "timestamp": datetime.now().isoformat(),
        "document_count": metrics["documents"]["total"],
        "code_blocks": metrics["code_examples"]["total_blocks"],
        "link_health_rate": metrics["link_health"]["health_rate"],
        "formal_elements": metrics["formal_elements"]["total"],
        "quality_score": metrics["quality_score"]["overall"],
        "build_time": metrics["build_time"]
    }
    
    history["records"].append(record)
    
    # 保留最近 52 周的数据
    if len(history["records"]) > 52:
        history["records"] = history["records"][-52:]
    
    # 计算趋势
    if len(history["records"]) >= 2:
        current = history["records"][-1]
        previous = history["records"][-2]
        
        history["trends"] = {
            "document_growth": current["document_count"] - previous["document_count"],
            "code_growth": current["code_blocks"] - previous["code_blocks"],
            "quality_change": round(current["quality_score"] - previous["quality_score"], 2)
        }
    
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    
    print(f"\n历史数据已更新: {history_path}")


def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AnalysisDataFlow 性能监控脚本"
    )
    parser.add_argument(
        "--path", "-p",
        default=".",
        help="项目根目录路径 (默认: 当前目录)"
    )
    parser.add_argument(
        "--update-history", "-u",
        action="store_true",
        help="更新历史趋势数据"
    )
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="快速模式 (仅统计文档数量)"
    )
    
    args = parser.parse_args()
    
    monitor = PerformanceMonitor(args.path)
    metrics = monitor.run_all_checks()
    
    if args.update_history:
        update_metrics_history(metrics, Path(args.path))
    
    # 根据告警数量返回状态码
    alert_count = len(metrics.get("alerts", []))
    critical_count = sum(1 for a in metrics.get("alerts", []) if a["severity"] == "critical")
    
    if critical_count > 0:
        sys.exit(2)  # 严重告警
    elif alert_count > 0:
        sys.exit(1)  # 一般告警
    else:
        sys.exit(0)  # 正常


if __name__ == "__main__":
    main()
