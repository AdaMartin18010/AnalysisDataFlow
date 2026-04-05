#!/usr/bin/env python3
"""
文档内容新鲜度标记自动化脚本

功能:
- 扫描指定目录的 Markdown 文件
- 检测是否已有新鲜度标记
- 为缺失标记的文档添加标准模板
- 生成更新报告

用法:
    python scripts/add-doc-status.py [options]

示例:
    # 扫描所有高优先级目录
    python scripts/add-doc-status.py

    # 仅扫描指定目录
    python scripts/add-doc-status.py --dirs "Flink/08-roadmap,Flink/06-ai-ml"

    # 预览模式（不实际修改文件）
    python scripts/add-doc-status.py --dry-run

    # 生成详细报告
    python scripts/add-doc-status.py --report
"""

import os
import re
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class DocStatus(Enum):
    """文档状态枚举"""
    STABLE = ("🟢", "稳定", "stable")
    PREVIEW = ("🟡", "预览", "preview")
    OUTDATED = ("🔴", "过时", "outdated")
    
    def __init__(self, emoji: str, cn_name: str, en_name: str):
        self.emoji = emoji
        self.cn_name = cn_name
        self.en_name = en_name
    
    @classmethod
    def from_string(cls, s: str) -> "DocStatus":
        """从字符串解析状态"""
        s_lower = s.lower()
        for status in cls:
            if s_lower in [status.cn_name, status.en_name, status.emoji]:
                return status
        return cls.STABLE


class ConfidenceLevel(Enum):
    """置信度评级枚举"""
    HIGH = ("高", "high")
    MEDIUM = ("中", "medium")
    LOW = ("低", "low")
    
    def __init__(self, cn_name: str, en_name: str):
        self.cn_name = cn_name
        self.en_name = en_name
    
    @classmethod
    def from_string(cls, s: str) -> "ConfidenceLevel":
        """从字符串解析置信度"""
        s_lower = s.lower()
        for level in cls:
            if s_lower in [level.cn_name, level.en_name]:
                return level
        return cls.MEDIUM


@dataclass
class DocStatusHeader:
    """文档状态标记数据结构"""
    status: DocStatus
    last_updated: str
    version: str
    confidence: ConfidenceLevel
    tags: List[str]
    
    def to_markdown(self) -> str:
        """转换为 Markdown 格式"""
        tags_str = ", ".join(self.tags) if self.tags else ""
        return f"""\
> **文档状态**: {self.status.emoji} {self.status.cn_name}  
> **最后更新**: {self.last_updated}  
> **技术版本**: {self.version}  
> **置信度**: {self.confidence.cn_name}  
> **标签**: {tags_str}

---

"""


@dataclass
class ScanResult:
    """扫描结果数据结构"""
    file_path: str
    has_status_header: bool
    suggested_status: Optional[DocStatus] = None
    suggested_confidence: Optional[ConfidenceLevel] = None
    suggested_version: Optional[str] = None
    suggested_tags: Optional[List[str]] = None
    existing_header: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "file_path": self.file_path,
            "has_status_header": self.has_status_header,
            "suggested_status": self.suggested_status.cn_name if self.suggested_status else None,
            "suggested_confidence": self.suggested_confidence.cn_name if self.suggested_confidence else None,
            "suggested_version": self.suggested_version,
            "suggested_tags": self.suggested_tags,
            "existing_header": self.existing_header
        }


