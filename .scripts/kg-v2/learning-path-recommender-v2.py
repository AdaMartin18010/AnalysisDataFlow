#!/usr/bin/env python3
"""
AnalysisDataFlow 知识图谱 v2.0 - 强化学习学习路径推荐器

基于深度强化学习的动态学习路径生成:
1. 使用 DQN/PPO 学习最优推荐策略
2. 用户行为建模 (知识状态、学习偏好、历史交互)
3. 动态路径生成与自适应调整
4. 多目标优化 (学习效率、知识覆盖率、用户满意度)

依赖:
    pip install torch numpy networkx scikit-learn tqdm matplotlib

Usage:
    python learning-path-recommender-v2.py
    python learning-path-recommender-v2.py --goal "Flink Exactly-Once"
    python learning-path-recommender-v2.py --train --epochs 1000
"""

import os
import json
import random
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set, NamedTuple
from dataclasses import dataclass, field
from collections import deque, defaultdict
from datetime import datetime

import numpy as np
import networkx as nx
from tqdm import tqdm

# PyTorch imports
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import torch.nn.functional as F
    from torch.utils.data import Dataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("Warning: PyTorch not available, using simplified Q-learning")


# ============================================
# Configuration
# ============================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_LEARNING_RATE = 0.001
DEFAULT_GAMMA = 0.99  # Discount factor
DEFAULT_EPSILON = 0.1  # Exploration rate
DEFAULT_MEMORY_SIZE = 10000
DEFAULT_BATCH_SIZE = 64


# ============================================
# Data Structures
# ============================================

@dataclass
class UserState:
    """用户学习状态"""
    known_concepts: Set[str] = field(default_factory=set)
    learning_history: List[Dict] = field(default_factory=list)
    difficulty_preference: float = 0.5  # 0=easy, 1=hard
    time_budget: int = 10  # hours per week
    goal_concepts: Set[str] = field(default_factory=set)
    
    def to_vector(self, all_concepts: List[str]) -> np.ndarray:
        """将状态转换为向量表示"""
        return np.array([1 if c in self.known_concepts else 0 for c in all_concepts])
    
    def progress_rate(self) -> float:
        """计算学习进度"""
        if not self.goal_concepts:
            return 0.0
        return len(self.known_concepts & self.goal_concepts) / len(self.goal_concepts)


@dataclass
class LearningAction:
    """学习动作 (推荐下一个概念)"""
    concept_id: str
    estimated_time: float
    difficulty_level: int
    prerequisites: List[str]
    

@dataclass
class LearningExperience:
    """学习经验 (S, A, R, S')"""
    state: np.ndarray
    action: int  # Concept index
    reward: float
    next_state: np.ndarray
    done: bool


@dataclass
class LearningPath:
    """学习路径"""
    steps: List[Dict]
    total_estimated_time: float
    coverage_score: float
    difficulty_curve: List[float]
    
    def to_dict(self) -> Dict:
        return {
            'steps': self.steps,
            'total_estimated_time': self.total_estimated_time,
            'coverage_score': self.coverage_score,
            'difficulty_curve': self.difficulty_curve
        }


# ============================================
# Knowledge Graph Environment
# ============================================

