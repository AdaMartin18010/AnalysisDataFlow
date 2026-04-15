# v4.2 管理员 5 分钟快速激活指南

> **目标**: 完成最后 3 项 GitHub 平台手动配置，让项目从"自动化就绪"变为"完全上线"  
> **预计耗时**: 5 分钟（不含 Algolia 审核等待时间）  
> **最后更新**: 2026-04-15 23:45

---

## 当前状态 ✅

| 任务 | 状态 | 说明 |
|------|------|------|
| GitHub Pages 启用 | ✅ 已完成 | Source = GitHub Actions，首次部署成功 |
| GitHub Discussions 开启 | ✅ 已完成 | 中文讨论模板已生效 |
| Algolia DocSearch 申请 | ⏳ 待手动 | 唯一剩余项，详见下方 |

> **备注**: 为启用 GitHub Pages（免费计划仅支持 Public 仓库），仓库已自动从 Private 切换为 Public。若需保持私有，请升级 GitHub Pro 计划。

---

## 已验证的线上资产

- 🌐 **站点**: `https://adamartin18010.github.io/AnalysisDataFlow/`
- 🔍 **Sitemap**: `https://adamartin18010.github.io/AnalysisDataFlow/sitemap.xml`
- 🤖 **robots.txt**: `https://adamartin18010.github.io/AnalysisDataFlow/robots.txt`
- 💬 **Discussions**: `https://github.com/AdaMartin18010/AnalysisDataFlow/discussions`
- ⚙️ **Actions**: `https://github.com/AdaMartin18010/AnalysisDataFlow/actions/workflows/deploy-knowledge-graph.yml`

---

## 唯一待执行：Algolia DocSearch 申请（2 分钟）

1. 访问 [https://docsearch.algolia.com/apply/](https://docsearch.algolia.com/apply/)
2. 填写表单：
   - **Email**: 你的邮箱
   - **Repository URL**: `https://github.com/AdaMartin18010/AnalysisDataFlow`
   - **Website URL**: `https://adamartin18010.github.io/AnalysisDataFlow/`
   - **Project Name**: `AnalysisDataFlow`
   - **Description**: "A comprehensive knowledge base for stream processing theory, formal methods, and Apache Flink ecosystem."
   - **Is your project open source?**: ✅ Yes
3. 点击提交
4. 等待 Algolia 邮件（通常 3-5 个工作日）
5. 收到 `appId`/`apiKey` 后，更新 `KNOWLEDGE-GRAPH/index.html` 中的 `ALGOLIA_CONFIG` 并重新部署

> 💡 即使 Algolia 未批复，站点也已内置本地搜索 fallback，不影响核心功能。

---

## 快速验证命令（可选）

```powershell
# 验证首页
Invoke-RestMethod -Uri 'https://adamartin18010.github.io/AnalysisDataFlow/' -UseBasicParsing | Select-Object -First 1

# 验证 sitemap
Invoke-RestMethod -Uri 'https://adamartin18010.github.io/AnalysisDataFlow/sitemap.xml' -UseBasicParsing | Select-Object -First 1

# 验证 robots.txt
Invoke-RestMethod -Uri 'https://adamartin18010.github.io/AnalysisDataFlow/robots.txt' -UseBasicParsing
```

---

## 遇到问题？

详见完整手册：
- [`v4.2-ADMIN-OPERATION-GUIDE.md`](./v4.2-ADMIN-OPERATION-GUIDE.md) — 详细操作步骤与 FAQ
- [`GO-LIVE-CHECKLIST-v4.2.md`](./GO-LIVE-CHECKLIST-v4.2.md) — 上线后验证清单
- [`ALGOLIA-DOCSEARCH-APPLICATION.md`](./ALGOLIA-DOCSEARCH-APPLICATION.md) — 预填充申请模板

---

*生成时间: 2026-04-15 | 状态: 待 1 项手动申请*
