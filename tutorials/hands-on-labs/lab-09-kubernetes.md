# Lab 9: Flink on Kubernetes 部署实战

> 所属阶段: Flink/Hands-on | 前置依赖: [Lab 8: 连接器使用](./lab-08-connectors.md) | 预计时间: 90分钟 | 形式化等级: L3

## 实验目标

- [x] 掌握 Flink Kubernetes Operator 的安装和配置
- [x] 学会部署 Flink Session 集群（会话模式）
- [x] 学会部署 Flink Application 集群（应用模式）
- [x] 掌握 Flink on K8s 的高可用（HA）配置
- [x] 学会集成 Prometheus 和 Grafana 进行监控
- [x] 理解 K8s 环境下的故障排查方法

## 前置知识

- Kubernetes 基础（Pod、Deployment、Service、ConfigMap）
- kubectl 命令行工具使用
- Helm 包管理器基础
- Docker 镜像构建

## 环境准备

### 1. 准备 Kubernetes 集群

```bash
# 使用本地开发集群(选择一个)
# 方案 1: minikube
minikube start --driver=docker --memory=8192 --cpus=4

# 方案 2: kind
kind create cluster --name flink-cluster

# 方案 3: Docker Desktop K8s(启用 Kubernetes)

# 验证集群
kubectl cluster-info
kubectl get nodes
```

### 2. 安装 Helm

```bash
# macOS
brew install helm

# Linux
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 验证
helm version
```

### 3. 安装必需工具

```bash
# 安装 k9s(可选,用于交互式查看 K8s 资源)
brew install k9s

# 安装 stern(日志查看)
brew install stern
```

## 实验步骤

### 步骤 1: 安装 Flink Kubernetes Operator

#### 1.1 添加 Helm 仓库

```bash
# 添加 Flink Operator Helm 仓库
helm repo add flink-operator-repo https://downloads.apache.org/flink/flink-kubernetes-operator-1.7.0/

# 更新仓库
helm repo update

# 查看可用版本
helm search repo flink-operator
```

#### 1.2 安装 Flink Operator

```bash
# 创建命名空间
kubectl create namespace flink-operator

# 安装 Operator(默认配置)
helm install flink-kubernetes-operator flink-operator-repo/flink-kubernetes-operator \
  --namespace flink-operator \
  --set image.repository=apache/flink-kubernetes-operator \
  --set image.tag=1.7.0

# 等待 Operator 就绪
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=flink-kubernetes-operator \
  -n flink-operator --timeout=300s

# 查看 Operator Pod
kubectl get pods -n flink-operator
```

#### 1.3 验证 Operator 安装

```bash
# 检查 CRD 是否已安装
kubectl get crd | grep flink

# 预期输出:
# flinkdeployments.flink.apache.org
# flinksessionjobs.flink.apache.org
# flinkstatebackends.flink.apache.org

# 查看 Operator 日志
kubectl logs -n flink-operator -l app.kubernetes.io/name=flink-kubernetes-operator --tail=100
```

#### 1.4 自定义 Operator 配置（可选）

创建 `operator-values.yaml`：

```yaml
# Operator 资源配置
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "1000m"

# 默认 Flink 版本
defaultFlinkVersion: v1.18

# 镜像配置
image:
  repository: apache/flink-kubernetes-operator
  tag: 1.7.0
  pullPolicy: IfNotPresent

# 监控配置
metrics:
  enabled: true
  port: 9999

# 日志级别
logLevel: INFO
```

安装时应用配置：

```bash
helm install flink-kubernetes-operator flink-operator-repo/flink-kubernetes-operator \
  --namespace flink-operator \
  -f operator-values.yaml
```

### 步骤 2: 部署 Flink Session 集群

Session 模式下，先启动一个长期运行的 Flink 集群，然后提交多个作业到该集群。

#### 2.1 创建 Session 集群 YAML

创建 `session-cluster.yaml`：

```yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: session-cluster
  namespace: flink
spec:
  image: flink:1.18.0-scala_2.12-java11
  flinkVersion: v1.18
  mode: native

  # JobManager 配置
  jobManager:
    resource:
      memory: "2048m"
      cpu: 1
    replicas: 1
    # 高可用配置(单节点可不配置)
    # replicas: 3

  # TaskManager 配置
  taskManager:
    resource:
      memory: "2048m"
      cpu: 1
    replicas: 2

  # Flink 配置
  flinkConfiguration:
    # Checkpoint 配置
    execution.checkpointing.interval: "10s"
    execution.checkpointing.min-pause-between-checkpoints: "5s"
    execution.checkpointing.max-concurrent-checkpoints: "1"
    state.backend: rocksdb
    state.checkpoints.dir: file:///tmp/flink-checkpoints

    # Web UI 配置
    rest.flamegraph.enabled: "true"
    web.submit.enable: "true"

    # 资源管理
    kubernetes.cluster-id: session-cluster
    kubernetes.container.image.pull-policy: IfNotPresent
    kubernetes.namespace: flink

  # 服务配置
  service:
    type: NodePort
    # 或 LoadBalancer(云环境)
    # type: LoadBalancer

  # Pod 模板(可选,用于自定义 Pod 配置)
  podTemplate:
    apiVersion: v1
    kind: Pod
    metadata:
      name: pod-template
    spec:
      containers:
        - name: flink-main-container
          env:
            - name: TZ
              value: Asia/Shanghai
          volumeMounts:
            - name: flink-volume
              mountPath: /opt/flink/volume
      volumes:
        - name: flink-volume
          emptyDir: {}
```

#### 2.2 部署 Session 集群

```bash
# 创建命名空间
kubectl create namespace flink

# 应用 Session 集群配置
kubectl apply -f session-cluster.yaml

# 查看部署状态
kubectl get flinkdeployment -n flink
kubectl describe flinkdeployment session-cluster -n flink

# 等待集群就绪
kubectl wait --for=condition=ready flinkdeployment/session-cluster -n flink --timeout=300s
```

#### 2.3 查看 Session 集群资源

```bash
# 查看所有 Pod
kubectl get pods -n flink

# 预期输出:
# NAME                                         READY   STATUS    RESTARTS   AGE
# session-cluster-7d9f8b6c5-x9k2p             1/1     Running   0          2m
# session-cluster-taskmanager-1-7d9f8b6c5-a1b2 1/1     Running   0          2m
# session-cluster-taskmanager-1-7d9f8b6c5-c3d4 1/1     Running   0          2m

# 查看 Service
kubectl get svc -n flink

# 获取 Web UI 地址
minikube service session-cluster-rest -n flink --url
# 或
kubectl port-forward svc/session-cluster-rest 8081:8081 -n flink
```

#### 2.4 提交作业到 Session 集群

```bash
# 获取 Flink CLI
docker exec -it <jobmanager-pod> bash

# 使用 Flink CLI 提交作业
flink run \
  --target kubernetes-session \
  -Dkubernetes.cluster-id=session-cluster \
  -Dkubernetes.namespace=flink \
  /opt/flink/examples/streaming/WordCount.jar

# 或使用 kubectl 提交 SessionJob 资源
```

创建 `session-job.yaml`：

```yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkSessionJob
metadata:
  name: wordcount-job
  namespace: flink
spec:
  deploymentName: session-cluster
  job:
    jarURI: local:///opt/flink/examples/streaming/WordCount.jar
    parallelism: 2
    upgradeMode: stateful
    state: running
    # 检查点配置
    checkpointingInterval: 10000
    # 重启策略
    restartPolicy:
      type: FixedDelay
      fixedDelay:
        attempts: 3
        delayBetweenAttempts: "10s"
```

```bash
kubectl apply -f session-job.yaml

# 查看作业状态
kubectl get flinksessionjob -n flink
kubectl describe flinksessionjob wordcount-job -n flink
```

