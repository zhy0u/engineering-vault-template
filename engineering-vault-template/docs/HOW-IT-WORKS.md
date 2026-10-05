# 工作原理

## 整体

```
你在 Obsidian 里写 ──> 文件在 projects/ inbox/ knowledge/
                               │
              git commit（Obsidian Git 每天一次 / 手动 / 计划任务）
                               │
          pre-commit 钩子：scripts/build_index.py 重新生成 Index.md、各 _index.md
                               │
                         （可选）push 到你的私有 GitHub 仓库

你在笔记库里运行 claude ──> 读 CLAUDE.md 的约定 + .claude/skills 的 3 个技能 ──> 整理/总结/存知识
```

## 各部分

**`CLAUDE.md`**：给 Claude 的约定。只有在笔记库文件夹里启动的 Claude Code 才会读到。里面是目录含义、命名、属性格式、整理步骤、硬规则（不删除、不覆盖、移动要确认、不强推、不写密钥）。

**`.claude/skills/`**：3 个技能，Claude 在你说出对应的话时触发。
`triage-inbox`（整理 inbox）、`save-knowledge`（存知识）、`project-digest`（总结项目）。

**`.claude/settings.json`**：允许 Claude 运行本库脚本和常用 git 命令；明确禁止 `rm`、`del`、`git push --force`、`git reset --hard`、`git clean` 等。

**`scripts/`**
- `vaultlib.py`：读属性、遍历笔记的公共代码。
- `build_index.py`：生成索引。没有属性的笔记也会进索引，状态显示“未规整”。
- `lint.py`：检查格式。
- `new_note.py`：按模板建笔记。
- `bootstrap.ps1` / `setup-new-machine.ps1` / `sync.ps1`：初始化、新电脑设置、手动同步。
- `githooks/pre-commit`：提交前刷新索引；找不到 Python 或脚本出错时直接跳过，不会让提交失败。需要 `git config core.hooksPath scripts/githooks`（安装脚本已做）。这个设置存在 `.git/config`，**不随仓库同步**，所以每个克隆都要做一次。

**`.obsidian/`**：窗口状态、核心插件、模板目录、Obsidian Git 插件及其配置（自动提交间隔 1440 分钟）。

**`_meta/user-level/`**（可选）：自动记录知识点的用户级钩子，见 FAQ。

## “未规整”是什么

你可以不按格式写。没有属性或文件名没有日期的笔记，索引里记为“未规整”，lint 只给警告。等你想整理时让 Claude 提方案：它只在文件顶部补属性、给出建议文件名，正文不改。这样写的时候零负担，整理的时候有人把关。

## 数据放哪里

全部在你自己的电脑上；如果你选了 `-Github`，同步到你自己账号下的私有仓库。模板作者看不到你的内容。
