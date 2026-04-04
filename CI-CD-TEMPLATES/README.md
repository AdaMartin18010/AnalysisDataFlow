# AnalysisDataFlow CI/CD 配置库

> 流计算知识体系项目的持续集成与持续部署配置模板集合

## 📋 目录结构

```
CI-CD-TEMPLATES/
├── README.md                          # 本文件
├── jenkins/                           # Jenkins Pipeline配置
│   ├── Jenkinsfile-flink-validation   # Flink专项验证
│   └── Jenkinsfile-full-check         # 完整验证流水线
├── gitlab/                            # GitLab CI配置
│   └── .gitlab-ci.yml                 # GitLab CI模板
├── scripts/                           # 自动化脚本
│   ├── check-links.py                 # 链接检查脚本
│   ├── update-stats.py                # 统计更新脚本
│   └── notify.py                      # 通知脚本
└── quality-gates/                     # 质量门禁配置
    ├── document-integrity-check.yml   # 文档完整性检查
    ├── cross-reference-validation.yml # 交叉引用验证
    └── mermaid-syntax-check.yml       # Mermaid语法检查
```

## 🚀 快速开始

### GitHub Actions（已内置）

项目已包含以下GitHub Actions工作流：

| 工作流 | 文件 | 描述 |
|--------|------|------|
| 文档验证 | `.github/workflows/validate.yml` | 定理编号、交叉引用、Mermaid图表验证 |
| 链接检查 | `.github/workflows/check-links.yml` | 内部和外部链接有效性检查 |
| 统计更新 | `.github/workflows/update-stats.yml` | 自动更新项目统计信息 |
| 预览部署 | `.github/workflows/deploy-preview.yml` | PR预览站点自动生成 |

### Jenkins

#### 1. Flink专项验证

```bash
# 在Jenkins中创建Pipeline项目，配置Pipeline脚本路径：
# CI-CD-TEMPLATES/jenkins/Jenkinsfile-flink-validation
```

**功能**：

- Flink目录结构验证
- Flink代码示例检查
- Flink定理编号验证
- Flink配置验证

**触发条件**：

- 定时触发（每周二凌晨3点）
- SCM变更触发
- 手动触发

#### 2. 完整验证流水线

```bash
# Pipeline脚本路径：
# CI-CD-TEMPLATES/jenkins/Jenkinsfile-full-check
```

**功能**：

- 定理注册表完整性验证
- 交叉引用验证
- Mermaid图表语法验证
- 链接有效性检查
- 质量门禁
- 生成综合报告

### GitLab CI

将 `CI-CD-TEMPLATES/gitlab/.gitlab-ci.yml` 复制到项目根目录：

```bash
cp CI-CD-TEMPLATES/gitlab/.gitlab-ci.yml .gitlab-ci.yml
```

**流水线阶段**：

1. `validate` - 验证阶段（定理、交叉引用、Mermaid）
2. `quality` - 质量检查（链接、统计更新）
3. `report` - 报告生成
4. `deploy` - 部署到GitLab Pages

## 🔧 自动化脚本

### 链接检查脚本

```bash
# 仅检查内部链接
python CI-CD-TEMPLATES/scripts/check-links.py

# 检查所有链接（包括外部）
python CI-CD-TEMPLATES/scripts/check-links.py --check-external --timeout 30

# 生成JSON报告
python CI-CD-TEMPLATES/scripts/check-links.py --format json --output link-report.json

# 生成HTML报告
python CI-CD-TEMPLATES/scripts/check-links.py --format html --output link-report.html
```

**功能**：

- ✅ 验证内部文档链接
- ✅ 验证外部HTTP/HTTPS链接（可选）
- ✅ 并发检查提高效率
- ✅ 生成详细报告（Text/JSON/HTML）

### 统计更新脚本

```bash
# 仅显示当前统计
python CI-CD-TEMPLATES/scripts/update-stats.py --check-only

# 更新所有统计文件
python CI-CD-TEMPLATES/scripts/update-stats.py --update-tracking --update-readme

# 生成JSON统计报告
python CI-CD-TEMPLATES/scripts/update-stats.py --format json --output stats.json
```

**功能**：

- 📊 扫描各目录文档数量
- 📊 统计形式化元素（定理、定义等）
- 📝 自动更新 `PROJECT-TRACKING.md`
- 📝 自动更新 `README.md`

### 通知脚本

