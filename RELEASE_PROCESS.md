# 发布流程指南 (Release Process)

> **版本**: v1.0 | **最后更新**: 2026-04-12 | **状态**: 生效

---

## 版本号规范

本项目采用 [语义化版本](https://semver.org/lang/zh-CN/) 规范：

版本格式：主版本号.次版本号.修订号（MAJOR.MINOR.PATCH）

- 主版本号（MAJOR）：重大架构变更或不兼容修改
- 次版本号（MINOR）：新增功能，向后兼容
- 修订号（PATCH）：问题修复，向后兼容

示例：v3.9.0

### 版本类型

| 类型 | 格式 | 触发条件 | 示例 |
|-----|------|---------|------|
| 正式版 | v{major}.{minor}.{patch} | 功能完成且稳定 | v3.9.0 |
| 预发布版 | v{major}.{minor}.{patch}-rc.{n} | 正式版前的测试版本 | v3.9.0-rc.1 |
| 热修复 | v{major}.{minor}.{patch+1} | 紧急问题修复 | v3.9.1 |

---

## 发布准备

### 发布前检查清单

- [ ] 所有计划功能已完成并合并
- [ ] 所有 Critical 和 High 优先级 Issue 已解决
- [ ] 自动化测试全部通过
- [ ] 文档已更新至最新状态
- [ ] CHANGELOG.md 已更新
- [ ] 版本号已更新（如适用）

### 发布分支管理

发布流程：

1. 从 main 分支创建 release/v{版本号} 分支
2. 进行最终测试
3. 如发现问题则修复
4. 测试通过后合并到 main
5. 创建标签
6. 发布 Release
7. 合并回 develop 分支

---

## 发布流程

### 1. 准备阶段

#### 1.1 创建发布分支

```bash
git checkout main
git pull origin main
git checkout -b release/v{版本号}
git push -u origin release/v{版本号}
```

#### 1.2 更新版本信息

更新以下文件中的版本号：

- PROJECT-META.json 中的 version 字段
- AGENTS.md 中的版本信息
- 相关文档中的版本引用

#### 1.3 更新变更日志

在 CHANGELOG.md 中添加新版本条目。

### 2. 测试阶段

运行验证脚本：

- make validate-docs
- make check-links
- make check-theorems

手动验证：

- 核心文档结构完整性
- 交叉引用正确性
- Mermaid 图表渲染
- 外部链接有效性

### 3. 发布阶段

#### 3.1 合并发布分支

```bash
git checkout main
git pull origin main
git merge --no-ff release/v{版本号}
git push origin main
```

#### 3.2 创建标签

```bash
git tag -a v{版本号} -m "Release v{版本号}"
git push origin v{版本号}
```

#### 3.3 创建 GitHub Release

1. 访问 GitHub Releases 页面
2. 点击 Draft a new release
3. 选择刚创建的标签
4. 填写发布说明
5. 如为预发布版本，勾选 This is a pre-release
6. 点击 Publish release

### 4. 发布后

合并回开发分支并删除发布分支。

---

## 热修复流程

对于需要紧急修复的问题：

1. 从 main 分支创建 hotfix/{问题描述} 分支
2. 修复问题（保持改动最小化）
3. 合并到 main 并创建新标签
4. 合并到 develop 分支

---

## 发布周期

| 版本类型 | 周期 | 说明 |
|---------|------|------|
| PATCH | 按需 | 发现问题即修复 |
| MINOR | 每月 | 新功能累积发布 |
| MAJOR | 每季度 | 重大架构变更 |

---

## 相关文件

- CHANGELOG.md - 版本变更记录
- PROJECT-TRACKING.md - 项目进度跟踪
- MAINTAINERS.md - 维护者指南

---

## 更新记录

| 版本 | 日期 | 变更内容 |
|-----|------|---------|
| v1.0 | 2026-04-12 | 初始版本 |

---

*确保每次发布都遵循此流程，保证项目质量与稳定性。*
