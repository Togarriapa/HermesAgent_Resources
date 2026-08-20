# Runtime / Provisioner Import Contract

This repository is declarative. A deployed Hermes host becomes compliant only when its provisioner/importer resolves, materializes, authorizes, isolates, and enforces the registry structurally.

## Canonical import pipeline

A production importer should perform these stages in order and fail closed on an invalid stage:

1. **Select source** — repository, immutable/pinned Git ref or explicitly approved moving ref, expected provenance.
2. **Fetch** — retrieve source without executing repository content.
3. **Validate raw registry** — run envelope/catalog/dependency/topology/deliberation/quality validation before activation.
4. **Resolve catalog selectors** — choose exact versions satisfying requested selectors.
5. **Resolve dependency graph** — recursively resolve `requires`, Bundle `imports`, and inheritance; reject missing/incompatible/cyclic dependencies.
6. **Resolve inheritance** — materialize parent→child manifest composition according to `SPEC.md`.
7. **Apply registry quality** — merge universal kind defaults and matching domain overlays from `QUALITY_POLICY.yaml` without expanding capabilities.
8. **Rebase local overlays** — apply local experience and private user-learned overlays semantically, surfacing conflicts.
9. **Apply current session context** — behavioral/contextual instructions for the current work.
10. **Enforce host authorization ceiling** — intersect requested capabilities with local filesystem/process/network/account/credential/side-effect policies. Anything not allowed is unavailable regardless of manifest/user request.
11. **Resolve compatibility** — OS/architecture/runtime/provider requirements; reject known incompatibility before launching.
12. **Plan isolation** — Profile identity, workspace/worktree, filesystem roots, network exposure, credential mounts/references, process/container limits, and inter-agent communication scope.
13. **Inject runtime secrets** — resolve only the credential references actually required by the authorized materialized resource. Never write resolved secrets back into generated manifests/workspaces/logs.
14. **Instantiate dependencies/providers** — Plugins/MCPs/channels/internal providers with health checks and least-privilege scope.
15. **Instantiate Profile/team** — with the effective resource contract and only the authorized capabilities.
16. **Register observability** — resource/version/policy version, instance identity, parent coordinator, permissions/capabilities, lifecycle and audit correlation.
17. **Acceptance check** — verify health, topology, required dependencies and critical read-only smoke tests before marking active.
18. **Atomic activation** — switch from prior effective generation only after acceptance; retain rollback state.

## Recommended resolved-resource record

For each instantiated resource, retain a non-secret internal record such as:

```yaml
resource:
  kind: Profile
  name: example
  declaredVersion: 1.0.0
  declaredPath: profiles/example.yaml
source:
  repository: Togarriapa/HermesAgent_Resources
  commit: <immutable-sha>
quality:
  policy: registry-quality@2.2.0
  domainOverlays: []
resolution:
  dependencies: []
  inheritance: []
  localOverlayRevision: <local-ref-or-none>
  privateOverlayRevision: <private-ref-or-none>
authorization:
  hostPolicyRevision: <local-policy-ref>
  grantedCapabilities: []
  deniedCapabilities: []
runtime:
  instanceId: <unique-id>
  parentCoordinator: orchestrator
  workspace: <non-secret-runtime-path>
  activatedAt: <timestamp>
```

Do not put resolved secret values into this record.

## Dependency and inheritance rules

- Resolve selectors to exact catalog versions before activation.
- Fail closed on missing/ambiguous dependency resolution.
- Detect inheritance cycles across the full graph.
- Parent configuration supplies defaults; child configuration specializes it according to the merge rules in `SPEC.md`.
- Dependencies provide only their declared capability surfaces.
- A Bundle's roster/imports do not merge all member permissions into every member.

## Quality-policy materialization

The quality policy is a restrictive/defaulting layer. The reference script:

```bash
python scripts/materialize_effective_registry.py
```

shows quality-policy materialization with secrets unresolved. A production importer must additionally resolve catalog dependencies/inheritance and local overlays as described above.

Store the policy version alongside the effective generation so a behavior change can be reproduced/rolled back.

## Authorization intersection

Authorization is not ordinary YAML precedence. Compute the effective requested capability, then intersect it with host policy:

`effective available capability = declared/resolved capability ∩ host/runtime permission ∩ credential/account scope`

For operations requiring explicit confirmation/order, user authority is an additional runtime predicate **inside that intersection**, never an expansion beyond it.

Examples:

- a Profile requiring GitHub does not gain repository write if the provided token/profile policy is read-only;
- a Bundle containing Financial Execution Operator does not authorize a trade;
- a valid trade confirmation cannot enable withdrawal permission absent from the execution credential/gateway policy;
- a Home Assistant control request cannot reach an entity that host/MCP exposure policy did not expose.

## Hermes-only topology enforcement

User channels should bind to Hermes at the adapter/router layer rather than trusting a prompt instruction.

Enforce:

- inbound/outbound Profile = Hermes;
- direct client Profile selection denied;
- non-Hermes Profile user-channel binding rejected at provisioning time;
- internal Profile messages authenticated/scoped to their assignment/session;
- clarification/results/alerts follow internal chain back to Hermes;
- session/correlation IDs prevent cross-user result delivery.

## Dynamic recruitment

When Orchestrator recruits a Profile:

1. resolve the latest compatible/allowed exact resource version from the current effective generation;
2. compute its own dependencies/effective quality/overlays;
3. intersect with host policy and available credential scope;
4. allocate isolated instance/workspace/context;
5. attach only assignment-relevant context;
6. register parent/child lifecycle and audit identity;
7. release the instance after handoff/completion.

Recruitment must never inherit the recruiting Profile's credentials merely because they communicate.

## Parallel writer isolation

For code/config/shared mutable state:

- isolated Git branches/worktrees/workspaces for independent technical writers;
- serialized or partitioned writes where target state cannot safely merge;
- explicit integration/reconciliation gate before shared-state promotion;
- rollback/compensation and post-write verification for material changes.

## Plugin/MCP lifecycle

Before exposing a Plugin/MCP to a Profile:

- resolve reviewed version/source;
- start in minimum network/process/filesystem scope;
- inject only required credential references;
- perform health/readiness checks;
- expose only approved tools/roots/operations;
- enforce timeout/retry/rate-limit policy;
- audit calls with redaction;
- stop/revoke cleanly when the Profile instance is released if the provider is instance-scoped.

Shared providers must still enforce per-Profile/user/account authorization on every call.

## Cron and Webhook instantiation

Scheduled/event resources are triggers, not standing permission grants.

The runtime should provide:

- idempotency/deduplication store;
- overlap/concurrency policy;
- retry/backoff/misfire behavior;
- payload/event validation and replay protection for Webhooks;
- correlation into Orchestrator/Hermes for user-visible results;
- exact authority checks before any state-changing action.

## Financial execution

The runtime must enforce the one-shot state machine in `FINANCIAL_ACCESS.md` outside LLM prompt text. Confirmation objects should be payload-bound, one-shot, short-lived, auditable and impossible to reuse after material changes.

Secrets/signing material stay behind execution-provider boundaries; decision Profiles receive normalized observations/results rather than raw keys.

## Resource evolution / activation

The daily reconcile process should create a **candidate generation**, never mutate the active generation in place.

Candidate flow:

`fetch -> validate -> resolve -> quality materialize -> rebase overlays -> permission-diff -> regression/smoke test -> snapshot -> atomic activate -> health verify`

On failure after activation, restore the prior generation while retaining overlay histories. Authority-expanding or semantically conflicting updates are quarantined rather than automatically applied.

## Shared host Codex authentication

The registry declares `codex` as host-managed with shared host authentication. A compliant provisioner should expose the approved host-managed Codex auth location/reference to eligible agent containers/processes without copying reusable credentials into individual agent workspaces.

Each agent should be able to use the authorized host connection while workspace isolation, Profile capability policy, and host account/session controls remain intact. The live provisioner implementation must verify the actual mount/reference behavior; the declaration alone is not proof that deployed agents currently share the authentication.

## Deployment acceptance criteria

A runtime generation should not be marked active until at minimum:

- all requested resources/dependencies resolved;
- raw and effective validation passed;
- Hermes is the only user-facing Profile;
- channel bindings/routes are correct;
- unauthorized capabilities are absent/fail closed;
- required Plugins/MCPs healthy;
- secret placeholders are not exposed in logs/materialized files;
- isolated workspaces/processes are available where required;
- relevant read-only health/smoke tests pass;
- rollback target is retained.

## Audit and rollback

Record non-secret generation metadata sufficient to answer:

- which source commit/resource versions/policy version were active;
- which overlays were applied;
- what host-policy revision authorized capabilities;
- which dependencies/providers/credentials references were selected;
- when activation occurred and acceptance tests passed;
- what generation to restore on rollback.

This lets the live Pi reproduce and diagnose effective behavior without storing credentials in Git or relying on undocumented prompt state.
