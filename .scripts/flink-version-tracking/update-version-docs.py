#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink Version Documentation Updater

自动更新版本跟踪文档，包括：
- 更新 PROJECT-VERSION-TRACKING.md
- 更新 FLIP 状态表
- 更新发布时间表
- 更新兼容性矩阵

作者: Flink Version Tracker
版本: 1.0.0
"""

import json
import logging
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# =============================================================================
# 配置和日志
# =============================================================================

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """配置日志记录器"""
    logger = logging.getLogger("doc-updater")
    logger.setLevel(getattr(logging, log_level.upper()))
    logger.handlers.clear()
    
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def load_config(config_path: str = "config.json") -> Dict:
    """加载配置文件"""
    default_config = {
        "storage": {
            "data_dir": "./data",
            "flip_cache_file": "flip_cache.json",
            "release_cache_file": "release_cache.json"
        },
        "docs": {
            "project_root": "../..",
            "version_tracking_file": "PROJECT-VERSION-TRACKING.md",
            "flink_dir": "Flink"
        }
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                    elif isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            if sub_key not in config[key]:
                                config[key][sub_key] = sub_value
                return config
        except (json.JSONDecodeError, IOError) as e:
            logging.warning(f"无法加载配置: {e}")
    
    return default_config


# =============================================================================
# 文档更新器
# =============================================================================

class DocumentationUpdater:
    """文档更新主控制器"""
    
    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        
        # 路径配置
        self.project_root = Path(config.get("docs", {}).get("project_root", "../.."))
        self.data_dir = Path(config.get("storage", {}).get("data_dir", "./data"))
        
        # 文件路径
        self.version_tracking_file = self.project_root / config.get("docs", {}).get(
            "version_tracking_file", "PROJECT-VERSION-TRACKING.md"
        )
        self.flink_dir = self.project_root / config.get("docs", {}).get("flink_dir", "Flink")
        
        # 缓存文件
        self.flip_cache = self.data_dir / config.get("storage", {}).get("flip_cache_file", "flip_cache.json")
        self.release_cache = self.data_dir / config.get("storage", {}).get("release_cache_file", "release_cache.json")
    
    def load_flip_data(self) -> List[Dict]:
        """加载 FLIP 数据"""
        if not self.flip_cache.exists():
            self.logger.warning(f"FLIP 缓存不存在: {self.flip_cache}")
            return []
        
        try:
            with open(self.flip_cache, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return list(data.get("flips", {}).values())
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error(f"加载 FLIP 数据失败: {e}")
            return []
    
    def load_release_data(self) -> List[Dict]:
        """加载发布数据"""
        if not self.release_cache.exists():
            self.logger.warning(f"Release 缓存不存在: {self.release_cache}")
            return []
        
        try:
            with open(self.release_cache, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return list(data.get("releases", {}).values())
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error(f"加载 Release 数据失败: {e}")
            return []
    
    def generate_flip_status_table(self, flips: List[Dict]) -> str:
        """
        生成 FLIP 状态表
        
        Args:
            flips: FLIP 数据列表
            
        Returns:
            Markdown 表格字符串
        """
        # 按状态分组
        status_order = ["implemented", "accepted", "under_discussion", "draft", "released", "withdrawn", "rejected"]
        
        # 排序
        sorted_flips = sorted(flips, key=lambda f: (
            status_order.index(f.get("status", "unknown")) if f.get("status") in status_order else 99,
            f.get("number", 0)
        ))
        
        lines = [
            "## FLIP 状态概览",
            "",
            f"> 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "| FLIP | 标题 | 状态 | 作者 | 目标版本 | 组件 |",
            "|------|------|------|------|----------|------|"
        ]
        
        status_emoji = {
            "implemented": "✅",
            "accepted": "🟢",
            "under_discussion": "🟡",
            "draft": "⚪",
            "released": "🚀",
            "withdrawn": "⚪",
            "rejected": "❌",
            "unknown": "❓"
        }
        
        for flip in sorted_flips[:100]:  # 限制数量
            flip_id = f"FLIP-{flip.get('number', '?')}"
            title = flip.get('title', 'Unknown')[:50]
            status = flip.get('status', 'unknown')
            author = flip.get('author', 'Unknown')[:20]
            target = flip.get('target_version', '-') or '-'
            component = flip.get('component', '-') or '-'
            
            emoji = status_emoji.get(status, '❓')
            
            # 创建链接
            url = flip.get('url', '')
            if url:
                flip_link = f"[{flip_id}]({url})"
            else:
                flip_link = flip_id
            
            lines.append(f"| {flip_link} | {title} | {emoji} {status} | {author} | {target} | {component} |")
        
        lines.append("")
        lines.append(f"*共 {len(flips)} 个 FLIP*")
        lines.append("")
        
        return '\n'.join(lines)
    
    def generate_release_timeline(self, releases: List[Dict]) -> str:
        """
        生成发布时间表
        
        Args:
            releases: 发布数据列表
            
        Returns:
            Markdown 字符串
        """
        # 过滤和排序
        valid_releases = [
            r for r in releases
            if r.get('version') and r.get('release_date')
        ]
        
        # 按版本号降序
        valid_releases.sort(
            key=lambda r: [int(x) for x in r['version'].split('.')[:3] if x.isdigit()] + [0] * (3 - len(r['version'].split('.'))),
            reverse=True
        )
        
        lines = [
            "## Flink 发布时间表",
            "",
            f"> 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "| 版本 | 发布日期 | 状态 | 下载 | 发布说明 |",
            "|------|----------|------|------|----------|"
        ]
        
        for rel in valid_releases[:50]:
            version = rel.get('version', 'Unknown')
            date = rel.get('release_date', '-')
            
            # 判断状态
            is_stable = rel.get('is_stable', True)
            status = "✅ 稳定版" if is_stable else "🧪 预览版"
            
            # 链接
            maven_url = rel.get('maven_url', '')
            notes_url = rel.get('release_notes_url', '')
            
            download_link = f"[Maven]({maven_url})" if maven_url else '-'
            notes_link = f"[Release Notes]({notes_url})" if notes_url else '-'
            
            lines.append(f"| {version} | {date} | {status} | {download_link} | {notes_link} |")
        
        lines.append("")
        lines.append(f"*共 {len(valid_releases)} 个版本*")
        lines.append("")
        
        return '\n'.join(lines)
    
    def generate_status_summary(self, flips: List[Dict], releases: List[Dict]) -> str:
        """生成状态摘要"""
        # FLIP 统计
        flip_status = {}
        for flip in flips:
            status = flip.get('status', 'unknown')
            flip_status[status] = flip_status.get(status, 0) + 1
        
        # 发布统计
        stable_count = sum(1 for r in releases if r.get('is_stable', True))
        
        lines = [
            "## 版本跟踪摘要",
            "",
            f"**最后更新**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "### FLIP 统计",
            ""
        ]
        
        for status, count in sorted(flip_status.items()):
            lines.append(f"- {status}: {count}")
        
        lines.extend([
            f"- **总计**: {len(flips)} 个 FLIP",
            "",
            "### 版本发布统计",
            "",
            f"- 稳定版本: {stable_count}",
            f"- 总版本数: {len(releases)}",
            ""
        ])
        
        return '\n'.join(lines)
    
    def update_version_tracking_doc(self) -> bool:
        """
        更新版本跟踪文档
        
        Returns:
            是否成功
        """
        if not self.version_tracking_file.exists():
            self.logger.warning(f"文档不存在，将创建: {self.version_tracking_file}")
            return self._create_version_tracking_doc()
        
        try:
            # 读取现有内容
            with open(self.version_tracking_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 加载数据
            flips = self.load_flip_data()
            releases = self.load_release_data()
            
            self.logger.info(f"加载了 {len(flips)} 个 FLIP, {len(releases)} 个版本")
            
            # 生成新内容
            summary = self.generate_status_summary(flips, releases)
            flip_table = self.generate_flip_status_table(flips)
            release_timeline = self.generate_release_timeline(releases)
            
            # 替换或插入内容
            content = self._replace_or_insert_section(content, "版本跟踪摘要", summary)
            content = self._replace_or_insert_section(content, "FLIP 状态概览", flip_table)
            content = self._replace_or_insert_section(content, "Flink 发布时间表", release_timeline)
            
            # 保存
            with open(self.version_tracking_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"文档已更新: {self.version_tracking_file}")
            return True
            
        except IOError as e:
            self.logger.error(f"更新文档失败: {e}")
            return False
    
    def _create_version_tracking_doc(self) -> bool:
        """创建新的版本跟踪文档"""
        try:
            flips = self.load_flip_data()
            releases = self.load_release_data()
            
            content_lines = [
                "# Flink 版本跟踪",
                "",
                "本文档自动跟踪 Apache Flink 的版本发布和 FLIP 状态。",
                "",
                "<!-- 自动生成的内容开始 -->",
                self.generate_status_summary(flips, releases),
                self.generate_flip_status_table(flips),
                self.generate_release_timeline(releases),
                "<!-- 自动生成的内容结束 -->",
                "",
                "---",
                "",
                "*本文档由自动化脚本生成，请勿手动编辑此部分。*"
            ]
            
            # 确保目录存在
            self.version_tracking_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.version_tracking_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(content_lines))
            
            self.logger.info(f"文档已创建: {self.version_tracking_file}")
            return True
            
        except IOError as e:
            self.logger.error(f"创建文档失败: {e}")
            return False
    
    def _replace_or_insert_section(self, content: str, section_title: str, new_section: str) -> str:
        """
        替换或插入文档章节
        
        Args:
            content: 原始内容
            section_title: 章节标题
            new_section: 新章节内容
            
        Returns:
            更新后的内容
        """
        # 尝试查找章节
        pattern = rf'(## {re.escape(section_title)}.*?)(?=\n## |\Z)'
        
        if re.search(pattern, content, re.DOTALL):
            # 替换现有章节
            content = re.sub(pattern, new_section + '\n\n', content, flags=re.DOTALL)
        else:
            # 在文件末尾插入
            content = content.rstrip() + '\n\n' + new_section + '\n'
        
        return content
    
    def update_flip_status_in_docs(self) -> bool:
        """
        更新 Flink 目录下的 FLIP 状态文档
        
        Returns:
            是否成功
        """
        if not self.flink_dir.exists():
            self.logger.warning(f"Flink 目录不存在: {self.flink_dir}")
            return False
        
        flips = self.load_flip_data()
        
        # 查找所有 FLIP 相关文档
        updated_count = 0
        
        for md_file in self.flink_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 查找文档中引用的 FLIP
                flip_refs = re.findall(r'FLIP[-\s]*(\d+)', content, re.IGNORECASE)
                
                if flip_refs:
                    updated = self._update_flip_refs_in_doc(content, flip_refs, flips)
                    if updated != content:
                        with open(md_file, 'w', encoding='utf-8') as f:
                            f.write(updated)
                        updated_count += 1
                        
            except IOError as e:
                self.logger.error(f"处理文件 {md_file} 失败: {e}")
        
        self.logger.info(f"更新了 {updated_count} 个文档")
        return updated_count > 0
    
    def _update_flip_refs_in_doc(self, content: str, flip_refs: List[str], all_flips: List[Dict]) -> str:
        """更新文档中的 FLIP 引用"""
        flip_map = {str(f.get('number')): f for f in all_flips}
        
        for ref in set(flip_refs):
            flip = flip_map.get(ref)
            if not flip:
                continue
            
            # 查找现有的 FLIP 引用
            status = flip.get('status', 'unknown')
            url = flip.get('url', '')
            
            # 如果已经有链接，跳过
            if f'FLIP-{ref}]' in content:
                continue
            
            # 添加状态标记
            status_mark = {
                "implemented": "✅",
                "accepted": "🟢",
                "under_discussion": "🟡",
                "draft": "⚪",
                "released": "🚀",
                "withdrawn": "⚪",
                "rejected": "❌"
            }.get(status, "")
            
            # 替换引用
            if url and status_mark:
                pattern = rf'FLIP[-\s]*{ref}(?!\])'
                replacement = f"[{status_mark} FLIP-{ref}]({url})"
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        return content
    
    def generate_changelog_entry(self) -> Optional[str]:
        """
        生成变更日志条目
        
        Returns:
            变更日志字符串
        """
        flips = self.load_flip_data()
        releases = self.load_release_data()
        
        if not flips and not releases:
            return None
        
        # 加载上次更新时间
        last_update = None
        changelog_file = self.data_dir / "version_changelog.json"
        if changelog_file.exists():
            try:
                with open(changelog_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get("history"):
                        last_update = data["history"][-1].get("timestamp")
            except (json.JSONDecodeError, IOError):
                pass
        
        lines = [
            f"## 更新 {datetime.now().strftime('%Y-%m-%d')}",
            ""
        ]
        
        # 新版本
        recent_releases = [
            r for r in releases
            if not last_update or r.get('discovered_at', '') > last_update
        ]
        
        if recent_releases:
            lines.extend(["### 新版本", ""])
            for rel in sorted(recent_releases, key=lambda x: x.get('version', '')):
                lines.append(f"- **{rel.get('version')}** ({rel.get('release_date', 'unknown')})")
            lines.append("")
        
        # FLIP 变更
        recent_flips = [
            f for f in flips
            if not last_update or f.get('updated_date', '') > last_update
        ]
        
        if recent_flips:
            lines.extend(["### FLIP 更新", ""])
            for flip in recent_flips[:10]:
                lines.append(f"- FLIP-{flip.get('number')}: {flip.get('title', 'Unknown')} [{flip.get('status', 'unknown')}]")
            lines.append("")
        
        return '\n'.join(lines) if len(lines) > 2 else None


# =============================================================================
# 命令行接口
# =============================================================================

def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Flink Version Doc Updater - 自动更新版本跟踪文档",
        epilog="""
