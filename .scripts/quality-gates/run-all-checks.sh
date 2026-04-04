#!/bin/bash
# run-all-checks.sh
# 质量门禁统一入口 - 顺序执行所有检查
# 返回码: 0=全部通过, 1=有检查失败, 2=执行错误

set -uo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# 脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 检查项定义
declare -a CHECK_NAMES=(
    "前瞻性内容检查"
    "Markdown语法检查"
    "Mermaid语法检查"
    "形式化元素检查"
)

declare -a CHECK_SCRIPTS=(
    "check-prospective-content.sh"
    "check-markdown-syntax.sh"
    "check-mermaid-syntax.sh"
    "check-formal-elements.sh"
)

# 结果追踪
declare -a CHECK_RESULTS=()
declare -a CHECK_EXIT_CODES=()
TOTAL_CHECKS=${#CHECK_SCRIPTS[@]}
PASSED_CHECKS=0
FAILED_CHECKS=0

# 输出函数
print_banner() {
    echo ""
    echo "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo "${CYAN}║${NC} ${BOLD}          AnalysisDataFlow 质量门禁检查套件          ${NC} ${CYAN}║${NC}"
    echo "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "执行时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "工作目录: $(pwd)"
    echo ""
}

print_section() {
    echo ""
    echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo "${BLUE}  $1${NC}"
    echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_pass() {
    echo -e "${GREEN}✓ PASS${NC} $1"
}

print_fail() {
    echo -e "${RED}✗ FAIL${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ INFO${NC} $1"
}

print_separator() {
    echo ""
    echo "${CYAN}────────────────────────────────────────────────────────────${NC}"
    echo ""
}

# 执行单个检查
run_check() {
    local index=$1
    local name="${CHECK_NAMES[$index]}"
    local script="${CHECK_SCRIPTS[$index]}"
    local script_path="${SCRIPT_DIR}/${script}"
    
    print_section "[$((index + 1))/${TOTAL_CHECKS}] ${name}"
    
    # 检查脚本是否存在
    if [[ ! -f "$script_path" ]]; then
        print_fail "脚本不存在: $script_path"
        CHECK_RESULTS+=("${name}: 脚本不存在")
        CHECK_EXIT_CODES+=(2)
        ((FAILED_CHECKS++))
        return 2
    fi
    
    # 检查脚本是否可执行
    if [[ ! -x "$script_path" ]]; then
        print_info "添加执行权限: $script"
        chmod +x "$script_path" 2>/dev/null || {
            print_fail "无法添加执行权限: $script"
            CHECK_RESULTS+=("${name}: 权限错误")
            CHECK_EXIT_CODES+=(2)
            ((FAILED_CHECKS++))
            return 2
        }
    fi
    
    # 执行检查
    print_info "开始执行: $script"
    echo ""
    
    local start_time
    start_time=$(date +%s)
    
    # 执行脚本并捕获输出
    local output
    local exit_code
    output=$("$script_path" 2>&1)
    exit_code=$?
    
    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    # 输出结果
    echo "$output"
    
    echo ""
    echo "执行耗时: ${duration}s | 返回码: $exit_code"
    
    # 记录结果
    if [[ $exit_code -eq 0 ]]; then
        print_pass "${name} 通过"
        CHECK_RESULTS+=("${name}: 通过")
        ((PASSED_CHECKS++))
    else
        print_fail "${name} 失败 (返回码: $exit_code)"
        CHECK_RESULTS+=("${name}: 失败 (返回码: $exit_code)")
        ((FAILED_CHECKS++))
    fi
    
    CHECK_EXIT_CODES+=($exit_code)
    return $exit_code
}

# 生成报告
print_report() {
    print_separator
    
    echo "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo "${CYAN}║${NC} ${BOLD}                     质量门禁检查报告                      ${NC} ${CYAN}║${NC}"
    echo "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "检查时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  检查结果明细"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    for i in "${!CHECK_RESULTS[@]}"; do
        local status_icon
        if [[ ${CHECK_EXIT_CODES[$i]} -eq 0 ]]; then
            status_icon="${GREEN}✓${NC}"
        else
            status_icon="${RED}✗${NC}"
        fi
        printf "  %s %s\n" "$status_icon" "${CHECK_RESULTS[$i]}"
    done
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  统计汇总"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    printf "  总检查项:  ${BOLD}%d${NC}\n" "$TOTAL_CHECKS"
    printf "  通过项:    ${GREEN}%d${NC}\n" "$PASSED_CHECKS"
    printf "  失败项:    ${RED}%d${NC}\n" "$FAILED_CHECKS"
    printf "  通过率:    %.1f%%\n" "$(( PASSED_CHECKS * 100 / TOTAL_CHECKS ))"
    echo ""
    
    # 最终结果
    if [[ $FAILED_CHECKS -eq 0 ]]; then
        echo "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
        echo "${GREEN}║${NC} ${BOLD}           所有质量门禁检查通过 ✓ 可以合并          ${NC} ${GREEN}║${NC}"
        echo "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        return 0
    else
        echo "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
        echo "${RED}║${NC} ${BOLD}        有 ${FAILED_CHECKS} 项质量门禁检查未通过 ✗ 请修复后重试        ${NC} ${RED}║${NC}"
        echo "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        return 1
    fi
}

# 保存报告到文件
save_report() {
    local report_file="${SCRIPT_DIR}/quality-gate-report-$(date +%Y%m%d-%H%M%S).txt"
    
    {
        echo "AnalysisDataFlow 质量门禁检查报告"
        echo "======================================"
        echo "检查时间: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo "检查结果明细:"
        echo "-------------"
        for result in "${CHECK_RESULTS[@]}"; do
            echo "  - $result"
        done
        echo ""
        echo "统计汇总:"
        echo "---------"
        echo "  总检查项: $TOTAL_CHECKS"
        echo "  通过项:   $PASSED_CHECKS"
        echo "  失败项:   $FAILED_CHECKS"
        echo "  通过率:   $(( PASSED_CHECKS * 100 / TOTAL_CHECKS ))%"
        echo ""
        echo "原始返回码: ${CHECK_EXIT_CODES[*]}"
        echo ""
        if [[ $FAILED_CHECKS -eq 0 ]]; then
            echo "结果: 所有检查通过 ✓"
        else
            echo "结果: 有 $FAILED_CHECKS 项检查未通过 ✗"
        fi
    } > "$report_file"
    
    print_info "报告已保存: $report_file"
}

# 使用说明
print_usage() {
    cat << EOF
使用: $(basename "$0") [选项]

选项:
    -h, --help      显示帮助信息
    -q, --quiet     静默模式（减少输出）
    -s, --save      保存报告到文件
    --skip PROSPECTIVE,MD,MERMAID,FORMAL
                    跳过指定检查（逗号分隔）

示例:
    $(basename "$0")                    # 运行所有检查
    $(basename "$0") --skip MERMAID     # 跳过Mermaid检查
    $(basename "$0") -s                 # 运行所有检查并保存报告

返回码:
    0 - 所有检查通过
    1 - 有检查未通过
    2 - 执行错误
EOF
}

# 解析参数
SKIP_CHECKS=()
SAVE_REPORT=false
QUIET=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            print_usage
            exit 0
            ;;
        -q|--quiet)
            QUIET=true
            shift
            ;;
        -s|--save)
            SAVE_REPORT=true
            shift
            ;;
        --skip)
            if [[ -n "${2:-}" ]]; then
                IFS=',' read -ra SKIP_CHECKS <<< "$2"
                shift 2
            else
                echo "错误: --skip 需要参数"
                exit 2
            fi
            ;;
        *)
            echo "未知选项: $1"
            print_usage
            exit 2
            ;;
    esac
