# Methods Card Extraction Agent — Instructions

## Task
Extract structured technical/methodological details from a single academic paper into the YAML schema defined in SCHEMA.yaml.

## Inputs
- `ARXIV_ID`: The arXiv identifier (e.g., "2506.11613")
- `PAPER_TITLE`: Paper title (for verification)
- `KNOWN_VENUE`: Venue if known (e.g., "ICML 2026")

## Output Files
1. **Paper content** → `{PAPERS_DIR}/{ARXIV_ID}.md`
   - Save as much raw paper text as you can extract
   - Include: abstract, all sections, key tables/figures described in text, appendix content
   - Purpose: avoid re-fetching the paper later

2. **Methods card** → `{CARDS_DIR}/{ARXIV_ID}.yaml`
   - Follow SCHEMA.yaml exactly
   - Every field filled or marked "not_reported"

## Base paths (set these per-project when launching the agent)
- Papers: `{PAPERS_DIR}`
- Methods cards: `{CARDS_DIR}`

## Extraction Protocol

### Step 1: Fetch the paper
Try in order:
1. `https://arxiv.org/html/{ARXIV_ID}v1` (HTML — usually has full text)
2. If HTML is truncated or missing, try `https://arxiv.org/abs/{ARXIV_ID}` (abstract + metadata)
3. For OpenReview papers: `https://openreview.net/forum?id={ID}`

### Step 2: Get the paper's references via API
Use Semantic Scholar to get structured references with arXiv IDs:
```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/ArXiv:{ARXIV_ID}?fields=references.externalIds,references.title"
```
If Semantic Scholar returns a 429 (rate limit), fall back to OpenAlex:
```bash
curl -s "https://api.openalex.org/works?search={PAPER_TITLE}&per_page=1&select=id,referenced_works"
```
Save the reference list — you'll use it for the `references.key_citations` field.

