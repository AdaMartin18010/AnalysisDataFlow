# Phase 2 自动化工具链

> **Automation Toolchain for Stream Processing**

## 概述

本目录包含20个自动化工具，支持开发、测试、部署和运维全流程。

## 工具分类

### 代码质量 (7个)

- 链接检查器
- 交叉引用检查
- 定理编号检查
- Mermaid渲染器
- 文档生成器
- 依赖检查器
- 安全扫描器

### CI/CD (5个)

- 性能基准测试
- 文档质量检查
- 发布自动化
- 备份自动化
- 通知工具

### 开发工具 (8个)

- 性能分析器
- 测试运行器
- 部署助手
- 配置验证
- 代码格式化
- Linter配置

## 使用方法

### 本地运行

```bash
python link_checker.py .
python theorem-checker/check_theorems.py .
```

### CI/CD集成

所有工具已集成到 GitHub Actions 工作流。

---

*Phase 2 - Automation Toolchain*
