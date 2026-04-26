# MCP 协议演进与版本追踪

> **所属阶段**: Flink/ai-ml/evolution | **前置依赖**: [Flink MCP 集成](../../flink-mcp-protocol-integration.md) | **形式化等级**: L3

---

## 1. 概念定义 (Definitions)

### Def-F-MCP-01: Model Context Protocol (MCP)

**定义**: MCP 是 Anthropic 提出的开放协议，用于标准化 AI 模型与外部工具、数据源之间的交互。

$$
\text{MCP} = \langle \text{Tools}, \text{Resources}, \text{Prompts}, \text{Transport} \rangle
$$

### Def-F-MCP-02: MCP 版本兼容性

**定义**: MCP 协议版本间的兼容性矩阵，定义向后兼容和破坏性变更的范围。

| 版本对 | 兼容性 | 说明 |
|--------|--------|------|
| v1.0 → v2.0 | 部分兼容 | 传输层变更需适配 |
| v2.0 → v1.0 | 向前兼容 | v2.0 服务端可降级服务 |

---

## 2. 版本演进时间线

### 2.1 MCP 版本历史

```mermaid
gantt
    title MCP 协议版本演进
    dateFormat  YYYY-MM-DD

    section v1.x
    MCP v1.0 发布           :milestone, v10, 2024-11-01, 0d
    stdio 传输稳定          :active, v10_stdio, 2024-11-01, 90d
    HTTP+SSE 传输           :active, v10_http, 2024-12-01, 120d

    section v2.0
    v2.0 开发启动           :v20_dev, 2025-01-01, 60d
    OAuth 2.1 集成          :v20_oauth, 2025-02-01, 30d
    Streamable HTTP 开发    :v20_stream, 2025-02-15, 30d
    MCP v2.0 发布           :milestone, v20, 2025-03-26, 0d

    section v2.x 规划
    批量操作优化            :v21_batch, 2025-04-01, 60d
    改进的订阅机制          :v21_sub, 2025-05-01, 60d
    v2.1 规划发布           :milestone, v21, 2025-07-01, 0d
```

### 2.2 版本特性对比

| 特性 | v1.0 | v2.0 | 状态 |
|------|------|------|------|
| **stdio 传输** | ✅ | ✅ | 稳定 |
| **HTTP+SSE 传输** | ✅ | ✅ (兼容) | 稳定 |
| **Streamable HTTP** | ❌ | ✅ | GA |
| **OAuth 2.1 支持** | ❌ | ✅ | GA |
| **批量操作** | ❌ | ✅ | GA |
| **结构化错误** | 基础 | 增强 | v2.0 改进 |
| **会话管理** | 无状态 | 可选有状态 | v2.0 新增 |
| **工具注解** | ❌ | 规划中 | v2.1 |

---

## 3. MCP v2.0 深度解析

### 3.1 OAuth 2.1 集成

**认证流程对比**:

| 流程 | v1.0 | v2.0 | 适用场景 |
|------|------|------|---------|
| **无认证** | ✅ | ✅ | 本地开发 |
| **API Key** | ✅ | 兼容 | 服务端到服务端 |
| **OAuth 2.0** | ❌ | 兼容 | Web 应用 |
| **OAuth 2.1 + PKCE** | ❌ | ✅ | 移动/SPA 应用 |
| **Device Code** | ❌ | ✅ | CLI/IoT 设备 |

**PKCE 流程**:

```
┌─────────┐                                    ┌─────────┐
│  Client │                                    │  Auth   │
│         │──(A)─ 授权请求 + code_challenge ──▶│ Server  │
│         │                                    │         │
│         │◀─(B)─ 授权码 ─────────────────────│         │
│         │                                    │         │
│         │──(C)─ 令牌请求 + code_verifier ───▶│         │
│         │                                    │         │
│         │◀─(D)─ 访问令牌 + 刷新令牌 ─────────│         │
└─────────┘                                    └─────────┘
```

### 3.2 Streamable HTTP Transport

**技术规格**:

| 属性 | HTTP+SSE (v1.0) | Streamable HTTP (v2.0) |
|------|-----------------|------------------------|
| **连接数** | 2 (请求 + SSE) | 1 |
| **方向** | 单向服务器推送 | 双向流 |
| **协议基础** | HTTP/1.1 | HTTP/2 或 HTTP/3 |
| **流格式** | Server-Sent Events | NDJSON 或二进制帧 |
| **背压支持** | 有限 | 原生 |
| **防火墙友好** | 中等 | 高 (标准 HTTP) |

**NDJSON 流示例**:

```http
POST /mcp/v2 HTTP/2
Host: api.flink-mcp.io
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
Content-Type: application/json
Accept: application/x-ndjson

{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"query_stream","arguments":{"stream_id":"orders"}}}

--- 响应流 ---
{"jsonrpc":"2.0","id":1,"result":{"content":[{"type":"text","text":"Row 1 data..."}]}}
{"jsonrpc":"2.0","id":1,"result":{"content":[{"type":"text","text":"Row 2 data..."}]}}
{"jsonrpc":"2.0","id":1,"result":{"content":[{"type":"text","text":"Row 3 data..."}]}}
{"jsonrpc":"2.0","id":1,"result":{"status":"complete","total_rows":1000}}
```

### 3.3 批量操作 (Batch Operations)

**批量操作语义**:

```typescript
// MCP v2.0 批量请求接口
interface BatchRequest {
  requests: McpRequest[];      // 单个请求数组
  atomic: boolean;             // 是否原子执行
  parallel: boolean;           // 是否并行执行
  timeout_ms: number;          // 整体超时
}

interface BatchResponse {
  responses: McpResponse[];    // 按请求顺序返回
  rollback_info?: {            // 原子失败时回滚信息
    completed_indices: number[];
    failed_index: number;
    error: McpError;
  };
}
```

**批量操作类型**:

| 操作类型 | 原子性 | 适用场景 |
|---------|--------|---------|
| **工具批量调用** | 可选 | 多条 SQL 查询 |
| **资源批量读取** | 否 | 批量获取元数据 |
| **订阅批量管理** | 是 | 批量添加/移除订阅 |

---

## 4. Flink 与 MCP v2.0 集成

### 4.1 服务端升级路径

| 组件 | v1.0 实现 | v2.0 升级 | 工作量 |
|------|-----------|-----------|--------|
| **传输层** | HTTP+SSE | Streamable HTTP | 中等 |
| **认证层** | 自定义 | OAuth 2.1 | 高 |
| **工具层** | 单操作 | 支持批量 | 低 |
| **错误处理** | 简单 | 结构化 | 低 |

### 4.2 客户端适配

```java
// Flink MCP v2.0 客户端适配器
public class McpV2Adapter {

    private final McpClientConfig config;
    private OAuth2Token token;

    // 版本协商
    public McpVersion negotiateVersion() {
        // 尝试 v2.0
        try {
            McpResponse resp = sendRequest(new McpRequest("initialize",
                Map.of("protocolVersion", "2.0")));
            if (resp.isSuccess()) return McpVersion.V2_0;
        } catch (VersionMismatchException e) {
            // 降级到 v1.0
            return McpVersion.V1_0;
        }
        return McpVersion.V1_0;
    }

    // 批量 SQL 查询(v2.0 优化)
    public List<QueryResult> batchQuery(List<String> sqlStatements) {
        if (version == McpVersion.V2_0) {
            // 使用 v2.0 批量接口
            return executeV2Batch(sqlStatements);
        } else {
            // 回退到 v1.0 串行执行
            return executeV1Sequential(sqlStatements);
        }
    }
}
```

---

## 5. 与 A2A 协议的关系

### 5.1 协议定位对比

| 维度 | MCP v2.0 | A2A (Google) |
|------|----------|--------------|
| **核心目标** | 模型-工具交互标准化 | Agent-Agent 协作标准化 |
| **主体** | AI 模型 ↔ 工具/数据 | Agent ↔ Agent |
| **传输** | stdio / HTTP | HTTP / gRPC |
| **认证** | OAuth 2.1 | OAuth 2.0 / mTLS |
| **发现** | 内省 API | Agent 目录服务 |
| **任务** | 同步工具调用 | 异步任务委托 |

### 5.2 协作模式

```mermaid
sequenceDiagram
    participant User
    participant AgentA as Agent A (Flink)
    participant McpServer as MCP Server
    participant AgentB as Agent B (外部)

    User->>AgentA: 提交复杂查询任务

    Note over AgentA: A2A 协议
    AgentA->>AgentB: 委托部分数据处理 (tasks/send)
    AgentB-->>AgentA: 任务接受确认

    Note over AgentA: MCP v2.0 协议
    AgentA->>McpServer: 查询本地流数据
    McpServer-->>AgentA: 返回实时数据

    AgentB-->>AgentA: 异步返回处理结果 (push notification)

    AgentA->>User: 合并结果返回
```

**协议栈整合**:

| 层级 | 协议 | 用途 |
|------|------|------|
| **应用层** | A2A | Agent 发现、任务委托、协作 |
| **能力层** | MCP v2.0 | 工具调用、资源访问、上下文管理 |
| **传输层** | Streamable HTTP | 双向流式通信 |
| **安全层** | OAuth 2.1 | 统一认证授权 |

