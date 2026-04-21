# Search Guide

> **Language**: Bilingual (Chinese/English) | **Last Updated**: 2026-04-21

---

## How to Navigate This Knowledge Base

With 800+ documents across `Struct/`, `Knowledge/`, `Flink/`, and `en/`, effective search is essential.

## By Directory

| Directory | Content | Best For |
|-----------|---------|----------|
| `Struct/` | Formal theories, proofs, definitions | Researchers, academics |
| `Knowledge/` | Design patterns, best practices, case studies | Engineers, architects |
| `Flink/` | Flink-specific architecture, APIs, roadmap | Flink users, operators |
| `en/` | English translations | International readers |
| `formal-methods/` | Coq/Lean/TLA+ code | Formal verification practitioners |

## By Topic Keywords

| Keyword | Primary Location |
|---------|-----------------|
| Exactly-Once | `Struct/04-proofs/`, `Flink/02-core/` |
| Watermark | `Flink/02-core/`, `Struct/01-foundation/` |
| Checkpoint | `Flink/02-core/checkpoint*.md` |
| Backpressure | `Flink/02-core/`, `Knowledge/02-design-patterns/` |
| CEP | `Flink/03-api/`, `Knowledge/02-design-patterns/` |
| State Backend | `Flink/02-core/`, `Knowledge/07-best-practices/` |

## By Document Numbering

Formal elements use unified numbering: `{Type}-{Stage}-{DocSeq}-{Order}`

| Type | Prefix | Example |
|------|--------|---------|
| Theorem | `Thm` | `Thm-S-01-01` |
| Definition | `Def` | `Def-K-03-01` |
| Lemma | `Lemma` | `Lemma-F-02-01` |

## By Mermaid Diagrams

Over 3,600 Mermaid diagrams are embedded. Search for ` ```mermaid ` in any directory.

## Quick Entry Points

- **New to streaming**: [QUICK-START.md](QUICK-START.md)
- **Flink quick start**: [en/FLINK-QUICK-START.md](en/FLINK-QUICK-START.md)
- **Glossary**: [en/GLOSSARY.md](en/GLOSSARY.md)
- **Project status**: [PROJECT-TRACKING.md](PROJECT-TRACKING.md)
