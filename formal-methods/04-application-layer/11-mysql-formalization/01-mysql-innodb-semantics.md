# MySQL InnoDB 存储引擎形式化语义

> **所属阶段**: Formal-Methods/Application-Layer | **前置依赖**: [02-distributed-transactions](../02-distributed-transactions/), [03-consistency-models](../../03-consistency-models/) | **形式化等级**: L5 (完全形式化)
> **版本**: v1.0 | **创建日期**: 2026-04-10

---

## 1. 概念定义 (Definitions)

### 1.1 MySQL 架构形式化定义

**定义 Def-FM-11-01 (MySQL 服务器架构)**

MySQL 服务器架构可形式化定义为五元组：

$$\mathcal{M} = \langle C, P, S, E, D \rangle$$

其中：

- $C$: 连接管理层 (Connection Layer) — 处理客户端连接和认证
- $P$: 解析优化层 (Parser/Optimizer Layer) — SQL解析、查询优化
- $S$: 服务层 (Service Layer) — 内置函数、存储过程、触发器
- $E$: 存储引擎层 (Storage Engine Layer) — 可插拔存储引擎接口
- $D$: 存储层 (Storage Layer) — 文件系统和磁盘I/O

**定义 Def-FM-11-02 (存储引擎接口)**

存储引擎接口 $\mathcal{I}_{SE}$ 定义为一组操作集合：

$$\mathcal{I}_{SE} = \{ \text{create}, \text{open}, \text{close}, \text{read}, \text{write}, \text{delete}, \text{index\_read}, \text{index\_write}, \text{commit}, \text{rollback} \}$$

### 1.2 InnoDB 存储引擎定义

**定义 Def-FM-11-03 (InnoDB 存储引擎)**

InnoDB 存储引擎形式化为八元组：

$$\mathcal{I}_{InnoDB} = \langle B, T, L, R, M, F, W, G \rangle$$

其中各组件定义为：

| 组件 | 符号 | 语义描述 |
|------|------|----------|
| Buffer Pool | $B$ | 内存中数据页的缓存区域，$B = \{ p_i \mid p_i = \langle page\_id, data, lsn, dirty \rangle \}$ |
| Transaction System | $T$ | 事务管理系统，跟踪活跃事务状态 |
| Lock System | $L$ | 锁管理系统，维护锁的授予等待图 |
| Recovery System | $R$ | 崩溃恢复系统，基于Redo/Undo日志 |
| MVCC System | $M$ | 多版本并发控制系统 |
| File System | $F$ | 表空间文件管理，包括系统表空间、独立表空间、通用表空间、Undo表空间、临时表空间 |
| Write-Ahead Log | $W$ | 预写日志系统，包含Redo Log和Undo Log |
| Change Buffer | $G$ | 更改缓冲区，延迟非唯一二级索引的写入 |

**定义 Def-FM-11-04 (表空间形式化)**

表空间 $\mathcal{TS}$ 定义为页的集合，每个表空间有唯一的space ID：

$$\mathcal{TS}_{sid} = \{ p_j \mid p_j \in \text{Page}, \text{space}(p_j) = sid \}$$

表空间类型：

- $\mathcal{TS}_{sys}$: 系统表空间 (space_id = 0)，包含数据字典、双写缓冲区、变更缓冲区
- $\mathcal{TS}_{undo}$: Undo表空间，存储回滚段
- $\mathcal{TS}_{temp}$: 临时表空间，存储临时表数据
- $\mathcal{TS}_{user}$: 用户表空间，独立表空间或通用表空间

### 1.3 MVCC 模型形式化定义

**定义 Def-FM-11-05 (元组版本链)**

每个数据行的历史版本形成版本链，形式化为链表结构：

$$\text{VersionChain}(row) = [v_1 \xrightarrow{next} v_2 \xrightarrow{next} \cdots \xrightarrow{next} v_n]$$

其中每个版本 $v_i = \langle trx\_id, roll\_ptr, data, db\_row\_id \rangle$ 包含：

- $trx\_id$: 创建此版本的事务ID (6字节)
- $roll\_ptr$: 指向Undo日志中前一版本的指针 (7字节)
- $data$: 实际行数据
- $db\_row\_id$: 隐藏主键 (若表无显式主键)

**定义 Def-FM-11-06 (Read View 形式化)**

Read View 是事务的快照视图，形式化为四元组：

$$\text{ReadView} = \langle m\_low\_limit\_id, m\_up\_limit\_id, m\_creator\_trx\_id, m\_ids \rangle$$

其中：

- $m\_low\_limit\_id$: 低水位线，已分配的最大事务ID+1，事务ID ≥ 此值的变更不可见
- $m\_up\_limit\_id$: 高水位线，活跃事务列表中最小事务ID，事务ID < 此值的变更可见
- $m\_creator\_trx\_id$: 创建此Read View的事务ID
- $m\_ids$: 创建Read View时活跃事务ID集合

**定义 Def-FM-11-07 (可见性判定函数)**

给定Read View $RV$ 和行版本 $v$ 的事务ID $trx\_id(v)$，可见性判定函数为：

$$\text{Visible}(RV, v) = \begin{cases}
\text{true} & \text{if } trx\_id(v) = m\_creator\_trx\_id \\
\text{true} & \text{if } trx\_id(v) < m\_up\_limit\_id \\
\text{false} & \text{if } trx\_id(v) \geq m\_low\_limit\_id \\
\text{true} & \text{if } trx\_id(v) \notin m\_ids \land m\_up\_limit\_id \leq trx\_id(v) < m\_low\_limit\_id \\
\text{false} & \text{otherwise}
\end{cases}$$

### 1.4 事务隔离级别形式化

**定义 Def-FM-11-08 (ANSI SQL 隔离级别)**

四种标准隔离级别基于三种异常现象定义：

| 隔离级别 | 脏读 (P1) | 不可重复读 (P2) | 幻读 (P3) |
|----------|-----------|-----------------|-----------|
| READ UNCOMMITTED | 允许 | 允许 | 允许 |
| READ COMMITTED | 禁止 | 允许 | 允许 |
| REPEATABLE READ | 禁止 | 禁止 | 部分禁止 |
| SERIALIZABLE | 禁止 | 禁止 | 禁止 |

