# Actor-to-CSP Encoding

> **Stage**: Struct/03-relationships | **Prerequisites**: [Actor Model](actor-model-formalization.md), [CSP](csp-formalization.md) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

Formal encoding from Actor model to CSP and analysis of expressiveness boundaries.

---

## 1. Definitions

### Actor System Configuration

$$\text{ActorConfig} = (A, M, a_0, \text{beh}, \text{mailbox})$$

- $A$: Set of actor addresses
- $M$: Set of messages
- $a_0$: Initial actor
- $\text{beh}: A \to (M \to A \times M^*)$: Behavior function
- $\text{mailbox}: A \to M^*$: Message queue

### Encoding Function

$$\llbracket a \rrbracket_{CSP} = \text{Mailbox}_a \parallel \text{Behavior}_a$$

Where:

- $\text{Mailbox}_a = \mu X.\text{receive}(m).X \mid \text{deliver}(m).X$
- $\text{Behavior}_a = \text{process}(m).(\text{send}(m_1, a_1) \mid \ldots \mid \text{send}(m_k, a_k))$

---

## 2. Key Results

### Thm-S-05-01 (Trace Semantics Preservation)

Static actor systems without dynamic address passing can be encoded into CSP preserving trace semantics.

### Limitations

| Feature | Encodable? | Reason |
|---------|-----------|--------|
| Static actors | Yes | Direct mapping to CSP processes |
| Dynamic creation | Partial | Requires recursive process definitions |
| Address passing | No | CSP channels are static |
| Distributed transparency | No | Location explicit in CSP |

---

## 3. References
