/**
 * AnalysisDataFlow 学习平台 - 课程数据
 * 包含所有课程、实验、挑战和测验的完整数据结构
 */

const coursesData = {
    // 认证路径
    certifications: {
        csa: {
            id: 'csa',
            name: 'CSA',
            fullName: 'Certified Streaming Associate',
            title: '流计算认证助理',
            description: '掌握流计算基础概念和Flink入门开发',
            duration: '40小时',
            color: '#22c55e',
            skills: ['Flink DataStream API', 'Event Time 处理', 'Window 聚合', '状态管理', 'Checkpoint & Exactly-Once'],
            prerequisites: [],
            modules: [
                { id: 'csa-01', title: '流计算基础概念', duration: '5小时', lessons: 5 },
                { id: 'csa-02', title: 'Flink 快速入门', duration: '5小时', lessons: 6 },
                { id: 'csa-03', title: 'DataStream API 基础', duration: '5小时', lessons: 7 },
                { id: 'csa-04', title: '窗口与聚合', duration: '5小时', lessons: 5 },
                { id: 'csa-05', title: '状态管理基础', duration: '5小时', lessons: 4 },
                { id: 'csa-06', title: 'Checkpoint 与容错', duration: '5小时', lessons: 4 },
                { id: 'csa-07', title: 'Table API 与 SQL 入门', duration: '5小时', lessons: 5 },
                { id: 'csa-08', title: '部署与监控', duration: '5小时', lessons: 4 }
            ]
        },
        csp: {
            id: 'csp',
            name: 'CSP',
            fullName: 'Certified Streaming Professional',
            title: '流计算认证专业人员',
            description: '深入Flink核心机制，掌握生产部署和性能调优',
            duration: '80小时',
            color: '#f59e0b',
            skills: ['内存管理优化', '网络栈调优', 'Checkpoint 调优', '反压处理', '生产运维'],
            prerequisites: ['csa'],
            modules: [
                { id: 'csp-01', title: 'Flink 运行时架构深度解析', duration: '8小时', lessons: 6 },
                { id: 'csp-02', title: '内存管理与配置', duration: '8小时', lessons: 5 },
                { id: 'csp-03', title: '网络栈与序列化优化', duration: '8小时', lessons: 5 },
                { id: 'csp-04', title: '高级状态管理', duration: '8小时', lessons: 6 },
                { id: 'csp-05', title: 'Checkpoint 高级配置', duration: '8小时', lessons: 5 },
                { id: 'csp-06', title: 'CEP 复杂事件处理', duration: '8小时', lessons: 5 },
                { id: 'csp-07', title: '生产环境部署', duration: '8小时', lessons: 6 },
                { id: 'csp-08', title: '监控与告警', duration: '8小时', lessons: 5 },
                { id: 'csp-09', title: '性能调优实战', duration: '8小时', lessons: 5 },
                { id: 'csp-10', title: '故障诊断与恢复', duration: '8小时', lessons: 5 }
            ]
        },
        cse: {
            id: 'cse',
            name: 'CSE',
            fullName: 'Certified Streaming Expert',
            title: '流计算认证专家',
            description: '形式化理论研究、架构设计和原创贡献',
            duration: '120小时',
            color: '#ef4444',
            skills: ['形式化语义', '一致性模型', '分布式架构设计', '原创研究', '社区贡献'],
            prerequisites: ['csp'],
            modules: [
                { id: 'cse-01', title: '流计算形式化基础', duration: '20小时', lessons: 8 },
                { id: 'cse-02', title: '一致性模型与证明', duration: '20小时', lessons: 7 },
                { id: 'cse-03', title: '大规模架构设计', duration: '20小时', lessons: 6 },
                { id: 'cse-04', title: '前沿技术探索', duration: '20小时', lessons: 6 },
                { id: 'cse-05', title: '研究方法论', duration: '20小时', lessons: 5 },
                { id: 'cse-06', title: '综合项目', duration: '20小时', lessons: 1 }
            ]
        }
    },

    // 课程列表
    courses: [
        {
            id: 'course-01',
            title: '流计算基础入门',
            description: '从零开始学习流计算的核心概念，包括Event Time、Processing Time、窗口计算等基础理论。',
            level: 'beginner',
            duration: '8小时',
            lessons: 12,
            icon: 'fa-play-circle',
            color: 'linear-gradient(135deg, #22c55e, #16a34a)',
            chapters: [
                { id: 'c01-l01', title: '什么是流计算', duration: '15分钟', type: 'video' },
                { id: 'c01-l02', title: '批处理 vs 流处理', duration: '20分钟', type: 'video' },
                { id: 'c01-l03', title: '时间语义详解', duration: '25分钟', type: 'video' },
                { id: 'c01-l04', title: 'Event Time 实战', duration: '30分钟', type: 'lab' },
                { id: 'c01-l05', title: '窗口计算基础', duration: '20分钟', type: 'video' },
                { id: 'c01-l06', title: '窗口类型对比', duration: '25分钟', type: 'video' },
                { id: 'c01-l07', title: '滚动窗口实战', duration: '30分钟', type: 'lab' },
                { id: 'c01-l08', title: '滑动窗口实战', duration: '30分钟', type: 'lab' },
                { id: 'c01-l09', title: '一致性模型', duration: '25分钟', type: 'video' },
                { id: 'c01-l10', title: 'Exactly-Once 语义', duration: '30分钟', type: 'video' },
                { id: 'c01-l11', title: '状态管理初探', duration: '20分钟', type: 'video' },
                { id: 'c01-l12', title: '章节测验', duration: '30分钟', type: 'quiz' }
            ]
        },
        {
            id: 'course-02',
            title: 'Flink DataStream API',
            description: '深入学习Flink DataStream API，掌握Source、Transformation、Sink等核心操作。',
            level: 'beginner',
            duration: '10小时',
            lessons: 15,
            icon: 'fa-code',
            color: 'linear-gradient(135deg, #3b82f6, #2563eb)',
            chapters: [
                { id: 'c02-l01', title: 'Flink 架构概览', duration: '20分钟', type: 'video' },
                { id: 'c02-l02', title: '开发环境搭建', duration: '30分钟', type: 'lab' },
                { id: 'c02-l03', title: '第一个 Flink 程序', duration: '25分钟', type: 'lab' },
                { id: 'c02-l04', title: '数据源 Source', duration: '30分钟', type: 'video' },
                { id: 'c02-l05', title: 'Kafka 集成', duration: '35分钟', type: 'lab' },
                { id: 'c02-l06', title: 'Transformation 基础', duration: '25分钟', type: 'video' },
                { id: 'c02-l07', title: 'map 和 filter', duration: '30分钟', type: 'lab' },
                { id: 'c02-l08', title: 'flatMap 和 keyBy', duration: '35分钟', type: 'lab' },
                { id: 'c02-l09', title: '窗口操作', duration: '30分钟', type: 'video' },
                { id: 'c02-l10', title: '聚合函数', duration: '35分钟', type: 'lab' },
                { id: 'c02-l11', title: '数据输出 Sink', duration: '25分钟', type: 'video' },
                { id: 'c02-l12', title: 'JDBC 输出', duration: '30分钟', type: 'lab' },
                { id: 'c02-l13', title: '并行度配置', duration: '20分钟', type: 'video' },
                { id: 'c02-l14', title: '作业提交', duration: '25分钟', type: 'lab' },
                { id: 'c02-l15', title: '章节测验', duration: '30分钟', type: 'quiz' }
            ]
        },
        {
            id: 'course-03',
            title: '状态管理与 Checkpoint',
            description: '理解Flink状态管理原理，学习Checkpoint机制和容错配置。',
            level: 'intermediate',
            duration: '12小时',
            lessons: 14,
            icon: 'fa-database',
            color: 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
            chapters: [
                { id: 'c03-l01', title: '状态管理概述', duration: '20分钟', type: 'video' },
                { id: 'c03-l02', title: 'Keyed State vs Operator State', duration: '25分钟', type: 'video' },
                { id: 'c03-l03', title: 'ValueState 使用', duration: '30分钟', type: 'lab' },
                { id: 'c03-l04', title: 'ListState 和 MapState', duration: '35分钟', type: 'lab' },
                { id: 'c03-l05', title: '状态 TTL 配置', duration: '25分钟', type: 'video' },
                { id: 'c03-l06', title: '状态后端对比', duration: '30分钟', type: 'video' },
                { id: 'c03-l07', title: 'MemoryStateBackend', duration: '20分钟', type: 'lab' },
                { id: 'c03-l08', title: 'FsStateBackend', duration: '25分钟', type: 'lab' },
                { id: 'c03-l09', title: 'RocksDBStateBackend', duration: '35分钟', type: 'lab' },
                { id: 'c03-l10', title: 'Checkpoint 原理', duration: '30分钟', type: 'video' },
                { id: 'c03-l11', title: 'Checkpoint 配置', duration: '30分钟', type: 'lab' },
                { id: 'c03-l12', title: '故障恢复测试', duration: '35分钟', type: 'lab' },
                { id: 'c03-l13', title: 'Savepoint 使用', duration: '25分钟', type: 'lab' },
                { id: 'c03-l14', title: '章节测验', duration: '30分钟', type: 'quiz' }
            ]
        },
        {
            id: 'course-04',
            title: '时间语义与 Watermark',
            description: '深入理解Flink时间处理机制，掌握Watermark和乱序数据处理。',
            level: 'intermediate',
            duration: '10小时',
            lessons: 12,
            icon: 'fa-clock',
            color: 'linear-gradient(135deg, #f59e0b, #d97706)',
            chapters: [
                { id: 'c04-l01', title: '时间语义回顾', duration: '15分钟', type: 'video' },
                { id: 'c04-l02', title: 'Watermark 机制', duration: '30分钟', type: 'video' },
                { id: 'c04-l03', title: '生成 Watermark', duration: '30分钟', type: 'lab' },
                { id: 'c04-l04', title: '乱序数据处理', duration: '35分钟', type: 'lab' },
                { id: 'c04-l05', title: 'Allowed Lateness', duration: '25分钟', type: 'video' },
                { id: 'c04-l06', title: '迟到数据处理', duration: '30分钟', type: 'lab' },
                { id: 'c04-l07', title: '侧输出流', duration: '25分钟', type: 'video' },
                { id: 'c04-l08', title: '侧输出流实战', duration: '30分钟', type: 'lab' },
                { id: 'c04-l09', title: '窗口触发器', duration: '30分钟', type: 'video' },
                { id: 'c04-l10', title: '自定义 Trigger', duration: '35分钟', type: 'lab' },
                { id: 'c04-l11', title: '多流时间对齐', duration: '30分钟', type: 'lab' },
                { id: 'c04-l12', title: '章节测验', duration: '30分钟', type: 'quiz' }
            ]
        },
        {
            id: 'course-05',
            title: 'Table API 与 SQL',
            description: '使用SQL进行流处理，学习Flink Table API和Streaming SQL。',
            level: 'intermediate',
            duration: '10小时',
            lessons: 13,
            icon: 'fa-table',
            color: 'linear-gradient(135deg, #06b6d4, #0891b2)',
            chapters: [
                { id: 'c05-l01', title: 'Table API 介绍', duration: '20分钟', type: 'video' },
                { id: 'c05-l02', title: 'TableEnvironment', duration: '25分钟', type: 'lab' },
                { id: 'c05-l03', title: 'DataStream 转 Table', duration: '30分钟', type: 'lab' },
                { id: 'c05-l04', title: 'DDL 定义表', duration: '30分钟', type: 'video' },
                { id: 'c05-l05', title: 'Kafka 连接器', duration: '35分钟', type: 'lab' },
                { id: 'c05-l06', title: '基础 SQL 查询', duration: '30分钟', type: 'lab' },
                { id: 'c05-l07', title: '窗口函数', duration: '35分钟', type: 'video' },
                { id: 'c05-l08', title: 'TUMBLE 窗口', duration: '30分钟', type: 'lab' },
                { id: 'c05-l09', title: 'HOP 和 SESSION', duration: '35分钟', type: 'lab' },
                { id: 'c05-l10', title: 'CDC 数据同步', duration: '40分钟', type: 'lab' },
                { id: 'c05-l11', title: 'Lookup Join', duration: '30分钟', type: 'lab' },
                { id: 'c05-l12', title: '流批一体', duration: '25分钟', type: 'video' },
                { id: 'c05-l13', title: '章节测验', duration: '30分钟', type: 'quiz' }
            ]
        },
        {
            id: 'course-06',
            title: '高级特性与优化',
            description: '探索Flink高级特性，学习性能调优和生产实践。',
            level: 'advanced',
            duration: '15小时',
            lessons: 16,
            icon: 'fa-rocket',
            color: 'linear-gradient(135deg, #ef4444, #dc2626)',
            chapters: [
                { id: 'c06-l01', title: 'CEP 复杂事件处理', duration: '35分钟', type: 'video' },
                { id: 'c06-l02', title: '模式定义', duration: '40分钟', type: 'lab' },
                { id: 'c06-l03', title: '近实时处理', duration: '30分钟', type: 'video' },
                { id: 'c06-l04', title: 'Async I/O', duration: '40分钟', type: 'lab' },
                { id: 'c06-l05', title: '广播状态', duration: '35分钟', type: 'video' },
                { id: 'c06-l06', title: '广播状态实战', duration: '40分钟', type: 'lab' },
                { id: 'c06-l07', title: 'ProcessFunction', duration: '35分钟', type: 'video' },
                { id: 'c06-l08', title: 'Timer 使用', duration: '40分钟', type: 'lab' },
                { id: 'c06-l09', title: '内存管理', duration: '35分钟', type: 'video' },
                { id: 'c06-l10', title: '网络缓冲调优', duration: '35分钟', type: 'lab' },
                { id: 'c06-l11', title: '对象重用', duration: '30分钟', type: 'lab' },
                { id: 'c06-l12', title: '序列化优化', duration: '35分钟', type: 'video' },
                { id: 'c06-l13', title: 'Avro 和 Protobuf', duration: '40分钟', type: 'lab' },
                { id: 'c06-l14', title: '反压处理', duration: '35分钟', type: 'video' },
                { id: 'c06-l15', title: '反压诊断', duration: '35分钟', type: 'lab' },
                { id: 'c06-l16', title: '章节测验', duration: '30分钟', type: 'quiz' }
            ]
        }
    ],

    // 动手实验
    labs: [
        {
            id: 'lab-01',
            title: 'Lab 1: 第一个 Flink 程序',
            description: '搭建开发环境，编写并运行你的第一个Flink程序——WordCount。',
            difficulty: 'beginner',
            duration: '45分钟',
            icon: 'fa-code',
            tasks: [
                '配置 Maven 项目',
                '编写 WordCount 程序',
                '本地运行测试',
                '查看运行结果'
            ]
        },
        {
            id: 'lab-02',
            title: 'Lab 2: Event Time 处理',
            description: '学习如何使用Event Time处理乱序数据，理解时间语义的重要性。',
            difficulty: 'beginner',
            duration: '60分钟',
            icon: 'fa-clock',
            tasks: [
                '生成带时间戳的数据',
                '设置 Watermark 策略',
                '观察乱序数据处理',
                '处理迟到数据'
            ]
        },
        {
            id: 'lab-03',
            title: 'Lab 3: Window 聚合',
            description: '掌握各种窗口类型的使用，实现实时统计功能。',
            difficulty: 'beginner',
            duration: '60分钟',
            icon: 'fa-window-maximize',
            tasks: [
                '滚动窗口统计',
                '滑动窗口计算',
                '会话窗口应用',
                '增量聚合优化'
            ]
        },
        {
            id: 'lab-04',
            title: 'Lab 4: 状态管理',
            description: '使用Keyed State实现有状态计算，理解状态后端差异。',
            difficulty: 'intermediate',
            duration: '75分钟',
            icon: 'fa-database',
            tasks: [
                'ValueState 计数器',
                'MapState 用户画像',
                '配置 TTL 过期',
                '状态后端切换'
            ]
        },
        {
            id: 'lab-05',
            title: 'Lab 5: Checkpoint 与恢复',
            description: '配置Checkpoint机制，测试故障恢复能力。',
            difficulty: 'intermediate',
            duration: '75分钟',
            icon: 'fa-shield-alt',
            tasks: [
                '启用 Checkpoint',
                '配置状态后端',
                '模拟故障场景',
                '验证恢复结果'
            ]
        },
        {
            id: 'lab-06',
            title: 'Lab 6: CEP 复杂事件处理',
            description: '使用CEP库检测复杂事件模式，实现欺诈检测。',
            difficulty: 'advanced',
            duration: '90分钟',
            icon: 'fa-project-diagram',
            tasks: [
                '定义匹配模式',
                '设置时间约束',
                '处理匹配结果',
                '优化模式性能'
            ]
        }
    ],

    // 编程挑战
    challenges: [
        {
            id: 'challenge-01',
            title: 'Challenge 1: 实时热门商品统计',
            description: '实现一个实时统计电商平台热门商品Top N的程序。',
            difficulty: 'beginner',
            duration: '2小时',
            points: 100,
            icon: 'fa-fire',
            requirements: [
                '使用 Kafka 作为数据源',
                '每分钟统计一次热门商品',
                '输出 Top 10 商品列表',
                '处理乱序数据'
            ],
            template: `import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

public class HotItems {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = 
            StreamExecutionEnvironment.getExecutionEnvironment();
        
        // TODO: 从 Kafka 读取用户行为数据
        
        // TODO: 设置 Watermark 策略
        
        // TODO: 按商品ID分组，统计点击次数
        
        // TODO: 使用窗口聚合计算热门商品
        
        // TODO: 输出结果到 Sink
        
        env.execute("Hot Items Job");
    }
}`,
            testCases: [
                { input: 'user1,item1,click,1000', expected: 'item1: 1' },
                { input: 'user2,item1,click,2000', expected: 'item1: 2' },
                { input: 'user3,item2,click,3000', expected: 'item2: 1' }
            ]
        },
        {
            id: 'challenge-02',
            title: 'Challenge 2: 恶意登录检测',
            description: '使用CEP检测短时间内多次失败的登录尝试，识别可疑行为。',
            difficulty: 'intermediate',
            duration: '3小时',
            points: 200,
            icon: 'fa-user-shield',
            requirements: [
                '定义登录失败模式',
                '5分钟内失败3次触发告警',
                '输出告警到指定Sink',
                '处理正常登录重置'
            ],
            template: `import org.apache.flink.cep.CEP;
import org.apache.flink.cep.PatternStream;
import org.apache.flink.cep.pattern.Pattern;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class LoginDetection {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = 
            StreamExecutionEnvironment.getExecutionEnvironment();
        
        // TODO: 读取登录日志流
        
        // TODO: 定义恶意登录模式（5分钟内3次失败）
        Pattern<LoginEvent, ?> pattern = Pattern
            .<LoginEvent>begin("fail")
            // ...
            .within(Time.minutes(5));
        
        // TODO: 应用模式检测
        
        // TODO: 处理匹配结果，输出告警
        
        env.execute("Login Detection Job");
    }
}`,
            testCases: [
                { input: 'user1,fail,t1;user1,fail,t2;user1,fail,t3', expected: 'ALERT: user1' },
                { input: 'user1,success,t1', expected: 'OK' }
            ]
        },
        {
            id: 'challenge-03',
            title: 'Challenge 3: 订单超时处理',
            description: '实现订单创建到支付的超时检测，自动取消超时订单。',
            difficulty: 'intermediate',
            duration: '3小时',
            points: 200,
            icon: 'fa-shopping-cart',
            requirements: [
                '监控订单创建事件',
                '30分钟未支付标记超时',
                '处理支付完成事件',
                '更新订单状态'
            ],
            template: `import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.co.CoProcessFunction;

public class OrderTimeout {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = 
            StreamExecutionEnvironment.getExecutionEnvironment();
        
        // TODO: 读取订单创建流
        
        // TODO: 读取支付完成流
        
        // TODO: 使用 Connect 和 CoProcessFunction 处理
        
        // TODO: 注册定时器检测超时
        
        // TODO: 输出超时订单
        
        env.execute("Order Timeout Job");
    }
}`,
            testCases: [
                { input: 'order1,create,t1;order1,pay,t2', expected: 'order1: PAID' },
                { input: 'order2,create,t1', expected: 'order2: TIMEOUT' }
            ]
        },
        {
            id: 'challenge-04',
            title: 'Challenge 4: 实时推荐系统',
            description: '基于用户行为实现简单的实时商品推荐。',
            difficulty: 'advanced',
            duration: '4小时',
            points: 300,
            icon: 'fa-star',
            requirements: [
                '收集用户行为数据',
                '使用广播状态存储商品特征',
                '实时计算推荐结果',
                '输出个性化推荐'
            ],
            template: `import org.apache.flink.api.common.state.MapState;
import org.apache.flink.api.common.state.MapStateDescriptor;
import org.apache.flink.streaming.api.datastream.BroadcastStream;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class RealtimeRecommendation {
    
    private static final MapStateDescriptor<String, ItemProfile> 
        itemStateDescriptor = 
            new MapStateDescriptor<>("items", String.class, ItemProfile.class);
    
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = 
            StreamExecutionEnvironment.getExecutionEnvironment();
        
        // TODO: 读取用户行为流
        
        // TODO: 读取商品特征流作为广播流
        
        // TODO: 连接两个流进行处理
        
        // TODO: 计算相似度并输出推荐
        
        env.execute("Recommendation Job");
    }
}`,
            testCases: [
                { input: 'user1,view,item1', expected: 'recommend: item2,item3' }
            ]
        },
        {
            id: 'challenge-05',
            title: 'Challenge 5: 实时数据清洗管道',
            description: '构建一个端到端的数据清洗管道，处理各种数据质量问题。',
            difficulty: 'advanced',
            duration: '4小时',
            points: 300,
            icon: 'fa-filter',
            requirements: [
                '数据格式校验',
                '缺失值处理',
                '异常值过滤',
                '数据标准化输出'
            ],
            template: `import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class DataPipeline {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = 
            StreamExecutionEnvironment.getExecutionEnvironment();
        
        // TODO: 读取原始数据流
        
        // TODO: 实现数据校验（格式检查）
        
        // TODO: 处理缺失值
        
        // TODO: 过滤异常值
        
        // TODO: 标准化输出到下游
        
        env.execute("Data Pipeline Job");
    }
}`,
            testCases: [
                { input: '{"id":1,"value":100}', expected: 'VALID' },
                { input: '{"id":2}', expected: 'MISSING_VALUE' },
                { input: 'invalid', expected: 'PARSE_ERROR' }
            ]
        }
    ],

    // 测验
    quizzes: [
        {
            id: 'quiz-01',
            title: '流计算基础知识测验',
            description: '测试你对流计算基础概念的理解，包括时间语义、窗口、一致性模型等。',
            duration: '30分钟',
            questions: 20,
            passingScore: 70,
            icon: 'fa-clipboard-check',
            category: 'fundamentals'
        },
        {
            id: 'quiz-02',
            title: 'Flink 专项测验',
            description: '深入测试Flink特定知识，包括API使用、配置调优等。',
            duration: '30分钟',
            questions: 20,
            passingScore: 70,
            icon: 'fa-code',
            category: 'flink'
        },
        {
            id: 'quiz-03',
            title: '设计模式测验',
            description: '测试流处理常见设计模式的掌握程度。',
            duration: '30分钟',
            questions: 20,
            passingScore: 70,
            icon: 'fa-puzzle-piece',
            category: 'patterns'
        },
        {
            id: 'quiz-04',
            title: '综合测试',
            description: '全面测试流计算知识体系，包含所有主题。',
            duration: '45分钟',
            questions: 30,
            passingScore: 75,
            icon: 'fa-graduation-cap',
            category: 'comprehensive'
        }
    ],

    // 测验题目数据
    quizQuestions: {
        'quiz-01': [
            {
                id: 1,
                question: '在流处理中，Event Time 指的是什么？',
                options: [
                    '数据到达 Flink 的时间',
                    '数据被处理的时间',
                    '数据实际产生的时间',
                    '作业启动的时间'
                ],
                correct: 2,
                explanation: 'Event Time 是事件实际发生的时间，通常嵌入在数据本身中。与之相对的是 Ingestion Time（数据进入Flink的时间）和 Processing Time（数据被处理的时间）。'
            },
            {
                id: 2,
                question: 'Watermark 的主要作用是什么？',
                options: [
                    '加速数据处理',
                    '处理乱序数据，触发窗口计算',
                    '压缩数据传输',
                    '加密敏感数据'
                ],
                correct: 1,
                explanation: 'Watermark 是 Flink 处理乱序数据的核心机制。它表示"所有时间戳小于等于该值的事件都已到达"，用于触发窗口计算和处理延迟数据。'
            },
            {
                id: 3,
                question: '以下哪种情况最适合使用 Processing Time？',
                options: [
                    '金融交易对账',
                    '实时告警系统（低延迟优先）',
                    '用户行为分析',
                    '日志审计'
                ],
                correct: 1,
                explanation: 'Processing Time 提供最低的延迟，适用于对延迟敏感、可以容忍一定不确定性的场景，如实时告警。对于需要精确结果的场景（如金融交易），应该使用 Event Time。'
            },
            {
                id: 4,
                question: '当 Watermark 为 10:00:00 时，以下哪个事件会被认为是迟到数据？',
                options: [
                    '时间戳为 09:59:55 的事件',
                    '时间戳为 10:00:00 的事件',
                    '时间戳为 10:00:01 的事件',
                    '以上都不是'
                ],
                correct: 0,
                explanation: 'Watermark 10:00:00 表示所有时间戳 <= 10:00:00 的事件应该都已到达。因此，时间戳 09:59:55 的事件在 Watermark 10:00:00 之后才到达，属于迟到数据。'
            },
            {
                id: 5,
                question: 'Allowed Lateness 的作用是？',
                options: [
                    '增加处理延迟',
                    '允许在窗口触发后继续接收迟到数据并更新结果',
                    '减少 Checkpoint 间隔',
                    '禁用 Watermark'
                ],
                correct: 1,
                explanation: 'Allowed Lateness 允许在窗口触发后的一段时间内继续接收和处理迟到数据，并可能更新窗口结果。这对于需要一定准确性的场景很有用。'
            },
            {
                id: 6,
                question: '滚动窗口 (Tumbling Window) 的特点是？',
                options: [
                    '窗口之间可能有重叠',
                    '每个事件只属于一个窗口，窗口之间不重叠',
                    '窗口大小不固定',
                    '窗口之间必须有间隔'
                ],
                correct: 1,
                explanation: '滚动窗口的窗口之间不重叠，每个事件只属于一个窗口。例如，1分钟滚动窗口会将时间划分为 [0,60), [60,120), [120,180) 等不重叠的区间。'
            },
            {
                id: 7,
                question: '滑动窗口 (Sliding Window) 的参数包括？',
                options: [
                    '仅窗口大小',
                    '窗口大小和滑动间隔',
                    '仅滑动间隔',
                    '窗口大小和会话超时'
                ],
                correct: 1,
                explanation: '滑动窗口有两个参数：窗口大小（Window Size）和滑动间隔（Slide Interval）。如果滑动间隔 < 窗口大小，窗口会重叠，一个事件可能属于多个窗口。'
            },
            {
                id: 8,
                question: '会话窗口 (Session Window) 的关键特性是？',
                options: [
                    '固定大小',
                    '固定起始时间',
                    '根据活动间隔动态合并',
                    '全局唯一'
                ],
                correct: 2,
                explanation: '会话窗口根据活动间隙（Gap）动态创建和合并。如果在指定时间内没有新事件，会话结束；如果新事件在 Gap 内到达，会话会扩展。'
            },
            {
                id: 9,
                question: 'AggregateFunction 相比 ProcessWindowFunction 的优势是？',
                options: [
                    '可以访问窗口元数据',
                    '可以访问窗口内所有数据',
                    '内存效率更高，支持增量计算',
                    '支持更复杂的逻辑'
                ],
                correct: 2,
                explanation: 'AggregateFunction 支持增量计算，只需要维护一个累加器状态，内存效率高。ProcessWindowFunction 需要缓存窗口内所有元素，内存开销大但功能更强。'
            },
            {
                id: 10,
                question: '窗口触发器 (Trigger) 的作用是？',
                options: [
                    '创建窗口',
                    '决定何时计算和输出窗口结果',
                    '删除过期窗口',
                    '分配事件到窗口'
                ],
                correct: 1,
                explanation: 'Trigger 决定何时触发窗口计算并输出结果。默认情况下，当 Watermark 超过窗口结束时间时触发，但可以通过自定义 Trigger 实现提前触发或延迟触发。'
            },
            {
                id: 11,
                question: 'Exactly-Once 语义的含义是？',
                options: [
                    '每条数据至少被处理一次',
                    '每条数据最多被处理一次',
                    '每条数据恰好被处理一次，结果正确',
                    '数据不丢失但也不处理'
                ],
                correct: 2,
                explanation: 'Exactly-Once 保证每条数据在发生故障恢复后，最终效果等价于恰好处理一次，不会丢失也不会重复处理。注意这指的是结果正确性，而非实际处理次数。'
            },
            {
                id: 12,
                question: 'Flink 的 Checkpoint 机制基于？',
                options: [
                    '两阶段提交',
                    'Chandy-Lamport 分布式快照算法',
                    'Raft 共识算法',
                    'Paxos 算法'
                ],
                correct: 1,
                explanation: 'Flink 使用基于 Chandy-Lamport 算法的分布式异步快照机制实现 Checkpoint。这是一种轻量级的快照方式，不会暂停整个流处理。'
            },
            {
                id: 13,
                question: '以下哪个不是实现 Exactly-Once 的必要条件？',
                options: [
                    '可重放的数据源',
                    '状态快照',
                    '事务性输出',
                    '无限内存'
                ],
                correct: 3,
                explanation: 'Exactly-Once 需要：1) 可重放的数据源（如 Kafka），2) 定期状态快照（Checkpoint），3) 事务性或幂等性输出。不需要无限内存。'
            },
            {
                id: 14,
                question: 'Checkpoint 和 Savepoint 的主要区别是？',
                options: [
                    'Checkpoint 用于升级，Savepoint 用于容错',
                    'Checkpoint 由 Flink 自动触发，Savepoint 由用户手动触发',
                    'Checkpoint 保存状态，Savepoint 不保存',
                    'Checkpoint 仅支持内存状态'
                ],
                correct: 1,
                explanation: 'Checkpoint 是自动触发的容错机制，用于故障恢复；Savepoint 是用户手动触发的，用于作业升级、迁移等运维操作。两者都保存完整状态。'
            },
            {
                id: 15,
                question: 'Barriers 在 Checkpoint 中的作用是？',
                options: [
                    '分隔数据',
                    '标记快照边界，确保一致性',
                    '压缩数据',
                    '加密数据'
                ],
                correct: 1,
                explanation: 'Barriers 是 Flink Checkpoint 的核心机制。它们被周期性地注入数据流，作为快照的边界。当算子收到所有输入流的 Barrier 时，就知道可以安全地对当前状态进行快照。'
            },
            {
                id: 16,
                question: 'ValueState 和 MapState 的主要区别是？',
                options: [
                    'ValueState 更快',
                    'MapState 可以存储键值对集合',
                    'ValueState 支持 TTL',
                    'MapState 只能存储一个值'
                ],
                correct: 1,
                explanation: 'ValueState 为每个 key 存储单个值，MapState 为每个 key 存储一个 Map（键值对集合）。两者都支持 TTL。'
            },
            {
                id: 17,
                question: 'State TTL 用于解决什么问题？',
                options: [
                    '提高处理速度',
                    '自动清理过期状态，防止无限增长',
                    '增加状态可见性',
                    '减少网络传输'
                ],
                correct: 1,
                explanation: 'State TTL（Time-To-Live）允许为状态设置过期时间，过期后自动清理，防止状态无限增长导致内存溢出。'
            },
            {
                id: 18,
                question: 'Keyed State 和 Operator State 的区别是？',
                options: [
                    'Keyed State 只能用于 Source',
                    'Operator State 按 key 分区',
                    'Keyed State 按 key 分区，Operator State 不分区',
                    '没有区别'
                ],
                correct: 2,
                explanation: 'Keyed State 与特定 key 关联，按 key 分区和并发处理；Operator State 与算子实例关联，通常用于 Source/Sink 等非 keyBy 场景。'
            },
            {
                id: 19,
                question: 'RocksDBStateBackend 适合什么场景？',
                options: [
                    '小状态，快速访问',
                    '大状态，内存有限',
                    '只读状态',
                    '临时状态'
                ],
                correct: 1,
                explanation: 'RocksDBStateBackend 将状态存储在磁盘上，适合大状态场景。MemoryStateBackend 适合小状态，FsStateBackend 适合中等大小状态。'
            },
            {
                id: 20,
                question: '在 Flink 中，以下哪个操作会自动触发 Checkpoint？',
                options: [
                    'map()',
                    'filter()',
                    'keyBy()',
                    '以上都不会'
                ],
                correct: 3,
                explanation: 'Checkpoint 由 Checkpoint Coordinator 周期性地触发，与具体算子操作无关。用户可以通过 env.enableCheckpointing(interval) 启用和配置 Checkpoint。'
            }
        ]
    },

    // 成就列表
    achievements: [
        {
            id: 'first-login',
            title: '初次见面',
            description: '首次登录学习平台',
            icon: 'fa-hand-wave',
            condition: '首次访问平台'
        },
        {
            id: 'first-course',
            title: '开始学习',
            description: '完成第一个课程',
            icon: 'fa-play',
            condition: '完成任意课程'
        },
        {
            id: 'first-lab',
            title: '动手实践',
            description: '完成第一个实验',
            icon: 'fa-flask',
            condition: '完成任意实验'
        },
        {
            id: 'first-challenge',
            title: '编程新手',
            description: '完成第一个编程挑战',
            icon: 'fa-code',
            condition: '完成任意挑战'
        },
        {
            id: 'perfect-quiz',
            title: '满分学霸',
            description: '测验获得满分',
            icon: 'fa-star',
            condition: '任意测验满分'
        },
        {
            id: 'study-streak-7',
            title: '坚持不懈',
            description: '连续学习7天',
            icon: 'fa-fire',
            condition: '连续7天登录学习'
        },
        {
            id: 'csa-certified',
            title: 'CSA 认证',
            description: '获得 CSA 认证',
            icon: 'fa-certificate',
            condition: '通过 CSA 考试'
        },
        {
            id: 'csp-certified',
            title: 'CSP 认证',
            description: '获得 CSP 认证',
            icon: 'fa-crown',
            condition: '通过 CSP 考试'
        },
        {
            id: 'cse-certified',
            title: 'CSE 认证',
            description: '获得 CSE 认证',
            icon: 'fa-trophy',
            condition: '通过 CSE 考试'
        }
    ]
};

// 导出数据
if (typeof module !== 'undefined' && module.exports) {
    module.exports = coursesData;
}
