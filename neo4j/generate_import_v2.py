#!/usr/bin/env python3
"""
AnalysisDataFlow Neo4j 图数据库导入文件生成器 v2
解析 THEOREM-REGISTRY.md 生成 Cypher 导入语句
支持多种表格格式
"""

import re
import json
from collections import defaultdict
from pathlib import Path

# 配置
INPUT_FILE = "THEOREM-REGISTRY.md"
OUTPUT_DIR = Path("neo4j/import")
BATCH_SIZE = 500

# 确保输出目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 类型映射
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

def extract_id_from_line(line):
    """从行中提取元素ID"""
    # 匹配 Thm-S-01-01, Def-K-02-001, Lemma-F-10-40 等
    pattern = r'(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{1,3})'
    match = re.search(pattern, line)
    if match:
        return match.group(0)
    return None

def parse_element_id(element_id):
    """解析元素ID为组成部分"""
    parts = element_id.split('-')
    if len(parts) >= 4:
        return {
            'id': element_id,
            'type_abbr': parts[0],
            'type': TYPE_MAPPING.get(parts[0], parts[0]),
            'stage_abbr': parts[1],
            'stage': STAGE_MAPPING.get(parts[1], parts[1]),
            'doc_num': parts[2],
            'seq_num': parts[3]
        }
    return None

def parse_full_format_line(line):
    """解析完整格式行: | ID | Name | Path | Level | Depends | Status |"""
    # 分割并清理
    parts = [p.strip() for p in line.split('|')]
    parts = [p for p in parts if p]  # 移除空字符串
    
    if len(parts) >= 6:
        element_id = parts[0]
        name = parts[1]
        path = parts[2]
        level = parts[3] if len(parts) > 3 else '-'
        depends = parts[4] if len(parts) > 4 else '-'
        status = parts[5] if len(parts) > 5 else '✅'
        
        parsed = parse_element_id(element_id)
        if parsed:
            parsed['name'] = name
            parsed['path'] = path
            parsed['formal_level'] = parse_formal_level(level)
            parsed['dependencies'] = extract_dependencies(depends)
            parsed['status'] = status
            return parsed
    return None

def parse_simple_format_line(line):
    """解析简化格式行: | ID | Path | Status |"""
    parts = [p.strip() for p in line.split('|')]
    parts = [p for p in parts if p]
    
    if len(parts) >= 2:
        element_id = parts[0]
        path = parts[1]
        status = parts[2] if len(parts) > 2 else '✅'
        
        parsed = parse_element_id(element_id)
        if parsed:
            # 生成默认名称
            parsed['name'] = f"{parsed['type']} {element_id}"
            parsed['path'] = path
            parsed['formal_level'] = 'L0'
            parsed['dependencies'] = []
            parsed['status'] = status
            return parsed
    return None

def parse_formal_level(level_str):
    """解析形式化等级"""
    if not level_str or level_str.strip() in ['-', '']:
        return 'L0'
    level_str = level_str.strip()
    if '-' in level_str and level_str.startswith('L'):
        return level_str.split('-')[0].strip()
    if level_str.startswith('L') and len(level_str) >= 2:
        return level_str[:2]
    return 'L0'

def extract_dependencies(depends_str):
    """提取依赖ID列表"""
    if not depends_str or depends_str.strip() in ['-', '']:
        return []
    pattern = r'(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d{2}-\d{1,3}'
    return re.findall(pattern, depends_str)

def sanitize_cypher_string(s):
    """转义Cypher字符串"""
    if not s:
        return ""
    s = s.strip()
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace("'", "\\'")
    s = ''.join(char for char in s if ord(char) >= 32 or char in '\n\t')
    return s[:500]  # 限制长度

