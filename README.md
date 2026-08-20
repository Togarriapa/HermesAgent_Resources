# HermesAgent Resources

A shared, versioned resource registry for Hermes agents. Resources are declarative YAML manifests consumed by a provisioner/importer; credentials and private learned state do not belong in Git.

## Conversation architecture

The canonical topology is:

`User <-> Hermes <-> Orchestrator <-> Specialist Profiles / Team bundles`

`hermes` is the only user-facing Profile. Web, Telegram, Discord, WhatsApp Business, and voice route exclusively through Hermes and reject direct Profile selection. Specialists, execution operators and Team Leaders remain internal-only.

## Parallel, hierarchical and deliberative orchestration

Orchestrator uses a dependency DAG. Independent work may run in parallel, nested Team Leaders may coordinate subteams, and multiple instances of the same Profile are permitted subject to host/runtime policy. Scaling increases capacity, not authority.

For material, ambiguous, strategic or trade-off-heavy work, Orchestrator may run structured multi-agent deliberation: independent first positions, evidence/assumption mapping, cross-critique and steelmanning, position revision, and synthesis by evidence plus user constraints rather than majority vote. Material dissent is preserved. See `ORCHESTRATION.md` and `DELIBERATION.md`.

Every Epic receives one ephemeral Kanban board. A completion summary is archived and the board deleted after accepted completion.

## Hermes response contract

Every Hermes response renders exactly these six sections:

1. **Initial Question or Request**
2. **Quick Answer / Result / Action**
3. **Detailed Answer / Result / Action**
4. **Agent Profiles That Contributed**
5. **Opinions Against the Final Answer / Solution and Why**
6. **Permissions Needed to Proceed**

When appropriate Hermes uses `No material dissent.` and `None.` rather than inventing disagreement or permissions.

## Registry v2.1 capability coverage

Catalog v2.1 completes the prior capability-gap audit and adds durable Profiles across:

- product management, business analysis/requirements, COO/operations, people operations, recruiting, privacy/GDPR, negotiation and decision science;
- automotive maintenance, home energy/solar, water/wastewater, emergency preparedness, arboriculture and building biology/pest management;
- farm planning, horticulture/orchards, livestock health navigation and farm machinery maintenance;
- child development, SEN/special education, mathematics, science and literacy/reading education;
- insurance, estate/succession research, procurement/vendor management, EU regulatory law and Portugal/EU employment law;
- network engineering, SRE, database reliability, AI/ML engineering and privacy/security engineering;
- fact checking/source verification, misinformation/media literacy, ethics and knowledge management;
- Catholic relationship guidance, traditional family advice, Catholic Tradition, Catholic history, and prayer/devotional planning;
- professional European Portuguese ↔ English translation;
- building architecture, 3D model design, 3D printing, model making and model optimization.

Reusable cross-domain Skills cover claim verification, negotiation preparation, scenario/sensitivity analysis, decision records, root-cause analysis, vendor comparison, privacy screening, emergency checklist design, cost-benefit/TCO analysis, requirements engineering, translation, architectural planning, CAD, additive manufacturing and printability optimization.

See `CAPABILITY_COVERAGE.md`, `PROFILE_MATRIX.md`, and `INTEGRATION_MATRIX.md`.

## Team bundles added in v2.1

The audit-requested teams are implemented:

- `product-strategy-team`
- `people-career-team`
- `privacy-compliance-team`
- `home-resilience-team`
- `farm-reliability-team`
- `decision-science-team`

Additional v2.1 teams are:

- `catholic-tradition-family-team`
- `core-education-team`
- `architecture-fabrication-team`
- `additive-manufacturing-team`
- `information-integrity-team`
- `farm-planning-team`

Bundles are starting compositions, not recruitment ceilings.

## Resource evolution without forgetting

Effective configuration is layered from upstream registry base through local experience and private user-learned overlays to current explicit context. `resource-evolution-manager` rebases compatible upstream changes without overwriting or publishing private learning. See `RESOURCE_EVOLUTION.md`.

## Voice and channels

The local-first voice pipeline uses Home Assistant/Wyoming: Speech-to-Phrase where suitable, Whisper for general STT, Piper for TTS, and optional openWakeWord. Raw-audio retention and cloud fallback are disabled by default.

WhatsApp uses supported WhatsApp Business integration only. All user-visible channels remain Hermes-only.

## Resource types

- `profiles/` — durable internal agent responsibilities and role boundaries.
- `skills/` — reusable procedures and domain playbooks.
- `plugins/` — optional runtime integrations.
- `mcps/` — Model Context Protocol definitions.
- `crons/` — recurring jobs.
- `webhooks/` — event-driven jobs.
- `channels/` — communication adapters.
- `bundles/` — curated starting teams.

## Canonical runtime import

A provisioner can fetch this repository at a pinned Git ref, resolve `catalog.yaml`, dependencies and inheritance, preserve `${ENV_VAR}` placeholders until runtime, and materialize effective resources.

```yaml
resourceSource:
  repository: Togarriapa/HermesAgent_Resources
  ref: main
imports:
  - bundles/hermes-runtime.yaml
```

The registry defines contracts declaratively; the deployed Hermes provisioner/runtime must consume and enforce them before the behavior is operational.

## Safe defaults

- No passwords, API keys, bearer tokens, bot tokens, private keys or private learned data in Git.
- All non-Hermes Profiles are internal-only.
- External integrations are least-privilege and explicit.
- Financial execution retains its explicit-order/confirmation boundaries.
- Regulated legal, medical/veterinary, architecture/engineering, electrical, gas and other licensed responsibilities are clearly escalated.
- Deliberation cannot vote away safety, authorization, privacy or professional boundaries.

## Contributing

Update or add versioned resources, index them in `catalog.yaml`, then run:

```bash
python3 scripts/validate_registry.py
python3 scripts/validate_deliberation.py
python3 scripts/validate_expansion_v21.py
```

See `CONTRIBUTING.md` and `SPEC.md`.
