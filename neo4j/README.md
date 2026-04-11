# AnalysisDataFlow Neo4j 知识图谱导入指南

> **版本**: 1.0 | **更新日期**: 2026-04-11 | **数据版本**: v2.9.7

## 概述

本项目提供完整的 Neo4j 图数据库导入文件，用于交互式探索 AnalysisDataFlow 项目的**10,483形式化元素**知识图谱。

## 数据模型

### 节点类型 (Labels)

| 标签 | 说明 | 数量 (约) |
|------|------|----------|
| `FormalElement` | 通用标签 (所有元素) | 2,415 |
| `Theorem` | 形式化定理 | 405 |
| `Definition` | 形式化定义 | 1,214 |
| `Lemma` | 引理/辅助定理 | 409 |
| `Proposition` | 性质命题 | 363 |
| `Corollary` | 推论 | 24 |
| `Mapping` | 形式化映射 | 待定 |

### 节点属性

```cypher
{
  id: "Thm-S-01-01",           // 唯一标识符
  name: "USTM组合性定理",       // 元素名称
  type_abbr: "Thm",            // 类型缩写
  stage: "Struct",             // 所属阶段 (Struct/Knowledge/Flink)
  stage_abbr: "S",             // 阶段缩写
  doc_num: "01",               // 文档序号
  seq_num: 1,                  // 元素序号
  path: "Struct/01.01",        // 文档路径
  formal_level: "L4",          // 形式化等级 (L0-L6)
  status: "✅"                  // 状态标记
}
```

### 关系类型

| 关系类型 | 说明 | 方向 |
|---------|------|------|
| `DEPENDS_ON` | 显式依赖关系 | 元素 → 依赖元素 |
| `PROVES` | 引理证明定理 | 引理 → 定理 |
| `DERIVES_FROM` | 推论派生自 | 推论 → 定理/引理 |
| `INSTANTIATES` | 定义实例化 | 定义 → 定理/引理 |
| `IMPLEMENTS` | Flink实现Knowledge | Flink → Knowledge |
| `BASED_ON` | 基于理论基础 | Knowledge → Struct |
| `RELATED_TO` | 同文档关联 | 元素 ↔ 元素 |

## 导入文件清单

```
neo4j/
├── import/
│   ├── schema.cypher    # 约束和索引定义
│   ├── nodes.cypher     # 节点创建语句 (~2,415个节点)
│   ├── edges.cypher     # 关系创建语句
│   └── stats.json       # 统计信息
└── README.md            # 本文件
```

## 导入步骤

### 方法 1: 使用 Neo4j Browser (推荐初学者)

1. **启动 Neo4j 数据库**

   ```bash
   # 使用 Docker
   docker run -p 7474:7474 -p 7687:7687 \
     -e NEO4J_AUTH=neo4j/password \
     neo4j:latest
   ```

2. **访问 Neo4j Browser**
   - 打开 <http://localhost:7474>
   - 登录: `neo4j` / `password`

3. **执行导入脚本**
   - 打开 `schema.cypher`，执行创建约束和索引
   - 打开 `nodes.cypher`，执行创建节点
   - 打开 `edges.cypher`，执行创建关系

### 方法 2: 使用 Cypher Shell (命令行)

```bash
# 1. 设置环境变量
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="password"

# 2. 导入 Schema (约束和索引)
cypher-shell -u $NEO4J_USER -p $NEO4J_PASSWORD < import/schema.cypher

# 3. 导入节点
cypher-shell -u $NEO4J_USER -p $NEO4J_PASSWORD < import/nodes.cypher

# 4. 导入关系
cypher-shell -u $NEO4J_USER -p $NEO4J_PASSWORD < import/edges.cypher
```

### 方法 3: 使用 APOC 批量导入 (大数据量)

```cypher
// 使用 APOC 分批导入 (避免内存问题)
CALL apoc.periodic.iterate(
  "CALL apoc.load.csv('file:///nodes.csv') YIELD map as row RETURN row",
  "MERGE (n:FormalElement {id: row.id})
   SET n.name = row.name, n.stage = row.stage, ...",
  {batchSize: 1000, parallel: false}
)
```

## 验证导入

```cypher
// 1. 统计节点总数
MATCH (n:FormalElement)
RETURN count(n) as TotalElements;

// 2. 按类型统计
MATCH (n:FormalElement)
RETURN labels(n)[0] as Type, count(*) as Count
ORDER BY Count DESC;

// 3. 按阶段统计
MATCH (n:FormalElement)
RETURN n.stage as Stage, count(*) as Count;

// 4. 统计关系
MATCH ()-[r]->()
RETURN type(r) as RelationType, count(*) as Count;
```

## 示例查询

### 基础查询

