# 维护减负脚本工具集

> 本地运行的文档维护工具，无需CI/CD，降低维护负担

## 快速开始

```bash
# 进入脚本目录
cd e:\_src\AnalysisDataFlow\.improvement-tracking\scripts

# 运行单个脚本
python find-orphaned-docs.py

# 或运行全部脚本生成综合报告
python maintenance-report-generator.py
```

## 脚本清单

| 脚本 | 功能 | 输出报告 |
|------|------|----------|
| `find-orphaned-docs.py` | 发现90天未修改的非核心文档 | `orphaned-docs-report.md` |
| `detect-duplicate-content.py` | 检测内容重复或相似的文档 | `duplicate-content-report.md` |
| `outdated-tech-check.py` | 检查技术版本是否过时 | `outdated-tech-report.md` |
| `quality-score-calculator.py` | 计算文档质量分数 | `quality-score-report.md` + `quality-scores.json` |
| `maintenance-report-generator.py` | 生成综合维护报告 | `B2-maintenance-report.md` |

## 脚本详情

### 1. find-orphaned-docs.py - 孤儿文档发现

**功能**: 找出90天未修改且不在核心层的文档

**核心逻辑**:
- 扫描所有 `.md` 文件
- 检查最后修改时间
- 排除 `Struct/`, `Knowledge/`, `Flink/` 核心目录
- 输出建议归档列表

**配置项** (在脚本内修改):
```python
DAYS_THRESHOLD = 90          # 闲置天数阈值
CORE_DIRECTORIES = ['Struct', 'Knowledge', 'Flink']  # 核心目录
```

**输出示例**:
```
📋 执行摘要
========================================
⚠️  发现 5 个文档建议归档
✅ 所有核心层文档都在维护周期内
```

---

### 2. detect-duplicate-content.py - 重复内容检测

**功能**: 检测内容重复或高度相似的文档

**算法**: Jaccard相似度 (k-gram shingle)

**检测类型**:
- 🔴 完全重复 (内容MD5相同)
- 🔴 高度相似 (≥80%)
- 🟡 中度相似 (60-80%)
- 🟢 部分相似 (40-60%)
- 📝 标题重复

**配置项**:
```python
SIMILARITY_THRESHOLD = 0.7   # 相似度阈值
PARTIAL_THRESHOLD = 0.4      # 部分相似阈值
```

**输出示例**:
```
📋 执行摘要
========================================
⚠️  发现 12 个问题:
   - 完全重复: 2 组
   - 内容相似: 5 高 / 3 中 / 2 低
```

---

### 3. outdated-tech-check.py - 版本过时检查

**功能**: 检查文档中的技术版本是否过时

**支持的技术栈**:
- Flink (从GitHub API获取最新版本)
- Java
- Scala
- Python
- Kafka
- Kubernetes
- Docker
- Maven
- Gradle

**版本状态判定**:
- 🔴 严重过时: 主版本落后或次版本落后超过2
- 🟡 需要关注: 次版本落后1-2
- ✅ 当前版本: 与最新版本一致

**输出示例**:
```
📡 获取最新版本信息...
   ✓ 从GitHub获取到Flink最新版本: 1.20.0
   
📊 分析版本状态...
   🔴 严重过时: 8 处
   🟡 需要关注: 15 处
   ✅ 当前版本: 42 处
```

---

### 4. quality-score-calculator.py - 质量分数计算

**功能**: 为每篇文档计算质量分数

**评分维度**:

| 维度 | 权重 | 评估要点 |
|------|------|----------|
| 完整性 | 35% | 字数、定义/定理数、示例数 |
| 时效性 | 25% | 最后修改时间 |
| 引用质量 | 20% | 引用标记数、外部链接数 |
| 结构规范 | 20% | 六段式结构、Mermaid图、表格 |

**分数等级**:
- A级 (优秀): ≥85分
- B级 (良好): 70-84分
- C级 (及格): 50-69分
- D级 (不及格): <50分

**输出**:
- Markdown报告: 质量分布、高分/低分文档排行
- JSON数据: 详细评分数据，可导入其他工具

---

### 5. maintenance-report-generator.py - 综合报告生成

**功能**: 运行所有脚本并生成综合维护报告

**报告内容**:
1. 文档资产统计 (数量、形式化元素)
2. 维护问题汇总 (孤儿、重复、过时、质量)
3. 问题热力图 (可视化问题分布)
4. 维护行动清单 (立即/短期/中期)
5. 自动化脚本使用指南

**使用场景**: 定期全面健康检查

