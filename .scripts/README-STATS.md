# update-stats.py 使用说明

## 概述

`update-stats.py` 是 AnalysisDataFlow 项目的文档统计自动更新脚本，用于收集、分析和更新项目统计信息。

## 功能特性

### 1. 文档统计
- 各目录文档数量统计 (Struct/, Knowledge/, Flink/, visuals/, tutorials/, LEARNING-PATHS/)
- 总文档数
- 总字节数和行数
- 代码示例数量

### 2. 形式化元素统计
- 定理 (Thm) 数量
- 定义 (Def) 数量
- 引理 (Lemma) 数量
- 命题 (Prop) 数量
- 推论 (Cor) 数量

### 3. 图表统计
- Mermaid图表数量
- 图片数量
- Markdown表格数量

### 4. 交叉引用统计
- 内部链接数量 (.md文件引用)
- 外部链接数量 (http/https链接)
- 锚点引用数量 (#锚点)

### 5. 自动更新
- 更新 README.md 统计信息
- 更新 PROJECT-TRACKING.md 进度数据
- 生成 .stats/project-stats.json 机器可读格式
- 更新 .stats/stats-history.json 历史记录
- 生成 .stats/STATISTICS-REPORT-GENERATED.md Markdown报告

### 6. 输出格式
- Markdown表格（人类可读）
- JSON机器可读格式
- 变更对比（与上次统计比较）

## 使用方法

### 基本使用

```bash
# 在项目根目录运行
python .scripts/update-stats.py

# 或在 .scripts 目录运行
cd .scripts
python update-stats.py
```

### 输出示例

```
============================================================
AnalysisDataFlow 文档统计更新
============================================================

📊 正在收集统计信息...
分析目录: struct...
分析目录: knowledge...
分析目录: flink...
分析目录: visuals...
分析目录: tutorials...
分析目录: learning_paths...

💾 保存统计JSON...
统计JSON已保存: E:\_src\AnalysisDataFlow\.stats\project-stats.json

📈 更新历史记录...
历史记录已更新: E:\_src\AnalysisDataFlow\.stats\stats-history.json

📝 生成Markdown报告...
Markdown报告已保存: E:\_src\AnalysisDataFlow\.stats\STATISTICS-REPORT-GENERATED.md

📄 更新 README.md...
README.md 已更新

📋 更新 PROJECT-TRACKING.md...
PROJECT-TRACKING.md 已更新

============================================================
统计摘要
============================================================
总文档数: 420
总大小: 12.98 MB
总行数: 388,787
形式化元素: 6,263
  - 定理: 1198
  - 定义: 3149
  - 引理: 1091
  - 命题: 785
  - 推论: 40
代码示例: 7118
Mermaid图表: 1774
...
```

## 输出文件

### 1. project-stats.json
机器可读的完整统计信息，包含：
- 时间戳和版本
- 总体统计摘要
- 各目录详细统计
- 形式化元素统计
- 链接统计

### 2. stats-history.json
历史记录数组，用于追踪项目增长趋势。

### 3. STATISTICS-REPORT-GENERATED.md
人类可读的Markdown格式报告，包含：
- 总体统计表格
- 形式化元素分布
- 各目录详细对比
- ASCII图表展示

### 4. README.md (自动更新)
更新项目概览中的统计数字。

### 5. PROJECT-TRACKING.md (自动更新)
更新项目进度看板中的统计信息。

## 统计检测规则

### 形式化元素识别
脚本通过以下模式识别形式化元素：
- **编号模式**: `Thm-S-01-01`, `Def-K-02-03`, `Prop-F-05-10` 等
- **标题模式**: `**定理**`, `## 定义`, `### 引理` 等

### 代码示例识别
- 代码块: ` ```language\ncode\n``` `
- 行内代码: `` `code` ``

### 图表识别
- Mermaid: ` ```mermaid\n...\n``` `
- 图片: `![alt](path)`
- 表格: Markdown表格语法

### 链接识别
- 内部链接: `[text](path.md)`
- 外部链接: `[text](http://...)`
- 锚点引用: `[text](#anchor)`

## 定时执行

可以通过 GitHub Actions 定时执行统计更新：

```yaml
name: Update Statistics
on:
  schedule:
    - cron: '0 0 * * *'  # 每天执行
  workflow_dispatch:  # 支持手动触发

jobs:
  update-stats:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Run stats update
        run: python .scripts/update-stats.py
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .
          git commit -m "Update project statistics" || exit 0
          git push
```

## 注意事项

1. **形式化元素计数**: 优先使用编号模式 (Thm-S-01-01) 进行计数，更准确
2. **历史记录**: 只保留最近30条历史记录
3. **文件编码**: 所有文件使用 UTF-8 编码
4. **备份**: 脚本会直接修改 README.md 和 PROJECT-TRACKING.md，建议提交前备份

## 故障排除

### 统计数字不准确
- 检查文档是否使用了标准的形式化元素编号格式
- 确认代码块使用了正确的 Markdown 语法

### 文件更新失败
- 确保脚本有文件写入权限
- 检查 README.md 和 PROJECT-TRACKING.md 是否存在

## 版本历史

- **v1.0.0** (2026-04-04): 初始版本
  - 支持6个目录的统计
  - 支持5种形式化元素
  - 支持3种图表类型
  - 支持3种链接类型
  - 自动更新3个文件
