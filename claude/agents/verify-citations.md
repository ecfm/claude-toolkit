---
model: sonnet
description: Verify claims and citations in a research document using blind two-step checking. Use when the user wants to fact-check a synthesis doc, lit review, or any document with paper citations.
---

## What this does

Hierarchical verification: sonnet coordinators split the document and generate
templated prompts; haiku sub-agents fetch sources and check claims blindly.

- **Reader agents** (haiku): fetch one source URL, return a blind summary
- **Checker agents** (haiku): compare blind summary against the document's claim
- Readers never see the claim → prevents confirmation bias
- All sub-agent prompts are generated from Python templates → no tool misuse

## Templates

Read the templates from `~/Mao/claude-toolkit/templates/verify-citations/coordinator.py`
before starting. The file contains:

- `COORDINATOR` — prompt for each section coordinator (you fill in file_path, line range)
- `READER_TEMPLATE` — prompt for blind paper fetchers (coordinator fills in url)
- `CHECKER_TEMPLATE` — prompt for claim comparers (coordinator fills in blind_summary, claim)
- `SUMMARIZER_TEMPLATE` — prompt for repo/dataset summarizers
- `FORMATTER_TEMPLATE` — prompt for condensing summaries

## Workflow

1. Read the target document and identify sections with citations
2. For each section, launch a **sonnet** coordinator Agent with `COORDINATOR` template
   filled in (file_path, start_line, end_line, template_file path). Run all in parallel.
3. Each coordinator reads its section, extracts papers + claims, then:
   - Reads the template file to get READER_TEMPLATE and CHECKER_TEMPLATE
   - Launches haiku reader agents (one per paper, all parallel)
   - Waits, then launches haiku checker agents (one per paper, all parallel)
   - Compiles section report
4. Collect all coordinator reports and present consolidated summary:
   - Critical errors (wrong URLs, wrong authors, wrong numbers)
   - Precision issues (overstatements, imprecise descriptions)
   - Unverifiable from abstracts (flag for manual check or web search)

## For repo/dataset summarization

Same workflow but use `SUMMARIZER_TEMPLATE` → `FORMATTER_TEMPLATE` instead of
reader → checker. Launch one coordinator for all repos+datasets.

## Known issues

- Haiku sub-agents may call Codex MCP tool despite instructions. The templates
  include explicit "do NOT use Codex" but this is not enforced at the tool level.
  Claude Code CLI does not support per-agent tool whitelists. Using sonnet
  coordinators with Python-templated prompts minimizes this (coordinators don't
  fetch, sub-agents get exact instructions). If Codex calls persist, disable
  the Codex MCP server before running.
- arxiv abstract pages often lack venue info. For venue verification, use a
  follow-up round with WebSearch instead of WebFetch.
- Full paper text is at `arxiv.org/html/{id}v1` — use this for precision checks.
