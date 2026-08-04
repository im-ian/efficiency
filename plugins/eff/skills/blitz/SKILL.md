---
name: blitz
description: "Force-parallel fork-merge orchestrator. Splits a task into parallel slices even when scopes overlap or conflicts are likely — overlap is treated as a merge problem, never a reason to serialize — then reconciles everything in a merge phase and enforces a mandatory verification gate (build, full tests, cross-slice integration checks, collision review, fresh-eyes review). Trigger on /eff:blitz or $eff:blitz, and on natural-language asks like: 'force parallel', 'parallelize anyway', 'ignore conflicts and run in parallel', 'fork first merge later', '충돌 무시하고 병렬로', '그냥 병렬로 돌려', '선작업 후 취합', '병렬로 먼저 하고 나중에 합쳐' — or whenever you are about to tell the user a task cannot be parallelized because of overlapping scope or conflict risk. Keep this distinct from eff:graph, which adaptively decides whether graph orchestration is warranted."
---

Read `PROMPT.md` in this skill directory completely and adopt it as the operating instructions.

Treat the text following the skill invocation as the task. Apply the go/no-go decision first; skip blitzing only when the task is smaller than the merge overhead. If the task contains `PLAN ONLY`, stop after the slice table and contract and do not execute.

Never respond that the task cannot be parallelized because scopes overlap or conflicts are likely. That objection is precisely what this skill overrides: slice, fan out, merge, and then verify. Never skip the final verification gate.