示例:
  %(prog)s                          # 更新所有文档
  %(prog)s --only-version-tracking  # 只更新版本跟踪文档
  %(prog)s --only-flip-docs         # 只更新 FLIP 引用
  %(prog)s --generate-changelog     # 生成变更日志
        """
    )
    
    parser.add_argument("-c", "--config", default="config.json",
                        help="配置文件路径")
    parser.add_argument("--only-version-tracking", action="store_true",
                        help="只更新版本跟踪文档")
    parser.add_argument("--only-flip-docs", action="store_true",
                        help="只更新 FLIP 引用")
    parser.add_argument("--generate-changelog", action="store_true",
                        help="生成变更日志条目")
    parser.add_argument("-l", "--log-level", default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    
    args = parser.parse_args()
    
    # 设置日志
    logger = setup_logging(args.log_level)
    
    # 加载配置
    config = load_config(args.config)
    
    # 创建更新器
    updater = DocumentationUpdater(config, logger)
    
    logger.info("=" * 60)
    logger.info("Flink Version Doc Updater v1.0")
    logger.info("=" * 60)
    
    success = True
    
    # 执行更新
    if args.generate_changelog:
        changelog = updater.generate_changelog_entry()
        if changelog:
            print("\n生成的变更日志:")
            print(changelog)
        else:
            print("\n无新变更")
    
    elif args.only_version_tracking:
        success = updater.update_version_tracking_doc()
    
    elif args.only_flip_docs:
        success = updater.update_flip_status_in_docs()
    
    else:
        # 全部更新
        success1 = updater.update_version_tracking_doc()
        success2 = updater.update_flip_status_in_docs()
        success = success1 and success2
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
