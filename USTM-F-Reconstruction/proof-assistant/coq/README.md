# USTM-F Coq Formalization

This directory contains the Coq formalization of the Unified Streaming Theory Meta-Framework (USTM-F).

## Project Structure

```
theories/
├── Foundation/
│   └── Types.v              # Base types, utilities, and relations
├── Models/
│   ├── Actor.v              # Actor model formalization
│   └── CSP.v                # CSP (Communicating Sequential Processes)
├── USTM/
│   └── Core.v               # USTM-F core definitions and semantics
├── Encodings/
│   └── Encoding.v           # Model encodings into USTM-F
└── Proofs/
    └── Determinism.v        # Determinism theorems and proofs
```

## Prerequisites

- Coq 8.15 or higher
- Coq standard library (Arith, Lists, Strings, etc.)

## Compilation

### Method 1: Using coq_makefile

```bash
# Generate the Makefile
coq_makefile -f _CoqProject -o Makefile.coq

# Compile all files
make -f Makefile.coq all

# Clean up
make -f Makefile.coq clean
```

### Method 2: Using the provided Makefile

```bash
# Compile all files
make

# Show statistics
make stats

# Clean up
make clean
```

### Method 3: Individual file compilation

```bash
coqc -Q theories/Foundation Foundation theories/Foundation/Types.v
coqc -Q theories/Foundation Foundation -Q theories/Models Models theories/Models/Actor.v
coqc -Q theories/Foundation Foundation -Q theories/Models Models theories/Models/CSP.v
coqc -Q theories/Foundation Foundation -Q theories/Models Models -Q theories/USTM USTM theories/USTM/Core.v
coqc -Q theories/Foundation Foundation -Q theories/Models Models -Q theories/USTM USTM -Q theories/Encodings Encodings theories/Encodings/Encoding.v
coqc -Q theories/Foundation Foundation -Q theories/Models Models -Q theories/USTM USTM -Q theories/Encodings Encodings -Q theories/Proofs Proofs theories/Proofs/Determinism.v
```

## Theorem Inventory

### Core Theorems (Completed)

| Theorem | File | Description |
|---------|------|-------------|
| `message_eq_refl` | Types.v | Message equality is reflexive |
| `rt_clos_trans` | Types.v | Reflexive-transitive closure is transitive |
| `trans_clos_implies_rt_clos` | Types.v | Transitive closure implies RT closure |
| `actor_step_preserves_wf` | Actor.v | Actor transitions preserve well-formedness |
| `ext_choice_comm` | CSP.v | External choice is commutative |
| `ext_choice_unit` | CSP.v | STOP is unit for external choice |
| `parallel_comm` | CSP.v | Parallel composition is commutative |
| `deterministic_unique` | CSP.v | Deterministic CSP has unique transitions |
| `skip_deadlock_free` | CSP.v | SKIP is deadlock-free |
| `prefix_deadlock_free` | CSP.v | Prefix preserves deadlock-freedom |
| `ustm_time_progress` | Core.v | Time always progresses in USTM |
| `deterministic_reduction` | Determinism.v | Deterministic USTM configurations |
| `compose_preserves_determinism` | Determinism.v | Composition preserves determinism |
| `ustm_main_determinism_theorem` | Determinism.v | Main determinism theorem |
| `confluence_implies_determinism` | Determinism.v | Confluence implies determinism |

### Theorems with Structured Proofs (Admitted)

The following theorems have proof structures but use `Admitted` for complex sub-goals that require:
- Detailed case analysis
- Auxiliary lemmas not yet formalized
- Advanced Coq tactics (induction, coinduction)

| Theorem | File | Status |
|---------|------|--------|
| `actor_confluence` | Actor.v | Structured, partial |
| `isolated_reduction_commute` | Actor.v | Structured, partial |
| `fair_trace_progress` | Actor.v | Structured, partial |
| `initials_sound` | CSP.v | Structured, partial |
| `ustm_local_confluence` | Core.v | Structured, partial |
| `ustm_compose_wf` | Core.v | Structured, partial |
| `stream_order_preserved` | Core.v | Structured, partial |
| `ustm_bisim_equivalence` | Core.v | Structured, partial |
| `actor_to_ustm_preservation` | Encoding.v | Structured, partial |
| `csp_to_ustm_preservation` | Encoding.v | Structured, partial |

## Statistics

- **Total Lines**: ~1,867
- **Definitions**: 86
- **Theorems/Lemmas**: 45
- **Completed Proofs**: 21 (46.7%)
- **Structured Proofs (Admitted)**: 24 (53.3%)

## Key Concepts

### Actor Model
- **Configuration**: `ActorConfig` with actors, behaviors, mailboxes
- **Transitions**: `ActorStep` captures send, receive, spawn, become
- **Properties**: Well-formedness preservation, determinism conditions

### CSP
- **Syntax**: Processes with prefix, choice, parallel, hide, rename
- **Semantics**: Structured operational semantics (SOS)
- **Properties**: Trace refinement, algebraic laws, deadlock-freedom

### USTM-F Core
- **Configuration**: Processing elements with stream connectivity
- **Semantics**: Step relation with process, fail, recover actions
- **Properties**: Time progress, compositionality, invariants

### Encodings
- **Actor → USTM**: Behavior as PE semantics, mailbox as stream
- **CSP → USTM**: Process as state space, events as actions
- **Correctness**: Semantic preservation, simulation relations

### Determinism
- **USTM Determinism**: Independent PEs yield deterministic execution
- **Encoding Preservation**: Determinism preserved under encoding
- **Normal Forms**: Unique normal forms for terminating systems

## Verification

Run the Python verification script to check proof structure:

```bash
python verify_proofs.py
```

This script performs:
- Syntactic validation of Coq files
- Proof structure analysis
- Statistics generation
- Requirements verification

## Notes

- Some proofs use `Admitted` for sub-goals requiring auxiliary lemmas
- The formalization follows the USTM-F specification document
- All core definitions are complete; proofs are being progressively completed
- The structure supports incremental extension with additional models (Dataflow, Petri nets)

## References

- USTM-F Specification Document
- "Unified Streaming Theory Meta-Framework" - AnalysisDataFlow Project
- Coq Reference Manual (https://coq.inria.fr/refman/)
