# 知识图谱 v2.0 部署指南

> **版本**: v2.0.0 | **更新日期**: 2026-04-12 | **状态**: 生产就绪

## 📋 部署概述

本指南详细说明如何将 AnalysisDataFlow 知识图谱 v2.0 部署到可访问的在线环境。

### 部署目标

- **GitHub Pages**: 主部署目标，免费且与代码库集成
- **Cloudflare Pages**: 备选方案，提供全球 CDN 加速
- **自定义域名**: 可选，通过 Cloudflare 配置

### 预期访问地址

| 环境 | URL |
|------|-----|
| GitHub Pages | `https://<username>.github.io/AnalysisDataFlow/knowledge-graph/` |
| Cloudflare Pages | `https://analysisdataflow.pages.dev` |
| 自定义域名 | `https://kg.analysisdataflow.com` (示例) |

---

## 🚀 快速部署（GitHub Pages）

### 前置条件

1. GitHub 账号
2. 仓库已推送到 GitHub
3. 已启用 GitHub Pages (Settings → Pages)

### 自动部署流程

项目已配置 GitHub Actions，推送代码后自动部署：

```yaml
# 触发条件
on:
  push:
    branches: [main, master]
    paths:
      - 'knowledge-graph-v4.html'
      - '.scripts/kg-v2/**'
      - '.github/workflows/deploy-kg.yml'
```

### 手动触发部署

1. 进入仓库 **Actions** 标签
2. 选择 **Deploy Knowledge Graph v2.0** 工作流
3. 点击 **Run workflow**
4. 选择部署目标 (`gh-pages` 或 `staging`)

### 验证部署

部署完成后，访问以下地址验证：

```
https://<username>.github.io/AnalysisDataFlow/knowledge-graph/
```

---

## 🔧 生产构建步骤

### 1. 生成静态数据

```bash
# 生成图谱数据
python .scripts/kg-v2/generate-static-data.py

# 生成搜索索引
python .scripts/kg-v2/generate-search-index.py

# 生成学习路径
python .scripts/kg-v2/generate-learning-paths.py
```

### 2. 资源优化

```bash
# 运行资源优化器
python .scripts/kg-v2/optimize-assets.py
```

优化内容包括：

- JSON 文件 gzip 压缩 (节省 ~70% 体积)
- 生成 Service Worker 实现离线访问
- 生成 Web App Manifest
- 创建 404 页面

### 3. 输出目录结构

```
knowledge-graph-site/
├── index.html              # 主页面
├── 404.html               # 错误页面
├── service-worker.js      # Service Worker
├── manifest.json          # PWA Manifest
├── .nojekyll              # 禁用 Jekyll 处理
├── load-optimizer.js      # 资源预加载优化
└── data/
    ├── graph-data.json         # 图谱数据
    ├── graph-data.json.gz      # 压缩版本
    ├── metadata.json           # 元数据
    ├── search-index.json       # 搜索索引
    ├── search-suggestions.json # 搜索建议
    ├── learning-paths.json     # 学习路径
    ├── skill-tree.json         # 技能树
    └── chunks/                 # 分块数据
        ├── struct.json
        ├── knowledge.json
        ├── flink.json
        └── ...
```

---

## 🌐 Cloudflare CDN 配置

### 方案 A: Cloudflare Pages（推荐）

#### 1. 创建 Cloudflare Pages 项目

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 导航至 **Pages** → **Create a project**
3. 选择 **Connect to Git**
4. 授权 GitHub 并选择 `AnalysisDataFlow` 仓库

#### 2. 构建设置

```yaml
# Build settings
Build command: python .scripts/kg-v2/generate-static-data.py && python .scripts/kg-v2/optimize-assets.py
Build output directory: knowledge-graph-site
Root directory: /
```

#### 3. 环境变量

```bash
PYTHON_VERSION=3.11
NODE_VERSION=20
```

#### 4. 部署预览

每次 PR 自动创建预览链接：

```
https://<branch-name>.analysisdataflow.pages.dev
```

### 方案 B: Cloudflare CDN (GitHub Pages 加速)

