---
description: Rebuild all derived artifacts (tree, README, PDF) from the graph source of truth
---

Run these in order from the repo root, reporting output of each step. Stop and diagnose on failure.

1. `python3 scripts/build_tree.py` — regenerate `ecosystem.json` from `graph/nodes.json` + `graph/edges.json`
2. `python3 scripts/generate_readme.py` — regenerate `README.md`
3. `python3 scripts/build_pdf.py` — regenerate `docs/ecosystem.pdf`

After all three succeed, report: segment count, category count, project count, and confirm PDF path. Do not commit or push unless the user asks.

The deployed MkDocs site is built by `.github/workflows/deploy-docs.yml` on push to `main`, so committing and pushing these regenerated files is what triggers the site update.
