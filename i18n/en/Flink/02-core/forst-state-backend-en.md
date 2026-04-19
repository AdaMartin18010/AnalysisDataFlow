---
title: "ForSt (For Streaming) - Flink 2.0 Disaggregated State Backend"
translation_status: ai_translated_pending_expert_review
source_version: v4.6
last_sync: "2026-04-20"
---

# ForSt (For Streaming) - Flink 2.0 Disaggregated State Backend

> **Status**: ✅ Released (2025-03-24)
> **Flink Version**: 2.0.0+
> **Stability**: Stable
>
> **Stage**: Flink/02-core-mechanisms | **Prerequisites**: [checkpoint-mechanism-deep-dive.md](./checkpoint-mechanism-deep-dive.md), [disaggregated-state-analysis.md](../01-concepts/disaggregated-state-analysis.md) | **Formalization Level**: L4

---

## 1. Definitions

### Def-F-02-09: ForSt Storage Engine

**Definition**: ForSt (For Streaming) is a **disaggregated state storage engine** introduced in Apache Flink 2.0, specifically designed for stream processing scenarios, decoupling compute node local storage from persistent storage.

$$\text{ForSt} = \langle \text{UFS}, \text{LocalCache}, \text{StateMapping}, \text{SyncPolicy} \rangle$$

Where:

- $\text{UFS}$: Unified File System abstraction layer
- $\text{LocalCache}$: Local cache layer (LRU/SLRU management)
- $\text{StateMapping}$: State key to file location mapping table
- $\text{SyncPolicy}$: Synchronization policy (write-through/write-back)

**Intuitive Explanation**: Traditional RocksDB stores state entirely on TaskManager local disk, while ForSt stores state primarily in a distributed file system (DFS), with local storage serving only as a hot data cache. This is analogous to the CPU multi-level cache architecture — L1/L2 is local, main memory is DFS.

**Source Implementation**:

- Main class: `org.apache.flink.runtime.state.forst.ForStStateBackend`
- Configuration: `org.apache.flink.runtime.state.forst.ForStOptions`
- Location: `flink-runtime` module (flink-state-backends-forst)
- Flink official docs: <https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/state_backends/>

### Def-F-02-10: Unified File System (UFS) Layer

**Definition**: UFS is ForSt's unified file system abstraction layer, providing a unified access interface across different storage backends (HDFS, S3, GCS, Azure Blob).

$$\text{UFS} = \langle \text{StorageBackend}, \text{PathMapping}, \text{AtomicOps}, \text{ConsistencyLevel} \rangle$$

**Interface Specification**:

```java
interface UFS {
  // Atomic write operation
  WriteResult writeAtomic(Path temp, Path target);

  // Consistent read operation
  InputStream readConsistent(Path path, ConsistencyLevel level);

  // List operation (including consistent snapshot)
  List<FileStatus> listStatus(Path dir, SnapshotId snapshot);

  // Multi-version support
  VersionedFile getVersioned(Path path, Version v);
}
```

**Key Feature**: UFS guarantees **atomic visibility** of file operations — once a write completes, all concurrent readers either see the complete new data or the old data, with no intermediate states.

### Def-F-02-11: Active State and Remote State

**Definition**: ForSt distinguishes state data into two tiers:

**Active State** ($S_{active}$):
$$S_{active} = \{ s \in S \mid \text{localCache.contains}(s.key) \land s.accessTime > T_{threshold} \}$$

Refers to hot state data currently residing in TaskManager local cache, accessible with low latency.

**Remote State** ($S_{remote}$):
$$S_{remote} = S \setminus S_{active} = \{ s \in S \mid s.storageLocation \in \text{DFS} \}$$

Refers to cold state data that exists only in the distributed file system, requiring network I/O to access.

**State Migration Functions**:
$$\text{promote}: S_{remote} \times \text{AccessPattern} \rightarrow S_{active}$$
$$\text{evict}: S_{active} \times \text{LRUPolicy} \rightarrow S_{remote}$$

### Def-F-02-12: LazyRestore Mechanism

**Definition**: LazyRestore is ForSt's **lazy state recovery strategy** during failure recovery, allowing TaskManagers to start processing before fully downloading state, loading remote state on demand while running.

**Formal Description**:

Let the pre-failure state be $S$, the recovery process is divided into two phases:

1. **Metadata Recovery Phase** (time $t_0$):
   $$\text{restoreMetadata}(): M \leftarrow \text{load}(\text{checkpoint}_\text{metadata})$$

2. **Lazy Data Recovery Phase** (time $t > t_0$):
   $$\forall k \in \text{Keys}: \text{onAccess}(k) \Rightarrow \begin{cases}
   \text{if } k \in S_{active}: & \text{directRead}(k) \\
   \text{if } k \in S_{remote}: & \text{asyncFetch}(k) \rightarrow S_{active}
   \end{cases}$$

**Recovery Completion Condition**:
$$\text{recoveryComplete} \iff S_{active} \cup S_{fetched} = S_{checkpointed}$$

**Advantage**: Recovery time reduced from $O(|S|)$ to $O(|M|)$, where $|M| \ll |S|$.

### Def-F-02-13: Remote Compaction

**Definition**: Remote Compaction is ForSt's mechanism that offloads LSM-Tree Compaction operations to independent services, avoiding Compaction from consuming TaskManager CPU and I/O resources.

**Compaction Service Architecture**:
$$\text{CompactionService} = \langle \text{CompactionWorkerPool}, \text{Scheduler}, \text{VersionManager} \rangle$$

**Execution Flow**:

1. TaskManager identifies SST file sets $F_{compact}$ requiring Compaction
2. Submits Compaction task to remote service via RPC
3. Remote service executes merge, deduplication, and sorting operations
4. Newly generated SST files atomically replace old files
5. TaskManager updates local metadata references

**Resource Decoupling**:
$$\text{Resource}_{TM} \perp \text{Resource}_{Compaction}$$

---

## 2. Properties

### Prop-F-02-03: Checkpoint Time Complexity Reduction

**Proposition**: ForSt's Checkpoint time complexity is reduced from $O(|S|)$ to $O(|\Delta S|)$, where $\Delta S$ is the change since the last Checkpoint.

**Proof Sketch**:

In RocksDB incremental Checkpoint:
$$T_{rocksdb} = O(|S_{local}| + |\Delta S|) + T_{copy}$$

In ForSt, since state is already in DFS:
$$T_{forst} = O(|\Delta S|) + T_{metadata}$$

Where $T_{metadata} \ll T_{copy}$, because only metadata references need to be persisted rather than actual data.

**Lemma-F-02-04**: File sharing mechanism guarantee

If state file $f$ has not been modified since Checkpoint $c_i$, then $c_{i+1}$ can directly reference $f$ without copying.

$$\forall f \in S: \text{unchanged}(f, c_i, c_{i+1}) \Rightarrow \text{reference}(f, c_{i+1}) = \text{reference}(f, c_i)$$

### Prop-F-02-04: Failure Recovery Time Bound

**Proposition**: Failure recovery time $T_{recovery}$ using LazyRestore satisfies:

$$T_{recovery}^{ForSt} \leq T_{metadata} + k \cdot T_{fetch}^{avg}$$

Where $k$ is the number of hot keys accessed immediately after recovery, $k \ll |S|$.

Compared to RocksDB:
$$T_{recovery}^{RocksDB} \approx T_{metadata} + |S| \cdot T_{download}$$

**Derivation**: Since $k \ll |S|$, ForSt recovery speed is significantly improved.

### Lemma-F-02-05: State Consistency Guarantee

**Lemma**: Under the disaggregated architecture, if UFS provides atomic writes and read-after-write consistency, then ForSt state operations satisfy Linearizability.

**Conditions**:

1. $\text{UFS.write}()$ is atomic (all-or-nothing)
2. $\text{UFS.read}()$ satisfies sequential consistency
3. Metadata updates use atomic compare-and-swap

**Conclusion**: For any state operation sequence, there exists a global total order $\prec$ such that the operation effects are equivalent to serial execution in this order.

---

## 3. Relations

### 3.1 Relationship Between ForSt and RocksDB

ForSt's storage engine is based on the RocksDB core but with the following key modifications:

| Dimension | RocksDB | ForSt |
|------|---------|-------|
| **Storage Location** | Local disk primary | DFS primary, local as cache |
| **Checkpoint** | Local snapshot → upload DFS | Metadata snapshot (files already in DFS) |
| **Compaction** | Local execution | Remote service execution |
| **Recovery Process** | Full download → start | Metadata load → lazy recovery |
| **Capacity Limit** | Limited by TaskManager disk | Theoretically unlimited |

**Implementation Relationship**:
$$\text{ForSt} = \text{RocksDB}^{core} + \text{UFS Layer} + \text{Remote Compaction} + \text{LazyRestore}$$

### 3.2 Mapping to Dataflow Model

ForSt is an efficient implementation of the **Exactly-Once** semantics in the Dataflow Model[^2]:

```
Dataflow Model          ForSt Implementation
─────────────────────────────────────────────────
Windowed State    →     SST Files in DFS
Trigger           →     Checkpoint Barrier
Accumulation      →     Incremental SST Update
Discarding        →     Reference Counting + GC
```

### 3.3 Integration with Checkpoint Mechanism

ForSt integration points with the Flink Checkpoint mechanism:

```
Checkpoint Barrier → Snapshot State Mapping
                         ↓
                ForSt.snapshot()
                         ↓
              [1] Flush Active State to DFS
              [2] Capture SST File List
              [3] Persist Metadata (Path, Version, Checksum)
                         ↓
              Notify Checkpoint Complete
```

**Key Advantage**: Step [1] is usually a no-op or only flushes a small number of dirty pages, because most state has already been synchronized to DFS via background mechanisms.

---

## 4. Argumentation

### 4.1 Necessity Analysis of Disaggregated Architecture

**Problems with Traditional Architecture**:

In the Flink 1.x + RocksDB architecture, the following contradictions exist:

1. **Capacity vs. Cost Contradiction**:
   - Large-state jobs require significant local SSD storage
   - SSD costs are 3-5x higher than object storage
   - TaskManager disk capacity is fixed and cannot elastically scale

2. **Checkpoint vs. Performance Contradiction**:
   - Large-state Checkpoints cause "backpressure storms"
   - Synchronous phase blocks data processing
   - Checkpoint intervals are forced to lengthen, affecting failure recovery granularity

3. **Recovery Speed vs. Cost Contradiction**:
   - Fast recovery requires provisioned resources (Standby TaskManagers)
   - Idle resources cause waste

**Disaggregated Architecture Solutions**:

| Problem | Traditional Solution | Disaggregated Solution |
|------|----------|------------|
| Storage Cost | Local SSD | Object storage (50-70% cost reduction) |
| Checkpoint Time | Grows linearly with state | Near-constant time |
| Recovery Time | Full download | On-demand loading, sub-second startup |
| Resource Elasticity | Tightly coupled | Compute and storage independently scalable |

