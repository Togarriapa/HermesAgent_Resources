#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from typing import Any

from registry_lib import ROOT, RESOURCE_DIRS, catalog, discover_resources, effective_spec as _effective_spec, load_quality_policy, load_yaml, resolve_inherited_spec

ENV_REF_RE = re.compile(r"^(?:\$\{[A-Z][A-Z0-9_]*\}|[A-Z][A-Z0-9_]*)$")
SECRET_KEYS = {"token", "tokenref", "password", "secret", "apikey", "api_key", "privatekey", "private_key", "seedphrase", "seed_phrase", "credentialref"}
REQUIRED_EFFECTIVE_PATHS: dict[str, tuple[str, ...]] = {
    "Profile": ("contract", "safety", "privacy", "reliability", "observability", "scope", "intake", "method", "evidence", "decisionPolicy", "execution", "collaboration", "failureHandling", "output"),
    "Skill": ("contract", "safety", "privacy", "reliability", "observability", "inputs", "preconditions", "procedure", "evidence", "verification", "failureModes", "outputs", "sideEffects", "quality"),
    "Plugin": ("contract", "safety", "privacy", "reliability", "observability", "capabilities", "security", "network", "sideEffects", "failureHandling", "provenancePolicy"),
    "MCP": ("contract", "safety", "privacy", "reliability", "observability", "capabilities", "security", "runtime", "sideEffects", "failureHandling", "provenancePolicy"),
    "Channel": ("contract", "safety", "privacy", "reliability", "observability", "routing", "admission", "sessions", "limits", "replayProtection", "failureHandling", "policy"),
    "Cron": ("contract", "safety", "privacy", "reliability", "observability", "concurrency", "idempotency", "timeouts", "retries", "misfire", "notifications", "policy"),
    "Webhook": ("contract", "safety", "privacy", "reliability", "observability", "replayProtection", "deduplication", "limits", "routing", "validation", "failureHandling", "policy"),
    "Bundle": ("contract", "safety", "privacy", "reliability", "observability", "purpose", "composition", "recruitment", "authority", "deliberation", "lifecycle"),
}
SKILL_METHOD_KEYS = {
    "principles",
    "procedure",
    "steps",
    "method",
    "checks",
    "rules",
    "workflow",
    "playbook",
    "guidelines",
    "process",
    "criteria",
    "techniques",
    "framework",
    "responsibilities",
    "instructions",
    "lifecycle",
    "states",
    "itemTypes",
}
PROFILE_ROLE_KEYS = {"instructions", "responsibilities", "principles", "role", "scope", "workflow", "method"}


