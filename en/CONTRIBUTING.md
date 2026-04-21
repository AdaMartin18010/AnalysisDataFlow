# Contributing to AnalysisDataFlow

> **Language**: English | **Source**: [../CONTRIBUTING.md](../CONTRIBUTING.md) | **Last Updated**: 2026-04-21

---

## Welcome

Thank you for your interest in contributing to AnalysisDataFlow! This project is a comprehensive knowledge base for streaming computation theory, hierarchical structures, engineering practices, and business modeling.

## Contribution Areas

| Area | Description | Skills Needed |
|------|-------------|---------------|
| **Content** | New documents, translations, corrections | Domain expertise in streaming/Flink/formal methods |
| **Formalization** | Coq/Lean/TLA+ proofs, theorem registration | Type theory, logic, proof assistants |
| **Translation** | English/i18n translations of core documents | Bilingual technical writing |
| **Quality** | Cross-reference fixing, link checking, Mermaid validation | Attention to detail |
| **Tools** | Automation scripts, CI/CD improvements | Python, GitHub Actions |

## Document Standards

### Naming Convention

All documents must follow: `{layer}.{sequence}-{topic-keywords}.md`
- All lowercase
- Hyphen `-` as separator

### Six-Section Template (Mandatory)

Every core document must contain:
1. **Definitions** — Formal definitions with at least one `Def-*` numbering
2. **Properties** — Derived lemmas with `Lemma-*` or `Prop-*` numbering
3. **Relations** — Mappings to other concepts/models/systems
4. **Argumentation** — Auxiliary theorems, counterexamples, boundary discussions
5. **Proof / Engineering Argument** — Complete proofs or rigorous engineering reasoning
6. **Examples** — Simplified instances, code snippets, configuration examples
7. **Visualizations** — At least one Mermaid diagram
8. **References** — `[^n]` format, centralized at document end

### Formal Element Numbering

Use global unified numbering: `{Type}-{Stage}-{DocSeq}-{Order}`

| Type | Abbreviation | Example |
|------|-------------|---------|
| Theorem | Thm | `Thm-S-01-01` |
| Definition | Def | `Def-S-01-01` |
| Lemma | Lemma | `Lemma-S-01-02` |
| Proposition | Prop | `Prop-K-03-01` |
| Corollary | Cor | `Cor-S-02-01` |

## Submission Process

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b content/{topic}`
3. **Write** following the six-section template
4. **Validate** using local scripts:
   ```bash
   python .scripts/validate-cross-refs.py
   python .scripts/six-section-validator.py
   python .scripts/mermaid-syntax-checker.py
   ```
5. **Submit** a Pull Request with clear description

## Code of Conduct

- Be respectful and constructive in discussions
- Cite authoritative sources for technical claims
- Prefer minimal changes that achieve the goal
- Update indexes (00-INDEX.md) when adding new documents

## Contact

For questions or clarifications, open a GitHub Discussion or refer to [COMMUNITY/SETUP-GUIDE.md](../COMMUNITY/SETUP-GUIDE.md).
