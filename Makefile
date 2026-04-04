# =============================================================================
# AnalysisDataFlow Makefile
# 流计算理论模型与工程实践知识库 - 构建工具
# 版本: v2.0
# =============================================================================

# 配置变量
PYTHON := python3
PIP := pip3
OUTPUT_DIR := pdf-output
REPORTS_DIR := reports
INDEX_FILE := .vscode/search-index.json

# VSCode 脚本路径
EXPORT_SCRIPT := .vscode/export-to-pdf.py
VALIDATE_PROJECT_SCRIPT := .vscode/validate-project.py
VALIDATE_CROSSREFS_SCRIPT := .vscode/validate-cross-refs.py
VALIDATE_MERMAID_SCRIPT := .vscode/validate-mermaid.py
SEARCH_SCRIPT := .vscode/search.py
BUILD_INDEX_SCRIPT := .vscode/build-search-index.py
DOC_DIFF_SCRIPT := .vscode/doc-diff.py

# 颜色定义 (用于终端输出)
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
MAGENTA := \033[35m
RESET := \033[0m

# 默认目标
.DEFAULT_GOAL := help

# 检测操作系统
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    RM := rmdir /s /q
    MKDIR := mkdir
else
    DETECTED_OS := $(shell uname -s)
    RM := rm -rf
    MKDIR := mkdir -p
endif

# =============================================================================
# 帮助信息 (Help)
# =============================================================================

.PHONY: help
help: ## 显示所有可用命令
	@echo "$(BLUE)╔══════════════════════════════════════════════════════════════════╗$(RESET)"
	@echo "$(BLUE)║        AnalysisDataFlow 构建工具 - 可用命令列表                  ║$(RESET)"
	@echo "$(BLUE)╚══════════════════════════════════════════════════════════════════╝$(RESET)"
	@echo ""
	@echo "$(GREEN)验证命令:$(RESET)"
	@echo "  $(YELLOW)make validate$(RESET)              运行所有验证"
	@echo "  $(YELLOW)make validate-project$(RESET)      运行项目验证(定理/定义编号检查)"
	@echo "  $(YELLOW)make validate-crossrefs$(RESET)    运行交叉引用验证(链接检查)"
	@echo "  $(YELLOW)make validate-mermaid$(RESET)      运行Mermaid图表验证"
	@echo ""
	@echo "$(GREEN)文档差异分析命令:$(RESET)"
	@echo "  $(YELLOW)make doc-diff$(RESET)              分析暂存区的文档变更"
	@echo "  $(YELLOW)make doc-diff-base BASE=xxx$(RESET) 分析指定基准到HEAD的变更"
	@echo "  $(YELLOW)make doc-diff-pr BASE=main$(RESET) 分析PR的变更(用于CI/CD)"
	@echo ""
	@echo "$(GREEN)Docker命令:$(RESET)"
	@echo "  $(YELLOW)make docker-build$(RESET)        构建Docker镜像"
	@echo "  $(YELLOW)make docker-validate$(RESET)     在Docker中运行所有验证"
	@echo "  $(YELLOW)make docker-shell$(RESET)        进入Docker容器交互式shell"
	@echo "  $(YELLOW)make docker-clean$(RESET)        清理Docker容器和镜像"
	@echo ""
	@echo "$(GREEN)搜索命令:$(RESET)"
	@echo "  $(YELLOW)make search INDEX=xxx QUERY=xxx$(RESET)  搜索索引(需先构建索引)"
	@echo "  $(YELLOW)make build-index$(RESET)         构建搜索索引"
	@echo ""
	@echo "$(GREEN)PDF导出命令:$(RESET)"
	@echo "  $(YELLOW)make pdf-single FILE=xxx.md$(RESET)    导出单个文件为PDF"
	@echo "  $(YELLOW)make pdf-batch DIR=xxx$(RESET)         批量导出目录"
	@echo "  $(YELLOW)make pdf-full$(RESET)                  导出完整项目"
	@echo "  $(YELLOW)make pdf-merge FILES='f1 f2'$(RESET)   合并多个文件导出"
	@echo "  $(YELLOW)make pdf-struct$(RESET)                导出Struct目录"
	@echo "  $(YELLOW)make pdf-knowledge$(RESET)             导出Knowledge目录"
	@echo "  $(YELLOW)make pdf-flink$(RESET)                 导出Flink目录"
	@echo ""
	@echo "$(GREEN)统计命令:$(RESET)"
	@echo "  $(YELLOW)make stats$(RESET)               显示项目统计信息"
	@echo "  $(YELLOW)make count-docs$(RESET)          统计文档数量"
	@echo "  $(YELLOW)make count-theorems$(RESET)      统计定理/定义数量"
	@echo ""
	@echo "$(GREEN)维护命令:$(RESET)"
	@echo "  $(YELLOW)make update-index$(RESET)        更新所有索引(搜索索引+知识图谱)"
	@echo "  $(YELLOW)make check-links$(RESET)         检查文档中的死链"
	@echo "  $(YELLOW)make fix-numbers$(RESET)         修复定理/定义编号"
	@echo "  $(YELLOW)make update-progress$(RESET)     自动更新PROJECT-TRACKING.md进度"
	@echo "  $(YELLOW)make fix-links$(RESET)           修复文档链接问题"
	@echo ""
	@echo "$(GREEN)自动化工具集命令:$(RESET)"
	@echo "  $(YELLOW)make validate-theorems$(RESET)   验证定理编号连续性和唯一性"
	@echo "  $(YELLOW)make validate-mermaid$(RESET)    验证Mermaid图表语法(增强版)"
	@echo "  $(YELLOW)make health-check$(RESET)        运行项目健康检查仪表盘"
	@echo "  $(YELLOW)make check-consistency$(RESET)   检查文档一致性(术语/格式)"
	@echo "  $(YELLOW)make update-stats$(RESET)        更新STATISTICS-REPORT.md"
	@echo "  $(YELLOW)make all-checks$(RESET)          运行所有检查(完整套件)"
	@echo "  $(YELLOW)make automation-help$(RESET)     显示自动化工具集详细帮助"
	@echo ""
	@echo "$(GREEN)环境命令:$(RESET)"
	@echo "  $(YELLOW)make install-deps$(RESET)        安装Python依赖"
	@echo "  $(YELLOW)make check$(RESET)               检查PDF导出环境"
	@echo "  $(YELLOW)make clean$(RESET)               清理生成的PDF文件"
	@echo "  $(YELLOW)make clean-all$(RESET)           清理所有生成文件"
	@echo ""
	@echo "$(GREEN)示例:$(RESET)"
	@echo "  make pdf-single FILE=README.md"
	@echo "  make pdf-batch DIR=Struct/"
	@echo "  make search QUERY='checkpoint'"
	@echo "  make docker-validate"

# =============================================================================
# 验证命令 (Validation)
# =============================================================================

.PHONY: validate
validate: ## 运行所有验证 (项目验证 + 交叉引用验证 + Mermaid验证)
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@echo "$(BLUE)  运行完整项目验证...$(RESET)"
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@$(MAKE) validate-project
	@echo ""
	@$(MAKE) validate-crossrefs
	@echo ""
	@$(MAKE) validate-mermaid
	@echo ""
	@echo "$(GREEN)✅ 所有验证完成!$(RESET)"

.PHONY: validate-project
validate-project: ## 运行项目验证 (检查定理/定义编号规范性)
	@echo "$(BLUE)▶ 运行项目验证 (定理/定义编号检查)...$(RESET)"
	@if [ ! -f "$(VALIDATE_PROJECT_SCRIPT)" ]; then \
		echo "$(RED)错误: 验证脚本不存在: $(VALIDATE_PROJECT_SCRIPT)$(RESET)"; \
		exit 1; \
	fi
	@$(PYTHON) $(VALIDATE_PROJECT_SCRIPT) || { \
		echo "$(RED)❌ 项目验证失败$(RESET)"; \
		exit 1; \
	}
	@echo "$(GREEN)✅ 项目验证通过$(RESET)"

.PHONY: validate-crossrefs
validate-crossrefs: ## 运行交叉引用验证 (检查文档间链接)
	@echo "$(BLUE)▶ 运行交叉引用验证...$(RESET)"
	@if [ ! -f "$(VALIDATE_CROSSREFS_SCRIPT)" ]; then \
		echo "$(RED)错误: 验证脚本不存在: $(VALIDATE_CROSSREFS_SCRIPT)$(RESET)"; \
		exit 1; \
	fi
	@$(PYTHON) $(VALIDATE_CROSSREFS_SCRIPT) || { \
		echo "$(RED)❌ 交叉引用验证失败$(RESET)"; \
		exit 1; \
	}
	@echo "$(GREEN)✅ 交叉引用验证通过$(RESET)"

.PHONY: validate-mermaid
validate-mermaid: ## 运行Mermaid图表验证 (检查图表语法)
	@echo "$(BLUE)▶ 运行Mermaid图表验证...$(RESET)"
	@if [ ! -f "$(VALIDATE_MERMAID_SCRIPT)" ]; then \
		echo "$(RED)错误: 验证脚本不存在: $(VALIDATE_MERMAID_SCRIPT)$(RESET)"; \
		exit 1; \
	fi
	@$(PYTHON) $(VALIDATE_MERMAID_SCRIPT) || { \
		echo "$(RED)❌ Mermaid验证失败$(RESET)"; \
		exit 1; \
	}
	@echo "$(GREEN)✅ Mermaid验证通过$(RESET)"

# =============================================================================
# 文档差异分析命令 (Doc Diff)
# =============================================================================

.PHONY: doc-diff
doc-diff: ## 分析暂存区的文档变更
	@echo "$(BLUE)▶ 分析暂存区的文档变更...$(RESET)"
	@if [ ! -f "$(DOC_DIFF_SCRIPT)" ]; then \
		echo "$(RED)错误: 文档差异分析脚本不存在: $(DOC_DIFF_SCRIPT)$(RESET)"; \
		exit 1; \
	fi
	@$(PYTHON) $(DOC_DIFF_SCRIPT) --staged --no-impact || { \
		echo "$(RED)❌ 文档差异分析发现问题$(RESET)"; \
		exit 1; \
	}
	@echo "$(GREEN)✅ 文档差异分析完成$(RESET)"

.PHONY: doc-diff-base
doc-diff-base: ## 分析指定基准到HEAD的变更 (用法: make doc-diff-base BASE=main)
	@echo "$(BLUE)▶ 分析从 $(BASE) 到 HEAD 的变更...$(RESET)"
	@if [ ! -f "$(DOC_DIFF_SCRIPT)" ]; then \
		echo "$(RED)错误: 文档差异分析脚本不存在: $(DOC_DIFF_SCRIPT)$(RESET)"; \
		exit 1; \
	fi
	@$(PYTHON) $(DOC_DIFF_SCRIPT) --base $(BASE) --head HEAD --no-impact || { \
		echo "$(RED)❌ 文档差异分析发现问题$(RESET)"; \
		exit 1; \
	}
	@echo "$(GREEN)✅ 文档差异分析完成$(RESET)"

.PHONY: doc-diff-pr
doc-diff-pr: ## 分析PR的变更 (用法: make doc-diff-pr BASE=main, 用于CI/CD)
	@echo "$(BLUE)▶ 分析PR变更 (基准: $(BASE))...$(RESET)"
	@if [ ! -f "$(DOC_DIFF_SCRIPT)" ]; then \
		echo "$(RED)错误: 文档差异分析脚本不存在: $(DOC_DIFF_SCRIPT)$(RESET)"; \
		exit 1; \
	fi
	@$(PYTHON) $(DOC_DIFF_SCRIPT) --base $(BASE) --head HEAD || { \
		echo "$(RED)❌ 文档差异分析发现严重问题，建议阻止合并$(RESET)"; \
		exit 1; \
	}
	@echo "$(GREEN)✅ PR文档差异分析通过$(RESET)"

# =============================================================================
# Docker命令 (Docker)
# =============================================================================

.PHONY: docker-build
docker-build: ## 构建Docker镜像
	@echo "$(BLUE)▶ 构建Docker镜像...$(RESET)"
	@docker-compose build || { \
		echo "$(RED)❌ Docker构建失败$(RESET)"; \
		echo "$(YELLOW)提示: 请确保Docker和Docker Compose已安装$(RESET)"; \
		exit 1; \
	}
	@echo "$(GREEN)✅ Docker镜像构建成功$(RESET)"

.PHONY: docker-validate
docker-validate: ## 在Docker中运行所有验证
	@echo "$(BLUE)▶ 在Docker中运行完整验证...$(RESET)"
	@docker-compose run --rm validate || { \
		echo "$(RED)❌ Docker验证失败$(RESET)"; \
		exit 1; \
	}
	@echo "$(GREEN)✅ Docker验证完成$(RESET)"

.PHONY: docker-shell
docker-shell: ## 进入Docker容器交互式shell
	@echo "$(BLUE)▶ 进入Docker容器...$(RESET)"
	@echo "$(YELLOW)提示: 输入 'exit' 退出容器$(RESET)"
	@docker-compose run --rm shell

.PHONY: docker-clean
docker-clean: ## 清理Docker容器和镜像
	@echo "$(YELLOW)▶ 清理Docker资源...$(RESET)"
	@docker-compose down -v 2>/dev/null || true
	@docker rmi analysisdataflow_validate 2>/dev/null || true
	@echo "$(GREEN)✅ Docker资源已清理$(RESET)"

# =============================================================================
# 搜索命令 (Search)
# =============================================================================

.PHONY: search
search: ## 搜索索引 (用法: make search QUERY='关键词')
	@if [ ! -f "$(INDEX_FILE)" ]; then \
		echo "$(RED)错误: 搜索索引不存在$(RESET)"; \
		echo "$(YELLOW)请先运行: make build-index$(RESET)"; \
		exit 1; \
	fi
	@if [ -z "$(QUERY)" ]; then \
		echo "$(RED)错误: 请指定 QUERY 参数$(RESET)"; \
		echo "用法: make search QUERY='checkpoint'"; \
		echo "      make search QUERY='Thm-S-17-01'"; \
		echo "      make search QUERY='watermark' --highlight"; \
		exit 1; \
	fi
	@echo "$(BLUE)▶ 搜索: $(QUERY)$(RESET)"
	@$(PYTHON) $(SEARCH_SCRIPT) "$(QUERY)" $(if $(HIGHLIGHT),--highlight,) || { \
		echo "$(RED)❌ 搜索失败$(RESET)"; \
		exit 1; \
	}

.PHONY: build-index
build-index: ## 构建搜索索引
	@echo "$(BLUE)▶ 构建搜索索引...$(RESET)"
	@if [ ! -f "$(BUILD_INDEX_SCRIPT)" ]; then \
		echo "$(RED)错误: 索引构建脚本不存在$(RESET)"; \
		exit 1; \
	fi
	@$(PYTHON) $(BUILD_INDEX_SCRIPT) $(if $(VERBOSE),--verbose,) || { \
		echo "$(RED)❌ 索引构建失败$(RESET)"; \
		exit 1; \
	}
	@echo "$(GREEN)✅ 搜索索引构建完成: $(INDEX_FILE)$(RESET)"

# =============================================================================
# PDF导出命令 (PDF Export)
# =============================================================================

.PHONY: pdf-single
pdf-single: ## 导出单个文件为PDF (用法: make pdf-single FILE=xxx.md)
	@if [ -z "$(FILE)" ]; then \
		echo "$(RED)错误: 请指定 FILE 参数$(RESET)"; \
		echo "用法: make pdf-single FILE=README.md"; \
		exit 1; \
	fi
	@if [ ! -f "$(FILE)" ]; then \
		echo "$(RED)错误: 文件不存在: $(FILE)$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BLUE)▶ 导出单个文件: $(FILE)$(RESET)"
	@$(PYTHON) $(EXPORT_SCRIPT) single "$(FILE)" || { \
		echo "$(RED)❌ PDF导出失败$(RESET)"; \
		exit 1; \
	}

.PHONY: pdf-batch
pdf-batch: ## 批量导出目录为PDF (用法: make pdf-batch DIR=xxx)
	@if [ -z "$(DIR)" ]; then \
		echo "$(RED)错误: 请指定 DIR 参数$(RESET)"; \
		echo "用法: make pdf-batch DIR=Struct/"; \
		exit 1; \
	fi
	@if [ ! -d "$(DIR)" ]; then \
		echo "$(RED)错误: 目录不存在: $(DIR)$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BLUE)▶ 批量导出目录: $(DIR)$(RESET)"
	@$(PYTHON) $(EXPORT_SCRIPT) batch "$(DIR)" || { \
		echo "$(RED)❌ 批量导出失败$(RESET)"; \
		exit 1; \
	}

.PHONY: pdf-full
pdf-full: ## 导出完整项目所有文档为PDF
	@echo "$(BLUE)▶ 导出完整项目...$(RESET)"
	@$(PYTHON) $(EXPORT_SCRIPT) full || { \
		echo "$(RED)❌ 完整导出失败$(RESET)"; \
		exit 1; \
	}
	@echo "$(GREEN)✅ 导出完成! 输出目录: $(OUTPUT_DIR)/$(RESET)"

.PHONY: pdf-merge
pdf-merge: ## 合并多个文件导出 (用法: make pdf-merge FILES='f1.md f2.md' OUT=merged.pdf)
	@if [ -z "$(FILES)" ]; then \
		echo "$(RED)错误: 请指定 FILES 参数$(RESET)"; \
		echo "用法: make pdf-merge FILES='a.md b.md' OUT=output.pdf"; \
		exit 1; \
	fi
	@$(eval OUT_FILE := $(if $(OUT),$(OUT),merged.pdf))
	@echo "$(BLUE)▶ 合并导出到: $(OUT_FILE)$(RESET)"
	@$(PYTHON) $(EXPORT_SCRIPT) merge $(FILES) -o "$(OUT_FILE)" || { \
		echo "$(RED)❌ 合并导出失败$(RESET)"; \
		exit 1; \
	}

.PHONY: pdf-struct
pdf-struct: ## 导出Struct目录为PDF
	@echo "$(BLUE)▶ 导出Struct目录...$(RESET)"
	@$(PYTHON) $(EXPORT_SCRIPT) batch Struct/ -o $(OUTPUT_DIR)/Struct/ || { \
		echo "$(RED)❌ Struct导出失败$(RESET)"; \
		exit 1; \
	}

.PHONY: pdf-knowledge
pdf-knowledge: ## 导出Knowledge目录为PDF
	@echo "$(BLUE)▶ 导出Knowledge目录...$(RESET)"
	@$(PYTHON) $(EXPORT_SCRIPT) batch Knowledge/ -o $(OUTPUT_DIR)/Knowledge/ || { \
		echo "$(RED)❌ Knowledge导出失败$(RESET)"; \
		exit 1; \
	}

.PHONY: pdf-flink
pdf-flink: ## 导出Flink目录为PDF
	@echo "$(BLUE)▶ 导出Flink目录...$(RESET)"
	@$(PYTHON) $(EXPORT_SCRIPT) batch Flink/ -o $(OUTPUT_DIR)/Flink/ || { \
		echo "$(RED)❌ Flink导出失败$(RESET)"; \
		exit 1; \
	}

.PHONY: pdf-readme
pdf-readme: ## 快速导出README.md为PDF
	@echo "$(BLUE)▶ 导出README.md...$(RESET)"
	@$(PYTHON) $(EXPORT_SCRIPT) single README.md -o $(OUTPUT_DIR)/README.pdf || { \
		echo "$(RED)❌ README导出失败$(RESET)"; \
		exit 1; \
	}

# =============================================================================
# 统计命令 (Statistics)
# =============================================================================

.PHONY: stats
stats: ## 显示项目统计信息
	@echo "$(BLUE)╔════════════════════════════════════════════════╗$(RESET)"
	@echo "$(BLUE)║           AnalysisDataFlow 项目统计            ║$(RESET)"
	@echo "$(BLUE)╚════════════════════════════════════════════════╝$(RESET)"
	@echo ""
	@$(MAKE) count-docs
	@echo ""
	@$(MAKE) count-theorems
	@echo ""
	@echo "$(MAGENTA)📊 其他统计:$(RESET)"
	@echo "  PDF输出目录: $(OUTPUT_DIR)/"
	@if [ -d "$(OUTPUT_DIR)" ]; then \
		count=$$(find $(OUTPUT_DIR) -name "*.pdf" 2>/dev/null | wc -l); \
		echo "  PDF文件数量: $$count"; \
	else \
		echo "  PDF文件数量: 0 (未生成)"; \
	fi
	@if [ -f "$(INDEX_FILE)" ]; then \
		doc_count=$$(python3 -c "import json; print(len(json.load(open('$(INDEX_FILE)'))['documents']))" 2>/dev/null || echo "未知"); \
		echo "  索引文档数量: $$doc_count"; \
	fi

.PHONY: count-docs
count-docs: ## 统计文档数量
	@echo "$(MAGENTA)📝 文档统计:$(RESET)"
	@struct_count=$$(find Struct -name "*.md" 2>/dev/null | wc -l); \
	knowledge_count=$$(find Knowledge -name "*.md" 2>/dev/null | wc -l); \
	flink_count=$$(find Flink -name "*.md" 2>/dev/null | wc -l); \
	root_count=$$(find . -maxdepth 1 -name "*.md" 2>/dev/null | wc -l); \
	total=$$((struct_count + knowledge_count + flink_count)); \
	echo "  Struct/:   $$struct_count 篇"; \
	echo "  Knowledge/: $$knowledge_count 篇"; \
	echo "  Flink/:    $$flink_count 篇"; \
	echo "  根目录:    $$root_count 篇"; \
	echo "  $(GREEN)总计: $$total 篇$(RESET)"

.PHONY: count-theorems
count-theorems: ## 统计定理/定义数量
	@echo "$(MAGENTA)📐 形式化元素统计:$(RESET)"
	@if [ -f "THEOREM-REGISTRY.md" ]; then \
		thm_count=$$(grep -c "^| \`Thm-" THEOREM-REGISTRY.md 2>/dev/null || echo 0); \
		def_count=$$(grep -c "^| \`Def-" THEOREM-REGISTRY.md 2>/dev/null || echo 0); \
		lemma_count=$$(grep -c "^| \`Lemma-" THEOREM-REGISTRY.md 2>/dev/null || echo 0); \
		prop_count=$$(grep -c "^| \`Prop-" THEOREM-REGISTRY.md 2>/dev/null || echo 0); \
		cor_count=$$(grep -c "^| \`Cor-" THEOREM-REGISTRY.md 2>/dev/null || echo 0); \
		total=$$((thm_count + def_count + lemma_count + prop_count + cor_count)); \
		echo "  定理(Thm):    $$thm_count"; \
		echo "  定义(Def):    $$def_count"; \
		echo "  引理(Lemma):  $$lemma_count"; \
		echo "  命题(Prop):   $$prop_count"; \
		echo "  推论(Cor):    $$cor_count"; \
		echo "  $(GREEN)总计: $$total 个形式化元素$(RESET)"; \
	else \
		echo "  $(YELLOW)未找到 THEOREM-REGISTRY.md$(RESET)"; \
	fi

# =============================================================================
# 维护命令 (Maintenance)
# =============================================================================

.PHONY: update-index
update-index: ## 更新所有索引 (搜索索引 + 知识图谱)
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@echo "$(BLUE)  更新项目索引...$(RESET)"
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@echo ""
	@echo "$(BLUE)▶ 1. 构建搜索索引...$(RESET)"
	@$(MAKE) build-index
	@echo ""
	@echo "$(BLUE)▶ 2. 构建知识图谱...$(RESET)"
	@if [ -f ".vscode/build-knowledge-graph.py" ]; then \
		$(PYTHON) .vscode/build-knowledge-graph.py || echo "$(YELLOW)警告: 知识图谱构建失败$(RESET)"; \
	else \
		echo "$(YELLOW)提示: 知识图谱脚本不存在$(RESET)"; \
	fi
	@echo ""
	@echo "$(GREEN)✅ 索引更新完成!$(RESET)"

.PHONY: check-links
check-links: ## 检查文档中的死链 (通过交叉引用验证)
	@echo "$(BLUE)▶ 检查文档链接...$(RESET)"
	@$(MAKE) validate-crossrefs

.PHONY: fix-numbers
fix-numbers: ## 修复定理/定义编号 (通过项目验证报告)
	@echo "$(BLUE)▶ 检查并修复定理/定义编号...$(RESET)"
	@echo "$(YELLOW)提示: 此功能需要手动检查验证报告$(RESET)"
	@$(MAKE) validate-project
	@echo ""
	@echo "$(YELLOW)请查看上述验证报告，手动修复编号问题$(RESET)"

# =============================================================================
# 环境和依赖 (Environment)
# =============================================================================

.PHONY: install-deps
install-deps: ## 安装Python依赖
	@echo "$(BLUE)▶ 安装Python依赖...$(RESET)"
	@$(PIP) install pyyaml 2>/dev/null || pip install pyyaml
	@echo "$(GREEN)✅ Python依赖安装完成$(RESET)"
	@echo "$(YELLOW)请手动安装以下工具:$(RESET)"
	@echo "  1. Pandoc: https://pandoc.org/installing.html"
	@echo "  2. TeX Live: https://tug.org/texlive/"
	@echo "  3. Mermaid CLI (可选): npm install -g @mermaid-js/mermaid-cli"

.PHONY: check
check: ## 检查PDF导出环境
	@echo "$(BLUE)▶ 检查PDF导出环境...$(RESET)"
	@if [ ! -f "$(EXPORT_SCRIPT)" ]; then \
		echo "$(RED)错误: 导出脚本不存在$(RESET)"; \
		exit 1; \
	fi
	@$(PYTHON) $(EXPORT_SCRIPT) check || { \
		echo "$(YELLOW)环境检查完成，部分依赖可能缺失$(RESET)"; \
	}

# =============================================================================
# 清理命令 (Cleanup)
# =============================================================================

.PHONY: clean
clean: ## 清理生成的PDF文件
	@echo "$(YELLOW)▶ 清理PDF输出目录...$(RESET)"
	@if [ -d "$(OUTPUT_DIR)" ]; then \
		rm -rf $(OUTPUT_DIR)/*; \
		echo "$(GREEN)✅ 已清理 $(OUTPUT_DIR)/$(RESET)"; \
	else \
		echo "$(YELLOW)目录不存在: $(OUTPUT_DIR)$(RESET)"; \
	fi

.PHONY: clean-all
clean-all: clean ## 清理所有生成文件 (包括临时文件)
	@echo "$(YELLOW)▶ 清理临时文件...$(RESET)"
	@find . -type f -name "*.aux" -delete 2>/dev/null || true
	@find . -type f -name "*.log" -delete 2>/dev/null || true
	@find . -type f -name "*.out" -delete 2>/dev/null || true
	@find . -type f -name "*.toc" -delete 2>/dev/null || true
	@find . -type f -name "*.synctex.gz" -delete 2>/dev/null || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@if [ -d "$(REPORTS_DIR)" ]; then \
		rm -rf $(REPORTS_DIR)/*; \
		echo "  已清理 $(REPORTS_DIR)/"; \
	fi
	@echo "$(GREEN)✅ 清理完成$(RESET)"

# =============================================================================
# CI/CD 报告生成 (Reports)
# =============================================================================

.PHONY: ci-reports
ci-reports: ## 生成CI/CD验证报告 (JSON格式)
	@echo "$(BLUE)▶ 生成CI/CD验证报告...$(RESET)"
	@$(MKDIR) $(REPORTS_DIR)
	@$(PYTHON) $(VALIDATE_PROJECT_SCRIPT) --json > $(REPORTS_DIR)/validation-report.json 2>&1 || true
	@$(PYTHON) $(VALIDATE_CROSSREFS_SCRIPT) --json > $(REPORTS_DIR)/cross-ref-report.json 2>&1 || true
	@$(PYTHON) $(VALIDATE_MERMAID_SCRIPT) --json > $(REPORTS_DIR)/mermaid-report.json 2>&1 || true
	@echo "$(GREEN)✅ 报告已保存到 $(REPORTS_DIR)/$(RESET)"

# =============================================================================
# 快捷命令 (Shortcuts)
# =============================================================================

.PHONY: pdf-index
pdf-index: ## 导出所有INDEX文件为PDF
	@echo "$(BLUE)▶ 导出索引文件...$(RESET)"
	@for file in */00-INDEX.md; do \
		if [ -f "$$file" ]; then \
			dir=$$(dirname "$$file"); \
			echo "  导出: $$file"; \
			$(PYTHON) $(EXPORT_SCRIPT) single "$$file" -o "$(OUTPUT_DIR)/$$dir-INDEX.pdf" 2>/dev/null || true; \
		fi \
	done
	@echo "$(GREEN)✅ 索引文件导出完成$(RESET)"

.PHONY: quick-validate
quick-validate: ## 快速验证 (仅检查关键文件)
	@echo "$(BLUE)▶ 快速验证关键文件...$(RESET)"
	@echo "$(YELLOW)检查文件:$(RESET)"
	@for file in README.md AGENTS.md PROJECT-TRACKING.md THEOREM-REGISTRY.md; do \
		if [ -f "$$file" ]; then \
			echo "  $(GREEN)✓$$file$(RESET)"; \
		else \
			echo "  $(RED)✗$$file$(RESET)"; \
		fi \
	done
	@$(MAKE) count-docs

# =============================================================================
# Windows 兼容命令 (Windows Compatibility)
# =============================================================================

.PHONY: pdf-single-win
pdf-single-win: ## Windows: 导出单个文件 (用法: set FILE=xxx.md && make pdf-single-win)
	@if not defined FILE ( \
		echo "$(RED)错误: 请设置 FILE 环境变量$(RESET)" & \
		echo "用法: set FILE=README.md ^&^& make pdf-single-win" & \
		exit /b 1 \
	)
	@python $(EXPORT_SCRIPT) single %FILE%

.PHONY: pdf-batch-win
pdf-batch-win: ## Windows: 批量导出目录 (用法: set DIR=xxx && make pdf-batch-win)
	@if not defined DIR ( \
		echo "$(RED)错误: 请设置 DIR 环境变量$(RESET)" & \
		echo "用法: set DIR=Struct/ ^&^& make pdf-batch-win" & \
		exit /b 1 \
	)
	@python $(EXPORT_SCRIPT) batch %DIR%

# =============================================================================
# 版本信息 (Version)
# =============================================================================

.PHONY: version
version: ## 显示Makefile版本信息
	@echo "$(BLUE)AnalysisDataFlow Makefile$(RESET)"
	@echo "版本: v2.0"
	@echo "操作系统: $(DETECTED_OS)"
	@echo "Python: $(PYTHON)"
	@echo "输出目录: $(OUTPUT_DIR)"

# =============================================================================
# 自动化工具集命令 (Automation Toolkit) - v1.0
# =============================================================================

# 脚本路径
SCRIPTS_DIR := .scripts
VALIDATE_THEOREMS_SCRIPT := $(SCRIPTS_DIR)/validate_theorem_numbers.py
VALIDATE_MERMAID_SCRIPT := $(SCRIPTS_DIR)/validate_mermaid.py
GENERATE_STATS_SCRIPT := $(SCRIPTS_DIR)/generate_stats_report.py
HEALTH_CHECK_SCRIPT := $(SCRIPTS_DIR)/health_check_dashboard.py
CHECK_CONSISTENCY_SCRIPT := $(SCRIPTS_DIR)/check_consistency.py
UPDATE_PROGRESS_SCRIPT := $(SCRIPTS_DIR)/update_progress.py

.PHONY: validate-theorems
validate-theorems: ## 验证定理编号连续性和唯一性
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@echo "$(BLUE)  验证定理编号...$(RESET)"
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@$(PYTHON) $(VALIDATE_THEOREMS_SCRIPT) --verbose || { \
		echo "$(RED)❌ 定理编号验证失败$(RESET)"; \
		exit 1; \
	}
	@echo "$(GREEN)✅ 定理编号验证通过$(RESET)"

.PHONY: validate-mermaid
validate-mermaid: ## 验证Mermaid图表语法
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@echo "$(BLUE)  验证Mermaid图表语法...$(RESET)"
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@$(PYTHON) $(VALIDATE_MERMAID_SCRIPT) || { \
		echo "$(RED)❌ Mermaid验证失败$(RESET)"; \
		exit 1; \
	}
	@echo "$(GREEN)✅ Mermaid验证通过$(RESET)"

.PHONY: stats
current-stats: ## 生成并显示项目统计报告
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@echo "$(BLUE)  生成项目统计报告...$(RESET)"
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@$(PYTHON) $(GENERATE_STATS_SCRIPT)

.PHONY: update-stats
update-stats: ## 更新STATISTICS-REPORT.md
	@echo "$(BLUE)▶ 更新统计报告文件...$(RESET)"
	@$(PYTHON) $(GENERATE_STATS_SCRIPT) --update
	@echo "$(GREEN)✅ STATISTICS-REPORT.md 已更新$(RESET)"

.PHONY: health-check
health-check: ## 运行项目健康检查仪表盘
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@echo "$(BLUE)  运行项目健康检查...$(RESET)"
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@$(PYTHON) $(HEALTH_CHECK_SCRIPT) --save || { \
		echo "$(YELLOW)⚠️  健康检查发现问题$(RESET)"; \
	}

.PHONY: health-check-json
health-check-json: ## 输出健康检查JSON报告
	@$(PYTHON) $(HEALTH_CHECK_SCRIPT) --json

.PHONY: check-consistency
check-consistency: ## 检查文档一致性（术语、格式等）
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@echo "$(BLUE)  检查文档一致性...$(RESET)"
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@$(PYTHON) $(CHECK_CONSISTENCY_SCRIPT) || { \
		echo "$(YELLOW)⚠️  一致性检查发现问题$(RESET)"; \
	}

.PHONY: fix-links
fix-links: ## 修复文档链接问题
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@echo "$(BLUE)  修复文档链接...$(RESET)"
	@echo "$(BLUE)════════════════════════════════════════════════$(RESET)"
	@if [ -f "$(SCRIPTS_DIR)/fix_all_cross_refs.py" ]; then \
		$(PYTHON) $(SCRIPTS_DIR)/fix_all_cross_refs.py; \
	else \
		$(PYTHON) $(SCRIPTS_DIR)/fix_cross_refs.py 2>/dev/null || \
		echo "$(YELLOW)提示: 链接修复脚本不存在$(RESET)"; \
	fi

.PHONY: update-progress
update-progress: ## 自动更新PROJECT-TRACKING.md进度
	@echo "$(BLUE)▶ 更新项目进度...$(RESET)"
	@$(PYTHON) $(UPDATE_PROGRESS_SCRIPT) --auto --update-file
	@echo "$(GREEN)✅ 进度已更新$(RESET)"

.PHONY: all-checks
all-checks: ## 运行所有检查（验证+健康检查+一致性）
	@echo "$(BLUE)╔══════════════════════════════════════════════════════════════════╗$(RESET)"
	@echo "$(BLUE)║           运行完整项目检查套件                                  ║$(RESET)"
	@echo "$(BLUE)╚══════════════════════════════════════════════════════════════════╝$(RESET)"
	@echo ""
	@echo "$(MAGENTA)▶ 步骤 1/6: 验证定理编号$(RESET)"
	@$(MAKE) validate-theorems || true
	@echo ""
	@echo "$(MAGENTA)▶ 步骤 2/6: 验证Mermaid语法$(RESET)"
	@$(MAKE) validate-mermaid || true
	@echo ""
	@echo "$(MAGENTA)▶ 步骤 3/6: 验证交叉引用$(RESET)"
	@$(MAKE) validate-crossrefs || true
	@echo ""
	@echo "$(MAGENTA)▶ 步骤 4/6: 项目健康检查$(RESET)"
	@$(MAKE) health-check || true
	@echo ""
	@echo "$(MAGENTA)▶ 步骤 5/6: 文档一致性检查$(RESET)"
	@$(MAKE) check-consistency || true
	@echo ""
	@echo "$(MAGENTA)▶ 步骤 6/6: 生成统计报告$(RESET)"
	@$(MAKE) current-stats || true
	@echo ""
	@echo "$(GREEN)╔══════════════════════════════════════════════════════════════════╗$(RESET)"
	@echo "$(GREEN)║           所有检查完成!                                         ║$(RESET)"
	@echo "$(GREEN)╚══════════════════════════════════════════════════════════════════╝$(RESET)"

.PHONY: automation-help
automation-help: ## 显示自动化工具集帮助
	@echo "$(BLUE)╔══════════════════════════════════════════════════════════════════╗$(RESET)"
	@echo "$(BLUE)║        AnalysisDataFlow 自动化工具集 - 可用命令                  ║$(RESET)"
	@echo "$(BLUE)╚══════════════════════════════════════════════════════════════════╝$(RESET)"
	@echo ""
	@echo "$(GREEN)验证命令:$(RESET)"
	@echo "  $(YELLOW)make validate-theorems$(RESET)     验证定理编号连续性和唯一性"
	@echo "  $(YELLOW)make validate-mermaid$(RESET)      验证Mermaid图表语法"
	@echo "  $(YELLOW)make validate-crossrefs$(RESET)    验证交叉引用链接"
	@echo "  $(YELLOW)make check-consistency$(RESET)     检查文档一致性"
	@echo ""
	@echo "$(GREEN)统计与报告:$(RESET)"
	@echo "  $(YELLOW)make current-stats$(RESET)         显示项目统计摘要"
	@echo "  $(YELLOW)make update-stats$(RESET)          更新STATISTICS-REPORT.md"
	@echo "  $(YELLOW)make health-check$(RESET)          运行项目健康检查仪表盘"
	@echo "  $(YELLOW)make health-check-json$(RESET)     输出JSON格式健康报告"
	@echo ""
	@echo "$(GREEN)维护命令:$(RESET)"
	@echo "  $(YELLOW)make update-progress$(RESET)       自动更新PROJECT-TRACKING.md进度"
	@echo "  $(YELLOW)make fix-links$(RESET)             修复文档链接问题"
	@echo ""
	@echo "$(GREEN)综合命令:$(RESET)"
	@echo "  $(YELLOW)make all-checks$(RESET)            运行所有检查（完整套件）"
	@echo "  $(YELLOW)make automation-help$(RESET)       显示本帮助信息"
	@echo ""
