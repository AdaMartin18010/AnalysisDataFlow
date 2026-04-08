# Flink Rust 原生 API 开发指南

> 所属阶段: Flink/09-language-foundations | 前置依赖: [Flink WASM UDF GA](flink-25-wasm-udf-ga.md) | 形式化等级: L3

本文档介绍如何在 Flink 中使用 Rust 语言进行原生扩展开发。

## 1. 概述

Flink 通过 WASM (WebAssembly) 技术支持 Rust 语言的 UDF 开发。Rust 的高性能和内存安全特性使其成为流处理计算密集型任务的理想选择。

## 2. 环境准备

- Rust 编译器 (1.70+)
- wasm32-unknown-unknown target
- Flink 2.5+

## 3. 开发流程

参见 [Flink 2.5 WASM UDF GA 指南](flink-25-wasm-udf-ga.md) 获取详细开发步骤。

## 4. 参考文档

- [WASI Component Model](10-wasi-component-model.md)
- [Flink WASM Streaming](../../05-ecosystem/05.03-wasm-udf/wasm-streaming.md)