class KnowledgeGraphEnv:
    """知识图谱强化学习环境"""
    
    def __init__(self, graph_data_path: Path):
        self.graph = nx.DiGraph()
        self.concepts: List[str] = []
        self.concept_to_idx: Dict[str, int] = {}
        self.dependencies: Dict[str, Set[str]] = {}
        self.difficulty_levels: Dict[str, int] = {}
        self.estimated_times: Dict[str, float] = {}
        
        self.load_graph(graph_data_path)
        self.reset()
    
    def load_graph(self, path: Path):
        """加载知识图谱数据"""
        print(f"Loading graph from {path}")
        
        if not path.exists():
            # Create sample graph
            self._create_sample_graph()
            return
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add nodes
        for node in data.get('nodes', []):
            concept_id = node['id']
            self.graph.add_node(concept_id, **node)
            self.concepts.append(concept_id)
            
            # Estimate difficulty from formality level
            formality = node.get('metadata', {}).get('formality_level', 'L1')
            if formality.startswith('L'):
                self.difficulty_levels[concept_id] = int(formality[1:])
            else:
                self.difficulty_levels[concept_id] = 3
            
            # Estimate time from type
            type_time = {
                'definition': 0.5,
                'theorem': 1.5,
                'lemma': 1.0,
                'proposition': 1.0,
                'corollary': 0.8,
                'document': 2.0
            }
            self.estimated_times[concept_id] = type_time.get(node.get('type'), 1.0)
        
        # Add edges (dependencies)
        for edge in data.get('edges', []):
            source = edge.get('source')
            target = edge.get('target')
            if source and target:
                if isinstance(source, dict):
                    source = source['id']
                if isinstance(target, dict):
                    target = target['id']
                
                self.graph.add_edge(source, target, **edge)
                
                if target not in self.dependencies:
                    self.dependencies[target] = set()
                self.dependencies[target].add(source)
        
        # Create index mapping
        self.concept_to_idx = {c: i for i, c in enumerate(self.concepts)}
        
        print(f"Loaded {len(self.concepts)} concepts and {len(data.get('edges', []))} edges")
    
    def _create_sample_graph(self):
        """创建示例图用于测试"""
        concepts = [
            # Foundation
            ('Def-S-01-01', 'USTM基础', 1, 0.5),
            ('Def-S-01-02', '进程演算', 2, 1.0),
            ('Thm-S-01-01', 'USTM组合性', 3, 1.5),
            # Properties
            ('Def-S-07-01', '流计算确定性', 3, 1.0),
            ('Thm-S-07-01', '确定性定理', 4, 2.0),
            ('Def-S-08-01', 'Exactly-Once', 4, 1.5),
            ('Thm-S-08-02', 'Exactly-Once正确性', 5, 2.5),
            # Flink
            ('Def-F-02-01', 'Checkpoint机制', 3, 1.0),
            ('Thm-F-02-01', 'Checkpoint一致性', 4, 2.0),
        ]
        
        for concept_id, label, difficulty, time in concepts:
            self.concepts.append(concept_id)
            self.difficulty_levels[concept_id] = difficulty
            self.estimated_times[concept_id] = time
            self.graph.add_node(concept_id, label=label)
        
        # Add dependencies
        dependencies = [
            ('Thm-S-01-01', 'Def-S-01-01'),
            ('Thm-S-01-01', 'Def-S-01-02'),
            ('Def-S-07-01', 'Def-S-01-02'),
            ('Thm-S-07-01', 'Def-S-07-01'),
            ('Def-S-08-01', 'Def-S-07-01'),
            ('Thm-S-08-02', 'Def-S-08-01'),
            ('Thm-S-08-02', 'Thm-S-07-01'),
            ('Def-F-02-01', 'Def-S-08-01'),
            ('Thm-F-02-01', 'Def-F-02-01'),
        ]
        
        for target, source in dependencies:
            self.graph.add_edge(source, target)
            if target not in self.dependencies:
                self.dependencies[target] = set()
            self.dependencies[target].add(source)
        
        self.concept_to_idx = {c: i for i, c in enumerate(self.concepts)}
    
    def reset(self, goal_concepts: Optional[Set[str]] = None) -> UserState:
        """重置环境"""
        self.state = UserState(
            known_concepts=set(),
            goal_concepts=goal_concepts or set(),
            learning_history=[]
        )
        return self.state
    
    def get_valid_actions(self, state: UserState) -> List[str]:
        """获取当前状态下可执行的动作"""
        valid = []
        for concept in self.concepts:
            if concept in state.known_concepts:
                continue
            
            # Check if prerequisites are satisfied
            prereqs = self.dependencies.get(concept, set())
            if prereqs.issubset(state.known_concepts):
                valid.append(concept)
        
        return valid
    
    def step(self, action: str) -> Tuple[UserState, float, bool, Dict]:
        """执行动作并返回 (next_state, reward, done, info)"""
        # Update state
        self.state.known_concepts.add(action)
        self.state.learning_history.append({
            'concept': action,
            'timestamp': datetime.now().isoformat(),
            'difficulty': self.difficulty_levels.get(action, 3)
        })
        
        # Calculate reward
        reward = self._calculate_reward(action)
        
        # Check if done
        done = False
        if self.state.goal_concepts:
            done = self.state.goal_concepts.issubset(self.state.known_concepts)
        
        info = {
            'concept_learned': action,
            'difficulty': self.difficulty_levels.get(action, 3),
            'time_spent': self.estimated_times.get(action, 1.0)
        }
        
        return self.state, reward, done, info
    
    def _calculate_reward(self, concept: str) -> float:
        """计算学习奖励"""
        reward = 1.0  # Base reward for learning
        
        # Bonus for learning goal concepts
        if concept in self.state.goal_concepts:
            reward += 5.0
        
        # Bonus for unlocking new concepts
        unlocks = sum(
            1 for c, deps in self.dependencies.items()
            if concept in deps and deps.issubset(self.state.known_concepts | {concept})
        )
        reward += unlocks * 0.5
        
        # Penalty for difficulty mismatch
        difficulty = self.difficulty_levels.get(concept, 3)
        avg_difficulty = np.mean([
            self.difficulty_levels.get(c, 3)
            for c in self.state.known_concepts
        ]) if self.state.known_concepts else 1
        
        difficulty_diff = abs(difficulty - (avg_difficulty + 1))
        reward -= difficulty_diff * 0.2
        
        return reward


