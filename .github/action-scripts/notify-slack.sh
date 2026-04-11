#!/bin/bash
# Slack通知脚本
# 用法: ./notify-slack.sh --webhook-url $SLACK_WEBHOOK --message "Build failed"

set -e

WEBHOOK_URL=""
MESSAGE=""
COLOR="good"  # good, warning, danger

# 解析参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --webhook-url)
      WEBHOOK_URL="$2"
      shift 2
      ;;
    --message)
      MESSAGE="$2"
      shift 2
      ;;
    --color)
      COLOR="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$WEBHOOK_URL" || -z "$MESSAGE" ]]; then
  echo "Usage: $0 --webhook-url <url> --message <message> [--color <color>]"
  exit 1
fi

# 构建Slack消息payload
PAYLOAD=$(cat <<EOF
{
  "attachments": [
    {
      "color": "$COLOR",
      "text": "$MESSAGE",
      "footer": "GitHub Actions",
      "ts": $(date +%s)
    }
  ]
}
EOF
)

# 发送通知
curl -s -X POST -H 'Content-type: application/json' \
  --data "$PAYLOAD" \
  "$WEBHOOK_URL"

echo "Notification sent successfully"
