#!/bin/bash
# Cloudflare Pages 部署配置脚本
# 用法: ./setup-cloudflare.sh <project-name>

set -e

PROJECT_NAME=${1:-"analysisdataflow-kg"}

echo "🚀 Cloudflare Pages 部署配置"
echo "=============================="
echo ""

# 检查 wrangler 是否安装
if ! command -v wrangler &> /dev/null; then
    echo "📦 安装 wrangler CLI..."
    npm install -g wrangler
fi

# 登录 Cloudflare
echo "🔑 登录 Cloudflare..."
wrangler login

# 创建 wrangler.toml
echo "📝 创建 wrangler.toml..."
cat > wrangler.toml << EOF
name = "${PROJECT_NAME}"
compatibility_date = "2026-04-12"

[build]
command = "python .scripts/kg-v2/generate-static-data.py && python .scripts/kg-v2/optimize-assets.py"

[site]
bucket = "./knowledge-graph-site"

[build.upload]
format = "directory"

# 环境变量（需要在 Cloudflare Dashboard 中设置）
# [env.production]
# vars = { ENVIRONMENT = "production" }

# [env.staging]
# vars = { ENVIRONMENT = "staging" }
EOF

echo "✅ wrangler.toml 已创建"
echo ""

# 创建 _headers 文件 (Cloudflare Pages 自定义头部)
echo "📝 创建 _headers..."
cat > knowledge-graph-site/_headers << 'EOF'
# 安全头部
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()

# JSON 文件缓存
/data/*.json
  Cache-Control: public, max-age=3600

# Gzip 压缩文件
/data/*.gz
  Content-Encoding: gzip
  Cache-Control: public, max-age=86400

# Service Worker 不缓存
/service-worker.js
  Cache-Control: no-cache
EOF

echo "✅ _headers 已创建"
echo ""

# 创建 _redirects 文件
echo "📝 创建 _redirects..."
cat > knowledge-graph-site/_redirects << 'EOF'
# SPA 回退
/* /index.html 200
EOF

echo "✅ _redirects 已创建"
echo ""

echo "🎉 配置完成!"
echo ""
echo "下一步:"
echo "1. 在 Cloudflare Dashboard 创建 Pages 项目"
echo "2. 连接 GitHub 仓库"
echo "3. 配置构建设置:"
echo "   - Build command: python .scripts/kg-v2/generate-static-data.py && python .scripts/kg-v2/optimize-assets.py"
echo "   - Build output directory: knowledge-graph-site"
echo ""
echo "或使用 wrangler 直接部署:"
echo "   wrangler pages deploy knowledge-graph-site"
