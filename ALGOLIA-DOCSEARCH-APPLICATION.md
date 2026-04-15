# Algolia DocSearch 申请模板

> **项目**: AnalysisDataFlow  
> **仓库**: https://github.com/AdaMartin18010/AnalysisDataFlow  
> **网站**: https://adamartin18010.github.io/AnalysisDataFlow/  
> **生成时间**: 2026-04-15

---

## 预填充申请表单

直接复制以下内容到 [DocSearch 申请表单](https://docsearch.algolia.com/apply/)：

| 字段 | 填写内容 |
|------|----------|
| **Email** | *(你的邮箱)* |
| **Repository URL** | `https://github.com/AdaMartin18010/AnalysisDataFlow` |
| **Website URL** | `https://adamartin18010.github.io/AnalysisDataFlow/` |
| **Project Name** | `AnalysisDataFlow` |
| **Description** | A comprehensive knowledge base for stream processing theory, formal methods, and Apache Flink ecosystem. |
| **Is your project open source?** | ✅ Yes |
| **License** | CC BY-SA 4.0 / Apache 2.0 (Mixed) |
| **Tech Stack** | React + static HTML (GitHub Pages) |
| **Owner of the website?** | Yes |

---

## 预写申请邮件（可选）

若需要向 Algolia 团队发送补充邮件，可直接复制以下内容：

```text
Subject: DocSearch Application for AnalysisDataFlow

Hi Algolia DocSearch Team,

We have applied for DocSearch for our open-source knowledge base project:

- Repository: https://github.com/AdaMartin18010/AnalysisDataFlow
- Site: https://adamartin18010.github.io/AnalysisDataFlow/
- Sitemap: https://adamartin18010.github.io/AnalysisDataFlow/sitemap.xml

The site is built with static HTML hosted on GitHub Pages and contains
over 900 Markdown documents, 10,000+ formalized theorems/definitions,
and an interactive 3D knowledge graph. We have already integrated the
DocSearch frontend placeholder and are ready to receive the crawler
configuration.

Please let us know if any additional information is needed.

Best regards,
AnalysisDataFlow Team
```

---

## 收到 API Key 后的操作

Algolia 批复后会邮件发送以下信息：
- `appId`
- `apiKey` (Search-Only API Key)
- `indexName`

### 更新 `KNOWLEDGE-GRAPH/index.html`

搜索文件中的 `ALGOLIA_CONFIG` 占位区：

```javascript
const ALGOLIA_CONFIG = {
    enabled: false,
    appId: 'YOUR_APP_ID',
    apiKey: 'YOUR_SEARCH_API_KEY',
    indexName: 'analysisdataflow',
    searchParameters: {
        hitsPerPage: 10
    }
};
```

替换为：

```javascript
const ALGOLIA_CONFIG = {
    enabled: true,
    appId: 'XXXXXXXXXX',      // ← 替换为 Algolia 提供的 appId
    apiKey: 'XXXXXXXXXX',     // ← 替换为 Search-Only API Key
    indexName: 'analysisdataflow',
    searchParameters: {
        hitsPerPage: 10
    }
};
```

> ⚠️ **警告**: 仅使用 **Search-Only API Key**，切勿暴露 Admin API Key。

### 触发重新部署

提交更改后，GitHub Actions 会自动部署。部署完成后：
1. 清除浏览器缓存
2. 访问站点首页
3. 在搜索框输入 "Flink" 测试是否返回 Algolia 结果

---

*最后更新: 2026-04-15*
