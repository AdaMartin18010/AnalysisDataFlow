#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink Change Notifier

检测到变更时发送通知，支持多种渠道：
- Slack Webhook
- 邮件 (SMTP)
- 自定义 Webhook
- 文件日志

作者: Flink Version Tracker
版本: 1.0.0
"""

import json
import logging
import os
import smtplib
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Dict, List, Optional, Callable
from urllib.parse import urljoin

# 尝试导入可选依赖
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    import urllib.request
    import urllib.error
    import ssl


# =============================================================================
# 配置和日志
# =============================================================================

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """配置日志记录器"""
    logger = logging.getLogger("change-notifier")
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
        "notification": {
            "slack": {
                "enabled": False,
                "webhook_url": "",
                "channel": "#flink-updates",
                "username": "Flink-Version-Tracker"
            },
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "from": "flink-tracker@example.com",
                "to": ["admin@example.com"]
            },
            "webhook": {
                "enabled": False,
                "url": "",
                "headers": {"Content-Type": "application/json"}
            }
        },
        "storage": {
            "data_dir": "./data"
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
# 数据模型
# =============================================================================

@dataclass
class ChangeEvent:
    """变更事件"""
    event_type: str  # new_release, flip_update, etc.
    title: str
    description: str
    details: Dict
    timestamp: str = None
    severity: str = "info"  # info, warning, critical
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class NotificationResult:
    """通知结果"""
    success: bool
    channel: str
    message: str
    error: Optional[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


# =============================================================================
# HTTP 客户端
# =============================================================================

class HTTPClient:
    """简单的 HTTP 客户端"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.has_requests = HAS_REQUESTS
    
    def post(self, url: str, data: Dict, headers: Optional[Dict] = None) -> bool:
        """发送 POST 请求"""
        payload = json.dumps(data).encode('utf-8')
        merged_headers = headers or {}
        merged_headers.setdefault("Content-Type", "application/json")
        
        try:
            if self.has_requests:
                response = requests.post(url, json=data, headers=merged_headers, timeout=30)
                return response.status_code < 400
            else:
                req = urllib.request.Request(
                    url,
                    data=payload,
                    headers=merged_headers,
                    method='POST'
                )
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
                    return response.status < 400
                    
        except Exception as e:
            self.logger.error(f"POST 请求失败: {e}")
            return False


# =============================================================================
# 通知渠道
# =============================================================================

class NotificationChannel:
    """通知渠道基类"""
    
    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
    
    def send(self, event: ChangeEvent) -> NotificationResult:
        """发送通知"""
        raise NotImplementedError
    
    def is_enabled(self) -> bool:
        """检查是否启用"""
        return self.config.get("enabled", False)


class SlackNotifier(NotificationChannel):
    """Slack 通知"""
    
    def __init__(self, config: Dict, logger: logging.Logger, http_client: HTTPClient):
        super().__init__(config, logger)
        self.http = http_client
    
    def send(self, event: ChangeEvent) -> NotificationResult:
        """发送 Slack 通知"""
        if not self.is_enabled():
            return NotificationResult(
                success=False,
                channel="slack",
                message="Slack 通知未启用"
            )
        
        webhook_url = self.config.get("webhook_url", "")
        if not webhook_url:
            return NotificationResult(
                success=False,
                channel="slack",
                message="未配置 Webhook URL",
                error="Missing webhook_url"
            )
        
        # 构建消息
        color = {
            "info": "#36a64f",
            "warning": "#ff9900",
            "critical": "#ff0000"
        }.get(event.severity, "#36a64f")
        
        emoji = {
            "new_release": "🚀",
            "flip_update": "📋",
            "version_eol": "⚠️",
            "security_alert": "🔒"
        }.get(event.event_type, "📢")
        
        payload = {
            "username": self.config.get("username", "Flink-Version-Tracker"),
            "channel": self.config.get("channel", "#flink-updates"),
            "icon_emoji": ":bell:",
            "attachments": [{
                "color": color,
                "title": f"{emoji} {event.title}",
                "text": event.description,
                "fields": [
                    {
                        "title": "类型",
                        "value": event.event_type,
                        "short": True
                    },
                    {
                        "title": "时间",
                        "value": event.timestamp[:19] if event.timestamp else "Unknown",
                        "short": True
                    }
                ],
                "footer": "Flink Version Tracker",
                "ts": int(datetime.now().timestamp())
            }]
        }
        
        # 添加详情
        if event.details:
            detail_text = "\n".join(f"• {k}: {v}" for k, v in event.details.items() if v)
            if detail_text:
                payload["attachments"][0]["fields"].append({
                    "title": "详情",
                    "value": detail_text[:1000],  # Slack 字段限制
                    "short": False
                })
        
        # 发送
        success = self.http.post(webhook_url, payload)
        
        if success:
            self.logger.info("Slack 通知发送成功")
            return NotificationResult(
                success=True,
                channel="slack",
                message="通知已发送到 Slack"
            )
        else:
            return NotificationResult(
                success=False,
                channel="slack",
                message="Slack 通知发送失败",
                error="HTTP request failed"
            )


