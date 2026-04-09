#!/usr/bin/env python3
"""Generate Kumu-ready CSVs from graph/nodes.json + graph/edges.json.

Writes:
  kumu/elements.csv     — one row per node (Kumu "elements")
  kumu/connections.csv  — one row per edge (Kumu "connections")

Kumu uses the `Label` column as the primary identifier. We guarantee
uniqueness by:
  - Categories: Label = breadcrumb, e.g. "Frameworks › Voice"
  - Projects:   Label = project name; on collision append " (parent)"

The From/To fields in connections.csv reference these Labels.
"""
from __future__ import annotations
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODES_IN = ROOT / "graph" / "nodes.json"
EDGES_IN = ROOT / "graph" / "edges.json"
OUT_DIR = ROOT / "kumu"
ELEMENTS_OUT = OUT_DIR / "elements.csv"
CONNECTIONS_OUT = OUT_DIR / "connections.csv"

BREADCRUMB = " › "  # U+203A


def main() -> None:
    nodes = {n["id"]: n for n in json.loads(NODES_IN.read_text())["nodes"]}
    edges = json.loads(EDGES_IN.read_text())["edges"]

    # First pass: detect project-name collisions so we can disambiguate.
    project_name_counts: Counter = Counter()
    for n in nodes.values():
        if n["type"] == "Project":
            project_name_counts[n["label"]] += 1

    # Build Category parent lookup from SUBCATEGORY_OF edges.
    parent_of: dict[str, str] = {
        e["from"]: e["to"] for e in edges if e["type"] == "SUBCATEGORY_OF"
    }
    # Project -> its (first) category, for disambiguation display.
    proj_category: dict[str, str] = {
        e["from"]: e["to"] for e in edges if e["type"] == "CATEGORY_OF"
    }

    def kumu_label(node_id: str) -> str:
        n = nodes[node_id]
        if n["type"] == "Category":
            return BREADCRUMB.join(n["path"])
        # Project
        base = n["label"]
        if project_name_counts[base] > 1:
            parent_id = proj_category.get(node_id)
            parent_tail = (
                nodes[parent_id]["label"] if parent_id and parent_id in nodes else ""
            )
            return f"{base} ({parent_tail})" if parent_tail else base
        return base

    OUT_DIR.mkdir(exist_ok=True)

    # elements.csv
    with ELEMENTS_OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Label", "Type", "Description", "URL", "Path"])
        for nid, n in nodes.items():
            if n["type"] == "Category":
                w.writerow([
                    kumu_label(nid),
                    "Category",
                    n.get("description", "") or "",
                    "",
                    BREADCRUMB.join(n["path"]),
                ])
            else:
                parent_id = proj_category.get(nid)
                path_hint = (
                    BREADCRUMB.join(nodes[parent_id]["path"])
                    if parent_id and parent_id in nodes
                    else ""
                )
                w.writerow([
                    kumu_label(nid),
                    "Project",
                    "",
                    n.get("url", "") or "",
                    path_hint,
                ])

    # connections.csv
    with CONNECTIONS_OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["From", "To", "Type"])
        for e in edges:
            frm = kumu_label(e["from"])
            to = kumu_label(e["to"])
            w.writerow([frm, to, e["type"]])

    cats = sum(1 for n in nodes.values() if n["type"] == "Category")
    projs = sum(1 for n in nodes.values() if n["type"] == "Project")
    print(f"elements:    {len(nodes)} ({cats} categories, {projs} projects)")
    print(f"connections: {len(edges)}")
    print(f"wrote {ELEMENTS_OUT.relative_to(ROOT)}")
    print(f"wrote {CONNECTIONS_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
