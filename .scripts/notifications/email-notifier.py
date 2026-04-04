#!/usr/bin/env python3
"""
邮件通知模块 (Email Notifier)

提供异步邮件发送功能，支持 HTML/纯文本格式、附件和模板系统。

作者: AnalysisDataFlow Team
日期: 2026-04-04
"""

import asyncio
import logging
import smtplib
import ssl
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from string import Template
import mimetypes

import aiofiles
import yaml
import aiosmtplib

logger = logging.getLogger(__name__)


@dataclass
class EmailAttachment:
    """邮件附件"""
    path: Union[str, Path]
    filename: Optional[str] = None
    content_type: Optional[str] = None
    content_id: Optional[str] = None  # 用于内嵌图片
    
    def __post_init__(self):
        self.path = Path(self.path)
        if not self.filename:
            self.filename = self.path.name
        if not self.content_type:
            self.content_type, _ = mimetypes.guess_type(str(self.path))
            if not self.content_type:
                self.content_type = "application/octet-stream"


@dataclass
class EmailMessage:
    """邮件消息"""
    subject: str
    to_addresses: List[str]
    from_address: str
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    cc_addresses: List[str] = field(default_factory=list)
    bcc_addresses: List[str] = field(default_factory=list)
    attachments: List[EmailAttachment] = field(default_factory=list)
    reply_to: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)


