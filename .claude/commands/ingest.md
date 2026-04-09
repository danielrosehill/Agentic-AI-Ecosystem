---
description: Classification-aware ingest of a new project into the ecosystem graph
---

This is the **thinking** ingest flow — for when the user gives you one or more projects (URL, or URL + rough notes) and wants you to figure out where each belongs in the taxonomy. Contrast with `/add`, which is the mechanical bulk-add command where the user already specifies the category path.

## Batch support

The user may paste a single project or a batch. A batch looks like a list of URLs, optionally each followed by a free-form note on the same line or the next line (e.g. "workflow focused", "think this is a new MCP gateway", "probably Frameworks → Voice"). Parse loosely — blank lines separate entries, notes are hints not commands.

For batches:
1. Process each project through the classification steps below **independently**.
2. Collect all proposals first, then present them together as a single plan before editing the file:
   - Table or list: project → proposed path → `existing` / `new subcat` / `new segment`
   - Group obvious/uncontroversial items separately from ones that need judgment
3. Wait for a single confirmation covering the batch (user can approve all, reject some, or adjust).
4. Apply all insertions in one pass, then report totals.

For a single project, you may skip the batch summary and go straight to a proposal.

Remember the project objective (see `CLAUDE.md`): **this repo is a taxonomy, with example projects as evidence.** The job when ingesting is not "dump this project somewhere" — it's "what classification does this project reveal or confirm?"

## Steps

1. **Read the project.** Fetch the URL (WebFetch) and/or read the repo README. Identify:
   - What it *is* (framework? runtime? harness? tool? standard? dataset?)
   - What functional slot it occupies in an agentic stack
   - What makes it distinct from near neighbours

2. **Survey the existing taxonomy.** Load `graph/nodes.json` (source of truth) — you can also skim `ecosystem.json` which is a regenerated tree view. Look for:
   - An exact match (existing segment/subcat that clearly fits)
   - A close match (fits but would benefit from a new, more specific subcat)
   - No match (genuinely new slot — a signal the taxonomy needs to grow)

3. **Propose a classification.** Report to the user, briefly:
   - Project one-liner (your own words, not the README's marketing copy)
   - Proposed path (e.g. `Frameworks → Voice` or `Context → Context Optimisation`)
   - Whether this is: `existing slot` / `new subcategory` / `new segment`
   - If new: the `description` you'd write for the new node
   - If the project reveals a distinction the current taxonomy flattens, flag it and suggest a split

4. **Wait for confirmation** unless the classification is obvious and uncontroversial (e.g. "another MCP gateway" into `MCP → Gateways`). For any new segment, new subcategory, or category split, **always confirm first.**

5. **Insert into the graph.** Edit `graph/nodes.json` and `graph/edges.json` directly — they are the source of truth.
   - Add new `Category` nodes (id `cat:<slug-path>`) with `description` if creating a new slot. Add a `SUBCATEGORY_OF` edge to the parent (unless it's a root segment).
   - Add a `Project` node (id `proj:<slug-name>`, disambiguated with `--<parent-slug>` on collision) with `label`, `url`. Add a `CATEGORY_OF` edge from the project to its category.
   - Slug rule: lowercase, non-alphanumerics → `-`, trim.
   - Bump `updated` in both files to today.
   - Run `python3 scripts/build_tree.py` to regenerate `ecosystem.json`.

6. **Do NOT regenerate the README** — that's `/update-readme`.

7. **Report:** path used, whether new nodes were created, new total project count.

## Classification heuristics

- **"It's a framework for X"** → `Frameworks → X` (create subcat if absent)
- **"It's an MCP server for X"** → `MCP → Third Party` or a more specific subcat
- **"It's a CLI/TUI for interacting with agents"** → `Frontends → TUIs and CLIs` or `Agents → Harnesses → CLIs`
- **"It's a runtime/sandbox"** → `Runtimes → Sandboxes`
- **"It's a memory layer"** → `Memory` (check internal subcats)
- **"It's an eval harness"** → `Evals and Experiment Tracking`
- **Project name is generic and could fit many slots** → pick by *primary* function, not secondary features

When unsure between two slots, prefer the *more specific* one. When a subcategory is borderline-warranted, **create it** — granularity is the point.

## Anti-patterns

- Creating a subcategory named after the project itself (e.g. `OpenClaw`). Subcategories are functional slots.
- Adding to `Uncategorized` instead of thinking. `Uncategorized` is a failure mode, not a bucket.
- Writing a project description into the `examples[]` entry. Entries are `{name, url}` only.
- Silently creating new segments without surfacing the decision to the user.

$ARGUMENTS
