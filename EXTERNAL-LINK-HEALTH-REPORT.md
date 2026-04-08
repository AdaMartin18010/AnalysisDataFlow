# 外部链接健康检测报告

> 生成时间: 2026-04-08 15:19:43
> 检测链接总数: 200
> 缓存有效期: 24 小时

## 📊 检测统计

| 指标 | 数量 | 百分比 |
|------|------|--------|
| 总链接数 | 200 | 100% |
| ✅ 可访问 | 199 | 99.5% |
| ❌ 失效 | 1 | 0.5% |
| 🔄 301重定向 | 0 | 0.0% |

### 按优先级分布

| 优先级 | 数量 | 可访问 | 失效 |
|--------|------|--------|------|
| 🔴 核心 (高) | 9 | 9 | 0 |
| 🟡 中等 | 191 | 190 | 1 |
| 🟢 低 | 0 | 0 | 0 |

## 🔴 核心链接状态

| 链接 | 状态 | HTTP | 响应时间 | 源文件 |
|------|------|------|----------|--------|
| [https://issues.apache.org/jira/browse/FLINK-36556...](https://issues.apache.org/jira/browse/FLINK-36556) | ✅ | 200 | 792ms | Flink\02-core\backpressure-and-flow-cont |
| [https://issues.apache.org/jira/browse/FLINK-7282...](https://issues.apache.org/jira/browse/FLINK-7282) | ✅ | 200 | 618ms | Flink\02-core\backpressure-and-flow-cont |
| [https://nightlies.apache.org/flink/...](https://nightlies.apache.org/flink/) | ✅ | 200 | 792ms | docs\i18n\en\05-LEARNING-PATH.md, LEARNI |
| [https://nightlies.apache.org/flink/flink-docs-stable/docs/de...](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/memory/network_mem_tuning/) | ✅ | 200 | 874ms | Flink\02-core\backpressure-and-flow-cont |
| [https://nightlies.apache.org/flink/flink-docs-stable/docs/de...](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/) | ✅ | 200 | 979ms | Knowledge\09-anti-patterns\streaming-ant |
| [https://nightlies.apache.org/flink/flink-docs-stable/docs/le...](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/) | ✅ | 200 | 833ms | visuals\selection-tree-consistency.md, S |
| [https://nightlies.apache.org/flink/flink-docs-stable/docs/op...](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/metrics/) | ✅ | 200 | 784ms | Flink\02-core\backpressure-and-flow-cont |
| [https://nightlies.apache.org/flink/flink-docs-stable/docs/op...](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/monitoring/back_pressure/) | ✅ | 200 | 719ms | Flink\02-core\backpressure-and-flow-cont |
| [https://nightlies.apache.org/flink/flink-docs-stable/docs/op...](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpointing_under_backpressure/) | ✅ | 200 | 711ms | Flink\09-practices\09.03-performance-tun |

## ❌ 失效链接清单

| 链接 | HTTP | 错误信息 | 源文件 | 建议操作 |
|------|------|----------|--------|----------|
| [https://gist.github.com/sindresorhus/a39789f98801d...](https://gist.github.com/sindresorhus/a39789f98801d908bbc7ff3ecc99d99c) | N/A | 连接超时 | learning-platform\node_modules | [Archive备份](https://web.archive.org/web/*/https://gist.github.com/sindresorhus/a39789f98801d908bbc7ff3ecc99d99c) |

## 🐌 响应缓慢的链接 (>5s)

| 链接 | 响应时间 | 源文件 |
|------|----------|--------|
| [https://github.com/inspect-js/is-symbol/compare/v1...](https://github.com/inspect-js/is-symbol/compare/v1.1.0...v1.1.1) | 15.1s | learning-platform\node_modules |
| [https://github.com/inspect-js/is-symbol/commit/3ab...](https://github.com/inspect-js/is-symbol/commit/3ab2748ab6c2de21fc24f131bb880c68ba0b7b34) | 10.3s | learning-platform\node_modules |
| [https://github.com/inspect-js/is-symbol/commit/042...](https://github.com/inspect-js/is-symbol/commit/042fb3aec590f0c0d205b15812b285ad95cfff6b) | 8.4s | learning-platform\node_modules |
| [https://github.com/inspect-js/is-symbol/commit/acf...](https://github.com/inspect-js/is-symbol/commit/acf85f027ec6ea70a7023646c47f9324ff9a5e25) | 6.9s | learning-platform\node_modules |
| [https://github.com/inspect-js/is-symbol/commit/518...](https://github.com/inspect-js/is-symbol/commit/51808a55f272023201f40a59b2459ec6305bf73a) | 6.8s | learning-platform\node_modules |
| [https://github.com/inspect-js/is-symbol/commit/892...](https://github.com/inspect-js/is-symbol/commit/892d92e7c40f3c0577583a98134106181c38bb7e) | 6.3s | learning-platform\node_modules |
| [https://github.com/inspect-js/is-symbol/commit/07f...](https://github.com/inspect-js/is-symbol/commit/07f36476b69e98353c09dc58cbcab8891e3ed2b7) | 6.0s | learning-platform\node_modules |
| [https://github.com/inspect-js/is-symbol/commit/5c3...](https://github.com/inspect-js/is-symbol/commit/5c332fc92cecbed4a2041bc0c52b991b4a593f34) | 5.5s | learning-platform\node_modules |

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
