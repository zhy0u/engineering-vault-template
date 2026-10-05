"""Shared helpers for the vault scripts. Standard library only."""
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ["inbox", "projects", "knowledge"]
FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.S)
DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")
NAME_RE = re.compile(r'^\d{4}-\d{2}-\d{2}-[^\s\\/:*?"<>|]+\.md$')
REQUIRED_KEYS = ("title", "type", "summary", "created", "updated")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)

MSG = {
    "zh": {
        "untidy_label": "未规整",
        "ai_unreviewed": "AI未审",
        "untyped": "未分类",
        "uncategorised": "(未分类)",
        "sep": "、",
        "r_no_fm": "缺少 frontmatter",
        "r_missing": "缺少 {keys}",
        "r_no_project": "缺少 project",
        "r_no_source": "缺少 source",
        "r_bad_name": "文件名不是 YYYY-MM-DD-主题.md",
        "gen_header": "<!-- 自动生成，请勿手改；运行 python scripts/build_index.py 重新生成 -->",
        "idx_title": "{name} 索引",
        "idx_summary": "共 {n} 篇（{u} 篇未规整），{types}。按记录日期倒序，子文件夹里的笔记也会收录。",
        "types_sep": "，",
        "idx_head": "| 日期 | 类型 | 笔记 | 状态 | 要点 |",
        "know_title": "knowledge 索引",
        "know_summary": "共 {n} 篇。按主题分组，组内按记录日期倒序。",
        "know_head": "| 日期 | 笔记 | 来源 | 项目 | 状态 | 要点 |",
        "all_title": "总索引",
        "all_inbox": "## Inbox\n\n待整理 {n} 篇。",
        "all_projects": "## 项目",
        "all_head": "| 项目 | 笔记数 | 未规整 | 最近记录 |",
        "all_know": "## 知识\n\n[[knowledge/_index\\|knowledge 索引]]，共 {n} 篇（{u} 篇未规整）。",
        "built": "已生成索引：{p} 个项目，{k} 篇知识，inbox {i} 篇",
        "lint_dup": "文件名重复（wikilink 会歧义）：{stem} -> {paths}",
        "lint_stale": "{r}: 在 inbox 里已 {age} 天，可以让 Claude 整理",
        "lint_untidy": "{r}: 未规整（{why}）",
        "lint_type": "{r}: type 必须是 {valid} 之一，现为 {got}",
        "lint_proj": "{r}: project={p} 与所在文件夹 {f} 不一致",
        "lint_ai": "{r}: AI 生成且尚未审阅",
        "lint_broken": "{r}: 断链 [[{target}]]",
        "lint_attach": "{r}: 附件不存在 [[{target}]]",
        "lint_warn": "警告  ",
        "lint_err": "错误  ",
        "lint_summary": "检查了 {n} 篇笔记：{e} 个错误，{u} 篇未规整，{b} 个断链，{w} 个其他提醒",
        "lint_hint": "提示：未规整的笔记不影响使用，需要时对 Claude 说“整理 <项目名>”即可。",
        "lint_strict_help": "未规整的笔记和断链也算错误",
        "nn_target": "项目名，或 knowledge/<主题>",
        "nn_slug": "文件名里的主题部分，默认由标题生成",
        "nn_exists": "已存在，不覆盖：{path}",
    },
    "en": {
        "untidy_label": "untidy",
        "ai_unreviewed": "AI-unreviewed",
        "untyped": "untyped",
        "uncategorised": "(uncategorised)",
        "sep": ", ",
        "r_no_fm": "no frontmatter",
        "r_missing": "missing {keys}",
        "r_no_project": "missing project",
        "r_no_source": "missing source",
        "r_bad_name": "file name is not YYYY-MM-DD-topic.md",
        "gen_header": "<!-- Generated, do not edit by hand; run python scripts/build_index.py to regenerate -->",
        "idx_title": "{name} index",
        "idx_summary": "{n} notes ({u} untidy); {types}. Newest first; notes in sub-folders are included.",
        "types_sep": ", ",
        "idx_head": "| Date | Type | Note | Status | Key point |",
        "know_title": "knowledge index",
        "know_summary": "{n} notes. Grouped by topic, newest first within each group.",
        "know_head": "| Date | Note | Source | Project | Status | Key point |",
        "all_title": "Overall index",
        "all_inbox": "## Inbox\n\n{n} waiting to be tidied.",
        "all_projects": "## Projects",
        "all_head": "| Project | Notes | Untidy | Latest |",
        "all_know": "## Knowledge\n\n[[knowledge/_index\\|knowledge index]], {n} notes ({u} untidy).",
        "built": "Index built: {p} projects, {k} knowledge notes, {i} in inbox",
        "lint_dup": "Duplicate file name (wikilinks would be ambiguous): {stem} -> {paths}",
        "lint_stale": "{r}: in inbox for {age} days; ask Claude to tidy it",
        "lint_untidy": "{r}: untidy ({why})",
        "lint_type": "{r}: type must be one of {valid}, got {got}",
        "lint_proj": "{r}: project={p} does not match its folder {f}",
        "lint_ai": "{r}: AI-generated and not yet reviewed",
        "lint_broken": "{r}: broken link [[{target}]]",
        "lint_attach": "{r}: attachment not found [[{target}]]",
        "lint_warn": "warning  ",
        "lint_err": "error    ",
        "lint_summary": "Checked {n} notes: {e} errors, {u} untidy, {b} broken links, {w} other notices",
        "lint_hint": "Note: untidy notes are fine to keep; ask Claude to \"tidy <project name>\" when you want them organised.",
        "lint_strict_help": "untidy notes and broken links count as errors",
        "nn_target": "project name, or knowledge/<topic>",
        "nn_slug": "topic part of the file name; default is generated from the title",
        "nn_exists": "Already exists, not overwriting: {path}",
    },
}


