# Formal Methods for Distributed Systems: Complete Technical Architecture

> **Document Positioning**: This documentation systematically organizes formal modeling theory and verification methods for distributed systems (including workflows, stream computing, and cloud-native containers), covering the complete technology stack from mathematical foundations, computational models, verification techniques to industrial practices.
>
> **Version**: v4.0 | **Created**: 2026-04-09 | **Last Updated**: 2026-04-10 | **Status**: ✅ Phase A/B/C Complete | 🚧 Phase D In Progress

---

## 🎯 Project Status Overview

| Phase | Goal | Status | Key Deliverables |
|-------|------|--------|------------------|
| **Phase A** | Foundational Theory Framework | ✅ Complete | 8 core units established |
| **Phase B** | Wikipedia 25 Core Concepts Full Coverage | ✅ 100% Complete | 25 in-depth concept analyses |
| **Phase C** | Industrial Case Deepening | ✅ Complete | 15+ industrial-grade verification cases |
| **Phase D** | Knowledge Graph & Learning Paths | 🚧 In Progress | Dynamic learning recommendation system |

---

## 📊 Content Statistics

| Metric | Count | Description |
|--------|-------|-------------|
| **Total Documents** | 95+ | Covering complete chain from theory to practice |
| **Formal Definitions** | 550+ | Strict mathematical definitions and specifications |
| **Theorems/Lemmas** | 380+ | Verified formal propositions |
| **Formal Proofs** | 180+ | Complete proofs or proof outlines |
| **Mermaid Diagrams** | 450+ | Visual structure and relationship diagrams |
| **References** | 550+ | Academic papers, books, technical documentation |

---

## 📁 Documentation Architecture

