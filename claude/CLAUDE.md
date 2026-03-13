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
Use the `commit-push` agent (Agent tool with subagent_type omitted, or the agent file) for all commits and pushes. Proactively invoke it — without waiting for the user to ask — whenever:
- A feature or task is complete
- Git diff shows 200+ lines changed
- The user says "done", "ship it", "that's it", or similar

Never commit manually with the Bash tool when this agent is available.
