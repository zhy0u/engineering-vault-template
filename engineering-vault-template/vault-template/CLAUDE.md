# engineering-vault 约定

这是用户的个人工程知识库：既是 Obsidian vault，也是 git 仓库。你（Claude）在这里的工作是帮用户记录、整理、检索，不是改写用户的内容。开始任何操作前先读完本文件。

## 目录

```
inbox/               随手记，不知道放哪就放这里，每周整理一次
projects/<项目>/     每个项目一个文件夹（ProjectA、ProjectB …），里面可以自由建子文件夹
knowledge/<主题>/    通用、可复用的知识，包括 Claude 查出来的结论（embedded、electronics、c、docker、git、ai …）
_templates/          Obsidian 模板
_attachments/        图片等附件
scripts/             build_index.py、lint.py、new_note.py、sync.ps1、githooks/
_local/              不入库（.gitignore），放敏感或保密内容（公司、客户资料等）
Index.md             自动生成，总索引
projects/*/_index.md、knowledge/_index.md   自动生成，禁止手改
```

主题文件夹按需创建，用小写英文。项目内用 frontmatter 的 `type` 区分 note / debug / decision。

## 自由书写，事后整理

用户可以直接在 `projects/<项目>/`（含子文件夹）或 `inbox/` 里新建、修改任何 md 文件，不要求格式，也不用跑任何命令。

- 没有 frontmatter、没有日期文件名的笔记同样会被收录进索引，状态列显示“未规整”。lint 只把它们当警告，不是错误。
- 索引由 `python scripts/build_index.py` 生成。仓库的 pre-commit 钩子（`scripts/githooks/pre-commit`，需要执行过一次 `git config core.hooksPath scripts/githooks`）会在每次提交时自动刷新；你在会话里做检索、总结、整理之前，也先运行一次，保证索引反映磁盘上的实际文件。
- 没有任何后台进程会在用户不操作时修改笔记。整理只发生在用户明确要求（或会话里你被要求处理）的时候。

### 整理某个项目（用户说“整理 ProjectA”“规整一下”）

1. `git status` 确认工作区；运行 `python scripts/lint.py`，列出未规整的笔记和原因。
2. 逐篇读完。每批最多 20 篇，给出提案表：`原文件 | 建议文件名 | 建议 type | 建议 title 和 summary | tags | 建议的 [[链接]] | 疑似重复于 | 动作（默认 accept）`。
   - 建议文件名：`YYYY-MM-DD-主题.md`。日期优先取笔记正文里写明的日期，其次取 `git log --diff-filter=A --format=%as -- <文件>` 的首次入库日期。
   - `project` 必须与所在项目文件夹一致。
3. **等用户确认**，用户可对每行说 accept / modify / merge / skip。没有确认不动任何文件。
4. 对确认的条目：用 `git mv` 重命名；只在文件顶部补 frontmatter，正文不改写；你补写的 summary、tags 等设 `ai_generated: true`、`reviewed: false`；链接只追加到“相关”小节。
5. 运行 `python scripts/build_index.py` 和 `python scripts/lint.py`，按同步规则提交，汇报处理了几篇、跳过几篇。

整理 `inbox/` 用 `triage-inbox` 技能。

## 命名（规整后的笔记）

- 文件名：`YYYY-MM-DD-主题.md`，日期是首次记录的日期，之后不改。
- 主题用小写英文 kebab-case 或中文，不含空格和 `\ / : * ? " < > |`。
- 全库文件名必须唯一，wikilink 一律只写文件名：`[[2026-10-05-st25dv-gpo-debug]]`，需要显示名时用 `[[文件名|显示名]]`。
- 以 `_` 开头的文件是生成物或系统文件，不当作笔记。

## Frontmatter（规整后的笔记）

