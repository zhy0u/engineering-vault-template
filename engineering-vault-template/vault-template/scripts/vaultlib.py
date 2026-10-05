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
        reasons.append("缺少 frontmatter")
    else:
        missing = [k for k in REQUIRED_KEYS if not meta.get(k)]
        if missing:
            reasons.append("缺少 " + "、".join(missing))
        if top == "projects" and not meta.get("project"):
            reasons.append("缺少 project")
        if top == "knowledge" and not meta.get("source"):
            reasons.append("缺少 source")
    if not NAME_RE.match(Path(path).name):
        reasons.append("文件名不是 YYYY-MM-DD-主题.md")
    return reasons
