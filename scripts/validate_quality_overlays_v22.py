#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from validate_quality_v22 import ROOT, effective_spec, load_yaml

POLICY_PATH = ROOT / "QUALITY_POLICY.yaml"

# Each case asserts the quality overlays that SHOULD and SHOULD NOT attach to a
# representative real catalog resource. These are regression tests for broad
# substring/tag matchers: a conservative policy is only useful if it remains
# relevant to the resource rather than attaching unrelated physical, medical,
# financial, or translation constraints everywhere.
CASES = {
    "profiles/systems-architect.yaml": {
        "must": {"software-data-infrastructure"},
        "must_not": {"physical-engineering-property-farm", "translation"},
    },
    "profiles/network-engineer.yaml": {
        "must": {"software-data-infrastructure"},
        "must_not": {"physical-engineering-property-farm"},
    },
    "profiles/building-architect.yaml": {
        "must": {"physical-engineering-property-farm"},
        "must_not": {"software-data-infrastructure"},
    },
    "profiles/language-teacher.yaml": {
        "must": {"children-education"},
        "must_not": {"translation"},
    },
    "profiles/portuguese-english-translator.yaml": {
        "must": {"translation"},
        "must_not": {"children-education"},
    },
    "profiles/portfolio-manager.yaml": {
        "must": {"finance-investment"},
        "must_not": {"physical-engineering-property-farm"},
    },
    "profiles/catholic-tradition-expert.yaml": {
        "must": {"catholic"},
        "must_not": {"translation"},
    },
    "profiles/psychology-expert.yaml": {
        "must": {"health-psychology-nutrition", "research-information-integrity"},
        "must_not": {"physical-engineering-property-farm"},
    },
    "profiles/eu-law-regulatory-specialist.yaml": {
        "must": {"legal-regulatory"},
        "must_not": {"finance-investment"},
    },
    "profiles/fact-checker-source-verification-specialist.yaml": {
        "must": {"research-information-integrity"},
        "must_not": {"legal-regulatory", "finance-investment"},
    },
    "profiles/3d-printer-specialist.yaml": {
        "must": {"physical-engineering-property-farm"},
        "must_not": {"software-data-infrastructure"},
    },
}


def overlays_for(relative_path: str, policy: dict) -> set[str]:
    path = ROOT / relative_path
    if not path.exists():
        raise FileNotFoundError(relative_path)
    doc = load_yaml(path)
    metadata = doc.get("metadata") or {}
    kind = str(doc.get("kind"))
    name = str(metadata.get("name"))
    raw_tags = metadata.get("tags") or []
    tags = set(raw_tags) if isinstance(raw_tags, list) else set()
    _effective, overlays = effective_spec(kind, name, tags, doc.get("spec") or {}, policy)
    return set(overlays)


def main() -> int:
    policy_doc = load_yaml(POLICY_PATH)
    policy = policy_doc.get("spec") or {}
    errors: list[str] = []

    for relative_path, expected in CASES.items():
        try:
            actual = overlays_for(relative_path, policy)
        except FileNotFoundError:
            errors.append(f"missing regression resource: {relative_path}")
            continue

        missing = sorted(expected["must"] - actual)
        forbidden = sorted(expected["must_not"] & actual)
        if missing:
            errors.append(f"{relative_path}: expected overlays missing: {missing}; actual={sorted(actual)}")
        if forbidden:
            errors.append(f"{relative_path}: unrelated overlays attached: {forbidden}; actual={sorted(actual)}")

    if errors:
        print("v2.2 quality-overlay regression validation failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"Quality overlay regression OK: {len(CASES)} representative resources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
