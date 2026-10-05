---
name: save-knowledge
description: Save a conclusion, procedure or principle that was just looked up as a knowledge note. Use when the user says "save this to notes", "keep this", "remember this in the vault" (记到笔记 / 存一下).
---

# save-knowledge

Turn the knowledge worth keeping from the current conversation into a note under `knowledge/`.

## Steps

1. Decide what to save: only conclusions, key reasons, steps, commands and source links — not chat transcripts and not trial and error.
2. Pick the topic folder `knowledge/<topic>/` in lowercase English (embedded, electronics, c, docker, git, ai …); reuse existing folders first.
3. Search first: `Grep` keywords and `Glob` over `knowledge/` and related projects.
   - If a related note exists: append, update `updated`, add a line to the "Changelog", and do not create a duplicate or rewrite existing content.
   - If not: create one with `python scripts/new_note.py knowledge/<topic> knowledge "<title>"`, then edit the content.
4. Fill the frontmatter: one-line `summary`; `source: claude`; `ai_generated: true`; `reviewed: false`; `project:` if related to a project; `tags`.
5. Keep the "Key points / Content / Sources / Related" structure. If the conclusion has no external source, keep the `> [!warning] Tested by me only; not verified by an external source` callout.
6. Link: use `[[file-name]]` to related project notes, and append a back-link in the "Related" section of that project note (append only; change nothing else).
7. Finish: run `python scripts/build_index.py` and `python scripts/lint.py`, then commit and push per the sync rules in CLAUDE.md.
8. Reply to the user with where it was saved (file name) and remind them it is AI-generated and not yet reviewed.

## Do not

- Do not save passwords, tokens or internal addresses.
- Do not touch the user's existing notes just to make them neat.
