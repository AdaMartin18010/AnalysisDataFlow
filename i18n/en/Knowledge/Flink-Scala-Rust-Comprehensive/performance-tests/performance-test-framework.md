---
title: "Stream Processing Performance Testing Framework"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Stream Processing Performance Testing Framework

> **Stage**: Knowledge/Flink-Scala-Rust-Comprehensive | **Prerequisites**: [Nexmark Benchmark](./nexmark-benchmark-suite.md) | **Formalization Level**: L3

## 1. Framework Goals

This framework provides a complete stream processing performance testing infrastructure, supporting:

| Capability | Description | Implementation Technology |
|------------|-------------|---------------------------|
| Cross-platform Benchmarking | Supports JVM, Native, WASM runtimes | JMH + Criterion |
| Reproducible Experiments | Version control + Environment固化 | Docker + Configuration Management |
| Automated Reporting | Chart generation + Statistical analysis | Python + Matplotlib |
| Regression Detection | Historical comparison + Threshold alerting | CI/CD Integration |

## 2. Framework Architecture

```mermaid
graph TB
    subgraph "Performance Testing Framework"
        A[Test Definition Layer] --> B[Data Generation Layer]
        B --> C[Execution Engine Layer]
        C --> D[Metrics Collection Layer]
        D --> E[Analysis Report Layer]

        A --> A1[YAML Config]
        A --> A2[Code Annotations]

        B --> B1[Nexmark Generator]
        B --> B2[Custom Generator]

        C --> C1[JMH]
        C --> C2[Criterion]
        C --> C3[Flink MiniCluster]

        D --> D1[JFR]
        D --> D2[Prometheus]
        D --> D3[Custom Sink]

        E --> E1[CSV Export]
        E --> E2[HTML Report]
        E --> E3[Trend Charts]
    end
```

## 3. Core Component Implementation

### 3.1 Test Configuration DSL

```yaml
# performance-tests/config/nexmark-q5.yaml
benchmark:
  name: "Nexmark Q5 Hot Items"
  version: "1.0"
  description: "Sliding window Top-N query performance test"

environment:
  jvm:
    version: "11"
    heap_size: "4g"
    gc: "G1"
    options:
      - "-XX:+UseStringDeduplication"
      - "-XX:MaxGCPauseMillis=100"

  flink:
    version: "1.18.0"
    parallelism: 4
    checkpointing:
      enabled: true
      interval: 10s
      mode: "EXACTLY_ONCE"
    state_backend:
      type: "rocksdb"
      incremental: true

workload:
  generator: "nexmark"
  config:
    events_per_second: 100000
    total_events: 10000000
    person_ratio: 1
    auction_ratio: 1
    bid_ratio: 9

queries:
  - id: "Q5"
    type: "sliding_window_top_n"
    window_size: "60s"
    slide_interval: "1s"
    top_n: 10

metrics:
  throughput:
    unit: "events/second"
    aggregation: "mean"
    report_p50: true
    report_p99: true

  latency:
    unit: "milliseconds"
    percentiles: [50, 90, 99, 99.9]

  resources:
    cpu_percent: true
    memory_mb: true
    gc_pause_ms: true

duration:
  warmup_seconds: 60
  measurement_seconds: 300
  iterations: 3
```

### 3.2 Java/JMH Testing Framework

