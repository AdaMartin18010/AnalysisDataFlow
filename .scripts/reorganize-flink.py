#!/usr/bin/env python3
"""
Flink 目录重组脚本
"""

import shutil
import os
from pathlib import Path
from typing import List, Tuple

# 配置
FLINK_DIR = Path('e:/_src/AnalysisDataFlow/Flink')
DRY_RUN = False  # 设置为True可以预览变更而不执行
# 注意: 下面会临时设为False来执行实际迁移

# 迁移映射: (源路径, 目标路径)
MIGRATIONS: List[Tuple[str, str]] = [
    # 元信息
    ('00-INDEX.md', '00-meta/00-INDEX.md'),
    ('00-QUICK-START.md', '00-meta/00-QUICK-START.md'),
    ('version-tracking.md', '00-meta/version-tracking.md'),
    ('version-tracking/', '00-meta/version-tracking/'),
    
    # 架构概念
    ('01-architecture/', '01-concepts/'),
    
    # 核心机制
    ('02-core-mechanisms/', '02-core/'),
    
    # API层
    ('03-sql-table-api/', '03-api/03.02-table-sql-api/'),
    ('09-language-foundations/', '03-api/09-language-foundations/'),
    
    # 运行时
    ('05-operations/', '04-runtime/04.02-operations/'),
    ('07-operations/', '04-runtime/04.02-operations/'),
    ('10-deployment/', '04-runtime/04.01-deployment/'),
    ('deployment/', '04-runtime/04.01-deployment/'),
    ('15-observability/', '04-runtime/04.03-observability/'),
    ('observability/', '04-runtime/04.03-observability/'),
    
    # 生态系统
    ('04-connectors/', '05-ecosystem/05.01-connectors/'),
    ('connectors/', '05-ecosystem/05.01-connectors/'),
    ('14-lakehouse/', '05-ecosystem/05.02-lakehouse/'),
    ('13-wasm/', '05-ecosystem/05.03-wasm-udf/'),
    ('14-graph/', '05-ecosystem/05.04-graph/'),
    ('ecosystem/', '05-ecosystem/ecosystem/'),
    
    # AI/ML
    ('12-ai-ml/', '06-ai-ml/'),
    ('ai-ml/', '06-ai-ml/ai-ml/'),
    
    # Rust原生
    ('14-rust-assembly-ecosystem/', '07-rust-native/'),
    
    # 路线图
    ('08-roadmap/', '08-roadmap/08.01-flink-24/'),
    ('flink-24/', '08-roadmap/08.01-flink-24/'),
    ('flink-25/', '08-roadmap/08.02-flink-25/'),
    ('flink-30/', '08-roadmap/08.03-flink-30/'),
    ('api-evolution/', '08-roadmap/08.04-feature-evolution/api-evolution/'),
    ('roadmap/', '08-roadmap/08.04-feature-evolution/roadmap/'),
    
    # 工程实践
    ('07-case-studies/', '09-practices/09.01-case-studies/'),
    ('11-benchmarking/', '09-practices/09.02-benchmarking/'),
    ('06-engineering/', '09-practices/09.03-performance-tuning/'),
    ('05-vs-competitors/', '09-practices/09.03-performance-tuning/05-vs-competitors/'),
    ('13-security/', '09-practices/09.04-security/'),
    ('security/', '09-practices/09.04-security/security/'),
]

def ensure_dir(path: Path):
    """确保目录存在"""
    if not DRY_RUN:
        path.parent.mkdir(parents=True, exist_ok=True)

def migrate_file(src: Path, dst: Path):
    """迁移文件"""
    if not src.exists():
        print(f"  ⚠️  源不存在: {src}")
        return False
    
    if dst.exists():
        print(f"  ⚠️  目标已存在: {dst}")
        return False
    
    ensure_dir(dst)
    
    if DRY_RUN:
        print(f"  [DRY-RUN] 移动: {src} -> {dst}")
    else:
        shutil.move(str(src), str(dst))
        print(f"  ✅ 移动: {src} -> {dst}")
    
    return True

def migrate_dir(src: Path, dst: Path):
    """迁移目录"""
    if not src.exists():
        print(f"  ⚠️  源不存在: {src}")
        return False
    
    if DRY_RUN:
        print(f"  [DRY-RUN] 移动目录: {src} -> {dst}")
        return True
    
    # 如果目标已存在，合并内容
    if dst.exists():
        print(f"  📁 合并到现有目录: {dst}")
        for item in src.iterdir():
            dst_item = dst / item.name
            if dst_item.exists():
                print(f"    ⚠️  跳过(已存在): {item.name}")
            else:
                shutil.move(str(item), str(dst_item))
                print(f"    ✅ 移动: {item.name}")
        # 删除空源目录
        if not any(src.iterdir()):
            src.rmdir()
    else:
        # 直接移动
        ensure_dir(dst.parent)
        shutil.move(str(src), str(dst))
        print(f"  ✅ 移动目录: {src} -> {dst}")
    
    return True

def main():
    print("=" * 60)
    print("Flink 目录重组")
    print("=" * 60)
    print(f"模式: {'预览(DRY-RUN)' if DRY_RUN else '实际执行'}")
    print(f"根目录: {FLINK_DIR}")
    print()
    
    os.chdir(FLINK_DIR)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for src_rel, dst_rel in MIGRATIONS:
        src = Path(src_rel)
        dst = Path(dst_rel)
        
        if not src.exists():
            print(f"⏭️  跳过(不存在): {src_rel}")
            skip_count += 1
            continue
        
        print(f"\n📦 {src_rel} -> {dst_rel}")
        
        try:
            if src.is_file():
                if migrate_file(src, dst):
                    success_count += 1
                else:
                    error_count += 1
            else:
                if migrate_dir(src, dst):
                    success_count += 1
                else:
                    error_count += 1
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            error_count += 1
    
    print("\n" + "=" * 60)
    print("重组完成")
    print("=" * 60)
    print(f"✅ 成功: {success_count}")
    print(f"⏭️  跳过: {skip_count}")
    print(f"❌ 错误: {error_count}")

if __name__ == '__main__':
    # 先执行 DRY-RUN 预览
    print("执行预览模式...\n")
    DRY_RUN = True
    main()
