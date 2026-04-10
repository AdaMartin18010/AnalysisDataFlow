# ============================================================================
# Python: 流式信号处理 (Signal Processing)
# ============================================================================
#
# 本示例演示使用 Python 生成器实现流式信号处理。
#
# 核心概念:
# - 无限流: 使用生成器表示无限信号
# - 流变换: 滤波、变换、采样
# - 实时处理: 逐样本处理, 低内存占用
# - 组合器: 组合多个流操作
#
# 信号处理操作:
# - 采样 (Sampling)
# - 滤波 (Filtering): 低通、高通、带通
# - 变换 (Transform): FFT、DCT
# - 分析 (Analysis): 包络、零交叉率
#
# 参考:
# - Oppenheim & Schafer (2010). Discrete-Time Signal Processing
# - Python Generators and Iterators
# ============================================================================

import math
import cmath
from typing import Iterator, Callable, List, Tuple, Optional
from dataclasses import dataclass
from collections import deque
import itertools

# ----------------------------------------------------------------------------
# 基础信号生成器
# ----------------------------------------------------------------------------

def sine_wave(frequency: float, sample_rate: float = 44100.0) -> Iterator[float]:
    """
    生成正弦波信号流
    
    Args:
        frequency: 频率 (Hz)
        sample_rate: 采样率 (Hz)
    
    Yields:
        正弦波样本值
    
    Example:
        >>> gen = sine_wave(440)  # A4音符
        >>> samples = [next(gen) for _ in range(10)]
    """
    phase = 0.0
    increment = 2 * math.pi * frequency / sample_rate
    while True:
        yield math.sin(phase)
        phase += increment
        # 保持相位在 [0, 2π) 范围内
        if phase >= 2 * math.pi:
            phase -= 2 * math.pi


def cosine_wave(frequency: float, sample_rate: float = 44100.0) -> Iterator[float]:
    """生成余弦波信号流"""
    phase = 0.0
    increment = 2 * math.pi * frequency / sample_rate
    while True:
        yield math.cos(phase)
        phase += increment
        if phase >= 2 * math.pi:
            phase -= 2 * math.pi


def square_wave(frequency: float, sample_rate: float = 44100.0, 
                duty_cycle: float = 0.5) -> Iterator[float]:
    """
    生成方波信号流
    
    Args:
        duty_cycle: 占空比 (0到1之间)
    """
    phase = 0.0
    period = sample_rate / frequency
    while True:
        yield 1.0 if (phase % period) < (duty_cycle * period) else -1.0
        phase += 1.0


def sawtooth_wave(frequency: float, sample_rate: float = 44100.0) -> Iterator[float]:
    """生成锯齿波信号流"""
    phase = 0.0
    period = sample_rate / frequency
    while True:
        yield 2.0 * (phase % period) / period - 1.0
        phase += 1.0


def triangle_wave(frequency: float, sample_rate: float = 44100.0) -> Iterator[float]:
    """生成三角波信号流"""
    phase = 0.0
    period = sample_rate / frequency
    while True:
        p = phase % period
        if p < period / 2:
            yield 4.0 * p / period - 1.0
        else:
            yield 3.0 - 4.0 * p / period
        phase += 1.0


def white_noise(amplitude: float = 1.0) -> Iterator[float]:
    """生成白噪声流"""
    import random
    while True:
        yield amplitude * (2.0 * random.random() - 1.0)


def impulse_train(frequency: float, sample_rate: float = 44100.0) -> Iterator[float]:
    """生成脉冲序列"""
    period = int(sample_rate / frequency)
    count = 0
    while True:
        yield 1.0 if count == 0 else 0.0
        count = (count + 1) % period


# ----------------------------------------------------------------------------
# 流变换操作
# ----------------------------------------------------------------------------

def map_stream(f: Callable[[float], float], 
               stream: Iterator[float]) -> Iterator[float]:
    """
    对流应用函数变换 (类似函数式编程的 map)
    
    Example:
        >>> sine = sine_wave(440)
        >>> amplified = map_stream(lambda x: x * 2, sine)
    """
    while True:
        yield f(next(stream))


