#!/usr/bin/env python3
"""Validate graph/nodes.json + graph/edges.json.

Checks:
  - ID uniqueness
  - ID slug-format conformance
  - Every edge endpoint exists as a node
  - Every Project has exactly one CATEGORY_OF edge (outgoing)
  - Every non-root Category has exactly one SUBCATEGORY_OF edge (outgoing)
  - No cycles in SUBCATEGORY_OF
  - --strict-descriptions: every Category has a non-empty description

Exit code 0 on success, 1 on failure.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODES_IN = ROOT / "graph" / "nodes.json"
EDGES_IN = ROOT / "graph" / "edges.json"

ID_PATTERN = re.compile(
    r"^(cat|proj):[a-z0-9]+(?:-[a-z0-9]+)*(?:/[a-z0-9]+(?:-[a-z0-9]+)*)*(?:--[a-z0-9]+(?:-[a-z0-9]+)*)?(?:-\d+)?$"
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict-short", action="store_true",
                    help="Fail if any Category has empty short_description")
    ap.add_argument("--strict-long", action="store_true",
                    help="Fail if any Category has empty long_description")
    args = ap.parse_args()

    nodes_data = json.loads(NODES_IN.read_text())
    edges_data = json.loads(EDGES_IN.read_text())
    nodes = nodes_data["nodes"]
    edges = edges_data["edges"]

    errors: list[str] = []
    warnings: list[str] = []

    # 1. ID uniqueness
    seen: dict[str, int] = {}
    for i, n in enumerate(nodes):
        if "id" not in n:
            errors.append(f"node[{i}] missing 'id'")
            continue
        if n["id"] in seen:
            errors.append(f"duplicate id: {n['id']} (indexes {seen[n['id']]}, {i})")
        seen[n["id"]] = i

    # 2. ID slug format
    for n in nodes:
        nid = n.get("id", "")
        if not ID_PATTERN.match(nid):
            errors.append(f"malformed id: {nid!r}")

    # Index for fast lookup
    node_by_id = {n["id"]: n for n in nodes}

    # 3. Edge endpoints exist
    for i, e in enumerate(edges):
        for side in ("from", "to"):
            if e.get(side) not in node_by_id:
                errors.append(f"edge[{i}] {side}={e.get(side)!r} not in nodes")

    # 4 & 5. Outgoing-edge cardinality
    out_cat_of: dict[str, int] = {}
    out_subcat_of: dict[str, int] = {}
    for e in edges:
        if e["type"] == "CATEGORY_OF":
            out_cat_of[e["from"]] = out_cat_of.get(e["from"], 0) + 1
        elif e["type"] == "SUBCATEGORY_OF":
            out_subcat_of[e["from"]] = out_subcat_of.get(e["from"], 0) + 1

    for n in nodes:
        nid = n["id"]
        if n["type"] == "Project":
            c = out_cat_of.get(nid, 0)
            if c == 0:
                errors.append(f"project {nid} has no CATEGORY_OF edge")
            elif c > 1:
                errors.append(f"project {nid} has {c} CATEGORY_OF edges (expected 1)")
        elif n["type"] == "Category":
            c = out_subcat_of.get(nid, 0)
            is_root = (n.get("path") or [None])[0:1] == [n.get("label")] and len(n.get("path", [])) == 1
            if not is_root and c == 0:
                errors.append(f"non-root category {nid} has no SUBCATEGORY_OF edge")
            elif c > 1:
                errors.append(f"category {nid} has {c} SUBCATEGORY_OF edges (expected 0 or 1)")

    # 6. Cycle detection in SUBCATEGORY_OF
    parent: dict[str, str] = {
        e["from"]: e["to"] for e in edges if e["type"] == "SUBCATEGORY_OF"
    }
    for start in parent:
        seen_path = {start}
        cur = parent.get(start)
        while cur is not None:
            if cur in seen_path:
                errors.append(f"cycle in SUBCATEGORY_OF involving {cur}")
                break
            seen_path.add(cur)
            cur = parent.get(cur)

    # 7. Description coverage
    def empty(n, field):
        return not (n.get(field) or "").strip()

    total_cats = sum(1 for n in nodes if n["type"] == "Category")
    empty_short = [n["id"] for n in nodes if n["type"] == "Category" and empty(n, "short_description")]
    empty_long  = [n["id"] for n in nodes if n["type"] == "Category" and empty(n, "long_description")]

    if args.strict_short:
        for nid in empty_short:
            errors.append(f"category {nid} has empty short_description (strict mode)")
    elif empty_short:
        warnings.append(
            f"{len(empty_short)}/{total_cats} categories have empty short_description"
        )

    if args.strict_long:
        for nid in empty_long:
            errors.append(f"category {nid} has empty long_description (strict mode)")
    elif empty_long:
        warnings.append(
            f"{len(empty_long)}/{total_cats} categories have empty long_description"
        )

    # Report
    cats = sum(1 for n in nodes if n["type"] == "Category")
    projs = sum(1 for n in nodes if n["type"] == "Project")
    print(f"nodes: {len(nodes)} ({cats} categories, {projs} projects)")
    print(f"edges: {len(edges)}")

    if warnings:
        print(f"\nwarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  ⚠ {w}")

    if errors:
        print(f"\nerrors ({len(errors)}):")
        for e in errors[:50]:
            print(f"  ✗ {e}")
        if len(errors) > 50:
            print(f"  … and {len(errors) - 50} more")
        return 1

    print("\n✓ validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
