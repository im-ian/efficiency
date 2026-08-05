---
name: toss
description: "Background handoff orchestrator. Packages the current work-in-progress into a self-contained brief, hands it to a background subagent, and immediately frees the main agent for any other work. The background agent reports back when finished; on completion or an explicit user stop the toss session is closed with elapsed time, token usage, and a work summary. Trigger on /eff:toss or $eff:toss, and on natural-language asks like: 'toss this', 'hand this off', 'finish this in the background', 'keep this running while we do something else', '이거 백그라운드로 넘겨', '백그라운드에서 마저 해줘', '토스해줘', '이건 서브 에이전트한테 맡기고 다른 거 하자'. Keep this distinct from eff:blitz (force-parallel slices of one task) and eff:graph (multi-node work graphs): toss moves ONE stream of work off the main thread."
---

Read `PROMPT.md` in this skill directory completely and adopt it as the operating instructions.

Treat the text following the skill invocation as the task to toss; with no text, toss the current work-in-progress. After spawning, immediately return control to the user — never wait on, poll, or narrate the background agent. Close a toss only on its completion report or an explicit user stop, and always finish with the `TOSS REPORT` (elapsed time, tokens, summary).
