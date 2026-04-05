#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前瞻性声明横幅添加脚本
用于自动为 Flink 未来版本相关文档添加前瞻性声明

用法:
    python add-prospective-banners.py --scan          # 扫描并生成报告
    python add-prospective-banners.py --dry-run       # 预览修改（不实际写入）
    python add-prospective-banners.py --apply         # 实际执行修改
    python add-prospective-banners.py --check <file>  # 检查单个文件
"""

import os
import re
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# ============ 配置 ============

PROJECT_ROOT = Path("e:/_src/AnalysisDataFlow")
FLINK_DIR = PROJECT_ROOT / "Flink"
TEMPLATE_PATH = PROJECT_ROOT / ".templates/prospective-banner.md"

# 需要扫描的目录模式
SCAN_PATTERNS = [
    "Flink/08-roadmap/**/*.md",
    "Flink/06-ai-ml/flip-531*.md",
    "Flink/06-ai-ml/flink-ai-agents*.md",
    "Flink/00-meta/version-tracking/*.md",
]

# 关键词匹配规则 (正则表达式)
KEYWORD_PATTERNS = {
    "Flink 3.0": re.compile(r"Flink\s*3\.[0-9]", re.IGNORECASE),
    "Flink 2.5": re.compile(r"Flink\s*2\.[5-9]", re.IGNORECASE),
    "Flink 2.4": re.compile(r"Flink\s*2\.4", re.IGNORECASE),
    "roadmap": re.compile(r"roadmap|路线图", re.IGNORECASE),
    "preview": re.compile(r"preview|预览", re.IGNORECASE),
    "future": re.compile(r"future|upcoming|即将到来", re.IGNORECASE),
    "前瞻": re.compile(r"前瞻|前瞻性"),
}

# 前瞻性声明检测模式
BANNER_PATTERNS = [
    re.compile(r"前瞻性声明|Prospective Content|⚠️\s*\*\*前瞻"),
]

# 版本到置信度的映射
VERSION_CONFIDENCE = {
    "Flink 3.0": ("🔴 低", "规划中"),
    "Flink 2.5": ("🟡 中", "开发中"),
    "Flink 2.4": ("🟢 高", "即将发布"),
}

# ============ 数据类 ============

@dataclass
class DocumentInfo:
    """文档信息"""
    path: Path
    relative_path: str
    detected_versions: List[str]
    matched_keywords: List[str]
    has_banner: bool
    flip_numbers: List[str]
    confidence: str = "🟡 中"
    release_status: str = "规划中"


@dataclass
class ProcessingReport:
    """处理报告"""
    scanned: int
    needs_banner: int
    already_has_banner: int
    flink_30_docs: int
    flink_25_docs: int
    flink_24_docs: int
    documents: List[DocumentInfo]


# ============ 核心函数 ============

def extract_flip_numbers(content: str) -> List[str]:
    """从文档内容提取 FLIP 编号"""
    flip_pattern = re.compile(r"FLIP[-\s]*(\d+)", re.IGNORECASE)
    matches = flip_pattern.findall(content)
    return sorted(set([f"FLIP-{m}" for m in matches]))

def detect_flink_version(content: str) -> Tuple[List[str], List[str]]:
    """
    检测文档中提到的 Flink 版本
    返回: (版本列表, 匹配的关键词列表)
    """
    versions = []
    keywords = []
    
    for keyword, pattern in KEYWORD_PATTERNS.items():
        if pattern.search(content):
            keywords.append(keyword)
            if keyword.startswith("Flink"):
                versions.append(keyword)
    
    return versions, keywords

def has_prospective_banner(content: str) -> bool:
    """检查文档是否已有前瞻性声明"""
    for pattern in BANNER_PATTERNS:
        if pattern.search(content):
            return True
    return False

def get_confidence_and_status(versions: List[str]) -> Tuple[str, str]:
    """根据版本获取置信度和发布状态"""
    if not versions:
        return "🟡 中", "规划中"
    
    # 取最低版本（即最前瞻的）
    for version_key in ["Flink 3.0", "Flink 2.5", "Flink 2.4"]:
        if any(version_key in v for v in versions):
            return VERSION_CONFIDENCE.get(version_key, ("🟡 中", "规划中"))
    
    return "🟡 中", "规划中"

def generate_banner(doc_info: DocumentInfo, date_str: str) -> str:
    """生成前瞻性声明横幅"""
    version = doc_info.detected_versions[0] if doc_info.detected_versions else "X.X"
    version_num = version.replace("Flink ", "") if version else "X.X"
    
    flip_str = ", ".join(doc_info.flip_numbers) if doc_info.flip_numbers else "无"
    
    banner = f"""> ⚠️ **前瞻性声明 (Prospective Content)**
