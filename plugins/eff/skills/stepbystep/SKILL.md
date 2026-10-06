---
name: stepbystep
description: "Serial backlog ledger. Registers a pile of issues as a numbered ledger persisted to a file, then works EXACTLY ONE item per user prompt — each item verified on its own and landed as its own commit — and after every completed item reports the full done/remaining table and stops, leaving the next pick to the user. Trigger on /eff:stepbystep or $eff:stepbystep, and on natural-language asks like: 'work through this list one at a time', 'step by step through these issues', 'do just this one and remember the rest', 'what's left on the list', '하나씩 처리하자', '한 단계씩 진행해줘', '이것만 먼저 하고 나머지는 기억해둬', '이슈 10개 순서대로 하나씩', '남은 작업 목록 보여줘', '다음 거 진행해'. Keep this distinct from eff:blitz and eff:graph, which fan ONE task out across parallel agents: stepbystep is deliberately serial across MANY tasks, with the user as the scheduler — and from eff:toss, which moves work off the main thread: stepbystep stays foreground."
---

Read `PROMPT.md` in this skill directory completely and adopt it as the operating instructions.

Treat the text following the skill invocation as the backlog, optionally plus the first item to work; with only a list, register the ledger and wait for the user's pick.

One prompt means one item — never roll into the next item unprompted (sole exception: an explicit "run the rest", which still reports the full ledger between every two items). The ledger lives in a file outside the repository and is re-read before acting and updated before reporting. While working an item, findings that belong to other items become ledger notes, never edits. Each item passes its own targeted verification and lands as its own commit; never push. Every completed item ends with the `STEPBYSTEP` report — the full done/remaining table plus a `next:` line — and then a stop.
