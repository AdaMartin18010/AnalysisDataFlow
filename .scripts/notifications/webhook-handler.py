#!/usr/bin/env python3
"""
Webhook 处理器 (Webhook Handler)

支持通用 Webhook、企业微信、钉钉、飞书等多种企业IM平台。

作者: AnalysisDataFlow Team
日期: 2026-04-04
"""

import asyncio
import json
import logging
import hashlib
import hmac
import base64
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from urllib.parse import urlencode

import aiohttp
import yaml

logger = logging.getLogger(__name__)


class WebhookPlatform(Enum):
    """Webhook 平台类型"""
    GENERIC = "generic"
    WECHAT_WORK = "wechat_work"  # 企业微信
    DINGTALK = "dingtalk"        # 钉钉
    FEISHU = "feishu"            # 飞书
    LARK = "lark"                # Lark (飞书国际版)


@dataclass
class WebhookMessage:
    """Webhook 消息"""
    content: str
    title: Optional[str] = None
    msg_type: str = "text"  # text, markdown, image, news, template_card
    at_users: List[str] = field(default_factory=list)
    at_mobiles: List[str] = field(default_factory=list)
    is_at_all: bool = False
    extras: Dict[str, Any] = field(default_factory=dict)


class BaseWebhookHandler:
    """Webhook 处理器基类"""
    
    def __init__(self, webhook_url: str, secret: Optional[str] = None):
        self.webhook_url = webhook_url
        self.secret = secret
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """获取或创建 HTTP session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self._session
    
    async def send(self, message: WebhookMessage) -> Dict[str, Any]:
        """发送消息 - 子类实现"""
        raise NotImplementedError
    
    async def close(self):
        """关闭连接"""
        if self._session and not self._session.closed:
            await self._session.close()


class WechatWorkHandler(BaseWebhookHandler):
    """
    企业微信 Webhook 处理器
    
    支持消息类型:
    - text: 文本消息
    - markdown: Markdown 消息
    - image: 图片消息
    - news: 图文消息
    - template_card: 模板卡片
    """
    
    def _generate_signature(self) -> Dict[str, str]:
        """生成企业微信签名"""
        if not self.secret:
            return {}
        
        timestamp = str(int(time.time()))
        string_to_sign = f"{timestamp}\n{self.secret}"
        
        hmac_code = hmac.new(
            self.secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        
        signature = base64.b64encode(hmac_code).decode('utf-8')
        
        return {
            "timestamp": timestamp,
            "sign": signature
        }
    
    async def send(self, message: WebhookMessage) -> Dict[str, Any]:
        """发送企业微信消息"""
        session = await self._get_session()
        
        # 构建消息体
        payload = self._build_payload(message)
        
        # 添加签名
        params = self._generate_signature()
        url = f"{self.webhook_url}?{urlencode(params)}" if params else self.webhook_url
        
        try:
            async with session.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                data = await response.json()
                
                if data.get("errcode") == 0:
                    logger.info("企业微信消息发送成功")
                    return {"success": True, "message_id": data.get("msgid")}
                else:
                    raise Exception(f"企业微信 API 错误: {data.get('errmsg')}")
                    
        except Exception as e:
            logger.error(f"企业微信发送失败: {e}")
            raise
    
    def _build_payload(self, message: WebhookMessage) -> Dict[str, Any]:
        """构建消息载荷"""
        msg_type = message.msg_type
        
        if msg_type == "text":
            payload = {
                "msgtype": "text",
                "text": {"content": message.content}
            }
            # 添加 @ 功能
            if message.at_users or message.at_mobiles or message.is_at_all:
                payload["text"]["mentioned_list"] = message.at_users
                payload["text"]["mentioned_mobile_list"] = message.at_mobiles
        
        elif msg_type == "markdown":
            payload = {
                "msgtype": "markdown",
                "markdown": {"content": message.content}
            }
        
        elif msg_type == "image":
            # 图片需要先转为 base64
            payload = {
                "msgtype": "image",
                "image": message.extras.get("image", {})
            }
        
        elif msg_type == "news":
            payload = {
                "msgtype": "news",
                "news": {
                    "articles": message.extras.get("articles", [])
                }
            }
        
        elif msg_type == "template_card":
            payload = {
                "msgtype": "template_card",
                "template_card": message.extras.get("card", {})
            }
        
        else:
            raise ValueError(f"不支持的消息类型: {msg_type}")
        
        return payload


class DingTalkHandler(BaseWebhookHandler):
    """
    钉钉 Webhook 处理器
    
    支持消息类型:
    - text: 文本
    - link: 链接
    - markdown: Markdown
    - actionCard: 整体跳转 ActionCard
    - feedCard: 独立跳转 ActionCard
    """
    
    def _generate_signature(self) -> Dict[str, str]:
        """生成钉钉签名"""
        if not self.secret:
            return {}
        
        timestamp = str(round(time.time() * 1000))
        string_to_sign = f"{timestamp}\n{self.secret}"
        
        hmac_code = hmac.new(
            self.secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        
        sign = base64.b64encode(hmac_code).decode('utf-8')
        
        return {
            "timestamp": timestamp,
            "sign": sign
        }
    
    async def send(self, message: WebhookMessage) -> Dict[str, Any]:
        """发送钉钉消息"""
        session = await self._get_session()
        
        payload = self._build_payload(message)
        
        # 添加签名
        params = self._generate_signature()
        url = f"{self.webhook_url}&{urlencode(params)}" if params else self.webhook_url
        
        try:
            async with session.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                data = await response.json()
                
                if data.get("errcode") == 0:
                    logger.info("钉钉消息发送成功")
                    return {"success": True}
                else:
                    raise Exception(f"钉钉 API 错误: {data.get('errmsg')}")
                    
        except Exception as e:
            logger.error(f"钉钉发送失败: {e}")
            raise
    
    def _build_payload(self, message: WebhookMessage) -> Dict[str, Any]:
        """构建钉钉消息载荷"""
        msg_type = message.msg_type
        
        if msg_type == "text":
            payload = {
                "msgtype": "text",
                "text": {"content": message.content},
                "at": {
                    "atMobiles": message.at_mobiles,
                    "atUserIds": message.at_users,
                    "isAtAll": message.is_at_all
                }
            }
        
        elif msg_type == "markdown":
            payload = {
                "msgtype": "markdown",
                "markdown": {
                    "title": message.title or "通知",
                    "text": message.content
                },
                "at": {
                    "atMobiles": message.at_mobiles,
                    "atUserIds": message.at_users,
                    "isAtAll": message.is_at_all
                }
            }
        
        elif msg_type == "link":
            payload = {
                "msgtype": "link",
                "link": {
                    "text": message.content,
                    "title": message.title or "链接",
                    **message.extras.get("link", {})
                }
            }
        
        elif msg_type == "actionCard":
            payload = {
                "msgtype": "action_card",
                "action_card": message.extras.get("action_card", {})
            }
        
        elif msg_type == "feedCard":
            payload = {
                "msgtype": "feedCard",
                "feedCard": {
                    "links": message.extras.get("links", [])
                }
            }
        
        else:
            raise ValueError(f"不支持的消息类型: {msg_type}")
        
        return payload


class FeishuHandler(BaseWebhookHandler):
    """
    飞书/Lark Webhook 处理器
    
    支持消息类型:
    - text: 纯文本
    - rich_text: 富文本
    - post: 帖子
    - share_chat: 分享群名片
    - interactive: 交互式卡片
    """
    
    def _generate_signature(self) -> Dict[str, str]:
        """生成飞书签名"""
        if not self.secret:
            return {}
        
        timestamp = str(int(time.time()))
        string_to_sign = f"{timestamp}\n{self.secret}"
        
        hmac_code = hmac.new(
            string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        
        signature = base64.b64encode(hmac_code).decode('utf-8')
        
        return {
            "timestamp": timestamp,
            "sign": signature
        }
    
    async def send(self, message: WebhookMessage) -> Dict[str, Any]:
        """发送飞书消息"""
        session = await self._get_session()
        
        payload = self._build_payload(message)
        
        # 添加签名
        sign_data = self._generate_signature()
        if sign_data:
            payload["timestamp"] = sign_data["timestamp"]
            payload["sign"] = sign_data["sign"]
        
        try:
            async with session.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                data = await response.json()
                
                if data.get("code") == 0:
                    logger.info("飞书消息发送成功")
                    return {"success": True, "message_id": data.get("data", {}).get("message_id")}
                else:
                    raise Exception(f"飞书 API 错误: {data.get('msg')}")
                    
        except Exception as e:
            logger.error(f"飞书发送失败: {e}")
            raise
    
    def _build_payload(self, message: WebhookMessage) -> Dict[str, Any]:
        """构建飞书消息载荷"""
        msg_type = message.msg_type
        
        if msg_type == "text":
            payload = {
                "msg_type": "text",
                "content": {"text": message.content}
            }
        
        elif msg_type == "rich_text":
            payload = {
                "msg_type": "post",
                "content": {
                    "post": {
                        "zh_cn": {
                            "title": message.title or "",
                            "content": message.extras.get("content", [])
                        }
                    }
                }
            }
        
        elif msg_type == "interactive":
            payload = {
                "msg_type": "interactive",
                "card": message.extras.get("card", {})
            }
        
        elif msg_type == "share_chat":
            payload = {
                "msg_type": "share_chat",
                "content": {
                    "share_chat_id": message.extras.get("chat_id", "")
                }
            }
        
        else:
            raise ValueError(f"不支持的消息类型: {msg_type}")
        
        return payload


class GenericWebhookHandler(BaseWebhookHandler):
    """通用 Webhook 处理器"""
    
    def __init__(
        self, 
        webhook_url: str, 
        secret: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        auth_type: Optional[str] = None
    ):
        super().__init__(webhook_url, secret)
        self.headers = headers or {}
        self.auth_type = auth_type  # bearer, basic, hmac
    
    async def send(self, message: WebhookMessage) -> Dict[str, Any]:
        """发送通用 Webhook 消息"""
        session = await self._get_session()
        
        # 构建请求
        headers = dict(self.headers)
        headers["Content-Type"] = "application/json"
        
        # 添加认证
        if self.auth_type == "bearer" and self.secret:
            headers["Authorization"] = f"Bearer {self.secret}"
        elif self.auth_type == "basic" and self.secret:
            import base64
            encoded = base64.b64encode(self.secret.encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"
        elif self.auth_type == "hmac" and self.secret:
            timestamp = str(int(time.time()))
            signature = hmac.new(
                self.secret.encode(),
                timestamp.encode(),
                hashlib.sha256
            ).hexdigest()
            headers["X-Signature"] = signature
            headers["X-Timestamp"] = timestamp
        
        # 构建载荷
        payload = {
            "message": message.content,
            "title": message.title,
            "type": message.msg_type,
            "timestamp": datetime.now().isoformat(),
            **message.extras
        }
        
        try:
            async with session.post(
                self.webhook_url,
                json=payload,
                headers=headers
            ) as response:
                response_text = await response.text()
                
                if response.status < 400:
                    logger.info("Webhook 发送成功")
                    try:
                        data = json.loads(response_text)
                        return {"success": True, "response": data}
                    except:
                        return {"success": True, "response": response_text}
                else:
                    raise Exception(f"Webhook 错误: {response.status} - {response_text}")
                    
        except Exception as e:
            logger.error(f"Webhook 发送失败: {e}")
            raise


class WebhookManager:
    """
    Webhook 管理器
    
    统一管理多个 Webhook 渠道，支持自动路由和批量发送。
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config = self._load_config(config_path)
        self.handlers: Dict[str, BaseWebhookHandler] = {}
        self._init_handlers()
    
    def _load_config(self, config_path: Optional[Path]) -> Dict[str, Any]:
        """加载配置"""
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def _init_handlers(self):
        """初始化处理器"""
        webhooks = self.config.get("webhooks", {})
        
        for name, config in webhooks.items():
            platform = config.get("platform", "generic")
            url = config.get("url")
            secret = config.get("secret")
            
            if not url:
                continue
            
            handler_class = self._get_handler_class(platform)
            if handler_class == GenericWebhookHandler:
                self.handlers[name] = GenericWebhookHandler(
                    url, secret,
                    headers=config.get("headers"),
                    auth_type=config.get("auth_type")
                )
            else:
                self.handlers[name] = handler_class(url, secret)
            
            logger.info(f"初始化 Webhook 处理器: {name} ({platform})")
    
    def _get_handler_class(self, platform: str) -> type:
        """获取处理器类"""
        mapping = {
            "wechat_work": WechatWorkHandler,
            "dingtalk": DingTalkHandler,
            "feishu": FeishuHandler,
            "lark": FeishuHandler,
            "generic": GenericWebhookHandler
        }
        return mapping.get(platform, GenericWebhookHandler)
    
    async def send(
        self,
        handler_name: str,
        message: WebhookMessage
    ) -> Dict[str, Any]:
        """发送到指定处理器"""
        if handler_name not in self.handlers:
            raise ValueError(f"未知的 Webhook 处理器: {handler_name}")
        
        handler = self.handlers[handler_name]
        return await handler.send(message)
    
    async def broadcast(
        self,
        message: WebhookMessage,
        handler_names: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """广播消息到多个渠道"""
        targets = handler_names or list(self.handlers.keys())
        results = {}
        
        # 并行发送
        tasks = {
            name: asyncio.create_task(self.send(name, message))
            for name in targets if name in self.handlers
        }
        
        for name, task in tasks.items():
            try:
                results[name] = await task
            except Exception as e:
                results[name] = {"success": False, "error": str(e)}
        
        return results
    
    async def close(self):
        """关闭所有连接"""
        for handler in self.handlers.values():
            await handler.close()


# 便捷函数
async def send_wechat_work(
    webhook_url: str,
    content: str,
    secret: Optional[str] = None,
    msg_type: str = "text",
    **kwargs
) -> Dict[str, Any]:
    """快速发送企业微信消息"""
    handler = WechatWorkHandler(webhook_url, secret)
    message = WebhookMessage(content=content, msg_type=msg_type, extras=kwargs)
    try:
        return await handler.send(message)
    finally:
        await handler.close()


async def send_dingtalk(
    webhook_url: str,
    content: str,
    secret: Optional[str] = None,
    msg_type: str = "text",
    **kwargs
) -> Dict[str, Any]:
    """快速发送钉钉消息"""
    handler = DingTalkHandler(webhook_url, secret)
    message = WebhookMessage(content=content, msg_type=msg_type, extras=kwargs)
    try:
        return await handler.send(message)
    finally:
        await handler.close()


async def send_feishu(
    webhook_url: str,
    content: str,
    secret: Optional[str] = None,
    msg_type: str = "text",
    **kwargs
) -> Dict[str, Any]:
    """快速发送飞书消息"""
    handler = FeishuHandler(webhook_url, secret)
    message = WebhookMessage(content=content, msg_type=msg_type, extras=kwargs)
    try:
        return await handler.send(message)
    finally:
        await handler.close()


# 使用示例
async def example():
    """使用示例"""
    # 企业微信示例
    result = await send_wechat_work(
        webhook_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
        content="系统告警：CPU使用率超过90%",
        secret="your-secret",
        msg_type="markdown"
    )
    print(f"企业微信发送结果: {result}")
    
    # 钉钉示例
    result = await send_dingtalk(
        webhook_url="https://oapi.dingtalk.com/robot/send?access_token=xxx",
        content="## 部署通知\n\n项目部署成功！",
        secret="your-secret",
        msg_type="markdown"
    )
    print(f"钉钉发送结果: {result}")
    
    # 飞书示例
    result = await send_feishu(
        webhook_url="https://open.feishu.cn/open-apis/bot/v2/hook/xxx",
        content="测试消息",
        msg_type="text"
    )
    print(f"飞书发送结果: {result}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # asyncio.run(example())
    pass
