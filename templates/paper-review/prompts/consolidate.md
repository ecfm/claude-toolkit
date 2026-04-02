# Consolidate Review Findings

Read all review outputs in [REVIEWS_DIR] and produce a single consolidated
report with deduplicated, prioritized findings.

## For each finding across all tracks:

1. **Deduplicate**: If two tracks found the same issue, merge into one entry
   citing both tracks.
2. **Classify severity**:
   - **Must-fix**: A claim in the paper would be factually wrong or misleading
   - **Should-fix**: Methodology issue, disclosure gap, or unclear text
   - **Disclosed**: Known limitation, already acknowledged
3. **Group by type**: Number mismatches, train/test leakage, metric validity,
   argument gaps, clarity issues, missing analyses.

## Output format

```
## Executive Summary
[3-5 sentences: overall assessment]

## Must-Fix ([count])
1. [finding] — Tracks: [which tracks found it]

## Should-Fix ([count])
...

## Disclosed / Won't Fix ([count])
...

## Priority Action List
1. [most important fix]
2. [second most important]
...
```

Be concise. One line per finding for must-fix/should-fix. More detail only
for findings that need explanation.
