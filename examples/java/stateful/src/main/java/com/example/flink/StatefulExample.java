package com.example.flink;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.RichFlatMapFunction;
import org.apache.flink.api.common.state.*;
import org.apache.flink.api.common.time.Time;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.util.Collector;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Flink 状态管理示例程序
 * 
 * 演示三种主要状态类型：
 * 1. ValueState - 单值状态（如计数器）
 * 2. ListState - 列表状态（如最近N个元素）
 * 3. MapState - 映射状态（如键值缓存）
 * 
 * 场景：电商订单处理 - 检测用户异常购买行为
 * - 统计用户下单次数（ValueState）
 * - 记录用户最近订单（ListState）
 * - 按商品统计购买次数（MapState）
 * 
 * 运行方式：
 * mvn compile exec:java -Dexec.mainClass="com.example.flink.StatefulExample" -Plocal
 * 
 * @author AnalysisDataFlow Project
 * @version 1.0.0
 */
public class StatefulExample {

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(2);

        System.out.println("=================================");
        System.out.println("Flink 状态管理示例");
        System.out.println("场景: 电商订单异常检测");
        System.out.println("=================================");

        // 模拟订单流
        DataStream<Order> orders = env.fromData(
            new Order("user_1", "iphone", 5999.0, System.currentTimeMillis()),
            new Order("user_2", "macbook", 12999.0, System.currentTimeMillis() + 1000),
            new Order("user_1", "airpods", 1299.0, System.currentTimeMillis() + 2000),
            new Order("user_1", "ipad", 4999.0, System.currentTimeMillis() + 3000),
            new Order("user_3", "iphone", 5999.0, System.currentTimeMillis() + 4000),
            new Order("user_1", "watch", 2999.0, System.currentTimeMillis() + 5000),
            new Order("user_2", "iphone", 5999.0, System.currentTimeMillis() + 6000),
            new Order("user_1", "macbook", 12999.0, System.currentTimeMillis() + 7000),
            new Order("user_3", "macbook", 12999.0, System.currentTimeMillis() + 8000),
            new Order("user_1", "iphone", 5999.0, System.currentTimeMillis() + 9000)
        );

        // 分配水印
        DataStream<Order> withTimestamps = orders.assignTimestampsAndWatermarks(
            WatermarkStrategy.<Order>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                .withTimestampAssigner((order, timestamp) -> order.timestamp)
        );

        // 应用有状态处理
        DataStream<Alert> alerts = withTimestamps
            .keyBy(order -> order.userId)
            .flatMap(new FraudDetectionFunction());

        // 输出告警
        alerts.print();

