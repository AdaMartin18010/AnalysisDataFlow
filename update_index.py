import re

path = 'phase2-case-studies/CASE-STUDIES-INDEX.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Finance & Insurance: add status column and banking row
old_finance = """### 金融与保险 (Finance & Insurance)

| 编号 | 行业 | 案例名称 | 文件 |
|------|------|----------|------|
| 11.13.1 | 金融 | 实时风控 | risk-control.md |
| 11.18.1 | 保险 | 理赔处理 | claims-processing.md |"""
new_finance = """### 金融与保险 (Finance & Insurance)

| 编号 | 行业 | 案例名称 | 文件 | 状态 |
|------|------|----------|------|------|
| 11.13.1 | 金融 | 实时风控 | risk-control.md | 初稿 |
| 11.18.1 | 保险 | 理赔处理 | claims-processing.md | **深度完成** |
| 11.37.1 | 银行 | 实时支付 | 11.37.1-realtime-payment.md | **深度完成** |"""
content = content.replace(old_finance, new_finance)

# 2. Retail & E-commerce: add status column and mark retail
old_retail = """### 零售与电商 (Retail & E-commerce)

| 编号 | 行业 | 案例名称 | 文件 |
|------|------|----------|------|
| 11.11.1 | 电商 | 实时推荐 | realtime-recommendation.md |
| 11.17.1 | 零售 | 动态定价 | realtime-pricing.md |
| 11.29.1 | 时尚 | 库存管理 | inventory.md |"""
new_retail = """### 零售与电商 (Retail & E-commerce)

| 编号 | 行业 | 案例名称 | 文件 | 状态 |
|------|------|----------|------|------|
| 11.11.1 | 电商 | 实时推荐 | realtime-recommendation.md | 初稿 |
| 11.17.1 | 零售 | 动态定价 | realtime-pricing.md | **深度完成** |
| 11.29.1 | 时尚 | 库存管理 | inventory.md | 初稿 |"""
content = content.replace(old_retail, new_retail)

# 3. Manufacturing & Industry: add status column and mark two rows
old_mfg = """### 制造与工业 (Manufacturing & Industry)

| 编号 | 行业 | 案例名称 | 文件 |
|------|------|----------|------|
| 11.14.1 | 制造 | 预测性维护 | predictive-maintenance.md |
| 11.8.1 | 石化 | 管道泄漏检测 | pipeline-leak.md |
| 11.27.1 | 矿业 | 安全监控 | mining-safety.md |
| 11.31.1 | 建筑 | 工地安全 | safety.md |"""
new_mfg = """### 制造与工业 (Manufacturing & Industry)

| 编号 | 行业 | 案例名称 | 文件 | 状态 |
|------|------|----------|------|------|
| 11.14.1 | 制造 | 预测性维护 | predictive-maintenance.md | **深度完成** |
| 11.8.1 | 石化 | 管道泄漏检测 | pipeline-leak.md | **深度完成** |
| 11.27.1 | 矿业 | 安全监控 | mining-safety.md | 初稿 |
| 11.31.1 | 建筑 | 工地安全 | safety.md | 初稿 |"""
content = content.replace(old_mfg, new_mfg)

# 4. Internet & Media: update livestreaming status
old_media = "| 11.20.1 | 传媒 | 直播互动 | livestreaming.md | 初稿 |"
new_media = "| 11.20.1 | 传媒 | 直播互动 | livestreaming.md | **深度完成** |"
content = content.replace(old_media, new_media)

# 5. Aerospace & Aviation: add status column and mark flight-data
old_aero = """### 航空航天 (Aerospace & Aviation)

| 编号 | 行业 | 案例名称 | 文件 |
|------|------|----------|------|
| 11.7.1 | 航空航天 | 飞行数据监控 | flight-data.md |
| 11.32.1 | 航空 | 行李追踪 | baggage.md |"""
new_aero = """### 航空航天 (Aerospace & Aviation)

| 编号 | 行业 | 案例名称 | 文件 | 状态 |
|------|------|----------|------|------|
| 11.7.1 | 航空航天 | 飞行数据监控 | flight-data.md | **深度完成** |
| 11.32.1 | 航空 | 行李追踪 | baggage.md | 初稿 |"""
content = content.replace(old_aero, new_aero)

# 6. Telecom & Network: add status column and mark network-traffic
old_telecom = """### 电信与网络 (Telecom & Network)

| 编号 | 行业 | 案例名称 | 文件 |
|------|------|----------|------|
| 11.9.1 | 电信 | 网络流量分析 | network-traffic.md |"""
new_telecom = """### 电信与网络 (Telecom & Network)

| 编号 | 行业 | 案例名称 | 文件 | 状态 |
|------|------|----------|------|------|
| 11.9.1 | 电信 | 网络流量分析 | network-traffic.md | **深度完成** |"""
content = content.replace(old_telecom, new_telecom)

