# ============================================================================
# Flink IoT 项目 - Windows PowerShell 快速启动脚本
# ============================================================================

$ErrorActionPreference = "Stop"

# 颜色函数
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) { Write-Output $args }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-ColorOutput Blue "============================================================"
Write-ColorOutput Blue "  Flink IoT Project - Quick Start (PowerShell)"
Write-ColorOutput Blue "============================================================"
Write-Output ""

# 检查docker
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-ColorOutput Red "Error: Docker is not installed"
    exit 1
}

if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-ColorOutput Red "Error: docker-compose is not installed"
    exit 1
}

Write-ColorOutput Green "✓ Docker and docker-compose are available"

# 解析参数
$MODE = if ($args[0]) { $args[0] } else { "all" }

switch ($MODE) {
    "all" {
        Write-ColorOutput Blue "Starting all services..."
        docker-compose up -d
    }
    "infra" {
        Write-ColorOutput Blue "Starting infrastructure only (no data generator)..."
        docker-compose up -d zookeeper kafka flink-jobmanager flink-taskmanager emqx influxdb grafana prometheus
    }
    "clean" {
        Write-ColorOutput Yellow "Stopping all services and removing volumes..."
        docker-compose down -v
        Write-ColorOutput Green "✓ All services stopped and volumes removed"
        exit 0
    }
    "stop" {
        Write-ColorOutput Yellow "Stopping all services..."
        docker-compose down
        Write-ColorOutput Green "✓ All services stopped"
        exit 0
    }
    default {
        Write-Output "Usage: .\start.ps1 [all|infra|clean|stop]"
        Write-Output "  all   - Start all services including data generator (default)"
        Write-Output "  infra - Start infrastructure only"
        Write-Output "  clean - Stop and remove all data"
        Write-Output "  stop  - Stop services without removing data"
        exit 1
    }
}

Write-Output ""
Write-ColorOutput Blue "Waiting for services to be ready..."
Write-Output ""

# 等待服务就绪函数
function Wait-ForService($Name, $Url, $MaxAttempts = 30) {
    $attempt = 1
    Write-Host -NoNewline "Waiting for $Name..."
    while ($attempt -le $MaxAttempts) {
        try {
            $response = Invoke-WebRequest -Uri $Url -Method HEAD -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-ColorOutput Green " ✓ Ready"
                return $true
            }
        } catch {
            # Continue waiting
        }
        Write-Host -NoNewline "."
        Start-Sleep -Seconds 2
        $attempt++
    }
    Write-ColorOutput Yellow " ⚠ Timeout (may still be starting)"
    return $false
}

# 等待核心服务
Wait-ForService "Flink JobManager" "http://localhost:8081/overview" 30
Wait-ForService "Grafana" "http://localhost:3000/api/health" 20

Write-Output ""
Write-ColorOutput Green "============================================================"
Write-ColorOutput Green "  All services are starting up!"
Write-ColorOutput Green "============================================================"
Write-Output ""
Write-ColorOutput Blue "Service URLs:"
Write-Output "  Flink Web UI:      http://localhost:8081"
Write-Output "  Grafana:           http://localhost:3000 (admin/flink-iot-grafana)"
Write-Output "  EMQX Dashboard:    http://localhost:18083 (admin/public)"
Write-Output "  Prometheus:        http://localhost:9090"
Write-Output "  InfluxDB:          http://localhost:8086"
Write-Output ""
Write-ColorOutput Blue "Useful commands:"
Write-Output "  View logs:         docker-compose logs -f [service]"
Write-Output "  Scale TaskManager: docker-compose up -d --scale flink-taskmanager=2"
Write-Output "  Run SQL client:    docker-compose exec flink-jobmanager .\bin\sql-client.sh"
Write-Output "  Check status:      docker-compose ps"
Write-Output ""
Write-ColorOutput Yellow "Note: Data generator may take 1-2 minutes to start producing data"
