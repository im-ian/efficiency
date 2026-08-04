# Efficiency

Focused agent workflows for doing complex work faster without weakening verification. One `eff` plugin installs independent skills for Claude Code and Codex.

## Skills

| Skill | Purpose |
| --- | --- |
| `eff:graph` | Decide between prompt, loop, and graph execution; when a graph is warranted, orchestrate a validated DAG of agent, validator, merge, and human nodes. |
| `eff:blitz` | Force overlapping work into isolated parallel slices, merge by intent, and pass a mandatory verification gate. |

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
```

## Repository structure

```text
.claude-plugin/marketplace.json   # Claude Code marketplace
.agents/plugins/marketplace.json # Codex marketplace
plugins/eff/                     # Shared plugin package
└── skills/
    ├── graph/
    └── blitz/
```

## Development

Validate the package before publishing:

```bash
claude plugin validate .
uv run --with pyyaml python ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/eff
uv run --with pyyaml python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/eff/skills/graph
uv run --with pyyaml python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/eff/skills/blitz
```

## License

MIT
