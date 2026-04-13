# AnalysisDataFlow 社区运营设置指南

> **版本**: v4.2 | **最后更新**: 2026-04-13

---

## 1. GitHub Discussions 分类配置

### 1.1 启用 Discussions（文字截图说明）

**步骤 1 — 进入仓库设置页面**

- 打开浏览器，访问 `https://github.com/AnalysisDataFlow/AnalysisDataFlow`
- 在页面顶部导航栏找到并点击 **Settings**（齿轮图标）
- 左侧边栏向下滚动，找到 **Features** 区域
- *文字截图说明*：此时页面右侧应显示 "Features" 标题，下方有 Issues、Discussions、Projects 等开关项，每个开关右侧有蓝色/灰色的 Toggle 按钮

**步骤 2 — 开启 Discussions**

- 在 Features 区域找到 **Discussions** 一行
- 点击右侧的 Toggle 开关，使其变为蓝色（启用状态）
- 页面会自动刷新，顶部导航栏出现 **Discussions** 标签页
- *文字截图说明*：刷新后页面顶部导航栏从左到右依次为 Code、Issues、Pull requests、**Discussions**、Actions、Projects，Discussions 为新增标签

**步骤 3 — 进入 Discussions 设置**

- 点击顶部导航栏的 **Discussions**
- 进入 Discussions 首页后，页面右侧有一个灰色按钮 **Manage categories**
- 点击 **Manage categories** 进入分类管理界面
- *文字截图说明*：Manage categories 按钮位于页面右侧 "About" 信息框下方，点击后页面标题变为 "Categories"，列表中默认只有 "General" 一个分类

### 1.2 创建分类（文字截图说明）

**步骤 4 — 新建 Announcements 分类**

- 在 Categories 页面点击绿色按钮 **New category**
- 弹出 "Create category" 对话框：
  - **Title** 输入框：输入 `Announcements`
  - **Description** 输入框：输入 `版本发布、重要公告与里程碑更新`
  - **Discussion Format** 单选：选择 `Announcement`（仅维护者可发布，其他人只能评论）
  - **Color** 选择器：输入 `#d73a4a` 或点击红色色块
- 点击对话框底部 **Create category** 按钮
- *文字截图说明*：对话框为模态浮层，居中显示，顶部标题为 "Create category"，底部有两个按钮：灰色 Cancel 和蓝色 Create category

**步骤 5 — 新建 General 分类**

- 再次点击 **New category**
- 填写：
  - **Title**: `General`
  - **Description**: `一般性讨论、提问与想法交流`
  - **Discussion Format**: `Open-ended discussion`（任何人可发起）
  - **Color**: `#0075ca`（蓝色）
- 点击 **Create category**

**步骤 6 — 新建 Learning 分类**

- 点击 **New category**
- 填写：
  - **Title**: `Learning`
  - **Description**: `学习路径、教程讨论与知识问答`
  - **Discussion Format**: `Question and Answer`（可标记最佳答案）
  - **Color**: `#a2eeef`（青色）
- 点击 **Create category**

**步骤 7 — 新建 Show and Tell 分类**

- 点击 **New category**
- 填写：
  - **Title**: `Show and Tell`
  - **Description**: `社区贡献展示、项目案例与学习成果分享`
  - **Discussion Format**: `Open-ended discussion`
  - **Color**: `#7057ff`（紫色）
- 点击 **Create category**

**步骤 8 — 新建 Q&A 分类**

- 点击 **New category**
- 填写：
  - **Title**: `Q&A`
  - **Description**: `技术问答、故障排查与最佳实践咨询`
  - **Discussion Format**: `Question and Answer`
  - **Color**: `#cfd3d7`（灰色）
- 点击 **Create category**

**步骤 9 — 验证分类列表**

- 创建完成后，Categories 页面应显示 6 个分类（含默认的 General）
- *文字截图说明*：页面中央为分类卡片列表，每张卡片左侧有一个彩色圆点，右侧显示分类名称、描述和讨论格式图标

### 1.3 分类清单汇总

| 分类名称 | Emoji | 用途 | 颜色 | Discussion Format |
|---------|-------|------|------|-------------------|
| Announcements | 📢 | 版本发布、重要公告 | #d73a4a | Announcement |
| General | 💡 | 一般性讨论、提问 | #0075ca | Open-ended discussion |
| Learning | 🎓 | 学习路径、教程讨论 | #a2eeef | Question and Answer |
| Show and Tell | 🏗️ | 社区贡献展示 | #7057ff | Open-ended discussion |
| Q&A | 🐛 | 技术问答、故障排查 | #cfd3d7 | Question and Answer |

### 1.4 标签体系

建议配置的标签：

- `question` - 提问
- `bug` - 疑似错误
- `content-request` - 内容补充请求
- `good first issue` - 新手友好
- `help wanted` - 需要社区帮助
- `discussion` - 需要进一步讨论
- `showcase` - 案例展示

---

## 2. Issue 模板优化

检查 `.github/ISSUE_TEMPLATE/` 目录，建议确保包含以下模板：

### 2.1 必备模板

1. **bug_report.md** - 缺陷报告
2. **feature_request.md** - 功能请求
3. **content_request.md** - 内容补充请求（新增）
4. **bug_report-zh.md** - 中文缺陷报告（新增）
5. **feature_request-zh.md** - 中文功能请求（新增）

### 2.2 Pull Request 模板

检查 `.github/PULL_REQUEST_TEMPLATE.md` 是否包含：

- 变更摘要
- 影响范围
- 检查清单（六段式合规、引用规范、Mermaid 验证）
- 关联 Issue

---

## 3. 贡献者流程

### 3.1 新贡献者引导路径

```
README.md → COMMUNITY/welcome-guide.md → docs/contributing/CONTRIBUTING.md
    ↓
选择贡献方向 → 阅读对应模板 → 提交 Issue/PR
```

### 3.2 贡献奖励机制

- 每月在 Discussion 中发布 "月度贡献者" 表彰
- 对优质 PR 给予 `contributor` 标签和感谢信
- 重大贡献者邀请加入项目维护者团队

---

## 4. 月度社区更新机制

### 4.1 更新内容

每月第一个周一发布，包含：

- 新增文档统计
- 本月合并的优质 PR 列表
- 下月内容规划预告
- 社区问答精选
- 寻求帮助的事项

### 4.2 发布渠道

- GitHub Discussions > Announcements
- 项目 README 顶部横幅（可选，更新后移除）

---

## 5. 社区行为准则

建议在仓库根目录创建 `CODE_OF_CONDUCT.md`，核心原则：

1. **尊重与包容** — 欢迎不同背景的参与者
2. **建设性反馈** — 批评内容而非个人
3. **耐心与帮助** — 对新问题保持耐心
4. **诚信与透明** — 注明引用来源，避免抄袭

---

*AnalysisDataFlow Community Setup Guide v4.2*
