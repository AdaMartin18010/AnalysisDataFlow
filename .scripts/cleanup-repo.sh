#!/bin/bash
# =============================================================================
# AnalysisDataFlow - Repository Cleanup Script
# 清理所有编译中间产物，保持GitHub友好
# =============================================================================

set -e

echo "======================================================================"
echo "AnalysisDataFlow - Repository Cleanup"
echo "======================================================================"

# 统计开始
START_SIZE=$(du -sh . 2>/dev/null | cut -f1)
echo "当前目录大小: $START_SIZE"
echo ""

# -----------------------------------------------------------------------------
# 1. Python缓存
# -----------------------------------------------------------------------------
echo "[1/10] 清理 Python __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.py[cod]" -delete 2>/dev/null || true
find . -type f -name "*.so" -delete 2>/dev/null || true
echo "✓ Python缓存已清理"

# -----------------------------------------------------------------------------
# 2. Node.js依赖和构建产物
# -----------------------------------------------------------------------------
echo "[2/10] 清理 Node.js 产物..."
find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".next" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "dist" -path "*/learning-platform/*" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "package-lock.json" -delete 2>/dev/null || true
find . -type f -name "yarn.lock" -delete 2>/dev/null || true
echo "✓ Node.js产物已清理"

# -----------------------------------------------------------------------------
# 3. Java/Maven构建产物
# -----------------------------------------------------------------------------
echo "[3/10] 清理 Java/Maven target目录..."
find . -type d -name "target" -path "*/Flink-Scala-Rust-Comprehensive/*" -exec rm -rf {} + 2>/dev/null || true
echo "✓ Java构建产物已清理"

# -----------------------------------------------------------------------------
# 4. Rust构建产物
# -----------------------------------------------------------------------------
echo "[4/10] 清理 Rust target目录..."
find . -type d -name "target" -path "*/rust/*" -exec rm -rf {} + 2>/dev/null || true
echo "✓ Rust构建产物已清理"

# -----------------------------------------------------------------------------
# 5. Go构建产物
# -----------------------------------------------------------------------------
echo "[5/10] 清理 Go 构建产物..."
find . -type f -name "*.exe" -path "*/go/*" -delete 2>/dev/null || true
echo "✓ Go构建产物已清理"

# -----------------------------------------------------------------------------
# 6. IDE配置
# -----------------------------------------------------------------------------
echo "[6/10] 清理 IDE 配置..."
find . -type d -name ".idea" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".vscode" -not -path "./.vscode" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.iml" -delete 2>/dev/null || true
find . -type f -name ".project" -delete 2>/dev/null || true
find . -type f -name ".classpath" -delete 2>/dev/null || true
echo "✓ IDE配置已清理"

# -----------------------------------------------------------------------------
# 7. 操作系统文件
# -----------------------------------------------------------------------------
echo "[7/10] 清理操作系统文件..."
find . -type f -name ".DS_Store" -delete 2>/dev/null || true
find . -type f -name "Thumbs.db" -delete 2>/dev/null || true
echo "✓ 操作系统文件已清理"

# -----------------------------------------------------------------------------
# 8. 日志和临时文件
# -----------------------------------------------------------------------------
echo "[8/10] 清理日志和临时文件..."
find . -type f -name "*.log" -not -path "*/Flink/*" -delete 2>/dev/null || true
find . -type f -name "*.tmp" -delete 2>/dev/null || true
find . -type f -name "*.temp" -delete 2>/dev/null || true
find . -type f -name "*.bak" -delete 2>/dev/null || true
echo "✓ 日志和临时文件已清理"

# -----------------------------------------------------------------------------
# 9. 生成的JSON数据文件
# -----------------------------------------------------------------------------
echo "[9/10] 清理生成的数据文件..."
find . -type f -name "validation-results.json" -delete 2>/dev/null || true
find . -type f -name "invalid-blocks.json" -delete 2>/dev/null || true
find . -type f -name "fixes-applied.json" -delete 2>/dev/null || true
find . -type d -name "audit-results" -path "*/.scripts/*" -exec rm -rf {} + 2>/dev/null || true
echo "✓ 生成的数据文件已清理"

# -----------------------------------------------------------------------------
# 10. 知识图谱站点构建产物
# -----------------------------------------------------------------------------
echo "[10/10] 清理知识图谱站点..."
find . -type d -name "knowledge-graph-site" -exec rm -rf {} + 2>/dev/null || true
echo "✓ 知识图谱站点已清理"

# -----------------------------------------------------------------------------
# 统计结束
# -----------------------------------------------------------------------------
echo ""
echo "======================================================================"
END_SIZE=$(du -sh . 2>/dev/null | cut -f1)
echo "清理后目录大小: $END_SIZE"
echo "======================================================================"
echo ""
echo "✅ 清理完成！"
echo ""
echo "提示:"
echo "  - 使用 'git status' 查看变更"
echo "  - 使用 'git add -A && git commit -m \"chore: cleanup build artifacts\"' 提交"
echo "  - 使用 'git push' 推送到GitHub"
