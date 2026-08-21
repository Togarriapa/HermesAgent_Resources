# Contributing

## Adding or improving a resource

1. Create a branch from current `main`.
2. Start from the matching kind-specific template under `templates/`.
3. Decide whether the change is a **resource contract change** or a **registry-wide restrictive quality-policy change**.
4. Keep `metadata.name` stable for compatible upgrades and bump `metadata.version` when an already-published resource contract changes.
5. Give Profiles domain-specific instructions/scope and Skills domain-specific method content. Quality defaults cannot manufacture expertise.
6. Keep credentials, private keys, tokens, private user data, and learned private overlays out of Git.
7. Put the manifest directly under its canonical discovery root using `<metadata.name>.yaml`. **Do not add a manual catalog entry:** v2.2 discovers manifests from their metadata.
8. If a genuinely new domain needs common restrictive behavior, add a reviewed quality-policy extension and regression cases rather than duplicating policy into every Profile.
9. Run the full validation suite.
10. Open a pull request describing purpose, behavior/authority impact, dependencies, evidence/source changes, compatibility impact, verification, and rollback.

## Discovery contract

`catalog.yaml@2.2.0` maps resource kinds to eight non-recursive roots. Every YAML manifest under those roots is automatically part of the registry.

The validator requires:

- directory kind matches manifest `kind`;
- filename matches `metadata.name`;
- semantic versioning;
- unique `(kind, name, version)`;
- resolvable dependency and inheritance selectors;
- Hermes-only user-facing topology;
- all special security/integration invariants.

See `CATALOG_DISCOVERY_V22.md`.

## Validation

```bash
python scripts/validate_registry.py
python scripts/validate_deliberation.py
python scripts/validate_expansion_v21.py
python scripts/validate_expansion_v22.py
python scripts/validate_quality_v22.py
python scripts/validate_quality_overlays_v22.py
python scripts/materialize_effective_registry.py --check-only
```

## Review expectations

Every change is reviewed against the **declared manifest** and its **effective contract** after quality policies and inheritance are applied.

Reviewers should verify, as applicable:

- the responsibility boundary is distinct and useful;
- Skills contain reusable domain procedure rather than labels;
- permissions are least-privilege and unlisted capability remains denied;
- secrets stay runtime-only and sensitive logs/artifacts are redacted;
- external calls have bounded timeout/retry/backoff and safe partial-failure behavior;
- state-changing operations are authorized, idempotent where possible, verified after execution, and reversible where feasible;
- Plugins/MCPs have bounded capability surfaces and trustworthy provenance;
- Channels are authenticated/admitted, session-isolated, bounded, and Hermes-only;
- Crons/Webhooks cannot manufacture authority;
- Bundles remain starting compositions and never expand member permissions;
- time-sensitive research refreshes current facts and preserves provenance;
- licensed, regulated, medical, veterinary, financial, or physical-safety boundaries are explicit;
- traditional/cultural research distinguishes documented practice from modern adaptation, evidence, safety, and reconstruction;
- user-visible results still pass through Hermes.

## Completion criteria

A resource is not complete merely because YAML parses. It must be understandable, executable within its authority, verifiable, observable, and safely degradable when inputs, tools, evidence, or permissions are missing.

See `RESOURCE_QUALITY.md`, `TOPOLOGY.md`, `ORCHESTRATION.md`, `DELIBERATION.md`, `EXTERNAL_INTEGRATIONS.md`, `FINANCIAL_ACCESS.md`, `RESOURCE_EVOLUTION.md`, and `SECURITY.md`.
