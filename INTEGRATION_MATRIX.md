# Profile Integration Matrix

This audit records the intended external-tool posture for every Profile. Composio is default-deny: only explicitly listed toolkits/tools may be exposed, connections are user-isolated, and unlisted toolkits remain unavailable. User-visible communication always follows `User <-> Hermes <-> Orchestrator <-> Specialists / Teams`.

| Profile | Integration posture |
| --- | --- |
| Base | No external account integration; internal-only defaults. |
| Hermes | Sole gateway; local voice-pipeline for STT/TTS; no specialist/account-tool expansion. |
| Orchestrator | Internal coordination + `epic-kanban`; no blanket user-account toolkit. |
| Team Leader | Internal leadership/recruitment; no blanket external-account toolkit. |
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
| Researcher | Web + GitHub research; no account-write integration. |
| Scientific Researcher | Web/evidence tooling; no account-write integration. |
| Product Research Specialist | Web research; no commerce/account-write integration by default. |
| Investment Research Analyst | Web/current-source investment research only; no broker, exchange, wallet, bank, property-purchase or custody integration. |
| Equity Analyst | Web/filings/current market-source research only; no securities-order execution. |
| Fixed Income Analyst | Web/issuer/central-bank/current-source research only; no bond/fund/derivative execution. |
| Macroeconomic Analyst | Web + official statistical/central-bank sources; no account integration. |
| Quantitative Investment Analyst | Codex + filesystem + web for models/reproducible research; no live trading connection. |
| Investment Risk Analyst | Web/current-source independent risk review; no execution authority. |
| Crypto Asset Analyst | Web/current protocol/market research; no exchange/wallet transaction access and no secrets handling. |
| Blockchain Researcher | Web + GitHub protocol/source research; no wallet signing, key access, bridging or on-chain execution. |
| Real Estate Investment Analyst | Web/property-market research; no transaction, title, deposit, financing or payment execution. |
| Writer | Composio Google Docs + Drive; document writes delegated-only. |
| Project Manager | Composio Calendar, Tasks, Docs, Drive; writes delegated-only, deletes/permission changes denied. |
| Scrum Master | Facilitation/process skills only; no account integration by default. |
| Agile Methodology Master | Method/process analysis only; no account integration by default. |
| CEO | Strategic/organizational profile; no blanket account integrations. |
| CFO | Composio Google Sheets + Drive with delegated writes, no deletes/permission changes; statutory accounting/tax/legal delegated. |
| CTO | Technology strategy/governance profile; no blanket execution toolkit. |
| Financial Advisor | Web/current-source planning research; no broker/product-purchase/account-opening integration; regulated personal advice boundaries remain explicit. |
| Wealth Manager | Web/current-source wealth planning; no custody, transfer, broker or account-administration execution. |
| Portfolio Manager | Web/current-source portfolio research; recommendations/rebalancing plans only, no order routing/execution. |
| Asset Manager | Web/current-source manager/asset oversight; no subscriptions, redemptions, custody, transfers or trading execution. |
| Stocks Manager | Web/current-source equity research; no securities order placement, modification or cancellation. |
| Cryptocurrency Manager | Web/current-source digital-asset research; no exchange trading, swaps, staking, bridging, transfer, approval or wallet signing. |
| Real Estate Manager | Web/current property/market research; no purchase/sale/lease/financing/deposit/title/payment execution. |
| Accountant — Portugal | Web + Composio Sheets/Drive; controlled writes, no deletes/permission changes; current Portuguese authority verification required. |
| Accountant — International | Web + Composio Sheets/Drive; controlled writes, no deletes/permission changes; current framework/jurisdiction verification required. |
| Portuguese Law Specialist | Web authoritative legal-source research only; no account writes or legal representation tooling. |
| International Law Specialist | Web treaty/institution/jurisdiction research only; no account writes or legal representation tooling. |
| Language Teacher | Local `voice-pipeline` for pronunciation/listening practice; no external learner account integration by default. |
| Curriculum Designer | No external account integration by default; recruits subject specialists as needed. |
| Homeschooling Specialist | Web curriculum/resource research; jurisdiction-specific law delegated to Law Specialist. |
| Homeroom Teacher | Composio Classroom read, Calendar read, Docs drafting; classroom writes/direct family contact denied by default. |
| History Teacher | Web/source research; no external account tools. |
| Music Teacher | Teaching skills only; no account integration by default. |
| Theology Teacher | Authoritative-source web research; no external account tools. |
| Catholic Guidance | Authoritative-source web research; no external account tools. |
| Catholic Traditional Advisor | Authoritative Catholic/liturgical web research; no external account tools. |
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
| Home & Farm Manager | Composio Calendar + Tasks with delegated writes; deletes denied; purchasing/external communication not implied. |
| Integration Curator | Web + GitHub + official MCP Registry + Agent37 discovery; discovery/review only, no auto-install/execute. |
| Skills Analyser | GitHub + filesystem for registry/task evidence analysis; private user data may not be exported. |
| Skills Reviewer | GitHub + filesystem for code/resource review; no execution authority implied. |
| Skills Improver | Codex + GitHub + filesystem for reviewed versioned improvements; private user learning may not be published. |
| Improvement Manager | Improvement portfolio/governance; no blanket external integration. |

## Investment-domain execution boundary

The financial/investment profiles are intentionally **research, planning, analysis and recommendation** capabilities. None receives a broker, bank, exchange, wallet-signing, custody, money-transfer, property-closing, financing, or purchase/sale execution integration from this registry version.

Future transaction-capable integrations must be introduced as separate reviewed resources with explicit authorization, account scoping, confirmation, audit, limits, rollback/compensation where possible, and jurisdiction/provider review. Adding a market-data or portfolio-data connector must not silently grant trading authority.

Digital-asset profiles must never request, store, log or transmit private keys, seed phrases, recovery codes, signing secrets or equivalent credentials.

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

## External-source policy

- **Home Assistant:** prefer official first-party MCP and Wyoming integrations.
- **MCP:** use the official MCP Registry for discovery, then review source and permissions before approval.
- **Composio:** managed provider with explicit per-profile/channel toolkit/tool allowlists and pinned production versions.
- **Agent37:** discovery index only; trace candidates to source and review before adoption.
- **WhatsApp:** use supported WhatsApp Business integration only; no personal-account automation workaround.
- **Investment data/execution:** research connectors must be separated from transaction authority; broker/exchange/wallet/custody execution remains absent by default.
- A popular or listed integration is not automatically trusted; local Hermes policy remains authoritative.
