# 用户级自动记录（可选）

在你**其他项目**的 Claude Code 会话里，每轮结束前自动检查一次：这一轮有没有产生值得记进 engineering-vault 的通用知识。有就写进 `knowledge/`，没有就静默结束。做法参考 zhfans/dotagents 的 Stop 钩子，但不依赖 `jq`。

这一套改动的是 `~/.claude/`（用户级，对所有项目生效），所以不放在 vault 的 `.claude/` 里，也不会自动安装，需要你自己运行安装脚本。

## 它由三部分组成

| 部分 | 作用 |
|---|---|
| `~/.claude/CLAUDE.md` 里一个标记小节 | 告诉 Claude 知识库在哪、记什么、不记什么、怎么写、怎么提交 |
| `~/.claude/hooks/vault-checkpoint.sh`（Stop 钩子） | 每轮结束前提醒 Claude 做一次检查；没有值得记的就静默结束 |
| `settings.json` 里的 `additionalDirectories` | 让其他项目的会话能读写知识库目录（写入仍然会弹出授权提示） |

## 安装

```
python <你的vault路径>\_meta\user-level\install_user_level.py
```

脚本会先列出要改的内容并询问，确认后才动手。只在文件内容真的变化时才备份（`<文件名>.bak-<时间>`），其余内容原样保留；`settings.json` 如果不是有效 JSON，脚本会直接中止、不改任何东西。已打开的 Claude Code 会话需要重启才生效。

想先看看会做什么，加 `--dry-run`。

## 关闭、卸载

- 临时关闭：创建空文件 `%USERPROFILE%\.claude\vault-checkpoint.off`，删掉它就恢复。
- 卸载：`python <你的vault路径>\_meta\user-level\install_user_level.py --uninstall`，会移除这个小节、这条钩子、知识库目录授权和钩子文件，其他内容不动。

## 它不会做什么，以及代价

- 在 vault 里启动的会话不会触发（那里本来就是整理笔记）。
- 钩子只是提醒，不是强制：Claude 可能判断“没有”而什么都不记，这是预期的。
- **每一轮多一次往返**，包括没什么可记的轮次，会增加一点用量和延迟。觉得烦就用上面的开关关掉。
- 从其他项目写入知识库、提交、推送，仍会按你的权限模式弹出授权提示，你可以逐次批准。
- 钩子由 Git Bash 执行（Windows 上 Claude Code 的默认方式）。如果你把 Claude Code 的 shell 改成了 PowerShell，这条钩子会报错，需要关掉或改写。

## 隐私

自动记录意味着你在其他项目（包括公司项目）里查到的知识，可能被写进你自己 GitHub 的私有仓库。`CLAUDE.snippet.md` 里已经要求 Claude：只记通用结论、记之前先去掉项目/客户/公司背景、不记任何密钥和内部地址、拿不准就不记。AI 写的笔记默认 `reviewed: false`，你可以定期在知识库里审阅，发现不该出现的内容就删掉并告诉我调整规则。公司项目是否允许这样做，仍需要你自己确认。
