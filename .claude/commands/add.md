---
description: Add one or more projects to ecosystem.json (segments-first structure)
---

The user will paste a list of projects in the syntax:

```
<github-url> <category path using -> or > separators>
```

`ecosystem.json` is structured as a nested tree:

```json
{
  "segments": [
    {
      "name": "Frameworks",
      "examples": [{"name": "...", "url": "..."}],
      "children": [
        {"name": "Voice", "examples": [...]}
      ]
    }
  ]
}
```

For each line the user provides:
1. Parse the URL and category path.
2. Derive `name` from the final URL segment.
3. Normalise the path (split on `->` or `>`, trim, preserve acronyms: CLI, SDK, macOS, .NET, RAG, MCP, GUI, TUI, IDE, API, OS).
4. Walk the `segments` tree, creating any missing nodes along the path. Append the project to the target node's `examples` array.
5. Preserve existing structure — do NOT reshuffle segments or re-sort.
6. Do NOT regenerate the README in this command — that's `/update-readme`.
7. Report back: count added, new total.

If no projects are pasted, ask the user for the batch.

$ARGUMENTS
