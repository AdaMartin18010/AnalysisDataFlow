# LLM-Guided Formal Proof Automation

> **Stage**: Struct/06-frontier | **Prerequisites**: [Formal Verification Methods](formal-verification-methods.md) | **Formalization Level**: L5-L6
> **Translation Date**: 2026-04-21

## Abstract

Systematic analysis of LLM-assisted formal proof automation (LFPA) across TLA+, Coq, and Lean 4.

---

## 1. Definitions

### LFPA System

$$\mathcal{LFPA} = \langle \mathcal{M}, \mathcal{T}, \mathcal{P}, \mathcal{G}, \mathcal{V}, \mathcal{S}, \mathcal{F} \rangle$$

- $\mathcal{M}$: LLM
- $\mathcal{T}$: proof assistant (TLA+/Coq/Lean)
- $\mathcal{P}$: proof context
- $\mathcal{G}$: goal state
- $\mathcal{V}$: verifier
- $\mathcal{S}$: success metric
- $\mathcal{F}$: feedback loop

---

## 2. Benchmarks (2025-2026)

| Model | Distributed Protocols | General Math |
|-------|----------------------|--------------|
| Claude-3.7-Sonnet | 42.3% | 35.1% |
| DeepSeek-V3.2-Exp | 50.0% | 41.2% |
| GPT-4o | 38.7% | 33.5% |

---

## 3. Key Insight

LLMs excel at proof sketch generation and tactic recommendation, but still struggle with:

- Inductive invariant discovery
- Complex algebraic manipulations
- Proof by contradiction

---

## 4. References
