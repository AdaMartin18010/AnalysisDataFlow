# Flink 版本对比工具

Flink 版本对比工具包，提供多版本特性对比、差异报告生成、特性矩阵可视化等功能。

## 功能特性

- **版本对比** (`compare-versions.py`): 比较 Flink 2.4/2.5/3.0 特性，生成对比表格
- **差异报告** (`generate-diff-report.py`): 生成文档差异报告，高亮新增/修改/删除内容
- **特性矩阵** (`feature-matrix-generator.py`): 生成特性支持矩阵，支持多种输出格式
- **配置管理** (`config.yaml`): 集中管理版本配置、文档路径映射、输出格式配置

## 目录结构

```
.scripts/version-comparison/
├── README.md                      # 本文档
├── __init__.py                    # 包初始化
├── config.yaml                    # 配置文件
├── compare-versions.py            # 版本对比脚本
├── generate-diff-report.py        # 差异报告脚本
├── feature-matrix-generator.py    # 特性矩阵生成脚本
└── logs/                          # 日志目录（自动生成）
```

## 快速开始

### 1. 版本对比

```bash
# 对比默认版本 (2.4 vs 2.5 vs 3.0) 生成 Markdown 报告
python compare-versions.py

# 对比指定版本
python compare-versions.py --versions 2.4 2.5

# 生成 HTML 报告
python compare-versions.py --format html --output report.html

# 生成 JSON 数据
python compare-versions.py --format json
```

### 2. 文档差异报告

```bash
# 对比特定文档
python generate-diff-report.py --from 2.3 --to 2.4 --document checkpoint-mechanism

# 生成 HTML 报告
python generate-diff-report.py --from 2.4 --to 2.5 --document ai-agent --format html
```

### 3. 特性矩阵生成

```bash
# 生成 Markdown 矩阵
python feature-matrix-generator.py --versions 2.4 2.5 3.0

# 生成所有格式
python feature-matrix-generator.py --versions 2.4 2.5 3.0 --format all --output-dir ./reports

# 生成 Mermaid 演进图
python feature-matrix-generator.py --versions 2.4 2.5 3.0 --mermaid

# 生成 ASCII 热力图
python feature-matrix-generator.py --versions 2.4 2.5 3.0 --heatmap
```

## 配置说明

配置文件 `config.yaml` 包含以下主要配置项：

### 版本配置

```yaml
versions:
  "2.4":
    release_date: "2026-H2"
    status: "预览/开发"
    highlights:
      - "FLIP-531 GA (AI Agent正式版)"
      - "Serverless Flink"
  "2.5":
    release_date: "2027+"
    # ...
```

### 文档路径映射

```yaml
document_paths:
  tracking:
    "2.4": "Flink/08-roadmap/flink-2.4-tracking.md"
    "2.5": "Flink/08-roadmap/flink-2.5-preview.md"
    "3.0": "Flink/08-roadmap/flink-30-architecture-redesign.md"
```

### 特性分类

```yaml
feature_categories:
  - name: "核心API"
    id: "core_api"
    features:
      - id: "datastream_api"
        name: "DataStream API"
        description: "流处理核心API"
```

### 特性支持状态

```yaml
feature_matrix:
  version_features:
    "2.4":
      datastream_api: "supported"
      ai_agent: "supported"
      serverless: "preview"
    "2.5":
      datastream_api: "supported"
      ai_agent: "supported"
      serverless: "supported"
```

## 输出格式

### Markdown 格式

- 版本概览对比表
- 特性支持矩阵
- 版本亮点对比
- 变更详情
- Mermaid 架构演进图

### HTML 格式

- 响应式设计
- 表格样式美化
- 状态颜色标识
- 支持 Mermaid 图表渲染

### CSV 格式

- 可导入 Excel
- 便于数据分析
- 包含完整元数据

### JSON 格式

- 结构化数据
- 便于程序处理
- 包含详细元信息

## 特性状态符号

| 符号 | 状态 | 说明 |
|------|------|------|
| ✅ | supported | 完全支持 |
| 🚧 | preview | 预览版 |
| ⚠️ | deprecated | 已弃用 |
| ❌ | not_supported | 不支持 |
| 🔜 | planned | 规划中 |

## 扩展开发

### 添加新版本

1. 在 `config.yaml` 的 `versions` 部分添加新版本配置
2. 更新 `feature_matrix.version_features` 添加特性支持状态
3. 在 `document_paths.tracking` 中添加版本文档路径

### 添加新特性

1. 在 `feature_categories` 中添加新特性定义
2. 更新各版本的 `version_features` 配置
3. 重新运行矩阵生成命令

### 自定义输出格式

1. 继承 `VersionComparator` 类
2. 重写 `generate_*_report` 方法
3. 注册新的输出格式

## 依赖要求

- Python 3.8+
- PyYAML >= 5.0

可选依赖：
- Jinja2 (用于高级模板)
- pandas (用于数据分析)

## 注意事项

1. 确保配置文件路径正确
2. 版本文档需要遵循项目文档规范
3. 特性ID需要全局唯一
4. 生成报告前建议更新配置文件

## 相关文档

- [Flink 版本对比矩阵](../../Flink/08-roadmap/flink-version-comparison-matrix.md)
- [Flink 版本演进完整指南](../../Flink/08-roadmap/flink-version-evolution-complete-guide.md)
- [Flink 2.4 跟踪文档](../../Flink/08-roadmap/flink-2.4-tracking.md)
- [Flink 2.5 预览](../../Flink/08-roadmap/flink-2.5-preview.md)
- [Flink 3.0 架构设计](../../Flink/08-roadmap/flink-30-architecture-redesign.md)

## 更新日志

### v1.0.0 (2026-04-04)

- 初始版本发布
- 支持 Flink 2.4/2.5/3.0 版本对比
- 支持 Markdown/HTML/CSV/JSON 输出格式
- 支持文档差异分析
- 支持特性矩阵可视化

## License

本项目遵循 Apache Flink 项目的开源协议。
