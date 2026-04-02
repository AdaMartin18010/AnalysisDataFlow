# GPU 机密计算 — Flink 安全流处理架构

> 所属阶段: Flink/Security | 前置依赖: [Flink 可信执行环境](./trusted-execution-flink.md) | 形式化等级: L4-L5

## 1. 概念定义 (Definitions)

### Def-F-13-08: GPU TEE (GPU Trusted Execution Environment)

**形式化定义**:

GPU TEE 是在 GPU 硬件上建立的隔离执行环境，用于保护数据在使用中的机密性和完整性：

$$\text{GPU-TEE} = (H_{GPU}, M_{CPR}, K_{session}, A_{attest}, F_{firewall})$$

其中：

- $H_{GPU}$: GPU 硬件根信任 (Root of Trust, RoT)，芯片制造时烧录的唯一加密身份
- $M_{CPR}$: 计算保护区域 (Compute Protected Region)，受硬件保护的 GPU 内存区域
- $K_{session}$: 会话密钥，用于 CPU-GPU 间加密通信
- $A_{attest}$: GPU 远程证明机制
- $F_{firewall}$: PCIe/NVLink 防火墙，阻止未授权访问

**安全保证**:

| 保证 | 描述 | 实现机制 |
|------|------|---------|
| 机密性 (Confidentiality) | GPU 内存数据对主机不可见 | HBM 硬件隔离 + AES-GCM 加密 |
| 完整性 (Integrity) | 代码和数据在传输/计算中不可篡改 | SPDM 安全会话 + 度量链 |
| 可验证性 (Verifiability) | 外部可密码学验证 GPU 状态 | 远程证明报告 |
| 可用性 (Availability) | 性能损失最小化 | 硬件加速加密引擎 |

---

### Def-F-13-09: NVIDIA H100 CC Mode

**形式化定义**:

NVIDIA H100 机密计算模式是世界首个原生支持 TEE 的 GPU 实现：

$$\text{H100-CC} = \text{GPU-TEE}(\text{RoT}_{on-die}, \text{AES}_{256-GCM}, \text{SPDM}_{1.2})$$

**关键硬件特性**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    NVIDIA H100 GPU (Hopper)                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           Compute Protected Region (CPR)                │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │   │
│  │  │ Tensor Core │  │    HBM3     │  │   DMA Engine    │  │   │
│  │  │   (FP8/16)  │  │  (3 TB/s)   │  │ (AES-GCM 256)   │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌────────────────────────┴───────────────────────────────┐    │
│  │           PCIe Firewall / NVLink Firewall              │    │
│  │         (Block unauthorized memory access)             │    │
│  └────────────────────────────────────────────────────────┘    │
│                           │                                     │
│  ┌────────────────────────┴───────────────────────────────┐    │
│  │              Hardware Root of Trust (RoT)              │    │
│  │    - Unique Device Identity (burned at manufacture)    │    │
│  │    - Secure Boot (firmware signature verification)     │    │
│  │    - Attestation Key (AK) for remote attestation       │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

**CC 模式状态机**:

```
[POWER_ON] ──→ [SECURE_BOOT] ──→ [IDLE] ──→ [CC_MODE_ON]
                   │                              │
                   ↓                              ↓
            [RoT Verified]              [Session Established]
                                               │
                                               ↓
                                      [TEE_OPERATION]
```

**模式对比**:

| 特性 | CC-Off (传统模式) | CC-On (机密模式) |
|------|------------------|-----------------|
| 主机访问 | 完全访问 GPU 内存 | 被 PCIe 防火墙阻断 |
| 性能计数器 | 可用 | 禁用（防侧信道） |
| DMA 加密 | 无 | AES-GCM 256 |
| 远程证明 | 无 | 完整证明链 |
| 性能开销 | 0% | <2% (典型) |

---

### Def-F-13-10: AMD MI300 Infinity Guard

**形式化定义**:

AMD Instinct MI300 系列 GPU 通过 Infinity Guard 技术栈提供 TEE 支持：

$$\text{MI300-TEE} = \text{GPU-TEE}(\text{SEV-SNP}_{ext}, \text{TSME}, \text{TIO})$$

其中：

- $\text{SEV-SNP}_{ext}$: 扩展的 SEV-SNP 支持，保护 GPU 内存免受恶意 Hypervisor 访问
- $\text{TSME}$: Transparent Secure Memory Encryption，透明安全内存加密
- $\text{TIO}$: Trusted I/O，将 TEE 扩展到外部可信设备

