# External Integration Governance

External catalogs/providers are capability sources, **not authorization sources**. A resource can be discoverable, connected, or technically callable and still be unavailable to a Profile because local Hermes policy, account scope, or explicit action authorization denies it.

## Trust tiers

Preferred evidence order for adopting an integration:

1. **First-party implementation/documentation** — preferred when available (for example Home Assistant MCP/Wyoming, GitHub APIs/MCP/Projects).
2. **Official protocol registry** — useful for provenance/discovery, followed by implementation/source review.
3. **Managed integration provider** — acceptable with explicit toolkit/tool/credential scoping, isolation, and version policy (for example Composio).
4. **Public skill/plugin index or marketplace** — discovery only until source, license, dependencies, scripts, maintainership, and requested permissions are reviewed.
5. **Unknown/unverifiable source** — do not install or execute.

Popularity, stars, listing status, namespace verification, or marketplace presence are supporting metadata—not security approval.

## Admission lifecycle

A new integration should move through explicit states:

`discovered -> provenance-reviewed -> capability/permission-reviewed -> isolated test -> approved/pinned -> deployed -> monitored -> upgraded/revoked`

Before approval, record:

- provider/source and reviewed version/digest;
- runtime/transport/network destinations;
- required credentials and account scope;
- exposed operations/tools and side effects;
- filesystem/shell/process access;
- data sent externally and retention expectations;
- timeout/rate-limit/retry behavior;
- destructive/financial/communication capabilities;
- logging/audit/redaction support;
- rollback/revocation procedure;
- responsible Profiles/Bundles allowed to request it.

## Runtime integration contract

`QUALITY_POLICY.yaml` supplies conservative defaults to every Plugin/MCP, including default-deny capability exposure, runtime-only credentials, bounded external calls, fail-closed authorization handling, redacted invocation auditing, and explicit side-effect policy.

At runtime:

- connection success does not imply operation permission;
- requested operation and target/account scope are authorized at call time;
- unlisted operations are denied;
- credentials are never returned to Profiles as text;
- rate limits are honored with bounded backoff rather than hot-loop retries;
- ambiguous partial failures are reconciled before retrying state-changing calls;
- provider request/operation IDs are retained when available for audit/idempotency;
- revoked/expired credentials fail closed and should trigger a scoped reconnection flow rather than credential guessing.

## Composio policy

The shared `composio` Plugin is default-deny. A Profile must declare explicit toolkit and tool allowlists. Connections are user-scoped; runtime credentials stay outside Git. Remote workbench, remote bash, arbitrary proxying, and unlisted toolkits are denied.

Production toolkit definitions are pinned to reviewed dated versions. Updating a pin is a dependency upgrade and should be reviewed for schema, permission, side-effect, and data-flow changes.

A Composio connection never makes a Profile user-facing or grants it all tools from the connected service.

## WhatsApp Business

WhatsApp is supported only through a supported **WhatsApp Business** connection. The registry pins the Composio WhatsApp toolkit version and allows only the messaging/history/media subset required by the Hermes channel.

Constraints:

- no personal-account automation workaround;
- inbound/outbound routing is Hermes-only;
- account/contact administration is denied;
- destructive/admin tools are denied;
- sender/chat admission follows explicit channel policy;
- proactive outbound behavior requires delegated/template-authorized handling;
- credentials remain runtime-only;
- provider message IDs should be used to correlate/deduplicate deliveries where available.

## Local voice / Home Assistant

Voice is standardized on Home Assistant's first-party Wyoming ecosystem and remains local-first:

- Speech-to-Phrase for constrained Home Assistant control language where appropriate;
- Whisper for general assistant STT;
- Piper for local TTS;
- optional openWakeWord for wake-word detection.

Raw audio retention and cloud fallback are denied by default. Voice capability does not grant additional Home Assistant control authority. Wake-word activation alone is not privileged-action authorization.

## Home Assistant MCP

Home Assistant uses its first-party MCP Server integration. Canonical endpoint: `${HOME_ASSISTANT_URL}/api/mcp`; `${HOME_ASSISTANT_URL}/api/mcp/assist` may be used when the built-in Assist LLM API is intentionally preferred.

Entity/tool exposure is least-privilege, credentials are runtime-only, and safety-sensitive controls remain confirmation/host-policy gated. The runtime should audit target entity/tool, requested operation, result, and correlation ID while avoiding secret/raw-sensitive-state logging.

## GitHub and Epic Kanban

GitHub access should use the smallest token/repository/tool scope required by the Profile or internal provider. Read-only is the default where practical; writes are explicit per task and destructive repository/project operations retain separate policy.

For repository-bound Epics, `epic-kanban` may use GitHub Projects v2. Board deletion is lifecycle-authorized only: archive the completion summary, verify Epic acceptance, then delete the ephemeral board. Project lifecycle permission does not imply repository-admin permission.

## Agent37 discovery

Agent37 remains read-only/discovery-only. Candidate resources must be traced to source and reviewed using `agent-skill-vetting` plus `third-party-supply-chain-review`. Discovery metadata never authorizes automatic installation or execution.

## MCP discovery/admission

Prefer the official MCP Registry for discovery where available, then review the actual server implementation/release. Evaluate transport, authentication, credentials, tools, roots, network access, filesystem/shell/process access, version provenance, maintenance status, data handling, and rollback.

An MCP server should expose only explicitly approved roots/tools to the requesting Profile. If a server cannot be meaningfully constrained or audited, do not deploy it merely because it implements MCP.

## Updates and revocation

Integration upgrades should be treated as permission-surface changes, not routine package bumps. Before promotion:

1. compare tool/permission/schema/network changes;
2. rerun supply-chain/provenance review where material;
3. test with non-production/least-privilege credentials where possible;
4. verify timeout/retry/idempotency behavior;
5. update pins/digests and rollback reference;
6. activate atomically and monitor initial calls.

On compromise, unexpected permission expansion, ownership change, or unsafe behavior, revoke credentials/connection first, disable the resource, preserve audit evidence, and only then investigate/re-enable.

## Review workflow

Candidate external resources flow through the internal integration review chain, typically:

`Integration Curator -> Cybersecurity Analyst -> Systems Architect -> relevant domain owner -> Team Leader/Orchestrator`

High-risk integrations may additionally recruit Privacy/GDPR, Privacy/Security Engineer, legal, financial-risk, or other relevant Profiles.

Approval for registry adoption still does not make installation/execution mandatory; the local provisioner/host policy remains authoritative.