```java
// performance-tests/framework/src/main/java/benchmark/StreamBenchmark.java
package benchmark;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.results.RunResult;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.configuration.RestOptions;

import java.util.concurrent.TimeUnit;
import java.util.Collection;

import org.apache.flink.streaming.api.datastream.DataStream;


@State(Scope.Benchmark)
@BenchmarkMode({Mode.Throughput, Mode.AverageTime})
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Warmup(iterations = 3, time = 10)
@Measurement(iterations = 5, time = 30)
@Fork(2)
public class StreamBenchmark {

    protected StreamExecutionEnvironment env;
    protected BenchmarkConfig config;
    protected MetricsCollector metricsCollector;

    @Setup(Level.Trial)
    public void setup() {
        // Configure Flink environment
        Configuration flinkConfig = new Configuration();
        flinkConfig.setInteger(RestOptions.PORT, 0); // random port

        env = StreamExecutionEnvironment.createLocalEnvironment(
            config.getParallelism(),
            flinkConfig
        );

        env.setParallelism(config.getParallelism());
        env.enableCheckpointing(config.getCheckpointInterval());

        // Set state backend
        if ("rocksdb".equals(config.getStateBackend())) {
            env.setStateBackend(new EmbeddedRocksDBStateBackend(config.isIncrementalCheckpointing()));
        }

        // Start metrics collection
        metricsCollector = new MetricsCollector(env);
        metricsCollector.start();
    }

    @TearDown(Level.Trial)
    public void tearDown() {
        if (metricsCollector != null) {
            metricsCollector.stop();
            metricsCollector.exportResults(config.getOutputDir());
        }
    }

    @Benchmark
    public BenchmarkResult runQuery() throws Exception {
        // Build data stream
        DataStream<Event> source = env.addSource(
            new NexmarkSource(config.getGeneratorConfig())
        );

        // Apply query
        DataStream<Result> result = QueryFactory
            .create(config.getQueryId())
            .apply(source);

        // Collect results
        ResultCollector collector = new ResultCollector();
        result.addSink(collector);

        // Execute
        JobExecutionResult executionResult = env.execute(
            "Benchmark-" + config.getQueryId()
        );

        return new BenchmarkResult(
            executionResult.getNetRuntime(TimeUnit.MILLISECONDS),
            collector.getRecordCount(),
            metricsCollector.getMetrics()
        );
    }

    public static void main(String[] args) throws RunnerException {
        Options opt = new OptionsBuilder()
            .include(StreamBenchmark.class.getSimpleName())
            .addProfiler(GCProfiler.class)
            .addProfiler(AsyncProfiler.class)
            .resultFormat(ResultFormatType.JSON)
            .result("benchmark-results.json")
            .build();

        Collection<RunResult> results = new Runner(opt).run();

        // Generate report
        ReportGenerator.generate(results, "benchmark-report.html");
    }
}
```

### 3.3 Rust/Criterion Testing Framework

```rust
// performance-tests/framework/src/lib.rs
use criterion::{Criterion, BenchmarkGroup, measurement::WallTime};
use std::time::Duration;

pub struct BenchmarkSuite {
    name: String,
    config: BenchmarkConfig,
}

impl BenchmarkSuite {
    pub fn new(name: &str, config: BenchmarkConfig) -> Self {
        Self {
            name: name.to_string(),
            config,
        }
    }

    pub fn run<F, T>(&self, group_name: &str, f: F)
    where
        F: FnMut() -> T,
    {
        let mut criterion = Criterion::default()
            .warm_up_time(Duration::from_secs(self.config.warmup_secs))
            .measurement_time(Duration::from_secs(self.config.measurement_secs))
            .sample_size(self.config.sample_size);

        let mut group = criterion.benchmark_group(group_name);

        group.bench_function(&self.name, |b| {
            b.iter(f)
        });

        group.finish();
        criterion.final_summary();
    }
}

pub struct BenchmarkConfig {
    pub warmup_secs: u64,
    pub measurement_secs: u64,
    pub sample_size: usize,
    pub iterations: u32,
}

impl Default for BenchmarkConfig {
    fn default() -> Self {
        Self {
            warmup_secs: 10,
            measurement_secs: 30,
            sample_size: 100,
            iterations: 5,
        }
    }
}
```

### 3.4 Metrics Collector

