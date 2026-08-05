---
name: update-skills
description: "Installed-skill version updater. Refreshes every marketplace, compares each installed plugin's version against the latest, previews a table (plugin, key updates, before → after version, estimated input-token delta), and only updates the set the user explicitly confirms. After updating it reminds that changes apply from the NEXT session, and lists every failed update with the verbatim error and a likely cause. Trigger on /eff:update-skills or $eff:update-skills, and on natural-language asks like: 'update my skills', 'update installed plugins', 'are my skills up to date', 'bump my plugins to latest', '스킬 업데이트 해줘', '설치된 스킬 최신으로 맞춰줘', '플러그인 버전 올려줘', '스킬 최신인지 확인해줘'. Keep this distinct from eff:dedupe-skills, which finds overlapping/redundant skills and helps remove them — update-skills only moves versions forward."
---

Read `PROMPT.md` in this skill directory completely and adopt it as the operating instructions.

Never run an update the user has not explicitly confirmed against the preview table. Never claim an update takes effect in the current session — updated plugins load from the next session. Always end a run that executed updates with the `UPDATE REPORT`, including the failed list with verbatim errors.
