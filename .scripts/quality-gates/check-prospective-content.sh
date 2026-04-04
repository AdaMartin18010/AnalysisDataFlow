#!/bin/bash
# check-prospective-content.sh
# 扫描新增文档中的前瞻性关键词和未标注的虚构API/配置
# 返回码: 0=通过, 1=发现前瞻性内容, 2=执行错误

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# 目标目录
TARGET_DIRS=("${PROJECT_ROOT}/Struct" "${PROJECT_ROOT}/Knowledge" "${PROJECT_ROOT}/Flink")

# 前瞻性关键词列表
PROSPECTIVE_PATTERNS=(
    # AI Agent 相关
    'ai\.agent'
    'ai-agent'
    'agent\.enabled'
    'agent\.config'
    'CREATE AGENT'
    'DROP AGENT'
    'ALTER AGENT'
    'AGENT CONFIG'
    
    # Serverless 相关（虚构配置）
    'serverless\.enabled'
    'serverless\.mode'
    'serverless\.config'
    'serverless\.provider'
    
    # 未来版本API（虚构）
    'FLIP-[0-9]{4,}'           # 高编号FLIP（如FLIP-9999，超过已知范围）
    'v9\.'                      # 超远未来版本
    'v10\.'
    '2\.[5-9][0-9]\.'          # 假设当前为2.x版本，检测远超当前版本的API
    
    # 实验性功能标记（需要标注）
    '@Experimental'
    '@Preview'
    'EXPERIMENTAL'
    'PREVIEW FEATURE'
    'COMING SOON'
    'WILL BE RELEASED'
    'FUTURE VERSION'
    
    # 虚构配置项
    'auto\.ai'
    'smart\.tuning'
    'predictive\.scaling'
    'neural\.checkpoint'
    'quantum\.stream'
)

# 前瞻性好词 - 如果前面有这些标记则跳过
EXEMPTION_MARKERS=(
    '\[前瞻性内容\]'
    '\[PROSPECTIVE\]'
    '\[未来规划\]'
    '\[DRAFT\]'
    '\[草案\]'
    '\[概念验证\]'
    '\[Proof of Concept\]'
    '\[RFC\]'
    '\[WIP\]'
    '\[Work in Progress\]'
    '<!-- PROSPECTIVE -->'
    '<!-- prospective -->'
)

# 统计
TOTAL_FILES=0
VIOLATION_COUNT=0
VIOLATIONS=()

# 输出函数
print_header() {
    echo "========================================"
    echo "  前瞻性内容检查"
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

# 检查文件是否被豁免
is_exempted() {
    local file="$1"
    local first_lines
    first_lines=$(head -20 "$file" 2>/dev/null || true)
    
    for marker in "${EXEMPTION_MARKERS[@]}"; do
        if echo "$first_lines" | grep -qE "$marker"; then
            return 0
        fi
    done
    return 1
}

# 检查单个文件
check_file() {
    local file="$1"
    local relative_path
    relative_path=$(realpath --relative-to="$PROJECT_ROOT" "$file" 2>/dev/null || echo "$file")
    
    ((TOTAL_FILES++))
    
    # 检查是否被豁免
    if is_exempted "$file"; then
        print_info "跳过 (已标注): $relative_path"
        return 0
    fi
    
    local file_has_violation=0
    local line_num=0
    
    while IFS= read -r line || [[ -n "$line" ]]; do
        ((line_num++))
        
        for pattern in "${PROSPECTIVE_PATTERNS[@]}"; do
            if echo "$line" | grep -qiE "$pattern"; then
                # 检查是否已有前瞻性标注
                local context_before=$((line_num > 5 ? line_num - 5 : 1))
                local context
                context=$(sed -n "${context_before},${line_num}p" "$file" 2>/dev/null || true)
                
                local is_marked=0
                for marker in "${EXEMPTION_MARKERS[@]}"; do
                    if echo "$context" | grep -qE "$marker"; then
                        is_marked=1
                        break
                    fi
                done
                
                if [[ $is_marked -eq 0 ]]; then
                    VIOLATIONS+=("$relative_path:$line_num: $line")
                    ((VIOLATION_COUNT++))
                    file_has_violation=1
                    
                    if [[ $file_has_violation -eq 1 ]]; then
                        print_fail "$relative_path"
                    fi
                    echo "  Line $line_num: 匹配模式 '$pattern'"
                    echo "    → $(echo "$line" | tr -s ' ' | head -c 100)"
                fi
            fi
        done
    done < "$file"
    
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
    echo "发现问题数: $VIOLATION_COUNT"
    echo ""
    
    if [[ $VIOLATION_COUNT -eq 0 ]]; then
        print_pass "未检测到未标注的前瞻性内容"
        echo ""
        return 0
    else
        print_fail "发现 $VIOLATION_COUNT 处未标注的前瞻性内容"
        echo ""
        echo "检测到的关键词模式:"
        for pattern in "${PROSPECTIVE_PATTERNS[@]}"; do
            echo "  - $pattern"
        done
        echo ""
        echo "如需豁免，请在文件前20行添加以下任一标记:"
        for marker in "${EXEMPTION_MARKERS[@]}"; do
            echo "  $marker"
        done
        echo ""
        return 1
    fi
}

# 执行主函数
main "$@"
exit $?
