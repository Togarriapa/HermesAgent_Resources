# Contributing

## Adding or improving a resource

1. Create a branch from current `main`.
2. Start from the matching kind-specific template under `templates/`; do not copy a superficially similar resource if doing so would inherit irrelevant permissions.
3. Decide whether the change is a **resource contract change** or a **registry-wide restrictive quality-policy change**:
   - resource capability/responsibility/integration changes require that resource's semantic-version bump and catalog update;
   - restrictive/defaulting changes that never expand authority belong in `QUALITY_POLICY.yaml` and are versioned there.
4. Keep `metadata.name` stable for compatible upgrades. Use a new name only for a genuinely different responsibility boundary.
5. Give Profiles domain-specific instructions/scope and Skills domain-specific method content. `QUALITY_POLICY.yaml` supplies operational defaults but must never be used to manufacture missing expertise.
6. Keep credentials, private keys, tokens, user data, learned private overlays, and environment-specific secrets out of Git. Use `${ENV_VAR}` or an explicit runtime credential reference. Follow `SECURITY.md`.
7. Add or update the entry in `catalog.yaml` when a catalog resource is created/versioned.
8. If domain-overlay match rules change, add/update representative regression cases in `scripts/validate_quality_overlays_v22.py` so broad tags/substrings cannot silently attach unrelated policies.
9. Run the full validation/materialization suite:

```bash
python3 scripts/validate_registry.py
python3 scripts/validate_deliberation.py
python3 scripts/validate_expansion_v21.py
python3 scripts/validate_quality_v22.py
python3 scripts/validate_quality_overlays_v22.py
python3 scripts/materialize_effective_registry.py --check-only
```

10. Open a pull request describing purpose, behavior/authority impact, dependencies, evidence/source changes, migration/compatibility impact, verification, and rollback path.

## Review expectations

Every change is reviewed against the **declared manifest** and its **effective contract** after `QUALITY_POLICY.yaml` is applied.

Reviewers should verify, as applicable:

- the responsibility boundary is distinct and useful rather than duplicating another Profile;
- Skills contain a reusable domain procedure rather than a description-only label;
- permissions are least-privilege and unlisted capabilities remain denied;
- secrets stay runtime-only and logs/artifacts redact sensitive values;
- external calls have bounded timeout/retry/backoff and safe partial-failure behavior;
- state-changing operations are authorized, idempotent where possible, verified after execution, and reversible where feasible;
- Plugins/MCPs have a bounded capability surface and trustworthy provenance;
- Channels are authenticated/admitted, session-isolated, rate/payload bounded, and Hermes-only;
- Crons define concurrency, idempotency, misfire, retry, notification, and authority behavior;
- Webhooks authenticate, validate, deduplicate, resist replay, and cannot create standing authority;
- Bundles remain starting compositions, permit dynamic recruitment, and never expand member permissions;
- time-sensitive research refreshes current facts and preserves dates/provenance;
- licensed, regulated, medical, veterinary, legal, financial, or physical-safety boundaries are explicit;
- user-visible results still pass through Hermes and preserve contributor/dissent/permission metadata;
- domain overlays are relevant to the matched resource and do not create nonsensical cross-domain constraints;
- a future provisioner can resolve/materialize the resource without undocumented assumptions.

## Completion criteria

A change is not complete merely because its YAML parses. It should be understandable, executable within its authority, verifiable, observable, safely degradable when inputs/tools/permissions are missing, and materializable by the runtime contract.

The main contracts are:

- `RESOURCE_QUALITY.md` / `QUALITY_POLICY.yaml` — effective completeness;
- `SPEC.md` — manifest/composition semantics;
- `RUNTIME_IMPORT.md` — fail-closed provisioner/import sequence;
- `SECURITY.md` — secret, authorization, supply-chain and state-change security;
- `TOPOLOGY.md` — Hermes-only routing/session boundary;
- `ORCHESTRATION.md` / `DELIBERATION.md` — work graph, teams, debate and synthesis;
- `EXTERNAL_INTEGRATIONS.md` — third-party lifecycle and runtime integration controls;
- `FINANCIAL_ACCESS.md` / `INVESTMENT_GOVERNANCE.md` — financial data/execution and investment governance;
- `RESOURCE_EVOLUTION.md` — safe learned-overlay/upstream evolution.
