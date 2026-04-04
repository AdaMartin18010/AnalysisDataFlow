#!/usr/bin/env python3
"""
统一通知服务 (Unified Notification Service)

提供统一的异步通知接口，支持多渠道、优先级处理和消息模板管理。

作者: AnalysisDataFlow Team
日期: 2026-04-04
"""

import asyncio
import logging
import json
import hashlib
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field, asdict
from pathlib import Path
import yaml
import aiohttp

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Priority(Enum):
    """通知优先级枚举"""
    CRITICAL = 1    # 关键 - 立即发送，所有渠道
    HIGH = 2        # 高 - 快速发送，主要渠道
    MEDIUM = 3      # 中 - 正常处理
    LOW = 4         # 低 - 批量或延迟发送
    INFO = 5        # 信息 - 仅记录


class ChannelType(Enum):
    """通知渠道类型"""
    SLACK = "slack"
    EMAIL = "email"
    WEBHOOK = "webhook"
    WECHAT = "wechat"
    DINGTALK = "dingtalk"
    FEISHU = "feishu"


@dataclass
class NotificationMessage:
    """通知消息数据类"""
    id: str = field(default_factory=lambda: hashlib.md5(
        str(datetime.now().timestamp()).encode()
    ).hexdigest()[:12])
    title: str = ""
    content: str = ""
    priority: Priority = Priority.MEDIUM
    channels: List[ChannelType] = field(default_factory=list)
    recipients: List[str] = field(default_factory=list)
    template_name: Optional[str] = None
    template_data: Dict[str, Any] = field(default_factory=dict)
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    scheduled_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['priority'] = self.priority.name
        data['channels'] = [c.value for c in self.channels]
        data['created_at'] = self.created_at.isoformat()
        if self.scheduled_at:
            data['scheduled_at'] = self.scheduled_at.isoformat()
        return data


@dataclass
class ChannelResult:
    """渠道发送结果"""
    channel: ChannelType
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
    response_time_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


class TemplateManager:
    """消息模板管理器"""
    
    def __init__(self, templates_dir: Optional[Path] = None):
        self.templates_dir = templates_dir or Path(__file__).parent / "templates"
        self.templates: Dict[str, Dict[str, Any]] = {}
        self._load_templates()
    
    def _load_templates(self):
        """加载模板配置"""
        config_path = Path(__file__).parent / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.templates = config.get('templates', {})
        
        # 加载内置模板
        self._load_builtin_templates()
    
    def _load_builtin_templates(self):
        """加载内置模板"""
        builtin_templates = {
            "alert_critical": {
                "title": "🚨 【关键告警】{service}",
                "content": """
**告警级别**: {priority}
**服务**: {service}
**时间**: {timestamp}
**详情**: {details}

请立即处理！
""",
                "channels": ["slack", "email", "wechat"]
            },
            "alert_warning": {
                "title": "⚠️ 【警告】{service}",
                "content": """
**级别**: {priority}
**服务**: {service}
**时间**: {timestamp}
**详情**: {details}
""",
                "channels": ["slack", "email"]
            },
            "deployment_success": {
                "title": "✅ 部署成功 - {project}",
                "content": """
**项目**: {project}
**版本**: {version}
**环境**: {environment}
**部署者**: {deployer}
**耗时**: {duration}
""",
                "channels": ["slack"]
            },
            "deployment_failure": {
                "title": "❌ 部署失败 - {project}",
                "content": """
**项目**: {project}
**版本**: {version}
**环境**: {environment}
**错误**: {error}
**日志**: {log_url}
""",
                "channels": ["slack", "email"]
            },
            "system_report": {
                "title": "📊 系统日报 - {date}",
                "content": """
**日期**: {date}
**服务状态**: {status}
**关键指标**:
{metrics}

**待处理事项**:
{todos}
""",
                "channels": ["email"]
            }
        }
        
        for name, template in builtin_templates.items():
            if name not in self.templates:
                self.templates[name] = template
    
    def render(self, template_name: str, data: Dict[str, Any]) -> Dict[str, str]:
        """渲染模板"""
        if template_name not in self.templates:
            logger.warning(f"模板 '{template_name}' 不存在，使用默认模板")
            return {
                "title": data.get("title", "通知"),
                "content": data.get("content", str(data)),
                "channels": []
            }
        
        template = self.templates[template_name]
        return {
            "title": template["title"].format(**data),
            "content": template["content"].format(**data),
            "channels": template.get("channels", [])
        }
    
    def list_templates(self) -> List[str]:
        """列出所有可用模板"""
        return list(self.templates.keys())


