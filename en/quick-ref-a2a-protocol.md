# A2A Protocol Quick Reference

> **Quick Reference**: Google Agent-to-Agent (A2A) Protocol core concepts, state transitions, and comparison
> **Translation Date**: 2026-04-21

## 1. Core Concepts

### A2A Protocol 6-Tuple

```text
A2A ≜ ⟨ 𝒜, 𝒯, ℳ, 𝒞, 𝒮, 𝒫 ⟩
```

| Symbol | Component | Description | Analogy |
|--------|-----------|-------------|---------|
| 𝒜 | Agent Set | Client + Remote Agents | Service provider/consumer |
| 𝒯 | Task Space | Lifecycle-bound work units | Workflow instances |
| ℳ | Message Space | Inter-Agent communication | HTTP request/response |
| 𝒞 | Capability Declaration | Agent Card skills | OpenAPI spec |
| 𝒮 | Security | OAuth2/mTLS/Audit | Enterprise security stack |
| 𝒫 | Protocol Primitives | send/subscribe/cancel/update | REST operations |

### Agent Roles

| Role | Responsibility | Typical Scenario |
|------|---------------|-----------------|
| Client Agent | Task initiation, monitoring, aggregation | Orchestrator, master Agent |
| Remote Agent | Task execution, artifact production | Domain-specific Agent |
| Hybrid Agent | Both initiate and receive | Cascading collaboration |

---

## 2. Task Lifecycle State Machine

```
Start → submitted → working → completed
                          ↓
                        failed
                          ↓
                        canceled
```

---

## 3. References
