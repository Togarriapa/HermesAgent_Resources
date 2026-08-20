# Hermes Conversation Topology

The canonical conversational topology is:

`User <-> Hermes <-> Orchestrator <-> Specialist profiles / Team bundles`

The transport may be text or audio, but the conversational identity and routing do not change.

## Single point of contact

`hermes` is the only profile permitted to bind to user-facing channels or communicate directly with the end user. All other profiles inherit an internal-only interaction default from `base`.

Current user-facing channels are:

- web;
- Telegram;
- Discord;
- WhatsApp Business;
- local voice/audio.

Every user-facing channel must:

- route inbound messages or transcripts to `hermes`;
- reject attempts to select another profile directly;
- deliver outbound user-visible text or speech only through `hermes`;
- route scheduled notifications, webhook outcomes, alerts, and follow-up results through `hermes` when intended for the user.

WhatsApp does not turn the Personal Assistant or another profile into a direct contact. Voice does not turn Home Assistant Optimizer or Smart Home & IoT Engineer into a voice endpoint.

## Hermes responsibilities

Hermes owns conversation intake, modality handling, clarification, and final delivery—not specialist execution. It preserves the request, constraints, relevant context, input modality, and output requirements, then hands the work-bearing request to `orchestrator`.

For voice:

`Audio -> STT -> Hermes -> Orchestrator -> ... -> Hermes -> TTS -> Audio`

For WhatsApp:

`WhatsApp Business -> Hermes -> Orchestrator -> ... -> Hermes -> WhatsApp Business`

Hermes does not directly recruit specialists. The Orchestrator owns decomposition, routing, recruitment, team composition, parallelism, conflict resolution, and synthesis.

If more information is required, the Orchestrator returns a clarification request to Hermes. Hermes asks the user through the active channel and sends the answer back into the same orchestration flow.

## Orchestrator responsibilities

The Orchestrator accepts user-originating work only through Hermes. It may recruit any registered specialist profile or suitable team bundle, including profiles outside the initial bundle or current roster.

It may also:

- run dependency-independent work packages concurrently;
- create multiple instances of the same profile when capacity is useful;
- delegate branches of an Epic to Team Leaders and nested subteams;
- maintain the Epic dependency graph and ephemeral Kanban;
- reconcile parallel results before returning a synthesized outcome.

Nested orchestration does not change the user-facing route. Deep internal results still flow upward to the Orchestrator and then to Hermes.

## Specialist responsibilities

Specialist profiles are internal execution roles. They may collaborate with other internal profiles when routed by the Orchestrator or an authorized Team Leader, but they must not bind directly to user channels or initiate user-facing conversation.

Their expertise can be represented in the final answer, but the conversational identity presented to the user remains Hermes.

## WhatsApp constraints

WhatsApp support is limited to a supported WhatsApp Business integration. Personal-account automation is not an accepted routing path. Account administration, contact administration, and destructive actions are denied by default. Proactive outbound communication requires separately delegated/template-authorized behavior.

## Voice constraints

Voice is local-first through the Home Assistant/Wyoming pipeline. Raw audio is not retained by default and cloud fallback is denied. Speech transcription enters Hermes like any other input; spoken output is generated only from the Hermes response. Safety-sensitive Home Assistant actions retain their normal authorization/confirmation requirements.

## Authority and security

Conversation topology does not expand permissions. Hermes cannot grant Orchestrator or specialists capabilities that local Hermes host policy denies. Recruitment and multiple profile instances do not transfer or multiply authority.

The runtime/provisioner must enforce this topology structurally rather than relying only on prompt instructions. Direct profile addressing from user channels fails closed unless the target profile is `hermes`.
