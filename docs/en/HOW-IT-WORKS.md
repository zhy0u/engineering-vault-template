# How it works

Chinese version: [../HOW-IT-WORKS.md](../HOW-IT-WORKS.md).

## Overview

```
You write in Obsidian ──> files in projects/ inbox/ knowledge/
                               │
        git commit (Obsidian Git once a day / manual / scheduled task)
                               │
   pre-commit hook: scripts/build_index.py regenerates Index.md and each _index.md
                               │
                  (optional) push to your private GitHub repo

You run claude in the vault ──> reads CLAUDE.md rules + the 3 skills in .claude/skills ──> tidy / summarise / save knowledge
```

## Parts

**`CLAUDE.md`**: the rules for Claude. Only Claude Code started inside the vault folder reads it. It covers the meaning of each folder, naming, property format, the tidy-up procedure, and hard rules (never delete, never overwrite, confirm moves, never force-push, no secrets).

**`.claude/skills/`**: three skills Claude triggers when you ask for the matching thing: `triage-inbox`, `save-knowledge`, `project-digest`.

**`.claude/settings.json`**: lets Claude run the vault's scripts and common git commands, and explicitly denies `rm`, `del`, `git push --force`, `git reset --hard`, `git clean` and similar.

**`scripts/`**
- `vaultlib.py`: shared code for reading properties and walking notes.
- `build_index.py`: generates the indexes. Notes without properties are included with status "untidy".
- `lint.py`: format checks.
- `new_note.py`: create a note from a template.
- `bootstrap.ps1` / `setup-new-machine.ps1` / `sync.ps1`: first-time setup, new-computer setup, manual sync.
- `githooks/pre-commit`: refreshes the index before each commit; if Python is missing or the script fails it skips silently and never blocks the commit. It needs `git config core.hooksPath scripts/githooks` (the installer does this). That setting lives in `.git/config` and is **not synced**, so each clone needs it once.

**`.obsidian/`**: window state, core plugins, template folder, the Obsidian Git plugin and its config (auto-commit every 1440 minutes).

**`.vault-lang`**: `en` or `zh`; read by the scripts to pick the language of generated indexes and messages (missing = `zh`).

**`_meta/user-level/`** (optional): the user-level auto-capture hook; see the FAQ.

## What "not yet tidied" means

You do not have to follow the format. A note without properties, or with a file name that has no date, is indexed as "untidy" and lint only warns. When you want to tidy, ask Claude for a proposal: it only adds properties at the top and suggests a file name; the body is untouched. Writing costs nothing, and tidying has a reviewer.

## Where your data lives

Entirely on your computer; and, if you chose `-Github`, in a private repository under your own account. The template's author cannot see your content.
