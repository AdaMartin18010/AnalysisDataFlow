#!/usr/bin/env python3
"""
AnalysisDataFlow Neo4j 图数据库导入文件生成器
解析 THEOREM-REGISTRY.md 生成 Cypher 导入语句

生成文件:
- nodes.cypher: 节点创建语句 (MERGE)
- edges.cypher: 关系创建语句 (MATCH + MERGE)
- stats.json: 统计信息
"""

import re
import json
from collections import defaultdict
from pathlib import Path

# 配置
INPUT_FILE = "THEOREM-REGISTRY.md"
OUTPUT_DIR = Path("neo4j/import")
BATCH_SIZE = 500  # 每批处理的节点数

# 确保输出目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 正则表达式模式
# 匹配: | Thm-S-01-01 | USTM组合性定理 | Struct/01.01 | L4 | - | ✅ |
ELEMENT_PATTERN = re.compile(
    r'\|\s*(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{1,3})\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]+)\|'
)

# 简化的匹配 (用于文档末尾的格式差异)
SIMPLE_PATTERN = re.compile(
    r'\|\s*(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{1,3})\s*\|\s*([^|]+)\|'
)

# 节点类型映射
TYPE_MAPPING = {
    'Thm': 'Theorem',
    'Def': 'Definition', 
    'Lemma': 'Lemma',
    'Prop': 'Proposition',
    'Cor': 'Corollary'
}

STAGE_MAPPING = {
    'S': 'Struct',
    'K': 'Knowledge',
    'F': 'Flink'
}

def parse_formal_level(level_str):
    """解析形式化等级 L1-L6"""
    if not level_str or level_str.strip() == '-':
        return 'L0'
    level_str = level_str.strip()
    # 处理 L4-L5 这样的范围
    if '-' in level_str and level_str.startswith('L'):
        parts = level_str.split('-')
        return parts[0].strip()  # 返回最低等级
    if level_str.startswith('L') and level_str[1:].isdigit():
        return level_str[:2]
    return 'L0'

def extract_dependencies(depends_str):
    """从依赖字符串提取引用的元素ID"""
    if not depends_str or depends_str.strip() in ['-', '']:
        return []
    
    # 匹配 Thm-S-01-01, Def-K-02-01 等模式
    dep_pattern = re.compile(r'(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d{2}-\d{1,3}')
    deps = dep_pattern.findall(depends_str)
    
    # 提取完整ID
    full_deps = []
    for match in dep_pattern.finditer(depends_str):
        full_deps.append(match.group(0))
    return full_deps

def sanitize_cypher_string(s):
    """转义Cypher字符串中的特殊字符"""
    if not s:
        return ""
    s = s.strip()
    # 转义引号
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace("'", "\\'")
    # 移除控制字符
    s = ''.join(char for char in s if ord(char) >= 32 or char in '\n\t')
    return s

def parse_registry():
    """解析定理注册表文件"""
    elements = []
    seen_ids = set()
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"错误: 无法读取 {INPUT_FILE}: {e}")
        return elements
    
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line.startswith('|') or '---' in line:
            continue
            
        match = ELEMENT_PATTERN.search(line)
        if match:
            type_abbr, stage, doc_num, seq_num, name, path, formal_level, depends, status = match.groups()
            element_id = f"{type_abbr}-{stage}-{doc_num}-{seq_num}"
            
            if element_id in seen_ids:
                continue
            seen_ids.add(element_id)
            
            element = {
                'id': element_id,
                'type': TYPE_MAPPING.get(type_abbr, type_abbr),
                'type_abbr': type_abbr,
                'stage': STAGE_MAPPING.get(stage, stage),
                'stage_abbr': stage,
                'doc_num': doc_num,
                'seq_num': seq_num,
                'name': sanitize_cypher_string(name),
                'path': path.strip() if path else '',
                'formal_level': parse_formal_level(formal_level),
                'dependencies': extract_dependencies(depends),
                'status': status.strip() if status else '✅'
            }
            elements.append(element)
    
    return elements

