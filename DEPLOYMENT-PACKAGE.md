# 知识图谱 v2.0 部署包

> **生成时间**: 2026-04-12 | **版本**: v2.0.0

## 📦 包内容清单

### 1. 核心文件

| 文件 | 描述 | 大小 |
|------|------|------|
| `knowledge-graph-v4.html` | 主知识图谱页面 | ~60KB |
| `knowledge-graph.html` | 旧版兼容页面 | ~30KB |
| `THEOREM-REGISTRY.md` | 定理注册表数据源 | ~300KB |

### 2. 构建脚本 (`.scripts/kg-v2/`)

| 脚本 | 功能 |
|------|------|
| `generate-static-data.py` | 生成静态图谱数据 |
| `generate-search-index.py` | 生成搜索索引 |
| `generate-learning-paths.py` | 生学习路径数据 |
| `optimize-assets.py` | 资源优化与压缩 |
| `push-to-algolia.py` | 推送数据到 Algolia |
| `setup-cloudflare.sh` | Cloudflare 配置脚本 |

### 3. 工作流配置 (`.github/workflows/`)

| 文件 | 描述 |
|------|------|
| `deploy-kg.yml` | 基础 GitHub Pages 部署 |
| `deploy-kg-v2.yml` | 完整生产部署（含 Algolia） |
| `deploy-knowledge-graph.yml` | 旧版工作流（备用） |

### 4. 生成的站点文件 (`knowledge-graph-site/`)

```
knowledge-graph-site/
├── index.html              # 主页面
├── 404.html               # 404 错误页面
├── service-worker.js      # Service Worker（离线支持）
├── manifest.json          # PWA Manifest
├── build-info.json        # 构建信息
├── .nojekyll              # 禁用 Jekyll
├── load-optimizer.js      # 资源预加载优化
├── _headers               # Cloudflare 头部配置
├── _redirects             # Cloudflare 重定向配置
└── data/
    ├── graph-data.json         # 图谱数据 (~5KB)
    ├── graph-data.json.gz      # 压缩版本 (~1KB)
    ├── metadata.json           # 元数据
    ├── search-index.json       # 搜索索引 (~2000+ 条目)
    ├── search-suggestions.json # 搜索建议
    ├── learning-paths.json     # 学习路径
    ├── skill-tree.json         # 技能树
    └── chunks/                 # 分块数据
        ├── struct.json
        ├── knowledge.json
        ├── flink.json
        ├── theorem.json
        ├── definition.json
        ├── lemma.json
        ├── proposition.json
        └── corollary.json
```

---

## 🚀 部署方式

### 方式一: GitHub Pages（推荐，免费）

**自动部署**:

1. 推送代码到 `main` 或 `master` 分支
2. GitHub Actions 自动构建并部署
3. 访问: `https://<username>.github.io/AnalysisDataFlow/knowledge-graph/`

**手动触发**:

1. 进入仓库 Actions 标签
2. 选择 "Deploy Knowledge Graph v2.0 (Production)"
3. 点击 "Run workflow"

### 方式二: Cloudflare Pages（全球 CDN）

**快速部署**:

```bash
# 安装 wrangler
npm install -g wrangler

# 登录 Cloudflare
wrangler login

# 部署
wrangler pages deploy knowledge-graph-site
```

**Git 集成**:

1. Cloudflare Dashboard → Pages → Create a project
2. 连接 GitHub 仓库
3. 构建设置:
   - Build command: `python .scripts/kg-v2/generate-static-data.py && python .scripts/kg-v2/optimize-assets.py`
   - Build output directory: `knowledge-graph-site`

### 方式三: 静态文件托管

任何支持静态文件托管的服务均可：

- Netlify
- Vercel
- AWS S3 + CloudFront
- Azure Static Web Apps
- 自有服务器

只需上传 `knowledge-graph-site/` 目录内容即可。

---

## ⚙️ 环境变量配置

### GitHub Secrets（必需）

| 变量名 | 用途 | 获取方式 |
|--------|------|----------|
| `ALGOLIA_APP_ID` | Algolia 应用 ID | Algolia Dashboard → API Keys |
| `ALGOLIA_ADMIN_KEY` | Algolia 管理密钥 | Algolia Dashboard → API Keys |
| `ALGOLIA_INDEX_NAME` | Algolia 索引名称 | 可选，默认: `analysisdataflow_kg` |
| `GA_TRACKING_ID` | Google Analytics ID | Google Analytics → 数据流 |

### Cloudflare Pages 环境变量

| 变量名 | 值 |
|--------|-----|
| `PYTHON_VERSION` | 3.11 |
| `NODE_VERSION` | 20 |
| `ALGOLIA_APP_ID` | (同上) |
| `ALGOLIA_ADMIN_KEY` | (同上) |

---

## 🌐 预期访问地址

部署成功后，可通过以下地址访问：

| 平台 | URL 格式 | 示例 |
|------|----------|------|
| GitHub Pages | `https://<username>.github.io/AnalysisDataFlow/knowledge-graph/` | `https://analysisdataflow.github.io/AnalysisDataFlow/knowledge-graph/` |
| Cloudflare Pages | `https://<project-name>.pages.dev` | `https://analysisdataflow-kg.pages.dev` |
| 自定义域名 | `https://kg.yourdomain.com` | `https://kg.analysisdataflow.com` |

---

## 🔒 安全与性能

### 已配置的安全措施

- ✅ HTTPS 强制（GitHub Pages/Cloudflare 默认）
- ✅ X-Frame-Options: DENY
- ✅ X-Content-Type-Options: nosniff
- ✅ Referrer-Policy: strict-origin-when-cross-origin
- ✅ CSP (Content Security Policy) 在 HTML 中配置

### 性能优化

- ✅ JSON 数据 gzip 压缩（节省 ~70% 体积）
- ✅ Service Worker 离线缓存
- ✅ CDN 资源预连接
- ✅ 懒加载和代码分割
- ✅ Brotli 压缩（Cloudflare）

### SEO 优化

- ✅ 完整的 Meta Tags
- ✅ Open Graph 协议
- ✅ Twitter Cards
- ✅ Schema.org 结构化数据
- ✅ Canonical URL

---

## 🧪 验证清单

部署后请验证以下功能：

### 基本功能

- [ ] 页面正常加载，无控制台错误
- [ ] 3D 可视化正常显示
- [ ] 节点可点击，显示详情
- [ ] 搜索功能正常工作
- [ ] 响应式布局（移动端/桌面端）

### 高级功能

- [ ] Service Worker 注册成功 (DevTools → Application → Service Workers)
- [ ] 离线访问正常 (断网后刷新)
- [ ] PWA 安装提示（支持的话）
- [ ] Algolia 搜索结果（如配置）

### 性能指标

- [ ] First Contentful Paint < 1.5s
- [ ] Largest Contentful Paint < 2.5s
- [ ] Time to Interactive < 3.5s

---

## 📞 故障排查

### 常见问题

**1. GitHub Pages 返回 404**

```bash
# 检查 .nojekyll 文件存在
touch knowledge-graph-site/.nojekyll
```

**2. Algolia 推送失败**

```bash
# 检查环境变量设置
echo $ALGOLIA_APP_ID
echo $ALGOLIA_ADMIN_KEY
```

**3. 静态资源加载失败**

- 检查文件路径大小写（Linux 区分大小写）
- 验证 `_headers` 和 `_redirects` 配置

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0.0 | 2026-04-12 | 初始部署包，支持 GitHub Pages + Cloudflare + Algolia |

---

*本文档由自动化部署工具生成*
