# 学术前沿论文数据集

> 本目录包含 VLDB/SIGMOD/OSDI/SOSP/CIDR 2024-2025 流处理相关论文的元数据

## 文件结构

```
papers/
├── README.md                          # 本文件
├── academic-papers-2024-2025.json     # 核心论文元数据 (58篇)
└── frontier-summary.md                # 前沿方向摘要
```

## 统计数据

| 类别 | 数量 |
|------|------|
| 论文总数 | 58 篇 |
| 会议论文 | 48 篇 |
| 期刊论文 | 5 篇 |
| Workshop | 7 篇 |

## 主题分布

- **事务流处理 (TSP)**: 12 篇
- **流推理 (Stream Reasoning)**: 11 篇
- **AI/ML for Streaming**: 16 篇
- **学习型优化器**: 6 篇
- **硬件加速**: 10 篇
- **边缘流处理**: 3 篇

## 会议覆盖

- VLDB 2024/2025: 18 篇
- SIGMOD 2024/2025: 15 篇
- OSDI 2024/2025: 16 篇
- SOSP 2024/2025: 4 篇
- CIDR 2025: 3 篇
- 其他: 2 篇

## 使用方式

### 加载数据

```python
import json

with open('academic-papers-2024-2025.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

papers = data['papers']
print(f"Total papers: {len(papers)}")
```

### 筛选论文

```python
# 按主题筛选
stream_reasoning = [p for p in papers if 'Stream Reasoning' in p['topics']]

# 按会议筛选
vldb_papers = [p for p in papers if 'VLDB' in p['conference']]

# 按关联度筛选
high_relevance = [p for p in papers if p['relevance'].count('⭐') >= 4]
```

## 核心论文推荐

### 必读论文 (五星关联度)

1. **A Survey on Transactional Stream Processing** (VLDBJ 2024)
   - 事务流处理最全面的综述

2. **Styx: Transactional Stateful Functions** (SIGMOD 2025)
   - 最新的 SFaaS 范式

3. **Grounding Stream Reasoning Research** (TGDK 2024)
   - 流推理领域奠基性综述

4. **Stream Types** (PLDI 2024)
   - 流处理的类型理论基础

5. **Learned Cost Models for Query Optimization** (VLDB 2025)
   - 学习型优化器前沿

## 数据字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 论文唯一标识 |
| title | string | 论文标题 |
| authors | array | 作者列表 |
| conference | string | 发表会议/期刊 |
| year | string | 发表年份 |
| type | string | 论文类型 (Research/Survey/Workshop) |
| topics | array | 研究主题标签 |
| abstract | string | 论文摘要 |
| relevance | string | 与项目关联度 (⭐-⭐⭐⭐⭐⭐) |
| project_gap | string | 与项目的具体差距分析 |

## 更新记录

- 2026-04-12: v1.0 初始版本，收录 58 篇论文
