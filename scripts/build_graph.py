#!/usr/bin/env python3
"""Convert ecosystem.json (tree) into nodes.json + edges.json (graph).

Graph model:
  Node types : Category, Project
  Edge types : SUBCATEGORY_OF (Category -> parent Category)
               CATEGORY_OF    (Project  -> Category)

IDs:
  cat:<slug-path>     e.g. cat:frameworks/voice
  proj:<slug-name>    e.g. proj:livekit-agents
  Collisions on project slugs are disambiguated by appending the
  parent category slug.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "ecosystem.json"
NODES_OUT = ROOT / "graph" / "nodes.json"
EDGES_OUT = ROOT / "graph" / "edges.json"


def slug(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "unnamed"


def cat_id(path: list[str]) -> str:
    return "cat:" + "/".join(slug(p) for p in path)


def proj_id(name: str, parent_path: list[str], taken: set[str]) -> str:
    base = f"proj:{slug(name)}"
    if base not in taken:
        return base
    # disambiguate with parent category slug
    disambig = f"{base}--{slug(parent_path[-1])}" if parent_path else base
    i = 2
    candidate = disambig
    while candidate in taken:
        candidate = f"{disambig}-{i}"
        i += 1
    return candidate


def walk(node: dict, parent_path: list[str], nodes: list, edges: list, taken: set[str]) -> None:
    path = parent_path + [node["name"]]
    cid = cat_id(path)
    nodes.append({
        "id": cid,
        "type": "Category",
        "label": node["name"],
        "path": path,
        "description": node.get("description", "") or "",
    })
    taken.add(cid)
    if parent_path:
        edges.append({
            "from": cid,
            "to": cat_id(parent_path),
            "type": "SUBCATEGORY_OF",
        })

    for proj in node.get("examples", []) or []:
        pid = proj_id(proj["name"], path, taken)
        taken.add(pid)
        nodes.append({
            "id": pid,
            "type": "Project",
            "label": proj["name"],
            "url": proj.get("url", "") or "",
        })
        edges.append({
            "from": pid,
            "to": cid,
            "type": "CATEGORY_OF",
        })

    for child in node.get("children", []) or []:
        walk(child, path, nodes, edges, taken)


def main() -> None:
    data = json.loads(SRC.read_text())
    nodes: list = []
    edges: list = []
    taken: set[str] = set()

    for segment in data["segments"]:
        walk(segment, [], nodes, edges, taken)

    NODES_OUT.parent.mkdir(exist_ok=True)
    NODES_OUT.write_text(json.dumps({
        "updated": data.get("updated"),
        "nodes": nodes,
    }, indent=2) + "\n")
    EDGES_OUT.write_text(json.dumps({
        "updated": data.get("updated"),
        "edges": edges,
    }, indent=2) + "\n")

    cats = sum(1 for n in nodes if n["type"] == "Category")
    projs = sum(1 for n in nodes if n["type"] == "Project")
    print(f"nodes: {len(nodes)} ({cats} categories, {projs} projects)")
    print(f"edges: {len(edges)}")
    print(f"wrote {NODES_OUT.relative_to(ROOT)} + {EDGES_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
