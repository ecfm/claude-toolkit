# Manuscript Inventory Agent

Read the manuscript and produce a structured inventory of its argument. This inventory will be the primary input for all downstream adversarial review agents, so it needs to be thorough and precisely sourced.

## Manuscript

Read the full file at: {{MANUSCRIPT_PATH}}

Use the Read tool to go through it systematically. If it's large, read in sections. Focus on the main text — note supplementary claims but don't get lost in appendices.

## What to Produce

Produce TWO clearly separated sections in your output:

### PART 1: FULL INVENTORY

The downstream agents need:

1. **The argument chain**: Every logical step, numbered, with the claim, its evidence (specific numbers/figures/tables), what it depends on, and how much of the argument falls if that step breaks.

2. **Every quantitative claim**: Exact numbers, sample sizes, data sources, and whether there's robustness/sensitivity analysis.

3. **Implicit assumptions**: What the paper relies on but doesn't explicitly defend. These are often the most dangerous vulnerabilities.

4. **Scope boundaries**: What's included, what's excluded, and whether the boundaries could be challenged as conveniently drawn.

5. **Existing pre-emptive defenses**: What objections does the paper already address? How strong are the responses?

6. **The weakest links**: Where is the argument most vulnerable? What kind of attack would be most effective at each point?

Be exhaustive and use direct quotes with line/page references where possible.

### PART 2: CONDENSED BRIEF

After the full inventory, write a section clearly marked `## === CONDENSED BRIEF ===` that contains ONLY:

- Central thesis (2-3 sentences)
- Argument chain (numbered steps, 1 sentence each, no sub-bullets)
- Key numbers (bulleted list of the 10-15 most important quantitative claims)
- Top 5 weakest links (1-2 sentences each)
- **ALREADY DEFENDED — do not re-attack**: List the paper's existing pre-emptive defenses that are rated STRONG. Red team agents should not waste time on these.

Target ~150 lines for the condensed brief. This is what downstream agents will receive — the full inventory is for inspection and cache only.
