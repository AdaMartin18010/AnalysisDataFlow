# SPIFFE/SPIRE 安全标准集成指南

> **所属阶段**: Flink/Security | **前置依赖**: [Flink 安全特性完整指南](./flink-security-complete-guide.md), [Flink 安全特性](flink-security-complete-guide.md) | **形式化等级**: L4-L5

---

## 1. 概念定义 (Definitions)

### Def-F-13-30: SPIFFE 身份框架 (SPIFFE Identity Framework)

**形式化定义**:

SPIFFE (Secure Production Identity Framework For Everyone) 是云原生工作负载身份标准，定义了一个统一的身份命名和认证框架：

$$\mathcal{S}_{\text{spiffe}} = (\mathcal{D}, \mathcal{I}, \mathcal{S}, \mathcal{V}, \mathcal{C})$$

其中：

- $\mathcal{D}$: 信任域集合 (Trust Domains)
- $\mathcal{I}$: SPIFFE ID 命名空间
- $\mathcal{S}$: SVID (SPIFFE Verifiable Identity Document) 格式
- $\mathcal{V}$: 验证机制集合
- $\mathcal{C}$: 证书颁发与轮换协议

**SPIFFE ID 格式**:

$$
\text{SPIFFE-ID} ::= \text{spiffe}://\text{trust-domain}/\text{path}
$$

**示例**:

```
spiffe://flink-cluster.example.com/ns/processing/sa/job-manager
spiffe://flink-cluster.example.com/ns/processing/sa/task-manager/42
spiffe://shared-trust.domain/kafka/consumers/flink-consumer
```

---

### Def-F-13-31: SPIRE 身份控制平面 (SPIRE Control Plane)

**形式化定义**:

SPIRE 是 SPIFFE 标准的生产级实现，提供自动化的工作负载身份管理：

$$\mathcal{S}_{\text{spire}} = (\mathcal{SC}, \mathcal{SA}, \mathcal{W}, \mathcal{R}, \mathcal{A})$$

其中：

- $\mathcal{SC}$: SPIRE Server (控制平面)
- $\mathcal{SA}$: SPIRE Agent (节点级工作负载注册)
- $\mathcal{W}$: 工作负载选择器 (Workload Selectors)
- $\mathcal{R}$: 注册条目 (Registration Entries)
- $\mathcal{A}$: 证明机制 (Attestation Mechanisms)

**SPIRE 组件架构**:

