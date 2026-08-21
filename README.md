# HermesAgent Resources

A versioned registry of Hermes capabilities and operating contracts. The repository describes what resources are and how they behave; **host/runtime policy, credential scope, and explicit authorization remain the capability ceiling**.

## Architecture

`User <-> Hermes <-> Orchestrator <-> Specialist Profiles / Team Bundles`

- Hermes is the only user-facing Profile and all user channels bind to Hermes.
- Orchestrator decomposes work, recruits any suitable registered Profile, runs safe independent work in parallel, and reconciles results.
- Team Leaders and specialists are internal-only.
- Bundles are starting rosters, not permission pools or recruitment ceilings.
- Scaling creates capacity, never authority.
- Material decisions may use evidence-driven deliberation; credible dissent is preserved.

See `TOPOLOGY.md`, `ORCHESTRATION.md`, and `DELIBERATION.md`.

## Registry discovery

`catalog.yaml` declares eight non-recursive manifest roots: Profiles, Skills, Plugins, MCPs, Crons, Webhooks, Channels, and Bundles. Every direct `*.yaml` manifest in those roots is discovered from its own metadata; there is no duplicated hand-maintained resource list.

CI verifies filename/name/kind/version consistency, dependency and inheritance selectors, deterministic catalog digest, topology/security invariants, semantic-version bumps on changed resources, and a catalog-version bump whenever the resource set changes.

## Effective quality

`QUALITY_POLICY.yaml` is the single canonical restrictive/defaulting quality policy. It supplies common evidence, verification, privacy, retry, failure, audit, lifecycle, and authority-non-escalation behavior plus narrowly matched domain overlays.

Behavior composition is:

`kind defaults < domain overlays < resolved manifest < local experience overlay < private user overlay < current session context`

Host/runtime authorization surrounds that entire composition and cannot be expanded by prompts, learning, Bundles, schedules, webhooks, or confirmation.

See `RESOURCE_QUALITY.md`, `SPEC.md`, and `SECURITY.md`.

## Capability coverage

The registry covers software/infrastructure/data/AI; product/operations/people; finance/investment/accounting; law/privacy; home/property/farm; education; research/humanities; Catholic theology/tradition/liturgy; traditional and historical living/remedies; fitness; translation; architecture/fabrication; and ebook/Kobo workflows.

Kobo support is based on user-exported notebooks and approved Dropbox/Google Drive/USB paths. Ebook delivery is explicit-user-order only; Kobo credential scraping, store purchasing, deletion, and DRM circumvention are denied.

See `CAPABILITY_COVERAGE.md` for the current domain map. For an always-current Profile/Skill/integration table generated directly from manifests, run:

```bash
python scripts/render_registry_reference.py
```

No static versioned matrix supplements are maintained.

## Financial and crypto separation

Research/management Profiles may analyse and recommend. Real-value execution stays isolated behind dedicated execution operators and exact one-shot authorization/confirmation contracts; autonomous crypto experimentation remains testnet-only. See `FINANCIAL_ACCESS.md` and `INVESTMENT_GOVERNANCE.md`.

## Resource evolution and update notifications

GitHub CI validates registry changes. After a successful validation run on `main`, an optional workflow can send a signed `registry-update-available` event to the live Hermes runtime. The event is **notification, not authority**: Resource Evolution Manager must fetch the immutable commit, validate/materialize it, rebase private/local overlays, compare permission surfaces, and classify it as import-ready or quarantined before activation.

See `RESOURCE_EVOLUTION.md` and `RUNTIME_IMPORT.md`.

## Kobo / ebook workflow

Typical flow:

`Kobo exported notes -> Kobo Library & Notebook Specialist -> Ebook Planner -> Writer -> Editor/Publisher -> Designer -> Converter -> EPUB validation -> explicit delivery to Kobo`

The `kobo-bridge` uses approved user-authorized cloud connections where the configured Kobo model supports them, with USB sideload/export fallback. The `ebook-toolchain` uses host-managed conversion/validation tools and keeps source artifacts intact.

## Resource layout

- `profiles/` — durable professional/operational responsibilities
- `skills/` — reusable methods and procedures
- `plugins/` — bounded integrations/runtime toolchains
- `mcps/` — bounded MCP definitions
- `channels/` — Hermes-only communication adapters
- `crons/` — recurring jobs
- `webhooks/` — authenticated events
- `bundles/` — starting team compositions
- `templates/` — canonical starters
- `scripts/` — discovery, validation, materialization and generated-reference tooling
- `catalog.yaml` — discovery and fail-closed catalog contract
- `QUALITY_POLICY.yaml` — canonical effective-quality policy

## Canonical documentation

- `SPEC.md` — manifest/discovery/composition contract
- `TOPOLOGY.md` — user/channel/session routing
- `ORCHESTRATION.md` — work packaging, teams and execution
- `DELIBERATION.md` — internal debate and Hermes response contract
- `RESOURCE_QUALITY.md` — completeness requirements
- `RESOURCE_EVOLUTION.md` — updates and learned overlays
- `RUNTIME_IMPORT.md` — provisioner/import lifecycle
- `EXTERNAL_INTEGRATIONS.md` — integration admission and provider rules
- `SECURITY.md` — security boundary and secrets
- `FINANCIAL_ACCESS.md` / `INVESTMENT_GOVERNANCE.md` — financial domain
- `CAPABILITY_COVERAGE.md` — current capability map
- `CONTRIBUTING.md` — change and PR rules

Update these canonical files when behavior changes; do not add versioned supplement documents.

## Validation

```bash
python scripts/check_catalog_consistency.py
python scripts/validate_registry.py
python scripts/validate_deliberation.py
python scripts/validate_expansion_v21.py
python scripts/validate_expansion_v22.py
python scripts/validate_quality_v22.py
python scripts/validate_quality_overlays_v22.py
python scripts/render_registry_reference.py --output /tmp/registry-reference.md
python scripts/materialize_effective_registry.py --check-only
```

On pull requests, CI additionally runs `scripts/check_pr_quality.py` against the base branch. See `CONTRIBUTING.md`.
