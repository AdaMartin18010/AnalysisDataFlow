# AnalysisDataFlow Internationalization (i18n)

> **Stream Computing Knowledge Base - Multi-language Documentation**

---

## 🌍 Supported Languages

| Language | Code | Status | Path | Completeness |
|----------|------|--------|------|--------------|
| 🇨🇳 中文 (Chinese) | zh | ✅ Active | [./zh/](./zh/) | 100% (Source) |
| 🇬🇧 English | en | ✅ Active | [./en/](./en/) | Core Docs |
| 🇯🇵 日本語 (Japanese) | ja | 📝 Partial (4 docs) | [./ja/](./ja/) | ~1% |
| 🇰🇷 한국어 (Korean) | ko | ⏸️ On Hold | - | - |

---

## 📖 English Documentation

The English documentation includes the following core guides:

| Document | Description | Path |
|----------|-------------|------|
| **Overview** | Project overview and introduction | [en/00-OVERVIEW.md](./en/00-OVERVIEW.md) |
| **Struct Guide** | Formal theory documentation guide | [en/01-STRUCT-GUIDE.md](./en/01-STRUCT-GUIDE.md) |
| **Knowledge Guide** | Engineering knowledge guide | [en/02-KNOWLEDGE-GUIDE.md](./en/02-KNOWLEDGE-GUIDE.md) |
| **Flink Guide** | Flink-specific technology guide | [en/03-FLINK-GUIDE.md](./en/03-FLINK-GUIDE.md) |
| **Quick Start** | Quick start guide for beginners | [en/04-QUICK-START.md](./en/04-QUICK-START.md) |
| **Learning Path** | Learning path guide | [en/05-LEARNING-PATH.md](./en/05-LEARNING-PATH.md) |
| **Glossary** | Terminology reference | [en/GLOSSARY.md](./en/GLOSSARY.md) |
| **Sidebar** | Navigation sidebar | [en/_sidebar.md](./en/_sidebar.md) |
| **00-Index** | English documentation index | [en/00-INDEX.md](./en/00-INDEX.md) |
| **Architecture** | System architecture overview | [en/ARCHITECTURE.md](./en/ARCHITECTURE.md) |
| **Best Practices** | Flink production best practices | [en/BEST-PRACTICES.md](./en/BEST-PRACTICES.md) |
| **Contributing** | Contribution guidelines | [en/CONTRIBUTING.md](./en/CONTRIBUTING.md) |
| **Flink Quick Start** | Flink-specific quick start | [en/FLINK-QUICK-START.md](./en/FLINK-QUICK-START.md) |
| **Knowledge Graph** | Knowledge graph guide | [en/KNOWLEDGE-GRAPH-GUIDE.md](./en/KNOWLEDGE-GRAPH-GUIDE.md) |
| **Observability** | Stream processing observability | [en/OBSERVABILITY-GUIDE.md](./en/OBSERVABILITY-GUIDE.md) |
| **Template** | Document template | [en/TEMPLATE.md](./en/TEMPLATE.md) |
| **Troubleshooting** | Troubleshooting manual | [en/TROUBLESHOOTING.md](./en/TROUBLESHOOTING.md) |

---

## 🎯 Translation Principles

### 1. Terminology Consistency

- Core terms follow the project's [Glossary](../../GLOSSARY.md) and [GLOSSARY-EN.md](../../archive/deprecated/GLOSSARY-EN.md)
- Technical product names remain untranslated (Apache Flink, Apache Kafka, etc.)
- Code examples and configuration parameters remain unchanged

### 2. Document Structure Preservation

- All documents maintain the six-section structure from the original
- Mermaid diagrams and code blocks are preserved
- Reference links are adapted for the target language where applicable

### 3. Cross-Reference Maintenance

- Internal links point to the corresponding language version
- Links to external resources remain unchanged
- Cross-directory references maintain the original structure

---

## 🏗️ Architecture

```
docs/i18n/
├── README.md              # This file - i18n overview
├── ARCHITECTURE.md        # i18n architecture documentation
├── zh/                    # Chinese (source language)
│   └── README.md          # Pointer to root Chinese docs
├── en/                    # English
│   ├── README.md
│   ├── 00-OVERVIEW.md
│   ├── 00-INDEX.md
│   ├── 01-STRUCT-GUIDE.md
│   ├── 02-KNOWLEDGE-GUIDE.md
│   ├── 03-FLINK-GUIDE.md
│   ├── 04-QUICK-START.md
│   ├── 05-LEARNING-PATH.md
│   ├── ARCHITECTURE.md
│   ├── BEST-PRACTICES.md
│   ├── CONTRIBUTING.md
│   ├── FLINK-QUICK-START.md
│   ├── GLOSSARY.md
│   ├── KNOWLEDGE-GRAPH-GUIDE.md
│   ├── OBSERVABILITY-GUIDE.md
│   ├── TEMPLATE.md
│   ├── TROUBLESHOOTING.md
│   └── _sidebar.md
└── templates/             # Translation templates
    └── translation-template.md
```

---

## 🚀 Usage

### Switching Languages

Language switch badges are available at the top of:

- Root [README.md](../README.md)
- Root [README-EN.md](../../README-EN.md)
- Each i18n documentation page

### Navigation

- Use the [English Sidebar](./en/_sidebar.md) for English documentation navigation
- Use the [Knowledge/00-INDEX.md](../../en/00-INDEX.md) for Chinese navigation

---

## 📊 Translation Progress

### English (en)

| Category | Total Docs | Translated | Progress |
|----------|------------|------------|----------|
| Core Guides | 17 | 17 | ✅ Active |
| Struct/ | 93 | 7 | 🚧 ~8% |
| Knowledge/ | 262 | 3 | 🚧 ~1% |
| Flink/ | 408 | 1 | 🚧 ~0.2% |

---

## 🤝 Contributing

To contribute to i18n efforts:

1. Follow the [ARCHITECTURE.md](./ARCHITECTURE.md) specifications
2. Use the [translation-template.md](./templates/translation-template.md)
3. Maintain terminology consistency with the glossary
4. Ensure all code examples remain functional

---

## 📄 License

All i18n documentation follows the same [Apache License 2.0](../../../LICENSE) as the main project.

---

> **Last Updated**: 2026-04-15
>
> **Note**: Directory unification in progress. Root `en/` files are being consolidated into `docs/i18n/en/`. See [i18n/ARCHITECTURE.md](../i18n/ARCHITECTURE.md) for details.
