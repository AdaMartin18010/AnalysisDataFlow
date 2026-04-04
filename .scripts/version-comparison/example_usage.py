#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink 版本对比工具使用示例
==========================

演示如何使用版本对比工具的 Python API

运行方式:
    python example_usage.py
"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

import yaml

# 导入工具类 (使用 importlib 因为文件名包含连字符)
import importlib.util

def load_module(module_name, file_path):
    """动态加载模块"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    print("=" * 60)
    print("Flink 版本对比工具 - 使用示例")
    print("=" * 60)
    
    # 加载配置
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    print("\n1. 加载配置成功")
    print(f"   配置的版本: {list(config.get('versions', {}).keys())}")
    
    # 示例 1: 版本对比
    print("\n2. 版本对比示例")
    print("-" * 40)
    
    compare_module = load_module("compare_versions", 
                                  Path(__file__).parent / "compare-versions.py")
    comparator = compare_module.VersionComparator(config)
    
    versions = ["2.4", "2.5", "3.0"]
    print(f"对比版本: {versions}")
    
    # 获取版本信息
    for v in versions:
        info = comparator.get_version_info(v)
        print(f"  Flink {v}: {info.description}")
    
    # 示例 2: 生成特性矩阵
    print("\n3. 特性矩阵示例 (核心API)")
    print("-" * 40)
    
    matrix_module = load_module("feature_matrix_generator", 
                                 Path(__file__).parent / "feature-matrix-generator.py")
    matrix_gen = matrix_module.FeatureMatrixGenerator(config)
    
    # 显示部分特性状态
    features_to_check = [
        ("datastream_api", "DataStream API"),
        ("ai_agent", "AI Agent"),
        ("serverless", "Serverless"),
        ("unified_execution", "统一执行层"),
    ]
    
    for feature_id, feature_name in features_to_check:
        print(f"\n  {feature_name}:")
        for v in versions:
            status = matrix_gen.get_feature_status(v, feature_id)
            symbol = matrix_gen.get_status_symbol(status)
            print(f"    Flink {v}: {symbol} ({status})")
    
    # 示例 3: 生成 ASCII 热力图
    print("\n4. 特性支持热力图")
    print("-" * 40)
    heatmap = matrix_gen.generate_ascii_heatmap(versions)
    # 只显示前几行
    for line in heatmap.split('\n')[:15]:
        print(line)
    print("  ... (省略后续内容)")
    
    print("\n" + "=" * 60)
    print("示例运行完成!")
    print("=" * 60)
    print("\n提示:")
    print("  - 使用命令行工具: python compare-versions.py --help")
    print("  - 查看详细文档: README.md")
    print("  - 修改配置: config.yaml")


if __name__ == "__main__":
    main()
