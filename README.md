# HermesAgent Resources

A shared, versioned resource registry for Hermes agents. The repository declares **capabilities and operating contracts, not authorization**: credentials, private learned state, and host-specific permissions stay outside Git.

## Architecture

Canonical user path:

`User <-> Hermes <-> Orchestrator <-> Specialist Profiles / Team bundles`

- **Hermes is the only user-facing Profile.** All user channels bind only to Hermes.
- **Orchestrator is internal.** It decomposes work into a dependency DAG, dynamically recruits any registered Profile/team, and runs independent work in parallel.
- **Team Leaders and specialists are internal.** Nested subteams and multiple instances are allowed subject to host policy.
- **Scaling creates capacity, never authority.**
- **Material decisions may deliberate.** Evidence and user constraints beat majority vote; credible dissent is preserved.
- **Every Epic gets an ephemeral Kanban.** The completion summary is archived before the board is removed.

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

## Registry v2.2: discovery instead of a duplicated index

`catalog.yaml@2.2.0` no longer repeats hundreds of manifest identities. It declares the eight resource roots and the quality-policy files. Every `*.yaml` directly under a recognized root is discovered automatically from its own metadata.

This means a new Profile/Skill/Plugin/MCP/Cron/Webhook/Channel/Bundle cannot be forgotten in a hand-maintained list. Validation still fails closed on malformed manifests, duplicate identities, missing/incompatible dependencies, invalid inheritance, topology violations, or security-policy violations.

See `CATALOG_DISCOVERY_V22.md`.

## Effective resource quality

Raw manifests stay focused on **domain-specific responsibility and capability**. `QUALITY_POLICY.yaml` and its restrictive extensions supply the common operating contract every resource needs: evidence freshness, assumptions, verification, privacy, secret handling, timeout/retry behavior, failure handling, auditability, lifecycle, and authority non-escalation.

Behavior/configuration composition is:

`kind defaults < domain quality overlays < resolved resource manifest < local experience overlay < private user-learned overlay < current session context`

**Host/runtime authorization is the absolute ceiling around the entire result.** User confirmation, learned behavior, inheritance, recruitment, scaling, or Bundle membership cannot create a permission the host/resource does not already possess.

See `RESOURCE_QUALITY.md`, `SPEC.md`, and `SECURITY.md`.

## Specialist capability coverage

v2.1 established broad specialist coverage across product/business/operations, law/privacy, technology, home/farm, education, information integrity, Catholic domains, architecture/fabrication, and more.

v2.2 adds **47 Profiles, 43 Skills, and 7 Bundles** across five major areas:

### HermesAgent and AI engineering

HermesAgent Expert; AI Developer; AI Systems Architect; AI Prompt Engineer; AI Agent Orchestration Engineer; AI Evaluation Engineer; LLMOps Engineer; AI Safety & Reliability Engineer; AI Knowledge Engineer.

### Traditional/naturalistic health research

Traditional Remedies Researcher; Herbalism & Ethnobotany Researcher; Historical Materia Medica Researcher; Natural Lifestyle Health Educator; Traditional Foodways Health Researcher.

Traditional use is never treated as clinical proof. These roles do not diagnose or prescribe and do not advise delaying urgent/effective care.

### Amish and ancient traditions

Dedicated Amish Profiles cover remedies, lifestyle, construction, farming, housekeeping, cooking, and preservation. Dedicated ancient-tradition Profiles cover remedies, lifestyle, construction, agriculture, domestic life, cooking, preservation, and crafts/material culture.

Amish claims are community/affiliation/region-specific. Ancient claims are civilization/place/period/source-specific. Neither domain is treated as a uniform tradition, and historical precedent never overrides modern safety.

### Traditional Catholic liturgy and heritage

Traditional Latin Mass; Roman Rite liturgical traditions; pre-Vatican-II practice; devotions/sacramentals; Gregorian chant/sacred music; calendar/fasting/abstinence; Patristics/Church Fathers; Ecclesiastical Latin.

These roles distinguish doctrine, liturgical law, discipline, historical practice, local custom, devotion, and opinion, and never impersonate ecclesiastical authority.

### Specialized fitness

Fitness Coach; Bodybuilding Coach; Calisthenics Coach; Powerlifting Coach; Prenatal/Postpartum Fitness Coach; Strength & Conditioning Coach; Mobility & Flexibility Coach; Endurance Conditioning Coach; Senior Fitness Coach; Youth Fitness Coach.

Fitness Profiles use symptom-aware progression and referral boundaries. Performance-enhancing drug/hormone advice and dangerous dehydration/rapid cuts are denied. Pregnancy/postpartum clinician restrictions are hard constraints.

See `CAPABILITY_COVERAGE.md`, `CAPABILITY_EXPANSION_V22.md`, `PROFILE_MATRIX_V22.md`, and `INTEGRATION_MATRIX_V22.md`.

## Financial and crypto separation

Research/management Profiles can analyse normalized data and propose actions. Real-value execution remains isolated to dedicated execution operators and exact authorization contracts.

- Banks/brokers/exchanges/Ledger use separate data and execution paths.
- A recommendation, target, schedule, previous order, or previous confirmation is not standing transaction authority.
- The dedicated Hermes live wallet remains confirmation-gated for real-value signing/broadcast.
- The autonomous sandbox wallet is testnet-only.

See `FINANCIAL_ACCESS.md` and `INVESTMENT_GOVERNANCE.md`.

## Learned behavior without forgetting

Runtime behavior is layered so upstream updates do not erase local learning:

`upstream/effective registry < local experience overlay < private user-learned overlay < current explicit context`

Learned overlays can improve behavior but cannot grant authority. See `RESOURCE_EVOLUTION.md`.

## Voice and user channels

Voice is local-first through Home Assistant/Wyoming: Speech-to-Phrase where suitable, Whisper for general STT, Piper for TTS, and optional openWakeWord. Raw-audio retention and cloud fallback are disabled by default.

WhatsApp support is WhatsApp Business only through its scoped integration. All user-visible channels remain Hermes-only.

## Resource layout

- `profiles/` — durable professional/operational responsibilities.
- `skills/` — reusable domain procedures.
- `plugins/` — bounded runtime/external integrations.
- `mcps/` — bounded Model Context Protocol definitions.
- `channels/` — Hermes-only communication adapters.
- `crons/` — recurring jobs.
- `webhooks/` — authenticated event-driven jobs.
- `bundles/` — starting team compositions.
- `templates/` — hardened kind-specific starters.
- `catalog.yaml` — discovery, quality-policy, and fail-closed catalog contract.

## Canonical import/materialization

A provisioner should fetch a pinned Git ref, discover and validate manifests, resolve selectors/dependencies/inheritance, apply quality policies, preserve secret placeholders, rebase permitted local/private overlays, intersect capabilities with host authorization, and only then instantiate resources.

`RUNTIME_IMPORT.md` defines the reference import pipeline and shared host-managed Codex authentication model.

```bash
python scripts/materialize_effective_registry.py --check-only
# or materialize unresolved effective resources under build/effective-registry/
python scripts/materialize_effective_registry.py
```

## Validation

Run the complete suite before merging:

```bash
python scripts/validate_registry.py
python scripts/validate_deliberation.py
python scripts/validate_expansion_v21.py
python scripts/validate_expansion_v22.py
python scripts/validate_quality_v22.py
python scripts/validate_quality_overlays_v22.py
python scripts/materialize_effective_registry.py --check-only
```

See `CONTRIBUTING.md` for contribution rules.
