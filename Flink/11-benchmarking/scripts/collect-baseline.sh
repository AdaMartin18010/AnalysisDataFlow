#!/bin/bash
# collect-baseline.sh - 收集系统基线指标

OUTPUT_FILE="${1:-baseline.json}"

echo "=== 收集系统基线指标 ==="
echo "输出文件: $OUTPUT_FILE"

# 临时文件
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# 收集系统信息
collect_system_info() {
    cat > "$TEMP_DIR/system_info.json" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "hostname": "$(hostname)",
    "os": {
        "name": "$(uname -s)",
        "release": "$(uname -r)",
        "version": "$(uname -v)",
        "machine": "$(uname -m)"
    }
}
EOF
}

# 收集CPU信息
collect_cpu_info() {
    local cpu_info="{}"
    
    if command -v lscpu &> /dev/null; then
        cpu_info=$(lscpu -J 2>/dev/null || echo "{}")
    elif [ -f /proc/cpuinfo ]; then
        cpu_info=$(cat /proc/cpuinfo | jq -R -s -c 'split("\n")' 2>/dev/null || echo "[]")
    elif command -v sysctl &> /dev/null; then
        cpu_info=$(sysctl -a machdep.cpu 2>/dev/null | jq -R -s -c 'split("\n")' || echo "[]")
    fi
    
    echo "$cpu_info" > "$TEMP_DIR/cpu_info.json"
}

# 收集内存信息
collect_memory_info() {
    local mem_info="{}"
    
    if command -v free &> /dev/null; then
        mem_info=$(free -b | jq -R -s '
            split("\n") | 
            map(select(length > 0)) |
            map(split(" ") | map(select(length > 0))) |
            {
                total: (.[1][1] | tonumber),
                used: (.[1][2] | tonumber),
                free: (.[1][3] | tonumber),
                shared: (.[1][4] | tonumber),
                buff_cache: (.[1][5] | tonumber),
                available: (.[1][6] | tonumber)
            }
        ' 2>/dev/null || echo "{}")
    fi
    
    echo "$mem_info" > "$TEMP_DIR/memory_info.json"
}

# 收集磁盘信息
collect_disk_info() {
    local disk_info="[]"
    
    if command -v df &> /dev/null; then
        disk_info=$(df -B1 | grep -E '^/dev/' | jq -R -s '
            split("\n") | 
            map(select(length > 0)) |
            map(split(" ") | map(select(length > 0))) |
            map({
                filesystem: .[0],
                size: (.[1] | tonumber),
                used: (.[2] | tonumber),
                available: (.[3] | tonumber),
                use_percent: .[4],
                mount: .[5]
            })
        ' 2>/dev/null || echo "[]")
    fi
    
    echo "$disk_info" > "$TEMP_DIR/disk_info.json"
}

# 收集Flink配置
collect_flink_config() {
    local flink_config="{}"
    
    if [ -n "$FLINK_HOME" ] && [ -f "$FLINK_HOME/conf/flink-conf.yaml" ]; then
        flink_config=$(cat "$FLINK_HOME/conf/flink-conf.yaml" | jq -R -s '
            split("\n") |
            map(select(test("^[a-z].*:"))) |
            map(capture("(?<key>[^#:]+):\\s*(?<value>.*)")) |
            map(select(.key != null)) |
            from_entries
        ' 2>/dev/null || echo "{}")
    fi
    
    echo "$flink_config" > "$TEMP_DIR/flink_config.json"
}

# 收集网络配置
collect_network_info() {
    local net_info="{}"
    
    # 网络接口
    if command -v ip &> /dev/null; then
        net_info=$(ip -j addr show 2>/dev/null || echo "[]")
    elif command -v ifconfig &> /dev/null; then
        net_info=$(ifconfig -a | jq -R -s 'split("\n")' 2>/dev/null || echo "[]")
    fi
    
    echo "$net_info" > "$TEMP_DIR/network_info.json"
}

# 收集JVM信息
collect_jvm_info() {
    local jvm_info="{}"
    
    if command -v java &> /dev/null; then
        jvm_info=$(cat << EOF
{
    "java_version": "$(java -version 2>&1 | head -1)",
    "java_home": "${JAVA_HOME:-not set}",
    "jvm_args": {
        "heap_min": "${FLINK_ENV_JAVA_OPTS:-not set}",
        "heap_max": "${FLINK_ENV_JAVA_OPTS:-not set}"
    }
}
EOF
)
    fi
    
    echo "$jvm_info" > "$TEMP_DIR/jvm_info.json"
}

# 合并所有信息
generate_final_report() {
    jq -n \
        --argfile system "$TEMP_DIR/system_info.json" \
        --argfile cpu "$TEMP_DIR/cpu_info.json" \
        --argfile memory "$TEMP_DIR/memory_info.json" \
        --argfile disk "$TEMP_DIR/disk_info.json" \
        --argfile flink "$TEMP_DIR/flink_config.json" \
        --argfile network "$TEMP_DIR/network_info.json" \
        --argfile jvm "$TEMP_DIR/jvm_info.json" \
        '{
            metadata: {
                collection_time: now,
                version: "1.0"
            },
            system: $system,
            cpu: $cpu,
            memory: $memory,
            disk: $disk,
            network: $network,
            flink_config: $flink,
            jvm: $jvm
        }' > "$OUTPUT_FILE"
}

# 主流程
main() {
    echo "正在收集系统信息..."
    collect_system_info
    
    echo "正在收集CPU信息..."
    collect_cpu_info
    
    echo "正在收集内存信息..."
    collect_memory_info
    
    echo "正在收集磁盘信息..."
    collect_disk_info
    
    echo "正在收集网络信息..."
    collect_network_info
    
    echo "正在收集Flink配置..."
    collect_flink_config
    
    echo "正在收集JVM信息..."
    collect_jvm_info
    
    echo "正在生成报告..."
    generate_final_report
    
    echo "基线指标已保存到: $OUTPUT_FILE"
    
    # 显示摘要
    echo ""
    echo "=== 基线摘要 ==="
    jq -r '
        "OS: \(.system.os.name) \(.system.os.release)",
        "Hostname: \(.system.hostname)",
        "Memory: \(.memory.total / 1024 / 1024 / 1024 | floor)GB total",
        "Flink Config Keys: \(.flink_config | keys | length)"
    ' "$OUTPUT_FILE"
}

# 检查jq
if ! command -v jq &> /dev/null; then
    echo "错误: 需要安装 jq (JSON处理器)"
    echo "Ubuntu/Debian: sudo apt-get install jq"
    echo "CentOS/RHEL: sudo yum install jq"
    echo "macOS: brew install jq"
    exit 1
fi

main "$@"