**定义 Def-FM-11-09 (InnoDB 隔离级别实现)**

InnoDB 通过锁和MVCC的组合实现隔离级别：

$$\text{IsolationImpl}(level) = \langle \text{lock\_mode}, \text{read\_view\_strategy}, \text{gap\_locking} \rangle$$

具体实现映射：

| 隔离级别 | 一致性读 | 锁定读 | 间隙锁 |
|----------|----------|--------|--------|
| READ UNCOMMITTED | 无Read View | 无锁 | 否 |
| READ COMMITTED | 每次查询新Read View | 行锁 | 否 |
| REPEATABLE READ | 事务开始时Read View | 行锁+间隙锁 | 是 |
| SERIALIZABLE | 无MVCC (全锁定) | 全表锁 | 是 |

---

## 2. 形式化模型 (Formal Model)

### 2.1 缓冲区管理形式化

**定义 Def-FM-11-10 (缓冲池页状态)**

缓冲池中的每个页具有状态机：

$$\text{PageState} \in \{ \text{FREE}, \text{CLEAN}, \text{DIRTY}, \text{IO\_READ}, \text{IO\_WRITE} \}$$

状态转换函数：

$$\delta: \text{PageState} \times \text{Event} \rightarrow \text{PageState}$$

**引理 Lemma-FM-11-01 (缓冲池不变量)**

对于缓冲池 $B$ 中的任意页 $p$：

$$\forall p \in B: (p.state = \text{DIRTY}) \implies (p.lsn \geq p.oldest\_modification)$$

**定义 Def-FM-11-11 (LRU 链表形式化)**

InnoDB使用改进的LRU算法，将缓冲池分为两个区域：

$$LRU = \langle LRU\_young, LRU\_old \rangle$$

- $LRU\_young$: 新子列表 (默认占5/8)，热点数据
- $LRU\_old$: 旧子列表 (默认占3/8)，冷数据

插入点位于 $LRU\_old$ 头部（距离LRU尾部的3/8处）。

**形式化操作**：

$$\text{access}(page): \begin{cases}
\text{若 } page \in LRU\_young: & \text{移至 } LRU\_young \text{ 头部} \\
\text{若 } page \in LRU\_old \land \text{停留} > \text{innodb\_old\_blocks\_time}: & \text{移至 } LRU\_young \text{ 头部} \\
\text{否则}: & \text{移至 } LRU\_old \text{ 头部}
\end{cases}$$

### 2.2 页结构形式化

**定义 Def-FM-11-12 (InnoDB 页通用头部)**

每个InnoDB页（默认16KB）具有通用页头：

$$\text{PageHeader} = \langle \text{FIL\_HEADER}, \text{PAGE\_HEADER}, \text{body}, \text{FIL\_TRAILER} \rangle$$

FIL_HEADER (38字节) 包含：
- `FIL_PAGE_SPACE`: 表空间ID (4字节)
- `FIL_PAGE_OFFSET`: 页偏移量 (4字节)
- `FIL_PAGE_PREV`: 前一页指针 (4字节)
- `FIL_PAGE_NEXT`: 后一页指针 (4字节)
- `FIL_PAGE_LSN`: 最后修改的LSN (8字节)
- `FIL_PAGE_TYPE`: 页类型 (2字节)
- `FIL_PAGE_FILE_FLUSH_LSN`: 表空间文件刷盘LSN (8字节)

**定义 Def-FM-11-13 (页类型集合)**

$$\text{PageType} = \{ \text{INDEX}, \text{UNDO\_LOG}, \text{INODE}, \text{IBUF\_FREE\_LIST}, \text{IBUF\_BITMAP}, \text{SYS}, \text{TRX\_SYS}, \text{FSP\_HDR}, \text{XDES}, \text{BLOB} \}$$

### 2.3 索引结构形式化 (B+树)

**定义 Def-FM-11-14 (B+树形式化)**

InnoDB的B+树索引定义为六元组：

$$\mathcal{B}^+ = \langle r, K, V, C, L, h \rangle$$

其中：
- $r$: 根节点页号
- $K$: 键值空间，全序集 $(K, \leq)$
- $V$: 值空间，$V = \text{Record} \cup \{\text{pointer}\}$
- $C$: 子节点指针函数，$C: K \rightarrow \text{PageNo}$
- $L$: 叶子节点链表，双向链表连接所有叶子
- $h$: 树高度

**定义 Def-FM-11-15 (聚簇索引)**

聚簇索引的叶子节点存储完整行数据：

$$\text{ClusteredKey} = \begin{cases}
\text{PrimaryKey} & \text{if defined} \\
\text{DB\_ROW\_ID} & \text{otherwise (自动生成)}
\end{cases}$$

聚簇索引值：$V_{clustered} = \text{FullRow}$（除主键外的所有列）

**定义 Def-FM-11-16 (二级索引)**

二级索引的叶子节点存储索引键和聚簇索引键：

$$V_{secondary} = \text{IndexColumns} \times \text{ClusteredKey}$$

回表操作：通过二级索引获取聚簇索引键，再查询聚簇索引获取完整行。

**引理 Lemma-FM-11-02 (B+树节点容量)**

对于键大小为 $k$ 字节、指针大小为 $p$ 字节（6字节）的B+树：

- 内部节点最大子节点数：$n = \left\lfloor \frac{16384 - 38 - 36}{k + p} \right\rfloor$
- 叶子节点最大记录数：取决于行大小

**定义 Def-FM-11-17 (索引页记录格式)**

页内记录采用紧凑格式存储：

$$\text{Record} = \langle \text{variable\_header}, \text{null\_bitmap}, \text{variable\_length}, \text{row\_data} \rangle$$

变长字段头包含长度信息，NULL位图标记NULL列。

### 2.4 日志系统形式化

**定义 Def-FM-11-18 (日志序列号 LSN)**

LSN 是单调递增的64位整数，表示日志字节偏移：

$$LSN: \mathbb{N}_{64}, \quad LSN_{t+1} = LSN_t + \text{log\_record\_size}$$

