# Hermes Resource Manifest v1

## Goals

The v1 manifest envelope makes agent resources portable, reviewable, composable, dynamically recruitable, safely updateable, and safe to share. Registry quality policy v2.2 adds a common effective operating contract without changing the eight catalog resource kinds.

## Required envelope

Each catalog resource YAML manifest must contain `apiVersion`, `kind`, `metadata`, and `spec`.

- `apiVersion`: currently `hermes.togarriapa/v1`.
- `kind`: one of `Profile`, `Skill`, `Plugin`, `MCP`, `Cron`, `Webhook`, `Channel`, or `Bundle`.
- `metadata.name`: stable lowercase kebab-case identifier.
- `metadata.version`: semantic version.
- `metadata.description`: human-readable purpose.
- `metadata.tags`: optional searchable tags used in discovery and quality-domain matching.
- `spec`: kind-specific configuration.

`Catalog` is a special registry index document rather than a normal importable resource.

## Dependencies

A resource may declare `spec.requires`:

```yaml
requires:
  skills:
    - docker-ops@^1.0.0
  plugins:
    - github@^1.0.0
```

Importers resolve dependencies by `(kind, name, version)` from `catalog.yaml` and fail closed when a required dependency is missing or incompatible. Resolving a dependency makes its declared capability available to the resource; it does not bypass host authorization or grant unrelated tools.

## Inheritance

Profiles, Skills, and Bundles may use `spec.extends` with a resource selector such as `base@^1.0.0`.

Merge rules:

1. Scalars from the child replace parent scalars.
2. Maps merge recursively.
3. Lists append by default.
4. A future importer may support explicit replace/delete operators, but v1 manifests should avoid relying on them.
5. Cyclic inheritance is invalid.
6. Inheritance may restrict or specialize behavior but cannot expand effective authority beyond the child resource's dependencies/integration policy and host authorization.

## Registry quality policy

`QUALITY_POLICY.yaml` is a non-catalog registry policy applied to **every resource indexed by `catalog.yaml`**. It supplies conservative defaults for fields that every production-quality resource needs but that would otherwise be repeated hundreds of times: evidence handling, assumptions, verification, retry/timeout behavior, privacy, secret handling, auditability, failure behavior, lifecycle, and authority non-escalation.

Effective quality composition is:

1. universal quality defaults;
2. kind-specific defaults;
3. matching domain overlays;
4. resolved published resource declaration (including `extends` inheritance);
5. local experience overlay;
6. private user-learned overlay;
7. current explicit session context.

Maps merge recursively. Lists append/deduplicate. Higher-precedence scalars replace lower-precedence scalars.

**Authorization is not a precedence layer.** Host/runtime policy is the absolute capability ceiling around the entire effective configuration. Explicit user authorization may permit an otherwise confirmation-gated action only when that action is already allowed by the host, resource dependencies/integration policy, account scope, and safety policy. Neither user confirmation, learning, inheritance, recruitment, scaling, nor bundle membership can create authority that the host/resource does not possess.

The quality policy itself is restrictive/defaulting only:

- it may complete missing process, evidence, verification, privacy, failure, or observability behavior;
- it may never add a credential, tool, account permission, filesystem root, network target, user-facing route, physical-control permission, transaction permission, or other capability;
- resource-specific declarations remain authoritative when they are more specific or stricter;
- secret placeholders remain unresolved until runtime.

See `RESOURCE_QUALITY.md`.

## Runtime learned overlays

Published manifests are not the only runtime state. Effective resources compose learned/context layers with increasing behavioral precedence:

1. upstream registry base (including the registry quality policy and published resource);
2. local experience overlay;
3. private user-learned overlay;
4. current explicit instruction/session context.

Upstream updates may replace layer 1 only. They must not overwrite layers 2 or 3. The runtime should semantically rebase overlays onto the new base, surface conflicts, regression-test the effective result, activate atomically, and retain rollback state.

Learned overlays may improve preferences, procedures, heuristics, and context. They **cannot grant new permissions or capabilities**. Private user-learned overlays are runtime-private data and must not be committed, exported, or converted into shared resources without deliberate de-identification/generalization and normal review.

See `RESOURCE_EVOLUTION.md`.

## Dynamic orchestration

Orchestration is dependency-graph based rather than sequential by default.

- Independent work packages may run concurrently.
- Team Leaders and other coordinators may execute nested subteams within delegated authority.
- Orchestrator and Team Leader may recruit any registered Profile when needed.
- Multiple instances of the same Profile are permitted when useful for parallelism.
- The registry imposes no numeric instance ceiling; effective limits come from host/runtime resource, cost, credential, authorization, and isolation policy.
- Scaling creates execution capacity only; instances retain the permissions and safety boundaries of their Profile.
- Concurrent technical writers should use isolated workspaces/branches/worktrees and reconcile through an integration gate.
- Material decisions may use adaptive multi-agent deliberation, but majority vote never overrides evidence, user constraints, safety, or authority.

### Epic Kanban

Every Epic gets one ephemeral Kanban board containing work items such as `epic`, `user-story`, `task`, `defect`, `spike`, `risk`, and `decision`. Independent work can proceed in parallel according to the dependency graph. After accepted completion, the runtime archives a concise completion summary and deletes the board.

Repository-backed work may use GitHub Projects v2; non-repository work may use a local ephemeral backend.

See `ORCHESTRATION.md` and `DELIBERATION.md`.

## Secrets

Manifests may reference environment variables with `${NAME}` or explicit environment credential references where the provider schema requires them. Importers must not resolve secret placeholders while parsing or materializing this repository; resolution happens at runtime after authorization and isolation policy are applied.

Secret-looking literals should be rejected by CI where practical. Secrets must not appear in responses, logs, commits, artifacts, learned overlays, Kanban items, or materialized registry files.

