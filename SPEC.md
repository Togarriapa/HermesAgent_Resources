# Hermes Resource Manifest v1

## Goals

The v1 contract makes agent resources portable, reviewable, composable, dynamically recruitable, safely updateable, and safe to share.

## Required envelope

Each YAML manifest must contain `apiVersion`, `kind`, `metadata`, and `spec`.

- `apiVersion`: currently `hermes.togarriapa/v1`.
- `kind`: one of `Profile`, `Skill`, `Plugin`, `MCP`, `Cron`, `Webhook`, `Channel`, or `Bundle`.
- `metadata.name`: stable lowercase kebab-case identifier.
- `metadata.version`: semantic version.
- `metadata.description`: human-readable purpose.
- `metadata.tags`: optional searchable tags.
- `spec`: kind-specific configuration.

## Dependencies

A resource may declare `spec.requires`:

```yaml
requires:
  skills:
    - docker-ops@^1.0.0
  plugins:
    - github@^1.0.0
```

Importers resolve dependencies by `(kind, name, version)` from `catalog.yaml` and fail closed when a required dependency is missing or incompatible.

## Inheritance

Profiles, skills, and bundles may use `spec.extends` with a resource selector such as `base@^1.0.0`.

Merge rules:

1. Scalars from the child replace parent scalars.
2. Maps merge recursively.
3. Lists append by default.
4. A future importer may support explicit replace/delete operators, but v1 manifests should avoid relying on them.
5. Cyclic inheritance is invalid.

## Runtime learned overlays

Published manifests are not the only runtime state. Effective resources compose layers with increasing precedence:

1. upstream registry base;
2. local experience overlay;
3. private user-learned overlay;
4. current explicit instruction/session context.

Upstream updates may replace layer 1 only. They must not overwrite layers 2 or 3. The runtime should semantically rebase overlays onto the new base, surface conflicts, regression-test the effective result, activate atomically, and retain rollback state.

Private user-learned overlays are runtime-private data. They must not be committed, exported, or converted into shared resources without deliberate de-identification/generalization and normal review.

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

### Epic Kanban

Every Epic gets one ephemeral Kanban board containing work items such as `epic`, `user-story`, `task`, `defect`, `spike`, `risk`, and `decision`. Independent work can proceed in parallel according to the dependency graph. After accepted completion, the runtime archives a concise completion summary and deletes the board.

Repository-backed work may use GitHub Projects v2; non-repository work may use a local ephemeral backend.

See `ORCHESTRATION.md`.

## Secrets

Manifests may reference environment variables with `${NAME}`. Importers must not resolve secret placeholders while parsing this repository; resolution happens at runtime. Secret-looking literals should be rejected by CI where practical.

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
4. Provider connectivity does not make a profile user-facing or expand local authorization.
5. Destructive actions, writes, sends, permission changes, and other side effects remain separately governed.
6. Runtime credentials stay outside Git and are scoped to the delegated user/account.
7. Marketplaces and indexes are discovery sources, not trust authorities.

See `EXTERNAL_INTEGRATIONS.md` and `INTEGRATION_MATRIX.md`.

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

Compatibility is advisory in v1 unless the importer enforces it.

## Conversation routing

The canonical conversational path is:

`User <-> Hermes <-> Orchestrator <-> Specialists / Teams`

Profile interaction fields are routing constraints, not merely behavioral suggestions. The runtime/importer should enforce them fail-closed.

- `base` defaults profiles to `userFacing: false`, `directUserContact: deny`, and `userChannelBinding: deny`.
- `hermes` is the sole profile permitted to override those defaults for user-facing interaction.
- User-facing channels, including web, Telegram, Discord, WhatsApp, and voice, route inbound and outbound through `hermes` and reject direct selection of any other profile.
- `orchestrator` accepts user-originating work from `hermes`, recruits and coordinates internal profiles/teams, and returns synthesized results to `hermes`.
- Specialists and Team Leaders communicate internally only.
- Clarification requests, scheduled outputs, webhook outcomes, alerts, and other user-visible events pass through `hermes` before delivery.

See `TOPOLOGY.md`.

## Voice

The shared voice contract is local-first. The preferred Home Assistant/Wyoming stack is Speech-to-Phrase for constrained home-control speech, Whisper for general speech-to-text, Piper for text-to-speech, and optional openWakeWord wake-word detection. Raw audio retention and cloud fallback are denied by default.

Voice input becomes a Hermes request; it does not bypass the Hermes/Orchestrator topology.

## WhatsApp

WhatsApp support is for WhatsApp Business accounts through an explicitly scoped integration. Personal-account automation is not part of the contract. WhatsApp is a user-facing channel and must route only through Hermes. Account-administration and destructive actions are denied by default. Proactive outbound behavior requires delegated/template-authorized handling.

## Improvement model

Do not silently mutate a published version. For behavior changes, bump `metadata.version`, keep the stable `metadata.name`, update the catalog, and document the change in the pull request. A local agent may extend a shared resource under a new name while preserving provenance through `metadata.source`.

Learned overlays differ from published versions: they are local composition layers and survive upstream resource replacement.

## Trust model

Repository content is configuration, not authorization. Local Hermes policy remains authoritative for filesystem access, shell execution, network access, credential use, destructive actions, outbound communications, profile-instance capacity, and external side effects. Conversation routing, integration policy, and resource manifests may restrict those capabilities but cannot expand them beyond host authority.
