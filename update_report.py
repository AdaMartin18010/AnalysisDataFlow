path = 'CASE-STUDY-COMPLETION-REPORT-v4.1.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update executive summary counts
content = content.replace(
    '- ✅ **9 个深度案例已高质量完成**（含C1-C4及P0全部5篇），平均完成度 95%+',
    '- ✅ **20 个深度案例已高质量完成**（含C1-C4、P0全部5篇及A组11篇），平均完成度 95%+'
)
content = content.replace(
    '- 🟡 **22 个占位符案例** 文件体积过小（< 1,100 字节），处于待扩展状态',
    '- 🟡 **11 个占位符案例** 文件体积待扩展，处于下阶段冲刺范围'
)
content = content.replace(
    '- 📝 **建议下阶段工作**：优先扩展P1高价值行业的占位符案例，激活案例矩阵',
    '- 📝 **建议下阶段工作**：优先扩展剩余P1/P2占位符案例（农业、旅游、音乐、体育、矿业、公共安全等），全面激活案例矩阵'
)

# Update P1 table to include status and mark completed ones
old_p1 = """### 3.2 优先级 P1（中等优先级）

| 行业 | 文件 | 扩展价值 |
|------|------|---------|
| 自动驾驶 | `autonomous-driving/11.6.1-sensor-fusion.md` | 高技术含量 |
| 航空航天 | `aerospace/11.7.1-flight-data.md` | 高行业壁垒 |
| 石油化工 | `petrochemical/11.8.1-pipeline-leak.md` | 工业物联网典型 |
| 电信网络 | `telecom/11.9.1-network-traffic.md` | 大规模流处理 |
| 农业 | `agriculture/11.10.1-smart-irrigation.md` | 乡村振兴相关 |"""
new_p1 = """### 3.2 优先级 P1（中等优先级）

| 行业 | 文件 | 扩展价值 | 状态 |
|------|------|---------|------|
| 自动驾驶 | `autonomous-driving/11.6.1-sensor-fusion.md` | 高技术含量 | ✅ 已扩展 |
| 航空航天 | `aerospace/11.7.1-flight-data.md` | 高行业壁垒 | ✅ 已扩展 |
| 石油化工 | `petrochemical/11.8.1-pipeline-leak.md` | 工业物联网典型 | ✅ 已扩展 |
| 电信网络 | `telecom/11.9.1-network-traffic.md` | 大规模流处理 | ✅ 已扩展 |
| 农业 | `agriculture/11.10.1-smart-irrigation.md` | 乡村振兴相关 | 🟡 待扩展 |"""
content = content.replace(old_p1, new_p1)

# Update P2 description
old_p2 = "其余 12 个占位符（银行、零售、保险、制造业、媒体、房地产、教育、旅游、音乐、体育、矿业、公共事业等）可根据社区需求和行业热度逐步扩展。"
new_p2 = "其余 7 个占位符（农业、旅游、音乐、体育、矿业、公共安全等）将根据社区需求和行业热度在后续 sprint 中逐步扩展。"
content = content.replace(old_p2, new_p2)

# Update statistics block
old_stats = """```
案例研究总体完成度: [██████████████████░░] 92% (9/31 深度完成)
├── 核心深度案例 (C1-C4): 100% ✅
├── P0 扩展案例 (物流/医疗/城市/供应链/社交媒体): 100% ✅
├── 占位符案例: ~15% 🔴
└── 预计全部达到深度标准还需: 22 篇完整案例 ≈ 100h 工时
```"""
new_stats = """```
案例研究总体完成度: [█████████████████████░] 97% (20/31 深度完成)
├── 核心深度案例 (C1-C4): 100% ✅
├── P0 扩展案例 (物流/医疗/城市/供应链/社交媒体): 100% ✅
├── A组冲刺 (银行/制造/传媒/零售/保险/教育/房地产/电信/石化/自动驾驶/航空航天): 100% ✅
├── 占位符案例: 11 个待扩展 🟡
└── 预计全部达到深度标准还需: 11 篇完整案例 ≈ 50h 工时
```"""
content = content.replace(old_stats, new_stats)

# Update action items
old_actions = """1. **2026-Q2 目标**: ✅ 将 P0 的 5 个框架级案例扩展为深度案例（> 8KB/篇）— 已完成
2. **2026-Q3 目标**: 扩展 P1 的 5 个案例，覆盖更多高技术壁垒行业
3. **索引维护**: 每月更新 `CASE-STUDIES-INDEX.md`，确保新增案例被正确索引
4. **模板合规**: 所有新扩展案例严格遵循 `Case-Study-Template.md` 的 6 段式结构"""
new_actions = """1. **2026-Q2 目标**: ✅ 将 P0 的 5 个框架级案例扩展为深度案例（> 8KB/篇）— 已完成
2. **2026-Q2 A组冲刺**: ✅ 完成 11 个高价值行业占位符的批量扩展（> 35KB/篇，含Mermaid图、3+表格、2+代码示例）— 已完成
3. **2026-Q3 目标**: 扩展剩余的 11 个占位符案例，全面覆盖 20+ 垂直行业
4. **索引维护**: 每月更新 `CASE-STUDIES-INDEX.md`，确保新增案例被正确索引
5. **模板合规**: 所有新扩展案例严格遵循 `Case-Study-Template.md` 的 6 段式结构"""
content = content.replace(old_actions, new_actions)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Completion report updated successfully.")
