# USTM Coq Formalization

Coq形式化实现 for USTM-F阶段五。

## 结构

- `theories/`: 核心形式化理论
  - `Utils/`: 工具库
  - `Foundation/`: 基础定义
  - `Models/`: 计算模型(Actor, CSP, Dataflow)
  - `Encodings/`: 编码理论
  - `Hierarchy/`: 层次理论
  - `Theorems/`: 主要定理证明

## 编译

```bash
make
```

## 依赖

- Coq 8.17+
- MathComp 2.0+ (可选)

## 文档对应

见04.05-coq-formalization.md