```cypher
// 查找特定定理
MATCH (t:Theorem {id: "Thm-S-01-01"})
RETURN t;

// 查找特定阶段的所有元素
MATCH (n:FormalElement)
WHERE n.stage = "Struct"
RETURN n.id, n.name
ORDER BY n.seq_num
LIMIT 10;

// 查找特定形式化等级的元素
MATCH (n:FormalElement)
WHERE n.formal_level = "L5"
RETURN n.stage, count(*) as Count
ORDER BY Count DESC;
```

### 关系查询

```cypher
// 查找依赖链
MATCH path = (n:Theorem {id: "Thm-S-17-01"})-[:DEPENDS_ON*1..3]->(dep)
RETURN path;

// 查找证明某定理的所有引理
MATCH (l:Lemma)-[:PROVES]->(t:Theorem {id: "Thm-S-04-01"})
RETURN l.id, l.name;

// 查找高度连接的元素 (中心节点)
MATCH (n:FormalElement)-[r]->()
WITH n, count(r) as degree
ORDER BY degree DESC
LIMIT 10
RETURN n.id, n.name, n.type_abbr, degree;
```

### 路径分析

```cypher
// 查找两个元素之间的最短路径
MATCH path = shortestPath(
  (a:Theorem {id: "Thm-S-01-01"})-[:DEPENDS_ON|PROVES|DERIVES_FROM*]-(b:Theorem {id: "Thm-S-17-01"})
)
RETURN path;

// 查找文档内的所有关联元素
MATCH (n:FormalElement {path: "Struct/01.01"})-[:RELATED_TO]-(m)
RETURN n.id, m.id, m.type_abbr;
```

### 聚合分析

```cypher
// 形式化等级分布
MATCH (n:FormalElement)
RETURN n.formal_level as Level,
       count(*) as Count,
       collect(DISTINCT n.stage) as Stages
ORDER BY Level;

// 各阶段的依赖密度
MATCH (n:FormalElement)
WHERE n.stage = "Flink"
OPTIONAL MATCH (n)-[r:DEPENDS_ON]->()
WITH n, count(r) as out_deps
RETURN avg(out_deps) as AvgDependencies;
```

## 可视化建议

### Neo4j Bloom 样式

```
节点样式:
- Theorem: 红色圆圈, 大小按连接数
- Definition: 蓝色方形
- Lemma: 绿色菱形
- Proposition: 黄色三角形
- Corollary: 紫色六边形

关系样式:
- DEPENDS_ON: 虚线, 灰色
- PROVES: 实线, 绿色箭头
- DERIVES_FROM: 实线, 紫色箭头
```

### Gephi 导出

```cypher
// 导出为 Gephi 格式
CALL apoc.export.graphml.query(
  "MATCH (n:FormalElement)-[r]->(m) RETURN n, r, m",
  "knowledge-graph.graphml",
  {}
);
```

## 性能优化

### 索引建议

```cypher
// 已包含在 schema.cypher 中:
// - 唯一约束: FormalElement.id
// - 索引: stage, type, formal_level, path
// - 全文索引: name + description
```

### 查询优化

```cypher
// 使用参数化查询
:param elementId => "Thm-S-01-01";
MATCH (n:FormalElement {id: $elementId})
RETURN n;

// 限制路径长度
MATCH path = (n)-[:DEPENDS_ON*1..5]->(m)
WHERE n.id = "Thm-S-01-01"
RETURN path;
```

## 数据更新

### 增量导入

```cypher
// 仅导入新元素 (使用 MERGE 避免重复)
MERGE (n:Theorem {id: "NEW-THEOREM-ID"})
ON CREATE SET n.name = "新定理名称", ...
ON MATCH SET n.updated = datetime();
```

### 清除数据

```cypher
// 删除所有节点和关系
MATCH (n) DETACH DELETE n;

// 删除特定类型
MATCH (n:Theorem) DETACH DELETE n;
```

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| 内存不足 | 减少 BATCH_SIZE，使用 APOC 分批导入 |
| 约束冲突 | 检查重复ID，使用 MERGE 替代 CREATE |
| 关系创建失败 | 确保目标节点已创建 |
| 查询缓慢 | 检查索引是否创建，使用 EXPLAIN 分析 |

## 统计数据

当前导入包含:

- **总节点**: 2,415 个唯一形式化元素
- **定理**: 405 个
- **定义**: 1,214 个
- **引理**: 409 个
- **命题**: 363 个
- **推论**: 24 个
- **阶段分布**: Flink (1,342) / Knowledge (673) / Struct (400)

## 参考资料

- [Neo4j Cypher 文档](https://neo4j.com/docs/cypher-manual/)
- [Neo4j Browser 指南](https://neo4j.com/docs/browser-manual/)
- [APOC 库文档](https://neo4j.com/docs/apoc/)
- AnalysisDataFlow 项目文档

## 许可证

与 AnalysisDataFlow 项目相同许可证。

---

**维护者**: AnalysisDataFlow 团队
**最后更新**: 2026-04-11