```scala
// performance-tests/framework/src/main/scala/metrics/MetricsCollector.scala
package metrics

import org.apache.flink.metrics.{Counter, Gauge, Histogram, Meter}
import org.apache.flink.runtime.metrics.MetricNames
import org.apache.flink.streaming.api.scala._

import java.util.concurrent.ConcurrentHashMap
import scala.collection.JavaConverters._

case class MetricSnapshot(
  timestamp: Long,
  throughput: Double,
  latencyP50: Double,
  latencyP99: Double,
  cpuPercent: Double,
  memoryMB: Long,
  gcCount: Long,
  gcTimeMs: Long
)

class MetricsCollector(env: StreamExecutionEnvironment) {

  private val snapshots = new ConcurrentHashMap[Long, MetricSnapshot]()
  private var collectorThread: Thread = _
  private var running = false

  def start(): Unit = {
    running = true
    collectorThread = new Thread(() => {
      while (running) {
        collectSnapshot()
        Thread.sleep(1000) // collect every second
      }
    })
    collectorThread.start()
  }

  def stop(): Unit = {
    running = false
    if (collectorThread != null) {
      collectorThread.join(5000)
    }
  }

  private def collectSnapshot(): Unit = {
    val timestamp = System.currentTimeMillis()

    // Collect from Flink Metric system
    val snapshot = MetricSnapshot(
      timestamp = timestamp,
      throughput = collectThroughput(),
      latencyP50 = collectLatencyPercentile(50),
      latencyP99 = collectLatencyPercentile(99),
      cpuPercent = collectCPUUsage(),
      memoryMB = collectMemoryUsage(),
      gcCount = collectGCCount(),
      gcTimeMs = collectGCTime()
    )

    snapshots.put(timestamp, snapshot)
  }

  private def collectThroughput(): Double = {
    // Retrieve from Flink Metrics
    0.0 // placeholder
  }

  private def collectLatencyPercentile(p: Int): Double = {
    0.0 // placeholder
  }

  private def collectCPUUsage(): Double = {
    val bean = java.lang.management.ManagementFactory.getOperatingSystemMXBean
    val method = bean.getClass.getDeclaredMethod("getProcessCpuLoad")
    method.setAccessible(true)
    method.invoke(bean).asInstanceOf[Double] * 100
  }

  private def collectMemoryUsage(): Long = {
    val runtime = Runtime.getRuntime
    (runtime.totalMemory() - runtime.freeMemory()) / (1024 * 1024)
  }

  private def collectGCCount(): Long = {
    java.lang.management.ManagementFactory.getGarbageCollectorMXBeans
      .asScala
      .map(_.getCollectionCount)
      .sum
  }

  private def collectGCTime(): Long = {
    java.lang.management.ManagementFactory.getGarbageCollectorMXBeans
      .asScala
      .map(_.getCollectionTime)
      .sum
  }

  def getMetrics(): List[MetricSnapshot] = {
    snapshots.values().asScala.toList.sortBy(_.timestamp)
  }

  def exportResults(outputDir: String): Unit = {
    val metrics = getMetrics()

    // Export CSV
    val csv = new StringBuilder
    csv.append("timestamp,throughput,latency_p50,latency_p99,cpu_percent,memory_mb,gc_count,gc_time_ms\n")

    metrics.foreach { m =>
      csv.append(s"${m.timestamp},${m.throughput},${m.latencyP50},${m.latencyP99},${m.cpuPercent},${m.memoryMB},${m.gcCount},${m.gcTimeMs}\n")
    }

    java.nio.file.Files.write(
      java.nio.file.Paths.get(outputDir, "metrics.csv"),
      csv.toString.getBytes
    )

    // Export JSON
    val json = ujson.Obj(
      "benchmark" -> ujson.Str("nexmark-q5"),
      "metrics" -> ujson.Arr(metrics.map(toJson): _*)
    )

    java.nio.file.Files.write(
      java.nio.file.Paths.get(outputDir, "metrics.json"),
      json.toString.getBytes
    )
  }

  private def toJson(m: MetricSnapshot): ujson.Obj = {
    ujson.Obj(
      "timestamp" -> ujson.Num(m.timestamp),
      "throughput" -> ujson.Num(m.throughput),
      "latency_p50" -> ujson.Num(m.latencyP50),
      "latency_p99" -> ujson.Num(m.latencyP99)
    )
  }
}
```

