#!/usr/bin/env python3
"""Generate README.md from ecosystem.json."""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "ecosystem.json").read_text())
projects = data["projects"]
total = len(projects)

tree = defaultdict(list)
for p in projects:
    top = p["path"][0] if p["path"] else "Uncategorized"
    tree[top].append(p)

def anchor(s):
    return s.lower().replace(" ", "-").replace("/", "")

lines = [
    "# Agentic AI Ecosystem Map",
    "",
    "A curated, categorised map of the agentic AI ecosystem — built from real projects outward to taxonomy.",
    "",
    f"**{total} projects** across **{len(tree)} top-level segments**. Source of truth: [`ecosystem.json`](./ecosystem.json).",
    "",
    "## How it works",
    "",
    "Each project is tagged with a hierarchical `path` (top category → subcategory → …). This README is generated from `ecosystem.json` — edit the JSON, then run `python scripts/generate_readme.py`.",
    "",
    "## Segments",
    "",
]
for top in sorted(tree.keys()):
    lines.append(f"- [{top}](#{anchor(top)}) ({len(tree[top])})")
lines += ["", "---", ""]

for top in sorted(tree.keys()):
    lines += [f"## {top}", ""]
    sub = defaultdict(list)
    for p in tree[top]:
        key = " → ".join(p["path"][1:]) if len(p["path"]) > 1 else ""
        sub[key].append(p)
    for key in sorted(sub.keys()):
        if key:
            lines += [f"### {key}", ""]
        for p in sorted(sub[key], key=lambda x: x["name"].lower()):
            lines.append(f"- [{p['name']}]({p['url']})")
        lines.append("")

(ROOT / "README.md").write_text("\n".join(lines))
print(f"wrote README.md ({total} projects, {len(tree)} segments)")
