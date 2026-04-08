#!/usr/bin/env python3
"""
知识图谱 v2.0 学习路径生成器
预计算推荐路径
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "knowledge-graph-site" / "data"

def generate_learning_paths():
    """生成预计算的学习路径"""
    
    paths = {
        "version": "2.0.0",
        "paths": [
            {
                "id": "beginner",
                "name": "初学者路径",
                "description": "从零开始学习流计算基础",
                "difficulty": "初级",
                "estimated_hours": 20,
                "steps": [
                    {
                        "order": 1,
                        "title": "流计算基础概念",
                        "resources": ["Struct/01-foundation", "QUICK-START.md"],
                        "concepts": ["Dataflow模型", "事件时间", "处理时间"]
                    },
                    {
                        "order": 2,
                        "title": "Flink快速入门",
                        "resources": ["Flink/01-getting-started", "QUICK-START.md"],
                        "concepts": ["DataStream API", "转换操作", "Sink"]
                    },
                    {
                        "order": 3,
                        "title": "状态与容错",
                        "resources": ["Flink/02-core-mechanisms/checkpointing.md"],
                        "concepts": ["Checkpoint", "状态后端", "Exactly-Once"]
                    },
                    {
                        "order": 4,
                        "title": "时间语义",
                        "resources": ["Flink/02-core-mechanisms/time-semantics.md"],
                        "concepts": ["Watermark", "窗口", "允许延迟"]
                    }
                ]
            },
            {
                "id": "intermediate",
                "name": "进阶开发者路径",
                "description": "深入理解Flink机制和最佳实践",
                "difficulty": "中级",
                "estimated_hours": 40,
                "steps": [
                    {
                        "order": 1,
                        "title": "高级状态管理",
                        "resources": ["Flink/02-core-mechanisms/state-management.md"],
                        "concepts": ["Keyed State", "Operator State", "状态TTL"]
                    },
                    {
                        "order": 2,
                        "title": "SQL与Table API",
                        "resources": ["Flink/03-sql-table-api"],
                        "concepts": ["Table API", "SQL", "动态表"]
                    },
                    {
                        "order": 3,
                        "title": "性能调优",
                        "resources": ["Flink/06-engineering/performance-tuning.md"],
                        "concepts": ["并行度", "Chaining", "Slot共享"]
                    },
                    {
                        "order": 4,
                        "title": "监控与可观测性",
                        "resources": ["Flink/15-observability"],
                        "concepts": ["Metrics", "Tracing", "日志聚合"]
                    }
                ]
            },
            {
                "id": "advanced",
                "name": "专家级路径",
                "description": "形式化理论和深度优化",
                "difficulty": "高级",
                "estimated_hours": 60,
                "steps": [
                    {
                        "order": 1,
                        "title": "形式化语义",
                        "resources": ["Struct/01-foundation", "Struct/02-properties"],
                        "concepts": ["进程演算", "CSP", "Actor模型"]
                    },
                    {
                        "order": 2,
                        "title": "一致性理论",
                        "resources": ["Struct/03-relationships/consistency-models.md"],
                        "concepts": ["一致性级别", "CAP定理", "PACELC"]
                    },
                    {
                        "order": 3,
                        "title": "分布式算法",
                        "resources": ["Struct/04-proofs"],
                        "concepts": ["共识算法", "快照算法", "故障检测"]
                    },
                    {
                        "order": 4,
                        "title": "生产环境实战",
                        "resources": ["Flink/10-deployment", "Flink/11-benchmarking"],
                        "concepts": ["Kubernetes部署", "自动扩缩容", "灾难恢复"]
                    }
                ]
            },
            {
                "id": "dataflow_expert",
                "name": "Dataflow模型专家",
                "description": "深入理解Dataflow模型及其应用",
                "difficulty": "高级",
                "estimated_hours": 35,
                "steps": [
                    {
                        "order": 1,
                        "title": "Dataflow模型基础",
                        "resources": ["Struct/01-foundation/dataflow-model.md"],
                        "concepts": ["Dataflow模型", "Beam模型", "流批统一"]
                    },
                    {
                        "order": 2,
                        "title": "窗口语义",
                        "resources": ["Struct/02-properties/window-semantics.md"],
                        "concepts": ["窗口类型", "触发器", "累积模式"]
                    },
                    {
                        "order": 3,
                        "title": "时间推理",
                        "resources": ["Struct/03-relationships/temporal-reasoning.md"],
                        "concepts": ["事件时间推理", "进度追踪", "水位线传播"]
                    }
                ]
            },
            {
                "id": "flink_operations",
                "name": "Flink运维工程师",
                "description": "Flink生产环境运维和管理",
                "difficulty": "中级",
                "estimated_hours": 30,
                "steps": [
                    {
                        "order": 1,
                        "title": "部署架构",
                        "resources": ["Flink/10-deployment"],
                        "concepts": ["Standalone", "YARN", "Kubernetes"]
                    },
                    {
                        "order": 2,
                        "title": "资源配置",
                        "resources": ["Flink/06-engineering/resource-management.md"],
                        "concepts": ["内存配置", "网络缓冲", "JVM调优"]
                    },
                    {
                        "order": 3,
                        "title": "故障排查",
                        "resources": ["TROUBLESHOOTING.md"],
                        "concepts": ["背压诊断", "OOM分析", "网络问题"]
                    }
                ]
            }
        ],
        "recommendations": {
            "by_role": {
                "数据工程师": ["beginner", "intermediate", "flink_operations"],
                "算法工程师": ["beginner", "intermediate", "dataflow_expert"],
                "架构师": ["intermediate", "advanced", "dataflow_expert"],
                "研究员": ["beginner", "advanced"],
                "运维工程师": ["beginner", "flink_operations"]
            },
            "by_goal": {
                "快速上手": ["beginner"],
                "性能优化": ["intermediate", "advanced"],
                "生产部署": ["intermediate", "flink_operations"],
                "理论深入": ["advanced", "dataflow_expert"],
                "故障排查": ["intermediate", "flink_operations"]
            }
        }
    }
    
    return paths

def generate_skill_tree():
    """生成技能树数据"""
    
    skill_tree = {
        "version": "2.0.0",
        "categories": [
            {
                "id": "fundamentals",
                "name": "基础理论",
                "skills": [
                    {"id": "f1", "name": "流计算概念", "level": 1, "depends_on": []},
                    {"id": "f2", "name": "事件时间vs处理时间", "level": 1, "depends_on": ["f1"]},
                    {"id": "f3", "name": "Dataflow模型", "level": 2, "depends_on": ["f1"]},
                    {"id": "f4", "name": "窗口计算", "level": 2, "depends_on": ["f2", "f3"]},
                    {"id": "f5", "name": "一致性模型", "level": 3, "depends_on": ["f3"]}
                ]
            },
            {
                "id": "flink_core",
                "name": "Flink核心",
                "skills": [
                    {"id": "c1", "name": "DataStream API", "level": 1, "depends_on": []},
                    {"id": "c2", "name": "状态管理", "level": 2, "depends_on": ["c1"]},
                    {"id": "c3", "name": "Checkpoint机制", "level": 2, "depends_on": ["c1"]},
                    {"id": "c4", "name": "Watermark", "level": 2, "depends_on": ["c1"]},
                    {"id": "c5", "name": "窗口实现", "level": 3, "depends_on": ["c2", "c4"]},
                    {"id": "c6", "name": "背压处理", "level": 3, "depends_on": ["c3"]}
                ]
            },
            {
                "id": "flink_advanced",
                "name": "Flink高级",
                "skills": [
                    {"id": "a1", "name": "Table API", "level": 1, "depends_on": ["c1"]},
                    {"id": "a2", "name": "Flink SQL", "level": 1, "depends_on": ["c1"]},
                    {"id": "a3", "name": "连接器开发", "level": 2, "depends_on": ["c1"]},
                    {"id": "a4", "name": "CEP复杂事件处理", "level": 3, "depends_on": ["c1"]},
                    {"id": "a5", "name": "性能调优", "level": 3, "depends_on": ["c2", "c3", "c6"]}
                ]
            }
        ]
    }
    
    return skill_tree

def main():
    """主函数"""
    print("📚 开始生成学习路径数据...")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 生成学习路径
    paths = generate_learning_paths()
    paths_file = OUTPUT_DIR / "learning-paths.json"
    with open(paths_file, 'w', encoding='utf-8') as f:
        json.dump(paths, f, ensure_ascii=False, indent=2)
    print(f"✅ 学习路径已生成: {paths_file}")
    print(f"   - 路径数: {len(paths['paths'])}")
    
    # 生成技能树
    skill_tree = generate_skill_tree()
    skill_tree_file = OUTPUT_DIR / "skill-tree.json"
    with open(skill_tree_file, 'w', encoding='utf-8') as f:
        json.dump(skill_tree, f, ensure_ascii=False, indent=2)
    print(f"✅ 技能树已生成: {skill_tree_file}")
    print(f"   - 技能类别: {len(skill_tree['categories'])}")
    
    print("\n🎉 学习路径数据生成完成!")

if __name__ == "__main__":
    main()
