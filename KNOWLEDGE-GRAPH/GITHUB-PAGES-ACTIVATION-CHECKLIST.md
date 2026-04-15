# GitHub Pages 激活与 Algolia 集成操作清单

> **版本**: v4.2 | **最后更新**: 2026-04-15

本清单记录仓库管理员需要在 GitHub UI 上手动完成的全部步骤。

---

## 1. 启用 GitHub Pages

1. 打开仓库主页，点击 **Settings** 标签
2. 在左侧导航栏选择 **Pages**
3. **Source** 选择 **GitHub Actions**
4. 点击 **Save**

## 2. 配置自定义域名

1. 在 **Settings > Pages** 页面
2. **Custom domain** 输入框填入：

   ```
   knowledge-graph.analysisdataflow.github.io
   ```

3. 点击 **Save**
4. 等待 DNS 检查通过（出现绿色 ✓ 标记）

## 3. 强制 HTTPS

1. 在 **Settings > Pages** 页面
2. 勾选 **Enforce HTTPS**
3. 点击 **Save**

## 4. 启用 Discussions（如未启用）

1. 在 **Settings > General** 页面
2. 找到 **Features** 区域
3. 勾选 **Discussions**
4. 点击 **Save**

## 5. 验证首次部署成功

1. 向 `main` 分支推送任意影响 `KNOWLEDGE-GRAPH/` 的更改（或手动触发工作流）
2. 打开仓库主页的 **Actions** 标签
3. 找到 **Deploy Knowledge Graph to GitHub Pages** 工作流
4. 确认最新运行状态为 ✅ **绿色通过**
5. 访问以下 URL 验证页面可正常加载：

   ```
   https://knowledge-graph.analysisdataflow.github.io/
   ```

## 6. 申请 Algolia DocSearch

1. 访问 <https://docsearch.algolia.com/apply/> 提交申请
2. 填写申请表格，需提供以下信息：
   - **Website URL**: `https://knowledge-graph.analysisdataflow.github.io/`
   - **GitHub Repository**: `https://github.com/AnalysisDataFlow/AnalysisDataFlow`
   - **Email**: 你的邮箱地址
3. 提交后等待 Algolia 团队审核（通常 1–3 个工作日）
4. 审核通过后，你将收到包含 `appId`、`apiKey`、`indexName` 的邮件

## 7. 获得凭证后更新 ALGOLIA_CONFIG

1. 打开 `KNOWLEDGE-GRAPH/index.html`
2. 找到 `ALGOLIA_CONFIG` 对象（位于 `<script>` 顶部）
3. 替换占位值：

   ```javascript
   const ALGOLIA_CONFIG = {
       enabled: true,
       appId: '你的实际_APP_ID',
       apiKey: '你的实际_SEARCH_API_KEY',
       indexName: 'analysisdataflow',
       searchParameters: {
           hitsPerPage: 10
       }
   };
   ```

4. 如需集成 DocSearch React 组件，可进一步替换 `SearchPanel` 中的 `// TODO: Integrate Algolia DocSearch here` 部分为官方 DocSearch 代码
5. 保存并提交到 `main` 分支，GitHub Actions 将自动重新部署

---

*AnalysisDataFlow Knowledge Graph Operations Checklist*
