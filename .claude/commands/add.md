---
description: Add one or more projects to the ecosystem graph
---

The user will paste a list of projects in the syntax:

```
<url> <category path using -> or > separators>
```

**Source of truth is the graph.** Edit `graph/nodes.json` and `graph/edges.json` directly. `ecosystem.json` and `README.md` are regenerated from the graph.

Graph model:
- Node types: `Category`, `Project`
- Edge types: `SUBCATEGORY_OF` (Category → parent Category), `CATEGORY_OF` (Project → Category)
- IDs: `cat:<slug-path>` (e.g. `cat:frameworks/voice`), `proj:<slug-name>` (disambiguate collisions with `--<parent-slug>`)
- Slug rule: lowercase, non-alphanumerics → `-`, trim.

For each line the user provides:

1. Parse URL and category path.
2. Derive `name` from the final URL segment (preserve acronyms: CLI, SDK, macOS, .NET, RAG, MCP, GUI, TUI, IDE, API, OS).
3. Normalise the category path (split on `->` or `>`, trim).
4. Walk the path. For each segment, compute `cat:<slug-path>`. If the category node doesn't exist in `graph/nodes.json`, create it with empty `description`, and add a `SUBCATEGORY_OF` edge to its parent (if any). **Never invent a category silently at segment level without flagging it — surface new top-level segments to the user.**
5. Create the `Project` node if absent, with `label`, `url`, `type: "Project"`. Add a `CATEGORY_OF` edge to the leaf category.
6. Bump `updated` in both `nodes.json` and `edges.json` to today.
7. Run `python3 scripts/build_tree.py` to regenerate `ecosystem.json`. Do NOT regenerate the README — that's `/update-readme`.
8. Report: count added, new totals (nodes, edges, projects).

If no projects are pasted, ask for the batch.

$ARGUMENTS
