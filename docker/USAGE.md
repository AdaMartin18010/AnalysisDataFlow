# AnalysisDataFlow Docker 使用指南

本文档介绍如何使用Docker环境来验证和开发 AnalysisDataFlow 项目。

## 目录

- [AnalysisDataFlow Docker 使用指南](#analysisdataflow-docker-使用指南)
  - [目录](#目录)
  - [快速开始](#快速开始)
    - [1. 构建镜像](#1-构建镜像)
    - [2. 运行验证](#2-运行验证)
    - [3. 进入交互式Shell](#3-进入交互式shell)
  - [可用服务](#可用服务)
    - [`validate` - 完整验证](#validate---完整验证)
    - [`stats` - 生成统计报告](#stats---生成统计报告)
    - [`shell` - 交互式开发环境](#shell---交互式开发环境)
    - [单独验证服务](#单独验证服务)
  - [常用命令](#常用命令)
    - [构建相关](#构建相关)
    - [运行验证](#运行验证)
    - [交互式使用](#交互式使用)
    - [清理](#清理)
  - [与CI/CD集成](#与cicd集成)
    - [GitHub Actions 示例](#github-actions-示例)
    - [GitLab CI 示例](#gitlab-ci-示例)
    - [Azure DevOps 示例](#azure-devops-示例)
  - [故障排除](#故障排除)
    - [问题：权限错误](#问题权限错误)
    - [问题：Mermaid验证超时](#问题mermaid验证超时)
    - [问题：内存不足](#问题内存不足)
    - [问题：中文显示问题](#问题中文显示问题)
    - [问题：卷挂载问题](#问题卷挂载问题)
  - [自定义配置](#自定义配置)
    - [环境变量](#环境变量)
    - [添加自定义验证](#添加自定义验证)
  - [参考](#参考)

---

## 快速开始

### 1. 构建镜像

```bash
# 使用Docker Compose构建
docker-compose build

# 或使用Makefile
make docker-build
```

### 2. 运行验证

```bash
# 运行所有验证
docker-compose run --rm validate

# 或使用Makefile
make docker-validate
```

### 3. 进入交互式Shell

```bash
# 启动开发环境
docker-compose run --rm shell

# 或使用Makefile
make docker-shell
```

---

## 可用服务

### `validate` - 完整验证

运行所有验证脚本：

```bash
docker-compose run --rm validate
```

这将依次执行：

1. 项目验证（定理/定义编号检查）
2. 交叉引用验证（链接检查）
3. Mermaid图表验证

### `stats` - 生成统计报告

生成JSON格式的详细报告：

```bash
docker-compose run --rm stats
```

报告将保存在 `reports/` 目录下：

- `validation-report.json` - 项目验证报告
- `cross-ref-report.json` - 交叉引用报告
- `mermaid-report.json` - Mermaid验证报告

### `shell` - 交互式开发环境

进入容器的bash shell：

```bash
docker-compose run --rm shell
```

在shell中你可以：

- 运行单个验证脚本
- 检查文件
- 手动执行命令

### 单独验证服务

```bash
# 仅验证项目
docker-compose run --rm validate-project

# 仅验证交叉引用
docker-compose run --rm validate-crossrefs

# 仅验证Mermaid图表
docker-compose run --rm validate-mermaid
```

---

## 常用命令

### 构建相关

```bash
# 构建所有服务镜像
docker-compose build

# 不使用缓存重新构建
docker-compose build --no-cache

# 构建特定服务
docker-compose build validate
```

### 运行验证

```bash
# 运行所有验证
docker-compose run --rm validate

# 生成统计报告
docker-compose run --rm stats

# 以JSON格式输出验证结果
docker-compose run --rm validate-project --json
```

### 交互式使用

```bash
# 进入shell
docker-compose run --rm shell

# 在shell中运行验证
python3 .vscode/validate-project.py
python3 .vscode/validate-cross-refs.py
python3 .vscode/validate-mermaid.py

# 退出shell
exit
```

### 清理

```bash
# 停止所有容器
docker-compose down

# 停止并删除所有容器和网络
docker-compose down -v

# 删除镜像
docker rmi analysisdataflow_validate
```

---

## 与CI/CD集成

### GitHub Actions 示例

```yaml
name: Validate Project

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Build Docker image
      run: docker-compose build validate

    - name: Run project validation
      run: docker-compose run --rm validate-project

    - name: Run cross-reference validation
      run: docker-compose run --rm validate-crossrefs

    - name: Run Mermaid validation
      run: docker-compose run --rm validate-mermaid

    - name: Generate reports
      if: always()
      run: docker-compose run --rm stats

    - name: Upload reports
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: validation-reports
        path: reports/
```

### GitLab CI 示例

```yaml
validate:
  stage: test
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker-compose build validate
    - docker-compose run --rm validate
  artifacts:
    paths:
      - reports/
    when: always
```

### Azure DevOps 示例

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: DockerCompose@0
  inputs:
    containerregistrytype: 'Container Registry'
    dockerComposeFile: '**/docker-compose.yml'
    action: 'Run services'
    services: 'validate'
```

---

## 故障排除

### 问题：权限错误

**症状**: 无法读取文件或写入报告

**解决**:

```bash
# 确保报告目录存在并有正确权限
mkdir -p reports
chmod 755 reports

# 在Windows上，可能需要调整卷挂载
```

### 问题：Mermaid验证超时

**症状**: Mermaid验证脚本超时

**解决**:

- 某些复杂的Mermaid图表可能需要更长时间
- 使用 `--online` 选项切换到在线验证：

  ```bash
  docker-compose run --rm validate-mermaid --online
  ```

### 问题：内存不足

**症状**: 容器被kill或内存错误

**解决**:

```bash
# 增加Docker内存限制
docker-compose run --rm -m 2g validate
```

### 问题：中文显示问题

**症状**: 终端中中文显示为乱码

**解决**:
镜像已安装 `fonts-noto-cjk` 字体包，如果仍有问题：

```bash
# 在宿主机设置正确的locale
export LANG=zh_CN.UTF-8
```

### 问题：卷挂载问题

**症状**: 文件修改后容器中看不到变化

**解决**:

```bash
# 确保使用正确的路径格式（Windows vs Linux/Mac）
# Windows:
docker-compose -f docker-compose.yml -f docker-compose.windows.yml run validate

# 或尝试直接挂载
docker run -v ${PWD}:/workspace:ro analysisdataflow_validate
```

---

## 自定义配置

### 环境变量

你可以通过环境变量自定义验证行为：

```bash
# 设置超时时间
VALIDATION_TIMEOUT=300 docker-compose run validate

# 启用详细输出
VERBOSE=1 docker-compose run validate
```

### 添加自定义验证

编辑 `docker-compose.yml` 添加新的服务：

```yaml
  my-custom-check:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - .:/workspace:ro
    command: python3 my-custom-script.py
```

---

## 参考

- [Docker 文档](https://docs.docker.com/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [Mermaid CLI 文档](https://github.com/mermaid-js/mermaid-cli)
- [Project README](../README.md)
