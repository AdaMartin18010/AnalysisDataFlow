# 社区反馈管理系统

本目录包含 AnalysisDataFlow 项目的社区反馈管理工具和模板。

## 📁 目录结构

```
.github/
├── ISSUE_TEMPLATE/           # GitHub Issue 表单模板
│   ├── 01_documentation_improvement.yml
│   ├── 02_bug_report.yml
│   ├── 03_content_suggestion.yml
│   ├── 04_new_topic_request.yml
│   └── config.yml
├── feedback-templates/       # 回复模板和分类指南
│   ├── README.md            # 本文件
│   ├── thank-you.md         # 感谢和回复模板
│   └── classification.md    # 分类指南
└── workflows/               # 自动化工作流
    └── feedback-management.yml
```

## 🚀 快速开始

### 提交反馈

1. 访问 [Issues 页面](../../issues/new/choose)
2. 选择合适的模板：
   - 📚 文档改进请求
   - 🐛 错误报告
   - 💡 内容建议
   - 🆕 新主题请求
3. 填写表单并提交

### 处理反馈（维护者）

1. **分类评估**（收到 Issue 后 3 天内）
   - 添加适当的标签（type, priority, category, status）
   - 使用感谢模板回复

2. **优先级处理**
   - 🔴 P0: 立即处理
   - 🟠 P1: 1 周内处理
   - 🟡 P2: 按计划处理
   - 🟢 P3: 时间允许时处理

3. **状态跟踪**
   - `triage` → `in-progress` → `completed`/`wontfix`

## 🏷️ 标签系统

### 类型标签
- `bug` - 错误报告
- `enhancement` - 功能建议
- `documentation` - 文档改进
- `new-topic` - 新主题请求

### 优先级标签
- `P0` - 关键，必须立即处理
- `P1` - 重要，应在近期处理
- `P2` - 一般，按计划处理
- `P3` - 建议性，时间允许时处理

### 领域标签
- `Struct` - 形式理论与分析
- `Knowledge` - 工程知识与设计模式
- `Flink` - Flink 专项技术

### 状态标签
- `triage` - 待分类评估
- `in-progress` - 处理中
- `needs-info` - 需要更多信息
- `blocked` - 处理受阻
- `completed` - 已完成
- `wontfix` - 不修复
- `duplicate` - 重复 Issue

## 📊 反馈聚合

### 生成本地报告

```bash
# 完整分析
python .scripts/feedback-aggregator.py --full-analysis

# 仅生成月度报告
python .scripts/feedback-aggregator.py --monthly

# 更新贡献者列表
python .scripts/feedback-aggregator.py --update-contributors

# 提取高优先级任务
python .scripts/feedback-aggregator.py --extract-p0-p1
```

### GitHub Actions 自动报告

项目配置了定时任务，每月自动生成反馈报告：
- 报告位置: `reports/feedback/monthly-report-YYYY-MM.md`
- 贡献者更新: `CONTRIBUTORS.md`

## 📈 可视化仪表板

### 本地仪表板

```bash
# 启动本地仪表板服务器
python .scripts/feedback-aggregator.py --dashboard

# 访问 http://localhost:8080
```

### 图表类型

1. **反馈趋势图** - Issue 提交和解决趋势
2. **类型分布图** - 按反馈类型分类统计
3. **优先级热力图** - P0-P3 分布情况
4. **贡献者活跃度** - 社区参与情况
5. **处理效率图** - 平均解决时间趋势

## 🤝 贡献指南

### 改进 Issue 模板

1. 编辑 `.github/ISSUE_TEMPLATE/*.yml`
2. 测试表单渲染
3. 提交 PR

### 添加新的回复模板

1. 在 `.github/feedback-templates/` 创建新模板
2. 遵循现有格式规范
3. 更新本 README

### 改进聚合脚本

1. 编辑 `.scripts/feedback-aggregator.py`
2. 添加测试用例
3. 提交 PR

## 📞 联系方式

- 💬 讨论区: [GitHub Discussions](../../discussions)
- 📧 邮件联系: [项目维护者](../../graphs/contributors)
- 🐛 Issue 模板问题: 提交 [Meta Issue](../../issues/new?labels=meta)

---

*最后更新: 2026-04-04*
