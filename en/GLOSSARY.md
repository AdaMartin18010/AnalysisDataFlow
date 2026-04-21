# Streaming & Flink Glossary

> **Language**: English | **Last Updated**: 2026-04-21

---

## A

**At-Least-Once** — A delivery guarantee where every record is processed one or more times. May produce duplicates on recovery.

**At-Most-Once** — A delivery guarantee where records are processed zero or one times. May lose records on failure.

## B

**Backpressure** — A flow-control mechanism where a slow downstream operator propagates pressure upstream, causing sources to reduce ingestion rate.

**Barrier** — A special event injected into the data stream to demarcate the boundary between pre-checkpoint and post-checkpoint data.

**Broadcast State** — A state type where identical state is replicated to all parallel instances of an operator, used for configuration or rule distribution.

## C

**Checkpoint** — A consistent snapshot of all operator states at a specific point in time, used for fault tolerance and recovery.

**Chandy-Lamport Snapshot** — The foundational algorithm for distributed snapshots, upon which Flink's checkpointing is based.

## E

**Event Time** — The timestamp embedded in the record itself, representing when the event actually occurred in the real world.

**Exactly-Once** — A processing guarantee where every record's effect on state and sink is applied exactly once, even across failures.

## K

**Keyed Stream** — A stream partitioned by a key, allowing stateful operations (aggregations, windows) scoped to each key.

## L

**Late Data** — Records that arrive after the watermark has already advanced past their event time, potentially missing their assigned window.

## S

**State Backend** — The pluggable component responsible for storing and checkpointing operator state. Flink supports Heap and RocksDB backends.

**Stream Record** — The fundamental unit of data in a Flink data stream, consisting of a value and optionally a timestamp.

## W

**Watermark** — A metadata event that carries a timestamp, signaling that no records with earlier event times are expected to arrive.

**Window** — A logical grouping of records by time or count boundaries, enabling aggregate computations over finite subsets of an infinite stream.

---

## References