**MI300 安全层次**:

| 层次 | 组件 | 功能 |
|------|------|------|
| L0 | AMD Security Processor | 硬件根信任、密钥管理 |
| L1 | Infinity Fabric | 加密互连、内存保护 |
| L2 | GPU Compute Die | 计算单元隔离 |
| L3 | HBM3 Stack | 内存加密引擎 |
| L4 | PCIe/CXL | 可信 I/O 通道 |

---

### Def-F-13-11: 安全流处理会话 (Secure Stream Processing Session)

**形式化定义**:

Flink 安全流处理会话是建立在 GPU TEE 之上的高层抽象：

$$\text{SSPS} = (CVM_{CPU}, TEE_{GPU}, K_{shared}, Ch_{secure}, \mathcal{O}_{stream})$$

其中：

- $CVM_{CPU}$: 机密虚拟机 (Confidential VM)，Intel TDX 或 AMD SEV-SNP
- $TEE_{GPU}$: GPU TEE 实例 (H100 CC Mode 或 MI300 TEE)
- $K_{shared}$: SPDM 会话派生的共享密钥
- $Ch_{secure}$: 安全通道，保护 CPU-GPU 数据传输
- $\mathcal{O}_{stream}$: 流算子集合，在 GPU TEE 内执行

**会话生命周期**:

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  INIT    │───→│ ATTEST   │───→│ COMPUTE  │───→│ TEARDOWN │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │
     ↓               ↓               ↓               ↓
 CVM Launch      GPU Quote      Data Stream     Key Eviction
 GPU Bind        NRAS Verify    Secure Exec     State Clear