def _read_lang():
    try:
        v = (ROOT / ".vault-lang").read_text(encoding="utf-8").strip().lower()
    except OSError:
        return "zh"
    return v if v in MSG else "zh"


LANG = _read_lang()


def t(key, **kw):
    """Message in the vault language (.vault-lang: zh or en; default zh)."""
    return MSG[LANG][key].format(**kw)



def utf8_stdout():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def parse_frontmatter(text):
    """Parse the simple YAML subset used by this vault. Returns (meta, body)."""
    m = FM_RE.match(text)
    if not m:
        return {}, text
    meta = {}
    key = None
    for raw in m.group(1).splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("-") and key is not None:
            if not isinstance(meta.get(key), list):
                meta[key] = [] if meta.get(key) in ("", None) else [meta[key]]
            meta[key].append(stripped[1:].strip().strip("\"'"))
            continue
        if ":" in raw and not raw.startswith((" ", "\t")):
            k, v = raw.split(":", 1)
            key = k.strip()
            v = v.strip()
            # drop trailing comments such as "solved   # note"
            if " #" in v and not v.startswith(('"', "'")):
                v = v.split(" #", 1)[0].strip()
            if v.startswith("[") and v.endswith("]"):
                meta[key] = [x.strip().strip("\"'") for x in v[1:-1].split(",") if x.strip()]
            else:
                meta[key] = v.strip("\"'")
    return meta, text[m.end():]


def read_note(path):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    meta, body = parse_frontmatter(text)
    return meta, body


def note_files(subdirs=None):
    """All note files (recursive) under the scanned folders; files starting with '_' are generated or system files."""
    files = []
    for d in subdirs or SCAN_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        for p in sorted(base.rglob("*.md")):
            if p.name.startswith("_"):
                continue
            files.append(p)
    return files


def truthy(value):
    return str(value).strip().lower() in ("true", "yes", "1")


def created_date(path, meta):
    """created from frontmatter, else the date prefix of the filename, else the mtime."""
    c = str(meta.get("created", ""))[:10]
    if re.match(r"^\d{4}-\d{2}-\d{2}$", c):
        return c
    m = DATE_PREFIX_RE.match(Path(path).name)
    if m:
        return m.group(1)
    return datetime.date.fromtimestamp(Path(path).stat().st_mtime).isoformat()


def rel(path):
    return Path(path).relative_to(ROOT).as_posix()


def display_title(path, meta, body):
    """frontmatter title, else the first H1, else the file name."""
    if meta.get("title"):
        return str(meta["title"])
    m = H1_RE.search(body)
    return m.group(1) if m else Path(path).stem


def untidy_reasons(path, meta):
    """Why a note is not yet 'tidy'. Empty list = tidy. inbox notes are never untidy (free-form by design)."""
    parts = rel(path).split("/")
    top = parts[0]
    if top == "inbox":
        return []
    reasons = []
    if not meta:
        reasons.append(t("r_no_fm"))
    else:
        missing = [k for k in REQUIRED_KEYS if not meta.get(k)]
        if missing:
            reasons.append(t("r_missing", keys=t("sep").join(missing)))
        if top == "projects" and not meta.get("project"):
            reasons.append(t("r_no_project"))
        if top == "knowledge" and not meta.get("source"):
            reasons.append(t("r_no_source"))
    if not NAME_RE.match(Path(path).name):
        reasons.append(t("r_bad_name"))
    return reasons
