#!/usr/bin/env python3
"""
Flink 版本和 FLIP 状态自动化跟踪脚本

功能:
1. 检查 Apache Flink 新版本发布
2. 跟踪 FLIP 提案状态变化
3. 自动生成版本跟踪报告
4. 更新文档状态

作者: AnalysisDataFlow 项目
版本: 2.1.0
更新日期: 2026-04-08
"""

import argparse
import json
import re
import sys
import urllib.request
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any


# 配置
FLINK_GITHUB_API = "https://api.github.com/repos/apache/flink/releases"
FLINK_JIRA_API = "https://issues.apache.org/jira/rest/api/2/search"
FLIP_WIKI_URL = "https://cwiki.apache.org/confluence/display/FLINK/Flink+Improvement+Proposals"
FLINK_ROADMAP_URL = "https://flink.apache.org/roadmap/"

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
FLINK_ROADMAP_DIR = PROJECT_ROOT / "Flink" / "08-roadmap"
META_DIR = PROJECT_ROOT / "Flink" / "00-meta"


@dataclass
class FlinkVersion:
    """Flink 版本信息"""
    version: str
    release_date: Optional[str]
    is_prerelease: bool
    html_url: str
    body: str
    
    def __str__(self) -> str:
        status = "Pre-release" if self.is_prerelease else "Stable"
        return f"Flink {self.version} ({status}) - {self.release_date or 'Unknown'}"


@dataclass
class FLIPStatus:
    """FLIP 状态信息"""
    flip_id: str
    title: str
    status: str  # Draft, Under Discussion, Accepted, Implemented, etc.
    target_version: Optional[str]
    last_updated: str
    
    def __str__(self) -> str:
        return f"{self.flip_id}: {self.title} [{self.status}] -> {self.target_version or 'TBD'}"


