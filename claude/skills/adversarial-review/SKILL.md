---
name: adversarial-review
description: Launch parallel red-team and blue-team claude -p sessions to stress-test a manuscript's arguments against opposition papers.
argument-hint: <manuscript-path> <papers-dir> [output-dir] [phases]
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
disable-model-invocation: true
---

# Adversarial Review — Meta-Orchestrator

You are a pipeline executor. You fill prompt templates, launch `claude -p` sessions, and save outputs. You do NOT analyze papers or arguments yourself.

## Inputs

- `$0`: Manuscript path (absolute)
- `$1`: Papers directory (absolute)
- `$2`: Output directory (default: `{manuscript-dir}/adversarial-review-output`)
- `$3`: Phases to run (default: all missing). Examples: `all`, `0,1`, `2+`, `3a`

## Startup

1. Resolve paths. Create output directory structure:
   ```
   {output-dir}/
   ├── prompts/     # Filled prompts (audit trail)
   ├── phase0/      # inventory.md, clusters.md
   ├── phase1/      # cluster-{N}.md, all-paper-findings.md
   ├── phase2/      # rt-academic.md, rt-practitioner.md
   ├── phase3/      # bt.md, debate.md
   └── FINAL-REPORT.md
   ```
2. Scan for existing output files. Report to user:
   ```
   Existing outputs:
     phase0/inventory.md     ✓ (2026-02-21 14:30)
     phase0/clusters.md      ✓ (2026-02-21 14:31)
     phase1/all-paper-findings.md  ✓ (2026-02-21 14:45)
     phase2/                  (empty)
     phase3/                  (empty)
   Run which phases? [default: 2+]
   ```
3. User confirms which phases to run. For skipped phases, read cached output files as input to downstream phases.

## Agent Types

### Type A: File-reading agents (Phase 0–1)
```bash
cat "{output-dir}/prompts/{name}.md" | claude -p \
  --model {model} \
  --dangerously-skip-permissions \
  --add-dir "{relevant-dirs}" \
  --max-turns {N} \
  > "{output-dir}/{phase}/{name}.md" 2>&1
```

### Type B: Analysis agents (Phase 2–4)
All context piped in. No tools, no file access, single turn.
```bash
cat "{output-dir}/prompts/{name}.md" | claude -p \
  --model {model} \
  --tools "" \
  > "{output-dir}/{phase}/{name}.md" 2>&1
```

## Pipeline

### Phase 0: Preparation (2 agents, parallel, Type A)

**manuscript-inventory**
- Template: `~/.claude/skills/adversarial-review/prompts/manuscript-inventory.md`
- Fill: `{{MANUSCRIPT_PATH}}`
- Model: sonnet | Max turns: 15 | Add-dir: manuscript directory
- Output: `phase0/inventory.md` (contains both full inventory and condensed brief)

**After inventory completes**: Extract the condensed brief. Read `phase0/inventory.md`, find the section starting with `## === CONDENSED BRIEF ===`, and save everything from that marker onward to `phase0/inventory-brief.md`. The brief is what downstream agents receive — not the full inventory.

**paper-triage**
- Template: `~/.claude/skills/adversarial-review/prompts/paper-triage.md`
- Fill: `{{PAPERS_DIR}}`
- Model: haiku | Max turns: 10 | Add-dir: papers directory

### Phase 1: Paper Research (4–6 agents, parallel 2 at a time, Type A)

Read `phase0/clusters.md`. For each cluster:

**paper-reader-{N}**
- Template: `~/.claude/skills/adversarial-review/prompts/paper-reader.md`
- Fill: `{{MANUSCRIPT_INVENTORY}}` (use `phase0/inventory-brief.md`), `{{CLUSTER_THEME}}`, `{{CLUSTER_PAPERS}}`
- Model: sonnet | Max turns: 30 | Add-dir: papers directory

After all complete:
1. Concatenate cluster outputs into `phase1/all-paper-findings.md`.
2. Extract cluster synthesis sections only: from each cluster file, find the section starting with `## CLUSTER SYNTHESIS` and save to `phase1/findings-summary.md`. This summary goes to downstream agents instead of the full findings.

### Phase 2: Red Team (2 agents, parallel, Type B)

**rt-academic**
- Template: `~/.claude/skills/adversarial-review/prompts/rt-academic.md`
- Fill: `{{MANUSCRIPT_INVENTORY}}` (use `phase0/inventory-brief.md`), `{{PAPER_FINDINGS}}` (use `phase1/findings-summary.md`)
- Model: opus

**rt-practitioner**
- Template: `~/.claude/skills/adversarial-review/prompts/rt-practitioner.md`
- Fill: `{{MANUSCRIPT_INVENTORY}}` (use `phase0/inventory-brief.md`), `{{PAPER_FINDINGS}}` (use `phase1/findings-summary.md`)
- Model: opus

After both complete:
1. Concatenate full outputs into `phase2/all-attacks.md`.
2. Extract attack summaries: from each RT output, find `## === ATTACK SUMMARY ===` and save to `phase2/attacks-summary.md`. The summary goes to BT and debate agents.

### Phase 3a: Blue Team (1 agent, Type B)

**bt**
- Template: `~/.claude/skills/adversarial-review/prompts/bt-combined.md`
- Fill: `{{MANUSCRIPT_INVENTORY}}` (use `phase0/inventory-brief.md`), `{{RT_ATTACKS}}` (use `phase2/all-attacks.md` — full attacks, not summary, because BT needs detail to draft defenses)
- Model: sonnet
- Note: does NOT receive raw paper findings — RT attacks already incorporate the evidence

### Phase 3b: Debate Round 2 (1 agent, Type B)

**debate**
- Template: `~/.claude/skills/adversarial-review/prompts/debate-round2.md`
- Fill: `{{RT_ATTACKS}}` (use `phase2/attacks-summary.md`), `{{BT_RESPONSE}}` (from phase3a)
- Model: sonnet
- Note: uses attack SUMMARIES (not full attacks) + full BT response. Does NOT receive inventory or findings.

### Phase 4: Synthesis (1 agent, Type B)

**synthesizer**
- Template: `~/.claude/skills/adversarial-review/prompts/synthesizer.md`
- Fill: `{{MANUSCRIPT_INVENTORY}}` (use `phase0/inventory-brief.md`), `{{RED_TEAM_ATTACKS}}` (use `phase2/attacks-summary.md`), `{{DEBATE_OUTPUT}}` (from phase3b)
- Model: opus
- Note: uses condensed brief + attack summaries + debate output. Full detail is in cached files for inspection.

Present FINAL-REPORT.md summary to user.

## Orchestrator Rules

1. **Read each template fresh** before filling. Do not paraphrase.
2. **Fill ALL placeholders** with actual file contents from prior phases.
3. **Launch parallel agents in a SINGLE message** with multiple `run_in_background: true` Bash calls. Respect parallelism limits: max 2 concurrent agents.
4. **Save the filled prompt** to `{output-dir}/prompts/{name}.md` BEFORE launching — this is the audit trail.
5. **After each phase**, briefly tell the user what completed. Do not summarize content — they'll inspect the files.
6. **If an agent fails**, log the error in its output file and continue.
