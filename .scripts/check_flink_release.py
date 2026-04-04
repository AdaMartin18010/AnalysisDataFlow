#!/usr/bin/env python3
"""
Flink Release Checker - Apache Flink 版本发布检测系统

功能:
- 检测 Flink 2.4/2.5/3.0 官方发布状态
- 监控 Maven Central、GitHub Releases、官方下载页面
- 检测 RC 版本、GA 版本发布
- 生成跟踪报告和通知

用法:
    python check_flink_release.py [选项]

返回码:
    0 - 无更新
    1 - 有新版本发布
    2 - 执行错误

作者: AnalysisDataFlow 项目
版本: 1.0.0
日期: 2026-04-04
"""

import argparse
import json
import logging
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
import os

# 默认配置
DEFAULT_CONFIG = {
    "tracked_versions": ["2.4", "2.5", "3.0"],
    "maven_group": "org.apache.flink",
    "maven_artifact": "flink-core",
    "github_repo": "apache/flink",
    "flink_website": "https://flink.apache.org",
    "check_rc": True,
    "check_snapshots": False,
    "timeout": 30,
    "output_dir": ".stats/flink-tracking",
    "cache_file": ".link-checker-cache/flink-release-cache.json",
    "notification_enabled": False,
    "notification_webhook": None
}

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VersionType(Enum):
    """版本类型枚举"""
    GA = "ga"           # General Availability
    RC = "rc"           # Release Candidate
    SNAPSHOT = "snapshot"
    UNKNOWN = "unknown"


class ReleaseStatus(Enum):
    """发布状态枚举"""
    UPCOMING = "upcoming"       # 尚未发布
    RC_AVAILABLE = "rc"         # RC版本可用
    GA_RELEASED = "ga"          # GA已发布
    TRACKING = "tracking"       # 持续跟踪


@dataclass
class VersionInfo:
    """版本信息数据类"""
    version: str
    full_version: str
    version_type: str
    major_minor: str
    release_date: Optional[str] = None
    source: str = ""
    url: str = ""
    is_new: bool = False
    release_notes_url: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class TrackedVersion:
    """跟踪版本数据类"""
    version: str                      # 如 "2.4"
    expected_release: str             # 预计发布时间
    actual_release: Optional[str] = None
    status: str = "upcoming"          # upcoming, rc, ga
    latest_version: Optional[str] = None
    latest_rc: Optional[str] = None
    flips: List[str] = field(default_factory=list)
    docs_updated: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "version": self.version,
            "expected_release": self.expected_release,
            "actual_release": self.actual_release,
            "status": self.status,
            "latest_version": self.latest_version,
            "latest_rc": self.latest_rc,
            "flips": self.flips,
            "docs_updated": self.docs_updated
        }


@dataclass
class TrackingReport:
    """跟踪报告数据类"""
    check_time: str
    has_updates: bool
    tracked_versions: List[str]
    versions: Dict[str, TrackedVersion]
    new_releases: List[VersionInfo]
    rc_versions: List[VersionInfo]
    upcoming_versions: List[Dict]
    all_discovered: List[VersionInfo]
    recommendations: List[str]
    errors: List[str]
    
    def to_dict(self) -> Dict:
        return {
            "check_time": self.check_time,
            "has_updates": self.has_updates,
            "tracked_versions": self.tracked_versions,
            "versions": {k: v.to_dict() for k, v in self.versions.items()},
            "new_releases": [v.to_dict() for v in self.new_releases],
            "rc_versions": [v.to_dict() for v in self.rc_versions],
            "upcoming_versions": self.upcoming_versions,
            "all_discovered_count": len(self.all_discovered),
            "recommendations": self.recommendations,
            "errors": self.errors
        }