```

---

## 2. 属性推导 (Properties)

### Prop-F-13-04: CPU-GPU 复合 TEE 安全定理

**命题**: 当 CPU TEE (CVM) 与 GPU TEE 联合使用时，系统可防护以下攻击者：

$$\text{Attacker} \in \{\text{OS}, \text{Hypervisor}, \text{BIOS}, \text{Admin}, \text{Network}, \text{PCIe-Snooper}\}$$

**证明概要**:

1. **CVM 层防护**:
   - CPU 内存加密 (Intel MKTME / AMD SME)
   - VM 隔离：Hypervisor 无法访问 CVM 内存
   - 证明：$\forall x \in M_{CVM}, \text{Hypervisor} \not\rightarrow x$

2. **GPU TEE 层防护**:
   - PCIe 防火墙阻断主机访问 $M_{CPR}$
   - DMA 引擎加密所有进出 CPR 的数据
   - 证明：$\forall y \in M_{CPR}, \text{Host} \not\rightarrow y$

3. **通道防护**:
   - SPDM 会话建立共享密钥 $K_{session}$
   - Bounce Buffer 使用 AES-GCM 256 加密
   - 证明：$\text{Data}_{transit} = \text{AES-GCM}_{K_{session}}(\text{plaintext})$

4. **端到端安全**:
   $$
   \text{Security}_{end-to-end} = \text{CVM}_{isolation} \land \text{GPU}_{isolation} \land \text{Channel}_{encryption}
   $$

---

### Prop-F-13-05: GPU TEE 数据机密性定理

**命题**: 在 GPU TEE 中处理的数据，对特权攻击者保持机密：

$$\text{Confidentiality}(D) \Rightarrow \forall A \in \text{Privileged}, \Pr[A \text{ learns } D] < \epsilon_{negl}$$

**推导**:

| 攻击向量 | 防护措施 | 安全边界 |
|---------|---------|---------|
| 内存转储 (Memory Dump) | CPR 硬件隔离 | 物理内存访问被阻断 |
| PCIe 嗅探 (PCIe Snooping) | AES-GCM 256 加密 | 密文不可区分性 |
| 侧信道 (Side Channel) | 性能计数器禁用 | 时序/功耗攻击失效 |
| 固件篡改 (Firmware Tampering) | 安全启动 + 度量 | 篡改可检测 |

---

### Lemma-F-13-02: 性能开销上界

**引理**: 对于大规模模型（如 Llama-3.1-70B），GPU TEE 的性能开销满足：

$$\text{Overhead}_{TEE} = \frac{T_{TEE} - T_{baseline}}{T_{baseline}} < 2\%$$

**条件**: 当批处理大小 (batch size) 足够大，使计算主导 I/O 时。

**证明依据**:

- GPU 内部计算不受 TEE 影响（全速 HBM 访问）
- 开销主要来自 CPU-GPU 数据传输加密
- 对于大模型，计算时间 $T_{compute} \gg T_{IO}$
- 因此 $\lim_{\text{model-size}\to\infty} \text{Overhead}_{TEE} = 0$

---

## 3. 关系建立 (Relations)

### 3.1 CPU TEE vs GPU TEE 对比矩阵

| 维度 | Intel SGX | Intel TDX | AMD SEV-SNP | NVIDIA H100 CC | AMD MI300 TEE |
|------|:---------:|:---------:|:-----------:|:--------------:|:-------------:|
| **隔离粒度** | 进程级 | VM级 | VM级 | GPU设备级 | GPU设备级 |
| **内存容量** | 128MB-1GB EPC | 无限制 | 无限制 | 80GB HBM3 | 192GB HBM3 |
| **TCB 大小** | 小 (CPU+uCode) | 较大 (TDX Module) | 较大 (SEV FW) | 中 (GPU RoT+FW) | 中 (SP+IF) |
| **计算特性** | 通用 | 通用 | 通用 | 张量加速 | 张量加速 |
| **带宽** | 内存带宽 | 内存带宽 | 内存带宽 | 3 TB/s | ~5 TB/s |
| **加密引擎** | 内存加密 | MKTME | SME | AES-GCM 256 (DMA) | TSME |
| **证明服务** | Intel PCS | Intel Trust Authority | AMD ASP | NVIDIA NRAS | AMD ASP |
| **依赖 CPU TEE** | 独立 | 独立 | 独立 | **必须** (TDX/SNP) | **必须** (SNP) |
| **代表应用** | 密钥管理 | 机密VM | 云原生安全 | 安全AI推理 | 安全AI训练 |

### 3.2 CPU-GPU TEE 协作架构

```mermaid
graph TB
    subgraph "可信边界外 (Untrusted)"
        HOST[Host OS / Hypervisor]
        HV[Hypervisor]
        NET[Network]
    end

    subgraph "CPU TEE (CVM)"
        direction TB
        CVM[Confidential VM]
        DRV[NVIDIA Driver<br/>SPDM Session]
        BB[Bounce Buffer<br/>Shared Memory]
        APP[Flink Application]

        subgraph "CVM 内部"
            FLINK[Flink Runtime]
            SEC[Security Manager]
        end
    end

    subgraph "GPU TEE"
        direction TB
        GPU_GPU[NVIDIA H100 / AMD MI300]

        subgraph "GPU 内部"
            CPR[Compute Protected Region<br/>CPR]
            HBM[HBM3 Memory]
            TC[Tensor Cores]
            DMA[DMA Engine<br/>AES-GCM 256]
        end

        ROT[Hardware RoT]
        FW[Signed Firmware]
    end

    subgraph "远程证明服务"
        NRAS[NVIDIA NRAS]
        ITA[Intel Trust Authority]
        ASP[AMD ASP]
    end

    HOST -.->|Blocked| CVM
    HV -.->|Blocked| GPU_GPU

    CVM <-->|SPDM Key Exchange| GPU_GPU
    BB <-->|Encrypted Transfer| DMA
    DMA --> CPR
    CPR --> HBM
    HBM --> TC

    FLINK --> SEC
    SEC --> DRV

    CVM <-->|CPU Attestation| ITA
    GPU_GPU <-->|GPU Attestation| NRAS

    ROT --> FW
    FW --> GPU_GPU
```

### 3.3 Flink + GPU TEE 映射关系

| Flink 组件 | GPU TEE 对应 | 安全增强 |
|-----------|-------------|---------|
| JobManager | CVM 内协调器 | 调度策略保密 |
| TaskManager | GPU TEE 容器 | 算子代码完整性 |
| State Backend | GPU HBM 加密存储 | 状态机密性 |
| Checkpoint | 密封加密检查点 | 持久化保护 |
| Source/Sink | 加密通道连接器 | 数据流保护 |
| UDF | GPU Kernel | 用户代码隔离 |

---

## 4. 论证过程 (Argumentation)

### 4.1 威胁模型：GPU 流处理场景

**攻击者能力层级**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    GPU TEE 威胁模型                             │
├─────────────────────────────────────────────────────────────────┤
│ L1: 网络攻击者      → 被动监听/篡改 PCIe/NVLink 流量            │
│ L2: 云租户          → 共享 GPU 的 MIG 逃逸攻击                  │
│ L3: 系统管理员      → 主机内存访问、驱动注入                     │
│ L4: 云运营商        → Hypervisor 控制、恶意固件                  │
│ L5: 物理攻击者      → 冷启动、总线嗅探、侧信道                   │
└─────────────────────────────────────────────────────────────────┘
```

