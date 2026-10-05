# 日常使用

## 目录

```
inbox/               随手记，不知道放哪就放这里
projects/<项目>/     每个项目一个文件夹，里面可以自由建子文件夹
knowledge/<主题>/    通用、可复用的知识（含 Claude 查出来的结论）
_templates/          笔记模板
_attachments/        图片等附件
_local/              不入库，放敏感或保密内容（自己建）
Index.md             总索引（自动生成，不要手改）
```

## 写笔记：三种方式，任选

1. **直接写**：在 `projects/<项目>/` 里新建 `.md`，想写什么写什么，格式不用管。会进索引，状态显示“未规整”。
2. **用模板**：Obsidian 里 `Ctrl+P` → “插入模板”，或命令行：
   ```powershell
   python scripts\new_note.py ProjectA debug "标题"
   python scripts\new_note.py knowledge/git knowledge "标题" --slug rebase-basics
   ```
   类型有 `note`、`debug`（问题排查）、`decision`（决策）、`knowledge`（通用知识）。
3. **丢进 inbox**：之后让 Claude 整理。

笔记文件名约定 `YYYY-MM-DD-主题.md`，笔记之间用 `[[文件名]]` 链接。顶部的属性（title、type、project、summary、created、updated …）规整之后才有，Claude 整理时帮你补。

## 让 Claude 帮忙（在笔记库文件夹里运行 `claude`）

| 你说 | 它做什么 |
|---|---|
| 整理 inbox | 逐篇读 inbox，给你一张方案表（放哪、叫什么、摘要、相关笔记、疑似重复），你对每行回复接受/修改/合并/跳过，确认后才移动和补属性 |
| 整理 ProjectA（任一项目名） | 找出该项目里“未规整”的笔记，给出建议文件名和属性，确认后只在顶部补属性，**正文不改** |
| 总结 ProjectA 最近两周 | 读该项目索引和 git 历史，再读相关笔记，在对话里给你重点 |
| 记到笔记 / 存一下 | 把刚才的结论整理成 `knowledge/<主题>/` 的笔记；已有相关笔记就追加，不重复新建 |

所有整理都**先给方案，你确认才动手**。不会删除、不会覆盖已有内容、移动前给出“原路径 → 新路径”。AI 写的笔记标记 `ai_generated: true`、`reviewed: false`，你看过之后改成 `true`。

## 索引与检查

索引每次提交时自动刷新；手动：

```powershell
python scripts\build_index.py     # 重新生成 Index.md 和各 _index.md
python scripts\lint.py            # 检查：未规整、断链只是警告
python scripts\lint.py --strict   # 严格模式：警告也算错误
```

错误只有三种：文件名重复、type 不合法、`project` 与所在文件夹不一致。

## 提交与同步

- Obsidian Git 每天自动提交一次（你也可以 `Ctrl+P` → “Git: Commit-and-sync” 随时手动提交）。
- 提交会自动把最新索引一起提交。
- 提交信息格式：`vault: <动作> <对象>`。

## 追踪“这篇是什么时候记的”

- 文件名里的日期 = 创建日。
- 属性里的 `created` / `updated`。
- `git log -- <文件路径>` 看每一次修改。

## 保密

公司或客户的保密内容放 `_local/`，已经被 `.gitignore` 排除，不会进仓库。别把密码和 token 写进笔记。
