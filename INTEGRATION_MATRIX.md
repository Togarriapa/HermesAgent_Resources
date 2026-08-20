# Profile Integration Matrix

This audit records the intended external-tool posture for every Profile. Composio is default-deny: only explicitly listed toolkits/tools may be exposed, connections are user-isolated, and unlisted toolkits remain unavailable. User-visible communication always follows `User <-> Hermes <-> Orchestrator <-> Specialists / Teams`.

| Profile | Integration posture |
| --- | --- |
| Base | No external account integration; internal-only defaults. |
| Hermes | Sole gateway; local voice-pipeline for STT/TTS plus six-section response composition; no specialist/account-tool expansion. |
| Orchestrator | Internal coordination + `epic-kanban` + adaptive internal deliberation; no blanket user-account toolkit. |
| Team Leader | Internal leadership/recruitment/deliberation; no blanket external-account toolkit. |
| Resource Evolution Manager | GitHub read/update discovery plus private local `resource-overlay-store`; private learned overlays never sync/export. |
| Developer | Codex + GitHub + filesystem/GitHub MCP. |
| Backend Developer | Scoped technical code toolchain; no generic SaaS expansion. |
| Frontend Developer | Scoped technical code toolchain; no generic SaaS expansion. |
| DevOps Developer | Scoped deployment/operations toolchain; no generic SaaS-account expansion. |
| Website Developer | Codex + GitHub + filesystem; recruit specialist web roles for depth/parallel work. |
| UX/UI Designer & Developer | Scoped design/development capability; no account toolkit required by default. |
| QA Developer / Tester | Scoped testing capability; no account toolkit required by default. |
| Systems Architect | Architecture/research capability; implementation delegated to specialists. |
| Cybersecurity Analyst | Defensive review on authorized systems only; no broad credential aggregator. |
| Infrastructure Manager | Management/governance only by default; implementation access delegated to DevOps/Homelab/etc. |
| Homelab Operator | Filesystem + official Home Assistant MCP with least-privilege entity exposure. |
| Home Assistant Optimizer | Web + official Home Assistant MCP; safety-sensitive control remains confirmation-gated. |
| Smart Home & IoT Engineer | Codex/filesystem + official Home Assistant MCP; no generic smart-home cloud marketplace access. |
| Mechanical Engineer | Web/standards research; no physical-execution integration by default. |
| Electrical Engineer | Web/standards research; no remote electrical-control capability by default. |
| Robotics Engineer | Codex/filesystem + web research; physical execution remains host-authorized and safety bounded. |
| Data Scientist | Codex/filesystem + Composio Sheets/Drive read-oriented access; writes denied by default. |
| Data Engineer | Codex/filesystem + controlled Composio Sheets/Drive; writes delegated-only, deletes denied. |
| Data Analytics Specialist | Codex + filesystem + web for reproducible business analytics; no blanket SaaS write access, and source-system writes remain delegated to Data Engineer/authorized integrations. |
| Researcher | Web + GitHub research; no account-write integration. |
| Scientific Researcher | Web/evidence tooling; no account-write integration. |
| Product Research Specialist | Web research; no commerce/account-write integration by default. |
| Investment Research Analyst | Web/current-source investment research only; no direct financial-account credentials or execution plugin. |
| Equity Analyst | Web/filings/current market-source research only; no direct securities-order execution. |
| Fixed Income Analyst | Web/issuer/central-bank/current-source research only; no direct bond/fund/derivative execution. |
| Macroeconomic Analyst | Web + official statistical/central-bank sources; no account integration. |
| Quantitative Investment Analyst | Codex + filesystem + web for models/reproducible research; no direct live trading connection. |
| Investment Risk Analyst | Web/current-source independent risk review; no direct execution authority. |
| Crypto Asset Analyst | Web/current protocol/market research; no exchange/wallet signing credentials. |
| Blockchain Researcher | Web + GitHub protocol/source research; production signing delegated; may recruit Crypto Sandbox Operator for testnet experiments. |
| Real Estate Investment Analyst | Web/property-market research; no transaction, title, deposit, financing or payment execution. |
| Financial Data Steward | `financial-data-hub` read-only aggregation for Revolut/BPI/moey via regulated AISP, Trading 212 read key, Pionex `Read` key, and Ledger `account.list`; raw credentials hidden. |
| Financial Execution Operator | `financial-execution-gateway` write-capable for supported bank PISP payment initiation, Trading 212 live orders/cancellation, Pionex `Trade` orders/cancellation, and Ledger transaction signing; **explicit user order + fresh one-shot confirmation required for every action**. |
| Crypto Live Wallet Operator | `agent-live-wallet`; dedicated real-value wallet, host-isolated keys, configured mainnet allowlist; may prepare transactions autonomously but sign/broadcast only from an explicit user order + fresh confirmation. |
| Crypto Sandbox Operator | `agent-sandbox-wallet`; autonomous Ethereum Sepolia/Solana Devnet testnet execution using faucet/test assets only; mainnet and real-value assets denied. |
| Writer | Composio Google Docs + Drive; document writes delegated-only. |
| Project Manager | Composio Calendar, Tasks, Docs, Drive; writes delegated-only, deletes/permission changes denied. |
| Scrum Master | Facilitation/process skills only; no account integration by default. |
| Agile Methodology Master | Method/process analysis only; no account integration by default. |
| Remote Work Manager | Web research plus internal productivity/operating-model analysis; no employee-surveillance toolkit and no automatic access to employer systems. |
| Career Advisor | Web/current labor-market research; no application submission, employer-account, reference-contact, or recruiter impersonation integration by default. |
| Career Development Specialist | Web/current labor-market and learning research; no employer HR-system or credential-issuing access by default. |
| CEO | Strategic/organizational profile; no blanket account integrations. |
| CFO | Composio Google Sheets + Drive with delegated writes, no deletes/permission changes; statutory accounting/tax/legal delegated. |
| CTO | Technology strategy/governance profile; no blanket execution toolkit. |
| Financial Advisor | Web/current-source planning research; may consume normalized financial data through Financial Data Steward; execution must be separately routed through Financial Execution Operator. |
| Wealth Manager | Web/current-source wealth planning + normalized financial data when recruited; no raw account credentials and no direct transaction plugin. |
| Portfolio Manager | Web/current-source portfolio research + normalized holdings; may propose orders/rebalancing but execution is isolated to Financial Execution Operator after user authorization. |
| Asset Manager | Web/current-source manager/asset oversight + normalized financial data; subscriptions/redemptions/custody actions are not direct capabilities. |
| Stocks Manager | Web/current-source equity research + normalized Trading 212 observations; may propose trades, but live order execution is isolated to Financial Execution Operator. |
| Cryptocurrency Manager | Web/current-source digital-asset research + normalized Pionex/Ledger/live-wallet observations; may propose actions, but real-value execution is isolated to the execution/live-wallet operators. |
| Real Estate Manager | Web/current property/market research; no purchase/sale/lease/financing/deposit/title/payment execution. |
| Accountant — Portugal | Web + Composio Sheets/Drive; controlled writes, no deletes/permission changes; current Portuguese authority verification required. |
| Accountant — International | Web + Composio Sheets/Drive; controlled writes, no deletes/permission changes; current framework/jurisdiction verification required. |
| Portuguese Law Specialist | Web authoritative legal-source research only; no account writes or legal representation tooling. |
| International Law Specialist | Web treaty/institution/jurisdiction research only; no account writes or legal representation tooling. |
| Philosophy Specialist | Web/source research only; no external-account write capability. |
| Culture Expert | Web/current and historical cultural-source research; no account-write integration. |
| Psychology Expert | Web/scientific literature research only; no health-record access, diagnosis tool, clinical-treatment integration, or direct patient-care capability. |
| Sociology Expert | Web/research-source analysis; no account-write integration. |
| Anthropology Expert | Web/research-source analysis; no field-subject tracking or personal-data collection integration by default. |
| Debate Analyst | Internal reasoning/debate role only; no external account integration and no user-facing channel. |
| Language Teacher | Local `voice-pipeline` for pronunciation/listening practice; no external learner account integration by default. |
| Curriculum Designer | No external account integration by default; recruits subject specialists as needed. |
| Homeschooling Specialist | Web curriculum/resource research; jurisdiction-specific law delegated to Law Specialist. |
| Homeroom Teacher | Composio Classroom read, Calendar read, Docs drafting; classroom writes/direct family contact denied by default. |
| History Teacher | Web/source research; no external account tools. |
| Music Teacher | Teaching skills only; no account integration by default. |
| Theology Teacher | Authoritative-source web research; no external account tools. |
| Catholic Guidance | Authoritative-source web research; no external account tools. |
| Catholic Traditional Advisor | Authoritative Catholic/liturgical web research; no external account tools. |
| Portuguese Catholic Family Advisor | Web + authoritative Catholic/Portuguese contextual research; no family-account, communications, or household-control integration. |
| Sicilian Catholic Family Advisor | Web + authoritative Catholic/Sicilian contextual research; no family-account, communications, or household-control integration. |
| Spanish Catholic Family Advisor | Web + authoritative Catholic/Spanish contextual research; no family-account, communications, or household-control integration. |
| German Catholic Family Advisor | Web + authoritative Catholic/German contextual research; no family-account, communications, or household-control integration. |
| Personal Trainer | Training guidance only; no health-record integration by default. |
| Nutritionist | General nutrition guidance only; no health-record integration by default. |
| Personal Chef | Culinary planning only; no grocery/commerce transaction tools by default. |
| Life Improvement Coach | Coaching skills only; no behavioral-tracking account integration by default. |
| Personal Assistant | Web + Composio Calendar, Gmail read/draft, Drive read, Google Tasks; email sending/deletes denied by default. |
| Farming Specialist | Web research; recruits Weather/Agronomy profiles instead of receiving broad account access. |
| Agricultural Specialist | Web research; no pesticide/vendor-marketplace execution integration. |
| Weather Analyst | Web + Composio HERE weather only; read-only weather tools. |
| Homesteading Specialist | Web research; delegates engineering/weather/nutrition work. |
| Home Improvement Specialist | Web research; regulated engineering/trade questions delegated. |
| Home Fixing Specialist | Web manuals/product/repair research; no remote utility-control access. |
| Home Maintenance Manager | Web manuals/maintenance research and internal planning; no remote utility-control or contractor-payment authority. |
| Plumbing Maintenance Specialist | Web/manual research only; no utility-account control or regulated plumbing/gas execution capability. |
| Appliance Maintenance Specialist | Web/model-manual research only; no remote mains/gas/refrigerant execution capability. |
| Carpentry & Joinery Specialist | Web/manual/material research; no contractor purchasing or structural execution authority. |
| Painting & Finishes Specialist | Web/product/manual research; no purchasing or hazardous-material handling authority. |
| Roofing & Drainage Specialist | Web/building research; no work-at-height execution or contractor-payment authority. |
| Garden & Grounds Maintenance Specialist | Web/seasonal research; no pesticide purchasing/application or powered-equipment remote control. |
| Home Comfort Maintenance Specialist | Web/model research; no refrigerant/gas/high-voltage service authority; Home Assistant control remains delegated to HA profiles. |
| Home & Farm Manager | Composio Calendar + Tasks with delegated writes; deletes denied; purchasing/external communication not implied. |
| Integration Curator | Web + GitHub + official MCP Registry + Agent37 discovery; discovery/review only, no auto-install/execute. |
| Skills Analyser | GitHub + filesystem for registry/task evidence analysis; private user data may not be exported. |
| Skills Reviewer | GitHub + filesystem for code/resource review; no execution authority implied. |
| Skills Improver | Codex + GitHub + filesystem for reviewed versioned improvements; private user learning may not be published. |
| Improvement Manager | Improvement portfolio/governance; no blanket external integration. |