class FlinkReleaseTracker:
    """Flink 版本发布跟踪器"""
    
    def __init__(self, cache_file: Optional[Path] = None):
        self.cache_file = cache_file or (PROJECT_ROOT / ".cache" / "flink-releases.json")
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.versions: List[FlinkVersion] = []
        self.flips: List[FLIPStatus] = []
        
    def fetch_github_releases(self, limit: int = 10) -> List[FlinkVersion]:
        """从 GitHub API 获取最新发布版本"""
        try:
            url = f"{FLINK_GITHUB_API}?per_page={limit}"
            req = urllib.request.Request(url)
            req.add_header('Accept', 'application/vnd.github.v3+json')
            req.add_header('User-Agent', 'Flink-Release-Tracker/2.1')
            
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode())
                
            versions = []
            for release in data:
                version = FlinkVersion(
                    version=release['tag_name'].lstrip('v'),
                    release_date=release.get('published_at', '').split('T')[0] if release.get('published_at') else None,
                    is_prerelease=release.get('prerelease', False),
                    html_url=release['html_url'],
                    body=release.get('body', '')
                )
                versions.append(version)
                
            self.versions = versions
            return versions
            
        except Exception as e:
            print(f"⚠️  获取 GitHub 发布信息失败: {e}")
            return []
    
    def load_local_flips(self) -> List[FLIPStatus]:
        """从本地文档加载 FLIP 状态"""
        flips = []
        
        # 从 2.5 路线图加载
        roadmap_25 = FLINK_ROADMAP_DIR / "08.02-flink-25" / "flink-25-roadmap.md"
        if roadmap_25.exists():
            content = roadmap_25.read_text(encoding='utf-8')
            # 解析 FLIP 表格
            flips.extend(self._parse_flip_table(content, "2.5"))
        
        # 从 2.5 预览加载
        preview_25 = FLINK_ROADMAP_DIR / "08.01-flink-24" / "flink-2.5-preview.md"
        if preview_25.exists():
            content = preview_25.read_text(encoding='utf-8')
            flips.extend(self._parse_flip_content(content, "2.5"))
        
        # 从 3.0 架构文档加载
        roadmap_30 = FLINK_ROADMAP_DIR / "08.01-flink-24" / "flink-30-architecture-redesign.md"
        if roadmap_30.exists():
            content = roadmap_30.read_text(encoding='utf-8')
            flips.extend(self._parse_flip_content(content, "3.0"))
        
        self.flips = flips
        return flips
    
    def _parse_flip_table(self, content: str, target_version: str) -> List[FLIPStatus]:
        """解析 FLIP 表格"""
        flips = []
        # 简单的表格解析
        lines = content.split('\n')
        for line in lines:
            if '| FLIP-' in line and '标题' not in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 5 and 'FLIP-' in parts[1]:
                    flip_match = re.search(r'FLIP-(\d+)', parts[1])
                    if flip_match:
                        flip_id = f"FLIP-{flip_match.group(1)}"
                        title = parts[2] if len(parts) > 2 else "Unknown"
                        status = parts[4] if len(parts) > 4 else "Unknown"
                        flips.append(FLIPStatus(
                            flip_id=flip_id,
                            title=title,
                            status=status,
                            target_version=target_version,
                            last_updated=datetime.now().isoformat()
                        ))
        return flips
    
    def _parse_flip_content(self, content: str, target_version: str) -> List[FLIPStatus]:
        """解析 FLIP 内容"""
        flips = []
        # 查找 FLIP 引用
        flip_pattern = r'FLIP-(\d+)\s*[-:]\s*([^\n]+)'
        matches = re.finditer(flip_pattern, content)
        for match in matches:
            flip_id = f"FLIP-{match.group(1)}"
            title = match.group(2).strip()
            # 查找状态
            status = "Unknown"
            if '🔄' in content[match.start():match.start()+200]:
                status = "In Progress"
            elif '📋' in content[match.start():match.start()+200]:
                status = "Planned"
            elif '✅' in content[match.start():match.start()+200]:
                status = "Completed"
            
            flips.append(FLIPStatus(
                flip_id=flip_id,
                title=title,
                status=status,
                target_version=target_version,
                last_updated=datetime.now().isoformat()
            ))
        return flips
    
    def generate_report(self) -> str:
        """生成版本跟踪报告"""
        lines = []
        lines.append("# Flink 版本跟踪报告")
        lines.append(f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("\n" + "="*60)
        
        # 最新版本
        lines.append("\n## 最新发布版本\n")
        if self.versions:
            for v in self.versions[:5]:
                lines.append(f"- {v}")
        else:
            lines.append("- 无法获取版本信息")
        
        # FLIP 状态
        lines.append("\n## FLIP 状态汇总\n")
        if self.flips:
            by_version: Dict[str, List[FLIPStatus]] = {}
            for flip in self.flips:
                version = flip.target_version or "Unknown"
                by_version.setdefault(version, []).append(flip)
            
            for version in sorted(by_version.keys()):
                lines.append(f"\n### Flink {version}\n")
                for flip in by_version[version]:
                    lines.append(f"- {flip}")
        else:
            lines.append("- 无法获取 FLIP 信息")
        
        # 文档状态
        lines.append("\n## 本地文档状态\n")
        docs = [
            ("Flink 2.5 路线图", FLINK_ROADMAP_DIR / "08.02-flink-25" / "flink-25-roadmap.md"),
            ("Flink 2.5 特性预览", FLINK_ROADMAP_DIR / "08.02-flink-25" / "flink-25-features-preview.md"),
            ("Flink 2.5 迁移指南", FLINK_ROADMAP_DIR / "08.02-flink-25" / "flink-25-migration-guide.md"),
            ("Flink 2.5 预览", FLINK_ROADMAP_DIR / "08.01-flink-24" / "flink-2.5-preview.md"),
            ("Flink 3.0 架构", FLINK_ROADMAP_DIR / "08.01-flink-24" / "flink-30-architecture-redesign.md"),
            ("版本跟踪", META_DIR / "version-tracking.md"),
        ]
        
        for name, path in docs:
            status = "✅" if path.exists() else "❌"
            mtime = datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y-%m-%d') if path.exists() else "N/A"
            lines.append(f"- {status} {name} (更新: {mtime})")
        
        lines.append("\n" + "="*60)
        return '\n'.join(lines)
    
    def update_version_tracking(self) -> bool:
        """更新版本跟踪文档"""
        tracking_file = META_DIR / "version-tracking.md"
        if not tracking_file.exists():
            print(f"❌ 版本跟踪文档不存在: {tracking_file}")
            return False
        
        content = tracking_file.read_text(encoding='utf-8')
        
        # 更新生成时间
        content = re.sub(
            r'> 生成时间: \d{4}-\d{2}-\d{2}',
            f'> 生成时间: {datetime.now().strftime("%Y-%m-%d")}',
            content
        )
        
        # 更新最后更新时间
        content = re.sub(
            r'最后更新: \d{4}-\d{2}-\d{2}',
            f'最后更新: {datetime.now().strftime("%Y-%m-%d")}',
            content
        )
        
        tracking_file.write_text(content, encoding='utf-8')
        print(f"✅ 已更新: {tracking_file}")
        return True
    
    def check_for_updates(self) -> List[str]:
        """检查更新并返回通知列表"""
        notifications = []
        
        # 检查新版本
        if self.versions:
            latest = self.versions[0]
            if not latest.is_prerelease:
                # 检查是否为 2.5 或 3.0 的新发布
                if latest.version.startswith('2.5'):
                    notifications.append(f"🎉 Flink 2.5 新版本发布: {latest.version}")
                elif latest.version.startswith('3.0'):
                    notifications.append(f"🎉 Flink 3.0 新版本发布: {latest.version}")
        
        # 检查 FLIP 状态变化
        for flip in self.flips:
            if flip.status in ["Implemented", "Completed"]:
                notifications.append(f"✅ {flip.flip_id} 已完成: {flip.title}")
            elif flip.status == "In Progress" and flip.target_version == "2.5":
                notifications.append(f"🔄 {flip.flip_id} 开发中: {flip.title}")
        
        return notifications


def main():
    parser = argparse.ArgumentParser(
        description="Flink 版本和 FLIP 状态自动化跟踪工具"
    )
    parser.add_argument(
        '--check-only', 
        action='store_true',
        help='仅检查新版本，不生成报告'
    )
    parser.add_argument(
        '--report', 
        action='store_true',
        help='生成并打印跟踪报告'
    )
    parser.add_argument(
        '--update-docs', 
        action='store_true',
        help='更新版本跟踪文档'
    )
    parser.add_argument(
        '--output', 
        type=str,
        help='报告输出文件路径'
    )
    parser.add_argument(
        '--no-fetch', 
        action='store_true',
        help='不获取远程数据，仅使用本地缓存'
    )
    
    args = parser.parse_args()
    
    tracker = FlinkReleaseTracker()
    
    print("🔍 Flink 版本跟踪器 v2.1.0")
    print("="*60)
    
    # 获取数据
    if not args.no_fetch:
        print("\n📡 正在获取最新发布信息...")
        versions = tracker.fetch_github_releases()
        print(f"   获取到 {len(versions)} 个版本")
        
        for v in versions[:3]:
            print(f"   - {v}")
    
    print("\n📂 正在加载本地 FLIP 信息...")
    flips = tracker.load_local_flips()
    print(f"   加载了 {len(flips)} 个 FLIP")
    
    # 检查更新
    if args.check_only:
        print("\n🔔 更新检查:")
        notifications = tracker.check_for_updates()
        if notifications:
            for n in notifications:
                print(f"   {n}")
        else:
            print("   暂无重要更新")
        return
    
    # 生成报告
    report = tracker.generate_report()
    
    if args.report:
        print("\n" + report)
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding='utf-8')
        print(f"\n✅ 报告已保存: {output_path}")
    
    # 更新文档
    if args.update_docs:
        print("\n📝 正在更新文档...")
        tracker.update_version_tracking()
    
    print("\n" + "="*60)
    print("✨ 完成!")


if __name__ == "__main__":
    main()
