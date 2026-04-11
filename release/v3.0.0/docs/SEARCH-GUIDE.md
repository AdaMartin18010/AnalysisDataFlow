# AnalysisDataFlow 搜索使用指南

> **版本**: v1.0 | **更新日期**: 2026-04-03 | **适用范围**: 全项目文档搜索

---

## 目录

- [AnalysisDataFlow 搜索使用指南](#analysisdataflow-搜索使用指南)
  - [目录](#目录)
  - [1. 快速开始](#1-快速开始)
    - [1.1 构建索引](#11-构建索引)
    - [1.2 基本搜索](#12-基本搜索)
  - [2. 搜索语法](#2-搜索语法)
    - [2.1 关键词搜索](#21-关键词搜索)
    - [2.2 定理编号搜索](#22-定理编号搜索)
    - [2.3 多关键词搜索](#23-多关键词搜索)
    - [2.4 路径搜索](#24-路径搜索)
  - [3. 高级搜索技巧](#3-高级搜索技巧)
    - [3.1 分类过滤](#31-分类过滤)
    - [3.2 形式化元素类型过滤](#32-形式化元素类型过滤)
    - [3.3 组合条件搜索](#33-组合条件搜索)
  - [4. 搜索结果解读](#4-搜索结果解读)
  - [5. 实用示例](#5-实用示例)
    - [5.1 查找特定定理](#51-查找特定定理)
    - [5.2 查找相关概念](#52-查找相关概念)
    - [5.3 查找技术实现](#53-查找技术实现)
    - [5.4 浏览文档详情](#54-浏览文档详情)
  - [6. 故障排除](#6-故障排除)
    - [问题：索引文件不存在](#问题索引文件不存在)
    - [问题：搜索结果为空](#问题搜索结果为空)
    - [问题：搜索性能慢](#问题搜索性能慢)
  - [7. 索引维护](#7-索引维护)
    - [定期更新索引](#定期更新索引)
    - [查看索引统计](#查看索引统计)
    - [脚本集成](#脚本集成)

---

## 1. 快速开始

### 1.1 构建索引

在使用搜索功能之前，需要先构建搜索索引：

```bash
# 进入项目根目录
cd AnalysisDataFlow

# 构建搜索索引
python .vscode/build-search-index.py

# 显示详细日志
python .vscode/build-search-index.py --verbose

# 指定输出路径
python .vscode/build-search-index.py --output custom-index.json
```

索引构建完成后，会生成 `.vscode/search-index.json` 文件，包含：

- 所有 Markdown 文档的元数据
- 提取的定理/定义/引理编号
- 倒排索引（关键词 → 文档映射）

### 1.2 基本搜索

```bash
# 搜索关键词
python .vscode/search.py "checkpoint"

# 搜索定理编号
python .vscode/search.py "Thm-S-17-01"

# 显示帮助
python .vscode/search.py --help
```

---

## 2. 搜索语法

### 2.1 关键词搜索

支持中英文关键词搜索，系统自动进行分词和模糊匹配：

```bash
# 单个关键词
python .vscode/search.py "flink"
python .vscode/search.py "checkpoint"

# 中文关键词
python .vscode/search.py "一致性"

# 技术术语
python .vscode/search.py "exactly-once"
python .vscode/search.py "watermark"
```

**模糊匹配**：搜索 `check` 也会匹配到 `checkpoint`、`checking` 等相关词汇。

### 2.2 定理编号搜索

支持精确和模糊的形式化元素编号搜索：

```bash
# 精确搜索定理
python .vscode/search.py "Thm-S-17-01"

# 搜索定义
python .vscode/search.py "Def-S-17-01"

# 搜索引理
python .vscode/search.py "Lemma-S-17-01"

# 模糊搜索（匹配部分编号）
python .vscode/search.py "Thm-S-17"
```

**编号格式**：`{类型}-{阶段}-{文档序号}-{顺序号}`

| 类型 | 缩写 | 示例 |
|------|------|------|
| 定理 | Thm | `Thm-S-17-01` |
| 定义 | Def | `Def-S-17-01` |
| 引理 | Lemma | `Lemma-S-17-01` |
| 命题 | Prop | `Prop-S-02-01` |
| 推论 | Cor | `Cor-S-02-01` |

**阶段标识**：

- `S` - Struct/ 形式化理论
- `K` - Knowledge/ 知识结构
- `F` - Flink/ 技术实现

### 2.3 多关键词搜索

支持多个关键词组合搜索：

```bash
# OR 模式（默认）：匹配任意关键词
python .vscode/search.py "checkpoint exactly-once"

# AND 模式：必须匹配所有关键词
python .vscode/search.py "checkpoint exactly-once" --operator AND

# 限制结果数量
python .vscode/search.py "flink" --limit 10
```

### 2.4 路径搜索

按文档路径进行搜索：

```bash
# 搜索特定目录下的文档
python .vscode/search.py "04-proofs" --path

# 搜索特定文件
python .vscode/search.py "checkpoint-correctness" --path
```

---

## 3. 高级搜索技巧

### 3.1 分类过滤

按文档分类进行过滤：

```bash
# 只搜索 Struct/ 目录
python .vscode/search.py "theorem" --category Struct

# 只搜索 Knowledge/ 目录
python .vscode/search.py "design pattern" --category Knowledge

# 只搜索 Flink/ 目录
python .vscode/search.py "checkpoint" --category Flink

# 只搜索根目录文档
python .vscode/search.py "registry" --category Root
```

**分类说明**：

| 分类 | 说明 | 典型内容 |
|------|------|----------|
| Struct | 形式化理论 | 定理证明、数学模型、形式化定义 |
| Knowledge | 知识结构 | 设计模式、业务场景、技术选型 |
| Flink | 技术实现 | Flink 架构、API、案例研究 |
| Root | 根目录 | 索引文件、注册表、项目文档 |

### 3.2 形式化元素类型过滤

按形式化元素类型过滤：

```bash
# 只搜索定理
python .vscode/search.py "watermark" --type theorem

# 只搜索定义
python .vscode/search.py "checkpoint" --type definition

# 只搜索引理
python .vscode/search.py "consistency" --type lemma

# 只搜索命题
python .vscode/search.py "safety" --type proposition
```

### 3.3 组合条件搜索

支持多种条件组合：

```bash
# Flink 目录中关于 checkpoint 的定理
python .vscode/search.py "checkpoint" --category Flink --type theorem

# Struct 目录中包含 "exactly-once" 和 "consistency" 的文档
python .vscode/search.py "exactly-once consistency" --category Struct --operator AND

# 显示相关形式化元素
python .vscode/search.py "actor" --show-formal

# 禁用高亮（适合脚本使用）
python .vscode/search.py "flink" --no-highlight
```

---

## 4. 搜索结果解读

搜索结果的显示格式：

```
══════════════════════════════════════════════════════════════════════
 找到 3 个结果
══════════════════════════════════════════════════════════════════════

1. Flink Checkpoint 一致性正确性证明 [0.9520]
   📄 Struct/04-proofs/04.01-flink-checkpoint-correctness.md [Struct]
   🔑 匹配: checkpoint, flink
   💡 ...异步屏障快照算法下，Flink 能够产生一致的分布式状态快照...

2. Flink/ 技术实现索引 [0.6520]
   📄 Flink/00-INDEX.md [Flink]
   🔑 匹配: flink
   💡 ...涵盖 Flink 架构设计、核心机制（Checkpoint、Watermark、Exactly-Once）...
```

**结果字段说明**：

| 字段 | 说明 |
|------|------|
| `1. 2. 3.` | 结果序号 |
| `[0.9520]` | 相关性得分（0-1，越高越相关） |
| `📄` | 文档路径 |
| `[Struct]` | 文档分类 |
| `🔑 匹配` | 匹配到的关键词 |
| `💡` | 内容高亮片段 |

**查看文档详情**：

```bash
# 查看指定文档的详细信息
python .vscode/search.py --doc "Struct/04-proofs/04.01-flink-checkpoint-correctness.md"
```

输出包括：

- 文档标题和元数据
- 关键词列表
- 完整摘要
- 包含的形式化元素
- 文档结构（标题层级）

---

## 5. 实用示例

### 5.1 查找特定定理

```bash
# 查找 Checkpoint 相关定理
python .vscode/search.py "checkpoint" --type theorem --show-formal

# 查找特定编号定理
python .vscode/search.py "Thm-S-17-01" --show-formal

# 查找 Struct 目录下的所有定理
python .vscode/search.py "Thm-S" --path
```

### 5.2 查找相关概念

```bash
# 查找一致性相关的所有文档
python .vscode/search.py "consistency" --limit 10

# 查找 Actor 模型的相关内容
python .vscode/search.py "actor" --show-formal

# 查找进程演算相关内容
python .vscode/search.py "process calculus" --operator AND
```

### 5.3 查找技术实现

```bash
# 查找 Flink 核心技术
python .vscode/search.py "checkpoint watermark exactly-once" --category Flink

# 查找 Flink SQL 相关内容
python .vscode/search.py "sql" --category Flink

# 查找案例研究
python .vscode/search.py "case study" --path
```

### 5.4 浏览文档详情

```bash
# 查看定理注册表
python .vscode/search.py --doc "THEOREM-REGISTRY.md"

# 查看索引文件
python .vscode/search.py --doc "Struct/00-INDEX.md"

# 查看项目跟踪
python .vscode/search.py --doc "PROJECT-TRACKING.md"
```

---

## 6. 故障排除

### 问题：索引文件不存在

```
错误: 索引文件不存在: .vscode/search-index.json
请先运行: python .vscode/build-search-index.py
```

**解决方案**：

```bash
python .vscode/build-search-index.py
```

### 问题：搜索结果为空

**可能原因**：

1. 索引未更新，需要重新构建
2. 关键词拼写错误
3. 搜索条件过于严格

**解决方案**：

```bash
# 重新构建索引
python .vscode/build-search-index.py

# 尝试模糊匹配
python .vscode/search.py "checkpiont"  # 拼写错误也能匹配

# 放宽搜索条件
python .vscode/search.py "flink" --operator OR
```

### 问题：搜索性能慢

**解决方案**：

```bash
# 限制结果数量
python .vscode/search.py "flink" --limit 10

# 禁用模糊匹配
python .vscode/search.py "checkpoint" --no-fuzzy
```

---

## 7. 索引维护

### 定期更新索引

建议在进行以下操作后更新索引：

- 新增或修改文档
- 添加新的定理/定义
- 重构文档结构

```bash
# 更新索引
python .vscode/build-search-index.py

# 提交到版本控制
git add .vscode/search-index.json
git commit -m "更新搜索索引"
```

### 查看索引统计

```bash
python .vscode/search.py --stats
```

输出示例：

```
==================================================
📊 索引统计信息
==================================================
文档总数: 238
形式化元素: 870
索引条目: 5624

📁 分类分布:
  - Flink: 130
  - Knowledge: 66
  - Root: 14
  - Struct: 28

📐 形式化元素类型:
  - theorem: 188
  - definition: 399
  - lemma: 158
  - proposition: 121
  - corollary: 4
```

### 脚本集成

在 CI/CD 或自动化脚本中使用：

```bash
# JSON 输出（适合脚本解析）
python .vscode/search.py "checkpoint" --json > results.json

# 禁用颜色和高亮
python .vscode/search.py "flink" --no-highlight --no-fuzzy
```

---

**提示**: 搜索索引是项目知识管理的重要工具。建议经常使用搜索功能快速定位所需内容，提高文档使用效率。