class EmailTemplateEngine:
    """邮件模板引擎"""
    
    def __init__(self, templates_dir: Optional[Path] = None):
        self.templates_dir = templates_dir or Path(__file__).parent / "email_templates"
        self.templates_dir.mkdir(exist_ok=True)
        self._cache: Dict[str, Dict[str, str]] = {}
    
    def _get_template_path(self, name: str) -> Path:
        """获取模板文件路径"""
        return self.templates_dir / f"{name}.html"
    
    def load_template(self, name: str) -> Dict[str, str]:
        """加载模板"""
        if name in self._cache:
            return self._cache[name]
        
        template_path = self._get_template_path(name)
        
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 生成纯文本版本 (简单转换)
            text_content = self._html_to_text(html_content)
            
            template = {
                "html": html_content,
                "text": text_content
            }
            self._cache[name] = template
            return template
        
        # 返回默认模板
        return self._get_default_template(name)
    
    def _html_to_text(self, html: str) -> str:
        """简单 HTML 转文本"""
        import re
        # 移除 script 和 style
        text = re.sub(r'<(script|style).*?>.*?</\1>', '', html, flags=re.DOTALL)
        # 替换 br 标签为换行
        text = re.sub(r'<br\s*/?>', '\n', text)
        # 替换 p 标签为换行
        text = re.sub(r'</p>', '\n\n', text)
        # 移除所有 HTML 标签
        text = re.sub(r'<[^>]+>', '', text)
        # 解码 HTML 实体
        text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')
        text = text.replace('&amp;', '&').replace('&quot;', '"')
        return text.strip()
    
    def _get_default_template(self, name: str) -> Dict[str, str]:
        """获取默认模板"""
        templates = {
            "alert": {
                "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #f44336; color: white; padding: 20px; text-align: center; }
        .content { background-color: #f9f9f9; padding: 20px; margin: 20px 0; }
        .footer { text-align: center; color: #666; font-size: 12px; margin-top: 20px; }
        .severity-critical { background-color: #d32f2f; }
        .severity-warning { background-color: #f57c00; }
        .severity-info { background-color: #1976d2; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header severity-$severity">
            <h1>🚨 $title</h1>
        </div>
        <div class="content">
            <h2>告警详情</h2>
            <p><strong>服务:</strong> $service</p>
            <p><strong>时间:</strong> $timestamp</p>
            <p><strong>级别:</strong> $severity</p>
            <hr>
            <p>$message</p>
        </div>
        <div class="footer">
            <p>本邮件由系统自动发送，请勿回复</p>
            <p>AnalysisDataFlow Notification System</p>
        </div>
    </div>
</body>
</html>
""",
                "text": """
告警通知: $title
================================

服务: $service
时间: $timestamp
级别: $severity

$message

---
本邮件由系统自动发送，请勿回复
AnalysisDataFlow Notification System
"""
            },
            "report": {
                "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { background-color: #2196F3; color: white; padding: 20px; text-align: center; }
        .content { background-color: #fff; padding: 20px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f5f5f5; }
        .metric { display: inline-block; margin: 10px; padding: 15px; background-color: #e3f2fd; border-radius: 8px; }
        .metric-value { font-size: 24px; font-weight: bold; color: #1976d2; }
        .footer { text-align: center; color: #666; font-size: 12px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 $title</h1>
            <p>$subtitle</p>
        </div>
        <div class="content">
            $content
        </div>
        <div class="footer">
            <p>生成时间: $generated_at</p>
            <p>AnalysisDataFlow Report System</p>
        </div>
    </div>
</body>
</html>
""",
                "text": """
$title
$subtitle
================================

$content

---
生成时间: $generated_at
AnalysisDataFlow Report System
"""
            },
            "notification": {
                "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; }
        .container { max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; }
        .header { border-bottom: 3px solid #4CAF50; padding-bottom: 15px; margin-bottom: 20px; }
        .content { margin: 20px 0; }
        .button { display: inline-block; padding: 12px 24px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 4px; }
        .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>$title</h1>
        </div>
        <div class="content">
            $content
        </div>
        <div class="footer">
            <p>AnalysisDataFlow Notification System</p>
        </div>
    </div>
</body>
</html>
""",
                "text": """
$title
================================

$content

---
AnalysisDataFlow Notification System
"""
            }
        }
        
        return templates.get(name, templates["notification"])
    
    def render(self, template_name: str, data: Dict[str, Any]) -> Dict[str, str]:
        """渲染模板"""
        template = self.load_template(template_name)
        
        # 使用 string.Template 进行简单替换
        html_template = Template(template["html"])
        text_template = Template(template["text"])
        
        return {
            "html": html_template.safe_substitute(data),
            "text": text_template.safe_substitute(data)
        }
    
    def save_template(self, name: str, html_content: str, text_content: Optional[str] = None):
        """保存模板到文件"""
        template_path = self._get_template_path(name)
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 更新缓存
        self._cache[name] = {
            "html": html_content,
            "text": text_content or self._html_to_text(html_content)
        }


class EmailNotifier:
    """
    邮件通知器
    
    功能特性:
    - 异步发送 (aiosmtplib)
    - HTML/纯文本双格式
    - 附件支持
    - 模板系统
    - 批量发送
    - 连接池复用
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config = self._load_config(config_path)
        
        # SMTP 配置
        smtp_config = self.config.get("email", {})
        self.smtp_host = smtp_config.get("smtp_host", "smtp.gmail.com")
        self.smtp_port = smtp_config.get("smtp_port", 587)
        self.smtp_user = smtp_config.get("smtp_user")
        self.smtp_password = smtp_config.get("smtp_password")
        self.use_tls = smtp_config.get("use_tls", True)
        self.timeout = smtp_config.get("timeout", 30)
        
        # 默认设置
        self.default_from = smtp_config.get("from_address", self.smtp_user)
        
        # 模板引擎
        self.template_engine = EmailTemplateEngine()
        
        # 连接池
        self._smtp: Optional[aiosmtplib.SMTP] = None
        self._connected = False
    
    def _load_config(self, config_path: Optional[Path]) -> Dict[str, Any]:
        """加载配置"""
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    async def _get_smtp(self) -> aiosmtplib.SMTP:
        """获取或创建 SMTP 连接"""
        if self._smtp is None or not self._connected:
            self._smtp = aiosmtplib.SMTP(
                self.smtp_host,
                self.smtp_port,
                timeout=self.timeout
            )
            await self._smtp.connect()
            
            if self.use_tls:
                await self._smtp.starttls()
            
            if self.smtp_user and self.smtp_password:
                await self._smtp.login(self.smtp_user, self.smtp_password)
            
            self._connected = True
            logger.info("SMTP 连接已建立")
        
        return self._smtp
    
    async def _close_smtp(self):
        """关闭 SMTP 连接"""
        if self._smtp and self._connected:
            await self._smtp.quit()
            self._connected = False
            self._smtp = None
            logger.info("SMTP 连接已关闭")
    
    def _build_message(
        self,
        message: EmailMessage
    ) -> MIMEMultipart:
        """构建 MIME 消息"""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = message.subject
        msg["From"] = message.from_address
        msg["To"] = ", ".join(message.to_addresses)
        
        if message.cc_addresses:
            msg["Cc"] = ", ".join(message.cc_addresses)
        
        if message.reply_to:
            msg["Reply-To"] = message.reply_to
        
        # 添加自定义头
        for key, value in message.headers.items():
            msg[key] = value
        
        # 添加纯文本部分
        if message.body_text:
            msg.attach(MIMEText(message.body_text, "plain", "utf-8"))
        
        # 添加 HTML 部分
        if message.body_html:
            msg.attach(MIMEText(message.body_html, "html", "utf-8"))
        
        # 处理附件
        if message.attachments:
            # 创建混合消息容器
            mixed_msg = MIMEMultipart("mixed")
            mixed_msg.attach(msg)
            
            for attachment in message.attachments:
                part = self._create_attachment_part(attachment)
                mixed_msg.attach(part)
            
            return mixed_msg
        
        return msg
    
    def _create_attachment_part(self, attachment: EmailAttachment) -> MIMEBase:
        """创建附件部分"""
        with open(attachment.path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        
        disposition = f'attachment; filename="{attachment.filename}"'
        part.add_header("Content-Disposition", disposition)
        
        if attachment.content_id:
            part.add_header("Content-ID", f"<{attachment.content_id}>")
        
        return part
    
    async def send(
        self,
        to_addresses: Union[str, List[str]],
        subject: str,
        body_text: Optional[str] = None,
        body_html: Optional[str] = None,
        template_name: Optional[str] = None,
        template_data: Optional[Dict] = None,
        cc_addresses: Optional[List[str]] = None,
        bcc_addresses: Optional[List[str]] = None,
        attachments: Optional[List[Union[str, Path, EmailAttachment]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送邮件
        
        Args:
            to_addresses: 收件人地址
            subject: 主题
            body_text: 纯文本内容
            body_html: HTML 内容
            template_name: 模板名称
            template_data: 模板数据
            cc_addresses: 抄送地址
            bcc_addresses: 密送地址
            attachments: 附件列表
            
        Returns:
            发送结果
        """
        # 处理收件人
        if isinstance(to_addresses, str):
            to_addresses = [to_addresses]
        
        # 使用模板
        if template_name and template_data:
            rendered = self.template_engine.render(template_name, template_data)
            body_html = rendered["html"]
            body_text = rendered["text"]
        
        # 处理附件
        email_attachments = []
        if attachments:
            for att in attachments:
                if isinstance(att, (str, Path)):
                    email_attachments.append(EmailAttachment(att))
                elif isinstance(att, EmailAttachment):
                    email_attachments.append(att)
        
        message = EmailMessage(
            subject=subject,
            to_addresses=to_addresses,
            from_address=self.default_from,
            body_text=body_text,
            body_html=body_html,
            cc_addresses=cc_addresses or [],
            bcc_addresses=bcc_addresses or [],
            attachments=email_attachments
        )
        
        return await self._send_message(message)
    
    async def _send_message(self, message: EmailMessage) -> Dict[str, Any]:
        """实际发送消息"""
        try:
            smtp = await self._get_smtp()
            mime_msg = self._build_message(message)
            
            # 合并所有接收人
            all_recipients = (
                message.to_addresses + 
                message.cc_addresses + 
                message.bcc_addresses
            )
            
            await smtp.send_message(
                mime_msg,
                sender=message.from_address,
                recipients=all_recipients
            )
            
            logger.info(f"邮件发送成功: {message.subject} -> {message.to_addresses}")
            
            return {
                "success": True,
                "message_id": mime_msg.get("Message-ID"),
                "recipients": all_recipients
            }
            
        except Exception as e:
            logger.error(f"邮件发送失败: {e}")
            # 连接失败时重置
            if "Connection" in str(e) or "authentication" in str(e).lower():
                await self._close_smtp()
            raise
    
    async def send_batch(
        self,
        messages: List[EmailMessage],
        delay: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        批量发送邮件
        
        Args:
            messages: 邮件消息列表
            delay: 每封邮件间隔(秒)，避免触发频率限制
        """
        results = []
        
        for i, message in enumerate(messages):
            try:
                result = await self._send_message(message)
                results.append(result)
                
                # 间隔发送
                if i < len(messages) - 1:
                    await asyncio.sleep(delay)
                    
            except Exception as e:
                logger.error(f"批量发送中第 {i+1} 封邮件失败: {e}")
                results.append({"success": False, "error": str(e)})
        
        return results
    
    async def close(self):
        """关闭连接"""
        await self._close_smtp()


# 便捷函数
async def send_alert_email(
    to_addresses: Union[str, List[str]],
    title: str,
    service: str,
    message: str,
    severity: str = "warning",
    **kwargs
) -> Dict[str, Any]:
    """快速发送告警邮件"""
    notifier = EmailNotifier()
    
    try:
        result = await notifier.send(
            to_addresses=to_addresses,
            subject=f"[{severity.upper()}] {title}",
            template_name="alert",
            template_data={
                "title": title,
                "service": service,
                "message": message,
                "severity": severity,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            **kwargs
        )
        return result
    finally:
        await notifier.close()


async def send_report_email(
    to_addresses: Union[str, List[str]],
    title: str,
    subtitle: str,
    content: str,
    **kwargs
) -> Dict[str, Any]:
    """发送报告邮件"""
    notifier = EmailNotifier()
    
    try:
        result = await notifier.send(
            to_addresses=to_addresses,
            subject=title,
            template_name="report",
            template_data={
                "title": title,
                "subtitle": subtitle,
                "content": content,
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            **kwargs
        )
        return result
    finally:
        await notifier.close()


# 使用示例
async def example():
    """使用示例"""
    # 发送告警邮件
    result = await send_alert_email(
        to_addresses=["admin@example.com"],
        title="数据库连接异常",
        service="user-service",
        message="无法连接到主数据库，已切换到备份节点",
        severity="critical"
    )
    print(f"告警邮件结果: {result}")
    
    # 发送报告邮件
    report_content = """
    <h3>系统性能指标</h3>
    <table>
        <tr><th>指标</th><th>数值</th></tr>
        <tr><td>CPU 使用率</td><td>45%</td></tr>
        <tr><td>内存使用</td><td>6.2GB / 16GB</td></tr>
        <tr><td>磁盘 I/O</td><td>120 MB/s</td></tr>
    </table>
    """
    
    result = await send_report_email(
        to_addresses=["team@example.com"],
        title="每日系统报告",
        subtitle="2026-04-04",
        content=report_content
    )
    print(f"报告邮件结果: {result}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # asyncio.run(example())
    pass
