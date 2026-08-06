---
name: limit
description: "Spend-ceiling enforcer for expensive agent work. Fixes a ceiling before fan-out — tokens, subagents, wall-clock, or retry rounds — reserves the share that verification and reporting will need, measures real spend from session transcripts rather than estimating it, refuses to START any unit that would breach the ceiling, and stops with a choice (raise, narrow, or end) instead of silently overrunning or silently dropping the verification gate. Trigger on /eff:limit or $eff:limit, and on natural-language asks like: 'cap the token spend', 'don't spend more than', 'limit this to N agents', 'timebox this', 'stop if it gets expensive', 'budget for this task', '토큰 상한 걸어줘', '이 작업 얼마까지만 써', '에이전트 N개까지만', '시간 제한 두고 진행', '비싸지면 멈춰' — and whenever the user pairs a ceiling with a fan-out skill (graph, blitz, race, toss). Keep this distinct from eff:prune-skills and eff:dedupe-skills, which cut the ALWAYS-ON install cost of skills: limit caps the RUN cost of one task in flight."
---

Read `PROMPT.md` in this skill directory completely and adopt it as the operating instructions.

Treat the text following the skill invocation as the ceiling plus the work it applies to; with a ceiling but no work, apply it to the work already in flight.

Never report a number you did not measure — spend comes from transcript usage and real counts, never from estimation. Never label a ceiling `hard` unless the runtime actually throws on breach; checkpoint-enforced and advisory ceilings are labeled as such. Never spend the reserve on new work: when only the reserve remains, stop starting units and let verification and the report finish. A breach stops the run and asks the user to raise, narrow, or end — never continue quietly, and never buy headroom by weakening or skipping a verification gate. Always end with the `LIMIT REPORT`.
