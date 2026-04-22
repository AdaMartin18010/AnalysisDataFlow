# Docker Compose Full-Stack One-Click Startup (PG16 + Kafka + Flink + Temporal + Kratos)

> **Stage**: TECH-STACK | **Prerequisites**: [Chinese source](../TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/05-deployment/05.01-docker-compose-fullstack.md) | **Formalization Level**: L2-L4 | **Last Updated**: 2026-04-22

## 1. Definitions

### Def-TS-05-01-01: Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. Developers describe the services, networks, and persistent volumes required by the application through a declarative YAML file, then use a single command `docker compose up` to start the complete application stack on a single machine.

### Def-TS-05-01-02: Service Orchestration

Service orchestration is the process of automatically deploying, configuring, scaling, and managing a group of interrelated service instances according to predefined dependency relationships, startup order, and lifecycle policies. In the Docker Compose context, orchestration is implemented through fields such as `depends_on`, `condition`, `healthcheck`, and `restart`.

### Def-TS-05-01-03: Health Check

A health check is a diagnostic probe executed by the container runtime at fixed intervals, used to report the readiness state of a service instance to the orchestration system. In Compose, the `healthcheck` field defines the probe command, execution interval, timeout threshold, and failure retry count; combined with `depends_on.condition: service_healthy`, it enables startup control with dependency semantics.

### Def-TS-05-01-04: Resource Limits

Resource limits are upper-bound constraints on the computing resources (CPU, memory) that a container can use. Docker Compose limits the maximum available amount through `deploy.resources.limits`, and can supplement with `reservations` to declare reserved amounts, thereby preventing a single service from exhausting host resources and affecting other services on the same machine.

## 2. Properties

### Lemma-TS-05-01-01: Partial Order Relation of Compose Service Startup Sequence

Let the full-stack service set be $S = \{s_1, s_2, \dots, s_n\}$, and define the dependency relation $\prec \subseteq S \times S$: $s_i \prec s_j$ means "$s_i$ must complete health check before $s_j$". Then $(S, \prec)$ satisfies the following three properties:

1. **Irreflexivity**: $\forall s \in S,\; s \not\prec s$. A service does not depend on its own startup.
2. **Antisymmetry**: $\forall s_i, s_j \in S,\; s_i \prec s_j \land s_j \prec s_i \Rightarrow s_i = s_j$. The Compose engine prohibits bidirectional strong dependencies; if bidirectional edges exist, startup will deadlock.
3. **Transitivity**: $\forall s_i, s_j, s_k \in S,\; s_i \prec s_j \land s_j \prec s_k \Rightarrow s_i \prec s_k$. If $s_k$ waits for $s_j$, and $s_j$ waits for $s_i$, then $s_k$ indirectly waits for $s_i$.

Therefore, $(S, \prec)$ constitutes a **strict partial order set**. The Compose engine performs topological sorting on this partial order set; the output is a valid linear startup sequence.

### Lemma-TS-05-01-02: Startup Reachability via Health Check Propagation

Assume each service $s \in S$'s health check converges to `healthy` with probability 1 within finite time (i.e., the service is actually normal and the probe configuration is correct); then for any service $s_k$, its startup condition is necessarily satisfied within finite time.

*Proof sketch*: By Lemma-TS-05-01-01, $(S, \prec)$ is a strict partial order; its Hasse diagram must be a directed acyclic graph (DAG). A DAG has a topological order. Compose starts services layer by layer according to the topological order; each layer only waits for its direct predecessors to become healthy. Since the number of predecessors in each layer is finite and their health checks converge independently, according to probability theory, the waiting time for all predecessors to be healthy simultaneously is almost surely finite. By mathematical induction, services at any level $h$ are reachable. ∎

## 3. Relations

This deployment plan contains 8 services, 5 named volumes, and 1 custom bridge network. Their topological relationships are as follows.

### 3.1 Network Relations

All services connect to the custom bridge network `streaming-stack` (`driver: bridge`). Within this network:

