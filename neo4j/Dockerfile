# AnalysisDataFlow Neo4j 图数据库 Dockerfile
# 版本: 1.0 | 更新日期: 2026-04-11

FROM neo4j:5.15-community

LABEL maintainer="AnalysisDataFlow Team"
LABEL description="Neo4j Graph Database for AnalysisDataFlow Knowledge Graph"
LABEL version="1.0"

# 安装必要的工具
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    procps \
    && rm -rf /var/lib/apt/lists/*

# 创建导入目录结构
RUN mkdir -p /import /plugins /queries /reports

# 复制初始化脚本
COPY import/schema.cypher /import/
COPY import/nodes.cypher /import/
COPY import/edges.cypher /import/

# 设置权限
RUN chmod -R 755 /import /plugins /queries /reports

# 安装APOC插件
ENV NEO4J_apoc_export_file_enabled=true
ENV NEO4J_apoc_import_file_enabled=true
ENV NEO4J_apoc_import_file_use__neo4j__config=true
ENV NEO4J_dbms_security_procedures_unrestricted=apoc.*

# 下载APOC插件
RUN curl -L -o /plugins/apoc-5.15.0-extended.jar https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/5.15.0/apoc-5.15.0-extended.jar || true
RUN curl -L -o /plugins/apoc-5.15.0-core.jar https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/5.15.0/apoc-5.15.0-core.jar || true

# 暴露端口
EXPOSE 7474 7687

# 健康检查
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
    CMD cypher-shell -u neo4j -p ${NEO4J_PASSWORD:-analysis123} 'RETURN 1' || exit 1

# 启动命令
CMD ["neo4j"]
