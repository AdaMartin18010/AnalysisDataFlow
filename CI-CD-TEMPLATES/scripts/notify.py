#!/usr/bin/env python3
"""
================================================================================
AnalysisDataFlow 自动通知脚本
================================================================================
描述: 自动化通知脚本，支持多种通知渠道
功能:
  - Slack通知
  - 邮件通知
  - Webhook通知
  - 企业微信/钉钉/飞书通知
  - 生成通知消息模板

使用方法:
  python notify.py [选项] --message "通知内容"

选项:
  --channel CHANNEL   通知渠道: slack|email|webhook|wecom|dingtalk|lark
  --message MESSAGE   通知消息内容
  --title TITLE       通知标题
  --level LEVEL       通知级别: info|warning|error|success
  --config FILE       配置文件路径

环境变量:
  SLACK_WEBHOOK_URL       Slack Webhook URL
  EMAIL_SMTP_HOST         SMTP服务器地址
  EMAIL_SMTP_PORT         SMTP端口
  EMAIL_USER              邮箱用户名
  EMAIL_PASSWORD          邮箱密码
  WEBHOOK_URL             通用Webhook URL
  WECOM_WEBHOOK_URL       企业微信Webhook URL
  DINGTALK_WEBHOOK_URL    钉钉Webhook URL
  LARK_WEBHOOK_URL        飞书Webhook URL

示例:
  # Slack通知
  python notify.py --channel slack --title "构建成功" --message "项目构建完成"

  # 使用环境变量
  export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
  python notify.py --channel slack --level success --message "部署完成"
================================================================================
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, Optional, List

# 尝试导入可选依赖
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("警告: requests库未安装，HTTP通知功能不可用")
    print("安装命令: pip install requests")


try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    SMTP_AVAILABLE = True
except ImportError:
    SMTP_AVAILABLE = False


class NotificationChannel:
    """通知渠道基类"""
    
    def __init__(self, config: Dict):
        self.config = config
    
    def send(self, title: str, message: str, level: str = 'info') -> bool:
        """发送通知"""
        raise NotImplementedError


class SlackNotifier(NotificationChannel):
    """Slack通知器"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.webhook_url = config.get('webhook_url') or os.getenv('SLACK_WEBHOOK_URL')
    
    def send(self, title: str, message: str, level: str = 'info') -> bool:
        if not REQUESTS_AVAILABLE:
            print("❌ requests库不可用")
            return False
        
        if not self.webhook_url:
            print("❌ Slack Webhook URL未配置")
            return False
        
        # 颜色映射
        color_map = {
            'info': '#36a64f',      # 绿色
            'warning': '#ff9900',   # 橙色
            'error': '#ff0000',     # 红色
            'success': '#36a64f'    # 绿色
        }
        
        emoji_map = {
            'info': ':information_source:',
            'warning': ':warning:',
            'error': ':x:',
            'success': ':white_check_mark:'
        }
        
        payload = {
            "attachments": [
                {
                    "color": color_map.get(level, '#36a64f'),
                    "title": f"{emoji_map.get(level, '')} {title}",
                    "text": message,
                    "footer": "AnalysisDataFlow CI/CD",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            print("✅ Slack通知发送成功")
            return True
        except Exception as e:
            print(f"❌ Slack通知发送失败: {e}")
            return False


class EmailNotifier(NotificationChannel):
    """邮件通知器"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.smtp_host = config.get('smtp_host') or os.getenv('EMAIL_SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(config.get('smtp_port') or os.getenv('EMAIL_SMTP_PORT', '587'))
        self.user = config.get('user') or os.getenv('EMAIL_USER')
        self.password = config.get('password') or os.getenv('EMAIL_PASSWORD')
        self.to_addresses = config.get('to', '').split(',') if config.get('to') else []
    
    def send(self, title: str, message: str, level: str = 'info') -> bool:
        if not SMTP_AVAILABLE:
            print("❌ SMTP模块不可用")
            return False
        
        if not all([self.user, self.password, self.to_addresses]):
            print("❌ 邮件配置不完整")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.user
            msg['To'] = ', '.join(self.to_addresses)
            msg['Subject'] = f"[AnalysisDataFlow] {title}"
            
            # 添加HTML内容
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: {'#28a745' if level == 'success' else '#dc3545' if level == 'error' else '#ffc107'};">
                    {title}
                </h2>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
                    <pre style="white-space: pre-wrap;">{message}</pre>
                </div>
                <p style="color: #6c757d; font-size: 12px; margin-top: 20px;">
                    发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)
            
            print("✅ 邮件发送成功")
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败: {e}")
            return False


class WebhookNotifier(NotificationChannel):
    """通用Webhook通知器"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.webhook_url = config.get('url') or os.getenv('WEBHOOK_URL')
        self.headers = config.get('headers', {'Content-Type': 'application/json'})
    
    def send(self, title: str, message: str, level: str = 'info') -> bool:
        if not REQUESTS_AVAILABLE:
            print("❌ requests库不可用")
            return False
        
        if not self.webhook_url:
            print("❌ Webhook URL未配置")
            return False
        
        payload = {
            "title": title,
            "message": message,
            "level": level,
            "timestamp": datetime.now().isoformat(),
            "source": "AnalysisDataFlow CI/CD"
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            print("✅ Webhook通知发送成功")
            return True
        except Exception as e:
            print(f"❌ Webhook通知发送失败: {e}")
            return False


class WeComNotifier(NotificationChannel):
    """企业微信通知器"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.webhook_url = config.get('webhook_url') or os.getenv('WECOM_WEBHOOK_URL')
    
    def send(self, title: str, message: str, level: str = 'info') -> bool:
        if not REQUESTS_AVAILABLE:
            print("❌ requests库不可用")
            return False
        
        if not self.webhook_url:
            print("❌ 企业微信Webhook URL未配置")
            return False
        
        # 根据级别选择颜色
        color_map = {
            'info': 'info',
            'warning': 'warning',
            'error': 'comment',
            'success': 'info'
        }
        
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"""**{title}**

{message}

> 发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            }
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            print("✅ 企业微信通知发送成功")
            return True
        except Exception as e:
            print(f"❌ 企业微信通知发送失败: {e}")
            return False


class DingTalkNotifier(NotificationChannel):
    """钉钉通知器"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.webhook_url = config.get('webhook_url') or os.getenv('DINGTALK_WEBHOOK_URL')
        self.secret = config.get('secret') or os.getenv('DINGTALK_SECRET', '')
    
    def send(self, title: str, message: str, level: str = 'info') -> bool:
        if not REQUESTS_AVAILABLE:
            print("❌ requests库不可用")
            return False
        
        if not self.webhook_url:
            print("❌ 钉钉Webhook URL未配置")
            return False
        
        import time
        import hmac
        import hashlib
        import base64
        import urllib.parse
        
        # 计算签名
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = f'{timestamp}\n{self.secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        
        webhook_url = f"{self.webhook_url}&timestamp={timestamp}&sign={sign}"
        
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"### {title}\n\n{message}\n\n---\n发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            }
        }
        
        try:
            response = requests.post(
                webhook_url,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            print("✅ 钉钉通知发送成功")
            return True
        except Exception as e:
            print(f"❌ 钉钉通知发送失败: {e}")
            return False


class LarkNotifier(NotificationChannel):
    """飞书通知器"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.webhook_url = config.get('webhook_url') or os.getenv('LARK_WEBHOOK_URL')
    
    def send(self, title: str, message: str, level: str = 'info') -> bool:
        if not REQUESTS_AVAILABLE:
            print("❌ requests库不可用")
            return False
        
        if not self.webhook_url:
            print("❌ 飞书Webhook URL未配置")
            return False
        
        # 颜色映射
        color_map = {
            'info': 'blue',
            'warning': 'orange',
            'error': 'red',
            'success': 'green'
        }
        
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": title
                    },
                    "template": color_map.get(level, 'blue')
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": message
                        }
                    },
                    {
                        "tag": "note",
                        "elements": [
                            {
                                "tag": "plain_text",
                                "content": f"发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            }
                        ]
                    }
                ]
            }
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            print("✅ 飞书通知发送成功")
            return True
        except Exception as e:
            print(f"❌ 飞书通知发送失败: {e}")
            return False


