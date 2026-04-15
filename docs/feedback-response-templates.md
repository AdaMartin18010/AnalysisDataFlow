# 反馈响应模板

> 所属阶段: 社区运营 | 前置依赖: [反馈处理流程](./feedback-handling-process.md) | 形式化等级: L2

本文档提供标准化的反馈响应模板，确保与用户的沟通专业、礼貌且有效。

---

## 使用指南

### 模板选择原则

| 场景 | 推荐模板 |
|------|----------|
| 首次收到反馈 | 感谢模板 |
| 需要确认问题 | 问题确认模板 |
| 已解决问题 | 解决方案模板 |
| 长期跟踪问题 | 跟进模板 |
| 反馈无法处理 | 婉拒模板 |

### 个性化原则

- 使用用户的名字（如果可知）
- 引用反馈中的具体内容
- 根据实际情况调整语气和内容
- 保持专业但友好的态度

---

## 1. 感谢模板

### 1.1 标准感谢

```markdown
Hi @{username},

感谢您抽出宝贵时间为我们提供反馈！🙏

我们已收到您的建议/报告,并已将此 Issue 标记为 `[appropriate label]`。
我们的团队将在 [timeframe] 内进行审核,并及时向您更新进展。

您的意见对改进项目质量至关重要,我们非常重视每一位用户的体验。

如有任何补充信息,欢迎随时在此 Issue 中回复。

再次感谢！

Best regards,
{team_name}
```

### 1.2 详细内容反馈感谢

```markdown
Hi @{username},

非常感谢您如此详细的反馈！👏

您对 [specific content] 的观察非常敏锐,这确实是我们需要关注的重要方面。

我们已将您的反馈分类为 `[category]`,并分配了 `[priority]` 优先级。
处理负责人:@{handler}

我们计划在 [timeframe] 内开始处理,届时会在此 Issue 中更新进展。

再次感谢您的宝贵时间和专业建议！

Best regards,
{team_name}
```

### 1.3 首次贡献者特别感谢

```markdown
Hi @{username},

欢迎参与社区！🎉

感谢您作为新贡献者为我们提供反馈。这是您第一次在此项目中提交 Issue,我们非常珍视这份信任。

我们已收到您的反馈,并将尽快进行处理。您可以期待:
- 48 小时内的首次回复
- 定期的进展更新
- 解决后的效果确认

如果您有任何疑问,随时 @ 我们！

Best regards,
{team_name}
```

---

## 2. 问题确认模板

### 2.1 信息确认请求

```markdown
Hi @{username},

感谢您报告这个问题！

为了帮助我们更好地理解和解决这个问题,能否请您提供以下信息:

1. **重现步骤**: 如何重现您遇到的问题？
2. **环境信息**: 您使用的浏览器/操作系统版本？
3. **预期行为**: 您期望看到什么？
4. **实际行为**: 实际发生了什么？
5. **截图/日志**: 如果有相关截图或错误日志,请一并提供

您提供的详细信息越多,我们越能快速定位和解决问题。

期待您的回复！

Best regards,
{team_name}
```

### 2.2 问题理解与复述

```markdown
Hi @{username},

感谢您的反馈！为了确保我们正确理解了您的问题,请允许我复述一下:

**您遇到的问题是**:
[paraphrased problem description]

**您期望的解决方案是**:
[expected solution]

**这对您的影响是**:
[impact on user's work]

请问我的理解正确吗？如果有任何不准确的地方,请随时指出。

确认后我们将立即开始处理。

Best regards,
{team_name}
```

### 2.3 相似问题关联

```markdown
Hi @{username},

感谢您的反馈！

在审核过程中,我们发现这个问题与以下已有 Issue 可能存在关联:

- #{related_issue_1} - [简要描述]
- #{related_issue_2} - [简要描述]

**请问**:
1. 这些 Issue 描述的是否是您遇到的问题？
2. 如果是,您是否有额外的信息可以补充？
3. 如果不是,请告诉我们具体差异在哪里

这样我们可以更好地分类和处理您的反馈。

Best regards,
{team_name}
```

---

## 3. 解决方案模板

### 3.1 问题已修复

