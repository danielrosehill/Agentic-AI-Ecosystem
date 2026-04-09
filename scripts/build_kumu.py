#!/usr/bin/env python3
"""Generate Kumu-ready CSVs from graph/nodes.json + graph/edges.json.

Writes:
  kumu/elements.csv     — one row per node (Kumu "elements")
  kumu/connections.csv  — one row per edge (Kumu "connections")

Labels are the leaf name only (e.g. "Frameworks", "Voice"), with
collisions disambiguated by appending " (parent)". Edges are flipped
and renamed for top-down visual flow:

  SUBCATEGORY_OF (child -> parent)  -->  CONTAINS     (parent -> child)
  CATEGORY_OF    (project -> category) -> HAS_EXAMPLE (category -> project)

The underlying graph files are untouched — the graph keeps the
semantically-correct direction; Kumu just gets a view that lays out
top-down.
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

BREADCRUMB = " › "  # U+203A, used only in the Path column for filtering


def main() -> None:
    nodes = {n["id"]: n for n in json.loads(NODES_IN.read_text())["nodes"]}
    edges = json.loads(EDGES_IN.read_text())["edges"]

    # Detect label collisions across ALL nodes (categories + projects share
    # a label namespace in Kumu).
    label_counts: Counter = Counter()
    for n in nodes.values():
        label_counts[n["label"]] += 1

    # Project -> its (first) category, for disambiguation hint.
    proj_category: dict[str, str] = {
        e["from"]: e["to"] for e in edges if e["type"] == "CATEGORY_OF"
    }
    # Category -> its parent category.
    cat_parent: dict[str, str] = {
        e["from"]: e["to"] for e in edges if e["type"] == "SUBCATEGORY_OF"
    }

    def kumu_label(node_id: str) -> str:
        n = nodes[node_id]
        base = n["label"]
        if label_counts[base] <= 1:
            return base
        # collision — disambiguate with parent label
        parent_id = (
            cat_parent.get(node_id)
            if n["type"] == "Category"
            else proj_category.get(node_id)
        )
        if parent_id and parent_id in nodes:
            return f"{base} ({nodes[parent_id]['label']})"
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
                    n.get("short_description", "") or "",
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

    # connections.csv — flip direction so parent -> child, rename types
    # for top-down layout semantics.
    edge_type_map = {
        "SUBCATEGORY_OF": "CONTAINS",
        "CATEGORY_OF":    "HAS_EXAMPLE",
    }
    with CONNECTIONS_OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["From", "To", "Type"])
        for e in edges:
            new_type = edge_type_map.get(e["type"], e["type"])
            # flip: original was child->parent; we want parent->child
            frm = kumu_label(e["to"])
            to = kumu_label(e["from"])
            w.writerow([frm, to, new_type])

    cats = sum(1 for n in nodes.values() if n["type"] == "Category")
    projs = sum(1 for n in nodes.values() if n["type"] == "Project")
    print(f"elements:    {len(nodes)} ({cats} categories, {projs} projects)")
    print(f"connections: {len(edges)}")
    print(f"wrote {ELEMENTS_OUT.relative_to(ROOT)}")
    print(f"wrote {CONNECTIONS_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
