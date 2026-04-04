# 📊 社区反馈报告

本目录包含 AnalysisDataFlow 项目的社区反馈统计报告。

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `monthly-report-YYYY-MM.md` | 月度反馈报告 |
| `quarterly-report-YYYY-QX.md` | 季度反馈报告 |
| `high-priority-tasks.md` | 高优先级任务列表 |
| `feedback-stats.json` | 统计数据 JSON |
| `feedback-details.json` | 详细反馈数据 |
| `dashboard.html` | 可视化仪表板 |

## 📈 报告生成

### 自动报告

项目配置了 GitHub Actions 工作流，每月自动生成报告：

- 工作流文件: `.github/workflows/feedback-management.yml`
- 运行时间: 每月 1 日 00:00 UTC
- 自动提交到本目录

### 手动生成

```bash
# 生成完整报告
python .scripts/feedback-aggregator.py --full-analysis

# 仅月度报告
python .scripts/feedback-aggregator.py --monthly

# 指定时间范围
python .scripts/feedback-aggregator.py --since 2024-01-01
```

## 🎯 可视化仪表板

### 启动本地仪表板

```bash
# 生成并启动
python .scripts/feedback-dashboard.py

# 仅生成 HTML
python .scripts/feedback-dashboard.py --generate

# 指定端口
python .scripts/feedback-dashboard.py --serve --port 3000
```

### 仪表板功能

1. **关键指标** - 总反馈数、待处理、已解决、平均解决时间
2. **趋势图表** - 月度反馈提交趋势
3. **类型分析** - 错误报告、功能建议、文档改进分布
4. **优先级热力图** - P0-P3 优先级分布
5. **领域分布** - Struct/Knowledge/Flink 各领域反馈
6. **高优先级任务** - 待处理的 P0/P1 任务列表

## 📊 数据字段说明

### feedback-stats.json

```json
{
  "generated_at": "ISO 时间戳",
  "total_issues": "总 Issue 数",
  "open_issues": "开放 Issue 数",
  "closed_issues": "已关闭 Issue 数",
  "by_type": {
    "bug": "错误报告数",
    "enhancement": "功能建议数",
    "documentation": "文档改进数",
    "new-topic": "新主题请求数"
  },
  "by_priority": {
    "P0": "关键级数",
    "P1": "重要级数",
    "P2": "一般级数",
    "P3": "建议级数"
  },
  "by_category": {
    "Struct": "形式理论领域数",
    "Knowledge": "工程知识领域数",
    "Flink": "Flink 专项数"
  },
  "monthly_trend": {
    "YYYY-MM": "该月 Issue 数"
  },
  "avg_resolution_days": "平均解决天数"
}
```

## 🔗 相关链接

- [贡献指南](../../CONTRIBUTING.md)
- [反馈模板](../../.github/feedback-templates/)
- [Issue 列表](https://github.com/your-org/AnalysisDataFlow/issues)
- [贡献者列表](../../CONTRIBUTORS.md)

---

*报告由 GitHub Actions 自动生成*
