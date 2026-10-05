---
name: save-knowledge
description: 把刚才查出来的结论、步骤或原理存成 knowledge 笔记。当用户说“记到笔记”“存一下”“save this to notes”时使用。
---

# save-knowledge

把当前对话里值得长期保留的知识点，整理成一篇 `knowledge/` 笔记。

## 步骤

1. 确定要存什么：只存结论、关键原因、步骤、命令和来源链接，不存聊天原文，不存过程中的试错。
2. 确定主题文件夹 `knowledge/<主题>/`，主题用小写英文（embedded、electronics、c、docker、git、ai …），已有的文件夹优先复用。
3. 先搜索：`Grep` 关键词，`Glob` 看 `knowledge/` 和相关项目。
   - 已有相关笔记：追加内容，更新 `updated`，在“更新记录”加一行，不新建重复笔记，不改写原有内容。
   - 没有：用 `python scripts/new_note.py knowledge/<主题> knowledge "<标题>"` 创建，再编辑内容。
4. 填写 frontmatter：`summary` 一句话；`source: claude`；`ai_generated: true`；`reviewed: false`；`project:` 如果与某个项目相关就填项目名；`tags`。
5. 正文保持“要点 / 内容 / 来源 / 相关”结构。结论没有外部来源时，保留 `> [!warning] 仅经本人测试，未经外部来源验证` 提示块。
6. 关联：用 `[[文件名]]` 链接到相关项目笔记；并在那篇项目笔记的“相关”小节追加反向链接（只追加，不改其他内容）。
7. 收尾：运行 `python scripts/build_index.py` 和 `python scripts/lint.py`，按 CLAUDE.md 的同步规则提交并推送。
8. 回复用户：说明存到了哪里（文件名），并提醒这是 AI 生成、尚未审阅的内容。

## 不要做

- 不要存密码、token、内网地址。
- 不要为了“整洁”改动用户已有的笔记。
