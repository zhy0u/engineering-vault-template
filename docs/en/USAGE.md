# Daily use

Chinese version: [../USAGE.md](../USAGE.md).

## Layout

```
inbox/               quick notes, when you do not know where something belongs
projects/<project>/  one folder per project; create sub-folders freely
knowledge/<topic>/   general reusable knowledge (including conclusions Claude looked up)
_templates/          note templates
_attachments/        images and other attachments
_local/              not committed; for sensitive or confidential material (create it yourself)
Index.md             overall index (generated, do not edit by hand)
```

## Writing notes: any of three ways

1. **Just write**: create a `.md` in `projects/<project>/` and write whatever you like. It goes into the index with status "untidy".
2. **Use a template**: in Obsidian `Ctrl+P` → "Insert template", or on the command line:
   ```powershell
   python scripts\new_note.py ProjectA debug "title"
   python scripts\new_note.py knowledge/git knowledge "title" --slug rebase-basics
   ```
   Types: `note`, `debug` (troubleshooting), `decision`, `knowledge` (general).
3. **Drop it in inbox** and let Claude tidy it later.

File names follow `YYYY-MM-DD-topic.md`; link notes with `[[file-name]]`. The properties at the top of a note (title, type, project, summary, created, updated …) are added when it is tidied; Claude does that for you.

## Asking Claude (run `claude` inside the vault folder)

| You say | What it does |
|---|---|
| "tidy my inbox" | Reads each inbox note and gives you a proposal table (destination, name, summary, related notes, suspected duplicates). You answer accept / modify / merge / skip per row; only then does it move files and add properties |
| "tidy ProjectA" | Finds untidy notes in that project, proposes names and properties, and after confirmation only adds properties at the top. **The body is never changed** |
| "summarise ProjectA for the last two weeks" | Reads the project index and git history, then the relevant notes, and answers in the conversation |
| "save this to my notes" | Turns the conclusion into a note in `knowledge/<topic>/`; appends to a related note rather than creating a duplicate |

Everything is **proposal first, your confirmation before any change**. It never deletes, never overwrites existing content, and shows "old path → new path" before moving. AI-written notes carry `ai_generated: true` and `reviewed: false`; set `reviewed: true` once you have read them.

## Index and checks

The index is refreshed on every commit; by hand:

```powershell
python scripts\build_index.py     # regenerate Index.md and each _index.md
python scripts\lint.py            # check: untidy notes and broken links are warnings
python scripts\lint.py --strict   # strict: warnings count as errors
```

Errors are only: duplicate file names, an invalid `type`, or `project` not matching the folder.

## Commit and sync

- Obsidian Git commits once a day (or any time: `Ctrl+P` → "Git: Commit-and-sync").
- Each commit includes the freshly built index.
- Commit message format: `vault: <action> <object>`.

## "When did I write this?"

- the date in the file name = creation day;
- `created` / `updated` in the properties;
- `git log -- <file path>` for every change.

## Confidentiality

Put employer or customer confidential material in `_local/`; `.gitignore` keeps it out of the repo. Never write passwords or tokens in notes.
