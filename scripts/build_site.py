#!/usr/bin/env python3
"""Generate a static microsite from ecosystem.json.

Layout:
  docs/index.html                        — landing: all segments
  docs/c/<segment-slug>/index.html       — segment page
  docs/c/<seg>/<subcat-slug>/index.html  — subcategory page (recurses)
  docs/assets/site.css                   — shared stylesheet

Each category page shows: breadcrumb, short/long description, inline SVG
hub-and-spoke visualisation of its children, subcategory cards, project list.
"""
import json
import math
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ECO = ROOT / "ecosystem.json"
DOCS = ROOT / "docs"
SITE_ROOT = DOCS
CAT_ROOT = DOCS / "c"
ASSETS = DOCS / "assets"

CSS = """
:root {
  --bg:#f7f8fa; --panel:#ffffff; --border:#e3e6eb; --text:#1a1f2c;
  --muted:#6b7280; --accent:#2563eb; --accent-soft:#e0ecff;
  --hub:#1f6feb; --spoke:#6aa9ff; --project:#f59e0b; --line:#c8cfdb;
}
* { box-sizing: border-box; }
html, body { margin:0; padding:0; background:var(--bg); color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  line-height:1.55; }
a { color:var(--accent); text-decoration:none; }
a:hover { text-decoration:underline; }

header.site { background:#fff; border-bottom:1px solid var(--border);
  padding:16px 28px; display:flex; justify-content:space-between; align-items:center; }
header.site .brand { font-weight:700; font-size:16px; color:var(--text); }
header.site .brand a { color:var(--text); }
header.site nav a { margin-left:18px; font-size:13px; color:var(--muted); }
header.site nav a:hover { color:var(--accent); }

main { max-width:1100px; margin:0 auto; padding:32px 28px 64px; }

.breadcrumb { font-size:13px; color:var(--muted); margin-bottom:14px; }
.breadcrumb a { color:var(--muted); }
.breadcrumb a:hover { color:var(--accent); }
.breadcrumb .sep { margin:0 6px; }
.breadcrumb .current { color:var(--text); font-weight:600; }

h1.page-title { font-size:32px; margin:0 0 6px; font-weight:700; }
h1.page-title.small { font-size:26px; }
.subtitle { color:var(--muted); font-size:14px; margin-bottom:22px; }
.short { font-size:17px; color:var(--text); font-style:italic;
  border-left:3px solid var(--accent); padding:4px 0 4px 14px; margin:18px 0 14px; }
.long { font-size:14.5px; color:#2d3748; margin-bottom:24px; max-width:760px; }

h2.section { font-size:13px; text-transform:uppercase; letter-spacing:0.8px;
  color:var(--muted); margin:34px 0 14px; font-weight:600; }

.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr));
  gap:14px; }
.card { background:var(--panel); border:1px solid var(--border); border-radius:10px;
  padding:16px 18px; transition:all 0.15s; display:block; }
.card:hover { border-color:var(--accent); box-shadow:0 4px 14px rgba(37,99,235,0.08);
  transform:translateY(-1px); text-decoration:none; }
.card .name { font-weight:600; font-size:15px; color:var(--text); }
.card .count { font-size:11px; color:var(--muted); background:#f0f2f5;
  padding:2px 9px; border-radius:10px; float:right; }
.card .blurb { font-size:12.5px; color:var(--muted); margin-top:6px; line-height:1.45; }

ul.projects { list-style:none; padding:0; margin:0;
  display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:8px; }
ul.projects li { background:var(--panel); border:1px solid var(--border);
  border-radius:8px; padding:10px 14px; font-size:13.5px; }
ul.projects li a { color:var(--text); font-weight:500; }
ul.projects li a:hover { color:var(--accent); }
ul.projects li .ext { font-size:11px; color:var(--muted); display:block; margin-top:2px;
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }

.viz { background:#fff; border:1px solid var(--border); border-radius:10px;
  padding:18px; margin:14px 0 28px; }
.viz svg { display:block; width:100%; height:auto; }
.viz .legend { font-size:11px; color:var(--muted); margin-top:8px; }
.viz-hub { fill:var(--hub); stroke:#fff; stroke-width:3; }
.viz-hub-text { fill:#fff; font-weight:700; font-size:13px;
  text-anchor:middle; dominant-baseline:middle; }
.viz-spoke { fill:var(--spoke); stroke:#fff; stroke-width:2; }
.viz-project { fill:var(--project); stroke:#fff; stroke-width:2; }
.viz-edge { stroke:var(--line); stroke-width:1.5; fill:none; }
.viz-label { font-size:11px; fill:var(--text); font-weight:600; }

footer.site { text-align:center; padding:28px; color:var(--muted); font-size:12px;
  border-top:1px solid var(--border); background:#fff; margin-top:40px; }
"""


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "x"


