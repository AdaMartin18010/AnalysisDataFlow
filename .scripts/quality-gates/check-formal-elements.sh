#!/bin/bash
# check-formal-elements.sh
# 形式化元素检查：定理/定义编号唯一性、引用格式
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

# 形式化元素模式
FORMAL_PATTERNS=(
    'Thm-[SKF]-[0-9]{2}-[0-9]{2,}'      # 定理
    'Lemma-[SKF]-[0-9]{2}-[0-9]{2,}'    # 引理
    'Def-[SKF]-[0-9]{2}-[0-9]{2,}'      # 定义
    'Prop-[SKF]-[0-9]{2}-[0-9]{2,}'     # 命题
    'Cor-[SKF]-[0-9]{2}-[0-9]{2,}'      # 推论
)

# 编号追踪
declare -A SEEN_THMS
declare -A SEEN_LEMMAS
declare -A SEEN_DEFS
declare -A SEEN_PROPS
declare -A SEEN_CORS

# 统计
TOTAL_FILES=0
TOTAL_ERRORS=0
ERRORS=()

# 输出函数
print_header() {
    echo "========================================"
    echo "  形式化元素检查"
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

# 检查编号唯一性
check_unique_ids() {
    local file="$1"
    local relative_path="$2"
    local errors=0
    local line_num=0
    
    while IFS= read -r line || [[ -n "$line" ]]; do
        ((line_num++))
        
        # 检查定理
        if [[ "$line" =~ (Thm-[SKF]-[0-9]{2}-[0-9]{2,}) ]]; then
            local id="${BASH_REMATCH[1]}"
            if [[ -n "${SEEN_THMS[$id]:-}" ]]; then
                ERRORS+=("$relative_path:$line_num: 定理编号重复: $id (首次出现在 ${SEEN_THMS[$id]})")
                ((errors++))
            else
                SEEN_THMS[$id]="$relative_path:$line_num"
            fi
        fi
        
        # 检查引理
        if [[ "$line" =~ (Lemma-[SKF]-[0-9]{2}-[0-9]{2,}) ]]; then
            local id="${BASH_REMATCH[1]}"
            if [[ -n "${SEEN_LEMMAS[$id]:-}" ]]; then
                ERRORS+=("$relative_path:$line_num: 引理编号重复: $id (首次出现在 ${SEEN_LEMMAS[$id]})")
                ((errors++))
            else
                SEEN_LEMMAS[$id]="$relative_path:$line_num"
            fi
        fi
        
        # 检查定义
        if [[ "$line" =~ (Def-[SKF]-[0-9]{2}-[0-9]{2,}) ]]; then
            local id="${BASH_REMATCH[1]}"
            if [[ -n "${SEEN_DEFS[$id]:-}" ]]; then
                ERRORS+=("$relative_path:$line_num: 定义编号重复: $id (首次出现在 ${SEEN_DEFS[$id]})")
                ((errors++))
            else
                SEEN_DEFS[$id]="$relative_path:$line_num"
            fi
        fi
        
        # 检查命题
        if [[ "$line" =~ (Prop-[SKF]-[0-9]{2}-[0-9]{2,}) ]]; then
            local id="${BASH_REMATCH[1]}"
            if [[ -n "${SEEN_PROPS[$id]:-}" ]]; then
                ERRORS+=("$relative_path:$line_num: 命题编号重复: $id (首次出现在 ${SEEN_PROPS[$id]})")
                ((errors++))
            else
                SEEN_PROPS[$id]="$relative_path:$line_num"
            fi
        fi
        
        # 检查推论
        if [[ "$line" =~ (Cor-[SKF]-[0-9]{2}-[0-9]{2,}) ]]; then
            local id="${BASH_REMATCH[1]}"
            if [[ -n "${SEEN_CORS[$id]:-}" ]]; then
                ERRORS+=("$relative_path:$line_num: 推论编号重复: $id (首次出现在 ${SEEN_CORS[$id]})")
                ((errors++))
            else
                SEEN_CORS[$id]="$relative_path:$line_num"
            fi
        fi
    done < "$file"
    
    echo $errors
}

# 检查引用格式
check_reference_format() {
    local file="$1"
    local relative_path="$2"
    local errors=0
    local line_num=0
    
    while IFS= read -r line || [[ -n "$line" ]]; do
        ((line_num++))
        
        # 检查引用格式 [^n] (上标格式)
        # 合法: [^1], [^123], [^label]
        # 非法: [^ 1], [^1 ], [^1^2], 等等
        
        # 查找所有可能的引用
        local refs
        refs=$(echo "$line" | grep -oE '\[\^[[:alnum:]_-]+\]' || true)
        
        if [[ -n "$refs" ]]; then
            # 检查是否有空格问题
            if echo "$line" | grep -qE '\[\^[[:space:]]'; then
                ERRORS+=("$relative_path:$line_num: 引用格式错误: 引用标签前有空格 [^ ...]")
                ((errors++))
            fi
            
            if echo "$line" | grep -qE '\[\^[[:alnum:]_-]+[[:space:]]+\]'; then
                ERRORS+=("$relative_path:$line_num: 引用格式错误: 引用标签后有空格 [^label ...]")
                ((errors++))
            fi
        fi
        
        # 检查引用列表格式（文档末尾的引用定义）
        # 合法: [^1]: 引用内容
        # 非法: [^1]:, [^1] 内容（缺少冒号）
        if [[ "$line" =~ ^\[\^[[:alnum:]_-]+\][[:space:]]*[^:] ]]; then
            # 这可能是引用定义但缺少冒号
            if echo "$line" | grep -qE '^\[\^[[:alnum:]_-]+\][[:space:]]+[A-Za-z]'; then
                # 确认不是普通文本中的引用使用
                local prev_context
                prev_context=$(sed -n "$((line_num - 3)),$((line_num - 1))p" "$file" 2>/dev/null || true)
                if echo "$prev_context" | grep -qE '^\[\^[[:alnum:]_-]+\]:'; then
                    # 前面有引用定义，这可能是连续的引用定义
                    ERRORS+=("$relative_path:$line_num: 引用定义格式错误: 可能缺少冒号 [^label]: 内容")
                    ((errors++))
                fi
            fi
        fi
        
        # 检查引用列表是否在文档末尾
        # 这是一个软性检查，不报错但记录
        
    done < "$file"
    
    echo $errors
}

# 检查编号连续性（建议）
check_id_continuity() {
    local file="$1"
    local relative_path="$2"
    local errors=0
    
    # 提取所有编号
    local all_ids
    all_ids=$(grep -oE '(Thm|Lemma|Def|Prop|Cor)-[SKF]-[0-9]{2}-[0-9]{2,}' "$file" 2>/dev/null | sort -u || true)
    
    if [[ -z "$all_ids" ]]; then
        echo 0
        return
    fi
    
    # 按类型分组检查连续性
    local types=("Thm" "Lemma" "Def" "Prop" "Cor")
    
    for type in "${types[@]}"; do
        local type_ids
        type_ids=$(echo "$all_ids" | grep "^$type-" | sort -t'-' -k4 -n || true)
        
        if [[ -z "$type_ids" ]]; then
            continue
        fi
        
        # 检查连续性（简单检查，不严格）
        local prev_num=0
        while IFS= read -r id; do
            if [[ "$id" =~ -([0-9]+)$ ]]; then
                local num="${BASH_REMATCH[1]}"
                if [[ $prev_num -ne 0 && $num -ne $((prev_num + 1)) && $num -ne $prev_num ]]; then
                    # 编号不连续（跳过是可以接受的，所以只是建议）
                    : # 暂不报错，只是信息
                fi
                prev_num=$num
            fi
        done <<< "$type_ids"
    done
    
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
    
    # 检查编号唯一性
    print_check "检查编号唯一性: $relative_path"
    errors=$(check_unique_ids "$file" "$relative_path")
    ((file_errors += errors))
    
    # 检查引用格式
    print_check "检查引用格式: $relative_path"
    errors=$(check_reference_format "$file" "$relative_path")
    ((file_errors += errors))
    
    # 检查编号连续性（建议）
    print_check "检查编号连续性: $relative_path"
    errors=$(check_id_continuity "$file" "$relative_path")
    ((file_errors += errors))
    
    if [[ $file_errors -eq 0 ]]; then
        print_pass "$relative_path"
    else
        print_fail "$relative_path ($file_errors 个问题)"
    fi
    
    ((TOTAL_ERRORS += file_errors))
    return 0
}

# 输出统计信息
print_statistics() {
    echo ""
    echo "========================================"
    echo "  形式化元素统计"
    echo "========================================"
    echo "定理数量: ${#SEEN_THMS[@]}"
    echo "引理数量: ${#SEEN_LEMMAS[@]}"
    echo "定义数量: ${#SEEN_DEFS[@]}"
    echo "命题数量: ${#SEEN_PROPS[@]}"
    echo "推论数量: ${#SEEN_CORS[@]}"
    echo "总计: $((${#SEEN_THMS[@]} + ${#SEEN_LEMMAS[@]} + ${#SEEN_DEFS[@]} + ${#SEEN_PROPS[@]} + ${#SEEN_CORS[@]}))"
    echo ""
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
    
    # 输出统计
    print_statistics
    
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
        print_pass "所有形式化元素检查通过"
        echo ""
        return 0
    else
        print_fail "发现 $TOTAL_ERRORS 处问题"
        echo ""
        return 1
    fi
}

# 执行主函数
main "$@"
exit $?
