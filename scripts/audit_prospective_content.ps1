# 前瞻性内容审计脚本
# AnalysisDataFlow 项目 - Q1-4 审计

param(
    [string]$ProjectRoot = "E:\_src\AnalysisDataFlow",
    [string]$ReportPath = "E:\_src\AnalysisDataFlow\AUDIT-PROSPECTIVE-CONTENT-REPORT.md"
)

# 定义前瞻性关键词模式
$Keywords = @(
    "Flink 2\.4",
    "Flink 2\.5", 
    "Flink 3\.0",
    "FLIP-531",
    "AI Agent",
    "Flink Agents",
    "前瞻性",
    "preview",
    "experimental"
)

# 状态标签模板
$StatusBanner = @"
> **状态**: 🔮 前瞻内容 | **风险等级**: 高 | **最后更新**: 2026-04
> 
> 此文档描述的内容处于早期规划阶段，可能与最终实现不符。请以 Apache Flink 官方发布为准。

"@

Write-Host "=== AnalysisDataFlow 前瞻性内容审计 ===" -ForegroundColor Cyan
Write-Host "项目根目录: $ProjectRoot"
Write-Host "开始扫描..."

# 获取所有 Markdown 文件
$allFiles = Get-ChildItem -Path $ProjectRoot -Filter "*.md" -Recurse -File | 
    Where-Object { $_.FullName -notmatch "node_modules|\.git" }

Write-Host "找到 $($allFiles.Count) 个 Markdown 文件" -ForegroundColor Yellow

# 存储匹配的文件信息
$matchedFiles = @()
$categoryStats = @{
    "Flink版本前瞻" = 0
    "AI Agent" = 0
    "其他前瞻内容" = 0
}

