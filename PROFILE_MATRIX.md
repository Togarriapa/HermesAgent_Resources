# Profile-to-Skill Matrix

Profiles intentionally import only capabilities directly relevant to their role. Shared skills are reused where responsibilities genuinely overlap; the registry does not grant every profile the full skill library.

| Profile | Skills |
| --- | --- |
| Hermes | conversation-gateway |
| Orchestrator | task-decomposition, delegation-coordination, decision-routing, progress-synthesis, specialist-recruitment |
| Team Leader | delegation-coordination, meeting-facilitation, feedback-coaching, project-planning, specialist-recruitment |
| Home Assistant Optimizer | home-assistant-ops, home-assistant-config-audit, automation-optimization, entity-device-hygiene, home-energy-optimization |
| Farming Specialist | farm-operations-planning, crop-production-planning, soil-health-management, livestock-husbandry-planning, integrated-pest-management |
| Weather Analyst | meteorological-analysis, forecast-uncertainty, severe-weather-risk, microclimate-analysis |
| Agricultural Specialist | agronomic-reasoning, soil-health-management, crop-production-planning, irrigation-water-management, integrated-pest-management |
| Homesteading Specialist | homestead-systems-planning, seasonal-resilience-planning, food-preservation-safety, small-scale-water-systems, farm-operations-planning |
| Home Improvement Specialist | home-maintenance-assessment, renovation-scope-planning, building-envelope, contractor-scope-review, household-project-safety |
| Mechanical Engineer | mechanical-design, engineering-calculations, materials-selection, failure-analysis, machine-safety |
| Robotics Engineer | robotics-system-design, embedded-systems-development, control-systems, sensor-actuator-integration, robot-safety |
| Electrical Engineer | circuit-analysis, electrical-system-design, engineering-calculations, instrumentation-measurement, power-electrical-safety, electrical-code-awareness |
| Smart Home & IoT Engineer | home-assistant-ops, smart-home-architecture, mqtt-integration, zigbee-thread-matter, iot-network-security, device-lifecycle-management |
| Integration Curator | integration-discovery, third-party-supply-chain-review, mcp-server-vetting, agent-skill-vetting |
| Scientific Researcher | scientific-method, literature-review, evidence-synthesis, academic-citation, statistical-reasoning |
| Writer | prose-craft, editing-revision, source-integrity |
| Personal Trainer | fitness-programming, exercise-safety, progress-tracking |
| Life Improvement Coach | goal-setting, habit-design, reflective-review |
| Nutritionist | nutrition-planning, nutrition-evidence, dietary-tracking |
| Catholic Guidance | catholic-catechesis, magisterial-source-research, pastoral-boundaries |
| Theology Teacher | theological-method, scripture-exegesis, magisterial-source-research, lesson-design |
| Music Teacher | music-theory, ear-training, practice-design, lesson-design |
| History Teacher | historical-method, primary-source-analysis, historiography, lesson-design |
| Project Manager | project-planning, risk-management, status-reporting, meeting-facilitation |
| Systems Architect | systems-design, architecture-review, technical-documentation, threat-modeling |
| Cybersecurity Analyst | threat-modeling, security-review, incident-triage, security-hardening |
| Data Scientist | exploratory-data-analysis, statistical-reasoning, statistical-modeling, machine-learning-workflow, data-visualization |
| Data Engineer | data-pipeline-design, dimensional-data-modeling, data-quality-engineering, database-sql-engineering, data-platform-operations |
| Accountant — Portugal | double-entry-bookkeeping, financial-reporting, reconciliation-controls, portuguese-snc-accounting, portuguese-tax-compliance |
| Accountant — International | double-entry-bookkeeping, financial-reporting, reconciliation-controls, ifrs-reporting, consolidation-multicurrency, cross-border-accounting |
| UX/UI Designer & Developer | user-experience-research, interaction-design, interface-visual-design, usability-testing, design-systems, web-accessibility |
| Backend Developer | api-contract-design, backend-service-development, database-sql-engineering, secure-application-development, automated-testing |
| Frontend Developer | frontend-application-development, design-system-implementation, web-accessibility, browser-performance, automated-testing |
| DevOps Developer | ci-cd-engineering, infrastructure-as-code, container-deployment-operations, observability-engineering, release-engineering, docker-ops |
| Scrum Master | scrum-facilitation, backlog-refinement, impediment-management, team-retrospectives |
| Agile Methodology Master | agile-method-selection, flow-metrics, continuous-improvement, agile-coaching |
| QA Developer / Tester | test-strategy, automated-testing, exploratory-testing, defect-triage, release-quality |
| Personal Chef | culinary-menu-planning, cooking-techniques, food-safety, kitchen-workflow |
| Homeroom Teacher | classroom-management, learner-progress-monitoring, family-school-communication, student-safeguarding, lesson-design |
| Personal Assistant | calendar-planning, task-follow-through, correspondence-support, meeting-preparation, travel-logistics, information-organization |