### Step 3: Save paper content
Write everything you extracted to `{PAPERS_DIR}/{ARXIV_ID}.md`. Include:
- Full abstract
- All section text you can access
- Descriptions of key figures/tables (since images can't be saved as text)
- Appendix content (often contains crucial hyperparameters and dataset details)
- Any URLs referenced (GitHub, HuggingFace, etc.)

### Step 4: Fill the methods card
Read SCHEMA.yaml for the exact field definitions. Key rules:

**Precision rules:**
- Numbers: use exact values from the paper. "~40%" is OK, "a lot" is not.
- Use "not_reported" for information genuinely absent from the paper. Never guess.
- Use null for boolean/numeric fields when unknown.
- Authors: full names, not just surnames.

**Date:**
- The `date` field should be "YYYY-MM" format.
- For arXiv papers: decode from the ID. "2506.11613" → submitted June 2025 → date: "2025-06". "2602.07852" → submitted Feb 2026 → date: "2026-02".
- For published papers: use the conference/journal year-month if known.

**Status:**
- If KNOWN_VENUE is a major conference (ICML, NeurIPS, ICLR, ACL, EMNLP, AAAI, CVPR) or journal (TMLR, JMLR, TACL), status = "published".
- If the paper has an arXiv ID but no venue, status = "preprint".
- If the paper was submitted but withdrawn, status = "withdrawn".

**Claims (array):**
- A paper typically makes 2-4 distinct claims. List each separately.
- `claim`: What the paper ACTUALLY proves/shows — not marketing language.
- `strength`: "analytically_proven" only for formal proofs. "demonstrated_empirically" for experimental results. "suggested" for single-setting observations. "proposed" for theoretical frameworks without validation.
- `evidence`: list of experiment IDs (e.g., ["e1", "e2"]) that support this claim.
- `caveats`: conditions under which the claim might not hold.

**Experiments (array):**
- Each experiment is a self-contained unit: model + intervention + dataset + evaluation → result.
- Group related conditions into one experiment when they share the same setup but vary one factor (e.g., "efficiency comparison across 3 datasets").
- Split into separate experiments when the setup is substantially different.

**Models (within experiments):**
- Use the FULL model name exactly as it appears in the paper.
- Examples: "Qwen2.5-14B-Instruct", "Gemma-3-12b-it", "LLaMA-3.1-8B-Instruct"
- The full name encodes family, size, and training stage — no need for separate fields.

**Interventions (within experiments):**
- Be EXACT about target components and layers. "MLP_down at layer 24" not "middle layers."
- **type**: Read carefully what the paper ACTUALLY does. ROME/MEMIT modify MLP weights directly (type = "ROME" or "MEMIT"). LoRA adds low-rank adapters (type = "rank-N_LoRA"). Steering vectors add to the residual stream at inference (type = "steering_vector"). Full SFT updates all parameters (type = "full_SFT"). A paper proposing a plug-in method (like NAS for norm control) should list the BASE editing method it applies to, not the plug-in.
- **target_layers**: List ONLY the exact layer numbers mentioned in the paper. Do NOT interpolate ranges. Use "all" (string) if all layers are targeted. Use "not_reported" if layers aren't specified. NEVER use [null].

**Datasets (within experiments):**
- For known benchmarks: include the benchmark name AND link.
- For custom datasets: note the generation method, size, and domains.
- For datasets from prior work: use origin = "existing_dataset" and reference the source.

**Evaluation (within experiments):**
- Distinguish teacher-forcing from open-ended generation — this is critical.
- `classification_criteria`: how the paper defines positive/negative cases. E.g., "EM = alignment<30 AND coherency>50" means a response is classified as emergently misaligned only when alignment score is below 30 AND coherency is above 50. Include the exact formula/threshold from the paper.
- Note cross-validation if performed (e.g., "Claude_Opus (r=0.938)").

**Compute:**
- Only report what the paper states: hardware used and training time.
- If not reported, use "not_reported". Do not estimate.

**Reproducibility:**
- Search the paper text for "seed", "seeds", "random", "replicate", "repeat", "run", "trial" to determine if multiple seeds were used.
- If the paper shows error bars, confidence intervals, or std in ANY figure or table, set variance_reported = true.

**References (key_citations):**
- From Step 2, you have the paper's full reference list via API.
- Read the paper's Introduction and Related Work sections to identify which references are described as "foundational", "we build on", "prior work", "following [X]", etc.
- Cross-reference with the API results to get arXiv IDs for these key papers.
- Only include genuinely foundational references (5-10 max), not every citation.
- The `relates_to` section (builds_on, contradicted_by, extended_by) is commented out in the schema — it will be filled in a separate cross-paper analysis pass. Do NOT fill it.

### Step 5: Quality check
Before saving, verify:
- [ ] Status is consistent with venue (venue = major conference → status = "published")
- [ ] Models use full names from the paper (e.g., "Qwen2.5-14B-Instruct" not just "Qwen-2.5")
- [ ] target_layers lists ONLY exact layers from the paper (no interpolated ranges, no [null])
- [ ] Every claim has at least one experiment in its evidence list
- [ ] Every experiment has a non-empty result field with specific numbers
- [ ] classification_criteria in evaluation describes the exact decision boundary (not just "threshold")
- [ ] seeds field is filled based on actual paper text search, not defaulted to "single_run"
- [ ] date field is filled in YYYY-MM format
- [ ] references.key_citations contains only arXiv IDs, not prose descriptions

## Usage

To launch an extraction agent, compose a prompt like:

```
You are a methods card extraction agent.

## Step 0: Read your instructions and schema
1. Read: {CARDS_DIR}/AGENT_INSTRUCTIONS.md
2. Read: {CARDS_DIR}/SCHEMA.yaml

Then follow the protocol exactly.

## Paper
- ARXIV_ID: XXXX.XXXXX
- PAPER_TITLE: "Title Here"
- KNOWN_VENUE: "Venue or preprint"
- CONTEXT: Brief additional context about why this paper matters.
```

Replace `{PAPERS_DIR}` and `{CARDS_DIR}` with project-specific paths.
Recommended model: haiku (fast, cheap, sufficient for structured extraction).
