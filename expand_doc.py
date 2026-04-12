# 读取现有内容
with open('Knowledge/06-frontier/edge-ai-streaming-architecture.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 在6.4节后添加额外内容
extra_content = """
### 6.5 智慧农业环境监测

**场景描述**：
大型农业基地需要实时监测土壤湿度、温度、光照、病虫害等环境参数，并根据AI模型自动调节灌溉、通风、补光系统。

**边缘AI系统架构**：

```mermaid
graph TB
    subgraph FarmField["农田区域"]
        S1[土壤传感器]
        S2[气象站]
        S3[摄像头]
        S4[虫情测报灯]
    end
    
    subgraph EdgeGateway["边缘网关"]
        GW[数据采集]
        AI[轻量AI模型]
        CTRL[本地控制]
    end
    
    subgraph Actuators["执行设备"]
        A1[灌溉阀门]
        A2[通风设备]
        A3[补光灯]
    end
    
    subgraph Cloud["农业云平台"]
        DB[(时序数据库)]
        ANALYTICS[数据分析]
        MODEL_TRAIN[模型训练]
    end
    
    S1 --> GW
    S2 --> GW
    S3 --> AI
    S4 --> AI
    GW --> AI
    AI --> CTRL
    CTRL --> A1
    CTRL --> A2
    CTRL --> A3
    
    AI -.->|汇总数据| Cloud
    Cloud -.->|模型更新| AI
```

**边缘AI模型部署**：

| 模型 | 任务 | 量化 | 延迟 | 准确率 |
|------|------|------|------|--------|
| MobileNetV3 | 病虫害识别 | INT8 | 25ms | 94.5% |
| LSTM | 环境预测 | FP16 | 15ms | MAE<2% |
| DecisionTree | 控制决策 | INT8 | 2ms | 97% |

**系统效益**：
- 节水30-40%
- 减少农药使用25%
- 作物产量提升15-20%
- 端到端延迟<100ms

---

## 附录A: 边缘模型选型速查表

### A.1 轻量级语言模型对比

| 模型 | 参数量 | 上下文长度 | 中文支持 | 量化后大小 | 推荐场景 |
|------|--------|------------|----------|------------|----------|
| Qwen2.5-0.5B | 0.5B | 32K | 优秀 | 300MB | 极简设备 |
| Qwen2.5-1.8B | 1.8B | 32K | 优秀 | 1GB | 移动设备 |
| Qwen2.5-3B | 3B | 32K | 优秀 | 1.8GB | 边缘服务器 |
| Qwen2.5-7B | 7B | 32K | 优秀 | 4GB | 高性能边缘 |
| Llama-3.2-1B | 1B | 128K | 良好 | 600MB | 英文场景 |
| Llama-3.2-3B | 3B | 128K | 良好 | 1.8GB | 通用英文 |
| Gemma-2B | 2B | 8K | 一般 | 1.2GB | Google生态 |
| Phi-3-mini | 3.8B | 128K | 良好 | 2.2GB | 微软生态 |

### A.2 视觉模型选型

| 模型 | 任务 | 参数量 | 量化大小 | 延迟(Jetson) |
|------|------|--------|----------|--------------|
| YOLOv8-nano | 目标检测 | 3.2M | 4MB | 8ms |
| YOLOv8-s | 目标检测 | 11M | 12MB | 15ms |
| YOLOv8-m | 目标检测 | 25M | 28MB | 25ms |
| MobileNetV3 | 分类 | 5.4M | 6MB | 5ms |
| EfficientNet-B0 | 分类 | 5.3M | 6MB | 8ms |
| ResNet18 | 分类 | 11M | 12MB | 10ms |
| OSNet | 重识别 | 2.2M | 3MB | 12ms |

---

## 附录B: 量化工具使用指南

### B.1 AutoGPTQ使用示例

```python
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig

# 配置量化参数
quantize_config = BaseQuantizeConfig(
    bits=4,
    group_size=128,
    desc_act=False,
)

# 加载模型并量化
model = AutoGPTQForCausalLM.from_pretrained(
    model_name,
    quantize_config=quantize_config,
)
model.quantize(examples)
model.save_quantized(output_dir)
```

### B.2 llama.cpp转换示例

```bash
# 下载并转换模型
python convert-hf-to-gguf.py models/Qwen2.5-7B/

# 量化模型
./quantize models/Qwen2.5-7B-f16.gguf models/Qwen2.5-7B-Q4_K_M.gguf Q4_K_M

# 推理测试
./main -m models/Qwen2.5-7B-Q4_K_M.gguf -p "你好" -n 100
```

### B.3 TensorRT-LLM构建示例

```python
from tensorrt_llm import Builder

# 构建引擎
builder = Builder()
builder_config = builder.create_builder_config(
    name='qwen',
    precision='fp16',
    use_fp8=True,
)

# 编译模型
engine = builder.build_engine(network, builder_config)
engine.save('qwen_7b_fp8.engine')
```
"""

# 找到引用参考的位置并插入
ref_pos = content.find('## 8. 引用参考')
new_content = content[:ref_pos] + extra_content + content[ref_pos:]

with open('Knowledge/06-frontier/edge-ai-streaming-architecture.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('文档已扩充')
