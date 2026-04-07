-- Q5: Hot Items
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

-- 创建滑动窗口物化视图
CREATE MATERIALIZED VIEW q5 AS
SELECT DISTINCT ON (window_start)
    auction,
    max_price as price,
    window_start
FROM (
    SELECT 
        auction,
        MAX(price) as max_price,
        date_trunc('minute', dateTime) as window_start
    FROM bid
    GROUP BY auction, date_trunc('minute', dateTime)
) sub
ORDER BY window_start, max_price DESC;
