# 感谢模板 (Thank You Templates)

本目录包含用于回复社区反馈的标准模板。

---

## 🙏 感谢提交 Issue

### 通用感谢

```markdown
Hi @{{username}},

感谢您对 AnalysisDataFlow 项目的贡献！🎉

我们已收到您的 {{issue_type}}，团队会在 **{{response_time}}** 内进行初步评估。

**Issue 信息摘要：**
- 编号: #{{issue_number}}
- 类型: {{type_label}}
- 优先级: {{priority}}
- 分类: {{category}}

在此期间，您可以：
- 补充更多细节或参考资料
- 关注此 Issue 的更新状态
- 查看我们的 [贡献指南](../../CONTRIBUTING.md) 了解更多信息

再次感谢您的参与！

---
*此回复为自动生成，如有疑问请联系维护团队。*
```

### 文档改进感谢

```markdown
Hi @{{username}},

非常感谢您提交的文档改进建议！📚

文档质量是我们项目的核心，您的反馈将帮助我们不断完善知识库。

**评估计划：**
- 初步评估: 3-5 个工作日
- 内容审查: 根据复杂度安排
- 实施更新: 确定方案后进行

如果您愿意直接提交 PR 修复，我们将非常欢迎！请参考 [文档贡献指南](../../CONTRIBUTING.md#11-文档改进)。

期待您的更多贡献！
```

### 错误报告感谢

```markdown
Hi @{{username}},

感谢您发现并报告这个问题！🐛

您的细致观察对维护项目质量非常重要。

**处理流程：**
1. 🔍 验证确认 (1-2 天)
2. 🔧 制定修复方案
3. ✅ 实施修复并验证
4. 📝 更新完成通知

**错误等级:** {{severity}}

我们会尽快处理，如有需要补充的信息会在此通知您。

感谢您的耐心！
```

---

## 🔄 处理进度更新

### 开始处理

```markdown
Hi @{{username}},

**更新: 您的 Issue #{{issue_number}} 已开始处理**

**当前状态:** 🔄 处理中

**负责人员:** @{{assignee}}

**计划时间线:**
- 分析阶段: {{analysis_date}}
- 实施阶段: {{implementation_date}}
- 验证阶段: {{verification_date}}
- 预计完成: {{completion_date}}

**下一步:**
{{next_steps}}

如有任何问题或建议，欢迎随时在此讨论！
```

### 需要更多信息

```markdown
Hi @{{username}},

感谢您提交的 Issue #{{issue_number}}。

在进一步处理之前，我们需要您补充以下信息：

**需要补充的内容：**
- [ ] {{info_request_1}}
- [ ] {{info_request_2}}
- [ ] {{info_request_3}}

**参考示例：**
```
{{example}}
```

请在方便时补充以上信息，这将帮助我们更快更好地解决问题。

**标签更新:** `needs-info` ⏳
```

### 处理受阻

```markdown
Hi @{{username}},

关于 Issue #{{issue_number}} 的进度更新：

**当前状态:** ⚠️ 处理受阻

**受阻原因:**
{{block_reason}}

**可能的解决方案:**
1. {{solution_1}}
2. {{solution_2}}
3. {{solution_3}}

**需要的帮助:**
{{help_needed}}

如果您有任何想法或建议，欢迎分享！
```

---

## ✅ 完成通知

### 已完成修复

```markdown
Hi @{{username}},

好消息！🎉 Issue #{{issue_number}} 已完成处理。

**完成摘要:**
- **处理方式:** {{resolution_type}}
- **相关提交:** {{commit_hash}}
- **相关 PR:** {{pr_number}}
- **文档更新:** {{doc_update}}

**变更详情:**
{{changes_description}}

**验证方式:**
{{verification_steps}}

感谢您的报告让项目变得更好！如果问题已解决，此 Issue 将在 7 天后自动关闭。如有后续问题，请随时 reopen。
```

### 已合并贡献

```markdown
Hi @{{username}},

恭喜！🎊 您的贡献已成功合并到主分支！

**贡献详情:**
- **类型:** {{contribution_type}}
- **合并提交:** {{merge_commit}}
- **影响范围:** {{impact_scope}}

**致谢:**
您的贡献已被记录在 [CONTRIBUTORS.md](../../CONTRIBUTORS.md) 中。

欢迎继续参与，期待您的下一个贡献！

---
*如果您希望获得贡献者徽章，请在 [Discussion #XXX](link) 中留言。*
```

### 作为已知问题关闭

```markdown
Hi @{{username}},

感谢您对 Issue #{{issue_number}} 的关注。

**处理决定:** 作为已知问题关闭

**原因说明:**
{{close_reason}}

**相关参考:**
- 类似 Issue: #{{related_issue}}
- 文档说明: [链接](url)
- 计划路线图: [ROADMAP.md](../../ROADMAP.md)

虽然此 Issue 被关闭，但您的反馈已被记录。如果未来情况发生变化，欢迎 reopen 或提交新的 Issue。

感谢您的理解！
```

### 无法复现/需要验证

```markdown
Hi @{{username}},

关于 Issue #{{issue_number}} 的状态更新：

**当前状态:** 🔍 需要验证

**说明:**
我们尝试了多种方式但未能复现您报告的问题：
- 测试环境: {{test_environment}}
- 测试版本: {{test_version}}
- 复现步骤: {{reproduction_steps}}

**请求协助:**
能否请您：
1. 确认问题在当前版本中是否仍然存在
2. 提供更详细的复现步骤
3. 分享您的环境配置

如果在 30 天内没有收到回复，此 Issue 将被标记为 `stale`。

感谢您的配合！
```

---

## 📋 快捷使用指南

### GitHub CLI 使用示例

```bash
# 回复感谢
github issue comment {{issue_number}} --body "$(cat .github/feedback-templates/thank-you.md | head -20)"

# 更新状态标签
github issue edit {{issue_number}} --add-label "in-progress" --remove-label "triage"

# 关闭 Issue
github issue close {{issue_number}} --comment "$(cat .github/feedback-templates/completed.md)"
```

### 自动化脚本使用

```python
from feedback_aggregator import FeedbackResponder

responder = FeedbackResponder()
responder.reply_thank_you(issue_number=123, username="contributor")
responder.update_progress(issue_number=123, status="in-progress")
responder.notify_completion(issue_number=123, resolution_type="fixed")
```

---

## 🏷️ 标签使用规范

| 标签 | 用途 | 对应模板 |
|------|------|----------|
| `triage` | 待分类评估 | 感谢模板 |
| `in-progress` | 处理中 | 进度更新 |
| `needs-info` | 需要补充信息 | 需要更多信息 |
| `blocked` | 处理受阻 | 处理受阻 |
| `completed` | 已完成 | 完成通知 |
| `wontfix` | 不修复 | 作为已知问题关闭 |
| `duplicate` | 重复 Issue | 引用相关 Issue |

---

*模板最后更新: 2026-04-04*
