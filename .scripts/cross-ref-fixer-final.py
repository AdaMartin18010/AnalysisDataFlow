#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用最终修复脚本
处理所有剩余的复杂链接问题
"""

import os
import re
from pathlib import Path
from datetime import datetime

class FinalCrossRefFixer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.fix_log = []
        self.files_modified = set()
        
        # 文件映射：旧/无效路径 -> 有效路径
        self.file_mappings = {
            # Flink Rust 生态系统
            '../flink-wasm-udf-ecosystem.md': './flink-25-wasm-udf-ga.md',  # 重命名文件
            '../../08-roadmap/flink-2x-roadmap-analysis.md': '../../08-roadmap/flink-2.3-2.4-roadmap.md',
            
            # iron-functions-complete-guide.md
            '../14-rust-assembly-ecosystem/rust-udf-development-guide.md': './risingwave-rust-udf-native-guide.md',
            '../../Flink/04-datastream-api/flink-wasm-integration.md': '../../09-language-foundations/flink-25-wasm-udf-ga.md',
            
            # arroyo-update
            '../../13-alternatives-comparison/13.1-dataflow-model.md': '../../13-wasm/01-wasm-udf-frameworks.md',
            '../risingwave-comparison/14.1-risingwave-comparison.md': '../risingwave-comparison/01-risingwave-comparison-guide.md',
            
            # heterogeneous-computing
            '../../../05-udfs/': '../../05-datastream-api/',
            '../../02-rust-ffi-bindings/': '../../09-language-foundations/',
            
            # iron-functions
            '../../../05-datastream-api/README.md': '../../../05-datastream-api/flink-datastream-api-complete-guide.md',
            '../../../06-table-sql-api/README.md': '../../../03-sql-table-api/flink-table-sql-complete-guide.md',
            
            # trends
            '../../14.0-rust-assembly-overview.md': '../00-MASTER-INDEX.md',
            '../../12-flink-connectors/12.1-flink-rust-connector-adoption.md': '../../04-connectors/flink-connectors-ecosystem-complete-guide.md',
            
            # wasi-0.3-async
            '../../12-component-model/01-component-model-basics.md': '../../13-wasm/01-wasm-udf-frameworks.md',
            '../../../09-flink-deployment/03-cloud-native/02-wasi-integration.md': '../../../13-wasm/09-wasm-udf-frameworks.md',
            
            # ai-native-streaming
            '../../../12-ai-ml/flink-ai-agents/flip-531-ai-agents.md': '../../../12-ai-ml/flink-ai-ml-integration-guide.md',
            
            # flash-engine
            '../../../01-architecture/': '../../../01-architecture/flink-architecture-overview.md',
            '../../../06-state-management/': '../../../06-state-management/state-backends-deep-comparison.md',
            
            # risingwave-comparison
            '../../../13-wasm/13-wasm-udf-deep-dive.md': '../../../09-language-foundations/flink-25-wasm-udf-ga.md',
            
            # wasm-3.0
            '../../02-rust-core/06-wasm-udfs.md': '../../09-language-foundations/09-wasm-udf-frameworks.md',
            
            # docs/chatbot-integration.md
            '../../Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md': '../../Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md',  # 检查是否存在
            
            # pulsar-functions-integration.md
            '../04-connectors/00.md': '../04-connectors/flink-connectors-ecosystem-complete-guide.md',
            
            # version-tracking
            '../../.scripts/flink-release-tracker-v2.py': '../../.scripts/flink-release-tracker.py',
            
            # arroyo-update PROGRESS-TRACKING.md
            './IMPACT-ANALYSIS.md': './01-arroyo-cloudflare-acquisition.md',
            
            # iron-functions VERSION-TRACKING.md
            '../COMPATIBILITY-MATRIX.md': '../00-MASTER-INDEX.md',
            
            # docs/i18n/en/QUICK-START.md
            '../../../Flink/00.md': '../../../Flink/00.md',  # 保持不变，可能需要检查
        }
    
    def fix_file(self, file_path, custom_fixes=None):
        """修复单个文件"""
        full_path = self.base_dir / file_path
        if not full_path.exists():
            print(f"  ⚠ 文件不存在: {file_path}")
            return False
        
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            fixes_applied = []
            
            # 应用自定义修复
            if custom_fixes:
                for old, new in custom_fixes:
                    if old in content:
                        content = content.replace(old, new)
                        fixes_applied.append((old, new))
            
            # 应用通用映射
            for old_path, new_path in self.file_mappings.items():
                if old_path in content:
                    content = content.replace(old_path, new_path)
                    fixes_applied.append((old_path, new_path))
            
            if content != original_content:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.files_modified.add(file_path)
                print(f"  ✓ 修复 {file_path}: {len(fixes_applied)}个链接")
                self.fix_log.append({
                    'file': file_path,
                    'fixes': len(fixes_applied),
                    'details': fixes_applied
                })
                return True
            return False
            
        except Exception as e:
            print(f"  ✗ 修复 {file_path} 时出错: {e}")
            return False
    
    def run(self):
        """运行所有修复"""
        print("="*70)
        print("交叉引用最终修复")
        print("="*70)
        
        files_to_fix = [
            'Flink/14-rust-assembly-ecosystem/flink-rust-ecosystem-trends-2026.md',
            'Flink/14-rust-assembly-ecosystem/iron-functions-complete-guide.md',
            'Flink/14-rust-assembly-ecosystem/arroyo-update/01-arroyo-cloudflare-acquisition.md',
            'Flink/14-rust-assembly-ecosystem/heterogeneous-computing/01-gpu-udf-cuda.md',
            'Flink/14-rust-assembly-ecosystem/iron-functions/01-iron-functions-complete-guide.md',
            'Flink/14-rust-assembly-ecosystem/trends/01-flink-rust-ecosystem-trends-2026.md',
            'Flink/14-rust-assembly-ecosystem/wasi-0.3-async/01-wasi-0.3-spec-guide.md',
            'Flink/14-rust-assembly-ecosystem/ai-native-streaming/01-ai-native-architecture.md',
            'Flink/14-rust-assembly-ecosystem/flash-engine/01-flash-architecture.md',
            'Flink/14-rust-assembly-ecosystem/flash-engine/03-forstdb-storage.md',
            'Flink/14-rust-assembly-ecosystem/risingwave-comparison/04-risingwave-rust-udf-guide.md',
            'Flink/14-rust-assembly-ecosystem/wasm-3.0/01-wasm-3.0-spec-guide.md',
            'Flink/pulsar-functions-integration.md',
            'Flink/version-tracking/flink-26-27-roadmap.md',
            'Flink/14-rust-assembly-ecosystem/arroyo-update/PROGRESS-TRACKING.md',
            'Flink/14-rust-assembly-ecosystem/iron-functions/VERSION-TRACKING.md',
        ]
        
        for file_path in files_to_fix:
            self.fix_file(file_path)
        
        # 特殊处理 docs/chatbot-integration.md
        print("\n特殊处理 docs/chatbot-integration.md...")
        chatbot_fixes = [
            ('../../Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md', 
             '../Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md'),
        ]
        self.fix_file('docs/chatbot-integration.md', chatbot_fixes)
        
        # 特殊处理 docs/i18n/en/QUICK-START.md 中的 Flink 链接
        print("\n特殊处理 docs/i18n/en/QUICK-START.md...")
        quickstart_fixes = [
            ('[Flink/00-INDEX.md](../../../Flink/00.md)', '[Flink/](../Flink/)'),
        ]
        self.fix_file('docs/i18n/en/QUICK-START.md', quickstart_fixes)
        
        print("\n" + "="*70)
        print(f"修复完成！修改了 {len(self.files_modified)} 个文件")
        print("="*70)
        
        return len(self.files_modified)

def main():
    base_dir = Path(__file__).parent.parent
    fixer = FinalCrossRefFixer(base_dir)
    return fixer.run()

if __name__ == '__main__':
    exit(main())
