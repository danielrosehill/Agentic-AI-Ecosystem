---
description: Render a timestamped Graphviz snapshot (PDF/PNG/SVG) from the graph
---

Run `python3 scripts/build_dot.py` from the repo root. It will write to `snapshots/<today>/`:
- `ecosystem.{dot,pdf,png,svg}` — radial (twopi) full map
- `ecosystem-tree.{dot,pdf,png,svg}` — hierarchical (dot) full map
- `segments/<slug>.{dot,pdf,png,svg}` — one per top-level segment

Report the snapshot directory and file count. If Graphviz is missing, tell the user to `sudo apt install graphviz`.

$ARGUMENTS
