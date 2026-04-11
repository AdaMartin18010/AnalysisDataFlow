// AnalysisDataFlow Neo4j 关系导入文件
// 版本: 2.0 | 生成日期: 2026-04-11
// 显式依赖关系数: 0

// ============================================
// 1. DEPENDS_ON 关系 (显式依赖)
// ============================================


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
