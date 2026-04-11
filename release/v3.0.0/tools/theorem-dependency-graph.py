#!/usr/bin/env python3
"""
定理依赖图生成器 - 增强版
生成主题聚焦和阶段聚焦的依赖图，以及交互式HTML可视化
"""

import re
import json
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path

# 主题关键词映射
TOPIC_KEYWORDS = {
    'lambda': [
        'lambda', 'λ', '演算', 'calculus', 'abstraction', 'application', 'beta', 'reduction',
        'binder', 'variable', 'substitution', 'normal form', 'confluence', 'church',
        'lambda演算', '抽象', '应用', '规约', '归约', '替换', '变量', '绑定'
    ],
    'types': [
        'type', 'typing', 'type system', 'featherweight', 'FG', 'FGG', 'DOT', 'session type',
        'dependent type', 'generic', 'subtype', 'polymorphism', 'inference', 'soundness',
        'complete', 'progress', 'preservation', '类型', '泛型', '子类型', '多态', 'FGG', 'DOT'
    ],
    'concurrency': [
        'concurrency', 'parallel', 'synchronization', 'race', 'lock', 'mutex', 'semaphore',
        'channel', 'csp', 'actor', 'mailbox', 'process calculus', 'π-calculus', 'ccs',
        '并发', '并行', '同步', '竞态', '锁', '通道', '邮箱', '进程演算', '互模拟'
    ],
    'verification': [
        'verification', 'proof', 'soundness', 'completeness', 'invariant', 'model checking',
        'TLA+', 'coq', 'isabelle', 'temporal logic', 'safety', 'liveness', 'bisimulation',
        '验证', '证明', '可靠性', '完备性', '不变式', '模型检测', '时序逻辑', '安全性', '活性'
    ]
}

# 阶段映射
STAGE_MAP = {
    'S': 'Struct',
    'K': 'Knowledge',
    'F': 'Flink',
    'U': 'Unified'
}

# 颜色配置
COLORS = {
    'Thm': '#fff3e0',      # 橙色 - 定理
    'Lemma': '#f3e5f5',    # 紫色 - 引理
    'Def': '#e1f5fe',      # 蓝色 - 定义
    'Prop': '#e8f5e9',     # 绿色 - 命题
    'Cor': '#fce4ec'       # 粉色 - 推论
}

STAGE_COLORS = {
    'S': '#ffcc80',        # Struct - 橙黄
    'K': '#81c784',        # Knowledge - 绿色
    'F': '#64b5f6',        # Flink - 蓝色
    'U': '#ba68c8'         # Unified - 紫色
}


def parse_theorem_registry(content):
    """解析定理注册表，提取所有形式化元素及其依赖"""
    elements = {}
    
    # 通用模式：匹配所有元素类型
    # 支持 Thm-S-01-01, Def-K-02-01, Lemma-F-03-01, Prop-S-01-01, Cor-K-01-01
    element_pattern = r'\|\s*(Thm|Lemma|Def|Prop|Cor)-([SKFU])-(\d+)-([\da-z]+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*)\|'
    
    for match in re.finditer(element_pattern, content):
        elem_type, stage, doc_num, seq_num, name, location, extra = match.groups()
        elem_id = f"{elem_type}-{stage}-{doc_num}-{seq_num}"
        
        # 从extra列解析依赖和状态
        dependencies = []
        # 查找依赖元素引用
        dep_pattern = r'(Thm|Lemma|Def|Prop|Cor)-([SKFU])-(\d+)-([\da-z]+)'
        for dep_match in re.finditer(dep_pattern, extra):
            dep_type, dep_stage, dep_doc, dep_seq = dep_match.groups()
            dep_id = f"{dep_type}-{dep_stage}-{dep_doc}-{dep_seq}"
            if dep_id != elem_id:  # 避免自引用
                dependencies.append(dep_id)
        
        # 也去名称中查找依赖
        for dep_match in re.finditer(dep_pattern, name):
            dep_type, dep_stage, dep_doc, dep_seq = dep_match.groups()
            dep_id = f"{dep_type}-{dep_stage}-{dep_doc}-{dep_seq}"
            if dep_id != elem_id and dep_id not in dependencies:
                dependencies.append(dep_id)
        
        elements[elem_id] = {
            'id': elem_id,
            'type': elem_type,
            'stage': stage,
            'doc_num': doc_num,
            'seq_num': seq_num,
            'name': name.strip().replace('**', '').replace('|', ''),
            'location': location.strip(),
            'dependencies': list(set(dependencies)),  # 去重
            'referenced_by': [],
            'topic': classify_topic(name)
        }
    
    # 构建反向引用
    for elem_id, elem in elements.items():
        for dep_id in elem['dependencies']:
            if dep_id in elements:
                if elem_id not in elements[dep_id]['referenced_by']:
                    elements[dep_id]['referenced_by'].append(elem_id)
    
    return elements


