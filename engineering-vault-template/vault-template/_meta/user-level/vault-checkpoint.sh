#!/usr/bin/env bash
#
# Stop hook: once per turn, before Claude finishes, ask whether this turn produced general,
# reusable knowledge worth saving to the engineering-vault. A "no" ends silently.
#
# - No jq needed (Git Bash on Windows usually has none): the two checks use grep on the stdin JSON.
# - Returns hookSpecificOutput.additionalContext, not decision:block, so it shows up as
#   non-error "Stop hook feedback".
# - stop_hook_active is true when a Stop hook already forced a continuation this turn: let it stop.
# - Sessions started inside the vault are skipped; they are about the notes already.
# - Off switch: create the empty file ~/.claude/vault-checkpoint.off (delete it to turn back on).

if [ -f "$HOME/.claude/vault-checkpoint.off" ]; then
  exit 0
fi

input=$(cat)

if printf '%s' "$input" | grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi

if printf '%s' "$input" | grep -Eq '"cwd"[[:space:]]*:[[:space:]]*"[^"]*engineering-vault'; then
  exit 0
fi

cat <<'EOF'
{"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"Before stopping: did this turn produce general, reusable knowledge worth saving to the engineering-vault, per the engineering-vault section of the user-level CLAUDE.md (a non-obvious discovery, a pitfall, a fix, a general rationale)? Save it only if it can be generalized without project, customer or company details and contains no secrets. If yes, save it now and mention the file in one short sentence. If no, just stop; do not mention this check or say there was nothing to save."}}
EOF
