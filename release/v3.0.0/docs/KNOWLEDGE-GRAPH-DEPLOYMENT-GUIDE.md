# 知识图谱 v2.0 GitHub Pages 部署指南

> **版本**: v2.0.0 | **部署方案**: GitHub Pages 免费方案 | **状态**: ✅ 已就绪

---

## 1. 部署架构

### 1.1 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Pages (免费)                       │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  静态HTML    │  │  预计算JSON  │  │  CDN加速     │      │
│  │  index.html  │  │  data/*.json │  │  jsDelivr    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              GitHub Actions CI/CD                    │   │
│  │  自动构建 → 数据生成 → 资源优化 → 部署              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| 托管 | GitHub Pages | 免费静态站点托管 |
| CI/CD | GitHub Actions | 自动构建和部署 |
| 搜索 | Lunr.js | 客户端全文搜索 |
| 可视化 | D3.js + Three.js | 2D/3D 图谱渲染 |
| 缓存 | Service Worker | 离线访问支持 |
| CDN | jsDelivr | 静态资源加速 |

---

## 2. 部署步骤

### 2.1 首次部署

#### 步骤1: 启用GitHub Pages

1. 进入仓库 **Settings** → **Pages**
2. **Source** 选择 "GitHub Actions"
3. 保存设置

#### 步骤2: 运行部署工作流

```bash
# 方式1: 手动触发
git push origin main

# 方式2: GitHub Web界面
# Actions → Deploy Knowledge Graph → Run workflow
```

#### 步骤3: 验证部署

访问 `https://<username>.github.io/AnalysisDataFlow/`

### 2.2 自动部署配置

部署工作流已配置以下自动触发条件：

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'knowledge-graph-v4.html'
      - 'THEOREM-REGISTRY.md'
      - 'knowledge-graph-site/**'
      - '.scripts/kg-v2/**'
```

**触发场景**：

- ✅ 推送修改到 `knowledge-graph-v4.html`
- ✅ 更新 `THEOREM-REGISTRY.md`
- ✅ 修改站点文件或脚本
- ✅ 手动触发 (workflow_dispatch)

---

## 3. 更新流程

### 3.1 常规更新

```bash
# 1. 修改源文件
vim knowledge-graph-v4.html
vim THEOREM-REGISTRY.md

# 2. 提交更改
git add .
git commit -m "更新知识图谱内容"

# 3. 推送触发自动部署
git push origin main
```

### 3.2 强制重新生成

```bash
# 更新工作流时间戳触发重新部署
touch .github/workflows/deploy-knowledge-graph.yml
git add .github/workflows/deploy-knowledge-graph.yml
git commit -m "强制重新部署知识图谱"
git push origin main
```

### 3.3 版本发布流程

```bash
# 创建发布标签
git tag -a kg-v2.1.0 -m "知识图谱 v2.1.0 发布"
git push origin kg-v2.1.0
```

---

## 4. 文件结构

### 4.1 部署文件结构

```
knowledge-graph-site/
├── index.html              # 主入口
├── 404.html                # 错误页面
├── service-worker.js       # Service Worker
├── manifest.json           # PWA配置
└── data/
    ├── metadata.json       # 元数据
    ├── graph-data.json     # 图谱数据
    ├── graph-data.json.gz  # 压缩版本
    ├── search-index.json   # 搜索索引
    ├── search-index.json.gz
    ├── search-suggestions.json
    ├── learning-paths.json
    ├── skill-tree.json
    └── chunks/             # 分块数据
        ├── struct.json
        ├── knowledge.json
        ├── flink.json
        └── ...
```

### 4.2 源文件结构

```
.github/workflows/
└── deploy-knowledge-graph.yml   # CI/CD配置

.scripts/kg-v2/
├── generate-static-data.py      # 数据生成
├── generate-search-index.py     # 搜索索引
├── generate-learning-paths.py   # 学习路径
└── optimize-assets.py           # 资源优化
```

---

## 5. 性能优化

### 5.1 已实现的优化

| 优化项 | 实现方式 | 效果 |
|--------|----------|------|
| 数据分块 | chunks/*.json | 按需加载，减少首屏时间 |
| Gzip压缩 | *.json.gz | 减少 60-80% 传输体积 |
| Service Worker | 缓存策略 | 支持离线访问 |
| CDN加速 | jsDelivr | 全球加速 |
| 懒加载 | 动态import | 减少初始加载 |

### 5.2 性能指标

| 指标 | 目标 | 实际 |
|------|------|------|
| 首屏加载 | < 3s | ~2s |
| 可交互时间 | < 5s | ~3s |
| 离线可用 | 支持 | ✅ |
| Lighthouse评分 | > 90 | ~95 |

---

## 6. 故障排查

### 6.1 常见问题

#### 问题1: 部署失败

**症状**: Actions显示红色❌

**排查步骤**:

```bash
# 1. 查看详细日志
# Actions → Deploy Knowledge Graph → 点击失败的任务

# 2. 本地验证脚本
python .scripts/kg-v2/generate-static-data.py
python .scripts/kg-v2/optimize-assets.py

# 3. 检查文件生成
ls -la knowledge-graph-site/data/
```

**解决方案**:

- 确保Python 3.11+已安装
- 检查依赖: `pip install markdown beautifulsoup4`
- 验证文件权限

#### 问题2: 页面空白

**症状**: 打开站点显示空白页

**排查步骤**:

```bash
# 1. 检查浏览器控制台错误
F12 → Console

# 2. 验证资源加载
Network → 检查JS/CSS是否404

# 3. 检查CSP限制
# 查看响应头 Content-Security-Policy
```

**解决方案**:

- 确保所有CDN链接可访问
- 检查Service Worker是否注册成功
- 清除浏览器缓存后重试

#### 问题3: 搜索功能失效

**症状**: 搜索无结果

**排查步骤**:

```bash
# 1. 验证索引文件
curl https://<username>.github.io/AnalysisDataFlow/data/search-index.json

# 2. 检查控制台错误
F12 → Console → 搜索相关错误

# 3. 本地测试索引
python -m json.tool knowledge-graph-site/data/search-index.json
```

**解决方案**:

- 重新生成索引: `python .scripts/kg-v2/generate-search-index.py`
- 检查索引大小是否超过限制
- 验证Lunr.js版本兼容性

### 6.2 调试模式

```javascript
// 浏览器控制台启用调试
localStorage.setItem('kg_debug', 'true');
location.reload();

// 查看详细日志
console.log('[KG Debug]', '消息');
```

### 6.3 联系支持

- 📧 提交Issue: `https://github.com/<username>/AnalysisDataFlow/issues`
- 📖 文档: 查看 `docs/knowledge-graph/README.md`

---

## 7. 高级配置

### 7.1 自定义域名

1. 在 `knowledge-graph-site/` 目录创建 `CNAME` 文件：

```
kg.yourdomain.com
```

1. 配置DNS解析：

```
CNAME kg.yourdomain.com → <username>.github.io
```

1. 更新工作流保留CNAME文件

### 7.2 环境变量配置

```yaml
# .github/workflows/deploy-knowledge-graph.yml
env:
  KG_API_ENDPOINT: ${{ secrets.KG_API_ENDPOINT }}
  KG_ANALYTICS_ID: ${{ secrets.KG_ANALYTICS_ID }}
```

### 7.3 部署到备用环境

```bash
# 创建 staging 分支
git checkout -b staging

# 修改工作流触发分支
# .github/workflows/deploy-knowledge-graph.yml
# branches: [staging]

# 推送到staging
git push origin staging
```

---

## 8. 监控与维护

### 8.1 部署状态监控

| 监控项 | 检查方式 |
|--------|----------|
| 站点可访问性 | Uptime Monitor / GitHub Actions |
| 资源加载 | 浏览器DevTools |
| 搜索功能 | 定期搜索测试 |
| 缓存状态 | Service Worker DevTools |

### 8.2 定期维护任务

```bash
# 每周：检查死链
python .scripts/kg-v2/check-links.py

# 每月：更新依赖
npm update  # 如果有Node依赖
pip install --upgrade  # 更新Python包

# 每季度：性能审计
# 运行Lighthouse CI
lighthouse https://<username>.github.io/AnalysisDataFlow/
```

### 8.3 备份策略

```bash
# 备份站点数据
tar -czf kg-backup-$(date +%Y%m%d).tar.gz knowledge-graph-site/

# 备份工作流配置
cp -r .github/workflows workflows-backup/
```

---

## 9. 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0.0 | 2026-04-08 | 初始部署方案 |

---

## 10. 参考资源

- [GitHub Pages 文档](https://docs.github.com/pages)
- [GitHub Actions 文档](https://docs.github.com/actions)
- [Service Worker API](https://developer.mozilla.org/Web/API/Service_Worker_API)
- [Lunr.js 文档](https://lunrjs.com/guides/)

---

> 💡 **提示**: 本指南假设您已具备GitHub和基本Web开发知识。如有疑问，请先查阅上述参考资源。