关键LSN值：
- $flushed\_to\_disk\_lsn$: 已刷入磁盘的最大LSN
- $checkpoint\_lsn$: 检查点LSN，之前的日志可安全清除
- $max\_page\_lsn$: 各页的最新修改LSN

**定义 Def-FM-11-19 (Redo 日志记录)**

Redo 日志记录物理页的修改，形式化为：

$$\text{RedoRecord} = \langle type, space\_id, page\_no, offset, data, lsn \rangle$$

Redo 日志类型：
- `MLOG_1BYTE` ~ `MLOG_8BYTES`: 字节级修改
- `MLOG_WRITE_STRING`: 字符串写入
- `MLOG_REC_INSERT` / `MLOG_REC_DELETE`: 记录插入/删除
- `MLOG_LIST_END_COPY` / `MLOG_LIST_START_COPY`: 页分裂
- `MLOG_INIT_FILE_PAGE`: 新页初始化
- `MLOG_UNDO_INSERT`: Undo日志插入

**定义 Def-FM-11-20 (Undo 日志记录)**

Undo 日志用于事务回滚和MVCC，形式化为：

$$\text{UndoRecord} = \langle trx\_id, type, table\_id, primary\_key, old\_values, roll\_ptr, next\_undo \rangle$$

Undo 类型：
- `TRX_UNDO_INSERT_REC`: 插入操作的Undo（只需保存主键，用于Purge）
- `TRX_UNDO_UPD_EXIST_REC`: 更新操作的Undo（保存修改前的值）
- `TRX_UNDO_DEL_MARK_REC`: 删除标记的Undo

**定义 Def-FM-11-21 (Undo 段)**

Undo 段是Undo日志的物理容器：

$$\text{UndoSegment} = \langle \text{rseg}, \text{space}, \text{page\_no}, \text{header\_page}, \text{records} \rangle$$

回滚段（Rollback Segment）包含多个Undo段：

$$\text{RollbackSegment} = \{ \text{UndoSegment}_1, \text{UndoSegment}_2, \ldots, \text{UndoSegment}_n \}$$

InnoDB 默认有128个回滚段（`innodb_rollback_segments`）。

---

## 3. 关系建立 (Relations)

### 3.1 InnoDB 与事务理论的映射

**命题 Prop-FM-11-01 (InnoDB 事务模型映射)**

InnoDB 事务实现与理论模型的对应关系：

| 理论概念 | InnoDB 实现 | 映射关系 |
|----------|-------------|----------|
| 原子性 (Atomicity) | Undo Log | $A \mapsto \text{Undo}$ |
| 一致性 (Consistency) | 约束检查 + MVCC | $C \mapsto \text{Constraints} \times \text{MVCC}$ |
| 隔离性 (Isolation) | MVCC + 锁 | $I \mapsto \text{MVCC} \times \text{Locking}$ |
| 持久性 (Durability) | Redo Log + Double Write | $D \mapsto \text{Redo} \times \text{DoubleWrite}$ |

### 3.2 MVCC 与快照隔离的关系

**命题 Prop-FM-11-02 (InnoDB REPEATABLE READ 与快照隔离)**

InnoDB 的 REPEATABLE READ 隔离级别实现了**快照隔离（Snapshot Isolation, SI）**的变体：

$$\text{RR}_{InnoDB} = SI + \text{Gap Locking}$$

关键差异：
1. 标准SI通过"First-Committer-Wins"防止写倾斜
2. InnoDB RR通过间隙锁防止幻读，但写倾斜仍可能发生
3. InnoDB RR在唯一键冲突时提供"First-Updater-Wins"语义

### 3.3 恢复算法与ARIES的关系

**命题 Prop-FM-11-03 (InnoDB 恢复与ARIES)**

InnoDB 的恢复机制基于ARIES算法[^6]，但有以下差异：

| ARIES 特性 | InnoDB 实现 |
|------------|-------------|
| Write-Ahead Logging (WAL) | Redo Log with LSN |
| Steal/No-Force 策略 | 支持（脏页可提前刷盘） |
| Redo-Only 恢复 | 支持，基于LSN的页级重做 |
| Undo 日志 | 支持，用于回滚和MVCC |
| 模糊检查点 | 支持，基于last checkpoint LSN |
| Compensation Log Records (CLRs) | 部分支持，Redo-only |

### 3.4 锁协议与两阶段锁定的关系

**命题 Prop-FM-11-04 (InnoDB 锁协议)**

InnoDB 实现**严格两阶段锁定（Strict 2PL）**的变体：

$$\text{LockProtocol}_{InnoDB} = \text{Strict 2PL} + \text{Intention Locks} + \text{Gap Locks}$$

扩展包括：
1. **意向锁（Intention Locks）**：表级锁的层次锁协议
2. **间隙锁（Gap Locks）**：用于防止幻读和唯一性检查
3. **插入意向锁（Insert Intention Locks）**：特殊的间隙锁，允许相容的插入

---

## 4. 论证过程 (Argumentation)

### 4.1 缓冲区管理策略论证

**命题 Prop-FM-11-05 (LRU 算法改进的必要性)**

标准LRU在处理全表扫描时存在**缓冲池污染**问题：

**问题描述**：
- 全表扫描读取大量冷数据页
- 标准LRU将所有访问页移至头部
- 结果：热点数据被驱逐，缓冲池命中率骤降

**InnoDB 解决方案**：
- 使用Young/Old分区LRU
- 首次访问插入Old区头部
- 需要多次访问才能进入Young区
- 全表扫描只影响Old区，保护Young区热点数据

**论证**：设缓冲池大小为 $N$，Young区比例为 $\alpha = 5/8$

全表扫描访问 $M$ 页 ($M > N$) 的影响：
- 标准LRU：热点数据全部被驱逐，命中率 $\rightarrow 0$
- 分区LRU：Young区保持 $\alpha N$ 热点页，Old区被扫描页占据

### 4.2 MVCC 实现权衡分析

**命题 Prop-FM-11-06 (MVCC 存储开销分析)**

MVCC引入的存储开销：

| 开销类型 | 来源 | 估算公式 |
|----------|------|----------|
| 行头开销 | DB_TRX_ID + DB_ROLL_PTR | 每行13字节 |
| Undo 日志 | 历史版本存储 | 取决于更新频率和事务长度 |
| Purge 开销 | 清理历史版本 | 后台线程CPU和I/O |