def parse_registry():
    """解析整个注册表文件"""
    elements = []
    seen_ids = set()
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"错误: 无法读取文件: {e}")
        return elements
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line.startswith('|') or '---' in line or '编号' in line:
            continue
        
        element = None
        
        # 尝试完整格式
        if line.count('|') >= 7:
            element = parse_full_format_line(line)
        
        # 尝试简化格式
        if not element:
            element = parse_simple_format_line(line)
        
        if element and element['id'] not in seen_ids:
            seen_ids.add(element['id'])
            # 清理名称
            element['name'] = sanitize_cypher_string(element['name'])
            element['path'] = sanitize_cypher_string(element['path'])
            elements.append(element)
    
    return elements

def generate_nodes_cypher(elements):
    """生成节点创建Cypher语句"""
    output_file = OUTPUT_DIR / "nodes.cypher"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"""// AnalysisDataFlow Neo4j 节点导入文件
// 包含所有形式化元素: 定理、定义、引理、命题、推论
// 版本: 2.0 | 生成日期: 2026-04-11
// 总节点数: {len(elements)}

// ============================================
// 节点创建语句
// ============================================

""")
        
        # 按类型分组
        by_type = defaultdict(list)
        for elem in elements:
            by_type[elem['type']].append(elem)
        
        # 为每种类型生成MERGE语句
        for node_type in ['Theorem', 'Definition', 'Lemma', 'Proposition', 'Corollary']:
            elems = by_type.get(node_type, [])
            if not elems:
                continue
            
            f.write(f"\n// ---------- {node_type} ({len(elems)}个) ----------\n")
            
            for i in range(0, len(elems), BATCH_SIZE):
                batch = elems[i:i+BATCH_SIZE]
                f.write(f"\n// Batch {i//BATCH_SIZE + 1}/{ (len(elems) + BATCH_SIZE - 1)//BATCH_SIZE }\n")
                
                for elem in batch:
                    cypher = f"""MERGE (n:{node_type} {{id: "{elem['id']}"}})
ON CREATE SET n.name = "{elem['name']}",
              n.stage = "{elem['stage']}",
              n.stage_abbr = "{elem['stage_abbr']}",
              n.doc_num = "{elem['doc_num']}",
              n.seq_num = {elem['seq_num']},
              n.path = "{elem['path']}",
              n.formal_level = "{elem['formal_level']}",
              n.type_abbr = "{elem['type_abbr']}",
              n.status = "{elem['status']}"
ON MATCH SET n.name = "{elem['name']}",
             n.stage = "{elem['stage']}",
             n.stage_abbr = "{elem['stage_abbr']}",
             n.doc_num = "{elem['doc_num']}",
             n.seq_num = {elem['seq_num']},
             n.path = "{elem['path']}",
             n.formal_level = "{elem['formal_level']}",
             n.type_abbr = "{elem['type_abbr']}",
             n.status = "{elem['status']}";
"""
                    f.write(cypher)
        
        # 添加通用标签
        f.write("""
// ============================================
// 添加通用标签 FormalElement
// ============================================

MATCH (n) WHERE n:Theorem OR n:Definition OR n:Lemma OR n:Proposition OR n:Corollary
  AND NOT n:FormalElement
SET n:FormalElement;

// ============================================
// 统计验证
// ============================================

// 总节点数
MATCH (n:FormalElement) RETURN count(n) as TotalElements;

// 按类型统计
MATCH (n:FormalElement)
RETURN labels(n)[0] as Type, count(*) as Count
ORDER BY Count DESC;

// 按阶段统计
MATCH (n:FormalElement)
RETURN n.stage as Stage, count(*) as Count
ORDER BY Count DESC;

// 按形式化等级统计
MATCH (n:FormalElement)
RETURN n.formal_level as Level, count(*) as Count
ORDER BY Level;
""")
    
    print(f"✅ 节点文件: {output_file} ({len(elements)} 个节点)")
    return len(elements)