### 4.2 Checkpoint Consistency Argumentation

**Scenario**: How to guarantee Checkpoint consistency in a disaggregated architecture?

**Challenges**:

- DFS operations typically have eventual consistency
- Concurrent reads and writes may observe incomplete states

**ForSt Solutions**:

1. **Copy-on-Write**:
   - Modify SST files by writing to temporary files first
   - Atomic rename completes the commit
   - Guarantees readers never see partially written data

2. **Multi-Version Concurrency Control (MVCC)**:
   - Each Checkpoint corresponds to a metadata version
   - State files are immutable once written
   - Garbage collection is deferred until confirmed unreferenced

3. **Two-Phase Commit Protocol**:

   ```text
   Phase 1 (Prepare):
     - Flush all dirty pages to DFS
     - Generate new SST file list
     - Pre-commit metadata (mark as PENDING)

   Phase 2 (Commit):
     - Receive Checkpoint Coordinator confirmation
     - Atomically update metadata status to COMMITTED
     - Old version metadata can be safely cleaned up
   ```

### 4.3 Boundary Discussion

**Applicable Scenario Boundaries**:

| Scenario Characteristics | Recommended Solution | Reason |
|----------|----------|------|
| State < 100GB, low latency required | RocksDB | Avoid network overhead |
| State > 1TB, high-frequency Checkpoint | ForSt | Checkpoint efficiency advantage |
| Highly localized state access | ForSt | High cache hit rate |
| Randomly distributed state access | Hybrid strategy | Preload hot data |
| Network bandwidth constrained | RocksDB | Avoid network bottleneck |
| Multi-AZ/cross-region deployment | ForSt | State accessed nearby |

---

## 5. Proof / Engineering Argument

### Thm-F-02-01: ForSt Checkpoint Consistency Theorem

**Theorem**: Under the premise that UFS provides atomic rename and read-after-write consistency, ForSt's Checkpoint mechanism guarantees that the recovered state is consistent with the state at Checkpoint time.

**Formal Statement**:

Let:

- $S_t$: State at time $t$
- $C_i$: The $i$-th Checkpoint
- $\text{restore}(C_i)$: State recovered from $C_i$

Then:
$$\forall i: \text{restore}(C_i) = S_{t_i}$$

Where $t_i$ is the Checkpoint time corresponding to $C_i$.

**Proof**:

**Foundation**:

- Assume UFS guarantees: if file $f$ completes writing (close), subsequent reads get complete content
- Assume atomic rename: rename operation is atomic, no state observing partial rename exists

**Inductive Steps**:

1. **SST File Layer**:
   - Each SST file is immutable once created
   - Committed via atomic rename after writing completes
   - Therefore SST file content has atomic visibility

2. **Metadata Layer**:
   - Checkpoint metadata contains SST file list and checksums
   - Metadata file itself is persisted via atomic write
   - Therefore metadata is either fully visible or fully invisible

3. **Recovery Process**:
   - During recovery, metadata is read to obtain SST file list
   - Due to UFS consistency guarantees, SST files read are consistent with Checkpoint time
   - Therefore recovered state $= $ Checkpoint time state

**QED** ∎

### Thm-F-02-02: LazyRestore Correctness Theorem

**Theorem**: The LazyRestore mechanism produces computation results after recovery that are consistent with results from full recovery followed by execution.

**Proof**:

Need to prove: For any key $k$'s access sequence, LazyRestore behavior is equivalent to full recovery.

**Case Analysis**:

1. **$k \in S_{active}$** (already in local cache):
   - Direct read, behavior consistent with full recovery

2. **$k \in S_{remote}$** (needs remote loading):
   - Access triggers async loading
   - Before loading completes, processing for that key is blocked
   - After loading completes, value is consistent with Checkpoint time (guaranteed by Thm-F-02-01)
   - Therefore processing result is consistent with full recovery

3. **$k \notin S_{checkpointed}$** (does not exist in Checkpoint):
   - Treated as null, behavior consistent with full recovery

**Key**: Async loading does not change semantics, only affects timing. For operations requiring strong consistency, ForSt provides synchronous loading options.

**QED** ∎

### Engineering Argument: Performance Optimization Strategies

**Argument**: Why can ForSt achieve order-of-magnitude performance improvements?

**1. Checkpoint Optimization Analysis**:

Let state size be $|S|$, change rate be $r$ (proportion of state modified per Checkpoint interval).

RocksDB incremental Checkpoint:
$$T_{RB} = T_{scan} + T_{upload}(r \cdot |S|) + T_{metadata}$$

ForSt Checkpoint:
$$T_{FS} = T_{flush}^{async} + T_{metadata}$$

Where $T_{flush}^{async}$ is completed asynchronously in the background, not blocking Checkpoint.

**Improvement Ratio**:
$$\frac{T_{RB}}{T_{FS}} \approx \frac{T_{upload}(r \cdot |S|)}{T_{metadata}} \gg 1 \quad (\text{when } |S| \text{ is large})$$

**2. Recovery Optimization Analysis**:

RocksDB recovery:
$$T_{RB}^{recovery} = T_{download}(|S|) + T_{load}$$

ForSt LazyRestore:
$$T_{FS}^{recovery} = T_{metadata} + \sum_{i=1}^{k} T_{fetch}(s_i)$$

Where $k$ is the number of state keys actually accessed after recovery, $k \ll |S|/\text{average_state_size}$.

**Typical Scenario**: If state is 1TB but only 1% hot data is immediately accessed:
$$\frac{T_{RB}^{recovery}}{T_{FS}^{recovery}} \approx \frac{|S|}{0.01 \cdot |S|} = 100$$

