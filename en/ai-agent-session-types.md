# AI Agent and Session Types

> **Stage**: Struct/06-frontier | **Prerequisites**: [Choreographic Deadlock Freedom](choreographic-deadlock-freedom.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

Multi-Agent Session Types (MAST) for type-safe communication in LLM-based multi-agent systems.

---

## 1. Definitions

### Def-S-29-01 (AI Agent Formal Model)

$$Agent = (State, LLM, Tools, Protocol, Memory)$$

### Def-S-29-02 (Multi-Agent Session Types)

$$MAST ::= p \to q: T; MAST \mid \text{choice}\{MAST_i\} \mid \mu X.MAST \mid X \mid \text{end}$$

### Def-S-29-04 (Type-Safe Agent Communication)

$$\Gamma \vdash Agents : MAST \Rightarrow \text{communication respects protocol}$$

---

## 2. Key Challenge

**LLM Non-Determinism**: LLM responses are probabilistic, not deterministic.

**Solution**: Wrap LLM in typed adapter with output validation.

---

## 3. Key Properties

### Prop-S-29-01 (Agent System Deadlock Freedom)

Well-typed MAST agents are deadlock-free.

---

## 4. References
