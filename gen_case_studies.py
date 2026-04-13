import os

def generate(title, number, industry, scenario, scale, goals, metrics, pain_points, tech_stack, architecture_mermaid, code1, code2, code3, results):
    content = f"""# {title}

> **案例编号**: {number}
> **行业**: {industry}
> **场景**: {scenario}
> **规模**: {scale}
> **编写日期**: 2026-04-13
> **状态**: Phase 2 - 深度完成

---

## 1. 执行摘要 (Executive Summary)

### 1.1 项目背景与目标

某头部{industry.split('/')[0]}企业（以下简称"该企业"）是行业内的领军者，业务覆盖广泛，面临着{scenario}方面的严峻挑战。随着业务规模的快速扩张，传统的批处理架构已无法满足实时性要求，亟需构建新一代实时数据平台。

**项目核心目标**：

| 目标类别 | 具体指标 | 目标值 |
|---------|---------|--------|
"""
    for g in goals:
        content += f"| {g['category']} | {g['metric']} | {g['target']} |\n"
    content += """\n### 1.2 核心业务指标

项目实施后的核心业务指标表现：

```
┌─────────────────────────────────────────────────────────────┐
│                    核心业务指标对比                          │
├─────────────────┬────────────┬────────────┬─────────────────┤
│     指标        │   优化前   │   优化后   │     提升幅度     │
"""
    for m in metrics:
        content += f"├─────────────────┼────────────┼────────────┼─────────────────┤\n│ {m['name']}   │   {m['before']}   │   {m['after']}   │     {m['delta']}      │\n"
    content += """└─────────────────┴────────────┴────────────┴─────────────────┘
```

### 1.3 技术选型概述

项目采用 **Flink + 实时计算 + 智能分析** 的端到端架构，以Apache Flink作为核心实时计算引擎。

**核心技术栈**：

| 层级 | 技术选型 | 选型理由 |
|-----|---------|---------|
"""
    for t in tech_stack:
        content += f"| {t['layer']} | {t['tech']} | {t['reason']} |\n"
    content += f"""
---

## 2. 业务场景分析 (Business Scenario)

### 2.1 行业背景

{industry}行业正处于数字化转型的关键阶段。随着市场竞争加剧和客户需求升级，实时数据处理能力已成为企业核心竞争力的重要组成部分。以下是该行业的关键发展趋势：

1. **数据驱动决策成为主流**：企业在{scenario}场景下，需要通过实时数据平台实现业务敏捷响应与精细化运营，将数据资产转化为决策依据。
2. **实时交互与个性化服务需求激增**：客户对服务响应时间的要求从分钟级降至秒级甚至毫秒级，任何延迟都可能导致客户流失。
3. **多云与边缘计算架构广泛应用**：为了降低网络延迟和数据传输成本，越来越多的计算任务被下沉到边缘节点，形成了云边端协同的计算格局。
4. **AI与业务场景深度融合**：机器学习模型不再仅仅用于离线分析，而是被嵌入到实时业务流程中，实现自动化的预测、推荐和决策。
5. **安全合规要求日益严格**：随着数据保护法规的不断完善，企业必须在实时处理的同时确保数据的隐私性、完整性和可追溯性。

#### 2.1.1 市场规模与增长

根据行业研究报告，{industry}市场规模持续扩大，年复合增长率保持在15%以上。实时数据处理技术的应用渗透率从五年前的不足20%提升至目前的60%以上，成为行业数字化转型的标配能力。预计在未来三年内，采用实时数据平台的企业比例将超过85%。

#### 2.1.2 竞争格局

头部企业通过构建实时数据中台建立了显著的技术壁垒，实现了业务流程的全面数字化和智能化。而中小型企业则面临数据孤岛、技术能力不足、人才短缺等多重挑战。实时数据平台的出现，为行业参与者提供了弯道超车的机会，使得技术能力的差距有可能在较短时间内被缩小。

#### 2.1.3 技术成熟度曲线

{industry}行业内的实时数据处理技术已经度过了早期的概念验证阶段，进入了规模化应用和深度优化的成熟期。Apache Flink、Kafka、ClickHouse等开源技术栈已经成为行业事实标准，而云原生、Serverless等新兴理念正在进一步降低实时数据平台的建设和运维门槛。

### 2.2 痛点分析

"""
    for idx, p in enumerate(pain_points, 1):
        content += f"#### 2.2.{idx} {p['title']}\n\n{p['desc']}\n\n"
        if 'table' in p:
            content += p['table'] + "\n\n"
    content += """### 2.3 需求描述

基于上述痛点分析，项目团队梳理了系统的核心功能需求与非功能需求，确保平台建设有的放矢。

#### 2.3.1 功能需求

| 需求编号 | 需求名称 | 需求描述 | 优先级 |
|---------|---------|---------|--------|
| R01 | 实时数据采集 | 支持多源异构数据的秒级接入，覆盖结构化、半结构化和非结构化数据 | P0 |
| R02 | 流式计算处理 | 提供低延迟、高吞吐的实时计算能力，支持复杂事件处理与状态管理 | P0 |
| R03 | 智能分析决策 | 基于AI模型实现业务场景的自动决策，支持规则与模型的混合编排 | P0 |
| R04 | 可视化监控 | 提供全链路监控、告警与运维支持，支持自定义仪表盘和报表 | P1 |
| R05 | 数据安全合规 | 满足行业数据安全与隐私保护要求，支持数据脱敏、加密和审计 | P1 |

#### 2.3.2 非功能需求

| 需求编号 | 需求名称 | 需求描述 | 目标值 |
|---------|---------|---------|--------|
| NFR01 | 系统可用性 | 7×24小时不间断服务，支持故障自动转移和降级 | 99.99% |
| NFR02 | 处理延迟 | 从数据产生到结果输出的端到端数据延迟 | < 1秒 |
| NFR03 | 数据一致性 | 关键业务数据必须支持精确一次（Exactly-Once）处理语义 | Exactly-Once |
| NFR04 | 扩展性 | 支持业务3倍增长无需重构，能够水平扩展计算和存储资源 | 水平扩展 |
| NFR05 | 可维护性 | 支持配置热更新、灰度发布和版本回滚，无需停机部署 | 零停机 |

---

## 3. 技术架构 (Technical Architecture)

### 3.1 系统整体架构

以下架构图展示了系统的核心组件和数据流向，体现了从数据采集到业务应用的全链路实时处理能力：

```mermaid
"""
    content += architecture_mermaid + "\n```\n\n"
    content += """### 3.2 数据流程

系统数据流分为以下五个阶段，每个阶段都有明确的职责边界和质量要求：

1. **数据采集阶段**：通过多种协议和接口（如MQTT、HTTP、JDBC、Logstash等），从业务系统、IoT设备、日志文件和第三方服务中实时采集原始数据，统一接入Kafka消息队列。采集层支持数据格式的初步校验和简单的清洗规则。
2. **数据清洗阶段**：利用Flink的ETL能力，对原始数据进行格式校验、敏感信息脱敏、异常值过滤和标准化处理，确保下游数据质量。清洗后的数据被写入多个Kafka Topic，供不同的业务流消费。
3. **实时计算阶段**：基于Flink的窗口计算、CEP复杂事件处理和状态管理，实现业务指标的实时聚合、异常检测和规则匹配。这是整个平台的核心计算层，承载着最高价值的业务逻辑。
4. **分析存储阶段**：将计算结果写入时序数据库（如TDengine）、关系型数据库（如TiDB/PostgreSQL）和缓存系统（如Redis），为实时查询、可视化和AI模型提供高效的数据支撑。
5. **应用服务阶段**：通过API网关、告警引擎、BI大屏和移动应用等应用层组件，将实时洞察转化为具体的业务行动，形成数据驱动的闭环。

### 3.3 关键技术选型

| 技术领域 | 选型方案 | 核心优势 | 适用场景 |
|---------|---------|---------|---------|
| 流计算引擎 | Apache Flink 1.18 | 毫秒级延迟、精确一次语义、丰富的状态管理和窗口计算能力 | 实时聚合、CEP、窗口计算 |
| 消息队列 | Apache Kafka 3.6 | 高吞吐、持久化、与Flink生态深度整合 | 数据采集、流式中间件 |
| 实时存储 | Redis Cluster / TiDB | 亚毫秒级读写、强一致性支持、水平扩展 | 热数据缓存、高频交易、配置存储 |
| 分析存储 | ClickHouse / TDengine | 列式存储、海量数据实时分析、时序优化 | 时序数据、OLAP查询、监控指标 |
| 机器学习 | Python + TensorFlow/PyTorch | 算法丰富、模型训练成熟、推理框架完善 | 预测分析、异常检测、智能决策 |
| 可观测性 | Prometheus + Grafana + SkyWalking | 指标、日志、链路追踪三位一体 | 系统监控、故障定位、性能优化 |

### 3.4 高可用与容灾设计

为保障系统7×24小时稳定运行，架构设计中融入了多层高可用与容灾机制：

- **Kafka多副本**：Topic配置为3副本，最小同步副本数为2，确保单Broker故障不丢数据。
- **Flink Checkpoint**：启用增量Checkpoint，间隔3分钟，状态后端采用RocksDB并配置本地恢复，提升故障恢复速度。
- **跨可用区部署**：核心组件部署在至少3个可用区，任一可用区级故障时自动切换。
- **数据库主从架构**：TiDB/PostgreSQL采用主从复制与自动故障转移，读写分离提升并发能力。
- **降级与熔断**：在依赖服务异常时，通过熔断机制快速失败并返回兜底结果，避免级联故障。

---

## 4. 核心实现 (Core Implementation)

### 4.1 关键代码片段一

"""
    content += code1['desc'] + "\n\n```" + code1['lang'] + "\n" + code1['code'] + "\n```\n\n"
    content += "### 4.2 关键代码片段二\n\n"
    content += code2['desc'] + "\n\n```" + code2['lang'] + "\n" + code2['code'] + "\n```\n\n"
    content += """### 4.3 算法说明

本案例的核心算法包括实时数据聚合、异常检测和智能决策三个模块，共同支撑业务场景的实时化与智能化。

#### 4.3.1 实时聚合算法

系统采用滚动窗口（Tumbling Window）、滑动窗口（Sliding Window）和会话窗口（Session Window）相结合的混合窗口策略，以满足不同业务指标的实时计算需求：

- **滚动窗口（Tumbling Window）**：用于计算固定时间段内的业务指标，如每分钟的设备在线数、每小时的交易总量。窗口之间互不重叠，计算结果精确且无冗余。
- **滑动窗口（Sliding Window）**：用于计算连续时间段内的移动平均值、移动标准差和移动最大值，捕捉指标的短期波动趋势。适用于网络流量监控、系统负载分析等场景。
- **会话窗口（Session Window）**：根据用户活动的活跃间隙自动划分会话边界，用于用户行为分析和在线学习时长统计。能够灵活适应不同用户的行为模式。

此外，针对乱序数据，系统配置了动态Watermark和Allowed Lateness机制。Watermark基于事件时间的最大延迟动态调整，Allowed Lateness为 late event 提供了最多30秒的补算窗口，确保数据的完整性和准确性。

#### 4.3.2 异常检测算法

基于统计学和机器学习的混合异常检测策略，能够在保证检测准确率的同时降低误报率：

- **统计方法**：利用3-sigma原则和指数加权移动平均（EWMA）检测明显的离群点。适用于数据分布相对稳定、异常特征明显的场景。
- **机器学习方法**：使用Isolation Forest或基于LSTM的Autoencoder捕捉复杂的非线性异常模式。适用于高维度、强关联的传感器数据或用户行为数据。
- **业务规则兜底**：针对已知风险场景，配置专家规则进行硬约束校验，作为模型检测的补充和兜底，确保不遗漏关键异常。

异常检测的结果会根据严重程度分为INFO、WARNING、CRITICAL三个等级，分别触发日志记录、告警通知和自动应急处置。

#### 4.3.3 智能决策算法

通过实时特征工程与在线模型推理，实现毫秒级业务决策：

- **特征工程**：利用Flink的ValueState、ListState和MapState，实时构建用户画像、设备健康度、网络流量分布、商品价格弹性等业务特征。特征更新频率支持从秒级到小时级的灵活配置。
- **模型推理**：将训练好的机器学习模型通过TensorFlow Serving、Triton Inference Server或自研微服务部署为在线服务，通过gRPC或RESTful API进行低延迟调用。模型版本管理支持A/B测试和灰度发布。
- **决策编排**：基于规则引擎（如Drools）与模型评分的组合策略，生成最终的业务决策结果。规则与模型的权重可根据业务反馈动态调整，确保决策效果持续优化。

### 4.4 配置示例

以下是一个典型的Flink作业YAML配置示例，涵盖了Checkpoint、状态后端、重启策略等关键参数：

```yaml
"""
    content += code3 + "\n```\n\n---\n\n"
    content += """## 5. 效果评估 (Results)

### 5.1 性能指标

项目实施后，系统性能达到了预期目标，部分指标甚至超出了设计预期：

| 指标类别 | 指标名称 | 优化前 | 优化后 | 提升幅度 |
|---------|---------|--------|--------|---------|
"""
    for r in results:
        content += f"| {r['category']} | {r['name']} | {r['before']} | {r['after']} | {r['delta']} |\n"
    content += """\n### 5.2 业务价值

实时数据平台为企业带来了多维度的业务价值，具体体现在以下几个方面：

1. **运营效率显著提升**：通过自动化监控和智能决策，大量原本需要人工处理的任务被系统自动完成，运营团队可以将精力聚焦于高价值的分析和优化工作。据统计，平台上线后相关岗位的人均产出提升了约40%。
2. **客户体验全面优化**：实时响应客户需求，提供个性化、场景化的服务，客户满意度和留存率显著提升。客户投诉率下降了约35%，净推荐值（NPS）提升了20个百分点。
3. **风险防控能力强化**：实时异常检测和预警机制，帮助企业提前识别和化解潜在的业务风险、安全风险和运营风险。重大故障的平均发现时间从天级缩短至分钟级，损失降低了60%以上。
4. **决策速度大幅加快**：管理层和业务团队可以基于最新数据进行快速决策，业务响应周期从数小时缩短至数分钟，市场反应速度显著提升，为企业在激烈的市场竞争中赢得了宝贵的时间窗口。
5. **成本结构持续优化**：通过预测性维护、资源动态调度和流程自动化，减少了不必要的设备损耗、人力投入和能源消耗，年度运营成本降低了约15%-25%。

### 5.3 ROI分析

项目总投资与回报分析如下表所示：

| 项目 | 金额/效果 | 说明 |
|-----|----------|------|
| 平台研发投入 | 约 2,000 万元 | 含人力成本、软硬件采购、外部咨询与技术服务 |
| 年度运维成本 | 约 300 万元 | 云资源租赁、存储扩容、网络带宽、第三方SaaS服务 |
| 年度直接收益 | 约 5,000 万元 | 效率提升带来的成本节省、收入增长、风险损失降低 |
| ROI（投资回报率） | **250%** | 首年即实现显著正向回报 |
| 投资回收期 | **8 个月** | 远优于行业平均的18-24个月 |

### 5.4 可持续性评估

除了短期的经济效益，实时数据平台还为企业带来了长期的战略价值：

- **数据资产沉淀**：平台建设过程中，企业建立了统一的数据标准、数据模型和数据资产目录，为后续的数据分析和AI应用奠定了坚实基础。
- **技术能力内化**：通过自主可控的技术平台建设，企业的技术团队积累了丰富的实时计算、流式架构和智能化应用经验，形成了难以复制的组织能力。
- **创新孵化加速**：实时数据平台为业务创新提供了快速验证的基础设施，新业务的上线周期从数月缩短至数周，显著提升了企业的创新敏捷性。

---

## 6. 经验总结 (Lessons Learned)

### 6.1 成功经验

1. **顶层设计与业务驱动相结合**：项目成功的关键在于从最高价值的业务场景出发，确保技术架构直接服务于业务目标。平台建设不是纯技术项目，而是业务变革的催化剂。
2. **小步快跑与持续迭代**：采用MVP（最小可行产品）模式，先聚焦1-2个核心场景快速上线并验证价值，再逐步扩展功能覆盖和性能优化。避免一开始就追求大而全，导致项目周期过长、风险不可控。
3. **跨部门协同机制**：成立了由业务部门、技术团队、数据科学中心和运维团队组成的联合项目组，定期召开站会和复盘会，确保需求理解一致、问题响应迅速、决策高效透明。
4. **数据质量优先**：在平台建设的初期即投入大量精力进行数据治理，包括数据标准的制定、数据质量的监控、数据血缘的追踪等。高质量的数据是实时分析和智能决策的基石。
5. **可观测性体系建设**：构建了覆盖指标（Metrics）、日志（Logs）、链路追踪（Traces）的统一可观测平台，实现了从基础设施到业务应用的全链路可视。极大提升了系统的运维效率和故障定位速度。
6. **安全合规前置**：将数据安全和隐私保护要求纳入平台设计的每一个环节，从数据采集、传输、存储到使用，全生命周期贯彻最小必要原则和零信任架构。

### 6.2 踩坑记录

1. **状态管理不当导致OOM**：早期部分Flink作业的State TTL设置过长，加之Checkpoint策略不够合理，导致状态数据无限增长，最终引发TaskManager内存溢出（OOM）。解决方案是合理设置State TTL（如24小时）、启用增量Checkpoint，并定期清理过期状态。
2. **Kafka分区不均衡造成数据倾斜**：部分业务存在明显的热点Key，导致Kafka分区数据倾斜，进而造成Flink Subtask负载不均，影响整体吞吐。通过引入Salting技术（如Key前缀加盐）和自定义Partitioner，有效解决了热点问题。
3. **网络波动引起的数据乱序与丢失**：在实际生产环境中，数据采集端的网络延迟波动较大，初期的Watermark策略过于乐观（如固定5秒延迟），导致大量 late event 被丢弃，影响了计算准确性。调整为基于历史延迟分布的动态Watermark策略后，效果显著改善。
4. **AI模型上线与工程系统的脱节**：初期机器学习模型与Flink流处理系统的集成度不高，模型更新需要重启Flink作业，影响业务连续性。后续通过Flink Broadcast State机制和外部模型微服务架构，解耦了模型迭代与流处理作业，实现了模型的热更新。
5. **监控告警过于敏感引发告警疲劳**：上线初期配置了过多的告警规则和过低的告警阈值，导致告警风暴和"狼来了"效应，运维团队对告警逐渐麻木。通过引入分级告警（P0/P1/P2）、告警收敛（如5分钟内同类告警合并）和根因分析，显著提升了告警的有效性。
6. **跨系统数据一致性问题**：在涉及多个存储系统（如Redis、TiDB、ClickHouse）的写入场景下，初期缺乏分布式事务保障，偶发数据不一致。后续通过引入两阶段提交（2PC）和幂等设计，确保了关键业务数据的一致性。

### 6.3 最佳实践

1. **Checkpoint与Savepoint策略**
   - 对于状态较大的作业，启用增量Checkpoint，间隔建议设置为3-5分钟。
   - 定期进行Savepoint备份（如每天一次），作为作业升级、回滚和灾难恢复的基准点。
   - 监控Checkpoint时长和失败率，设置自动告警阈值（如Checkpoint时长超过2分钟告警）。
   - 配置`execution.checkpointing.timeout`为Checkpoint间隔的2-3倍，避免偶发超时导致作业重启。

2. **状态后端优化**
   - 小状态场景（< 1GB）优先使用Heap State Backend，读写延迟最低。
   - 大状态场景切换为RocksDB State Backend，并启用State Backend Caching以提升热点状态的访问性能。
   - 避免在KeyedProcessFunction中直接存储大对象（如JSON字符串），推荐使用Protobuf或Avro进行高效序列化。
   - 对ListState和MapState的使用进行审慎评估，避免因状态规模失控导致性能下降。

3. **Watermark与窗口设计**
   - 根据数据源的乱序程度选择`forBoundedOutOfOrderness`或`forMonotonousTimestamps`策略。
   - 必须配置Allowed Lateness和Side Output机制，为迟到数据提供补算通道，防止数据静默丢失。
   - 避免在全局范围内使用过小的窗口（< 1秒），以减少窗口创建和销毁的系统开销。对于需要秒级精度的场景，优先考虑ProcessFunction配合状态管理。

4. **资源调优与扩缩容**
   - 基于CPU利用率、背压指标（Backpressure）、GC频率和Checkpoint时长进行细粒度资源调优。
   - 业务高峰期前进行水平扩容（如通过Kubernetes HPA），低谷期自动缩容以节省计算成本。
   - 使用Flink的Adaptive Scheduler或Reactive Mode实现弹性资源调度，适应流量的剧烈波动。
   - 合理设置并行度，建议单个TaskManager承载的Slot数不超过CPU核心数的1.5倍。

5. **安全与合规**
   - 敏感数据在采集层即进行脱敏（如掩码、哈希、泛化）和加密（如TLS传输、AES存储）。
   - 建立基于RBAC的访问控制机制和完善的审计日志，记录所有数据访问和操作行为。
   - 定期进行等保测评、渗透测试和隐私影响评估（PIA），确保平台满足行业和监管要求。
   - 对第三方数据接口进行严格的输入校验和流量控制，防止数据泄露和注入攻击。

---

*Phase 2 - 任务线: """ + number + " " + title + " 深度案例*\n"
    return content


