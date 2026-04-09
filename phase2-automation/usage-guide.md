# 自动化工具使用指南

## 快速开始

### 链接检查器

```bash
cd phase2-automation
python link_checker.py ../docs
```

### 定理检查器

```bash
python theorem-checker/check_theorems.py ../phase2-formal-proofs
```

### 交叉引用检查

```bash
python cross-ref-checker/check_refs.py ..
```

## CI/CD 使用

### 本地测试

```bash
# 运行所有检查
make check

# 运行特定检查
make check-links
make check-theorems
```

### GitHub Actions

所有工具已集成到 `.github/workflows/`

## 添加新工具

1. 在 `phase2-automation/` 创建目录
2. 编写工具脚本
3. 添加 CI/CD 配置
4. 更新文档

---

*Usage Guide*
