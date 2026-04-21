# FG/FGG Type Safety Proof

> **Stage**: Struct/04-proofs | **Prerequisites**: [Type Safety Derivation](type-safety-derivation.md) | **Formalization Level**: L5
> **Translation Date**: 2026-04-21

## Abstract

Type safety for Featherweight Go (FG) and Featherweight Generic Go (FGG): progress + preservation.

---

## 1. Syntax

### FG

$$e ::= x \mid e.f \mid e.m(\bar{e}) \mid \text{struct}\{ \bar{v} \}$$

$$d ::= \text{type}\ S\ \text{struct}\{ \bar{f}\ T \} \mid \text{func}\ (x\ T)\ m(\bar{x}\ \bar{T})\ T\ \{ e \}$$

### FGG

Adds type parameters: $T ::= S\langle\bar{T}\rangle$

---

## 2. Type Safety

### Progress

$$\Gamma \vdash e: T \Rightarrow e \text{ is a value or } \exists e': e \to e'$$

### Preservation

$$\Gamma \vdash e: T \land e \to e' \Rightarrow \Gamma \vdash e': T$$

---

## 3. Key Theorem

### Type Safety

Well-typed FG/FGG programs never get stuck.

### FGG Monomorphization Correctness

Monomorphized FGG is type-equivalent to original FGG.

---

## 4. References
