# Research Methodology Practices

Lessons for conducting research with AI agents — literature review, critical analysis,
and research direction planning. Complements experiment-practices.md (running experiments)
and pipeline-architecture.md (code architecture).

---

## 1. Agent Instruction Iteration

When designing agent tasks (lit review, paper extraction, analysis), iterate the
instructions before scaling:

1. **Design** the schema/instructions
2. **Test on 1 example** where you already know the answer
3. **Compare** agent output to ground truth — identify systematic errors
4. **Fix instructions** to address each error type
5. **Re-test** on the same example until clean
6. **Test on 2-3 diverse examples** (different paper types, domains)
7. **Then batch** the remaining work

Common instruction failure modes:
- Agent guesses when it should say "not_reported"
- Agent interpolates ranges instead of listing exact values
- Agent confuses what the paper does vs what the paper studies
- Agent defaults to a value instead of searching the paper text
- Temporal reasoning errors (paper A can't build on paper B if B is newer)

Each failure mode becomes an explicit rule in the instructions. The instructions
grow by accumulating specific fixes — not by adding general advice.

**Anti-pattern:** Writing perfect-sounding instructions once and launching 30 agents.
The first agent reveals 5 systematic errors, but you've already wasted 29 runs.

## 2. Structured Paper Extraction: Link Claims to Experiments

When extracting technical details from papers, the fundamental unit is the
**experiment**, not the paper. A paper is a collection of claims, each supported
by specific experiments.

Structure:
```
claims:
  - claim: "X achieves Y"
    evidence: [experiment_ids]
    caveats: "only tested on Z"

experiments:
  - id: "e1"
    models: [exact names]
    intervention: {type, target, layers, hyperparams}
    dataset: {name, origin, size}
    evaluation: {method, judge, criteria}
    result: "specific number"
    figure: "Figure 4a"
```

This prevents the common failure of citing a paper's claim without knowing:
- Which models it was tested on (generalizability)
- What evaluation method was used (teacher-forcing inflation?)
- How many seeds/runs (reliability)
- What the exact decision criteria were (reproducibility)

## 3. External Adversarial Review

Before committing to a research direction, send your analysis to a different
model/perspective for critique. The prompt should explicitly ask:

- "Where am I overconfident given the evidence?"
- "What logical errors or missed connections?"
- "Is this experiment design confounded?"
- "Does the experiment actually test the stated hypothesis?"

Key lesson: distinguish **sufficiency** from **mediation**. Showing that X
produces Y (sufficiency) is NOT the same as showing that interventions cause
Y *through* X (mediation). Mediation requires blocking X and showing Y
disappears while the intervention's intended effect remains. This distinction
is easy to miss when designing experiments.

## 4. Evidential Hierarchy

When building arguments across papers, classify each finding by evidential
strength before using it as a premise:

| Level | Meaning | Trust |
|-------|---------|-------|
| Analytically proven | Formal mathematical proof | High — check assumptions |
| Demonstrated empirically | Tested across models/datasets with controls | Medium-high — check generalizability |
| Suggested | Single-setting observation or limited testing | Medium — needs replication |
| Proposed | Theoretical framework without validation | Low — treat as hypothesis |

Do not build load-bearing arguments on "suggested" findings. If your core
claim depends on a single-setting preprint, flag this explicitly.

Also track:
- **Peer review status**: Published (ICML, NeurIPS) > preprint > withdrawn
- **Replication**: Tested on N model families > single model
- **Evaluation method**: Open-ended generation > teacher-forcing (the latter
  inflates results by up to 2.5x in model editing)

## 5. Cross-Paper Contradiction Detection

When synthesizing across papers, explicitly check for contradictions. Common
types:

- **Scope mismatch**: Paper A shows X at one layer, paper B shows ¬X at all
  layers. Not a real contradiction — different scope.
- **Metric mismatch**: Paper A measures success on direct recall, paper B on
  downstream consequences. Both can be "right" simultaneously.
- **Level mismatch**: Paper A works in weight space, paper B in activation space.
  These can give different answers because they're different projections of the
  same phenomenon.
- **Genuine contradiction**: Paper A and B measure the same thing on the same
  level and disagree. Resolve by checking sample size, evaluation method,
  and model family.

The most productive contradictions are ones where two papers make the SAME
measurement but get different results — these reveal hidden confounds or
boundary conditions.

## 6. Separate Description from Explanation

When reviewing a field, keep three levels distinct:

1. **What happens** (established facts): "Sequential editing causes norm growth"
2. **How it happens** (mechanisms): "The L&E update rule has exponential growth"
3. **Why it happens** (root causes): "Feature superposition makes perturbation non-local"

Most papers establish level 1 (empirical observation), some establish level 2
(specific mechanism), and very few establish level 3 (root cause). Do not
upgrade a level-1 finding to level-3 status because it sounds like an
explanation.

Test: could the finding be a symptom of something deeper? If yes, it's not a
root cause. "Norm growth causes editing collapse" could be true, but norm
growth might itself be a symptom of a deeper geometric property. Classify
accordingly.
