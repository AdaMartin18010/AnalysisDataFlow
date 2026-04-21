# A2A Protocol Quick Reference

> **Language**: English | **Source**: [Knowledge/98-exercises/quick-ref-a2a-protocol.md](../Knowledge/98-exercises/quick-ref-a2a-protocol.md) | **Last Updated**: 2026-04-21

---

## Core Concepts

### A2A Protocol Sextuple

```text
A2A ≜ ⟨ 𝒜, 𝒯, ℳ, 𝒞, 𝒮, 𝒫 ⟩
```

| Symbol | Component | Description | Analogy |
|--------|-----------|-------------|---------|
| 𝒜 | **Agent Set** | Client Agent + Remote Agent | Service provider & consumer |
| 𝒯 | **Task Space** | Lifecycle-managed work units | Workflow instance |
| ℳ | **Message Space** | Agent-to-agent communication | HTTP request/response |
| 𝒞 | **Capability Declaration** | Skills described in Agent Card | OpenAPI spec |
| 𝒮 | **Security** | OAuth2 / mTLS / audit | Enterprise security stack |
| 𝒫 | **Protocol Primitives** | send / subscribe / cancel / update | REST operations |

### Agent Roles

| Role | Responsibility | Typical Scenario |
|------|----------------|------------------|
| **Client Agent** | Task initiation, status monitoring, result aggregation | Orchestrator, master agent |
| **Remote Agent** | Task execution, artifact production | Domain-specific agent |
| **Hybrid Agent** | Both initiates and receives | Intermediate agent in cascaded collaboration |

## Task Lifecycle State Machine

```
                    ┌─────────────────────────────────────┐
                    │                                     │
                    ▼                                     │
┌──────────┐   submit    ┌─────────┐   start      ┌──────┴───┐
│   Start  │────────────►│Submitted│─────────────►│ Working  │
└──────────┘             └─────────┘              └────┬─────┘
                                                       │
           ┌───────────────────────────────────────────┼───┐
           │                                           │   │
           ▼                                           ▼   │
    ┌──────────┐                               ┌────────┐  │
    │ Completed│◄──────────────────────────────│ Failed │  │
    └──────────┘         retry                 └────────┘  │
           ▲                                               │
           └───────────────────────────────────────────────┘
                            cancel
```

| State | Description | Transitions |
|-------|-------------|-------------|
| **Submitted** | Task received, pending execution | → Working, → Canceled |
| **Working** | Agent actively processing | → Completed, → Failed, → Canceled |
| **Completed** | Task finished successfully | — |
| **Failed** | Error occurred | → Working (retry), → Canceled |
| **Canceled** | Explicitly terminated | — |

## Protocol Primitives

| Primitive | HTTP Method | Description |
|-----------|-------------|-------------|
| `send` | POST /tasks | Submit new task |
| `subscribe` | SSE /tasks/{id}/events | Listen for status updates |
| `cancel` | POST /tasks/{id}/cancel | Abort running task |
| `update` | POST /tasks/{id}/messages | Send additional input mid-task |

## A2A vs MCP Comparison

| Dimension | A2A (Google) | MCP (Anthropic) |
|-----------|--------------|-----------------|
| **Scope** | Agent-to-agent | Agent-to-tool |
| **Unit** | Task (lifecycle) | Tool call (stateless) |
| **Transport** | HTTP + SSE | stdio / HTTP |
| **Discovery** | Agent Card URL | Tool list endpoint |
| **Security** | OAuth2, mTLS | Local process trust |
| **Streaming** | ✅ SSE-based updates | ❌ Request-response |

## References
