#!/usr/bin/env python3
"""Apply schema/proposed.yaml to graph/nodes.json + graph/edges.json.

Idempotent: safe to re-run. For each segment in proposed.yaml:
  * Create the top-level category node if missing.
  * For each label in `absorbs`, re-parent the current root with that label
    under the new top-level segment (adds a SUBCATEGORY_OF edge).
  * Recursively create declared `children` as new category nodes under it.

Node IDs are opaque (cat:<slug>) and remain stable — we do not rename
existing IDs. The `path` field on re-parented nodes is recomputed so
the graph stays self-consistent for tools that read it.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
NODES = ROOT / "graph" / "nodes.json"
EDGES = ROOT / "graph" / "edges.json"
PROPOSED = ROOT / "schema" / "proposed.yaml"


def slug(s: str) -> str:
    s = s.lower().strip()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "unnamed"


def main() -> None:
    nodes_data = json.loads(NODES.read_text())
    edges_data = json.loads(EDGES.read_text())
    proposed = yaml.safe_load(PROPOSED.read_text())

    nodes: dict[str, dict] = {n["id"]: n for n in nodes_data["nodes"]}
    edges: list[dict] = edges_data["edges"]

    # Index current SUBCATEGORY_OF edges: child -> parent
    parent_of: dict[str, str] = {}
    for e in edges:
        if e["type"] == "SUBCATEGORY_OF":
            parent_of[e["from"]] = e["to"]

    # Label → id lookup for current root categories only
    label_to_root_id: dict[str, str] = {}
    for n in nodes.values():
        if n["type"] == "Category" and n["id"] not in parent_of:
            label_to_root_id[n["label"]] = n["id"]

    def ensure_category(label: str, parent_id: str | None, kind: str | None = None) -> str:
        """Create (or reuse) a category node. Returns its id.

        If parent_id is None, this is a root. Otherwise a SUBCATEGORY_OF edge
        is added (if not already present).
        """
        # Prefer reusing an existing root with the same label
        existing_id = label_to_root_id.get(label)
        if existing_id is None:
            # Slug-based id; if it clashes with a non-root node, disambiguate
            base = f"cat:{slug(label)}"
            cid = base
            suffix = 2
            while cid in nodes and nodes[cid]["label"] != label:
                cid = f"{base}-{suffix}"
                suffix += 1
        else:
            cid = existing_id

        if cid not in nodes:
            nodes[cid] = {
                "id": cid,
                "type": "Category",
                "label": label,
                "path": [],  # recomputed below
                "short_description": "",
                "long_description": "",
                "examples_narrative": "",
            }

        if kind:
            nodes[cid]["kind"] = kind

        if parent_id is not None:
            # Add edge if missing; re-parent if currently pointing elsewhere
            current_parent = parent_of.get(cid)
            if current_parent != parent_id:
                # Remove any existing SUBCATEGORY_OF edge from this node
                for e in list(edges):
                    if e["type"] == "SUBCATEGORY_OF" and e["from"] == cid:
                        edges.remove(e)
                edges.append({"from": cid, "to": parent_id, "type": "SUBCATEGORY_OF"})
                parent_of[cid] = parent_id
                # It is no longer a root under this label
                if label_to_root_id.get(label) == cid:
                    del label_to_root_id[label]
        else:
            # Root: ensure no SUBCATEGORY_OF edge exists from it
            label_to_root_id[label] = cid

        return cid

    def recurse_children(parent_id: str, children_spec: list[dict]) -> None:
        for ch in children_spec or []:
            cid = ensure_category(ch["name"], parent_id)
            if ch.get("children"):
                recurse_children(cid, ch["children"])

    # --- Apply top-level segments from proposed.yaml ---
    for seg in proposed["segments"]:
        top_id = ensure_category(seg["name"], None, kind=seg.get("kind"))

        # Absorb listed labels under this new top-level
        for absorbed_label in seg.get("absorbs", []) or []:
            if absorbed_label == seg["name"]:
                continue  # self-absorb is a no-op
            absorbed_id = label_to_root_id.get(absorbed_label)
            if absorbed_id is None:
                # Not found as a current root — might already have been
                # absorbed by a previous run, or might not exist at all.
                # Try matching any category by label as a fallback.
                match = [
                    nid for nid, n in nodes.items()
                    if n["type"] == "Category" and n["label"] == absorbed_label
                ]
                if not match:
                    print(f"  skip: no category labelled {absorbed_label!r}")
                    continue
                absorbed_id = match[0]
            # Re-parent the absorbed category under the new top
            if parent_of.get(absorbed_id) != top_id:
                for e in list(edges):
                    if e["type"] == "SUBCATEGORY_OF" and e["from"] == absorbed_id:
                        edges.remove(e)
                edges.append({"from": absorbed_id, "to": top_id, "type": "SUBCATEGORY_OF"})
                parent_of[absorbed_id] = top_id
                label_to_root_id.pop(absorbed_label, None)

        # Create declared children under this top-level
        recurse_children(top_id, seg.get("children") or [])

    # --- Recompute path fields top-down ---
    # Build reverse index
    children_of: dict[str, list[str]] = {}
    for child, par in parent_of.items():
        children_of.setdefault(par, []).append(child)

    roots = [nid for nid, n in nodes.items()
             if n["type"] == "Category" and nid not in parent_of]

    def set_path(nid: str, path: list[str]) -> None:
        nodes[nid]["path"] = path
        for c in children_of.get(nid, []):
            set_path(c, path + [nodes[c]["label"]])

    for rid in roots:
        set_path(rid, [nodes[rid]["label"]])

    # --- Write back ---
    nodes_data["nodes"] = list(nodes.values())
    edges_data["edges"] = edges
    nodes_data["updated"] = "2026-04-09"
    edges_data["updated"] = "2026-04-09"

    NODES.write_text(json.dumps(nodes_data, indent=2) + "\n")
    EDGES.write_text(json.dumps(edges_data, indent=2) + "\n")

    cat_count = sum(1 for n in nodes.values() if n["type"] == "Category")
    root_count = len(roots)
    print(f"applied proposed.yaml v{proposed.get('version','?')}")
    print(f"  categories: {cat_count}")
    print(f"  roots:      {root_count}")


if __name__ == "__main__":
    main()