class DocStatusMarker:
    """文档状态标记器"""
    
    # 状态标记检测正则
    STATUS_PATTERN = re.compile(
        r'^\s*>\s*\*\*文档状态\*\*\s*[:：]\s*([🟢🟡🔴])\s*(稳定|预览|过时的?)',
        re.MULTILINE | re.IGNORECASE
    )
    
    # 原有版本标记检测（兼容性）
    LEGACY_STATUS_PATTERN = re.compile(
        r'^\s*<!--\s*版本状态标记[^>]*-->',
        re.MULTILINE | re.IGNORECASE
    )
    
    # 目录优先级映射
    DIR_PRIORITY = {
        "Flink/08-roadmap": {"status": DocStatus.PREVIEW, "confidence": ConfidenceLevel.LOW, "version": "Flink 2.4+"},
        "Flink/06-ai-ml": {"status": DocStatus.PREVIEW, "confidence": ConfidenceLevel.MEDIUM, "version": "Flink 2.3+"},
        "Knowledge/06-frontier": {"status": DocStatus.PREVIEW, "confidence": ConfidenceLevel.MEDIUM, "version": "通用"},
        "Struct": {"status": DocStatus.STABLE, "confidence": ConfidenceLevel.HIGH, "version": "通用"},
        "Knowledge/01-fundamentals": {"status": DocStatus.STABLE, "confidence": ConfidenceLevel.HIGH, "version": "通用"},
        "Knowledge/02-concepts": {"status": DocStatus.STABLE, "confidence": ConfidenceLevel.HIGH, "version": "通用"},
        "Knowledge/03-models": {"status": DocStatus.STABLE, "confidence": ConfidenceLevel.HIGH, "version": "通用"},
        "Knowledge/04-systems": {"status": DocStatus.STABLE, "confidence": ConfidenceLevel.HIGH, "version": "Flink 1.18+"},
        "Knowledge/05-patterns": {"status": DocStatus.STABLE, "confidence": ConfidenceLevel.HIGH, "version": "Flink 1.18+"},
        "Flink/01-introduction": {"status": DocStatus.STABLE, "confidence": ConfidenceLevel.HIGH, "version": "通用"},
        "Flink/02-core": {"status": DocStatus.STABLE, "confidence": ConfidenceLevel.HIGH, "version": "Flink 1.18+"},
        "Flink/03-runtime": {"status": DocStatus.STABLE, "confidence": ConfidenceLevel.HIGH, "version": "Flink 1.18+"},
        "Flink/04-deployment": {"status": DocStatus.STABLE, "confidence": ConfidenceLevel.HIGH, "version": "Flink 1.18+"},
        "Flink/05-operations": {"status": DocStatus.STABLE, "confidence": ConfidenceLevel.HIGH, "version": "Flink 1.18+"},
        "Flink/07-ecosystem": {"status": DocStatus.STABLE, "confidence": ConfidenceLevel.HIGH, "version": "Flink 1.18+"},
    }
    
    # 文件名关键词映射
    FILE_KEYWORDS = {
        "roadmap": {"status": DocStatus.PREVIEW, "tags": ["roadmap"]},
        "preview": {"status": DocStatus.PREVIEW, "tags": ["preview"]},
        "tracking": {"status": DocStatus.PREVIEW, "tags": ["tracking"]},
        "flip": {"status": DocStatus.PREVIEW, "tags": ["flip", "proposal"]},
        "ai": {"status": DocStatus.PREVIEW, "tags": ["ai", "ml"]},
        "agent": {"status": DocStatus.PREVIEW, "tags": ["ai-agent"]},
        "llm": {"status": DocStatus.PREVIEW, "tags": ["llm", "ai"]},
        "frontier": {"status": DocStatus.PREVIEW, "tags": ["frontier"]},
        "experimental": {"status": DocStatus.PREVIEW, "tags": ["experimental"]},
    }
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.results: List[ScanResult] = []
        self.today = datetime.now().strftime("%Y-%m-%d")
    
    def has_status_header(self, content: str) -> bool:
        """检查文档是否已有状态标记"""
        return bool(self.STATUS_PATTERN.search(content))
    
    def has_legacy_header(self, content: str) -> bool:
        """检查文档是否有旧版本标记"""
        return bool(self.LEGACY_STATUS_PATTERN.search(content))
    
    def extract_legacy_info(self, content: str) -> Optional[Dict]:
        """从旧版本标记中提取信息"""
        # 尝试提取状态
        status_match = re.search(r'status=([^,\s]+)', content, re.IGNORECASE)
        target_match = re.search(r'target=([^\s]+)', content, re.IGNORECASE)
        
        info = {}
        if status_match:
            status_str = status_match.group(1).lower()
            if "preview" in status_str or "前瞻" in status_str:
                info["status"] = DocStatus.PREVIEW
            elif "stable" in status_str or "稳定" in status_str:
                info["status"] = DocStatus.STABLE
            elif "outdated" in status_str or "过时" in status_str:
                info["status"] = DocStatus.OUTDATED
        
        if target_match:
            info["target"] = target_match.group(1)
        
        return info if info else None
    
    def suggest_tags(self, file_path: Path, content: str) -> List[str]:
        """根据文件路径和内容建议标签"""
        tags = set()
        file_name_lower = file_path.stem.lower()
        content_lower = content.lower()
        
        # 基于文件名关键词
        for keyword, info in self.FILE_KEYWORDS.items():
            if keyword in file_name_lower:
                tags.update(info.get("tags", []))
        
        # 基于目录结构
        path_str = str(file_path.relative_to(self.project_root)).lower()
        if "flink" in path_str:
            tags.add("flink")
        if "roadmap" in path_str:
            tags.add("roadmap")
        if "ai-ml" in path_str or "ai/ml" in path_str:
            tags.add("ai-ml")
        if "frontier" in path_str:
            tags.add("frontier")
        if "struct" in path_str:
            tags.add("theory")
        if "knowledge" in path_str:
            tags.add("knowledge")
        
        # 基于内容关键词
        if "checkpoint" in content_lower:
            tags.add("checkpoint")
        if "watermark" in content_lower:
            tags.add("watermark")
        if "state" in content_lower:
            tags.add("state-management")
        if "exactly-once" in content_lower:
            tags.add("exactly-once")
        if "sql" in content_lower:
            tags.add("sql")
        if "table api" in content_lower:
            tags.add("table-api")
        
        return sorted(list(tags))
    
    def suggest_defaults(self, file_path: Path, content: str) -> Tuple[DocStatus, ConfidenceLevel, str, List[str]]:
        """根据文件路径和内容建议默认值"""
        rel_path = file_path.relative_to(self.project_root)
        path_str = str(rel_path).replace("\\", "/")
        
        # 提取旧版本信息（如果存在）
        legacy_info = self.extract_legacy_info(content) if self.has_legacy_header(content) else None
        
        # 基于目录的默认设置
        status = DocStatus.STABLE
        confidence = ConfidenceLevel.HIGH
        version = "通用"
        
        for dir_pattern, defaults in sorted(self.DIR_PRIORITY.items(), key=lambda x: -len(x[0])):
            if dir_pattern in path_str:
                status = defaults.get("status", status)
                confidence = defaults.get("confidence", confidence)
                version = defaults.get("version", version)
                break
        
        # 应用旧版本信息覆盖
        if legacy_info:
            if "status" in legacy_info:
                status = legacy_info["status"]
        
        # 生成标签
        tags = self.suggest_tags(file_path, content)
        
        # 根据内容长度调整置信度
        if len(content) < 1000:  # 非常短的文档
            confidence = ConfidenceLevel.LOW
        
        return status, confidence, version, tags
    
    def scan_file(self, file_path: Path) -> ScanResult:
        """扫描单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"警告: 无法读取文件 {file_path}: {e}")
            return ScanResult(
                file_path=str(file_path.relative_to(self.project_root)),
                has_status_header=False,
                existing_header=None
            )
        
        has_header = self.has_status_header(content)
        has_legacy = self.has_legacy_header(content)
        
        result = ScanResult(
            file_path=str(file_path.relative_to(self.project_root)),
            has_status_header=has_header
        )
        
        if not has_header:
            status, confidence, version, tags = self.suggest_defaults(file_path, content)
            result.suggested_status = status
            result.suggested_confidence = confidence
            result.suggested_version = version
            result.suggested_tags = tags
            
            if has_legacy:
                result.existing_header = "检测到旧版本状态标记 (HTML注释格式)"
        
        return result
    
    def scan_directory(self, directory: str, recursive: bool = True) -> List[ScanResult]:
        """扫描目录"""
        dir_path = self.project_root / directory
        if not dir_path.exists():
            print(f"警告: 目录不存在: {dir_path}")
            return []
        
        results = []
        pattern = "**/*.md" if recursive else "*.md"
        
        for file_path in dir_path.glob(pattern):
            if file_path.is_file():
                result = self.scan_file(file_path)
                results.append(result)
        
        return results
    
    def add_status_header(self, file_path: Path, result: ScanResult, dry_run: bool = False) -> bool:
        """为文件添加状态标记"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"错误: 无法读取文件 {file_path}: {e}")
            return False
        
        # 如果已有标记，跳过
        if self.has_status_header(content):
            print(f"  跳过 (已有标记): {file_path.name}")
            return False
        
        # 创建状态标记头
        header = DocStatusHeader(
            status=result.suggested_status or DocStatus.STABLE,
            last_updated=self.today,
            version=result.suggested_version or "通用",
            confidence=result.suggested_confidence or ConfidenceLevel.MEDIUM,
            tags=result.suggested_tags or []
        )
        
        header_md = header.to_markdown()
        
        # 查找插入位置（在第一个标题之前，或保留旧注释之后）
        lines = content.split('\n')
        insert_index = 0
        
        # 跳过开头的空行
        while insert_index < len(lines) and not lines[insert_index].strip():
            insert_index += 1
        
        # 如果第一行是旧版本注释，保留它
        if insert_index < len(lines) and lines[insert_index].strip().startswith('<!--'):
            # 找到注释结束位置
            while insert_index < len(lines) and '-->' not in lines[insert_index]:
                insert_index += 1
            insert_index += 1
            # 跳过注释后的空行
            while insert_index < len(lines) and not lines[insert_index].strip():
                insert_index += 1
        
        # 插入状态标记
        new_lines = lines[:insert_index] + [''] + header_md.split('\n') + lines[insert_index:]
        new_content = '\n'.join(new_lines)
        
        if dry_run:
            print(f"  [预览] 将添加标记到: {file_path.name}")
            return True
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  已添加标记: {file_path.name}")
            return True
        except Exception as e:
            print(f"错误: 无法写入文件 {file_path}: {e}")
            return False
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """生成扫描报告"""
        total = len(self.results)
        with_header = sum(1 for r in self.results if r.has_status_header)
        without_header = total - with_header
        
        report_lines = [
            "# 文档内容新鲜度标记扫描报告",
            "",
            f"**生成时间**: {self.today}",
            f"**项目根目录**: {self.project_root}",
            "",
            "## 统计摘要",
            "",
            f"- **总文档数**: {total}",
            f"- **已有标记**: {with_header}",
            f"- **需要添加标记**: {without_header}",
            f"- **覆盖率**: {(with_header/total*100):.1f}%" if total > 0 else "- **覆盖率**: N/A",
            "",
            "## 优先级文档清单",
            "",
            "### 高优先级（需要尽快标记）",
            "",
        ]
        
        # 按优先级分组
        high_priority = []
        standard_priority = []
        
        for result in self.results:
            path_lower = result.file_path.lower()
            if any(p in path_lower for p in ["08-roadmap", "06-ai-ml", "06-frontier"]):
                high_priority.append(result)
            else:
                standard_priority.append(result)
        
        # 高优先级 - 需要添加标记
        report_lines.append("#### 缺失标记的文档")
        report_lines.append("")
        report_lines.append("| 文件路径 | 建议状态 | 建议置信度 | 建议版本 | 建议标签 |")
        report_lines.append("|----------|----------|------------|----------|----------|")
        
        for result in sorted(high_priority, key=lambda x: x.file_path):
            if not result.has_status_header:
                status = result.suggested_status.cn_name if result.suggested_status else "-"
                confidence = result.suggested_confidence.cn_name if result.suggested_confidence else "-"
                version = result.suggested_version or "-"
                tags = ", ".join(result.suggested_tags) if result.suggested_tags else "-"
                report_lines.append(f"| {result.file_path} | {status} | {confidence} | {version} | {tags} |")
        
        report_lines.append("")
        report_lines.append("#### 已有标记的文档")
        report_lines.append("")
        
        for result in sorted(high_priority, key=lambda x: x.file_path):
            if result.has_status_header:
                report_lines.append(f"- ✅ {result.file_path}")
        
        # 标准优先级
        report_lines.append("")
        report_lines.append("### 标准优先级")
        report_lines.append("")
        report_lines.append(f"共 {len(standard_priority)} 个文档，其中需要添加标记 {sum(1 for r in standard_priority if not r.has_status_header)} 个")
        report_lines.append("")
        
        # 详细列表
        report_lines.append("## 完整文档列表")
        report_lines.append("")
        report_lines.append("| 文件路径 | 状态 | 备注 |")
        report_lines.append("|----------|------|------|")
        
        for result in sorted(self.results, key=lambda x: x.file_path):
            status = "✅ 已有" if result.has_status_header else "⚠️ 缺失"
            note = result.existing_header if result.existing_header else ""
            report_lines.append(f"| {result.file_path} | {status} | {note} |")
        
        # JSON 数据
        report_lines.append("")
        report_lines.append("## JSON 数据")
        report_lines.append("")
        report_lines.append("```json")
        report_lines.append(json.dumps([r.to_dict() for r in self.results], indent=2, ensure_ascii=False))
        report_lines.append("```")
        
        report_content = '\n'.join(report_lines)
        
        if output_file:
            output_path = self.project_root / output_file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"\n报告已保存: {output_path}")
        
        return report_content


