---
title: "A2A Protocol Quick Reference Card"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# A2A Protocol Quick Reference Card

> **Quick Reference**: Google Agent-to-Agent (A2A) protocol core concepts, state transitions, and comparisons
>
> **Full Documents**: [ai-agent-a2a-protocol.md](../06-frontier/ai-agent-a2a-protocol.md) | [a2a-protocol-agent-communication.md](../06-frontier/a2a-protocol-agent-communication.md)

---

## 📋 Core Concepts Quick Reference

### A2A Protocol Sextuple

```text
A2A ≜ ⟨ 𝒜, 𝒯, ℳ, 𝒞, 𝒮, 𝒫 ⟩
```

| Symbol | Component | Description | Analogy |
|--------|-----------|-------------|---------|
| 𝒜 | **Agent Set** | Client Agent + Remote Agent | Service provider and consumer |
| 𝒯 | **Task Space** | Work units with lifecycles | Workflow instance |
| ℳ | **Message Space** | Communication carrier between Agents | HTTP request/response |
| 𝒞 | **Capability Declaration** | Skills described in Agent Card | OpenAPI specification |
| 𝒮 | **Security Mechanism** | OAuth2/mTLS/auditing | Enterprise security stack |
| 𝒫 | **Protocol Primitives** | send/subscribe/cancel/update | REST operations |

### Agent Role Quick Reference

| Role | Responsibility | Typical Scenario |
|------|----------------|------------------|
| **Client Agent** | Task initiation, status monitoring, result aggregation | Orchestrator, master Agent |
| **Remote Agent** | Task execution, producing Artifacts | Domain-specific Agent |
| **Hybrid Agent** | Can both initiate and receive | Intermediate Agent in cascading collaboration |

---

## 🔄 Task Lifecycle State Transitions

### State Machine Quick Reference Diagram

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

### State Quick Reference Table

| State | Semantics | Duration | Transferable Events |
|-------|-----------|----------|---------------------|
| `submitted` | Task created, waiting for assignment | Milliseconds-seconds | start, cancel, fail |
| `working` | Executing | Seconds-hours | complete, need_input, fail, cancel |
| `input_required` | Needs additional input (human-AI collaboration) | Indeterminate (pausable) | provide_input, cancel |
| `completed` | Successfully completed, Artifact available | **Terminal state** | - |
| `failed` | Execution failed, contains error info | **Terminal state** | - |
| `cancelled` | Cancelled | **Terminal state** | - |

### State Transition API Quick Reference

```http
# Submit task
POST /a2a/v1/tasks
{
  "id": "task-123",
  "skill": "analyze-data",
  "input": {...}
}

# Subscribe to status updates (SSE)
GET /a2a/v1/tasks/{task-id}/subscribe

# Provide input (human-AI collaboration node)
POST /a2a/v1/tasks/{task-id}/input
{
  "parts": [...]
}

# Cancel task
POST /a2a/v1/tasks/{task-id}/cancel
```

---

## ⚖️ A2A vs MCP Quick Comparison Table

### Core Differences Matrix

| Dimension | **MCP** (Model Context Protocol) | **A2A** (Agent-to-Agent Protocol) |
|-----------|----------------------------------|-----------------------------------|
| **Abstraction Level** | L2: Model Context Layer | L3: Agent Collaboration Layer |
| **Communication Paradigm** | Hub-and-Spoke (centralized) | Peer-to-Peer (decentralized) |
| **Core Entities** | Resources, Tools, Prompts | Tasks, Messages, Artifacts |
| **State Model** | Stateless (request-response) | Stateful (lifecycle management) |
| **Discovery Mechanism** | Runtime capability negotiation | Pre-declared Agent Card |
| **Interaction Duration** | Milliseconds-seconds | Milliseconds-hours |
| **Relationship Direction** | Agent → Tool (unidirectional) | Agent ↔ Agent (bidirectional) |
| **Primary Use Case** | Tool integration, data retrieval | Agent orchestration, workflow collaboration |
| **Initiator** | Single Host (AI application) | Any Agent |
| **Complexity** | Simple, lightweight | Rich, complete |

### Usage Pattern Decision Tree

```
Usage Scenario Analysis
│
├── Single Agent + Tool Access ──────────────────► MCP Only
│   └─ Example: Customer service Agent queries knowledge base
│
├── Multi-Agent Collaboration ───────────────────► A2A (+ MCP optional)
│   │
│   ├─ Each Agent needs tool access ─────────────► A2A + MCP
│   │   └─ Example: Recruitment workflow Agent coordinates HR, interviewer, background-check Agent
│   │
│   └─ Pure Agent collaboration, no tools ───────► A2A Only
│       └─ Example: Multi-Agent research system
│
└── Hybrid Scenario ─────────────────────────────► A2A + MCP
    └─ Example: Master Agent uses MCP to retrieve data, uses A2A to delegate to analysis Agent
```

### Architecture Layer Relationship

```
┌─────────────────────────────────────────────────────┐
│  L3: Agent Collaboration Layer                      │
│  ┌─────────────────────────────────────────────┐   │
│  │           A2A Protocol                      │   │
│  │     (Agent-to-Agent Communication)          │   │
│  └─────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────┤
│  L2: Model Context Layer                            │
│  ┌─────────────────────────────────────────────┐   │
│  │           MCP Protocol                      │   │
│  │     (Model Context Protocol)                │   │
│  └─────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────┤
│  L1: Model Inference Layer                          │
│  ┌─────────────────────────────────────────────┐   │
│  │           LLM Engine                        │   │
│  │     (GPT/Claude/Gemini, etc.)               │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Agent Card Core Field Quick Reference

### Required Fields

```typescript
{
  // Identification layer
  "name": "string",           // Globally unique identifier
  "url": "string",            // A2A endpoint address
  "version": "string",        // Semantic version

  // Capability layer
  "capabilities": {
    "streaming": boolean,              // Supports SSE streaming
    "pushNotifications": boolean,      // Supports push notifications
    "stateTransitionHistory": boolean  // Provides status history
  },

  // Security layer
  "authentication": {
    "schemes": ["Bearer", "OAuth2", "ApiKey", "mTLS"]
  },

  // Skill layer (core)
  "skills": [{
    "id": "string",
    "name": "string",
    "description": "string",
    "inputModes": ["text/plain", "application/json"],
    "outputModes": ["text/plain", "image/png"]
  }]
}
```

### Discovery URL

```
GET {agent-url}/.well-known/agent.json  →  Returns Agent Card
```

---

## 🚀 Quick Start Code Template

### Python Client Example

```python
import asyncio
import aiohttp

async def invoke_agent(agent_url: str, skill: str, input_data: dict):
    """Invoke Remote Agent"""

    # 1. Discover Agent Card
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{agent_url}/.well-known/agent.json") as resp:
            agent_card = await resp.json()

    # 2. Validate capability match
    target_skill = next(s for s in agent_card["skills"] if s["id"] == skill)

    # 3. Submit task
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

## 📚 Further Reading

| Document | Content |
|----------|---------|
| [ai-agent-a2a-protocol.md](../06-frontier/ai-agent-a2a-protocol.md) | A2A Protocol Complete Deep Dive |
| [a2a-protocol-agent-communication.md](../06-frontier/a2a-protocol-agent-communication.md) | Technical Analysis and Actor Model Relationship |
| [mcp-protocol-agent-streaming.md](../06-frontier/mcp-protocol-agent-streaming.md) | MCP Protocol and Stream Processing Integration |

---

*Quick Reference Card v1.0 | Last Updated: 2026-04-03*
