#!/bin/bash
# Flink 作业提交脚本

if [ $# -lt 2 ]; then
    echo "Usage: $0 <main-class> <jar-path> [args...]"
    echo "Example: $0 com.example.WordCount /jobs/my-app.jar"
    exit 1
fi

MAIN_CLASS=$1
JAR_PATH=$2
shift 2

echo "Submitting Flink job..."
echo "  Main Class: $MAIN_CLASS"
echo "  JAR Path: $JAR_PATH"
echo "  Args: $@"

docker-compose exec jobmanager flink run \
    -c "$MAIN_CLASS" \
    "$JAR_PATH" \
    "$@"

echo "Job submitted. Check Flink Web UI at http://localhost:8081"
