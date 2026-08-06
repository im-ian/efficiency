# Crosscheck — Adversarial Review Debate

You hand an existing change to two fresh subagents that never watched it being written — a challenger that argues it is broken and a defender that argues it is sound — run them through a bounded debate, and then adjudicate against the real code yourself. The debate generates the candidates; running the code decides.

Core stance — read first:

- The author's context is the bias. You already know why the code looks like this, so your own review is worth less than a stranger's. Both debaters are spawned subagents; reviewing it yourself and calling that a cross-check is the one thing this skill exists to prevent.
- Roles are assigned, truth is not. A challenger that manufactures a defect to fill its role, or a defender that defends something indefensible, has failed its job — both are told so in their packet. Conceding is a normal, expected output, not a loss.
- There is no winner and no score. The debate exists to surface claims with their strongest counter-argument attached; the verdict comes from the code in step 4, never from who argued better.
- Every claim carries a burden of evidence. A charge without a concrete failure is not a charge; a defense without a cited guard, contract, or caller is not a defense.
- Debaters are read-only. A debater that edits code has stopped reviewing and started being an unreviewed author.

## 0. Scope (one line)

What is under review, in priority order: the text following the invocation; a named commit range, PR, or file set; otherwise the current uncommitted working diff (`git diff HEAD`). Empty diff and nothing named → `CROSSCHECK: nothing to review` and stop.

Emit `CROSSCHECK: <n> files, <±lines> — challenger vs defender, max 2 rounds`. Diffs above roughly 1500 changed lines are split by area and debated separately; an argument that ranges over 3000 lines settles nothing.

## 1. Packet

Both debaters start with ZERO conversation context and see only this — the same packet, differing in one line (the role):

- **goal** — what the change is supposed to achieve, one or two lines, stated as requirements.
- **constraints** — the contract it must respect: public API, back-compat, style rules, performance or security requirements.
- **how to verify** — the repo's build, test, and lint commands, so a claim can be tested instead of argued.
- **the change** — the diff, plus the fact that the full repo is readable. Both sides are expected to open callers and neighbors.
- **role** — challenger or defender, with the burden from step 2 verbatim.
- **rules** — verbatim: "You did not write this and you are not told why it was written this way. You are read-only: never edit the code. Every claim needs file:line and evidence — for a charge, the input or state that triggers it and the wrong result; for a defense, the guard, contract, or caller that prevents it. Run the verification commands before claiming anything. If you cannot meet the burden, say so plainly — an honest 'nothing here' or 'this one is real' is the correct answer, and inventing material to fill your role is a failed run. No style preferences, no praise, no summary of what the code does."

Never include in the packet, for either side: the author's rationale, what was already checked, which parts you suspect, or the other side's identity beyond the role. The defender derives its defense from the repo, exactly like the challenger derives its charges.

## 2. Roles and burdens

| role | argues | burden met by | fails by |
|---|---|---|---|
| challenger | this change is broken or unsafe | file:line + triggering input/state + the wrong result it produces | listing style nits, restating risk in the abstract, inventing a caller that does not exist |
| defender | this change is sound as written | the guard, contract clause, caller constraint, or test that makes the charge impossible | "probably fine", "unlikely in practice", arguing intent instead of citing code |

Challenger search space — sweep all four, report per area: contract (does it meet the stated goal, including boundaries); blast radius (callers, back-compat, migrations, dead code, siblings routing through the same function); failure paths (errors, partial failure, retries, concurrency, empty and malformed input); trust boundary (only when the diff touches auth, input handling, secrets, permissions, or money).

Large or high-stakes diff → spawn one challenger per area against a single defender. Debate structure and burdens are unchanged; only the challenger count moves.

## 3. Debate — bounded, 2 rounds max

1. **Round 1 — charges.** Challenger returns its charges, each meeting the burden. No charges that meet the burden → it returns none, and the debate ends there.
2. **Round 1 — defense.** Defender receives the charge list verbatim (nothing else added) and answers EVERY charge with one of: `rebut` + cited evidence, or `concede` + one line on why the charge holds. A defender conceding everything is a valid outcome.
3. **Round 2 — reply.** Challenger sees only the rebuttals and may reply to those. Two hard rules: no new charges in round 2 unless a rebuttal itself exposed one (mark it `new-from-rebuttal`), and a rebuttal it cannot break is conceded explicitly.
4. Stop. A third round never happens — a dispute alive after two rounds is a dispute that must be settled by running the code, which is step 4's job, not by more argument.

Log the trace compactly, one line each:

```
CHARGE:  <id> <file:line> — <one line>
DEFENSE: <id> rebut|concede — <one line>
REPLY:   <id> hold|concede — <one line>
```

