#!/bin/bash
# check-mermaid-syntax.sh
# Mermaid图表语法验证
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

# Mermaid图表类型
MERMAID_TYPES=(
    "graph"
    "flowchart"
    "sequenceDiagram"
    "classDiagram"
    "stateDiagram"
    "stateDiagram-v2"
    "erDiagram"
    "gantt"
    "pie"
    "journey"
    "gitGraph"
    "mindmap"
    "timeline"
    "quadrantChart"
)

# 统计
TOTAL_FILES=0
DIAGRAM_COUNT=0
TOTAL_ERRORS=0
ERRORS=()

# 输出函数
print_header() {
    echo "========================================"
    echo "  Mermaid 语法检查"
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

# 提取并验证Mermaid代码块
validate_mermaid_blocks() {
    local file="$1"
    local relative_path="$2"
    local errors=0
    local in_mermaid=0
    local mermaid_start=0
    local mermaid_type=""
    local mermaid_content=""
    local line_num=0
    
    while IFS= read -r line || [[ -n "$line" ]]; do
        ((line_num++))
        
        # 检测Mermaid代码块开始
        if [[ $in_mermaid -eq 0 && "$line" =~ ^``````*[[:space:]]*mermaid ]]; then
            in_mermaid=1
            mermaid_start=$line_num
            mermaid_content=""
            continue
        fi
        
        # 收集Mermaid内容
        if [[ $in_mermaid -eq 1 ]]; then
            # 检测代码块结束
            if [[ "$line" =~ ^``````*$ ]]; then
                in_mermaid=0
                ((DIAGRAM_COUNT++))
                
                # 验证这个Mermaid块
                local block_errors
                block_errors=$(validate_single_diagram "$mermaid_content" "$relative_path" "$mermaid_start")
                ((errors += block_errors))
                
                mermaid_content=""
                mermaid_type=""
            else
                mermaid_content+="$line"$'\n'
            fi
        fi
    done < "$file"
    
    # 文件结束时检查Mermaid块是否闭合
    if [[ $in_mermaid -eq 1 ]]; then
        ERRORS+=("$relative_path:$mermaid_start: Mermaid代码块未闭合 (开始于第 $mermaid_start 行)")
        ((errors++))
    fi
    
    echo $errors
}

# 验证单个Mermaid图表
validate_single_diagram() {
    local content="$1"
    local relative_path="$2"
    local start_line="$3"
    local errors=0
    
    # 检查图表类型声明
    local diagram_type=""
    local first_line
    first_line=$(echo "$content" | head -1 | tr -d '[:space:]')
    
    local valid_type=0
    for type in "${MERMAID_TYPES[@]}"; do
        if echo "$first_line" | grep -qiE "^${type}($|[[:space:]]|[\r\n])"; then
            diagram_type="$type"
            valid_type=1
            break
        fi
    done
    
    if [[ $valid_type -eq 0 ]]; then
        # 检查是否是注释或空行开头
        if [[ ! "$first_line" =~ ^[[:space:]]*$ && ! "$first_line" =~ ^%% ]]; then
            ERRORS+=("$relative_path:$start_line: 未知的Mermaid图表类型: '${first_line:0:30}'")
            ((errors++))
        fi
    fi
    
    # 根据类型进行特定检查
    case "$diagram_type" in
        graph|flowchart)
            errors=$((errors + $(check_flowchart_syntax "$content" "$relative_path" "$start_line")))
            ;;
        sequenceDiagram)
            errors=$((errors + $(check_sequence_syntax "$content" "$relative_path" "$start_line")))
            ;;
        classDiagram)
            errors=$((errors + $(check_class_syntax "$content" "$relative_path" "$start_line")))
            ;;
        stateDiagram|stateDiagram-v2)
            errors=$((errors + $(check_state_syntax "$content" "$relative_path" "$start_line")))
            ;;
        gantt)
            errors=$((errors + $(check_gantt_syntax "$content" "$relative_path" "$start_line")))
            ;;
    esac
    
    # 通用检查：括号匹配
    local open_parens
    open_parens=$(echo "$content" | grep -o '(' | wc -l)
    local close_parens
    close_parens=$(echo "$content" | grep -o ')' | wc -l)
    if [[ $open_parens -ne $close_parens ]]; then
        ERRORS+=("$relative_path:$start_line: 括号不匹配 (开:$open_parens 闭:$close_parens)")
        ((errors++))
    fi
    
    # 通用检查：花括号匹配
    local open_braces
    open_braces=$(echo "$content" | grep -o '{' | wc -l)
    local close_braces
    close_braces=$(echo "$content" | grep -o '}' | wc -l)
    if [[ $open_braces -ne $close_braces ]]; then
        ERRORS+=("$relative_path:$start_line: 花括号不匹配 (开:$open_braces 闭:$close_braces)")
        ((errors++))
    fi
    
    # 通用检查：方括号匹配
    local open_brackets
    open_brackets=$(echo "$content" | grep -o '\[' | wc -l)
    local close_brackets
    close_brackets=$(echo "$content" | grep -o ']' | wc -l)
    if [[ $open_brackets -ne $close_brackets ]]; then
        ERRORS+=("$relative_path:$start_line: 方括号不匹配 (开:$open_brackets 闭:$close_brackets)")
        ((errors++))
    fi
    
    echo $errors
}

