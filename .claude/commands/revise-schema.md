---
description: Iteratively revise the top-level taxonomy schema
argument-hint: "[optional feedback]"
---

# /revise-schema

The taxonomy's top-level shape is the heart of this project. This command is the
iteration loop for getting it right: show the current proposed schema in a
reviewable tree format, accept feedback, repeat until the user is happy, then
execute the restructure.

## Where "current" lives

The schema under revision is tracked at `schema/proposed.yaml` (create it if it
doesn't exist). This file holds the **proposed** top-level structure — it is
NOT the live graph. The live graph stays in `graph/nodes.json` until the user
explicitly says "execute" / "apply" / "ship it".

Structure of `schema/proposed.yaml`:

```yaml
version: N              # bumped on every iteration
notes: |
  Free-form notes about what changed in this version and why.
segments:
  - name: Prompts
    kind: runtime        # runtime | meta
    absorbs:             # old top-level segments this one swallows
      - Prompt Management
      - Workflow Definition
    children:            # optional — for deeper skeletal shape
      - name: Instruction Assembly
      - name: Conversational Control
  - name: Models
    ...
```

## Steps

1. **Load state.** Read `schema/proposed.yaml`. If it doesn't exist yet, seed it
   from the last proposal in the conversation (or from `ecosystem.json` as a
   starting point — but **never** assume the live graph is the latest proposal).

2. **Render the current schema.** Print it in this exact format, grouped by
   `kind`. Use indentation for depth. Include absorption hints as dim parens:

   ```
   ## Proposed schema — v{N}

   ### Runtime-layer segments ({count})
    1. Prompts            ← Prompt Management, Workflow Definition, Formatting
        ├── Instruction Assembly
        └── Conversational Control
    2. Models             ← LLMs, Embedding Models, Trainers, RL, Synthetic Data
    ...

   ### Meta / ecosystem segments ({count})
   15. Frameworks & Runtimes  ← Frameworks, Runtimes, Harnesses, ...
   ...

   Total: {N} top-level segments.
   ```

   Always show the full tree. Do not summarise or elide. This is the artefact
   the user is reviewing — they need to see it whole.

3. **Integrate the user's feedback.** If `$ARGUMENTS` is present, treat it as
   the feedback for this round. Otherwise read the most recent user message in
   the conversation. Apply the changes directly to `schema/proposed.yaml`:
   - Moves ("put X under Y")
   - Renames ("call it Grounding not Search")
   - Adds ("add Agent in the Loop as sibling of HITL")
   - Deletes ("drop Destinations — no evidence")
   - Reorderings, regroupings, depth changes

   Bump `version`. Record a one-line entry in `notes` describing the change.

4. **Re-render.** Print the updated schema in the same format as step 2. Do
   NOT ask the user to confirm small structural questions inline — just apply
   them. Only flag genuine ambiguities.

5. **Stop and wait.** Do not run any build scripts, do not touch
   `graph/nodes.json`, do not regenerate the site. The only output is the
   updated `schema/proposed.yaml` and the rendered tree. The user will either
   give more feedback (re-invoke this command) or say "execute it".

## When the user says "execute" / "apply" / "ship it" / "do it"

That's the signal to leave this command and run the restructure workflow (a
separate concern — not part of /revise-schema). At that point:

1. Build the restructure plan from `schema/proposed.yaml` against
   `graph/nodes.json`.
2. Create new parent category nodes, rewire `SUBCATEGORY_OF` edges for old
   top-level segments so they become children of the new parents, update all
   descendant `path` arrays.
3. Run `validate_graph.py` → `build_tree.py` → `generate_readme.py` →
   `build_site.py`.
4. Do NOT commit automatically — report the diff and let the user commit.

## Principles to enforce while iterating

- **Narrow top, deep middle** (CLAUDE.md principle 7). Push specificity down.
- **Depth up to 10 levels** where each level earns its place.
- **Every new segment earns a description later** via /describe-missing —
  don't block iteration on descriptions.
- **Absorption preserves identity**: when segment X is absorbed into new
  top-level Y, X becomes a child of Y, not a deletion. Old subcategories
  under X stay intact one level deeper.
- **No orphans**: every old top-level segment must land somewhere in the new
  schema. If the user's feedback would orphan one, flag it and ask.

## Feedback this invocation

$ARGUMENTS
