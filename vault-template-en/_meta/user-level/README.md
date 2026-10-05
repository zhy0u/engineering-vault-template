# User-level auto-capture (optional)

In Claude Code sessions in your **other projects**, check once before each turn ends: did this turn produce general knowledge worth recording in the engineering-vault? If yes, write it to `knowledge/`; if not, finish silently. The approach follows the Stop hook of zhfans/dotagents, without needing `jq`.

This changes `~/.claude/` (user level, applies to every project), so it does not live in the vault's `.claude/` and is never installed automatically; you run the installer yourself.

## Three parts

| Part | Purpose |
|---|---|
| A marked section in `~/.claude/CLAUDE.md` | Tells Claude where the knowledge base is, what to record and not, how to write it, how to commit |
| `~/.claude/hooks/vault-checkpoint.sh` (Stop hook) | Reminds Claude to run the check before each turn ends; ends silently when there is nothing to record |
| `additionalDirectories` in `settings.json` | Lets sessions in other projects read and write the vault folder (writes still prompt for permission) |

## Install

```
python <your-vault-path>\_meta\user-level\install_user_level.py
```

The script lists what it will change and asks first. A backup (`<name>.bak-<timestamp>`) is made only when the content really changes, everything else is kept as is; if `settings.json` is not valid JSON the script aborts without changing anything. Claude Code sessions that are already open must be restarted.

To see what it would do first, add `--dry-run`.

## Turn off, uninstall

- Temporarily off: create an empty file `%USERPROFILE%\.claude\vault-checkpoint.off`; delete it to resume.
- Uninstall: `python <your-vault-path>\_meta\user-level\install_user_level.py --uninstall` removes the section, the hook, the vault directory permission and the hook file; nothing else is touched.

## What it does not do, and the cost

- Sessions started inside the vault do not trigger it (that is where you tidy notes anyway).
- The hook is a reminder, not a command: Claude may decide there is nothing to record, and that is expected.
- **One extra round trip per turn**, including turns with nothing to record, adds a little usage and latency. If it annoys you, use the off switch above.
- Writing to the vault, committing and pushing from other projects still prompts according to your permission mode; you can approve each time.
- The hook runs under Git Bash (the Claude Code default on Windows). If you switched Claude Code's shell to PowerShell the hook will error; turn it off or rewrite it.

## Privacy

Auto-capture means knowledge you find in other projects (including employer projects) may be written into your own private GitHub repository. `CLAUDE.snippet.md` already tells Claude to record general conclusions only, strip project / customer / company context first, never record keys or internal addresses, and skip when unsure. AI-written notes default to `reviewed: false`, so you can review them regularly and delete anything that should not be there. Whether your employer allows this is for you to confirm.