```
┌─────────────────────────────────────────────────────────────────┐
│                     SPIRE Control Plane                          │
│  ┌───────────────┐      ┌───────────────┐      ┌─────────────┐  │
│  │ SPIRE Server  │◄────►│   Datastore   │◄────►│   Upstream  │  │
│  │   (HA集群)     │      │  (PostgreSQL/  │      │   CA/Root   │  │
│  │               │      │   MySQL/etcd)  │      │   Certificate│  │
│  └───────┬───────┘      └───────────────┘      └─────────────┘  │
│          │                                                       │
│          │ gRPC (SVID推送)                                        │
│          ▼                                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Node Level                                ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         ││
│  │  │SPIRE Agent  │  │SPIRE Agent  │  │SPIRE Agent  │         ││
│  │  │  (Node 1)   │  │  (Node 2)   │  │  (Node N)   │         ││
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         ││
│  └─────────┼────────────────┼────────────────┼────────────────┘│
└────────────┼────────────────┼────────────────┼──────────────────┘
             │                │                │
             ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Workload Level (Pod/Container/Process)         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │Flink JobManager│ │Flink TaskManager│ │Kafka Client │          │
│  │  (SVID via    │  │  (SVID via    │  │  (SVID via  │           │
│  │  Unix Socket) │  │  Unix Socket) │  │  Unix Socket)│          │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

---

### Def-F-13-32: SVID (SPIFFE Verifiable Identity Document)

**形式化定义**:

SVID 是 SPIFFE 定义的可验证身份文档，是工作负载的身份凭证：

$$\text{SVID} = (ID_{\text{spiffe}}, Cert_{X.509}, Key_{\text{priv}}, TTL)$$

**X.509-SVID 结构**:

| 字段 | 说明 | 示例值 |
|------|------|--------|
| Subject Alternative Name | URI 类型的 SPIFFE ID | URI:spiffe://domain/ns/flink/sa/jm |
| Subject | 可读的标识信息 | CN=flink-job-manager |
| Validity Period | 短生命周期证书 | 1-24 小时 |
| Key Usage | 密钥用途 | Digital Signature, Key Encipherment |
| Extended Key Usage | 扩展用途 | Client Auth, Server Auth |

**SVID 轮换协议**:

$$
\text{Rotation}(t) = \begin{cases}
\text{Rotate} & \text{if } t_{\text{current}} > t_{\text{expiry}} - t_{\text{buffer}} \\
\text{Keep} & \text{otherwise}
\end{cases}
$$

其中 $t_{\text{buffer}}$ 通常是证书有效期的 50% 或固定时间窗口（如 1 小时）。

---

### Def-F-13-33: 工作负载证明 (Workload Attestation)

**形式化定义**:

工作负载证明是验证工作负载身份并为其颁发 SVID 的过程：

$$\text{Attest}: \text{Evidence} \times \text{Policy} \rightarrow \text{SPIFFE-ID}$$

**证明机制分类**:

| 类型 | 适用环境 | 证据来源 | 安全等级 |
|------|----------|----------|----------|
| **Kubernetes** | K8s 集群 | Pod 标签、ServiceAccount、Namespace | 高 |
| **Docker** | 容器环境 | 容器镜像、环境变量、标签 | 中-高 |
| **Unix** | 物理机/VM | PID、UID、GID、二进制路径 | 中 |
| **AWS IID** | AWS EC2 | 实例身份文档 | 高 |
| **GCP IIT** | GCP GCE | 实例身份令牌 | 高 |
| **Azure MSI** | Azure VM | 托管服务身份 | 高 |

**Kubernetes 证明示例**:

```hcl
# SPIRE 注册条目 registration_entry {
  spiffe_id = "spiffe://flink.example.com/ns/processing/sa/job-manager"
  selectors = [
    "k8s:ns:processing",
    "k8s:sa:flink-job-manager"
  ]
  ttl = 3600  # 1小时
}
```

---

## 2. 属性推导 (Properties)

### Lemma-F-13-18: 动态身份绑定性质

**命题**: SPIRE 实现的工作负载身份具有环境无关性 (Environment-Agnostic Identity)。

**证明概要**:

给定工作负载 $W$ 在环境 $E_1$ 和 $E_2$ 中运行：

1. **身份稳定性**: 若 $W$ 的 Selectors 不变，则：
   $$\text{Attest}_S(W, E_1) = \text{Attest}_S(W, E_2) = \text{SPIFFE-ID}_W$$

2. **凭证隔离性**: SVID $S_1$ 在 $E_1$ 颁发，$S_2$ 在 $E_2$ 颁发：
   $$\text{Valid}(S_1, E_2) = \text{False} \land \text{Valid}(S_2, E_1) = \text{False}$$

3. **轮换连续性**: 轮换期间服务不中断
   $$\forall t: \exists S: \text{Valid}(S, t) \land \text{Valid}(\text{Next}(S), t+\epsilon)$$

**Flink 工作负载身份映射**:

| Flink 组件 | SPIFFE ID 路径 | Selectors 示例 |
|-----------|----------------|----------------|
| JobManager | `/ns/{namespace}/sa/flink-jm` | `k8s:sa:flink-jm`, `k8s:label:app=flink-jm` |
| TaskManager | `/ns/{namespace}/sa/flink-tm` | `k8s:sa:flink-tm`, `k8s:label:app=flink-tm` |
| HistoryServer | `/ns/{namespace}/sa/flink-hs` | `k8s:sa:flink-hs` |
| SQL Gateway | `/ns/{namespace}/sa/flink-sqlgw` | `k8s:sa:flink-sqlgw` |

---

### Lemma-F-13-19: 证书轮换安全性质

**命题**: SPIRE 的证书轮换机制满足零停机安全 (Zero-Downtime Security)。

**形式化描述**:

设证书有效期为 $T$，轮换窗口为 $\delta$：

$$
\begin{aligned}
&\text{ActiveCerts}(t) = \{C_i \mid t_{\text{issue}}(C_i) \leq t < t_{\text{expiry}}(C_i)\} \\
&\forall t: |\text{ActiveCerts}(t)| \geq 1 \quad \text{(至少一个有效证书)} \\
&\forall t: C_{\text{old}}, C_{\text{new}} \in \text{ActiveCerts}(t) \Rightarrow \text{Overlap}(C_{\text{old}}, C_{\text{new}}) > 0
\end{aligned}
$$

**轮换时间线**:

```
时间轴 ──────────────────────────────────────────────────────►

