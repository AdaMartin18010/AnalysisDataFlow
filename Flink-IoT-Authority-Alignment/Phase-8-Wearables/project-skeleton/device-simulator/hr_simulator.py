#!/usr/bin/env python3
"""
心率(HR)和心率变异性(HRV)设备模拟器
模拟智能手表/手环的心率监测功能

使用方法:
    python hr_simulator.py --device-id WATCH_001 --patient-id PATIENT_001 --interval 1
"""

import json
import random
import time
import math
import argparse
import signal
import sys
from datetime import datetime, timezone
from typing import Optional

try:
    from kafka import KafkaProducer
except ImportError:
    print("请先安装kafka-python: pip install kafka-python")
    sys.exit(1)


class HeartRateSimulator:
    """
    心率数据模拟器
    
    模拟心率变化的生理模型：
    - 基础心率（静息状态）
    - 呼吸性窦性心律不齐（RSA）
    - 随机噪声
    - 运动状态影响
    """
    
    def __init__(
        self,
        device_id: str,
        patient_id: str,
        kafka_bootstrap: str = 'localhost:9092',
        base_hr: int = 70,
        enable_rsa: bool = True
    ):
        self.device_id = device_id
        self.patient_id = patient_id
        self.kafka_bootstrap = kafka_bootstrap
        self.base_hr = base_hr
        self.enable_rsa = enable_rsa
        
        # RSA参数（呼吸周期约4秒）
        self.rsa_amplitude = 5  # RSA幅度±5bpm
        self.rsa_period = 4.0   # 呼吸周期
        
        # 状态跟踪
        self.current_activity = 'rest'
        self.activity_start_time = time.time()
        
        # 初始化Kafka生产者
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=kafka_bootstrap.split(','),
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',
                retries=3,
                request_timeout_ms=10000
            )
            print(f"✓ Kafka连接成功: {kafka_bootstrap}")
        except Exception as e:
            print(f"✗ Kafka连接失败: {e}")
            self.producer = None
        
        self.running = True
        self.reading_count = 0
        
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """处理终止信号"""
        print(f"\n接收到信号 {signum}，正在关闭模拟器...")
        self.running = False
    
    def _update_activity_state(self):
        """更新活动状态"""
        elapsed = time.time() - self.activity_start_time
        
        # 状态转换概率
        if self.current_activity == 'rest':
            if elapsed > 300 and random.random() < 0.1:  # 5分钟后10%概率开始活动
                self.current_activity = random.choice(['walking', 'light_exercise'])
                self.activity_start_time = time.time()
        elif self.current_activity in ['walking', 'light_exercise']:
            if elapsed > 180 and random.random() < 0.15:  # 3分钟后15%概率停止
                self.current_activity = 'rest'
                self.activity_start_time = time.time()
    
    def _get_activity_hr_offset(self) -> int:
        """根据活动状态获取心率偏移"""
        offsets = {
            'rest': 0,
            'walking': random.randint(20, 40),
            'light_exercise': random.randint(40, 70),
            'sleeping': random.randint(-10, -5)
        }
        return offsets.get(self.current_activity, 0)
    
    def generate_reading(self) -> dict:
        """
        生成心率读数
        
        Returns:
            dict: 包含心率数据的字典
        """
        # 更新活动状态
        self._update_activity_state()
        
        # 当前时间（用于RSA计算）
        t = time.time()
        
        # 基础心率 + 活动偏移
        activity_offset = self._get_activity_hr_offset()
        base = self.base_hr + activity_offset
        
        # 呼吸性窦性心律不齐（RSA）
        rsa = 0
        if self.enable_rsa and self.current_activity == 'rest':
            rsa = self.rsa_amplitude * math.sin(2 * math.pi * t / self.rsa_period)
        
        # 随机噪声
        noise = random.gauss(0, 2)
        
        # 计算心率
        hr = int(base + rsa + noise)
        hr = max(30, min(220, hr))  # 限制在合理范围
        
        # 计算RR间期（毫秒）
        rr_ms = int(60000 / hr) if hr > 0 else 0
        
        # 检测置信度（运动时降低）
        if self.current_activity == 'rest':
            confidence = round(random.uniform(0.90, 1.0), 2)
        else:
            confidence = round(random.uniform(0.70, 0.95), 2)
        
        # 运动标记
        motion_flag = self.current_activity != 'rest'
        
        reading = {
            'device_id': self.device_id,
            'patient_id': self.patient_id,
            'heart_rate': hr,
            'rr_interval_ms': rr_ms,
            'confidence': confidence,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'motion_flag': motion_flag,
            'activity_type': self.current_activity,
            'signal_quality': 'GOOD' if confidence > 0.8 else 'FAIR'
        }
        
        return reading
    
    def send_reading(self, reading: dict, topic: str = 'hr-raw-readings') -> bool:
        """发送读数到Kafka"""
        if not self.producer:
            print(f"模拟发送: {reading}")
            return True
        
        try:
            key = reading['patient_id']
            future = self.producer.send(topic, key=key, value=reading)
            record_metadata = future.get(timeout=10)
            return True
        except Exception as e:
            print(f"发送失败: {e}")
            return False
    
    def run(
        self,
        interval_seconds: float = 1.0,
        max_readings: Optional[int] = None,
        topic: str = 'hr-raw-readings'
    ):
        """
        运行模拟器
        
        Args:
            interval_seconds: 采样间隔（秒），默认1秒
            max_readings: 最大读数数量
            topic: Kafka topic名称
        """
        print(f"\n{'='*60}")
        print(f"心率模拟器启动")
        print(f"设备ID: {self.device_id}")
        print(f"患者ID: {self.patient_id}")
        print(f"基础心率: {self.base_hr} bpm")
        print(f"采样间隔: {interval_seconds}秒")
        print(f"RSA模拟: {'启用' if self.enable_rsa else '禁用'}")
        print(f"{'='*60}\n")
        
        try:
            while self.running:
                reading = self.generate_reading()
                self.reading_count += 1
                
                success = self.send_reading(reading, topic)
                
                status = "✓" if success else "✗"
                print(
                    f"[{status}] {self.reading_count:6d} | "
                    f"Patient: {self.patient_id} | "
                    f"HR: {reading['heart_rate']:3d} bpm | "
                    f"RR: {reading['rr_interval_ms']:4d}ms | "
                    f"Activity: {reading['activity_type']:15} | "
                    f"Motion: {'Yes' if reading['motion_flag'] else 'No '}"
                )
                
                if max_readings and self.reading_count >= max_readings:
                    print(f"\n达到最大读数限制 ({max_readings})，停止模拟")
                    break
                
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\n用户中断")
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """清理资源"""
        print(f"\n{'='*60}")
        print(f"模拟器停止")
        print(f"总读数: {self.reading_count}")
        print(f"{'='*60}")
        
        if self.producer:
            self.producer.flush()
            self.producer.close()


