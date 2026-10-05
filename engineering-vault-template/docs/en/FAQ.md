# FAQ

Chinese version: [../FAQ.md](../FAQ.md).

**Do I have to install Claude Code?**
No. Obsidian + git + the Python scripts already give you notes, version history and indexes. Claude Code only does tidying, summarising and saving knowledge, and needs a Claude account.

**Do I need GitHub?**
No; local commits are enough. For a cloud backup use a private repository.

**Can I write in any format?**
Yes. Notes without a format are indexed as "未规整" (not yet tidied), which is only a warning. Ask Claude for a proposal when you want to tidy.

**The index did not update after a commit.**
Check that `git config core.hooksPath` prints `scripts/githooks`; if not, run `git config core.hooksPath scripts/githooks`. Also make sure `python` runs. `python scripts\build_index.py` always works by hand.

**Auto-commit never fires.**
The Obsidian Git timer only counts while Obsidian runs and resets on every restart. A once-a-day interval may never be reached if you close Obsidian daily. Use the daily scheduled task from `scripts\setup-new-machine.ps1`, or commit by hand with `Ctrl+P` → "Git: Commit-and-sync".

**My commits show the wrong (employer) email.**
Git uses your global identity. Fix it for future commits with `git config --global user.email "you@personal.example"`, or per repo without `--global`. To make git refuse to guess, run `git config --global user.useConfigOnly true`; it then asks you to set an identity in each repo. To rewrite commits that were already made and pushed:

```powershell
git config user.name "Your Name"
git config user.email "you@personal.example"
git log --format="%h %an <%ae> | %cn <%ce>"
git rebase -r --root --exec "git commit --amend --reset-author --no-edit"
git push --force-with-lease
```

This changes every commit's hash, so do it before others have cloned the repo. The old commits may stay reachable on GitHub by their old hashes for a while; GitHub Support can purge them if that matters. In GitHub → Settings → Emails you can also turn on "Keep my email addresses private" and "Block command line pushes that expose my email".

**What can Claude do in this vault, and what can it not?**
It can read notes, produce tidy-up proposals, and — after you confirm — add properties, move files (`git mv`), commit and summarise. It cannot (by rule and by permission): delete files, overwrite existing content, force-push, `git reset --hard`, or `git clean`. When unsure it asks.

**Do things I ask Claude in ordinary chats go into the vault automatically?**
No. Only if you say "save this to my notes" in a Claude Code session inside the vault, or if you installed the auto-capture hook below and are in a Claude Code session in *another project*.

## Auto-capture hook (optional)

In your other projects' Claude Code sessions, it reminds Claude once before each turn ends to check whether there is general, reusable knowledge worth saving; if so it writes it to `knowledge/`, otherwise it stays silent.

```powershell
python <vault>\_meta\user-level\install_user_level.py --dry-run   # show what would change
python <vault>\_meta\user-level\install_user_level.py             # install (asks first)
python <vault>\_meta\user-level\install_user_level.py --uninstall # remove completely
# temporary off: create an empty file %USERPROFILE%\.claude\vault-checkpoint.off ; delete it to resume
```

It changes three things under `~/.claude/`: `hooks/vault-checkpoint.sh`, a marked section in `CLAUDE.md`, and a Stop hook plus a vault directory permission in `settings.json`. Everything else is left alone; a `.bak-<timestamp>` backup is made only when content changes; if `settings.json` is not valid JSON the script aborts. Takes effect in new sessions only.

Limits: the hook is only a reminder, Claude may decide there is nothing to save; each turn costs an extra round trip and a little usage; the hook runs under Git Bash (the Windows default), so if your shell is set to PowerShell it will error — switch it off with the toggle; writes and commits still follow your permission mode prompts.

**Privacy:** it means knowledge found in your other projects (including employer projects) may be written into your own private repository. The rules tell Claude to save only general conclusions, strip project and company context, never save secrets or internal addresses, and skip when unsure; AI-written notes default to `reviewed: false`, so review them regularly. **Whether your employer allows this is for you to confirm.**

**How do I update the template?**
Template updates do not change your vault automatically. Compare `scripts/`, `.claude/` and `CLAUDE.md` in `vault-template/` and merge by hand (do not overwrite your own edits to `CLAUDE.md`).
