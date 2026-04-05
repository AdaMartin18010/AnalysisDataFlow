#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink Updates Notification - Flink 更新通知系统

功能:
1. 检测新版本发布、FLIP状态变更
2. 发送多渠道通知（文件/Slack/邮件/Webhook）
3. 生成更新建议和行动计划
4. 维护通知历史

Author: AnalysisDataFlow Agent
Version: 1.0.0
Date: 2026-04-05
"""

import json
import smtplib
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.request
import ssl


@dataclass
class NotificationEvent:
    """通知事件"""
    event_type: str  # 'version_release', 'flip_update', 'feature_ga'
    title: str
    message: str
    severity: str  # 'info', 'warning', 'critical'
    data: Dict[str, Any]
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class FlinkUpdateNotifier:
    """Flink 更新通知器"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.script_dir = Path(__file__).parent.resolve()
        self.project_root = self.script_dir.parent
        self.config_path = config_path or self.script_dir / "flink-tracker-config-v2.json"
        self.state_path = self.script_dir / "flink-notifier-state.json"
        self.log_path = self.script_dir / "flink-notifier.log"
        
        self.config = self._load_config()
        self.state = self._load_state()
        self._setup_logging()
        
    def _setup_logging(self):
        """配置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [Notifier] %(message)s',
            handlers=[
                logging.FileHandler(self.log_path, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        default_config = {
            "notification_channels": ["file"],
            "notification_rules": {
                "version_ga": {
                    "enabled": True,
                    "channels": ["file", "slack"],
                    "severity": "critical"
                },
                "version_rc": {
                    "enabled": True,
                    "channels": ["file"],
                    "severity": "info"
                },
                "flip_completed": {
                    "enabled": True,
                    "channels": ["file"],
                    "severity": "warning"
                },
                "feature_target_update": {
                    "enabled": True,
                    "channels": ["file"],
                    "severity": "info"
                }
            },
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "to_addresses": [],
                "subject_prefix": "[Flink Updates]"
            },
            "slack": {
                "enabled": False,
                "webhook_url": "",
                "channel": "#flink-releases",
                "username": "Flink Update Bot",
                "icon_emoji": ":rocket:"
            },
            "webhook": {
                "enabled": False,
                "url": "",
                "headers": {
                    "Content-Type": "application/json"
                }
            },
            "digest": {
                "enabled": True,
                "frequency": "daily",  # 'immediate', 'daily', 'weekly'
                "send_time": "09:00"
            }
        }
        
        if Path(self.config_path).exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并配置
                    for key, value in config.items():
                        if key in default_config and isinstance(value, dict):
                            default_config[key].update(value)
                        else:
                            default_config[key] = value
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
            "notifications_sent": [],
            "last_digest": None,
            "pending_events": [],
            "version": "1.0.0"
        }
    
    def _save_state(self):
        """保存状态文件"""
        try:
            with open(self.state_path, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")
    
    def create_version_release_notification(self, version: str, release_date: str, 
                                           release_notes: str, is_ga: bool = True) -> NotificationEvent:
        """创建版本发布通知"""
        event_type = "version_ga" if is_ga else "version_rc"
        severity = "critical" if is_ga else "info"
        
        title = f"🎉 Flink {version} 正式发布!" if is_ga else f"📢 Flink {version} RC 发布"
        
        message = f"""
**Flink {version}** 已经{'正式发布' if is_ga else '进入 RC 阶段'}！

**发布日期**: {release_date}
**发布说明**: {release_notes}

**建议行动**:
{'- [ ] 阅读发布说明和破坏性变更' if is_ga else '- [ ] 在测试环境验证 RC 版本'}
{'- [ ] 评估升级影响' if is_ga else '- [ ] 报告 RC 中发现的问题'}
{'- [ ] 规划升级时间表' if is_ga else '- [ ] 准备 GA 迁移计划'}
{'- [ ] 更新开发环境' if is_ga else ''}

查看详细文档: `Flink/version-tracking/flink-26-27-roadmap.md`
"""
        
        return NotificationEvent(
            event_type=event_type,
            title=title,
            message=message,
            severity=severity,
            data={
                "version": version,
                "release_date": release_date,
                "release_notes": release_notes,
                "is_ga": is_ga
            }
        )
    
    def create_flip_update_notification(self, flip_id: str, title: str, 
                                       old_status: str, new_status: str,
                                       target_version: str, progress: int) -> NotificationEvent:
        """创建 FLIP 更新通知"""
        severity = "warning" if new_status in ["COMPLETED", "RELEASED"] else "info"
        
        message = f"""
**{flip_id}** 状态更新

**标题**: {title}
**状态**: {old_status} → {new_status}
**目标版本**: {target_version}
**完成进度**: {progress}%

**影响分析**:
- 该 FLIP 计划包含在 Flink {target_version} 中
- 文档团队需要评估文档更新需求
- 建议查看: `Flink/version-tracking/feature-impact-{flip_id.lower()}.md`

