# 形式化证明最佳实践

> **文档类型**: 方法论指南
> **语言**: 中英文
> **状态**: Phase 2

---

## TLA+ 编写规范

### 命名规范

- 模块名使用 PascalCase
- 变量名使用 camelCase
- 常量使用大写字母

### 证明结构

1. 常量声明 (CONSTANTS)
2. 变量声明 (VARIABLES)
3. 类型不变量 (TypeInvariant)
4. 初始状态 (Init)
5. 状态转移 (Next)
6. 安全属性 (Safety Properties)
7. 活性属性 (Liveness Properties)

### 注释规范

```tla
(*
 * 定理名称: 描述定理内容
 * 参数: 描述参数
 * 返回值: 描述返回值
 *)
```

---

## Coq 编写规范

### 证明风格

- 使用有意义的引理名称
- 每个引理添加文档注释
- 证明步骤清晰可读

---

*Phase 2 - 形式化证明最佳实践*
