#!/usr/bin/env python3
"""
个性化学习路径生成器 - 基于用户目标推荐学习路线
功能：
1. 分析用户目标和技术背景
2. 生成个性化学习路径
3. 推荐相关文档和资源
4. 估算学习时间和难度

用法：
    python learning-path-personalizer.py --goal "成为Flink专家" --background "Java后端3年"
    python learning-path-personalizer.py --goal "理解流计算理论" --level beginner
    python learning-path-personalizer.py --interactive
    python learning-path-personalizer.py --list-goals
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum

# 尝试导入可选依赖
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class SkillLevel(Enum):
    """技能水平"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class LearningNode:
    """学习节点"""
    id: str
    title: str
    doc_path: str
    difficulty: int  # 1-10
    estimated_hours: float
    prerequisites: List[str]
    outcomes: List[str]
    resources: List[Dict[str, str]]


@dataclass
class LearningPath:
    """学习路径"""
    name: str
    description: str
    target_audience: str
    total_hours: float
    difficulty_distribution: Dict[str, int]
    phases: List[Dict]
    nodes: List[LearningNode]
    milestones: List[Dict]


class LearningPathGenerator:
    """学习路径生成器"""
    
    # 预定义的学习目标模板
    GOAL_TEMPLATES = {
        "flink-developer": {
            "name": "Flink开发工程师",
            "description": "掌握Flink应用开发，能够独立开发和优化流处理作业",
            "prerequisites": ["Java/Scala基础", "基础分布式概念"],
            "core_topics": [
                "Flink架构概览",
                "DataStream API",
                "时间语义与Watermark",
                "状态管理",
                "Checkpoint与容错",
                "窗口操作",
                "Connector使用",
                "性能调优"
            ],
            "estimated_hours": 120
        },
        "streaming-architect": {
            "name": "流计算架构师",
            "description": "深入理解流计算理论和Flink内核，能够设计大规模流处理系统",
            "prerequisites": ["分布式系统经验", "流计算基础", "架构设计经验"],
            "core_topics": [
                "统一流计算理论",
                "进程演算基础",
                "一致性模型",
                "Flink内部架构",
                "Checkpoint算法",
                "Exactly-Once语义",
                "状态后端设计",
                "资源调度"
            ],
            "estimated_hours": 200
        },
        "data-engineer": {
            "name": "流式数据工程师",
            "description": "掌握流数据处理 pipeline 构建，熟悉SQL和实时数仓",
            "prerequisites": ["SQL基础", "数据处理经验"],
            "core_topics": [
                "Flink SQL基础",
                "Table API",
                "流批一体概念",
                "实时数仓设计",
                "CDC数据集成",
                "Lakehouse架构",
                "数据质量保证"
            ],
            "estimated_hours": 100
        },
        "researcher": {
            "name": "流计算研究员",
            "description": "深入流计算理论，能够进行形式化分析和创新研究",
            "prerequisites": ["形式化方法基础", "编程语言理论", "数学基础"],
            "core_topics": [
                "进程演算",
                "Actor模型形式化",
                "类型理论",
                "一致性层次",
                "形式化验证",
                "表达能力分析",
                "开源问题"
            ],
            "estimated_hours": 300
        }
    }
    
    # 文档库映射
    DOC_LIBRARY = {
        # 基础理论
        "统一流计算理论": "Struct/01-foundation/01.01-unified-streaming-theory.md",
        "进程演算基础": "Struct/01-foundation/01.02-process-calculus-primer.md",
        "Actor模型形式化": "Struct/01-foundation/01.03-actor-model-formalization.md",
        "Dataflow模型": "Struct/01-foundation/01.04-dataflow-model-formalization.md",
        
        # 性质与证明
        "确定性": "Struct/02-properties/02.01-determinism-in-streaming.md",
        "一致性层级": "Struct/02-properties/02.02-consistency-hierarchy.md",
        "Watermark单调性": "Struct/02-properties/02.03-watermark-monotonicity.md",
        "Checkpoint正确性": "Struct/04-proofs/04.01-flink-checkpoint-correctness.md",
        "Exactly-Once正确性": "Struct/04-proofs/04.02-flink-exactly-once-correctness.md",
        
        # Flink核心
        "Flink架构概览": "Flink/01-architecture/flink-architecture-overview.md",
        "DataStream API": "Flink/09-language-foundations/datastream-api-guide.md",
        "时间语义与Watermark": "Flink/02-core-mechanisms/time-semantics-and-watermark.md",
        "状态管理": "Flink/02-core-mechanisms/state-management-deep-dive.md",
        "Checkpoint机制": "Flink/02-core-mechanisms/checkpoint-mechanism-deep-dive.md",
        "窗口操作": "Flink/03-sql-table-api/windows-guide.md",
        "Flink SQL基础": "Flink/03-sql-table-api/flink-sql-quickstart.md",
        
        # 设计模式
        "事件时间处理": "Knowledge/02-design-patterns/pattern-event-time-processing.md",
        "状态管理模式": "Knowledge/02-design-patterns/pattern-state-management.md",
        "容错设计": "Knowledge/02-design-patterns/pattern-fault-tolerance.md",
    }
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.user_profile = {}
    
    def analyze_goal(self, goal: str, background: str, level: str) -> Dict:
        """分析用户目标"""
        # 简单启发式匹配
        goal_lower = goal.lower()
        background_lower = background.lower()
        
        matched_goals = []
        
        if any(kw in goal_lower for kw in ['开发', 'developer', 'engineer', 'programming']):
            matched_goals.append('flink-developer')
        
        if any(kw in goal_lower for kw in ['架构', 'architect', 'design', 'system']):
            matched_goals.append('streaming-architect')
        
        if any(kw in goal_lower for kw in ['数据', 'data', 'sql', 'etl', 'pipeline']):
            matched_goals.append('data-engineer')
        
        if any(kw in goal_lower for kw in ['研究', 'research', '理论', 'theory', 'phd']):
            matched_goals.append('researcher')
        
        # 如果没有匹配，默认选择开发者路径
        if not matched_goals:
            matched_goals = ['flink-developer']
        
        return {
            'primary_goal': matched_goals[0],
            'matched_templates': matched_goals,
            'skill_level': level,
            'background_analysis': self._analyze_background(background)
        }
    
    def _analyze_background(self, background: str) -> Dict:
        """分析技术背景"""
        bg_lower = background.lower()
        
        analysis = {
            'has_distributed_exp': any(kw in bg_lower for kw in ['分布式', 'distributed', 'kafka', 'spark']),
            'has_java_exp': any(kw in bg_lower for kw in ['java', 'scala', 'jvm']),
            'has_sql_exp': any(kw in bg_lower for kw in ['sql', 'database', 'hive']),
            'years_exp': self._extract_years(background)
        }
        
        return analysis
    
    def _extract_years(self, text: str) -> int:
        """提取工作年限"""
        import re
        match = re.search(r'(\d+)\s*年', text)
        if match:
            return int(match.group(1))
        match = re.search(r'(\d+)\s*years?', text)
        if match:
            return int(match.group(1))
        return 0
    
    def generate_path(self, goal: str, background: str, level: str = "intermediate") -> LearningPath:
        """生成学习路径"""
        analysis = self.analyze_goal(goal, background, level)
        template = self.GOAL_TEMPLATES.get(analysis['primary_goal'], self.GOAL_TEMPLATES['flink-developer'])
        
        # 根据背景调整
        bg_analysis = analysis['background_analysis']
        
        # 构建学习节点
        nodes = []
        phase_idx = 0
        phases = []
        current_phase_nodes = []
        phase_hours = 0
        
        for topic in template['core_topics']:
            doc_path = self.DOC_LIBRARY.get(topic, f"Knowledge/{topic}.md")
            
            # 估算难度和时间
            difficulty = self._estimate_difficulty(topic, level)
            hours = self._estimate_hours(topic, bg_analysis)
            
            # 跳过过于基础的内容（对有经验的用户）
            if bg_analysis['years_exp'] > 3 and difficulty < 3:
                hours *= 0.5
            
            node = LearningNode(
                id=f"node-{len(nodes)}",
                title=topic,
                doc_path=doc_path,
                difficulty=difficulty,
                estimated_hours=hours,
                prerequisites=self._get_prerequisites(topic),
                outcomes=self._get_outcomes(topic),
                resources=self._get_resources(topic)
            )
            
            nodes.append(node)
            current_phase_nodes.append(node)
            phase_hours += hours
            
            # 每3-4个节点作为一个阶段
            if len(current_phase_nodes) >= 3 or topic == template['core_topics'][-1]:
                phase_idx += 1
                phases.append({
                    'name': f"阶段 {phase_idx}: {self._get_phase_name(phase_idx)}",
                    'nodes': [n.id for n in current_phase_nodes],
                    'estimated_hours': phase_hours,
                    'milestone': self._get_milestone(phase_idx)
                })
                current_phase_nodes = []
                phase_hours = 0
        
        # 计算总时长
        total_hours = sum(n.estimated_hours for n in nodes)
        
        # 难度分布
        difficulty_dist = {'easy': 0, 'medium': 0, 'hard': 0}
        for node in nodes:
            if node.difficulty <= 3:
                difficulty_dist['easy'] += 1
            elif node.difficulty <= 7:
                difficulty_dist['medium'] += 1
            else:
                difficulty_dist['hard'] += 1
        
        return LearningPath(
            name=template['name'],
            description=template['description'],
            target_audience=f"{level} level developers",
            total_hours=total_hours,
            difficulty_distribution=difficulty_dist,
            phases=phases,
            nodes=nodes,
            milestones=self._generate_milestones(phases)
        )
    
    def _estimate_difficulty(self, topic: str, user_level: str) -> int:
        """估算主题难度"""
        difficulty_map = {
            '统一流计算理论': 9,
            '进程演算基础': 8,
            'Actor模型形式化': 8,
            'Checkpoint正确性': 9,
            'Exactly-Once正确性': 9,
            '一致性层级': 7,
            'DataStream API': 4,
            'Flink SQL基础': 3,
            '时间语义与Watermark': 6,
            '状态管理': 6,
            '窗口操作': 5,
        }
        
        base_difficulty = difficulty_map.get(topic, 5)
        
        # 根据用户水平调整
        if user_level == 'beginner':
            base_difficulty = min(10, base_difficulty + 1)
        elif user_level == 'expert':
            base_difficulty = max(1, base_difficulty - 1)
        
        return base_difficulty
    
    def _estimate_hours(self, topic: str, bg_analysis: Dict) -> float:
        """估算学习时间"""
        hours_map = {
            '统一流计算理论': 20,
            '进程演算基础': 15,
            'Actor模型形式化': 15,
            'Checkpoint正确性': 12,
            'Exactly-Once正确性': 12,
            'DataStream API': 10,
            'Flink SQL基础': 8,
            '时间语义与Watermark': 12,
            '状态管理': 15,
        }
        
        base_hours = hours_map.get(topic, 8)
        
        # 根据背景调整
        if bg_analysis['has_distributed_exp']:
            base_hours *= 0.8
        
        return round(base_hours, 1)
    
    def _get_prerequisites(self, topic: str) -> List[str]:
        """获取前置知识"""
        prereqs = {
            'Checkpoint正确性': ['Flink架构概览', '状态管理'],
            'Exactly-Once正确性': ['Checkpoint机制', '一致性层级'],
            '状态管理': ['DataStream API', '时间语义与Watermark'],
            '时间语义与Watermark': ['DataStream API'],
        }
        return prereqs.get(topic, [])
    
    def _get_outcomes(self, topic: str) -> List[str]:
        """获取学习成果"""
        return [
            f"理解{topic}的核心概念",
            f"能够在实际项目中应用{topic}",
            f"能够排查{topic}相关问题"
        ]
    
    def _get_resources(self, topic: str) -> List[Dict[str, str]]:
        """获取学习资源"""
        return [
            {'type': 'document', 'title': f'{topic}文档', 'path': self.DOC_LIBRARY.get(topic, '')},
            {'type': 'practice', 'title': f'{topic}练习题', 'path': f'tutorials/practice/{topic}.md'},
        ]
    
    def _get_phase_name(self, phase_idx: int) -> str:
        """获取阶段名称"""
        names = ['基础入门', '核心概念', '进阶应用', '专家精通']
        return names[min(phase_idx - 1, len(names) - 1)]
    
    def _get_milestone(self, phase_idx: int) -> str:
        """获取里程碑"""
        milestones = [
            '完成基础环境搭建和Hello World',
            '掌握核心API和基础概念',
            '能够独立开发复杂作业',
            '具备性能优化和故障排查能力'
        ]
        return milestones[min(phase_idx - 1, len(milestones) - 1)]
    
    def _generate_milestones(self, phases: List[Dict]) -> List[Dict]:
        """生成里程碑列表"""
        return [
            {
                'phase': p['name'],
                'description': p['milestone'],
                'criteria': [f'完成阶段所有文档阅读', '通过阶段测试']
            }
            for p in phases
        ]
    
    def generate_learning_report(self, path: LearningPath, output_format: str = 'markdown') -> str:
        """生成学习报告"""
        if output_format == 'markdown':
            return self._generate_markdown_report(path)
        elif output_format == 'json':
            return json.dumps(asdict(path), ensure_ascii=False, indent=2)
        else:
            return self._generate_text_report(path)
    
    def _generate_markdown_report(self, path: LearningPath) -> str:
        """生成Markdown格式的学习路径报告"""
        md = f"""# 🎯 个性化学习路径: {path.name}

> {path.description}

## 📊 路径概览

| 指标 | 值 |
|------|-----|
| 总学习时长 | {path.total_hours:.1f} 小时 |
| 学习节点数 | {len(path.nodes)} 个 |
| 难度分布 | 简单:{path.difficulty_distribution['easy']} 中等:{path.difficulty_distribution['medium']} 困难:{path.difficulty_distribution['hard']} |
| 目标受众 | {path.target_audience} |

## 🗺️ 学习路线图

```mermaid
graph LR
    Start([开始]) --> Phase1[阶段1: 基础入门]
    Phase1 --> Phase2[阶段2: 核心概念]
    Phase2 --> Phase3[阶段3: 进阶应用]
    Phase3 --> Phase4[阶段4: 专家精通]
    Phase4 --> End([完成])
    
    style Phase1 fill:#e1f5fe
    style Phase2 fill:#fff3e0
    style Phase3 fill:#f3e5f5
    style Phase4 fill:#e8f5e9
```

## 📚 详细学习计划

"""
        
        for phase in path.phases:
            md += f"\n### {phase['name']}\n\n"
            md += f"**预计时长**: {phase['estimated_hours']:.1f} 小时\n\n"
            md += f"**里程碑**: {phase['milestone']}\n\n"
            md += "**学习内容**:\n\n"
            
            for node_id in phase['nodes']:
                node = next((n for n in path.nodes if n.id == node_id), None)
                if node:
                    difficulty_emoji = '🟢' if node.difficulty <= 3 else '🟡' if node.difficulty <= 7 else '🔴'
                    md += f"- {difficulty_emoji} [{node.title}]({node.doc_path}) - {node.estimated_hours}h\n"
            
            md += "\n"
        
        md += """## 🎓 学习建议

1. **循序渐进**: 按阶段顺序学习，不要跳过前置知识
2. **实践结合**: 每学完一个主题，完成相关练习
3. **定期回顾**: 每周复习已学内容，巩固理解
4. **社区参与**: 参与讨论，解决学习中遇到的问题

## 📈 进度追踪

- [ ] 阶段1完成
- [ ] 阶段2完成
- [ ] 阶段3完成
- [ ] 阶段4完成

---

*本学习路径由AI根据您的目标和背景自动生成*
"""
        
        return md
    
    def _generate_text_report(self, path: LearningPath) -> str:
        """生成纯文本报告"""
        lines = [
            f"="*60,
            f"个性化学习路径: {path.name}",
            f"="*60,
            f"",
            f"描述: {path.description}",
            f"总时长: {path.total_hours:.1f} 小时",
            f"节点数: {len(path.nodes)}",
            f"",
            f"学习阶段:",
        ]
        
        for phase in path.phases:
            lines.append(f"\n  {phase['name']} ({phase['estimated_hours']:.1f}h)")
            for node_id in phase['nodes']:
                node = next((n for n in path.nodes if n.id == node_id), None)
                if node:
                    lines.append(f"    - {node.title} ({node.estimated_hours}h)")
        
        lines.append("\n" + "="*60)
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="个性化学习路径生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --goal "成为Flink专家" --background "Java后端3年"
  %(prog)s --goal "理解流计算理论" --level beginner --output learning-path.md
  %(prog)s --interactive
  %(prog)s --list-goals
        """
    )
    
    parser.add_argument('--goal', '-g', help='学习目标')
    parser.add_argument('--background', '-b', help='技术背景')
    parser.add_argument('--level', '-l', 
                       choices=['beginner', 'intermediate', 'advanced', 'expert'],
                       default='intermediate',
                       help='当前技能水平')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--format', '-f', choices=['markdown', 'json', 'text'],
                       default='markdown', help='输出格式')
    
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='交互模式')
    parser.add_argument('--list-goals', action='store_true',
                       help='列出预设学习目标')
    
    args = parser.parse_args()
    
    generator = LearningPathGenerator()
    
    if args.list_goals:
        print("\n预设学习目标:\n")
        for key, template in generator.GOAL_TEMPLATES.items():
            print(f"  {key}:")
            print(f"    名称: {template['name']}")
            print(f"    描述: {template['description']}")
            print(f"    预计时长: {template['estimated_hours']} 小时\n")
    
    elif args.interactive:
        print("="*60)
        print("🎯 个性化学习路径生成器")
        print("="*60)
        
        print("\n请选择学习目标:")
        for i, (key, template) in enumerate(generator.GOAL_TEMPLATES.items(), 1):
            print(f"  {i}. {template['name']} - {template['description']}")
        
        try:
            choice = int(input("\n输入数字 (1-4): ")) - 1
            goal_key = list(generator.GOAL_TEMPLATES.keys())[choice]
            goal = generator.GOAL_TEMPLATES[goal_key]['name']
        except (ValueError, IndexError):
            goal = input("\n描述你的学习目标: ")
        
        background = input("你的技术背景: ")
        level = input("当前水平 (beginner/intermediate/advanced/expert) [intermediate]: ").strip() or "intermediate"
        
        print(f"\n正在生成学习路径...\n")
        
        path = generator.generate_path(goal, background, level)
        report = generator.generate_learning_report(path, args.format)
        
        print(report)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n报告已保存到: {args.output}")
    
    elif args.goal:
        background = args.background or "有一定编程基础"
        
        print(f"正在生成学习路径: {args.goal}")
        print(f"背景: {background}")
        print(f"水平: {args.level}\n")
        
        path = generator.generate_path(args.goal, background, args.level)
        report = generator.generate_learning_report(path, args.format)
        
        print(report)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n报告已保存到: {args.output}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
