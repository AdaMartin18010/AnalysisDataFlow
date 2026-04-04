#!/usr/bin/env python3
"""
动态学习路径推荐系统
Dynamic Learning Path Recommender System for AnalysisDataFlow

功能：根据用户画像和学习目标，智能推荐个性化学习路径
版本: v1.0
作者: AnalysisDataFlow Agent
"""

import json
import os
import sys
import argparse
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum
from pathlib import Path
from collections import defaultdict
import random


class Role(Enum):
    """用户角色"""
    STUDENT = "student"
    DEVELOPER = "developer"
    ARCHITECT = "architect"
    RESEARCHER = "researcher"


class Experience(Enum):
    """经验等级"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Goal(Enum):
    """学习目标"""
    THEORY = "theory"
    PRACTICE = "practice"
    INTERVIEW = "interview"
    RESEARCH = "research"


class TimeFrame(Enum):
    """时间范围"""
    SHORT = "short"      # 1周
    MEDIUM = "medium"    # 1月
    LONG = "long"        # 3月


class PathType(Enum):
    """路径类型"""
    SHORTEST = "shortest"      # 最短路径 - 快速达成目标
    COMPREHENSIVE = "comprehensive"  # 最全面路径 - 覆盖所有相关内容
    BALANCED = "balanced"      # 平衡路径 - 时间与深度的平衡


@dataclass
class UserProfile:
    """用户画像"""
    role: Role
    experience: Experience
    goal: Goal
    timeframe: TimeFrame
    # 可选参数
    interests: List[str] = field(default_factory=list)
    known_topics: List[str] = field(default_factory=list)
    preferred_formats: List[str] = field(default_factory=lambda: ["markdown", "code"])
    weekly_hours: int = 10
    
    def to_dict(self) -> Dict:
        return {
            "role": self.role.value,
            "experience": self.experience.value,
            "goal": self.goal.value,
            "timeframe": self.timeframe.value,
            "interests": self.interests,
            "known_topics": self.known_topics,
            "preferred_formats": self.preferred_formats,
            "weekly_hours": self.weekly_hours
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "UserProfile":
        return cls(
            role=Role(data.get("role", "student")),
            experience=Experience(data.get("experience", "beginner")),
            goal=Goal(data.get("goal", "practice")),
            timeframe=TimeFrame(data.get("timeframe", "medium")),
            interests=data.get("interests", []),
            known_topics=data.get("known_topics", []),
            preferred_formats=data.get("preferred_formats", ["markdown", "code"]),
            weekly_hours=data.get("weekly_hours", 10)
        )


@dataclass
class ContentItem:
    """学习内容项"""
    id: str
    title: str
    path: str
    difficulty: int  # L1-L6
    topics: List[str]
    prerequisites: List[str]
    estimated_hours: float
    content_type: str  # "theory", "engineering", "flink", "frontier"
    format: str  # "markdown", "code", "exercise"
    popularity: int = 0  # 热门度 0-100
    is_new: bool = False
    description: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class LearningStage:
    """学习阶段"""
    name: str
    duration_days: int
    items: List[ContentItem]
    checkpoints: List[str] = field(default_factory=list)
    
    def total_hours(self) -> float:
        return sum(item.estimated_hours for item in self.items)


@dataclass
class LearningPath:
    """学习路径"""
    name: str
    description: str
    path_type: PathType
    total_hours: float
    stages: List[LearningStage]
    checkpoints: List[str]
    recommended_for: List[str]
    created_at: str = field(default_factory=lambda: "2026-04-04")
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "path_type": self.path_type.value,
            "total_hours": self.total_hours,
            "total_days": sum(s.duration_days for s in self.stages),
            "stages": [
                {
                    "name": s.name,
                    "duration_days": s.duration_days,
                    "total_hours": s.total_hours(),
                    "items": [i.to_dict() for i in s.items],
                    "checkpoints": s.checkpoints
                }
                for s in self.stages
            ],
            "checkpoints": self.checkpoints,
            "recommended_for": self.recommended_for
        }


class ContentLibrary:
    """内容库 - 管理所有学习内容"""
    
    def __init__(self):
        self.items: Dict[str, ContentItem] = {}
        self._initialize_content()
    
    def _initialize_content(self):
        """初始化内容库"""
        # Struct/ - 形式理论内容
        struct_content = [
            ContentItem("s-01-01", "流计算形式化基础", "Struct/01-foundation/01.01-stream-computing-formalism.md", 
                       3, ["theory", "foundation"], [], 4, "theory", "markdown", 85, False,
                       "流计算的数学形式化定义与基本概念"),
            ContentItem("s-02-01", "一致性层次结构", "Struct/02-properties/02.02-consistency-hierarchy.md",
                       3, ["theory", "consistency"], ["s-01-01"], 3, "theory", "markdown", 90, False,
                       "流处理中的一致性模型层次结构"),
            ContentItem("s-02-02", "Watermark单调性定理", "Struct/02-properties/02.03-watermark-monotonicity.md",
                       4, ["theory", "time", "watermark"], ["s-01-01"], 4, "theory", "markdown", 88, False,
                       "Watermark机制的形式化分析与证明"),
            ContentItem("s-04-01", "Checkpoint正确性证明", "Struct/04-proofs/04.01-flink-checkpoint-correctness.md",
                       5, ["theory", "checkpoint", "fault-tolerance"], ["s-02-01"], 6, "theory", "markdown", 82, False,
                       "Flink Checkpoint机制的形式化正确性证明"),
            ContentItem("s-04-02", "Exactly-Once语义正确性", "Struct/04-proofs/04.02-flink-exactly-once-correctness.md",
                       5, ["theory", "exactly-once", "semantics"], ["s-04-01"], 6, "theory", "markdown", 80, False,
                       "Exactly-Once语义的形式化定义与正确性证明"),
        ]
        
        # Knowledge/ - 工程知识内容
        knowledge_content = [
            ContentItem("k-01-01", "流处理模型思维导图", "Knowledge/01-concept-atlas/streaming-models-mindmap.md",
                       2, ["engineering", "concept"], [], 2, "engineering", "markdown", 95, False,
                       "流处理核心概念的视觉化梳理"),
            ContentItem("k-01-02", "数据流全景图2026", "Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md",
                       2, ["engineering", "landscape"], [], 3, "engineering", "markdown", 92, True,
                       "2026年数据流处理技术全景分析"),
            ContentItem("k-02-01", "事件时间处理模式", "Knowledge/02-design-patterns/pattern-event-time-processing.md",
                       3, ["engineering", "pattern", "time"], ["k-01-01"], 3, "engineering", "markdown", 88, False,
                       "事件时间处理的设计模式与最佳实践"),
            ContentItem("k-02-02", "窗口聚合模式", "Knowledge/02-design-patterns/pattern-windowed-aggregation.md",
                       2, ["engineering", "pattern", "window"], ["k-01-01"], 2, "engineering", "markdown", 85, False,
                       "窗口化聚合计算的设计模式"),
            ContentItem("k-02-03", "有状态计算模式", "Knowledge/02-design-patterns/pattern-stateful-computation.md",
                       3, ["engineering", "pattern", "state"], ["k-02-02"], 4, "engineering", "markdown", 87, False,
                       "有状态流处理的设计模式"),
            ContentItem("k-03-01", "IoT流处理业务模型", "Knowledge/03-business-patterns/iot-stream-processing.md",
                       3, ["engineering", "business", "iot"], ["k-02-01"], 3, "engineering", "markdown", 78, False,
                       "IoT场景下的流处理业务建模"),
            ContentItem("k-04-01", "流处理引擎选型指南", "Knowledge/04-technology-selection/engine-selection-guide.md",
                       3, ["engineering", "selection", "architecture"], ["k-01-01"], 4, "engineering", "markdown", 90, False,
                       "流处理引擎的技术选型方法论"),
            ContentItem("k-09-01", "反模式检查清单", "Knowledge/09-anti-patterns/anti-pattern-checklist.md",
                       2, ["engineering", "anti-pattern", "best-practice"], ["k-02-01"], 2, "engineering", "markdown", 93, False,
                       "流处理常见反模式与避免方法"),
            ContentItem("k-98-01", "Flink基础练习", "Knowledge/98-exercises/exercise-02-flink-basics.md",
                       2, ["engineering", "exercise", "flink"], [], 4, "engineering", "exercise", 86, False,
                       "Flink基础编程练习集"),
            ContentItem("k-98-02", "Checkpoint分析练习", "Knowledge/98-exercises/exercise-03-checkpoint-analysis.md",
                       3, ["engineering", "exercise", "checkpoint"], ["k-98-01"], 3, "engineering", "exercise", 75, False,
                       "Checkpoint机制分析练习"),
        ]
        
        # Flink/ - Flink实践内容
        flink_content = [
            ContentItem("f-01-01", "部署架构", "Flink/01-architecture/deployment-architectures.md",
                       2, ["flink", "architecture", "deployment"], [], 2, "flink", "markdown", 88, False,
                       "Flink部署架构详解"),
            ContentItem("f-02-01", "Checkpoint机制深入", "Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md",
                       3, ["flink", "checkpoint", "fault-tolerance"], ["f-01-01"], 4, "flink", "markdown", 95, False,
                       "Flink Checkpoint机制的深入解析"),
            ContentItem("f-02-02", "Exactly-Once语义深入", "Flink/02-core-mechanisms/exactly-once-semantics-deep-dive.md",
                       3, ["flink", "exactly-once", "semantics"], ["f-02-01"], 4, "flink", "markdown", 92, False,
                       "Flink Exactly-Once语义实现详解"),
            ContentItem("f-02-03", "时间语义与Watermark", "Flink/02-core-mechanisms/time-semantics-and-watermark.md",
                       3, ["flink", "time", "watermark"], ["f-01-01"], 3, "flink", "markdown", 90, False,
                       "Flink时间语义与Watermark机制"),
            ContentItem("f-02-04", "状态后端选型", "Flink/02-core-mechanisms/state-backend-selection.md",
                       3, ["flink", "state", "backend"], ["f-02-01"], 3, "flink", "markdown", 85, False,
                       "Flink状态后端的选择与配置"),
            ContentItem("f-02-05", "反压与流控", "Flink/02-core-mechanisms/backpressure-and-flow-control.md",
                       4, ["flink", "backpressure", "performance"], ["f-02-01"], 4, "flink", "markdown", 87, False,
                       "Flink反压机制与流量控制"),
            ContentItem("f-03-01", "Flink SQL窗口函数", "Flink/03-sql-table-api/flink-sql-window-functions-deep-dive.md",
                       3, ["flink", "sql", "window"], ["f-01-01"], 3, "flink", "markdown", 84, False,
                       "Flink SQL窗口函数详解"),
            ContentItem("f-03-02", "物化表", "Flink/03-sql-table-api/materialized-tables.md",
                       3, ["flink", "sql", "materialized"], ["f-03-01"], 3, "flink", "markdown", 80, True,
                       "Flink物化表概念与应用"),
            ContentItem("f-04-01", "Kafka集成模式", "Flink/04-connectors/kafka-integration-patterns.md",
                       3, ["flink", "connector", "kafka"], ["f-01-01"], 3, "flink", "markdown", 89, False,
                       "Flink与Kafka集成的高级模式"),
            ContentItem("f-04-02", "CDC 3.0数据集成", "Flink/04-connectors/flink-cdc-3.0-data-integration.md",
                       3, ["flink", "cdc", "integration"], ["f-04-01"], 4, "flink", "markdown", 91, True,
                       "Flink CDC 3.0数据集成方案"),
            ContentItem("f-06-01", "性能调优指南", "Flink/06-engineering/performance-tuning-guide.md",
                       4, ["flink", "performance", "tuning"], ["f-02-05"], 5, "flink", "markdown", 88, False,
                       "Flink作业性能调优完整指南"),
            ContentItem("f-07-01", "实时分析案例", "Flink/07-case-studies/case-realtime-analytics.md",
                       3, ["flink", "case-study", "analytics"], ["f-03-01"], 3, "flink", "markdown", 86, False,
                       "实时数据分析Flink案例"),
            ContentItem("f-07-02", "电商实时推荐", "Flink/07-case-studies/case-ecommerce-realtime-recommendation.md",
                       4, ["flink", "case-study", "recommendation", "ecommerce"], ["f-07-01"], 4, "flink", "markdown", 87, False,
                       "电商实时推荐系统Flink案例"),
            ContentItem("f-10-01", "Kubernetes部署", "Flink/10-deployment/kubernetes-deployment.md",
                       3, ["flink", "deployment", "kubernetes"], ["f-01-01"], 4, "flink", "markdown", 85, False,
                       "Flink on Kubernetes部署指南"),
        ]
        
        # 预定义学习路径
        predefined_paths = [
            ContentItem("lp-01", "零基础入门", "LEARNING-PATHS/beginner-zero-foundation.md",
                       1, ["path", "beginner"], [], 0, "path", "markdown", 95, False,
                       "完全新手的流处理入门路径"),
            ContentItem("lp-02", "有基础入门", "LEARNING-PATHS/beginner-with-foundation.md",
                       2, ["path", "beginner"], [], 0, "path", "markdown", 88, False,
                       "有经验开发者的快速入门"),
            ContentItem("lp-03", "DataStream专家", "LEARNING-PATHS/intermediate-datastream-expert.md",
                       3, ["path", "intermediate", "datastream"], ["lp-02"], 0, "path", "markdown", 82, False,
                       "DataStream API专家路径"),
            ContentItem("lp-04", "SQL专家", "LEARNING-PATHS/intermediate-sql-expert.md",
                       3, ["path", "intermediate", "sql"], ["lp-02"], 0, "path", "markdown", 80, False,
                       "Flink SQL专家路径"),
            ContentItem("lp-05", "架构师路径", "LEARNING-PATHS/expert-architect-path.md",
                       5, ["path", "expert", "architecture"], ["lp-03"], 0, "path", "markdown", 78, False,
                       "流处理架构师成长路径"),
            ContentItem("lp-06", "研究员路径", "LEARNING-PATHS/researcher-path.md",
                       5, ["path", "expert", "research"], ["lp-03"], 0, "path", "markdown", 75, False,
                       "流计算理论研究路径"),
            ContentItem("lp-07", "面试准备", "LEARNING-PATHS/interview-prep-path.md",
                       3, ["path", "interview"], ["lp-03"], 0, "path", "markdown", 92, False,
                       "流处理面试准备路径"),
        ]
        
        all_content = struct_content + knowledge_content + flink_content + predefined_paths
        for item in all_content:
            self.items[item.id] = item
    
    def get_by_difficulty(self, min_level: int, max_level: int) -> List[ContentItem]:
        """按难度获取内容"""
        return [item for item in self.items.values() 
                if min_level <= item.difficulty <= max_level]
    
    def get_by_topic(self, topic: str) -> List[ContentItem]:
        """按主题获取内容"""
        return [item for item in self.items.values() if topic in item.topics]
    
    def get_by_type(self, content_type: str) -> List[ContentItem]:
        """按类型获取内容"""
        return [item for item in self.items.values() if item.content_type == content_type]
    
    def get_popular(self, limit: int = 10) -> List[ContentItem]:
        """获取热门内容"""
        return sorted(self.items.values(), key=lambda x: x.popularity, reverse=True)[:limit]
    
    def get_new(self, limit: int = 5) -> List[ContentItem]:
        """获取新内容"""
        return [item for item in self.items.values() if item.is_new][:limit]
    
    def resolve_dependencies(self, item_ids: List[str]) -> List[str]:
        """解析依赖关系，返回拓扑排序后的ID列表"""
        visited = set()
        result = []
        temp_mark = set()
        
        def visit(item_id: str):
            if item_id in temp_mark:
                return  # 循环依赖，跳过
            if item_id in visited:
                return
            if item_id not in self.items:
                return
            
            temp_mark.add(item_id)
            item = self.items[item_id]
            for prereq in item.prerequisites:
                visit(prereq)
            temp_mark.remove(item_id)
            visited.add(item_id)
            result.append(item_id)
        
        for item_id in item_ids:
            visit(item_id)
        
        return result


class RecommendationEngine:
    """推荐引擎"""
    
    def __init__(self, content_library: ContentLibrary):
        self.library = content_library
        self.user_feedback: Dict[str, Dict] = defaultdict(dict)
    
    def _get_difficulty_range(self, profile: UserProfile) -> Tuple[int, int]:
        """根据经验等级获取难度范围"""
        ranges = {
            Experience.BEGINNER: (1, 3),
            Experience.INTERMEDIATE: (2, 4),
            Experience.ADVANCED: (3, 6)
        }
        return ranges.get(profile.experience, (1, 3))
    
    def _get_time_budget(self, profile: UserProfile) -> float:
        """根据时间框架获取总学习时间预算"""
        timeframe_hours = {
            TimeFrame.SHORT: 40,      # 1周
            TimeFrame.MEDIUM: 160,    # 1月
            TimeFrame.LONG: 480       # 3月
        }
        return timeframe_hours.get(profile.timeframe, 160)
    
    def _score_content(self, item: ContentItem, profile: UserProfile) -> float:
        """为内容项打分"""
        score = 0.0
        
        # 目标匹配度
        goal_preferences = {
            Goal.THEORY: ["theory"],
            Goal.PRACTICE: ["engineering", "flink"],
            Goal.INTERVIEW: ["engineering", "flink", "pattern"],
            Goal.RESEARCH: ["theory", "frontier"]
        }
        preferred_topics = goal_preferences.get(profile.goal, [])
        for topic in item.topics:
            if topic in preferred_topics:
                score += 10
        
        # 角色匹配度
        role_preferences = {
            Role.STUDENT: ["foundation", "concept", "exercise"],
            Role.DEVELOPER: ["engineering", "flink", "pattern", "case-study"],
            Role.ARCHITECT: ["architecture", "selection", "pattern", "case-study"],
            Role.RESEARCHER: ["theory", "frontier", "proof"]
        }
        preferred_topics = role_preferences.get(profile.role, [])
        for topic in item.topics:
            if topic in preferred_topics:
                score += 8
        
        # 兴趣匹配
        for interest in profile.interests:
            if interest in item.topics:
                score += 5
        
        # 热门度加成
        score += item.popularity * 0.05
        
        # 新内容加成
        if item.is_new:
            score += 3
        
        # 格式偏好
        if item.format in profile.preferred_formats:
            score += 2
        
        return score
    
    def generate_path(self, profile: UserProfile, path_type: PathType = PathType.BALANCED) -> LearningPath:
        """生成学习路径"""
        difficulty_min, difficulty_max = self._get_difficulty_range(profile)
        time_budget = self._get_time_budget(profile)
        
        # 获取候选内容
        candidates = self.library.get_by_difficulty(difficulty_min, difficulty_max)
        
        # 排除已知内容
        candidates = [c for c in candidates if c.id not in profile.known_topics]
        
        # 按相关度打分并排序
        scored = [(self._score_content(c, profile), c) for c in candidates]
        scored.sort(key=lambda x: x[0], reverse=True)
        
        # 根据路径类型选择内容
        if path_type == PathType.SHORTEST:
            # 最短路径：选择核心且时间短的
            selected = self._select_shortest_path(scored, time_budget)
        elif path_type == PathType.COMPREHENSIVE:
            # 全面路径：尽可能覆盖所有相关主题
            selected = self._select_comprehensive_path(scored, time_budget)
        else:
            # 平衡路径
            selected = self._select_balanced_path(scored, time_budget)
        
        # 解析依赖
        selected_ids = [item.id for _, item in selected]
        ordered_ids = self.library.resolve_dependencies(selected_ids)
        selected_items = [self.library.items[id] for id in ordered_ids if id in self.library.items]
        
        # 分阶段
        stages = self._organize_stages(selected_items, profile)
        
        # 生成检查点
        checkpoints = self._generate_checkpoints(stages, profile)
        
        # 计算总时间
        total_hours = sum(item.estimated_hours for item in selected_items)
        
        # 生成路径描述
        description = self._generate_description(profile, path_type, total_hours)
        
        # 生成路径名称
        path_name = self._generate_path_name(profile, path_type)
        
        return LearningPath(
            name=path_name,
            description=description,
            path_type=path_type,
            total_hours=total_hours,
            stages=stages,
            checkpoints=checkpoints,
            recommended_for=[profile.role.value, profile.experience.value, profile.goal.value]
        )
    
    def _select_shortest_path(self, scored: List[Tuple[float, ContentItem]], 
                              time_budget: float) -> List[Tuple[float, ContentItem]]:
        """选择最短路径的内容"""
        selected = []
        total_time = 0
        
        for score, item in scored:
            if total_time + item.estimated_hours <= time_budget * 0.7:  # 70%时间预算，留有余量
                selected.append((score, item))
                total_time += item.estimated_hours
            if total_time >= time_budget * 0.6:  # 达到60%即可
                break
        
        return selected
    
    def _select_comprehensive_path(self, scored: List[Tuple[float, ContentItem]], 
                                   time_budget: float) -> List[Tuple[float, ContentItem]]:
        """选择全面路径的内容"""
        selected = []
        total_time = 0
        topics_covered = set()
        
        for score, item in scored:
            # 优先选择能覆盖新主题的内容
            new_topics = set(item.topics) - topics_covered
            if new_topics or score > 15:  # 高评分或新主题
                if total_time + item.estimated_hours <= time_budget * 1.1:  # 允许稍微超预算
                    selected.append((score, item))
                    total_time += item.estimated_hours
                    topics_covered.update(item.topics)
        
        return selected
    
    def _select_balanced_path(self, scored: List[Tuple[float, ContentItem]], 
                              time_budget: float) -> List[Tuple[float, ContentItem]]:
        """选择平衡路径的内容"""
        selected = []
        total_time = 0
        
        # 首先选择核心内容（高分项）
        for score, item in scored:
            if score >= 15:
                if total_time + item.estimated_hours <= time_budget * 0.5:
                    selected.append((score, item))
                    total_time += item.estimated_hours
        
        # 然后填充其他内容
        for score, item in scored:
            if (score, item) not in selected:
                if total_time + item.estimated_hours <= time_budget * 0.95:
                    selected.append((score, item))
                    total_time += item.estimated_hours
        
        return selected
    
    def _organize_stages(self, items: List[ContentItem], profile: UserProfile) -> List[LearningStage]:
        """将内容组织为学习阶段"""
        stages = []
        
        # 根据内容类型分组
        theory_items = [i for i in items if i.content_type == "theory"]
        eng_items = [i for i in items if i.content_type == "engineering"]
        flink_items = [i for i in items if i.content_type == "flink"]
        
        # 阶段1: 基础概念
        if theory_items or eng_items:
            stage1_items = theory_items[:2] + eng_items[:2]
            stages.append(LearningStage(
                name="基础概念",
                duration_days=7,
                items=stage1_items[:4],
                checkpoints=[
                    "理解流处理与批处理的核心区别",
                    "掌握Event Time与Processing Time的概念"
                ]
            ))
        
        # 阶段2: 核心机制
        if flink_items:
            stages.append(LearningStage(
                name="Flink核心机制",
                duration_days=14,
                items=flink_items[:5],
                checkpoints=[
                    "能够配置和调优Checkpoint",
                    "理解Exactly-Once语义实现原理"
                ]
            ))
        
        # 阶段3: 进阶应用
        remaining = [i for i in items if i not in sum([s.items for s in stages], [])]
        if remaining:
            stages.append(LearningStage(
                name="进阶应用",
                duration_days=14,
                items=remaining[:6],
                checkpoints=[
                    "能够独立完成中等复杂度项目",
                    "掌握性能调优基本方法"
                ]
            ))
        
        return stages
    
    def _generate_checkpoints(self, stages: List[LearningStage], profile: UserProfile) -> List[str]:
        """生成检查点"""
        checkpoints = []
        
        role_checkpoints = {
            Role.STUDENT: [
                "能够解释流处理的基本概念",
                "能够运行和调试Flink示例程序",
                "完成至少一个综合练习项目"
            ],
            Role.DEVELOPER: [
                "能够独立开发Flink DataStream应用",
                "能够诊断和解决常见运行问题",
                "掌握生产环境部署最佳实践"
            ],
            Role.ARCHITECT: [
                "能够设计高可用流处理架构",
                "能够进行合理的技术选型",
                "掌握容量规划和性能评估方法"
            ],
            Role.RESEARCHER: [
                "理解流计算的形式化理论基础",
                "能够阅读和分析相关学术论文",
                "具备独立开展研究的能力"
            ]
        }
        
        goal_checkpoints = {
            Goal.THEORY: ["掌握核心理论的数学基础"],
            Goal.PRACTICE: ["具备生产环境实战能力"],
            Goal.INTERVIEW: ["能够回答技术面试常见问题"],
            Goal.RESEARCH: ["能够撰写技术研究文档"]
        }
        
        checkpoints.extend(role_checkpoints.get(profile.role, []))
        checkpoints.extend(goal_checkpoints.get(profile.goal, []))
        
        # 添加阶段检查点
        for stage in stages:
            checkpoints.extend(stage.checkpoints)
        
        return checkpoints
    
    def _generate_description(self, profile: UserProfile, path_type: PathType, total_hours: float) -> str:
        """生成路径描述"""
        descriptions = {
            PathType.SHORTEST: f"为{profile.role.value}设计的快速学习路径，重点覆盖核心概念，预计{total_hours:.0f}小时",
            PathType.COMPREHENSIVE: f"为{profile.role.value}设计的全面学习路径，涵盖流处理各方面知识，预计{total_hours:.0f}小时",
            PathType.BALANCED: f"为{profile.role.value}设计的平衡学习路径，理论与实践并重，预计{total_hours:.0f}小时"
        }
        return descriptions.get(path_type, descriptions[PathType.BALANCED])
    
    def _generate_path_name(self, profile: UserProfile, path_type: PathType) -> str:
        """生成路径名称"""
        type_names = {
            PathType.SHORTEST: "快速入门",
            PathType.COMPREHENSIVE: "全面精通",
            PathType.BALANCED: "系统学习"
        }
        role_names = {
            Role.STUDENT: "学生",
            Role.DEVELOPER: "开发者",
            Role.ARCHITECT: "架构师",
            Role.RESEARCHER: "研究员"
        }
        return f"{role_names.get(profile.role, '学习者')}{type_names.get(path_type, '学习')}路径"
    
    def get_recommendations(self, profile: UserProfile, 
                           recommendation_type: str = "personalized") -> List[Dict]:
        """获取推荐内容"""
        recommendations = []
        
        if recommendation_type == "popular":
            # 热门推荐
            items = self.library.get_popular(10)
            for item in items:
                recommendations.append({
                    "type": "popular",
                    "item": item.to_dict(),
                    "reason": f"热门度: {item.popularity}"
                })
        
        elif recommendation_type == "new":
            # 新内容推荐
            items = self.library.get_new(5)
            for item in items:
                recommendations.append({
                    "type": "new",
                    "item": item.to_dict(),
                    "reason": "新发布内容"
                })
        
        else:
            # 个性化推荐
            difficulty_min, difficulty_max = self._get_difficulty_range(profile)
            candidates = self.library.get_by_difficulty(difficulty_min, difficulty_max)
            candidates = [c for c in candidates if c.id not in profile.known_topics]
            
            scored = [(self._score_content(c, profile), c) for c in candidates]
            scored.sort(key=lambda x: x[0], reverse=True)
            
            for score, item in scored[:10]:
                recommendations.append({
                    "type": "personalized",
                    "item": item.to_dict(),
                    "score": round(score, 2),
                    "reason": f"匹配度评分: {score:.1f}"
                })
        
        return recommendations
    
    def record_feedback(self, user_id: str, item_id: str, feedback: str, rating: int):
        """记录用户反馈"""
        self.user_feedback[user_id][item_id] = {
            "feedback": feedback,
            "rating": rating,
            "timestamp": "2026-04-04"
        }


class OutputGenerator:
    """输出生成器"""
    
    @staticmethod
    def to_markdown(path: LearningPath) -> str:
        """生成Markdown格式的学习路径"""
        md = f"""# {path.name}

