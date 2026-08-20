#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required: python3 -m pip install pyyaml", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
API_VERSION = "hermes.togarriapa/v1"
VALID_KINDS = {"Profile", "Skill", "Plugin", "MCP", "Cron", "Webhook", "Channel", "Bundle"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def fail(message: str, errors: list[str]):
    errors.append(message)


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

    seen: set[tuple[str, str, str]] = set()
    for entry in catalog.get("resources", []):
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

        path = (ROOT / rel).resolve()
        if ROOT not in path.parents:
            fail(f"{rel}: path escapes repository", errors)
            continue
        if not path.is_file():
            fail(f"{rel}: file is missing", errors)
            continue

        doc = load_yaml(path) or {}
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

    if errors:
        print("Registry validation failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print(f"Registry OK: {len(seen)} resources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
