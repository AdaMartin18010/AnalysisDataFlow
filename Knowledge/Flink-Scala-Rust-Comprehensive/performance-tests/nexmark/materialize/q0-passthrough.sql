-- Q0: Passthrough 基准测试
-- Materialize 实现

CREATE SOURCE bid (
    auction BIGINT,
    bidder BIGINT,
    price BIGINT,
    channel TEXT,
    url TEXT,
    dateTime TIMESTAMP,
    extra TEXT
) FROM LOAD GENERATOR AUCTION FOR ALL TABLES;

-- 创建物化视图
CREATE MATERIALIZED VIEW q0 AS SELECT * FROM bid;
