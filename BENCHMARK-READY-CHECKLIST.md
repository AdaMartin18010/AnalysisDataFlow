# AnalysisDataFlow 基准测试就绪检查清单 v4.1

> **用途**: 在实际执行性能基准测试前，逐项确认环境和前置条件

---

## 环境准备

- [ ] 测试集群已就绪（3 节点 K8s 或等效环境）
- [ ] 各节点硬件规格符合 `BENCHMARK-EXECUTION-PLAN-v4.1.md` 要求
- [ ] 网络连通性测试通过（节点间延迟 < 0.1ms）
- [ ] 磁盘 I/O 基准测试通过（NVMe SSD 顺序写 > 1GB/s）

## 软件栈

- [ ] Apache Flink 2.0.0 镜像已拉取
- [ ] Kubernetes 1.29+ 集群正常运行
- [ ] Kafka 3.6+ 可用于数据源注入
- [ ] Prometheus + Grafana 已部署并可访问
- [ ] Python 3.11+ 和依赖库已安装

## 部署验证

- [ ] `kubectl apply -f benchmark-data/k8s/flink-benchmark-deployment.yaml` 成功
- [ ] Flink JobManager Web UI 可访问（`kubectl port-forward svc/flink-benchmark-jobmanager 8081:8081`）
- [ ] 6 个 TaskManager 全部注册成功（Total Slots = 48）
- [ ] Checkpoint 目录可写并持久化

## 脚本验证

- [ ] `python .scripts/benchmark-runner/generate-workload.py --output-dir /tmp/benchmark-workloads` 成功
- [ ] `python .scripts/benchmark-runner/collect-metrics.py --output-dir /tmp/benchmark-metrics` 成功
- [ ] `python .scripts/benchmark-runner/generate-report.py --results-dir /tmp/benchmark-metrics --output /tmp/test-report.md` 成功

## 数据验证

- [ ] Nexmark 数据生成器可正常生成事件流
- [ ] 自定义状态访问作业的 JAR 包已上传至 Flink 集群可访问位置
- [ ] 100GB 状态数据预热方案已确认

## 安全与回退

- [ ] 测试期间生产环境隔离确认
- [ ] 故障注入脚本不会造成集群级联故障
- [ ] 本地 Docker Compose 回退方案已验证（`docker-compose -f benchmark-data/docker-compose.yml up`）

## 人员与日程

- [ ] 测试负责人已确认
- [ ] 云资源预算已审批
- [ ] 测试时间窗口已预订（建议避开业务高峰期）

---

**确认人**: _________________
**确认日期**: _________________
**下一步**: 执行 `python .scripts/benchmark-runner/run-all-benchmarks.py --environment k8s --output-dir benchmark-results/v4.1`
