# Runtime / Provisioner Import Contract

This repository is declarative. A deployed Hermes host becomes compliant only when its provisioner/importer discovers, resolves, materializes, authorizes, isolates and enforces the registry structurally.

## Canonical import pipeline

A production importer should fail closed through these stages:

1. **Select source** — repository plus immutable/pinned commit and expected provenance.
2. **Fetch** — retrieve source without executing repository content.
3. **Discover/validate raw registry** — use the catalog roots; validate envelopes, identities, dependencies, topology, deliberation and quality.
4. **Resolve selectors/dependency graph** — recursively resolve `requires`, Bundle imports and compatible versions.
5. **Resolve inheritance** — parent→child composition according to `SPEC.md`; reject cycles.
6. **Apply registry quality** — merge universal/kind defaults and matching domain overlays from the single `QUALITY_POLICY.yaml` without expanding capability.
7. **Rebase local/private overlays** — semantically preserve local experience and private user learning; quarantine conflicts.
8. **Apply current session context** — behavioral context for current work only.
9. **Intersect host authorization** — filesystem/process/network/account/credential/side-effect policy is the absolute ceiling.
10. **Resolve compatibility** — OS/architecture/runtime/provider/device requirements.
11. **Plan isolation** — Profile identity, workspace/worktree, filesystem roots, network exposure, credential references, process/container limits and internal communication scope.
12. **Inject runtime secrets** — resolve only authorized references and never persist resolved values into registry/workspace/logs.
13. **Instantiate providers/resources** — Plugins/MCPs/channels/internal providers, then Profiles/Bundles with least privilege and health checks.
14. **Register observability** — source commit, resource/policy versions, instance lineage, effective capabilities and audit correlation.
15. **Acceptance check** — health, topology, dependencies and relevant read-only/smoke tests.
16. **Atomic activation** — switch generations only after acceptance and retain rollback state.

## Effective capability

`available capability = declared/resolved capability ∩ host/runtime policy ∩ credential/account scope`

Where an operation requires confirmation/order, valid user authority is an additional predicate **inside** that intersection. It never expands it.

A Bundle does not pool member permissions; recruitment does not inherit the coordinator's credentials; schedule/webhook receipt does not create mutation authority.

## Recommended resolved record

Retain non-secret provenance sufficient to reproduce behavior:

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

## Hermes-only topology

Adapters enforce Hermes inbound/outbound, deny direct specialist selection and non-Hermes user-channel binding, scope internal messages to assignment/session, and correlate clarifications/results/alerts back to the correct Hermes conversation.

## Dynamic recruitment and parallelism

Recruit against the active generation, resolve the recruited Profile's own dependencies/effective quality, intersect with host policy, allocate isolated context/workspace, register parent-child lifecycle and release after handoff. Concurrent technical writers use isolated branches/worktrees or serialized/partitioned writes plus an integration gate.

## Provider lifecycle

Before exposing a Plugin/MCP, resolve reviewed source/version, restrict network/process/filesystem scope, inject only required credentials, health-check it, expose only approved operations, enforce timeout/retry/rate policy, audit with redaction and revoke/stop cleanly when no longer needed.

## Crons and Webhooks

The runtime maintains idempotency/dedup/replay stores, overlap/misfire policies, bounded retry, payload validation and exact authority checks. User-visible outcomes route through Hermes.

### Registry update notice

A successful `main` validation may cause GitHub to POST the signed `registry-update-available` event defined by `webhooks/registry-update-notice.yaml` when repository notification settings are enabled.

The runtime must:

1. verify HMAC signature, event type, delivery ID/replay and payload schema;
2. verify repository and immutable commit;
3. compare the commit with the active generation;
4. run the normal candidate pipeline below;
5. report assessment through Hermes.

**Receipt does not authorize import/activation.** The configured webhook secret authenticates a notification source only.

## Candidate update / resource evolution

Never mutate the active generation in place. Candidate flow:

`notice/daily-check -> fetch immutable commit -> discover/validate -> resolve -> quality materialize -> rebase overlays -> permission/compatibility diff -> regression/smoke tests -> snapshot -> policy-approved activation -> health verify`

Authority-expanding, breaking, semantically conflicting or incompatible updates are quarantined. Rollback restores the prior generation without discarding overlay histories. See `RESOURCE_EVOLUTION.md`.

## Kobo / ebook runtime requirements

`kobo-bridge` must detect device/model capability before choosing cloud delivery. Dropbox/Google Drive connections are owner-authorized OAuth connections and must expose only the required read/write file operations. USB mode requires an explicitly approved Kobo mount root.

Notebook inputs are exported user files, not scraped Kobo account data. Delivery accepts validated non-DRM EPUB/PDF only and requires an explicit user order. Existing-file replacement requires confirmation.

`ebook-toolchain` should expose approved host binaries (for example Pandoc/EPUBCheck/Calibre where installed) through a bounded wrapper rather than arbitrary shell access. Conversion keeps source artifacts, validates outputs and records checksums/results.

## Financial execution

The runtime enforces the one-shot state machine in `FINANCIAL_ACCESS.md` outside prompt text. Confirmation objects are exact-payload-bound, short-lived, one-shot and auditable; ambiguous provider outcomes reconcile before retry. Secret/signing material stays behind execution-provider boundaries.

## Shared host Codex authentication

Eligible agents reuse the approved host-managed Codex authentication location/reference. Do not require separate per-agent login or copy reusable credentials into agent workspaces. Workspace isolation and Profile/host policy still apply to every Codex call.

## Deployment acceptance criteria

Do not mark a generation active until requested resources/dependencies resolve, raw/effective validation passes, Hermes-only topology holds, unauthorized capabilities are absent, required providers are healthy, secrets remain protected, needed isolation exists, relevant smoke tests pass and a rollback target is retained.

## Audit and rollback

Record source commit/catalog/policy/resource versions, applied overlays, host-policy revision, dependency/provider/credential references, acceptance outcome, activation time and rollback target—without secret values. This allows the Pi runtime to reproduce and diagnose effective behavior rather than relying on undocumented prompt state.
