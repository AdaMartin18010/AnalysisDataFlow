#!/usr/bin/env pwsh
<#
.SYNOPSIS
    一键应用 Algolia DocSearch 凭证并重新部署
.DESCRIPTION
    收到 Algolia 的 appId 和 apiKey 后，运行此脚本即可：
    1. 更新 KNOWLEDGE-GRAPH/index.html 中的 ALGOLIA_CONFIG
    2. 提交更改到 git
    3. 触发 GitHub Actions 重新部署
.PARAMETER AppId
    Algolia 提供的 App ID
.PARAMETER ApiKey
    Algolia 提供的 Search-Only API Key
.PARAMETER IndexName
    Algolia 索引名称（默认: analysisdataflow）
.EXAMPLE
    .\.scripts\apply-algolia-credentials.ps1 -AppId "YOUR_APP_ID" -ApiKey "YOUR_API_KEY"
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$AppId,

    [Parameter(Mandatory = $true)]
    [string]$ApiKey,

    [string]$IndexName = "analysisdataflow"
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$indexFile = Join-Path $repoRoot "KNOWLEDGE-GRAPH\index.html"

if (-not (Test-Path $indexFile)) {
    Write-Error "找不到文件: $indexFile"
    exit 1
}

Write-Host "🔧 正在更新 Algolia 配置..." -ForegroundColor Cyan
Write-Host "   App ID: $AppId"
Write-Host "   Index : $IndexName"

$content = Get-Content $indexFile -Raw -Encoding UTF8

# 替换 ALGOLIA_CONFIG 配置块
$pattern = 'const ALGOLIA_CONFIG = \{[\s\S]*?\};'
$replacement = @"
const ALGOLIA_CONFIG = {
    enabled: true,
    appId: '$AppId',
    apiKey: '$ApiKey',
    indexName: '$IndexName',
    searchParameters: {
        hitsPerPage: 10
    }
};
"@

if ($content -notmatch $pattern) {
    Write-Error "无法在 $indexFile 中找到 ALGOLIA_CONFIG 配置块，请检查文件内容。"
    exit 1
}

$newContent = $content -replace $pattern, $replacement
Set-Content -Path $indexFile -Value $newContent -Encoding UTF8 -NoNewline

Write-Host "✅ KNOWLEDGE-GRAPH/index.html 已更新" -ForegroundColor Green

# Git 提交
Set-Location $repoRoot
$hasChanges = git diff --name-only
if ($hasChanges) {
    git add "KNOWLEDGE-GRAPH/index.html"
    git commit -m "chore(algolia): integrate DocSearch credentials for $IndexName

- AppId: $AppId
- Index: $IndexName
- Auto-deploy triggered by apply-algolia-credentials.ps1"
    
    Write-Host "🚀 正在推送更改..." -ForegroundColor Cyan
    git push origin main
    Write-Host "✅ 已推送，GitHub Actions 将自动部署" -ForegroundColor Green
} else {
    Write-Host "⚠️  没有检测到更改，可能是配置已经相同。" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 完成！约 2-3 分钟后站点将启用 Algolia 搜索。" -ForegroundColor Green
Write-Host "   验证 URL: https://adamartin18010.github.io/AnalysisDataFlow/" -ForegroundColor Gray