class NotificationService:
    """
    统一通知服务
    
    核心功能:
    - 多渠道异步发送
    - 优先级队列管理
    - 消息模板渲染
    - 重试机制
    - 发送状态追踪
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path(__file__).parent / "config.yaml"
        self.config = self._load_config()
        self.template_manager = TemplateManager()
        
        # 渠道处理器映射
        self.channel_handlers: Dict[ChannelType, Callable] = {}
        
        # 优先级队列
        self.queues: Dict[Priority, asyncio.Queue] = {
            Priority.CRITICAL: asyncio.Queue(),
            Priority.HIGH: asyncio.Queue(),
            Priority.MEDIUM: asyncio.Queue(),
            Priority.LOW: asyncio.Queue(),
            Priority.INFO: asyncio.Queue()
        }
        
        # 统计信息
        self.stats = {
            "sent": 0,
            "failed": 0,
            "retried": 0,
            "dropped": 0
        }
        
        # 运行状态
        self._running = False
        self._workers: List[asyncio.Task] = []
        
        logger.info("通知服务初始化完成")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def register_channel_handler(
        self, 
        channel_type: ChannelType, 
        handler: Callable[[NotificationMessage], asyncio.Coroutine]
    ):
        """注册渠道处理器"""
        self.channel_handlers[channel_type] = handler
        logger.info(f"已注册渠道处理器: {channel_type.value}")
    
    async def send(
        self,
        title: str,
        content: str,
        priority: Priority = Priority.MEDIUM,
        channels: Optional[List[ChannelType]] = None,
        recipients: Optional[List[str]] = None,
        template_name: Optional[str] = None,
        template_data: Optional[Dict[str, Any]] = None,
        attachments: Optional[List[Dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送通知
        
        Args:
            title: 通知标题
            content: 通知内容
            priority: 优先级
            channels: 指定渠道，None则使用配置默认
            recipients: 接收人列表
            template_name: 模板名称
            template_data: 模板数据
            attachments: 附件列表
            
        Returns:
            发送结果字典
        """
        # 如果使用模板
        if template_name:
            rendered = self.template_manager.render(
                template_name, 
                template_data or {}
            )
            title = rendered["title"]
            content = rendered["content"]
            if not channels and rendered["channels"]:
                channels = [ChannelType(c) for c in rendered["channels"]]
        
        # 构建消息
        message = NotificationMessage(
            title=title,
            content=content,
            priority=priority,
            channels=channels or self._get_default_channels(priority),
            recipients=recipients or [],
            template_name=template_name,
            template_data=template_data or {},
            attachments=attachments or [],
            metadata=kwargs
        )
        
        # 根据优先级处理
        if priority == Priority.CRITICAL:
            # 关键消息立即发送
            return await self._process_message(message)
        else:
            # 其他消息入队
            await self.queues[priority].put(message)
            logger.debug(f"消息 {message.id} 已加入 {priority.name} 队列")
            return {"message_id": message.id, "status": "queued"}
    
    async def _process_message(
        self, 
        message: NotificationMessage
    ) -> Dict[str, Any]:
        """处理消息发送"""
        results = []
        
        for channel in message.channels:
            if channel not in self.channel_handlers:
                logger.warning(f"未注册渠道处理器: {channel.value}")
                continue
            
            result = await self._send_to_channel(message, channel)
            results.append(asdict(result))
        
        # 更新统计
        success_count = sum(1 for r in results if r["success"])
        if success_count > 0:
            self.stats["sent"] += 1
        else:
            self.stats["failed"] += 1
        
        return {
            "message_id": message.id,
            "success": success_count > 0,
            "channel_results": results
        }
    
    async def _send_to_channel(
        self, 
        message: NotificationMessage, 
        channel: ChannelType
    ) -> ChannelResult:
        """发送到指定渠道，带重试机制"""
        handler = self.channel_handlers[channel]
        start_time = asyncio.get_event_loop().time()
        
        for attempt in range(message.max_retries + 1):
            try:
                result = await handler(message)
                elapsed = (asyncio.get_event_loop().time() - start_time) * 1000
                
                return ChannelResult(
                    channel=channel,
                    success=True,
                    message_id=result.get("message_id"),
                    response_time_ms=elapsed
                )
                
            except Exception as e:
                logger.warning(
                    f"发送失败 (尝试 {attempt + 1}/{message.max_retries + 1}): {e}"
                )
                if attempt < message.max_retries:
                    self.stats["retried"] += 1
                    await asyncio.sleep(2 ** attempt)  # 指数退避
                else:
                    elapsed = (asyncio.get_event_loop().time() - start_time) * 1000
                    return ChannelResult(
                        channel=channel,
                        success=False,
                        error=str(e),
                        response_time_ms=elapsed
                    )
        
        return ChannelResult(channel=channel, success=False, error="Max retries exceeded")
    
    def _get_default_channels(self, priority: Priority) -> List[ChannelType]:
        """获取默认渠道配置"""
        rules = self.config.get("rules", {})
        
        if priority == Priority.CRITICAL:
            return [ChannelType.SLACK, ChannelType.EMAIL, ChannelType.WEBHOOK]
        elif priority == Priority.HIGH:
            return [ChannelType.SLACK, ChannelType.EMAIL]
        elif priority == Priority.MEDIUM:
            return [ChannelType.SLACK]
        else:
            return [ChannelType.EMAIL]
    
    async def start(self):
        """启动通知服务"""
        if self._running:
            return
        
        self._running = True
        
        # 为每个优先级启动工作线程
        for priority in [Priority.LOW, Priority.MEDIUM, Priority.HIGH]:
            worker = asyncio.create_task(
                self._queue_worker(priority)
            )
            self._workers.append(worker)
        
        logger.info("通知服务已启动")
    
    async def stop(self):
        """停止通知服务"""
        self._running = False
        
        # 等待队列清空
        for priority in Priority:
            while not self.queues[priority].empty():
                await asyncio.sleep(0.1)
        
        # 取消工作线程
        for worker in self._workers:
            worker.cancel()
        
        self._workers = []
        logger.info("通知服务已停止")
    
    async def _queue_worker(self, priority: Priority):
        """队列工作线程"""
        queue = self.queues[priority]
        
        while self._running:
            try:
                message = await asyncio.wait_for(queue.get(), timeout=1.0)
                await self._process_message(message)
                queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"处理消息时出错: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self.stats,
            "queue_sizes": {
                p.name: self.queues[p].qsize() 
                for p in Priority
            }
        }


