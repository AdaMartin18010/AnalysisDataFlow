#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 学术顾问邀请邮件发送工具

功能：
- 读取邮件模板并个性化定制
- 发送邮件并记录状态
- 错误处理和重试机制
- 发送日志保存

作者: AnalysisDataFlow Project Team
版本: 1.0.0
日期: 2026-04-12
"""

import json
import logging
import os
import re
import smtplib
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Optional, Dict, Any


# ============================================================================
# 配置常量
# ============================================================================

CONFIG = {
    "sender_email": "advisory-board@analysisdataflow.org",
    "sender_name": "AnalysisDataFlow Project Team",
    "smtp_server": "smtp.gmail.com",  # 根据实际情况修改
    "smtp_port": 587,
    "use_tls": True,
    "send_interval_seconds": 1800,  # 30分钟间隔
    "max_retries": 3,
    "retry_delay_seconds": 60,
    "log_file": "email-sender.log",
    "record_file": "send-records.json",
    "emails_dir": "emails",
    "attachments_dir": "attachments",
}


# ============================================================================
# 数据类定义
# ============================================================================

@dataclass
class EmailTemplate:
    """邮件模板数据类"""
    recipient_name: str
    recipient_email: str
    subject: str
    body: str
    attachments: List[str]
    template_path: str


@dataclass
class SendRecord:
    """发送记录数据类"""
    id: str
    recipient_name: str
    recipient_email: str
    subject: str
    sent_at: Optional[str]
    status: str  # pending, sending, sent, failed, retrying
    error_message: Optional[str]
    retry_count: int
    template_path: str


# ============================================================================
# 日志配置
# ============================================================================

def setup_logging(log_file: str = CONFIG["log_file"]) -> logging.Logger:
    """配置日志系统"""
    logger = logging.getLogger("EmailSender")
    logger.setLevel(logging.INFO)
    
    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


logger = setup_logging()


# ============================================================================
# 邮件解析类
# ============================================================================

class MarkdownEmailParser:
    """Markdown格式邮件解析器"""
    
    @staticmethod
    def parse_email_file(file_path: str) -> EmailTemplate:
        """
        解析Markdown格式的邮件文件
        
        Args:
            file_path: 邮件文件路径
            
        Returns:
            EmailTemplate对象
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析主题行
        subject_match = re.search(r'\*\*Subject\*\*:\s*(.+?)(?:\n|$)', content)
        subject = subject_match.group(1).strip() if subject_match else ""
        
        # 解析收件人姓名（从文件名或内容中提取）
        recipient_name = MarkdownEmailParser._extract_recipient_name(file_path, content)
        
        # 解析邮件正文（在"## 邮件内容"之后）
        body_match = re.search(r'## 邮件内容\s*\n\n(.+?)(?:\n---|\Z)', content, re.DOTALL)
        if body_match:
            body = body_match.group(1).strip()
        else:
            # 尝试提取邮件主体部分
            body_start = content.find("Dear ")
            if body_start > 0:
                body = content[body_start:].strip()
            else:
                body = content
        
        # 解析附件清单
        attachments = MarkdownEmailParser._extract_attachments(content)
        
        return EmailTemplate(
            recipient_name=recipient_name,
            recipient_email="",  # 需要手动配置
            subject=subject,
            body=body,
            attachments=attachments,
            template_path=file_path
        )
    
    @staticmethod
    def _extract_recipient_name(file_path: str, content: str) -> str:
        """提取收件人姓名"""
        # 尝试从文件名提取
        file_name = os.path.basename(file_path)
        name_match = re.search(r'\d+-([\w-]+)-invitation', file_name)
        if name_match:
            name_slug = name_match.group(1)
            # 转换 slug 为正式名称
            name_map = {
                'tyler-akidau': 'Tyler Akidau',
                'martin-kleppmann': 'Martin Kleppmann',
                'stephan-ewen': 'Stephan Ewen',
                'neha-narkhede': 'Neha Narkhede',
                'volker-markl': 'Volker Markl',
            }
            return name_map.get(name_slug, name_slug.replace('-', ' ').title())
        
        # 尝试从内容标题提取
        title_match = re.search(r'^# (.+?)个性化邀请邮件', content)
        if title_match:
            return title_match.group(1).strip()
        
        return "Unknown"
    
    @staticmethod
    def _extract_attachments(content: str) -> List[str]:
        """提取附件列表"""
        attachments = []
        
        # 查找附件清单部分
        attach_match = re.search(r'## 附件清单\s*\n\n(.+?)(?:\n---|\Z)', content, re.DOTALL)
        if attach_match:
            attach_section = attach_match.group(1)
            # 提取已勾选的附件
            for line in attach_section.split('\n'):
                if line.strip().startswith('- [x]'):
                    file_match = re.search(r'- \[x\]\s*(.+?)(?:\s*\(|$)', line)
                    if file_match:
                        attachments.append(file_match.group(1).strip())
        
        return attachments
    
    @staticmethod
    def personalize_email(template: EmailTemplate, **kwargs) -> EmailTemplate:
        """
        个性化邮件内容
        
        Args:
            template: 原始模板
            **kwargs: 替换变量
            
        Returns:
            个性化后的模板
        """
        body = template.body
        
        # 替换变量
        for key, value in kwargs.items():
            placeholder = f"[{key}]"
            body = body.replace(placeholder, str(value))
        
        # 替换默认变量
        defaults = {
            "Your Name": kwargs.get("sender_name", CONFIG["sender_name"]),
            "Your Full Name": kwargs.get("sender_full_name", CONFIG["sender_name"]),
            "Your Title": kwargs.get("sender_title", "Project Lead"),
            "email@analysisdataflow.org": CONFIG["sender_email"],
        }
        
        for key, value in defaults.items():
            body = body.replace(f"[{key}]", value)
        
        return EmailTemplate(
            recipient_name=template.recipient_name,
            recipient_email=kwargs.get("recipient_email", template.recipient_email),
            subject=template.subject,
            body=body,
            attachments=template.attachments,
            template_path=template.template_path
        )