        env.execute("Flink Stateful Example - Fraud Detection");
    }

    /**
     * 欺诈检测函数 - 使用多种状态类型
     */
    public static class FraudDetectionFunction extends RichFlatMapFunction<Order, Alert> {

        // ValueState: 记录用户下单次数
        private ValueState<Integer> orderCountState;
        
        // ValueState: 记录用户累计消费金额
        private ValueState<Double> totalSpentState;
        
        // ListState: 记录用户最近3个订单
        private ListState<Order> recentOrdersState;
        
        // MapState: 记录用户每种商品的购买次数
        private MapState<String, Integer> productPurchaseCountState;

        @Override
        public void open(Configuration parameters) {
            StateTtlConfig ttlConfig = StateTtlConfig
                .newBuilder(Time.hours(24))
                .setUpdateType(StateTtlConfig.UpdateType.OnCreateAndWrite)
                .setStateVisibility(StateTtlConfig.StateVisibility.NeverReturnExpired)
                .build();

            // 初始化ValueState
            ValueStateDescriptor<Integer> countDescriptor = 
                new ValueStateDescriptor<>("orderCount", Integer.class);
            countDescriptor.enableTimeToLive(ttlConfig);
            orderCountState = getRuntimeContext().getState(countDescriptor);

            ValueStateDescriptor<Double> spentDescriptor = 
                new ValueStateDescriptor<>("totalSpent", Double.class);
            spentDescriptor.enableTimeToLive(ttlConfig);
            totalSpentState = getRuntimeContext().getState(spentDescriptor);

            // 初始化ListState
            ListStateDescriptor<Order> recentDescriptor = 
                new ListStateDescriptor<>("recentOrders", Order.class);
            recentDescriptor.enableTimeToLive(ttlConfig);
            recentOrdersState = getRuntimeContext().getListState(recentDescriptor);

            // 初始化MapState
            MapStateDescriptor<String, Integer> productDescriptor = 
                new MapStateDescriptor<>("productCount", String.class, Integer.class);
            productDescriptor.enableTimeToLive(ttlConfig);
            productPurchaseCountState = getRuntimeContext().getMapState(productDescriptor);
        }

        @Override
        public void flatMap(Order order, Collector<Alert> out) throws Exception {
            // 更新ValueState - 订单计数
            Integer currentCount = orderCountState.value();
            if (currentCount == null) {
                currentCount = 0;
            }
            currentCount++;
            orderCountState.update(currentCount);

            // 更新ValueState - 累计消费
            Double currentSpent = totalSpentState.value();
            if (currentSpent == null) {
                currentSpent = 0.0;
            }
            currentSpent += order.amount;
            totalSpentState.update(currentSpent);

            // 更新ListState - 最近订单（只保留3个）
            List<Order> recentOrders = new ArrayList<>();
            for (Order o : recentOrdersState.get()) {
                recentOrders.add(o);
            }
            recentOrders.add(order);
            if (recentOrders.size() > 3) {
                recentOrders.remove(0);
            }
            recentOrdersState.update(recentOrders);

            // 更新MapState - 商品购买计数
            Integer productCount = productPurchaseCountState.get(order.product);
            if (productCount == null) {
                productCount = 0;
            }
            productCount++;
            productPurchaseCountState.put(order.product, productCount);

            // 检测异常行为
            StringBuilder alertMsg = new StringBuilder();
            boolean isSuspicious = false;

            // 规则1: 10分钟内下单超过5次
            if (currentCount >= 5) {
                isSuspicious = true;
                alertMsg.append(String.format("短时间内高频下单(%d次)", currentCount));
            }

            // 规则2: 累计消费超过30000
            if (currentSpent > 30000) {
                if (isSuspicious) alertMsg.append(", ");
                isSuspicious = true;
                alertMsg.append(String.format("累计消费金额异常(%.0f元)", currentSpent));
            }

            // 规则3: 同一商品重复购买超过2次
            for (Map.Entry<String, Integer> entry : productPurchaseCountState.entries()) {
                if (entry.getValue() >= 3) {
                    if (isSuspicious) alertMsg.append(", ");
                    isSuspicious = true;
                    alertMsg.append(String.format("重复购买%s(%d次)", entry.getKey(), entry.getValue()));
                    break;
                }
            }

            // 输出告警
            if (isSuspicious) {
                out.collect(new Alert(
                    order.userId,
                    alertMsg.toString(),
                    currentCount,
                    currentSpent,
                    new ArrayList<>(recentOrders)
                ));
            }

            // 输出当前状态信息
            System.out.printf("[状态更新] 用户=%s, 订单数=%d, 累计消费=%.0f, 最近订单=%d%n",
                order.userId, currentCount, currentSpent, recentOrders.size());
        }
    }

    /**
     * 订单数据类
     */
    public static class Order {
        public String userId;
        public String product;
        public double amount;
        public long timestamp;

        public Order() {}

        public Order(String userId, String product, double amount, long timestamp) {
            this.userId = userId;
            this.product = product;
            this.amount = amount;
            this.timestamp = timestamp;
        }

        @Override
        public String toString() {
            return String.format("Order{%s buys %s for %.0f}", userId, product, amount);
        }
    }

    /**
     * 告警数据类
     */
    public static class Alert {
        public String userId;
        public String reason;
        public int orderCount;
        public double totalSpent;
        public List<Order> recentOrders;

        public Alert(String userId, String reason, int orderCount, double totalSpent, List<Order> recentOrders) {
            this.userId = userId;
            this.reason = reason;
            this.orderCount = orderCount;
            this.totalSpent = totalSpent;
            this.recentOrders = recentOrders;
        }

        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            sb.append("\n╔════════════════════════════════════════════════╗\n");
            sb.append("║           ⚠️  异常购买行为告警                   ║\n");
            sb.append("╠════════════════════════════════════════════════╣\n");
            sb.append(String.format("║ 用户ID: %-38s ║%n", userId));
            sb.append(String.format("║ 告警原因: %-36s ║%n", reason));
            sb.append(String.format("║ 订单总数: %-36d ║%n", orderCount));
            sb.append(String.format("║ 累计消费: %-36.0f ║%n", totalSpent));
            sb.append("║ 最近订单:                                      ║\n");
            for (Order o : recentOrders) {
                sb.append(String.format("║   - %-42s ║%n", o.toString()));
            }
            sb.append("╚════════════════════════════════════════════════╝");
            return sb.toString();
        }
    }
}