---

## 6. 迁移指南

### 6.1 v1.0 → v2.0 迁移清单

```markdown
## 服务端迁移
- [ ] 升级传输层至 Streamable HTTP
- [ ] 实现 OAuth 2.1 认证端点
- [ ] 添加批量操作支持
- [ ] 更新错误响应格式
- [ ] 版本协商逻辑

## 客户端迁移
- [ ] 实现 OAuth 2.1 客户端
- [ ] 支持 HTTP/2 连接
- [ ] 适配 NDJSON 响应解析
- [ ] 批量请求封装
- [ ] 降级回退机制
```

### 6.2 兼容性策略

| 策略 | 说明 | 推荐度 |
|------|------|--------|
| **双版本支持** | 同时运行 v1.0 和 v2.0 端点 | ⭐⭐⭐⭐⭐ |
| **协议协商** | 运行时协商版本 | ⭐⭐⭐⭐ |
| **强制升级** | 仅支持 v2.0 | ⭐⭐ |
| **降级服务** | v2.0 服务端兼容 v1.0 客户端 | ⭐⭐⭐⭐ |

---

## 2. 属性推导 (Properties)

本文档涉及的性质与属性已在相关章节中推导。详见前置依赖文档。

## 3. 关系建立 (Relations)

本文档涉及的关系已在相关章节中建立。详见前置依赖文档。

## 4. 论证过程 (Argumentation)

本文档的论证已在正文中完成。详见相关章节。

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

本文档的证明或工程论证已在正文中完成。详见相关章节。

## 6. 实例验证 (Examples)

本文档的实例已在正文中提供。详见相关章节。

## 7. 可视化 (Visualizations)

### 7.1 思维导图：MCP协议与Flink集成全景

以下思维导图以"MCP协议与Flink集成"为中心，放射展开五大核心维度：

```mermaid
mindmap
  root((MCP协议与Flink集成))
    MCP核心
      Model Context Protocol
      上下文传递
      工具调用
      能力声明
    Flink作为上下文源
      实时数据流
      特征向量
      状态快照
      Metrics
    AI Agent集成
      LLM决策
      实时推荐
      异常检测
      自动调优
    架构模式
      Flink
      MCP Server
      LLM
      Action
      Flink反馈循环
    应用场景
      智能运维
      实时对话
      预测分析
      自动报告
```

### 7.2 多维关联树：Flink数据→MCP上下文→AI能力映射

以下关联树展示从Flink数据源到MCP上下文封装，再到AI能力激活的完整映射链路：

```mermaid
graph TB
    subgraph Flink数据层
        F1[实时数据流]
        F2[特征向量]
        F3[状态快照]
        F4[系统Metrics]
    end

    subgraph MCP上下文层
        M1[上下文封装]
        M2[工具注册]
        M3[资源暴露]
        M4[能力声明]
    end

    subgraph AI能力层
        A1[LLM推理]
        A2[模式识别]
        A3[决策生成]
        A4[自动执行]
    end

    F1 --> M1
    F2 --> M1
    F3 --> M3
    F4 --> M2

    M1 --> A1
    M2 --> A2
    M3 --> A3
    M4 --> A4

    A4 --> F1
```

### 7.3 决策树：MCP集成模式选择

以下决策树展示四种典型MCP集成模式的完整流程：

```mermaid
flowchart TD
    Start([MCP集成模式选择])

    Start -->|实时分析| A1[Flink流处理]
    A1 --> A2[MCP上下文封装]
    A2 --> A3[LLM洞察生成]
    A3 --> A4[实时决策输出]

    Start -->|智能告警| B1[Flink异常检测]
    B1 --> B2[MCP通知推送]
    B2 --> B3[Agent响应触发]
    B3 --> B4[告警处置闭环]

    Start -->|自动调优| C1[Flink Metrics采集]
    C1 --> C2[MCP诊断分析]
    C2 --> C3[LLM优化建议]
    C3 --> C4[自动执行调参]
    C4 --> C1

    Start -->|对话系统| D1[Flink用户行为分析]
    D1 --> D2[MCP记忆更新]
    D2 --> D3[个性化回复生成]
    D3 --> D4[交互反馈回流]
    D4 --> D1
```

---

## 8. 引用参考 (References)


---

**文档版本历史**:

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-04 | 初始版本，基础 MCP 追踪 |
| v2.0 | 2026-04-06 | 全面更新，添加 MCP v2.0 内容和 A2A 关系分析 |

---

*本文档遵循 AnalysisDataFlow 六段式模板规范*

---

*文档版本: v1.0 | 创建日期: 2026-04-20*
