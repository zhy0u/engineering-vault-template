#!/usr/bin/env python3
"""Install or remove the user-level "auto-save knowledge to the vault" setup in ~/.claude.

  python install_user_level.py              # show the plan, ask, then install
  python install_user_level.py --dry-run    # only show the plan
  python install_user_level.py --yes        # install without asking
  python install_user_level.py --uninstall  # remove everything this script added

What it changes (a file is backed up as <name>.bak-<timestamp> only when its content changes):
  ~/.claude/hooks/vault-checkpoint.sh   copied
  ~/.claude/CLAUDE.md                   one marked section appended or replaced
  ~/.claude/settings.json               a Stop hook and the vault in permissions.additionalDirectories added
Everything else in those files is left as it is.
"""
import argparse
import json
import re
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
VAULT = HERE.parent.parent
CLAUDE_DIR = Path.home() / ".claude"
HOOK_NAME = "vault-checkpoint.sh"
HOOK_CMD = f'bash "$HOME/.claude/hooks/{HOOK_NAME}"'
START = "<!-- engineering-vault:start -->"
END = "<!-- engineering-vault:end -->"
BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)


def _lang():
    try:
        v = (VAULT / ".vault-lang").read_text(encoding="utf-8").strip().lower()
    except OSError:
        return "zh"
    return v if v in ("zh", "en") else "zh"


LANG = _lang()


def tr(zh, en):
    return en if LANG == "en" else zh


def say(msg=""):
    print(msg)


def write_if_changed(path, data, keep_eol=False):
    """Write only when the content changes; back the old file up first. Returns True if written."""
    raw = data if isinstance(data, bytes) else data.encode("utf-8")
    if keep_eol and path.exists() and b"\r\n" in path.read_bytes():
        raw = raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")  # keep the file's CRLF style
    if path.exists():
        if path.read_bytes() == raw:
            say(tr(f"  无变化 {path}", f"  unchanged {path}"))
            return False
        dest = path.with_name(path.name + ".bak-" + time.strftime("%Y%m%d%H%M%S"))
        shutil.copy2(path, dest)
        say(tr(f"  已备份 {path.name} -> {dest.name}", f"  backed up {path.name} -> {dest.name}"))
    path.write_bytes(raw)
    say(tr(f"  已写入 {path}", f"  wrote {path}"))
    return True


def read_text(path):
    return path.read_bytes().decode("utf-8").replace("\r\n", "\n") if path.exists() else ""


def load_settings(path):
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        raise SystemExit(tr(f"{path} 不是有效的 JSON（{e}）。为避免弄坏它，脚本没有做任何修改，请先修好或移走它。", f"{path} is not valid JSON ({e}). To avoid breaking it, nothing was changed; fix or move it first."))
    if not isinstance(data, dict):
        raise SystemExit(tr(f"{path} 的顶层不是对象，脚本没有做任何修改。", f"The top level of {path} is not an object; nothing was changed."))
    return data


