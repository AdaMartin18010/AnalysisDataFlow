-- PostgreSQL 初始化脚本
-- Flink Playground 数据库设置

-- 创建结果表
CREATE TABLE IF NOT EXISTS word_count_results (
    word VARCHAR(255) PRIMARY KEY,
    count BIGINT NOT NULL,
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sensor_readings (
    sensor_id VARCHAR(50) NOT NULL,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    reading_time TIMESTAMP NOT NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sensor_time ON sensor_readings(sensor_id, reading_time);

CREATE TABLE IF NOT EXISTS user_events (
    user_id VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    page_url TEXT,
    session_id VARCHAR(100),
    event_time TIMESTAMP NOT NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_events_time ON user_events(event_time);
CREATE INDEX IF NOT EXISTS idx_user_events_session ON user_events(session_id);

CREATE TABLE IF NOT EXISTS aggregated_metrics (
    metric_name VARCHAR(100) NOT NULL,
    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL,
    value DOUBLE PRECISION,
    count BIGINT,
    PRIMARY KEY (metric_name, window_start, window_end)
);

CREATE TABLE IF NOT EXISTS alert_log (
    alert_id SERIAL PRIMARY KEY,
    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    message TEXT,
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- 创建视图
CREATE OR REPLACE VIEW latest_word_counts AS
SELECT word, count, updated_at
FROM word_count_results
ORDER BY count DESC;

CREATE OR REPLACE VIEW sensor_stats AS
SELECT 
    sensor_id,
    COUNT(*) as reading_count,
    AVG(temperature) as avg_temp,
    MAX(temperature) as max_temp,
    MIN(temperature) as min_temp,
    AVG(humidity) as avg_humidity
FROM sensor_readings
GROUP BY sensor_id;
