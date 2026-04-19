# 时间感知缓存替换

> **所属阶段**: Knowledge/ | **前置依赖**: [bounded-staleness-cache.md](../Struct/bounded-staleness-cache.md), [state-prefetching.md](../Struct/state-prefetching.md) | **形式化等级**: L4

---

## 1. 概念定义 (Definitions)

传统缓存替换策略（如 LRU、LFU）主要基于访问频率和最近性来决定哪些数据保留在缓存中。然而，在流处理和时序数据场景中，数据的时间属性（如有效期限、过期时间、时序查询模式）对缓存决策同样重要。时间感知缓存替换策略（Timestamp-Aware Caching）将时间维度显式纳入替换决策中，优先保留那些在查询时间窗口内仍然有效且可能被访问的数据。

**Def-K-06-401 时间感知缓存 (Timestamp-Aware Cache)**

时间感知缓存 $\mathcal{C}_T$ 中的每个条目 $e$ 包含一个元组 $(k, v, t_{insert}, t_{expire}, f_{access})$：

- $k$: 键
- $v$: 值
- $t_{insert}$: 插入时间戳
- $t_{expire}$: 过期时间戳
- $f_{access}$: 历史访问频率

替换决策函数 $R(e)$ 综合考虑了时间有效性和访问热度：

$$
R(e) = w_1 \cdot f_{access}(e) + w_2 \cdot \frac{t_{expire} - t_{current}}{T_{max}} + w_3 \cdot recency(e)
$$

其中 $w_1, w_2, w_3$ 为权重系数。当需要腾出空间时，优先替换 $R(e)$ 最低的条目。

**Def-K-06-402 时序查询局部性 (Temporal Query Locality)**

时序查询局部性是指查询倾向于访问特定时间范围内的数据。设查询时间窗口为 $[t_q - \Delta, t_q]$，则键 $k$ 在该窗口内被访问的概率为：

$$
P(access(k) | t_q) \propto \mathbb{1}(t_{expire}(k) \geq t_q - \Delta) \cdot f_{access}(k)
$$

*说明*: 即将过期的数据如果在查询窗口内不再有效，即使访问频率高也应被优先替换。$\square$

---

## 2. 属性推导 (Properties)

**Lemma-K-06-154 LRU 的时序次优性**

在存在明显时序查询局部性的工作负载下，纯 LRU 策略的命中率可能显著低于最优时间感知策略。设 LRU 命中率为 $h_{LRU}$，最优策略命中率为 $h_{OPT}$，则：

$$
\frac{h_{LRU}}{h_{OPT}} \leq \frac{1}{1 + \rho \cdot \Delta t_{skew}}
$$

其中 $\rho$ 为时序倾斜度，$\Delta t_{skew}$ 为访问时间分布的偏度。

*说明*: 时序倾斜越严重，LRU 相对于时间感知策略的劣势越大。$\square$

**Prop-K-06-142 过期感知替换的收益**

设缓存容量为 $C$，数据中过期键的比例为 $p_{exp}$。若替换策略能够识别并优先淘汰过期键，则有效缓存利用率提升：

$$
\eta_{gain} = \frac{C}{C - p_{exp} \cdot C} - 1 = \frac{p_{exp}}{1 - p_{exp}}
$$

*说明*: 在时序数据密集的场景中，$p_{exp}$ 可能达到 30-50%，此时过期感知替换的收益非常显著。$\square$

---

## 3. 关系建立 (Relations)

### 3.1 缓存替换策略对比

| 策略 | 考虑因素 | 时序适应性 | 适用场景 |
|------|---------|-----------|---------|
| **LRU** | 最近访问 | 差 | 通用工作负载 |
| **LFU** | 访问频率 | 差 | 稳定热点数据 |
| **TTL** | 固定过期时间 | 中 | 会话缓存 |
| **T-LRU** | 最近访问 + 过期时间 | 好 | 时序数据缓存 |
| **时间感知替换** | 访问频率 + 时间有效性 + 查询窗口 | 优 | 流处理状态缓存 |

### 3.2 时间感知缓存在流处理中的位置

```mermaid
graph TB
    Query["时序查询<br/>WHERE ts > NOW() -1h"] --> Eval[评估缓存条目时间有效性]
    Eval --> Rank[按 R(e) 排序]
    Rank --> Evict[淘汰低价值条目]
    Evict --> Load[加载新数据到缓存]
    Load --> Query
```

---

## 4. 论证过程 (Argumentation)

### 4.1 为什么需要时间感知缓存替换？

