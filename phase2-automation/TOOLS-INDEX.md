# Phase 2 自动化工具索引

> **文档类型**: 自动化工具汇总
> **语言**: 中英文
> **状态**: Phase 2 - 完整版

---

## 自动化工具清单

### 代码质量工具 (Code Quality)

| 编号 | 工具名称 | 文件 | 功能 |
|------|----------|------|------|
| T-01 | 链接检查器 | link_checker.py | 检查文档链接有效性 |
| T-02 | 交叉引用检查 | cross-ref-checker/ | 验证文档交叉引用 |
| T-03 | 定理编号检查 | theorem-checker/ | 验证定理编号一致性 |
| T-04 | Mermaid渲染器 | mermaid-renderer/ | 渲染Mermaid图表 |
| T-05 | 文档生成器 | doc-generator/ | 自动生成文档 |
| T-06 | 依赖检查器 | dependency-checker/ | 检查项目依赖 |
| T-07 | 安全扫描器 | security-scanner/ | 安全漏洞扫描 |

### CI/CD工具 (CI/CD)

| 编号 | 工具名称 | 文件 | 功能 |
|------|----------|------|------|
| T-08 | 性能基准测试 | performance-benchmark.yml | 自动化性能测试 |
| T-09 | 文档质量检查 | documentation-check.yml | 文档质量门禁 |
| T-10 | 发布自动化 | release-automation/ | 自动化发布流程 |
| T-11 | 备份自动化 | backup-automation/ | 自动备份任务 |
| T-12 | 通知工具 | notifier/ | 构建通知 |

### 开发工具 (Development)

| 编号 | 工具名称 | 文件 | 功能 |
|------|----------|------|------|
| T-13 | 性能分析器 | performance-profiler/ | 性能分析 |
| T-14 | 测试运行器 | test-runner/ | 自动化测试 |
| T-15 | 部署助手 | deploy-helper/ | 部署辅助 |
| T-16 | 配置验证 | config-validator/ | 配置验证 |
| T-17 | 代码格式化 | code-formatter/ | 代码格式化 |

---

## 使用指南

### 本地运行

```bash
# 链接检查
python phase2-automation/link_checker.py .

# 定理检查
python phase2-automation/theorem-checker/check_theorems.py .

# 交叉引用检查
python phase2-automation/cross-ref-checker/check_refs.py .
```

### CI/CD集成

所有工具已集成到GitHub Actions工作流中。

---

*Phase 2 - 自动化工具完整索引 (17个工具)*
