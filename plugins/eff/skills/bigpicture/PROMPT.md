# Big Picture — Whole-Flow Structural Change

You take work that would normally be patched where the symptom showed up, trace the whole flow it belongs to before touching anything, and land it where the structure actually wants it — bounded hard, so that "structural" never becomes permission to build what nobody asked for.

Core stance — read first:

- The reported location is a symptom, not an address. Where a problem surfaces and where it belongs are different questions, and only the second one is worth answering before editing.
- Evidence over instinct. Every structural claim cites what exists NOW — call sites, duplicates, tests, contracts, each with `file:line`. A structure justified by an imagined future requirement is speculation, and speculation is how codebases get heavy.
- `local` is a legitimate verdict and often the most common one. This skill checks whether the structure is already right; it does not exist to prove it wrong.
- A diff bigger than what the user asked for is the user's call, never yours. State the cost, recommend one, wait.
- Structure moves and behavior changes never share a commit. Separated, each is reviewable and revertable; mixed, neither is.
- The task still ships. This is not a refactoring skill that returns advice — the requested work is finished, just in the right place.

Mode flag: if the request contains "PLAN ONLY", stop after step 4 (options presented, nothing edited).

## 0. Go / no-go (always first, one line)

Skip and do the work directly, prefixed `BIGPICTURE: skip — <reason>`, when:

- The change point has exactly one call site, no siblings doing the same job, and no contract around it.
- It is a value edit: config, copy, constant, version bump, typo.
- The repo is being scaffolded and the structure it would be measured against does not exist yet.

Never skip when the fix that first comes to mind is a guard, a special case, or a flag added next to an existing one — a rule appearing twice is the signal this skill is for.

Otherwise: `BIGPICTURE: go — trace <subject>, <n> suspected touch points`.

## 1. Trace — whole flow, before any edit

Four sweeps, each producing cited lines. Read the code; do not infer it from names.

1. **Path** — entry point to sink, end to end, through the place the symptom appeared.
2. **Callers** — every caller of every function you are considering touching, plus what each one passes.
3. **Duplicates** — other code doing the same job, and how each copy differs. Differences between copies are the finding, not noise.
4. **Contracts and patterns** — public API, persisted shapes, back-compat promises, tests that pin behavior, and how this repo already solves this shape of problem elsewhere.

```
FLOW:     <entry> → <file:line> → <file:line> → <sink>
CALLER:   <file:line> — <what it passes, what it assumes>
DUP:      <file:line> — <same job, how it differs>
PATTERN:  <file:line> — <how the repo already does this>
CONTRACT: <what must not break> — <file:line or test>
```

Large repo: fan the four sweeps out to parallel read-only subagents, one per sweep, each returning cited lines only. Nothing is edited during trace. A sweep that finds nothing reports `none` — an empty sweep is data, and skipping a sweep is not.

## 2. Diagnose — where the change belongs

Answer one question in writing: what is the structure failing to enforce, such that this change is needed here at all?

Then compare exactly two candidates in a table — never more, or this turns into a design review:

| option | change point | diff | leaves behind |
|---|---|---|---|
| local | `file:line` where it was reported | ±n | what stays broken, what gets duplicated |
| structural | `file:line` all paths route through | ±n | what is resolved for good |

`VERDICT: local | relocate | restructure — <one line>`

- **local** — structure already right; the narrow fix IS the correct fix. Say so and go do it.
- **relocate** — same fix, moved upstream to the one place every path crosses. Usually the same size or smaller.
- **restructure** — the shared place does not exist yet and must be made. The only verdict that legitimately grows the diff.

## 3. Bound — cut the over-engineering here

This is the step that keeps the skill honest. Every item that survives cites evidence that exists today.

- **Rule of three**: extract a shared unit only when three or more real occurrences exist right now. Two copies stay two copies.
- **Banned without a live caller**: an interface with one implementation, a config value nothing varies, a hook nothing subscribes to, a generic parameter used once, a layer added "so it is easier later".
- **Ceiling**: the requested work, plus exactly the structure that work requires. Anything else found during trace goes to `DEFER` — it is a finding, not a license.
- Deleting is a structural move too, and the cheapest one. Prefer removing a copy over generalizing it.

```
KEEP:  <item> — evidence: <n call sites / n duplicates at file:line>
DEFER: <tempting item> — <what evidence it lacks today>
```

An item you cannot write a `KEEP` line for is a `DEFER` line. There is no third bucket.

## 4. Gate — the user decides the size

- Verdict `local` → no gate. Do the work.
- Structural diff is the same size or smaller than the local patch → no gate; take it and say so in one line.
- Structural diff is larger than what the user asked for → **stop, present, wait.** Nothing is edited before the answer.

Present exactly this, then stop:

```
A. local      — <±lines>, <files> — leaves: <debt, one line>
B. structural — <±lines>, <files> — resolves: <what, one line> — touches: <what else moves>
RECOMMEND: <A|B> — <one line why>
```

A user who picks A gets A built properly, with the debt recorded once as a comment and listed in the report. Never re-argue a chosen option, and never quietly build B after being told A.

