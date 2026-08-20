# External Integration Sources

Third-party directories are discovery inputs, not authorization sources. Runtime permissions remain local to Hermes.

## Trust tiers

1. **First-party implementation/documentation** — preferred when available. Example: Home Assistant's official MCP Server integration.
2. **Official protocol registry** — useful for provenance/discovery metadata, followed by source review. Example: the official MCP Registry.
3. **Managed integration provider** — acceptable with explicit toolkit/credential scoping and version policy. Example: Composio.
4. **Public skill index or marketplace** — discovery only until the underlying source, license, scripts, dependencies, and permissions are reviewed. Example: Agent37 Skills.
5. **Unknown source** — do not install or execute without provenance and security review.

## Composio policy

The shared `composio` plugin is default-deny. A profile must declare an explicit toolkit allowlist and explicit tool allowlists. Connections are user-scoped and runtime credentials stay outside Git. Remote Composio workbench, remote bash, arbitrary proxying, and unlisted toolkits are denied by the registry policy.

Profiles receive only toolkits needed for their normal responsibility. A toolkit connection never makes a profile user-facing; user communication still follows `User <-> Hermes <-> Orchestrator <-> Specialists / Teams`.

Production toolkit definitions should be pinned to reviewed dated versions. Updating a pinned toolkit should be treated as a dependency upgrade and reviewed for tool/schema/permission changes before rollout.

## Agent37 policy

Agent37 is useful as a large searchable index of public skills, but indexing, stars, forks, and activity are not security review. `agent37-discovery` is therefore read-only/discovery-only. Candidate skills must be traced to their source repository and reviewed using `agent-skill-vetting` and `third-party-supply-chain-review` before any concept or executable component is adopted.

## MCP policy

Use the official MCP Registry for discovery when possible, but registry metadata alone is not sufficient to approve execution. The official registry is intentionally permissive and currently in preview, so review the server source, transport, authentication, requested credentials, tools, network destinations, filesystem/shell access, release provenance, maintenance, and rollback path before approval.

The registry's namespace verification is useful provenance evidence, not a guarantee that a server is appropriate or safe for Hermes.

## Home Assistant

Home Assistant is standardized on its **first-party Model Context Protocol Server integration**. The canonical endpoint is `${HOME_ASSISTANT_URL}/api/mcp`; `${HOME_ASSISTANT_URL}/api/mcp/assist` is available when the built-in Assist LLM API is explicitly preferred. Entity exposure stays least-privilege and safety-sensitive controls remain confirmation-gated.

## Review workflow

Candidate external resources should flow through the internal `integration-review-team`:

`Integration Curator -> Cybersecurity Analyst -> Systems Architect -> Team Leader`

That team may recommend a resource for registry adoption, but installation/execution still requires the local Hermes provisioner/runtime policy to permit it.
