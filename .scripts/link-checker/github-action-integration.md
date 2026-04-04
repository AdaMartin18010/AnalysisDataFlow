# GitHub Actions 集成指南

> 版本: 1.0.0 | 适用于 AnalysisDataFlow 项目

本文档描述如何将链接检查器与 GitHub Actions 集成，实现自动化的链接健康监控。

---

## 📋 目录

- [概述](#概述)
- [工作流配置](#工作流配置)
- [PR检查工作流](#pr检查工作流)
- [定期全量检查](#定期全量检查)
- [通知配置](#通知配置)
- [高级配置](#高级配置)
- [故障排除](#故障排除)

---

## 概述

GitHub Actions 集成提供以下功能：

1. **PR 检查**: 在 Pull Request 中自动检查修改的文件
2. **定期全量检查**: 每周/每月自动检查整个仓库
3. **报告生成**: 自动生成 HTML/Markdown 报告
4. **PR 评论**: 在 PR 中发布检查结果
5. **Issue 创建**: 发现失效链接时自动创建 Issue

---

## 工作流配置

### 基础配置

在项目根目录创建 `.github/workflows/link-checker.yml`：

```yaml
name: Link Checker

on:
  # PR 触发
  pull_request:
    paths:
      - '**.md'

  # 手动触发
  workflow_dispatch:
    inputs:
      check_type:
        description: '检查类型'
        required: true
        default: 'pr'
        type: choice
        options:
          - pr
          - full
          - quick

  # 定期触发 (每周一凌晨3点)
  schedule:
    - cron: '0 3 * * 1'

env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '20'

jobs:
  link-check:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
      pull-requests: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # 需要完整历史以获取文件变更

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          pip install aiohttp pyyaml requests

      - name: Run link checker
        id: check
        run: |
          cd .scripts/link-checker
          python link-checker.py \
            --path ../../ \
            --config config.yaml \
            --output link-check-results.json \
            --verbose
        continue-on-error: true

      - name: Generate report
        if: always()
        run: |
          cd .scripts/link-checker
          python report-generator.py \
            --input link-check-results.json \
            --output-html link-report.html \
            --output-md link-report.md \
            --save-history

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: link-check-results
          path: |
            .scripts/link-checker/link-check-results.json
            .scripts/link-checker/link-report.html
            .scripts/link-checker/link-report.md
          retention-days: 30

      - name: Comment PR
        if: github.event_name == 'pull_request' && always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const results = JSON.parse(
              fs.readFileSync('.scripts/link-checker/link-check-results.json', 'utf8')
            );
            const summary = results.summary;

            const status = summary.broken_links > 0 ? '❌' : '✅';
            const brokenList = results.results
              .filter(r => !r.is_valid)
              .slice(0, 10)
              .map(r => `- \`${r.url}\` in \`${r.source_file}:${r.line_number}\``)
              .join('\n');

            const body = `## ${status} Link Checker Report

            | 指标 | 数值 |
            |------|------|
            | 检查文件 | ${summary.total_files} |
            | 总链接 | ${summary.total_links} |
            | ✅ 有效 | ${summary.valid_links} |
            | ❌ 失效 | ${summary.broken_links} |
            | ⚠️ 警告 | ${summary.warning_links} |
            | 耗时 | ${summary.check_duration.toFixed(1)}s |

            ${summary.broken_links > 0 ? `### 失效链接详情\n${brokenList}\n${summary.broken_links > 10 ? `\n*... 还有 ${summary.broken_links - 10} 个失效链接*\n` : ''}` : ''}

            [查看完整报告](https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }})
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });

      - name: Create issue for broken links
        if: github.event_name == 'schedule' && steps.check.outcome == 'failure'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const results = JSON.parse(
              fs.readFileSync('.scripts/link-checker/link-check-results.json', 'utf8')
            );

            const brokenLinks = results.results.filter(r => !r.is_valid);

            if (brokenLinks.length === 0) return;

            const issueTitle = `🔗 [Auto] 发现 ${brokenLinks.length} 个失效链接`;
            const issueBody = `## 链接检查报告

            定期全量检查发现 **${brokenLinks.length}** 个失效链接。

            ### 统计摘要
            - 检查文件数: ${results.summary.total_files}
            - 总链接数: ${results.summary.total_links}
            - 有效链接: ${results.summary.valid_links}
            - 失效链接: ${results.summary.broken_links}
            - 警告链接: ${results.summary.warning_links}

            ### 失效链接列表

            | URL | 源文件 | 行号 | 错误 |
            |-----|--------|------|------|
            ${brokenLinks.slice(0, 50).map(r => `| ${r.url.substring(0, 60)}${r.url.length > 60 ? '...' : ''} | ${r.source_file} | ${r.line_number} | ${r.error_message?.substring(0, 40) || ''} |`).join('\n')}

            ${brokenLinks.length > 50 ? `\n*... 还有 ${brokenLinks.length - 50} 个失效链接*\n` : ''}

            ### 建议操作

            1. 运行修复建议工具: \`python .scripts/link-checker/fix-suggestions.py --input .scripts/link-checker/link-check-results.json\`
            2. 查看完整报告: [Actions Run #${{ github.run_id }}](https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }})

            ---
            *此 Issue 由 GitHub Actions 自动创建*
            *运行时间: ${new Date().toISOString()}*
            `;

            // 检查是否已存在类似的开放 Issue
            const issues = await github.rest.issues.listForRepo({
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'open',
              labels: 'broken-links,automated'
            });

            const existingIssue = issues.data.find(i => i.title.includes('失效链接'));

            if (existingIssue) {
              // 更新现有 Issue
              await github.rest.issues.update({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: existingIssue.number,
                body: issueBody
              });
            } else {
              // 创建新 Issue
              await github.rest.issues.create({
                owner: context.repo.owner,
                repo: context.repo.repo,
                title: issueTitle,
                body: issueBody,
                labels: ['broken-links', 'automated']
              });
            }
```

---

## PR检查工作流

### 仅检查变更的文件

```yaml
name: Link Checker (PR)

on:
  pull_request:
    paths:
      - '**.md'

jobs:
  link-check-pr:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changed-files
        run: |
          # 获取变更的Markdown文件
          changed_files=$(git diff --name-only --diff-filter=ACMRT origin/${{ github.base_ref }}...HEAD | grep '\.md$' || true)
          echo "files=$changed_files" >> $GITHUB_OUTPUT
          echo "Changed files: $changed_files"

      - name: Set up Python
        if: steps.changed-files.outputs.files != ''
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        if: steps.changed-files.outputs.files != ''
        run: pip install aiohttp pyyaml requests

      - name: Run link checker on changed files
        if: steps.changed-files.outputs.files != ''
        run: |
          cd .scripts/link-checker
          # 仅检查变更的文件
          for file in ${{ steps.changed-files.outputs.files }}; do
            echo "Checking: $file"
          done

          python link-checker.py \
            --path ../../ \
            --config config.yaml \
            --output link-check-results.json
        continue-on-error: true

      - name: Comment PR with results
        if: steps.changed-files.outputs.files != ''
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');

            let results;
            try {
              results = JSON.parse(fs.readFileSync('.scripts/link-checker/link-check-results.json', 'utf8'));
            } catch (e) {
              console.log('No results file found');
              return;
            }

            const summary = results.summary;
            const status = summary.broken_links > 0 ? '❌' : '✅';

            const body = `## ${status} PR Link Check

            变更文件中的链接检查结果：

            | 指标 | 数值 |
            |------|------|
            | 检查文件 | ${summary.total_files} |
            | 总链接 | ${summary.total_links} |
            | ✅ 有效 | ${summary.valid_links} |
            | ❌ 失效 | ${summary.broken_links} |

            ${summary.broken_links > 0 ? '⚠️ **请在合并前修复失效链接**' : '✅ 所有链接检查通过'}
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
```

---

## 定期全量检查

### 每周完整扫描

```yaml
name: Weekly Link Check

on:
  schedule:
    - cron: '0 3 * * 1'  # 每周一凌晨3点
  workflow_dispatch:

jobs:
  full-check:
    runs-on: ubuntu-latest
    timeout-minutes: 60

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install aiohttp pyyaml requests

      - name: Run full link check
        run: |
          cd .scripts/link-checker
          python link-checker.py \
            --path ../../ \
            --config config.yaml \
            --output link-check-results.json \
            --patterns "**/*.md"

      - name: Generate and save reports
        run: |
          cd .scripts/link-checker
          python report-generator.py \
            --input link-check-results.json \
            --output-html reports/full-report-${{ github.run_id }}.html \
            --output-md reports/full-report-${{ github.run_id }}.md \
            --save-history

      - name: Deploy report to GitHub Pages
        if: always()
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./.scripts/link-checker/reports
          destination_dir: link-checker-reports

      - name: Notify Slack on failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "🔗 链接检查失败: ${{ github.repository }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*链接检查工作流失败*\n仓库: ${{ github.repository }}\n运行: <https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}|查看详情>"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## 通知配置

### Slack 通知

1. 在 Slack 中创建 Incoming Webhook
2. 将 Webhook URL 添加到 GitHub Secrets: `SLACK_WEBHOOK_URL`
3. 在工作流中使用:

```yaml
- name: Notify Slack
  uses: slackapi/slack-github-action@v1
  if: failure()
  with:
    payload: |
      {
        "text": "链接检查完成",
        "attachments": [{
          "color": "${{ steps.check.outcome == 'success' ? 'good' : 'danger' }}",
          "fields": [
            {"title": "Repository", "value": "${{ github.repository }}", "short": true},
            {"title": "Broken Links", "value": "${{ steps.check.outputs.broken_count }}", "short": true}
          ]
        }]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Email 通知

```yaml
- name: Send email notification
  if: failure()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 587
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: "[Link Check] 发现失效链接 - ${{ github.repository }}"
    to: team@example.com
    from: github-actions@example.com
    html_body: |
      <h2>链接检查报告</h2>
      <p>发现失效链接，请查看 <a href="https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}">Actions 详情</a></p>
```

---

## 高级配置

### 增量检查

仅检查自上次成功运行以来变更的文件:

```yaml
- name: Get last successful run
  id: last-run
  run: |
    # 使用 GitHub API 获取上次成功的 commit
    last_successful_sha=$(curl -s \
      -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
      "https://api.github.com/repos/${{ github.repository }}/actions/workflows/link-checker.yml/runs?status=success&per_page=1" \
      | jq -r '.workflow_runs[0].head_sha')
    echo "sha=$last_successful_sha" >> $GITHUB_OUTPUT

- name: Check only changed files
  run: |
    changed_files=$(git diff --name-only ${{ steps.last-run.outputs.sha }}...HEAD | grep '\.md$')
    python link-checker.py --patterns "$changed_files"
```

### 分片并行检查

对于大型仓库，分片检查以提高速度:

```yaml
strategy:
  matrix:
    shard: [1, 2, 3, 4]
    total_shards: [4]

steps:
  - name: Run link checker (shard ${{ matrix.shard }})
    run: |
      python link-checker.py \
        --shard ${{ matrix.shard }} \
        --total-shards ${{ matrix.total_shards }} \
        --output results-${{ matrix.shard }}.json

  - name: Merge results
    if: matrix.shard == 1
    run: |
      python -c "
      import json
      results = []
      for i in range(1, 5):
          with open(f'results-{i}.json') as f:
              results.extend(json.load(f)['results'])
      with open('merged-results.json', 'w') as f:
          json.dump({'results': results}, f)
      "
```

---

## 故障排除

### 常见问题

#### 1. 检查超时

增加超时设置:

```yaml
- name: Run link checker
  timeout-minutes: 60
  run: python link-checker.py ...
```

#### 2. 内存不足

减少并发数:

```yaml
# 在 config.yaml 中
max_concurrent: 20
max_per_host: 5
```

#### 3. 速率限制

添加延迟:

```yaml
# 在 config.yaml 中
delay_between_requests: 1.0
```

#### 4. SSL 证书错误

```yaml
# 在 config.yaml 中
verify_ssl: false
```

### 调试技巧

```yaml
- name: Debug
  if: failure()
  run: |
    cat link-checker.log
    ls -la .scripts/link-checker/
```

---

## 参考

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [link-checker.py 文档](./link-checker.py)
- [config.yaml 配置说明](./config.yaml)
