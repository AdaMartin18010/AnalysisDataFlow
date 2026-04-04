# Flink 版本跟踪 - 定时任务配置

本文档说明如何配置定时任务来自动执行 Flink 版本跟踪脚本。

## 目录

- [概述](#概述)
- [GitHub Actions 配置](#github-actions-配置)
- [本地定时任务配置](#本地定时任务配置)
- [Windows 任务计划程序](#windows-任务计划程序)
- [Linux Cron 配置](#linux-cron-配置)
- [Docker 定时任务](#docker-定时任务)
- [监控和日志](#监控和日志)
- [故障排除](#故障排除)

---

## 概述

### 推荐执行频率

| 任务 | 频率 | 说明 |
|------|------|------|
| FLIP 状态检查 | 每 6 小时 | FLIP 变更相对频繁 |
| 版本发布检查 | 每 12 小时 | 新版本发布频率较低 |
| 文档更新 | 每日一次 | 批量更新文档 |
| 每日摘要通知 | 每日 9:00 | 工作时间开始时发送 |

### 任务执行流程

```
┌─────────────────────────────────────────────────────────────────┐
│                     定时任务执行流程                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ 检查新版本    │    │ 检查FLIP状态  │    │ 生成变更摘要  │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │              │
│         ▼                   ▼                   │              │
│  ┌──────────────┐    ┌──────────────┐          │              │
│  │ 保存到缓存    │    │ 保存到缓存    │          │              │
│  └──────┬───────┘    └──────┬───────┘          │              │
│         │                   │                   │              │
│         └───────────┬───────┘                   │              │
│                     ▼                           │              │
│            ┌────────────────┐                   │              │
│            │ 检测到新内容?   │◄──────────────────┘              │
│            └────────┬───────┘                                  │
│                     │                                          │
│           ┌─────────┴─────────┐                                │
│           ▼                   ▼                                │
│     [是] /                   \ [否]                            │
│         /                     \                                │
│        ▼                       ▼                               │
│ ┌──────────────┐      ┌──────────────┐                        │
│ │ 更新文档      │      │ 结束         │                        │
│ └──────┬───────┘      └──────────────┘                        │
│        │                                                      │
│        ▼                                                      │
│ ┌──────────────┐                                             │
│ │ 发送通知      │                                             │
│ └──────────────┘                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## GitHub Actions 配置

### 工作流文件

创建 `.github/workflows/flink-version-tracking.yml`:

```yaml
name: Flink Version Tracking

on:
  schedule:
    # 每 6 小时运行一次 (UTC)
    - cron: '0 */6 * * *'
  workflow_dispatch:  # 允许手动触发

env:
  PYTHON_VERSION: '3.11'

jobs:
  # =====================================================
  # 任务 1: 检查 FLIP 状态
  # =====================================================
  check-flip-status:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          pip install requests beautifulsoup4 packaging

      - name: Fetch FLIP status
        id: fetch_flip
        run: |
          cd .scripts/flink-version-tracking
          python fetch-flip-status.py --detailed --output data/flip_result.json
        continue-on-error: true

      - name: Upload FLIP data
        if: steps.fetch_flip.outcome == 'success'
        uses: actions/upload-artifact@v4
        with:
          name: flip-data
          path: .scripts/flink-version-tracking/data/
          retention-days: 30

  # =====================================================
  # 任务 2: 检查新版本
  # =====================================================
  check-new-releases:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          pip install requests packaging

      - name: Check new releases
        id: check_releases
        run: |
          cd .scripts/flink-version-tracking
          python check-new-releases.py --stable-only --output data/release_result.json
        continue-on-error: true

      - name: Upload release data
        if: steps.check_releases.outcome == 'success'
        uses: actions/upload-artifact@v4
        with:
          name: release-data
          path: .scripts/flink-version-tracking/data/
          retention-days: 30

  # =====================================================
  # 任务 3: 更新文档
  # =====================================================
  update-documentation:
    needs: [check-flip-status, check-new-releases]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: .scripts/flink-version-tracking/data/
          merge-multiple: true

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Update documentation
        run: |
          cd .scripts/flink-version-tracking
          python update-version-docs.py

      - name: Check for changes
        id: check_changes
        run: |
          git add -A
          git diff --staged --quiet || echo "changes=true" >> $GITHUB_OUTPUT

      - name: Commit changes
        if: steps.check_changes.outputs.changes == 'true'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git commit -m "docs: 自动更新 Flink 版本跟踪文档 [$(date +%Y-%m-%d)]"
          git push

  # =====================================================
  # 任务 4: 发送通知
  # =====================================================
  send-notifications:
    needs: [check-flip-status, check-new-releases]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: .scripts/flink-version-tracking/data/
          merge-multiple: true

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Send notifications
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
          EMAIL_USERNAME: ${{ secrets.EMAIL_USERNAME }}
          EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
        run: |
          cd .scripts/flink-version-tracking
          python notify-changes.py --from-check-results
```

### 环境变量配置

在 GitHub 仓库设置中配置以下 Secrets:

| Secret 名称 | 说明 | 必需 |
|------------|------|------|
| `SLACK_WEBHOOK_URL` | Slack Webhook URL | 可选 |
| `EMAIL_USERNAME` | SMTP 用户名 | 可选 |
| `EMAIL_PASSWORD` | SMTP 密码 | 可选 |

---

## 本地定时任务配置

### 使用 cron (Linux/macOS)

#### 1. 编辑 crontab

```bash
crontab -e
```

#### 2. 添加定时任务

```bash
# Flink 版本跟踪定时任务
# 每 6 小时检查 FLIP 状态
0 */6 * * * cd /path/to/project/.scripts/flink-version-tracking && python fetch-flip-status.py >> logs/flip.log 2>&1

# 每 12 小时检查新版本
0 */12 * * * cd /path/to/project/.scripts/flink-version-tracking && python check-new-releases.py >> logs/release.log 2>&1

# 每日 8:00 更新文档
0 8 * * * cd /path/to/project/.scripts/flink-version-tracking && python update-version-docs.py >> logs/docs.log 2>&1

# 每日 9:00 发送摘要通知
0 9 * * * cd /path/to/project/.scripts/flink-version-tracking && python notify-changes.py --daily-summary >> logs/notify.log 2>&1
```

#### 3. 创建日志目录

```bash
mkdir -p /path/to/project/.scripts/flink-version-tracking/logs
```

---

## Windows 任务计划程序

### 使用 PowerShell 脚本

创建 `setup-windows-scheduler.ps1`:

```powershell
# 需要管理员权限运行

$scriptPath = "E:\_src\AnalysisDataFlow\.scripts\flink-version-tracking"
$pythonPath = "python"  # 或完整的 python.exe 路径

# 创建任务函数
function New-FlinkTrackerTask {
    param(
        [string]$TaskName,
        [string]$ScriptName,
        [string]$Schedule,
        [string]$Modifier
    )
    
    $action = New-ScheduledTaskAction `
        -Execute $pythonPath `
        -Argument "$scriptPath\$ScriptName" `
        -WorkingDirectory $scriptPath
    
    $trigger = switch ($Schedule) {
        "Hourly" { New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours $Modifier) }
        "Daily" { New-ScheduledTaskTrigger -Daily -At $Modifier }
        "Weekly" { New-ScheduledTaskTrigger -Weekly -DaysOfWeek $Modifier -At "09:00" }
    }
    
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable
    
    Register-ScheduledTask `
        -TaskName "FlinkTracker-$TaskName" `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description "Flink Version Tracking - $TaskName" `
        -Force
    
    Write-Host "已创建任务: FlinkTracker-$TaskName"
}

# 检查 FLIP 状态 (每 6 小时)
New-FlinkTrackerTask `
    -TaskName "CheckFLIP" `
    -ScriptName "fetch-flip-status.py" `
    -Schedule "Hourly" `
    -Modifier 6

# 检查新版本 (每 12 小时)
New-FlinkTrackerTask `
    -TaskName "CheckReleases" `
    -ScriptName "check-new-releases.py" `
    -Schedule "Hourly" `
    -Modifier 12

# 更新文档 (每日 8:00)
New-FlinkTrackerTask `
    -TaskName "UpdateDocs" `
    -ScriptName "update-version-docs.py" `
    -Schedule "Daily" `
    -Modifier "08:00"

# 发送通知 (每日 9:00)
New-FlinkTrackerTask `
    -TaskName "SendNotification" `
    -ScriptName "notify-changes.py" `
    -Schedule "Daily" `
    -Modifier "09:00"

Write-Host "所有任务已创建!"
Write-Host "查看任务: Get-ScheduledTask | Where-Object { $_.TaskName -like 'FlinkTracker-*' }"
```

### 运行脚本

```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\setup-windows-scheduler.ps1
```

### 查看和管理任务

```powershell
# 查看所有 Flink 跟踪任务
Get-ScheduledTask | Where-Object { $_.TaskName -like 'FlinkTracker-*' }

# 手动运行任务
Start-ScheduledTask -TaskName "FlinkTracker-CheckFLIP"

# 删除任务
Unregister-ScheduledTask -TaskName "FlinkTracker-CheckFLIP" -Confirm:$false
```

---

## Docker 定时任务

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制脚本
COPY . .

# 创建数据目录
RUN mkdir -p data logs

# 安装 cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# 创建 crontab 文件
RUN echo "0 */6 * * * cd /app && python fetch-flip-status.py >> logs/flip.log 2>&1\n\
0 */12 * * * cd /app && python check-new-releases.py >> logs/release.log 2>&1\n\
0 8 * * * cd /app && python update-version-docs.py >> logs/docs.log 2>&1\n\
0 9 * * * cd /app && python notify-changes.py --daily-summary >> logs/notify.log 2>&1" > /etc/cron.d/flink-tracker \
    && chmod 0644 /etc/cron.d/flink-tracker \
    && crontab /etc/cron.d/flink-tracker

# 启动 cron
CMD ["cron", "-f"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  flink-tracker:
    build: .
    container_name: flink-version-tracker
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ../../:/app/project  # 挂载项目目录
    environment:
      - SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL}
      - EMAIL_USERNAME=${EMAIL_USERNAME}
      - EMAIL_PASSWORD=${EMAIL_PASSWORD}
    restart: unless-stopped
```

### 运行

```bash
# 构建和启动
docker-compose up --build -d

# 查看日志
docker-compose logs -f

# 手动执行检查
docker-compose exec flink-tracker python fetch-flip-status.py
```

---

## 监控和日志

### 日志配置

所有脚本都支持日志级别配置:

```bash
# 详细日志
python fetch-flip-status.py -l DEBUG

# 仅错误
python check-new-releases.py -l ERROR
```

### 日志轮转 (Linux)

创建 `/etc/logrotate.d/flink-tracker`:

```
/path/to/project/.scripts/flink-version-tracking/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 user user
}
```

### 健康检查脚本

创建 `health-check.sh`:

```bash
#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"
LOG_DIR="$SCRIPT_DIR/logs"

# 检查数据文件是否更新
check_data_freshness() {
    local file=$1
    local max_age_hours=$2
    
    if [ ! -f "$file" ]; then
        echo "❌ 数据文件不存在: $file"
        return 1
    fi
    
    local file_age=$(( ($(date +%s) - $(stat -c %Y "$file")) / 3600 ))
    
    if [ $file_age -gt $max_age_hours ]; then
        echo "⚠️ 数据文件过期 ($file_age 小时): $file"
        return 1
    fi
    
    echo "✅ 数据文件正常: $file (年龄: $file_age 小时)"
    return 0
}

echo "Flink Version Tracker 健康检查"
echo "================================"

# 检查 FLIP 数据
check_data_freshness "$DATA_DIR/flip_cache.json" 8

# 检查发布数据
check_data_freshness "$DATA_DIR/release_cache.json" 14

# 检查日志文件大小
for log_file in "$LOG_DIR"/*.log; do
    if [ -f "$log_file" ]; then
        size=$(stat -c%s "$log_file")
        if [ $size -gt 10485760 ]; then  # 10MB
            echo "⚠️ 日志文件过大 ($size bytes): $log_file"
        fi
    fi
done

echo "================================"
echo "检查完成"
```

---

## 故障排除

### 常见问题

#### 1. GitHub API 速率限制

**错误**: `API rate limit exceeded`

**解决**:
- 使用 GitHub Personal Access Token
- 降低检查频率
- 添加缓存机制

```python
# 在请求头中添加认证
headers = {
    "Authorization": f"token {os.environ.get('GITHUB_TOKEN')}"
}
```

#### 2. 网络超时

**错误**: `Connection timeout`

**解决**:
- 增加超时时间
- 启用重试机制
- 检查代理设置

#### 3. 邮件发送失败

**错误**: `SMTP authentication failed`

**解决**:
- 检查 SMTP 凭据
- 使用应用专用密码 (Gmail)
- 启用 "不够安全的应用访问" (不推荐用于生产)

#### 4. Slack Webhook 404

**错误**: `Webhook returned 404`

**解决**:
- 检查 Webhook URL
- 重新生成 Webhook
- 确认频道存在

### 调试模式

```bash
# 启用详细日志
export FLINK_TRACKER_DEBUG=1
python fetch-flip-status.py -l DEBUG

# 测试单个组件
python notify-changes.py --test-slack
python check-new-releases.py --filter 1.18.*
```

---

## 附录

### Cron 表达式参考

| 表达式 | 说明 |
|--------|------|
| `0 */6 * * *` | 每 6 小时 |
| `0 */12 * * *` | 每 12 小时 |
| `0 8 * * *` | 每日 8:00 |
| `0 9 * * 1` | 每周一 9:00 |
| `0 0 1 * *` | 每月 1 日 |

### 环境变量列表

| 变量名 | 说明 |
|--------|------|
| `FLINK_TRACKER_DEBUG` | 启用调试模式 |
| `SLACK_WEBHOOK_URL` | Slack Webhook URL |
| `EMAIL_USERNAME` | SMTP 用户名 |
| `EMAIL_PASSWORD` | SMTP 密码 |
| `GITHUB_TOKEN` | GitHub Personal Access Token |

---

*最后更新: 2026-04-04*
