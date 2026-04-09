#!/usr/bin/env python3
"""Restructure graph to v5 narrow-top taxonomy.

Rewrites category paths via PATH_MAP (old path prefix -> new path prefix).
Projects are untouched; their CATEGORY_OF edge targets get rewritten to the
new category IDs. Descriptions are preserved where present (they're all
blank right now, but future-proof).
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODES = ROOT / "graph" / "nodes.json"
EDGES = ROOT / "graph" / "edges.json"

# Old top-level -> new path prefix (as tuple of path segments).
# Longer/more-specific rules must come before shorter ones.
PATH_MAP = [
    # Context Store sub-splits
    (("Context Store", "Context"),                 ("Context, Memory & Data", "Context")),
    (("Context Store", "Context Optimisation"),    ("Context, Memory & Data", "Context", "Optimisation")),
    (("Context Store", "Memory"),                   ("Context, Memory & Data", "Memory")),
    (("Context Store", "Personal AI"),              ("Context, Memory & Data", "Memory", "Personal AI")),
    (("Context Store", "Session State Management"), ("Context, Memory & Data", "Memory", "Session State")),
    (("Context Store", "RAG"),                       ("Context, Memory & Data", "Data", "RAG")),
    (("Context Store", "Vector Databases"),          ("Context, Memory & Data", "Data", "Vector Databases")),
    (("Context Store", "Semantic Search"),           ("Context, Memory & Data", "Data", "Semantic Search")),
    (("Context Store", "Embedding Pipeline Orchestrators"), ("Context, Memory & Data", "Data", "Embedding Pipelines")),
    (("Context Store",),                             ("Context, Memory & Data",)),  # fallback: anything else
    # Storage / Grounding fold into Data
    (("Storage",),                                   ("Context, Memory & Data", "Data", "Storage")),
    (("Grounding",),                                 ("Context, Memory & Data", "Data", "Grounding")),
    # Agents absorptions
    (("Agent to Agent",),                            ("Agents", "Agent to Agent")),
    (("Agent Tools",),                               ("Agents", "Tools")),
    (("Simulations & Worlds",),                      ("Agents", "Simulations & Worlds")),
    # Frameworks absorbs Pipelines
    (("Pipelines",),                                 ("Frameworks & Runtimes", "Pipelines")),
    # Models & Inference merge
    (("Models",),                                    ("Models & Inference", "Models")),
    (("Inference",),                                 ("Models & Inference", "Inference")),
    # Tools & Integrations merge
    (("Actions",),                                   ("Tools & Integrations", "Actions")),
    (("MCP",),                                       ("Tools & Integrations", "MCP")),
    (("Standards",),                                 ("Tools & Integrations", "Standards")),
    # Interfaces merge
    (("Frontends",),                                 ("Interfaces", "Frontends")),
    (("Interfaces & Workspaces",),                   ("Interfaces",)),  # absorb children directly
    # Dev Tools & Skills absorbs Prompts
    (("Prompts",),                                   ("Dev Tools & Skills", "Prompts")),
    # Renames (top-level)
    (("Observability",),                             ("Observability & Evals",)),
    (("Safety",),                                    ("Safety & Governance",)),
    # Ecosystem bucket
    (("Organisations",),                             ("Ecosystem", "Organisations")),
    (("Uncategorized",),                             ("Ecosystem", "Uncategorized")),
    (("Destinations",),                              ("Ecosystem", "Destinations")),
    # Identity passes (kept for clarity; handled by default if unmatched)
    (("Agents",),                                    ("Agents",)),
    (("Frameworks & Runtimes",),                     ("Frameworks & Runtimes",)),
    (("Dev Tools & Skills",),                        ("Dev Tools & Skills",)),
    (("Builders & Platforms",),                      ("Builders & Platforms",)),
]

def remap_path(path):
    p = tuple(path)
    for old, new in PATH_MAP:
        if p[:len(old)] == old:
            return list(new) + list(p[len(old):])
    return list(p)  # unknown top-level — leave alone

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def cat_id(path):
    return "cat:" + "/".join(slugify(s) for s in path)

def main():
    nodes = json.loads(NODES.read_text())
    edges = json.loads(EDGES.read_text())

    # Build old_id -> new_id map for categories, and ensure all ancestor cats exist.
    old_to_new = {}
    new_cats = {}  # new_id -> node dict
    project_nodes = []

    for n in nodes["nodes"]:
        if n["type"] == "Category":
            new_path = remap_path(n["path"])
            new_id = cat_id(new_path)
            old_to_new[n["id"]] = new_id
            # Merge: if multiple old cats collapse to same new id, keep first desc
            if new_id not in new_cats:
                new_cats[new_id] = {
                    "id": new_id,
                    "type": "Category",
                    "label": new_path[-1],
                    "path": new_path,
                    "description": n.get("description", "") or "",
                }
            else:
                # preserve any non-empty description
                if not new_cats[new_id]["description"] and n.get("description"):
                    new_cats[new_id]["description"] = n["description"]
        else:
            project_nodes.append(n)

    # Ensure every ancestor category exists
    def ensure_ancestors(path):
        for i in range(1, len(path)):
            ancestor = path[:i]
            aid = cat_id(ancestor)
            if aid not in new_cats:
                new_cats[aid] = {
                    "id": aid,
                    "type": "Category",
                    "label": ancestor[-1],
                    "path": list(ancestor),
                    "description": "",
                }

    for c in list(new_cats.values()):
        ensure_ancestors(c["path"])

    # Rebuild edges
    new_edges = []
    # SUBCATEGORY_OF from path
    for c in new_cats.values():
        if len(c["path"]) > 1:
            parent = cat_id(c["path"][:-1])
            new_edges.append({"from": c["id"], "to": parent, "type": "SUBCATEGORY_OF"})
    # CATEGORY_OF for projects — rewrite via old_to_new
    for e in edges["edges"]:
        if e["type"] == "CATEGORY_OF":
            new_to = old_to_new.get(e["to"], e["to"])
            new_edges.append({"from": e["from"], "to": new_to, "type": "CATEGORY_OF"})
        # drop old SUBCATEGORY_OF (rebuilt above)

    # Write
    out_nodes = {
        "updated": "2026-04-09",
        "nodes": sorted(new_cats.values(), key=lambda n: n["id"]) + sorted(project_nodes, key=lambda n: n["id"]),
    }
    out_edges = {"updated": "2026-04-09", "edges": new_edges}

    NODES.write_text(json.dumps(out_nodes, indent=2, ensure_ascii=False) + "\n")
    EDGES.write_text(json.dumps(out_edges, indent=2, ensure_ascii=False) + "\n")

    # Report
    tops = sorted({c["path"][0] for c in new_cats.values()})
    print(f"categories: {len(new_cats)}  projects: {len(project_nodes)}  top-level: {len(tops)}")
    for t in tops:
        print(f"  - {t}")

if __name__ == "__main__":
    main()
