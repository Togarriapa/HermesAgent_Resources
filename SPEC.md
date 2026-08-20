# Hermes Resource Manifest v1

## Goals

The v1 contract makes agent resources portable, reviewable, composable, and safe to share.

## Required envelope

Each YAML manifest must contain `apiVersion`, `kind`, `metadata`, and `spec`.

- `apiVersion`: currently `hermes.togarriapa/v1`.
- `kind`: one of `Profile`, `Skill`, `Plugin`, `MCP`, `Cron`, `Webhook`, `Channel`, or `Bundle`.
- `metadata.name`: stable lowercase kebab-case identifier.
- `metadata.version`: semantic version.
- `metadata.description`: human-readable purpose.
- `metadata.tags`: optional searchable tags.
- `spec`: kind-specific configuration.

## Dependencies

A resource may declare `spec.requires`:

```yaml
requires:
  skills:
    - docker-ops@^1.0.0
  plugins:
    - github@^1.0.0
```

Importers should resolve dependencies by `(kind, name, version)` from `catalog.yaml` and fail closed when a required dependency is missing or incompatible.

## Inheritance

Profiles, skills, and bundles may use `spec.extends` with a resource selector such as `base@^1.0.0`.

Merge rules:

1. Scalars from the child replace parent scalars.
2. Maps merge recursively.
3. Lists append by default.
4. A future importer may support explicit replace/delete operators, but v1 manifests should avoid relying on them.
5. Cyclic inheritance is invalid.

## Secrets

Manifests may reference environment variables with `${NAME}`. Importers must not resolve secret placeholders while parsing this repository; resolution happens at runtime. Secret-looking literals should be rejected by CI where practical.

## Compatibility

Resources may declare:

```yaml
compatibility:
  hermes: ">=1"
  os:
    - linux
  architectures:
    - arm64
    - amd64
```

Compatibility is advisory in v1 unless the importer enforces it.

## Conversation routing

The canonical conversational path is:

`User <-> Hermes <-> Orchestrator <-> Specialists / Teams`

Profile interaction fields are routing constraints, not merely behavioral suggestions. The runtime/importer should enforce them fail-closed.

- `base` defaults profiles to `userFacing: false`, `directUserContact: deny`, and `userChannelBinding: deny`.
- `hermes` is the sole profile permitted to override those defaults for user-facing interaction.
- User-facing channels must route inbound and outbound traffic through `hermes` and must reject direct selection of any other profile.
- `orchestrator` accepts user-originating work from `hermes`, recruits and coordinates internal profiles or teams, and returns synthesized results to `hermes`.
- Specialists and Team Leaders may communicate internally according to their delegated work, but they must not become user-facing endpoints.
- Clarification requests, scheduled outputs, webhook outcomes, alerts, and other user-visible events must pass through `hermes` before delivery.

See `TOPOLOGY.md` for the complete topology contract.

## Improvement model

Do not silently mutate a published version. For behavior changes, bump `metadata.version`, keep the stable `metadata.name`, update the catalog, and document the change in the pull request. A local agent may extend a shared resource under a new name while preserving provenance through `metadata.source`.

## Trust model

Repository content is configuration, not authorization. Local Hermes policy remains authoritative for filesystem access, shell execution, network access, credential use, destructive actions, and outbound communications. Conversation routing constraints likewise do not expand permissions; they only restrict which profiles may receive or emit user-facing traffic.