class EmailNotifier(NotificationChannel):
    """邮件通知"""
    
    def send(self, event: ChangeEvent) -> NotificationResult:
        """发送邮件通知"""
        if not self.is_enabled():
            return NotificationResult(
                success=False,
                channel="email",
                message="邮件通知未启用"
            )
        
        # 获取配置
        smtp_server = self.config.get("smtp_server", "")
        smtp_port = self.config.get("smtp_port", 587)
        username = self.config.get("username", "")
        password = self.config.get("password", "")
        from_addr = self.config.get("from", "")
        to_addrs = self.config.get("to", [])
        
        if not all([smtp_server, from_addr, to_addrs]):
            return NotificationResult(
                success=False,
                channel="email",
                message="邮件配置不完整",
                error="Missing configuration"
            )
        
        try:
            # 构建邮件
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"[Flink Tracker] {event.title}"
            msg['From'] = from_addr
            msg['To'] = ', '.join(to_addrs)
            
            # 纯文本内容
            text_body = f"""
事件类型: {event.event_type}
严重程度: {event.severity}
时间: {event.timestamp}

{event.description}

详情:
{json.dumps(event.details, indent=2, ensure_ascii=False)}
            """.strip()
            
            # HTML 内容
            html_body = f"""
<html>
<head><style>
body {{ font-family: Arial, sans-serif; }}
.header {{ background: #f0f0f0; padding: 10px; }}
.content {{ padding: 20px; }}
.footer {{ color: #666; font-size: 12px; }}
</style></head>
<body>
<div class="header">
    <h2>{event.title}</h2>
    <p>类型: {event.event_type} | 严重程度: {event.severity}</p>
</div>
<div class="content">
    <p>{event.description.replace(chr(10), '<br>')}</p>
    <h3>详情</h3>
    <pre>{json.dumps(event.details, indent=2, ensure_ascii=False)}</pre>
</div>
<div class="footer">
    <p>发送时间: {event.timestamp}</p>
    <p>Flink Version Tracker</p>
</div>
</body>
</html>
            """
            
            msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # 发送邮件
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                if username and password:
                    server.login(username, password)
                server.sendmail(from_addr, to_addrs, msg.as_string())
            
            self.logger.info("邮件发送成功")
            return NotificationResult(
                success=True,
                channel="email",
                message=f"邮件已发送到 {', '.join(to_addrs)}"
            )
            
        except Exception as e:
            self.logger.error(f"邮件发送失败: {e}")
            return NotificationResult(
                success=False,
                channel="email",
                message="邮件发送失败",
                error=str(e)
            )


class WebhookNotifier(NotificationChannel):
    """自定义 Webhook 通知"""
    
    def __init__(self, config: Dict, logger: logging.Logger, http_client: HTTPClient):
        super().__init__(config, logger)
        self.http = http_client
    
    def send(self, event: ChangeEvent) -> NotificationResult:
        """发送 Webhook 通知"""
        if not self.is_enabled():
            return NotificationResult(
                success=False,
                channel="webhook",
                message="Webhook 通知未启用"
            )
        
        webhook_url = self.config.get("url", "")
        if not webhook_url:
            return NotificationResult(
                success=False,
                channel="webhook",
                message="未配置 Webhook URL",
                error="Missing URL"
            )
        
        headers = self.config.get("headers", {})
        
        # 构建 payload
        payload = {
            "event": event.to_dict(),
            "meta": {
                "source": "flink-version-tracker",
                "version": "1.0.0",
                "sent_at": datetime.now().isoformat()
            }
        }
        
        success = self.http.post(webhook_url, payload, headers)
        
        if success:
            self.logger.info("Webhook 通知发送成功")
            return NotificationResult(
                success=True,
                channel="webhook",
                message="通知已发送到自定义 Webhook"
            )
        else:
            return NotificationResult(
                success=False,
                channel="webhook",
                message="Webhook 通知发送失败",
                error="HTTP request failed"
            )


class FileNotifier(NotificationChannel):
    """文件日志通知"""
    
    def __init__(self, config: Dict, logger: logging.Logger, data_dir: Path):
        super().__init__(config, logger)
        self.data_dir = data_dir
        self.log_file = data_dir / "notifications.log"
    
    def send(self, event: ChangeEvent) -> NotificationResult:
        """记录到文件"""
        try:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "event": event.to_dict()
            }
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
            return NotificationResult(
                success=True,
                channel="file",
                message=f"已记录到 {self.log_file}"
            )
            
        except IOError as e:
            return NotificationResult(
                success=False,
                channel="file",
                message="文件写入失败",
                error=str(e)
            )


