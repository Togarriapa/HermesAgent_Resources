# Parallel and Hierarchical Orchestration

Hermes orchestration is dependency-graph based, not sequential by default.

## Execution model

For every Epic, the Orchestrator creates one Kanban board and a dependency graph. Independent items run in parallel; dependency edges determine where sequencing is required. The Orchestrator may delegate branches of the graph to Team Leaders, which may form their own subteams and recruit specialists within delegated authority.

## Elastic profile instances

The registry does not impose a numeric maximum on instances of a profile. The Orchestrator may instantiate multiple copies of the same profile when parallel capacity is useful—for example, twenty Developer instances for twenty genuinely independent work packages. Actual concurrency is constrained by host/runtime CPU, RAM, API limits, credentials, workspace isolation, cost policy, and authorization.

Every instance has a unique identity, scoped assignment/context, its profile's original permissions, and a lifecycle. Scaling creates capacity, not additional authority.

## Parallel technical work

Concurrent code or configuration writers use isolated branches/worktrees/workspaces. Integration happens through an explicit reconciliation/review gate to avoid uncoordinated writes to the same state.

## Epic Kanban lifecycle

Each Epic board contains all relevant `Epic`, `User Story`, `Task`, `Defect`, `Spike`, `Risk`, and `Decision` items and uses `Backlog`, `Ready`, `In Progress`, `Review`, `Blocked`, and `Done` states. GitHub-backed work may use GitHub Projects v2; other work uses a local ephemeral board. After acceptance, Hermes archives a concise completion summary and deletes the board.

User-facing communication remains `User <-> Hermes <-> Orchestrator <-> Teams / Specialists` regardless of orchestration depth.
