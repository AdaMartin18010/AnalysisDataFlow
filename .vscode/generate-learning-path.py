#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 交互式学习路径生成器

根据用户背景和目标生成个性化学习路径
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
LEARNING_PATHS_DIR = PROJECT_ROOT / "LEARNING-PATHS"
TEMPLATE_PATH = Path(__file__).parent / "learning-path-template.md"

# 知识库文档索引
KNOWLEDGE_BASE = {
    "struct": {
        "foundation": [
            ("01.01-unified-streaming-theory.md", "统一流处理理论", "L3", "3h"),
            ("01.02-process-calculus-primer.md", "进程演算入门", "L4", "4h"),
            ("01.03-actor-model-formalization.md", "Actor模型形式化", "L4", "3h"),
            ("01.04-dataflow-model-formalization.md", "Dataflow模型形式化", "L3", "3h"),
            ("01.05-csp-formalization.md", "CSP形式化", "L4", "4h"),
            ("01.07-session-types.md", "会话类型", "L5", "4h"),
        ],
        "properties": [
            ("02.01-determinism-in-streaming.md", "流处理确定性", "L4", "3h"),
            ("02.02-consistency-hierarchy.md", "一致性层次结构", "L3", "2h"),
            ("02.03-watermark-monotonicity.md", "Watermark单调性", "L3", "2h"),
            ("02.04-liveness-and-safety.md", "活性与安全性", "L4", "3h"),
            ("02.05-type-safety-derivation.md", "类型安全推导", "L5", "4h"),
        ],
        "proofs": [
            ("04.01-flink-checkpoint-correctness.md", "Flink Checkpoint正确性", "L4", "4h"),
            ("04.02-flink-exactly-once-correctness.md", "Flink Exactly-Once正确性", "L4", "4h"),
            ("04.03-chandy-lamport-consistency.md", "Chandy-Lamport一致性", "L4", "3h"),
        ],
        "frontier": [
            ("06.01-open-problems-streaming-verification.md", "流处理验证开放问题", "L6", "5h"),
            ("06.03-ai-agent-session-types.md", "AI Agent会话类型", "L5", "4h"),
        ]
    },
    "knowledge": {
        "concepts": [
            ("01-concept-atlas/streaming-models-mindmap.md", "流处理模型思维导图", "L2", "2h"),
            ("01-concept-atlas/data-streaming-landscape-2026-complete.md", "2026流处理全景", "L2", "3h"),
        ],
        "patterns": [
            ("02-design-patterns/pattern-event-time-processing.md", "事件时间处理", "L3", "3h"),
            ("02-design-patterns/pattern-windowed-aggregation.md", "窗口聚合", "L2", "2h"),
            ("02-design-patterns/pattern-stateful-computation.md", "有状态计算", "L3", "3h"),
            ("02-design-patterns/pattern-checkpoint-recovery.md", "Checkpoint恢复", "L3", "3h"),
            ("02-design-patterns/pattern-cep-complex-event.md", "复杂事件处理", "L3", "4h"),
            ("02-design-patterns/pattern-async-io-enrichment.md", "异步IO增强", "L3", "2h"),
        ],
        "business": [
            ("03-business-patterns/iot-stream-processing.md", "IoT流处理", "L2", "2h"),
            ("03-business-patterns/fintech-realtime-risk-control.md", "金融科技实时风控", "L3", "3h"),
            ("03-business-patterns/real-time-recommendation.md", "实时推荐系统", "L3", "3h"),
            ("03-business-patterns/log-monitoring.md", "日志监控", "L2", "2h"),
        ],
        "selection": [
            ("04-technology-selection/engine-selection-guide.md", "引擎选择指南", "L2", "2h"),
            ("04-technology-selection/flink-vs-risingwave.md", "Flink vs RisingWave", "L3", "2h"),
            ("04-technology-selection/streaming-database-guide.md", "流数据库指南", "L2", "2h"),
        ],
        "anti_patterns": [
            ("09-anti-patterns/anti-pattern-checklist.md", "反模式检查清单", "L2", "2h"),
            ("09-anti-patterns/anti-pattern-01-global-state-abuse.md", "全局状态滥用", "L2", "1h"),
            ("09-anti-patterns/anti-pattern-02-watermark-misconfiguration.md", "Watermark配置错误", "L2", "1h"),
            ("09-anti-patterns/anti-pattern-08-ignoring-backpressure.md", "忽视反压", "L2", "1h"),
        ],
        "exercises": [
            ("98-exercises/exercise-02-flink-basics.md", "Flink基础练习", "L2", "4h"),
            ("98-exercises/exercise-03-checkpoint-analysis.md", "Checkpoint分析", "L3", "3h"),
            ("98-exercises/exercise-04-consistency-models.md", "一致性模型", "L3", "3h"),
        ]
    },
    "flink": {
        "architecture": [
            ("01-architecture/deployment-architectures.md", "部署架构", "L2", "2h"),
            ("01-architecture/flink-1.x-vs-2.0-comparison.md", "Flink 1.x vs 2.0", "L2", "2h"),
        ],
        "core_mechanisms": [
            ("02-core-mechanisms/checkpoint-mechanism-deep-dive.md", "Checkpoint机制", "L3", "4h"),
            ("02-core-mechanisms/exactly-once-semantics-deep-dive.md", "Exactly-Once语义", "L3", "4h"),
            ("02-core-mechanisms/time-semantics-and-watermark.md", "时间语义与Watermark", "L3", "3h"),
            ("02-core-mechanisms/backpressure-and-flow-control.md", "反压与流量控制", "L3", "3h"),
            ("02-core-mechanisms/state-backend-selection.md", "状态后端选择", "L3", "2h"),
        ],
        "sql_api": [
            ("03-sql-table-api/flink-sql-window-functions-deep-dive.md", "SQL窗口函数", "L3", "3h"),
            ("03-sql-table-api/materialized-tables.md", "物化表", "L3", "3h"),
            ("03-sql-table-api/sql-vs-datastream-comparison.md", "SQL vs DataStream", "L2", "2h"),
        ],
        "connectors": [
            ("04-connectors/kafka-integration-patterns.md", "Kafka集成", "L2", "3h"),
            ("04-connectors/flink-cdc-3.0-data-integration.md", "CDC数据集成", "L3", "4h"),
            ("04-connectors/flink-paimon-integration.md", "Paimon集成", "L3", "3h"),
        ],
        "deployment": [
            ("10-deployment/kubernetes-deployment.md", "Kubernetes部署", "L3", "4h"),
            ("10-deployment/kubernetes-deployment-production-guide.md", "生产环境部署指南", "L3", "4h"),
        ],
        "case_studies": [
            ("07-case-studies/case-realtime-analytics.md", "实时分析案例", "L2", "2h"),
            ("07-case-studies/case-iot-stream-processing.md", "IoT流处理案例", "L2", "2h"),
            ("07-case-studies/case-ecommerce-realtime-recommendation.md", "电商实时推荐", "L3", "3h"),
        ],
        "ai_ml": [
            ("12-ai-ml/flink-ml-architecture.md", "Flink ML架构", "L3", "3h"),
            ("12-ai-ml/realtime-feature-engineering-feature-store.md", "实时特征工程", "L3", "4h"),
            ("12-ai-ml/flink-llm-integration.md", "LLM集成", "L4", "4h"),
        ]
    }
}

