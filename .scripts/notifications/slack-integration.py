#!/usr/bin/env python3
"""
Slack 集成模块 (Slack Integration)

提供完整的 Slack 消息发送功能，支持富文本格式、频道管理和线程回复。

作者: AnalysisDataFlow Team
日期: 2026-04-04
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path

import aiohttp
import yaml

logger = logging.getLogger(__name__)


class BlockType(Enum):
    """Slack Block 类型"""
    SECTION = "section"
    DIVIDER = "divider"
    IMAGE = "image"
    ACTIONS = "actions"
    CONTEXT = "context"
    HEADER = "header"
    FILE = "file"


class TextType(Enum):
    """文本类型"""
    PLAIN = "plain_text"
    MARKDOWN = "mrkdwn"


@dataclass
class SlackField:
    """Slack 字段"""
    title: str
    value: str
    short: bool = False
    
    def to_block(self) -> Dict[str, Any]:
        return {
            "type": TextType.MARKDOWN.value,
            "text": f"*{title}*\n{value}"
        }


@dataclass
class SlackAttachment:
    """Slack 附件配置"""
    color: str = "#36a64f"  # 绿色
    pretext: Optional[str] = None
    author_name: Optional[str] = None
    author_link: Optional[str] = None
    author_icon: Optional[str] = None
    title: Optional[str] = None
    title_link: Optional[str] = None
    text: Optional[str] = None
    fields: List[SlackField] = field(default_factory=list)
    image_url: Optional[str] = None
    thumb_url: Optional[str] = None
    footer: Optional[str] = None
    footer_icon: Optional[str] = None
    timestamp: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为 Slack attachment 格式"""
        result = {"color": self.color}
        
        if self.pretext:
            result["pretext"] = self.pretext
        if self.author_name:
            result["author_name"] = self.author_name
        if self.author_link:
            result["author_link"] = self.author_link
        if self.author_icon:
            result["author_icon"] = self.author_icon
        if self.title:
            result["title"] = self.title
        if self.title_link:
            result["title_link"] = self.title_link
        if self.text:
            result["text"] = self.text
        if self.fields:
            result["fields"] = [
                {"title": f.title, "value": f.value, "short": f.short}
                for f in self.fields
            ]
        if self.image_url:
            result["image_url"] = self.image_url
        if self.thumb_url:
            result["thumb_url"] = self.thumb_url
        if self.footer:
            result["footer"] = self.footer
        if self.footer_icon:
            result["footer_icon"] = self.footer_icon
        if self.timestamp:
            result["ts"] = self.timestamp
        
        return result


class SlackBlockBuilder:
    """Slack Block Kit 构建器"""
    
    def __init__(self):
        self.blocks: List[Dict[str, Any]] = []
    
    def add_header(self, text: str) -> 'SlackBlockBuilder':
        """添加标题块"""
        self.blocks.append({
            "type": BlockType.HEADER.value,
            "text": {
                "type": TextType.PLAIN.value,
                "text": text
            }
        })
        return self
    
    def add_section(self, text: str, fields: Optional[List[Dict]] = None) -> 'SlackBlockBuilder':
        """添加文本块"""
        block = {
            "type": BlockType.SECTION.value,
            "text": {
                "type": TextType.MARKDOWN.value,
                "text": text
            }
        }
        if fields:
            block["fields"] = fields
        self.blocks.append(block)
        return self
    
    def add_divider(self) -> 'SlackBlockBuilder':
        """添加分隔线"""
        self.blocks.append({"type": BlockType.DIVIDER.value})
        return self
    
    def add_image(self, image_url: str, alt_text: str, title: Optional[str] = None) -> 'SlackBlockBuilder':
        """添加图片块"""
        block = {
            "type": BlockType.IMAGE.value,
            "image_url": image_url,
            "alt_text": alt_text
        }
        if title:
            block["title"] = {"type": TextType.PLAIN.value, "text": title}
        self.blocks.append(block)
        return self
    
    def add_context(self, elements: List[Dict[str, Any]]) -> 'SlackBlockBuilder':
        """添加上下文块"""
        self.blocks.append({
            "type": BlockType.CONTEXT.value,
            "elements": elements
        })
        return self
    
    def add_actions(self, elements: List[Dict[str, Any]]) -> 'SlackBlockBuilder':
        """添加操作按钮"""
        self.blocks.append({
            "type": BlockType.ACTIONS.value,
            "elements": elements
        })
        return self
    
    def build(self) -> List[Dict[str, Any]]:
        """构建 blocks 列表"""
        return self.blocks


