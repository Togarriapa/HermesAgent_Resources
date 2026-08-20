# Contributing

## Adding or improving a resource

1. Create a branch.
2. Copy the closest existing resource or `templates/resource.yaml`.
3. Keep `metadata.name` stable for compatible upgrades and bump `metadata.version` using semantic versioning.
4. Never commit credentials or private endpoint tokens.
5. Add or update the entry in `catalog.yaml`.
6. Run `python3 scripts/validate_registry.py`.
7. Open a pull request describing the motivation, behavior change, compatibility impact, and rollback path.

## Review expectations

Changes to shell-capable skills, MCP servers, plugins, cron jobs, webhooks, or channels should be reviewed for least privilege, secret handling, idempotency, timeout behavior, and destructive side effects.

Profiles should describe durable behavior rather than one-off tasks. Skills should be narrow enough to compose. Cron jobs should be safe to retry. Webhooks should authenticate events before invoking agent work.
