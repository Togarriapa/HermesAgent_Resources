# Hermes Conversation Topology

The canonical conversational topology is:

`User <-> Hermes <-> Orchestrator <-> Specialist profiles / Team bundles`

## Single point of contact

`hermes` is the only profile permitted to bind to user-facing channels or communicate directly with the end user. All other profiles inherit an internal-only interaction default from `base`.

A user-facing channel must:

- route inbound messages to `hermes`;
- reject or ignore attempts to select another profile directly;
- only deliver outbound user-visible responses through `hermes`;
- route scheduled notifications, webhook outcomes, alerts, and follow-up results through `hermes` when they are intended for the user.

## Hermes responsibilities

Hermes owns conversation intake and final delivery, not specialist execution. It preserves the request, constraints, relevant context, and response requirements, then hands the work-bearing request to `orchestrator`.

Hermes does not directly recruit specialists. The Orchestrator owns decomposition, routing, recruitment, team composition, conflict resolution, and synthesis.

If more information is required, the Orchestrator returns a clarification request to Hermes. Hermes asks the user and sends the answer back into the same orchestration flow.

## Orchestrator responsibilities

The Orchestrator accepts user-originating work only through Hermes. It may recruit any registered specialist profile or suitable team bundle under the registry's `specialist-recruitment` rules, including profiles outside the initial bundle or current roster.

Specialists report to the Orchestrator, not directly to the user. The Orchestrator synthesizes their outputs and returns the result to Hermes.

## Specialist responsibilities

Specialist profiles are internal execution roles. They may collaborate with other internal profiles when routed by the Orchestrator or an authorized Team Leader, but they must not bind directly to user channels or initiate user-facing conversation.

Their expertise can be represented in the final answer, but the conversational identity presented to the user remains Hermes.

## Authority and security

Conversation topology does not expand permissions. Hermes cannot grant Orchestrator or specialists capabilities that local Hermes host policy denies. Recruitment likewise does not transfer the recruiter's privileges to a recruited profile.

The runtime/provisioner should enforce this topology structurally rather than relying only on prompt instructions. In particular, direct profile addressing from user channels should fail closed unless the target profile is `hermes`.