# 7. Education & Sports: add status column and mark online-learning
old_edu = """### 教育与体育 (Education & Sports)

| 编号 | 行业 | 案例名称 | 文件 |
|------|------|----------|------|
| 11.22.1 | 教育 | 在线学习分析 | online-learning.md |
| 11.24.1 | 体育 | 赛事分析 | sports-analytics.md |"""
new_edu = """### 教育与体育 (Education & Sports)

| 编号 | 行业 | 案例名称 | 文件 | 状态 |
|------|------|----------|------|------|
| 11.22.1 | 教育 | 在线学习分析 | online-learning.md | **深度完成** |
| 11.24.1 | 体育 | 赛事分析 | sports-analytics.md | 初稿 |"""
content = content.replace(old_edu, new_edu)

# 8. Smart City & Transportation: add status column and mark two rows
old_city = """### 智慧城市与交通 (Smart City & Transportation)

| 编号 | 行业 | 案例名称 | 文件 |
|------|------|----------|------|
| 11.3.1 | 智慧城市 | 交通流量分析 | traffic-flow-analysis.md |
| 11.6.1 | 自动驾驶 | 传感器融合 | sensor-fusion.md |
| 11.21.1 | 房地产 | 智慧楼宇 | smart-building.md |"""
new_city = """### 智慧城市与交通 (Smart City & Transportation)

| 编号 | 行业 | 案例名称 | 文件 | 状态 |
|------|------|----------|------|------|
| 11.3.1 | 智慧城市 | 交通流量分析 | traffic-flow-analysis.md | **深度完成** |
| 11.6.1 | 自动驾驶 | 传感器融合 | sensor-fusion.md | **深度完成** |
| 11.21.1 | 房地产 | 智慧楼宇 | smart-building.md | **深度完成** |"""
content = content.replace(old_city, new_city)

# 9. Update statistics
old_stats = """- **总计**: 40个行业案例 (新增9个深度案例)
- **覆盖行业**: 20+个垂直领域
- **平均每个案例**: 约60行详细内容"""
new_stats = """- **总计**: 40个行业案例 (新增20个深度案例)
- **覆盖行业**: 20+个垂直领域
- **平均每个案例**: 约800+行详细内容"""
content = content.replace(old_stats, new_stats)

# 10. Add new entries in the 新增深度案例 section
old_additions = """| 11.5.1 | 社交媒体 | 内容推荐深度案例 | 11.5.1-content-recommendation.md | 1,194 | 深度完成 |

> **说明**: 带 `.2` 后缀的编号为深度案例研究，相比基础案例(`.1`)包含更详细的技术架构、实现细节和量化指标。"""
new_additions = """| 11.5.1 | 社交媒体 | 内容推荐深度案例 | 11.5.1-content-recommendation.md | 1,194 | 深度完成 |
| 11.37.1 | 银行 | 实时支付清算深度案例 | 11.37.1-realtime-payment.md | 1,450 | 深度完成 |
| 11.14.1 | 制造 | 预测性维护深度案例 | 11.14.1-predictive-maintenance.md | 1,480 | 深度完成 |
| 11.20.1 | 传媒 | 直播实时互动深度案例 | 11.20.1-livestreaming.md | 1,420 | 深度完成 |
| 11.17.1 | 零售 | 实时动态定价深度案例 | 11.17.1-realtime-pricing.md | 1,460 | 深度完成 |
| 11.18.1 | 保险 | 实时理赔处理深度案例 | 11.18.1-claims-processing.md | 1,470 | 深度完成 |
| 11.22.1 | 教育 | 在线学习分析深度案例 | 11.22.1-online-learning.md | 1,430 | 深度完成 |
| 11.21.1 | 房地产 | 智慧楼宇深度案例 | 11.21.1-smart-building.md | 1,510 | 深度完成 |
| 11.9.1 | 电信 | 网络流量分析深度案例 | 11.9.1-network-traffic.md | 1,490 | 深度完成 |
| 11.8.1 | 石化 | 管道泄漏检测深度案例 | 11.8.1-pipeline-leak.md | 1,500 | 深度完成 |
| 11.6.1 | 自动驾驶 | 传感器融合深度案例 | 11.6.1-sensor-fusion.md | 1,530 | 深度完成 |
| 11.7.1 | 航空航天 | 飞行数据监控深度案例 | 11.7.1-flight-data.md | 1,540 | 深度完成 |

> **说明**: 带 `.2` 后缀的编号为深度案例研究，相比基础案例(`.1`)包含更详细的技术架构、实现细节和量化指标。本次A组冲刺将11个 `.1` 框架级占位符扩展为深度案例。"""
content = content.replace(old_additions, new_additions)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Index updated successfully.")
