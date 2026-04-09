#!/usr/bin/env python3
"""Generate SCHEMA.md — the full taxonomy tree — from ecosystem.json."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "ecosystem.json").read_text())
segments = data["segments"]


def slug(s: str) -> str:
    s = s.lower().strip()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "unnamed"


def cat_id(path):
    return "cat:" + "/".join(slug(p) for p in path)


def render_example(ex):
    if ex.get("url"):
        return f"  - [{ex['name']}]({ex['url']})"
    return f"  - {ex['name']}"


def render(node, path, depth):
    out = []
    heading = "#" * min(depth + 2, 6)
    full = path + [node["name"]]
    out.append(f"{heading} {node['name']}")
    out.append(f"<sub>`{cat_id(full)}`</sub>")
    out.append("")
    short = (node.get("short_description") or node.get("description") or "").strip()
    long_ = (node.get("long_description") or "").strip()
    if short:
        out.append(f"*{short}*")
        out.append("")
    if long_:
        out.append(long_)
        out.append("")
    for ex in sorted(node.get("examples", []) or [], key=lambda e: e["name"].lower()):
        out.append(render_example(ex))
    if node.get("examples"):
        out.append("")
    for child in node.get("children", []) or []:
        out.extend(render(child, full, depth + 1))
    return out


lines = [
    "# Schema — Full Taxonomy Tree",
    "",
    f"*Generated from `ecosystem.json` (updated: {data.get('updated', '?')}). Do not hand-edit — run `python3 scripts/generate_schema.py`.*",
    "",
    "The compact overview lives in [README.md](./README.md). This file is the exhaustive tree: every cluster, sub-area, description, and project, with stable category IDs.",
    "",
    "---",
    "",
]

for s in sorted(segments, key=lambda x: x["name"].lower()):
    lines.extend(render(s, [], 0))

(ROOT / "SCHEMA.md").write_text("\n".join(lines))
print(f"wrote SCHEMA.md ({len(segments)} segments)")
