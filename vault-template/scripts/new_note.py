#!/usr/bin/env python3
"""Create a note from a template.

  python scripts/new_note.py ProjectA debug "ST25DV GPO 不触发"
  python scripts/new_note.py knowledge/embedded knowledge "Open-Drain 需要外部上拉"
  python scripts/new_note.py ProjectA note "标题" --slug nvm-layout
"""
import argparse
import datetime
import re
import sys

from vaultlib import ROOT, t, utf8_stdout

TEMPLATES = {"note": "note.md", "debug": "debug.md", "decision": "decision.md", "knowledge": "knowledge.md"}


def slugify(title):
    s = re.sub(r'[\\/:*?"<>|]', "", title).strip().lower()
    s = re.sub(r"\s+", "-", s)
    return s.strip("-") or "untitled"


def main():
    utf8_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help=t("nn_target"))
    ap.add_argument("type", choices=sorted(TEMPLATES))
    ap.add_argument("title")
    ap.add_argument("--slug", help=t("nn_slug"))
    args = ap.parse_args()

    today = datetime.date.today().isoformat()
    is_knowledge = args.target.replace("\\", "/").startswith("knowledge")
    if is_knowledge:
        folder = ROOT / args.target.replace("\\", "/")
        project = ""
    else:
        folder = ROOT / "projects" / args.target
        project = args.target
    folder.mkdir(parents=True, exist_ok=True)

    path = folder / f"{today}-{args.slug or slugify(args.title)}.md"
    if path.exists():
        print(t("nn_exists", path=path))
        return 1

    text = (ROOT / "_templates" / TEMPLATES[args.type]).read_text(encoding="utf-8")
    text = text.replace("{{title}}", args.title).replace("{{date:YYYY-MM-DD}}", today)
    if project:
        text = re.sub(r"^project:.*$", f"project: {project}", text, count=1, flags=re.M)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(path.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