class FlinkReleaseChecker:
    """Flink 版本发布检测器"""
    
    def __init__(self, config: Dict):
        self.config = {**DEFAULT_CONFIG, **config}
        self.tracked_prefixes = self.config["tracked_versions"]
        self.timeout = self.config["timeout"]
        self.errors: List[str] = []
        self.all_discovered_versions: List[VersionInfo] = []
        self.tracked_versions: Dict[str, TrackedVersion] = {}
        
        # 初始化跟踪版本
        self._init_tracked_versions()
        
        # 确保输出目录存在
        os.makedirs(self.config["output_dir"], exist_ok=True)
        
    def _init_tracked_versions(self):
        """初始化跟踪版本配置"""
        tracked_config = {
            "2.4": {
                "expected_release": "2026 Q3-Q4",
                "flips": ["FLIP-531", "FLIP-540", "FLIP-541", "FLIP-542", 
                         "FLIP-543", "FLIP-544", "FLIP-545", "FLIP-546"]
            },
            "2.5": {
                "expected_release": "2027 Q1-Q2",
                "flips": ["FLIP-550", "FLIP-551", "FLIP-552", "FLIP-553"]
            },
            "3.0": {
                "expected_release": "2027 Q1-Q2",
                "flips": ["FLIP-600", "FLIP-601", "FLIP-602"]
            }
        }
        
        for version in self.tracked_prefixes:
            config = tracked_config.get(version, {})
            self.tracked_versions[version] = TrackedVersion(
                version=version,
                expected_release=config.get("expected_release", "TBD"),
                flips=config.get("flips", [])
            )
    
    def _http_get(self, url: str, headers: Optional[Dict] = None) -> Optional[str]:
        """执行HTTP GET请求"""
        try:
            req = urllib.request.Request(
                url,
                headers=headers or {"User-Agent": "Flink-Release-Checker/1.0 (AnalysisDataFlow Project)"}
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return resp.read().decode('utf-8')
        except urllib.error.URLError as e:
            self.errors.append(f"HTTP Error for {url}: {e}")
            logger.warning(f"HTTP Error for {url}: {e}")
            return None
        except Exception as e:
            self.errors.append(f"Unexpected error for {url}: {e}")
            logger.error(f"Unexpected error for {url}: {e}")
            return None
    
    def _parse_version(self, version_str: str) -> Tuple[str, VersionType]:
        """解析版本字符串，返回(major.minor, 版本类型)"""
        version_lower = version_str.lower()
        
        # 检测版本类型
        if "-snapshot" in version_lower:
            vtype = VersionType.SNAPSHOT
        elif "-rc" in version_lower:
            vtype = VersionType.RC
        elif re.match(r'^\d+\.\d+\.\d+$', version_str):
            vtype = VersionType.GA
        else:
            vtype = VersionType.UNKNOWN
        
        # 提取 major.minor
        match = re.match(r'^(\d+\.\d+)', version_str)
        major_minor = match.group(1) if match else ""
        
        return major_minor, vtype
    
    def _is_tracked_version(self, major_minor: str) -> bool:
        """检查版本是否在跟踪列表中"""
        return any(major_minor == tracked or major_minor.startswith(tracked) 
                   for tracked in self.tracked_prefixes)
    
    def check_maven_central(self) -> List[VersionInfo]:
        """检查Maven Central获取最新版本"""
        logger.info("Checking Maven Central...")
        versions = []
        
        group = self.config["maven_group"]
        artifact = self.config["maven_artifact"]
        url = f"https://search.maven.org/solrsearch/select?q=g:{group}+AND+a:{artifact}&core=gav&rows=100&wt=json"
        
        response = self._http_get(url)
        if not response:
            return versions
        
        try:
            data = json.loads(response)
            docs = data.get("response", {}).get("docs", [])
            
            for doc in docs:
                version_str = doc.get("v", "")
                if not version_str:
                    continue
                
                major_minor, vtype = self._parse_version(version_str)
                
                # 只处理跟踪的版本系列
                if not self._is_tracked_version(major_minor):
                    continue
                
                # 跳过SNAPSHOT（除非配置启用）
                if vtype == VersionType.SNAPSHOT and not self.config["check_snapshots"]:
                    continue
                
                version_info = VersionInfo(
                    version=version_str,
                    full_version=version_str,
                    version_type=vtype.value,
                    major_minor=major_minor,
                    release_date=doc.get("timestamp"),
                    source="maven-central",
                    url=f"https://search.maven.org/artifact/{group}/{artifact}/{version_str}/jar"
                )
                versions.append(version_info)
                
        except json.JSONDecodeError as e:
            self.errors.append(f"Failed to parse Maven Central response: {e}")
            logger.error(f"Failed to parse Maven Central response: {e}")
        
        logger.info(f"Found {len(versions)} versions from Maven Central")
        return versions
    
    def check_github_releases(self) -> List[VersionInfo]:
        """检查GitHub Releases页面"""
        logger.info("Checking GitHub Releases...")
        versions = []
        
        repo = self.config["github_repo"]
        
        urls = [
            f"https://api.github.com/repos/{repo}/releases",
            f"https://api.github.com/repos/{repo}/tags"
        ]
        
        headers = {
            "User-Agent": "Flink-Release-Checker/1.0",
            "Accept": "application/vnd.github.v3+json"
        }
        
        for url in urls:
            response = self._http_get(url, headers)
            if response:
                try:
                    items = json.loads(response)
                    
                    for item in items[:50]:  # 检查最近50个
                        tag_name = item.get("tag_name") or item.get("name", "")
                        tag_name = tag_name.lstrip("v")
                        
                        if not tag_name or not re.match(r'^\d+\.\d+', tag_name):
                            continue
                        
                        major_minor, vtype = self._parse_version(tag_name)
                        
                        # 检测RC版本
                        if "-rc" in tag_name.lower() or "-RC" in tag_name:
                            vtype = VersionType.RC
                        
                        release_date = item.get("published_at") or item.get("created_at")
                        html_url = item.get("html_url", "")
                        
                        version_info = VersionInfo(
                            version=tag_name,
                            full_version=tag_name,
                            version_type=vtype.value,
                            major_minor=major_minor,
                            release_date=release_date,
                            source="github",
                            url=html_url,
                            release_notes_url=item.get("html_url") if "releases" in url else None
                        )
                        versions.append(version_info)
                        
                except json.JSONDecodeError as e:
                    self.errors.append(f"Failed to parse GitHub response: {e}")
                    logger.error(f"Failed to parse GitHub response: {e}")
                break
        
        logger.info(f"Found {len(versions)} versions from GitHub")
        return versions
    
    def check_flink_website(self) -> List[VersionInfo]:
        """检查Flink官方网站"""
        logger.info("Checking Flink website...")
        versions = []
        
        # 检查下载页面
        url = f"{self.config['flink_website']}/downloads/"
        response = self._http_get(url)
        
        if response:
            # 解析HTML查找版本信息
            patterns = [
                r'Apache Flink (\d+\.\d+\.\d+)',
                r'flink-(\d+\.\d+\.\d+)-bin',
                r'version["\']?\s*[:=]\s*["\']?(\d+\.\d+\.\d+)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, response)
                for version_str in set(matches):
                    major_minor, vtype = self._parse_version(version_str)
                    
                    if not self._is_tracked_version(major_minor):
                        continue
                    
                    # 检查是否已存在
                    if any(v.version == version_str for v in versions):
                        continue
                    
                    version_info = VersionInfo(
                        version=version_str,
                        full_version=version_str,
                        version_type=vtype.value,
                        major_minor=major_minor,
                        source="flink-website",
                        url=url
                    )
                    versions.append(version_info)
        
        logger.info(f"Found {len(versions)} versions from Flink website")
        return versions
    
    def check_apache_archives(self) -> List[VersionInfo]:
        """检查Apache归档站点"""
        logger.info("Checking Apache archives...")
        versions = []
        
        url = "https://archive.apache.org/dist/flink/"
        response = self._http_get(url)
        
        if response:
            # 解析目录列表
            pattern = r'flink-(\d+\.\d+\.\d+)/'
            matches = re.findall(pattern, response)
            
            for version_str in set(matches):
                major_minor, vtype = self._parse_version(version_str)
                
                if not self._is_tracked_version(major_minor):
                    continue
                
                version_info = VersionInfo(
                    version=version_str,
                    full_version=version_str,
                    version_type=vtype.value,
                    major_minor=major_minor,
                    source="apache-archives",
                    url=f"https://archive.apache.org/dist/flink/flink-{version_str}/"
                )
                versions.append(version_info)
        
        logger.info(f"Found {len(versions)} versions from Apache archives")
        return versions
    
    def _get_latest_per_minor(self, versions: List[VersionInfo]) -> Dict[str, VersionInfo]:
        """获取每个minor版本的最新版本"""
        latest: Dict[str, VersionInfo] = {}
        
        for v in versions:
            key = v.major_minor
            if key not in latest:
                latest[key] = v
            else:
                current = latest[key].version
                if self._version_compare(v.version, current) > 0:
                    latest[key] = v
        
        return latest
    
    def _version_compare(self, v1: str, v2: str) -> int:
        """比较两个版本号"""
        def normalize(v: str) -> List[int]:
            v = re.sub(r'-rc\d+', '', v, flags=re.IGNORECASE)
            v = re.sub(r'-snapshot.*', '', v, flags=re.IGNORECASE)
            return [int(x) for x in v.split('.') if x.isdigit()]
        
        parts1 = normalize(v1)
        parts2 = normalize(v2)
        
        for i in range(max(len(parts1), len(parts2))):
            p1 = parts1[i] if i < len(parts1) else 0
            p2 = parts2[i] if i < len(parts2) else 0
            if p1 > p2:
                return 1
            elif p1 < p2:
                return -1
        
        return 0
    
    def _load_previous_state(self) -> Optional[Dict]:
        """加载之前的检查状态"""
        cache_file = self.config.get("cache_file")
        if not cache_file:
            return None
        
        try:
            path = Path(cache_file)
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load previous state: {e}")
        
        return None
    
    def _save_state(self, report: TrackingReport):
        """保存状态到缓存文件"""
        cache_file = self.config.get("cache_file")
        if not cache_file:
            return
        
        try:
            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)
            logger.info(f"State saved to {cache_file}")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
    def _detect_new_releases(self, current: Dict[str, VersionInfo], 
                             previous: Optional[Dict]) -> Tuple[List[VersionInfo], List[VersionInfo]]:
        """检测新发布的版本"""
        new_releases = []
        rc_versions = []
        
        if not previous:
            # 首次运行
            for v in current.values():
                if v.version_type == VersionType.GA.value:
                    new_releases.append(v)
                elif v.version_type == VersionType.RC.value:
                    rc_versions.append(v)
            return new_releases, rc_versions
        
        prev_versions = previous.get("versions", {})
        
        for major_minor, v in current.items():
            prev_version = prev_versions.get(major_minor, {}).get("latest_version", "")
            
            if v.version_type == VersionType.RC.value:
                rc_versions.append(v)
            
            if self._version_compare(v.version, prev_version) > 0:
                v.is_new = True
                if v.version_type == VersionType.GA.value:
                    new_releases.append(v)
        
        return new_releases, rc_versions
    
    def _update_tracked_versions(self, latest_versions: Dict[str, VersionInfo],
                                  rc_versions: List[VersionInfo]):
        """更新跟踪版本状态"""
        for major_minor, version_info in latest_versions.items():
            if major_minor in self.tracked_versions:
                tracked = self.tracked_versions[major_minor]
                tracked.latest_version = version_info.version
                tracked.actual_release = version_info.release_date
                
                if version_info.version_type == VersionType.GA.value:
                    tracked.status = "ga"
                elif version_info.version_type == VersionType.RC.value:
                    tracked.status = "rc"
        
        # 更新RC版本信息
        for rc in rc_versions:
            if rc.major_minor in self.tracked_versions:
                tracked = self.tracked_versions[rc.major_minor]
                if tracked.latest_rc is None or self._version_compare(
                    rc.version, tracked.latest_rc) > 0:
                    tracked.latest_rc = rc.version
                    if tracked.status == "upcoming":
                        tracked.status = "rc"
    
    def _get_upcoming_versions(self) -> List[Dict]:
        """获取尚未发布的版本信息"""
        upcoming = []
        
        for version, tracked in self.tracked_versions.items():
            if tracked.status == "upcoming":
                upcoming.append({
                    "version": version,
                    "expected_release": tracked.expected_release,
                    "status": "upcoming",
                    "message": f"Flink {version}.x 尚未发布，预计 {tracked.expected_release}"
                })
        
        return upcoming
    
    def _generate_recommendations(self, report: TrackingReport) -> List[str]:
        """生成建议操作"""
        recommendations = []
        
        # GA发布建议
        if report.new_releases:
            for v in report.new_releases:
                recommendations.append(
                    f"🚀 【P1-2】Flink {v.version} GA发布！ - "
                    f"立即更新前瞻文档: Flink/{v.major_minor}-roadmap/"
                )
                recommendations.append(
                    f"   1. 更新文档状态标记: `status: preview` → `status: released`"
                )
                recommendations.append(
                    f"   2. 验证API签名与实际发布一致"
                )
                recommendations.append(
                    f"   3. 更新Maven依赖版本号"
                )
        
        # RC版本建议
        if report.rc_versions:
            for v in report.rc_versions:
                recommendations.append(
                    f"🔍 【P1-1】Flink {v.version} RC可用 - "
                    f"关注GA发布计划，准备文档更新"
                )
        
        # 前瞻版本建议
        for upcoming in report.upcoming_versions:
            recommendations.append(
                f"📅 【P1-4】持续跟踪 Flink {upcoming['version']}.x - "
                f"预计发布时间: {upcoming['expected_release']}"
            )
        
        # 常规建议
        if not report.new_releases and not report.rc_versions:
            recommendations.append("✅ 暂无新版本发布，继续监控...")
        
        # P1-3: API同步建议
        for version, tracked in report.versions.items():
            if tracked.status == "ga" and not tracked.docs_updated:
                recommendations.append(
                    f"📝 【P1-3】Flink {version}.x 已发布，需要同步API和配置文档"
                )
        
        return recommendations
    
    def run(self) -> TrackingReport:
        """执行检查"""
        logger.info("=" * 60)
        logger.info("Flink Release Checker - Starting check...")
        logger.info("=" * 60)
        
        # 收集所有来源的版本信息
        all_versions = []
        all_versions.extend(self.check_maven_central())
        all_versions.extend(self.check_github_releases())
        all_versions.extend(self.check_flink_website())
        all_versions.extend(self.check_apache_archives())
        
        # 保存所有发现的版本
        self.all_discovered_versions = all_versions
        
        # 去重
        seen = set()
        unique_versions = []
        for v in all_versions:
            if v.version not in seen:
                seen.add(v.version)
                unique_versions.append(v)
        
        # 获取每个minor版本的最新版
        latest_versions = self._get_latest_per_minor(unique_versions)
        
        # 更新跟踪版本状态
        rc_versions = [v for v in unique_versions if v.version_type == VersionType.RC.value]
        self._update_tracked_versions(latest_versions, rc_versions)
        
        # 获取尚未发布的版本
        upcoming_versions = self._get_upcoming_versions()
        
        # 加载之前的状态
        previous_state = self._load_previous_state()
        
        # 检测新发布
        new_releases, detected_rc = self._detect_new_releases(
            latest_versions, previous_state
        )
        
        has_updates = len(new_releases) > 0
        
        # 构建报告
        report = TrackingReport(
            check_time=datetime.now().isoformat(),
            has_updates=has_updates,
            tracked_versions=self.config["tracked_versions"],
            versions=self.tracked_versions,
            new_releases=new_releases,
            rc_versions=detected_rc,
            upcoming_versions=upcoming_versions,
            all_discovered=unique_versions,
            recommendations=[],
            errors=self.errors
        )
        
        # 生成建议
        report.recommendations = self._generate_recommendations(report)
        
        # 保存状态
        self._save_state(report)
        
        return report
    
    def generate_markdown_report(self, report: TrackingReport) -> str:
        """生成Markdown格式的报告"""
        lines = []
        lines.append("# Flink 版本发布跟踪报告")
        lines.append("")
        lines.append(f"> **检查时间**: {report.check_time}")
        lines.append(f"> **检查状态**: {'🆕 有新版本' if report.has_updates else '✅ 无更新'}")
        lines.append("")
        
        lines.append("## 跟踪版本状态")
        lines.append("")
        lines.append("| 版本 | 预计发布 | 实际发布 | 状态 | 最新版本 | 最新RC |")
        lines.append("|------|----------|----------|------|----------|--------|")
        
        for version, tracked in report.versions.items():
            status_emoji = {
                "upcoming": "📅 计划中",
                "rc": "🔍 RC可用", 
                "ga": "✅ 已发布"
            }.get(tracked.status, tracked.status)
            
            lines.append(
                f"| {version} | {tracked.expected_release} | "
                f"{tracked.actual_release or '-'} | {status_emoji} | "
                f"{tracked.latest_version or '-'} | {tracked.latest_rc or '-'} |"
            )
        
        lines.append("")
        
        if report.new_releases:
            lines.append("## 🆕 新发布版本")
            lines.append("")
            for v in report.new_releases:
                lines.append(f"### Flink {v.version}")
                lines.append(f"- **类型**: GA正式发布")
                lines.append(f"- **来源**: {v.source}")
                lines.append(f"- **发布日期**: {v.release_date or 'Unknown'}")
                lines.append(f"- **链接**: {v.url}")
                lines.append("")
        
        if report.rc_versions:
            lines.append("## 🔍 RC版本")
            lines.append("")
            for v in report.rc_versions:
                lines.append(f"- **Flink {v.version}** - {v.source}")
            lines.append("")
        
        lines.append("## 📋 行动建议")
        lines.append("")
        for i, rec in enumerate(report.recommendations, 1):
            lines.append(f"{i}. {rec}")
        lines.append("")
        
        if report.errors:
            lines.append("## ⚠️ 错误信息")
            lines.append("")
            for err in report.errors:
                lines.append(f"- {err}")
            lines.append("")
        
        lines.append("---")
        lines.append("*自动生成 by Flink Release Checker*")
        
        return "\n".join(lines)
    
    def save_json_report(self, report: TrackingReport, filename: str = None):
        """保存JSON报告"""
        if filename is None:
            filename = f"flink-release-check-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        
        filepath = os.path.join(self.config["output_dir"], filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)
            logger.info(f"JSON report saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save JSON report: {e}")
            return None
    
    def save_markdown_report(self, report: TrackingReport, filename: str = None):
        """保存Markdown报告"""
        if filename is None:
            filename = f"flink-release-check-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        
        filepath = os.path.join(self.config["output_dir"], filename)
        
        try:
            content = self.generate_markdown_report(report)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Markdown report saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save Markdown report: {e}")
            return None


def load_config(config_path: Optional[str] = None) -> Dict:
    """加载配置文件"""
    if not config_path:
        default_paths = [
            "flink-checker-config.json",
            Path.home() / ".config" / "flink-checker" / "config.json"
        ]
        for p in default_paths:
            if Path(p).exists():
                config_path = str(p)
                break
    
    if config_path and Path(config_path).exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load config {config_path}: {e}")
    
    return {}


def main():
    parser = argparse.ArgumentParser(
        description="Flink Release Checker - Apache Flink 2.4/2.5/3.0 版本发布检测",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 基本检查
    python check_flink_release.py
    
    # 详细输出
    python check_flink_release.py --verbose
    
    # 指定配置
    python check_flink_release.py --config config.json
    
    # 输出到特定目录
    python check_flink_release.py --output-dir ./reports
    
    # 生成报告文件
    python check_flink_release.py --report-json --report-md
        """
    )
    
    parser.add_argument(
        "-c", "--config",
        help="配置文件路径 (JSON格式)"
    )
    parser.add_argument(
        "-o", "--output-dir",
        help="输出目录"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="启用详细日志输出"
    )
    parser.add_argument(
        "--report-json",
        action="store_true",
        help="生成JSON报告"
    )
    parser.add_argument(
        "--report-md",
        action="store_true",
        help="生成Markdown报告"
    )
    parser.add_argument(
        "--check-rc",
        action="store_true",
        default=True,
        help="检查RC版本"
    )
    parser.add_argument(
        "--no-check-rc",
        dest="check_rc",
        action="store_false",
        help="不检查RC版本"
    )
    parser.add_argument(
        "--tracked-versions",
        nargs="+",
        default=["2.4", "2.5", "3.0"],
        help="要跟踪的版本号列表"
    )
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 加载配置
    config = load_config(args.config)
    
    # 命令行参数覆盖配置
    if args.output_dir:
        config["output_dir"] = args.output_dir
    if not args.check_rc:
        config["check_rc"] = False
    if args.tracked_versions:
        config["tracked_versions"] = args.tracked_versions
    
    # 创建检查器并运行
    checker = FlinkReleaseChecker(config)
    
    try:
        report = checker.run()
        
        # 输出结果到控制台
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
        
        # 生成报告文件
        if args.report_json:
            checker.save_json_report(report)
        if args.report_md:
            checker.save_markdown_report(report)
        
        # 保存默认报告
        checker.save_json_report(report, "flink-release-latest.json")
        checker.save_markdown_report(report, "flink-release-latest.md")
        
        # 设置返回码
        if report.errors and not report.versions:
            return 2
        return 1 if report.has_updates else 0
        
    except Exception as e:
        logger.exception("Checker failed")
        print(json.dumps({
            "error": str(e),
            "check_time": datetime.now().isoformat()
        }, indent=2))
        return 2


if __name__ == "__main__":
    sys.exit(main())