> 本文档包含 **Flink {version_num}** 的前瞻性设计内容。Flink {version_num} 尚未正式发布，
> 部分特性为预测/规划性质，具体实现以 Apache Flink 官方最终发布为准。
> 
> | 属性 | 值 |
> |------|-----|
> | 📅 最后更新 | {date_str} |
> | 🚀 预期发布 | {doc_info.release_status} |
> | 🎯 内容置信度 | {doc_info.confidence} |
> | 📌 相关 FLIP | {flip_str} |
> 
> **置信度说明:**
> - 🟢 **高**: 已合入主干/官方确认
> - 🟡 **中**: FLIP 已接受/社区共识
> - 🔴 **低**: 早期讨论/概念阶段

---

"""
    return banner

def find_insert_position(content: str) -> int:
    """
    找到在文档中插入横幅的位置
    通常在第一个标题之后
    """
    # 查找第一个一级标题 (# Title)
    title_pattern = re.compile(r'^(# .+)$', re.MULTILINE)
    match = title_pattern.search(content)
    
    if match:
        # 在标题行之后插入，跳过空行
        pos = match.end()
        # 跳过标题后的空行
        while pos < len(content) and content[pos] == '\n':
            pos += 1
        return pos
    
    return 0

def scan_document(file_path: Path) -> Optional[DocumentInfo]:
    """扫描单个文档"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ⚠️ 无法读取文件 {file_path}: {e}")
        return None
    
    # 检测版本和关键词
    versions, keywords = detect_flink_version(content)
    
    # 如果没有检测到前瞻性相关内容，跳过
    if not versions and not any(k in ["roadmap", "preview", "future", "前瞻"] for k in keywords):
        return None
    
    # 检查是否已有横幅
    banner_exists = has_prospective_banner(content)
    
    # 提取 FLIP 编号
    flips = extract_flip_numbers(content)
    
    # 确定置信度和发布状态
    confidence, status = get_confidence_and_status(versions)
    
    # 计算相对路径
    relative_path = str(file_path.relative_to(PROJECT_ROOT)).replace('\\', '/')
    
    return DocumentInfo(
        path=file_path,
        relative_path=relative_path,
        detected_versions=versions,
        matched_keywords=keywords,
        has_banner=banner_exists,
        flip_numbers=flips,
        confidence=confidence,
        release_status=status
    )

def scan_all_documents() -> ProcessingReport:
    """扫描所有文档"""
    documents = []
    scanned = 0
    needs_banner = 0
    already_has_banner = 0
    flink_30_count = 0
    flink_25_count = 0
    flink_24_count = 0
    
    print("🔍 开始扫描文档...")
    
    # 收集所有需要扫描的文件
    files_to_scan = set()
    
    for pattern in SCAN_PATTERNS:
        glob_pattern = pattern.replace("Flink/", str(FLINK_DIR) + "/")
        for file_path in PROJECT_ROOT.glob(pattern):
            if file_path.is_file() and file_path.suffix == '.md':
                files_to_scan.add(file_path)
    
    # 额外扫描包含关键词的文档
    for md_file in FLINK_DIR.rglob("*.md"):
        scanned += 1
        doc_info = scan_document(md_file)
        if doc_info:
            documents.append(doc_info)
            if doc_info.has_banner:
                already_has_banner += 1
            else:
                needs_banner += 1
            
            # 统计各版本文档数
            if any("Flink 3.0" in v for v in doc_info.detected_versions):
                flink_30_count += 1
            elif any("Flink 2.5" in v for v in doc_info.detected_versions):
                flink_25_count += 1
            elif any("Flink 2.4" in v for v in doc_info.detected_versions):
                flink_24_count += 1
    
    print(f"   扫描完成: 共 {scanned} 个文件")
    
    return ProcessingReport(
        scanned=scanned,
        needs_banner=needs_banner,
        already_has_banner=already_has_banner,
        flink_30_docs=flink_30_count,
        flink_25_docs=flink_25_count,
        flink_24_docs=flink_24_count,
        documents=documents
    )

