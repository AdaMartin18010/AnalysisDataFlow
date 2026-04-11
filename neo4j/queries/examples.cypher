// AnalysisDataFlow Neo4j 示例查询库
// 版本: 1.0 | 生成日期: 2026-04-11
// 包含常用查询模板和验证查询

// ============================================
// 1. 基础统计查询
// ============================================

// 1.1 统计所有节点总数
MATCH (n:FormalElement)
RETURN count(n) as TotalNodes;

// 1.2 按标签类型统计节点
MATCH (n)
RETURN labels(n)[0] as NodeType, count(*) as Count
ORDER BY Count DESC;

// 1.3 按阶段统计
MATCH (n:FormalElement)
RETURN n.stage as Stage, count(*) as Count
ORDER BY Count DESC;

// 1.4 按形式化等级统计
MATCH (n:FormalElement)
RETURN n.formal_level as FormalLevel, count(*) as Count
ORDER BY FormalLevel;

// ============================================
// 2. 关系统计查询
// ============================================

// 2.1 统计所有关系
MATCH ()-[r]->()
RETURN count(r) as TotalRelations;

// 2.2 按关系类型统计
MATCH ()-[r]->()
RETURN type(r) as RelationType, count(*) as Count
ORDER BY Count DESC;

// ============================================
// 3. 特定元素查询
// ============================================

// 3.1 查找特定定理 (USTM组合性定理)
MATCH (t:Theorem {id: "Thm-S-01-01"})
RETURN t.id, t.name, t.stage, t.formal_level;

// 3.2 查找特定文档的所有元素
MATCH (n:FormalElement)
WHERE n.path = "Struct/01.01"
RETURN n.id, n.name, labels(n)[0] as Type
ORDER BY n.seq_num;

// 3.3 查找所有L5/L6高形式化等级元素
MATCH (n:FormalElement)
WHERE n.formal_level IN ["L5", "L6"]
RETURN n.id, n.name, n.stage, n.formal_level
ORDER BY n.formal_level DESC, n.stage
LIMIT 20;

// ============================================
// 4. 依赖关系查询
// ============================================

// 4.1 查找证明某定理的所有引理
MATCH (l:Lemma)-[:PROVES]->(t:Theorem {id: "Thm-S-04-01"})
RETURN l.id, l.name;

// 4.2 查找从某元素出发的依赖链 (1-3层)
MATCH path = (n:Theorem {id: "Thm-S-17-01"})-[:DEPENDS_ON|PROVES*1..3]->(dep)
RETURN path
LIMIT 10;

// 4.3 查找高度连接的元素 (Top 10)
MATCH (n:FormalElement)-[r]->()
WITH n, count(r) as out_degree
ORDER BY out_degree DESC
LIMIT 10
RETURN n.id as ID, n.name as Name, n.type_abbr as Type, out_degree as OutDegree;

// ============================================
// 5. 跨阶段关系查询
// ============================================

// 5.1 查找Flink实现Knowledge概念的关系
MATCH (f:FormalElement)-[r:IMPLEMENTS]->(k:FormalElement)
WHERE f.stage = "Flink" AND k.stage = "Knowledge"
RETURN f.id, f.name, k.id, k.name
LIMIT 10;

// 5.2 查找基于Struct理论的Knowledge元素
MATCH (k:FormalElement)-[r:BASED_ON]->(s:FormalElement)
WHERE k.stage = "Knowledge" AND s.stage = "Struct"
RETURN k.id, k.name, s.id, s.name
LIMIT 10;

// ============================================
// 6. 路径分析查询
// ============================================

// 6.1 查找两个定理之间的最短路径
MATCH path = shortestPath(
  (a:Theorem {id: "Thm-S-01-01"})-[:DEPENDS_ON|PROVES|DERIVES_FROM|INSTANTIATES*]-(b:Theorem {id: "Thm-S-17-01"})
)
RETURN path;

// 6.2 查找同文档内所有关联元素
MATCH (n:FormalElement {path: "Struct/02.02"})-[:RELATED_TO]-(m)
RETURN n.id, m.id, m.type_abbr
LIMIT 20;

// ============================================
// 7. 聚合分析查询
// ============================================

// 7.1 各阶段的形式化等级分布
MATCH (n:FormalElement)
RETURN n.stage as Stage, 
       n.formal_level as Level, 
       count(*) as Count
ORDER BY Stage, Level;

// 7.2 每个文档的元素数量
MATCH (n:FormalElement)
WITH n.path as Path, count(*) as Count
ORDER BY Count DESC
LIMIT 20
RETURN Path, Count;

// 7.3 按阶段和类型统计
MATCH (n:FormalElement)
RETURN n.stage as Stage,
       labels(n)[0] as Type,
       count(*) as Count
ORDER BY Stage, Count DESC;

// ============================================
// 8. 全文搜索查询
// ============================================

// 8.1 搜索包含特定关键词的元素 (需要全文索引)
CALL db.index.fulltext.queryNodes('element_name_description_search', 'Checkpoint') 
YIELD node, score
RETURN node.id, node.name, node.stage, score
LIMIT 10;

// 8.2 模糊搜索元素名称
MATCH (n:FormalElement)
WHERE n.name CONTAINS "Exactly-Once"
RETURN n.id, n.name, n.stage, labels(n)[0] as Type
ORDER BY n.stage;

// ============================================
// 9. 验证查询
// ============================================

// 9.1 验证节点总数是否为2415
MATCH (n:FormalElement)
WITH count(n) as Total
RETURN Total, 
       CASE WHEN Total = 2415 THEN '✅ PASS' ELSE '❌ FAIL' END as Status;

// 9.2 验证各类型数量
MATCH (n)
RETURN labels(n)[0] as Type, count(*) as Count,
       CASE labels(n)[0]
         WHEN 'Theorem' THEN CASE WHEN count(*) = 405 THEN '✅' ELSE '❌' END
         WHEN 'Definition' THEN CASE WHEN count(*) = 1214 THEN '✅' ELSE '❌' END
         WHEN 'Lemma' THEN CASE WHEN count(*) = 409 THEN '✅' ELSE '❌' END
         WHEN 'Proposition' THEN CASE WHEN count(*) = 363 THEN '✅' ELSE '❌' END
         WHEN 'Corollary' THEN CASE WHEN count(*) = 24 THEN '✅' ELSE '❌' END
         ELSE 'ℹ️'
       END as Verification;

// ============================================
// 10. 导出查询
// ============================================

// 10.1 导出所有节点为CSV (需要APOC)
// CALL apoc.export.csv.query(
//   "MATCH (n:FormalElement) RETURN n.id, n.name, n.stage, n.formal_level",
//   "nodes_export.csv",
//   {}
// );

// 10.2 导出子图为GraphML (需要APOC)
// CALL apoc.export.graphml.query(
//   "MATCH (n:FormalElement)-[r]->(m) RETURN n, r, m LIMIT 100",
//   "knowledge_graph_subset.graphml",
//   {}
// );
