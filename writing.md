# Writing guide

One guide for every agent and every project. Part 1 applies to all chat replies.
Parts 2 to 4 apply when drafting or reviewing a document, such as a paper,
report, letter, or figure. A project may add its own rules (for example
`WRITING_RULES.md`); project rules take priority where they differ.

Merged on 2026-10-02 from the Claude "Writing Style" section, the Codex
`writing-guidance/` files (drafting, review, figures), and the general rules of
the Validation Dilemma `WRITING_RULES.md` (R-001, R-002, R-017, R-019, R-021,
R-022, which now point here).

## Part 1. Chat replies

Write in plain language by default.

- Short sentences. One idea per sentence.
- No jargon. If a technical term is needed, define it in plain words the first time.
- No figurative language. No metaphors, no analogies, no "lens", "lands", "carries", "punches above".
- No complex clauses. Avoid em-dash asides, nested subordinate clauses, and stacked qualifiers.
- Prefer a list over a long paragraph when there is more than one point.

This does not apply to code comments or to documents that must match a
surrounding house style.

## Part 2. Documents

Preserve meaning and necessary qualifications before shortening. When rules
compete: keep the meaning, fix confusion that matters, then shorten. Respect
text the author has protected and real length or format limits.

### Define terms

Define or describe, never just name. Define a term at its first use, in its own
sentence, or replace it with a plain description of what it is or does. Do not
coin a name for something the text uses only once. Introduce the concrete
concept before its technical label. Use an example when an essential term stays
abstract; do not add a second example unless the mechanism changes.

### Plain wording

Plain, complete wording. Split sentences that stack several clauses into
separate sentences or a short enumerated list ((i), (ii), (iii)). Use simple
connected sentences, not nested clauses or fragments that make readers rebuild
the relationships.

### Stable names

Use one name for one thing. If two expressions mean different things, make the
difference visible. Do not vary wording just to avoid repetition. Use parallel
wording for comparable conditions.

### Actor and action

Check each edited sentence for its actor, action, object, data source,
comparator, and claim scope. Say who acts, what information they have, and what
changes between conditions. The system, the researcher, and the model may each
do a different step.

### Pronouns and references

Resolve pronouns and abstract phrases without filling gaps by inference. Recheck
edited sentences against the described operation, including captions and figure
labels. Watch phrases such as "the procedure", "the argument", or "the model
selects".

### Procedures as steps

Describe a procedure as its steps in order, naming who does each step, instead
of compressing it into its result. Do not imply an order, cause, or dependency
that does not exist. For example, "before" and "after" imply a sequence that two
alternative setups do not have.

### Say it once

Do not repeat in a caption what the figure's legend or axis labels already show,
and do not add a sentence or paragraph that restates the preceding conclusion.
A summary must add an implication, a priority, or a connection. Keep
repetition only when a section must be read on its own.

### Structure

- Give the reader the full story at the right depth: the question, the setup,
  the comparison, the result, and what follows from it.
- Open with the main point. Do not announce the document's structure at length.
- Choose prose, a list, a table, or a diagram by the reader's task. Every table
  column should answer a clear question. A diagram must show a relationship that
  saves more text than the space it takes.

### Quantities

Name the measured quantity, the comparison, the denominator, the units, and the
direction when needed. Tell relative changes apart from percentage-point
changes. Check real word limits and the rendered layout.

### Evidence

Keep findings, interpretation, proposals, and decisions apart. Do not invent
certainty. Keep citations, assumptions, and uncertainty next to the claim they
support. Put workflow notes, review logs, and editing history in supporting
records, not in the reader-facing text.

## Part 3. Review and revise loops

Use this only when running or building a review-and-revise loop for prose.

- A readability reviewer stands in for the intended reader. For a blind review,
  give only the passage to be read; do not let source knowledge or author
  explanations fill the gaps.
- Section reviews are diagnostic. One editor reconciles all comments using the
  full draft, the sources, and the author's preferences. Each comment gets
  accept, adapt, or decline. Fix the underlying problem, not only the suggested
  remedy.
- Find the real obstacle: an unclear actor, referent, baseline, condition, order,
  or step from evidence to conclusion. Make the smallest repair that is enough,
  then reread the passage around it.
- Keep prose that is already clear, scientific qualifications, and protected
  author text. Do not write for every possible reviewer objection.
- Readability review is not fact checking. Tie each verdict to the version
  reviewed.
- When building a reusable harness: test on fixed inputs that include both
  confusing and already-clear passages, keep earlier outputs, and save the
  prompts, configuration, inputs, and replay steps.

## Part 4. Figures

- Start from what the reader should learn and whether a plot helps.
- The figure must support the document's actual argument, not a flattering
  subset.
- Limit how much the reader must parse at once.
- Titles, axes, and legends name the quantity plotted and the comparison made.
  Tell apart a prediction, a selection rule, and an observed outcome. Make the
  direction of improvement clear.
- Keep terms and notation the same as in the text and captions.
- Show uncertainty for what it measures. Tell confidence intervals apart from
  spread in the data. Do not invent precision.
- Check labels, units, signs, and the rendered layout.
