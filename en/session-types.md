# Session Types

> **Language**: English | **Source**: [Struct/01-foundation/01.07-session-types.md](../Struct/01-foundation/01.07-session-types.md) | **Last Updated**: 2026-04-21

---

## 1. Definitions

Session Types, introduced by Kohei Honda (1993), are type theories for describing structured communication protocols between processes.

### Binary Session Type Syntax

Given value type $T$, session type $S$ is defined as:

$$
\begin{aligned}
S &::= !T.S \quad \text{(send value of type } T \text{, then continue as } S\text{)} \\
  &\mid \; ?T.S \quad \text{(receive value of type } T \text{, then continue as } S\text{)} \\
  &\mid \; \oplus \{ l_i : S_i \}_{i \in I} \quad \text{(internal choice: select label } l_i\text{)} \\
  &\mid \; \& \{ l_i : S_i \}_{i \in I} \quad \text{(external choice: offer branches } l_i\text{)} \\
  &\mid \; \text{end} \quad \text{(session termination)}
\end{aligned}
$$

### Duality

The dual of a session type represents the complementary behavior:

$$
\begin{aligned}
\overline{!T.S} &= ?T.\overline{S} \\
\overline{?T.S} &= !T.\overline{S} \\
\overline{\oplus \{ l_i : S_i \}} &= \& \{ l_i : \overline{S_i} \} \\
\overline{\& \{ l_i : S_i \}} &= \oplus \{ l_i : \overline{S_i} \} \\
\overline{\text{end}} &= \text{end}
\end{aligned}
$$

## 2. Properties

### Type Environment Formation

Well-typed processes satisfy:

$$
\Gamma; \Delta \vdash P :: T
$$

where $\Gamma$ is the shared environment, $\Delta$ is the linear session environment.

### Channel Linearity

Each session channel must be used exactly once (for communication) before being delegated or closed:

$$
\text{lin}(c) \Rightarrow \text{use}(c) = 1
$$

## 3. Key Theorems

### Type Safety

Well-typed processes do not commit communication errors (mismatched types, unexpected labels).

### Freedom from Deadlock

Well-typed binary session processes with no shared channels are deadlock-free.

### Protocol Compliance

If $P$ has session type $S$ and $Q$ has session type $\overline{S}$, then $P \mid Q$ satisfies the protocol without runtime communication errors.

## 4. Mapping to Stream Processing

| Session Type Concept | Stream Processing Equivalent |
|---------------------|------------------------------|
| $!T.S$ (send) | Producer emitting record type $T$ |
| $?T.S$ (receive) | Consumer reading record type $T$ |
| $\oplus$ (internal choice) | Stream partitioning by key |
| $\&$ (external choice) | Union of multiple input streams |
| $\text{end}$ | Stream termination / watermark |

## 5. Example: Two-Phase Commit

```
Coordinator:  !Prepare.(&{ Commit: !CommitAck.end,
                          Abort:  !AbortAck.end })
Participant:  ?Prepare.(⊕{ Commit: ?CommitAck.end,
                          Abort:  ?AbortAck.end })
```

## References

[^1]: Honda, "Types for Dyadic Interaction", CONCUR 1993.
[^2]: Wadler, "Propositions as Sessions", ICFP 2012.
[^3]: Gay & Hole, "Subtyping for Session Types in the Pi-Calculus", Acta Informatica, 2005.