## Financial account and execution architecture

Read and write capabilities are deliberately separated by credential and role.

- **Banks (Revolut/BPI/moey):** read through a regulated AISP; payment initiation through a regulated PISP adapter where institution coverage permits. Direct password/PIN/MFA scraping is denied.
- **Trading 212:** one read-only key plus a separate live execution key with the minimum order permission and IP restriction. Live Market/Limit/Stop/Stop-Limit orders and cancellation are available only behind the explicit-order gateway.
- **Pionex:** separate `Read` and `Trade` keys; the Trade key is restricted to order placement/cancellation, with withdrawals/transfers denied.
- **Ledger:** read via `account.list`; write via `transaction.sign`/`transaction.signAndBroadcast`, with both the Hermes authorization envelope and Ledger hardware/on-device confirmation. Arbitrary message signing stays denied by default.
- **Hermes live wallet:** a separate host-isolated real-value wallet, never derived from the user's Ledger. It may receive assets and prepare transactions, but any mainnet signing/broadcast requires explicit order + fresh confirmation.
- **Hermes sandbox wallet:** autonomous testnet-only execution using faucet/test assets.

A recommendation, target allocation, scheduled task, prior order, user preference, or past confirmation never becomes standing transaction authority.

## Deliberation and response architecture

Deliberation is an internal capability, not an external integration. Orchestrator/Team Leader may recruit multiple independent profiles and Debate Analyst, but no extra user-facing endpoint is created. Contributor profile names, summarized material dissent, and required permissions are returned to Hermes for the canonical six-section response.

