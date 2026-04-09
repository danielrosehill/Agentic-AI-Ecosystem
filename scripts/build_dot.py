#!/usr/bin/env python3
"""Generate Graphviz .dot files and render PDF/PNG/SVG snapshots.

Outputs under snapshots/<ISO-date>/:
  ecosystem.dot / .pdf / .png / .svg              — full map (twopi, radial)
  ecosystem-tree.dot / .pdf / .png / .svg         — full map (dot, hierarchical)
  segments/<slug>.dot / .pdf / .png / .svg        — one per top-level segment

Requires graphviz (`dot`, `twopi`) on PATH.
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODES_IN = ROOT / "graph" / "nodes.json"
EDGES_IN = ROOT / "graph" / "edges.json"
OUT_BASE = ROOT / "snapshots"

CAT_COLOR = "#6aa9ff"
CAT_HUB_COLOR = "#1f6feb"
PROJ_COLOR = "#f59e0b"
EDGE_COLOR = "#c8cfdb"
BG_COLOR = "#f7f8fa"
FONT = "Helvetica"


def slug(s: str) -> str:
    s = s.lower().strip()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "unnamed"


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def load():
    nodes = {n["id"]: n for n in json.loads(NODES_IN.read_text())["nodes"]}
    edges = json.loads(EDGES_IN.read_text())["edges"]
    return nodes, edges


def degree(edges):
    d: dict[str, int] = {}
    for e in edges:
        d[e["from"]] = d.get(e["from"], 0) + 1
        d[e["to"]] = d.get(e["to"], 0) + 1
    return d


def emit_dot(nodes, edges, title, engine="twopi") -> str:
    deg = degree(edges)
    lines = [f'digraph G {{']
    lines.append(f'  graph [layout={engine}, overlap=false, splines=true, '
                 f'bgcolor="{BG_COLOR}", fontname="{FONT}", labelloc="t", '
                 f'label="{esc(title)}", fontsize=22, pad=0.4];')
    lines.append(f'  node [fontname="{FONT}", style="filled", '
                 f'penwidth=0, fontcolor="#1a1f2c"];')
    lines.append(f'  edge [color="{EDGE_COLOR}", arrowsize=0.5, penwidth=0.8];')

    node_ids = {n["id"] for n in nodes.values()}

    for nid, n in nodes.items():
        is_proj = n["type"] == "Project"
        if is_proj:
            shape = "diamond"
            color = PROJ_COLOR
            size = 0.4
            fontsize = 9
        else:
            shape = "circle"
            d = deg.get(nid, 0)
            color = CAT_HUB_COLOR if d > 8 else CAT_COLOR
            size = 0.5 + min(d, 20) * 0.07
            fontsize = 11 if d > 8 else 10
        label = n["label"]
        tooltip = (n.get("short_description") or "") if not is_proj else (n.get("url") or "")
        url = n.get("url", "") if is_proj else ""
        attrs = [
            f'label="{esc(label)}"',
            f'shape={shape}',
            f'fillcolor="{color}"',
            f'width={size:.2f}',
            f'height={size:.2f}',
            f'fontsize={fontsize}',
            f'tooltip="{esc(tooltip)}"',
        ]
        if url:
            attrs.append(f'URL="{esc(url)}"')
        lines.append(f'  "{nid}" [{", ".join(attrs)}];')

    # Flip edges: parent -> child for readable hierarchy.
    for e in edges:
        if e["from"] not in node_ids or e["to"] not in node_ids:
            continue
        if e["type"] in ("SUBCATEGORY_OF", "CATEGORY_OF"):
            src, dst = e["to"], e["from"]
        else:
            src, dst = e["from"], e["to"]
        lines.append(f'  "{src}" -> "{dst}";')

    lines.append("}")
    return "\n".join(lines)


def render(dot_path: Path, engine: str) -> None:
    for fmt in ("pdf", "png", "svg"):
        out = dot_path.with_suffix(f".{fmt}")
        try:
            subprocess.run(
                [engine, f"-T{fmt}", str(dot_path), "-o", str(out)],
                check=True, capture_output=True, text=True,
            )
        except subprocess.CalledProcessError as e:
            sys.stderr.write(
                f"{engine} failed on {dot_path.name} ({fmt}): {e.stderr}\n"
            )


def subgraph_for_segment(all_nodes, all_edges, seg_root_id):
    """Collect every descendant of seg_root_id (categories + their projects)."""
    keep_cats = {seg_root_id}
    changed = True
    child_of: dict[str, list[str]] = {}
    for e in all_edges:
        if e["type"] == "SUBCATEGORY_OF":
            child_of.setdefault(e["to"], []).append(e["from"])
    stack = [seg_root_id]
    while stack:
        cur = stack.pop()
        for ch in child_of.get(cur, []):
            if ch not in keep_cats:
                keep_cats.add(ch)
                stack.append(ch)
    # Include projects attached to any kept category
    keep = set(keep_cats)
    for e in all_edges:
        if e["type"] == "CATEGORY_OF" and e["to"] in keep_cats:
            keep.add(e["from"])
    nodes = {nid: n for nid, n in all_nodes.items() if nid in keep}
    edges = [
        e for e in all_edges
        if e["from"] in keep and e["to"] in keep
    ]
    return nodes, edges


def main() -> None:
    nodes, edges = load()

    stamp = date.today().isoformat()
    out_dir = OUT_BASE / stamp
    (out_dir / "segments").mkdir(parents=True, exist_ok=True)

    # Full map — radial and hierarchical
    for name, engine in (("ecosystem", "twopi"), ("ecosystem-tree", "dot")):
        dot_path = out_dir / f"{name}.dot"
        dot_path.write_text(emit_dot(nodes, edges, "Agentic AI Ecosystem", engine=engine))
        render(dot_path, engine)
        print(f"  {dot_path.relative_to(ROOT)}")

    # Per-segment (top-level categories)
    segments = [
        n for n in nodes.values()
        if n["type"] == "Category" and len(n.get("path", [])) == 1
    ]
    segments.sort(key=lambda n: n["label"].lower())
    for seg in segments:
        sub_nodes, sub_edges = subgraph_for_segment(nodes, edges, seg["id"])
        if len(sub_nodes) <= 1:
            continue  # empty segment — skip
        dot_path = out_dir / "segments" / f"{slug(seg['label'])}.dot"
        dot_path.write_text(emit_dot(sub_nodes, sub_edges, seg["label"], engine="dot"))
        render(dot_path, "dot")
        print(f"  {dot_path.relative_to(ROOT)}")

    print(f"\nwrote snapshot {out_dir.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
