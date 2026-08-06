---
name: race
description: "Competitive multi-attempt orchestrator. Runs the SAME problem through 2–4 deliberately different approaches in isolated lanes at once, scores them with a judge that wrote no lane against a rubric fixed BEFORE the results were seen, adopts the winner, grafts the surviving ideas from the losers, and passes a mandatory verification gate. Trigger on /eff:race or $eff:race, and on natural-language asks like: 'try a few approaches', 'compare implementations', 'which approach is better', 'we already tried and it failed, try something else', 'best of N', 'race a few solutions', '여러 방법으로 시도해봐', '접근법 몇 개 비교해줘', '어떤 방식이 나은지 붙여봐', '이 방법 실패했으니 다른 방식으로', '여러 안 만들어서 제일 나은 걸로' — or whenever a single attempt has already failed and the next move is a different approach rather than another retry of the same one. Keep this distinct from eff:blitz, which SPLITS one task into complementary slices that all get merged: race DUPLICATES one task across competing attempts and keeps exactly one."
---

Read `PROMPT.md` in this skill directory completely and adopt it as the operating instructions.

Treat the text following the skill invocation as the problem to race. Apply the go/no-go decision first; racing costs N times one attempt, so skip it when a single approach is obviously correct. If the request contains `PLAN ONLY`, stop after the rubric and lane table and do not execute.

Fix the rubric before any lane runs and never edit it after seeing results — a rubric written to fit a winner is not a rubric. The judge must be an agent or pass that wrote no lane, must disqualify on hard constraints before scoring anything else, and must never write code. Losing lanes are deleted, not half-merged: graft only specific ideas that survive the rubric, never blend two approaches. Never skip the final verification gate, and always end with the `RACE REPORT`.