**优化策略**：
1. **短事务优先**：减少Undo日志保留时间
2. **Purge 线程优化**：innodb_purge_threads（默认4个）
3. **Undo 表空间截断**：定期回收空间

### 4.3 锁粒度选择论证

**命题 Prop-FM-11-07 (锁粒度的权衡)**

InnoDB 支持多粒度锁：行锁、页锁、表锁

| 粒度 | 并发度 | 开销 | 适用场景 |
|------|--------|------|----------|
| 行锁 | 最高 | 高（锁表内存） | 高并发OLTP |
| 页锁 | 中 | 中 | 批量操作 |
| 表锁 | 低 | 低 | DDL、全表扫描 |

**自动锁升级策略**：

InnoDB 不自动进行锁升级（区别于SQL Server），原因：
1. 行锁开销在大多数场景下可接受
2. 锁升级可能导致意外死锁
3. 通过`innodb_lock_wait_timeout`控制等待

### 4.4 双写缓冲区的必要性论证

**命题 Prop-FM-11-08 (双写缓冲区的作用)**

**问题**：部分页写入（Partial Page Write）

当InnoDB刷新16KB页到磁盘时，若发生崩溃，可能只有部分数据写入：
- 磁盘扇区大小通常为512字节或4KB
- 16KB页需要4次或32次I/O
- 崩溃可能发生在任意中间状态

**双写缓冲区解决方案**：

1. **写入阶段**：
   - 先将脏页顺序写入双写缓冲区（系统表空间中2MB区域）
   - 再写入实际数据文件位置

2. **恢复阶段**：
   - 检查数据页LSN与Redo Log LSN
   - 若页损坏（checksum失败），从双写缓冲区恢复

**形式化保证**：

$$\text{DoubleWrite} \implies \text{AtomicPageWrite}$$

即：双写机制确保页写入的原子性，避免部分页损坏。

---

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

### 5.1 可串行化证明

**定理 Thm-FM-11-01 (REPEATABLE READ + 间隙锁的可串行化)**

在InnoDB的REPEATABLE READ隔离级别下，对于满足以下条件的调度：
1. 所有读取操作都使用锁定读（`SELECT ... FOR UPDATE` 或 `SELECT ... LOCK IN SHARE MODE`）
2. 所有写入操作都获取排他锁

该调度的执行结果等价于某个串行调度的执行结果。

**证明**：

**步骤1：锁类型定义**

定义锁的相容矩阵 $C: \text{LockType} \times \text{LockType} \rightarrow \{\text{true}, \text{false}\}$

|  | IS | IX | S | X | GAP | IGAP |
|--|----|----|---|---|-----|------|
| IS | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| IX | ✓ | ✓ | ✗ | ✗ | ✓ | ✓ |
| S | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ |
| X | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| GAP | ✓ | ✓ | ✗ | ✗ | ✓ | ✓ |
| IGAP | ✓ | ✓ | ✗ | ✗ | ✓ | ✓ |

其中：IS=意向共享锁，IX=意向排他锁，S=共享锁，X=排他锁，GAP=间隙锁，IGAP=插入意向锁

**步骤2：冲突可串行化条件**

根据冲突可串行化理论，若调度 $S$ 的优先图（Precedence Graph）无环，则 $S$ 是冲突可串行化的。

优先图 $G = (V, E)$，其中：
- $V = \{T_1, T_2, \ldots, T_n\}$ 是事务集合
- $(T_i, T_j) \in E$ 当且仅当存在冲突操作对 $(o_i, o_j)$ 且 $o_i \prec_S o_j$

**步骤3：2PL 保证可串行化**

InnoDB实现严格两阶段锁定：
- ** growing phase**：事务获取所需的所有锁
- **shrinking phase**：事务提交或回滚时释放所有锁

根据两阶段锁定定理[^2]，任何遵循2PL的调度都是冲突可串行化的。

**步骤4：InnoDB锁协议的2PL特性**

验证InnoDB满足2PL：
1. 锁获取：事务执行期间按需获取锁
2. 锁释放：
   - 事务提交时：释放所有锁
   - 事务回滚时：释放所有锁
   - 锁等待超时：回滚事务

因此，InnoDB的锁定读操作遵循2PL协议。

**步骤5：间隙锁与幻读预防**

标准2PL无法防止幻读，因为幻读涉及"幻影元组"（新插入的满足查询条件的行）。

InnoDB通过间隙锁解决这个问题：
- 范围查询获取间隙锁，锁定索引记录之间的间隙
- 其他事务无法在锁定间隙内插入新记录
- 这实现了**谓词锁定（Predicate Locking）**的效果

**结论**：

在REPEATABLE READ隔离级别下，使用锁定读的事务调度等价于2PL调度，因此是冲突可串行化的。

$$\therefore \text{InnoDB RR with locking reads} \implies \text{Serializable}$$

∎

### 5.2 恢复正确性证明

**定理 Thm-FM-11-02 (崩溃恢复正确性)**

InnoDB的崩溃恢复算法保证：
1. 已提交事务的修改持久化到数据库
2. 未提交事务的修改被撤销
3. 数据库恢复到一致性状态

**证明**：

**步骤1：Redo 阶段正确性**

Redo阶段重放从checkpoint开始的Redo日志：

$$\text{RedoPhase} = \{ \text{apply}(r) \mid r \in \text{RedoLog}, r.lsn \geq \text{checkpoint\_lsn} \}$$

对于每条Redo记录 $r = \langle page, offset, data, lsn \rangle$：

$$
\text{apply}(r) = \begin{cases}
\text{write}(page, offset, data) & \text{if } page.lsn < r.lsn \\
\text{skip} & \text{otherwise}
\end{cases}$$

**引理**：Redo操作是幂等的（Idempotent）

**证明**：若页已包含该修改（page.lsn ≥ r.lsn），则跳过。因此多次应用Redo不会改变结果。

**步骤2：Undo 阶段正确性**

Undo阶段回滚活跃事务：

$$\text{UndoPhase} = \{ \text{rollback}(T) \mid T \in \text{ActiveTransactionsAtCrash} \}$$