> **路径类型**: {path.path_type.value} | **预计总时长**: {path.total_hours:.0f}小时 | **生成日期**: {path.created_at}

## 路径概述

{path.description}

### 适合人群

"""
        for target in path.recommended_for:
            md += f"- {target}\n"
        
        md += f"""
### 学习阶段 ({len(path.stages)}个阶段)

| 阶段 | 时长 | 内容数 | 预计学时 |
|------|------|--------|----------|
"""
        for i, stage in enumerate(path.stages, 1):
            md += f"| {stage.name} | {stage.duration_days}天 | {len(stage.items)} | {stage.total_hours():.1f}h |\n"
        
        md += """
---

## 详细学习内容

"""
        for i, stage in enumerate(path.stages, 1):
            md += f"""### 阶段{i}: {stage.name}

**时间安排**: {stage.duration_days}天 | **预计学时**: {stage.total_hours():.1f}小时

#### 学习清单

| 序号 | 内容 | 难度 | 类型 | 预计时间 | 路径 |
|------|------|------|------|----------|------|
"""
            for j, item in enumerate(stage.items, 1):
                md += f"| {j} | {item.title} | L{item.difficulty} | {item.content_type} | {item.estimated_hours}h | `{item.path}` |\n"
            
            md += f"""
#### 阶段检查点

