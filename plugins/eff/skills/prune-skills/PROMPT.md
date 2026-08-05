# Prune Skills — Unused-Skill Pruner

You measure which installed skills and plugin tools are actually used, surface the dead weight with evidence, and remove only what the user explicitly confirms.

Core stance — read first:

- Real data only. Every usage number comes from transcript scans; never estimate, extrapolate, or guess a call count. Unmeasurable → `no data`, and `no data` is NOT evidence of non-use.
- Analysis is free; removal never is. No uninstall, disable, or file move before the user confirms specific items from the usage table. "Remove everything unused" said in advance → still show the table, confirm against it.
- Prefer reversible: `plugin disable` over `plugin uninstall`; skills-dir folders move to a backup dir, never `rm`. Uninstall only when the user explicitly picks it.
- A plugin's value may not be skill invocations: hooks fire harness-side, LSP servers attach silently. Never call a hook/LSP plugin "unused" from skill counts alone — mark it `hook-driven — usage n/a`.
- Respond in the user's language; keep report block labels as-is.

Plugin CLI: `claude plugin …` in Claude Code, `codex plugin …` in Codex. Window default: 90 days (user may override, e.g. "last 30 days").

## 0. Inventory

- `claude plugin list --json` → installed plugins: id, version, `installedAt`, `installPath`, enabled.
- Per plugin, from `installPath`: skill names (`skills/*/SKILL.md`), whether it ships hooks/MCP servers/LSP (`hooks/`, `.mcp.json`, plugin.json entries — or `claude plugin details <name>`).
- Always-on cost per plugin: `claude plugin details <name>`.
- Personal skills (`~/.claude/skills/*/SKILL.md`) join the same table.

## 1. Measure usage

Scan session transcripts: `~/.claude/projects/*/*.jsonl`, files with mtime inside the window. One pass, one script — count per transcript line of type `assistant` every `message.content[].type == "tool_use"`:

- `name == "Skill"` → count `input.skill` (values look like `plugin:skill` or bare `skill`).
- `name` starting `mcp__<server>__` → count per server; map server → plugin that ships it.
- Any other `name` matching a plugin-provided tool → count to that plugin.

Record per skill/plugin: total calls, last-used date (transcript file mtime of the newest hit). Keep the scan cheap: pre-filter files with `grep -l` on the skill/tool names, then parse only hits. Codex or a runtime without local transcripts → say usage cannot be measured there and stop (never fabricate a table).

## 2. Usage table + candidates

| skill/plugin | calls (window) | last used | always-on tok | verdict |

Verdicts:

- **unused** — 0 calls, no hooks/LSP, installed BEFORE the window started (grace: anything installed inside the window is `too new`, never a candidate).
- **rare** — calls > 0 but ≲1/month AND always-on cost meaningful; judgment call, show the math.
- **hook-driven — usage n/a** — ships hooks/LSP; excluded from candidates unless the user says they stopped wanting the behavior itself.
- **active** / **too new** / **no data** — kept, listed for completeness (collapse the active rows to one summary line if long).

Candidates = unused + rare, sorted by always-on cost descending. Below the table: same plugin-granularity note as removal applies per PLUGIN — one used skill in a plugin protects its unused siblings; say so per item.

No candidates → one line: n skills scanned over <window>, nothing worth pruning. Stop.

## 3. Confirm + execute

- Ask (AskUserQuestion, multiSelect: one option per candidate labeled `<name> — <calls> calls, saves ~<t> tok/session`; plus 취소). Execute only the confirmed subset.
- Plugin: `claude plugin disable <name>` (default) or `claude plugin uninstall <name>` (only if user chose it).
- Personal skill dir: `mv` to `~/.claude/disabled-skills/<name>`.
- Per item: `PRUNE: <item> → disabled|uninstalled|moved|fail — <one line>`. A failure never aborts the rest.

## 4. Report

```
PRUNE REPORT
window: <period> · scanned: <k> transcripts
removed: <n>/<m> confirmed (disabled <a> · uninstalled <b> · moved <c>)
saved: ~<t> input tok/session
적용 시점: 새 세션부터 — 현재 세션에는 반영되지 않음
kept: <candidates the user chose to keep, one line>
FAILED (<j>):
- <item>: "<verbatim error>" → <one-line cause + fix>
```

- `FAILED` only when j > 0. Nothing confirmed → `PRUNE REPORT — cancelled, nothing changed.`

## Output order (strict)

1. Usage table + granularity notes + confirmation question (or the nothing-to-prune one-liner)
2. Per-item execution lines
3. `PRUNE REPORT`
