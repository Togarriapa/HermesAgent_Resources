# Resource Quality and Completeness Contract

`QUALITY_POLICY.yaml` is the registry-wide quality layer for every resource indexed by `catalog.yaml`. It exists to make the effective configuration complete without duplicating the same safety, evidence, retry, verification, observability, and lifecycle boilerplate into hundreds of manifests.

## Effective resource composition

For quality and behavior constraints, the importer composes configuration from low to high precedence:

1. the universal defaults in `QUALITY_POLICY.yaml`;
2. the kind defaults for Profile, Skill, Plugin, MCP, Channel, Cron, Webhook, or Bundle;
3. every matching domain overlay;
4. the resource manifest itself;
5. local host/runtime policy;
6. current explicit user authority where an action legitimately requires it.

Maps merge recursively. Lists append with duplicate removal. Higher-precedence scalars replace lower-precedence scalars.

The quality layer is **restrictive/defaulting only**. It may complete missing procedure, verification, failure-handling, privacy, or observability behavior; it may never grant a tool, credential, filesystem root, network target, account permission, user-facing route, side effect, financial authority, physical-control authority, or other capability that the resource/host did not already possess.

Host/runtime authorization remains authoritative.

## What “complete” means

Every effective resource must state enough information for another runtime or profile to use it without guessing its operating contract.

### Profile

An effective Profile defines:

- declared-role scope and out-of-scope delegation;
- intake of goals, constraints, assumptions, and current context;
- an inspect/plan/perform/verify/handoff workflow;
- evidence freshness, source traceability, and uncertainty handling;
- decision and trade-off rules;
- execution/side-effect authority boundaries;
- collaboration and recruitment handoff context;
- failure and escalation behavior;
- privacy/secret handling;
- observability/audit expectations;
- structured output expectations.

Only Hermes may be user-facing. A Profile cannot acquire authority from recruitment, scaling, bundle membership, previous similar work, or inference.

### Skill

An effective Skill defines:

- expected inputs and preconditions;
- a reusable procedure;
- evidence/input traceability;
- verification and success criteria;
- common failure modes;
- outputs and limitations;
- whether side effects exist and how they are authorized.

The quality policy provides a generic procedure shell, but every Skill manifest must still contain domain-specific method content such as principles, steps, rules, checks, a workflow, or equivalent specialist guidance. A description alone is not a complete Skill.

### Plugin

An effective Plugin defines:

- explicit capability exposure and default-deny behavior;
- credential isolation and least privilege;
- network timeout/retry/TLS behavior where applicable;
- write/destructive/financial side-effect rules;
- failure behavior;
- audit/redaction behavior;
- provider/source provenance expectations.

A provider connection never grants a Profile authority by itself.

### MCP

An effective MCP definition specifies explicit tools/roots or another bounded capability surface, runtime isolation, credentials, operation timeouts, side-effect policy, failure handling, auditing, and source/version provenance.

### Channel

An effective user channel specifies identity/admission, Hermes-only routing, session isolation, payload/rate/attachment limits, replay or message-ID deduplication, privacy/logging, delivery failure behavior, and observability.

No channel may expose a non-Hermes Profile directly.

### Cron

An effective Cron defines schedule/timezone, concurrency, idempotency, misfire behavior, timeouts/retries, mutation authority, failure notification, Hermes routing for user-visible results, and audit records.

A schedule is never standing authorization for an otherwise privileged side effect.

### Webhook

An effective Webhook defines authentication, event/schema validation, replay protection, deduplication, payload/rate limits, side-effect authority, safe failure behavior, audit records, and Hermes routing for user-visible results.

Receipt of a webhook is evidence that an event arrived; it is not implicit authorization to perform unrelated external writes.

### Bundle

An effective Bundle defines its purpose, starting composition, dynamic recruitment behavior, authority non-escalation, deliberation mode, lifecycle/release rules, completion verification, and contributor/delegation observability.

Bundles compose resources; they do not create new permissions.

## Domain overlays

`QUALITY_POLICY.yaml` applies additional constraints when resource names/tags indicate a domain with recurring risks or evidence requirements. Current overlays cover:

- legal/regulatory/privacy;
- finance/investment/insurance;
- health/psychology/nutrition;
- children/education;
- physical engineering/property/farm/automotive/additive manufacturing;
- Catholic theology/tradition/family guidance;
- research/information integrity/history;
- software/data/infrastructure;
- professional translation.

The overlays are intentionally conservative and additive. A resource may define stricter or more detailed rules.

## Materialization

Runtime/importer implementations should materialize the effective policy before instantiating a resource and retain both:

- the declared manifest; and
- the effective merged contract with the quality-policy version that produced it.

Secret placeholders remain unresolved during registry parsing/materialization. Runtime injection happens only after authorization and isolation policy are applied.

## Validation

`python scripts/validate_quality_v22.py` iterates every catalog entry individually, applies the quality policy, and checks that the resulting effective contract is complete for its kind. It also checks direct manifest signals that cannot safely be manufactured by defaults, such as domain-specific Profile instructions, domain-specific Skill method content, bounded plugin/MCP capability declarations, channel routing, Cron schedules, Webhook authentication, and Bundle imports.

The validator is complementary to:

- `validate_registry.py` — envelope, dependencies, topology and key integration invariants;
- `validate_deliberation.py` — debate and six-section Hermes response invariants;
- `validate_expansion_v21.py` — specialist expansion coverage and high-risk role boundaries.

## Evolution rule

Global quality defaults are a restrictive registry policy rather than a resource capability version. Updating them must:

1. remain non-authority-expanding;
2. preserve all explicit resource boundaries;
3. pass the full validation suite;
4. document behavior-affecting changes;
5. preserve learned/private overlays;
6. allow rollback to the prior quality-policy version.

If a resource itself gains a new capability, changes its professional responsibility, changes an integration permission, or otherwise changes its public manifest contract, its own semantic version must still be bumped normally.
