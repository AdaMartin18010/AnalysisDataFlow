# Formal Methods Documentation System

> **Systematic formal modeling theory and verification methods for distributed systems**
>
> **Version**: v4.0 | **Last Updated**: 2026-04-10 | **Status**: 🚧 English Translation In Progress

---

## 📋 Introduction

This is the **English translation** of the Formal Methods Documentation System, a comprehensive knowledge base covering:

- **251+ documents** spanning mathematical foundations to cutting-edge research
- **550+ formal definitions** with rigorous mathematical specifications
- **380+ theorems/lemmas** with verified formal propositions
- **450+ visual diagrams** using Mermaid for intuitive understanding
- **Bilingual support**: Chinese (Primary) 🇨🇳 + English (In Progress) 🇬🇧

The documentation systematically organizes formal modeling theory and verification methods for distributed systems (including workflows, stream computing, and cloud-native containers), covering the complete technology stack from mathematical foundations, computational models, verification techniques to industrial practices.

---

## 📁 Document Navigation

### Struct/ Unit — Mathematical Foundations (11 Documents)

The **Struct/** unit covers core mathematical foundations and formal theories:

| # | Document | Status | Description |
|---|----------|--------|-------------|
| 01 | [Introduction](01-introduction.md) | ✅ Translated | Overview of formal methods landscape |
| 02 | [Lambda Calculus](02-lambda-calculus.md) | ✅ Translated | Foundation of functional computation |
| 03 | [Type Systems](03-type-systems.md) | ✅ Translated | Static verification foundations |
| 04 | [Hoare Logic](04-hoare-logic.md) | ✅ Translated | Axiomatic program verification |
| 05 | [Separation Logic](05-separation-logic.md) | ✅ Translated | Modular reasoning about heap |
| 06 | [Concurrency Theory](06-concurrency-theory.md) | ✅ Translated | CCS, CSP, π-calculus, Actor model |
| 07 | [Abstract Interpretation](07-abstract-interpretation.md) | ⏳ Pending | Static analysis framework |
| 08 | [Temporal Logic](08-temporal-logic.md) | ⏳ Pending | LTL, CTL, μ-calculus |
| 09 | [Bisimulation](09-bisimulation.md) | ⏳ Pending | Behavioral equivalence |
| 09 | [Petri Nets](09-petri-nets.md) | ⏳ Pending | Net-based concurrent modeling |
| 10 | [Distributed Computing](10-distributed-computing.md) | ⏳ Pending | Consensus, fault tolerance, consistency |
| 11 | [Formal Methods Overview](01-wikipedia-formal-methods.md) | ⏳ Pending | Wikipedia-style comprehensive overview |

### Knowledge/ Unit — Applied Knowledge (In Progress)

The **Knowledge/** unit bridges theory and practice:

| Category | Topics | Status |
|----------|--------|--------|
| Design Patterns | Workflow patterns, Stream processing patterns | ⏳ In Progress |
| System Architecture | Cloud-native, Microservices, Serverless | ⏳ In Progress |
| Business Modeling | Domain-driven design, Event sourcing | ⏳ In Progress |
| Best Practices | Industrial verification case studies | ⏳ In Progress |

### Flink/ Unit — Stream Processing (In Progress)

The **Flink/** unit provides in-depth coverage of Apache Flink:

| Category | Topics | Status |
|----------|--------|--------|
| Core Architecture | Checkpointing, Watermarks, State backends | ⏳ In Progress |
| Exactly-Once Semantics | End-to-end consistency guarantees | ⏳ In Progress |
| Backpressure & Scheduling | Flow control mechanisms | ⏳ In Progress |
| Table API & SQL | Declarative stream processing | ⏳ In Progress |
| AI/ML Integration | Flink ML, Real-time inference | ⏳ In Progress |

---

## 🚀 Quick Links

### Core Theoretical Topics

| Topic | Description | Chinese Equivalent |
|-------|-------------|-------------------|
| [Lambda Calculus](02-lambda-calculus.md) | Universal model of computation; foundation of functional programming | λ演算 |
| [Type Systems](03-type-systems.md) | Static verification through type discipline; from simply-typed λ to dependent types | 类型系统 |
| [Hoare Logic](04-hoare-logic.md) | Axiomatic semantics for imperative programs; Floyd-Hoare verification | Hoare逻辑 |
| [Separation Logic](05-separation-logic.md) | Modular reasoning about mutable state; frame rule and local reasoning | 分离逻辑 |
| [Concurrency Theory](06-concurrency-theory.md) | Process calculi (CCS, CSP, π-calculus), Actor model, session types | 并发理论 |

### Advanced Topics

| Topic | Description | Status |
|-------|-------------|--------|
| Probabilistic Programming | Formal semantics for randomized algorithms | ⏳ Planned |
| Homotopy Type Theory | Univalent foundations, higher inductive types | ⏳ Planned |
| Game Semantics | Interactive semantics of programming languages | ⏳ Planned |
| Certified Compilation | Compiler verification (CompCert approach) | ⏳ Planned |
| Distributed Consensus | Paxos, Raft, Byzantine fault tolerance | ⏳ Planned |

---

## 💻 Formal Code Repository

Our documentation is complemented by executable formalizations:

### Lean 4 Formalization

```lean4
-- Example: Simply-typed lambda calculus in Lean 4
inductive Ty : Type
  | base : Ty
  | arrow : Ty → Ty → Ty

inductive Tm : Type
  | var : Nat → Tm
  | abs : Ty → Tm → Tm
  | app : Tm → Tm → Tm

-- Type safety theorem (progress & preservation)
theorem type_safety (t : Tm) (T : Ty) :
  has_type t T → (value t ∨ ∃ t', steps t t') := by
  -- Proof implementation
```

**Location**: `formal-methods/formal-code/lean4/`

### TLA+ Specifications

```tla
(* Example: Two-Phase Commit in TLA+ *)
MODULE TwoPhaseCommit

VARIABLES rmState, tmState, tmPrepared, msgs

Init ==
  ∧ rmState = [r ∈ RM ↦ "working"]
  ∧ tmState = "init"
  ∧ tmPrepared = {}
  ∧ msgs = {}

Phase1a(r) ==
  ∧ rmState[r] = "working"
  ∧ rmState' = [rmState EXCEPT ![r] = "prepared"]
  ∧ msgs' = msgs ∪ {[type ↦ "Prepared", rm ↦ r]}
  ∧ UNCHANGED ⟨tmState, tmPrepared⟩

(* Safety property: Consistency *)
Consistency ==
  ∀ r1, r2 ∈ RM :
    (rmState[r1] = "committed") ∧ (rmState[r2] = "aborted") ⇒ FALSE
```

**Location**: `formal-methods/formal-code/tla+/`

### Isabelle/HOL Proofs

```isabelle
(* Example: Separation Logic in Isabelle *)
theorem frame_rule:
  assumes "⊢ {P} c {Q}"
  shows "⊢ {P ** R} c {Q ** R}"
  using assms
  by (rule frame_rule_aux)
```

**Location**: `formal-methods/formal-code/isabelle/`

---

## 🤝 How to Contribute

### Translation Guide

We welcome contributions to expand English coverage:

1. **Pick an untranslated document** from the status tables above
2. **Follow the document template**:
   - Six-section structure: Definitions → Properties → Relations → Argumentation → Proofs → Examples
   - Include at least one Mermaid diagram per document
   - Use formal numbering: `Def-*`, `Thm-*`, `Lemma-*`, `Prop-*`, `Cor-*`
3. **Maintain terminology consistency** using our glossary
4. **Submit a pull request** with clear description

### Translation Workflow

```
1. Fork repository
      ↓
2. Create branch: translate/struct-07-abstract-interpretation
      ↓
3. Translate document following style guide
      ↓
4. Update this README with ✅ status
      ↓
5. Submit PR for review
```

### Terminology Reference

| English | Chinese | Notes |
|---------|---------|-------|
| Formal Methods | 形式化方法 | Rigorous mathematical approaches to software/hardware verification |
| Process Calculus | 进程演算 | CCS, CSP, π-calculus family |
| Model Checking | 模型检测 | Automated state-space exploration |
| Theorem Proving | 定理证明 | Interactive/automated proof assistants |
| Bisimulation | 互模拟 | Behavioral equivalence relation |
| Abstract Interpretation | 抽象解释 | Static analysis framework |
| Separation Logic | 分离逻辑 | Heap reasoning with separating conjunction |
| Temporal Logic | 时序逻辑 | LTL, CTL for specifying system behavior |
| Session Types | 会话类型 | Types for structured communication |
| Refinement | 精化 | Stepwise development from abstract to concrete |

---

## 📊 Translation Progress

### Overall Status

```
Struct/:   [██████░░░░░░░░░░░░░░] 55% (6/11 translated)
Knowledge/: [░░░░░░░░░░░░░░░░░░░░] 0% (In planning)
Flink/:    [░░░░░░░░░░░░░░░░░░░░] 0% (In planning)
Total:     [██░░░░░░░░░░░░░░░░░░] ~20% (6/30+ documents)
```

### Completed Documents (✅)

- ✅ 01-introduction.md
- ✅ 02-lambda-calculus.md
- ✅ 03-type-systems.md
- ✅ 04-hoare-logic.md
- ✅ 05-separation-logic.md
- ✅ 06-concurrency-theory.md

### Pending Translation (⏳)

- ⏳ 07-abstract-interpretation.md
- ⏳ 08-temporal-logic.md
- ⏳ 09-bisimulation.md
- ⏳ 09-petri-nets.md
- ⏳ 10-distributed-computing.md
- ⏳ 01-wikipedia-formal-methods.md

---

## 📚 Learning Paths

### Path 1: Foundations First

For readers with strong mathematical background:

```
01-introduction → 02-lambda-calculus → 03-type-systems → 04-hoare-logic → 05-separation-logic
```

### Path 2: Concurrency Focus

For distributed systems engineers:

```
01-introduction → 06-concurrency-theory → 10-distributed-computing → (planned: consensus-algorithms)
```

### Path 3: Verification Practitioner

For engineers applying formal methods:

```
01-introduction → 03-type-systems → 04-hoare-logic → 05-separation-logic → (planned: model-checking-tools)
```

---

## 🔗 Related Resources

### Official Documentation

| Resource | Link | Description |
|----------|------|-------------|
| TLA+ | <https://lamport.azurewebsites.net/tla/tla.html> | Leslie Lamport's temporal logic |
| Lean | <https://lean-lang.org/> | Modern theorem prover |
| Coq | <https://coq.inria.fr/> | Interactive proof assistant |
| Isabelle | <https://isabelle.in.tum.de/> | Higher-order logic prover |

### Academic References

- T. Nipkow, G. Klein. *Concrete Semantics with Isabelle/HOL*. Springer, 2014.
- B. C. Pierce et al. *Software Foundations*. Electronic textbook.
- C. A. R. Hoare. "An Axiomatic Basis for Computer Programming". CACM, 1969.
- R. Milner. *Communication and Concurrency*. Prentice Hall, 1989.
- J. C. Reynolds. "Separation Logic: A Logic for Shared Mutable Data Structures". LICS, 2002.

---

## 📄 License

This documentation is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/):

- **Attribution**: You must give appropriate credit
- **ShareAlike**: If you remix, transform, or build upon the material, you must distribute your contributions under the same license

---

## 🌐 Language Versions

- [中文 (Chinese)](README.md)
- [English](README.md) (This document)

---

> **Last Updated**: 2026-04-10 | **Status**: 🚧 English Translation In Progress | **Version**: v4.0
>
> **Maintainers**: Formal Methods Documentation Team
