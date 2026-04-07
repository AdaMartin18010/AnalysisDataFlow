-- Q5: Hot Items
-- 滑动窗口 Top-N 查询
-- 测试窗口聚合性能

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

-- 创建滑动窗口物化视图
CREATE MATERIALIZED VIEW q5 AS
WITH max_prices AS (
    SELECT 
        auction,
        MAX(price) as max_price,
        window_start
    FROM TUMBLE(bid, dateTime, INTERVAL '60' SECOND)
    GROUP BY auction, window_start
),
ranked AS (
    SELECT 
        auction,
        max_price,
        window_start,
        ROW_NUMBER() OVER (PARTITION BY window_start ORDER BY max_price DESC) as rank
    FROM max_prices
)
SELECT auction, max_price as price, window_start
FROM ranked
WHERE rank = 1;