# 预定义学习路径配置
PREDEFINED_PATHS = {
    "data-engineer": {
        "name": "数据工程师",
        "difficulty": "中级",
        "duration": "8-12周",
        "target_audience": "数据工程师、ETL开发者、数据平台工程师",
        "objectives": [
            "掌握流处理核心概念和架构",
            "熟练使用Flink进行数据处理",
            "理解Checkpoint和Exactly-Once语义",
            "具备生产环境调优和故障排查能力"
        ],
        "prerequisites": [
            "熟悉SQL和至少一种编程语言(Java/Python/Scala)",
            "了解基础的数据库概念",
            "有批处理数据处理经验"
        ],
        "phases": [
            {
                "name": "基础概念阶段",
                "duration": "第1-2周",
                "topics": ["流处理基础", "时间语义", "Window机制"],
                "docs": {
                    "knowledge": ["concepts/01", "concepts/02"],
                    "flink": ["architecture/01", "core_mechanisms/03"]
                }
            },
            {
                "name": "Flink核心机制",
                "duration": "第3-5周",
                "topics": ["Checkpoint机制", "Exactly-Once", "状态管理"],
                "docs": {
                    "flink": ["core_mechanisms/01", "core_mechanisms/02", "core_mechanisms/05"],
                    "struct": ["properties/02", "properties/03"]
                }
            },
            {
                "name": "实践应用阶段",
                "duration": "第6-8周",
                "topics": ["SQL/Table API", "连接器", "部署运维"],
                "docs": {
                    "flink": ["sql_api/01", "sql_api/02", "connectors/01", "deployment/01"],
                    "knowledge": ["patterns/01", "patterns/02", "anti_patterns/01"]
                }
            },
            {
                "name": "高级优化阶段",
                "duration": "第9-12周",
                "topics": ["性能调优", "反压处理", "生产实践"],
                "docs": {
                    "flink": ["core_mechanisms/04", "case_studies/01"],
                    "knowledge": ["business/01", "selection/01"]
                }
            }
        ],
        "projects": [
            "实现一个实时日志分析Pipeline",
            "构建用户行为实时分析Dashboard",
            "设计并优化一个电商实时推荐流"
        ],
        "checkpoints": [
            "能够解释Event Time和Processing Time的区别",
            "能够设计合理的Checkpoint策略",
            "能够诊断和解决反压问题",
            "能够完成生产环境的部署配置"
        ]
    },
    "backend-developer": {
        "name": "后端开发工程师",
        "difficulty": "中级",
        "duration": "6-10周",
        "target_audience": "后端开发工程师、全栈开发者",
        "objectives": [
            "理解流处理在后端系统中的应用场景",
            "掌握Flink与现有系统的集成方法",
            "能够设计和实现实时数据处理服务"
        ],
        "prerequisites": [
            "扎实的Java或Python编程基础",
            "了解微服务架构",
            "熟悉消息队列(Kafka等)"
        ],
        "phases": [
            {
                "name": "流处理入门",
                "duration": "第1-2周",
                "topics": ["流处理基础", "架构模式"],
                "docs": {
                    "knowledge": ["concepts/01"],
                    "flink": ["architecture/01"]
                }
            },
            {
                "name": "核心概念掌握",
                "duration": "第3-5周",
                "topics": ["时间语义", "状态管理", "容错机制"],
                "docs": {
                    "flink": ["core_mechanisms/03", "core_mechanisms/01"],
                    "struct": ["properties/02"]
                }
            },
            {
                "name": "系统集成",
                "duration": "第6-8周",
                "topics": ["连接器", "SQL API", "部署"],
                "docs": {
                    "flink": ["connectors/01", "sql_api/03", "deployment/01"]
                }
            },
            {
                "name": "生产实践",
                "duration": "第9-10周",
                "topics": ["监控告警", "故障排查"],
                "docs": {
                    "knowledge": ["anti_patterns/01", "patterns/03"]
                }
            }
        ],
        "projects": [
            "集成Flink到现有微服务架构",
            "实现实时通知推送服务",
            "构建业务指标实时监控系统"
        ],
        "checkpoints": [
            "能够用Flink实现基本的流处理任务",
            "理解并与现有系统集成的注意事项",
            "能够处理常见的生产环境问题"
        ]
    },
    "researcher": {
        "name": "研究员",
        "difficulty": "高级",
        "duration": "12-16周",
        "target_audience": "研究人员、博士生、高级算法工程师",
        "objectives": [
            "深入理解流处理的形式化理论基础",
            "掌握分布式系统的验证方法",
            "能够进行流处理系统的理论分析"
        ],
        "prerequisites": [
            "扎实的理论基础(形式语言、自动机、逻辑)",
            "熟悉进程演算或相关形式化方法",
            "有阅读学术论文的经验"
        ],
        "phases": [
            {
                "name": "理论基础",
                "duration": "第1-4周",
                "topics": ["进程演算", "Actor模型", "CSP", "会话类型"],
                "docs": {
                    "struct": ["foundation/02", "foundation/03", "foundation/05", "foundation/06"]
                }
            },
            {
                "name": "流处理语义",
                "duration": "第5-7周",
                "topics": ["Dataflow模型", "一致性模型", "类型安全"],
                "docs": {
                    "struct": ["foundation/04", "properties/02", "properties/05"]
                }
            },
            {
                "name": "验证与证明",
                "duration": "第8-11周",
                "topics": ["Checkpoint正确性", "Exactly-Once", "活性安全"],
                "docs": {
                    "struct": ["proofs/01", "proofs/02", "proofs/03", "properties/04"]
                }
            },
            {
                "name": "前沿研究",
                "duration": "第12-16周",
                "topics": ["开放问题", "AI Agent", "新范式"],
                "docs": {
                    "struct": ["frontier/01", "frontier/02"],
                    "knowledge": ["concepts/02"]
                }
            }
        ],
        "projects": [
            "形式化验证一个小型流处理系统",
            "设计新的流处理语义",
            "发表相关研究论文或技术报告"
        ],
        "checkpoints": [
            "能够用形式化方法描述流处理系统",
            "理解主要定理的证明思路",
            "能够发现并提出研究问题"
        ]
    },
    "architect": {
        "name": "系统架构师",
        "difficulty": "高级",
        "duration": "6-8周",
        "target_audience": "系统架构师、技术负责人",
        "objectives": [
            "全面评估流处理技术选型",
            "设计大规模流处理架构",
            "指导团队进行技术决策"
        ],
        "prerequisites": [
            "丰富的分布式系统设计经验",
            "熟悉主流大数据技术栈",
            "有技术选型和架构设计经验"
        ],
        "phases": [
            {
                "name": "技术全景",
                "duration": "第1-2周",
                "topics": ["流处理生态", "技术对比"],
                "docs": {
                    "knowledge": ["concepts/02", "selection/01", "selection/02", "selection/03"]
                }
            },
            {
                "name": "架构设计",
                "duration": "第3-4周",
                "topics": ["部署架构", "存储选型", "连接器"],
                "docs": {
                    "flink": ["architecture/01", "connectors/02", "connectors/03"],
                    "knowledge": ["patterns/04"]
                }
            },
            {
                "name": "生产考量",
                "duration": "第5-6周",
                "topics": ["运维监控", "成本优化", "安全合规"],
                "docs": {
                    "flink": ["deployment/02"],
                    "knowledge": ["anti_patterns/01", "business/02"]
                }
            },
            {
                "name": "案例学习",
                "duration": "第7-8周",
                "topics": ["业界案例", "最佳实践"],
                "docs": {
                    "knowledge": ["business/03", "business/04"],
                    "flink": ["case_studies/02", "case_studies/03"]
                }
            }
        ],
        "projects": [
            "设计一个企业级流处理平台架构",
            "完成流处理技术选型报告",
            "制定团队流处理开发规范"
        ],
        "checkpoints": [
            "能够根据场景选择合适的技术栈",
            "能够识别架构设计中的风险点",
            "能够制定可落地的实施计划"
        ]
    },
    "student": {
        "name": "学生",
        "difficulty": "初级",
        "duration": "4-6周",
        "target_audience": "计算机专业学生、转行者",
        "objectives": [
            "建立流处理的基础概念框架",
            "掌握Flink的基本使用",
            "具备入门级项目开发能力"
        ],
        "prerequisites": [
            "基础编程能力(Java/Python)",
            "了解基本的数据结构",
            "对大数据技术有兴趣"
        ],
        "phases": [
            {
                "name": "入门阶段",
                "duration": "第1周",
                "topics": ["流处理简介", "环境搭建"],
                "docs": {
                    "knowledge": ["concepts/01"],
                    "knowledge_exercises": ["exercises/01"]
                }
            },
            {
                "name": "基础概念",
                "duration": "第2-3周",
                "topics": ["DataStream API", "时间语义", "窗口"],
                "docs": {
                    "flink": ["core_mechanisms/03"],
                    "knowledge": ["patterns/01", "patterns/02"]
                }
            },
            {
                "name": "实践入门",
                "duration": "第4-5周",
                "topics": ["简单项目", "SQL入门"],
                "docs": {
                    "flink": ["sql_api/03"],
                    "knowledge_exercises": ["exercises/02"]
                }
            },
            {
                "name": "项目实战",
                "duration": "第6周",
                "topics": ["综合项目", "总结回顾"],
                "docs": {
                    "flink": ["case_studies/01"]
                }
            }
        ],
        "projects": [
            "实现WordCount流处理程序",
            "构建简单的实时数据统计",
            "完成一个端到端的流处理项目"
        ],
        "checkpoints": [
            "理解流处理和批处理的区别",
            "能够独立运行Flink程序",
            "能够解释基本的流处理概念"
        ]
    },
    "interview-prep": {
        "name": "面试准备",
        "difficulty": "中高级",
        "duration": "2-4周",
        "target_audience": "准备流处理相关面试的候选人",
        "objectives": [
            "系统复习流处理核心知识点",
            "掌握常见面试题和解答思路",
            "能够清晰表达技术方案"
        ],
        "prerequisites": [
            "有一定的流处理实践经验",
            "了解目标公司的业务场景"
        ],
        "phases": [
            {
                "name": "核心概念速览",
                "duration": "第1周",
                "topics": ["时间语义", "Watermark", "窗口类型"],
                "docs": {
                    "struct": ["properties/02", "properties/03"],
                    "knowledge": ["concepts/01"]
                }
            },
            {
                "name": "机制深入",
                "duration": "第2周",
                "topics": ["Checkpoint", "Exactly-Once", "状态后端"],
                "docs": {
                    "flink": ["core_mechanisms/01", "core_mechanisms/02"],
                    "struct": ["proofs/01", "proofs/02"]
                }
            },
            {
                "name": "设计与优化",
                "duration": "第3周",
                "topics": ["设计模式", "性能优化", "反模式"],
                "docs": {
                    "knowledge": ["patterns/01", "patterns/02", "patterns/03", "anti_patterns/01"],
                    "flink": ["core_mechanisms/04"]
                }
            },
            {
                "name": "模拟演练",
                "duration": "第4周",
                "topics": ["案例分析", "系统设计"],
                "docs": {
                    "flink": ["case_studies/01", "case_studies/02"],
                    "knowledge": ["selection/01"]
                }
            }
        ],
        "projects": [
            "模拟面试问题集练习",
            "设计题方案梳理",
            "手写核心算法实现"
        ],
        "checkpoints": [
            "能够清晰解释核心概念",
            "能够分析和解决常见问题",
            "能够进行系统设计讨论"
        ]
    }
}