- Services communicate via built-in DNS resolution using service names (e.g., `postgres`, `kafka`, `temporal` are directly reachable as hostnames).
- External access is exposed through port mapping (`ports`), for example Flink Web UI `8081`, Kratos HTTP `8000`, Temporal gRPC `7233`.
- Isolated from the default `bridge` network, avoiding address or port conflicts with other containers on the host.

### 3.2 Volume Mount Relations

| Volume Name | Mounted Service | Container Path | Purpose |
|------|---------|---------|------|
| `postgres_data` | `postgres` | `/var/lib/postgresql/data` | PG16 data persistence (upgrade to PG18 after release) |
| `kafka_data` | `kafka` | `/var/lib/kafka/data` | Kafka log segment persistence |
| `zookeeper_data` | `zookeeper` | `/var/lib/zookeeper/data` | ZK snapshot persistence |
| `zookeeper_logs` | `zookeeper` | `/var/lib/zookeeper/log` | ZK transaction logs |
| `flink-checkpoints` | `flink-jobmanager`, `flink-taskmanager` | `/tmp/flink-checkpoints` | Flink checkpoint shared directory |

### 3.3 Dependency Relations (Edges of the Partial Order Graph)

According to the actual call chain and data flow of each component, the following dependency edges are defined:

- `zookeeper` $\prec$ `kafka`
- `postgres` $\prec$ `flink-jobmanager` (as JDBC HA / metadata backend)
- `postgres` $\prec$ `temporal` (schema auto-migration and persistence)
- `postgres` $\prec$ `kratos` (business database)
- `kafka` $\prec$ `temporal` (optional Visibility storage backend)
- `flink-jobmanager` $\prec$ `flink-taskmanager` (TaskManager registers with JobManager)
- `temporal` $\prec$ `temporal-worker` (Worker polls Temporal Server task queue)
- `temporal` $\prec$ `kratos` (business service calls Workflow)

A valid topological sort of this dependency graph is:

> `zookeeper` → `postgres` → `kafka` → `flink-jobmanager` → `temporal` → `flink-taskmanager` → `temporal-worker` → `kratos`

## 4. Argumentation

### 4.1 Containerization Plan for the Five-Technology Stack

#### PostgreSQL 16

Using the `postgres:16` image (PG18 official image not yet released; can directly replace the image tag after release to enable stricter `pg_parameter_check` and enhanced parallel query等新特性). Injects `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` through environment variables, and configures `pg_isready` as a health probe to ensure downstream services only start when the database is truly ready to accept connections.

#### ZooKeeper + Kafka

Using `confluentinc/cp-zookeeper` and `confluentinc/cp-kafka` to build a single-node Kafka cluster. ZooKeeper provides cluster coordination, Leader election, and metadata storage for Brokers. Although Kafka 3.x supports KRaft mode to remove ZooKeeper, in full-stack integration testing and multi-component compatibility verification scenarios, the ZooKeeper solution's ecosystem toolchain (e.g., Flink Kafka Connector's ZooKeeper metadata query) is more mature. The Kafka data directory is persisted through the named volume `kafka_data`, avoiding topic data loss due to container rebuilds.

#### Flink 1.20

Separately deploys JobManager and TaskManager, both based on the `flink:1.20-scala_2.12` image:

- **JobManager**: Responsible for task scheduling, checkpoint coordination, and REST API. Maps host port `8081` for Web UI access.
- **TaskManager**: Responsible for task execution. Automatically registers with JobManager via environment variable `JOB_MANAGER_RPC_ADDRESS`. Configures `taskmanager.numberOfTaskSlots: 2` to support limited parallelism testing.

JobManager additionally depends on PostgreSQL, which can serve as a high-availability metadata storage backend (`high-availability: zookeeper` or JDBC HA), ensuring that stateful recovery paths can be verified even in the development environment.

#### Temporal

Using the `temporalio/auto-setup` image, which has the PostgreSQL driver built-in and automatically executes Schema Migration on first startup. Key environment variables:

- `DB=postgresql12`, `DB_HOST=postgres`, `DB_PORT=5432` point to the PG service.
- `POSTGRES_USER`, `POSTGRES_PWD` share the same database credentials.
- `VISIBILITY_DRIVER=postgres` writes visibility data to PG as well, simplifying single-machine configuration.

