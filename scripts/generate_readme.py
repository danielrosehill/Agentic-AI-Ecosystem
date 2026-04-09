#!/usr/bin/env python3
"""Generate README.md from ecosystem.json (segments-first structure)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "ecosystem.json").read_text())
segments = data["segments"]


def count_examples(node):
    n = len(node.get("examples", []))
    for c in node.get("children", []):
        n += count_examples(c)
    return n


def anchor(s):
    return s.lower().replace(" ", "-").replace("/", "").replace(".", "")


def render_example(ex):
    if ex.get("url"):
        return f"- [{ex['name']}]({ex['url']})"
    return f"- {ex['name']}"


def render_node(node, depth):
    """Render a segment node. depth=0 is top-level (## ), depth=1 is ### …"""
    lines = []
    heading = "#" * min(depth + 2, 6)
    lines.append(f"{heading} {node['name']}")
    lines.append("")
    for ex in sorted(node.get("examples", []), key=lambda e: e["name"].lower()):
        lines.append(render_example(ex))
    if node.get("examples"):
        lines.append("")
    for child in node.get("children", []):
        lines.extend(render_node(child, depth + 1))
    return lines


total = sum(count_examples(s) for s in segments)

lines = [
    "# Agentic AI Ecosystem Map",
    "",
    "A curated, categorised map of the agentic AI ecosystem — built from real projects outward to taxonomy.",
    "",
    f"**{total} projects** across **{len(segments)} top-level segments**. Source of truth: [`ecosystem.json`](./ecosystem.json).",
    "",
    "## How it works",
    "",
    "The JSON is organised as a tree of segments, each with nested subcategories and example projects. This README is generated from `ecosystem.json` — edit the JSON, then run `python scripts/generate_readme.py`.",
    "",
    "## Segments",
    "",
]
for s in segments:
    lines.append(f"- [{s['name']}](#{anchor(s['name'])}) ({count_examples(s)})")
lines += ["", "---", ""]

for s in segments:
    lines.extend(render_node(s, 0))

(ROOT / "README.md").write_text("\n".join(lines))
print(f"wrote README.md ({total} projects, {len(segments)} segments)")