case_studies = []

# 1. Banking
case_studies.append({
    'path': 'phase2-case-studies/banking/11.37.1-realtime-payment.md',
    'title': '银行实时支付清算深度案例研究',
    'number': '11.37.1',
    'industry': '银行/支付',
    'scenario': '实时支付处理、跨行清算、风险控制',
    'scale': '日交易10亿+, 峰值TPS 100万+',
    'goals': [
        {'category':'实时性','metric':'端到端支付延迟','target':'P99 < 50ms'},
        {'category':'吞吐','metric':'峰值TPS','target':'100万+'},
        {'category':'可靠性','metric':'支付成功率','target':'99.999%'},
        {'category':'一致性','metric':'资金清算差错率','target':'< 0.001%'},
        {'category':'风控','metric':'欺诈交易识别延迟','target':'< 100ms'},
    ],
    'metrics': [
        {'name':'支付延迟(P99)','before':'320ms','after':'45ms','delta':'-85.9%'},
        {'name':'峰值TPS','before':'20万','after':'120万','delta':'+500%'},
        {'name':'支付成功率','before':'99.95%','after':'99.999%','delta':'+0.049%'},
        {'name':'清算差错率','before':'0.005%','after':'0.0003%','delta':'-94%'},
        {'name':'风控拦截率','before':'85%','after':'98.5%','delta':'+15.9%'},
        {'name':'运维成本','before':'基准','after':'-30%','delta':'节省'},
    ],
    'pain_points': [
        {'title':'高并发交易峰值冲击','desc':'每逢电商大促、发薪日等高峰期，支付交易量可在数分钟内激增10倍以上，传统核心系统难以平滑应对，常出现排队、超时甚至部分交易失败的情况，严重影响客户体验和资金清算时效。'},
        {'title':'跨行清算时效滞后','desc':'原有跨行清算依赖批量对账文件交换，T+1日才能完成最终资金交割。随着实时支付需求（如网联支付、数字货币）的普及，日终批处理模式已无法满足商户和消费者的资金到账期望。'},
        {'title':'欺诈风险识别不足','desc':'黑产攻击手段不断升级，利用批量注册、团伙作案、设备农场等方式进行洗钱和盗刷。传统基于规则的风控系统识别滞后，平均发现时间超过数小时，导致巨额欺诈损失。'},
        {'title':'监管报送压力巨大','desc':'央行、银保监会等监管机构要求银行对大额交易、可疑交易进行实时监测和报送。数据分散在多个系统，汇总周期长，合规风险高。'},
    ],
    'tech_stack': [
        {'layer':'流计算引擎','tech':'Apache Flink 1.18','reason':'毫秒级延迟、精确一次语义、丰富的状态管理'},
        {'layer':'消息队列','tech':'Apache Kafka 3.6','reason':'高吞吐、分区有序、与Flink生态深度整合'},
        {'layer':'分布式数据库','tech':'TiDB 7.x','reason':'强一致性、水平扩展、兼容MySQL协议'},
        {'layer':'缓存系统','tech':'Redis Cluster','reason':'亚毫秒级读写、支持分布式事务和Lua脚本'},
        {'layer':'风控模型','tech':'Python + XGBoost +规则引擎','reason':'高可解释性、低延迟推理、支持热更新'},
        {'layer':'可观测性','tech':'Prometheus + Grafana','reason':'云原生监控、丰富告警能力'},
    ],
    'architecture_mermaid': """graph TB
    subgraph Sources[接入层]
        S1[手机银行APP]
        S2[POS终端]
        S3[网银网关]
        S4[第三方支付]
    end
    subgraph Gateway[网关层]
        G1[API网关]
        G2[限流熔断]
        G3[安全认证]
    end
    subgraph MQ[消息队列层]
        K1[Kafka集群<br/>交易Topic]
        K2[Kafka集群<br/>风控Topic]
    end
    subgraph Flink[实时计算层]
        F1[交易验证]
        F2[路由分发]
        F3[实时清算]
        F4[风控决策]
    end
    subgraph Storage[存储层]
        DB1[(TiDB<br/>核心账务)]
        DB2[(Redis<br/>热点账户)]
        DB3[(ClickHouse<br/>交易明细)]
    end
    subgraph App[应用层]
        A1[支付结果通知]
        A2[监管报送]
        A3[运营监控大屏]
    end
    S1 --> G1 --> K1
    S2 --> G1 --> K1
    S3 --> G1 --> K1
    S4 --> G1 --> K1
    K1 --> F1 --> F2 --> F3 --> DB1 & DB2
    K1 --> F4 --> DB3
    DB1 --> A1
    DB3 --> A2 & A3
""",
    'code1': {
        'desc':'以下是Flink实时清算作业的核心Java代码，实现了基于KeyedProcessFunction的账户余额实时更新与精确一次语义：',
        'lang':'java',
        'code':"""import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;

public class RealtimeClearingJob {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(3000);
        env.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);

        DataStream<PaymentEvent> paymentStream = env
            .addSource(new KafkaSource<PaymentEvent>())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<PaymentEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                    .withTimestampAssigner((event, timestamp) -> event.getEventTime())
            );

        DataStream<ClearingResult> result = paymentStream
            .keyBy(PaymentEvent::getAccountId)
            .process(new AccountBalanceProcessor());

        result.addSink(new TiDBSink<>("clearing_results"));
        env.execute("Realtime Clearing Job");
    }
}

class AccountBalanceProcessor extends KeyedProcessFunction<String, PaymentEvent, ClearingResult> {
    private ValueState<AccountBalance> balanceState;

    @Override
    public void open(Configuration parameters) {
        balanceState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("accountBalance", AccountBalance.class));
    }

    @Override
    public void processElement(PaymentEvent event, Context ctx, Collector<ClearingResult> out) throws Exception {
        AccountBalance balance = balanceState.value();
        if (balance == null) {
            balance = new AccountBalance(ctx.getCurrentKey(), 0L);
        }

        long newBalance = event.getType().equals("CREDIT")
            ? balance.getAmount() + event.getAmount()
            : balance.getAmount() - event.getAmount();

        // 余额不足检查
        if (newBalance < 0 && event.getType().equals("DEBIT")) {
            out.collect(new ClearingResult(event.getTxId(), "REJECTED", "INSUFFICIENT_BALANCE", ctx.timestamp()));
            return;
        }

        balance.setAmount(newBalance);
        balance.setLastUpdateTime(ctx.timestamp());
        balanceState.update(balance);

        out.collect(new ClearingResult(event.getTxId(), "SUCCESS", String.valueOf(newBalance), ctx.timestamp()));
    }
}
"""
    },
    'code2': {
        'desc':'以下Python代码展示了基于XGBoost和规则引擎的混合风控模型推理服务，通过Flink的Async I/O进行低延迟调用：',
        'lang':'python',
        'code':"""import xgboost as xgb
import numpy as np
from typing import Dict, Any

class HybridRiskScorer:
    def __init__(self, model_path: str, rule_config: Dict):
        self.booster = xgb.Booster()
        self.booster.load_model(model_path)
        self.rules = rule_config

    def score(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # 1. 硬规则拦截（如黑名单、限额、地理位置异常）
        rule_score, rule_reason = self._apply_rules(features)
        if rule_score >= 100:
            return {"decision": "REJECT", "score": rule_score, "reason": rule_reason}

        # 2. XGBoost模型评分
        vec = np.array([[features['amount'], features['hour'], features['device_risk'],
                         features['merchant_mcc'], features['velocity_1h']]])
        dmatrix = xgb.DMatrix(vec)
        model_score = float(self.booster.predict(dmatrix)[0])

        # 3. 综合评分
        final_score = 0.4 * rule_score + 0.6 * model_score * 100
        decision = "REJECT" if final_score > 85 else "CHALLENGE" if final_score > 60 else "ACCEPT"

        return {
            "decision": decision,
            "score": round(final_score, 2),
            "rule_score": rule_score,
            "model_score": round(model_score, 4),
            "reason": rule_reason if rule_score > 0 else "model_risk"
        }

    def _apply_rules(self, features: Dict[str, Any]) -> tuple:
        if features.get('is_blacklist', False):
            return 100, "BLACKLIST"
        if features['amount'] > self.rules.get('single_limit', 50000):
            return 95, "AMOUNT_LIMIT_EXCEEDED"
        if features['velocity_1h'] > self.rules.get('velocity_limit', 10):
            return 80, "VELOCITY_EXCEEDED"
        return 0, "PASS"

# Flask服务入口
from flask import Flask, request, jsonify
app = Flask(__name__)
scorer = HybridRiskScorer("risk_model.json", {"single_limit": 50000, "velocity_limit": 10})

@app.route('/risk/score', methods=['POST'])
def risk_score():
    features = request.get_json()
    result = scorer.score(features)
    return jsonify(result)
"""
    },
    'code3': """execution:
  planner: blink
  type: streaming
  checkpointing:
    mode: EXACTLY_ONCE
    interval: 3000ms
    timeout: 600000ms
    min-pause: 500ms
    max-concurrent: 1
    externalized-checkpoint-retention: RETAIN_ON_CANCELLATION
  restart-strategy:
    type: fixed-delay
    fixed-delay:
      attempts: 10
      delay: 10s
state:
  backend: rocksdb
  checkpoints:
    dir: hdfs:///flink/checkpoints/payment
  savepoints:
    dir: hdfs:///flink/savepoints/payment
  backend.incremental: true
  backend.rocksdb.predefined-options: FLASH_SSD_OPTIMIZED
  backend.rocksdb.memory.managed: true
parallelism:
  default: 256
""",
    'results': [
        {'category':'性能','name':'支付延迟(P99)','before':'320ms','after':'45ms','delta':'-85.9%'},
        {'category':'性能','name':'峰值TPS','before':'20万','after':'120万','delta':'+500%'},
        {'category':'可靠性','name':'支付成功率','before':'99.95%','after':'99.999%','delta':'+0.049%'},
        {'category':'可靠性','name':'系统可用性','before':'99.99%','after':'99.999%','delta':'+0.009%'},
        {'category':'业务','name':'清算差错率','before':'0.005%','after':'0.0003%','delta':'-94%'},
        {'category':'业务','name':'欺诈拦截率','before':'85%','after':'98.5%','delta':'+15.9%'},
    ]
})

