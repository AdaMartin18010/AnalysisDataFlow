# 运行所有知识图谱分析工具
# =====================================

$ErrorActionPreference = "Stop"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SCRIPT_DIR

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "知识图谱管理和分析工具" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 创建输出目录
New-Item -ItemType Directory -Force -Path "output" | Out-Null
New-Item -ItemType Directory -Force -Path "index" | Out-Null

# 检查Python
if (!(Get-Command python3 -ErrorAction SilentlyContinue)) {
    Write-Host "错误: Python3 未安装" -ForegroundColor Red
    exit 1
}

# 检查依赖
Write-Host ""
Write-Host "[1/5] 检查依赖..." -ForegroundColor Yellow
pip install -q -r requirements.txt

# 1. 概念图谱构建
Write-Host ""
Write-Host "[2/5] 构建概念关系图谱..." -ForegroundColor Yellow
python3 concept-map-builder.py -c config.json

# 2. 定理依赖分析
Write-Host ""
Write-Host "[3/5] 分析定理依赖关系..." -ForegroundColor Yellow
python3 theorem-dependency-analyzer.py -c config.json

# 3. 文档相似度分析
Write-Host ""
Write-Host "[4/5] 分析文档相似度..." -ForegroundColor Yellow
python3 doc-similarity-analyzer.py -c config.json

# 4. 构建搜索索引
Write-Host ""
Write-Host "[5/5] 构建搜索索引..." -ForegroundColor Yellow
python3 knowledge-search-engine.py index -c config.json

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "所有工具运行完成!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "输出文件:" -ForegroundColor White
Write-Host "  - output/graph-data.cypher     (Neo4j导入)"
Write-Host "  - output/graph.gexf            (Gephi可视化)"
Write-Host "  - output/theorem-dependencies.json"
Write-Host "  - output/critical-path.txt"
Write-Host "  - output/similarity-matrix.json"
Write-Host "  - output/doc-clusters.json"
Write-Host "  - output/content-gaps.json"
Write-Host "  - index/search-index.json      (搜索索引)"
Write-Host ""
