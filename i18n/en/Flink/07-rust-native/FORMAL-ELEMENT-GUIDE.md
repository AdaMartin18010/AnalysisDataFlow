---
title: "Formal Element ID Specification v2.0"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Formal Element ID Specification v2.0

> **Effective Date**: 2026-04-04
> **Scope**: All documents under Flink/14-rust-assembly-ecosystem/

---

## 1. ID Format Specification

### 1.1 Basic Format

```
{Type}-{Module}-{Number}
```

| Component | Description | Example |
|-----------|-------------|---------|
| **Type** | Element type | Def, Prop, Lemma, Thm, Cor |
| **Module** | Module code | WASM, SIMD, FLASH, RW, WASI, VEC, HET, EDGE, AI |
| **Number** | Two-digit sequence | 01-99 |

### 1.2 Element Type Definitions

| Type Code | Full Name | Purpose |
|-----------|-----------|---------|
| **Def** | Definition | Concept definition |
| **Prop** | Proposition | Property proposition |
| **Lemma** | Lemma | Auxiliary lemma |
| **Thm** | Theorem | Major theorem |
| **Cor** | Corollary | Theorem corollary |

### 1.3 Module Code Definitions

| Code | Module Name | Directory |
|------|-------------|-----------|
| **WASM** | WebAssembly 3.0 | wasm-3.0/ |
| **SIMD** | SIMD/Assembly Optimization | simd-optimization/ |
| **FLASH** | Flash Engine Analysis | flash-engine/ |
| **RW** | RisingWave Comparison | risingwave-comparison/ |
| **WASI** | WASI 0.3 Async Model | wasi-0.3-async/ |
| **VEC** | Vectorized UDF | vectorized-udfs/ |
| **HET** | Heterogeneous Computing | heterogeneous-computing/ |
| **EDGE** | Edge Computing | edge-wasm-runtime/ |
| **AI** | AI-Native Streaming | ai-native-streaming/ |

---

## 2. Number Allocation Rules

### 2.1 Continuity Principle

- IDs must be continuous, starting from 01
- No skipping allowed
- No reuse allowed

### 2.2 In-File Allocation

```
IDs within a file should be allocated continuously without gaps.

Example (wasm-3.0/01-wasm-3.0-spec-guide.md):
- Def-WASM-01
- Def-WASM-02
- Def-WASM-03
- Def-WASM-04
- Def-WASM-05

Next file (02-memory64-deep-dive.md):
- Def-WASM-06
- Def-WASM-07
- Def-WASM-08
- Def-WASM-09
```

### 2.3 Independent Numbering by Type

```
Definitions, propositions, and theorems are numbered independently:

Definitions:
- Def-WASM-01
- Def-WASM-02
...

Propositions (independent numbering):
- Prop-WASM-01
- Prop-WASM-02
...

Theorems (independent numbering):
- Thm-WASM-01
- Thm-WASM-02
...
```

---

## 3. Naming Format Specification

### 3.1 Title Format

```markdown
### Def-{Module}-{Number}: {Chinese Name} ({English Name})

Examples:
### Def-WASM-01: WebAssembly 模块 (WebAssembly Module)
### Prop-SIMD-02: 向量化效率 (Vectorization Efficiency)
### Thm-FLASH-01: 性能提升边界 (Performance Improvement Bound)
```

### 3.2 Reference Format

```markdown
In-document reference: [Def-WASM-01](#def-wasm-01-webassembly-模块-webassembly-module)
Cross-document reference: [Def-WASM-01](wasm-3.0/01-wasm-3.0-spec-guide.md#def-wasm-01-webassembly-30-规范里程碑)
```

---

## 4. Module ID Ranges

### 4.1 Allocated Ranges (As of 2026-04-04)

| Module | Definition Range | Proposition Range | Theorem Range |
|--------|------------------|-------------------|---------------|
| **WASM** | Def-WASM-01 ~ Def-WASM-17 | Prop-WASM-01 ~ Prop-WASM-15 | Thm-WASM-01 ~ Thm-WASM-04 |
| **SIMD** | Def-SIMD-01 ~ Def-SIMD-15 | Prop-SIMD-01 ~ Prop-SIMD-10 | - |
| **FLASH** | Def-FLASH-01 ~ Def-FLASH-20 | Prop-FLASH-01 ~ Prop-FLASH-15 | - |
| **RW** | Def-RW-01 ~ Def-RW-16 | Prop-RW-01 ~ Prop-RW-13 | - |
| **WASI** | Def-WASI-01 ~ Def-WASI-16 | Prop-WASI-01 ~ Prop-WASI-12 | - |
| **VEC** | Def-VEC-01 ~ Def-VEC-17 | Prop-VEC-01 ~ Prop-VEC-12 | Thm-VEC-01 ~ Thm-VEC-07 |
| **HET** | Def-HET-01 ~ Def-HET-16 | Prop-HET-01 ~ Prop-HET-12 | - |
| **EDGE** | Def-EDGE-01 ~ Def-EDGE-20 | Prop-EDGE-01 ~ Prop-EDGE-16 | - |
| **AI** | Def-AI-01 ~ Def-AI-16 | Prop-AI-01 ~ Prop-AI-09 | - |

