"""
Prompt templates for the verify-citations workflow.

Usage:
    The verify-citations agent reads these templates and uses them
    to generate exact prompts for sub-agents. The coordinator (sonnet)
    fills in the templates via f-strings; haiku sub-agents execute them.
"""

# ── Coordinator prompt ──────────────────────────────────────────────
# Launched by the top-level agent, one per document section.
# Model: sonnet

COORDINATOR = """
You are a coordinator agent verifying claims in a research document.

Read {file_path}, lines {start_line} through {end_line}.

Extract every cited paper with its URL and the specific claim made about it.

Then execute the two-step verification below using EXACT templated prompts.
Generate each sub-agent prompt by reading the READER_TEMPLATE and CHECKER_TEMPLATE
from {template_file} and filling in the variables with Python f-strings.

## Step 1: Reader agents

For each paper, launch a **haiku** Agent with the prompt from READER_TEMPLATE,
filling in {{url}} with the paper's URL.

Launch ALL reader agents **in parallel**. Wait for all to complete.

## Step 2: Checker agents

After ALL readers return, launch a **haiku** Agent for each paper with the prompt
from CHECKER_TEMPLATE, filling in {{blind_summary}} (from the reader) and
{{claim}} (the exact text from the document about this paper).

Launch ALL checker agents **in parallel**. Wait for all to complete.

## Step 3: Compile report

After all checkers return, compile:

| Paper | Status | Issues |
|-------|--------|--------|

List critical errors first, then precision issues, then unverifiable items.
Count: X verified, Y flagged, Z couldn't verify.
"""


# ── Reader sub-agent prompt ─────────────────────────────────────────
# Launched by coordinator, one per source URL.
# Model: haiku

READER_TEMPLATE = """
Use the WebFetch tool to fetch {url}

Do NOT use any other tool. Do NOT use Codex, WebSearch, mcp__codex__codex,
or any MCP tool. If WebFetch fails, try {url_fallback} or report failure.

Summarize what you find:
- Paper/method name
- Authors (full list)
- Venue and year
- What the method does (1-2 sentences)
- Key quantitative results (exact numbers from the page)

Return ONLY the structured summary. Do not editorialize or add interpretation.
"""


# ── Checker sub-agent prompt ────────────────────────────────────────
# Launched by coordinator after readers complete.
# Model: haiku

CHECKER_TEMPLATE = """
You are comparing a blind paper summary against a claim. Do NOT use any tools.

## Blind summary (from fetching the actual paper):
{blind_summary}

## Claim to verify:
{claim}

Compare and report on each:
1. Authors — correct?
2. Venue/year — correct?
3. Quantitative numbers — accurate?
4. Method description — accurate?
5. Any misattributions or overstatements?

Return one of: VERIFIED / FLAGGED / COULDN'T VERIFY
With a one-line explanation per category.
"""


# ── Summarizer sub-agent prompt (for repos/datasets) ────────────────
# Model: haiku

SUMMARIZER_TEMPLATE = """
Use the WebFetch tool to fetch {url}

Do NOT use any other tool. Do NOT use Codex, WebSearch, mcp__codex__codex,
or any MCP tool. If WebFetch fails, report failure.

Summarize this resource:
- What it is (code repo, dataset, benchmark)
- What it contains
- Key stats (size, number of examples, tasks, languages)
- What it is used for

Return a 2-3 sentence factual summary.
"""


# ── Formatter sub-agent prompt (for repos/datasets) ─────────────────
# Model: haiku

FORMATTER_TEMPLATE = """
Do NOT use any tools. Just reformat the summary below.

## Raw summary:
{raw_summary}

Condense into exactly 1-2 sentences for a research document.
Format: [Name](URL) — summary.
Keep it factual. No editorializing.
"""
