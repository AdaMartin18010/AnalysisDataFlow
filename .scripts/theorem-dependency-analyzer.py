#!/usr/bin/env python3
"""
定理依赖关系分析工具
功能：
- 解析THEOREM-REGISTRY.md
- 构建定理依赖图
- 检测循环依赖

作者: AnalysisDataFlow Toolchain Team
版本: 1.0.0
日期: 2026-04-11
"""

import re
import os
import json
import glob
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import argparse


@dataclass
class Theorem:
    """定理节点"""
    id: str
    name: str
    name_zh: str
    name_en: str
    stage: str  # 'S', 'K', 'F'
    doc_id: str
    seq_num: int
    statement: str
    source_file: str
    dependencies: List[str] = field(default_factory=list)
    used_by: List[str] = field(default_factory=list)


@dataclass
class DependencyCycle:
    """依赖循环"""
    cycle: List[str]
    length: int
    theorem_ids: List[str]


class TheoremDependencyAnalyzer:
    """定理依赖关系分析器"""
    
    # 定理ID模式
    THEOREM_PATTERN = re.compile(r'(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2,3})')
    
    # 依赖关键词
    DEPENDENCY_KEYWORDS = [
        '依赖', 'depends on', 'relies on', '基于', 'by',
        '引用', '引用自', '引用定理', 'see',
        '根据', 'according to',
        '由.*可得', '由.*推出'
    ]
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        self.theorems: Dict[str, Theorem] = {}
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)  # 定理 -> 依赖的定理集合
        self.reverse_deps: Dict[str, Set[str]] = defaultdict(set)  # 定理 -> 被哪些定理依赖
        self.cycles: List[DependencyCycle] = []
        
    def parse_theorem_registry(self) -> List[Theorem]:
        """解析THEOREM-REGISTRY.md文件"""
        registry_path = self.base_path / 'THEOREM-REGISTRY.md'
        theorems = []
        
        if not registry_path.exists():
            print(f"Warning: {registry_path} not found")
            return theorems
            
        try:
            content = registry_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading registry: {e}")
            return theorems
            
        lines = content.split('\n')
        current_theorem = None
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # 匹配定理条目（表格行）
            # 格式: | Thm-S-01-01 | 定理名称 | ... |
            if line.startswith('| Thm-') or line.startswith('| Def-') or line.startswith('| Lemma-') or line.startswith('| Prop-') or line.startswith('| Cor-'):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 3:
                    theorem_id = parts[0]
                    name_zh = parts[1] if len(parts) > 1 else ''
                    name_en = parts[2] if len(parts) > 2 else ''
                    
                    # 解析ID
                    match = self.THEOREM_PATTERN.match(theorem_id)
                    if match:
                        type_abbr, stage, doc_id, seq_num = match.groups()
                        
                        theorem = Theorem(
                            id=theorem_id,
                            name=name_zh or name_en,
                            name_zh=name_zh,
                            name_en=name_en,
                            stage=stage,
                            doc_id=doc_id,
                            seq_num=int(seq_num),
                            statement='',
                            source_file='THEOREM-REGISTRY.md',
                            dependencies=[],
                            used_by=[]
                        )
                        theorems.append(theorem)
                        self.theorems[theorem_id] = theorem
                        current_theorem = theorem
                        
            # 收集依赖关系（在备注/依赖列中）
            if current_theorem and ('依赖' in line or 'depends' in line.lower()):
                # 提取依赖的定理ID
                deps = self.THEOREM_PATTERN.findall(line)
                for dep in deps:
                    dep_id = '-'.join(dep)
                    current_theorem.dependencies.append(dep_id)
                    self.dependencies[current_theorem.id].add(dep_id)
                    
        return theorems
    
    def scan_theorem_usage(self):
        """扫描所有文档中的定理引用"""
        print("\n🔎 Scanning theorem usage in documents...")
        
        md_files = []
        patterns = ["Struct/**/*.md", "Knowledge/**/*.md", "Flink/**/*.md"]
        
        for pattern in patterns:
            files = glob.glob(str(self.base_path / pattern), recursive=True)
            md_files.extend(files)
            
        md_files = list(set(md_files))
        
        for i, file_path in enumerate(md_files, 1):
            if i % 100 == 0:
                print(f"   Progress: {i}/{len(md_files)} files")
                
            try:
                content = Path(file_path).read_text(encoding='utf-8')
            except Exception:
                continue
                
            rel_path = str(Path(file_path).relative_to(self.base_path))
            
            # 查找所有定理引用
            for match in self.THEOREM_PATTERN.finditer(content):
                theorem_id = match.group(0)
                if theorem_id in self.theorems:
                    # 更新来源文件（如果不是来自registry本身）
                    if self.theorems[theorem_id].source_file == 'THEOREM-REGISTRY.md':
                        self.theorems[theorem_id].source_file = rel_path
                        
                    # 检查是否是依赖关系（在证明或相关上下文中）
                    # 简单启发式：查找周围文本中的依赖关键词
                    start = max(0, match.start() - 200)
                    end = min(len(content), match.end() + 200)
                    context = content[start:end]
                    
                    # 查找当前文档中定义的定理
                    local_theorems = self.THEOREM_PATTERN.findall(content)
                    for local in local_theorems:
                        local_id = '-'.join(local)
                        if local_id != theorem_id and local_id in self.theorems:
                            # 检查是否有依赖关键词
                            for keyword in self.DEPENDENCY_KEYWORDS:
                                if keyword in context:
                                    self.theorems[local_id].dependencies.append(theorem_id)
                                    self.dependencies[local_id].add(theorem_id)
                                    break
                                    
    def build_dependency_graph(self):
        """构建依赖图"""
        print("\n🔗 Building dependency graph...")
        
        # 构建反向依赖
        for theorem_id, deps in self.dependencies.items():
            for dep_id in deps:
                self.reverse_deps[dep_id].add(theorem_id)
                if dep_id in self.theorems:
                    self.theorems[dep_id].used_by.append(theorem_id)
                    
        print(f"   Built graph with {len(self.dependencies)} nodes")
        
    def detect_cycles(self) -> List[DependencyCycle]:
        """检测循环依赖"""
        print("\n🔄 Detecting dependency cycles...")
        
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node_id, path):
            visited.add(node_id)
            rec_stack.add(node_id)
            
            for neighbor in self.dependencies.get(node_id, []):
                if neighbor not in visited:
                    result = dfs(neighbor, path + [neighbor])
                    if result:
                        return result
                elif neighbor in rec_stack:
                    # 发现循环
                    cycle_start = path.index(neighbor) if neighbor in path else 0
                    cycle = path[cycle_start:] + [neighbor]
                    return cycle
                    
            rec_stack.remove(node_id)
            return None
            
        for theorem_id in self.theorems:
            if theorem_id not in visited:
                cycle = dfs(theorem_id, [theorem_id])
                if cycle:
                    cycles.append(DependencyCycle(
                        cycle=cycle,
                        length=len(cycle),
                        theorem_ids=cycle
                    ))
                    
        self.cycles = cycles
        return cycles
    
    def calculate_metrics(self) -> Dict:
        """计算依赖图指标"""
        metrics = {
            'total_theorems': len(self.theorems),
            'total_dependencies': sum(len(deps) for deps in self.dependencies.values()),
            'avg_dependencies': round(sum(len(deps) for deps in self.dependencies.values()) / len(self.theorems), 2) if self.theorems else 0,
            'max_dependencies': max((len(deps) for deps in self.dependencies.values()), default=0),
            'theorems_without_deps': len([t for t in self.theorems if not self.dependencies.get(t, [])]),
            'theorems_not_used': len([t for t in self.theorems if t not in self.reverse_deps or not self.reverse_deps[t]]),
            'cycles_detected': len(self.cycles),
            'by_stage': defaultdict(lambda: {'count': 0, 'deps': 0}),
        }
        
        for theorem_id, theorem in self.theorems.items():
            metrics['by_stage'][theorem.stage]['count'] += 1
            metrics['by_stage'][theorem.stage]['deps'] += len(self.dependencies.get(theorem_id, []))
            
        return metrics
    
    def find_proof_chains(self, target_theorem: str, max_depth: int = 5) -> List[List[str]]:
        """查找证明链"""
        chains = []
        
        def backtrack(current, chain, depth):
            if depth > max_depth:
                return
                
            deps = self.dependencies.get(current, set())
            if not deps:
                chains.append(chain[:])
                return
                
            for dep in deps:
                if dep not in chain:  # 避免循环
                    chain.append(dep)
                    backtrack(dep, chain, depth + 1)
                    chain.pop()
                    
        backtrack(target_theorem, [target_theorem], 0)
        return chains
    
    def analyze_critical_path(self) -> List[str]:
        """分析关键路径（被最多定理依赖的定理）"""
        # 计算每个定理被多少其他定理依赖（传递闭包）
        influence = {}
        
        for theorem_id in self.theorems:
            # BFS计算影响范围
            visited = set()
            queue = [theorem_id]
            count = -1  # 排除自身
            
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                count += 1
                
                for dependent in self.reverse_deps.get(current, []):
                    if dependent not in visited:
                        queue.append(dependent)
                        
            influence[theorem_id] = count
            
        # 排序返回影响最大的定理
        return sorted(influence.keys(), key=lambda x: influence[x], reverse=True)[:10]
    
    def export_dependency_graph(self, output_path: str):
        """导出依赖图"""
        graph_data = {
            'nodes': [
                {
                    'id': t.id,
                    'name': t.name,
                    'stage': t.stage,
                    'doc_id': t.doc_id,
                    'seq_num': t.seq_num,
                    'dependency_count': len(t.dependencies),
                    'used_by_count': len(t.used_by)
                }
                for t in self.theorems.values()
            ],
            'edges': [
                {'source': source, 'target': target, 'type': 'depends_on'}
                for source, targets in self.dependencies.items()
                for target in targets
            ],
            'cycles': [asdict(c) for c in self.cycles],
            'metadata': self.calculate_metrics()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
            
        print(f"\n📁 Dependency graph exported to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Theorem Dependency Analyzer')
    parser.add_argument('--base-path', default='.', help='项目根目录')
    parser.add_argument('--output', default='theorem-dependency-graph.json', help='输出文件路径')
    parser.add_argument('--find-chains', help='查找指定定理的证明链')
    parser.add_argument('--max-depth', type=int, default=5, help='证明链最大深度')
    
    args = parser.parse_args()
    
    analyzer = TheoremDependencyAnalyzer(args.base_path)
    
    # 1. 解析注册表
    print("📚 Theorem Dependency Analyzer")
    print("=" * 50)
    print("\n🔎 Parsing THEOREM-REGISTRY.md...")
    theorems = analyzer.parse_theorem_registry()
    print(f"   Found {len(theorems)} theorems in registry")
    
    # 2. 扫描文档中的引用
    analyzer.scan_theorem_usage()
    
    # 3. 构建依赖图
    analyzer.build_dependency_graph()
    
    # 4. 检测循环依赖
    cycles = analyzer.detect_cycles()
    
    # 5. 计算指标
    metrics = analyzer.calculate_metrics()
    
    # 6. 导出
    analyzer.export_dependency_graph(args.output)
    
    # 7. 可选：查找证明链
    if args.find_chains:
        chains = analyzer.find_proof_chains(args.find_chains, args.max_depth)
        print(f"\n📜 Proof chains for {args.find_chains}:")
        for i, chain in enumerate(chains[:5], 1):
            print(f"   Chain {i}: {' -> '.join(chain)}")
            
    # 8. 关键路径分析
    critical = analyzer.analyze_critical_path()
    
    # 打印摘要
    print("\n" + "=" * 50)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Total theorems:       {metrics['total_theorems']}")
    print(f"Total dependencies:   {metrics['total_dependencies']}")
    print(f"Avg dependencies:     {metrics['avg_dependencies']}")
    print(f"Max dependencies:     {metrics['max_dependencies']}")
    print(f"Theorems w/o deps:    {metrics['theorems_without_deps']}")
    print(f"Theorems not used:    {metrics['theorems_not_used']}")
    print(f"Cycles detected:      {metrics['cycles_detected']}")
    print("\nBy stage:")
    for stage, data in metrics['by_stage'].items():
        stage_name = {'S': 'Struct', 'K': 'Knowledge', 'F': 'Flink'}.get(stage, stage)
        print(f"  {stage_name}: {data['count']} theorems, {data['deps']} dependencies")
    print("\nTop 10 critical theorems (most influential):")
    for i, tid in enumerate(critical, 1):
        t = analyzer.theorems.get(tid)
        if t:
            print(f"  {i}. {tid}: {t.name[:50]}")
    print("=" * 50)
    
    if cycles:
        print("\n⚠️  Warning: Dependency cycles detected!")
        for c in cycles:
            print(f"   Cycle: {' -> '.join(c.cycle)}")
            
    return 0


if __name__ == '__main__':
    exit(main())