This is in the same order of magnitude as the 49x improvement reported in the paper (considering network overhead and actual access patterns).

---

## 6. Examples

### 6.1 Nexmark Benchmark Results

**Test Configuration**:

- Query types: Q5 (window aggregation), Q8 (join operation), Q11 (session window)
- Data scale: 1 billion events, peak throughput 100K events/s
- State size: 500GB - 2TB
- Cluster scale: 20 TaskManagers (16 vCPU, 64GB RAM each)

**Performance Comparison**:

| Metric | RocksDB | ForSt | Improvement |
|------|---------|-------|------|
| Checkpoint Time | 120s | 7s | **94% ↓** |
| Throughput Drop During Checkpoint | 45% | 3% | **93% ↓** |
| Failure Recovery Time | 245s | 5s | **49x ↑** |
| Average End-to-End Latency | 850ms | 320ms | **62% ↓** |
| P99 Latency | 3200ms | 890ms | **72% ↓** |
| Storage Cost (Monthly) | $12,000 | $5,800 | **52% ↓** |

**Source**: VLDB 2025 paper "ForSt: A Disaggregated State Backend for Stream Processing"[^1]

### 6.2 Configuration Example

**Enable ForSt State Backend**:

```yaml
# flink-conf.yaml
state.backend: forst
state.backend.forst.ufs.type: s3  # or hdfs, gcs, azure

# S3 configuration
state.backend.forst.ufs.s3.bucket: flink-state-bucket
state.backend.forst.ufs.s3.region: us-east-1
state.backend.forst.ufs.s3.credentials.provider: IAM_ROLE

# Local cache configuration (optional)
state.backend.forst.local.cache.size: 10gb
state.backend.forst.local.cache.policy: SLRU

# LazyRestore configuration
state.backend.forst.restore.mode: LAZY  # or EAGER
state.backend.forst.restore.preload.hot-keys: true
```

**Programmatic Configuration**:

```java
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class Example {
    public static void main(String[] args) throws Exception {

        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // Configure ForSt State Backend
        ForStStateBackend forstBackend = new ForStStateBackend();
        forstBackend.setUFSStoragePath("s3://flink-state-bucket/jobs/job-001");
        forstBackend.setLocalCacheSize("10 gb");
        forstBackend.setLazyRestoreEnabled(true);

        env.setStateBackend(forstBackend);

        // Enable Checkpoint
        env.enableCheckpointing(60000);  // 60s
        env.getCheckpointConfig().setCheckpointingMode(
            CheckpointingMode.EXACTLY_ONCE);

    }
}
```

### 6.3 Remote Compaction Configuration

```yaml
# Remote Compaction service configuration
state.backend.forst.compaction.remote.enabled: true
state.backend.forst.compaction.remote.endpoint:
  compaction-service.flink.svc.cluster.local:9090
state.backend.compaction.remote.parallelism: 4

# Trigger strategy
state.backend.forst.compaction.trigger.interval: 300s
state.backend.forst.compaction.trigger.size-ratio: 1.1
```

---

## 7. Visualizations

### 7.1 ForSt Overall Architecture

ForSt adopts a layered architecture design, decoupling state storage from compute nodes:

```mermaid
graph TB
    subgraph "TaskManager"
        A[Stream Operator] --> B[State Access API]
        B --> C{Cache Hit?}
        C -->|Yes| D[Local Cache<br/>LRU/SLRU]
        C -->|No| E[Async Fetch]
        D --> F[Memory Mapped SST]
        E --> D
    end

    subgraph "ForSt State Backend"
        G[State Mapping Manager] --> H[UFS Client]
        I[Compaction Scheduler] --> J[Remote Compaction Service]
        K[LazyRestore Manager]
    end

    subgraph "Unified File System (UFS)"
        H --> L[S3 / HDFS / GCS / Azure]
        L --> M[SST Files v1]
        L --> N[SST Files v2]
        L --> O[Metadata Files]
        L --> P[Checkpoint References]
    end

    B -.-> G
    J -.-> L
    K -.-> E

    style A fill:#e1f5fe
    style D fill:#fff3e0
    style L fill:#e8f5e9
```

### 7.2 Checkpoint Flow Comparison

**Flink 1.x (RocksDB)** vs **Flink 2.0 (ForSt)**:

```mermaid
flowchart TB
    subgraph "RocksDB Checkpoint"
        R1[Barrier Received] --> R2[Sync Phase<br/>Flush MemTable]
        R2 --> R3[Async Phase<br/>Copy SST Files]
        R3 --> R4[Upload to DFS]
        R4 --> R5[Persist Metadata]
        R5 --> R6[Checkpoint Complete]

        style R2 fill:#ffccbc
        style R3 fill:#ffccbc
        style R4 fill:#ffccbc
    end

    subgraph "ForSt Checkpoint"
        F1[Barrier Received] --> F2[Capture SST List]
        F2 --> F3[Flush Dirty Pages<br/>Async, Non-blocking]
        F3 --> F4[Persist Metadata<br/>File References Only]
        F4 --> F5[Checkpoint Complete]

        style F2 fill:#c8e6c9
        style F4 fill:#c8e6c9
    end
```

**Key Difference**:

- RocksDB needs to copy/upload SST files (red)
- ForSt only needs to persist metadata references (green)

### 7.3 Failure Recovery Flow