```
formal-methods/
├── 📖 README.md                          # This file - Overview and navigation
├── 📖 README-EN.md                       # English version of this document
│
├── 01-foundations/                       # Unit 1: Mathematical Foundations
│   ├── 01-order-theory.md               # Order Theory - CPO, Lattice Theory
│   ├── 02-category-theory.md            # Category Theory - Coalgebra, Bisimulation
│   ├── 03-logic-foundations.md          # Logic Foundations - LTL/CTL/Hoare
│   ├── 04-domain-theory.md              # Domain Theory - Denotational Semantics
│   ├── 05-type-theory.md                # Type Theory - Static Verification
│   └── 06-coalgebra-advanced.md         # Advanced Coalgebra - Infinite Behavior
│
├── 02-calculi/                          # Unit 2: Process Calculi
│   ├── 01-w-calculus-family/
│   │   ├── 01-omega-calculus.md         # ω-calculus: MANET Networks
│   │   ├── 02-W-calculus.md             # W-calculus: Digital Signal Processing
│   │   └── 03-w-calculus-linguistic.md  # w-calculus: Computational Linguistics
│   ├── 02-pi-calculus/
│   │   ├── 01-pi-calculus-basics.md     # π-calculus Fundamentals
│   │   ├── 02-pi-calculus-workflow.md   # π-calculus in Workflow Applications
│   │   ├── 03-pi-calculus-patterns.md   # Common Patterns and Idioms
│   │   └── 04-pi-calculus-encodings.md  # Encoding Other Computational Models
│   └── 03-stream-calculus/
│       ├── 01-stream-calculus.md        # Stream Calculus (Rutten)
│       ├── 02-network-algebra.md        # Network Algebra (Bergstra)
│       ├── 03-kahn-process-networks.md  # Kahn Process Networks
│       ├── 04-dataflow-process-networks.md # Dataflow Process Networks
│       ├── 05-stream-equations.md       # Stream Equation Systems
│       └── 06-combinatorial-streams.md  # Combinatorial Stream Theory
│
├── 03-model-taxonomy/                   # Unit 3: Five-Dimensional Classification
│   ├── 01-system-models/
│   │   ├── 01-sync-async.md             # Synchronous/Asynchronous Models
│   │   ├── 02-failure-models.md         # Failure Models
│   │   └── 03-communication-models.md   # Communication Models
│   ├── 02-computation-models/
│   │   ├── 01-process-algebras.md       # Process Algebra Family
│   │   ├── 02-automata.md               # Automata Models
│   │   ├── 03-net-models.md             # Net Models (Petri Nets)
│   │   ├── abstract-interpretation.md   # Abstract Interpretation
│   │   └── dataflow-analysis-formal.md  # Dataflow Analysis Formalization
│   ├── 03-resource-deployment/
│   │   ├── 01-virtualization.md         # Virtualization Formalization
│   │   ├── 02-container-orchestration.md # Container Orchestration
│   │   └── 03-elasticity.md             # Elastic Scaling
│   ├── 04-consistency/
│   │   ├── 01-consistency-spectrum.md   # Consistency Spectrum
│   │   ├── 02-cap-theorem.md            # CAP Theorem
│   │   └── consistency-decision-tree.md # Consistency Selection Decision Tree
│   └── 05-verification-methods/
│       ├── 01-logic-methods.md          # Logic Methods (TLA+/Event-B)
│       ├── 02-model-checking.md         # Model Checking
│       └── 03-theorem-proving.md        # Theorem Proving
│
├── 04-application-layer/                # Unit 4: Application Layer Formalization
│   ├── 01-workflow/
│   │   ├── 01-workflow-formalization.md # Workflow Formalization Goals
│   │   ├── 02-soundness-axioms.md       # Soundness Axiom Systems
│   │   ├── 03-bpmn-semantics.md         # BPMN Formal Semantics
│   │   ├── 04-workflow-patterns.md      # Workflow Patterns
│   │   └── scenario-tree.md             # Scenario Decision Tree
│   ├── 02-stream-processing/
│   │   ├── 01-stream-formalization.md   # Stream Computing Formalization Goals
│   │   ├── 02-kahn-theorem.md           # Kahn Fixed-Point Theorem
│   │   ├── 03-window-semantics.md       # Window Semantics
│   │   ├── 04-flink-formalization.md    # Flink Formalization
│   │   ├── 04-flink-formal-verification.md # Flink Formal Verification
│   │   ├── 05-spark-formal-verification.md # Spark Formal Verification
│   │   ├── 05-stream-joins.md           # Stream Join Formalization
│   │   └── scenario-tree.md             # Scenario Decision Tree
│   ├── 03-cloud-native/
│   │   ├── 01-cloud-formalization.md    # Cloud-Native Formalization Goals
│   │   ├── 02-kubernetes-verification.md # K8s Verification
│   │   ├── 03-industrial-cases.md       # Industrial Practice Cases
│   │   ├── 04-service-mesh.md           # Service Mesh Formalization
│   │   └── 05-serverless.md             # Serverless Formalization
│   ├── 04-blockchain-verification/
│   │   └── 01-smart-contract-formalization.md # Smart Contract Formalization
│   ├── 05-network-protocol-verification/
│   │   └── 01-tcp-formalization.md      # TCP Protocol Formalization
│   └── 06-compiler-verification/
│       └── 01-compiler-correctness.md   # Compiler Correctness
│
├── 05-verification/                     # Unit 5: Verification Methods
│   ├── 01-logic/
│   │   ├── 01-tla-plus.md               # TLA+ Temporal Logic
│   │   ├── 02-event-b.md                # Event-B Refinement
│   │   └── 03-separation-logic.md       # Separation Logic
│   ├── 02-model-checking/
│   │   ├── 01-explicit-state.md         # Explicit State Model Checking
│   │   ├── 02-symbolic-mc.md            # Symbolic Model Checking
│   │   └── 03-realtime-mc.md            # Real-Time Model Checking
│   └── 03-theorem-proving/
│       ├── 01-coq-isabelle.md           # Coq/Isabelle
│       ├── 02-smt-solvers.md            # SMT Solvers
│       └── 03-lean4.md                  # Lean 4 Modern Theorem Proving
│
├── 06-tools/                            # Unit 6: Toolchain
│   ├── academic/
│   │   ├── 01-spin-nusmv.md             # SPIN/NuSMV
│   │   ├── 02-uppaal.md                 # UPPAAL
│   │   ├── 03-cpn-tools.md              # CPN Tools
│   │   ├── 04-tla-toolbox.md            # TLA+ Toolbox
│   │   ├── 05-rodin.md                  # Rodin Event-B Platform
│   │   ├── 06-dafny.md                  # Dafny Program Verification
│   │   ├── 07-ivy.md                    # Ivy Verification Tool
│   │   └── 05-quantum-formalization.md  # Quantum Formalization
│   ├── industrial/
│   │   ├── 01-aws-zelkova-tiros.md      # AWS Zelkova/Tiros
│   │   ├── 02-azure-verification.md     # Azure Verification
│   │   ├── 03-google-kubernetes.md      # Google K8s Verification
│   │   ├── 04-facebook-infer.md         # Facebook Infer
│   │   ├── 05-rust-verification.md      # Rust Verification Ecosystem
│   │   ├── 06-fizzbee.md                # FizzBee Distributed Specifications
│   │   ├── 07-shuttle-turmoil.md        # AWS Deterministic Simulation Framework
│   │   ├── 09-azure-ccf.md              # Azure CCF Smart Casual
│   │   ├── aws-s3-formalization.md      # AWS S3 Formalization
│   │   ├── azure-service-fabric.md      # Azure Service Fabric
│   │   ├── compcert.md                  # CompCert Compiler Verification
│   │   ├── google-chubby.md             # Google Chubby Lock Service
│   │   ├── ironfleet.md                 # Ironfleet Verification System
│   │   └── sel4-case-study.md           # seL4 Microkernel Verification
│   └── tutorials/
│       ├── 01-tla-plus-tutorial.md      # TLA+ Getting Started Tutorial
│       ├── 02-coq-tutorial.md           # Coq Getting Started Tutorial
│       └── 03-spin-tutorial.md          # SPIN Getting Started Tutorial
│
├── 07-future/                           # Unit 7: Challenges and Future
│   ├── 01-current-challenges.md         # Current Challenges
│   ├── 02-future-trends.md              # Future Trends
│   ├── 03-ai-formal-methods.md          # AI Formal Methods
│   ├── 03-history-of-formal-methods.md  # History of Formal Methods
│   ├── 04-quantum-distributed.md        # Quantum Distributed Systems
│   ├── 05-web3-blockchain.md            # Web3 and Blockchain
│   ├── 06-cyber-physical.md             # Cyber-Physical Systems
│   └── 07-formal-methods-education.md   # Formal Methods Education
│
├── 08-ai-formal-methods/                # Unit 8: AI Formal Methods
│   ├── README.md                        # Directory Index
│   ├── 01-neural-theorem-proving.md     # Neural Theorem Proving (AlphaProof, etc.)
│   ├── 02-llm-formalization.md          # LLM Formal Specification Generation
│   ├── 03-neural-network-verification.md # Neural Network Verification
│   └── 04-neuro-symbolic-ai.md          # Neuro-Symbolic AI
│
├── 98-appendices/                       # Appendices
│   ├── 01-key-theorems.md               # Key Theorems Summary
│   ├── 02-glossary.md                   # Glossary
│   ├── 03-theorem-index.md              # Global Theorem Index
│   ├── 03-theorem-dependency-graph.md   # Theorem Dependency Graph
│   ├── 04-cross-references.md           # Cross-Reference Index
│   ├── 05-global-search-index.md        # Global Search Index
│   ├── 06-educational-resources.md      # Educational Resources
│   ├── 07-faq.md                        # Frequently Asked Questions
│   ├── KNOWLEDGE-GRAPH.md               # Knowledge Graph Navigation
│   └── wikipedia-concepts/              # Wikipedia 25 Concepts Full Coverage
│       ├── README.md                    # Concept Index
│       ├── 01-formal-methods.md         # Formal Methods
│       ├── 02-model-checking.md         # Model Checking
│       ├── 03-theorem-proving.md        # Theorem Proving
│       ├── 04-process-calculus.md       # Process Calculus
│       ├── 05-temporal-logic.md         # Temporal Logic
│       ├── 06-hoare-logic.md            # Hoare Logic
│       ├── 07-type-theory.md            # Type Theory
│       ├── 08-abstract-interpretation.md # Abstract Interpretation
│       ├── 09-bisimulation.md           # Bisimulation
│       ├── 10-petri-nets.md             # Petri Nets
│       ├── 11-distributed-computing.md  # Distributed Computing
│       ├── 12-byzantine-fault-tolerance.md # Byzantine Fault Tolerance
│       ├── 13-consensus.md              # Consensus Algorithms
│       ├── 14-cap-theorem.md            # CAP Theorem
│       ├── 15-linearizability.md        # Linearizability
│       ├── 16-serializability.md        # Serializability
│       ├── 17-two-phase-commit.md       # Two-Phase Commit
│       ├── 18-paxos.md                  # Paxos Algorithm
│       ├── 19-raft.md                   # Raft Algorithm
│       ├── 20-distributed-hash-table.md # Distributed Hash Table
│       ├── 21-modal-logic.md            # Modal Logic
│       ├── 22-first-order-logic.md      # First-Order Logic
│       ├── 23-set-theory.md             # Set Theory
│       ├── 24-domain-theory.md          # Domain Theory
│       └── 25-category-theory.md        # Category Theory
│
└── 99-references/                       # Reference Network
    ├── bibliography.md                  # Complete Bibliography Index
    ├── classical-papers.md              # Classical Papers Classification
    ├── surveys.md                       # Survey Literature
    ├── books.md                         # Classic Books
    ├── conferences.md                   # Academic Conferences
    ├── online-resources.md              # Online Resources
    └── by-topic/                        # By-Topic Classification
        ├── README.md
        ├── model-checking.md
        ├── theorem-proving.md
        ├── process-algebra.md
        └── distributed-systems.md
```