def generate_nodes_cypher(elements):
    """生成节点创建Cypher语句"""
    output_file = OUTPUT_DIR / "nodes.cypher"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("""// AnalysisDataFlow Neo4j 节点导入文件
// 包含所有形式化元素: 定理、定义、引理、命题、推论
// 版本: 1.0 | 生成日期: 2026-04-11
// 总节点数: {count}

// ============================================
// 1. 创建定理节点 (Theorem)
// ============================================

""".format(count=len(elements)))
        
        # 按类型分组
        by_type = defaultdict(list)
        for elem in elements:
            by_type[elem['type']].append(elem)
        
        # 生成各类型的MERGE语句
        for node_type in ['Theorem', 'Definition', 'Lemma', 'Proposition', 'Corollary']:
            elems = by_type.get(node_type, [])
            if not elems:
                continue
                
            f.write(f"// {node_type} 节点 ({len(elems)}个)\n")
            
            for i in range(0, len(elems), BATCH_SIZE):
                batch = elems[i:i+BATCH_SIZE]
                f.write(f"\n// Batch {i//BATCH_SIZE + 1}\n")
                
                for elem in batch:
                    cypher = f"""MERGE (n:{node_type} {{id: "{elem['id']}"}})
ON CREATE SET n.name = "{elem['name']}",
              n.stage = "{elem['stage']}",
              n.doc_num = "{elem['doc_num']}",
              n.seq_num = {elem['seq_num']},
              n.path = "{elem['path']}",
              n.formal_level = "{elem['formal_level']}",
              n.type_abbr = "{elem['type_abbr']}",
              n.stage_abbr = "{elem['stage_abbr']}"
ON MATCH SET n.name = "{elem['name']}",
             n.stage = "{elem['stage']}",
             n.doc_num = "{elem['doc_num']}",
             n.seq_num = {elem['seq_num']},
             n.path = "{elem['path']}",
             n.formal_level = "{elem['formal_level']}",
             n.type_abbr = "{elem['type_abbr']}",
             n.stage_abbr = "{elem['stage_abbr']}";
"""
                    f.write(cypher)
                
                # 每批后添加性能优化提示
                f.write(f"// 已处理 {min(i+BATCH_SIZE, len(elems))}/{len(elems)} 个 {node_type}\n")
        
        # 添加标签为通用 FormalElement
        f.write("""
// ============================================
// 2. 添加通用标签 FormalElement
// ============================================

MATCH (n:Theorem) WHERE NOT n:FormalElement SET n:FormalElement;
MATCH (n:Definition) WHERE NOT n:FormalElement SET n:FormalElement;
MATCH (n:Lemma) WHERE NOT n:FormalElement SET n:FormalElement;
MATCH (n:Proposition) WHERE NOT n:FormalElement SET n:FormalElement;
MATCH (n:Corollary) WHERE NOT n:FormalElement SET n:FormalElement;
""")
        
        # 添加统计查询
        f.write("""
// ============================================
// 3. 验证导入结果
// ============================================

// 统计各类节点数量
MATCH (n:FormalElement)
RETURN n.type_abbr as Type, count(*) as Count
ORDER BY Count DESC;

// 统计各阶段节点数量  
MATCH (n:FormalElement)
RETURN n.stage as Stage, count(*) as Count
ORDER BY Count DESC;

// 统计形式化等级分布
MATCH (n:FormalElement)
RETURN n.formal_level as Level, count(*) as Count
ORDER BY Level;
""")
    
    print(f"✅ 节点文件已生成: {output_file}")
    return len(elements)

def generate_edges_cypher(elements):
    """生成关系创建Cypher语句"""
    output_file = OUTPUT_DIR / "edges.cypher"
    
    # 构建ID到类型的映射
    id_to_type = {elem['id']: elem['type'] for elem in elements}
    
    # 收集所有依赖关系
    dependencies = []
    for elem in elements:
        for dep_id in elem['dependencies']:
            if dep_id in id_to_type:
                dependencies.append({
                    'from_id': elem['id'],
                    'from_type': elem['type'],
                    'to_id': dep_id,
                    'to_type': id_to_type[dep_id],
                    'rel_type': 'DEPENDS_ON'
                })
    
    # 推断其他关系类型
    # 引理 -> 定理 (PROVES)
    # 推论 -> 定理/引理 (DERIVES_FROM)
    # 定义 -> 定理/引理 (INSTANTIATES)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("""// AnalysisDataFlow Neo4j 关系导入文件
// 包含元素间的依赖关系
// 版本: 1.0 | 生成日期: 2026-04-11
// 总关系数: {count}

// ============================================
// 1. 创建 DEPENDS_ON 关系 (显式依赖)
// ============================================

""".format(count=len(dependencies)))
        
        # 分批处理依赖关系
        for i in range(0, len(dependencies), BATCH_SIZE):
            batch = dependencies[i:i+BATCH_SIZE]
            f.write(f"\n// Batch {i//BATCH_SIZE + 1} ({len(batch)} 个关系)\n")
            
            for dep in batch:
                cypher = f"""MATCH (a {{id: "{dep['from_id']}"}}), (b {{id: "{dep['to_id']}"}})
MERGE (a)-[r:DEPENDS_ON]->(b)
ON CREATE SET r.inferred = false;
"""
                f.write(cypher)
        
        # 添加推断关系
        f.write("""
// ============================================
// 2. 创建 PROVES 关系 (引理 -> 定理)
// ============================================

MATCH (lemma:Lemma), (theorem:Theorem)
WHERE lemma.name CONTAINS theorem.name OR theorem.name CONTAINS lemma.name
  AND NOT (lemma)-[:DEPENDS_ON]->(theorem)
MERGE (lemma)-[r:PROVES]->(theorem)
ON CREATE SET r.inferred = true;

// ============================================
// 3. 创建 DERIVES_FROM 关系 (推论 -> 定理/引理)
// ============================================

MATCH (cor:Corollary), (target)
WHERE (target:Theorem OR target:Lemma) 
  AND cor.path = target.path