```yaml
---
title: ST25DV GPO 不触发
type: debug              # note | debug | decision | knowledge
project: ProjectA             # projects/ 下必填，与所在文件夹一致；knowledge 可选
summary: 一句话要点，供索引和检索使用
status: solved           # 可选：draft | active | solved | accepted | superseded
tags: [nfc, embedded]
created: 2026-10-05      # 首次记录日期，不改
updated: 2026-10-05      # 每次修改内容时更新
source: self             # self | claude；knowledge 必填
ai_generated: false      # Claude 写的内容为 true
reviewed: true           # ai_generated 为 true 时初始为 false，用户确认后改 true
---
```

## 项目笔记与知识的区别

- 项目笔记记录“这个项目里发生了什么”：现象、排查过程、决策、当时的上下文。
- knowledge 记录“以后任何项目都用得上的事实”：原理、规则、坑、命令。
- 在 debug 里得出可复用的结论时，另写（或追加到已有的）一篇 knowledge，两边互相 `[[链接]]`。
- 只靠用户自己测试、没有外部来源佐证的结论，用提示块标出：`> [!warning] 仅经本人测试，未经外部来源验证`。

## 追踪时间

- `created` 不改；改动内容时更新 `updated`。
- 重要修改在笔记末尾的“更新记录”追加一行：`- 2026-10-12 补充了示波器截图结论`。
- 时间以 git 历史为准：`git log --follow <文件>` 能看到一篇笔记的全部演变。

## 保存 Claude 查出来的知识

用户说“记到笔记”“存一下”时，用 `save-knowledge` 技能：

- 只存结论、步骤、关键原因和来源链接，不存聊天原文。
- 写入 `knowledge/<主题>/`，`source: claude`，`ai_generated: true`，`reviewed: false`。
- 先搜索是否已有相关笔记，有就追加并更新 `updated`，不要新建重复的。
- 与某个项目相关时，在正文和对应项目笔记里互相链接。
- 在 vault 里的会话按用户要求记录。在其他项目的会话里，如果用户安装了用户级钩子（见 `_meta/user-level/README.md`），Claude 会在每轮结束前自动检查并记录通用知识；那样写入的笔记同样是 `ai_generated: true`、`reviewed: false`，等用户审阅。

## 检索与总结

- 先运行 `python scripts/build_index.py`，读 `Index.md` 和相关 `_index.md`，用 `summary` 缩小范围，再读正文。未规整的笔记没有 summary，要直接读正文。
- 总结某段时间的进展：读该项目的 `_index.md`，加 `git log --since=<日期> -- projects/<项目>`，再读涉及的笔记，不要凭印象写。
- 总结结果默认只在对话里给出；用户要求保存时，才写成一篇 note。

## 硬规则

1. 永远不要删除笔记或附件。需要清理时，列出清单交给用户。
2. 不要覆盖已有笔记的内容。修改已有笔记时只做局部编辑或追加，保留原有信息。
3. 移动或重命名只用 `git mv`，并且先把计划（原路径 → 新路径）给用户确认。
4. 发现重复或高度相似的笔记：报告并提议合并方案，等用户批准，不要自己合并。
5. 不确定归属就放 `inbox/`，不要猜。
6. 不要手改自动生成的索引文件；改完笔记后重新运行脚本。
7. 不要把密码、token、内网地址、客户信息写进笔记。发现用户笔记里有这类内容时提醒他，并建议移到 `_local/`。
8. 不要 `git push --force`、`git reset --hard`、`git clean`。

## 同步规则

Obsidian Git 插件会每 30 分钟自动提交并推送，所以你动手前先 `git status`，不要覆盖用户未提交的修改。

你改完笔记后：

1. `python scripts/build_index.py`，然后 `python scripts/lint.py`；有错误先修（未规整只是警告）。
2. `git add` 具体的文件，不要 `git add -A`。
3. 提交信息格式：`vault: <动作> <对象>`，例如 `vault: add debug note st25dv-gpo`。
4. 有 `origin` 就 `git push`；push 失败时如实告诉用户，不要强推。没有 `origin` 就只在本地提交。
