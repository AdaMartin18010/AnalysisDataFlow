#!/bin/bash
# Coq证明助手环境配置脚本
# 支持: Ubuntu/Debian, macOS, WSL
# 版本: 1.0

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查系统类型
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            echo "ubuntu"
        elif command -v yum &> /dev/null; then
            echo "centos"
        elif command -v pacman &> /dev/null; then
            echo "arch"
        else
            echo "linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# 检查依赖
check_dependencies() {
    log_info "检查系统依赖..."
    
    local deps=("curl" "wget" "gcc" "make")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done
    
    if [ ${#missing[@]} -ne 0 ]; then
        log_warn "缺少依赖: ${missing[*]}"
        return 1
    fi
    
    log_info "所有依赖已满足"
    return 0
}

# 安装系统依赖
install_system_deps() {
    local os=$1
    
    case $os in
        ubuntu)
            log_info "安装Ubuntu依赖..."
            sudo apt-get update
            sudo apt-get install -y \
                opam \
                ocaml \
                ocaml-native-compilers \
                libocaml-expat-dev \
                libgtk2.0-dev \
                libgtksourceview2.0-dev \
                liblablgtk2-ocaml-dev
            ;;
        macos)
            log_info "安装macOS依赖..."
            if ! command -v brew &> /dev/null; then
                log_error "请先安装Homebrew: https://brew.sh/"
                exit 1
            fi
            brew install opam ocaml pkg-config gtk+
            ;;
        *)
            log_error "不支持的操作系统: $os"
            exit 1
            ;;
    esac
}

# 配置opam和OCaml
setup_opam() {
    log_info "配置opam..."
    
    # 初始化opam (如果不存在)
    if [ ! -d "$HOME/.opam" ]; then
        opam init --disable-sandboxing --auto-setup -y
    fi
    
    # 加载opam环境
    eval $(opam env)
    
    # 创建项目专用switch
    local switch_name="stream-verify"
    local ocaml_version="4.14.1"
    
    if ! opam switch list | grep -q "$switch_name"; then
        log_info "创建opam switch: $switch_name (OCaml $ocaml_version)"
        opam switch create "$switch_name" "$ocaml_version"
    else
        log_info "使用已存在的switch: $switch_name"
    fi
    
    opam switch "$switch_name"
    eval $(opam env)
    
    # 更新opam仓库
    opam update
}

# 安装Coq及其生态系统
install_coq() {
    log_info "安装Coq生态系统..."
    
    local coq_version="8.18.0"
    local iris_version="4.0.0"
    
    # 核心组件
    log_info "安装Coq $coq_version..."
    opam install -y coq.$coq_version
    
    # MathComp (数学组件)
    log_info "安装MathComp..."
    opam install -y \
        coq-mathcomp-ssreflect \
        coq-mathcomp-algebra \
        coq-mathcomp-fingroup \
        coq-mathcomp-solvable \
        coq-mathcomp-field
    
    # Iris分离逻辑
    log_info "安装Iris $iris_version..."
    opam install -y coq-iris.$iris_version coq-iris-heap-lang
    
    # 其他有用库
    log_info "安装辅助库..."
    opam install -y \
        coq-ext-lib \
        coq-equations \
        coq-record-update
    
    # 自动化工具
    log_info "安装自动化工具..."
    opam install -y coq-hammer
}

# 安装VSCode扩展
install_vscode_extensions() {
    if command -v code &> /dev/null; then
        log_info "安装VSCode Coq扩展..."
        code --install-extension maximedenes.vscoq || true
        code --install-extension vestiii.vscoq-syntax || true
    else
        log_warn "未检测到VSCode，跳过扩展安装"
    fi
}