def print_header():
    """打印欢迎信息"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║    AnalysisDataFlow 交互式学习路径生成器                         ║
║                                                                  ║
║    根据您的背景和目标，为您定制个性化学习路径                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")


def ask_question(question: str, options: List[Tuple[str, str]], allow_multiple: bool = False) -> str or List[str]:
    """提问并获取答案"""
    print(f"\n📋 {question}\n")
    for i, (key, desc) in enumerate(options, 1):
        print(f"   {i}. {key}")
        if desc:
            print(f"      {desc}")
    
    if allow_multiple:
        print("\n   (可输入多个选项，用逗号分隔，如: 1,2,3)")
    
    while True:
        try:
            choice = input("\n👉 请输入选项编号: ").strip()
            
            if allow_multiple:
                indices = [int(x.strip()) for x in choice.split(",")]
                return [options[i-1][0] for i in indices if 1 <= i <= len(options)]
            else:
                idx = int(choice)
                if 1 <= idx <= len(options):
                    return options[idx-1][0]
        except (ValueError, IndexError):
            pass
        print("❌ 无效输入，请重新选择")


def interactive_assessment() -> Dict:
    """交互式评估用户背景"""
    print_header()
    
    # 1. 角色
    role = ask_question(
        "您目前的角色是？",
        [
            ("data-engineer", "数据工程师，负责ETL和数据管道开发"),
            ("backend-developer", "后端开发工程师，需要集成流处理能力"),
            ("researcher", "研究员或博士生，关注理论和方法"),
            ("architect", "系统架构师，负责技术选型和架构设计"),
            ("student", "学生或初学者，希望入门学习"),
            ("other", "其他角色")
        ]
    )
    
    # 2. 经验水平
    experience = ask_question(
        "您的流处理经验水平如何？",
        [
            ("beginner", "初学者：几乎没有流处理经验"),
            ("intermediate", "中级：有过一些流处理项目经验"),
            ("advanced", "高级：有丰富的流处理实战经验"),
            ("expert", "专家：深入理解流处理原理和实现")
        ]
    )
    
    # 3. 学习目标
    goal = ask_question(
        "您的主要学习目标是什么？",
        [
            ("job", "求职：为找工作或跳槽做准备"),
            ("project", "项目：为完成实际工作任务"),
            ("research", "研究：深入理解原理，可能发表论文"),
            ("interview", "面试：准备技术面试"),
            ("general", "通用：提升技术能力，拓宽知识面")
        ]
    )
    
    # 4. 时间投入
    time_commitment = ask_question(
        "您每周可以投入多少时间学习？",
        [
            ("minimal", "< 5小时，碎片化学习"),
            ("moderate", "5-10小时，有固定学习时间"),
            ("intensive", "10-20小时，可以集中学习"),
            ("fulltime", "> 20小时，全职学习")
        ]
    )
    
    # 5. 兴趣方向（可多选）
    interests = ask_question(
        "您对哪些方向最感兴趣？",
        [
            ("theory", "理论基础：形式化方法、语义分析"),
            ("practice", "工程实践：Flink开发、性能调优"),
            ("architecture", "系统设计：架构选型、平台搭建"),
            ("ai-ml", "AI/ML：实时特征工程、模型服务"),
            ("business", "业务应用：行业案例、最佳实践")
        ],
        allow_multiple=True
    )
    
    return {
        "role": role,
        "experience": experience,
        "goal": goal,
        "time_commitment": time_commitment,
        "interests": interests if isinstance(interests, list) else [interests]
    }


def select_path(config: Dict) -> Tuple[str, Dict]:
    """根据用户配置选择最合适的学习路径"""
    
    # 映射逻辑
    if config["goal"] == "interview":
        return "interview-prep", PREDEFINED_PATHS["interview-prep"]
    
    if config["role"] in PREDEFINED_PATHS:
        return config["role"], PREDEFINED_PATHS[config["role"]]
    
    # 根据经验调整
    if config["experience"] == "beginner":
        return "student", PREDEFINED_PATHS["student"]
    
    if config["experience"] in ["advanced", "expert"] and "theory" in config["interests"]:
        return "researcher", PREDEFINED_PATHS["researcher"]
    
    # 默认选择数据工程师路径
    return "data-engineer", PREDEFINED_PATHS["data-engineer"]


def generate_path_content(path_key: str, path_config: Dict, user_config: Dict) -> str:
    """生成学习路径内容"""
    
    # 读取模板
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 根据用户配置调整难度和时间
    difficulty = path_config["difficulty"]
    if user_config["experience"] == "beginner":
        difficulty = "初级"
    elif user_config["experience"] in ["advanced", "expert"]:
        difficulty = "高级"
    
    # 生成阶段内容
    phases_content = ""
    for i, phase in enumerate(path_config["phases"], 1):
        phases_content += f"""### 阶段{i}: {phase['name']}

