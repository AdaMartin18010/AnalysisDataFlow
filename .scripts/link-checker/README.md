# 🔗 链接检查自动化系统

> 版本: 1.0.0 | AnalysisDataFlow 项目

一套完整的 Markdown 文件链接检查和修复自动化系统。

---

## 📋 功能特性

- ✅ **递归扫描**: 自动扫描所有 Markdown 文件中的链接
- 🌐 **外部链接检查**: 验证 HTTP/HTTPS 链接的可访问性
- 📁 **内部链接检查**: 验证相对路径和锚点的有效性
- ⚡ **异步并发**: 使用 aiohttp 实现高并发检查
- 📊 **详细报告**: 生成 HTML 和 Markdown 格式的报告
- 🔧 **修复建议**: 自动提供 Wayback Machine 存档等替代链接
- 🔄 **CI/CD 集成**: 完整的 GitHub Actions 工作流支持
- 📈 **历史趋势**: 跟踪链接健康度变化趋势

---

## 🚀 快速开始

### 安装依赖

```bash
cd .scripts/link-checker
pip install -r requirements.txt
```

### 基本使用

```bash
# 检查当前目录下的所有 Markdown 文件
python link-checker.py

# 指定目录
python link-checker.py --path ../../docs

# 使用自定义配置
python link-checker.py --config config.yaml

# 生成报告
python report-generator.py --input link-check-results.json --output-html report.html

# 获取修复建议
python fix-suggestions.py --input link-check-results.json --generate-script
```

---

## 📁 文件结构

```
.scripts/link-checker/
├── README.md                    # 本文档
├── requirements.txt             # Python 依赖
├── config.yaml                  # 配置文件
├── link-checker.py             # 核心检查脚本
├── report-generator.py         # 报告生成器
├── fix-suggestions.py          # 修复建议工具
└── github-action-integration.md # GitHub Actions 集成指南
```

---

## ⚙️ 配置说明

编辑 `config.yaml` 来自定义检查行为:

```yaml
# 排除特定URL模式
exclude:
  - '^https?://localhost'
  - '^https?://example\.com'

# 超时设置 (秒)
timeout:
  total: 30
  connect: 10

# 重试策略
retry:
  max_retries: 3
  delay: 1

# 并发控制
max_concurrent: 50
max_per_host: 10
```

---

## 📊 报告示例

检查完成后会生成:

- `link-check-results.json` - 详细的JSON结果
- `link-report.html` - 美观的HTML报告
- `link-report.md` - 适合GitHub的Markdown报告

HTML报告包含:
- 统计概览卡片
- 历史趋势图表
- 失效链接详情表格
- 域名健康度统计
- 按文件汇总的链接状态

---

## 🔧 修复建议

运行修复建议工具来自动获取替代链接:

```bash
python fix-suggestions.py --input link-check-results.json
```

支持的建议类型:
- 🔀 **自动重定向**: 检测并建议正确的重定向目标
- 🔒 **HTTPS升级**: http:// 升级到 https://
- 📚 **Wayback存档**: 从 Internet Archive 获取历史快照
- 📖 **文档更新**: 建议更新到最新版本文档
- ✋ **手动修复**: 标记需要人工介入的链接

自动生成 `auto-fix-links.py` 脚本用于批量修复。

---

## 🔄 GitHub Actions 集成

详见 [github-action-integration.md](./github-action-integration.md)

### 主要功能

- **PR检查**: 自动检查 Pull Request 中的链接
- **定期扫描**: 每周自动全量检查
- **自动Issue**: 发现失效链接时自动创建 Issue
- **PR评论**: 在 PR 中发布检查结果摘要

### 快速设置

1. 将工作流文件复制到 `.github/workflows/`
2. 配置 Secrets (可选): `SLACK_WEBHOOK_URL`
3. 提交并推送

---

## 📈 历史趋势

启用历史记录来跟踪链接健康度变化:

```bash
python report-generator.py --input results.json --save-history
```

历史数据保存在 `link-check-history/` 目录，用于:
- 趋势分析图表
- 回归检测
- 链接健康度报告

---

## 🛠️ 高级用法

### 仅检查特定文件

```bash
python link-checker.py --patterns "docs/**/*.md" "README.md"
```

### 详细日志

```bash
python link-checker.py --verbose
```

### 自定义输出

```bash
python link-checker.py --output my-results.json
python report-generator.py --input my-results.json --output-html my-report.html
```

---

## 🔍 支持的链接类型

| 类型 | 示例 | 检查方式 |
|------|------|----------|
| 外部HTTP/HTTPS | `https://example.com` | HTTP HEAD/GET 请求 |
| 相对路径 | `./docs/guide.md` | 文件系统检查 |
| 绝对路径 | `/docs/guide.md` | 基于根目录检查 |
| 锚点链接 | `#section-title` | Markdown标题解析 |
| 邮件链接 | `mailto:email@example.com` | 格式验证 |
| 文件链接 | `file://path/to/file` | 文件存在性检查 |

---

## ⚠️ 注意事项

1. **速率限制**: 请合理设置 `delay_between_requests` 避免被目标网站封禁
2. **SSL验证**: 默认禁用 SSL 验证，可在 config.yaml 中启用
3. **排除列表**: 建议将内部系统、需要登录的页面添加到排除列表
4. **并发数**: 大型仓库建议降低 `max_concurrent` 以避免内存问题

---

## 🐛 故障排除

### 检查超时

增加超时设置:
```yaml
timeout:
  total: 60
  connect: 20
```

### 内存不足

降低并发数:
```yaml
max_concurrent: 20
file_batch_size: 5
```

### 大量SSL错误

```yaml
verify_ssl: false
```

---

## 🤝 贡献

欢迎提交 Issue 和 PR 来改进链接检查系统!

---

## 📄 许可证

与主项目许可证一致 (MIT)

---

*Generated for AnalysisDataFlow Project*