## Conversation topology

The user-facing chain is strictly:

`User <-> Hermes <-> Orchestrator <-> Specialists / Teams`

Hermes is the only user-facing profile. It owns conversation intake, clarification with the user, and final response delivery. It does not directly recruit specialists; every work-bearing request goes to the Orchestrator.

The Orchestrator is internal-only. It decomposes requests, chooses the best specialist or team, recruits additional registered profiles when necessary, resolves dependencies and conflicts, and synthesizes the result before returning it to Hermes.

Team Leader is also internal-only. When recruited by the Orchestrator or used inside a team bundle, it retains `specialist-recruitment` authority and may recruit any registered profile needed for its delegated objective, but it still reports internally and never becomes a direct user endpoint.

All other specialist profiles inherit the base profile's default-deny user-contact policy. User-facing web, Telegram, and Discord channels are bound only to Hermes and must reject direct selection of any other profile.

See `TOPOLOGY.md` for the runtime enforcement contract.

## Boundary rule

A profile gains a skill only when that skill is part of the profile's normal responsibility, not merely because it might occasionally be useful. Cross-domain work is delegated to another specialist profile or explicitly composed at runtime.

Additional boundaries for the new domains:

- Farming Specialist owns practical farm operations; Agricultural Specialist owns deeper agronomic analysis; Weather Analyst owns forecast interpretation.
- Home Assistant Optimizer improves Home Assistant configuration and automation; Smart Home & IoT Engineer owns the wider protocol/network/device architecture.
- Home Improvement Specialist scopes and coordinates household projects but does not replace licensed electrical, structural, gas, or other regulated trades.
- Mechanical, Electrical, and Robotics engineers share calculations and interfaces only where their domains overlap; safety-critical certification stays with competent professionals.
- Integration Curator discovers and vets third-party resources but cannot auto-install or execute them solely because a marketplace or index lists them.
- Personal Chef handles culinary execution and food safety; nutritional targets and medical diets should be coordinated with Nutritionist.
- Scrum Master facilitates Scrum and team improvement; Team Leader retains leadership authority and Agile Methodology Master handles broader method/system design.
- QA Developer / Tester owns quality evidence and release-risk assessment but does not unilaterally replace the designated release authority.
- Homeroom Teacher supports learning and safeguarding escalation without diagnosing medical, developmental, or mental-health conditions.
- Personal Assistant organizes and prepares work but does not claim that a message, booking, or calendar change occurred unless an authorized integration actually performed it.

## Dynamic recruitment rule

Orchestrator and Team Leader are the two general leadership profiles authorized by this registry to use `specialist-recruitment`. They may recruit **any registered Profile** when task requirements justify additional expertise, capacity, independent review, or domain coverage. Recruitment is not limited to profiles already present in the active bundle or initial team.

This scope automatically covers every present and future catalogued specialist, so leadership manifests do not need editing each time the registry gains another profile.

When the selected profile is registered but not currently running, these leadership profiles may request that the Hermes provisioner instantiate it. The host remains authoritative: recruitment does not bypass local authorization, resource limits, or policy, and a recruited specialist retains its own profile-specific skills, permissions, and safety boundaries rather than inheriting the recruiter's privileges.

The default preference is the smallest competent team; specialists should be released once their assignment and required handoffs are complete.
