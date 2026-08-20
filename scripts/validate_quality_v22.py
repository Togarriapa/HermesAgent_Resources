#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("PyYAML is required: python3 -m pip install pyyaml", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "QUALITY_POLICY.yaml"
CATALOG_PATH = ROOT / "catalog.yaml"
SUPPORTED_KINDS = {"Profile", "Skill", "Plugin", "MCP", "Channel", "Cron", "Webhook", "Bundle"}
ENV_REF_RE = re.compile(r"^(?:\$\{[A-Z][A-Z0-9_]*\}|[A-Z][A-Z0-9_]*)$")
SECRET_KEYS = {"token", "tokenref", "password", "secret", "apikey", "api_key", "privatekey", "private_key", "seedphrase", "seed_phrase", "credentialref"}

REQUIRED_EFFECTIVE_PATHS: dict[str, tuple[str, ...]] = {
    "Profile": (
        "contract", "safety", "privacy", "reliability", "observability",
        "scope", "intake", "method", "evidence", "decisionPolicy", "execution",
        "collaboration", "failureHandling", "output",
    ),
    "Skill": (
        "contract", "safety", "privacy", "reliability", "observability",
        "inputs", "preconditions", "procedure", "evidence", "verification",
        "failureModes", "outputs", "sideEffects", "quality",
    ),
    "Plugin": (
        "contract", "safety", "privacy", "reliability", "observability",
        "capabilities", "security", "network", "sideEffects", "failureHandling", "provenancePolicy",
    ),
    "MCP": (
        "contract", "safety", "privacy", "reliability", "observability",
        "capabilities", "security", "runtime", "sideEffects", "failureHandling", "provenancePolicy",
    ),
    "Channel": (
        "contract", "safety", "privacy", "reliability", "observability",
        "routing", "admission", "sessions", "limits", "replayProtection", "failureHandling", "policy",
    ),
    "Cron": (
        "contract", "safety", "privacy", "reliability", "observability",
        "concurrency", "idempotency", "timeouts", "retries", "misfire", "notifications", "policy",
    ),
    "Webhook": (
        "contract", "safety", "privacy", "reliability", "observability",
        "replayProtection", "deduplication", "limits", "routing", "validation", "failureHandling", "policy",
    ),
    "Bundle": (
        "contract", "safety", "privacy", "reliability", "observability",
        "purpose", "composition", "recruitment", "authority", "deliberation", "lifecycle",
    ),
}

SKILL_METHOD_KEYS = {
    "principles", "procedure", "steps", "method", "checks", "rules", "workflow", "playbook",
    "guidelines", "process", "criteria", "techniques", "framework", "responsibilities",
}
PROFILE_ROLE_KEYS = {"instructions", "responsibilities", "principles", "role", "scope", "workflow", "method"}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: YAML root must be a mapping")
    return data


def merge(low: Any, high: Any) -> Any:
    """Merge restrictive/default configuration from low precedence to high precedence."""
    if isinstance(low, dict) and isinstance(high, dict):
        result = deepcopy(low)
        for key, value in high.items():
            result[key] = merge(result[key], value) if key in result else deepcopy(value)
        return result
    if isinstance(low, list) and isinstance(high, list):
        result = deepcopy(low)
        for item in high:
            if item not in result:
                result.append(deepcopy(item))
        return result
    return deepcopy(high)


def has_path(mapping: dict[str, Any], dotted: str) -> bool:
    current: Any = mapping
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return False
        current = current[part]
    return current is not None


def matches_overlay(name: str, tags: set[str], match: dict[str, Any]) -> bool:
    contains = match.get("nameContains") or []
    tag_any = set(match.get("tagsAny") or [])
    return any(fragment in name for fragment in contains) or bool(tags & tag_any)


