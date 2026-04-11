package nexmark

import org.apache.flink.streaming.api.functions.source.{RichParallelSourceFunction, SourceFunction}
import org.apache.flink.configuration.Configuration

import java.time.Instant
import java.util.Random

class NexmarkGenerator(config: GeneratorConfig) extends RichParallelSourceFunction[NexmarkEvent] {
  
  @volatile private var isRunning = true
  private var eventCount = 0L
  private var nextId = 0L
  private val random = new Random()
  
  override def open(parameters: Configuration): Unit = {
    val subtaskIndex = getRuntimeContext.getIndexOfThisSubtask
    val totalSubtasks = getRuntimeContext.getNumberOfParallelSubtasks
    nextId = config.firstEventNumber + subtaskIndex
  }
  
  override def run(ctx: SourceFunction.SourceContext[NexmarkEvent]): Unit = {
    val startTime = System.currentTimeMillis()
    
    while (isRunning && eventCount < config.maxEvents) {
      val event = generateNextEvent()
      val timestamp = System.currentTimeMillis()
      
      ctx.collectWithTimestamp(event, timestamp)
      eventCount += 1
      
      // 速率控制
      val expectedTime = startTime + (eventCount * 1000L / config.eventsPerSecond)
      val sleepTime = expectedTime - System.currentTimeMillis()
      if (sleepTime > 0) {
        Thread.sleep(sleepTime)
      }
    }
  }
  
  private def generateNextEvent(): NexmarkEvent = {
    val totalProportion = config.personProportion + config.auctionProportion + config.bidProportion
    val randomValue = random.nextInt(totalProportion)
    val now = Instant.now()
    
    if (randomValue < config.personProportion) {
      generatePerson(now)
    } else if (randomValue < config.personProportion + config.auctionProportion) {
      generateAuction(now)
    } else {
      generateBid(now)
    }
  }
  
  private def generatePerson(now: Instant): Person = {
    val id = nextId
    nextId += getRuntimeContext.getNumberOfParallelSubtasks
    
    val states = Array("OR", "ID", "CA", "TX", "NY", "WA", "FL", "AZ")
    val cities = Array("Portland", "Boise", "Los Angeles", "Austin", "New York", 
                       "Seattle", "Miami", "Phoenix")
    
    val stateIdx = random.nextInt(states.length)
    Person(
      id = id,
      name = s"Person_$id",
      email = s"person$id@example.com",
      creditCard = f"${random.nextInt(10000)}%04d-${random.nextInt(10000)}%04d",
      city = cities(stateIdx),
      state = states(stateIdx),
      timestamp = now
    )
  }
  
  private def generateAuction(now: Instant): Auction = {
    val id = nextId
    nextId += getRuntimeContext.getNumberOfParallelSubtasks
    
    val categories = (1L to 20L).toArray
    val category = categories(random.nextInt(categories.length))
    val initialBid = 1000 + random.nextInt(9000)
    val reserve = (initialBid * (1.0 + random.nextDouble())).toLong
    
    Auction(
      id = id,
      itemName = s"Item_$id",
      description = s"Description for item $id",
      initialBid = initialBid,
      reserve = reserve,
      dateTime = now,
      expires = now.plusSeconds(60 + random.nextInt(300)),
      seller = math.abs(random.nextLong()) % 1000000,
      category = category,
      timestamp = now
    )
  }
  
  private def generateBid(now: Instant): Bid = {
    val channels = Array("Google", "Facebook", "Twitter", "Bing", "Direct")
    
    Bid(
      auction = math.abs(random.nextLong()) % 1000000,
      bidder = math.abs(random.nextLong()) % 1000000,
      price = 100 + random.nextInt(9900),
      channel = channels(random.nextInt(channels.length)),
      url = s"https://example.com/auction/${random.nextInt(1000000)}",
      dateTime = now,
      extra = s"extra_${random.nextInt(1000)}",
      timestamp = now
    )
  }
  
  override def cancel(): Unit = {
    isRunning = false
  }
}
