# RisingWave MCP Server Integration Guide

> **Language**: English | **Source**: [Knowledge/06-frontier/risingwave-mcp-integration-guide.md](../Knowledge/06-frontier/risingwave-mcp-integration-guide.md) | **Last Updated**: 2026-04-21

---

## 1. Definitions

### Def-K-06-EN-440: RisingWave MCP Server

The official RisingWave MCP Server (`risingwavelabs/risingwave-mcp`) is a standardized interface based on the Model Context Protocol, enabling any MCP-compatible AI Agent to directly query real-time materialized views and stream data in RisingWave:

$$
\mathcal{M}_{rw} = \langle \mathcal{C}, \mathcal{S}, \mathcal{Q}, \mathcal{V}, \mathcal{T} \rangle
$$

| Component | Symbol | Description |
|-----------|--------|-------------|
| MCP Client | $\mathcal{C}$ | Any MCP-compatible Agent (Claude, Cursor, custom) |
| MCP Server | $\mathcal{S}$ | `risingwave-mcp` official implementation |
| SQL Query | $\mathcal{Q}$ | SQL → Result via PostgreSQL protocol |
| Vector Search | $\mathcal{V}$ | $\mathbb{R}^d \times k \rightarrow \text{Top-K}$ via HNSW index |
| Materialized View | $\mathcal{T}$ | Incrementally maintained real-time views |

### Def-K-06-EN-441: Agent-Stream-DB Triad

AI Agent, stream database, and MCP protocol form a new data access triad:

$$
\mathcal{A}_{stream} = \langle \text{Agent}, \text{MCP}, \text{RisingWave} \rangle
$$

**Traditional vs. MCP-Stream Architecture**:

| Dimension | Traditional | MCP-Stream |
|-----------|-------------|------------|
| Data access | REST API + SDK | MCP standard protocol |
| Real-time | Polling / cache | Materialized view push |
| Integration cost | Custom per agent | Plug-and-play |
| Query capability | Predefined endpoints | Full SQL + vector search |

## 2. Properties

### Lemma-K-06-EN-440: MCP Server Query Latency Bound

Query latency through RisingWave MCP Server satisfies:

$$
L_{mcp} = L_{protocol} + L_{sql} + L_{network}
$$

where:

- $L_{protocol}$: MCP JSON-RPC serialization (~1ms)
- $L_{sql}$: RisingWave SQL execution (~10-100ms)
- $L_{network}$: Network round-trip (~1-10ms)

**Total latency**: $L_{mcp} \approx 12$-$111$ms, suitable for interactive Agent queries.

### Prop-K-06-EN-440: Zero-Code Integration

Any MCP-compatible AI Agent can access RisingWave data without custom code:

$$
\forall A \in \text{MCP-Compatible}: \text{connect}(A, \mathcal{M}_{rw}) \in O(1)
$$

## 3. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Agent Ecosystem                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    MCP Protocol    ┌─────────────────────┐ │
│  │ Claude      │◄──────────────────►│ RisingWave MCP      │ │
│  │ Cursor      │    stdio/SSE       │ Server              │ │
│  │ Custom Agent│                    │  - list_tables()    │ │
│  └─────────────┘                    │  - query(sql)       │ │
│                                     │  - vector_search()  │ │
│                                     └──────────┬──────────┘ │
│                                                │            │
│                                     PostgreSQL Protocol     │
│                                                │            │
│                                     ┌──────────▼──────────┐ │
│                                     │   RisingWave        │ │
│                                     │  ┌───────────────┐  │ │
│                                     │  │ Materialized  │  │ │
│                                     │  │ Views + HNSW  │  │ │
│                                     │  └───────────────┘  │ │
│                                     └─────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 4. Why RisingWave + MCP for Agent Data Layer?

| Advantage | Explanation |
|-----------|-------------|
| **Real-time** | Agents need "now" data, not yesterday's snapshot. MVs update every 1 second. |
| **Simplicity** | PostgreSQL protocol means standard SQL queries, no new API to learn. |
| **Vector-native** | Agent RAG needs vector search; RisingWave has built-in HNSW. |
| **MCP Standard** | RisingWave becomes an Agent "tool" automatically via MCP Server. |

## 5. Comparison: RisingWave MCP vs. Flink MCP

| Dimension | RisingWave MCP | Flink MCP (Custom) |
|-----------|---------------|-------------------|
| Official support | ✅ `risingwavelabs/risingwave-mcp` | ❌ Community-built |
| Query interface | Native PostgreSQL | REST API / Queryable State |
| Vector search | ✅ Built-in HNSW | ❌ External integration |
| Data freshness | 1-second checkpoint | Checkpoint interval |
| Deployment complexity | Low (single binary) | High (Flink cluster) |
| MCP tool exposure | Auto (all tables/MVs) | Manual registration |

## References