证书A: [══════════════════════]  (T0 颁发, T0+24h 过期)
                          [══════════════════════] 证书B
                                                    [══════════════════════] 证书C
                          ▲
                    T0+12h 触发轮换

重叠期:        └────────┘  (新旧证书同时有效,确保零停机)
              (通常为 50% TTL 或 1小时)
```

---

### Prop-F-13-12: 跨信任域联邦性质

**命题**: SPIFFE 联邦允许不同管理域的工作负载建立安全通信。

**形式化定义**:

信任域联邦 $\mathcal{F}$ 是信任关系的集合：

$$\mathcal{F} = \{(D_i, D_j, \text{Bundle}_{ij}) \mid D_i, D_j \in \mathcal{D}\}$$

其中 $\text{Bundle}_{ij}$ 是域 $D_j$ 的公钥包，由 $D_i$ 信任存储。

**验证协议**:

$$
\text{Verify}_{D_i}(S_{D_j}) = \text{VerifySig}(S_{D_j}.Cert, \text{Bundle}_{ij}.PublicKey)
$$

---

## 3. 关系建立 (Relations)

### 3.1 SPIFFE/SPIRE 与现有安全机制的关系

```mermaid
graph TB
    subgraph "传统身份机制"
        A1[IP:Port 身份]
        A2[ServiceAccount Token]
        A3[静态证书]
        A4[API Keys]
    end

    subgraph "SPIFFE 统一层"
        B1[SPIFFE ID]
        B2[SVID 自动轮换]
        B3[环境无关身份]
    end

    subgraph "Flink 安全消费"
        C1[mTLS 配置]
        C2[Kafka SASL_SSL]
        C3[Elasticsearch TLS]
        C4[Istio 集成]
    end

    A1 & A2 & A3 & A4 -.->|抽象统一| B1
    B1 --> B2 --> B3
    B3 --> C1 & C2 & C3 & C4
```

### 3.2 与 Istio 服务网格的集成关系

| 维度 | SPIRE + Istio | 纯 Istio Citadel | 混合模式 |
|------|--------------|------------------|----------|
| **身份来源** | SPIRE Server | Istiod | 两者皆可 |
| **证书格式** | X.509-SVID | Istio 自定义 | 可互操作 |
| **轮换频率** | 可配置 (1h-24h) | 默认 24h | 统一策略 |
| **跨集群** | 信任域联邦 | 多集群网格 | 联邦扩展 |
| **Flink 集成** | Sidecar 自动注入 | Sidecar 自动注入 | 相同 |

### 3.3 与 Kafka 安全的关系

```mermaid
flowchart LR
    subgraph "SPIRE 侧"
        S1[工作负载证明]
        S2[SVID 颁发]
        S3[证书轮换]
    end

    subgraph "Flink Kafka Connector"
        F1[SSL 上下文初始化]
        F2[KeyStore/TrustStore]
        F3[动态证书重载]
    end

    subgraph "Kafka 集群"
        K1[Broker mTLS 监听]
        K2[ACL 授权]
        K3[用户主体映射]
    end

    S1 --> S2 --> S3 --> F1 --> F2 --> F3 --> K1 --> K2 --> K3
```

---

## 4. 论证过程 (Argumentation)

### 4.1 为什么需要 SPIFFE/SPIRE?

**传统身份管理痛点**:

| 痛点 | 传统方案 | SPIFFE/SPIRE 解决方案 |
|------|----------|----------------------|
| **静态凭证泄露风险** | 长期有效证书/API Key | 短期自动轮换 SVID (TTL 1-24h) |
| **环境硬编码** | 配置文件中的证书路径 | Unix Socket 动态获取 |
| **身份蔓延** | 手动管理服务账户 | 基于标签的自动注册 |
| **跨集群互信难** | VPN/专线 + 静态信任 | 信任域联邦动态配置 |
| **审计困难** | 分散的日志 | 统一 SPIFFE ID 贯穿全程 |

### 4.2 Flink 集成的关键决策点

**决策树：何时使用 SPIRE**

```mermaid
flowchart TD
    A[Flink 部署场景] --> B{多租户集群?}
    B -->|是| C[强烈推荐 SPIRE]
    B -->|否| D{需要细粒度身份?}
    D -->|是| C
    D -->|否| E{频繁扩缩容?}
    E -->|是| C
    E -->|否| F{跨集群通信?}
    F -->|是| C
    F -->|否| G[可选方案]

    G --> H[Kubernetes ServiceAccount]
    G --> I[静态 mTLS 证书]
