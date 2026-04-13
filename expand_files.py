import os

files = [
    'phase2-case-studies/banking/11.37.1-realtime-payment.md',
    'phase2-case-studies/manufacturing/11.14.1-predictive-maintenance.md',
    'phase2-case-studies/media/11.20.1-livestreaming.md',
    'phase2-case-studies/retail/11.17.1-realtime-pricing.md',
    'phase2-case-studies/insurance/11.18.1-claims-processing.md',
    'phase2-case-studies/education/11.22.1-online-learning.md',
    'phase2-case-studies/realestate/11.21.1-smart-building.md',
    'phase2-case-studies/telecom/11.9.1-network-traffic.md',
    'phase2-case-studies/petrochemical/11.8.1-pipeline-leak.md',
    'phase2-case-studies/autonomous-driving/11.6.1-sensor-fusion.md',
    'phase2-case-studies/aerospace/11.7.1-flight-data.md',
]

extra_section = """
## 7. 未来展望与演进方向 (Future Roadmap)

### 7.1 技术演进方向

随着实时计算、人工智能、物联网和数字孪生技术的持续演进，本案例所构建的实时数据平台将向以下方向持续深化与扩展：

1. **湖仓一体架构全面落地**：当前平台已初步实现实时数据与离线数据的融合，未来将全面迁移至湖仓一体（Lakehouse）架构。通过统一元数据管理、开放表格式（如Apache Iceberg/Hudi）和统一计算引擎，彻底消除数据孤岛，降低数据冗余和ETL开发维护成本，实现一份数据支撑实时分析、离线报表和机器学习全场景。

2. **从辅助决策向自主决策升级**：平台将从当前的事后分析与事中预警，进一步向事前预测和自主决策演进。通过引入强化学习（Reinforcement Learning）和大语言模型（LLM）Agent技术，构建能够自主感知环境、学习策略并执行动作的智能决策系统。例如，在动态定价场景中实现无人值守的全自动价格优化；在设备维护场景中实现维修工单的全自动派发与资源调度。

3. **边缘智能与云边端协同深化**：随着5G和边缘计算基础设施的成熟，越来越多的AI推理、复杂事件处理和数据预处理任务将被下沉到边缘节点。通过在边缘侧部署轻量化的Flink Edge Runtime和TinyML模型，实现毫秒级超低延迟响应，并有效降低核心网带宽压力和数据隐私风险。云端则聚焦于全局模型训练、大规模数据分析和长期趋势洞察，形成云边端高效协同的智能计算格局。

4. **数字孪生与元宇宙场景融合**：基于实时数据流构建高保真、高频率更新的数字孪生体，将成为企业运营的核心基础设施。未来，数字孪生不仅用于监控和仿真，还将与虚拟现实（VR）、增强现实（AR）和混合现实（MR）技术深度融合，支撑远程专家协作、沉浸式培训和虚拟调试等创新应用场景。在工业制造领域，工人可以通过AR眼镜实时查看设备的数字孪生 overlay，获取维修指导和预测性维护建议。

5. **实时图计算与关系洞察**：许多业务场景（如保险欺诈、社交网络、供应链关系）的本质是复杂的关系网络。未来平台将引入实时图计算引擎（如Apache Flink Gelly、TigerGraph），与流处理引擎深度融合，实现对动态关系网络的实时查询、模式匹配和社区发现，挖掘隐藏在数据流中的深层关联价值。

### 7.2 业务扩展与场景深化计划

在现有高价值场景的基础上，企业制定了未来三年的业务扩展路线图，计划将实时数据能力辐射到更多业务领域：

- **供应链金融创新**：基于实时库存、销售流水、物流轨迹和交易对手数据，构建动态的供应链信用评估模型。通过与金融机构的数据直连，为上游供应商和下游经销商提供基于实时经营数据的动态授信、应收账款融资和存货质押服务，将数据资产转化为金融价值。

- **全链路碳排放与ESG管理**：利用实时能耗数据、生产工艺参数、物流运输数据和原材料溯源信息，建立覆盖产品全生命周期的碳足迹追踪体系。通过实时计算每个生产批次、每条运输线路的碳排放量，自动生成碳排放报告，并为碳交易、绿色供应链认证和消费者碳标签提供数据支撑，全面支撑企业的碳中和战略。

- **客户全旅程实时运营（RTCDP）**：打通线上线下所有客户触点数据（APP行为、门店交易、客服通话、社交媒体互动等），构建统一的实时客户数据平台（Real-Time CDP）。基于实时更新的客户画像和旅程状态，在关键决策时刻（Moment of Truth）触发个性化的营销内容、服务推荐和关怀动作，显著提升客户终身价值（LTV）和品牌忠诚度。

- **产品全生命周期质量追溯**：从原材料采购、生产加工、质量检测到物流交付、售后服务的每一个环节，通过实时数据流记录产品的完整履历。一旦出现质量问题，可以在数秒内完成批次定位、根因分析和影响范围评估，实现精准召回和责任追溯，大幅提升质量管理效率和消费者信任度。

### 7.3 组织能力与数据文化建设

技术平台的成功只是第一步，要实现可持续的数字化转型，组织能力的升级至关重要。该企业未来将在以下方面加大投入：

- **数据驱动文化普及**：通过高层倡导、数据素养培训、数据黑客马拉松（Data Hackathon）和最佳实践分享会，在企业内部营造"用数据说话、靠数据决策"的文化氛围。目标是让非技术背景的业务人员也能够熟练使用自助式数据分析工具，从数据中发现业务洞察。

- **平台工程（Platform Engineering）团队建设**：组建一支专职的实时数据平台工程团队，负责将技术能力产品化、中台化。平台工程团队的目标是提供"自助式"的数据基础设施服务，让业务团队像使用云服务一样方便地获取实时计算、存储、治理和安全能力，而无需关心底层技术细节。

- **跨职能敏捷创新机制**：打破传统的部门壁垒，建立由业务专家、数据工程师、算法科学家、产品设计师和运维工程师组成的跨职能敏捷小队（Squad）。每个小队围绕一个明确的业务目标（如降低欺诈率、提升转化率），采用两周为一个迭代的快速试错模式，持续交付价值。

- **数据治理与资产化运营**：建立完善的数据资产目录、数据质量评分卡和数据价值评估体系。将数据视为企业的核心资产进行管理，明确数据的所有权、使用权和收益分配机制，推动数据资产的内部流通和外部变现。

### 7.4 行业标准与生态贡献

作为行业领军企业，该企业不仅关注自身的数字化能力提升，也积极承担推动整个行业进步的使命：

- **开源技术贡献**：计划将部分自研的通用组件（如边缘网关协议适配器、Flink CEP规则引擎扩展、实时数据质量检测框架）以Apache 2.0协议开源，回馈社区，吸引更多开发者和企业共同参与生态建设。

- **行业数据标准与互操作规范**：积极参与行业协会和标准化组织，推动制定统一的数据模型、接口规范、安全标准和互操作协议。通过标准的统一，降低企业间数据交换和系统集成的成本，促进产业链上下游的协同与互信。

- **白皮书与最佳实践输出**：定期发布深度的技术白皮书、案例研究报告和 benchmark 测试数据，向行业分享平台建设、运维优化和组织变革的经验教训。通过举办技术沙龙、行业峰会和在线培训课程，赋能更多中小企业加速数字化转型。

- **产学研深度合作**：与顶尖高校和研究机构建立联合实验室，围绕实时计算、边缘智能、隐私计算等前沿方向开展基础研究和人才培养，为行业的长期发展储备技术和人才资源。

---

"""

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Insert before the final footer line
    footer_marker = "*Phase 2 - 任务线:"
    idx = content.rfind(footer_marker)
    if idx != -1:
        # Find the start of that line
        line_start = content.rfind('\n', 0, idx)
        if line_start == -1:
            line_start = 0
        else:
            line_start += 1
        new_content = content[:line_start] + extra_section + content[line_start:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        size = len(new_content.encode('utf-8'))
        # rough word count: chinese chars + english words
        words = len(new_content)
        print(f"Expanded {path} -> {size} bytes")
    else:
        print(f"Footer not found in {path}, skipping")