class SlackNotifier:
    """
    Slack 通知器
    
    功能特性:
    - 支持 Incoming Webhook 和 Bot Token
    - 富文本格式 (Block Kit)
    - 附件上传
    - 线程回复
    - 频道管理
    - 消息更新/删除
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config = self._load_config(config_path)
        self.webhook_url = self.config.get("slack", {}).get("webhook_url")
        self.bot_token = self.config.get("slack", {}).get("bot_token")
        self.default_channel = self.config.get("slack", {}).get("default_channel", "#general")
        self.username = self.config.get("slack", {}).get("username", "Notification Bot")
        self.icon_emoji = self.config.get("slack", {}).get("icon_emoji", ":bell:")
        
        self._session: Optional[aiohttp.ClientSession] = None
        self._message_cache: Dict[str, Dict] = {}  # 缓存已发送消息
    
    def _load_config(self, config_path: Optional[Path]) -> Dict[str, Any]:
        """加载配置"""
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """获取或创建 HTTP session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self._session
    
    async def send_message(
        self,
        text: str,
        channel: Optional[str] = None,
        blocks: Optional[List[Dict]] = None,
        attachments: Optional[List[SlackAttachment]] = None,
        thread_ts: Optional[str] = None,
        unfurl_links: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送消息到 Slack
        
        Args:
            text: 消息文本 (备用纯文本)
            channel: 目标频道，默认使用配置
            blocks: Block Kit blocks
            attachments: 传统附件
            thread_ts: 回复线程的时间戳
            unfurl_links: 是否展开链接预览
            
        Returns:
            发送结果，包含消息ID和时间戳
        """
        if not self.webhook_url and not self.bot_token:
            raise ValueError("必须配置 webhook_url 或 bot_token")
        
        payload = {
            "text": text,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "unfurl_links": unfurl_links
        }
        
        if channel:
            payload["channel"] = channel
        
        if blocks:
            payload["blocks"] = blocks
        
        if attachments:
            payload["attachments"] = [a.to_dict() for a in attachments]
        
        if thread_ts:
            payload["thread_ts"] = thread_ts
        
        payload.update(kwargs)
        
        # 使用 Webhook 发送
        if self.webhook_url:
            return await self._send_via_webhook(payload)
        else:
            return await self._send_via_api(payload)
    
    async def _send_via_webhook(self, payload: Dict) -> Dict[str, Any]:
        """通过 Incoming Webhook 发送"""
        session = await self._get_session()
        
        try:
            async with session.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = {"success": True, "status": response.status}
                    # Webhook 不返回消息ID，生成一个追踪ID
                    result["message_id"] = f"webhook_{datetime.now().timestamp()}"
                    logger.info(f"Slack 消息发送成功")
                    return result
                else:
                    text = await response.text()
                    raise Exception(f"Slack API 错误: {response.status} - {text}")
                    
        except Exception as e:
            logger.error(f"发送 Slack 消息失败: {e}")
            raise
    
    async def _send_via_api(self, payload: Dict) -> Dict[str, Any]:
        """通过 Bot Token API 发送"""
        session = await self._get_session()
        
        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        try:
            async with session.post(
                "https://slack.com/api/chat.postMessage",
                json=payload,
                headers=headers
            ) as response:
                data = await response.json()
                
                if data.get("ok"):
                    result = {
                        "success": True,
                        "message_id": data.get("ts"),
                        "channel": data.get("channel")
                    }
                    # 缓存消息信息用于后续回复
                    self._message_cache[data.get("ts")] = result
                    logger.info(f"Slack 消息发送成功: {data.get('ts')}")
                    return result
                else:
                    raise Exception(f"Slack API 错误: {data.get('error')}")
                    
        except Exception as e:
            logger.error(f"发送 Slack 消息失败: {e}")
            raise
    
    async def reply_in_thread(
        self,
        thread_ts: str,
        text: str,
        channel: Optional[str] = None,
        blocks: Optional[List[Dict]] = None,
        broadcast: bool = False
    ) -> Dict[str, Any]:
        """
        在线程中回复
        
        Args:
            thread_ts: 父消息时间戳
            text: 回复内容
            channel: 频道
            blocks: Block Kit blocks
            broadcast: 是否广播到频道
        """
        return await self.send_message(
            text=text,
            channel=channel,
            blocks=blocks,
            thread_ts=thread_ts,
            reply_broadcast=broadcast
        )
    
    async def update_message(
        self,
        channel: str,
        timestamp: str,
        text: str,
        blocks: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """更新已发送的消息"""
        if not self.bot_token:
            raise ValueError("更新消息需要 bot_token")
        
        payload = {
            "channel": channel,
            "ts": timestamp,
            "text": text
        }
        
        if blocks:
            payload["blocks"] = blocks
        
        session = await self._get_session()
        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        async with session.post(
            "https://slack.com/api/chat.update",
            json=payload,
            headers=headers
        ) as response:
            data = await response.json()
            if data.get("ok"):
                return {"success": True, "timestamp": timestamp}
            else:
                raise Exception(f"更新消息失败: {data.get('error')}")
    
    async def delete_message(self, channel: str, timestamp: str) -> bool:
        """删除消息"""
        if not self.bot_token:
            raise ValueError("删除消息需要 bot_token")
        
        payload = {"channel": channel, "ts": timestamp}
        
        session = await self._get_session()
        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        async with session.post(
            "https://slack.com/api/chat.delete",
            json=payload,
            headers=headers
        ) as response:
            data = await response.json()
            return data.get("ok", False)
    
    async def upload_file(
        self,
        file_path: Union[str, Path],
        channels: Optional[List[str]] = None,
        title: Optional[str] = None,
        initial_comment: Optional[str] = None,
        thread_ts: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        上传文件到 Slack
        
        Args:
            file_path: 文件路径
            channels: 目标频道列表
            title: 文件标题
            initial_comment: 初始评论
            thread_ts: 回复到指定线程
        """
        if not self.bot_token:
            raise ValueError("上传文件需要 bot_token")
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        session = await self._get_session()
        
        data = aiohttp.FormData()
        data.add_field("file", open(file_path, "rb"))
        data.add_field("channels", ",".join(channels or [self.default_channel]))
        
        if title:
            data.add_field("title", title)
        if initial_comment:
            data.add_field("initial_comment", initial_comment)
        if thread_ts:
            data.add_field("thread_ts", thread_ts)
        
        headers = {"Authorization": f"Bearer {self.bot_token}"}
        
        async with session.post(
            "https://slack.com/api/files.upload",
            data=data,
            headers=headers
        ) as response:
            data = await response.json()
            if data.get("ok"):
                return {
                    "success": True,
                    "file_id": data.get("file", {}).get("id"),
                    "permalink": data.get("file", {}).get("permalink")
                }
            else:
                raise Exception(f"上传文件失败: {data.get('error')}")
    
    async def get_channel_list(self) -> List[Dict[str, Any]]:
        """获取频道列表"""
        if not self.bot_token:
            raise ValueError("获取频道列表需要 bot_token")
        
        session = await self._get_session()
        headers = {"Authorization": f"Bearer {self.bot_token}"}
        
        channels = []
        cursor = None
        
        while True:
            params = {"types": "public_channel,private_channel", "limit": 200}
            if cursor:
                params["cursor"] = cursor
            
            async with session.get(
                "https://slack.com/api/conversations.list",
                params=params,
                headers=headers
            ) as response:
                data = await response.json()
                if data.get("ok"):
                    channels.extend(data.get("channels", []))
                    cursor = data.get("response_metadata", {}).get("next_cursor")
                    if not cursor:
                        break
                else:
                    raise Exception(f"获取频道列表失败: {data.get('error')}")
        
        return channels
    
    async def close(self):
        """关闭连接"""
        if self._session and not self._session.closed:
            await self._session.close()


# 便捷函数
async def send_alert(
    title: str,
    message: str,
    severity: str = "warning",
    channel: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """快速发送告警通知"""
    notifier = SlackNotifier()
    
    # 根据严重程度选择颜色
    colors = {
        "critical": "#FF0000",
        "error": "#FF4444",
        "warning": "#FFA500",
        "info": "#36a64f"
    }
    
    attachment = SlackAttachment(
        color=colors.get(severity, "#36a64f"),
        title=title,
        text=message,
        footer="Notification System",
        timestamp=int(datetime.now().timestamp())
    )
    
    try:
        result = await notifier.send_message(
            text=f"{title}: {message}",
            channel=channel,
            attachments=[attachment],
            **kwargs
        )
        return result
    finally:
        await notifier.close()


async def send_deployment_notification(
    project: str,
    version: str,
    environment: str,
    status: str,
    details: Optional[Dict] = None,
    channel: Optional[str] = None
) -> Dict[str, Any]:
    """发送部署通知"""
    notifier = SlackNotifier()
    
    status_emoji = {
        "success": "✅",
        "failed": "❌",
        "started": "🚀",
        "rolling_back": "⏮️"
    }
    
    status_colors = {
        "success": "#36a64f",
        "failed": "#FF0000",
        "started": "#FFA500",
        "rolling_back": "#FFD700"
    }
    
    emoji = status_emoji.get(status, "📦")
    color = status_colors.get(status, "#36a64f")
    
    builder = SlackBlockBuilder()
    builder.add_header(f"{emoji} 部署 {status.upper()} - {project}")
    builder.add_section(
        f"*项目:* {project}\n"
        f"*版本:* `{version}`\n"
        f"*环境:* {environment}\n"
        f"*状态:* {status.upper()}\n"
        f"*时间:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    if details:
        builder.add_divider()
        details_text = "\n".join([f"*{k}:* `{v}`" for k, v in details.items()])
        builder.add_section(f"*详细信息:*\n{details_text}")
    
    try:
        result = await notifier.send_message(
            text=f"部署 {status}: {project} {version} to {environment}",
            channel=channel,
            blocks=builder.build()
        )
        return result
    finally:
        await notifier.close()


# 使用示例
async def example():
    """使用示例"""
    # 简单告警
    result = await send_alert(
        title="服务异常",
        message="API 响应时间超过阈值",
        severity="warning",
        channel="#alerts"
    )
    print(f"告警发送结果: {result}")
    
    # 部署通知
    result = await send_deployment_notification(
        project="api-gateway",
        version="v2.5.1",
        environment="production",
        status="success",
        details={"duration": "3m 42s", "deployer": "ci-cd"},
        channel="#deployments"
    )
    print(f"部署通知结果: {result}")


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 运行示例
    # asyncio.run(example())
    pass
