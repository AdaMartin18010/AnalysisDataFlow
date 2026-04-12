> **状态**: 🔮 前瞻内容 | **风险等级**: 高 | **最后更新**: 2026-04
>
> 此文档描述的内容处于早期规划阶段，可能与最终实现不符。请以 Apache Flink 官方发布为准。
>
# AnalysisDataFlow Glossar

> **Version**: v1.1 | **Aktualisierungsdatum**: 2026-04-04 | **Umfang**: Gesamtes Projekt
>
> **Versionshinweise**: Markierungen wie [2.0], [2.4], [2.5], [3.0] bei Begriffen zeigen an, dass diese in der entsprechenden Flink-Version eingeführt oder zu einer Kernfunktion wurden
>
> Dieses Dokument ist die maßgebliche Begriffsreferenz des AnalysisDataFlow-Projekts, alphabetisch sortiert und deckt die Bereiche Stream-Computing-Theorie, Flink-Ingenieurpraxis und Cutting-Edge-Technologien ab.

---

## Inhaltsverzeichnis

- [Glossar-Navigation](#glossar-navigation)
- [Begriffskategorie-Index](#begriffskategorie-index)
- [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [K](#k) · [L](#l) · [M](#m) · [P](#p) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [W](#w)

---

## Glossar-Navigation

| Kategorie | Begriffsanzahl | Hauptbereiche |
|-----------|----------------|---------------|
| [Grundlagenbegriffe](#1-grundlagenbegriffe) | 35+ | Stream-Computing, Batch-Verarbeitung, Echtzeit-Verarbeitung |
| [Theoriebegriffe](#2-theoriebegriffe) | 40+ | Prozesskalküle, Formalisierungsverifikation, Typentheorie |
| [Flink-Begriffe](#3-flink-begriffe) | 50+ | Kernkonzepte, APIs, Konfigurationsparameter |
| [Ingenieurbegriffe](#4-ingenieurbegriffe) | 30+ | Design-Patterns, Architektur, Betrieb |
| [Cutting-Edge-Begriffe](#5-cutting-edge-begriffe) | 35+ | AI Agents, Stream-Datenbanken, Cloud-Native |

---

## Begriffskategorie-Index

### 1. Grundlagenbegriffe

- **Stream-Computing**: Dataflow, Event Time, Processing Time, Watermark, Window
- **Batch-Verarbeitung**: Batch Processing, Bounded Stream, Checkpoint
- **Echtzeit-Verarbeitung**: Real-time Processing, Latency, Throughput

### 2. Theoriebegriffe

- **Prozesskalkül-Begriffe**: CCS, CSP, π-Calculus, Actor Model, Session Types
- **Formalisierungsverifikation**: Bisimulation, Model Checking, TLA+, Iris
- **Typentheorie**: FG/FGG, DOT, Path-Dependent Types

### 3. Flink-Begriffe

- **Kernkonzepte**: JobManager, TaskManager, Operator, State Backend
- **API-bezogen**: DataStream API, Table API, SQL
- **Konfigurationsparameter**: Parallelism, Checkpoint Interval, Watermark Strategy

### 4. Ingenieurbegriffe

- **Design-Patterns**: Windowed Aggregation, Async I/O, Side Output
- **Architektur**: Microservices, Event-Driven Architecture, Data Mesh
- **Betrieb**: Backpressure, Monitoring, Autoscaling

### 5. Cutting-Edge-Begriffe

- **AI Agent-Begriffe**: AI Agent, ReAct, MCP, A2A, Agentic Workflow, FLIP-531
- **Serverless**: Serverless Flink, Scale-to-Zero, FaaS
- **Performance-Optimierung**: Adaptive Execution Engine, Smart Checkpointing
- **Stream-Datenbanken**: Materialized View, Continuous Query, Incremental Update
- **Cloud-Native**: Kubernetes, Serverless, WASM, Lakehouse

---

## A

### Adaptive Execution Engine (Adaptiver Ausführungsmotor) [Flink 1.17+]

**Definition**: Von Flink eingeführter intelligenter Ausführungsoptimierungsrahmen, der Ausführungsplan, Ressourcenallokation und Parallelität dynamisch basierend auf Laufzeitstatistiken anpasst.

**Formalisierungsdefinition**:

```
AEE-V2 = (𝒫, ℳ, 𝒜, 𝒞, ℛ, δ, π)
```

wobei 𝒫 der physische Ausführungsplan, ℳ die Laufzeitmetriken, 𝒜 die adaptiven Aktionen, 𝒞 die Beschränkungen, ℛ der Re-Optimizer, δ die Entscheidungsfunktion und π das Performance-Vorhersagemodell ist.

**Kernfähigkeiten**: Automatische Daten-Skew-Verarbeitung, dynamische Parallelitätsanpassung, adaptive Ressourcenallokation

**Verwandte Begriffe**: Smart Checkpointing, Backpressure, Parallelism

---

### Actor Model (Actor-Modell)

**Definition**: Ein Nebenläufigkeits-Computing-Modell, in dem die grundlegende Berechnungseinheit der Actor ist – eine autonome Einheit, die Nachrichten empfangen, Entscheidungen treffen, neue Actors erstellen und Nachrichten senden kann.

**Formalisierungsdefinition**:

```
Actor ::= ⟨Mailbox, Behavior, State, Children, Supervisor⟩
```

**Verwandte Begriffe**: CSP (Communicating Sequential Processes), π-Calculus, Nachrichtenübermittlung

---

### AI Agent (Künstliche-Intelligenz-Agent) [Allgemeiner Begriff]

**Definition**: Ein intelligentes System, das autonom in der Umgebung wahrnehmen, schlussfolgern, handeln und lernen kann, formalisiert als 6-Tupel:

```
𝒜_agent ≜ ⟨𝒮, 𝒫, 𝒟, 𝒜, ℳ, 𝒢⟩
```

wobei 𝒮 der Zustandsraum, 𝒫 die Wahrnehmung, 𝒟 die Entscheidung, 𝒜 die Aktion, ℳ das Gedächtnis und 𝒢 das Ziel ist.

**Flink-Integration**: Flink Agent ist eine auf dem Stream-Computing-Framework basierende AI-Agent-Implementierung

**Verwandte Begriffe**: ReAct, MCP, A2A, Multi-Agent, FLIP-531

---

### A2A Protocol (Agent-to-Agent-Protokoll) [Google 2025]

**Definition**: Von Google vorgeschlagener offener Agent-Interoperabilitätsstandard, der Aufgabendelegation, Zustandssynchronisation und Ergebnisrückgabe zwischen Agents unterstützt.

**Formalisierungsdefinition**:

```
A2A_Flink = ⟨𝒫, ℳ, 𝒮, 𝒜⟩
```

wobei 𝒫 die Menge der teilnehmenden Agents, ℳ die Nachrichtentypen, 𝒮 die Sitzungszustandsmaschine und 𝒜 der Authentifizierungs-Autorisierungsmechanismus ist.

**Aufgabenstatus-Übergang**: `pending → working → input-required → completed/failed`

**Verwandte Begriffe**: AI Agent, MCP, Orchestration, FLIP-531

---

### Aligned Checkpoint (Ausgerichteter Checkpoint)

**Definition**: Flink-Mechanismus, bei dem ein Operator einen Zustands-Snapshot erst erst auslöst, nachdem er Barriere von **allen** Eingangskanälen empfangen hat.

**Formalisierungsdefinition**:

```
AlignedSnapshot(t, n) ⟺ ∀c ∈ Inputs(t): Barrier(n) ∈ Received(c)
```

**Verwandte Begriffe**: Unaligned Checkpoint, Barrier, Exactly-Once

---

### Async I/O (Asynchrones I/O)

**Definition**: Ein Pattern, das es Stream-Processing-Operatoren ermöglicht, externe Systemaufrufe nebenläufig auszuführen, um die Blockierung des Datenflusses zu vermeiden.

**Formalisierungsdefinition**:

```
AsyncFunction: I × C → Future[O]
```

wobei C der Parallelitätsparameter ist, der die Anzahl gleichzeitig laufender asynchroner Anfragen steuert.

**Verwandte Begriffe**: Backpressure, Enrichment, Concurrency

---

### At-Least-Once (Mindestens-einmal-Semantik)

**Definition**: Die Semantik eines Stream-Computing-Systems, die garantiert, dass die Auswirkungen jeder Eingabedaten auf die externe Welt **mindestens einmal** erfolgen.

**Formalisierungsdefinition**:

```
∀r ∈ I. c(r, 𝒯) ≥ 1
```

wobei c(r, 𝒯) die Kausalitäts-Einflusszählung ist.

**Verwandte Begriffe**: At-Most-Once, Exactly-Once, Delivery Guarantee

---

### At-Most-Once (Höchstens-einmal-Semantik)

**Definition**: Die Semantik eines Stream-Computing-Systems, die garantiert, dass die Auswirkungen jeder Eingabedaten auf die externe Welt **höchstens einmal** erfolgen, mit möglichem Datenverlust.

**Formalisierungsdefinition**:

```
∀r ∈ I. c(r, 𝒯) ≤ 1
```

**Verwandte Begriffe**: At-Least-Once, Exactly-Once, Best-Effort

---

## B

### Backpressure (Rückstau)

**Definition**: Ein Mechanismus in Stream-Processing-Systemen, bei dem die Flusskontrollsignale nach oben weitergegeben werden, wenn die Downstream-Verarbeitung langsamer als der Upstream ist.

**Prinzip**: Credit-basierte Flusskontrolle; Senden wird pausiert, wenn der Empfangspuffer voll ist.

**Verwandte Begriffe**: Flow Control, Buffer, Credit-Based

---

### Barrier (Checkpoint Barrier)

**Definition**: Ein spezielles Kontrollereignis in Flink, das in den Datenstrom eingefügt wird, um die Daten-Grenzen zwischen verschiedenen Checkpoints zu trennen.

**Formalisierungsdefinition**:

```
Barrier(n) = ⟨Type = CONTROL, checkpointId = n, timestamp = ts⟩
```

**Verwandte Begriffe**: Checkpoint, Aligned Checkpoint, Unaligned Checkpoint

---

### Batch Processing (Stapelverarbeitung)

**Definition**: Ein Berechnungsmodell zur Verarbeitung endlicher, begrenzter Datensätze, bei dem die Daten vor Berechnungsbeginn vollständig verfügbar sind.

**Merkmale**:

- Eingabedaten sind begrenzt (Bounded)
- Zugriff auf vollständigen Datensatz möglich
- Latenz ist nicht kritisch, hoher Durchsatz wird angestrebt

**Verwandte Begriffe**: Stream Processing, Bounded Stream, Lambda Architecture

---

### Best-Effort (Bestmöglicher Versuch)

**Definition**: Eine Liefersemantik ohne Konsistenzgarantien; das System verarbeitet Daten nach bestem Bemühen, garantiert aber weder Verlustfreiheit noch Eindeutigkeit.

**Verwandte Begriffe**: At-Most-Once, Delivery Guarantee

---

### Bisimulation (Bisimulation)

**Definition**: Eine Beziehung in der Prozessalgebra zur Bestimmung der Verhaltensäquivalenz zweier Prozesse, die verlangt, dass beide Prozesse alle möglichen Aktionen gegenseitig simulieren können.

**Formalisierungsdefinition**:

```
R ist eine Bisimulation ⟺ ∀(P,Q)∈R. ∀α. P→αP' ⇒ ∃Q'. Q→αQ' ∧ (P',Q')∈R
```

**Verwandte Begriffe**: Process Calculus, Trace Equivalence, CCS

---

### Bounded Stream (Begrenzter Strom)

**Definition**: Ein Datenstrom mit endlicher Datenmenge; Datenabstraktion der Stapelverarbeitung.

**Formalisierungsdefinition**:

```
Bounded(S) ⟺ |S| < ∞
```

**Verwandte Begriffe**: Unbounded Stream, Batch Processing

---

### Buffer (Puffer)

**Definition**: Ein Speicherbereich in der Stream-Verarbeitung zur temporären Datenspeicherung zwischen Produzent und Konsument.

**Verwandte Begriffe**: Backpressure, Queue, Network Buffer

---

## C

### CALM Theorem (CALM-Theorem)

**Definition**: Consistency As Logical Monotonicity — logisch monotone Programme können Konsistenz ohne Koordination garantieren.

**Formalisierungsausdruck**:

```
Programm P koordinationsfrei ⟺ P ist logisch monoton
```

**Verwandte Begriffe**: Eventual Consistency, Coordination

---

### Causal Consistency (Kausale Konsistenz)

**Definition**: Ein Konsistenzmodell in verteilten Systemen, das die Reihenfolge kausal abhängiger Operationen bewahrt.

**Formalisierungsdefinition**:

```
∀op_i, op_j. op_i ≺hb op_j ⇒ op_i ≺obs op_j
```

**Verwandte Begriffe**: Strong Consistency, Eventual Consistency, Happens-Before

---

### CEP (Complex Event Processing, Komplexe Ereignisverarbeitung)

**Definition**: Eine Technologie zur Erkennung komplexer Muster in Ereignisströmen und Generierung zusammengesetzter Ereignisse.

**Formalisierungsdefinition**:

```
CEP: Stream × Pattern → DetectedEvents
```

**Verwandte Begriffe**: Pattern Matching, Event Pattern, Window

---

### CCS (Calculus of Communicating Systems)

**Definition**: Von Milner 1980 vorgeschlagene Prozessalgebra basierend auf markierter Synchronisation.

**Syntax**:

```
P, Q ::= 0 | α.P | P + Q | P | Q | P \ L | P[f]
```

**Verwandte Begriffe**: CSP, π-Calculus, Process Algebra

---

### CDC (Change Data Capture, Änderungsdatenerfassung)

**Definition**: Eine Technologie zum Erfassen von Datenbank-Änderungsereignissen (Einfügen, Aktualisieren, Löschen) und deren Echtzeit-Propagation zu Downstream-Systemen.

**Verwandte Begriffe**: Debezium, Streaming ETL, Log Mining

---

### Checkpoint (Kontrollpunkt)

**Definition**: Ein global konsistenter Zustands-Snapshot eines verteilten Stream-Verarbeitungsauftrags zu einem bestimmten Zeitpunkt, verwendet für Fehlerwiederherstellung.

**Formalisierungsdefinition**:

```
CP = ⟨ID, TS, {S_i}_{i∈Tasks}, Metadata⟩
```

**Verwandte Begriffe**: Savepoint, State Backend, Recovery

---

### Chandy-Lamport Algorithm

**Definition**: Ein klassischer Algorithmus in verteilten Systemen zum Erfassen global konsistenter Snapshots; theoretische Grundlage von Flink Checkpoints.

**Verwandte Begriffe**: Global Snapshot, Consistent Cut, Checkpoint

---

### Choreographic Programming (Choreographische Programmierung)

**Definition**: Ein verteiltes Programmierparadigma, das Interaktionsprotokolle zwischen mehreren Parteien aus globaler Sicht beschreibt und dann auf die einzelnen Parteien projiziert.

**Verwandte Begriffe**: Session Types, Endpoint Projection, Deadlock Freedom

---

### Cloud-Native (Cloud-Nativ)

**Definition**: Eine Methodik zum Erstellen und Betreiben von Anwendungen unter Nutzung der Vorteile von Cloud-Computing, mit Schwerpunkt auf Containerisierung, Microservices, Continuous Delivery und DevOps.

**Verwandte Begriffe**: Kubernetes, Containerization, Microservices

---

### Concurrency (Nebenläufigkeit)

**Definition**: Die Fähigkeit mehrerer Berechnungsaufgaben, sich in überlappenden Zeitabschnitten auszuführen; zu unterscheiden von Parallelism (Parallelität).

**Verwandte Begriffe**: Parallelism, Race Condition, Synchronization

---

### Consistency Model (Konsistenzmodell)

**Definition**: Eine Menge von Regeln, die die Sichtbarkeit und Reihenfolge von Datenoperationen in verteilten Systemen definieren.

**Hierarchie**: Strong Consistency → Causal Consistency → Eventual Consistency

**Verwandte Begriffe**: Linearizability, Serializability, CAP Theorem

---

### Continuous Query (Kontinuierliche Abfrage)

**Definition**: Eine Abfrage in Stream-Datenbanken, die kontinuierlich läuft und Ergebnisse automatisch aktualisiert, wenn Daten eintreffen.

**Formalisierungsdefinition**:

```
q: S → 𝒱, wobei q eine zeitveränderliche Funktion ist
```

**Verwandte Begriffe**: Materialized View, Streaming Database

---

### Credit-Based Flow Control (Kredit-basierte Flusskontrolle)

**Definition**: Ein Mechanismus, bei dem der Empfänger durch Senden von Kreditwerten dem Sender mitteilt, wie viele Daten er empfangen kann.

**Verwandte Begriffe**: Backpressure, Flow Control

---

### CSP (Communicating Sequential Processes)

**Definition**: Von Hoare 1985 vorgeschlagene Prozessalgebra basierend auf synchroner Kommunikation und statischen Ereignisnamen.

**Syntax**:

```
P, Q ::= STOP | SKIP | a → P | P □ Q | P ⊓ Q | P ||| Q | P |[A]| Q
```

**Verwandte Begriffe**: CCS, π-Calculus, Go Channels

---

## D

### Dataflow Model (Dataflow-Modell)

**Definition**: Ein Modell, das Berechnungen als Datenfluss zwischen Operatoren darstellt; die zentrale theoretische Grundlage des Stream-Computing.

**Formalisierungsdefinition**:

```
𝒢 = (V, E, P, Σ, 𝕋)
```

wobei V die Menge der Knoten, E die Menge der Kanten, P die Verarbeitungsfunktion, Σ der Zustand und 𝕋 das Zeitmodell ist.

**Verwandte Begriffe**: DAG, Operator, Stream Graph

---

### DAG (Directed Acyclic Graph, Gerichteter azyklischer Graph)

**Definition**: Eine Graphstruktur zur Darstellung von Stream-Verarbeitungstopologien; Knoten sind Operatoren, Kanten sind Datenströme, ohne Zyklen.

**Verwandte Begriffe**: Dataflow Model, Job Graph, Execution Graph

---

### Deadlock Freedom (Verklemmungsfreiheit)

**Definition**: Eine Eigenschaft, die garantiert, dass kein Prozess dauerhaft blockiert ist, weil er auf ein Ereignis wartet, das nie eintritt.

**Verwandte Begriffe**: Liveness, Choreographic Programming, Session Types

---

### Delivery Guarantee (Liefergarantie)

**Definition**: Die Zusicherung eines Stream-Verarbeitungssystems bezüglich der Zuverlässigkeit der Nachrichtenübermittlung; unterteilt in At-Most-Once, At-Least-Once, Exactly-Once.

**Verwandte Begriffe**: At-Most-Once, At-Least-Once, Exactly-Once

---

### Determinism (Determinismus)

**Definition**: Die Eigenschaft, dass ein System bei gleicher Eingabe immer die gleiche Ausgabe erzeugt.

**Formalisierungsdefinition**:

```
Deterministic(P) ⟺ ∀x. P(x) = P(x)
```

**Verwandte Begriffe**: Reproducibility, Consistency

---

### Distributed Snapshot (Verteilter Snapshot)

**Definition**: Ein konsistenter Snapshot, der den globalen Zustand eines verteilten Systems zu einem bestimmten Zeitpunkt erfasst.

**Verwandte Begriffe**: Chandy-Lamport Algorithm, Checkpoint, Consistent Cut

---

## E

### Edge Computing (Edge-Computing)

**Definition**: Ein Berechnungsparadigma, das Datenverarbeitung in der Nähe der Datenquelle (am Netzwerk-Edge) durchführt, um Latenz und Bandbreitenverbrauch zu reduzieren.

**Verwandte Begriffe**: Cloud-Edge Continuum, IoT, Latency

---

### End-to-End Consistency (Ende-zu-Ende-Konsistenz)

**Definition**: Die Konsistenzgarantie für die gesamte Pipeline von der externen Datenquelle bis zum externen Datensenke.

**Formalisierungsdefinition**:

```
End-to-End-EO(J) ⟺ Replayable(Src) ∧ ConsistentCheckpoint(Ops) ∧ AtomicOutput(Snk)
```

**Verwandte Begriffe**: Internal Consistency, Exactly-Once, Source, Sink

---

### Event-Driven Architecture (Ereignis-getriebene Architektur)

**Definition**: Ein Software-Architekturpattern, das die Komponenteninteraktion um die Erzeugung, Erkennung und Verbrauch von Ereignissen organisiert.

**Verwandte Begriffe**: Event Streaming, Pub/Sub, CQRS

---

### Event Time (Ereigniszeit)

**Definition**: Der Zeitstempel, zu dem ein Datensatz erzeugt wurde; vom Datenquelle zugewiesen.

**Formalisierungsdefinition**:

```
t_e: Record → Timestamp
```

**Verwandte Begriffe**: Processing Time, Ingestion Time, Watermark

---

### Eventual Consistency (Eventuelle Konsistenz)

**Definition**: Ein Konsistenzmodell, das garantiert, dass alle Repliken schließlich zum gleichen Wert konvergieren, wenn keine neuen Updates vorliegen.

**Formalisierungsdefinition**:

```
◇□(replicas converge)
```

**Verwandte Begriffe**: Strong Consistency, Causal Consistency, CALM Theorem

---

### Exactly-Once (Genau-einmal-Semantik)

**Definition**: Die Semantik eines Stream-Computing-Systems, die garantiert, dass die Auswirkungen jeder Eingabedaten auf die externe Welt **genau einmal** erfolgen.

**Formalisierungsdefinition**:

```
∀r ∈ I. c(r, 𝒯) = 1
```

**Verwandte Begriffe**: At-Least-Once, At-Most-Once, Idempotency

---

### Execution Graph (Ausführungsgraph)

**Definition**: Eine Graphstruktur in Flink, die den logischen JobGraph in einen physischen Ausführungsplan umwandelt; enthält konkrete parallele Instanzen.

**Verwandte Begriffe**: Job Graph, Task, Parallelism

---

## F

### Flink Agent [Flink 2.0+, FLIP-531]

**Definition**: Ein autonomer intelligenter Agent, der auf dem Flink Stream-Computing-Framework basiert; unterstützt kontinuierliche Wahrnehmung, Entscheidung und Aktion.

**Formalisierungsdefinition**:

```
𝒜_Flink = ⟨𝒮_state, 𝒫_perception, 𝒟_decision, 𝒜_action, ℳ_memory, 𝒢_goal⟩
```

**Kernmerkmale**: Zustandspersistenz, Replayability, verteilte Ausführung, Exactly-Once-Semantik

**Verwandte Begriffe**: AI Agent, FLIP-531, MCP, A2A, Stateful Stream Processing

---

### FLIP-531 (Flink AI Agents Proposal) [Flink 2.0+]

**Definition**: Offizieller Feature-Vorschlag von Apache Flink zur Einführung nativer AI-Agent-Laufzeitunterstützung und tiefer Integration von Stream-Computing und AI-Intelligenz.

**Kernkomponenten**:

- **Flink Agent Runtime**: Agent-Ausführungsumgebung
- **MCP-Integration**: Model Context Protocol Unterstützung
- **A2A-Protokoll**: Agent-zu-Agent-Interoperabilität
- **Agentic Workflow**: Intelligente Agent-Workflow-Orchestrierung

**Formalisierungsdefinition**:

```
FLIP-531 = ⟨ℛ_agent, ℐ_mcp, 𝒫_a2a, 𝒲_workflow⟩
```

**Verwandte Begriffe**: Flink Agent, MCP, A2A, Agentic Workflow

---

### Flow Control (Flusskontrolle)

**Definition**: Ein Mechanismus zur Regulierung der Datenübertragungsrate zwischen Datenproduzent und -konsument.

**Verwandte Begriffe**: Backpressure, Credit-Based, Buffer

---

### Function as a Service (FaaS)

**Definition**: Ein Serverless-Computing-Modell, bei dem Benutzer Funktionscode schreiben und die Plattform Infrastruktur und automatische Skalierung verwaltet.

**Verwandte Begriffe**: Serverless, Lambda, Cloud-Native

---

## G

### GPU Acceleration (GPU-Beschleunigung) [Flink 2.5+]

**Definition**: Nutzung der massiven Parallelitätsfähigkeiten von GPUs zur Ausführung von Stream-Processing-Operatoren; CPU-intensive Operationen werden über CUDA/OpenCL auf die GPU ausgelagert.

**Formalisierungsdefinition**:

```
𝒪_GPU(D) = GPUKernel(Transfer(D_CPU→GPU))
```

**Beschleunigungsverhältnis**: S_GPU = T_CPU / (T_transfer + T_kernel + T_sync)

**Anwendungsbedingungen**: Batch-Größe n > n_threshold UND Berechnung/Transfer-Verhältnis > γ

**Verwandte Begriffe**: CUDA, Vector Search, Flink-CUDA Runtime

---

### Global Snapshot (Globaler Snapshot)

**Definition**: Die Menge aller Prozesszustände eines verteilten Systems zu einem bestimmten Zeitpunkt; verwendet für Fehlerwiederherstellung und Konsistenzprüfung.

**Verwandte Begriffe**: Distributed Snapshot, Chandy-Lamport Algorithm, Checkpoint

---

### Global Window (Globales Fenster)

**Definition**: Ein einzelnes Fenster, das alle Datensätze enthält; normalerweise mit benutzerdefiniertem Trigger verwendet.

**Formalisierungsdefinition**:

```
Global: wid_global = (-∞, +∞)
```

**Verwandte Begriffe**: Tumbling Window, Sliding Window, Session Window

---

## H

### Happens-Before (Happens-Before-Beziehung)

**Definition**: Eine Beziehung, die die kausale Partialordnung zwischen Ereignissen definiert; Grundlage der verteilten Konsistenz.

**Verwandte Begriffe**: Causal Consistency, Partial Order, Clock

---

## I

### Idempotency (Idempotenz)

**Definition**: Die Eigenschaft, dass eine Operation bei mehrfacher Anwendung außer der ersten keinen weiteren Einfluss auf den Systemzustand hat.

**Formalisierungsdefinition**:

```
f(x) = f(f(x))
```

**Verwandte Begriffe**: Exactly-Once, At-Least-Once, Fault Tolerance

---

### Incremental Checkpoint (Inkrementeller Checkpoint)

**Definition**: Ein Checkpoint-Mechanismus, der nur den seit dem letzten Checkpoint geänderten Zustand speichert.

**Verwandte Begriffe**: Checkpoint, State Backend, RocksDB

---

### Ingestion Time (Erfassungszeit)

**Definition**: Der Zeitstempel, zu dem ein Datensatz in das Stream-Verarbeitungssystem aufgenommen wurde.

**Verwandte Begriffe**: Event Time, Processing Time, Watermark

---

## K

### Keyed State (Schlüssel-basierter Zustand)

**Definition**: Nach Schlüssel partitionierter Zustand; Datensätze mit dem gleichen Schlüssel greifen auf die gleiche Zustandsinstanz zu.

**Verwandte Begriffe**: Operator State, State Backend, KeyedStream

---

### Kafka

**Definition**: Eine Hochdurchsatz-Streaming-Plattform; bietet Publish/Subscribe-Messaging und Stream-Processing.

**Verwandte Begriffe**: CDC, Streaming ETL, Event Streaming

---

### Kubernetes

**Definition**: Eine Open-Source-Container-Orchestrierungsplattform für das Management containerisierter Workloads und Dienste.

**Verwandte Begriffe**: Cloud-Native, Container, Orchestration

---

## L

### Latency (Latenz)

**Definition**: Die Zeit zwischen dem Auftreten eines Ereignisses und der Verfügbarkeit seiner Verarbeitungsergebnisse.

**Verwandte Begriffe**: Throughput, Event Time, Processing Time

---

### Liveness (Lebendigkeit)

**Definition**: Eine Sicherheitseigenschaft, die garantiert, dass das System letztendlich die erforderliche Aktion ausführt.

**Verwandte Begriffe**: Safety, Deadlock Freedom, Fairness

---

## M

### Materialized View (Materialisierte Sicht)

**Definition**: Ein Datenbankobjekt, das Abfrageergebnisse vorab berechnet und speichert; in Stream-Datenbanken kontinuierlich aktualisiert.

**Verwandte Begriffe**: Continuous Query, Streaming Database, Incremental View Maintenance

---

### MCP (Model Context Protocol) [Anthropic 2024]

**Definition**: Von Anthropic vorgeschlagenes Standardprotokoll, das AI Agents eine einheitliche Schnittstelle zur Kommunikation mit externen Tools und Datenquellen bietet.

**Verwandte Begriffe**: AI Agent, A2A, Tool Calling, Flink Agent

---

### Microservices (Microservices)

**Definition**: Ein Architekturstil, der eine Anwendung als Sammlung kleiner Dienste strukturiert; jeder Dienst läuft in seinem eigenen Prozess und kommuniziert über leichte Mechanismen.

**Verwandte Begriffe**: Service Mesh, Container, Cloud-Native

---

## P

### Parallelism (Parallelität)

**Definition**: Die Anzahl der Instanzen, die eine Aufgabe parallel ausführen.

**Verwandte Begriffe**: Concurrency, Task, Slot

---

### Pattern Matching (Pattern-Matching)

**Definition**: Der Prozess der Abgleichung von Ereignissequenzen gegen in CEP definierte Muster.

**Verwandte Begriffe**: CEP, Event Pattern, Window

---

### Processing Time (Verarbeitungszeit)

**Definition**: Die lokale Zeit der Maschine zu dem Zeitpunkt, zu dem ein Datensatz vom Operator verarbeitet wird.

**Verwandte Begriffe**: Event Time, Ingestion Time, Watermark

---

### π-Calculus (π-Kalkül)

**Definition**: Von Milner vorgeschlagene mobile Prozessalgebra; unterstützt dynamische Kanalerstellung und Namensübergabe.

**Formalisierungsdefinition**:

```
P, Q ::= 0 | α.P | P + Q | P | Q | (νa)P | !P
```

**Verwandte Begriffe**: CCS, CSP, Mobile Processes

---

## R

### Race Condition (Wettlaufbedingung)

**Definition**: Eine Situation, in der mehrere Prozesse auf gemeinsame Ressourcen zugreifen und das Ergebnis von der Zeit abhängt.

**Verwandte Begriffe**: Concurrency, Synchronization, Mutual Exclusion

---

### Replayability (Wiedergabefähigkeit)

**Definition**: Die Fähigkeit einer Quelle, vorherige Daten erneut zu senden; unerlässlich für Exactly-Once-Semantik.

**Verwandte Begriffe**: Exactly-Once, Source, Checkpoint

---

### RocksDB

**Definition**: Von Facebook entwickelter leistungsstarker eingebetteter Key-Value-Store; wird häufig als Flink State-Backend verwendet.

**Verwandte Begriffe**: State Backend, Incremental Checkpoint, ForSt

---

## S

### Savepoint (Speicherpunkt)

**Definition**: Ein manuell ausgelöster konsistenter Snapshot einer Flink-Anwendung; verwendet für Upgrades und Migrationen.

**Verwandte Begriffe**: Checkpoint, State, Recovery

---

### Session Window (Sitzungsfenster)

**Definition**: Ein Fenstertyp, der Datensätze basierend auf Aktivitätszeiträumen gruppiert; schließt nach einer Lücke.

**Formalisierungsdefinition**:

```
Session(gap): Intervall zwischen aufeinanderfolgenden Ereignissen < gap
```

**Verwandte Begriffe**: Tumbling Window, Sliding Window, Global Window

---

### Side Output (Seitenausgabe)

**Definition**: Ein zusätzlicher Ausgabestrom zum Trennen von verspäteten Daten oder Ausnahmen vom Hauptausgabestrom.

**Verwandte Begriffe**: Late Data, Output Tag, Multi-Output

---

### Sink (Senke)

**Definition**: Der Endpunkt einer Stream-Verarbeitungspipeline; schreibt Daten in externe Systeme.

**Verwandte Begriffe**: Source, Connector, Exactly-Once

---

### Sliding Window (Gleitendes Fenster)

**Definition**: Ein Fenstertyp mit fester Größe, der in einem angegebenen Schiebeintervall bewegt wird; Fenster können sich überschneiden.

**Formalisierungsdefinition**:

```
Sliding(size, slide): [t - size, t) bei t = k × slide (k ∈ ℕ)
```

**Verwandte Begriffe**: Tumbling Window, Session Window, Global Window

---

### Source (Quelle)

**Definition**: Der Startpunkt einer Stream-Verarbeitungspipeline; liest Daten aus externen Systemen.

**Verwandte Begriffe**: Sink, Connector, Replayability

---

### State (Zustand)

**Definition**: Daten, die ein Stream-Processing-Operator zwischen Ereignissen beibehält; zwei Arten: Keyed State und Operator State.

**Verwandte Begriffe**: State Backend, Checkpoint, Stateful Processing

---

### State Backend (Zustands-Backend)

**Definition**: Ein Speichermechanismus, der bestimmt, wie Zustände während des Checkpoints gespeichert und wiederhergestellt werden.

**Implementierungen**: MemoryStateBackend, FsStateBackend, RocksDBStateBackend

**Verwandte Begriffe**: State, Checkpoint, Incremental Checkpoint

---

### Stream Processing (Stromverarbeitung)

**Definition**: Ein Berechnungsmodell zur Echtzeit-Verarbeitung kontinuierlicher und unendlicher Datenströme.

**Merkmale**:

- Eingabedaten sind unendlich (Unbounded)
- Niedrige Latenzverarbeitung
- Kontinuierliche Berechnung

**Verwandte Begriffe**: Batch Processing, Event Streaming, Real-time Processing

---

### Streaming Database (Stream-Datenbank)

**Definition**: Ein Datenbanksystem, das SQL-Abfragen auf kontinuierlich ankommenden Datenströmen ausführt und Ergebnisse in Echtzeit aktualisiert.

**Beispiele**: Materialize, RisingWave, Timeplus

**Verwandte Begriffe**: Materialized View, Continuous Query, Stream Processing

---

### Strong Consistency (Starke Konsistenz)

**Definition**: Ein Konsistenzmodell, bei dem alle Operationen so erscheinen, als würden sie in einer global sichtbaren Totalordnung ausgeführt.

**Verwandte Begriffe**: Linearizability, Serializability, Causal Consistency

---

## T

### Task (Aufgabe)

**Definition**: Die grundlegende Einheit der parallelen Ausführung in Flink; eine parallele Instanz eines logischen Operators.

**Verwandte Begriffe**: Operator, Subtask, Execution Graph

---

### TaskManager

**Definition**: Flink-Cluster-Arbeitsknoten; führt Aufgaben aus und kommuniziert über das Netzwerk mit anderen TaskManagern.

**Verwandte Begriffe**: JobManager, Slot, ResourceManager

---

### Throughput (Durchsatz)

**Definition**: Die Datenmenge, die ein System pro Zeiteinheit verarbeiten kann.

**Verwandte Begriffe**: Latency, Performance, Scalability

---

### Tumbling Window (Tumbling-Fenster)

**Definition**: Ein Fenstertyp mit fester Größe, benachbart und nicht überlappend.

**Formalisierungsdefinition**:

```
Tumbling(size): [k × size, (k+1) × size) (k ∈ ℕ)
```

**Verwandte Begriffe**: Sliding Window, Session Window, Global Window

---

## U

### Unaligned Checkpoint (Nicht-ausgerichteter Checkpoint)

**Definition**: Ein Flink-Checkpoint-Mechanismus, der es Operatoren ermöglicht, Zustands-Snapshots auszulösen, bevor sie alle Barrieren empfangen haben; reduziert Checkpoint-Latenzen unter Backpressure.

**Verwandte Begriffe**: Aligned Checkpoint, Barrier, Backpressure

---

### Unbounded Stream (Unbegrenzter Strom)

**Definition**: Ein Datenstrom mit unendlicher Datenmenge; Datenabstraktion der Stromverarbeitung.

**Formalisierungsdefinition**:

```
Unbounded(S) ⟺ |S| = ∞
```

**Verwandte Begriffe**: Bounded Stream, Stream Processing

---

## W

### Watermark (Wasserzeichen)

**Definition**: Ein Metadatenereignis in der Event-Time-Stromverarbeitung, das den Fortschritt der Zeit anzeigt; markiert, dass alle Ereignisse vor einem bestimmten Zeitstempel angekommen sind.

**Formalisierungsdefinition**:

```
WM(t) = max{ t_e | Ereignis e ist angekommen } - allowed_lateness
```

**Verwandte Begriffe**: Event Time, Window, Late Data

---

### Window (Fenster)

**Definition**: Ein Mechanismus zur Aufteilung unendlicher Ströme in endliche "Buckets"; ermöglicht Aggregation und Analyse.

**Typen**: Tumbling Window, Sliding Window, Session Window, Global Window

**Verwandte Begriffe**: Windowed Aggregation, Event Time, Watermark

---

### Windowed Aggregation (Fenster-Aggregation)

**Definition**: Eine Operation, die Aggregationsfunktionen (SUM, COUNT, AVG usw.) auf alle Ereignisse in einem Fenster anwendet.

**Verwandte Begriffe**: Window, Aggregate Function, Event Time

---

---

> **Übersetzer-Hinweis**: Dieses Glossar deckt über 100 Kernbegriffe im Zusammenhang mit Stream-Computing und Flink ab. Es wurde unter Beibehaltung der technischen Genauigkeit des Originals und im Einklang mit dem deutschen technischen Dokumentationsstil übersetzt. Formalisierte Notationen, Theorem-Nummern und API-Namen sind identisch mit dem Original.
>
> Für das vollständige Glossar siehe die englische Version GLOSSARY.md.
>
> 📅 **Letztes Update**: 2026-04-11 | 📝 **Version**: v1.0 (Deutsche Version)