def zip_with_streams(f: Callable[[float, float], float],
                     stream1: Iterator[float],
                     stream2: Iterator[float]) -> Iterator[float]:
    """
    合并两个流 (类似 Haskell 的 zipWith)
    
    Example:
        >>> mixed = zip_with_streams(lambda a, b: (a+b)/2, sine, cosine)
    """
    while True:
        yield f(next(stream1), next(stream2))


def filter_stream(predicate: Callable[[float], bool],
                  stream: Iterator[float]) -> Iterator[float]:
    """
    过滤流中的值 (类似函数式编程的 filter)
    
    注意: 这是一个有状态的过滤器, 会跳过不满足条件的样本
    """
    while True:
        value = next(stream)
        if predicate(value):
            yield value


def take(n: int, stream: Iterator[float]) -> List[float]:
    """从流中取前n个值"""
    return [next(stream) for _ in range(n)]


def drop(n: int, stream: Iterator[float]) -> Iterator[float]:
    """跳过流的前n个值"""
    for _ in range(n):
        next(stream)
    return stream


def every_nth(n: int, stream: Iterator[float]) -> Iterator[float]:
    """每n个样本取一个 (降采样)"""
    count = 0
    for value in stream:
        if count % n == 0:
            yield value
        count += 1


# ----------------------------------------------------------------------------
# 数字滤波器
# ----------------------------------------------------------------------------

def moving_average(window_size: int, 
                   stream: Iterator[float]) -> Iterator[float]:
    """
    移动平均滤波器 (低通滤波器)
    
    平滑信号, 去除高频噪声
    """
    window = deque(maxlen=window_size)
    
    # 填充窗口
    for _ in range(window_size):
        window.append(next(stream))
        yield sum(window) / len(window)
    
    # 滑动窗口
    for value in stream:
        window.append(value)
        yield sum(window) / window_size


def exponential_smoothing(alpha: float, 
                          stream: Iterator[float]) -> Iterator[float]:
    """
    指数平滑滤波器
    
    Args:
        alpha: 平滑因子 (0 < alpha < 1)
               较小值: 更平滑, 响应更慢
               较大值: 更敏感, 更多噪声
    """
    # 初始化
    smoothed = next(stream)
    yield smoothed
    
    for value in stream:
        smoothed = alpha * value + (1 - alpha) * smoothed
        yield smoothed


def high_pass_filter(cutoff: float, sample_rate: float,
                     stream: Iterator[float]) -> Iterator[float]:
    """
    简单高通滤波器 (一阶差分近似)
    
    Args:
        cutoff: 截止频率 (Hz)
    """
    RC = 1.0 / (2 * math.pi * cutoff)
    dt = 1.0 / sample_rate
    alpha = RC / (RC + dt)
    
    prev_input = next(stream)
    prev_output = 0.0
    yield prev_output
    
    for input_val in stream:
        output = alpha * (prev_output + input_val - prev_input)
        yield output
        prev_input = input_val
        prev_output = output


def low_pass_filter(cutoff: float, sample_rate: float,
                    stream: Iterator[float]) -> Iterator[float]:
    """
    简单低通滤波器 (一阶 RC 滤波器)
    
    Args:
        cutoff: 截止频率 (Hz)
    """
    RC = 1.0 / (2 * math.pi * cutoff)
    dt = 1.0 / sample_rate
    alpha = dt / (RC + dt)
    
    smoothed = next(stream)
    yield smoothed
    
    for value in stream:
        smoothed = smoothed + alpha * (value - smoothed)
        yield smoothed


def band_pass_filter(low_cutoff: float, high_cutoff: float,
                     sample_rate: float,
                     stream: Iterator[float]) -> Iterator[float]:
    """带通滤波器: 低通 + 高通级联"""
    return high_pass_filter(low_cutoff, sample_rate,
                           low_pass_filter(high_cutoff, sample_rate, stream))


# ----------------------------------------------------------------------------
# 信号分析
# ----------------------------------------------------------------------------

def rms_window(window_size: int, 
               stream: Iterator[float]) -> Iterator[float]:
    """
    滑动窗口 RMS (均方根) 计算
    
    用于计算信号的能量/响度
    """
    window = deque(maxlen=window_size)
    
    for value in stream:
        window.append(value * value)
        if len(window) == window_size:
            yield math.sqrt(sum(window) / window_size)


