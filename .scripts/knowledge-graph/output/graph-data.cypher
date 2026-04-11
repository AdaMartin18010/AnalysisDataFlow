// 概念图谱Cypher导入脚本
// 生成时间: 2026-04-11T15:41:21.357983

CREATE CONSTRAINT concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE;

CREATE (c_Def_S_01_01:Concept {
    id: "Def-S-01-01",
    name: "Event Time定义",
    category: "definition",
    source_file: "Struct/1.1-streaming-foundations.md",
    definition: "事件时间是指事件实际发生的时间..."
});

CREATE (c_Def_S_01_02:Concept {
    id: "Def-S-01-02",
    name: "Processing Time定义",
    category: "definition",
    source_file: "Struct/1.1-streaming-foundations.md",
    definition: "处理时间是指事件被处理的时间..."
});

CREATE (c_Thm_S_01_01:Concept {
    id: "Thm-S-01-01",
    name: "流计算基本定理",
    category: "theorem",
    source_file: "Struct/1.1-streaming-foundations.md",
    definition: "流计算系统的基本理论性质..."
});

CREATE (c_Def_S_01_01)-[:REFERENCES {weight: 1.0}]->(c_Thm_S_01_01);
CREATE (c_Def_S_01_02)-[:REFERENCES {weight: 1.0}]->(c_Thm_S_01_01);

CREATE INDEX concept_category IF NOT EXISTS FOR (c:Concept) ON (c.category);
