#!/usr/bin/env python3
"""Generate Index.md, projects/<name>/_index.md and knowledge/_index.md.

Every .md under projects/ (including sub-folders) and knowledge/ is listed, with or without
frontmatter. Notes that are not tidy yet are marked "untidy" (未规整 in a Chinese vault) in the status column.
"""
from collections import Counter, defaultdict

from vaultlib import (ROOT, created_date, display_title, note_files, read_note, rel, t, truthy,
                      untidy_reasons, utf8_stdout)

HEADER = t("gen_header") + "\n\n"


def cell(text):
    return str(text or "").replace("|", "\\|").replace("\n", " ").strip()


def load(p):
    meta, body = read_note(p)
    info = {
        "path": p,
        "meta": meta,
        "date": created_date(p, meta),
        "title": display_title(p, meta, body),
        "untidy": bool(untidy_reasons(p, meta)),
    }
    return info


def link(info):
    return f"[[{info['path'].stem}\\|{cell(info['title'])}]]"


def status_cell(info):
    meta = info["meta"]
    parts = []
    if meta.get("status"):
        parts.append(str(meta["status"]))
    if info["untidy"]:
        parts.append(t("untidy_label"))
    if truthy(meta.get("ai_generated")) and not truthy(meta.get("reviewed")):
        parts.append(t("ai_unreviewed"))
    return cell(" / ".join(parts))


def sort_items(items):
    return sorted(items, key=lambda i: (i["date"], i["path"].name), reverse=True)


def write(path, content):
    path.write_text(content, encoding="utf-8", newline="\n")


def project_index(name, items):
    types = Counter((i["meta"].get("type") or t("untyped")) for i in items)
    untidy = sum(1 for i in items if i["untidy"])
    lines = [HEADER, "# " + t("idx_title", name=name) + "\n\n"]
    lines.append(
        t("idx_summary", n=len(items), u=untidy,
          types=t("types_sep").join(f"{k} {n}" for k, n in sorted(types.items()))) + "\n\n"
    )
    lines.append(t("idx_head") + "\n|---|---|---|---|---|\n")
    for i in items:
        lines.append(
            f"| {i['date']} | {cell(i['meta'].get('type') or '-')} | {link(i)} | {status_cell(i)} | {cell(i['meta'].get('summary'))} |\n"
        )
    return "".join(lines)


def knowledge_index(items):
    groups = defaultdict(list)
    for i in items:
        parts = i["path"].relative_to(ROOT / "knowledge").parts
        groups[parts[0] if len(parts) > 1 else t("uncategorised")].append(i)
    lines = [HEADER, "# " + t("know_title") + "\n\n", t("know_summary", n=len(items)) + "\n\n"]
    for topic in sorted(groups):
        lines.append(f"## {topic}\n\n" + t("know_head") + "\n|---|---|---|---|---|---|\n")
        for i in sort_items(groups[topic]):
            m = i["meta"]
            lines.append(
                f"| {i['date']} | {link(i)} | {cell(m.get('source'))} | {cell(m.get('project'))} | {status_cell(i)} | {cell(m.get('summary'))} |\n"
            )
        lines.append("\n")
    return "".join(lines)


def main():
    utf8_stdout()
    projects_dir = ROOT / "projects"
    project_rows = []
    if projects_dir.exists():
        for d in sorted(x for x in projects_dir.iterdir() if x.is_dir() and not x.name.startswith(("_", "."))):
            items = sort_items([load(p) for p in note_files(["projects/" + d.name])])
            write(d / "_index.md", project_index(d.name, items))
            project_rows.append((d.name, len(items), sum(1 for i in items if i["untidy"]), items[0]["date"] if items else "-"))

    k_items = sort_items([load(p) for p in note_files(["knowledge"])])
    (ROOT / "knowledge").mkdir(exist_ok=True)
    write(ROOT / "knowledge" / "_index.md", knowledge_index(k_items))

    inbox = note_files(["inbox"])
    lines = [HEADER, "# " + t("all_title") + "\n\n", t("all_inbox", n=len(inbox)) + "\n\n"]
    for p in inbox:
        lines.append(f"- [[{p.stem}]]\n")
    lines.append("\n" + t("all_projects") + "\n\n" + t("all_head") + "\n|---|---|---|---|\n")
    for name, count, untidy, latest in project_rows:
        lines.append(f"| [[projects/{name}/_index\\|{name}]] | {count} | {untidy} | {latest} |\n")
    k_untidy = sum(1 for i in k_items if i["untidy"])
    lines.append("\n" + t("all_know", n=len(k_items), u=k_untidy) + "\n")
    write(ROOT / "Index.md", "".join(lines))

    print(t("built", p=len(project_rows), k=len(k_items), i=len(inbox)))


if __name__ == "__main__":
    main()
