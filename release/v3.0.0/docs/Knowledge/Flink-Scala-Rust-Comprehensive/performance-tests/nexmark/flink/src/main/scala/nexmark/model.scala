package nexmark

import java.time.Instant

// 事件基类
trait NexmarkEvent extends Serializable {
  def id: Long
  def timestamp: Instant
}

// Person 事件 - 用户注册
case class Person(
  id: Long,
  name: String,
  email: String,
  creditCard: String,
  city: String,
  state: String,
  timestamp: Instant
) extends NexmarkEvent

// Auction 事件 - 拍卖创建
case class Auction(
  id: Long,
  itemName: String,
  description: String,
  initialBid: Long,
  reserve: Long,
  dateTime: Instant,
  expires: Instant,
  seller: Long,
  category: Long,
  timestamp: Instant
) extends NexmarkEvent

// Bid 事件 - 竞价
case class Bid(
  auction: Long,
  bidder: Long,
  price: Long,
  channel: String,
  url: String,
  dateTime: Instant,
  extra: String,
  timestamp: Instant
) extends NexmarkEvent {
  override def id: Long = auction
}

// 查询结果
case class QueryResult(
  queryId: String,
  throughput: Double,
  latencyP50: Double,
  latencyP99: Double,
  cpuUsage: Double,
  memoryMB: Long
)

// Q1 结果
case class BidConverted(
  auction: Long,
  bidder: Long,
  price: Double,
  dateTime: Instant,
  extra: String
)

// Q2 结果
case class AuctionPrice(auction: Long, price: Long)

// Q3 结果
case class PersonAuctionJoin(
  personName: String,
  city: String,
  state: String,
  auctionId: Long,
  itemName: String
)

// Q5 结果
case class HotItemResult(
  auction: Long,
  price: Long,
  bidder: Long,
  windowStart: Instant
)

// Q8 结果
case class NewUserMonitorResult(
  personId: Long,
  personName: String,
  stateCount: Long
)

// 配置类
case class GeneratorConfig(
  firstEventNumber: Long = 0L,
  maxEvents: Long = 100_000_000L,
  eventsPerSecond: Long = 10_000L,
  personProportion: Int = 1,
  auctionProportion: Int = 1,
  bidProportion: Int = 9
)

case class BenchmarkConfig(
  queryId: String = "Q0",
  parallelism: Int = 4,
  maxEvents: Long = 10_000_000L,
  eventsPerSecond: Long = 100_000L,
  checkpointInterval: Long = 10000L,
  checkpointDir: String = "file:///tmp/flink-checkpoints",
  maxOutOfOrderness: Long = 1000L
)

object BenchmarkConfig {
  def parse(args: Array[String]): BenchmarkConfig = {
    var config = BenchmarkConfig()
    
    var i = 0
    while (i < args.length) {
      args(i) match {
        case "--query" | "-q" => 
          config = config.copy(queryId = args(i + 1))
          i += 2
        case "--parallelism" | "-p" =>
          config = config.copy(parallelism = args(i + 1).toInt)
          i += 2
        case "--max-events" | "-e" =>
          config = config.copy(maxEvents = args(i + 1).toLong)
          i += 2
        case "--events-per-second" | "-r" =>
          config = config.copy(eventsPerSecond = args(i + 1).toLong)
          i += 2
        case _ => i += 1
      }
    }
    
    config
  }
}
