# =============================================================================
# AnalysisDataFlow - Repository Cleanup Script (PowerShell)
# 清理所有编译中间产物，保持GitHub友好
# =============================================================================

$ErrorActionPreference = "Continue"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "AnalysisDataFlow - Repository Cleanup (Windows)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 统计开始
$startSize = (Get-ChildItem -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "当前目录大小: $([math]::Round($startSize, 2)) MB"
Write-Host ""

# -----------------------------------------------------------------------------
# 1. Python缓存
# -----------------------------------------------------------------------------
Write-Host "[1/10] 清理 Python __pycache__..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter "*.py[cod]" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter "*.so" | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "✓ Python缓存已清理" -ForegroundColor Green

# -----------------------------------------------------------------------------
# 2. Node.js依赖和构建产物
# -----------------------------------------------------------------------------
Write-Host "[2/10] 清理 Node.js 产物..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Directory -Filter "node_modules" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Directory -Filter ".next" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "learning-platform" -Recurse -Directory -Filter "dist" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter "package-lock.json" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter "yarn.lock" | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "✓ Node.js产物已清理" -ForegroundColor Green

# -----------------------------------------------------------------------------
# 3. Java/Maven构建产物
# -----------------------------------------------------------------------------
Write-Host "[3/10] 清理 Java/Maven target目录..." -ForegroundColor Yellow
Get-ChildItem -Path "Knowledge\Flink-Scala-Rust-Comprehensive" -Recurse -Directory -Filter "target" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✓ Java构建产物已清理" -ForegroundColor Green

# -----------------------------------------------------------------------------
# 4. IDE配置
# -----------------------------------------------------------------------------
Write-Host "[4/10] 清理 IDE 配置..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Directory -Filter ".idea" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter "*.iml" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter ".project" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter ".classpath" | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "✓ IDE配置已清理" -ForegroundColor Green

# -----------------------------------------------------------------------------
# 5. 操作系统文件
# -----------------------------------------------------------------------------
Write-Host "[5/10] 清理操作系统文件..." -ForegroundColor Yellow
Get-ChildItem -Recurse -File -Filter ".DS_Store" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter "Thumbs.db" | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "✓ 操作系统文件已清理" -ForegroundColor Green

# -----------------------------------------------------------------------------
# 6. 日志和临时文件
# -----------------------------------------------------------------------------
Write-Host "[6/10] 清理日志和临时文件..." -ForegroundColor Yellow
Get-ChildItem -Recurse -File -Filter "*.log" | Where-Object { $_.FullName -notlike "*\Flink\*" } | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter "*.tmp" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter "*.temp" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter "*.bak" | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "✓ 日志和临时文件已清理" -ForegroundColor Green

# -----------------------------------------------------------------------------
# 7. 生成的JSON数据文件
# -----------------------------------------------------------------------------
Write-Host "[7/10] 清理生成的数据文件..." -ForegroundColor Yellow
Get-ChildItem -Recurse -File -Filter "validation-results.json" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter "invalid-blocks.json" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter "fixes-applied.json" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path ".scripts" -Recurse -Directory -Filter "audit-results" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✓ 生成的数据文件已清理" -ForegroundColor Green

# -----------------------------------------------------------------------------
# 8. 知识图谱站点构建产物
# -----------------------------------------------------------------------------
Write-Host "[8/10] 清理知识图谱站点..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Directory -Filter "knowledge-graph-site" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✓ 知识图谱站点已清理" -ForegroundColor Green

# -----------------------------------------------------------------------------
# 统计结束
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
$endSize = (Get-ChildItem -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "清理后目录大小: $([math]::Round($endSize, 2)) MB" -ForegroundColor Cyan
$saved = $startSize - $endSize
Write-Host "节省空间: $([math]::Round($saved, 2)) MB" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ 清理完成！" -ForegroundColor Green
Write-Host ""
Write-Host "提示:" -ForegroundColor Yellow
Write-Host "  - 使用 'git status' 查看变更"
Write-Host "  - 使用 'git add -A && git commit -m \"chore: cleanup build artifacts\"' 提交"
Write-Host "  - 使用 'git push' 推送到GitHub"
