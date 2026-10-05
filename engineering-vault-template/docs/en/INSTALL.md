# Installation

Goal: get your own independent notes vault (Obsidian + git) on your computer, optionally backed up to your own private GitHub repo, with Claude Code able to tidy notes inside it.

Steps are for Windows; macOS / Linux differences are at the end. Chinese version: [../INSTALL.md](../INSTALL.md).

## 0. Prerequisites

| Software | Purpose | Install |
|---|---|---|
| Git | history | `winget install Git.Git` |
| Python 3 | index and lint scripts | `winget install Python.Python.3.12` |
| Obsidian | writing | `winget install Obsidian.Obsidian` |
| Claude Code | tidy / search / summarise (optional, needs a Claude account) | `winget install Anthropic.ClaudeCode` |
| GitHub CLI | one-command cloud repo (optional) | `winget install GitHub.cli` |

**Close the terminal and open a new one** so PATH updates. Check with `git --version` and `python --version`.

Set your git identity (use a personal address, not an employer's):

```powershell
git config --global user.name "Your Name"
git config --global user.email "your-personal-email"
```

## 1. Get the template

```powershell
git clone https://github.com/<whoever-sent-you-this>/engineering-vault-template.git
cd engineering-vault-template
```

## 2. Install your own vault

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1 -Path D:\my-vault
```

It copies `vault-template/` to `D:\my-vault` (it stops if the target is not empty, never overwrites) → `git init` → sets the index hook → builds the first index → makes the first commit.

To also create a private cloud repo:

```powershell
gh auth login
powershell -ExecutionPolicy Bypass -File install.ps1 -Path D:\my-vault -Github
```

The repo name defaults to `<your-github-username>/engineering-vault`, private. Use `-Repo you/other-name` to change it.

> The template folder is only the source of the install; you can delete it afterwards. From now on you work in `D:\my-vault`.

## 3. Configure Obsidian

1. Obsidian → "Open folder as vault" → choose `D:\my-vault`.
2. Settings → Community plugins → turn off restricted mode, then enable **Obsidian Git** (its files are already in the vault; nothing to download).
3. Fully quit and reopen Obsidian. The auto-commit interval is 1440 minutes (once a day); change it in Settings → Git → Automatic.
4. The Templates core plugin already points at `_templates`.

## 4. Tidy with Claude Code (optional)

```powershell
cd D:\my-vault
claude
```

Log in and choose "trust this folder" the first time. Then just ask, e.g. "tidy my inbox". See [USAGE.md](USAGE.md).

## 5. Two optional extras

```powershell
powershell -ExecutionPolicy Bypass -File D:\my-vault\scripts\setup-new-machine.ps1
```

It checks the tools, confirms the index hook, and asks separately about:

- **Daily scheduled task**: runs `scripts\sync.ps1` (commit, pull, push) at 18:00. The Obsidian timer only counts while Obsidian is running, so if you often close it, this task guarantees a daily commit. Without a remote it commits locally only.
- **Auto-capture hook**: while you use Claude Code in *other projects*, general knowledge it finds is written into your vault. It has privacy implications; read the [FAQ](FAQ.md) first.

## 6. Another computer

Repeat step 0, then `git clone` **your own** vault repo (not the template) and run `scripts\setup-new-machine.ps1` inside it. The repo carries `CLAUDE.md`, `.claude/` (rules and skills), the scripts and the Obsidian Git plugin; what each computer needs again is the git identity, the index hook, the hook in `~/.claude`, and the scheduled task — the script handles all of these.

## Verify

```powershell
cd D:\my-vault
python scripts\new_note.py ProjectA note "first test"
python scripts\lint.py
git log --oneline
```

`new_note.py` creates a dated note in `projects/ProjectA/`, `lint.py` should report 0 errors, and `git log` shows the first commit.

## macOS / Linux

- `scripts/*.py`, `scripts/githooks/pre-commit` and the Obsidian config are cross-platform.
- `install.ps1`, `bootstrap.ps1` and `sync.ps1` need PowerShell 7 (`pwsh`); or do it by hand: copy `vault-template/` → `git init -b main` → `git config core.hooksPath scripts/githooks` → `python3 scripts/build_index.py` → `git add -A && git commit`.
- The hook needs the executable bit: `chmod +x scripts/githooks/pre-commit`.
- Use cron/launchd instead of a scheduled task.

## Uninstall

Delete the vault folder. If you installed the auto-capture hook, first run `python <vault>\_meta\user-level\install_user_level.py --uninstall`.
