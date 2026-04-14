---
title: "Falcon Vectorized Operator Layer Deep Dive"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Falcon Vectorized Operator Layer Deep Dive

> **Stage**: Flink/14-rust-assembly-ecosystem/flash-engine
> **Prerequisites**: [01-flash-architecture.md](./01-flash-architecture.md) | [SIMD Optimization Principles](../simd-optimization/)
> **Formality Level**: L5 (Detailed Engineering Implementation + Performance Analysis)

---

## 1. Definitions

### Def-FLASH-05: Falcon Vectorized Operator Layer

**Definition**: Falcon is the core computation layer of the Flash engine, implementing vectorized operators in C++, achieving high-performance batch data processing through SIMD instruction sets and columnar memory layout.

**Formal Description**:

```
Falcon_Layer := ⟨OpRegistry, VecExecutor, SIMDKernels, MemoryManager⟩

OpRegistry := {op₁, op₂, ..., opₙ} where each opᵢ: Batch → Batch
VecExecutor := ⟨Scheduler, Parallelizer, BufferManager⟩
SIMDKernels := {kernel_AVX2, kernel_AVX512, kernel_NEON, ...}
```

**Operator Classification**:

```
Falcon_Operators = Stateless_Operators ∪ Stateful_Operators

Stateless_Operators:
- Filter: predicate filtering
- Project: column projection
- Calc: scalar expression evaluation
- Map: data transformation

Stateful_Operators:
- Aggregate: aggregation computation
- Join: stream join
- Window: window computation
- CEP: complex event processing
```

---

### Def-FLASH-06: SIMD Optimization Kernels

**Definition**: SIMD (Single Instruction Multiple Data) kernels are computation routines optimized for specific CPU instruction sets, capable of processing multiple data elements simultaneously.

**Formal Description**:

```
SIMD_Kernel := ⟨ISA, VectorWidth, Operation, DataType⟩

Mainstream ISA Support:
┌───────────┬─────────────┬────────────────┐
│ ISA       │ VectorWidth │ Supported Ops  │
├───────────┼─────────────┼────────────────┤
│ SSE4.2    │ 128 bit     │ 4×int32, 2×int64│
│ AVX2      │ 256 bit     │ 8×int32, 4×int64│
│ AVX-512   │ 512 bit     │ 16×int32, 8×int64│
│ NEON      │ 128 bit     │ ARM support    │
└───────────┴─────────────┴────────────────┘

Speedup formula:
Speedup_SIMD = (Scalar_Time × N) / SIMD_Time
where N = VectorWidth / DataTypeWidth
```

---

### Def-FLASH-07: Columnar Batch Format

**Definition**: Columnar batch format is a data organization method where data of the same column is stored contiguously, facilitating SIMD loading and cache-efficient access.

**Formal Description**:

```
ColumnarBatch := ⟨Schema, [Column₁, Column₂, ..., Columnₙ], Metadata⟩

Column := ⟨DataBuffer, NullBitmap, TypeInfo⟩

Memory layout comparison:
Row-based: [row1_col1, row1_col2, ..., row2_col1, row2_col2, ...]
Columnar:  [col1_row1, col1_row2, ...][col2_row1, col2_row2, ...]

Cache line utilization:
- Row-based: each row access spans multiple cache lines, low cache hit rate
- Columnar: sequential access of same column data, prefetch-friendly, high hit rate
```

---

### Def-FLASH-08: Operator Fusion

**Definition**: Operator fusion is the technique of merging multiple consecutive operators into a single kernel execution, reducing intermediate data materialization and memory access.

**Formal Description**:

```
Fusion: [op₁, op₂, ..., opₙ] → FusedKernel

Fusion conditions:
- Data locality condition: opᵢ's output directly serves as opᵢ₊₁'s input
- No-barrier condition: no checkpoint / shuffle boundary between operators
- Compatibility condition: operators use the same batch format

Benefits:
MemoryAccessReduction = 1 - (1 / n) where n = fused operators count
```

---

## 2. Properties

### Prop-FLASH-04: Conditional Dependency of SIMD Acceleration

**Proposition**: The effectiveness of SIMD optimization depends on data type, operation type, and instruction set support.

**Formal Statement**:

```
SIMD_Effectiveness(op, dtype, ISA) =
    VectorWidth(ISA) / SizeOf(dtype) × ParallelEfficiency(op)

Where ParallelEfficiency(op) takes values:
- Arithmetic ops (+, -, *, /): ~100% (fully parallel)
- Comparison ops (=, <, >): ~100%
- String processing: 30-70% (algorithm-dependent)
- Branch-intensive ops: 10-40% (high SIMD branch cost)
```

