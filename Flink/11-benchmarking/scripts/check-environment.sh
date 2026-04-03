#!/bin/bash
# check-environment.sh - 环境检查脚本

set -e

echo "=== Flink基准测试环境检查 ==="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0
WARN=0

check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 已安装: $(command -v $1)"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗${NC} $1 未找到"
        ((FAIL++))
        return 1
    fi
}

check_version() {
    local cmd=$1
    local expected=$2
    local actual=$($cmd 2>&1 | head -1)
    echo "  版本: $actual"
}

check_java() {
    echo "检查 Java 环境..."
    if check_command java; then
        JAVA_VERSION=$(java -version 2>&1 | head -1 | cut -d'"' -f2)
        echo "  Java版本: $JAVA_VERSION"
        
        # 检查Java版本 >= 11
        if [[ $JAVA_VERSION == 11.* ]] || [[ $JAVA_VERSION == 17.* ]] || [[ $JAVA_VERSION == 21.* ]]; then
            echo -e "${GREEN}✓${NC} Java版本符合要求 (>= 11)"
            ((PASS++))
        else
            echo -e "${YELLOW}!${NC} 建议使用Java 11或更高版本"
            ((WARN++))
        fi
    fi
    echo ""
}

check_flink() {
    echo "检查 Flink 环境..."
    if check_command flink; then
        FLINK_VERSION=$(flink --version 2>&1 | grep -oP 'Version: \K[^,]+')
        echo "  Flink版本: $FLINK_VERSION"
        
        # 检查FLINK_HOME
        if [ -z "$FLINK_HOME" ]; then
            echo -e "${YELLOW}!${NC} FLINK_HOME 未设置"
            ((WARN++))
        else
            echo -e "${GREEN}✓${NC} FLINK_HOME: $FLINK_HOME"
            ((PASS++))
        fi
    fi
    echo ""
}

check_kafka() {
    echo "检查 Kafka 环境..."
    if check_command kafka-topics.sh; then
        echo -e "${GREEN}✓${NC} Kafka CLI 已安装"
        ((PASS++))
    else
        echo -e "${YELLOW}!${NC} Kafka CLI 未找到（如果使用Kafka作为Source则需要）"
        ((WARN++))
    fi
    echo ""
}

check_monitoring() {
    echo "检查监控工具..."
    
    # Prometheus
    if check_command prometheus; then
        PROM_VERSION=$(prometheus --version 2>&1 | head -1)
        echo "  $PROM_VERSION"
    else
        echo -e "${YELLOW}!${NC} Prometheus 未安装（推荐用于指标收集）"
        ((WARN++))
    fi
    
    # kubectl (如果使用K8s)
    if command -v kubectl &> /dev/null; then
        echo -e "${GREEN}✓${NC} kubectl 已安装"
        K8S_VERSION=$(kubectl version --client 2>&1 | grep -oP 'GitVersion:"\K[^"]+')
        echo "  版本: $K8S_VERSION"
        ((PASS++))
    fi
    
    echo ""
}

check_resources() {
    echo "检查系统资源..."
    
    # CPU
    CPU_COUNT=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "未知")
    echo "  CPU核心数: $CPU_COUNT"
    
    # 内存
    if command -v free &> /dev/null; then
        MEM_TOTAL=$(free -h | awk '/^Mem:/ {print $2}')
        MEM_AVAILABLE=$(free -h | awk '/^Mem:/ {print $7}')
        echo "  总内存: $MEM_TOTAL"
        echo "  可用内存: $MEM_AVAILABLE"
    elif command -v vm_stat &> /dev/null; then
        echo "  内存信息: $(vm_stat | head -5)"
    fi
    
    # 磁盘
    echo "  磁盘空间:"
    df -h | grep -E '^/dev/' | head -5 | while read line; do
        echo "    $line"
    done
    
    # 推荐配置检查
    if [ "$CPU_COUNT" -lt 8 ] 2>/dev/null; then
        echo -e "${YELLOW}!${NC} 建议至少8核CPU以获得准确结果"
        ((WARN++))
    else
        ((PASS++))
    fi
    
    echo ""
}

check_network() {
    echo "检查网络配置..."
    
    # 检查端口占用
    if command -v netstat &> /dev/null; then
        FLINK_PORTS=$(netstat -tlnp 2>/dev/null | grep -E '8081|6123' || true)
        if [ -n "$FLINK_PORTS" ]; then
            echo -e "${YELLOW}!${NC} Flink端口已被占用:"
            echo "$FLINK_PORTS"
            ((WARN++))
        else
            echo -e "${GREEN}✓${NC} Flink默认端口可用"
            ((PASS++))
        fi
    fi
    
    echo ""
}

check_benchmark_jars() {
    echo "检查基准测试JAR包..."
    
    if [ -f "./nexmark-flink.jar" ]; then
        echo -e "${GREEN}✓${NC} nexmark-flink.jar 存在"
        ((PASS++))
    else
        echo -e "${YELLOW}!${NC} nexmark-flink.jar 未找到"
        echo "  请从 https://github.com/nexmark/nexmark/releases 下载"
        ((WARN++))
    fi
    
    if [ -f "./benchmark.jar" ]; then
        echo -e "${GREEN}✓${NC} benchmark.jar 存在"
        ((PASS++))
    else
        echo -e "${YELLOW}!${NC} benchmark.jar 未找到"
        echo "  请构建自定义基准测试JAR"
        ((WARN++))
    fi
    
    echo ""
}

# 主流程
main() {
    check_java
    check_flink
    check_kafka
    check_monitoring
    check_resources
    check_network
    check_benchmark_jars
    
    # 总结
    echo "=== 检查总结 ==="
    echo -e "${GREEN}通过: $PASS${NC}"
    echo -e "${YELLOW}警告: $WARN${NC}"
    echo -e "${RED}失败: $FAIL${NC}"
    echo ""
    
    if [ $FAIL -eq 0 ]; then
        echo -e "${GREEN}环境检查通过！可以继续执行基准测试。${NC}"
        exit 0
    else
        echo -e "${RED}环境检查失败！请修复上述问题后再运行测试。${NC}"
        exit 1
    fi
}

main "$@"
