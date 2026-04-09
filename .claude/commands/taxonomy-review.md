---
description: Review ecosystem taxonomy for dedup, logical grouping, and descriptions
---

Review `ecosystem.json` and improve the taxonomy:

1. **Deduplicate**
   - Find segments/subcategories that overlap semantically (e.g. near-synonyms, same concept under different names).
   - Find projects listed more than once across segments.
   - Propose merges; after confirmation, consolidate.

2. **Logical grouping**
   - Check that segments sit at a consistent level of abstraction.
   - Collapse near-empty segments into a parent where it makes sense.
   - Promote oversized subcategories to top-level segments where it makes sense.
   - Ensure alphabetical ordering of segments and children (unless a deliberate grouping overrides it).

3. **Descriptions (required)**
   - Every segment and every subcategory (`children[*]`) MUST have a `description` field — a 1–2 sentence explanation of what belongs there and how it differs from sibling categories.
   - If you cannot yet write a meaningful description, add `"description": ""` as a placeholder so the field exists everywhere.
   - Do not leave any segment or subcategory without the key.

4. **Output**
   - Before editing, summarise proposed dedup/restructure moves and wait for confirmation on anything non-trivial.
   - After edits, report: # segments, # subcats, # projects, and any remaining empty descriptions.

Do not touch the `examples[]` entries' schema. Preserve `name` + `url` on projects.