# ============================================
# Deep Q-Network
# ============================================

class DQN(nn.Module):
    """深度Q网络"""
    
    def __init__(self, state_dim: int, action_dim: int, hidden_dim: int = 256):
        super(DQN, self).__init__()
        
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.out = nn.Linear(hidden_dim // 2, action_dim)
        
        self.dropout = nn.Dropout(0.2)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = F.relu(self.fc3(x))
        return self.out(x)


class DQNAgent:
    """DQN智能体"""
    
    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        learning_rate: float = DEFAULT_LEARNING_RATE,
        gamma: float = DEFAULT_GAMMA,
        epsilon: float = DEFAULT_EPSILON,
        memory_size: int = DEFAULT_MEMORY_SIZE,
        batch_size: int = DEFAULT_BATCH_SIZE
    ):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma
        self.epsilon = epsilon
        self.batch_size = batch_size
        
        if TORCH_AVAILABLE:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            
            # Q-networks
            self.policy_net = DQN(state_dim, action_dim).to(self.device)
            self.target_net = DQN(state_dim, action_dim).to(self.device)
            self.target_net.load_state_dict(self.policy_net.state_dict())
            
            self.optimizer = optim.Adam(self.policy_net.parameters(), lr=learning_rate)
            self.memory = deque(maxlen=memory_size)
        else:
            # Fallback: Simple Q-table
            self.q_table = defaultdict(lambda: np.zeros(action_dim))
            self.memory = deque(maxlen=memory_size)
    
    def select_action(self, state: np.ndarray, valid_actions: List[int]) -> int:
        """选择动作 (ε-greedy)"""
        if not valid_actions:
            return 0
        
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        
        if TORCH_AVAILABLE:
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
                q_values = self.policy_net(state_tensor).cpu().numpy()[0]
                
                # Mask invalid actions
                masked_q = np.full(self.action_dim, float('-inf'))
                masked_q[valid_actions] = q_values[valid_actions]
                return int(np.argmax(masked_q))
        else:
            state_key = tuple(state)
            q_values = self.q_table[state_key]
            return valid_actions[np.argmax([q_values[a] for a in valid_actions])]
    
    def store_transition(self, experience: LearningExperience):
        """存储经验"""
        self.memory.append(experience)
    
    def learn(self):
        """学习更新"""
        if len(self.memory) < self.batch_size:
            return
        
        # Sample batch
        batch = random.sample(self.memory, self.batch_size)
        
        if TORCH_AVAILABLE:
            states = torch.FloatTensor([e.state for e in batch]).to(self.device)
            actions = torch.LongTensor([e.action for e in batch]).to(self.device)
            rewards = torch.FloatTensor([e.reward for e in batch]).to(self.device)
            next_states = torch.FloatTensor([e.next_state for e in batch]).to(self.device)
            dones = torch.FloatTensor([e.done for e in batch]).to(self.device)
            
            # Current Q values
            current_q = self.policy_net(states).gather(1, actions.unsqueeze(1)).squeeze()
            
            # Target Q values
            with torch.no_grad():
                next_q = self.target_net(next_states).max(1)[0]
                target_q = rewards + (1 - dones) * self.gamma * next_q
            
            # Loss and update
            loss = F.mse_loss(current_q, target_q)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            return loss.item()
        else:
            # Q-learning update
            for e in batch:
                state_key = tuple(e.state)
                next_state_key = tuple(e.next_state)
                
                current_q = self.q_table[state_key][e.action]
                next_max_q = np.max(self.q_table[next_state_key]) if not e.done else 0
                
                self.q_table[state_key][e.action] = current_q + 0.1 * (
                    e.reward + self.gamma * next_max_q - current_q
                )
    
    def update_target_network(self):
        """更新目标网络"""
        if TORCH_AVAILABLE:
            self.target_net.load_state_dict(self.policy_net.state_dict())


