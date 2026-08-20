# HermesAgent Resources

A shared, versioned resource registry for Hermes agents.

This repository is designed to be consumed by an agent provisioner/importer and improved through normal Git workflows. Resources are declarative YAML manifests: agents may pin them, compose them, extend them, and submit improved versions without embedding credentials in Git.

## Resource types

- `profiles/` — agent roles, operating principles, defaults, and resource dependencies.
- `skills/` — reusable procedures and domain playbooks.
- `plugins/` — optional runtime integrations exposed to an agent.
- `mcps/` — Model Context Protocol server definitions.
- `crons/` — recurring agent jobs.
- `webhooks/` — event-driven jobs and validation requirements.
- `channels/` — inbound/outbound communication adapters.
- `bundles/` — curated sets of resources for common agent roles.

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

## Suggested agent import

A Hermes provisioner can clone or fetch this repository at a pinned Git ref, read `catalog.yaml`, resolve the requested resource and its dependencies, then materialize the resulting configuration into the agent workspace.

Example bundle selection:

```yaml
resourceSource:
  repository: Togarriapa/HermesAgent_Resources
  ref: main
imports:
  - bundles/homelab-agent.yaml
```

Agents should pin production imports to a tag or commit SHA. `main` is appropriate for development/test agents.

## Safe defaults

- No passwords, API keys, bearer tokens, Cloudflare credentials, bot tokens, or private keys belong in this repository.
- Secret values are referenced as `${ENV_VAR}` and injected by the runtime.
- Destructive operations should require explicit authorization unless the local agent policy says otherwise.
- Network-facing webhooks should validate signatures and reject unsigned traffic by default.

## Contributing

Fork/branch, extend an existing resource or add a new version, update `catalog.yaml`, run `python3 scripts/validate_registry.py`, and open a pull request. See [`CONTRIBUTING.md`](CONTRIBUTING.md).
