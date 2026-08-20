# Profile-to-Skill Matrix

Profiles intentionally import only capabilities that are directly relevant to their role. Shared skills are reused where responsibilities genuinely overlap; the registry does not grant every profile the full skill library.

| Profile | Skills |
| --- | --- |
| Hermes | conversation-gateway |
| Orchestrator | task-decomposition, delegation-coordination, decision-routing, progress-synthesis, specialist-recruitment |
| Scientific Researcher | scientific-method, literature-review, evidence-synthesis, academic-citation, statistical-reasoning |
| Writer | prose-craft, editing-revision, source-integrity |
| Team Leader | delegation-coordination, meeting-facilitation, feedback-coaching, project-planning, specialist-recruitment |
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

A profile should gain a new skill only when that skill is part of the profile's normal responsibility, not merely because it might occasionally be useful. Cross-domain work should be delegated to another specialist profile or explicitly composed at runtime.

Examples of intentional boundaries:

- Personal Chef handles culinary execution and food safety; nutritional targets and medical diets should be coordinated with Nutritionist rather than turning the chef into a nutrition clinician.
- Scrum Master facilitates Scrum and team improvement; Team Leader retains leadership authority and Agile Methodology Master handles broader method/system design.
- UX/UI Designer & Developer owns user-centered interface design and implementation-aware design systems; Frontend Developer owns application implementation and runtime behavior.
- QA Developer / Tester owns quality evidence and release-risk assessment but does not unilaterally replace the designated release authority.
- Homeroom Teacher supports learning and safeguarding escalation without diagnosing medical, developmental, or mental-health conditions.
- Personal Assistant organizes and prepares work but does not claim that a message, booking, or calendar change occurred unless an authorized integration actually performed it.

## Dynamic recruitment rule

Orchestrator and Team Leader are the two general leadership profiles authorized by this registry to use `specialist-recruitment`. They may recruit **any registered Profile** when task requirements justify additional expertise, capacity, independent review, or domain coverage. Recruitment is not limited to profiles already present in the active bundle or initial team.

This scope automatically covers all present and future catalogued specialists, including Data Scientist, Data Engineer, both Accountant profiles, UX/UI Designer & Developer, Backend Developer, Frontend Developer, DevOps Developer, Scrum Master, Agile Methodology Master, QA Developer / Tester, Personal Chef, Homeroom Teacher, and Personal Assistant. Leadership manifests therefore do not need to be edited every time the registry gains another specialist.

When the selected profile is registered but not currently running, these leadership profiles may request that the Hermes provisioner instantiate it. The host remains authoritative: recruitment does not bypass local authorization, resource limits, or policy, and a recruited specialist retains its own profile-specific skills, permissions, and safety boundaries rather than inheriting the recruiter's privileges.

The default preference is the smallest competent team; specialists should be released once their assignment and required handoffs are complete.
