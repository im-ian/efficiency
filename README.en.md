# Efficiency

[한국어](README.md) | **English**

Focused agent workflows for doing complex work faster without weakening verification. One `eff` plugin installs independent skills for Claude Code and Codex.

## Why these exist

Not a feature list someone imagined. Each skill hardened a friction point hit repeatedly during daily agent work.

- **`graph`** — Improvising the breakdown of a large task every time meant verification steps got dropped and ordering drifted. This pins the structure before execution starts.
- **`blitz`** — "These files overlap, so this can't be parallelized" came up far too often. Overlap is a merge problem, not a parallelization blocker: fork first, merge later, then prove it with a gate.
- **`toss`** — One long-running task shouldn't hold the whole session hostage. Hand it to a background agent and keep the main thread working.

## Skills

| Skill | Purpose |
| --- | --- |
| `eff:graph` | Decide between prompt, loop, and graph execution; when a graph is warranted, orchestrate a validated DAG of agent, validator, merge, and human nodes. |
| `eff:blitz` | Force overlapping work into isolated parallel slices, merge by intent, and pass a mandatory verification gate. |
| `eff:toss` | Hand the current work-in-progress to a background subagent and stay free for anything else; close out with elapsed time, token usage, and a work summary. |

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
```

## License

MIT
