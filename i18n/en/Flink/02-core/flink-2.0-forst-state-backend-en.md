# Flink 2.0 ForSt State Backend - VLDB 2025 Deep Dive

> **Language**: English | **Translated from**: Flink/02-core/flink-2.0-forst-state-backend.md | **Translation date**: 2026-04-20
> **Status**: ✅ Released (2025-03-24)
> **Flink Version**: 2.0.0+
> **Stability**: Stable
>
> **Stage**: Flink/02-core-mechanisms | **Prerequisites**: [forst-state-backend.md](./forst-state-backend.md), [disaggregated-state-analysis.md](../01-concepts/disaggregated-state-analysis.md) | **Formalization Level**: L4

---

## 1. Definitions

### Def-F-02-61: ForSt Storage Engine

**Definition**: ForSt (For Streaming) is a **Disaggregated State Backend** introduced in Apache Flink 2.0, designed specifically for large-scale stream processing scenarios. It thoroughly decouples compute and storage, achieving an architectural paradigm of "stateless compute nodes, remotely centralized state storage".

$$
\text{ForSt} = \langle \text{LSM}_{\text{abstract}}, \text{UFS}, \text{Cache}_{\text{local}}, \text{Compaction}_{\text{remote}}, \text{Sync}_{\text{policy}} \rangle
$$

Where:

| Component | Description | Responsibility |
|------|------|------|
| $\text{LSM}_{\text{abstract}}$ | LSM-Tree abstraction layer | Unified state data organization structure |
| $\text{UFS}$ | Unified File System | Unified file system interface, shielding underlying storage differences |
| $\text{Cache}_{\text{local}}$ | Local cache layer | Memory + local disk two-tier cache |
| $\text{Compaction}_{\text{remote}}$ | Remote Compaction service | Offload Compaction to dedicated clusters |
| $\text{Sync}_{\text{policy}}$ | Sync policy | Write-through/write-back policy control |

**Core Design Goals**:

1. **Compute-Storage Separation**: State is not bound to TaskManager, supporting instant failure recovery
2. **Lightweight Checkpoint**: Through file hard link sharing, Checkpoint time approaches constant time
3. **Elastic Scaling**: No state migration required, compute resources can scale independently
4. **Cost Optimization**: Utilize inexpensive object storage to replace local SSD, reducing storage cost by 50%

**Source Code Implementation**:

```java
// Main class: org.apache.flink.runtime.state.forst.ForStStateBackend
// Config: org.apache.flink.runtime.state.forst.ForStOptions
// Config builder: org.apache.flink.runtime.state.forst.ForStStateBackendConfig
```

- Located in: `flink-runtime` module (`flink-state-backends/flink-state-backend-forst`)
- Flink official docs: <https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/state_backends/>
- FLIP paper: VLDB 2025 "ForSt: A Disaggregated State Backend for Stream Processing"

### Def-F-02-62: Unified File System Layer (UFS)

**Definition**: UFS is ForSt's unified storage abstraction layer, providing consistent access interfaces across S3, GCS, Azure Blob, and HDFS, supporting atomic operations and multi-version management.

$$
\text{UFS} = \langle \text{StorageBackend}, \text{PathResolver}, \text{AtomicOps}, \text{Versioning}, \text{Consistency} \rangle
$$

**UFS Operation Semantics**:

| Operation | Semantics | Atomicity Guarantee |
|------|------|-----------|
| `put(key, data)` | Write object | All-or-nothing |
| `get(key)` | Read object | Read-after-write consistency |
| `delete(key)` | Delete object | Atomic |
| `list(prefix)` | List objects | Prefix consistent |
| `copy(src, dst)` | Copy object | Metadata atomic |

**Key Feature - Hard Link Semantics**:

ForSt leverages UFS's Copy-on-Write feature to implement Checkpoint hard link sharing:

$$
\forall f \in \text{SSTFiles}: \text{checkpoint}_i(f) = \begin{cases}
\text{reference}(f) & \text{if } f \text{ unmodified} \\
\text{new}(f') & \text{if } f \text{ modified}
\end{cases}
$$

This enables Checkpoint to only persist references to changed files, rather than full data copies.

### Def-F-02-63: Disaggregated Storage Architecture

**Definition**: Disaggregated storage is an architectural pattern that decouples local storage on compute nodes from persistent storage, where remote storage serves as the primary storage and local storage acts only as a performance acceleration layer.

$$
\text{DisaggregatedStorage} = (\mathcal{C}_{\text{mem}}, \mathcal{C}_{\text{disk}}, \mathcal{R}, \eta, \gamma)
$$

Where:

- $\mathcal{C}_{\text{mem}}$: Memory cache (L1 Cache)
- $\mathcal{C}_{\text{disk}}$: Local disk cache (L2 Cache)
- $\mathcal{R}$: Remote object storage (Main Storage)
- $\eta$: Cache replacement policy (LRU/SLRU/W-TinyLFU)
- $\gamma$: Prefetch policy (Predictive Prefetching)

**Storage Tier Hierarchy**:

```
┌─────────────────────────────────────────────────────────────┐
│                    ForSt Storage Tiers                       │
├─────────────────────────────────────────────────────────────┤
│  L1 Cache (Memory)     │  Hot data, μs-level access, limited capacity        │
│  L2 Cache (Local SSD)  │  Warm data, ms-level access, TB-level capacity      │
│  Main Storage (UFS)    │  Full data, 10ms-level access, unlimited scaling    │
└─────────────────────────────────────────────────────────────┘
```

**Data Flow**:

$$
\text{Write}: \text{Operator} \rightarrow \mathcal{C}_{\text{mem}} \xrightarrow{\text{async}} \mathcal{R}
$$

$$
\text{Read}: \text{Operator} \rightarrow \mathcal{C}_{\text{mem}} \xrightarrow{\text{miss}} \mathcal{C}_{\text{disk}} \xrightarrow{\text{miss}} \mathcal{R} \rightarrow \mathcal{C}_{\text{disk}} \rightarrow \mathcal{C}_{\text{mem}}
$$

### Def-F-02-64: Instant Recovery Mechanism

**Definition**: Instant recovery is ForSt's failure recovery strategy, allowing TaskManager to begin processing immediately after loading only Checkpoint metadata, with state data loaded on-demand asynchronously.

**Formal Description**:

Let Checkpoint $C$ contain metadata $M$ and state data $S = \{s_1, s_2, ..., s_n\}$.

Traditional recovery time:

$$
T_{\text{traditional}} = T_{\text{metadata}} + \sum_{i=1}^{n} T_{\text{download}}(s_i) + T_{\text{load}}
$$

Instant recovery time:

$$
T_{\text{instant}} = T_{\text{metadata}} + \epsilon \quad \text{where } \epsilon \approx 0
$$

**Lazy Load Guarantee**:

For first access to state key $k$:

$$
\text{access}(k) \Rightarrow \begin{cases}
\text{if } k \in \mathcal{C}: & \text{directRead}(k) \\
\text{if } k \notin \mathcal{C}: & \text{blockUntil}(\text{fetch}(k, \mathcal{R}) \rightarrow \mathcal{C})
\end{cases}
$$

**Prefetch Optimization**:

Prefetch strategy based on access pattern prediction:

$$
\text{prefetch}(K_{\text{predicted}}) = \{ k \mid P(\text{access}(k) \mid \text{history}) > \theta \}
$$

### Def-F-02-65: Remote Compaction Service

**Definition**: Remote Compaction is a mechanism that offloads LSM-Tree Compaction operations to independent compute clusters, freeing TaskManager CPU and I/O resources.

$$
\text{RemoteCompaction} = \langle \text{Scheduler}, \text{WorkerPool}, \text{TaskQueue}, \text{VersionManager} \rangle
$$

**Compaction Task Lifecycle**:

```
TaskManager                          Compaction Service
     │                                       │
     │── 1. Submit Compaction Task ─────────>│
     │   (input files, target level)         │
     │                                       │
     │                               ┌───────┴───────┐
     │                               │  Worker Pool  │
     │                               │  ┌─────────┐  │
     │                               │  │ Compact │  │
     │                               │  │  SSTs   │  │
     │                               │  └────┬────┘  │
     │                               └───────┼───────┘
     │                                       │
     │<─ 2. Return Output Files ─────────────│
     │   (new SSTs with version)             │
     │                                       │
     │── 3. Update Metadata ────────────────>│
     │   (atomic switch)                     │
```

**Resource Decoupling Benefit**:

$$
\text{Resource}_{\text{TM}} = \text{Resource}_{\text{compute}} \perp \text{Resource}_{\text{compaction}}
$$

---

## 2. Properties

### Prop-F-02-21: Checkpoint Time Complexity Bound

**Proposition**: ForSt's Checkpoint time complexity is $O(1)$ (constant time), independent of state size.

**Proof Sketch**:

Let state size be $|S|$, and changes since last Checkpoint be $|\Delta S|$.

**RocksDB Incremental Checkpoint**:

$$
T_{\text{rocksdb}} = O(|\Delta S_{\text{local}}|) + T_{\text{upload}}(|\Delta S|) + T_{\text{metadata}}
$$

Where $T_{\text{upload}}$ grows linearly with state size.

**ForSt Checkpoint**:

$$
T_{\text{forst}} = T_{\text{flush}}^{\text{async}} + T_{\text{metadata}} \approx O(1)
$$

Because:

1. State files are already in UFS, no upload needed
2. New versions are only created when files are modified
3. Checkpoint only persists metadata reference list

**File Sharing Mechanism**:

$$
\forall f \in \text{SSTFiles}: \text{unchanged}(f) \Rightarrow \text{reference}_{c_{i+1}}(f) = \text{reference}_{c_i}(f)
$$

### Prop-F-02-22: Recovery Speed Improvement Bound

**Proposition**: Using instant recovery, failure recovery speed improves by $O(|S| / |S_{\text{hot}}|)$ times compared to traditional recovery.

**Proof**:

Traditional recovery requires downloading full state:

$$
T_{\text{traditional}} = \frac{|S|}{B_{\text{network}}} + T_{\text{load}}
$$

Instant recovery only needs to load metadata, with state loaded on-demand:

$$
T_{\text{instant}} = T_{\text{metadata}} + \frac{|S_{\text{hot}}|}{B_{\text{network}}}
$$

Where $|S_{\text{hot}}| \ll |S|$ is the actually accessed hot data subset.

**Speedup**:

$$
\text{Speedup} = \frac{T_{\text{traditional}}}{T_{\text{instant}}} \approx \frac{|S|}{|S_{\text{hot}}|}
$$

In production environments, $|S_{\text{hot}}| / |S| \approx 1\% - 5\%$, so speedup can reach **20x - 100x**.

### Lemma-F-02-23: Cost Optimization Lower Bound

**Lemma**: Adopting ForSt disaggregated storage can reduce state storage cost by at least 50%.

**Cost Model**:

**RocksDB Cost** (local SSD):

$$
\text{Cost}_{\text{rocksdb}} = |S| \times C_{\text{ssd}} \times R_{\text{replication}} \times T_{\text{reserved}}
$$

Where:

- $C_{\text{ssd}} \approx \$0.10/\text{GB}/\text{month}$
- $R_{\text{replication}} = 2$ (high availability requires dual replicas)
- $T_{\text{reserved}} = 1.5$ (reserved capacity)

**ForSt Cost** (object storage + local cache):

$$
\text{Cost}_{\text{forst}} = |S| \times C_{\text{object}} + (0.1 \times |S|) \times C_{\text{ssd}}
$$

Where:

- $C_{\text{object}} \approx \$0.023/\text{GB}/\text{month}$
- $0.1 \times |S|$ is 10% hot data local cache

**Cost Comparison**:

$$
\frac{\text{Cost}_{\text{forst}}}{\text{Cost}_{\text{rocksdb}}} = \frac{0.023 + 0.1 \times 0.10}{0.10 \times 2 \times 1.5} = \frac{0.033}{0.30} \approx 0.11
$$

Considering network transfer and request fees, actual cost reduction is about **50-70%**.

### Prop-F-02-24: Seamless Reconfiguration Guarantee

**Proposition**: ForSt supports seamless scaling without state migration; scaling time is $O(1)$.

**Proof**:

Since state is stored in UFS rather than locally, TaskManager scaling does not involve state migration:

$$
\forall TM_{\text{old}}, TM_{\text{new}}: \text{State}(TM_{\text{old}}) = \text{State}(TM_{\text{new}}) = \mathcal{R}
$$

When a new TaskManager starts:

1. Load Checkpoint metadata (constant time)
2. Begin processing immediately
3. Load state from UFS on-demand

Therefore scaling time is independent of state size:

$$
T_{\text{scale}} = T_{\text{metadata}} + T_{\text{schedule}} = O(1)
$$

---

## 3. Relations

### 3.1 ForSt and RocksDB Evolution Relationship

ForSt inherits and extends RocksDB's LSM-Tree core, but undergoes cloud-native architectural refactoring:

| Dimension | RocksDB | ForSt | Difference |
|------|---------|-------|------|
| **Storage location** | Local disk primary | UFS primary, local as cache | Compute-storage decoupling |
| **Checkpoint** | Local snapshot → upload DFS | Metadata snapshot (files already in UFS) | 94% time reduction |
| **Compaction** | Local execution | Remote service execution | CPU resource release |
| **Recovery** | Full download → start | Metadata load → instant start | 49x speedup |
| **Capacity limit** | Limited by local disk | Theoretically unlimited | Elastic scaling |
| **Cost model** | Local SSD reservation | Object storage on-demand | 50% cost reduction |

**Evolution Formula**:

$$
\text{ForSt} = \text{RocksDB}^{\text{core}} + \text{UFS Layer} + \text{Remote Compaction} + \text{Instant Recovery} + \text{Predictive Cache}
$$

### 3.2 Mapping to Dataflow Model

ForSt is an efficient implementation of the **Exactly-Once** semantics in the Dataflow Model:

```
Dataflow Model          ForSt Implementation
─────────────────────────────────────────────────
Windowed State    →     SST Files in UFS
Trigger           →     Checkpoint Barrier
Accumulation      →     Incremental SST Update (Hard Link)
Discarding        →     Reference Counting + GC
```

**Consistency Guarantees**:

ForSt guarantees Dataflow Model consistency requirements through the following mechanisms:

1. **Barrier alignment**: Checkpoint Barrier global alignment guarantees snapshot consistency
2. **Two-phase commit**: Checkpoint prepare → commit protocol guarantees atomicity
3. **File immutability**: SST files are immutable once written, supporting multi-versioning

### 3.3 Integration with State V2 API

Flink 2.0's State V2 API is deeply integrated with ForSt:

```java
// [Pseudo-code snippet - not directly runnable] Shows core logic only
// State V2 API with ForSt Backend
StateDescriptor<V> descriptor = StateDescriptor
    .<V>builder("my-state", TypeInformation.of(V.class))
    .withOptions(StateOptions.builder()
        .withDisaggregatedStorage(true)
        .withPrefetchPolicy(PrefetchPolicy.PREDICTIVE)
        .withConsistencyLevel(ConsistencyLevel.EVENTUAL)
        .build())
    .build();
```

**API Feature Mapping**:

| State V2 API Feature | ForSt Implementation | Performance Impact |
|------------------|-----------|---------|
| `AsyncState` | Async UFS read/write | 3x throughput improvement |
| `TTL` | SST-level expiration eviction | Storage efficiency improvement |
| `Queryable State` | Query directly from UFS | Query latency 10-100ms |

---

## 4. Argumentation

### 4.1 Necessity Argument for Disaggregated Storage

**Core Contradictions of Traditional Architecture**:

In large-scale stream processing scenarios, the Flink 1.x + RocksDB architecture faces three irreconcilable contradictions:

**Contradiction 1: Capacity Elasticity and Cost**

$$
\text{Capacity}_{\text{rocksdb}} = \sum_{i=1}^{N} \text{Disk}(TM_i) = \text{Fixed}
$$

- State growth requires TaskManager pre-scaling
- Local SSD cost is 4-5x that of object storage
- Reserved capacity utilization is low (average < 40%)

**Contradiction 2: Checkpoint Time and State Size**

$$
T_{\text{checkpoint}} \propto |S|
$$

- Large-state job Checkpoint can take several minutes
- Synchronous phase blocks data processing, causing backpressure
- Checkpoint interval forced to lengthen, affecting recovery granularity

**Contradiction 3: Recovery Speed and Resource Cost**

$$
T_{\text{recovery}} = \frac{|S|}{B_{\text{network}}} \quad \text{vs} \quad \text{Cost}_{\text{standby}} = N_{\text{standby}} \times C_{\text{tm}}
$$

- Fast recovery requires pre-provisioned Standby TaskManagers
- Idle resources cause significant waste

**Disaggregated Architecture Solutions**:

| Problem | Traditional Solution | Disaggregated Solution | Benefit |
|------|----------|-----------|------|
| Storage cost | Local SSD $0.10/GB | Object storage $0.023/GB | **-50%** |
| Checkpoint time | $O(\|S\|)$ | $O(1)$ | **-94%** |
| Recovery time | Minutes | Seconds | **49x** |
| Resource elasticity | Tight coupling | Independent scaling | Pay-as-you-go |

### 4.2 Lightweight Checkpoint Principle

**Challenge**: How to guarantee Checkpoint consistency without copying full state?

**ForSt Solution - Hard Link Sharing**:

```
Checkpoint N:     [SST-v1] [SST-v2] [SST-v3]
                      │        │        │
                      └────────┴────────┘
                         Reference
                              │
Checkpoint N+1:   [SST-v1] [SST-v2] [SST-v3'] (v3 modified)
                      │        │        │
                      └────────┴────────┘
                      Shared   Shared   New
```

**Consistency Guarantees**:

1. **Copy-on-Write (COW)**: Create new copy before modifying SST
2. **Atomic rename**: Metadata update completes atomically
3. **Reference counting**: Garbage collect old versions with no references

### 4.3 Boundary Discussion

**Applicable Scenario Boundaries**:

| Scenario Feature | Recommended Solution | Reason |
|----------|----------|------|
| State < 10GB, low latency < 1ms | RocksDB | Avoid network overhead |
| State > 50GB, frequent Checkpoint | **ForSt** | Checkpoint efficiency advantage |
| Highly localized state access | **ForSt** | Cache hit rate > 90% |
| Randomly distributed state access | Hybrid strategy | Pre-load hot data |
| Network bandwidth limited (< 1Gbps) | RocksDB | Avoid network bottleneck |
| Multi-AZ/cross-region deployment | **ForSt** | State accessed nearby |
| Cloud-native/K8s environment | **ForSt** | Compute elastic scaling |

**Inapplicable Scenarios**:

- Ultra-low latency requirements (< 1ms P99) strict real-time scenarios
- Edge computing environments with severely limited network bandwidth
- Simple jobs with very small state (< 100MB)

---

## 5. Proof / Engineering Argument

### Thm-F-02-45: ForSt Checkpoint Consistency Theorem

**Theorem**: Under the premise that UFS provides atomic rename and read-after-write consistency, ForSt's lightweight Checkpoint mechanism guarantees that the recovered state is consistent with the state at Checkpoint time.

**Formal Statement**:

Let:

- $S_t$: state at time $t$
- $C_i$: the $i$-th Checkpoint
- $\text{restore}(C_i)$: state recovered from $C_i$

Then:

$$
\forall i: \text{restore}(C_i) = S_{t_i}
$$

Where $t_i$ is the Checkpoint time corresponding to $C_i$.

**Proof**:

**Base Assumptions**:

1. UFS guarantee: if file $f$ write completes (close), subsequent reads get complete content
2. Atomic rename: rename operation is atomic; no intermediate state with partial rename is observable
3. SST file immutability: once created, files cannot be modified; updates only via creating new versions

**Inductive Steps**:

**Step 1 - SST File Layer**:

For any SST file $f$:

$$
\text{write}(f) \Rightarrow \text{create}(f_{\text{temp}}) \rightarrow \text{write}(f_{\text{temp}}, \text{data}) \rightarrow \text{rename}(f_{\text{temp}}, f)
$$

By atomic rename guarantee, at any moment readers either see the complete old file or the complete new file.

**Step 2 - Metadata Layer**:

Checkpoint metadata $M_i$ contains:

$$
M_i = \{ (f_j, \text{version}_j, \text{checksum}_j) \mid f_j \in \text{SSTFiles}_i \}
$$

Metadata file itself is persisted through atomic write:

$$
\text{persist}(M_i) \Rightarrow \text{atomicWrite}(M_i) \Rightarrow \text{all-or-nothing}
$$

**Step 3 - Recovery Process**:

During recovery:

1. Read metadata $M_i$, obtain SST file list
2. By UFS consistency guarantee, read SST files are consistent with Checkpoint time
3. Verify file integrity through checksum

Therefore:

$$
\text{restore}(C_i) = \bigcup_{f \in M_i} \text{read}(f) = S_{t_i}
$$

**QED** ∎

### Thm-F-02-46: Instant Recovery Correctness Theorem

**Theorem**: The computation results after instant recovery are consistent with the results after full recovery followed by execution.

**Proof**:

Need to prove: for any key $k$'s access sequence, instant recovery behavior is equivalent to full recovery.

**Case Analysis**:

**Case 1 - $k \in \mathcal{C}_{\text{mem}}$ (memory cache hit)**:

Direct read from local cache, behavior consistent with full recovery.

**Case 2 - $k \in \mathcal{C}_{\text{disk}}$ (disk cache hit)**:

Read from local disk, slightly higher latency but semantically consistent.

**Case 3 - $k \in \mathcal{R}$ (needs remote load)**:

Access triggers async load flow:

1. Check local cache (miss)
2. Async fetch SST file from UFS
3. Block until load completes
4. Update local cache
5. Return state value

By Thm-F-02-45 guarantee, loaded state value is consistent with Checkpoint time.

**Case 4 - $k \notin S_{\text{checkpointed}}$ (does not exist in Checkpoint)**:

Treated as null value, behavior consistent with full recovery.

**Key**: Async load does not change semantics, only affects timing. For operations requiring strong consistency, ForSt provides synchronous load option `SyncPolicy.SYNC`.

**QED** ∎

### Engineering Argument: Performance Optimization Strategy

**Argument**: How does ForSt achieve order-of-magnitude performance improvement?

**1. Checkpoint Optimization Analysis**:

Let state size be $|S|$, change rate be $r$ (proportion of state modified per Checkpoint interval).

RocksDB incremental Checkpoint:

$$
T_{\text{rocksdb}} = T_{\text{scan}} + T_{\text{upload}}(r \cdot |S|) + T_{\text{metadata}}
$$

ForSt Checkpoint:

$$
T_{\text{forst}} = T_{\text{flush}}^{\text{async}} + T_{\text{metadata}}
$$

Where $T_{\text{flush}}^{\text{async}}$ is completed asynchronously in the background, not blocking Checkpoint.

**Improvement Ratio**:

$$
\frac{T_{\text{rocksdb}}}{T_{\text{forst}}} \approx \frac{T_{\text{upload}}(r \cdot |S|)}{T_{\text{metadata}}} \gg 1 \quad (\text{when } |S| > 50\text{GB})
$$

**2. Recovery Optimization Analysis**:

RocksDB recovery:

$$
T_{\text{rocksdb}}^{\text{recovery}} = T_{\text{download}}(|S|) + T_{\text{load}}
$$

ForSt instant recovery:

$$
T_{\text{forst}}^{\text{recovery}} = T_{\text{metadata}} + \sum_{i=1}^{k} T_{\text{fetch}}(s_i)
$$

Where $k$ is the number of state keys actually accessed after recovery, $k \ll |S|/\text{average_state_size}$.

**Typical Scenario**: If state is 1TB but only 1% hot data is immediately accessed:

$$
\frac{T_{\text{rocksdb}}^{\text{recovery}}}{T_{\text{forst}}^{\text{recovery}}} \approx \frac{|S|}{0.01 \cdot |S|} = 100
$$

This is on the same order of magnitude as the 49x improvement reported in the VLDB 2025 paper (considering network overhead and actual access patterns).

---

## 6. Examples

### 6.1 Nexmark Benchmark Performance Comparison

**Test Configuration**:

| Parameter | Configuration |
|------|------|
| Query type | Q5 (window aggregation), Q8 (join operation), Q11 (session window) |
| Data scale | 1 billion events, peak throughput 100K events/s |
| State size | 500GB - 2TB |
| Cluster scale | 20 TaskManagers (16 vCPU, 64GB RAM each) |
| Checkpoint interval | 60 seconds |

**Performance Comparison Results**:

| Metric | RocksDB | ForSt | Improvement |
|------|---------|-------|------|
| **Checkpoint time** | 120s | 7s | **94% ↓** |
| **Checkpoint throughput drop** | 45% | 3% | **93% ↓** |
| **Failure recovery time** | 245s | 5s | **49x ↑** |
| **Average end-to-end latency** | 850ms | 320ms | **62% ↓** |
| **P99 latency** | 3200ms | 890ms | **72% ↓** |
| **Storage cost (monthly)** | $12,000 | $5,800 | **52% ↓** |

**Source**: VLDB 2025 paper "ForSt: A Disaggregated State Backend for Stream Processing"[^1]

### 6.2 TMall Logistics Production Case

**Business Background**: Alibaba TMall logistics real-time tracking system

| Parameter | Value |
|------|------|
| Daily processed messages | 10 billion+ |
| State size | 15TB |
| Concurrent TaskManagers | 200+ |
| SLA requirement | 99.99% availability, P99 < 500ms |

**Before and After Migration Comparison**:

| Metric | RocksDB (Before) | ForSt (After) | Improvement |
|------|-----------------|----------------|------|
| Checkpoint time | 8 minutes | 10 seconds | **48x** |
| Failure recovery time | 35 minutes | 30 seconds | **70x** |
| Storage cost | ¥4.5M/year | ¥2.2M/year | **51% ↓** |
| Peak throughput | 80K TPS | 120K TPS | **50% ↑** |
| TM OOM frequency | 5 times/week | 0 times/week | **100% ↓** |

**Key Benefits**:

1. **Cost savings**: Annual storage cost reduced by 51%, approximately ¥2.3M
2. **Stability improvement**: Job failures caused by Checkpoint timeout dropped from 10/month to 0
3. **Elastic scaling**: Scaling time during peak sales dropped from 30 minutes to 1 minute

### 6.3 Complete ForSt Configuration

**flink-conf.yaml Configuration**:

```yaml
# ========================================
# ForSt State Backend Core Configuration
# ========================================

# Enable ForSt state backend
state.backend: forst

# Remote storage configuration (UFS)
state.backend.forst.ufs.type: s3  # Options: s3, gcs, azure, hdfs
state.backend.forst.ufs.s3.bucket: flink-state-bucket
state.backend.forst.ufs.s3.region: us-east-1
state.backend.forst.ufs.s3.credentials.provider: IAM_ROLE

# State storage path
state.backend.forst.state.dir: s3://flink-state-bucket/flink-jobs/${job.name}

# ========================================
# Local Cache Configuration
# ========================================

# Memory cache size (recommend: 20-30% of TM memory)
state.backend.forst.cache.memory.size: 4gb

# Local disk cache size (recommend: 10-20% of state size)
state.backend.forst.cache.disk.size: 100gb
state.backend.forst.cache.disk.path: /mnt/flink-forst-cache

# Cache replacement policy: LRU | SLRU | W_TINY_LFU
state.backend.forst.cache.policy: SLRU

# ========================================
# Instant Recovery Configuration
# ========================================

# Recovery mode: LAZY (lazy load) | EAGER (full pre-load)
state.backend.forst.restore.mode: LAZY

# Pre-load hot key count (actively loaded during recovery)
state.backend.forst.restore.preload.keys: 10000

# Pre-load thread count
state.backend.forst.restore.preload.threads: 4

# ========================================
# Remote Compaction Configuration
# ========================================

state.backend.forst.compaction.remote.enabled: true
state.backend.forst.compaction.remote.endpoint: compaction-service.flink.svc.cluster.local:9090
state.backend.forst.compaction.remote.parallelism: 8

# Compaction trigger strategy
state.backend.forst.compaction.trigger.interval: 300s
state.backend.forst.compaction.trigger.size-ratio: 1.1

# ========================================
# Checkpoint Configuration
# ========================================

execution.checkpointing.interval: 60s
execution.checkpointing.mode: EXACTLY_ONCE
execution.checkpointing.max-concurrent-checkpoints: 1
execution.checkpointing.externalized-checkpoint-retention: RETAIN_ON_CANCELLATION

# ForSt-specific: async flush interval
state.backend.forst.async-flush-interval: 100ms
```

### 6.4 Java API Complete Example

```java
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.runtime.state.forst.ForStStateBackend;
import org.apache.flink.runtime.state.forst.ForStStateBackendConfig;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.state.StateTtlConfig;
import org.apache.flink.api.common.time.Time;

import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.streaming.api.CheckpointingMode;


public class ForStStateBackendExample {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // ========================================
        // Configure ForSt State Backend
        // ========================================
        ForStStateBackendConfig forstConfig = ForStStateBackendConfig
            .builder()
            // UFS storage path
            .setUFSStoragePath("s3://flink-state-bucket/jobs/user-behavior")

            // Local cache configuration
            .setCacheMemorySize("4gb")
            .setCacheDiskSize("100gb")
            .setCachePolicy(ForStStateBackendConfig.CachePolicy.SLRU)

            // Recovery mode
            .setRestoreMode(ForStStateBackendConfig.RestoreMode.LAZY)
            .setPreloadHotKeys(true)
            .setPreloadKeyCount(10000)

            // Remote Compaction
            .enableRemoteCompaction(true)
            .setRemoteCompactionEndpoint("compaction-service:9090")

            // Sync policy
            .setSyncPolicy(ForStStateBackendConfig.SyncPolicy.ASYNC)
            .setAsyncFlushIntervalMs(100)

            // Consistency level
            .setConsistencyLevel(ForStStateBackendConfig.ConsistencyLevel.EVENTUAL)

            .build();

        ForStStateBackend forstBackend = new ForStStateBackend(forstConfig);
        env.setStateBackend(forstBackend);

        // ========================================
        // Checkpoint Configuration
        // ========================================
        env.enableCheckpointing(60000);  // 60 seconds
        env.getCheckpointConfig().setCheckpointingMode(
            CheckpointingMode.EXACTLY_ONCE);
        env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30000);
        env.getCheckpointConfig().setCheckpointTimeout(600000);
        env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);
        env.getCheckpointConfig().enableExternalizedCheckpoints(
            ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION);

        // ========================================
        // Business Logic: Real-time User Behavior Analysis
        // ========================================
        DataStream<UserEvent> events = env
            .addSource(new KafkaSource<>())
            .keyBy(UserEvent::getUserId)
            .process(new UserBehaviorAnalyzer());

        events.addSink(new ElasticsearchSink<>());

        env.execute("ForSt State Backend Example");
    }

    /**
     * User behavior analysis operator - using State V2 API
     */
    public static class UserBehaviorAnalyzer extends KeyedProcessFunction<String, UserEvent, UserProfile> {

        // ValueState: stores user profile
        private ValueState<UserProfile> userProfileState;

        // ListState: stores recent behavior sequence
        private ListState<UserAction> recentActionsState;

        // MapState: stores category preferences
        private MapState<String, Double> categoryPreferenceState;

        @Override
        public void open(Configuration parameters) {
            // State TTL configuration: 30-day expiration
            StateTtlConfig ttlConfig = StateTtlConfig
                .newBuilder(Time.days(30))
                .setUpdateType(StateTtlConfig.UpdateType.OnCreateAndWrite)
                .setStateVisibility(StateTtlConfig.StateVisibility.NeverReturnExpired)
                .cleanupInRocksdbCompactFilter(1000)
                .build();

            // User profile state
            ValueStateDescriptor<UserProfile> profileDescriptor =
                new ValueStateDescriptor<>("user-profile", UserProfile.class);
            profileDescriptor.enableTimeToLive(ttlConfig);
            userProfileState = getRuntimeContext().getState(profileDescriptor);

            // Recent behavior sequence (keep last 100)
            ListStateDescriptor<UserAction> actionsDescriptor =
                new ListStateDescriptor<>("recent-actions", UserAction.class);
            recentActionsState = getRuntimeContext().getListState(actionsDescriptor);

            // Category preference state
            MapStateDescriptor<String, Double> preferenceDescriptor =
                new MapStateDescriptor<>("category-preference", String.class, Double.class);
            categoryPreferenceState = getRuntimeContext().getMapState(preferenceDescriptor);
        }

        @Override
        public void processElement(UserEvent event, Context ctx, Collector<UserProfile> out)
                throws Exception {

            // Read user profile
            UserProfile profile = userProfileState.value();
            if (profile == null) {
                profile = new UserProfile(event.getUserId());
            }

            // Update profile
            profile.updateWithEvent(event);

            // Update behavior sequence
            recentActionsState.add(event.toAction());

            // Update category preference
            String category = event.getProductCategory();
            Double currentPref = categoryPreferenceState.get(category);
            if (currentPref == null) {
                currentPref = 0.0;
            }
            categoryPreferenceState.put(category, currentPref + event.getScore());

            // Save updated profile
            userProfileState.update(profile);

            // Output result
            out.collect(profile);
        }
    }
}
```

### 6.5 Kubernetes Deployment Configuration

```yaml
# flink-forst-deployment.yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: forst-job
spec:
  image: flink:2.0.0-forst
  flinkVersion: v2.0
  jobManager:
    resource:
      memory: "4Gi"
      cpu: 2
  taskManager:
    resource:
      memory: "16Gi"
      cpu: 8
    # Local cache mount
    podTemplate:
      spec:
        containers:
          - name: flink-main-container
            volumeMounts:
              - name: forst-cache
                mountPath: /mnt/flink-forst-cache
        volumes:
          - name: forst-cache
            emptyDir:
              sizeLimit: 150Gi
              medium: ""  # Use node disk; can change to Memory for testing
  flinkConfiguration:
    state.backend: forst
    state.backend.forst.ufs.type: s3
    state.backend.forst.ufs.s3.bucket: flink-state-bucket
    state.backend.forst.cache.memory.size: 4gb
    state.backend.forst.cache.disk.size: 100gb
    state.backend.forst.restore.mode: LAZY
    execution.checkpointing.interval: 60s
  job:
    jarURI: local:///opt/flink/examples/user-behavior-analysis.jar
    parallelism: 20
    upgradeMode: savepoint
    state: running
```

---

## 7. Visualizations

### 7.1 ForSt Overall Architecture Diagram

ForSt adopts a layered architecture design, thoroughly decoupling state storage from compute nodes:

```mermaid
graph TB
    subgraph "TaskManager"
        A[Stream Operator] --> B[State Access API<br/>State V2]
        B --> C{Cache Hit?}
        C -->|L1 Hit| D[Memory Cache<br/>LRU/SLRU<br/>~1μs]
        C -->|L2 Hit| E[Disk Cache<br/>Local SSD<br/>~1ms]
        C -->|Miss| F[Async Fetch<br/>From UFS]
        D --> G[Process]
        E --> G
        F --> H[Populate Cache] --> G
    end

    subgraph "ForSt State Backend"
        I[LSM-Tree Manager] --> J[Unified File System<br/>UFS Client]
        K[Compaction Scheduler] --> L[Remote Compaction Service]
        M[Instant Recovery<br/>Manager]
        N[Checkpoint Manager<br/>Hard Link]
    end

    subgraph "Unified File System (UFS)"
        J --> O[S3 / OSS / GCS / Azure]
        O --> P[SST Files<br/>Immutable]
        O --> Q[Metadata Files<br/>Versioned]
        O --> R[Checkpoint References<br/>Hard Links]
    end

    B -.-> I
    L -.-> O
    M -.-> F
    N -.-> Q

    style A fill:#e3f2fd
    style D fill:#fff3e0
    style E fill:#fff3e0
    style O fill:#e8f5e9
    style L fill:#fce4ec
```

**Architecture Description**:

- **Three-tier storage**: Memory cache (L1) → Local disk (L2) → Remote UFS (main storage)
- **Compute-storage separation**: TaskManager only retains hot data cache; state authority resides in UFS
- **Remote Compaction**: Offload CPU-intensive operations to dedicated services
- **Instant recovery**: Second-level recovery after failure, state loaded on-demand

### 7.2 LSM-Tree Implementation in ForSt

```mermaid
graph TB
    subgraph "LSM-Tree Abstraction Layer"
        A[Active MemTable] -->|Flush| B[Immutable MemTable]
        B -->|Flush| C[L0 SST Files]
        C -->|Compaction| D[L1 SST Files]
        D -->|Compaction| E[L2 SST Files]
        E -->|Compaction| F[L3+ SST Files]
    end

    subgraph "Storage Tier Mapping"
        A1[Active MemTable] -->|Memory| M1[TaskManager RAM]
        B1[Immutable MemTable] -->|Memory| M1
        C1[L0 SST] -->|Disk| M2[Local SSD Cache]
        D1[L1 SST] -->|UFS| M3[S3/OSS]
        E1[L2 SST] -->|UFS| M3
        F1[L3+ SST] -->|UFS| M3
    end

    subgraph "Compaction Flow"
        G[Compaction Scheduler] --> H{Level Check}
        H -->|L0→L1| I[Local Compaction]
        H -->|L1+→L2+| J[Remote Compaction Service]
        I --> K[Update Metadata]
        J --> K
    end

    style M1 fill:#fff3e0
    style M2 fill:#e1f5fe
    style M3 fill:#e8f5e9
    style J fill:#fce4ec
```

**LSM-Tree Optimizations**:

- **Tiered storage**: Hot data retained locally, cold data offloaded to UFS
- **Remote Compaction**: Compaction for levels above L1 executed remotely
- **Immutable SST**: Supports multi-versioning and hard link Checkpoint

### 7.3 Checkpoint Flow Comparison

**RocksDB vs ForSt Checkpoint Flow**:

```mermaid
flowchart TB
    subgraph "RocksDB Checkpoint (Flink 1.x)"
        R1[Barrier Received] --> R2[Sync Phase<br/>Flush MemTable<br/>~50ms]
        R2 --> R3[Async Phase<br/>Copy SST Files<br/>~60s]
        R3 --> R4[Upload to DFS<br/>Network Transfer<br/>~60s]
        R4 --> R5[Persist Metadata<br/>~10ms]
        R5 --> R6[Checkpoint Complete<br/>Total: ~120s]

        style R2 fill:#ffccbc
        style R3 fill:#ffccbc
        style R4 fill:#ffccbc
    end

    subgraph "ForSt Checkpoint (Flink 2.0)"
        F1[Barrier Received] --> F2[Capture SST List<br/>File References<br/>~2ms]
        F2 --> F3[Flush Dirty Pages<br/>Async, Non-blocking<br/>~5ms]
        F3 --> F4[Persist Metadata<br/>Hard Link References<br/>~5ms]
        F4 --> F5[Checkpoint Complete<br/>Total: ~7s]

        style F2 fill:#c8e6c9
        style F4 fill:#c8e6c9
    end

    subgraph "Performance Comparison"
        P1[Checkpoint Time] --> P2[RocksDB: 120s]
        P1 --> P3[ForSt: 7s]
        P2 --> P4[Improvement: 94%↓]
        P3 --> P4

        P5[Throughput Impact] --> P6[RocksDB: 45%↓]
        P5 --> P7[ForSt: 3%↓]
        P6 --> P8[Improvement: 93%↓]
        P7 --> P8
    end
```

**Key Differences**:

- **RocksDB**: Needs to copy/upload SST files (red), duration proportional to state size
- **ForSt**: Only needs to persist metadata references (green), time approaches constant

### 7.4 Failure Recovery Flow

```mermaid
sequenceDiagram
    participant JM as JobManager
    participant TM as TaskManager (New)
    participant UFS as UFS (S3/OSS)
    participant Cache as Local Cache

    Note over JM,Cache: Fault Recovery Flow - Instant Recovery

    JM->>UFS: 1. Request Latest Checkpoint
    UFS-->>JM: 2. Return Metadata (KB-level)
    JM->>TM: 3. Deploy Task with Metadata

    Note over TM: Recovery complete! Time < 5s

    TM->>TM: 4. Start Processing (No State)

    alt First access to hot key
        TM->>Cache: 5a. Check Cache (Miss)
        Cache-->>TM: 5b. Cache Miss
        TM->>UFS: 5c. Async Fetch SST
        UFS-->>TM: 5d. Return SST Data
        TM->>Cache: 5e. Populate Cache
        Cache-->>TM: 5f. Continue Processing
    end

    alt Prefetch strategy triggered
        TM->>UFS: 6a. Predictive Prefetch
        UFS-->>Cache: 6b. Load Predicted Keys
    end

    Note over TM: Background continuous hot data loading
```

### 7.5 Performance Comparison Radar Chart

```mermaid
graph LR
    subgraph "Nexmark Q8 Performance Comparison"
        direction TB

        subgraph "RocksDB"
            R_CHECK[Checkpoint: ★☆☆☆☆]
            R_RECV[Recovery: ★★☆☆☆]
            R_COST[Cost: ★★☆☆☆]
            R_LAT[LATENCY: ★★★☆☆]
            R_THRU[Throughput: ★★★☆☆]
        end

        subgraph "ForSt"
            F_CHECK[Checkpoint: ★★★★★]
            F_RECV[Recovery: ★★★★★]
            F_COST[Cost: ★★★★★]
            F_LAT[LATENCY: ★★★★☆]
            F_THRU[Throughput: ★★★★★]
        end
    end

    style F_CHECK fill:#c8e6c9
    style F_RECV fill:#c8e6c9
    style F_COST fill:#c8e6c9
    style F_THRU fill:#c8e6c9
```

**Scoring Explanation** (5-star scale):

| Dimension | RocksDB | ForSt | Note |
|------|---------|-------|------|
| Checkpoint speed | ★★☆☆☆ | ★★★★★ | ForSt 17x faster |
| Recovery speed | ★★☆☆☆ | ★★★★★ | ForSt 49x faster |
| Storage cost | ★★☆☆☆ | ★★★★★ | ForSt saves 50% |
| Access latency | ★★★★☆ | ★★★☆☆ | RocksDB local access is better |
| Throughput | ★★★☆☆ | ★★★★★ | ForSt 50% higher |

### 7.6 Storage Cost Structure Comparison

```mermaid
graph LR
    subgraph "RocksDB Cost Structure"
        R1[Local SSD<br/>$0.10/GB/month] --> R2[High-Availability Replication<br/>×2]
        R2 --> R3[Reserved Capacity<br/>×1.5]
        R3 --> R4[Total Cost Factor<br/>3.0x]
        R4 --> R5[$300/month/TB]
    end

    subgraph "ForSt Cost Structure"
        F1[Object Storage<br/>$0.023/GB/month] --> F2[Automatic Redundancy<br/>Built-in]
        F2 --> F3[Pay-as-you-go<br/>×1.0]
        F3 --> F4[Storage Cost<br/>$23/month/TB]
        F5[Local Cache<br/>10% Hot Data<br/>$10/month/TB] --> F6[Total Cost Factor<br/>~1.1x]
        F4 --> F6
        F6 --> F7[$33/month/TB]
    end

    R5 --> COMPARE[Cost Comparison]
    F7 --> COMPARE
    COMPARE --> RESULT[Savings<br/>89%]

    style R5 fill:#ffccbc
    style F7 fill:#c8e6c9
    style RESULT fill:#c8e6c9
```

---

## 8. Applicable Scenarios and Selection Guide

### 8.1 Recommended Scenarios for ForSt

| Scenario | Feature | Benefit |
|------|------|------|
| **Large-state jobs** | State > 50GB | Checkpoint time reduced by 94% |
| **Cloud-native deployment** | K8s + object storage | Compute elastic scaling, unlimited storage |
| **High-frequency Checkpoint** | Checkpoint interval < 30s | Low-impact Checkpoint |
| **Fast recovery requirement** | SLA requires RTO < 1 minute | Recovery speed improved 49x |
| **Cost-sensitive** | Budget constrained | Storage cost reduced by 50%+ |
| **High data locality** | 80%+ access concentrated | Cache hit rate > 90% |

### 8.2 Inapplicable Scenarios

| Scenario | Reason | Alternative |
|------|------|----------|
| **Ultra-low latency** | P99 < 1ms requirement | RocksDB + memory optimization |
| **Limited network bandwidth** | < 100Mbps network | RocksDB local storage |
| **Very small state** | < 100MB | HashMapStateBackend |
| **Random access pattern** | No data locality | Increase local cache |

### 8.3 Selection Decision Tree

```mermaid
flowchart TD
    START[State size?] -->|> 50GB| Q1[Checkpoint frequency?]
    START -->|< 50GB| Q2[Latency requirement?]

    Q1 -->|> 1/min| FORST1[✅ Recommend ForSt]
    Q1 -->|< 1/min| Q3[Deployment environment?]

    Q3 -->|Cloud/K8s| FORST2[✅ Recommend ForSt]
    Q3 -->|Bare metal| Q4[Recovery time requirement?]

    Q4 -->|< 5 minutes| FORST3[✅ Recommend ForSt]
    Q4 -->|> 5 minutes| ROCKS1[⚠️ RocksDB]

    Q2 -->|< 1ms P99| ROCKS2[✅ Recommend RocksDB]
    Q2 -->|> 1ms P99| FORST4[✅ ForSt Optional]

    FORST1 --> CONFIG[Configure cache size<br/>10-20% of state size]
    FORST2 --> CONFIG
    FORST3 --> CONFIG
    FORST4 --> CONFIG

    style FORST1 fill:#c8e6c9
    style FORST2 fill:#c8e6c9
    style FORST3 fill:#c8e6c9
    style FORST4 fill:#c8e6c9
    style ROCKS1 fill:#fff3e0
    style ROCKS2 fill:#c8e6c9
```

---

## 9. References

[^1]: J. Zhang et al., "ForSt: A Disaggregated State Backend for Stream Processing Systems", Proceedings of the VLDB Endowment, Vol. 18, No. 4, 2025. (Apache Flink 2.0)

---

## Appendix: Formalization Level L4 Explanation

This document achieves **L4 (Formal Specification)** level, specifically demonstrated in:

| Level Requirement | Document Demonstration |
|----------|------------|
| L1 Concept Definition | Def-F-02-61 through Def-F-02-65, five core definitions |
| L2 Property Derivation | Prop-F-02-21 through Prop-F-02-24, Lemma-F-02-23 |
| L3 Relation Establishment | Relationship mapping with RocksDB, Dataflow Model, State V2 API |
| L4 Formal Proof | Thm-F-02-45 (Checkpoint consistency), Thm-F-02-46 (Instant recovery correctness) |
| L5 Machine Verification | Out of scope for this document |
| L6 Proof Assistant | Out of scope for this document |

**Proof Strategy**: Based on UFS atomicity assumptions and LSM-Tree immutability, deductive reasoning of state consistency guarantees under disaggregated architecture.

---

*Document version: v1.0 | Updated: 2026-04-03 | Formalization Level: L4 | Status: Completed*
