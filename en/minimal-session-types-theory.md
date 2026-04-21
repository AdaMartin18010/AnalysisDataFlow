# Minimal Session Types Theory

> **Stage**: Struct/01-foundation | **Prerequisites**: [Session Types](session-types.md), [Process Calculus](process-calculus-primer.md) | **Formalization Level**: L5-L6
> **Translation Date**: 2026-04-21

## Abstract

Minimal Session Types (MST): standard session types compile to a system with only output (!), input (?), and end — no explicit sequential composition needed.

---

## 1. Definitions

### Def-S-11-01 (MST Syntax)

$$S ::= \ !T.S \ \mid \ ?T.S \ \mid \ \text{end}$$

### Def-S-11-05 (MST Duality)

$$\overline{!T.S} = ?T.\overline{S}, \quad \overline{?T.S} = !T.\overline{S}, \quad \overline{\text{end}} = \text{end}$$

### Def-S-11-09 (Compilation Mapping)

$$\llbracket S_1 ; S_2 \rrbracket = \text{synchronized delegation via fresh channel}$$

Sequential composition encoded without explicit operator.

---

## 2. Key Result

### Thm-S-11-01 (MST Expressiveness Equivalence)

Standard session types and MST are observationally equivalent under the compilation mapping.

**Implication**: Type checkers need only handle 3 constructors, reducing implementation complexity.

---

## 3. Relations

| Theory | Relation to MST |
|--------|-----------------|
| Standard Session Types | Compilable to MST |
| π-calculus | MST embeds into π |
| Linear Logic | Curry-Howard correspondence preserved |
| Choreographic Programming | Endpoint projection compatible |

---

## 4. References