---

## 使用模式

### 模式一：日常快速检查

```bash
# 只检查是否有孤儿文档
python find-orphaned-docs.py
```

### 模式二：深度维护

```bash
# 运行所有检查
python maintenance-report-generator.py

# 查看生成的 B2-maintenance-report.md
```

### 模式三：定时自动化

**Linux/Mac (crontab)**:
```bash
# 每月1日凌晨执行
0 0 1 * * cd /path/to/project && python .improvement-tracking/scripts/maintenance-report-generator.py
```

**Windows (任务计划程序)**:
1. 创建基本任务
2. 触发器: 每月
3. 操作: 启动程序
4. 程序: `python`
5. 参数: `.improvement-tracking\scripts\maintenance-report-generator.py`
6. 起始于: `e:\_src\AnalysisDataFlow`

---

## 集成到工作流

### Git Pre-commit Hook

创建 `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "🔍 运行文档质量检查..."

cd "$(git rev-parse --show-toplevel)"
python .improvement-tracking/scripts/quality-score-calculator.py

# 检查是否有D级文档
if [ -f .improvement-tracking/quality-score-report.md ]; then
    POOR_COUNT=$(grep -c "D级" .improvement-tracking/quality-score-report.md || echo 0)
    if [ "$POOR_COUNT" -gt 0 ]; then
        echo "⚠️  警告: 存在质量不及格的文档，请检查 quality-score-report.md"
        # 如需阻止提交，取消下一行的注释
        # exit 1
    fi
fi

echo "✅ 检查完成"
```

Windows 批处理版本 `.git/hooks/pre-commit.bat`:

```batch
@echo off
echo 🔍 运行文档质量检查...

cd /d "%~dp0\..\.."
python .improvement-tracking\scripts\quality-score-calculator.py

echo ✅ 检查完成
```

---

## 自定义配置

### 修改评分权重

编辑 `quality-score-calculator.py`:

```python
WEIGHTS = {
    'completeness': 0.40,    # 提高完整性权重
    'freshness': 0.20,       # 降低时效性权重
    'references': 0.20,
    'structure': 0.20
}
```

### 修改时间阈值

编辑 `find-orphaned-docs.py`:

```python
DAYS_THRESHOLD = 180  # 改为180天
```

### 添加新的技术栈检测

编辑 `outdated-tech-check.py`:

```python
VERSION_PATTERNS = {
    # 添加新的技术
    'Spark': [
        r'Spark\s+([0-9]+\.[0-9]+)',
        r'spark-([0-9]+\.[0-9]+)',
    ],
    # ...
}

DEFAULT_LATEST_VERSIONS = {
    # 添加最新版本
    'Spark': '3.5.0',
    # ...
}
```

---

## 报告文件位置

所有报告输出到 `.improvement-tracking/` 目录:

```
.improvement-tracking/
├── scripts/
│   ├── README.md                       # 本文件
│   ├── find-orphaned-docs.py
│   ├── detect-duplicate-content.py
│   ├── outdated-tech-check.py
│   ├── quality-score-calculator.py
│   └── maintenance-report-generator.py
│
├── orphaned-docs-report.md             # 孤儿文档报告
├── duplicate-content-report.md         # 重复内容报告
├── outdated-tech-report.md             # 版本过时报告
├── quality-score-report.md             # 质量分数报告
├── quality-scores.json                 # 质量分数JSON数据
└── B2-maintenance-report.md            # 综合维护报告
```

---

## 故障排除

### 脚本运行缓慢

- `detect-duplicate-content.py` 在大文档库上可能较慢，这是正常的
- 相似度计算是 O(n²) 复杂度
- 建议：在较小范围内先测试

### 中文显示乱码

Windows PowerShell:
```powershell
chcp 65001  # 设置UTF-8编码
```

### 无法获取Flink最新版本

- 检查网络连接
- GitHub API有速率限制
- 脚本会自动回退到硬编码的默认版本

### Python版本要求

- Python 3.7+
- 无需安装第三方包

---

## 开发计划

未来可能的增强:

- [ ] 增量检查模式（只检查修改过的文件）
- [ ] 配置外部化（支持配置文件）
- [ ] 历史趋势图表
- [ ] Web可视化界面
- [ ] 更多技术栈版本检测
- [ ] 链接健康检查集成

---

## 贡献

如需修改脚本:

1. 保持纯Python标准库，避免外部依赖
2. 保持输出格式一致
3. 更新本README文档
4. 测试所有使用场景

---

**最后更新**: 2026-04-05
