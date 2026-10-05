# 常见问题

**必须装 Claude Code 吗？**
不必须。Obsidian + git + Python 脚本已经能完成写笔记、版本记录、生成索引。Claude Code 只负责整理、总结和存知识这几件事，需要 Claude 账号。

**必须有 GitHub 吗？**
不必须，只在本地提交也行。云端备份建议用私有仓库。

**我随便写也行吗？**
行。没格式的笔记会进索引并标成“未规整”，只是警告。想整理时让 Claude 提方案。

**为什么提交后索引没更新？**
检查 `git config core.hooksPath` 是否是 `scripts/githooks`，没有就运行 `git config core.hooksPath scripts/githooks`。也要确认能运行 `python`。手动 `python scripts\build_index.py` 随时可用。

**自动提交怎么没触发？**
Obsidian Git 的计时器只在 Obsidian 运行时计，每次重启归零。一天一次的间隔如果你每天都会关掉 Obsidian，可能永远走不到。用 `scripts\setup-new-machine.ps1` 里的每日计划任务，或手动 `Ctrl+P` → “Git: Commit-and-sync”。

**Claude 在这个库里能做什么、不能做什么？**
能：读笔记、生成整理方案、你确认后补属性、移动文件（`git mv`）、提交、总结。
不能（规则 + 权限禁止）：删除文件、覆盖已有内容、强制推送、`git reset --hard`、`git clean`。不确定的会问你。

**我对话里问 Claude 的知识，会自动进笔记库吗？**
不会。只有两种情况：你在笔记库里的 Claude Code 会话里说“记到笔记”；或者你装了下面的自动记录钩子，并且在*其他项目*的 Claude Code 会话里。

## 自动记录钩子（可选）

在你其他项目的 Claude Code 会话里，每轮结束前提醒 Claude 检查一次：有没有值得记进笔记库的通用知识，有就写进 `knowledge/`，没有就静默结束。

```powershell
python <vault>\_meta\user-level\install_user_level.py --dry-run   # 先看会改什么
python <vault>\_meta\user-level\install_user_level.py             # 安装（会询问）
python <vault>\_meta\user-level\install_user_level.py --uninstall # 完全卸载
# 临时关闭：创建空文件 %USERPROFILE%\.claude\vault-checkpoint.off ，删掉即恢复
```

它改动三处（都在 `~/.claude/`）：`hooks/vault-checkpoint.sh`、`CLAUDE.md` 里一个带标记的小节、`settings.json` 里一条 Stop 钩子和笔记库目录授权。其余内容不动，内容变化时才备份成 `.bak-<时间>`；`settings.json` 不是有效 JSON 时直接中止。新开的会话才生效。

限制：钩子只是提醒，Claude 可能判断“没有”；每轮多一次往返，会增加一点用量；钩子由 Git Bash 执行（Windows 默认），Shell 设成 PowerShell 的话会报错，用开关关掉；写入、提交仍按你的权限模式弹出授权提示。

**隐私**：它意味着你在其他项目（包括公司项目）里查到的知识可能被写进你自己的私有仓库。规则要求 Claude 只记通用结论、去掉项目和公司背景、不记密钥和内部地址、拿不准就不记；AI 写的笔记默认 `reviewed: false`，请定期审阅。**公司项目是否允许这样做，需要你自己确认。**

**怎么更新模板？**
模板更新后，你的笔记库不会自动变。需要时对照 `vault-template/` 里的 `scripts/`、`.claude/`、`CLAUDE.md` 手动合并（不要覆盖你自己的 `CLAUDE.md` 修改）。

**提交里的邮箱是公司的怎么办？**
git 用的是全局身份。以后的提交：`git config --global user.email "你的个人邮箱"`（或不加 `--global` 只改当前仓库）；想让 git 不再自动猜，运行 `git config --global user.useConfigOnly true`。已经提交并推送的，改写历史：

```powershell
git config user.name "你的名字"
git config user.email "你的个人邮箱"
git log --format="%h %an <%ae> | %cn <%ce>"
git rebase -r --root --exec "git commit --amend --reset-author --no-edit"
git push --force-with-lease
```

所有提交的哈希会变，最好在别人 clone 之前做。旧提交在 GitHub 上可能还能通过旧哈希访问一段时间，介意的话联系 GitHub Support 清除。也可以在 GitHub → Settings → Emails 勾选“Keep my email addresses private”和“Block command line pushes that expose my email”。
