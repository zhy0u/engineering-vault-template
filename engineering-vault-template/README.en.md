# engineering-vault-template

English · [中文](README.md)

A template for **keeping personal notes organised by project**: write in [Obsidian](https://obsidian.md), let git record when each note was written, and let [Claude Code](https://claude.com/claude-code) tidy, search and summarise on demand. After installation it is your own private git repository; the data stays with you.

> **Language note:** the documentation is available in English and Chinese, but the vault template itself (`vault-template/`: the `CLAUDE.md` rules, the three Claude skills, note templates, and the messages printed by the Python scripts) is currently written in **Chinese**. Everything works the same way in either language, but you will see Chinese in the generated indexes (e.g. the status "未规整" = "not yet tidied") and in the rules Claude reads. If you want a fully English vault, open an issue or translate those files — they are small (about 1,000 lines in total).

## What problem it solves

Notes end up scattered across folders, mixed up between projects, and after a while you cannot find them or say when you wrote them. This template pulls them together:

- **Organised by project**: one folder per project, `projects/<project>/`, with any sub-folders you like.
- **Write first, tidy later**: no commands needed to create a file. Write straight into the project folder, then ask Claude to propose a tidy-up; it only acts after you confirm.
- **Time is traceable**: dates in file names, created/updated dates at the top of each note, and git history for every change.
- **Highlights on demand**: an auto-generated overall index and a per-project index (one line per note: date, type, key point), so Claude can answer "what happened in project X over the last two weeks".
- **Knowledge Claude looked up can be kept**: general knowledge lives in `knowledge/<topic>/`; ask Claude to turn a conclusion into a note.
- **Automatic backup**: the Obsidian Git plugin commits once a day; an optional scheduled task syncs even when Obsidian is closed.

## What is in it

| Part | Purpose |
|---|---|
| `vault-template/` | The vault itself: folder layout, note templates, `CLAUDE.md` rules, 3 Claude skills, index/lint scripts, Obsidian config |
| `install.ps1` | Copies `vault-template/` to a location you choose, runs `git init`, optionally creates a private GitHub repo |
| `docs/en/` | [Install](docs/en/INSTALL.md) · [Daily use](docs/en/USAGE.md) · [How it works](docs/en/HOW-IT-WORKS.md) · [FAQ](docs/en/FAQ.md) |

## Install in three minutes (Windows)

Install git, Python and Obsidian first, and optionally Claude Code and the GitHub CLI.

```powershell
winget install Git.Git
winget install Python.Python.3.12
winget install Obsidian.Obsidian
winget install Anthropic.ClaudeCode      # only if you want Claude to tidy notes
winget install GitHub.cli                # only if you want a cloud backup
```

**Open a new terminal** afterwards, then:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your-personal-email"

git clone https://github.com/<whoever-sent-you-this>/engineering-vault-template.git
cd engineering-vault-template
powershell -ExecutionPolicy Bypass -File install.ps1 -Path D:\my-vault
```

For a private GitHub backup repo, run `gh auth login` first and add `-Github` to the last command.

Then in Obsidian choose "Open folder as vault", pick `D:\my-vault`, turn on community plugins and enable Obsidian Git. Full steps, and what each one does, are in [docs/en/INSTALL.md](docs/en/INSTALL.md).

## Use it (shortest version)

- Jot things down: put them in `inbox/`, or write directly in `projects/<project>/`, in any format.
- To tidy up: run `claude` inside the vault folder and say "整理 inbox" or "整理 <project name>" (the trigger phrases are in Chinese, but Claude understands you describing the same thing in English, e.g. "tidy my inbox").
- To see highlights: "summarise <project> for the last two weeks".
- To keep knowledge: "save that conclusion to my notes".

See [docs/en/USAGE.md](docs/en/USAGE.md).

## Important

- Claude always proposes first and waits for your confirmation. The rules in `vault-template/CLAUDE.md` include hard limits: never delete, never overwrite, never force-push.
- The vault is **your own private repository**. Keep passwords, tokens and confidential employer material out of notes; put them in `_local/` (not committed).
- The optional "auto-capture" hook lets Claude Code sessions in other projects write general knowledge into your vault. Read the privacy section of [docs/en/FAQ.md](docs/en/FAQ.md) first and make sure your employer allows it.
- The author tested the Python scripts and the hook on Linux and has used the PowerShell scripts on a single Windows machine. Please report problems in Issues.

## License

MIT, see [LICENSE](LICENSE). `vault-template/.obsidian/plugins/obsidian-git/` contains release files of the [Obsidian Git](https://github.com/Vinzent03/obsidian-git) plugin (MIT); copyright remains with its authors.
