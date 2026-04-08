# AnalysisDataFlow AI Assistant Makefile
# AI辅助文档生成工具集成

.PHONY: help summarize translate comments cross-ref ai-analysis clean

# 工具路径
PYTHON := python
SUMMARIZER := $(PYTHON) doc-summarizer.py
TRANSLATOR := $(PYTHON) auto-translator.py
COMMENTER := $(PYTHON) code-comment-generator.py
REF_SUGGESTER := $(PYTHON) cross-ref-suggester.py

# 输出目录
OUTPUT_DIR := output
LOGS_DIR := logs

help:
	@echo "AnalysisDataFlow AI Assistant"
	@echo ""
	@echo "可用目标:"
	@echo "  make summarize     - 生成所有文档摘要"
	@echo "  make translate     - 翻译所有文档为英文"
	@echo "  make comments      - 为代码添加注释"
	@echo "  make cross-ref     - 生成交叉引用报告"
	@echo "  make ai-analysis   - 运行所有分析"
	@echo "  make clean         - 清理输出文件"
	@echo ""
	@echo "单个文件处理示例:"
	@echo "  $(SUMMARIZER) Struct/00-INDEX.md --stdout"
	@echo "  $(TRANSLATOR) README.md -t en"

# 生成所有文档摘要
summarize: $(OUTPUT_DIR)
	@echo "=== 生成 Struct/ 文档摘要 ==="
	-$(SUMMARIZER) ../../Struct/ --batch -o $(OUTPUT_DIR) 2>&1 | tee $(LOGS_DIR)/summarize-struct.log
	@echo "=== 生成 Knowledge/ 文档摘要 ==="
	-$(SUMMARIZER) ../../Knowledge/ --batch -o $(OUTPUT_DIR) 2>&1 | tee $(LOGS_DIR)/summarize-knowledge.log
	@echo "=== 生成 Flink/ 文档摘要 ==="
	-$(SUMMARIZER) ../../Flink/ --batch -o $(OUTPUT_DIR) 2>&1 | tee $(LOGS_DIR)/summarize-flink.log
	@echo "✅ 摘要生成完成，输出到 $(OUTPUT_DIR)/"

# 翻译所有文档
translate: $(OUTPUT_DIR)
	@echo "=== 翻译 Struct/ 文档 ==="
	-$(TRANSLATOR) ../../Struct/ --batch -t en -o $(OUTPUT_DIR)/translations 2>&1 | tee $(LOGS_DIR)/translate.log
	@echo "✅ 翻译完成"

# 代码注释生成
comments: $(OUTPUT_DIR)
	@echo "=== 为脚本添加注释 ==="
	-$(COMMENTER) ../../scripts/ --batch --inline 2>&1 | tee $(LOGS_DIR)/comments.log
	@echo "✅ 注释生成完成"

# 交叉引用分析
cross-ref: $(OUTPUT_DIR)
	@echo "=== 生成交叉引用报告 ==="
	-$(REF_SUGGESTER) ../.. -o $(OUTPUT_DIR)/cross-ref-report.md --json $(OUTPUT_DIR)/cross-ref.json 2>&1 | tee $(LOGS_DIR)/cross-ref.log
	@echo "✅ 交叉引用报告生成完成"

# 一键运行所有分析
ai-analysis: clean summarize cross-ref
	@echo ""
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║           AI 分析完成!                                      ║"
	@echo "╠════════════════════════════════════════════════════════════╣"
	@echo "║  摘要文件: $(OUTPUT_DIR)/*.summary.md                      ║"
	@echo "║  交叉引用: $(OUTPUT_DIR)/cross-ref-report.md               ║"
	@echo "║  日志文件: $(LOGS_DIR)/*.log                               ║"
	@echo "╚════════════════════════════════════════════════════════════╝"

# 创建输出目录
$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR) $(LOGS_DIR)

# 清理输出
clean:
	rm -rf $(OUTPUT_DIR)/* $(LOGS_DIR)/*
	@echo "✅ 已清理输出文件"

# 测试单个工具
test-summarizer:
	$(SUMMARIZER) ../../Struct/00-INDEX.md --stdout

test-translator:
	$(TRANSLATOR) ../../README.md --stdout -t en | head -50

test-cross-ref:
	$(REF_SUGGESTER) ../../Struct/ -o $(OUTPUT_DIR)/test-cross-ref.md
