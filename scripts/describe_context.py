#!/usr/bin/env python3
"""Dump context for every category with missing descriptions.

Outputs a JSON array to stdout. Each entry is a complete, self-contained
context blob that an agent can use to write short_description,
long_description, and examples_narrative *without* re-exploring the graph.

Used by /describe-missing to build parallel-agent prompts.

Filter options:
  --missing short|long|both     (default: short)
  --max N                       cap the number of entries
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODES_IN = ROOT / "graph" / "nodes.json"
EDGES_IN = ROOT / "graph" / "edges.json"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--missing", choices=["short", "long", "both"], default="short")
    ap.add_argument("--max", type=int, default=0)
    args = ap.parse_args()

    nodes = {n["id"]: n for n in json.loads(NODES_IN.read_text())["nodes"]}
    edges = json.loads(EDGES_IN.read_text())["edges"]

    parent_of = {e["from"]: e["to"] for e in edges if e["type"] == "SUBCATEGORY_OF"}
    children_of: dict[str, list[str]] = {}
    for e in edges:
        if e["type"] == "SUBCATEGORY_OF":
            children_of.setdefault(e["to"], []).append(e["from"])
    projects_of: dict[str, list[str]] = {}
    for e in edges:
        if e["type"] == "CATEGORY_OF":
            projects_of.setdefault(e["to"], []).append(e["from"])

    def empty(n, field):
        return not (n.get(field) or "").strip()

    def needs(n):
        if n["type"] != "Category":
            return False
        if args.missing == "short":
            return empty(n, "short_description")
        if args.missing == "long":
            return empty(n, "long_description")
        return empty(n, "short_description") or empty(n, "long_description")

    out = []
    for nid, n in nodes.items():
        if not needs(n):
            continue
        parent_id = parent_of.get(nid)
        parent = nodes.get(parent_id) if parent_id else None
        siblings = []
        if parent_id:
            for sid in children_of.get(parent_id, []):
                if sid == nid:
                    continue
                s = nodes[sid]
                siblings.append({
                    "label": s["label"],
                    "short": s.get("short_description", "") or "",
                })
        sub_children = [
            {"label": nodes[c]["label"],
             "short": nodes[c].get("short_description", "") or ""}
            for c in children_of.get(nid, [])
        ]
        projects = [nodes[p]["label"] for p in projects_of.get(nid, [])]
        out.append({
            "id": nid,
            "label": n["label"],
            "path": n.get("path", []),
            "parent_id": parent_id,
            "parent_label": parent["label"] if parent else None,
            "parent_short": (parent.get("short_description", "") if parent else "") or "",
            "siblings": siblings,
            "children": sub_children,
            "projects": projects,
            "current_short": n.get("short_description", "") or "",
            "current_long": n.get("long_description", "") or "",
        })

    if args.max:
        out = out[: args.max]

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
