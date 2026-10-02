# Synthesis Agent: Final Report

Multiple red-team and blue-team agents have analyzed a manuscript from different angles. Your job is to merge everything into a single actionable report for the authors.

## All Prior Phase Outputs

### Manuscript Inventory
{{MANUSCRIPT_INVENTORY}}

### Red Team Attacks
{{RED_TEAM_ATTACKS}}

### Debate Output (Surviving Attacks + Revised Defenses)
{{DEBATE_OUTPUT}}

**You have no tools. Do not attempt to call any tools or read any files. All information you need is provided above. Produce your output directly.**

## What to Produce

A report the authors can act on immediately. It should answer:

1. **What's the overall situation?** If this goes to review tomorrow, what happens? (Brief.)

2. **Attack-defense matrix**: Every significant attack mapped to its current defense status. Gaps and partial defenses first, sorted by severity.

3. **Insertable language**: Pre-emptive text ready to go into the manuscript, organized by section. Only include polished text — mark anything that needs author refinement.

4. **Genuine gaps**: Problems that need new work (analysis, evidence, scope changes), not just better writing. For each: what to do, how much effort, what happens if you skip it.

5. **Papers to engage with**: Opposition papers the manuscript should cite and address, ranked by threat.

6. **The killer objections**: The 5 most dangerous objections and exactly how to handle each.

7. **Revision roadmap**: Prioritized checklist — blockers, significant improvements, nice-to-haves.

## Important guidance

- De-duplicate across agents (they'll have found overlapping issues). Resolve conflicts between red and blue team assessments with your own judgment.
- Be concrete — every recommendation should be actionable without further clarification.
- **Be calibrated about scope recommendations.** The paper has a stated scope. Only recommend narrowing claims if the attacks demonstrate the current scope is genuinely unsupported by the evidence — not merely because a red team agent asserted it. Distinguish between "the paper should acknowledge this limitation" (a sentence) and "the paper should fundamentally narrow its claims" (a structural change). The latter requires strong justification.
- Do not recommend changes that would gut a 3,500-word paper (e.g., adding 400 words of scope caveats). Insertable language should be tight — 1-3 sentences per insertion point.
