#!/usr/bin/env python3
"""
Flink 版本发布后文档批量更新脚本

功能:
- 批量更新前瞻文档的状态标记
- 更新代码示例中的版本标记
- 添加发布日期和官方链接
- 生成更新报告

用法:
    python update-docs-on-release.py --old-version 2.4-preview --new-version 2.4 --ga-date 2026-10-15
    python update-docs-on-release.py --version 2.4 --dry-run  # 预览变更
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class UpdateResult:
    """更新结果数据类"""
    file_path: Path
    changes: List[Tuple[str, str, str]]  # (类型, 旧值, 新值)
    success: bool
    error: str = ""


class DocUpdater:
    """文档更新器"""
    
    def __init__(self, base_dir: Path, dry_run: bool = False):
        self.base_dir = base_dir
        self.dry_run = dry_run
        self.results: List[UpdateResult] = []
        
    def find_preview_docs(self, version: str) -> List[Path]:
        """查找指定版本的前瞻文档"""
        docs = []
        flink_dir = self.base_dir / "Flink"
        
        if not flink_dir.exists():
            print(f"Warning: {flink_dir} does not exist")
            return docs
            
        for md_file in flink_dir.rglob("*.md"):
            content = md_file.read_text(encoding='utf-8')
            # 检查是否包含版本前瞻标记
            if f"status=preview" in content and version in content:
                docs.append(md_file)
            elif f"status: preview" in content and version in content:
                docs.append(md_file)
            elif f"{version}-preview" in content:
                docs.append(md_file)
                
        return sorted(docs)
    
    def update_status_markers(self, content: str, old_version: str, new_version: str, 
                              ga_date: str) -> Tuple[str, List[Tuple[str, str, str]]]:
        """更新状态标记"""
        changes = []
        
        # 1. 更新 HTML 注释标记
        pattern1 = rf'<!-- 版本状态标记: status=preview[^-]*-->'
        replacement1 = f'<!-- 版本状态标记: status=released, ga={ga_date} -->'
        if re.search(pattern1, content):
            content = re.sub(pattern1, replacement1, content)
            changes.append(("status_marker", "preview", f"released (ga={ga_date})"))
        
        # 2. 更新表格中的文档状态
        pattern2 = r'\*\*文档状态\*\*\s*\|\s*🔍 前瞻 \(Preview\)'
        replacement2 = '**文档状态** | ✅ 已更新 (Updated)'
        if re.search(pattern2, content):
            content = re.sub(pattern2, replacement2, content)
            changes.append(("doc_status", "🔍 前瞻 (Preview)", "✅ 已更新 (Updated)"))
        
        # 3. 更新目标版本/发布版本
        pattern3 = r'\*\*目标版本\*\*\s*\|\s*Flink ([\d.]+)'
        def replace_target(match):
            return f'**发布版本** | {match.group(1)} GA'
        if re.search(pattern3, content):
            content = re.sub(pattern3, replace_target, content)
            changes.append(("version_label", "目标版本", "发布版本"))
        
        # 4. 更新预计发布时间/发布日期
        pattern4 = r'\*\*预计发布时间\*\*\s*\|\s*([\d\sQ-]+)'
        if re.search(pattern4, content):
            content = re.sub(pattern4, f'**发布日期** | {ga_date}', content)
            changes.append(("release_date", "预计发布时间", ga_date))
        
        # 5. 更新元数据中的状态
        pattern5 = r'\*\*状态\*\*:\s*preview'
        if re.search(pattern5, content):
            content = re.sub(pattern5, '**状态**: released', content)
            changes.append(("meta_status", "preview", "released"))
        
        # 6. 更新前瞻声明
        pattern6 = r'> ⚠️ \*\*前瞻性声明\*\*\n> 本文档包含Flink ([\d.]+)的前瞻性设计内容[^\n]*\n> 部分特性为预测/规划性质[^\n]*'
        replacement6 = f'''> ✅ **版本已发布**
> Flink {new_version}.0 已于 {ga_date} 正式发布。'''
        if re.search(pattern6, content, re.DOTALL):
            content = re.sub(pattern6, replacement6, content, flags=re.DOTALL)
            changes.append(("header_notice", "前瞻性声明", "版本已发布"))
        
        return content, changes
    
    def update_code_markers(self, content: str, old_version: str, 
                           new_version: str) -> Tuple[str, List[Tuple[str, str, str]]]:
        """更新代码示例中的版本标记"""
        changes = []
        
        # 1. 更新代码注释中的前瞻标记
        pattern1 = rf'\[Flink {re.escape(old_version)} 前瞻\]'
        replacement1 = f'[Flink {new_version}]'
        if re.search(pattern1, content):
            content = re.sub(pattern1, replacement1, content)
            changes.append(("code_comment", f"[Flink {old_version} 前瞻]", f"[Flink {new_version}]"))
        
        # 2. 更新 since 标记
        pattern2 = rf'since:\s*{re.escape(old_version)}-preview'
        replacement2 = f'since: {new_version}'
        if re.search(pattern2, content):
            content = re.sub(pattern2, replacement2, content)
            changes.append(("since_marker", f"{old_version}-preview", new_version))
        
        # 3. 更新 since 标记 (方括号格式)
        pattern3 = rf'since {re.escape(old_version)}-preview'
        replacement3 = f'since {new_version}'
        if re.search(pattern3, content):
            content = re.sub(pattern3, replacement3, content)
            changes.append(("since_marker2", f"{old_version}-preview", new_version))
        
        # 4. 更新版本声明
        pattern4 = r'版本\*\*:\s*([\d.]+)-preview'
        replacement4 = f'**版本**: {new_version}'
        if re.search(pattern4, content):
            content = re.sub(pattern4, replacement4, content)
            changes.append(("version_meta", f"{new_version}-preview", new_version))
        
        return content, changes
    
    def add_official_links(self, content: str, version: str) -> Tuple[str, List[Tuple[str, str, str]]]:
        """添加官方发布链接"""
        changes = []
        
        # 检查是否已存在官方发布链接
        if "github.com/apache/flink/releases" not in content:
            # 在表格后添加官方链接
            pattern = r'(\| \*\*跟踪系统\*\* \| .* \|\n)'
            replacement = r'''\1> | **官方发布** | [GitHub Release](https://github.com/apache/flink/releases/tag/release-{version}) |
> | **Maven Central** | [flink-core:{version}](https://search.maven.org/artifact/org.apache.flink/flink-core/{version}) |
'''.format(version=version)
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes.append(("official_links", "", "added"))
        
        return content, changes
    
    def update_file(self, file_path: Path, old_version: str, new_version: str, 
                   ga_date: str) -> UpdateResult:
        """更新单个文件"""
        try:
            content = file_path.read_text(encoding='utf-8')
            all_changes = []
            
            # 应用所有更新
            content, changes1 = self.update_status_markers(content, old_version, new_version, ga_date)
            all_changes.extend(changes1)
            
            content, changes2 = self.update_code_markers(content, old_version, new_version)
            all_changes.extend(changes2)
            
            content, changes3 = self.add_official_links(content, new_version)
            all_changes.extend(changes3)
            
            # 写入文件 (如果不是 dry-run)
            if not self.dry_run and all_changes:
                file_path.write_text(content, encoding='utf-8')
                print(f"  Updated: {file_path.relative_to(self.base_dir)}")
            elif all_changes:
                print(f"  Would update: {file_path.relative_to(self.base_dir)}")
            
            return UpdateResult(
                file_path=file_path,
                changes=all_changes,
                success=True
            )
            
        except Exception as e:
            return UpdateResult(
                file_path=file_path,
                changes=[],
                success=False,
                error=str(e)
            )
    
    def run(self, old_version: str, new_version: str, ga_date: str) -> Dict:
        """运行批量更新"""
        print(f"\n{'='*60}")
        print(f"Flink 文档批量更新")
        print(f"{'='*60}")
        print(f"Old version: {old_version}")
        print(f"New version: {new_version}")
        print(f"GA date: {ga_date}")
        print(f"Dry run: {self.dry_run}")
        print(f"{'='*60}\n")
        
        # 查找所有前瞻文档
        print(f"查找 {old_version} 的前瞻文档...")
        docs = self.find_preview_docs(old_version)
        print(f"找到 {len(docs)} 个文档\n")
        
        if not docs:
            print("未找到需要更新的文档")
            return {"total": 0, "updated": 0, "errors": 0}
        
        # 更新每个文档
        print("开始更新文档...")
        for doc in docs:
            result = self.update_file(doc, old_version, new_version, ga_date)
            self.results.append(result)
        
        # 生成报告
        return self.generate_report()
    
    def generate_report(self) -> Dict:
        """生成更新报告"""
        updated = sum(1 for r in self.results if r.success and r.changes)
        errors = sum(1 for r in self.results if not r.success)
        total = len(self.results)
        
        print(f"\n{'='*60}")
        print("更新报告")
        print(f"{'='*60}")
        print(f"总文档数: {total}")
        print(f"已更新: {updated}")
        print(f"错误: {errors}")
        print(f"{'='*60}\n")
        
        # 详细变更列表
        if any(r.changes for r in self.results):
            print("详细变更:")
            for result in self.results:
                if result.changes:
                    print(f"\n  {result.file_path.name}:")
                    for change_type, old_val, new_val in result.changes:
                        print(f"    - {change_type}: {old_val} → {new_val}")
                elif not result.success:
                    print(f"\n  {result.file_path.name}: ERROR - {result.error}")
        
        return {
            "total": total,
            "updated": updated,
            "errors": errors,
            "results": self.results
        }


def main():
    parser = argparse.ArgumentParser(
        description="Flink 版本发布后文档批量更新脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 预览变更 (不实际修改)
    python update-docs-on-release.py --version 2.4 --dry-run
    
    # 执行实际更新
    python update-docs-on-release.py --old-version 2.4-preview --new-version 2.4 --ga-date 2026-10-15
    
    # 只更新特定文件
    python update-docs-on-release.py --version 2.4 --files Flink/08-roadmap/flink-2.4-tracking.md
        """
    )
    
    parser.add_argument(
        "--old-version",
        help="旧版本标记 (如: 2.4-preview)"
    )
    parser.add_argument(
        "--new-version",
        help="新版本号 (如: 2.4)"
    )
    parser.add_argument(
        "--version",
        help="简写版本 (自动推导 old=new-preview, new=version)"
    )
    parser.add_argument(
        "--ga-date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="GA发布日期 (格式: YYYY-MM-DD, 默认: 今天)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览变更但不实际修改文件"
    )
    parser.add_argument(
        "--base-dir",
        default="../..",
        help="项目根目录 (默认: ../../)"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        help="指定要更新的文件路径 (默认: 自动查找所有前瞻文档)"
    )
    
    args = parser.parse_args()
    
    # 处理简写版本
    if args.version:
        old_version = f"{args.version}-preview"
        new_version = args.version
    elif args.old_version and args.new_version:
        old_version = args.old_version
        new_version = args.new_version
    else:
        parser.error("必须提供 --version 或同时提供 --old-version 和 --new-version")
    
    # 创建更新器并运行
    base_dir = Path(args.base_dir).resolve()
    updater = DocUpdater(base_dir, dry_run=args.dry_run)
    
    result = updater.run(old_version, new_version, args.ga_date)
    
    # 返回码
    if result["errors"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