done

# 主函数
main() {
    # 显示banner
    if [[ "$QUIET" != "true" ]]; then
        print_banner
    fi
    
    # 执行所有检查
    local overall_exit_code=0
    
    for i in $(seq 0 $((TOTAL_CHECKS - 1))); do
        local should_skip=false
        
        # 检查是否需要跳过
        for skip in "${SKIP_CHECKS[@]}"; do
            case "$skip" in
                PROSPECTIVE|prospective)
                    [[ $i -eq 0 ]] && should_skip=true
                    ;;
                MD|md|MARKDOWN|markdown)
                    [[ $i -eq 1 ]] && should_skip=true
                    ;;
                MERMAID|mermaid)
                    [[ $i -eq 2 ]] && should_skip=true
                    ;;
                FORMAL|formal)
                    [[ $i -eq 3 ]] && should_skip=true
                    ;;
            esac
        done
        
        if [[ "$should_skip" == "true" ]]; then
            print_info "跳过: ${CHECK_NAMES[$i]}"
            CHECK_RESULTS+=("${CHECK_NAMES[$i]}: 已跳过")
            CHECK_EXIT_CODES+=(0)
            continue
        fi
        
        # 执行检查
        run_check "$i"
        local result=$?
        
        if [[ $result -ne 0 ]]; then
            overall_exit_code=1
        fi
    done
    
    # 生成报告
    if [[ "$QUIET" != "true" ]]; then
        print_report
    fi
    
    # 保存报告
    if [[ "$SAVE_REPORT" == "true" ]]; then
        save_report
    fi
    
    # 简单输出（静默模式）
    if [[ "$QUIET" == "true" ]]; then
        if [[ $overall_exit_code -eq 0 ]]; then
            echo "质量门禁通过: ${PASSED_CHECKS}/${TOTAL_CHECKS}"
        else
            echo "质量门禁失败: ${FAILED_CHECKS}/${TOTAL_CHECKS} 项未通过"
        fi
    fi
    
    exit $overall_exit_code
}

# 执行主函数
main "$@"
