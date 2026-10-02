@~/Mao/claude-toolkit/AGENTS.md

# Claude Code only

- The shared toolkit is pulled at session start by a hook. Use `/sync-learnings`
  at the end of a session to commit and push new learnings.
- After the user approves a commit, the `commit-push` agent may stage, commit,
  and push it. `/ship` runs the same ask-first flow.
- Testing agents. Name the exact test files or functions to run.
  - `test-and-fix`: runs the named tests and fixes the implementation only, never
    the tests. Use when a change could break existing behavior.
  - `write-tests`: writes new tests to a spec and fixes until they pass. Use for
    new logic worth protecting, not for wiring, UI, or config.