def add_banner_to_file(doc_info: DocumentInfo, dry_run: bool = True) -> bool:
    """为文档添加横幅"""
    try:
        with open(doc_info.path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ 无法读取文件: {e}")
        return False
    
    # 再次检查是否已有横幅
    if has_prospective_banner(content):
        print(f"  ⏭️  已存在横幅，跳过")
        return False
    
    # 生成横幅
    date_str = datetime.now().strftime("%Y-%m-%d")
    banner = generate_banner(doc_info, date_str)
    
    # 找到插入位置
    insert_pos = find_insert_position(content)
    
    # 插入横幅
    new_content = content[:insert_pos] + "\n" + banner + content[insert_pos:]
    
    if dry_run:
        print(f"  📝 [Dry Run] 将添加横幅到: {doc_info.relative_path}")
        return True
    else:
        try:
            with open(doc_info.path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✅ 已添加横幅: {doc_info.relative_path}")
            return True
        except Exception as e:
            print(f"  ❌ 写入失败: {e}")
            return False

def generate_report(report: ProcessingReport, output_file: Optional[Path] = None):
    """生成扫描报告"""
    lines = []
    
    lines.append("# 前瞻性声明横幅 - 扫描报告")
    lines.append("")
    lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## 📊 统计概览")
    lines.append("")
    lines.append(f"| 指标 | 数量 |")
    lines.append(f"|------|------|")
    lines.append(f"| 扫描文档总数 | {report.scanned} |")
    lines.append(f"| 需要添加横幅 | {report.needs_banner} |")
    lines.append(f"| 已有横幅 | {report.already_has_banner} |")
    lines.append(f"| Flink 3.0 相关 | {report.flink_30_docs} |")
    lines.append(f"| Flink 2.5 相关 | {report.flink_25_docs} |")
    lines.append(f"| Flink 2.4 相关 | {report.flink_24_docs} |")
    lines.append("")
    
    # 按版本分组
    lines.append("## 📁 需要处理的文档清单")
    lines.append("")
    
    # Flink 3.0 文档
    lines.append("### Flink 3.0 相关 (高优先级)")
    lines.append("")
    flink_30_docs = [d for d in report.documents if any("Flink 3.0" in v for v in d.detected_versions) and not d.has_banner]
    if flink_30_docs:
        for doc in flink_30_docs:
            flips = ", ".join(doc.flip_numbers) if doc.flip_numbers else "无"
            lines.append(f"- [ ] `{doc.relative_path}` | 置信度: {doc.confidence} | FLIP: {flips}")
    else:
        lines.append("- 无需处理")
    lines.append("")
    
    # Flink 2.5 文档
    lines.append("### Flink 2.5 相关")
    lines.append("")
    flink_25_docs = [d for d in report.documents if any("Flink 2.5" in v for v in d.detected_versions) and not d.has_banner]
    if flink_25_docs:
        for doc in flink_25_docs:
            flips = ", ".join(doc.flip_numbers) if doc.flip_numbers else "无"
            lines.append(f"- [ ] `{doc.relative_path}` | 置信度: {doc.confidence} | FLIP: {flips}")
    else:
        lines.append("- 无需处理")
    lines.append("")
    
    # Flink 2.4 文档
    lines.append("### Flink 2.4 相关")
    lines.append("")
    flink_24_docs = [d for d in report.documents if any("Flink 2.4" in v for v in d.detected_versions) and not d.has_banner]
    if flink_24_docs:
        for doc in flink_24_docs:
            flips = ", ".join(doc.flip_numbers) if doc.flip_numbers else "无"
            lines.append(f"- [ ] `{doc.relative_path}` | 置信度: {doc.confidence} | FLIP: {flips}")
    else:
        lines.append("- 无需处理")
    lines.append("")
    
    # 其他前瞻性文档
    lines.append("### 其他前瞻性文档 (roadmap/preview/future)")
    lines.append("")
    other_docs = [d for d in report.documents if not d.detected_versions and not d.has_banner]
    if other_docs:
        for doc in other_docs[:20]:  # 限制数量
            keywords = ", ".join(doc.matched_keywords)
            lines.append(f"- [ ] `{doc.relative_path}` | 关键词: {keywords}")
        if len(other_docs) > 20:
            lines.append(f"- ... 还有 {len(other_docs) - 20} 个文档")
    else:
        lines.append("- 无需处理")
    lines.append("")
    
    # 已有横幅的文档
    lines.append("## ✅ 已有前瞻性声明的文档")
    lines.append("")
    has_banner_docs = [d for d in report.documents if d.has_banner]
    if has_banner_docs:
        for doc in has_banner_docs:
            lines.append(f"- `{doc.relative_path}`")
    else:
        lines.append("- 无")
    lines.append("")
    
    # 使用说明
    lines.append("## 🚀 后续操作")
    lines.append("")
    lines.append("```bash")
    lines.append("# 预览修改（不实际写入）")
    lines.append("python scripts/add-prospective-banners.py --dry-run")
    lines.append("")
    lines.append("# 执行实际修改")
    lines.append("python scripts/add-prospective-banners.py --apply")
    lines.append("```")
    lines.append("")
    
    report_text = "\n".join(lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"\n📄 报告已保存: {output_file}")
    
    return report_text

def main():
    parser = argparse.ArgumentParser(
        description="为 Flink 前瞻性文档添加统一声明横幅",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python add-prospective-banners.py --scan          # 扫描并生成报告
    python add-prospective-banners.py --dry-run       # 预览修改
    python add-prospective-banners.py --apply         # 执行修改
    python add-prospective-banners.py --check <file>  # 检查单个文件
        """
    )
    
    parser.add_argument("--scan", action="store_true", help="扫描文档并生成报告")
    parser.add_argument("--dry-run", action="store_true", help="预览修改但不写入")
    parser.add_argument("--apply", action="store_true", help="执行实际修改")
    parser.add_argument("--check", metavar="FILE", help="检查单个文件")
    parser.add_argument("--report", metavar="FILE", default="prospective-report.md", help="报告输出路径")
    
    args = parser.parse_args()
    
    if args.check:
        # 检查单个文件
        file_path = Path(args.check)
        if not file_path.exists():
            file_path = PROJECT_ROOT / args.check
        
        if not file_path.exists():
            print(f"❌ 文件不存在: {args.check}")
            sys.exit(1)
        
        doc_info = scan_document(file_path)
        if doc_info:
            print(f"\n📄 {doc_info.relative_path}")
            print(f"   检测版本: {doc_info.detected_versions}")
            print(f"   匹配关键词: {doc_info.matched_keywords}")
            print(f"   FLIP 编号: {doc_info.flip_numbers}")
            print(f"   已有横幅: {'是' if doc_info.has_banner else '否'}")
            print(f"   置信度: {doc_info.confidence}")
        else:
            print("ℹ️ 该文档不包含前瞻性内容")
        return
    
    # 扫描所有文档
    report = scan_all_documents()
    
    print(f"\n📊 扫描结果:")
    print(f"   总文档数: {report.scanned}")
    print(f"   需要横幅: {report.needs_banner}")
    print(f"   已有横幅: {report.already_has_banner}")
    print(f"   Flink 3.0: {report.flink_30_docs}")
    print(f"   Flink 2.5: {report.flink_25_docs}")
    print(f"   Flink 2.4: {report.flink_24_docs}")
    
    # 生成报告
    report_path = PROJECT_ROOT / "reports" / args.report
    report_path.parent.mkdir(exist_ok=True)
    generate_report(report, report_path)
    
    # 执行修改
    if args.dry_run or args.apply:
        docs_to_process = [d for d in report.documents if not d.has_banner]
        
        if not docs_to_process:
            print("\n✅ 没有需要处理的文档")
            return
        
        mode = "[预览模式]" if args.dry_run else "[执行模式]"
        print(f"\n🚀 {mode} 开始处理 {len(docs_to_process)} 个文档...")
        
        success_count = 0
        for doc in docs_to_process:
            if add_banner_to_file(doc, dry_run=args.dry_run):
                success_count += 1
        
        print(f"\n{'='*50}")
        print(f"处理完成: {success_count}/{len(docs_to_process)}")
        
        if args.dry_run:
            print("\n💡 使用 --apply 参数执行实际修改")

if __name__ == "__main__":
    main()
