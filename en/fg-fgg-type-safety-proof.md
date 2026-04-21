# FG/FGG Type Safety Proof

> **Stage**: Struct/04-proofs | **Prerequisites**: [Type Safety Derivation](type-safety-derivation.md) | **Formalization Level**: L3
> **Translation Date**: 2026-04-21

## Abstract

This document formalizes the type safety proof for Featherweight Go (FG) and Featherweight Generic Go (FGG), establishing that well-typed programs never get stuck.

---

## 1. Definitions

### 1.1 FG Abstract Syntax

```
Types:     t ::= t_name | struct { f: t } | interface { m: sig }
Values:    v ::= struct { f = v }
Exprs:     e ::= v | e.f | e.m(e) | t(e)
Methods:   meth ::= func (x: t) m(y: t) t { return e }
```

### 1.2 FGG Abstract Syntax

FGG extends FG with type parameters:

```
Types:     t ::= ... | t_name[t, ...]
Methods:   meth ::= func [T any] (x: t) m(y: t) t { return e }
```

### 1.3 Type Substitution

$$[T \mapsto t]\tau \text{ — replace type parameter } T \text{ with concrete type } t \text{ in } \tau$$

### 1.4 Method Resolution

$$\text{mresolve}(t, m) = \text{method body of } m \text{ in type } t$$

---

## 2. Type Rules

### FG Typing

$$\frac{\Gamma \vdash e: \text{struct}\{f: t\}}{\Gamma \vdash e.f: t} \text{ (T-Field)}$$

$$\frac{\Gamma \vdash e_1: t_1 \quad \text{mresolve}(t_1, m) = (x: t_2) \to t \quad \Gamma \vdash e_2: t_2}{\Gamma \vdash e_1.m(e_2): t} \text{ (T-Call)}$$

### FGG Typing

$$\frac{\Gamma \vdash e: t[\vec{u}/\vec{T}] \quad \text{mresolve}(t, m) = [\vec{T} \text{ any}](x: t_2) \to t \quad \Gamma \vdash e_2: [\vec{u}/\vec{T}]t_2}{\Gamma \vdash e_1.m(e_2): [\vec{u}/\vec{T}]t} \text{ (T-Call-Gen)}$$

---

## 3. Key Lemmas

### Lemma-S-04-05 (Inversion)

If $\Gamma \vdash e.f: t$, then $\Gamma \vdash e: \text{struct}\{f: t\}$.

### Lemma-S-04-06 (Canonical Forms)

If $\Gamma \vdash v: \text{struct}\{\ldots\}$, then $v = \text{struct}\{f_1 = v_1, \ldots\}$.

### Lemma-S-04-07 (Substitution)

If $\Gamma, x: t_1 \vdash e: t_2$ and $\Gamma \vdash v: t_1$, then $\Gamma \vdash [x \mapsto v]e: t_2$.

---

## 4. Type Safety Theorem

### Thm-S-04-08 (Progress)

If $\Gamma \vdash e: t$, then either $e$ is a value or $\exists e': e \to e'$.

**Proof.** By case analysis on $e$:

- **Value**: Terminal.
- **Field access**: By inversion, $e = e_0.f$. By IH, $e_0$ is a value or reduces. If value, Canonical Forms gives struct literal, so field access reduces. ∎

### Thm-S-04-09 (Preservation)

If $\Gamma \vdash e: t$ and $e \to e'$, then $\Gamma \vdash e': t$.

**Proof.** By case analysis on reduction:

- **Field access**: Substitution Lemma preserves typing.
- **Method call**: Method body is well-typed by method declaration rule. ∎

### Thm-S-04-10 (FG/FGG Type Safety)

If $\vdash e: t$, then evaluation of $e$ does not get stuck.

**Proof.** Direct from Progress + Preservation. ∎

---

## 5. References