class NotificationManager:
    """通知管理器"""
    
    NOTIFIER_MAP = {
        'slack': SlackNotifier,
        'email': EmailNotifier,
        'webhook': WebhookNotifier,
        'wecom': WeComNotifier,
        'dingtalk': DingTalkNotifier,
        'lark': LarkNotifier,
        'wechat': WeComNotifier,  # 别名
    }
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.notifiers: Dict[str, NotificationChannel] = {}
    
    def get_notifier(self, channel: str, channel_config: Optional[Dict] = None) -> Optional[NotificationChannel]:
        """获取通知器实例"""
        if channel not in self.NOTIFIER_MAP:
            print(f"❌ 未知的通知渠道: {channel}")
            print(f"支持的渠道: {', '.join(self.NOTIFIER_MAP.keys())}")
            return None
        
        config = channel_config or self.config.get(channel, {})
        notifier_class = self.NOTIFIER_MAP[channel]
        return notifier_class(config)
    
    def send(self, channel: str, title: str, message: str, level: str = 'info', 
             channel_config: Optional[Dict] = None) -> bool:
        """发送通知"""
        notifier = self.get_notifier(channel, channel_config)
        if notifier:
            return notifier.send(title, message, level)
        return False
    
    def broadcast(self, channels: List[str], title: str, message: str, level: str = 'info') -> Dict[str, bool]:
        """广播到多个渠道"""
        results = {}
        for channel in channels:
            results[channel] = self.send(channel, title, message, level)
        return results


