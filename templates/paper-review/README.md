# Paper Review Templates

Multi-layer verification system for empirical research papers before submission.
See `research-methodology.md` Section 8 for the full methodology.

## Structure

```
paper-review/
├── project_config.yaml        # Fill this with your paper's details
├── fill_templates.py          # Generates ready-to-use prompts from config
├── launch.py                  # Async Python orchestrator with timeout/retry
├── phase0/
│   ├── check_numbers.py       # Number reconciliation (provenance → tex → source)
│   └── check_staleness.py     # Output freshness detection (script hash → output hash)
└── prompts/                   # Templates with [PLACEHOLDER] markers
    ├── E_execute.md            # Execute & verify
    ├── M1_metric_validity.md   # Metric validity
    ├── M2_train_test.md        # Train/test integrity
    ├── M3_statistical.md       # Statistical claims
    ├── A1_break_argument.md    # Break the main argument
    ├── A2_baseline_fairness.md # Comparison fairness
    ├── A3_missing_analyses.md  # Missing analyses (reviewer simulation)
    ├── naive_reader.md         # First-time comprehension test
    ├── citation_verify.md      # Attribution accuracy
    └── consolidate.md          # Merge + deduplicate all findings
```

## Usage

### 1. Copy and configure
```bash
cp -r templates/paper-review/ my-paper/review/
cd my-paper/review/
# Edit project_config.yaml with your paper's paths, claims, metrics, etc.
```

### 2. Generate prompts from config
```bash
python fill_templates.py project_config.yaml
python fill_templates.py project_config.yaml --inject-known  # prepend known fixes
python fill_templates.py project_config.yaml --tracks E1,M1,A1  # subset
python fill_templates.py project_config.yaml --list  # show available tracks
```

### 3. Run Phase 0 (free, instant, deterministic)
```bash
python phase0/check_staleness.py      # are outputs fresh?
python phase0/check_numbers.py        # do numbers match sources?
```

### 4. Run LLM reviews
```bash
python launch.py --parallel 2 --layer exec
python launch.py --parallel 2 --layer method
python launch.py --parallel 2 --layer adversarial
python launch.py --tracks naive_reader,citation_verify
```

### 5. Consolidate findings
```bash
# Run consolidation agent on all review outputs
python launch.py --tracks consolidate
```

### 6. Fix issues, then re-verify
```bash
python phase0/check_numbers.py        # confirm 0 mismatches
python phase0/check_staleness.py --update-hashes  # record new baseline
```

## Model Selection

| Track type | Recommended model | Why |
|-----------|-------------------|-----|
| Execute (E) | Codex/GPT-5.4 | Needs tool access for code execution |
| Methodology (M) | Claude Opus | Deep multi-file reasoning |
| Adversarial (A) | Claude Opus | Creative argument construction |
| Naive reader | Any fresh model | Must not have seen the paper before |
| Citation verify | Sonnet + web search | Needs to look up papers |
