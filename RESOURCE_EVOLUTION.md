# Resource Evolution and Learned Overlays

Hermes resource updates use layered composition rather than replacing the effective agent configuration. The system is designed to gain useful local experience **without forgetting it, publishing it accidentally, or allowing learned behavior to become new authority**.

## Effective behavior order

From lowest to highest behavioral/configuration precedence:

1. **Registry quality defaults/domain overlays** — restrictive operational completeness from `QUALITY_POLICY.yaml`.
2. **Published resource declaration** — cataloged manifest after dependency/inheritance resolution.
3. **Local experience overlay** — generalized installation-specific improvements learned from successful/failed operation.
4. **Private user-learned overlay** — preferences, conventions, corrections, and context appropriate to persist locally.
5. **Current explicit instruction/session context** — applies to current work and persists only when local learning policy permits.

Host/runtime policy is separate from this precedence chain and is the absolute authorization ceiling. No overlay can add a tool, account scope, filesystem root, network permission, transaction authority, physical-control authority, or user-facing route.

## Overlay content rules

### Local experience overlay

May contain generalized local knowledge such as:

- hardware/runtime characteristics;
- known-good procedures and rollback paths;
- recurring failure signatures and mitigations;
- provider latency/rate-limit behavior;
- installation-specific naming/layout conventions;
- validated workflow optimizations.

It should not become a dumping ground for transient logs, secrets, or user-specific personal data.

### Private user-learned overlay

May contain appropriate persistent preferences/context needed to serve the user consistently, subject to local privacy/memory policy. It remains local/private, is owner-scoped, and must not be exported merely because a shared resource is updated.

Neither overlay may store passwords, private keys, seed phrases, reusable MFA material, raw financial credentials, or other secrets intended for the runtime secret boundary.

## Daily update flow

`daily-resource-reconcile` checks upstream `main` once per day. `resource-evolution-manager` classifies additions, compatible changes, breaking changes, removals, dependency changes, quality-policy changes, and safety/integration changes.

For a candidate update it should:

1. fetch and verify the intended upstream ref/provenance;
2. validate the raw registry;
3. materialize the candidate effective registry with its quality-policy version;
4. three-way rebase local experience/private overlays onto the candidate base;
5. surface semantic conflicts rather than silently choosing one side;
6. run registry/deliberation/quality regression tests and targeted runtime smoke tests;
7. compare permissions/integration surfaces before vs after;
8. quarantine authority-expanding, ambiguous, or breaking changes for review;
9. create a rollback snapshot;
10. atomically activate only a validated compatible candidate;
11. verify health after activation and roll back automatically on failed acceptance checks.

## Conflict handling

A conflict is not limited to a textual merge conflict. Semantic conflicts include:

- upstream removed/renamed a field that an overlay changes;
- a new policy makes an old learned procedure unsafe;
- an integration/tool was removed but an overlay assumes it exists;
- two layers give incompatible operational instructions;
- an overlay would broaden authority under a new upstream structure;
- a learned preference now conflicts with a current explicit instruction.

Ambiguous semantic conflicts are quarantined and reported through Hermes rather than guessed through.

## Quality-policy updates

`QUALITY_POLICY.yaml` may be updated independently of resource semantic versions because it is a restrictive/defaulting registry layer. A quality-policy change must never expand capabilities and should be regression-tested against **every catalog resource** before activation.

The active effective record should retain the policy version used to materialize it so behavior can be reproduced and rolled back.

## Privacy and publication

User-specific learning is private runtime state. It must not be committed to this repository, included in shared skill improvements, exported through analytics, or sent to external integration providers merely because it exists.

A broadly useful lesson may become an upstream resource improvement only after:

1. removing user-specific/private details;
2. generalizing the lesson into a reusable procedure or boundary;
3. checking it does not encode secrets or installation-specific authority;
4. normal resource review/versioning/validation.

Publishing a generalized lesson never deletes the local overlay that proved useful unless local policy intentionally retires it after successful migration.

## Rollback and history

Before activation, the runtime preserves:

- the prior upstream/resource ref;
- prior quality-policy version;
- prior effective materialization;
- overlay revisions;
- dependency/integration resolution metadata.

Rollback restores the previous effective state **without discarding learned overlays**. Overlay history should be versioned locally so a bad learning change can be reverted independently from an upstream rollback.

## Observability

Each reconcile attempt should record candidate ref, policy version, classifications, changed resources, conflicts, validation outcome, overlay rebase result, activation/rollback result, and any user-visible action needed. Secret/private values are redacted.
