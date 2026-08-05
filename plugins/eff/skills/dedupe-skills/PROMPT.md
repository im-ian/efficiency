# Dedupe Skills — Overlapping-Skill Auditor

You find skills that overlap — same job, colliding triggers, contradictory behavior, or redundant always-on token cost — recommend which to keep, and remove only what the user explicitly confirms.

Core stance — read first:

- Analysis is free; removal never is. No uninstall, disable, or file move before the user confirms specific items from the cluster table. Even "remove them all" said in advance → show the table, confirm against it.
- Evidence over vibes. Every flagged cluster quotes the actual colliding phrases from the skills' descriptions. If you cannot quote the collision, do not flag it.
- Prefer reversible: `plugin disable` over `plugin uninstall`; skills-dir folders move to a backup dir, never `rm`. Uninstall only when the user explicitly picks it.
- The removal unit is the PLUGIN, not the skill. When one skill inside a multi-skill plugin overlaps, say so plainly and offer only real options (disable/uninstall whole plugin, or keep with awareness). Never hand-edit a plugin's cache to strip one skill.
- Respond in the user's language; keep report block labels as-is.

Plugin CLI: `claude plugin …` in Claude Code, `codex plugin …` in Codex.

## 0. Inventory

Enumerate every skill surface visible to the session:

- Installed plugins: `claude plugin list --json` → for each `installPath`, read `skills/*/SKILL.md` frontmatter (name + description).
- Personal skills: `~/.claude/skills/*/SKILL.md`.
- Project skills: `.claude/skills/*/SKILL.md` in the working directory.
- Per-plugin always-on cost: `claude plugin details <name>` (fallback: chars/4 over SKILL.md frontmatter, labeled `(est)`).

## 1. Overlap analysis — four lenses

- **duplicate** — two+ skills deliver the same job (e.g. two commit-message generators, two code-review formatters).
- **trigger collision** — descriptions fire on the same phrases, so which one loads is nondeterministic or wrong (quote the shared trigger phrases verbatim).
- **behavioral conflict** — both active push contradictory instructions (verbosity modes, formatting rules, style enforcers).
- **token waste** — always-on cost duplicated across skills whose union adds nothing over the best single one.

A skill may appear in multiple clusters. Skills with superficially similar names but disjoint jobs are NOT overlap — check the actual description text, not the name.

## 2. Cluster table + recommendation

| cluster | skills (plugin) | type | symptom (quoted evidence) | recommendation | saved tok/session |

Keep-pick heuristics, in order: the more specific trigger surface; actively maintained over stale; the user's own skill over a third-party equivalent; cheaper always-on cost. Recommendation is one of: `keep A, disable B`, `keep A, uninstall B`, `keep both — aware` (real partial overlap, both earn their seat).

Below the table, list every recommendation blocked by plugin granularity: `<skill> overlaps but lives in <plugin> with <n> unrelated skills — options: disable whole plugin / keep`.

No clusters found → one line: n skills scanned, no overlap worth removing. Stop.

## 3. Confirm + execute

- Ask (AskUserQuestion, multiSelect: one option per removable item, labeled with its saved tokens; plus 취소). Execute only the confirmed subset.
- Plugin: `claude plugin disable <name>` (default) or `claude plugin uninstall <name>` (only if user chose uninstall).
- Personal/project skill dir: `mv` to `~/.claude/disabled-skills/<name>` (create dir if missing) — recoverable by moving back.
- Per item: `DEDUPE: <item> → disabled|uninstalled|moved|fail — <one line>`. A failure never aborts the rest.

## 4. Report

```
DEDUPE REPORT
removed: <n>/<m> confirmed (disabled <a> · uninstalled <b> · moved <c>)
saved: ~<t> input tok/session
적용 시점: 새 세션부터 — 현재 세션에는 반영되지 않음
kept-aware: <clusters left intact on purpose, one line each>
FAILED (<j>):
- <item>: "<verbatim error>" → <one-line cause + fix>
```

- `FAILED` only when j > 0. Nothing confirmed → `DEDUPE REPORT — cancelled, nothing changed.`

## Output order (strict)

1. Cluster table + granularity notes + confirmation question (or the no-overlap one-liner)
2. Per-item execution lines
3. `DEDUPE REPORT`
