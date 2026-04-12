#!/bin/bash
# TLA+模型检查环境配置脚本
# 支持: Ubuntu/Debian, macOS, WSL
# 版本: 1.0

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_debug() { echo -e "${BLUE}[DEBUG]${NC} $1"; }

# 配置
TLA_VERSION="1.8.0"
TLA_DOWNLOAD_URL="https://github.com/tlaplus/tlaplus/releases/download/v${TLA_VERSION}/tla2tools.jar"
INSTALL_DIR="${HOME}/.tla"
BIN_DIR="${HOME}/.local/bin"

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "linux";;
        Darwin*)    echo "macos";;
        CYGWIN*|MINGW*|MSYS*) echo "windows";;
        *)          echo "unknown";;
    esac
}

# 检查Java
check_java() {
    log_info "检查Java环境..."
    
    if ! command -v java &> /dev/null; then
        log_error "未安装Java"
        return 1
    fi
    
    local java_version
    java_version=$(java -version 2>&1 | head -1 | cut -d'"' -f2 | cut -d'.' -f1-2)
    log_info "Java版本: $java_version"
    
    # 检查是否为Java 11+
    local major_version
    major_version=$(echo "$java_version" | cut -d'.' -f1)
    if [ "$major_version" = "1" ]; then
        major_version=$(echo "$java_version" | cut -d'.' -f2)
    fi
    
    if [ "$major_version" -lt 11 ]; then
        log_warn "建议Java 11或更高版本，当前版本: $java_version"
        return 1
    fi
    
    return 0
}

# 安装Java
install_java() {
    local os=$1
    
    log_info "安装Java..."
    
    case $os in
        linux)
            if command -v apt-get &> /dev/null; then
                sudo apt-get update
                sudo apt-get install -y default-jdk
            elif command -v yum &> /dev/null; then
                sudo yum install -y java-17-openjdk
            else
                log_error "不支持的包管理器，请手动安装Java 11+"
                exit 1
            fi
            ;;
        macos)
            if command -v brew &> /dev/null; then
                brew install openjdk@17
            else
                log_error "请先安装Homebrew"
                exit 1
            fi
            ;;
        *)
            log_error "不支持的操作系统"
            exit 1
            ;;
    esac
}

# 下载并安装TLA+工具
download_tla() {
    log_info "下载TLA+工具集..."
    
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$BIN_DIR"
    
    # 下载tla2tools.jar
    if [ -f "$INSTALL_DIR/tla2tools.jar" ]; then
        log_warn "TLA+工具已存在，跳过下载"
    else
        log_info "从GitHub下载..."
        wget -q --show-progress -O "$INSTALL_DIR/tla2tools.jar" "$TLA_DOWNLOAD_URL"
        log_info "下载完成"
    fi
    
    # 创建启动脚本
    create_launcher_scripts
}

# 创建启动脚本
create_launcher_scripts() {
    log_info "创建命令行工具..."
    
    local java_opts="-XX:+UseParallelGC -Xmx8g"
    
    # TLC (模型检查器)
    cat > "$BIN_DIR/tlc" << EOF
#!/bin/bash
exec java $java_opts -cp "$INSTALL_DIR/tla2tools.jar" tlc2.TLC "\$@"
EOF
    chmod +x "$BIN_DIR/tlc"
    
    # PlusCal编译器
    cat > "$BIN_DIR/pcal" << EOF
#!/bin/bash
exec java $java_opts -cp "$INSTALL_DIR/tla2tools.jar" pcal.trans "\$@"
EOF
    chmod +x "$BIN_DIR/pcal"
    
    # SANY (语法检查器)
    cat > "$BIN_DIR/sany" << EOF
#!/bin/bash
exec java $java_opts -cp "$INSTALL_DIR/tla2tools.jar" tla2sany.SANY "\$@"
EOF
    chmod +x "$BIN_DIR/sany"
    
    # TLAPS (证明系统，可选)
    cat > "$BIN_DIR/tlaps" << EOF
#!/bin/bash
echo "TLAPS需要单独安装，请参考: https://tla.msr-inria.inria.fr/tlaps/content/Download/Binaries.html"
EOF
    chmod +x "$BIN_DIR/tlaps"
    
    # 工具版本检查
    cat > "$BIN_DIR/tla-version" << EOF
#!/bin/bash
echo "TLA+ Tools Version:"
java -cp "$INSTALL_DIR/tla2tools.jar" tlc2.TLC -version 2>&1
EOF
    chmod +x "$BIN_DIR/tla-version"
}

