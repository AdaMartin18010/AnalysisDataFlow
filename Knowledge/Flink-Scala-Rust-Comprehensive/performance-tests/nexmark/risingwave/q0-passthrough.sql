-- Q0: Passthrough 基准测试
-- 测试流处理引擎的基础开销（解析、序列化、网络传输）

CREATE SOURCE bid (
    auction BIGINT,
    bidder BIGINT,
    price BIGINT,
    channel VARCHAR,
    url VARCHAR,
    dateTime TIMESTAMP,
    extra VARCHAR
) WITH (
    connector = 'nexmark',
    nexmark.split.num = '4',
    nexmark.event.num = '100000000'
) ROW FORMAT JSON;

-- 创建物化视图 - 简单的透传
CREATE MATERIALIZED VIEW q0 AS 
SELECT * FROM bid;

-- 可选：添加输出 sink 用于验证
-- CREATE SINK q0_sink FROM q0
-- WITH (
--     connector = 'blackhole'
-- );