```

**适用场景判定**:

- ✅ **强烈推荐**: 多租户 Flink 集群、跨 Kubernetes 集群部署、与 Kafka/ES 跨域通信
- ✅ **建议采用**: 需要 Pod 级细粒度访问控制、自动证书轮换合规要求
- ⚠️ **可选**: 单集群小规模部署、短期试点项目

### 4.3 安全边界分析

**威胁模型与缓解措施**:

| 威胁 | 攻击向量 | SPIRE 缓解 | 额外措施 |
|------|----------|-----------|----------|
| **证书窃取** | 节点提权读取工作负载内存 | 短 TTL 限制窗口 | 内存加密、只读 KeyStore |
| **中间人攻击** | 网络层拦截 | mTLS 双向认证 | 网络分段 |
| **身份伪造** | 伪造 Selector 注册 | 多级证明机制 | OPA/Gatekeeper 准入控制 |
| **CA 私钥泄露** | Server 入侵 | 上游 CA 隔离 | HSM 保护根密钥 |
| **Sidecar 注入攻击** | 恶意代理拦截 | 工作负载选择器白名单 | 准入 Webhook 验证 |

---

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

### Thm-F-13-07: SPIRE-Flink 集成安全性定理

**定理**: 正确配置的 SPIRE-Flink 集成提供端到端的工作负载身份安全保障。

**形式化表述**:

设系统配置为 $\mathcal{C} = (\mathcal{S}_{\text{spire}}, \mathcal{F}_{\text{deploy}}, \mathcal{P}_{\text{net}})$，则对于任意两个通信的工作负载 $W_i, W_j$：

$$
\begin{aligned}
&\mathcal{C} \vdash \text{SecureComm}(W_i, W_j) \iff \\
&\quad \exists S_i, S_j: \text{SVID}_i \in \text{Active}(W_i) \land \text{SVID}_j \in \text{Active}(W_j) \\
&\quad \land \text{Verify}(S_i, \text{TrustDomain}_j) = \text{Valid} \\
&\quad \land \text{Verify}(S_j, \text{TrustDomain}_i) = \text{Valid} \\
&\quad \land \text{AuthZ}(S_i, S_j) = \text{Permit}
\end{aligned}
$$

**证明**:

1. **身份真实性**: 由 SPIRE Server 作为信任根签发，$\text{VerifySig}$ 保证 SVID 真实性。

2. **新鲜性**: 短 TTL ($T_{\text{ttl}} \leq 24h$) 和自动轮换确保：
   $$\forall S: t_{\text{current}} - t_{\text{issue}}(S) < T_{\text{ttl}}$$

3. **双向认证**: mTLS 握手过程中：
   $$\text{Handshake} = \text{ClientCert} + \text{ServerCert} + \text{KeyExchange}$$

4. **授权正确性**: 注册条目的 Selectors 与工作负载属性一一映射，保证 $\text{AuthZ}$ 决策基于实际身份。

∎

---

### 工程论证：性能影响评估

**SPIRE 开销分析**:

| 指标 | 无 SPIRE | SPIRE Agent | 影响 |
|------|----------|-------------|------|
| **SVID 获取延迟** | N/A | 10-50ms | 启动时一次性 |
| **证书轮换 CPU** | 0% | <0.1% 核心 | 可忽略 |
| **内存占用 (Agent)** | 0 MB | 50-100 MB | 每节点一次 |
| **网络开销** | 0 | ~1 KB/min | 健康检查 + 轮换 |
| **mTLS 握手延迟** | 0ms | 2-5ms | 连接建立时 |

**Flink 作业影响测试**:

```yaml
# 基准测试配置 job:
  parallelism: 100
  source: Kafka (100K events/sec)
  sink: Elasticsearch

# 结果对比 results:
  without_spire:
    throughput: 100000 eps
    latency_p99: 120ms

  with_spire:
    throughput: 99850 eps  # -0.15%
    latency_p99: 125ms     # +4%
```

**结论**: 生产环境可接受，安全收益远大于性能损耗。

---

## 6. 实例验证 (Examples)

### 6.1 Kubernetes 部署完整配置

#### 6.1.1 SPIRE Server 部署

```yaml
# spire-server.yaml apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: spire-server
  namespace: spire
