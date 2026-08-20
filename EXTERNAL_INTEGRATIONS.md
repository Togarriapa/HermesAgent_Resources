# External Integration Sources

Third-party directories are discovery inputs, not authorization sources. Runtime permissions remain local to Hermes.

## Trust tiers

1. **First-party implementation/documentation** — preferred when available. Examples: Home Assistant MCP/Wyoming integrations and GitHub Projects/GitHub MCP.
2. **Official protocol registry** — useful for provenance/discovery metadata, followed by source review. Example: the official MCP Registry.
3. **Managed integration provider** — acceptable with explicit toolkit/credential scoping and version policy. Example: Composio.
4. **Public skill index or marketplace** — discovery only until the underlying source, license, scripts, dependencies, and permissions are reviewed. Example: Agent37 Skills.
5. **Unknown source** — do not install or execute without provenance and security review.

## Composio policy

The shared `composio` plugin is default-deny. A profile must declare explicit toolkit and tool allowlists. Connections are user-scoped and runtime credentials stay outside Git. Remote workbench, remote bash, arbitrary proxying, and unlisted toolkits are denied.

Production toolkit definitions are pinned to reviewed dated versions. Updating a pin is a dependency upgrade and should be reviewed for tool/schema/permission changes.

A toolkit connection never makes a profile user-facing; all user communication still follows `User <-> Hermes <-> Orchestrator <-> Specialists / Teams`.

## WhatsApp Business

WhatsApp is integrated only through a supported **WhatsApp Business** connection. The registry pins the Composio `whatsapp` toolkit version and exposes only the messaging/history/media subset required by the Hermes channel.

Policy:

- personal WhatsApp account automation is unsupported and not used;
- inbound and outbound routing is Hermes-only;
- account/contact administration is denied;
- destructive tools are denied;
- replies to an inbound conversation may be permitted by local policy;
- proactive outbound communication requires delegated/template-authorized behavior;
- credentials remain runtime-only.

## Local voice / Home Assistant

Voice is standardized on Home Assistant's first-party Wyoming ecosystem and remains local-first:

- Speech-to-Phrase is preferred for constrained Home Assistant control phrases where appropriate;
- Whisper is preferred for general assistant speech-to-text;
- Piper is the preferred local text-to-speech engine;
- openWakeWord may be enabled as an optional wake-word service.

Raw audio retention and cloud fallback are denied by default. Transcripts and spoken responses still pass through the Hermes-only conversation topology. Voice capability does not grant additional Home Assistant control authority.

## Home Assistant MCP

Home Assistant is standardized on its first-party Model Context Protocol Server integration. The canonical endpoint is `${HOME_ASSISTANT_URL}/api/mcp`; `${HOME_ASSISTANT_URL}/api/mcp/assist` is available when the built-in Assist LLM API is explicitly preferred. Entity exposure stays least-privilege and safety-sensitive controls remain confirmation-gated.

## Epic Kanban / GitHub Projects

For repository-bound Epics, the internal `epic-kanban` provider may use GitHub Projects v2 to create the temporary Epic board, add/update work items and fields, and delete the project after accepted completion. Non-repository work uses a local ephemeral backend.

Board deletion is lifecycle-authorized only: first archive a concise completion summary, then delete the board after the Epic is accepted done. GitHub credentials remain runtime-only and the board is internal, not a new user-facing channel.

## Agent37 policy

Agent37 is a searchable index of public skills, but indexing, stars, forks, and activity are not security review. `agent37-discovery` is read-only/discovery-only. Candidate skills must be traced to their source repository and reviewed using `agent-skill-vetting` and `third-party-supply-chain-review` before any concept or executable component is adopted.

## MCP policy

Use the official MCP Registry for discovery when possible, but registry metadata alone is not sufficient to approve execution. The registry is intentionally permissive and may be in preview; review server source, transport, authentication, requested credentials, tools, network destinations, filesystem/shell access, release provenance, maintenance, and rollback path before approval.

Namespace verification is useful provenance evidence, not a guarantee that a server is appropriate or safe for Hermes.

## Review workflow

Candidate external resources should flow through the internal `integration-review-team`:

`Integration Curator -> Cybersecurity Analyst -> Systems Architect -> Team Leader`

That team may recommend a resource for registry adoption, but installation/execution still requires the local Hermes provisioner/runtime policy to permit it.
