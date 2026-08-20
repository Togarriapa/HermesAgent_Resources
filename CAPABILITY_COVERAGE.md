# Capability Coverage — v2.1 Breadth / v2.2 Effective Quality

The former capability-gap audit has been fully consumed into registry resources. This document records implemented responsibility domains rather than maintaining a speculative backlog.

**v2.1 established breadth. v2.2 hardens every indexed resource's effective operating contract through `QUALITY_POLICY.yaml`.** The quality layer does not create new expertise or permissions; it adds consistent evidence, verification, privacy, failure, observability, lifecycle, and authority-non-escalation behavior around the existing catalog.

## Product, operations, people and decisions

Profiles include Product Manager; Business Analyst / Requirements Engineer; COO / Operations Manager; People Operations / HR Specialist; Recruiter / Talent Acquisition Specialist; Privacy / GDPR Specialist; Negotiation & Conflict Resolution Specialist; Decision Scientist / Operations Research Specialist; plus CEO/CFO/CTO, Project/Agile/Scrum, analytics, research, and implementation roles.

## Household, property and resilience

Coverage includes Home Maintenance Manager with plumbing, appliance, carpentry/joinery, finishes, roofing/drainage, grounds, and home-comfort specialists; Home Fixing/Improvement; Automotive Maintenance; Home Energy/Solar; Water & Wastewater; Emergency Preparedness & Resilience; Arboriculture/Tree Care; Pest & Building Biology; smart-home/Home Assistant; and relevant engineering.

## Farm and food systems

Coverage includes Farm Planner; Home & Farm Manager; Farming; Agriculture; Homesteading; Weather; Horticulture/Orchard; Livestock Health Navigator; Farm Machinery Maintenance; garden/grounds; water/irrigation and related engineering/maintenance roles.

Livestock Health Navigator remains non-veterinary and routes diagnosis/prescribing to qualified veterinary care.

## Education, development and family

Coverage includes Curriculum Designer; Homeschooling/Homeroom; Language, History, Music, Theology, Mathematics and Science teachers; Literacy/Reading; Child Development; Special Education/SEN; Catholic family perspectives; Psychology and relevant family/routine specialists.

Child-development/SEN guidance remains non-diagnostic and safeguarding/age appropriateness remain primary constraints.

## Career, work and organizational life

Coverage includes Career Advisor; Career Development Specialist; Remote Work Manager; People Operations/HR; Recruiter/Talent Acquisition; Negotiation/Conflict Resolution; Psychology/Sociology; and management/executive roles.

## Legal, privacy, finance and commercial operations

Coverage includes Portuguese Law; International Law; EU Law/Regulatory; Portugal/EU Employment Law; Privacy/GDPR; Privacy/Security Engineering; Accountant Portugal/International; Insurance; Estate & Succession Planning Research; Procurement/Vendor Management; finance/wealth/investment managers, analysts, data and execution operators.

Legal/regulatory Profiles provide research/information within jurisdictional/professional boundaries rather than representation.

## Technology and digital systems

Coverage includes Systems Architect; Network Engineer; Site Reliability Engineer; Database Reliability Specialist; AI/ML Engineer; Cybersecurity; Privacy/Security Engineering; backend/frontend/general/web/DevOps developers; QA; Data Engineer/Data Scientist/Data Analytics; Infrastructure Manager; Homelab Operator; Home Assistant/IoT; Robotics; and electrical/mechanical engineering.

## Information quality, research and reasoning

Coverage includes Researcher; Scientific Researcher; Fact Checker / Source Verification; Media Literacy / Misinformation Analyst; Debate Analyst; Ethics Specialist; Knowledge Manager / Archivist; Philosophy; Culture; Psychology; Sociology; Anthropology; History; and evidence/source-integrity skills.

The v2.2 research overlay requires provenance, current-fact refresh where material, supporting/disconfirming evidence, and explicit uncertainty.

## Catholic specialist domain

Coverage includes Catholic Guidance; Catholic Traditional Advisor; Catholic Relationship Expert; Catholic Traditional Family Advisor; Catholic Tradition Expert; Catholic History Expert; Catholic Prayer Planner / Writer; Theology Teacher; and Portuguese, Sicilian, Spanish and German Catholic Family Advisors.

The v2.2 Catholic overlay reinforces source hierarchy and separation of binding doctrine, discipline/liturgical law, theological opinion, devotional/customary practice, and prudential judgment without impersonating clergy/ecclesiastical authority.

## Translation, architecture and digital fabrication

Coverage includes Professional European Portuguese ↔ English Translator; Building Architect; 3D Model Designer; 3D Printer Specialist; 3D Model Maker; and 3D Model Optimizer, supported by translation, architectural-planning, CAD, additive-manufacturing and printability Skills.

Building architecture remains distinct from Systems Architecture and does not imply licensed/statutory sign-off. Translation does not falsely claim sworn/certified status. Digital-fabrication capability does not automatically grant unattended machine control.

## Reusable cross-domain procedures

In addition to the large existing Skill library, reusable procedures include claim verification, negotiation preparation, scenario/sensitivity analysis, decision records, root-cause analysis, vendor comparison, privacy impact screening, emergency checklist design, cost-benefit/TCO analysis, requirements engineering, professional PT↔EN translation, architectural design planning, 3D CAD modeling, additive manufacturing and printability optimization.

Every effective Skill receives common input/precondition/procedure-shell/verification/failure/output behavior from the quality policy, but its own manifest must still contain domain-specific method content.

## Team coverage

Specialist Bundles cover product strategy, people/career, privacy/compliance, home resilience, farm reliability/planning, decision science, Catholic tradition/family, core education, architecture/fabrication, additive manufacturing, information integrity, finance/investment, software/data/infrastructure, smart home/homelab, research/writing, and other existing domains.

All Bundles are starting compositions, not recruitment ceilings. Orchestrator/Team Leader can recruit any registered Profile and multiple instances when useful.

## Completeness guarantee

`python scripts/validate_quality_v22.py` iterates every catalog resource individually, merges the universal/kind/domain quality policy with its declared manifest, and checks the effective contract for that resource kind. `materialize_effective_registry.py` provides the reference unresolved materialization used by a future provisioner/importer.

The registry can therefore remain modular and concise without allowing sparse YAML to mean undefined runtime behavior.
