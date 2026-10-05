---
name: triage-inbox
description: Tidy the quick notes in inbox/: give a classification proposal, and only after the user confirms move files and add frontmatter and links. Use when the user says "tidy my inbox", "triage" (整理 inbox).
---

# triage-inbox

## Steps

1. Run `git status` first to make sure no uncommitted user changes get involved.
2. List every note under `inbox/` and read each one.
3. For each note decide:
   - type: note / debug / decision / knowledge
   - destination: `projects/<project>/` or `knowledge/<topic>/` (if unsure, leave it in inbox and say what information is missing)
   - new file name: `YYYY-MM-DD-topic.md`; take the date written in the note, otherwise the file's creation time
   - summary (one line) and tags
   - related existing notes (Grep first) and suggested `[[links]]`
   - whether it duplicates an existing note (report only, never merge)
   - whether it contains passwords, tokens or internal addresses (flag it and suggest moving it to `_local/`)
4. Give the proposal to the user as a table: `file | type | destination | title | summary | related notes | duplicate of | action`, action defaulting to accept. At most 20 notes per batch.
5. **Wait for the user's confirmation.** The user can say accept / modify / merge / skip per row. Do not touch any file without it.
6. For confirmed items:
   - move and rename with `git mv`
   - complete the frontmatter (`created` from the original recording date; mark the summary etc. you wrote with `ai_generated: true`, `reviewed: false`)
   - keep the body as is; only append links to the "Related" section at the end
7. Run `python scripts/build_index.py` and `python scripts/lint.py` and fix errors.
8. One commit per batch: `vault: triage inbox batch <number>`, push if there is an origin.
9. Report: how many were processed, skipped and remaining, and what the user needs to decide.

## Do not

Delete any file; merge duplicates automatically; rewrite bodies; move anything without confirmation.