---

## 🚀 Quick Start Guide

### 5-Minute Project Overview

Recommended reading order for new users:

1. **[📖 Wikipedia Concept Index](98-appendices/wikipedia-concepts/README.md)** - Quick browse of 25 core concepts
2. **[🎯 Learning Path Recommendations](LEARNING-PATHS.md)** - Choose learning paths based on your background
3. **[❓ Frequently Asked Questions](98-appendices/07-faq.md)** - Answers to common questions

### Choose Your Learning Path

| Your Background | Recommended Starting Point | Estimated Duration | Target Outcome |
|-----------------|---------------------------|-------------------|----------------|
| **Distributed Systems Engineer** | `04-application-layer/` → `06-tools/` | 2-3 weeks | Master verification tool usage |
| **Programming Language Researcher** | `01-foundations/` → `02-calculi/` | 3-4 weeks | Understand formal foundation theory |
| **Student/Beginner** | `LEARNING-PATHS.md` → `98-appendices/wikipedia-concepts/` | 1-2 weeks | Build complete knowledge framework |
| **Industrial Verification Engineer** | `06-tools/industrial/` → `04-application-layer/` | 2-3 weeks | Master industrial-grade verification practices |

---

## 🎯 Learning Path Recommendations

### Path 1: Theoretical Research Track

