# Paper Triage Agent

Cluster the papers in the directory below into 4-6 thematic groups for parallel processing by downstream reader agents.

## Papers Directory

{{PAPERS_DIR}}

Use Glob to find all papers (*.pdf, *.md, *.tex). Read abstracts (page 1) of the ~15 most relevant-looking papers for better clustering — judge relevance from filenames.

## What to Produce

For each cluster:
- Theme label and 1-sentence description of what threat these papers pose
- Full filenames of papers in the cluster
- Priority: HIGH (strong empirical claims for LLM simulation) / MEDIUM (partial or conditional claims) / LOW (tangential)

**Assign each paper to exactly one cluster.** If a paper spans themes, place it in the cluster where it poses the greatest threat to the manuscript. No duplicates across clusters.

Sort by priority. Aim for roughly balanced cluster sizes (8-15 papers) so downstream agents have similar workloads. Flag outliers that don't fit but might contain novel arguments.
