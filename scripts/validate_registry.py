#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("PyYAML is required: python3 -m pip install pyyaml", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
API_VERSION = "hermes.togarriapa/v1"
VALID_KINDS = {"Profile", "Skill", "Plugin", "MCP", "Cron", "Webhook", "Channel", "Bundle"}
RESOURCE_DIRS = {
    "Profile": "profiles",
    "Skill": "skills",
    "Plugin": "plugins",
    "MCP": "mcps",
    "Cron": "crons",
    "Webhook": "webhooks",
    "Channel": "channels",
    "Bundle": "bundles",
}
DEPENDENCY_KINDS = {
    "profiles": "Profile",
    "skills": "Skill",
    "plugins": "Plugin",
    "mcps": "MCP",
    "crons": "Cron",
    "webhooks": "Webhook",
    "channels": "Channel",
    "bundles": "Bundle",
}
USER_CHANNELS = {"web", "telegram", "discord", "whatsapp", "voice"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
SELECTOR_RE = re.compile(r"^([a-z0-9]+(?:-[a-z0-9]+)*)@(\^?)(\d+\.\d+\.\d+)$")
COMPOSIO_VERSION_RE = re.compile(r"^\d{8}_\d{2}$")


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def version_tuple(version: str) -> tuple[int, int, int]:
    core = version.split("-", 1)[0].split("+", 1)[0]
    major, minor, patch = core.split(".")
    return int(major), int(minor), int(patch)


def selector_matches(candidate: str, requested: str, caret: bool) -> bool:
    c = version_tuple(candidate)
    r = version_tuple(requested)
    if not caret:
        return c == r
    if r[0] > 0:
        return c[0] == r[0] and c >= r
    if r[1] > 0:
        return c[0] == 0 and c[1] == r[1] and c >= r
    return c[0] == 0 and c[1] == 0 and c[2] == r[2]


def validate_selector(
    rel: str,
    field: str,
    kind: str,
    selector: Any,
    versions: dict[tuple[str, str], set[str]],
    errors: list[str],
) -> None:
    if not isinstance(selector, str):
        fail(f"{rel}: {field} selector must be a string", errors)
        return
    match = SELECTOR_RE.fullmatch(selector)
    if not match:
        fail(f"{rel}: {field} has invalid selector {selector!r}", errors)
        return
    name, caret_marker, requested = match.groups()
    candidates = versions.get((kind, name), set())
    if not candidates:
        fail(f"{rel}: {field} references missing {kind} {name!r}", errors)
        return
    if not any(selector_matches(candidate, requested, bool(caret_marker)) for candidate in candidates):
        fail(f"{rel}: {field} selector {selector!r} is not satisfied by {sorted(candidates)}", errors)


def validate_dependency_map(
    rel: str,
    field: str,
    dependency_map: Any,
    versions: dict[tuple[str, str], set[str]],
    errors: list[str],
) -> None:
    if dependency_map is None:
        return
    if not isinstance(dependency_map, dict):
        fail(f"{rel}: {field} must be a mapping", errors)
        return
    for plural, selectors in dependency_map.items():
        kind = DEPENDENCY_KINDS.get(plural)
        if kind is None:
            fail(f"{rel}: {field} has unknown dependency group {plural!r}", errors)
            continue
        if not isinstance(selectors, list):
            fail(f"{rel}: {field}.{plural} must be a list", errors)
            continue
        for selector in selectors:
            validate_selector(rel, f"{field}.{plural}", kind, selector, versions, errors)


def validate_composio_policy(rel: str, spec: dict[str, Any], errors: list[str]) -> None:
    policy = (spec.get("integrationPolicy") or {}).get("composio")
    if policy is None:
        return
    if not isinstance(policy, dict):
        fail(f"{rel}: integrationPolicy.composio must be a mapping", errors)
        return

    required_plugins = ((spec.get("requires") or {}).get("plugins") or [])
    if not any(isinstance(item, str) and item.startswith("composio@") for item in required_plugins):
        fail(f"{rel}: Composio policy requires an explicit composio plugin dependency", errors)

    toolkits = policy.get("toolkits")
    if not isinstance(toolkits, list) or not toolkits:
        fail(f"{rel}: integrationPolicy.composio.toolkits must be a non-empty list", errors)
        return

    seen_slugs: set[str] = set()
    for toolkit in toolkits:
        if not isinstance(toolkit, dict):
            fail(f"{rel}: each Composio toolkit entry must be a mapping", errors)
            continue
        slug = toolkit.get("slug")
        version = toolkit.get("version")
        tools = toolkit.get("allowedTools")
        if not isinstance(slug, str) or not NAME_RE.fullmatch(slug.replace("_", "-")):
            fail(f"{rel}: invalid Composio toolkit slug {slug!r}", errors)
            continue
        if slug in seen_slugs:
            fail(f"{rel}: duplicate Composio toolkit {slug!r}", errors)
        seen_slugs.add(slug)
        if not isinstance(version, str) or not COMPOSIO_VERSION_RE.fullmatch(version):
            fail(f"{rel}: Composio toolkit {slug!r} must pin a dated version", errors)
        if not isinstance(tools, list) or not tools:
            fail(f"{rel}: Composio toolkit {slug!r} must explicitly allow tools", errors)
            continue
        expected_prefix = slug.upper() + "_"
        for tool in tools:
            if not isinstance(tool, str) or not tool.startswith(expected_prefix):
                fail(f"{rel}: tool {tool!r} does not match toolkit {slug!r}", errors)


def main() -> int:
    errors: list[str] = []
    catalog_path = ROOT / "catalog.yaml"
    if not catalog_path.exists():
        print("catalog.yaml is missing", file=sys.stderr)
        return 1

    catalog = load_yaml(catalog_path) or {}
    if catalog.get("apiVersion") != API_VERSION:
        fail(f"catalog.yaml: apiVersion must be {API_VERSION}", errors)
    if catalog.get("kind") != "Catalog":
        fail("catalog.yaml: kind must be Catalog", errors)

    entries = catalog.get("resources", [])
    if not isinstance(entries, list):
        fail("catalog.yaml: resources must be a list", errors)
        entries = []

    seen: set[tuple[str, str, str]] = set()
    catalog_paths: set[str] = set()
    versions: dict[tuple[str, str], set[str]] = {}
    docs: list[tuple[str, str, str, str, dict[str, Any]]] = []

    for entry in entries:
        if not isinstance(entry, dict):
            fail("catalog.yaml: each resource entry must be a mapping", errors)
            continue
        kind = entry.get("kind")
        name = entry.get("name")
        version = entry.get("version")
        rel = entry.get("path")
        key = (str(kind), str(name), str(version))
        if key in seen:
            fail(f"catalog.yaml: duplicate resource {key}", errors)
            continue
        seen.add(key)

        if kind not in VALID_KINDS:
            fail(f"{rel}: invalid kind {kind!r}", errors)
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            fail(f"{rel}: invalid metadata.name {name!r}", errors)
        if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
            fail(f"{rel}: invalid version {version!r}", errors)
        if not isinstance(rel, str):
            fail(f"catalog.yaml: resource {key} has no path", errors)
            continue

        catalog_paths.add(rel)
        path = (ROOT / rel).resolve()
        if ROOT not in path.parents:
            fail(f"{rel}: path escapes repository", errors)
            continue
        if not path.is_file():
            fail(f"{rel}: file is missing", errors)
            continue

        doc = load_yaml(path) or {}
        if not isinstance(doc, dict):
            fail(f"{rel}: document must be a mapping", errors)
            continue
        metadata = doc.get("metadata") or {}
        if doc.get("apiVersion") != API_VERSION:
            fail(f"{rel}: apiVersion must be {API_VERSION}", errors)
        if doc.get("kind") != kind:
            fail(f"{rel}: kind differs from catalog", errors)
        if metadata.get("name") != name:
            fail(f"{rel}: metadata.name differs from catalog", errors)
        if metadata.get("version") != version:
            fail(f"{rel}: metadata.version differs from catalog", errors)
        if not metadata.get("description"):
            fail(f"{rel}: metadata.description is required", errors)
        if not isinstance(doc.get("spec"), dict):
            fail(f"{rel}: spec must be a mapping", errors)
            continue

        versions.setdefault((kind, name), set()).add(version)
        docs.append((rel, kind, name, version, doc))

    disk_paths: set[str] = set()
    for directory in RESOURCE_DIRS.values():
        root = ROOT / directory
        if not root.exists():
            continue
        for path in root.glob("*.yaml"):
            disk_paths.add(path.relative_to(ROOT).as_posix())
    for rel in sorted(disk_paths - catalog_paths):
        fail(f"{rel}: resource manifest is not indexed in catalog.yaml", errors)
    for rel in sorted(catalog_paths - disk_paths):
        fail(f"{rel}: catalog path is not a recognized resource manifest", errors)

    for rel, kind, name, _version, doc in docs:
        spec = doc["spec"]
        validate_dependency_map(rel, "spec.requires", spec.get("requires"), versions, errors)
        if kind == "Bundle":
            validate_dependency_map(rel, "spec.imports", spec.get("imports"), versions, errors)

        extends = spec.get("extends")
        if extends is not None:
            validate_selector(rel, "spec.extends", kind, extends, versions, errors)

        if kind == "Profile":
            interaction = spec.get("interaction") or {}
            if name == "hermes":
                if interaction.get("userFacing") is not True:
                    fail(f"{rel}: Hermes must be userFacing=true", errors)
                if interaction.get("directUserContact") != "allow":
                    fail(f"{rel}: Hermes must allow directUserContact", errors)
                if interaction.get("userChannelBinding") != "allow":
                    fail(f"{rel}: Hermes must allow userChannelBinding", errors)
                if interaction.get("soleUserEntryPoint") is not True:
                    fail(f"{rel}: Hermes must be soleUserEntryPoint=true", errors)
            else:
                if interaction.get("userFacing") is True:
                    fail(f"{rel}: only Hermes may be userFacing=true", errors)
                if interaction.get("directUserContact") == "allow":
                    fail(f"{rel}: only Hermes may allow directUserContact", errors)
                if interaction.get("userChannelBinding") == "allow":
                    fail(f"{rel}: only Hermes may allow userChannelBinding", errors)
            validate_composio_policy(rel, spec, errors)

        if kind == "Channel" and name in USER_CHANNELS:
            routing = spec.get("routing") or {}
            policy = spec.get("policy") or {}
            if routing.get("inboundProfile") != "hermes":
                fail(f"{rel}: inboundProfile must be hermes", errors)
            if routing.get("outboundProfile") != "hermes":
                fail(f"{rel}: outboundProfile must be hermes", errors)
            if routing.get("allowDirectProfileSelection") is not False:
                fail(f"{rel}: direct profile selection must be disabled", errors)
            if routing.get("allowedUserFacingProfiles") != ["hermes"]:
                fail(f"{rel}: allowedUserFacingProfiles must be exactly [hermes]", errors)
            if policy.get("requireHermesGateway") is not True:
                fail(f"{rel}: requireHermesGateway must be true", errors)
            if policy.get("rejectNonHermesProfileTarget") is not True:
                fail(f"{rel}: rejectNonHermesProfileTarget must be true", errors)

    by_resource = {(kind, name): doc for _rel, kind, name, _version, doc in docs}

    composio = by_resource.get(("Plugin", "composio"), {}).get("spec", {})
    if composio:
        policy = composio.get("policy") or {}
        sessions = composio.get("sessions") or {}
        if policy.get("denyUnlistedToolkits") is not True:
            fail("plugins/composio.yaml: denyUnlistedToolkits must be true", errors)
        if policy.get("remoteWorkbench") != "deny" or policy.get("remoteBash") != "deny":
            fail("plugins/composio.yaml: remote workbench and bash must be denied", errors)
        if sessions.get("requireToolkitAllowlist") is not True:
            fail("plugins/composio.yaml: toolkit allowlists must be required", errors)

    agent37 = by_resource.get(("Plugin", "agent37-discovery"), {}).get("spec", {})
    if agent37:
        policy = agent37.get("policy") or {}
        if policy.get("autoInstall") is not False or policy.get("autoExecute") is not False:
            fail("plugins/agent37-discovery.yaml: auto-install and auto-execute must stay disabled", errors)
        if policy.get("requireSourceRepositoryReview") is not True:
            fail("plugins/agent37-discovery.yaml: source repository review must be required", errors)

    home_assistant = by_resource.get(("MCP", "home-assistant"), {}).get("spec", {})
    if home_assistant:
        if home_assistant.get("endpoint") != "${HOME_ASSISTANT_URL}/api/mcp":
            fail("mcps/home-assistant.yaml: canonical endpoint must be ${HOME_ASSISTANT_URL}/api/mcp", errors)
        if (home_assistant.get("provenance") or {}).get("officialIntegration") != "mcp_server":
            fail("mcps/home-assistant.yaml: official Home Assistant MCP provenance is required", errors)

    orchestrator = by_resource.get(("Profile", "orchestrator"), {}).get("spec", {})
    if orchestrator:
        orchestration = orchestrator.get("orchestration") or {}
        recruitment = orchestrator.get("recruitment") or {}
        kanban = orchestrator.get("kanban") or {}
        if orchestration.get("parallelExecution") is not True or orchestration.get("hierarchicalDelegation") is not True:
            fail("profiles/orchestrator.yaml: parallel and hierarchical orchestration must stay enabled", errors)
        if orchestration.get("executionModel") != "dependency-dag":
            fail("profiles/orchestrator.yaml: executionModel must remain dependency-dag", errors)
        if recruitment.get("allowMultipleInstancesPerProfile") is not True:
            fail("profiles/orchestrator.yaml: multiple instances per profile must be allowed", errors)
        if recruitment.get("registryMaxInstancesPerProfile") != "none":
            fail("profiles/orchestrator.yaml: registry must not impose a numeric per-profile instance ceiling", errors)
        if recruitment.get("effectiveInstanceLimit") != "host-policy":
            fail("profiles/orchestrator.yaml: effective instance limit must remain host-policy", errors)
        if kanban.get("oneBoardPerEpic") is not True or kanban.get("deleteOnAcceptedDone") is not True:
            fail("profiles/orchestrator.yaml: one ephemeral board per Epic is required", errors)

    team_leader = by_resource.get(("Profile", "team-leader"), {}).get("spec", {})
    if team_leader:
        recruitment = team_leader.get("recruitment") or {}
        orchestration = team_leader.get("orchestration") or {}
        if recruitment.get("allowMultipleInstancesPerProfile") is not True:
            fail("profiles/team-leader.yaml: multiple profile instances must be supported", errors)
        if orchestration.get("parallelSubteams") is not True or orchestration.get("nestedDelegation") is not True:
            fail("profiles/team-leader.yaml: parallel nested subteams must stay enabled", errors)

    overlay_store = by_resource.get(("Plugin", "resource-overlay-store"), {}).get("spec", {})
    if overlay_store:
        policy = overlay_store.get("policy") or {}
        if policy.get("gitSync") != "deny" or policy.get("networkExport") != "deny":
            fail("plugins/resource-overlay-store.yaml: private overlays must not sync/export", errors)
        if policy.get("atomicWrites") is not True or policy.get("versionHistory") is not True:
            fail("plugins/resource-overlay-store.yaml: atomic writes and version history are required", errors)

    evolution = by_resource.get(("Profile", "resource-evolution-manager"), {}).get("spec", {})
    if evolution:
        merge = evolution.get("mergePolicy") or {}
        apply = evolution.get("applyPolicy") or {}
        expected_layers = ["local-experience-overlay", "private-user-learned-overlay"]
        if merge.get("neverOverwriteLayers") != expected_layers:
            fail("profiles/resource-evolution-manager.yaml: learned/local overlays must be protected", errors)
        if merge.get("privateLayersMayPublish") is not False:
            fail("profiles/resource-evolution-manager.yaml: private overlays must never auto-publish", errors)
        if apply.get("atomicActivation") is not True or apply.get("rollbackSnapshot") is not True:
            fail("profiles/resource-evolution-manager.yaml: atomic activation and rollback are required", errors)

    reconcile = by_resource.get(("Cron", "daily-resource-reconcile"), {}).get("spec", {})
    if reconcile:
        policy = reconcile.get("policy") or {}
        if policy.get("autoApply") != "safe-compatible-only":
            fail("crons/daily-resource-reconcile.yaml: only safe compatible changes may auto-apply", errors)
        if policy.get("preserveLocalExperienceOverlay") is not True or policy.get("preservePrivateUserLearnedOverlay") is not True:
            fail("crons/daily-resource-reconcile.yaml: both learned overlays must be preserved", errors)
        if policy.get("publishPrivateOverlays") is not False:
            fail("crons/daily-resource-reconcile.yaml: private overlays must not publish", errors)

    epic_kanban = by_resource.get(("Plugin", "epic-kanban"), {}).get("spec", {})
    if epic_kanban:
        lifecycle = epic_kanban.get("lifecycle") or {}
        if lifecycle.get("createOnEpicStart") is not True or lifecycle.get("deleteAfterAcceptedDone") is not True:
            fail("plugins/epic-kanban.yaml: Epic boards must be created and deleted with Epic lifecycle", errors)
        if lifecycle.get("archiveCompletionSummary") is not True:
            fail("plugins/epic-kanban.yaml: completion summary must be archived before deletion", errors)

    voice = by_resource.get(("Plugin", "voice-pipeline"), {}).get("spec", {})
    if voice:
        policy = voice.get("policy") or {}
        if policy.get("localFirst") is not True or policy.get("cloudFallback") != "deny":
            fail("plugins/voice-pipeline.yaml: voice must remain local-first with cloud fallback denied", errors)
        if policy.get("rawAudioRetention") is not False:
            fail("plugins/voice-pipeline.yaml: raw audio retention must stay disabled", errors)
        if (voice.get("textToSpeech") or {}).get("preferred") != "piper":
            fail("plugins/voice-pipeline.yaml: Piper must remain the preferred local TTS", errors)

    whatsapp = by_resource.get(("Channel", "whatsapp"), {}).get("spec", {})
    if whatsapp:
        integration = whatsapp.get("integration") or {}
        policy = whatsapp.get("policy") or {}
        if integration.get("toolkit") != "whatsapp":
            fail("channels/whatsapp.yaml: Composio whatsapp toolkit is required", errors)
        if not COMPOSIO_VERSION_RE.fullmatch(str(integration.get("version", ""))):
            fail("channels/whatsapp.yaml: toolkit version must be pinned", errors)
        if policy.get("businessAccountsOnly") is not True:
            fail("channels/whatsapp.yaml: personal WhatsApp accounts must not be supported", errors)
        if policy.get("proactiveOutbound") != "delegated-template-only":
            fail("channels/whatsapp.yaml: proactive outbound must remain delegated-template-only", errors)
        if policy.get("accountAdministration") != "deny":
            fail("channels/whatsapp.yaml: WhatsApp account administration must stay denied", errors)

    if errors:
        print("Registry validation failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print(f"Registry OK: {len(seen)} resources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
