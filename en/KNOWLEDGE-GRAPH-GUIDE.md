# Knowledge Graph Guide

> **Language**: English | **Source**: [KNOWLEDGE-GRAPH/](../KNOWLEDGE-GRAPH/) | **Last Updated**: 2026-04-21

---

## Overview

The AnalysisDataFlow Knowledge Graph is a structured representation of relationships between streaming computation concepts, theorems, definitions, and engineering artifacts. It enables semantic navigation and cross-reference validation.

## Graph Schema

### Entity Types

| Type | Description | Example |
|------|-------------|---------|
| **Concept** | Abstract streaming concept | Watermark, Checkpoint, Backpressure |
| **Theorem** | Formal theorem or lemma | Thm-S-01-01 (exactly-once semantics) |
| **Definition** | Formal definition | Def-S-01-01 (event stream) |
| **Document** | Source document | `Struct/01-foundation/01.01-streaming-semantics.md` |
| **System** | Concrete system or framework | Apache Flink, RisingWave, Kafka Streams |
| **Pattern** | Design or anti-pattern | Event-time join, Global window abuse |

### Relationship Types

| Type | Description | Example |
|------|-------------|---------|
| `depends_on` | Logical dependency | `type_safety` depends_on `progress` |
| `proves` | Proof relationship | `exactly_once_checkpoint_recovery` proves `exactly_once_two_phase_commit` |
| `implements` | Implementation relation | `Flink Checkpoint` implements `Chandy-Lamport` |
| `contradicts` | Contradiction or anti-pattern | `processing_time_bias` contradicts `event_time_semantics` |
| `extends` | Extension or generalization | `DBSP` extends `Differential Dataflow` |

## Usage

### Local Exploration

The knowledge graph data is available in `KNOWLEDGE-GRAPH/data/` as JSON and CSV exports. Use the provided scripts:

```bash
# Build graph from current documents
python .vscode/build-knowledge-graph.py

# Generate learning path from concept A to concept B
python .vscode/generate-learning-path.py --from "Watermark" --to "Exactly-Once"
```

### Web Visualization

A deployed version is available via GitHub Pages at the project documentation site. The visualization uses D3.js for interactive exploration.

## Statistics

- **Entities**: 7,550+ (as of v6.2)
- **Relationships**: 13,000+ cross-references
- **Coverage**: Struct/ Knowledge/ Flink/ en/ directories

## References