1. **数据时效性**: 流处理中的许多数据只在有限时间窗口内有效（如过去 1 小时的传感器读数）
2. **查询窗口约束**: 时序查询通常带有 WHERE ts > T - Δ 的约束，过期数据永远不会被查询到
3. **缓存污染**: 传统 LRU 可能保留大量高频率但已过期的数据，排挤真正有用的条目
4. **内存效率**: 主动淘汰过期数据可以释放空间给新的有效数据

### 4.2 时间感知替换策略的设计

一种实用的时间感知替换策略（T-LRU+）结合了三个信号：

1. **时序相关性分数**: 衡量键的过期时间与当前查询窗口的匹配度
2. **访问频率衰减**: 使用指数衰减而非原始计数，使近期访问权重更高
3. **空间局部性**: 对于范围查询，保留与热门键时间相邻的条目

### 4.3 反例：过度依赖时间导致的缓存抖动

某系统将时间权重设置得过高，导致缓存中的条目在过期前 1 秒就被全部清空。结果：

- 大量实际上仍有查询价值的数据被过早淘汰
- 缓存命中率从 85% 骤降至 30%
- 后端存储压力剧增

**教训**: 时间感知策略必须平衡时间有效性和访问热度，不能单方面追求新鲜度。

---

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

**Thm-K-06-161 时间感知替换的最优性条件**

设查询负载中每个查询 $q$ 关联一个时间窗口 $W_q = [t_q - \Delta, t_q]$。若键 $k$ 的访问概率满足：

$$
P(k \text{ 被访问} | q) = f(k) \cdot \mathbb{1}(t_{expire}(k) \in W_q)
$$

则按 $R(k) = f(k) \cdot \mathbb{1}(t_{expire}(k) \geq t_{current})$ 排序的替换策略在所有基于当前状态信息的策略中具有最高的期望命中率。

*证明梗概*:

对于任意查询 $q$，只有满足 $t_{expire}(k) \in W_q$ 的键才可能被访问。在所有满足时间条件的键中，访问概率最高的键应被优先保留。$R(k)$ 正是这种排序的量化表示。因此按 $R(k)$ 降序保留的缓存配置在任何容量限制下都能最大化期望命中键数。$\square$

---

## 6. 实例验证 (Examples)

### 6.1 时间感知缓存管理器

```python
import time
from collections import OrderedDict

class TimestampAwareCache:
    def __init__(self, capacity, time_weight=0.5, freq_weight=0.5):
        self.capacity = capacity
        self.time_weight = time_weight
        self.freq_weight = freq_weight
        self.cache = OrderedDict()

    def score(self, entry):
        now = time.time()
        time_value = max(0, entry['expire'] - now)
        freq_value = entry['freq']
        return self.time_weight * time_value + self.freq_weight * freq_value

    def put(self, key, value, expire_time):
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                self._evict()
            self.cache[key] = {'value': value, 'expire': expire_time, 'freq': 1, 'last_access': time.time()}

    def get(self, key):
        if key not in self.cache:
            return None
        entry = self.cache[key]
        if entry['expire'] < time.time():
            del self.cache[key]
            return None
        entry['freq'] += 1
        entry['last_access'] = time.time()
        self.cache.move_to_end(key)
        return entry['value']

    def _evict(self):
        # 找到评分最低的条目并淘汰
        min_key = min(self.cache.keys(), key=lambda k: self.score(self.cache[k]))
        del self.cache[min_key]
```

### 6.2 Flink 状态缓存中的时间感知替换

```java
// [伪代码片段 - 不可直接运行] 仅展示核心逻辑
// 概念性配置：为 RocksDB 块缓存启用时间感知替换
RocksDBStateBackendConfig config = new RocksDBStateBackendConfig();
config.setCacheReplacementPolicy(CacheReplacementPolicy.TIME_AWARE_LRU);
config.setTimeWindowMillis(3600000); // 1小时查询窗口
config.setTimeWeight(0.6f);
config.setFrequencyWeight(0.4f);
```

---

## 7. 可视化 (Visualizations)

### 7.1 时间感知替换 vs LRU 的命中率对比

```mermaid
xychart-beta
    title "时序倾斜工作负载下的缓存命中率"
    x-axis [10%, 30%, 50%, 70%, 90%]
    y-axis "命中率 (%)" 0 --> 100
    line "LRU" {45, 50, 55, 60, 65}
    line "T-LRU" {55, 65, 75, 82, 88}
    line "时间感知替换" {60, 72, 82, 90, 95}
```

*X 轴：时序查询占比*

---

## 8. 引用参考 (References)
