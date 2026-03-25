---
model: haiku
description: Verify claims and citations in a research document using blind two-step checking. Use when the user wants to fact-check a synthesis doc, lit review, or any document with paper citations.
---

Hierarchical citation verification. You are the **top-level orchestrator** — you
do NOT read the document yourself. You delegate everything to sub-agents.

## Named sub-agents (tool-restricted)

These agents have explicit tool allowlists — no MCP tools (Codex etc.):

| Agent name | Model | Tools | Purpose |
|-----------|-------|-------|---------|
| `citation-reader` | haiku | Read, WebFetch, Bash | Blind-fetch one URL, summarize |
| `citation-checker` | haiku | Read | Compare blind summary vs claim |
| `citation-venue-checker` | haiku | Read, WebFetch, WebSearch, Bash | Verify venue/year via web search |
| `citation-summarizer` | haiku | Read, WebFetch, Bash | Fetch and summarize one repo/dataset |

## Templates

Prompt templates in `~/Mao/claude-toolkit/templates/verify-citations/`:

| File | Filled by | Passed to | Placeholders |
|------|----------|-----------|-------------|
| `coordinator.txt` | Orchestrator (you) | haiku coordinator Agent | `{file_path}`, `{start_line}`, `{end_line}`, `{reader_template_path}`, `{checker_template_path}` |
| `reader.txt` | Coordinator | `citation-reader` agent | `{url}`, `{url_fallback}` |
| `checker.txt` | Coordinator | `citation-checker` agent | `{blind_summary}`, `{claim}` |
| `summarizer.txt` | Coordinator | `citation-summarizer` agent | `{url}` |
| `formatter.txt` | Coordinator | `citation-checker` agent (reused) | `{raw_summary}` |

**Context optimization**: No agent loads another agent's template. Every level
uses Bash/Python to read the template, fill placeholders, and pass the result
as the sub-agent prompt.

## Workflow

1. Launch a **haiku splitter agent** that reads the target document, identifies
   sections containing citations, and returns a list of `(section_name, start_line, end_line)`.

2. For each section, use Bash to read `coordinator.txt` and fill placeholders:
   ```
   python3 -c "
   t = open('coordinator.txt').read()
   print(t.format(file_path=..., start_line=..., end_line=...,
                  reader_template_path=..., checker_template_path=...))
   "
   ```
   Launch a **haiku coordinator** Agent with the output. Run all in parallel.

3. Each coordinator:
   - Reads its document section and extracts papers + claims
   - Uses Bash/Python to fill `reader.txt` → launches `citation-reader` agents (parallel)
   - Waits for readers, fills `checker.txt` → launches `citation-checker` agents (parallel)
   - Returns ONLY flagged items + verified count

4. Collect coordinator reports and present consolidated summary.

## Incremental mode

For re-checking after fixes, pass a paper list to the coordinator:
> Only check these specific papers: {paper_list}. Skip all others.

## Venue verification follow-up

For papers where venue couldn't be confirmed from arxiv abstracts, launch
`citation-venue-checker` agents with WebSearch access.

## For repo/dataset summarization

Same pattern with `citation-summarizer` agents and `summarizer.txt` → `formatter.txt`.

## Known issues

- Tool restrictions via `tools` field may not enforce in `bypassPermissions` mode.
- arxiv abstract pages often lack venue info — use venue-checker follow-up.
- Full paper text at `arxiv.org/html/{id}v1` — use as `{url_fallback}`.