Temporal Server exposes `7233` (Frontend gRPC) and `8233` (HTTP API). `temporal-worker` is an independent service, usually built on `temporalio/sdk-go`, responsible for polling the task queue and executing Activities and Workflows.

#### Kratos

> **Naming Note**: The Kratos here refers to the [Go-Kratos](https://go-kratos.dev/) microservices framework (open-sourced by bilibili), which is a completely different project from ORY Kratos (Identity and Access Management IAM system) despite the same name. This document's Docker Compose stack uses Go-Kratos to build business microservices; if IAM capabilities are needed, please refer to the `oryd/kratos` Helm Chart.

Built on a `golang:1.23-alpine` multi-stage build custom image, embedding the Kratos framework-generated microservice binary. The Kratos service needs to connect to PostgreSQL (business data) and Temporal (workflow orchestration) at startup, so it depends on both. Exposes HTTP `8000` and gRPC `9000`, and performs readiness probing via `/health/ready`.

### 4.2 Service Dependency Order and Startup Strategy

The Compose file uses the extended syntax `condition: service_healthy` of `depends_on`, forcing downstream services to wait until upstream health probes pass before being created. For example:

```yaml
depends_on:
  postgres:
    condition: service_healthy
```

This eliminates race conditions caused by traditional `depends_on` only waiting for container startup (rather than service readiness). For Flink TaskManager, using `condition: service_started` is sufficient, as it only needs to wait for the JobManager container to exist before initiating RPC registration, without needing to wait for the JobManager health probe.

### 4.3 Health Check Configuration

Health check commands and strategies for each service are as follows:

- **PG16**: `pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}`
  - Probe interval `10s`, timeout `5s`, marked unhealthy after `5` failures, with `start_period: 10s` to tolerate first initialization overhead.
- **Kafka**: `kafka-broker-api-versions --bootstrap-server localhost:9092`
  - Directly verifies the Broker's API version negotiation capability, ensuring Kafka is not only process-alive but truly service-capable.
- **Temporal**: `tctl cluster health || exit 1`
  - Uses the Temporal official CLI to query cluster health status. The `auto-setup` image has `tctl` built-in, requiring no additional mounts.
- **Kratos**: `wget --no-verbose --tries=1 --spider http://localhost:8000/health/ready || exit 1`
  - Verifies the Kratos service and its dependency database connection pool, Temporal client initialization are all complete through the HTTP readiness probe.

### 4.4 Resource Limits

To prevent OOM due to resource contention on development machines or CI Runners, `deploy.resources.limits` is configured for each service:

- **ZooKeeper**: CPU `0.5` / Memory `512M`
- **Kafka**: CPU `1.0` / Memory `1G`
- **PostgreSQL**: CPU `1.0` / Memory `1G`
- **Flink JobManager**: CPU `1.0` / Memory `1G`
- **Flink TaskManager**: CPU `2.0` / Memory `2G` (stream computing is memory-intensive, given the highest quota)
- **Temporal Server**: CPU `1.0` / Memory `1G`
- **Temporal Worker**: CPU `0.5` / Memory `512M`
- **Kratos**: CPU `0.5` / Memory `512M`

The above limits total approximately CPU `6.5`, Memory `7.5G`, which can run smoothly on an 8-core 16G development machine.

### 4.5 Restart Strategy

All services are uniformly configured with `restart: unless-stopped`. This strategy guarantees:

1. When a container exits due to internal exceptions, the Docker Daemon automatically recreates the container.
2. After host reboot, services automatically recover with Docker.
3. When a developer explicitly executes `docker compose stop`, automatic restart is not triggered, conforming to human-com协作 intuition.

### 4.6 Network Isolation

The custom bridge network `streaming-stack` provides the following engineering value:

1. **Automatic DNS discovery**: Service names are hostnames; no hard-coded IPs needed.
2. **Namespace isolation**: No interference with other containers in the default `bridge` network.
3. **Subnet planning**: Explicitly configures `subnet: 172.28.0.0/16`, facilitating avoidance of routing conflicts with host VPN or enterprise intranet address ranges.
4. **Scalability**: When adding auxiliary services such as `nginx`, `prometheus`, `grafana` in the future, simply declaring the same network is sufficient for access, without modifying existing service network configurations.

## 5. Proof / Engineering Argument

### Thm-TS-05-01-01: DAG Guarantees Startup Reachability

If the directed graph $G=(S, E)$ formed by service dependency relations is acyclic (DAG), and the health check of each service $s \in S$ eventually converges to `healthy`, then the full-stack startup process necessarily completes within finite time, and all services eventually reach a stable running state.

**Engineering Argument**:

1. **Graph Structure Acyclicity Verification**
   Perform topological level analysis on the dependency edge set $E$ defined in Section 3:
   - **Level 0 (in-degree 0)**: `zookeeper`, `postgres`. No external dependencies; can be created immediately.
   - **Level 1**: `kafka` (depends on ZK), `flink-jobmanager` (depends on PG).
   - **Level 2**: `temporal` (depends on PG, Kafka).
   - **Level 3**: `flink-taskmanager` (depends on JM), `temporal-worker` (depends on Temporal), `kratos` (depends on PG, Temporal).

   For any edge $(u, v) \in E$, we have $\text{level}(u) < \text{level}(v)$. Since the level function maps nodes to finite non-negative integers, there are no edges returning from lower to higher levels; thus $G$ contains no directed cycles.

2. **Startup Reachability Inductive Proof**
   - **Base case**: Level 0 nodes have in-degree 0; the Compose engine creates them immediately upon `docker compose up`. According to the health check convergence assumption, they will become `healthy` within finite time.
   - **Inductive hypothesis**: Assume all services at level $\le k$ have started and passed health checks.
   - **Inductive step**: For level $k+1$ service $v$, all its direct predecessors $u \in \text{pred}(v)$ have levels $\le k$. By the inductive hypothesis, these predecessors are all in `healthy` state. After the Compose engine detects that all `depends_on.condition: service_healthy` are satisfied, it triggers the creation and startup of $v$. The health check of $v$ also converges (by assumption).
   - **Conclusion**: By mathematical induction, for the maximum level $H_{\max} = 3$, all services can reach healthy state within finite time.

3. **Fault Boundary Discussion**
   If a service fails to converge to healthy due to configuration errors (e.g., wrong `DB_HOST`), its direct successor services will remain in `Pending` (containers not created) rather than starting and repeatedly crashing. This "block rather than crash" behavior conforms to the fault isolation principle, avoiding massive error logs and cascading retry storms in downstream services due to connection timeouts, and facilitating rapid root cause location by developers through `docker compose ps`.

In summary, dependency DAG structure + health check convergence $\Rightarrow$ full-stack startup is reachable and predictable in the engineering sense. ∎

## 6. Examples

The following `docker-compose.yml` is a directly runnable full-stack definition, approximately 180 lines, covering PG16, ZooKeeper, Kafka, Flink, Temporal, Temporal Worker, and Kratos.

```yaml
version: "3.8"

x-default-logging: &default-logging
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.6.0
    container_name: stack-zookeeper
    hostname: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"
    volumes:
      - zookeeper_data:/var/lib/zookeeper/data
      - zookeeper_logs:/var/lib/zookeeper/log
    healthcheck:
      test: ["CMD-SHELL", "echo ruok | nc localhost 2181 | grep imok"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    logging: *default-logging
    networks:
      - streaming-stack
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M

  kafka:
    image: confluentinc/cp-kafka:7.6.0
    container_name: stack-kafka
    hostname: kafka
    depends_on:
      zookeeper:
        condition: service_healthy
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    ports:
      - "9092:9092"
      - "29092:29092"
    volumes:
      - kafka_data:/var/lib/kafka/data
    healthcheck:
      test: ["CMD-SHELL", "kafka-broker-api-versions --bootstrap-server localhost:9092"]
      interval: 10s
      timeout: 10s
      retries: 6
    restart: unless-stopped
    logging: *default-logging
    networks:
      - streaming-stack
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G

  postgres:
    image: postgres:16  # Upgrade to postgres:18 after PG18 official image release
    container_name: stack-postgres
    hostname: postgres
    environment:
      POSTGRES_USER: stack_user
      POSTGRES_PASSWORD: stack_pass
      POSTGRES_DB: stack_db
      POSTGRES_INITDB_ARGS: "--encoding=UTF8"
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    restart: unless-stopped
    logging: *default-logging
    networks:
      - streaming-stack
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G

  flink-jobmanager:
    image: flink:1.20-scala_2.12
    container_name: stack-flink-jobmanager
    hostname: flink-jobmanager
    depends_on:
      postgres:
        condition: service_healthy
    command: jobmanager
    environment:
      JOB_MANAGER_RPC_ADDRESS: flink-jobmanager
      FLINK_PROPERTIES: |-
        jobmanager.memory.process.size: 1024m
        state.backend: rocksdb
        state.checkpoints.dir: file:///tmp/flink-checkpoints
    ports:
      - "8081:8081"
    volumes:
      - flink-checkpoints:/tmp/flink-checkpoints
    restart: unless-stopped
    logging: *default-logging
    networks:
      - streaming-stack
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G

  flink-taskmanager:
    image: flink:1.20-scala_2.12
    container_name: stack-flink-taskmanager
    hostname: flink-taskmanager
    depends_on:
      flink-jobmanager:
        condition: service_started
    command: taskmanager
    environment:
      JOB_MANAGER_RPC_ADDRESS: flink-jobmanager
      FLINK_PROPERTIES: |-
        taskmanager.memory.process.size: 2048m
        taskmanager.numberOfTaskSlots: 2
    volumes:
      - flink-checkpoints:/tmp/flink-checkpoints
    restart: unless-stopped
    logging: *default-logging
    networks:
      - streaming-stack
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 2G

  temporal:
    image: temporalio/auto-setup:1.24.0
    container_name: stack-temporal
    hostname: temporal
    depends_on:
      postgres:
        condition: service_healthy
      kafka:
        condition: service_healthy
    environment:
      - DB=postgresql12
      - DB_HOST=postgres
      - DB_PORT=5432
      - POSTGRES_USER=stack_user
      - POSTGRES_PWD=stack_pass
      - POSTGRES_SEEDS=postgres
      - DYNAMIC_CONFIG_FILE_PATH=config/dynamicconfig/development-sql.yaml
      - KAFKA_SEEDS=kafka
      - VISIBILITY_DRIVER=postgres
    ports:
      - "7233:7233"
      - "8233:8233"
    healthcheck:
      test: ["CMD-SHELL", "tctl cluster health || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 30s
    restart: unless-stopped
    logging: *default-logging
    networks:
      - streaming-stack
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G

  temporal-worker:
    # NOTE: User needs to provide ./temporal-worker/Dockerfile and source code to build this service
    build:
      context: ./temporal-worker
      dockerfile: Dockerfile
    container_name: stack-temporal-worker
    hostname: temporal-worker
    depends_on:
      temporal:
        condition: service_healthy
    environment:
      - TEMPORAL_HOST=temporal:7233
      - TEMPORAL_NAMESPACE=default
      - TEMPORAL_TASK_QUEUE=kratos-task-queue
    restart: unless-stopped
    logging: *default-logging
    networks:
      - streaming-stack
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M

  kratos:
    # NOTE: User needs to provide ./kratos/Dockerfile and source code to build this service
    build:
      context: ./kratos
      dockerfile: Dockerfile
    container_name: stack-kratos
    hostname: kratos
    depends_on:
      postgres:
        condition: service_healthy
      temporal:
        condition: service_healthy
    environment:
      - KRATOS_DB_DSN=postgres://stack_user:stack_pass@postgres:5432/stack_db?sslmode=disable
      - KRATOS_TEMPORAL_HOST=temporal:7233
      - KRATOS_HTTP_PORT=8000
      - KRATOS_GRPC_PORT=9000
    ports:
      - "8000:8000"
      - "9000:9000"
    healthcheck:
      test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider http://localhost:8000/health/ready || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    restart: unless-stopped
    logging: *default-logging
    networks:
      - streaming-stack
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M

volumes:
  postgres_data:
    driver: local
  kafka_data:
    driver: local
  zookeeper_data:
    driver: local
  zookeeper_logs:
    driver: local
  flink-checkpoints:
    driver: local

networks:
  streaming-stack:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

**Startup and Verification Commands**:

```bash
# 1. Enter deployment directory
cd TECH-STACK-STREAMING-POSTGRES-TEMPORAL-KRATOS/05-deployment

# 2. Build custom images (Kratos / Temporal Worker) and start full stack in background
docker compose up -d --build

# 3. View real-time health status
docker compose ps

# 4. Track startup logs
docker compose logs -f temporal kratos

# 5. Verify Flink Web UI
open http://localhost:8081        # macOS
# xdg-open http://localhost:8081  # Linux

# 6. Verify Kratos health endpoint
curl -s http://localhost:8000/health/ready | jq .

# 7. Verify Temporal cluster health
docker compose exec temporal tctl cluster health

# 8. Stop full stack (preserve data volumes)
docker compose down

# 9. Complete cleanup (including named volumes)
docker compose down -v
```

## 7. Visualizations

The following Mermaid diagram shows the Docker Compose service dependency topology, startup order, and component classification.

```mermaid
graph TB
    subgraph Network["streaming-stack (bridge)"]
        Z["zookeeper<br/>(ZooKeeper 3.x)"]
        K["kafka<br/>(Confluent Kafka 7.6)"]
        P["postgres<br/>(PostgreSQL 16)"]
        FJ["flink-jobmanager<br/>(Flink 1.20)"]
        FT["flink-taskmanager<br/>(Flink 1.20)"]
        T["temporal<br/>(Temporal Server 1.24)"]
        TW["temporal-worker<br/>(Temporal Worker)"]
        KR["kratos<br/>(Go 1.23 + Kratos)"]
    end

    Z -->|depends_on<br/>service_healthy| K
    P -->|depends_on<br/>service_healthy| FJ
    P -->|depends_on<br/>service_healthy| T
    P -->|depends_on<br/>service_healthy| KR
    K -->|depends_on<br/>service_healthy| T
    FJ -->|depends_on<br/>service_started| FT
    T -->|depends_on<br/>service_healthy| TW
    T -->|depends_on<br/>service_healthy| KR

    style Z fill:#e1f5fe
    style K fill:#e1f5fe
    style P fill:#e8f5e9
    style FJ fill:#fff3e0
    style FT fill:#fff3e0
    style T fill:#fce4ec
    style TW fill:#fce4ec
    style KR fill:#f3e5f5
```

### Figure Notes

- **Green node** (`postgres`) is the data persistence root service, shared by three downstream components.
- **Blue nodes** (`zookeeper`, `kafka`) are message infrastructure, constituting the event bus layer.
- **Orange nodes** (`flink-jobmanager`, `flink-taskmanager`) are the stream computing engine layer.
- **Pink nodes** (`temporal`, `temporal-worker`) are the workflow orchestration layer.
- **Purple node** (`kratos`) is the microservice gateway and business logic layer, having the most incoming edges, located at the end of the topological sort, and starting last.

### 3.2 Project Knowledge Base Cross-References

The Docker Compose full-stack deployment described in this document relates to the following entries in the project knowledge base:

- [Flink Kubernetes Deployment Guide](../Flink/04-runtime/04.01-deployment/kubernetes-deployment.md) — Migration path from Docker Compose to K8s deployment
- [Flink Deployment Operations Complete Guide](../Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md) — Containerized deployment operations best practices
- [High Availability Patterns](../Knowledge/07-best-practices/07.06-high-availability-patterns.md) — High availability design patterns at the container orchestration layer
- [Performance Tuning Patterns](../Knowledge/07-best-practices/07.02-performance-tuning-patterns.md) — Association between container resource limits and performance tuning

## 8. References
