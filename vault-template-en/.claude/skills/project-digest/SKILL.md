---
name: project-digest
description: Summarise a project's recent progress, or give highlights and an index by topic. Use when the user says "summarise ProjectA for the last two weeks", "what pitfalls do we have around ST25" (总结 ProjectA 最近两周).
---

# project-digest

## Summarise project progress over time

1. Read `projects/<project>/_index.md` and mark the notes in the time range.
2. Run `git log --since=<date> --name-status -- projects/<project>` to see which notes were added and which modified (the modification date reflects progress better than `created`).
3. Read the bodies of the relevant notes, not just the summaries.
4. Output:
   - what was completed / solved in the period (root cause and fix for debug notes, conclusions for decisions)
   - problems still open (status other than solved/accepted)
   - new decisions
   - content worth turning into knowledge but not yet captured
   - a `[[note-file-name]]` after every conclusion so the user can click through

## Find highlights by topic

1. Grep the topic keyword first (part number, protocol name …) over `projects/` and `knowledge/`.
2. Filter with the frontmatter `type`, `status` and `tags`, and sort by `created`.
3. Give a time-ordered list first (date, note, key point), then the 3–5 most important lessons.

## Rules

- Answer only from the notes and git history; if the notes do not say it, say so. Do not fill in from impression.
- By default answer only in the conversation; when the user asks to keep it, write it as a note with `new_note.py`.
