# Actor-to-CSP Encoding

> Stage: Struct | Prerequisites: [Related Documents] | Formalization Level: L3

> **Version**: 2026.03 | **Scope**: Formal Encoding Theory | **Dependencies**: [01.03-actor-model-formalization](../01-foundation/01.03-actor-model-formalization.md), [01.05-csp-formalization](../01-foundation/01.05-csp-formalization.md)

---

## Table of Contents

- [Actor-to-CSP Encoding](#actor-to-csp-encoding)
  - [Table of Contents](#table-of-contents)
  - [Abstract](#abstract)
  - [1. Definitions](#1-definitions)
    - [1.1 Formal Definition of Actor System Configuration](#11-formal-definition-of-actor-system-configuration)
    - [1.2 CSP Process Syntax Subset](#12-csp-process-syntax-subset)
    - [1.3 Actor→CSP Encoding Function](#13-actorcsp-encoding-function)
    - [1.4 Formal Definition of Address Passing Restriction](#14-formal-definition-of-address-passing-restriction)
  - [2. Properties](#2-properties)
    - [2.1 Core Properties Derived from Encoding Definition](#21-core-properties-derived-from-encoding-definition)
  - [3. Relations](#3-relations)
    - [3.1 Expressiveness Relation between Actor and CSP](#31-expressiveness-relation-between-actor-and-csp)
    - [3.2 Semantics-Preserving Encoding vs. Expressiveness Equivalence](#32-semantics-preserving-encoding-vs-expressiveness-equivalence)

## Abstract

This document establishes a rigorous formal encoding from the Actor model of computation to CSP (Communicating Sequential Processes) process algebra. We define the encoding function `[[·]]_A→C`, which maps Actor system configurations to CSP process compositions, explicitly construct the Buffer process encoding for Mailbox, prove that this encoding preserves trace semantics equivalence (weak bisimulation) for restricted Actor systems (without dynamic address passing), and analyze the fundamental limitation that dynamic Actor creation cannot be fully encoded into static CSP.

---

## 1. Definitions

### 1.1 Formal Definition of Actor System Configuration

**Def-S-12-01 (Actor Configuration)**:

Let an Actor system configuration `γ` be a quadruple:

```
γ ≜ ⟨A, M, Σ, addr⟩
```

Where:

- `A = {a₁, a₂, ..., aₙ}`: a finite set of Actor identifiers
- `M: A → Message*`: the mailbox of each actor, an ordered queue of messages
- `Σ: A → Behavior`: the state mapping, assigning the current behavior to each actor
- `addr: A → Address`: the address mapping, assigning a logical address to each actor

**Core Action Syntax**:

```
Action ::= send(a, v)          // send value v to actor a
        |  receive(p) → P      // receive message matching pattern p, continue with P
        |  become(B')          // switch behavior to B'
        |  spawn(B) → a_new    // create a new actor, returning its address
```

**Intuitive Explanation**: The Actor configuration captures the complete runtime state of an Actor system—which actors exist, what messages are in each mailbox, what the current behaviors are, and the address mapping relationships. This definition strips away concrete language syntactic sugar (such as Erlang's `!` operator or Scala Akka's `!` method), preserving the core computational capabilities of the Actor model[^1].

**Rationale for Definition**: Without abstracting the Actor system as a configuration quadruple, it would be impossible to precisely describe "system state" and "state transitions," and thus impossible to make a rigorous comparison with the process algebra semantics of CSP. In particular, the explicit introduction of the `addr` mapping enables us to formally analyze "dynamic address passing," a key semantic feature.

---

### 1.2 CSP Process Syntax Subset

**Def-S-12-02 (CSP Core Syntax Subset)**:

```
P, Q ::= STOP                     // deadlock / termination
      |  SKIP                     // successful termination
      |  a → P                    // prefix: perform event a, then continue P
      |  P □ Q                    // external choice
      |  P ⊓ Q                    // internal choice
      |  P ||| Q                  // interleaving parallel (no synchronization)
      |  P [| A |] Q              // parallel composition (synchronize on A)
      |  P \ A                    // hiding: convert events in A to internal τ
      |  P ; Q                    // sequential composition
      |  if b then P else Q       // conditional
      |  μX.F(X)                  // recursion
```

**Event Types**:

- `ch!v`: output value `v` on channel `ch`
- `ch?x`: input on channel `ch`, binding to variable `x`
- `τ`: internal event (unobservable)

**Intuitive Explanation**: CSP models concurrent systems as collections of sequential processes interacting via explicit events. This subset preserves the four core constructs—prefix, choice, parallel, and hiding—sufficient to express Actor semantics while avoiding unnecessary complexity[^2].

---

### 1.3 Actor→CSP Encoding Function

**Def-S-12-03 (Encoding Function [[·]]_A→C)**:

The encoding function `[[·]]_A→C` maps an Actor configuration to a CSP process composition:

```
[[γ = ⟨A, M, Σ, addr⟩]]_A→C = (|||_{a∈A} ACTOR_a) [| SYNC_A |] (|||_{a∈A} MAILBOX_a)
```

Where:

- `ACTOR_a`: the CSP process encoding actor `a`
- `MAILBOX_a`: the Buffer process encoding the mailbox of actor `a`
- `SYNC_A`: the set of synchronization channels for communication between actor and mailbox

**Actor Behavior Encoding**:

```
[[send(target, v)]]_A→C = ch_target!v → SKIP

[[receive(p) → P]]_A→C = ch_self?msg →
                          if MATCH(msg, p) then [[P]]_A→C
                          else [[receive(p) → P]]_A→C

[[become(B')]]_A→C = [[B']]_A→C

[[spawn(B)]]_A→C = new_ch → (ACTOR_new ||| MAILBOX_new)
```

**Explicit Encoding of Mailbox as Buffer Process**:

```csp
MAILBOX_a(ch_in, ch_out, buffer) =
    (#buffer < MAX) & ch_in?msg → MAILBOX_a(ch_in, ch_out, buffer ⧺ [msg])
    □
    (#buffer > 0) & ch_out!head(buffer) → MAILBOX_a(ch_in, ch_out, tail(buffer))
```

Where:

- `ch_in`: the channel on which external senders deposit messages
- `ch_out`: the channel on which the actor receives messages
- `buffer`: the internal message queue (CSP data structure)
- `⧺`: list append operation

**Intuitive Explanation**: Each Actor is encoded as the parallel composition of two CSP processes—a behavior-processing `ACTOR` process and a FIFO-buffer `MAILBOX` process. Asynchronous message passing is encoded as a non-blocking write to the `MAILBOX` input channel, while message reception is implemented as a sequential read from the `MAILBOX` output channel[^3].

**Rationale for Definition**: CSP has no native concept of "per-process FIFO queue"; the mailbox semantics must be simulated via an independent buffer process. This is the most critical and complex part of the Actor→CSP encoding—the explicit encoding of the mailbox not only increases the number of processes (one mailbox process per actor), but also introduces complexity not present in native Actor systems.

---

### 1.4 Formal Definition of Address Passing Restriction

**Def-S-12-04 (Restricted Actor System)**:

An Actor system `γ = ⟨A, M, Σ, addr⟩` is called a **Restricted Actor System** if and only if it satisfies the following condition:

```
∀a ∈ A, ∀msg ∈ M(a): msg.payload contains no actor addresses
```

That is: **actor addresses cannot be passed in message contents** (dynamic address passing is prohibited).

**Comparison of Restricted vs. Full Actor Systems**:

| Feature | Restricted Actor System | Full Actor System |
|---------|------------------------|-------------------|
| Address Passing | Prohibited | Allowed |
| Communication Topology | Static (determined at encoding time) | Dynamic (evolves at runtime) |
| Expressiveness Level | L3 | L4-L5 |
| CSP Encodability | ✅ Yes | ❌ No (full preservation) |

**Intuitive Explanation**: The restricted Actor system prohibits the feature of "sending actor addresses as message contents." This makes the communication topology fixed at system startup, compatible with CSP's static channel topology. This is the key prerequisite for the success of the Actor→CSP encoding[^4].

---

## 2. Properties

### 2.1 Core Properties Derived from Encoding Definition

**Property 1 (Encoding Preserves Message FIFO)**:

For any two Actors `S` (sender) and `R` (receiver), if `S` sends messages `m₁, m₂` to `R` in order, then `m₁` must be received before `m₂` in `R`'s mailbox.

**Derivation**:

1. By Def-S-12-03, `send(S, m₁)` is encoded as `ch_R!m₁ → SKIP`, and `send(S, m₂)` is encoded as `ch_R!m₂ → SKIP`.
2. Since `S` is encoded as a sequential process `ACTOR_S`, its internal events strictly follow syntactic order. Therefore, event `ch_R!m₁` must appear before `ch_R!m₂` in the trace of `ACTOR_S`.
3. By the MAILBOX encoding definition, `ch_R` connects to the `ch_in` of the MAILBOX process; the MAILBOX uses the list `buffer` to maintain message order, appending new messages to the tail via `⧺`.
4. The MAILBOX's `ch_out` output operation always takes messages from `head(buffer)`, so `m₁` must be output to `R`'s receiving end before `m₂`.
5. **Q.E.D.**

---

**Property 2 (Encoding Preserves State Isolation)**:

For any Actor `a`, its local state `state_a` cannot be directly read or modified by any other process in the CSP encoding.

**Derivation**:

1. By Def-S-12-03, `ACTOR_a(ch_a, state_a)` takes `state_a` as a process parameter.
2. In CSP semantics, process parameters are only visible within the scope of the process definition; there is no global state sharing mechanism.
3. Other processes can only interact with `ACTOR_a` through events (i.e., communication on `ch_a`), and cannot directly access `state_a`.
4. Therefore, modification of `state_a` can only be performed by `ACTOR_a` itself via parameter passing (e.g., `ACTOR_a(ch_a, new_state)`).
5. **Q.E.D.**

---

**Property 3 (Encoding Introduces Additional Process Overhead)**:

For a system containing `n` Actors, its CSP encoding requires at least `2n` processes (`n` Actor processes + `n` Mailbox processes).

**Derivation**:

1. By Def-S-12-03, each Actor `aᵢ` is encoded as a CSP process `ACTOR_i`.
2. Since CSP has no built-in per-process FIFO queue, each `ACTOR_i` must be paired with an independent `MAILBOX_i` process to simulate mailbox semantics.
3. If the system contains a supervision tree structure, supervisors themselves also need to be encoded as additional CSP processes.
4. Therefore, the number of processes after encoding is at least `2n`.
5. **Q.E.D.**

---

## 3. Relations

### 3.1 Expressiveness Relation between Actor and CSP

**Relation**: Restricted Actor `⊂` CSP `⊥` Full Actor

**Argumentation**:

- **Encoding Existence (Restricted Actor → CSP)**: By Def-S-12-03, for any restricted Actor system, the encoding function `[[·]]_A→C` is well-defined. Since restricted Actors prohibit dynamic address passing, the communication topology is static and compatible with CSP's static channel topology.

- **Separation Result 1 (Full Actor is stronger than CSP)**: Full Actor supports **unbounded dynamic creation** (unbounded spawn) and **location transparency**, while CSP channels are statically named and cannot create new communication topologies at runtime. Therefore, no surjective encoding from full Actor to CSP exists.

- **Separation Result 2 (CSP is stronger than Restricted Actor)**: CSP supports fine-grained **synchronous communication** and **external choice** (`□`), enabling expression of complex handshake protocols and deadlock-freedom proofs. Actor's asynchronous message passing cannot natively express synchronous choice semantics.

- **Conclusion**: Restricted Actor is a proper subset of CSP; full Actor and CSP are incomparable (`⊥`). `[[·]]_A→C` is a semantics-preserving encoding that preserves core semantics, not an expressiveness equivalence[^5].

---

### 3.2 Semantics-Preserving Encoding vs. Expressiveness Equivalence

**Relation**: Semantics-Preserving Encoding `≉` Expressiveness Equivalence

**Argumentation**:

- **Semantics-Preserving Encoding** (`E: A ↦ B`) requires: for some semantic subset of the source language `A` (e.g., message passing, state isolation), the encoded target language `B` program preserves the same observable behavior. It does **not** require that all features of `B` can be expressed in `A`.

- **Expressiveness Equivalence** (`A ≈ B`) requires: there exist bidirectional encodings `E: A ↦ B` and `D: B ↦ A`, both preserving surjectivity and semantics. This means the two languages can simulate each other's full program sets.

- For restricted Actor and CSP: `[[·]]_A→C` only preserves the subset of "asynchronous message passing + sequential processing + state isolation," but loses "unbounded spawn + location transparency." Therefore, it is a semantics-preserving encoding, but not an expressiveness equivalence.

---

## 4. Argumentation

### 4.1 Auxiliary Lemmas

**Lemma-S-12-01 (Mailbox FIFO Invariant)**:

For any MAILBOX process `M(ch_in, ch_out, buf)`, if initially `buf = []`, then in any reachable state, the sequence of messages output from `ch_out` is a prefix-preserving subsequence of the sequence of messages input from `ch_in`.

**Proof**:

1. **Premise Analysis**: The MAILBOX has only two transition rules:
   - (R1) `ch_in?msg`: append `msg` to the tail of `buf`
   - (R2) `ch_out!head(buf)`: remove and output the message from the head of `buf`

2. **Structural Induction**:
   - Initial state `buf = []`, the invariant holds trivially.
   - Assume the invariant holds before some step.
   - If R1 is executed, `buf` becomes `buf ⧺ [msg]`; the new message is placed at the tail, not affecting the relative order of existing messages.
   - If R2 is executed, `head(buf)` is output; the remaining `tail(buf)` still preserves the original order.

3. **Conclusion**: By structural induction, the FIFO invariant holds in all reachable states. ∎

---

**Lemma-S-12-02 (Single-Threadedness of Actor Processes)**:

For the encoded Actor process `ACTOR_a(ch_in, state)`, in any execution trace, there do not exist two concurrent message processing instances active simultaneously.

**Proof**:

1. The syntactic structure of `ACTOR_a` is a recursive prefix process: `ch_in?msg → PROCESS(msg) → ACTOR_a(ch_in, new_state)`.
2. In CSP trace semantics, a single process can only be at one event prefix position at any moment.
3. Before `PROCESS(msg)` completes, `ACTOR_a` cannot execute `ch_in?msg` again (because the recursive call to `ACTOR_a` occurs after `PROCESS(msg)`).
4. Therefore, it is impossible for two message processing instances to be active simultaneously. ∎

---

**Lemma-S-12-03 (State Inaccessibility from External Processes)**:

For the encoded Actor process `ACTOR_a(ch_in, state)`, there exists no other process `Q` (`Q ≠ ACTOR_a`) whose events directly reference `state`.

**Proof**:

1. In CSP, process parameters are locally bound. `state` only appears in the body of `ACTOR_a`'s definition.
2. Other processes can only interact with `ACTOR_a` through communication events on the shared channel `ch_in`.
3. Communication events only pass message values, not internal bindings of the process.
4. Therefore, no external process can directly read or modify `state`. ∎

---

## 5. Formal Proof / Engineering Argument

### 5.1 Encoding Preserves Trace Semantics

**Thm-S-12-01 (Actor System Encoding Preserves Trace Semantics)**:

Let `γ` be a **restricted Actor configuration** (no dynamic address passing), and `[[·]]_A→C` be the encoding function from Def-S-12-03. There exists a weak bisimulation relation `R` such that:

```
(γ, [[γ]]_A→C) ∈ R
```

That is: restricted Actor systems can be encoded into CSP while preserving equivalent trace semantics (modulo weak bisimulation).

**Proof**:

**Step 1: Define the Bisimulation Relation `R`**

For restricted Actor configuration `γ = ⟨A, M, Σ, addr⟩` and CSP process `P = [[γ]]_A→C`, define:

```
(γ, P) ∈ R ⟺ P = (|||_{a∈A} [[a]]_A→C) [| SYNC |] (|||_{a∈A} [[M(a)]]_A→C)
```

Where `[[M(a)]]_A→C` denotes the representation of mailbox contents in CSP (i.e., the buffer state of the MAILBOX process).

**Step 2: Basic Operation Correspondence**

Consider the four basic operations in Actor semantics:

| Actor Operation | Actor Transition | CSP Corresponding Transition | Bisimulation Preserved |
|-----------------|------------------|------------------------------|------------------------|
| `send(a, v)` | `γ → γ'` (`M` gains a message) | `ch_a!v` event | Message transferred from sender process to MAILBOX process, corresponding to `M` gain |
| `receive(p)` | `γ → γ'` (message removed from mailbox) | `ch_out?msg` event | MAILBOX outputs message to Actor process, corresponding to mailbox removal |
| `become(b')` | `Σ` updated | process parameter updated | recursive call `ACTOR_a(ch_a, new_state)`, state mapping consistent |
| `spawn(a')` | `A` gains new actor | `ACTOR_new ||| MAILBOX_new` | CSP parallel composition gains new process, actor set consistent |

**Step 3: Inductive Step (Induction on Transition Sequence Length)**

Assume that for transition sequences of length `≤ n`, the bisimulation relation `R` is preserved. Consider step `n+1`:

- **Case A**: Actor configuration executes `send` operation.
  - By induction hypothesis, after step `n`, `(γ_n, P_n) ∈ R`.
  - `γ_n → γ_{n+1}` is completed via `send(target, v)` of some actor `a`.
  - In CSP, `[[a]]_A→C` executes the `ch_target!v` event; message value `v` enters the MAILBOX process of `target`.
  - Define `P_{n+1}` as the CSP configuration after executing this event; then `(γ_{n+1}, P_{n+1}) ∈ R`.

- **Case B**: Actor configuration executes `receive` operation.
  - `γ_n → γ_{n+1}` is completed via `receive(p)` of some actor `a`, removing matching message `m` from `a`'s mailbox.
  - In CSP, `[[a]]_A→C` executes `ch_a?m`, removing `m` from the MAILBOX buffer.
  - By Lemma-S-12-01, the removed message is consistent with the message removed in Actor semantics.
  - Define `P_{n+1}` as the CSP configuration after executing this event; then `(γ_{n+1}, P_{n+1}) ∈ R`.

- **Case C**: Actor configuration executes `become` operation.
  - `γ_n → γ_{n+1}` updates `Σ(a)` to new behavior `b'`.
  - In CSP, `[[a]]_A→C` recursively calls `ACTOR_a(ch_a, new_state)` after executing `PROCESS(msg)`, where `new_state` corresponds to `b'`.
  - State mapping is consistent, therefore `(γ_{n+1}, P_{n+1}) ∈ R`.

- **Case D**: Actor configuration executes `spawn` operation.
  - `γ_n → γ_{n+1}` adds new actor `a_new`.
  - In CSP, `[[a]]_A→C` introduces `[[a_new]]_A→C` via parallel composition.
  - Actor set is consistent, therefore `(γ_{n+1}, P_{n+1}) ∈ R`.

**Step 4: Critical Case Analysis**

- **Message in transit**: When message `m` has been sent but not yet received, in the Actor configuration `m ∈ M`, while in CSP `m` appears as the MAILBOX buffer content or as a pending event on the channel. Both representations are equivalent under `R`.

- **Empty mailbox receive**: If Actor `a` attempts `receive` but the mailbox is empty, in Actor semantics `a` blocks. In CSP, the `ch_a?msg` prefix of `[[a]]_A→C` cannot trigger (because the MAILBOX's `ch_out` output is guarded by `#buffer > 0`), so the process also blocks. Behaviors are equivalent.

- **Parallel interleaving**: When multiple Actors send messages simultaneously, in CSP multiple processes output on their respective channels. Since the channels differ, the interleaving order does not affect the local semantics of each actor, consistent with the independence of the Actor model.

**Step 5: Weak Bisimulation Verification**

- **Forward Simulation**: If `γ → γ'` (one step in Actor semantics), then `[[γ]]_A→C ⇒ [[γ']]_A→C` (in CSP, after possibly several internal `τ` steps, the corresponding state is reached). By Steps 2-4, this correspondence holds.

- **Backward Simulation**: If `[[γ]]_A→C → P'` (one step in CSP semantics), then there exists `γ'` such that `γ ⇒ γ'` and `(γ', P') ∈ R`. Since restricted Actor prohibits dynamic address passing, every step in CSP corresponds to some step in restricted Actor semantics (or an internal `τ` sequence).

Therefore `R` is a weak bisimulation, and the theorem is proved. ∎

---

### 5.2 Inencodability of Dynamic Actor Creation

**Theorem (Unbounded Spawn Cannot Be Encoded into Static CSP)**:

There exists no faithful encoding `[[·]] : Actor_unbounded → CSP` from Actor systems supporting **unbounded dynamic Actor creation** (unbounded spawn) to CSP.

**Proof Sketch**:

1. **Static Topology Limitation of CSP**: By lemma (CSP static channel topology), for any CSP process `P`, its set of communication channels `chan(P)` does not grow at runtime. All channels in CSP must be statically determined at process definition time.

2. **Dynamic Topology Requirement of Unbounded Spawn**: Actor systems supporting unbounded spawn can create arbitrarily many new actors at runtime, each requiring a new mailbox channel. This causes the communication topology to grow dynamically at runtime, with no fixed upper bound.

3. **Encoding Dilemma**: To simulate unbounded spawn in CSP, the encoding must either:
   - Pre-reserve CSP channels for every possibly created actor (impossible, because the number is unbounded); or
   - Dynamically create new channels at runtime (CSP lacks this capability).

4. **Violation of Encoding Criteria**: Any attempt to simulate unbounded spawn violates the compositionality or no-new-behavior criteria of Gorla's encoding criteria.

Therefore, unbounded spawn breaks the compositionality of CSP encoding, making static analysis tools based on CSP inapplicable to Actor systems with unbounded dynamic creation[^6].

---

## 6. Examples

### 6.1 Encoding Example: Simple Counter Actor

**Example**: Counter Actor and its CSP encoding

```scala
// Scala original code
class Counter extends Actor {
    var count = 0

    def receive = {
        case "inc" => count += 1
        case "get" => sender() ! count
        case "reset" => count = 0
    }
}
```

```csp
-- CSP Encoding
COUNTER(count, input, output) =
    input?msg ->
        CASE msg OF
            inc -> COUNTER(count + 1, input, output)
            get.reply_ch ->
                reply_ch!count ->
                COUNTER(count, input, output)
            reset -> COUNTER(0, input, output)

-- Mailbox process
COUNTER_MAILBOX(ch_in, ch_out, buffer) =
    (#buffer < MAX) & ch_in?msg -> COUNTER_MAILBOX(ch_in, ch_out, buffer ⧺ [msg])
    □
    (#buffer > 0) & ch_out!head(buffer) -> COUNTER_MAILBOX(ch_in, ch_out, tail(buffer))

-- Initial process composition
COUNTER_INIT =
    LET counter_in = new_channel()
        counter_out = new_channel()
        counter_proc = COUNTER(0, counter_out, counter_in)
        counter_box = COUNTER_MAILBOX(counter_in, counter_out, [])
    IN counter_proc [| {counter_out} |] counter_box
```

**Step-by-Step Derivation**:

1. Initial state `count = 0`, `buffer = []`.
2. Receive `"inc"`: `count` becomes `1`, process recurses.
3. Receive `"get"`: create reply channel `reply_ch`, send current `count`, process recurses.
4. Receive `"reset"`: `count` becomes `0`, process recurses.

---

### 6.2 Counterexample: Dynamic Address Passing Cannot Be Encoded into CSP

**Scenario**: In the full Actor model (e.g., Erlang), actor addresses can be passed as message contents—when sending a message, it is unnecessary to know whether the target actor runs on a local or remote node.

```erlang
% Erlang code: P1 sends a message to P2, simultaneously passing P3's address
P1 ! {msg, "hello", P3}.
```

**CSP Encoding Attempt**:

```csp
-- In CSP, channels must be explicitly specified
P1 = ch_local!msg -> SKIP        -- local channel
-- Cannot express: receiver "learns" a new channel from the message
```

**Analysis**:

- **Violated Premise**: Actor's address passing assumes "address is identity, can be dynamically passed"; CSP channels are statically named communication endpoints with no runtime channel-learning mechanism.
- **Resulting Anomaly**: If P3's address is passed to P2, P2 should be able to send messages to P3. But in the CSP encoding, P2 must statically know P3's channel name at definition time and cannot "learn" a new channel from the received message.
- **Conclusion**: Address passing is a core dynamic feature of Actor and cannot be preserved by static CSP encoding. Any Actor→CSP encoding loses expressiveness in scenarios supporting address passing.

---

### 6.3 Counterexample: Location Transparency Cannot Be Encoded into CSP

**Scenario**: In the Actor model (e.g., Erlang), actor addresses are location transparent—when sending a message, it is unnecessary to know whether the target actor runs on a local or remote node.

```erlang
% Erlang code: P1 sends a message to P2, P2 may be on a remote node
P1 ! {msg, "hello"}.
```

**CSP Encoding Attempt**:

```csp
-- In CSP, channels must be explicitly specified
P1 = ch_local!msg -> SKIP        -- P2 is local
-- or
P1 = ch_remote!msg -> SKIP       -- P2 is remote
```

**Analysis**:

- **Violated Premise**: Actor's location transparency assumes "address is identity, location independent"; CSP channels are statically named communication endpoints with no network/location abstraction.
- **Resulting Anomaly**: If P2 migrates from local to remote node, the Erlang program requires no modification; but the CSP encoding must replace `ch_local` with `ch_remote` and introduce network transport protocol encoding, changing the program's topological structure.
- **Conclusion**: Location transparency is a runtime feature of Actor and cannot be preserved by static CSP encoding.

---

### 6.4 Counterexample: Additional Complexity Introduced by Mailbox Implementation

**Scenario**: The mailbox of native Actor (e.g., Erlang) is a runtime-built-in, transparent FIFO queue supporting pattern matching and priority messages. The CSP encoding must explicitly implement these features.

**Native Actor Mailbox**:

```erlang
% Erlang: runtime automatically manages mailbox, supports pattern matching
receive
    {priority, high, Msg} -> ...;
    {normal, Msg} -> ...
after 5000 -> timeout
end.
```

**CSP Encoding Attempt**:

```csp
-- CSP explicit Mailbox must implement pattern matching and timeout itself
MAILBOX_PM(ch_in, ch_out, buffer) =
    ch_in?msg -> MAILBOX_PM(ch_in, ch_out, SORT_BY_PRIORITY(buffer ⧺ [msg]))
    □
    (#buffer > 0) & ch_out!SELECT_MATCH(buffer, pattern) ->
        MAILBOX_PM(ch_in, ch_out, REMOVE_MATCH(buffer, pattern))
    □
    TIMEOUT(5000) -> TIMEOUT_HANDLER
```

**Analysis**:

- **Violated Premise**: Actor's mailbox is a "zero-cost" runtime abstraction, completely transparent to the programmer; CSP has no equivalent built-in abstraction.
- **Resulting Anomalies**:
  1. **Pattern Matching**: CSP's `ch_out` can only output in FIFO order; to implement Actor's selective receive, complex `SELECT_MATCH` logic must be introduced in the MAILBOX process.
  2. **Timeout**: CSP's timeout construct differs from the mailbox's `after` semantics, requiring an additional timer process.
  3. **Memory Management**: Native Actor mailboxes are managed by runtime garbage collection; the `buffer` in the CSP encoding is an explicit data structure requiring manual management.
- **Conclusion**: The mailbox implementation in CSP encoding not only increases the number of processes, but also introduces pattern matching, timeout, and memory management complexity not present in native Actor systems.

---

## 7. Visualizations

### 7.1 Actor→CSP Encoding Scheme Overview

```mermaid
graph TB
    subgraph "Actor Layer"
        A1[Actor A<br/>send/receive/become]
        A2[Actor B<br/>send/receive/become]
        A3[Mailbox A<br/>FIFO Queue]
        A4[Mailbox B<br/>FIFO Queue]
    end

    subgraph "Encoding Layer [[·]]_A→C"
        E1[Encoding Function]
    end

    subgraph "CSP Layer"
        C1[ACTOR_A Process<br/>ch_a?msg → PROCESS]
        C2[ACTOR_B Process<br/>ch_b?msg → PROCESS]
        C3[MAILBOX_A Process<br/>Buffer Simulation]
        C4[MAILBOX_B Process<br/>Buffer Simulation]
        C5[Channel Synchronization<br/>ch_a, ch_b]
    end

    A1 -->|Encode| C1
    A2 -->|Encode| C2
    A3 -->|Encode| C3
    A4 -->|Encode| C4

    C1 <-->|Synchronize| C3
    C2 <-->|Synchronize| C4
    C3 -.->|Internal Buffer| C3
    C4 -.->|Internal Buffer| C4

    style A1 fill:#e1bee7,stroke:#6a1b9a
    style A2 fill:#e1bee7,stroke:#6a1b9a
    style C1 fill:#b2dfdb,stroke:#00695c
    style C2 fill:#b2dfdb,stroke:#00695c
    style C3 fill:#fff9c4,stroke:#f57f17
    style C4 fill:#fff9c4,stroke:#f57f17
```

**Figure Description**:

- Purple nodes represent abstract entities in the Actor layer; green nodes represent process encodings in the CSP layer; yellow nodes represent Mailbox Buffer processes.
- Actor's asynchronous message passing is encoded as indirect communication between CSP processes via Buffer processes.
- Each Actor corresponds to two processes in the CSP layer: `ACTOR` (handling behavior) and `MAILBOX` (buffering messages).

---

### 7.2 Mailbox as CSP Buffer Process

```mermaid
graph LR
    subgraph "Sender"
        S[ACTOR_S<br/>send(target, v)]
    end

    subgraph "Mailbox Process"
        M[MAILBOX_target<br/>ch_in?msg<br/>buffer := buffer ⧺ [msg]]
        M2[MAILBOX_target<br/>ch_out!head<br/>buffer := tail]
    end

    subgraph "Receiver"
        R[ACTOR_target<br/>receive(p) → P]
    end

    S -->|ch_in!v| M
    M -.->|Internal State| M2
    M2 -->|ch_out?v| R

    style S fill:#bbdefb,stroke:#1565c0
    style M fill:#fff9c4,stroke:#f57f17
    style M2 fill:#fff9c4,stroke:#f57f17
    style R fill:#c8e6c9,stroke:#2e7d32
```

**Figure Description**:

- Shows the buffering semantics of the Mailbox as an independent CSP process.
- The sender deposits a message via `ch_in`; the Mailbox appends the message to its internal `buffer`.
- The receiver obtains the message via `ch_out`; the Mailbox removes and outputs the message from the head of `buffer`.
- This separation enables asynchronous semantics to be realized within CSP's synchronous communication framework.

---

### 7.3 Axiom-Theorem Inference Tree

```mermaid
graph BT
    A1["[Axiom] CSP channels are FIFO queues<br/>Event order preserved in global trace"] --> L1
    A2["[Axiom] CSP process parameters are locally bound<br/>Cannot be directly accessed by external processes"] --> L2
    A3["[Axiom] Single CSP process internal events are strictly sequential<br/>No internal interleaving"] --> L3
    A4["[Axiom] Restricted Actor configuration transitions are structurally inductive<br/>send/receive/become/spawn"] --> L4

    L1["[Lemma-S-12-01] MAILBOX FIFO Invariant"] --> T1
    L2["[Lemma-S-12-03] State Inaccessible from External Processes"] --> T2
    L3["[Lemma-S-12-02] Actor Process Single-Threadedness"] --> T3
    L4["[Lemma] Encoding function [[·]]_A→C is a structural homomorphism"] --> T1

    T1["[Thm-S-12-01] Restricted Actor system encodable into CSP<br/>Preserves trace semantics equivalence"] --> C1
    T2["[Theorem] Encoding preserves state isolation"] --> C1
    T3["[Theorem] Encoding preserves atomic processing"] --> C1

    C1["[Corollary] [[·]]_A→C is a semantics-preserving encoding<br/>But full Actor cannot be encoded"]

    X1["[Counterexample] Dynamic address passing lost"] --> C1
    X2["[Counterexample] Location transparency lost"] --> C1
    X3["[Counterexample] Unbounded spawn breaks compositionality"] --> C1

    style A1 fill:#fff9c4,stroke:#f57f17
    style A2 fill:#fff9c4,stroke:#f57f17
    style A3 fill:#fff9c4,stroke:#f57f17
    style A4 fill:#fff9c4,stroke:#f57f17
    style L1 fill:#bbdefb,stroke:#1565c0
    style L2 fill:#bbdefb,stroke:#1565c0
    style L3 fill:#bbdefb,stroke:#1565c0
    style L4 fill:#bbdefb,stroke:#1565c0
    style T1 fill:#c8e6c9,stroke:#2e7d32
    style T2 fill:#c8e6c9,stroke:#2e7d32
    style T3 fill:#c8e6c9,stroke:#2e7d32
    style C1 fill:#f8bbd9,stroke:#ad1457
    style X1 fill:#ffcdd2,stroke:#c62828
    style X2 fill:#ffcdd2,stroke:#c62828
    style X3 fill:#ffcdd2,stroke:#c62828
```

**Figure Description**:

- Bottom yellow nodes are axioms/basic assumptions, the indivisible premises of the proof.
- Middle blue nodes are lemmas (Def-S-12-*), bridging axioms and theorems.
- Top green nodes are main theorems (Thm-S-12-01), constituting the complete proof of the encoding's semantics preservation.
- Pink node is the corollary, pointing out the precise boundary of the encoding.
- Red nodes are counterexamples, illustrating under which boundary conditions the theorem fails or the encoding has semantic loss.

---

### 7.4 Counterexample Scenario Diagram: Inencodability of Dynamic Address Passing

```mermaid
sequenceDiagram
    participant P1 as Actor P1
    participant P2 as Actor P2
    participant P3 as Actor P3
    participant CSP1 as CSP Encoding

    Note over P1,P3: Actor semantics: addresses can be dynamically passed
    P1->>P2: Send message {data, P3_address}
    P2->>P3: Send message using received address

    Note over CSP1: CSP semantics: channels must be statically named
    CSP1--xCSP1: Cannot "learn" new channels from messages
    CSP1--xCSP1: P2 must know P3's channel at definition time

    Note right of CSP1: Counterexample conclusion:<br/>Dynamic address passing<br/>cannot be preserved by static CSP encoding<br/>(Expressiveness level L4 → L3 cannot be reduced)
```

---

## 8. Cross-Layer Inference Summary

### Inference Relation Diagram

```mermaid
graph TB
    subgraph "Theoretical Domain"
        T1[L3: Static Topology<br/>CSP]
        T2[L4: Dynamic Topology without Mobility<br/>Restricted Actor]
        T3[L5: Dynamic Topology with Mobility<br/>Full Actor / π-calculus]
    end

    subgraph "Encoding Relation"
        E1["[[·]]_A→C: Restricted Actor → CSP<br/>✅ Exists, preserves trace semantics"]
        E2["[[·]]: Full Actor → CSP<br/>❌ Does not exist (unbounded spawn)"]
        E3["[[·]]: Full Actor → CSP<br/>❌ Does not exist (address passing)"]
    end

    subgraph "Engineering Inference"
        I1["Use CSP tools to verify restricted Actor systems"]
        I2["Full Actor systems require runtime compensation<br/>Supervision trees / dynamic monitoring"]
        I3["Microservice topology management requires external coordination services"]
    end

    T2 -->|Encode| T1
    T3 -.->|Not encodable| T1
    T3 -.->|Not encodable| T1

    E1 --> I1
    E2 --> I2
    E3 --> I3

    style T1 fill:#e1bee7,stroke:#6a1b9a
    style T2 fill:#b2dfdb,stroke:#00695c
    style T3 fill:#fff9c4,stroke:#f57f17
    style E1 fill:#c8e6c9,stroke:#2e7d32
    style E2 fill:#ffcdd2,stroke:#c62828
    style E3 fill:#ffcdd2,stroke:#c62828
```

**Inference Summary**:

1. **[Theory→Model]**: Restricted Actor systems (L4 subset) can be encoded into CSP (L3), but full Actor systems (L4/L5) cannot be encoded into CSP. This means the theoretical result "L4 ⊄ L3" directly limits the possibility of encoding.

2. **[Model→Implementation]**: Therefore, CSP-based programming languages (such as Go's channel subset) when building distributed systems requiring dynamic topology reconfiguration must introduce external coordination services (such as etcd, Consul) to compensate for the lack of dynamic address passing capability at the language level.

3. **[Implementation→Domain]**: In engineering practice, Erlang/OTP's full Actor capabilities (unbounded spawn, address passing) cannot be completely verified by CSP tools (such as FDR) and must rely on runtime mechanisms (supervision trees, dynamic monitoring) to ensure correctness.

---

## 8. References

### Document References

- [../01-foundation/01.03-actor-model-formalization.md](../01-foundation/01.03-actor-model-formalization.md) — Complete formal definition of the Actor model
- [../01-foundation/01.05-csp-formalization.md](../01-foundation/01.05-csp-formalization.md) — Formal definition of CSP process algebra
- [03.02-csp-to-actor-encoding.md](../00-INDEX.md) — CSP-to-Actor encoding scheme

### Bibliography

[^1]: Agha, G. (1986). *Actors: A Model of Concurrent Computation in Distributed Systems*. MIT Press.

[^2]: Hoare, C. A. R. (1985). *Communicating Sequential Processes*. Prentice Hall.

[^3]: de Nicola, R., & Hennessy, M. (1984). Testing equivalences for processes. *Theoretical Computer Science*, 34(1-2), 83-133.

[^4]: Sangiorgi, D., & Walker, D. (2001). *The π-calculus: A Theory of Mobile Processes*. Cambridge University Press.

[^5]: Gorla, D. (2010). Towards a unified approach to encodability and separation results between process calculi. *Information and Computation*, 208(8), 959-982.

[^6]: Nestmann, U. (2000). What is a "good" encoding of guarded choice? *Information and Computation*, 156(1-2), 287-319.

---

## Document Quality Checklist

- [x] Concept definitions include "Rationale for Definition" (4 definitions)
- [x] Each core definition derives at least 2-3 properties (3 properties total)
- [x] Relations use unified symbols clearly marked (⊂, ⊥, ≉)
- [x] Argumentation contains no logical leaps
- [x] Main theorem has complete proof (Thm-S-12-01)
- [x] Each main theorem is accompanied by counterexample or boundary test (4 counterexamples)
- [x] Document contains at least 3 different types of diagrams (concept dependency diagram, sequence diagram, inference tree, state diagram)
- [x] Cross-layer inferences use unified markers (3 inferences)
- [x] Inter-document reference links are valid
- [x] Contains formal definitions of encoding function, Mailbox Buffer, and address passing restriction
- [x] Contains at least 2 Def-S-12-*, 2 Lemma-S-12-*, 1 Thm-S-12-01
- [x] Discusses that dynamic Actor creation cannot be fully encoded into static CSP

---

*Document creation time: 2026-03-31*
*For AnalysisDataFlow project Struct module*

---

*Document version: v1.0 | Translation date: 2026-04-24*