def get_label(cat: dict) -> str:
    return cat.get("name") or cat.get("label") or ""


def count_descendants(cat: dict) -> int:
    n = len(cat.get("examples", []) or [])
    for c in cat.get("children", []) or []:
        n += count_descendants(c)
    return n


def rel_root(depth: int) -> str:
    # depth=0 for landing (docs/), 1 for docs/c/seg/, 2 for docs/c/seg/sub/
    return "../" * depth if depth else ""


def header_html(depth: int) -> str:
    r = rel_root(depth)
    return f"""<header class="site">
<div class="brand"><a href="{r}index.html">Agentic AI Ecosystem</a></div>
<nav>
  <a href="{r}index.html">Home</a>
  <a href="{r}explore.html">Explore</a>
  <a href="{r}graph.html">Graph</a>
  <a href="https://github.com/danielrosehill/Agentic-AI-Ecosystem">GitHub</a>
</nav>
</header>"""


def footer_html() -> str:
    return (
        '<footer class="site">A hand-curated taxonomy of the agentic AI ecosystem · '
        '<a href="https://github.com/danielrosehill/Agentic-AI-Ecosystem">source on GitHub</a>'
        "</footer>"
    )


def page_shell(title: str, depth: int, body: str) -> str:
    r = rel_root(depth)
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<title>{escape(title)} · Agentic AI Ecosystem</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="{r}assets/site.css">
</head><body>
{header_html(depth)}
<main>
{body}
</main>
{footer_html()}
</body></html>
"""


def breadcrumb_html(crumbs: list) -> str:
    # crumbs = [(label, href_or_None), ...]
    parts = []
    for i, (label, href) in enumerate(crumbs):
        if i > 0:
            parts.append('<span class="sep">›</span>')
        if href and i < len(crumbs) - 1:
            parts.append(f'<a href="{href}">{escape(label)}</a>')
        else:
            parts.append(f'<span class="current">{escape(label)}</span>')
    return '<div class="breadcrumb">' + "".join(parts) + "</div>"


def viz_html(center_label: str, children: list, project_children: list) -> str:
    """Static SVG hub-and-spoke visualisation."""
    items = []
    for c in children:
        items.append((get_label(c), "spoke"))
    for p in project_children:
        items.append((p.get("name", ""), "project"))
    n = len(items)
    if n == 0:
        return ""

    W, H = 900, 560
    cx, cy = W / 2, H / 2
    radius = min(250, max(150, 18 * n + 60))
    # scale H if radius too big
    need_h = int(radius * 2 + 160)
    if need_h > H:
        H = need_h
        cy = H / 2

    parts = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img">']

    for i in range(n):
        ang = (i / n) * 2 * math.pi - math.pi / 2
        x = cx + math.cos(ang) * radius
        y = cy + math.sin(ang) * radius
        parts.append(f'<line class="viz-edge" x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}"/>')

    # hub
    parts.append(f'<circle class="viz-hub" cx="{cx}" cy="{cy}" r="52"/>')
    # wrap hub label
    words = center_label.split()
    lines, line = [], ""
    for w in words:
        if len((line + " " + w).strip()) > 13 and line:
            lines.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        lines.append(line)
    lh = 15
    start_y = cy - (len(lines) - 1) * lh / 2
    parts.append(f'<text class="viz-hub-text" x="{cx}" y="{cy}">')
    for i, ln in enumerate(lines):
        parts.append(f'<tspan x="{cx}" y="{start_y + i * lh:.1f}">{escape(ln)}</tspan>')
    parts.append("</text>")

    for i, (label, kind) in enumerate(items):
        ang = (i / n) * 2 * math.pi - math.pi / 2
        x = cx + math.cos(ang) * radius
        y = cy + math.sin(ang) * radius
        r = 14 if kind == "project" else 22
        cls = "viz-project" if kind == "project" else "viz-spoke"
        parts.append(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>')

        lx = cx + math.cos(ang) * (radius + r + 10)
        ly = cy + math.sin(ang) * (radius + r + 10)
        cos = math.cos(ang)
        anchor = "start" if cos > 0.3 else ("end" if cos < -0.3 else "middle")
        tl = label if len(label) <= 28 else label[:27] + "…"
        parts.append(
            f'<text class="viz-label" x="{lx:.1f}" y="{ly:.1f}" '
            f'text-anchor="{anchor}" dominant-baseline="middle">{escape(tl)}</text>'
        )
    parts.append("</svg>")
    legend = (
        '<div class="legend">'
        '● Hub (current)   ● Subcategory   ● Project'
        "</div>"
    )
    return '<div class="viz">' + "".join(parts) + legend + "</div>"


def card_html(label: str, href: str, count: int, blurb: str) -> str:
    blurb_html = f'<div class="blurb">{escape(blurb)}</div>' if blurb else ""
    return (
        f'<a class="card" href="{href}">'
        f'<span class="count">{count}</span>'
        f'<div class="name">{escape(label)}</div>'
        f"{blurb_html}"
        "</a>"
    )


def projects_html(projects: list) -> str:
    if not projects:
        return ""
    parts = ['<ul class="projects">']
    for p in projects:
        name = escape(p.get("name", ""))
        url = escape(p.get("url", "#"))
        host = re.sub(r"^https?://", "", url).split("/")[0]
        parts.append(
            f'<li><a href="{url}" target="_blank" rel="noopener">{name}</a>'
            f'<span class="ext">{escape(host)}</span></li>'
        )
    parts.append("</ul>")
    return "".join(parts)


def write_category_page(cat: dict, out_dir: Path, depth: int, crumbs: list, path_labels: list):
    out_dir.mkdir(parents=True, exist_ok=True)
    label = get_label(cat)
    short = cat.get("short_description", "") or ""
    long_ = cat.get("long_description", "") or ""
    children = cat.get("children", []) or []
    projects = cat.get("examples", []) or []

    body_parts = [breadcrumb_html(crumbs)]
    body_parts.append(f'<h1 class="page-title small">{escape(label)}</h1>')
    if len(path_labels) > 1:
        path_str = " › ".join(path_labels)
        body_parts.append(f'<div class="subtitle">{escape(path_str)}</div>')

    if short:
        body_parts.append(f'<div class="short">{escape(short)}</div>')
    if long_:
        body_parts.append(f'<div class="long">{escape(long_)}</div>')
    if not short and not long_:
        body_parts.append(
            '<div class="long" style="color:var(--muted);font-style:italic">'
            "No description yet.</div>"
        )

    if children or projects:
        body_parts.append('<h2 class="section">Map</h2>')
        body_parts.append(viz_html(label, children, projects))

    if children:
        body_parts.append(f'<h2 class="section">Subcategories ({len(children)})</h2>')
        body_parts.append('<div class="grid">')
        for c in children:
            slug = slugify(get_label(c))
            body_parts.append(
                card_html(
                    get_label(c),
                    f"{slug}/index.html",
                    count_descendants(c),
                    c.get("short_description", "") or "",
                )
            )
        body_parts.append("</div>")

    if projects:
        body_parts.append(f'<h2 class="section">Projects ({len(projects)})</h2>')
        body_parts.append(projects_html(projects))

    html = page_shell(label, depth, "\n".join(body_parts))
    (out_dir / "index.html").write_text(html)

    for c in children:
        slug = slugify(get_label(c))
        # Rebuild crumbs relative to the child dir.
        # crumbs currently ends with (label, None) for this page; make it clickable.
        fixed = []
        n_levels = len(crumbs)  # child is n_levels deep below Home
        for i, (lbl, _) in enumerate(crumbs):
            up = "../" * (n_levels - i)
            fixed.append((lbl, f"{up}index.html"))
        fixed.append((get_label(c), None))
        write_category_page(
            c, out_dir / slug, depth + 1, fixed, path_labels + [get_label(c)]
        )


def write_landing(tree: dict):
    segments = tree.get("segments", [])
    body = [
        breadcrumb_html([("Home", None)]),
        '<h1 class="page-title">Agentic AI Ecosystem</h1>',
        f'<div class="subtitle">{len(segments)} top-level segments · updated '
        f'{escape(tree.get("updated", ""))}</div>',
        '<div class="long">A hand-curated taxonomy of the agentic AI tooling landscape. '
        "Browse by segment below, explore interactively, or view the full graph.</div>",
        '<h2 class="section">Segments</h2>',
        '<div class="grid">',
    ]
    for seg in segments:
        slug = slugify(get_label(seg))
        body.append(
            card_html(
                get_label(seg),
                f"c/{slug}/index.html",
                count_descendants(seg),
                seg.get("short_description", "") or "",
            )
        )
    body.append("</div>")
    html = page_shell("Home", 0, "\n".join(body))
    (SITE_ROOT / "index.html").write_text(html)


def main():
    tree = json.loads(ECO.read_text())
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "site.css").write_text(CSS)

    # Clean category tree before regenerating
    if CAT_ROOT.exists():
        shutil.rmtree(CAT_ROOT)
    CAT_ROOT.mkdir(parents=True, exist_ok=True)

    write_landing(tree)

    segments = tree.get("segments", [])
    for seg in segments:
        slug = slugify(get_label(seg))
        out = CAT_ROOT / slug
        crumbs = [
            ("Home", "../../index.html"),
            (get_label(seg), None),
        ]
        write_category_page(
            seg, out, depth=2, crumbs=crumbs, path_labels=[get_label(seg)]
        )

    n_pages = sum(1 for _ in CAT_ROOT.rglob("index.html")) + 1
    print(f"wrote {n_pages} pages under docs/")


if __name__ == "__main__":
    main()