# ============================================================================
# 邮件发送类
# ============================================================================

class EmailSender:
    """邮件发送器"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or CONFIG
        self.records: List[SendRecord] = []
        self._load_records()
    
    def _load_records(self):
        """加载历史发送记录"""
        record_file = self.config["record_file"]
        if os.path.exists(record_file):
            try:
                with open(record_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.records = [SendRecord(**r) for r in data]
                logger.info(f"加载了 {len(self.records)} 条历史记录")
            except Exception as e:
                logger.error(f"加载记录失败: {e}")
                self.records = []
    
    def _save_records(self):
        """保存发送记录"""
        record_file = self.config["record_file"]
        try:
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(r) for r in self.records], f, indent=2, ensure_ascii=False)
            logger.info(f"保存了 {len(self.records)} 条记录")
        except Exception as e:
            logger.error(f"保存记录失败: {e}")
    
    def _create_email_message(self, template: EmailTemplate) -> MIMEMultipart:
        """创建邮件消息对象"""
        msg = MIMEMultipart('mixed')
        msg['Subject'] = template.subject
        msg['From'] = f"{self.config['sender_name']} <{self.config['sender_email']}>"
        msg['To'] = f"{template.recipient_name} <{template.recipient_email}>"
        
        # 创建邮件正文部分
        msg_body = MIMEMultipart('alternative')
        
        # 纯文本版本
        text_part = MIMEText(template.body, 'plain', 'utf-8')
        msg_body.attach(text_part)
        
        # HTML版本（简化转换）
        html_body = self._markdown_to_html(template.body)
        html_part = MIMEText(html_body, 'html', 'utf-8')
        msg_body.attach(html_part)
        
        msg.attach(msg_body)
        
        # 添加附件
        for attachment in template.attachments:
            attach_path = os.path.join(self.config["attachments_dir"], attachment)
            if os.path.exists(attach_path):
                with open(attach_path, 'rb') as f:
                    part = MIMEApplication(f.read(), Name=attachment)
                    part['Content-Disposition'] = f'attachment; filename="{attachment}"'
                    msg.attach(part)
                logger.info(f"添加附件: {attachment}")
            else:
                logger.warning(f"附件不存在: {attach_path}")
        
        return msg
    
    def _markdown_to_html(self, markdown_text: str) -> str:
        """简单Markdown转HTML"""
        html = markdown_text
        
        # 基本转换
        html = html.replace('&', '&amp;')
        html = html.replace('<', '&lt;')
        html = html.replace('>', '&gt;')
        
        # 标题
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # 粗体和斜体
        html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        
        # 链接
        html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
        
        # 段落
        paragraphs = html.split('\n\n')
        html = '\n'.join(f'<p>{p}</p>' if not p.startswith('<h') else p for p in paragraphs)
        
        # 包装在HTML文档中
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #555; border-bottom: 1px solid #ddd; padding-bottom: 5px; }}
        h3 {{ color: #666; }}
        a {{ color: #0066cc; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
        
        return html
    
    def send_email(self, template: EmailTemplate, dry_run: bool = False) -> bool:
        """
        发送单封邮件
        
        Args:
            template: 邮件模板
            dry_run: 如果为True，只模拟发送不实际发送
            
        Returns:
            发送是否成功
        """
        record_id = f"{template.recipient_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        record = SendRecord(
            id=record_id,
            recipient_name=template.recipient_name,
            recipient_email=template.recipient_email,
            subject=template.subject,
            sent_at=None,
            status="sending",
            error_message=None,
            retry_count=0,
            template_path=template.template_path
        )
        
        self.records.append(record)
        
        if dry_run:
            logger.info(f"[DRY RUN] 模拟发送邮件给 {template.recipient_name}")
            record.status = "dry_run"
            record.sent_at = datetime.now().isoformat()
            self._save_records()
            return True
        
        # 检查收件人邮箱
        if not template.recipient_email:
            error_msg = f"未设置收件人邮箱: {template.recipient_name}"
            logger.error(error_msg)
            record.status = "failed"
            record.error_message = error_msg
            self._save_records()
            return False
        
        # 创建邮件消息
        msg = self._create_email_message(template)
        
        # 发送邮件
        for attempt in range(self.config["max_retries"]):
            try:
                logger.info(f"发送邮件给 {template.recipient_name} (尝试 {attempt + 1}/{self.config['max_retries']})")
                
                with smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"]) as server:
                    if self.config["use_tls"]:
                        server.starttls()
                    
                    # 登录 (需要配置密码或应用密钥)
                    # server.login(self.config["sender_email"], "YOUR_PASSWORD")
                    
                    server.send_message(msg)
                
                record.status = "sent"
                record.sent_at = datetime.now().isoformat()
                logger.info(f"✅ 邮件成功发送给 {template.recipient_name}")
                self._save_records()
                return True
                
            except Exception as e:
                error_msg = str(e)
                logger.error(f"❌ 发送失败 (尝试 {attempt + 1}): {error_msg}")
                record.retry_count = attempt + 1
                record.error_message = error_msg
                
                if attempt < self.config["max_retries"] - 1:
                    record.status = "retrying"
                    logger.info(f"等待 {self.config['retry_delay_seconds']} 秒后重试...")
                    time.sleep(self.config["retry_delay_seconds"])
                else:
                    record.status = "failed"
                    logger.error(f"❌ 邮件发送最终失败: {template.recipient_name}")
                
                self._save_records()
        
        return False
    
    def send_batch(self, templates: List[EmailTemplate], dry_run: bool = False):
        """
        批量发送邮件
        
        Args:
            templates: 邮件模板列表
            dry_run: 如果为True，只模拟发送
        """
        logger.info(f"开始批量发送，共 {len(templates)} 封邮件")
        logger.info(f"发送间隔: {self.config['send_interval_seconds']} 秒")
        
        success_count = 0
        fail_count = 0
        
        for i, template in enumerate(templates):
            logger.info(f"\n{'='*60}")
            logger.info(f"处理第 {i+1}/{len(templates)} 封邮件: {template.recipient_name}")
            logger.info(f"{'='*60}")
            
            if self.send_email(template, dry_run=dry_run):
                success_count += 1
            else:
                fail_count += 1
            
            # 等待间隔（最后一封不需要等待）
            if i < len(templates) - 1:
                logger.info(f"等待 {self.config['send_interval_seconds']} 秒后发送下一封...")
                time.sleep(self.config["send_interval_seconds"])
        
        logger.info(f"\n{'='*60}")
        logger.info(f"批量发送完成")
        logger.info(f"成功: {success_count} 封")
        logger.info(f"失败: {fail_count} 封")
        logger.info(f"{'='*60}")
        
        return success_count, fail_count
    
    def get_pending_emails(self) -> List[SendRecord]:
        """获取待发送的邮件记录"""
        return [r for r in self.records if r.status in ("pending", "failed")]
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取发送统计"""
        stats = {
            "total": len(self.records),
            "pending": len([r for r in self.records if r.status == "pending"]),
            "sending": len([r for r in self.records if r.status == "sending"]),
            "sent": len([r for r in self.records if r.status == "sent"]),
            "failed": len([r for r in self.records if r.status == "failed"]),
            "retrying": len([r for r in self.records if r.status == "retrying"]),
            "dry_run": len([r for r in self.records if r.status == "dry_run"]),
        }
        return stats