### 步骤 3: 部署 Flink Application 集群

Application 模式下，每个作业独立运行在自己的 Flink 集群中。

#### 3.1 准备应用镜像

创建 `Dockerfile`：

```dockerfile
FROM flink:1.18.0-scala_2.12-java11

# 复制作业 JAR
COPY target/my-flink-job-1.0.jar /opt/flink/usrlib/my-job.jar

# 复制依赖(如需要)
# COPY lib/ /opt/flink/lib/

# 设置权限
RUN chown -R flink:flink /opt/flink/usrlib

USER flink
```

构建并推送镜像：

```bash
# 构建镜像
docker build -t my-registry/my-flink-job:1.0 .

# 推送镜像(本地测试可跳过)
docker push my-registry/my-flink-job:1.0

# 对于 minikube,加载镜像到集群
minikube image load my-registry/my-flink-job:1.0
```

#### 3.2 创建 Application 集群 YAML

创建 `application-cluster.yaml`：

```yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: user-behavior-analysis
  namespace: flink
spec:
  image: my-registry/my-flink-job:1.0
  flinkVersion: v1.18
  mode: native

  jobManager:
    resource:
      memory: "2048m"
      cpu: 1
    replicas: 1

  taskManager:
    resource:
      memory: "4096m"
      cpu: 2
    replicas: 3

  # 作业配置
  job:
    jarURI: local:///opt/flink/usrlib/my-job.jar
    mainClass: com.example.UserBehaviorAnalysis
    args:
      - "--kafka.bootstrap.servers"
      - "kafka:9092"
      - "--output.path"
      - "/data/output"
    parallelism: 6
    upgradeMode: stateful
    state: running

  flinkConfiguration:
    # Checkpoint 和 Savepoint
    execution.checkpointing.interval: "30s"
    execution.checkpointing.timeout: "10min"
    execution.checkpointing.externalized-checkpoint-retention: RETAIN_ON_CANCELLATION
    state.backend: rocksdb
    state.backend.incremental: "true"
    state.checkpoints.dir: s3p://my-bucket/flink-checkpoints
    state.savepoints.dir: s3p://my-bucket/flink-savepoints

    # 网络内存配置
    taskmanager.memory.network.fraction: "0.15"
    taskmanager.memory.network.min: "128mb"
    taskmanager.memory.network.max: "512mb"

    # 序列化缓冲区
    taskmanager.memory.framework.off-heap.batch-allocations: "true"

    # JVM 参数
    env.java.opts.jobmanager: "-XX:+UseG1GC -XX:MaxRAMPercentage=75.0"
    env.java.opts.taskmanager: "-XX:+UseG1GC -XX:MaxRAMPercentage=75.0"

  # Pod 模板
  podTemplate:
    spec:
      containers:
        - name: flink-main-container
          volumeMounts:
            - name: config-volume
              mountPath: /opt/flink/conf/extra
            - name: data-volume
              mountPath: /data
      volumes:
        - name: config-volume
          configMap:
            name: flink-config
        - name: data-volume
          persistentVolumeClaim:
            claimName: flink-data-pvc
```

#### 3.3 部署 Application 集群

```bash
# 先创建 ConfigMap 和 PVC(如需要)
kubectl create configmap flink-config \
  --from-file=application.conf \
  -n flink

kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: flink-data-pvc
  namespace: flink
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
EOF

# 部署 Application 集群
kubectl apply -f application-cluster.yaml

# 查看部署状态
kubectl get flinkdeployment user-behavior-analysis -n flink

# 查看 Pod
kubectl get pods -n flink -l app=user-behavior-analysis

# 查看日志
kubectl logs -n flink -l app=user-behavior-analysis -f
```

### 步骤 4: 配置高可用（HA）

#### 4.1 基于 Kubernetes 的 HA

