#!/usr/bin/env python3
"""Generate an MkDocs Material source tree from graph/nodes.json.

Navigation model:
  - Left sidebar: 11 top-level domains (flat).
  - Within-domain navigation lives in an in-page "sub-nav" block rendered
    at the top of every category page (breadcrumb + siblings + children).
  - Top tabs: "Explore" (domains) and "About" (project meta).

Every Category becomes `mkdocs_src/<slug-path>/index.md`. Examples
(formerly "Projects") are rendered as GitHub-preview cards using
opengraph.githubassets.com for GitHub URLs; non-GitHub links fall back
to a minimal card. All example links open in a new tab.
"""
from __future__ import annotations
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
NODES = ROOT / "graph" / "nodes.json"
EDGES = ROOT / "graph" / "edges.json"
SRC = ROOT / "mkdocs_src"
STATIC_SRC = ROOT / "docs_static"  # preserved raw assets (explore.html, data/, etc.)

# Files currently in docs/ that we want to carry over into the built site.
# These are read from docs_static/ if present, otherwise from the live docs/.
LEGACY_DOCS = ROOT / "docs"
PRESERVE = ["explore.html", "graph.html", "data", "ecosystem.pdf", "ecosystem.typ"]


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "x"


def safe(s: str) -> str:
    return (s or "").strip()


def parse_github(url: str):
    try:
        u = urlparse(url)
    except Exception:
        return None
    if u.netloc.lower() not in {"github.com", "www.github.com"}:
        return None
    parts = [p for p in u.path.strip("/").split("/") if p]
    if len(parts) < 2:
        return None
    return parts[0], parts[1]


def load():
    nodes = json.loads(NODES.read_text())["nodes"]
    edges = json.loads(EDGES.read_text())["edges"]
    cats = {n["id"]: n for n in nodes if n["type"] == "Category"}
    projs = {n["id"]: n for n in nodes if n["type"] == "Project"}
    children_of = defaultdict(list)
    projects_of = defaultdict(list)
    parent_of = {}
    for e in edges:
        if e["type"] == "SUBCATEGORY_OF":
            children_of[e["to"]].append(e["from"])
            parent_of[e["from"]] = e["to"]
        elif e["type"] == "CATEGORY_OF":
            projects_of[e["to"]].append(e["from"])
    return cats, projs, children_of, projects_of, parent_of


def cat_path(cat) -> Path:
    parts = [slug(p) for p in cat["path"]]
    return SRC / Path(*parts) / "index.md"


def rel_to(from_path: list[str], to_path: list[str]) -> str:
    """Relative URL from one category to another (both path arrays)."""
    # Find common prefix
    i = 0
    while i < len(from_path) and i < len(to_path) and slug(from_path[i]) == slug(to_path[i]):
        i += 1
    ups = ["../"] * (len(from_path) - i)
    downs = [slug(p) for p in to_path[i:]]
    if not ups and not downs:
        return "./"
    return "".join(ups) + "/".join(downs) + "/"


