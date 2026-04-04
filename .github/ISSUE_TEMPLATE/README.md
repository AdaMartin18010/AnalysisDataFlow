# GitHub Issue 模板

本目录包含 AnalysisDataFlow 项目的 GitHub Issue 表单模板。

## 📋 模板列表

| 模板 | 文件名 | 用途 |
|------|--------|------|
| 📚 文档改进请求 | `01_documentation_improvement.yml` | 改进现有文档内容、结构或表述 |
| 🐛 错误报告 | `02_bug_report.yml` | 报告项目中的错误或问题 |
| 💡 内容建议 | `03_content_suggestion.yml` | 建议添加新内容或扩展现有主题 |
| 🆕 新主题请求 | `04_new_topic_request.yml` | 建议添加全新的知识主题 |

## 🚀 使用方法

1. 访问项目的 [Issues 页面](https://github.com/your-org/AnalysisDataFlow/issues/new/choose)
2. 点击 "Get started" 选择合适的模板
3. 填写表单中的所有必填项
4. 提交 Issue

## 🏷️ 标签自动应用

提交 Issue 时，系统会自动应用以下标签：

| 模板 | 自动标签 |
|------|----------|
| 文档改进请求 | `documentation`, `triage` |
| 错误报告 | `bug`, `triage` |
| 内容建议 | `enhancement`, `triage` |
| 新主题请求 | `new-topic`, `triage` |

维护者后续会根据内容添加：

- 优先级标签: `P0`, `P1`, `P2`, `P3`
- 领域标签: `Struct`, `Knowledge`, `Flink`
- 状态标签: `in-progress`, `needs-info`, `blocked`

## 📝 模板字段说明

### 文档改进请求

- **改进类型** - 内容错误、表述不清、缺少示例等
- **所属领域** - Struct/Knowledge/Flink
- **文件路径** - 需要改进的具体文件
- **定理/定义编号** - 如涉及特定形式化元素
- **当前内容** - 现有问题内容
- **建议改进** - 期望的改进方式
- **参考依据** - 支持建议的权威来源
- **优先级建议** - P0/P1/P2/P3

### 错误报告

- **错误类型** - 内容/引用/格式/定理问题等
- **所属领域** - 错误所在的领域
- **文件路径** - 包含错误的文件
- **错误描述** - 详细的问题描述
- **期望的正确内容** - 正确的表述
- **复现步骤** - 如适用
- **证据支持** - 证明错误的权威依据
- **严重程度** - 严重/重要/一般/微小

### 内容建议

- **建议类型** - 扩展现有/添加案例/改进示例等
- **目标领域** - 建议内容所属领域
- **目标文档** - 如针对特定文档
- **详细描述** - 建议内容详情
- **动机与背景** - 建议的重要性
- **内容大纲** - 初步的章节结构
- **参考资源** - 支持资源

### 新主题请求

- **主题标题** - 建议的新主题名称
- **建议所属目录** - Struct/Knowledge/Flink/新建
- **主题概述** - 核心内容和范围
- **与项目的相关性** - 为什么适合加入
- **内容大纲** - 详细的章节结构
- **前置知识要求** - 读者需要的准备知识
- **关键参考资料** - 学术论文、文档等

## 🛠️ 维护者指南

### 添加新模板

1. 创建新的 `.yml` 文件（使用数字前缀确保顺序）
2. 参考 [GitHub 文档](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
3. 测试表单渲染
4. 更新本 README

### 修改现有模板

1. 编辑对应的 `.yml` 文件
2. 在测试仓库验证表单
3. 提交 PR 并说明变更原因

## 🔗 相关资源

- [GitHub Issue 表单语法](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- [反馈分类指南](../feedback-templates/classification.md)
- [回复模板](../feedback-templates/thank-you.md)
- [项目贡献指南](../../CONTRIBUTING.md)

---

*模板设计遵循项目贡献规范*
