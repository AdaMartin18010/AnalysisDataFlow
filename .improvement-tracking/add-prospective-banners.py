#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前瞻性内容免责声明批量添加脚本
生成时间: 2026-04-05
任务: A2 - 统一标注所有前瞻性内容

功能:
1. 读取 prospective-content-index.json 索引文件
2. 根据文件类型选择对应免责声明模板
3. 批量添加免责声明到文件头部
4. 生成操作报告

使用方式:
    python add-prospective-banners.py [--dry-run] [--target-dir DIR]

参数:
    --dry-run       模拟运行，不实际修改文件
    --target-dir    指定目标目录（默认: 项目根目录）
    --type          仅处理指定类型 (version-feature/planned-api/concept-design)
"""

import json
import os
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 模板定义
TEMPLATES = {
    "version-feature": '''<!-- 版本状态标记: status=preview, target={version}-{quarter} -->
> ⚠️ **前瞻性声明**
> 本文档包含Flink {version}的前瞻性设计内容。Flink {version}尚未正式发布，
> 部分特性为预测/规划性质。具体实现以Apache Flink官方最终发布为准。
>
> | 属性 | 值 |
> |------|-----|
> | **文档状态** | 🔍 前瞻 (Preview) |
> | **目标版本** | {version}.0 GA |
> | **预计发布时间** | {year} {quarter} |
> | **Feature Freeze** | {freeze_date} (预估) |
> | **最后更新** | {today} |
> | **跟踪系统** | [.tasks/flink-release-tracker.md](../../.tasks/flink-release-tracker.md) |

---

''',
    "planned-api": '''<!-- 特性状态标记: status=planned{flip_attr} -->
> ⚠️ **前瞻性声明**
> 本文档描述的特性处于规划/设计阶段，尚未在Flink稳定版本中实现。
> 特性设计可能根据社区反馈和技术演进进行调整。
> 实际可用性请以官方发布说明为准。
>
> | 属性 | 值 |
> |------|-----|
> | **文档状态** | 📋 计划中 (Planned) |
> | **相关FLIP** | {flip_info} |
> | **目标版本** | {target_version} (预估) |
> | **稳定性** | 设计阶段，可能变更 |
> | **最后更新** | {today} |

---

''',
    "concept-design": '''<!-- 概念状态标记: status=concept, level={level} -->
> ⚠️ **前瞻性声明**
> 本文档内容为概念性设计和架构探索，属于技术前瞻性研究。
> 所述架构、API和实现细节不代表官方路线图，仅供技术参考和讨论。
> 实际采纳情况取决于社区共识和技术可行性验证。
>
> | 属性 | 值 |
> |------|-----|
> | **文档状态** | 🔭 概念设计 (Concept) |
> | **形式化等级** | {level} |
> | **稳定性** | 探索阶段，可能大幅变更 |
> | **参考性质** | 技术研究，非官方承诺 |
> | **最后更新** | {today} |

---

'''
}


def extract_version_from_path(path: str) -> Optional[str]:
    """从文件路径中提取Flink版本号"""
    patterns = [
        r'flink[-\s]*(\d+\.\d+)',
        r'(\d+\.\d+)[-\s]*preview',
        r'(\d+\.\d+)[-\s]*tracking',
    ]
    for pattern in patterns:
        match = re.search(pattern, path, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def extract_flip_from_content(content: str) -> Optional[str]:
    """从文件内容中提取FLIP编号"""
    patterns = [
        r'FLIP[-\s]*(\d+)',
        r'flip[-\s]*(\d+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    return None


def extract_level_from_content(content: str) -> str:
    """从文件内容中提取形式化等级"""
    match = re.search(r'形式化等级[:\s]*([Ll]\d)', content)
    if match:
        return match.group(1).upper()
    return "L3"  # 默认值


def parse_existing_header(content: str) -> tuple:
    """
    解析文件头部，返回 (前置内容, 正文内容)
    前置内容包括: HTML注释、YAML frontmatter
    """
    # 检查YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return f"---{parts[1]}---\n", parts[2].lstrip()
    
    # 检查HTML注释
    html_comment_pattern = r'^(<!--[\s\S]*?-->\s*)'
    match = re.match(html_comment_pattern, content)
    if match:
        pre_content = match.group(1)
        body_content = content[len(pre_content):].lstrip()
        return pre_content, body_content
    
    return "", content


def has_existing_banner(content: str) -> bool:
    """检查文件是否已有免责声明"""
    banner_patterns = [
        r'前瞻性声明',
        r'前瞻性内容',
        r'⚠️.*preview',
        r'⚠️.*plan',
        r'>.*免责声明',
        r'status=preview',
        r'status=planned',
        r'status=concept',
    ]
    for pattern in banner_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    return False


def generate_banner(file_info: Dict, content: str, today: str) -> str:
    """根据文件信息生成免责声明"""
    file_type = file_info.get("type", "concept-design")
    template = TEMPLATES.get(file_type, TEMPLATES["concept-design"])
    
    if file_type == "version-feature":
        version = file_info.get("target_version") or extract_version_from_path(file_info["path"]) or "X.X"
        year = "2027"  # 可根据版本推断
        quarter = "Q1-Q2"
        freeze_date = "2027-02"
        
        # 根据版本调整时间
        if version == "2.4":
            year, quarter, freeze_date = "2026", "Q2-Q3", "2026-05"
        elif version == "2.5":
            year, quarter, freeze_date = "2027", "Q1-Q2", "2027-02"
        elif version == "3.0":
            year, quarter, freeze_date = "2027", "Q3-Q4", "2027-08"
        
        return template.format(
            version=version,
            year=year,
            quarter=quarter,
            freeze_date=freeze_date,
            today=today
        )
    
    elif file_type == "planned-api":
        flip_number = extract_flip_from_content(content)
        flip_attr = f", flip={flip_number}" if flip_number else ""
        flip_info = f"FLIP-{flip_number}" if flip_number else "待定"
        target_version = file_info.get("target_version") or "待定"
        
        return template.format(
            flip_attr=flip_attr,
            flip_info=flip_info,
            target_version=target_version,
            today=today
        )
    
    else:  # concept-design
        level = extract_level_from_content(content)
        return template.format(level=level, today=today)


def process_file(file_info: Dict, base_dir: Path, dry_run: bool = True) -> Dict:
    """处理单个文件，返回处理结果"""
    result = {
        "path": file_info["path"],
        "status": "skipped",
        "reason": "",
        "backup_path": None
    }
    
    file_path = base_dir / file_info["path"]
    
    # 检查文件是否存在
    if not file_path.exists():
        result["status"] = "error"
        result["reason"] = f"文件不存在: {file_path}"
        return result
    
    try:
        # 读取文件内容
        content = file_path.read_text(encoding='utf-8')
        
        # 检查是否已有免责声明
        if has_existing_banner(content):
            result["status"] = "skipped"
            result["reason"] = "已有免责声明"
            return result
        
        # 解析文件头部
        pre_content, body_content = parse_existing_header(content)
        
        # 生成免责声明
        today = datetime.now().strftime("%Y-%m-%d")
        banner = generate_banner(file_info, content, today)
        
        # 组合新内容
        new_content = pre_content + banner + body_content
        
        if dry_run:
            result["status"] = "dry_run"
            result["reason"] = "模拟模式，未实际修改"
        else:
            # 创建备份
            backup_path = file_path.with_suffix('.md.bak')
            file_path.rename(backup_path)
            result["backup_path"] = str(backup_path)
            
            # 写入新内容
            file_path.write_text(new_content, encoding='utf-8')
            result["status"] = "success"
            result["reason"] = "成功添加免责声明"
    
    except Exception as e:
        result["status"] = "error"
        result["reason"] = f"处理异常: {str(e)}"
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="批量添加前瞻性内容免责声明",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 模拟运行（默认）
    python add-prospective-banners.py
    
    # 实际执行
    python add-prospective-banners.py --no-dry-run
    
    # 仅处理特定类型
    python add-prospective-banners.py --type version-feature
    
    # 指定目标目录
    python add-prospective-banners.py --target-dir /path/to/project
        """
    )
    parser.add_argument(
        "--no-dry-run",
        action="store_true",
        help="实际执行修改（默认模拟运行）"
    )
    parser.add_argument(
        "--target-dir",
        default=".",
        help="目标项目目录（默认: 当前目录）"
    )
    parser.add_argument(
        "--type",
        choices=["version-feature", "planned-api", "concept-design"],
        help="仅处理指定类型的文件"
    )
    parser.add_argument(
        "--index-file",
        default="prospective-content-index.json",
        help="索引文件路径（默认: prospective-content-index.json）"
    )
    
    args = parser.parse_args()
    
    dry_run = not args.no_dry_run
    base_dir = Path(args.target_dir).resolve()
    index_path = base_dir / ".improvement-tracking" / args.index_file
    
    print("=" * 60)
    print("前瞻性内容免责声明批量添加工具")
    print("=" * 60)
    print(f"运行模式: {'模拟运行' if dry_run else '实际执行'}")
    print(f"目标目录: {base_dir}")
    print(f"索引文件: {index_path}")
    print("=" * 60)
    
    # 加载索引文件
    if not index_path.exists():
        print(f"错误: 索引文件不存在: {index_path}")
        return 1
    
    with open(index_path, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
    
    files = index_data.get("files", [])
    
    # 过滤文件类型
    if args.type:
        files = [f for f in files if f.get("type") == args.type]
        print(f"过滤类型: {args.type}")
    
    # 仅处理 missing-banner 的文件
    files_to_process = [f for f in files if f.get("status") == "missing-banner"]
    
    print(f"总计文件: {len(files)}")
    print(f"待处理文件: {len(files_to_process)}")
    print("=" * 60)
    
    if not files_to_process:
        print("没有需要处理的文件。")
        return 0
    
    # 处理文件
    results = []
    for i, file_info in enumerate(files_to_process, 1):
        print(f"\n[{i}/{len(files_to_process)}] 处理: {file_info['path']}")
        result = process_file(file_info, base_dir, dry_run)
        results.append(result)
        print(f"    状态: {result['status']}")
        print(f"    说明: {result['reason']}")
    
    # 生成报告
    print("\n" + "=" * 60)
    print("处理结果统计")
    print("=" * 60)
    
    status_counts = {}
    for r in results:
        status = r["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    
    # 保存详细报告
    report_path = base_dir / ".improvement-tracking" / "banner-addition-report.json"
    report_data = {
        "generated_at": datetime.now().isoformat(),
        "dry_run": dry_run,
        "target_dir": str(base_dir),
        "summary": status_counts,
        "results": results
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细报告已保存: {report_path}")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())
