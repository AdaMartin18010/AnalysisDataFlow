# AnalysisDataFlow 国际化 (i18n) 模块

本文档介绍 AnalysisDataFlow 项目的国际化架构和使用方法。

## 目录结构

```
docs/i18n/
├── ARCHITECTURE.md           # 国际化架构设计文档
├── README.md                 # 本文件
├── i18n-content/             # 多语言内容
│   ├── zh/                   # 中文（源语言）
│   ├── en/                   # 英文
│   └── ...
├── glossary/                 # 术语表
│   ├── core-terms.json       # 核心术语
│   └── prohibited-list.json  # 禁止翻译列表
├── workflows/                # 工作流状态
│   ├── translation-queue.json
│   └── version-lock.json
├── templates/                # 模板文件
└── config/                   # 配置
    └── i18n-config.yaml
```

## 快速开始

### 1. 查看翻译进度

```bash
python .scripts/i18n-manager.py stats --lang en
```

### 2. 提取待翻译内容

```bash
python .scripts/i18n-manager.py extract --source Struct/ --lang en --output translation-package.json
```

### 3. 检查缺失翻译

```bash
python .scripts/i18n-manager.py check-missing --lang en
```

### 4. 生成完整报告

```bash
python .scripts/i18n-manager.py report --output i18n-report.json
```

## 翻译工作流

1. **创建翻译任务**: 从待翻译队列中选择文档
2. **锁定原文**: 防止原文在翻译期间变更
3. **翻译文档**: 按照术语表和翻译规范进行翻译
4. **提交审核**: 完成翻译后提交三级审核
5. **审核通过**: 更新文档状态为 completed
6. **解除锁定**: 原文恢复可编辑状态

## 术语管理

- 核心术语表: `glossary/core-terms.json`
- 禁止翻译列表: `glossary/prohibited-list.json`

添加新术语时，请同时更新这两个文件。

## 翻译规范

1. 遵循文档六段式模板结构
2. 代码块和命令行保持原文
3. 产品名称和技术术语参考术语表
4. 首次出现的缩写需提供全称

## 状态说明

| 状态 | 说明 |
|------|------|
| `not_started` | 未开始翻译 |
| `in_progress` | 翻译中 |
| `pending_review` | 等待审核 |
| `completed` | 翻译完成 |
| `outdated` | 原文已更新，需要同步 |

## 更多资源

- [国际化架构设计](ARCHITECTURE.md)
- [术语表](glossary/core-terms.json)
- **工具帮助**（运行 `.scripts/i18n-manager.py --help`）
