package nexmark

import org.apache.flink.api.common.eventtime.{SerializableTimestampAssigner, WatermarkStrategy}
import org.apache.flink.contrib.streaming.state.EmbeddedRocksDBStateBackend
import org.apache.flink.runtime.state.storage.FileSystemCheckpointStorage
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.{CheckpointingMode, TimeCharacteristic}

import java.time.Duration
import java.util.concurrent.TimeUnit

object BenchmarkRunner {
  
  def main(args: Array[String]): Unit = {
    val config = BenchmarkConfig.parse(args)
    
    println(s"Starting Nexmark Benchmark - Query ${config.queryId}")
    println(s"Configuration: $config")
    
    // 创建执行环境
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setParallelism(config.parallelism)
    env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)
    
    // 配置 Checkpoint
    if (config.checkpointInterval > 0) {
      env.enableCheckpointing(config.checkpointInterval)
      env.getCheckpointConfig.setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE)
      env.getCheckpointConfig.setCheckpointStorage(
        new FileSystemCheckpointStorage(config.checkpointDir)
      )
      env.setStateBackend(new EmbeddedRocksDBStateBackend(true))
    }
    
    // 配置 Watermark 策略
    val watermarkStrategy = WatermarkStrategy
      .forBoundedOutOfOrderness[NexmarkEvent](Duration.ofMillis(config.maxOutOfOrderness))
      .withTimestampAssigner(new SerializableTimestampAssigner[NexmarkEvent] {
        override def extractTimestamp(element: NexmarkEvent, recordTimestamp: Long): Long = {
          element.timestamp.toEpochMilli
        }
      })
    
    // 创建数据源
    val generatorConfig = GeneratorConfig(
      maxEvents = config.maxEvents,
      eventsPerSecond = config.eventsPerSecond
    )
    
    // 根据查询选择对应的数据流
    val resultStream = config.queryId match {
      case "Q0" => 
        val source = createBidSource(env, generatorConfig, watermarkStrategy)
        Q0.execute(env, source)
        
      case "Q1" =>
        val source = createBidSource(env, generatorConfig, watermarkStrategy)
        Q1.execute(env, source)
        
      case "Q2" =>
        val source = createBidSource(env, generatorConfig, watermarkStrategy)
        Q2.execute(env, source)
        
      case "Q5" =>
        val source = createBidSource(env, generatorConfig, watermarkStrategy)
        Q5.execute(env, source)
        
      case "Q8" =>
        val source = createPersonSource(env, generatorConfig, watermarkStrategy)
        Q8.execute(env, source)
        
      case _ => throw new IllegalArgumentException(s"Unknown query: ${config.queryId}")
    }
    
    // 添加性能监控 Sink
    resultStream
      .addSink(new PerformanceMetricsSink(config.queryId))
      .name("PerformanceMetrics")
    
    // 执行
    val jobResult = env.execute(s"Nexmark-${config.queryId}")
    
    // 输出结果
    println(s"Benchmark completed: ${jobResult.getJobID}")
    println(s"Duration: ${jobResult.getNetRuntime(TimeUnit.SECONDS)}s")
  }
  
  private def createBidSource(
    env: StreamExecutionEnvironment,
    config: GeneratorConfig,
    watermarkStrategy: WatermarkStrategy[NexmarkEvent]
  ): DataStream[Bid] = {
    env
      .addSource(new NexmarkGenerator(config))
      .filter(_.isInstanceOf[Bid])
      .map(_.asInstanceOf[Bid])
      .assignTimestampsAndWatermarks(watermarkStrategy.asInstanceOf[WatermarkStrategy[Bid]])
  }
  
  private def createPersonSource(
    env: StreamExecutionEnvironment,
    config: GeneratorConfig,
    watermarkStrategy: WatermarkStrategy[NexmarkEvent]
  ): DataStream[Person] = {
    env
      .addSource(new NexmarkGenerator(config))
      .filter(_.isInstanceOf[Person])
      .map(_.asInstanceOf[Person])
      .assignTimestampsAndWatermarks(watermarkStrategy.asInstanceOf[WatermarkStrategy[Person]])
  }
}

// 性能指标 Sink
class PerformanceMetricsSink(queryId: String) 
  extends org.apache.flink.streaming.api.functions.sink.RichSinkFunction[Any] {
  
  private var eventCount = 0L
  private var startTime = 0L
  private var lastReportTime = 0L
  private var lastEventCount = 0L
  
  override def open(parameters: org.apache.flink.configuration.Configuration): Unit = {
    startTime = System.currentTimeMillis()
    lastReportTime = startTime
  }
  
  override def invoke(value: Any): Unit = {
    eventCount += 1
    
    val currentTime = System.currentTimeMillis()
    val elapsed = currentTime - startTime
    
    // 每 5 秒输出一次统计
    if (currentTime - lastReportTime >= 5000) {
      val periodEvents = eventCount - lastEventCount
      val periodTime = (currentTime - lastReportTime) / 1000.0
      val throughput = periodEvents / periodTime
      val totalThroughput = eventCount * 1000.0 / elapsed
      
      println(f"[$queryId] Time: ${elapsed / 1000}s, Events: $eventCount, " +
               f"Instant Throughput: $throughput%.2f events/s, " +
               f"Avg Throughput: $totalThroughput%.2f events/s")
      
      lastReportTime = currentTime
      lastEventCount = eventCount
    }
  }
  
  override def close(): Unit = {
    val elapsed = System.currentTimeMillis() - startTime
    val totalThroughput = if (elapsed > 0) eventCount * 1000.0 / elapsed else 0.0
    println(f"[$queryId] Final - Total Events: $eventCount, " +
             f"Duration: ${elapsed / 1000}s, " +
             f"Final Avg Throughput: $totalThroughput%.2f events/s")
  }
}