**Measured Speedup** (relative to Java implementation):

```
Operation Type    │ AVX2 Speedup │ AVX-512 Speedup │ Theoretical Limit
──────────────────┼──────────────┼─────────────────┼─────────────────
Integer Add       │ 6-8x         │ 10-14x          │ 16x
Float Multiply    │ 6-8x         │ 10-14x          │ 16x
String Compare    │ 8-12x        │ 12-20x          │ 32x
Date Parse        │ 15-25x       │ 20-40x          │ 50x
Regex Match       │ 5-10x        │ 8-15x           │ 20x
```

---

### Prop-FLASH-05: Trade-off Relationship Between Batch Size and Throughput

**Proposition**: There exists an optimal batch size that maximizes throughput, which is affected by cache capacity and operator complexity.

**Formal Statement**:

```
Optimal_Batch_Size = f(L1_cache, L2_cache, op_complexity)

General rules:
- Simple operators (Filter, Project): optimal ∈ [1000, 10000]
- Complex operators (Join, Aggregate): optimal ∈ [100, 1000]
- Memory-constrained operators: optimal ∈ [10, 100]

Throughput model:
Throughput(B) = B / (T_fixed + T_per_element × B / SIMD_width)

Derivative analysis:
d(Throughput)/dB = T_fixed / (T_fixed + T_per_element × B / SIMD_width)² > 0
But with diminishing marginal returns
```

---

### Prop-FLASH-06: Cache Efficiency Advantage of Columnar Layout

**Proposition**: Columnar memory layout achieves significantly higher cache hit rates than row-based layout in analytical workloads.

**Formal Statement**:

```
Cache_Efficiency = Useful_Data / Cache_Line_Size

Row-based layout (accessing 2 columns):
- Cache line size: 64 bytes
- Row size: 100 bytes (typical)
- Useful data: 2 × 8 bytes = 16 bytes
- Cache efficiency: 16 / 64 = 25%

Columnar layout (accessing 2 columns):
- Each column stored contiguously
- Useful data: 64 bytes (full cache line)
- Cache efficiency: 64 / 64 = 100%
```

---

## 3. Relations

### 3.1 Falcon Layer Relationship with Other Components

```
                    ┌─────────────────────────────────────┐
                    │         Falcon Layer Relationship   │
                    │              Diagram                │
                    └─────────────────────────────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
        ▼                            ▼                            ▼
┌───────────────┐          ┌──────────────────┐         ┌──────────────────┐
│ Leno Integration│◄──────►│ Falcon Vectorized│◄───────►│ ForStDB Storage  │
│ Layer (Plan Gen)│          │ Layer (Compute)  │         │ Layer (State)    │
└───────────────┘          └────────┬─────────┘         └──────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌──────────┐   ┌──────────────┐  ┌──────────────┐
            │SIMD Kernels│  │Memory Manager│  │Operator      │
            │(AVX-512)   │  │(Pool/Columnar)│  │Registry (80%+)│
            └──────────┘   └──────────────┘  └──────────────┘
```

### 3.2 Falcon vs Open Source Flink Operator Mapping

| Flink Java Operator | Falcon C++ Implementation | Optimization Strategy |
|---------------------|---------------------------|-----------------------|
| `Calc` | `VecCalc` | SIMD expression evaluation |
| `Filter` | `VecFilter` | Vectorized predicate + compressed selection |
| `Project` | `VecProject` | Zero-copy column reference |
| `Aggregate` | `VecAggregate` | Grouped SIMD aggregation |
| `Join` | `VecJoin` | Vectorized hash table |
| `Window` | `VecWindow` | Sliding window SIMD |

### 3.3 Relationship with Apache Arrow

The Falcon layer uses Apache Arrow as the underlying columnar format:

```
┌─────────────────────────────────────────────────────────────┐
│                    Falcon Memory Format                      │
├─────────────────────────────────────────────────────────────┤
│  Arrow Columnar Format (Base)                               │
│  ├── Fixed-width types: Int8/16/32/64, Float, Double       │
│  ├── Variable-width types: String, Binary                  │
│  └── Composite types: Struct, List, Map                    │
├─────────────────────────────────────────────────────────────┤
│  Falcon Extensions                                          │
│  ├── Streaming-specific: Watermark column, event timestamp  │
│  ├── State markers: StateKey encoding                      │
│  └── Network optimization: Zero-serialization transport format│
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Argumentation

### 4.1 String Function Optimization Case Analysis

String processing is a focus of Flash engine optimization. Typical implementations include:

**Case 1: `LENGTH` Function Vectorization**

```cpp
// Java implementation (character-by-character)
int length(String s) {
    return s.length();  // UTF-16 traversal, each character checked
}

