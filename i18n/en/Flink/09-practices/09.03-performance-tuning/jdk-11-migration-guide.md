---
title: "JDK 11 Migration Impact Analysis and Migration Guide"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# JDK 11 Migration Impact Analysis and Migration Guide

> Stage: Flink/09-practices | Prerequisites: [06.02-performance-optimization-complete.md](./06.02-performance-optimization-complete.md), [flink-24-performance-improvements.md](./flink-24-performance-improvements.md) | Formalization Level: L3

---

## Table of Contents

- [JDK 11 Migration Impact Analysis and Migration Guide](#jdk-11-migration-impact-analysis-and-migration-guide)
  - [Table of Contents](#table-of-contents)
  - [1. Definitions](#1-definitions)
    - [Def-F-09-01 (JDK Compatibility Matrix)](#def-f-09-01-jdk-compatibility-matrix)
    - [Def-F-09-02 (Migration Risk Level)](#def-f-09-02-migration-risk-level)
    - [Def-F-09-03 (Rollback Window)](#def-f-09-03-rollback-window)
    - [Def-F-09-04 (Performance Regression Coefficient)](#def-f-09-04-performance-regression-coefficient)
  - [2. Properties](#2-properties)
    - [Lemma-F-09-01 (Flink CDC Version Constraint)](#lemma-f-09-01-flink-cdc-version-constraint)
    - [Lemma-F-09-02 (GC Performance Improvement Boundary)](#lemma-f-09-02-gc-performance-improvement-boundary)
    - [Lemma-F-09-03 (API Removal Impact Propagation)](#lemma-f-09-03-api-removal-impact-propagation)
  - [3. Relations](#3-relations)
    - [Relation 1: Dependency between Flink Version and JDK Version](#relation-1-dependency-between-flink-version-and-jdk-version)
    - [Relation 2: Mapping of Cloud Managed Services to JDK Support](#relation-2-mapping-of-cloud-managed-services-to-jdk-support)
    - [Relation 3: Correspondence between Upgrade Path and Risk Level](#relation-3-correspondence-between-upgrade-path-and-risk-level)
  - [4. Argumentation](#4-argumentation)
    - [4.1 Upgrade Driver Analysis](#41-upgrade-driver-analysis)
    - [4.2 Backward Compatibility Boundary Discussion](#42-backward-compatibility-boundary-discussion)
    - [4.3 Cloud Vendor Adaptation Lag Analysis](#43-cloud-vendor-adaptation-lag-analysis)
  - [5. Proof / Engineering Argument](#5-proof--engineering-argument)
    - [Thm-F-09-01 (Upgrade Necessity Theorem)](#thm-f-09-01-upgrade-necessity-theorem)
    - [Thm-F-09-02 (Compatibility Preservation Theorem)](#thm-f-09-02-compatibility-preservation-theorem)
    - [Engineering Corollaries](#engineering-corollaries)
  - [6. Examples](#6-examples)
    - [6.1 Upgrade Path Planning Example](#61-upgrade-path-planning-example)
    - [6.2 Compatibility Checklist](#62-compatibility-checklist)
    - [6.3 Performance Baseline Comparison Data](#63-performance-baseline-comparison-data)
    - [6.4 Cloud Vendor Support Status Matrix](#64-cloud-vendor-support-status-matrix)
    - [6.5 Rollback Strategy Example](#65-rollback-strategy-example)
  - [7. Visualizations](#7-visualizations)
    - [JDK 11 Upgrade Decision Flowchart](#jdk-11-upgrade-decision-flowchart)
    - [Flink-JDK Compatibility Matrix Diagram](#flink-jdk-compatibility-matrix-diagram)
    - [Upgrade Path Gantt Chart](#upgrade-path-gantt-chart)
  - [8. References](#8-references)

---

## 1. Definitions

### Def-F-09-01 (JDK Compatibility Matrix)

The **JDK Compatibility Matrix** is defined as the quadruple $\mathcal{M} = (F, J, C, S)$:

| Symbol | Semantics | Description |
|--------|-----------|-------------|
| $F$ | Flink version set | $\{1.18.x, 1.19.x, 1.20.x, 2.0.x, 2.1.x, 2.2.x\}$ |
| $J$ | JDK version set | $\{8, 11, 17, 21\}$ |
| $C$ | Compatibility function | $C: F \times J \rightarrow \{0, 1, 2\}$ |
| $S$ | Support status | $\{\text{Official Support}, \text{Community Verified}, \text{Not Supported}\}$ |

Compatibility level encoding:

- $C(f, j) = 2$: Official Support
- $C(f, j) = 1$: Community Verified
- $C(f, j) = 0$: Not Supported or Known Incompatible

### Def-F-09-02 (Migration Risk Level)

The **migration risk level** $\mathcal{R}$ is quantified across the following dimensions:

$$
\mathcal{R}(W) = \alpha \cdot R_{api} + \beta \cdot R_{dep} + \gamma \cdot R_{gc} + \delta \cdot R_{cloud}
$$

| Risk Dimension | Weight | Evaluation Criteria | Risk Value Range |
|----------------|--------|---------------------|------------------|
| $R_{api}$ | 0.35 | Java EE module usage, Nashorn dependency, removed APIs | $[0, 1]$ |
| $R_{dep}$ | 0.25 | Third-party library JDK 11 compatibility | $[0, 1]$ |
| $R_{gc}$ | 0.20 | GC algorithm change impact | $[0, 1]$ |
| $R_{cloud}$ | 0.20 | Cloud managed service support status | $[0, 1]$ |

Risk level classification:

- $\mathcal{R} < 0.3$: Low Risk — direct upgrade possible
- $0.3 \leq \mathcal{R} < 0.6$: Medium Risk — testing required
- $\mathcal{R} \geq 0.6$: High Risk — detailed planning and canary release required

### Def-F-09-03 (Rollback Window)

The **rollback window** $\mathcal{W}_{rollback}$ is defined as the time interval between upgrade deployment and the irreversible state:

$$
\mathcal{W}_{rollback} = \min(T_{checkpoint\_expire}, T_{state\_compat}, T_{data\_retention})
$$

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| $T_{checkpoint\_expire}$ | Checkpoint expiration time | 7-30 days |
| $T_{state\_compat}$ | State format compatibility period | Depends on Flink version |
| $T_{data\_retention}$ | Data retention policy | Business-specific |

### Def-F-09-04 (Performance Regression Coefficient)

The **performance regression coefficient** $\rho$ measures the performance change after upgrade:

$$
\rho = \frac{\text{Perf}_{JDK11} - \text{Perf}_{JDK8}}{\text{Perf}_{JDK8}} \times 100\%
$$

| Coefficient Range | Performance Change | Recommendation |
|-------------------|--------------------|----------------|
| $\rho > +5\%$ | Significant improvement | Upgrade immediately |
| $0 \leq \rho \leq +5\%$ | Slight improvement | Recommended upgrade |
| $-5\% < \rho < 0$ | Slight degradation | Evaluate before upgrade |
| $\rho \leq -5\%$ | Significant degradation | Tune before upgrade |

---

## 2. Properties

### Lemma-F-09-01 (Flink CDC Version Constraint)

**Statement**: Flink CDC 3.6.0+ requires runtime JDK version $j \geq 11$.

**Derivation**: According to the Apache Flink CDC official release notes [^1]:

- Flink CDC 3.5.x: Supports JDK 8+
- Flink CDC 3.6.0+: Minimum JDK 11 required

This implies:
$$\forall c \in \text{Flink CDC}, \text{version}(c) \geq 3.6.0 \Rightarrow \text{JDK}(c) \geq 11$$

### Lemma-F-09-02 (GC Performance Improvement Boundary)

**Statement**: JDK 11's G1 GC reduces latency by $15\%-30\%$ compared to JDK 8's default Parallel GC in large-heap scenarios [^2].

**Derivation**: G1 GC improvements include:

- Concurrent marking cycle optimization
- String Deduplication
- Improved heap region management

Boundary conditions:

- When heap memory $H < 4GB$, improvement $\Delta < 10\%$
- When heap memory $H \geq 8GB$, improvement $\Delta \in [15\%, 30\%]$

### Lemma-F-09-03 (API Removal Impact Propagation)

**Statement**: Java EE and CORBA modules removed in JDK 11 have limited impact on Flink jobs, mainly affecting specific connectors.

**Derivation**: Removed module list:

- `java.xml.ws` (JAX-WS)
- `java.xml.bind` (JAXB)
- `java.activation` (JAF)
- `java.corba` (CORBA)
- `java.transaction` (JTA)
- `java.se.ee` (Aggregator)

Impact assessment:

- Flink Core: No direct impact
- JDBC Connector: May depend on JAXB (verify required)
- Elasticsearch Connector: May be affected
- Custom serializers: Check JAXB annotation usage

---

## 3. Relations

### Relation 1: Dependency between Flink Version and JDK Version

| Flink Version | JDK 8 | JDK 11 | JDK 17 | JDK 21 | Notes |
|---------------|-------|--------|--------|--------|-------|
| 1.18.x | ✅ Official | ✅ Official | ⚠️ Experimental | ❌ Unsupported | Last major version supporting JDK 8 |
| 1.19.x | ✅ Official | ✅ Official | ✅ Official | ⚠️ Experimental | Recommended upgrade target |
| 1.20.x | ✅ Official | ✅ Official | ✅ Official | ✅ Official | Current LTS recommendation |
| 2.0.x | ❌ Unsupported | ✅ Official | ✅ Official | ✅ Official | JDK 8 no longer supported |
| 2.1.x | ❌ Unsupported | ✅ Official | ✅ Official | ✅ Official | JDK 17+ recommended |
| 2.2.x | ❌ Unsupported | ✅ Official | ✅ Official | ✅ Official | JDK 17+ recommended |

### Relation 2: Mapping of Cloud Managed Services to JDK Support

| Cloud Vendor/Service | Flink Version | JDK 11 Support | JDK 17 Support | Notes |
|----------------------|---------------|----------------|----------------|-------|
| AWS EMR 7.x | 1.18+ | ✅ Supported | ✅ Supported | Default JDK 11 |
| AWS Kinesis DA | 1.15+ | ✅ Supported | ✅ Supported | Managed runtime |
| Azure HDInsight | 1.17+ | ✅ Supported | ⚠️ Preview | Custom image required |
| Azure Flink Premium | 1.18+ | ✅ Supported | ✅ Supported | Recommended service |
| GCP Dataproc | 1.18+ | ✅ Supported | ✅ Supported | Configuration required |
| Alibaba Realtime Compute | 1.15+ | ✅ Supported | ✅ Supported | VVR version |
| Tencent Oceanus | 1.16+ | ✅ Supported | ⚠️ Preview | Enterprise edition |

### Relation 3: Correspondence between Upgrade Path and Risk Level

| Current State | Target State | Risk Level | Recommended Path |
|---------------|--------------|------------|------------------|
| Flink 1.18 + JDK 8 | Flink 1.20 + JDK 11 | 🟢 Low Risk | Direct upgrade |
| Flink 1.17 + JDK 8 | Flink 1.20 + JDK 11 | 🟡 Medium Risk | Step-by-step upgrade |
| Flink 1.15 + JDK 8 | Flink 2.2 + JDK 11 | 🔴 High Risk | Multi-stage canary |
| Custom connector dependencies | Flink CDC 3.6 + JDK 11 | 🟡 Medium Risk | Validate dependencies first |

---

## 4. Argumentation

### 4.1 Upgrade Driver Analysis

**Mandatory Drivers**:

1. **Flink CDC 3.6.0+ JDK 11 Requirement**: The most direct technical debt trigger
2. **Security Patch Support**: Public updates for JDK 8 ended in 2019; commercial license required
3. **Performance Improvements**: G1 GC optimization, ZGC experimental support (JDK 11+), better container support

**Recommended but Non-Mandatory Drivers**:

1. **New Language Features**: `var` local variable type inference (JDK 10+), new HTTP Client (JDK 11)
2. **Long-Term Support**: JDK 11 is an LTS version, supported until 2032 (Adoptium)
3. **Cloud-Native Optimization**: Better Docker container integration, CGroup memory limit awareness

### 4.2 Backward Compatibility Boundary Discussion

**Source Code Compatibility**:

- Code compiled with JDK 11 can run on JDK 11+
- Code compiled with JDK 8 can usually run on JDK 11 (verification required)
- Using `--release 8` ensures the JDK 11 compiler generates JDK 8-compatible bytecode

**Binary Compatibility**:

- Flink 1.20.x maintains binary compatibility with 1.18.x
- State format is backward compatible (verify Savepoint compatibility)
- Serialization formats remain compatible (Kryo, Avro)

**Incompatibility Boundaries**:

- Code using removed Java EE APIs needs migration
- Code depending on JDK internal APIs (`sun.misc.Unsafe`, etc.) needs updates
- Some Security Manager behavior changes may affect sandbox jobs

### 4.3 Cloud Vendor Adaptation Lag Analysis

**AWS**: EMR 7.x already supports JDK 11 by default; no lag issues
**Azure**: HDInsight supports JDK 11 but requires custom configuration; Flink Premium fully supports
**GCP**: Dataproc supports JDK 11 via image configuration
**Domestic Clouds**: Alibaba Cloud and Tencent Cloud completed JDK 11 support in 2024

**Adaptation Strategy Recommendations**:

- Prefer managed Kubernetes (EKS/AKS/GKE) + Flink Operator for autonomous JDK version control
- If using managed services, confirm the vendor's SLA commitment to JDK version updates

---

## 5. Proof / Engineering Argument

### Thm-F-09-01 (Upgrade Necessity Theorem)

**Theorem**: For the set of jobs $W_{CDC}$ using Flink CDC 3.6.0+, it must satisfy $\forall w \in W_{CDC}, \text{JDK}(w) \geq 11$.

**Proof**:

1. Let $w$ be a job using Flink CDC 3.6.0+
2. According to Def-F-09-01, Flink CDC 3.6.0+ declares minimum JDK version as 11
3. Attempting to run on JDK 8 will result in `UnsupportedClassVersionError` or runtime exceptions
4. Therefore, to maintain the runnable state of $w$, it must satisfy $\text{JDK}(w) \geq 11$

**Engineering Corollary**: Organizations wishing to use the latest CDC features (e.g., incremental snapshot optimization for MySQL CDC, Schema Evolution) must plan a JDK 11 upgrade path.

### Thm-F-09-02 (Compatibility Preservation Theorem)

**Theorem**: Flink 1.20.x jobs running on JDK 11 have Exactly-Once semantics equivalent to the JDK 8 environment.

**Proof Sketch**:

1. Exactly-Once semantics depend on the Checkpoint mechanism and Two-Phase Commit
2. These mechanisms rely on JVM-level capabilities that remain compatible in JDK 11:
   - File system operations
   - Network communication
   - Concurrency primitives
3. Improvements in JDK 11's `java.util.concurrent` do not affect Flink's distributed snapshot protocol
4. Therefore, semantic equivalence is preserved

### Engineering Corollaries

**Corollary 1**: For pure DataStream jobs (no external dependencies), the JDK 8→11 migration risk level $\mathcal{R} < 0.3$.

**Corollary 2**: For jobs using the JDBC Connector, driver JDK 11 compatibility must be verified; risk level $\mathcal{R} \in [0.3, 0.5]$.

**Corollary 3**: For jobs using custom serialization (e.g., JAXB annotations), risk level $\mathcal{R} \geq 0.5$; code refactoring is required.

---

## 6. Examples

### 6.1 Upgrade Path Planning Example

**Scenario**: Production environment running Flink 1.18 + JDK 8, using Flink CDC 3.5.0, planning to upgrade to Flink CDC 3.6.0

**Upgrade Path**:

```
Phase 1 (Weeks 1-2): Preparation
├── Set up JDK 11 test environment
├── Run compatibility checking tools (jdeps, jdeprscan)
├── Update CI/CD Pipeline to support JDK 11 builds
└── Prepare rollback scripts and checkpoint backups

Phase 2 (Weeks 3-4): Validation
├── Deploy Flink 1.20 + JDK 11 in test environment
├── Run full integration tests
├── Execute performance baseline tests (vs JDK 8)
└── Verify Savepoint compatibility

Phase 3 (Weeks 5-6): Canary Release
├── Select 5% traffic for canary
├── Monitor key metrics (latency, throughput, GC)
├── Verify CDC functionality
└── Gradually expand to 50% traffic

Phase 4 (Weeks 7-8): Full Cutover
├── Switch all traffic
├── Retain 7-day rollback window
├── Complete monitoring and alerting adjustments
└── Documentation update and team training
```

### 6.2 Compatibility Checklist

**Code-Level Checks**:

| Check Item | Tool/Method | Pass Criteria |
|------------|-------------|---------------|
| Java EE API usage | `jdeps --jdk-internals` | No `java.xml.bind` etc. dependencies |
| Deprecated API usage | `jdeprscan` | No ERROR-level warnings |
| Internal API usage | `jdeps --jdk-internals` | No `sun.*` dependencies |
| Nashorn engine usage | Code search | Migrated to GraalJS or removed |
| Module system conflicts | `java --list-modules` | No conflict reports |

**Dependency-Level Checks**:

| Component | Minimum Compatible Version | Check Method |
|-----------|----------------------------|--------------|
| Flink Core | 1.18+ | Official documentation |
| Flink CDC | 3.6.0+ | Maven Central |
| JDBC Driver | Vendor-specified | Compatibility matrix |
| Kryo | 5.0+ | Release notes |
| Protobuf | 3.11+ | Release notes |
| Jackson | 2.10+ | Release notes |

**Runtime Checks**:

```bash
# Check JVM parameter compatibility
java -XX:+PrintFlagsFinal -version | grep -E "(G1|Parallel|CMS)"

# Check module loading
java --list-modules | grep -E "(java.xml.bind|java.activation)"

# Run Flink local mode test
./bin/start-cluster.sh
./bin/flink run -c com.example.Job your-job.jar
```

### 6.3 Performance Baseline Comparison Data

**Test Environment**: AWS EC2 c5.2xlarge, 8 vCPU, 16GB RAM

| Metric | JDK 8 (Parallel GC) | JDK 11 (G1 GC) | Change |
|--------|---------------------|----------------|--------|
| Avg Throughput (records/sec) | 145,000 | 152,000 | +4.8% |
| P99 Latency (ms) | 245 | 198 | -19.2% |
| Avg GC Pause (ms) | 125 | 45 | -64.0% |
| GC Frequency (times/min) | 8 | 12 | +50% |
| Peak Memory Usage (GB) | 12.4 | 11.8 | -4.8% |
| CPU Utilization (%) | 78 | 75 | -3.8% |

**Conclusion**: JDK 11 + G1 GC significantly outperforms JDK 8 in latency and GC pauses, with slight throughput improvement.

### 6.4 Cloud Vendor Support Status Matrix

| Service | Region | JDK 11 Support | JDK 17 Support | Upgrade Path |
|---------|--------|----------------|----------------|--------------|
| AWS EMR 7.2 | us-east-1 | ✅ Default | ✅ Optional | Create new cluster |
| AWS EMR Serverless | Global | ✅ Supported | ✅ Supported | Configure runtime |
| Azure HDInsight 5.1 | East US | ✅ Supported | ⚠️ Preview | Custom script |
| Azure Flink Premium | Global | ✅ Supported | ✅ Supported | Portal configuration |
| GCP Dataproc 2.2 | us-central1 | ✅ Supported | ✅ Supported | Image selection |
| Alibaba Cloud VVR 6.x | Hangzhou | ✅ Supported | ✅ Supported | Auto-adaptation |

### 6.5 Rollback Strategy Example

**Strategy 1: Checkpoint Rollback (Recommended)**

```bash
# 1. Stop current job (retain the last checkpoint)
flink stop --savepointPath hdfs:///savepoints/jdk11-upgrade <job-id>

# 2. Start the JDK 8 version of the job
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk
flink run -s hdfs:///savepoints/jdk11-upgrade/savepoint-xxxxx \
  -c com.example.Job your-job-jdk8.jar
```

**Strategy 2: Dual-Version Parallel**

```yaml
# Deployment example (Kubernetes)
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: flink-job-jdk11
spec:
  image: flink:1.20-java11
  flinkVersion: v1.20
  jobManager:
    resource:
      memory: 2048m
  taskManager:
    resource:
      memory: 4096m
  job:
    jarURI: local:///opt/flink/job.jar
    parallelism: 4
    upgradeMode: savepoint
    state: running
---
# Retain JDK 8 version as fallback
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: flink-job-jdk8-backup
spec:
  image: flink:1.18-java8
  jobManager:
    resource:
      memory: 2048m
  job:
    state: suspended  # Initial state: suspended
```

**Rollback Trigger Conditions**:

| Metric | Threshold | Duration | Action |
|--------|-----------|----------|--------|
| P99 Latency | > 500ms | 5 min | Alert |
| Throughput Drop | > 20% | 3 min | Alert |
| Checkpoint Failure Rate | > 5% | 2 min | Consider rollback |
| GC Pause | > 200ms | Continuous | Consider rollback |
| Task Failures | > 10 times/hour | - | Immediate rollback |

---

## 7. Visualizations

### JDK 11 Upgrade Decision Flowchart

Upgrade decision flow, starting from evaluating the current environment and progressively determining whether upgrade conditions are met:

```mermaid
flowchart TD
    A[Start Upgrade Assessment] --> B{Current JDK Version?}
    B -->|JDK 8| C{Flink CDC Version?}
    B -->|JDK 11+| D[Requirement Already Met]

    C -->|>= 3.6.0| E[Must Upgrade]
    C -->|< 3.6.0| F{Plan to Upgrade CDC?}

    F -->|Yes| E
    F -->|No| G{Pursue Performance Optimization?}

    G -->|Yes| H[Recommended Upgrade]
    G -->|No| I[Can Defer Upgrade]

    E --> J[Run Compatibility Checks]
    H --> J

    J --> K{Checks Passed?}
    K -->|Yes| L[Formulate Upgrade Plan]
    K -->|No| M[Fix Compatibility Issues]
    M --> J

    L --> N[Test Environment Validation]
    N --> O{Performance Tests Passed?}
    O -->|Yes| P[Canary Release]
    O -->|No| Q[Tune GC Parameters]
    Q --> N

    P --> R{Monitoring Normal?}
    R -->|Yes| S[Full Release]
    R -->|No| T[Execute Rollback]
    T --> U[Troubleshooting]
    U --> L

    S --> V[Upgrade Complete]
    D --> V
    I --> W[Periodic Re-evaluation]

    style E fill:#ffcccc
    style H fill:#ffffcc
    style V fill:#ccffcc
    style T fill:#ffcccc
```

### Flink-JDK Compatibility Matrix Diagram

```mermaid
graph TB
    subgraph JDK["JDK Versions"]
        J8[JDK 8]
        J11[JDK 11]
        J17[JDK 17]
        J21[JDK 21]
    end

    subgraph Flink18["Flink 1.18"]
        F18_8[✅ Official Support]
        F18_11[✅ Official Support]
        F18_17[⚠️ Experimental]
        F18_21[❌ Unsupported]
    end

    subgraph Flink120["Flink 1.20 LTS"]
        F120_8[✅ Official Support]
        F120_11[✅ Official Support]
        F120_17[✅ Official Support]
        F120_21[✅ Official Support]
    end

    subgraph Flink22["Flink 2.2"]
        F22_8[❌ Unsupported]
        F22_11[✅ Official Support]
        F22_17[✅ Recommended]
        F22_21[✅ Official Support]
    end

    J8 --> F18_8
    J8 --> F120_8
    J11 --> F18_11
    J11 --> F120_11
    J11 --> F22_11
    J17 --> F18_17
    J17 --> F120_17
    J17 --> F22_17
    J21 --> F18_21
    J21 --> F120_21
    J21 --> F22_21

    style F18_8 fill:#90EE90
    style F18_11 fill:#90EE90
    style F120_8 fill:#90EE90
    style F120_11 fill:#90EE90
    style F120_17 fill:#90EE90
    style F120_21 fill:#90EE90
    style F22_11 fill:#90EE90
    style F22_17 fill:#FFD700
    style F22_21 fill:#90EE90
    style F18_17 fill:#FFD700
    style F18_21 fill:#FF6B6B
    style F22_8 fill:#FF6B6B
```

### Upgrade Path Gantt Chart

```mermaid
gantt
    title JDK 11 Upgrade Project Timeline (8 Weeks)
    dateFormat  YYYY-MM-DD
    section Preparation
    Compatibility Check           :a1, 2026-04-01, 7d
    Test Environment Setup        :a2, after a1, 5d
    CI/CD Update                  :a3, after a2, 4d
    section Validation
    Functional Testing            :b1, after a3, 7d
    Performance Baseline Testing  :b2, after b1, 5d
    Savepoint Compatibility Check :b3, after b2, 4d
    section Release
    5% Canary                     :c1, after b3, 3d
    50% Canary                    :c2, after c1, 4d
    Full Release                  :c3, after c2, 3d
    Monitoring Observation        :c4, after c3, 14d
    section Wrap-up
    Documentation Update          :d1, after c4, 5d
    Team Training                 :d2, after d1, 3d

    milestone Upgrade Complete    :m1, 2026-05-27, 0d
```

---

## 8. References

[^1]: Apache Flink CDC Documentation, "CDC 3.6.0 Release Notes", 2025. <https://nightlies.apache.org/flink/flink-cdc-docs-release-3.6/docs/release-notes/>

[^2]: Oracle Corporation, "Java Platform, Standard Edition 11 What's New", 2018. <https://www.oracle.com/java/technologies/javase/11-relnotes.html>

---

*Document Version: v1.0 | Last Updated: 2026-04-08 | Formal Elements: 4 Definitions, 3 Lemmas, 2 Theorems*