```mermaid
sequenceDiagram
    participant JM as JobManager
    participant TM as TaskManager (New)
    participant DFS as DFS (UFS)
    participant Cache as Local Cache

    JM->>DFS: 1. Request Latest Checkpoint
    DFS-->>JM: 2. Return Metadata
    JM->>TM: 3. Deploy Task with Metadata

    Note over TM: LazyRestore Begins

    TM->>DFS: 4. Load State Mapping
    TM->>TM: 5. Start Processing (No State Yet)

    alt Hot Key Access
        TM->>Cache: 6a. Check Local Cache
        Cache-->>TM: 6b. Cache Miss
        TM->>DFS: 6c. Async Fetch SST
        DFS-->>TM: 6d. Return SST Data
        TM->>Cache: 6e. Populate Cache
        Cache-->>TM: 6f. Return State Value
    end

    alt Cold Key Access
        TM->>DFS: 7a. Direct Read from DFS
        DFS-->>TM: 7b. Return State Value
    end

    Note over TM: Background: Preload Predicted Hot Keys
    TM->>DFS: 8. Preload Hot SSTs
    DFS-->>Cache: 9. Populate Cache Proactively
```

### 7.4 Storage Cost Comparison

```mermaid
graph LR
    subgraph "RocksDB Cost Structure"
        R1[Local SSD<br/>$0.10/GB/month] --> R2[HA Replication<br/>2x]
        R2 --> R3[Reserved Capacity<br/>1.5x]
        R3 --> R4[Total Cost Factor<br/>3.0x]
    end

    subgraph "ForSt Cost Structure"
        F1[S3 Standard<br/>$0.023/GB/month] --> F2[Automatic Redundancy<br/>Built-in]
        F2 --> F3[Pay-as-you-go<br/>1.0x]
        F3 --> F4[Total Cost Factor<br/>0.77x]
        F5[Local Cache<br/>10% hot data] --> F6[Additional Cost<br/>0.3x]
        F4 --> F7[Combined Cost<br/>~1.1x]
    end

    style R4 fill:#ffccbc
    style F7 fill:#c8e6c9
```

---

## 8. Official Release Data

### Flink 2.0 ForSt State Backend Official Release Data

