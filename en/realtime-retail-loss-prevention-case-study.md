# Real-Time Smart Retail Loss Prevention Case Study

> Stage: Knowledge/ Flink/ | Prerequisites: [Operator Panorama Classification](../Knowledge/01-concept-atlas/operator-deep-dive/01.06-single-input-operators.md) | [CEP Pattern](./pattern-cep-complex-event.md) | Formalization Level: L4

## 1. Definitions

### Def-RLP-01-01: Smart Retail Loss Prevention System (智慧零售防损系统)

A Smart Retail Loss Prevention System is an integrated system that leverages POS transaction data, RFID inventory, video surveillance, and stream computing platforms to achieve abnormal transaction detection, inventory discrepancy early warning, and theft behavior identification.

$$\mathcal{R} = (P, I, V, F)$$

Where $P$ is the POS transaction stream, $I$ is the inventory change stream, $V$ is the video analysis stream, and $F$ is the stream computing processing topology.

### Def-RLP-01-02: Abnormal Transaction Index (异常交易指数)

$$ATI = \omega_1 \cdot \frac{Amount}{AvgAmount} + \omega_2 \cdot \frac{VoidCount}{TotalCount} + \omega_3 \cdot \frac{DiscountRate}{AvgDiscount}$$

Where $\omega_1 + \omega_2 + \omega_3 = 1$. $ATI > 3$ triggers a deep audit.

### Def-RLP-01-03: Inventory Shrinkage Rate (库存差异率)

$$Shrinkage = \frac{I_{book} - I_{physical}}{I_{book}} \cdot 100\%$$

Industry warning threshold: $Shrinkage > 1.5\%$.

## 2. Examples

### 2.1 Abnormal Transaction Detection

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<Transaction> transactions = env
    .addSource(new KafkaSource<>("retail.pos.transactions"))
    .map(new TransactionParser());

DataStream<TransactionAlert> alerts = transactions
    .keyBy(t -> t.getCashierId())
    .window(SlidingEventTimeWindows.of(Time.hours(1), Time.minutes(5)))
    .aggregate(new TransactionAggregate() {
        @Override
        public void aggregate(Transaction tx, Accumulator acc) {
            acc.addAmount(tx.getAmount());
            acc.addVoid(tx.isVoid());
            double ati = calculateATI(acc);
            if (ati > THRESHOLD) {
                out.collect(new TransactionAlert(tx.getCashierId(), ati));
            }
        }
    });

alerts.addSink(new AuditSink());
```

### 2.2 Real-Time Inventory Shrinkage Analysis

```java
DataStream<Inventory> inventory = env
    .addSource(new KafkaSource<>("retail.inventory"))
    .map(new InventoryParser());

DataStream<ShrinkageAlert> shrinkage = inventory
    .keyBy(i -> i.getSku())
    .window(TumblingEventTimeWindows.of(Time.days(1)))
    .aggregate(new ShrinkageAggregate());

shrinkage.addSink(new AlertSink());
```

## 3. References
