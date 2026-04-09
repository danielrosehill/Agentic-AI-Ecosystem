#!/usr/bin/env python3
"""Regenerate ecosystem.json (tree) from graph/nodes.json + graph/edges.json.

The graph is the source of truth. This script is the inverse of build_graph.py.
It rebuilds the legacy tree shape so that generate_readme.py and any downstream
consumers keep working unchanged.

Ordering: categories and projects are sorted alphabetically (case-insensitive)
at every level, matching the repo's ordering rule.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODES_IN = ROOT / "graph" / "nodes.json"
EDGES_IN = ROOT / "graph" / "edges.json"
TREE_OUT = ROOT / "ecosystem.json"


def main() -> None:
    nodes_data = json.loads(NODES_IN.read_text())
    edges_data = json.loads(EDGES_IN.read_text())
    nodes = {n["id"]: n for n in nodes_data["nodes"]}
    edges = edges_data["edges"]

    # Build adjacency:
    #   parent_of[child_cat_id] = parent_cat_id   (from SUBCATEGORY_OF)
    #   children_of[cat_id] = [child_cat_id, ...]
    #   projects_of[cat_id] = [project_id, ...]
    parent_of: dict[str, str] = {}
    children_of: dict[str, list[str]] = {}
    projects_of: dict[str, list[str]] = {}

    for e in edges:
        if e["type"] == "SUBCATEGORY_OF":
            parent_of[e["from"]] = e["to"]
            children_of.setdefault(e["to"], []).append(e["from"])
        elif e["type"] == "CATEGORY_OF":
            projects_of.setdefault(e["to"], []).append(e["from"])

    # Roots = category nodes with no parent
    roots = [
        n["id"] for n in nodes.values()
        if n["type"] == "Category" and n["id"] not in parent_of
    ]

    def sort_key(label: str) -> str:
        return label.lower()

    def build_category(cat_id: str) -> dict:
        n = nodes[cat_id]
        out: dict = {"name": n["label"]}

        child_ids = sorted(
            children_of.get(cat_id, []),
            key=lambda cid: sort_key(nodes[cid]["label"]),
        )
        if child_ids:
            out["children"] = [build_category(c) for c in child_ids]

        proj_ids = sorted(
            projects_of.get(cat_id, []),
            key=lambda pid: sort_key(nodes[pid]["label"]),
        )
        if proj_ids:
            out["examples"] = [
                {"name": nodes[p]["label"], "url": nodes[p].get("url", "")}
                for p in proj_ids
            ]

        # Preserve empty arrays where build_graph would have seen them —
        # i.e. always emit at least examples for leaves, children for parents,
        # matching the existing schema. The taxonomy-review pass can tidy.
        if "children" not in out and "examples" not in out:
            out["examples"] = []

        out["short_description"] = n.get("short_description", "") or ""
        out["long_description"] = n.get("long_description", "") or ""
        out["examples_narrative"] = n.get("examples_narrative", "") or ""
        return out

    segments = [
        build_category(rid)
        for rid in sorted(roots, key=lambda rid: sort_key(nodes[rid]["label"]))
    ]

    tree = {
        "updated": nodes_data.get("updated"),
        "segments": segments,
    }

    TREE_OUT.write_text(json.dumps(tree, indent=2) + "\n")
    print(f"wrote {TREE_OUT.relative_to(ROOT)}")
    print(f"segments: {len(segments)}")
    print(f"categories: {sum(1 for n in nodes.values() if n['type'] == 'Category')}")
    print(f"projects:   {sum(1 for n in nodes.values() if n['type'] == 'Project')}")


if __name__ == "__main__":
    main()
