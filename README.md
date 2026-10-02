# ML/LLM Best Practices

Shared knowledge base for ML experiment workflows. Synced across servers via Git
and loaded into Claude Code sessions automatically.

## Contents

- **[experiment-practices.md](experiment-practices.md)** — Output structure, logging,
  diagnostics, monitoring, run ordering, early stopping, vLLM optimization. Read this
  before running or planning ML experiments.

- **[pipeline-architecture.md](pipeline-architecture.md)** — Modular pipeline design,
  type contracts, config management, stage caching. Read this when designing a new
  pipeline or adding a new method.

- **[research-methodology.md](research-methodology.md)** — Agent instruction iteration,
  structured paper extraction, external adversarial review, evidential hierarchy,
  contradiction detection. Read this when conducting literature review or planning
  research directions with AI agents.

- **[templates/paper-cards/](templates/paper-cards/)** — Reusable YAML schema and
  agent instructions for extracting structured methods cards from academic papers.
  Links claims to specific experiments with full provenance (models, datasets,
  evaluation methods, hyperparams).

- **[templates/lit-review/](templates/lit-review/)** — Multi-agent deep literature
  review skill. Orchestration loop with iterative follow-up, citation graph traversal
  (OpenAlex/Semantic Scholar), convergence-based stopping, and tiered reading.
  Includes search agent protocol, state tracking, and report templates.

## What Gets Synced

```
AGENTS.md                  → ~/.codex/AGENTS.md           # Global instructions, all agents
writing.md                 (read on demand)               # Writing guide, all agents
claude/
├── CLAUDE.md              → ~/.claude/CLAUDE.md          # Imports AGENTS.md + Claude-only notes
├── settings.json          (copied, not linked)           # Hooks, theme, status line
├── commands/*.md          → ~/.claude/commands/          # Slash commands
├── agents/*.md            → ~/.claude/agents/            # Subagents
└── skills/*/              → ~/.claude/skills/            # Skills
```

Guides read on demand (see the table in `AGENTS.md`): `writing.md`,
`experiment-practices.md`, `pipeline-architecture.md`, `research-methodology.md`,
`report-writing.md`, `agent-design.md`.

## Setup

```bash
git clone git@github.com:ecfm/claude-toolkit.git ~/Mao/claude-toolkit
bash ~/Mao/claude-toolkit/install.sh
```

This symlinks the instruction files, commands, agents, and skills so every Claude
Code and Codex session inherits them. `settings.json` is copied only if none exists,
because each machine keeps its own local settings.

## Usage

- `AGENTS.md` is the one global instruction file. Claude Code loads it through
  the import in `claude/CLAUDE.md`; Codex loads it through `~/.codex/AGENTS.md`.
- Use `/sync-learnings` at end of session to commit and push new learnings
- `runs.yaml` in each project repo tracks run stability (see experiment-practices.md
  section 11)
