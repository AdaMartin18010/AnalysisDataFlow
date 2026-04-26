# YARN部署演进 特性跟踪

> 所属阶段: Flink/deployment/evolution | 前置依赖: [YARN部署][^1] | 形式化等级: L3

## 1. 概念定义 (Definitions)

### Def-F-Deploy-YARN-01: YARN Session

YARN会话：
$$
\text{YARNSession} = \text{SharedCluster} + \text{DynamicResource}
$$

## 2. 属性推导 (Properties)

### Prop-F-Deploy-YARN-01: Resource Elasticity

资源弹性：
$$
\text{Resources} = f(\text{Load})
$$

## 3. 关系建立 (Relations)

### YARN演进

| 版本 | 特性 | 状态 |
|------|------|------|
| 2.4 | 动态分配 | GA |
| 2.5 | GPU资源 | GA |
| 3.0 | YARN原生优化 | 设计中 |

## 4. 论证过程 (Argumentation)

### 4.1 部署命令

```bash
# 启动YARN会话 ./bin/yarn-session.sh -nm flink-session -q

# 提交作业 ./bin/flink run -t yarn-per-job ./examples/streaming/WordCount.jar
```

## 5. 形式证明 / 工程论证

### 5.1 资源配置

```yaml
yarn.application-attempts: 10
yarn.application-attempt-failures-validity-interval: 3600000
```

## 6. 实例验证 (Examples)

### 6.1 动态资源

```java
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
public class Example {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.getConfig().setAutoWatermarkInterval(200);

    }
}

```

## 7. 可视化 (Visualizations)

```mermaid
graph TB
    A[YARN RM] --> B[Flink JM]
    B --> C[TM Container]
    B --> D[TM Container]
```

### YARN部署演进思维导图

以下思维导图以"YARN部署演进"为中心，放射展示早期模式、YARN集成、优化改进、与K8s对比及迁移路径五大维度。

```mermaid
mindmap
  root((YARN部署演进))
    早期模式
      Session模式
      Per-Job模式
      资源静态分配
    YARN集成
      AM注册
      Container申请
      资源本地化
      日志聚合
    优化改进
      动态资源
      GPU支持
      本地性优化
      队列调度
    与K8s对比
      部署复杂度
      生态成熟度
      运维习惯
      云厂商支持
    迁移路径
      YARN→K8s评估
      混合部署
      渐进迁移
```

### YARN组件→Flink运行时→部署产物映射

以下关联树展示YARN底层组件如何映射到Flink运行时实体，并生成最终部署产物。

```mermaid
graph TB
    subgraph YARN组件
        RM[ResourceManager]
        NM[NodeManager]
        YAM[YARN ApplicationMaster]
    end
    subgraph Flink运行时
        JM[JobManager]
        TM[TaskManager]
        Slot[Task Slot]
    end
    subgraph 部署产物
        Cont[YARN Container]
        Log[日志文件]
        Jar[作业JAR包]
        CP[Checkpoint状态]
    end
    RM -->|调度| YAM
    NM -->|启动| Cont
    YAM -->|对应| JM
    JM -->|管理| TM
    TM -->|分配| Slot
    TM -->|运行| Cont
    JM -->|聚合| Log
    Slot -->|加载| Jar
    TM -->|持久化| CP
```

### YARN vs K8s 选型决策树

以下决策树帮助根据现有集群状态、需求类型及运行环境，在YARN与K8s之间做出部署选型判断。

```mermaid
flowchart TD
    Start([开始选型]) --> Q1{已有YARN集群？}
    Q1 -->|是| A1[继续使用YARN<br/>渐进评估K8s]
    Q1 -->|否| Q2{新建集群？}
    Q2 -->|是| A2[优先K8s<br/>云原生生态]
    Q2 -->|否| Q3{混合需求？}
    Q3 -->|是| A3[YARN批处理<br/>K8s流处理]
    Q3 -->|否| Q4{云环境？}
    Q4 -->|是| A4[直接K8s/托管服务]
    Q4 -->|否| A5[评估本地运维能力<br/>按需选择]
```

## 8. 引用参考 (References)

[^1]: Flink YARN Documentation

---

## 跟踪信息

| 属性 | 值 |
|------|-----|
| 版本 | 2.4-3.0 |
| 当前状态 | 演进中 |

---

*文档版本: v1.0 | 创建日期: 2026-04-19*