**GPU TEE 防护边界**:

- 有效防护至 **L4**（云运营商级别）
- L5 需要额外物理防护（如防拆封、温度监控）

### 4.2 安全流处理架构设计

**分层安全策略**:

```
┌─────────────────────────────────────────────────────────────────┐
│ Layer 5: 应用层安全 (Flink SQL/UDF 沙箱)                        │
│         - 算子级隔离、内存安全语言 (Rust)                         │
├─────────────────────────────────────────────────────────────────┤
│ Layer 4: 运行时安全 (CUDA 驱动验证)                             │
│         - 驱动签名验证、API 调用审计                             │
├─────────────────────────────────────────────────────────────────┤
│ Layer 3: GPU TEE (CPR 隔离、DMA 加密)                           │
│         - 硬件级内存保护、AES-GCM 256                           │
├─────────────────────────────────────────────────────────────────┤
│ Layer 2: CPU-GPU 通道安全 (SPDM 1.2)                            │
│         - 相互认证、会话密钥派生                                 │
├─────────────────────────────────────────────────────────────────┤
│ Layer 1: CPU TEE (CVM 隔离)                                     │
│         - VM 内存加密、Hypervisor 隔离                           │
├─────────────────────────────────────────────────────────────────┤
│ Layer 0: 硬件根信任 (RoT)                                       │
│         - 设备身份、安全启动、固件度量                            │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 性能-安全权衡分析

| 配置 | 安全级别 | 性能开销 | 适用场景 |
|------|---------|---------|---------|
| 无 TEE | L0 | 0% | 非敏感数据 |
| 仅 CPU TEE | L3 | 3-5% | 一般敏感数据 |
| CPU+GPU TEE | L4 | 1-7% | 高敏感 AI/ML |
| + MIG 隔离 | L4+ | 2-10% | 多租户安全 |

**关键观察**: 对于大规模流处理（大 batch），开销趋近于零。

---

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

### 5.1 GPU TEE 远程证明协议

**协议参与者**:

- $\mathcal{C}$: CPU CVM (Flink 运行时)
- $\mathcal{G}$: GPU TEE (H100/MI300)
- $\mathcal{V}$: 验证者 (NRAS / Intel Trust Authority)
- $\mathcal{R}$: 依赖方 (密钥服务)

**协议步骤**:

```
Phase 1: 设备身份建立
─────────────────────────────────────────
1.  𝒢 上电 → 安全启动验证固件签名
2.  RoT 生成设备密钥对 (EK_pub, EK_priv)
3.  固件度量值: FW_MEASUREMENT = SHA256(FW_IMAGE)

Phase 2: SPDM 会话建立
─────────────────────────────────────────
4.  𝒞 ←→ 𝒢: SPDM VCA (Version/Capabilities/Algorithms)
5.  𝒞 ←→ 𝒢: SPDM Key Exchange
    - 临时密钥对 (ephemeral)
    - 共享密钥派生: K_session = KDF(ECDH_shared, transcript)

Phase 3: 远程证明
─────────────────────────────────────────
6.  𝒞 → 𝒢: GET_MEASUREMENTS (nonce 𝒩)
7.  𝒢 生成 Quote:
    Quote = {
      HEADER: "NV_GPU_QUOTE",
      DEVICE_ID: EK_pub,
      FW_MEASUREMENT: H(FW),
      NONCE: 𝒩,
      SIGNATURE: Sign(AK, above)
    }
8.  𝒞 → 𝒱: Quote
9.  𝒱 验证:
    a. 验证 AK 证书链 → NVIDIA RoT CA
    b. 对比 FW_MEASUREMENT 与 RIM (Reference Integrity Manifest)
    c. 检查证书吊销状态 (OCSP)
10. 𝒱 → 𝒞: EAT (Entity Attestation Token)

