#!/usr/bin/env python3
"""
CGM (Continuous Glucose Monitoring) 设备模拟器
模拟连续血糖监测设备的数据生成和发送

使用方法:
    python cgm_simulator.py --device-id CGM_001 --patient-id PATIENT_001 --interval 300
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


class CGMDataSimulator:
    """
    CGM数据模拟器
    
    模拟血糖变化的生理模型：
    - 随机游走模型模拟基础血糖波动
    - 餐食事件引起血糖上升
    - 胰岛素事件引起血糖下降
    - 昼夜节律影响基础水平
    """
    
    def __init__(
        self,
        device_id: str,
        patient_id: str,
        kafka_bootstrap: str = 'localhost:9092',
        base_glucose: float = 100.0,
        volatility: float = 3.0
    ):
        self.device_id = device_id
        self.patient_id = patient_id
        self.kafka_bootstrap = kafka_bootstrap
        self.current_glucose = base_glucose
        self.volatility = volatility
        self.transmitter_id = f"TX_{device_id}"
        self.sensor_id = f"SENSOR_{device_id}"
        
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
        
        # 运行控制
        self.running = True
        self.reading_count = 0
        
        # 模拟生理事件
        self.last_meal_time = time.time() - 3600  # 1小时前
        self.last_insulin_time = time.time() - 3600
        
        # 信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """处理终止信号"""
        print(f"\n接收到信号 {signum}，正在关闭模拟器...")
        self.running = False
    
    def _get_trend_arrow(self, change: float) -> str:
        """
        根据血糖变化率确定趋势箭头
        
        变化率 (mg/dL/5min):
        - -3.0 ~ : ↓↓ (快速下降)
        - -1.0 ~ -3.0: ↓ (下降)
        - -1.0 ~ 1.0: → (平稳)
        - 1.0 ~ 3.0: ↑ (上升)
        - 3.0 ~ : ↑↑ (快速上升)
        """
        if change < -3.0:
            return '↓↓'
        elif change < -1.0:
            return '↓'
        elif change > 3.0:
            return '↑↑'
        elif change > 1.0:
            return '↑'
        return '→'
    
    def _simulate_meal_effect(self) -> float:
        """模拟餐食对血糖的影响"""
        if random.random() < 0.05:  # 5%概率触发餐食
            self.last_meal_time = time.time()
            return random.uniform(20, 60)  # 血糖上升20-60
        return 0
    
    def _simulate_insulin_effect(self) -> float:
        """模拟胰岛素对血糖的影响"""
        if random.random() < 0.03:  # 3%概率触发胰岛素
            self.last_insulin_time = time.time()
            return random.uniform(-40, -20)  # 血糖下降20-40
        return 0
    
    def _simulate_circadian_rhythm(self, hour: int) -> float:
        """模拟昼夜节律对血糖的影响"""
        # 凌晨3-6点黎明现象（血糖升高）
        if 3 <= hour <= 6:
            return random.uniform(0, 5)
        # 睡眠期间基础水平较低
        elif 0 <= hour <= 5:
            return random.uniform(-5, 0)
        return 0
    
    def generate_reading(self) -> dict:
        """
        生成CGM读数
        
        Returns:
            dict: 包含所有CGM读数字段的字典
        """
        # 基础随机游走
        change = random.gauss(0, self.volatility)
        
        # 叠加生理效应
        change += self._simulate_meal_effect()
        change += self._simulate_insulin_effect()
        
        # 叠加昼夜节律
        current_hour = datetime.now(timezone.utc).hour
        change += self._simulate_circadian_rhythm(current_hour)
        
        # 更新当前血糖值
        self.current_glucose = max(40, min(400, self.current_glucose + change))
        
        # 计算趋势箭头
        trend = self._get_trend_arrow(change)
        
        # 生成模拟电压值
        raw_voltage = round(random.uniform(0.5, 1.5), 6)
        
        reading = {
            'device_id': self.device_id,
            'transmitter_id': self.transmitter_id,
            'patient_id': self.patient_id,
            'glucose_mg_dl': int(self.current_glucose),
            'trend_arrow': trend,
            'reading_time': datetime.now(timezone.utc).isoformat(),
            'sensor_id': self.sensor_id,
            'raw_voltage': raw_voltage,
            'temperature_c': round(random.uniform(32.0, 38.0), 1),
            'data_quality': 'VALID' if 40 <= self.current_glucose <= 400 else 'OUT_OF_RANGE'
        }
        
        return reading
    
    def send_reading(self, reading: dict, topic: str = 'cgm-raw-readings') -> bool:
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
        interval_seconds: float = 300.0,
        max_readings: Optional[int] = None,
        topic: str = 'cgm-raw-readings'
    ):
        """
        运行模拟器
        
        Args:
            interval_seconds: 采样间隔（秒），默认5分钟
            max_readings: 最大读数数量，None表示无限运行
            topic: Kafka topic名称
        """
        print(f"\n{'='*60}")
        print(f"CGM模拟器启动")
        print(f"设备ID: {self.device_id}")
        print(f"患者ID: {self.patient_id}")
        print(f"采样间隔: {interval_seconds}秒 ({interval_seconds/60:.1f}分钟)")
        print(f"Kafka: {self.kafka_bootstrap}")
        print(f"{'='*60}\n")
        
        try:
            while self.running:
                # 生成读数
                reading = self.generate_reading()
                self.reading_count += 1
                
                # 发送数据
                success = self.send_reading(reading, topic)
                
                # 打印状态
                status = "✓" if success else "✗"
                print(
                    f"[{status}] {self.reading_count:6d} | "
                    f"Patient: {self.patient_id} | "
                    f"Glucose: {reading['glucose_mg_dl']:3d} mg/dL | "
                    f"Trend: {reading['trend_arrow']:>2} | "
                    f"Time: {reading['reading_time'][:19]}"
                )
                
                # 检查是否达到最大读数
                if max_readings and self.reading_count >= max_readings:
                    print(f"\n达到最大读数限制 ({max_readings})，停止模拟")
                    break
                
                # 等待下一次采样
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
        description='CGM设备数据模拟器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 基础用法（5分钟间隔）
  python cgm_simulator.py --device-id CGM_001 --patient-id PATIENT_001
  
  # 快速测试模式（10秒间隔）
  python cgm_simulator.py --device-id CGM_001 --patient-id PATIENT_001 --interval 10
  
  # 指定Kafka地址
  python cgm_simulator.py --device-id CGM_001 --patient-id PATIENT_001 --kafka kafka:9092
  
  # 生成指定数量的读数后停止
  python cgm_simulator.py --device-id CGM_001 --patient-id PATIENT_001 --max-readings 100
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
        help='Kafka bootstrap服务器地址 (默认: localhost:9092)'
    )
    parser.add_argument(
        '--interval', '-i',
        type=float,
        default=300.0,
        help='采样间隔（秒）(默认: 300 = 5分钟)'
    )
    parser.add_argument(
        '--base-glucose', '-b',
        type=float,
        default=100.0,
        help='基础血糖值 (默认: 100 mg/dL)'
    )
    parser.add_argument(
        '--volatility', '-v',
        type=float,
        default=3.0,
        help='血糖波动程度 (默认: 3.0)'
    )
    parser.add_argument(
        '--max-readings', '-m',
        type=int,
        default=None,
        help='最大读数数量 (默认: 无限)'
    )
    parser.add_argument(
        '--topic', '-t',
        default='cgm-raw-readings',
        help='Kafka topic名称 (默认: cgm-raw-readings)'
    )
    
    args = parser.parse_args()
    
    # 创建并运行模拟器
    simulator = CGMDataSimulator(
        device_id=args.device_id,
        patient_id=args.patient_id,
        kafka_bootstrap=args.kafka,
        base_glucose=args.base_glucose,
        volatility=args.volatility
    )
    
    simulator.run(
        interval_seconds=args.interval,
        max_readings=args.max_readings,
        topic=args.topic
    )


if __name__ == '__main__':
    main()