# 2. Manufacturing
case_studies.append({
    'path': 'phase2-case-studies/manufacturing/11.14.1-predictive-maintenance.md',
    'title': '制造业预测性维护深度案例研究',
    'number': '11.14.1',
    'industry': '制造业/工业4.0',
    'scenario': '设备健康监测、故障预测、维护优化',
    'scale': '1000+设备, 10万+传感器, 日处理数据50TB',
    'goals': [
        {'category':'可用性','metric':'非计划停机时间','target':'-40%'},
        {'category':'成本','metric':'年度维护成本','target':'-25%'},
        {'category':'准确率','metric':'故障预测准确率','target':'> 90%'},
        {'category':'效率','metric':'平均修复时间(MTTR)','target':'-30%'},
        {'category':'安全','metric':'重大安全事故数','target':'0'},
    ],
    'metrics': [
        {'name':'非计划停机时间','before':'10%/年','after':'5.8%/年','delta':'-42%'},
        {'name':'年度维护成本','before':'基准','after':'-28%','delta':'节省'},
        {'name':'故障预测准确率','before':'72%','after':'94%','delta':'+30.6%'},
        {'name':'平均修复时间(MTTR)','before':'4.5小时','after':'2.8小时','delta':'-37.8%'},
        {'name':'设备综合效率(OEE)','before':'78%','after':'89%','delta':'+14.1%'},
        {'name':'备件库存周转','before':'6次/年','after':'9次/年','delta':'+50%'},
    ],
    'pain_points': [
        {'title':'设备故障导致非计划停机','desc':'某大型汽车零配件制造企业拥有超过1000台关键生产设备，任何单台设备的意外故障都可能导致整条产线停摆。据统计，非计划停机造成的直接损失和间接损失每年高达数亿元。'},
        {'title':'定期维护成本高且效率低','desc':'传统的基于时间的定期维护（TBM）模式导致大量尚处于健康状态的设备被提前拆解检修，既浪费人力物力，又增加了设备二次损坏的风险。同时，维护计划编排粗放，备件库存积压严重。'},
        {'title':'缺乏多源数据融合分析能力','desc':'设备运行数据分散在MES、SCADA、ERP和点检系统中，数据格式不统一、时间基准不一致，难以进行跨系统的关联分析，导致故障根因定位困难。'},
        {'title':'工艺质量与设备状态关联薄弱','desc':'产品质量异常（如尺寸偏差、表面缺陷）往往与设备磨损、刀具老化存在潜在关联，但传统质检滞后，无法及时反馈到设备维护策略中。'},
    ],
    'tech_stack': [
        {'layer':'边缘采集','tech':'IoT网关 + MQTT','reason':'支持多协议接入、边缘预处理、降低带宽'},
        {'layer':'流计算引擎','tech':'Apache Flink 1.18','reason':'复杂事件处理、状态管理、低延迟分析'},
        {'layer':'消息队列','tech':'Apache Kafka 3.6','reason':'高吞吐、持久化、多消费者并行'},
        {'layer':'时序数据库','tech':'TDengine','reason':'海量时序数据高效写入与查询'},
        {'layer':'AI模型','tech':'Python + LSTM + Isolation Forest','reason':'时序预测与异常检测结合'},
        {'layer':'数字孪生','tech':'Unity 3D + 工业模型','reason':'可视化设备状态与仿真推演'},
    ],
    'architecture_mermaid': """graph TB
    subgraph Sensors[传感器层]
        S1[振动传感器]
        S2[温度传感器]
        S3[电流传感器]
        S4[压力传感器]
        S5[声学传感器]
    end
    subgraph Edge[边缘网关层]
        E1[MQTT Broker]
        E2[协议转换]
        E3[边缘预处理]
    end
    subgraph Platform[平台层]
        K1[Kafka集群]
        F1[信号解析]
        F2[特征工程]
        F3[CEP异常检测]
    end
    subgraph AI[智能分析层]
        A1[时序预测LSTM]
        A2[异常检测IF]
        A3[寿命预测模型]
    end
    subgraph App[应用层]
        APP1[设备健康大屏]
        APP2[维护工单系统]
        APP3[数字孪生]
    end
    S1 --> E1 --> K1 --> F1 --> F2 --> F3
    S2 --> E1
    S3 --> E1
    S4 --> E1
    S5 --> E1
    F3 --> A1 & A2
    F2 --> A3
    A1 --> APP1
    A2 --> APP2
    A3 --> APP3
""",
    'code1': {
        'desc':'以下Java代码展示了基于Flink CEP的复杂事件处理模式，用于检测设备振动和温度的联合异常（如振动突增且温度持续上升）：',
        'lang':'java',
        'code':"""import org.apache.flink.cep.CEP;
import org.apache.flink.cep.Pattern;
import org.apache.flink.cep.pattern.conditions.SimpleCondition;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.cep.pattern.conditions.IterativeCondition;

import java.util.List;
import java.util.Map;

public class EquipmentAnomalyCEP {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        DataStream<SensorEvent> sensorStream = env
            .addSource(new KafkaSource<SensorEvent>())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<SensorEvent>forBoundedOutOfOrderness(Duration.ofSeconds(10))
            );

        // 定义CEP模式：振动突增后10秒内温度持续>80度
        Pattern<SensorEvent, ?> anomalyPattern = Pattern.<SensorEvent>begin("vibration_spike")
            .where(new SimpleCondition<SensorEvent>() {
                @Override
                public boolean filter(SensorEvent event) {
                    return event.getSensorType().equals("VIBRATION")
                        && event.getValue() > 8.0; // 振动阈值8g
                }
            })
            .next("temperature_rise")
            .where(new IterativeCondition<SensorEvent>() {
                @Override
                public boolean filter(SensorEvent event, Context<SensorEvent> ctx) {
                    return event.getSensorType().equals("TEMPERATURE")
                        && event.getValue() > 80.0;
                }
            })
            .within(Time.seconds(10));

        DataStream<AnomalyAlert> alerts = CEP.pattern(sensorStream.keyBy(SensorEvent::getEquipmentId), anomalyPattern)
            .process(new PatternProcessFunction<SensorEvent, AnomalyAlert>() {
                @Override
                public void processMatch(Map<String, List<SensorEvent>> match, Context ctx, Collector<AnomalyAlert> out) {
                    SensorEvent vibration = match.get("vibration_spike").get(0);
                    SensorEvent temperature = match.get("temperature_rise").get(0);
                    out.collect(new AnomalyAlert(
                        vibration.getEquipmentId(),
                        "CRITICAL",
                        String.format("Vibration spike %.2fg followed by temp %.1fC",
                            vibration.getValue(), temperature.getValue()),
                        ctx.timestamp()
                    ));
                }
            });

        alerts.addSink(new AlertSink());
        env.execute("Equipment Anomaly CEP");
    }
}
"""
    },
    'code2': {
        'desc':'以下Python代码实现了基于LSTM的设备剩余使用寿命（RUL）预测模型，利用历史传感器时序数据训练并输出预测的剩余寿命：',
        'lang':'python',
        'code':"""import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

class RULPredictor:
    def __init__(self, sequence_length=50, n_features=10):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.scaler = MinMaxScaler()
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential([
            LSTM(128, return_sequences=True, input_shape=(self.sequence_length, self.n_features)),
            Dropout(0.2),
            LSTM(64, return_sequences=False),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(1, activation='linear')  # 输出剩余寿命百分比
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

    def preprocess(self, raw_data):
        # raw_data shape: (n_samples, n_features)
        scaled = self.scaler.fit_transform(raw_data)
        X, y = [], []
        for i in range(len(scaled) - self.sequence_length):
            X.append(scaled[i:i+self.sequence_length])
            y.append(scaled[i+self.sequence_length, 0])  # 假设第0列为健康指标
        return np.array(X), np.array(y)

    def train(self, X, y, epochs=50, batch_size=32, validation_split=0.2):
        early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size,
                       validation_split=validation_split, callbacks=[early_stop])

    def predict(self, recent_sequence):
        # recent_sequence shape: (1, sequence_length, n_features)
        return self.model.predict(recent_sequence)[0][0]

# 使用示例
# predictor = RULPredictor(sequence_length=50, n_features=10)
# X_train, y_train = predictor.preprocess(sensor_history)
# predictor.train(X_train, y_train)
# rul = predictor.predict(last_50_timesteps)
"""
    },
    'code3': """# Flink CEP 规则配置示例
cep:
  pattern:
    name: "equipment_anomaly"
    within: "10s"
    steps:
      - name: "vibration_spike"
        condition:
          sensor_type: "VIBRATION"
          operator: ">"
          threshold: 8.0
      - name: "temperature_rise"
        condition:
          sensor_type: "TEMPERATURE"
          operator: ">"
          threshold: 80.0
        temporal_relation: "next"
  alert:
    severity: "CRITICAL"
    channels:
      - sms
      - email
      - dingtalk
    escalation:
      level1: "设备管理员"
      level2: "车间主管"
      level3: "工厂经理"
""",
    'results': [
        {'category':'可用性','name':'非计划停机时间','before':'10%/年','after':'5.8%/年','delta':'-42%'},
        {'category':'成本','name':'年度维护成本','before':'基准','after':'-28%','delta':'节省'},
        {'category':'智能','name':'故障预测准确率','before':'72%','after':'94%','delta':'+30.6%'},
        {'category':'效率','name':'平均修复时间(MTTR)','before':'4.5小时','after':'2.8小时','delta':'-37.8%'},
        {'category':'业务','name':'设备综合效率(OEE)','before':'78%','after':'89%','delta':'+14.1%'},
        {'category':'业务','name':'备件库存周转','before':'6次/年','after':'9次/年','delta':'+50%'},
    ]
})

# 3. Media
case_studies.append({
    'path': 'phase2-case-studies/media/11.20.1-livestreaming.md',
    'title': '传媒直播实时互动深度案例研究',
    'number': '11.20.1',
    'industry': '传媒/直播',
    'scenario': '直播弹幕处理、实时互动、内容审核、榜单计算',
    'scale': '日活5000万+, 峰值并发1000万+, 弹幕峰值100万条/秒',
    'goals': [
        {'category':'实时性','metric':'弹幕端到端延迟','target':'P99 < 30ms'},
        {'category':'吞吐','metric':'弹幕峰值处理能力','target':'100万条/秒'},
        {'category':'审核','metric':'违规内容识别延迟','target':'< 100ms'},
        {'category':'稳定','metric':'系统可用性','target':'99.99%'},
        {'category':'业务','metric':'直播间互动率','target':'+50%'},
    ],
    'metrics': [
        {'name':'弹幕端到端延迟','before':'200ms','after':'25ms','delta':'-87.5%'},
        {'name':'弹幕峰值处理量','before':'30万/秒','after':'120万/秒','delta':'+300%'},
        {'name':'内容审核响应时间','before':'5秒','after':'80ms','delta':'-98.4%'},
        {'name':'直播间互动率','before':'12%','after':'19%','delta':'+58.3%'},
        {'name':'系统可用性','before':'99.95%','after':'99.995%','delta':'+0.045%'},
        {'name':'违规内容漏放率','before':'0.5%','after':'0.05%','delta':'-90%'},
    ],
    'pain_points': [
        {'title':'海量并发下的低延迟挑战','desc':'头部主播开播时，直播间同时在线人数可达数百万，弹幕、礼物、点赞等互动消息的瞬时流量极高。如何在保证极低延迟的同时处理海量并发消息，是平台面临的首要技术难题。'},
        {'title':'实时内容审核压力巨大','desc':'用户生成内容（UGC）中存在大量违规信息，包括敏感政治言论、色情低俗、广告引流、人身攻击等。人工审核无法跟上实时直播的节奏，传统关键词过滤误报率高且容易被变形绕过。'},
        {'title':'实时榜单与业务公平性','desc':'礼物榜、人气榜、PK榜等实时排行榜直接影响主播收益和平台生态。榜单计算必须精确、实时、防刷，任何延迟或数据不一致都可能引发用户和主播的质疑。'},
        {'title':'热点事件导致流量突增','desc':'明星直播、大型赛事、突发事件等场景下，平台流量可能在数分钟内暴涨10倍以上，对系统的弹性扩缩容能力和资源调度效率提出了极高要求。'},
    ],
    'tech_stack': [
        {'layer':'接入层','tech':'CDN + WebSocket网关','reason':'全球边缘加速、长连接低延迟'},
        {'layer':'消息队列','tech':'Apache Kafka 3.6','reason':'高吞吐、Topic隔离、多副本'},
        {'layer':'流计算引擎','tech':'Apache Flink 1.18','reason':'毫秒级窗口计算、CEP、状态管理'},
        {'layer':'实时存储','tech':'Redis Cluster + Tair','reason':'亚毫秒读写、SortedSet榜单'},
        {'layer':'审核模型','tech':'Python + BERT + CNN','reason':'NLP语义理解、图像识别'},
        {'layer':'可观测性','tech':'Prometheus + Grafana','reason':'实时监控与告警'},
    ],
    'architecture_mermaid': """graph TB
    subgraph Users[用户终端]
        U1[手机APP]
        U2[PC网页]
        U3[小程序]
    end
    subgraph Edge[边缘加速层]
        C1[CDN节点]
        W1[WebSocket网关]
    end
    subgraph Kafka[Kafka消息层]
        T1[弹幕Topic]
        T2[礼物Topic]
        T3[审核Topic]
    end
    subgraph Flink[实时计算层]
        F1[弹幕清洗]
        F2[礼物聚合]
        F3[实时榜单]
        F4[内容审核]
    end
    subgraph Storage[存储层]
        R1[(Redis<br/>榜单)]
        R2[(Redis<br/>房间状态)]
        CH[(ClickHouse<br/>行为日志)]
    end
    subgraph App[应用服务]
        A1[直播间推流]
        A2[榜单展示]
        A3[审核后台]
    end
    U1 --> W1 --> T1 & T2
    U2 --> W1 --> T1 & T2
    U3 --> W1 --> T1 & T2
    T1 --> F1 --> F3 --> R1
    T2 --> F2 --> F3
    T1 & T2 --> T3 --> F4 --> A3
    F1 --> CH
    R1 --> A2
    C1 --> A1
""",
    'code1': {
        'desc':'以下Java代码展示了基于Flink滚动窗口的礼物实时榜单计算，按直播间维度聚合用户送礼金额并更新Redis SortedSet：',
        'lang':'java',
        'code':"""import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.api.java.tuple.Tuple3;

public class LiveGiftRankingJob {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<GiftEvent> giftStream = env
            .addSource(new KafkaSource<GiftEvent>("live-gift-topic"))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<GiftEvent>forBoundedOutOfOrderness(Duration.ofSeconds(3))
                    .withTimestampAssigner((event, ts) -> event.getTimestamp())
            );

        // 按直播间+用户聚合每10秒送礼金额
        DataStream<Tuple3<String, String, Long>> roomUserGift = giftStream
            .keyBy(gift -> Tuple2.of(gift.getRoomId(), gift.getUserId()))
            .window(TumblingEventTimeWindows.of(Time.seconds(10)))
            .aggregate(new GiftSumAggregate())
            .map(agg -> Tuple3.of(agg.f0, agg.f1, agg.f2));

        // 更新Redis榜单
        roomUserGift.addSink(new RedisRankingSink());
        env.execute("Live Gift Ranking");
    }
}

class RedisRankingSink extends RichSinkFunction<Tuple3<String, String, Long>> {
    private JedisPool jedisPool;

    @Override
    public void open(Configuration parameters) {
        jedisPool = new JedisPool(new JedisPoolConfig(), "redis-cluster", 6379);
    }

    @Override
    public void invoke(Tuple3<String, String, Long> value, Context context) {
        String roomId = value.f0;
        String userId = value.f1;
        long amount = value.f2;
        String key = "ranking:gift:" + roomId;
        try (Jedis jedis = jedisPool.getResource()) {
            jedis.zincrby(key, amount, userId);
            jedis.expire(key, 86400); // 24小时过期
        }
    }
}
"""
    },
    'code2': {
        'desc':'以下Python代码展示了基于BERT的直播弹幕文本审核模型，对弹幕进行多标签分类（政治敏感、色情、广告、辱骂、正常）：',
        'lang':'python',
        'code':"""import torch
import torch.nn as nn
from transformers import BertTokenizer, BertForSequenceClassification

class DanmuModerator:
    def __init__(self, model_path, num_labels=5, max_length=128):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path, num_labels=num_labels)
        self.model.eval()
        self.max_length = max_length
        self.label_map = {0: 'POLITICAL', 1: 'PORN', 2: 'AD', 3: 'ABUSE', 4: 'NORMAL'}

    def predict(self, texts):
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt"
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)
            predictions = torch.argmax(probs, dim=-1)
            confidences = torch.max(probs, dim=-1).values

        results = []
        for pred, conf in zip(predictions, confidences):
            label = self.label_map[pred.item()]
            score = conf.item()
            results.append({
                "label": label,
                "score": round(score, 4),
                "action": "BLOCK" if label != "NORMAL" and score > 0.9 else "PASS"
            })
        return results

# 使用示例
# moderator = DanmuModerator("bert-danmu-moderation")
# batch_texts = ["主播好棒", "低价出售账号", "****"]
# results = moderator.predict(batch_texts)
"""
    },
    'code3': """# Flink 直播实时计算集群配置
execution:
  planner: blink
  type: streaming
  checkpointing:
    mode: EXACTLY_ONCE
    interval: 5000ms
    timeout: 300000ms
    min-pause: 500ms
    max-concurrent: 1
  restart-strategy:
    type: exponential-delay
    exponential-delay:
      initial-backoff: 1s
      max-backoff: 60s
      backoff-multiplier: 2.0
      reset-backoff-threshold: 300s
state:
  backend: rocksdb
  checkpoints:
    dir: hdfs:///flink/checkpoints/livestream
  backend.incremental: true
  backend.rocksdb.memory.managed: true
parallelism:
  default: 512
""",
    'results': [
        {'category':'实时性','name':'弹幕端到端延迟','before':'200ms','after':'25ms','delta':'-87.5%'},
        {'category':'吞吐','name':'弹幕峰值处理量','before':'30万/秒','after':'120万/秒','delta':'+300%'},
        {'category':'审核','name':'内容审核响应时间','before':'5秒','after':'80ms','delta':'-98.4%'},
        {'category':'业务','name':'直播间互动率','before':'12%','after':'19%','delta':'+58.3%'},
        {'category':'稳定性','name':'系统可用性','before':'99.95%','after':'99.995%','delta':'+0.045%'},
        {'category':'安全','name':'违规内容漏放率','before':'0.5%','after':'0.05%','delta':'-90%'},
    ]
})

