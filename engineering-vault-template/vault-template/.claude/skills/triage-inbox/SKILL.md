---
name: triage-inbox
description: 整理 inbox/ 里的随手记：给出归类提案，用户确认后再移动、补 frontmatter 和链接。用户说“整理 inbox”“triage”时使用。
---

# triage-inbox

## 步骤

1. 先 `git status`，确认没有未提交的用户修改被牵连。
2. 列出 `inbox/` 下所有笔记，逐篇读完。
3. 为每篇判断：
   - 类型：note / debug / decision / knowledge
   - 去向：`projects/<项目>/` 或 `knowledge/<主题>/`（不确定就留在 inbox，并说明缺什么信息）
   - 新文件名：`YYYY-MM-DD-主题.md`，日期取笔记里写明的日期，其次取文件的创建时间
   - summary（一句话）、tags
   - 相关的已有笔记（先 Grep 查），建议加的 `[[链接]]`
   - 是否与已有笔记重复（只报告，不合并）
   - 是否含密码、token、内网地址（有的话标红，建议移到 `_local/`）
4. 把提案以表格给用户：`原文件 | 类型 | 目标路径 | 标题 | summary | 相关笔记 | 重复于 | 动作`，动作默认 accept。每批最多 20 篇。
5. **等用户确认。** 用户可以对每行说 accept / modify / merge / skip。没有确认不要动任何文件。
6. 对确认的条目：
   - 用 `git mv` 移动并重命名
   - 补齐 frontmatter（`created` 取原始记录日期；你补写的 summary 等设 `ai_generated: true`、`reviewed: false`）
   - 正文原样保留，只在末尾“相关”小节追加链接
7. 运行 `python scripts/build_index.py` 和 `python scripts/lint.py`，修复错误。
8. 每批一次提交：`vault: triage inbox batch <序号>`，有 origin 则推送。
9. 汇报：处理了几篇、跳过了几篇、还剩几篇，以及需要用户决定的事项。

## 不要做

删除任何文件；自动合并重复笔记；改写正文；在没有确认时移动。