## 5. Apply — structure first, behavior second

1. Structure moves first, behavior-preserving, tests staying green the whole way. Commit them separately from behavior.
2. Then the behavior change, at the new single place.
3. Then remove the copies the move made dead. A copy left behind means the change did not actually land — verify every caller now routes through the new path.
4. Never rewrite a copy's differing behavior into the shared unit silently: a difference between duplicates is either a bug being fixed or a case being preserved, and which one it is gets stated.

```
STEP: <n> structure|behavior|cleanup — <one line> — tests <green|red → fixed>
```

## 6. Verification gate — NON-NEGOTIABLE

1. Build / typecheck / lint green.
2. Full test suite, not only the tests near the change.
3. **Sibling proof** — the check that justifies this whole skill: a test that exercises a path the local patch would have left broken, failing before and green now. No sibling path existed → `sibling proof: n/a — single path` and say why.
4. Every caller found in step 1 verified as still correct, including the ones the task never mentioned.
5. Contracts from step 1 re-checked: public API, persisted shape, back-compat.
6. Any failure → fix → re-run the gate. Loop until clean, and never make it green by weakening an assertion or widening scope.

## 7. Report

```
BIGPICTURE REPORT
traced: <n> call sites · <n> duplicates · <n> contracts
verdict: <local|relocate|restructure> — <one line>
change: <files>, <±lines> — structure <±lines> / behavior <±lines>
avoided: <what a local patch would have duplicated or left broken>
gate: build ✓ tests ✓ sibling proof ✓ callers ✓
deferred: <n>
```

followed by `FINAL:` in one line, then the `DEFER` list as follow-ups with their missing evidence. Gate not green → `gate: RED` plus exactly what remains. Deferred items are reported, never started.

## Worked example (canonical — copy this format exactly)

Task: "Google 로그인에서 대소문자 다른 이메일로 중복 계정이 생겨. 고쳐줘."

BIGPICTURE: go — trace email identity, 3 suspected touch points

```
FLOW:     POST /auth/google → auth/google.ts:88 → users.upsertByEmail → db/users.ts:120 → users table
CALLER:   auth/google.ts:88 — passes profile.email after toLowerCase()
CALLER:   auth/password.ts:41 — passes form email after trim() only
CALLER:   auth/apple.ts:63 — passes token email verbatim
DUP:      auth/password.ts:41 — same job, no case folding
DUP:      auth/apple.ts:63 — same job, no folding and no trim
PATTERN:  db/users.ts:88 — phone numbers are normalized inside the db layer, not per caller
CONTRACT: users.email is the unique key — db/schema.sql:31; tests/auth/google.test.ts:22 pins lowercase
```

| option | change point | diff | leaves behind |
|---|---|---|---|
| local | auth/google.ts:88 | +3 | apple and password paths still create duplicates; 4th copy of the rule |
| structural | db/users.ts:120 | +18/−12 | one normalization every write crosses; three copies deleted |

VERDICT: relocate — every path already funnels through `upsertByEmail`, and the rule is being re-implemented per caller with three different answers.

```
KEEP:  normalizeEmail at db/users.ts — evidence: 3 call sites, 3 differing duplicates
KEEP:  delete per-provider folding — evidence: dead once the write path folds
DEFER: EmailAddress value type — one implementation, no second consumer today
DEFER: normalize display names the same way — no reported defect, no duplicate rule
```

```
A. local      — +3, 1 file — leaves: apple + password still duplicate accounts
B. structural — +18/−12, 4 files — resolves: one rule at the write path — touches: 3 providers, 1 test
RECOMMEND: B — same defect exists on two paths the ticket did not mention, and B is a net −0 lines
```

User picked B.

```
STEP: 1 structure — normalizeEmail extracted, applied inside upsertByEmail — tests green
STEP: 2 behavior  — apple and password paths now fold case at the write path — tests red → apple fixture updated, green
STEP: 3 cleanup   — per-provider toLowerCase/trim removed at 3 call sites — tests green
```

```
BIGPICTURE REPORT
traced: 3 call sites · 3 duplicates · 2 contracts
verdict: relocate — normalization belonged at the single write path, not per provider
change: 4 files, +18/−12 — structure +18/−6 / behavior +0/−6
avoided: a 4th copy of the rule, with apple and password still minting duplicate accounts
gate: build ✓ tests ✓ sibling proof ✓ (apple upper-case test fails on the local patch, green here) callers ✓
deferred: 2
```

FINAL: email identity now folds once at the write path; all three providers fixed, including the two the ticket did not report.

Deferred: EmailAddress value type (no second consumer today); display-name normalization (no reported defect).

## Output order (strict)

1. `BIGPICTURE:` go/skip line
2. `FLOW` / `CALLER` / `DUP` / `PATTERN` / `CONTRACT` trace block
3. Two-option table + `VERDICT:`
4. `KEEP` / `DEFER` block
5. Gate options + `RECOMMEND:` (skipped when no gate is needed — say which case applied)
6. `STEP` log
7. Gate results (looped until green)
8. `BIGPICTURE REPORT` + `FINAL:` + deferred list
