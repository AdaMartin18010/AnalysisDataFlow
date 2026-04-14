# B-Layer Expert Review List

> **Generated**: 2026-04-15
> **Status**: Translation in progress, pending expert review
> **Policy**: B-layer documents are AI-translated but require technical expert review before being marked as production-ready.

## Overview

The B-layer consists of 10 high-impact technical documents covering Flink core mechanisms, formal methods, design patterns, and API guides. These documents have been translated by AI but contain complex technical concepts that benefit from human expert validation.

## Review Checklist

| # | Source Document (zh) | English Translation Path | Domain | Size (KB) | Translation Status | Reviewer | Review Date | Notes |
|---|---------------------|-------------------------|--------|-----------|-------------------|----------|-------------|-------|
| 1 | `Flink/02-core/checkpoint-mechanism-deep-dive.md` | `i18n/en/Flink/02-core/checkpoint-mechanism-deep-dive.md` | Core Mechanisms | ~58 | `ai_translated_pending_expert_review` | TBD | - | Deep dive on checkpoint internals |
| 2 | `Flink/02-core/exactly-once-semantics-deep-dive.md` | `i18n/en/Flink/02-core/exactly-once-semantics-deep-dive.md` | Core Mechanisms | ~51 | `ai_translated_pending_expert_review` | TBD | - | End-to-end exactly-once semantics |
| 3 | `Flink/02-core/time-semantics-and-watermark.md` | `i18n/en/Flink/02-core/time-semantics-and-watermark.md` | Core Mechanisms | ~52 | `ai_translated_pending_expert_review` | TBD | - | Event time and watermark theory |
| 4 | `Flink/03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md` | `i18n/en/Flink/03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md` | API / SQL | ~62 | `ai_translated_pending_expert_review` | TBD | - | Comprehensive Table API & SQL guide |
| 5 | `Struct/02-properties/02.02-consistency-hierarchy.md` | `i18n/en/Struct/02-properties/02.02-consistency-hierarchy.md` | Formal Methods | ~48 | `ai_translated_pending_expert_review` | TBD | - | Consistency model hierarchy |
| 6 | `Struct/01-foundation/01.01-unified-streaming-theory.md` | `i18n/en/Struct/01-foundation/01.01-unified-streaming-theory.md` | Formal Methods | ~21 | `ai_translated_pending_expert_review` | TBD | - | Unified streaming theory |
| 7 | `Struct/03-relationships/03.05-cross-model-mappings.md` | `i18n/en/Struct/03-relationships/03.05-cross-model-mappings.md` | Formal Methods | ~31 | `ai_translated_pending_expert_review` | TBD | - | Cross-model mappings and encodings |
| 8 | `Knowledge/02-design-patterns/pattern-event-time-processing.md` | `i18n/en/Knowledge/02-design-patterns/pattern-event-time-processing.md` | Design Patterns | ~28 | `ai_translated_pending_expert_review` | TBD | - | Event-time processing patterns |
| 9 | `Knowledge/02-design-patterns/pattern-stateful-computation.md` | `i18n/en/Knowledge/02-design-patterns/pattern-stateful-computation.md` | Design Patterns | ~21 | `ai_translated_pending_expert_review` | TBD | - | Stateful computation patterns |
| 10 | `Knowledge/01-concept-atlas/01.01-stream-processing-fundamentals.md` | `i18n/en/Knowledge/01-concept-atlas/01.01-stream-processing-fundamentals.md` | Concept Atlas | ~35 | `ai_translated_pending_expert_review` | TBD | - | Stream processing fundamentals |

## Review Criteria

Reviewers should focus on the following aspects:

1. **Terminology Accuracy**: Verify that specialized terms (e.g., Checkpoint, Watermark, Backpressure, Exactly-Once, State Backend, CEP) are used correctly and consistently.
2. **Formula & Proof Integrity**: Ensure that all formal definitions (`Def-*`), lemmas (`Lemma-*`), theorems (`Thm-*`), propositions (`Prop-*`), and corollaries (`Cor-*`) are accurately translated.
3. **Code & Configuration**: Validate that code snippets, YAML, and configuration examples are syntactically correct and that inline Chinese comments are appropriately translated.
4. **Mermaid Diagrams**: Confirm that Mermaid graph labels and node text make sense in the English context.
5. **Cross-References**: Check that internal links and references remain valid after path unification (`i18n/en/` structure).

## How to Mark as Reviewed

When a document has been reviewed, update this table and change the frontmatter in the translated document:

```yaml
---
title: "<English Title>"
translation_status: expert_reviewed
source_version: v4.1
last_sync: "2026-04-15"
reviewed_by: "<Reviewer Name>"
reviewed_at: "2026-04-XX"
---
```

## C-Layer Policy Reminder

Documents in `Struct/04-proofs/` (formal theorem proofs) are **C-layer** and are restricted from pure AI translation. Existing AI-translated proof documents in `docs/i18n/en/Struct/04-proofs/` carry explicit `AI-Generated Unverified` warnings and must be reviewed or rewritten by formal-methods experts.
