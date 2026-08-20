# HermesAgent Resources

A shared, versioned resource registry for Hermes agents. The repository declares **capabilities and operating contracts, not authorization**: credentials, private learned state, and host-specific permissions stay outside Git.

## Architecture

Canonical user path:

`User <-> Hermes <-> Orchestrator <-> Specialist Profiles / Team bundles`

- **Hermes is the only user-facing Profile.** Web, Telegram, Discord, WhatsApp Business, and voice bind only to Hermes and reject direct specialist selection.
- **Orchestrator is internal.** It decomposes work into a dependency DAG, dynamically recruits any registered Profile/team, runs independent work in parallel, and may create multiple instances subject to host limits.
- **Team Leaders and specialists are internal.** Nested subteams are allowed; scaling creates capacity, never authority.
- **Material decisions may deliberate.** Independent first-pass positions, cross-critique/steelmanning, assumption challenge, revision, and Debate Analyst can be used; evidence and user constraints beat majority vote.
- **Every Epic gets one ephemeral Kanban.** The board is updated during work, a completion summary is archived, and the board is deleted after accepted completion.

See `TOPOLOGY.md`, `ORCHESTRATION.md`, and `DELIBERATION.md`.

## Hermes response contract

Every user-facing Hermes result is normalized into six sections:

1. **Initial Question or Request**
2. **Quick Answer / Result / Action**
3. **Detailed Answer / Result / Action**
4. **Agent Profiles That Contributed**
5. **Opinions Against the Final Answer / Solution and Why**
6. **Permissions Needed to Proceed**

When no credible dissent or additional permission exists, Hermes uses `No material dissent.` and `None.` rather than manufacturing content.

## Effective resource quality — v2.2

Raw manifests intentionally stay focused on **domain-specific responsibility and capability**. `QUALITY_POLICY.yaml` supplies the restrictive operational contract that every indexed resource also needs: evidence freshness, assumptions, verification, privacy, secret handling, timeout/retry behavior, failure handling, auditability, lifecycle, and authority non-escalation.

Effective quality composition is:

`kind defaults < domain quality overlays < resolved resource manifest < local experience overlay < private user-learned overlay < current session context`

That is a behavior/configuration precedence chain only. **Host/runtime authorization is an absolute ceiling around the entire result.** User confirmation, learned behavior, inheritance, recruitment, scaling, or Bundle membership cannot create a permission the host/resource does not already possess.

`QUALITY_POLICY.yaml` is defaulting/restrictive only; it never grants tools, credentials, account access, filesystem roots, network targets, physical control, transaction authority, or user-facing routes.

See `RESOURCE_QUALITY.md`, `SPEC.md`, and `SECURITY.md`.

## Capability coverage

The registry has specialist coverage across software/infrastructure, data/analytics/AI, product/business/operations/HR, finance/investment/accounting, law/privacy, home/property/resilience, farming/agriculture, education/homeschooling, research/information integrity, humanities/social sciences, career/remote work, Catholic theology/tradition/family guidance, professional PT↔EN translation, building architecture, and 3D/additive manufacturing.

`CAPABILITY_COVERAGE.md` is the concise capability map. `PROFILE_MATRIX.md` / `PROFILE_MATRIX_V21.md` document Profile-to-Skill boundaries; `INTEGRATION_MATRIX.md` / `INTEGRATION_MATRIX_V21.md` document external-tool posture.

Bundles are **starting compositions**, never closed rosters. Orchestrator and Team Leader may recruit outside the active Bundle whenever a different specialist is needed.

## Financial and crypto separation

Research/management Profiles can analyse normalized account/portfolio data and propose actions. Real-value execution remains isolated to dedicated execution operators and explicit authorization contracts.

- Banks/brokers/exchanges/Ledger use separate data vs execution paths.
- A recommendation, target allocation, schedule, previous order, or previous confirmation is not standing transaction authority.
- The dedicated Hermes live wallet is separate from user Ledger secrets and remains confirmation-gated for real-value signing/broadcast.
- The autonomous sandbox wallet is testnet-only.

