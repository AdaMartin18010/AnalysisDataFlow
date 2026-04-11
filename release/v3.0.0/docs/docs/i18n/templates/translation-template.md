# 翻译模板

## 文件头部元数据

所有翻译文件必须包含以下 frontmatter：

```yaml
---
translation_status: "in_progress"  # not_started | in_progress | pending_review | completed
source_version: "abc123def456"     # 原文版本哈希
translator: "translator-id"        # 翻译者标识
reviewer: "reviewer-id"            # 审核者标识（翻译完成前可为空）
translated_at: "2026-04-04T15:26:26Z"
reviewed_at: null
completion_percentage: 0           # 完成百分比
---
```

## 翻译标记

### 段落级标记

```markdown
<!-- TRANSLATION_STATUS: pending -->
本节待翻译

<!-- TRANSLATION_STATUS: completed -->
本节翻译完成
```

### 术语标记

```markdown
<!-- TERM: checkpoint | 检查点 -->
A checkpoint is a consistent snapshot...
```

## 翻译规范

1. **标题层级**: 保持与原文一致
2. **代码块**: 完全保持原文，不翻译
3. **链接**: 更新为对应语言的相对链接
4. **图片**: 如无本地化版本，使用原文图片
5. **引用**: 保持原文引用格式

## 质量检查清单

- [ ] 所有标题已翻译
- [ ] 术语符合术语表
- [ ] 代码块未改动
- [ ] 链接有效
- [ ] 格式正确
- [ ] 通过术语检查
- [ ] 通过格式检查
