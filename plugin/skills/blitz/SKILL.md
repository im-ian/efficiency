---
name: blitz
description: "Force-parallel fork-merge orchestrator. Splits a task into parallel slices even when scopes overlap or conflicts are likely — overlap is treated as a merge problem, never a reason to serialize — then reconciles everything in a merge phase and enforces a mandatory verification gate (build, full tests, cross-slice integration checks, collision review, fresh-eyes review). Trigger on /blitz or $blitz, and on natural-language asks like: 'force parallel', 'parallelize anyway', 'ignore conflicts and run in parallel', 'fork first merge later', '충돌 무시하고 병렬로', '그냥 병렬로 돌려', '선작업 후 취합', '병렬로 먼저 하고 나중에 합쳐' — or whenever you are about to tell the user a task cannot be parallelized because of overlapping scope or conflict risk."
---

Read the file `PROMPT.md` located in the same directory as this SKILL.md and adopt its entire contents as your operating instructions.

The text following the skill invocation is the task. Apply the go/no-go decision first; only skip blitzing when the task is smaller than the merge overhead. If the task contains "PLAN ONLY", stop after the slice table and contract — do not execute.

Hard rule: never respond that the task "cannot be parallelized due to overlapping scope or conflict risk". That objection is precisely what this skill exists to override — slice, fan out, merge, then verify. The verification gate at the end is mandatory and may never be skipped.
