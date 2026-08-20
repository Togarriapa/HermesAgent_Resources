# Profile-to-Skill Matrix

Profiles intentionally import only capabilities that are directly relevant to their role. Shared skills are reused where responsibilities genuinely overlap; the registry does not grant every profile the full skill library.

| Profile | Skills |
| --- | --- |
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

## Boundary rule

A profile should gain a new skill only when that skill is part of the profile's normal responsibility, not merely because it might occasionally be useful. Cross-domain work should be delegated to another specialist profile or explicitly composed at runtime.

## Dynamic recruitment rule

Orchestrator and Team Leader are the two general leadership profiles authorized by this registry to use `specialist-recruitment`. They may recruit **any registered Profile** when task requirements justify additional expertise, capacity, independent review, or domain coverage. Recruitment is not limited to profiles already present in the active bundle or initial team.

When the selected profile is registered but not currently running, these leadership profiles may request that the Hermes provisioner instantiate it. The host remains authoritative: recruitment does not bypass local authorization, resource limits, or policy, and a recruited specialist retains its own profile-specific skills, permissions, and safety boundaries rather than inheriting the recruiter's privileges.

The default preference is the smallest competent team; specialists should be released once their assignment and required handoffs are complete.