### 4.2 Reserved Ranges

| Module | Reserved Definition Range | Reserved Proposition Range |
|--------|---------------------------|----------------------------|
| **WASM** | Def-WASM-18 ~ Def-WASM-30 | Prop-WASM-16 ~ Prop-WASM-25 |
| **SIMD** | Def-SIMD-16 ~ Def-SIMD-30 | Prop-SIMD-11 ~ Prop-SIMD-20 |
| **FLASH** | Def-FLASH-21 ~ Def-FLASH-35 | Prop-FLASH-16 ~ Prop-FLASH-25 |
| **RW** | Def-RW-17 ~ Def-RW-30 | Prop-RW-14 ~ Prop-RW-25 |
| **WASI** | Def-WASI-17 ~ Def-WASI-30 | Prop-WASI-13 ~ Prop-WASI-25 |
| **VEC** | Def-VEC-18 ~ Def-VEC-30 | Prop-VEC-13 ~ Prop-VEC-25 |
| **HET** | Def-HET-17 ~ Def-HET-30 | Prop-HET-13 ~ Prop-HET-25 |
| **EDGE** | Def-EDGE-21 ~ Def-EDGE-35 | Prop-EDGE-17 ~ Prop-EDGE-30 |
| **AI** | Def-AI-17 ~ Def-AI-30 | Prop-AI-10 ~ Prop-AI-25 |

---

## 5. Document Structure Specification

### 5.1 Six-Section Template

Every document must contain the following sections:

```markdown
## 1. Concept Definitions (Definitions)
At least 3 Def-{Module}-* definitions

## 2. Property Derivation (Properties)
At least 2 Prop-{Module}-* propositions

## 3. Relations (Relations)
Relationships with other concepts/systems

## 4. Argumentation (Argumentation)
Technical analysis and boundary discussion

## 5. Formal Proof / Engineering Argument (Proof / Engineering Argument)
Theorem proofs or engineering selection arguments

## 6. Examples (Examples)
Runnable code examples

## 7. Visualizations (Visualizations)
At least 1 Mermaid diagram

## 8. References (References)
Authoritative source references
```

### 5.2 Formal Element Density

| Element Type | Minimum | Recommended |
|--------------|---------|-------------|
| Definition (Def) | 3 | 4-5 |
| Proposition (Prop) | 2 | 3-4 |
| Theorem (Thm) | 0 | 1-2 |
| Lemma (Lemma) | 0 | 0-1 |

---

## 6. Quality Checklist

### 6.1 New Document Checks

- [ ] ID conforms to {Type}-{Module}-{Number} format
- [ ] IDs are continuous with no skips
- [ ] Module code is correct
- [ ] Type code is correct
- [ ] Title format is correct
- [ ] Reference format is correct

### 6.2 Modified Document Checks

- [ ] Modified IDs still conform to the specification
- [ ] All references are updated accordingly
- [ ] No duplicate IDs
- [ ] No skipped IDs

---

## 7. Violation Handling

### 7.1 Common Violations

| Violation Type | Example | Fix |
|----------------|---------|-----|
| **Double numbering** | Def-EDGE-01-01 | Change to Def-EDGE-01 |
| **Excessive hierarchy** | Def-WASM-3.0-01 | Change to Def-WASM-01 |
| **Prefix confusion** | Def-AVX-01 (in SIMD module) | Change to Def-SIMD-04 |
| **Type error** | Theorem-WASM-01 | Change to Thm-WASM-01 |

### 7.2 Fix Process

1. Discover the violation
2. Look up the mapping in THEOREM-INDEX.md
3. Use StrReplaceFile for batch replacement
4. Verify all references are updated
5. Update THEOREM-INDEX.md

---

## 8. Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-04-04 | Initial specification, based on AGENTS.md |
| v2.0 | 2026-04-04 | Fixed numbering chaos, unified specification |

---

## 9. References

- [PROJECT-AUDIT-REPORT.md](./PROJECT-AUDIT-REPORT.md) - ID issue audit report
- [THEOREM-INDEX.md](./THEOREM-INDEX.md) - Global formal element index
