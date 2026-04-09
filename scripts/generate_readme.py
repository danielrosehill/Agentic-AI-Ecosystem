#!/usr/bin/env python3
"""Generate README.md from ecosystem.json (segments-first structure).

Shows category descriptions and stable IDs so the README doubles as a
browsable reference to the graph. Project entries are just name + URL.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "ecosystem.json").read_text())
segments = data["segments"]


def slug(s: str) -> str:
    s = s.lower().strip()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "unnamed"


def cat_id(path: list[str]) -> str:
    return "cat:" + "/".join(slug(p) for p in path)


def count_examples(node):
    n = len(node.get("examples", []) or [])
    for c in node.get("children", []) or []:
        n += count_examples(c)
    return n


def anchor(s):
    return s.lower().replace(" ", "-").replace("/", "").replace(".", "")


def render_example(ex):
    if ex.get("url"):
        return f"- [{ex['name']}]({ex['url']})"
    return f"- {ex['name']}"


def render_node(node, path, depth):
    """Render a category node. depth=0 is top-level (## ), depth=1 is ### …"""
    lines = []
    heading = "#" * min(depth + 2, 6)
    full_path = path + [node["name"]]
    cid = cat_id(full_path)
    lines.append(f"{heading} {node['name']}")
    lines.append(f"<sub>`{cid}`</sub>")
    lines.append("")
    short = (node.get("short_description") or node.get("description") or "").strip()
    long_ = (node.get("long_description") or "").strip()
    narrative = (node.get("examples_narrative") or "").strip()
    if short:
        lines.append(f"*{short}*")
        lines.append("")
    if long_:
        lines.append(long_)
        lines.append("")
    for ex in sorted(node.get("examples", []) or [], key=lambda e: e["name"].lower()):
        lines.append(render_example(ex))
    if node.get("examples"):
        lines.append("")
    if narrative:
        lines.append(narrative)
        lines.append("")
    for child in node.get("children", []) or []:
        lines.extend(render_node(child, full_path, depth + 1))
    return lines


lines = [
    "# Agentic AI Ecosystem Map",
    "",
    "## Purpose",
    "",
    "This project maps the **categories, subcategories, and connections** between emerging tooling in the agentic AI space. It is a taxonomy, not a project directory.",
    "",
    "The primary mechanism is **real project → taxonomy**: example projects are collected as evidence that a functional slot exists, and the taxonomy is refined backwards from those examples. A category with one example (or even zero) is valid if it represents a distinct functional slot in an agentic stack.",
    "",
    "Every category has a stable ID (`cat:<slug-path>`) so the taxonomy can be referenced as a foreign key, a Neo4j constraint, or a uniqueness guarantee in downstream tools.",
    "",
    "**Source of truth**: [`graph/nodes.json`](./graph/nodes.json) + [`graph/edges.json`](./graph/edges.json). [`ecosystem.json`](./ecosystem.json) is a regenerated tree view for human reading.",
    "",
    "**Interactive 3D viz**: [danielrosehill.github.io/Agentic-AI-Ecosystem/viz/](https://danielrosehill.github.io/Agentic-AI-Ecosystem/viz/)",
    "",
    "## Segments",
    "",
]
for s in segments:
    lines.append(f"- [{s['name']}](#{anchor(s['name'])})")
lines += ["", "---", ""]

for s in segments:
    lines.extend(render_node(s, [], 0))

(ROOT / "README.md").write_text("\n".join(lines))
print(f"wrote README.md ({len(segments)} segments)")
