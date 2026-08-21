#!/usr/bin/env python3
from __future__ import annotations

from registry_lib import ROOT, catalog, discover_resources, load_yaml, names_by_kind

EXPECTED_PROFILES = {
    "hermesagent-expert", "ai-developer", "ai-systems-architect", "ai-prompt-engineer", "ai-agent-orchestration-engineer", "ai-evaluation-engineer", "llmops-engineer", "ai-safety-reliability-engineer", "ai-knowledge-engineer",
    "traditional-remedies-researcher", "herbalism-ethnobotany-researcher", "historical-materia-medica-researcher", "natural-lifestyle-health-educator", "traditional-foodways-health-researcher",
    "amish-remedies-expert", "amish-lifestyle-expert", "amish-construction-expert", "amish-farming-expert", "amish-housekeeping-expert", "amish-cook-expert", "amish-food-preservation-expert",
    "ancient-traditional-remedies-expert", "ancient-lifestyle-expert", "ancient-building-traditions-expert", "ancient-agriculture-expert", "ancient-housekeeping-domestic-life-expert", "ancient-cook-foodways-expert", "ancient-food-preservation-expert", "ancient-crafts-material-culture-expert",
    "traditional-latin-mass-expert", "roman-rite-liturgical-traditions-expert", "pre-vatican-ii-catholic-practice-researcher", "catholic-devotions-sacramentals-expert", "gregorian-chant-sacred-music-expert", "catholic-calendar-fasting-abstinence-expert", "patristics-church-fathers-expert", "ecclesiastical-latin-expert",
    "fitness-coach", "bodybuilding-coach", "calisthenics-coach", "powerlifting-coach", "prenatal-postpartum-fitness-coach", "strength-conditioning-coach", "mobility-flexibility-coach", "endurance-conditioning-coach", "senior-fitness-coach", "youth-fitness-coach",
}
EXPECTED_SKILLS = {
    "hermesagent-runtime-architecture", "ai-application-engineering", "ai-system-architecture", "prompt-engineering", "agentic-workflow-engineering", "ai-evaluation-benchmarking", "llmops-model-operations", "ai-safety-reliability-evaluation", "retrieval-knowledge-engineering",
    "traditional-remedy-source-analysis", "herbal-remedy-evidence-screening", "historical-materia-medica-analysis", "natural-lifestyle-evidence-screening", "traditional-foodways-analysis",
    "amish-cultural-practice-research", "amish-building-practice-analysis", "amish-agriculture-practice-analysis", "amish-household-practice-analysis", "amish-foodways-analysis", "historical-food-preservation-analysis",
    "ancient-traditions-context-analysis", "ancient-domestic-life-research", "ancient-agricultural-history", "ancient-building-traditions-analysis", "ancient-foodways-analysis", "ancient-material-culture-analysis",
    "traditional-latin-mass-research", "roman-rite-liturgical-history", "catholic-devotional-traditions", "gregorian-chant-liturgical-music", "catholic-calendar-fasting-practice", "patristic-source-research", "ecclesiastical-latin-analysis",
    "fitness-coaching", "hypertrophy-programming", "calisthenics-programming", "powerlifting-programming", "prenatal-postpartum-exercise", "strength-conditioning", "mobility-flexibility-programming", "endurance-conditioning", "senior-fitness-programming", "youth-fitness-programming",
}
EXPECTED_BUNDLES = {"ai-engineering-team", "traditional-remedies-research-team", "amish-traditional-living-team", "ancient-traditions-team", "traditional-catholic-liturgy-team", "strength-fitness-team", "life-stage-fitness-team"}
REMEDY_PROFILES = {"traditional-remedies-researcher", "herbalism-ethnobotany-researcher", "historical-materia-medica-researcher", "amish-remedies-expert", "ancient-traditional-remedies-expert"}
AMISH_PROFILES = {name for name in EXPECTED_PROFILES if name.startswith("amish-")}
ANCIENT_PROFILES = {name for name in EXPECTED_PROFILES if name.startswith("ancient-")}


def doc(name: str) -> dict:
    return load_yaml(ROOT / "profiles" / f"{name}.yaml")


def instructions(name: str) -> str:
    return " ".join((doc(name).get("spec") or {}).get("instructions") or []).lower()


def main() -> int:
    errors: list[str] = []
    if (catalog().get("metadata") or {}).get("version") != "2.2.0":
        errors.append("catalog.yaml must be version 2.2.0")
    resources = discover_resources()
    names = names_by_kind(resources)
    for kind, expected in (("Profile", EXPECTED_PROFILES), ("Skill", EXPECTED_SKILLS), ("Bundle", EXPECTED_BUNDLES)):
        missing = sorted(expected - names.get(kind, set()))
        if missing:
            errors.append(f"missing v2.2 {kind} resources: {missing}")
    for name in EXPECTED_PROFILES:
        interaction = (doc(name).get("spec") or {}).get("interaction") or {}
        if interaction.get("userFacing") is True or interaction.get("directUserContact") == "allow" or interaction.get("userChannelBinding") == "allow":
            errors.append(f"{name} must remain internal-only")
    for name in REMEDY_PROFILES:
        text = instructions(name)
        if not any(term in text for term in ("diagnos", "prescrib")):
            errors.append(f"{name}: remedy role must explicitly deny diagnosis/prescribing")
        if name in {"traditional-remedies-researcher", "amish-remedies-expert"} and not any(term in text for term in ("urgent", "effective care", "modern care")):
            errors.append(f"{name}: must preserve modern/urgent-care boundary")
    for name in AMISH_PROFILES:
        text = instructions(name)
        tags = set((doc(name).get("metadata") or {}).get("tags") or [])
        if "amish" not in tags:
            errors.append(f"{name}: missing amish tag")
        if not any(term in text for term in ("region", "community", "affiliation", "uniform")):
            errors.append(f"{name}: must preserve Amish community/region variation")
    for name in ANCIENT_PROFILES:
        tags = set((doc(name).get("metadata") or {}).get("tags") or [])
        text = instructions(name)
        if "ancient-traditions" not in tags:
            errors.append(f"{name}: missing ancient-traditions tag")
        if not any(term in text for term in ("civilization", "culture", "period")):
            errors.append(f"{name}: must be civilization/culture/period specific")
    latin = instructions("traditional-latin-mass-expert")
    if "historical" not in latin or not any(term in latin for term in ("authority", "permission", "clergy")):
        errors.append("traditional-latin-mass-expert must distinguish historical/current context and ecclesiastical authority")
    prompt = instructions("ai-prompt-engineer")
    if "authorization" not in prompt or "substitute" not in prompt:
        errors.append("ai-prompt-engineer must state prompt text cannot substitute for structural authorization")
    maternity = instructions("prenatal-postpartum-fitness-coach")
    if "clinician" not in maternity or "diagnos" not in maternity:
        errors.append("prenatal-postpartum-fitness-coach must preserve clinician and non-diagnosis boundaries")
    bodybuilding = instructions("bodybuilding-coach")
    if "steroids" not in bodybuilding or "dehydration" not in bodybuilding:
        errors.append("bodybuilding-coach must deny drug and dangerous dehydration advice")
    if errors:
        print("v2.2 specialist expansion validation failed:")
        for error in errors:
            print(f" - {error}")
        return 1
    print(f"v2.2 expansion OK: {len(EXPECTED_PROFILES)} profiles, {len(EXPECTED_SKILLS)} skills, {len(EXPECTED_BUNDLES)} bundles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
