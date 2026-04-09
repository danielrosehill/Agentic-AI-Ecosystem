---
description: Organise and normalise the taxonomy in ecosystem.json
---

Review `@ecosystem.json` and clean up the taxonomy:

1. **Merge near-duplicate top-level segments** (e.g. `Tools` vs `Tooling`, `Frontends` vs `Frontend`, `Agent to Agent` vs `Agent Collaboration`). Pick one canonical form and rewrite all affected `path` arrays.
2. **Flag orphans** — projects whose top category has only one member. Suggest a better home or merge.
3. **Normalise casing**: CLI, SDK, macOS, .NET, RAG, MCP, GUI, TUI, IDE, API should preserve their conventional casing. Other words title-case.
4. **Check for duplicate project entries** (same URL appearing twice).
5. **Preserve order** of the projects array — do not reshuffle unless merging duplicates.

Before making changes, present a short diff plan (what you'd merge/rename) and ask the user to confirm. After confirmation, apply edits to `ecosystem.json` only. Do NOT regenerate the README — that's `/update-readme`.
