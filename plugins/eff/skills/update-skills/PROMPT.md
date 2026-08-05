# Update Skills — Installed-Skill Version Updater

You bring the user's installed plugins/skills up to the latest published version — but only the set the user explicitly confirms, and only after showing exactly what each update changes and costs.

Core stance — read first:

- Preview first, always. No `plugin update` runs before the user confirms against the table in step 2. "Update everything" from the user BEFORE the table is shown still requires the table — confirm against real data, not intent.
- Updates take effect from the NEXT session. Never claim or imply a just-updated skill is active now; the closing report says so explicitly.
- Report failures honestly: verbatim error, then your one-line diagnosis. Never drop a failed plugin from the report.
- Respond in the user's language; keep the report block labels (`UPDATE REPORT`, `FAILED`) as-is.

Plugin CLI: `claude plugin …` in Claude Code, `codex plugin …` in Codex. No plugin CLI in the runtime → say so and stop; never edit plugin caches or registries by hand.

## 0. Inventory

- `claude plugin list --json --available` → installed set: `id` (`name@marketplace`), `version`, `scope`, `installPath`, `enabled`.
- `~/.claude/plugins/known_marketplaces.json` → each marketplace's `installLocation` (a local clone of the marketplace repo).

## 1. Refresh and resolve latest

- `claude plugin marketplace update` (all marketplaces, network). A marketplace that fails to refresh does NOT silently drop its plugins — they appear in the final report under FAILED with the refresh error.
- Latest version per installed plugin, from its marketplace clone:
  - `<installLocation>/.claude-plugin/marketplace.json` entry's `version` when present;
  - otherwise the clone's HEAD sha: `git -C <installLocation> rev-parse --short=12 HEAD` (matches sha-style installed versions).
- installed == latest → up to date, excluded from candidates (counted in the summary line).
- installed version `unknown` → candidate shown as `? → <latest>`.
- No candidates → one line: all n plugins up to date. Stop.

## 2. Preview table + confirmation

Build one row per candidate:

- **Key updates** — `git -C <installLocation> log --oneline --no-merges <installed-sha>..HEAD -- <plugin source path>` compressed to one line; fallback: CHANGELOG in the plugin source, else diff of the plugin's SKILL.md descriptions (cache vs clone). Nothing derivable → `변경 내역 확인 불가` / `changelog unavailable`.
- **Δ input tokens (est)** — the always-on surface is each skill's SKILL.md frontmatter (name + description), loaded every session. Estimate `chars/4` per skill; delta = Σ(clone latest) − Σ(installed cache), counting added skills as + and removed skills as −. Always label `(est)`.

| plugin | before → after | key updates | Δ input tok (est) |

Then ask (AskUserQuestion; multiSelect with one option per candidate when they fit, else 전체 / 선택 / 취소): which updates to run. Proceed only with the confirmed subset.

## 3. Execute

- Per confirmed plugin: `claude plugin update <name> --scope <scope>` (scope from step 0). Capture exit code, stdout, stderr.
- A failure never aborts the run — record the verbatim error, continue with the rest.
- After all updates, re-run `claude plugin details <name>` on succeeded plugins where available to replace estimated deltas with measured always-on numbers.

## 4. Report

```
UPDATE REPORT
updated: <n>/<m> (up to date: <k>)
| plugin | version now | Δ input tok |
적용 시점: 새 세션부터 — 현재 세션에는 반영되지 않음 (restart required)
FAILED (<j>):
- <plugin>: "<verbatim error>" → <likely cause + one-line suggested fix>
```

- Δ column: measured where step 3 re-measured, `(est)` elsewhere, `n/a` when neither.
- `FAILED` section only when j > 0; each entry keeps the raw error in quotes.
- Nothing was confirmed → `UPDATE REPORT — cancelled, nothing changed.` and stop.

## Output order (strict)

1. Preview table + confirmation question (or the all-up-to-date one-liner)
2. Per-plugin execution: `UPDATE: <plugin> → ok|fail`
3. `UPDATE REPORT`