Flink 使用 Kubernetes ConfigMap 存储 JobManager 的高可用数据。

更新 `session-cluster-ha.yaml`：

```yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: session-cluster-ha
  namespace: flink
spec:
  image: flink:1.18.0-scala_2.12-java11
  flinkVersion: v1.18
  mode: native

  jobManager:
    resource:
      memory: "2048m"
      cpu: 1
    replicas: 3  # HA 需要多个 JobManager

  taskManager:
    resource:
      memory: "2048m"
      cpu: 1
    replicas: 2

  flinkConfiguration:
    # HA 配置
    high-availability: org.apache.flink.kubernetes.highavailability.KubernetesHaServicesFactory
    high-availability.cluster-id: session-cluster-ha
    high-availability.storageDir: file:///tmp/flink-ha

    # JobManager 选举配置
    kubernetes.leader-election.enabled: "true"

    # 检查点配置(HA 必需)
    execution.checkpointing.interval: "10s"
    state.backend: rocksdb
    state.checkpoints.dir: file:///tmp/flink-checkpoints

    # 故障恢复
    restart-strategy: fixed-delay
    restart-strategy.fixed-delay.attempts: 10
    restart-strategy.fixed-delay.delay: 10s

  # 需要 RBAC 权限来操作 ConfigMap
  serviceAccount: flink
```

#### 4.2 创建 RBAC 权限

```bash
# 创建 ServiceAccount
kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: flink
  namespace: flink
EOF

# 创建 Role
kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: flink
  namespace: flink
rules:
  - apiGroups: [""]
    resources: ["pods", "configmaps", "services", "persistentvolumeclaims"]
    verbs: ["create", "get", "list", "watch", "update", "delete", "patch"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["create", "get", "list", "watch", "update", "delete", "patch"]
EOF

# 创建 RoleBinding
kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: flink
  namespace: flink
subjects:
  - kind: ServiceAccount
    name: flink
    namespace: flink
roleRef:
  kind: Role
  name: flink
  apiGroup: rbac.authorization.k8s.io
EOF
```

#### 4.3 验证 HA 配置

```bash
# 部署 HA 集群
kubectl apply -f session-cluster-ha.yaml

# 查看多个 JobManager
kubectl get pods -n flink -l component=jobmanager

# 模拟 JobManager 故障
kubectl delete pod session-cluster-ha-jobmanager-0 -n flink

# 观察自动恢复
kubectl get pods -n flink -w

# 检查 HA 数据存储
kubectl get configmaps -n flink | grep session-cluster-ha
```

### 步骤 5: 监控集成（Prometheus + Grafana）

#### 5.1 安装 Prometheus

```bash
# 添加 Prometheus Helm 仓库
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# 安装 Prometheus
helm install prometheus prometheus-community/prometheus \
  --namespace monitoring \
  --create-namespace \
  --set server.persistentVolume.enabled=false

# 等待 Prometheus 就绪
kubectl wait --for=condition=ready pod -l app=prometheus-server \
  -n monitoring --timeout=300s
```

#### 5.2 配置 Flink 指标暴露

更新 Flink 配置：

```yaml
flinkConfiguration:
  # 启用 Prometheus 报告器
  metrics.reporters: prom
  metrics.reporter.prom.class: org.apache.flink.metrics.prometheus.PrometheusReporter
  metrics.reporter.prom.port: "9999"

  # 详细指标
  metrics.scope.jm: "jobmanager"
  metrics.scope.tm: "taskmanager"
  metrics.scope.task: "task"
  metrics.scope.operator: "operator"
```

#### 5.3 创建 ServiceMonitor

创建 `flink-servicemonitor.yaml`：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: flink-metrics
  namespace: monitoring
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: flink
  namespaceSelector:
    matchNames:
      - flink
  endpoints:
    - port: metrics
      interval: 15s
      path: /metrics
