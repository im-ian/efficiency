# blitz — Force-Parallel Fork-Merge Orchestrator

A Claude Code / Codex skill that refuses to refuse parallelization.

Agents often decline to parallelize code work — "the scopes overlap", "these tasks will conflict", "this has to be done sequentially". **blitz overrides that objection.** Overlap is a merge problem, not a parallelization blocker: fork first, merge later, and pay for the speed with a verification gate that is never optional.

```
       ┌─ slice A ─┐
task ──┼─ slice B ─┼──▶ merge ──▶ verification gate ──▶ done
       └─ slice C ─┘    (취합)     (build · tests · review)
 (선작업: shared contract first)
```

## The trade

blitz is a **speed-first** strategy. It deliberately accepts textual and semantic conflicts during fan-out in exchange for wall-clock time, then repays the debt at the end:

| phase | what happens |
|-------|--------------|
| **Slice** | 2–6 slices by deliverable, overlapping files allowed; collision zones declared up front |
| **Contract (선작업)** | ≤10% of effort pinning shared interfaces, stubs, and naming so slices diverge less |
| **Fan-out** | all slices run concurrently, no mid-flight coordination — stub and keep going |
| **Merge (취합)** | one merger resolves textual conflicts by intent and hunts semantic ones (duplicate helpers, double registration, divergent naming) |
| **Gate** | build + full test suite + line-by-line collision review + fresh-eyes review of the merged diff. Loop until green. **Never skipped.** |

A blitz run that skips the gate is a failed run, however fast it finished.

## Install

Marketplace (recommended):

```
/plugin marketplace add im-ian/blitz-skills
/plugin install blitz@blitz
```

Manual symlink:

```
ln -s "$PWD/plugin/skills/blitz" ~/.claude/skills/blitz
```

## Usage

```
/blitz add dark mode and i18n to the app
/blitz PLAN ONLY refactor auth + add rate limiting
```

Also triggers on natural language: "parallelize anyway", "ignore conflicts and run in parallel", "충돌 무시하고 병렬로", "선작업 후 취합".

`PLAN ONLY` stops after the slice table and contract — nothing executes.

## When not to use

- A change smaller than the merge overhead (blitz skips itself: `BLITZ: skip — too small`).
- Destructive/irreversible steps (live-data migrations, force-push) — blitz serializes those after the gate and parallelizes everything around them.

## License

MIT
