#!/bin/bash
# AnalysisDataFlow 发布包创建脚本
# 版本: v3.0.0
# 创建日期: 2026-04-11

set -e

# 配置
VERSION="3.0.0"
RELEASE_DIR="release/v${VERSION}"
PROJECT_NAME="analysis-dataflow"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 创建目录结构
create_directories() {
    log_info "创建发布目录结构..."
    mkdir -p "${RELEASE_DIR}"/{docs,pdf,website,neo4j,tools}
    log_info "目录结构创建完成"
}

# 复制文档
copy_docs() {
    log_info "复制 Markdown 文档..."
    
    # 根目录 Markdown 文件
    find . -maxdepth 1 -name "*.md" -type f -exec cp {} "${RELEASE_DIR}/docs/" \;
    
    # 子目录 Markdown 文件
    for dir in docs Flink Struct Knowledge whitepapers formal-methods tutorials; do
        if [ -d "$dir" ]; then
            log_info "  - 复制 $dir/ 目录..."
            mkdir -p "${RELEASE_DIR}/docs/$dir"
            find "$dir" -name "*.md" -type f -exec cp --parents {} "${RELEASE_DIR}/docs/" \;
        fi
    done
    
    # 复制重要配置文件
    cp README.md "${RELEASE_DIR}/" 2>/dev/null || true
    cp AGENTS.md "${RELEASE_DIR}/docs/" 2>/dev/null || true
    cp CHANGELOG.md "${RELEASE_DIR}/docs/" 2>/dev/null || true
    
    # 复制定理注册表和其他重要文件
    cp THEOREM-REGISTRY.md "${RELEASE_DIR}/docs/" 2>/dev/null || true
    cp NAVIGATION-INDEX.md "${RELEASE_DIR}/docs/" 2>/dev/null || true
    
    log_info "文档复制完成"
}