$counter = 0
foreach ($file in $allFiles) {
    $counter++
    if ($counter % 100 -eq 0) {
        Write-Host "已扫描 $counter / $($allFiles.Count) 个文件..." -ForegroundColor Gray
    }
    
    try {
        $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
        if (-not $content) { continue }
        
        $matched = $false
        $categories = @()
        $keywordsFound = @()
        
        # 检查每个关键词
        foreach ($keyword in $Keywords) {
            if ($content -match $keyword) {
                $matched = $true
                $keywordsFound += $keyword
                
                # 分类
                if ($keyword -match "Flink 2\.[45]|Flink 3\.0") {
                    if (-not ($categories -contains "Flink版本前瞻")) {
                        $categories += "Flink版本前瞻"
                    }
                }
                elseif ($keyword -match "AI Agent|Flink Agents|FLIP-531") {
                    if (-not ($categories -contains "AI Agent")) {
                        $categories += "AI Agent"
                    }
                }
                else {
                    if (-not ($categories -contains "其他前瞻内容")) {
                        $categories += "其他前瞻内容"
                    }
                }
            }
        }
        
        if ($matched) {
            # 检查是否已经有状态标签
            $hasBanner = $content -match "状态.*前瞻|🔮|前瞻内容|PROSPECTIVE"
            
            $fileInfo = [PSCustomObject]@{
                Path = $file.FullName.Replace($ProjectRoot, "").TrimStart("\", "/")
                FullPath = $file.FullName
                Categories = $categories -join ", "
                KeywordsFound = ($keywordsFound -join ", ")
                HasBanner = $hasBanner
                Size = $file.Length
            }
            
            $matchedFiles += $fileInfo
            
            # 更新统计
            foreach ($cat in $categories) {
                $categoryStats[$cat]++
            }
        }
    }
    catch {
        Write-Host "警告: 无法读取文件 $($file.FullName): $_" -ForegroundColor Red
    }
}

Write-Host "`n扫描完成! 找到 $($matchedFiles.Count) 个包含前瞻性内容的文件" -ForegroundColor Green

# 显示分类统计
Write-Host "`n分类统计:" -ForegroundColor Cyan
foreach ($cat in $categoryStats.Keys) {
    Write-Host "  $cat`: $($categoryStats[$cat])" -ForegroundColor White
}

# 添加状态标签到未标记的文件
$modifiedCount = 0
$skippedCount = 0

Write-Host "`n开始添加状态标签..." -ForegroundColor Cyan

foreach ($fileInfo in $matchedFiles | Where-Object { -not $_.HasBanner }) {
    try {
        $content = Get-Content -Path $fileInfo.FullPath -Raw
        
        # 检查文件是否有 YAML frontmatter
        if ($content -match "^---\s*\n") {
            # 在 frontmatter 后添加状态标签
            $newContent = $content -replace "^(---\s*\n.*?\n---\s*\n)", "`$1`n$StatusBanner"
        }
        else {
            # 在文件开头添加状态标签
            $newContent = $StatusBanner + $content
        }
        
        # 写回文件
        Set-Content -Path $fileInfo.FullPath -Value $newContent -NoNewline
        $modifiedCount++
        
        if ($modifiedCount % 10 -eq 0) {
            Write-Host "  已修改 $modifiedCount 个文件..." -ForegroundColor Gray
        }
    }
    catch {
        Write-Host "错误: 无法修改文件 $($fileInfo.Path): $_" -ForegroundColor Red
    }
}

$skippedCount = ($matchedFiles | Where-Object { $_.HasBanner }).Count

Write-Host "`n修改完成!" -ForegroundColor Green
Write-Host "  已添加标签: $modifiedCount 个文件"
Write-Host "  已跳过(已有标签): $skippedCount 个文件"

# 生成审计报告
Write-Host "`n生成审计报告..." -ForegroundColor Cyan

$reportContent = @"
# 前瞻性内容审计报告 (Q1-4)

> **生成时间**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")  
> **审计范围**: AnalysisDataFlow 全项目 Markdown 文件  
> **总文件数**: $($allFiles.Count)  
> **识别文件数**: $($matchedFiles.Count)

---

## 执行摘要

本次审计扫描了项目中的 **$($allFiles.Count)** 个 Markdown 文件，识别出 **$($matchedFiles.Count)** 篇包含前瞻性内容的文档。

- **已添加状态标签**: $modifiedCount 篇
- **已存在标签**: $skippedCount 篇
- **风险等级**: 全部为 "高" (前瞻性内容)

---

## 分类统计

| 类别 | 文档数量 | 占比 |
|------|----------|------|
"@

$totalMatched = $matchedFiles.Count
foreach ($cat in $categoryStats.Keys | Sort-Object) {
    $count = $categoryStats[$cat]
    $percent = if ($totalMatched -gt 0) { [math]::Round(($count / $totalMatched) * 100, 1) } else { 0 }
    $reportContent += "`n| $cat | $count | $percent% |"
}

$reportContent += @"

---

## 已标记文档清单

### 按类别分组

"@

# Flink 版本前瞻
$flinkVersionDocs = $matchedFiles | Where-Object { $_.Categories -match "Flink版本前瞻" }
if ($flinkVersionDocs.Count -gt 0) {
    $reportContent += "`n#### Flink 版本前瞻 ($($flinkVersionDocs.Count) 篇)`n`n"
    foreach ($doc in ($flinkVersionDocs | Sort-Object Path)) {
        $status = if ($doc.HasBanner) { "✅ 已有标签" } else { "📝 新添加" }
        $reportContent += "- ``$($doc.Path)`` - $status`n"
    }
}

# AI Agent
$aiAgentDocs = $matchedFiles | Where-Object { $_.Categories -match "AI Agent" }
if ($aiAgentDocs.Count -gt 0) {
    $reportContent += "`n#### AI Agent ($($aiAgentDocs.Count) 篇)`n`n"
    foreach ($doc in ($aiAgentDocs | Sort-Object Path)) {
        $status = if ($doc.HasBanner) { "✅ 已有标签" } else { "📝 新添加" }
        $reportContent += "- ``$($doc.Path)`` - $status`n"
    }
}

# 其他前瞻内容
$otherDocs = $matchedFiles | Where-Object { $_.Categories -match "其他前瞻内容" -and $_.Categories -notmatch "Flink版本前瞻|AI Agent" }
if ($otherDocs.Count -gt 0) {
    $reportContent += "`n#### 其他前瞻内容 ($($otherDocs.Count) 篇)`n`n"
    foreach ($doc in ($otherDocs | Sort-Object Path)) {
        $status = if ($doc.HasBanner) { "✅ 已有标签" } else { "📝 新添加" }
        $reportContent += "- ``$($doc.Path)`` - $status`n"
    }
}

$reportContent += @"

---

## 风险等级分布

| 风险等级 | 文档数量 | 说明 |
|----------|----------|------|
| 🔴 高 | $($matchedFiles.Count) | 所有前瞻性内容均为高风险 |

### 风险说明

- **高风险**: 内容基于早期规划、路线图或未发布的 FLIP，可能与最终实现存在显著差异
- **建议**: 读者应以 Apache Flink 官方发布文档为准，本内容仅供参考

---

## 关键词命中统计

以下关键词用于识别前瞻性内容：

| 关键词 | 匹配文件数 |
|--------|-----------|
| Flink 2.4 | $(($matchedFiles | Where-Object { $_.KeywordsFound -match "Flink 2\.4" }).Count) |
| Flink 2.5 | $(($matchedFiles | Where-Object { $_.KeywordsFound -match "Flink 2\.5" }).Count) |
| Flink 3.0 | $(($matchedFiles | Where-Object { $_.KeywordsFound -match "Flink 3\.0" }).Count) |
| FLIP-531 | $(($matchedFiles | Where-Object { $_.KeywordsFound -match "FLIP-531" }).Count) |
| AI Agent | $(($matchedFiles | Where-Object { $_.KeywordsFound -match "AI Agent" }).Count) |
| Flink Agents | $(($matchedFiles | Where-Object { $_.KeywordsFound -match "Flink Agents" }).Count) |
| 前瞻性 | $(($matchedFiles | Where-Object { $_.KeywordsFound -match "前瞻性" }).Count) |
| preview | $(($matchedFiles | Where-Object { $_.KeywordsFound -match "preview" }).Count) |
| experimental | $(($matchedFiles | Where-Object { $_.KeywordsFound -match "experimental" }).Count) |

---

## 后续建议

1. **定期更新**: 建议每季度重新审计一次，随着 Flink 版本发布更新内容状态
2. **官方对齐**: 当 Flink 2.4/2.5/3.0 正式发布后，应及时更新对应文档状态
3. **读者提示**: 在文档显著位置保持状态标签，提醒读者注意内容时效性
4. **版本追踪**: 建议维护 FLIP-531 等关键特性的实现进度追踪

---

## 审计执行日志

- **脚本执行时间**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
- **执行用户**: $env:USERNAME
- **修改文件数**: $modifiedCount
- **跳过文件数**: $skippedCount

---

*本报告由前瞻性内容审计脚本自动生成*
"@

# 写入报告
Set-Content -Path $ReportPath -Value $reportContent -Encoding UTF8
Write-Host "审计报告已生成: $ReportPath" -ForegroundColor Green

# 输出最终统计
Write-Host "`n=== 审计完成 ===" -ForegroundColor Green
Write-Host "总扫描文件: $($allFiles.Count)" -ForegroundColor White
Write-Host "识别文件: $($matchedFiles.Count)" -ForegroundColor White
Write-Host "修改文件: $modifiedCount" -ForegroundColor White
Write-Host "报告路径: $ReportPath" -ForegroundColor Cyan

# 导出详细列表供后续使用
$matchedFiles | Export-Csv -Path "$ProjectRoot\prospective_content_audit_detail.csv" -NoTypeInformation -Encoding UTF8
Write-Host "详细清单: $ProjectRoot\prospective_content_audit_detail.csv" -ForegroundColor Cyan
