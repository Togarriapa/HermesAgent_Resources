# Security Policy

HermesAgent Resources is configuration, not a credential store or authorization system. **Deployed host/runtime policy plus actually provisioned credential/account scope is the absolute capability ceiling.** Profiles, Bundles, schedules, webhooks, learned overlays, prior access and user confirmation cannot create a capability that ceiling does not allow.

## Secrets and sensitive data

Never commit passwords/PINs, API/OAuth/bot tokens, private keys/seeds/recovery material, reusable MFA, provider/database/financial credentials, private learned overlays, or unnecessary personal data. Use `${ENV_VAR}`/runtime references and keep them unresolved during repository materialization.

Redact/exclude secrets from logs, PRs/issues, Kanban, generated artifacts, user-facing output and learned overlays. `.gitignore` is defense in depth, not a secret-management boundary.

## Private content

Kobo notebook exports, reading notes, draft manuscripts and personal annotations are private user data by default. Process only the files/folders explicitly supplied or authorized for the task, retain provenance where needed, minimize copies, and do not commit or publish them through this repository. Ebook source/rights provenance must be preserved and DRM circumvention is denied.

## Credential provisioning

Use least privilege, explicit owner/account binding, read/write separation where supported, useful expiry/rotation/revocation, runtime-only injection after resource resolution/host authorization, and protected mounts rather than copying reusable credentials into workspaces.

Provider connectivity does not imply Profile access.

## Financial/signing material

User wallet keys/seeds/PINs/MFA never enter Profile-visible text. Real-value financial execution follows `FINANCIAL_ACCESS.md`, including exact one-shot authorization, confirmation, idempotency and reconciliation.

## Third-party integrations

Verify provenance/version, requested credentials/filesystem/process/network access, side effects, external data flow, least-privilege testing, pins, rollback/revocation and full registry validation before adoption/upgrades. See `EXTERNAL_INTEGRATIONS.md`.

## State-changing actions

Authorize exact target/operation at action time; use dedup/idempotency where possible; bound timeouts/retries; verify after execution; preserve rollback/compensation; and reconcile ambiguous external-write failures before retry. Signed webhooks—including registry update notices—are triggers, never independent mutation authority.

## User-facing routing

Only Hermes may be directly user-facing. Channels authenticate/admit identities, isolate sessions, reject specialist targeting and protect against replay/duplicate privileged actions. User-visible job/event results route through Hermes.

## Private learned overlays

Private owner-scoped overlays stay local and cannot grant authority. Upstream updates may rebase but never silently publish or erase them. See `RESOURCE_EVOLUTION.md`.

## Validation

CI runs catalog consistency, PR semantic-version/document hygiene, registry/topology/deliberation/specialist/quality regression checks and effective materialization. A GitHub Actions job that fails before any visible step executes is infrastructure state, not evidence that a validator itself failed.

## Reporting

Do not put live credentials, private user content, exploitable live-installation details or secret-bearing logs in issues/PRs. Report privately to the repository owner with redacted/synthetic reproduction details. If a credential may be compromised, revoke/rotate it first when safe, disable the affected integration and preserve redacted evidence.
