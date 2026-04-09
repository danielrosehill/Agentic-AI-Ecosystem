---
description: Add one or more projects to ecosystem.json
---

The user will paste a list of projects in the syntax:

```
<github-url> <category path using -> or > separators>
```

For each line:
1. Parse the URL and category path.
2. Derive `name` from the final URL segment (keep original casing where reasonable).
3. Normalise the path into an array of segments (split on `->` or `>`, trim whitespace, title-case sensibly but preserve acronyms like CLI, SDK, macOS, .NET, RAG, MCP, GUI, TUI, IDE).
4. Append a new entry to the `projects` array in `@ecosystem.json`:
   ```json
   {"name": "...", "url": "...", "path": ["...", "..."]}
   ```
5. Do NOT regenerate the README in this command — that's `/update-readme`.
6. Report back a count of added projects and new total.

If the user provides no projects in the invocation, ask them to paste the batch.

$ARGUMENTS