# 4. Retail
case_studies.append({
    'path': 'phase2-case-studies/retail/11.17.1-realtime-pricing.md',
    'title': '零售实时动态定价深度案例研究',
    'number': '11.17.1',
    'industry': '零售/电商',
    'scenario': '实时价格调整、竞争分析、库存联动定价',
    'scale': 'SKU 100万+, 日调价请求500万+, 覆盖门店3000+',
    'goals': [
        {'category':'响应速度','metric':'价格调整生效时间','target':'< 5秒'},
        {'category':'毛利率','metric':'整体毛利率提升','target':'+5%'},
        {'category':'库存周转','metric':'库存周转天数','target':'-20%'},
        {'category':'竞争力','metric':'价格竞争力指数','target':'Top 3'},
        {'category':'自动化','metric':'自动调价覆盖率','target':'80%'},
    ],
    'metrics': [
        {'name':'价格调整生效时间','before':'天级','after':'3秒','delta':'-99.9%'},
        {'name':'整体毛利率','before':'20.0%','after':'21.5%','delta':'+7.5%'},
        {'name':'库存周转天数','before':'30天','after':'22天','delta':'-26.7%'},
        {'name':'滞销SKU占比','before':'15%','after':'8%','delta':'-46.7%'},
        {'name':'促销损耗率','before':'5.0%','after':'2.5%','delta':'-50%'},
        {'name':'人工调价工作量','before':'基准','after':'-70%','delta':'节省'},
    ],
    'pain_points': [
        {'title':'价格战频繁导致利润承压','desc':'电商平台和竞争对手频繁发起价格战，传统的人工调价模式响应迟缓，往往在对手降价数小时甚至数天后才跟进，导致市场份额流失；而盲目跟进降价又严重侵蚀利润空间。'},
        {'title':'库存与价格决策脱节','desc':'大量SKU的库存状态（在库量、临期情况、区域分布）与定价策略缺乏实时联动。畅销品缺货时未能及时提价抑制需求，滞销品积压时未能快速降价促销清仓，造成机会损失和库存报废。'},
        {'title':'促销计划与实际执行偏差大','desc':'促销活动开始前制定的价格方案，在实际执行过程中常因市场反应、库存变化、竞品动态而需要调整，但人工审批流程冗长，错失最佳调整窗口。'},
        {'title':'多渠道价格不一致','desc':'同一商品在自有APP、小程序、第三方电商平台、线下门店的价格不同步，引发消费者投诉、渠道冲突和价格形象受损。'},
    ],
    'tech_stack': [
        {'layer':'数据采集','tech':'Scrapy + Flink CDC','reason':'竞品价格抓取、内部库存变更捕获'},
        {'layer':'消息队列','tech':'Apache Kafka 3.6','reason':'高吞吐事件总线'},
        {'layer':'流计算引擎','tech':'Apache Flink 1.18','reason':'实时价格计算、Broadcast State'},
        {'layer':'规则引擎','tech':'Drools + 自研策略引擎','reason':'复杂定价规则的可配置化'},
        {'layer':'实时存储','tech':'Redis Cluster + TiDB','reason':'价格缓存、事务一致性'},
        {'layer':'预测模型','tech':'Python + Prophet + XGBoost','reason':'需求预测与价格弹性建模'},
    ],
    'architecture_mermaid': """graph TB
    subgraph External[外部数据源]
        E1[竞品价格爬虫]
        E2[天气数据]
        E3[节假日日历]
    end
    subgraph Internal[内部系统]
        I1[POS销售系统]
        I2[WMS仓储系统]
        I3[ERP主数据]
    end
    subgraph Kafka[Kafka消息层]
        K1[库存变更Topic]
        K2[竞品价格Topic]
        K3[销售事件Topic]
    end
    subgraph Flink[实时定价引擎]
        F1[库存状态流]
        F2[竞品价格流]
        F3[需求预测流]
        F4[定价决策]<\br/>Broadcast State
    end
    subgraph Storage[存储层]
        R1[(Redis<br/>当前价格)]
        DB1[(TiDB<br/>价格历史)]
    end
    subgraph Channels[销售渠道]
        C1[APP/小程序]
        C2[线下POS]
        C3[电商平台]
    end
    E1 --> K2
    I1 --> K3
    I2 --> K1
    K1 --> F1 --> F4
    K2 --> F2 --> F4
    K3 --> F3 --> F4
    F4 --> R1 --> C1 & C2 & C3
    F4 --> DB1
""",
    'code1': {
        'desc':'以下Java代码展示了Flink中使用Broadcast State实现动态定价规则的热更新，主数据流为SKU销售事件，广播流为定价策略变更：',
        'lang':'java',
        'code':"""import org.apache.flink.streaming.api.datastream.BroadcastStream;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.api.common.state.MapStateDescriptor;
import org.apache.flink.api.common.state.BroadcastState;
import org.apache.flink.streaming.api.functions.co.BroadcastProcessFunction;
import org.apache.flink.util.Collector;

public class DynamicPricingJob {

    private static final MapStateDescriptor<String, PricingRule> ruleStateDescriptor =
        new MapStateDescriptor<>("pricingRules", String.class, PricingRule.class);

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // 主数据流：SKU销售与库存事件
        DataStream<SalesEvent> salesStream = env
            .addSource(new KafkaSource<SalesEvent>("sales-events"))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<SalesEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
            );

        // 广播流：定价策略更新
        DataStream<PricingRule> ruleStream = env
            .addSource(new KafkaSource<PricingRule>("pricing-rules"));

        BroadcastStream<PricingRule> broadcastRules = ruleStream.broadcast(ruleStateDescriptor);

        DataStream<PriceDecision> decisions = salesStream
            .connect(broadcastRules)
            .process(new BroadcastProcessFunction<SalesEvent, PricingRule, PriceDecision>() {
                @Override
                public void processElement(SalesEvent event, ReadOnlyContext ctx, Collector<PriceDecision> out) {
                    PricingRule rule = ctx.getBroadcastState(ruleStateDescriptor).get(event.getSkuId());
                    if (rule == null) {
                        rule = ctx.getBroadcastState(ruleStateDescriptor).get("DEFAULT");
                    }
                    double newPrice = calculatePrice(event, rule);
                    out.collect(new PriceDecision(event.getSkuId(), newPrice, event.getTimestamp()));
                }

                @Override
                public void processBroadcastElement(PricingRule rule, Context ctx, Collector<PriceDecision> out) {
                    ctx.getBroadcastState(ruleStateDescriptor).put(rule.getSkuId(), rule);
                }

                private double calculatePrice(SalesEvent event, PricingRule rule) {
                    double basePrice = rule.getBasePrice();
                    double inventoryFactor = event.getInventory() < rule.getSafetyStock() ? 1.15 : 1.0;
                    double competitorFactor = event.getCompetitorPrice() < basePrice ? 0.98 : 1.0;
                    return basePrice * inventoryFactor * competitorFactor;
                }
            });

        decisions.addSink(new RedisPriceSink());
        env.execute("Dynamic Pricing Job");
    }
}
"""
    },
    'code2': {
        'desc':'以下Python代码实现了基于价格弹性和需求预测的智能定价模型，输出最优建议价格以最大化预期利润：',
        'lang':'python',
        'code':"""import numpy as np
from scipy.optimize import minimize_scalar

class ElasticityPricingModel:
    def __init__(self, base_price, cost, elasticity_coeff):
        self.base_price = base_price
        self.cost = cost
        self.elasticity = elasticity_coeff  # 负值，如 -2.0

    def expected_demand(self, price):
        # 需求价格弹性模型：Q = Q0 * (P/P0)^elasticity
        relative_change = (price / self.base_price) ** self.elasticity
        base_demand = 1000  # 基准需求
        return base_demand * relative_change

    def profit(self, price):
        demand = self.expected_demand(price)
        return -1 * (price - self.cost) * demand  # 负号用于最小化

    def optimal_price(self, bounds=(0.5, 2.0)):
        # 在基准价格的0.5倍到2.0倍之间寻找最优价格
        result = minimize_scalar(
            lambda ratio: self.profit(self.base_price * ratio),
            bounds=bounds,
            method='bounded'
        )
        optimal_ratio = result.x
        optimal_price = self.base_price * optimal_ratio
        max_profit = -result.fun
        return {
            "optimal_price": round(optimal_price, 2),
            "optimal_ratio": round(optimal_ratio, 3),
            "expected_demand": round(self.expected_demand(optimal_price), 0),
            "max_profit": round(max_profit, 2)
        }

# 使用示例
# model = ElasticityPricingModel(base_price=100, cost=60, elasticity_coeff=-2.5)
# decision = model.optimal_price()
"""
    },
    'code3': """# 动态定价规则引擎配置示例
pricing:
  default_strategy: "competitive_margin"
  rules:
    - sku_pattern: "ELECTRONICS_*"
      strategy: "lowest_competitor_plus"
      params:
        margin_floor: 0.05
        competitor_weight: 0.8
    - sku_pattern: "FRESH_*"
      strategy: "inventory_driven"
      params:
        discount_steps: [0.9, 0.8, 0.7, 0.5]
        hours_to_expiry: [24, 12, 6, 2]
    - sku_pattern: "APPAREL_*"
      strategy: "seasonal_promotion"
      params:
        season_boost: 1.2
        clearance_discount: 0.6
  constraints:
    min_margin_rate: 0.03
    max_daily_price_change: 0.30
    channel_sync_delay_ms: 1000
""",
    'results': [
        {'category':'响应速度','name':'价格调整生效时间','before':'天级','after':'3秒','delta':'-99.9%'},
        {'category':'盈利','name':'整体毛利率','before':'20.0%','after':'21.5%','delta':'+7.5%'},
        {'category':'库存','name':'库存周转天数','before':'30天','after':'22天','delta':'-26.7%'},
        {'category':'库存','name':'滞销SKU占比','before':'15%','after':'8%','delta':'-46.7%'},
        {'category':'促销','name':'促销损耗率','before':'5.0%','after':'2.5%','delta':'-50%'},
        {'category':'效率','name':'人工调价工作量','before':'基准','after':'-70%','delta':'节省'},
    ]
})

# 5. Insurance
case_studies.append({
    'path': 'phase2-case-studies/insurance/11.18.1-claims-processing.md',
    'title': '保险实时理赔处理深度案例研究',
    'number': '11.18.1',
    'industry': '保险/金融',
    'scenario': '理赔申请实时处理、欺诈检测、自动核赔',
    'scale': '日理赔申请10万+, 峰值并发5000+, 平均处理时效< 5分钟',
    'goals': [
        {'category':'时效','metric':'小额理赔处理时效','target':'< 5分钟'},
        {'category':'自动化','metric':'自动核赔率','target':'> 70%'},
        {'category':'风控','metric':'欺诈识别准确率','target':'> 90%'},
        {'category':'体验','metric':'客户满意度(NPS)','target':'> 60'},
        {'category':'成本','metric':'单案处理成本','target':'-40%'},
    ],
    'metrics': [
        {'name':'小额理赔处理时效','before':'3天','after':'3分钟','delta':'-99.9%'},
        {'name':'自动核赔率','before':'20%','after':'75%','delta':'+275%'},
        {'name':'欺诈识别准确率','before':'60%','after':'92%','delta':'+53.3%'},
        {'name':'客户满意度(NPS)','before':'25','after':'68','delta':'+172%'},
        {'name':'单案处理成本','before':'120元','after':'65元','delta':'-45.8%'},
        {'name':'理赔纠纷率','before':'3.5%','after':'0.8%','delta':'-77.1%'},
    ],
    'pain_points': [
        {'title':'人工审核效率低下','desc':'某大型财产保险公司日均理赔申请超过10万件，传统模式下大量案件依赖人工核赔员逐一审核。尤其在自然灾害、大型事故后，案件量激增，审核积压严重，客户等待时间长，投诉率高。'},
        {'title':'欺诈理赔损失巨大','desc':'保险欺诈手段不断升级，从单一个体的虚假索赔发展到有组织的团伙骗保。传统基于经验规则的反欺诈系统识别能力有限，大量欺诈案件在事后稽核中才被发现，此时资金已赔付，追回难度大。'},
        {'title':'客户期望秒级理赔体验','desc':'随着互联网保险和移动理赔的普及，客户对理赔时效的期望从天级缩短至分钟级甚至秒级。特别是在车险小额案件、意外险医疗案件等高频场景中，快速的理赔体验直接影响客户留存和口碑。'},
        {'title':' legacy系统烟囱林立','desc':'核心系统、影像系统、反欺诈系统、财务系统各自独立，数据交换依赖接口文件和定时任务。理赔案件的完整信息分散在多个系统中，核赔员需要在多个界面之间切换查询，效率极低。'},
    ],
    'tech_stack': [
        {'layer':'接入层','tech':'移动APP + OCR识别','reason':'客户自助报案、票据自动识别'},
        {'layer':'消息队列','tech':'Apache Kafka 3.6','reason':'理赔事件高可靠流转'},
        {'layer':'流计算引擎','tech':'Apache Flink 1.18','reason':'实时规则校验、流程编排'},
        {'layer':'规则引擎','tech':'Drools + 自研核赔引擎','reason':'复杂核赔规则的可配置化'},
        {'layer':'AI模型','tech':'Python + XGBoost + GNN','reason':'欺诈检测、医疗合理性审核'},
        {'layer':'核心存储','tech':'TiDB + MongoDB','reason':'结构化与非结构化数据统一存储'},
    ],
    'architecture_mermaid': """graph TB
    subgraph Client[客户端]
        C1[保险APP]
        C2[代理人端]
        C3[客服系统]
    end
    subgraph Intake[受理层]
        I1[OCR识别]
        I2[影像存储]
        I3[报案录入]
    end
    subgraph Kafka[Kafka消息层]
        K1[理赔申请Topic]
        K2[影像Topic]
        K3[审核结果Topic]
    end
    subgraph Flink[实时处理层]
        F1[信息完整性校验]
        F2[规则引擎核赔]
        F3[欺诈检测]
        F4[自动赔付路由]
    end
    subgraph AI[AI审核层]
        A1[医疗合理性模型]
        A2[反欺诈模型]
        A3[定损评估模型]
    end
    subgraph Core[核心系统]
        DB1[(TiDB<br/>理赔主表)]
        DB2[(MongoDB<br/>影像文档)]
        PAY[支付网关]
    end
    C1 --> I1 --> I2 --> K2
    C1 --> I3 --> K1
    K1 --> F1 --> F2 --> F4
    F2 --> A1
    F3 --> A2
    F4 --> DB1 --> PAY
    DB1 --> DB2
""",
    'code1': {
        'desc':'以下Java代码展示了基于Flink的理赔流程编排器，使用KeyedProcessFunction管理每个理赔案件的审核状态机，实现自动流转与超时处理：',
        'lang':'java',
        'code':"""import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;

public class ClaimsOrchestrationJob {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        DataStream<ClaimEvent> claimStream = env
            .addSource(new KafkaSource<ClaimEvent>("claims-topic"))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<ClaimEvent>forBoundedOutOfOrderness(Duration.ofSeconds(10))
            );

        DataStream<ClaimStatusUpdate> updates = claimStream
            .keyBy(ClaimEvent::getClaimId)
            .process(new ClaimStateMachine());

        updates.addSink(new TiDBSink<>("claim_status"));
        env.execute("Claims Orchestration");
    }
}

class ClaimStateMachine extends KeyedProcessFunction<String, ClaimEvent, ClaimStatusUpdate> {
    private ValueState<ClaimContext> contextState;

    @Override
    public void open(Configuration parameters) {
        contextState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("claimContext", ClaimContext.class));
    }

    @Override
    public void processElement(ClaimEvent event, Context ctx, Collector<ClaimStatusUpdate> out) throws Exception {
        ClaimContext context = contextState.value();
        if (context == null) {
            context = new ClaimContext(ctx.getCurrentKey(), "INIT", ctx.timestamp());
        }

        switch (event.getEventType()) {
            case "SUBMIT":
                context.setStatus("UNDER_REVIEW");
                out.collect(new ClaimStatusUpdate(ctx.getCurrentKey(), "UNDER_REVIEW", ctx.timestamp()));
                // 设置5分钟超时计时器
                ctx.timerService().registerEventTimeTimer(ctx.timestamp() + 300000);
                break;
            case "FRAUD_CHECK_PASS":
                if ("UNDER_REVIEW".equals(context.getStatus())) {
                    context.setStatus("AUTO_APPROVED");
                    out.collect(new ClaimStatusUpdate(ctx.getCurrentKey(), "AUTO_APPROVED", ctx.timestamp()));
                }
                break;
            case "MANUAL_REVIEW_REQUIRED":
                context.setStatus("MANUAL_REVIEW");
                out.collect(new ClaimStatusUpdate(ctx.getCurrentKey(), "MANUAL_REVIEW", ctx.timestamp()));
                break;
        }
        contextState.update(context);
    }

    @Override
    public void onTimer(long timestamp, OnTimerContext ctx, Collector<ClaimStatusUpdate> out) throws Exception {
        ClaimContext context = contextState.value();
        if (context != null && "UNDER_REVIEW".equals(context.getStatus())) {
            out.collect(new ClaimStatusUpdate(ctx.getCurrentKey(), "ESCALATE", timestamp));
        }
    }
}
"""
    },
    'code2': {
        'desc':'以下Python代码展示了基于图神经网络（GNN）的保险欺诈检测模型，通过构建投保人-代理人-医疗机构关系图识别团伙欺诈模式：',
        'lang':'python',
        'code':"""import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class FraudGNN(torch.nn.Module):
    def __init__(self, num_features, hidden_dim=64, num_classes=2):
        super(FraudGNN, self).__init__()
        self.conv1 = GCNConv(num_features, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.classifier = torch.nn.Linear(hidden_dim, num_classes)
        self.dropout = torch.nn.Dropout(0.3)

    def forward(self, x, edge_index):
        # x: 节点特征矩阵 [num_nodes, num_features]
        # edge_index: 边索引 [2, num_edges]
        h = self.conv1(x, edge_index)
        h = F.relu(h)
        h = self.dropout(h)
        h = self.conv2(h, edge_index)
        h = F.relu(h)
        out = self.classifier(h)
        return F.log_softmax(out, dim=1)

# 欺诈评分服务
class FraudScorer:
    def __init__(self, model_path):
        self.model = FraudGNN(num_features=20)
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def score_claim(self, node_features, edges):
        with torch.no_grad():
            x = torch.tensor(node_features, dtype=torch.float)
            edge_index = torch.tensor(edges, dtype=torch.long)
            logits = self.model(x, edge_index)
            probs = torch.exp(logits)
            fraud_prob = probs[0][1].item()  # 假设节点0为当前案件
        return {
            "fraud_probability": round(fraud_prob, 4),
            "decision": "REJECT" if fraud_prob > 0.85 else "MANUAL" if fraud_prob > 0.5 else "PASS"
        }
"""
    },
    'code3': """# 理赔实时处理 Flink 配置
execution:
  planner: blink
  type: streaming
  checkpointing:
    mode: EXACTLY_ONCE
    interval: 60000ms
    timeout: 600000ms
    min-pause: 1000ms
    max-concurrent: 1
  restart-strategy:
    type: fixed-delay
    fixed-delay:
      attempts: 5
      delay: 30s
state:
  backend: rocksdb
  checkpoints:
    dir: hdfs:///flink/checkpoints/insurance
  backend.incremental: true
  backend.rocksdb.memory.managed: true
parallelism:
  default: 128
""",
    'results': [
        {'category':'时效','name':'小额理赔处理时效','before':'3天','after':'3分钟','delta':'-99.9%'},
        {'category':'自动化','name':'自动核赔率','before':'20%','after':'75%','delta':'+275%'},
        {'category':'风控','name':'欺诈识别准确率','before':'60%','after':'92%','delta':'+53.3%'},
        {'category':'体验','name':'客户满意度(NPS)','before':'25','after':'68','delta':'+172%'},
        {'category':'成本','name':'单案处理成本','before':'120元','after':'65元','delta':'-45.8%'},
        {'category':'质量','name':'理赔纠纷率','before':'3.5%','after':'0.8%','delta':'-77.1%'},
    ]
})

