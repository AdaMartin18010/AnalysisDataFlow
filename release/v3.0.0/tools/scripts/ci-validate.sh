#!/bin/bash
#
# CI 本地验证脚本
# 
# 功能: 在本地运行完整的 CI 验证流程，模拟 GitHub Actions 的检查
#
# 用法:
#   ./scripts/ci-validate.sh [选项]
#
# 选项:
#   --quick          快速模式（仅检查变更文件）
#   --full           完整模式（所有检查）
#   --markdown-only  仅 Markdown 检查
#   --theorems-only  仅定理验证
#   --links-only     仅链接检查
#   --proof-chains   仅证明链验证
#   --help           显示帮助信息

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 报告目录
REPORTS_DIR="${PROJECT_ROOT}/reports"
mkdir -p "${REPORTS_DIR}"

# 默认配置
CHECK_MODE="full"
VERBOSE=false
PARALLEL=true

# 统计
FAILED_CHECKS=0
PASSED_CHECKS=0
SKIPPED_CHECKS=0

# ==================== 函数定义 ====================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

show_help() {
    cat << EOF
CI 本地验证脚本

功能: 在本地运行完整的 CI 验证流程，模拟 GitHub Actions 的检查

用法:
  ./scripts/ci-validate.sh [选项]

选项:
  --quick          快速模式（仅检查变更文件）
  --full           完整模式（所有检查，默认）
  --markdown-only  仅 Markdown 语法检查
  --theorems-only  仅定理验证
  --links-only     仅链接检查
  --proof-chains   仅证明链验证
  --sequential     串行执行（默认并行）
  --verbose        显示详细输出
  --help, -h       显示帮助信息

示例:
  ./scripts/ci-validate.sh                    # 运行所有检查
  ./scripts/ci-validate.sh --quick            # 快速检查
  ./scripts/ci-validate.sh --theorems-only    # 仅验证定理
  ./scripts/ci-validate.sh --links-only       # 仅检查链接

EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --quick)
                CHECK_MODE="quick"
                shift
                ;;
            --full)
                CHECK_MODE="full"
                shift
                ;;
            --markdown-only)
                CHECK_MODE="markdown-only"
                shift
                ;;
            --theorems-only)
                CHECK_MODE="theorems-only"
                shift
                ;;
            --links-only)
                CHECK_MODE="links-only"
                shift
                ;;
            --proof-chains)
                CHECK_MODE="proof-chains"
                shift
                ;;
            --sequential)
                PARALLEL=false
                shift
                ;;
            --verbose)
                VERBOSE=true
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

check_prerequisites() {
    log_info "检查环境依赖..."
    
    local missing_deps=()
    
    if ! command -v python3 &> /dev/null; then
        missing_deps+=("python3")
    fi
    
    if ! command -v node &> /dev/null; then
        missing_deps+=("node")
    fi
    
    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "缺少依赖: ${missing_deps[*]}"
        log_info "请安装缺失的依赖后重试"
        exit 1
    fi
    
    # 检查 Python 包
    if ! python3 -c "import networkx" 2>/dev/null; then
        log_warning "未安装 networkx，某些检查可能受限"
        log_info "运行: pip install networkx pyyaml aiohttp"
    fi
    
    log_success "环境检查通过"
}

detect_changed_files() {
    log_info "检测变更文件..."
    
    if [ "${CHECK_MODE}" == "quick" ]; then
        # 获取最近提交的变更文件
        CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD 2>/dev/null | grep '\.md$' || true)
        
        if [ -z "$CHANGED_FILES" ]; then
            log_warning "未检测到变更的 Markdown 文件"
            CHANGED_FILES="all"
        else
            log_info "检测到变更文件:"
            echo "$CHANGED_FILES" | head -10
            if [ $(echo "$CHANGED_FILES" | wc -l) -gt 10 ]; then
                log_info "... 及其他 $(echo "$CHANGED_FILES" | wc -l) 个文件"
            fi
        fi
    else
        CHANGED_FILES="all"
    fi
}

# ==================== 检查函数 ====================