def main():
    parser = argparse.ArgumentParser(
        description='心率设备数据模拟器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 基础用法（1秒间隔）
  python hr_simulator.py --device-id WATCH_001 --patient-id PATIENT_001
  
  # 指定基础心率
  python hr_simulator.py --device-id WATCH_001 --patient-id PATIENT_001 --base-hr 60
  
  # 禁用RSA模拟
  python hr_simulator.py --device-id WATCH_001 --patient-id PATIENT_001 --no-rsa
  
  # 指定Kafka地址
  python hr_simulator.py --device-id WATCH_001 --patient-id PATIENT_001 --kafka kafka:9092
        '''
    )
    
    parser.add_argument(
        '--device-id', '-d',
        required=True,
        help='设备唯一标识符'
    )
    parser.add_argument(
        '--patient-id', '-p',
        required=True,
        help='患者唯一标识符'
    )
    parser.add_argument(
        '--kafka', '-k',
        default='localhost:9092',
        help='Kafka bootstrap服务器地址'
    )
    parser.add_argument(
        '--interval', '-i',
        type=float,
        default=1.0,
        help='采样间隔（秒）(默认: 1)'
    )
    parser.add_argument(
        '--base-hr', '-b',
        type=int,
        default=70,
        help='基础心率 (默认: 70 bpm)'
    )
    parser.add_argument(
        '--no-rsa',
        action='store_true',
        help='禁用呼吸性窦性心律不齐模拟'
    )
    parser.add_argument(
        '--max-readings', '-m',
        type=int,
        default=None,
        help='最大读数数量'
    )
    parser.add_argument(
        '--topic', '-t',
        default='hr-raw-readings',
        help='Kafka topic名称'
    )
    
    args = parser.parse_args()
    
    simulator = HeartRateSimulator(
        device_id=args.device_id,
        patient_id=args.patient_id,
        kafka_bootstrap=args.kafka,
        base_hr=args.base_hr,
        enable_rsa=not args.no_rsa
    )
    
    simulator.run(
        interval_seconds=args.interval,
        max_readings=args.max_readings,
        topic=args.topic
    )


if __name__ == '__main__':
    main()