def classify_topic(name):
    """根据名称分类主题"""
    name_lower = name.lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw.lower() in name_lower for kw in keywords):
            return topic
    return 'general'


def generate_topic_graph(elements, topic):
    """生成主题聚焦的依赖图"""
    # 筛选相关元素
    topic_elements = {k: v for k, v in elements.items() if v['topic'] == topic}
    
    # 如果没有直接匹配，通过关键词扩展
    if len(topic_elements) < 5:
        keywords = TOPIC_KEYWORDS.get(topic, [])
        topic_elements = {}
        for elem_id, elem in elements.items():
            if any(kw.lower() in elem['name'].lower() for kw in keywords):
                topic_elements[elem_id] = elem
    
    # 构建子图 - 包含直接依赖和引用
    subgraph_elements = dict(topic_elements)
    for elem_id in list(topic_elements.keys()):
        elem = elements.get(elem_id)
        if elem:
            # 添加依赖
            for dep_id in elem['dependencies']:
                if dep_id in elements and dep_id not in subgraph_elements:
                    subgraph_elements[dep_id] = elements[dep_id]
            # 添加被引用
            for ref_id in elem['referenced_by']:
                if ref_id in elements and ref_id not in subgraph_elements:
                    subgraph_elements[ref_id] = elements[ref_id]
    
    return subgraph_elements


def generate_stage_graph(elements, stage):
    """生成阶段聚焦的依赖图"""
    return {k: v for k, v in elements.items() if v['stage'] == stage}


def detect_cycles(elements):
    """检测循环依赖"""
    cycles = []
    visited = set()
    rec_stack = set()
    
    def dfs(node_id, path):
        if node_id in rec_stack:
            # 找到循环
            try:
                cycle_start = path.index(node_id)
                cycles.append(path[cycle_start:] + [node_id])
            except ValueError:
                pass
            return
        
        if node_id in visited or node_id not in elements:
            return
        
        visited.add(node_id)
        rec_stack.add(node_id)
        path.append(node_id)
        
        elem = elements.get(node_id)
        if elem:
            for dep_id in elem['dependencies']:
                dfs(dep_id, path.copy())
        
        rec_stack.remove(node_id)
    
    for elem_id in elements:
        if elem_id not in visited:
            dfs(elem_id, [])
    
    # 去重循环
    unique_cycles = []
    seen = set()
    for cycle in cycles:
        cycle_key = tuple(sorted(cycle))
        if cycle_key not in seen:
            seen.add(cycle_key)
            unique_cycles.append(cycle)
    
    return unique_cycles


def find_isolated_elements(elements):
    """找出孤立元素（无依赖且未被引用）"""
    isolated = []
    for elem_id, elem in elements.items():
        if not elem['dependencies'] and not elem['referenced_by']:
            isolated.append(elem_id)
    return isolated


def find_longest_dependency_chains(elements, max_chains=10):
    """找出最长的依赖链"""
    # 记忆化缓存
    memo = {}
    
    def get_depth(node_id, visited=None):
        if visited is None:
            visited = set()
        
        if node_id in memo:
            return memo[node_id]
        
        if node_id in visited or node_id not in elements:
            return 0
        
        visited.add(node_id)
        elem = elements[node_id]
        
        if not elem['dependencies']:
            depth = 1
        else:
            max_dep_depth = 0
            for dep_id in elem['dependencies']:
                if dep_id in elements and dep_id not in visited:
                    dep_depth = get_depth(dep_id, visited.copy())
                    max_dep_depth = max(max_dep_depth, dep_depth)
            depth = 1 + max_dep_depth
        
        memo[node_id] = depth
        return depth
    
    # 计算每个节点的深度
    node_depths = {}
    for elem_id in elements:
        node_depths[elem_id] = get_depth(elem_id)
    
    # 重建最长链
    def reconstruct_chain(node_id):
        chain = [node_id]
        current = node_id
        visited = {node_id}
        
        while True:
            elem = elements.get(current)
            if not elem or not elem['dependencies']:
                break
            
            # 找到最深的依赖
            next_node = None
            max_depth = 0
            for dep_id in elem['dependencies']:
                if dep_id in elements and dep_id not in visited:
                    dep_depth = node_depths.get(dep_id, 0)
                    if dep_depth > max_depth:
                        max_depth = dep_depth
                        next_node = dep_id
            
            if not next_node:
                break
            
            chain.append(next_node)
            visited.add(next_node)
            current = next_node
        
        return chain
    
    # 按深度排序
    sorted_nodes = sorted(node_depths.items(), key=lambda x: -x[1])
    chains = []
    
    for node_id, depth in sorted_nodes[:max_chains]:
        chain = reconstruct_chain(node_id)
        chains.append((len(chain), chain))
    
    return chains