# 创建项目结构
create_project_structure() {
    log_info "创建项目结构..."
    
    local project_root="${1:-.}"
    
    mkdir -p "$project_root"/{theories,proofs,scripts,extracted}
    
    # 创建_CoqProject
    cat > "$project_root/_CoqProject" << 'EOF'
-R theories/ StreamVerify
-R proofs/ StreamProofs

-arg -w -arg -notation-overridden
-arg -w -arg -redundant-canonical-projection
-arg -w -arg -ambiguous-paths

theories/utils.v
theories/stream.v
theories/watermark.v
theories/checkpoint.v
theories/state.v
proofs/exactly_once.v
proofs/watermark_monotonic.v
proofs/checkpoint_correct.v
EOF

    # 创建Makefile
    cat > "$project_root/Makefile" << 'EOF'
COQMAKEFILE=$(shell which coq_makefile)
COQDOCFLAGS="--toc --html --interpolate"

all: Makefile.coq
	$(MAKE) -f Makefile.coq all

Makefile.coq: _CoqProject
	$(COQMAKEFILE) -f _CoqProject -o Makefile.coq

clean: Makefile.coq
	$(MAKE) -f Makefile.coq clean
	rm -f Makefile.coq

doc: all
	$(MAKE) -f Makefile.coq html

.PHONY: all clean doc
EOF

    # 创建.gitignore
    cat > "$project_root/.gitignore" << 'EOF'
*.vo
*.vok
*.vos
*.glob
*.aux
Makefile.coq
Makefile.coq.conf
.coqdeps.d
.coq-native
.lia.cache
.nia.cache
*.cmi
*.cmo
*.cmx
*.o
html/
EOF

    log_info "项目结构已创建于: $project_root"
}

# 验证安装
verify_installation() {
    log_info "验证安装..."
    
    eval $(opam env)
    
    # 检查Coq
    if command -v coqc &> /dev/null; then
        log_info "Coq版本: $(coqc --version | head -1)"
    else
        log_error "Coq安装失败"
        return 1
    fi
    
    # 检查CoqIDE
    if command -v coqide &> /dev/null; then
        log_info "CoqIDE可用"
    else
        log_warn "CoqIDE未安装"
    fi
    
    # 测试编译
    log_info "运行简单测试..."
    cat > /tmp/test_coq.v << 'EOF'
Require Import Arith.
Theorem test: forall n m, n + m = m + n.
Proof. intros. apply Nat.add_comm. Qed.
EOF
    
    if coqc /tmp/test_coq.v -o /tmp/test_coq.vo 2>/dev/null; then
        log_info "测试编译成功"
        rm -f /tmp/test_coq.v /tmp/test_coq.vo
    else
        log_error "测试编译失败"
        return 1
    fi
    
    return 0
}

# 创建环境激活脚本
create_env_script() {
    local project_root="${1:-.}"
    
    cat > "$project_root/activate-coq-env.sh" << 'EOF'
#!/bin/bash
# Coq环境激活脚本

eval $(opam env --switch=stream-verify --set-switch)
echo "Coq环境已激活"
echo "Coq版本: $(coqc --version 2>/dev/null | head -1)"
EOF
    chmod +x "$project_root/activate-coq-env.sh"
}

# 主函数
main() {
    log_info "开始配置Coq证明助手环境..."
    
    local project_root="${1:-./coq-project}"
    local os=$(detect_os)
    
    log_info "检测到操作系统: $os"
    
    # 检查依赖
    if ! check_dependencies; then
        log_info "尝试安装系统依赖..."
        install_system_deps "$os"
    fi
    
    # 配置opam
    setup_opam
    
    # 安装Coq
    install_coq
    
    # 安装VSCode扩展
    install_vscode_extensions
    
    # 创建项目结构
    create_project_structure "$project_root"
    
    # 验证安装
    if verify_installation; then
        log_info "✅ Coq环境配置成功!"
        log_info "项目位置: $project_root"
        log_info "激活环境: source $project_root/activate-coq-env.sh"
        log_info "开始证明: cd $project_root && make"
    else
        log_error "❌ 配置过程中出现问题，请检查错误信息"
        exit 1
    fi
    
    # 创建环境激活脚本
    create_env_script "$project_root"
}

# 帮助信息
show_help() {
    cat << 'EOF'
Coq证明助手环境配置脚本

用法: ./setup-coq-env.sh [项目目录]

选项:
  -h, --help     显示此帮助信息
  -v, --version  显示版本信息

示例:
  ./setup-coq-env.sh                    # 使用默认目录 ./coq-project
  ./setup-coq-env.sh ./my-proof-project # 指定项目目录

环境要求:
  - Ubuntu 20.04+ / macOS 11+
  - 网络连接
  - sudo权限 (安装系统包)

输出:
  - Coq 8.18.0
  - MathComp生态系统
  - Iris 4.0.0分离逻辑框架
  - 项目模板结构
EOF
}

# 参数解析
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    -v|--version)
        echo "setup-coq-env.sh version 1.0"
        exit 0
        ;;
esac

# 执行主函数
main "$@"