def main():
    parser = argparse.ArgumentParser(
        description="文档内容新鲜度标记自动化脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 扫描所有高优先级目录
    python scripts/add-doc-status.py
    
    # 仅扫描指定目录
    python scripts/add-doc-status.py --dirs "Flink/08-roadmap,Flink/06-ai-ml"
    
    # 预览模式（不实际修改文件）
    python scripts/add-doc-status.py --dry-run
    
    # 生成详细报告
    python scripts/add-doc-status.py --report --report-file reports/doc-status-report.md
        """
    )
    
    parser.add_argument(
        "--dirs",
        type=str,
        default="Flink/08-roadmap,Flink/06-ai-ml,Knowledge/06-frontier",
        help="要扫描的目录，用逗号分隔 (默认: Flink/08-roadmap,Flink/06-ai-ml,Knowledge/06-frontier)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="扫描所有 Markdown 文档 (包括 Struct, Knowledge, Flink)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览模式，不实际修改文件"
    )
    
    parser.add_argument(
        "--apply",
        action="store_true",
        help="实际应用标记到缺失的文档"
    )
    
    parser.add_argument(
        "--report",
        action="store_true",
        help="生成详细报告"
    )
    
    parser.add_argument(
        "--report-file",
        type=str,
        default="reports/doc-status-report.md",
        help="报告输出文件路径 (默认: reports/doc-status-report.md)"
    )
    
    parser.add_argument(
        "--root",
        type=str,
        default=".",
        help="项目根目录 (默认: 当前目录)"
    )
    
    args = parser.parse_args()
    
    # 初始化标记器
    marker = DocStatusMarker(project_root=args.root)
    
    # 确定扫描目录
    if args.all:
        directories = ["Struct", "Knowledge", "Flink"]
    else:
        directories = [d.strip() for d in args.dirs.split(",")]
    
    print(f"开始扫描目录: {', '.join(directories)}")
    print("-" * 60)
    
    # 扫描所有目录
    for directory in directories:
        print(f"\n扫描: {directory}")
        results = marker.scan_directory(directory, recursive=True)
        marker.results.extend(results)
        print(f"  找到 {len(results)} 个 Markdown 文件")
    
    print("\n" + "=" * 60)
    print(f"扫描完成: 共 {len(marker.results)} 个文档")
    
    # 统计
    with_header = sum(1 for r in marker.results if r.has_status_header)
    without_header = len(marker.results) - with_header
    print(f"  - 已有标记: {with_header}")
    print(f"  - 需要添加标记: {without_header}")
    
    # 应用标记
    if args.apply:
        print("\n" + "=" * 60)
        print("开始添加标记...")
        print("-" * 60)
        
        applied_count = 0
        for result in marker.results:
            if not result.has_status_header:
                file_path = marker.project_root / result.file_path
                if marker.add_status_header(file_path, result, dry_run=args.dry_run):
                    applied_count += 1
        
        mode_str = "[预览模式] " if args.dry_run else ""
        print(f"\n{mode_str}已处理 {applied_count} 个文档")
    
    # 生成报告
    if args.report:
        print("\n" + "=" * 60)
        print("生成报告...")
        marker.generate_report(output_file=args.report_file)
    
    print("\n完成!")


if __name__ == "__main__":
    main()