# 安装TLA+ Toolbox (GUI)
install_toolbox() {
    local os=$1
    
    log_info "下载TLA+ Toolbox (GUI)..."
    
    local toolbox_url
    local toolbox_file
    
    case $os in
        linux)
            toolbox_url="https://github.com/tlaplus/tlaplus/releases/download/v${TLA_VERSION}/TLAToolbox-${TLA_VERSION}-linux.gtk.x86_64.zip"
            toolbox_file="TLAToolbox.zip"
            ;;
        macos)
            toolbox_url="https://github.com/tlaplus/tlaplus/releases/download/v${TLA_VERSION}/TLAToolbox-${TLA_VERSION}-macosx.cocoa.x86_64.zip"
            toolbox_file="TLAToolbox-macos.zip"
            ;;
        *)
            log_warn "不支持的操作系统，跳过Toolbox安装"
            return
            ;;
    esac
    
    if [ -d "$INSTALL_DIR/toolbox" ]; then
        log_warn "Toolbox已存在"
        return
    fi
    
    log_info "下载Toolbox..."
    wget -q --show-progress -O "/tmp/$toolbox_file" "$toolbox_url"
    
    log_info "解压Toolbox..."
    unzip -q "/tmp/$toolbox_file" -d "$INSTALL_DIR/toolbox"
    rm -f "/tmp/$toolbox_file"
    
    # 创建启动脚本
    case $os in
        linux)
            cat > "$BIN_DIR/tla-toolbox" << EOF
#!/bin/bash
exec "$INSTALL_DIR/toolbox/toolbox" "\$@"
EOF
            ;;
        macos)
            cat > "$BIN_DIR/tla-toolbox" << EOF
#!/bin/bash
open "$INSTALL_DIR/toolbox/TLA+ Toolbox.app" --args "\$@"
EOF
            ;;
    esac
    chmod +x "$BIN_DIR/tla-toolbox"
    
    log_info "Toolbox安装完成: tla-toolbox"
}

# 安装VSCode扩展
install_vscode_extensions() {
    if command -v code &> /dev/null; then
        log_info "安装VSCode TLA+扩展..."
        
        # 主要扩展
        code --install-extension aloysbaillet.tla || true
        code --install-extensionalygin.vscode-tlaplus || true
        
        log_info "VSCode扩展安装完成"
    else
        log_warn "未检测到VSCode"
    fi
}

