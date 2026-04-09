#!/usr/bin/env python3
"""Apply description proposals to graph/nodes.json.

Reads a JSON file (default: proposals.json in repo root) shaped as:

  [
    {
      "id": "cat:foo/bar",
      "short_description": "...",
      "long_description": "...",
      "examples_narrative": "..."      # optional
    },
    ...
  ]

Only fields present in each entry are written — so a proposal can update
just short_description and leave long_description alone. Missing ids are
reported but skipped. Dry-run prints the diff without writing.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODES_IN = ROOT / "graph" / "nodes.json"

FIELDS = ("short_description", "long_description", "examples_narrative")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("proposals", nargs="?", default=str(ROOT / "proposals.json"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    proposals_path = Path(args.proposals)
    if not proposals_path.exists():
        sys.stderr.write(f"proposals file not found: {proposals_path}\n")
        return 1

    proposals = json.loads(proposals_path.read_text())
    data = json.loads(NODES_IN.read_text())
    nodes = {n["id"]: n for n in data["nodes"]}

    applied = 0
    missing = []
    for p in proposals:
        nid = p.get("id")
        if nid not in nodes:
            missing.append(nid)
            continue
        n = nodes[nid]
        if n["type"] != "Category":
            sys.stderr.write(f"skip non-category: {nid}\n")
            continue
        changed = []
        for f in FIELDS:
            if f in p and (p[f] or "") != (n.get(f) or ""):
                if args.dry_run:
                    changed.append(f)
                else:
                    n[f] = p[f] or ""
                    changed.append(f)
        if changed:
            applied += 1
            print(f"  {nid}  [{' '.join(changed)}]")

    if missing:
        sys.stderr.write(f"\n⚠ {len(missing)} ids not found in graph:\n")
        for m in missing:
            sys.stderr.write(f"  · {m}\n")

    if args.dry_run:
        print(f"\n(dry run — {applied} categories would be updated)")
        return 0

    NODES_IN.write_text(json.dumps(data, indent=2) + "\n")
    print(f"\napplied to {applied} categories → {NODES_IN.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
