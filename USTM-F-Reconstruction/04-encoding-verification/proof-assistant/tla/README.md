# USTM TLA+ Specifications

TLA+ specifications for USTM-F phase 5.

## Structure

- `models/`: Flink core components
- `protocols/`: Distributed protocols
- `properties/`: Safety and liveness properties

## Files

- `JobManager.tla`: JobManager specification
- `TaskManager.tla`: TaskManager specification
- `CheckpointCoordinator.tla`: Checkpoint coordination
- `ChandyLamport.tla`: Distributed snapshot algorithm
- `ExactlyOnce.tla`: Exactly-once processing

## Model Checking

Use TLC (TLA+ Model Checker) with the provided configuration files.

## Documentation

See 04.06-tla-plus-specifications.md for detailed correspondence.
