# AI 与形式化方法 (AI × Formal Methods)

> **文档定位**: 本目录系统梳理人工智能与形式化方法的交叉领域，涵盖神经定理证明、LLM辅助形式化、神经网络验证、神经符号AI等前沿方向。
>
> **版本**: v1.0 | **创建日期**: 2026-04-10 | **状态**: 持续更新

---

## 📁 文档体系

```
08-ai-formal-methods/
├── README.md                          # 本文件 - 目录索引
├── 01-neural-theorem-proving.md       # 神经定理证明 (AlphaProof等)
├── 02-llm-formalization.md            # LLM形式化规范生成
├── 03-neural-network-verification.md  # 神经网络形式化验证
├── 04-neuro-symbolic-ai.md            # 神经符号AI
└── 90-examples/                       # 代码示例
    ├── copra_example.py
    ├── lean_dojo_example.py
    └── marabou_example.py
```

---

## 🎯 内容概览

### 1. 神经定理证明 (Neural Theorem Proving)

| 系统 | 机构 | 核心创新 | 成就 |
|------|------|---------|------|
| **AlphaProof** | DeepMind | 强化学习 + 形式证明搜索 | IMO 2024 银牌水平 |
| **DeepSeek-Prover-V1.5** | DeepSeek | 证明助手反馈的强化学习 | 高完成率 |
| **Goedel-Prover-V2** | 多机构 | 脚手架数据合成 + 自我校正 | 扩展证明能力 |
| **Kimina-Prover** | 多机构 | 基于强化学习的形式推理 | 高效搜索 |
| **STP** | 多机构 | 自教学证明器 | 13.2% → 28.5% 完成率 |
| **Copra** | 多机构 | 上下文感知证明策略 | ICLR 2024 |

### 2. LLM 形式化规范生成

- 自然语言到 TLA+/Coq/Lean 的自动转换
- 需求补全与错误检测
- 规范生成的不完备性理论

### 3. 神经网络验证

| 技术路线 | 代表工具 | 适用场景 |
|---------|---------|---------|
| 抽象解释 | AI², ERAN, DeepPoly | 鲁棒性验证 |
| SMT编码 | Reluplex, Marabou | 局部性质验证 |
| 凸松弛 | β-CROWN, CROWN | 大规模网络验证 |
| 形式化综合 | DiffAI, CERT-RNN | 训练时保证 |

### 4. 神经符号 AI

- 感知-推理闭环
- 符号知识蒸馏
- AlphaProof 系统架构

---

## 🌐 学习路径

### 路径一: 快速入门

```
01-neural-theorem-proving.md → 02-llm-formalization.md → 05-ai-assisted-proof.md
```

### 路径二: 深入研究

```
01-neural-theorem-proving.md → 03-neural-network-verification.md → 04-neuro-symbolic-ai.md
```

### 路径三: 实践导向

```
05-ai-assisted-proof.md → 06-benchmarks-and-evaluation.md → 90-examples/
```

---

## 📊 统计与进展

| 类别 | 文档数 | 形式化定义 | 定理/引理 |
|------|--------|-----------|----------|
| 神经定理证明 | 1 | 8+ | 5+ |
| LLM形式化 | 1 | 6+ | 4+ |
| NN验证 | 1 | 10+ | 8+ |
| 神经符号AI | 1 | 7+ | 4+ |
| **总计** | **4** | **31+** | **21+** |

---

## 🔗 外部资源

| 资源类型 | 链接 | 描述 |
|---------|------|------|
| **AlphaProof** | <https://deepmind.google/discover/blog/ai-solves-imo-problems-at-silver-medal-level/> | DeepMind 官方博客 |
| **LeanDojo** | <https://leandojo.org/> | 神经定理证明环境 |
| **EuroProofNet WG5** | <https://europroofnet.github.io/wg5/> | 机器学习与定理证明 |
| **Marabou** | <https://neuralnetworkverification.github.io/marabou/> | 神经网络验证器 |
| **β-CROWN** | <https://github.com/Verified-Intelligence/beta-CROWN> | 完整NN验证器 |
| **LemmaBench** | <https://arxiv.org/abs/2602.24173> | LLM数学能力基准 |

---

> **最后更新**: 2026-04-10
>
> **维护者**: AI形式化方法文档组
