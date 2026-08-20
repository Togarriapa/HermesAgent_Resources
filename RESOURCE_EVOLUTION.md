# Resource Evolution and Learned Overlays

Hermes resource updates use layered composition rather than replacing the effective agent configuration.

## Effective resource order

From lowest to highest precedence:

1. **Upstream registry base** — versioned shared manifests from `Togarriapa/HermesAgent_Resources`.
2. **Local experience overlay** — generalized improvements learned from successful/failed operation on this Hermes installation.
3. **Private user-learned overlay** — preferences, conventions, corrections, and context learned from the user that are appropriate to persist locally.
4. **Current explicit instruction/session context** — applies to the current work and is persisted only when the local learning policy says it should be.

Upstream updates may replace the upstream layer but must never overwrite the two local overlay layers. The `resource-evolution-manager` performs a three-way semantic rebase of overlays onto the new upstream base.

## Daily update flow

`daily-resource-reconcile` checks `main` once per day. The manager classifies upstream additions, compatible changes, breaking changes, removals, dependency changes, and safety/integration changes. Compatible changes are merged, regression-tested, and atomically activated. Ambiguous, conflicting, breaking, or authority-expanding changes are quarantined for review.

## Privacy

User-specific learning is private runtime state. It must not be committed to this repository, included in public/shared skill improvements, exported through analytics, or sent to external integration providers merely because it exists. A broadly useful lesson may be generalized only after removing user-specific/private details and passing normal skill review.

## Rollback

Before activation, the runtime preserves the previously effective configuration and overlay revisions. A failed validation or runtime smoke test restores the previous effective state without discarding learned overlays.