def generate_mermaid_graph(elements, title="定理依赖图"):
    """生成Mermaid图"""
    if not elements:
        return f"graph TB\n    %% {title}\n    %% 无数据"
    
    lines = ["graph TB", f"    %% {title}", f"    %% 生成时间: {datetime.now().isoformat()}", ""]
    
    # 按类型分组
    groups = defaultdict(list)
    for elem_id, elem in elements.items():
        groups[elem['type']].append(elem)
    
    # 生成节点
    type_names = {'Thm': '定理', 'Lemma': '引理', 'Def': '定义', 'Prop': '命题', 'Cor': '推论'}
    
    for elem_type in ['Def', 'Lemma', 'Prop', 'Thm', 'Cor']:  # 按逻辑顺序
        elems = groups.get(elem_type, [])
        if not elems:
            continue
        type_name = type_names.get(elem_type, elem_type)
        lines.append(f"    subgraph {elem_type}Group[{type_name} ({len(elems)})]")
        for elem in elems:
            short_name = elem['name'][:35] + "..." if len(elem['name']) > 35 else elem['name']
            safe_name = short_name.replace('"', '&quot;').replace('[', '&#91;').replace(']', '&#93;')
            stage_color = STAGE_COLORS.get(elem['stage'], '#ccc')
            lines.append(f"        {elem['id']}[\"{elem['id']}<br/>{safe_name}\"]")
        lines.append("    end")
        lines.append("")
    
    # 生成边 - 限制边数以保持可读性
    lines.append("    %% 依赖关系")
    edges = set()
    edge_count = 0
    max_edges = 100  # 限制边数
    
    for elem_id, elem in elements.items():
        for dep_id in elem['dependencies']:
            if dep_id in elements and edge_count < max_edges:
                edge = (dep_id, elem_id)  # 依赖指向被依赖
                if edge not in edges:
                    edges.add(edge)
                    lines.append(f"    {dep_id} --> {elem_id}")
                    edge_count += 1
    
    if edge_count >= max_edges:
        lines.append(f"    %% 边数超过限制，仅显示前 {max_edges} 条")
    
    lines.append("")
    
    # 样式定义
    lines.append("    %% 样式定义")
    for elem_type, color in COLORS.items():
        lines.append(f"    classDef {elem_type}Style fill:{color},stroke:#333,stroke-width:1px")
    
    # 应用样式
    lines.append("")
    lines.append("    %% 应用样式")
    for elem_type, elems in groups.items():
        if elems:
            ids = ','.join([e['id'] for e in elems[:50]])  # 限制样式应用数量
            if len(elems) > 50:
                lines.append(f"    %% {elem_type} 类型有 {len(elems)} 个元素，仅前50个应用样式")
            lines.append(f"    class {ids} {elem_type}Style")
    
    return '\n'.join(lines)