```
01-foundations → 02-calculi → 03-model-taxonomy → 05-verification → 98-appendices/03-theorem-index.md
```

**Target Audience**: Academic researchers, PhD students, those interested in theoretical depth

### Path 2: Engineering Practice Track

```
04-application-layer → 06-tools → 03-model-taxonomy/03-resource-deployment → 07-future
```

**Target Audience**: System engineers, DevOps, industrial verification engineers

### Path 3: Quick Start Track

```
02-calculi/02-pi-calculus → 04-application-layer/01-workflow → 04-application-layer/02-stream-processing → 06-tools
```

**Target Audience**: Those with programming foundations who want to get hands-on quickly

### Path 4: AI Formal Methods Special Topic

```
08-ai-formal-methods/ → 07-future/03-ai-formal-methods.md → 06-tools/academic/05-quantum-formalization.md
```

**Target Audience**: AI researchers, those exploring the intersection of AI and formal methods

---

## 🌟 Phase B Completion Statement: Wikipedia 25 Concepts Full Coverage

> **Status**: ✅ **100% Complete**

We have completed in-depth analysis of **25 core concepts** in the Wikipedia distributed systems and formal methods domains. Each concept includes:

- ✅ Formal definitions and mathematical semantics
- ✅ Core theorems and proofs
- ✅ Industrial application cases
- ✅ Visual relationship diagrams
- ✅ Mapping of associations with other concepts

### 📚 Wikipedia Concept Direct Navigation