#### 1. 添加域名到 Cloudflare

1. 注册 Cloudflare 账号
2. 添加域名 (如 `analysisdataflow.com`)
3. 按照指引修改域名服务器

#### 2. 配置 DNS

```
Type: CNAME
Name: kg
Target: <username>.github.io
Proxy status: Proxied (橙色云)
TTL: Auto
```

#### 3. 启用 HTTPS

1. **SSL/TLS** → **Overview**
2. 选择 **Full (strict)** 模式
3. 启用 **Always Use HTTPS**

#### 4. 缓存优化配置

**页面规则** (Page Rules)：

```
URL: kg.analysisdataflow.com/data/*
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 7 days
  - Browser Cache TTL: 1 day
```

```
URL: kg.analysisdataflow.com/*.json
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 day
```

#### 5. 性能优化

**Speed** → **Optimization**：

- Auto Minify: 启用 HTML, CSS, JS
- Brotli: 启用
- Early Hints: 启用
- HTTP/2: 启用
- HTTP/3 (QUIC): 启用

---

## 🔍 Algolia 搜索集成

### 1. 创建 Algolia 账号

1. 访问 [Algolia](https://www.algolia.com) 注册账号
2. 创建新应用 (Application)
3. 记录以下凭证：
   - Application ID
   - Search-Only API Key
   - Admin API Key

### 2. 配置索引

**创建索引**: `analysisdataflow_kg`

**索引配置**:

```json
{
  "searchableAttributes": [
    "name",
    "description",
    "category",
    "tags"
  ],
  "attributesForFaceting": [
    "category",
    "type"
  ],
  "ranking": [
    "typo",
    "geo",
    "words",
    "filters",
    "proximity",
    "attribute",
    "exact",
    "custom"
  ]
}
```

### 3. 数据推送脚本

创建 `.scripts/kg-v2/push-to-algolia.py`：

```python
#!/usr/bin/env python3
"""推送搜索数据到 Algolia"""

from algoliasearch.search_client import SearchClient
import json
from pathlib import Path

# 配置
APP_ID = "YOUR_APP_ID"
ADMIN_KEY = "YOUR_ADMIN_API_KEY"
INDEX_NAME = "analysisdataflow_kg"

# 初始化客户端
client = SearchClient.create(APP_ID, ADMIN_KEY)
index = client.init_index(INDEX_NAME)

# 读取本地搜索索引
with open("knowledge-graph-site/data/search-index.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

# 添加对象ID（必需）
for i, doc in enumerate(documents):
    doc["objectID"] = f"doc_{i}"

# 批量上传
index.save_objects(documents)
print(f"✅ 已上传 {len(documents)} 条记录到 Algolia")

# 配置索引设置
index.set_settings({
    "searchableAttributes": ["name", "description", "content"],
    "attributesForFaceting": ["category"],
    "highlightPreTag": "<mark>",
    "highlightPostTag": "</mark>"
})
```

### 4. 前端集成

在 `knowledge-graph-site/index.html` 中添加：

```html
<!-- Algolia InstantSearch.js -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/instantsearch.css@7/themes/algolia-min.css">
<script src="https://cdn.jsdelivr.net/npm/algoliasearch@4/dist/algoliasearch-lite.umd.js"></script>
<script src="https://cdn.jsdelivr.net/npm/instantsearch.js@4"></script>

<script>
// 初始化 Algolia 搜索
const searchClient = algoliasearch('YOUR_APP_ID', 'YOUR_SEARCH_KEY');
const search = instantsearch({
    indexName: 'analysisdataflow_kg',
    searchClient,
});

// 添加搜索框
search.addWidget(
    instantsearch.widgets.searchBox({
        container: '#search-box',
        placeholder: '搜索知识图谱...',
    })
);

// 添加结果展示
search.addWidget(
    instantsearch.widgets.hits({
        container: '#search-results',
        templates: {
            item: (hit) => `
                <div class="hit-item">
                    <h3>${hit.name}</h3>
                    <p>${hit.description}</p>
                    <span class="category">${hit.category}</span>
                </div>
            `
        }
    })
);

search.start();
</script>
```

### 5. GitHub Actions 自动同步

添加工作流步骤：

```yaml
- name: Push to Algolia
  env:
    ALGOLIA_APP_ID: ${{ secrets.ALGOLIA_APP_ID }}
    ALGOLIA_ADMIN_KEY: ${{ secrets.ALGOLIA_ADMIN_KEY }}
  run: python .scripts/kg-v2/push-to-algolia.py
```

---

## 📦 部署准备包清单

### GitHub Actions Workflow

文件：`.github/workflows/deploy-kg.yml` ✅ 已配置

### 必要的环境变量

| 变量名 | 用途 | 设置位置 |
|--------|------|----------|
| `ALGOLIA_APP_ID` | Algolia 应用 ID | GitHub Secrets |
| `ALGOLIA_ADMIN_KEY` | Algolia 管理密钥 | GitHub Secrets |
| `GA_TRACKING_ID` | Google Analytics ID | GitHub Secrets |

### 域名配置说明

如需使用自定义域名：

1. **DNS 配置**:

   ```
   CNAME kg.analysisdataflow.com → <username>.github.io
   ```

2. **GitHub 配置**:
   - Settings → Pages → Custom domain
   - 输入: `kg.analysisdataflow.com`
   - 勾选 Enforce HTTPS

3. **验证 DNS**:

   ```bash
   dig kg.analysisdataflow.com +nostats +nocomments +nocmd
   ```

---

## 🔒 SEO 优化配置

### 1. Sitemap

文件已内嵌在 HTML 中，如需独立 sitemap：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://kg.analysisdataflow.com/</loc>
    <lastmod>2026-04-12</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

### 2. Robots.txt

```
User-agent: *
Allow: /

Sitemap: https://kg.analysisdataflow.com/sitemap.xml
```

### 3. 结构化数据

已配置 Schema.org SoftwareApplication 标记：

- 应用名称
- 描述
- 许可证信息
- 价格（免费）

---

## 🧪 部署验证

### 自动化测试

部署工作流包含以下测试：

1. **HTML 验证**: 使用 htmlhint 检查语法
2. **文件大小检查**: 确保文件不超过 50MB
3. **必需文件验证**: 检查 index.html, 404.html, .nojekyll

### 手动验证清单

- [ ] 页面正常加载，无控制台错误
- [ ] 3D 可视化正常显示
- [ ] 搜索功能正常工作
- [ ] Service Worker 注册成功 (DevTools → Application)
- [ ] 离线访问正常 (断网测试)
- [ ] 响应式布局正常 (移动端测试)

### 性能指标

目标性能指标：

| 指标 | 目标 | 工具 |
|------|------|------|
| First Contentful Paint | < 1.5s | Lighthouse |
| Largest Contentful Paint | < 2.5s | Lighthouse |
| Time to Interactive | < 3.5s | Lighthouse |
| Cumulative Layout Shift | < 0.1 | Lighthouse |

---

## 🚨 故障排查

### 常见问题

**1. GitHub Pages 404**

- 确保已启用 GitHub Pages (Settings → Pages)
- 检查 Source 设置为 GitHub Actions

**2. 静态资源加载失败**

- 检查 `knowledge-graph-site/.nojekyll` 文件存在
- 验证文件路径大小写（Linux 区分大小写）

**3. 搜索无结果**

- 验证 `search-index.json` 已生成
- 检查 Algolia 索引配置和 API 密钥

**4. Service Worker 未注册**

- 确保使用 HTTPS 访问
- 检查浏览器支持情况

---

## 📞 支持

如有部署问题，请通过以下方式获取帮助：

- 创建 GitHub Issue: [New Issue](https://github.com/AnalysisDataFlow/AnalysisDataFlow/issues)
- 查看部署日志: Actions → Deploy Knowledge Graph → 最新运行

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0.0 | 2026-04-12 | 初始部署文档，支持 GitHub Pages + Cloudflare CDN + Algolia |

---

*本文档由自动化部署工具生成，最后更新: 2026-04-12*
