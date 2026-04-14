# GitHub Discussions 配置指南

> **版本**: v4.2 | **最后更新**: 2026-04-14
>
> 本指南说明如何为 AnalysisDataFlow 项目配置 GitHub Discussions，以建立有序、高效的社区交流环境。
> 详细部署背景请参考 [ECOSYSTEM-DEPLOYMENT-PLAN-v4.2.md](../ECOSYSTEM-DEPLOYMENT-PLAN-v4.2.md) 第 3.1 节。

---

## 1. 快速启用步骤

1. 进入仓库 **Settings > Features**。
2. 找到 **Discussions** 开关并启用。
3. 点击顶部导航栏的 **Discussions**。
4. 在右侧点击 **Manage categories** 进入分类管理界面。

---

## 2. 推荐分类配置

建议创建以下 5 个分类：

| 分类 | Emoji | 用途 | 颜色 | Discussion Format |
|------|-------|------|------|-------------------|
| **Announcements** | 📢 | 项目公告、版本发布、里程碑更新 | `#d73a4a` | Announcement（仅维护者可发布） |
| **General** | 💡 | 一般性讨论、提问与想法交流 | `#0075ca` | Open-ended discussion |
| **Learning** | 🎓 | 学习路径、教程讨论与知识问答 | `#a2eeef` | Question and Answer（可标记最佳答案） |
| **Show and Tell** | 🏗️ | 社区贡献展示、项目案例与学习成果分享 | `#7057ff` | Open-ended discussion |
| **Q&A** | 🐛 | 技术问答、故障排查与最佳实践咨询 | `#cfd3d7` | Question and Answer |

创建时的推荐字段填写：

- **Announcements**: Title=`Announcements`, Description=`版本发布、重要公告与里程碑更新`, Format=`Announcement`, Color=`#d73a4a`
- **General**: Title=`General`, Description=`一般性讨论、提问与想法交流`, Format=`Open-ended discussion`, Color=`#0075ca`
- **Learning**: Title=`Learning`, Description=`学习路径、教程讨论与知识问答`, Format=`Question and Answer`, Color=`#a2eeef`
- **Show and Tell**: Title=`Show and Tell`, Description=`社区贡献展示、项目案例与学习成果分享`, Format=`Open-ended discussion`, Color=`#7057ff`
- **Q&A**: Title=`Q&A`, Description=`技术问答、故障排查与最佳实践咨询`, Format=`Question and Answer`, Color=`#cfd3d7`

---

## 3. 标签体系

建议在 Discussion 与 Issue 中统一使用以下标签，便于内容检索与分发：

| 标签 | 用途 |
|------|------|
| `announcement` | 官方公告 |
| `question` | 提问 |
| `learning` | 学习相关 |
| `showcase` | 案例展示 |
| `help wanted` | 需要社区帮助 |
| `bug` | 疑似错误 |
| `content-request` | 内容补充请求 |
| `good first issue` | 新手友好 |
| `discussion` | 需要进一步讨论 |

---

## 4. 版主职责

版主（Maintainer）负责维护 Discussion 的健康运转，主要职责包括：

1. **内容审核** — 定期检查新帖，确保帖子发布在正确的分类下。
2. **标签管理** — 为讨论帖添加或修正标签，便于检索。
3. **问题引导** — 对未获得回答的提问进行补充说明或 @ 相关专家。
4. **氛围维护** — 及时处理不友善言论，确保社区包容、尊重。
5. **信息同步** — 将高频问题整理为 FAQ 或文档改进项。

---

## 5. 置顶规则

为了提升重要信息的可见性，建议采用以下置顶策略：

| 置顶类型 | 数量上限 | 内容示例 | 置顶时长 |
|---------|---------|---------|---------|
| **官方公告** | 1 条 | 版本发布、重大更新 | 长期，直至下一版本发布 |
| **新手必读** | 1 条 | 欢迎指南、行为准则链接 | 长期 |
| **活动/征集** | 1 条 | 月度分享会、案例征集 | 活动期间 |
| **热门问答** | 1 条 | 高频技术问题的精华帖 | 每月轮换 |

> **注意**: GitHub Discussions 默认最多同时置顶 3 条帖子，请根据当前阶段优先级动态调整。

---

## 6. 配置检查清单

- [ ] Discussions 功能已在仓库设置中启用
- [ ] 已创建上述 5 个分类，格式与颜色配置正确
- [ ] 标签体系已同步到 Issue / Discussion 标签库
- [ ] 版主团队已明确分工
- [ ] 置顶规则已在团队内部达成共识
- [ ] 首条置顶帖（欢迎指南）已发布

---

*AnalysisDataFlow Community Team*
