# 安装

目标：在你自己的电脑上得到一个独立的笔记库（Obsidian + git），可选地备份到你自己的私有 GitHub 仓库，并让 Claude Code 能在里面整理笔记。

下面以 Windows 为例；macOS / Linux 的差别见最后一节。

## 0. 准备

| 软件 | 用途 | 安装 |
|---|---|---|
| Git | 记录历史 | `winget install Git.Git` |
| Python 3 | 生成索引、检查格式 | `winget install Python.Python.3.12` |
| Obsidian | 写笔记 | `winget install Obsidian.Obsidian` |
| Claude Code | 让 Claude 整理、检索（可选，需要 Claude 账号） | `winget install Anthropic.ClaudeCode` |
| GitHub CLI | 一条命令建云端仓库（可选） | `winget install GitHub.cli` |

装完**关掉终端重新打开**，让 PATH 生效。用 `git --version`、`python --version` 检查。

设置 git 身份（用你自己的，不要用公司邮箱）：

```powershell
git config --global user.name "你的名字"
git config --global user.email "你的个人邮箱"
```

## 1. 获取模板

```powershell
git clone https://github.com/<发给你的人>/engineering-vault-template.git
cd engineering-vault-template
```

## 2. 安装你自己的笔记库

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1 -Path D:\my-vault
```

想要英文笔记库，加 `-Lang en`（规则、技能、模板、索引、脚本提示都是英文），选择会记录在笔记库的 `.vault-lang` 文件里。

它会：把 `vault-template/` 复制到 `D:\my-vault`（目标非空会直接停止，不覆盖）→ `git init` → 设置索引钩子 → 生成第一份索引 → 做第一次提交。

要同时建云端私有仓库：

```powershell
gh auth login
powershell -ExecutionPolicy Bypass -File install.ps1 -Path D:\my-vault -Github
```

仓库名默认是 `<你的GitHub用户名>/engineering-vault`，私有。想换名字加 `-Repo 你/别的名字`。

> 模板文件夹 `engineering-vault-template` 只是安装来源，装完可以删掉；以后用的是 `D:\my-vault`。

## 3. 配置 Obsidian

1. 打开 Obsidian → “打开文件夹作为仓库” → 选 `D:\my-vault`。
2. 设置 → 第三方插件 → 关闭“安全模式”/开启社区插件，在已安装插件里启用 **Obsidian Git**（文件已在笔记库里，不用下载）。
3. 彻底退出再重开一次 Obsidian。自动提交间隔是 1440 分钟（一天一次），改动在 设置 → Git → Automatic。
4. 模板在 设置 → 核心插件 → 模板 里已指向 `_templates`。

## 4. 用 Claude Code 整理（可选）

```powershell
cd D:\my-vault
claude
```

第一次要登录并选择“信任此文件夹”。之后在里面直接说“整理 inbox”即可，见 [USAGE.md](USAGE.md)。

## 5. 可选的两个附加项

运行：

```powershell
powershell -ExecutionPolicy Bypass -File D:\my-vault\scripts\setup-new-machine.ps1
```

它会检查工具、确认索引钩子，并分别询问：

- **每日同步计划任务**：每天 18:00 运行 `scripts\sync.ps1`（提交、拉取、推送）。Obsidian 的定时器只在 Obsidian 运行时计时，如果你经常关掉它，这个任务能保证每天都有提交。没有远程仓库时只在本地提交。
- **自动记录钩子**：让你在*其他项目*里用 Claude Code 时，把查到的通用知识写进笔记库。有隐私影响，先读 [FAQ](FAQ.md)。

## 6. 换一台电脑

在新电脑上重复第 0 步，然后 `git clone` 你**自己的**笔记库仓库（不是模板），在里面运行 `scripts\setup-new-machine.ps1`。仓库自带的有：`CLAUDE.md`、`.claude/`（规则和技能）、脚本、Obsidian Git 插件；每台电脑要重做的有：git 身份、索引钩子、`~/.claude` 里的钩子、计划任务，这个脚本一步处理。

## 验证安装

```powershell
cd D:\my-vault
python scripts\new_note.py ProjectA note "第一篇测试"
python scripts\lint.py
git log --oneline
```

`new_note.py` 会在 `projects/ProjectA/` 生成一篇带日期的笔记，`lint.py` 应该显示 0 个错误，`git log` 能看到第一次提交。

## macOS / Linux

- `scripts/*.py`、`scripts/githooks/pre-commit`、Obsidian 配置都是跨平台的。
- `install.ps1`、`bootstrap.ps1`、`sync.ps1` 需要 PowerShell 7（`pwsh`）；或者手动：复制 `vault-template/` → `git init -b main` → `git config core.hooksPath scripts/githooks` → `python3 scripts/build_index.py` → `git add -A && git commit`。
- 提交钩子需要可执行权限：`chmod +x scripts/githooks/pre-commit`。
- 计划任务用 cron/launchd 代替。

## 卸载

删掉笔记库文件夹即可。如果装过自动记录钩子，先运行 `python <vault>\_meta\user-level\install_user_level.py --uninstall`。