# ============================================
# Learning Path Generator
# ============================================

class LearningPathGenerator:
    """学习路径生成器"""
    
    def __init__(self, env: KnowledgeGraphEnv, agent: DQNAgent):
        self.env = env
        self.agent = agent
    
    def generate_path(
        self,
        goal_concepts: List[str],
        max_steps: int = 50,
        time_budget: float = 20.0
    ) -> LearningPath:
        """生成学习路径"""
        state = self.env.reset(goal_concepts=set(goal_concepts))
        
        steps = []
        total_time = 0.0
        difficulties = []
        
        for step in range(max_steps):
            # Get valid actions
            valid_concepts = self.env.get_valid_actions(state)
            if not valid_concepts:
                break
            
            valid_indices = [self.env.concept_to_idx[c] for c in valid_concepts]
            
            # Convert state to vector
            state_vector = state.to_vector(self.env.concepts)
            
            # Select action
            action_idx = self.agent.select_action(state_vector, valid_indices)
            concept = self.env.concepts[action_idx]
            
            # Check time budget
            concept_time = self.env.estimated_times.get(concept, 1.0)
            if total_time + concept_time > time_budget:
                break
            
            # Execute action
            next_state, reward, done, info = self.env.step(concept)
            
            # Record step
            steps.append({
                'step': step + 1,
                'concept': concept,
                'label': self.env.graph.nodes[concept].get('label', concept),
                'difficulty': info['difficulty'],
                'estimated_time': info['time_spent'],
                'reward': reward
            })
            
            total_time += concept_time
            difficulties.append(info['difficulty'])
            
            state = next_state
            
            if done:
                break
        
        # Calculate coverage
        coverage = len(state.known_concepts & set(goal_concepts)) / len(goal_concepts) if goal_concepts else 0
        
        return LearningPath(
            steps=steps,
            total_estimated_time=total_time,
            coverage_score=coverage,
            difficulty_curve=difficulties
        )
    
    def train(self, num_episodes: int = 1000, update_target_every: int = 10):
        """训练推荐模型"""
        print(f"\nTraining for {num_episodes} episodes...")
        
        rewards_history = []
        
        for episode in tqdm(range(num_episodes)):
            # Random goal for training
            goal = random.sample(self.env.concepts, min(3, len(self.env.concepts)))
            state = self.env.reset(goal_concepts=set(goal))
            
            episode_reward = 0
            step_count = 0
            max_steps = 50
            
            while step_count < max_steps:
                # Get valid actions
                valid_concepts = self.env.get_valid_actions(state)
                if not valid_concepts:
                    break
                
                valid_indices = [self.env.concept_to_idx[c] for c in valid_concepts]
                
                # Convert state
                state_vector = state.to_vector(self.env.concepts)
                
                # Select and execute action
                action_idx = self.agent.select_action(state_vector, valid_indices)
                concept = self.env.concepts[action_idx]
                
                next_state, reward, done, info = self.env.step(concept)
                next_state_vector = next_state.to_vector(self.env.concepts)
                
                # Store transition
                experience = LearningExperience(
                    state=state_vector,
                    action=action_idx,
                    reward=reward,
                    next_state=next_state_vector,
                    done=done
                )
                self.agent.store_transition(experience)
                
                # Learn
                self.agent.learn()
                
                episode_reward += reward
                state = next_state
                step_count += 1
                
                if done:
                    break
            
            rewards_history.append(episode_reward)
            
            # Update target network
            if episode % update_target_every == 0:
                self.agent.update_target_network()
            
            # Decay epsilon
            if episode % 100 == 0:
                self.agent.epsilon = max(0.01, self.agent.epsilon * 0.95)
        
        print(f"Training complete. Average reward: {np.mean(rewards_history[-100:]):.2f}")
        return rewards_history


# ============================================
# Evaluation
# ============================================

