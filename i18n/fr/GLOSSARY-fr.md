> **状态**: 🔮 前瞻内容 | **风险等级**: 高 | **最后更新**: 2026-04
>
> 此文档描述的内容处于早期规划阶段，可能与最终实现不符。请以 Apache Flink 官方发布为准。
>
# Glossaire AnalysisDataFlow

> **Version** : v1.1 | **Date de mise à jour** : 2026-04-04 | **Portée** : Projet entier
>
> **Notes de version** : Les marques [2.0], [2.4], [2.5], [3.0] après les termes indiquent qu'ils ont été introduits ou sont devenus des fonctionnalités fondamentales dans la version correspondante de Flink
>
> Ce document est la référence terminologique faisant autorité du projet AnalysisDataFlow, organisée par ordre alphabétique, couvrant les domaines de la théorie du stream computing, de la pratique d'ingénierie Flink et des technologies de pointe.

---

## Table des matières

- [Navigation du glossaire](#navigation-du-glossaire)
- [Index des catégories terminologiques](#index-des-catégories-terminologiques)
- [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [K](#k) · [L](#l) · [M](#m) · [P](#p) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [W](#w)

---

## Navigation du glossaire

| Catégorie | Nombre de termes | Domaines principaux |
|-----------|------------------|---------------------|
| [Termes fondamentaux](#1-termes-fondamentaux) | 35+ | Stream computing, traitement par lots, traitement temps réel |
| [Termes théoriques](#2-termes-théoriques) | 40+ | Calculs de processus, vérification formalisée, théorie des types |
| [Termes Flink](#3-termes-flink) | 50+ | Concepts fondamentaux, APIs, paramètres de configuration |
| [Termes d'ingénierie](#4-termes-dingénierie) | 30+ | Design patterns, architecture, opérations |
| [Termes de pointe](#5-termes-de-pointe) | 35+ | AI Agents, bases de données de flux, cloud-natif |

---

## Index des catégories terminologiques

### 1. Termes fondamentaux

- **Stream computing** : Dataflow, Event Time, Processing Time, Watermark, Window
- **Traitement par lots** : Batch Processing, Bounded Stream, Checkpoint
- **Traitement temps réel** : Real-time Processing, Latency, Throughput

### 2. Termes théoriques

- **Termes de calculs de processus** : CCS, CSP, π-Calculus, Actor Model, Session Types
- **Termes de vérification formalisée** : Bisimulation, Model Checking, TLA+, Iris
- **Termes de théorie des types** : FG/FGG, DOT, Path-Dependent Types

### 3. Termes Flink

- **Concepts fondamentaux** : JobManager, TaskManager, Operator, State Backend
- **Liés aux API** : DataStream API, Table API, SQL
- **Paramètres de configuration** : Parallelism, Checkpoint Interval, Watermark Strategy

### 4. Termes d'ingénierie

- **Termes de design patterns** : Windowed Aggregation, Async I/O, Side Output
- **Termes d'architecture** : Microservices, Event-Driven Architecture, Data Mesh
- **Termes d'opérations** : Backpressure, Monitoring, Autoscaling

### 5. Termes de pointe

- **Termes AI Agent** : AI Agent, ReAct, MCP, A2A, Agentic Workflow, FLIP-531
- **Termes Serverless** : Serverless Flink, Scale-to-Zero, FaaS
- **Termes d'optimisation de performance** : Adaptive Execution Engine, Smart Checkpointing
- **Termes de bases de données de flux** : Materialized View, Continuous Query, Incremental Update
- **Termes cloud-natifs** : Kubernetes, Serverless, WASM, Lakehouse

---

## A

### Adaptive Execution Engine (Moteur d'exécution adaptatif) [Flink 1.17+]

**Définition** : Cadre d'optimisation d'exécution intelligent introduit par Flink, capable d'ajuster dynamiquement le plan d'exécution, l'allocation de ressources et le parallélisme basé sur les statistiques d'exécution.

**Définition formalisée** :

```
AEE-V2 = (𝒫, ℳ, 𝒜, 𝒞, ℛ, δ, π)
```

où 𝒫 est le plan d'exécution physique, ℳ les métriques d'exécution, 𝒜 les actions adaptatives, 𝒞 les contraintes, ℛ le re-optimiseur, δ la fonction de décision et π le modèle de prédiction de performance.

**Capacités fondamentales** : Traitement automatique du skew de données, ajustement dynamique du parallélisme, allocation de ressources adaptative

**Termes connexes** : Smart Checkpointing, Backpressure, Parallelism

---

### Actor Model (Modèle Actor)

**Définition** : Un modèle de calcul parallèle où l'unité fondamentale de calcul est l'Actor – une entité autonome capable de recevoir des messages, prendre des décisions, créer de nouveaux Actors et envoyer des messages.

**Définition formalisée** :

```
Actor ::= ⟨Mailbox, Behavior, State, Children, Supervisor⟩
```

**Termes connexes** : CSP (Communicating Sequential Processes), π-Calculus, passage de messages

---

### AI Agent (Agent d'intelligence artificielle) [Terme général]

**Définition** : Un système intelligent capable de percevoir, raisonner, agir et apprendre de manière autonome dans l'environnement, formalisé comme un 6-uplet :

```
𝒜_agent ≜ ⟨𝒮, 𝒫, 𝒟, 𝒜, ℳ, 𝒢⟩
```

où 𝒮 est l'espace d'état, 𝒫 la perception, 𝒟 la décision, 𝒜 l'action, ℳ la mémoire et 𝒢 l'objectif.

**Intégration Flink** : Flink Agent est une implémentation AI Agent basée sur le framework de stream computing

**Termes connexes** : ReAct, MCP, A2A, Multi-Agent, FLIP-531

---

### A2A Protocol (Protocole Agent-to-Agent) [Google 2025]

**Définition** : Standard d'interopérabilité ouvert d'Agent proposé par Google, supportant la délégation de tâches, la synchronisation d'état et le retour de résultats entre Agents.

**Définition formalisée** :

```
A2A_Flink = ⟨𝒫, ℳ, 𝒮, 𝒜⟩
```

où 𝒫 est l'ensemble des Agents participants, ℳ les types de messages, 𝒮 la machine à états de session et 𝒜 le mécanisme d'authentification-autorisation.

**Transition d'état de tâche** : `pending → working → input-required → completed/failed`

**Termes connexes** : AI Agent, MCP, Orchestration, FLIP-531

---

### Aligned Checkpoint (Checkpoint aligné)

**Définition** : Mécanisme dans Flink où l'opérateur ne déclenche le snapshot d'état qu'après avoir reçu la barrière de **tous** les canaux d'entrée.

**Définition formalisée** :

```
AlignedSnapshot(t, n) ⟺ ∀c ∈ Inputs(t): Barrier(n) ∈ Received(c)
```

**Termes connexes** : Unaligned Checkpoint, Barrier, Exactly-Once

---

### Async I/O (E/S asynchrone)

**Définition** : Un pattern permettant aux opérateurs de stream processing d'exécuter des appels à des systèmes externes de manière concurrente, évitant le blocage du traitement du flux de données.

**Définition formalisée** :

```
AsyncFunction: I × C → Future[O]
```

où C est le paramètre de concurrence, contrôlant le nombre de requêtes asynchrones simultanées.

**Termes connexes** : Backpressure, Enrichment, Concurrency

---

### At-Least-Once (Sémantique au moins une fois)

**Définition** : La sémantique d'un système de stream computing garantissant que l'impact de chaque donnée d'entrée sur le monde extérieur final se produit **au moins une fois**.

**Définition formalisée** :

```
∀r ∈ I. c(r, 𝒯) ≥ 1
```

où c(r, 𝒯) est le comptage d'influence de causalité.

**Termes connexes** : At-Most-Once, Exactly-Once, Delivery Guarantee

---

### At-Most-Once (Sémantique au plus une fois)

**Définition** : La sémantique d'un système de stream computing garantissant que l'impact de chaque donnée d'entrée sur le monde extérieur final se produit **au plus une fois**, avec perte de données possible.

**Définition formalisée** :

```
∀r ∈ I. c(r, 𝒯) ≤ 1
```

**Termes connexes** : At-Least-Once, Exactly-Once, Best-Effort

---

## B

### Backpressure (Contre-pression)

**Définition** : Un mécanisme dans les systèmes de stream processing où, lorsque la vitesse de traitement en aval est inférieure à celle en amont, des signaux de contrôle de débit sont transmis vers l'amont.

**Principe** : Contrôle de flux basé sur les crédits ; la transmission est suspendue lorsque le tampon de réception est plein.

**Termes connexes** : Flow Control, Buffer, Credit-Based

---

### Barrier (Barrière de checkpoint)

**Définition** : Un événement de contrôle spécial injecté dans le flux de données dans Flink, utilisé pour séparer les frontières de données entre différents checkpoints.

**Définition formalisée** :

```
Barrier(n) = ⟨Type = CONTROL, checkpointId = n, timestamp = ts⟩
```

**Termes connexes** : Checkpoint, Aligned Checkpoint, Unaligned Checkpoint

---

### Batch Processing (Traitement par lots)

**Définition** : Un modèle de calcul pour traiter des ensembles de données finis et bornés, où les données sont entièrement disponibles avant le début du calcul.

**Caractéristiques** :

- Données d'entrée bornées (Bounded)
- Accès à l'ensemble de données complet possible
- Latence non critique, recherche de haut débit

**Termes connexes** : Stream Processing, Bounded Stream, Lambda Architecture

---

### Best-Effort (Meilleur effort)

**Définition** : Une sémantique de livraison sans garantie de cohérence ; le système traite les données au mieux mais ne garantit ni la perte ni la duplication.

**Termes connexes** : At-Most-Once, Delivery Guarantee

---

### Bisimulation (Bisimulation)

**Définition** : Une relation en algèbre de processus pour déterminer l'équivalence comportementale de deux processus, exigeant que les deux processus puissent se simuler mutuellement sur toutes les actions possibles.

**Définition formalisée** :

```
R est une bisimulation ⟺ ∀(P,Q)∈R. ∀α. P→αP' ⇒ ∃Q'. Q→αQ' ∧ (P',Q')∈R
```

**Termes connexes** : Process Calculus, Trace Equivalence, CCS

---

### Bounded Stream (Flux borné)

**Définition** : Un flux de données avec une quantité de données finie ; abstraction de données du traitement par lots.

**Définition formalisée** :

```
Bounded(S) ⟺ |S| < ∞
```

**Termes connexes** : Unbounded Stream, Batch Processing

---

### Buffer (Tampon)

**Définition** : Une zone mémoire dans le stream processing pour le stockage temporaire de données, située entre le producteur et le consommateur.

**Termes connexes** : Backpressure, Queue, Network Buffer

---

## C

### CALM Theorem (Théorème CALM)

**Définition** : Consistency As Logical Monotonicity — les programmes logiquement monotones peuvent garantir la cohérence sans coordination.

**Expression formalisée** :

```
Programme P sans coordination ⟺ P est logiquement monotone
```

**Termes connexes** : Eventual Consistency, Coordination

---

### Causal Consistency (Cohérence causale)

**Définition** : Un modèle de cohérence dans les systèmes distribués qui préserve l'ordre des opérations ayant une relation de dépendance causale.

**Définition formalisée** :

```
∀op_i, op_j. op_i ≺hb op_j ⇒ op_i ≺obs op_j
```

**Termes connexes** : Strong Consistency, Eventual Consistency, Happens-Before

---

### CEP (Complex Event Processing, Traitement d'événements complexes)

**Définition** : Une technologie pour détecter des motifs complexes dans les flux d'événements et générer des événements composites.

**Définition formalisée** :

```
CEP: Stream × Pattern → DetectedEvents
```

**Termes connexes** : Pattern Matching, Event Pattern, Window

---

### CCS (Calculus of Communicating Systems)

**Définition** : Algèbre de processus basée sur la synchronisation étiquetée, proposée par Milner en 1980.

**Syntaxe** :

```
P, Q ::= 0 | α.P | P + Q | P | Q | P \ L | P[f]
```

**Termes connexes** : CSP, π-Calculus, Process Algebra

---

### CDC (Change Data Capture, Capture de données modifiées)

**Définition** : Une technologie pour capturer les événements de modification de base de données (insertion, mise à jour, suppression) et les propager en temps réel vers les systèmes en aval.

**Termes connexes** : Debezium, Streaming ETL, Log Mining

---

### Checkpoint (Point de contrôle)

**Définition** : Un snapshot d'état globalement cohérent d'un job de stream processing distribué à un moment donné, utilisé pour la récupération d'erreurs.

**Définition formalisée** :

```
CP = ⟨ID, TS, {S_i}_{i∈Tasks}, Metadata⟩
```

**Termes connexes** : Savepoint, State Backend, Recovery

---

### Chandy-Lamport Algorithm

**Définition** : Un algorithme classique dans les systèmes distribués pour capturer des snapshots globalement cohérents ; fondement théorique des checkpoints Flink.

**Termes connexes** : Global Snapshot, Consistent Cut, Checkpoint

---

### Choreographic Programming (Programmation chorégraphique)

**Définition** : Un paradigme de programmation distribuée décrivant les protocoles d'interaction entre plusieurs parties d'un point de vue global, puis projetés sur chaque participant.

**Termes connexes** : Session Types, Endpoint Projection, Deadlock Freedom

---

### Cloud-Native (Cloud-natif)

**Définition** : Une méthodologie pour construire et exécuter des applications en exploitant les avantages du cloud computing, mettant l'accent sur la conteneurisation, les microservices, la livraison continue et DevOps.

**Termes connexes** : Kubernetes, Containerization, Microservices

---

### Concurrency (Concurrence)

**Définition** : La capacité de plusieurs tâches de calcul à s'exécuter dans des intervalles de temps qui se chevauchent ; à distinguer du parallélisme (Parallelism).

**Termes connexes** : Parallelism, Race Condition, Synchronization

---

### Consistency Model (Modèle de cohérence)

**Définition** : Un ensemble de règles définissant la visibilité et l'ordre des opérations sur les données dans les systèmes distribués.

**Hiérarchie** : Strong Consistency → Causal Consistency → Eventual Consistency

**Termes connexes** : Linearizability, Serializability, CAP Theorem

---

### Continuous Query (Requête continue)

**Définition** : Une requête dans les bases de données de flux qui s'exécute en continu et met à jour les résultats automatiquement à l'arrivée des données.

**Définition formalisée** :

```
q: S → 𝒱, où q est une fonction variant dans le temps
```

**Termes connexes** : Materialized View, Streaming Database

---

### Credit-Based Flow Control (Contrôle de flux basé sur crédits)

**Définition** : Un mécanisme où le récepteur informe l'émetteur de la quantité de données qu'il peut recevoir en envoyant des valeurs de crédit.

**Termes connexes** : Backpressure, Flow Control

---

### CSP (Communicating Sequential Processes)

**Définition** : Algèbre de processus basée sur la communication synchrone et les noms d'événements statiques, proposée par Hoare en 1985.

**Syntaxe** :

```
P, Q ::= STOP | SKIP | a → P | P □ Q | P ⊓ Q | P ||| Q | P |[A]| Q
```

**Termes connexes** : CCS, π-Calculus, Go Channels

---

## D

### Dataflow Model (Modèle Dataflow)

**Définition** : Un modèle représentant les calculs comme un flux de données entre opérateurs ; fondement théorique central du stream computing.

**Définition formalisée** :

```
𝒢 = (V, E, P, Σ, 𝕋)
```

où V est l'ensemble des sommets, E l'ensemble des arêtes, P la fonction de traitement, Σ l'état et 𝕋 le modèle temporel.

**Termes connexes** : DAG, Operator, Stream Graph

---

### DAG (Directed Acyclic Graph, Graphe dirigé acyclique)

**Définition** : Une structure de graphe représentant la topologie de traitement de flux de données ; les nœuds sont des opérateurs, les arêtes sont des flux de données, sans cycles.

**Termes connexes** : Dataflow Model, Job Graph, Execution Graph

---

### Deadlock Freedom (Absence d'interblocage)

**Définition** : Une propriété garantissant qu'aucun processus n'est bloqué indéfiniment en attendant un événement qui ne se produira jamais.

**Termes connexes** : Liveness, Choreographic Programming, Session Types

---

### Delivery Guarantee (Garantie de livraison)

**Définition** : L'engagement d'un système de traitement de flux concernant la fiabilité de la transmission des messages ; divisé en At-Most-Once, At-Least-Once, Exactly-Once.

**Termes connexes** : At-Most-Once, At-Least-Once, Exactly-Once

---

### Determinism (Déterminisme)

**Définition** : La propriété qu'un système produit toujours la même sortie pour la même entrée.

**Définition formalisée** :

```
Deterministic(P) ⟺ ∀x. P(x) = P(x)
```

**Termes connexes** : Reproducibility, Consistency

---

### Distributed Snapshot (Snapshot distribué)

**Définition** : Un snapshot cohérent capturant l'état global d'un système distribué à un moment donné.

**Termes connexes** : Chandy-Lamport Algorithm, Checkpoint, Consistent Cut

---

## E

### Edge Computing (Calcul en périphérie)

**Définition** : Un paradigme de calcul effectuant le traitement de données près de la source de données (au bord du réseau), réduisant la latence et la consommation de bande passante.

**Termes connexes** : Cloud-Edge Continuum, IoT, Latency

---

### End-to-End Consistency (Cohérence de bout en bout)

**Définition** : La garantie de cohérence pour l'ensemble du pipeline de la source de données externe au puits de données externe.

**Définition formalisée** :

```
End-to-End-EO(J) ⟺ Replayable(Src) ∧ ConsistentCheckpoint(Ops) ∧ AtomicOutput(Snk)
```

**Termes connexes** : Internal Consistency, Exactly-Once, Source, Sink

---

### Event-Driven Architecture (Architecture pilotée par événements)

**Définition** : Un pattern d'architecture logicielle organisant l'interaction des composants autour de la production, de la détection et de la consommation d'événements.

**Termes connexes** : Event Streaming, Pub/Sub, CQRS

---

### Event Time (Temps d'événement)

**Définition** : L'horodatage à laquelle un enregistrement de données a été généré ; attribué par la source de données.

**Définition formalisée** :

```
t_e: Record → Timestamp
```

**Termes connexes** : Processing Time, Ingestion Time, Watermark

---

### Eventual Consistency (Cohérence éventuelle)

**Définition** : Un modèle de cohérence garantissant qu'en l'absence de nouvelles mises à jour, tous les réplicas finiront par converger vers la même valeur.

**Définition formalisée** :

```
◇□(réplicas convergent)
```

**Termes connexes** : Strong Consistency, Causal Consistency, CALM Theorem

---

### Exactly-Once (Sémantique exactement une fois)

**Définition** : La sémantique d'un système de stream computing garantissant que l'impact de chaque donnée d'entrée sur le monde extérieur final se produit **exactement une fois**.

**Définition formalisée** :

```
∀r ∈ I. c(r, 𝒯) = 1
```

**Termes connexes** : At-Least-Once, At-Most-Once, Idempotency

---

### Execution Graph (Graphe d'exécution)

**Définition** : Une structure de graphe dans Flink convertissant le JobGraph logique en plan d'exécution physique ; contient des instances parallèles concrètes.

**Termes connexes** : Job Graph, Task, Parallelism

---

## F

### Flink Agent [Flink 2.0+, FLIP-531]

**Définition** : Un agent intelligent autonome construit sur le framework de stream computing Flink ; supporte la perception, la décision et l'action continues.

**Définition formalisée** :

```
𝒜_Flink = ⟨𝒮_state, 𝒫_perception, 𝒟_decision, 𝒜_action, ℳ_memory, 𝒢_goal⟩
```

**Caractéristiques fondamentales** : Persistance d'état, Replayability, exécution distribuée, sémantique Exactly-Once

**Termes connexes** : AI Agent, FLIP-531, MCP, A2A, Stateful Stream Processing

---

### FLIP-531 (Flink AI Agents Proposal) [Flink 2.0+]

**Définition** : Proposition de fonctionnalité officielle d'Apache Flink introduisant le support natif d'exécution AI Agent et réalisant l'intégration profonde du stream computing et de l'intelligence AI.

**Composants fondamentaux** :

- **Flink Agent Runtime** : Environnement d'exécution Agent
- **Intégration MCP** : Support du Model Context Protocol
- **Protocole A2A** : Interopérabilité Agent-à-Agent
- **Agentic Workflow** : Orchestration de workflow intelligent Agent

**Définition formalisée** :

```
FLIP-531 = ⟨ℛ_agent, ℐ_mcp, 𝒫_a2a, 𝒲_workflow⟩
```

**Termes connexes** : Flink Agent, MCP, A2A, Agentic Workflow

---

### Flow Control (Contrôle de flux)

**Définition** : Un mécanisme pour réguler le taux de transfert de données entre producteur et consommateur de données.

**Termes connexes** : Backpressure, Credit-Based, Buffer

---

### Function as a Service (FaaS)

**Définition** : Un modèle de calcul sans serveur où les utilisateurs écrivent du code de fonction et la plateforme gère l'infrastructure et le scaling automatique.

**Termes connexes** : Serverless, Lambda, Cloud-Native

---

## G

### GPU Acceleration (Accélération GPU) [Flink 2.5+]

**Définition** : Utilisation des capacités de calcul massivement parallèles des GPUs pour exécuter des opérateurs de stream processing ; déchargement des opérations intensives en calcul du CPU vers le GPU via CUDA/OpenCL.

**Définition formalisée** :

```
𝒪_GPU(D) = GPUKernel(Transfer(D_CPU→GPU))
```

**Rapport d'accélération** : S_GPU = T_CPU / (T_transfer + T_kernel + T_sync)

**Conditions d'application** : Taille de lot n > n_threshold ET ratio calcul/transfert > γ

**Termes connexes** : CUDA, Vector Search, Flink-CUDA Runtime

---

### Global Snapshot (Snapshot global)

**Définition** : L'ensemble de tous les états de processus d'un système distribué à un moment donné ; utilisé pour la récupération d'erreurs et la vérification de cohérence.

**Termes connexes** : Distributed Snapshot, Chandy-Lamport Algorithm, Checkpoint

---

### Global Window (Fenêtre globale)

**Définition** : Une fenêtre unique contenant tous les enregistrements ; généralement utilisée avec un déclencheur personnalisé.

**Définition formalisée** :

```
Global: wid_global = (-∞, +∞)
```

**Termes connexes** : Tumbling Window, Sliding Window, Session Window

---

## H

### Happens-Before (Relation de précédence)

**Définition** : Une relation définissant l'ordre partiel causal entre événements ; fondement de la cohérence distribuée.

**Termes connexes** : Causal Consistency, Partial Order, Clock

---

## I

### Idempotency (Idempotence)

**Définition** : La propriété qu'une opération n'affecte pas l'état du système au-delà de la première application, même si elle est appliquée plusieurs fois.

**Définition formalisée** :

```
f(x) = f(f(x))
```

**Termes connexes** : Exactly-Once, At-Least-Once, Fault Tolerance

---

### Incremental Checkpoint (Checkpoint incrémental)

**Définition** : Un mécanisme de checkpoint ne sauvegardant que l'état modifié depuis le dernier checkpoint.

**Termes connexes** : Checkpoint, State Backend, RocksDB

---

### Ingestion Time (Temps d'ingestion)

**Définition** : L'horodatage à laquelle un enregistrement de données est ingéré dans le système de traitement de flux.

**Termes connexes** : Event Time, Processing Time, Watermark

---

## K

### Keyed State (État clé)

**Définition** : État partitionné par clé ; les enregistrements avec la même clé accèdent à la même instance d'état.

**Termes connexes** : Operator State, State Backend, KeyedStream

---

### Kafka

**Définition** : Une plateforme de streaming distribuée à haut débit ; fournit la messagerie publish/subscribe et le stream processing.

**Termes connexes** : CDC, Streaming ETL, Event Streaming

---

### Kubernetes

**Définition** : Une plateforme d'orchestration de conteneurs open-source pour la gestion des charges de travail et des services conteneurisés.

**Termes connexes** : Cloud-Native, Container, Orchestration

---

## L

### Latency (Latence)

**Définition** : Le temps entre l'occurrence d'un événement et la disponibilité de son résultat de traitement.

**Termes connexes** : Throughput, Event Time, Processing Time

---

### Liveness (Vivacité)

**Définition** : Une propriété de sûreté garantissant que le système effectuera finalement l'action requise.

**Termes connexes** : Safety, Deadlock Freedom, Fairness

---

## M

### Materialized View (Vue matérialisée)

**Définition** : Un objet de base de données stockant les résultats de requête pré-calculés ; dans les bases de données de flux, mis à jour en continu.

**Termes connexes** : Continuous Query, Streaming Database, Incremental View Maintenance

---

### MCP (Model Context Protocol) [Anthropic 2024]

**Définition** : Protocole standard proposé par Anthropic fournissant une interface unifiée pour que les AI Agents communiquent avec des outils externes et des sources de données.

**Termes connexes** : AI Agent, A2A, Tool Calling, Flink Agent

---

### Microservices (Microservices)

**Définition** : Un style d'architecture structurant une application comme un ensemble de petits services ; chaque service s'exécute dans son propre processus et communique via des mécanismes légers.

**Termes connexes** : Service Mesh, Container, Cloud-Native

---

## P

### Parallelism (Parallélisme)

**Définition** : Le nombre d'instances exécutant une tâche en parallèle.

**Termes connexes** : Concurrency, Task, Slot

---

### Pattern Matching (Correspondance de motifs)

**Définition** : Le processus de mise en correspondance de séquences d'événements contre des motifs définis en CEP.

**Termes connexes** : CEP, Event Pattern, Window

---

### Processing Time (Temps de traitement)

**Définition** : Le temps local de la machine au moment où un enregistrement de données est traité par un opérateur.

**Termes connexes** : Event Time, Ingestion Time, Watermark

---

### π-Calculus (π-calcul)

**Définition** : Algèbre de processus mobiles proposée par Milner ; supporte la création dynamique de canaux et le passage de noms.

**Définition formalisée** :

```
P, Q ::= 0 | α.P | P + Q | P | Q | (νa)P | !P
```

**Termes connexes** : CCS, CSP, Mobile Processes

---

## R

### Race Condition (Condition de concurrence)

**Définition** : Une situation où plusieurs processus accèdent à des ressources partagées et le résultat dépend du timing.

**Termes connexes** : Concurrency, Synchronization, Mutual Exclusion

---

### Replayability (Rejouabilité)

**Définition** : La capacité d'une source à renvoyer des données précédentes ; essentielle pour la sémantique Exactly-Once.

**Termes connexes** : Exactly-Once, Source, Checkpoint

---

### RocksDB

**Définition** : Magasin clé-valeur embarqué haute performance développé par Facebook ; largement utilisé comme backend d'état de Flink.

**Termes connexes** : State Backend, Incremental Checkpoint, ForSt

---

## S

### Savepoint (Point de sauvegarde)

**Définition** : Un snapshot cohérent d'une application Flink déclenché manuellement ; utilisé pour les mises à niveau et les migrations.

**Termes connexes** : Checkpoint, State, Recovery

---

### Session Window (Fenêtre de session)

**Définition** : Un type de fenêtre groupant les enregistrements basé sur des périodes d'activité ; se ferme après une période d'inactivité.

**Définition formalisée** :

```
Session(gap): Intervalle entre événements consécutifs < gap
```

**Termes connexes** : Tumbling Window, Sliding Window, Global Window

---

### Side Output (Sortie latérale)

**Définition** : Un flux de sortie supplémentaire pour séparer les données en retard ou les exceptions du flux de sortie principal.

**Termes connexes** : Late Data, Output Tag, Multi-Output

---

### Sink (Puits)

**Définition** : Le point final d'un pipeline de traitement de flux ; écrit les données dans des systèmes externes.

**Termes connexes** : Source, Connector, Exactly-Once

---

### Sliding Window (Fenêtre glissante)

**Définition** : Un type de fenêtre de taille fixe se déplaçant à un intervalle de glissement spécifié ; les fenêtres peuvent se chevaucher.

**Définition formalisée** :

```
Sliding(size, slide): [t - size, t) où t = k × slide (k ∈ ℕ)
```

**Termes connexes** : Tumbling Window, Session Window, Global Window

---

### Source (Source)

**Définition** : Le point de départ d'un pipeline de traitement de flux ; lit les données à partir de systèmes externes.

**Termes connexes** : Sink, Connector, Replayability

---

### State (État)

**Définition** : Données qu'un opérateur de stream processing maintient entre les événements ; deux types : Keyed State et Operator State.

**Termes connexes** : State Backend, Checkpoint, Stateful Processing

---

### State Backend (Backend d'état)

**Définition** : Un mécanisme de stockage déterminant comment les états sont sauvegardés et restaurés pendant le checkpoint.

**Implémentations** : MemoryStateBackend, FsStateBackend, RocksDBStateBackend

**Termes connexes** : State, Checkpoint, Incremental Checkpoint

---

### Stream Processing (Traitement de flux)

**Définition** : Un modèle de calcul traitant des flux de données continus et infinis en temps réel.

**Caractéristiques** :

- Données d'entrée infinies (Unbounded)
- Traitement à faible latence
- Calcul continu

**Termes connexes** : Batch Processing, Event Streaming, Real-time Processing

---

### Streaming Database (Base de données de flux)

**Définition** : Un système de base de données exécutant des requêtes SQL sur des flux de données arrivant en continu et mettant à jour les résultats en temps réel.

**Exemples** : Materialize, RisingWave, Timeplus

**Termes connexes** : Materialized View, Continuous Query, Stream Processing

---

### Strong Consistency (Cohérence forte)

**Définition** : Un modèle de cohérence où toutes les opérations apparaissent comme exécutées dans un ordre total globalement visible.

**Termes connexes** : Linearizability, Serializability, Causal Consistency

---

## T

### Task (Tâche)

**Définition** : L'unité fondamentale d'exécution parallèle dans Flink ; une instance parallèle d'un opérateur logique.

**Termes connexes** : Operator, Subtask, Execution Graph

---

### TaskManager

**Définition** : Nœud worker du cluster Flink ; exécute des tâches et communique avec d'autres TaskManagers via le réseau.

**Termes connexes** : JobManager, Slot, ResourceManager

---

### Throughput (Débit)

**Définition** : La quantité de données qu'un système peut traiter par unité de temps.

**Termes connexes** : Latency, Performance, Scalability

---

### Tumbling Window (Fenêtre basculante)

**Définition** : Un type de fenêtre de taille fixe, adjacentes, sans chevauchement.

**Définition formalisée** :

```
Tumbling(size): [k × size, (k+1) × size) (k ∈ ℕ)
```

**Termes connexes** : Sliding Window, Session Window, Global Window

---

## U

### Unaligned Checkpoint (Checkpoint non aligné)

**Définition** : Un mécanisme de checkpoint Flink permettant aux opérateurs de déclencher des snapshots d'état avant de recevoir toutes les barrières ; réduit les latences de checkpoint sous backpressure.

**Termes connexes** : Aligned Checkpoint, Barrier, Backpressure

---

### Unbounded Stream (Flux non borné)

**Définition** : Un flux de données avec une quantité de données infinie ; abstraction de données du traitement de flux.

**Définition formalisée** :

```
Unbounded(S) ⟺ |S| = ∞
```

**Termes connexes** : Bounded Stream, Stream Processing

---

## W

### Watermark (Filigrane)

**Définition** : Un événement de métadonnées dans le stream processing basé sur le temps d'événement indiquant la progression du temps ; marque que tous les événements avant un certain horodatage sont arrivés.

**Définition formalisée** :

```
WM(t) = max{ t_e | événement e est arrivé } - allowed_lateness
```

**Termes connexes** : Event Time, Window, Late Data

---

### Window (Fenêtre)

**Définition** : Un mécanisme divisant les flux infinis en "buckets" finis ; permet l'agrégation et l'analyse.

**Types** : Tumbling Window, Sliding Window, Session Window, Global Window

**Termes connexes** : Windowed Aggregation, Event Time, Watermark

---

### Windowed Aggregation (Agrégation par fenêtre)

**Définition** : Une opération appliquant des fonctions d'agrégation (SUM, COUNT, AVG, etc.) à tous les événements dans une fenêtre.

**Termes connexes** : Window, Aggregate Function, Event Time

---

---

> **Note du traducteur** : Ce glossaire couvre plus de 100 termes fondamentaux liés au stream computing et à Flink. Il a été traduit en conservant l'exactitude technique de l'original et selon le style des documents techniques français. Les notations formalisées, les numéros de théorèmes et les noms d'API sont identiques à l'original.
>
> Pour le glossaire complet, voir la version anglaise GLOSSARY.md.
>
> 📅 **Dernière mise à jour** : 2026-04-11 | 📝 **Version** : v1.0 (Version française)