# 6. Education
case_studies.append({
    'path': 'phase2-case-studies/education/11.22.1-online-learning.md',
    'title': '教育在线学习分析深度案例研究',
    'number': '11.22.1',
    'industry': '教育/在线学习',
    'scenario': '学习行为分析、知识点掌握评估、个性化推荐',
    'scale': '学员1000万+, 课程50万+, 日处理学习事件20亿+',
    'goals': [
        {'category':'学习效果','metric':'课程完课率','target':'> 55%'},
        {'category':'参与度','metric':'人均学习时长','target':'+40%'},
        {'category':'个性化','metric':'推荐准确率','target':'> 80%'},
        {'category':'教学效率','metric':'教师备课效率','target':'+30%'},
        {'category':'满意度','metric':'学员NPS','target':'> 50'},
    ],
    'metrics': [
        {'name':'课程完课率','before':'45%','after':'58%','delta':'+28.9%'},
        {'name':'人均学习时长','before':'30分钟/天','after':'48分钟/天','delta':'+60%'},
        {'name':'推荐内容点击率','before':'8%','after':'18%','delta':'+125%'},
        {'name':'教师备课时间','before':'3小时/课','after':'2小时/课','delta':'-33.3%'},
        {'name':'学员NPS','before':'32','after':'55','delta':'+71.9%'},
        {'name':'退课率','before':'12%','after':'6%','delta':'-50%'},
    ],
    'pain_points': [
        {'title':'完课率低、学习动力不足','desc':'在线教育平台普遍存在"高开低走"的现象，大量学员在注册后很快流失。传统课程缺乏实时互动和个性化反馈，学员难以感知自己的进步，学习动力逐渐消退。据统计，行业平均完课率不足30%。'},
        {'title':'教学内容与学员水平不匹配','desc':'同一班级的学员知识基础、学习速度和理解能力差异巨大。统一进度的录播课程无法满足个体需求，基础薄弱的学员跟不上，能力强的学员又觉得内容过于简单，导致两头抱怨。'},
        {'title':'教师缺乏实时学情洞察','desc':'在大型直播课或录播课中，教师难以实时掌握数千甚至数万名学员的学习状态（如哪些地方反复观看、哪些题目错误率高、哪些学员开始走神），无法及时调整教学策略。'},
        {'title':'推荐系统冷启动严重','desc':'新学员和新课程缺乏历史行为数据，协同过滤等常规推荐算法效果差，导致新学员首页推荐内容与其兴趣不匹配，影响首因效应和留存率。'},
    ],
    'tech_stack': [
        {'layer':'数据采集','tech':'SDK + Web埋点','reason':'全端学习行为采集'},
        {'layer':'消息队列','tech':'Apache Kafka 3.6','reason':'高并发事件流'},
        {'layer':'流计算引擎','tech':'Apache Flink 1.18','reason':'实时知识状态估计'},
        {'layer':'知识追踪','tech':'Python + Deep Knowledge Tracing','reason':'精准掌握度建模'},
        {'layer':'推荐引擎','tech':'Two-Tower DNN + Redis','reason':'实时个性化推荐'},
        {'layer':'分析存储','tech':'ClickHouse','reason':'大规模学习分析'},
    ],
    'architecture_mermaid': """graph TB
    subgraph Terminal[学习终端]
        T1[APP]
        T2[PC网页]
        T3[平板]
    end
    subgraph Collect[采集层]
        C1[行为SDK]
        C2[视频播放埋点]
        C3[答题事件]
    end
    subgraph Kafka[Kafka消息层]
        K1[学习行为Topic]
        K2[答题Topic]
        K3[互动Topic]
    end
    subgraph Flink[实时计算层]
        F1[学习时长聚合]
        F2[知识状态DKT]
        F3[实时推荐]
    end
    subgraph Model[模型层]
        M1[知识追踪模型]
        M2[内容理解模型]
        M3[推荐模型]
    end
    subgraph Storage[存储层]
        R1[(Redis<br/>学员画像)]
        DB1[(ClickHouse<br/>学习分析)]
    end
    subgraph App[应用层]
        A1[学习报告]
        A2[教师dashboard]
        A3[课程推荐]
    end
    T1 --> C1 --> K1
    T2 --> C2 --> K1
    T3 --> C3 --> K2
    K1 --> F1 --> DB1
    K2 --> F2 --> M1
    F1 & F2 --> F3 --> M3 --> R1
    R1 --> A1 & A3
    DB1 --> A2
""",
    'code1': {
        'desc':'以下Java代码展示了基于Flink的实时学习时长聚合作业，使用会话窗口（Session Window）自动识别学员的学习会话并统计有效学习时长：',
        'lang':'java',
        'code':"""import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.assigners.EventTimeSessionWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

public class LearningSessionJob {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<LearningEvent> eventStream = env
            .addSource(new KafkaSource<LearningEvent>("learning-events"))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<LearningEvent>forBoundedOutOfOrderness(Duration.ofSeconds(10))
                    .withTimestampAssigner((event, ts) -> event.getEventTime())
            );

        // 会话窗口：学员5分钟无活动视为一个会话结束
        DataStream<SessionSummary> sessions = eventStream
            .keyBy(LearningEvent::getUserId)
            .window(EventTimeSessionWindows.withGap(Time.minutes(5)))
            .aggregate(new SessionAggregateFunction(), new SessionProcessFunction());

        sessions.addSink(new ClickHouseSink<>("learning_sessions"));
        env.execute("Learning Session Aggregation");
    }
}

class SessionAggregateFunction implements AggregateFunction<LearningEvent, SessionAccumulator, SessionSummary> {
    @Override
    public SessionAccumulator createAccumulator() {
        return new SessionAccumulator();
    }

    @Override
    public SessionAccumulator add(LearningEvent value, SessionAccumulator accumulator) {
        accumulator.addEvent(value);
        return accumulator;
    }

    @Override
    public SessionSummary getResult(SessionAccumulator accumulator) {
        return accumulator.toSummary();
    }

    @Override
    public SessionAccumulator merge(SessionAccumulator a, SessionAccumulator b) {
        a.merge(b);
        return a;
    }
}
"""
    },
    'code2': {
        'desc':'以下Python代码实现了基于Deep Knowledge Tracing（DKT）的知识点掌握度预测模型，输入学员答题序列，输出各知识点的掌握概率：',
        'lang':'python',
        'code':"""import torch
import torch.nn as nn

class DKTModel(nn.Module):
    def __init__(self, num_skills, hidden_dim=128, embedding_dim=64):
        super(DKTModel, self).__init__()
        self.num_skills = num_skills
        self.embedding_dim = embedding_dim
        # 交互嵌入：将(skill_id, correctness)组合为输入
        self.interaction_embed = nn.Embedding(num_skills * 2, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True, num_layers=2, dropout=0.3)
        self.output_layer = nn.Linear(hidden_dim, num_skills)
        self.sigmoid = nn.Sigmoid()

    def forward(self, interactions):
        # interactions: [batch_size, seq_len] 其中值为 skill_id * 2 + correctness
        embeds = self.interaction_embed(interactions)  # [batch, seq_len, embed_dim]
        lstm_out, _ = self.lstm(embeds)  # [batch, seq_len, hidden_dim]
        logits = self.output_layer(lstm_out)  # [batch, seq_len, num_skills]
        return self.sigmoid(logits)

class KnowledgeTracer:
    def __init__(self, model_path, num_skills):
        self.model = DKTModel(num_skills)
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def predict_mastery(self, interaction_history):
        # interaction_history: list of (skill_id, correctness)
        input_seq = torch.tensor([[s * 2 + c for s, c in interaction_history]])
        with torch.no_grad():
            probs = self.model(input_seq)  # [1, seq_len, num_skills]
        # 返回最后一个时间步各知识点的掌握概率
        mastery = probs[0, -1, :].numpy()
        return {f"skill_{i}": round(float(p), 4) for i, p in enumerate(mastery)}

# 使用示例
# tracer = KnowledgeTracer("dkt_model.pt", num_skills=500)
# mastery = tracer.predict_mastery([(23, 1), (45, 0), (23, 1)])
"""
    },
    'code3': """# 在线学习实时分析 Flink 配置
execution:
  planner: blink
  type: streaming
  checkpointing:
    mode: EXACTLY_ONCE
    interval: 30000ms
    timeout: 300000ms
    min-pause: 500ms
    max-concurrent: 1
  restart-strategy:
    type: fixed-delay
    fixed-delay:
      attempts: 10
      delay: 10s
state:
  backend: rocksdb
  checkpoints:
    dir: hdfs:///flink/checkpoints/education
  backend.incremental: true
  backend.rocksdb.memory.managed: true
parallelism:
  default: 256
""",
    'results': [
        {'category':'学习效果','name':'课程完课率','before':'45%','after':'58%','delta':'+28.9%'},
        {'category':'参与度','name':'人均学习时长','before':'30分钟/天','after':'48分钟/天','delta':'+60%'},
        {'category':'个性化','name':'推荐内容点击率','before':'8%','after':'18%','delta':'+125%'},
        {'category':'教学效率','name':'教师备课时间','before':'3小时/课','after':'2小时/课','delta':'-33.3%'},
        {'category':'满意度','name':'学员NPS','before':'32','after':'55','delta':'+71.9%'},
        {'category':'运营','name':'退课率','before':'12%','after':'6%','delta':'-50%'},
    ]
})