# 复制 PDF 文件
copy_pdfs() {
    log_info "复制 PDF 文件..."
    
    if [ -d "pdf" ]; then
        cp pdf/*.pdf "${RELEASE_DIR}/pdf/" 2>/dev/null || true
        log_info "  - 已复制 $(ls -1 pdf/*.pdf 2>/dev/null | wc -l) 个 PDF 文件"
    fi
    
    # 复制其他可能存在的PDF
    find . -name "*.pdf" -type f -not -path "${RELEASE_DIR}/*" -exec cp {} "${RELEASE_DIR}/pdf/" \;
    
    log_info "PDF 复制完成"
}

# 复制网站文件
copy_website() {
    log_info "复制网站文件 (HTML)..."
    
    # 知识图谱 HTML 文件
    for html in knowledge-graph*.html; do
        if [ -f "$html" ]; then
            cp "$html" "${RELEASE_DIR}/website/"
        fi
    done
    
    # 复制学习路径推荐器
    cp learning-path-recommender.js "${RELEASE_DIR}/website/" 2>/dev/null || true
    
    # 复制定理依赖图脚本
    cp theorem-dependency-graph.py "${RELEASE_DIR}/website/" 2>/dev/null || true
    
    log_info "网站文件复制完成"
}

# 复制 Neo4j 数据
copy_neo4j() {
    log_info "复制 Neo4j 数据..."
    
    # 复制知识图谱相关数据文件
    if [ -d "KNOWLEDGE-GRAPH" ]; then
        mkdir -p "${RELEASE_DIR}/neo4j/knowledge-graph"
        find KNOWLEDGE-GRAPH -type f \( -name "*.json" -o -name "*.cypher" -o -name "*.csv" \) -exec cp {} "${RELEASE_DIR}/neo4j/knowledge-graph/" \;
    fi
    
    # 复制交叉引用报告（可作为 Neo4j 导入数据）
    for json in cross-ref-validation-report*.json; do
        if [ -f "$json" ]; then
            cp "$json" "${RELEASE_DIR}/neo4j/"
        fi
    done
    
    log_info "Neo4j 数据复制完成"
}

# 复制工具脚本
copy_tools() {
    log_info "复制工具脚本..."
    
    # 复制脚本目录
    if [ -d "scripts" ]; then
        mkdir -p "${RELEASE_DIR}/tools/scripts"
        find scripts -type f \( -name "*.py" -o -name "*.sh" -o -name "*.js" \) -exec cp {} "${RELEASE_DIR}/tools/scripts/" \;
    fi
    
    # 复制验证和检查脚本
    cp pdf-export.py "${RELEASE_DIR}/tools/" 2>/dev/null || true
    cp six_section_audit.py "${RELEASE_DIR}/tools/" 2>/dev/null || true
    cp analyze_broken_links.py "${RELEASE_DIR}/tools/" 2>/dev/null || true
    
    # 复制 Makefile
    cp Makefile "${RELEASE_DIR}/tools/" 2>/dev/null || true
    
    log_info "工具脚本复制完成"
}

# 创建发布说明
create_release_notes() {
    log_info "创建发布说明..."
    
    cat > "${RELEASE_DIR}/README.md" << 'EOF'
# AnalysisDataFlow v3.0.0 发布包

> **发布日期**: 2026-04-11  
> **版本**: v3.0.0  
> **状态**: 100% 完成 ✅  
> **项目状态**: 生产就绪

## 📦 发布内容概览

本发布包包含 AnalysisDataFlow 项目的完整文档、工具和资源。

### 目录结构

```
v3.0.0/
├── docs/          # 所有 Markdown 文档 (800+)
├── pdf/           # PDF 导出文件 (8个)
├── website/       # 交互式网站文件
├── neo4j/         # Neo4j 图数据库导入数据
├── tools/         # 工具脚本和实用程序
└── README.md      # 本文件
```

## 📚 文档 (docs/)

包含项目所有 Markdown 文档，总计超过 800 个文件：

- **根目录文档**: 177 个核心 Markdown 文件
  - 项目文档: README.md, AGENTS.md, CHANGELOG.md
  - 架构文档: ARCHITECTURE.md, DESIGN-PRINCIPLES.md
  - 最佳实践: BEST-PRACTICES.md, CONTRIBUTING.md
  - 完整定理注册表: THEOREM-REGISTRY.md (v3.6, 10,483+ 形式化元素)
  
- **Struct/**: 形式理论、分析论证、严格证明 (43 文档, 380 定理)
- **Knowledge/**: 知识结构、设计模式、商业应用 (134 文档, 65 定理)
- **Flink/**: Flink 专项文档 (178 文档, 681 定理)
- **whitepapers/**: 白皮书系列
- **docs/**: 补充文档、指南和教程
- **formal-methods/**: 形式化方法相关文档
- **tutorials/**: 教程和入门指南

### 关键文档导航

| 文档 | 描述 |
|------|------|
| `README.md` | 项目总览和快速开始 |
| `AGENTS.md` | Agent 工作规范和环境设置 |
| `ARCHITECTURE.md` | 系统架构全面解析 |
| `THEOREM-REGISTRY.md` | 定理/定义/引理完整注册表 |
| `NAVIGATION-INDEX.md` | 文档导航索引 |
| `BEST-PRACTICES.md` | 最佳实践指南 |
| `100-PERCENT-COMPLETION-FINAL-REPORT.md` | 项目完成报告 |

## 📄 PDF 文档 (pdf/)

专业排版的 PDF 导出文件，适合打印和离线阅读：

1. **Flink-Complete.pdf** (92KB) - Flink 完整指南
2. **Foundation-Complete.pdf** (67KB) - 基础理论完整版
3. **Knowledge-Mapping.pdf** (96KB) - 知识图谱映射
4. **Proof-Chains-Checkpoint.pdf** (90KB) - 检查点证明链
5. **Proof-Chains-Complete.pdf** (321KB) - 完整证明链
6. **Proof-Chains-Encoding.pdf** (72KB) - 编码证明链
7. **Proof-Chains-Exactly-Once.pdf** (77KB) - Exactly-Once 语义证明
8. **Properties-Complete.pdf** (82KB) - 属性完整分析

## 🌐 交互式网站 (website/)

可交互的知识图谱和可视化工具：

- **knowledge-graph.html** - 知识图谱 v1.0
- **knowledge-graph-v2.html** - 知识图谱 v2.0
- **knowledge-graph-v3.html** - 知识图谱 v3.0
- **knowledge-graph-v4.html** - 知识图谱 v4.0 (最新)
- **knowledge-graph-theorem.html** - 定理知识图谱
- **learning-path-recommender.js** - 学习路径推荐引擎
- **theorem-dependency-graph.py** - 定理依赖图生成器

使用方法：在浏览器中打开任意 HTML 文件即可查看交互式知识图谱。

## 🗄️ Neo4j 数据 (neo4j/)

用于导入 Neo4j 图数据库的数据文件：

- **knowledge-graph/**: 知识图谱节点和关系数据
- **cross-ref-validation-report*.json**: 交叉引用验证报告

### 导入 Neo4j

```cypher
// 示例：导入知识图谱数据
CALL apoc.load.json("file:///knowledge-graph/nodes.json") YIELD value
CREATE (n:Concept {id: value.id, name: value.name, type: value.type})
```

## 🛠️ 工具脚本 (tools/)

实用的脚本和工具集合：

### Python 脚本
- **pdf-export.py** - PDF 导出工具
- **six_section_audit.py** - 六段式文档审计
- **analyze_broken_links.py** - 链接检查工具
- **formal_element_*.py** - 形式化元素检查工具
- **full_cross_ref_validator.py** - 交叉引用验证器

### Shell 脚本
- **ci-setup.sh** - CI/CD 环境设置
- **ci-validate.sh** - 持续集成验证
- **export-to-pdf.sh** - PDF 批量导出

### 其他工具
- **Makefile** - 项目构建和自动化任务
- **learning-path-recommender.js** - 学习路径推荐引擎

## 📊 项目统计

| 指标 | 数值 |
|------|------|
| 总文档数 | 800+ |
| 总定理数 | 1,910+ |
| 总定义数 | 4,564+ |
| 总引理数 | 1,568+ |
| 总命题数 | 1,194+ |
| 总推论数 | 121+ |
| PDF 文件数 | 8 |
| HTML 可视化 | 5 |
| 工具脚本数 | 50+ |

## 🎯 版本亮点 (v3.0.0)

### 核心特性
- ✅ 100% 项目完成 - 所有规划内容已交付
- ✅ 10,483+ 形式化元素完整注册
- ✅ 零交叉引用错误
- ✅ Coq 形式化验证完成
- ✅ TLA+ 模型检查通过
- ✅ AI Agent 流处理深化
- ✅ 动态学习路径推荐系统

### 新增内容
- Flink AI Agents (FLIP-531)
- Multi-Agent 流编排
- 实时图流处理 (TGN)
- 多模态流处理
- Temporal + Flink 分层架构
- Google A2A 协议集成
- Smart Casual 验证方法

## 🚀 快速开始

1. **浏览文档**: 从 `docs/README.md` 开始
2. **查看知识图谱**: 在浏览器中打开 `website/knowledge-graph-v4.html`
3. **阅读 PDF**: 查看 `pdf/` 目录中的专业排版文档
4. **运行工具**: 使用 `tools/` 中的脚本进行验证和检查

## 📖 推荐阅读路径

### 对于初学者
1. `docs/README.md` - 项目概览
2. `docs/QUICK-START.md` - 快速开始指南
3. `docs/BEST-PRACTICES.md` - 最佳实践

### 对于研究人员
1. `docs/THEOREM-REGISTRY.md` - 形式化元素注册表
2. `docs/Struct/` - 形式理论体系
3. `docs/formal-methods/` - 形式化方法

### 对于工程师
1. `docs/Flink/` - Flink 专项文档
2. `docs/Knowledge/` - 工程知识库
3. `docs/BEST-PRACTICES.md` - 工程最佳实践

## 🔗 相关链接

- **项目主页**: AnalysisDataFlow 知识库
- **知识图谱**: 打开 `website/knowledge-graph-v4.html`
- **定理注册表**: `docs/THEOREM-REGISTRY.md`
- **完整报告**: `docs/100-PERCENT-COMPLETION-FINAL-REPORT.md`

## 📝 许可

本项目遵循开源许可协议。详见项目根目录的 LICENSE 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request。详见 `docs/CONTRIBUTING.md`。

---

**AnalysisDataFlow Team**  
*2026-04-11*
EOF

    log_info "发布说明创建完成"
}

# 统计文件数量
count_files() {
    log_info "统计文件数量..."
    
    DOCS_COUNT=$(find "${RELEASE_DIR}/docs" -type f 2>/dev/null | wc -l)
    PDF_COUNT=$(find "${RELEASE_DIR}/pdf" -type f 2>/dev/null | wc -l)
    WEBSITE_COUNT=$(find "${RELEASE_DIR}/website" -type f 2>/dev/null | wc -l)
    NEO4J_COUNT=$(find "${RELEASE_DIR}/neo4j" -type f 2>/dev/null | wc -l)
    TOOLS_COUNT=$(find "${RELEASE_DIR}/tools" -type f 2>/dev/null | wc -l)
    
    TOTAL_COUNT=$((DOCS_COUNT + PDF_COUNT + WEBSITE_COUNT + NEO4J_COUNT + TOOLS_COUNT))
    
    log_info "文件统计:"
    log_info "  - 文档 (docs/): ${DOCS_COUNT}"
    log_info "  - PDF (pdf/): ${PDF_COUNT}"
    log_info "  - 网站 (website/): ${WEBSITE_COUNT}"
    log_info "  - Neo4j 数据 (neo4j/): ${NEO4J_COUNT}"
    log_info "  - 工具 (tools/): ${TOOLS_COUNT}"
    log_info "  - 总计: ${TOTAL_COUNT}"
    
    # 保存统计信息
    cat > "${RELEASE_DIR}/PACKAGE-INFO.txt" << EOF
AnalysisDataFlow Release v${VERSION}
=====================================
生成日期: $(date '+%Y-%m-%d %H:%M:%S')

文件统计:
- 文档 (docs/): ${DOCS_COUNT} 文件
- PDF (pdf/): ${PDF_COUNT} 文件
- 网站 (website/): ${WEBSITE_COUNT} 文件
- Neo4j 数据 (neo4j/): ${NEO4J_COUNT} 文件
- 工具 (tools/): ${TOOLS_COUNT} 文件
- 总计: ${TOTAL_COUNT} 文件

目录大小:
$(du -sh "${RELEASE_DIR}"/* 2>/dev/null || echo "Size info not available")
EOF
}

# 主函数
main() {
    log_info "开始创建 AnalysisDataFlow v${VERSION} 发布包..."
    log_info "=================================================="
    
    create_directories
    copy_docs
    copy_pdfs
    copy_website
    copy_neo4j
    copy_tools
    create_release_notes
    count_files
    
    log_info "=================================================="
    log_info "发布包创建完成！"
    log_info "发布目录: ${RELEASE_DIR}/"
    
    return 0
}

# 执行主函数
main "$@"
