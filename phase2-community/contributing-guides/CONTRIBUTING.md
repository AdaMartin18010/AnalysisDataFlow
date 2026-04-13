# Contributing Guide - Phase 2 Community Building

> **Project**: AnalysisDataFlow
> **Version**: Phase 2
> **Last Updated**: 2026-04-09

Thank you for your interest in contributing to AnalysisDataFlow! This document provides guidelines and instructions for contributing.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [How to Contribute](#how-to-contribute)
3. [Contribution Types](#contribution-types)
4. [Style Guidelines](#style-guidelines)
5. [Review Process](#review-process)
6. [Community Guidelines](#community-guidelines)

---

## Getting Started

### Prerequisites

- GitHub account
- Basic understanding of Markdown
- Familiarity with stream processing concepts (for content contributions)

### Setup Development Environment

```bash
# Fork the repository
# Clone your fork
git clone https://github.com/YOUR_USERNAME/AnalysisDataFlow.git
cd AnalysisDataFlow

# Create a branch for your contribution
git checkout -b feature/your-contribution
```

---

## How to Contribute

### 1. Report Issues

If you find errors, broken links, or have suggestions:

1. Check if the issue already exists
2. Create a new issue with:
   - Clear title
   - Detailed description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior

### 2. Submit Content

#### Option A: Direct Edit (Small Changes)

1. Navigate to the file on GitHub
2. Click the edit (pencil) icon
3. Make your changes
4. Submit a Pull Request

#### Option B: Local Development (Large Changes)

1. Fork and clone the repository
2. Create a new branch: `git checkout -b feature/description`
3. Make your changes
4. Test locally (see [Testing](#testing))
5. Commit with clear messages
6. Push to your fork
7. Create a Pull Request

### 3. Translation Contributions

We welcome translations! See [Translation Guide](#translation-guide).

---

## Contribution Types

### Type 1: Documentation Improvements

- Fix typos and grammar
- Improve clarity and readability
- Update outdated information
- Add examples or clarifications

**Priority**: High
**Skill Level**: Beginner-friendly

### Type 2: New Content

- Add new case studies
- Create tutorials or guides
- Write technical deep-dives
- Develop interactive examples

**Priority**: Medium
**Skill Level**: Intermediate

### Type 3: Formalization Work

- Create formal proofs (Coq, TLA+, etc.)
- Verify existing proofs
- Add machine-checkable specifications

**Priority**: High
**Skill Level**: Advanced (formal methods expertise required)

### Type 4: Tool Development

- Build automation tools
- Create visualization components
- Develop CI/CD improvements

**Priority**: Medium
**Skill Level**: Intermediate to Advanced

### Type 5: Translations

- Translate documents to other languages
- Review and improve existing translations
- Maintain translation consistency

**Priority**: Medium
**Skill Level**: Beginner-friendly (requires language proficiency)

---

## Style Guidelines

### Markdown Style

- Use ATX-style headers (`#` not `===`)
- Wrap lines at 80-100 characters
- Use fenced code blocks with language tags
- Prefer `-` for unordered lists

### Content Structure

Documents should follow this structure:

```markdown
# Title

> Metadata: version, date, status

## Summary

Brief overview (2-3 sentences)

## 1. Section Name

### 1.1 Subsection

Content...

## 2. Another Section

...

## References

[^1]: Citation...
```

### Mathematical Notation

- Use LaTeX for math: `$E = mc^2$`
- Define symbols before first use
- Number equations for reference

### Code Examples

- Provide runnable examples when possible
- Include comments explaining key parts
- Specify version requirements

---

## Translation Guide

### Getting Started

1. Check the [i18n directory](../i18n/) for your language
2. See [translation status](../README.md) for pending work
3. Claim a document by opening an issue

### Translation Standards

- Maintain technical accuracy
- Use industry-standard terminology
- Keep formatting consistent with original
- Add translator notes for ambiguous terms

### Review Process

Translations require:

1. Initial translation by contributor
2. Review by native speaker
3. Technical review by domain expert
4. Final approval by maintainer

---

## Review Process

### Pull Request Checklist

Before submitting PR:

- [ ] Content follows style guidelines
- [ ] No broken links (run link checker)
- [ ] Grammar and spelling checked
- [ ] Examples tested (if applicable)
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### Review Timeline

- Initial response: 3-5 days
- Review completion: 1-2 weeks
- Complex changes: 2-4 weeks

### Feedback Incorporation

1. Address reviewer comments
2. Update PR with changes
3. Request re-review when ready

---

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Assume good intentions
- Focus on constructive feedback

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions, ideas
- **Slack/Discord**: Real-time chat (invite-only)
- **Email**: <analysisdataflow@example.org>

### Recognition

Contributors will be:

- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Eligible for committer status (after sustained contributions)

---

## Testing

### For Documentation

```bash
# Install dependencies
pip install -r requirements.txt

# Run link checker
python tools/link_checker.py

# Run format validator
python tools/format_validator.py
```

### For Formal Proofs

```bash
# Compile Coq proofs
coq_makefile -f _CoqProject -o Makefile
make

# Check TLA+ models
tlc ModelName.tla
```

---

## Questions?

- Check [FAQ](../../FAQ.md)
- Open a [GitHub Discussion](../../discussions)
- Contact maintainers: <maintainers@analysisdataflow.org>

---

Thank you for contributing to AnalysisDataFlow! 🎉