Phase 4: 安全通道建立
─────────────────────────────────────────
11. 𝒞 验证 EAT 后，派生数据加密密钥
12. 𝒞 ←→ 𝒢: 所有数据经 AES-GCM 256 加密传输
```

**安全性论证**:

| 属性 | 证明 |
|------|------|
| **身份真实性** | AK 证书链锚定至 NVIDIA RoT CA，不可伪造 |
| **完整性** | Quote 包含固件度量，篡改可检测 |
| **新鲜性** | Nonce 防止重放攻击 |
| **前向保密** | 临时 ECDH 密钥确保会话独立 |

---

### 5.2 Flink GPU TEE 流处理正确性论证

**系统模型**:

$$
\text{System} = \langle S, \Sigma, \delta, s_0, F \rangle$$

- $S$: 系统状态集合（流数据、GPU 状态、密钥状态）
- $\Sigma$: 事件集合（数据到达、检查点、证明请求）
- $\delta: S \times \Sigma \rightarrow S$: 状态转移函数
- $s_0$: 初始状态（未初始化 TEE）
- $F$: 接受状态（安全处理完成）

**安全不变式**:

对于所有可达状态 $s \in S$:

1. **密钥隔离不变式**:
   $$\text{KeyMaterial}(s) \subseteq M_{CPR}(s) \land \text{Host} \not\rightarrow M_{CPR}$$

2. **数据机密性不变式**:
   $$\forall d \in \text{SensitiveData}(s): \text{Attacker} \not\rightarrow d$$

3. **代码完整性不变式**:
   $$\text{Code}_{running} = \text{Code}_{expected} \Rightarrow \text{MRENCLAVE} = H(\text{Code}_{expected})$$

**证明概要**:

- **初始状态** $s_0$: 无敏感数据，不变式平凡成立
- **归纳步骤**:
  - 证明请求处理: 远程证明确保只有合法 GPU 可接收密钥
  - 数据处理: DMA 加密确保传输机密性
  - 检查点: 密封存储绑定至 TEE 身份
- **终止状态**: 密钥被安全销毁，无信息泄露

---

### 5.3 性能开销形式化分析

**定义**:

- $T_{compute}$: GPU 内部计算时间
- $T_{IO}$: CPU-GPU 数据传输时间
- $T_{encrypt}$: 加密/解密时间 (硬件加速)

**基线执行时间**:

$$T_{baseline} = T_{compute} + T_{IO}$$

**TEE 执行时间**:

$$T_{TEE} = T_{compute} + T_{IO} + T_{encrypt}$$

**开销公式**:

$$\text{Overhead} = \frac{T_{encrypt}}{T_{compute} + T_{IO}}$$

**定理**: 当满足以下条件时，开销 < 2%:

$$T_{compute} > 50 \times T_{encrypt}$$

**证明**:

- H100 DMA 引擎支持 PCIe Gen5 线速加密 (~64 GB/s)
- 对于 Llama-3.1-70B 推理：
  - $T_{compute}$ ≈ 100ms (token generation)
  - $T_{encrypt}$ ≈ 1-2ms (数据传输)
  - $\text{Overhead} = \frac{1}{100} = 1\%$

**实证数据** (来源: arXiv 2409.03992):

| 模型 | 参数 | Batch Size | TEE Overhead |
|------|------|-----------|--------------|
| Llama-3.1-8B | 8B | 1 | ~7% |
| Phi3-14B | 14B | 8 | ~4% |
| Llama-3.1-70B | 70B | 32 | ~1% |
| Mixtral-8x22B | 176B | 64 | <1% |

---

## 6. 实例验证 (Examples)

### 6.1 机密 ML 推理 Flink 作业

**场景**: 金融机构使用 Flink 进行实时风控模型推理，模型权重和交易数据均为敏感信息。

**架构实现**:

```mermaid
flowchart TB
    subgraph "输入层"
        KAFKA[Kafka Stream<br/>加密交易数据]
    end

    subgraph "Flink Cluster (CVM)"
        JM[JobManager<br/>Intel TDX CVM]

        subgraph "TaskManager 1"
            TM1_CPU[CPU 预处理]
        end

        subgraph "TaskManager 2 (GPU TEE)"
            TM2_CPU[CPU 输入缓冲]

            subgraph "NVIDIA H100 CC Mode"
                GPU_DEC[解密 Kernel]
                GPU_INF[推理 Kernel]
                GPU_ENC[结果加密]

                subgraph "CPR 内存"
                    MODEL[模型权重<br/>AES-256 加密]
                    ACT[激活值]
                end
            end
        end

        subgraph "密钥管理"
            KM[密封密钥存储]
            RA[远程证明客户端]
        end
    end

    subgraph "验证服务"
        NRAS_S[NVIDIA NRAS]
        ITA_S[Intel Trust Authority]
    end

    subgraph "输出层"
        RESULT[加密结果输出]
    end

    KAFKA --> JM
    JM --> TM1_CPU
    TM1_CPU --> TM2_CPU
    TM2_CPU --> GPU_DEC
    GPU_DEC --> GPU_INF
    GPU_INF --> GPU_ENC

    MODEL -.-> GPU_INF
    KM -.->|Unseal| GPU_DEC

    RA <-->|Attestation| NRAS_S
    RA <-->|Attestation| ITA_S

    GPU_ENC --> RESULT
