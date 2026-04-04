# AnalysisDataFlow 配置模板库

> 所属阶段: CONFIG-TEMPLATES | 版本: 1.0 | 最后更新: 2026-04-04

## 概述

本目录包含 Apache Flink 在各种环境和场景下的完整配置模板，涵盖开发、测试、生产环境以及主流云厂商的部署方案。

## 目录结构

```
CONFIG-TEMPLATES/
├── README.md                              # 本文件
├── development/                           # 开发环境配置
│   ├── flink-conf-dev.yaml               # 开发环境 Flink 配置
│   ├── docker-compose-dev.yml            # Docker Compose 开发环境
│   └── ide-config-guide.md               # IDE 配置指南
├── testing/                               # 测试环境配置
│   ├── flink-conf-test.yaml              # 测试环境 Flink 配置
│   ├── k8s-flink-test.yaml               # Kubernetes 测试部署
│   └── test-data-generator.py            # 测试数据生成脚本
├── production/                            # 生产环境配置
│   ├── flink-conf-production.yaml        # 生产环境 Flink 配置
│   ├── k8s-flink-production.yaml         # Kubernetes 生产部署
│   └── ha-security-guide.md              # 高可用与安全指南
├── scenarios/                             # 场景专用配置
│   ├── low-latency-config.yaml           # 低延迟场景
│   ├── high-throughput-config.yaml       # 高吞吐场景
│   ├── large-state-config.yaml           # 大状态场景
│   ├── multi-tenant-config.yaml          # 多租户场景
│   └── scenario-comparison.md            # 场景对比说明
└── cloud-providers/                       # 云厂商配置
    ├── aws-emr-config.yaml               # AWS EMR 配置
    ├── azure-hdinsight-config.yaml       # Azure HDInsight 配置
    ├── gcp-dataproc-config.yaml          # GCP Dataproc 配置
    ├── aliyun-realtime-compute-config.yaml # 阿里云配置
    └── cloud-provider-comparison.md      # 云厂商对比
```

## 快速开始

### 开发环境

```bash
# 使用 Docker Compose 启动本地开发环境
cd development
docker-compose -f docker-compose-dev.yml up -d

# 访问 Flink Web UI
open http://localhost:8081
```

### 测试环境 (Kubernetes)

```bash
# 部署到 Kubernetes 测试集群
cd testing
kubectl apply -f k8s-flink-test.yaml

# 验证部署
kubectl get pods -n flink-test
```

### 生产环境 (Kubernetes)

```bash
# 设置环境变量
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx

# 部署生产集群
cd production
envsubst < k8s-flink-production.yaml | kubectl apply -f -
```

## 配置选择指南

### 按环境选择

| 环境 | 推荐配置 | 适用场景 |
|------|----------|----------|
| **本地开发** | `flink-conf-dev.yaml` | 单机调试、功能开发 |
| **集成测试** | `flink-conf-test.yaml` | CI/CD、自动化测试 |
| **生产部署** | `flink-conf-production.yaml` | 线上服务、核心业务 |

### 按场景选择

| 场景 | 配置文件 | 关键特性 |
|------|----------|----------|
| **低延迟** | `low-latency-config.yaml` | 延迟 < 100ms |
| **高吞吐** | `high-throughput-config.yaml` | 吞吐 > 1M/s |
| **大状态** | `large-state-config.yaml` | 支持 TB 级状态 |
| **多租户** | `multi-tenant-config.yaml` | 资源隔离、安全 |

### 按云厂商选择

| 云厂商 | 配置文件 | 集成服务 |
|--------|----------|----------|
| **AWS** | `aws-emr-config.yaml` | S3, Kinesis, MSK, Glue |
| **Azure** | `azure-hdinsight-config.yaml` | ADLS, Event Hubs, Synapse |
| **GCP** | `gcp-dataproc-config.yaml` | GCS, BigQuery, Pub/Sub |
| **阿里云** | `aliyun-realtime-compute-config.yaml` | OSS, DataHub, Hologres |

## 关键配置参数速查

### 内存配置

| 环境 | JM 内存 | TM 内存 | 托管内存 |
|------|---------|---------|----------|
| 开发 | 1024m | 2048m | 512m |
| 测试 | 2048m | 4096m | 1024m |
| 生产 | 4096m | 16384m | 4096m |
| 大状态 | 4096m | 65536m | 16384m |

### Checkpoint 配置

| 场景 | 间隔 | 超时 | Unaligned |
|------|------|------|-----------|
| 低延迟 | 5s | 1m | 启用 |
| 高吞吐 | 60s | 10m | 禁用 |
| 大状态 | 300s | 20m | 禁用 |

## 环境变量模板

各配置文件支持以下环境变量，可在部署前设置：

```bash
# 必需变量
export ZOOKEEPER_QUORUM=zookeeper:2181
export CHECKPOINT_DIR=s3p://bucket/checkpoints
export SAVEPOINT_DIR=s3p://bucket/savepoints
export HA_STORAGE_DIR=s3p://bucket/ha

# 云厂商认证
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
export AZURE_CLIENT_ID=xxx
export AZURE_CLIENT_SECRET=xxx
export ALICLOUD_ACCESS_KEY_ID=xxx
export ALICLOUD_ACCESS_KEY_SECRET=xxx
```

## 配置对比说明

### 开发 vs 测试 vs 生产

| 特性 | 开发 | 测试 | 生产 |
|------|------|------|------|
| **高可用** | ❌ | ✅ | ✅ |
| **资源限制** | 宽松 | 中等 | 严格 |
| **安全检查** | 宽松 | 中等 | 严格 |
| **日志级别** | DEBUG | INFO | WARN |
| **监控** | 基础 | 完整 | 全面 |

## 最佳实践

### 1. 配置管理

- 使用版本控制管理配置变更
- 敏感信息使用环境变量或 Secret
- 不同环境使用独立的配置文件

### 2. 安全建议

- 生产环境启用 SSL/TLS
- 使用托管标识代替密钥
- 配置网络隔离策略

### 3. 性能优化

- 根据数据特征选择状态后端
- 合理设置并行度和 Slot
- 监控 Checkpoint 和反压指标

### 4. 成本控制

- 使用 Spot/抢占式实例
- 配置自动扩缩容
- 定期清理过期 Checkpoint

## 故障排查

### 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| OOM | 内存不足 | 增大 TM 内存或优化状态 |
| 反压 | 处理速度慢 | 增加并行度或优化逻辑 |
| Checkpoint 失败 | 存储问题 | 检查 S3/OSS 连接 |
| 启动慢 | 资源不足 | 检查资源配额和限制 |

## 参考资源

- [Apache Flink 官方文档](https://nightlies.apache.org/flink/flink-docs-stable/)
- [Flink on Kubernetes](https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-stable/)
- [AWS EMR Flink](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-flink.html)
- [Azure HDInsight Flink](https://docs.microsoft.com/azure/hdinsight/flink/)
- [GCP Dataproc Flink](https://cloud.google.com/dataproc/docs/concepts/components/flink)

## 更新日志

### v1.0 (2026-04-04)

- 初始版本
- 包含开发、测试、生产环境配置
- 覆盖四大场景配置
- 支持主流云厂商

---

*如有问题或建议，请参考项目主文档或提交 Issue。*
