# Registry Catalog Discovery — v2.2

## Why the catalog changed

Before v2.2, `catalog.yaml` repeated every resource's kind, name, version, and path. The manifest already contained the same identity, so the list created a second source of truth and allowed a valid new manifest to be forgotten during catalog editing.

v2.2 makes the resource manifests authoritative for resource identity and makes `catalog.yaml` a small discovery contract.

## Discovery roots

`catalog.yaml` declares exactly eight non-recursive resource roots:

- `profiles/` → `Profile`
- `skills/` → `Skill`
- `plugins/` → `Plugin`
- `mcps/` → `MCP`
- `crons/` → `Cron`
- `webhooks/` → `Webhook`
- `channels/` → `Channel`
- `bundles/` → `Bundle`

Every `*.yaml` directly under those roots is a registry resource and is validated. A new resource therefore cannot exist in a recognized root without becoming part of the discovered registry.

## Identity and validation

For each discovered resource:

1. the directory determines the expected `kind`;
2. `metadata.name` is the canonical stable name;
3. the filename must equal `metadata.name + .yaml`;
4. `metadata.version` must be semantic version;
5. `(kind, name, version)` must be unique;
6. every dependency selector and `extends` selector must resolve against discovered manifests;
7. cycles, missing dependencies, incompatible selectors, malformed manifests, and policy violations fail closed.

The runtime can build the complete catalog index deterministically by reading manifest metadata, so no generated index needs to be committed.

## Quality policy composition

`catalog.yaml` also declares the ordered quality-policy files. v2.2 currently loads:

1. `QUALITY_POLICY.yaml` — universal and kind defaults plus original domain overlays;
2. `QUALITY_POLICY_EXPANSION_V22.yaml` — additional restrictive overlays for AI engineering, traditional remedies, Amish/ancient cultural context, pregnancy/postpartum fitness, and specialized fitness.

Extensions may restrict behavior but cannot grant capability or exceed the local host authorization ceiling.

## Runtime import

The provisioner should discover manifests from the same roots, validate them, resolve dependencies and inheritance, apply quality policies, rebase approved local/private overlays, and then intersect the effective configuration with host authorization before instantiation.

See `RUNTIME_IMPORT.md`, `RESOURCE_QUALITY.md`, and `SPEC.md`.
