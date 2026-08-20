# Profile Integration Matrix

This audit records the intended external-tool posture for every Profile. `Composio` is default-deny: only the explicitly listed toolkits/tools may be exposed to a profile, connections are user-isolated, and unlisted toolkits remain unavailable. User-visible communication always follows `User <-> Hermes <-> Orchestrator <-> Specialists / Teams`.

| Profile | Integration posture |
| --- | --- |
| Base | No external account integration; internal-only defaults. |
| Hermes | User-facing gateway only; no specialist/account toolkit expansion. |
| Orchestrator | Coordination/recruitment only; delegates tool-bearing work to specialists. |
| Team Leader | Internal leadership/recruitment only; no blanket external-account toolkit. |
| Personal Assistant | Web + Composio: Google Calendar, Gmail draft/read, Drive read, Google Tasks; sending/deletes denied by default. |
| Project Manager | Composio: Calendar, Tasks, Docs, Drive; writes delegated-only, deletes/permission changes denied. |
| Writer | Composio: Google Docs + Drive; document writes delegated-only. |
| Data Scientist | Codex/filesystem plus Composio Sheets/Drive read-oriented access; writes denied by default. |
| Data Engineer | Codex/filesystem plus Composio Sheets/Drive; writes delegated-only, deletes denied. |
| Accountant — Portugal | Web + Composio Sheets/Drive; controlled writes, no deletes/permission changes; authoritative Portuguese source verification remains required. |
| Accountant — International | Web + Composio Sheets/Drive; controlled writes, no deletes/permission changes; framework/jurisdiction verification remains required. |
| Homeroom Teacher | Composio Classroom read, Calendar read, Docs drafting; classroom writes and direct family contact denied by default. |
| Home Assistant Optimizer | Web + official Home Assistant MCP, least-privilege exposed entities. |
| Smart Home & IoT Engineer | Codex/filesystem + official Home Assistant MCP; no generic smart-home cloud marketplace access. |
| Homelab Operator | Filesystem + official Home Assistant MCP; no Composio expansion. |
| Weather Analyst | Web + Composio HERE weather only; read-only weather tools, no writes. |
| Integration Curator | Web + GitHub + official MCP Registry + Agent37 discovery; discovery/review only, no auto-install or auto-execute. |
| Robotics Engineer | Codex/filesystem + web research; physical execution remains locally authorized and safety bounded. |
| Electrical Engineer | Web/standards research only; no remote control of electrical equipment by default. |
| Mechanical Engineer | Web/standards research only; no physical execution integration by default. |
| Farming Specialist | Web research; recruits Weather/Agronomy specialists rather than receiving broad external account access. |
| Agricultural Specialist | Web research; no pesticide/vendor marketplace execution integrations. |
| Homesteading Specialist | Web research; delegates engineering/weather/nutrition tasks to specialists. |
| Home Improvement Specialist | Web research; delegates regulated engineering/trade questions to specialists. |
| Developer | Existing scoped code/GitHub/filesystem toolchain; no Composio addition. |
| Backend Developer | Existing scoped technical toolchain; no Composio addition. |
| Frontend Developer | Existing scoped technical toolchain; no Composio addition. |
| DevOps Developer | Existing scoped deployment/operations toolchain; no generic SaaS-account expansion. |
| UX/UI Designer & Developer | Existing scoped design/development capabilities; no external-account toolkit required by default. |
| QA Developer / Tester | Existing scoped test toolchain; no external-account toolkit required by default. |
| Systems Architect | Architecture/research capabilities only; recruits implementation specialists for execution. |
| Cybersecurity Analyst | Defensive review only on authorized systems; no broad credential aggregator. |
| Researcher | Web/GitHub research where defined; no account-write integration. |
| Scientific Researcher | Web/evidence tooling where defined; no account-write integration. |
| Scrum Master | Facilitation/process skills only; no account integration by default. |
| Agile Methodology Master | Method/process analysis only; no account integration by default. |
| Catholic Guidance | Authoritative-source web research where defined; no external account tools. |
| Theology Teacher | Authoritative-source web research where defined; no external account tools. |
| History Teacher | Web/source research where defined; no external account tools. |
| Music Teacher | Teaching skills only; no account integration by default. |
| Personal Trainer | Training guidance only; no health-account integration by default. |
| Nutritionist | General nutrition guidance only; no health-record integration by default. |
| Personal Chef | Culinary planning only; no grocery/commerce transaction tools by default. |
| Life Improvement Coach | Coaching skills only; no behavioral-tracking account integration by default. |

## External-source policy

- **Home Assistant:** use the official first-party MCP Server integration.
- **MCP:** use the official MCP Registry for discovery, then review source and permissions before approval.
- **Composio:** useful managed provider, but profile sessions must use explicit toolkit/tool allowlists and pinned production versions.
- **Agent37:** discovery index only. Every candidate skill must be traced to its source and reviewed before adoption.
- A popular integration is not automatically a trusted integration; local Hermes policy remains authoritative.
