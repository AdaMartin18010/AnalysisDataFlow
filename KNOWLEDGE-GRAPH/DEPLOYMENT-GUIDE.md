# AnalysisDataFlow 知识图谱 v2.0 部署指南

> **版本**: v4.2 | **最后更新**: 2026-04-13

---

## 1. 部署概述

AnalysisDataFlow 知识图谱 v2.0 是一个基于 React 18 + D3.js + Three.js 的静态单页应用，
可直接部署到 GitHub Pages，无需后端服务器。

## 2. 前置要求

- GitHub 仓库管理员权限
- 可选：自定义域名及 DNS 管理权限
- 可选：Cloudflare 账户（用于 CDN 加速）

## 3. GitHub Pages 部署步骤

### 3.1 启用 GitHub Pages

1. 进入仓库 Settings > Pages
2. Source 选择 **"GitHub Actions"**
3. 保存设置

### 3.2 验证自动部署

推送任意更改到 `KNOWLEDGE-GRAPH/` 目录或 `.github/workflows/deploy-knowledge-graph.yml`，
GitHub Actions 工作流将自动构建并部署。

部署完成后，访问：

```
https://github.com/luyanfeng/AnalysisDataFlow/
```

## 4. 自定义域名配置

1. 修改 `KNOWLEDGE-GRAPH/CNAME` 文件，写入你的域名：

   ```
   kg.analysisdataflow.io
   ```

2. 在 DNS 服务商添加 CNAME 记录：

   ```
   kg.analysisdataflow.io → github.com/luyanfeng/AnalysisDataFlow
   ```

3. 在仓库 Settings > Pages 的 Custom domain 中填入域名并验证
4. 勾选 "Enforce HTTPS"

## 5. Algolia DocSearch 集成

### 5.1 申请 DocSearch

访问 <https://docsearch.algolia.com/apply/> 提交申请。

所需信息：

- 网站 URL
- GitHub 仓库链接
- 邮箱地址

### 5.2 集成搜索代码

获得 `appId`、`apiKey`、`indexName` 后，更新 `KNOWLEDGE-GRAPH/index.html` 中的搜索组件配置：

```javascript
const searchConfig = {
  appId: 'YOUR_APP_ID',
  apiKey: 'YOUR_SEARCH_API_KEY',
  indexName: 'analysisdataflow',
};
```

## 6. Cloudflare CDN 加速

1. 在 Cloudflare 添加域名
2. DNS 记录指向 GitHub Pages
3. 开启以下优化：
   - Auto Minify (HTML/CSS/JS)
   - Brotli 压缩
   - Always Use HTTPS
   - Rocket Loader（可选，视 Three.js 兼容性而定）

## 7. 故障排查

| 问题 | 排查方法 |
|------|---------|
| 页面空白 | 检查浏览器控制台是否有 CDN 资源加载失败 |
| 404 错误 | 确认 `404.html` 已部署；检查自定义域名解析 |
| 搜索不工作 | 确认 Algolia 配置正确，索引已构建 |
| HTTPS 证书错误 | 在 GitHub Pages 设置中重新验证域名 |

---

*AnalysisDataFlow Knowledge Graph Deployment Guide*
