---
name: dedupe-skills
description: "Overlapping-skill auditor. Sweeps every installed skill surface (plugins, personal and project skills), clusters skills that do the same job, collide on triggers, contradict each other when both active, or burn always-on input tokens redundantly — then recommends which to keep and which to remove, and performs only the removals the user explicitly confirms (preferring reversible disable over uninstall). Trigger on /eff:dedupe-skills or $eff:dedupe-skills, and on natural-language asks like: 'find duplicate skills', 'which of my skills overlap', 'my skills conflict with each other', 'clean up redundant skills', '겹치는 스킬 찾아줘', '중복 스킬 정리해줘', '스킬끼리 충돌하는 것 같아', '비슷한 스킬 추려줘'. Keep this distinct from eff:update-skills (version bumps only) and eff:prune-skills (removal by low USAGE) — dedupe-skills removes by functional OVERLAP."
---

Read `PROMPT.md` in this skill directory completely and adopt it as the operating instructions.

Analysis is free; removal never is — no uninstall, disable, or file move without explicit per-item confirmation against the cluster table. Every overlap claim must quote the actual colliding description text; never flag on vibes. Always end a run that removed anything with the `DEDUPE REPORT`.
