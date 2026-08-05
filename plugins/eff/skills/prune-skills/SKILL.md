---
name: prune-skills
description: "Unused-skill pruner. Measures ACTUAL usage from local session transcripts — how often each installed skill was invoked and each plugin's MCP/plugin tools were called over a time window — joins that with each plugin's always-on input-token cost, surfaces the never-used and rarely-used ones as removal candidates with evidence (last used, call counts, cost per session), and performs only the removals the user explicitly confirms (preferring reversible disable over uninstall). Trigger on /eff:prune-skills or $eff:prune-skills, and on natural-language asks like: 'which skills do I never use', 'prune unused skills', 'what plugins are dead weight', 'remove skills I don't use', '안 쓰는 스킬 찾아줘', '사용 안 하는 플러그인 정리해줘', '잘 안 쓰는 스킬 지워줘', '죽은 스킬 추려줘'. Keep this distinct from eff:dedupe-skills (removal by functional OVERLAP) and eff:update-skills (version bumps) — prune-skills removes by low USAGE."
---

Read `PROMPT.md` in this skill directory completely and adopt it as the operating instructions.

Usage numbers come from real transcript data — never estimate or guess a call count; a skill with unmeasurable usage is reported as `no data`, not as unused. No uninstall, disable, or file move without explicit per-item confirmation against the usage table. Always end a run that removed anything with the `PRUNE REPORT`.
