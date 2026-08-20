# HermesAgent Resources

A shared, versioned resource registry for Hermes agents.

This repository is designed to be consumed by an agent provisioner/importer and improved through normal Git workflows. Resources are declarative YAML manifests: agents may pin them, compose them, extend them, and submit improved versions without embedding credentials in Git.

## Conversation architecture

The canonical user-facing topology is:

`User <-> Hermes <-> Orchestrator <-> Specialist profiles / Team bundles`

`hermes` is the **only** profile permitted to communicate directly with the user. Web, Telegram, Discord, WhatsApp Business, and voice channels all route exclusively through Hermes and reject direct profile selection.

Hermes receives text or speech, sends work-bearing requests to the Orchestrator, handles clarification, and returns the final text or spoken response. Specialists and Team Leaders remain internal-only regardless of orchestration depth.

See [`TOPOLOGY.md`](TOPOLOGY.md) for the enforcement contract.

## Parallel and hierarchical orchestration

The Orchestrator uses a dependency DAG rather than a sequential-only queue. Independent work packages run in parallel. Work may be delegated through multiple levels of Team Leaders and specialist subteams, and the Orchestrator may create multiple instances of the same profile when parallel capacity is useful.

The registry does **not** impose a numeric per-profile instance ceiling. Effective concurrency is governed by host/runtime CPU, RAM, API limits, cost, credentials, authorization, and workspace-isolation policy. Scaling increases capacity, not authority.

Every Epic receives one ephemeral Kanban board containing Epic/User Story/Task/Defect/Spike/Risk/Decision items. The board is updated throughout execution, a completion summary is archived after acceptance, and the board is then deleted. Repository-bound Epics may use GitHub Projects v2; other work uses a local ephemeral backend.

See [`ORCHESTRATION.md`](ORCHESTRATION.md).

## Resource evolution without forgetting

Daily resource reconciliation does not overwrite local learning.

Effective resources are layered, low to high precedence:

1. upstream registry base;
2. local experience improvements;
3. private user-learned overlay;
4. current explicit instruction/session context.

`resource-evolution-manager` checks upstream daily, rebases local overlays onto compatible changes, regression-tests the effective result, and atomically activates safe updates. Breaking or ambiguous changes are quarantined. User-specific learning remains private local state and is never automatically pushed to the shared repository.

See [`RESOURCE_EVOLUTION.md`](RESOURCE_EVOLUTION.md).

## Voice

The local-first voice pipeline uses Home Assistant's Wyoming ecosystem:

- Speech-to-Phrase for fast constrained home-control speech where appropriate;
- Whisper for general assistant speech-to-text;
- Piper for local text-to-speech;
- optional openWakeWord wake-word detection.

Raw audio retention and cloud fallback are disabled by default. Voice traffic still follows `Audio <-> Hermes <-> Orchestrator <-> Specialists`.

## WhatsApp

WhatsApp is supported as a **WhatsApp Business** channel using the scoped Composio WhatsApp toolkit. It does not use unsupported personal-account automation. Inbound/outbound traffic is Hermes-only; account administration and destructive tools are denied, while proactive outbound messages require delegated/template-authorized behavior.

## Resource types

- `profiles/` — agent roles, operating principles, defaults, and resource dependencies.
- `skills/` — reusable procedures and domain playbooks.
- `plugins/` — optional runtime integrations exposed to an agent.
- `mcps/` — Model Context Protocol server definitions.
- `crons/` — recurring agent jobs.
- `webhooks/` — event-driven jobs and validation requirements.
- `channels/` — inbound/outbound communication adapters.
- `bundles/` — curated sets of resources for common agent roles and teams.

## Contract

Every resource uses:

```yaml
apiVersion: hermes.togarriapa/v1
kind: Skill
metadata:
  name: example
  version: 1.0.0
  description: Example resource
spec: {}
```

The canonical index is [`catalog.yaml`](catalog.yaml). See [`SPEC.md`](SPEC.md) for inheritance, dependency, secret, orchestration, integration, and import semantics.

## Canonical runtime import

A Hermes provisioner can clone or fetch this repository at a pinned Git ref, read `catalog.yaml`, resolve requested resources and dependencies, and materialize the effective configuration into the agent workspace.

```yaml
resourceSource:
  repository: Togarriapa/HermesAgent_Resources
  ref: main
imports:
  - bundles/hermes-runtime.yaml
```

`hermes-runtime` supplies Hermes, the internal elastic Orchestrator, web/Telegram/Discord/WhatsApp/voice channels, and daily safe resource reconciliation. Specialist/team bundles remain internal and dynamically recruitable.

The repository defines these contracts declaratively; the live Hermes provisioner/importer must enforce them before they are operational on deployed agents.

## Safe defaults

- No passwords, API keys, bearer tokens, Cloudflare credentials, bot tokens, private keys, or user-learned private data belong in this repository.
- Secret values are referenced as `${ENV_VAR}` and injected by the runtime.
- All profiles are internal-only by default; only `hermes` may be user-facing.
- External integration access is least-privilege and explicit.
- Destructive actions require authorization according to local policy.
- Private learned overlays never auto-publish.

## Contributing

Fork/branch, extend an existing resource or add a new version, update `catalog.yaml`, run `python3 scripts/validate_registry.py`, and open a pull request. See [`CONTRIBUTING.md`](CONTRIBUTING.md).
