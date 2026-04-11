package nexmark

import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.scala.function.ProcessWindowFunction
import org.apache.flink.streaming.api.windowing.assigners.{SlidingEventTimeWindows, TumblingEventTimeWindows}
import org.apache.flink.streaming.api.windowing.time.Time
import org.apache.flink.streaming.api.windowing.windows.TimeWindow
import org.apache.flink.util.Collector

// 查询 trait
trait NexmarkQuery extends Serializable {
  def name: String
}

trait SingleStreamQuery[OUT] extends NexmarkQuery {
  def execute(env: StreamExecutionEnvironment, source: DataStream[Bid]): DataStream[OUT]
}

// Q0: Passthrough
object Q0 extends SingleStreamQuery[Bid] {
  override def name: String = "Q0-Passthrough"
  
  override def execute(env: StreamExecutionEnvironment, source: DataStream[Bid]): DataStream[Bid] = {
    source.map(bid => bid.copy(price = bid.price))
      .name("Q0-Passthrough")
      .uid("q0-pass")
  }
}

// Q1: Currency Conversion
object Q1 extends SingleStreamQuery[BidConverted] {
  override def name: String = "Q1-CurrencyConversion"
  
  private val EXCHANGE_RATE = 0.908
  
  override def execute(env: StreamExecutionEnvironment, source: DataStream[Bid]): DataStream[BidConverted] = {
    source.map { bid =>
      BidConverted(
        auction = bid.auction,
        bidder = bid.bidder,
        price = bid.price * EXCHANGE_RATE,
        dateTime = bid.dateTime,
        extra = bid.extra
      )
    }
    .name("Q1-CurrencyConversion")
    .uid("q1-conversion")
  }
}

// Q2: Selection
object Q2 extends SingleStreamQuery[AuctionPrice] {
  override def name: String = "Q2-Selection"
  
  private val targetAuctions = Set(1007L, 1020L, 2001L, 2019L, 2087L)
  
  override def execute(env: StreamExecutionEnvironment, source: DataStream[Bid]): DataStream[AuctionPrice] = {
    source
      .filter(bid => targetAuctions.contains(bid.auction))
      .map(bid => AuctionPrice(bid.auction, bid.price))
      .name("Q2-Selection")
      .uid("q2-filter")
  }
}

// Q5: Hot Items
object Q5 extends SingleStreamQuery[HotItemResult] {
  override def name: String = "Q5-HotItems"
  
  private val WINDOW_SIZE = Time.seconds(60)
  private val WINDOW_SLIDE = Time.seconds(1)
  
  case class MaxBidPrice(auction: Long, price: Long, windowStart: Long)
  
  override def execute(env: StreamExecutionEnvironment, source: DataStream[Bid]): DataStream[HotItemResult] = {
    
    // Step 1: 计算每个 auction 在每个窗口内的最高出价
    val maxPrices = source
      .keyBy(_.auction)
      .window(SlidingEventTimeWindows.of(WINDOW_SIZE, WINDOW_SLIDE))
      .aggregate(
        new AggregateFunction[Bid, Long, MaxBidPrice] {
          override def createAccumulator(): Long = Long.MinValue
          override def add(bid: Bid, acc: Long): Long = math.max(acc, bid.price)
          override def getResult(acc: Long): MaxBidPrice = MaxBidPrice(0, acc, 0)
          override def merge(a: Long, b: Long): Long = math.max(a, b)
        },
        new ProcessWindowFunction[MaxBidPrice, MaxBidPrice, Long, TimeWindow] {
          override def process(
            key: Long,
            context: Context,
            elements: Iterable[MaxBidPrice],
            out: Collector[MaxBidPrice]
          ): Unit = {
            elements.foreach { m =>
              out.collect(m.copy(auction = key, windowStart = context.window.getStart))
            }
          }
        }
      )
    
    // Step 2: 找出每个窗口内价格最高的 auction
    maxPrices
      .keyBy(_.windowStart)
      .window(SlidingEventTimeWindows.of(WINDOW_SIZE, WINDOW_SLIDE))
      .process(new ProcessWindowFunction[MaxBidPrice, HotItemResult, Long, TimeWindow] {
        override def process(
          key: Long,
          context: Context,
          elements: Iterable[MaxBidPrice],
          out: Collector[HotItemResult]
        ): Unit = {
          val maxPrice = elements.map(_.price).max
          elements.filter(_.price == maxPrice).foreach { m =>
            out.collect(HotItemResult(
              auction = m.auction,
              price = m.price,
              bidder = 0L,
              windowStart = java.time.Instant.ofEpochMilli(m.windowStart)
            ))
          }
        }
      })
      .name("Q5-HotItems")
      .uid("q5-hot-items")
  }
}

// Q8: Monitor New Users
object Q8 extends NexmarkQuery {
  override def name: String = "Q8-MonitorNewUsers"
  
  private val WINDOW_SIZE = Time.hours(12)
  
  def execute(env: StreamExecutionEnvironment, source: DataStream[Person]): DataStream[NewUserMonitorResult] = {
    source
      .windowAll(TumblingEventTimeWindows.of(WINDOW_SIZE))
      .process(new ProcessAllWindowFunction[Person, NewUserMonitorResult, TimeWindow] {
        override def process(
          context: Context,
          elements: Iterable[Person],
          out: Collector[NewUserMonitorResult]
        ): Unit = {
          val persons = elements.toList
          val maxTime = persons.map(_.timestamp).max
          val windowStart = maxTime.minusSeconds(12 * 3600)
          
          val recentPersons = persons.filter(_.timestamp.isAfter(windowStart))
          val stateCounts = recentPersons.groupBy(_.state).view.mapValues(_.size.toLong).toMap
          
          recentPersons.foreach { p =>
            out.collect(NewUserMonitorResult(
              personId = p.id,
              personName = p.name,
              stateCount = stateCounts.getOrElse(p.state, 0L)
            ))
          }
        }
      })
      .name("Q8-MonitorNewUsers")
      .uid("q8-new-users")
  }
}