def effective_spec(kind: str, name: str, tags: set[str], raw_spec: dict[str, Any], policy: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    return _effective_spec(kind, name, tags, raw_spec, policy)


def has_path(mapping: dict[str, Any], dotted: str) -> bool:
    current: Any = mapping
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return False
        current = current[part]
    return current is not None


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
        if not path or not isinstance(value, str):
            continue
        key = path[-1].replace("-", "").lower()
        if key not in SECRET_KEYS:
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
        errors.append(f"{rel}: metadata.tags must be a list of non-empty strings")
    if kind == "Profile":
        if not any(key in spec for key in PROFILE_ROLE_KEYS):
            errors.append(f"{rel}: Profile needs direct domain role/instruction content")
        interaction = spec.get("interaction") or {}
        if name == "hermes":
            if interaction.get("userFacing") is not True:
                errors.append(f"{rel}: Hermes must remain explicitly user-facing")
        elif interaction.get("userFacing") is True or interaction.get("directUserContact") == "allow" or interaction.get("userChannelBinding") == "allow":
            errors.append(f"{rel}: non-Hermes Profile cannot become user-facing")
    elif kind == "Skill":
        if not (set(spec) & SKILL_METHOD_KEYS):
            errors.append(f"{rel}: Skill needs direct domain method content")
    elif kind == "Plugin":
        if not any(key in spec for key in ("provider", "endpoint", "command", "runtime", "adapters")):
            errors.append(f"{rel}: Plugin must declare provider/endpoint/runtime surface")
    elif kind == "MCP":
        if not spec.get("transport") or not any(key in spec for key in ("endpoint", "command", "image")):
            errors.append(f"{rel}: MCP requires transport and endpoint/command/image")
    elif kind == "Channel":
        routing = spec.get("routing") or {}
        if routing.get("inboundProfile") != "hermes" or routing.get("outboundProfile") != "hermes":
            errors.append(f"{rel}: Channel must explicitly bind Hermes inbound/outbound")
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


def homelab_authorization_checks(rel: str, kind: str, name: str, doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    spec = doc.get("spec") or {}
    if name == "homelab-infrastructure-operator":
        auth = spec.get("authorization") or {}
        if auth.get("identityProvider") != "authentik" or auth.get("requiredEffectiveGroup") != "System":
            errors.append(f"{rel}: infrastructure operator must require Authentik effective group System")
        if auth.get("mutationCheck") != "fresh-before-tool-call" or auth.get("alarmRecipientCheck") != "fresh-at-delivery" or auth.get("failClosed") is not True:
            errors.append(f"{rel}: infrastructure operator must freshly verify mutations and alarm recipients and fail closed")
        if auth.get("userSuppliedClaims") != "deny" or auth.get("cachedGroupMembershipAsAuthority") != "deny":
            errors.append(f"{rel}: user-supplied or cached group claims cannot grant infrastructure authority")
    elif name == "authentik-authorization":
        policy = spec.get("policy") or {}
        runtime = spec.get("runtime") or {}
        if policy.get("writes") != "deny" or policy.get("groupAdministration") != "deny" or policy.get("roleAdministration") != "deny":
            errors.append(f"{rel}: Authentik authorization adapter must remain read-only")
        if policy.get("failClosedOnLookupFailure") is not True or runtime.get("requiredGroupName") != "System" or runtime.get("membershipMode") != "direct-and-indirect":
            errors.append(f"{rel}: Authentik adapter must resolve effective System membership and fail closed")
        if runtime.get("cacheUseForAuthorization") != "deny":
            errors.append(f"{rel}: cached Authentik membership cannot be used as authority")
    elif name == "homelab-ops-broker":
        policy = spec.get("policy") or {}
        runtime = spec.get("runtime") or {}
        if policy.get("arbitraryShell") != "deny" or policy.get("rawSsh") != "deny" or policy.get("arbitraryCommand") != "deny":
            errors.append(f"{rel}: homelab operations broker must deny raw SSH/arbitrary shell/commands")
        if policy.get("writesRequireFreshAuthentikSystemMembership") is not True or runtime.get("requiredEffectiveGroupForWrites") != "System":
            errors.append(f"{rel}: homelab operations writes must require fresh Authentik System membership")
    elif name == "cloudflare-homelab":
        policy = spec.get("policy") or {}
        runtime = spec.get("runtime") or {}
        if policy.get("writesRequireFreshAuthentikSystemMembership") is not True or runtime.get("requiredEffectiveGroupForWrites") != "System":
            errors.append(f"{rel}: Cloudflare homelab writes must require fresh Authentik System membership")
        for denied in ("unrelatedZoneAccess", "unrelatedTunnelAccess", "accountAdministration", "apiTokenAdministration"):
            if policy.get(denied) != "deny":
                errors.append(f"{rel}: policy.{denied} must remain deny")
    elif name == "homelab-health-review":
        policy = spec.get("policy") or {}
        if policy.get("authorityFromSchedule") != "deny" or policy.get("remediationFromSchedule") != "deny":
            errors.append(f"{rel}: homelab health schedule cannot create remediation authority")
        if policy.get("infrastructureAlarmRequiredGroup") != "System" or policy.get("resolveRecipientsAtDelivery") is not True or policy.get("failClosedOnRecipientAuthorizationFailure") is not True:
            errors.append(f"{rel}: infrastructure alarms must resolve current Authentik System recipients and fail closed")
        if policy.get("staticRecipientListAsAuthority") != "deny":
            errors.append(f"{rel}: static infrastructure alarm recipients cannot grant delivery authority")
    elif name == "homelab-operations-team":
        policy = spec.get("policy") or {}
        if policy.get("infrastructureMutationRequiredEffectiveGroup") != "System" or policy.get("infrastructureAlarmRequiredEffectiveGroup") != "System":
            errors.append(f"{rel}: homelab bundle must preserve System-only infrastructure mutation and alarm boundaries")
        if policy.get("authorityExpansion") != "deny" or policy.get("failClosedOnAuthorizationFailure") is not True:
            errors.append(f"{rel}: homelab bundle cannot expand authority and must fail closed")
    return errors


def main() -> int:
    errors: list[str] = []
    try:
        cat = catalog()
        resources = discover_resources()
        policy = load_quality_policy()
    except (ValueError, OSError) as exc:
        print(f"Quality discovery failed: {exc}", file=sys.stderr)
        return 1

    if (cat.get("metadata") or {}).get("version") != "2.3.1":
        errors.append("catalog.yaml: current quality validation expects catalog version 2.3.1")
    application = policy.get("application") or {}
    if application.get("scope") != "every-catalog-resource":
        errors.append("QUALITY_POLICY.yaml: policy must apply to every catalog resource")
    for field in ("defaultsMayExpandCapability", "overlaysMayExpandCapability", "resourceMayExceedHostAuthority", "learnedOverlayMayExpandCapability", "sessionContextMayExpandCapability"):
        if application.get(field) is not False:
            errors.append(f"QUALITY_POLICY.yaml: application.{field} must be false")
    if application.get("authorizationCeiling") != "local-host-policy":
        errors.append("QUALITY_POLICY.yaml: local host policy must remain the authorization ceiling")

    defaults = policy.get("defaults") or {}
    for kind in RESOURCE_DIRS:
        if not isinstance(defaults.get(kind), dict):
            errors.append(f"quality policy missing defaults for {kind}")

    overlay_counts: dict[str, int] = {}
    kind_counts: dict[str, int] = {}
    for item in resources:
        rel = item["rel"]
        kind = str(item.get("kind"))
        name = str(item.get("name"))
        doc = item["doc"]
        metadata = doc.get("metadata") or {}
        raw_tags = metadata.get("tags") or []
        tags = set(raw_tags) if isinstance(raw_tags, list) else set()
        try:
            resolved = resolve_inherited_spec(item, resources)
        except ValueError as exc:
            errors.append(f"{rel}: {exc}")
            continue
        effective, overlays = effective_spec(kind, name, tags, resolved, policy)
        kind_counts[kind] = kind_counts.get(kind, 0) + 1
        for overlay in overlays:
            overlay_counts[overlay] = overlay_counts.get(overlay, 0) + 1
        for required in REQUIRED_EFFECTIVE_PATHS.get(kind, ()):
            if not has_path(effective, required):
                errors.append(f"{rel}: effective {kind} contract missing {required}")
        errors.extend(direct_manifest_checks(rel, kind, name, doc))
        errors.extend(secret_literal_errors(rel, doc))
        errors.extend(homelab_authorization_checks(rel, kind, name, doc))
        if (effective.get("safety") or {}).get("authorityFromInference") != "deny":
            errors.append(f"{rel}: effective policy must deny authority inferred from context")
        if (effective.get("privacy") or {}).get("secretCommit") != "deny":
            errors.append(f"{rel}: effective policy must deny committing secrets")
        if kind == "Bundle" and (effective.get("authority") or {}).get("membershipExpandsAuthority") is not False:
            errors.append(f"{rel}: Bundle membership must not expand authority")
        if kind == "Cron" and (effective.get("policy") or {}).get("authorityFromSchedule") != "deny":
            errors.append(f"{rel}: schedule must not create authority")
        if kind == "Webhook" and (effective.get("policy") or {}).get("authorityFromWebhookReceipt") != "deny":
            errors.append(f"{rel}: webhook receipt must not create authority")
        if kind == "Channel" and (effective.get("routing") or {}).get("allowedUserFacingProfiles") != ["hermes"]:
            errors.append(f"{rel}: effective Channel must expose only Hermes")

    missing_kinds = sorted(set(RESOURCE_DIRS) - set(kind_counts))
    if missing_kinds:
        errors.append(f"quality validation saw no resources for kinds: {missing_kinds}")
    if errors:
        print("Registry quality validation failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1
    overlays = ", ".join(f"{name}={count}" for name, count in sorted(overlay_counts.items())) or "none"
    kinds = ", ".join(f"{kind}={kind_counts.get(kind, 0)}" for kind in RESOURCE_DIRS)
    print(f"Quality OK: {len(resources)} resources checked individually ({kinds}); overlays: {overlays}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
