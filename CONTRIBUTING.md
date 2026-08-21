# Contributing

## Change model

1. Branch from current `main`.
2. Start from the matching template in `templates/`.
3. Put each resource directly under its canonical root as `<metadata.name>.yaml`; discovery is automatic.
4. Keep a stable `metadata.name`; bump `metadata.version` whenever an existing resource contract changes.
5. Bump `catalog.yaml` version whenever the resource set changes. The catalog does **not** contain a manual resource list.
6. Give Profiles real role-specific instructions and Skills real reusable method content; quality defaults cannot manufacture expertise.
7. Keep credentials, secrets, private learned overlays and unnecessary user data out of Git.
8. Update existing canonical documentation when behavior, responsibility or integration boundaries change. **Do not create versioned/supplemental root docs** such as `*_V23.md`, capability-expansion supplements, catalog-discovery supplements, or quality-policy extension files.
9. Update `PROFILE_MATRIX.md`, `INTEGRATION_MATRIX.md`, and `CAPABILITY_COVERAGE.md` when their respective responsibility/integration/domain maps change.
10. Add/adjust validator regression cases for new safety, topology, integration or quality invariants.
11. Open a PR describing behavior, authority impact, compatibility, verification and rollback.

## Discovery contract

`catalog.yaml` maps the eight resource kinds to non-recursive manifest roots. CI requires directory-kind agreement, filename/name agreement, semantic versioning, unique identity, resolvable dependencies/inheritance, and fail-closed security/topology rules.

`python scripts/check_catalog_consistency.py` emits deterministic counts and a SHA-256 digest of the discovered registry. This is the canonical catalog-consistency check; there is no second resource list to sort manually.

## Pull-request quality rules

`python scripts/check_pr_quality.py` runs in PR CI and enforces:

- changed existing resources bump semantic version;
- any resource-set change bumps catalog version relative to the base branch;
- canonical root documents exist;
- forbidden versioned/supplemental root docs are absent;
- canonical Markdown local links resolve;
- checkout has enough history to compare against the PR base.

The PR template and CODEOWNERS reinforce review of catalog, quality-policy, workflow and validator changes. Repository rules/branch protection should require the validation status before merging.

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

## Review expectations

Review both the declared manifest and its inherited/effective quality contract. Confirm distinct responsibility, least privilege, bounded integrations, runtime-only secrets, safe retries/idempotency, explicit side-effect authorization, verification/rollback where applicable, Hermes-only user routing, non-authority-bearing Cron/Webhook/Bundle behavior, current evidence where material, and explicit professional/medical/legal/physical/financial boundaries.

For homelab/infrastructure changes additionally preserve the Authentik `System` boundary: trusted Hermes session principal binding, current direct/indirect effective-group evaluation, fresh pre-tool authorization for writes, fresh recipient resolution for infrastructure alarms, fail-closed Authentik failure, read-only Authentik administration surface, no raw SSH/arbitrary shell, bounded host/Nextcloud/Cloudflare targets, and no mutation authority from schedules/webhooks/alarms. `System` membership never replaces destructive-action confirmation or rollback/verification requirements.

For Kobo/ebook changes additionally preserve exported/authorized-file-only notebook ingestion, source/rights provenance, model/transport capability detection, EPUB validation, explicit outbound delivery, source-artifact preservation, and the no-DRM-circumvention boundary.

## Canonical documentation

Keep these living documents current rather than adding supplements: `README.md`, `SPEC.md`, `TOPOLOGY.md`, `ORCHESTRATION.md`, `DELIBERATION.md`, `PROFILE_MATRIX.md`, `INTEGRATION_MATRIX.md`, `CAPABILITY_COVERAGE.md`, `RESOURCE_QUALITY.md`, `RESOURCE_EVOLUTION.md`, `RUNTIME_IMPORT.md`, `EXTERNAL_INTEGRATIONS.md`, `SECURITY.md`, `FINANCIAL_ACCESS.md`, `INVESTMENT_GOVERNANCE.md`, and `CONTRIBUTING.md`.
