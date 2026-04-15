# AnalysisDataFlow v4.2 上线检查清单

> **版本**: v4.2 | **日期**: 2026-04-15 | **状态**: 🟢 GitHub Pages + Discussions 已上线，待 Algolia DocSearch 申请
>
> 本清单用于确保所有上线准备工作已就绪。勾选项代表**已验证完成**的离线任务；未勾选项代表**必须由项目维护者在 GitHub 上手动执行**的在线任务。

---

## 1. GitHub Pages 启用步骤

### 1.1 进入仓库设置

**点击路径**: `https://github.com/AnalysisDataFlow/AnalysisDataFlow` → 顶部导航栏点击 **Settings**（齿轮图标）→ 左侧侧边栏点击 **Pages**

### 1.2 配置 Pages 源

- [x] **Build and deployment** 区域：
  - **Source** 下拉框选择 `GitHub Actions`
  - 不要选择 "Deploy from a branch"（工作流已配置为 Actions 部署）

### 1.3 验证工作流运行

- [x] 点击仓库顶部 **Actions** 标签
- [x] 在左侧工作流列表中选择 **Deploy Knowledge Graph to GitHub Pages**
- [x] 确认最近一次运行状态为 ✅ **green checkmark**
- [x] 点击进入运行详情，展开 **Deploy to GitHub Pages** 步骤，确认输出 `URL: https://adamartin18010.github.io/AnalysisDataFlow/`

### 1.4 验证站点可访问

- [x] 在浏览器访问 `https://adamartin18010.github.io/AnalysisDataFlow/`
- [x] 确认页面标题为 `AnalysisDataFlow 知识图谱 v4.2...`
- [x] 确认 3D 可视化画布加载成功（出现节点和边）
- [x] 确认搜索框可以输入并返回结果（本地搜索 fallback 已生效）
- [x] 打开浏览器开发者工具 → Network，确认没有 404 的关键 JS/CSS 资源

---

## 2. 自定义域名 DNS 配置示例

### 2.1 目标域名

当前 CNAME 文件内容：`kg.analysisdataflow.io`（见 `KNOWLEDGE-GRAPH/CNAME`）

> 注：`CNAME` 文件中当前为注释状态。如需启用自定义域名，需先取消注释并提交到 `main` 分支。

### 2.2 DNS 配置示例（Cloudflare / 通用 DNS 提供商）

| 类型 | 主机记录 | 记录值 | TTL | 说明 |
|------|---------|--------|-----|------|
| CNAME | `kg` | `analysisdataflow.github.io` | Auto | 将子域名指向 GitHub Pages 服务器 |

**配置截图文字说明（以 Cloudflare 为例）**:

1. 登录 Cloudflare Dashboard → 选择域名 `analysisdataflow.io`
2. 左侧菜单点击 **DNS** → **Records**
3. 点击橙色 **Add record** 按钮
4. **Type** 选择 `CNAME`
5. **Name** 输入 `kg`
6. **Target** 输入 `analysisdataflow.github.io`
7. **TTL** 选择 `Auto`
8. 关闭 Proxy 状态（灰色云图标，仅 DNS），因为 GitHub Pages 已有 HTTPS，开启 Orange Cloud 可能导致证书循环
9. 点击 **Save**

### 2.3 GitHub 端域名确认

- [ ] 在仓库 **Settings > Pages** 中，**Custom domain** 输入框填入 `kg.analysisdataflow.io`
- [ ] 点击 **Save**
- [ ] 等待 GitHub 自动进行 DNS 检查并生成 SSL 证书（通常 5-15 分钟）
- [ ] 确认 **Enforce HTTPS** 复选框可用并已勾选

### 2.4 验证

- [ ] 浏览器访问 `https://kg.analysisdataflow.io/`，确认无证书警告
- [ ] 确认地址栏显示 🔒 安全锁图标

---

## 3. Cloudflare CDN 配置步骤

> 若已使用 Cloudflare DNS，可进一步开启 CDN 加速（Orange Cloud）。**注意**：GitHub Pages 自带全球 CDN，Cloudflare 加速为可选增强。

### 3.1 开启 CDN 代理

- [ ] 回到 Cloudflare DNS 记录列表
- [ ] 将 `kg` 对应的 CNAME 记录Proxy 状态切换为 🟠 **Orange Cloud**（已代理）

### 3.2 SSL/TLS 模式设置

- [ ] 左侧菜单点击 **SSL/TLS** → **Overview**
- [ ] **SSL/TLS encryption mode** 选择 `Full (strict)` 或 `Full`
- [ ] 进入 **SSL/TLS > Edge Certificates**，确认 **Always Use HTTPS** 开启

### 3.3 缓存规则（可选）

- [ ] 左侧菜单 **Caching** → **Configuration**
- [ ] **Browser Cache TTL** 设置为 `4 hours`（静态 JS/CSS 缓存）
- [ ] **Always Online** 可开启，为静态页面提供降级访问

### 3.4 性能优化（可选）

- [ ] 左侧菜单 **Speed** → **Optimization**
- [ ] 开启 **Auto Minify**（CSS、JS、HTML）
- [ ] 开启 **Brotli** 压缩

---

## 4. Algolia DocSearch 申请状态跟踪表

### 4.1 申请步骤