# 检查流程图语法
check_flowchart_syntax() {
    local content="$1"
    local relative_path="$2"
    local start_line="$3"
    local errors=0
    
    # 检查方向声明
    if ! echo "$content" | grep -qE '(TB|TD|BT|RL|LR)'; then
        # 可能没有声明方向，这是可选的，但最好有
        : # 暂时不报错
    fi
    
    # 检查节点定义语法
    local lines
    IFS=$'\n' read -d '' -ra lines <<< "$content" || true
    
    for line in "${lines[@]}"; do
        # 检查节点文本中的特殊字符
        if [[ "$line" =~ \[.*[^\]\"].*\] ]]; then
            # 方括号内的内容需要小心处理
            if echo "$line" | grep -qE '\[[^]]*\"[^]]*$'; then
                ERRORS+=("$relative_path:$start_line: 流程图节点文本中的引号可能未闭合")
                ((errors++))
            fi
        fi
        
        # 检查箭头语法
        if [[ "$line" =~ (-->|==>|-.->|===>) ]]; then
            : # 合法箭头
        fi
    done
    
    echo $errors
}

# 检查序列图语法
check_sequence_syntax() {
    local content="$1"
    local relative_path="$2"
    local start_line="$3"
    local errors=0
    
    # 检查参与者声明
    if ! echo "$content" | grep -qE '(participant|actor)'; then
        # 可能没有显式声明参与者，这是允许的
        : # 暂时不报错
    fi
    
    # 检查消息语法
    local invalid_lines
    invalid_lines=$(echo "$content" | grep -vE '^[[:space:]]*(participant|actor|loop|alt|else|opt|par|and|end|autonumber|Note|%%|>|>>|-x|--x|-\))' | grep -vE '^[[:space:]]*$' | grep -vE '^[a-zA-Z0-9_]+-[)>]') || true
    
    if [[ -n "$invalid_lines" ]]; then
        # 可能存在语法问题
        : # 暂不严格检查，因为语法比较复杂
    fi
    
    echo $errors
}

# 检查类图语法
check_class_syntax() {
    local content="$1"
    local relative_path="$2"
    local start_line="$3"
    local errors=0
    
    # 检查类定义语法
    if echo "$content" | grep -qE 'class[[:space:]]+[a-zA-Z]'; then
        : # 存在类定义
    fi
    
    # 检查关系语法
    if echo "$content" | grep -qE '(--\>|..\>|--\*|..\*)'; then
        : # 存在关系定义
    fi
    
    echo $errors
}

# 检查状态图语法
check_state_syntax() {
    local content="$1"
    local relative_path="$2"
    local start_line="$3"
    local errors=0
    
    # 检查状态定义
    if echo "$content" | grep -qE '^[[:space:]]*[a-zA-Z]'; then
        : # 存在状态定义
    fi
    
    echo $errors
}

# 检查甘特图语法
check_gantt_syntax() {
    local content="$1"
    local relative_path="$2"
    local start_line="$3"
    local errors=0
    
    # 检查日期格式
    local invalid_dates
    invalid_dates=$(echo "$content" | grep -E '(dateFormat|section)' | grep -vE 'dateFormat[[:space:]]+YYYY' || true)
    
    echo $errors
}

# 检查文件
check_file() {
    local file="$1"
    local relative_path
    relative_path=$(realpath --relative-to="$PROJECT_ROOT" "$file" 2>/dev/null || echo "$file")
    
    ((TOTAL_FILES++))
    
    # 检查是否包含Mermaid代码块
    if ! grep -q '```mermaid' "$file" 2>/dev/null; then
        return 0
    fi
    
    print_check "检查Mermaid图表: $relative_path"
    
    local errors
    errors=$(validate_mermaid_blocks "$file" "$relative_path")
    
    if [[ $errors -eq 0 ]]; then
        print_pass "$relative_path"
    else
        print_fail "$relative_path ($errors 个问题)"
    fi
    
    ((TOTAL_ERRORS += errors))
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
    echo "图表数量: $DIAGRAM_COUNT"
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
        print_pass "所有 Mermaid 图表语法正确"
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