```

**关键代码模式**:

```java
// Flink GPU TEE 安全推理算子
public class SecureGPUInference extends RichAsyncFunction<byte[], byte[]> {

    private transient GpuTEEContext teeCtx;
    private transient SealedKey sealedModelKey;

    @Override
    public void open(Configuration params) {
        // 1. 初始化 GPU TEE 上下文
        teeCtx = GpuTEEContext.create("nvidia-h100");

        // 2. 执行复合远程证明
        CompositeAttestation attest = CompositeAttestation.builder()
            .cpuTEE(TEEType.INTEL_TDX)
            .gpuTEE(TEEType.NVIDIA_H100_CC)
            .build();

        AttestationResult result = attest.verify(
            IntelTrustAuthority.getInstance(),
            NVIDIANRAS.getInstance()
        );

        if (!result.isValid()) {
            throw new SecurityException("GPU TEE attestation failed");
        }

        // 3. 解封模型密钥
        sealedModelKey = loadSealedModelKey();
        byte[] modelKey = teeCtx.unseal(sealedModelKey);

        // 4. 加载加密模型到 GPU CPR
        teeCtx.loadEncryptedModel("model.bin", modelKey);

        // 5. 销毁明文密钥
        Arrays.fill(modelKey, (byte) 0);
    }

    @Override
    public void asyncInvoke(byte[] encryptedInput, ResultFuture<byte[]> future) {
        // 数据在 GPU TEE 内解密、推理、加密输出
        CompletableFuture.supplyAsync(() -> {
            // 所有操作在 GPU TEE 内部完成
            return teeCtx.secureInference(encryptedInput);
        }, gpuExecutor).thenAccept(result -> {
            future.complete(Collections.singletonList(result));
        });
    }
}
```

---

### 6.2 多租户 GPU 安全隔离

**场景**: 云服务商使用 MIG (Multi-Instance GPU) 为多个租户提供隔离的 Flink 流处理能力。

**MIG + CC 架构**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    NVIDIA H100 GPU (80GB)                       │
│                    CC Mode + MIG Enabled                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │   MIG Instance 0 │ │   MIG Instance 1 │ │   MIG Instance 2 │   │
│  │   (20GB)         │ │   (20GB)         │ │   (20GB)         │   │
│  │                  │ │                  │ │                  │   │
│  │  ┌───────────┐  │ │  ┌───────────┐  │ │  ┌───────────┐  │   │
│  │  │ Tenant A  │  │ │  │ Tenant B  │  │ │  │ Tenant C  │  │   │
│  │  │ Flink Job │  │ │  │ Flink Job │  │ │  │ Flink Job │  │   │
│  │  │ TEE-GPU 0 │  │ │  │ TEE-GPU 1 │  │ │  │ TEE-GPU 2 │  │   │
│  │  └───────────┘  │ │  └───────────┘  │ │  └───────────┘  │   │
│  │                  │ │                  │ │                  │   │
│  │  CPR-0 (隔离)    │ │  CPR-1 (隔离)    │ │  CPR-2 (隔离)    │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Hardware Firewalls                         │   │
│  │  - NVLink 防火墙隔离 MIG 实例间访问                      │   │
│  │  - PCIe 防火墙隔离主机访问                               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**安全保证**:

- 每个 MIG 实例拥有独立的 CPR
- 硬件防火墙阻止跨实例内存访问
- 每个实例独立证明（独立 Quote）

---

## 7. 可视化 (Visualizations)

### 7.1 GPU TEE 安全架构全景图

```mermaid
graph TB
    subgraph "应用层 (Application)"
        FLINK_APP[Flink Streaming Application]
        ML_LIB[ML Inference Library]
        CRYPTO[Crypto Operations]
    end

    subgraph "运行时层 (Runtime)"
        CUDART[CUDA Runtime]
        SPDM[SPDM 1.2 Stack]
        UVM[Unified Virtual Memory]
    end

    subgraph "GPU TEE 抽象层"
        TEE_API[GPU TEE API<br/>nvtrust / AMD TEE]
        ATTEST_MGR[Attestation Manager]
        KEY_MGR[Key Manager]
    end

    subgraph "硬件 TEE 层"
        subgraph "NVIDIA H100"
            H100_CC[H100 CC Mode]
            H100_CPR[CPR - 80GB HBM3]
            H100_DMA[DMA + AES-GCM 256]
        end

        subgraph "AMD MI300"
            MI300_TEE[MI300 TEE Mode]
            MI300_CPR[CPR - 192GB HBM3]
            MI300_TSME[TSME Engine]
        end
    end

    subgraph "CPU TEE 层 (必需)"
        TDX[Intel TDX CVM]
        SNP[AMD SEV-SNP CVM]
    end

    subgraph "远程证明服务"
        NRAS[NVIDIA NRAS]
        ITA[Intel Trust Authority]
        ASP[AMD ASP]
    end

    FLINK_APP --> ML_LIB --> CUDART
    CRYPTO --> SPDM

    CUDART --> TEE_API
    SPDM --> ATTEST_MGR
    UVM --> KEY_MGR

    TEE_API --> H100_CC
    TEE_API --> MI300_TEE

    ATTEST_MGR <-->|GPU Attestation| NRAS
    ATTEST_MGR <-->|CPU Attestation| ITA
    ATTEST_MGR <-->|CPU Attestation| ASP

    H100_CC <-->|SPDM Session| TDX
    H100_CC <-->|SPDM Session| SNP
    MI300_TEE <-->|TIO| SNP

    H100_CC --> H100_DMA --> H100_CPR
    MI300_TEE --> MI300_TSME --> MI300_CPR
