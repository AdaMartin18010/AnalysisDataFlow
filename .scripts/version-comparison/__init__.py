# -*- coding: utf-8 -*-
"""
Flink 版本对比工具包
===================

提供 Flink 多版本特性对比、差异报告生成、特性矩阵可视化等功能。

模块说明:
- compare_versions: 版本对比主模块
- generate_diff_report: 文档差异报告生成
- feature_matrix_generator: 特性矩阵生成
- config: 配置管理

使用示例:
    from version_comparison import VersionComparator
    
    comparator = VersionComparator(config)
    report = comparator.generate_markdown_report(["2.4", "2.5", "3.0"])

版本: 1.0.0
作者: Agent
日期: 2026-04-04
"""

__version__ = "1.0.0"
__author__ = "Agent"
__date__ = "2026-04-04"

# 导出主要类
# 注意: 这些类需要在导入时可用，但由于可能存在循环依赖，
# 实际使用时建议直接从模块导入

__all__ = [
    "VersionComparator",
    "DiffReportGenerator",
    "FeatureMatrixGenerator",
    "FeatureExtractor",
    "load_config",
]


def load_config(config_path: str = None):
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径，默认为 config.yaml
        
    Returns:
        配置字典
    """
    import yaml
    from pathlib import Path
    
    if config_path is None:
        config_path = Path(__file__).parent / "config.yaml"
    else:
        config_path = Path(config_path)
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