## User-facing channels

| Channel | Integration posture |
| --- | --- |
| Web | Hermes-only; upstream authentication required; direct profile selection denied. |
| Telegram | Hermes-only; allowed-chat list; unknown chats denied. |
| Discord | Hermes-only; allowed-guild list; unknown guilds denied. |
| WhatsApp | **WhatsApp Business only** via pinned Composio `whatsapp@20260721_00`; Hermes-only; account/contact administration and destructive tools denied; proactive outbound delegated/template-only. |
| Voice | Local-first Home Assistant/Wyoming pipeline: Speech-to-Phrase for constrained home control, Whisper for general STT, Piper for TTS, optional openWakeWord; Hermes-only; no cloud fallback or raw-audio retention by default. |

## Runtime-only infrastructure integrations

- `epic-kanban` may use GitHub Projects v2 for repository-backed Epics and local ephemeral boards otherwise. It is internal-only and deletes boards only as part of the accepted-Epic lifecycle after archiving a completion summary.
- `resource-overlay-store` is local/private, owner-only, denies Git sync/network export, and preserves version history for experiential and user-learned overlays.
- `daily-resource-reconcile` uses the Resource Evolution Manager to retrieve upstream registry changes while preserving local overlay layers.
- `financial-data-hub` normalizes read-only observations while hiding provider credentials from Profiles.
- `financial-execution-gateway` exposes write adapters but requires a one-shot explicit user order and fresh confirmation for every real-money action.
- `agent-live-wallet` is real-value and confirmation-gated; `agent-sandbox-wallet` is autonomous but testnet-only.

## External-source policy

- **Home Assistant:** prefer official first-party MCP and Wyoming integrations.
- **MCP:** use the official MCP Registry for discovery, then review source and permissions before approval.
- **Composio:** managed provider with explicit per-profile/channel toolkit/tool allowlists and pinned production versions.
- **Agent37:** discovery index only; trace candidates to source and review before adoption.
- **WhatsApp:** use supported WhatsApp Business integration only; no personal-account automation workaround.
- **Financial integrations:** separate data credentials, execution credentials, decision roles and execution roles; secrets remain host-managed and transactions are explicit-order-only.
- **Focused v2 specialists:** web/tool access stays narrow; cultural, psychological, career, home-maintenance, and deliberation roles do not inherit unrelated account/control permissions.
- A popular or listed integration is not automatically trusted; local Hermes policy remains authoritative.
