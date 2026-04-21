# Real-Time RAG Architecture

> **Language**: English | **Source**: [Knowledge/06-frontier/real-time-rag-architecture.md](../Knowledge/06-frontier/real-time-rag-architecture.md) | **Last Updated**: 2026-04-21

---

## 1. Definitions

### Def-K-06-EN-26: RAG Pipeline

A RAG pipeline is a 4-tuple $\mathcal{P}_{RAG} = (\mathcal{D}, \mathcal{E}, \mathcal{V}, \mathcal{L})$:

- $\mathcal{D}$: Document stream, $d_i = (\text{content}_i, \text{metadata}_i, t_i)$
- $\mathcal{E}$: Embedding function, $\mathcal{E}: \mathcal{D} \rightarrow \mathbb{R}^k$
- $\mathcal{V}$: Vector store, $\mathcal{V} \subset \mathbb{R}^k$, supporting ANN queries
- $\mathcal{L}$: LLM inference, $\mathcal{L}: (q, \mathcal{C}) \rightarrow \text{response}$

### Def-K-06-EN-27: Real-Time Embedding Generation

Stream processing operator $\Phi_{embed}$:

$$
\Phi_{embed}: \text{Stream}(\mathcal{D}) \rightarrow \text{Stream}(\mathbb{R}^k)
$$

$$
\Phi_{embed}(d_t) = \text{ML\_PREDICT}(\text{model}_{emb}, \text{chunk}(d_t))
$$

where $\text{chunk}(\cdot)$ splits documents into semantic chunks, and latency constraint is $L_{embed} < 100\text{ms}$.

### Def-K-06-EN-28: Streaming Context Retrieval

Stateful operator $\Phi_{retrieve}$:

$$
\Phi_{retrieve}: (q_t, \mathcal{V}_t) \rightarrow \mathcal{C}_t
$$

$$
\mathcal{C}_t = \text{TOP\_K}\left\{ v \in \mathcal{V}_t \mid \text{sim}(\mathcal{E}(q_t), v) \geq \theta \right\}
$$

| Strategy | Use Case | Complexity |
|----------|----------|------------|
| HNSW | High-dim dense vectors | $O(\log n)$ |
| IVF | Balanced accuracy/speed | $O(\sqrt{n})$ |
| Flat (brute-force) | Small dataset (< 10K) | $O(n)$ |

## 2. Architecture

```mermaid
graph TB
    subgraph "Ingestion"
        Docs[Documents<br/>Web/API/Files] --> Chunk[Chunking]
        Chunk --> Embed[Embedding Model]
    end
    subgraph "Storage"
        Embed --> VectorDB[(Vector DB<br/>RisingWave/Pinecone/Milvus)]
    end
    subgraph "Query"
        Query[User Query] --> QEmbed[Query Embedding]
        QEmbed --> Retrieve[ANN Retrieval]
        VectorDB --> Retrieve
        Retrieve --> Context[Top-K Context]
        Context --> LLM[LLM Inference]
        LLM --> Response[Generated Response]
    end
```

## 3. Streaming RAG with Flink

```java
// Document ingestion pipeline
DataStream<Document> docs = env
    .addSource(new DocumentSource("kafka-topic"));

DataStream<VectorRecord> vectors = docs
    .map(new ChunkAndEmbed())   // chunk + embed
    .keyBy(v -> v.getPartition())
    .addSink(new VectorDBSink());  // upsert to vector store

// Query serving (separate job or REST API)
DataStream<QueryResult> results = queries
    .mapAsync(new AsyncVectorSearch())  // ANN lookup
    .map(new LLMGenerate());            // LLM with context
```

## 4. Key Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Embedding latency | < 100ms | Per-document p99 |
| Retrieval latency | < 50ms | ANN query p99 |
| Index freshness | < 5s | Watermark lag |
| Relevance (NDCG@5) | > 0.8 | Human evaluation |

## References