See `FINANCIAL_ACCESS.md` and `INVESTMENT_GOVERNANCE.md`.

## Learned behavior without forgetting

Runtime behavior is layered so upstream updates do not erase local learning:

`upstream/effective registry < local experience overlay < private user-learned overlay < current explicit context`

`resource-evolution-manager` rebases compatible updates, protects private layers, regression-tests the effective result, activates atomically, and retains rollback state. Learned overlays may improve behavior but cannot grant authority.

See `RESOURCE_EVOLUTION.md`.

## Voice and user channels

Voice is local-first through the Home Assistant/Wyoming ecosystem: Speech-to-Phrase where suitable, Whisper for general STT, Piper for TTS, and optional openWakeWord. Raw-audio retention and cloud fallback are disabled by default.

WhatsApp support is **WhatsApp Business only** through its scoped integration. Every user-visible channel inherits Hermes-only routing, identity/session isolation, rate/payload controls, replay/dedup behavior where applicable, and redacted observability from the quality policy.

## Resource layout

- `profiles/` — durable professional/operational responsibilities.
- `skills/` — reusable domain procedures.
- `plugins/` — bounded runtime/external integrations.
- `mcps/` — bounded Model Context Protocol server definitions.
- `channels/` — Hermes-only communication adapters.
- `crons/` — recurring jobs.
- `webhooks/` — authenticated event-driven jobs.
- `bundles/` — starting team compositions.
- `templates/` — hardened kind-specific resource starters.
- `catalog.yaml` — canonical resource index.
- `QUALITY_POLICY.yaml` — registry-wide effective completeness defaults.

## Canonical import/materialization

A provisioner should fetch a pinned Git ref, validate the registry, resolve catalog selectors/dependencies/inheritance, apply `QUALITY_POLICY.yaml`, preserve secret placeholders, apply permitted local/private overlays, intersect capabilities with host authorization, and only then instantiate resources.

```yaml
resourceSource:
  repository: Togarriapa/HermesAgent_Resources
  ref: main
imports:
  - bundles/hermes-runtime.yaml
```

`RUNTIME_IMPORT.md` defines the fail-closed reference import pipeline, including isolation, credential injection, health acceptance, dynamic recruitment, atomic generation activation/rollback, and shared host-managed Codex authentication.

A reference quality-policy materializer is provided:

```bash
python scripts/materialize_effective_registry.py --check-only
# or write unresolved effective manifests under build/effective-registry/
python scripts/materialize_effective_registry.py
```

The live Hermes provisioner/runtime must consume and enforce these contracts before repository declarations become operational on the Pi.

## Validation

Run the complete suite before merging registry changes:

```bash
python scripts/validate_registry.py
python scripts/validate_deliberation.py
python scripts/validate_expansion_v21.py
python scripts/validate_quality_v22.py
python scripts/validate_quality_overlays_v22.py
python scripts/materialize_effective_registry.py --check-only
```

The main quality validator iterates every catalog resource individually and verifies its **effective** contract plus direct domain content that defaults cannot invent. The overlay regression validator checks representative cross-domain resources so broad matching rules cannot silently attach inappropriate quality policies.

## Safety model

- Secrets and private learned data never belong in Git.
- Non-Hermes Profiles remain internal-only.
- External integrations are explicit, least-privilege, and default-deny.
- Scheduled/event receipt does not create authority.
- State changes are authorized, bounded, verified, and reversible where feasible.
- Current/time-sensitive claims are refreshed when material.
- Licensed/regulated/legal/medical/veterinary/engineering/physical-safety boundaries are identified and escalated.
- Deliberation cannot vote away safety, privacy, authorization, or professional boundaries.

For contribution rules and templates, see `CONTRIBUTING.md` and `templates/README.md`. For runtime/security boundaries, see `RUNTIME_IMPORT.md` and `SECURITY.md`.
