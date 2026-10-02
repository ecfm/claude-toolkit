# Adversarial Review Output Format

## Directory Structure After Completion

```
{output-dir}/
├── prompts/                          # Audit trail — exact prompts sent to each agent
│   ├── manuscript-inventory.md
│   ├── paper-triage.md
│   ├── paper-reader-1.md
│   ├── paper-reader-2.md
│   ├── ...
│   ├── rt-logic.md
│   ├── rt-empirical.md
│   ├── rt-scope.md
│   ├── rt-plausible.md
│   ├── bt-preempt.md
│   ├── bt-gaps.md
│   └── synthesizer.md
├── phase0/
│   ├── inventory.md                  # Structured inventory of manuscript's argument
│   └── clusters.md                   # Paper clusters for Phase 1
├── phase1/
│   ├── cluster-1.md                  # Findings from each paper cluster
│   ├── cluster-2.md
│   ├── ...
│   └── all-paper-findings.md         # Merged findings
├── phase2/
│   ├── rt-logic.md                   # Logical structure attacks
│   ├── rt-empirical.md               # Empirical evidence attacks
│   ├── rt-scope.md                   # Scope and framing attacks
│   ├── rt-plausible.md               # Plausible-sounding objections
│   └── all-attacks.md                # Merged attacks
├── phase3/
│   ├── bt-preempt.md                 # Pre-emptive rebuttals
│   └── bt-gaps.md                    # Genuine vulnerabilities
└── FINAL-REPORT.md                   # Synthesized final report
```

## Key Properties

- **Reproducible**: The `prompts/` directory contains every prompt sent to every agent. Re-running with the same prompts should produce similar (not identical) results.
- **Traceable**: Every claim in the FINAL-REPORT can be traced back through phase outputs to specific agent analyses.
- **Incremental**: Each phase's output is saved before the next phase starts. If the workflow is interrupted, completed phases are preserved.
- **Budget-aware**: Approximate costs per run:
  - Phase 0: ~$1.25 (1 opus + 1 haiku)
  - Phase 1: ~$8-12 (4-6 sonnet agents reading PDFs)
  - Phase 2: ~$8 (4 opus agents)
  - Phase 3: ~$4 (2 opus agents)
  - Phase 4: ~$2 (1 opus agent)
  - **Total**: ~$23-27 per full run
