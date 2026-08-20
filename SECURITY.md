# Security Policy

HermesAgent Resources is a configuration and capability registry. Repository content can **restrict and describe** runtime behavior, but it is not a credential store and cannot authorize actions beyond the local Hermes host/runtime policy.

## Security boundary

The absolute authorization ceiling is the deployed host/runtime policy plus the credentials/account scopes actually provisioned there. The following never create new authority by themselves:

- a Profile instruction;
- a Bundle membership;
- Orchestrator recruitment or additional instances;
- a Cron schedule or Webhook event;
- a learned/private overlay;
- prior successful access;
- prior user confirmation;
- current user confirmation for an operation the host/resource does not allow.

`QUALITY_POLICY.yaml` is restrictive/defaulting only and is validated to remain non-authority-expanding.

## Secrets and sensitive data

Do not commit:

- passwords or PINs;
- API keys, bearer/OAuth tokens or bot tokens;
- private keys, wallet seeds/recovery phrases, signing secrets or reusable MFA material;
- Cloudflare or provider credentials;
- database credentials/connection secrets;
- private financial credentials;
- private user-learned overlay contents;
- personal data that is not necessary to define a general reusable resource.

Use `${ENV_VAR}` or an explicit runtime credential reference in manifests. Secret placeholders must remain unresolved during registry validation and materialization.

Secrets must also be excluded/redacted from:

- logs and error messages;
- GitHub issues/PRs/comments;
- Kanban items;
- artifacts and generated effective-registry files;
- user-facing output;
- learned overlays unless a separate host secret-management facility owns the value.

`.gitignore` excludes common local environment/key/generated paths, but ignore rules are defense-in-depth rather than permission to keep secrets inside the repository directory.

## Credential provisioning

Runtime credentials should follow:

- least privilege;
- explicit user/account/tenant binding;
- separate read vs write credentials where the provider supports it;
- IP/network restrictions where useful;
- expiry/rotation/revocation metadata;
- runtime-only injection after resource resolution and host authorization;
- no credential copying into agent workspaces unless an integration explicitly requires a protected runtime mount.

Provider connectivity is not equivalent to Profile access. A Profile receives only operations allowed by its dependency/integration policy and host policy.

## Financial and signing material

Financial account and wallet credentials require stronger isolation. User private keys, seed phrases, recovery codes, PINs and reusable MFA material must never enter Profile-visible text context.

The Hermes live-wallet key boundary is separate from the user's Ledger/other wallets. Real-value signing/execution follows `FINANCIAL_ACCESS.md` and remains one-shot explicit-order + fresh-confirmation gated.

## Third-party dependencies and integrations

Treat external Plugins, MCPs, package dependencies, marketplaces and integration providers as supply-chain dependencies.

Before adoption or upgrade:

1. verify provenance/source and reviewed version/digest;
2. inspect requested credentials, filesystem/process/network access and tools;
3. review side effects and data sent externally;
4. test with least-privilege/non-production scope where possible;
5. pin reviewed production versions when practical;
6. document rollback/revocation;
7. run the full registry validation suite.

See `EXTERNAL_INTEGRATIONS.md`.

## State-changing actions

State changes should be:

- authorized at action time;
- scoped to the exact target/operation;
- idempotent/deduplicated where possible;
- bounded by timeout/retry behavior;
- verified after execution;
- reversible or compensatable where feasible;
- auditable without revealing secrets.

Ambiguous failures after a potentially successful external write must be reconciled before retrying blindly.

## User-facing routing

Only Hermes may be directly user-facing. User channels must authenticate/admit identities, isolate sessions, reject direct specialist targeting, protect against replay/duplicate privileged actions, and route user-visible Cron/Webhook/specialist results through Hermes.

See `TOPOLOGY.md`.

## Private learned overlays

Private learned/user-specific overlays remain local owner-scoped state. They must not sync to Git or external analytics/providers merely because upstream registry resources are updated.

Learned overlays can improve behavior/preferences but cannot grant permissions. See `RESOURCE_EVOLUTION.md`.

## Validation

Security-relevant registry invariants are enforced by:

```bash
python scripts/validate_registry.py
python scripts/validate_deliberation.py
python scripts/validate_expansion_v21.py
python scripts/validate_quality_v22.py
python scripts/validate_quality_overlays_v22.py
python scripts/materialize_effective_registry.py --check-only
```

CI runs these checks for proposed changes. A validation/CI error should be investigated before promotion; a GitHub Actions job that fails before any visible step executes is an infrastructure state, not evidence that a validator itself failed.

## Reporting a security issue

Do not publish credentials, exploit details against a live Hermes installation, private user information, or screenshots/logs containing secrets in a public issue/PR.

For this private repository, report a suspected security issue to the repository owner through an appropriate private channel. Include the affected resource/path, impact, reproduction conditions using redacted/synthetic values, and a proposed containment/rollback if known.

If a live credential may be compromised, revoke/rotate it first where doing so is safe, disable the affected integration, preserve redacted audit evidence, and investigate before re-enabling.