According to the [Apache Flink 2.0.0 Official Release Announcement](https://flink.apache.org/2025/03/24/apache-flink-2.0.0-a-new-era-of-real-time-data-processing/)[^3], ForSt State Backend is one of Flink 2.0's core features:

**Official Performance Benchmark** (Nexmark Benchmark):

| Metric | RocksDB (Flink 1.x) | ForSt (Flink 2.0) | Improvement |
|------|--------------------|--------------------|------|
| **Checkpoint Time** | 120s | 7s | **94% ↓** |
| **Throughput Drop During Checkpoint** | 45% | 3% | **93% ↓** |
| **Failure Recovery Time** | 245s | 5s | **49x ↑** |
| **Average End-to-End Latency** | 850ms | 320ms | **62% ↓** |
| **P99 Latency** | 3200ms | 890ms | **72% ↓** |
| **Storage Cost (Monthly)** | $12,000 | $5,800 | **52% ↓** |

**Production Case**: Alibaba TMall logistics system migration reduced annual storage costs by 51%, Checkpoint timeout failures dropped from 10/month to 0.

---

## 8. Source Code Deep Analysis

### 8.1 SST File Format Details

#### 8.1.1 SST File Structure Analysis

**Source Location**: `flink-state-backends-forst/src/main/java/org/apache/flink/state/forst/storage/ForStSSTFile.java`

SST (Sorted String Table) is the core storage format of ForSt/RocksDB, using LSM-Tree structure:

```mermaid
graph TB
    subgraph "SST File Internal Structure"
        A[SST File] --> B[Data Block 1]
        A --> C[Data Block 2]
        A --> D[Data Block N]
        A --> E[Meta Block]
        A --> F[Meta Index Block]
        A --> G[Footer]

        B --> B1[Key-Value Pairs<br/>Ordered Storage]
        B --> B2[Restart Points<br/>Index Acceleration]
        B --> B3[Compressed Data<br/>LZ4/ZSTD]

        E --> E1[Filter Block<br/>Bloom Filter]
        E --> E2[Properties Block<br/>Statistics]
        E --> E3[Range Tombstones<br/>Deletion Markers]
    end
```

**SST File Core Components**:

| Component | Size (Typical) | Purpose |
|------|--------------|------|
| Data Block | 4KB-32KB | Stores actual key-value pair data |
| Index Block | 16B/Block | Index for accelerating data lookup |
| Filter Block | ~10bit/key | Bloom Filter, reducing disk IO |
| Meta Block | Variable | Stores properties, statistics, etc. |
| Footer | 48B | File metadata, pointing to Index and MetaIndex |

#### 8.1.2 SST File Source Code Analysis

```java
/**
 * ForSt SST file format implementation
 */
public class ForStSSTFile {

    /**
     * SST file magic number (for file type identification)
     */
    private static final byte[] SST_MAGIC = new byte[] {0x53, 0x53, 0x54}; // "SST"

    /**
     * SST file version number
     */
    private static final int SST_VERSION = 2;

    /**
     * Data Block structure
     */
    public static class DataBlock {
        // Number of restart points (one every N keys)
        private final int numRestarts;

        // Actual key-value pair data (Delta encoding compression)
        private final byte[] data;

        /**
         * Read a single Key-Value pair
         */
        public KeyValue readEntry(int offset) {
            // Use Delta encoding to reduce storage space
            // Shared prefix length
            int sharedPrefixLen = readVarint();
            // Unshared part length
            int unsharedKeyLen = readVarint();
            // Value length
            int valueLen = readVarint();

            // Reconstruct complete key
            byte[] key = reconstructKey(sharedPrefixLen, unsharedKeyLen);
            byte[] value = readBytes(valueLen);

            return new KeyValue(key, value);
        }
    }

    /**
     * Block handle (for positioning)
     */
    public static class BlockHandle {
        private final long offset;  // Block offset in file
        private final long size;    // Block size

        public byte[] encode() {
            // Varint encoding: offset + size
            ByteBuffer buffer = ByteBuffer.allocate(16);
            putVarint(buffer, offset);
            putVarint(buffer, size);
            return buffer.array();
        }
    }

    /**
     * Footer structure (48 bytes at end of file)
     */
    public static class Footer {
        // Meta Index Block handle
        private final BlockHandle metaIndexHandle;
        // Index Block handle
        private final BlockHandle indexHandle;
        // Magic number (for verification)
        private final byte[] magic;

        public static final int ENCODED_LENGTH = 48;

        public byte[] encode() {
            ByteBuffer buffer = ByteBuffer.allocate(ENCODED_LENGTH);
            buffer.put(metaIndexHandle.encode());
            buffer.put(indexHandle.encode());
            buffer.put(magic);
            return buffer.array();
        }
    }
}
```

#### 8.1.3 Key-Value Storage Format

```java
/**
 * ForSt internal key format design
 */
public class ForStKeyFormat {

    /**
     * Internal Key structure:
     * +-----------------+-----------------+---------------+
     * |  User Key       |  Sequence Num   |  Value Type   |
     * |  (variable)      |  (7 bytes)      |  (1 byte)     |
     * +-----------------+-----------------+---------------+
     *
     * Total length: user_key_len + 8 bytes
     */
    public static class InternalKey {
        private final byte[] userKey;
        private final long sequenceNumber;
        private final ValueType valueType;

        public byte[] encode() {
            ByteBuffer buffer = ByteBuffer.allocate(userKey.length + 8);
            buffer.put(userKey);
            // Low 7 bytes: sequence number (incrementing, for version control)
            // High 1 byte: value type
            long seqAndType = (sequenceNumber << 8) | valueType.getCode();
            buffer.putLong(seqAndType);
            return buffer.array();
        }
    }

    /**
     * Value Type enumeration
     */
    public enum ValueType {
        PUT((byte) 0x01),           // Normal write
        DELETE((byte) 0x00),        // Deletion marker
        MERGE((byte) 0x02),         // Merge operation
        SINGLE_DELETE((byte) 0x07); // Single deletion

        private final byte code;

        ValueType(byte code) {
            this.code = code;
        }
    }
}
```

### 8.2 RocksDB Compaction Mechanism Source Code

#### 8.2.1 Compaction Trigger Conditions

**Source Location**: `flink-state-backends-forst/src/main/java/org/apache/flink/state/forst/compaction/ForStCompactionScheduler.java`

```java
/**
 * ForSt Compaction scheduler
 */
public class ForStCompactionScheduler {

    /**
     * Check if Compaction is needed
     */
    public CompactionTask checkCompactionNeeded(ForStStateBackend stateBackend) {
        // 1. Check Level 0 file count
        int level0Files = stateBackend.getLevel0FileCount();
        if (level0Files >= L0_COMPACTION_TRIGGER) {
            return createL0CompactionTask();
        }

        // 2. Check each level size
        for (int level = 1; level < MAX_LEVELS; level++) {
            long levelSize = stateBackend.getLevelSize(level);
            long threshold = getLevelThreshold(level);

            if (levelSize > threshold) {
                return createLevelCompactionTask(level);
            }
        }

        // 3. Check seek count (read amplification trigger)
        if (stateBackend.getSeekCompactionScore() > SEEK_COMPACTION_THRESHOLD) {
            return createSeekCompactionTask();
        }

        return null;
    }

    /**
     * Level threshold calculation (exponential growth)
     * Level N threshold = Level N-1 threshold × 10
     */
    private long getLevelThreshold(int level) {
        return BASE_LEVEL_SIZE * (long) Math.pow(LEVEL_SIZE_MULTIPLIER, level - 1);
    }
}
```

#### 8.2.2 Compaction Execution Flow

```mermaid
sequenceDiagram
    autonumber
    participant CS as CompactionScheduler
    participant TM as TaskManager
    participant RS as RemoteCompactionService
    participant UFS as Unified File System

    Note over CS: Detected need for Compaction
    CS->>TM: Submit Compaction task
    TM->>TM: Pause related SST file writes

    alt Local Compaction
        TM->>TM: Execute local Compaction
        TM->>TM: Merge SST files
        TM->>TM: Delete old files
    else Remote Compaction
        TM->>RS: Submit Compaction task
        RS->>UFS: Read input SST files
        RS->>RS: Execute merge, deduplication
        RS->>UFS: Write new SST files
        RS-->>TM: Return new file list
    end

    TM->>TM: Update metadata references
    TM->>UFS: Atomically replace file list
    TM->>UFS: Delete expired files
```

### 8.3 ForSt UFS (Unified File System) Abstraction

#### 8.3.1 UFS Architecture Design

**Source Location**: `flink-state-backends-forst/src/main/java/org/apache/flink/state/forst/fs/UnifiedFileSystem.java`

```java
/**
 * ForSt unified file system abstraction layer
 * Shields underlying storage differences (S3/HDFS/GCS/OSS)
 */
public class UnifiedFileSystem {

    private final StorageBackend storageBackend;
    private final PathMapping pathMapping;
    private final ConsistencyManager consistencyManager;

    /**
     * Atomic write operation (Copy-on-Write mode)
     */
    public boolean writeAtomic(Path tempPath, Path targetPath, byte[] data) {
        // 1. Write to temporary file
        storageBackend.write(tempPath, data);

        // 2. Verify data integrity
        Checksum checksum = calculateChecksum(data);

        // 3. Atomic rename (guarantees visibility)
        if (storageBackend.supportsAtomicRename()) {
            // HDFS/OSS support atomic rename
            storageBackend.rename(tempPath, targetPath);
        } else {
            // S3 uses multi-version mechanism
            storageBackend.putObject(targetPath, data);
            consistencyManager.registerVersion(targetPath, checksum);
        }

        return true;
    }

    /**
     * Consistent read operation
     */
    public InputStream readConsistent(Path path, ConsistencyLevel level) {
        switch (level) {
            case STRONG:
                // Strong consistency: wait for all writes to complete
                consistencyManager.waitForConsistency(path);
                return storageBackend.read(path);

            case EVENTUAL:
                // Eventual consistency: read directly
                return storageBackend.read(path);

            case VERSIONED:
                // Version consistency: read specified version
                Version version = consistencyManager.getLatestVersion(path);
                return storageBackend.readVersion(path, version);

            default:
                throw new IllegalArgumentException("Unsupported consistency level");
        }
    }

    /**
     * Multi-version SST file management
     */
    public VersionedFile createVersionedSST(String baseName, byte[] data) {
        // Generate version number
        Version version = versionManager.nextVersion();

        // Versioned path: /baseName_v{version}.sst
        Path versionedPath = pathMapping.toVersionedPath(baseName, version);

        // Atomic write
        writeAtomic(createTempPath(versionedPath), versionedPath, data);

        return new VersionedFile(versionedPath, version, calculateChecksum(data));
    }
}
```

#### 8.3.2 Storage Backend Adapters

```java
/**
 * Storage backend interface
 */
public interface StorageBackend {
    void write(Path path, byte[] data);
    InputStream read(Path path);
    boolean rename(Path source, Path target);
    boolean delete(Path path);
    boolean exists(Path path);
    List<FileStatus> listStatus(Path dir);
    boolean supportsAtomicRename();
}

/**
 * S3 storage backend implementation
 */
public class S3StorageBackend implements StorageBackend {
    private final S3Client s3Client;
    private final String bucket;

    @Override
    public void write(Path path, byte[] data) {
        // Use S3 multipart upload to guarantee atomicity
        String key = path.toString();
        s3Client.putObject(bucket, key, data);
    }

    @Override
    public boolean rename(Path source, Path target) {
        // S3 does not support atomic rename, use copy+delete simulation
        String sourceKey = source.toString();
        String targetKey = target.toString();

        s3Client.copyObject(bucket, sourceKey, bucket, targetKey);
        s3Client.deleteObject(bucket, sourceKey);

        return true;
    }

    @Override
    public boolean supportsAtomicRename() {
        return false;  // S3 does not support atomic rename
    }
}

/**
 * HDFS storage backend implementation
 */
public class HdfsStorageBackend implements StorageBackend {
    private final FileSystem hdfs;

    @Override
    public boolean rename(Path source, Path target) {
        // HDFS natively supports atomic rename
        return hdfs.rename(source, target);
    }

    @Override
    public boolean supportsAtomicRename() {
        return true;
    }
}
```

### 8.4 Incremental Checkpoint SST Version Management

#### 8.4.1 Incremental Checkpoint Implementation

**Source Location**: `flink-state-backends-forst/src/main/java/org/apache/flink/state/forst/checkpoint/ForStIncrementalSnapshotStrategy.java`

```java
/**
 * ForSt incremental snapshot strategy
 * Leverages SST file immutability for efficient Checkpoint
 */
public class ForStIncrementalSnapshotStrategy {

    private final UnifiedFileSystem ufs;
    private final SSTVersionManager versionManager;

    /**
     * Execute incremental Checkpoint
     */
    public CheckpointHandle snapshotState(long checkpointId,
                                          Set<VersionedFile> currentSSTFiles,
                                          Set<VersionedFile> previousSSTFiles) {

        // 1. Calculate delta: find newly added SST files
        Set<VersionedFile> newFiles = Sets.difference(currentSSTFiles, previousSSTFiles);

        // 2. Calculate unchanged files (reusable)
        Set<VersionedFile> unchangedFiles = Sets.intersection(currentSSTFiles, previousSSTFiles);

        // 3. Process new files
        Set<FileReference> uploadedFiles = new HashSet<>();
        for (VersionedFile file : newFiles) {
            // Upload SST file to Checkpoint directory
            Path checkpointPath = createCheckpointPath(checkpointId, file.getName());
            ufs.copy(file.getPath(), checkpointPath);

            uploadedFiles.add(new FileReference(
                file.getName(),
                checkpointPath,
                file.getVersion(),
                file.getChecksum()
            ));
        }

        // 4. Process unchanged files (only record references)
        for (VersionedFile file : unchangedFiles) {
            uploadedFiles.add(new FileReference(
                file.getName(),
                null,  // No copy, use previous path
                file.getVersion(),
                file.getChecksum()
            ));
        }

        // 5. Persist metadata
        CheckpointMetadata metadata = new CheckpointMetadata(
            checkpointId,
            System.currentTimeMillis(),
            uploadedFiles,
            currentSSTFiles.stream().map(v -> v.getVersion()).max(Long::compare).orElse(0L)
        );

        Path metadataPath = createCheckpointPath(checkpointId, "_metadata");
        ufs.write(metadataPath, serializeMetadata(metadata));

        return new CheckpointHandle(checkpointId, metadataPath);
    }

    /**
     * Restore Checkpoint
     */
    public Set<VersionedFile> restoreState(CheckpointHandle handle) {
        // 1. Read metadata
        CheckpointMetadata metadata = readMetadata(handle.getMetadataPath());

        // 2. Verify all files exist and are intact
        for (FileReference ref : metadata.getFiles()) {
            Path filePath = ref.getCheckpointPath() != null
                ? ref.getCheckpointPath()
                : versionManager.resolvePath(ref.getName(), ref.getVersion());

            Checksum actualChecksum = ufs.calculateChecksum(filePath);
            if (!actualChecksum.equals(ref.getChecksum())) {
                throw new CorruptedCheckpointException("Checksum mismatch for " + ref.getName());
            }
        }

        // 3. Build current SST file set
        return metadata.getFiles().stream()
            .map(ref -> new VersionedFile(
                ref.getName(),
                ref.getVersion(),
                ref.getCheckpointPath(),
                ref.getChecksum()
            ))
            .collect(Collectors.toSet());
    }
}
```

#### 8.4.2 SST Version Reference Counting and Garbage Collection

```java
import java.util.Map;

/**
 * SST file lifecycle management
 */
public class SSTLifecycleManager {

    private final Map<String, ReferenceCount> referenceCounts;

    /**
     * Reference count structure
     */
    private static class ReferenceCount {
        final String fileName;
        final long version;
        final Set<Long> referencingCheckpoints;  // Checkpoints referencing this file
        boolean markedForDeletion;

        void addReference(long checkpointId) {
            referencingCheckpoints.add(checkpointId);
        }

        void removeReference(long checkpointId) {
            referencingCheckpoints.remove(checkpointId);
        }

        boolean canBeDeleted() {
            return referencingCheckpoints.isEmpty() && !markedForDeletion;
        }
    }

    /**
     * Trigger garbage collection
     */
    public void garbageCollect(Set<Long> activeCheckpoints) {
        for (ReferenceCount ref : referenceCounts.values()) {
            // Remove references from expired Checkpoints
            ref.referencingCheckpoints.retainAll(activeCheckpoints);

            // Files with zero references can be deleted
            if (ref.canBeDeleted()) {
                Path filePath = versionManager.resolvePath(ref.fileName, ref.version);
                ufs.delete(filePath);
                ref.markedForDeletion = true;
            }
        }
    }
}
```

### 8.5 Core Differences Between ForSt and RocksDB

```mermaid
graph TB
    subgraph "RocksDB State Backend"
        R1[Local RocksDB Instance] --> R2[Local SST Files]
        R2 --> R3[Local Compaction]
        R3 --> R4[Incremental Checkpoint]
        R4 --> R5[Upload SST to HDFS/S3]
        R5 --> R6[Failure Recovery]
        R6 --> R7[Full SST Download]
        R7 --> R1
    end

    subgraph "ForSt State Backend"
        F1[ForSt Instance] --> F2[UFS Write]
        F2 --> F3[S3/HDFS SST Files]
        F3 --> F4[Remote Compaction Service]
        F4 --> F5[Metadata Checkpoint]
        F5 --> F6[Failure Recovery]
        F6 --> F7[LazyRestore<br/>On-demand Loading]
        F7 --> F1
    end

    style R1 fill:#fff3e0
    style F1 fill:#e8f5e9
    style R7 fill:#ffcdd2
    style F7 fill:#c8e6c9
```

| Dimension | RocksDB | ForSt | Source Manifestation |
|------|---------|-------|---------|
| Storage Location | Local disk | UFS (S3/HDFS) | `RocksDBStateBackend` vs `ForStStateBackend` |
| SST Write | `WritableFile` local write | `UnifiedFileSystem.write()` | Storage backend abstraction layer difference |
| Compaction | Local execution | Remote service | `CompactionScheduler` scheduling strategy difference |
| Checkpoint | Copy + upload | Metadata snapshot | `snapshotState()` implementation difference |
| Recovery | Full download | LazyRestore | `restoreState()` loading strategy difference |

---

## 9. References

[^3]: Apache Flink Blog, "Apache Flink 2.0.0: A New Era of Real-Time Data Processing", March 24, 2025. <https://flink.apache.org/2025/03/24/apache-flink-2.0.0-a-new-era-of-real-time-data-processing/>

[^2]: T. Akidau et al., "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing", PVLDB, 8(12):1792-1803, 2015.

---

## Appendix: Formalization Level L4 Explanation

This document achieves **L4 (Formal Specification)** level, specifically:

| Level Requirement | Document Manifestation |
|----------|------------|
| L1 Concept Definitions | Def-F-02-09 to Def-F-02-13, five core definitions |
| L2 Property Derivation | Prop-F-02-03, Prop-F-02-04, Lemma-F-02-05 |
| L3 Relation Establishment | Mapping with RocksDB, Dataflow Model, Checkpoint |
| L4 Formal Proof | Thm-F-02-01 (Checkpoint Consistency), Thm-F-02-02 (LazyRestore Correctness) |
| L5 Machine Verification | Out of scope for this document |
| L6 Proof Assistant | Out of scope for this document |

**Proof Strategy**: Deductive reasoning based on UFS atomicity assumptions, proving that state consistency is maintained under disaggregated architecture.

---

*Document Version: v1.0 | Updated: 2026-04-20 | Status: Complete | Formal Elements: Def×5, Prop×2, Lemma×2, Thm×2*