回滚操作：

1. 从Undo日志链读取修改前数据
2. 将页恢复到修改前状态
3. 写入补偿日志记录（CLR）

**步骤3：持久性保证**

设事务 $T$ 的提交LSN为 $lsn_{commit}$：

- **前提**：事务提交前，Redo日志已刷盘（WAL协议）
- **恢复**：Redo阶段重放所有已刷盘的Redo记录
- **结论**：已提交事务的修改必定被恢复

**步骤4：原子性保证**

设事务 $T$ 在崩溃时未提交：

- Undo日志记录了 $T$ 的所有修改
- Undo阶段按相反顺序应用Undo记录
- 结果：$T$ 的所有修改被撤销，数据库状态如同 $T$ 从未执行

**步骤5：一致性保证**

数据库一致性由以下机制保证：

1. 约束检查：在修改前验证约束
2. 级联操作：外键约束的级联更新/删除
3. 触发器：业务规则的一致性维护

恢复过程保证：

- 已提交事务：所有约束、级联、触发器效果完整恢复
- 未提交事务：所有效果被撤销，不破坏一致性

**结论**：

InnoDB的崩溃恢复算法正确实现了ARIES协议，保证ACID属性中的原子性和持久性。

$$\therefore \text{InnoDB Recovery} \implies \text{Correctness}$$

∎

### 5.3 MVCC 可见性正确性证明

**定理 Thm-FM-11-03 (MVCC 可见性判定正确性)**

InnoDB的MVCC可见性判定函数 $\text{Visible}(RV, v)$ 正确实现了快照隔离的可见性规则。

**证明**：

**步骤1：快照隔离的可见性规则**

根据快照隔离定义[^1]，事务 $T$ 的快照包含：

- 所有在 $T$ 开始前已提交的事务的修改
- 不包括在 $T$ 开始时仍活跃的事务的修改
- 包括 $T$ 自身的修改

**步骤2：Read View 与快照的对应**

设事务 $T$ 的Read View为 $RV_T = \langle low, up, creator, active \rangle$：

| Read View 字段 | 快照隔离语义 |
|----------------|--------------|
| $creator = T.id$ | 自身事务ID |
| $up$ | 最早活跃事务的ID，ID < up的事务在T开始前已提交 |
| $low$ | 最新分配事务ID+1，ID ≥ low的事务在T开始后启动 |
| $active$ | T开始时活跃的事务集合 |

**步骤3：可见性条件的形式化验证**

对于行版本 $v$ 的事务ID $trx\_id(v)$：

1. **$trx\_id(v) = creator$**（自身修改）：
   - 语义：事务可见自己的修改
   - 判定：$\text{Visible} = \text{true}$ ✓

2. **$trx\_id(v) < up$**（在T开始前已提交）：
   - 语义：这些事务在T开始前已提交，其修改应可见
   - 判定：$\text{Visible} = \text{true}$ ✓

3. **$trx\_id(v) \geq low$**（在T开始后启动）：
   - 语义：这些事务在T开始后启动，其修改不应可见
   - 判定：$\text{Visible} = \text{false}$ ✓

4. **$up \leq trx\_id(v) < low \land trx\_id(v) \notin active$**（T执行期间提交）：
   - 语义：这些事务在T开始前已启动但已提交，其修改应可见
   - 判定：$\text{Visible} = \text{true}$ ✓

5. **$up \leq trx\_id(v) < low \land trx\_id(v) \in active$**（T开始时仍活跃）：
   - 语义：这些事务在T开始时仍活跃，其修改不应可见
   - 判定：$\text{Visible} = \text{false}$ ✓

**步骤4：完备性证明**

所有可能的 $trx\_id(v)$ 值被划分为互斥的五种情况：

- $trx\_id(v) = creator$
- $trx\_id(v) < up$
- $trx\_id(v) \geq low$
- $up \leq trx\_id(v) < low \land trx\_id(v) \notin active$
- $up \leq trx\_id(v) < low \land trx\_id(v) \in active$

且每种情况都正确实现了快照隔离语义。

**结论**：

InnoDB的MVCC可见性判定函数正确实现了快照隔离。

$$\therefore \text{MVCC Visibility} \iff \text{Snapshot Isolation Semantics}$$

∎

---

## 6. 实例验证 (Examples)

### 6.1 索引操作实例

#### 6.1.1 聚簇索引插入流程

```sql
-- 创建表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 插入数据
INSERT INTO users (name, email) VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com'),
    ('Charlie', 'charlie@example.com');
```

**内部执行流程**：

1. **获取自增值**：从内存计数器获取 `id = 1`
2. **构造行记录**：
   - DB_TRX_ID = 当前事务ID (假设为 100)
   - DB_ROLL_PTR = NULL（首次插入）
   - 列数据：(1, 'Alice', '<alice@example.com>', NOW())
3. **定位插入位置**：在聚簇索引B+树中找到 `id = 1` 应插入的叶子页
4. **检查唯一性**：若email有唯一索引，检查唯一性约束
5. **写入页**：在目标页的用户记录区插入新记录
6. **更新页目录**：维护页内稀疏目录，优化二分查找
7. **写入Undo日志**：
   - 类型：TRX_UNDO_INSERT_REC
   - 内容：主键值 (1)，用于Purge时物理删除

#### 6.1.2 二级索引维护

```sql
-- email 列的二级索引插入
-- 索引键: ('alice@example.com', 1)
-- 值: 聚簇索引键 (id = 1)
```

**Change Buffer 优化**：

若 `email` 索引页不在缓冲池，且启用了Change Buffer：

1. 不立即读取索引页
2. 将插入操作缓存在Change Buffer
3. 后续读取时合并或定期后台合并
4. 减少随机I/O

### 6.2 事务执行实例

#### 6.2.1 并发事务场景

```sql
-- 事务A
START TRANSACTION;
SELECT * FROM accounts WHERE id = 1;  -- 余额: 1000
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- 此时未提交

-- 事务B (并发)
START TRANSACTION;
SELECT * FROM accounts WHERE id = 1;  -- 取决于隔离级别
-- READ UNCOMMITTED: 看到 900 (脏读)
-- READ COMMITTED: 看到 1000 (读取已提交版本)
-- REPEATABLE READ: 看到 1000 (快照读)
```