# ============================================================================
# 命令行接口
# ============================================================================

def print_usage():
    """打印使用说明"""
    print("""
AnalysisDataFlow 邮件发送工具

用法:
    python email-sender.py <command> [options]

命令:
    parse <file>           解析邮件模板文件
    send <file>            发送单封邮件
    send-batch             批量发送所有准备好的邮件
    dry-run <file>         模拟发送（不实际发送）
    dry-run-batch          批量模拟发送
    status                 显示发送状态统计
    list                   列出所有邮件模板
    
选项:
    --email <email>        指定收件人邮箱
    --name <name>          指定收件人姓名
    --interval <seconds>   设置发送间隔（秒）
    
示例:
    python email-sender.py parse emails/01-tyler-akidau-invitation.md
    python email-sender.py dry-run emails/01-tyler-akidau-invitation.md --email tyler@example.com
    python email-sender.py send-batch
    python email-sender.py status
""")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1]
    sender = EmailSender()
    parser = MarkdownEmailParser()
    
    if command == "parse":
        if len(sys.argv) < 3:
            print("错误: 请指定邮件文件路径")
            sys.exit(1)
        
        file_path = sys.argv[2]
        template = parser.parse_email_file(file_path)
        
        print(f"\n解析结果:")
        print(f"收件人: {template.recipient_name}")
        print(f"主题: {template.subject}")
        print(f"附件: {', '.join(template.attachments) if template.attachments else '无'}")
        print(f"\n正文预览 (前500字符):")
        print(template.body[:500] + "..." if len(template.body) > 500 else template.body)
    
    elif command == "send":
        if len(sys.argv) < 3:
            print("错误: 请指定邮件文件路径")
            sys.exit(1)
        
        file_path = sys.argv[2]
        template = parser.parse_email_file(file_path)
        
        # 解析额外参数
        recipient_email = None
        for i, arg in enumerate(sys.argv):
            if arg == "--email" and i + 1 < len(sys.argv):
                recipient_email = sys.argv[i + 1]
        
        if recipient_email:
            template = parser.personalize_email(template, recipient_email=recipient_email)
        
        print(f"准备发送邮件给: {template.recipient_name}")
        print(f"收件人邮箱: {template.recipient_email or '未设置'}")
        confirm = input("确认发送? (yes/no): ")
        
        if confirm.lower() == "yes":
            sender.send_email(template)
        else:
            print("已取消发送")
    
    elif command == "send-batch":
        # 加载所有邮件模板
        emails_dir = CONFIG["emails_dir"]
        templates = []
        
        for file in sorted(os.listdir(emails_dir)):
            if file.endswith("-invitation.md"):
                file_path = os.path.join(emails_dir, file)
                template = parser.parse_email_file(file_path)
                templates.append(template)
                print(f"已加载: {template.recipient_name}")
        
        print(f"\n共找到 {len(templates)} 封邮件")
        confirm = input("确认批量发送? (yes/no): ")
        
        if confirm.lower() == "yes":
            sender.send_batch(templates)
        else:
            print("已取消发送")
    
    elif command == "dry-run":
        if len(sys.argv) < 3:
            print("错误: 请指定邮件文件路径")
            sys.exit(1)
        
        file_path = sys.argv[2]
        template = parser.parse_email_file(file_path)
        sender.send_email(template, dry_run=True)
    
    elif command == "dry-run-batch":
        emails_dir = CONFIG["emails_dir"]
        templates = []
        
        for file in sorted(os.listdir(emails_dir)):
            if file.endswith("-invitation.md"):
                file_path = os.path.join(emails_dir, file)
                template = parser.parse_email_file(file_path)
                templates.append(template)
        
        sender.send_batch(templates, dry_run=True)
    
    elif command == "status":
        stats = sender.get_statistics()
        print("\n发送状态统计:")
        print(f"总计: {stats['total']}")
        print(f"待发送: {stats['pending']}")
        print(f"发送中: {stats['sending']}")
        print(f"已发送: {stats['sent']}")
        print(f"发送失败: {stats['failed']}")
        print(f"重试中: {stats['retrying']}")
        print(f"模拟发送: {stats['dry_run']}")
    
    elif command == "list":
        emails_dir = CONFIG["emails_dir"]
        print("\n邮件模板列表:")
        
        for file in sorted(os.listdir(emails_dir)):
            if file.endswith("-invitation.md"):
                file_path = os.path.join(emails_dir, file)
                template = parser.parse_email_file(file_path)
                print(f"  - {file}")
                print(f"    收件人: {template.recipient_name}")
                print(f"    主题: {template.subject[:60]}...")
    
    else:
        print(f"未知命令: {command}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