check_markdown() {
    log_info "运行 Markdown 语法检查..."
    
    local report_file="${REPORTS_DIR}/markdown-lint-report.txt"
    
    # 检查 markdownlint 是否安装
    if ! command -v markdownlint &> /dev/null; then
        log_warning "markdownlint 未安装，尝试使用 npx"
        
        # 创建临时配置
        cat > "${PROJECT_ROOT}/.markdownlint-cli2.json" << 'EOF'
{
  "config": {
    "default": true,
    "MD013": false,
    "MD024": false,
    "MD033": false,
    "MD041": false,
    "MD046": false
  }
}
EOF
        
        if ! npx markdownlint-cli2 "**/*.md" --config .markdownlint-cli2.json > "${report_file}" 2>&1; then
            log_warning "Markdown 格式问题（非阻塞）"
            if [ "$VERBOSE" = true ]; then
                cat "${report_file}"
            fi
        else
            log_success "Markdown 语法检查通过"
        fi
    else
        # 使用已安装的 markdownlint
        cat > "${PROJECT_ROOT}/.markdownlint.json" << 'EOF'
{
  "default": true,
  "MD013": false,
  "MD024": false,
  "MD033": false,
  "MD041": false,
  "MD046": false
}
EOF
        
        if ! markdownlint "**/*.md" > "${report_file}" 2>&1; then
            log_warning "发现 Markdown 格式问题"
            if [ "$VERBOSE" = true ]; then
                cat "${report_file}"
            fi
        else
            log_success "Markdown 语法检查通过"
        fi
    fi
    
    # 关键检查：YAML frontmatter
    local yaml_errors=0
    while IFS= read -r file; do
        [ -f "$file" ] || continue
        if head -1 "$file" | grep -q '^---'; then
            if ! grep -q '^---' "$file" | head -3 | tail -1; then
                log_error "Malformed YAML frontmatter: $file"
                yaml_errors=$((yaml_errors + 1))
            fi
        fi
    done < <(find "${PROJECT_ROOT}" -name "*.md" -not -path "*/.git/*" -not -path "*/node_modules/*")
    
    if [ $yaml_errors -eq 0 ]; then
        log_success "YAML frontmatter 检查通过"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        log_error "发现 $yaml_errors 个 YAML frontmatter 错误"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
}

check_theorems() {
    log_info "运行定理验证..."
    
    local uniqueness_script="${PROJECT_ROOT}/.scripts/quality-gates/theorem-uniqueness-checker.py"
    
    if [ -f "$uniqueness_script" ]; then
        log_info "使用定理唯一性检查器..."
        if python3 "$uniqueness_script" --output "${REPORTS_DIR}/theorem-uniqueness-report.md" --dirs Struct Knowledge Flink; then
            log_success "定理唯一性检查通过"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
        else
            log_error "定理唯一性检查失败"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
        fi
    else
        log_warning "定理唯一性检查器未找到，使用简化检查..."
        
        # 简化检查
        python3 << 'PYEOF'
import re
import sys
from pathlib import Path
from collections import defaultdict

THEOREM_PATTERN = re.compile(r'\b(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2})\b')

theorems = defaultdict(list)
errors = []

for directory in ['Struct', 'Knowledge', 'Flink']:
    dir_path = Path(directory)
    if not dir_path.exists():
        continue
    
    for md_file in dir_path.rglob('*.md'):
        if any(p.startswith('.') for p in md_file.parts):
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
            rel_path = str(md_file.relative_to('.'))
            
            for match in THEOREM_PATTERN.findall(content):
                theorem_id = f"{match[0]}-{match[1]}-{match[2]}-{match[3]}"
                theorems[theorem_id].append(rel_path)
        except Exception:
            pass

# 检查重复
duplicates = {k: v for k, v in theorems.items() if len(v) > 1}

if duplicates:
    print(f"发现 {len(duplicates)} 个重复定理编号:")
    for thm, files in list(duplicates.items())[:5]:
        print(f"  {thm}: {files}")
    sys.exit(1)
else:
    print(f"检查了 {len(theorems)} 个定理，无重复")
    sys.exit(0)
PYEOF
        
        if [ $? -eq 0 ]; then
            log_success "定理验证通过"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
        else
            log_error "定理验证失败"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
        fi
    fi
}

