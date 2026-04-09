#!/usr/bin/env python3
"""Build landscape2 inputs from graph/nodes.json + edges.json.

landscape2 is strictly 2-level (category → subcategory → items). Our taxonomy
goes up to 4-5 levels deep, so we flatten:
  - category    = top-level segment (11 domains)
  - subcategory = " / ".join(path[1:])  (so depth-2 becomes the subcategory
    label, depth-3+ is shown as e.g. "Autonomous / Trading")

Every project becomes an item. Logos are auto-generated as SVG initials tiles
(landscape2 requires an SVG logo file per item).

Outputs:
  landscape2/landscape.yml
  landscape2/settings.yml
  landscape2/logos/<slug>.svg
"""
from __future__ import annotations
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    raise SystemExit("install pyyaml: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
NODES = ROOT / "graph" / "nodes.json"
EDGES = ROOT / "graph" / "edges.json"
OUT_DIR = ROOT / "landscape2"
LOGOS_DIR = OUT_DIR / "logos"


PALETTE = [
    ("#7cc4ff", "#0b2840"),
    ("#ffb86b", "#3a2410"),
    ("#a2e4b8", "#0f2a1a"),
    ("#f49ac1", "#3a1020"),
    ("#c9a7ff", "#22124a"),
    ("#ffec99", "#3a3410"),
    ("#96d9d1", "#0e2a2a"),
    ("#ff9e7a", "#3a1a10"),
    ("#b4e27a", "#1a2a10"),
    ("#9ac5ff", "#10213a"),
    ("#ffb4e0", "#3a1026"),
]


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "x"


def initials(name: str) -> str:
    words = [w for w in re.split(r"[\s\-_/]+", name) if w]
    if not words:
        return "?"
    if len(words) == 1:
        w = words[0]
        return (w[:2] if len(w) > 1 else w).upper()
    return (words[0][0] + words[-1][0]).upper()


def logo_svg(name: str) -> str:
    text = initials(name)
    h = int(hashlib.md5(name.encode()).hexdigest(), 16)
    bg, fg = PALETTE[h % len(PALETTE)]
    font_size = 44 if len(text) <= 2 else 36
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="14" fill="{bg}"/>
  <text x="50" y="50" font-family="Inter, -apple-system, sans-serif"
        font-weight="700" font-size="{font_size}"
        text-anchor="middle" dominant-baseline="central" fill="{fg}">{text}</text>
</svg>
'''


def load_graph():
    nodes = json.loads(NODES.read_text())["nodes"]
    edges = json.loads(EDGES.read_text())["edges"]
    cats = {n["id"]: n for n in nodes if n["type"] == "Category"}
    projs = {n["id"]: n for n in nodes if n["type"] == "Project"}
    cat_of = defaultdict(list)  # cat_id -> [project node]
    for e in edges:
        if e["type"] == "CATEGORY_OF" and e["from"] in projs and e["to"] in cats:
            cat_of[e["to"]].append(projs[e["from"]])
    return cats, projs, cat_of


def main():
    cats, projs, cat_of = load_graph()
    OUT_DIR.mkdir(exist_ok=True)
    LOGOS_DIR.mkdir(exist_ok=True)

    # Flatten: (top_segment, subcat_label) -> list of project nodes
    by_slot: dict[tuple[str, str], list] = defaultdict(list)
    # Also track descriptions for subcat-slot ordering
    slot_descriptions: dict[tuple[str, str], str] = {}

    for cat in cats.values():
        path = cat["path"]
        if len(path) < 2:
            continue  # top-level itself has no items directly in landscape2 model
        top = path[0]
        sub_label = " / ".join(path[1:])
        slot = (top, sub_label)
        if slot not in slot_descriptions:
            desc = cat.get("short_description") or ""
            slot_descriptions[slot] = desc
        for p in cat_of.get(cat["id"], []):
            by_slot[slot].append(p)

    # Also: top-level cats sometimes have direct projects (unusual). Put them
    # in a synthetic subcategory "General".
    for cat in cats.values():
        if len(cat["path"]) == 1:
            projs_here = cat_of.get(cat["id"], [])
            if projs_here:
                slot = (cat["path"][0], "General")
                slot_descriptions.setdefault(slot, cat.get("short_description") or "")
                by_slot[slot].extend(projs_here)

    # Build categories list
    top_segments = sorted({k[0] for k in by_slot.keys()})
    categories_out = []
    item_count = 0
    used_logos: set[str] = set()

    for top in top_segments:
        subs = sorted({k[1] for k in by_slot.keys() if k[0] == top})
        sub_entries = []
        for sub in subs:
            items = []
            for p in by_slot[(top, sub)]:
                name = p["label"]
                url = p.get("url") or ""
                if not url:
                    continue
                logo_name = f"{slug(name)}.svg"
                if logo_name not in used_logos:
                    (LOGOS_DIR / logo_name).write_text(logo_svg(name))
                    used_logos.add(logo_name)
                items.append({
                    "name": name,
                    "homepage_url": url,
                    "logo": logo_name,
                    "description": slot_descriptions.get((top, sub), "") or f"Listed under {top} / {sub}.",
                    "repo_url": url if "github.com" in url else None,
                })
                item_count += 1
            # landscape2 requires at least one item per subcat
            if items:
                for it in items:
                    if it["repo_url"] is None:
                        del it["repo_url"]
                sub_entries.append({"name": sub, "items": items})
        if sub_entries:
            categories_out.append({"name": top, "subcategories": sub_entries})

    data = {"categories": categories_out}
    (OUT_DIR / "landscape.yml").write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000)
    )

    settings = {
        "foundation": "Agentic AI Ecosystem",
        "url": "https://danielrosehill.github.io/Agentic-AI-Ecosystem/landscape/",
        "base_path": "/Agentic-AI-Ecosystem/landscape",
        "colors": {
            "color1": "rgba(124, 196, 255, 1)",
            "color2": "rgba(255, 184, 107, 1)",
            "color3": "rgba(154, 209, 255, 1)",
            "color4": "rgba(124, 196, 255, 1)",
            "color5": "rgba(23, 28, 36, 1)",
            "color6": "rgba(18, 22, 28, 1)",
            "color7": "rgba(34, 42, 53, 1)",
        },
        "images": {},
        "social_networks": {},
    }
    (OUT_DIR / "settings.yml").write_text(
        yaml.safe_dump(settings, sort_keys=False, allow_unicode=True)
    )

    print(f"categories: {len(categories_out)}")
    print(f"subcategories: {sum(len(c['subcategories']) for c in categories_out)}")
    print(f"items: {item_count}")
    print(f"logos: {len(used_logos)}")
    print(f"wrote {OUT_DIR}/landscape.yml, settings.yml, logos/")


if __name__ == "__main__":
    main()