**REPEATABLE READ 隔离级别的Read View变化**：

```
时间线:
T1: 事务A启动, 创建Read View A (creator_trx_id = 100, m_ids = {100})
T2: 事务B启动, 创建Read View B (creator_trx_id = 101, m_ids = {100, 101})
T3: 事务A更新记录 (trx_id = 100), 写入Undo日志
T4: 事务B查询
    - 检查行版本trx_id = 100
    - 100 ∈ m_ids (活跃事务)
    - 100 ≠ creator_trx_id (不是B自己)
    - 不可见！沿roll_ptr找到旧版本
T5: 事务A提交
T6: 事务B再次查询 (REPEATABLE READ)
    - 仍使用创建时的Read View B
    - 仍然不可见trx_id = 100的版本
    - 结果与T4相同 (可重复读!)
```

#### 6.2.2 幻读场景演示

```sql
-- 事务A
START TRANSACTION;
SELECT * FROM orders WHERE amount > 1000;  -- 返回2条记录

-- 事务B (并发)
START TRANSACTION;
INSERT INTO orders (amount) VALUES (1500);  -- 插入满足条件的记录
COMMIT;

-- 事务A继续
SELECT * FROM orders WHERE amount > 1000;
-- READ COMMITTED: 返回3条记录 (幻读!)
-- REPEATABLE READ: 返回2条记录 (无幻读，间隙锁阻止插入)
```

**间隙锁阻止幻读机制**：

```
索引结构 (amount列):
[100] -- [500] -- [800] -- [1200] -- [1500] -- [2000]

事务A查询 WHERE amount > 1000:
- 锁定记录 [1200] 的行锁
- 锁定间隙 (800, 1200] 的间隙锁
- 锁定间隙 (1200, 1500] 的间隙锁
- 锁定间隙 (1500, 2000] 的间隙锁
- 锁定间隙 (2000, +∞) 的间隙锁

事务B尝试插入 amount = 1500:
- 需要获取 (1200, 1500] 间隙的插入意向锁
- 与事务A的间隙锁冲突！
- 事务B等待，直到事务A释放锁
```

### 6.3 并发控制实例

#### 6.3.1 死锁检测与解决

```sql
-- 事务A
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- 获取id=1的X锁
-- 暂停...
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- 等待id=2的X锁

-- 事务B (并发)
START TRANSACTION;
UPDATE accounts SET balance = balance - 50 WHERE id = 2;   -- 获取id=2的X锁
UPDATE accounts SET balance = balance + 50 WHERE id = 1;   -- 等待id=1的X锁 (死锁!)
```

**死锁检测**：

InnoDB维护锁的等待图（Wait-For Graph）：

```
等待图:
T1 (事务A) --等待--> 锁(id=2) --被持有--> T2 (事务B)
T2 (事务B) --等待--> 锁(id=1) --被持有--> T1 (事务A)

形成环: T1 -> T2 -> T1 (死锁!)
```

**死锁解决**：

1. 检测到死锁后，选择代价较小的事务回滚
2. 通常选择修改行数较少的事务
3. 回滚事务收到错误：`ERROR 1213 (40001): Deadlock found`
4. 另一个事务继续执行

#### 6.3.2 锁等待超时处理

```sql
-- 设置锁等待超时
SET SESSION innodb_lock_wait_timeout = 50;  -- 默认50秒

-- 事务A持有锁不释放
START TRANSACTION;
UPDATE products SET stock = stock - 1 WHERE id = 1;
-- 不提交...

-- 事务B尝试更新同一行
START TRANSACTION;
UPDATE products SET stock = stock - 1 WHERE id = 1;
-- 等待50秒后:
-- ERROR 1205 (HY000): Lock wait timeout exceeded
```

### 6.4 代码示例

#### 6.4.1 乐观锁实现

```sql
-- 使用版本号实现乐观锁
CREATE TABLE inventory (
    product_id INT PRIMARY KEY,
    quantity INT NOT NULL,
    version INT NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 读取商品信息（包含版本号）
SELECT product_id, quantity, version
FROM inventory
WHERE product_id = 1;
-- 返回: (1, 100, 5)

-- 更新库存（带版本号检查）
UPDATE inventory
SET quantity = quantity - 1,
    version = version + 1,
    updated_at = NOW()
WHERE product_id = 1
  AND version = 5;  -- 乐观锁检查

-- 检查影响行数
-- 若 affected_rows = 1: 更新成功
-- 若 affected_rows = 0: 版本冲突，需要重试
```

#### 6.4.2 分布式事务（XA）

```sql
-- 应用程序代码 (伪代码)
-- 使用XA实现跨库事务

-- 第一阶段：准备
XA START 'trx-001';
    INSERT INTO db1.orders (...);
XA END 'trx-001';
XA PREPARE 'trx-001';  -- 准备阶段，记录Redo/Undo

-- 协调器记录事务状态
-- 若所有参与者都PREPARE成功，则提交
-- 若有参与者失败，则回滚

-- 第二阶段：提交
XA COMMIT 'trx-001';   -- 或 XA ROLLBACK 'trx-001'
```

**XA事务的两阶段提交**：

```
阶段1 (Prepare):
    协调器 -> 参与者1: PREPARE
    协调器 -> 参与者2: PREPARE
    参与者1 -> 协调器: YES (已记录Prepare日志)
    参与者2 -> 协调器: YES (已记录Prepare日志)

阶段2 (Commit):
    协调器持久化决策: COMMIT
    协调器 -> 参与者1: COMMIT
    协调器 -> 参与者2: COMMIT
    参与者1 -> 协调器: ACK
    参与者2 -> 协调器: ACK
```

#### 6.4.3 防止丢失更新