```markdown
Hi @{username},

好消息！🎉 您报告的问题已经修复。

**修复详情**:
- 问题原因: [root cause]
- 修复方案: [solution description]
- 相关提交: [commit/PR link]

**您可以这样验证修复效果**:
1. [verification step 1]
2. [verification step 2]
3. [verification step 3]

请在方便的时候验证一下,确认问题是否已完全解决。
如果仍有问题,请随时在此 Issue 中回复。

感谢您的耐心等待和宝贵反馈！

Best regards,
{team_name}
```

### 3.2 功能已实现

```markdown
Hi @{username},

您建议的功能已经实现！✨

**实现详情**:
- 功能名称: [feature name]
- 实现方式: [implementation description]
- 使用文档: [documentation link]
- 相关 PR: [PR link]

**如何使用**:
```

[usage example]

```

我们希望这个新功能能够满足您的需求。欢迎试用并提供进一步的反馈！

Best regards,
{team_name}
```

### 3.3 替代方案提供

```markdown
Hi @{username},

感谢您提出的建议！

经过评估,我们决定采用以下替代方案:

**原建议**: [original suggestion]
**替代方案**: [alternative solution]
**原因**: [reason for choosing alternative]

**替代方案的优势**:
1. [advantage 1]
2. [advantage 2]
3. [advantage 3]

我们希望这个方案能够同样满足您的需求。如果您有任何疑虑或建议,欢迎继续讨论！

Best regards,
{team_name}
```

### 3.4 部分解决

```markdown
Hi @{username},

感谢您提供的详细反馈！

关于您提出的几点建议,我们的处理进展如下:

✅ **已实现**:
- [suggestion 1] - 已在 [version/commit] 中实现

🔄 **计划中**:
- [suggestion 2] - 已列入路线图,预计 [timeframe] 实现

❌ **暂不实现**:
- [suggestion 3] - [reason for not implementing]

如果您对已实现的部分有任何反馈,或希望讨论其他建议,请随时告诉我们！

Best regards,
{team_name}
```

---

## 4. 跟进模板

### 4.1 进展更新

```markdown
Hi @{username},

这是关于您反馈的进展更新 📊

**当前状态**: [status]
**最新进展**: [progress description]
**预计完成**: [estimated completion date]
**下一步**: [next steps]

感谢您的耐心等待,我们会继续在此 Issue 中更新进展。

Best regards,
{team_name}
```

### 4.2 延期通知

```markdown
Hi @{username},

感谢您对 #{issue_number} 的关注。

我们想向您坦诚地说明,这个问题的解决时间需要比预期延长。

**原因**:
[reason for delay]

**新的预计时间**: [new estimated date]
**我们正在做的**:
- [action 1]
- [action 2]

我们深知这可能给您带来不便,会尽最大努力尽快解决。
如有任何疑问,请随时联系我们。

Best regards,
{team_name}
```

### 4.3 定期跟进（长期 Issue）

```markdown
Hi @{username},

这是关于您反馈的定期跟进 📅

距离您提交反馈已有 [time elapsed],我们想确认:

1. 之前提供的解决方案是否有效？
2. 您是否遇到了新的相关问题？
3. 您还有其他反馈或建议吗？

如果问题已解决,我们将关闭此 Issue。如果仍需跟进,请告知。

7 天内未收到回复,我们将默认问题已解决并关闭此 Issue。

Best regards,
{team_name}
```

### 4.4 用户验证请求

```markdown
Hi @{username},

我们已针对您报告的问题进行了改进 🛠️

**改进内容**: [improvement description]
**验证方式**:
1. [step 1]
2. [step 2]
3. [step 3]

能否请您在方便的时候验证一下改进效果？

- ✅ 如果问题解决,请回复 "已解决"
- ❌ 如果问题仍在,请告诉我们具体情况
- 💡 如果有其他建议,欢迎提出

期待您的反馈！

Best regards,
{team_name}
```

---

## 5. 婉拒模板

### 5.1 超出范围

```markdown
Hi @{username},

感谢您的建议！

经过评估,我们遗憾地告知,这个建议超出了当前项目的范围。

**原因**: [reason - e.g., "本项目专注于流计算理论,不涉及具体实现框架的开发"]

**替代建议**:
- 您可以关注 [related project] 项目
- 或者查看 [alternative resource]

虽然这个建议无法在当前项目中实现,但我们非常感谢您的思考和分享！

Best regards,
{team_name}
```

### 5.2 技术限制

