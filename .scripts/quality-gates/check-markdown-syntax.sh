#!/bin/bash
# check-markdown-syntax.sh
# Markdown语法检查：标题层级、代码块闭合、基础语法
# 返回码: 0=通过, 1=发现问题, 2=执行错误

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# 目标目录
TARGET_DIRS=("${PROJECT_ROOT}/Struct" "${PROJECT_ROOT}/Knowledge" "${PROJECT_ROOT}/Flink")

# 统计
TOTAL_FILES=0
TOTAL_ERRORS=0
ERRORS=()

# 输出函数
print_header() {
    echo "========================================"
    echo "  Markdown 语法检查"
    echo "========================================"
    echo ""
}

print_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

print_check() {
    echo -e "${BLUE}[CHECK]${NC} $1"
}

# 检查标题层级
check_heading_levels() {
    local file="$1"
    local relative_path="$2"
    local errors=0
    local prev_level=0
    local line_num=0
    
    while IFS= read -r line || [[ -n "$line" ]]; do
        ((line_num++))
        
        # 检测标题行
        if [[ "$line" =~ ^(#{1,6})[[:space:]] ]]; then
            local current_level=${#BASH_REMATCH[1]}
            
            # 检查标题层级跳跃（不能跳级，如 # 后直接 ###）
            if [[ $prev_level -ne 0 && $current_level -gt $((prev_level + 1)) ]]; then
                ERRORS+=("$relative_path:$line_num: 标题层级跳跃: H$prev_level → H$current_level")
                ((errors++))
            fi
            
            # 检查标题后是否有空格
            if [[ ! "$line" =~ ^#{1,6}[[:space:]]+ ]]; then
                ERRORS+=("$relative_path:$line_num: 标题后缺少空格")
                ((errors++))
            fi
            
            prev_level=$current_level
        fi
        
        # 检查Setext风格标题（下划线）
        if [[ "$line" =~ ^={3,}$ || "$line" =~ ^-{3,}$ ]]; then
            # Setext风格只能在文件开始或前面是空行
            : # 暂时允许，因为可能是合法的
        fi
        done < "$file"
    
    echo $errors
}

# 检查代码块闭合
check_code_blocks() {
    local file="$1"
    local relative_path="$2"
    local errors=0
    local in_code_block=0
    local code_block_start=0
    local fence_type=""
    local line_num=0
    
    while IFS= read -r line || [[ -n "$line" ]]; do
        ((line_num++))
        
        # 检测代码块开始
        if [[ $in_code_block -eq 0 && "$line" =~ ^(``````*)[[:space:]]*([a-zA-Z0-9]*) ]]; then
            in_code_block=1
            fence_type="${BASH_REMATCH[2]}"
            code_block_start=$line_num
        # 检测代码块结束
        elif [[ $in_code_block -eq 1 && "$line" =~ ^(``````*)$ ]]; then
            in_code_block=0
            fence_type=""
        fi
    done < "$file"
    
    # 文件结束时检查代码块是否闭合
    if [[ $in_code_block -eq 1 ]]; then
        ERRORS+=("$relative_path:$code_block_start: 代码块未闭合 (开始于第 $code_block_start 行)")
        ((errors++))
    fi
    
    echo $errors
}

# 检查常见语法错误
check_common_issues() {
    local file="$1"
    local relative_path="$2"
    local errors=0
    local line_num=0
    
    while IFS= read -r line || [[ -n "$line" ]]; do
        ((line_num++))
        
        # 检查连续空行（超过3行可能是有问题）
        # 这个需要前后文，简单检查
        
        # 检查链接语法错误 [](url) -> 应该是 [text](url)
        if [[ "$line" =~ \[\]\( ]]; then
            ERRORS+=("$relative_path:$line_num: 链接语法错误: 缺少链接文本 [text](url)")
            ((errors++))
        fi
        
        # 检查图片语法错误
        if [[ "$line" =~ !\[\]\( ]]; then
            ERRORS+=("$relative_path:$line_num: 图片语法错误: 缺少alt文本 ![alt](url)")
            ((errors++))
        fi
        
        # 检查不规范的列表缩进
        if [[ "$line" =~ ^[[:space:]]{1,3}[-*+][[:space:]] ]]; then
            # 列表缩进不是0、2或4个空格
            local leading_spaces
            leading_spaces=$(echo "$line" | sed 's/^\([[:space:]]*\).*/\1/')
            local space_count=${#leading_spaces}
            if [[ $space_count -ne 0 && $space_count -ne 2 && $space_count -ne 4 ]]; then
                ERRORS+=("$relative_path:$line_num: 列表缩进不规范: ${space_count}空格 (建议使用0/2/4空格)")
                ((errors++))
            fi
        fi
        
        # 检查表格分隔符
        if [[ "$line" =~ ^\|.*\|$ ]]; then
            # 可能是表格行，检查是否有对齐标记
            if [[ "$line" =~ ^\|[-:\|[:space:]]+\|$ ]]; then
                # 这是分隔行，检查格式
                if [[ ! "$line" =~ ^\|([[:space:]]*[:-]-*[:-][[:space:]]*\|)+$ ]]; then
                    ERRORS+=("$relative_path:$line_num: 表格分隔行格式可能有问题")
                    ((errors++))
                fi
            fi
        fi
        
        # 检查HTML标签闭合（简单检查）
        local open_tags
        open_tags=$(echo "$line" | grep -oP '<[a-zA-Z][^>]*>' | grep -v '/>' | grep -v '^</' | wc -l)
        local close_tags
        close_tags=$(echo "$line" | grep -oP '</[a-zA-Z][^>]*>' | wc -l)
        # 简单统计，不精确但有帮助
        
    done < "$file"
    
    echo $errors
}

# 检查文件
check_file() {
    local file="$1"
    local relative_path
    relative_path=$(realpath --relative-to="$PROJECT_ROOT" "$file" 2>/dev/null || echo "$file")
    
    ((TOTAL_FILES++))
    
    local file_errors=0
    local errors=0
    
    # 检查标题层级
    print_check "检查标题层级: $relative_path"
    errors=$(check_heading_levels "$file" "$relative_path")
    ((file_errors += errors))
    
    # 检查代码块
    print_check "检查代码块: $relative_path"
    errors=$(check_code_blocks "$file" "$relative_path")
    ((file_errors += errors))
    
    # 检查常见问题
    print_check "检查常见语法: $relative_path"
    errors=$(check_common_issues "$file" "$relative_path")
    ((file_errors += errors))
    
    if [[ $file_errors -eq 0 ]]; then
        print_pass "$relative_path"
    else
        print_fail "$relative_path ($file_errors 个问题)"
    fi
    
    ((TOTAL_ERRORS += file_errors))
    return 0
}

# 主函数
main() {
    print_header
    
    # 检查目标目录
    for dir in "${TARGET_DIRS[@]}"; do
        if [[ ! -d "$dir" ]]; then
            print_info "目录不存在，跳过: $dir"
            continue
        fi
        
        # 查找所有markdown文件
        while IFS= read -r -d '' file; do
            check_file "$file"
        done < <(find "$dir" -type f -name "*.md" -print0 2>/dev/null || true)
    done
    
    echo ""
    echo "========================================"
    echo "  检查结果汇总"
    echo "========================================"
    echo "扫描文件数: $TOTAL_FILES"
    echo "发现错误数: $TOTAL_ERRORS"
    echo ""
    
    if [[ ${#ERRORS[@]} -gt 0 ]]; then
        echo "详细错误列表:"
        for error in "${ERRORS[@]}"; do
            echo "  - $error"
        done
        echo ""
    fi
    
    if [[ $TOTAL_ERRORS -eq 0 ]]; then
        print_pass "所有 Markdown 文件语法正确"
        echo ""
        return 0
    else
        print_fail "发现 $TOTAL_ERRORS 处语法问题"
        echo ""
        return 1
    fi
}

# 执行主函数
main "$@"
exit $?
