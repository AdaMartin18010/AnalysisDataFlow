# AnalysisDataFlow Internationalization (i18n)

> **Stream Computing Knowledge Base - Multi-language Documentation**

---

## 🌍 Supported Languages

| Language | Code | Status | Path | Completeness |
|----------|------|--------|------|--------------|
| 🇨🇳 中文 (Chinese) | zh | ✅ Active | [./zh/](./zh/) | 100% (Source) |
| 🇬🇧 English | en | ✅ Active | [./en/](./en/) | Core Docs |
| 🇯🇵 日本語 (Japanese) | ja | 📝 Planned | - | - |
| 🇰🇷 한국어 (Korean) | ko | 📝 Planned | - | - |

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

---

## 🎯 Translation Principles

### 1. Terminology Consistency

- Core terms follow the project's [Glossary](../../../GLOSSARY.md) and [GLOSSARY-EN.md](../../../GLOSSARY-EN.md)
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
│   ├── 00-OVERVIEW.md
│   ├── 01-STRUCT-GUIDE.md
│   ├── 02-KNOWLEDGE-GUIDE.md
│   ├── 03-FLINK-GUIDE.md
│   ├── 04-QUICK-START.md
│   ├── 05-LEARNING-PATH.md
│   ├── GLOSSARY.md
│   └── _sidebar.md
└── templates/             # Translation templates
    └── translation-template.md
```

---

## 🚀 Usage

### Switching Languages

Language switch badges are available at the top of:
- Root [README.md](../../../README.md)
- Root [README-EN.md](../../../README-EN.md)
- Each i18n documentation page

### Navigation

- Use the [English Sidebar](./en/_sidebar.md) for English documentation navigation
- Use the [Knowledge/00-INDEX.md](../../../Knowledge/00-INDEX.md) for Chinese navigation

---

## 📊 Translation Progress

### English (en)

| Category | Total Docs | Translated | Progress |
|----------|------------|------------|----------|
| Core Guides | 8 | 8 | ✅ 100% |
| Struct/ | 43 | 0 | 📋 Planned |
| Knowledge/ | 134 | 0 | 📋 Planned |
| Flink/ | 173 | 0 | 📋 Planned |

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

> **Last Updated**: 2026-04-08