# =============================================================================
# 变更摘要生成器
# =============================================================================

class ChangeSummaryGenerator:
    """变更摘要生成器"""
    
    @staticmethod
    def from_release_check(release_data: Dict) -> List[ChangeEvent]:
        """从发布检查结果生成事件"""
        events = []
        
        new_releases = release_data.get("new_releases", [])
        for rel in new_releases:
            events.append(ChangeEvent(
                event_type="new_release",
                title=f"Flink {rel.get('version')} 已发布",
                description=f"发现 Flink 新版本 {rel.get('version')}，发布日期: {rel.get('release_date', 'unknown')}",
                details={
                    "version": rel.get('version'),
                    "release_date": rel.get('release_date'),
                    "is_stable": rel.get('is_stable', True),
                    "new_features": len(rel.get('new_features', [])),
                    "bug_fixes": len(rel.get('bug_fixes', [])),
                    "release_notes": rel.get('release_notes_url', ''),
                    "maven_url": rel.get('maven_url', '')
                },
                severity="info" if rel.get('is_stable', True) else "warning"
            ))
        
        return events
    
    @staticmethod
    def from_flip_check(flip_data: Dict) -> List[ChangeEvent]:
        """从 FLIP 检查结果生成事件"""
        events = []
        
        new_flips = flip_data.get("new_flips", [])
        for flip in new_flips:
            events.append(ChangeEvent(
                event_type="new_flip",
                title=f"新 FLIP: {flip.get('flip_id', 'Unknown')}",
                description=f"发现新的 Flink 改进提案: {flip.get('title', 'Unknown')}",
                details={
                    "flip_id": flip.get('flip_id'),
                    "title": flip.get('title'),
                    "status": flip.get('status'),
                    "author": flip.get('author'),
                    "component": flip.get('component'),
                    "url": flip.get('url')
                },
                severity="info"
            ))
        
        updated_flips = flip_data.get("updated_flips", [])
        for flip in updated_flips:
            events.append(ChangeEvent(
                event_type="flip_update",
                title=f"FLIP 更新: {flip.get('flip_id', 'Unknown')}",
                description=f"FLIP 状态已更新",
                details={
                    "flip_id": flip.get('flip_id'),
                    "new_status": flip.get('status'),
                    "url": flip.get('url')
                },
                severity="info"
            ))
        
        return events
    
    @staticmethod
    def create_daily_summary(events: List[ChangeEvent]) -> ChangeEvent:
        """创建每日摘要"""
        if not events:
            return ChangeEvent(
                event_type="daily_summary",
                title="Flink 版本跟踪 - 无更新",
                description="今日未检测到 Flink 版本或 FLIP 更新",
                details={},
                severity="info"
            )
        
        new_releases = sum(1 for e in events if e.event_type == "new_release")
        new_flips = sum(1 for e in events if e.event_type == "new_flip")
        updated_flips = sum(1 for e in events if e.event_type == "flip_update")
        
        return ChangeEvent(
            event_type="daily_summary",
            title=f"Flink 版本跟踪 - {len(events)} 个更新",
            description=f"今日检测到 {new_releases} 个新版本，{new_flips} 个新 FLIP，{updated_flips} 个 FLIP 更新",
            details={
                "total_events": len(events),
                "new_releases": new_releases,
                "new_flips": new_flips,
                "updated_flips": updated_flips
            },
            severity="info"
        )


# =============================================================================
# 通知管理器
# =============================================================================

