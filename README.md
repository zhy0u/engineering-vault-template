# engineering-vault-template

[English](README.en.md) · 中文

一套**按项目整理个人笔记**的模板：用 [Obsidian](https://obsidian.md) 写，用 git 记录每篇笔记什么时候写的，用 [Claude Code](https://claude.com/claude-code) 在你需要时帮你整理、检索、总结。装好之后是你自己的一个私有 git 仓库，数据只在你自己手里。

## 它解决什么问题

笔记散落在各个文件夹，给不同项目写的东西混在一起，过一阵就找不到、也说不清是什么时候记的。这个模板把它收拢成：

- **按项目分类**：每个项目一个文件夹 `projects/<项目>/`，里面想怎么建子文件夹都行。
- **随手写，事后整理**：不用每次先敲命令建文件。直接写在项目文件夹里，之后让 Claude 提出整理方案，你确认了才动手。
- **能追踪时间**：文件名带日期，笔记顶部有创建/更新日期，git 记录每一次修改。
- **要重点时有索引**：自动生成总索引和每个项目的索引（一行一篇：日期、类型、要点），可以让 Claude 据此给你“某项目最近两周的进展”。
- **查来的知识能存下来**：通用知识放 `knowledge/<主题>/`，可以让 Claude 把刚查出来的结论整理成笔记存进去。
- **自动备份**：Obsidian Git 插件每天提交一次；可选的计划任务保证 Obsidian 没开也会同步。

## 它由什么组成

| 部分 | 作用 |
|---|---|
| `vault-template/` | 笔记库本体：目录结构、笔记模板、`CLAUDE.md` 约定、3 个 Claude 技能、索引/检查脚本、Obsidian 配置 |
| `vault-template-en/` | 英文覆盖层：替换规则、技能、模板和用户级钩子文本，并把脚本提示切成英文（`install.ps1 -Lang en` 时使用） |
| `install.ps1` | 把 `vault-template/` 复制到你选的位置，初始化 git，（可选）建一个私有 GitHub 仓库；`-Lang en` 装英文版 |
| `docs/`（英文在 `docs/en/`，见 [README.en.md](README.en.md)） | [安装](docs/INSTALL.md) · [日常使用](docs/USAGE.md) · [工作原理](docs/HOW-IT-WORKS.md) · [常见问题](docs/FAQ.md) |

## 三分钟安装（Windows）

先装好 git、Python、Obsidian，再（可选）装 Claude Code 和 GitHub CLI。

```powershell
winget install Git.Git
winget install Python.Python.3.12
winget install Obsidian.Obsidian
winget install Anthropic.ClaudeCode      # 想用 Claude 整理才需要
winget install GitHub.cli                # 想要云端备份才需要
```

装完**新开一个终端**，然后：

```powershell
git config --global user.name "你的名字"
git config --global user.email "你的个人邮箱"

git clone https://github.com/<发给你的人>/engineering-vault-template.git
cd engineering-vault-template
powershell -ExecutionPolicy Bypass -File install.ps1 -Path D:\my-vault
```

想要英文笔记库（规则、技能、模板、索引、脚本提示都是英文），在最后一条命令后加 `-Lang en`。

想同时建一个私有 GitHub 仓库备份，先 `gh auth login`，然后在最后一条命令后加 `-Github`。

然后在 Obsidian 里“打开文件夹作为仓库”，选 `D:\my-vault`，开启社区插件并启用 Obsidian Git。完整步骤和每一步的作用见 [docs/INSTALL.md](docs/INSTALL.md)。

## 怎么用（最短版）

- 随手记：放进 `inbox/`，或直接写在 `projects/<项目>/` 里，格式随意。
- 想整理：在笔记库文件夹里运行 `claude`，说“整理 inbox”或“整理 <项目名>”。
- 想看重点：说“总结 <项目名> 最近两周”。
- 想存知识：说“把刚才的结论记到笔记”。

详见 [docs/USAGE.md](docs/USAGE.md)。

## 重要提醒

- Claude 的整理一律先给方案、等你确认；规则写在 `vault-template/CLAUDE.md`，里面有硬规则：不删除、不覆盖、不强推。
- 笔记库是**你自己的私有仓库**。密码、token、公司保密内容不要写进笔记，放 `_local/`（不入库）。
- 可选的“自动记录知识点”钩子会让其他项目里的 Claude Code 会话把通用知识写进你的笔记库，装之前先读 [docs/FAQ.md](docs/FAQ.md) 的隐私一节，并确认你所在公司允许。
- 本模板由作者在 Linux 环境测过 Python 脚本和钩子；PowerShell 脚本和 Windows 上的钩子行为作者自己也只在一台 Windows 电脑上用过，遇到问题请到 Issues 反馈。

## 许可

MIT，见 [LICENSE](LICENSE)。`vault-template/.obsidian/plugins/obsidian-git/` 里是 [Obsidian Git](https://github.com/Vinzent03/obsidian-git) 插件（MIT）的发布文件，版权归其作者。
