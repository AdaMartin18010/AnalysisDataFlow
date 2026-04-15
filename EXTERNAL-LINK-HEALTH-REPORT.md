# 外部链接健康检测报告

> 生成时间: 2026-04-16 00:03:38
> 检测链接总数: 20
> 缓存有效期: 24 小时

## 📊 检测统计

| 指标 | 数量 | 百分比 |
|------|------|--------|
| 总链接数 | 20 | 100% |
| ✅ 可访问 | 15 | 75.0% |
| ❌ 失效 | 5 | 25.0% |
| 🔄 301重定向 | 0 | 0.0% |

### 按优先级分布

| 优先级 | 数量 | 可访问 | 失效 |
|--------|------|--------|------|
| 🔴 核心 (高) | 7 | 6 | 1 |
| 🟡 中等 | 2 | 0 | 2 |
| 🟢 低 | 11 | 9 | 2 |

## 🔴 核心链接状态

| 链接 | 状态 | HTTP | 响应时间 | 源文件 |
|------|------|------|----------|--------|
| [https://archive.org/web/*/https://nightlies.apache.org/flink...](https://archive.org/web/*/https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/dev/datastream/fault-tolerance/queryable_state/) | ❌ | N/A | 10776ms | Flink\02-core\flink-state-management-com |
| [https://github.com/apache/flink...](https://github.com/apache/flink) | ✅ | 200 | 3404ms | Flink\00-meta\version-tracking.md, relea |
| [https://github.com/apache/flink/releases...](https://github.com/apache/flink/releases) | ✅ | 200 | 1149ms | Flink\00-meta\version-tracking.md, Flink |
| [https://nightlies.apache.org/flink/flink-docs-stable/...](https://nightlies.apache.org/flink/flink-docs-stable/) | ✅ | 200 | 3354ms | release\v3.0.0\docs\i18n\ja\README-ja.md |
| [https://nightlies.apache.org/flink/flink-docs-stable/docs/co...](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/flink-architecture/) | ✅ | 200 | 1264ms | Flink\10-internals\jobmanager-source-ana |
| [https://nightlies.apache.org/flink/flink-docs-stable/docs/de...](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/security/) | ✅ | 200 | 2047ms | formal-methods\Knowledge\en\16-security. |
| [https://nightlies.apache.org/flink/flink-docs-stable/docs/op...](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/state_backends/) | ✅ | 200 | 1068ms | Flink\02-core\flink-state-management-com |

## ❌ 失效链接清单

| 链接 | HTTP | 错误信息 | 源文件 | 建议操作 |
|------|------|----------|--------|----------|
| [https://archive.org/web/*/https://nightlies.apache...](https://archive.org/web/*/https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/dev/datastream/fault-tolerance/queryable_state/) | N/A | 连接超时 | Flink\02-core\flink-state-mana | [Archive备份](https://web.archive.org/web/*/https://archive.org/web/*/https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/dev/datastream/fault-tolerance/queryable_state/) |
| [https://github.com/your-org/AnalysisDataFlow...](https://github.com/your-org/AnalysisDataFlow) | 404 | HTTP 404 | RELEASE-NOTES-v5.0.0-DRAFT.md, | [Archive备份](https://web.archive.org/web/*/https://github.com/your-org/AnalysisDataFlow) |
| [https://github.com/luyanfeng/AnalysisDataFlow/acti...](https://github.com/luyanfeng/AnalysisDataFlow/actions/workflows/pr-quality-gate.yml/badge.svg) | 404 | HTTP 404 | release\v3.0.0\docs\i18n\ja\RE | [Archive备份](https://web.archive.org/web/*/https://github.com/luyanfeng/AnalysisDataFlow/actions/workflows/pr-quality-gate.yml/badge.svg) |
| [https://en.wikipedia.org/wiki/Category_theory...](https://en.wikipedia.org/wiki/Category_theory) | N/A | 连接超时 | formal-methods\98-appendices\w | [Archive备份](https://web.archive.org/web/*/https://en.wikipedia.org/wiki/Category_theory) |
| [https://cert.analysisdataflow.org/verify...](https://cert.analysisdataflow.org/verify) | N/A | 客户端错误: Cannot connect to host  | docs\certification\csa\exam-gu | [Archive备份](https://web.archive.org/web/*/https://cert.analysisdataflow.org/verify) |

## 🐌 响应缓慢的链接 (>5s)

| 链接 | 响应时间 | 源文件 |
|------|----------|--------|
| [https://cheatsheetseries.owasp.org/cheatsheets/Tra...](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html) | 9.0s | formal-methods\Knowledge\en\16 |

## 🔧 修复建议

### 自动修复

运行自动修复脚本更新301重定向：
```bash
python .scripts/fix-external-links.py --mode fix-redirects
```

### 手动修复

1. **失效链接**: 使用Archive.org备份或寻找替代链接
2. **404错误**: 检查链接是否拼写正确
3. **超时链接**: 可能是暂时性问题，稍后重试

### Archive.org备份

对于失效链接，可以使用以下方式查找备份：
- 直接访问: `https://web.archive.org/web/*/{URL}`
- 使用工具批量查询: `python .scripts/fix-external-links.py --mode find-archive`