def evaluate_path(path: LearningPath, env: KnowledgeGraphEnv) -> Dict:
    """评估学习路径质量"""
    
    # Difficulty progression (should increase gradually)
    difficulty_scores = []
    for i in range(1, len(path.difficulty_curve)):
        diff = path.difficulty_curve[i] - path.difficulty_curve[i-1]
        # Ideal: small positive increase
        if 0 <= diff <= 2:
            difficulty_scores.append(1.0)
        elif diff > 2:
            difficulty_scores.append(0.5)  # Too steep
        else:
            difficulty_scores.append(0.8)  # Decrease is okay
    
    avg_difficulty_score = np.mean(difficulty_scores) if difficulty_scores else 0
    
    # Coverage
    coverage_score = path.coverage_score
    
    # Efficiency (concepts per hour)
    efficiency = len(path.steps) / path.total_estimated_time if path.total_estimated_time > 0 else 0
    
    # Overall score
    overall = (
        coverage_score * 0.4 +
        avg_difficulty_score * 0.3 +
        min(efficiency / 2, 1.0) * 0.3
    )
    
    return {
        'coverage': coverage_score,
        'difficulty_progression': avg_difficulty_score,
        'efficiency': efficiency,
        'overall_score': overall,
        'total_concepts': len(path.steps),
        'total_time': path.total_estimated_time
    }


# ============================================
# Main
# ============================================

def main():
    parser = argparse.ArgumentParser(description='RL-based Learning Path Recommender v2.0')
    parser.add_argument('--graph-path', type=Path, default=PROJECT_ROOT / '.vscode' / 'graph-data.json')
    parser.add_argument('--goal', nargs='+', help='Goal concepts to learn')
    parser.add_argument('--train', action='store_true', help='Train the model')
    parser.add_argument('--epochs', type=int, default=1000, help='Training epochs')
    parser.add_argument('--output', type=Path, default=PROJECT_ROOT / '.scripts' / 'kg-v2' / 'learning-path.json')
    parser.add_argument('--time-budget', type=float, default=20.0, help='Time budget in hours')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("AnalysisDataFlow 知识图谱 v2.0 - 强化学习推荐器")
    print("=" * 60)
    
    # Initialize environment
    print("\n[1/4] Initializing environment...")
    env = KnowledgeGraphEnv(args.graph_path)
    
    # Initialize agent
    print("\n[2/4] Initializing DQN agent...")
    state_dim = len(env.concepts)
    action_dim = len(env.concepts)
    agent = DQNAgent(state_dim, action_dim)
    
    # Initialize generator
    generator = LearningPathGenerator(env, agent)
    
    # Train if requested
    if args.train or not TORCH_AVAILABLE:
        print("\n[3/4] Training model...")
        rewards = generator.train(num_episodes=args.epochs)
    
    # Generate path
    print("\n[4/4] Generating learning path...")
    
    if args.goal:
        goals = args.goal
    else:
        # Default: sample some advanced concepts
        advanced = [c for c in env.concepts if env.difficulty_levels.get(c, 1) >= 4]
        goals = random.sample(advanced, min(3, len(advanced))) if advanced else env.concepts[:3]
    
    print(f"Goal concepts: {goals}")
    
    path = generator.generate_path(
        goal_concepts=goals,
        max_steps=30,
        time_budget=args.time_budget
    )
    
    # Evaluate
    evaluation = evaluate_path(path, env)
    
    # Output results
    print("\n" + "=" * 60)
    print("Generated Learning Path")
    print("=" * 60)
    print(f"Total steps: {len(path.steps)}")
    print(f"Estimated time: {path.total_estimated_time:.1f} hours")
    print(f"Coverage: {evaluation['coverage']*100:.1f}%")
    print(f"Overall score: {evaluation['overall_score']*100:.1f}%")
    print("\nPath:")
    for step in path.steps:
        print(f"  {step['step']}. {step['label']} ({step['concept']})")
        print(f"     Difficulty: L{step['difficulty']}, Time: {step['estimated_time']:.1f}h, Reward: {step['reward']:.2f}")
    
    # Save to file
    output_data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'goals': goals,
            'time_budget': args.time_budget
        },
        'path': path.to_dict(),
        'evaluation': evaluation
    }
    
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Path saved to {args.output}")


if __name__ == '__main__':
    main()
