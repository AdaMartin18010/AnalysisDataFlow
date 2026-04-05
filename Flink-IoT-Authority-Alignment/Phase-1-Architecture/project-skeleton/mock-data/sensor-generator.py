#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink IoT 项目 - 传感器数据生成器
================================
生成模拟IoT传感器数据，支持：
- 100个设备的温度、压力、湿度数据
- 乱序数据模拟
- 批量数据上报
- Kafka和MQTT双通道输出

文档编号: F-GENERATOR-05
形式化等级: L4
创建时间: 2026-04-05
"""

import json
import random
import time
import uuid
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import threading
import signal

# 尝试导入外部库，如未安装则给出友好提示
try:
    from kafka import KafkaProducer
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False
    print("Warning: kafka-python not installed. Kafka output disabled.")

try:
    import paho.mqtt.client as mqtt
    MQTT_AVAILABLE = True
except ImportError:
    MQTT_AVAILABLE = False
    print("Warning: paho-mqtt not installed. MQTT output disabled.")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("Warning: numpy not installed. Using random module instead.")


class DeviceRegistry:
    """设备注册表管理"""
    
    def __init__(self, registry_file: str = "device-registry.json"):
        self.registry_file = registry_file
        self.devices = []
        self.device_types = {}
        self.locations = {}
        self.load_registry()
    
    def load_registry(self):
        """加载设备注册表"""
        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.devices = data.get('devices', [])
                self.device_types = {dt['type_id']: dt for dt in data.get('device_types', [])}
                self.locations = {loc['location_id']: loc for loc in data.get('locations', [])}
            print(f"✅ Loaded {len(self.devices)} devices from registry")
        except FileNotFoundError:
            print(f"⚠️ Registry file not found: {self.registry_file}")
            self._generate_default_devices()
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing registry: {e}")
            self._generate_default_devices()
    
    def _generate_default_devices(self):
        """生成默认设备列表（当注册表不存在时）"""
        device_types = ['TEMPERATURE_SENSOR', 'PRESSURE_SENSOR', 'HUMIDITY_SENSOR', 
                       'MULTI_SENSOR', 'SMART_METER']
        locations = ['BUILDING_A_FLOOR_1', 'BUILDING_A_FLOOR_2', 'BUILDING_B_WAREHOUSE',
                    'BUILDING_B_SERVER_ROOM', 'OUTDOOR_YARD_NORTH', 'OUTDOOR_YARD_SOUTH']
        
        for i in range(1, 101):
            device = {
                'device_id': f'DEV-{i:03d}',
                'device_name': f'Sensor {i}',
                'device_type': random.choice(device_types),
                'location': random.choice(locations),
                'status': 'ACTIVE',
                'calibration_offset': random.uniform(-0.5, 0.5),
                'firmware_version': f'v{random.randint(1, 3)}.{random.randint(0, 9)}'
            }
            self.devices.append(device)
        print(f"✅ Generated {len(self.devices)} default devices")
    
    def get_active_devices(self) -> List[Dict]:
        """获取活跃设备列表"""
        return [d for d in self.devices if d.get('status') == 'ACTIVE']
    
    def get_device_by_id(self, device_id: str) -> Optional[Dict]:
        """根据ID获取设备"""
        for device in self.devices:
            if device['device_id'] == device_id:
                return device
        return None


class SensorDataGenerator:
    """传感器数据生成器"""
    
    # 传感器读数基准值和范围
    SENSOR_PROFILES = {
        'TEMPERATURE_SENSOR': {
            'base_temp': 22.0,
            'temp_variation': 5.0,
            'seasonal_factor': 10.0,  # 季节性变化幅度
            'daily_factor': 3.0,      # 日变化幅度
            'noise_level': 0.2
        },
        'PRESSURE_SENSOR': {
            'base_pressure': 101.3,
            'pressure_variation': 10.0,
            'noise_level': 0.5
        },
        'HUMIDITY_SENSOR': {
            'base_humidity': 50.0,
            'humidity_variation': 20.0,
            'noise_level': 1.0
        },
        'MULTI_SENSOR': {
            'base_temp': 22.0,
            'base_pressure': 101.3,
            'base_humidity': 50.0,
            'noise_level': 0.3
        },
        'SMART_METER': {
            'base_voltage': 3.3,
            'voltage_variation': 0.3,
            'noise_level': 0.05
        }
    }
    
    def __init__(self, device_registry: DeviceRegistry):
        self.registry = device_registry
        self.start_time = datetime.utcnow()
    
    def generate_reading(self, device: Dict, timestamp: datetime, 
                        out_of_order: bool = False) -> Dict:
        """
        生成单个传感器读数
        
        Args:
            device: 设备信息
            timestamp: 事件时间戳
            out_of_order: 是否为乱序数据
        """
        device_type = device['device_type']
        profile = self.SENSOR_PROFILES.get(device_type, self.SENSOR_PROFILES['TEMPERATURE_SENSOR'])
        
        reading = {
            'reading_id': str(uuid.uuid4()),
            'device_id': device['device_id'],
            'device_type': device_type,
            'location': device.get('location', 'UNKNOWN'),
            'event_time': timestamp.isoformat() + 'Z',
            'sensor_version': device.get('sensor_version', 'v1.0'),
            'firmware_version': device.get('firmware_version', 'v1.0'),
            'out_of_order': out_of_order
        }
        
        # 根据设备类型生成相应的传感器数据
        if device_type == 'TEMPERATURE_SENSOR':
            reading.update(self._generate_temperature_data(profile, timestamp))
        elif device_type == 'PRESSURE_SENSOR':
            reading.update(self._generate_pressure_data(profile))
        elif device_type == 'HUMIDITY_SENSOR':
            reading.update(self._generate_humidity_data(profile))
        elif device_type == 'MULTI_SENSOR':
            reading.update(self._generate_multi_sensor_data(profile, timestamp))
        elif device_type == 'SMART_METER':
            reading.update(self._generate_smart_meter_data(profile))
        
        # 应用校准偏移
        calibration = device.get('calibration_offset', 0.0)
        if 'temperature' in reading and reading['temperature'] is not None:
            reading['temperature'] += calibration
        
        # 偶尔生成缺失值（模拟传感器故障）
        if random.random() < 0.02:  # 2%概率数据缺失
            field_to_null = random.choice(['temperature', 'pressure', 'humidity'])
            if field_to_null in reading:
                reading[field_to_null] = None
        
        # 偶尔生成异常值
        if random.random() < 0.005:  # 0.5%概率异常值
            if 'temperature' in reading and reading['temperature'] is not None:
                reading['temperature'] = random.uniform(80, 100)  # 异常高温
        
        return reading
    
    def _generate_temperature_data(self, profile: Dict, timestamp: datetime) -> Dict:
        """生成温度数据（带季节性/日变化模式）"""
        base = profile['base_temp']
        
        # 季节性变化（简化模型）
        day_of_year = timestamp.timetuple().tm_yday
        seasonal = profile['seasonal_factor'] * (day_of_year / 365 - 0.5)
        
        # 日变化
        hour = timestamp.hour
        daily = profile['daily_factor'] * ((hour - 14) / 12)  # 14点为最高温
        
        # 随机噪声
        noise = random.gauss(0, profile['noise_level'])
        
        temperature = base + seasonal + daily + noise
        
        return {
            'temperature': round(temperature, 2),
            'pressure': None,
            'humidity': None,
            'voltage': round(random.uniform(3.0, 3.6), 2)
        }
    
    def _generate_pressure_data(self, profile: Dict) -> Dict:
        """生成压力数据"""
        base = profile['base_pressure']
        variation = random.gauss(0, profile['pressure_variation'])
        noise = random.gauss(0, profile['noise_level'])
        
        pressure = base + variation + noise
        
        return {
            'temperature': None,
            'pressure': round(pressure, 2),
            'humidity': None,
            'voltage': round(random.uniform(3.0, 3.6), 2)
        }
    
    def _generate_humidity_data(self, profile: Dict) -> Dict:
        """生成湿度数据"""
        base = profile['base_humidity']
        variation = random.gauss(0, profile['humidity_variation'])
        noise = random.gauss(0, profile['noise_level'])
        
        humidity = base + variation + noise
        humidity = max(0, min(100, humidity))  # 限制在0-100范围内
        
        return {
            'temperature': None,
            'pressure': None,
            'humidity': round(humidity, 2),
            'voltage': round(random.uniform(3.0, 3.6), 2)
        }
    
    def _generate_multi_sensor_data(self, profile: Dict, timestamp: datetime) -> Dict:
        """生成多传感器数据"""
        temp_base = profile['base_temp']
        hour = timestamp.hour
        daily = 3.0 * ((hour - 14) / 12)
        temperature = temp_base + daily + random.gauss(0, 0.3)
        
        pressure = profile['base_pressure'] + random.gauss(0, 5.0)
        humidity = profile['base_humidity'] + random.gauss(0, 10.0)
        
        return {
            'temperature': round(temperature, 2),
            'pressure': round(pressure, 2),
            'humidity': round(max(0, min(100, humidity)), 2),
            'voltage': round(random.uniform(3.0, 3.6), 2)
        }
    
    def _generate_smart_meter_data(self, profile: Dict) -> Dict:
        """生成智能电表数据"""
        base = profile['base_voltage']
        variation = random.gauss(0, profile['voltage_variation'])
        noise = random.gauss(0, profile['noise_level'])
        
        voltage = base + variation + noise
        voltage = max(0, min(5, voltage))
        
        return {
            'temperature': round(random.uniform(20, 30), 2),  # 设备温度
            'pressure': None,
            'humidity': None,
            'voltage': round(voltage, 3),
            'current': round(random.uniform(0.1, 10.0), 3),
            'power': round(random.uniform(0.5, 50.0), 3)
        }


class DataPublisher:
    """数据发布器 - 支持Kafka和MQTT"""
    
    def __init__(self, kafka_servers: str = None, mqtt_broker: str = None, mqtt_port: int = 1883):
        self.kafka_producer = None
        self.mqtt_client = None
        self.messages_sent = {'kafka': 0, 'mqtt': 0, 'console': 0}
        
        # 初始化Kafka
        if KAFKA_AVAILABLE and kafka_servers:
            try:
                self.kafka_producer = KafkaProducer(
                    bootstrap_servers=kafka_servers,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    key_serializer=lambda v: v.encode('utf-8') if v else None,
                    acks='all',
                    retries=3,
                    batch_size=16384,
                    linger_ms=10
                )
                print(f"✅ Kafka producer connected to {kafka_servers}")
            except Exception as e:
                print(f"⚠️ Kafka connection failed: {e}")
        
        # 初始化MQTT
        if MQTT_AVAILABLE and mqtt_broker:
            try:
                self.mqtt_client = mqtt.Client()
                self.mqtt_client.on_connect = self._on_mqtt_connect
                self.mqtt_client.on_publish = self._on_mqtt_publish
                self.mqtt_client.connect(mqtt_broker, mqtt_port, 60)
                self.mqtt_client.loop_start()
                print(f"✅ MQTT client connected to {mqtt_broker}:{mqtt_port}")
            except Exception as e:
                print(f"⚠️ MQTT connection failed: {e}")
    
    def _on_mqtt_connect(self, client, userdata, flags, rc):
        """MQTT连接回调"""
        if rc == 0:
            print("✅ MQTT connected successfully")
        else:
            print(f"⚠️ MQTT connection failed with code {rc}")
    
    def _on_mqtt_publish(self, client, userdata, mid):
        """MQTT发布回调"""
        pass
    
    def publish_to_kafka(self, topic: str, message: Dict, key: str = None):
        """发布到Kafka"""
        if self.kafka_producer:
            try:
                future = self.kafka_producer.send(topic, key=key, value=message)
                # 不等待确认，提高吞吐量
                self.messages_sent['kafka'] += 1
                return True
            except Exception as e:
                print(f"❌ Kafka publish error: {e}")
                return False
        return False
    
    def publish_to_mqtt(self, topic: str, message: Dict):
        """发布到MQTT"""
        if self.mqtt_client:
            try:
                payload = json.dumps(message)
                result = self.mqtt_client.publish(topic, payload, qos=1)
                if result.rc == 0:
                    self.messages_sent['mqtt'] += 1
                    return True
            except Exception as e:
                print(f"❌ MQTT publish error: {e}")
                return False
        return False
    
    def publish_to_console(self, message: Dict):
        """输出到控制台（用于调试）"""
        print(json.dumps(message, indent=2, ensure_ascii=False))
        self.messages_sent['console'] += 1
        return True
    
    def get_stats(self) -> Dict:
        """获取发送统计"""
        return self.messages_sent.copy()
    
    def close(self):
        """关闭连接"""
        if self.kafka_producer:
            self.kafka_producer.flush()
            self.kafka_producer.close()
            print("✅ Kafka producer closed")
        
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            print("✅ MQTT client disconnected")


class BatchDataGenerator:
    """批量数据生成器 - 模拟批量上报场景"""
    
    def __init__(self, sensor_generator: SensorDataGenerator, device_registry: DeviceRegistry):
        self.generator = sensor_generator
        self.registry = device_registry
    
    def generate_batch(self, device_ids: List[str], start_time: datetime, 
                      end_time: datetime, interval_seconds: int = 60) -> List[Dict]:
        """
        生成批量历史数据
        
        Args:
            device_ids: 设备ID列表
            start_time: 开始时间
            end_time: 结束时间
            interval_seconds: 数据间隔（秒）
        """
        batch_data = []
        current_time = start_time
        
        devices = [self.registry.get_device_by_id(did) for did in device_ids]
        devices = [d for d in devices if d is not None]
        
        while current_time <= end_time:
            for device in devices:
                reading = self.generator.generate_reading(device, current_time)
                reading['batch_mode'] = True
                reading['batch_sequence'] = len(batch_data)
                batch_data.append(reading)
            
            current_time += timedelta(seconds=interval_seconds)
        
        return batch_data


class SensorSimulator:
    """传感器模拟器主类"""
    
    def __init__(self):
        self.running = False
        self.registry = None
        self.generator = None
        self.publisher = None
        self.batch_generator = None
        
        # 配置参数（从环境变量读取，提供默认值）
        self.config = {
            'device_count': int(os.getenv('DEVICE_COUNT', '100')),
            'message_rate': int(os.getenv('MESSAGE_RATE', '10')),  # 每秒消息数
            'out_of_order_probability': float(os.getenv('OUT_OF_ORDER_PROBABILITY', '0.05')),
            'batch_mode': os.getenv('BATCH_MODE', 'false').lower() == 'true',
            'kafka_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092'),
            'mqtt_broker': os.getenv('MQTT_BROKER', 'emqx'),
            'mqtt_port': int(os.getenv('MQTT_PORT', '1883')),
            'registry_file': os.getenv('DEVICE_REGISTRY_FILE', 'device-registry.json')
        }
        
        # 乱序数据缓冲区
        self.out_of_order_buffer = []
        
        # 统计信息
        self.stats = {
            'messages_generated': 0,
            'out_of_order_count': 0,
            'batch_messages': 0,
            'start_time': None
        }
        
        # 信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """处理终止信号"""
        print("\n🛑 Shutting down gracefully...")
        self.running = False
    
    def initialize(self):
        """初始化组件"""
        print("🚀 Initializing Sensor Simulator...")
        print(f"📊 Configuration: {json.dumps(self.config, indent=2)}")
        
        # 加载设备注册表
        self.registry = DeviceRegistry(self.config['registry_file'])
        
        # 初始化数据生成器
        self.generator = SensorDataGenerator(self.registry)
        
        # 初始化数据发布器
        self.publisher = DataPublisher(
            kafka_servers=self.config['kafka_servers'],
            mqtt_broker=self.config['mqtt_broker'],
            mqtt_port=self.config['mqtt_port']
        )
        
        # 初始化批量生成器
        self.batch_generator = BatchDataGenerator(self.generator, self.registry)
        
        self.stats['start_time'] = datetime.utcnow()
        print("✅ Initialization complete")
    
    def generate_out_of_order_timestamp(self, base_time: datetime) -> Tuple[datetime, bool]:
        """
        生成可能乱序的时间戳
        
        Returns:
            (timestamp, is_out_of_order)
        """
        if random.random() < self.config['out_of_order_probability']:
            # 生成延迟5-60秒的乱序数据
            delay_seconds = random.randint(5, 60)
            delayed_time = base_time - timedelta(seconds=delay_seconds)
            return delayed_time, True
        return base_time, False
    
    def run_realtime_mode(self):
        """运行实时模式"""
        print("🔄 Starting REAL-TIME mode...")
        
        active_devices = self.registry.get_active_devices()
        if not active_devices:
            print("❌ No active devices found!")
            return
        
        print(f"📟 Active devices: {len(active_devices)}")
        
        interval = 1.0 / self.config['message_rate']
        
        while self.running:
            try:
                # 随机选择设备
                device = random.choice(active_devices)
                
                # 生成时间戳（可能乱序）
                current_time = datetime.utcnow()
                event_time, is_out_of_order = self.generate_out_of_order_timestamp(current_time)
                
                # 生成读数
                reading = self.generator.generate_reading(device, event_time, is_out_of_order)
                
                # 如果是乱序数据，加入缓冲区
                if is_out_of_order:
                    self.out_of_order_buffer.append(reading)
                    self.stats['out_of_order_count'] += 1
                    
                    # 随机释放缓冲区中的旧数据
                    if len(self.out_of_order_buffer) > 10 or random.random() < 0.3:
                        old_reading = self.out_of_order_buffer.pop(0)
                        self._publish_reading(old_reading)
                else:
                    self._publish_reading(reading)
                
                self.stats['messages_generated'] += 1
                
                # 定期打印统计
                if self.stats['messages_generated'] % 100 == 0:
                    self._print_stats()
                
                time.sleep(interval)
                
            except Exception as e:
                print(f"❌ Error in realtime loop: {e}")
                time.sleep(1)
        
        # 清空缓冲区
        print(f"📤 Flushing {len(self.out_of_order_buffer)} buffered messages...")
        for reading in self.out_of_order_buffer:
            self._publish_reading(reading)
    
    def run_batch_mode(self):
        """运行批量模式"""
        print("📦 Starting BATCH mode...")
        
        active_devices = self.registry.get_active_devices()
        device_ids = [d['device_id'] for d in active_devices[:20]]  # 使用前20个设备
        
        # 生成过去24小时的历史数据
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)
        
        print(f"📊 Generating batch data from {start_time} to {end_time}")
        
        batch_data = self.batch_generator.generate_batch(
            device_ids=device_ids,
            start_time=start_time,
            end_time=end_time,
            interval_seconds=300  # 每5分钟一条数据
        )
        
        print(f"📦 Generated {len(batch_data)} batch records")
        
        # 打乱顺序模拟乱序到达
        random.shuffle(batch_data)
        
        # 发布数据
        for i, reading in enumerate(batch_data):
            if not self.running:
                break
            
            self._publish_reading(reading)
            self.stats['batch_messages'] += 1
            
            if (i + 1) % 100 == 0:
                print(f"📤 Published {i + 1}/{len(batch_data)} batch records")
            
            time.sleep(0.01)  # 控制发布速率
        
        print(f"✅ Batch mode complete. Published {self.stats['batch_messages']} records")
    
    def _publish_reading(self, reading: Dict):
        """发布读数到所有可用通道"""
        device_id = reading['device_id']
        device_type = reading['device_type']
        
        # Kafka发布
        self.publisher.publish_to_kafka(
            topic='sensor-readings',
            message=reading,
            key=device_id
        )
        
        # MQTT发布
        mqtt_topic = f"sensors/{device_id}/data"
        self.publisher.publish_to_mqtt(mqtt_topic, reading)
        
        # 设备事件（注册表变更）
        if random.random() < 0.001:  # 0.1%概率发送设备事件
            self._publish_device_event(reading)
    
    def _publish_device_event(self, reading: Dict):
        """发布设备事件"""
        event = {
            'device_id': reading['device_id'],
            'event_type': 'HEARTBEAT',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'status': 'ACTIVE'
        }
        self.publisher.publish_to_kafka('device-events', event)
    
    def _print_stats(self):
        """打印统计信息"""
        elapsed = (datetime.utcnow() - self.stats['start_time']).total_seconds()
        rate = self.stats['messages_generated'] / elapsed if elapsed > 0 else 0
        
        print(f"\n📊 Statistics (running for {elapsed:.0f}s):")
        print(f"   Messages generated: {self.stats['messages_generated']}")
        print(f"   Out of order: {self.stats['out_of_order_count']} ({100*self.stats['out_of_order_count']/max(self.stats['messages_generated'],1):.1f}%)")
        print(f"   Generation rate: {rate:.1f} msg/s")
        print(f"   Publisher stats: {self.publisher.get_stats()}")
    
    def run(self):
        """主运行循环"""
        self.running = True
        
        try:
            if self.config['batch_mode']:
                self.run_batch_mode()
            else:
                self.run_realtime_mode()
        finally:
            self._print_stats()
            self.publisher.close()
            print("👋 Simulator stopped")


def main():
    """入口函数"""
    print("=" * 60)
    print("  Flink IoT Sensor Data Generator")
    print("  Version: 1.0.0 | Formality Level: L4")
    print("=" * 60)
    
    simulator = SensorSimulator()
    simulator.initialize()
    simulator.run()


if __name__ == "__main__":
    main()