MERGE (cor)-[r:DERIVES_FROM]->(target)
ON CREATE SET r.inferred = true;

// ============================================
// 4. 创建 INSTANTIATES 关系 (定义 -> 定理/引理)
// ============================================

MATCH (def:Definition), (target)
WHERE (target:Theorem OR target:Lemma)
  AND def.path = target.path
  AND (target.name CONTAINS def.name OR def.name CONTAINS target.name)
MERGE (def)-[r:INSTANTIATES]->(target)
ON CREATE SET r.inferred = true;

// ============================================
// 5. 创建 IMPLEMENTS 关系 (Flink -> Knowledge)
// ============================================

MATCH (f:FormalElement) WHERE f.stage = "Flink"
MATCH (k:FormalElement) WHERE k.stage = "Knowledge"
  AND f.name CONTAINS k.name
MERGE (f)-[r:IMPLEMENTS]->(k)
ON CREATE SET r.inferred = true;

// ============================================
// 6. 创建 SIMILAR_TO 关系 (名称相似)
// ============================================

MATCH (a:FormalElement), (b:FormalElement)
WHERE a.id <> b.id
  AND a.name = b.name
  AND NOT (a)-[:DEPENDS_ON|PROVES|DERIVES_FROM|INSTANTIATES]->(b)
  AND NOT (b)-[:DEPENDS_ON|PROVES|DERIVES_FROM|INSTANTIATES]->(a)
MERGE (a)-[r:SIMILAR_TO]->(b)
ON CREATE SET r.similarity = 'name_exact';
""")
        
        # 添加统计查询
        f.write("""
// ============================================
// 7. 验证关系导入结果
// ============================================

// 统计各类型关系数量
MATCH ()-[r]->()
RETURN type(r) as RelationType, count(*) as Count
ORDER BY Count DESC;

// 查找高度连接的元素 (中心节点)
MATCH (n:FormalElement)-[r:DEPENDS_ON]-()
WITH n, count(r) as degree
ORDER BY degree DESC
LIMIT 10
RETURN n.id as ElementID, n.name as Name, n.type_abbr as Type, degree as Connections;

// 查找依赖最多的元素
MATCH (n:FormalElement)<-[r:DEPENDS_ON]-()
WITH n, count(r) as dependents
ORDER BY dependents DESC
LIMIT 10
RETURN n.id as ElementID, n.name as Name, dependents as DependentsCount;
""")
    
    print(f"✅ 关系文件已生成: {output_file}")
    return len(dependencies)

def generate_stats(elements, edge_count):
    """生成统计信息"""
    stats = {
        'total_elements': len(elements),
        'by_type': defaultdict(int),
        'by_stage': defaultdict(int),
        'by_formal_level': defaultdict(int),
        'dependencies_count': edge_count
    }
    
    for elem in elements:
        stats['by_type'][elem['type']] += 1
        stats['by_stage'][elem['stage']] += 1
        stats['by_formal_level'][elem['formal_level']] += 1
    
    # 转换为普通dict以便JSON序列化
    stats['by_type'] = dict(stats['by_type'])
    stats['by_stage'] = dict(stats['by_stage'])
    stats['by_formal_level'] = dict(stats['by_formal_level'])
    
    output_file = OUTPUT_DIR / "stats.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 统计文件已生成: {output_file}")
    return stats

def main():
    print("="*60)
    print("AnalysisDataFlow Neo4j 导入文件生成器")
    print("="*60)
    
    # 解析注册表
    print(f"\n📖 正在解析 {INPUT_FILE}...")
    elements = parse_registry()
    
    if not elements:
        print("❌ 未能解析到任何形式化元素")
        return
    
    print(f"✅ 解析到 {len(elements)} 个形式化元素")
    
    # 生成节点文件
    print("\n📝 正在生成节点文件...")
    node_count = generate_nodes_cypher(elements)
    
    # 生成关系文件
    print("\n🔗 正在生成关系文件...")
    edge_count = generate_edges_cypher(elements)
    
    # 生成统计
    print("\n📊 正在生成统计信息...")
    stats = generate_stats(elements, edge_count)
    
    # 打印摘要
    print("\n" + "="*60)
    print("生成完成摘要")
    print("="*60)
    print(f"总节点数: {stats['total_elements']}")
    print(f"总关系数: {stats['dependencies_count']}")
    print("\n按类型分布:")
    for t, c in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
        print(f"  - {t}: {c}")
    print("\n按阶段分布:")
    for s, c in sorted(stats['by_stage'].items(), key=lambda x: -x[1]):
        print(f"  - {s}: {c}")
    print("\n按形式化等级分布:")
    for l, c in sorted(stats['by_formal_level'].items()):
        print(f"  - {l}: {c}")
    print("\n输出文件:")
    print(f"  - {OUTPUT_DIR}/schema.cypher")
    print(f"  - {OUTPUT_DIR}/nodes.cypher")
    print(f"  - {OUTPUT_DIR}/edges.cypher")
    print(f"  - {OUTPUT_DIR}/stats.json")
    print("="*60)

if __name__ == '__main__':
    main()