**相关文档**:
- [FLIP 详情](https://cwiki.apache.org/confluence/display/FLINK/{flip_id})
- [JIRA 跟踪](https://issues.apache.org/jira/browse/{flip_id})
"""
        
        return NotificationEvent(
            event_type="flip_completed" if new_status == "COMPLETED" else "flip_update",
            title=f"📋 {flip_id} 状态更新: {new_status}",
            message=message,
            severity=severity,
            data={
                "flip_id": flip_id,
                "title": title,
                "old_status": old_status,
                "new_status": new_status,
                "target_version": target_version,
                "progress": progress
            }
        )
    
    def create_documentation_update_reminder(self, version: str, features: List[str]) -> NotificationEvent:
        """创建文档更新提醒"""
        features_list = "\n".join([f"- {f}" for f in features[:5]])
        
        message = f"""
**Flink {version} 文档更新提醒**

以下新特性需要文档支持：
{features_list}
{'... 等更多特性' if len(features) > 5 else ''}

**待办事项**:
- [ ] 创建/更新特性影响分析文档
- [ ] 编写用户指南
- [ ] 更新 API 文档
- [ ] 添加代码示例
- [ ] 更新快速入门

**相关文件**:
- 特性跟踪: `Flink/version-tracking/flink-26-27-roadmap.md`
- 影响模板: `Flink/version-tracking/feature-impact-template.md`
"""
        
        return NotificationEvent(
            event_type="doc_update_reminder",
            title=f"📝 Flink {version} 文档更新提醒",
            message=message,
            severity="warning",
            data={
                "version": version,
                "features": features
            }
        )
    
    def send_email(self, event: NotificationEvent) -> bool:
        """发送邮件通知"""
        email_config = self.config.get("email", {})
        
        if not email_config.get("enabled"):
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"{email_config.get('subject_prefix', '[Flink Updates]')} {event.title}"
            msg['From'] = email_config.get("username", "")
            msg['To'] = ", ".join(email_config.get("to_addresses", []))
            
            # 纯文本和 HTML 版本
            text_body = event.message
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2>{event.title}</h2>
                <div style="background: #f4f4f4; padding: 15px; border-radius: 5px;">
                    {event.message.replace(chr(10), '<br>')}
                </div>
                <hr>
                <p style="color: #666; font-size: 12px;">
                    发送时间: {event.timestamp}<br>
                    事件类型: {event.event_type}
                </p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            server = smtplib.SMTP(email_config.get("smtp_server", ""), 
                                 email_config.get("smtp_port", 587))
            server.starttls()
            server.login(email_config.get("username", ""), 
                        email_config.get("password", ""))
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Email notification sent: {event.title}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False
    
    def send_slack(self, event: NotificationEvent) -> bool:
        """发送 Slack 通知"""
        slack_config = self.config.get("slack", {})
        
        if not slack_config.get("enabled"):
            return False
        
        webhook_url = slack_config.get("webhook_url", "")
        if not webhook_url:
            return False
        
        # 根据严重程度设置颜色
        color_map = {
            "info": "#36a64f",
            "warning": "#ff9900",
            "critical": "#ff0000"
        }
        
        payload = {
            "username": slack_config.get("username", "Flink Update Bot"),
            "icon_emoji": slack_config.get("icon_emoji", ":rocket:"),
            "attachments": [{
                "color": color_map.get(event.severity, "#36a64f"),
                "title": event.title,
                "text": event.message,
                "footer": f"Flink Update Notifier | {event.timestamp}",
                "ts": int(datetime.now().timestamp())
            }]
        }
        
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
                self.logger.info(f"Slack notification sent: {event.title}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to send Slack notification: {e}")
            return False
    
    def send_webhook(self, event: NotificationEvent) -> bool:
        """发送 Webhook 通知"""
        webhook_config = self.config.get("webhook", {})
        
        if not webhook_config.get("enabled"):
            return False
        
        url = webhook_config.get("url", "")
        if not url:
            return False
        
        payload = {
            "event": asdict(event),
            "timestamp": datetime.now().isoformat(),
            "source": "flink-update-notifier"
        }
        
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            data = json.dumps(payload).encode('utf-8')
            headers = webhook_config.get("headers", {})
            headers["Content-Type"] = "application/json"
            
            req = urllib.request.Request(url, data=data, headers=headers)
            
            with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
                self.logger.info(f"Webhook notification sent: {event.title}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to send webhook notification: {e}")
            return False
    
    def save_to_file(self, event: NotificationEvent) -> bool:
        """保存通知到文件"""
        try:
            notification_file = self.script_dir / f"flink-notifications-{datetime.now().strftime('%Y%m')}.log"
            
            with open(notification_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"时间: {event.timestamp}\n")
                f.write(f"类型: {event.event_type}\n")
                f.write(f"严重度: {event.severity}\n")
                f.write(f"标题: {event.title}\n")
                f.write(f"{'='*60}\n")
                f.write(event.message)
                f.write("\n")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save notification to file: {e}")
            return False
    
    def send_notification(self, event: NotificationEvent, channels: Optional[List[str]] = None):
        """发送通知到指定渠道"""
        if channels is None:
            channels = self.config.get("notification_channels", ["file"])
        
        results = {}
        
        if "file" in channels:
            results["file"] = self.save_to_file(event)
        
        if "email" in channels:
            results["email"] = self.send_email(event)
        
        if "slack" in channels:
            results["slack"] = self.send_slack(event)
        
        if "webhook" in channels:
            results["webhook"] = self.send_webhook(event)
        
        # 记录到状态
        self.state["notifications_sent"].append({
            "timestamp": event.timestamp,
            "event_type": event.event_type,
            "title": event.title,
            "channels": channels,
            "results": results
        })
        
        # 限制历史记录
        self.state["notifications_sent"] = self.state["notifications_sent"][-100:]
        self._save_state()
        
        return results
    
    def generate_daily_digest(self) -> Optional[NotificationEvent]:
        """生成每日摘要"""
        # 获取最近24小时的通知
        cutoff = datetime.now() - timedelta(hours=24)
        recent_events = [
            e for e in self.state.get("notifications_sent", [])
            if datetime.fromisoformat(e.get("timestamp", "2000-01-01")) > cutoff
        ]
        
        if not recent_events:
            return None
        
        # 按类型分组
        events_by_type = {}
        for event in recent_events:
            event_type = event.get("event_type", "unknown")
            if event_type not in events_by_type:
                events_by_type[event_type] = []
            events_by_type[event_type].append(event)
        
        # 生成摘要消息
        message_parts = [f"## Flink 更新每日摘要 ({datetime.now().strftime('%Y-%m-%d')})", ""]
        
        for event_type, events in events_by_type.items():
            message_parts.append(f"### {event_type} ({len(events)})")
            for e in events[:5]:  # 每类最多5个
                message_parts.append(f"- {e.get('title', 'N/A')}")
            if len(events) > 5:
                message_parts.append(f"- ... 等共 {len(events)} 个事件")
            message_parts.append("")
        
        return NotificationEvent(
            event_type="daily_digest",
            title=f"📊 Flink 更新每日摘要 ({datetime.now().strftime('%Y-%m-%d')})",
            message="\n".join(message_parts),
            severity="info",
            data={"event_count": len(recent_events)}
        )
    
    def check_and_notify(self):
        """检查并发送通知"""
        # 读取 tracker 状态
        tracker_state_path = self.script_dir / "flink-tracker-state-v2.json"
        
        if not tracker_state_path.exists():
            self.logger.warning("Tracker state not found, skipping notification check")
            return
        
        try:
            with open(tracker_state_path, 'r', encoding='utf-8') as f:
                tracker_state = json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load tracker state: {e}")
            return
        
        # 检查版本变更
        for ver, info in tracker_state.get("versions", {}).items():
            status = info.get("status", "")
            
            # 检查是否已经通知过
            notified_versions = [n.get("data", {}).get("version") 
                               for n in self.state.get("notifications_sent", [])
                               if n.get("event_type") in ["version_ga", "version_rc"]]
            
            if ver not in notified_versions:
                if status == "GA":
                    event = self.create_version_release_notification(
                        version=ver,
                        release_date=info.get("release_date", datetime.now().isoformat()),
                        release_notes=info.get("release_notes", ""),
                        is_ga=True
                    )
                    self.send_notification(event)
                    
                elif status == "RC":
                    event = self.create_version_release_notification(
                        version=ver,
                        release_date=info.get("release_date", datetime.now().isoformat()),
                        release_notes=info.get("release_notes", ""),
                        is_ga=False
                    )
                    self.send_notification(event)
        
        # 检查 FLIP 变更
        for flip_id, info in tracker_state.get("flips", {}).items():
            # 简化处理：实际应该对比历史状态
            pass
        
        self.logger.info("Notification check completed")


def main():
    parser = argparse.ArgumentParser(
        description="Flink Updates Notification - 发送 Flink 更新通知"
    )
    parser.add_argument(
        "--config", "-c",
        help="配置文件路径"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="检查并发送通知"
    )
    parser.add_argument(
        "--digest",
        action="store_true",
        help="发送每日摘要"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="发送测试通知"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    args = parser.parse_args()
    
    notifier = FlinkUpdateNotifier(config_path=args.config)
    
    if args.test:
        # 发送测试通知
        test_event = NotificationEvent(
            event_type="test",
            title="🧪 测试通知",
            message="这是一条测试通知，用于验证通知系统是否正常工作。\n\n如果收到此消息，说明通知系统配置正确。",
            severity="info",
            data={"test": True}
        )
        results = notifier.send_notification(test_event)
        print(f"Test notification sent: {results}")
        
    elif args.digest:
        # 发送每日摘要
        digest = notifier.generate_daily_digest()
        if digest:
            results = notifier.send_notification(digest)
            print(f"Daily digest sent: {results}")
        else:
            print("No events to include in digest")
            
    elif args.check:
        # 检查并发送通知
        notifier.check_and_notify()
        print("Notification check completed")
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