### 3.5 Statistical Analysis and Visualization

```python
# performance-tests/framework/src/main/python/analyze.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import sys
from pathlib import Path

def load_metrics(csv_path):
    """Load metrics CSV file"""
    return pd.read_csv(csv_path)

def plot_throughput_over_time(df, output_path):
    """Plot throughput over time"""
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['throughput'], label='Throughput')
    plt.axhline(y=df['throughput'].mean(), color='r', linestyle='--', label='Mean')
    plt.fill_between(df['timestamp'],
                     df['throughput'].mean() - df['throughput'].std(),
                     df['throughput'].mean() + df['throughput'].std(),
                     alpha=0.2)
    plt.xlabel('Time')
    plt.ylabel('Events/Second')
    plt.title('Throughput Over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()

def plot_latency_distribution(df, output_path):
    """Plot latency distribution"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Time series
    axes[0].plot(df['timestamp'], df['latency_p50'], label='P50')
    axes[0].plot(df['timestamp'], df['latency_p99'], label='P99')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Latency (ms)')
    axes[0].set_title('Latency Over Time')
    axes[0].legend()
    axes[0].grid(True)

    # Box plot
    latency_data = [df['latency_p50'], df['latency_p99']]
    axes[1].boxplot(latency_data, labels=['P50', 'P99'])
    axes[1].set_ylabel('Latency (ms)')
    axes[1].set_title('Latency Distribution')
    axes[1].grid(True)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_resource_usage(df, output_path):
    """Plot resource usage"""
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # CPU usage
    axes[0].plot(df['timestamp'], df['cpu_percent'])
    axes[0].set_ylabel('CPU %')
    axes[0].set_title('CPU Usage')
    axes[0].grid(True)

    # Memory usage
    axes[1].plot(df['timestamp'], df['memory_mb'])
    axes[1].set_xlabel('Time')
    axes[1].set_ylabel('Memory (MB)')
    axes[1].set_title('Memory Usage')
    axes[1].grid(True)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def generate_summary(df):
    """Generate statistical summary"""
    summary = {
        "throughput": {
            "mean": df['throughput'].mean(),
            "std": df['throughput'].std(),
            "min": df['throughput'].min(),
            "max": df['throughput'].max(),
            "p50": df['throughput'].median(),
            "p99": df['throughput'].quantile(0.99)
        },
        "latency_p50": {
            "mean": df['latency_p50'].mean(),
            "p99": df['latency_p50'].quantile(0.99)
        },
        "latency_p99": {
            "mean": df['latency_p99'].mean(),
            "max": df['latency_p99'].max()
        },
        "resources": {
            "avg_cpu": df['cpu_percent'].mean(),
            "peak_memory_mb": df['memory_mb'].max(),
            "total_gc_time_ms": df['gc_time_ms'].iloc[-1] - df['gc_time_ms'].iloc[0]
        }
    }
    return summary

def generate_html_report(df, summary, output_path):
    """Generate HTML report"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Performance Benchmark Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .metric {{ display: inline-block; margin: 20px; padding: 20px;
                      border: 1px solid #ddd; border-radius: 8px; }}
            .metric-value {{ font-size: 32px; font-weight: bold; color: #2196F3; }}
            .metric-label {{ font-size: 14px; color: #666; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #2196F3; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Performance Benchmark Report</h1>
        <p>Generated: {pd.Timestamp.now()}</p>

        <h2>Key Metrics</h2>
        <div class="metric">
            <div class="metric-value">{summary['throughput']['mean']:.0f}</div>
            <div class="metric-label">Avg Throughput (events/s)</div>
        </div>
        <div class="metric">
            <div class="metric-value">{summary['latency_p50']['mean']:.2f}</div>
            <div class="metric-label">Avg Latency P50 (ms)</div>
        </div>
        <div class="metric">
            <div class="metric-value">{summary['latency_p99']['mean']:.2f}</div>
            <div class="metric-label">Avg Latency P99 (ms)</div>
        </div>
        <div class="metric">
            <div class="metric-value">{summary['resources']['peak_memory_mb']:.0f}</div>
            <div class="metric-label">Peak Memory (MB)</div>
        </div>

        <h2>Detailed Statistics</h2>
        <table>
            <tr><th>Metric</th><th>Mean</th><th>Std</th><th>Min</th><th>Max</th><th>P50</th><th>P99</th></tr>
            <tr>
                <td>Throughput</td>
                <td>{summary['throughput']['mean']:.0f}</td>
                <td>{summary['throughput']['std']:.0f}</td>
                <td>{summary['throughput']['min']:.0f}</td>
                <td>{summary['throughput']['max']:.0f}</td>
                <td>{summary['throughput']['p50']:.0f}</td>
                <td>{summary['throughput']['p99']:.0f}</td>
            </tr>
        </table>

        <h2>Charts</h2>
        <img src="throughput.png" width="100%">
        <img src="latency.png" width="100%">
        <img src="resources.png" width="100%">
    </body>
    </html>
    """

    with open(output_path, 'w') as f:
        f.write(html)

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <metrics.csv>")
        sys.exit(1)

    csv_path = sys.argv[1]
    output_dir = Path(csv_path).parent

    # Load data
    df = load_metrics(csv_path)

    # Generate charts
    plot_throughput_over_time(df, output_dir / 'throughput.png')
    plot_latency_distribution(df, output_dir / 'latency.png')
    plot_resource_usage(df, output_dir / 'resources.png')

    # Generate summary
    summary = generate_summary(df)

    # Save JSON
    with open(output_dir / 'summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    # Generate HTML report
    generate_html_report(df, summary, output_dir / 'report.html')

    print(f"Report generated: {output_dir / 'report.html'}")

if __name__ == '__main__':
    main()
```

