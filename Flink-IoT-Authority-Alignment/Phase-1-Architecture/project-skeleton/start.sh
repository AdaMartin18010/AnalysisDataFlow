#!/bin/bash
# ============================================================================
# Flink IoT 项目 - 快速启动脚本
# 支持: Linux / macOS / Git Bash on Windows
# ============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}  Flink IoT Project - Quick Start${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# 检查docker和docker-compose
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: docker-compose is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker and docker-compose are available${NC}"

# 函数: 等待服务就绪
wait_for_service() {
    local name=$1
    local url=$2
    local max_attempts=${3:-30}
    local attempt=1
    
    echo -n "Waiting for $name..."
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo -e " ${GREEN}✓ Ready${NC}"
            return 0
        fi
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    echo -e " ${YELLOW}⚠ Timeout (may still be starting)${NC}"
    return 1
}

# 解析参数
MODE=${1:-"all"}

case "$MODE" in
    "all")
        echo -e "${BLUE}Starting all services...${NC}"
        docker-compose up -d
        ;;
    "infra")
        echo -e "${BLUE}Starting infrastructure only (no data generator)...${NC}"
        docker-compose up -d zookeeper kafka flink-jobmanager flink-taskmanager emqx influxdb grafana prometheus
        ;;
    "clean")
        echo -e "${YELLOW}Stopping all services and removing volumes...${NC}"
        docker-compose down -v
        echo -e "${GREEN}✓ All services stopped and volumes removed${NC}"
        exit 0
        ;;
    "stop")
        echo -e "${YELLOW}Stopping all services...${NC}"
        docker-compose down
        echo -e "${GREEN}✓ All services stopped${NC}"
        exit 0
        ;;
    *)
        echo "Usage: $0 [all|infra|clean|stop]"
        echo "  all   - Start all services including data generator (default)"
        echo "  infra - Start infrastructure only"
        echo "  clean - Stop and remove all data"
        echo "  stop  - Stop services without removing data"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}Waiting for services to be ready...${NC}"
echo ""

# 等待核心服务就绪
wait_for_service "Flink JobManager" "http://localhost:8081/overview" 30
wait_for_service "Grafana" "http://localhost:3000/api/health" 20
wait_for_service "InfluxDB" "http://localhost:8086/health" 20

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  All services are starting up!${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo -e "${BLUE}Service URLs:${NC}"
echo "  Flink Web UI:      http://localhost:8081"
echo "  Grafana:           http://localhost:3000 (admin/flink-iot-grafana)"
echo "  EMQX Dashboard:    http://localhost:18083 (admin/public)"
echo "  Prometheus:        http://localhost:9090"
echo "  InfluxDB:          http://localhost:8086"
echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo "  View logs:         docker-compose logs -f [service]"
echo "  Scale TaskManager: docker-compose up -d --scale flink-taskmanager=2"
echo "  Run SQL client:    docker-compose exec flink-jobmanager ./bin/sql-client.sh"
echo "  Check status:      docker-compose ps"
echo ""
echo -e "${YELLOW}Note: Data generator may take 1-2 minutes to start producing data${NC}"
