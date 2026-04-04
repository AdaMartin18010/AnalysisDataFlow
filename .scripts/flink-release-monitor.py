#!/usr/bin/env python3
"""
Flink Release Monitor - Apache Flink官方发布监控脚本

功能:
- 监控Maven Central最新版本
- 监控GitHub Releases页面
- 检测新版本、RC版本、GA版本
- 输出JSON格式报告

用法:
    python flink-release-monitor.py [选项]

返回码:
    0 - 无更新
    1 - 有新版本发布
    2 - 执行错误
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
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# 默认配置
DEFAULT_CONFIG = {
    "tracked_versions": ["2.4", "2.5", "3.0"],
    "maven_group": "org.apache.flink",
    "maven_artifact": "flink-core",
    "github_repo": "apache/flink",
    "check_rc": True,
    "check_snapshots": False,
    "timeout": 30,
    "output_file": "flink-release-status.json"
}

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VersionType(Enum):
    """版本类型枚举"""
    GA = "ga"           # General Availability
    RC = "rc"           # Release Candidate
    SNAPSHOT = "snapshot"
    UNKNOWN = "unknown"


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
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ReleaseStatus:
    """发布状态数据类"""
    check_time: str
    has_updates: bool
    tracked_versions: List[str]
    latest_versions: Dict[str, VersionInfo]
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
            "latest_versions": {k: v.to_dict() for k, v in self.latest_versions.items()},
            "new_releases": [v.to_dict() for v in self.new_releases],
            "rc_versions": [v.to_dict() for v in self.rc_versions],
            "upcoming_versions": self.upcoming_versions,
            "all_discovered_count": len(self.all_discovered),
            "recommendations": self.recommendations,
            "errors": self.errors
        }


class FlinkReleaseMonitor:
    """Flink发布监控器"""
    
    def __init__(self, config: Dict):
        self.config = {**DEFAULT_CONFIG, **config}
        self.tracked_prefixes = self.config["tracked_versions"]
        self.timeout = self.config["timeout"]
        self.errors: List[str] = []
        self.all_discovered_versions: List[VersionInfo] = []
        
    def _http_get(self, url: str, headers: Optional[Dict] = None) -> Optional[str]:
        """执行HTTP GET请求"""
        try:
            req = urllib.request.Request(
                url,
                headers=headers or {"User-Agent": "Flink-Release-Monitor/1.0"}
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return resp.read().decode('utf-8')
        except urllib.error.URLError as e:
            self.errors.append(f"HTTP Error for {url}: {e}")
            logger.error(f"HTTP Error for {url}: {e}")
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
    
    def _get_upcoming_versions(self) -> List[Dict]:
        """基于已发布版本预测即将发布的版本"""
        upcoming = []
        
        # 分析当前最新的已发布版本
        latest_released = {}
        for v in self.all_discovered_versions:
            mm = v.major_minor
            if mm not in latest_released or self._version_compare(v.version, latest_released[mm].version) > 0:
                latest_released[mm] = v
        
        # 检查跟踪的前瞻版本
        for tracked in self.tracked_prefixes:
            if tracked not in latest_released:
                # 这个前瞻版本尚未发布
                upcoming.append({
                    "major_minor": tracked,
                    "status": "upcoming",
                    "message": f"版本 {tracked}.x 尚未发布，正在等待GA版本"
                })
        
        return upcoming
    
    def check_maven_central(self) -> List[VersionInfo]:
        """检查Maven Central获取最新版本"""
        logger.info("Checking Maven Central...")
        versions = []
        
        # Maven Central搜索API
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
        
        # 尝试多个GitHub API端点
        urls = [
            f"https://api.github.com/repos/{repo}/releases",
            f"https://api.github.com/repos/{repo}/tags"
        ]
        
        headers = {
            "User-Agent": "Flink-Release-Monitor/1.0",
            "Accept": "application/vnd.github.v3+json"
        }
        
        for url in urls:
            response = self._http_get(url, headers)
            if response:
                try:
                    items = json.loads(response)
                    
                    for item in items[:30]:  # 只检查最近30个
                        # Releases和Tags的字段名略有不同
                        tag_name = item.get("tag_name") or item.get("name", "")
                        tag_name = tag_name.lstrip("v")
                        
                        if not tag_name or not re.match(r'^\d+\.\d+', tag_name):
                            continue
                        
                        major_minor, vtype = self._parse_version(tag_name)
                        
                        # 对于GitHub，我们收集所有版本（不仅限于跟踪列表）
                        # 这样可以发现最新版本，然后在后续处理中筛选
                        
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
                            url=html_url
                        )
                        versions.append(version_info)
                        
                except json.JSONDecodeError as e:
                    self.errors.append(f"Failed to parse GitHub response: {e}")
                    logger.error(f"Failed to parse GitHub response: {e}")
                break  # 成功获取后跳出
        
        logger.info(f"Found {len(versions)} versions from GitHub")
        return versions
    
    def check_flink_website(self) -> List[VersionInfo]:
        """检查Flink官方网站新闻"""
        logger.info("Checking Flink website...")
        versions = []
        
        # 检查Flink下载页面
        url = "https://flink.apache.org/downloads/"
        response = self._http_get(url)
        
        if response:
            # 解析HTML查找版本信息
            pattern = r'Apache Flink (\d+\.\d+\.\d+)'
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
                    source="flink-website",
                    url=url
                )
                versions.append(version_info)
        
        logger.info(f"Found {len(versions)} versions from Flink website")
        return versions
    
    def _get_latest_per_minor(self, versions: List[VersionInfo]) -> Dict[str, VersionInfo]:
        """获取每个minor版本的最新版本"""
        latest: Dict[str, VersionInfo] = {}
        
        for v in versions:
            key = v.major_minor
            if key not in latest:
                latest[key] = v
            else:
                # 比较版本号
                current = latest[key].version
                if self._version_compare(v.version, current) > 0:
                    latest[key] = v
        
        return latest
    
    def _version_compare(self, v1: str, v2: str) -> int:
        """比较两个版本号，返回1如果v1>v2，-1如果v1<v2，0如果相等"""
        def normalize(v: str) -> List[int]:
            # 移除RC和SNAPSHOT后缀进行基础比较
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
        output_file = self.config.get("output_file")
        if not output_file:
            return None
        
        try:
            path = Path(output_file)
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load previous state: {e}")
        
        return None
    
    def _detect_new_releases(self, current: Dict[str, VersionInfo], 
                             previous: Optional[Dict]) -> Tuple[List[VersionInfo], List[VersionInfo]]:
        """检测新发布的版本"""
        new_releases = []
        rc_versions = []
        
        if not previous:
            # 首次运行，所有GA版本都认为是新的
            for v in current.values():
                if v.version_type == VersionType.GA.value:
                    new_releases.append(v)
                elif v.version_type == VersionType.RC.value:
                    rc_versions.append(v)
            return new_releases, rc_versions
        
        prev_versions = previous.get("latest_versions", {})
        
        for major_minor, v in current.items():
            prev_version = prev_versions.get(major_minor, {}).get("version", "")
            
            if v.version_type == VersionType.RC.value:
                rc_versions.append(v)
            
            if self._version_compare(v.version, prev_version) > 0:
                v.is_new = True
                if v.version_type == VersionType.GA.value:
                    new_releases.append(v)
        
        return new_releases, rc_versions
    
    def _generate_recommendations(self, status: ReleaseStatus) -> List[str]:
        """生成建议操作"""
        recommendations = []
        
        if status.new_releases:
            for v in status.new_releases:
                recommendations.append(
                    f"🚀 新版本发布: Flink {v.version} - "
                    f"请更新前瞻文档 (Flink/{v.major_minor}-roadmap.md)"
                )
        
        if status.rc_versions:
            for v in status.rc_versions:
                recommendations.append(
                    f"🔍 RC版本可用: Flink {v.version} - "
                    f"请关注GA版本发布计划"
                )
        
        # 前瞻版本建议
        for upcoming in status.upcoming_versions:
            recommendations.append(
                f"📅 前瞻版本: Flink {upcoming['major_minor']}.x - "
                f"{upcoming['message']}"
            )
        
        if not recommendations:
            recommendations.append("✅ 暂无新版本，当前跟踪版本均为最新")
        
        return recommendations
    
    def run(self) -> ReleaseStatus:
        """执行监控检查"""
        logger.info("Starting Flink release monitoring...")
        
        # 收集所有来源的版本信息
        all_versions = []
        all_versions.extend(self.check_maven_central())
        all_versions.extend(self.check_github_releases())
        all_versions.extend(self.check_flink_website())
        
        # 保存所有发现的版本
        self.all_discovered_versions = all_versions
        
        # 去重（基于版本号）
        seen = set()
        unique_versions = []
        for v in all_versions:
            if v.version not in seen:
                seen.add(v.version)
                unique_versions.append(v)
        
        # 获取每个minor版本的最新版（限制在跟踪列表内）
        latest_versions = self._get_latest_per_minor(unique_versions)
        
        # 获取前瞻版本信息
        upcoming_versions = self._get_upcoming_versions()
        
        # 加载之前的状态
        previous_state = self._load_previous_state()
        
        # 检测新发布
        new_releases, rc_versions = self._detect_new_releases(
            latest_versions, previous_state
        )
        
        has_updates = len(new_releases) > 0
        
        # 构建状态对象
        status = ReleaseStatus(
            check_time=datetime.now().isoformat(),
            has_updates=has_updates,
            tracked_versions=self.config["tracked_versions"],
            latest_versions=latest_versions,
            new_releases=new_releases,
            rc_versions=rc_versions,
            upcoming_versions=upcoming_versions,
            all_discovered=all_versions,
            recommendations=[],
            errors=self.errors
        )
        
        # 生成建议
        status.recommendations = self._generate_recommendations(status)
        
        return status
    
    def save_status(self, status: ReleaseStatus):
        """保存状态到文件"""
        output_file = self.config.get("output_file")
        if not output_file:
            return
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(status.to_dict(), f, indent=2, ensure_ascii=False)
            logger.info(f"Status saved to {output_file}")
        except Exception as e:
            logger.error(f"Failed to save status: {e}")


def load_config(config_path: Optional[str] = None) -> Dict:
    """加载配置文件"""
    if not config_path:
        # 尝试默认位置
        default_paths = [
            "flink-monitor-config.json",
            Path.home() / ".config" / "flink-monitor" / "config.json"
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


def generate_sample_report() -> Dict:
    """生成示例报告（用于测试）"""
    return {
        "check_time": datetime.now().isoformat(),
        "has_updates": True,
        "tracked_versions": ["2.4", "2.5", "3.0"],
        "latest_versions": {
            "2.2": {
                "version": "2.2.0",
                "full_version": "2.2.0",
                "version_type": "ga",
                "major_minor": "2.2",
                "release_date": "2025-01-15T00:00:00",
                "source": "maven-central",
                "url": "https://search.maven.org/artifact/org.apache.flink/flink-core/2.2.0/jar",
                "is_new": False
            }
        },
        "new_releases": [],
        "rc_versions": [
            {
                "version": "2.3.0-rc1",
                "full_version": "2.3.0-rc1",
                "version_type": "rc",
                "major_minor": "2.3",
                "release_date": "2025-03-01T00:00:00",
                "source": "github",
                "url": "https://github.com/apache/flink/releases/tag/release-2.3.0-rc1",
                "is_new": True
            }
        ],
        "upcoming_versions": [
            {"major_minor": "2.4", "status": "upcoming", "message": "版本 2.4.x 尚未发布，正在等待GA版本"},
            {"major_minor": "2.5", "status": "upcoming", "message": "版本 2.5.x 尚未发布，正在等待GA版本"},
            {"major_minor": "3.0", "status": "upcoming", "message": "版本 3.0.x 尚未发布，正在等待GA版本"}
        ],
        "all_discovered_count": 5,
        "recommendations": [
            "🔍 RC版本可用: Flink 2.3.0-rc1 - 请关注GA版本发布计划",
            "📅 前瞻版本: Flink 2.4.x - 版本 2.4.x 尚未发布，正在等待GA版本",
            "📅 前瞻版本: Flink 2.5.x - 版本 2.5.x 尚未发布，正在等待GA版本",
            "📅 前瞻版本: Flink 3.0.x - 版本 3.0.x 尚未发布，正在等待GA版本"
        ],
        "errors": []
    }


def main():
    parser = argparse.ArgumentParser(
        description="Flink Release Monitor - 监控Apache Flink官方发布",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python flink-release-monitor.py
    python flink-release-monitor.py --config custom-config.json
    python flink-release-monitor.py --output status.json --verbose
        """
    )
    
    parser.add_argument(
        "-c", "--config",
        help="配置文件路径 (JSON格式)"
    )
    parser.add_argument(
        "-o", "--output",
        help="输出文件路径 (JSON格式)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="启用详细日志输出"
    )
    parser.add_argument(
        "--check-rc",
        action="store_true",
        default=True,
        help="检查RC版本 (默认: True)"
    )
    parser.add_argument(
        "--no-check-rc",
        action="store_true",
        help="不检查RC版本"
    )
    parser.add_argument(
        "--tracked-versions",
        nargs="+",
        default=["2.4", "2.5", "3.0"],
        help="要跟踪的版本号列表 (如: 2.4 2.5 3.0)"
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="生成示例报告（用于测试）"
    )
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 加载配置
    config = load_config(args.config)
    
    # 命令行参数覆盖配置
    if args.output:
        config["output_file"] = args.output
    if args.no_check_rc:
        config["check_rc"] = False
    if args.tracked_versions:
        config["tracked_versions"] = args.tracked_versions
    
    # 示例模式
    if args.sample:
        sample = generate_sample_report()
        print(json.dumps(sample, indent=2, ensure_ascii=False))
        return 1 if sample["has_updates"] else 0
    
    # 创建监控器并运行
    monitor = FlinkReleaseMonitor(config)
    
    try:
        status = monitor.run()
        monitor.save_status(status)
        
        # 输出结果到控制台
        print(json.dumps(status.to_dict(), indent=2, ensure_ascii=False))
        
        # 设置返回码
        if status.errors and not status.latest_versions:
            return 2
        return 1 if status.has_updates else 0
        
    except Exception as e:
        logger.exception("Monitor failed")
        print(json.dumps({
            "error": str(e),
            "check_time": datetime.now().isoformat()
        }, indent=2))
        return 2


if __name__ == "__main__":
    sys.exit(main())