def render_subnav(cat, cats, children_of, parent_of) -> str:
    """In-page sub-nav: breadcrumb + siblings + children, above the title."""
    path = cat["path"]
    here = path
    lines: list[str] = []

    # Breadcrumb
    crumb_parts = []
    for i, seg in enumerate(path):
        partial = path[: i + 1]
        if i == len(path) - 1:
            crumb_parts.append(f"**{seg}**")
        else:
            rel = rel_to(here, partial)
            crumb_parts.append(f"[{seg}]({rel})")
    # Home link at front
    home_rel = "../" * len(path)
    crumb = f"[:material-home:]({home_rel}) / " + " / ".join(crumb_parts)

    # Siblings (only if we have a parent)
    parent_id = parent_of.get(cat["id"])
    sibling_md = ""
    if parent_id:
        sib_ids = [c for c in children_of.get(parent_id, []) if c != cat["id"]]
        sibs = sorted((cats[c] for c in sib_ids), key=lambda x: x["label"].lower())
        if sibs:
            items = []
            for s in sibs[:20]:
                rel = rel_to(here, s["path"])
                items.append(f"[{s['label']}]({rel})")
            more = f" · +{len(sibs) - 20} more" if len(sibs) > 20 else ""
            sibling_md = f"**Siblings** · " + " · ".join(items) + more

    # Children
    child_ids = children_of.get(cat["id"], [])
    children_md = ""
    if child_ids:
        kids = sorted((cats[c] for c in child_ids), key=lambda x: x["label"].lower())
        items = []
        for k in kids[:24]:
            rel = rel_to(here, k["path"])
            items.append(f"[{k['label']}]({rel})")
        more = f" · +{len(kids) - 24} more" if len(kids) > 24 else ""
        children_md = f"**Subcategories** · " + " · ".join(items) + more

    lines.append('<div class="subnav" markdown>')
    lines.append("")
    lines.append(crumb)
    lines.append("")
    if sibling_md:
        lines.append(sibling_md)
        lines.append("")
    if children_md:
        lines.append(children_md)
        lines.append("")
    lines.append("</div>")
    lines.append("")
    return "\n".join(lines)


def render_examples(project_ids, projs) -> str:
    if not project_ids:
        return ""
    lines = ["## Examples", ""]
    sorted_projects = sorted(project_ids, key=lambda pid: projs[pid]["label"].lower())
    for pid in sorted_projects:
        p = projs[pid]
        name = p["label"]
        url = p.get("url") or "#"
        gh = parse_github(url) if url else None
        if gh:
            owner, repo = gh
            stars = f"https://img.shields.io/github/stars/{owner}/{repo}?style=flat&logo=github&label=%E2%98%85"
            updated = f"https://img.shields.io/github/last-commit/{owner}/{repo}?style=flat&label=updated"
            lines.append(
                f"- [**{owner}/{repo}**]({url}) "
                f"![stars]({stars}) "
                f"![updated]({updated})"
            )
        else:
            host = ""
            try:
                host = urlparse(url).netloc
            except Exception:
                pass
            suffix = f" — `{host}`" if host else ""
            lines.append(f"- [**{name}**]({url}){suffix}")
    lines.append("")
    return "\n".join(lines)


def render_category(cat, cats, projs, children_of, projects_of, parent_of) -> str:
    label = cat["label"]
    short = safe(cat.get("short_description") or "")
    long_ = safe(cat.get("long_description") or "")
    narrative = safe(cat.get("examples_narrative") or "")

    lines: list[str] = []
    lines.append("---")
    lines.append(f"title: {label}")
    if short:
        lines.append(f"description: {json.dumps(short)[1:-1]}")
    lines.append("---")
    lines.append("")
    # Sub-nav block (only for non-top-level; top-level gets a different landing)
    if len(cat["path"]) > 1:
        lines.append(render_subnav(cat, cats, children_of, parent_of))
    else:
        # Top-level: just a simple home crumb
        lines.append('<div class="subnav" markdown>')
        lines.append("")
        lines.append(f"[:material-home:](../) / **{label}**")
        lines.append("")
        lines.append("</div>")
        lines.append("")

    lines.append(f"# {label}")
    lines.append("")
    if short:
        lines.append(f"**{short}**")
        lines.append("")
    if long_:
        lines.append(long_)
        lines.append("")
    if narrative:
        lines.append(f"> {narrative}")
        lines.append("")

    # Subcategories as material grid cards (only on top-level domain pages;
    # deeper pages already show children in the sub-nav bar).
    child_ids = children_of.get(cat["id"], [])
    if child_ids and len(cat["path"]) == 1:
        lines.append("## Subcategories")
        lines.append("")
        lines.append('<div class="grid cards" markdown>')
        lines.append("")
        kids = sorted((cats[c] for c in child_ids), key=lambda x: x["label"].lower())
        for k in kids:
            s = slug(k["label"])
            child_short = safe(k.get("short_description") or "")
            sub_n = len(children_of.get(k["id"], []))
            proj_n = len(projects_of.get(k["id"], []))
            meta_parts = []
            if sub_n:
                meta_parts.append(f"{sub_n} sub")
            if proj_n:
                meta_parts.append(f"{proj_n} examples")
            meta = " · ".join(meta_parts)
            lines.append(f"-   __[{k['label']}]({s}/index.md)__")
            lines.append("")
            if child_short:
                lines.append(f"    {child_short}")
                lines.append("")
            if meta:
                lines.append(f"    _{meta}_")
                lines.append("")
        lines.append("</div>")
        lines.append("")

    # Examples
    proj_ids = projects_of.get(cat["id"], [])
    if proj_ids:
        lines.append(render_examples(proj_ids, projs))

    return "\n".join(lines)