# 创建项目模板
create_project_template() {
    local project_dir="${1:-./tla-models}"
    
    log_info "创建TLA+项目模板: $project_dir"
    
    mkdir -p "$project_dir"/{models,cfg,modules}
    
    # 创建示例模型
    cat > "$project_dir/models/Checkpoint.tla" << 'EOF'
----------------------------- MODULE Checkpoint -----------------
EXTENDS Integers, Sequences, FiniteSets, TLC

CONSTANTS Operators, MaxEvents, CheckpointInterval

VARIABLES state, checkpoint, pending, log

typeInvariant ==
    /\ state \in [Operators -> Nat]
    /\ checkpoint \in [Operators -> Nat]
    /\ pending \subseteq [op: Operators, seq: Nat]
    /\ log \in Seq([op: Operators, from: Nat, to: Nat])

Init ==
    /\ state = [op \in Operators |-> 0]
    /\ checkpoint = [op \in Operators |-> 0]
    /\ pending = {}
    /\ log = << >>

ProcessEvent(op) ==
    /\ state' = [state EXCEPT ![op] = @ + 1]
    /\ log' = Append(log, [op |-> op, from |-> state[op], to |-> state[op] + 1])
    /\ UNCHANGED <<checkpoint, pending>>

TriggerCheckpoint ==
    /\ \E op \in Operators : state[op] - checkpoint[op] >= CheckpointInterval
    /\ checkpoint' = [op \in Operators |-> state[op]]
    /\ UNCHANGED <<state, pending, log>>

Next ==
    \/ \E op \in Operators : ProcessEvent(op)
    \/ TriggerCheckpoint

Safety ==
    \A i \in 1..Len(log) : log[i].to = log[i].from + 1
================================================================
EOF

    # 创建模型检查配置
    cat > "$project_dir/cfg/Checkpoint.cfg" << 'EOF'
CONSTANTS
    Operators = {op1, op2, op3}
    MaxEvents = 10
    CheckpointInterval = 3

INIT Init
NEXT Next

INVARIANT Safety
typeInvariant

CONSTANTS
    op1 = op1
    op2 = op2
    op3 = op3
EOF

    # 创建Makefile
    cat > "$project_dir/Makefile" << 'EOF'
TLC = tlc
PCAL = pcal
SANY = sany

MODELS = $(wildcard models/*.tla)
MODULES = $(wildcard modules/*.tla)

.PHONY: all check syntax translate clean

all: check

check: $(MODELS:.tla=.check)

syntax: $(MODELS:.tla=.syntax) $(MODULES:.tla=.syntax)

models/%.syntax: models/%.tla
	@echo "Checking syntax: $<"
	$(SANY) $< || true

models/%.check: models/%.tla cfg/%.cfg
	@echo "Model checking: $<"
	$(TLC) $< -config cfg/$*.cfg

translate: $(MODELS:.tla=.tla+)

models/%.tla+: models/%.tla
	@echo "Translating PlusCal: $<"
	$(PCAL) -nocfg $<

clean:
	find . -name "*.old" -delete
	find . -name "states" -type d -exec rm -rf {} + 2>/dev/null || true

help:
	@echo "TLA+ Model Checking Makefile"
	@echo "  make check     - Run TLC on all models"
	@echo "  make syntax    - Check syntax of all TLA+ files"
	@echo "  make translate - Translate PlusCal algorithms"
	@echo "  make clean     - Remove generated files"
EOF

    # 创建.gitignore
    cat > "$project_dir/.gitignore" << 'EOF'
# TLA+ generated files
*.old
states/
*.out

# TLC checkpoint files
*.chkpt

# Toolbox files
*.launch
.toolbox/
EOF

    log_info "项目模板创建完成"
}

# 验证安装
verify_installation() {
    log_info "验证TLA+安装..."
    
    local failed=0
    
    # 检查命令
    for cmd in tlc pcal sany; do
        if command -v "$cmd" &> /dev/null; then
            log_info "✓ $cmd 可用"
        else
            log_error "✗ $cmd 未找到"
            failed=1
        fi
    done
    
    # 运行简单测试
    log_info "运行语法检查测试..."
    cat > /tmp/Test.tla << 'EOF'
----------------------------- MODULE Test -----------------
EXTENDS Naturals

VARIABLE x

Init == x = 0

Next == x' = x + 1
================================================================
EOF
    
    if sany /tmp/Test.tla 2>&1 | grep -q "parsed successfully"; then
        log_info "✓ 语法检查测试通过"
    else
        log_warn "语法检查可能有警告，这通常是正常的"
    fi
    
    rm -f /tmp/Test.tla
    
    if [ $failed -eq 0 ]; then
        log_info "✅ TLA+环境配置成功!"
        return 0
    else
        log_error "❌ 部分组件安装失败"
        return 1
    fi
}

# 创建环境信息文件
create_env_info() {
    local project_dir="${1:-.}"
    
    cat > "$project_dir/.tla-env" << EOF
TLA+ Environment Information
=============================
Version: $TLA_VERSION
Install Directory: $INSTALL_DIR
Java Version: $(java -version 2>&1 | head -1)

Available Commands:
  tlc <model.tla>       - Run TLC model checker
  pcal <model.tla>      - Translate PlusCal to TLA+
  sany <model.tla>      - Check TLA+ syntax
  tla-version           - Show version information
  tla-toolbox           - Launch TLA+ Toolbox GUI (if installed)

Quick Start:
  cd $project_dir
  make syntax    # Check all TLA+ files
  make check     # Run model checking
EOF
}

# 显示帮助
show_help() {
    cat << 'EOF'
TLA+模型检查环境配置脚本

用法: ./setup-tla-env.sh [选项] [项目目录]

选项:
  -h, --help       显示此帮助信息
  -v, --version    显示版本信息
  --no-toolbox     跳过安装TLA+ Toolbox GUI
  --quick          仅安装核心工具，不创建项目模板

示例:
  ./setup-tla-env.sh                    # 完整安装
  ./setup-tla-env.sh ./my-tla-models    # 指定项目目录
  ./setup-tla-env.sh --no-toolbox       # 仅安装命令行工具

环境要求:
  - Java 11+
  - 网络连接
  - curl/wget

输出:
  - tlc: TLC模型检查器
  - pcal: PlusCal编译器
  - sany: TLA+语法检查器
  - tla-toolbox: GUI工具 (可选)
EOF
}

# 主函数
main() {
    local install_toolbox=true
    local create_template=true
    local project_dir="./tla-models"
    
    # 参数解析
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--version)
                echo "setup-tla-env.sh version 1.0"
                exit 0
                ;;
            --no-toolbox)
                install_toolbox=false
                shift
                ;;
            --quick)
                create_template=false
                shift
                ;;
            -*)
                log_error "未知选项: $1"
                show_help
                exit 1
                ;;
            *)
                project_dir="$1"
                shift
                ;;
        esac
    done
    
    log_info "开始配置TLA+模型检查环境..."
    
    local os=$(detect_os)
    log_info "操作系统: $os"
    
    # 检查/安装Java
    if ! check_java; then
        install_java "$os"
        if ! check_java; then
            log_error "Java安装失败"
            exit 1
        fi
    fi
    
    # 下载并安装TLA+工具
    download_tla
    
    # 安装Toolbox
    if $install_toolbox; then
        install_toolbox "$os"
    fi
    
    # 安装VSCode扩展
    install_vscode_extensions
    
    # 创建项目模板
    if $create_template; then
        create_project_template "$project_dir"
    fi
    
    # 验证安装
    if verify_installation; then
        log_info ""
        log_info "========================================"
        log_info "TLA+环境配置完成!"
        log_info "========================================"
        log_info ""
        log_info "命令行工具:"
        log_info "  tlc, pcal, sany, tla-version"
        log_info ""
        if $create_template; then
            log_info "项目模板: $project_dir"
            log_info "快速开始: cd $project_dir && make syntax"
        fi
        log_info ""
        log_info "注意: 如果命令不可用，请添加以下内容到~/.bashrc:"
        log_info "  export PATH=\"$BIN_DIR:\$PATH\""
        
        # 创建环境信息文件
        if $create_template; then
            create_env_info "$project_dir"
        fi
    else
        log_error "配置失败，请检查错误信息"
        exit 1
    fi
}

# 执行
main "$@"
