#!/usr/bin/env python3
"""Generate a Typst PDF of the ecosystem taxonomy with descriptions + projects."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ECO = ROOT / "ecosystem.json"
OUT_TYP = ROOT / "docs" / "ecosystem.typ"
OUT_PDF = ROOT / "docs" / "ecosystem.pdf"


def esc(s: str) -> str:
    if not s:
        return ""
    return (
        s.replace("\\", "\\\\")
        .replace("#", "\\#")
        .replace("*", "\\*")
        .replace("_", "\\_")
        .replace("$", "\\$")
        .replace("<", "\\<")
        .replace(">", "\\>")
        .replace("@", "\\@")
        .replace('"', '\\"')
    )


def render_category(cat: dict, depth: int, lines: list):
    label = esc(cat.get("label", ""))
    short = esc(cat.get("short_description", "") or "")
    long_ = esc(cat.get("long_description", "") or "")
    indent = "  " * depth

    # Heading styled by depth
    if depth == 0:
        lines.append(f'#block(above: 1.2em, below: 0.4em)[#text(size: 14pt, weight: "bold", fill: rgb("#1a365d"))[{label}]]')
    elif depth == 1:
        lines.append(f'#block(above: 0.8em, below: 0.3em, inset: (left: {depth*12}pt))[#text(size: 12pt, weight: "bold", fill: rgb("#2b6cb0"))[{label}]]')
    else:
        lines.append(f'#block(above: 0.6em, below: 0.2em, inset: (left: {depth*12}pt))[#text(size: 10.5pt, weight: "bold", fill: rgb("#4a5568"))[{label}]]')

    if short:
        lines.append(f'#block(inset: (left: {depth*12+8}pt), below: 0.2em)[#text(size: 9pt, style: "italic", fill: rgb("#4a5568"))[{short}]]')
    if long_ and long_ != short:
        lines.append(f'#block(inset: (left: {depth*12+8}pt), below: 0.3em)[#text(size: 8.5pt, fill: rgb("#2d3748"))[{long_}]]')

    examples = cat.get("examples", []) or []
    if examples:
        items = ", ".join(esc(e.get("name", "")) for e in examples)
        lines.append(f'#block(inset: (left: {depth*12+8}pt), below: 0.4em)[#text(size: 8.5pt, fill: rgb("#2f855a"))[*Examples:* {items}]]')

    for child in cat.get("children", []) or []:
        render_category(child, depth + 1, lines)


def main():
    eco = json.loads(ECO.read_text())
    lines = [
        '#set document(title: "Agentic AI Ecosystem Taxonomy")',
        '#set page(paper: "a4", margin: (x: 1.6cm, y: 1.8cm), numbering: "1 / 1")',
        '#set text(font: "DejaVu Sans", size: 10pt)',
        '#set par(justify: true, leading: 0.55em)',
        '',
        '#align(center)[#text(size: 22pt, weight: "bold", fill: rgb("#1a365d"))[Agentic AI Ecosystem]]',
        '#align(center)[#text(size: 11pt, fill: rgb("#4a5568"))[A hand-curated taxonomy of the agentic AI tooling landscape]]',
        f'#align(center)[#text(size: 9pt, fill: rgb("#718096"))[Generated from ecosystem.json · updated {esc(eco.get("updated",""))}]]',
        '#v(1em)',
        '#line(length: 100%, stroke: 0.5pt + rgb("#cbd5e0"))',
        '#v(0.5em)',
    ]
    for seg in eco.get("segments", []):
        render_category(seg, 0, lines)

    OUT_TYP.parent.mkdir(parents=True, exist_ok=True)
    OUT_TYP.write_text("\n".join(lines))
    print(f"wrote {OUT_TYP.relative_to(ROOT)}")

    subprocess.run(["typst", "compile", str(OUT_TYP), str(OUT_PDF)], check=True)
    print(f"wrote {OUT_PDF.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
