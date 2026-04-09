---
description: Draft missing category descriptions in parallel via sub-agents
---

Fill in missing `short_description` (and optionally `long_description`) on every Category in `graph/nodes.json`, using parallel sub-agents so the research for independent categories runs concurrently.

## Defaults

- Field: `short_description` (pass `long` or `both` in $ARGUMENTS to target other fields)
- Batch size: **12** categories per agent
- Max categories this run: **60** (pass `--all` in $ARGUMENTS to remove the cap)

## Steps

1. **Audit** — run `python3 scripts/describe_context.py --missing short` (or `long` / `both` per args). The output is a JSON array where each entry is a self-contained context blob: id, label, path, parent info, sibling labels+shorts, children, existing projects, and current values.

2. **Chunk** — split the array into chunks of **12**. Cap at 60 total unless `--all`. If fewer than 12 remain, send them as one batch.

3. **Dispatch parallel sub-agents** — in a single message, spawn one `general-purpose` agent per chunk using the Agent tool. Each agent prompt should:
   - Contain the **entire** JSON array for that chunk (don't try to re-fetch from disk — the context blob is self-contained).
   - Explain the project purpose: mapping categories/subcategories/connections in agentic AI; taxonomy is built backwards from real projects as evidence of functional slots.
   - Specify the writing contract:
     - `short_description`: one sentence, **≤140 characters**, defines what belongs in this slot and how it differs from its siblings. No marketing language. No meta-phrases like "This category contains…". Start with a noun or gerund.
     - `long_description`: 2–3 sentences, **≤400 characters**, expanding on what's in-scope vs out-of-scope, typical interface (library / service / protocol / etc.), and where it sits in an agentic stack.
     - `examples_narrative`: OPTIONAL. One short paragraph of prose mentioning the existing projects as illustrative examples, only if it adds clarity. Leave empty otherwise.
   - **Output format**: the agent must respond with ONLY a fenced JSON code block containing an array of objects `{id, short_description, long_description, examples_narrative}`. One entry per input category. No prose before or after. No markdown. Do NOT write to any file.
   - Instruct the agent that if it cannot confidently describe a category (e.g. unclear label, no context), it should return an empty string for the fields it can't fill — not guess.

4. **Collect and merge** — when all agents return, parse each fenced JSON block and concatenate into a single array. If any agent returns malformed output, retry just that chunk with a reminder about the format.

5. **Present for confirmation** — before writing anything, show the user a compact table:

   ```
   cat:foo/bar
     short: <proposed short description>
     long:  <proposed long description (truncated to 120 chars)>
   ```

   Group by parent segment for readability. Note how many entries have empty fields (agent declined).

6. **Apply on confirmation** — on user approval, write the full proposals array to `proposals.json` in repo root, then run `python3 scripts/apply_descriptions.py`. If the user wants to edit a few entries, ask them to specify the edits inline; update the array; then apply.

7. **Post-apply** — run these in sequence and report the deltas:
   - `python3 scripts/validate_graph.py`
   - `python3 scripts/build_tree.py`
   - `python3 scripts/generate_readme.py`
   - `python3 scripts/build_kumu.py`

8. **Do NOT commit** — the user commits manually after reviewing. Report which files changed and suggest running `/update-readme` or a commit command if they want.

## Agent prompt template

Use this exact structure inside each Agent tool call's prompt (replacing the placeholders):

```
You are drafting descriptions for a taxonomy of agentic AI tooling.

PROJECT PURPOSE: This repository maps categories, subcategories, and connections
between emerging agentic AI tools. It is a taxonomy, not a project directory.
Every category represents a distinct functional slot in an agentic stack.
Projects are collected as EVIDENCE that a slot exists.

YOUR TASK: For each category in the JSON array below, write a short_description
and long_description (and optionally examples_narrative). Each category's context
block contains its label, path, parent info, sibling labels+shorts, children,
and existing example projects.

CONTRACT:
- short_description: ONE sentence, ≤140 chars. Defines what belongs here and
  distinguishes it from siblings. Start with a noun or gerund. No marketing
  language, no "This category contains…", no "A curated collection of…".
- long_description: 2–3 sentences, ≤400 chars. Scope boundaries, typical
  interface/shape (library / service / protocol / SaaS / etc.), where it sits
  in an agentic stack.
- examples_narrative: OPTIONAL. One short paragraph mentioning the example
  projects if it adds clarity. Leave as empty string otherwise.
- If a category is unclear or you lack context, return empty strings — do not guess.

OUTPUT FORMAT: Respond with ONLY a fenced JSON code block. No prose. No markdown
outside the block. The block must contain an array of objects with keys
{id, short_description, long_description, examples_narrative}. One object per
input category, in the same order.

INPUT:
<paste the JSON chunk here>
```

$ARGUMENTS
