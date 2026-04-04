# 形式化元素编号规范 v2.0

> **生效日期**: 2026-04-04
> **适用范围**: Flink/14-rust-assembly-ecosystem/ 全部文档

---

## 1. 编号格式规范

### 1.1 基本格式

```
{Type}-{Module}-{Number}
```

| 组件 | 说明 | 示例 |
|------|------|------|
| **Type** | 元素类型 | Def, Prop, Lemma, Thm, Cor |
| **Module** | 模块代码 | WASM, SIMD, FLASH, RW, WASI, VEC, HET, EDGE, AI |
| **Number** | 两位序号 | 01-99 |

### 1.2 元素类型定义

| 类型代码 | 全称 | 用途 |
|----------|------|------|
| **Def** | Definition | 概念定义 |
| **Prop** | Proposition | 性质命题 |
| **Lemma** | Lemma | 辅助引理 |
| **Thm** | Theorem | 主要定理 |
| **Cor** | Corollary | 定理推论 |

### 1.3 模块代码定义

| 代码 | 模块名称 | 目录 |
|------|----------|------|
| **WASM** | WebAssembly 3.0 | wasm-3.0/ |
| **SIMD** | SIMD/Assembly 优化 | simd-optimization/ |
| **FLASH** | Flash 引擎分析 | flash-engine/ |
| **RW** | RisingWave 对比 | risingwave-comparison/ |
| **WASI** | WASI 0.3 异步模型 | wasi-0.3-async/ |
| **VEC** | 向量化 UDF | vectorized-udfs/ |
| **HET** | 异构计算 | heterogeneous-computing/ |
| **EDGE** | 边缘计算 | edge-wasm-runtime/ |
| **AI** | AI 原生流处理 | ai-native-streaming/ |

---

## 2. 编号分配规则

### 2.1 连续性原则

- 编号必须连续，从 01 开始
- 不得跳过编号
- 不得重复使用编号

### 2.2 文件内分配

```
文件内编号应连续分配，不预留空隙。

示例 (wasm-3.0/01-wasm-3.0-spec-guide.md):
- Def-WASM-01
- Def-WASM-02
- Def-WASM-03
- Def-WASM-04
- Def-WASM-05

下一个文件 (02-memory64-deep-dive.md):
- Def-WASM-06
- Def-WASM-07
- Def-WASM-08
- Def-WASM-09
```

### 2.3 不同类型独立编号

```
定义、命题、定理各自独立编号：

定义:
- Def-WASM-01
- Def-WASM-02
...

命题 (独立编号):
- Prop-WASM-01
- Prop-WASM-02
...

定理 (独立编号):
- Thm-WASM-01
- Thm-WASM-02
...
```

---

## 3. 命名格式规范

### 3.1 标题格式

```markdown
### Def-{Module}-{Number}: {中文名称} ({英文名称})

示例:
### Def-WASM-01: WebAssembly 模块 (WebAssembly Module)
### Prop-SIMD-02: 向量化效率 (Vectorization Efficiency)
### Thm-FLASH-01: 性能提升边界 (Performance Improvement Bound)
```

### 3.2 引用格式

```markdown
文档内引用: [Def-WASM-01](#def-wasm-01)
跨文档引用: [Def-WASM-01](../wasm-3.0/01-wasm-3.0-spec-guide.md#def-wasm-01)
```

---

## 4. 各模块编号范围

### 4.1 已分配范围 (截至 2026-04-04)

