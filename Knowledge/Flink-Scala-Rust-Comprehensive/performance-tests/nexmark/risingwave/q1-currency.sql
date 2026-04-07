-- Q1: Currency Conversion
-- 测试投影操作 + 简单算术运算性能

CREATE SOURCE bid (
    auction BIGINT,
    bidder BIGINT,
    price BIGINT,
    channel VARCHAR,
    url VARCHAR,
    dateTime TIMESTAMP,
    extra VARCHAR
) WITH (
    connector = 'nexmark'
) ROW FORMAT JSON;

-- 货币转换查询
CREATE MATERIALIZED VIEW q1 AS 
SELECT 
    auction, 
    bidder, 
    CAST(price * 0.908 AS BIGINT) as price, 
    dateTime, 
    extra 
FROM bid;