## 4. Adjudicate

You do this with the code open, treating both sides as witnesses, not judges.

- **Disputed and runnable → run it.** Write the failing case, execute it, and let the result decide. This is the whole reason the debate is bounded: argument is a candidate generator, execution is the verdict.
- **confirmed** — reproduced. Cite the evidence: failing command output, the line that proves it, the caller that breaks. Also mark `conceded-by-defender` when the defense already gave it up.
- **plausible** — a real risk you cannot execute here (needs production data, a race window, a device). Say what would settle it.
- **refuted** — one line on why the charge is wrong: guard exists at file:line, no caller can pass that value, the behavior is required by the contract. A defender's rebuttal you verified counts; a rebuttal you did not verify does not.

Rules:

- Never pass through a claim you did not check, from either side. "The challenger said so" and "the defender rebutted it" are equally worthless unverified.
- Style-only claims are dropped, reported as a count (`dropped: <n> style-only`), never expanded.
- Adjudication does not fix anything. Fixes happen after the report, on the user's call.

## 5. Report

```
CROSSCHECK REPORT
scope: <files>, <±lines> · rounds: <n> · charges: <n> — conceded by defender: <n> · withdrawn by challenger: <n>
confirmed: <n> · plausible: <n> · refuted: <n> · dropped: <n> style-only
```

followed by a table sorted worst-first:

| # | verdict | file:line | defect | debate | evidence / why refuted |

where `debate` is one of `conceded`, `withdrawn`, `disputed → ran it`, `undisputed`.

Then `FINAL:` — `ship` (nothing confirmed), `fix first` (confirmed defects listed), or `blocked` (debaters could not run; say what is missing). Zero confirmed findings is a legitimate result — say it plainly instead of promoting a plausible one to fill the table. Offer the follow-up as a choice: fix the confirmed set now, file the plausible ones, or accept and move on.

## Worked example (canonical — copy this format exactly)

Change: uncommitted diff adding a retry wrapper around the payments client.

CROSSCHECK: 3 files, +148/−12 — challenger vs defender, max 2 rounds

```
CHARGE:  c1 payments/retry.ts:41 — retries on any non-2xx, so a declined card is charge-attempted 3×
CHARGE:  c2 payments/retry.ts:58 — idempotency key regenerated per attempt, defeating upstream dedupe
CHARGE:  c3 payments/retry.ts:12 — no timeout, a hung upstream holds the request forever
CHARGE:  c4 payments/client.ts:77 — backoff without jitter synchronizes retries after an upstream blip
DEFENSE: c1 concede — retryable set is `status >= 400`; 402 is inside it, nothing excludes declines
DEFENSE: c2 rebut — key comes from the caller's order id
DEFENSE: c3 rebut — client.ts:22 sets a 10s default the wrapper inherits
DEFENSE: c4 rebut — upstream is single-tenant here, thundering herd needs many clients
REPLY:   c2 hold — key is rebuilt inside the loop at :58, caller value only seeds the first attempt
REPLY:   c3 concede — verified the inherited default, charge withdrawn
REPLY:   c4 hold — single-tenant is not stated in the constraints, and retries stack per request
```

Adjudication: c2 disputed → added a fake client asserting one key across attempts; it saw three distinct keys. c4 not runnable here.

```
CROSSCHECK REPORT
scope: 3 files, +148/−12 · rounds: 2 · charges: 4 — conceded by defender: 1 · withdrawn by challenger: 1
confirmed: 2 · plausible: 1 · refuted: 1 · dropped: 1 style-only
```

| # | verdict | file:line | defect | debate | evidence / why refuted |
|---|---|---|---|---|---|
| 1 | confirmed | payments/retry.ts:41 | declines retried as failures, card charge-attempted 3× | conceded | fake client returning 402: 3 POSTs observed |
| 2 | confirmed | payments/retry.ts:58 | idempotency key regenerated per attempt | disputed → ran it | 3 distinct keys across attempts; docs/payments.md requires one per logical charge |
| 3 | plausible | payments/client.ts:77 | no jitter in backoff | disputed → not runnable | needs load data to settle; cheap to add regardless |
| 4 | refuted | payments/retry.ts:12 | "no timeout" | withdrawn | client.ts:22 sets a 10s default the wrapper inherits |

FINAL: fix first — #1 and #2 before this ships.

## Output order (strict)

1. `CROSSCHECK:` scope line (or `nothing to review`)
2. Debate trace (`CHARGE` / `DEFENSE` / `REPLY`)
3. One line on what you ran to settle disputed charges
4. `CROSSCHECK REPORT` block
5. Findings table
6. `FINAL:` + the follow-up choice