| 模块 | 定义范围 | 命题范围 | 定理范围 |
|------|----------|----------|----------|
| **WASM** | Def-WASM-01 ~ Def-WASM-17 | Prop-WASM-01 ~ Prop-WASM-15 | Thm-WASM-01 ~ Thm-WASM-04 |
| **SIMD** | Def-SIMD-01 ~ Def-SIMD-15 | Prop-SIMD-01 ~ Prop-SIMD-10 | - |
| **FLASH** | Def-FLASH-01 ~ Def-FLASH-20 | Prop-FLASH-01 ~ Prop-FLASH-15 | - |
| **RW** | Def-RW-01 ~ Def-RW-16 | Prop-RW-01 ~ Prop-RW-13 | - |
| **WASI** | Def-WASI-01 ~ Def-WASI-16 | Prop-WASI-01 ~ Prop-WASI-12 | - |
| **VEC** | Def-VEC-01 ~ Def-VEC-17 | Prop-VEC-01 ~ Prop-VEC-12 | Thm-VEC-01 ~ Thm-VEC-07 |
| **HET** | Def-HET-01 ~ Def-HET-16 | Prop-HET-01 ~ Prop-HET-12 | - |
| **EDGE** | Def-EDGE-01 ~ Def-EDGE-20 | Prop-EDGE-01 ~ Prop-EDGE-16 | - |
| **AI** | Def-AI-01 ~ Def-AI-16 | Prop-AI-01 ~ Prop-AI-09 | - |

### 4.2 预留范围

| 模块 | 预留定义范围 | 预留命题范围 |
|------|-------------|-------------|
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

## 5. 文档结构规范

### 5.1 六段式模板

每篇文档必须包含以下章节：

```markdown
## 1. 概念定义 (Definitions)
至少 3 个 Def-{Module}-* 定义

## 2. 属性推导 (Properties)
至少 2 个 Prop-{Module}-* 命题

## 3. 关系建立 (Relations)
与其他概念/系统的关系

## 4. 论证过程 (Argumentation)
技术分析与边界讨论

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)
定理证明或工程选型论证

## 6. 实例验证 (Examples)
可运行的代码示例

## 7. 可视化 (Visualizations)
至少 1 个 Mermaid 图表

## 8. 引用参考 (References)
权威资料引用
```

### 5.2 形式化元素密度

| 元素类型 | 最小数量 | 推荐数量 |
|----------|----------|----------|
| 定义 (Def) | 3 | 4-5 |
| 命题 (Prop) | 2 | 3-4 |
| 定理 (Thm) | 0 | 1-2 |
| 引理 (Lemma) | 0 | 0-1 |

---

## 6. 质量检查清单

### 6.1 新增文档检查

- [ ] 编号符合 {Type}-{Module}-{Number} 格式
- [ ] 编号连续，无跳过
- [ ] 模块代码正确
- [ ] 类型代码正确
- [ ] 标题格式正确
- [ ] 引用格式正确

### 6.2 修改文档检查

- [ ] 修改后的编号仍符合规范
- [ ] 所有引用同步更新
- [ ] 无重复编号
- [ ] 无跳号

---

## 7. 违规处理

### 7.1 常见违规

| 违规类型 | 示例 | 处理方式 |
|----------|------|----------|
| **双编号** | Def-EDGE-01-01 | 改为 Def-EDGE-01 |
| **多余层级** | Def-WASM-3.0-01 | 改为 Def-WASM-01 |
| **前缀混乱** | Def-AVX-01 (在SIMD模块) | 改为 Def-SIMD-04 |
| **类型错误** | Theorem-WASM-01 | 改为 Thm-WASM-01 |

### 7.2 修复流程

1. 发现违规编号
2. 在 THEOREM-INDEX.md 中查找映射关系
3. 使用 StrReplaceFile 批量替换
4. 验证所有引用已更新
5. 更新 THEOREM-INDEX.md

---

## 8. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-04 | 初始规范，基于 AGENTS.md |
| v2.0 | 2026-04-04 | 修复编号混乱，统一规范 |

---

## 9. 参考

- [PROJECT-AUDIT-REPORT.md](./PROJECT-AUDIT-REPORT.md) - 编号问题审计报告
- [THEOREM-INDEX.md](./THEOREM-INDEX.md) - 形式化元素全局索引
