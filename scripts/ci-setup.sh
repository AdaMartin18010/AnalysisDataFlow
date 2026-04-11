#!/bin/bash
#
# CI 环境设置脚本
#
# 功能: 设置 CI 验证所需的开发环境
#
# 用法:
#   ./scripts/ci-setup.sh [选项]
#
# 选项:
#   --minimal    最小安装（仅必要依赖）
#   --full       完整安装（所有工具）
#   --check      仅检查环境状态
#   --help       显示帮助信息

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Python 版本要求
PYTHON_VERSION_MIN="3.9"
NODE_VERSION_MIN="18"

# 安装模式
SETUP_MODE="full"
CHECK_ONLY=false

# ==================== 函数定义 ====================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
}

show_help() {
    cat << EOF
CI 环境设置脚本

功能: 设置 CI 验证所需的开发环境

用法:
  ./scripts/ci-setup.sh [选项]

选项:
  --minimal    最小安装（仅必要依赖）
  --full       完整安装（所有工具，默认）
  --check      仅检查环境状态，不安装
  --help, -h   显示帮助信息

示例:
  ./scripts/ci-setup.sh           # 完整安装
  ./scripts/ci-setup.sh --minimal # 最小安装
  ./scripts/ci-setup.sh --check   # 检查环境

EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --minimal)
                SETUP_MODE="minimal"
                shift
                ;;
            --full)
                SETUP_MODE="full"
                shift
                ;;
            --check)
                CHECK_ONLY=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                log_error "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# ==================== 检查函数 ====================

check_python() {
    log_step "检查 Python 环境..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 未安装"
        return 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    log_info "Python 版本: ${PYTHON_VERSION}"
    
    # 版本比较
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
        log_success "Python 版本符合要求 (>= ${PYTHON_VERSION_MIN})"
        return 0
    else
        log_error "Python 版本过低，需要 >= ${PYTHON_VERSION_MIN}"
        return 1
    fi
}

check_node() {
    log_step "检查 Node.js 环境..."
    
    if ! command -v node &> /dev/null; then
        log_error "Node.js 未安装"
        return 1
    fi
    
    NODE_VERSION=$(node --version | sed 's/v//')
    log_info "Node.js 版本: ${NODE_VERSION}"
    
    # 简单版本检查
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d. -f1)
    if [ "$NODE_MAJOR" -ge 18 ]; then
        log_success "Node.js 版本符合要求 (>= ${NODE_VERSION_MIN})"
        return 0
    else
        log_warning "Node.js 版本较低，建议 >= ${NODE_VERSION_MIN}"
        return 1
    fi
}

check_git() {
    log_step "检查 Git..."
    
    if ! command -v git &> /dev/null; then
        log_error "Git 未安装"
        return 1
    fi
    
    GIT_VERSION=$(git --version | awk '{print $3}')
    log_info "Git 版本: ${GIT_VERSION}"
    log_success "Git 已安装"
    return 0
}

