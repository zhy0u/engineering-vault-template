## Personal knowledge base (engineering-vault)

My personal knowledge base is at `{{VAULT}}`: an Obsidian vault that is also a git repository (your own private GitHub repo).

### Proactively record general knowledge

When you find something during work that will be useful again, record it in the knowledge base without waiting for me to ask: non-obvious discoveries, pitfalls of parts/protocols/tools, how a hard problem was solved, the general reason behind a design choice, references worth keeping. Record reusable conclusions only, not a step-by-step log.

Do not record:

- Project-internal details, customer information, company names, unreleased designs, internal addresses.
- Any password, token or key.
- Anything you are unsure about: skip it, or ask me once.

Before recording, generalise the content and strip project and company context. For example write "the ST25DV GPO is an open-drain output and needs an external pull-up", not "in some project the GPO did not work".

How to record:

1. Read `{{VAULT}}\CLAUDE.md` first (no need to re-read if you did in this session) and write to `{{VAULT}}\knowledge\<topic>\YYYY-MM-DD-topic.md` per its conventions, with a lowercase English topic.
2. In the frontmatter use `source: claude`, `ai_generated: true`, `reviewed: false`, and a one-line `summary`.
3. Search existing notes first (grep keywords under `{{VAULT}}\knowledge`); if one exists, append and update `updated` — do not create a duplicate and do not rewrite existing content.
4. After writing, commit and push in the knowledge base: `git -C {{VAULT}} add <file>`, `git -C {{VAULT}} commit -m "vault: add knowledge <topic>"`, `git -C {{VAULT}} push`. Never force-push.
5. Do not interrupt the task in progress for this; after recording, say at most one sentence about which file it went to.

Never delete files in the knowledge base and never overwrite existing content.

### Consulting it

When a task may already be documented (a part you looked up before, a protocol, how a pitfall was solved), look in `{{VAULT}}` first (read `Index.md`, or grep keywords) before deciding whether to research from scratch. Whether it is worth checking is your call; not every task needs it.
