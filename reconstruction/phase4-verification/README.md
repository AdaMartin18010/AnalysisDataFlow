# AnalysisDataFlow 形式化验证套件

> **版本**: v2.0 | **最后更新**: 2026-04-19 | **状态**: 可复现验证环境就绪

---

## 目录结构

```
phase4-verification/
├── coq-proofs/                  # Coq 交互式定理证明
│   ├── WatermarkAlgebra.v
│   ├── ExactlyOnceCoq.v
│   └── ...
├── tla-specs/                   # TLA+ 模型检查规格
│   ├── StateBackendEquivalence.tla
│   ├── ExactlyOnce.tla
│   └── ...
├── Makefile                     # 一键验证入口
├── docker-compose.yml           # Docker 可复现环境
├── Dockerfile.verification      # 验证环境镜像定义
└── README.md                    # 本文件
```

---

## 快速开始

### 方式一：本地验证（需安装 Coq 和 TLA+ Tools）

```bash
# 验证所有证明
make verify

# 仅验证 Coq
make verify-coq

# 仅验证 TLA+ 语法
make verify-tla

# 清理编译产物
make clean
```

### 方式二：Docker 验证（推荐，零依赖）

```bash
# 构建并运行验证容器
docker compose build
docker compose run --rm formal-verification

# 或一步完成
docker compose up --build
```

Docker 环境包含：
- Coq 8.18 + OCaml 4.14
- TLA+ Tools 1.8
- Z3 SMT 求解器
- Java 21 (JRE)

### 方式三：GitHub Actions CI

每次提交到 `main` 分支且修改了 `reconstruction/phase4-verification/` 时，CI 自动运行验证：
- `verify-coq` 任务：编译所有 `.v` 文件
- `verify-tla` 任务：解析所有 `.tla` 文件
- `docker-verify` 任务：Docker 环境全量验证

每月 1 日进行定时全量验证。

---

## 证明清单

| 证明 | 文件 | 语言 | 状态 | 说明 |
|------|------|------|:----:|------|
| Watermark 代数完备性 | `coq-proofs/WatermarkAlgebraComplete.v` | Coq | ✅ | 744行, 19定理 |
| Exactly-Once 语义 | `coq-proofs/ExactlyOnceComplete.v` | Coq | ✅ | 864行, 19定理 |
| State Backend 等价性 | `tla-specs/StateBackendEquivalenceComplete.tla` | TLA+ | ✅ | 500+行, 13定理 |

---

## 本地开发指南

### 安装 Coq 8.18

```bash
# macOS
brew install opam
opam init --disable-sandboxing
opam switch create coq-8.18 ocaml-base-compiler.4.14.1
eval $(opam env --switch=coq-8.18)
opam install coq.8.18.0

# Ubuntu
sudo apt install opam
opam init --disable-sandboxing
opam switch create coq-8.18 ocaml-base-compiler.4.14.1
eval $(opam env --switch=coq-8.18)
opam install coq.8.18.0
```

### 安装 TLA+ Tools

```bash
wget https://github.com/tlaplus/tlaplus/releases/download/v1.8.0/tla2tools.jar
sudo mv tla2tools.jar /usr/local/lib/
```

---

## 与 Veil 框架的集成

本项目支持将 Coq/TLA+ 规格迁移到 [Veil Framework](../../formal-methods/06-tools/veil-framework-introduction.md) 进行自动不变式综合：

```bash
# 将 TLA+ 规格转换为 Veil 输入格式
python ../.scripts/tla-to-veil.py \
    --input tla-specs/StateBackendEquivalence.tla \
    --output veil-inputs/StateBackend.veil

# 运行 Veil 自动综合
veil verify veil-inputs/StateBackend.veil
```

---

## 引用参考

[^1]: AnalysisDataFlow, "FORMAL-PROOF-COMPLETION-REPORT-v4.1.md", 2026-04.
[^2]: T. Yu et al., "Model Checking TLA+ Specifications", CHARME 1999.
[^3]: The Coq Development Team, "The Coq Proof Assistant, version 8.18", 2024.