def render_landing(cats, children_of, projects_of) -> str:
    top_ids = sorted(
        [cid for cid, c in cats.items() if len(c["path"]) == 1],
        key=lambda cid: cats[cid]["label"].lower(),
    )
    total_cats = len(cats)
    total_projs = sum(len(v) for v in projects_of.values())
    lines = [
        "---",
        "title: Home",
        "hide:",
        "  - navigation",
        "  - toc",
        "---",
        "",
        "# Agentic AI Ecosystem",
        "",
        f"A hand-curated taxonomy of the agentic AI tooling landscape — **{len(top_ids)} domains**, "
        f"**{total_cats} categories**, **{total_projs} example projects**. Categories are functional slots; "
        "example projects are evidence that a slot exists.",
        "",
        "Pick a domain below or use the search bar.",
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
    return "\n".join(lines)


def write_about_pages(total_cats, total_projs, top_count):
    about = SRC / "about"
    about.mkdir(parents=True, exist_ok=True)
    (about / "index.md").write_text(f"""---
title: About
---

# About this project

The **Agentic AI Ecosystem** is a hand-curated taxonomy of the agentic AI tooling
landscape. The goal is *not* an exhaustive project directory — it's a
**classification map**. Example projects are collected as *evidence* that a
category exists, and then used in reverse to derive and refine the taxonomy itself.

Think of it as: *"What are the real functional categories in agentic AI tooling
right now?"* — with a handful of representative projects pinned under each as proof.

Currently the map holds **{top_count} top-level domains**, **{total_cats} categories**,
and **{total_projs} example projects**.

## Working principles

1. **Granularity over consolidation.** Deep, specific subcategories are preferred
   over broad buckets. A category with one example (or even zero) is fine if it
   represents a distinct functional slot.
2. **Categories first, examples second.** When adding a project, the question is
   *"what classification does this reveal or confirm?"* — not *"where can I dump this?"*
3. **Every category has a description** explaining what belongs in that slot and
   how it differs from its siblings.
4. **Narrow top, deep middle.** The first level of the hierarchy is narrow
   (~11 domains). Value accrues at depth: precise distinctions belong in level
   2/3/4 subcategories.
5. **Project entries are minimal**: `{{ name, url }}`. The taxonomy carries the meaning.

## Contributing

The source of truth is `graph/nodes.json` + `graph/edges.json` in the
[GitHub repository](https://github.com/danielrosehill/Agentic-AI-Ecosystem).
To suggest a new category or project, open an issue or pull request.
""")

    (about / "schema.md").write_text("""---
title: Schema
---

# Data schema

The source of truth is a directed graph with two node types and two edge types.

## Nodes (`graph/nodes.json`)

```json
{
  "updated": "YYYY-MM-DD",
  "nodes": [
    {
      "id": "cat:agents/autonomous/trading",
      "type": "Category",
      "label": "Trading",
      "path": ["Agents", "Autonomous", "Trading"],
      "short_description": "…",
      "long_description": "…"
    },
    {
      "id": "proj:ai-trader",
      "type": "Project",
      "label": "AI-Trader",
      "url": "https://github.com/owner/repo"
    }
  ]
}
```

## Edges (`graph/edges.json`)

```json
{
  "edges": [
    { "from": "cat:agents/autonomous/trading", "to": "cat:agents/autonomous", "type": "SUBCATEGORY_OF" },
    { "from": "proj:ai-trader",                "to": "cat:agents/autonomous/trading", "type": "CATEGORY_OF" }
  ]
}
```

## ID rules

- Categories: `cat:<slug-path>`
- Projects: `proj:<slug-name>`
- Slugs: lowercase, non-alphanumerics replaced with `-`

## Derived artefacts

- `ecosystem.json` — a derived tree view regenerated by `scripts/build_tree.py`
- `README.md` — regenerated by `scripts/generate_readme.py`
- This site — built by `scripts/build_mkdocs.py` + `mkdocs build`
""")


def main():
    if SRC.exists():
        shutil.rmtree(SRC)
    SRC.mkdir()

    cats, projs, children_of, projects_of, parent_of = load()

    for cat in cats.values():
        p = cat_path(cat)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(render_category(cat, cats, projs, children_of, projects_of, parent_of))

    (SRC / "index.md").write_text(render_landing(cats, children_of, projects_of))

    top_count = sum(1 for c in cats.values() if len(c["path"]) == 1)
    total_cats = len(cats)
    total_projs = sum(len(v) for v in projects_of.values())
    write_about_pages(total_cats, total_projs, top_count)

    # Custom CSS
    css_dir = SRC / "assets" / "stylesheets"
    css_dir.mkdir(parents=True, exist_ok=True)
    (css_dir / "extra.css").write_text("""
/* In-page sub-nav block shown above every category title */
.subnav {
  font-size: 0.8rem;
  padding: 0.6rem 0.9rem;
  margin: 0 0 1.2rem 0;
  background: var(--md-code-bg-color);
  border-left: 3px solid var(--md-accent-fg-color);
  border-radius: 4px;
  line-height: 1.6;
}
.subnav p { margin: 0.2rem 0; }
.subnav a { text-decoration: none; }
.subnav a:hover { text-decoration: underline; }

/* Example cards: GitHub OpenGraph previews in a responsive grid */
.gh-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 12px;
  margin: 14px 0 24px;
}
@media (min-width: 1200px) {
  .gh-grid { grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }
}
.gh-card {
  position: relative;
  display: block;
  text-decoration: none !important;
  color: inherit !important;
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 8px;
  overflow: hidden;
  background: var(--md-code-bg-color);
  aspect-ratio: 2 / 1;
  transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
}
.gh-card::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 8px;
  pointer-events: none;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04);
}
.gh-card:hover {
  transform: translateY(-3px);
  border-color: var(--md-accent-fg-color);
  box-shadow: 0 8px 24px rgba(0,0,0,0.22), 0 2px 6px rgba(0,0,0,0.14);
}
.gh-card img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  background: #0d1117;
}
/* Subtle top accent on hover */
.gh-card::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--md-accent-fg-color), var(--md-primary-fg-color));
  opacity: 0;
  transition: opacity 0.18s ease;
  z-index: 2;
}
.gh-card:hover::before { opacity: 1; }

.gh-card--plain {
  aspect-ratio: auto;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 18px 16px;
  min-height: 120px;
  justify-content: center;
  align-items: flex-start;
}
.gh-card--plain .gh-icon { font-size: 1.6rem; color: var(--md-accent-fg-color); }
.gh-card--plain .gh-name { font-weight: 600; font-size: 0.9rem; }
.gh-card--plain .gh-host { font-size: 0.75rem; color: var(--md-default-fg-color--light); opacity: 0.8; }
""")

    # Preserve existing static assets
    src_root = STATIC_SRC if STATIC_SRC.exists() else LEGACY_DOCS
    for name in PRESERVE:
        src = src_root / name
        if not src.exists():
            continue
        dst = SRC / name
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    print(f"wrote {len(cats)} category pages + landing + about → {SRC}")


if __name__ == "__main__":
    main()
