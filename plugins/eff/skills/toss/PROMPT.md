# Toss — Background Handoff Orchestrator

You are tossing work: hand the current work-in-progress (or a described task) to a background subagent, then immediately return to the user free for anything else. A toss is only finished when the background agent reports back and you close it out with elapsed time, token usage, and a work summary.

Core stance — read first:

- A toss never blocks. After spawn you are fully available for any other request; never wait on the background agent, never poll it, never fabricate or predict its progress or results.
- The background agent starts with ZERO conversation context. The handoff packet must be self-contained enough that a stranger could finish the work from it alone.

## 0. Scope (one line)

What gets tossed: the task text following the invocation; with no text, the current work-in-progress. If nothing is in flight and no task is given: `TOSS: nothing to toss` and stop.

## 1. Handoff packet

Build a self-contained brief — the subagent sees only this:

- **goal** — one line: what "done" means.
- **state** — working directory, branch, files touched so far, decisions already made and why.
- **remaining** — the concrete steps left, in order.
- **constraints** — user preferences and hard rules the work must respect (e.g. commit locally but never push, match existing code style).
- **verify** — the command(s) that prove the work is done (build, tests, lint). Done without verification is not done.
- **report-back** — include verbatim: "Your final message is your report. State what you did, verification results with real output, files touched, and anything left undone. Report failures honestly — never claim green that you did not see."

## 2. Spawn

- Record wall-clock start (e.g. `date +%s`).
- Launch ONE background subagent carrying the packet. In Claude Code: the Agent tool with `run_in_background: true` and `name: toss-<slug>`. In another runtime, use its background-agent primitive.
- No background primitive in this runtime → say so plainly and offer to run the work in the foreground instead. Never fake a toss.
- Then immediately hand control back with the receipt and nothing more:

`TOSS: <name> — <one-line task> — running in background, you're free to keep working.`

## 3. While it runs

- Handle any new user work normally. More tosses are fine; each gets its own name and its own close-out.
- Status only on request: read the task's live output (TaskOutput or equivalent) and report one line. Never invent progress.
- The completion signal arrives on its own as a task notification. Do not schedule polls for it.

## 4. Close-out

Triggered by exactly two things: (a) the completion notification arrives, or (b) the user explicitly asks to stop the toss — then stop the background task first (TaskStop or equivalent) and capture whatever output exists.

Terminate the toss session and report:

```
TOSS REPORT — <name>
status: done | stopped | failed
elapsed: <recorded start → now>
tokens: <from the harness's task metadata/notification; n/a if not surfaced>
summary: <2–5 lines — what was done, verification result, files touched, what remains>
```

- `done` requires the agent's report to show verification actually ran and passed. Verification failed or skipped → `failed`, and the summary names exactly what is red.
- `stopped` → summarize the partial progress visible in captured output; never guess at unseen work.
- After the report the toss is closed. Do not resurrect it — follow-up work is a new toss.

## Worked example (canonical — copy this format exactly)

Mid-session, the user has been refactoring `parser.ts` and says "toss this, let's look at the login bug instead."

TOSS: toss-parser-refactor — finish parser.ts refactor + green tests — running in background, you're free to keep working.

*(main agent immediately starts on the login bug; later, the completion notification arrives)*

```
TOSS REPORT — toss-parser-refactor
status: done
elapsed: 9m 41s
tokens: 38.4k
summary: Extracted tokenize/parse split in parser.ts, updated 3 call sites,
adjusted parser.test.ts. Verification: `npm test` green (42/42).
Files: src/parser.ts, src/index.ts, test/parser.test.ts. Nothing remains.
```

## Output order (strict)

1. `TOSS:` receipt (or `TOSS: nothing to toss`)
2. — silence about the toss while it runs —
3. `TOSS REPORT` on completion or user stop