```bash
# 设置环境变量
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."

# 发送Slack通知
python CI-CD-TEMPLATES/scripts/notify.py \
  --channel slack \
  --title "构建成功" \
  --message "项目构建完成" \
  --level success

# 企业微信通知
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/..."
python CI-CD-TEMPLATES/scripts/notify.py \
  --channel wecom \
  --title "文档验证完成" \
  --message "所有检查通过"

# 钉钉通知
export DINGTALK_WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=..."
export DINGTALK_SECRET="your-secret"
python CI-CD-TEMPLATES/scripts/notify.py \
  --channel dingtalk \
  --title "构建通知" \
  --message "部署成功"
```

**支持的通知渠道**：

- Slack
- 邮件
- 企业微信 (WeCom)
- 钉钉 (DingTalk)
- 飞书 (Lark)
- 通用 Webhook

## 🛡️ 质量门禁

### 文档完整性检查

配置文件：`CI-CD-TEMPLATES/quality-gates/document-integrity-check.yml`

**检查项**：

- ✅ 必需文件和目录存在
- ✅ 文档结构符合六段式模板
- ✅ 文件名命名规范
- ✅ 文件大小限制
- ✅ Markdown格式规范

### 交叉引用验证

配置文件：`CI-CD-TEMPLATES/quality-gates/cross-reference-validation.yml`

**检查项**：

- ✅ 内部链接有效性
- ✅ 定理编号存在性
- ✅ 循环引用检测
- ✅ 孤立文档检测
- ✅ 引用完整性

### Mermaid语法检查

配置文件：`CI-CD-TEMPLATES/quality-gates/mermaid-syntax-check.yml`

**检查项**：

- ✅ 图表类型有效性
- ✅ 语法正确性
- ✅ 代码块完整性
- ✅ 图表大小限制
- ✅ 节点命名规范

## 📊 配置参数说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `PYTHON_VERSION` | Python版本 | 3.11 |
| `NODE_VERSION` | Node.js版本 | 20 |
| `SLACK_WEBHOOK_URL` | Slack Webhook地址 | - |
| `WECOM_WEBHOOK_URL` | 企业微信Webhook地址 | - |
| `DINGTALK_WEBHOOK_URL` | 钉钉Webhook地址 | - |
| `LARK_WEBHOOK_URL` | 飞书Webhook地址 | - |

### 质量门禁阈值

| 检查项 | 错误阈值 | 警告阈值 |
|--------|----------|----------|
| 无效内部链接 | > 0 | - |
| 重复定理编号 | > 0 | - |
| Mermaid语法错误 | > 0 | - |
| 文件大小 | > 500KB | > 300KB |
| 文档字数 | < 100 | < 200 |

## 🔨 故障处理指南

### 常见问题

#### 1. 定理编号冲突

**症状**：验证失败，提示定理编号重复

**解决方案**：

```bash
# 查找重复的定理编号
grep -r "Thm-S-01-01" --include="*.md" .

# 手动修改冲突的编号
# 确保编号格式: Thm-S-XX-YY (阶段-文档号-顺序号)
```

#### 2. 无效内部链接

**症状**：链接检查报告损坏链接

**解决方案**：

```bash
# 运行链接检查脚本
python CI-CD-TEMPLATES/scripts/check-links.py --verbose

# 根据报告修复链接路径
# 确保使用相对路径或正确的绝对路径
```

#### 3. Mermaid图表渲染失败

**症状**：Mermaid验证失败

**解决方案**：

```bash
# 安装Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# 验证单个图表
mmdc -i diagram.mmd -o output.svg

# 检查常见错误：
# - 节点ID格式错误
# - 箭头语法错误
# - 缺少结束符
```

#### 4. 外部链接超时

**症状**：外部链接检查超时或失败

**解决方案**：

```bash
# 增加超时时间
python CI-CD-TEMPLATES/scripts/check-links.py \
  --check-external \
  --timeout 60

# 在CI配置中排除特定URL
# 修改 exclude_patterns 配置
```

### 调试技巧

1. **启用详细输出**

   ```bash
   python script.py --verbose
   ```

2. **仅检查特定目录**

   ```bash
   cd Struct && python ../CI-CD-TEMPLATES/scripts/check-links.py
   ```

3. **生成调试报告**

   ```bash
   python script.py --format json --output debug.json
   ```

## 📝 贡献指南

1. 修改配置前请先备份
2. 在测试环境验证更改
3. 更新本文档说明
4. 提交PR时说明变更原因

## 📚 相关文档

- [PROJECT-TRACKING.md](../PROJECT-TRACKING.md) - 项目进度跟踪
- [AGENTS.md](../AGENTS.md) - Agent工作规范
- [ARCHITECTURE.md](../ARCHITECTURE.md) - 项目架构文档

---

*本配置库由AnalysisDataFlow项目维护*