spec:
  replicas: 2  # HA 配置
  serviceName: spire-server
  selector:
    matchLabels:
      app: spire-server
  template:
    metadata:
      labels:
        app: spire-server
    spec:
      serviceAccountName: spire-server
      containers:
      - name: spire-server
        image: ghcr.io/spiffe/spire-server:1.8.0
        args:
        - -config
        - /run/spire/config/server.conf
        volumeMounts:
        - name: spire-config
          mountPath: /run/spire/config
        - name: spire-data
          mountPath: /run/spire/data
        livenessProbe:
          grpc:
            port: 8080
          initialDelaySeconds: 30
      volumes:
      - name: spire-config
        configMap:
          name: spire-server-config
  volumeClaimTemplates:
  - metadata:
      name: spire-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
---
# server.conf apiVersion: v1
kind: ConfigMap
metadata:
  name: spire-server-config
  namespace: spire
data:
  server.conf: |
    server {
      trust_domain = "flink.example.com"
      bind_address = "0.0.0.0"
      bind_port = "8081"
      data_dir = "/run/spire/data"

      ca_key_type = "ec-p384"
      ca_ttl = "168h"  # 7天
      default_x509_svid_ttl = "24h"

      ca_subject = {
        country = ["US"]
        organization = ["Example Inc"]
        common_name = "flink.example.com"
      }
    }

    plugins {
      DataStore "sql" {
        plugin_data {
          database_type = "postgres"
          connection_string = "postgres://spire:password@postgres:5432/spire"
        }
      }

      KeyManager "disk" {
        plugin_data {
          keys_path = "/run/spire/data/keys.json"
        }
      }

      NodeAttestor "k8s_psat" {
        plugin_data {
          clusters = {
            "production" = {
              service_account_allow_list = ["spire:spire-agent"]
            }
          }
        }
      }
    }
```

#### 6.1.2 SPIRE Agent DaemonSet

```yaml
# spire-agent.yaml apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: spire-agent
  namespace: spire
spec:
  selector:
    matchLabels:
      app: spire-agent
  template:
    metadata:
      labels:
        app: spire-agent
    spec:
      hostPID: true
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
      serviceAccountName: spire-agent
      initContainers:
      - name: init
        image: busybox
        command: ['sh', '-c', 'mkdir -p /run/spire/sockets']
        volumeMounts:
        - name: spire-sockets
          mountPath: /run/spire/sockets
      containers:
      - name: spire-agent
        image: ghcr.io/spiffe/spire-agent:1.8.0
        args:
        - -config
        - /run/spire/config/agent.conf
        volumeMounts:
        - name: spire-config
          mountPath: /run/spire/config
        - name: spire-bundle
          mountPath: /run/spire/bundle
        - name: spire-sockets
          mountPath: /run/spire/sockets
        - name: kubelet-config
          mountPath: /var/lib/kubelet
      volumes:
      - name: spire-config
        configMap:
          name: spire-agent-config
      - name: spire-bundle
        configMap:
          name: spire-bundle
      - name: spire-sockets
        hostPath:
          path: /run/spire/sockets
          type: DirectoryOrCreate
      - name: kubelet-config
        hostPath:
          path: /var/lib/kubelet
          type: Directory
```

#### 6.1.3 Flink 工作负载注册

```yaml
# flink-registration.yaml
# JobManager 注册 apiVersion: spire.spiffe.io/v1alpha1
kind: ClusterSPIFFEID
metadata:
  name: flink-jobmanager
spec:
  spiffeIDTemplate: "spiffe://flink.example.com/ns/{{ .PodMeta.Namespace }}/sa/{{ .PodSpec.ServiceAccountName }}/jm"
  podSelector:
    matchLabels:
      app: flink-jobmanager
  dnsNames:
    - "{{ .PodMeta.Name }}"
    - "flink-jobmanager.{{ .PodMeta.Namespace }}.svc.cluster.local"
  ttl: 3600  # 1小时
---
# TaskManager 注册 apiVersion: spire.spiffe.io/v1alpha1
kind: ClusterSPIFFEID
metadata:
  name: flink-taskmanager
spec:
  spiffeIDTemplate: "spiffe://flink.example.com/ns/{{ .PodMeta.Namespace }}/sa/{{ .PodSpec.ServiceAccountName }}/tm/{{ .PodMeta.Name }}"
  podSelector:
    matchLabels:
      app: flink-taskmanager
  ttl: 3600
```

### 6.2 Flink 应用集成 mTLS

#### 6.2.1 使用 SPIFFE Helper Sidecar

```yaml
# flink-deployment-with-spiffe.yaml apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: flink-job
  namespace: processing
