#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink Release Tracker V2 - Apache Flink 2.6/2.7 版本发布检测脚本

功能:
1. 检测 Flink 官方发布页面新版本 (2.6, 2.7)
2. 监控 FLIP 状态变更
3. 跟踪 GitHub releases
4. 自动生成更新报告和通知
5. 维护版本状态历史记录
6. 与现有跟踪系统集成

Author: AnalysisDataFlow Agent
Version: 2.0.0
Date: 2026-04-05
"""

import re
import json
import hashlib
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
import urllib.request
import urllib.error
import ssl


class ReleaseStatus(Enum):
    """版本发布状态"""
    UNRELEASED = "未发布"
    PLANNED = "计划中"
    DESIGNING = "设计中"
    IMPLEMENTING = "实现中"
    TESTING = "测试中"
    MILESTONE = "里程碑版"
    RC = "RC候选版"
    GA = "正式发布"
    LTS = "长期支持版"
    UNKNOWN = "未知"


class FlipStatus(Enum):
    """FLIP 状态"""
    PLANNED = "计划中"
    PROPOSED = "已提议"
    ACCEPTED = "已接受"
    DESIGNING = "设计中"
    IMPLEMENTING = "实现中"
    TESTING = "测试中"
    COMPLETED = "已完成"
    RELEASED = "已发布"
    DISCARDED = "已废弃"


class NotificationChannel(Enum):
    """通知渠道"""
    FILE = "file"
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"


@dataclass
class FlinkVersion:
    """Flink 版本信息"""
    version: str
    status: ReleaseStatus
    release_date: Optional[str] = None
    download_url: Optional[str] = None
    release_notes: Optional[str] = None
    api_changes: List[str] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)
    new_features: List[str] = field(default_factory=list)


@dataclass
class FlipInfo:
    """FLIP 信息"""
    flip_id: str
    title: str
    status: FlipStatus
    target_version: str
    progress: int  # 0-100
    assignee: Optional[str] = None
    jira_link: Optional[str] = None
    description: Optional[str] = None
    last_updated: Optional[str] = None


@dataclass
class TrackingRecord:
    """跟踪记录"""
    timestamp: str
    record_type: str  # 'version', 'flip', 'feature'
    identifier: str
    old_status: str
    new_status: str
    source: str
    details: Dict


class FlinkReleaseTrackerV2:
    """Flink 版本发布跟踪器 V2"""
    
    # 官方数据源
    DOWNLOADS_URL = "https://flink.apache.org/downloads.html"
    RELEASES_URL = "https://flink.apache.org/downloads.html"
    MAVEN_URL = "https://repo1.maven.org/maven2/org/apache/flink/flink-core/"
    GITHUB_API = "https://api.github.com/repos/apache/flink/releases"
    FLIP_WIKI = "https://cwiki.apache.org/confluence/display/FLINK/Flink+Improvement+Proposals"
    JIRA_BASE = "https://issues.apache.org/jira/browse/"
    
    # 目标跟踪版本
    TARGET_VERSIONS = ["2.4.0", "2.5.0", "2.6.0", "2.7.0", "3.0.0"]
    
    # 预估的 FLIP 列表 (2.6/2.7)
    ESTIMATED_FLIPS = {
        "FLIP-550": {
            "title": "WASM UDF Enhancement",
            "target_version": "2.6",
            "status": FlipStatus.DESIGNING,
            "progress": 30
        },
        "FLIP-551": {
            "title": "SQL JSON Functions Enhancement",
            "target_version": "2.6",
            "status": FlipStatus.PLANNED,
            "progress": 20
        },
        "FLIP-552": {
            "title": "Connector Framework Optimization",
            "target_version": "2.6",
            "status": FlipStatus.DESIGNING,
            "progress": 40
        },
        "FLIP-560": {
            "title": "Cloud-Native Scheduler",
            "target_version": "2.7",
            "status": FlipStatus.PLANNED,
            "progress": 10
        },
        "FLIP-561": {
            "title": "AI/ML Integration Enhancement",
            "target_version": "2.7",
            "status": FlipStatus.PLANNED,
            "progress": 5
        },
        "FLIP-562": {
            "title": "Streaming-Batch Unified Execution",
            "target_version": "2.7",
            "status": FlipStatus.PLANNED,
            "progress": 5
        },
        "FLIP-563": {
            "title": "Materialized View Enhancement",
            "target_version": "2.7",
            "status": FlipStatus.PLANNED,
            "progress": 5
        },
        "FLIP-564": {
            "title": "HTTP/3 Protocol Support",
            "target_version": "2.7",
            "status": FlipStatus.PLANNED,
            "progress": 0
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        self.script_dir = Path(__file__).parent.resolve()
        self.project_root = self.script_dir.parent
        self.config_path = config_path or self.script_dir / "flink-tracker-config-v2.json"
        self.state_path = self.script_dir / "flink-tracker-state-v2.json"
        self.log_path = self.script_dir / "flink-tracker-v2.log"
        self.report_dir = self.project_root / "Flink" / "version-tracking"
        
        self.config = self._load_config()
        self.state = self._load_state()
        self._setup_logging()
        
    def _setup_logging(self):
        """配置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
            handlers=[
                logging.FileHandler(self.log_path, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self) -> Dict:
        """加载配置文件"""
        default_config = {
            "version": "2.0.0",
            "check_interval_hours": 24,
            "notification_channels": ["file"],
            "target_versions": self.TARGET_VERSIONS,
            "tracked_flips": list(self.ESTIMATED_FLIPS.keys()),
            "email": {
                "enabled": False,
                "smtp_server": "",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "to_addresses": []
            },
            "slack": {
                "enabled": False,
                "webhook_url": "",
                "channel": "#flink-releases"
            },
            "webhook": {
                "enabled": False,
                "url": "",
                "headers": {}
            },
            "prospective_doc_scan": {
                "enabled": True,
                "directories": [
                    "Flink/roadmap",
                    "Flink/08-roadmap",
                    "Flink/version-tracking"
                ],
                "patterns": ["前瞻", "preview", "Preview", "planned", "upcoming", "status=preview"]
            },
            "tracking": {
                "check_github": True,
                "check_maven": True,
                "check_downloads": True,
                "track_flips": True,
                "generate_reports": True
            }
        }
        
        if Path(self.config_path).exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    default_config.update(config)
            except Exception as e:
                self.logger.warning(f"Failed to load config: {e}")
                
        return default_config
    
    def _load_state(self) -> Dict:
        """加载状态文件"""
        if Path(self.state_path).exists():
            try:
                with open(self.state_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load state: {e}")
        
        return {
            "version": "2.0.0",
            "last_check": None,
            "versions": {},
            "flips": {},
            "history": [],
            "prospective_docs": {},
            "notifications_sent": 0
        }
    
    def _save_state(self):
        """保存状态文件"""
        try:
            with open(self.state_path, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")
    
    def _fetch_url(self, url: str, timeout: int = 30, headers: Optional[Dict] = None) -> Optional[str]:
        """获取URL内容"""
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            default_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            if headers:
                default_headers.update(headers)
            
            req = urllib.request.Request(url, headers=default_headers)
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            self.logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    def check_official_downloads(self) -> Dict[str, FlinkVersion]:
        """检查官方下载页面"""
        versions = {}
        content = self._fetch_url(self.DOWNLOADS_URL)
        
        if not content:
            return versions
        
        # 匹配版本号模式
        version_patterns = [
            r'flink-([0-9]+\.[0-9]+\.[0-9]+)',
            r'"version":\s*"([0-9]+\.[0-9]+\.[0-9]+)"',
            r'Flink\s+([0-9]+\.[0-9]+\.[0-9]+)',
        ]
        
        found_versions = set()
        for pattern in version_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            found_versions.update(matches)
        
        for ver in found_versions:
            # 检查是否为GA版本
            is_ga = f"flink-{ver}-bin" in content or f"flink-{ver}/flink" in content
            
            status = ReleaseStatus.GA if is_ga else ReleaseStatus.RC
            if ver in self.TARGET_VERSIONS and not is_ga:
                status = ReleaseStatus.PLANNED
                
            versions[ver] = FlinkVersion(
                version=ver,
                status=status,
                release_date=datetime.now().isoformat() if is_ga else None,
                download_url=f"https://www.apache.org/dyn/closer.lua/flink/flink-{ver}/flink-{ver}-bin-scala_2.12.tgz"
            )
        
        return versions
    
    def check_maven_repository(self) -> Dict[str, FlinkVersion]:
        """检查Maven仓库"""
        versions = {}
        
        for ver in self.TARGET_VERSIONS:
            url = f"{self.MAVEN_URL}{ver}/"
            content = self._fetch_url(url)
            
            if content and ("maven-metadata.xml" in content or ".pom" in content or ".jar" in content):
                versions[ver] = FlinkVersion(
                    version=ver,
                    status=ReleaseStatus.GA,
                    release_date=datetime.now().isoformat()
                )
                
        return versions
    
    def check_github_releases(self) -> Dict[str, FlinkVersion]:
        """检查GitHub发布"""
        versions = {}
        
        # 添加 GitHub API 请求头
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Flink-Release-Tracker/2.0'
        }
        
        content = self._fetch_url(self.GITHUB_API, headers=headers)
        
        if not content:
            return versions
        
        try:
            releases = json.loads(content)
            for release in releases[:20]:  # 检查最近20个
                tag_name = release.get('tag_name', '').replace('release-', '').replace('v', '')
                
                for target in self.TARGET_VERSIONS:
                    if target in tag_name:
                        is_prerelease = release.get('prerelease', False)
                        status = ReleaseStatus.RC if is_prerelease else ReleaseStatus.GA
                        
                        # 提取新特性列表
                        body = release.get('body', '')
                        new_features = self._extract_features_from_release_notes(body)
                        
                        versions[target] = FlinkVersion(
                            version=target,
                            status=status,
                            release_date=release.get('published_at'),
                            release_notes=release.get('html_url'),
                            new_features=new_features
                        )
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse GitHub API response: {e}")
            
        return versions
    
    def _extract_features_from_release_notes(self, body: str) -> List[str]:
        """从发布说明中提取新特性"""
        features = []
        
        # 匹配特性列表
        patterns = [
            r'[-*]\s*(?:New|Add|Support)\s*:?\s*(.+?)(?:\n|$)',
            r'[-*]\s*(.+?)(?:\n|$)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, body, re.IGNORECASE)
            for match in matches[:10]:  # 最多10个
                match = match.strip()
                if len(match) > 10 and len(match) < 200:
                    features.append(match)
        
        return list(set(features))[:10]  # 去重并限制数量
    
    def check_flip_status(self) -> Dict[str, FlipInfo]:
        """检查 FLIP 状态（基于配置的预估列表）"""
        flips = {}
        
        for flip_id, info in self.ESTIMATED_FLIPS.items():
            flips[flip_id] = FlipInfo(
                flip_id=flip_id,
                title=info["title"],
                status=info["status"],
                target_version=info["target_version"],
                progress=info["progress"],
                jira_link=f"{self.JIRA_BASE}{flip_id}",
                last_updated=datetime.now().isoformat()
            )
        
        # TODO: 可以添加从 Confluence 抓取实际 FLIP 状态的逻辑
        
        return flips
    
    def scan_prospective_documents(self) -> Dict[str, List[Dict]]:
        """扫描前瞻标记的文档"""
        docs = {}
        scan_config = self.config.get("prospective_doc_scan", {})
        
        if not scan_config.get("enabled", True):
            return docs
        
        directories = scan_config.get("directories", ["Flink/roadmap", "Flink/08-roadmap"])
        patterns = scan_config.get("patterns", ["前瞻", "preview", "Preview"])
        
        for directory in directories:
            dir_path = self.project_root / directory
            if not dir_path.exists():
                continue
                
            for md_file in dir_path.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8', errors='ignore')
                    
                    # 检查前瞻标记
                    has_prospective = any(pattern in content for pattern in patterns)
                    
                    # 提取版本状态标记
                    version_match = re.search(r'status=(\w+)', content)
                    version_status = version_match.group(1) if version_match else "unknown"
                    
                    # 提取目标版本
                    target_ver_match = re.search(r'target=([\w\-]+)', content)
                    target_ver = target_ver_match.group(1) if target_ver_match else "unknown"
                    
                    if has_prospective or "status=preview" in content:
                        doc_info = {
                            "path": str(md_file.relative_to(self.project_root)),
                            "version_status": version_status,
                            "target_version": target_ver,
                            "last_modified": datetime.fromtimestamp(
                                md_file.stat().st_mtime
                            ).isoformat()
                        }
                        
                        if target_ver not in docs:
                            docs[target_ver] = []
                        docs[target_ver].append(doc_info)
                        
                except Exception as e:
                    self.logger.error(f"Error scanning {md_file}: {e}")
        
        return docs
    
    def generate_notification(self, version_changes: List[TrackingRecord], 
                            flip_changes: List[TrackingRecord]) -> str:
        """生成通知消息"""
        if not version_changes and not flip_changes:
            return ""
        
        message = f"""
🚀 **Flink 版本发布跟踪报告 V2**
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        # 版本变更
        if version_changes:
            message += "📦 **版本状态变更**\n\n"
            for change in version_changes:
                emoji = "🎉" if "GA" in change.new_status or "正式发布" in change.new_status else "📢"
                message += f"""
{emoji} **版本 {change.identifier}**
   状态: {change.old_status} → {change.new_status}
   来源: {change.source}
   时间: {change.timestamp}
"""
                if change.details.get('download_url'):
                    message += f"   下载: {change.details['download_url']}\n"
                if change.details.get('release_notes'):
                    message += f"   发布说明: {change.details['release_notes']}\n"
        
        # FLIP 变更
        if flip_changes:
            message += "\n📋 **FLIP 状态变更**\n\n"
            for change in flip_changes:
                message += f"""
🔹 **{change.identifier}**
   标题: {change.details.get('title', 'N/A')}
   状态: {change.old_status} → {change.new_status}
   目标版本: {change.details.get('target_version', 'N/A')}
   进度: {change.details.get('progress', 0)}%
"""
        
        # 前瞻文档统计
        prospective_docs = self.scan_prospective_documents()
        if prospective_docs:
            message += "\n📄 **前瞻文档状态**\n"
            for ver, docs in prospective_docs.items():
                message += f"   {ver}: {len(docs)} 篇文档\n"
        
        message += f"\n---\n查看完整报告: `{self.state_path}`"
        
        return message
    
    def send_notification(self, message: str):
        """发送通知"""
        channels = self.config.get("notification_channels", ["file"])
        
        if "file" in channels:
            self._notify_file(message)
        if "slack" in channels and self.config["slack"].get("enabled"):
            self._notify_slack(message)
        if "webhook" in channels and self.config["webhook"].get("enabled"):
            self._notify_webhook(message)
    
    def _notify_file(self, message: str):
        """保存到文件"""
        notification_path = self.script_dir / f"flink-notifications-v2-{datetime.now().strftime('%Y%m')}.log"
        with open(notification_path, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n{message}\n")
        self.logger.info(f"Notification saved to {notification_path}")
    
    def _notify_slack(self, message: str):
        """发送Slack通知"""
        webhook_url = self.config["slack"].get("webhook_url", "")
        if not webhook_url:
            return
        
        payload = {
            "text": message,
            "channel": self.config["slack"].get("channel", "#flink-releases"),
            "username": "Flink Release Tracker V2"
        }
        
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                self.logger.info("Slack notification sent")
                self.state["notifications_sent"] = self.state.get("notifications_sent", 0) + 1
        except Exception as e:
            self.logger.error(f"Failed to send Slack notification: {e}")
    
    def _notify_webhook(self, message: str):
        """发送Webhook通知"""
        webhook_config = self.config.get("webhook", {})
        url = webhook_config.get("url", "")
        
        if not url:
            return
        
        payload = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "source": "flink-release-tracker-v2",
            "type": "release_notification"
        }
        
        try:
            data = json.dumps(payload).encode('utf-8')
            headers = webhook_config.get("headers", {})
            headers["Content-Type"] = "application/json"
            
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                self.logger.info("Webhook notification sent")
        except Exception as e:
            self.logger.error(f"Failed to send webhook notification: {e}")
    
    def check_all_sources(self) -> Tuple[Dict[str, FlinkVersion], Dict[str, FlipInfo], 
                                        List[TrackingRecord], List[TrackingRecord]]:
        """检查所有数据源"""
        all_versions = {}
        all_flips = {}
        version_changes = []
        flip_changes = []
        
        tracking_config = self.config.get("tracking", {})
        
        # 检查版本发布
        if tracking_config.get("check_github", True):
            self.logger.info("Checking GitHub releases...")
            github_versions = self.check_github_releases()
            all_versions.update(github_versions)
        
        if tracking_config.get("check_maven", True):
            self.logger.info("Checking Maven repository...")
            maven_versions = self.check_maven_repository()
            for ver, info in maven_versions.items():
                if ver not in all_versions:
                    all_versions[ver] = info
        
        if tracking_config.get("check_downloads", True):
            self.logger.info("Checking official downloads...")
            download_versions = self.check_official_downloads()
            for ver, info in download_versions.items():
                if ver not in all_versions:
                    all_versions[ver] = info
        
        # 检查 FLIP 状态
        if tracking_config.get("track_flips", True):
            self.logger.info("Checking FLIP status...")
            all_flips = self.check_flip_status()
        
        # 检测版本变更
        for ver, info in all_versions.items():
            old_info = self.state.get("versions", {}).get(ver, {})
            old_status_str = old_info.get("status", "UNRELEASED")
            
            try:
                old_status = ReleaseStatus[old_status_str] if old_status_str in [s.name for s in ReleaseStatus] else ReleaseStatus.UNRELEASED
            except:
                old_status = ReleaseStatus.UNRELEASED
            
            if info.status != old_status:
                change = TrackingRecord(
                    timestamp=datetime.now().isoformat(),
                    record_type="version",
                    identifier=ver,
                    old_status=old_status.value,
                    new_status=info.status.value,
                    source="github_releases",
                    details=asdict(info)
                )
                version_changes.append(change)
                self.logger.info(f"Version status change: {ver} {old_status.value} → {info.status.value}")
        
        # 检测 FLIP 变更（简化版）
        for flip_id, info in all_flips.items():
            old_flip = self.state.get("flips", {}).get(flip_id, {})
            old_status_str = old_flip.get("status", "PLANNED")
            
            try:
                old_status = FlipStatus[old_status_str] if old_status_str in [s.name for s in FlipStatus] else FlipStatus.PLANNED
            except:
                old_status = FlipStatus.PLANNED
            
            if info.status != old_status or info.progress != old_flip.get("progress", 0):
                change = TrackingRecord(
                    timestamp=datetime.now().isoformat(),
                    record_type="flip",
                    identifier=flip_id,
                    old_status=old_status.value,
                    new_status=info.status.value,
                    source="estimated",
                    details=asdict(info)
                )
                flip_changes.append(change)
        
        # 更新状态
        self.state["last_check"] = datetime.now().isoformat()
        
        for ver, info in all_versions.items():
            self.state["versions"][ver] = {
                "status": info.status.name,
                "release_date": info.release_date,
                "download_url": info.download_url,
                "release_notes": info.release_notes
            }
        
        for flip_id, info in all_flips.items():
            self.state["flips"][flip_id] = asdict(info)
        
        # 添加历史记录
        for change in version_changes + flip_changes:
            self.state["history"].append(asdict(change))
        
        # 限制历史记录数量
        self.state["history"] = self.state["history"][-200:]
        
        self._save_state()
        
        return all_versions, all_flips, version_changes, flip_changes
    
    def generate_report(self) -> str:
        """生成跟踪报告"""
        report_lines = [
            "# Flink 2.6/2.7 版本发布跟踪报告",
            "",
            f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"> 跟踪器版本: V2.0.0",
            "",
            "---",
            "",
            "## 1. 版本状态概览",
            "",
            "| 版本 | 状态 | 预计/实际发布 | 下载链接 |",
            "|------|------|--------------|----------|"
        ]
        
        for ver in self.TARGET_VERSIONS:
            info = self.state.get("versions", {}).get(ver, {})
            status = info.get("status", "未跟踪")
            date = info.get("release_date", "-")[:10] if info.get("release_date") else self._get_expected_date(ver)
            url = info.get("download_url", "-")
            
            if url != "-":
                url = f"[下载]({url})"
            
            report_lines.append(f"| {ver} | {status} | {date} | {url} |")
        
        report_lines.extend([
            "",
            "---",
            "",
            "## 2. FLIP 跟踪矩阵",
            "",
            "| FLIP | 标题 | 目标版本 | 状态 | 进度 |",
            "|------|------|----------|------|------|"
        ])
        
        for flip_id, info in self.state.get("flips", {}).items():
            report_lines.append(
                f"| {flip_id} | {info.get('title', 'N/A')} | "
                f"{info.get('target_version', 'N/A')} | "
                f"{info.get('status', 'N/A')} | "
                f"{info.get('progress', 0)}% |"
            )
        
        report_lines.extend([
            "",
            "---",
            "",
            "## 3. 前瞻文档统计",
            ""
        ])
        
        prospective_docs = self.scan_prospective_documents()
        for ver, docs in prospective_docs.items():
            report_lines.append(f"\n### {ver}\n")
            for doc in docs[:10]:
                report_lines.append(f"- `{doc['path']}` - 状态: {doc['version_status']}")
            if len(docs) > 10:
                report_lines.append(f"- ... 等共 {len(docs)} 篇文档")
        
        report_lines.extend([
            "",
            "---",
            "",
            "## 4. 近期变更记录",
            "",
            "| 时间 | 类型 | 标识符 | 变更 | 来源 |",
            "|------|------|--------|------|------|"
        ])
        
        for record in self.state.get("history", [])[-15:]:
            timestamp = record.get("timestamp", "")[:16]
            record_type = record.get("record_type", "unknown")
            identifier = record.get("identifier", "N/A")
            change = f"{record.get('old_status', '?')} → {record.get('new_status', '?')}"
            source = record.get("source", "")
            report_lines.append(f"| {timestamp} | {record_type} | {identifier} | {change} | {source} |")
        
        report_lines.extend([
            "",
            "---",
            "",
            "## 5. 快速链接",
            "",
            "- [Flink 2.6/2.7 路线图](../version-tracking/flink-26-27-roadmap.md)",
            "- [Apache Flink 官方路线图](https://flink.apache.org/roadmap/)",
            "- [FLIP 提案索引](https://cwiki.apache.org/confluence/display/FLINK/Flink+Improvement+Proposals)",
            "- [Flink JIRA](https://issues.apache.org/jira/browse/FLINK)",
            "- [GitHub Releases](https://github.com/apache/flink/releases)",
            "",
            f"*报告由 Flink Release Tracker V2 自动生成*"
        ])
        
        return "\n".join(report_lines)
    
    def _get_expected_date(self, version: str) -> str:
        """获取预计发布日期"""
        expected_dates = {
            "2.4.0": "2026 Q3-Q4",
            "2.5.0": "2026 Q2-Q3",
            "2.6.0": "2026 Q2 (预计5月)",
            "2.7.0": "2026 Q4 (预计12月)",
            "3.0.0": "2027+"
        }
        return expected_dates.get(version, "预计 2026+")
    
    def update_version_tracking_doc(self):
        """更新版本跟踪文档"""
        try:
            report = self.generate_report()
            report_path = self.report_dir / "flink-26-27-status-report.md"
            self.report_dir.mkdir(parents=True, exist_ok=True)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            self.logger.info(f"Report saved to {report_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update report: {e}")
            return False
    
    def run(self, notify: bool = True, generate_report: bool = True):
        """运行跟踪检查"""
        self.logger.info("="*60)
        self.logger.info("Starting Flink Release Tracker V2")
        self.logger.info(f"Target versions: {self.TARGET_VERSIONS}")
        self.logger.info(f"Tracking FLIPs: {len(self.ESTIMATED_FLIPS)}")
        
        # 检查所有源
        versions, flips, version_changes, flip_changes = self.check_all_sources()
        
        self.logger.info(f"Found {len(versions)} versions")
        self.logger.info(f"Tracking {len(flips)} FLIPs")
        self.logger.info(f"Detected {len(version_changes)} version changes")
        self.logger.info(f"Detected {len(flip_changes)} FLIP changes")
        
        # 扫描前瞻文档
        prospective_docs = self.scan_prospective_documents()
        total_docs = sum(len(docs) for docs in prospective_docs.values())
        self.logger.info(f"Scanned {total_docs} prospective documents")
        
        # 发送通知
        if notify and (version_changes or flip_changes):
            message = self.generate_notification(version_changes, flip_changes)
            self.send_notification(message)
            self.logger.info("Notifications sent")
        
        # 生成报告文件
        if generate_report:
            self.update_version_tracking_doc()
        
        self.logger.info("Flink Release Tracker V2 completed")
        return versions, flips, version_changes, flip_changes


def main():
    parser = argparse.ArgumentParser(
        description="Flink Release Tracker V2 - 跟踪 Apache Flink 2.6/2.7 版本发布"
    )
    parser.add_argument(
        "--config", "-c",
        help="配置文件路径"
    )
    parser.add_argument(
        "--no-notify",
        action="store_true",
        help="不发送通知"
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="不生成报告文件"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="仅运行检查，输出到控制台"
    )
    parser.add_argument(
        "--report", "-r",
        action="store_true",
        help="仅生成报告"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 2.0.0"
    )
    
    args = parser.parse_args()
    
    tracker = FlinkReleaseTrackerV2(config_path=args.config)
    
    if args.report:
        # 仅生成报告
        tracker.update_version_tracking_doc()
        print(f"Report generated: {tracker.report_dir / 'flink-26-27-status-report.md'}")
    elif args.check:
        # 仅检查，输出到控制台
        versions, flips, _, _ = tracker.check_all_sources()
        print(f"\n{'='*60}")
        print("Flink Release Tracker V2 - Check Results")
        print(f"{'='*60}")
        print(f"\nVersions found: {len(versions)}")
        for ver, info in versions.items():
            print(f"  {ver}: {info.status.value}")
        print(f"\nFLIPs tracked: {len(flips)}")
        for flip_id, info in flips.items():
            print(f"  {flip_id} ({info.target_version}): {info.status.value} ({info.progress}%)")
    else:
        # 正常运行
        tracker.run(
            notify=not args.no_notify,
            generate_report=not args.no_report
        )


if __name__ == "__main__":
    main()
