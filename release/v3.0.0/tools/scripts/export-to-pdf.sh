#!/bin/bash
# =============================================================================
# AnalysisDataFlow PDF 导出脚本
# =============================================================================
# 功能：将推导链文档导出为 PDF 格式
# 支持：单文件导出、批量导出、合并导出
# 工具：pandoc + wkhtmltopdf / markdown-pdf
#
# 用法:
#   ./export-to-pdf.sh single <file.md> [output.pdf]     # 导出单个文件
#   ./export-to-pdf.sh batch <directory> [output_dir]    # 批量导出目录
#   ./export-to-pdf.sh merge <file1.md> <file2.md> ...   # 合并多个文件
#   ./export-to-pdf.sh chain <chain_name>                # 导出推导链
#   ./export-to-pdf.sh index                             # 生成PDF索引
#   ./export-to-pdf.sh check                             # 检查依赖
#
# 示例:
#   ./export-to-pdf.sh single Struct/00-INDEX.md
#   ./export-to-pdf.sh batch Struct/ pdf/struct/
#   ./export-to-pdf.sh chain flink-architecture
#   ./export-to-pdf.sh index
# =============================================================================

set -e

# 脚本配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PDF_OUTPUT_DIR="$PROJECT_ROOT/pdf"
COVER_TEMPLATE="$SCRIPT_DIR/pdf-cover.md"
STYLES_CSS="$SCRIPT_DIR/pdf-styles.css"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[OK]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# =============================================================================
# 依赖检查
# =============================================================================
check_dependencies() {
    print_info "检查依赖环境..."
    
    local missing=()
    
    # 检查必需工具
    if ! command -v pandoc &> /dev/null; then
        missing+=("pandoc")
    fi
    
    if ! command -v wkhtmltopdf &> /dev/null; then
        missing+=("wkhtmltopdf")
    fi
    
    # 检查可选工具
    local optional_missing=()
    if ! command -v markdown-pdf &> /dev/null; then
        optional_missing+=("markdown-pdf (Node.js)")
    fi
    
    if [ ${#missing[@]} -ne 0 ]; then
        print_error "缺少必需依赖: ${missing[*]}"
        echo ""
        echo "安装指南:"
        echo "  Ubuntu/Debian:"
        echo "    sudo apt-get install pandoc wkhtmltopdf"
        echo ""
        echo "  macOS:"
        echo "    brew install pandoc wkhtmltopdf"
        echo ""
        echo "  Windows (Chocolatey):"
        echo "    choco install pandoc wkhtmltopdf"
        echo ""
        return 1
    fi
    
    print_success "所有必需依赖已安装"
    
    if [ ${#optional_missing[@]} -ne 0 ]; then
        print_warning "可选工具未安装: ${optional_missing[*]}"
        echo "  如需使用 markdown-pdf: npm install -g markdown-pdf"
    fi
    
    # 显示版本
    echo ""
    echo "工具版本:"
    pandoc --version | head -1
    wkhtmltopdf --version | head -1
    
    return 0
}

# =============================================================================
# 初始化目录
# =============================================================================
init_directories() {
    mkdir -p "$PDF_OUTPUT_DIR"
    mkdir -p "$PDF_OUTPUT_DIR/struct"
    mkdir -p "$PDF_OUTPUT_DIR/knowledge"
    mkdir -p "$PDF_OUTPUT_DIR/flink"
    mkdir -p "$PDF_OUTPUT_DIR/chains"
    mkdir -p "$PDF_OUTPUT_DIR/merged"
}

# =============================================================================
# 生成封面 HTML
# =============================================================================
generate_cover_html() {
    local title="$1"
    local subtitle="${2:-AnalysisDataFlow Project}"
    local date_str=$(date +"%Y-%m-%d")
    
    cat << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>$title</title>
    <style>
        @page {
            margin: 0;
            size: A4;
        }
        body {
            margin: 0;
            padding: 0;
            font-family: "Noto Serif CJK SC", "Source Han Serif SC", "SimSun", serif;
            background: linear-gradient(135deg, #1f4e79 0%, #3a7bd5 100%);
            height: 297mm;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
        }
        .badge {
            font-size: 24pt;
            letter-spacing: 8px;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        .title {
            font-size: 36pt;
            font-weight: bold;
            margin-bottom: 20px;
            padding: 0 40px;
            line-height: 1.3;
        }
        .subtitle {
            font-size: 16pt;
            opacity: 0.85;
            margin-bottom: 60px;
        }
        .divider {
            width: 200px;
            height: 3px;
            background: #c5a464;
            margin: 30px 0;
        }
        .meta {
            font-size: 12pt;
            opacity: 0.8;
            line-height: 2;
        }
        .footer {
            position: absolute;
            bottom: 40px;
            font-size: 10pt;
            opacity: 0.6;
        }
    </style>
</head>
<body>
    <div class="badge">ANALYSISDATAFLOW</div>
    <div class="title">$title</div>
    <div class="subtitle">$subtitle</div>
    <div class="divider"></div>
    <div class="meta">
        <div>PDF 导出日期: $date_str</div>
        <div>流计算领域权威知识库</div>
    </div>
    <div class="footer">https://github.com/AnalysisDataFlow</div>
</body>
</html>
EOF
}

# =============================================================================
# 导出单个文件 (使用 pandoc + wkhtmltopdf)
# =============================================================================
export_single() {
    local input_file="$1"
    local output_file="${2:-}"
    
    if [ ! -f "$input_file" ]; then
        print_error "文件不存在: $input_file"
        return 1
    fi
    
    # 自动确定输出路径
    if [ -z "$output_file" ]; then
        local basename=$(basename "$input_file" .md)
        output_file="$PDF_OUTPUT_DIR/${basename}.pdf"
    fi
    
    # 提取标题
    local title=$(grep -m1 "^# " "$input_file" | sed 's/^# //')
    if [ -z "$title" ]; then
        title=$(basename "$input_file" .md)
    fi
    
    print_info "导出: $input_file -> $output_file"
    
    # 创建临时目录
    local temp_dir=$(mktemp -d)
    trap "rm -rf $temp_dir" EXIT
    
    # 生成封面
    generate_cover_html "$title" > "$temp_dir/cover.html"
    
    # 转换封面为 PDF
    wkhtmltopdf \
        --page-size A4 \
        --margin-top 0 \
        --margin-bottom 0 \
        --margin-left 0 \
        --margin-right 0 \
        "$temp_dir/cover.html" \
        "$temp_dir/cover.pdf" 2>/dev/null
    
    # 使用 pandoc 转换正文
    pandoc "$input_file" \
        --pdf-engine=wkhtmltopdf \
        --css="$STYLES_CSS" \
        --toc \
        --toc-depth=3 \
        --number-sections \
        -V geometry:margin=2.5cm \
        -V colorlinks=true \
        -V linkcolor=blue \
        -V urlcolor=blue \
        -o "$temp_dir/content.pdf"
    
    # 合并封面和正文
    if command -v pdfunite &> /dev/null; then
        pdfunite "$temp_dir/cover.pdf" "$temp_dir/content.pdf" "$output_file"
    else
        # 如果没有 pdfunite，只输出内容
        cp "$temp_dir/content.pdf" "$output_file"
        print_warning "未安装 pdfunite，封面未合并"
    fi
    
    if [ -f "$output_file" ]; then
        local size=$(du -h "$output_file" | cut -f1)
        print_success "导出成功: $output_file ($size)"
        return 0
    else
        print_error "导出失败"
        return 1
    fi
}

# =============================================================================
# 批量导出目录
# =============================================================================
export_batch() {
    local input_dir="$1"
    local output_dir="${2:-$PDF_OUTPUT_DIR}"
    
    if [ ! -d "$input_dir" ]; then
        print_error "目录不存在: $input_dir"
        return 1
    fi
    
    # 查找所有 Markdown 文件
    local md_files=($(find "$input_dir" -name "*.md" -type f ! -path "*/.git/*" ! -path "*/node_modules/*"))
    local total=${#md_files[@]}
    
    if [ $total -eq 0 ]; then
        print_warning "未找到 Markdown 文件: $input_dir"
        return 0
    fi
    
    print_info "批量导出: $total 个文件"
    print_info "输出目录: $output_dir"
    echo ""
    
    local success=0
    local failed=0
    
    for ((i=0; i<$total; i++)); do
        local file="${md_files[$i]}"
        local basename=$(basename "$file" .md)
        local rel_path=$(dirname "$file" | sed "s|$input_dir/||")
        
        local out_dir="$output_dir"
        if [ "$rel_path" != "." ] && [ -n "$rel_path" ]; then
            out_dir="$output_dir/$rel_path"
            mkdir -p "$out_dir"
        fi
        
        echo -n "[$((i+1))/$total] $basename ... "
        
        if export_single "$file" "$out_dir/${basename}.pdf" > /dev/null 2>&1; then
            echo -e "${GREEN}OK${NC}"
            ((success++))
        else
            echo -e "${RED}FAIL${NC}"
            ((failed++))
        fi
    done
    
    echo ""
    print_success "完成: $success 成功, $failed 失败"
    
    return 0
}

# =============================================================================
# 合并导出多个文件
# =============================================================================
export_merge() {
    local output_file="$1"
    shift
    local input_files=("$@")
    
    if [ ${#input_files[@]} -eq 0 ]; then
        print_error "未指定输入文件"
        return 1
    fi
    
    print_info "合并导出 ${#input_files[@]} 个文件 -> $output_file"
    
    # 创建临时目录
    local temp_dir=$(mktemp -d)
    trap "rm -rf $temp_dir" EXIT
    
    # 合并 Markdown 内容
    local merged_md="$temp_dir/merged.md"
    echo "---" > "$merged_md"
    echo "title: AnalysisDataFlow 文档合集" >> "$merged_md"
    echo "date: $(date +%Y-%m-%d)" >> "$merged_md"
    echo "---" >> "$merged_md"
    echo "" >> "$merged_md"
    
    for file in "${input_files[@]}"; do
        if [ -f "$file" ]; then
            echo -e "\n\\newpage\n" >> "$merged_md"
            cat "$file" >> "$merged_md"
            echo "" >> "$merged_md"
        else
            print_warning "跳过不存在的文件: $file"
        fi
    done
    
    # 导出合并后的文件
    export_single "$merged_md" "$output_file"
}

# =============================================================================
# 导出推导链
# =============================================================================
export_chain() {
    local chain_name="$1"
    
    # 定义推导链映射
    declare -A chains
    chains["struct-basics"]="Struct/00-INDEX.md Struct/01-streaming-model-intro.md"
    chains["knowledge-patterns"]="Knowledge/00-INDEX.md Knowledge/design-patterns/"
    chains["flink-architecture"]="Flink/00-INDEX.md Flink/01-flink-intro.md"
    chains["streaming-concepts"]="STREAMING-CONCEPTS-COMPREHENSIVE-ANALYSIS.md"
    chains["design-principles"]="DESIGN-PRINCIPLES.md"
    chains["best-practices"]="BEST-PRACTICES.md"
    
    if [ -z "${chains[$chain_name]}" ]; then
        print_error "未知的推导链: $chain_name"
        echo "可用的推导链:"
        for key in "${!chains[@]}"; do
            echo "  - $key"
        done
        return 1
    fi
    
    local chain_files=(${chains[$chain_name]})
    local resolved_files=()
    
    # 解析文件路径
    for item in "${chain_files[@]}"; do
        if [ -f "$PROJECT_ROOT/$item" ]; then
            resolved_files+=("$PROJECT_ROOT/$item")
        elif [ -d "$PROJECT_ROOT/$item" ]; then
            while IFS= read -r file; do
                resolved_files+=("$file")
            done < <(find "$PROJECT_ROOT/$item" -name "*.md" -type f | sort)
        fi
    done
    
    local output_file="$PDF_OUTPUT_DIR/chains/${chain_name}.pdf"
    mkdir -p "$(dirname "$output_file")"
    
    print_info "导出推导链: $chain_name"
    print_info "包含文件: ${#resolved_files[@]} 个"
    
    export_merge "$output_file" "${resolved_files[@]}"
}

# =============================================================================
# 生成 PDF 索引
# =============================================================================
generate_index() {
    print_info "生成 PDF 索引..."
    
    local index_file="$PDF_OUTPUT_DIR/README.md"
    local date_str=$(date +"%Y-%m-%d %H:%M:%S")
    
    cat > "$index_file" << EOF
# AnalysisDataFlow PDF 文档索引

> 自动生成于 $date_str

## 目录结构

### 📊 Struct/ - 形式理论
形式化定义、定理证明、严格推导

| 文件名 | 大小 | 描述 |
|--------|------|------|
EOF

    # 添加 Struct PDFs
    if [ -d "$PDF_OUTPUT_DIR/struct" ]; then
        for pdf in "$PDF_OUTPUT_DIR/struct"/*.pdf; do
            if [ -f "$pdf" ]; then
                local name=$(basename "$pdf")
                local size=$(du -h "$pdf" | cut -f1)
                echo "| $name | $size | - |" >> "$index_file"
            fi
        done
    fi
    
    cat >> "$index_file" << EOF

### 📚 Knowledge/ - 知识结构
设计模式、最佳实践、业务建模

| 文件名 | 大小 | 描述 |
|--------|------|------|
EOF

    # 添加 Knowledge PDFs
    if [ -d "$PDF_OUTPUT_DIR/knowledge" ]; then
        for pdf in "$PDF_OUTPUT_DIR/knowledge"/*.pdf; do
            if [ -f "$pdf" ]; then
                local name=$(basename "$pdf")
                local size=$(du -h "$pdf" | cut -f1)
                echo "| $name | $size | - |" >> "$index_file"
            fi
        done
    fi
    
    cat >> "$index_file" << EOF

### 🔥 Flink/ - Flink 专项
Flink 架构、机制、对比、路线图

| 文件名 | 大小 | 描述 |
|--------|------|------|
EOF

    # 添加 Flink PDFs
    if [ -d "$PDF_OUTPUT_DIR/flink" ]; then
        for pdf in "$PDF_OUTPUT_DIR/flink"/*.pdf; do
            if [ -f "$pdf" ]; then
                local name=$(basename "$pdf")
                local size=$(du -h "$pdf" | cut -f1)
                echo "| $name | $size | - |" >> "$index_file"
            fi
        done
    fi
    
    cat >> "$index_file" << EOF

### 🔗 推导链合集

| 文件名 | 大小 | 描述 |
|--------|------|------|
EOF

    # 添加 Chain PDFs
    if [ -d "$PDF_OUTPUT_DIR/chains" ]; then
        for pdf in "$PDF_OUTPUT_DIR/chains"/*.pdf; do
            if [ -f "$pdf" ]; then
                local name=$(basename "$pdf")
                local size=$(du -h "$pdf" | cut -f1)
                echo "| $name | $size | - |" >> "$index_file"
            fi
        done
    fi
    
    cat >> "$index_file" << EOF

## 导出命令参考

\`\`\`bash
# 导出单个文件
./scripts/export-to-pdf.sh single Struct/00-INDEX.md

# 批量导出目录
./scripts/export-to-pdf.sh batch Struct/ pdf/struct/

# 导出推导链
./scripts/export-to-pdf.sh chain flink-architecture

# 合并多个文件
./scripts/export-to-pdf.sh merge output.pdf file1.md file2.md file3.md
\`\`\`

---

*AnalysisDataFlow Project | 流计算领域权威知识库*
EOF

    print_success "索引已生成: $index_file"
}

# =============================================================================
# 显示帮助
# =============================================================================
show_help() {
    cat << EOF
AnalysisDataFlow PDF 导出脚本

用法:
  $0 <command> [options]

命令:
  check                           检查依赖环境
  single <file.md> [output.pdf]   导出单个文件
  batch <dir> [output_dir]        批量导出目录
  merge <out.pdf> <files...>      合并多个文件
  chain <chain_name>              导出推导链
  index                           生成PDF索引

推导链:
  struct-basics       Struct 基础理论
  knowledge-patterns  Knowledge 设计模式
  flink-architecture  Flink 架构体系
  streaming-concepts  流计算概念分析
  design-principles   设计原则
  best-practices      最佳实践

示例:
  $0 check
  $0 single README.md
  $0 batch Struct/ pdf/struct/
  $0 chain flink-architecture
  $0 index

依赖:
  - pandoc (必需)
  - wkhtmltopdf (必需)
  - pdfunite (可选, 用于合并封面)

安装:
  Ubuntu/Debian: sudo apt-get install pandoc wkhtmltopdf poppler-utils
  macOS:         brew install pandoc wkhtmltopdf poppler
  Windows:       choco install pandoc wkhtmltopdf
EOF
}

# =============================================================================
# 主函数
# =============================================================================
main() {
    # 初始化
    init_directories
    
    # 检查是否有命令
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    local command="$1"
    shift
    
    case "$command" in
        check)
            check_dependencies
            ;;
        single)
            if [ $# -lt 1 ]; then
                print_error "用法: $0 single <file.md> [output.pdf]"
                exit 1
            fi
            check_dependencies && export_single "$@"
            ;;
        batch)
            if [ $# -lt 1 ]; then
                print_error "用法: $0 batch <directory> [output_dir]"
                exit 1
            fi
            check_dependencies && export_batch "$@"
            ;;
        merge)
            if [ $# -lt 2 ]; then
                print_error "用法: $0 merge <output.pdf> <file1.md> [file2.md...]"
                exit 1
            fi
            check_dependencies && export_merge "$@"
            ;;
        chain)
            if [ $# -lt 1 ]; then
                print_error "用法: $0 chain <chain_name>"
                exit 1
            fi
            check_dependencies && export_chain "$@"
            ;;
        index)
            generate_index
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