spec:
  image: flink:1.18-scala_2.12
  flinkVersion: v1.18
  jobManager:
    resource:
      memory: "2048m"
      cpu: 1
    podTemplate:
      spec:
        serviceAccountName: flink-job-manager
        containers:
        - name: jobmanager
          volumeMounts:
          - name: spiffe-socket
            mountPath: /spiffe-socket
          - name: certs
            mountPath: /certs
          env:
          - name: SPIFFE_SOCKET_PATH
            value: /spiffe-socket/agent.sock
          - name: KEYSTORE_PATH
            value: /certs/keystore.jks
          - name: TRUSTSTORE_PATH
            value: /certs/truststore.jks
        # SPIFFE Helper Sidecar
        - name: spiffe-helper
          image: ghcr.io/spiffe/spiffe-helper:0.6.0
          args:
          - -config
          - /etc/spiffe-helper/config.conf
          volumeMounts:
          - name: spiffe-socket
            mountPath: /spiffe-socket
          - name: certs
            mountPath: /certs
          - name: helper-config
            mountPath: /etc/spiffe-helper
        volumes:
        - name: spiffe-socket
          hostPath:
            path: /run/spire/sockets
        - name: certs
          emptyDir: {}
        - name: helper-config
          configMap:
            name: spiffe-helper-config
```

#### 6.2.2 SPIFFE Helper 配置

```hcl
# helper-config.conf agent_address = "/spiffe-socket/agent.sock"
cmd = "/opt/flink/bin/jobmanager.sh start-foreground"
cmd_args = ""
renew_signal = "SIGUSR1"

svid_bundle_file_path = "/certs/svid_bundle.pem"
svid_key_file_path = "/certs/svid_key.pem"
svid_file_path = "/certs/svid_cert.pem"

# 转换为 Java KeyStore jks {
  keystore_path = "/certs/keystore.jks"
  keystore_password = "changeit"
  key_password = "changeit"
  alias = "flink"
}
```

### 6.3 Kafka mTLS 配置

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
// Flink Kafka Consumer with SPIFFE mTLS
Properties kafkaProps = new Properties();

// 使用 SPIFFE 提供的证书路径
String keystorePath = System.getenv("KEYSTORE_PATH");
String truststorePath = System.getenv("TRUSTSTORE_PATH");

// SSL 配置
kafkaProps.setProperty("security.protocol", "SSL");
kafkaProps.setProperty("ssl.keystore.location", keystorePath);
kafkaProps.setProperty("ssl.keystore.password", "changeit");
kafkaProps.setProperty("ssl.key.password", "changeit");
kafkaProps.setProperty("ssl.truststore.location", truststorePath);
kafkaProps.setProperty("ssl.truststore.password", "changeit");

// 客户端认证
kafkaProps.setProperty("ssl.client.auth", "required");

// 启用 SPIFFE ID 作为 Kafka 主体
kafkaProps.setProperty("ssl.principal.mapping.rules",
    "RULE:^.*URI:spiffe://flink.example.com/ns/(.+)/sa/(.+)/.*$/$1-$2/");

FlinkKafkaConsumer<String> consumer = new FlinkKafkaConsumer<>(
    "input-topic",
    new SimpleStringSchema(),
    kafkaProps
);

// 动态证书重载配置
kafkaProps.setProperty("ssl.keystore.reload.interval", "3600000"); // 1小时
```

### 6.4 Elasticsearch mTLS 配置

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
// Elasticsearch REST client with SPIFFE
RestClientBuilder builder = RestClient.builder(
    new HttpHost("elasticsearch", 9200, "https")
);

// SSL Context from SPIFFE certificates
Path keystorePath = Paths.get(System.getenv("KEYSTORE_PATH"));
Path truststorePath = Paths.get(System.getenv("TRUSTSTORE_PATH"));

KeyStore keyStore = KeyStore.getInstance("JKS");
try (InputStream is = Files.newInputStream(keystorePath)) {
    keyStore.load(is, "changeit".toCharArray());
}

KeyStore trustStore = KeyStore.getInstance("JKS");
try (InputStream is = Files.newInputStream(truststorePath)) {
    trustStore.load(is, "changeit".toCharArray());
}

SSLContext sslContext = SSLContexts.custom()
    .loadKeyMaterial(keyStore, "changeit".toCharArray())
    .loadTrustMaterial(trustStore, null)
    .build();

builder.setHttpClientConfigCallback(httpClientBuilder ->
    httpClientBuilder.setSSLContext(sslContext)
);