def load_config(config_path: str) -> Dict:
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  无法加载配置文件 {config_path}: {e}")
        return {}


def generate_build_message(
    status: str,
    project: str = "AnalysisDataFlow",
    branch: str = "main",
    commit: str = "",
    build_url: str = "",
    duration: str = "",
    errors: List[str] = None
) -> str:
    """生成构建通知消息"""
    status_emoji = {
        'success': '✅',
        'failure': '❌',
        'aborted': '🚫',
        'unstable': '⚠️'
    }.get(status, 'ℹ️')
    
    message = f"""{status_emoji} **构建{status.upper()}**

📦 **项目:** {project}
🌿 **分支:** {branch}
"""
    
    if commit:
        message += f"🔖 **提交:** {commit[:8]}\n"
    
    if duration:
        message += f"⏱️ **耗时:** {duration}\n"
    
    if build_url:
        message += f"🔗 **链接:** {build_url}\n"
    
    if errors:
        message += f"\n❌ **错误:**\n"
        for error in errors[:5]:
            message += f"  - {error}\n"
        if len(errors) > 5:
            message += f"  ...还有 {len(errors) - 5} 个错误\n"
    
    return message


def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 通知工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # Slack通知
  export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
  python notify.py --channel slack --title "构建成功" --message "部署完成"

  # 多级别通知
  python notify.py --channel slack --level error --title "构建失败" --message "检查日志"
        """
    )
    
    parser.add_argument(
        '--channel',
        required=True,
        help='通知渠道 (slack|email|webhook|wecom|dingtalk|lark)'
    )
    parser.add_argument(
        '--message',
        required=True,
        help='通知消息内容'
    )
    parser.add_argument(
        '--title',
        default='AnalysisDataFlow通知',
        help='通知标题'
    )
    parser.add_argument(
        '--level',
        choices=['info', 'warning', 'error', 'success'],
        default='info',
        help='通知级别'
    )
    parser.add_argument(
        '--config',
        help='配置文件路径'
    )
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config) if args.config else {}
    
    # 创建通知管理器
    manager = NotificationManager(config)
    
    # 发送通知
    success = manager.send(
        channel=args.channel,
        title=args.title,
        message=args.message,
        level=args.level
    )
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