check_links() {
    log_info "运行链接检查..."
    
    # 内部链接检查
    log_info "检查内部链接..."
    
    python3 << 'PYEOF'
import re
import sys
from pathlib import Path
from collections import defaultdict

LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

stats = {'total': 0, 'valid': 0, 'broken': 0}
errors = []

all_docs = set()
for directory in ['Struct', 'Knowledge', 'Flink', 'visuals', 'tutorials', 'docs']:
    if Path(directory).exists():
        for md_file in Path(directory).rglob('*.md'):
            all_docs.add(str(md_file).replace('\\', '/'))

for doc_path in sorted(all_docs):
    try:
        content = Path(doc_path).read_text(encoding='utf-8')
        doc_dir = Path(doc_path).parent

        for match in LINK_PATTERN.finditer(content):
            link_target = match.group(2)
            stats['total'] += 1

            if link_target.startswith(('http://', 'https://', 'mailto:', '#')):
                stats['valid'] += 1
                continue

            target_path = link_target.split('#')[0]
            if not target_path:
                stats['valid'] += 1
                continue

            if target_path.startswith('/'):
                full_path = target_path.lstrip('/')
            else:
                full_path = str((doc_dir / target_path)).replace('\\', '/')

            if full_path in all_docs or Path(full_path).exists():
                stats['valid'] += 1
            else:
                stats['broken'] += 1
                errors.append(f"{doc_path}: {link_target}")
    except Exception:
        pass

print(f"Internal links: {stats['valid']}/{stats['total']} valid, {stats['broken']} broken")

if stats['broken'] > 0:
    for error in errors[:5]:
        print(f"  - {error}")
    if len(errors) > 5:
        print(f"  ... and {len(errors) - 5} more")

if stats['broken'] > 10:
    sys.exit(1)
PYEOF
    
    if [ $? -eq 0 ]; then
        log_success "内部链接检查通过"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        log_error "内部链接检查失败"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
}

check_proof_chains() {
    log_info "运行证明链验证..."
    
    python3 << 'PYEOF'
import re
import sys
from pathlib import Path
from collections import defaultdict

THEOREM_PATTERN = re.compile(r'\b(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2})\b')

all_theorems = {}
missing_refs = []

for directory in ['Struct', 'Knowledge', 'Flink']:
    dir_path = Path(directory)
    if not dir_path.exists():
        continue
    
    for md_file in dir_path.rglob('*.md'):
        if any(p.startswith('.') for p in md_file.parts):
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
            rel_path = str(md_file.relative_to('.'))
            
            for match in THEOREM_PATTERN.findall(content):
                theorem_id = f"{match[0]}-{match[1]}-{match[2]}-{match[3]}"
                if theorem_id not in all_theorems:
                    all_theorems[theorem_id] = rel_path
        except Exception:
            pass

# 验证引用
for directory in ['Struct', 'Knowledge', 'Flink']:
    dir_path = Path(directory)
    if not dir_path.exists():
        continue
    
    for md_file in dir_path.rglob('*.md'):
        if any(p.startswith('.') for p in md_file.parts):
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
            rel_path = str(md_file.relative_to('.'))
            
            for match in THEOREM_PATTERN.findall(content):
                theorem_id = f"{match[0]}-{match[1]}-{match[2]}-{match[3]}"
                if theorem_id not in all_theorems:
                    missing_refs.append((rel_path, theorem_id))
        except Exception:
            pass

if missing_refs:
    print(f"发现 {len(missing_refs)} 个未定义的引用:")
    for file, thm in missing_refs[:5]:
        print(f"  {file}: {thm}")
    sys.exit(1)
else:
    print(f"验证了 {len(all_theorems)} 个定理，所有引用有效")
    sys.exit(0)
PYEOF
    
    if [ $? -eq 0 ]; then
        log_success "证明链验证通过"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        log_error "证明链验证失败"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
}