```sql
-- 场景: 两个会话同时读取并更新同一行

-- 会话1
START TRANSACTION;
SELECT balance INTO @bal FROM accounts WHERE id = 1;
-- @bal = 1000
-- ... 一些业务逻辑 ...
UPDATE accounts SET balance = @bal - 100 WHERE id = 1;
COMMIT;

-- 会话2 (并发执行)
START TRANSACTION;
SELECT balance INTO @bal FROM accounts WHERE id = 1;
-- @bal = 1000 (同时读取)
-- ... 业务逻辑 ...
UPDATE accounts SET balance = @bal - 200 WHERE id = 1;
COMMIT;

-- 结果: balance = 800 (而不是预期的700)
-- 会话1的更新被"丢失"了

-- 解决方案1: 使用锁定读
START TRANSACTION;
SELECT balance INTO @bal FROM accounts WHERE id = 1 FOR UPDATE;
-- 获取排他锁，阻止其他事务读取
UPDATE accounts SET balance = @bal - 100 WHERE id = 1;
COMMIT;

-- 解决方案2: 使用CAS (Compare-And-Swap)
UPDATE accounts
SET balance = balance - 100
WHERE id = 1 AND balance = 1000;  -- 预期当前值
```

---

## 7. 可视化 (Visualizations)

### 7.1 InnoDB 架构层次图

以下图表展示了InnoDB存储引擎的整体架构层次：

```mermaid
graph TB
    subgraph "SQL Layer"
        SQL[SQL Parser & Optimizer]
        HANDLER[Handler Interface]
    end

    subgraph "InnoDB Engine"
        DICT[Data Dictionary]
        SQL --> HANDLER --> DICT

        subgraph "In-Memory Structures"
            BP[Buffer Pool<br/>Page Cache]
            CB[Change Buffer<br/>Secondary Index]
            AHI[Adaptive Hash Index<br/>Hot Pages]
            LR[Log Buffer<br/>Redo Log Buffer]
        end

        subgraph "Transaction & Locking"
            TS[Transaction System<br/>Undo Logs]
            LS[Lock System<br/>Row-Level Locks]
        end

        DICT --> BP
        DICT --> CB
        BP --> AHI
    end

    subgraph "On-Disk Structures"
        TSYS[System Tablespace<br/>ibdata1]
        FIB[File-Per-Table<br/>.ibd files]
        UNDO[Undo Tablespaces<br/>undo_001, undo_002]
        REDO[Redo Logs<br/>ib_logfile0/1]
        TEMP[Temporary Tablespace<br/>ibtmp1]
        DWB[Doublewrite Buffer]
    end

    BP -.->|Flush| TSYS
    BP -.->|Flush| FIB
    TS -.->|Write| UNDO
    LR -.->|Flush| REDO
    BP -.->|Doublewrite| DWB

    style BP fill:#e1f5ff
    style TS fill:#fff4e1
    style LS fill:#ffe1e1
    style REDO fill:#e8ffe1
    style UNDO fill:#ffe1f5
```

### 7.2 MVCC 版本链与Read View示意图

以下图表展示了MVCC如何通过版本链实现非锁定读：

```mermaid
graph LR
    subgraph "当前表数据 (Latest)"
        V0[Row: id=1<br/>name='Alice_v3'<br/>trx_id=150<br/>DB_ROLL_PTR]
    end

    subgraph "Undo Log (History)"
        V1[Version 2<br/>name='Alice_v2'<br/>trx_id=120]
        V2[Version 1<br/>name='Alice_v1'<br/>trx_id=100]
    end

    V0 -->|roll_ptr| V1
    V1 -->|roll_ptr| V2

    subgraph "Read Views"
        RV1[Read View A<br/>creator=80<br/>up_limit=90<br/>low_limit=151<br/>m_ids={150}<br/><br/>可见: V2]
        RV2[Read View B<br/>creator=160<br/>up_limit=151<br/>low_limit=200<br/>m_ids={}<br/><br/>可见: V0]
        RV3[Read View C<br/>creator=130<br/>up_limit=100<br/>low_limit=151<br/>m_ids={120,150}<br/><br/>可见: V2]
    end

    V0 -.->|不可见| RV1
    V1 -.->|不可见| RV1
    V2 -.->|可见| RV1

    V0 -.->|可见| RV2

    V0 -.->|不可见| RV3
    V1 -.->|不可见| RV3
    V2 -.->|可见| RV3

    style V0 fill:#e1f5ff
    style V1 fill:#f0f0f0
    style V2 fill:#f5f5f5
    style RV1 fill:#fff4e1
    style RV2 fill:#e8ffe1
    style RV3 fill:#ffe1e1
```

### 7.3 锁类型与相容性矩阵

以下图表展示了InnoDB锁类型及其相容关系：

```mermaid
flowchart TB
    subgraph "锁粒度层次"
        direction TB
        TL[表级锁 TABLE LOCK]
        PL[页级锁 PAGE LOCK]
        RL[行级锁 ROW LOCK]
        GL[间隙锁 GAP LOCK]
        NL[Next-Key Lock<br/>行锁+间隙锁]
    end

    subgraph "锁模式"
        direction TB
        IS[IS<br/>意向共享]
        IX[IX<br/>意向排他]
        S[S<br/>共享锁]
        X[X<br/>排他锁]
        AI[AUTO_INC<br/>自增锁]
    end

    subgraph "相容性矩阵"
        direction TB
        M[| IS | IX | S | X |<br>| IS | ✓ | ✓ | ✓ | ✗ |<br>| IX | ✓ | ✓ | ✗ | ✗ |<br>| S | ✓ | ✗ | ✓ | ✗ |<br>| X | ✗ | ✗ | ✗ | ✗ |]
    end

    TL --> IS
    TL --> IX
    TL --> S
    TL --> X
    TL --> AI
    RL --> S
    RL --> X
    GL --> IS
    GL --> IX
    GL --> S
    GL --> X
    NL --> X

    style X fill:#ffcdd2
    style S fill:#c8e6c9
    style IS fill:#fff9c4
    style IX fill:#ffe0b2
```

### 7.4 崩溃恢复流程图

以下图表展示了InnoDB崩溃恢复的完整流程：