1. 访问 [https://docsearch.algolia.com/apply/](https://docsearch.algolia.com/apply/)
2. 填写申请表单：
   - **Email**: 项目维护者邮箱
   - **URL**: `https://adamartin18010.github.io/AnalysisDataFlow/`
   - **Repository URL**: `https://github.com/AdaMartin18010/AnalysisDataFlow`
   - **Owner of the website?** Yes
   - **Tech Stack**: React + static HTML (GitHub Pages)
3. 提交后等待 Algolia 团队邮件回复（通常 3-7 个工作日）

### 4.2 状态跟踪

| 步骤 | 状态 | 预计时间 | 备注 |
|------|------|---------|------|
| 提交申请 | ⬜ 待执行 | — | 由维护者手动提交 |
| 收到确认邮件 | ⬜ 待确认 | T+1~2d | 确认网站所有权 |
| 收到 API Key | ⬜ 待确认 | T+3~7d | 包含 `appId`, `apiKey`, `indexName` |
| 集成到 index.html | ✅ 就绪 | 收到后 1h | 搜索组件代码已预留配置位置 |
| 首次索引完成 | ⬜ 待验证 | 集成后 24h | 在站点测试搜索 |

### 4.3 预配置完成项

- ✅ `KNOWLEDGE-GRAPH/index.html` — DocSearch 前端组件已集成（含本地搜索 fallback）
- ✅ `.github/workflows/deploy-knowledge-graph.yml` — 部署工作流已配置 `workflow_dispatch`
- ✅ `KNOWLEDGE-GRAPH/sitemap-full.xml` — 1,531 URL 已生成，供 Algolia 爬虫使用

### 4.3 回退方案

若 Algolia 审批周期过长或被拒：

- 站点已内置本地搜索功能（基于概念嵌入和标签过滤），无需外部服务即可使用。
- 可在 `KNOWLEDGE-GRAPH/index.html` 中继续完善本地搜索的词汇表和词干匹配逻辑。

---

## 5. 首次上线后的验证测试清单

### 5.1 功能验证

| # | 检查项 | 验证方法 | 状态 |
|---|--------|---------|------|
| 1 | 首页正常加载 | 访问根 URL，3D 图渲染 | ⬜ |
| 2 | 搜索框可用 | 输入 "Flink"，返回相关节点 | ⬜ |
| 3 | 节点详情面板 | 点击任意节点，右侧显示详情 | ⬜ |
| 4 | 视图切换（2D/3D） | 点击 2D/3D 按钮，场景切换 | ⬜ |
| 5 | 分类过滤 | 勾选/取消分类，节点正确显示/隐藏 | ⬜ |
| 6 | 统计面板 | 确认节点数、边数、连通分量统计正确 | ⬜ |
| 7 | 404 页面 | 访问不存在路径 `/not-found`，显示 404.html | ⬜ |

### 5.2 SEO 验证

| # | 检查项 | 验证方法 | 状态 |
|---|--------|---------|------|
| 8 | 标题唯一且准确 | 查看 `<title>` 标签 | ⬜ |
| 9 | Meta description 存在 | 查看页面源码 `<meta name="description">` | ⬜ |
| 10 | Open Graph 标签完整 | 使用 [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) | ⬜ |
| 11 | Twitter Card 标签完整 | 使用 [Twitter Card Validator](https://cards-dev.twitter.com/validator) | ⬜ |
| 12 | Schema.org 结构化数据 | 使用 [Google Rich Results Test](https://search.google.com/test/rich-results) | ⬜ |
| 13 | robots.txt 可访问 | 访问 `/robots.txt` | ⬜ |
| 14 | sitemap.xml 可访问 | 访问 `/sitemap.xml` | ⬜ |

### 5.3 性能验证

| # | 检查项 | 验证方法 | 目标值 | 状态 |
|---|--------|---------|--------|------|
| 15 | Lighthouse Performance | Chrome DevTools → Lighthouse | ≥ 90 | ⬜ |
| 16 | First Contentful Paint (FCP) | Chrome DevTools → Performance | < 1.8s | ⬜ |
| 17 | Largest Contentful Paint (LCP) | Chrome DevTools → Performance | < 2.5s | ⬜ |
| 18 | JS 资源加载 | Network 面板 | 无阻塞 render | ⬜ |

### 5.4 安全验证

| # | 检查项 | 验证方法 | 状态 |
|---|--------|---------|------|
| 19 | HTTPS 强制 | 访问 `http://...`，确认 301/307 到 HTTPS | ⬜ |
| 20 | 无混合内容警告 | DevTools Console 无 Mixed Content 报错 | ⬜ |
| 21 | CSP / X-Frame 响应头 | Network 面板查看响应头（GitHub Pages 默认提供） | ⬜ |

---

## 6. 紧急回退检查项

若上线后发现问题，按以下顺序回退：

1. **关闭 GitHub Pages**：Settings > Pages → Source 改为 `None`（立即停止公开访问）
2. **回退工作流**：在 Actions 页面取消最近的部署运行
3. **恢复默认域名**：删除/注释 `KNOWLEDGE-GRAPH/CNAME` 中的自定义域名，保留 `github.io` 域名
4. **本地搜索兜底**：Algolia 未就绪时不影响核心搜索功能

---

*AnalysisDataFlow Go-Live Checklist v4.2*
