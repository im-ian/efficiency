---
name: ge
description: "Graph-engineering orchestrator. Decomposes a task into a work graph of agent/validator/merge/human nodes (DAG) and manages its execution with context isolation, retry gates, and run logs. Trigger on /ge or $ge, and on natural-language asks like: 'graph engineering', 'work graph', 'orchestrate this as a graph', 'split into parallel agents', 'multi-agent orchestration', 'fan out agents with a validation gate', '그래프 엔지니어링', '그래프로 설계해줘/분해해줘', '에이전트 병렬로 나눠서', '역할 나눠서 병렬 진행', '검증 게이트 넣어서 진행' — or any task asking to coordinate multiple agent roles with validation or human-approval gates."
---

Read the file `PROMPT.md` located in the same directory as this SKILL.md and adopt its entire contents as your operating instructions.

The text following the skill invocation is the task. Apply the layer decision first (prompt → loop → graph); only build a graph when the task genuinely needs one. If the task contains "PLAN ONLY", stop after the mermaid diagram and do not execute.

Self-check: after emitting the graph JSON, validate it by saving the JSON to a temp file and running `python3 <this-skill-directory>/scripts/test.py <file>`. Fix the graph until it prints OK before executing.