```mermaid
flowchart TD
    A[系统启动<br/>Crash Recovery] --> B[读取表空间<br/>检查文件完整性]
    B --> C[定位Redo日志文件<br/>ib_logfile0/1]
    C --> D[找到最后检查点<br/>Checkpoint LSN]

    subgraph "Redo Phase"
        E[从Checkpoint LSN开始扫描]
        F{LSN < 页LSN?}
        G[应用Redo记录]
        H[跳过已应用记录]
        I[所有Redo处理完成]

        E --> F
        F -->|是| H
        F -->|否| G
        G --> E
        H --> E
        E --> I
    end

    D --> E

    subgraph "Undo Phase"
        J[识别活跃事务<br/>从Transaction System]
        K[构建Undo日志链]
        L{所有活跃事务<br/>已回滚?}
        M[应用Undo记录<br/>恢复修改前值]
        N[写入CLR<br/>补偿日志记录]
        O[Undo完成]

        J --> K
        K --> L
        L -->|否| M
        M --> N
        N --> L
        L -->|是| O
    end

    I --> J

    subgraph "完成阶段"
        O --> P[刷新所有脏页到磁盘]
        P --> Q[写新的Checkpoint]
        Q --> R[接受新连接]
    end

    style A fill:#e3f2fd
    style I fill:#e8f5e9
    style O fill:#fff3e0
    style R fill:#f3e5f5
```

### 7.5 B+树索引结构示意图

以下图表展示了InnoDB B+树索引的结构：

```mermaid
graph TB
    subgraph "聚簇索引 Clustered Index"
        Root[根节点<br/>Page: 3<br/>Keys: [50, 100]]

        I1[内部节点<br/>Page: 10<br/>Keys: [10, 20, 30, 40]]
        I2[内部节点<br/>Page: 11<br/>Keys: [60, 70, 80, 90]]
        I3[内部节点<br/>Page: 12<br/>Keys: [110, 120, 130, 140]]

        L1[叶子节点<br/>Page: 100<br/>Records: [1..10]<br/>↔]
        L2[叶子节点<br/>Page: 101<br/>Records: [11..20]<br/>↔]
        L3[叶子节点<br/>Page: 102<br/>Records: [21..30]<br/>↔]
        L4[叶子节点<br/>Page: 103<br/>Records: [31..50]<br/>↔]
        L5[叶子节点<br/>Page: 104<br/>Records: [51..60]<br/>↔]
        L6[叶子节点<br/>Page: 105<br/>Records: [61..100]<br/>↔]
        L7[叶子节点<br/>Page: 106<br/>Records: [101..110]<br/>↔]
        L8[叶子节点<br/>Page: 107<br/>Records: [111..∞]<br/>↔]
    end

    Root -->|key < 50| I1
    Root -->|50 ≤ key < 100| I2
    Root -->|key ≥ 100| I3

    I1 --> L1
    I1 --> L2
    I1 --> L3
    I1 --> L4

    I2 --> L5
    I2 --> L6

    I3 --> L7
    I3 --> L8

    L1 <--> L2
    L2 <--> L3
    L3 <--> L4
    L4 <--> L5
    L5 <--> L6
    L6 <--> L7
    L7 <--> L8

    style Root fill:#e3f2fd
    style I1 fill:#fff3e0
    style I2 fill:#fff3e0
    style I3 fill:#fff3e0
    style L1 fill:#e8f5e9
    style L2 fill:#e8f5e9
    style L3 fill:#e8f5e9
    style L4 fill:#e8f5e9
    style L5 fill:#e8f5e9
    style L6 fill:#e8f5e9
    style L7 fill:#e8f5e9
    style L8 fill:#e8f5e9
```

---

## 8. 引用参考 (References)

[^1]: H. Berenson, P. Bernstein, J. Gray, J. Melton, E. O'Neil, and P. O'Neil. "A Critique of ANSI SQL Isolation Levels." In Proceedings of the 1995 ACM SIGMOD International Conference on Management of Data, pp. 1-10. 1995. <https://doi.org/10.1145/568271.223785>















---

## 附录 A: 关键系统变量参考

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `innodb_buffer_pool_size` | 128MB | 缓冲池大小 |
| `innodb_buffer_pool_instances` | 1 | 缓冲池实例数 |
| `innodb_log_file_size` | 48MB | Redo日志文件大小 |
| `innodb_log_files_in_group` | 2 | Redo日志文件数量 |
| `innodb_flush_log_at_trx_commit` | 1 | Redo刷盘策略 |
| `innodb_flush_method` | fsync | 数据刷盘方法 |
| `innodb_file_per_table` | ON | 独立表空间 |
| `innodb_lock_wait_timeout` | 50 | 锁等待超时(秒) |
| `innodb_deadlock_detect` | ON | 死锁检测开关 |
| `innodb_read_io_threads` | 4 | 读I/O线程数 |
| `innodb_write_io_threads` | 4 | 写I/O线程数 |
| `innodb_purge_threads` | 4 | Purge线程数 |
| `innodb_change_buffering` | all | Change Buffer类型 |
| `transaction_isolation` | REPEATABLE READ | 默认隔离级别 |

---

## 附录 B: 页类型速查

| 页类型值 | 名称 | 用途 |
|----------|------|------|
| 0x0000 | FIL_PAGE_TYPE_ALLOCATED | 新分配页 |
| 0x0002 | FIL_PAGE_UNDO_LOG | Undo日志页 |
| 0x0003 | FIL_PAGE_INODE | 段信息页 |
| 0x0004 | FIL_PAGE_IBUF_FREE_LIST | Change Buffer空闲列表 |
| 0x0005 | FIL_PAGE_IBUF_BITMAP | Change Buffer位图 |
| 0x0006 | FIL_PAGE_TYPE_SYS | 系统页 |
| 0x0007 | FIL_PAGE_TYPE_TRX_SYS | 事务系统页 |
| 0x0008 | FIL_PAGE_TYPE_FSP_HDR | 表空间头部 |
| 0x0009 | FIL_PAGE_TYPE_XDES | 区描述页 |
| 0x000A | FIL_PAGE_TYPE_BLOB | BLOB页 |
| 0x45BF | FIL_PAGE_INDEX | B+树索引页 |

---

*文档结束*

> **形式化元素统计**: 定义 21个 | 引理 2个 | 命题 8个 | 定理 3个 | 可视化 5个 | 引用 15个
>
> **交叉引用**: [MySQL官方文档](https://dev.mysql.com/doc/) | [InnoDB Internals](https://dev.mysql.com/doc/internals/en/innodb.html)