```

### 7.2 GPU TEE 信任链与远程证明流程

```mermaid
sequenceDiagram
    autonumber
    participant CVM as Intel TDX CVM<br/>Flink Runtime
    participant GPU as NVIDIA H100<br/>CC Mode
    participant NRAS as NVIDIA NRAS
    participant ITA as Intel Trust Authority
    participant KMS as Key Management Service

    rect rgb(230, 245, 255)
        Note over CVM,GPU: Phase 1: 硬件初始化 & 安全启动
        GPU->>GPU: Secure Boot<br/>验证固件签名
        GPU->>GPU: RoT 生成设备身份
        CVM->>CVM: TDX VM 启动<br/>内存加密启用
    end

    rect rgb(255, 245, 230)
        Note over CVM,GPU: Phase 2: SPDM 安全会话建立
        CVM->>GPU: VCA (Version/Capabilities)
        GPU-->>CVM: 响应
        CVM->>GPU: Key Exchange<br/>ECDH 临时密钥
        GPU-->>CVM: 响应
        Note right of CVM: 派生会话密钥<br/>K_session
    end

    rect rgb(230, 255, 230)
        Note over CVM,NRAS: Phase 3: GPU 远程证明
        CVM->>GPU: GET_MEASUREMENTS<br/>Nonce = N
        GPU->>GPU: 生成 Quote<br/>Sign(AK, MRENCLAVE || N)
        GPU-->>CVM: GPU Quote
        CVM->>NRAS: verifyQuote(GPU Quote)
        NRAS->>NRAS: 验证证书链<br/>对比 RIM
        NRAS-->>CVM: GPU EAT Token
    end

    rect rgb(255, 230, 245)
        Note over CVM,ITA: Phase 4: CPU 远程证明
        CVM->>ITA: TDX Quote
        ITA->>ITA: 验证 TDX 证据
        ITA-->>CVM: CPU EAT Token
    end

    rect rgb(255, 255, 230)
        Note over CVM,KMS: Phase 5: 复合证明 & 密钥分发
        CVM->>ITA: collectCompositeToken<br/>(CPU EAT + GPU EAT)
        ITA->>NRAS: 验证 GPU Token<br/>(Option 1)
        ITA-->>CVM: Composite EAT
        CVM->>KMS: 请求密钥<br/>+ Composite EAT
        KMS->>KMS: 验证复合证明
        KMS-->>CVM: 密封密钥 (Sealed Key)
    end

    rect rgb(240, 240, 240)
        Note over CVM,GPU: Phase 6: 安全流处理
        CVM->>GPU: 加密数据<br/>AES-GCM(K_session)
        GPU->>GPU: 解密 -> 处理 -> 加密
        GPU-->>CVM: 加密结果
    end
