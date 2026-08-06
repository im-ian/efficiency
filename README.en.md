# Efficiency

[한국어](README.md) | **English**

Focused agent workflows for doing complex work faster without weakening verification. Not a feature list someone imagined — each skill hardened a friction point hit repeatedly during daily agent work. One `eff` plugin installs independent skills for Claude Code and Codex.

## Skills

| Skill | Purpose |
| --- | --- |
| `eff:graph` | Decide between prompt, loop, and graph execution; when a graph is warranted, orchestrate a validated DAG of agent, validator, merge, and human nodes. |
| `eff:blitz` | Force overlapping work into isolated parallel slices, merge by intent, and pass a mandatory verification gate. |
| `eff:toss` | Hand the current work-in-progress to a background subagent and stay free for anything else; close out with elapsed time, token usage, and a work summary. |
| `eff:race` | Run the same problem through competing approaches in isolated lanes, score them with a judge against a rubric fixed before any lane runs, adopt one winner, graft only the loser ideas that survive the rubric, and pass a verification gate. |
| `eff:bigpicture` | Trace the whole flow — path, callers, duplicates, contracts — before editing anything, decide whether the change belongs where the symptom appeared or at the one place every path crosses, bound the answer to evidence that exists today, stop for approval before the diff grows past what was asked, and prove the result with a test the narrow patch would have failed. |
| `eff:crosscheck` | Debate a change with two fresh subagents — challenger vs defender, given the goal and constraints but not the author's rationale — over at most two rounds, then settle what is still disputed by running it and report only adjudicated findings. |
| `eff:limit` | Fix a ceiling (tokens, subagents, wall-clock, rounds) before fan-out, reserve what verification and reporting will need, measure real spend instead of estimating, decline to start any unit that would breach it, and stop with a raise / narrow / end choice. |
| `eff:update-skills` | Check installed skills for newer versions, preview key updates, before → after versions, and estimated input-token delta in a table, then update only the confirmed set; failed updates are reported with verbatim errors. |
| `eff:dedupe-skills` | Find overlapping skills — duplicates, trigger collisions, behavioral conflicts, redundant token cost — with quoted evidence, recommend keeps/removals, and execute only confirmed ones (disable preferred). |
| `eff:prune-skills` | Measure actual skill and plugin-tool usage from session transcripts, surface never-used and rarely-used ones with evidence, and remove only confirmed ones (disable preferred). |

The skills share an installation namespace but keep separate prompts, triggers, and operating contracts.

## Install

### Claude Code

Run in a Claude Code session:

```text
/plugin marketplace add im-ian/efficiency
/plugin install eff@efficiency
```

Then invoke:

```text
/eff:<skill> <task>    # e.g. /eff:graph <task>
```

### Codex

Run in a terminal:

```bash
codex plugin marketplace add im-ian/efficiency
codex plugin add eff@efficiency
```

Start a new session, then invoke:

```text
$eff:<skill> <task>    # e.g. $eff:graph <task>
```

## License

MIT