```

```bash
kubectl apply -f flink-servicemonitor.yaml
```

#### 5.4 安装 Grafana

```bash
# 添加 Grafana Helm 仓库
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# 安装 Grafana
helm install grafana grafana/grafana \
  --namespace monitoring \
  --set adminPassword=admin \
  --set service.type=NodePort

# 获取 Grafana 访问地址
minikube service grafana -n monitoring --url
# 或
kubectl port-forward svc/grafana 3000:3000 -n monitoring
```

#### 5.5 导入 Flink Dashboard

```bash
# 获取 Grafana 登录密码(如未设置)
kubectl get secret grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 --decode

# 登录 Grafana (admin/admin)
# 访问: http://localhost:3000
```

在 Grafana 中：

1. 进入 **Configuration > Data Sources**
2. 添加 **Prometheus** 数据源，URL: `http://prometheus-server.monitoring.svc.cluster.local`
3. 导入 Flink Dashboard（ID: `11049` 或自定义 JSON）

自定义 Dashboard JSON 配置：

```json
{
  "dashboard": {
    "title": "Flink on K8s Dashboard",
    "panels": [
      {
        "title": "TaskManager Count",
        "type": "stat",
        "targets": [{
          "expr": "flink_taskmanager_numRegisteredTaskManagers"
        }]
      },
      {
        "title": "Checkpoint Duration",
        "type": "graph",
        "targets": [{
          "expr": "flink_jobmanager_checkpoint_duration"
        }]
      },
      {
        "title": "Records Per Second",
        "type": "graph",
        "targets": [{
          "expr": "rate(flink_taskmanager_job_task_numRecordsIn[1m])"
        }]
      }
    ]
  }
}
```

#### 5.6 配置告警规则

创建 `flink-alerts.yaml`：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: flink-alerts
  namespace: monitoring
spec:
  groups:
    - name: flink
      rules:
        - alert: FlinkCheckpointFailed
          expr: increase(flink_jobmanager_checkpoint_numberOfFailedCheckpoints[5m]) > 0
          for: 1m
          labels:
            severity: critical
          annotations:
            summary: "Flink checkpoint failed"

        - alert: FlinkJobRestarting
          expr: flink_jobmanager_job_restartingTime > 0
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Flink job is restarting"

        - alert: FlinkHighMemoryUsage
          expr: flink_taskmanager_Status_JVM_Memory_Heap_Used / flink_taskmanager_Status_JVM_Memory_Heap_Committed > 0.8
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Flink TaskManager high memory usage"
```

```bash
kubectl apply -f flink-alerts.yaml
```

### 步骤 6: 日志集成

#### 6.1 配置日志收集

创建 `log4j-console.properties` ConfigMap：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: flink-log4j
  namespace: flink
data:
  log4j-console.properties: |
    rootLogger.level = INFO
    rootLogger.appenderRef.console.ref = ConsoleAppender

    appender.console.name = ConsoleAppender
    appender.console.type = CONSOLE
    appender.console.layout.type = PatternLayout
    appender.console.layout.pattern = %d{yyyy-MM-dd HH:mm:ss,SSS} %-5p %-60c %x - %m%n

    # 增加 Flink 特定日志
    logger.flink.name = org.apache.flink
    logger.flink.level = INFO
```

#### 6.2 使用 Loki 收集日志（可选）

```bash
# 安装 Loki
helm install loki grafana/loki-stack \
  --namespace monitoring \
  --set grafana.enabled=false \
  --set promtail.enabled=true

# 配置 Pod 日志标签
podTemplate:
  metadata:
    annotations:
      promtail.io/scrape: "true"
      promtail.io/port: "9999"
```

## 验证方法

### 检查清单

- [ ] Flink Operator 运行正常
- [ ] Session 集群所有 Pod 就绪
- [ ] Application 集群启动成功
- [ ] 作业提交并正常运行
- [ ] HA 配置下 JobManager 故障可自动恢复
- [ ] Prometheus 能采集到 Flink 指标
- [ ] Grafana Dashboard 显示正常

