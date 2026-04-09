#!/usr/bin/env python3
"""Generate an MkDocs Material source tree from graph/nodes.json.

Every Category becomes a markdown file at `mkdocs_src/<path>/index.md`
(so MkDocs' nested sidebar tree mirrors the taxonomy exactly). Each file
contains the category's short + long description, a list of subcategories
with their shorts, and a list of example projects with links.

The root `mkdocs_src/index.md` is a landing page with stats and the 11
top-level domains as cards.

Static assets under docs/ that we want to preserve (explore.html,
graph.html, data/, assets/) are copied into mkdocs_src/ so they end up in
the final build output.
"""
from __future__ import annotations
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODES = ROOT / "graph" / "nodes.json"
EDGES = ROOT / "graph" / "edges.json"
SRC = ROOT / "mkdocs_src"
DOCS = ROOT / "docs"  # current static files to preserve

PRESERVE = ["explore.html", "graph.html", "data", "assets", "ecosystem.pdf", "ecosystem.typ"]


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "x"


def safe(s: str) -> str:
    return (s or "").replace("|", "\\|").strip()


def load():
    nodes = json.loads(NODES.read_text())["nodes"]
    edges = json.loads(EDGES.read_text())["edges"]
    cats = {n["id"]: n for n in nodes if n["type"] == "Category"}
    projs = {n["id"]: n for n in nodes if n["type"] == "Project"}
    children_of = defaultdict(list)
    projects_of = defaultdict(list)
    for e in edges:
        if e["type"] == "SUBCATEGORY_OF":
            children_of[e["to"]].append(e["from"])
        elif e["type"] == "CATEGORY_OF":
            projects_of[e["to"]].append(e["from"])
    return cats, projs, children_of, projects_of


def cat_path(cat) -> Path:
    parts = [slug(p) for p in cat["path"]]
    return SRC / Path(*parts) / "index.md"


def render_category(cat, cats, projs, children_of, projects_of) -> str:
    label = cat["label"]
    short = cat.get("short_description") or ""
    long_ = cat.get("long_description") or ""
    narrative = cat.get("examples_narrative") or ""

    # breadcrumb — MkDocs handles nav, but a visible path helps context
    crumb = " / ".join(cat["path"])

    lines: list[str] = []
    lines.append(f"# {label}")
    lines.append("")
    lines.append(f'!!! abstract ""')
    lines.append(f"    {crumb}")
    lines.append("")
    if short:
        lines.append(f"**{safe(short)}**")
        lines.append("")
    if long_:
        lines.append(safe(long_))
        lines.append("")
    if narrative:
        lines.append(f"> {safe(narrative)}")
        lines.append("")

    # Subcategories
    child_ids = sorted(
        children_of.get(cat["id"], []),
        key=lambda cid: cats[cid]["label"].lower(),
    )
    if child_ids:
        lines.append("## Subcategories")
        lines.append("")
        for cid in child_ids:
            child = cats[cid]
            child_slug = slug(child["label"])
            child_short = safe(child.get("short_description") or "")
            child_proj_count = len(projects_of.get(cid, []))
            child_sub_count = len(children_of.get(cid, []))
            meta_parts = []
            if child_sub_count:
                meta_parts.append(f"{child_sub_count} sub")
            if child_proj_count:
                meta_parts.append(f"{child_proj_count} proj")
            meta = f" *({', '.join(meta_parts)})*" if meta_parts else ""
            if child_short:
                lines.append(f"- [**{child['label']}**]({child_slug}/index.md){meta} — {child_short}")
            else:
                lines.append(f"- [**{child['label']}**]({child_slug}/index.md){meta}")
        lines.append("")

    # Projects
    proj_ids = sorted(
        projects_of.get(cat["id"], []),
        key=lambda pid: projs[pid]["label"].lower(),
    )
    if proj_ids:
        lines.append("## Projects")
        lines.append("")
        for pid in proj_ids:
            p = projs[pid]
            url = p.get("url") or "#"
            lines.append(f"- [**{p['label']}**]({url})")
        lines.append("")

    return "\n".join(lines)


def render_landing(cats, children_of, projects_of) -> str:
    top_ids = sorted(
        [cid for cid, c in cats.items() if len(c["path"]) == 1],
        key=lambda cid: cats[cid]["label"].lower(),
    )
    total_cats = len(cats)
    total_projs = sum(len(v) for v in projects_of.values())
    lines = [
        "# Agentic AI Ecosystem",
        "",
        f"A hand-curated taxonomy of the agentic AI tooling landscape — **{len(top_ids)} domains**, "
        f"**{total_cats} categories**, **{total_projs} projects**. Categories are functional slots; "
        "projects are evidence that a slot exists.",
        "",
        "Browse via the sidebar on the left, use the search bar, or click a domain below.",
        "",
        "## Domains",
        "",
        '<div class="grid cards" markdown>',
        "",
    ]
    for cid in top_ids:
        c = cats[cid]
        s = slug(c["label"])
        short = safe(c.get("short_description") or "")
        sub_n = len(children_of.get(cid, []))
        lines.append(f"-   __[{c['label']}]({s}/index.md)__")
        lines.append("")
        lines.append(f"    ---")
        lines.append("")
        if short:
            lines.append(f"    {short}")
            lines.append("")
        lines.append(f"    _{sub_n} subcategories_")
        lines.append("")
    lines.append("</div>")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "Alternate views: [Hub-Spoke](explore.html) · "
        "[Graph](graph.html) · [JSON](data/ecosystem.json) · "
        "[GitHub](https://github.com/danielrosehill/Agentic-AI-Ecosystem)"
    )
    return "\n".join(lines)


def main():
    if SRC.exists():
        shutil.rmtree(SRC)
    SRC.mkdir()

    cats, projs, children_of, projects_of = load()

    for cat in cats.values():
        p = cat_path(cat)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(render_category(cat, cats, projs, children_of, projects_of))

    (SRC / "index.md").write_text(render_landing(cats, children_of, projects_of))

    # Copy preserved static assets so they end up in the built site
    for name in PRESERVE:
        src = DOCS / name
        if not src.exists():
            continue
        dst = SRC / name
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    print(f"wrote {len(cats)} category pages + landing → {SRC}")


if __name__ == "__main__":
    main()
