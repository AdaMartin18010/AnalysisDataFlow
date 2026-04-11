#!/bin/bash
# Flink可运行示例验证脚本
# 用于验证所有示例项目的完整性和可运行性

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 计数器
TOTAL=0
PASSED=0
FAILED=0

echo "====================================="
echo "Flink可运行示例验证脚本"
echo "====================================="
echo ""

# 检查目录是否存在
check_directory() {
    local dir=$1
    local name=$2
    TOTAL=$((TOTAL + 1))
    
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅${NC} $name 目录存在"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}❌${NC} $name 目录不存在: $dir"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

# 检查文件是否存在
check_file() {
    local file=$1
    local name=$2
    TOTAL=$((TOTAL + 1))
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅${NC} $name 文件存在"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}❌${NC} $name 文件不存在: $file"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

# 检查Java项目
check_java_project() {
    local project=$1
    local dir="examples/java/$project"
    
    echo ""
    echo "检查Java项目: $project"
    echo "-------------------------------------"
    
    check_directory "$dir" "$project"
    check_file "$dir/pom.xml" "pom.xml"
    check_file "$dir/README.md" "README.md"
    check_file "$dir/src/main/java/com/example/flink/*.java" "主程序"
}

# 检查Python项目
check_python_project() {
    local project=$1
    local dir="examples/python/$project"
    
    echo ""
    echo "检查Python项目: $project"
    echo "-------------------------------------"
    
    check_directory "$dir" "$project"
    check_file "$dir/requirements.txt" "requirements.txt"
    check_file "$dir/README.md" "README.md"
    check_file "$dir/*.py" "主程序"
}

# 验证Maven项目
validate_maven() {
    local project=$1
    local dir="examples/java/$project"
    
    echo ""
    echo "验证Maven项目: $project"
    echo "-------------------------------------"
    
    if [ -f "$dir/pom.xml" ]; then
        cd "$dir"
        if mvn validate -q > /dev/null 2>&1; then
            echo -e "${GREEN}✅${NC} Maven配置有效"
            PASSED=$((PASSED + 1))
        else
            echo -e "${RED}❌${NC} Maven配置无效"
            FAILED=$((FAILED + 1))
        fi
        cd - > /dev/null
    fi
    TOTAL=$((TOTAL + 1))
}

# 验证Python语法
validate_python() {
    local project=$1
    local dir="examples/python/$project"
    
    echo ""
    echo "验证Python项目: $project"
    echo "-------------------------------------"
    
    local py_files=$(find "$dir" -name "*.py" -type f 2>/dev/null)
    if [ -n "$py_files" ]; then
        local valid=true
        for file in $py_files; do
            if ! python -m py_compile "$file" 2>/dev/null; then
                echo -e "${RED}❌${NC} 语法错误: $(basename $file)"
                valid=false
            fi
        done
        
        if [ "$valid" = true ]; then
            echo -e "${GREEN}✅${NC} Python语法检查通过"
            PASSED=$((PASSED + 1))
        else
            FAILED=$((FAILED + 1))
        fi
    else
        echo -e "${YELLOW}⚠️${NC} 未找到Python文件"
    fi
    TOTAL=$((TOTAL + 1))
}

# 检查Docker配置
check_docker() {
    echo ""
    echo "检查Docker配置"
    echo "-------------------------------------"
    
    check_file "examples/docker/docker-compose.yml" "docker-compose.yml"
    check_file "examples/docker/README.md" "README.md"
    
    if command -v docker-compose &> /dev/null; then
        if docker-compose -f examples/docker/docker-compose.yml config > /dev/null 2>&1; then
            echo -e "${GREEN}✅${NC} Docker Compose配置有效"
            PASSED=$((PASSED + 1))
        else
            echo -e "${RED}❌${NC} Docker Compose配置无效"
            FAILED=$((FAILED + 1))
        fi
    else
        echo -e "${YELLOW}⚠️${NC} Docker Compose未安装，跳过验证"
    fi
    TOTAL=$((TOTAL + 1))
}

# 检查CI配置
check_ci() {
    echo ""
    echo "检查CI配置"
    echo "-------------------------------------"
    
    check_file ".github/workflows/examples-ci.yml" "CI工作流"
}

# 主流程
echo "1. 检查项目结构"
echo "====================================="

check_java_project "wordcount"
check_java_project "windowing"
check_java_project "stateful"

check_python_project "wordcount"
check_python_project "table-api"

check_docker
check_ci

echo ""
echo "2. 验证项目配置"
echo "====================================="

validate_maven "wordcount"
validate_maven "windowing"
validate_maven "stateful"

validate_python "wordcount"
validate_python "table-api"

echo ""
echo "====================================="
echo "验证完成!"
echo "====================================="
echo "总计: $TOTAL 项"
echo -e "通过: ${GREEN}$PASSED${NC} 项"
echo -e "失败: ${RED}$FAILED${NC} 项"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ 所有验证通过!${NC}"
    echo ""
    echo "可运行的示例数量: 5 个"
    echo "  - Java: 3 个 (wordcount, windowing, stateful)"
    echo "  - Python: 2 个 (wordcount, table-api)"
    echo "  - Docker: 1 个 (一键启动环境)"
    exit 0
else
    echo -e "${RED}❌ 存在失败的验证项，请修复后重试${NC}"
    exit 1
fi