## External integration policy

Profiles may narrow a shared integration provider through `spec.integrationPolicy`. The Composio contract is allowlist-based:

```yaml
requires:
  plugins:
    - composio@^1.0.0
integrationPolicy:
  composio:
    toolkits:
      - slug: gmail
        version: 20260721_00
        allowedTools:
          - GMAIL_FETCH_EMAILS
          - GMAIL_CREATE_EMAIL_DRAFT
    emailSend: deny
```

Rules:

1. Declaring `integrationPolicy.composio` requires an explicit `composio` plugin dependency.
2. Every toolkit is explicit, pins a dated production version, and contains a non-empty tool allowlist.
3. Tools from unlisted toolkits are unavailable.
4. Provider connectivity does not make a Profile user-facing or expand local authorization.
5. Destructive actions, writes, sends, permission changes, transactions, signing, and other side effects remain separately governed.
6. Runtime credentials stay outside Git and are scoped to the delegated user/account.
7. Marketplaces and indexes are discovery sources, not trust authorities.
8. External calls should have bounded timeout/retry/backoff and produce auditable, redacted failure information.
9. Connection/account scope must be checked at action time; prior successful access is not standing authorization.

See `EXTERNAL_INTEGRATIONS.md` and the integration matrices.

## Compatibility

Resources may declare:

```yaml
compatibility:
  hermes: ">=1"
  os:
    - linux
  architectures:
    - arm64
    - amd64
```

Compatibility is advisory in v1 unless the importer enforces it. A production importer should reject known-incompatible resources before materialization rather than attempting execution and discovering incompatibility through failure.

## Conversation routing

The canonical conversational path is:

`User <-> Hermes <-> Orchestrator <-> Specialists / Teams`

Profile interaction fields are routing constraints, not merely behavioral suggestions. The runtime/importer must enforce them fail-closed.

- `base` defaults Profiles to `userFacing: false`, `directUserContact: deny`, and `userChannelBinding: deny`.
- `hermes` is the sole Profile permitted to override those defaults for user-facing interaction.
- User-facing channels, including web, Telegram, Discord, WhatsApp, and voice, route inbound and outbound through `hermes` and reject direct selection of any other Profile.
- `orchestrator` accepts user-originating work from `hermes`, recruits and coordinates internal Profiles/teams, and returns synthesized results to `hermes`.
- Specialists and Team Leaders communicate internally only.
- Clarification requests, scheduled outputs, webhook outcomes, alerts, and other user-visible events pass through `hermes` before delivery.
- Channel/session identity must not leak context between users or allow a client-supplied Profile target to bypass routing.

See `TOPOLOGY.md`.

## Hermes response contract and deliberation

Hermes normalizes user-facing results into the six-section response contract defined in `DELIBERATION.md`: initial request, quick result, detailed result, contributing Profiles, material dissent, and permissions needed.

For material/ambiguous decisions, Orchestrator may collect independent first-pass positions, run cross-critique/steelman rounds, recruit Debate Analyst, allow revisions, and synthesize by evidence and user constraints. Internal reasoning stays internal; user-visible responses expose contributor identity and summarized material dissent rather than private scratch reasoning.

## Voice

The shared voice contract is local-first. The preferred Home Assistant/Wyoming stack is Speech-to-Phrase for constrained home-control speech, Whisper for general speech-to-text, Piper for text-to-speech, and optional openWakeWord wake-word detection. Raw audio retention and cloud fallback are denied by default.

Voice input becomes a Hermes request; it does not bypass the Hermes/Orchestrator topology. Voice sessions inherit the same authentication, correlation, permission, and confirmation requirements as text.

## WhatsApp

WhatsApp support is for WhatsApp Business accounts through an explicitly scoped integration. Personal-account automation is not part of the contract. WhatsApp is a user-facing channel and must route only through Hermes. Account-administration and destructive actions are denied by default. Proactive outbound behavior requires delegated/template-authorized handling.

## Materialization

A registry importer should preserve both the declared resource and the effective resource produced after quality defaults, domain overlays, inheritance, and permitted learned overlays are composed. The effective record should include the quality-policy version and provenance needed for audit/rollback.

`python scripts/materialize_effective_registry.py` provides a reference quality-policy materializer. It deliberately does not resolve secrets or expand authorization.

## Improvement model

Do not silently mutate a published resource version. For capability, responsibility, integration, or other resource-contract changes, bump `metadata.version`, keep the stable `metadata.name`, update the catalog, and document the change in the pull request. A local agent may extend a shared resource under a new name while preserving provenance through `metadata.source`.

Registry-wide restrictive/defaulting quality-policy changes are versioned in `QUALITY_POLICY.yaml` rather than forcing a semantic-version bump across every resource they constrain. Such changes must never expand authority and must pass full effective-registry validation.

Learned overlays differ from published versions: they are local composition layers and survive upstream resource replacement.

## Validation

The canonical suite is:

```bash
python scripts/validate_registry.py
python scripts/validate_deliberation.py
python scripts/validate_expansion_v21.py
python scripts/validate_quality_v22.py
python scripts/materialize_effective_registry.py --check-only
```

`validate_quality_v22.py` iterates every catalog entry individually and verifies the effective kind contract as well as direct domain content that defaults cannot invent.

## Trust model

Repository content is configuration, not authorization. Local Hermes host/runtime policy remains authoritative for filesystem access, shell execution, network access, credential use, destructive actions, outbound communications, account scope, financial transactions, physical controls, profile-instance capacity, and all external side effects.

Conversation routing, quality policy, integration policy, resource manifests, bundles, learned overlays, user confirmation, and orchestration may **restrict** or select within those capabilities but cannot expand them beyond host authority.