```markdown
Hi @{username},

感谢您的反馈！

我们认真评估了您的建议,但由于以下技术限制,目前无法实现:

**技术限制**:
1. [technical limitation 1]
2. [technical limitation 2]

**我们正在做的**:
- [alternative approach being considered]
- [long-term plan]

一旦技术条件成熟,我们会重新考虑这个建议。

Best regards,
{team_name}
```

### 5.3 重复反馈

```markdown
Hi @{username},

感谢您的反馈！

我们发现这个反馈与已有的 Issue #{original_issue} 重复。

**原 Issue**: #{original_issue} - [title]

为了保持讨论集中,我们将关闭此 Issue 并建议您关注原 Issue。
您的反馈中如有额外信息,欢迎在原 Issue 中补充。

感谢您的理解！

Best regards,
{team_name}
```

### 5.4 无效反馈

```markdown
Hi @{username},

感谢您提交反馈。

经过审核,我们无法将此反馈作为有效 Issue 处理,原因是:

[reason - e.g., "信息不完整无法重现", "与项目无关", "违反社区准则"]

**建议**:
- 如果您能提供更多信息,欢迎重新提交
- 如有疑问,请查看 [contribution guide]

感谢您的理解！

Best regards,
{team_name}
```

---

## 6. 特殊场景模板

### 6.1 升级通知

```markdown
Hi @{username},

您的反馈 #{issue_number} 已升级处理 🚀

**升级原因**: [reason for escalation]
**新处理人**: @{new_handler}
**预计处理时间**: [timeframe]

升级后,您将获得:
- 更专业的技术支持
- 更快的响应速度
- 更深入的解决方案

我们会继续在此 Issue 中保持沟通。

Best regards,
{team_name}
```

### 6.2 社区参与邀请

```markdown
Hi @{username},

感谢您的宝贵反馈！

您对 [topic] 的深入见解让我们印象深刻。我们想邀请您:

1. **参与社区讨论**: 加入我们的 [Discord/Slack/论坛]
2. **贡献内容**: 如果您有兴趣,欢迎提交 PR 改进相关文档
3. **用户访谈**: 我们正在进行用户研究,诚挚邀请您参与 30 分钟的访谈

您的参与将帮助项目变得更好！

Best regards,
{team_name}
```

### 6.3 关闭 Issue

```markdown
Hi @{username},

此 Issue 将被关闭。

**关闭原因**: [reason - e.g., "已解决", "已解决且有用户确认", "重复", "无效"]

[如果是已解决]
感谢您帮助我们改进项目！如果将来遇到其他问题,欢迎随时提交新 Issue。

[如果是重复/无效]
感谢您的时间和理解。

此 Issue 已关闭,但您仍可继续评论。如有需要,可以重新打开。

Best regards,
{team_name}
```

---

## 7. 中文模板

### 7.1 标准感谢（中文）

```markdown
@{username},您好！

感谢您抽出宝贵时间为我们提供反馈！🙏

我们已收到您的建议/报告,并已将此 Issue 标记为 `[appropriate label]`。
我们的团队将在 [timeframe] 内进行审核,并及时向您更新进展。

您的意见对改进项目质量至关重要,我们非常重视每一位用户的体验。

如有任何补充信息,欢迎随时在此 Issue 中回复。

再次感谢！

此致
{team_name}
```

### 7.2 问题已修复（中文）

```markdown
@{username},您好！

好消息！🎉 您报告的问题已经修复。

**修复详情**:
- 问题原因:[root cause]
- 修复方案:[solution description]
- 相关提交:[commit/PR link]

**您可以这样验证修复效果**:
1. [verification step 1]
2. [verification step 2]
3. [verification step 3]

请在方便的时候验证一下,确认问题是否已完全解决。
如果仍有问题,请随时在此 Issue 中回复。

感谢您的耐心等待和宝贵反馈！

此致
{team_name}
```

---

## 使用检查清单

在发送响应前，请检查：

- [ ] 使用了正确的模板
- [ ] 个性化了用户名
- [ ] 引用了具体的反馈内容
- [ ] 提供了明确的时间预期
- [ ] 包含了必要的链接/参考
- [ ] 语气友好且专业
- [ ] 没有拼写或语法错误
- [ ] 添加了正确的标签

---

*本文档版本: v1.0 | 最后更新: 2026-04-12*