## 4. Usage Examples

### 4.1 Run Full Test

```bash
# 1. Prepare environment
cd performance-tests
./setup.sh

# 2. Run test
./run-benchmark.sh --config config/nexmark-q5.yaml --output results/q5/

# 3. Generate report
python framework/src/main/python/analyze.py results/q5/metrics.csv

# 4. View report
open results/q5/report.html
```

### 4.2 CI/CD Integration

```yaml
# .github/workflows/benchmark.yml
name: Performance Benchmark

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Environment
        uses: ./.github/actions/setup-benchmark

      - name: Run Benchmarks
        run: |
          ./run-benchmark.sh \
            --config config/nexmark-all.yaml \
            --output benchmark-results/

      - name: Compare with Baseline
        run: |
          python framework/src/main/python/compare.py \
            --baseline baseline-results/ \
            --current benchmark-results/ \
            --threshold 5% \
            --output comparison.md

      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const comparison = fs.readFileSync('comparison.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comparison
            });
```

## 5. Framework Extensions

### 5.1 Add New Test

```scala
// 1. Define test class
@BenchmarkMeta(id = "Q6", description = "Session Window")
class Q6Benchmark extends StreamBenchmark {
  override def buildPipeline(): DataStream[Result] = {
    // Implement test logic
  }
}

// 2. Add to suite
object BenchmarkSuite {
  def main(args: Array[String]): Unit = {
    register("Q6", classOf[Q6Benchmark])
    runAll()
  }
}
```

### 5.2 Custom Metrics

```java
public class CustomMetricsCollector implements MetricsCollector {
    @Override
    public void collect(Environment env) {
        // Custom metrics collection logic
        record("custom.metric", measure());
    }
}
```

---
