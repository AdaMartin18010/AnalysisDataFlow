# TKG 推理的强化学习方法

> **所属阶段**: Knowledge/ | **前置依赖**: [online-tkg-learning.md](../Struct/online-tkg-learning.md), [rl-query-optimization.md](./rl-query-optimization.md) | **形式化等级**: L4

---

## 1. 概念定义 (Definitions)

时序知识图谱（TKG）推理的核心任务之一是链接预测：给定主体实体和关系，预测在特定时间有效的客体实体。
传统的基于嵌入的方法（如 TComplEx）通过静态训练学习表示，而强化学习方法（如 ARLIE）将推理建模为图上的路径遍历问题，通过与 TKG 环境交互来学习最优的推理策略。

**Def-K-06-390 TKG 推理 MDP**

TKG 推理 MDP $\mathcal{M}_{TKG}$ 定义为：

$$
\mathcal{M}_{TKG} = (\mathcal{E} \times \mathcal{T}, \mathcal{R}, \mathcal{P}, \mathcal{R}_{goal}, \gamma)
$$

其中：

- 状态 $(e_t, \tau)$: 当前所在实体和时间戳
- 动作 $r$: 选择的关系边进行转移
- 转移: 从 $(e_t, \tau)$ 通过关系 $r$ 转移到 $(e_{t+1}, \tau')$，其中 $(e_t, r, e_{t+1}, \tau') \in \mathcal{G}$
- 奖励: 若最终到达目标实体则 $R = 1$，否则 $R = 0$

**Def-K-06-391 时序路径策略 (Temporal Path Policy)**

策略网络 $\pi_\theta$ 根据当前状态和历史路径选择下一个关系：

$$
\pi_\theta(r | (e, \tau), path_{hist}) = \text{softmax}(W \cdot [h_e; h_\tau; h_{path}] + b)
$$

其中 $h_e, h_\tau, h_{path}$ 分别为实体嵌入、时间嵌入和历史路径嵌入。

---

## 2. 属性推导 (Properties)

**Lemma-K-06-148 路径长度的偏差-方差权衡**

设最大路径长度为 $K$。增加 $K$ 可以降低由于路径过短导致的假阴性（偏差），但会增加策略网络搜索的方差：

$$
\text{Bias}^2 \propto e^{-\beta K}, \quad \text{Var} \propto K \cdot d_{out}^{K}
$$

*说明*: 最优 $K$ 取决于 TKG 的平均直径和连通度。$\square$

---

## 3. 关系建立 (Relations)

### 3.1 RL 推理与嵌入方法的对比

| 维度 | 嵌入方法 | RL 推理 |
|------|---------|---------|
| 可解释性 | 低 | 高（显式路径） |
| 训练数据 | 大量三元组 | 正负路径样本 |
| 泛化 | 跨实体泛化 | 跨关系泛化 |
| 时序建模 | 隐式 | 显式（时间约束） |

---

## 4. 论证过程 (Argumentation)

### 4.1 ARLIE 的核心创新

ARLIE（TKDE 2026）提出三项关键机制：

1. **时间感知注意力**: 在路径选择时优先选择时间跨度与查询窗口重叠的边
2. **历史路径正则化**: 惩罚循环路径和冗余跳跃
3. **课程学习**: 从简单查询（短路径、高连通实体）开始训练，逐步增加难度

---

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

**Thm-K-06-155 RL 路径推理的完备性**

设 TKG 中从 $s$ 到 $o$ 存在长度不超过 $K$ 的有效时序路径。若策略网络以非零概率探索所有可能的边，则在足够多的 episode 后，RL 智能体找到该路径的概率趋于 1。

*证明*: 这是多臂老虎机探索-利用问题的直接推论。$\epsilon$-greedy 或熵正则化策略保证了每条边被无限次探索。$\square$

---

## 6. 实例验证 (Examples)

### 6.1 路径推理 Agent 的伪代码

```python
class TKGReasoningAgent:
    def __init__(self, entity_embeddings, relation_embeddings):
        self.e_emb = entity_embeddings
        self.r_emb = relation_embeddings

    def step(self, current_entity, query_time, query_relation, path_history):
        candidates = self.get_neighbors(current_entity, query_time)
        scores = []
        for next_entity, relation, edge_time in candidates:
            state_vec = np.concatenate([
                self.e_emb[next_entity],
                self.r_emb[relation],
                self.time_embed(edge_time),
                self.path_embed(path_history)
            ])
            score = self.policy_net(state_vec)
            scores.append(score)

        action_idx = np.argmax(scores)
        return candidates[action_idx]
```

---

## 7. 可视化 (Visualizations)

### 7.1 TKG 上的路径搜索

```mermaid
graph LR
    S[Alice] -->|worksAt<br/>2020| A[TechCorp]
    A -->|acquires<br/>2021| B[StartUp]
    B -->|produces<br/>2022| C[AIChip]
    style C fill:#e8f5e9,stroke:#1b5e20
```

---

## 8. 引用参考 (References)

---

*文档版本: v1.0 | 创建日期: 2026-04-15*
