---
description: Full workflow — add batch of projects, update JSON, regenerate README, commit and push
---

Full ingest workflow. The user will paste a batch of projects in the syntax used by `/add`:

```
<github-url> <category path using -> or > separators>
```

Steps:
1. Follow the `/add` logic to append all entries to `@ecosystem.json`.
2. Run `python3 scripts/generate_readme.py` to regenerate `README.md`.
3. Show `git status` and `git diff --stat` so the user can eyeball the changes.
4. Ask the user to confirm before committing.
5. On confirmation, stage `ecosystem.json` and `README.md`, commit with a message like `Add N projects (total M)`, and `git push`.

$ARGUMENTS
