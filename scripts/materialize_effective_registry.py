#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from validate_quality_v22 import ROOT, effective_spec, load_yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Materialize catalog resources with QUALITY_POLICY defaults/domain overlays applied without resolving secrets."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "build" / "effective-registry",
        help="Output directory (default: build/effective-registry)",
    )
    parser.add_argument(
        "--resource",
        help="Optional resource name to materialize; all catalog resources are processed when omitted.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Compute effective resources and report counts without writing output files.",
    )
    return parser.parse_args()


def materialize_one(entry: dict[str, Any], policy: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    rel = entry["path"]
    doc = load_yaml(ROOT / rel)
    metadata = doc.get("metadata") or {}
    tags = set(metadata.get("tags") or []) if isinstance(metadata.get("tags") or [], list) else set()
    effective, overlays = effective_spec(entry["kind"], entry["name"], tags, doc.get("spec") or {}, policy)

    result = {
        "apiVersion": doc.get("apiVersion"),
        "kind": doc.get("kind"),
        "metadata": dict(metadata),
        "spec": effective,
        "materialization": {
            "qualityPolicy": "registry-quality@2.2.0",
            "qualityDomainOverlays": overlays,
            "declaredManifest": rel,
            "secretsResolved": False,
            "authorizationExpanded": False,
        },
    }
    return result, overlays


def main() -> int:
    args = parse_args()
    policy_doc = load_yaml(ROOT / "QUALITY_POLICY.yaml")
    policy = policy_doc.get("spec") or {}
    catalog = load_yaml(ROOT / "catalog.yaml")
    entries = [entry for entry in (catalog.get("resources") or []) if isinstance(entry, dict)]

    if args.resource:
        entries = [entry for entry in entries if entry.get("name") == args.resource]
        if not entries:
            raise SystemExit(f"No catalog resource named {args.resource!r}")

    kind_counts: dict[str, int] = {}
    overlay_counts: dict[str, int] = {}
    materialized: list[tuple[dict[str, Any], dict[str, Any]]] = []

    for entry in entries:
        if entry.get("kind") not in {"Profile", "Skill", "Plugin", "MCP", "Channel", "Cron", "Webhook", "Bundle"}:
            continue
        result, overlays = materialize_one(entry, policy)
        materialized.append((entry, result))
        kind = str(entry["kind"])
        kind_counts[kind] = kind_counts.get(kind, 0) + 1
        for overlay in overlays:
            overlay_counts[overlay] = overlay_counts.get(overlay, 0) + 1

    if not args.check_only:
        output = args.output.resolve()
        output.mkdir(parents=True, exist_ok=True)
        for entry, result in materialized:
            relative = Path(str(entry["path"]))
            target = output / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                yaml.safe_dump(result, sort_keys=False, allow_unicode=True, width=120),
                encoding="utf-8",
            )

        manifest = {
            "qualityPolicy": "registry-quality@2.2.0",
            "catalogVersion": (catalog.get("metadata") or {}).get("version"),
            "resourceCount": len(materialized),
            "kinds": dict(sorted(kind_counts.items())),
            "domainOverlays": dict(sorted(overlay_counts.items())),
            "secretsResolved": False,
        }
        (output / "MATERIALIZATION.yaml").write_text(
            yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8"
        )

    kinds = ", ".join(f"{kind}={count}" for kind, count in sorted(kind_counts.items()))
    mode = "checked" if args.check_only else f"materialized to {args.output}"
    print(f"Effective registry {mode}: {len(materialized)} resources ({kinds})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
