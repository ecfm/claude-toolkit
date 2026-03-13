---
model: haiku
description: Stage, commit, and push changes. Use when the user asks to commit, push, or "commit and push".
---

Stage relevant modified files (never commit .env, credentials, or large binaries),
write a concise commit message that focuses on the "why" (not just the "what"),
commit, then push. If the push is rejected, pull --rebase first, then push again.

End every commit message with:
Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