**时间安排**: {phase['duration']}

**学习主题**:
"""
        for topic in phase["topics"]:
            phases_content += f"- {topic}\n"
        
        phases_content += "\n**推荐文档**:\n"
        for category, docs in phase.get("docs", {}).items():
            if docs:
                phases_content += f"- {category.upper()}: " + ", ".join(docs) + "\n"
        
        phases_content += "\n---\n\n"
    
    # 生成项目内容
    projects_content = ""
    for i, project in enumerate(path_config["projects"], 1):
        projects_content += f"### 项目{i}: {project}\n\n"
        projects_content += "**建议产出**:\n"
        projects_content += "- 可运行的代码\n"
        projects_content += "- 设计文档\n"
        projects_content += "- 遇到的问题和解决方案\n\n"
    
    # 生成检查点内容
    checkpoints_content = ""
    for i, checkpoint in enumerate(path_config["checkpoints"], 1):
        checkpoints_content += f"- [ ] **检查点{i}**: {checkpoint}\n"
    
    # 文档引用表格（简化版）
    def make_doc_table(category: str, docs: List[Tuple]) -> str:
        lines = []
        for doc_file, title, level, time in docs[:5]:  # 限制数量
            lines.append(f"| `{doc_file}` | {title} | {level} | {time} |")
        return "\n".join(lines) if lines else "| (根据阶段选择) | - | - | - |"
    
    # 替换模板变量
    content = template.replace("{{path_name}}", path_config["name"])
    content = content.replace("{{difficulty}}", difficulty)
    content = content.replace("{{duration}}", path_config["duration"])
    content = content.replace("{{target_audience}}", path_config["target_audience"])
    
    # 学习目标
    objectives = "\n".join([f"- {obj}" for obj in path_config["objectives"]])
    content = content.replace("{{learning_objectives}}", objectives)
    
    # 前置知识
    prereqs = "\n".join([f"- {p}" for p in path_config["prerequisites"]])
    content = content.replace("{{prerequisites}}", prereqs)
    
    # 完成标准
    completion = "完成所有阶段学习并通过自测检查点"
    content = content.replace("{{completion_criteria}}", completion)
    
    # 各部分内容
    content = content.replace("{{phases}}", phases_content)
    content = content.replace("{{projects}}", projects_content)
    content = content.replace("{{checkpoints}}", checkpoints_content)
    
    # 文档表格
    struct_docs = []
    for cat in KNOWLEDGE_BASE["struct"].values():
        struct_docs.extend(cat[:2])
    content = content.replace("{{struct_docs}}", make_doc_table("struct", struct_docs))
    
    knowledge_docs = []
    for cat in KNOWLEDGE_BASE["knowledge"].values():
        knowledge_docs.extend(cat[:2])
    content = content.replace("{{knowledge_docs}}", make_doc_table("knowledge", knowledge_docs))
    
    flink_docs = []
    for cat in KNOWLEDGE_BASE["flink"].values():
        flink_docs.extend(cat[:2])
    content = content.replace("{{flink_docs}}", make_doc_table("flink", flink_docs))
    
    # 延伸阅读
    further = """- Apache Flink官方文档
