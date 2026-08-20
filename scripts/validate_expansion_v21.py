#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_PROFILES = {
    "product-manager", "business-analyst-requirements-engineer", "coo-operations-manager",
    "people-operations-hr-specialist", "recruiter-talent-acquisition-specialist", "privacy-gdpr-specialist",
    "negotiation-conflict-resolution-specialist", "decision-scientist-operations-research-specialist",
    "automotive-maintenance-specialist", "home-energy-solar-specialist", "water-wastewater-specialist",
    "emergency-preparedness-resilience-manager", "arboriculture-tree-care-specialist", "pest-building-biology-specialist",
    "horticulture-orchard-specialist", "livestock-health-navigator", "farm-machinery-maintenance-specialist",
    "child-development-specialist", "special-education-sen-specialist", "mathematics-teacher", "science-teacher",
    "literacy-reading-specialist", "insurance-specialist", "estate-succession-planning-research-specialist",
    "procurement-vendor-manager", "eu-law-regulatory-specialist", "employment-law-portugal-eu-specialist",
    "network-engineer", "site-reliability-engineer", "database-reliability-specialist", "ai-ml-engineer",
    "privacy-security-engineer", "fact-checker-source-verification-specialist", "media-literacy-misinformation-analyst",
    "ethics-specialist", "knowledge-manager-archivist", "catholic-relationship-expert",
    "catholic-traditional-family-advisor", "catholic-tradition-expert", "catholic-history-expert",
    "catholic-prayer-planner-writer", "portuguese-english-translator", "building-architect", "farm-planner",
    "3d-model-designer", "3d-printer-specialist", "3d-model-maker", "3d-model-optimizer",
}

EXPECTED_SKILLS = {
    "claim-verification", "negotiation-preparation", "scenario-sensitivity-analysis", "decision-recording",
    "root-cause-analysis", "vendor-comparison", "privacy-impact-screening", "emergency-checklist-design",
    "cost-benefit-tco-analysis", "requirements-engineering", "professional-translation-portuguese-english",
    "architectural-design-planning", "3d-modeling-cad", "additive-manufacturing", "3d-printability-optimization",
}

EXPECTED_BUNDLES = {
    "product-strategy-team", "people-career-team", "privacy-compliance-team", "home-resilience-team",
    "farm-reliability-team", "decision-science-team", "catholic-tradition-family-team", "core-education-team",
    "architecture-fabrication-team", "additive-manufacturing-team", "information-integrity-team", "farm-planning-team",
}


def main() -> int:
    errors = []
    catalog = yaml.safe_load((ROOT / "catalog.yaml").read_text())
    if catalog.get("metadata", {}).get("version") != "2.1.0":
        errors.append("catalog.yaml must be version 2.1.0")

    entries = catalog.get("resources", [])
    names = {}
    for entry in entries:
        names.setdefault(entry.get("kind"), set()).add(entry.get("name"))

    for kind, expected in (("Profile", EXPECTED_PROFILES), ("Skill", EXPECTED_SKILLS), ("Bundle", EXPECTED_BUNDLES)):
        missing = sorted(expected - names.get(kind, set()))
        if missing:
            errors.append(f"missing {kind} resources: {missing}")

    if (ROOT / "CAPABILITY_GAP_AUDIT.md").exists():
        errors.append("CAPABILITY_GAP_AUDIT.md must be removed after all recommendations are implemented")

    for name in EXPECTED_PROFILES:
        path = ROOT / "profiles" / f"{name}.yaml"
        if not path.exists():
            errors.append(f"missing profile manifest {path.relative_to(ROOT)}")
            continue
        doc = yaml.safe_load(path.read_text())
        interaction = doc.get("spec", {}).get("interaction", {})
        if interaction.get("userFacing") is True or interaction.get("directUserContact") == "allow" or interaction.get("userChannelBinding") == "allow":
            errors.append(f"{name} must remain internal-only")

    livestock = yaml.safe_load((ROOT / "profiles/livestock-health-navigator.yaml").read_text())
    text = " ".join(livestock.get("spec", {}).get("instructions", [])).lower()
    if "do not diagnose" not in text or "prescribe veterinary" not in text:
        errors.append("livestock-health-navigator must preserve non-veterinary diagnosis/prescribing boundary")

    architect = yaml.safe_load((ROOT / "profiles/building-architect.yaml").read_text())
    text = " ".join(architect.get("spec", {}).get("instructions", [])).lower()
    if "licensed" not in text or "statutory" not in text:
        errors.append("building-architect must distinguish design assistance from licensed/statutory responsibility")

    catholic = yaml.safe_load((ROOT / "profiles/catholic-traditional-family-advisor.yaml").read_text())
    text = " ".join(catholic.get("spec", {}).get("instructions", [])).lower()
    if "binding doctrine" not in text or "prudential" not in text:
        errors.append("catholic-traditional-family-advisor must distinguish doctrine from prudential/custom matters")

    if errors:
        print("v2.1 expansion validation failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"v2.1 expansion OK: {len(EXPECTED_PROFILES)} profiles, {len(EXPECTED_SKILLS)} skills, {len(EXPECTED_BUNDLES)} bundles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
