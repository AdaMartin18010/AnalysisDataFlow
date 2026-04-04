#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink 测试数据生成器
用途: 生成各种测试数据集用于 Flink 作业的集成测试和性能测试
支持: Kafka, Socket, File, Kinesis 等多种输出
"""

import json
import random
import string
import time
import argparse
import asyncio
import aiohttp
import aiokafka
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
import threading


# =============================================================================
# 数据模型定义
# =============================================================================

@dataclass
class UserEvent:
    """用户行为事件"""
    user_id: str
    event_type: str  # click, view, purchase, logout
    timestamp: int
    page_id: str
    session_id: str
    device_type: str  # mobile, desktop, tablet
    ip_address: str
    user_agent: str
    referrer: str
    
    def to_json(self) -> str:
        return json.dumps(asdict(self))


@dataclass
class Transaction:
    """交易数据"""
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    merchant_id: str
    timestamp: int
    status: str  # pending, completed, failed
    payment_method: str
    location: Dict[str, float]  # lat, lon
    
    def to_json(self) -> str:
        return json.dumps(asdict(self))


@dataclass
class SensorReading:
    """传感器读数"""
    sensor_id: str
    device_type: str
    reading_type: str  # temperature, humidity, pressure
    value: float
    unit: str
    timestamp: int
    location: str
    battery_level: float
    
    def to_json(self) -> str:
        return json.dumps(asdict(self))


@dataclass
class LogEntry:
    """日志条目"""
    level: str  # DEBUG, INFO, WARN, ERROR
    service: str
    message: str
    timestamp: int
    trace_id: str
    span_id: str
    thread: str
    class_name: str
    method: str
    line: int
    
    def to_json(self) -> str:
        return json.dumps(asdict(self))


# =============================================================================
# 数据生成器基类
# =============================================================================

class DataGenerator:
    """数据生成器基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.running = False
        self.stats = {
            'generated': 0,
            'sent': 0,
            'errors': 0
        }
    
    def generate_user_id(self) -> str:
        """生成用户ID"""
        return f"user_{random.randint(1, self.config.get('num_users', 10000))}"
    
    def generate_session_id(self) -> str:
        """生成会话ID"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
    
    def generate_ip(self) -> str:
        """生成随机IP地址"""
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    
    def generate_timestamp(self, max_delay_ms: int = 0) -> int:
        """生成时间戳"""
        base_time = int(time.time() * 1000)
        if max_delay_ms > 0:
            base_time -= random.randint(0, max_delay_ms)
        return base_time


# =============================================================================
# 具体数据生成器
# =============================================================================

class UserEventGenerator(DataGenerator):
    """用户事件生成器"""
    
    EVENT_TYPES = ['click', 'view', 'purchase', 'add_to_cart', 'search', 'logout']
    DEVICE_TYPES = ['mobile', 'desktop', 'tablet', 'smart_tv']
    PAGES = ['/home', '/product', '/cart', '/checkout', '/profile', '/search', '/category']
    REFERRERS = ['google', 'facebook', 'direct', 'email', 'twitter', 'bing']
    
    def generate(self) -> UserEvent:
        return UserEvent(
            user_id=self.generate_user_id(),
            event_type=random.choice(self.EVENT_TYPES),
            timestamp=self.generate_timestamp(max_delay_ms=5000),
            page_id=random.choice(self.PAGES),
            session_id=self.generate_session_id(),
            device_type=random.choice(self.DEVICE_TYPES),
            ip_address=self.generate_ip(),
            user_agent='Mozilla/5.0 (compatible; TestGenerator/1.0)',
            referrer=random.choice(self.REFERRERS)
        )


class TransactionGenerator(DataGenerator):
    """交易数据生成器"""
    
    CURRENCIES = ['USD', 'EUR', 'GBP', 'CNY', 'JPY']
    STATUSES = ['pending', 'completed', 'failed', 'refunded']
    PAYMENT_METHODS = ['credit_card', 'debit_card', 'paypal', 'apple_pay', 'google_pay']
    
    def generate(self) -> Transaction:
        cities = [
            {'lat': 40.7128, 'lon': -74.0060},   # NYC
            {'lat': 51.5074, 'lon': -0.1278},    # London
            {'lat': 48.8566, 'lon': 2.3522},     # Paris
            {'lat': 35.6762, 'lon': 139.6503},   # Tokyo
            {'lat': 39.9042, 'lon': 116.4074},   # Beijing
        ]
        
        return Transaction(
            transaction_id=''.join(random.choices(string.ascii_uppercase + string.digits, k=20)),
            user_id=self.generate_user_id(),
            amount=round(random.uniform(1.0, 1000.0), 2),
            currency=random.choice(self.CURRENCIES),
            merchant_id=f"merchant_{random.randint(1, 1000)}",
            timestamp=self.generate_timestamp(),
            status=random.choice(self.STATUSES),
            payment_method=random.choice(self.PAYMENT_METHODS),
            location=random.choice(cities)
        )


class SensorReadingGenerator(DataGenerator):
    """传感器读数生成器"""
    
    DEVICE_TYPES = ['thermostat', 'weather_station', 'industrial_sensor', 'smart_meter']
    READING_TYPES = [
        ('temperature', -20, 50, 'celsius'),
        ('humidity', 0, 100, 'percent'),
        ('pressure', 980, 1050, 'hpa'),
        ('light', 0, 100000, 'lux')
    ]
    LOCATIONS = ['warehouse_a', 'warehouse_b', 'office_floor_1', 'office_floor_2', 'outdoor']
    
    def generate(self) -> SensorReading:
        reading_type, min_val, max_val, unit = random.choice(self.READING_TYPES)
        
        return SensorReading(
            sensor_id=f"sensor_{random.randint(1, 5000)}",
            device_type=random.choice(self.DEVICE_TYPES),
            reading_type=reading_type,
            value=round(random.uniform(min_val, max_val), 2),
            unit=unit,
            timestamp=self.generate_timestamp(),
            location=random.choice(self.LOCATIONS),
            battery_level=round(random.uniform(0, 100), 1)
        )


class LogEntryGenerator(DataGenerator):
    """日志条目生成器"""
    
    LEVELS = ['DEBUG', 'INFO', 'WARN', 'ERROR']
    LEVEL_WEIGHTS = [30, 50, 15, 5]  # 日志级别分布权重
    SERVICES = ['auth-service', 'payment-service', 'inventory-service', 'user-service', 'api-gateway']
    MESSAGES = {
        'DEBUG': ['Processing request', 'Cache hit', 'Database query executed'],
        'INFO': ['User logged in', 'Order created', 'Payment processed', 'Email sent'],
        'WARN': ['Slow query detected', 'Rate limit approaching', 'Cache miss', 'Retry attempt'],
        'ERROR': ['Database connection failed', 'Payment declined', 'Timeout occurred', 'Invalid request']
    }
    
    def generate(self) -> LogEntry:
        level = random.choices(self.LEVELS, weights=self.LEVEL_WEIGHTS)[0]
        
        return LogEntry(
            level=level,
            service=random.choice(self.SERVICES),
            message=random.choice(self.MESSAGES[level]),
            timestamp=self.generate_timestamp(),
            trace_id=''.join(random.choices(string.hexdigits, k=32)),
            span_id=''.join(random.choices(string.hexdigits, k=16)),
            thread=f"pool-{random.randint(1, 10)}-thread-{random.randint(1, 10)}",
            class_name=f"com.example.service.{random.choice(self.SERVICES).replace('-', '.')}",
            method=random.choice(['process', 'handle', 'execute', 'validate']),
            line=random.randint(1, 500)
        )


# =============================================================================
# 数据发送器
# =============================================================================

class KafkaSender:
    """Kafka 数据发送器"""
    
    def __init__(self, bootstrap_servers: str, topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None
    
    async def connect(self):
        self.producer = aiokafka.AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: v.encode('utf-8'),
            compression_type='lz4'
        )
        await self.producer.start()
    
    async def send(self, message: str):
        await self.producer.send(self.topic, message)
    
    async def close(self):
        if self.producer:
            await self.producer.stop()


class SocketSender:
    """Socket 数据发送器"""
    
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = None
    
    async def connect(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        self.socket = writer
    
    async def send(self, message: str):
        if self.socket:
            self.socket.write((message + '\n').encode())
            await self.socket.drain()
    
    async def close(self):
        if self.socket:
            self.socket.close()
            await self.socket.wait_closed()


class FileSender:
    """文件数据发送器"""
    
    def __init__(self, filepath: str, rotate_size_mb: int = 100):
        self.filepath = filepath
        self.rotate_size_mb = rotate_size_mb
        self.file = None
        self.current_size = 0
        self.file_index = 0
    
    async def connect(self):
        self._open_file()
    
    def _open_file(self):
        if self.file:
            self.file.close()
        filepath = f"{self.filepath}.{self.file_index:04d}"
        self.file = open(filepath, 'w')
        self.current_size = 0
        self.file_index += 1
    
    async def send(self, message: str):
        line = message + '\n'
        self.file.write(line)
        self.current_size += len(line.encode())
        
        # 文件轮转
        if self.current_size > self.rotate_size_mb * 1024 * 1024:
            self._open_file()
    
    async def close(self):
        if self.file:
            self.file.close()


class HttpSender:
    """HTTP 数据发送器"""
    
    def __init__(self, endpoint: str, batch_size: int = 100):
        self.endpoint = endpoint
        self.batch_size = batch_size
        self.batch = []
        self.session = None
    
    async def connect(self):
        self.session = aiohttp.ClientSession()
    
    async def send(self, message: str):
        self.batch.append(message)
        if len(self.batch) >= self.batch_size:
            await self._flush()
    
    async def _flush(self):
        if not self.batch:
            return
        payload = '\n'.join(self.batch)
        async with self.session.post(self.endpoint, data=payload) as response:
            if response.status != 200:
                print(f"HTTP send failed: {response.status}")
        self.batch = []
    
    async def close(self):
        await self._flush()
        if self.session:
            await self.session.close()


# =============================================================================
# 主控制器
# =============================================================================

class TestDataGenerator:
    """测试数据生成主控制器"""
    
    GENERATORS = {
        'user_event': UserEventGenerator,
        'transaction': TransactionGenerator,
        'sensor': SensorReadingGenerator,
        'log': LogEntryGenerator
    }
    
    SENDERS = {
        'kafka': KafkaSender,
        'socket': SocketSender,
        'file': FileSender,
        'http': HttpSender
    }
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.generator = None
        self.sender = None
        self.running = False
        self.stats = {
            'generated': 0,
            'sent': 0,
            'errors': 0,
            'start_time': None
        }
    
    async def initialize(self):
        """初始化生成器和发送器"""
        # 创建数据生成器
        generator_class = self.GENERATORS.get(self.config['data_type'])
        if not generator_class:
            raise ValueError(f"Unknown data type: {self.config['data_type']}")
        self.generator = generator_class(self.config)
        
        # 创建发送器
        output_type = self.config['output']['type']
        sender_class = self.SENDERS.get(output_type)
        if not sender_class:
            raise ValueError(f"Unknown output type: {output_type}")
        
        if output_type == 'kafka':
            self.sender = sender_class(
                self.config['output']['bootstrap_servers'],
                self.config['output']['topic']
            )
        elif output_type == 'socket':
            self.sender = sender_class(
                self.config['output']['host'],
                self.config['output']['port']
            )
        elif output_type == 'file':
            self.sender = sender_class(
                self.config['output']['filepath'],
                self.config['output'].get('rotate_size_mb', 100)
            )
        elif output_type == 'http':
            self.sender = sender_class(
                self.config['output']['endpoint'],
                self.config['output'].get('batch_size', 100)
            )
        
        await self.sender.connect()
        print(f"Initialized: {self.config['data_type']} -> {output_type}")
    
    async def run(self):
        """主运行循环"""
        self.running = True
        self.stats['start_time'] = time.time()
        
        rate = self.config.get('rate', 1000)  # 每秒消息数
        interval = 1.0 / rate
        
        print(f"Starting generator at {rate} msg/s")
        
        last_report = time.time()
        report_interval = 10  # 每 10 秒报告一次
        
        while self.running:
            try:
                # 生成数据
                data = self.generator.generate()
                message = data.to_json()
                self.stats['generated'] += 1
                
                # 发送数据
                await self.sender.send(message)
                self.stats['sent'] += 1
                
                # 控制速率
                await asyncio.sleep(interval)
                
                # 统计报告
                now = time.time()
                if now - last_report >= report_interval:
                    self._print_stats()
                    last_report = now
                
            except Exception as e:
                self.stats['errors'] += 1
                print(f"Error: {e}")
                if self.config.get('stop_on_error'):
                    break
    
    def _print_stats(self):
        """打印统计信息"""
        elapsed = time.time() - self.stats['start_time']
        rate = self.stats['sent'] / elapsed if elapsed > 0 else 0
        print(f"[{elapsed:.1f}s] Generated: {self.stats['generated']}, "
              f"Sent: {self.stats['sent']}, Errors: {self.stats['errors']}, "
              f"Rate: {rate:.1f} msg/s")
    
    def stop(self):
        """停止生成器"""
        self.running = False
    
    async def cleanup(self):
        """清理资源"""
        if self.sender:
            await self.sender.close()
        self._print_stats()


# =============================================================================
# 命令行接口
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Flink Test Data Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # Kafka 输出 - 用户事件
  python test-data-generator.py --type user_event --output kafka \\
      --kafka-bootstrap localhost:9092 --topic user-events --rate 1000
  
  # 文件输出 - 传感器数据
  python test-data-generator.py --type sensor --output file \\
      --filepath /tmp/sensor_data --rate 500
  
  # Socket 输出 - 日志数据
  python test-data-generator.py --type log --output socket \\
      --host localhost --port 9999 --rate 2000
        """
    )
    
    # 数据类型
    parser.add_argument('--type', required=True,
                       choices=['user_event', 'transaction', 'sensor', 'log'],
                       help='数据类型')
    
    # 输出配置
    parser.add_argument('--output', required=True,
                       choices=['kafka', 'socket', 'file', 'http'],
                       help='输出类型')
    
    # Kafka 参数
    parser.add_argument('--kafka-bootstrap', default='localhost:9092',
                       help='Kafka bootstrap servers')
    parser.add_argument('--topic', default='test-topic',
                       help='Kafka topic')
    
    # Socket 参数
    parser.add_argument('--host', default='localhost',
                       help='Target host')
    parser.add_argument('--port', type=int, default=9999,
                       help='Target port')
    
    # 文件参数
    parser.add_argument('--filepath', default='/tmp/flink_test_data',
                       help='Output file path')
    parser.add_argument('--rotate-size', type=int, default=100,
                       help='File rotation size (MB)')
    
    # HTTP 参数
    parser.add_argument('--endpoint', default='http://localhost:8080/api/events',
                       help='HTTP endpoint')
    parser.add_argument('--batch-size', type=int, default=100,
                       help='HTTP batch size')
    
    # 通用参数
    parser.add_argument('--rate', type=int, default=1000,
                       help='Messages per second')
    parser.add_argument('--num-users', type=int, default=10000,
                       help='Number of unique users')
    parser.add_argument('--duration', type=int, default=0,
                       help='Duration in seconds (0 = infinite)')
    parser.add_argument('--stop-on-error', action='store_true',
                       help='Stop on first error')
    
    args = parser.parse_args()
    
    # 构建配置
    config = {
        'data_type': args.type,
        'rate': args.rate,
        'num_users': args.num_users,
        'stop_on_error': args.stop_on_error,
        'output': {
            'type': args.output
        }
    }
    
    # 根据输出类型添加特定配置
    if args.output == 'kafka':
        config['output'].update({
            'bootstrap_servers': args.kafka_bootstrap,
            'topic': args.topic
        })
    elif args.output == 'socket':
        config['output'].update({
            'host': args.host,
            'port': args.port
        })
    elif args.output == 'file':
        config['output'].update({
            'filepath': args.filepath,
            'rotate_size_mb': args.rotate_size
        })
    elif args.output == 'http':
        config['output'].update({
            'endpoint': args.endpoint,
            'batch_size': args.batch_size
        })
    
    # 创建并运行生成器
    generator = TestDataGenerator(config)
    
    async def run_with_timeout():
        await generator.initialize()
        
        if args.duration > 0:
            # 设置超时
            await asyncio.wait_for(generator.run(), timeout=args.duration)
        else:
            # 无限运行直到 Ctrl+C
            try:
                await generator.run()
            except KeyboardInterrupt:
                print("\nStopping generator...")
                generator.stop()
        
        await generator.cleanup()
    
    try:
        asyncio.run(run_with_timeout())
    except asyncio.TimeoutError:
        print("\nDuration reached, stopping generator...")
        generator.stop()
        asyncio.run(generator.cleanup())


if __name__ == '__main__':
    main()

# =============================================================================
# 安装依赖:
#   pip install aiokafka aiohttp
#
# 功能特性:
# - 支持多种数据类型 (用户事件、交易、传感器、日志)
# - 支持多种输出 (Kafka、Socket、文件、HTTP)
# - 可控的生成速率
# - 实时统计报告
# - 异步高性能实现
# - 支持文件轮转
# - 支持批量发送
# =============================================================================
