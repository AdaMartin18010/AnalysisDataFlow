# AnalysisDataFlow Project Makefile
# 提供便捷的Docker和验证命令

.PHONY: help docker-build docker-validate docker-shell docker-stats docker-clean validate-local

# 默认目标
.DEFAULT_GOAL := help

# 颜色定义（用于输出）
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
NC := \033[0m # No Color

##@ 帮助

help: ## 显示此帮助信息
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "$(BLUE)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

##@ Docker 命令

docker-build: ## 构建Docker镜像
	@echo "$(GREEN)>>> 构建Docker镜像...$(NC)"
	docker-compose build

docker-build-no-cache: ## 不使用缓存构建Docker镜像
	@echo "$(GREEN)>>> 重新构建Docker镜像（无缓存）...$(NC)"
	docker-compose build --no-cache

docker-validate: ## 运行所有Docker验证
	@echo "$(GREEN)>>> 运行Docker验证...$(NC)"
	docker-compose run --rm validate

docker-validate-project: ## 仅运行项目验证
	@echo "$(GREEN)>>> 运行项目验证...$(NC)"
	docker-compose run --rm validate-project

docker-validate-crossrefs: ## 仅运行交叉引用验证
	@echo "$(GREEN)>>> 运行交叉引用验证...$(NC)"
	docker-compose run --rm validate-crossrefs

docker-validate-mermaid: ## 仅运行Mermaid验证
	@echo "$(GREEN)>>> 运行Mermaid验证...$(NC)"
	docker-compose run --rm validate-mermaid

docker-stats: ## 生成统计报告
	@echo "$(GREEN)>>> 生成统计报告...$(NC)"
	mkdir -p reports
	docker-compose run --rm stats

docker-shell: ## 进入Docker交互式shell
	@echo "$(GREEN)>>> 进入Docker shell...$(NC)"
	docker-compose run --rm shell

docker-clean: ## 清理Docker容器和镜像
	@echo "$(YELLOW)>>> 清理Docker资源...$(NC)"
	docker-compose down --rmi all --volumes --remove-orphans
	@echo "$(GREEN)>>> 清理完成$(NC)"

docker-prune: ## 深度清理所有未使用的Docker资源
	@echo "$(RED)>>> 深度清理Docker资源...$(NC)"
	docker system prune -f --volumes
	@echo "$(GREEN)>>> 深度清理完成$(NC)"

##@ 本地验证（需要Python 3.11+）

validate-local: ## 在本地运行所有验证（需要Python 3.11+）
	@echo "$(GREEN)>>> 运行本地项目验证...$(NC)"
	python3 .vscode/validate-project.py
	@echo "$(GREEN)>>> 运行本地交叉引用验证...$(NC)"
	python3 .vscode/validate-cross-refs.py
	@echo "$(GREEN)>>> 运行本地Mermaid验证...$(NC)"
	python3 .vscode/validate-mermaid.py

validate-project-local: ## 在本地运行项目验证
	python3 .vscode/validate-project.py

validate-crossrefs-local: ## 在本地运行交叉引用验证
	python3 .vscode/validate-cross-refs.py

validate-mermaid-local: ## 在本地运行Mermaid验证
	python3 .vscode/validate-mermaid.py

##@ 报告和统计

reports: ## 生成所有验证报告（JSON格式）
	@echo "$(GREEN)>>> 生成验证报告...$(NC)"
	mkdir -p reports
	python3 .vscode/validate-project.py --json > reports/validation-report.json
	python3 .vscode/validate-cross-refs.py --json > reports/cross-ref-report.json
	python3 .vscode/validate-mermaid.py --json > reports/mermaid-report.json
	@echo "$(GREEN)>>> 报告已保存到 reports/ 目录$(NC)"

stats: ## 显示项目统计信息
	@echo "$(BLUE)=== AnalysisDataFlow 项目统计 ===$(NC)"
	@echo "文档数量:"
	@find Struct Knowledge Flink -name "*.md" 2>/dev/null | wc -l
	@echo ""
	@echo "代码行数:"
	@find .vscode -name "*.py" -exec wc -l {} + 2>/dev/null | tail -1

##@ CI/CD 集成

ci-validate: ## CI/CD验证命令（不交互，输出JSON）
	@echo "$(GREEN)>>> 运行CI验证...$(NC)"
	python3 .vscode/validate-project.py --json
	python3 .vscode/validate-cross-refs.py --json
	python3 .vscode/validate-mermaid.py --json

ci-docker-validate: ## CI/CD Docker验证
	@echo "$(GREEN)>>> 运行Docker CI验证...$(NC)"
	docker-compose run --rm validate-project
	docker-compose run --rm validate-crossrefs
	docker-compose run --rm validate-mermaid

##@ 开发工具

dev-setup: ## 设置开发环境
	@echo "$(GREEN)>>> 检查依赖...$(NC)"
	@python3 --version || (echo "$(RED)需要Python 3.11+$(NC)" && exit 1)
	@which docker || (echo "$(RED)需要Docker$(NC)" && exit 1)
	@which docker-compose || (echo "$(RED)需要Docker Compose$(NC)" && exit 1)
	@echo "$(GREEN)>>> 所有依赖已满足$(NC)"
	@echo "$(BLUE)可用命令:$(NC)"
	@echo "  make docker-build    - 构建Docker镜像"
	@echo "  make docker-validate - 运行验证"
	@echo "  make docker-shell    - 进入开发shell"

##@ 项目维护

lint: ## 检查验证脚本语法
	@echo "$(GREEN)>>> 检查Python脚本...$(NC)"
	python3 -m py_compile .vscode/validate-project.py
	python3 -m py_compile .vscode/validate-cross-refs.py
	python3 -m py_compile .vscode/validate-mermaid.py
	@echo "$(GREEN)>>> 所有脚本语法正确$(NC)"

# Windows兼容规则（使用PowerShell）
ifeq ($(OS),Windows_NT)
    SHELL := powershell.exe
    SHELLFLAGS := -Command
    MKDIR := New-Item -ItemType Directory -Force
    RM := Remove-Item -Recurse -Force
else
    MKDIR := mkdir -p
    RM := rm -rf
endif
