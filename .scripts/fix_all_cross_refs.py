#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面交叉引用修复脚本
修复所有文件不存在和锚点不存在错误
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

class ComprehensiveCrossRefFixer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.fixes_applied = []
        self.fixes_skipped = []
        self.file_set = set()
        self.dir_set = set()
        self.load_file_index()
        
    def load_file_index(self):
        """加载所有文件索引"""
        for item in self.base_dir.rglob('*'):
            if '.git' in item.parts:
                continue
            if item.is_file() and item.suffix == '.md':
                rel_path = item.relative_to(self.base_dir)
                self.file_set.add(str(rel_path).replace('\\', '/'))
            elif item.is_dir():
                rel_path = item.relative_to(self.base_dir)
                self.dir_set.add(str(rel_path).replace('\\', '/'))
        print(f"已加载 {len(self.file_set)} 个Markdown文件")
        
    def read_file(self, filepath):
        """读取文件内容"""
        full_path = self.base_dir / filepath
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"读取文件 {filepath} 失败: {e}")
            return None
    
    def write_file(self, filepath, content):
        """写入文件内容"""
        full_path = self.base_dir / filepath
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"写入文件 {filepath} 失败: {e}")
            return False

    # ========== 修复策略1: 修复截断的链接 ==========
    def fix_truncated_links(self):
        """修复截断的链接（如 .m) 应为 .md)）"""
        fixes = [
            # (文件路径, 旧链接, 新链接)
            ("LEARNING-PATHS/data-engineer-path.md", 
             "[Flink/02-core-mechanisms/state-backend-selection.m](../Flink/02-core-mechanisms/state-backend-selection.md)",
             "[Flink/02-core-mechanisms/state-backend-selection.md](../Flink/02-core-mechanisms/state-backend-selection.md)"),
            ("visuals/selection-tree-consistency.md",
             "[Struct/02-properties/02.02-consistency-hierarchy.m](../../Struct/02-properties/02.02-consistency-hierarchy.md)",
             "[Struct/02-properties/02.02-consistency-hierarchy.md](../../Struct/02-properties/02.02-consistency-hierarchy.md)"),
            ("visuals/selection-tree-consistency.md",
             "[Flink/02-core-mechanisms/exactly-once-end-to-end.m](../../Flink/02-core-mechanisms/exactly-once-end-to-end.md)",
             "[Flink/02-core-mechanisms/exactly-once-end-to-end.md](../../Flink/02-core-mechanisms/exactly-once-end-to-end.md)"),
            ("Knowledge/06-frontier/materialize-comparison-guide.md",
             "[../../Struct/03-stateful/stateful-computing-founda](../../Struct/03-stateful/stateful-computing-foundations.md)",
             "[../../Struct/03-stateful/stateful-computing-foundations.md](../../Struct/03-stateful/stateful-computing-foundations.md)"),
        ]
        
        for filepath, old_link, new_link in fixes:
            content = self.read_file(filepath)
            if content and old_link in content:
                content = content.replace(old_link, new_link)
                if self.write_file(filepath, content):
                    self.fixes_applied.append({
                        'file': filepath,
                        'type': 'truncated_link',
                        'old': old_link,
                        'new': new_link
                    })
                    print(f"✓ 修复截断链接: {filepath}")

    # ========== 修复策略2: 修复LaTeX公式误识别 ==========
    def fix_latex_false_positives(self):
        """修复LaTeX公式被误识别为链接的问题"""
        # 这些是误报，实际上不是链接问题，而是LaTeX语法
        # 需要在验证脚本中排除，而不是修改文档
        print("ℹ LaTeX公式误报已在验证脚本中处理，无需修改文档")

    # ========== 修复策略3: 修复指向不存在文件的链接 ==========
    def fix_nonexistent_file_links(self):
        """修复指向不存在文件的链接"""
        fixes = [
            # Exercise文件链接修复 - 指向正确的位置
            ("Knowledge/98-exercises/exercise-01-process-calculus.md",
             "../Struct/01-foundations.md",
             "../Struct/01-foundation/01.01-unified-streaming-theory.md"),
            ("Knowledge/98-exercises/exercise-02-flink-basics.md",
             "../Flink/01-architecture-overview.md",
             "../Flink/01-architecture/flink-architecture-overview.md"),
            ("Knowledge/98-exercises/exercise-03-checkpoint-analysis.md",
             "../Flink/03-fault-tolerance.md",
             "../Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md"),
            ("Knowledge/98-exercises/exercise-04-consistency-models.md",
             "../Struct/02-consistency-models.md",
             "../Struct/02-properties/02.02-consistency-hierarchy.md"),
            ("Knowledge/98-exercises/exercise-06-tla-practice.md",
             "../Struct/02-consistency-models.md",
             "../Struct/02-properties/02.02-consistency-hierarchy.md"),
             
            # Migration guides 修复
            ("Knowledge/05-migrations/kafka-streams-to-flink-guide.md",
             "../Flink/03-api-layer/ds-core-abstraction.md",
             "../../Flink/02-core-mechanisms/flink-datastream-api-guide.md"),
            ("Knowledge/05-mapping-guides/migration-guides/05.1-spark-streaming-to-flink-migration.md",
             "../../Flink/03-api-layer/ds-core-abstraction.md",
             "../../../Flink/02-core-mechanisms/flink-datastream-api-guide.md"),
            ("Knowledge/05-mapping-guides/migration-guides/05.2-kafka-streams-to-flink-migration.md",
             "../../Flink/03-api-layer/connectors/kafka-connector.md",
             "../../../Flink/04-connectors/flink-connectors-ecosystem-complete-guide.md"),
            ("Knowledge/05-mapping-guides/migration-guides/05.3-storm-to-flink-migration.md",
             "../../Flink/02-core-mechanisms/jobgraph-execution-model.md",
             "../../../Flink/01-architecture/flink-jobgraph-execution-model.md"),
            ("Knowledge/05-mapping-guides/migration-guides/05.5-batch-to-streaming-migration.md",
             "../../Flink/03-api-layer/ds-core-abstraction.md",
             "../../../Flink/02-core-mechanisms/flink-datastream-api-guide.md"),
            ("Knowledge/05-mapping-guides/migration-guides/05.5-batch-to-streaming-migration.md",
             "../../Flink/02-core-mechanisms/time-semantics.md",
             "../../../Flink/02-core-mechanisms/time-semantics-and-watermark.md"),
             
            # Case studies 修复
            ("Knowledge/10-case-studies/ecommerce/10.2.3-big-promotion-realtime-dashboard.md",
             "../10.2.1-flink-production-deployment.md",
             "../../07-best-practices/flink-production-checklist.md"),
            ("Knowledge/10-case-studies/ecommerce/10.2.3-big-promotion-realtime-dashboard.md",
             "../10.2.2-realtime-warehouse-practice.md",
             "../../03-business-patterns/realtime-warehouse-patterns.md"),
            ("Knowledge/10-case-studies/gaming/10.5.2-anti-cheat-system.md",
             "../../05-flink-advanced/flink-2.4-wasm-udf.md",
             "../../../Flink/09-language-foundations/flink-25-wasm-udf-ga.md"),
            ("Knowledge/10-case-studies/social-media/10.4.2-realtime-recommendation-content.md",
             "../../../Flink/07-ai-integration/07.1-flink-ai-agents.md",
             "../../../Flink/12-ai-ml/flink-ai-agents-flip-531.md"),
             
            # Flink 文档修复
            ("Flink/03-sql-table-api/built-in-functions-complete-list.md",
             "../01-overview/flink-sql-overview.md",
             "../01-architecture/flink-sql-overview.md"),
            ("Flink/03-sql-table-api/data-types-complete-reference.md",
             "./01-architecture-overview.md",
             "../01-architecture/flink-architecture-overview.md"),
            ("Flink/04-connectors/elasticsearch-connector-complete-guide.md",
             "../02-api/02.01-datastream-api-basics.md",
             "../02-core-mechanisms/flink-datastream-api-guide.md"),
            ("Flink/04-connectors/elasticsearch-connector-complete-guide.md",
             "../03-core/03.02-checkpoint-mechanism.md",
             "../02-core-mechanisms/checkpoint-mechanism-deep-dive.md"),
            ("Flink/04-connectors/pulsar-integration-guide.md",
             "01-connector-basics.md",
             "flink-connectors-ecosystem-complete-guide.md"),
            ("Flink/04-connectors/pulsar-integration-guide.md",
             "03-01-state-management.md",
             "../02-core-mechanisms/flink-state-management-complete-guide.md"),
            ("Flink/05-operations/production-checklist.md",
             "../10-deployment/flink-deployment-guide.md",
             "../10-deployment/flink-kubernetes-deployment.md"),
            ("Flink/05-operations/production-checklist.md",
             "../15-observability/monitoring-setup.md",
             "../11-monitoring-observability/flink-monitoring-setup-guide.md"),
            ("Flink/07-case-studies/case-clickstream-user-behavior-analytics.md",
             "../05-ecosystem/",
             "../04-connectors/"),
            ("Flink/07-case-studies/case-ecommerce-realtime-recommendation.md",
             "../06-ml/",
             "../12-ai-ml/"),
            ("Flink/09-language-foundations/10-wasi-component-model.md",
             "../../13-wasm/wasm-streaming.md",
             "./flink-25-wasm-udf-ga.md"),
            ("Flink/09-language-foundations/10-wasi-component-model.md",
             "../03-rust-native.md",
             "./flink-rust-native-api-guide.md"),
            ("Flink/10-deployment/multi-cloud-deployment-templates.md",
             "./flink-kubernetes-deployment.md",
             "./flink-kubernetes-deployment-complete-guide.md"),
            ("Flink/10-deployment/multi-cloud-deployment-templates.md",
             "../01-architecture/flink-cluster-architecture.md",
             "../01-architecture/flink-architecture-overview.md"),
            ("Flink/11-benchmarking/performance-benchmarking-guide.md",
             "../04-mechanisms/",
             "../02-core-mechanisms/"),
            ("Flink/11-benchmarking/streaming-benchmarks.md",
             "../04-internals/README.md",
             "../00-INDEX.md"),
            ("Flink/12-ai-ml/flink-ai-agents-flip-531.md",
             "flink-llm-integration-guide.md",
             "flink-llm-integration.md"),
            ("Flink/12-ai-ml/flink-ai-agents-flip-531.md",
             "mcp-protocol-agent-streaming.md",
             "../06-frontier/mcp-protocol-agent-streaming.md"),
            ("Flink/12-ai-ml/flink-llm-integration.md",
             "../05-sql/flink-sql-advanced.md",
             "../03-sql-table-api/flink-sql-advanced-features.md"),
            ("Flink/12-ai-ml/flink-llm-integration.md",
             "./flink-ml-foundation.md",
             "./flink-ml-architecture.md"),
            ("Flink/12-ai-ml/flink-ml-architecture.md",
             "../01-core/flink-datastream-api.md",
             "../02-core-mechanisms/flink-datastream-api-guide.md"),
            ("Flink/12-ai-ml/flink-realtime-ml-inference.md",
             "../04-streaming-foundations/flink-async-io.md",
             "../02-core-mechanisms/async-io-mechanism.md"),
            ("Flink/12-ai-ml/flink-realtime-ml-inference.md",
             "../05-state-management/flink-state-management.md",
             "../02-core-mechanisms/flink-state-management-complete-guide.md"),
            ("Flink/12-ai-ml/model-serving-streaming.md",
             "../11-feature-engineering/feature-engineering-patterns.md",
             "./realtime-feature-engineering-feature-store.md"),
            ("Flink/12-ai-ml/rag-streaming-architecture.md",
             "../../03-sql-table-api/vector-search.md",
             "../03-sql-table-api/vector-search.md"),
            ("Flink/12-ai-ml/realtime-feature-engineering-feature-store.md",
             "../02-core-mechanisms/dual-stream-join.md",
             "../02-core-mechanisms/stream-join-mechanisms.md"),
            ("Flink/12-ai-ml/realtime-feature-engineering-feature-store.md",
             "../02-core-mechanisms/state-management.md",
             "../02-core-mechanisms/flink-state-management-complete-guide.md"),
            ("Flink/12-ai-ml/vector-database-integration.md",
             "./11.4-flink-ml-inference.md",
             "./flink-realtime-ml-inference.md"),
            ("Flink/12-ai-ml/vector-database-integration.md",
             "../04-connectors/04.1-jdbc-connector.md",
             "../04-connectors/jdbc-connector-guide.md"),
             
            # Security 文档修复
            ("Flink/13-security/flink-security-complete-guide.md",
             "../12-security/flink-security-architecture.md",
             "./flink-security-architecture.md"),
            ("Flink/13-security/spiffe-spire-integration-guide.md",
             "../12-security/flink-security-architecture.md",
             "./flink-security-architecture.md"),
            ("Flink/13-security/streaming-security-best-practices.md",
             "../11-security/flink-security-authorization.md",
             "./flink-security-authorization.md"),
            ("Flink/13-security/streaming-security-best-practices.md",
             "../12-security/flink-security-network-isolation.md",
             "./flink-security-network-isolation.md"),
            ("Flink/13-security/trusted-execution-flink.md",
             "../12-security/flink-security-architecture.md",
             "./flink-security-architecture.md"),
             
            # WASM 文档修复
            ("Flink/13-wasm/wasm-streaming.md",
             "../01-architecture/flink-architecture-overview.md",
             "../01-architecture/flink-cluster-architecture.md"),
            ("Flink/13-wasm/wasm-streaming.md",
             "../05-udf/flink-udf-extension.md",
             "../09-language-foundations/flink-udf-development-guide.md"),
             
            # Graph 文档修复
            ("Flink/14-graph/flink-gelly.md",
             "../06-dataset/flink-dataset-api.md",
             "../01-architecture/flink-batch-streaming-unified.md"),
            ("Flink/14-graph/flink-gelly.md",
             "../12-iteration/flink-iteration.md",
             "./flink-gelly-streaming-graph-processing.md"),
             
            # Observability 文档修复
            ("Flink/15-observability/distributed-tracing.md",
             "../08-state/checkpoint-mechanism.md",
             "../02-core-mechanisms/checkpoint-mechanism-deep-dive.md"),
            ("Flink/15-observability/distributed-tracing.md",
             "./backpressure-monitoring.md",
             "./flink-backpressure-monitoring.md"),
            ("Flink/15-observability/flink-opentelemetry-observability.md",
             "../13-checkpoint/flink-exactly-once-semantics.md",
             "../02-core-mechanisms/exactly-once-semantics.md"),
            ("Flink/15-observability/flink-opentelemetry-observability.md",
             "../10-architecture/flink-state-management.md",
             "../02-core-mechanisms/flink-state-management-complete-guide.md"),
            ("Flink/15-observability/metrics-and-monitoring.md",
             "../12-fault-tolerance/checkpoint-mechanism.md",
             "../02-core-mechanisms/checkpoint-mechanism-deep-dive.md"),
            ("Flink/15-observability/realtime-data-quality-monitoring.md",
             "../14-security/streaming-data-governance.md",
             "../../Knowledge/08-standards/streaming-data-governance.md"),
             
            # Knowledge 文档修复
            ("Knowledge/03-business-patterns/alibaba-double11-flink.md",
             "../../Flink/01-architecture/flink-24-performance-improvements.md",
             "../../Flink/06-engineering/flink-24-performance-improvements.md"),
            ("Knowledge/08-standards/streaming-security-compliance.md",
             "../../Flink/11-monitoring-observability/flink-security-audit-logging.md",
             "../../Flink/13-security/flink-security-audit-logging.md"),
             
            # Struct 文档修复
            ("Struct/04-proofs/04.05-type-safety-fg-fgg.md",
             "\bar{e}",
             None),  # LaTeX误报，不处理
            ("Struct/04-proofs/04.05-type-safety-fg-fgg.md",
             "\theta(\bar{e}",
             None),  # LaTeX误报，不处理
            ("Struct/04-proofs/04.05-type-safety-fg-fgg.md",
             "v_1, ...",
             None),  # LaTeX误报，不处理
        ]
        
        for filepath, old_url, new_url in fixes:
            if new_url is None:  # LaTeX误报，跳过
                continue
            content = self.read_file(filepath)
            if content and old_url in content:
                content = content.replace(old_url, new_url)
                if self.write_file(filepath, content):
                    self.fixes_applied.append({
                        'file': filepath,
                        'type': 'file_not_found',
                        'old': old_url,
                        'new': new_url
                    })
                    print(f"✓ 修复文件链接: {filepath}")

    # ========== 修复策略4: 修复Exercise答案文件链接 ==========
    def fix_exercise_answer_links(self):
        """修复练习文档中的答案文件链接"""
        # 这些答案文件不存在，需要将链接改为文本或创建占位符
        exercise_files = [
            "Knowledge/98-exercises/exercise-01-process-calculus.md",
            "Knowledge/98-exercises/exercise-02-flink-basics.md",
            "Knowledge/98-exercises/exercise-03-checkpoint-analysis.md",
            "Knowledge/98-exercises/exercise-04-consistency-models.md",
            "Knowledge/98-exercises/exercise-05-pattern-implementation.md",
            "Knowledge/98-exercises/exercise-06-tla-practice.md",
        ]
        
        for filepath in exercise_files:
            content = self.read_file(filepath)
            if not content:
                continue
                
            # 将答案文件链接改为文本（因为这些答案文件不存在）
            # 匹配模式: [text](./answers/xxx.md#anchor) -> **text**（稍后手动添加答案）
            patterns = [
                (r'\[([^\]]+)\]\(\./answers/([^)]+\.md)(?:#[^)]+)?\)', r'**\1**（答案待添加）'),
                (r'\[([^\]]+)\]\(\./answers/([^)]+\.(?:java|go|tla))\)', r'**\1**（代码示例待添加）'),
            ]
            
            modified = False
            for pattern, replacement in patterns:
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    modified = True
            
            if modified:
                if self.write_file(filepath, content):
                    self.fixes_applied.append({
                        'file': filepath,
                        'type': 'exercise_answer_link',
                        'note': '将答案链接改为文本'
                    })
                    print(f"✓ 修复练习答案链接: {filepath}")

    # ========== 修复策略5: 修复Exercise目录链接 ==========
    def fix_exercise_directory_links(self):
        """修复练习README中的目录链接"""
        filepath = "Knowledge/98-exercises/README.md"
        content = self.read_file(filepath)
        if not content:
            return
            
        fixes = [
            ("../Struct/", "../Struct/00-INDEX.md"),
            ("../Flink/", "../Flink/00-INDEX.md"),
        ]
        
        modified = False
        for old_link, new_link in fixes:
            if old_link in content:
                content = content.replace(old_link, new_link)
                modified = True
        
        if modified:
            if self.write_file(filepath, content):
                self.fixes_applied.append({
                    'file': filepath,
                    'type': 'directory_link',
                    'note': '将目录链接指向索引文件'
                })
                print(f"✓ 修复练习目录链接: {filepath}")

    # ========== 修复策略6: 修复锚点问题 ==========
    def fix_anchor_issues(self):
        """修复锚点不存在问题"""
        # 主要问题是特殊字符在锚点中的处理
        # 根据Markdown规范，中文锚点应该使用原始标题
        
        # 定义锚点映射: (文件, 错误锚点, 正确锚点)
        anchor_fixes = [
            # BENCHMARK-REPORT.md
            ("BENCHMARK-REPORT.md", "#5-形式证明--工程论证-proof--engineering-argument", "#5-形式证明--工程论证"),
            # THEOREM-REGISTRY.md - 这些是目录链接问题
            ("THEOREM-REGISTRY.md", "#2-定理注册表-thm-s-xx-xx--thm-k-xx-xx--thm-f-xx-xx", "#2-定理注册表"),
            ("THEOREM-REGISTRY.md", "#3-定义注册表-def-s-xx-xx--def-k-xx-xx--def-f-xx-xx", "#3-定义注册表"),
            ("THEOREM-REGISTRY.md", "#4-引理注册表-lemma-s-xx-xx--lemma-k-xx-xx--lemma-f-xx-xx", "#4-引理注册表"),
            ("THEOREM-REGISTRY.md", "#51-命题-prop-s-xx-xx--prop-k-xx-xx--prop-f-xx-xx", "#51-命题"),
            ("THEOREM-REGISTRY.md", "#52-推论-cor-s-xx-xx--cor-k-xx-xx--cor-f-xx-xx", "#52-推论"),
            # TROUBLESHOOTING-COMPLETE.md
            ("TROUBLESHOOTING-COMPLETE.md", "#关系-1-问题症状--根因映射", "#关系-1"),
            ("TROUBLESHOOTING-COMPLETE.md", "#关系-2-排查流程--故障恢复", "#关系-2"),
            ("TROUBLESHOOTING-COMPLETE.md", "#5-形式证明--工程论证-proof--engineering-argument", "#5-形式证明--工程论证"),
            # Flink/00-INDEX.md
            ("Flink/00-INDEX.md", "#7-跨引用索引flink--struct", "#7-跨引用索引"),
            # Knowledge/00-INDEX.md
            ("Knowledge/00-INDEX.md", "#41-领域--模式映射", "#41-领域--"),
            ("Knowledge/00-INDEX.md", "#107-web3与区块链流处理--new", "#107-web3与区块链流处理"),
            ("Knowledge/00-INDEX.md", "#108-data-mesh与实时数据产品--v23", "#108-data-mesh与实时数据产品"),
            # Visuals
            ("visuals/knowledge-pattern-relations.md", "#31-领域--模式矩阵", "#31-领域-"),
            ("visuals/matrix-patterns.md", "#21-核心业务需求--设计模式矩阵", "#21-核心业务需求-"),
            ("visuals/matrix-scenarios.md", "#完整业务场景--技术要素矩阵", "#"),
        ]
        
        for filepath, old_anchor, new_anchor in anchor_fixes:
            content = self.read_file(filepath)
            if content and old_anchor in content:
                content = content.replace(old_anchor, new_anchor)
                if self.write_file(filepath, content):
                    self.fixes_applied.append({
                        'file': filepath,
                        'type': 'anchor_fix',
                        'old': old_anchor,
                        'new': new_anchor
                    })
                    print(f"✓ 修复锚点: {filepath}")

    # ========== 修复策略7: 修复GitHub相关链接 ==========
    def fix_github_links(self):
        """修复GitHub相关链接"""
        # 这些是GitHub特有的链接，不需要修复（issues, discussions等）
        # 但在验证时会被标记为错误
        print("ℹ GitHub链接（issues, discussions等）是有效的外部链接，无需修复")

    # ========== 修复策略8: 修复docs/i18n链接 ==========
    def fix_docs_i18n_links(self):
        """修复docs/i18n目录中的链接"""
        filepath = "docs/i18n/README.md"
        content = self.read_file(filepath)
        if not content:
            return
            
        # 将脚本帮助链接改为文本
        old_link = "[工具帮助](.scripts/i18n-manager.py --help)"
        new_text = "**工具帮助**（运行 `.scripts/i18n-manager.py --help`）"
        
        if old_link in content:
            content = content.replace(old_link, new_text)
            if self.write_file(filepath, content):
                self.fixes_applied.append({
                    'file': filepath,
                    'type': 'script_link',
                    'old': old_link,
                    'new': new_text
                })
                print(f"✓ 修复脚本链接: {filepath}")

    # ========== 修复策略9: 修复.github反馈模板链接 ==========
    def fix_github_template_links(self):
        """修复GitHub模板中的链接"""
        # 这些链接指向GitHub的功能（issues/new/choose等）
        # 这些是有效的，不需要修复
        print("ℹ GitHub模板链接是有效的外部链接，无需修复")

    def run_all_fixes(self):
        """运行所有修复"""
        print("="*70)
        print("开始全面修复交叉引用错误")
        print("="*70)
        
        self.fix_truncated_links()
        self.fix_nonexistent_file_links()
        self.fix_exercise_answer_links()
        self.fix_exercise_directory_links()
        self.fix_anchor_issues()
        self.fix_docs_i18n_links()
        
        print("\n" + "="*70)
        print("修复完成统计")
        print("="*70)
        print(f"总修复数: {len(self.fixes_applied)}")
        
        if self.fixes_applied:
            print("\n修复详情:")
            for fix in self.fixes_applied:
                print(f"  - {fix['file']}: {fix.get('type', 'unknown')}")

def main():
    base_dir = Path(__file__).parent.parent
    fixer = ComprehensiveCrossRefFixer(base_dir)
    fixer.run_all_fixes()
    print("\n修复完成!")

if __name__ == '__main__':
    main()