| Category | Concept Links |
|----------|---------------|
| **Foundation Theory** | [Formal Methods](98-appendices/wikipedia-concepts/01-formal-methods.md) · [Type Theory](98-appendices/wikipedia-concepts/07-type-theory.md) · [Set Theory](98-appendices/wikipedia-concepts/23-set-theory.md) · [First-Order Logic](98-appendices/wikipedia-concepts/22-first-order-logic.md) · [Modal Logic](98-appendices/wikipedia-concepts/21-modal-logic.md) |
| **Verification Technology** | [Model Checking](98-appendices/wikipedia-concepts/02-model-checking.md) · [Theorem Proving](98-appendices/wikipedia-concepts/03-theorem-proving.md) · [Abstract Interpretation](98-appendices/wikipedia-concepts/08-abstract-interpretation.md) · [Hoare Logic](98-appendices/wikipedia-concepts/06-hoare-logic.md) |
| **Computational Models** | [Process Calculus](98-appendices/wikipedia-concepts/04-process-calculus.md) · [Temporal Logic](98-appendices/wikipedia-concepts/05-temporal-logic.md) · [Petri Nets](98-appendices/wikipedia-concepts/10-petri-nets.md) · [Bisimulation](98-appendices/wikipedia-concepts/09-bisimulation.md) |
| **Distributed Systems Core** | [Distributed Computing](98-appendices/wikipedia-concepts/11-distributed-computing.md) · [Consensus Algorithms](98-appendices/wikipedia-concepts/13-consensus.md) · [CAP Theorem](98-appendices/wikipedia-concepts/14-cap-theorem.md) · [Linearizability](98-appendices/wikipedia-concepts/15-linearizability.md) · [Serializability](98-appendices/wikipedia-concepts/16-serializability.md) |
| **Fault Tolerance** | [Byzantine Fault Tolerance](98-appendices/wikipedia-concepts/12-byzantine-fault-tolerance.md) · [Two-Phase Commit](98-appendices/wikipedia-concepts/17-two-phase-commit.md) · [Paxos](98-appendices/wikipedia-concepts/18-paxos.md) · [Raft](98-appendices/wikipedia-concepts/19-raft.md) |
| **Data Structures** | [Distributed Hash Table](98-appendices/wikipedia-concepts/20-distributed-hash-table.md) · [Domain Theory](98-appendices/wikipedia-concepts/24-domain-theory.md) · [Category Theory](98-appendices/wikipedia-concepts/25-category-theory.md) |

👉 **[View Complete Wikipedia Concept Index](98-appendices/wikipedia-concepts/README.md)**

---

## 🏭 Phase C Completion Statement: Industrial Case Deepening

> **Status**: ✅ **Complete**

We have included **15+ industrial-grade formal verification cases**, covering:

### Cloud Service Provider Cases

- **[AWS S3](06-tools/industrial/aws-s3-formalization.md)** - Zelkova/Tiros Policy Verification
- **[Azure CCF](06-tools/industrial/09-azure-ccf.md)** - Smart Casual Verification Framework
- **[Google Chubby](06-tools/industrial/google-chubby.md)** - Lock Service Formalization

### Operating Systems and Kernels

- **[seL4](06-tools/industrial/sel4-case-study.md)** - Microkernel Integrity Verification
- **[Ironfleet](06-tools/industrial/ironfleet.md)** - Distributed System Verification

### Compilers and Languages

- **[CompCert](06-tools/industrial/compcert.md)** - Verified Compiler
- **[Rust Verification](06-tools/industrial/05-rust-verification.md)** - Ownership Formalization

### Emerging Tools

- **[FizzBee](06-tools/industrial/06-fizzbee.md)** - High-Level Distributed Specification Language
- **[Shuttle/Turmoil](06-tools/industrial/07-shuttle-turmoil.md)** - Deterministic Simulation Framework

👉 **[View All Industrial Cases](06-tools/industrial/README.md)**

---

## 🔍 Global Index System

This project provides a complete cross-document indexing system:

| Index Type | File Path | Purpose |
|------------|-----------|---------|
| **Global Theorem Index** | [98-appendices/03-theorem-index.md](98-appendices/03-theorem-index.md) | Find all theorems by category |
| **Theorem Dependency Graph** | [98-appendices/03-theorem-dependency-graph.md](98-appendices/03-theorem-dependency-graph.md) | Understand theorem proof relationships |
| **Cross-Reference Index** | [98-appendices/04-cross-references.md](98-appendices/04-cross-references.md) | Cross-document concept associations |
| **Global Search Index** | [98-appendices/05-global-search-index.md](98-appendices/05-global-search-index.md) | Keyword full-text search |
| **Knowledge Graph** | [98-appendices/KNOWLEDGE-GRAPH.md](98-appendices/KNOWLEDGE-GRAPH.md) | Visual knowledge network |
| **Glossary** | [98-appendices/02-glossary.md](98-appendices/02-glossary.md) | Professional terminology explanations |

---

## 🤖 AI Formal Methods Zone

Unit 8 **AI Formal Methods** explores the intersection of artificial intelligence and formal methods:

| Topic | Document | Core Content |
|-------|----------|--------------|
| **Neural Theorem Proving** | [01-neural-theorem-proving.md](08-ai-formal-methods/01-neural-theorem-proving.md) | AlphaProof, LeanDojo, etc. |
| **LLM Formalization** | [02-llm-formalization.md](08-ai-formal-methods/02-llm-formalization.md) | LLM-generated formal specifications |
| **Neural Network Verification** | [03-neural-network-verification.md](08-ai-formal-methods/03-neural-network-verification.md) | AI system safety verification |
| **Neuro-Symbolic AI** | [04-neuro-symbolic-ai.md](08-ai-formal-methods/04-neuro-symbolic-ai.md) | Symbolic and neural network combination |

👉 **[Enter AI Formal Methods Zone](08-ai-formal-methods/README.md)**

---

## 📈 Unit Detailed Statistics

| Unit | Topics | Files | Status | Highlights |
|------|--------|-------|--------|------------|
| 01-foundations | 6 | 7 | ✅ Complete | Added Domain Theory, Type Theory, Coalgebra |
| 02-calculi | 3 | 15 | ✅ Complete | Extended π-calculus patterns and encodings |
| 03-model-taxonomy | 5 | 16 | ✅ Complete | Added Abstract Interpretation, Dataflow Analysis |
| 04-application-layer | 6 | 18 | ✅ Complete | Added Blockchain, Network Protocol, Compiler Verification |
| 05-verification | 3 | 9 | ✅ Complete | Lean 4 Modern Theorem Proving |
| 06-tools | 3 | 22 | ✅ Complete | Added FizzBee, Shuttle, Ivy, etc. |
| 07-future | 8 | 8 | ✅ Complete | Added AI Formalization, Quantum, Education |
| **08-ai-formal-methods** | **4** | **5** | ✅ **New** | AI and Formal Methods Cross-Frontier |
| 98-appendices | 10 | 27 | ✅ Complete | Wikipedia 25 Concepts Full Coverage |
| 99-references | 7 | 7 | ✅ Complete | Subject-Classified References |
| **Index** | - | 7 | ✅ Complete | Global Index System |
| **Total** | **45+** | **95+** | ✅ **100% Complete** | Continuously Updated |

---

## 🔄 Continuous Progress Plan

| Phase | Timeline | Goal | Status |
|-------|----------|------|--------|
| Phase A | 2026-04 | Complete foundational framework (8 units) | ✅ Completed |
| Phase B | 2026-04 | Wikipedia 25 core concepts full coverage | ✅ 100% Complete |
| Phase C | 2026-04 | Industrial case deepening (15+ cases) | ✅ Completed |
| Phase D | 2026-04+ | Knowledge graph and learning path system | 🚧 In Progress |
| Phase E | 2026-05+ | Community contributions and continuous maintenance | ⏳ Planned |

---

## 🌐 English Community Resources

### Academic Communities

| Community | Description | Link |
|-----------|-------------|------|
| **TLA+ Google Group** | TLA+ user community and discussions | <https://groups.google.com/g/tlaplus> |
| **Coq Discourse** | Coq theorem prover community forum | <https://coq.discourse.group/> |
| **Lean Zulip Chat** | Lean prover real-time chat community | <https://leanprover.zulipchat.com/> |
| **Isabelle Mailing List** | Isabelle/HOL user mailing list | <https://lists.cam.ac.uk/mailman/listinfo/cl-isabelle-users> |
| **Formal Methods World** | Global formal methods community hub | <https://www.formal-methods.com/> |
| **FME (Formal Methods Europe)** | European formal methods association | <https://www.fmeurope.org/> |

### Industrial Verification Communities