# 使用示例
async def example_usage():
    """使用示例"""
    service = NotificationService()
    
    # 注册示例处理器 (实际使用时应连接真实实现)
    async def dummy_handler(message: NotificationMessage) -> Dict:
        logger.info(f"[DUMMY] 发送消息: {message.title}")
        return {"message_id": "dummy-123"}
    
    service.register_channel_handler(ChannelType.SLACK, dummy_handler)
    service.register_channel_handler(ChannelType.EMAIL, dummy_handler)
    
    # 启动服务
    await service.start()
    
    # 发送普通消息
    result = await service.send(
        title="测试通知",
        content="这是一条测试消息",
        priority=Priority.MEDIUM
    )
    print(f"发送结果: {result}")
    
    # 使用模板发送
    result = await service.send(
        template_name="alert_critical",
        template_data={
            "service": "api-gateway",
            "priority": "CRITICAL",
            "timestamp": datetime.now().isoformat(),
            "details": "CPU使用率超过95%"
        },
        priority=Priority.CRITICAL
    )
    print(f"模板发送结果: {result}")
    
    # 查看统计
    print(f"统计信息: {service.get_stats()}")
    
    # 停止服务
    await asyncio.sleep(2)
    await service.stop()


if __name__ == "__main__":
    asyncio.run(example_usage())