```

### 7.3 CPU vs GPU TEE 决策树

```mermaid
flowchart TD
    START[选择机密计算方案] --> Q1{工作负载类型?}

    Q1 -->|通用计算| Q2{数据规模?}
    Q1 -->|AI/ML 推理| Q3{模型大小?}
    Q1 -->|AI/ML 训练| Q4{GPU 可用?}

    Q2 -->|小数据 (<1GB)| SGX[Intel SGX<br/>进程级 TEE]
    Q2 -->|大数据/VM级| Q5{云环境?}

    Q3 -->|< 1B 参数| Q6{延迟敏感?}
    Q3 -->|> 1B 参数| GPU_TEE[GPU TEE<br/>H100 / MI300]

    Q4 -->|是| GPU_TEE_TRAIN[GPU TEE<br/>多卡并行]
    Q4 -->|否| TDX_CPU[Intel TDX<br/>CPU 训练]

    Q5 -->|Azure| TDX_AZURE[Intel TDX<br/>Azure CC]
    Q5 -->|AWS| SEV_AWS[AMD SEV-SNP<br/>AWS CVM]
    Q5 -->|GCP| SEV_GCP[AMD SEV-SNP<br/>GCP CC]
    Q5 -->|私有云| Q7{CPU 厂商?}

    Q6 -->|是| TDX_INF[Intel TDX<br/>低延迟]
    Q6 -->|否| GPU_TEE_INF[GPU TEE<br/>高吞吐]

    Q7 -->|Intel| TDX_PRIV[Intel TDX]
    Q7 -->|AMD| SEV_PRIV[AMD SEV-SNP]

    GPU_TEE --> Q8{GPU 厂商?}
    Q8 -->|NVIDIA| H100[NVIDIA H100<br/>CC Mode + TDX/SNP]
    Q8 -->|AMD| MI300[AMD MI300<br/>Infinity Guard + SNP]

    SGX --> FLINK[Flink TEE 集成]
    TDX_AZURE --> FLINK
    SEV_AWS --> FLINK
    SEV_GCP --> FLINK
    TDX_PRIV --> FLINK
    SEV_PRIV --> FLINK
    TDX_INF --> FLINK
    GPU_TEE_INF --> FLINK
    H100 --> FLINK
    MI300 --> FLINK
    GPU_TEE_TRAIN --> FLINK
```

---

## 8. 引用参考 (References)

[^1]: NVIDIA, "NVIDIA H100 Tensor Core GPU Architecture", GTC 2022 Whitepaper. https://www.advancedclustering.com/wp-content/uploads/2022/03/gtc22-whitepaper-hopper.pdf

[^2]: NVIDIA, "Announcing Confidential Computing General Access on NVIDIA H100 Tensor Core GPUs", NVIDIA Developer Blog, 2024. https://developer.nvidia.com/blog/announcing-confidential-computing-general-access-on-nvidia-h100-tensor-core-gpus/

[^3]: H. Franke et al., "Creating the First Confidential GPUs", Communications of the ACM, 2024. https://cacm.acm.org/practice/creating-the-first-confidential-gpus/

[^4]: J. Zhu et al., "Confidential Computing on Heterogeneous CPU-GPU Systems: Survey and Future Directions", arXiv:2408.11601, 2024. https://arxiv.org/abs/2408.11601

[^5]: Phala Network, "GPU TEE Deep Dive: Securing AI at the Hardware Layer", 2025. https://phala.com/posts/Phala-GPU-TEE-Deep-Dive

[^6]: NVIDIA, "NVIDIA Confidential Computing", Official Documentation. https://docs.nvidia.com/confidential-computing/

[^7]: Intel, "Seamless Attestation of Intel TDX and NVIDIA H100 TEEs with Intel Trust Authority", Intel Community, 2024. https://community.intel.com/t5/Blogs/Products-and-Solutions/Security/Seamless-Attestation-of-Intel-TDX-and-NVIDIA-H100-TEEs-with/post/1525587

[^8]: Phala Network, "Confidential Computing on Nvidia H100 GPU: A Performance Benchmark Study", 2024. https://phala.com/posts/confidential-computing-on-nvidia-h100-gpu-a-performance-benchmark-study

[^9]: AMD, "AMD Infinity Guard", Official Product Page. https://www.amd.com/en/products/processors/server/epyc/infinity-guard.html

[^10]: DMTF, "Security Protocol and Data Model (SPDM) Specification", Version 1.2, 2022.