def generate_edges_cypher(elements):
    """生成关系创建Cypher语句"""
    output_file = OUTPUT_DIR / "edges.cypher"
    
    # 构建ID映射
    id_to_elem = {elem['id']: elem for elem in elements}
    
    # 收集依赖关系
    dependencies = []
    for elem in elements:
        for dep_id in elem['dependencies']:
            if dep_id in id_to_elem:
                dependencies.append({
                    'from_id': elem['id'],
                    'to_id': dep_id,
                    'from_type': elem['type'],
                    'to_type': id_to_elem[dep_id]['type']
                })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"""// AnalysisDataFlow Neo4j 关系导入文件
// 版本: 2.0 | 生成日期: 2026-04-11
// 显式依赖关系数: {len(dependencies)}

// ============================================
// 1. DEPENDS_ON 关系 (显式依赖)
// ============================================

""")
        
        # 写入依赖关系
        for i in range(0, len(dependencies), BATCH_SIZE):
            batch = dependencies[i:i+BATCH_SIZE]
            f.write(f"\n// Batch {i//BATCH_SIZE + 1}\n")
            
            for dep in batch:
                cypher = f"""MATCH (a {{id: "{dep['from_id']}"}}), (b {{id: "{dep['to_id']}"}})
MERGE (a)-[r:DEPENDS_ON]->(b)
ON CREATE SET r.inferred = false, r.type = 'explicit';
"""
                f.write(cypher)
        
        # 添加推断关系
        f.write("""
// ============================================
// 2. 推断关系 (基于规则)
// ============================================

// 引理证明定理 (同文档同序号的引理和定理)
MATCH (lemma:Lemma), (theorem:Theorem)
WHERE lemma.stage_abbr = theorem.stage_abbr 
  AND lemma.doc_num = theorem.doc_num
  AND lemma.seq_num = theorem.seq_num
  AND NOT (lemma)-[:DEPENDS_ON]->(theorem)
MERGE (lemma)-[r:PROVES]->(theorem)
ON CREATE SET r.inferred = true;

// 推论派生自定理
MATCH (cor:Corollary), (th:Theorem)
WHERE cor.path = th.path
  AND NOT (cor)-[:DEPENDS_ON]->(th)
MERGE (cor)-[r:DERIVES_FROM]->(th)
ON CREATE SET r.inferred = true;

// 推论派生自引理
MATCH (cor:Corollary), (lm:Lemma)
WHERE cor.path = lm.path
  AND NOT (cor)-[:DEPENDS_ON]->(lm)
  AND NOT (cor)-[:DERIVES_FROM]->(:Theorem)
MERGE (cor)-[r:DERIVES_FROM]->(lm)
ON CREATE SET r.inferred = true;

// 定义实例化定理
MATCH (def:Definition), (th:Theorem)
WHERE def.path = th.path
  AND NOT (def)-[:DEPENDS_ON]->(th)
MERGE (def)-[r:INSTANTIATES]->(th)
ON CREATE SET r.inferred = true;

// 定义实例化引理
MATCH (def:Definition), (lm:Lemma)
WHERE def.path = lm.path
  AND NOT (def)-[:DEPENDS_ON]->(lm)
  AND NOT (def)-[:INSTANTIATES]->(:Theorem)
MERGE (def)-[r:INSTANTIATES]->(lm)
ON CREATE SET r.inferred = true;

// 同路径元素关联
MATCH (a:FormalElement), (b:FormalElement)
WHERE a.id <> b.id 
  AND a.path = b.path
  AND a.stage_abbr = b.stage_abbr
  AND a.doc_num = b.doc_num
  AND NOT (a)-[:DEPENDS_ON|PROVES|DERIVES_FROM|INSTANTIATES]-(b)
MERGE (a)-[r:RELATED_TO]->(b)
ON CREATE SET r.basis = 'same_document';

// ============================================
// 3. 跨阶段关系
// ============================================

// Flink实现Knowledge概念
MATCH (f:FormalElement) WHERE f.stage = "Flink"
MATCH (k:FormalElement) WHERE k.stage = "Knowledge"
  AND (f.name CONTAINS k.name OR k.name CONTAINS f.name)
  AND f.name <> k.name
MERGE (f)-[r:IMPLEMENTS]->(k)
ON CREATE SET r.inferred = true;

// Struct是基础理论
MATCH (s:FormalElement) WHERE s.stage = "Struct"
MATCH (k:FormalElement) WHERE k.stage = "Knowledge"
  AND (k.name CONTAINS s.name OR s.name CONTAINS k.name)
MERGE (k)-[r:BASED_ON]->(s)
ON CREATE SET r.inferred = true;

// ============================================
// 4. 统计验证
// ============================================

// 各类型关系数量
MATCH ()-[r]->()
RETURN type(r) as RelationType, count(*) as Count
ORDER BY Count DESC;

// 高度连接的元素 (Top 20)
MATCH (n:FormalElement)-[r]->()
WITH n, count(r) as out_degree
ORDER BY out_degree DESC
LIMIT 20
RETURN n.id as ID, n.name as Name, n.type_abbr as Type, out_degree as OutDegree;

// 被依赖最多的元素 (Top 20)
MATCH (n:FormalElement)<-[r:DEPENDS_ON]-()
WITH n, count(r) as in_degree
ORDER BY in_degree DESC
LIMIT 20
RETURN n.id as ID, n.name as Name, n.type_abbr as Type, in_degree as InDegree;
""")
    
    print(f"✅ 关系文件: {output_file} ({len(dependencies)} 个显式依赖)")
    return len(dependencies)

