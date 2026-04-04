# Flink 版本跟踪自动化系统

一套完整的自动化脚本系统，用于跟踪 Apache Flink 的版本发布、FLIP (Flink Improvement Proposals) 状态，并自动更新文档。

## 功能特性

- 🔍 **FLIP 状态跟踪** - 从 GitHub 和 Confluence Wiki 获取 FLIP 状态
- 📦 **版本发布检查** - 监控 Maven Central 和 GitHub Releases
- 📝 **文档自动更新** - 自动更新版本跟踪文档和 FLIP 状态表
- 🔔 **多渠道通知** - 支持 Slack、邮件、Webhook 通知
- ⏰ **定时任务支持** - GitHub Actions、Cron、Windows 任务计划程序

## 快速开始

### 1. 安装依赖

```bash
cd .scripts/flink-version-tracking
pip install -r requirements.txt
```

### 2. 配置

复制示例配置或直接编辑 `config.json`:

```json
{
  "notification": {
    "slack": {
      "enabled": true,
      "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    }
  }
}
```

### 3. 运行

```bash
# 获取 FLIP 状态
python fetch-flip-status.py --detailed

# 检查新版本
python check-new-releases.py

# 更新文档
python update-version-docs.py

# 发送测试通知
python notify-changes.py --test-slack
```

## 脚本说明

### fetch-flip-status.py

从 Apache Flink GitHub API 和 Confluence Wiki 获取 FLIP 状态。

```bash
# 基础模式
python fetch-flip-status.py

# 获取详细信息（较慢）
python fetch-flip-status.py --detailed --max 50

# 过滤特定状态
python fetch-flip-status.py --status-filter accepted,implemented

# 导出到文件
python fetch-flip-status.py --output flips.json
```

### check-new-releases.py

检查 Flink 新版本发布，对比 Maven Central 和 GitHub Releases。

```bash
# 检查所有来源
python check-new-releases.py

# 只检查 GitHub
python check-new-releases.py --github-only

# 过滤版本
python check-new-releases.py --filter 1.18.*

# 只显示稳定版本
python check-new-releases.py --stable-only
```

### update-version-docs.py

自动更新版本跟踪文档。

```bash
# 更新所有文档
python update-version-docs.py

# 只更新版本跟踪文档
python update-version-docs.py --only-version-tracking

# 只更新 FLIP 引用
python update-version-docs.py --only-flip-docs

# 生成变更日志
python update-version-docs.py --generate-changelog
```

### notify-changes.py

发送变更通知。

```bash
# 测试 Slack 通知
python notify-changes.py --test-slack

# 测试邮件
python notify-changes.py --test-email

# 从检查结果发送通知
python notify-changes.py --from-check-results

# 发送每日摘要
python notify-changes.py --daily-summary
```

## 定时任务配置

### GitHub Actions

详见 `cron-schedule.md`，已包含完整的工作流配置。

### Linux/macOS Cron

```bash
# 编辑 crontab
crontab -e

# 添加任务
0 */6 * * * cd /path/to/project/.scripts/flink-version-tracking && python fetch-flip-status.py
0 */12 * * * cd /path/to/project/.scripts/flink-version-tracking && python check-new-releases.py
0 8 * * * cd /path/to/project/.scripts/flink-version-tracking && python update-version-docs.py
```

### Windows 任务计划程序

运行 PowerShell 脚本:

```powershell
.\setup-windows-scheduler.ps1
```

## 项目结构

```
.scripts/flink-version-tracking/
├── config.json              # 配置文件
├── requirements.txt         # Python 依赖
├── README.md               # 本文件
├── cron-schedule.md        # 定时任务配置说明
├── fetch-flip-status.py    # FLIP 状态获取
├── check-new-releases.py   # 版本发布检查
├── update-version-docs.py  # 文档自动更新
├── notify-changes.py       # 变更通知
└── data/                   # 数据目录 (自动创建)
    ├── flip_cache.json     # FLIP 缓存
    ├── release_cache.json  # 版本缓存
    └── *.json              # 检查结果
```

## 配置说明

### 配置文件结构

```json
{
  "flink": {
    "github_repo": "apache/flink",
    "flip_base_url": "https://cwiki.apache.org/confluence/display/FLINK"
  },
  "api": {
    "request_timeout": 30,
    "retry_attempts": 3
  },
  "storage": {
    "data_dir": "./data"
  },
  "notification": {
    "slack": { "enabled": false, "webhook_url": "" },
    "email": { "enabled": false, "smtp_server": "", ... }
  }
}
```

### 环境变量

| 变量名 | 说明 |
|--------|------|
| `SLACK_WEBHOOK_URL` | Slack Webhook URL |
| `EMAIL_USERNAME` | SMTP 用户名 |
| `EMAIL_PASSWORD` | SMTP 密码 |
| `GITHUB_TOKEN` | GitHub API Token (可选) |

## 故障排除

### 依赖问题

```bash
# 如果缺少 requests
pip install requests beautifulsoup4 packaging

# 如果缺少 lxml 解析器
pip install lxml
```

### 权限问题

```bash
# 确保数据目录可写
chmod 755 data
```

### 网络问题

- 检查代理设置
- 增加超时时间 (修改 config.json)
- 检查防火墙设置

## 开发

### 添加新的通知渠道

1. 在 `notify-changes.py` 中继承 `NotificationChannel`
2. 实现 `send()` 方法
3. 在 `NotificationManager` 中注册

### 扩展数据解析

1. 在相应的脚本中添加解析器类
2. 遵循现有的数据模型
3. 添加测试用例

## 许可证

本项目遵循 Apache 2.0 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request!

---

*最后更新: 2026-04-04*