### 验证命令

```bash
# 检查 FlinkDeployment 状态
kubectl get flinkdeployment -n flink

# 查看详细状态
kubectl describe flinkdeployment session-cluster -n flink

# 查看事件
kubectl get events -n flink --sort-by='.lastTimestamp'

# 端口转发访问 Web UI
kubectl port-forward svc/session-cluster-rest 8081:8081 -n flink

# 验证 Prometheus 指标
curl http://prometheus-server.monitoring.svc.cluster.local:9090/api/v1/query?query=flink_jobmanager_numRegisteredTaskManagers
```

## 故障排查

### 常见问题诊断

| 问题 | 诊断命令 | 解决方案 |
|------|---------|---------|
| Pod 启动失败 | `kubectl describe pod <pod> -n flink` | 检查资源限制、镜像拉取 |
| 作业提交失败 | `kubectl logs <jobmanager> -n flink` | 检查类名、JAR 路径 |
| 检查点失败 | `kubectl logs <taskmanager> -n flink` | 检查存储权限、网络 |
| 内存不足 | `kubectl top pod -n flink` | 调整内存配置 |
| 网络不通 | `kubectl exec -it <pod> -- ping <target>` | 检查 Service、NetworkPolicy |

### Pod 调试

```bash
# 进入 Pod 调试
kubectl exec -it <taskmanager-pod> -n flink -- bash

# 查看进程
ps aux | grep flink

# 查看内存使用
free -h
cat /proc/$(pgrep java)/status | grep VmRSS

# 网络调试
netstat -tlnp
curl http://jobmanager:8081/config
```

### 获取 Heap Dump

```yaml
podTemplate:
  spec:
    containers:
      - name: flink-main-container
        env:
          - name: JVM_ARGS
            value: "-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/heapdump.hprof"
        volumeMounts:
          - name: heap-dumps
            mountPath: /tmp
    volumes:
      - name: heap-dumps
        emptyDir:
          sizeLimit: 2Gi
```

## 清理资源

```bash
# 删除 Flink 作业和集群
kubectl delete -f session-job.yaml
kubectl delete -f application-cluster.yaml
kubectl delete -f session-cluster.yaml

# 删除 Operator
helm uninstall flink-kubernetes-operator -n flink-operator

# 删除命名空间
kubectl delete namespace flink
kubectl delete namespace flink-operator

# 删除监控
helm uninstall prometheus -n monitoring
helm uninstall grafana -n monitoring
kubectl delete namespace monitoring
```

## 生产部署建议

```yaml
# 生产环境推荐配置
spec:
  # 资源预留
  jobManager:
    resource:
      memory: "4096m"
      cpu: 2
    replicas: 3  # HA

  taskManager:
    resource:
      memory: "8192m"
      cpu: 4
    replicas: 5

  flinkConfiguration:
    # 生产级检查点配置
    execution.checkpointing.interval: "5min"
    execution.checkpointing.timeout: "30min"
    execution.checkpointing.max-concurrent-checkpoints: "1"
    execution.checkpointing.min-pause-between-checkpoints: "30s"
    execution.checkpointing.prefer-checkpoint-for-recovery: "true"

    # 网络配置
    taskmanager.memory.network.fraction: "0.2"
    taskmanager.memory.network.min: "256mb"
    taskmanager.memory.network.max: "1gb"

    # 反压处理
    web.backpressure.refresh-interval: "60000"

    # 安全性
    security.ssl.enabled: "true"
    security.ssl.internal.enabled: "true"
```

## 下一步

完成本实验后，继续学习：

- [Lab 5: Checkpoint 机制](../interactive/hands-on-labs/lab-05-checkpoint.md) - 深入理解检查点
- [Flink 官方文档 - Kubernetes Integration](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/resource-providers/native_kubernetes/)
- Flink on K8s 高级调优和最佳实践

## 引用参考