def generate_interactive_html(elements):
    """生成交互式HTML可视化"""
    
    # 限制节点数以确保性能
    max_nodes = 500
    if len(elements) > max_nodes:
        # 优先选择有被引用或依赖的节点
        priority_elements = {
            k: v for k, v in elements.items() 
            if v['dependencies'] or v['referenced_by']
        }
        if len(priority_elements) > max_nodes:
            elements = dict(list(priority_elements.items())[:max_nodes])
        else:
            elements = priority_elements
    
    # 准备D3.js数据
    nodes = []
    links = []
    node_map = {}
    
    for i, (elem_id, elem) in enumerate(elements.items()):
        node = {
            'id': elem_id,
            'name': elem['name'][:50],
            'type': elem['type'],
            'stage': elem['stage'],
            'topic': elem['topic'],
            'group': list(COLORS.keys()).index(elem['type']),
            'ref_count': len(elem['referenced_by']),
            'dep_count': len(elem['dependencies']),
            'radius': 5 + min(len(elem['referenced_by']), 20) * 0.5
        }
        nodes.append(node)
        node_map[elem_id] = i
    
    for elem_id, elem in elements.items():
        for dep_id in elem['dependencies']:
            if dep_id in node_map:
                links.append({
                    'source': node_map[dep_id],
                    'target': node_map[elem_id],
                    'value': 1
                })
    
    data_json = json.dumps({'nodes': nodes, 'links': links}, ensure_ascii=False)
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>定理依赖图 - 交互式可视化</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            overflow: hidden;
        }}
        #container {{ display: flex; height: 100vh; }}
        #sidebar {{
            width: 340px;
            background: white;
            box-shadow: 2px 0 8px rgba(0,0,0,0.1);
            padding: 20px;
            overflow-y: auto;
            flex-shrink: 0;
        }}
        #graph {{
            flex: 1;
            position: relative;
            overflow: hidden;
        }}
        h1 {{ font-size: 18px; margin-bottom: 20px; color: #333; }}
        h2 {{ font-size: 14px; margin: 20px 0 10px; color: #666; text-transform: uppercase; }}
        .stat {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}
        .stat-value {{ font-weight: bold; color: #2196F3; }}
        .legend {{
            display: flex;
            align-items: center;
            margin: 5px 0;
            font-size: 12px;
        }}
        .legend-color {{
            width: 16px;
            height: 16px;
            border-radius: 50%;
            margin-right: 8px;
            border: 2px solid #333;
        }}
        #search {{
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 15px;
            font-size: 14px;
        }}
        .filter-group {{ margin: 10px 0; }}
        .filter-group label {{
            display: flex;
            align-items: center;
            margin: 5px 0;
            font-size: 12px;
            cursor: pointer;
        }}
        .filter-group input {{ margin-right: 8px; }}
        #tooltip {{
            position: absolute;
            background: rgba(0,0,0,0.9);
            color: white;
            padding: 10px 15px;
            border-radius: 4px;
            font-size: 12px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
            z-index: 1000;
            max-width: 300px;
        }}
        #tooltip h3 {{ font-size: 13px; margin-bottom: 5px; color: #FFD700; }}
        #tooltip p {{ margin: 3px 0; line-height: 1.4; }}
        .controls {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: white;
            padding: 10px;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .controls button {{
            display: block;
            width: 100%;
            padding: 8px 12px;
            margin: 5px 0;
            border: none;
            background: #2196F3;
            color: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }}
        .controls button:hover {{ background: #1976D2; }}
        svg {{ width: 100%; height: 100%; }}
        .node {{
            cursor: pointer;
            stroke: #333;
            stroke-width: 1.5px;
        }}
        .node:hover {{ stroke-width: 3px; }}
        .link {{
            stroke: #999;
            stroke-opacity: 0.6;
            stroke-width: 1px;
        }}
        .link.highlight {{
            stroke: #FF5722;
            stroke-width: 2px;
            stroke-opacity: 1;
        }}
        .node.highlight {{ stroke: #FF5722; stroke-width: 3px; }}
        .node.dimmed {{ opacity: 0.2; }}
        .link.dimmed {{ opacity: 0.1; }}
    </style>
</head>
<body>
    <div id="container">
        <div id="sidebar">
            <h1>📊 定理依赖网络可视化</h1>
            
            <input type="text" id="search" placeholder="搜索定理、定义、引理...">
            
            <h2>📈 统计信息</h2>
            <div class="stat">
                <span>总元素数</span>
                <span class="stat-value">{len(elements)}</span>
            </div>
            <div class="stat">
                <span>定理 (Thm)</span>
                <span class="stat-value">{sum(1 for e in elements.values() if e['type'] == 'Thm')}</span>
            </div>
            <div class="stat">
                <span>引理 (Lemma)</span>
                <span class="stat-value">{sum(1 for e in elements.values() if e['type'] == 'Lemma')}</span>
            </div>
            <div class="stat">
                <span>定义 (Def)</span>
                <span class="stat-value">{sum(1 for e in elements.values() if e['type'] == 'Def')}</span>
            </div>
            <div class="stat">
                <span>命题 (Prop)</span>
                <span class="stat-value">{sum(1 for e in elements.values() if e['type'] == 'Prop')}</span>
            </div>
            <div class="stat">
                <span>推论 (Cor)</span>
                <span class="stat-value">{sum(1 for e in elements.values() if e['type'] == 'Cor')}</span>
            </div>
            
            <h2>🎨 图例</h2>
            <div class="legend">
                <div class="legend-color" style="background: {COLORS['Thm']}"></div>
                <span>定理 (Theorem)</span>
            </div>
            <div class="legend">
                <div class="legend-color" style="background: {COLORS['Lemma']}"></div>
                <span>引理 (Lemma)</span>
            </div>
            <div class="legend">
                <div class="legend-color" style="background: {COLORS['Def']}"></div>
                <span>定义 (Definition)</span>
            </div>
            <div class="legend">
                <div class="legend-color" style="background: {COLORS['Prop']}"></div>
                <span>命题 (Proposition)</span>
            </div>
            <div class="legend">
                <div class="legend-color" style="background: {COLORS['Cor']}"></div>
                <span>推论 (Corollary)</span>
            </div>
            
            <h2>🔍 类型过滤</h2>
            <div class="filter-group">
                <label><input type="checkbox" checked data-type="Thm"> 定理</label>
                <label><input type="checkbox" checked data-type="Lemma"> 引理</label>
                <label><input type="checkbox" checked data-type="Def"> 定义</label>
                <label><input type="checkbox" checked data-type="Prop"> 命题</label>
                <label><input type="checkbox" checked data-type="Cor"> 推论</label>
            </div>
            
            <h2>📚 阶段过滤</h2>
            <div class="filter-group">
                <label><input type="checkbox" checked data-stage="S"> Struct (形式理论)</label>
                <label><input type="checkbox" checked data-stage="K"> Knowledge (知识结构)</label>
                <label><input type="checkbox" checked data-stage="F"> Flink (Flink专项)</label>
            </div>
            
            <h2>📖 使用说明</h2>
            <div style="font-size: 12px; color: #666; line-height: 1.6;">
                <p>• 滚轮缩放，拖拽移动</p>
                <p>• 点击节点高亮连接</p>
                <p>• 拖拽节点调整布局</p>
                <p>• 搜索框过滤节点</p>
            </div>
        </div>
        
        <div id="graph">
            <div class="controls">
                <button onclick="zoomIn()">🔍 放大</button>
                <button onclick="zoomOut()">🔍 缩小</button>
                <button onclick="resetZoom()">⟲ 重置</button>
                <button onclick="toggleAnimation()">⏯ 动画</button>
            </div>
            <div id="tooltip"></div>
        </div>
    </div>

    <script>
        const data = {data_json};
        const colors = {json.dumps(COLORS)};
        const stageColors = {json.dumps(STAGE_COLORS)};
        
        let width, height, svg, g, link, node, simulation;
        let currentZoom = d3.zoomIdentity;
        let animationEnabled = true;
        
        function init() {{
            const container = document.getElementById('graph');
            width = container.clientWidth;
            height = container.clientHeight;
            
            svg = d3.select('#graph')
                .append('svg')
                .attr('width', width)
                .attr('height', height);
            
            g = svg.append('g');
            
            const zoom = d3.zoom()
                .scaleExtent([0.1, 4])
                .on('zoom', (event) => {{
                    currentZoom = event.transform;
                    g.attr('transform', event.transform);
                }});
            
            svg.call(zoom);
            
            simulation = d3.forceSimulation(data.nodes)
                .force('link', d3.forceLink(data.links).id(d => d.id).distance(80))
                .force('charge', d3.forceManyBody().strength(-200))
                .force('center', d3.forceCenter(width / 2, height / 2))
                .force('collision', d3.forceCollide().radius(d => d.radius + 3));
            
            render();
            setupInteractions();
        }}
        
        function render() {{
            link = g.append('g')
                .attr('class', 'links')
                .selectAll('line')
                .data(data.links)
                .enter().append('line')
                .attr('class', 'link');
            
            node = g.append('g')
                .attr('class', 'nodes')
                .selectAll('circle')
                .data(data.nodes)
                .enter().append('circle')
                .attr('class', 'node')
                .attr('r', d => d.radius)
                .attr('fill', d => colors[d.type] || '#ccc')
                .attr('stroke', d => stageColors[d.stage] || '#333')
                .call(d3.drag()
                    .on('start', dragstarted)
                    .on('drag', dragged)
                    .on('end', dragended));
            
            const labels = g.append('g')
                .attr('class', 'labels')
                .selectAll('text')
                .data(data.nodes)
                .enter().append('text')
                .attr('font-size', 9)
                .attr('text-anchor', 'middle')
                .attr('dy', d => -d.radius - 5)
                .text(d => d.id)
                .style('pointer-events', 'none')
                .style('fill', '#333')
                .style('opacity', 0.7);
            
            simulation.on('tick', () => {{
                link
                    .attr('x1', d => d.source.x)
                    .attr('y1', d => d.source.y)
                    .attr('x2', d => d.target.x)
                    .attr('y2', d => d.target.y);
                
                node
                    .attr('cx', d => d.x)
                    .attr('cy', d => d.y);
                
                labels
                    .attr('x', d => d.x)
                    .attr('y', d => d.y);
            }});
        }}
        
        function setupInteractions() {{
            const tooltip = d3.select('#tooltip');
            
            node.on('mouseover', function(event, d) {{
                tooltip.style('opacity', 1)
                    .html(`
                        <h3>${{d.id}}</h3>
                        <p><strong>名称:</strong> ${{d.name}}</p>
                        <p><strong>类型:</strong> ${{d.type}}</p>
                        <p><strong>阶段:</strong> ${{d.stage}}</p>
                        <p><strong>主题:</strong> ${{d.topic}}</p>
                        <p><strong>被引用:</strong> ${{d.ref_count}} 次</p>
                        <p><strong>依赖:</strong> ${{d.dep_count}} 个</p>
                    `)
                    .style('left', (event.pageX + 10) + 'px')
                    .style('top', (event.pageY + 10) + 'px');
                
                highlightConnections(d);
            }})
            .on('mouseout', function() {{
                tooltip.style('opacity', 0);
                unhighlightConnections();
            }})
            .on('click', function(event, d) {{
                event.stopPropagation();
                focusOnNode(d);
            }});
            
            document.getElementById('search').addEventListener('input', function(e) {{
                const term = e.target.value.toLowerCase();
                if (term) {{
                    node.classed('dimmed', d => 
                        !d.id.toLowerCase().includes(term) && 
                        !d.name.toLowerCase().includes(term)
                    );
                }} else {{
                    node.classed('dimmed', false);
                }}
            }});
            
            document.querySelectorAll('.filter-group input[data-type]').forEach(cb => {{
                cb.addEventListener('change', filterNodes);
            }});
            
            document.querySelectorAll('.filter-group input[data-stage]').forEach(cb => {{
                cb.addEventListener('change', filterNodes);
            }});
            
            svg.on('click', () => {{ unhighlightConnections(); }});
        }}
        
        function highlightConnections(d) {{
            const connected = new Set();
            connected.add(d.id);
            
            data.links.forEach(l => {{
                if (l.source.id === d.id) connected.add(l.target.id);
                if (l.target.id === d.id) connected.add(l.source.id);
            }});
            
            node.classed('dimmed', n => !connected.has(n.id));
            node.classed('highlight', n => n.id === d.id);
            link.classed('dimmed', l => l.source.id !== d.id && l.target.id !== d.id);
            link.classed('highlight', l => l.source.id === d.id || l.target.id === d.id);
        }}
        
        function unhighlightConnections() {{
            node.classed('dimmed', false).classed('highlight', false);
            link.classed('dimmed', false).classed('highlight', false);
        }}
        
        function filterNodes() {{
            const activeTypes = Array.from(document.querySelectorAll('.filter-group input[data-type]:checked'))
                .map(cb => cb.dataset.type);
            const activeStages = Array.from(document.querySelectorAll('.filter-group input[data-stage]:checked'))
                .map(cb => cb.dataset.stage);
            
            node.style('display', d => {{
                const typeMatch = activeTypes.includes(d.type);
                const stageMatch = activeStages.includes(d.stage);
                return typeMatch && stageMatch ? 'block' : 'none';
            }});
            
            link.style('display', d => {{
                const sourceVisible = activeTypes.includes(d.source.type) && activeStages.includes(d.source.stage);
                const targetVisible = activeTypes.includes(d.target.type) && activeStages.includes(d.target.stage);
                return sourceVisible && targetVisible ? 'block' : 'none';
            }});
        }}
        
        function focusOnNode(d) {{
            svg.transition().duration(750).call(
                d3.zoom().transform,
                d3.zoomIdentity.translate(width/2, height/2).scale(1.5).translate(-d.x, -d.y)
            );
        }}
        
        function zoomIn() {{
            svg.transition().duration(300).call(d3.zoom().scaleBy, 1.3);
        }}
        
        function zoomOut() {{
            svg.transition().duration(300).call(d3.zoom().scaleBy, 0.7);
        }}
        
        function resetZoom() {{
            svg.transition().duration(750).call(d3.zoom().transform, d3.zoomIdentity);
        }}
        
        function toggleAnimation() {{
            animationEnabled = !animationEnabled;
            if (animationEnabled) {{
                simulation.restart();
            }} else {{
                simulation.stop();
            }}
        }}
        
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}
        
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}
        
        window.addEventListener('resize', () => {{
            const container = document.getElementById('graph');
            width = container.clientWidth;
            height = container.clientHeight;
            svg.attr('width', width).attr('height', height);
            simulation.force('center', d3.forceCenter(width / 2, height / 2));
            simulation.alpha(0.3).restart();
        }});
        
        init();
    </script>
</body>
</html>
'''
    return html_content


def generate_statistics_report(elements):
    """生成统计报告"""
    
    # 按类型统计
    type_stats = Counter(e['type'] for e in elements.values())
    stage_stats = Counter(e['stage'] for e in elements.values())
    
    # 1. 最常被引用的定义TOP20
    all_count = {k: v for k, v in elements.items()}
    top_referenced = sorted(all_count.items(), key=lambda x: len(x[1]['referenced_by']), reverse=True)[:20]
    
    # 2. 最复杂的依赖链
    longest_chains = find_longest_dependency_chains(elements, 10)
    
    # 3. 孤立元素
    isolated = find_isolated_elements(elements)
    
    # 4. 循环依赖检测
    cycles = detect_cycles(elements)
    
    report = f'''# 定理依赖网络统计报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **统计范围**: {len(elements)} 个形式化元素

---

## 1. 总体统计

### 1.1 按类型分布

| 类型 | 数量 | 占比 |
|------|------|------|
'''
    for t in ['Thm', 'Def', 'Lemma', 'Prop', 'Cor']:
        count = type_stats.get(t, 0)
        pct = count / len(elements) * 100 if elements else 0
        type_name = {'Thm': '定理', 'Def': '定义', 'Lemma': '引理', 'Prop': '命题', 'Cor': '推论'}.get(t, t)
        report += f'| {t} ({type_name}) | {count} | {pct:.1f}% |\n'
    
    report += f'''
### 1.2 按阶段分布

| 阶段 | 数量 | 占比 |
|------|------|------|
'''
    for s in ['S', 'K', 'F', 'U']:
        count = stage_stats.get(s, 0)
        if count > 0:
            pct = count / len(elements) * 100 if elements else 0
            stage_name = STAGE_MAP.get(s, s)
            report += f'| {stage_name} ({s}) | {count} | {pct:.1f}% |\n'
    
    total_refs = sum(len(e['referenced_by']) for e in elements.values())
    total_deps = sum(len(e['dependencies']) for e in elements.values())
    
    report += f'''
### 1.3 连接统计

- **总引用关系数**: {total_deps}
- **总被引用次数**: {total_refs}
- **平均出度**: {total_deps / len(elements):.2f} (每个元素平均依赖)
- **平均入度**: {total_refs / len(elements):.2f} (每个元素平均被引用)

---

## 2. 最常被引用的元素 TOP20

| 排名 | 元素ID | 名称 | 类型 | 被引用次数 | 所在阶段 |
|------|--------|------|------|-----------|----------|
'''
    for i, (elem_id, elem) in enumerate(top_referenced, 1):
        ref_count = len(elem['referenced_by'])
        stage = STAGE_MAP.get(elem['stage'], elem['stage'])
        name = elem['name'][:35] + '...' if len(elem['name']) > 35 else elem['name']
        report += f'| {i} | `{elem_id}` | {name} | {elem["type"]} | {ref_count} | {stage} |\n'
    
    report += f'''
---

## 3. 最复杂的依赖链

'''
    for i, (length, chain) in enumerate(longest_chains[:10], 1):
        report += f'### 3.{i} 链 #{i} (深度: {length})\n\n```\n'
        for j, elem_id in enumerate(chain):
            elem = elements.get(elem_id, {})
            name = elem.get('name', 'Unknown')[:40]
            indent = '  ' * j
            report += f'{indent}→ {elem_id}: {name}\n'
        report += '```\n\n'
    
    report += f'''---

## 4. 孤立元素分析

'''
    if isolated:
        report += f'检测到 **{len(isolated)}** 个孤立元素（无依赖且未被引用）：\n\n'
        report += '| 元素ID | 名称 | 类型 |\n|--------|------|------|\n'
        for elem_id in isolated[:50]:  # 限制显示数量
            elem = elements.get(elem_id, {})
            name = elem.get('name', 'Unknown')[:30]
            report += f'| `{elem_id}` | {name} | {elem.get("type", "?")} |\n'
        if len(isolated) > 50:
            report += f'| ... | 还有 {len(isolated) - 50} 个 | ... |\n'
    else:
        report += '✅ **未检测到孤立元素**，所有元素都参与引用网络。\n'
    
    report += f'''
---

## 5. 循环依赖检测

'''
    if cycles:
        report += f'⚠️ 检测到 **{len(cycles)}** 个循环依赖：\n\n'
        for i, cycle in enumerate(cycles[:10], 1):
            report += f'### 5.{i} 循环 #{i}\n\n'
            report += ' → '.join([f'`{c}`' for c in cycle]) + '\n\n'
    else:
        report += '✅ **未检测到循环依赖**，依赖图是无环的（DAG）。\n'
    
    report += f'''
---

## 6. 主题分布

'''
    topic_stats = Counter(e['topic'] for e in elements.values())
    for topic, count in sorted(topic_stats.items(), key=lambda x: -x[1]):
        topic_name = {
            'general': '一般',
            'lambda': 'Lambda演算',
            'types': '类型系统',
            'concurrency': '并发理论',
            'verification': '验证方法'
        }.get(topic, topic)
        report += f'- **{topic_name}** ({topic}): {count} 个元素\n'
    
    report += f'''
---

## 7. 关键洞察

1. **网络规模**: 共有 {len(elements)} 个形式化元素，{total_deps} 条依赖边
2. **核心枢纽**: 被引用最多的是 `{top_referenced[0][0] if top_referenced else "N/A"}`，有 {len(top_referenced[0][1]['referenced_by']) if top_referenced else 0} 个引用
3. **证明复杂度**: 最长依赖链深度为 {longest_chains[0][0] if longest_chains else 0}
4. **网络密度**: 平均每个元素依赖 {total_deps / len(elements):.2f} 个其他元素
5. **引用比例**: 平均每个元素被引用 {total_refs / len(elements):.2f} 次
6. **孤立比例**: {len(isolated)} / {len(elements)} = {len(isolated)/len(elements)*100:.1f}% 的元素是孤立的

---

## 8. 可视化文件列表

生成的可视化文件：

| 文件 | 说明 |
|------|------|
| `visuals/interactive-dependency.html` | 交互式D3.js可视化 |
| `visuals/lambda-deps.mmd` | Lambda演算主题依赖图 (Mermaid) |
| `visuals/types-deps.mmd` | 类型系统主题依赖图 (Mermaid) |
| `visuals/concurrency-deps.mmd` | 并发理论主题依赖图 (Mermaid) |
| `visuals/verification-deps.mmd` | 验证方法主题依赖图 (Mermaid) |
| `visuals/s-stage-deps.mmd` | Struct阶段依赖图 (Mermaid) |
| `visuals/k-stage-deps.mmd` | Knowledge阶段依赖图 (Mermaid) |
| `visuals/f-stage-deps.mmd` | Flink阶段依赖图 (Mermaid) |
| `visuals/dependency-stats.md` | 本统计报告 |

---

*报告由 theorem-dependency-graph.py 自动生成*
'''
    return report


def main():
    """主函数"""
    print("🔍 读取定理注册表...")
    
    # 读取定理注册表
    registry_path = Path('THEOREM-REGISTRY.md')
    if not registry_path.exists():
        print(f"❌ 错误: 未找到 {registry_path}")
        return
    
    content = registry_path.read_text(encoding='utf-8')
    
    print("📊 解析形式化元素...")
    elements = parse_theorem_registry(content)
    print(f"   解析到 {len(elements)} 个形式化元素")
    
    # 打印类型分布
    type_stats = Counter(e['type'] for e in elements.values())
    print(f"   类型分布: 定理={type_stats.get('Thm',0)}, 定义={type_stats.get('Def',0)}, 引理={type_stats.get('Lemma',0)}, 命题={type_stats.get('Prop',0)}, 推论={type_stats.get('Cor',0)}")
    
    # 确保输出目录存在
    output_dir = Path('visuals')
    output_dir.mkdir(exist_ok=True)
    
    # 1. 生成主题聚焦的依赖图
    topics = ['lambda', 'types', 'concurrency', 'verification']
    for topic in topics:
        print(f"🎯 生成 {topic} 主题依赖图...")
        topic_elements = generate_topic_graph(elements, topic)
        if topic_elements:
            mermaid = generate_mermaid_graph(topic_elements, f"{topic.capitalize()}主题依赖图")
            output_path = output_dir / f"{topic}-deps.mmd"
            output_path.write_text(mermaid, encoding='utf-8')
            print(f"   ✓ 已保存: {output_path} ({len(topic_elements)} 个元素)")
        else:
            print(f"   ⚠️ 未找到 {topic} 主题的相关元素")
    
    # 2. 生成阶段聚焦的依赖图
    stages = ['S', 'K', 'F']
    for stage in stages:
        stage_name = STAGE_MAP[stage]
        print(f"📚 生成 {stage_name} 阶段依赖图...")
        stage_elements = generate_stage_graph(elements, stage)
        if stage_elements:
            mermaid = generate_mermaid_graph(stage_elements, f"{stage_name}阶段依赖图")
            output_path = output_dir / f"{stage.lower()}-stage-deps.mmd"
            output_path.write_text(mermaid, encoding='utf-8')
            print(f"   ✓ 已保存: {output_path} ({len(stage_elements)} 个元素)")
        else:
            print(f"   ⚠️ 未找到 {stage_name} 阶段的相关元素")
    
    # 3. 生成交互式HTML可视化
    print("🌐 生成交互式HTML可视化...")
    html = generate_interactive_html(elements)
    html_path = output_dir / "interactive-dependency.html"
    html_path.write_text(html, encoding='utf-8')
    print(f"   ✓ 已保存: {html_path}")
    
    # 4. 生成统计报告
    print("📈 生成统计报告...")
    report = generate_statistics_report(elements)
    report_path = output_dir / "dependency-stats.md"
    report_path.write_text(report, encoding='utf-8')
    print(f"   ✓ 已保存: {report_path}")
    
    print("\n" + "="*60)
    print("✅ 所有可视化文件已生成完成！")
    print("="*60)
    print(f"\n输出文件列表:")
    print(f"  📊 visuals/interactive-dependency.html (交互式D3.js可视化)")
    print(f"  📈 visuals/lambda-deps.mmd (Lambda演算依赖图)")
    print(f"  📈 visuals/types-deps.mmd (类型系统依赖图)")
    print(f"  📈 visuals/concurrency-deps.mmd (并发理论依赖图)")
    print(f"  📈 visuals/verification-deps.mmd (验证方法依赖图)")
    print(f"  📚 visuals/s-stage-deps.mmd (Struct阶段依赖图)")
    print(f"  📚 visuals/k-stage-deps.mmd (Knowledge阶段依赖图)")
    print(f"  📚 visuals/f-stage-deps.mmd (Flink阶段依赖图)")
    print(f"  📝 visuals/dependency-stats.md (统计报告)")


if __name__ == '__main__':
    main()
