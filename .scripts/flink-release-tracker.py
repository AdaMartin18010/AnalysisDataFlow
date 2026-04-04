#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink Release Tracker - Apache Flink 版本发布检测脚本

功能:
1. 检测 Flink 官方发布页面新版本
2. 跟踪 Flink 2.4/2.5/3.0 发布状态
3. 发送通知到多种渠道 (文件/邮件/Slack/Webhook)
4. 维护版本状态历史记录

Author: AnalysisDataFlow Agent
Version: 1.0.0
Date: 2026-04-04
"""

import re
import json
import hashlib
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import urllib.request
import urllib.error
import ssl


class ReleaseStatus(Enum):
    """版本发布状态"""
    UNRELEASED = "未发布"
    PLANNED = "计划中"
    MILESTONE = "里程碑版"
    RC = "RC候选版"
    GA = "正式发布"
    LTS = "长期支持版"
    UNKNOWN = "未知"


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
    api_changes: List[str] = None
    breaking_changes: List[str] = None
    
    def __post_init__(self):
        if self.api_changes is None:
            self.api_changes = []
        if self.breaking_changes is None:
            self.breaking_changes = []


@dataclass
class TrackingRecord:
    """跟踪记录"""
    timestamp: str
    version: str
    old_status: ReleaseStatus
    new_status: ReleaseStatus
    source: str
    details: Dict


class FlinkReleaseTracker:
    """Flink 版本发布跟踪器"""
    
    # 官方数据源
    DOWNLOADS_URL = "https://flink.apache.org/downloads.html"
    RELEASES_URL = "https://flink.apache.org/downloads.html"
    MAVEN_URL = "https://repo1.maven.org/maven2/org/apache/flink/flink-core/"
    GITHUB_API = "https://api.github.com/repos/apache/flink/releases"
    
    # 目标跟踪版本
    TARGET_VERSIONS = ["2.4.0", "2.5.0", "3.0.0"]
    
    def __init__(self, config_path: Optional[str] = None):
        self.script_dir = Path(__file__).parent.resolve()
        self.project_root = self.script_dir.parent
        self.config_path = config_path or self.script_dir / "flink-tracker-config.json"
        self.state_path = self.script_dir / "flink-tracker-state.json"
        self.log_path = self.script_dir / "flink-tracker.log"
        
        self.config = self._load_config()
        self.state = self._load_state()
        self._setup_logging()
        
    def _setup_logging(self):
        """配置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_path, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self) -> Dict:
        """加载配置文件"""
        default_config = {
            "check_interval_hours": 24,
            "notification_channels": ["file"],
            "target_versions": self.TARGET_VERSIONS,
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
                "directories": ["Flink/roadmap", "Flink/08-roadmap"],
                "patterns": ["前瞻", "preview", "Preview", "planned", "upcoming"]
            }
        }
        
        if Path(self.config_path).exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    default_config.update(config)
            except Exception as e:
                print(f"Warning: Failed to load config: {e}")
                
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
            "last_check": None,
            "versions": {},
            "history": [],
            "prospective_docs": {}
        }
    
    def _save_state(self):
        """保存状态文件"""
        try:
            with open(self.state_path, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")
    
    def _fetch_url(self, url: str, timeout: int = 30) -> Optional[str]:
        """获取URL内容"""
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            req = urllib.request.Request(url, headers=headers)
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
        content = self._fetch_url(self.GITHUB_API)
        
        if not content:
            return versions
        
        try:
            releases = json.loads(content)
            for release in releases[:10]:  # 只检查最近10个
                tag_name = release.get('tag_name', '').replace('release-', '').replace('v', '')
                
                for target in self.TARGET_VERSIONS:
                    if target in tag_name:
                        status = ReleaseStatus.GA if not release.get('prerelease') else ReleaseStatus.RC
                        versions[target] = FlinkVersion(
                            version=target,
                            status=status,
                            release_date=release.get('published_at'),
                            release_notes=release.get('html_url')
                        )
        except json.JSONDecodeError:
            self.logger.error("Failed to parse GitHub API response")
            
        return versions
    
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
    
    def generate_notification(self, changes: List[TrackingRecord]) -> str:
        """生成通知消息"""
        if not changes:
            return ""
        
        message = f"""
🚀 **Flink 版本发布跟踪报告**
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        for change in changes:
            emoji = "🎉" if change.new_status == ReleaseStatus.GA else "📢"
            message += f"""
{emoji} **版本 {change.version} 状态变更**
   状态: {change.old_status.value} → {change.new_status.value}
   来源: {change.source}
   时间: {change.timestamp}
"""
            if change.details.get('download_url'):
                message += f"   下载: {change.details['download_url']}\n"
            if change.details.get('release_notes'):
                message += f"   发布说明: {change.details['release_notes']}\n"
        
        # 添加前瞻文档统计
        prospective_docs = self.scan_prospective_documents()
        if prospective_docs:
            message += "\n📄 **前瞻文档状态**\n"
            for ver, docs in prospective_docs.items():
                message += f"   {ver}: {len(docs)} 篇文档\n"
        
        message += f"\n---\n查看完整报告: `.scripts/flink-tracker-state.json`"
        
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
        notification_path = self.script_dir / f"flink-notifications-{datetime.now().strftime('%Y%m')}.log"
        with open(notification_path, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n{message}\n")
        self.logger.info(f"Notification saved to {notification_path}")
    
    def _notify_slack(self, message: str):
        """发送Slack通知"""
        import urllib.request
        import json
        
        webhook_url = self.config["slack"].get("webhook_url", "")
        if not webhook_url:
            return
        
        payload = {
            "text": message,
            "channel": self.config["slack"].get("channel", "#flink-releases")
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
        except Exception as e:
            self.logger.error(f"Failed to send Slack notification: {e}")
    
    def _notify_webhook(self, message: str):
        """发送Webhook通知"""
        import urllib.request
        import json
        
        webhook_config = self.config.get("webhook", {})
        url = webhook_config.get("url", "")
        
        if not url:
            return
        
        payload = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "source": "flink-release-tracker"
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
    
    def check_all_sources(self) -> Tuple[Dict[str, FlinkVersion], List[TrackingRecord]]:
        """检查所有数据源"""
        all_versions = {}
        changes = []
        
        # 检查各个数据源
        sources = [
            ("downloads_page", self.check_official_downloads),
            ("maven_repo", self.check_maven_repository),
            ("github_releases", self.check_github_releases)
        ]
        
        for source_name, check_func in sources:
            self.logger.info(f"Checking {source_name}...")
            versions = check_func()
            
            for ver, info in versions.items():
                if ver not in all_versions:
                    all_versions[ver] = info
                    
                    # 检查状态变更
                    old_status = self.state.get("versions", {}).get(ver, {}).get("status", "UNRELEASED")
                    old_status_enum = ReleaseStatus(old_status) if old_status in [s.value for s in ReleaseStatus] else ReleaseStatus.UNRELEASED
                    
                    if info.status != old_status_enum:
                        change = TrackingRecord(
                            timestamp=datetime.now().isoformat(),
                            version=ver,
                            old_status=old_status_enum,
                            new_status=info.status,
                            source=source_name,
                            details=asdict(info)
                        )
                        changes.append(change)
                        self.logger.info(f"Status change detected for {ver}: {old_status} → {info.status.value}")
        
        # 更新状态
        self.state["last_check"] = datetime.now().isoformat()
        for ver, info in all_versions.items():
            self.state["versions"][ver] = {
                "status": info.status.value,
                "release_date": info.release_date,
                "download_url": info.download_url,
                "release_notes": info.release_notes
            }
        
        # 添加历史记录
        for change in changes:
            self.state["history"].append(asdict(change))
        
        # 限制历史记录数量
        self.state["history"] = self.state["history"][-100:]
        
        self._save_state()
        
        return all_versions, changes
    
    def generate_report(self) -> str:
        """生成跟踪报告"""
        report = f"""# Flink 版本发布跟踪报告

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 跟踪版本状态

| 版本 | 状态 | 预计/实际发布 | 下载链接 |
|------|------|--------------|----------|
"""
        
        for ver in self.TARGET_VERSIONS:
            info = self.state.get("versions", {}).get(ver, {})
            status = info.get("status", "未跟踪")
            date = info.get("release_date", "-")[:10] if info.get("release_date") else "预计 2026+"
            url = info.get("download_url", "-")
            
            if url != "-":
                url = f"[下载]({url})"
            
            report += f"| {ver} | {status} | {date} | {url} |\n"
        
        report += """
## 前瞻文档统计

"""
        
        prospective_docs = self.scan_prospective_documents()
        for ver, docs in prospective_docs.items():
            report += f"\n### {ver}\n\n"
            for doc in docs[:10]:  # 最多显示10个
                report += f"- `{doc['path']}` - 状态: {doc['version_status']}\n"
            if len(docs) > 10:
                report += f"- ... 等共 {len(docs)} 篇文档\n"
        
        report += """
## 历史变更记录

| 时间 | 版本 | 变更 | 来源 |
|------|------|------|------|
"""
        
        for record in self.state.get("history", [])[-10:]:
            timestamp = record.get("timestamp", "")[:16]
            version = record.get("version", "")
            change = f"{record.get('old_status', '?')} → {record.get('new_status', '?')}"
            source = record.get("source", "")
            report += f"| {timestamp} | {version} | {change} | {source} |\n"
        
        return report
    
    def run(self, notify: bool = True, generate_report_file: bool = False):
        """运行跟踪检查"""
        self.logger.info("="*60)
        self.logger.info("Starting Flink Release Tracker")
        self.logger.info(f"Target versions: {self.TARGET_VERSIONS}")
        
        # 检查所有源
        versions, changes = self.check_all_sources()
        
        self.logger.info(f"Found {len(versions)} versions")
        self.logger.info(f"Detected {len(changes)} changes")
        
        # 扫描前瞻文档
        prospective_docs = self.scan_prospective_documents()
        self.logger.info(f"Scanned {sum(len(docs) for docs in prospective_docs.values())} prospective documents")
        
        # 发送通知
        if notify and changes:
            message = self.generate_notification(changes)
            self.send_notification(message)
            self.logger.info("Notifications sent")
        
        # 生成报告文件
        if generate_report_file:
            report = self.generate_report()
            report_path = self.project_root / "Flink" / "version-tracking.md"
            report_path.parent.mkdir(parents=True, exist_ok=True)
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            self.logger.info(f"Report saved to {report_path}")
        
        self.logger.info("Flink Release Tracker completed")
        return versions, changes


def main():
    parser = argparse.ArgumentParser(
        description="Flink Release Tracker - 跟踪 Apache Flink 版本发布"
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
        "--report", "-r",
        action="store_true",
        help="生成报告文件"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    args = parser.parse_args()
    
    tracker = FlinkReleaseTracker(config_path=args.config)
    tracker.run(
        notify=not args.no_notify,
        generate_report_file=args.report
    )


if __name__ == "__main__":
    main()