"""
            for checkpoint in stage.checkpoints:
                md += f"- [ ] {checkpoint}\n"
            
            md += "\n---\n\n"
        
        md += """## 总体检查点

"""
        for checkpoint in path.checkpoints:
            md += f"- [ ] {checkpoint}\n"
        
        md += """
---

## 学习进度跟踪

```markdown
### 周进度记录

| 周次 | 计划内容 | 完成情况 | 遇到的问题 | 备注 |
|------|----------|----------|------------|------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

### 月度总结

**本月完成内容**:
- 

**主要收获**:
- 

**下月计划**:
- 
```

---

*此学习路径由动态推荐系统生成*
"""
        return md
    
    @staticmethod
    def to_json(path: LearningPath) -> str:
        """生成JSON格式的学习路径"""
        return json.dumps(path.to_dict(), ensure_ascii=False, indent=2)
    
    @staticmethod
    def to_checklist(path: LearningPath) -> str:
        """生成纯检查清单格式"""
        checklist = f"# {path.name} - 学习检查清单\n\n"
        
        for i, stage in enumerate(path.stages, 1):
            checklist += f"## 阶段{i}: {stage.name}\n\n"
            for item in stage.items:
                checklist += f"- [ ] {item.title} ({item.estimated_hours}h) - `{item.path}`\n"
            checklist += "\n"
        
        checklist += "## 检查点\n\n"
        for checkpoint in path.checkpoints:
            checklist += f"- [ ] {checkpoint}\n"
        
        return checklist


class InteractiveCLI:
    """交互式命令行界面"""
    
    def __init__(self):
        self.library = ContentLibrary()
        self.engine = RecommendationEngine(self.library)
        self.output = OutputGenerator()
    
    def run(self):
        """运行交互式界面"""
        print("=" * 60)
        print("  AnalysisDataFlow 动态学习路径推荐系统")
        print("=" * 60)
        print()
        
        # 收集用户信息
        profile = self._collect_profile()
        
        print("\n" + "=" * 60)
        print("  正在生成个性化学习路径...")
        print("=" * 60 + "\n")
        
        # 生成三种类型的路径供选择
        paths = {
            "shortest": self.engine.generate_path(profile, PathType.SHORTEST),
            "balanced": self.engine.generate_path(profile, PathType.BALANCED),
            "comprehensive": self.engine.generate_path(profile, PathType.COMPREHENSIVE)
        }
        
        # 显示路径选择
        print("为您生成了以下学习路径选项:\n")
        for key, path in paths.items():
            print(f"[{key}]")
            print(f"  名称: {path.name}")
            print(f"  描述: {path.description}")
            print(f"  总时长: {path.total_hours:.0f}小时")
            print(f"  阶段数: {len(path.stages)}")
            print()
        
        # 选择路径
        choice = input("请选择路径类型 (shortest/balanced/comprehensive): ").strip().lower()
        selected_path = paths.get(choice, paths["balanced"])
        
        # 选择输出格式
        format_choice = input("\n选择输出格式 (markdown/json/checklist): ").strip().lower()
        
        # 生成输出
        if format_choice == "json":
            output = self.output.to_json(selected_path)
            ext = "json"
        elif format_choice == "checklist":
            output = self.output.to_checklist(selected_path)
            ext = "md"
        else:
            output = self.output.to_markdown(selected_path)
            ext = "md"
        
        # 保存文件
        filename = f"learning-path-{profile.role.value}-{selected_path.path_type.value}.{ext}"
        filepath = os.path.join("LEARNING-PATHS", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f"\n✅ 学习路径已保存至: {filepath}")
        
        # 是否显示推荐
        show_recommendations = input("\n是否查看个性化推荐内容? (y/n): ").strip().lower()
        if show_recommendations == 'y':
            self._show_recommendations(profile)
    
    def _collect_profile(self) -> UserProfile:
        """收集用户画像信息"""
        print("请回答以下问题以生成个性化学习路径:\n")
        
        # 角色
        print("1. 您的角色是?")
        print("   [1] 学生 (student)")
        print("   [2] 开发者 (developer)")
        print("   [3] 架构师 (architect)")
        print("   [4] 研究员 (researcher)")
        role_choice = input("   选择 (1-4): ").strip()
        roles = {"1": Role.STUDENT, "2": Role.DEVELOPER, "3": Role.ARCHITECT, "4": Role.RESEARCHER}
        role = roles.get(role_choice, Role.STUDENT)
        
        # 经验
        print("\n2. 您的经验水平是?")
        print("   [1] 初级 (beginner)")
        print("   [2] 中级 (intermediate)")
        print("   [3] 高级 (advanced)")
        exp_choice = input("   选择 (1-3): ").strip()
        exps = {"1": Experience.BEGINNER, "2": Experience.INTERMEDIATE, "3": Experience.ADVANCED}
        experience = exps.get(exp_choice, Experience.BEGINNER)
        
        # 目标
        print("\n3. 您的学习目标是?")
        print("   [1] 理论学习 (theory)")
        print("   [2] 工程实践 (practice)")
        print("   [3] 面试准备 (interview)")
        print("   [4] 学术研究 (research)")
        goal_choice = input("   选择 (1-4): ").strip()
        goals = {"1": Goal.THEORY, "2": Goal.PRACTICE, "3": Goal.INTERVIEW, "4": Goal.RESEARCH}
        goal = goals.get(goal_choice, Goal.PRACTICE)
        
        # 时间
        print("\n4. 您的时间安排是?")
        print("   [1] 短期 (1周)")
        print("   [2] 中期 (1月)")
        print("   [3] 长期 (3月)")
        time_choice = input("   选择 (1-3): ").strip()
        times = {"1": TimeFrame.SHORT, "2": TimeFrame.MEDIUM, "3": TimeFrame.LONG}
        timeframe = times.get(time_choice, TimeFrame.MEDIUM)
        
        # 每周学习小时
        hours = input("\n5. 您每周可投入多少小时学习? (默认10): ").strip()
        weekly_hours = int(hours) if hours.isdigit() else 10
        
        # 兴趣标签
        print("\n6. 您感兴趣的主题标签 (用逗号分隔，可选):")
        print("   可选: theory, engineering, flink, kafka, checkpoint, state, sql, performance")
        interests_input = input("   输入: ").strip()
        interests = [i.strip() for i in interests_input.split(",") if i.strip()]
        
        return UserProfile(
            role=role,
            experience=experience,
            goal=goal,
            timeframe=timeframe,
            weekly_hours=weekly_hours,
            interests=interests
        )
    
    def _show_recommendations(self, profile: UserProfile):
        """显示推荐内容"""
        print("\n" + "=" * 60)
        print("  个性化推荐内容")
        print("=" * 60 + "\n")
        
        recommendations = self.engine.get_recommendations(profile, "personalized")
        
        print(f"基于您的画像 ({profile.role.value}, {profile.experience.value}, {profile.goal.value}):\n")
        
        for i, rec in enumerate(recommendations[:5], 1):
            item = rec["item"]
            print(f"{i}. {item['title']}")
            print(f"   难度: L{item['difficulty']} | 时间: {item['estimated_hours']}h | {rec['reason']}")
            print(f"   路径: {item['path']}")
            print()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="动态学习路径推荐系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互式模式
  python learning-path-recommender.py
  
  # 从配置文件生成
  python learning-path-recommender.py --config profile.json --output my-path.md
  
  # 生成热门推荐
  python learning-path-recommender.py --recommend popular --output recommendations.md
        """
    )
    
    parser.add_argument("--config", "-c", help="用户配置文件路径 (JSON)")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--format", "-f", choices=["markdown", "json", "checklist"], 
                       default="markdown", help="输出格式")
    parser.add_argument("--path-type", "-t", choices=["shortest", "balanced", "comprehensive"],
                       default="balanced", help="路径类型")
    parser.add_argument("--recommend", "-r", choices=["personalized", "popular", "new"],
                       help="生成推荐列表而非学习路径")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="强制使用交互式模式")
    parser.add_argument("--web", "-w", action="store_true",
                       help="启动Web服务器模式")
    
    args = parser.parse_args()
    
    # 创建核心组件
    library = ContentLibrary()
    engine = RecommendationEngine(library)
    output_gen = OutputGenerator()
    
    # Web模式
    if args.web:
        print("启动Web服务器模式...")
        print("请在浏览器中访问: http://localhost:8080")
        # 这里可以集成Flask/FastAPI，当前版本仅作预留
        return
    
    # 交互式模式
    if args.interactive or (not args.config and not args.recommend):
        cli = InteractiveCLI()
        cli.run()
        return
    
    # 配置文件模式
    if args.config:
        with open(args.config, 'r', encoding='utf-8-sig') as f:
            profile_data = json.load(f)
        profile = UserProfile.from_dict(profile_data)
    else:
        # 默认画像
        profile = UserProfile(
            role=Role.DEVELOPER,
            experience=Experience.INTERMEDIATE,
            goal=Goal.PRACTICE,
            timeframe=TimeFrame.MEDIUM
        )
    
    # 生成推荐或路径
    if args.recommend:
        recommendations = engine.get_recommendations(profile, args.recommend)
        output = json.dumps(recommendations, ensure_ascii=False, indent=2)
    else:
        path_type = PathType(args.path_type)
        path = engine.generate_path(profile, path_type)
        
        if args.format == "json":
            output = output_gen.to_json(path)
        elif args.format == "checklist":
            output = output_gen.to_checklist(path)
        else:
            output = output_gen.to_markdown(path)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"输出已保存至: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