# 7. Real Estate / Smart Building
case_studies.append({
    'path': 'phase2-case-studies/realestate/11.21.1-smart-building.md',
    'title': '房地产智慧楼宇深度案例研究',
    'number': '11.21.1',
    'industry': '房地产/智慧物业',
    'scenario': '楼宇设备监控、能耗优化、安防预警、空间管理',
    'scale': '管理楼宇100+, 接入传感器50万+, 日处理数据10TB',
    'goals': [
        {'category':'能耗','metric':'年度能耗成本','target':'-20%'},
        {'category':'安全','metric':'安防事件响应时间','target':'< 30秒'},
        {'category':'体验','metric':'租户满意度','target':'> 90%'},
        {'category':'效率','metric':'设备故障发现时间','target':'-50%'},
        {'category':'运营','metric':'物业管理人力成本','target':'-15%'},
    ],
    'metrics': [
        {'name':'年度能耗成本','before':'基准','after':'-22%','delta':'节省'},
        {'name':'安防事件响应时间','before':'10分钟','after':'25秒','delta':'-95.8%'},
        {'name':'租户满意度','before':'75%','after':'93%','delta':'+24%'},
        {'name':'设备故障发现时间','before':'2小时','after':'45分钟','delta':'-62.5%'},
        {'name':'平均维修工单时长','before':'4小时','after':'2.5小时','delta':'-37.5%'},
        {'name':'碳排放强度','before':'基准','after':'-18%','delta':'减少'},
    ],
    'pain_points': [
        {'title':'楼宇能耗居高不下','desc':'某大型物业管理集团运营超过100栋商业楼宇和产业园区，空调、照明、电梯等设备24小时运行，能耗成本占总运营成本的40%以上。由于缺乏精细化的能耗监测和智能调控手段，大量能源在无人时段和低负载时段被浪费。'},
        {'title':'安防响应迟缓、事件漏报多','desc':'传统安防依赖人工巡逻和固定摄像头事后回放，从事件发生到被发现平均需要10分钟以上。对于非法闯入、火灾烟雾、电梯困人等紧急情况，延迟响应可能导致严重后果。'},
        {'title':'设备维护被动低效','desc':'楼宇内的暖通空调（HVAC）、给排水、供配电等设备数量庞大，传统定期巡检模式无法及时发现潜在故障，往往在设备完全损坏后才进行抢修，维修成本高且影响租户正常办公。'},
        {'title':'多系统数据孤岛严重','desc':'楼宇自动化系统（BAS）、消防系统、门禁系统、能耗管理系统由不同厂商建设，数据格式和通信协议各异，缺乏统一的数据平台，难以进行跨系统的联动分析和全局优化。'},
    ],
    'tech_stack': [
        {'layer':'感知层','tech':'BACnet/Modbus/LoRa传感器','reason':'楼宇设备多协议接入'},
        {'layer':'边缘网关','tech':'边缘计算网关','reason':'本地预处理、协议转换'},
        {'layer':'消息队列','tech':'Apache Kafka 3.6','reason':'海量IoT数据高可靠传输'},
        {'layer':'流计算引擎','tech':'Apache Flink 1.18','reason':'实时能耗计算、CEP安防'},
        {'layer':'时序数据库','tech':'TDengine','reason':'高效时序数据存储与查询'},
        {'layer':'数字孪生','tech':'BIM + 3D可视化引擎','reason':'楼宇状态全息呈现'},
    ],
    'architecture_mermaid': """graph TB
    subgraph Sensors[设备与传感器层]
        S1[温湿度传感器]
        S2[电表/水表]
        S3[空调控制器]
        S4[电梯监控]
        S5[摄像头/门禁]
        S6[烟感/消防]
    end
    subgraph Edge[边缘网关层]
        E1[协议转换网关]
        E2[边缘预处理]
        E3[本地控制]
    end
    subgraph Kafka[Kafka消息层]
        K1[能耗Topic]
        K2[安防Topic]
        K3[设备状态Topic]
    end
    subgraph Flink[实时计算层]
        F1[能耗实时统计]
        F2[设备异常检测]
        F3[安防事件CEP]
    end
    subgraph Storage[存储层]
        DB1[(TDengine<br/>时序数据)]
        DB2[(PostgreSQL<br/>楼宇元数据)]
    end
    subgraph App[应用层]
        A1[能源管理大屏]
        A2[安防指挥中心]
        A3[设备运维APP]
        A4[BIM数字孪生]
    end
    S1 & S2 & S3 --> E1 --> K1 --> F1 --> DB1 --> A1
    S4 --> E1 --> K3 --> F2 --> DB1 --> A3
    S5 & S6 --> E2 --> K2 --> F3 --> A2
    DB1 --> A4
""",
    'code1': {
        'desc':'以下Java代码展示了基于Flink CEP的楼宇安防事件关联分析，用于检测"门禁刷卡后短时间内同一区域出现翻越围墙"的异常入侵模式：',
        'lang':'java',
        'code':"""import org.apache.flink.cep.CEP;
import org.apache.flink.cep.Pattern;
import org.apache.flink.cep.pattern.conditions.SimpleCondition;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.cep.pattern.conditions.IterativeCondition;

import java.util.List;
import java.util.Map;

public class SecurityCEPJob {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        DataStream<SecurityEvent> eventStream = env
            .addSource(new KafkaSource<SecurityEvent>("security-events"))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<SecurityEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
            );

        // 定义入侵模式：某区域门禁正常刷卡后30秒内，同区域围墙红外报警
        Pattern<SecurityEvent, ?> intrusionPattern = Pattern.<SecurityEvent>begin("access_granted")
            .where(new SimpleCondition<SecurityEvent>() {
                @Override
                public boolean filter(SecurityEvent event) {
                    return "ACCESS_CONTROL".equals(event.getDeviceType())
                        && "GRANTED".equals(event.getEventType());
                }
            })
            .followedBy("perimeter_breach")
            .where(new IterativeCondition<SecurityEvent>() {
                @Override
                public boolean filter(SecurityEvent event, Context<SecurityEvent> ctx) {
                    return "PERIMETER_ALARM".equals(event.getDeviceType())
                        && "BREACH".equals(event.getEventType());
                }
            })
            .within(Time.seconds(30));

        DataStream<SecurityAlert> alerts = CEP.pattern(
                eventStream.keyBy(SecurityEvent::getZoneId), intrusionPattern)
            .process(new PatternProcessFunction<SecurityEvent, SecurityAlert>() {
                @Override
                public void processMatch(Map<String, List<SecurityEvent>> match, Context ctx, Collector<SecurityAlert> out) {
                    SecurityEvent access = match.get("access_granted").get(0);
                    SecurityEvent breach = match.get("perimeter_breach").get(0);
                    out.collect(new SecurityAlert(
                        access.getZoneId(),
                        "INTRUSION_SUSPECT",
                        String.format("Access at %s then perimeter breach at %s",
                            access.getDeviceId(), breach.getDeviceId()),
                        ctx.timestamp()
                    ));
                }
            });

        alerts.addSink(new AlertSink());
        env.execute("Smart Building Security CEP");
    }
}
"""
    },
    'code2': {
        'desc':'以下Python代码实现了基于LSTM的楼宇能耗预测模型，结合天气预报和历史能耗数据，预测未来24小时各楼宇的电力需求，用于提前优化空调和照明策略：',
        'lang':'python',
        'code':"""import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import StandardScaler

class EnergyForecaster:
    def __init__(self, sequence_length=24, n_features=8):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.scaler = StandardScaler()
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential([
            LSTM(64, return_sequences=True, input_shape=(self.sequence_length, self.n_features)),
            Dropout(0.2),
            LSTM(32, return_sequences=False),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(1, activation='linear')
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

    def prepare_features(self, history_df):
        # 特征包括：小时、温度、湿度、 occupancy_rate、工作日标记、前一天同期能耗、上周同期能耗
        features = history_df[['hour', 'temperature', 'humidity', 'occupancy',
                               'is_workday', 'lag_24h', 'lag_168h', 'rolling_mean_7d']].values
        scaled = self.scaler.fit_transform(features)
        X, y = [], []
        for i in range(len(scaled) - self.sequence_length):
            X.append(scaled[i:i+self.sequence_length])
            y.append(history_df['energy_kwh'].iloc[i+self.sequence_length])
        return np.array(X), np.array(y)

    def train(self, X, y, epochs=30, batch_size=32):
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size, validation_split=0.2)

    def predict_next_24h(self, last_24h_features):
        predictions = []
        current_seq = last_24h_features.copy()
        for _ in range(24):
            pred = self.model.predict(current_seq.reshape(1, self.sequence_length, self.n_features))[0][0]
            predictions.append(pred)
            # 滑动窗口更新
            current_seq = np.roll(current_seq, -1, axis=0)
            current_seq[-1, -1] = pred  # 简化：将预测值作为最新特征
        return predictions

# 使用示例
# forecaster = EnergyForecaster()
# X, y = forecaster.prepare_features(building_history)
# forecaster.train(X, y)
# next_day_energy = forecaster.predict_next_24h(last_24h)
"""
    },
    'code3': """# 智慧楼宇 IoT 数据采集配置
iot:
  gateway:
    protocols:
      - name: "bacnet"
        port: 47808
        poll_interval_ms: 5000
      - name: "modbus"
        port: 502
        poll_interval_ms: 3000
      - name: "lora"
        frequency: "470MHz"
        data_rate: "SF7BW125"
  edge_preprocess:
    enabled: true
    rules:
      - sensor_type: "temperature"
        filter: "outlier"
        threshold: 3.0  # 3-sigma
      - sensor_type: "energy_meter"
        aggregation: "1min_sum"
  kafka:
    brokers: "kafka-1:9092,kafka-2:9092,kafka-3:9092"
    topics:
      - "building.energy"
      - "building.security"
      - "building.equipment"
""",
    'results': [
        {'category':'能耗','name':'年度能耗成本','before':'基准','after':'-22%','delta':'节省'},
        {'category':'安全','name':'安防事件响应时间','before':'10分钟','after':'25秒','delta':'-95.8%'},
        {'category':'体验','name':'租户满意度','before':'75%','after':'93%','delta':'+24%'},
        {'category':'运维','name':'设备故障发现时间','before':'2小时','after':'45分钟','delta':'-62.5%'},
        {'category':'效率','name':'平均维修工单时长','before':'4小时','after':'2.5小时','delta':'-37.5%'},
        {'category':'可持续','name':'碳排放强度','before':'基准','after':'-18%','delta':'减少'},
    ]
})

# 8. Telecom
case_studies.append({
    'path': 'phase2-case-studies/telecom/11.9.1-network-traffic.md',
    'title': '电信网络流量分析深度案例研究',
    'number': '11.9.1',
    'industry': '电信/网络',
    'scenario': '5G网络流量监控、异常检测、QoS保障、容量规划',
    'scale': '5G用户1亿+, IoT设备5000万+, 日流量数据100TB',
    'goals': [
        {'category':'实时性','metric':'故障发现时间','target':'< 30秒'},
        {'category':'定位','metric':'故障根因定位时间','target':'< 5分钟'},
        {'category':'体验','metric':'网络投诉率','target':'-50%'},
        {'category':'效率','metric':'带宽利用率','target':'+30%'},
        {'category':'预测','metric':'流量预测准确率','target':'> 85%'},
    ],
    'metrics': [
        {'name':'故障发现时间','before':'30分钟','after':'20秒','delta':'-98.9%'},
        {'name':'故障定位时间','before':'2小时','after':'4分钟','delta':'-96.7%'},
        {'name':'网络投诉率','before':'0.8%','after':'0.35%','delta':'-56.3%'},
        {'name':'带宽利用率','before':'60%','after':'82%','delta':'+36.7%'},
        {'name':'流量预测准确率','before':'70%','after':'89%','delta':'+27.1%'},
        {'name':'运维人力成本','before':'基准','after':'-25%','delta':'节省'},
    ],
    'pain_points': [
        {'title':'网络流量规模巨大且增长迅猛','desc':'某头部电信运营商拥有超过1亿5G用户和5000万IoT连接，核心网和无线接入网每天产生超过100TB的NetFlow、信令和用户面数据。传统的大数据分析平台（如Hadoop）以小时级甚至天级为周期，无法满足实时网络优化的需求。'},
        {'title':'网络故障发现与定位滞后','desc':'基站退服、核心网元过载、传输链路中断等故障时有发生。传统依赖网管告警和人工排查的模式，从故障发生到定位根因平均需要2小时以上，严重影响用户体验和网络KPI。'},
        {'title':'QoS保障难度高','desc':'5G网络承载了增强移动宽带（eMBB）、超高可靠低时延（uRLLC）和海量机器通信（mMTC）三大类业务，不同业务对带宽、时延、抖动的要求差异巨大。如何在共享网络基础设施上为VIP用户和关键业务提供差异化保障，是网络运营的难题。'},
        {'title':'容量规划缺乏前瞻性','desc':'流量需求随时间、地点、事件波动剧烈。节假日、大型活动、突发事件会导致局部区域流量激增数倍。缺乏精准的流量预测能力，使得网络扩容要么滞后于需求（导致拥塞），要么过度超前（造成资源浪费）。'},
    ],
    'tech_stack': [
        {'layer':'数据采集','tech':'NetFlow/sFlow + DPI探针','reason':'全量网络流量与用户行为采集'},
        {'layer':'消息队列','tech':'Apache Kafka 3.6','reason':'高吞吐、多分区、持久化'},
        {'layer':'流计算引擎','tech':'Apache Flink 1.18','reason':'毫秒级流量统计、CEP故障检测'},
        {'layer':'分析存储','tech':'ClickHouse + Elasticsearch','reason':'实时OLAP与日志检索'},
        {'layer':'AI模型','tech':'Python + Prophet + LSTM','reason':'流量预测与异常检测'},
        {'layer':'数字孪生','tech':'网络拓扑孪生平台','reason':'可视化网络状态与仿真'},
    ],
    'architecture_mermaid': """graph TB
    subgraph Source[数据源层]
        S1[5G基站 gNB]
        S2[核心网 UPF/AMF]
        S3[DPI探针]
        S4[终端设备]
        S5[网管系统]
    end
    subgraph Collection[采集层]
        L1[Logstash/Fluentd]
        K0[Kafka集群<br/>原始数据]
    end
    subgraph Flink[实时处理层]
        F1[流量统计 Flink]
        F2[用户行为分析]
        F3[QoS监控]
        F4[CEP故障检测]
    end
    subgraph AI[AI分析层]
        A1[流量预测]
        A2[异常检测]
        A3[根因定位]
    end
    subgraph Storage[存储层]
        CH[(ClickHouse)]
        ES[(Elasticsearch)]
        R[(Redis)]
    end
    subgraph App[应用层]
        APP1[NOC监控大屏]
        APP2[告警平台]
        APP3[容量规划系统]
    end
    S1 --> L1 --> K0
    S2 --> L1 --> K0
    S3 --> K0
    S4 --> K0
    S5 --> K0
    K0 --> F1 --> CH
    K0 --> F2 --> CH
    K0 --> F3 --> R
    K0 --> F4 --> ES --> APP2
    CH --> A1 & A2 --> APP3
    CH --> APP1
""",
    'code1': {
        'desc':'以下Java代码展示了基于Flink的5G基站流量异常检测作业，使用KeyedProcessFunction维护每个基站的历史流量统计状态，动态检测流量突增和突降：',
        'lang':'java',
        'code':"""import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;
import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics;

public class CellTrafficAnomalyJob {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        DataStream<CellTraffic> trafficStream = env
            .addSource(new KafkaSource<CellTraffic>("network-traffic"))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<CellTraffic>forBoundedOutOfOrderness(Duration.ofSeconds(5))
            );

        DataStream<TrafficAlert> alerts = trafficStream
            .keyBy(CellTraffic::getCellId)
            .process(new TrafficAnomalyFunction());

        alerts.addSink(new AlertSink());
        env.execute("Cell Traffic Anomaly Detection");
    }
}

class TrafficAnomalyFunction extends KeyedProcessFunction<String, CellTraffic, TrafficAlert> {
    private ValueState<DescriptiveStatistics> statsState;
    private static final int HISTORY_WINDOW = 60; // 60分钟历史
    private static final double SPIKE_THRESHOLD = 3.0; // 3倍标准差
    private static final double DROP_THRESHOLD = 0.3; // 降至30%以下

    @Override
    public void open(Configuration parameters) {
        statsState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("trafficStats", DescriptiveStatistics.class));
    }

    @Override
    public void processElement(CellTraffic traffic, Context ctx, Collector<TrafficAlert> out) {
        DescriptiveStatistics stats = statsState.value();
        if (stats == null) {
            stats = new DescriptiveStatistics(HISTORY_WINDOW);
        }

        double current = traffic.getThroughputMbps();
        if (stats.getN() >= 10) {
            double mean = stats.getMean();
            double stdDev = stats.getStandardDeviation();

            if (stdDev > 0 && current > mean + SPIKE_THRESHOLD * stdDev) {
                out.collect(new TrafficAlert(
                    ctx.getCurrentKey(), "TRAFFIC_SPIKE",
                    String.format("Throughput %.0f Mbps (normal: %.0f ± %.0f)", current, mean, stdDev),
                    ctx.timestamp()
                ));
            }
            if (mean > 0 && current < mean * DROP_THRESHOLD) {
                out.collect(new TrafficAlert(
                    ctx.getCurrentKey(), "TRAFFIC_DROP",
                    String.format("Throughput dropped to %.0f Mbps (normal: %.0f)", current, mean),
                    ctx.timestamp()
                ));
            }
        }
        stats.addValue(current);
        statsState.update(stats);
    }
}
"""
    },
    'code2': {
        'desc':'以下Python代码实现了基于Prophet和LSTM的网络流量预测模型，用于预测未来1小时各基站的上下行流量，支撑自动扩容决策：',
        'lang':'python',
        'code':"""import numpy as np
import pandas as pd
from fbprophet import Prophet
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class TrafficForecaster:
    def __init__(self, model_type='hybrid'):
        self.model_type = model_type
        self.prophet = Prophet(yearly_seasonality=False, daily_seasonality=True,
                               hourly_seasonality=True, interval_width=0.95)
        self.lstm = self._build_lstm()

    def _build_lstm(self):
        model = Sequential([
            LSTM(64, input_shape=(24, 1), return_sequences=False),
            Dense(32, activation='relu'),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def train(self, df):
        # df 包含 ds (datetime) 和 y (traffic)
        if self.model_type in ['prophet', 'hybrid']:
            self.prophet.fit(df[['ds', 'y']])
        if self.model_type in ['lstm', 'hybrid']:
            seq, target = self._create_sequences(df['y'].values)
            self.lstm.fit(seq, target, epochs=20, batch_size=32, verbose=0)

    def _create_sequences(self, data, seq_len=24):
        xs, ys = [], []
        for i in range(len(data) - seq_len):
            xs.append(data[i:i+seq_len].reshape(-1, 1))
            ys.append(data[i+seq_len])
        return np.array(xs), np.array(ys)

    def predict(self, future_periods=60, freq='min'):
        if self.model_type == 'prophet':
            future = self.prophet.make_future_dataframe(periods=future_periods, freq=freq)
            forecast = self.prophet.predict(future)
            return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(future_periods)
        # hybrid / lstm logic omitted for brevity
        return None

# 使用示例
# df = pd.read_csv('cell_traffic.csv')
# df['ds'] = pd.to_datetime(df['timestamp'])
# df['y'] = df['throughput_mbps']
# forecaster = TrafficForecaster(model_type='prophet')
# forecaster.train(df)
# next_hour = forecaster.predict(future_periods=60, freq='min')
"""
    },
    'code3': """# 电信网络流量实时分析 Flink SQL 配置
execution:
  planner: blink
  type: streaming
  checkpointing:
    mode: EXACTLY_ONCE
    interval: 10000ms
    timeout: 300000ms
    min-pause: 500ms
  restart-strategy:
    type: fixed-delay
    fixed-delay:
      attempts: 10
      delay: 10s
state:
  backend: rocksdb
  checkpoints:
    dir: hdfs:///flink/checkpoints/telecom
  backend.incremental: true
  backend.rocksdb.memory.managed: true
parallelism:
  default: 384
""",
    'results': [
        {'category':'实时性','name':'故障发现时间','before':'30分钟','after':'20秒','delta':'-98.9%'},
        {'category':'定位','name':'故障根因定位时间','before':'2小时','after':'4分钟','delta':'-96.7%'},
        {'category':'体验','name':'网络投诉率','before':'0.8%','after':'0.35%','delta':'-56.3%'},
        {'category':'资源','name':'带宽利用率','before':'60%','after':'82%','delta':'+36.7%'},
        {'category':'预测','name':'流量预测准确率','before':'70%','after':'89%','delta':'+27.1%'},
        {'category':'成本','name':'运维人力成本','before':'基准','after':'-25%','delta':'节省'},
    ]
})

