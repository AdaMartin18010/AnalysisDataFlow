// AnalysisDataFlow Neo4j Graph Database Schema
// 创建约束和索引以优化知识图谱查询
// 版本: 1.0 | 生成日期: 2026-04-11

// ============================================
// 1. 创建节点约束 (唯一性)
// ============================================

// 为所有形式化元素创建唯一约束
CREATE CONSTRAINT formal_element_id IF NOT EXISTS
FOR (n:FormalElement) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT theorem_id IF NOT EXISTS
FOR (n:Theorem) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT definition_id IF NOT EXISTS
FOR (n:Definition) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT lemma_id IF NOT EXISTS
FOR (n:Lemma) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT proposition_id IF NOT EXISTS
FOR (n:Proposition) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT corollary_id IF NOT EXISTS
FOR (n:Corollary) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT mapping_id IF NOT EXISTS
FOR (n:Mapping) REQUIRE n.id IS UNIQUE;

// ============================================
// 2. 创建索引 (加速查询)
// ============================================

// 按类型索引
CREATE INDEX element_type_index IF NOT EXISTS
FOR (n:FormalElement) ON (n.type);

// 按阶段索引 (Struct/Knowledge/Flink)
CREATE INDEX element_stage_index IF NOT EXISTS
FOR (n:FormalElement) ON (n.stage);

// 按形式化等级索引
CREATE INDEX element_level_index IF NOT EXISTS
FOR (n:FormalElement) ON (n.formal_level);

// 按文档路径索引
CREATE INDEX element_path_index IF NOT EXISTS
FOR (n:FormalElement) ON (n.path);

// 按名称索引 (支持模糊搜索)
CREATE INDEX element_name_index IF NOT EXISTS
FOR (n:FormalElement) ON (n.name);

// 复合索引: 阶段 + 类型
CREATE INDEX element_stage_type_index IF NOT EXISTS
FOR (n:FormalElement) ON (n.stage, n.type);

// 全文搜索索引 (名称和描述)
CREATE FULLTEXT INDEX element_name_description_search IF NOT EXISTS
FOR (n:FormalElement) ON EACH [n.name, n.description];

// ============================================
// 3. 创建关系约束
// ============================================

// 确保关系类型一致性
CREATE CONSTRAINT depends_on_rel IF NOT EXISTS
FOR ()-[r:DEPENDS_ON]-() REQUIRE r.type IS NOT NULL;

// ============================================
// 4. 统计信息提示
// ============================================

CALL db.schema.visualization();

// 显示所有索引和约束
SHOW CONSTRAINTS;
SHOW INDEXES;
