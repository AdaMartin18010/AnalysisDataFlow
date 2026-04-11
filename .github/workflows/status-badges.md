# CI/CD 状态徽章配置

## 徽章代码

### 基本徽章

```markdown
<!-- Quality Gate -->
![Quality Gate](https://github.com/OWNER/REPO/workflows/Quality%20Gate/badge.svg)

<!-- Nightly Check -->
![Nightly Check](https://github.com/OWNER/REPO/workflows/Nightly%20Check/badge.svg)

<!-- Release -->
![Release](https://github.com/OWNER/REPO/workflows/Release%20Automation/badge.svg)

<!-- Formal Verification -->
![Formal Verification](https://github.com/OWNER/REPO/workflows/Formal%20Verification/badge.svg)
```

### 带链接的徽章

```markdown
[![Quality Gate](https://github.com/OWNER/REPO/workflows/Quality%20Gate/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/quality-gate.yml)
```

### 带样式的徽章 (shields.io)

```markdown
<!-- 自定义样式 -->
![Quality Gate](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/quality-gate.yml?branch=main&label=Quality%20Gate&logo=github&style=flat-square)

<!-- 带颜色的状态徽章 -->
![Build Status](https://img.shields.io/github/workflow/status/OWNER/REPO/Quality%20Gate/main?label=build&color=brightgreen)
```

---

## 完整徽章集合

### README.md 顶部徽章

```markdown
<!-- 主状态徽章行 -->
[![Quality Gate](https://github.com/OWNER/REPO/workflows/Quality%20Gate/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/quality-gate.yml)
[![Nightly Check](https://github.com/OWNER/REPO/workflows/Nightly%20Check/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/nightly-check.yml)
[![Release](https://github.com/OWNER/REPO/workflows/Release%20Automation/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/release-automation.yml)

<!-- 形式化验证徽章 -->
[![Coq](https://img.shields.io/badge/Coq-8.17.1-blue.svg)](https://coq.inria.fr/)
[![TLA+](https://img.shields.io/badge/TLA%2B-Verified-green.svg)](https://lamport.azurewebsites.net/tla/tla.html)

<!-- 项目统计徽章 -->
![Documents](https://img.shields.io/badge/Documents-250+-blue.svg)
![Theorems](https://img.shields.io/badge/Theorems-2000+-purple.svg)
![Definitions](https://img.shields.io/badge/Definitions-4500+-orange.svg)
```

---

## 工作流特定的徽章URL

| 工作流 | 徽章URL |
|--------|---------|
| Quality Gate | `https://github.com/OWNER/REPO/workflows/Quality%20Gate/badge.svg` |
| Nightly Check | `https://github.com/OWNER/REPO/workflows/Nightly%20Check/badge.svg` |
| Release Automation | `https://github.com/OWNER/REPO/workflows/Release%20Automation/badge.svg` |
| Formal Verification | `https://github.com/OWNER/REPO/workflows/Formal%20Verification/badge.svg` |
| Dependency Update | `https://github.com/OWNER/REPO/workflows/Dependency%20Update/badge.svg` |

---

## 高级徽章配置

### 按分支的徽章

```markdown
<!-- main分支 -->
![Quality Gate Main](https://github.com/OWNER/REPO/workflows/Quality%20Gate/badge.svg?branch=main)

<!-- develop分支 -->
![Quality Gate Develop](https://github.com/OWNER/REPO/workflows/Quality%20Gate/badge.svg?branch=develop)
```

### 按事件的徽章

```markdown
<!-- 只在push事件时显示 -->
![Quality Gate Push](https://github.com/OWNER/REPO/workflows/Quality%20Gate/badge.svg?event=push)
```

---

## 使用说明

1. **替换占位符**:
   - `OWNER` - GitHub用户名或组织名
   - `REPO` - 仓库名

2. **添加到README**:

   ```bash
   # 在README.md顶部添加徽章
   cat status-badges.md >> README.md
   ```

3. **验证徽章**:
   - 提交后等待几分钟让GitHub生成徽章
   - 检查徽章是否正确显示

---

*配置文件版本: v1.0*