| Organization | Resource | Description |
|--------------|----------|-------------|
| **AWS** | [AWS Open Source Formal Methods](https://github.com/awslabs) | TLA+ specifications for AWS services |
| **Microsoft** | [TLA+ in Azure](https://azure.microsoft.com/en-us/blog/tag/tla/) | Azure verification case studies |
| **Google** | [Chubby Paper](https://research.google/pubs/pub27897/) | Lock service formalization |
| **Rust** | [Rust Verification Workshop](https://sites.google.com/view/rustverify2024) | Rust verification community |
| **seL4** | [seL4 Forum](https://sel4.discourse.group/) | Microkernel verification community |

### Key Conferences and Workshops

| Conference/Workshop | Focus Area | Typical Timeline |
|---------------------|------------|------------------|
| **CAV** | Computer Aided Verification | July |
| **FM** | Formal Methods | TBD (biennial) |
| **TACAS** | Tools and Algorithms for Construction and Analysis of Systems | April |
| **POPL** | Principles of Programming Languages | January |
| **PLDI** | Programming Language Design and Implementation | June |
| **CONCUR** | Concurrency Theory | September |
| **DISC** | Distributed Computing | October |
| **NSDI/SOSP/OSDI** | Systems (with increasing formal methods presence) | Various |

### Educational Resources (English)

| Resource | Type | Description |
|----------|------|-------------|
| **MIT 6.826** | Course | Principles of Computer Systems (formal methods focus) |
| **CMU 15-712** | Course | Advanced and Distributed Operating Systems |
| **Stanford CS240** | Course | Advanced Topics in Operating Systems |
| **Berkeley CS162** | Course | Operating Systems and System Programming |
| **TLA+ Video Course** | Video | Leslie Lamport's TLA+ video series |
| **Software Foundations** | Book/Tutorial | Coq-based formal methods course (online) |
| **Concrete Semantics** | Book | Isabelle/HOL semantics formalization |

### Online Forums and Q&A

| Platform | Purpose |
|----------|---------|
| **Stack Overflow** | `[tla+]`, `[coq]`, `[isabelle]`, `[formal-methods]` tags |
| **CS Theory Stack Exchange** | Theoretical computer science Q&A |
| **Reddit r/formalmethods** | Formal methods community discussions |
| **Theoretical Computer Science Discord** | Real-time discussions |

---

## 🆘 Getting Help

- **📖 [Frequently Asked Questions (FAQ)](98-appendices/07-faq.md)** - Answers to most common questions
- **🎯 [Learning Path Guide](LEARNING-PATHS.md)** - Choose learning paths based on background
- **📚 [Glossary](98-appendices/02-glossary.md)** - Quick reference for professional terminology
- **🔗 [Cross-Reference Index](98-appendices/04-cross-references.md)** - Cross-document navigation

---

## 🔗 External Authoritative Resources Index

| Resource Type | Link/Description |
|---------------|------------------|
| **TLA+** | <https://lamport.azurewebsites.net/tla/tla.html> |
| **Coq** | <https://coq.inria.fr/> |
| **Isabelle** | <https://isabelle.in.tum.de/> |
| **Lean** | <https://lean-lang.org/> |
| **UPPAAL** | <https://uppaal.org/> |
| **CPN Tools** | <https://cpntools.org/> |
| **SPIN** | <https://spinroot.com/> |
| **AWS TLA+** | <https://github.com/tlaplus/awslabs> |
| **seL4** | <https://sel4.systems/> |
| **CompCert** | <https://compcert.org/> |
| **FizzBee** | <https://fizzbee.io/> |

---

## 📜 Contributing and Community

### How to Contribute

We welcome contributions from researchers, engineers, and students worldwide:

1. **Report Issues**: Found an error or unclear explanation? Open an issue
2. **Suggest Improvements**: Have ideas for better content? Start a discussion
3. **Submit Content**: Want to add new theorems, proofs, or case studies? Submit a PR
4. **Translate**: Help translate content to other languages

### Code of Conduct

- Be respectful and professional in all interactions
- Provide constructive feedback
- Credit original authors and sources
- Follow academic integrity standards

### Contact

- **Project Maintainer**: Formal Methods Documentation Team
- **Repository**: AnalysisDataFlow/formal-methods
- **Issues**: Use GitHub Issues for bug reports and feature requests

---

## 📚 Citation

If you use this documentation in your research or work, please cite:

```bibtex
@misc{formal-methods-distribsys,
  title={Formal Methods for Distributed Systems: Complete Technical Architecture},
  author={AnalysisDataFlow Documentation Team},
  year={2026},
  url={https://github.com/AnalysisDataFlow/formal-methods},
  version={4.0}
}
```

---

## 📄 License

This documentation is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/):

- **Attribution**: You must give appropriate credit
- **ShareAlike**: If you remix, transform, or build upon the material, you must distribute your contributions under the same license

Individual code examples and tool-specific content may have their own licenses as indicated.

---

> **Contribution Guide**: This documentation system is continuously being improved. Contributions of new content and error corrections are welcome.
>
> **Last Updated**: 2026-04-10 | **Status**: ✅ Phase A/B/C Complete | 🚧 Phase D In Progress | **Document Version**: v4.0
>
> **Language Versions**: [中文 (Chinese)](README.md) | [English](README-EN.md)