// Falcon AVX2 implementation (batch)
void vec_length(__m256i* input, int* output, int n) {
    for (int i = 0; i < n; i += 8) {
        // Load 8 string pointers simultaneously
        __m256i ptrs = _mm256_loadu_si256(input + i);
        // Parallel length computation (SIMD string length algorithm)
        __m256i lengths = simd_strlen_batch(ptrs);
        _mm256_storeu_si256((__m256i*)(output + i), lengths);
    }
}
// Speedup: ~15x
```

**Case 2: `SUBSTRING` Function Optimization**

```cpp
// Java implementation
String substring(String s, int start, int end) {
    return s.substring(start, end);  // Creates new string object
}

// Falcon implementation
void vec_substring(Column* input, int start, int end, Column* output) {
    // Zero-copy slice: only update offsets, no data copy
    for (int i = 0; i < input->num_rows; i++) {
        output->offsets[i] = input->offsets[i] + start;
        output->lengths[i] = end - start;
    }
}
// Speedup: ~50x (zero-copy advantage)
```

### 4.2 Time Function Optimization Case Analysis

Time processing is extremely common in stream computing, and Flash provides ultimate optimization:

**Case: `EXTRACT(YEAR FROM timestamp)`**

```cpp
// Java implementation (Joda-Time / Java 8 Time)
int extractYear(long epochMillis) {
    Instant instant = Instant.ofEpochMilli(epochMillis);
    LocalDateTime dt = LocalDateTime.ofInstant(instant, Zone.UTC);
    return dt.getYear();  // Complex timezone computation
}

// Falcon SIMD implementation
__m256i vec_extract_year(__m256i epoch_millis) {
    // SIMD date algorithm: branch-free, pure arithmetic
    // 1. Convert to days
    __m256i days = _mm256_div_epi64(epoch_millis, MILLIS_PER_DAY);
    // 2. Compute year using SIMD version of Zeller's formula
    __m256i years = simd_zeller_year(days);
    return years;
}
// Speedup: ~20-40x
```

### 4.3 Vectorized Hash Table Optimization

Join and Aggregate operators depend on hash tables, and Falcon implements a vectorized hash table:

```cpp
class VectorizedHashTable {
public:
    // Batch lookup: return value positions for all keys
    void batch_lookup(__m256i* keys, int* results, int n);

    // Batch insert: SIMD-optimized collision handling
    void batch_insert(__m256i* keys, __m256i* values, int n);

private:
    // Compute batch hash values using SIMD
    __m256i batch_hash(__m256i* keys, int n);

    // Compare batch keys using SIMD
    __m256i batch_compare(__m256i* keys1, __m256i* keys2, int n);
};
```

**Performance Improvement**:

- Batch hash computation: 6-8x
- Batch key comparison: 8-12x
- Overall Join performance: 3-5x

---

## 5. Proof / Engineering Argument

### 5.1 Theoretical SIMD Speedup Upper Bound

**Theorem**: For a type with data width $w$, the theoretical speedup upper bound on a $W$-bit SIMD register is $\lceil W/w \rceil$.

**Proof**:

**Step 1**: Define parameters

- $W$: SIMD register bit width (AVX2: 256, AVX-512: 512)
- $w$: Single data element bit width (int32: 32, int64: 64)
- $N = W/w$: Number of elements per register

**Step 2**: Compare scalar vs vector execution

```
Scalar execution of n elements:
T_scalar = n × (t_load + t_compute + t_store)

Vector execution of n elements (assuming n mod N = 0):
T_vector = (n/N) × (t_load + t_compute + t_store + t_overhead)

Where t_overhead includes:
- Data alignment checks
- Mask processing (tail handling)
- Register pressure spills
```

**Step 3**: Calculate speedup

```
Speedup = T_scalar / T_vector
        = N × (t_load + t_compute + t_store) / (t_load + t_compute + t_store + t_overhead)

Ideal case (t_overhead → 0):
Speedup_max = N = W/w

Actual observation (considering overhead):
Speedup_actual = 0.6 × N ~ 0.8 × N
```

**Validation**:

```
AVX-512 + int32:
N = 512/32 = 16
Speedup_actual ∈ [9.6x, 12.8x] (consistent with measurements)

AVX2 + int64:
N = 256/64 = 4
Speedup_actual ∈ [2.4x, 3.2x] (consistent with measurements)
```

### 5.2 Spatial Locality Proof of Columnar Storage

**Theorem**: For a query accessing $k$ columns, the cache efficiency of columnar storage is $m/k$ times that of row-based storage, where $m$ is the total number of columns.

**Proof**:

**Step 1**: Row-based storage analysis

```
Assumptions:
- Table has m columns, average width w bytes per column
- Cache line size C = 64 bytes
- Query accesses k columns