def effective_spec(kind: str, name: str, tags: set[str], raw_spec: dict[str, Any], policy: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    spec = merge({}, policy.get("universal") or {})
    spec = merge(spec, ((policy.get("defaults") or {}).get(kind) or {}))
    applied: list[str] = []
    for overlay in policy.get("domainOverlays") or []:
        if not isinstance(overlay, dict):
            continue
        if matches_overlay(name, tags, overlay.get("match") or {}):
            spec = merge(spec, overlay.get("apply") or {})
            applied.append(str(overlay.get("name") or "unnamed"))
    spec = merge(spec, raw_spec)
    return spec, applied


def iter_scalars(value: Any, prefix: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from iter_scalars(child, prefix + (str(key),))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_scalars(child, prefix + (str(index),))
    else:
        yield prefix, value


def secret_literal_errors(rel: str, doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for path, value in iter_scalars(doc.get("spec") or {}):
        if not path:
            continue
        key = path[-1].replace("-", "").lower()
        if key not in SECRET_KEYS or value is None or not isinstance(value, str):
            continue
        if value in {"runtime-only", "deny", "none", "host-managed"}:
            continue
        if not ENV_REF_RE.fullmatch(value):
            errors.append(f"{rel}: possible secret literal at spec.{'.'.join(path)}; use a runtime environment reference")
    return errors


def direct_manifest_checks(rel: str, kind: str, name: str, doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    metadata = doc.get("metadata") or {}
    spec = doc.get("spec") or {}
    description = metadata.get("description")
    tags = metadata.get("tags")

    if not isinstance(description, str) or len(description.strip()) < 20:
        errors.append(f"{rel}: description must communicate a substantive purpose")
    if tags is not None and (not isinstance(tags, list) or any(not isinstance(tag, str) or not tag for tag in tags)):
        errors.append(f"{rel}: metadata.tags must be a list of non-empty strings when present")

    if kind == "Profile":
        if not any(key in spec for key in PROFILE_ROLE_KEYS):
            errors.append(f"{rel}: Profile needs domain-specific role/instruction content; quality defaults cannot invent expertise")
        interaction = spec.get("interaction") or {}
        if name == "hermes":
            if interaction.get("userFacing") is not True:
                errors.append(f"{rel}: Hermes must remain explicitly user-facing")
        elif interaction.get("userFacing") is True or interaction.get("directUserContact") == "allow" or interaction.get("userChannelBinding") == "allow":
            errors.append(f"{rel}: non-Hermes Profile cannot become user-facing")

    elif kind == "Skill":
        if not (set(spec) & SKILL_METHOD_KEYS):
            substantive = set(spec) - {"requires", "extends", "compatibility"}
            if not substantive:
                errors.append(f"{rel}: Skill needs domain-specific method content; description-only Skills are incomplete")

    elif kind == "Plugin":
        if not any(key in spec for key in ("provider", "endpoint", "command", "runtime")):
            errors.append(f"{rel}: Plugin must declare a provider/endpoint/runtime surface")

    elif kind == "MCP":
        if not spec.get("transport"):
            errors.append(f"{rel}: MCP transport is required")
        if not any(key in spec for key in ("endpoint", "command", "image")):
            errors.append(f"{rel}: MCP must declare an endpoint, command, or image")

    elif kind == "Channel":
        routing = spec.get("routing") or {}
        if routing.get("inboundProfile") != "hermes" or routing.get("outboundProfile") != "hermes":
            errors.append(f"{rel}: user channel routing must explicitly bind Hermes inbound and outbound")

    elif kind == "Cron":
        if not spec.get("schedule") or not spec.get("timezone") or not isinstance(spec.get("action"), dict):
            errors.append(f"{rel}: Cron requires schedule, timezone, and action")

    elif kind == "Webhook":
        if not spec.get("path") or not spec.get("method") or not isinstance(spec.get("authentication"), dict):
            errors.append(f"{rel}: Webhook requires path, method, and authentication")

    elif kind == "Bundle":
        imports = spec.get("imports")
        if not isinstance(imports, dict) or not any(isinstance(v, list) and v for v in imports.values()):
            errors.append(f"{rel}: Bundle requires at least one imported resource")

    return errors


def main() -> int:
    errors: list[str] = []

    if not POLICY_PATH.exists():
        print("QUALITY_POLICY.yaml is missing", file=sys.stderr)
        return 1
    policy_doc = load_yaml(POLICY_PATH)
    policy_meta = policy_doc.get("metadata") or {}
    policy = policy_doc.get("spec") or {}
    application = policy.get("application") or {}

    if policy_doc.get("kind") != "RegistryQualityPolicy":
        errors.append("QUALITY_POLICY.yaml: kind must be RegistryQualityPolicy")
    if policy_meta.get("version") != "2.2.0":
        errors.append("QUALITY_POLICY.yaml: expected policy version 2.2.0")
    if application.get("scope") != "every-catalog-resource":
        errors.append("QUALITY_POLICY.yaml: policy must apply to every catalog resource")
    if application.get("authorizationCeiling") != "local-host-policy":
        errors.append("QUALITY_POLICY.yaml: local host policy must be the absolute authorization ceiling")
    if application.get("explicitUserAuthority") != "within-host-policy-only":
        errors.append("QUALITY_POLICY.yaml: explicit user authority must remain within host policy")
    for key in (
        "defaultsMayExpandCapability", "overlaysMayExpandCapability", "resourceMayExceedHostAuthority",
        "learnedOverlayMayExpandCapability", "sessionContextMayExpandCapability",
    ):
        if application.get(key) is not False:
            errors.append(f"QUALITY_POLICY.yaml: {key} must be false")

    catalog = load_yaml(CATALOG_PATH)
    entries = catalog.get("resources") or []
    if not isinstance(entries, list):
        errors.append("catalog.yaml: resources must be a list")
        entries = []

    covered = 0
    overlay_counts: dict[str, int] = {}
    kind_counts: dict[str, int] = {}

    defaults = policy.get("defaults") or {}
    for kind in SUPPORTED_KINDS:
        if not isinstance(defaults.get(kind), dict):
            errors.append(f"QUALITY_POLICY.yaml: missing kind defaults for {kind}")

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        kind = entry.get("kind")
        name = entry.get("name")
        rel = entry.get("path")
        if kind not in SUPPORTED_KINDS or not isinstance(name, str) or not isinstance(rel, str):
            continue
        path = ROOT / rel
        if not path.exists():
            continue
        doc = load_yaml(path)
        raw_spec = doc.get("spec") or {}
        metadata = doc.get("metadata") or {}
        tags = set(metadata.get("tags") or []) if isinstance(metadata.get("tags") or [], list) else set()
        effective, overlays = effective_spec(kind, name, tags, raw_spec, policy)
        covered += 1
        kind_counts[kind] = kind_counts.get(kind, 0) + 1
        for overlay in overlays:
            overlay_counts[overlay] = overlay_counts.get(overlay, 0) + 1

        for required in REQUIRED_EFFECTIVE_PATHS[kind]:
            if not has_path(effective, required):
                errors.append(f"{rel}: effective {kind} contract missing {required}")

        errors.extend(direct_manifest_checks(rel, kind, name, doc))
        errors.extend(secret_literal_errors(rel, doc))

        if not has_path(effective, "safety.authorityFromInference") or effective["safety"].get("authorityFromInference") != "deny":
            errors.append(f"{rel}: effective policy must deny authority inferred from context")
        if (effective.get("privacy") or {}).get("secretCommit") != "deny":
            errors.append(f"{rel}: effective policy must deny committing secrets")

        if kind == "Bundle" and (effective.get("authority") or {}).get("membershipExpandsAuthority") is not False:
            errors.append(f"{rel}: Bundle membership must not expand authority")
        if kind == "Cron" and (effective.get("policy") or {}).get("authorityFromSchedule") != "deny":
            errors.append(f"{rel}: schedule must not create authority")
        if kind == "Webhook" and (effective.get("policy") or {}).get("authorityFromWebhookReceipt") != "deny":
            errors.append(f"{rel}: webhook receipt must not create authority")
        if kind == "Channel":
            routing = effective.get("routing") or {}
            if routing.get("allowedUserFacingProfiles") != ["hermes"]:
                errors.append(f"{rel}: effective channel policy must expose only Hermes")

    missing_kinds = sorted(SUPPORTED_KINDS - set(kind_counts))
    if missing_kinds:
        errors.append(f"quality validation saw no catalog resources for kinds: {missing_kinds}")

    if errors:
        print("Registry quality validation failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    overlay_summary = ", ".join(f"{name}={count}" for name, count in sorted(overlay_counts.items())) or "none"
    kinds = ", ".join(f"{kind}={count}" for kind, count in sorted(kind_counts.items()))
    print(f"Quality OK: {covered} resources checked individually ({kinds}); overlays: {overlay_summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