def envelope_follower(attack: float, release: float,
                      stream: Iterator[float]) -> Iterator[float]:
    """
    包络跟随器
    
    提取信号的振幅包络
    
    Args:
        attack: 上升时间系数 (0-1)
        release: 下降时间系数 (0-1)
    """
    envelope = 0.0
    
    for value in stream:
        abs_val = abs(value)
        if abs_val > envelope:
            envelope = attack * abs_val + (1 - attack) * envelope
        else:
            envelope = release * abs_val + (1 - release) * envelope
        yield envelope


def zero_crossing_rate(window_size: int,
                       stream: Iterator[float]) -> Iterator[float]:
    """
    零交叉率计算
    
    用于区分清音/浊音, 或检测周期性
    """
    window = deque(maxlen=window_size)
    prev = next(stream)
    window.append(0)
    
    for value in stream:
        crossing = 1 if (prev < 0 and value >= 0) or (prev >= 0 and value < 0) else 0
        window.append(crossing)
        prev = value
        
        if len(window) == window_size:
            yield sum(window) / window_size


def autocorrelation(lag: int, stream: Iterator[float]) -> Iterator[float]:
    """
    自相关计算 (用于基频检测)
    
    Args:
        lag: 延迟样本数
    """
    buffer = deque(maxlen=lag)
    
    # 填充缓冲区
    for _ in range(lag):
        buffer.append(next(stream))
    
    for value in stream:
        old_value = buffer.popleft()
        buffer.append(value)
        yield value * old_value


# ----------------------------------------------------------------------------
# 频域分析 (简化 DFT)
# ----------------------------------------------------------------------------

