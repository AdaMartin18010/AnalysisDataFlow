# Iron Functions 版本跟踪

> **项目主页**: <https://irontools.dev>
> **文档**: <https://irontools.dev/docs/>
> **GitHub**: <https://github.com/irontools/iron-functions>
> **最后检查**: 2026-04-05

## 当前版本

- **最新版本**: 检查中...
- **文档版本**: 基于 2025-06 版本
- **状态**: ✅ 同步 / ⚠️ 需更新

## 版本历史

| 版本 | 发布日期 | 主要变更 | 文档影响 |
|------|----------|----------|----------|
| v0.x | 2025-06 | 初始版本 | 基准 |

## 跟踪检查清单

每月检查：

- [ ] 官网版本更新
- [ ] CLI工具新特性
- [ ] SDK API变更
- [ ] 支持语言扩展
- [ ] 性能优化公告

## 待同步项

- [ ] 验证当前文档准确性
- [ ] 跟踪 WASM 运行时更新
- [ ] 跟踪 Flink 兼容性更新

---

## 详细版本信息

### Iron Functions Core

| 组件 | 当前版本 | 最新版本 | 状态 |
|------|----------|----------|------|
| ironfun CLI | - | - | ⏳ 待检查 |
| Rust SDK | - | - | ⏳ 待检查 |
| Go SDK | - | - | ⏳ 待检查 |
| TypeScript SDK | - | - | ⏳ 待检查 |
| Flink Runtime Integration | - | - | ⏳ 待检查 |

### 依赖组件

| 依赖 | 当前版本 | 最新版本 | 影响等级 |
|------|----------|----------|----------|
| Extism PDK | 0.3.x | - | 高 |
| WebAssembly Runtime | - | - | 高 |
| Apache Flink | 1.18.x | - | 中 |

## 自动化检查

```bash
# 手动运行版本检查
python .scripts/iron-functions-tracker.py --check

# 生成同步建议
python .scripts/iron-functions-tracker.py --sync-advice

# 更新版本记录
python .scripts/iron-functions-tracker.py --update
```

## 变更通知

当检测到新版本时，自动创建 GitHub Issue：

- 标签: `external-dependency`, `iron-functions`
- 优先级根据变更影响等级确定

## 参考链接

- [Iron Functions 文档](https://irontools.dev/docs/)
- [GitHub Releases](https://github.com/irontools/iron-functions/releases)
- [Flink 兼容性矩阵](../00-MASTER-INDEX.md)