# 9. Petrochemical
case_studies.append({
    'path': 'phase2-case-studies/petrochemical/11.8.1-pipeline-leak.md',
    'title': '石油石化管道泄漏检测深度案例研究',
    'number': '11.8.1',
    'industry': '石油石化',
    'scenario': '油气管道泄漏检测、压力异常预警、安全监控',
    'scale': '管道总长1万公里, 传感器10万+, 日数据量5TB',
    'goals': [
        {'category':'安全','metric':'泄漏发现时间','target':'< 5分钟'},
        {'category':'精度','metric':'泄漏定位精度','target':'< 100米'},
        {'category':'误报','metric':'误报率','target':'< 5%'},
        {'category':'成本','metric':'年度泄漏损失','target':'-70%'},
        {'category':'环保','metric':'环境事故数','target':'0'},
    ],
    'metrics': [
        {'name':'泄漏发现时间','before':'数天','after':'3分钟','delta':'-99.9%'},
        {'name':'泄漏定位精度','before':'公里级','after':'50米','delta':'+95%'},
        {'name':'误报率','before':'20%','after':'4%','delta':'-80%'},
        {'name':'年度泄漏损失','before':'5000万','after':'800万','delta':'-84%'},
        {'name':'环境事故数','before':'3起/年','after':'0起/年','delta':'-100%'},
        {'name':'巡检人力成本','before':'基准','after':'-40%','delta':'节省'},
    ],
    'pain_points': [
        {'title':'管道老化导致泄漏风险高','desc':'某大型国有石油公司运营油气管道总长度超过1万公里，部分管道服役超过20年，受腐蚀、焊缝缺陷、第三方施工破坏等因素影响，泄漏风险逐年上升。单次重大泄漏事故不仅造成数千万的经济损失，还会引发严重的环境污染和社会影响。'},
        {'title':'传统人工巡检周期长、发现滞后','desc':'传统的人工徒步巡检和直升机巡线模式，巡检周期长（通常每周一次），且受天气和地形限制大。很多泄漏点在初期渗流阶段难以被发现，往往要等到形成明显油污或被群众举报后才知晓，错失最佳处置时机。'},
        {'title':'环境干扰导致误报率高','desc':'管道周边存在大量噪声源，如公路车辆通行、铁路振动、农田灌溉、降雨等，这些干扰信号与泄漏特征相似，容易造成监测系统误报。高误报率不仅浪费应急资源，还会导致运维人员对真实告警的麻痹。'},
        {'title':'长距离管道定位困难','desc':'即使检测到泄漏信号，要在长达数百公里的管段上精确确定泄漏点位置也非常困难。传统的基于压力波速的定位方法受管道材质、流体特性、温度等因素影响，定位误差常达数公里，给抢修人员带来极大挑战。'},
    ],
    'tech_stack': [
        {'layer':'感知层','tech':'DAS光纤 + 压力/流量/温度传感器','reason':'全管道覆盖、高灵敏度'},
        {'layer':'边缘层','tech':'防爆边缘网关','reason':'现场预处理、低延迟'},
        {'layer':'消息队列','tech':'Apache Kafka 3.6','reason':'高可靠工业数据传输'},
        {'layer':'流计算引擎','tech':'Apache Flink 1.18','reason':'实时信号处理与模式识别'},
        {'layer':'AI诊断','tech':'Python + CNN + 信号处理','reason':'DAS波形分类与泄漏识别'},
        {'layer':'定位算法','tech':'多传感器融合定位','reason':'高精度泄漏点定位'},
    ],
    'architecture_mermaid': """graph TB
    subgraph Field[现场感知层]
        S1[DAS光纤声波]
        S2[压力传感器]
        S3[流量传感器]
        S4[温度传感器]
        S5[视频监控]
    end
    subgraph Edge[边缘计算层]
        E1[防爆边缘网关]
        E2[信号预处理]
        E3[本地缓存]
    end
    subgraph Kafka[Kafka消息层]
        K1[DAS Topic]
        K2[SCADA Topic]
    end
    subgraph Flink[实时处理层]
        F1[波形特征提取]
        F2[压力突变检测]
        F3[多流关联分析]
    end
    subgraph AI[AI诊断层]
        A1[CNN泄漏识别]
        A2[定位计算]
    end
    subgraph App[应用层]
        APP1[监控中心]
        APP2[应急指挥]
        APP3[数字孪生]
    end
    S1 --> E2 --> K1 --> F1 --> A1
    S2 & S3 & S4 --> E1 --> K2 --> F2 --> F3 --> A2
    S5 --> E1
    A1 & A2 --> APP1 & APP2
    APP1 --> APP3
""",
    'code1': {
        'desc':'以下Java代码展示了基于Flink KeyedProcessFunction的管道压力突降检测，维护每个传感器的历史压力状态，识别异常快速下降模式：',
        'lang':'java',
        'code':"""import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;

public class PipelinePressureMonitor {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        DataStream<PressureReading> pressureStream = env
            .addSource(new KafkaSource<PressureReading>("scada-pressure"))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<PressureReading>forBoundedOutOfOrderness(Duration.ofSeconds(10))
            );

        DataStream<PressureAlert> alerts = pressureStream
            .keyBy(PressureReading::getSensorId)
            .process(new PressureDropDetector());

        alerts.addSink(new EmergencyAlertSink());
        env.execute("Pipeline Pressure Monitor");
    }
}

class PressureDropDetector extends KeyedProcessFunction<String, PressureReading, PressureAlert> {
    private ValueState<Double> lastPressureState;
    private static final double DROP_RATE_THRESHOLD = 0.10; // 10%突降
    private static final int CONSECUTIVE_DROPS = 3;
    private int consecutiveCount = 0;

    @Override
    public void open(Configuration parameters) {
        lastPressureState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("lastPressure", Double.class));
    }

    @Override
    public void processElement(PressureReading reading, Context ctx, Collector<PressureAlert> out) throws Exception {
        Double lastPressure = lastPressureState.value();
        double current = reading.getPressureBar();
        if (lastPressure != null) {
            double dropRate = (lastPressure - current) / lastPressure;
            if (dropRate > DROP_RATE_THRESHOLD) {
                consecutiveCount++;
                if (consecutiveCount >= CONSECUTIVE_DROPS) {
                    out.collect(new PressureAlert(
                        ctx.getCurrentKey(),
                        "CRITICAL",
                        String.format("Pressure dropped %.1f%% consecutively to %.2f bar", dropRate * 100, current),
                        ctx.timestamp()
                    ));
                    consecutiveCount = 0;
                }
            } else {
                consecutiveCount = 0;
            }
        }
        lastPressureState.update(current);
    }
}
"""
    },
    'code2': {
        'desc':'以下Python代码展示了基于卷积神经网络（CNN）的DAS光纤声波信号分类模型，用于区分正常环境噪声与真实的管道泄漏声波特征：',
        'lang':'python',
        'code':"""import torch
import torch.nn as nn
import torch.nn.functional as F

class DASLeakCNN(nn.Module):
    def __init__(self, num_classes=4):
        super(DASLeakCNN, self).__init__()
        # 输入：DAS时频图 [batch, 1, 64, 256]
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.pool1 = nn.MaxPool2d(2, 2)

        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool2 = nn.MaxPool2d(2, 2)

        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.pool3 = nn.MaxPool2d(2, 2)

        self.fc1 = nn.Linear(128 * 8 * 32, 256)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.pool1(F.relu(self.bn1(self.conv1(x))))
        x = self.pool2(F.relu(self.bn2(self.conv2(x))))
        x = self.pool3(F.relu(self.bn3(self.conv3(x))))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)

class DASClassifier:
    def __init__(self, model_path, label_map=None):
        self.model = DASLeakCNN(num_classes=4)
        self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
        self.model.eval()
        self.label_map = label_map or {0: 'NORMAL', 1: 'LEAK', 2: 'CONSTRUCTION', 3: 'TRAFFIC'}

    def classify(self, spectrogram):
        # spectrogram: numpy array [1, 64, 256]
        tensor = torch.tensor(spectrogram, dtype=torch.float).unsqueeze(0)
        with torch.no_grad():
            output = self.model(tensor)
            pred = torch.argmax(output, dim=1).item()
            prob = torch.exp(output)[0][pred].item()
        return {
            "label": self.label_map[pred],
            "confidence": round(prob, 4),
            "alert": self.label_map[pred] == "LEAK" and prob > 0.85
        }
"""
    },
    'code3': """# 管道泄漏监测告警配置
alert:
  levels:
    - name: "INFO"
      conditions:
        - sensor: "DAS"
          label: "CONSTRUCTION"
          confidence_min: 0.7
    - name: "WARNING"
      conditions:
        - sensor: "DAS"
          label: "LEAK"
          confidence_min: 0.5
        - sensor: "PRESSURE"
          drop_rate: 0.05
          consecutive: 2
    - name: "CRITICAL"
      conditions:
        - sensor: "DAS"
          label: "LEAK"
          confidence_min: 0.85
        - sensor: "PRESSURE"
          drop_rate: 0.10
          consecutive: 3
  escalation:
    critical:
      - sms: "调度中心"
      - phone: "应急指挥长"
      - wechat: "抢修班组"
    auto_action:
      - close_valve: "上游最近的截断阀"
      - notify: "地方政府应急办"
""",
    'results': [
        {'category':'安全','name':'泄漏发现时间','before':'数天','after':'3分钟','delta':'-99.9%'},
        {'category':'精度','name':'泄漏定位精度','before':'公里级','after':'50米','delta':'+95%'},
        {'category':'误报','name':'误报率','before':'20%','after':'4%','delta':'-80%'},
        {'category':'经济','name':'年度泄漏损失','before':'5000万','after':'800万','delta':'-84%'},
        {'category':'环保','name':'环境事故数','before':'3起/年','after':'0起/年','delta':'-100%'},
        {'category':'效率','name':'巡检人力成本','before':'基准','after':'-40%','delta':'节省'},
    ]
})

# 10. Autonomous Driving
case_studies.append({
    'path': 'phase2-case-studies/autonomous-driving/11.6.1-sensor-fusion.md',
    'title': '自动驾驶传感器融合深度案例研究',
    'number': '11.6.1',
    'industry': '自动驾驶/智能汽车',
    'scenario': '多传感器数据融合、实时障碍物检测、路径规划',
    'scale': '单车100+传感器, 感知-决策延迟<50ms, 日测试里程100万公里',
    'goals': [
        {'category':'延迟','metric':'端到端感知延迟','target':'P99 < 50ms'},
        {'category':'准确率','metric':'目标检测准确率','target':'> 99.9%'},
        {'category':'安全','metric':'功能安全等级','target':'ASIL-D'},
        {'category':'同步','metric':'多传感器时间同步精度','target':'< 1μs'},
        {'category':'规模','metric':'日处理传感器数据','target':'10PB'},
    ],
    'metrics': [
        {'name':'端到端感知延迟','before':'150ms','after':'42ms','delta':'-72%'},
        {'name':'目标检测准确率','before':'95%','after':'99.95%','delta':'+5.2%'},
        {'name':'多目标跟踪准确率','before':'90%','after':'98.5%','delta':'+9.4%'},
        {'name':'时间同步精度','before':'5ms','after':'0.5μs','delta':'+10000x'},
        {'name':'系统可用性','before':'99.9%','after':'99.999%','delta':'+0.099%'},
        {'name':'日均测试里程','before':'10万km','after':'150万km','delta':'+1400%'},
    ],
    'pain_points': [
        {'title':'超低延迟与高精度感知的矛盾','desc':'自动驾驶车辆搭载激光雷达、摄像头、毫米波雷达等多种传感器，单车原始数据量高达10GB/s。要在100毫秒内完成数据采集、融合、感知、预测和路径规划，对计算平台的吞吐量和延迟提出了极致要求。'},
        {'title':'多传感器时间同步精度不足','desc':'不同传感器的采样频率和数据传输路径各异，如果融合时存在毫秒级的时间偏差，快速运动的车辆、行人位置可能出现数米的误差，导致错误的避障决策，危及行车安全。'},
        {'title':'传感器数据质量问题','desc':'恶劣天气（雨、雪、雾、强光）会导致摄像头图像模糊、激光雷达点云噪声增加；复杂城市环境中存在大量遮挡、反射和相似物体干扰，给目标检测和分类带来巨大挑战。'},
        {'title':'功能安全与系统可靠性','desc':'自动驾驶系统属于最高安全等级（ASIL-D），任何单点故障都可能导致灾难性后果。系统必须具备完善的冗余设计、故障检测、降级策略和实时监控能力。'},
    ],
    'tech_stack': [
        {'layer':'传感器层','tech':'LiDAR + Camera + Radar + IMU/GNSS','reason':'多模态感知冗余'},
        {'layer':'同步层','tech':'PTP/gPTP时间同步 + 硬件触发','reason':'微秒级时间对齐'},
        {'layer':'中间件','tech':'ROS2 + DDS + Flink','reason':'实时数据分发与流处理'},
        {'layer':'感知融合','tech':'Python + PyTorch + CUDA','reason':'深度学习模型推理'},
        {'layer':'规划控制','tech':'C++ + Apollo/自研算法','reason':'毫秒级路径规划'},
        {'layer':'数据闭环','tech':'数据湖 + 自动标注','reason':'模型持续迭代优化'},
    ],
    'architecture_mermaid': """graph TB
    subgraph Sensors[传感器层]
        L1[激光雷达<br/>10Hz/128线]
        C1[摄像头<br/>30Hz/8MP]
        R1[毫米波雷达<br/>20Hz]
        G1[GNSS+IMU<br/>100Hz]
    end
    subgraph Sync[同步层]
        T1[PTP主时钟]
        B1[时间对齐缓冲]
    end
    subgraph Compute[计算层]
        P1[点云预处理]
        P2[图像预处理]
        F1[多传感器融合]
        F2[目标跟踪]
    end
    subgraph Decision[决策层]
        D1[行为预测]
        D2[路径规划]
        D3[车辆控制]
    end
    L1 --> T1 --> B1 --> P1 --> F1
    C1 --> T1 --> B1 --> P2 --> F1
    R1 --> T1 --> B1 --> F1
    G1 --> T1 --> B1 --> F1
    F1 --> F2 --> D1 --> D2 --> D3
""",
    'code1': {
        'desc':'以下Java代码展示了基于Flink Interval Join的多传感器时间同步与融合，将激光雷达、摄像头和毫米波雷达的数据流按时间窗口进行精确对齐：',
        'lang':'java',
        'code':"""import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.time.Time;

public class SensorFusionJob {

    private static final long SYNC_WINDOW_MS = 20; // 20ms同步窗口

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<LidarFrame> lidarStream = env
            .addSource(new LidarSource())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<LidarFrame>forBoundedOutOfOrderness(Duration.ofMillis(5))
                    .withTimestampAssigner((event, ts) -> event.getTimestampMicros() / 1000)
            );

        DataStream<CameraFrame> cameraStream = env
            .addSource(new CameraSource())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<CameraFrame>forBoundedOutOfOrderness(Duration.ofMillis(5))
                    .withTimestampAssigner((event, ts) -> event.getTimestampMicros() / 1000)
            );

        DataStream<RadarFrame> radarStream = env
            .addSource(new RadarSource())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<RadarFrame>forBoundedOutOfOrderness(Duration.ofMillis(5))
                    .withTimestampAssigner((event, ts) -> event.getTimestampMicros() / 1000)
            );

        // LiDAR与Camera同步
        DataStream<FusedPerception> lidarCameraFused = lidarStream
            .keyBy(LidarFrame::getVehicleId)
            .intervalJoin(cameraStream.keyBy(CameraFrame::getVehicleId))
            .between(Time.milliseconds(-SYNC_WINDOW_MS), Time.milliseconds(SYNC_WINDOW_MS))
            .process(new LidarCameraFusionFunction());

        // 加入Radar进行三模态融合
        DataStream<FusedPerception> multiModalFused = lidarCameraFused
            .keyBy(FusedPerception::getVehicleId)
            .intervalJoin(radarStream.keyBy(RadarFrame::getVehicleId))
            .between(Time.milliseconds(-SYNC_WINDOW_MS), Time.milliseconds(SYNC_WINDOW_MS))
            .process(new MultiModalFusionFunction());

        multiModalFused
            .map(new PerceptionPostProcess())
            .addSink(new PlanningServiceSink());

        env.execute("Autonomous Driving Sensor Fusion");
    }
}
"""
    },
    'code2': {
        'desc':'以下Python代码实现了基于匈牙利算法的多目标跟踪（MOT）与传感器融合后处理，将激光雷达检测框、摄像头检测框和雷达点迹进行关联匹配，输出稳定跟踪目标列表：',
        'lang':'python',
        'code':"""import numpy as np
from scipy.optimize import linear_sum_assignment

class SensorFusionTracker:
    def __init__(self, iou_threshold=0.3, max_lost=5):
        self.iou_threshold = iou_threshold
        self.max_lost = max_lost
        self.trackers = {}  # track_id -> {'kf': KalmanFilter, 'lost': int}
        self.next_id = 0

    def update(self, lidar_dets, camera_dets, radar_dets):
        # 1. 将三种传感器的检测结果统一到世界坐标系下
        all_dets = self._project_to_world(lidar_dets, camera_dets, radar_dets)

        # 2. 预测已有跟踪器位置
        predictions = {}
        for track_id, tracker in self.trackers.items():
            predictions[track_id] = tracker['kf'].predict()

        # 3. 匹配检测与预测
        matches, unmatched_dets, unmatched_tracks = self._associate(all_dets, predictions)

        # 4. 更新匹配的目标
        for det_idx, track_id in matches:
            self.trackers[track_id]['kf'].update(all_dets[det_idx])
            self.trackers[track_id]['lost'] = 0

        # 5. 创建新跟踪器
        for det_idx in unmatched_dets:
            self.trackers[self.next_id] = {
                'kf': KalmanFilter(all_dets[det_idx]),
                'lost': 0
            }
            self.next_id += 1

        # 6. 删除长期丢失的目标
        for track_id in list(unmatched_tracks):
            self.trackers[track_id]['lost'] += 1
            if self.trackers[track_id]['lost'] > self.max_lost:
                del self.trackers[track_id]

        return self._get_tracks()

    def _associate(self, detections, predictions):
        if len(detections) == 0 or len(predictions) == 0:
            return [], list(range(len(detections))), list(predictions.keys())

        cost_matrix = np.zeros((len(detections), len(predictions)))
        pred_ids = list(predictions.keys())
        for i, det in enumerate(detections):
            for j, track_id in enumerate(pred_ids):
                cost_matrix[i, j] = 1 - self._iou(det['bbox'], predictions[track_id]['bbox'])

        det_indices, pred_indices = linear_sum_assignment(cost_matrix)
        matches = []
        for d, p in zip(det_indices, pred_indices):
            if cost_matrix[d, p] < (1 - self.iou_threshold):
                matches.append((d, pred_ids[p]))

        matched_dets = set(d for d, _ in matches)
        matched_tracks = set(t for _, t in matches)
        unmatched_dets = list(set(range(len(detections))) - matched_dets)
        unmatched_tracks = list(set(pred_ids) - matched_tracks)
        return matches, unmatched_dets, unmatched_tracks

    def _iou(self, boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        interArea = max(0, xB - xA) * max(0, yB - yA)
        boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
        return interArea / float(boxAArea + boxBArea - interArea + 1e-6)

    def _project_to_world(self, lidar_dets, camera_dets, radar_dets):
        # 简化：假设已完成外参标定，直接合并
        return lidar_dets + camera_dets + radar_dets

    def _get_tracks(self):
        return [{"id": tid, "state": t['kf'].get_state()} for tid, t in self.trackers.items()]
"""
    },
    'code3': """# 自动驾驶感知融合系统 DDS 配置
ros2:
  qos:
    sensor_data:
      reliability: best_effort
      history: keep_last
      depth: 10
      deadline: 50ms
      lifespan: 100ms
    perception_output:
      reliability: reliable
      history: keep_last
      depth: 5
      deadline: 20ms
  nodes:
    - name: "lidar_preprocessor"
      topic: "/sensors/lidar/points"
      qos_profile: "sensor_data"
    - name: "camera_preprocessor"
      topic: "/sensors/camera/image"
      qos_profile: "sensor_data"
    - name: "fusion_engine"
      subscriptions:
        - "/sensors/lidar/points"
        - "/sensors/camera/image"
        - "/sensors/radar/targets"
      publisher: "/perception/fused_objects"
      qos_profile: "perception_output"
""",
    'results': [
        {'category':'延迟','name':'端到端感知延迟','before':'150ms','after':'42ms','delta':'-72%'},
        {'category':'准确率','name':'目标检测准确率','before':'95%','after':'99.95%','delta':'+5.2%'},
        {'category':'跟踪','name':'多目标跟踪准确率','before':'90%','after':'98.5%','delta':'+9.4%'},
        {'category':'同步','name':'时间同步精度','before':'5ms','after':'0.5μs','delta':'+10000x'},
        {'category':'可靠','name':'系统可用性','before':'99.9%','after':'99.999%','delta':'+0.099%'},
        {'category':'规模','name':'日均测试里程','before':'10万km','after':'150万km','delta':'+1400%'},
    ]
})

