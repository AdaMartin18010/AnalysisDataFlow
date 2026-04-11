#!/bin/bash
# 运行所有知识图谱分析工具
# =====================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "知识图谱管理和分析工具"
echo "=========================================="

# 创建输出目录
mkdir -p output
mkdir -p index

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: Python3 未安装"
    exit 1
fi

# 检查依赖
echo ""
echo "[1/5] 检查依赖..."
pip install -q -r requirements.txt

# 1. 概念图谱构建
echo ""
echo "[2/5] 构建概念关系图谱..."
python3 concept-map-builder.py -c config.json

# 2. 定理依赖分析
echo ""
echo "[3/5] 分析定理依赖关系..."
python3 theorem-dependency-analyzer.py -c config.json

# 3. 文档相似度分析
echo ""
echo "[4/5] 分析文档相似度..."
python3 doc-similarity-analyzer.py -c config.json

# 4. 构建搜索索引
echo ""
echo "[5/5] 构建搜索索引..."
python3 knowledge-search-engine.py index -c config.json

echo ""
echo "=========================================="
echo "所有工具运行完成!"
echo "=========================================="
echo ""
echo "输出文件:"
echo "  - output/graph-data.cypher     (Neo4j导入)"
echo "  - output/graph.gexf            (Gephi可视化)"
echo "  - output/theorem-dependencies.json"
echo "  - output/critical-path.txt"
echo "  - output/similarity-matrix.json"
echo "  - output/doc-clusters.json"
echo "  - output/content-gaps.json"
echo "  - index/search-index.json      (搜索索引)"
echo ""
