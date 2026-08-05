# Efficiency

[한국어](README.md) | **English**

Focused agent workflows for doing complex work faster without weakening verification. One `eff` plugin installs independent skills for Claude Code and Codex.

## Why these exist

Not a feature list someone imagined. Each skill hardened a friction point hit repeatedly during daily agent work.

- **`graph`** — Improvising the breakdown of a large task every time meant verification steps got dropped and ordering drifted. This pins the structure before execution starts.
- **`blitz`** — "These files overlap, so this can't be parallelized" came up far too often. Overlap is a merge problem, not a parallelization blocker: fork first, merge later, then prove it with a gate.
- **`toss`** — One long-running task shouldn't hold the whole session hostage. Hand it to a background agent and keep the main thread working.
- **`update-skills`** — Installed skills quietly went stale because nothing surfaced when updates shipped. Preview version, changelog, and token delta in a table, then update only what's confirmed.
- **`dedupe-skills`** — Accumulated skills started stealing each other's triggers and pushing contradictory instructions. Find the overlap with quoted evidence and help clean it up.
- **`prune-skills`** — Install-and-forget skills were burning always-on tokens every session. Measure real usage from transcripts and cull the dead weight.

## Skills

| Skill | Purpose |
| --- | --- |
| `eff:graph` | Decide between prompt, loop, and graph execution; when a graph is warranted, orchestrate a validated DAG of agent, validator, merge, and human nodes. |
| `eff:blitz` | Force overlapping work into isolated parallel slices, merge by intent, and pass a mandatory verification gate. |
| `eff:toss` | Hand the current work-in-progress to a background subagent and stay free for anything else; close out with elapsed time, token usage, and a work summary. |
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
/eff:graph <task>
/eff:blitz <task>
/eff:toss <task>
/eff:update-skills
/eff:dedupe-skills
/eff:prune-skills
```

### Codex

Run in a terminal:

```bash
codex plugin marketplace add im-ian/efficiency
codex plugin add eff@efficiency
```

Start a new session, then invoke:

```text
$eff:graph <task>
$eff:blitz <task>
$eff:toss <task>
$eff:update-skills
$eff:dedupe-skills
$eff:prune-skills
```

## License

MIT
