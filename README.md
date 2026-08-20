# HermesAgent Resources

A shared, versioned resource registry for Hermes agents.

This repository is designed to be consumed by an agent provisioner/importer and improved through normal Git workflows. Resources are declarative YAML manifests: agents may pin them, compose them, extend them, and submit improved versions without embedding credentials in Git.

## Conversation architecture

The canonical user-facing topology is:

`User <-> Hermes <-> Orchestrator <-> Specialist profiles / Team bundles`

`hermes` is the **only** profile permitted to communicate directly with the user. The Orchestrator, Team Leader, and all specialist profiles are internal-only. User-facing web, Telegram, and Discord channels route exclusively to Hermes and reject direct profile selection.

Hermes receives the user's request and sends every work-bearing task to the Orchestrator. The Orchestrator decomposes the request, recruits the best-suited specialist profile or team, gathers and synthesizes the work, and returns the result to Hermes. Hermes then delivers the response to the user.

A recruited Team Leader may still recruit any additional registered profile needed for its delegated objective, but it remains internal and reports back through the orchestration chain rather than becoming a user endpoint.

If clarification is required, the Orchestrator asks Hermes, Hermes asks the user, and the answer returns through the same orchestration flow. User-visible scheduled results, alerts, webhook outcomes, and follow-ups must also surface through Hermes.

See [`TOPOLOGY.md`](TOPOLOGY.md) for the enforcement contract.

## Resource types

- `profiles/` — agent roles, operating principles, defaults, and resource dependencies.
- `skills/` — reusable procedures and domain playbooks.
- `plugins/` — optional runtime integrations exposed to an agent.
- `mcps/` — Model Context Protocol server definitions.
- `crons/` — recurring agent jobs.
- `webhooks/` — event-driven jobs and validation requirements.
- `channels/` — inbound/outbound communication adapters.
- `bundles/` — curated sets of resources for common agent roles and teams.

## Contract

Every resource uses:

```yaml
apiVersion: hermes.togarriapa/v1
kind: Skill
metadata:
  name: example
  version: 1.0.0
  description: Example resource
spec: {}
```

The canonical index is [`catalog.yaml`](catalog.yaml). See [`SPEC.md`](SPEC.md) for inheritance, dependency, secret, and import semantics.

## Canonical runtime import

A Hermes provisioner can clone or fetch this repository at a pinned Git ref, read `catalog.yaml`, resolve the requested resource and its dependencies, then materialize the resulting configuration into the agent workspace.

The normal user-facing deployment should import the `hermes-runtime` bundle:

```yaml
resourceSource:
  repository: Togarriapa/HermesAgent_Resources
  ref: main
imports:
  - bundles/hermes-runtime.yaml
```

`hermes-runtime` supplies the sole user-facing Hermes profile, the internal Orchestrator, user channels, and the single-contact routing contract. Specialist and team bundles remain internal resources that the Orchestrator or an authorized Team Leader can recruit when needed.

The repository defines this contract declaratively; the Hermes provisioner/importer still needs to enforce these routing fields at runtime before the architecture is operational on deployed agents.

Agents should pin production imports to a tag or commit SHA. `main` is appropriate for development/test agents.

## Safe defaults

- No passwords, API keys, bearer tokens, Cloudflare credentials, bot tokens, or private keys belong in this repository.
- Secret values are referenced as `${ENV_VAR}` and injected by the runtime.
- All profiles are internal-only by default; only the `hermes` profile explicitly overrides the base interaction policy for user-facing contact.
- Destructive operations should require explicit authorization unless the local agent policy says otherwise.
- Network-facing webhooks should validate signatures and reject unsigned traffic by default.

## Contributing

Fork/branch, extend an existing resource or add a new version, update `catalog.yaml`, run `python3 scripts/validate_registry.py`, and open a pull request. See [`CONTRIBUTING.md`](CONTRIBUTING.md).