# 11. Aerospace
case_studies.append({
    'path': 'phase2-case-studies/aerospace/11.7.1-flight-data.md',
    'title': '航空航天飞行数据监控深度案例研究',
    'number': '11.7.1',
    'industry': '航空航天',
    'scenario': '飞行数据实时监控、发动机健康监测、预测性维护',
    'scale': '运营飞机1000+, 日均航班5000+, 每架飞机10万+参数',
    'goals': [
        {'category':'可用性','metric':'非计划停机时间','target':'-35%'},
        {'category':'安全','metric':'飞行中重大故障发现时间','target':'实时'},
        {'category':'成本','metric':'年度维护成本','target':'-20%'},
        {'category':'合规','metric':'飞行数据留存完整性','target':'100%'},
        {'category':'预测','metric':'发动机RUL预测准确率','target':'> 85%'},
    ],
    'metrics': [
        {'name':'非计划停机时间','before':'5.0%/年','after':'3.1%/年','delta':'-38%'},
        {'name':'飞行中故障实时发现','before':'飞行后','after':'实时','delta':'质变'},
        {'name':'年度维护成本','before':'基准','after':'-22%','delta':'节省'},
        {'name':'发动机RUL预测准确率','before':'72%','after':'88%','delta':'+22.2%'},
        {'name':'航班延误率（技术原因）','before':'3.5%','after':'1.8%','delta':'-48.6%'},
        {'name':'AOG（停场）次数','before':'120次/年','after':'65次/年','delta':'-45.8%'},
    ],
    'pain_points': [
        {'title':'海量飞行参数实时处理难度大','desc':'某大型航空公司运营超过1000架民航客机，每架飞机每秒产生1000+飞行参数，涵盖发动机、航电、液压、环控等数十个系统。传统的QAR（快速存取记录器）数据在航班落地后通过人工拷贝或卫星回传，分析滞后，无法实现飞行中的实时监控。'},
        {'title':'发动机健康状态难以精准评估','desc':'航空发动机是飞机最核心、最昂贵的部件，其健康状态直接影响飞行安全和运营成本。传统的维护计划基于飞行小时和循环数，缺乏对发动机实际退化状态的精准评估，导致维护不足或过度维护并存。'},
        {'title':'飞行中突发故障响应不及时','desc':'在长途国际航班或跨洋飞行中，如果发动机或关键系统在空中出现异常，机组人员往往只能依赖机载告警系统的有限信息做出判断。地面工程师无法实时掌握飞机状态，难以及时提供决策支持。'},
        {'title':'数据格式多样、标准化困难','desc':'不同机型（如A320、B787、A350）的飞行数据采集标准不同，ARINC 429、ARINC 664、AFDX等多种总线协议并存。数据解析和标准化工作量大，给统一的数据平台建设带来了巨大挑战。'},
    ],
    'tech_stack': [
        {'layer':'机载采集','tech':'QAR + ACARS + SATCOM','reason':'飞行数据记录与空地传输'},
        {'layer':'数据解析','tech':'ARINC 429/664解析引擎','reason':'多协议飞行参数解析'},
        {'layer':'消息队列','tech':'Apache Kafka 3.6','reason':'高可靠飞行数据总线'},
        {'layer':'流计算引擎','tech':'Apache Flink 1.18','reason':'实时参数监控与事件检测'},
        {'layer':'时序数据库','tech':'TDengine','reason':'海量飞行时序数据存储'},
        {'layer':'AI预测','tech':'Python + LSTM + 物理模型','reason':'发动机健康预测与RUL估计'},
    ],
    'architecture_mermaid': """graph TB
    subgraph Aircraft[飞机端]
        Q1[QAR记录器]
        A1[ACARS数据链]
        S1[卫星通信<br/>SATCOM]
    end
    subgraph Ground[地面接入层]
        G1[ACARS地面站]
        G2[卫星地面站]
        G3[数据解析网关]
    end
    subgraph Kafka[Kafka消息层]
        K1[飞行参数Topic]
        K2[告警事件Topic]
    end
    subgraph Flink[实时计算层]
        F1[参数解码]
        F2[发动机健康监测]
        F3[超限告警检测]
        F4[飞行事件识别]
    end
    subgraph Storage[存储层]
        DB1[(TDengine<br/>时序数据)]
        DB2[(PostgreSQL<br/>航班元数据)]
    end
    subgraph AI[AI分析层]
        AI1[异常检测]
        AI2[RUL预测]
        AI3[故障诊断]
    end
    subgraph App[应用层]
        APP1[MCC监控大屏]
        APP2[维护决策系统]
        APP3[飞行品质分析]
    end
    Q1 --> S1 --> G2 --> G3 --> K1
    A1 --> G1 --> G3 --> K1
    K1 --> F1 --> F2 & F3 & F4 --> DB1
    DB1 --> AI1 & AI2 & AI3 --> APP2
    DB1 --> APP1 & APP3
    DB2 --> APP1
""",
    'code1': {
        'desc':'以下Java代码展示了基于Flink的飞行发动机健康实时监测作业，从ACARS数据流中解析发动机参数，使用滚动窗口计算EGT裕度、N1振动等关键健康指标：',
        'lang':'java',
        'code':"""import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

public class EngineHealthMonitorJob {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<AcarsMessage> acarsStream = env
            .addSource(new KafkaSource<AcarsMessage>("acars-messages"))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<AcarsMessage>forBoundedOutOfOrderness(Duration.ofSeconds(30))
                    .withTimestampAssigner((msg, ts) -> msg.getTimestamp())
            );

        // 解析ARINC参数
        DataStream<FlightParameter> paramStream = acarsStream
            .flatMap(new FlatMapFunction<AcarsMessage, FlightParameter>() {
                @Override
                public void flatMap(AcarsMessage msg, Collector<FlightParameter> out) {
                    List<FlightParameter> params = ArincParser.parse(msg.getPayload());
                    for (FlightParameter p : params) {
                        out.collect(p);
                    }
                }
            });

        // 发动机EGT温度监测
        DataStream<EngineHealth> egtHealth = paramStream
            .filter(p -> "EGT".equals(p.getParameterCode()) && "ENGINE".equals(p.getSystemCode()))
            .keyBy(p -> p.getEngineId())
            .window(TumblingEventTimeWindows.of(Time.minutes(1)))
            .aggregate(new EgtAggregateFunction(), new EngineHealthProcessFunction("EGT_MARGIN"));

        // N1振动监测
        DataStream<EngineHealth> n1Vibration = paramStream
            .filter(p -> "N1VIB".equals(p.getParameterCode()))
            .keyBy(p -> p.getEngineId())
            .window(TumblingEventTimeWindows.of(Time.minutes(1)))
            .aggregate(new VibrationAggregateFunction(), new EngineHealthProcessFunction("N1_VIBRATION"));

        egtHealth.addSink(new TDengineSink<>("engine_health"));
        n1Vibration.addSink(new TDengineSink<>("engine_health"));

        env.execute("Engine Health Monitor");
    }
}

class EgtAggregateFunction implements AggregateFunction<FlightParameter, EgtAccumulator, EgtStats> {
    @Override
    public EgtAccumulator createAccumulator() { return new EgtAccumulator(); }
    @Override
    public EgtAccumulator add(FlightParameter value, EgtAccumulator accumulator) {
        accumulator.add(value.getNumericValue());
        return accumulator;
    }
    @Override
    public EgtStats getResult(EgtAccumulator accumulator) {
        return accumulator.toStats();
    }
    @Override
    public EgtAccumulator merge(EgtAccumulator a, EgtAccumulator b) {
        a.merge(b); return a;
    }
}
"""
    },
    'code2': {
        'desc':'以下Python代码实现了基于LSTM和物理退化模型的航空发动机剩余使用寿命（RUL）预测模型，结合飞行循环数据和多传感器时序特征进行精准预测：',
        'lang':'python',
        'code':"""import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

class AeroEngineRULPredictor:
    def __init__(self, sequence_length=50, n_features=14):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential([
            LSTM(100, return_sequences=True, input_shape=(self.sequence_length, self.n_features)),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25, activation='relu'),
            Dense(1, activation='linear')  # 输出剩余飞行循环数
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

    def prepare_data(self, flight_cycles):
        # flight_cycles: DataFrame，每行为一个飞行循环的参数
        # 特征包括：T24, T30, T50, P30, Nf, Nc, epr, Ps30, phi, NRf, NRc, BPR, htBleed, W31
        features = flight_cycles[[
            'T24', 'T30', 'T50', 'P30', 'Nf', 'Nc', 'epr',
            'Ps30', 'phi', 'NRf', 'NRc', 'BPR', 'htBleed', 'W31'
        ]].values
        # 归一化
        self.feature_min = features.min(axis=0)
        self.feature_max = features.max(axis=0)
        scaled = (features - self.feature_min) / (self.feature_max - self.feature_min + 1e-8)

        X, y = [], []
        max_rul = 130  # 假设最大RUL为130个循环
        for i in range(len(scaled) - self.sequence_length):
            X.append(scaled[i:i+self.sequence_length])
            # RUL标签：分段线性衰减（前段保持恒定，后段线性下降）
            rul = max_rul - (i + self.sequence_length)
            y.append(max(rul, 0))
        return np.array(X), np.array(y)

    def train(self, X, y, epochs=50, batch_size=32):
        early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size, validation_split=0.2, callbacks=[early_stop])

    def predict_rul(self, recent_cycles):
        scaled = (recent_cycles - self.feature_min) / (self.feature_max - self.feature_min + 1e-8)
        pred = self.model.predict(scaled.reshape(1, self.sequence_length, self.n_features))[0][0]
        return {"predicted_rul_cycles": round(float(pred), 1), "alert": pred < 30}

# 使用示例
# predictor = AeroEngineRULPredictor()
# X_train, y_train = predictor.prepare_data(engine_df)
# predictor.train(X_train, y_train)
# rul = predictor.predict_rul(last_50_cycles)
"""
    },
    'code3': """# 飞行数据实时监控 Flink 配置
execution:
  planner: blink
  type: streaming
  checkpointing:
    mode: EXACTLY_ONCE
    interval: 60000ms
    timeout: 600000ms
    min-pause: 1000ms
    max-concurrent: 1
  restart-strategy:
    type: fixed-delay
    fixed-delay:
      attempts: 5
      delay: 60s
state:
  backend: rocksdb
  checkpoints:
    dir: hdfs:///flink/checkpoints/aerospace
  backend.incremental: true
  backend.rocksdb.memory.managed: true
parallelism:
  default: 192
""",
    'results': [
        {'category':'可用性','name':'非计划停机时间','before':'5.0%/年','after':'3.1%/年','delta':'-38%'},
        {'category':'安全','name':'飞行中故障实时发现','before':'飞行后','after':'实时','delta':'质变'},
        {'category':'成本','name':'年度维护成本','before':'基准','after':'-22%','delta':'节省'},
        {'category':'预测','name':'发动机RUL预测准确率','before':'72%','after':'88%','delta':'+22.2%'},
        {'category':'运营','name':'航班延误率（技术原因）','before':'3.5%','after':'1.8%','delta':'-48.6%'},
        {'category':'维护','name':'AOG（停场）次数','before':'120次/年','after':'65次/年','delta':'-45.8%'},
    ]
})

# Write all files
for cs in case_studies:
    content = generate(
        title=cs['title'],
        number=cs['number'],
        industry=cs['industry'],
        scenario=cs['scenario'],
        scale=cs['scale'],
        goals=cs['goals'],
        metrics=cs['metrics'],
        pain_points=cs['pain_points'],
        tech_stack=cs['tech_stack'],
        architecture_mermaid=cs['architecture_mermaid'],
        code1=cs['code1'],
        code2=cs['code2'],
        code3=cs['code3'],
        results=cs['results']
    )
    os.makedirs(os.path.dirname(cs['path']), exist_ok=True)
    with open(cs['path'], 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Written {cs['path']} ({len(content.encode('utf-8'))} bytes)")

print("All case studies generated successfully.")
