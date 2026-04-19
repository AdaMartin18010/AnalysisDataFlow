# A2A协议快速参考卡片

> **快速查阅**: Google Agent-to-Agent (A2A) 协议核心概念、状态转换与对比
>
> **完整文档**: [ai-agent-a2a-protocol.md](../06-frontier/ai-agent-a2a-protocol.md) | [a2a-protocol-agent-communication.md](../06-frontier/a2a-protocol-agent-communication.md)

---

## 📋 核心概念速查

### A2A协议六元组

```text
A2A ≜ ⟨ 𝒜, 𝒯, ℳ, 𝒞, 𝒮, 𝒫 ⟩
```

| 符号 | 组件 | 说明 | 类比 |
|------|------|------|------|
| 𝒜 | **Agent集合** | Client Agent + Remote Agent | 服务提供者与消费者 |
| 𝒯 | **任务空间** | 有生命周期的工作单元 | 工作流实例 |
| ℳ | **消息空间** | Agent间通信载体 | HTTP请求/响应 |
| 𝒞 | **能力声明** | Agent Card描述的技能 | OpenAPI规范 |
| 𝒮 | **安全机制** | OAuth2/mTLS/审计 | 企业安全栈 |
| 𝒫 | **协议原语** | send/subscribe/cancel/update | REST操作 |

### Agent角色速查

| 角色 | 职责 | 典型场景 |
|------|------|----------|
| **Client Agent** | 任务发起、状态监听、结果聚合 | 编排器、主控Agent |
| **Remote Agent** | 任务执行、产出Artifact | 专业领域Agent |
| **Hybrid Agent** | 既可发起也可接收 | 级联协作中的中间Agent |

---

## 🔄 Task生命周期状态转换

### 状态机速查图

```
                    ┌─────────────────────────────────────┐
                    │                                     │
                    ▼                                     │
┌──────────┐   submit    ┌─────────┐   start      ┌──────┴───┐
│   Start  │────────────►│submitted│─────────────►│ working  │
└──────────┘             └─────────┘              └────┬─────┘
                                                       │
           ┌───────────────────────────────────────────┼───┐
           │                                           │   │
           ▼                                           ▼   │
    ┌─────────────┐                           ┌──────────────┐
    │   failed    │◄──────────────────────────│ input_required│
    └──────┬──────┘         fail/complete     └──────┬───────┘
           │                                          │
           │              ┌──────────┐               │
           │              │completed │◄──────────────┘
           └─────────────►│  (final) │   provide_input
                         └──────────┘
                              ▲
                              │ complete
                         ┌────┴─────┐
                         │cancelled │◄──────────────────────┐
                         │ (final)  │                       │
                         └──────────┘                    cancel
```

### 状态速查表

| 状态 | 语义 | 停留时长 | 可转移事件 |
|------|------|----------|------------|
| `submitted` | 任务已创建，等待分配 | 毫秒-秒级 | start, cancel, fail |
| `working` | 正在执行中 | 秒-小时级 | complete, need_input, fail, cancel |
| `input_required` | 需要额外输入（人机协作） | 不确定（可暂停） | provide_input, cancel |
| `completed` | 成功完成，Artifact可用 | **终止状态** | - |
| `failed` | 执行失败，含错误信息 | **终止状态** | - |
| `cancelled` | 已取消 | **终止状态** | - |

### 状态转换API速查

```http
# 提交任务 POST /a2a/v1/tasks
{
  "id": "task-123",
  "skill": "analyze-data",
  "input": {...}
}

# 订阅状态更新 (SSE)
GET /a2a/v1/tasks/{task-id}/subscribe

# 提供输入(人机协作节点)
POST /a2a/v1/tasks/{task-id}/input
{
  "parts": [...]
}

# 取消任务 POST /a2a/v1/tasks/{task-id}/cancel
```

---

## ⚖️ A2A vs MCP 对比速查表

### 核心差异矩阵