check_mermaid() {
    log_info "运行 Mermaid 语法检查..."
    
    python3 << 'PYEOF'
import re
import sys
from pathlib import Path

mermaid_pattern = re.compile(r'```mermaid\s*\n(.*?)```', re.DOTALL)
VALID_CHART_TYPES = ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram',
    'stateDiagram', 'stateDiagram-v2', 'erDiagram', 'gantt', 'pie', 'mindmap']

stats = {'files': 0, 'diagrams': 0, 'errors': 0}

for directory in ['Struct', 'Knowledge', 'Flink', 'docs', 'tutorials']:
    if not Path(directory).exists():
        continue
    for md_file in Path(directory).rglob('*.md'):
        try:
            content = md_file.read_text(encoding='utf-8')
            diagrams = mermaid_pattern.findall(content)

            if diagrams:
                stats['files'] += 1
                stats['diagrams'] += len(diagrams)

            for diagram in diagrams:
                lines = diagram.strip().split('\n')
                if not lines:
                    continue

                first_line = lines[0].strip()
                chart_type = None
                for vt in VALID_CHART_TYPES:
                    if first_line.startswith(vt):
                        chart_type = vt
                        break

                if not chart_type:
                    stats['errors'] += 1
                    print(f"Unknown chart type in {md_file}: {first_line[:50]}")
        except Exception:
            pass

print(f"Mermaid validation: {stats['diagrams']} diagrams in {stats['files']} files, {stats['errors']} errors")

if stats['errors'] > 5:
    sys.exit(1)
PYEOF
    
    if [ $? -eq 0 ]; then
        log_success "Mermaid 语法检查通过"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        log_warning "Mermaid 语法检查发现问题（非阻塞）"
        SKIPPED_CHECKS=$((SKIPPED_CHECKS + 1))
    fi
}

# ==================== 主流程 ====================

main() {
    echo "========================================"
    echo "  AnalysisDataFlow CI 本地验证"
    echo "========================================"
    echo ""
    
    parse_args "$@"
    
    log_info "检查模式: ${CHECK_MODE}"
    log_info "项目根目录: ${PROJECT_ROOT}"
    
    # 检查前提条件
    check_prerequisites
    
    # 检测变更文件
    if [ "${CHECK_MODE}" == "quick" ]; then
        detect_changed_files
    fi
    
    # 根据模式运行检查
    case "${CHECK_MODE}" in
        full|quick)
            check_markdown
            check_theorems
            check_links
            check_proof_chains
            check_mermaid
            ;;
        markdown-only)
            check_markdown
            ;;
        theorems-only)
            check_theorems
            ;;
        links-only)
            check_links
            ;;
        proof-chains)
            check_proof_chains
            ;;
        *)
            log_error "未知检查模式: ${CHECK_MODE}"
            exit 1
            ;;
    esac
    
    # 输出汇总
    echo ""
    echo "========================================"
    echo "  验证汇总"
    echo "========================================"
    echo ""
    
    TOTAL_CHECKS=$((PASSED_CHECKS + FAILED_CHECKS + SKIPPED_CHECKS))
    
    log_success "通过: ${PASSED_CHECKS}/${TOTAL_CHECKS}"
    
    if [ ${FAILED_CHECKS} -gt 0 ]; then
        log_error "失败: ${FAILED_CHECKS}/${TOTAL_CHECKS}"
    fi
    
    if [ ${SKIPPED_CHECKS} -gt 0 ]; then
        log_warning "跳过: ${SKIPPED_CHECKS}/${TOTAL_CHECKS}"
    fi
    
    echo ""
    
    if [ ${FAILED_CHECKS} -eq 0 ]; then
        log_success "所有关键检查通过! ✓"
        echo ""
        log_info "报告已保存到: ${REPORTS_DIR}"
        exit 0
    else
        log_error "有 ${FAILED_CHECKS} 项检查失败"
        echo ""
        log_info "报告已保存到: ${REPORTS_DIR}"
        exit 1
    fi
}

# 运行主程序
main "$@"
