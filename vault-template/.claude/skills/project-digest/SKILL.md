---
name: project-digest
description: 总结某个项目最近一段时间的进展，或按主题给出重点和索引。用户说“总结 ProjectA 最近两周”“ST25 相关的坑有哪些”时使用。
---

# project-digest

## 按时间总结项目进展

1. 读 `projects/<项目>/_index.md`，圈出时间范围内的笔记。
2. 运行 `git log --since=<日期> --name-status -- projects/<项目>`，看哪些笔记新增、哪些被修改（修改日期比 `created` 更能反映进展）。
3. 读相关笔记的正文，不要只看 summary。
4. 输出：
   - 本期完成/解决了什么（debug 的根因和解决、decision 的结论）
   - 仍未解决的问题（status 不是 solved/accepted 的）
   - 新增的决策
   - 值得沉淀成 knowledge 但还没有沉淀的内容
   - 每条结论后面附 `[[笔记文件名]]`，方便点进去

## 按主题找重点

1. 先 Grep 主题关键词（器件型号、协议名等），范围包括 `projects/` 和 `knowledge/`。
2. 用 frontmatter 的 `type`、`status`、`tags` 筛选，按 `created` 排序。
3. 先给一个按时间排序的清单（日期、笔记、要点），再给 3–5 条最重要的经验。

## 规则

- 只依据笔记和 git 历史回答，笔记里没有的就说没有，不要凭印象补充。
- 默认只在对话里回答；用户要求保存时，再用 `new_note.py` 写成一篇 note。