| 维度 | **MCP** (Model Context Protocol) | **A2A** (Agent-to-Agent Protocol) |
|------|----------------------------------|-----------------------------------|
| **抽象层级** | L2: 模型上下文层 | L3: Agent协作层 |
| **通信范式** | Hub-and-Spoke（中心化） | Peer-to-Peer（对等） |
| **核心实体** | Resources, Tools, Prompts | Tasks, Messages, Artifacts |
| **状态模型** | 无状态（请求-响应） | 有状态（生命周期管理） |
| **发现机制** | 运行时能力协商 | 预声明Agent Card |
| **交互时长** | 毫秒-秒级 | 毫秒-小时级 |
| **关系方向** | Agent → Tool（单向） | Agent ↔ Agent（双向） |
| **主要用途** | 工具集成、数据获取 | Agent编排、工作流协作 |
| **发起方** | 单一Host (AI应用) | 任意Agent |
| **复杂度** | 简单、轻量 | 丰富、完整 |

### 使用模式决策树

```
使用场景分析
│
├── 单一Agent + 工具访问 ──────────────────► 仅 MCP
│   └─ 例:客服Agent查询知识库
│
├── 多Agent协作 ──────────────────────────► A2A (+ MCP可选)
│   │
│   ├─ 各Agent需访问工具 ────────────────► A2A + MCP
│   │   └─ 例:招聘流程Agent协调HR、面试官、背景调查Agent
│   │
│   └─ 纯Agent协作无工具 ────────────────► 仅 A2A
│       └─ 例:多Agent研究系统
│
└── 混合场景 ─────────────────────────────► A2A + MCP
    └─ 例:主Agent用MCP获取数据,用A2A委托分析Agent
```

### 架构层级关系

```
┌─────────────────────────────────────────────────────┐
│  L3: Agent 协作层                                   │
│  ┌─────────────────────────────────────────────┐   │
│  │           A2A Protocol                      │   │
│  │     (Agent-to-Agent 通信)                    │   │
│  └─────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────┤
│  L2: 模型上下文层                                   │
│  ┌─────────────────────────────────────────────┐   │
│  │           MCP Protocol                      │   │
│  │     (Model Context Protocol)                │   │
│  └─────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────┤
│  L1: 模型推理层                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │           LLM Engine                        │   │
│  │     (GPT/Claude/Gemini等)                    │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Agent Card核心字段速查

### 必备字段

```typescript
{
  // 标识层
  "name": "string",           // 全局唯一标识
  "url": "string",            // A2A端点地址
  "version": "string",        // 语义化版本

  // 能力层
  "capabilities": {
    "streaming": boolean,              // 支持SSE流式
    "pushNotifications": boolean,      // 支持推送通知
    "stateTransitionHistory": boolean  // 提供状态历史
  },

  // 安全层
  "authentication": {
    "schemes": ["Bearer", "OAuth2", "ApiKey", "mTLS"]
  },

  // 技能层 (核心)
  "skills": [{
    "id": "string",
    "name": "string",
    "description": "string",
    "inputModes": ["text/plain", "application/json"],
    "outputModes": ["text/plain", "image/png"]
  }]
}
```

### 发现URL

```
GET {agent-url}/.well-known/agent.json  →  返回Agent Card
```

---

## 🚀 快速开始代码模板

### Python Client示例

```python
import asyncio
import aiohttp

async def invoke_agent(agent_url: str, skill: str, input_data: dict):
    """调用Remote Agent"""

    # 1. 发现Agent Card
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{agent_url}/.well-known/agent.json") as resp:
            agent_card = await resp.json()

    # 2. 验证能力匹配
    target_skill = next(s for s in agent_card["skills"] if s["id"] == skill)

    # 3. 提交任务
    task = {
        "id": f"task-{uuid.uuid4()}",
        "skill": skill,
        "input": {"parts": [{"type": "text", "text": str(input_data)}]}
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{agent_url}/a2a/v1/tasks",
            json=task,
            headers={"Authorization": f"Bearer {token}"}
        ) as resp:
            return await resp.json()
```

---

## 📚 延伸阅读

| 文档 | 内容 |
|------|------|
| [ai-agent-a2a-protocol.md](../06-frontier/ai-agent-a2a-protocol.md) | A2A协议完整深度解析 |
| [a2a-protocol-agent-communication.md](../06-frontier/a2a-protocol-agent-communication.md) | 技术分析与Actor模型关系 |
| [mcp-protocol-agent-streaming.md](../06-frontier/mcp-protocol-agent-streaming.md) | MCP协议与流处理集成 |

---

*快速参考卡片 v1.0 | 最后更新: 2026-04-03*

---

*文档版本: v1.0 | 创建日期: 2026-04-18*