- Kleppmann《Designing Data-Intensive Applications》
- Akidau《Streaming Systems》
- 相关学术论文（见各文档引用）"""
    content = content.replace("{{further_reading}}", further)
    
    # 生成日期
    content = content.replace("{{generation_date}}", datetime.now().strftime("%Y-%m-%d"))
    
    return content


def save_path(path_key: str, content: str):
    """保存学习路径到文件"""
    filename = f"{path_key}-custom.md"
    filepath = LEARNING_PATHS_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath


def main():
    """主函数"""
    # 确保目录存在
    LEARNING_PATHS_DIR.mkdir(exist_ok=True)
    
    # 交互式评估
    user_config = interactive_assessment()
    
    print("\n" + "="*60)
    print("正在生成您的个性化学习路径...")
    print("="*60)
    
    # 选择路径
    path_key, path_config = select_path(user_config)
    
    # 生成内容
    content = generate_path_content(path_key, path_config, user_config)
    
    # 保存文件
    filepath = save_path(path_key, content)
    
    print(f"\n✅ 学习路径已生成!")
    print(f"\n📄 文件位置: {filepath}")
    print(f"\n📚 路径概要:")
    print(f"   - 名称: {path_config['name']}")
    print(f"   - 难度: {path_config['difficulty']}")
    print(f"   - 预计时长: {path_config['duration']}")
    print(f"   - 阶段数: {len(path_config['phases'])}")
    
    print(f"\n🎯 建议从以下文档开始:")
    first_phase = path_config['phases'][0]
    for category, docs in first_phase.get('docs', {}).items():
        if docs:
            print(f"   - [{category.upper()}] {docs[0]}")
    
    print("\n💡 提示:")
    print("   - 使用 VS Code 打开项目可以方便地浏览所有文档")
    print("   - 每个阶段完成后，请在检查点处进行自我测试")
    print("   - 遇到问题可以查阅 THEOREM-REGISTRY.md 查找相关定理")
    
    print("\n" + "="*60)
    print("祝您学习顺利!")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消学习路径生成")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)