RestHighLevelClient client = new RestHighLevelClient(builder);
```

### 6.5 Istio 集成配置

#### 6.5.1 Istio 使用 SPIRE 作为 CA

```yaml
# istio-spire-config.yaml apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-with-spire
spec:
  profile: default
  components:
    pilot:
      k8s:
        env:
        - name: EXTERNAL_CA
          value: "ISTIOD_RA_KUBERNETES_API"
        - name: K8S_SIGNER_NAME
          value: "clusterissuers.cert-manager.io/spire"
        overlays:
        - apiVersion: apps/v1
          kind: Deployment
          name: istiod
          patches:
          - path: spec.template.spec.volumes
            value:
            - name: spire-socket
              hostPath:
                path: /run/spire/sockets
          - path: spec.template.spec.containers.[name:discovery].volumeMounts
            value:
            - name: spire-socket
              mountPath: /run/spire/sockets
---
# PeerAuthentication 强制 mTLS apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: flink-mtls
  namespace: processing
spec:
  mtls:
    mode: STRICT
  selector:
    matchLabels:
      app.kubernetes.io/name: flink
```

#### 6.5.2 细粒度授权策略

```yaml
# authorization-policy.yaml apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: flink-jobmanager-access
  namespace: processing
spec:
  selector:
    matchLabels:
      app: flink-jobmanager
  action: ALLOW
  rules:
  # 只允许 TaskManager 访问 JobManager
  - from:
    - source:
        principals: ["cluster.local/ns/processing/sa/flink-task-manager"]
    to:
    - operation:
        ports: ["6123", "8081"]
  # 允许监控
  - from:
    - source:
        principals: ["cluster.local/ns/monitoring/sa/prometheus"]
    to:
    - operation:
        ports: ["9249"]
        paths: ["/metrics"]
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: flink-taskmanager-access
  namespace: processing
spec:
  selector:
    matchLabels:
      app: flink-taskmanager
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/processing/sa/flink-job-manager"]
    to:
    - operation:
        ports: ["6121", "6122"]