def dump_settings(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def has_hook(settings):
    for entry in settings.get("hooks", {}).get("Stop", []) or []:
        for h in entry.get("hooks", []) or []:
            if HOOK_NAME in str(h.get("command", "")):
                return True
    return False


def snippet_block():
    text = (HERE / "CLAUDE.snippet.md").read_text(encoding="utf-8").replace("{{VAULT}}", str(VAULT))
    return f"{START}\n{text.strip()}\n{END}\n"


def plan(uninstall):
    verb = tr("移除", "remove") if uninstall else tr("安装", "install")
    say(tr(f"将要{verb}（知识库：{VAULT}；用户配置目录：{CLAUDE_DIR}）：", f"About to {verb} (vault: {VAULT}; user config folder: {CLAUDE_DIR}):"))
    say(f"  - {CLAUDE_DIR / 'hooks' / HOOK_NAME}")
    say(tr(f"  - {CLAUDE_DIR / 'CLAUDE.md'} 里标记为 engineering-vault 的一个小节", f"  - the engineering-vault marked section in {CLAUDE_DIR / 'CLAUDE.md'}"))
    say(tr(f"  - {CLAUDE_DIR / 'settings.json'} 里的 Stop 钩子，以及 permissions.additionalDirectories 中的知识库路径", f"  - the Stop hook and the vault path in permissions.additionalDirectories in {CLAUDE_DIR / 'settings.json'}"))
    if not uninstall:
        say(tr("效果：在你的其他项目会话里，Claude 每轮结束前会检查一次有没有值得记进知识库的通用知识。", "Effect: in your other projects, Claude checks once before each turn ends whether there is general knowledge worth saving to the vault."))
        say(tr(f"关闭开关：创建空文件 {CLAUDE_DIR / 'vault-checkpoint.off'}。", f"Off switch: create an empty file {CLAUDE_DIR / 'vault-checkpoint.off'}."))


def install():
    settings_path = CLAUDE_DIR / "settings.json"
    md_path = CLAUDE_DIR / "CLAUDE.md"
    settings = load_settings(settings_path)  # validate before touching anything

    (CLAUDE_DIR / "hooks").mkdir(parents=True, exist_ok=True)

    # 1. hook script, always LF so Git Bash can run it
    hook = CLAUDE_DIR / "hooks" / HOOK_NAME
    hook_bytes = (HERE / HOOK_NAME).read_bytes().replace(b"\r\n", b"\n")
    write_if_changed(hook, hook_bytes)
    try:
        hook.chmod(0o755)
    except Exception:  # noqa: BLE001
        pass

    # 2. CLAUDE.md section
    block = snippet_block()
    existing = read_text(md_path)
    if START in existing and END in existing:
        new = BLOCK_RE.sub(lambda _m: block, existing, count=1)
    else:
        new = (existing.rstrip("\n") + "\n\n" if existing.strip() else "") + block
    write_if_changed(md_path, new, keep_eol=True)

    # 3. settings.json
    hooks = settings.setdefault("hooks", {})
    stop = hooks.setdefault("Stop", [])
    if not has_hook(settings):
        stop.append({"hooks": [{"type": "command", "command": HOOK_CMD, "timeout": 5}]})
    dirs = settings.setdefault("permissions", {}).setdefault("additionalDirectories", [])
    if str(VAULT) not in dirs:
        dirs.append(str(VAULT))
    write_if_changed(settings_path, dump_settings(settings))


def uninstall():
    settings_path = CLAUDE_DIR / "settings.json"
    md_path = CLAUDE_DIR / "CLAUDE.md"
    settings = load_settings(settings_path)

    existing = read_text(md_path)
    if START in existing and END in existing:
        new = BLOCK_RE.sub("", existing, count=1).rstrip("\n")
        write_if_changed(md_path, (new + "\n") if new else "", keep_eol=True)

    if settings_path.exists():
        hooks = settings.get("hooks", {})
        kept = []
        for entry in hooks.get("Stop", []) or []:
            entry["hooks"] = [h for h in entry.get("hooks", []) if HOOK_NAME not in str(h.get("command", ""))]
            if entry["hooks"]:
                kept.append(entry)
        if kept:
            hooks["Stop"] = kept
        else:
            hooks.pop("Stop", None)
        if not hooks:
            settings.pop("hooks", None)
        perms = settings.get("permissions", {})
        dirs = [d for d in perms.get("additionalDirectories", []) if d != str(VAULT)]
        if dirs:
            perms["additionalDirectories"] = dirs
        else:
            perms.pop("additionalDirectories", None)
        if not perms:
            settings.pop("permissions", None)
        write_if_changed(settings_path, dump_settings(settings))

    hook = CLAUDE_DIR / "hooks" / HOOK_NAME
    if hook.exists():
        hook.unlink()
        say(tr(f"  已移除 {hook}", f"  removed {hook}"))


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--uninstall", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--yes", action="store_true")
    args = ap.parse_args()

    plan(args.uninstall)
    if args.dry_run:
        return 0
    if not args.yes and input(tr("继续吗？[y/N] ", "Continue? [y/N] ")).strip().lower() not in ("y", "yes"):
        say(tr("已取消，没有做任何修改。", "Cancelled; nothing was changed."))
        return 1
    (uninstall if args.uninstall else install)()
    say(tr("完成。新开的 Claude Code 会话会生效，已打开的会话需要重启。", "Done. New Claude Code sessions pick it up; restart sessions that are already open."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
