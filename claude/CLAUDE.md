# Shared Learnings
At the start of each session, pull shared learnings: `cd ~/ml-best-practices && git pull --quiet`
Use `/sync-learnings` to commit and push any new learnings at end of session.

# Best Practices Reference (~/ml-best-practices/)
Read the relevant file BEFORE starting that type of work:

| When you are...                    | Read                         |
|------------------------------------|------------------------------|
| Running or planning ML experiments | experiment-practices.md      |
| Designing a new pipeline or method | pipeline-architecture.md     |

# Committing

Use `commit-push` (Haiku agent) for all commits and pushes. Proactively invoke it whenever:
- A feature or task is complete
- Git diff shows 200+ lines changed
- The user says "done", "ship it", "that's it", or similar

Never commit manually with the Bash tool when this agent is available.

**Before committing, decide whether tests are needed:**

| Change type | Action |
|---|---|
| New logic, breaking change, bug fix in critical path | `test-and-fix` → write new tests, run until passing → `commit-push` |
| Refactor or change to code with existing tests | `test-and-fix` → run existing tests only → `commit-push` |
| UI tweaks, config, docs, trivial features, wiring code | `commit-push` directly |

When invoking `test-and-fix`, the outer model provides detailed instructions: what to test, expected behavior, edge cases, and the test command. The agent handles the rest.
