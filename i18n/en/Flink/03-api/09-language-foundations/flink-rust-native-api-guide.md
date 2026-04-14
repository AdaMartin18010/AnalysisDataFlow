---
title: "Flink Rust Native API Development Guide"
translation_status: "ai_translated_reviewed"
source_version: "v4.1"
last_sync: "2026-04-15"
---

# Flink Rust Native API Development Guide

> **Status**: Forward-looking | **Estimated Release**: 2026-Q3 | **Last Updated**: 2026-04-12
>
> ⚠️ The features described in this document are in early discussion stages and have not been officially released. Implementation details may change.

> **Stage**: Flink/09-language-foundations | **Prerequisites**: [Flink WASM UDF GA](flink-25-wasm-udf-ga.md) | **Formalization Level**: L3

This document introduces how to develop native extensions in Rust for Flink.

## 1. Overview

Flink supports Rust UDF development through WASM (WebAssembly) technology. Rust's high performance and memory safety characteristics make it an ideal choice for compute-intensive stream processing tasks.

## 2. Environment Preparation

- Rust compiler (1.70+)
- wasm32-unknown-unknown target
- Flink 2.5+

## 3. Development Workflow

Refer to the [Flink 2.5 WASM UDF GA Guide](flink-25-wasm-udf-ga.md) for detailed development steps.

## 4. Reference Documents

- [WASI Component Model](10-wasi-component-model.md)
- [Flink WASM Streaming](../../05-ecosystem/05.03-wasm-udf/wasm-streaming.md)