def dft_window(window_size: int, 
               stream: Iterator[float]) -> Iterator[List[complex]]:
    """
    滑动窗口 DFT (离散傅里叶变换)
    
    每次产生窗口内信号的频谱
    """
    window = deque(maxlen=window_size)
    
    while True:
        # 填充窗口
        while len(window) < window_size:
            window.append(next(stream))
        
        # 计算 DFT
        spectrum = []
        for k in range(window_size):
            sum_val = 0+0j
            for n, sample in enumerate(window):
                angle = -2j * math.pi * k * n / window_size
                sum_val += sample * cmath.exp(angle)
            spectrum.append(sum_val)
        
        yield spectrum
        
        # 滑动 (跳跃 size/2)
        for _ in range(window_size // 2):
            window.append(next(stream))


def goertzel(frequency: float, sample_rate: float,
             stream: Iterator[float]) -> Iterator[float]:
    """
    Goertzel 算法: 计算特定频率的能量
    
    比完整 DFT 更高效, 适用于单频检测 (如 DTMF)
    """
    k = int(0.5 + (len(list(itertools.islice(stream, 100))) * frequency / sample_rate))
    
    # 重新创建流
    omega = 2.0 * math.pi * k / 100
    sine = math.sin(omega)
    cosine = math.cos(omega)
    coeff = 2.0 * cosine
    
    s_prev = 0.0
    s_prev2 = 0.0
    
    for sample in stream:
        s = sample + coeff * s_prev - s_prev2
        s_prev2 = s_prev
        s_prev = s
        
        power = s_prev2 * s_prev2 + s_prev * s_prev - coeff * s_prev * s_prev2
        yield power


# ----------------------------------------------------------------------------
# 信号合成
# ----------------------------------------------------------------------------

def mix_signals(*streams: Iterator[float]) -> Iterator[float]:
    """混合多个信号 (求平均)"""
    while True:
        values = [next(s) for s in streams]
        yield sum(values) / len(values)


def add_signals(*streams: Iterator[float]) -> Iterator[float]:
    """信号相加"""
    while True:
        yield sum(next(s) for s in streams)


def multiply_signals(stream1: Iterator[float], 
                     stream2: Iterator[float]) -> Iterator[float]:
    """信号相乘 (调制)"""
    while True:
        yield next(stream1) * next(stream2)


def amplitude_modulation(carrier_freq: float, mod_freq: float,
                         sample_rate: float = 44100.0,
                         mod_depth: float = 0.5) -> Iterator[float]:
    """
    幅度调制 (AM)
    
    产生调幅信号: [1 + m * sin(2π*mod*t)] * sin(2π*carrier*t)
    """
    carrier = sine_wave(carrier_freq, sample_rate)
    modulator = sine_wave(mod_freq, sample_rate)
    
    while True:
        m = next(modulator)
        c = next(carrier)
        yield (1 + mod_depth * m) * c


def frequency_modulation(carrier_freq: float, mod_freq: float,
                         deviation: float,
                         sample_rate: float = 44100.0) -> Iterator[float]:
    """
    频率调制 (FM)
    
    Args:
        deviation: 频率偏移量 (Hz)
    """
    phase = 0.0
    mod = sine_wave(mod_freq, sample_rate)
    
    while True:
        instantaneous_freq = carrier_freq + deviation * next(mod)
        phase += 2 * math.pi * instantaneous_freq / sample_rate
        yield math.sin(phase)


# ----------------------------------------------------------------------------
# 实用工具
# ----------------------------------------------------------------------------

def signal_to_list(n: int, stream: Iterator[float]) -> List[float]:
    """将流的 n 个样本转换为列表"""
    return take(n, stream)


def print_signal(name: str, n: int, stream: Iterator[float]):
    """打印信号的前 n 个样本"""
    samples = take(n, stream)
    print(f"{name}: {['%.3f' % s for s in samples]}")


def write_wav(filename: str, duration: float, sample_rate: float,
              stream: Iterator[float]):
    """将流写入 WAV 文件 (需要 wave 模块)"""
    try:
        import wave
        import struct
        
        num_samples = int(duration * sample_rate)
        samples = take(num_samples, stream)
        
        # 转换为 16-bit PCM
        pcm_samples = [int(max(-1, min(1, s)) * 32767) for s in samples]
        
        with wave.open(filename, 'w') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            wav.writeframes(struct.pack('<' + 'h' * len(pcm_samples), *pcm_samples))
        
        print(f"Wrote {filename}")
    except ImportError:
        print("wave module not available")


# ----------------------------------------------------------------------------
# 示例演示
# ----------------------------------------------------------------------------

def demo():
    """信号处理示例演示"""
    print("=" * 60)
    print("Signal Processing Stream Demo")
    print("=" * 60)
    
    # 1. 基本信号
    print("\n1. Sine wave (440 Hz, 10 samples):")
    sine = sine_wave(440, 44100)
    print_signal("Sine", 10, sine)
    
    # 2. 信号混合
    print("\n2. Mix of sine (440 Hz) and cosine (880 Hz):")
    mixed = mix_signals(sine_wave(440, 44100), cosine_wave(880, 44100))
    print_signal("Mixed", 10, mixed)
    
    # 3. 移动平均滤波
    print("\n3. Sine wave with moving average filter:")
    noisy = map_stream(lambda x: x + 0.3 * (2 * (hash(str(x)) % 2) - 1), 
                       sine_wave(440, 44100))
    filtered = moving_average(5, noisy)
    print_signal("Filtered", 10, filtered)
    
    # 4. 包络跟随
    print("\n4. AM signal envelope:")
    am_signal = amplitude_modulation(1000, 5, 44100, 0.8)
    envelope = envelope_follower(0.1, 0.1, am_signal)
    print_signal("Envelope", 10, envelope)
    
    # 5. 指数平滑
    print("\n5. Exponential smoothing (alpha=0.3):")
    smoothed = exponential_smoothing(0.3, sine_wave(440, 44100))
    print_signal("Smoothed", 10, smoothed)
    
    # 6. 零交叉率
    print("\n6. Zero crossing rate:")
    zcr = zero_crossing_rate(20, sine_wave(100, 44100))
    print_signal("ZCR", 5, zcr)
    
    # 7. 降采样
    print("\n7. Downsampled by 4:")
    downsampled = every_nth(4, sine_wave(440, 44100))
    print_signal("Downsampled", 10, downsampled)
    
    # 8. RMS 能量
    print("\n8. RMS energy:")
    rms = rms_window(10, sine_wave(440, 44100))
    print_signal("RMS", 5, rms)
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    demo()
