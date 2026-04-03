# AnalysisDataFlow 项目验证环境
# 基于Python 3.11，包含Node.js和Mermaid CLI

FROM python:3.11-slim

LABEL maintainer="AnalysisDataFlow Project"
LABEL description="Docker environment for validating AnalysisDataFlow project"

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV NODE_VERSION=20.x
ENV DEBIAN_FRONTEND=noninteractive

# 安装系统依赖和Node.js
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    build-essential \
    chromium \
    fonts-noto-cjk \
    && curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION} | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安装Mermaid CLI
RUN npm install -g @mermaid-js/mermaid-cli@latest

# 设置工作目录
WORKDIR /workspace

# 复制验证脚本（用于缓存优化）
COPY .vscode/validate-*.py /workspace/.vscode/

# 验证安装
RUN python3 --version && node --version && npm --version && mmdc --version

# 设置默认命令
CMD ["python3", ".vscode/validate-project.py"]