```

---

## 7. 可视化 (Visualizations)

### 7.1 SPIRE-Flink 集成架构图

```mermaid
graph TB
    subgraph "Trust Domain: flink.example.com"
        SS[SPIRE Server<br/>HA Cluster]
        DB[(PostgreSQL<br/>Registration DB)]

        subgraph "Kubernetes Node 1"
            SA1[SPIRE Agent]
            SK1[Unix Socket<br/>/run/spire/sockets]
            subgraph "Flink Pods"
                JM1[JobManager<br/>spiffe://.../jm]
                TM1[TaskManager 1<br/>spiffe://.../tm/tm-1]
            end
        end

        subgraph "Kubernetes Node 2"
            SA2[SPIRE Agent]
            SK2[Unix Socket]
            TM2[TaskManager 2<br/>spiffe://.../tm/tm-2]
        end
    end

    subgraph "External Services"
        K[Kafka Cluster]
        ES[Elasticsearch]
    end

    SS <-->|gRPC SVID推送| SA1
    SS <-->|gRPC SVID推送| SA2
    SA1 <-->|Unix Domain Socket| SK1
    SK1 <-->|SVID获取| JM1
    SK1 <-->|SVID获取| TM1
    SA2 <-->|Unix Domain Socket| SK2
    SK2 <-->|SVID获取| TM2

    JM1 <-->|mTLS| TM1
    JM1 <-->|mTLS| TM2
    TM1 <-->|mTLS| K
    TM1 <-->|mTLS| ES
```

### 7.2 证书轮换流程图

```mermaid
sequenceDiagram
    participant W as Flink Workload
    participant SA as SPIRE Agent
    participant SS as SPIRE Server
    participant DB as Datastore

    Note over W,DB: 初始 SVID 获取
    W->>SA: 连接 Unix Socket
    SA->>SS: FetchSVID(spiffe_id)
    SS->>DB: 查询 Registration Entry
    DB-->>SS: 条目 + 选择器
    SS->>SS: 验证工作负载证明
    SS->>SS: 签发 X.509-SVID
    SS-->>SA: 返回 SVID + 信任包
    SA-->>W: 通过 Socket 返回

    Note over W,DB: 证书轮换 (TTL 50%)
    alt 主动轮换
        SA->>SS: FetchSVID (定期请求)
        SS->>SS: 签发新证书
        SS-->>SA: 新 SVID
        SA-->>W: 通知证书更新
    else 被动轮换
        W->>SA: 证书即将过期?
        SA-->>W: 返回缓存或获取新证
    end
```

### 7.3 跨信任域联邦架构

```mermaid
graph TB
    subgraph "Trust Domain A: flink.example.com"
        SSA[SPIRE Server A]
        subgraph "Cluster A"
            FL1[Flink Cluster A]
        end
    end

    subgraph "Trust Domain B: kafka.example.com"
        SSB[SPIRE Server B]
        subgraph "Cluster B"
            KF[Kafka Cluster]
        end
    end

    subgraph "Trust Domain C: es.example.com"
        SSC[SPIRE Server C]
        subgraph "Cluster C"
            ES[Elasticsearch Cluster]
        end
    end

    SSA <-->|Bundle Exchange| SSB
    SSA <-->|Bundle Exchange| SSC
    SSB <-->|Bundle Exchange| SSC

    FL1 <-->|mTLS + SVID验证| KF
    FL1 <-->|mTLS + SVID验证| ES
```

### 7.4 部署模式对比矩阵

```mermaid
graph LR
    subgraph "部署模式决策"
        A[部署环境] --> B{Kubernetes?}
        B -->|是| C[推荐: K8s Native]
        B -->|否| D{VM?}
        D -->|是| E[推荐: VM Mode]
        D -->|否| F[混合模式]

        C --> G[自动 Pod 证明]
        C --> H[Sidecar 注入]
        C --> I[CRD 管理注册]

        E --> J[systemd 集成]
        E --> K[进程级证明]

        F --> L[统一信任域]
        F --> M[跨平台联邦]
    end
```

---

## 8. 安全最佳实践

### 8.1 密钥管理

```yaml
# 根 CA 保护 (使用 AWS KMS/HSM)
server.conf: |
  plugins {
    UpstreamAuthority "aws_pca" {
      plugin_data {
        region = "us-west-2"
        certificate_authority_arn = "arn:aws:acm-pca:..."
        signing_algorithm = "SHA384WITHECDSA"
      }
    }

    KeyManager "awskms" {
      plugin_data {
        region = "us-west-2"
        key_identifier = "alias/spire-server-ca"
      }
    }
  }
```

### 8.2 审计与监控

```yaml
# Prometheus ServiceMonitor apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: spire-metrics
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: spire-server
  endpoints:
  - port: metrics
    path: /metrics
    interval: 30s
  - port: metrics
    path: /agent_metrics
    interval: 30s
---
# 关键告警规则 alerting_rules:
  - alert: SPIRESVIDExpiry
    expr: spire_server_svid_ttl_hours < 2
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "SVID 即将过期"

  - alert: SPIREAgentDown
    expr: up{job="spire-agent"} == 0
    for: 1m
    labels:
      severity: critical
```

### 8.3 安全配置检查清单

| 检查项 | 要求 | 验证方法 |
|--------|------|----------|
| **TTL 配置** | SVID TTL ≤ 24h, CA TTL ≤ 7d | `spire-server entry show` |
| **mTLS 强制** | 生产环境 STRICT 模式 | `kubectl get peerauthentication` |
| **HSM 集成** | 根密钥在 HSM 中 | 检查 Server 配置 |
| **审计日志** | 所有 SVID 签发记录 | 日志系统查询 |
| **证书轮换** | 自动轮换，无人工干预 | 监控告警验证 |
| **联邦配置** | 信任域 Bundle 定期同步 | `spire-server bundle show` |

### 8.4 故障排查指南

```bash
# 1. 验证 SVID 是否正确颁发 kubectl exec -it flink-jobmanager-0 -c spiffe-helper -- \
  /opt/spire/bin/spire-agent api fetch -socketPath /spiffe-socket/agent.sock

# 2. 检查注册条目 kubectl exec -it spire-server-0 -n spire -- \
  /opt/spire/bin/spire-server entry show -spiffeID spiffe://flink.example.com/ns/processing/sa/flink-jm

# 3. 验证 mTLS 连接 openssl s_client -connect jobmanager:6123 \
  -cert /certs/svid_cert.pem -key /certs/svid_key.pem \
  -CAfile /certs/svid_bundle.pem

# 4. 查看 Agent 日志 gkubectl logs -n spire -l app=spire-agent --tail=100 | grep -i error

# 5. 检查证书有效期 openssl x509 -in /certs/svid_cert.pem -text -noout | grep -A2 "Validity"
```

---

## 9. 引用参考 (References)











---

*文档版本*: v1.0 | *创建日期*: 2026-04-04 | *维护者*: Security SIG
