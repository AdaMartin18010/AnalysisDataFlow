# Contributing to AnalysisDataFlow

> **Thank you for your interest in making this project better!**

---

## 1. Project Overview

AnalysisDataFlow is an open-source knowledge base dedicated to stream processing theory, architecture, and engineering practice. Our content spans:

- **Struct/**: Formal theory, proofs, and rigorous analysis
- **Knowledge/**: Design patterns, business applications, and concept maps
- **Flink/**: Apache Flink deep dives, comparisons, and roadmaps

---

## 2. How to Contribute

### 2.1 Content Contributions

We welcome contributions in the following areas:

- **Technical deep dives**: Flink internals, stream processing patterns, case studies
- **Translations**: Expanding English documentation (`en/`)
- **Visualizations**: Mermaid diagrams, architecture illustrations
- **Code examples**: Validated Java, Python, SQL, and YAML snippets
- **Fixes**: Broken links, outdated information, typos

### 2.2 Contribution Workflow

1. **Open an Issue**: Describe the proposed change or content gap
2. **Discussion**: Maintainters will provide feedback and scope alignment
3. **Draft & Review**: Submit a PR following our style guidelines
4. **Merge**: After approval, your contribution becomes part of the knowledge graph

---

## 3. Writing Standards

### 3.1 Document Structure (The "Six-Section Template")

Core documents **must** include:

1. **Concept Definitions** — Formal definitions with intuitive explanations
2. **Property Derivation** — Lemmas and propositions derived from definitions
3. **Relation Establishment** — Mappings to other concepts/systems
4. **Argumentation** — Auxiliary theorems, counterexamples, boundary discussions
5. **Proof / Engineering Argument** — Complete proofs or rigorous engineering rationale
6. **Examples** — Simplified examples, code snippets, real-world cases
7. **Visualizations** — At least one Mermaid diagram
8. **References** — Cited using `[^n]` format

### 3.2 Naming Convention

- All lowercase with hyphens: `topic-name.md`
- Include hierarchical prefix: `01.02-topic-name.md`

### 3.3 Formal Element Numbering

| Type | Prefix | Example |
|------|--------|---------|
| Theorem | Thm | `Thm-S-01-01` |
| Lemma | Lemma | `Lemma-S-01-02` |
| Definition | Def | `Def-S-01-01` |
| Proposition | Prop | `Prop-S-03-01` |
| Corollary | Cor | `Cor-S-02-01` |

---

## 4. Quality Checklist

Before submitting a PR, please verify:

- [ ] The document follows the six-section template (for core docs)
- [ ] All Mermaid diagrams render correctly
- [ ] External links are valid
- [ ] Code examples are syntactically correct
- [ ] References use the `[^n]` superscript format
- [ ] The file is placed in the correct directory (Struct/, Knowledge/, or Flink/)

---

## 5. Community

- **Discussions**: Use GitHub Discussions for questions and ideas
- **Issues**: Report bugs or request content via GitHub Issues
- **Code of Conduct**: Be respectful, constructive, and inclusive

---

## 6. References
