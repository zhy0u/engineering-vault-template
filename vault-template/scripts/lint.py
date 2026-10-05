#!/usr/bin/env python3
"""Check the vault.

Free-form writing is allowed: notes without frontmatter or a dated file name are reported as
"untidy" (未规整 in a Chinese vault) warnings, not errors, so Claude can tidy them later after asking you.
Errors are only real inconsistencies: duplicate file names, invalid type, project != folder.

  python scripts/lint.py            # errors fail (exit 1), everything else is a warning
  python scripts/lint.py --strict   # untidy notes and broken links also count as errors
"""
import argparse
import datetime
import re
import sys

from vaultlib import ROOT, note_files, read_note, rel, t, untidy_reasons, utf8_stdout

VALID_TYPES = {"note", "debug", "decision", "knowledge"}
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
INBOX_STALE_DAYS = 7


def main():
    utf8_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help=t("lint_strict_help"))
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
            errors.append(t("lint_dup", stem=stem, paths=", ".join(rel(p) for p in paths)))

    broken = []
    for p in notes:
        r = rel(p)
        parts = r.split("/")
        top = parts[0]
        meta, body = read_note(p)

        if top == "inbox":
            age = (datetime.datetime.now() - datetime.datetime.fromtimestamp(p.stat().st_mtime)).days
            if age >= INBOX_STALE_DAYS:
                warnings.append(t("lint_stale", r=r, age=age))
        else:
            reasons = untidy_reasons(p, meta)
            if reasons:
                untidy_notes.add(r)
                untidy.append(t("lint_untidy", r=r, why="; ".join(reasons)))
            if meta.get("type") and meta["type"] not in VALID_TYPES:
                errors.append(t("lint_type", r=r, valid=sorted(VALID_TYPES), got=meta["type"]))
            if top == "projects" and meta.get("project") and len(parts) > 2 and meta["project"] != parts[1]:
                errors.append(t("lint_proj", r=r, p=meta["project"], f=parts[1]))
            if str(meta.get("ai_generated", "")).lower() == "true" and str(meta.get("reviewed", "")).lower() != "true":
                warnings.append(t("lint_ai", r=r))

        text = INLINE_CODE_RE.sub("", FENCE_RE.sub("", body))
        for target in LINK_RE.findall(text):
            target = target.strip().replace("\\", "")
            if "/" in target:
                if (ROOT / target).exists() or (ROOT / (target + ".md")).exists():
                    continue
                broken.append(t("lint_broken", r=r, target=target))
            elif "." in target and not target.endswith(".md"):
                if target not in all_files:
                    broken.append(t("lint_attach", r=r, target=target))
            elif target.removesuffix(".md") not in link_targets:
                broken.append(t("lint_broken", r=r, target=target))

    if args.strict:
        errors += untidy + broken
        untidy, broken = [], []

    for w in warnings + broken + untidy:
        print(t("lint_warn") + w)
    for e in errors:
        print(t("lint_err") + e)
    print("\n" + t("lint_summary", n=len(notes), e=len(errors), u=len(untidy_notes), b=len(broken), w=len(warnings)))
    if untidy_notes:
        print(t("lint_hint"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
