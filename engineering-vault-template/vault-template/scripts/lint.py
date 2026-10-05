#!/usr/bin/env python3
"""Check the vault.

Free-form writing is allowed: notes without frontmatter or a dated file name are reported as
"未规整" (untidy) warnings, not errors, so Claude can tidy them later after asking you.
Errors are only real inconsistencies: duplicate file names, invalid type, project != folder.

  python scripts/lint.py            # errors fail (exit 1), everything else is a warning
  python scripts/lint.py --strict   # untidy notes and broken links also count as errors
"""
import argparse
import datetime
import re
import sys

from vaultlib import ROOT, note_files, read_note, rel, untidy_reasons, utf8_stdout

VALID_TYPES = {"note", "debug", "decision", "knowledge"}
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
INBOX_STALE_DAYS = 7


def main():
    utf8_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="untidy notes and broken links become errors")
    args = ap.parse_args()

    errors, untidy, warnings = [], [], []
    untidy_notes = set()

    notes = note_files()
    stems = {}
    for p in notes:
        stems.setdefault(p.stem, []).append(p)

    link_targets = set(stems) | {"Index", "README", "CLAUDE"}
    templates = ROOT / "_templates"
    if templates.exists():
        link_targets |= {p.stem for p in templates.glob("*.md")}
    all_files = {f.name for f in ROOT.rglob("*") if f.is_file() and ".git" not in f.parts}

    for stem, paths in stems.items():
        if len(paths) > 1:
            errors.append(f"文件名重复（wikilink 会歧义）：{stem} -> " + ", ".join(rel(p) for p in paths))

    broken = []
    for p in notes:
        r = rel(p)
        parts = r.split("/")
        top = parts[0]
        meta, body = read_note(p)

        if top == "inbox":
            age = (datetime.datetime.now() - datetime.datetime.fromtimestamp(p.stat().st_mtime)).days
            if age >= INBOX_STALE_DAYS:
                warnings.append(f"{r}: 在 inbox 里已 {age} 天，可以让 Claude 整理")
        else:
            reasons = untidy_reasons(p, meta)
            if reasons:
                untidy_notes.add(r)
                untidy.append(f"{r}: 未规整（" + "；".join(reasons) + "）")
            if meta.get("type") and meta["type"] not in VALID_TYPES:
                errors.append(f"{r}: type 必须是 {sorted(VALID_TYPES)} 之一，现为 {meta['type']}")
            if top == "projects" and meta.get("project") and len(parts) > 2 and meta["project"] != parts[1]:
                errors.append(f"{r}: project={meta['project']} 与所在文件夹 {parts[1]} 不一致")
            if str(meta.get("ai_generated", "")).lower() == "true" and str(meta.get("reviewed", "")).lower() != "true":
                warnings.append(f"{r}: AI 生成且尚未审阅")

        text = INLINE_CODE_RE.sub("", FENCE_RE.sub("", body))
        for target in LINK_RE.findall(text):
            target = target.strip().replace("\\", "")
            if "/" in target:
                if (ROOT / target).exists() or (ROOT / (target + ".md")).exists():
                    continue
                broken.append(f"{r}: 断链 [[{target}]]")
            elif "." in target and not target.endswith(".md"):
                if target not in all_files:
                    broken.append(f"{r}: 附件不存在 [[{target}]]")
            elif target.removesuffix(".md") not in link_targets:
                broken.append(f"{r}: 断链 [[{target}]]")

    if args.strict:
        errors += untidy + broken
        untidy, broken = [], []

    for w in warnings + broken + untidy:
        print("警告  " + w)
    for e in errors:
        print("错误  " + e)
    print(
        f"\n检查了 {len(notes)} 篇笔记：{len(errors)} 个错误，{len(untidy_notes)} 篇未规整，"
        f"{len(broken)} 个断链，{len(warnings)} 个其他提醒"
    )
    if untidy_notes:
        print("提示：未规整的笔记不影响使用，需要时对 Claude 说“整理 <项目名>”即可。")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
