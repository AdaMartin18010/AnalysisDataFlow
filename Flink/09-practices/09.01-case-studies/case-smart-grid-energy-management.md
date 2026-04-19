# 智能电网实时能源管理与优化案例研究 (Smart Grid Real-time Energy Management)

> **所属阶段**: Flink/07-case-studies | **前置依赖**: [../02-core-mechanisms/time-semantics-and-watermark.md](../../02-core/time-semantics-and-watermark.md), [../02-core-mechanisms/checkpoint-mechanism-deep-dive.md](../../02-core/checkpoint-mechanism-deep-dive.md), [../12-ai-ml/online-learning-algorithms.md](../../06-ai-ml/online-learning-algorithms.md) | **形式化等级**: L4

---

> **案例性质**: 🔬 概念验证架构 | **验证状态**: 基于理论推导与架构设计，未经独立第三方生产验证
>
> 本案例描述的是基于项目理论框架推导出的理想架构方案，包含假设性性能指标与理论成本模型。
> 实际生产部署可能因环境差异、数据规模、团队能力等因素产生显著不同结果。
> 建议将其作为架构设计参考而非直接复制粘贴的生产蓝图。
>
## 目录

- [智能电网实时能源管理与优化案例研究 (Smart Grid Real-time Energy Management)](#智能电网实时能源管理与优化案例研究-smart-grid-real-time-energy-management)
  - [目录](#目录)
  - [1. 概念定义 (Definitions)](#1-概念定义-definitions)
    - [1.1 智能电网形式化定义](#11-智能电网形式化定义)
    - [1.2 负荷预测形式化定义](#12-负荷预测形式化定义)
    - [1.3 可再生能源出力预测形式化定义](#13-可再生能源出力预测形式化定义)
    - [1.4 需求响应形式化定义](#14-需求响应形式化定义)
    - [1.5 电网异常检测形式化定义](#15-电网异常检测形式化定义)
  - [2. 属性推导 (Properties)](#2-属性推导-properties)
    - [2.1 预测准确率边界](#21-预测准确率边界)
    - [2.2 实时性保证](#22-实时性保证)
    - [2.3 系统稳定性保证](#23-系统稳定性保证)
  - [3. 关系建立 (Relations)](#3-关系建立-relations)
    - [3.1 与SCADA系统的关系](#31-与scada系统的关系)
    - [3.2 与EMS能量管理系统的关系](#32-与ems能量管理系统的关系)
    - [3.3 与AMI高级计量架构的关系](#33-与ami高级计量架构的关系)
    - [3.4 与电力市场的关系](#34-与电力市场的关系)
  - [4. 论证过程 (Argumentation)](#4-论证过程-argumentation)
    - [4.1 实时优化必要性论证](#41-实时优化必要性论证)
    - [4.2 可再生能源波动处理论证](#42-可再生能源波动处理论证)
    - [4.3 动态定价策略论证](#43-动态定价策略论证)
  - [5. 工程论证 (Engineering Argument)](#5-工程论证-engineering-argument)
    - [5.1 预测算法选型论证](#51-预测算法选型论证)
    - [5.2 状态后端选型论证](#52-状态后端选型论证)
    - [5.3 时间序列数据库选型论证](#53-时间序列数据库选型论证)
  - [6. 实例验证 (Examples)](#6-实例验证-examples)
    - [6.1 案例背景](#61-案例背景)
    - [6.2 完整Flink实现代码](#62-完整flink实现代码)
      - [6.2.1 项目依赖 (pom.xml)](#621-项目依赖-pomxml)
      - [6.2.2 核心数据模型](#622-核心数据模型)
      - [6.2.3 主应用程序](#623-主应用程序)
    - [6.3 CEP电网异常检测实现](#63-cep电网异常检测实现)
    - [6.4 实时负荷预测实现](#64-实时负荷预测实现)
    - [6.5 动态定价策略实现](#65-动态定价策略实现)
  - [7. 可视化 (Visualizations)](#7-可视化-visualizations)
    - [7.1 智能电网架构图](#71-智能电网架构图)
    - [7.2 电网拓扑数据流图](#72-电网拓扑数据流图)
    - [7.3 预测曲线对比图](#73-预测曲线对比图)
    - [7.4 异常检测CEP流程图](#74-异常检测cep流程图)
  - [8. 业务成果 (Business Outcomes)](#8-业务成果-business-outcomes)
    - [8.1 预测准确率提升](#81-预测准确率提升)
    - [8.2 运营效率提升](#82-运营效率提升)
    - [8.3 经济效益](#83-经济效益)
    - [8.4 环境效益](#84-环境效益)
  - [9. 经验总结 (Lessons Learned)](#9-经验总结-lessons-learned)
    - [9.1 成功经验](#91-成功经验)
    - [9.2 挑战与应对](#92-挑战与应对)
    - [9.3 最佳实践](#93-最佳实践)
  - [10. 引用参考 (References)](#10-引用参考-references)

---

## 1. 概念定义 (Definitions)

### 1.1 智能电网形式化定义

**Def-F-07-50** (智能电网系统): 智能电网是一个十元组 $\mathcal{G} = (N, L, G, C, S, D, \mathcal{P}, \mathcal{F}, \mathcal{T}, \mathcal{O})$，其中：

- $N$：电网节点集合，$N = \{n_1, n_2, ..., n_m\}$，包含发电节点、变电节点、负荷节点
  - 发电节点 $N_G \subseteq N$：传统火电、水电、核电等
  - 可再生能源节点 $N_R \subseteq N$：风电场、光伏电站
  - 负荷节点 $N_L \subseteq N$：工业、商业、居民用户

- $L$：输电线路集合，$L = \{(n_i, n_j, cap_{ij}, imp_{ij}) | n_i, n_j \in N\}$
  - $cap_{ij}$：线路容量上限 (MW)
  - $imp_{ij}$：线路阻抗参数

- $G$：发电机集合，$G = \{g_1, g_2, ..., g_k\}$，每台发电机 $g_i = (P_{min}, P_{max}, R_{up}, R_{down}, c_i(P))$
  - $R_{up}, R_{down}$：上下爬坡速率 (MW/min)
  - $c_i(P)$：发电成本函数

- $C$：智能电表集合 (AMI)，$C = \{c_1, c_2, ..., c_n\}$，采样周期 $\Delta t \in \{15s, 1min, 5min, 15min\}$

- $S$：实时数据流，$S = \{(t, src, type, value, quality) | t \in \mathcal{T}, src \in C \cup W \cup M\}$
  - $W$：气象数据源
  - $M$：市场数据源

- $D$：需求响应资源集合，$D = \{d_1, d_2, ..., d_p\}$，每个资源有弹性调节能力

- $\mathcal{P}$：预测模型集合，$\mathcal{P} = \{P_{load}, P_{solar}, P_{wind}, P_{price}\}$

- $\mathcal{F}$：控制决策函数，$\mathcal{F}: S \times \mathcal{H} \rightarrow \mathcal{A}$

- $\mathcal{T}$：时间域，支持事件时间和处理时间语义

- $\mathcal{O}$：优化目标函数：

$$
\min_{P_G, P_R, P_{DR}} \quad \sum_{t} \left[ c_{gen}(P_G(t)) + c_{curt}(P_{curt}(t)) + c_{imb}(\Delta P(t)) \right]
$$

约束条件：

- 功率平衡：$\sum P_G + \sum P_R + \sum P_{DR} = P_{load}$ (实时)
- 线路容量：$|flow_{ij}| \leq cap_{ij}, \forall (i,j) \in L$
- 发电机约束：$P_{min} \leq P_G \leq P_{max}$, $|\Delta P_G/\Delta t| \leq R$

### 1.2 负荷预测形式化定义

**Def-F-07-51** (负荷预测): 负荷预测是一个时序回归问题，定义为：

$$
\hat{P}_{load}(t + h) = f_{load}(\mathcal{H}_{load}, \mathcal{H}_{weather}, \mathcal{H}_{calendar}, \theta_{load})
$$

其中：

- $h$：预测提前期 (forecast horizon)，$h \in \{5min, 15min, 1h, 4h, 24h\}$
- $\mathcal{H}_{load}$：历史负荷序列，$\mathcal{H}_{load} = \{P_{load}(t - k) | k = 1, 2, ..., K\}$
- $\mathcal{H}_{weather}$：历史气象数据（温度、湿度、风速）
- $\mathcal{H}_{calendar}$：日历特征（时段、星期、节假日）
- $\theta_{load}$：模型参数

**预测精度指标**:

**MAPE** (Mean Absolute Percentage Error):

$$
\text{MAPE} = \frac{100\%}{N} \sum_{i=1}^{N} \left| \frac{P_i - \hat{P}_i}{P_i} \right|
$$

**RMSE** (Root Mean Square Error):

$$
\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (P_i - \hat{P}_i)^2}
$$

**预测等级分类**:

| 预测类型 | 提前期 | 应用场景 | 精度要求 |
|---------|--------|---------|---------|
| 超短期 | 5-15分钟 | 实时调度、AGC | MAPE < 3% |
| 短期 | 1-4小时 | 经济调度 | MAPE < 5% |
| 日前 | 24小时 | 日前市场 | MAPE < 8% |

### 1.3 可再生能源出力预测形式化定义

**Def-F-07-52** (可再生能源出力预测):

**光伏出力预测**:

$$
\hat{P}_{PV}(t + h) = \eta_{PV} \cdot A_{PV} \cdot I_{POA}(t + h) \cdot (1 - \alpha_{temp}(T_{cell} - T_{ref}))
$$

其中：

- $\eta_{PV}$：光伏板转换效率
- $A_{PV}$：光伏阵列面积
- $I_{POA}$：倾斜面辐照度 (Plane of Array irradiance)
- $\alpha_{temp}$：温度系数 (~0.4%/°C)
- $T_{cell}$：电池板温度

**风电出力预测**:

$$
\hat{P}_{wind}(t + h) = \begin{cases}
0 & v < v_{cut-in} \\
\frac{1}{2} \rho A C_p(\lambda, \beta) v^3 & v_{cut-in} \leq v < v_{rated} \\
P_{rated} & v_{rated} \leq v < v_{cut-out} \\
0 & v \geq v_{cut-out}
\end{cases}
$$

其中：

- $\rho$：空气密度 (kg/m³)
- $A$：风轮扫风面积 (m²)
- $C_p$：功率系数 (Betz极限 0.593)
- $v$：风速 (m/s)

**预测不确定性量化**:

**Def-F-07-53** (预测区间): 预测区间 $[\hat{P}_{lower}, \hat{P}_{upper}]$ 满足：

$$
P(P_{actual} \in [\hat{P}_{lower}, \hat{P}_{upper}]) \geq 1 - \alpha
$$

其中置信水平 $1 - \alpha$ 通常取 90% 或 95%。

### 1.4 需求响应形式化定义

**Def-F-07-54** (需求响应): 需求响应是负荷侧弹性资源的调度机制：

$$
\mathcal{DR} = (D, \pi(t), \Delta P_{DR}(t), R_{DR}, \tau_{response})
$$

其中：

- $D$：可调度负荷集合，分类如下：
  - $D_{ind}$：工业可中断负荷（如电解铝、水泥磨）
  - $D_{comm}$：商业空调、照明
  - $D_{res}$：居民智能家电、EV充电

- $\pi(t)$：动态电价信号，$\pi(t) = f(wholesale\_price, congestion, renewable\_forecast)$

- $\Delta P_{DR}(t)$：负荷调节量，$\Delta P_{DR}(t) = P_{baseline}(t) - P_{actual}(t)$

- $R_{DR}$：需求响应容量，$R_{DR} = \sum_{d \in D} \Delta P_d^{max}$

- $\tau_{response}$：响应时间，不同类型DR资源：
  - 直接负荷控制 (DLC): $\tau < 1s$
  - 可中断负荷 (IL): $\tau < 10min$
  - 价格响应: $\tau < 1h$

**价格弹性模型**:

$$
\epsilon = \frac{\Delta P / P_0}{\Delta \pi / \pi_0} = \frac{(P_1 - P_0) / P_0}{(\pi_1 - \pi_0) / \pi_0}
$$

典型弹性值：

- 居民用电：$\epsilon \in [-0.2, -0.5]$
- 工业用电：$\epsilon \in [-0.3, -0.8]$
- EV充电：$\epsilon \in [-1.0, -3.0]$

### 1.5 电网异常检测形式化定义

**Def-F-07-55** (电网异常检测): 电网异常检测是一个复杂事件处理 (CEP) 问题：

$$
\mathcal{AD} = (E, \mathcal{R}, \mathcal{M}, \tau_{detect})
$$

其中：

- $E$：事件类型集合：
  - $E_{freq}$：频率异常 ($|f - 50Hz| > 0.2Hz$)
  - $E_{volt}$：电压异常 ($|V - V_{nom}| / V_{nom} > 5\%$)
  - $E_{line}$：线路过载 ($I > 0.9 \cdot I_{rated}$)
  - $E_{gen}$：发电机脱网
  - $E_{trans}$：变压器过载

- $\mathcal{R}$：检测规则集合，每条规则 $R_i = (pattern_i, condition_i, action_i)$

- $\mathcal{M}$：异常模式库：
  - 模式1：频率快速下降 $\rightarrow$ 发电短缺
  - 模式2：电压骤降 + 电流突增 $\rightarrow$ 短路故障
  - 模式3：线路过载持续 > 5min $\rightarrow$ 连锁跳闸风险
  - 模式4：功率振荡 $f_{osc} \in [0.2, 2]Hz$ $\rightarrow$ 低频振荡

- $\tau_{detect}$：检测延迟要求，$\tau_{detect} < 1s$ 对紧急故障

---

## 2. 属性推导 (Properties)

### 2.1 预测准确率边界

**Lemma-F-07-50** (预测误差下界): 对于任何负荷预测模型，预测误差的理论下界由信号本身的不可预测性决定：

$$
\mathbb{E}[(P_{actual} - \hat{P})^2] \geq \sigma^2_{irreducible}
$$

其中 $\sigma^2_{irreducible}$ 包含：

- 随机负荷波动
- 突发事件（设备故障、极端天气）
- 测量噪声

**Lemma-F-07-51** (预测精度随提前期衰减): 预测精度随预测提前期 $h$ 增加而衰减：

$$
\text{MAPE}(h) \approx \text{MAPE}_0 \cdot (1 + \alpha \cdot h^{\beta}), \quad \beta \in [0.5, 1.0]
$$

对于典型电力负荷，经验参数：

- 超短期 ($h \leq 15min$): $\beta \approx 0.5$
- 短期 ($h \leq 4h$): $\beta \approx 0.7$
- 日前 ($h = 24h$): $\beta \approx 1.0$

**Thm-F-07-50** (预测精度上界定理): 在给定数据质量 $Q_{data}$ 和模型复杂度 $\mathcal{C}_{model}$ 约束下，可达到的最佳预测精度满足：

$$
\text{MAPE}_{min} = \frac{\sigma_{noise}}{SNR \cdot \sqrt{Q_{data}}} + \epsilon_{model}(\mathcal{C}_{model})
$$

其中：

- $SNR$：信噪比
- $\epsilon_{model}$：模型偏差

### 2.2 实时性保证

**Lemma-F-07-52** (端到端延迟分解): 智能电网实时处理系统的端到端延迟 $L_{total}$ 可分解为：

$$
L_{total} = L_{meter} + L_{network} + L_{ingest} + L_{process} + L_{decision}
$$

各分量典型值：

| 延迟分量 | 典型值 | 优化手段 |
|---------|--------|---------|
| 电表采集 $L_{meter}$ | 1-15s | 高频采样、边缘聚合 |
| 网络传输 $L_{network}$ | 50-200ms | 5G/光纤、就近接入 |
| 数据摄入 $L_{ingest}$ | 10-50ms | Kafka批量优化 |
| 流处理 $L_{process}$ | 100-500ms | Flink优化、增量计算 |
| 决策执行 $L_{decision}$ | 50-500ms | 预计算策略、缓存 |

**Thm-F-07-51** (实时性保证定理): 在Flink流处理系统中，端到端延迟满足：

$$
L_{total} \leq \tau_{max} \quad \text{if} \quad \lambda_{in} \leq \mu_{process} \cdot (1 - p_{checkpoint})
$$

其中：

- $\lambda_{in}$：输入数据率
- $\mu_{process}$：处理能力
- $p_{checkpoint}$：checkpoint开销比例

### 2.3 系统稳定性保证

**Lemma-F-07-53** (功率平衡稳定性条件): 电网频率稳定的必要条件是实时功率平衡：

$$
\left| \sum P_{gen} + \sum P_{renewable} - P_{load} \right| \leq \Delta P_{max}
$$

其中 $\Delta P_{max}$ 由系统惯性决定：

$$
\Delta P_{max} = 2H \cdot f_0 \cdot \frac{df}{dt}_{max}
$$

$H$ 为系统惯性常数 (典型值 2-8s)。

**Thm-F-07-52** (可再生能源渗透率上限): 在给定系统惯性和调节能力下，可再生能源渗透率上限为：

$$
\rho_{RE}^{max} = 1 - \frac{R_{reg} + R_{DR}}{\sigma_{RE} \cdot P_{peak}}
$$

其中：

- $R_{reg}$：传统机组调节能力
- $R_{DR}$：需求响应能力
- $\sigma_{RE}$：可再生能源出力波动标准差

---

## 3. 关系建立 (Relations)

### 3.1 与SCADA系统的关系

**SCADA** (Supervisory Control And Data Acquisition) 是电网运行的基础监控系统：

```
┌─────────────────────────────────────────────────────────────────┐
│                        数据流向关系                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   SCADA RTU ──► SCADA Server ──► Historian                     │
│        │                            │                          │
│        │         实时数据            ▼                          │
│        └────────────────────► Flink Stream Processing          │
│                                        │                       │
│                    高级分析 ◄──────────┤                       │
│                    预测/优化 ◄─────────┘                       │
│                                        │                       │
│                              控制指令 ▼                         │
│                              SCADA Control                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**关系映射**:

| SCADA概念 | Flink映射 | 说明 |
|----------|----------|------|
| RTU/IED | Source Function | 遥测/遥信数据采集 |
| 遥测量 (AI) | DataStream<Double> | 模拟量：电压、电流、功率 |
| 遥信量 (DI) | DataStream<Boolean> | 开关状态、告警信号 |
| 遥控命令 (DO) | Sink Function | 下发控制指令 |
| 扫描周期 | Watermark间隔 | 数据新鲜度保证 |

**数据集成模式**:

- **模式1**: SCADA通过MQTT/Modbus将数据推送到Kafka，Flink订阅处理
- **模式2**: Flink通过OPC-UA客户端主动拉取SCADA数据
- **模式3**: 通过PI System/OSIsoft Historian中间层集成

### 3.2 与EMS能量管理系统的关系

**EMS** (Energy Management System) 是电网调度的决策中枢：

```
┌──────────────────────────────────────────────────────────────┐
│                    EMS-Flink协同架构                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │   EMS核心    │◄──►│  Flink实时   │◄──►│  高级应用服务    │  │
│  │             │    │   分析引擎   │    │                 │  │
│  │ • 状态估计   │    │             │    │ • 负荷预测       │  │
│  │ • 潮流计算   │    │ • 实时聚合   │    │ • 出力预测       │  │
│  │ • 经济调度   │    │ • 异常检测   │    │ • 优化调度       │  │
│  │ • 安全分析   │    │ • CEP处理   │    │ • 市场出清       │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
│         ▲                                          │         │
│         └────────────── 模型更新 ◄─────────────────┘         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**功能分工**:

| 功能 | EMS (传统) | Flink (实时增强) |
|------|-----------|-----------------|
| 数据采集 | 秒级 (4-10s) | 毫秒级 (100ms) |
| 状态估计 | 分钟级周期 | 连续实时估计 |
| 负荷预测 | 日前/小时前 | 分钟级滚动预测 |
| 安全分析 | N-1离线分析 | 实时N-k风险评估 |
| 优化调度 | 15分钟经济调度 | 实时AGC辅助决策 |

### 3.3 与AMI高级计量架构的关系

**AMI** (Advanced Metering Infrastructure) 提供用户侧细粒度数据：

```
┌──────────────────────────────────────────────────────────────┐
│                   AMI数据集成架构                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   智能电表 ──► 采集器 ──► 集中器 ──► 主站系统 ──► Kafka    │
│      │                                              │        │
│      │          15分钟/5分钟/1分钟 负荷曲线           │        │
│      ▼                                              ▼        │
│   ┌────────┐                                   ┌────────┐   │
│   │ 负荷特性 │◄────────────────────────────────►│ Flink  │   │
│   │ 分析   │      用户行为模式/异常用电检测       │ 处理   │   │
│   └────────┘                                   └────────┘   │
│                                                      │        │
│                                                      ▼        │
│                                               ┌──────────┐   │
│                                               │ 需求响应  │   │
│                                               │ 控制策略  │   │
│                                               └──────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**AMI数据特征**:

| 数据类型 | 采集频率 | 数据量 | 用途 |
|---------|---------|-------|------|
| 负荷曲线 | 15分钟 | ~100TB/年 | 负荷预测、计费 |
| 瞬时量测 | 1分钟 | ~1PB/年 | 实时分析 |
| 事件记录 | 触发式 | ~10GB/年 | 故障分析 |
| 告警信息 | 实时 | ~1GB/年 | 异常检测 |

### 3.4 与电力市场的关系

**电力市场与实时优化的闭环**:

```
┌──────────────────────────────────────────────────────────────────┐
│                     市场-运行协同优化                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│   │   日前市场   │─────►│   日内市场   │─────►│   实时市场   │     │
│   │  (D-1)     │      │  (H-4)     │      │  (5min)    │     │
│   └──────┬──────┘      └──────┬──────┘      └──────┬──────┘     │
│          │                    │                    │             │
│          ▼                    ▼                    ▼             │
│   ┌──────────────────────────────────────────────────────┐      │
│   │              Flink 预测与优化引擎                     │      │
│   │  • 价格预测 ◄── 负荷预测 ◄── 出力预测                 │      │
│   │  • 投标策略优化                                       │      │
│   │  • 实时平衡优化                                       │      │
│   └──────────────────────────────────────────────────────┘      │
│                              │                                   │
│                              ▼                                   │
│   ┌──────────────────────────────────────────────────────┐      │
│   │                 结算与评估                            │      │
│   └──────────────────────────────────────────────────────┘      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. 论证过程 (Argumentation)

### 4.1 实时优化必要性论证

**论证**: 为什么需要毫秒/秒级的实时优化？

**论据1: 可再生能源波动性**

风电出力可在数分钟内变化数百MW：

- 风速变化 1m/s $\rightarrow$ 出力变化 ~30% (立方关系)
- 云层遮挡 $\rightarrow$ 光伏出力骤降 70% 仅需数秒

**论据2: 电网频率稳定要求**

| 频率偏差 | 允许时间 | 后果 |
|---------|---------|------|
| $\pm 0.2Hz$ | 持续 | 正常运行 |
| $\pm 0.5Hz$ | < 10min | 启动备用 |
| $\pm 1.0Hz$ | < 2min | 切负荷 |
| $\pm 2.0Hz$ | 立即 | 系统崩溃 |

**论据3: 经济性考量**

实时优化 vs 传统调度的成本对比：

| 场景 | 传统调度成本 | 实时优化成本 | 节省 |
|------|------------|------------|------|
| 备用容量配置 | 100% | 70% | 30% |
| 弃风弃光 | 基准 | -35% | 35% |
| 偏差考核 | 基准 | -40% | 40% |

**结论**: 实时优化是应对高比例可再生能源并网的必然选择。

### 4.2 可再生能源波动处理论证

**挑战**: 如何处理45%可再生能源的高波动性？

**多时间尺度协调策略**:

```
时间尺度        波动类型              应对手段
─────────────────────────────────────────────────────────
秒级-分钟级     云遮/阵风            电池储能 + 需求响应
分钟级-小时级   天气变化             机组调节 + 备用调度
小时级-日前     日前预测偏差         日内市场 + 跨区互济
多日前          气候模式             季节性储能 + 燃料储备
```

**波动平抑能力矩阵**:

| 资源类型 | 响应速度 | 调节范围 | 持续时间 | 成本 |
|---------|---------|---------|---------|------|
| 电池储能 | < 1s | ±100MW | 1-4h | 高 |
| 需求响应 | 1-10min | ±500MW | 1-4h | 低 |
| 燃气机组 | 5-10min | ±1000MW | 持续 | 中 |
| 抽蓄电站 | 10s | ±2000MW | 6-8h | 低 |

### 4.3 动态定价策略论证

**论证**: 动态定价如何促进电网优化？

**价格信号设计**:

$$
\pi(t) = \pi_{base} + \pi_{energy}(t) + \pi_{congestion}(t) + \pi_{renewable}(t)
$$

其中：

- $\pi_{energy}$：边际发电成本
- $\pi_{congestion}$：线路阻塞成本
- $\pi_{renewable}$：可再生能源溢价（可为负值）

**不同时段定价策略**:

| 时段类型 | 典型时间 | 电价倍数 | 目的 |
|---------|---------|---------|------|
| 峰时 | 9:00-12:00, 18:00-22:00 | 2.0-3.0x | 抑制高峰负荷 |
| 平时 | 8:00-9:00, 12:00-18:00 | 1.0x | 正常引导 |
| 谷时 | 22:00-8:00 | 0.3-0.5x | 鼓励填谷 |
| 负电价 | 可再生大发时段 | -0.1-0x | 消纳富余电力 |

---

## 5. 工程论证 (Engineering Argument)

### 5.1 预测算法选型论证

**负荷预测算法对比**:

| 算法 | 短期精度 | 训练成本 | 推断延迟 | 适用场景 |
|------|---------|---------|---------|---------|
| ARIMA | 85-90% | 低 | < 1ms | 基线预测 |
| Prophet | 88-92% | 低 | < 5ms | 含节假日效应 |
| LSTM | 92-96% | 高 | 5-20ms | 复杂模式 |
| XGBoost | 90-94% | 中 | 1-5ms | 特征丰富场景 |
| Transformer | 94-97% | 很高 | 10-50ms | 超短期预测 |

**推荐方案**: 组合预测 (Ensemble)

```
┌─────────────────────────────────────────────────────┐
│                  组合预测架构                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│   输入数据 ──► ┌─────────┐                          │
│              │ 特征工程 │                          │
│              └────┬────┘                          │
│                   │                                 │
│       ┌───────────┼───────────┐                     │
│       ▼           ▼           ▼                     │
│   ┌────────┐  ┌────────┐  ┌────────┐               │
│   │ Prophet │  │ LSTM  │  │ XGBoost│               │
│   └────┬───┘  └───┬────┘  └───┬────┘               │
│        │          │          │                      │
│        └──────────┼──────────┘                      │
│                   ▼                                 │
│              ┌─────────┐                            │
│              │ 加权融合 │  w₁·P₁ + w₂·P₂ + w₃·P₃   │
│              └────┬────┘                            │
│                   ▼                                 │
│              最终预测结果                            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**权重自适应调整**:

$$
w_i(t) = \frac{\exp(-\beta \cdot \text{MAPE}_i(t))}{\sum_j \exp(-\beta \cdot \text{MAPE}_j(t))}
$$

### 5.2 状态后端选型论证

**状态后端对比**:

| 特性 | MemoryStateBackend | FsStateBackend | RocksDBStateBackend |
|------|-------------------|----------------|---------------------|
| 状态容量 | 小 (JVM Heap) | 中 (本地磁盘) | 大 (本地磁盘+内存) |
|  checkpoint速度 | 快 | 中 | 慢 |
| 恢复速度 | 快 | 中 | 中 |
| 推荐状态大小 | < 100MB | < 1GB | > 1GB |
| 增量checkpoint | 不支持 | 支持 | 支持 |

**智能电网场景选型**:

**场景1: 实时异常检测**

- 状态规模：~100MB（滑动窗口状态）
- 推荐：MemoryStateBackend
- 理由：超低延迟，状态可重建

**场景2: 负荷预测模型状态**

- 状态规模：~1-10GB（模型参数、历史特征）
- 推荐：RocksDBStateBackend + 增量checkpoint
- 理由：大状态支持，增量checkpoint减少开销

**配置建议**:

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
// RocksDB配置优化
RocksDBStateBackend rocksDbBackend = new RocksDBStateBackend(
    "hdfs://checkpoint/grid-realtime",
    true  // 启用增量checkpoint
);

// 调优参数
rocksDbBackend.setPredefinedOptions(
    PredefinedOptions.FLASH_SSD_OPTIMIZED
);

env.setStateBackend(rocksDbBackend);
env.enableCheckpointing(60000);  // 1分钟checkpoint间隔
env.getCheckpointConfig().setCheckpointTimeout(300000);
```

### 5.3 时间序列数据库选型论证

**TSDB对比**:

| 数据库 | 写入吞吐 | 查询性能 | 压缩率 | 扩展性 | 适用场景 |
|-------|---------|---------|-------|-------|---------|
| InfluxDB | 高 | 高 | 10:1 | 中 | 中小规模 |
| TimescaleDB | 高 | 很高 | 5:1 | 高 | SQL生态 |
| TDengine | 很高 | 很高 | 10:1 | 高 | 物联网 |
| IoTDB | 很高 | 高 | 15:1 | 高 | 工业时序 |
| ClickHouse | 很高 | 很高 | 5:1 | 很高 | OLAP分析 |

**推荐方案**: TDengine + Flink集成

**理由**:

1. 专为IoT设计，支持海量设备写入
2. 超级表概念匹配AMI电表模型
3. 边缘-云协同架构
4. Flink Connector成熟

---

## 6. 实例验证 (Examples)

### 6.1 案例背景

**客户概况**: 某区域电网运营商

| 指标 | 数值 |
|------|------|
| 服务用户 | 1000万+ |
| 最大负荷 | 15,000 MW |
| 年用电量 | 80 TWh |
| 可再生能源占比 | 45% |
| 风电装机 | 3,500 MW |
| 光伏装机 | 2,800 MW |
| 智能电表 | 1000万+ |

**业务挑战**:

1. **供需平衡困难**: 可再生能源出力波动大，传统调度难以应对
2. **弃风弃光严重**: 高峰期弃电率曾达 20%+
3. **电网稳定性风险**: 频率偏差事件月均 15+ 次
4. **预测精度不足**: 传统预测方法准确率仅 80-85%

**技术目标**:

| 目标项 | 目标值 |
|-------|-------|
| 负荷预测准确率 | ≥ 95% |
| 可再生能源预测准确率 | ≥ 90% |
| 弃风弃光率降低 | ≥ 30% |
| 峰值负荷削减 | ≥ 10% |
| 故障检测时间 | < 5秒 |

### 6.2 完整Flink实现代码

#### 6.2.1 项目依赖 (pom.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.gridoperator</groupId>
    <artifactId>smart-grid-realtime</artifactId>
    <version>1.0.0</version>

    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <flink.version>1.18.0</flink.version>
        <scala.binary.version>2.12</scala.binary.version>
    </properties>

    <dependencies>
        <!-- Flink Core -->
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-streaming-java</artifactId>
            <version>${flink.version}</version>
        </dependency>

        <!-- Flink CEP -->
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-cep</artifactId>
            <version>${flink.version}</version>
        </dependency>

        <!-- Flink ML -->
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-ml-core</artifactId>
            <version>${flink.version}</version>
        </dependency>

        <!-- Kafka Connector -->
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-connector-kafka</artifactId>
            <version>${flink.version}</version>
        </dependency>

        <!-- Redis Connector -->
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-connector-redis</artifactId>
            <version>1.1.0</version>
        </dependency>

        <!-- TDengine Connector -->
        <dependency>
            <groupId>com.taosdata.jdbc</groupId>
            <artifactId>taos-jdbcdriver</artifactId>
            <version>3.2.7</version>
        </dependency>

        <!-- DL4J for LSTM -->
        <dependency>
            <groupId>org.deeplearning4j</groupId>
            <artifactId>deeplearning4j-core</artifactId>
            <version>1.0.0-M2.1</version>
        </dependency>

        <!-- Jackson for JSON -->
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.15.2</version>
        </dependency>
    </dependencies>
</project>
```

#### 6.2.2 核心数据模型

```java
package com.gridoperator.model;

import java.io.Serializable;
import java.time.Instant;

/**
 * 智能电表数据点 (AMI Meter Reading)
 */
public class MeterReading implements Serializable {
    private static final long serialVersionUID = 1L;

    private String meterId;           // 电表ID
    private String userType;          // 用户类型: RESIDENTIAL/COMMERCIAL/INDUSTRIAL
    private String regionCode;        // 区域编码
    private Instant timestamp;        // 时间戳
    private double activePower;       // 有功功率 (kW)
    private double reactivePower;     // 无功功率 (kVAR)
    private double voltage;           // 电压 (V)
    private double current;           // 电流 (A)
    private double powerFactor;       // 功率因数
    private double frequency;         // 频率 (Hz)
    private ReadingQuality quality;   // 数据质量

    // 构造函数、Getter/Setter
    public MeterReading() {}

    public MeterReading(String meterId, Instant timestamp, double activePower) {
        this.meterId = meterId;
        this.timestamp = timestamp;
        this.activePower = activePower;
    }

    // Getters and Setters...
    public String getMeterId() { return meterId; }
    public void setMeterId(String meterId) { this.meterId = meterId; }

    public Instant getTimestamp() { return timestamp; }
    public void setTimestamp(Instant timestamp) { this.timestamp = timestamp; }

    public double getActivePower() { return activePower; }
    public void setActivePower(double activePower) { this.activePower = activePower; }

    public String getRegionCode() { return regionCode; }
    public void setRegionCode(String regionCode) { this.regionCode = regionCode; }

    public ReadingQuality getQuality() { return quality; }
    public void setQuality(ReadingQuality quality) { this.quality = quality; }

    public double getVoltage() { return voltage; }
    public void setVoltage(double voltage) { this.voltage = voltage; }

    public double getFrequency() { return frequency; }
    public void setFrequency(double frequency) { this.frequency = frequency; }
}

/**
 * 数据质量枚举
 */
public enum ReadingQuality {
    GOOD,           // 良好
    SUSPECT,        // 可疑
    BAD,            // 错误
    MISSING,        // 缺失
    SUBSTITUTED     // 插值替代
}

/**
 * 气象数据
 */
public class WeatherData implements Serializable {
    private static final long serialVersionUID = 1L;

    private String stationId;
    private Instant timestamp;
    private double temperature;       // 温度 (°C)
    private double humidity;          // 湿度 (%)
    private double windSpeed;         // 风速 (m/s)
    private double windDirection;     // 风向 (°)
    private double solarIrradiance;   // 太阳辐照度 (W/m²)
    private double pressure;          // 气压 (hPa)
    private String regionCode;

    // 构造函数、Getter/Setter...
    public WeatherData() {}

    public WeatherData(String stationId, Instant timestamp,
                       double temperature, double windSpeed, double solarIrradiance) {
        this.stationId = stationId;
        this.timestamp = timestamp;
        this.temperature = temperature;
        this.windSpeed = windSpeed;
        this.solarIrradiance = solarIrradiance;
    }

    // Getters and Setters...
    public String getStationId() { return stationId; }
    public void setStationId(String stationId) { this.stationId = stationId; }

    public Instant getTimestamp() { return timestamp; }
    public void setTimestamp(Instant timestamp) { this.timestamp = timestamp; }

    public double getTemperature() { return temperature; }
    public void setTemperature(double temperature) { this.temperature = temperature; }

    public double getWindSpeed() { return windSpeed; }
    public void setWindSpeed(double windSpeed) { this.windSpeed = windSpeed; }

    public double getSolarIrradiance() { return solarIrradiance; }
    public void setSolarIrradiance(double solarIrradiance) {
        this.solarIrradiance = solarIrradiance;
    }

    public String getRegionCode() { return regionCode; }
    public void setRegionCode(String regionCode) { this.regionCode = regionCode; }
}

/**
 * 可再生能源出力数据
 */
public class RenewableOutput implements Serializable {
    private static final long serialVersionUID = 1L;

    private String plantId;
    private String plantType;         // WIND/SOLAR
    private Instant timestamp;
    private double actualOutput;      // 实际出力 (MW)
    private double forecastOutput;    // 预测出力 (MW)
    private double capacity;          // 装机容量 (MW)
    private double availability;      // 可用率

    // Getters and Setters...
}

/**
 * 预测结果
 */
public class ForecastResult implements Serializable {
    private static final long serialVersionUID = 1L;

    private String forecastType;      // LOAD/SOLAR/WIND/PRICE
    private String regionCode;
    private Instant timestamp;        // 预测生成时间
    private Instant targetTime;       // 预测目标时间
    private double predictedValue;    // 预测值
    private double lowerBound;        // 置信区间下限
    private double upperBound;        // 置信区间上限
    private double confidence;        // 置信度
    private int horizonMinutes;       // 预测提前期(分钟)

    // Getters and Setters...
}

/**
 * 电网异常告警
 */
public class GridAnomaly implements Serializable {
    private static final long serialVersionUID = 1L;

    private String anomalyId;
    private AnomalyType type;
    private AnomalySeverity severity;
    private Instant timestamp;
    private String location;
    private String description;
    private double value;
    private double threshold;
    private String suggestedAction;

    // Getters and Setters...
}

public enum AnomalyType {
    FREQUENCY_DEVIATION,
    VOLTAGE_VIOLATION,
    LINE_OVERLOAD,
    GENERATOR_TRIP,
    POWER_OSCILLATION,
    RENEWABLE_CUTOUT
}

public enum AnomalySeverity {
    INFO, WARNING, CRITICAL, EMERGENCY
}
```

#### 6.2.3 主应用程序

```java
package com.gridoperator;

import com.gridoperator.model.*;
import com.gridoperator.source.*;
import com.gridoperator.process.*;
import com.gridoperator.sink.*;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.restartstrategy.RestartStrategies;
import org.apache.flink.api.common.time.Time;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.cep.CEP;
import org.apache.flink.cep.Pattern;
import org.apache.flink.cep.PatternSelectFunction;
import org.apache.flink.cep.pattern.conditions.SimpleCondition;
import org.apache.flink.contrib.streaming.state.EmbeddedRocksDBStateBackend;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;
import org.apache.flink.api.common.serialization.SimpleStringSchema;

import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.Properties;

public class SmartGridRealtimeApplication {

    public static void main(String[] args) throws Exception {
        // 参数解析
        ParameterTool params = ParameterTool.fromArgs(args);

        // 创建执行环境
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // 配置状态后端
        EmbeddedRocksDBStateBackend rocksDbBackend =
            new EmbeddedRocksDBStateBackend(true);
        env.setStateBackend(rocksDbBackend);

        // Checkpoint配置
        env.enableCheckpointing(60000);  // 1分钟
        env.getCheckpointConfig().setCheckpointTimeout(300000);
        env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30000);

        // 故障恢复策略
        env.setRestartStrategy(RestartStrategies.fixedDelayRestart(
            3,                    // 最大重启次数
            Time.seconds(10)      // 重启间隔
        ));

        // 配置并行度
        env.setParallelism(params.getInt("parallelism", 8));

        // ==================== 数据源配置 ====================

        // Kafka配置
        Properties kafkaProps = new Properties();
        kafkaProps.setProperty("bootstrap.servers",
            params.get("kafka.servers", "kafka:9092"));
        kafkaProps.setProperty("group.id", "smart-grid-processor");

        // 1. 智能电表数据流
        FlinkKafkaConsumer<String> meterConsumer = new FlinkKafkaConsumer<>(
            "ami-meter-readings",
            new SimpleStringSchema(),
            kafkaProps
        );
        meterConsumer.setStartFromLatest();

        DataStream<MeterReading> meterStream = env
            .addSource(meterConsumer)
            .name("AMI Meter Readings")
            .map(new MeterReadingParser())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy
                    .<MeterReading>forBoundedOutOfOrderness(
                        Duration.ofSeconds(30))
                    .withIdleness(Duration.ofMinutes(5))
            );

        // 2. 气象数据流
        FlinkKafkaConsumer<String> weatherConsumer = new FlinkKafkaConsumer<>(
            "weather-data",
            new SimpleStringSchema(),
            kafkaProps
        );

        DataStream<WeatherData> weatherStream = env
            .addSource(weatherConsumer)
            .name("Weather Data")
            .map(new WeatherDataParser())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy
                    .<WeatherData>forBoundedOutOfOrderness(
                        Duration.ofMinutes(2))
            );

        // 3. 可再生能源出力数据
        FlinkKafkaConsumer<String> renewableConsumer = new FlinkKafkaConsumer<>(
            "renewable-output",
            new SimpleStringSchema(),
            kafkaProps
        );

        DataStream<RenewableOutput> renewableStream = env
            .addSource(renewableConsumer)
            .name("Renewable Output")
            .map(new RenewableOutputParser())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy
                    .<RenewableOutput>forBoundedOutOfOrderness(
                        Duration.ofSeconds(15))
            );

        // ==================== 数据处理管道 ====================

        // 1. 实时负荷聚合 (按区域、时间窗口)
        DataStream<RegionalLoad> regionalLoadStream = meterStream
            .keyBy(MeterReading::getRegionCode)
            .window(TumblingEventTimeWindows.of(Time.minutes(5)))
            .aggregate(new LoadAggregationFunction())
            .name("Regional Load Aggregation");

        // 2. 负荷预测 (连接气象数据)
        DataStream<ForecastResult> loadForecastStream = regionalLoadStream
            .keyBy(RegionalLoad::getRegionCode)
            .connect(weatherStream.keyBy(WeatherData::getRegionCode))
            .process(new LoadForecastProcessFunction())
            .name("Load Forecasting");

        // 3. 可再生能源出力预测
        DataStream<ForecastResult> renewableForecastStream = renewableStream
            .keyBy(RenewableOutput::getPlantId)
            .connect(weatherStream.keyBy(WeatherData::getRegionCode))
            .process(new RenewableForecastProcessFunction())
            .name("Renewable Forecasting");

        // 4. 电网异常检测 (CEP)
        DataStream<GridAnomaly> anomalyStream = createAnomalyDetectionStream(
            regionalLoadStream, renewableStream, meterStream);

        // 5. 需求响应管理
        DataStream<DRSignal> drSignalStream = loadForecastStream
            .keyBy(ForecastResult::getRegionCode)
            .process(new DemandResponseProcessFunction())
            .name("Demand Response Management");

        // 6. 动态定价计算
        DataStream<PricingSignal> pricingStream = loadForecastStream
            .keyBy(ForecastResult::getRegionCode)
            .connect(renewableForecastStream.keyBy(ForecastResult::getRegionCode))
            .process(new DynamicPricingProcessFunction())
            .name("Dynamic Pricing");

        // ==================== 数据输出 ====================

        // 输出到Kafka
        FlinkKafkaProducer<String> forecastProducer = new FlinkKafkaProducer<>(
            "forecast-results",
            new SimpleStringSchema(),
            kafkaProps
        );

        FlinkKafkaProducer<String> anomalyProducer = new FlinkKafkaProducer<>(
            "grid-anomalies",
            new SimpleStringSchema(),
            kafkaProps
        );

        loadForecastStream
            .map(new ForecastResultSerializer())
            .addSink(forecastProducer)
            .name("Forecast Output");

        renewableForecastStream
            .map(new ForecastResultSerializer())
            .addSink(forecastProducer)
            .name("Renewable Forecast Output");

        anomalyStream
            .map(new AnomalySerializer())
            .addSink(anomalyProducer)
            .name("Anomaly Alerts");

        // 输出到TDengine
        regionalLoadStream
            .addSink(new TDengineLoadSink(params))
            .name("TDengine Load Storage");

        // 输出到Redis (实时查询)
        loadForecastStream
            .addSink(new RedisForecastSink(params))
            .name("Redis Forecast Cache");

        // 执行
        env.execute("Smart Grid Real-time Energy Management");
    }

    /**
     * 创建异常检测流 (CEP)
     */
    private static DataStream<GridAnomaly> createAnomalyDetectionStream(
            DataStream<RegionalLoad> loadStream,
            DataStream<RenewableOutput> renewableStream,
            DataStream<MeterReading> meterStream) {

        // 频率异常检测模式
        Pattern<MeterReading, ?> frequencyAnomalyPattern = Pattern
            .<MeterReading>begin("freq_deviation_start")
            .where(new SimpleCondition<MeterReading>() {
                @Override
                public boolean filter(MeterReading reading) {
                    double freq = reading.getFrequency();
                    return Math.abs(freq - 50.0) > 0.2;  // 频率偏差>0.2Hz
                }
            })
            .next("freq_deviation_continue")
            .where(new SimpleCondition<MeterReading>() {
                @Override
                public boolean filter(MeterReading reading) {
                    double freq = reading.getFrequency();
                    return Math.abs(freq - 50.0) > 0.2;
                }
            })
            .within(Time.seconds(5));

        // 应用CEP模式
        DataStream<GridAnomaly> frequencyAnomalies = CEP.pattern(
                meterStream.keyBy(MeterReading::getRegionCode),
                frequencyAnomalyPattern
            )
            .process(new PatternSelectFunction<MeterReading, GridAnomaly>() {
                @Override
                public GridAnomaly select(Map<String, List<MeterReading>> pattern) {
                    MeterReading first = pattern.get("freq_deviation_start").get(0);
                    return new GridAnomaly(
                        java.util.UUID.randomUUID().toString(),
                        AnomalyType.FREQUENCY_DEVIATION,
                        Math.abs(first.getFrequency() - 50.0) > 0.5 ?
                            AnomalySeverity.CRITICAL : AnomalySeverity.WARNING,
                        Instant.now(),
                        first.getRegionCode(),
                        "Frequency deviation detected: " + first.getFrequency() + "Hz",
                        first.getFrequency(),
                        50.0,
                        "Check generator dispatch and renewable output"
                    );
                }
            });

        // 线路过载检测 (基于区域负荷)
        Pattern<RegionalLoad, ?> overloadPattern = Pattern
            .<RegionalLoad>begin("high_load")
            .where(new SimpleCondition<RegionalLoad>() {
                @Override
                public boolean filter(RegionalLoad load) {
                    return load.getLoadMw() > load.getCapacityMw() * 0.85;
                }
            })
            .timesOrMore(3)
            .within(Time.minutes(5));

        DataStream<GridAnomaly> overloadAnomalies = CEP.pattern(
                loadStream.keyBy(RegionalLoad::getRegionCode),
                overloadPattern
            )
            .process(new PatternSelectFunction<RegionalLoad, GridAnomaly>() {
                @Override
                public GridAnomaly select(Map<String, List<RegionalLoad>> pattern) {
                    RegionalLoad last = pattern.get("high_load").get(
                        pattern.get("high_load").size() - 1);
                    double utilization = last.getLoadMw() / last.getCapacityMw() * 100;
                    return new GridAnomaly(
                        java.util.UUID.randomUUID().toString(),
                        AnomalyType.LINE_OVERLOAD,
                        utilization > 95 ? AnomalySeverity.EMERGENCY :
                            AnomalySeverity.CRITICAL,
                        Instant.now(),
                        last.getRegionCode(),
                        String.format("Line overload: %.1f%% utilization", utilization),
                        utilization,
                        85.0,
                        "Activate demand response or reconfigure network"
                    );
                }
            });

        // 合并所有异常流
        return frequencyAnomalies
            .union(overloadAnomalies);
    }
}
```

### 6.3 CEP电网异常检测实现

```java
package com.gridoperator.cep;

import com.gridoperator.model.*;
import org.apache.flink.cep.Pattern;
import org.apache.flink.cep.PatternSelectFunction;
import org.apache.flink.cep.nfa.aftermatch.AfterMatchSkipStrategy;
import org.apache.flink.cep.pattern.conditions.IterativeCondition;
import org.apache.flink.cep.pattern.conditions.SimpleCondition;
import org.apache.flink.streaming.api.windowing.time.Time;

import java.util.List;
import java.util.Map;

/**
 * 电网异常检测模式库
 */
public class GridAnomalyPatterns {

    /**
     * 模式1: 电压骤降 (Voltage Sag)
     * 检测条件: 电压在100ms内下降超过10%
     */
    public static Pattern<MeterReading, ?> voltageSagPattern() {
        return Pattern.<MeterReading>begin("normal_voltage")
            .where(new SimpleCondition<MeterReading>() {
                @Override
                public boolean filter(MeterReading r) {
                    return r.getVoltage() >= 0.9 * 220;  // 正常电压
                }
            })
            .next("voltage_drop")
            .where(new SimpleCondition<MeterReading>() {
                @Override
                public boolean filter(MeterReading r) {
                    return r.getVoltage() < 0.9 * 220;  // 电压下降
                }
            })
            .within(Time.milliseconds(100));
    }

    /**
     * 模式2: 频率崩溃连锁检测
     * 检测条件: 频率连续下降超过3个采样点
     */
    public static Pattern<MeterReading, ?> frequencyCollapsePattern() {
        return Pattern.<MeterReading>begin("freq_drop_1")
            .where(new SimpleCondition<MeterReading>() {
                @Override
                public boolean filter(MeterReading r) {
                    return r.getFrequency() < 49.8;
                }
            })
            .next("freq_drop_2")
            .where(new IterativeCondition<MeterReading>() {
                private MeterReading prev;

                @Override
                public boolean filter(MeterReading r, Context<MeterReading> ctx) {
                    if (prev == null) {
                        prev = r;
                        return r.getFrequency() < 49.8;
                    }
                    boolean descending = r.getFrequency() < prev.getFrequency();
                    prev = r;
                    return descending && r.getFrequency() < 49.8;
                }
            })
            .next("freq_drop_3")
            .where(new SimpleCondition<MeterReading>() {
                @Override
                public boolean filter(MeterReading r) {
                    return r.getFrequency() < 49.5;
                }
            })
            .within(Time.seconds(3));
    }

    /**
     * 模式3: 功率振荡检测 (低频振荡)
     * 检测条件: 功率在0.2-2Hz范围内振荡
     */
    public static Pattern<MeterReading, ?> powerOscillationPattern() {
        return Pattern.<MeterReading>begin("oscillation_start")
            .where(new SimpleCondition<MeterReading>() {
                @Override
                public boolean filter(MeterReading r) {
                    return true;  // 记录起始点
                }
            })
            .followedBy("peak_1")
            .where(new IterativeCondition<MeterReading>() {
                @Override
                public boolean filter(MeterReading r, Context<MeterReading> ctx) {
                    // 检测峰值需要比较历史值
                    Iterable<MeterReading> prevEvents = ctx.getEventsForPattern("oscillation_start");
                    double avgPower = 0;
                    int count = 0;
                    for (MeterReading e : prevEvents) {
                        avgPower += e.getActivePower();
                        count++;
                    }
                    if (count > 0) avgPower /= count;
                    return r.getActivePower() > avgPower * 1.05;  // 高于平均5%
                }
            })
            .followedBy("valley_1")
            .where(new IterativeCondition<MeterReading>() {
                @Override
                public boolean filter(MeterReading r, Context<MeterReading> ctx) {
                    Iterable<MeterReading> peaks = ctx.getEventsForPattern("peak_1");
                    double lastPeak = 0;
                    for (MeterReading e : peaks) {
                        lastPeak = e.getActivePower();
                    }
                    return r.getActivePower() < lastPeak * 0.95;  // 比峰值低5%
                }
            })
            .followedBy("peak_2")
            .where(new IterativeCondition<MeterReading>() {
                @Override
                public boolean filter(MeterReading r, Context<MeterReading> ctx) {
                    Iterable<MeterReading> valleys = ctx.getEventsForPattern("valley_1");
                    double lastValley = Double.MAX_VALUE;
                    for (MeterReading e : valleys) {
                        lastValley = Math.min(lastValley, e.getActivePower());
                    }
                    return r.getActivePower() > lastValley * 1.05;
                }
            })
            .within(Time.seconds(10));  // 0.2-2Hz对应0.5-5s周期
    }

    /**
     * 模式4: 可再生能源大规模脱网
     */
    public static Pattern<RenewableOutput, ?> renewableTripPattern() {
        return Pattern.<RenewableOutput>begin("normal_output")
            .where(new SimpleCondition<RenewableOutput>() {
                @Override
                public boolean filter(RenewableOutput r) {
                    return r.getActualOutput() > r.getCapacity() * 0.1;  // 正常发电
                }
            })
            .next("sudden_drop")
            .where(new SimpleCondition<RenewableOutput>() {
                @Override
                public boolean filter(RenewableOutput r) {
                    return r.getActualOutput() < r.getCapacity() * 0.1;  // 出力骤降
                }
            })
            .within(Time.seconds(5));
    }

    /**
     * 模式5: 变压器过载预警
     */
    public static Pattern<RegionalLoad, ?> transformerOverloadPattern() {
        return Pattern.<RegionalLoad>begin("high_load_start")
            .where(new SimpleCondition<RegionalLoad>() {
                @Override
                public boolean filter(RegionalLoad r) {
                    return r.getLoadMw() / r.getCapacityMw() > 0.8;
                }
            })
            .timesOrMore(6)  // 持续30分钟 (5分钟窗口)
            .within(Time.minutes(30));
    }

    /**
     * 异常处理选择函数
     */
    public static class AnomalySelector implements PatternSelectFunction<MeterReading, GridAnomaly> {
        private final AnomalyType type;
        private final String description;

        public AnomalySelector(AnomalyType type, String description) {
            this.type = type;
            this.description = description;
        }

        @Override
        public GridAnomaly select(Map<String, List<MeterReading>> pattern) {
            MeterReading event = pattern.values().iterator().next().get(0);

            AnomalySeverity severity = determineSeverity(type, event);
            String action = determineAction(type);

            return new GridAnomaly(
                java.util.UUID.randomUUID().toString(),
                type,
                severity,
                Instant.now(),
                event.getRegionCode(),
                description + " at " + event.getMeterId(),
                event.getActivePower(),
                0.0,  // 阈值根据具体类型确定
                action
            );
        }

        private AnomalySeverity determineSeverity(AnomalyType type, MeterReading event) {
            switch (type) {
                case FREQUENCY_DEVIATION:
                    double freqDev = Math.abs(event.getFrequency() - 50.0);
                    if (freqDev > 1.0) return AnomalySeverity.EMERGENCY;
                    if (freqDev > 0.5) return AnomalySeverity.CRITICAL;
                    return AnomalySeverity.WARNING;
                case VOLTAGE_VIOLATION:
                    double voltDev = Math.abs(event.getVoltage() - 220.0) / 220.0;
                    if (voltDev > 0.15) return AnomalySeverity.CRITICAL;
                    return AnomalySeverity.WARNING;
                default:
                    return AnomalySeverity.WARNING;
            }
        }

        private String determineAction(AnomalyType type) {
            switch (type) {
                case FREQUENCY_DEVIATION:
                    return "Activate AGC, check generator dispatch";
                case VOLTAGE_VIOLATION:
                    return "Adjust reactive power compensation";
                case LINE_OVERLOAD:
                    return "Reconfigure network topology, activate DR";
                case POWER_OSCILLATION:
                    return "Enable PSS, reduce tie-line flow";
                default:
                    return "Monitor and investigate";
            }
        }
    }
}
```

### 6.4 实时负荷预测实现

```java
package com.gridoperator.ml;

import com.gridoperator.model.*;
import org.apache.flink.api.common.state.*;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.co.KeyedCoProcessFunction;
import org.apache.flink.util.Collector;

import java.time.Duration;
import java.time.Instant;
import java.util.*;

import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;


/**
 * 实时负荷预测处理函数
 * 使用LSTM模型结合Prophet进行组合预测
 */
public class LoadForecastProcessFunction extends KeyedCoProcessFunction<
        String, RegionalLoad, WeatherData, ForecastResult> {

    // 状态定义
    private ValueState<LSTMModelState> modelState;
    private ListState<LoadHistoryPoint> loadHistory;
    private ValueState<WeatherData> latestWeather;
    private MapState<String, Double> hourlyPatterns;

    // 配置参数
    private static final int HISTORY_LENGTH = 96;  // 24小时 * 15分钟
    private static final int[] FORECAST_HORIZONS = {1, 4, 12, 24, 96};  // 15min, 1h, 3h, 6h, 24h
    private static final double LEARNING_RATE = 0.001;

    @Override
    public void open(Configuration parameters) {
        StateTtlConfig ttlConfig = StateTtlConfig
            .newBuilder(Duration.ofHours(48))
            .setUpdateType(StateTtlConfig.UpdateType.OnCreateAndWrite)
            .setStateVisibility(StateTtlConfig.StateVisibility.NeverReturnExpired)
            .build();

        modelState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("lstm-model", LSTMModelState.class));

        loadHistory = getRuntimeContext().getListState(
            new ListStateDescriptor<>("load-history", LoadHistoryPoint.class));

        latestWeather = getRuntimeContext().getState(
            new ValueStateDescriptor<>("latest-weather", WeatherData.class));

        hourlyPatterns = getRuntimeContext().getMapState(
            new MapStateDescriptor<>("hourly-patterns", String.class, Double.class));
    }

    @Override
    public void processElement1(RegionalLoad load, Context ctx, Collector<ForecastResult> out)
            throws Exception {

        // 更新历史负荷状态
        loadHistory.add(new LoadHistoryPoint(
            load.getTimestamp(),
            load.getLoadMw(),
            load.getRegionCode()
        ));

        // 维护历史窗口大小
        trimHistory();

        // 获取最新气象数据
        WeatherData weather = latestWeather.value();
        if (weather == null) {
            return;  // 等待气象数据
        }

        // 生成多时间尺度预测
        for (int horizon : FORECAST_HORIZONS) {
            ForecastResult forecast = generateForecast(load, weather, horizon);
            out.collect(forecast);
        }

        // 模型在线更新 (每96个点 = 24小时)
        if (ctx.timestamp() % (96 * 15 * 60 * 1000) < 15 * 60 * 1000) {
            updateModel(load);
        }
    }

    @Override
    public void processElement2(WeatherData weather, Context ctx, Collector<ForecastResult> out) {
        // 更新最新气象状态
        latestWeather.update(weather);
    }

    /**
     * 生成负荷预测
     */
    private ForecastResult generateForecast(RegionalLoad current, WeatherData weather, int horizon) {
        try {
            // 特征提取
            double[] features = extractFeatures(current, weather, horizon);

            // LSTM预测
            double lstmPrediction = predictWithLSTM(features);

            // Prophet风格时间序列分解
            double prophetPrediction = predictWithProphet(current, horizon);

            // 组合预测 (自适应加权)
            double[] weights = calculateAdaptiveWeights();
            double ensemblePrediction = weights[0] * lstmPrediction + weights[1] * prophetPrediction;

            // 计算预测区间
            double predictionStd = calculatePredictionStd(horizon);
            double confidence = 0.95;
            double zScore = 1.96;  // 95%置信区间

            Instant targetTime = current.getTimestamp().plus(
                Duration.ofMinutes(horizon * 15));

            return new ForecastResult(
                "LOAD",
                current.getRegionCode(),
                Instant.now(),
                targetTime,
                ensemblePrediction,
                ensemblePrediction - zScore * predictionStd,
                ensemblePrediction + zScore * predictionStd,
                confidence,
                horizon * 15
            );

        } catch (Exception e) {
            // 预测失败时使用简单外推
            return fallbackForecast(current, horizon);
        }
    }

    /**
     * 特征工程
     */
    private double[] extractFeatures(RegionalLoad load, WeatherData weather, int horizon) {
        Calendar cal = Calendar.getInstance();
        cal.setTimeInMillis(load.getTimestamp().toEpochMilli());

        int hour = cal.get(Calendar.HOUR_OF_DAY);
        int dayOfWeek = cal.get(Calendar.DAY_OF_WEEK);
        int month = cal.get(Calendar.MONTH);
        boolean isHoliday = isHoliday(cal);

        // 获取历史统计
        double[] historyStats = calculateHistoryStats();

        return new double[] {
            load.getLoadMw(),                    // 当前负荷
            load.getLoadMw() / load.getCapacityMw(),  // 负载率
            weather.getTemperature(),            // 温度
            weather.getHumidity() / 100.0,       // 湿度
            weather.getSolarIrradiance() / 1000.0, // 辐照度
            hour / 24.0,                         // 小时归一化
            dayOfWeek / 7.0,                     // 星期归一化
            month / 12.0,                        // 月份归一化
            isHoliday ? 1.0 : 0.0,               // 节假日标记
            Math.sin(2 * Math.PI * hour / 24),   // 小时周期特征
            Math.cos(2 * Math.PI * hour / 24),   // 小时周期特征
            historyStats[0],                     // 历史均值
            historyStats[1],                     // 历史标准差
            horizon / 96.0                       // 预测提前期归一化
        };
    }

    /**
     * Prophet风格预测 (时间序列分解)
     */
    private double predictWithProphet(RegionalLoad current, int horizon) {
        Calendar cal = Calendar.getInstance();
        cal.setTimeInMillis(current.getTimestamp().toEpochMilli());
        cal.add(Calendar.MINUTE, horizon * 15);

        int hour = cal.get(Calendar.HOUR_OF_DAY);
        int dayOfWeek = cal.get(Calendar.DAY_OF_WEEK);

        // 趋势项 (简单线性)
        double trend = calculateTrend();

        // 季节项 (日内周期)
        double dailySeasonality = getHourlyPattern(hour);

        // 周季节项
        double weeklyEffect = getWeeklyEffect(dayOfWeek);

        // 节假日效应
        double holidayEffect = isHoliday(cal) ? -0.15 : 0.0;

        return trend * (1 + dailySeasonality + weeklyEffect + holidayEffect);
    }

    /**
     * 使用LSTM模型预测
     */
    private double predictWithLSTM(double[] features) {
        // 简化的LSTM推理 (实际使用DL4J)
        // 这里使用线性近似模拟
        double prediction = 0;
        double[] weights = {0.3, 0.2, 0.15, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.03, 0.03, 0.02, 0.02, 0.05};

        for (int i = 0; i < Math.min(features.length, weights.length); i++) {
            prediction += features[i] * weights[i];
        }

        // 反归一化 (假设负荷范围 0-15000MW)
        return Math.max(0, prediction * 15000);
    }

    /**
     * 计算自适应权重
     */
    private double[] calculateAdaptiveWeights() {
        // 基于近期预测误差动态调整权重
        double lstmAccuracy = getRecentAccuracy("LSTM");
        double prophetAccuracy = getRecentAccuracy("PROPHET");

        double total = lstmAccuracy + prophetAccuracy;
        if (total == 0) return new double[]{0.5, 0.5};

        return new double[]{lstmAccuracy / total, prophetAccuracy / total};
    }

    /**
     * 计算预测标准差 (不确定性)
     */
    private double calculatePredictionStd(int horizon) {
        // 不确定性随预测提前期增加
        double baseStd = 200;  // 基础标准差 200MW
        double growthRate = 0.02;  // 每15分钟增长2%
        return baseStd * Math.exp(growthRate * horizon);
    }

    /**
     * 后备预测 (简单持久性)
     */
    private ForecastResult fallbackForecast(RegionalLoad current, int horizon) {
        Instant targetTime = current.getTimestamp().plus(
            Duration.ofMinutes(horizon * 15));

        return new ForecastResult(
            "LOAD",
            current.getRegionCode(),
            Instant.now(),
            targetTime,
            current.getLoadMw(),  // 使用当前值
            current.getLoadMw() * 0.9,
            current.getLoadMw() * 1.1,
            0.8,  // 较低的置信度
            horizon * 15
        );
    }

    /**
     * 维护历史窗口
     */
    private void trimHistory() throws Exception {
        List<LoadHistoryPoint> history = new ArrayList<>();
        loadHistory.get().forEach(history::add);

        if (history.size() > HISTORY_LENGTH) {
            loadHistory.clear();
            for (int i = history.size() - HISTORY_LENGTH; i < history.size(); i++) {
                loadHistory.add(history.get(i));
            }
        }
    }

    /**
     * 在线模型更新
     */
    private void updateModel(RegionalLoad actual) {
        // 使用实际观测值更新LSTM权重
        // 实际实现使用DL4J的在线学习API
    }

    // 辅助方法
    private boolean isHoliday(Calendar cal) {
        // 节假日判断逻辑
        return false;
    }

    private double[] calculateHistoryStats() {
        return new double[]{1000.0, 200.0};  // 均值、标准差
    }

    private double calculateTrend() {
        return 5000.0;  // 趋势值
    }

    private double getHourlyPattern(int hour) {
        // 典型日负荷曲线
        double[] pattern = {0.6, 0.5, 0.5, 0.5, 0.55, 0.7, 0.85, 0.95, 1.0, 0.95,
                           0.9, 0.88, 0.85, 0.88, 0.9, 0.92, 0.95, 1.0, 1.0, 0.95,
                           0.9, 0.85, 0.75, 0.65};
        return pattern[hour % 24];
    }

    private double getWeeklyEffect(int dayOfWeek) {
        double[] effects = {0.0, 0.05, 0.05, 0.05, 0.05, 0.05, -0.1};  // 周日到周六
        return effects[dayOfWeek - 1];
    }

    private double getRecentAccuracy(String model) {
        return 0.5;  // 默认相等权重
    }

    // 内部类
    private static class LoadHistoryPoint {
        Instant timestamp;
        double loadMw;
        String regionCode;

        LoadHistoryPoint(Instant timestamp, double loadMw, String regionCode) {
            this.timestamp = timestamp;
            this.loadMw = loadMw;
            this.regionCode = regionCode;
        }
    }

    private static class LSTMModelState {
        // LSTM模型参数
        double[][] weights;
        double[] biases;
    }
}
```

### 6.5 动态定价策略实现

```java
package com.gridoperator.pricing;

import com.gridoperator.model.*;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.co.KeyedCoProcessFunction;
import org.apache.flink.util.Collector;

import java.time.Instant;

/**
 * 动态定价处理函数
 * 基于负荷预测、可再生能源预测和电网状态实时计算电价
 */
public class DynamicPricingProcessFunction extends KeyedCoProcessFunction<
        String, ForecastResult, ForecastResult, PricingSignal> {

    // 状态
    private ValueState<GridState> gridState;
    private ValueState<PricingParams> pricingParams;

    // 定价参数
    private static final double BASE_PRICE = 0.5;  // 基础电价 0.5元/kWh
    private static final double PEAK_MULTIPLIER = 2.5;
    private static final double VALLEY_MULTIPLIER = 0.3;
    private static final double CONGESTION_MULTIPLIER = 1.5;
    private static final double RENEWABLE_BONUS = -0.1;  // 负电价补贴

    @Override
    public void open(Configuration parameters) {
        gridState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("grid-state", GridState.class));

        pricingParams = getRuntimeContext().getState(
            new ValueStateDescriptor<>("pricing-params", PricingParams.class));
    }

    @Override
    public void processElement1(ForecastResult loadForecast, Context ctx,
                                Collector<PricingSignal> out) throws Exception {

        GridState state = gridState.value();
        if (state == null) {
            state = new GridState();
        }

        // 更新负荷预测
        state.setLoadForecast(loadForecast);
        gridState.update(state);

        // 如果有可再生能源预测,触发定价计算
        if (state.getRenewableForecast() != null) {
            PricingSignal signal = calculatePrice(state);
            out.collect(signal);
        }
    }

    @Override
    public void processElement2(ForecastResult renewableForecast, Context ctx,
                                Collector<PricingSignal> out) throws Exception {

        GridState state = gridState.value();
        if (state == null) {
            state = new GridState();
        }

        // 更新可再生能源预测
        state.setRenewableForecast(renewableForecast);
        gridState.update(state);

        // 如果有负荷预测,触发定价计算
        if (state.getLoadForecast() != null) {
            PricingSignal signal = calculatePrice(state);
            out.collect(signal);
        }
    }

    /**
     * 计算动态电价
     */
    private PricingSignal calculatePrice(GridState state) {
        ForecastResult load = state.getLoadForecast();
        ForecastResult renewable = state.getRenewableForecast();

        // 计算供需比
        double demand = load.getPredictedValue();  // MW
        double supply = renewable.getPredictedValue();  // MW
        double supplyDemandRatio = supply / Math.max(demand, 1);

        // 基础价格调整
        double price = BASE_PRICE;

        // 1. 时段系数 (TOU - Time of Use)
        double timeMultiplier = calculateTimeMultiplier(load.getTargetTime());

        // 2. 供需平衡系数
        double balanceMultiplier = calculateBalanceMultiplier(demand, supply);

        // 3. 可再生能源激励
        double renewableBonus = 0;
        if (supplyDemandRatio > 0.8) {
            renewableBonus = RENEWABLE_BONUS * (supplyDemandRatio - 0.8);
        }

        // 4. 阻塞成本 (假设)
        double congestionCost = calculateCongestionCost(state);

        // 最终价格
        double finalPrice = price * timeMultiplier * balanceMultiplier +
                           renewableBonus + congestionCost;

        // 价格边界保护
        finalPrice = Math.max(0.1, Math.min(3.0, finalPrice));

        // 确定价格区间
        PriceTier tier = determinePriceTier(finalPrice, timeMultiplier);

        return new PricingSignal(
            load.getRegionCode(),
            Instant.now(),
            load.getTargetTime(),
            finalPrice,
            tier,
            generatePricingRecommendations(tier, supplyDemandRatio),
            demand,
            supply,
            supplyDemandRatio
        );
    }

    /**
     * 计算时段系数
     */
    private double calculateTimeMultiplier(Instant time) {
        java.time.ZonedDateTime dt = time.atZone(java.time.ZoneId.of("Asia/Shanghai"));
        int hour = dt.getHour();

        // 峰谷平时段定义
        if (hour >= 9 && hour < 12 || hour >= 18 && hour < 22) {
            // 峰时
            return PEAK_MULTIPLIER;
        } else if (hour >= 22 || hour < 8) {
            // 谷时
            return VALLEY_MULTIPLIER;
        } else {
            // 平时
            return 1.0;
        }
    }

    /**
     * 计算供需平衡系数
     */
    private double calculateBalanceMultiplier(double demand, double supply) {
        double reserve = supply - demand;
        double reserveRatio = reserve / demand;

        if (reserveRatio > 0.2) {
            // 供过于求,降价鼓励用电
            return 0.8 + (reserveRatio - 0.2) * -0.5;
        } else if (reserveRatio > 0) {
            // 供需平衡
            return 1.0;
        } else if (reserveRatio > -0.1) {
            // 供应紧张
            return 1.0 + Math.abs(reserveRatio) * 2;
        } else {
            // 严重短缺
            return CONGESTION_MULTIPLIER;
        }
    }

    /**
     * 计算阻塞成本
     */
    private double calculateCongestionCost(GridState state) {
        // 简化的阻塞成本模型
        double load = state.getLoadForecast().getPredictedValue();
        double capacity = 15000;  // 假设容量
        double utilization = load / capacity;

        if (utilization > 0.85) {
            return (utilization - 0.85) * 0.5;  // 高负载时附加阻塞成本
        }
        return 0;
    }

    /**
     * 确定价格区间
     */
    private PriceTier determinePriceTier(double price, double timeMultiplier) {
        if (timeMultiplier == PEAK_MULTIPLIER) {
            return PriceTier.PEAK;
        } else if (timeMultiplier == VALLEY_MULTIPLIER) {
            return price < BASE_PRICE * 0.5 ? PriceTier.SUPER_OFF_PEAK : PriceTier.OFF_PEAK;
        } else if (price < BASE_PRICE * 0.8) {
            return PriceTier.OFF_PEAK;
        } else if (price > BASE_PRICE * 1.5) {
            return PriceTier.CRITICAL_PEAK;
        } else {
            return PriceTier.MID_PEAK;
        }
    }

    /**
     * 生成定价建议
     */
    private String generatePricingRecommendations(PriceTier tier, double supplyDemandRatio) {
        StringBuilder sb = new StringBuilder();

        switch (tier) {
            case SUPER_OFF_PEAK:
                sb.append("最佳充电时段,建议EV充电、储能充电。");
                break;
            case OFF_PEAK:
                sb.append("电价较低,适合可推迟负荷。");
                break;
            case MID_PEAK:
                sb.append("正常电价,无特殊建议。");
                break;
            case PEAK:
                sb.append("电价高峰,建议减少非必要用电。");
                break;
            case CRITICAL_PEAK:
                sb.append("紧急高峰,高耗电设备建议暂停。");
                break;
        }

        if (supplyDemandRatio > 0.9) {
            sb.append(" 可再生能源充裕,清洁电力占比高。");
        }

        return sb.toString();
    }

    // 内部类
    private static class GridState {
        private ForecastResult loadForecast;
        private ForecastResult renewableForecast;
        private double currentFrequency = 50.0;
        private double reserveMargin = 0.15;

        // Getters and Setters
        public ForecastResult getLoadForecast() { return loadForecast; }
        public void setLoadForecast(ForecastResult loadForecast) {
            this.loadForecast = loadForecast;
        }

        public ForecastResult getRenewableForecast() { return renewableForecast; }
        public void setRenewableForecast(ForecastResult renewableForecast) {
            this.renewableForecast = renewableForecast;
        }
    }

    private static class PricingParams {
        private double basePrice = BASE_PRICE;
        private double rampRate = 0.1;  // 价格变化速率限制
        private double maxPrice = 3.0;
        private double minPrice = 0.1;
    }
}

/**
 * 定价信号
 */
class PricingSignal {
    private String regionCode;
    private Instant timestamp;
    private Instant targetTime;
    private double price;  // 元/kWh
    private PriceTier tier;
    private String recommendations;
    private double predictedDemand;
    private double predictedRenewable;
    private double supplyDemandRatio;

    public PricingSignal(String regionCode, Instant timestamp, Instant targetTime,
                        double price, PriceTier tier, String recommendations,
                        double predictedDemand, double predictedRenewable,
                        double supplyDemandRatio) {
        this.regionCode = regionCode;
        this.timestamp = timestamp;
        this.targetTime = targetTime;
        this.price = price;
        this.tier = tier;
        this.recommendations = recommendations;
        this.predictedDemand = predictedDemand;
        this.predictedRenewable = predictedRenewable;
        this.supplyDemandRatio = supplyDemandRatio;
    }

    // Getters
    public String getRegionCode() { return regionCode; }
    public double getPrice() { return price; }
    public PriceTier getTier() { return tier; }
    public String getRecommendations() { return recommendations; }
}

enum PriceTier {
    SUPER_OFF_PEAK,  // 深谷电价
    OFF_PEAK,        // 谷时电价
    MID_PEAK,        // 平时电价
    PEAK,            // 峰时电价
    CRITICAL_PEAK    // 紧急峰时
}
```

---

## 7. 可视化 (Visualizations)

### 7.1 智能电网架构图

智能电网实时能源管理系统的整体架构如下：

```mermaid
flowchart TB
    subgraph DataSources["数据源层"]
        AMI["AMI智能电表<br/>1000万+用户"]
        Weather["气象站<br/>温度/辐照度/风速"]
        SCADA["SCADA系统<br/>实时量测"]
        Market["电力市场<br/>电价信号"]
    end

    subgraph Ingestion["数据摄入层"]
        Kafka["Apache Kafka<br/>消息总线"]
        MQTT["MQTT Broker<br/>设备接入"]
    end

    subgraph Processing["Flink实时处理层"]
        subgraph Stream1["负荷预测管道"]
            F1["数据清洗"]
            F2["特征工程"]
            F3["LSTM/Prophet预测"]
        end

        subgraph Stream2["可再生能源预测"]
            F4["气象数据关联"]
            F5["出力预测"]
            F6["不确定性量化"]
        end

        subgraph Stream3["异常检测"]
            F7["CEP复杂事件处理"]
            F8["模式匹配"]
            F9["告警生成"]
        end

        subgraph Stream4["优化决策"]
            F10["需求响应调度"]
            F11["动态定价"]
            F12["控制指令生成"]
        end
    end

    subgraph Storage["存储层"]
        TDengine["TDengine<br/>时序数据"]
        Redis["Redis<br/>实时缓存"]
        HDFS["HDFS<br/>历史归档"]
    end

    subgraph Application["应用层"]
        Dashboard["监控大屏"]
        Dispatch["调度系统"]
        Mobile["用户APP"]
        Trading["交易平台"]
    end

    AMI --> MQTT
    Weather --> MQTT
    SCADA --> Kafka
    Market --> Kafka

    MQTT --> Kafka

    Kafka --> F1
    Kafka --> F4
    Kafka --> F7

    F1 --> F2 --> F3
    F4 --> F5 --> F6
    F7 --> F8 --> F9

    F3 --> F10
    F6 --> F11
    F9 --> F12

    F3 --> TDengine
    F6 --> TDengine
    F9 --> TDengine
    F11 --> Redis

    TDengine --> Dashboard
    Redis --> Mobile
    F12 --> Dispatch
    F11 --> Trading
```

### 7.2 电网拓扑数据流图

```mermaid
graph TB
    subgraph Generation["发电侧"]
        G1["火电站<br/>3000MW"]
        G2["水电站<br/>2000MW"]
        G3["风电场<br/>3500MW"]
        G4["光伏电站<br/>2800MW"]
    end

    subgraph Transmission["输电网络"]
        T1["500kV主干"]
        T2["220kV骨干"]
        T3["110kV配电"]
    end

    subgraph Distribution["配电网"]
        D1["区域A变电站"]
        D2["区域B变电站"]
        D3["区域C变电站"]
    end

    subgraph Consumption["负荷侧"]
        L1["工业负荷<br/>40%"]
        L2["商业负荷<br/>30%"]
        L3["居民负荷<br/>30%"]
        DR["需求响应<br/>可调负荷500MW"]
    end

    G1 --> T1
    G2 --> T1
    G3 --> T2
    G4 --> T2

    T1 --> T2 --> T3

    T3 --> D1
    T3 --> D2
    T3 --> D3

    D1 --> L1
    D2 --> L2
    D3 --> L3

    DR -.->|响应信号| D1
    DR -.->|响应信号| D2
    DR -.->|响应信号| D3

    style G3 fill:#90EE90
    style G4 fill:#FFD700
    style DR fill:#87CEEB
```

### 7.3 预测曲线对比图

```mermaid
xychart-beta
    title "24小时负荷预测 vs 实际值"
    x-axis [00:00, 02:00, 04:00, 06:00, 08:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00]
    y-axis "负荷 (MW)" 4000 --> 15000

    line "预测值" [6500, 5200, 4800, 5500, 8500, 12000, 13500, 12800, 11500, 14000, 13800, 9000]
    line "实际值" [6400, 5100, 4750, 5600, 8600, 11900, 13600, 12900, 11600, 14100, 13700, 8900]
    line "置信区间上限" [7000, 5700, 5300, 6100, 9200, 12600, 14100, 13400, 12100, 14600, 14400, 9500]
    line "置信区间下限" [6000, 4700, 4300, 4900, 7800, 11400, 12900, 12200, 10900, 13400, 13200, 8500]
```

### 7.4 异常检测CEP流程图

```mermaid
stateDiagram-v2
    [*] --> NormalOperation: 系统启动

    NormalOperation --> FrequencyWatch: 频率监测
    NormalOperation --> VoltageWatch: 电压监测
    NormalOperation --> LoadWatch: 负荷监测

    FrequencyWatch --> FrequencyDeviation: |f-50Hz|>0.2Hz
    VoltageWatch --> VoltageViolation: |V-Vnom|/Vnom>5%
    LoadWatch --> OverloadWarning: 负载率>80%

    FrequencyDeviation --> CriticalFrequency: |f-50Hz|>0.5Hz
    FrequencyDeviation --> NormalOperation: 恢复

    VoltageViolation --> CriticalVoltage: 持续>30s
    VoltageViolation --> NormalOperation: 恢复

    OverloadWarning --> LineOverload: 持续>5min
    OverloadWarning --> NormalOperation: 负载下降

    CriticalFrequency --> EmergencyAction: 启动紧急控制
    CriticalVoltage --> EmergencyAction: 启动紧急控制
    LineOverload --> EmergencyAction: 启动负荷转移

    EmergencyAction --> NormalOperation: 故障清除
    EmergencyAction --> [*]: 系统保护动作
```

---

## 8. 业务成果 (Business Outcomes)

本项目实施后取得显著的业务成效：

### 8.1 预测准确率提升

| 预测类型 | 实施前 | 实施后 | 提升幅度 |
|---------|-------|-------|---------|
| 负荷预测 | 85% | 96% | +11% |
| 光伏出力预测 | 78% | 94% | +16% |
| 风电出力预测 | 72% | 89% | +17% |
| 价格预测 | 80% | 92% | +12% |

### 8.2 运营效率提升

| 指标 | 基准值 | 目标值 | 实际达成 |
|------|-------|-------|---------|
| 弃风弃光率 | 20% | < 14% | 13% ✓ |
| 峰值负荷削减 | 0% | ≥ 10% | 12% ✓ |
| 备用容量需求 | 100% | 70% | 68% ✓ |
| 故障检测时间 | 5分钟 | < 5秒 | 2秒 ✓ |

### 8.3 经济效益

| 效益类别 | 年度节省/收益 |
|---------|--------------|
| 减少弃电损失 | 2.8亿元 |
| 降低备用容量成本 | 1.5亿元 |
| 需求响应收益 | 0.8亿元 |
| 减少偏差考核 | 0.6亿元 |
| **总计** | **5.7亿元** |

### 8.4 环境效益

- 年减少CO₂排放：**120万吨**
- 可再生能源消纳能力提升：**35%**
- 等效植树：**6500万棵**

---

## 9. 经验总结 (Lessons Learned)

### 9.1 成功经验

**1. 多时间尺度预测组合**

- 超短期 (5-15分钟): LSTM捕捉快速变化
- 短期 (1-4小时): Prophet处理周期性
- 日前 (24小时): 集成气象预报

**2. CEP异常检测的价值**

- 将故障检测从分钟级降至秒级
- 预测性维护减少非计划停机
- 模式库持续积累提升检测精度

**3. 需求响应的规模化应用**

- 价格信号引导用户行为
- 工业负荷作为"虚拟电厂"
- 电动汽车V2G双向互动

### 9.2 挑战与应对

| 挑战 | 应对策略 |
|------|---------|
| 数据质量问题 | 边缘清洗 + 质量评分 |
| 模型冷启动 | 迁移学习 + 在线更新 |
| 网络延迟波动 | 自适应Watermark策略 |
| 极端天气预测 | 多模型集成 + 人工介入 |

### 9.3 最佳实践

1. **状态后端选择**: 大状态场景必选RocksDB，配合增量checkpoint
2. **Watermark策略**: 多源数据使用不同容忍度，关键数据严格对齐
3. **模型更新**: 在线学习避免全量重训，A/B测试验证效果
4. **监控告警**: Flink作业健康度监控，预测偏差自动告警

---

## 10. 引用参考 (References)

      Foundations and Trends in Electric Energy Systems, 2019.
      <https://doi.org/10.1561/3100000014>

      Renewable and Sustainable Energy Reviews, 2022.
      <https://doi.org/10.1016/j.rser.2022.112912>

      Neurocomputing, 2017. <https://doi.org/10.1016/j.neucom.2017.04.070>

      <https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/>

      Intelligent Energy Systems, and Smart Loads", IEEE Transactions on
      Industrial Informatics, 2011. <https://doi.org/10.1109/TII.2011.2158841>


      <https://www.iea.org/reports/digitalisation-and-energy>

      for Smart Grid Control Architecture", CIRED Workshop, 2016.


       Chapter 4: Load Forecasting, Elsevier, 2021.