class NotificationManager:
    """通知管理器"""
    
    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.http = HTTPClient(logger)
        
        data_dir = Path(config.get("storage", {}).get("data_dir", "./data"))
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化通知渠道
        self.channels: List[NotificationChannel] = []
        
        # Slack
        slack_config = config.get("notification", {}).get("slack", {})
        self.channels.append(SlackNotifier(slack_config, logger, self.http))
        
        # Email
        email_config = config.get("notification", {}).get("email", {})
        self.channels.append(EmailNotifier(email_config, logger))
        
        # Webhook
        webhook_config = config.get("notification", {}).get("webhook", {})
        self.channels.append(WebhookNotifier(webhook_config, logger, self.http))
        
        # File (始终启用)
        file_config = {"enabled": True}
        self.channels.append(FileNotifier(file_config, logger, data_dir))
    
    def send(self, event: ChangeEvent) -> List[NotificationResult]:
        """发送通知到所有启用的渠道"""
        results = []
        
        for channel in self.channels:
            try:
                result = channel.send(event)
                results.append(result)
                
                if result.success:
                    self.logger.info(f"[{channel.__class__.__name__}] {result.message}")
                else:
                    self.logger.warning(f"[{channel.__class__.__name__}] {result.message}: {result.error}")
                    
            except Exception as e:
                self.logger.error(f"通知发送异常: {e}")
                results.append(NotificationResult(
                    success=False,
                    channel=channel.__class__.__name__,
                    message="发送异常",
                    error=str(e)
                ))
        
        return results
    
    def send_batch(self, events: List[ChangeEvent]) -> Dict[str, List[NotificationResult]]:
        """批量发送通知"""
        all_results = {}
        
        for event in events:
            results = self.send(event)
            all_results[event.event_type] = results
        
        return all_results
    
    def load_check_results(self, result_type: str = "all") -> Dict:
        """加载检查结果"""
        data_dir = Path(self.config.get("storage", {}).get("data_dir", "./data"))
        
        results = {}
        
        if result_type in ["all", "release"]:
            release_file = data_dir / "release_check_result.json"
            if release_file.exists():
                try:
                    with open(release_file, 'r', encoding='utf-8') as f:
                        results["release"] = json.load(f)
                except (json.JSONDecodeError, IOError) as e:
                    self.logger.error(f"加载发布检查结果失败: {e}")
        
        if result_type in ["all", "flip"]:
            flip_file = data_dir / "flip_check_result.json"
            if flip_file.exists():
                try:
                    with open(flip_file, 'r', encoding='utf-8') as f:
                        results["flip"] = json.load(f)
                except (json.JSONDecodeError, IOError) as e:
                    self.logger.error(f"加载 FLIP 检查结果失败: {e}")
        
        return results


# =============================================================================
# 命令行接口
# =============================================================================

def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Flink Change Notifier - 发送变更通知",
        epilog="""
示例:
  %(prog)s --test-slack                # 测试 Slack 通知
  %(prog)s --test-email                # 测试邮件通知
  %(prog)s --from-check-results        # 从检查结果发送通知
  %(prog)s --daily-summary             # 发送每日摘要
        """
    )
    
    parser.add_argument("-c", "--config", default="config.json",
                        help="配置文件路径")
    parser.add_argument("--test-slack", action="store_true",
                        help="发送测试 Slack 通知")
    parser.add_argument("--test-email", action="store_true",
                        help="发送测试邮件")
    parser.add_argument("--test-webhook", action="store_true",
                        help="发送测试 Webhook")
    parser.add_argument("--from-check-results", action="store_true",
                        help="从检查结果发送通知")
    parser.add_argument("--daily-summary", action="store_true",
                        help="发送每日摘要")
    parser.add_argument("--event-type", default="test",
                        help="事件类型")
    parser.add_argument("--title", default="测试通知",
                        help="通知标题")
    parser.add_argument("--message", default="这是一条测试消息",
                        help="通知内容")
    parser.add_argument("-l", "--log-level", default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    
    args = parser.parse_args()
    
    # 检查依赖
    if not HAS_REQUESTS:
        print("警告: 未安装 requests 库，使用 urllib 作为后备")
    
    # 设置日志
    logger = setup_logging(args.log_level)
    
    # 加载配置
    config = load_config(args.config)
    
    # 创建管理器
    manager = NotificationManager(config, logger)
    
    logger.info("=" * 60)
    logger.info("Flink Change Notifier v1.0")
    logger.info("=" * 60)
    
    # 确定要发送的事件
    events = []
    
    if args.test_slack or args.test_email or args.test_webhook:
        events.append(ChangeEvent(
            event_type=args.event_type,
            title=args.title,
            description=args.message,
            details={"test": True, "timestamp": datetime.now().isoformat()},
            severity="info"
        ))
    
    elif args.from_check_results:
        results = manager.load_check_results()
        
        if "release" in results:
            events.extend(ChangeSummaryGenerator.from_release_check(results["release"]))
        if "flip" in results:
            events.extend(ChangeSummaryGenerator.from_flip_check(results["flip"]))
        
        logger.info(f"从检查结果生成了 {len(events)} 个事件")
    
    elif args.daily_summary:
        results = manager.load_check_results()
        all_events = []
        
        if "release" in results:
            all_events.extend(ChangeSummaryGenerator.from_release_check(results["release"]))
        if "flip" in results:
            all_events.extend(ChangeSummaryGenerator.from_flip_check(results["flip"]))
        
        events.append(ChangeSummaryGenerator.create_daily_summary(all_events))
    
    else:
        # 默认发送测试通知
        events.append(ChangeEvent(
            event_type="test",
            title="Flink Version Tracker 测试",
            description="通知系统运行正常",
            details={"test": True},
            severity="info"
        ))
    
    # 发送通知
    if events:
        print(f"\n发送 {len(events)} 个通知事件...")
        
        for event in events:
            print(f"\n事件: {event.title}")
            results = manager.send(event)
            
            for result in results:
                status = "✅" if result.success else "❌"
                print(f"  {status} [{result.channel}] {result.message}")
    else:
        print("\n没有需要发送的通知")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