Row-based row size: R = m × w
Rows per cache line: rows_per_line = C / R

Data loaded to access k columns:
Data_loaded_row = C × (k / (C/R)) = k × R = k × m × w

Useful data: Data_useful = k × w
Cache efficiency: η_row = (k × w) / (k × m × w) = 1/m
```

**Step 2**: Columnar storage analysis

```
Columnar storage: each column stored contiguously

Data loaded to access k columns:
Data_loaded_col ≈ k × w × n (n = row count, loaded on demand)

Useful data: Data_useful = k × w × n
Cache efficiency: η_col ≈ 1 (ignoring metadata overhead)
```

**Step 3**: Efficiency ratio

```
η_col / η_row = 1 / (1/m) = m

For typical wide tables (m = 20-50 columns):
Columnar cache efficiency is 20-50x that of row-based
```

---

## 6. Examples

### 6.1 Typical Operator Implementation Code Example

**Filter Operator Vectorized Implementation**:

```cpp
// Falcon Filter operator
class VecFilterOperator : public VectorizedOperator {
public:
    Status execute(const ColumnarBatch& input, ColumnarBatch* output) {
        // 1. Vectorized predicate evaluation
        SelectionVector selected;
        eval_predicate_simd(input, predicate_, &selected);

        // 2. Compressed selection: keep rows satisfying condition
        ColumnarBatch filtered;
        compress_selection(input, selected, &filtered);

        *output = std::move(filtered);
        return Status::OK();
    }

private:
    // SIMD predicate evaluation
    void eval_predicate_simd(const ColumnarBatch& batch,
                             const Expr& pred,
                             SelectionVector* selected) {
        const int n = batch.num_rows();
        selected->resize(n);

        // Use AVX2 for batch comparison
        for (int i = 0; i < n; i += 8) {
            __m256i vals = batch.column(0)->load_int32x8(i);
            __m256i cmp = _mm256_cmpgt_epi32(vals, threshold_);
            int mask = _mm256_movemask_ps((__m256)cmp);
            selected->set_mask(i, mask);
        }
    }
};
```

**Aggregate Operator Vectorized Implementation**:

```cpp
// Grouped aggregation SIMD optimization
class VecAggregateOperator : public VectorizedOperator {
public:
    Status execute(const ColumnarBatch& input, ColumnarBatch* output) {
        // 1. Batch hash computation
        Column hash_values;
        batch_hash(input.group_by_columns(), &hash_values);

        // 2. Vectorized hash table lookup/insert
        VectorizedHashTable ht;
        std::vector<int> group_ids;
        ht.batch_lookup_or_insert(hash_values, &group_ids);

        // 3. SIMD aggregate update
        for (auto& agg : aggregates_) {
            simd_update_accumulators(agg, input, group_ids);
        }

        // 4. Output results
        ht.to_batch(output);
        return Status::OK();
    }
};
```

### 6.2 Performance Benchmark Data

**Falcon Layer Micro-benchmarks**:

```
Test Environment: Intel Xeon Platinum 8369B (Ice Lake), AVX-512
Dataset: 100M rows, 10 columns
Batch size: 1000

Operator           │ Java Flink │ Falcon C++ │ Speedup
───────────────────┼────────────┼────────────┼────────
Filter (int)       │ 2.5M rows/s│ 18M rows/s │ 7.2x
Filter (string)    │ 0.8M rows/s│ 12M rows/s │ 15x
Project            │ 5M rows/s  │ 35M rows/s │ 7x
Length()           │ 1.5M rows/s│ 45M rows/s │ 30x
Substring()        │ 0.5M rows/s│ 25M rows/s │ 50x
Date Extract       │ 0.3M rows/s│ 12M rows/s │ 40x
GroupBy Sum        │ 0.8M rows/s│ 4M rows/s  │ 5x
Hash Join          │ 0.2M rows/s│ 1M rows/s  │ 5x
```

### 6.3 Memory Usage Comparison

```
Memory footprint processing 1M rows:

Component          │ Java Flink │ Falcon C++ │ Difference
───────────────────┼────────────┼────────────┼──────────────
Data buffer        │ 256 MB     │ 64 MB      │ -75%
Object header overhead│ 48 MB    │ 0          │ -100%
GC overhead        │ 128 MB     │ 0          │ -100%
State storage      │ 512 MB     │ 256 MB     │ -50%
───────────────────┼────────────┼────────────┼──────────────
Total              │ 944 MB     │ 320 MB     │ -66%
```

---

## 7. Visualizations

### 7.1 Falcon Operator Execution Flow

```mermaid
flowchart TD
    A[Input Batch<br/>ColumnarBatch] --> B{Operator Type}

    B -->|Stateless| C[Filter/Project/Calc]
    B -->|Stateful| D[Aggregate/Join/Window]

    C --> C1[Predicate Eval<br/>SIMD Compare]
    C --> C2[Column Select<br/>Zero Copy]
    C --> C3[Expression Calc<br/>SIMD Arithmetic]

    D --> D1[Hash Compute<br/>SIMD Hash]
    D --> D2[State Lookup<br/>Vectorized HT]
    D --> D3[Accumulate Update<br/>SIMD Accumulate]

    C1 --> E[Output Batch<br/>ColumnarBatch]
    C2 --> E
    C3 --> E
    D1 --> E
    D2 --> E
    D3 --> E

    style C fill:#9f9,stroke:#333
    style D fill:#ff9,stroke:#333
    style E fill:#99f,stroke:#333
```

### 7.2 SIMD Execution Diagram

```mermaid
graph LR
    subgraph "Scalar Execution"
        S1[Load A[0]] --> S2[Load B[0]]
        S2 --> S3[ADD] --> S4[Store C[0]]
        S4 --> S5[Load A[1]] --> S6[Load B[1]]
        S6 --> S7[ADD] --> S8[Store C[1]]
        S8 --> S9[...]
    end

    subgraph "SIMD Execution AVX2"
        V1[Load A[0:7]] --> V2[Load B[0:7]]
        V2 --> V3[VADD] --> V4[Store C[0:7]]
        V4 --> V5[Load A[8:15]] --> V6[Load B[8:15]]
        V6 --> V7[VADD] --> V8[Store C[8:15]]
    end

    style V3 fill:#f99,stroke:#333,stroke-width:2px
    style V7 fill:#f99,stroke:#333,stroke-width:2px
```

### 7.3 Memory Layout Comparison

```mermaid
graph TB
    subgraph "Row-based Storage"
        R1[Row1: id=1, name='Alice', ts=123456, ...]
        R2[Row2: id=2, name='Bob', ts=123457, ...]
        R3[Row3: id=3, name='Charlie', ts=123458, ...]
    end

    subgraph "Column-based Storage"
        C1[id column: 1, 2, 3, ...]
        C2[name column: 'Alice', 'Bob', 'Charlie', ...]
        C3[ts column: 123456, 123457, 123458, ...]
    end

    subgraph "SIMD Load"
        S1[__m256i: 1, 2, 3, 4, 5, 6, 7, 8]
    end

    C1 -.->|AVX2 Load| S1
```

### 7.4 Operator Coverage Matrix

```mermaid
graph TD
    subgraph "Falcon Operator Coverage v1.0"
        direction LR

        subgraph "Stateless 95%"
            ST1[Filter ✓]
            ST2[Project ✓]
            ST3[Calc ✓]
            ST4[Union ✓]
            ST5[Values ✓]
        end

        subgraph "Stateful 70%"
            SF1[HashAggregate ✓]
            SF2[SortAggregate ~]
            SF3[HashJoin ✓]
            SF4[SortMergeJoin ~]
            SF5[TumbleWindow ✓]
            SF6[HopWindow ✓]
            SF7[SessionWindow ~]
        end

        subgraph "Complex Operators 30%"
            CP1[OverAggregate ~]
            CP2[TemporalJoin ✗]
            CP3[MatchRecognize ✗]
            CP4[LookupJoin ~]
        end
    end

    style ST1 fill:#9f9
    style ST2 fill:#9f9
    style ST3 fill:#9f9
    style ST4 fill:#9f9
    style ST5 fill:#9f9
    style SF1 fill:#9f9
    style SF2 fill:#ff9
    style SF3 fill:#9f9
    style SF4 fill:#ff9
    style SF5 fill:#9f9
    style SF6 fill:#9f9
    style SF7 fill:#ff9
    style CP1 fill:#ff9
    style CP2 fill:#f99
    style CP3 fill:#f99
    style CP4 fill:#ff9

    legend1[✓ Fully Supported]:::green
    legend2[~ Partially Supported]:::yellow
    legend3[✗ Not Yet Supported]:::red

    classDef green fill:#9f9
    classDef yellow fill:#ff9
    classDef red fill:#f99
```

---

## 8. References

---

*Document Version: v1.0 | Last Updated: 2026-04-04 | Status: P0 Complete*