def generate_stats(elements, edge_count):
    """生成统计信息"""
    stats = {
        'total_elements': len(elements),
        'by_type': {},
        'by_stage': {},
        'by_formal_level': {},
        'dependencies_count': edge_count,
        'by_doc': defaultdict(int)
    }
    
    for elem in elements:
        stats['by_type'][elem['type']] = stats['by_type'].get(elem['type'], 0) + 1
        stats['by_stage'][elem['stage']] = stats['by_stage'].get(elem['stage'], 0) + 1
        stats['by_formal_level'][elem['formal_level']] = stats['by_formal_level'].get(elem['formal_level'], 0) + 1
        doc_key = f"{elem['stage']}/{elem['doc_num']}"
        stats['by_doc'][doc_key] += 1
    
    stats['by_doc'] = dict(stats['by_doc'])
    
    output_file = OUTPUT_DIR / "stats.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 统计文件: {output_file}")
    return stats

def main():
    print("="*60)
    print("AnalysisDataFlow Neo4j 导入文件生成器 v2")
    print("="*60)
    
    print(f"\n📖 解析 {INPUT_FILE}...")
    elements = parse_registry()
    
    if not elements:
        print("❌ 未能解析到任何元素")
        return
    
    print(f"✅ 解析到 {len(elements)} 个形式化元素")
    
    print("\n📝 生成节点文件...")
    node_count = generate_nodes_cypher(elements)
    
    print("\n🔗 生成关系文件...")
    edge_count = generate_edges_cypher(elements)
    
    print("\n📊 生成统计信息...")
    stats = generate_stats(elements, edge_count)
    
    print("\n" + "="*60)
    print("生成完成摘要")
    print("="*60)
    print(f"总节点数: {stats['total_elements']}")
    print(f"显式依赖关系: {stats['dependencies_count']}")
    print("\n按类型分布:")
    for t, c in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
        print(f"  - {t}: {c}")
    print("\n按阶段分布:")
    for s, c in sorted(stats['by_stage'].items(), key=lambda x: -x[1]):
        print(f"  - {s}: {c}")
    print("\n文件输出:")
    print(f"  - {OUTPUT_DIR}/schema.cypher")
    print(f"  - {OUTPUT_DIR}/nodes.cypher")
    print(f"  - {OUTPUT_DIR}/edges.cypher")
    print(f"  - {OUTPUT_DIR}/stats.json")
    print("="*60)

if __name__ == '__main__':
    main()
