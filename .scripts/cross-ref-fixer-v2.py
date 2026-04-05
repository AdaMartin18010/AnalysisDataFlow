#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用修复脚本 v2
系统性修复所有剩余交叉引用错误
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class CrossRefFixer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.fix_log = []
        self.files_modified = set()
        
    def load_report(self):
        """加载验证报告"""
        report_path = self.base_dir / '.stats/cross_ref_report_v2.json'
        with open(report_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def fix_file_content(self, file_path, replacements):
        """修复文件内容"""
        full_path = self.base_dir / file_path
        if not full_path.exists():
            print(f"文件不存在: {file_path}")
            return False
            
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            for old, new in replacements:
                content = content.replace(old, new)
            
            if content != original_content:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.files_modified.add(file_path)
                return True
            return False
        except Exception as e:
            print(f"修复文件 {file_path} 时出错: {e}")
            return False
    
    def fix_i18n_en_docs(self):
        """修复英文翻译文档中的链接"""
        print("\n[1/5] 修复英文翻译文档链接...")
        
        # docs/i18n/en/QUICK-START.md - 修复相对路径
        quick_start_fixes = [
            ('[Struct/00-INDEX.md](./Struct/00-INDEX.md)', '[Struct/00-INDEX.md](../../../Struct/00-INDEX.md)'),
            ('[Knowledge/00-INDEX.md](./Knowledge/00-INDEX.md)', '[Knowledge/00-INDEX.md](../../../Knowledge/00-INDEX.md)'),
            ('[Flink/00-INDEX.md](./Flink/00-INDEX.md)', '[Flink/00-INDEX.md](../../../Flink/00.md)'),
            ('[THEOREM-REGISTRY.md](./THEOREM-REGISTRY.md)', '[THEOREM-REGISTRY.md](../../../THEOREM-REGISTRY.md)'),
            ('[PROJECT-TRACKING.md](./PROJECT-TRACKING.md)', '[PROJECT-TRACKING.md](../../../PROJECT-TRACKING.md)'),
            ('[AGENTS.md](./AGENTS.md)', '[AGENTS.md](../../../AGENTS.md)'),
        ]
        
        if self.fix_file_content('docs/i18n/en/QUICK-START.md', quick_start_fixes):
            print("  ✓ 修复 docs/i18n/en/QUICK-START.md")
            self.fix_log.append({
                'file': 'docs/i18n/en/QUICK-START.md',
                'type': 'relative_path',
                'fixes': len(quick_start_fixes)
            })
        
        # docs/i18n/en/README.md
        readme_fixes = [
            ('[knowledge-graph.html](knowledge-graph.html)', '[knowledge-graph.html](../../../knowledge-graph.html)'),
            ('[PROJECT-VERSION-TRACKING.md](./PROJECT-VERSION-TRACKING.md)', '[PROJECT-VERSION-TRACKING.md](../../../PROJECT-VERSION-TRACKING.md)'),
            ('[ROADMAP-v3.3-and-beyond.md](./ROADMAP-v3.3-and-beyond.md)', '[ROADMAP-v3.3-and-beyond.md](../../../ROADMAP-v3.3-and-beyond.md)'),
            ('[Apache License 2.0](./LICENSE)', '[Apache License 2.0](../../../LICENSE)'),
            ('[LICENSE](./LICENSE)', '[LICENSE](../../../LICENSE)'),
            ('[LICENSE-NOTICE.md](./LICENSE-NOTICE.md)', '[LICENSE-NOTICE.md](../../../LICENSE-NOTICE.md)'),
            ('[THIRD-PARTY-NOTICES.md](./THIRD-PARTY-NOTICES.md)', '[THIRD-PARTY-NOTICES.md](../../../THIRD-PARTY-NOTICES.md)'),
        ]
        
        if self.fix_file_content('docs/i18n/en/README.md', readme_fixes):
            print("  ✓ 修复 docs/i18n/en/README.md")
            self.fix_log.append({
                'file': 'docs/i18n/en/README.md',
                'type': 'relative_path',
                'fixes': len(readme_fixes)
            })
        
        # docs/i18n/en/ARCHITECTURE.md
        arch_fixes = [
            ('[docs/i18n/ARCHITECTURE.md](../i18n/ARCHITECTURE.md)', '[docs/i18n/ARCHITECTURE.md](../ARCHITECTURE.md)'),
            ('[AGENTS.md](../../AGENTS.md)', '[AGENTS.md](../../../AGENTS.md)'),
            ('[PROJECT-TRACKING.md](../../PROJECT-TRACKING.md)', '[PROJECT-TRACKING.md](../../../PROJECT-TRACKING.md)'),
            ('[THEOREM-REGISTRY.md](../../THEOREM-REGISTRY.md)', '[THEOREM-REGISTRY.md](../../../THEOREM-REGISTRY.md)'),
            ('[README.md](../../README.md)', '[README.md](../../../README.md)'),
        ]
        
        if self.fix_file_content('docs/i18n/en/ARCHITECTURE.md', arch_fixes):
            print("  ✓ 修复 docs/i18n/en/ARCHITECTURE.md")
            self.fix_log.append({
                'file': 'docs/i18n/en/ARCHITECTURE.md',
                'type': 'relative_path',
                'fixes': len(arch_fixes)
            })
    
    def fix_docs_chatbot(self):
        """修复 docs/chatbot-integration.md"""
        print("\n[2/5] 修复 docs/chatbot-integration.md...")
        fixes = [
            ('[Checkpoint Mechanism Deep Dive](Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md)',
             '[Checkpoint Mechanism Deep Dive](../../Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md)'),
        ]
        
        if self.fix_file_content('docs/chatbot-integration.md', fixes):
            print("  ✓ 修复 docs/chatbot-integration.md")
            self.fix_log.append({
                'file': 'docs/chatbot-integration.md',
                'type': 'relative_path',
                'fixes': len(fixes)
            })
    
    def fix_flink_rust_ecosystem(self):
        """修复 Flink/14-rust-assembly-ecosystem/ 目录下的文件"""
        print("\n[3/5] 修复 Flink Rust 生态系统文档...")
        
        # flink-rust-ecosystem-trends-2026.md
        fixes1 = [
            ('[Flink WASM UDF 生态](./flink-wasm-udf-ecosystem.md)', '[Flink WASM UDF 生态](../flink-wasm-udf-ecosystem.md)'),
            ('[Flink 2.x 路线图](../08-roadmap/flink-2x-roadmap-analysis.md)', '[Flink 2.x 路线图](../../08-roadmap/flink-2x-roadmap-analysis.md)'),
        ]
        if self.fix_file_content('Flink/14-rust-assembly-ecosystem/flink-rust-ecosystem-trends-2026.md', fixes1):
            print("  ✓ 修复 flink-rust-ecosystem-trends-2026.md")
            self.fix_log.append({'file': 'Flink/14-rust-assembly-ecosystem/flink-rust-ecosystem-trends-2026.md', 'type': 'relative_path', 'fixes': 2})
        
        # iron-functions-complete-guide.md
        fixes2 = [
            ('[Flink/14-rust-assembly-ecosystem/rust-ud](../14-rust-assembly-ecosystem/rust-udf-development-guide.md)',
             '[Flink/14-rust-assembly-ecosystem/rust-udf](../rust-udf-development-guide.md)'),
            ('[Flink/04-datastream-api/flink-wasm-integ](../../Flink/04-datastream-api/flink-wasm-integration.md)',
             '[Flink/04-datastream-api/flink-wasm-integ](../../../04-datastream-api/flink-wasm-integration.md)'),
        ]
        if self.fix_file_content('Flink/14-rust-assembly-ecosystem/iron-functions-complete-guide.md', fixes2):
            print("  ✓ 修复 iron-functions-complete-guide.md")
            self.fix_log.append({'file': 'Flink/14-rust-assembly-ecosystem/iron-functions-complete-guide.md', 'type': 'relative_path', 'fixes': 2})
        
        # trends/01-flink-rust-ecosystem-trends-2026.md
        fixes3 = [
            ('[14.0-rust-assembly-overview](../14.0-rust-assembly-overview.md)', '[14.0-rust-assembly-overview](../../14.0-rust-assembly-overview.md)'),
            ('[12.1-flink-rust-connector-adoption](../12-flink-connectors/12.1-flink-rust-connector-adoption.md)', '[12.1-flink-rust-connector-adoption](../../12-flink-connectors/12.1-flink-rust-connector-adoption.md)'),
        ]
        if self.fix_file_content('Flink/14-rust-assembly-ecosystem/trends/01-flink-rust-ecosystem-trends-2026.md', fixes3):
            print("  ✓ 修复 trends/01-flink-rust-ecosystem-trends-2026.md")
            self.fix_log.append({'file': 'Flink/14-rust-assembly-ecosystem/trends/01-flink-rust-ecosystem-trends-2026.md', 'type': 'relative_path', 'fixes': 2})
        
        # arroyo-update/01-arroyo-cloudflare-acquisition.md
        fixes4 = [
            ('[13.1-dataflow-model.md](../13-alternatives-comparison/13.1-dataflow-model.md)', '[13.1-dataflow-model.md](../../13-alternatives-comparison/13.1-dataflow-model.md)'),
            ('[14.1-risingwave-comparison.md](../14-rust-assembly-ecosystem/risingwave-comparison/14.1-risingwave-comparison.md)',
             '[14.1-risingwave-comparison.md](../risingwave-comparison/14.1-risingwave-comparison.md)'),
        ]
        if self.fix_file_content('Flink/14-rust-assembly-ecosystem/arroyo-update/01-arroyo-cloudflare-acquisition.md', fixes4):
            print("  ✓ 修复 arroyo-update/01-arroyo-cloudflare-acquisition.md")
            self.fix_log.append({'file': 'Flink/14-rust-assembly-ecosystem/arroyo-update/01-arroyo-cloudflare-acquisition.md', 'type': 'relative_path', 'fixes': 2})
        
        # comparison/01-rust-streaming-engines-comparison.md
        fixes5 = [
            ('[Flink 架构文档](../01-architecture/)', '[Flink 架构文档](../../01-architecture/)'),
            ('[Dataflow 模型理论](../../Struct/)', '[Dataflow 模型理论](../../../Struct/)'),
        ]
        if self.fix_file_content('Flink/14-rust-assembly-ecosystem/comparison/01-rust-streaming-engines-comparison.md', fixes5):
            print("  ✓ 修复 comparison/01-rust-streaming-engines-comparison.md")
            self.fix_log.append({'file': 'Flink/14-rust-assembly-ecosystem/comparison/01-rust-streaming-engines-comparison.md', 'type': 'relative_path', 'fixes': 2})
        
        # heterogeneous-computing/01-gpu-udf-cuda.md
        fixes6 = [
            ('[Flink UDF 基础](../../05-udfs/)', '[Flink UDF 基础](../../../05-udfs/)'),
            ('[Rust FFI 绑定](../02-rust-ffi-bindings/)', '[Rust FFI 绑定](../../02-rust-ffi-bindings/)'),
        ]
        if self.fix_file_content('Flink/14-rust-assembly-ecosystem/heterogeneous-computing/01-gpu-udf-cuda.md', fixes6):
            print("  ✓ 修复 heterogeneous-computing/01-gpu-udf-cuda.md")
            self.fix_log.append({'file': 'Flink/14-rust-assembly-ecosystem/heterogeneous-computing/01-gpu-udf-cuda.md', 'type': 'relative_path', 'fixes': 2})
        
        # iron-functions/01-iron-functions-complete-guide.md
        fixes7 = [
            ('[Flink DataStream API](../05-datastream-api/README.md)', '[Flink DataStream API](../../../05-datastream-api/README.md)'),
            ('[Flink Table/SQL API](../06-table-sql-api/README.md)', '[Flink Table/SQL API](../../../06-table-sql-api/README.md)'),
        ]
        if self.fix_file_content('Flink/14-rust-assembly-ecosystem/iron-functions/01-iron-functions-complete-guide.md', fixes7):
            print("  ✓ 修复 iron-functions/01-iron-functions-complete-guide.md")
            self.fix_log.append({'file': 'Flink/14-rust-assembly-ecosystem/iron-functions/01-iron-functions-complete-guide.md', 'type': 'relative_path', 'fixes': 2})
        
        # wasi-0.3-async/01-wasi-0.3-spec-guide.md
        fixes8 = [
            ('[WebAssembly Component Model](../12-component-model/01-component-model-basics.md)', '[WebAssembly Component Model](../../12-component-model/01-component-model-basics.md)'),
            ('[WASI 0.2 接口规范](../../09-flink-deployment/03-cloud-native/02-wasi-integration.md)', '[WASI 0.2 接口规范](../../../09-flink-deployment/03-cloud-native/02-wasi-integration.md)'),
        ]
        if self.fix_file_content('Flink/14-rust-assembly-ecosystem/wasi-0.3-async/01-wasi-0.3-spec-guide.md', fixes8):
            print("  ✓ 修复 wasi-0.3-async/01-wasi-0.3-spec-guide.md")
            self.fix_log.append({'file': 'Flink/14-rust-assembly-ecosystem/wasi-0.3-async/01-wasi-0.3-spec-guide.md', 'type': 'relative_path', 'fixes': 2})
        
        # ai-native-streaming/01-ai-native-architecture.md
        fixes9 = [
            ('[FLIP-531 AI Agents](../../flink-ai-agents/flip-531-ai-agents.md)', '[FLIP-531 AI Agents](../../../12-ai-ml/flink-ai-agents/flip-531-ai-agents.md)'),
        ]
        if self.fix_file_content('Flink/14-rust-assembly-ecosystem/ai-native-streaming/01-ai-native-architecture.md', fixes9):
            print("  ✓ 修复 ai-native-streaming/01-ai-native-architecture.md")
            self.fix_log.append({'file': 'Flink/14-rust-assembly-ecosystem/ai-native-streaming/01-ai-native-architecture.md', 'type': 'relative_path', 'fixes': 1})
        
        # flash-engine/01-flash-architecture.md
        fixes10 = [
            ('[Apache Flink 架构基础](../../01-core-concepts/)', '[Apache Flink 架构基础](../../../01-architecture/)'),
        ]
        if self.fix_file_content('Flink/14-rust-assembly-ecosystem/flash-engine/01-flash-architecture.md', fixes10):
            print("  ✓ 修复 flash-engine/01-flash-architecture.md")
            self.fix_log.append({'file': 'Flink/14-rust-assembly-ecosystem/flash-engine/01-flash-architecture.md', 'type': 'relative_path', 'fixes': 1})
        
        # flash-engine/03-forstdb-storage.md
        fixes11 = [
            ('[Flink 状态后端](../../04-state-management/)', '[Flink 状态后端](../../../06-state-management/)'),
        ]
        if self.fix_file_content('Flink/14-rust-assembly-ecosystem/flash-engine/03-forstdb-storage.md', fixes11):
            print("  ✓ 修复 flash-engine/03-forstdb-storage.md")
            self.fix_log.append({'file': 'Flink/14-rust-assembly-ecosystem/flash-engine/03-forstdb-storage.md', 'type': 'relative_path', 'fixes': 1})
        
        # risingwave-comparison/04-risingwave-rust-udf-guide.md
        fixes12 = [
            ('[Flink WASM UDF 指南](../../11-connectors/udfs/13-wasm-udf-deep-dive.md)', '[Flink WASM UDF 指南](../../../13-wasm/13-wasm-udf-deep-dive.md)'),
        ]
        if self.fix_file_content('Flink/14-rust-assembly-ecosystem/risingwave-comparison/04-risingwave-rust-udf-guide.md', fixes12):
            print("  ✓ 修复 risingwave-comparison/04-risingwave-rust-udf-guide.md")
            self.fix_log.append({'file': 'Flink/14-rust-assembly-ecosystem/risingwave-comparison/04-risingwave-rust-udf-guide.md', 'type': 'relative_path', 'fixes': 1})
        
        # wasm-3.0/01-wasm-3.0-spec-guide.md
        fixes13 = [
            ('[Rust WebAssembly 基础](../../02-flink-rust-core/06-wasm-udfs.md)', '[Rust WebAssembly 基础](../../02-rust-core/06-wasm-udfs.md)'),
        ]
        if self.fix_file_content('Flink/14-rust-assembly-ecosystem/wasm-3.0/01-wasm-3.0-spec-guide.md', fixes13):
            print("  ✓ 修复 wasm-3.0/01-wasm-3.0-spec-guide.md")
            self.fix_log.append({'file': 'Flink/14-rust-assembly-ecosystem/wasm-3.0/01-wasm-3.0-spec-guide.md', 'type': 'relative_path', 'fixes': 1})
    
    def fix_flink_ecosystem(self):
        """修复 Flink/ecosystem/ 目录"""
        print("\n[4/5] 修复 Flink 生态系统文档...")
        
        # materialize-comparison.md
        fixes1 = [
            ('[RisingWave Deep Dive](../Knowledge/06-frontier/risingwave-deep-dive.md)', '[RisingWave Deep Dive](../../Knowledge/06-frontier/risingwave-deep-dive.md)'),
            ('[Streaming Databases Guide](../Knowledge/06-frontier/streaming-databases.md)', '[Streaming Databases Guide](../../Knowledge/06-frontier/streaming-databases.md)'),
        ]
        if self.fix_file_content('Flink/ecosystem/materialize-comparison.md', fixes1):
            print("  ✓ 修复 materialize-comparison.md")
            self.fix_log.append({'file': 'Flink/ecosystem/materialize-comparison.md', 'type': 'relative_path', 'fixes': 2})
        
        # pulsar-functions-integration.md
        fixes2 = [
            ('[Flink Connectors Overview](./04-connectors/00-INDEX.md)', '[Flink Connectors Overview](../04-connectors/00.md)'),
        ]
        if self.fix_file_content('Flink/pulsar-functions-integration.md', fixes2):
            print("  ✓ 修复 pulsar-functions-integration.md")
            self.fix_log.append({'file': 'Flink/pulsar-functions-integration.md', 'type': 'relative_path', 'fixes': 1})
        
        # risingwave-integration-guide.md
        fixes3 = [
            ('[Knowledge: Flink vs RisingWave](../Knowledge/04-technology-selection/flink-vs-risingwave.md)', '[Knowledge: Flink vs RisingWave](../../Knowledge/04-technology-selection/flink-vs-risingwave.md)'),
        ]
        if self.fix_file_content('Flink/ecosystem/risingwave-integration-guide.md', fixes3):
            print("  ✓ 修复 risingwave-integration-guide.md")
            self.fix_log.append({'file': 'Flink/ecosystem/risingwave-integration-guide.md', 'type': 'relative_path', 'fixes': 1})
    
    def fix_anchor_errors(self):
        """修复锚点错误"""
        print("\n[5/5] 修复锚点错误...")
        
        report = self.load_report()
        anchor_errors = report['errors_by_category']['anchor_not_found']
        
        # 过滤出真实锚点错误并按文件分组
        real_errors = [e for e in anchor_errors 
                      if not e['source'].startswith('.scripts/') 
                      and not e['source'].startswith('reports/')]
        
        # 常见锚点问题映射
        common_anchor_fixes = {
            '#ci-cd-集成': '#cicd-集成',
            '#5-形式证明--工程论证': '#5-形式证明--工程论证-proof--engineering-argument',
            '#5-形式证明--工程论证-proof--engineering-argument': '#5-形式证明--工程论证-proof--engineering-argument',
            '#表-71-模型-×-性质-×-可判定性矩阵': '#表71-模型--性质--可判定性矩阵',
            '#关系-1-choreographic-⊃-传统数据流': '#关系-1-choreographic--传统数据流',
            '#33-actor--dataflow-双层架构关系': '#33-actor--dataflow-双层架构',
            '#业务模式-日志分析与监控-business-pattern-log-analysis--monitoring': '#业务模式-日志分析与监控',
        }
        
        # 按文件分组
        by_file = defaultdict(list)
        for err in real_errors:
            by_file[err['source']].append(err)
        
        fixed_count = 0
        for file_path, errors in by_file.items():
            replacements = []
            for err in errors:
                anchor = err.get('anchor', '')
                url = err.get('url', '')
                text = err.get('text', '')
                
                # 尝试找到修复方案
                if url in common_anchor_fixes:
                    new_url = common_anchor_fixes[url]
                    old_link = f'[{text}]({url})'
                    new_link = f'[{text}]({new_url})'
                    replacements.append((old_link, new_link))
            
            if replacements:
                if self.fix_file_content(file_path, replacements):
                    print(f"  ✓ 修复 {file_path}: {len(replacements)}个锚点")
                    self.fix_log.append({
                        'file': file_path,
                        'type': 'anchor',
                        'fixes': len(replacements)
                    })
                    fixed_count += len(replacements)
        
        print(f"  共修复 {fixed_count} 个锚点错误")
        return fixed_count
    
    def generate_log(self):
        """生成修复日志"""
        log_content = f"""# P0-1 交叉引用修复日志

> 修复时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 修复脚本: `.scripts/cross-ref-fixer-v2.py`

## 修复统计

| 指标 | 数值 |
|------|------|
| 修改文件数 | {len(self.files_modified)} |
| 修复条目数 | {sum(f['fixes'] for f in self.fix_log)} |

## 修复详情

### 按文件统计

| 文件 | 修复类型 | 修复数量 |
|------|----------|----------|
"""
        
        for entry in self.fix_log:
            log_content += f"| {entry['file']} | {entry['type']} | {entry['fixes']} |\n"
        
        log_content += """
## 修复类型说明

- **relative_path**: 修复相对路径错误（如 `./Struct/` → `../../../Struct/`）
- **anchor**: 修复锚点链接错误（如 `#ci-cd-集成` → `#cicd-集成`）

## 主要修复类别

### 1. 英文翻译文档 (docs/i18n/en/)
修复了指向根目录文件的相对路径，将 `./` 路径修正为 `../../../` 多层相对路径。

### 2. Flink Rust 生态系统 (Flink/14-rust-assembly-ecosystem/)
修复了子目录中文件之间的交叉引用，修正了 `../` 和 `../../` 路径层级。

### 3. Flink 生态对比 (Flink/ecosystem/)
修复了指向 Knowledge/ 目录的跨目录链接。

### 4. 锚点链接
修复了六段式模板中常见的锚点格式问题。

---
*由 cross-ref-fixer-v2.py 自动生成*
"""
        
        log_path = self.base_dir / 'P0-1-CROSS-REF-FIX-LOG.md'
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(log_content)
        
        print(f"\n修复日志已保存到: {log_path}")
        return log_path
    
    def run(self):
        """运行所有修复"""
        print("="*70)
        print("交叉引用修复脚本 v2")
        print("="*70)
        
        self.fix_i18n_en_docs()
        self.fix_docs_chatbot()
        self.fix_flink_rust_ecosystem()
        self.fix_flink_ecosystem()
        self.fix_anchor_errors()
        
        print("\n" + "="*70)
        print(f"修复完成！修改了 {len(self.files_modified)} 个文件")
        print("="*70)
        
        self.generate_log()
        
        return len(self.files_modified)

def main():
    base_dir = Path(__file__).parent.parent
    fixer = CrossRefFixer(base_dir)
    return fixer.run()

if __name__ == '__main__':
    exit(main())