check_python_packages() {
    log_step "检查 Python 包..."
    
    local packages=("networkx" "pyyaml" "requests" "aiohttp")
    local missing=()
    
    for pkg in "${packages[@]}"; do
        if ! python3 -c "import ${pkg}" 2>/dev/null; then
            missing+=("$pkg")
        fi
    done
    
    if [ ${#missing[@]} -eq 0 ]; then
        log_success "所有 Python 包已安装"
        return 0
    else
        log_warning "缺少 Python 包: ${missing[*]}"
        return 1
    fi
}

check_node_packages() {
    log_step "检查 Node.js 包..."
    
    # 检查全局安装的 markdownlint
    if command -v markdownlint &> /dev/null; then
        log_success "markdownlint 已全局安装"
        return 0
    elif npm list -g markdownlint-cli &> /dev/null 2>&1; then
        log_success "markdownlint-cli 已安装"
        return 0
    else
        log_warning "markdownlint-cli 未安装"
        return 1
    fi
}

check_project_structure() {
    log_step "检查项目结构..."
    
    local required_dirs=("Struct" "Knowledge" "Flink")
    local missing=()
    
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "${PROJECT_ROOT}/${dir}" ]; then
            missing+=("$dir")
        fi
    done
    
    if [ ${#missing[@]} -eq 0 ]; then
        log_success "项目结构完整"
        return 0
    else
        log_error "缺少目录: ${missing[*]}"
        return 1
    fi
}

# ==================== 安装函数 ====================

install_python_packages() {
    log_step "安装 Python 依赖..."
    
    local packages="networkx pyyaml requests aiohttp"
    
    if [ "$SETUP_MODE" == "full" ]; then
        packages="${packages} matplotlib numpy"
    fi
    
    log_info "安装包: ${packages}"
    pip install -q ${packages}
    
    log_success "Python 包安装完成"
}

install_node_packages() {
    log_step "安装 Node.js 依赖..."
    
    if [ "$SETUP_MODE" == "minimal" ]; then
        log_info "最小模式：跳过 Node.js 包安装"
        return 0
    fi
    
    log_info "安装 markdownlint-cli..."
    npm install -g markdownlint-cli@0.41.0
    
    log_success "Node.js 包安装完成"
}

setup_git_hooks() {
    log_step "设置 Git Hooks..."
    
    if [ ! -d "${PROJECT_ROOT}/.git" ]; then
        log_warning "不是 Git 仓库，跳过 hooks 设置"
        return 0
    fi
    
    # 创建 pre-commit hook
    cat > "${PROJECT_ROOT}/.git/hooks/pre-commit" << 'EOF'
#!/bin/bash
# Pre-commit hook for AnalysisDataFlow

echo "Running pre-commit checks..."

# 检查变更的 Markdown 文件
CHANGED_MD_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$' || true)

if [ -z "$CHANGED_MD_FILES" ]; then
    echo "No Markdown files changed, skipping checks"
    exit 0
fi

echo "Changed Markdown files:"
echo "$CHANGED_MD_FILES"

# 运行快速检查
if [ -f "scripts/ci-validate.sh" ]; then
    ./scripts/ci-validate.sh --quick
    exit $?
fi

echo "Pre-commit checks completed"
EOF
    
    chmod +x "${PROJECT_ROOT}/.git/hooks/pre-commit"
    log_success "Git pre-commit hook 已设置"
}

create_directories() {
    log_step "创建必要目录..."
    
    mkdir -p "${PROJECT_ROOT}/reports"
    mkdir -p "${PROJECT_ROOT}/.cache"
    
    log_success "目录创建完成"
}

# ==================== 主流程 ====================

print_header() {
    echo ""
    echo "========================================"
    echo "  AnalysisDataFlow CI 环境设置"
    echo "========================================"
    echo ""
    log_info "项目根目录: ${PROJECT_ROOT}"
    log_info "安装模式: ${SETUP_MODE}"
    echo ""
}

print_summary() {
    echo ""
    echo "========================================"
    echo "  环境状态汇总"
    echo "========================================"
    echo ""
    
    local all_checks_passed=true
    
    # 重新检查各项
    if check_python &> /dev/null; then
        log_success "Python 3"
    else
        log_error "Python 3"
        all_checks_passed=false
    fi
    
    if check_node &> /dev/null; then
        log_success "Node.js"
    else
        log_warning "Node.js"
    fi
    
    if check_git &> /dev/null; then
        log_success "Git"
    else
        log_error "Git"
        all_checks_passed=false
    fi
    
    if check_python_packages &> /dev/null; then
        log_success "Python 包"
    else
        log_warning "Python 包"
    fi
    
    if check_node_packages &> /dev/null; then
        log_success "Node.js 包"
    else
        log_warning "Node.js 包"
    fi
    
    echo ""
    
    if $all_checks_passed; then
        log_success "核心环境就绪!"
        return 0
    else
        log_error "核心环境有缺失，请安装必要依赖"
        return 1
    fi
}

main() {
    parse_args "$@"
    
    print_header
    
    # 检查模式
    if [ "$CHECK_ONLY" = true ]; then
        print_summary
        exit $?
    fi
    
    # 环境检查
    log_info "开始环境检查..."
    echo ""
    
    local python_ok=false
    local node_ok=false
    local git_ok=false
    
    if check_python; then
        python_ok=true
    else
        log_error "Python 环境检查失败，请安装 Python >= ${PYTHON_VERSION_MIN}"
        exit 1
    fi
    
    check_node || true
    check_git || exit 1
    check_project_structure || exit 1
    
    echo ""
    log_info "开始安装..."
    echo ""
    
    # 安装依赖
    if $python_ok; then
        install_python_packages
    fi
    
    if command -v npm &> /dev/null; then
        install_node_packages
    fi
    
    # 设置
    create_directories
    setup_git_hooks
    
    echo ""
    log_success "CI 环境设置完成!"
    echo ""
    
    # 最终汇总
    print_summary
}

# 运行主程序
main "$@"
